"""Decision 162 focused tests; all records are in-memory diagnostics."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.dont_write_bytecode = True
REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY / "scripts"))
from case_bootstrap.contracts import Contracts
from case_bootstrap.storage import OperationalError

REF = {"ref_id": "image-requirement-register", "artifact_type": "IMAGE_REQUIREMENT_REGISTER",
       "required": False, "applicability": "CONDITIONAL", "artifact_id": "FILE-0001",
       "repository_path": "cases/FILE-0001/image-requirements.json",
       "sha256": "ab76dc0a0b580f505c9b7f325b06e460b1631fd75b3a30d65a2887c58dacbd6b",
       "source_step": "CPW-019"}


def journal():
    stamp = "2026-09-14T00:00:00Z"
    value = {
        "record_format_version": "v0.1", "artifact_type": "TRANSACTION_JOURNAL",
        "case_id": "FILE-0001", "transaction_id": "FILE-0001-TXN-9876", "state": "PREPARED",
        "initiated_by_actor_id": "ACTOR-0001", "initiated_by_actor_role": "Image Agent",
        "created_at": stamp, "updated_at": stamp,
        "write_intent": [], "preconditions": [],
        "lease_binding": {"lease_path": ".projectorigin/leases/FILE-0001.json",
                          "lease_sha256": "0" * 64,
                          "allocation_record_ref": ".projectorigin/transaction-allocations/FILE-0001/FILE-0001-TXN-9876.json",
                          "allocation_record_sha256": "0" * 64, "acquired_at": stamp,
                          "expires_at": "2026-09-14T01:00:00Z"},
        "semantic_event_requirement": "REQUIRED",
        "required_semantic_events": [{"event_id": "FILE-0001-EVT-9876", "event_type": "RECORD_CREATED",
                                     "record_ref": copy.deepcopy(REF)}],
        "commit_window": {"entered": False, "entered_at": None}, "write_progress": [],
    }
    for path, role in [(REF["repository_path"], "CANONICAL_TARGET"),
                       ("cases/FILE-0001/semantic-events/FILE-0001-EVT-9876.json", "SEMANTIC_EVENT")]:
        base = {"target_path": path, "operation": "CREATE", "role": role}
        value["write_intent"].append({**base, "prospective_sha256": "0" * 64})
        value["preconditions"].append({"target_path": path, "existence": "MUST_NOT_EXIST", "sha256": None})
        value["write_progress"].append({**base, "progress_state": "NOT_STARTED", "last_observed_at": stamp})
    return value


class Focused(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = Contracts(REPOSITORY)
        actual = Path(sys.modules["case_bootstrap.contracts"].__file__).resolve()
        assert actual == (REPOSITORY / "scripts/case_bootstrap/contracts.py").resolve()

    def rejected(self, value, code="CROSS_CASE_IDENTITY", contracts=None):
        with self.assertRaises(OperationalError) as caught:
            (contracts or self.contracts).validate(value)
        self.assertEqual(caught.exception.code, code)

    def test_journal_singleton_reference(self):
        self.contracts.validate(journal())

    def test_prefixed_same_case_reference(self):
        value = journal()
        value["required_semantic_events"][0]["record_ref"]["artifact_id"] = "FILE-0001-IMG-0001"
        self.contracts.validate(value)

    def test_cross_case_singleton_reference(self):
        value = journal()
        value["required_semantic_events"][0]["record_ref"]["artifact_id"] = "FILE-0002"
        self.rejected(value)

    def test_cross_case_prefixed_reference(self):
        value = journal()
        value["required_semantic_events"][0]["record_ref"]["artifact_id"] = "FILE-0002-IMG-0001"
        self.rejected(value)

    def test_cpw019_exact_record_ref(self):
        self.contracts.validate_definition("artifactReference", REF)
        value = journal()
        self.assertEqual(value["required_semantic_events"][0]["record_ref"], REF)
        self.contracts.validate(value)

    def test_transaction_id_cross_case(self):
        value = journal()
        value["transaction_id"] = "FILE-0002-TXN-9876"
        self.rejected(value)

    def test_event_id_cross_case(self):
        value = journal()
        value["required_semantic_events"][0]["event_id"] = "FILE-0002-EVT-9876"
        self.rejected(value)

    def test_transaction_id_singleton_still_invalid(self):
        value = journal()
        value["transaction_id"] = "FILE-0001"
        self.rejected(value, "SCHEMA_ERROR")

    def test_event_id_singleton_still_invalid(self):
        value = journal()
        value["required_semantic_events"][0]["event_id"] = "FILE-0001"
        self.rejected(value, "SCHEMA_ERROR")

    def test_reference_sha_rules_preserved(self):
        value = journal()
        value["required_semantic_events"][0]["record_ref"]["sha256"] = "0" * 63
        self.rejected(value, "SCHEMA_ERROR")

    def test_reference_path_rules_preserved(self):
        value = journal()
        value["required_semantic_events"][0]["record_ref"]["repository_path"] = "../outside.json"
        with self.assertRaises(OperationalError):
            self.contracts.validate(value)

    def test_non_file_reference_identity_unchanged(self):
        value = journal()
        value["required_semantic_events"][0]["record_ref"]["artifact_id"] = "synthetic"
        self.contracts.validate(value)

    def test_reference_inside_nullable_branch(self):
        # Human decision reference is a real artifactReference, including anyOf descendants.
        definition = {"type": "object", "properties": {
            "artifact_type": {"const": "TRANSACTION_ALLOCATION"},
            "case_id": {"const": "FILE-0001"},
            "reference": {"anyOf": [
                {"$ref": "urn:projectorigin:schema:operations:operational-defs:v0.1#/$defs/artifactReference"},
                {"type": "null"}]}}}
        value = {"artifact_type": "TRANSACTION_ALLOCATION", "case_id": "FILE-0001", "reference": REF}
        with patch.object(self.contracts, "schema", return_value=definition):
            self.contracts.validate(value)

    def test_arbitrary_artifact_id_not_exempt(self):
        definition = {"type": "object", "properties": {
            "artifact_type": {"const": "TRANSACTION_ALLOCATION"},
            "case_id": {"const": "FILE-0001"}, "artifact_id": {"type": "string"}}}
        value = {"artifact_type": "TRANSACTION_ALLOCATION", "case_id": "FILE-0001", "artifact_id": "FILE-0001"}
        with patch.object(self.contracts, "schema", return_value=definition):
            self.rejected(value)

    def test_shape_lookalike_without_reference_schema_not_exempt(self):
        # Shape alone must never enable the exception: this is an ordinary object schema.
        reference_shape = self.contracts.definition("artifactReference")
        definition = {"type": "object", "properties": {
            "artifact_type": {"const": "TRANSACTION_ALLOCATION"},
            "case_id": {"const": "FILE-0001"}, "ordinary_object": reference_shape}}
        value = {"artifact_type": "TRANSACTION_ALLOCATION", "case_id": "FILE-0001",
                 "ordinary_object": copy.deepcopy(REF)}
        with patch.object(self.contracts, "schema", return_value=definition):
            self.rejected(value)

    def test_does_not_mutate_journal(self):
        value = journal()
        original = copy.deepcopy(value)
        self.contracts.validate(value)
        self.assertEqual(value, original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
