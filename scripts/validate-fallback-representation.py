#!/usr/bin/env python3
"""Read-only mechanical validator for ProjectORIGIN fallback representation validation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

try:
    from jsonschema import Draft202012Validator
except Exception:  # pragma: no cover - capability boundary
    Draft202012Validator = None

DRAFT = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_ID = "projectorigin://schemas/cases/fallback-representation-validation/v1.0"


class InvalidTarget(ValueError):
    pass


def duplicate_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise InvalidTarget("duplicate JSON key: " + key)
        value[key] = item
    return value


def load_schema(path: Path):
    if Draft202012Validator is None:
        raise RuntimeError("Draft202012Validator unavailable")
    schema = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=duplicate_object)
    if schema.get("$schema") != DRAFT or schema.get("$id") != SCHEMA_ID:
        raise InvalidTarget("unexpected fallback validation schema identity")
    Draft202012Validator.check_schema(schema)
    return schema, Draft202012Validator(schema)


def load_json_bytes(raw: bytes):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise InvalidTarget("UTF-8 BOM is not permitted")
    if b"\r" in raw:
        raise InvalidTarget("CR/CRLF is not canonical")
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise InvalidTarget("exactly one final LF is required")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidTarget("invalid UTF-8") from exc
    try:
        return json.loads(text, object_pairs_hook=duplicate_object)
    except (json.JSONDecodeError, InvalidTarget) as exc:
        raise InvalidTarget(str(exc)) from exc


def safe_relative(path: Path, root: Path) -> str:
    resolved_root = root.resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise InvalidTarget("path escapes repository root") from exc


def validate_bytes(raw: bytes, schema: dict, validator, repository_root: Path, input_path: Path):
    value = load_json_bytes(raw)
    errors = sorted(validator.iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        raise InvalidTarget("schema validation failed: " + errors[0].message)

    case_id = value["case_id"]
    req = value["requirement_id"]
    version = value["representation_version"]
    expected_rep = f"cases/{case_id}/fallback-representations/{case_id}_{req}_FALLBACK_{version}.md"
    expected_validation = f"cases/{case_id}/fallback-representations/{case_id}_{req}_FALLBACK-VALIDATION_{version}.json"
    expected_reader_ref = f"cases/{case_id}/image-requirements.json#{req}"

    if value["representation_reference"] != expected_rep:
        raise InvalidTarget("representation_reference does not match the formal filename contract")
    if value["reader_purpose_reference"] != expected_reader_ref:
        raise InvalidTarget("reader_purpose_reference does not bind the exact Image Requirement")
    if safe_relative(input_path, repository_root) != expected_validation:
        raise InvalidTarget("validation artifact path does not match the formal filename contract")

    candidate = repository_root / expected_rep
    if not candidate.is_file() or candidate.is_symlink():
        raise InvalidTarget("fallback representation candidate is missing or is a symlink")
    raw_candidate = candidate.read_bytes()
    if not raw_candidate:
        raise InvalidTarget("fallback representation candidate is empty")
    if raw_candidate.startswith(b"\xef\xbb\xbf"):
        raise InvalidTarget("fallback representation candidate contains UTF-8 BOM")
    try:
        raw_candidate.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidTarget("fallback representation candidate is not UTF-8") from exc
    observed = hashlib.sha256(raw_candidate).hexdigest()
    if observed != value["representation_sha256"]:
        raise InvalidTarget("representation_sha256 does not match candidate bytes")
    return value


def build_parser():
    p = argparse.ArgumentParser(description="Read-only fallback representation mechanical validator")
    p.add_argument("--schema", required=True, type=Path)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--repository-root", required=True, type=Path)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        schema, validator = load_schema(args.schema)
        validate_bytes(args.input.read_bytes(), schema, validator, args.repository_root, args.input)
    except RuntimeError as exc:
        print("VALIDATOR ERROR:", exc, file=sys.stderr)
        return 2
    except (OSError, InvalidTarget) as exc:
        print("VALIDATOR RESULT: INVALID —", exc, file=sys.stderr)
        return 1
    print("VALIDATOR RESULT: VALID — structural and exact-byte binding checks only; factual Reader Purpose sufficiency, Audit, Human Approval, Rights, registration, Repository Integration, and Publication authority are not independently established by this validator.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
