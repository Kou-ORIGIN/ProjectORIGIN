"""Storage tests run exclusively in disposable directories, never Case data."""

import multiprocessing
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from case_bootstrap import storage as s


SCHEMA = {"properties": {"id": {"type": "string"},
                         "note": {"type": "string"},
                         "items": {"items": {"type": "integer"}}}}
VALUE = {"note": "日本/e\u0301", "items": [2, 1], "id": "example"}
EXPECTED = ('{\n  "id": "example",\n  "note": "日本/e\u0301",\n'
            '  "items": [\n    2,\n    1\n  ]\n}\n').encode("utf-8")


def encode(value):
    return s.serialize(value, SCHEMA, lambda ref: None)


def validate(value):
    if set(value) != {"id", "note", "items"}:
        s.reject("SCHEMA_ERROR")


def publish(root, checkpoint=lambda phase: None):
    return s.immutable_publish(root, "evidence/record.json", VALUE,
                               validate=validate, encode=encode,
                               identity={"id": "example"}, checkpoint=checkpoint)


def publish_worker(root, start, queue):
    start.wait(10)
    try:
        publish(root)
        queue.put("PASS")
    except s.OperationalError as exc:
        queue.put(exc.code)


def lock_worker(root, case, start, queue):
    start.wait(10)
    with s.namespace_lock(root, case, "TXN"):
        # Python 3.9 on macOS does not promise a shared monotonic-clock origin
        # across processes. Wall-clock observations share an epoch on this host.
        begin = time.time_ns()
        time.sleep(0.25)
        end = time.time_ns()
    queue.put((begin, end))


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def assert_code(self, code, function, *args, **kwargs):
        with self.assertRaises(s.OperationalError) as caught:
            function(*args, **kwargs)
        self.assertEqual(code, caught.exception.code)

    def test_expected_bytes(self):
        self.assertEqual(EXPECTED, encode(VALUE))

    def test_expected_sha256(self):
        self.assertEqual("f1f5be8d7aaee50cda649e3d06ae6a48a5662517f6888d5c7bc74448e9aa7023",
                         s.sha256(encode(VALUE)))

    def test_insertion_order_does_not_change_bytes(self):
        self.assertEqual(encode(VALUE), encode(dict(reversed(list(VALUE.items())))))

    def test_array_order_preserved(self):
        self.assertNotEqual(encode(VALUE), encode(dict(VALUE, items=[1, 2])))

    def test_unicode_not_normalized(self):
        self.assertIn("e\u0301".encode(), encode(VALUE))
        self.assertNotIn("é".encode(), encode(VALUE))

    def test_timestamp_not_normalized(self):
        value = dict(VALUE, note="2026-09-12T18:10:00.000+09:00")
        self.assertIn(value["note"].encode(), encode(value))

    def test_unknown_order_rejected(self):
        self.assert_code("SERIALIZATION_SCHEMA_ORDER_UNDEFINED", encode,
                         dict(VALUE, unknown=True))

    def test_nested_object_order(self):
        schema = {"properties": {"child": {"$ref": "urn:test"}}}
        data = s.serialize({"child": {"b": 1, "a": 2}}, schema,
                           lambda ref: {"properties": {"a": {}, "b": {}}})
        self.assertLess(data.index(b'"a"'), data.index(b'"b"'))

    def test_nonfinite_rejected(self):
        self.assert_code("SERIALIZATION_INVALID", encode, dict(VALUE, items=[float("nan")]))

    def test_duplicate_json_key_rejected(self):
        self.assert_code("JSON_DUPLICATE_KEY", s.parse_json, b'{"id":1,"id":2}')

    def test_json_nonfinite_rejected(self):
        self.assert_code("JSON_NONFINITE_NUMBER", s.parse_json, b'{"id":NaN}')

    def test_json_invalid_rejected(self):
        self.assert_code("JSON_INVALID", s.parse_json, b'\xff')

    def test_ref_invalid_names(self):
        for ref in ("/tmp/escape", "../escape", "a/../b", "./a", "a//b",
                    "a/", "a\\b", "C:/escape", "", "a/./b", "a\x00b"):
            with self.subTest(ref=ref):
                self.assert_code("REFERENCE_PATH_INVALID", s.path_at, self.root, ref)

    def test_symlink_escape_rejected(self):
        (self.root / "escape").symlink_to(self.root.parent, target_is_directory=True)
        self.assert_code("REFERENCE_SYMLINK_UNSUPPORTED", s.path_at,
                         self.root, "escape/file")

    def test_missing_durable_ref(self):
        self.assert_code("REFERENCE_TARGET_MISSING", s.read_ref,
                         self.root, "missing.json", "0" * 64, {"id": "example"})

    def test_sha_mismatch(self):
        publish(self.root)
        self.assert_code("REFERENCE_FIXITY_MISMATCH", s.read_ref,
                         self.root, "evidence/record.json", "0" * 64, {"id": "example"})

    def test_invalid_sha(self):
        self.assert_code("REFERENCE_SHA256_INVALID", s.read_ref,
                         self.root, "evidence/record.json", "A" * 64, {"id": "example"})

    def test_identity_mismatch(self):
        result = publish(self.root)
        self.assert_code("REFERENCE_IDENTITY_MISMATCH", s.read_ref,
                         self.root, result["ref"], result["sha256"], {"id": "other"})

    def test_empty_identity_rejected(self):
        result = publish(self.root)
        self.assert_code("REFERENCE_IDENTITY_MISMATCH", s.read_ref,
                         self.root, result["ref"], result["sha256"], {})

    def test_success_readback(self):
        result = publish(self.root)
        self.assertEqual(len(EXPECTED), result["byte_size"])
        self.assertEqual(EXPECTED, (self.root / result["ref"]).read_bytes())
        self.assertEqual(VALUE, s.read_ref(self.root, result["ref"], result["sha256"],
                                          {"id": "example"}))

    def test_no_final_overwrite(self):
        result = publish(self.root)
        self.assert_code("ARTIFACT_FINAL_PATH_ALREADY_EXISTS", publish, self.root)
        self.assertEqual(EXPECTED, (self.root / result["ref"]).read_bytes())

    def test_schema_failure_no_materialization(self):
        self.assert_code("SCHEMA_ERROR", s.immutable_publish, self.root,
                         "evidence/record.json", {}, validate=validate, encode=encode,
                         identity={"id": "example"})
        self.assertEqual([], list(self.root.iterdir()))

    def test_failure_before_publication(self):
        def fail(phase):
            if phase == "durable_stage":
                raise OSError("injected")
        self.assert_code("IMMUTABLE_ARTIFACT_ATOMIC_PUBLICATION_UNAVAILABLE",
                         publish, self.root, fail)
        self.assertFalse((self.root / "evidence/record.json").exists())

    def test_ambiguous_after_link(self):
        def fail(phase):
            if phase == "linked":
                raise OSError("injected")
        self.assert_code("ARTIFACT_PUBLICATION_OUTCOME_AMBIGUOUS", publish,
                         self.root, fail)
        self.assertEqual(EXPECTED, (self.root / "evidence/record.json").read_bytes())

    def test_unavailable_no_copy_fallback(self):
        with mock.patch.object(s.os, "link", side_effect=OSError(s.errno.EXDEV, "injected")):
            self.assert_code("IMMUTABLE_ARTIFACT_ATOMIC_PUBLICATION_UNAVAILABLE",
                             publish, self.root)
        self.assertFalse((self.root / "evidence/record.json").exists())

    def test_cleanup_failure_does_not_negate_verified_publish(self):
        with mock.patch.object(s.os, "unlink", side_effect=OSError("injected")):
            result = publish(self.root)
        self.assertEqual(EXPECTED, (self.root / result["ref"]).read_bytes())
        self.assertEqual(1, len(list((self.root / "evidence").glob(".publication-*.tmp"))))

    def test_final_readback_failure_is_ambiguous(self):
        with mock.patch.object(s, "read_bytes", side_effect=OSError("injected")):
            self.assert_code("ARTIFACT_PUBLICATION_OUTCOME_AMBIGUOUS", publish, self.root)

    def test_collision_between_observation_and_link(self):
        def race(phase):
            if phase == "durable_stage":
                (self.root / "evidence/record.json").write_bytes(b"foreign")
        self.assert_code("IMMUTABLE_ARTIFACT_PUBLICATION_COLLISION", publish,
                         self.root, race)
        self.assertEqual(b"foreign", (self.root / "evidence/record.json").read_bytes())

    def test_invalid_ids(self):
        for case in ("FILE-0000", "FILE-1", "FILE-10000"):
            self.assert_code("CASE_ID_INVALID", s.validate_case, case)
        for value in ("FILE-0001-TXN-0000", "FILE-0002-TXN-0001", "FILE-0001-TXN-1"):
            self.assert_code("OPERATIONAL_ID_INVALID", s.validate_id,
                             value, "TXN", "FILE-0001")

    def test_lock_inode_retained(self):
        ref = ".projectorigin/allocation-locks/FILE-0001.lock"
        with s.namespace_lock(self.root, "FILE-0001", "TXN"):
            inode = (self.root / ref).stat().st_ino
        with s.namespace_lock(self.root, "FILE-0001", "TXN"):
            self.assertEqual(inode, (self.root / ref).stat().st_ino)

    def test_unavailable_lock_fails_closed(self):
        with mock.patch.object(s.fcntl, "flock", side_effect=OSError("injected")):
            with self.assertRaises(s.OperationalError) as caught:
                with s.namespace_lock(self.root, "FILE-0001", "TXN"):
                    self.fail("unlocked fallback")
        self.assertEqual("ALLOCATION_SERIALIZATION_UNAVAILABLE", caught.exception.code)

    def test_lock_responsibilities_distinct(self):
        with s.namespace_lock(self.root, "FILE-0001", "TXN"):
            with s.namespace_lock(self.root, "FILE-0001", "RDET"):
                with s.resolution_lock(self.root, "FILE-0001", "FILE-0001-TXN-0001"):
                    with s.lease_slot_lock(self.root, "FILE-0001", "UNAVAILABLE"):
                        self.assertEqual(4, len(list(self.root.rglob("*.lock"))))

    def processes(self, worker, arguments):
        context = multiprocessing.get_context("spawn")
        start = context.Event()
        queue = context.Queue()
        processes = [context.Process(target=worker, args=(str(self.root), *args, start, queue))
                     for args in arguments]
        try:
            for process in processes:
                process.start()
            start.set()
            result = [queue.get(timeout=20) for _ in processes]
            for process in processes:
                process.join(20)
                self.assertEqual(0, process.exitcode)
            return result
        finally:
            for process in processes:
                if process.is_alive():
                    process.terminate()
                    process.join()
            queue.close()

    def test_real_concurrent_publication(self):
        results = self.processes(publish_worker, [(), (), (), ()])
        self.assertEqual(1, results.count("PASS"))
        self.assertTrue(set(results) <= {"PASS", "ARTIFACT_FINAL_PATH_ALREADY_EXISTS",
                                        "IMMUTABLE_ARTIFACT_PUBLICATION_COLLISION"})
        self.assertEqual(EXPECTED, (self.root / "evidence/record.json").read_bytes())

    def test_real_same_case_exclusion(self):
        intervals = sorted(self.processes(lock_worker, [("FILE-0001",)] * 3))
        self.assertTrue(all(a[1] <= b[0] for a, b in zip(intervals, intervals[1:])))

    def test_real_different_case_parallelism(self):
        # Longer independent holding periods make overlap robust to spawn jitter.
        intervals = self.processes(lock_worker, [("FILE-0001",), ("FILE-0002",)])
        self.assertLess(max(i[0] for i in intervals), min(i[1] for i in intervals))


if __name__ == "__main__":
    unittest.main()
