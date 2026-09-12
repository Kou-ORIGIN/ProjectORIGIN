"""Human Source Review / DR06 adversarial regressions; disposable repositories only."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest import mock

from test_operations import Base, CASE, IDENTITY, ROLE, EXPIRY, CONTRACTS, completed, writes, validation, authorization, recovery_context
from case_bootstrap import storage as s
from case_bootstrap.operations import Operations, actor, envelope, now
from case_bootstrap.contracts import record_path
from case_bootstrap.recovery import UNKNOWN, evaluate
from case_bootstrap.audit import audit
from case_bootstrap.contextual import load_validator


class DR06Tests(Base):
    def scenario(self, outcome='VALIDATING', entered=True, actual='pre', count=2):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        plan=[]
        for i in range(count):
            path='cases/'+CASE+'/item'+str(i)+'.json'
            target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'{"old":true}\n')
            plan.append({'target_path':path,'operation':'UPDATE','role':'CANONICAL_TARGET','bytes':b'{"new":true}\n'})
        result=self.ops.execute(allocation,lease,plan,[],validation)
        for value in (result['receipt'],result['lease_release_record']):
            (self.root/record_path(value)).unlink()
        ref='.projectorigin/journals/'+CASE+'/'+allocation['transaction_id']+'.json'
        journal=self.ops.read(ref);journal['state']=outcome
        journal['commit_window']={'entered':entered,'entered_at':now() if entered else None}
        self.corrupt(journal)
        for i,w in enumerate(plan):
            (self.root/w['target_path']).write_bytes(b'{"old":true}\n' if actual=='pre' or actual=='mixed' and i==0 else w['bytes'])
        return allocation,lease,journal,plan

    def inspection(self,allocation):
        return self.ops.inspect(CASE,allocation['transaction_id'],IDENTITY,ROLE)

    def assert_outcome(self,allocation,determination,consistency=None):
        result=self.inspection(allocation)
        self.assertEqual(determination,result['determination'],result)
        if consistency:self.assertEqual(consistency,result['evidence']['consistency'])
        return result

    def test_01_prepared_before_precondition_verification(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        path=self.root/'cases'/CASE/'item.json';path.parent.mkdir(parents=True);path.write_text('existing')
        seen=[]
        def checkpoint(phase):
            if phase=='prepared_before_preconditions':
                journal=self.ops.read('.projectorigin/journals/'+CASE+'/'+allocation['transaction_id']+'.json')
                self.assertEqual('PREPARED',journal['state']);seen.append(phase)
        self.ops.checkpoint=checkpoint
        result=self.ops.execute(allocation,lease,writes(),[],validation)
        self.assertEqual(['prepared_before_preconditions'],seen)
        self.assertEqual('STALE_WRITE_CONFLICT',result['failure_code'])
        self.assertEqual('ABORTED',result['receipt']['terminal_outcome'])
        self.assertEqual('existing',path.read_text())

    def test_02_create_conflict_has_journal_receipt_and_release(self):
        allocation=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(allocation,EXPIRY)
        path=self.root/'cases'/CASE/'item.json';path.parent.mkdir(parents=True);path.write_text('existing')
        result=self.ops.execute(allocation,lease,writes(),[],validation)
        self.assertEqual('ABORTED',self.ops.read('.projectorigin/journals/'+CASE+'/'+allocation['transaction_id']+'.json')['state'])
        self.assertEqual('ABORTED',self.ops.read(record_path(result['receipt']))['terminal_outcome'])
        self.assertFalse((self.root/record_path(lease)).exists())

    def test_03_exact_pre_safe(self):
        a,*_=self.scenario();self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','MATCHES_PRE_TRANSACTION_STATE')

    def test_04_exact_committed_safe(self):
        a,*_=self.scenario(actual='committed');self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','MATCHES_COMMITTED_STATE')

    def test_05_recovery_required_pre_safe(self):
        a,*_=self.scenario(outcome='RECOVERY_REQUIRED');self.assert_outcome(a,'SAFE_TO_START_NEW_TXN')

    def test_06_recovery_required_committed_safe(self):
        a,*_=self.scenario(outcome='RECOVERY_REQUIRED',actual='committed');self.assert_outcome(a,'SAFE_TO_START_NEW_TXN')

    def test_07_partial_state_unsafe(self):
        a,*_=self.scenario(actual='mixed');self.assert_outcome(a,'UNSAFE_TO_PROCEED','CONFLICTING_STATE')

    def test_08_valid_lease_exists_unsafe(self):
        a,lease,*_=self.scenario();self.ops.acquire(a,EXPIRY);self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_09_expired_lease_exists_unsafe(self):
        a,lease,*_=self.scenario();lease.update(acquired_at='2020-01-01T00:00:00Z',expires_at='2020-01-02T00:00:00Z')
        self.corrupt(lease);self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_10_foreign_lease_exists_unsafe(self):
        a,*_=self.scenario();other=self.ops.allocate(CASE,IDENTITY,ROLE);self.ops.acquire(other,EXPIRY)
        self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_11_lease_unobservable_undetermined(self):
        a,*_=self.scenario();original=s.read_bytes
        def read(root,path):
            if path=='.projectorigin/leases/'+CASE+'.json':raise PermissionError('injected')
            return original(root,path)
        with mock.patch.object(s,'read_bytes',side_effect=read):self.assert_outcome(a,'UNDETERMINED')

    def test_12_no_scope_basis_undetermined(self):
        a=self.ops.allocate(CASE,IDENTITY,ROLE);self.assert_outcome(a,'UNDETERMINED')

    def test_13_dangling_journal_allocation_unsafe(self):
        a,l,j,p=self.scenario();j['lease_binding']['allocation_record_ref']='missing.json';self.corrupt(j)
        self.assert_outcome(a,'UNSAFE_TO_PROCEED','CONFLICTING_STATE')

    def test_14_journal_receipt_outcome_mismatch_unsafe(self):
        a,l,r,release=completed(self.ops)
        j=self.ops.read('.projectorigin/journals/'+CASE+'/'+a['transaction_id']+'.json');j['state']='ABORTED';self.corrupt(j)
        self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def add_required_event(self,journal):
        event={'event_id':CASE+'-EVT-0001','event_type':'RECORD_CREATED','record_ref':{'ref_id':'fixture','artifact_type':'FIXTURE','required':True,'applicability':'REQUIRED'}}
        journal['semantic_event_requirement']='REQUIRED';journal['required_semantic_events']=[event];self.corrupt(journal)
        return 'cases/'+CASE+'/semantic-events/'+event['event_id']+'.json'

    def test_15_required_event_missing_unsafe(self):
        a,l,j,p=self.scenario();self.add_required_event(j);self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_16_required_event_invalid_unsafe(self):
        a,l,j,p=self.scenario();path=self.root/self.add_required_event(j);path.parent.mkdir(parents=True);path.write_text('{}')
        self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_17_manifest_mismatch_unsafe(self):
        a,l,j,p=self.scenario(actual='committed');j['write_intent'][0]['role']='MANIFEST';j['write_progress'][0]['role']='MANIFEST';self.corrupt(j)
        self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def proposed_rdet(self):
        a,*_=self.scenario()
        return {**envelope('RECOVERY_DETERMINATION',CASE),'recovery_determination_id':CASE+'-RDET-0001','prior_transaction_id':a['transaction_id'],**self.inspection(a),**actor('determined_by',IDENTITY,ROLE),'determined_at':now(),'rationale':'Synthetic snapshot'}

    def test_18_safe_conflicting_rejected(self):
        r=self.proposed_rdet();r['evidence']['consistency']='CONFLICTING_STATE'
        self.code('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',self.ops.publish,r)

    def test_19_safe_lease_exists_rejected(self):
        a,*_=self.scenario();self.ops.acquire(a,EXPIRY)
        r={**envelope('RECOVERY_DETERMINATION',CASE),'recovery_determination_id':CASE+'-RDET-0001','prior_transaction_id':a['transaction_id'],**self.inspection(a),**actor('determined_by',IDENTITY,ROLE),'determined_at':now(),'rationale':'Synthetic'}
        r['determination']='SAFE_TO_START_NEW_TXN'
        self.code('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',self.ops.publish,r)

    def test_20_safe_unobservable_rejected(self):
        r=self.proposed_rdet();r['evidence']['lease_observation'].update(state=dict(UNKNOWN),validation='UNAVAILABLE')
        self.code('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',self.ops.publish,r)

    def test_21_audit_detects_stored_mismatch(self):
        r=self.proposed_rdet();self.ops.publish(r);r['determination']='UNSAFE_TO_PROCEED';self.corrupt(r)
        result=audit(self.root);self.assertEqual('FAIL',result['overall_status'])
        self.assertIn('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',[f['code'] for f in result['findings']])

    def test_22_state_changed_after_rauth_no_allocation(self):
        a,l,j,p=self.scenario();r=self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Synthetic');auth=authorization(self.ops,r)
        before=list((self.root/'.projectorigin/transaction-allocations'/CASE).iterdir());(self.root/p[0]['target_path']).write_text('third state')
        self.code('RECOVERY_STATE_CHANGED',self.ops.allocate,CASE,IDENTITY,ROLE,recovery_context(self.ops,r,auth))
        self.assertEqual(before,list((self.root/'.projectorigin/transaction-allocations'/CASE).iterdir()))

    def test_23_superseded_rdet_blocks_continuation(self):
        a,*_=self.scenario();r=self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Synthetic');auth=authorization(self.ops,r)
        meta=self.ops.metadata(r);ref={'ref_id':'prior','artifact_type':'RECOVERY_DETERMINATION','artifact_id':r['recovery_determination_id'],'required':True,'applicability':'REQUIRED','repository_path':meta['ref'],'sha256':meta['sha256']}
        self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Successor',supersedes=ref)
        self.code('RECOVERY_DETERMINATION_SUPERSEDED',self.ops.allocate,CASE,IDENTITY,ROLE,recovery_context(self.ops,r,auth))

    def test_24_journal_wrong_sha_unsafe(self):
        a,l,j,p=self.scenario();j['lease_binding']['allocation_record_sha256']='0'*64;self.corrupt(j)
        self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_25_lease_snapshot_full_identity(self):
        a=self.ops.allocate(CASE,IDENTITY,ROLE);lease=self.ops.acquire(a,EXPIRY)
        o=self.inspection(a)['evidence']['lease_observation']
        self.assertEqual('VALID',o['validation']);self.assertEqual(lease,o['data'])
        self.assertEqual(s.sha256(CONTRACTS.encode(lease)),o['state']['sha256'])
        for k in ('case_id','transaction_id','holder_actor_id','holder_actor_role','allocation_record_ref','allocation_record_sha256','acquired_at','expires_at'):self.assertIn(k,o['data'])

    def test_26_deterministic_audit_order(self):
        for case in ['FILE-0002','FILE-0001']:
            p=self.root/'.projectorigin/index/semantic-events'/str(case+'.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('[]')
        results=[json.dumps(audit(self.root),sort_keys=True) for _ in range(4)]
        self.assertEqual(1,len(set(results)))

    def canonical_fixture(self):
        path='cases/'+CASE+'/record.json';target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True)
        value={'artifact_id':'REC-0001','artifact_type':'FIXTURE'};target.write_text(json.dumps(value))
        reference={'ref_id':'fixture','artifact_type':'FIXTURE','artifact_id':'REC-0001','required':True,'applicability':'REQUIRED','repository_path':path,'sha256':s.sha256(target.read_bytes())}
        return reference

    def test_27_manifest_reference_fixity_identity(self):
        ref=self.canonical_fixture();path=self.root/'cases'/CASE/'orchestration-manifest.json'
        for field,bad,code in [('repository_path','missing.json','REFERENCE_TARGET_MISSING'),('sha256','0'*64,'REFERENCE_FIXITY_MISMATCH'),('artifact_id','wrong','REFERENCE_IDENTITY_MISMATCH')]:
            with self.subTest(field=field):
                value=copy.deepcopy(ref);value[field]=bad
                path.write_text(json.dumps({'case_id':CASE,'artifact_references':[value]}))
                result=audit(self.root);self.assertIn(code,[f['code'] for f in result['findings']])

    def event_fixture(self):
        ref=self.canonical_fixture();event={'event_id':CASE+'-EVT-0001','occurred_at':now(),'event_type':'RECORD_CREATED','record_ref':ref,'actor_id':IDENTITY,'actor_role':ROLE,'authority_type':'NONE','authority_reference':None,'previous_state':None,'new_state':None,'evidence_references':[]}
        path=self.root/'cases'/CASE/'semantic-events'/str(event['event_id']+'.json');path.parent.mkdir(parents=True)
        path.write_bytes(s.serialize(event,CONTRACTS.definition('semanticEvent'),CONTRACTS.resolve))
        return path,event

    def test_28_contextual_validator_unavailable_fails_closed(self):
        self.event_fixture();result=audit(self.root)
        self.assertIn('CONTEXTUAL_EVENT_VALIDATION_UNAVAILABLE',[f['code'] for f in result['findings']]);self.assertEqual('FAIL',result['overall_status'])

    def test_29_contextual_validator_invalid_fails(self):
        self.event_fixture();result=audit(self.root,contextual_validator=lambda p,e:[{'code':'SYNTHETIC_CONTEXT_INVALID','severity':'ERROR'}])
        self.assertIn('SYNTHETIC_CONTEXT_INVALID',[f['code'] for f in result['findings']])

    def test_30_contextual_validator_valid_passes(self):
        self.event_fixture();result=audit(self.root,contextual_validator=lambda p,e:[])
        self.assertEqual(0,result['counts']['ERROR'])

    def test_cli_contextual_capability_wiring(self):
        self.event_fixture();module=self.root/'validator.py';module.write_text('def validate(root,path,event):\n    return []\n')
        script=Path(__file__).resolve().parents[2]/'scripts/audit-operations.py'
        result=subprocess.run([sys.executable,'-B',str(script),'--repository-root',str(self.root),'--contextual-validator',str(module)+':validate'],capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr);self.assertEqual(0,json.loads(result.stdout)['counts']['ERROR'])

    def test_committed_before_commit_window_unsafe(self):
        a,*_=self.scenario(entered=False,actual='committed');self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_prepared_without_receipt_pre_safe(self):
        a,*_=self.scenario(outcome='PREPARED',entered=False);self.assert_outcome(a,'SAFE_TO_START_NEW_TXN')

    def test_receipt_without_ephemeral_journal_safe(self):
        a,l,r,release=completed(self.ops);(self.root/'.projectorigin/journals'/CASE/str(a['transaction_id']+'.json')).unlink()
        self.assert_outcome(a,'SAFE_TO_START_NEW_TXN')

    def test_third_state_unsafe(self):
        a,l,j,p=self.scenario();(self.root/p[0]['target_path']).write_text('third');self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_missing_exact_pre_sha_insufficient(self):
        a,l,j,p=self.scenario();j['preconditions'][0]['sha256']=None;self.corrupt(j);self.assert_outcome(a,'UNDETERMINED')

    def test_noop_tie_pre_without_terminal_commit(self):
        a,l,j,p=self.scenario()
        for item in j['write_intent']:item['prospective_sha256']=s.sha256(b'{"old":true}\n')
        self.corrupt(j);result=self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','MATCHES_PRE_TRANSACTION_STATE')
        self.assertTrue(all(o['comparison']=='MATCHES_BOTH' for o in result['evidence']['canonical_observations']))

    def test_rdet_snapshot_survives_later_journal_change(self):
        a,l,j,p=self.scenario();r=self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Synthetic');raw=(self.root/record_path(r)).read_bytes()
        j['state']='RECOVERY_REQUIRED';self.corrupt(j)
        self.assertEqual(r,self.ops.read(record_path(r)));self.assertEqual(raw,(self.root/record_path(r)).read_bytes())

    def test_invalid_lease_does_not_fabricate_identity(self):
        a,*_=self.scenario();path=self.root/'.projectorigin/leases'/str(CASE+'.json');path.write_text('{}')
        result=self.assert_outcome(a,'UNSAFE_TO_PROCEED');self.assertIsNone(result['evidence']['lease_observation']['data'])

    def test_recovery_inspection_readonly(self):
        a,*_=self.scenario();before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.inspection(a);self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_noop_terminal_committed_tie(self):
        a,l,j,p=self.scenario(outcome='COMMITTED')
        for item in j['write_intent']:item['prospective_sha256']=s.sha256(b'{"old":true}\n')
        self.corrupt(j);self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','MATCHES_COMMITTED_STATE')

    def test_noop_terminal_aborted_tie(self):
        a,l,j,p=self.scenario(outcome='ABORTED')
        for item in j['write_intent']:item['prospective_sha256']=s.sha256(b'{"old":true}\n')
        self.corrupt(j);self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','MATCHES_PRE_TRANSACTION_STATE')

    def test_valid_empty_scope_not_applicable(self):
        a,l,j,p=self.scenario();j.update(write_intent=[],preconditions=[],write_progress=[]);self.corrupt(j)
        self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','NOT_APPLICABLE')

    def test_unsafe_precedes_unobservable(self):
        a,l,j,p=self.scenario();j['lease_binding']['allocation_record_ref']='missing.json';self.corrupt(j)
        original=s.read_bytes
        def read(root,path):
            if path=='.projectorigin/leases/'+CASE+'.json':raise PermissionError('injected')
            return original(root,path)
        with mock.patch.object(s,'read_bytes',side_effect=read):self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_existing_unreadable_lease_still_unsafe(self):
        a,*_=self.scenario();self.ops.acquire(a,EXPIRY);original=s.read_bytes
        def read(root,path):
            if path=='.projectorigin/leases/'+CASE+'.json':raise PermissionError('injected')
            return original(root,path)
        with mock.patch.object(s,'read_bytes',side_effect=read):
            result=self.assert_outcome(a,'UNSAFE_TO_PROCEED');o=result['evidence']['lease_observation']
            self.assertEqual('EXISTS',o['state']['existence']);self.assertEqual('UNAVAILABLE',o['validation']);self.assertIsNone(o['data'])

    def test_missing_update_target_terminalizes(self):
        a=self.ops.allocate(CASE,IDENTITY,ROLE);l=self.ops.acquire(a,EXPIRY);plan=writes();plan[0]['operation']='UPDATE'
        result=self.ops.execute(a,l,plan,[],validation)
        self.assertEqual('ABORTED',result['receipt']['terminal_outcome']);self.assertEqual('STALE_WRITE_CONFLICT',result['failure_code'])
        self.assertTrue((self.root/'.projectorigin/journals'/CASE/str(a['transaction_id']+'.json')).exists())

    def test_snapshot_scope_cannot_be_omitted(self):
        r=self.proposed_rdet();r['evidence']['canonical_observations']=[]
        self.code('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',self.ops.publish,r)

    def test_snapshot_expected_state_cannot_be_forged(self):
        r=self.proposed_rdet();r['evidence']['canonical_observations'][0]['expected_committed_state']['sha256']='0'*64
        self.code('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',self.ops.publish,r)

    def test_snapshot_journal_bytes_fixity(self):
        r=self.proposed_rdet();r['evidence']['journal_observation']['data']['updated_at']=now()
        self.code('RECOVERY_SNAPSHOT_FIXITY_MISMATCH',self.ops.publish,r)

    def test_changed_journal_after_rauth_blocks_allocation(self):
        a,l,j,p=self.scenario();r=self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Synthetic');auth=authorization(self.ops,r)
        j['state']='RECOVERY_REQUIRED';self.corrupt(j)
        self.code('RECOVERY_STATE_CHANGED',self.ops.allocate,CASE,IDENTITY,ROLE,recovery_context(self.ops,r,auth))

    def test_supersession_does_not_retroactively_invalidate_allocation(self):
        a,*_=self.scenario();r=self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Synthetic');auth=authorization(self.ops,r)
        allocated=self.ops.allocate(CASE,IDENTITY,ROLE,recovery_context(self.ops,r,auth));meta=self.ops.metadata(r)
        self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Successor',supersedes={'ref_id':'prior','artifact_type':'RECOVERY_DETERMINATION','artifact_id':r['recovery_determination_id'],'required':True,'applicability':'REQUIRED','repository_path':meta['ref'],'sha256':meta['sha256']})
        self.ops.check_links(allocated)

    def test_manifest_valid_references_pass(self):
        ref=self.canonical_fixture();path=self.root/'cases'/CASE/'orchestration-manifest.json'
        path.write_text(json.dumps({'case_id':CASE,'artifact_references':[ref]}))
        self.assertEqual(0,audit(self.root)['counts']['ERROR'])

    def test_manifest_untyped_reference_fails_closed(self):
        ref=self.canonical_fixture();path=self.root/'cases'/CASE/'orchestration-manifest.json'
        path.write_text(json.dumps({'case_id':CASE,'artifact_references':[{'repository_path':'missing.json'}]}))
        self.assertEqual('FAIL',audit(self.root)['overall_status'])

    def test_manifest_required_event_relationship(self):
        from case_bootstrap.contextual import check_manifest
        path,event=self.event_fixture();ref=self.canonical_fixture()
        manifest={'case_id':CASE,'artifact_references':[ref]}
        self.code('MANIFEST_REQUIRED_EVENT_MISSING',check_manifest,self.ops,'cases/'+CASE+'/orchestration-manifest.json',manifest,[{k:event[k] for k in ('event_id','event_type','record_ref')}])

    def test_contextual_validator_exception_fails_closed(self):
        self.event_fixture()
        def broken(path,event):raise RuntimeError('injected')
        self.assertIn('CONTEXTUAL_EVENT_VALIDATOR_FAILURE',[f['code'] for f in audit(self.root,contextual_validator=broken)['findings']])

    def test_deterministic_audit_across_hash_seeds(self):
        for case in ['FILE-0002','FILE-0001']:
            p=self.root/'.projectorigin/index/semantic-events'/str(case+'.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('[]')
        script=Path(__file__).resolve().parents[2]/'scripts/audit-operations.py'
        outputs=[]
        for seed in ('1','31','87'):
            env=dict(os.environ,PYTHONHASHSEED=seed)
            result=subprocess.run([sys.executable,'-B',str(script),'--repository-root',str(self.root)],env=env,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stderr);outputs.append(result.stdout)
        self.assertEqual(1,len(set(outputs)))

    def test_missing_exact_committed_sha_insufficient(self):
        a,l,j,p=self.scenario();j['write_intent'][0]['prospective_sha256']=None;self.corrupt(j)
        self.assert_outcome(a,'UNDETERMINED')

    def event_scenario(self,manifest=False):
        a,l,j,p=self.scenario(actual='committed');path,event=self.event_fixture()
        self.ops.contextual_validator=lambda path,event:[]
        required={k:event[k] for k in ('event_id','event_type','record_ref')}
        j['semantic_event_requirement']='REQUIRED';j['required_semantic_events']=[required]
        targets=[(path,'SEMANTIC_EVENT')]
        if manifest:
            event_ref={'ref_id':'event','artifact_type':'SEMANTIC_EVENT','artifact_id':event['event_id'],'required':True,'applicability':'REQUIRED','repository_path':path.relative_to(self.root).as_posix(),'sha256':s.sha256(path.read_bytes())}
            m=self.root/'cases'/CASE/'orchestration-manifest.json'
            m.write_text(json.dumps({'case_id':CASE,'artifact_references':[event['record_ref'],event_ref]}))
            targets.append((m,'MANIFEST'))
        for target,role in targets:
            relative=target.relative_to(self.root).as_posix()
            j['write_intent'].append({'target_path':relative,'operation':'CREATE','role':role,'prospective_sha256':s.sha256(target.read_bytes())})
            j['preconditions'].append({'target_path':relative,'existence':'MUST_NOT_EXIST','sha256':None})
            j['write_progress'].append({'target_path':relative,'operation':'CREATE','role':role,'progress_state':'VERIFIED','last_observed_at':now()})
        self.corrupt(j)
        return a,j,targets

    def test_recovery_valid_required_event_safe(self):
        a,j,targets=self.event_scenario();self.assert_outcome(a,'SAFE_TO_START_NEW_TXN','MATCHES_COMMITTED_STATE')

    def test_recovery_event_capability_unavailable_undetermined(self):
        a,j,targets=self.event_scenario();self.ops.contextual_validator=None
        self.assert_outcome(a,'UNDETERMINED')

    def test_recovery_manifest_and_events_valid_safe(self):
        a,j,targets=self.event_scenario(manifest=True);self.assert_outcome(a,'SAFE_TO_START_NEW_TXN')

    def test_rdet_missing_integrity_check_rejected(self):
        a,j,targets=self.event_scenario(manifest=True)
        r={**envelope('RECOVERY_DETERMINATION',CASE),'recovery_determination_id':CASE+'-RDET-0001','prior_transaction_id':a['transaction_id'],**self.inspection(a),**actor('determined_by',IDENTITY,ROLE),'determined_at':now(),'rationale':'Synthetic'}
        r['evidence']['integrity_results']=[]
        self.code('RECOVERY_DETERMINATION_EVIDENCE_MISMATCH',self.ops.publish,r)

    def test_manifest_change_after_rauth_blocked(self):
        a,j,targets=self.event_scenario(manifest=True);r=self.ops.determine(CASE,a['transaction_id'],IDENTITY,ROLE,'Synthetic');auth=authorization(self.ops,r)
        targets[-1][0].write_text('{}')
        self.code('RECOVERY_STATE_CHANGED',self.ops.allocate,CASE,IDENTITY,ROLE,recovery_context(self.ops,r,auth))

    def test_journal_receipt_lease_binding_mismatch_unsafe(self):
        a,l,r,release=completed(self.ops)
        j=self.ops.read('.projectorigin/journals/'+CASE+'/'+a['transaction_id']+'.json')
        j['lease_binding']['lease_sha256']='0'*64;self.corrupt(j)
        self.assert_outcome(a,'UNSAFE_TO_PROCEED')

    def test_journal_manifest_role_cannot_hide_manifest(self):
        a,l,j,p=self.scenario()
        for collection in ('write_intent','preconditions','write_progress'):
            j[collection][0]['target_path']='cases/'+CASE+'/orchestration-manifest.json'
        self.corrupt(j);self.assert_outcome(a,'UNSAFE_TO_PROCEED')
