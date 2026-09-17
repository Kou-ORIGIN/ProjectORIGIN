from pathlib import Path
import importlib.util, sys, tempfile, unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mvr_remediation", ROOT/"scripts/validate-image-registration.py")
mvr = importlib.util.module_from_spec(spec); spec.loader.exec_module(mvr)
sys.path.insert(0, str(ROOT/"scripts"))
from case_bootstrap.contracts import Contracts

class RemediationTests(unittest.TestCase):
    def fixture(self, result="PASS", audit_asset="FILE-9999-IMG-0001"):
        td = tempfile.TemporaryDirectory(); root = Path(td.name)
        rel = "cases/FILE-9999/audit/FILE-9999-IMG-0001_IMAGE-AUDIT_v1.0.md"
        p = root/rel; p.parent.mkdir(parents=True)
        base_sha = "1"*64
        p.write_text(
            "# FILE-9999-IMG-0001 Formal Image Audit\n"
            "**Case ID:** FILE-9999\n"
            "**Requirement ID:** IMGREQ-003\n"
            f"**Asset ID:** {audit_asset}\n"
            "**Asset Version:** v1.0\n"
            "**Base Asset Filename:** FILE-9999-IMG-0001_v1.0.png\n"
            f"**SHA-256:** {base_sha}\n"
            f"**Audit Result:** {result}\n"
            "**Approved Image Asset Eligibility:** ELIGIBLE\n",
            encoding="utf-8")
        rec = {
            "case_id":"FILE-9999","requirement_id":"IMGREQ-003",
            "asset_id":"FILE-9999-IMG-0001","asset_version":"v1.0",
            "base_asset_evidence":{"path":"cases/FILE-9999/assets/FILE-9999-IMG-0001_v1.0.png","observed_sha256":base_sha},
            "image_audit_evidence":{"path":rel,"existence":"EXISTS",
                "expected_sha256":mvr.sha256(p.read_bytes()),
                "observed_sha256":mvr.sha256(p.read_bytes()),
                "observed_result":result},
        }
        side = {"image_audit_reference":rel,"image_audit_result":result}
        return td, root, rec, side, p

    def test_markdown_binding_pass(self):
        td,r,rec,side,p=self.fixture()
        with td: self.assertEqual((True,False),mvr._audit_binding(rec,r,side))
    def test_wrong_sidecar_path_fails(self):
        td,r,rec,side,p=self.fixture(); side["image_audit_reference"]="wrong.md"
        with td: self.assertEqual((False,False),mvr._audit_binding(rec,r,side))
    def test_wrong_identity_fails(self):
        td,r,rec,side,p=self.fixture(audit_asset="FILE-9999-IMG-9999")
        with td: self.assertEqual((False,False),mvr._audit_binding(rec,r,side))
    def test_nonpass_result_fails(self):
        td,r,rec,side,p=self.fixture(result="FAIL")
        with td: self.assertEqual((False,False),mvr._audit_binding(rec,r,side))
    def test_wrong_sha_rejected(self):
        td,r,rec,side,p=self.fixture(); rec["image_audit_evidence"]["expected_sha256"]="0"*64
        with td:
            self.assertEqual((False,False),mvr._audit_binding(rec,r,side))
    def test_absent_is_fail_not_limited(self):
        td,r,rec,side,p=self.fixture()
        with td:
            p.unlink(); rec["image_audit_evidence"].update({"existence":"ABSENT","expected_sha256":None,"observed_sha256":None})
            self.assertEqual((False,False),mvr._audit_binding(rec,r,side))
    def test_missing_sidecar_is_limited(self):
        td,r,rec,side,p=self.fixture()
        with td: self.assertEqual((False,True),mvr._audit_binding(rec,r,None))
    def writes(self):
        return [
            {"target_path":"cases/FILE-9999/registration-validations/FILE-9999-IMG-0001/FILE-9999-TXN-0001.json","operation":"CREATE","role":"CANONICAL_TARGET","prospective_sha256":"1"*64},
            {"target_path":"cases/FILE-9999/semantic-events/FILE-9999-EVT-0001.json","operation":"CREATE","role":"SEMANTIC_EVENT","prospective_sha256":"2"*64},
        ]
    def test_adapter_result_contract_pass(self):
        with tempfile.TemporaryDirectory() as td:
            result=mvr.MechanicalTransactionValidator(Path(td))("PROSPECTIVE",self.writes())
            Contracts().validate_definition("validationResult",result)
    def test_missing_layers_rejected(self):
        with self.assertRaises(Exception):
            Contracts().validate_definition("validationResult",{"status":"PASS","findings":[]})
    def test_extra_property_rejected(self):
        value=mvr._transaction_validation_result(); value["blocking"]=False
        with self.assertRaises(Exception): Contracts().validate_definition("validationResult",value)
