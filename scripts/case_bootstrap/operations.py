"""Local operational lifecycle. Human declarations are checked, not authenticated.

Mutations are explicit API calls. Reading/inspection never allocates or repairs.
Canonical content and contextual governance validation are supplied by the
applicable production layer; no default permissive authorizer is provided.
"""
import copy
from contextlib import ExitStack
from datetime import datetime, timezone
import os
from pathlib import Path
import tempfile

from . import storage as s
from .contracts import Contracts, KINDS, TERMINAL, TRANSITIONS, eligible, record_path, require, timestamp


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def actor(prefix, identity, role):
    return {prefix + '_actor_id': identity, prefix + '_actor_role': role}


def envelope(kind, case, transaction=None):
    value = {'record_format_version': 'v0.1', 'artifact_type': kind, 'case_id': case}
    if transaction:
        value['transaction_id'] = transaction
    return value


def binding(prefix, ref):
    return {prefix + '_ref': ref['ref'], prefix + '_sha256': ref['sha256']}


def state(root, path):
    try:
        return {'existence': 'EXISTS', 'sha256': s.sha256(s.read_bytes(root, path))}
    except s.OperationalError as exc:
        if exc.code == 'REFERENCE_TARGET_MISSING':
            return {'existence': 'ABSENT', 'sha256': None}
        raise


def unavailable_result(code):
    return {'status': 'VALIDATION_LIMITED', 'layers': {k: 'VALIDATION_LIMITED' for k in
            ('SCHEMA', 'SEMANTIC', 'CROSS_ARTIFACT', 'GOVERNANCE')},
            'findings': [{'code': code, 'severity': 'ERROR', 'blocking': True,
                          'message': 'Required validation was not completed.'}]}


class Operations:
    def __init__(self, root, contracts=None, checkpoint=None, contextual_validator=None):
        self.root = Path(root).resolve(strict=True)
        self.contracts = contracts or Contracts()
        self.checkpoint = checkpoint or (lambda phase: None)
        self.contextual_validator = contextual_validator

    def metadata(self, value):
        path = record_path(value)
        data = s.read_bytes(self.root, path)
        return {'ref': path, 'sha256': s.sha256(data), 'byte_size': len(data)}

    def read(self, ref, expected=None):
        data = s.read_bytes(self.root, ref)
        if expected is not None:
            require(s.sha256(data) == expected, 'REFERENCE_FIXITY_MISMATCH', ref)
        value = s.parse_json(data)
        self.contracts.validate(value)
        require(record_path(value) == ref, 'ARTIFACT_PATH_IDENTITY_MISMATCH', ref)
        require(self.contracts.encode(value) == data, 'NONCANONICAL_SERIALIZATION', ref)
        return value

    def linked(self, value, prefix, kind, transaction_field='transaction_id'):
        target = self.read(value[prefix + '_ref'], value[prefix + '_sha256'])
        require(target['artifact_type'] == kind and target['case_id'] == value['case_id'], 'CROSS_ARTIFACT_IDENTITY_MISMATCH', prefix)
        if transaction_field:
            require(target['transaction_id'] == value[transaction_field], 'CROSS_ARTIFACT_IDENTITY_MISMATCH', prefix)
        return target

    def records(self, kind, case):
        s.validate_case(case)
        directory = '.projectorigin/' + KINDS[kind][2] + '/' + case
        path = s.path_at(self.root, directory)
        if not path.exists():
            return []
        return [self.read(p.relative_to(self.root).as_posix()) for p in sorted(path.glob('*.json'))]

    def next_id(self, kind, case, namespace):
        field = KINDS[kind][1]
        records = self.records(kind, case)
        ids = [r[field] for r in records]
        require(len(set(ids)) == len(ids), 'OPERATIONAL_ID_COLLISION')
        serial = max([int(i.rsplit('-', 1)[1]) for i in ids] or [0]) + 1
        require(serial <= 9999, 'OPERATIONAL_ID_NAMESPACE_EXHAUSTED')
        return case + '-' + namespace + '-' + str(serial).zfill(4)

    def check_recovery(self, case, context, fresh=False):
        try:
            rdet = self.read(context['recovery_determination_ref'], context['recovery_determination_sha256'])
            rauth = self.read(context['recovery_authorization_ref'], context['recovery_authorization_sha256'])
            require(rdet['artifact_type'] == 'RECOVERY_DETERMINATION' and rauth['artifact_type'] == 'RECOVERY_AUTHORIZATION', 'RECOVERY_PROVENANCE_MISMATCH')
            require(rdet['case_id'] == rauth['case_id'] == case and rdet['prior_transaction_id'] == rauth['prior_transaction_id'] == context['prior_transaction_id'], 'RECOVERY_PROVENANCE_MISMATCH')
            require(rdet['determination'] == 'SAFE_TO_START_NEW_TXN' and rauth['authorization'] == 'AUTHORIZED', 'RECOVERY_PROVENANCE_MISMATCH')
            require(all(rauth[k] == context[k] for k in ('recovery_determination_ref', 'recovery_determination_sha256')), 'RECOVERY_PROVENANCE_MISMATCH')
            self.check_links(rauth)
            if fresh:
                for successor in self.records('RECOVERY_DETERMINATION', case):
                    if successor.get('supersedes', {}).get('repository_path') == context['recovery_determination_ref']:
                        require(False, 'RECOVERY_DETERMINATION_SUPERSEDED')
                inspection = self.inspect(case, context['prior_transaction_id'], rdet['evidence']['inspected_by_actor_id'], rdet['evidence']['inspected_by_actor_role'])
                require(inspection['determination'] == 'SAFE_TO_START_NEW_TXN' and self.snapshot(inspection['evidence']) == self.snapshot(rdet['evidence']), 'RECOVERY_STATE_CHANGED')
            return rdet, rauth
        except (KeyError, TypeError):
            s.reject('RECOVERY_PROVENANCE_MISMATCH')

    def check_links(self, value):
        kind, case = value['artifact_type'], value['case_id']
        if kind == 'TRANSACTION_ALLOCATION' and value['transaction_origin'] == 'RECOVERY_CONTINUATION':
            self.check_recovery(case, value['recovery_context'])
            require(value['transaction_id'] != value['recovery_context']['prior_transaction_id'], 'RECOVERY_PROVENANCE_MISMATCH')
        if kind == 'CASE_WRITE_LEASE':
            allocation = self.linked(value, 'allocation_record', 'TRANSACTION_ALLOCATION')
            require((value['holder_actor_id'], value['holder_actor_role']) == (allocation['allocated_by_actor_id'], allocation['allocated_by_actor_role']), 'ACTOR_BINDING_MISMATCH')
        if kind in ('TRANSACTION_JOURNAL', 'TRANSACTION_RECEIPT'):
            lease = value['lease_binding' if kind == 'TRANSACTION_JOURNAL' else 'lease_evidence']
            allocation = self.read(lease['allocation_record_ref'], lease['allocation_record_sha256'])
            require(allocation['artifact_type'] == 'TRANSACTION_ALLOCATION', 'ALLOCATION_BINDING_MISMATCH')
            require(all(value[k] == allocation[k] for k in ('case_id', 'transaction_id')), 'ALLOCATION_BINDING_MISMATCH')
            require((value['initiated_by_actor_id'], value['initiated_by_actor_role']) == (allocation['allocated_by_actor_id'], allocation['allocated_by_actor_role']), 'ACTOR_BINDING_MISMATCH')
            require(lease['lease_path'] == '.projectorigin/leases/' + case + '.json', 'LEASE_BINDING_MISMATCH')
            if kind == 'TRANSACTION_JOURNAL':
                current_path = s.path_at(self.root, lease['lease_path'])
                if current_path.exists():
                    current_lease = self.read(lease['lease_path'])
                    if current_lease['transaction_id'] == value['transaction_id']:
                        require(self.metadata(current_lease)['sha256'] == lease['lease_sha256'], 'LEASE_BINDING_MISMATCH')
                        require(all(current_lease[k] == lease[k] for k in ('allocation_record_ref','allocation_record_sha256','acquired_at','expires_at')), 'LEASE_BINDING_MISMATCH')
                require(value.get('recovery_context') == allocation.get('recovery_context'), 'RECOVERY_PROVENANCE_MISMATCH')
            else:
                require((lease['holder_actor_id'], lease['holder_actor_role']) == (value['initiated_by_actor_id'], value['initiated_by_actor_role']), 'ACTOR_BINDING_MISMATCH')
                journal_path = '.projectorigin/journals/' + case + '/' + value['transaction_id'] + '.json'
                if s.path_at(self.root, journal_path).exists():
                    journal = self.read(journal_path)
                    require(journal['state'] == value['terminal_outcome'], 'RECEIPT_JOURNAL_MISMATCH')
                    require(journal['required_semantic_events'] == value['required_semantic_events'], 'SEMANTIC_EVENT_SET_MISMATCH')
                    require(journal['lease_binding'] == {k: lease[k] for k in journal['lease_binding']}, 'LEASE_BINDING_MISMATCH')
                    require({i['target_path'] for i in journal['write_intent']} == {r['target_path'] for r in value['write_results']}, 'WRITE_SET_MISMATCH')
                for event in value['emitted_semantic_event_refs']:
                    ref = 'cases/' + case + '/semantic-events/' + event['event_id'] + '.json'
                    content = s.read_ref(self.root, ref, event['event_sha256'], {'event_id': event['event_id']})
                    require(all(content[k] == event[k] for k in ('event_type', 'record_ref')), 'SEMANTIC_EVENT_BINDING_MISMATCH')
        if kind == 'RECOVERY_DETERMINATION':
            evidence = value['evidence']
            # Historical Journal/Receipt snapshots are validated internally, not
            # rebound to mutable current Journal bytes. Durable anchors remain fixed.
            if evidence['allocation_observation']['validation'] == 'VALID':
                self.linked(dict(evidence, case_id=case, prior_transaction_id=value['prior_transaction_id']), 'allocation_record', 'TRANSACTION_ALLOCATION', 'prior_transaction_id')
            observed_lease=evidence['lease_observation']
            if observed_lease['validation']=='VALID':
                self.check_links(observed_lease['data'])
            observed_receipt=evidence['receipt_observation']
            if observed_receipt['validation']=='VALID':
                self.read(observed_receipt['target_path'],observed_receipt['state']['sha256'])
            for reference in evidence['prior_determination_references']:
                previous = self.read(reference['repository_path'], reference['sha256'])
                require(previous['artifact_type'] == kind and previous['case_id'] == case and previous['prior_transaction_id'] == value['prior_transaction_id'] and previous['recovery_determination_id'] == reference['artifact_id'], 'RECOVERY_PROVENANCE_MISMATCH')
            if 'supersedes' in value:
                target = value['supersedes']
                previous = self.read(target['repository_path'], target['sha256'])
                require(previous['artifact_type'] == kind and previous['case_id'] == case and previous['prior_transaction_id'] == value['prior_transaction_id'] and previous['recovery_determination_id'] != value['recovery_determination_id'], 'RDET_SUPERSESSION_INVALID')
        if kind == 'RECOVERY_AUTHORIZATION':
            rdet = self.linked(value, 'recovery_determination', 'RECOVERY_DETERMINATION', None)
            require(rdet['prior_transaction_id'] == value['prior_transaction_id'], 'RECOVERY_PROVENANCE_MISMATCH')
            if value['authorization'] == 'AUTHORIZED':
                require(rdet['determination'] == 'SAFE_TO_START_NEW_TXN', 'RECOVERY_PROVENANCE_MISMATCH')
            require(timestamp(value['authorized_at']) >= timestamp(rdet['determined_at']), 'AUTHORIZATION_TIME_INVALID')
            reference = value['human_decision_reference']
            # This verifies the supplied declaration/evidence, never authenticates
            # its author or interprets an arbitrary document as consent.
            require(s.sha256(s.read_bytes(self.root, reference['repository_path'])) == reference['sha256'], 'REFERENCE_FIXITY_MISMATCH')
        if kind == 'LEASE_RELEASE_RECORD':
            receipt = self.linked(value, 'receipt', 'TRANSACTION_RECEIPT')
            require(value['expected_lease'] == receipt['lease_evidence'], 'LEASE_BINDING_MISMATCH')
        if kind == 'LEASE_RELEASE_RESOLUTION':
            root = self.linked(value, 'lease_release_record', 'LEASE_RELEASE_RECORD')
            predecessor = self.read(value['predecessor_ref'], value['predecessor_sha256'])
            require(predecessor['artifact_type'] in ('LEASE_RELEASE_RECORD', kind) and predecessor['case_id'] == case and predecessor['transaction_id'] == value['transaction_id'], 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID')
            if predecessor['artifact_type'] == 'LEASE_RELEASE_RECORD':
                require(record_path(predecessor) == record_path(root), 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID')
            else:
                require(predecessor['lease_release_record_ref'] == value['lease_release_record_ref'], 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID')

    def publish(self, value):
        self.contracts.validate(value)
        self.check_links(value)
        _, field, _ = KINDS[value['artifact_type']]
        return s.immutable_publish(self.root, record_path(value), value,
                                  validate=self.contracts.validate, encode=self.contracts.encode,
                                  identity={field: value[field], 'case_id': value['case_id'], 'artifact_type': value['artifact_type']},
                                  checkpoint=self.checkpoint)

    def allocate(self, case, identity, role, recovery_context=None):
        self.contracts.validate_definition('operationalActorId', identity)
        self.contracts.validate_definition('operationalActorRole', role)
        with s.namespace_lock(self.root, case, 'TXN'), ExitStack() as guards:
            if recovery_context is not None:
                guards.enter_context(s.namespace_lock(self.root, case, 'RDET'))
                guards.enter_context(s.lease_slot_lock(self.root, case, 'RECOVERY_SERIALIZATION_UNAVAILABLE'))
            transaction = self.next_id('TRANSACTION_ALLOCATION', case, 'TXN')
            if recovery_context is not None:
                self.check_recovery(case, recovery_context, fresh=True)
                require(not any(a.get('recovery_context', {}).get('recovery_authorization_ref') == recovery_context['recovery_authorization_ref'] for a in self.records('TRANSACTION_ALLOCATION', case)), 'RECOVERY_AUTHORIZATION_ALREADY_CONSUMED')
            value = {**envelope('TRANSACTION_ALLOCATION', case, transaction), **actor('allocated_by', identity, role),
                     'allocated_at': now(), 'transaction_origin': 'RECOVERY_CONTINUATION' if recovery_context else 'NORMAL'}
            if recovery_context is not None:
                value['recovery_context'] = copy.deepcopy(recovery_context)
            try:
                self.publish(value)
            except s.OperationalError as exc:
                if 'COLLISION' in exc.code or exc.code == 'ARTIFACT_FINAL_PATH_ALREADY_EXISTS':
                    s.reject('TRANSACTION_ALLOCATION_COLLISION', exc)
                raise
        return value

    def acquire(self, allocation, expires_at):
        canonical = self.read(record_path(allocation))
        require(canonical == allocation, 'ALLOCATION_BINDING_MISMATCH')
        case = allocation['case_id']
        value = {**envelope('CASE_WRITE_LEASE', case, allocation['transaction_id']),
                 **binding('allocation_record', self.metadata(allocation)),
                 **actor('holder', allocation['allocated_by_actor_id'], allocation['allocated_by_actor_role']),
                 'acquired_at': now(), 'expires_at': expires_at}
        self.contracts.validate(value)
        with s.lease_slot_lock(self.root, case, 'LEASE_ATOMIC_ACQUISITION_UNAVAILABLE'):
            require(not s.path_at(self.root, record_path(value)).exists(), 'CASE_WRITE_LEASE_CONFLICT')
            try:
                self.publish(value)
            except s.OperationalError as exc:
                if exc.code == 'IMMUTABLE_ARTIFACT_ATOMIC_PUBLICATION_UNAVAILABLE':
                    s.reject('LEASE_ATOMIC_ACQUISITION_UNAVAILABLE', exc)
                raise
            require(self.read(record_path(value)) == value, 'LEASE_ACQUISITION_OUTCOME_AMBIGUOUS')
        return value

    def lease_evidence(self, lease):
        result = {'lease_path': record_path(lease), 'lease_sha256': self.metadata(lease)['sha256']}
        result.update({k: lease[k] for k in ('allocation_record_ref', 'allocation_record_sha256', 'holder_actor_id', 'holder_actor_role', 'acquired_at', 'expires_at')})
        return result

    def owned(self, lease):
        current = self.read(record_path(lease))
        require(current == lease and self.contracts.encode(lease) == s.read_bytes(self.root, record_path(lease)), 'LEASE_RELEASE_OWNERSHIP_MISMATCH')

    def replace_mutable(self, ref, data, expected):
        require(state(self.root, ref) == expected, 'STALE_WRITE_CONFLICT', ref)
        path = s.ensure_parent(self.root, ref)
        fd, staging = tempfile.mkstemp(prefix='.materialize-', suffix='.tmp', dir=path.parent)
        try:
            with os.fdopen(fd, 'w+b') as stream:
                stream.write(data); stream.flush(); stream.seek(0)
                require(stream.read() == data, 'STAGING_FIXITY_MISMATCH')
                s.file_barrier(stream.fileno())
            require(state(self.root, ref) == expected, 'STALE_WRITE_CONFLICT', ref)
            if expected['existence'] == 'ABSENT':
                os.link(staging, path)
            else:
                os.replace(staging, path)
            s.directory_barrier(path.parent)
            require(s.read_bytes(self.root, ref) == data, 'MATERIALIZATION_FIXITY_MISMATCH')
        finally:
            try:
                os.unlink(staging)
            except FileNotFoundError:
                pass

    def write_journal(self, journal, previous=None):
        self.contracts.validate(journal)
        self.check_links(journal)
        ref = record_path(journal)
        if previous is None:
            require(journal['state'] == 'PREPARED', 'JOURNAL_TRANSITION_INVALID')
            lease = self.read(journal['lease_binding']['lease_path'], journal['lease_binding']['lease_sha256'])
            require(lease['transaction_id'] == journal['transaction_id'], 'LEASE_BINDING_MISMATCH')
            expected = {'existence': 'ABSENT', 'sha256': None}
        else:
            current = self.read(ref)
            require(current == previous, 'STALE_WRITE_CONFLICT')
            require(previous['state'] not in TERMINAL, 'JOURNAL_TERMINAL_IMMUTABLE')
            require(journal['state'] == previous['state'] or journal['state'] in TRANSITIONS[previous['state']], 'JOURNAL_TRANSITION_INVALID')
            for key in previous:
                if key not in ('state', 'updated_at', 'commit_window', 'write_progress'):
                    require(journal.get(key) == previous[key], 'JOURNAL_IMMUTABLE_FIELD', key)
            expected = state(self.root, ref)
        self.replace_mutable(ref, self.contracts.encode(journal), expected)

    def safe_release(self, receipt):
        self.contracts.validate(receipt); self.check_links(receipt)
        require(self.read(record_path(receipt)) == receipt, 'RECEIPT_FIXITY_MISMATCH')
        expected = receipt['lease_evidence']; case = receipt['case_id']
        observed = {'existence': 'UNDETERMINED', 'sha256': None}
        evidence = {'observed_at': now(), 'exact_instance_verified': False,
                    'safe_delete_performed': False, 'post_observation': observed, 'finding_code': None}
        outcome = 'FAILED'
        try:
            with s.lease_slot_lock(self.root, case, 'LEASE_SAFE_RELEASE_UNAVAILABLE'):
                observed = state(self.root, expected['lease_path'])
                evidence['post_observation'] = observed
                if observed['existence'] == 'ABSENT':
                    evidence['finding_code'] = 'LEASE_RELEASE_ALREADY_ABSENT'
                    return 'ALREADY_ABSENT', evidence
                if observed['sha256'] != expected['lease_sha256']:
                    evidence['finding_code'] = 'LEASE_RELEASE_OWNERSHIP_MISMATCH'
                    return 'OWNERSHIP_MISMATCH', evidence
                lease = self.read(expected['lease_path'], expected['lease_sha256'])
                require(lease['case_id'] == case and lease['transaction_id'] == receipt['transaction_id'] and all(lease[k] == expected[k] for k in ('holder_actor_id', 'holder_actor_role', 'allocation_record_ref', 'allocation_record_sha256', 'acquired_at', 'expires_at')), 'LEASE_RELEASE_OWNERSHIP_MISMATCH')
                path = s.path_at(self.root, expected['lease_path']); before = path.lstat()
                evidence['exact_instance_verified'] = True
                self.checkpoint('before_release_compare')
                current = path.lstat()
                require((before.st_dev, before.st_ino) == (current.st_dev, current.st_ino) and state(self.root, expected['lease_path']) == observed, 'LEASE_RELEASE_OWNERSHIP_MISMATCH')
                self.checkpoint('before_release_unlink')
                os.unlink(path)
                evidence['safe_delete_performed'] = True
                self.checkpoint('after_release_unlink')
                s.directory_barrier(path.parent)
                evidence['post_observation'] = state(self.root, expected['lease_path'])
                require(evidence['post_observation']['existence'] == 'ABSENT', 'LEASE_RELEASE_OUTCOME_AMBIGUOUS')
                return 'RELEASED', evidence
        except (s.OperationalError, OSError) as exc:
            code = getattr(exc, 'code', 'LEASE_RELEASE_IO_FAILURE')
            if evidence['safe_delete_performed']:
                code = 'LEASE_RELEASE_OUTCOME_AMBIGUOUS'
                outcome = 'AMBIGUOUS'
                evidence['post_observation'] = {'existence': 'UNDETERMINED', 'sha256': None}
            elif code == 'LEASE_RELEASE_OWNERSHIP_MISMATCH':
                outcome = 'OWNERSHIP_MISMATCH'
            evidence['finding_code'] = code
            return outcome, evidence

    def release(self, receipt, identity, role):
        ref = '.projectorigin/lease-releases/' + receipt['case_id'] + '/' + receipt['transaction_id'] + '.json'
        require(not s.path_at(self.root, ref).exists(), 'ARTIFACT_FINAL_PATH_ALREADY_EXISTS')
        outcome, evidence = self.safe_release(receipt)
        value = {**envelope('LEASE_RELEASE_RECORD', receipt['case_id'], receipt['transaction_id']),
                 **binding('receipt', self.metadata(receipt)), 'expected_lease': receipt['lease_evidence'],
                 'release_outcome': outcome, **actor('release_attempted_by', identity, role), 'release_evidence': evidence}
        self.publish(value)
        return value

    def chain(self, lrel):
        self.check_links(lrel)
        root = record_path(lrel)
        nodes = [r for r in self.records('LEASE_RELEASE_RESOLUTION', lrel['case_id']) if r['transaction_id'] == lrel['transaction_id']]
        successors = {}
        for node in nodes:
            self.check_links(node)
            require(node['lease_release_record_ref'] == root and node['lease_release_record_sha256'] == self.metadata(lrel)['sha256'], 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID')
            predecessor = node['predecessor_ref']
            require(predecessor not in successors, 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID', 'branch')
            successors[predecessor] = node
        tip = lrel; seen = {root}
        while record_path(tip) in successors:
            require(tip.get('resolution_status') != 'RESOLVED_RELEASED', 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID', 'successor of terminal')
            tip = successors[record_path(tip)]
            require(record_path(tip) not in seen, 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID', 'cycle')
            seen.add(record_path(tip))
        require(len(seen) == len(nodes) + 1, 'LEASE_RELEASE_RESOLUTION_CHAIN_INVALID', 'disconnected/cyclic chain')
        return tip

    def resolve_release(self, lrel, predecessor_ref, identity, role, retry=False):
        case, transaction = lrel['case_id'], lrel['transaction_id']
        with s.resolution_lock(self.root, case, transaction):
            lrel = self.read(record_path(lrel))
            tip = self.chain(lrel)
            require(record_path(tip) == predecessor_ref and tip.get('resolution_status') != 'RESOLVED_RELEASED', 'LEASE_RELEASE_RESOLUTION_SUCCESSOR_CONFLICT')
            receipt = self.read(lrel['receipt_ref'], lrel['receipt_sha256'])
            if retry:
                outcome, evidence = self.safe_release(receipt)
                status = {'RELEASED':'RESOLVED_RELEASED','ALREADY_ABSENT':'RESOLVED_ABSENT','OWNERSHIP_MISMATCH':'FOREIGN_OR_REPLACEMENT_LEASE','FAILED':'UNDETERMINED','AMBIGUOUS':'UNDETERMINED'}[outcome]
            else:
                observed = state(self.root, lrel['expected_lease']['lease_path'])
                status = 'RESOLVED_ABSENT' if observed['existence'] == 'ABSENT' else ('STILL_PRESENT' if observed['sha256'] == lrel['expected_lease']['lease_sha256'] else 'FOREIGN_OR_REPLACEMENT_LEASE')
                evidence = {'observed_at':now(),'exact_instance_verified':False,'safe_delete_performed':False,'post_observation':observed,'finding_code':None}
            with s.namespace_lock(self.root, case, 'LRRES'):
                value = {**envelope('LEASE_RELEASE_RESOLUTION', case, transaction),
                         'lease_release_resolution_id':self.next_id('LEASE_RELEASE_RESOLUTION', case, 'LRRES'),
                         **binding('lease_release_record', self.metadata(lrel)), **binding('predecessor', self.metadata(tip)),
                         'resolution_status':status, **actor('observed_by', identity, role),'release_evidence':evidence}
                self.publish(value)
        return value

    @staticmethod
    def snapshot(evidence):
        return {k:v for k,v in evidence.items() if k not in ('inspected_at','inspected_by_actor_id','inspected_by_actor_role','prior_determination_references')}

    def inspect(self, case, transaction, identity, role):
        from .recovery import inspect
        return inspect(self, case, transaction, identity, role)

    def determine(self, case, transaction, identity, role, rationale, supersedes=None):
        with s.namespace_lock(self.root,case,'RDET'):
            inspection = self.inspect(case,transaction,identity,role)
            value = {**envelope('RECOVERY_DETERMINATION',case),'recovery_determination_id':self.next_id('RECOVERY_DETERMINATION',case,'RDET'),
                     'prior_transaction_id':transaction,**inspection,**actor('determined_by',identity,role),'determined_at':now(),'rationale':rationale}
            if supersedes is not None:
                value['supersedes']=supersedes
            self.publish(value)
        return value

    def record_authorization(self, declaration):
        """Finalize an explicitly supplied Human declaration; no default decision.

        Caller supplies authorization, Human declaration, actor, time, rationale,
        RDET binding, and fixed durable decision evidence. This method only adds
        the serialized operational identity. It never authenticates the Human.
        """
        value=copy.deepcopy(declaration)
        case=value['case_id']
        with s.namespace_lock(self.root,case,'RAUTH'):
            require('recovery_authorization_id' not in value, 'OPERATIONAL_ID_ASSIGNED_BY_ALLOCATOR')
            value['recovery_authorization_id']=self.next_id('RECOVERY_AUTHORIZATION',case,'RAUTH')
            self.publish(value)
        return value

    def execute(self, allocation, lease, writes, required_events, validator):
        """Execute a governed write set under an already allocated/held Lease.

        Each write has target_path, operation, role, and bytes (None for DELETE).
        validator(phase, writes) must perform applicable schema, semantic,
        cross-artifact AND governance checks and return a validationResult.
        No validator, inferred authorization, or permissive fallback is supplied.
        """
        require(callable(validator), 'GOVERNANCE_VALIDATOR_REQUIRED')
        self.owned(lease)
        self.check_links(lease)
        require(all(allocation[k] == lease[k] for k in ('case_id','transaction_id')), 'ALLOCATION_BINDING_MISMATCH')
        case, transaction = allocation['case_id'], allocation['transaction_id']
        writes = copy.deepcopy(writes)
        require(writes and len({w['target_path'] for w in writes}) == len(writes), 'WRITE_SET_INVALID')
        require(sum(w['role']=='MANIFEST' for w in writes) <= 1, 'MANIFEST_SET_INVALID')
        for write in writes:
            s.canonical_ref(write['target_path'])
            require(write['target_path'].startswith('cases/'+case+'/'), 'CANONICAL_WRITE_SCOPE_INVALID')
            require(write['operation'] in ('CREATE','UPDATE','DELETE') and write['role'] in ('CANONICAL_TARGET','SEMANTIC_EVENT','MANIFEST'), 'WRITE_INTENT_INVALID')
            require((write['operation']=='DELETE' and write['bytes'] is None) or (write['operation']!='DELETE' and isinstance(write['bytes'],bytes)), 'WRITE_BYTES_INVALID')
            if write['target_path'].endswith('/orchestration-manifest.json'):
                require(write['role']=='MANIFEST', 'MANIFEST_ROLE_INVALID')
            if '/semantic-events/' in write['target_path']:
                require(write['role']=='SEMANTIC_EVENT' and write['operation']=='CREATE', 'SEMANTIC_EVENT_IMMUTABLE')
            if write['role']=='SEMANTIC_EVENT':
                require(write['operation']=='CREATE', 'SEMANTIC_EVENT_IMMUTABLE')
        before = {w['target_path']:state(self.root,w['target_path']) for w in writes}
        stamp=now(); evidence=self.lease_evidence(lease)
        journal={**envelope('TRANSACTION_JOURNAL',case,transaction),'state':'PREPARED',
                 **actor('initiated_by',allocation['allocated_by_actor_id'],allocation['allocated_by_actor_role']),
                 'created_at':stamp,'updated_at':stamp,
                 'write_intent':[{k:w[k] for k in ('target_path','operation','role')} | {'prospective_sha256':s.sha256(w['bytes']) if w['bytes'] is not None else None} for w in writes],
                 'preconditions':[{'target_path':w['target_path'],'existence':'MUST_NOT_EXIST' if w['operation']=='CREATE' else 'MUST_EXIST','sha256':None if w['operation']=='CREATE' else before[w['target_path']]['sha256']} for w in writes],
                 'lease_binding':{k:v for k,v in evidence.items() if k not in ('holder_actor_id','holder_actor_role')},
                 'semantic_event_requirement':'REQUIRED' if required_events else 'NOT_REQUIRED',
                 'required_semantic_events':copy.deepcopy(required_events),
                 'commit_window':{'entered':False,'entered_at':None},
                 'write_progress':[{**{k:w[k] for k in ('target_path','operation','role')},'progress_state':'NOT_STARTED','last_observed_at':stamp} for w in writes]}
        if 'recovery_context' in allocation:
            journal['recovery_context']=copy.deepcopy(allocation['recovery_context'])
        self.write_journal(journal)
        prospective=unavailable_result('PROSPECTIVE_NOT_COMPLETED')
        post=unavailable_result('POST_WRITE_NOT_COMPLETED')
        emitted=[]; problem=None
        def update(**changes):
            nonlocal journal
            next_journal=copy.deepcopy(journal)
            next_journal.update(copy.deepcopy(changes)); next_journal['updated_at']=now()
            self.write_journal(next_journal,journal)
            journal=next_journal
        try:
            self.checkpoint('prepared_before_preconditions')
            for w in writes:
                require(before[w['target_path']]['existence'] == ('ABSENT' if w['operation']=='CREATE' else 'EXISTS') and state(self.root,w['target_path']) == before[w['target_path']], 'STALE_WRITE_CONFLICT')
            events={e['event_id']:e for e in required_events}
            materialized_events={}
            for w in writes:
                if w['role']=='SEMANTIC_EVENT':
                    event=s.parse_json(w['bytes'])
                    self.contracts.validate_event(event,w['bytes'])
                    require(event['event_id'] in events and w['target_path']=='cases/'+case+'/semantic-events/'+event['event_id']+'.json', 'SEMANTIC_EVENT_SET_MISMATCH')
                    require(all(event[k]==events[event['event_id']][k] for k in ('event_type','record_ref')), 'SEMANTIC_EVENT_BINDING_MISMATCH')
                    materialized_events[event['event_id']]=event
            require(materialized_events.keys()==events.keys(), 'SEMANTIC_EVENT_SET_MISMATCH')
            update(state='VALIDATING')
            prospective=validator('PROSPECTIVE',copy.deepcopy(writes))
            self.contracts.validate_definition('validationResult',prospective)
            require(eligible(prospective),'PROSPECTIVE_VALIDATION_FAILED')
            self.checkpoint('before_commit_recheck')
            self.owned(lease)
            require(all(state(self.root,p)==old for p,old in before.items()), 'STALE_WRITE_CONFLICT')
            update(commit_window={'entered':True,'entered_at':now()})
            for write in sorted(writes,key=lambda w:('CANONICAL_TARGET','SEMANTIC_EVENT','MANIFEST').index(w['role'])):
                path=write['target_path']; self.checkpoint('before_target:'+path)
                self.owned(lease)
                require(state(self.root,path)==before[path],'STALE_WRITE_CONFLICT',path)
                if write['operation']=='DELETE':
                    os.unlink(s.path_at(self.root,path)); s.directory_barrier(s.path_at(self.root,path).parent)
                else:
                    self.replace_mutable(path,write['bytes'],before[path])
                progress=copy.deepcopy(journal['write_progress'])
                next(p for p in progress if p['target_path']==path).update(progress_state='MATERIALIZED',last_observed_at=now())
                update(write_progress=progress)
                expected={'existence':'ABSENT' if write['operation']=='DELETE' else 'EXISTS','sha256':None if write['bytes'] is None else s.sha256(write['bytes'])}
                require(state(self.root,path)==expected,'POST_WRITE_FIXITY_MISMATCH')
                next(p for p in progress if p['target_path']==path).update(progress_state='VERIFIED',last_observed_at=now())
                update(write_progress=progress)
                if write['role']=='SEMANTIC_EVENT':
                    event=s.parse_json(write['bytes'])
                    emitted.append({**events[event['event_id']],'event_sha256':expected['sha256']})
            post=validator('POST_WRITE',copy.deepcopy(writes))
            self.contracts.validate_definition('validationResult',post)
            require(eligible(post),'POST_WRITE_VALIDATION_FAILED')
            for w in writes:
                require(state(self.root,w['target_path']) == {'existence':'ABSENT' if w['operation']=='DELETE' else 'EXISTS','sha256':None if w['bytes'] is None else s.sha256(w['bytes'])},'POST_WRITE_FIXITY_MISMATCH')
            outcome='COMMITTED'
        except (s.OperationalError,OSError,ValueError,KeyError,TypeError) as exc:
            problem=getattr(exc,'code',type(exc).__name__)
            try:
                unchanged=all(state(self.root,p)==old for p,old in before.items())
            except (s.OperationalError,OSError):
                unchanged=False
            outcome='ABORTED' if unchanged else 'RECOVERY_REQUIRED'
        results=[]
        for write in writes:
            path=write['target_path']
            try:
                after=state(self.root,path)
            except (s.OperationalError,OSError):
                after={'existence':'UNDETERMINED','sha256':None}
            result='UNCHANGED' if after==before[path] else ('UNDETERMINED' if outcome!='COMMITTED' else {'CREATE':'CREATED','UPDATE':'UPDATED','DELETE':'DELETED'}[write['operation']])
            results.append({'target_path':path,'operation':write['operation'],'role':write['role'],'pre_write_state':before[path],'post_write_state':after,'result':result})
        update(state=outcome)
        receipt={**envelope('TRANSACTION_RECEIPT',case,transaction),'terminal_outcome':outcome,
                 **actor('initiated_by',allocation['allocated_by_actor_id'],allocation['allocated_by_actor_role']),
                 **actor('recorded_by',allocation['allocated_by_actor_id'],allocation['allocated_by_actor_role']),
                 'terminal_at':journal['updated_at'],'receipt_created_at':now(),'lease_evidence':evidence,
                 'write_results':results,'validation_evidence':{'prospective_validation':prospective,'post_write_verification':post},
                 'semantic_event_requirement':journal['semantic_event_requirement'],'required_semantic_events':required_events,'emitted_semantic_event_refs':emitted}
        self.publish(receipt)
        release=self.release(receipt,allocation['allocated_by_actor_id'],allocation['allocated_by_actor_role'])
        return {'receipt':receipt,'lease_release_record':release,'failure_code':problem}
