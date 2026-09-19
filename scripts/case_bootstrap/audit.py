"""Decision 123 read-only audit. Findings never create authority or HOLD."""
from pathlib import Path

from . import storage as s
from .contracts import KINDS, record_path
from .operations import Operations, state

FAMILIES = ('SCHEMA','SERIALIZATION','FIXITY','IDENTITY','CROSS_ARTIFACT','TRANSACTION',
            'RECOVERY','LEASE_LIFECYCLE','SEMANTIC_EVENT','NAMESPACE','GOVERNANCE_BOUNDARY')


def audit(root, contracts=None, contextual_validator=None):
    ops=Operations(root,contracts,contextual_validator=contextual_validator)
    findings=[]; records=[]; seen={}; consumed={}
    def finding(code,family,ref,detail='',severity='ERROR'):
        findings.append({'code':code,'family':family,'severity':severity,'ref':ref,'message':str(detail or code)})
    def failed(exc,ref):
        code=getattr(exc,'code','OPERATIONAL_READ_FAILURE')
        family=('SERIALIZATION' if 'SERIALIZATION' in code or code.startswith('JSON_') else
                'FIXITY' if 'FIXITY' in code or 'REFERENCE' in code else
                'IDENTITY' if 'IDENTITY' in code or 'ACTOR' in code else
                'SCHEMA' if code.startswith('SCHEMA') else
                'RECOVERY' if 'RECOVERY' in code or 'HUMAN' in code else
                'LEASE_LIFECYCLE' if 'LEASE' in code else
                'SEMANTIC_EVENT' if 'EVENT' in code else 'CROSS_ARTIFACT')
        finding(code,family,ref,str(exc))
    base=s.path_at(ops.root,'.projectorigin')
    paths=sorted(base.rglob('*.json')) if base.exists() else []
    canonical_dirs={v[2] for v in KINDS.values()}
    raw_resolutions=[]
    for path in paths:
        ref=path.relative_to(ops.root).as_posix()
        if ref.split('/')[1] not in canonical_dirs:
            continue
        try:
            raw=s.parse_json(s.read_bytes(ops.root,ref))
            if isinstance(raw,dict) and raw.get('artifact_type') in KINDS:
                kind=raw['artifact_type'];field=KINDS[kind][1]
                identity=(kind,raw.get(field))
                if identity in seen:
                    finding('IMMUTABLE_IDENTITY_COLLISION','IDENTITY',ref,seen[identity])
                seen[identity]=ref
                if kind=='LEASE_RELEASE_RESOLUTION':
                    raw_resolutions.append((ref,raw))
            if isinstance(raw,dict) and raw.get('artifact_type')=='RECOVERY_DETERMINATION':
                from .recovery import evaluate
                consistency, determination = evaluate(raw['evidence'])
                if consistency != raw['evidence']['consistency'] or determination != raw['determination']:
                    finding('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH','RECOVERY',ref)
            record=ops.read(ref)
            records.append(record)
            ops.check_links(record)
        except (s.OperationalError,OSError,ValueError,KeyError,TypeError) as exc:
            failed(exc,ref)
    # Detect topology independently of SHA-validity, so corrupt cycles/branches
    # are reported rather than hidden behind their inevitable fixity errors.
    graph={ref:raw.get('predecessor_ref') for ref,raw in raw_resolutions}
    successors={}
    for ref,raw in raw_resolutions:
        parent=raw.get('predecessor_ref')
        if parent in successors:
            finding('LEASE_RELEASE_RESOLUTION_BRANCH','LEASE_LIFECYCLE',ref)
        successors[parent]=ref
        visited=set(); cursor=ref
        while cursor in graph:
            if cursor in visited:
                finding('LEASE_RELEASE_RESOLUTION_CYCLE','LEASE_LIFECYCLE',ref)
                break
            visited.add(cursor);cursor=graph[cursor]
    namespaces={}
    writers={}
    for record in records:
        if record['artifact_type']=='TRANSACTION_RECEIPT':
            for result in record['write_results']:
                writers.setdefault(result['target_path'],[]).append((record,result))
    for target, entries in writers.items():
        if len(entries)==1 and entries[0][0]['terminal_outcome']=='COMMITTED':
            try:
                if state(ops.root,target)!=entries[0][1]['post_write_state']:
                    finding('CURRENT_TARGET_FIXITY_MISMATCH','FIXITY',target)
            except (s.OperationalError,OSError) as exc:
                failed(exc,target)
        elif len(entries)>1:
            finding('HISTORICAL_TARGET_COMPARISON_NOT_APPLICABLE','TRANSACTION',target,severity='INFO')
    for record in records:
        kind=record['artifact_type'];ref=record_path(record);case=record['case_id']
        if kind in ('TRANSACTION_ALLOCATION','RECOVERY_DETERMINATION','RECOVERY_AUTHORIZATION','LEASE_RELEASE_RESOLUTION'):
            key=(case,kind);identity=record[KINDS[kind][1]]
            namespaces.setdefault(key,[]).append(int(identity.rsplit('-',1)[1]))
        if kind=='TRANSACTION_ALLOCATION' and record['transaction_origin']=='RECOVERY_CONTINUATION':
            key=record['recovery_context']['recovery_authorization_ref']
            if key in consumed:
                finding('RECOVERY_AUTHORIZATION_ALREADY_CONSUMED','RECOVERY',ref,consumed[key])
            consumed[key]=ref
        if kind=='LEASE_RELEASE_RECORD':
            try:
                ops.chain(record)
            except (s.OperationalError,OSError,KeyError) as exc:
                failed(exc,ref)
        if kind=='TRANSACTION_RECEIPT':
            lease=record['lease_evidence']
            lease_path=s.path_at(ops.root,lease['lease_path'])
            if not lease_path.exists():
                finding('HISTORICAL_EPHEMERAL_LEASE_UNAVAILABLE','LEASE_LIFECYCLE',ref,severity='WARNING')
            release_ref='.projectorigin/lease-releases/'+case+'/'+record['transaction_id']+'.json'
            if not s.path_at(ops.root,release_ref).exists():
                finding('LEASE_RELEASE_EVIDENCE_UNAVAILABLE','LEASE_LIFECYCLE',ref,severity='WARNING')
        if kind=='TRANSACTION_JOURNAL' and record['state'] not in ('COMMITTED','ABORTED','RECOVERY_REQUIRED'):
            finding('TRANSACTION_NONTERMINAL','TRANSACTION',ref,severity='WARNING')
    for (case,kind),serials in namespaces.items():
        if sorted(set(serials))!=list(range(1,max(serials)+1)):
            finding('PERMITTED_SERIAL_GAP','NAMESPACE',case+'/'+kind,severity='WARNING')
    events_by_case={}
    cases=s.path_at(ops.root,'cases')
    for path in sorted(cases.glob('FILE-*/semantic-events/*.json')) if cases.exists() else []:
        ref=path.relative_to(ops.root).as_posix();case=path.parents[1].name
        try:
            data=s.read_bytes(ops.root,ref);event=s.parse_json(data)
            ops.contracts.validate_event(event,data)
            s.validate_id(event['event_id'],'EVT',case)
            if path.stem!=event['event_id']:
                s.reject('SEMANTIC_EVENT_IDENTITY_MISMATCH')
            ops.contracts.validate_definition('operationalActorId',event['actor_id'])
            ops.contracts.validate_definition('operationalActorRole',event['actor_role'])
            ops.contracts.validate_definition('eventType',event['event_type'])
            ops.contracts.validate_definition('artifactReference',event['record_ref'])
            from .contextual import check_event
            check_event(ops,ref,event)
            events_by_case.setdefault(case,[]).append({'event_id':event['event_id'],'event_type':event['event_type'],'record_ref':event['record_ref'],'occurred_at':event['occurred_at'],'event_path':ref,'event_sha256':s.sha256(data)})
        except (s.OperationalError,OSError,ValueError,KeyError,TypeError) as exc:
            failed(exc,ref)
    for case,events in events_by_case.items():
        serials=[int(event['event_id'].rsplit('-',1)[1]) for event in events]
        if sorted(set(serials))!=list(range(1,max(serials)+1)):
            finding('PERMITTED_SERIAL_GAP','NAMESPACE',case+'/EVT',severity='WARNING')
    index_dir=s.path_at(ops.root,'.projectorigin/index/semantic-events')
    index_cases={p.stem for p in index_dir.glob('*.json')} if index_dir.exists() else set()
    for case in sorted(set(events_by_case)|index_cases):
        ref='.projectorigin/index/semantic-events/'+case+'.json'
        try:
            actual=s.parse_json(s.read_bytes(ops.root,ref))
        except (s.OperationalError,OSError):
            actual=None
        if actual!=events_by_case.get(case,[]):
            finding('DERIVED_INDEX_STALE','SEMANTIC_EVENT',ref,severity='WARNING')
    # Audit applicable manifests even when no operational records remain.
    from .contextual import integrity
    manifests={p.relative_to(ops.root).as_posix():[] for p in sorted(cases.glob('FILE-*/orchestration-manifest.json'))} if cases.exists() else {}
    for record in records:
        if record['artifact_type'] in ('TRANSACTION_JOURNAL','TRANSACTION_RECEIPT'):
            for intent in record.get('write_intent',record.get('write_results',[])):
                if intent.get('role')=='MANIFEST':
                    manifests[intent['target_path']]=record['required_semantic_events']
    for ref, events in sorted(manifests.items()):
        result=integrity(ops,ref,'MANIFEST',events)
        for code in result['findings']:
            finding(code,'CROSS_ARTIFACT',ref)
    if base.exists():
        for path in sorted(base.rglob('*.tmp')):
            finding('NONAUTHORITATIVE_TEMP_DEBRIS','NAMESPACE',path.relative_to(ops.root).as_posix(),severity='WARNING')
    if not records:
        finding('NO_OPERATIONAL_RECORDS','TRANSACTION','.projectorigin',severity='INFO')
    findings.sort(key=lambda f:(f['ref'],f['family'],f['code'],f['severity'],f['message']))
    counts={severity:sum(f['severity']==severity for f in findings) for severity in ('ERROR','WARNING','INFO')}
    return {'overall_status':'FAIL' if counts['ERROR'] else 'PASS_WITH_WARNINGS' if counts['WARNING'] else 'PASS',
            'counts':counts,'findings':findings,'records_checked':len(records),'families':list(FAMILIES),
            'authority_boundary':'Structural declarations only; no authentication, approval, repair, or HOLD.'}
