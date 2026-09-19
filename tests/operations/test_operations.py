"""DR05 and Decisions 84–125 fixtures: all evidence is synthetic and temporary."""
import copy
import json
import multiprocessing
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from case_bootstrap import storage as s
from case_bootstrap.contracts import Contracts, KINDS, record_path
from case_bootstrap.operations import Operations, actor, envelope, binding, now
from case_bootstrap.audit import audit

CASE='FILE-0001'
IDENTITY='ACTOR-0001'
ROLE='Repository / Data Agent'
EXPIRY='2099-01-01T00:00:00Z'
CONTRACTS=Contracts()


def validation(phase,writes):
    # Fixture policy, not production Human authority. Only harmless fixture JSON.
    for w in writes:
        if w['bytes'] is not None:
            json.loads(w['bytes'])
    return {'status':'PASS','layers':{k:'PASS' for k in ('SCHEMA','SEMANTIC','CROSS_ARTIFACT','GOVERNANCE')},'findings':[]}


def writes(name='item.json'):
    return [{'target_path':'cases/'+CASE+'/'+name,'operation':'CREATE','role':'CANONICAL_TARGET','bytes':b'{"fixture": true}\n'}]


def completed(ops,name='item.json'):
    allocation=ops.allocate(CASE,IDENTITY,ROLE)
    lease=ops.acquire(allocation,EXPIRY)
    result=ops.execute(allocation,lease,writes(name),[],validation)
    return allocation,lease,result['receipt'],result['lease_release_record']


def authorization(ops,rdet,namespace='HUMAN-0001',decision='AUTHORIZED'):
    evidence=ops.root/'synthetic-human-decision.txt'
    evidence.write_text('SYNTHETIC TEST DECLARATION ONLY; not real Human authority.\n')
    declaration={**envelope('RECOVERY_AUTHORIZATION',CASE),'prior_transaction_id':rdet['prior_transaction_id'],
                 **binding('recovery_determination',ops.metadata(rdet)),'authorization':decision,
                 **actor('authorized_by',namespace,'Human Approver'),'authorized_at':now(),
                 'human_authority':{'authority_type':'EXPLICIT_HUMAN_DECISION','human_actor_id':namespace},
                 'human_decision_reference':{'ref_id':'synthetic-only','artifact_type':'SYNTHETIC_HUMAN_DECISION','artifact_id':'synthetic-only','required':True,'applicability':'REQUIRED','repository_path':evidence.name,'sha256':s.sha256(evidence.read_bytes())},
                 'rationale':'Synthetic test declaration only.'}
    return ops.record_authorization(declaration)


def recovery_context(ops,rdet,rauth):
    return {'prior_transaction_id':rdet['prior_transaction_id'],**binding('recovery_determination',ops.metadata(rdet)),**binding('recovery_authorization',ops.metadata(rauth))}


def concurrent_worker(root,action,argument,start,queue):
    ops=Operations(root)
    start.wait(20)
    try:
        if action=='allocate':
            result=ops.allocate(argument,IDENTITY,ROLE)['transaction_id']
        elif action=='recovery':
            result=ops.allocate(CASE,IDENTITY,ROLE,argument)['transaction_id']
        elif action=='lease':
            result=ops.acquire(argument,EXPIRY)['transaction_id']
        elif action=='resolve':
            lrel=ops.read(argument)
            result=ops.resolve_release(lrel,argument,IDENTITY,ROLE)['lease_release_resolution_id']
        elif action=='determine':
            result=ops.determine(CASE,argument,IDENTITY,ROLE,'Synthetic inspection')['recovery_determination_id']
        elif action=='authorize':
            rdet=ops.read(argument)
            result=authorization(ops,rdet)['recovery_authorization_id']
        queue.put(('PASS',result))
    except s.OperationalError as exc:
        queue.put(('ERROR',exc.code))


class Base(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.ops=Operations(self.root,CONTRACTS)

    def code(self,code,fn,*args,**kwargs):
        with self.assertRaises(s.OperationalError) as caught:
            fn(*args,**kwargs)
        self.assertEqual(code,caught.exception.code)

    def bundle(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        journal=self.ops.read('.projectorigin/journals/'+CASE+'/'+allocation['transaction_id']+'.json')
        rdet=self.ops.determine(CASE,allocation['transaction_id'],IDENTITY,ROLE,'Synthetic recovery assessment')
        rauth=authorization(self.ops,rdet)
        lrres=self.ops.resolve_release(lrel,record_path(lrel),IDENTITY,ROLE)
        return [allocation,lease,journal,receipt,rdet,rauth,lrel,lrres]

    def corrupt(self,value):
        (self.root/record_path(value)).write_bytes(CONTRACTS.encode(value))


class ActorTests(Base):
    def test_human_and_actor_ids(self):
        for value in ('HUMAN-0000','HUMAN-0001','ACTOR-0000','ACTOR-0001','ACTOR-0042'):
            CONTRACTS.validate_definition('operationalActorId',value)

    def test_malformed_namespaces(self):
        for value in ('HUMAN-1','HUMAN-00001','human-0001','HUMAN-0001\n','ACTOR-1','ACTOR-00001','ACTOR-0001\n','AGENT-0001','SYSTEM-0001','user',''):
            with self.subTest(value=value):
                self.code('SCHEMA_ERROR',CONTRACTS.validate_definition,'operationalActorId',value)

    def test_every_role(self):
        roles=CONTRACTS.definition('operationalActorRole')['enum']
        self.assertEqual(14,len(roles))
        for role in roles:
            CONTRACTS.validate_definition('operationalActorRole',role)

    def test_unknown_roles(self):
        for role in ('human approver','Human Approver ','Human  Approver','Repository/Data Agent','Agent','ADMIN',''):
            self.code('SCHEMA_ERROR',CONTRACTS.validate_definition,'operationalActorRole',role)

    def test_no_namespace_role_restriction(self):
        first=self.ops.allocate(CASE,'HUMAN-0001','Research Agent')
        second=self.ops.allocate(CASE,'ACTOR-0001','Human Approver')
        third=self.ops.allocate(CASE,'ACTOR-0001','Audit Agent')
        self.assertEqual('HUMAN-0001',first['allocated_by_actor_id'])
        self.assertEqual(second['allocated_by_actor_id'],third['allocated_by_actor_id'])

    def test_actor_fields_use_central_refs(self):
        found=set()
        def walk(value):
            if isinstance(value,dict):
                for key,child in value.get('properties',{}).items():
                    if key.endswith('_actor_id'):
                        self.assertTrue(child['$ref'].endswith('#/$defs/operationalActorId'));found.add(key)
                    if key.endswith('_actor_role'):
                        self.assertTrue(child['$ref'].endswith('#/$defs/operationalActorRole'));found.add(key)
                for child in value.values():walk(child)
            elif isinstance(value,list):
                for child in value:walk(child)
        for key,value in CONTRACTS.documents.items():
            if key.startswith('urn:projectorigin:schema:operations:'):walk(value)
        self.assertEqual(18,len(found))

    def test_human_id_role_do_not_grant_authority(self):
        rdet=self.bundle()[4]
        good=authorization(self.ops,rdet)
        for key in ('human_authority','human_decision_reference'):
            bad=copy.deepcopy(good);del bad[key]
            self.code('SCHEMA_ERROR',CONTRACTS.validate,bad)

    def test_actor_cannot_supply_explicit_human_authority(self):
        rdet=self.bundle()[4]
        self.code('SCHEMA_ERROR',authorization,self.ops,rdet,'ACTOR-0001')

    def test_no_generated_authority_or_hold(self):
        before=list(self.root.rglob('*'))
        self.code('SCHEMA_ARTIFACT_TYPE',self.ops.record_authorization,{'case_id':CASE})
        self.assertFalse(list(self.root.rglob('*RAUTH-*.json')))
        self.assertFalse(list(self.root.rglob('*HOLD*')))
        self.assertEqual([],before)


class SchemaTests(Base):
    def test_all_nine_schemas_execute(self):
        self.assertEqual(9,len([k for k in CONTRACTS.documents if k.startswith('urn:projectorigin:schema:operations:')]))
        for value in self.bundle():CONTRACTS.validate(value)

    def test_unknown_fields_rejected_all(self):
        for value in self.bundle():
            with self.subTest(kind=value['artifact_type']):
                self.code('SCHEMA_ERROR',CONTRACTS.validate,dict(value,unknown=True))

    def test_missing_fields_rejected_all(self):
        for value in self.bundle():
            bad=dict(value);bad.pop('case_id')
            self.code('SCHEMA_ERROR',CONTRACTS.validate,bad)

    def test_actor_pair_completeness(self):
        for value in self.bundle():
            for key in value:
                if key.endswith('_actor_role'):
                    bad=dict(value);bad.pop(key)
                    self.code('SCHEMA_ERROR',CONTRACTS.validate,bad)

    def test_recovery_context_conditionals(self):
        value=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.code('SCHEMA_ERROR',CONTRACTS.validate,dict(value,transaction_origin='RECOVERY_CONTINUATION'))
        context={'prior_transaction_id':value['transaction_id'],'recovery_determination_ref':'a','recovery_determination_sha256':'0'*64,'recovery_authorization_ref':'b','recovery_authorization_sha256':'0'*64}
        self.code('SCHEMA_ERROR',CONTRACTS.validate,dict(value,recovery_context=context))

    def test_zero_transaction_rejected(self):
        value=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.code('SCHEMA_ERROR',CONTRACTS.validate,dict(value,transaction_id=CASE+'-TXN-0000'))

    def test_nested_closed_world(self):
        receipt=self.bundle()[3]
        receipt['lease_evidence']['unknown']=1
        self.code('SCHEMA_ERROR',CONTRACTS.validate,receipt)

    def test_timestamp_validity(self):
        value=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.code('SCHEMA_ERROR',CONTRACTS.validate,dict(value,allocated_at='2026-99-99T25:00:00Z'))

    def test_operational_roundtrip_deterministic(self):
        for value in self.bundle():
            self.assertEqual(value,s.parse_json(CONTRACTS.encode(value)))
            self.assertEqual(CONTRACTS.encode(value),CONTRACTS.encode(dict(reversed(list(value.items())))))


class SemanticEventAllocationTests(Base):
    def lease(self, case=CASE):
        allocation = self.ops.allocate(case, IDENTITY, ROLE)
        return self.ops.acquire(allocation, EXPIRY)

    def event(self, case, serial):
        return {
            'event_id': case + '-EVT-' + str(serial).zfill(4),
            'occurred_at': '2026-09-18T00:00:00Z',
            'event_type': 'RECORD_CREATED',
            'record_ref': {
                'ref_id': 'fixture',
                'artifact_type': 'FIXTURE',
                'required': False,
                'applicability': 'CONDITIONAL'
            },
            'actor_id': IDENTITY,
            'actor_role': ROLE,
            'authority_type': 'NONE',
            'authority_reference': None,
            'previous_state': None,
            'new_state': None,
            'evidence_references': []
        }

    def write_event(self, case, serial):
        event = self.event(case, serial)
        CONTRACTS.validate_event(event)
        path = self.root / 'cases' / case / 'semantic-events' / (event['event_id'] + '.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(s.serialize(event, CONTRACTS.definition('semanticEvent'), CONTRACTS.resolve))
        return path

    def test_empty_namespace_starts_at_one(self):
        self.assertEqual(CASE + '-EVT-0001', self.ops.next_event_id(CASE, self.lease()))

    def test_existing_event_advances_serial(self):
        lease = self.lease(); self.write_event(CASE, 1)
        self.assertEqual(CASE + '-EVT-0002', self.ops.next_event_id(CASE, lease))

    def test_gap_is_not_reused(self):
        lease = self.lease(); self.write_event(CASE, 1); self.write_event(CASE, 3)
        self.assertEqual(CASE + '-EVT-0004', self.ops.next_event_id(CASE, lease))

    def test_case_isolation(self):
        lease = self.lease(); self.write_event('FILE-0002', 9)
        self.assertEqual(CASE + '-EVT-0001', self.ops.next_event_id(CASE, lease))

    def test_malformed_event_fails_closed(self):
        lease = self.lease()
        path = self.root / 'cases' / CASE / 'semantic-events' / (CASE + '-EVT-0001.json')
        path.parent.mkdir(parents=True); path.write_bytes(b'{}\n')
        self.code('SCHEMA_ERROR', self.ops.next_event_id, CASE, lease)

    def test_namespace_exhaustion(self):
        lease = self.lease(); self.write_event(CASE, 9999)
        self.code('SEMANTIC_EVENT_ID_NAMESPACE_EXHAUSTED', self.ops.next_event_id, CASE, lease)

    def test_missing_active_lease_fails(self):
        lease = self.lease(); (self.root / record_path(lease)).unlink()
        self.code('REFERENCE_TARGET_MISSING', self.ops.next_event_id, CASE, lease)

    def test_foreign_lease_fails(self):
        lease = self.lease('FILE-0002')
        self.code('LEASE_BINDING_MISMATCH', self.ops.next_event_id, CASE, lease)

    def test_stale_lease_fails(self):
        lease = self.lease(); current = copy.deepcopy(lease); current['expires_at'] = '2098-01-01T00:00:00Z'; self.corrupt(current)
        self.code('LEASE_RELEASE_OWNERSHIP_MISMATCH', self.ops.next_event_id, CASE, lease)

    def test_duplicate_identity_fails(self):
        lease = self.lease(); path = self.write_event(CASE, 1)
        original = Path.glob
        def duplicate(directory, pattern):
            found = list(original(directory, pattern))
            return iter(found + found)
        with mock.patch.object(Path, 'glob', duplicate):
            self.code('SEMANTIC_EVENT_DUPLICATE', self.ops.next_event_id, CASE, lease)


class LifecycleTests(Base):
    def test_committed_lifecycle(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        self.assertEqual('COMMITTED',receipt['terminal_outcome'])
        self.assertEqual('RELEASED',lrel['release_outcome'])
        self.assertFalse((self.root/record_path(lease)).exists())
        self.assertEqual('MATCHES_COMMITTED_STATE',self.ops.inspect(CASE,allocation['transaction_id'],IDENTITY,ROLE)['evidence']['consistency'])

    def test_no_validator_no_write(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        self.code('GOVERNANCE_VALIDATOR_REQUIRED',self.ops.execute,allocation,lease,writes(),[],None)
        self.assertFalse((self.root/'cases').exists())

    def test_denied_prospective_aborts(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        def denied(phase,writes):
            result=validation(phase,writes);result['status']='FAIL';result['layers']['GOVERNANCE']='FAIL';return result
        result=self.ops.execute(allocation,lease,writes(),[],denied)
        self.assertEqual('ABORTED',result['receipt']['terminal_outcome'])
        self.assertFalse((self.root/'cases').exists())

    def test_stale_before_commit(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        def inject(phase):
            if phase=='before_commit_recheck':
                p=self.root/'cases'/CASE/'item.json';p.parent.mkdir(parents=True);p.write_text('foreign')
        self.ops.checkpoint=inject
        result=self.ops.execute(allocation,lease,writes(),[],validation)
        self.assertEqual('STALE_WRITE_CONFLICT',result['failure_code'])
        self.assertEqual('RECOVERY_REQUIRED',result['receipt']['terminal_outcome'])
        self.assertEqual('foreign',(self.root/'cases'/CASE/'item.json').read_text())

    def test_partial_mutation_requires_recovery(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        plan=writes()+writes('second.json')
        def inject(phase):
            if phase.endswith('second.json'):raise OSError('injected')
        self.ops.checkpoint=inject
        result=self.ops.execute(allocation,lease,plan,[],validation)
        self.assertEqual('RECOVERY_REQUIRED',result['receipt']['terminal_outcome'])

    def test_manifest_last(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        plan=writes('manifest.json')+writes();plan[0]['role']='MANIFEST'
        observed=[];self.ops.checkpoint=lambda phase:observed.append(phase) if phase.startswith('before_target:') else None
        result=self.ops.execute(allocation,lease,plan,[],validation)
        self.assertEqual('COMMITTED',result['receipt']['terminal_outcome'])
        self.assertTrue(observed[-1].endswith('manifest.json'))

    def test_required_event_failure_prohibits_commit(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        event={'event_id':CASE+'-EVT-0001','event_type':'RECORD_CREATED','record_ref':{'ref_id':'fixture','artifact_type':'FIXTURE','required':True,'applicability':'REQUIRED'}}
        result=self.ops.execute(allocation,lease,writes(),[event],validation)
        self.assertEqual('ABORTED',result['receipt']['terminal_outcome'])

    def test_terminal_journal_cannot_resume(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        journal=self.ops.read('.projectorigin/journals/'+CASE+'/'+allocation['transaction_id']+'.json')
        bad=dict(journal,state='VALIDATING')
        self.code('JOURNAL_TERMINAL_IMMUTABLE',self.ops.write_journal,bad,journal)

    def test_serials_never_reused_after_lease_conflict(self):
        first=self.ops.allocate(CASE,IDENTITY,ROLE);self.ops.acquire(first,EXPIRY)
        second=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.code('CASE_WRITE_LEASE_CONFLICT',self.ops.acquire,second,EXPIRY)
        third=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.assertTrue(third['transaction_id'].endswith('0003'))

    def test_expired_lease_not_takeover(self):
        first=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(first,EXPIRY)
        lease['acquired_at']='2000-01-01T00:00:00Z';lease['expires_at']='2001-01-01T00:00:00Z';self.corrupt(lease)
        second=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.code('CASE_WRITE_LEASE_CONFLICT',self.ops.acquire,second,EXPIRY)
        self.assertEqual(lease,self.ops.read(record_path(lease)))

    def test_allocation_actor_binding(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        bad=dict(lease,holder_actor_id='ACTOR-0042')
        self.code('ACTOR_BINDING_MISMATCH',self.ops.check_links,bad)

    def test_recovery_readonly(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result=self.ops.inspect(CASE,allocation['transaction_id'],IDENTITY,ROLE)
        after={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual('SAFE_TO_START_NEW_TXN',result['determination']);self.assertEqual(before,after)

    def test_missing_receipt_not_abort_proof(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE)
        self.assertEqual('UNDETERMINED',self.ops.inspect(CASE,allocation['transaction_id'],IDENTITY,ROLE)['determination'])

    def test_recovery_safe_requires_no_active_lease(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);self.ops.acquire(allocation,EXPIRY)
        self.assertEqual('UNSAFE_TO_PROCEED',self.ops.inspect(CASE,allocation['transaction_id'],IDENTITY,ROLE)['determination'])

    def test_recovery_binding_and_single_use(self):
        rdet=self.bundle()[4];rauth=authorization(self.ops,rdet);context=recovery_context(self.ops,rdet,rauth)
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE,context)
        self.assertEqual(context,allocation['recovery_context'])
        self.code('RECOVERY_AUTHORIZATION_ALREADY_CONSUMED',self.ops.allocate,CASE,IDENTITY,ROLE,context)

    def test_recovery_cross_case_rejected(self):
        rdet=self.bundle()[4];rauth=authorization(self.ops,rdet)
        self.code('RECOVERY_PROVENANCE_MISMATCH',self.ops.allocate,'FILE-0002',IDENTITY,ROLE,recovery_context(self.ops,rdet,rauth))

    def test_non_safe_authorization_rejected(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE)
        rdet=self.ops.determine(CASE,allocation['transaction_id'],IDENTITY,ROLE,'Synthetic unknown')
        self.code('RECOVERY_PROVENANCE_MISMATCH',authorization,self.ops,rdet)

    def test_denied_authorization_not_allocation(self):
        rdet=self.bundle()[4];rauth=authorization(self.ops,rdet,decision='DENIED')
        self.code('RECOVERY_PROVENANCE_MISMATCH',self.ops.allocate,CASE,IDENTITY,ROLE,recovery_context(self.ops,rdet,rauth))

    def test_recovery_state_recheck(self):
        rdet=self.bundle()[4];rauth=authorization(self.ops,rdet)
        (self.root/'cases'/CASE/'item.json').write_text('changed')
        self.code('RECOVERY_STATE_CHANGED',self.ops.allocate,CASE,IDENTITY,ROLE,recovery_context(self.ops,rdet,rauth))

    def test_rdet_and_rauth_serials(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        first=self.ops.determine(CASE,allocation['transaction_id'],IDENTITY,ROLE,'one')
        second=self.ops.determine(CASE,allocation['transaction_id'],IDENTITY,ROLE,'two')
        a=authorization(self.ops,first);b=authorization(self.ops,second)
        self.assertTrue(second['recovery_determination_id'].endswith('0002'))
        self.assertTrue(b['recovery_authorization_id'].endswith('0002'))


class ReleaseTests(Base):
    def failed_release(self):
        def inject(phase):
            if phase=='before_release_unlink':raise OSError('injected release failure')
        self.ops.checkpoint=inject
        result=completed(self.ops)
        self.ops.checkpoint=lambda phase:None
        return result

    def test_release_failure_preserves_commit(self):
        allocation,lease,receipt,lrel=self.failed_release()
        self.assertEqual('COMMITTED',receipt['terminal_outcome']);self.assertEqual('FAILED',lrel['release_outcome'])
        self.assertEqual('LEASE_RELEASE_IO_FAILURE',lrel['release_evidence']['finding_code'])

    def test_release_ambiguous(self):
        def inject(phase):
            if phase=='after_release_unlink':raise OSError('injected')
        self.ops.checkpoint=inject
        allocation,lease,receipt,lrel=completed(self.ops)
        self.assertEqual('AMBIGUOUS',lrel['release_outcome'])
        self.assertEqual('COMMITTED',receipt['terminal_outcome'])

    def test_replacement_not_deleted(self):
        allocation,lease,receipt,lrel=self.failed_release()
        replacement=dict(lease,holder_actor_id='ACTOR-0002');self.corrupt(replacement)
        outcome,evidence=self.ops.safe_release(receipt)
        self.assertEqual('OWNERSHIP_MISMATCH',outcome)
        self.assertEqual(replacement,self.ops.read(record_path(lease)))

    def test_replacement_between_read_and_compare(self):
        allocation,lease,receipt,lrel=self.failed_release()
        replacement=dict(lease,holder_actor_id='ACTOR-0002')
        self.ops.checkpoint=lambda phase:self.corrupt(replacement) if phase=='before_release_compare' else None
        outcome,evidence=self.ops.safe_release(receipt)
        self.assertEqual('OWNERSHIP_MISMATCH',outcome)
        self.assertEqual(replacement,self.ops.read(record_path(lease)))

    def test_duplicate_lrel(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        self.code('ARTIFACT_FINAL_PATH_ALREADY_EXISTS',self.ops.release,receipt,IDENTITY,ROLE)

    def test_already_absent_not_release_proof(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        outcome,evidence=self.ops.safe_release(receipt)
        self.assertEqual('ALREADY_ABSENT',outcome);self.assertFalse(evidence['safe_delete_performed'])

    def test_lrres_retry_and_terminal(self):
        allocation,lease,receipt,lrel=self.failed_release()
        resolution=self.ops.resolve_release(lrel,record_path(lrel),IDENTITY,ROLE,retry=True)
        self.assertEqual('RESOLVED_RELEASED',resolution['resolution_status'])
        self.code('LEASE_RELEASE_RESOLUTION_SUCCESSOR_CONFLICT',self.ops.resolve_release,lrel,record_path(resolution),IDENTITY,ROLE)

    def test_lrres_stale_tip_rejected(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        self.ops.resolve_release(lrel,record_path(lrel),IDENTITY,ROLE)
        self.code('LEASE_RELEASE_RESOLUTION_SUCCESSOR_CONFLICT',self.ops.resolve_release,lrel,record_path(lrel),IDENTITY,ROLE)

    def test_lrres_cross_transaction_rejected(self):
        a,b,c,root1=completed(self.ops)
        a,b,c,root2=completed(self.ops,'second.json')
        resolution=self.ops.resolve_release(root1,record_path(root1),IDENTITY,ROLE)
        resolution.update(binding('predecessor',self.ops.metadata(root2)))
        self.code('LEASE_RELEASE_RESOLUTION_CHAIN_INVALID',self.ops.check_links,resolution)


class IntegrityTests(Base):
    def codes(self):return {f['code'] for f in audit(self.root,CONTRACTS)['findings']}

    def test_empty_audit_readonly(self):
        self.assertEqual('PASS',audit(self.root,CONTRACTS)['overall_status'])
        self.assertEqual([],list(self.root.iterdir()))

    def test_valid_bundle_audit(self):
        self.bundle();result=audit(self.root,CONTRACTS)
        self.assertEqual(0,result['counts']['ERROR'],result)
        self.assertEqual('PASS_WITH_WARNINGS',result['overall_status'])

    def test_audit_readonly_corrupt_evidence(self):
        value=self.ops.allocate(CASE,IDENTITY,ROLE)
        path=self.root/record_path(value);path.write_text(json.dumps(value))
        before={p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertIn('NONCANONICAL_SERIALIZATION',self.codes())
        self.assertEqual(before,{p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_missing_durable_ref(self):
        bundle=self.bundle();(self.root/record_path(bundle[0])).unlink()
        self.assertIn('REFERENCE_TARGET_MISSING',self.codes())

    def test_sha_mismatch(self):
        bundle=self.bundle();bundle[3]['lease_evidence']['allocation_record_sha256']='0'*64;self.corrupt(bundle[3])
        self.assertIn('REFERENCE_FIXITY_MISMATCH',self.codes())

    def test_duplicate_identity(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE)
        path=self.root/record_path(allocation);(path.parent/'duplicate.json').write_bytes(path.read_bytes())
        self.assertIn('IMMUTABLE_IDENTITY_COLLISION',self.codes())

    def test_stale_index_warning(self):
        path=self.root/'.projectorigin/index/semantic-events'/ (CASE+'.json');path.parent.mkdir(parents=True);path.write_text('["stale"]')
        result=audit(self.root,CONTRACTS)
        self.assertIn('DERIVED_INDEX_STALE',{f['code'] for f in result['findings']})
        self.assertEqual(0,result['counts']['ERROR'])

    def test_semantic_event_gap_warning(self):
        target={'artifact_id':'fixture','artifact_type':'FIXTURE'}
        target_ref='cases/'+CASE+'/fixture.json'
        target_raw=json.dumps(target,separators=(',',':'),sort_keys=True).encode()
        target_path=self.root/target_ref
        target_path.parent.mkdir(parents=True,exist_ok=True)
        target_path.write_bytes(target_raw)

        def write_event(serial):
            event={
                'event_id':CASE+'-EVT-'+str(serial).zfill(4),
                'occurred_at':'2026-09-18T00:00:00Z',
                'event_type':'RECORD_CREATED',
                'record_ref':{
                    'ref_id':'fixture','artifact_type':'FIXTURE','required':False,
                    'applicability':'CONDITIONAL','artifact_id':'fixture',
                    'repository_path':target_ref,'sha256':s.sha256(target_raw)
                },
                'actor_id':IDENTITY,'actor_role':ROLE,
                'authority_type':'NONE','authority_reference':None,
                'previous_state':None,'new_state':None,'evidence_references':[]
            }
            path=self.root/'cases'/CASE/'semantic-events'/(event['event_id']+'.json')
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(s.serialize(event,CONTRACTS.definition('semanticEvent'),CONTRACTS.resolve))

        write_event(1);write_event(3)
        result=audit(self.root,CONTRACTS,contextual_validator=lambda path,event:[])
        gaps=[f for f in result['findings'] if f['code']=='PERMITTED_SERIAL_GAP' and f['ref']==CASE+'/EVT']
        self.assertEqual(1,len(gaps),result)
        self.assertEqual('WARNING',gaps[0]['severity'])
        self.assertEqual(0,result['counts']['ERROR'],result)

    def test_temp_debris_warning(self):
        path=self.root/'.projectorigin/receipts'/'stale.tmp';path.parent.mkdir(parents=True);path.write_bytes(b'partial')
        self.assertIn('NONAUTHORITATIVE_TEMP_DEBRIS',self.codes())

    def test_lrres_branch_detected(self):
        bundle=self.bundle();resolution=bundle[-1]
        fork=copy.deepcopy(resolution);fork['lease_release_resolution_id']=CASE+'-LRRES-0002';self.corrupt(fork)
        self.assertIn('LEASE_RELEASE_RESOLUTION_BRANCH',self.codes())

    def test_lrres_cycle_detected(self):
        bundle=self.bundle();resolution=bundle[-1]
        resolution['predecessor_ref']=record_path(resolution);resolution['predecessor_sha256']='0'*64;self.corrupt(resolution)
        self.assertIn('LEASE_RELEASE_RESOLUTION_CYCLE',self.codes())

    def test_actor_corruption_detected(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE)
        allocation['allocated_by_actor_role']='administrator';self.corrupt(allocation)
        self.assertIn('SCHEMA_ERROR',self.codes())

    def test_duplicate_rauth_consumption(self):
        bundle=self.bundle();rdet,rauth=bundle[4:6];context=recovery_context(self.ops,rdet,rauth)
        one=self.ops.allocate(CASE,IDENTITY,ROLE,context)
        two=copy.deepcopy(one);two['transaction_id']=CASE+'-TXN-0003';self.corrupt(two)
        self.assertIn('RECOVERY_AUTHORIZATION_ALREADY_CONSUMED',self.codes())


class ConcurrencyTests(Base):
    def run_workers(self,action,arguments):
        context=multiprocessing.get_context('spawn');start=context.Event();queue=context.Queue()
        workers=[context.Process(target=concurrent_worker,args=(str(self.root),action,arg,start,queue)) for arg in arguments]
        try:
            for worker in workers:worker.start()
            start.set();results=[queue.get(timeout=40) for _ in workers]
            for worker in workers:
                worker.join(40);self.assertEqual(0,worker.exitcode)
            return results
        finally:
            for worker in workers:
                if worker.is_alive():worker.terminate();worker.join()
            queue.close()

    def test_same_case_allocations_unique(self):
        results=self.run_workers('allocate',[CASE]*4)
        self.assertEqual(4,len({r[1] for r in results}));self.assertTrue(all(r[0]=='PASS' for r in results),results)

    def test_different_case_allocations(self):
        results=self.run_workers('allocate',[CASE,'FILE-0002'])
        self.assertEqual({CASE+'-TXN-0001','FILE-0002-TXN-0001'},{r[1] for r in results})

    def test_recovery_consumed_once(self):
        bundle=self.bundle();rdet,rauth=bundle[4:6];context=recovery_context(self.ops,rdet,rauth)
        results=self.run_workers('recovery',[context]*3)
        self.assertEqual(1,sum(r[0]=='PASS' for r in results),results)
        self.assertEqual(2,sum(r[1]=='RECOVERY_AUTHORIZATION_ALREADY_CONSUMED' for r in results))

    def test_lease_slot_one_winner(self):
        allocations=[self.ops.allocate(CASE,IDENTITY,ROLE) for _ in range(3)]
        results=self.run_workers('lease',allocations)
        self.assertEqual(1,sum(r[0]=='PASS' for r in results),results)

    def test_one_resolution_successor(self):
        a,b,c,lrel=completed(self.ops)
        results=self.run_workers('resolve',[record_path(lrel)]*3)
        self.assertEqual(1,sum(r[0]=='PASS' for r in results),results)
        self.assertEqual(2,sum(r[1]=='LEASE_RELEASE_RESOLUTION_SUCCESSOR_CONFLICT' for r in results))

    def test_case_wide_lrres_ids(self):
        a,b,c,first=completed(self.ops);a,b,c,second=completed(self.ops,'second.json')
        results=self.run_workers('resolve',[record_path(first),record_path(second)])
        self.assertTrue(all(r[0]=='PASS' for r in results),results);self.assertEqual(2,len({r[1] for r in results}))

    def test_rdet_ids(self):
        allocation,lease,receipt,lrel=completed(self.ops)
        results=self.run_workers('determine',[allocation['transaction_id']]*3)
        self.assertTrue(all(r[0]=='PASS' for r in results),results);self.assertEqual(3,len({r[1] for r in results}))

    def test_rauth_ids(self):
        bundle=self.bundle();rdet=bundle[4]
        results=self.run_workers('authorize',[record_path(rdet)]*3)
        self.assertTrue(all(r[0]=='PASS' for r in results),results);self.assertEqual(3,len({r[1] for r in results}))


if __name__=='__main__':unittest.main()
