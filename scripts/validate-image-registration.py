#!/usr/bin/env python3
"""Decision 172 candidate: dedicated image mechanical-registration validator.

This module validates the truthfulness and fixity of a MECHANICAL_VALIDATION_RECORD
and provides a stateful Case Bootstrap transaction adapter. A successful
transaction validation means the record/event pair is truthfully storable; it
does not mean the mechanical result itself is PASS, and creates no Human
authority, Formal Audit, Registration Verification, closure, or placement.
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, importlib.metadata, json, re, sys
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker

CHECK_IDS = (
    'FILE_EXISTENCE','FILENAME','IDENTITY_UNIQUENESS','VERSION_CONSISTENCY',
    'BYTE_IDENTITY','SIDECAR_JSON','REQUIRED_METADATA','IMAGE_AUDIT_BINDING',
    'APPROVED_ELIGIBILITY','ASSET_PRESERVATION',
)
RESULTS = ('PASS','PASS_WITH_WARNINGS','FAIL','VALIDATION_LIMITED')
TOP_LEVEL = (
    'record_format_version','artifact_type','case_id','source_step','transaction_id',
    'requirement_id','asset_id','asset_version','register_evidence','base_asset_evidence',
    'sidecar_evidence','image_audit_evidence','management_status_observation',
    'governing_references','validator_identity','runtime_identity','validated_at',
    'actor_id','actor_role','checks','result','findings','prior_record_reference',
)

class MechanicalValidationError(RuntimeError):
    pass

def require(cond: bool, message: str) -> None:
    if not cond:
        raise MechanicalValidationError(message)

def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def strict_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'DUPLICATE_JSON_KEY:' + str(key))
        out[key] = value
    return out

def load_json_strict_bytes(raw: bytes) -> Any:
    require(not raw.startswith(b'\xef\xbb\xbf'), 'UTF8_BOM_FORBIDDEN')
    require(b'\r' not in raw, 'CR_BYTES_FORBIDDEN')
    require(raw.endswith(b'\n'), 'FINAL_LF_REQUIRED')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise MechanicalValidationError('INVALID_UTF8') from exc
    try:
        return json.loads(text, object_pairs_hook=strict_pairs)
    except json.JSONDecodeError as exc:
        raise MechanicalValidationError('INVALID_JSON:' + str(exc)) from exc

def load_json_strict(path: Path) -> Any:
    return load_json_strict_bytes(path.read_bytes())

def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def at(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative and not relative.startswith('/'), 'ABSOLUTE_OR_EMPTY_PATH')
    parts = Path(relative).parts
    require('..' not in parts, 'PARENT_PATH_FORBIDDEN')
    target = (root / relative).resolve()
    root_real = root.resolve()
    require(target == root_real or root_real in target.parents, 'PATH_ESCAPE')
    return target

def observe(root: Path, relative: str) -> tuple[str, str|None]:
    p = at(root, relative)
    if not p.exists():
        return 'ABSENT', None
    require(p.is_file() and not p.is_symlink(), 'NON_REGULAR_EVIDENCE:' + relative)
    return 'EXISTS', sha256(p.read_bytes())

def validate_evidence(root: Path, evidence: dict, label: str) -> None:
    actual_exists, actual_sha = observe(root, evidence['path'])
    require(evidence['existence'] == actual_exists, label + ':EXISTENCE_FALSE')
    require(evidence['observed_sha256'] == actual_sha, label + ':OBSERVED_SHA_FALSE')

def all_scalars(value: Any):
    if isinstance(value, dict):
        for child in value.values():
            yield from all_scalars(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_scalars(child)
    elif value is not None:
        yield str(value)

def contains_scalar(value: Any, needle: str) -> bool:
    return needle in set(all_scalars(value))

def requirement_matches(register: Any, requirement_id: str) -> list[dict]:
    if not isinstance(register, dict) or not isinstance(register.get('requirements'), list):
        return []
    return [x for x in register['requirements'] if isinstance(x, dict) and x.get('requirement_id') == requirement_id]

def _status_from(required_ok: bool, limited: bool=False) -> str:
    return 'VALIDATION_LIMITED' if limited else ('PASS' if required_ok else 'FAIL')

def _strict_json_or_none(root: Path, evidence: dict):
    if evidence['existence'] != 'EXISTS':
        return None
    try:
        return load_json_strict(at(root, evidence['path']))
    except Exception:
        return None

def _prior(record: dict, root: Path):
    ref = record.get('prior_record_reference')
    if ref is None:
        return None
    p = at(root, ref['repository_path'])
    require(p.is_file(), 'PRIOR_RECORD_MISSING')
    raw = p.read_bytes()
    require(sha256(raw) == ref['sha256'], 'PRIOR_RECORD_SHA_MISMATCH')
    prior = load_json_strict_bytes(raw)
    require(prior.get('artifact_type') == 'MECHANICAL_VALIDATION_RECORD', 'PRIOR_RECORD_TYPE')
    require(prior.get('case_id') == record['case_id'], 'PRIOR_RECORD_CASE')
    require(prior.get('asset_id') == record['asset_id'], 'PRIOR_RECORD_ASSET')
    require(prior.get('transaction_id') == ref['transaction_id'], 'PRIOR_RECORD_TXN')
    require(ref['case_id'] == record['case_id'] and ref['asset_id'] == record['asset_id'], 'PRIOR_REFERENCE_IDENTITY')
    require(ref['repository_path'] != canonical_record_path(record), 'PRIOR_SELF_REFERENCE')
    return prior

def canonical_record_path(record: dict) -> str:
    return f"cases/{record['case_id']}/registration-validations/{record['asset_id']}/{record['transaction_id']}.json"

def _audit_binding(record: dict, root: Path, side: Any) -> tuple[bool,bool]:
    evidence = record['image_audit_evidence']
    if evidence['existence'] == 'UNDETERMINED':
        return False, True
    if evidence['existence'] != 'EXISTS':
        return False, False

    # Preserve original strict-JSON audit semantics.
    audit_json = _strict_json_or_none(root, evidence)
    if audit_json is not None:
        base_sha = record['base_asset_evidence']['observed_sha256']
        ok = (
            contains_scalar(audit_json, record['asset_id'])
            and base_sha is not None
            and contains_scalar(audit_json, base_sha)
            and contains_scalar(audit_json, 'PASS')
        )
        return ok, False

    # Canonical FILE-0001 Formal Image Audits are Markdown.
    if side is None:
        return False, True
    try:
        text = at(root, evidence['path']).read_bytes().decode('utf-8')
    except (OSError, UnicodeDecodeError):
        return False, False

    current = text.split('```', 1)[0]

    fields = {}
    for line in current.splitlines():
        cleaned = line.strip()
        if cleaned.startswith('- '):
            cleaned = cleaned[2:].strip()
        cleaned = cleaned.replace('**', '')
        if ':' not in cleaned:
            continue
        key, value = cleaned.split(':', 1)
        fields.setdefault(key.strip(), value.strip().strip('`'))

    base_name = Path(record['base_asset_evidence']['path']).name
    base_sha = record['base_asset_evidence']['observed_sha256']
    audit_result = fields.get('Final Audit Result', fields.get('Audit Result'))

    fixity_ok = (
        evidence.get('expected_sha256') is not None
        and evidence.get('expected_sha256') == evidence.get('observed_sha256')
    )
    sidecar_ok = (
        side.get('image_audit_reference') == evidence['path']
        and side.get('image_audit_result') == 'PASS'
        and evidence.get('observed_result') == 'PASS'
    )
    identity_ok = (
        fields.get('Case ID') == record['case_id']
        and fields.get('Requirement ID') == record['requirement_id']
        and fields.get('Asset ID') == record['asset_id']
        and fields.get('Asset Version') == record['asset_version']
        and fields.get('Base Asset Filename') == base_name
        and fields.get('SHA-256') == base_sha
    )
    formal_ok = 'Formal Image Audit' in current
    pass_ok = audit_result == 'PASS'

    return (
        fixity_ok and sidecar_ok and identity_ok and formal_ok and pass_ok,
        False,
    )


def evaluate_checks(record: dict, root: Path) -> dict[str,str]:
    reg = _strict_json_or_none(root, record['register_evidence'])
    side = _strict_json_or_none(root, record['sidecar_evidence'])
    audit_ok, audit_limited = _audit_binding(record, root, side)
    result = {}

    required_evidence = [record['register_evidence'], record['base_asset_evidence'], record['sidecar_evidence'], record['image_audit_evidence']]
    missing = any(e['existence'] == 'ABSENT' for e in required_evidence)
    undetermined = any(e['existence'] == 'UNDETERMINED' for e in required_evidence)
    result['FILE_EXISTENCE'] = _status_from(not missing, undetermined)

    base_name = Path(record['base_asset_evidence']['path']).name
    side_name = Path(record['sidecar_evidence']['path']).name
    filename_ok = record['asset_id'] in base_name and record['asset_version'] in base_name and record['asset_id'] in side_name
    result['FILENAME'] = _status_from(filename_ok)

    matches = requirement_matches(reg, record['requirement_id']) if reg is not None else []
    identity_ok = len(matches) == 1 and contains_scalar(matches[0], record['asset_id']) and (not isinstance(reg, dict) or reg.get('case_id') in (None, record['case_id']))
    result['IDENTITY_UNIQUENESS'] = _status_from(identity_ok, reg is None)

    version_ok = record['asset_version'] in base_name
    version_limited = side is None
    if side is not None:
        version_ok = version_ok and contains_scalar(side, record['asset_version'])
    result['VERSION_CONSISTENCY'] = _status_from(version_ok, version_limited)

    base = record['base_asset_evidence']
    if base['expected_sha256'] is None:
        result['BYTE_IDENTITY'] = 'VALIDATION_LIMITED'
    else:
        result['BYTE_IDENTITY'] = _status_from(base['existence'] == 'EXISTS' and base['expected_sha256'] == base['observed_sha256'])

    result['SIDECAR_JSON'] = _status_from(side is not None)

    metadata_needles = (record['case_id'],record['requirement_id'],record['asset_id'],record['asset_version'],base['observed_sha256'])
    metadata_ok = side is not None and all(n is not None and contains_scalar(side, str(n)) for n in metadata_needles)
    result['REQUIRED_METADATA'] = _status_from(metadata_ok, side is None)

    result['IMAGE_AUDIT_BINDING'] = _status_from(audit_ok, audit_limited)

    management = record['management_status_observation']
    if management['source_path'] is None or management['source_sha256'] is None or management['observed_status'] is None:
        result['APPROVED_ELIGIBILITY'] = 'VALIDATION_LIMITED'
    else:
        exists, digest = observe(root, management['source_path'])
        source_value = None
        try:
            source_value = load_json_strict(at(root, management['source_path'])) if exists == 'EXISTS' else None
        except Exception:
            pass
        approved_ok = exists == 'EXISTS' and digest == management['source_sha256'] and management['observed_status'] == 'APPROVED' and source_value is not None and contains_scalar(source_value, record['asset_id']) and contains_scalar(source_value, 'APPROVED')
        result['APPROVED_ELIGIBILITY'] = _status_from(approved_ok, source_value is None)

    prior = _prior(record, root)
    preservation_ok = base['expected_sha256'] is not None and base['expected_sha256'] == base['observed_sha256']
    if prior is not None:
        preservation_ok = preservation_ok and prior['base_asset_evidence']['observed_sha256'] == base['observed_sha256']
    result['ASSET_PRESERVATION'] = _status_from(preservation_ok, base['expected_sha256'] is None)
    return result

def aggregate(checks: dict[str,str], findings: list[dict]) -> str:
    values = list(checks.values())
    if 'FAIL' in values or any(f.get('blocking') and f.get('severity') == 'ERROR' for f in findings):
        return 'FAIL'
    if 'VALIDATION_LIMITED' in values:
        return 'VALIDATION_LIMITED'
    if 'PASS_WITH_WARNINGS' in values or any(f.get('severity') == 'WARNING' for f in findings):
        return 'PASS_WITH_WARNINGS'
    return 'PASS'


def _validate_record_bytes(raw: bytes, record_relative_path: str,
                           repository_root: Path,
                           schema_path: Path|None=None) -> dict:
    record = load_json_strict_bytes(raw)
    require(list(record) == list(TOP_LEVEL), 'TOP_LEVEL_PROPERTY_ORDER')
    require(raw == canonical_bytes(record), 'NON_CANONICAL_JSON_BYTES')
    if schema_path is None:
        schema_path = repository_root / 'schemas/cases/mechanical-validation-record.schema.json'
    schema = load_json_strict(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    require(not errors, 'SCHEMA:' + '; '.join(e.message for e in errors[:5]))
    require(record['transaction_id'].startswith(record['case_id'] + '-TXN-'), 'TXN_CASE_MISMATCH')
    require(record['asset_id'].startswith(record['case_id'] + '-IMG-'), 'ASSET_CASE_MISMATCH')
    require(record_relative_path == canonical_record_path(record), 'CANONICAL_RECORD_PATH_MISMATCH')
    for key in ('register_evidence','base_asset_evidence','sidecar_evidence','image_audit_evidence'):
        validate_evidence(repository_root, record[key], key)
    for item in record['governing_references']:
        exists, digest = observe(repository_root, item['document_path'])
        require(exists == 'EXISTS' and digest == item['sha256'], 'GOVERNING_REFERENCE_MISMATCH:' + item['document_path'])
    impl = record['validator_identity']
    exists, digest = observe(repository_root, impl['implementation_path'])
    require(exists == 'EXISTS' and digest == impl['sha256'], 'VALIDATOR_IDENTITY_MISMATCH')
    require(record['runtime_identity']['python_version'] == sys.version.split()[0], 'PYTHON_RUNTIME_MISMATCH')
    libs = record['runtime_identity']['libraries']
    require([x['name'] for x in libs] == sorted(x['name'] for x in libs), 'RUNTIME_LIBRARY_ORDER')
    expected = evaluate_checks(record, repository_root)
    observed = {x['check_id']:x['result'] for x in record['checks']}
    require(list(observed) == list(CHECK_IDS), 'CHECK_ORDER_OR_SET_MISMATCH')
    require(observed == expected, 'CHECK_RESULT_FALSE:' + repr((observed, expected)))
    require(record['result'] == aggregate(expected, record['findings']), 'AGGREGATE_RESULT_FALSE')
    return record

def validate_record_bytes(raw: bytes, record_relative_path: str,
                          repository_root: Path,
                          schema_path: Path|None=None) -> dict:
    return _validate_record_bytes(raw, record_relative_path, repository_root, schema_path)

def validate_record(record_path: Path, repository_root: Path,
                    schema_path: Path|None=None) -> dict:
    return _validate_record_bytes(
        record_path.read_bytes(),
        str(record_path.relative_to(repository_root)),
        repository_root,
        schema_path,
    )


def transaction_eligible(record: dict) -> bool:
    return record['result'] in ('PASS','PASS_WITH_WARNINGS') and not any(f.get('blocking') for f in record['findings'])

def select_current_record(root: Path, case_id: str, asset_id: str) -> tuple[Path,dict]|None:
    directory = root / 'cases' / case_id / 'registration-validations' / asset_id
    if not directory.is_dir():
        return None
    candidates = []
    for p in directory.glob('*.json'):
        try:
            value = load_json_strict(p)
            if value.get('case_id') == case_id and value.get('asset_id') == asset_id and value.get('transaction_id'):
                serial = int(value['transaction_id'].rsplit('-',1)[1])
                candidates.append((serial,p,value))
        except Exception:
            continue
    if not candidates:
        return None
    _, p, value = max(candidates, key=lambda x:x[0])
    return p, value

def _walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, (list,tuple)):
        for child in value:
            yield from _walk_dicts(child)

def _extract_write_dicts(args, kwargs):
    seen = []
    for root in (args, kwargs):
        for obj in _walk_dicts(root):
            if {'target_path','operation','role'} <= set(obj):
                if id(obj) not in [id(x) for x in seen]:
                    seen.append(obj)
    return seen


def _transaction_validation_result() -> dict:
    return {
        'status': 'PASS',
        'layers': {
            'SCHEMA': 'PASS',
            'SEMANTIC': 'PASS',
            'CROSS_ARTIFACT': 'PASS',
            'GOVERNANCE': 'PASS',
        },
        'findings': [],
    }

def _write_digest(write: dict) -> str|None:
    raw = write.get('bytes')
    if isinstance(raw, (bytes, bytearray)):
        return sha256(bytes(raw))
    return write.get('prospective_sha256') or write.get('sha256')

class MechanicalTransactionValidator:
    def __init__(self, repository_root: Path, schema_path: Path|None=None):
        self.root = repository_root
        self.schema_path = schema_path or repository_root / 'schemas/cases/mechanical-validation-record.schema.json'
        self._frozen = None
        self._phase = None
        self._prospective_record_bytes = False

    def __call__(self, *args, **kwargs):
        phase = kwargs.get('phase')
        if phase is None:
            phase = next((x for x in args if isinstance(x,str) and x in ('PROSPECTIVE','POST_WRITE')), None)
        require(phase in ('PROSPECTIVE','POST_WRITE'), 'TRANSACTION_PHASE_UNRECOGNIZED')
        require(not (self._phase is None and phase == 'POST_WRITE'), 'POST_WRITE_BEFORE_PROSPECTIVE')
        require(not (self._phase == 'POST_WRITE'), 'VALIDATOR_INSTANCE_REUSED_AFTER_POST_WRITE')
        writes = _extract_write_dicts(args, kwargs)
        writes = list({(w['target_path'],w['operation'],w['role']):w for w in writes}.values())
        require(len(writes) == 2, 'MECHANICAL_TRANSACTION_EXACT_TWO_WRITES_REQUIRED')
        require(all(w['operation'] == 'CREATE' for w in writes), 'MECHANICAL_TRANSACTION_CREATE_ONLY')
        require(sorted(w['role'] for w in writes) == ['CANONICAL_TARGET','SEMANTIC_EVENT'], 'MECHANICAL_TRANSACTION_ROLE_SET')
        record_write = next(w for w in writes if w['role'] == 'CANONICAL_TARGET')
        event_write = next(w for w in writes if w['role'] == 'SEMANTIC_EVENT')
        require('/registration-validations/' in record_write['target_path'], 'MECHANICAL_RECORD_TARGET_PATH')
        require('/semantic-events/' in event_write['target_path'], 'MECHANICAL_EVENT_TARGET_PATH')
        descriptor = tuple(sorted(
            (w['target_path'],w['operation'],w['role'],_write_digest(w)) for w in writes
        ))
        if phase == 'PROSPECTIVE':
            raw = record_write.get('bytes')
            self._prospective_record_bytes = isinstance(raw, (bytes, bytearray))
            if self._prospective_record_bytes:
                value = validate_record_bytes(bytes(raw), record_write['target_path'], self.root, self.schema_path)
                require(transaction_eligible(value), 'MECHANICAL_RECORD_NOT_TRANSACTION_ELIGIBLE')
            self._frozen = descriptor
            self._phase = phase
        else:
            require(descriptor == self._frozen, 'POST_WRITE_DESCRIPTOR_MISMATCH')
            record_path = at(self.root, record_write['target_path'])
            if self._prospective_record_bytes:
                require(record_path.is_file(), 'POST_WRITE_MECHANICAL_RECORD_MISSING')
                value = validate_record(record_path, self.root, self.schema_path)
                require(transaction_eligible(value), 'MECHANICAL_RECORD_NOT_TRANSACTION_ELIGIBLE')
            elif record_path.is_file():
                value = validate_record(record_path, self.root, self.schema_path)
                require(transaction_eligible(value), 'MECHANICAL_RECORD_NOT_TRANSACTION_ELIGIBLE')
            self._phase = phase
        return _transaction_validation_result()


def mechanical_transaction_validator(repository_root: Path, schema_path: Path|None=None):
    return MechanicalTransactionValidator(repository_root, schema_path)

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--repository-root', type=Path, required=True)
    p.add_argument('--record', type=Path, required=True)
    p.add_argument('--schema', type=Path)
    p.add_argument('--format', choices=('human','json'), default='human')
    args = p.parse_args(argv)
    try:
        value = validate_record(args.record, args.repository_root, args.schema)
        report = {'validator_result':'PASS','record_result':value['result'],'closure_eligible':transaction_eligible(value),'exit_code':0}
    except Exception as exc:
        report = {'validator_result':'FAIL','error':str(exc),'exit_code':1}
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.format == 'json' else '\n'.join(f'{k}: {v}' for k,v in report.items()))
    return report['exit_code']

if __name__ == '__main__':
    raise SystemExit(main())
