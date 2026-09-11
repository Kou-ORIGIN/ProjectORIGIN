import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-workflow.py"
SCHEMA = ROOT / "schemas" / "workflows" / "case-production-workflow-definition.schema.json"
DEFINITION = ROOT / "workflows" / "case-production-workflow_v1.0.json"
SPEC = importlib.util.spec_from_file_location("validate_workflow", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class WorkflowValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(DEFINITION.read_text(encoding="utf-8"))

    def mutated(self):
        return copy.deepcopy(self.baseline)

    def ids(self, definition):
        return {item["id"]: item for item in definition["steps"]}

    def substates(self, definition):
        return {
            state["id"]: state
            for step in definition["steps"]
            for state in step.get("substates", [])
        }

    def finding_ids(self, definition):
        return {item["id"] for item in VALIDATOR.validate_semantics(definition)}

    def assert_finding(self, definition, expected):
        self.assertIn(expected, self.finding_ids(definition))

    def test_01_current_definition_passes_semantics(self):
        self.assertEqual([], VALIDATOR.validate_semantics(self.mutated()))

    def test_02_valid_revision_route_is_accepted(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-014"]["failure_routing"]["routes"][0]
        self.assertEqual(("REVISION", "CPW-013"), (route["route_kind"], route["target"]))
        self.assertEqual([], VALIDATOR.validate_routes_and_graph(definition))

    def test_03_valid_external_wait_is_accepted(self):
        definition = self.mutated()
        self.assertEqual([], VALIDATOR.validate_rights(definition))

    def test_04_missing_cpw_step(self):
        definition = self.mutated()
        definition["steps"].pop()
        self.assert_finding(definition, "GRAPH-STEP-COUNT")

    def test_05_duplicate_cpw_id(self):
        definition = self.mutated()
        definition["steps"][-1]["id"] = "CPW-028"
        self.assert_finding(definition, "GRAPH-DUPLICATE-STEP")

    def test_06_cpw_030(self):
        definition = self.mutated()
        definition["steps"][-1]["id"] = "CPW-030"
        self.assert_finding(definition, "GRAPH-CPW-SET-ORDER")

    def test_07_unknown_route_target(self):
        definition = self.mutated()
        self.ids(definition)["CPW-001"]["routing"]["routes"][0]["target"] = "CPW-099"
        self.assert_finding(definition, "GRAPH-UNKNOWN-TARGET")

    def test_08_cpw_028_bypass(self):
        definition = self.mutated()
        self.ids(definition)["CPW-027"]["routing"]["routes"][0]["target"] = "CPW-029"
        self.assert_finding(definition, "HUMAN-GATE-CPW028-BYPASS")

    def test_09_missing_rights_substate(self):
        definition = self.mutated()
        self.ids(definition)["CPW-021"]["substates"].pop()
        self.assert_finding(definition, "RIGHTS-SET-ORDER")

    def test_10_rights_order_changed(self):
        definition = self.mutated()
        states = self.ids(definition)["CPW-021"]["substates"]
        states[0], states[1] = states[1], states[0]
        self.assert_finding(definition, "RIGHTS-SET-ORDER")

    def test_11_legacy_send_authorized(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-04"]["human_gate"]["allowed_decisions"] = ["SEND_AUTHORIZED"]
        found = self.finding_ids(definition)
        self.assertIn("HUMAN-GATE-LEGACY-DECISION", found)

    def test_12_silence_as_permission(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-05"]["external_dependency"]["silence_is_permission"] = True
        self.assert_finding(definition, "RIGHTS-SILENCE-PERMISSION")

    def test_13_timeout_as_rejection(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-05"]["external_dependency"]["timeout_is_rejection"] = True
        self.assert_finding(definition, "RIGHTS-TIMEOUT-REJECTION")

    def test_14_rights_04_auto_cross(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-04"]["human_gate"]["automatic_crossing_prohibited"] = False
        self.assert_finding(definition, "HUMAN-GATE-AUTO-CROSS")

    def test_15_draft_reaches_wait(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-03"]["routing"]["routes"].append(
            {"route_kind": "DEFAULT", "target": "CPW-021", "condition_ref": "ENTER_RIGHTS-05"}
        )
        self.assert_finding(definition, "RIGHTS-DRAFT-TO-WAIT")

    def test_16_human_interpretation_bypasses_rights_09(self):
        definition = self.mutated()
        resume = self.substates(definition)["RIGHTS-08"]["human_gate"]["resume_rule"]
        resume["target"] = "CPW-022"
        self.assert_finding(definition, "RIGHTS-INTERPRETATION-BOUNDARY")

    def test_17_missing_delivery_substate(self):
        definition = self.mutated()
        self.ids(definition)["CPW-029"]["substates"].pop()
        self.assert_finding(definition, "PUBLICATION-SET-ORDER")

    def test_18_delivery_order_changed(self):
        definition = self.mutated()
        states = self.ids(definition)["CPW-029"]["substates"]
        states[2], states[3] = states[3], states[2]
        self.assert_finding(definition, "PUBLICATION-SET-ORDER")

    def test_19_tracking_as_publication_evidence(self):
        definition = self.mutated()
        tracking = self.substates(definition)["DELIVERY-05"]
        tracking["source_of_truth"] = [{"result_kind": "PUBLICATION_COMPLETION"}]
        self.assert_finding(definition, "PUBLICATION-TRACKING-AS-EVIDENCE")

    def test_20_mechanical_validation_as_formal_audit(self):
        definition = self.mutated()
        self.ids(definition)["CPW-025"]["audit_applicability"]["audit_category"] = "MECHANICAL_VALIDATION"
        self.assert_finding(definition, "IMAGE-VALIDATION-AUDIT-ALIAS")

    def test_21_automatic_global_invalidation(self):
        definition = self.mutated()
        self.ids(definition)["CPW-026"]["change_impact"]["automatic_global_invalidation"] = True
        self.assert_finding(definition, "IMAGE-AUTOMATIC-GLOBAL-INVALIDATION")

    def test_22_automatic_final_flow_hold(self):
        definition = self.mutated()
        self.ids(definition)["CPW-027"]["failure_routing"]["routes"][0]["route_kind"] = "HOLD"
        found = self.finding_ids(definition)
        self.assertTrue({"FINAL-FLOW-HOLD-ROUTE", "FINAL-FLOW-FAILURE-ROUTE"} <= found)

    def test_23_hold_route_kind_vocabulary(self):
        definition = self.mutated()
        definition["controlled_vocabularies"]["route_kinds"].append("HOLD")
        self.assert_finding(definition, "FINAL-FLOW-HOLD-ROUTE")

    def test_24_cpw_028_automatic_approval(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-028"]["routing"]["routes"][0]
        route["route_kind"] = "DEFAULT"
        route.pop("result_ref", None)
        self.assert_finding(definition, "HUMAN-GATE-AUTO-APPROVAL")

    def test_25_fully_automatable(self):
        definition = self.mutated()
        definition["controlled_vocabularies"]["automation_classification"].append("FULLY_AUTOMATABLE")
        self.assert_finding(definition, "IDENTITY-FULLY-AUTOMATABLE")

    def test_26_governance_version_mismatch(self):
        definition = self.mutated()
        definition["applicable_governance"][0]["version"] = "v9.9"
        errors, _ = VALIDATOR.validate_governance(definition, ROOT)
        self.assertIn("GOVERNANCE-DECLARATION-MISMATCH", {item["id"] for item in errors})

    def test_27_missing_governance_reference(self):
        definition = self.mutated()
        definition["applicable_governance"].pop()
        errors, _ = VALIDATOR.validate_governance(definition, ROOT)
        self.assertIn("GOVERNANCE-DECLARATION-MISMATCH", {item["id"] for item in errors})

    def test_28_unexpected_cpw_id(self):
        definition = self.mutated()
        definition["steps"][5]["id"] = "OTHER-006"
        self.assert_finding(definition, "GRAPH-CPW-SET-ORDER")

    def test_29_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"a": 1, "a": 2}\n', encoding="utf-8")
            with self.assertRaises(VALIDATOR.DuplicateKeyError):
                VALIDATOR.load_json_strict(path)

    def test_30_schema_capability_is_explicit(self):
        report = VALIDATOR.run_validation(SCHEMA, DEFINITION, ROOT, True)
        self.assertIn(report["layers"]["SCHEMA_VALIDATION"], {"PASS", "UNAVAILABLE"})
        if report["layers"]["SCHEMA_VALIDATION"] == "UNAVAILABLE":
            self.assertEqual("VALIDATION_LIMITED", report["validator_result"])
            self.assertEqual(3, report["exit_code"])

    def test_31_json_cli_output(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--schema", str(SCHEMA), "--definition", str(DEFINITION),
             "--repository-root", str(ROOT), "--check-governance", "--format", "json"],
            check=False, capture_output=True, text=True,
        )
        report = json.loads(completed.stdout)
        self.assertEqual(report["exit_code"], completed.returncode)
        self.assertEqual("PASS", report["layers"]["SEMANTIC_VALIDATION"])
        self.assertEqual("PASS", report["layers"]["GOVERNANCE_COMPATIBILITY"])

    def test_32_registration_cannot_establish_human_approval(self):
        definition = self.mutated()
        self.ids(definition)["CPW-025"]["source_of_truth"].append(
            {"result_kind": "HUMAN_APPROVAL_DECISION"}
        )
        self.assert_finding(definition, "IMAGE-REGISTRATION-DOWNSTREAM-INFERENCE")

    def test_33_publication_execution_cannot_establish_completion(self):
        definition = self.mutated()
        self.substates(definition)["DELIVERY-02"]["source_of_truth"] = [
            {"result_kind": "PUBLICATION_COMPLETION"}
        ]
        self.assert_finding(definition, "PUBLICATION-STATE-INFERENCE")

    def test_34_top_level_cpw_reorder(self):
        definition = self.mutated()
        definition["steps"][3], definition["steps"][4] = definition["steps"][4], definition["steps"][3]
        self.assert_finding(definition, "GRAPH-CPW-SET-ORDER")

    def test_35_unconditional_self_revision_cycle(self):
        definition = self.mutated()
        self.ids(definition)["CPW-014"]["routing"]["routes"][0] = {
            "route_kind": "REVISION", "target": "CPW-014"
        }
        self.assert_finding(definition, "GRAPH-CYCLE-UNGUARDED")

    def test_36_unconditional_backward_revision_cycle(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-014"]["failure_routing"]["routes"][0]
        route.pop("result_ref", None)
        route.pop("condition_ref", None)
        route.pop("resume_rule", None)
        self.assert_finding(definition, "GRAPH-CYCLE-UNGUARDED")

    def test_37_condition_governed_revision_cycle(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-014"]["failure_routing"]["routes"][0]
        self.assertEqual("REVISION", route["route_kind"])
        self.assertTrue(route.get("condition_ref") or route.get("result_ref") or route.get("resume_rule"))
        self.assertNotIn("GRAPH-CYCLE-UNGUARDED", self.finding_ids(definition))

    def test_38_closed_cyclic_scc(self):
        definition = self.mutated()
        step = self.ids(definition)["CPW-014"]
        guarded = {"route_kind": "REVISION", "target": "CPW-014", "condition_ref": "new-evidence"}
        step["routing"]["routes"] = [copy.deepcopy(guarded)]
        step["failure_routing"]["routes"] = [copy.deepcopy(guarded)]
        step["audit_applicability"]["on_pass"] = copy.deepcopy(guarded)
        step["audit_applicability"]["on_revision_required"] = copy.deepcopy(guarded)
        step["audit_applicability"]["on_blocked"] = copy.deepcopy(guarded)
        self.assert_finding(definition, "GRAPH-CYCLE-NO-EXIT")

    def test_39_response_evidence_as_permission(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-06"]["source_of_truth"] = [
            {"result_kind": "PERMISSION", "source_type": "RIGHTS_RESPONSE_EVIDENCE"}
        ]
        self.assert_finding(definition, "RIGHTS-RESPONSE-AS-PERMISSION")

    def test_40_ai_extraction_as_human_consent(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-07"]["source_of_truth"] = [
            {"result_kind": "HUMAN_CONSENT", "source_type": "HUMAN_DECISION_RECORD"}
        ]
        self.assert_finding(definition, "RIGHTS-AI-AS-HUMAN-CONSENT")

    def test_41_rights_verification_to_cpw_028(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-09"]["routing"]["routes"] = [
            {"route_kind": "DEFAULT", "target": "CPW-028"}
        ]
        self.assert_finding(definition, "RIGHTS-VERIFICATION-AS-HUMAN-APPROVAL")

    def test_42_rights_verification_to_cpw_029(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-10"]["routing"]["routes"][0]["target"] = "CPW-029"
        self.assert_finding(definition, "RIGHTS-VERIFICATION-AS-HUMAN-APPROVAL")

    def test_43_rights_substate_final_approval_gate(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-09"]["human_gate"] = {
            "gate_type": "FINAL_HUMAN_APPROVAL"
        }
        self.assert_finding(definition, "RIGHTS-VERIFICATION-AS-HUMAN-APPROVAL")

    def test_44_equivalent_rights_prose_rewording(self):
        definition = self.mutated()
        self.substates(definition)["RIGHTS-08"]["human_gate"]["resume_rule"]["resume_rule"] = (
            "Informational wording changed without changing the structured route."
        )
        self.assertEqual([], VALIDATOR.validate_semantics(definition))

    def test_45_review_package_prose_is_informational(self):
        definition = self.mutated()
        definition["interfaces"]["human_review_package"]["responsibility_boundary"] = (
            "Contradictory or reworded informational prose is not interpreted by this validator."
        )
        self.assertEqual([], VALIDATOR.validate_semantics(definition))

    def test_46_manifest_prose_is_informational(self):
        definition = self.mutated()
        definition["interfaces"]["orchestration_manifest"]["responsibility_boundary"] = (
            "Reworded informational prose; normative structured fields remain unchanged."
        )
        self.assertEqual([], VALIDATOR.validate_semantics(definition))

    def test_47_structured_manifest_authority_misuse(self):
        definition = self.mutated()
        self.ids(definition)["CPW-028"]["human_gate"]["decision_source"]["reference"]["artifact_type"] = (
            "ORCHESTRATION_MANIFEST"
        )
        self.assert_finding(definition, "BOUNDARY-MANIFEST-AUTHORITY")

    def test_48_structured_review_package_authority_misuse(self):
        definition = self.mutated()
        self.ids(definition)["CPW-028"]["human_gate"]["decision_source"]["reference"]["artifact_type"] = (
            "HUMAN_REVIEW_PACKAGE"
        )
        self.assert_finding(definition, "BOUNDARY-HUMAN-REVIEW-PACKAGE-AUTHORITY")

    def test_49_unconditional_self_return_cycle(self):
        definition = self.mutated()
        self.ids(definition)["CPW-014"]["routing"]["routes"][0] = {
            "route_kind": "RETURN", "target": "CPW-014"
        }
        self.assert_finding(definition, "GRAPH-CYCLE-UNGUARDED")

    def test_50_unconditional_backward_return_cycle(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-004"]["failure_routing"]["routes"][0]
        self.assertEqual("RETURN", route["route_kind"])
        route.pop("condition_ref")
        self.assert_finding(definition, "GRAPH-CYCLE-UNGUARDED")

    def test_51_guarded_canonical_return_cycle_with_exit(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-004"]["failure_routing"]["routes"][0]
        self.assertEqual(("RETURN", "CPW-003"), (route["route_kind"], route["target"]))
        self.assertTrue(route.get("condition_ref"))
        self.assertEqual([], VALIDATOR.validate_routes_and_graph(definition))

    def test_52_guarded_closed_return_scc(self):
        definition = self.mutated()
        step = self.ids(definition)["CPW-014"]
        guarded = {"route_kind": "RETURN", "target": "CPW-014", "condition_ref": "retry-required"}
        step["routing"]["routes"] = [copy.deepcopy(guarded)]
        step["failure_routing"]["routes"] = [copy.deepcopy(guarded)]
        step["audit_applicability"]["on_pass"] = copy.deepcopy(guarded)
        step["audit_applicability"]["on_revision_required"] = copy.deepcopy(guarded)
        step["audit_applicability"]["on_blocked"] = copy.deepcopy(guarded)
        self.assert_finding(definition, "GRAPH-CYCLE-NO-EXIT")

    def test_53_valid_re_audit_cycle(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-027"]["failure_routing"]["routes"][3]
        self.assertEqual("RE_AUDIT", route["route_kind"])
        self.assertNotIn("GRAPH-CYCLE-UNGUARDED", self.finding_ids(definition))

    def test_54_valid_alternative_source_cycle(self):
        definition = self.mutated()
        route = self.ids(definition)["CPW-021"]["routing"]["routes"][1]
        self.assertEqual("ALTERNATIVE_SOURCE", route["route_kind"])
        self.assertNotIn("GRAPH-CYCLE-UNGUARDED", self.finding_ids(definition))

    def test_55_missing_manifest_format_binding(self):
        definition = self.mutated()
        definition["interfaces"]["orchestration_manifest"].pop("format_binding")
        self.assert_finding(definition, "BOUNDARY-MANIFEST-FORMAT-BINDING")

    def test_56_wrong_manifest_format_field(self):
        definition = self.mutated()
        definition["interfaces"]["orchestration_manifest"]["format_binding"]["field"] = "version"
        self.assert_finding(definition, "BOUNDARY-MANIFEST-FORMAT-BINDING")

    def test_57_wrong_manifest_format_value(self):
        definition = self.mutated()
        definition["interfaces"]["orchestration_manifest"]["format_binding"]["value"] = "v2.0"
        self.assert_finding(definition, "BOUNDARY-MANIFEST-FORMAT-BINDING")

    def test_58_extra_manifest_format_property(self):
        definition = self.mutated()
        definition["interfaces"]["orchestration_manifest"]["format_binding"]["extra"] = True
        self.assert_finding(definition, "BOUNDARY-MANIFEST-FORMAT-BINDING")

    def test_59_missing_review_package_snapshot_contract(self):
        definition = self.mutated()
        definition["interfaces"]["human_review_package"].pop("snapshot_contract")
        self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_60_review_package_reference_only_false(self):
        definition = self.mutated()
        definition["interfaces"]["human_review_package"]["snapshot_contract"]["reference_only"] = False
        self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_61_review_package_version_bound_false(self):
        definition = self.mutated()
        definition["interfaces"]["human_review_package"]["snapshot_contract"]["version_bound"] = False
        self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_62_review_package_immutable_false(self):
        definition = self.mutated()
        definition["interfaces"]["human_review_package"]["snapshot_contract"]["immutable"] = False
        self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_63_review_package_material_change_version_false(self):
        definition = self.mutated()
        contract = definition["interfaces"]["human_review_package"]["snapshot_contract"]
        contract["material_change_requires_new_version"] = False
        self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_64_review_package_as_publication_authority(self):
        definition = self.mutated()
        self.substates(definition)["DELIVERY-02"]["source_of_truth"] = [{
            "result_kind": "PUBLICATION_STATUS", "source_type": "HUMAN_REVIEW_PACKAGE"
        }]
        self.assert_finding(definition, "BOUNDARY-HRP-AUTHORITY")

    def test_65_review_package_missing_snapshot_property(self):
        for property_name in (
            "reference_only", "version_bound", "immutable", "material_change_requires_new_version"
        ):
            with self.subTest(property_name=property_name):
                definition = self.mutated()
                definition["interfaces"]["human_review_package"]["snapshot_contract"].pop(property_name)
                self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_66_review_package_extra_snapshot_property(self):
        definition = self.mutated()
        definition["interfaces"]["human_review_package"]["snapshot_contract"]["extra"] = True
        self.assert_finding(definition, "BOUNDARY-HRP-SNAPSHOT-CONTRACT")

    def test_67_duplicate_manifest_interface(self):
        definition = self.mutated()
        definition["interfaces"]["duplicate_manifest"] = copy.deepcopy(
            definition["interfaces"]["orchestration_manifest"]
        )
        self.assert_finding(definition, "SOURCE-MANIFEST-BOUNDARY")

    def test_68_duplicate_review_package_interface(self):
        definition = self.mutated()
        definition["interfaces"]["duplicate_review_package"] = copy.deepcopy(
            definition["interfaces"]["human_review_package"]
        )
        self.assert_finding(definition, "SOURCE-REVIEW-PACKAGE-BOUNDARY")



class AdoptionContractTests(unittest.TestCase):
    """All authority data below is synthetic and exists only in TemporaryDirectory.
    Git commits belong only to that disposable fixture repository.
    """
    def setUp(self):
        import shutil
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in list(VALIDATOR.EXPECTED_GOVERNANCE) + ["scripts/validate-workflow.py", "tests/workflows/test_validate_workflow.py"]:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        for source in SCHEMA.parent.glob("*.schema.json"):
            destination = self.root / "schemas/workflows" / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        self.schema = self.root / SCHEMA.relative_to(ROOT)
        self.workflow = self.root / "workflows/case-production-workflow_v1.0.json"
        self.candidate = json.loads(DEFINITION.read_text())
        self.write(self.workflow, self.candidate)
        self.git("init", "-q")
        self.git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid", "add", ".")
        self.git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Synthetic candidate fixture")
        self.commit = self.git("rev-parse", "HEAD").strip()
        self.target = {"workflow_path": str(self.workflow.relative_to(self.root)), "workflow_version": "v1.0", "definition_format_version": "v1.0", "candidate_definition_sha256": VALIDATOR._sha(self.workflow.read_bytes()), "candidate_git_commit_sha": self.commit}
        self.decision_path = self.root / "fixture-decision.json"
        self.adoption_path = self.root / "fixture-adoption.json"
        self.deprecation_path = self.root / "fixture-deprecation.json"
        self.decision = {"record_format_version":"v1.0", "decision_id":"WFADOPTDEC-9001", "decision_type":"WORKFLOW_FORMAL_ADOPTION", "decision_value":"AUTHORIZE_ADOPTION", "target":copy.deepcopy(self.target), "human_authority":{"authority_type":"EXPLICIT_HUMAN_DECISION","human_actor_id":"HUMAN-9001"}, "validation_evidence":self.evidence(self.target["candidate_definition_sha256"]), "decided_at":"2026-09-11T01:00:00Z", "rationale":"Synthetic test only"}
        self.write(self.decision_path, self.decision)
        self.adopted = dict(self.candidate, status="ADOPTED")
        self.write(self.workflow, self.adopted)
        self.adoption = {"record_format_version":"v1.0", "adoption_record_id":"WFADOPT-9001", "record_type":"WORKFLOW_FORMAL_ADOPTION_RECORD", "target":dict(self.target, adopted_definition_sha256=VALIDATOR._sha(self.workflow.read_bytes())), "transition":{"from_status":"PROPOSED","to_status":"ADOPTED"}, "human_decision":{"decision_id":"WFADOPTDEC-9001","decision_path":"fixture-decision.json","decision_sha256":VALIDATOR._sha(self.decision_path.read_bytes())}, "adopted_at":"2026-09-11T02:00:00Z", "adopted_state_validation_evidence":self.evidence(VALIDATOR._sha(self.workflow.read_bytes()))}
        self.write(self.adoption_path, self.adoption)
        self.authority_path = self.root / "fixture-human-authority.txt"
        self.authority_path.write_text("SYNTHETIC TEST AUTHORITY; not an actual Human decision")
        self.deprecation = {"record_format_version":"v1.0", "deprecation_record_id":"WFDEPREC-9001", "record_type":"WORKFLOW_DEPRECATION_RECORD", "target":self.adoption_ref(), "human_authority":{"authority_type":"EXPLICIT_HUMAN_DECISION","authority_path":"fixture-human-authority.txt","authority_sha256":VALIDATOR._sha(self.authority_path.read_bytes())}, "deprecated_at":"2026-09-11T03:00:00Z", "reason":"Synthetic test only", "successor":None}

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True, stderr=subprocess.PIPE)

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")

    def evidence(self, digest):
        paths = list(VALIDATOR.EXPECTED_GOVERNANCE) + ["scripts/validate-workflow.py", "tests/workflows/test_validate_workflow.py"]
        paths += [str(p.relative_to(self.root)) for p in (self.root / "schemas/workflows").glob("*.schema.json")]
        return {"definition_sha256":digest,"result":"PASS", "json_integrity":"PASS", "schema_validation":"PASS", "semantic_validation":"PASS", "governance_compatibility":"PASS", "tests":{"total":7,"passed":7,"failed":0,"skipped":0,"expected_failures":0}, "validator_exit_code":0,"controlled_artifact_integrity":"PASS", "controlled_artifacts":[{"path":p,"sha256":VALIDATOR._sha((self.root/p).read_bytes())} for p in paths],"warnings":[]}

    def adoption_ref(self):
        return {"workflow_path":self.target["workflow_path"],"workflow_version":"v1.0","adoption_record_id":"WFADOPT-9001","adoption_record_path":"fixture-adoption.json","adoption_record_sha256":VALIDATOR._sha(self.adoption_path.read_bytes()),"adopted_definition_sha256":self.adoption["target"]["adopted_definition_sha256"]}

    def run_set(self, records=None, prospective=False):
        return VALIDATOR.run_validation(self.schema, self.workflow, self.root, True, records if records is not None else [self.adoption_path], prospective)

    def assert_valid(self, report):
        self.assertEqual(0, report["exit_code"], report)
        self.assertEqual("PASS", report["layers"]["SCHEMA_VALIDATION"])
        self.assertEqual("PASS", report["layers"]["CROSS_ARTIFACT_VALIDATION"])

    def assert_invalid(self, report):
        self.assertEqual(1, report["exit_code"], report)
        self.assertTrue(report["errors"])

    def test_valid_completed_adoption(self):
        self.assert_valid(self.run_set())

    def test_current_proposed(self):
        self.write(self.workflow,self.candidate)
        self.assert_valid(self.run_set([]))

    def test_adopted_requires_record(self):
        self.assert_invalid(self.run_set([]))

    def test_proposed_cannot_claim_completed_record(self):
        self.write(self.workflow,self.candidate)
        self.assert_invalid(self.run_set())

    def test_prospective_no_self_reference(self):
        self.assert_valid(self.run_set([],True))
        self.assertNotIn("final_verification_report", self.adoption)
        self.assert_invalid(self.run_set([self.adoption_path],True))

    def test_missing_decision(self):
        self.decision_path.unlink()
        self.assert_invalid(self.run_set())

    def test_duplicate_ids(self):
        duplicate=self.root/'duplicate.json';self.write(duplicate,self.decision)
        self.assert_invalid(self.run_set([self.decision_path,duplicate,self.adoption_path]))

    def test_deprecation_without_successor(self):
        self.write(self.deprecation_path,self.deprecation)
        self.assert_valid(self.run_set([self.adoption_path,self.deprecation_path]))
        self.assertEqual('ADOPTED',json.loads(self.workflow.read_text())['status'])

    def test_deprecation_conflicting_records(self):
        self.write(self.deprecation_path,self.deprecation)
        second=copy.deepcopy(self.deprecation);second['deprecation_record_id']='WFDEPREC-9002'
        p=self.root/'second-deprecation.json';self.write(p,second)
        self.assert_invalid(self.run_set([self.adoption_path,self.deprecation_path,p]))

    def test_authority_artifact_missing(self):
        self.authority_path.unlink();self.write(self.deprecation_path,self.deprecation)
        self.assert_invalid(self.run_set([self.adoption_path,self.deprecation_path]))

    def test_stale_validation_artifact(self):
        (self.root/'tests/workflows/test_validate_workflow.py').write_text('changed')
        self.assert_invalid(self.run_set())

    def test_all_schema_definitions_execute(self):
        from jsonschema import Draft202012Validator
        for path in self.schema.parent.glob('*.schema.json'):
            Draft202012Validator.check_schema(json.loads(path.read_text()))

    def test_validator_has_no_write_or_git_side_effects(self):
        def snapshot():
            return {str(p.relative_to(self.root)):VALIDATOR._sha(p.read_bytes()) for p in self.root.rglob('*') if p.is_file()}
        before=snapshot();self.assert_valid(self.run_set());self.assertEqual(before,snapshot())

    def test_pass_result_exit_zero(self):
        self.write(self.workflow,self.candidate)
        report=VALIDATOR.run_validation(self.schema,self.workflow,None,False)
        self.assertEqual(('PASS',0),(report['validator_result'],report['exit_code']))

    def test_warnings_explicit_nonblocking(self):
        report=self.run_set()
        self.assertEqual(('PASS_WITH_WARNINGS',0),(report['validator_result'],report['exit_code']))
        self.assertTrue(all(w.get('blocking') is False for w in report['warnings']))

    def test_limited_result_exit_three(self):
        from unittest.mock import patch
        self.write(self.workflow,self.candidate)
        with patch.dict(sys.modules,{'jsonschema':None}):
            report=self.run_set([])
        self.assertEqual(('VALIDATION_LIMITED',3),(report['validator_result'],report['exit_code']))

    def test_cli_input_error_exit_two(self):
        result=subprocess.run([sys.executable,'-B',str(SCRIPT),'--schema',str(self.schema),'--definition',str(self.root/'absent.json'),'--format','json'],capture_output=True,text=True)
        self.assertEqual(2,result.returncode)
        self.assertEqual(2,json.loads(result.stdout)['exit_code'])

    def test_git_missing_capability_limited(self):
        from unittest.mock import patch
        with patch.object(VALIDATOR.subprocess,'run',side_effect=FileNotFoundError('git')):
            report=self.run_set()
        self.assertEqual(3,report['exit_code'])


def _set_nested(data, path, value):
    for key in path[:-1]:data=data[key]
    if value is _DELETE:del data[path[-1]]
    else:data[path[-1]]=copy.deepcopy(value)


_DELETE=object()

def _decision_case(path,value,valid=False):
    def test(self):
        _set_nested(self.decision,path,value)
        self.write(self.decision_path,self.decision)
        self.write(self.workflow,self.candidate)
        report=self.run_set([self.decision_path])
        (self.assert_valid if valid else self.assert_invalid)(report)
    return test


_DECISION_CASES={
 'reject':(['decision_value'],'DO_NOT_AUTHORIZE_ADOPTION',True),
 'revise':(['decision_value'],'REVISE_BEFORE_ADOPTION',True),
 'unknown_value':(['decision_value'],'APPROVED',False),
 'zero_id':(['decision_id'],'WFADOPTDEC-0000',False),
 'newline_id':(['decision_id'],'WFADOPTDEC-9001\n',False),
 'newline_actor':(['human_authority','human_actor_id'],'HUMAN-9001\n',False),
 'newline_sha':(['target','candidate_definition_sha256'],'a'*64+'\n',False),
 'short_id':(['decision_id'],'WFADOPTDEC-1',False),
 'bad_sha':(['target','candidate_definition_sha256'],'A'*64,False),
 'short_commit':(['target','candidate_git_commit_sha'],'a'*7,False),
 'missing_commit':(['target','candidate_git_commit_sha'],'0'*40,False),
 'missing_git_path':(['target','workflow_path'],'workflows/absent.json',False),
 'absolute_path':(['target','workflow_path'],'/tmp/a.json',False),
 'traversal_path':(['target','workflow_path'],'../a.json',False),
 'nonhuman':(['human_authority','authority_type'],'AI',False),
 'actor_malformed':(['human_authority','human_actor_id'],'HUMAN-1',False),
 'missing_rationale':(['rationale'],_DELETE,False),
 'empty_rationale':(['rationale'],'   ',False),
 'offset_timestamp':(['decided_at'],'2026-09-11T01:00:00+00:00',False),
 'fraction_timestamp':(['decided_at'],'2026-09-11T01:00:00.1Z',False),
 'invalid_date':(['decided_at'],'2026-02-30T01:00:00Z',False),
 'unknown_field':(['updated_at'],'2026-09-11T01:00:00Z',False),
 'no_pass_evidence':(['validation_evidence'],None,False),
 'stale_candidate':(['validation_evidence','definition_sha256'],'0'*64,False),
 'limited_evidence':(['validation_evidence','result'],'VALIDATION_LIMITED',False),
 'failed_evidence':(['validation_evidence','result'],'FAIL',False),
 'bad_test_count':(['validation_evidence','tests','total'],8,False),
 'skipped_tests':(['validation_evidence','tests','skipped'],1,False),
 'missing_controlled':(['validation_evidence','controlled_artifacts'],[],False),
 'git_bytes_mismatch':(['target','candidate_definition_sha256'],'0'*64,False),
}
for name,(path,value,valid) in _DECISION_CASES.items():
    setattr(AdoptionContractTests,'test_decision_'+name,_decision_case(path,value,valid))


def _record_case(path,value):
    def test(self):
        _set_nested(self.adoption,path,value);self.write(self.adoption_path,self.adoption)
        self.assert_invalid(self.run_set())
    return test


for name,path,value in [
 ('decision_sha',['human_decision','decision_sha256'],'0'*64),
 ('candidate_sha',['target','candidate_definition_sha256'],'0'*64),
 ('commit',['target','candidate_git_commit_sha'],'0'*40),
 ('path',['target','workflow_path'],'workflows/other.json'),
 ('version',['target','workflow_version'],'v2.0'),
 ('format',['target','definition_format_version'],'v2.0'),
 ('adopted_sha',['target','adopted_definition_sha256'],'0'*64),
 ('time_order',['adopted_at'],'2026-09-11T00:00:00Z'),
 ('reverse_from',['transition','from_status'],'ADOPTED'),
 ('reverse_to',['transition','to_status'],'PROPOSED'),
 ('unknown',['final_verification_report_sha256'],'0'*64),
]:setattr(AdoptionContractTests,'test_record_'+name,_record_case(path,value))


def _delta_case(field):
    def test(self):
        if field=='notes':self.adopted['notes'].append('unauthorized')
        if field=='steps':self.adopted['steps'][0]['purpose']='unauthorized'
        if field=='governance':self.adopted['applicable_governance'][0]['version']='v99.0'
        if field=='version':self.adopted['workflow_version']='v2.0'
        self.write(self.workflow,self.adopted)
        digest=VALIDATOR._sha(self.workflow.read_bytes())
        self.adoption['target']['adopted_definition_sha256']=digest
        self.adoption['adopted_state_validation_evidence']=self.evidence(digest)
        self.write(self.adoption_path,self.adoption)
        self.assert_invalid(self.run_set())
    return test
for field in ['notes','steps','governance','version']:
    setattr(AdoptionContractTests,'test_delta_'+field,_delta_case(field))


def _deprecation_case(path,value):
    def test(self):
        _set_nested(self.deprecation,path,value);self.write(self.deprecation_path,self.deprecation)
        self.assert_invalid(self.run_set([self.adoption_path,self.deprecation_path]))
    return test
for name,path,value in [
 ('target_record',['target','adoption_record_sha256'],'0'*64),
 ('target_sha',['target','adopted_definition_sha256'],'0'*64),
 ('date',['deprecated_at'],'2026-02-30T00:00:00Z'),
 ('time_order',['deprecated_at'],'2026-09-11T01:00:00Z'),
 ('reason',['reason'],''),
 ('authority_sha',['human_authority','authority_sha256'],'0'*64),
]:setattr(AdoptionContractTests,'test_deprecation_'+name,_deprecation_case(path,value))


def _version_case(value,valid):
    def test(self):
        self.candidate['workflow_version']=value;self.write(self.workflow,self.candidate)
        (self.assert_valid if valid else self.assert_invalid)(self.run_set([]))
    return test
for i,value in enumerate(['1.0','v1','v1.0.0','V1.0','v0.0','v01.0','v1.00','v1.-1','v1.0x']):
    setattr(AdoptionContractTests,'test_version_invalid_'+str(i),_version_case(value,False))
for i,value in enumerate(['v1.0','v2.3','v10.0']):
    setattr(AdoptionContractTests,'test_version_valid_'+str(i),_version_case(value,True))



def _make_successor(self, supersedes=False, version="v1.1"):
    path=self.root/'workflows/successor.json'
    candidate=copy.deepcopy(self.candidate);candidate['workflow_version']=version
    if supersedes:
        ref=self.adoption_ref();ref['repository_path']=ref.pop('workflow_path')
        ref['workflow_id']=candidate['workflow_id'];ref['definition_format_version']='v1.0'
        candidate['supersedes']=ref
    self.write(path,candidate)
    self.git('add','workflows/successor.json')
    self.git('-c','user.name=Synthetic Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic successor')
    target=dict(self.target,workflow_path='workflows/successor.json',workflow_version=version,candidate_git_commit_sha=self.git('rev-parse','HEAD').strip(),candidate_definition_sha256=VALIDATOR._sha(path.read_bytes()))
    decision=copy.deepcopy(self.decision);decision['decision_id']='WFADOPTDEC-9002';decision['target']=target;decision['validation_evidence']=self.evidence(target['candidate_definition_sha256'])
    dp=self.root/'successor-decision.json';self.write(dp,decision)
    self.write(path,dict(candidate,status='ADOPTED'))
    record=copy.deepcopy(self.adoption);record['adoption_record_id']='WFADOPT-9002';record['target']=dict(target,adopted_definition_sha256=VALIDATOR._sha(path.read_bytes()));record['human_decision']={'decision_id':'WFADOPTDEC-9002','decision_path':dp.name,'decision_sha256':VALIDATOR._sha(dp.read_bytes())};record['adopted_state_validation_evidence']=self.evidence(record['target']['adopted_definition_sha256'])
    rp=self.root/'successor-adoption.json';self.write(rp,record)
    return {'workflow_path':target['workflow_path'],'workflow_version':version,'adoption_record_id':'WFADOPT-9002','adoption_record_path':rp.name,'adoption_record_sha256':VALIDATOR._sha(rp.read_bytes()),'adopted_definition_sha256':record['target']['adopted_definition_sha256']},path,rp
AdoptionContractTests.make_successor=_make_successor


def _successor_case(mode):
    def test(self):
        if mode=='self':ref=self.adoption_ref()
        else:
            ref,path,rp=self.make_successor(mode=='supersession')
            if mode=='proposed':
                data=json.loads(path.read_text());data['status']='PROPOSED';self.write(path,data)
            if mode=='sha':ref['adopted_definition_sha256']='0'*64
        self.deprecation['successor']=ref;self.write(self.deprecation_path,self.deprecation)
        report=self.run_set([self.adoption_path,self.deprecation_path])
        (self.assert_valid if mode in {'valid','supersession'} else self.assert_invalid)(report)
    return test
for mode in ['valid','self','proposed','sha','supersession']:
    setattr(AdoptionContractTests,'test_successor_'+mode,_successor_case(mode))


def _reject_authority(value):
    def test(self):
        self.decision['decision_value']=value;self.decision['validation_evidence']=None;self.write(self.decision_path,self.decision)
        self.adoption['human_decision']['decision_sha256']=VALIDATOR._sha(self.decision_path.read_bytes());self.write(self.adoption_path,self.adoption)
        self.assert_invalid(self.run_set())
    return test
for value in ['DO_NOT_AUTHORIZE_ADOPTION','REVISE_BEFORE_ADOPTION']:
    setattr(AdoptionContractTests,'test_not_authorization_'+value,_reject_authority(value))


def _reject_without_evidence(self):
    self.decision['decision_value']='DO_NOT_AUTHORIZE_ADOPTION';self.decision['validation_evidence']=None
    self.write(self.decision_path,self.decision);self.write(self.workflow,self.candidate)
    self.assert_valid(self.run_set([self.decision_path]))
AdoptionContractTests.test_reject_without_pass_evidence=_reject_without_evidence


def _git_candidate_adopted(self):
    self.git('add',self.target['workflow_path']);self.git('-c','user.name=Synthetic Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic already-adopted candidate')
    self.decision['target']['candidate_git_commit_sha']=self.git('rev-parse','HEAD').strip()
    self.decision['target']['candidate_definition_sha256']=VALIDATOR._sha(self.workflow.read_bytes())
    self.write(self.decision_path,self.decision)
    self.assert_invalid(self.run_set([self.decision_path]))
AdoptionContractTests.test_git_candidate_already_adopted=_git_candidate_adopted


def _unknown_status(self):
    self.candidate['status']='UNKNOWN';self.write(self.workflow,self.candidate)
    self.assert_invalid(self.run_set([]))
AdoptionContractTests.test_unknown_status=_unknown_status


def _warning_evidence(blocking):
    def test(self):
        self.decision['validation_evidence']['result']='PASS_WITH_WARNINGS'
        self.decision['validation_evidence']['warnings']=[{'id':'TEST','message':'synthetic','blocking':blocking}]
        self.write(self.decision_path,self.decision);self.write(self.workflow,self.candidate)
        (self.assert_invalid if blocking else self.assert_valid)(self.run_set([self.decision_path]))
    return test
AdoptionContractTests.test_evidence_nonblocking_warnings=_warning_evidence(False)
AdoptionContractTests.test_evidence_blocking_warnings=_warning_evidence(True)


def _current_candidate_changed(self):
    self.candidate['notes'].append('changed after validation');self.write(self.workflow,self.candidate)
    self.assert_invalid(self.run_set([self.decision_path]))
AdoptionContractTests.test_current_candidate_evidence_stale=_current_candidate_changed


def _proposed_deprecation_target(self):
    self.write(self.workflow,self.candidate);self.write(self.deprecation_path,self.deprecation)
    self.assert_invalid(self.run_set([self.adoption_path,self.deprecation_path]))
AdoptionContractTests.test_deprecation_proposed_target=_proposed_deprecation_target


def _supersession_self(self):
    ref=self.adoption_ref();ref['repository_path']=ref.pop('workflow_path');ref['workflow_id']=self.candidate['workflow_id'];ref['definition_format_version']='v1.0'
    self.candidate['supersedes']=ref;self.write(self.workflow,self.candidate)
    self.assert_invalid(self.run_set([]))
AdoptionContractTests.test_self_supersession=_supersession_self


def _supersession_cycle_guard(self):
    context=VALIDATOR.AdoptionSet(self.root,self.schema)
    record=context.record(self.adoption_path)
    context.visiting.add(record['adoption_record_id'])
    with self.assertRaisesRegex(VALIDATOR.AdoptionInvalid,'cycle'):
        context.adoption(record)
AdoptionContractTests.test_supersession_cycle_guard=_supersession_cycle_guard


def _unknown_nested_record_fields(self):
    for name,record in [('workflow-adoption-decision',self.decision),('workflow-adoption-record',self.adoption),('workflow-deprecation-record',self.deprecation)]:
        schema=json.loads((self.schema.parent/(name+'.schema.json')).read_text())
        for key in ['target','human_authority' if 'human_authority' in record else 'human_decision']:
            with self.subTest(schema=name,object=key):
                data=copy.deepcopy(record);data[key]['invented_authority']=True
                status,_,_=VALIDATOR.validate_schema_optional(schema,data)
                self.assertEqual('FAIL',status)
AdoptionContractTests.test_closed_nested_objects=_unknown_nested_record_fields


def _cli_bad_invocation(self):
    completed=subprocess.run([sys.executable,'-B',str(SCRIPT)],capture_output=True,text=True)
    self.assertEqual(2,completed.returncode)
AdoptionContractTests.test_bad_invocation_exit_two=_cli_bad_invocation


def _same_version_new_bytes(self):
    ref,path,rp=self.make_successor(version='v1.0')
    self.deprecation['successor']=ref;self.write(self.deprecation_path,self.deprecation)
    self.assert_invalid(self.run_set([self.adoption_path,self.deprecation_path]))
AdoptionContractTests.test_no_second_adoption_same_workflow_version=_same_version_new_bytes

if __name__ == "__main__":
    unittest.main()
