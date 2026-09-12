"""Local POSIX storage primitives for Decisions 113–122.

All writers must use this protocol. The repository and its parent directories
must be controlled by the operator; hostile directory replacement is outside
this local cooperating-process protocol. No network-filesystem guarantees are
inferred. Lock files are persistent rendezvous points, never unlinked on release.
"""

import contextlib
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


class OperationalError(Exception):
    def __init__(self, code, detail=""):
        self.code = code
        self.detail = str(detail)
        super().__init__(code + (": " + self.detail if detail else ""))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def reject(code, detail=""):
    raise OperationalError(code, detail)


def canonical_ref(value):
    if (not isinstance(value, str) or not value or value.startswith("/")
            or "\\" in value or "\x00" in value
            or any(part in ("", ".", "..") for part in value.split("/"))
            or re.match(r"^[A-Za-z]:", value)):
        reject("REFERENCE_PATH_INVALID", repr(value))
    return value


def path_at(root, ref):
    """Resolve a canonical relative name, conservatively rejecting symlinks."""
    canonical_ref(ref)
    root = Path(root).resolve(strict=True)
    path = root
    for part in ref.split("/"):
        path = path / part
        if path.is_symlink():
            reject("REFERENCE_SYMLINK_UNSUPPORTED", ref)
    try:
        path.resolve().relative_to(root)
    except ValueError:
        reject("REFERENCE_REPOSITORY_ESCAPE", ref)
    return path


def read_bytes(root, ref):
    path = path_at(root, ref)
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                reject("REFERENCE_NOT_REGULAR_FILE", ref)
            return stream.read()
    except FileNotFoundError:
        reject("REFERENCE_TARGET_MISSING", ref)


def parse_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                reject("JSON_DUPLICATE_KEY", key)
            result[key] = value
        return result

    def invalid(value):
        reject("JSON_NONFINITE_NUMBER", value)

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=invalid)
    except (UnicodeError, ValueError) as exc:
        reject("JSON_INVALID", exc)


def read_ref(root, ref, expected_sha256, identity):
    """Verify final bytes first, then caller-specified logical identity fields."""
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256 or ""):
        reject("REFERENCE_SHA256_INVALID", ref)
    data = read_bytes(root, ref)
    if sha256(data) != expected_sha256:
        reject("REFERENCE_FIXITY_MISMATCH", ref)
    value = parse_json(data)
    if not isinstance(value, dict) or not identity or any(
            value.get(key) != expected for key, expected in identity.items()):
        reject("REFERENCE_IDENTITY_MISMATCH", ref)
    return value


def serialize(value, schema, resolve_ref):
    """Order every object by its schema properties; reject unordered objects.

    Validation is a separate required publication step. A schema resolver is
    supplied by the schema layer, keeping serialization independent of tooling
    and external authority. Arrays and Unicode strings are not normalized.
    """
    def ordered(item, definition):
        if "$ref" in definition:
            definition = resolve_ref(definition["$ref"])
        if isinstance(item, dict):
            properties = definition.get("properties")
            if properties is None or set(item) - set(properties):
                reject("SERIALIZATION_SCHEMA_ORDER_UNDEFINED")
            return {key: ordered(item[key], child)
                    for key, child in properties.items() if key in item}
        if isinstance(item, list):
            if "items" not in definition:
                reject("SERIALIZATION_SCHEMA_ORDER_UNDEFINED")
            return [ordered(child, definition["items"]) for child in item]
        return item

    try:
        return (json.dumps(ordered(value, schema), ensure_ascii=False,
                           allow_nan=False, indent=2) + "\n").encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        reject("SERIALIZATION_INVALID", exc)


def directory_barrier(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def file_barrier(fd):
    os.fsync(fd)
    # macOS F_FULLFSYNC flushes the hardware cache; fsync alone is weaker.
    if hasattr(fcntl, "F_FULLFSYNC"):
        fcntl.fcntl(fd, fcntl.F_FULLFSYNC)


def ensure_parent(root, ref):
    path = path_at(root, ref)
    chain = []
    parent = path.parent
    while not parent.exists():
        chain.append(parent)
        parent = parent.parent
    for directory in reversed(chain):
        try:
            directory.mkdir()
        except FileExistsError:
            if not directory.is_dir() or directory.is_symlink():
                raise
        directory_barrier(directory.parent)
    path_at(root, ref)
    return path


@contextlib.contextmanager
def exclusive_lock(root, ref, unavailable_code):
    """One stable inode per lock name. OS releases flock on process exit."""
    fd = None
    acquired = False
    try:
        path = ensure_parent(root, ref)
        fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            reject(unavailable_code, "non-regular lock")
        fcntl.flock(fd, fcntl.LOCK_EX)
        acquired = True
        held = os.fstat(fd)
        current = path.lstat()
        if (held.st_dev, held.st_ino) != (current.st_dev, current.st_ino):
            reject(unavailable_code, "lock rendezvous replaced")
    except (OSError, AttributeError) as exc:
        if fd is not None:
            os.close(fd)
        reject(unavailable_code, exc)
    except BaseException:
        if fd is not None:
            os.close(fd)
        raise
    try:
        yield
    finally:
        if acquired:
            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def immutable_publish(root, ref, value, *, validate, encode, identity,
                      checkpoint=lambda phase: None):
    """Create-only publication, with ambiguity after final-link attempts.

    validate must raise on any schema/semantic failure; encode supplies the
    schema-ordered serializer. Neither callback creates authority. checkpoint
    supports deterministic failure injection in isolated tests.
    """
    validate(value)
    data = encode(value)
    if parse_json(data) != value:
        reject("SERIALIZATION_VALUE_MISMATCH", ref)
    expected = sha256(data)
    if not identity or any(value.get(k) != v for k, v in identity.items()):
        reject("REFERENCE_IDENTITY_MISMATCH", ref)
    path = path_at(root, ref)
    if path.exists():
        reject("ARTIFACT_FINAL_PATH_ALREADY_EXISTS", ref)
    temporary = None
    publication_attempted = False
    try:
        path = ensure_parent(root, ref)
        fd, temporary = tempfile.mkstemp(prefix=".publication-", suffix=".tmp",
                                          dir=path.parent)
        with os.fdopen(fd, "w+b") as stream:
            stream.write(data)
            stream.flush()
            stream.seek(0)
            observed = stream.read()
            if len(observed) != len(data) or sha256(observed) != expected:
                reject("STAGING_FIXITY_MISMATCH", ref)
            checkpoint("staged")
            file_barrier(stream.fileno())
        checkpoint("durable_stage")
        publication_attempted = True
        try:
            os.link(temporary, path, follow_symlinks=False)
        except FileExistsError:
            reject("IMMUTABLE_ARTIFACT_PUBLICATION_COLLISION", ref)
        except OSError as exc:
            if exc.errno in (errno.EXDEV, errno.ENOTSUP, errno.EOPNOTSUPP,
                             errno.ENOSYS):
                reject("IMMUTABLE_ARTIFACT_ATOMIC_PUBLICATION_UNAVAILABLE", exc)
            raise
        checkpoint("linked")
        directory_barrier(path.parent)
        checkpoint("directory_durable")
        observed = read_bytes(root, ref)
        if len(observed) != len(data) or observed != data:
            reject("ARTIFACT_PUBLICATION_OUTCOME_AMBIGUOUS", ref)
        read_ref(root, ref, expected, identity)
        checkpoint("verified")
        return {"ref": ref, "sha256": expected, "byte_size": len(data)}
    except OperationalError as exc:
        if publication_attempted and exc.code not in (
                "IMMUTABLE_ARTIFACT_PUBLICATION_COLLISION",
                "IMMUTABLE_ARTIFACT_ATOMIC_PUBLICATION_UNAVAILABLE",
                "ARTIFACT_PUBLICATION_OUTCOME_AMBIGUOUS"):
            reject("ARTIFACT_PUBLICATION_OUTCOME_AMBIGUOUS", exc)
        raise
    except (OSError, RuntimeError) as exc:
        reject("ARTIFACT_PUBLICATION_OUTCOME_AMBIGUOUS" if publication_attempted
               else "IMMUTABLE_ARTIFACT_ATOMIC_PUBLICATION_UNAVAILABLE", exc)
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass  # Non-authoritative debris, never retry final publication.


def namespace_lock(root, case_id, namespace):
    validate_case(case_id)
    if namespace == "TXN":
        return exclusive_lock(root, ".projectorigin/allocation-locks/" +
                              case_id + ".lock", "ALLOCATION_SERIALIZATION_UNAVAILABLE")
    if namespace not in ("RDET", "RAUTH", "LRRES"):
        reject("OPERATIONAL_NAMESPACE_INVALID", namespace)
    return exclusive_lock(root, ".projectorigin/id-allocation-locks/" + namespace
                          + "/" + case_id + ".lock",
                          "OPERATIONAL_ID_SERIALIZATION_UNAVAILABLE")


def validate_case(case_id):
    if not re.fullmatch(r"FILE-(?!0000)[0-9]{4}", case_id or ""):
        reject("CASE_ID_INVALID", case_id)


def validate_id(value, namespace, case_id):
    validate_case(case_id)
    if not re.fullmatch(re.escape(case_id + "-" + namespace + "-") +
                        r"(?!0000)[0-9]{4}", value or ""):
        reject("OPERATIONAL_ID_INVALID", value)


def resolution_lock(root, case_id, transaction_id):
    validate_id(transaction_id, "TXN", case_id)
    return exclusive_lock(root, ".projectorigin/lease-release-resolution-locks/"
                          + case_id + "/" + transaction_id + ".lock",
                          "LEASE_RELEASE_RESOLUTION_SERIALIZATION_UNAVAILABLE")


def lease_slot_lock(root, case_id, unavailable_code):
    """Serialize lease-slot syscalls, not transaction ownership or authority.

    Acquire and release both use this private mutex. It is held only around
    fresh observation/publication or compare/delete, never during a transaction.
    It belongs to the already ignored leases directory and is not a Case Lease.
    """
    validate_case(case_id)
    return exclusive_lock(root, ".projectorigin/leases/" + case_id + ".slot.lock",
                          unavailable_code)
