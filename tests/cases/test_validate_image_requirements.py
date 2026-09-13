"""Synthetic Decision 126/142 tests; never creates a production Case artifact."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validate-image-requirements.py"
SCHEMA = ROOT / "schemas/cases/image-requirement-register.schema.json"
spec = importlib.util.spec_from_file_location("image_requirements_validator", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def requirement(serial=1):
    return {
        "requirement_id": "IMGREQ-%03d" % serial,
        "case_id": "FILE-9876",
        "requirement_status": "REQUIRED",
        "reader_purpose": "合成テスト用の説明図",
        "classification_candidate": "Diagram",
        "production_route": "Synthetic diagram candidate",
        "dependency_references": [],
        "source_rights_references": [],
        "intended_placement_references": [],
        "current_orchestration_state": "Synthetic descriptive state",
        "blocking_reasons": [],
        "resulting_asset_reference": None,
        "completion_condition": "Separately authoritative completion evidence",
    }


def register(*serials):
    return {
        "register_format_version": "v1.0",
        "artifact_type": "IMAGE_REQUIREMENT_REGISTER",
        "case_id": "FILE-9876",
        "requirements": [requirement(serial) for serial in serials],
    }


def asset():
    return {
        "asset_id": "FILE-9876-IMG-0042",
        "asset_version": "v1.0",
        "repository_path": "cases/FILE-9876/assets/FILE-9876-IMG-0042_v1.0.svg",
        "sha256": "abcdef0123456789" * 4,
    }


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def snapshot(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file() and not path.is_symlink()}


class ImageRequirementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema, cls.validator = module.load_schema(SCHEMA)

    def check(self, value):
        module.validate_bytes(encoded(value), self.schema, self.validator)

    def reject(self, data):
        with self.assertRaises(module.InvalidTarget):
            module.validate_bytes(data, self.schema, self.validator)

    def cli(self, target, *extra, cwd=None):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--schema", str(SCHEMA),
             "--input", str(target), *extra], cwd=cwd,
            capture_output=True, text=True,
        )

    def test_valid_empty_register(self):
        self.check(register())

    def test_valid_multiple_items(self):
        self.check(register(1, 2, 3))

    def test_missing_requirement_property(self):
        for key in requirement():
            with self.subTest(key=key):
                value = register(1)
                del value["requirements"][0][key]
                self.reject(encoded(value))

    def test_noncontiguous_ids(self):
        self.check(register(1, 12, 999))

    def test_empty_reference_arrays(self):
        self.check(register(1))

    def test_empty_blocking_reasons(self):
        self.check(register(1))

    def test_null_resulting_asset(self):
        self.check(register(1))

    def test_valid_populated_asset(self):
        value = register(1)
        value["requirements"][0]["resulting_asset_reference"] = asset()
        self.check(value)

    def test_reference_strings_are_descriptive(self):
        value = register(1)
        item = value["requirements"][0]
        for key in ("dependency_references", "source_rights_references",
                    "intended_placement_references", "blocking_reasons"):
            item[key] = ["Synthetic reference; no authority asserted"]
        self.check(value)

    def test_optional_and_required_do_not_determine_completion(self):
        for status in ("OPTIONAL", "REQUIRED"):
            value = register(1)
            item = value["requirements"][0]
            item["requirement_status"] = status
            item["current_orchestration_state"] = "Unresolved, descriptive only"
            item["blocking_reasons"] = ["Synthetic unresolved issue"]
            self.check(value)

    def test_all_classifications(self):
        for classification in ("Historical Photo", "Document Scan", "Map", "Diagram",
                               "AI Visualization", "Reconstruction", "Background Image",
                               "Case Card Image", None):
            value = register(1)
            value["requirements"][0]["classification_candidate"] = classification
            self.check(value)

    def test_unicode_is_preserved_without_normalization(self):
        for text in ("é", "e\u0301", "日本語", "\U0001f30f"):
            value = register(1)
            value["requirements"][0]["reader_purpose"] = text
            original = encoded(value)
            self.check(value)
            self.assertEqual(module.canonical_bytes(value, self.schema), original)

    def test_schema_capability(self):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(self.schema["$schema"], module.DRAFT)
        self.assertEqual(self.schema["$id"], module.SCHEMA_ID)

    def test_input_bytes_unchanged_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            for data, code in ((encoded(register(1)), 0), (b"{}\n", 1)):
                path.write_bytes(data)
                self.assertEqual(self.cli(path).returncode, code)
                self.assertEqual(path.read_bytes(), data)

    def test_no_repository_or_git_write_side_effects(self):
        with tempfile.TemporaryDirectory() as directory:
            sandbox = Path(directory)
            (sandbox / ".git").mkdir()
            (sandbox / ".git/HEAD").write_text("ref: refs/heads/synthetic\n")
            path = sandbox / "synthetic.json"
            path.write_bytes(encoded(register(1)))
            before = snapshot(ROOT)
            local_before = snapshot(sandbox)
            self.assertEqual(self.cli(path, cwd=sandbox).returncode, 0)
            self.assertEqual(snapshot(ROOT), before)
            self.assertEqual(snapshot(sandbox), local_before)

    def test_cli_valid_exit_zero_and_authority_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_bytes(encoded(register()))
            result = self.cli(path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(result.stdout.startswith("VALIDATOR RESULT: VALID"))
            self.assertIn("no Audit, Human, Rights", result.stdout)
            self.assertNotIn("AUDIT RESULT", result.stdout)

    def test_cli_invalid_exit_one(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_bytes(b"{}\n")
            self.assertEqual(self.cli(path).returncode, 1)

    def test_cli_bad_invocation_exit_two(self):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT)], capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_cli_missing_input_exit_two(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.cli(Path(directory) / "missing.json").returncode, 2)

    def test_cli_missing_capability_exit_two(self):
        result = subprocess.run(
            [sys.executable, "-B", "-S", str(SCRIPT), "--schema", str(SCHEMA),
             "--input", "unused-synthetic.json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Draft202012Validator unavailable", result.stderr)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repository"
            root.mkdir()
            (root / "outside").symlink_to(Path(directory), target_is_directory=True)
            with self.assertRaises(module.InvalidTarget):
                module.check_path("outside/synthetic.svg", root)

    def test_missing_asset_fields(self):
        for key in asset():
            value = register(1)
            ref = asset()
            del ref[key]
            value["requirements"][0]["resulting_asset_reference"] = ref
            self.reject(encoded(value))


def add_invalid_test(name, transform):
    def test(self):
        self.reject(transform())
    setattr(ImageRequirementTests, "test_" + name, test)


def changed(scope, key, value):
    def fixture():
        document = register(1)
        target = document
        if scope in ("item", "asset"):
            target = document["requirements"][0]
        if scope == "asset":
            target["resulting_asset_reference"] = asset()
            target = target["resulting_asset_reference"]
        target[key] = copy.deepcopy(value)
        return encoded(document)
    return fixture


for name, scope, key, value in [
    ("unknown_top_property", "top", "unknown", True),
    ("unknown_requirement_property", "item", "unknown", True),
    ("invalid_status", "item", "requirement_status", "COMPLETE"),
    ("invalid_classification", "item", "classification_candidate", "Photo"),
    ("zero_requirement_id", "item", "requirement_id", "IMGREQ-000"),
    ("malformed_requirement_id", "item", "requirement_id", "IMGREQ-1"),
    ("case_mismatch", "item", "case_id", "FILE-9875"),
    ("malformed_case_id", "top", "case_id", "FILE-123"),
    ("zero_case_id", "top", "case_id", "FILE-0000"),
    ("wrong_version", "top", "register_format_version", "v2.0"),
    ("wrong_artifact_type", "top", "artifact_type", "OTHER"),
    ("requirements_not_array", "top", "requirements", {}),
    ("extra_asset_property", "asset", "unknown", True),
    ("malformed_sha", "asset", "sha256", "a" * 63),
    ("uppercase_sha", "asset", "sha256", "A" * 64),
    ("absolute_path", "asset", "repository_path", "/tmp/synthetic.svg"),
    ("traversal_path", "asset", "repository_path", "../synthetic.svg"),
    ("embedded_traversal", "asset", "repository_path", "cases/../../synthetic.svg"),
    ("windows_absolute_path", "asset", "repository_path", "C:\\synthetic.svg"),
    ("backslash_traversal", "asset", "repository_path", "..\\synthetic.svg"),
    ("nul_path", "asset", "repository_path", "bad\x00path"),
    ("empty_asset_path", "asset", "repository_path", ""),
    ("empty_asset_version", "asset", "asset_version", ""),
    ("malformed_asset_id", "asset", "asset_id", "IMGREQ-001"),
    ("asset_sha_final_newline", "asset", "sha256", "a" * 64 + "\n"),
]:
    add_invalid_test(name, changed(scope, key, value))

for field in ("reader_purpose", "production_route", "current_orchestration_state",
              "completion_condition"):
    add_invalid_test("empty_" + field, changed("item", field, ""))

for field in ("dependency_references", "source_rights_references",
              "intended_placement_references", "blocking_reasons"):
    add_invalid_test("empty_string_" + field, changed("item", field, [""]))
    add_invalid_test("object_in_" + field, changed("item", field, [{}]))
    add_invalid_test("not_array_" + field, changed("item", field, "reference"))

add_invalid_test("duplicate_requirement_id", lambda: encoded(register(1, 1)))
add_invalid_test("descending_ids", lambda: encoded(register(2, 1)))
add_invalid_test("bom", lambda: b"\xef\xbb\xbf" + encoded(register()))
add_invalid_test("invalid_utf8", lambda: b"\xff\n")
add_invalid_test("duplicate_json_key", lambda: encoded(register()).replace(
    b'"case_id": "FILE-9876",', b'"case_id": "FILE-9876", "case_id": "FILE-9876",'))
add_invalid_test("nested_duplicate_json_key", lambda: encoded(register(1)).replace(
    b'"reader_purpose":', b'"requirement_id": "IMGREQ-001", "reader_purpose":'))
add_invalid_test("crlf", lambda: encoded(register()).replace(b"\n", b"\r\n"))
add_invalid_test("bare_cr", lambda: encoded(register()).replace(b"\n", b"\r", 1))
add_invalid_test("missing_final_lf", lambda: encoded(register())[:-1])
add_invalid_test("extra_final_lf", lambda: encoded(register()) + b"\n")
add_invalid_test("noncanonical_indentation", lambda: (
    json.dumps(register(), indent=4) + "\n").encode())
add_invalid_test("top_key_order", lambda: encoded(dict(reversed(list(register().items())))))


def wrong_nested_order(asset_reference=False):
    value = register(1)
    if asset_reference:
        value["requirements"][0]["resulting_asset_reference"] = dict(reversed(list(asset().items())))
    else:
        value["requirements"][0] = dict(reversed(list(requirement().items())))
    return encoded(value)


add_invalid_test("requirement_key_order", wrong_nested_order)
add_invalid_test("asset_key_order", lambda: wrong_nested_order(True))
add_invalid_test("escaped_unicode", lambda: (
    json.dumps(register(1), ensure_ascii=True, indent=2) + "\n").encode())
add_invalid_test("nonfinite_json", lambda: b'{"requirements": NaN}\n')
add_invalid_test("invalid_json", lambda: b'{\n')


if __name__ == "__main__":
    unittest.main()
