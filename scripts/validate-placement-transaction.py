#!/usr/bin/env python3
"""CPW-026 Placement Transaction validator and Case Bootstrap transaction adapter.

This module validates:
- PLACEMENT_RECORD
- CHANGE_IMPACT_ASSESSMENT
- exact cross-artifact binding
- exact Approved Image Asset identity/version/SHA
- sidecar caption/credit references
- caller-supplied Human-approved placement scope
- 4-write Case Bootstrap transaction shape:
  2 CANONICAL_TARGET + 2 SEMANTIC_EVENT

Validation creates no Human authority, no Publication Repository Integration,
no Publication Status, and no CPW-026 closure by itself.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

try:
    from case_bootstrap.contracts import Contracts
except ImportError:
    # Support direct execution from repository root/scripts.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from case_bootstrap.contracts import Contracts


PLACEMENT_SCHEMA = "schemas/cases/placement-record.schema.json"
IMPACT_SCHEMA = "schemas/cases/change-impact-assessment.schema.json"
IMPLEMENTATION_PATH = "scripts/validate-placement-transaction.py"
IMPACT_KEYS = (
    "AUDIT",
    "HUMAN_READ_REVIEW",
    "HUMAN_VISUAL_REVIEW",
    "PLACEMENT",
    "HUMAN_REVIEW_PACKAGE",
)


class PlacementValidationError(RuntimeError):
    pass


def require(cond: bool, message: str) -> None:
    if not cond:
        raise PlacementValidationError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "DUPLICATE_JSON_KEY:" + str(key))
        out[key] = value
    return out


def load_json_strict_bytes(raw: bytes) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF8_BOM_FORBIDDEN")
    require(b"\r" not in raw, "CR_BYTES_FORBIDDEN")
    require(raw.endswith(b"\n"), "FINAL_LF_REQUIRED")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PlacementValidationError("INVALID_UTF8") from exc
    try:
        return json.loads(text, object_pairs_hook=strict_pairs)
    except json.JSONDecodeError as exc:
        raise PlacementValidationError("INVALID_JSON:" + str(exc)) from exc


def load_json_strict(path: Path) -> Any:
    return load_json_strict_bytes(path.read_bytes())


def at(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative and not relative.startswith("/"),
            "ABSOLUTE_OR_EMPTY_PATH")
    parts = Path(relative).parts
    require(".." not in parts, "PARENT_PATH_FORBIDDEN")
    target = (root / relative).resolve()
    root_real = root.resolve()
    require(target == root_real or root_real in target.parents, "PATH_ESCAPE")
    return target


def _schema(root: Path, relative: str) -> dict:
    return load_json_strict(at(root, relative))


def _validate_schema(value: dict, schema: dict, label: str) -> None:
    errors = list(Draft202012Validator(
        schema, format_checker=FormatChecker()
    ).iter_errors(value))
    require(not errors, "SCHEMA_ERROR:" + label + ":" + "; ".join(e.message for e in errors))


def canonical_placement_path(case_id: str, transaction_id: str) -> str:
    return f"cases/{case_id}/placement-transactions/{transaction_id}/placement-record.json"


def canonical_impact_path(case_id: str, transaction_id: str) -> str:
    return f"cases/{case_id}/placement-transactions/{transaction_id}/change-impact-assessment.json"


def _verify_governing_references(root: Path, references: list[dict], label: str) -> None:
    for ref in references:
        path = at(root, ref["document_path"])
        require(path.is_file() and not path.is_symlink(), label + ":GOVERNING_REFERENCE_MISSING")
        require(sha256(path.read_bytes()) == ref["sha256"],
                label + ":GOVERNING_REFERENCE_SHA_MISMATCH")


def _verify_validator_identity(root: Path, identity: dict, label: str) -> None:
    require(identity["implementation_path"] == IMPLEMENTATION_PATH,
            label + ":VALIDATOR_PATH_MISMATCH")
    path = at(root, IMPLEMENTATION_PATH)
    require(path.is_file() and not path.is_symlink(), label + ":VALIDATOR_MISSING")
    require(sha256(path.read_bytes()) == identity["sha256"],
            label + ":VALIDATOR_SHA_MISMATCH")


def _scope_tuple(item: dict) -> tuple:
    return (
        item["target_artifact_identity"],
        item["target_artifact_version"],
        item["asset_id"],
        item["asset_version"],
        item["section"],
        item["slot"],
    )


def _normalize_expected_scope(expected_scope: Any) -> tuple[tuple, ...]:
    require(isinstance(expected_scope, list) and expected_scope,
            "EXPECTED_SCOPE_REQUIRED")
    normalized = []
    required = {
        "target_artifact_identity", "target_artifact_version",
        "asset_id", "asset_version", "section", "slot",
    }
    for item in expected_scope:
        require(isinstance(item, dict) and required <= set(item),
                "EXPECTED_SCOPE_INVALID")
        normalized.append(tuple(item[k] for k in (
            "target_artifact_identity", "target_artifact_version",
            "asset_id", "asset_version", "section", "slot",
        )))
    require(len(normalized) == len(set(normalized)), "EXPECTED_SCOPE_DUPLICATE")
    return tuple(sorted(normalized))


def _verify_sidecar_binding(root: Path, case_id: str, placement: dict) -> None:
    asset_id = placement["asset_id"]
    asset_version = placement["asset_version"]
    require(asset_id.startswith(case_id + "-IMG-"), "ASSET_CASE_MISMATCH")

    side = placement["sidecar_reference"]
    caption = placement["caption_reference"]
    credit = placement["credit_reference"]
    require(caption["repository_path"] == side["repository_path"] ==
            credit["repository_path"], "SIDECAR_REFERENCE_PATH_MISMATCH")
    require(caption["sha256"] == side["sha256"] == credit["sha256"],
            "SIDECAR_REFERENCE_SHA_MISMATCH")
    require(caption["json_pointer"] == "/caption", "CAPTION_POINTER_INVALID")
    require(credit["json_pointer"] == "/credit", "CREDIT_POINTER_INVALID")

    expected_sidecar = (
        f"cases/{case_id}/assets/{asset_id}_{asset_version}.metadata.json"
    )
    require(side["repository_path"] == expected_sidecar,
            "SIDECAR_CANONICAL_PATH_MISMATCH")

    path = at(root, side["repository_path"])
    require(path.is_file() and not path.is_symlink(), "SIDECAR_MISSING")
    raw = path.read_bytes()
    require(sha256(raw) == side["sha256"], "SIDECAR_SHA_MISMATCH")
    value = load_json_strict_bytes(raw)

    require(value.get("asset_id") == asset_id, "SIDECAR_ASSET_ID_MISMATCH")
    require(value.get("asset_version") == asset_version, "SIDECAR_ASSET_VERSION_MISMATCH")
    require(value.get("sha256") == placement["sha256"], "SIDECAR_BASE_SHA_MISMATCH")
    require(value.get("management_status") == "APPROVED", "ASSET_NOT_APPROVED")
    require(isinstance(value.get("caption"), str) and value["caption"],
            "SIDECAR_CAPTION_MISSING")
    require(isinstance(value.get("credit"), str) and value["credit"],
            "SIDECAR_CREDIT_MISSING")
    filename = value.get("filename")
    require(isinstance(filename, str) and filename, "SIDECAR_FILENAME_MISSING")
    base = path.parent / filename
    require(base.is_file() and not base.is_symlink(), "BASE_ASSET_MISSING")
    require(sha256(base.read_bytes()) == placement["sha256"],
            "BASE_ASSET_SHA_MISMATCH")


def _verify_placement_semantics(root: Path, record: dict, expected_scope: Any) -> None:
    case_id = record["case_id"]
    txn = record["transaction_id"]
    require(txn.startswith(case_id + "-TXN-"), "TRANSACTION_CASE_MISMATCH")

    observed_scope = tuple(sorted(_scope_tuple(x) for x in record["placements"]))
    require(observed_scope == _normalize_expected_scope(expected_scope),
            "HUMAN_APPROVED_SCOPE_MISMATCH")

    seen_assets = set()
    for placement in record["placements"]:
        require(placement["target_artifact_identity"].startswith(case_id + "_"),
                "TARGET_ARTIFACT_CASE_MISMATCH")
        require(
            placement["target_artifact_identity"].endswith(
                "_" + placement["target_artifact_version"] + ".md"
            ),
            "TARGET_ARTIFACT_VERSION_MISMATCH",
        )
        require(placement["asset_id"] not in seen_assets, "DUPLICATE_ASSET_PLACEMENT")
        seen_assets.add(placement["asset_id"])
        _verify_sidecar_binding(root, case_id, placement)

        state = placement["rollback_failure_state"]
        if placement["placement_result"] == "PLACED":
            require(state == {
                "rollback_required": False,
                "rollback_performed": False,
                "failure_state": "NONE",
            }, "PLACED_ROLLBACK_STATE_INVALID")
        if placement["placement_result"] == "FAILED":
            require(state["failure_state"] != "NONE", "FAILED_STATE_NOT_RECORDED")

    _verify_governing_references(root, record["governing_references"], "PLACEMENT")
    _verify_validator_identity(root, record["validator_identity"], "PLACEMENT")


def _audit_aggregate(record: dict) -> str:
    values = [p["re_audit_determination"] for p in record["placements"]]
    if "REQUIRED" in values:
        return "REQUIRED"
    if "UNDETERMINED" in values:
        return "UNDETERMINED"
    return "NOT_REQUIRED"


def _verify_impact_semantics(root: Path, placement: dict, impact: dict,
                             placement_raw: bytes) -> None:
    require(impact["case_id"] == placement["case_id"], "IMPACT_CASE_MISMATCH")
    require(impact["transaction_id"] == placement["transaction_id"], "IMPACT_TXN_MISMATCH")
    case_id = placement["case_id"]
    txn = placement["transaction_id"]

    ref = impact["placement_record_reference"]
    require(ref["artifact_id"] == txn and ref["transaction_id"] == txn,
            "PLACEMENT_REFERENCE_IDENTITY_MISMATCH")
    require(ref["repository_path"] == canonical_placement_path(case_id, txn),
            "PLACEMENT_REFERENCE_PATH_MISMATCH")
    require(ref["sha256"] == sha256(placement_raw),
            "PLACEMENT_REFERENCE_SHA_MISMATCH")

    impacts = impact["impact_determinations"]
    require(tuple(impacts.keys()) == IMPACT_KEYS or set(impacts) == set(IMPACT_KEYS),
            "IMPACT_KEY_SET_MISMATCH")
    require(impacts["AUDIT"]["determination"] == _audit_aggregate(placement),
            "AUDIT_IMPACT_AGGREGATION_MISMATCH")

    computed_closed = True
    for key in IMPACT_KEYS:
        item = impacts[key]
        if item["determination"] == "UNDETERMINED":
            require(item["closure_state"] == "OPEN",
                    key + ":UNDETERMINED_MUST_BE_OPEN")
        if item["determination"] == "NOT_REQUIRED":
            require(item["closure_state"] == "CLOSED",
                    key + ":NOT_REQUIRED_MUST_BE_CLOSED")
        if item["determination"] == "REQUIRED" and item["closure_state"] == "CLOSED":
            require(bool(item["evidence_references"]),
                    key + ":CLOSED_REQUIRED_IMPACT_NEEDS_EVIDENCE")
        if item["closure_state"] != "CLOSED" or item["determination"] == "UNDETERMINED":
            computed_closed = False

    require(impact["all_applicable_impacts_closed"] == computed_closed,
            "IMPACT_CLOSURE_AGGREGATION_MISMATCH")
    require(impact["automatic_global_invalidation"] is False,
            "AUTOMATIC_GLOBAL_INVALIDATION_FORBIDDEN")

    _verify_governing_references(root, impact["governing_references"], "IMPACT")
    _verify_validator_identity(root, impact["validator_identity"], "IMPACT")


def validate_bundle_bytes(
    placement_raw: bytes,
    placement_relative_path: str,
    impact_raw: bytes,
    impact_relative_path: str,
    repository_root: Path,
    expected_scope: Any,
    placement_schema_path: Path | None = None,
    impact_schema_path: Path | None = None,
) -> tuple[dict, dict]:
    placement = load_json_strict_bytes(placement_raw)
    impact = load_json_strict_bytes(impact_raw)

    pschema = load_json_strict(placement_schema_path) if placement_schema_path else _schema(repository_root, PLACEMENT_SCHEMA)
    ischema = load_json_strict(impact_schema_path) if impact_schema_path else _schema(repository_root, IMPACT_SCHEMA)

    _validate_schema(placement, pschema, "PLACEMENT_RECORD")
    _validate_schema(impact, ischema, "CHANGE_IMPACT_ASSESSMENT")

    case_id = placement["case_id"]
    txn = placement["transaction_id"]
    require(placement_relative_path == canonical_placement_path(case_id, txn),
            "PLACEMENT_CANONICAL_PATH_MISMATCH")
    require(impact_relative_path == canonical_impact_path(case_id, txn),
            "IMPACT_CANONICAL_PATH_MISMATCH")

    _verify_placement_semantics(repository_root, placement, expected_scope)
    _verify_impact_semantics(repository_root, placement, impact, placement_raw)
    return placement, impact


def validate_bundle(
    placement_path: Path,
    impact_path: Path,
    repository_root: Path,
    expected_scope: Any,
    placement_schema_path: Path | None = None,
    impact_schema_path: Path | None = None,
) -> tuple[dict, dict]:
    # macOS may expose TemporaryDirectory paths as /var/... while Path.resolve()
    # canonicalizes descendants to /private/var/.... Resolve both sides before
    # relative_to() so canonical-path validation is stable across that alias.
    root_real = repository_root.resolve()
    placement_real = placement_path.resolve()
    impact_real = impact_path.resolve()
    return validate_bundle_bytes(
        placement_real.read_bytes(),
        str(placement_real.relative_to(root_real)),
        impact_real.read_bytes(),
        str(impact_real.relative_to(root_real)),
        root_real,
        expected_scope,
        placement_schema_path,
        impact_schema_path,
    )


def _walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from _walk_dicts(child)


def _extract_write_dicts(args, kwargs):
    seen = []
    ids = set()
    for root in (args, kwargs):
        for obj in _walk_dicts(root):
            if {"target_path", "operation", "role"} <= set(obj):
                if id(obj) not in ids:
                    ids.add(id(obj))
                    seen.append(obj)
    return seen


def _write_digest(write: dict) -> str | None:
    raw = write.get("bytes")
    if isinstance(raw, (bytes, bytearray)):
        return sha256(bytes(raw))
    return write.get("prospective_sha256") or write.get("sha256")


def _transaction_validation_result() -> dict:
    return {
        "status": "PASS",
        "layers": {
            "SCHEMA": "PASS",
            "SEMANTIC": "PASS",
            "CROSS_ARTIFACT": "PASS",
            "GOVERNANCE": "PASS",
        },
        "findings": [],
    }


def _event_binding(event: dict) -> tuple:
    ref = event["record_ref"]
    return (
        ref.get("ref_id"),
        ref.get("artifact_type"),
        ref.get("artifact_id"),
        ref.get("repository_path"),
        ref.get("sha256"),
        ref.get("source_step"),
    )


def _validate_events(event_writes: list[dict], case_id: str, txn: str,
                     placement_path: str, placement_sha: str,
                     impact_path: str, impact_sha: str,
                     from_disk: bool, root: Path) -> None:
    expected = {
        (
            "placement-record",
            "PLACEMENT_RECORD",
            txn,
            placement_path,
            placement_sha,
            "CPW-026",
        ),
        (
            "change-impact-assessment",
            "CHANGE_IMPACT_ASSESSMENT",
            txn,
            impact_path,
            impact_sha,
            "CPW-026",
        ),
    }
    observed = set()
    event_ids = set()
    contracts = Contracts()
    for write in event_writes:
        raw = (
            at(root, write["target_path"]).read_bytes()
            if from_disk else write.get("bytes")
        )
        require(isinstance(raw, (bytes, bytearray)), "SEMANTIC_EVENT_BYTES_REQUIRED")
        event = load_json_strict_bytes(bytes(raw))
        contracts.validate_event(event)
        require(event["event_type"] == "RECORD_CREATED", "PLACEMENT_EVENT_TYPE_INVALID")
        require(event["authority_type"] == "NONE" and event["authority_reference"] is None,
                "PLACEMENT_EVENT_AUTHORITY_INVALID")
        require(event["previous_state"] is None and event["new_state"] is None,
                "PLACEMENT_EVENT_STATE_DELTA_INVALID")
        require(event["event_id"] not in event_ids, "SEMANTIC_EVENT_ID_DUPLICATE")
        event_ids.add(event["event_id"])
        require(
            write["target_path"] ==
            f"cases/{case_id}/semantic-events/{event['event_id']}.json",
            "SEMANTIC_EVENT_TARGET_PATH_MISMATCH",
        )
        observed.add(_event_binding(event))
    require(observed == expected, "SEMANTIC_EVENT_RECORD_BINDING_MISMATCH")


class PlacementTransactionValidator:
    def __init__(
        self,
        repository_root: Path,
        expected_scope: Any,
        placement_schema_path: Path | None = None,
        impact_schema_path: Path | None = None,
    ):
        self.root = repository_root
        self.expected_scope = expected_scope
        _normalize_expected_scope(expected_scope)
        self.placement_schema_path = placement_schema_path
        self.impact_schema_path = impact_schema_path
        self._frozen = None
        self._phase = None

    def __call__(self, *args, **kwargs):
        phase = kwargs.get("phase")
        if phase is None:
            phase = next(
                (x for x in args if isinstance(x, str)
                 and x in ("PROSPECTIVE", "POST_WRITE")),
                None,
            )
        require(phase in ("PROSPECTIVE", "POST_WRITE"),
                "TRANSACTION_PHASE_UNRECOGNIZED")
        require(not (self._phase is None and phase == "POST_WRITE"),
                "POST_WRITE_BEFORE_PROSPECTIVE")
        require(self._phase != "POST_WRITE",
                "VALIDATOR_INSTANCE_REUSED_AFTER_POST_WRITE")

        writes = _extract_write_dicts(args, kwargs)
        writes = list({
            (w["target_path"], w["operation"], w["role"]): w
            for w in writes
        }.values())
        require(len(writes) == 4, "PLACEMENT_TRANSACTION_EXACT_FOUR_WRITES_REQUIRED")
        require(all(w["operation"] == "CREATE" for w in writes),
                "PLACEMENT_TRANSACTION_CREATE_ONLY")
        require(sum(w["role"] == "CANONICAL_TARGET" for w in writes) == 2,
                "PLACEMENT_TRANSACTION_CANONICAL_TARGET_COUNT")
        require(sum(w["role"] == "SEMANTIC_EVENT" for w in writes) == 2,
                "PLACEMENT_TRANSACTION_SEMANTIC_EVENT_COUNT")

        canonical = [w for w in writes if w["role"] == "CANONICAL_TARGET"]
        event_writes = [w for w in writes if w["role"] == "SEMANTIC_EVENT"]
        placement_write = next(
            (w for w in canonical if w["target_path"].endswith("/placement-record.json")),
            None,
        )
        impact_write = next(
            (w for w in canonical if w["target_path"].endswith("/change-impact-assessment.json")),
            None,
        )
        require(placement_write is not None and impact_write is not None,
                "PLACEMENT_TRANSACTION_CANONICAL_TARGET_SET")

        descriptor = tuple(sorted(
            (w["target_path"], w["operation"], w["role"], _write_digest(w))
            for w in writes
        ))

        if phase == "PROSPECTIVE":
            praw = placement_write.get("bytes")
            iraw = impact_write.get("bytes")
            require(isinstance(praw, (bytes, bytearray)),
                    "PROSPECTIVE_PLACEMENT_BYTES_REQUIRED")
            require(isinstance(iraw, (bytes, bytearray)),
                    "PROSPECTIVE_IMPACT_BYTES_REQUIRED")
            placement, impact = validate_bundle_bytes(
                bytes(praw),
                placement_write["target_path"],
                bytes(iraw),
                impact_write["target_path"],
                self.root,
                self.expected_scope,
                self.placement_schema_path,
                self.impact_schema_path,
            )
            _validate_events(
                event_writes,
                placement["case_id"],
                placement["transaction_id"],
                placement_write["target_path"],
                sha256(bytes(praw)),
                impact_write["target_path"],
                sha256(bytes(iraw)),
                False,
                self.root,
            )
            self._frozen = descriptor
            self._phase = phase
        else:
            require(descriptor == self._frozen, "POST_WRITE_DESCRIPTOR_MISMATCH")
            ppath = at(self.root, placement_write["target_path"])
            ipath = at(self.root, impact_write["target_path"])
            require(ppath.is_file(), "POST_WRITE_PLACEMENT_RECORD_MISSING")
            require(ipath.is_file(), "POST_WRITE_IMPACT_RECORD_MISSING")
            placement, impact = validate_bundle(
                ppath,
                ipath,
                self.root,
                self.expected_scope,
                self.placement_schema_path,
                self.impact_schema_path,
            )
            _validate_events(
                event_writes,
                placement["case_id"],
                placement["transaction_id"],
                placement_write["target_path"],
                sha256(ppath.read_bytes()),
                impact_write["target_path"],
                sha256(ipath.read_bytes()),
                True,
                self.root,
            )
            self._phase = phase

        return _transaction_validation_result()


def placement_transaction_validator(repository_root: Path, expected_scope: Any,
                                    placement_schema_path: Path | None = None,
                                    impact_schema_path: Path | None = None):
    return PlacementTransactionValidator(
        repository_root,
        expected_scope,
        placement_schema_path,
        impact_schema_path,
    )


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--repository-root", type=Path, required=True)
    p.add_argument("--placement-record", type=Path, required=True)
    p.add_argument("--change-impact-assessment", type=Path, required=True)
    p.add_argument("--expected-scope-file", type=Path, required=True)
    p.add_argument("--placement-schema", type=Path)
    p.add_argument("--impact-schema", type=Path)
    p.add_argument("--format", choices=("human", "json"), default="human")
    args = p.parse_args(argv)
    try:
        expected_scope = load_json_strict(args.expected_scope_file)
        validate_bundle(
            args.placement_record,
            args.change_impact_assessment,
            args.repository_root,
            expected_scope,
            args.placement_schema,
            args.impact_schema,
        )
        report = {"validator_result": "PASS", "exit_code": 0}
    except Exception as exc:
        report = {"validator_result": "FAIL", "error": str(exc), "exit_code": 1}
    print(
        json.dumps(report, ensure_ascii=False, indent=2)
        if args.format == "json"
        else "\n".join(f"{k}: {v}" for k, v in report.items())
    )
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
