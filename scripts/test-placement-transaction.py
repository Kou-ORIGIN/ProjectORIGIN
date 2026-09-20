#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest

from case_bootstrap.contracts import Contracts


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / "scripts" / "validate-placement-transaction.py"
SPEC = importlib.util.spec_from_file_location("placement_validator", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(m)


def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def h(raw):
    return hashlib.sha256(raw).hexdigest()


class PlacementTransactionTests(unittest.TestCase):
    def fixture(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)

        (root / "schemas/cases").mkdir(parents=True)
        (root / "scripts").mkdir(parents=True)
        (root / "docs").mkdir(parents=True)
        (root / "cases/FILE-9999/assets").mkdir(parents=True)
        (root / "cases/FILE-9999/semantic-events").mkdir(parents=True)

        shutil.copy2(REPO / "schemas/cases/placement-record.schema.json",
                     root / "schemas/cases/placement-record.schema.json")
        shutil.copy2(REPO / "schemas/cases/change-impact-assessment.schema.json",
                     root / "schemas/cases/change-impact-assessment.schema.json")
        shutil.copy2(MODULE_PATH, root / "scripts/validate-placement-transaction.py")

        governing = []
        for rel, ver, raw in (
            ("docs/Image Rule.md", "v1.4", b"image-rule\n"),
            ("docs/ProjectORIGIN Repository Rule.md", "v1.2", b"repo-rule\n"),
            ("docs/Audit Rule.md", "v1.4.1", b"audit-rule\n"),
        ):
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
            governing.append({
                "document_path": rel,
                "applicable_version": ver,
                "sha256": h(raw),
            })

        base_raw = b"<svg>fixture</svg>\n"
        base_path = root / "cases/FILE-9999/assets/FILE-9999-IMG-0001_v1.0.svg"
        base_path.write_bytes(base_raw)
        side = {
            "asset_id": "FILE-9999-IMG-0001",
            "asset_version": "v1.0",
            "filename": base_path.name,
            "management_status": "APPROVED",
            "sha256": h(base_raw),
            "caption": "Fixture caption.",
            "credit": "Fixture credit.",
        }
        side_raw = jbytes(side)
        side_rel = "cases/FILE-9999/assets/FILE-9999-IMG-0001_v1.0.metadata.json"
        (root / side_rel).write_bytes(side_raw)

        validator_sha = h((root / "scripts/validate-placement-transaction.py").read_bytes())
        runtime = {
            "python_version": "3.x",
            "libraries": [{"name": "jsonschema", "version": "fixture"}],
        }
        scope = [{
            "target_artifact_identity": "FILE-9999_CLASSIFIED_v1.0.md",
            "target_artifact_version": "v1.0",
            "asset_id": "FILE-9999-IMG-0001",
            "asset_version": "v1.0",
            "section": "5.1 Fixture",
            "slot": "after section introduction",
        }]
        placement = {
            "record_format_version": "v1.0",
            "artifact_type": "PLACEMENT_RECORD",
            "case_id": "FILE-9999",
            "source_step": "CPW-026",
            "transaction_id": "FILE-9999-TXN-0001",
            "placements": [{
                **scope[0],
                "sha256": h(base_raw),
                "sidecar_reference": {
                    "repository_path": side_rel,
                    "sha256": h(side_raw),
                },
                "caption_reference": {
                    "repository_path": side_rel,
                    "sha256": h(side_raw),
                    "json_pointer": "/caption",
                },
                "credit_reference": {
                    "repository_path": side_rel,
                    "sha256": h(side_raw),
                    "json_pointer": "/credit",
                },
                "placement_operation_date": "2026-09-20T00:00:00Z",
                "placement_result": "PLACED",
                "affected_audit_references": [],
                "re_audit_determination": "NOT_REQUIRED",
                "rollback_failure_state": {
                    "rollback_required": False,
                    "rollback_performed": False,
                    "failure_state": "NONE",
                },
            }],
            "governing_references": governing,
            "validator_identity": {
                "implementation_path": "scripts/validate-placement-transaction.py",
                "sha256": validator_sha,
            },
            "runtime_identity": runtime,
            "created_at": "2026-09-20T00:00:00Z",
            "actor_id": "ACTOR-0001",
            "actor_role": "Repository / Data Agent",
        }
        placement_raw = jbytes(placement)
        placement_rel = m.canonical_placement_path("FILE-9999", "FILE-9999-TXN-0001")

        closed = lambda rationale: {
            "determination": "NOT_REQUIRED",
            "closure_state": "CLOSED",
            "rationale": rationale,
            "evidence_references": [],
        }
        impact = {
            "record_format_version": "v1.0",
            "artifact_type": "CHANGE_IMPACT_ASSESSMENT",
            "case_id": "FILE-9999",
            "source_step": "CPW-026",
            "transaction_id": "FILE-9999-TXN-0001",
            "placement_record_reference": {
                "artifact_type": "PLACEMENT_RECORD",
                "artifact_id": "FILE-9999-TXN-0001",
                "transaction_id": "FILE-9999-TXN-0001",
                "repository_path": placement_rel,
                "sha256": h(placement_raw),
            },
            "impact_determinations": {
                "AUDIT": closed("Fixture: no additional audit action."),
                "HUMAN_READ_REVIEW": closed("Fixture: no additional read review."),
                "HUMAN_VISUAL_REVIEW": closed("Fixture: no additional visual review."),
                "PLACEMENT": closed("Fixture placement impact closed."),
                "HUMAN_REVIEW_PACKAGE": closed("Fixture: no package impact."),
            },
            "automatic_global_invalidation": False,
            "all_applicable_impacts_closed": True,
            "governing_references": governing,
            "validator_identity": {
                "implementation_path": "scripts/validate-placement-transaction.py",
                "sha256": validator_sha,
            },
            "runtime_identity": runtime,
            "assessed_at": "2026-09-20T00:00:00Z",
            "actor_id": "ACTOR-0001",
            "actor_role": "Repository / Data Agent",
        }
        impact_raw = jbytes(impact)
        impact_rel = m.canonical_impact_path("FILE-9999", "FILE-9999-TXN-0001")

        def event(eid, ref_id, artifact_type, path, digest):
            return {
                "event_id": eid,
                "occurred_at": "2026-09-20T00:00:00Z",
                "event_type": "RECORD_CREATED",
                "record_ref": {
                    "ref_id": ref_id,
                    "artifact_type": artifact_type,
                    "required": True,
                    "applicability": "REQUIRED",
                    "artifact_id": "FILE-9999-TXN-0001",
                    "repository_path": path,
                    "sha256": digest,
                    "source_step": "CPW-026",
                },
                "actor_id": "ACTOR-0001",
                "actor_role": "Repository / Data Agent",
                "authority_type": "NONE",
                "authority_reference": None,
                "previous_state": None,
                "new_state": None,
                "evidence_references": [],
                "note": "Fixture RECORD_CREATED event.",
            }

        e1 = event(
            "FILE-9999-EVT-0001", "placement-record", "PLACEMENT_RECORD",
            placement_rel, h(placement_raw),
        )
        e2 = event(
            "FILE-9999-EVT-0002", "change-impact-assessment",
            "CHANGE_IMPACT_ASSESSMENT", impact_rel, h(impact_raw),
        )
        writes = [
            {
                "target_path": placement_rel,
                "operation": "CREATE",
                "role": "CANONICAL_TARGET",
                "bytes": placement_raw,
                "prospective_sha256": h(placement_raw),
            },
            {
                "target_path": impact_rel,
                "operation": "CREATE",
                "role": "CANONICAL_TARGET",
                "bytes": impact_raw,
                "prospective_sha256": h(impact_raw),
            },
            {
                "target_path": "cases/FILE-9999/semantic-events/FILE-9999-EVT-0001.json",
                "operation": "CREATE",
                "role": "SEMANTIC_EVENT",
                "bytes": jbytes(e1),
                "prospective_sha256": h(jbytes(e1)),
            },
            {
                "target_path": "cases/FILE-9999/semantic-events/FILE-9999-EVT-0002.json",
                "operation": "CREATE",
                "role": "SEMANTIC_EVENT",
                "bytes": jbytes(e2),
                "prospective_sha256": h(jbytes(e2)),
            },
        ]
        return td, root, scope, placement, impact, writes

    def test_valid_bundle(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            a, b = m.validate_bundle_bytes(
                writes[0]["bytes"], writes[0]["target_path"],
                writes[1]["bytes"], writes[1]["target_path"],
                root, scope,
            )
            self.assertEqual("PLACEMENT_RECORD", a["artifact_type"])
            self.assertEqual("CHANGE_IMPACT_ASSESSMENT", b["artifact_type"])

    def test_adapter_result_contract_pass(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            result = m.PlacementTransactionValidator(root, scope)("PROSPECTIVE", writes)
            Contracts().validate_definition("validationResult", result)

    def test_missing_write_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td, self.assertRaises(Exception):
            m.PlacementTransactionValidator(root, scope)("PROSPECTIVE", writes[:-1])

    def test_extra_write_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            extra = deepcopy(writes[0])
            extra["target_path"] += ".extra"
            with self.assertRaises(Exception):
                m.PlacementTransactionValidator(root, scope)("PROSPECTIVE", writes + [extra])

    def test_swapped_or_duplicate_event_binding_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            bad = deepcopy(writes)
            event = json.loads(bad[2]["bytes"].decode("utf-8"))
            event["record_ref"] = json.loads(bad[3]["bytes"].decode("utf-8"))["record_ref"]
            bad[2]["bytes"] = jbytes(event)
            bad[2]["prospective_sha256"] = h(bad[2]["bytes"])
            with self.assertRaises(Exception):
                m.PlacementTransactionValidator(root, scope)("PROSPECTIVE", bad)

    def test_sidecar_sha_mismatch_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            p = deepcopy(placement)
            p["placements"][0]["sidecar_reference"]["sha256"] = "0" * 64
            praw = jbytes(p)
            i = deepcopy(impact)
            i["placement_record_reference"]["sha256"] = h(praw)
            with self.assertRaises(Exception):
                m.validate_bundle_bytes(
                    praw, writes[0]["target_path"], jbytes(i), writes[1]["target_path"],
                    root, scope,
                )

    def test_caption_pointer_mismatch_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            p = deepcopy(placement)
            p["placements"][0]["caption_reference"]["json_pointer"] = "/credit"
            praw = jbytes(p)
            i = deepcopy(impact)
            i["placement_record_reference"]["sha256"] = h(praw)
            with self.assertRaises(Exception):
                m.validate_bundle_bytes(
                    praw, writes[0]["target_path"], jbytes(i), writes[1]["target_path"],
                    root, scope,
                )

    def test_human_scope_mismatch_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            wrong = deepcopy(scope)
            wrong[0]["slot"] = "different slot"
            with self.assertRaises(Exception):
                m.validate_bundle_bytes(
                    writes[0]["bytes"], writes[0]["target_path"],
                    writes[1]["bytes"], writes[1]["target_path"],
                    root, wrong,
                )

    def test_global_invalidation_true_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            i = deepcopy(impact)
            i["automatic_global_invalidation"] = True
            with self.assertRaises(Exception):
                m.validate_bundle_bytes(
                    writes[0]["bytes"], writes[0]["target_path"],
                    jbytes(i), writes[1]["target_path"],
                    root, scope,
                )

    def test_prospective_postwrite_descriptor_drift_rejected(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            v = m.PlacementTransactionValidator(root, scope)
            v("PROSPECTIVE", writes)
            drift = deepcopy(writes)
            drift[0]["prospective_sha256"] = "f" * 64
            drift[0].pop("bytes")
            with self.assertRaises(Exception):
                v("POST_WRITE", drift)

    def test_valid_postwrite(self):
        td, root, scope, placement, impact, writes = self.fixture()
        with td:
            v = m.PlacementTransactionValidator(root, scope)
            v("PROSPECTIVE", writes)
            for w in writes:
                p = root / w["target_path"]
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(w["bytes"])
            result = v("POST_WRITE", writes)
            Contracts().validate_definition("validationResult", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
