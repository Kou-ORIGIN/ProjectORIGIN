"""DR06 read-only observations and deterministic historical evidence evaluation."""
from . import storage as s

UNKNOWN = {'existence': 'UNDETERMINED', 'sha256': None}
ABSENT = {'existence': 'ABSENT', 'sha256': None}


def observed_state(root, path):
    from .operations import state
    try:
        return state(root, path)
    except (s.OperationalError, OSError):
        try:
            s.path_at(root,path).stat()
            return {'existence':'EXISTS','sha256':None}
        except (s.OperationalError,OSError):
            return dict(UNKNOWN)


def observe(ops, path, case, transaction=None):
    observation = {'target_path': path, 'state': observed_state(ops.root, path),
                   'validation': 'ABSENT', 'data': None, 'findings': []}
    existence = observation['state']['existence']
    if existence == 'ABSENT':
        return observation
    if existence == 'UNDETERMINED' or existence == 'EXISTS' and observation['state']['sha256'] is None:
        observation['validation'] = 'UNAVAILABLE'
        return observation
    try:
        value = ops.read(path, observation['state']['sha256'])
        if value['case_id'] != case or transaction is not None and value['transaction_id'] != transaction:
            s.reject('RECOVERY_OBSERVATION_IDENTITY_MISMATCH')
        ops.check_links(value)
        observation.update(validation='VALID', data=value)
    except OSError as exc:
        observation.update(validation='UNAVAILABLE', findings=[type(exc).__name__])
    except (s.OperationalError, ValueError, KeyError, TypeError) as exc:
        observation.update(validation='INVALID', findings=[getattr(exc, 'code', type(exc).__name__)])
    return observation


def basis(evidence):
    """Derive full mutation scope from validated embedded records, never labels."""
    journal = evidence['journal_observation']['data'] if evidence['journal_observation']['validation'] == 'VALID' else None
    receipt = evidence['receipt_observation']['data'] if evidence['receipt_observation']['validation'] == 'VALID' else None
    paths = {}
    if journal:
        pre = {p['target_path']: p for p in journal['preconditions']}
        for item in journal['write_intent']:
            p = pre[item['target_path']]
            before = dict(ABSENT) if p['existence'] == 'MUST_NOT_EXIST' else ({'existence': 'EXISTS', 'sha256': p['sha256']} if p['sha256'] else dict(UNKNOWN))
            after = dict(ABSENT) if item['operation'] == 'DELETE' else ({'existence': 'EXISTS', 'sha256': item['prospective_sha256']} if item['prospective_sha256'] else dict(UNKNOWN))
            paths[item['target_path']] = {**{k: item[k] for k in ('target_path', 'operation', 'role')}, 'expected_pre_transaction_state': before, 'expected_committed_state': after}
    if receipt:
        for result in receipt['write_results']:
            path = result['target_path']
            # Receipt's observed post-state is the DR06 fallback when Journal is absent.
            if path not in paths:
                role = result.get('role', 'SEMANTIC_EVENT' if '/semantic-events/' in path else ('MANIFEST' if path.endswith('/orchestration-manifest.json') else 'CANONICAL_TARGET'))
                paths[path] = {'target_path': path, 'operation': result['operation'], 'role': role,
                              'expected_pre_transaction_state': result['pre_write_state'], 'expected_committed_state': result['post_write_state']}
    return paths, journal, receipt


def comparison(actual, before, after):
    if any(v['existence'] == 'UNDETERMINED' or v['existence'] == 'EXISTS' and not v['sha256'] for v in (actual, before, after)):
        return 'INSUFFICIENT'
    pre, post = actual == before, actual == after
    return 'MATCHES_BOTH' if pre and post else 'MATCHES_PRE' if pre else 'MATCHES_COMMITTED' if post else 'CONFLICTING'


def evaluate(evidence):
    """Pure DR06 truth table; suitable for publication and independent audit use."""
    paths, journal, receipt = basis(evidence)
    observations = evidence['canonical_observations']
    invalid = any(evidence[k+'_observation']['validation'] == 'INVALID' for k in ('allocation','journal','receipt','lease'))
    insufficient = any(evidence[k+'_observation']['validation'] == 'UNAVAILABLE' for k in ('allocation','journal','receipt','lease'))
    insufficient |= evidence['allocation_observation']['validation'] != 'VALID'
    invalid |= any(not f.startswith('UNAVAILABLE:') for f in evidence['prior_observation_findings'])
    insufficient |= any(f.startswith('UNAVAILABLE:') for f in evidence['prior_observation_findings'])
    if journal and receipt:
        invalid |= journal['state'] != receipt['terminal_outcome'] or journal['state'] not in ('COMMITTED','ABORTED','RECOVERY_REQUIRED')
        invalid |= {p['target_path'] for p in journal['write_intent']} != {p['target_path'] for p in receipt['write_results']}
        invalid |= journal['required_semantic_events'] != receipt['required_semantic_events']
        invalid |= journal['lease_binding'] != {k:receipt['lease_evidence'][k] for k in journal['lease_binding']}
        for result in receipt['write_results']:
            item = paths.get(result['target_path'])
            if item:
                # An aborted precondition conflict legitimately records observed pre-state
                # differing from the requested CREATE precondition. It remains a conflict.
                invalid |= result['operation'] != item['operation']
                if receipt['terminal_outcome'] == 'COMMITTED':
                    invalid |= result['post_write_state'] != item['expected_committed_state']
    invalid |= len(observations) != len({o['target_path'] for o in observations})
    invalid |= {o['target_path'] for o in observations} != set(paths)
    kinds = []
    for o in observations:
        expected = paths.get(o['target_path'])
        if expected is None:
            continue
        invalid |= any(o[k] != val for k, val in expected.items())
        result = comparison(o['actual_state'], expected['expected_pre_transaction_state'], expected['expected_committed_state'])
        invalid |= result != o['comparison']
        kinds.append(result)
    invalid |= any(r['status'] == 'INVALID' for r in evidence['integrity_results'])
    insufficient |= any(r['status'] == 'UNAVAILABLE' for r in evidence['integrity_results'])
    required = (journal or receipt or {}).get('required_semantic_events', [])
    # Every applicable event/manifest must have a recorded check, including missing ones.
    case = evidence['allocation_observation']['data']['case_id'] if evidence['allocation_observation']['data'] else None
    needed = {p for p, item in paths.items() if item['role'] in ('SEMANTIC_EVENT','MANIFEST')}
    if case:
        needed |= {'cases/'+case+'/semantic-events/'+event['event_id']+'.json' for event in required}
    invalid |= not needed.issubset({r['target_path'] for r in evidence['integrity_results']})
    invalid |= len(evidence['integrity_results']) != len({r['target_path'] for r in evidence['integrity_results']})
    actuals={o['target_path']:o['actual_state'] for o in observations}
    for check in evidence['integrity_results']:
        path=check['target_path']
        if check['status']=='NOT_APPLICABLE':
            item=paths.get(path)
            invalid |= not (item and item['role']=='MANIFEST' and actuals.get(path)==ABSENT and (item['expected_pre_transaction_state']==ABSENT or item['expected_committed_state']==ABSENT))
        if check['status']=='VALID':
            invalid |= not check['sha256'] or bool(check['findings'])
            if path in actuals:
                invalid |= actuals[path] != {'existence':'EXISTS','sha256':check['sha256']}

    invalid |= 'CONFLICTING' in kinds or ('MATCHES_PRE' in kinds and 'MATCHES_COMMITTED' in kinds)
    if journal and not journal['commit_window']['entered'] and 'MATCHES_COMMITTED' in kinds:
        invalid = True
    insufficient |= any(o['actual_state']['existence']=='UNDETERMINED' or o['actual_state']['existence']=='EXISTS' and o['actual_state']['sha256'] is None for o in observations)
    insufficient |= 'INSUFFICIENT' in kinds or not (journal or receipt)
    if invalid:
        consistency = 'CONFLICTING_STATE'
    elif insufficient:
        consistency = 'INSUFFICIENT_EVIDENCE'
    elif not paths:
        consistency = 'NOT_APPLICABLE'
    elif 'MATCHES_COMMITTED' in kinds:
        consistency = 'MATCHES_COMMITTED_STATE'
    elif 'MATCHES_PRE' in kinds:
        consistency = 'MATCHES_PRE_TRANSACTION_STATE'
    else:
        terminal = receipt['terminal_outcome'] if receipt else journal['state']
        consistency = 'MATCHES_COMMITTED_STATE' if terminal == 'COMMITTED' else 'MATCHES_PRE_TRANSACTION_STATE'
    lease = evidence['lease_observation']['state']['existence']
    determination = ('UNSAFE_TO_PROCEED' if invalid or lease == 'EXISTS' else
                     'UNDETERMINED' if insufficient or lease == 'UNDETERMINED' else
                     'SAFE_TO_START_NEW_TXN' if lease == 'ABSENT' else 'UNSAFE_TO_PROCEED')
    return consistency, determination


def validate_snapshot(contracts, value):
    """Check internal fixity/identity and recompute labels without rereading history."""
    e = value['evidence']
    allocation = e['allocation_observation']['data']
    for name in ('allocation','journal','receipt','lease'):
        o = e[name+'_observation']; data = o['data']; existence = o['state']['existence']
        if o['validation'] == 'VALID':
            if data is None or existence != 'EXISTS':
                s.reject('RECOVERY_EVIDENCE_INVALID')
            contracts.validate(data)
            if s.sha256(contracts.encode(data)) != o['state']['sha256']:
                s.reject('RECOVERY_SNAPSHOT_FIXITY_MISMATCH')
            from .contracts import record_path
            if record_path(data) != o['target_path'] or data['case_id'] != value['case_id']:
                s.reject('RECOVERY_EVIDENCE_IDENTITY_MISMATCH')
            if name != 'lease' and data['transaction_id'] != value['prior_transaction_id']:
                s.reject('RECOVERY_EVIDENCE_IDENTITY_MISMATCH')
            if name in ('journal','receipt') and allocation:
                binding = data['lease_binding' if name == 'journal' else 'lease_evidence']
                if binding['allocation_record_ref'] != e['allocation_record_ref'] or binding['allocation_record_sha256'] != e['allocation_record_sha256'] or binding['lease_path'] != '.projectorigin/leases/'+value['case_id']+'.json':
                    s.reject('RECOVERY_EVIDENCE_BINDING_MISMATCH')
                if (data['initiated_by_actor_id'],data['initiated_by_actor_role']) != (allocation['allocated_by_actor_id'],allocation['allocated_by_actor_role']):
                    s.reject('RECOVERY_EVIDENCE_BINDING_MISMATCH')
                if name=='journal' and data.get('recovery_context') != allocation.get('recovery_context'):
                    s.reject('RECOVERY_EVIDENCE_BINDING_MISMATCH')
        elif data is not None or (o['validation'] == 'ABSENT' and existence != 'ABSENT') or (o['validation'] == 'INVALID' and existence != 'EXISTS'):
            s.reject('RECOVERY_EVIDENCE_INVALID')
    if e['allocation_record_ref'] != e['allocation_observation']['target_path'] or e['allocation_record_sha256'] != e['allocation_observation']['state']['sha256']:
        s.reject('RECOVERY_EVIDENCE_BINDING_MISMATCH')
    journal = e['journal_observation']['data']; receipt = e['receipt_observation']['data']
    if e['journal_state'] != (journal['state'] if journal else None) or e['journal_sha256'] != e['journal_observation']['state']['sha256']:
        s.reject('RECOVERY_EVIDENCE_BINDING_MISMATCH')
    if e['receipt_ref'] != (e['receipt_observation']['target_path'] if receipt else None) or e['receipt_sha256'] != e['receipt_observation']['state']['sha256']:
        s.reject('RECOVERY_EVIDENCE_BINDING_MISMATCH')
    consistency, determination = evaluate(e)
    if consistency != e['consistency'] or determination != value['determination']:
        s.reject('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH')


def _legacy_committed_mvr_event_compatibility(ops, path, events, paths, journal, receipt):
    """Accept one historical committed MVR Event missing only artifact_id.

    This is recovery-inspection compatibility only. It never mutates bytes and
    it does not weaken the general contextual reference contract.
    """
    if not journal or not receipt or journal.get('state') != 'COMMITTED' or receipt.get('terminal_outcome') != 'COMMITTED':
        return None
    item = paths.get(path)
    if not item or item.get('role') != 'SEMANTIC_EVENT' or item.get('operation') != 'CREATE':
        return None
    committed = item.get('expected_committed_state')
    actual = observed_state(ops.root, path)
    if not committed or committed.get('existence') != 'EXISTS' or not committed.get('sha256') or actual != committed:
        return None
    try:
        raw = s.read_bytes(ops.root, path)
        if s.sha256(raw) != committed['sha256']:
            return None
        event = s.parse_json(raw)
        ops.contracts.validate_event(event, raw)
        case = path.split('/')[1]
        s.validate_id(event['event_id'], 'EVT', case)
        if path != 'cases/'+case+'/semantic-events/'+event['event_id']+'.json':
            return None

        required = [v for v in events if v.get('event_id') == event['event_id']]
        if len(required) != 1 or any(required[0][k] != event[k] for k in ('event_type','record_ref')):
            return None

        from .contextual import references, check_reference
        refs = list(references(event))
        record_ref = event.get('record_ref')
        if record_ref not in refs or record_ref.get('artifact_id') is not None:
            return None
        if not record_ref.get('repository_path') or not record_ref.get('sha256') or record_ref.get('artifact_type') != 'MECHANICAL_VALIDATION_RECORD':
            return None

        target_path = record_ref['repository_path']
        target_item = paths.get(target_path)
        if not target_item or target_item.get('role') != 'CANONICAL_TARGET' or target_item.get('operation') != 'CREATE':
            return None
        target_committed = target_item.get('expected_committed_state')
        target_actual = observed_state(ops.root, target_path)
        if not target_committed or target_committed.get('existence') != 'EXISTS' or target_actual != target_committed:
            return None
        if record_ref['sha256'] != target_committed.get('sha256'):
            return None

        target_raw = s.read_bytes(ops.root, target_path)
        if s.sha256(target_raw) != record_ref['sha256']:
            return None
        target = s.parse_json(target_raw)
        if target.get('artifact_type') != 'MECHANICAL_VALIDATION_RECORD' or target.get('transaction_id') != receipt.get('transaction_id'):
            return None

        inferred = dict(record_ref, artifact_id=receipt['transaction_id'])
        check_reference(ops, inferred)
        for reference in refs:
            if reference is not record_ref:
                check_reference(ops, reference)

        if ops.contextual_validator is not None:
            findings = ops.contextual_validator(path, event)
            if not isinstance(findings, list):
                return None
            if any(f.get('severity','ERROR') == 'ERROR' or f.get('blocking',False) for f in findings):
                return None
        return {'target_path':path,'status':'VALID','sha256':committed['sha256'],'findings':[]}
    except (s.OperationalError, OSError, ValueError, KeyError, TypeError):
        return None


def inspect(ops, case, transaction, identity, role):
    from .operations import now, actor
    from .contextual import integrity
    s.validate_id(transaction, 'TXN', case)
    ops.contracts.validate_definition('operationalActorId', identity)
    ops.contracts.validate_definition('operationalActorRole', role)
    prefix = '.projectorigin/'
    allocation = observe(ops,prefix+'transaction-allocations/'+case+'/'+transaction+'.json',case,transaction)
    journal = observe(ops,prefix+'journals/'+case+'/'+transaction+'.json',case,transaction)
    receipt = observe(ops,prefix+'receipts/'+case+'/'+transaction+'.json',case,transaction)
    lease = observe(ops,prefix+'leases/'+case+'.json',case)
    e = {'allocation_record_ref':allocation['target_path'],'allocation_record_sha256':allocation['state']['sha256'],
         'allocation_observation':allocation,'journal_observation':journal,'receipt_observation':receipt,'lease_observation':lease,
         'journal_state':journal['data']['state'] if journal['data'] else None,'journal_sha256':journal['state']['sha256'],
         'receipt_ref':receipt['target_path'] if receipt['data'] else None,'receipt_sha256':receipt['state']['sha256'],
         'canonical_observations':[],'integrity_results':[],'prior_determination_references':[], 'prior_observation_findings':[],
         'inspected_at':now(),**actor('inspected_by',identity,role)}
    paths,j,r = basis(e)
    for path,item in sorted(paths.items()):
        actual = observed_state(ops.root,path)
        e['canonical_observations'].append({**item,'actual_state':actual,'comparison':comparison(actual,item['expected_pre_transaction_state'],item['expected_committed_state'])})
    events = (j or r or {}).get('required_semantic_events',[])
    checks = {path:item['role'] for path,item in paths.items() if item['role'] in ('SEMANTIC_EVENT','MANIFEST')}
    checks.update({'cases/'+case+'/semantic-events/'+v['event_id']+'.json':'SEMANTIC_EVENT' for v in events})
    for path,kind in sorted(checks.items()):
        item = paths.get(path)
        # No applicable manifest in the validated PRE state of a CREATE/DELETE.
        actual = observed_state(ops.root,path)
        if kind == 'MANIFEST' and item and actual == ABSENT and (item['expected_pre_transaction_state'] == ABSENT or item['expected_committed_state'] == ABSENT):
            result={'target_path':path,'status':'NOT_APPLICABLE','sha256':None,'findings':[]}
        else:
            result=integrity(ops,path,kind,events)
            if (kind == 'SEMANTIC_EVENT' and result.get('status') == 'INVALID' and
                    result.get('findings') == ['CANONICAL_REFERENCE_EVIDENCE_INSUFFICIENT']):
                compatible = _legacy_committed_mvr_event_compatibility(ops,path,events,paths,j,r)
                if compatible is not None:
                    result = compatible
        e['integrity_results'].append(result)
    try:
        for previous in ops.records('RECOVERY_DETERMINATION',case):
            if previous['prior_transaction_id'] == transaction:
                meta=ops.metadata(previous)
                e['prior_determination_references'].append({'ref_id':previous['recovery_determination_id'],'artifact_type':'RECOVERY_DETERMINATION','artifact_id':previous['recovery_determination_id'],'required':False,'applicability':'CONDITIONAL','repository_path':meta['ref'],'sha256':meta['sha256']})
    except OSError as exc:
        e['prior_observation_findings'].append('UNAVAILABLE:'+type(exc).__name__)
    except (s.OperationalError,ValueError,KeyError,TypeError) as exc:
        e['prior_observation_findings'].append(getattr(exc,'code',type(exc).__name__))
    e['consistency'],determination=evaluate(e)
    return {'determination':determination,'evidence':e}
