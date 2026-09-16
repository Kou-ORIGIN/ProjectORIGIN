#!/usr/bin/env python3
from pathlib import Path
import hashlib, importlib.util, json, shutil, sys, tempfile, unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/validate-image-registration.py'
SCHEMA = ROOT / 'schemas/cases/mechanical-validation-record.schema.json'
spec = importlib.util.spec_from_file_location('mvr', SCRIPT)
mvr = importlib.util.module_from_spec(spec); spec.loader.exec_module(mvr)

def sha(raw): return hashlib.sha256(raw).hexdigest()
def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(mvr.canonical_bytes(value))

def evidence(root, rel, expected=True):
    p = root / rel
    if p.exists():
        digest = sha(p.read_bytes())
        return {'path':rel,'expected_sha256':digest if expected else None,'observed_sha256':digest,'existence':'EXISTS'}
    return {'path':rel,'expected_sha256':None,'observed_sha256':None,'existence':'ABSENT'}

class Fixture:
    def __init__(self, root):
        self.root = root; self.case='FILE-9999'; self.req='IMGREQ-001'; self.asset='FILE-9999-IMG-0001'; self.version='v1.0'; self.txn='FILE-9999-TXN-0001'
        (root/'docs').mkdir(parents=True)
        (root/'docs/Image Rule.md').write_text('Image Rule candidate fixture\n', encoding='utf-8')
        (root/'docs/ProjectORIGIN Repository Rule.md').write_text('Repository Rule candidate fixture\n', encoding='utf-8')
        self.base_rel=f'cases/{self.case}/images/{self.asset}_{self.version}.png'
        self.side_rel=f'cases/{self.case}/images/{self.asset}_{self.version}.json'
        self.audit_rel=f'cases/{self.case}/image-audits/{self.asset}_{self.version}.json'
        self.reg_rel=f'cases/{self.case}/image-requirements.json'
        self.mgmt_rel=self.reg_rel
        base=root/self.base_rel; base.parent.mkdir(parents=True, exist_ok=True); base.write_bytes(b'PNG-FIXTURE\n')
        base_sha=sha(base.read_bytes())
        side={'case_id':self.case,'requirement_id':self.req,'asset_id':self.asset,'asset_version':self.version,'sha256':base_sha,'management_status':'APPROVED'}
        write_json(root/self.side_rel,side)
        audit={'artifact_type':'IMAGE_AUDIT','case_id':self.case,'asset_id':self.asset,'asset_version':self.version,'candidate_sha256':base_sha,'result':'PASS'}
        write_json(root/self.audit_rel,audit)
        reg={'case_id':self.case,'requirements':[{'requirement_id':self.req,'resulting_asset_reference':{'asset_id':self.asset,'asset_version':self.version,'sha256':base_sha},'management_status':'APPROVED'}]}
        write_json(root/self.reg_rel,reg)
    def record(self):
        script_sha=sha(SCRIPT.read_bytes())
        gov=[]
        for rel,ver in [('docs/Image Rule.md','v1.4'),('docs/ProjectORIGIN Repository Rule.md','current')]:
            gov.append({'document_path':rel,'applicable_version':ver,'sha256':sha((self.root/rel).read_bytes())})
        reg=evidence(self.root,self.reg_rel); base=evidence(self.root,self.base_rel); side=evidence(self.root,self.side_rel); audit=evidence(self.root,self.audit_rel)
        audit['observed_result']='PASS'
        mg={'source_path':self.mgmt_rel,'source_sha256':sha((self.root/self.mgmt_rel).read_bytes()),'observed_status':'APPROVED'}
        libs=[]
        try:
            import importlib.metadata
            libs=[{'name':'jsonschema','version':importlib.metadata.version('jsonschema')}]
        except Exception: pass
        r={
            'record_format_version':'v1.0','artifact_type':'MECHANICAL_VALIDATION_RECORD','case_id':self.case,'source_step':'CPW-025','transaction_id':self.txn,
            'requirement_id':self.req,'asset_id':self.asset,'asset_version':self.version,
            'register_evidence':reg,'base_asset_evidence':base,'sidecar_evidence':side,'image_audit_evidence':audit,
            'management_status_observation':mg,'governing_references':gov,
            'validator_identity':{'implementation_path':'scripts/validate-image-registration.py','sha256':script_sha},
            'runtime_identity':{'python_version':sys.version.split()[0],'libraries':libs},
            'validated_at':'2026-09-16T12:00:00Z','actor_id':'ACTOR-0001','actor_role':'Image Agent',
            'checks':[{'check_id':x,'result':'PASS','evidence_references':[]} for x in mvr.CHECK_IDS],
            'result':'PASS','findings':[],'prior_record_reference':None,
        }
        expected=mvr.evaluate_checks(r,self.root)
        r['checks']=[{'check_id':x,'result':expected[x],'evidence_references':[]} for x in mvr.CHECK_IDS]
        r['result']=mvr.aggregate(expected,r['findings'])
        return r
    def record_path(self, r):
        return self.root/mvr.canonical_record_path(r)

class MechanicalRecordTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.root=Path(self.t.name)
        # Candidate implementation itself is part of the fixture identity.
        (self.root/'scripts').mkdir(parents=True); shutil.copy2(SCRIPT,self.root/'scripts/validate-image-registration.py')
        (self.root/'schemas/cases').mkdir(parents=True); shutil.copy2(SCHEMA,self.root/'schemas/cases/mechanical-validation-record.schema.json')
        self.fx=Fixture(self.root)
    def tearDown(self): self.t.cleanup()
    def save(self,r): p=self.fx.record_path(r); write_json(p,r); return p
    def test_pass_record(self):
        r=self.fx.record(); p=self.save(r); out=mvr.validate_record(p,self.root); self.assertEqual('PASS',out['result']); self.assertTrue(mvr.transaction_eligible(out))
    def test_closed_world_schema(self):
        r=self.fx.record(); r['extra']=1; p=self.save(r)
        with self.assertRaises(Exception): mvr.validate_record(p,self.root)
    def test_duplicate_json_rejected(self):
        with self.assertRaises(Exception): mvr.load_json_strict_bytes(b'{"a":1,"a":2}\n')
    def test_bom_rejected(self):
        with self.assertRaises(Exception): mvr.load_json_strict_bytes(b'\xef\xbb\xbf{}\n')
    def test_noncanonical_rejected(self):
        r=self.fx.record(); p=self.fx.record_path(r); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(r)+'\n',encoding='utf-8')
        with self.assertRaises(Exception): mvr.validate_record(p,self.root)
    def test_base_sha_mismatch_yields_false_record_rejection(self):
        r=self.fx.record(); r['base_asset_evidence']['observed_sha256']='0'*64; p=self.save(r)
        with self.assertRaises(Exception): mvr.validate_record(p,self.root)
    def test_missing_base_truthfully_fails(self):
        (self.root/self.fx.base_rel).unlink(); r=self.fx.record(); expected=mvr.evaluate_checks(r,self.root); r['checks']=[{'check_id':x,'result':expected[x],'evidence_references':[]} for x in mvr.CHECK_IDS]; r['result']=mvr.aggregate(expected,[]); p=self.save(r); out=mvr.validate_record(p,self.root); self.assertEqual('FAIL',out['result'])
    def test_limited_expected_sha(self):
        r=self.fx.record(); r['base_asset_evidence']['expected_sha256']=None; expected=mvr.evaluate_checks(r,self.root); r['checks']=[{'check_id':x,'result':expected[x],'evidence_references':[]} for x in mvr.CHECK_IDS]; r['result']=mvr.aggregate(expected,[]); p=self.save(r); out=mvr.validate_record(p,self.root); self.assertEqual('VALIDATION_LIMITED',out['result'])
    def test_warning_aggregate(self):
        r=self.fx.record(); r['findings']=[{'code':'NONBLOCKING_NOTE','severity':'WARNING','blocking':False,'message':'fixture warning'}]; expected=mvr.evaluate_checks(r,self.root); r['checks']=[{'check_id':x,'result':expected[x],'evidence_references':[]} for x in mvr.CHECK_IDS]; r['result']=mvr.aggregate(expected,r['findings']); p=self.save(r); out=mvr.validate_record(p,self.root); self.assertEqual('PASS_WITH_WARNINGS',out['result'])
    def test_prior_record_same_asset_and_preservation(self):
        r1=self.fx.record(); p1=self.save(r1); d=sha(p1.read_bytes())
        self.fx.txn='FILE-9999-TXN-0002'; r2=self.fx.record(); r2['prior_record_reference']={'artifact_type':'MECHANICAL_VALIDATION_RECORD','case_id':self.fx.case,'asset_id':self.fx.asset,'transaction_id':'FILE-9999-TXN-0001','repository_path':str(p1.relative_to(self.root)),'sha256':d}; expected=mvr.evaluate_checks(r2,self.root); r2['checks']=[{'check_id':x,'result':expected[x],'evidence_references':[]} for x in mvr.CHECK_IDS]; r2['result']=mvr.aggregate(expected,[]); p2=self.save(r2); self.assertEqual('PASS',mvr.validate_record(p2,self.root)['result']); self.assertEqual(p2,mvr.select_current_record(self.root,self.fx.case,self.fx.asset)[0])

class TransactionAdapterTests(unittest.TestCase):
    def test_stateful_exact_two_create_writes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); adapter=mvr.MechanicalTransactionValidator(root,SCHEMA)
            writes=[{'target_path':'cases/FILE-9999/registration-validations/FILE-9999-IMG-0001/FILE-9999-TXN-0001.json','operation':'CREATE','role':'CANONICAL_TARGET','prospective_sha256':'1'*64},{'target_path':'cases/FILE-9999/semantic-events/FILE-9999-EVT-0001.json','operation':'CREATE','role':'SEMANTIC_EVENT','prospective_sha256':'2'*64}]
            self.assertEqual('PASS',adapter('PROSPECTIVE',writes)['status']); self.assertEqual('PASS',adapter('POST_WRITE',writes)['status'])
    def test_post_before_prospective_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); adapter=mvr.MechanicalTransactionValidator(root,SCHEMA); writes=[{'target_path':'cases/FILE-9999/registration-validations/a/b.json','operation':'CREATE','role':'CANONICAL_TARGET'},{'target_path':'cases/FILE-9999/semantic-events/e.json','operation':'CREATE','role':'SEMANTIC_EVENT'}]
            with self.assertRaises(Exception): adapter('POST_WRITE',writes)
    def test_third_write_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); adapter=mvr.MechanicalTransactionValidator(root,SCHEMA); writes=[{'target_path':'cases/FILE-9999/registration-validations/a/b.json','operation':'CREATE','role':'CANONICAL_TARGET'},{'target_path':'cases/FILE-9999/semantic-events/e.json','operation':'CREATE','role':'SEMANTIC_EVENT'},{'target_path':'cases/FILE-9999/images/x.png','operation':'UPDATE','role':'CANONICAL_TARGET'}]
            with self.assertRaises(Exception): adapter('PROSPECTIVE',writes)
    def test_update_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); adapter=mvr.MechanicalTransactionValidator(root,SCHEMA); writes=[{'target_path':'cases/FILE-9999/registration-validations/a/b.json','operation':'UPDATE','role':'CANONICAL_TARGET'},{'target_path':'cases/FILE-9999/semantic-events/e.json','operation':'CREATE','role':'SEMANTIC_EVENT'}]
            with self.assertRaises(Exception): adapter('PROSPECTIVE',writes)
    def test_post_descriptor_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); adapter=mvr.MechanicalTransactionValidator(root,SCHEMA); a=[{'target_path':'cases/FILE-9999/registration-validations/a/b.json','operation':'CREATE','role':'CANONICAL_TARGET','prospective_sha256':'1'*64},{'target_path':'cases/FILE-9999/semantic-events/e.json','operation':'CREATE','role':'SEMANTIC_EVENT','prospective_sha256':'2'*64}]; b=[dict(x) for x in a]; b[0]['prospective_sha256']='3'*64; adapter('PROSPECTIVE',a)
            with self.assertRaises(Exception): adapter('POST_WRITE',b)

if __name__ == '__main__': unittest.main()
