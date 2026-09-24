#!/usr/bin/env python3
"""Read-only Image Requirement Register validation; never an audit or approval.

This validates canonical v1.0 and successor v1.1 register bytes, structure and
local cross-field constraints. It cannot establish historical ID non-reuse,
Reader Purpose sufficiency as a factual matter, Rights, registration, placement,
blocker absence, Human Approval, workflow closure or publication authority.
No referenced asset or fallback representation is required to exist and no
evidence is created or changed.
"""

import argparse
import json
from pathlib import Path
import re
import sys

# CLI imports must not leave bytecode files behind.
sys.dont_write_bytecode = True

SCHEMA_ID = "urn:projectorigin:schema:cases:image-requirement-register:v1.1"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
ROOT = Path(__file__).resolve().parents[1]


class InvalidTarget(ValueError):
    """Invalid target bytes, structure or semantics (exit 1)."""


class CapabilityError(ValueError):
    """Unavailable validation capability or unusable schema (exit 2)."""


def parse_json(data):
    def pairs(entries):
        result = {}
        for key, value in entries:
            if key in result:
                raise InvalidTarget("duplicate JSON object key: " + key)
            result[key] = value
        return result

    def constant(value):
        raise InvalidTarget("non-JSON numeric constant: " + value)

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=constant)
    except (UnicodeError, ValueError) as exc:
        raise InvalidTarget(str(exc)) from exc


def load_schema(path):
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise CapabilityError("Draft202012Validator unavailable: " + str(exc)) from exc
    try:
        schema = parse_json(Path(path).read_bytes())
        if (not isinstance(schema, dict) or schema.get("$schema") != DRAFT
                or schema.get("$id") != SCHEMA_ID):
            raise ValueError("expected Image Requirement Register v1.1 schema identity and Draft 2020-12")
        Draft202012Validator.check_schema(schema)
        return schema, Draft202012Validator(schema)
    except Exception as exc:
        raise CapabilityError("schema unavailable/invalid: " + str(exc)) from exc


def canonical_bytes(value, schema):
    """Order by schema properties without normalizing any Unicode string."""
    def ordered(item, definition):
        if isinstance(item, dict):
            return {key: ordered(item[key], child)
                    for key, child in definition["properties"].items() if key in item}
        if isinstance(item, list):
            return [ordered(child, definition["items"]) for child in item]
        return item

    return (json.dumps(ordered(value, schema), ensure_ascii=False,
                       allow_nan=False, indent=2) + "\n").encode("utf-8")


def check_path(value, repository_root):
    # Existing canonical_ref convention, independently implemented read-only.
    if (value.startswith("/") or "\\" in value or "\x00" in value
            or re.match(r"^[A-Za-z]:", value)
            or any(part in ("", ".", "..") for part in value.split("/"))):
        raise InvalidTarget("invalid repository-relative asset path")
    root = Path(repository_root).resolve()
    try:
        (root / value).resolve().relative_to(root)
    except ValueError as exc:
        raise InvalidTarget("asset path escapes repository containment") from exc


def validate_bytes(data, schema, validator, repository_root=ROOT):
    if data.startswith(b"\xef\xbb\xbf"):
        raise InvalidTarget("UTF-8 BOM prohibited")
    if b"\r" in data:
        raise InvalidTarget("CR/CRLF prohibited")
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise InvalidTarget("exactly one final LF required")
    value = parse_json(data)
    error = next(validator.iter_errors(value), None)
    if error is not None:
        raise InvalidTarget("schema validation: " + error.message)

    previous = 0
    seen = set()
    for item in value["requirements"]:
        if item["case_id"] != value["case_id"]:
            raise InvalidTarget("Requirement case_id differs from register case_id")
        identifier = item["requirement_id"]
        if identifier in seen:
            raise InvalidTarget("duplicate requirement_id: " + identifier)
        serial = int(identifier[7:])
        if serial <= previous:
            raise InvalidTarget("Requirement IDs must be in ascending numeric order")
        previous = serial
        seen.add(identifier)
        asset = item["resulting_asset_reference"]
        if asset is not None:
            check_path(asset["repository_path"], repository_root)

        if value["register_format_version"] == "v1.1":
            mode = item["fulfillment_mode"]
            status = item["fulfillment_status"]
            representation = item["resulting_representation_reference"]

            if mode == "IMAGE_ASSET":
                if representation is not None:
                    raise InvalidTarget(
                        "IMAGE_ASSET fulfillment cannot use a fallback representation reference"
                    )
                if status == "SATISFIED" and asset is None:
                    raise InvalidTarget(
                        "SATISFIED IMAGE_ASSET fulfillment requires resulting_asset_reference"
                    )
                if status == "PENDING" and asset is not None:
                    raise InvalidTarget(
                        "PENDING IMAGE_ASSET fulfillment cannot have a resulting asset"
                    )
            elif mode == "FALLBACK_REPRESENTATION":
                if asset is not None:
                    raise InvalidTarget(
                        "FALLBACK_REPRESENTATION fulfillment cannot use an Approved Image Asset reference"
                    )
                if status == "SATISFIED" and representation is None:
                    raise InvalidTarget(
                        "SATISFIED FALLBACK_REPRESENTATION requires a validated representation reference"
                    )
                if status == "PENDING" and representation is not None:
                    raise InvalidTarget(
                        "PENDING FALLBACK_REPRESENTATION cannot have a resulting representation"
                    )
    try:
        canonical = canonical_bytes(value, schema)
    except UnicodeError as exc:
        raise InvalidTarget("invalid Unicode scalar value") from exc
    if data != canonical:
        raise InvalidTarget("noncanonical serialization or schema-defined key order")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        schema, validator = load_schema(args.schema)
        validate_bytes(args.input.read_bytes(), schema, validator)
    except InvalidTarget as exc:
        print("VALIDATOR RESULT: INVALID — " + str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print("VALIDATOR RESULT: ERROR — " + str(exc), file=sys.stderr)
        return 2
    print("VALIDATOR RESULT: VALID — structural, serialization and local semantic "
          "checks only; no Audit, Human, Rights, registration, placement, "
          "workflow or publication authority is established.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
