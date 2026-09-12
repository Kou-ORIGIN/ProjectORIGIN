"""Executable v0.1 schemas and shared mechanical invariants (no authority grant)."""
import copy
from datetime import datetime
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from . import storage as s

U = 'urn:projectorigin:schema:operations:'
KINDS = {
    'TRANSACTION_ALLOCATION': ('transaction-allocation', 'transaction_id', 'transaction-allocations'),
    'CASE_WRITE_LEASE': ('case-write-lease', 'transaction_id', 'leases'),
    'TRANSACTION_JOURNAL': ('transaction-journal', 'transaction_id', 'journals'),
    'TRANSACTION_RECEIPT': ('transaction-receipt', 'transaction_id', 'receipts'),
    'RECOVERY_DETERMINATION': ('recovery-determination', 'recovery_determination_id', 'recovery-determinations'),
    'RECOVERY_AUTHORIZATION': ('recovery-authorization', 'recovery_authorization_id', 'recovery-authorizations'),
    'LEASE_RELEASE_RECORD': ('lease-release-record', 'transaction_id', 'lease-releases'),
    'LEASE_RELEASE_RESOLUTION': ('lease-release-resolution', 'lease_release_resolution_id', 'lease-release-resolutions'),
}
TERMINAL = {'COMMITTED', 'ABORTED', 'RECOVERY_REQUIRED'}
TRANSITIONS = {'PREPARED': {'VALIDATING', 'ABORTED', 'RECOVERY_REQUIRED'},
               'VALIDATING': TERMINAL}


def require(condition, code, detail=''):
    if not condition:
        s.reject(code, detail)


def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def record_path(value):
    kind = value['artifact_type']
    _, field, directory = KINDS[kind]
    case = value['case_id']
    if kind == 'CASE_WRITE_LEASE':
        return '.projectorigin/leases/' + case + '.json'
    return '.projectorigin/' + directory + '/' + case + '/' + value[field] + '.json'


def eligible(result):
    return (result['status'] in ('PASS', 'PASS_WITH_WARNINGS')
            and all(v == 'PASS' for v in result['layers'].values())
            and not any(f['severity'] == 'ERROR' or f['blocking'] for f in result['findings'])
            and (result['status'] == 'PASS_WITH_WARNINGS') ==
                any(f['severity'] == 'WARNING' for f in result['findings']))


class Contracts:
    def __init__(self, repository=None):
        repository = Path(repository or Path(__file__).resolve().parents[2])
        self.documents = {}
        for directory in ('operations', 'workflows'):
            for path in (repository / 'schemas' / directory).glob('*.schema.json'):
                value = s.parse_json(path.read_bytes())
                Draft202012Validator.check_schema(value)
                self.documents[value['$id']] = value
        self.registry = Registry().with_resources(
            (key, Resource.from_contents(value)) for key, value in self.documents.items())

    def resolve(self, reference):
        base, _, pointer = reference.partition('#')
        value = self.documents[base]
        for part in pointer.strip('/').split('/') if pointer else []:
            value = value[part.replace('~1', '/').replace('~0', '~')]
        value = copy.deepcopy(value)
        def absolute(node):
            if isinstance(node, dict):
                if '$ref' in node and node['$ref'].startswith('#'):
                    node['$ref'] = base + node['$ref']
                for child in node.values():
                    absolute(child)
            elif isinstance(node, list):
                for child in node:
                    absolute(child)
        absolute(value)
        if '$ref' in value:
            return self.resolve(value['$ref'])
        return value

    def definition(self, name):
        return self.resolve(U + 'operational-defs:v0.1#/$defs/' + name)

    def schema(self, value):
        require(value.get('artifact_type') in KINDS, 'SCHEMA_ARTIFACT_TYPE')
        return self.documents[U + KINDS[value['artifact_type']][0] + ':v0.1']

    def validate_definition(self, name, value):
        errors = list(Draft202012Validator(self.definition(name), registry=self.registry,
                                           format_checker=FormatChecker()).iter_errors(value))
        require(not errors, 'SCHEMA_ERROR', '; '.join(e.message for e in errors))

    def validate_event(self, value, raw=None):
        self.validate_definition('semanticEvent', value)
        require((value['authority_type'] == 'NONE') == (value['authority_reference'] is None), 'EVENT_AUTHORITY_REFERENCE_INVALID')
        before, after = value['previous_state'], value['new_state']
        if value['event_type'] in ('STATE_TRANSITION', 'IDENTITY_FIXED', 'RIGHTS_STATE_CHANGED', 'GATE_CHANGED', 'LIFECYCLE_CHANGED', 'RECORD_SUPERSEDED', 'RECORD_RETIRED', 'RECORD_VOIDED'):
            require(before is not None and after is not None and before != after, 'EVENT_STATE_DELTA_INVALID')
        if value['event_type'] == 'RECORD_CREATED':
            require(before is None and after is None, 'EVENT_STATE_DELTA_INVALID')
        if value['event_type'] == 'HUMAN_DECISION_RECORDED':
            require(value['authority_type'] == 'EXPLICIT_HUMAN_DECISION', 'EVENT_HUMAN_AUTHORITY_REQUIRED')
        if value['event_type'] == 'EVIDENCE_ATTACHED':
            require(bool(value['evidence_references']), 'EVENT_EVIDENCE_REQUIRED')
        if raw is not None:
            require(raw == s.serialize(value, self.definition('semanticEvent'), self.resolve), 'NONCANONICAL_SERIALIZATION')

    def encode(self, value):
        return s.serialize(value, self.schema(value), self.resolve)

    def validate(self, value):
        errors = list(Draft202012Validator(self.schema(value), registry=self.registry,
                                           format_checker=FormatChecker()).iter_errors(value))
        require(not errors, 'SCHEMA_ERROR', '; '.join(e.message for e in errors))
        case = value['case_id']
        def walk(node):
            if isinstance(node, dict):
                for key, child in node.items():
                    if key.endswith('_at') and isinstance(child, str):
                        try:
                            parsed = timestamp(child)
                            require(parsed.tzinfo is not None, 'SCHEMA_ERROR', key)
                        except ValueError:
                            s.reject('SCHEMA_ERROR', 'invalid timestamp: ' + key)
                    if key in ('target_path', 'lease_path', 'repository_path') or key.endswith('_ref') and isinstance(child, str):
                        s.canonical_ref(child)
                    if key != 'case_id' and key.endswith('_id') and isinstance(child, str) and child.startswith('FILE-'):
                        require(child.startswith(case + '-'), 'CROSS_CASE_IDENTITY', key)
                    walk(child)
                if 'existence' in node and 'sha256' in node:
                    exists = node['existence'] == 'EXISTS'
                    require((node['existence']=='MUST_EXIST') or (value['artifact_type']=='RECOVERY_DETERMINATION' and exists and node['sha256'] is None) or exists == (node['sha256'] is not None), 'STATE_FIXITY_INVALID')
            elif isinstance(node, list):
                for child in node:
                    walk(child)
        walk(value)
        kind = value['artifact_type']
        if kind == 'RECOVERY_DETERMINATION':
            from .recovery import validate_snapshot
            validate_snapshot(self, value)
        if kind == 'CASE_WRITE_LEASE':
            require(timestamp(value['expires_at']) > timestamp(value['acquired_at']), 'LEASE_TIME_INVALID')
        if kind == 'TRANSACTION_JOURNAL':
            require(timestamp(value['updated_at']) >= timestamp(value['created_at']), 'JOURNAL_TIME_INVALID')
            window = value['commit_window']
            require(window['entered'] == (window['entered_at'] is not None), 'COMMIT_WINDOW_INVALID')
            intent = {i['target_path']: i for i in value['write_intent']}
            pre = {p['target_path']: p for p in value['preconditions']}
            progress = {p['target_path']: p for p in value['write_progress']}
            require(len(intent) == len(value['write_intent']) and len(pre) == len(value['preconditions'])
                    and len(progress) == len(value['write_progress']) and intent.keys() == pre.keys() == progress.keys(), 'WRITE_SET_MISMATCH')
            for path, item in intent.items():
                if path.endswith('/orchestration-manifest.json'):
                    require(item['role']=='MANIFEST', 'MANIFEST_ROLE_INVALID')
                require(pre[path]['existence'] == ('MUST_NOT_EXIST' if item['operation'] == 'CREATE' else 'MUST_EXIST'), 'WRITE_PRECONDITION_INVALID')
                require(item['operation'] != 'DELETE' or item['prospective_sha256'] is None, 'WRITE_INTENT_INVALID')
                require(all(progress[path][k] == item[k] for k in ('operation', 'role')), 'WRITE_PROGRESS_MISMATCH')
            if value['state'] == 'COMMITTED':
                require(window['entered'] and all(p['progress_state'] == 'VERIFIED' for p in progress.values()), 'COMMITTED_PROGRESS_INVALID')
        if kind in ('TRANSACTION_JOURNAL', 'TRANSACTION_RECEIPT'):
            ids = [e['event_id'] for e in value['required_semantic_events']]
            require(len(ids) == len(set(ids)), 'SEMANTIC_EVENT_DUPLICATE')
            require(bool(ids) == (value['semantic_event_requirement'] == 'REQUIRED'), 'SEMANTIC_EVENT_REQUIREMENT_MISMATCH')
        if kind == 'TRANSACTION_RECEIPT':
            results = value['write_results']
            for result in results:
                if result['target_path'].endswith('/orchestration-manifest.json'):
                    require(result['role']=='MANIFEST', 'MANIFEST_ROLE_INVALID')
            require(len({r['target_path'] for r in results}) == len(results), 'WRITE_RESULT_DUPLICATE')
            if value['terminal_outcome'] == 'COMMITTED':
                require(all(eligible(v) for v in value['validation_evidence'].values()), 'COMMITTED_VALIDATION_INVALID')
                required = {e['event_id']: e for e in value['required_semantic_events']}
                emitted = value['emitted_semantic_event_refs']
                require(len(emitted) == len(required) and {e['event_id'] for e in emitted} == set(required), 'SEMANTIC_EVENT_SET_MISMATCH')
                for event in emitted:
                    require({k: event[k] for k in required[event['event_id']]} == required[event['event_id']], 'SEMANTIC_EVENT_BINDING_MISMATCH')
                for result in results:
                    op = result['operation']
                    require(result['result'] == {'CREATE':'CREATED','UPDATE':'UPDATED','DELETE':'DELETED'}[op]
                            and result['post_write_state']['existence'] == ('ABSENT' if op == 'DELETE' else 'EXISTS'), 'COMMITTED_RESULT_INVALID')
            if value['terminal_outcome'] == 'ABORTED':
                require(all(r['pre_write_state'] == r['post_write_state'] and r['result'] == 'UNCHANGED' for r in results), 'ABORTED_MUTATION_UNPROVEN')
        if kind == 'RECOVERY_AUTHORIZATION':
            require(value['authorized_by_actor_id'] == value['human_authority']['human_actor_id'], 'HUMAN_AUTHORITY_MISMATCH')
            reference = value['human_decision_reference']
            require(reference.get('repository_path') and reference.get('sha256') and reference.get('artifact_id'), 'HUMAN_AUTHORITY_EVIDENCE_REQUIRED')
        if kind in ('LEASE_RELEASE_RECORD', 'LEASE_RELEASE_RESOLUTION'):
            evidence = value['release_evidence']
            status = value.get('release_outcome', value.get('resolution_status'))
            if status in ('RELEASED', 'RESOLVED_RELEASED'):
                require(evidence['exact_instance_verified'] and evidence['safe_delete_performed'] and evidence['post_observation']['existence'] == 'ABSENT', 'RELEASE_EVIDENCE_INVALID')
            if status in ('ALREADY_ABSENT', 'RESOLVED_ABSENT'):
                require(not evidence['safe_delete_performed'] and evidence['post_observation']['existence'] == 'ABSENT', 'RELEASE_EVIDENCE_INVALID')
