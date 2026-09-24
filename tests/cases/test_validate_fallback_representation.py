"""Synthetic tests for the read-only fallback representation mechanical validator."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validate-fallback-representation.py"
SCHEMA = ROOT / "schemas/cases/fallback-representation-validation.schema.json"
SPEC = importlib.util.spec_from_file_location("fallback_validator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


class FallbackRepresentationValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema, cls.validator = MODULE.load_schema(SCHEMA)

    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        case_id = "FILE-9876"
        req = "IMGREQ-001"
        version = "v1.0"
        directory = root / "cases" / case_id / "fallback-representations"
        directory.mkdir(parents=True)
        candidate = directory / f"{case_id}_{req}_FALLBACK_{version}.md"
        candidate.write_text("# Synthetic Document Source Card\n\nEvidence Boundary: synthetic only.\n", encoding="utf-8")
        data = {
            "validation_format_version": "v1.0",
            "artifact_type": "FALLBACK_REPRESENTATION_VALIDATION",
            "case_id": case_id,
            "requirement_id": req,
            "representation_type": "DOCUMENT_SOURCE_CARD",
            "representation_version": version,
            "representation_reference": f"cases/{case_id}/fallback-representations/{case_id}_{req}_FALLBACK_{version}.md",
            "representation_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
            "reader_purpose_reference": f"cases/{case_id}/image-requirements.json#{req}",
            "reader_purpose_result": "SATISFIED",
            "validation_basis": "Synthetic validation basis; no production authority.",
            "source_references": ["SRC-SYNTHETIC-001"],
            "institutional_locator": None,
            "evidence_boundary": "Synthetic fallback does not establish facts outside this fixture.",
            "validation_result": "VALIDATED_FALLBACK_REPRESENTATION",
        }
        target = directory / f"{case_id}_{req}_FALLBACK-VALIDATION_{version}.json"
        target.write_bytes(canonical(data))
        return root, candidate, target, data

    def validate(self, root, target):
        return MODULE.validate_bytes(target.read_bytes(), self.schema, self.validator, root, target)

    def test_valid_exact_binding(self):
        root, _, target, _ = self.fixture()
        self.validate(root, target)

    def test_wrong_candidate_sha_rejected(self):
        root, _, target, data = self.fixture()
        data["representation_sha256"] = "0" * 64
        target.write_bytes(canonical(data))
        with self.assertRaises(MODULE.InvalidTarget):
            self.validate(root, target)

    def test_wrong_representation_path_rejected(self):
        root, _, target, data = self.fixture()
        data["representation_reference"] = "cases/FILE-9876/fallback-representations/other.md"
        target.write_bytes(canonical(data))
        with self.assertRaises(MODULE.InvalidTarget):
            self.validate(root, target)

    def test_wrong_validation_path_rejected(self):
        root, _, target, data = self.fixture()
        wrong = target.with_name("wrong.json")
        wrong.write_bytes(canonical(data))
        with self.assertRaises(MODULE.InvalidTarget):
            self.validate(root, wrong)

    def test_asset_id_property_rejected(self):
        root, _, target, data = self.fixture()
        data["asset_id"] = "FILE-9876-IMG-0001"
        target.write_bytes(canonical(data))
        with self.assertRaises(MODULE.InvalidTarget):
            self.validate(root, target)

    def test_nonvalidated_state_rejected(self):
        root, _, target, data = self.fixture()
        data["validation_result"] = "APPROVED"
        target.write_bytes(canonical(data))
        with self.assertRaises(MODULE.InvalidTarget):
            self.validate(root, target)

    def test_cli_is_read_only_and_reports_boundary(self):
        root, _, target, _ = self.fixture()
        before = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
        cp = subprocess.run([
            sys.executable, "-B", str(SCRIPT), "--schema", str(SCHEMA),
            "--input", str(target), "--repository-root", str(root),
        ], capture_output=True, text=True)
        self.assertEqual(0, cp.returncode, cp.stderr)
        self.assertIn("VALIDATOR RESULT: VALID", cp.stdout)
        self.assertIn("not independently established", cp.stdout)
        after = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
