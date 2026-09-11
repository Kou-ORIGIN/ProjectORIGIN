#!/usr/bin/env python3
"""Read-only validator for ProjectORIGIN workflow definitions.

Results are validator execution results, not ProjectORIGIN Audit Results,
Human decisions, Rights decisions, workflow statuses, or publication statuses.
When Draft 2020-12 validation is unavailable, successful remaining layers produce
VALIDATION_LIMITED and exit code 3, never an unqualified full PASS.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import subprocess
from datetime import datetime
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


EXPECTED_IDENTITY = {
    "definition_type": "CASE_PRODUCTION_WORKFLOW",
    "workflow_id": "PROJECTORIGIN-CASE-PRODUCTION-WORKFLOW",
    "definition_format_version": "v1.0",
    "entry_step": "CPW-001",
    "terminal_step": "CPW-029",
}
EXPECTED_CPW = [f"CPW-{number:03d}" for number in range(1, 30)]
EXPECTED_RIGHTS = [f"RIGHTS-{number:02d}" for number in range(1, 11)]
EXPECTED_DELIVERY = [f"DELIVERY-{number:02d}" for number in range(1, 6)]
EXPECTED_GOVERNANCE = {
    "AGENTS.md": "v1.2",
    "docs/Image Rule.md": "v1.3",
    "docs/ProjectORIGIN Repository Rule.md": "v1.2",
    "docs/Audit Rule.md": "v1.4.0",
    "docs/ProjectORIGIN Publication Bible.md": "v1.1",
    "docs/Operating Manual.md": "v1.2",
    "docs/Case File Template.md": "v1.0.1",
    "docs/Database Rule.md": "v3.0",
    "docs/Database Schema.md": "v1.3",
}
EXPECTED_GATE_DECISIONS = {
    "CPW-015": [
        "FREE_HUMAN_READ_REVIEW_COMPLETE",
        "FREE_HUMAN_READ_REVIEW_REVISION_REQUESTED",
    ],
    "CPW-018": [
        "CLASSIFIED_HUMAN_READ_REVIEW_COMPLETE",
        "CLASSIFIED_HUMAN_READ_REVIEW_REVISION_REQUESTED",
    ],
    "CPW-023": [
        "HUMAN_VISUAL_REVIEW_COMPLETE",
        "HUMAN_VISUAL_REVIEW_REVISION_REQUESTED",
    ],
    "RIGHTS-04": ["HUMAN_SEND_CONFIRMED"],
    "RIGHTS-08": ["HUMAN_RIGHTS_INTERPRETATION_RECORDED"],
}
LEGACY_GATE_DECISIONS = {
    "FREE_HUMAN_READ_REVIEW_COMPLETED",
    "CLASSIFIED_HUMAN_READ_REVIEW_COMPLETED",
    "HUMAN_VISUAL_REVIEW_COMPLETED",
    "SEND_AUTHORIZED",
    "RIGHTS_INTERPRETATION_RECORDED",
}
DOMAIN_RESULT_KINDS = {
    "AUDIT_RESULT",
    "RIGHTS_RESULT",
    "HUMAN_READ_REVIEW_RESULT",
    "HUMAN_VISUAL_REVIEW_RESULT",
    "HUMAN_APPROVAL_DECISION",
    "REPOSITORY_INTEGRATION_RESULT",
    "PUBLICATION_COMPLETION",
    "PUBLICATION_STATUS",
}
PERMITTED_CYCLE_KINDS = {"REVISION", "RE_AUDIT", "ALTERNATIVE_SOURCE", "EXTERNAL_WAIT_RESUME", "RETURN"}


class DuplicateKeyError(ValueError):
    pass


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate object key: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not permitted")
    text = raw.decode("utf-8", errors="strict")
    value = json.loads(text, object_pairs_hook=_strict_object)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value, raw


def finding(layer: str, code: str, message: str, path: str | None = None) -> dict[str, str]:
    item = {"layer": layer, "id": code, "message": message}
    if path:
        item["path"] = path
    return item


def _step_map(definition: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        step.get("id"): step
        for step in definition.get("steps", [])
        if isinstance(step, dict) and isinstance(step.get("id"), str)
    }


def _substate_map(definition: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for step in definition.get("steps", []):
        if isinstance(step, dict):
            for state in step.get("substates", []):
                if isinstance(state, dict) and isinstance(state.get("id"), str):
                    result[state["id"]] = state
    return result


def _all_routes(definition: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any], bool]]:
    for step in definition.get("steps", []):
        if not isinstance(step, dict):
            continue
        owner = str(step.get("id", "<unknown>"))
        for field in ("routing", "failure_routing"):
            for route in step.get(field, {}).get("routes", []):
                if isinstance(route, dict):
                    yield owner, route, True
        audit = step.get("audit_applicability")
        if isinstance(audit, dict):
            for field in ("on_pass", "on_revision_required", "on_blocked"):
                route = audit.get(field)
                if isinstance(route, dict):
                    yield owner, route, True
        gate = step.get("human_gate")
        if isinstance(gate, dict) and isinstance(gate.get("resume_rule"), dict):
            yield owner, gate["resume_rule"], True
        for state in step.get("substates", []):
            if not isinstance(state, dict):
                continue
            sub_owner = str(state.get("id", owner))
            for route in state.get("routing", {}).get("routes", []):
                if isinstance(route, dict):
                    yield sub_owner, route, False
            sub_gate = state.get("human_gate")
            if isinstance(sub_gate, dict) and isinstance(sub_gate.get("resume_rule"), dict):
                yield sub_owner, sub_gate["resume_rule"], False
            wait = state.get("external_dependency")
            if isinstance(wait, dict) and isinstance(wait.get("fallback_route"), dict):
                yield sub_owner, wait["fallback_route"], False


def _has_route(step: dict[str, Any], target: str, kind: str | None = None, condition: str | None = None) -> bool:
    routes = list(step.get("routing", {}).get("routes", [])) + list(step.get("failure_routing", {}).get("routes", []))
    for route in routes:
        if route.get("target") != target:
            continue
        if kind is not None and route.get("route_kind") != kind:
            continue
        if condition is not None and route.get("condition_ref") != condition:
            continue
        return True
    return False


def validate_identity(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    for key, expected in EXPECTED_IDENTITY.items():
        if definition.get(key) != expected:
            errors.append(finding("SEMANTIC_VALIDATION", "IDENTITY-MISMATCH", f"{key} must equal {expected!r}", key))
    if definition.get("title") != "ProjectORIGIN Case Production Workflow":
        errors.append(finding("SEMANTIC_VALIDATION", "IDENTITY-TITLE", "unexpected workflow title", "title"))
    if definition.get("status") not in {"PROPOSED", "ADOPTED"}:
        errors.append(finding("SEMANTIC_VALIDATION", "IDENTITY-STATUS", "status must be PROPOSED or ADOPTED", "status"))
    if not re.fullmatch(r"v[1-9][0-9]*\.(0|[1-9][0-9]*)", str(definition.get("workflow_version", ""))):
        errors.append(finding("SEMANTIC_VALIDATION", "IDENTITY-VERSION", "workflow_version must use canonical vMAJOR.MINOR"))
    return errors


def validate_cpw(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    steps = definition.get("steps")
    if not isinstance(steps, list):
        return [finding("SEMANTIC_VALIDATION", "GRAPH-STEPS-TYPE", "steps must be an array", "steps")]
    ids = [step.get("id") if isinstance(step, dict) else None for step in steps]
    if len(ids) != 29:
        errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-STEP-COUNT", "exactly 29 top-level steps are required", "steps"))
    if len(ids) != len(set(ids)):
        errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-DUPLICATE-STEP", "duplicate top-level CPW ID"))
    if ids != EXPECTED_CPW:
        errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-CPW-SET-ORDER", "CPW IDs must be the exact ordered set CPW-001 through CPW-029", "steps"))
    return errors


def validate_routes_and_graph(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    steps = _step_map(definition)
    graph: dict[str, list[tuple[str, str, dict[str, Any]]]] = defaultdict(list)
    for owner, route, top_level in _all_routes(definition):
        kind = route.get("route_kind")
        target = route.get("target")
        if kind == "HOLD":
            errors.append(finding("SEMANTIC_VALIDATION", "FINAL-FLOW-HOLD-ROUTE", "HOLD is not a permitted route kind", owner))
        if target is not None and target not in steps:
            errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-UNKNOWN-TARGET", f"unknown route target {target!r}", owner))
        if top_level and owner in steps and target in steps:
            graph[owner].append((target, str(kind), route))

    if not errors and "CPW-001" in steps:
        reached = {"CPW-001"}
        queue = deque(["CPW-001"])
        while queue:
            current = queue.popleft()
            for target, _, _ in graph.get(current, []):
                if target not in reached:
                    reached.add(target)
                    queue.append(target)
        missing = [step for step in EXPECTED_CPW if step not in reached]
        if missing:
            errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-UNREACHABLE", f"unreachable mandatory steps: {', '.join(missing)}"))

        reverse: dict[str, list[str]] = defaultdict(list)
        for source, edges in graph.items():
            for target, _, _ in edges:
                reverse[target].append(source)
        can_finish = {"CPW-029"}
        queue = deque(["CPW-029"])
        while queue:
            current = queue.popleft()
            for source in reverse.get(current, []):
                if source not in can_finish:
                    can_finish.add(source)
                    queue.append(source)
        stranded = [step for step in EXPECTED_CPW if step not in can_finish]
        if stranded:
            errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-NO-DOWNSTREAM", f"steps lack a route to CPW-029: {', '.join(stranded)}"))

    step_order = {step_id: position for position, step_id in enumerate(EXPECTED_CPW)}

    def can_reach(start: str, destination: str) -> bool:
        pending = [start]
        visited: set[str] = set()
        while pending:
            current = pending.pop()
            if current == destination:
                return True
            if current in visited:
                continue
            visited.add(current)
            pending.extend(target for target, _, _ in graph.get(current, []))
        return False

    for source, edges in graph.items():
        for target, kind, route in edges:
            participates_in_cycle = target == source or can_reach(target, source)
            closes_cycle = participates_in_cycle and step_order.get(target, -1) <= step_order.get(source, -1)
            if closes_cycle and kind not in PERMITTED_CYCLE_KINDS:
                errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-INVALID-CYCLE", f"cycle-closing edge {source} -> {target} uses unpermitted kind {kind}", source))
            if participates_in_cycle and kind in PERMITTED_CYCLE_KINDS and not any(
                route.get(field) for field in ("condition_ref", "result_ref", "resume_rule")
            ):
                errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-CYCLE-UNGUARDED", f"cyclic {kind} route lacks a structured condition, result, or resume guard", source))

    # Tarjan SCC analysis verifies that every actual cyclic component has a
    # usable modeled exit. Guard validation above applies to the backward/self
    # edge that closes a cycle; ordinary forward edges inside an SCC need not
    # themselves carry revision guards.
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    components: list[set[str]] = []

    def strongconnect(node: str) -> None:
        nonlocal index
        indices[node] = lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target, _, _ in graph.get(node, []):
            if target not in indices:
                strongconnect(target)
                lowlink[node] = min(lowlink[node], lowlink[target])
            elif target in on_stack:
                lowlink[node] = min(lowlink[node], indices[target])
        if lowlink[node] == indices[node]:
            component: set[str] = set()
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.add(member)
                if member == node:
                    break
            components.append(component)

    for node in steps:
        if node not in indices:
            strongconnect(node)
    for component in components:
        has_self_loop = any(target == source for source in component for target, _, _ in graph.get(source, []))
        if len(component) == 1 and not has_self_loop:
            continue
        has_target_exit = any(target not in component for source in component for target, _, _ in graph.get(source, []))
        has_block_exit = any(
            route.get("route_kind") == "BLOCK" and route.get("blocking_ref")
            for owner, route, top_level in _all_routes(definition)
            if top_level and owner in component
        )
        if not has_target_exit and not has_block_exit:
            errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-CYCLE-NO-EXIT", f"cyclic component has no usable exit: {', '.join(sorted(component))}"))

    incoming_029 = [(source, kind) for source, edges in graph.items() for target, kind, _ in edges if target == "CPW-029"]
    if not incoming_029 or any(source != "CPW-028" for source, _ in incoming_029):
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-CPW028-BYPASS", "CPW-029 may be entered only from CPW-028"))

    required_links = [
        ("CPW-013", "CPW-014"), ("CPW-014", "CPW-015"), ("CPW-015", "CPW-027"),
        ("CPW-016", "CPW-017"), ("CPW-017", "CPW-018"), ("CPW-018", "CPW-027"),
    ]
    for source, target in required_links:
        if source not in steps or not _has_route(steps[source], target):
            errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-BRANCH-LINK", f"required branch link {source} -> {target} is absent"))
    for source in ("CPW-013", "CPW-014", "CPW-016", "CPW-017"):
        if any(target == "CPW-027" for target, _, _ in graph.get(source, [])):
            errors.append(finding("SEMANTIC_VALIDATION", "GRAPH-BRANCH-JOIN-BYPASS", f"{source} bypasses its required audit or review before CPW-027"))
    return errors


def validate_gate(gate: Any, gate_id: str, expected_type: str, decisions: list[str]) -> list[dict[str, str]]:
    errors = []
    if not isinstance(gate, dict):
        return [finding("SEMANTIC_VALIDATION", "HUMAN-GATE-MISSING", "required Human Gate is absent", gate_id)]
    if gate.get("gate_type") != expected_type:
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-TYPE", f"expected gate type {expected_type}", gate_id))
    if gate.get("gate_required") is not True:
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-NOT-REQUIRED", "gate_required must be true", gate_id))
    if gate.get("automatic_crossing_prohibited") is not True:
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-AUTO-CROSS", "automatic Human Gate crossing must be prohibited", gate_id))
    if gate.get("allowed_decisions") != decisions:
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-DECISIONS", f"allowed decisions must equal {decisions!r}", gate_id))
    decision_source = gate.get("decision_source")
    if not isinstance(decision_source, dict) or decision_source.get("authoritative") is not True:
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-DECISION-SOURCE", "decision source must be an authoritative reference", gate_id))
    return errors


def validate_human_gates(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    steps, substates = _step_map(definition), _substate_map(definition)
    expected_types = {
        "CPW-015": "FREE_HUMAN_READ_REVIEW",
        "CPW-018": "CLASSIFIED_HUMAN_READ_REVIEW",
        "CPW-023": "HUMAN_VISUAL_REVIEW",
        "RIGHTS-04": "RIGHTS_INQUIRY_SEND",
        "RIGHTS-08": "RIGHTS_BINDING_INTERPRETATION",
    }
    for gate_id, decisions in EXPECTED_GATE_DECISIONS.items():
        owner = steps.get(gate_id) or substates.get(gate_id)
        if owner is None:
            errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-OWNER-MISSING", "gate owner step/substate is absent", gate_id))
        else:
            errors.extend(validate_gate(owner.get("human_gate"), gate_id, expected_types[gate_id], decisions))

    for value in _walk_strings(definition):
        if value in LEGACY_GATE_DECISIONS:
            errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-LEGACY-DECISION", f"legacy decision token {value!r} is prohibited"))

    cpw23 = steps.get("CPW-023", {})
    if cpw23.get("automation_classification") != "CONDITIONAL":
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-VISUAL-CONDITIONALITY", "CPW-023 must remain CONDITIONAL"))
    if "NOT_APPLICABLE" in cpw23.get("human_gate", {}).get("allowed_decisions", []):
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-APPLICABILITY-AS-DECISION", "non-applicability is not a Human decision"))

    cpw28 = steps.get("CPW-028", {})
    errors.extend(validate_gate(cpw28.get("human_gate"), "CPW-028", "FINAL_HUMAN_APPROVAL", ["APPROVED"]))
    for route in cpw28.get("routing", {}).get("routes", []):
        if route.get("target") == "CPW-029":
            if route.get("route_kind") != "HUMAN_GATE_RESUME" or route.get("result_ref") != "final-human-approval-decision":
                errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-AUTO-APPROVAL", "CPW-029 entry must use the authoritative Human Gate resume decision"))
    if not any(ref.get("ref_id") == "final-human-approval-decision" for ref in steps.get("CPW-029", {}).get("inputs", []) if isinstance(ref, dict)):
        errors.append(finding("SEMANTIC_VALIDATION", "HUMAN-GATE-DELIVERY-DEPENDENCY", "CPW-029 must depend on final Human Approval evidence"))
    return errors


def _walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)


def validate_rights(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    steps = _step_map(definition)
    cpw21 = steps.get("CPW-021", {})
    substates = cpw21.get("substates", [])
    ids = [state.get("id") for state in substates if isinstance(state, dict)]
    if ids != EXPECTED_RIGHTS:
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-SET-ORDER", "RIGHTS substates must be the exact ordered set RIGHTS-01 through RIGHTS-10"))
        return errors
    states = {state["id"]: state for state in substates}
    wait = states["RIGHTS-05"].get("external_dependency")
    if not isinstance(wait, dict):
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-WAIT-MISSING", "RIGHTS-05 External Wait is absent"))
    else:
        if wait.get("resumable") is not True:
            errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-WAIT-NOT-RESUMABLE", "RIGHTS-05 must be resumable"))
        if wait.get("silence_is_permission") is not False:
            errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-SILENCE-PERMISSION", "silence cannot establish permission"))
        if wait.get("timeout_is_rejection") is not False:
            errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-TIMEOUT-REJECTION", "timeout cannot establish rejection"))

    send_resume = states["RIGHTS-04"].get("human_gate", {}).get("resume_rule", {})
    if send_resume.get("target") != "CPW-021" or send_resume.get("condition_ref") != "HUMAN_SEND_CONFIRMED_AND_DISPATCH_EVIDENCE_REFERENCED":
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-SEND-EVIDENCE", "RIGHTS-05 entry requires Human Send Confirmation and dispatch evidence"))
    draft_routes = states["RIGHTS-03"].get("routing", {}).get("routes", [])
    if any(route.get("target") == "CPW-021" and "RIGHTS-05" in str(route) for route in draft_routes if isinstance(route, dict)):
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-DRAFT-TO-WAIT", "Inquiry Draft completion cannot enter RIGHTS-05"))

    permission_results = {"PERMISSION", "RIGHTS_PERMISSION", "RIGHTS_VERIFIED", "FINAL_HUMAN_APPROVAL", "HUMAN_APPROVAL_DECISION"}
    response = states["RIGHTS-06"]
    if response.get("name") != "Response Evidence Capture" or any(
        reference.get("result_kind") in permission_results
        for reference in response.get("source_of_truth", [])
        if isinstance(reference, dict)
    ) or any(route.get("target") in {"CPW-022", "CPW-028", "CPW-029"} for route in response.get("routing", {}).get("routes", []) if isinstance(route, dict)):
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-RESPONSE-AS-PERMISSION", "RIGHTS-06 may capture response evidence but cannot establish permission, Rights Verification, or Human Approval"))

    extraction = states["RIGHTS-07"]
    extraction_prohibited = permission_results | {"HUMAN_CONSENT", "HUMAN_DECISION"}
    if extraction.get("name") != "AI-Assisted Factual Extraction" or "human_gate" in extraction or any(
        reference.get("result_kind") in extraction_prohibited or reference.get("source_type") in {"HUMAN_DECISION_RECORD", "HUMAN_CONSENT_RECORD"}
        for reference in extraction.get("source_of_truth", [])
        if isinstance(reference, dict)
    ) or any(route.get("target") in {"CPW-022", "CPW-028", "CPW-029"} for route in extraction.get("routing", {}).get("routes", []) if isinstance(route, dict)):
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-AI-AS-HUMAN-CONSENT", "RIGHTS-07 AI extraction cannot establish Human consent, binding interpretation, permission, Rights Verification, or Human Approval"))

    interpretation = states["RIGHTS-08"].get("human_gate", {}).get("resume_rule", {})
    if interpretation.get("target") != "CPW-021" or interpretation.get("condition_ref") != "HUMAN_RIGHTS_INTERPRETATION_RECORDED":
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-INTERPRETATION-BOUNDARY", "Human interpretation must route to RIGHTS-09 without establishing permission or Rights Verification"))

    for state_id in ("RIGHTS-09", "RIGHTS-10"):
        state = states[state_id]
        if state.get("human_gate", {}).get("gate_type") == "FINAL_HUMAN_APPROVAL" or any(
            route.get("target") in {"CPW-028", "CPW-029"}
            for route in state.get("routing", {}).get("routes", [])
            if isinstance(route, dict)
        ) or any(
            reference.get("result_kind") in {"FINAL_HUMAN_APPROVAL", "HUMAN_APPROVAL_DECISION"}
            or reference.get("source_type") in {"HUMAN_APPROVAL_DECISION_RECORD", "HUMAN_DECISION_RECORD"}
            for reference in state.get("source_of_truth", [])
            if isinstance(reference, dict)
        ):
            errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-VERIFICATION-AS-HUMAN-APPROVAL", f"{state_id} cannot establish or route directly to Final Human Approval"))
    allowed_rights10 = {
        ("CONDITIONAL", "CPW-022"),
        ("ALTERNATIVE_SOURCE", "CPW-020"),
        ("BLOCK", None),
    }
    if any((route.get("route_kind"), route.get("target")) not in allowed_rights10 for route in states["RIGHTS-10"].get("routing", {}).get("routes", []) if isinstance(route, dict)):
        errors.append(finding("SEMANTIC_VALIDATION", "RIGHTS-10-ROUTING", "RIGHTS-10 may route only to Continue, Stop, or Alternative Source handling"))
    return errors


def validate_image_and_final_flow(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    steps = _step_map(definition)
    cpw25 = steps.get("CPW-025", {})
    outputs = {item.get("ref_id"): item for item in cpw25.get("outputs", []) if isinstance(item, dict)}
    mechanical = outputs.get("registration-mechanical-validation", {})
    formal = outputs.get("registration-verification-audit", {})
    if mechanical.get("required") is not True or mechanical.get("applicability") != "REQUIRED":
        errors.append(finding("SEMANTIC_VALIDATION", "IMAGE-MECHANICAL-REQUIRED", "mechanical registration validation must be required"))
    if formal.get("required") is not False or formal.get("applicability") != "CONDITIONAL":
        errors.append(finding("SEMANTIC_VALIDATION", "IMAGE-FORMAL-AUDIT-CONDITIONAL", "Formal Registration Verification Audit must be conditional"))
    audit = cpw25.get("audit_applicability", {})
    if audit.get("audit_category") != "FORMAL_AUDIT" or audit.get("audit_required") is not False:
        errors.append(finding("SEMANTIC_VALIDATION", "IMAGE-VALIDATION-AUDIT-ALIAS", "mechanical validation and conditional Formal Audit must remain distinct"))
    prohibited_registration_results = {"HUMAN_APPROVAL_DECISION", "REPOSITORY_INTEGRATION_RESULT", "PUBLICATION_COMPLETION", "PUBLICATION_STATUS"}
    if any(
        reference.get("result_kind") in prohibited_registration_results
        for reference in cpw25.get("source_of_truth", [])
        if isinstance(reference, dict)
    ):
        errors.append(finding("SEMANTIC_VALIDATION", "IMAGE-REGISTRATION-DOWNSTREAM-INFERENCE", "registration cannot establish Human Approval, Repository Integration, or Publication"))

    impact = steps.get("CPW-026", {}).get("change_impact", {})
    required_impacts = {"AUDIT", "HUMAN_READ_REVIEW", "HUMAN_VISUAL_REVIEW", "PLACEMENT", "HUMAN_REVIEW_PACKAGE"}
    if impact.get("automatic_global_invalidation") is not False:
        errors.append(finding("SEMANTIC_VALIDATION", "IMAGE-AUTOMATIC-GLOBAL-INVALIDATION", "automatic global invalidation must be false"))
    if set(impact.get("possible_impacts", [])) != required_impacts:
        errors.append(finding("SEMANTIC_VALIDATION", "IMAGE-IMPACT-SET", "CPW-026 possible impact set is incomplete or expanded"))

    cpw27 = steps.get("CPW-027", {})
    allowed_failure = {"REVISION", "RE_AUDIT", "BLOCK"}
    for route in cpw27.get("failure_routing", {}).get("routes", []):
        if route.get("route_kind") not in allowed_failure:
            errors.append(finding("SEMANTIC_VALIDATION", "FINAL-FLOW-FAILURE-ROUTE", "Final Flow failure may route only through revision, re-audit, or block handling"))
    return errors


def validate_publication(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    cpw29 = _step_map(definition).get("CPW-029", {})
    states = cpw29.get("substates", [])
    ids = [state.get("id") for state in states if isinstance(state, dict)]
    if ids != EXPECTED_DELIVERY:
        errors.append(finding("SEMANTIC_VALIDATION", "PUBLICATION-SET-ORDER", "DELIVERY substates must be the exact ordered set DELIVERY-01 through DELIVERY-05"))
        return errors
    by_id = {state["id"]: state for state in states}
    prohibited_by_state = {
        "DELIVERY-01": {"PUBLICATION_COMPLETION", "PUBLICATION_STATUS"},
        "DELIVERY-02": {"PUBLICATION_COMPLETION", "PUBLICATION_STATUS"},
        "DELIVERY-03": {"PUBLICATION_STATUS"},
        "DELIVERY-05": {"PUBLICATION_COMPLETION", "PUBLICATION_STATUS"},
    }
    for state_id, prohibited in prohibited_by_state.items():
        sources = by_id[state_id].get("source_of_truth", [])
        if any(item.get("result_kind") in prohibited for item in sources if isinstance(item, dict)):
            errors.append(finding("SEMANTIC_VALIDATION", "PUBLICATION-STATE-INFERENCE", f"{state_id} collapses a later Publication responsibility"))
    tracking_sources = by_id["DELIVERY-05"].get("source_of_truth", [])
    if any(item.get("result_kind") in {"PUBLICATION_COMPLETION", "PUBLICATION_STATUS"} for item in tracking_sources if isinstance(item, dict)):
        errors.append(finding("SEMANTIC_VALIDATION", "PUBLICATION-TRACKING-AS-EVIDENCE", "publication tracking cannot establish evidence or Publication Status"))
    expected_names = {
        "DELIVERY-01": "Publication Artifact Repository Integration",
        "DELIVERY-02": "Publication Execution",
        "DELIVERY-03": "Publication Completion Evidence Capture",
        "DELIVERY-04": "Publication Status Establishment",
        "DELIVERY-05": "publication-tracking update",
    }
    for state_id, name in expected_names.items():
        if by_id[state_id].get("name") != name:
            errors.append(finding("SEMANTIC_VALIDATION", "PUBLICATION-STATE-COLLAPSE", f"{state_id} identity/name changed"))
    return errors


def validate_boundaries(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors = []
    vocab = definition.get("controlled_vocabularies", {})
    if "FULLY_AUTOMATABLE" in vocab.get("automation_classification", []):
        errors.append(finding("SEMANTIC_VALIDATION", "IDENTITY-FULLY-AUTOMATABLE", "FULLY_AUTOMATABLE is prohibited"))
    if "HOLD" in vocab.get("route_kinds", []):
        errors.append(finding("SEMANTIC_VALIDATION", "FINAL-FLOW-HOLD-ROUTE", "HOLD route kind is prohibited"))
    for key in ("sha256", "workflow_sha256", "definition_sha256", "self_hash"):
        if key in definition:
            errors.append(finding("SEMANTIC_VALIDATION", "IDENTITY-SELF-HASH", "Workflow Definition cannot contain its own authoritative hash", key))
    for step in definition.get("steps", []):
        for reference in step.get("source_of_truth", []) if isinstance(step, dict) else []:
            if not isinstance(reference, dict):
                continue
            if reference.get("read_mode") != "REFERENCE_ONLY" or reference.get("cache_is_authoritative") is not False:
                errors.append(finding("SEMANTIC_VALIDATION", "SOURCE-AUTHORITY-BOUNDARY", "Source-of-Truth declarations must remain reference-only and non-authoritative", str(step.get("id"))))
            if reference.get("result_kind") in DOMAIN_RESULT_KINDS and reference.get("source_type") in {"ORCHESTRATION_MANIFEST", "PUBLICATION_TRACKING_RECORD", "VALIDATOR_RESULT", "HUMAN_REVIEW_PACKAGE"}:
                errors.append(finding("SEMANTIC_VALIDATION", "SOURCE-DOMAIN-INFERENCE", "manifest, tracking, or validator output cannot establish a domain result", str(step.get("id"))))
    interfaces = definition.get("interfaces", {})
    package = interfaces.get("human_review_package", {})
    manifest = interfaces.get("orchestration_manifest", {})
    interface_values = [value for value in interfaces.values() if isinstance(value, dict)] if isinstance(interfaces, dict) else []
    manifest_count = sum(
        value.get("artifact_type") == "ORCHESTRATION_MANIFEST"
        or value.get("path_pattern") == "cases/FILE-XXXX/orchestration-manifest.json"
        for value in interface_values
    )
    package_count = sum(
        value.get("artifact_type") == "HUMAN_REVIEW_PACKAGE"
        or value.get("path_pattern") == "cases/FILE-XXXX/human-review-package_v<version>.json"
        for value in interface_values
    )
    expected_manifest = {
        "interface_id": "ORCHESTRATION_MANIFEST_V1",
        "artifact_type": "ORCHESTRATION_MANIFEST",
        "path_pattern": "cases/FILE-XXXX/orchestration-manifest.json",
        "direction": "REFERENCE_ONLY",
        "required_fields": {"manifest_version", "case_id", "workflow_binding", "execution_cursor"},
        "format_binding": {"field": "manifest_version", "value": "v1.0"},
    }
    if manifest_count != 1 or any(manifest.get(key) != value for key, value in expected_manifest.items() if key not in {"required_fields", "format_binding"}) or set(manifest.get("required_fields", [])) != expected_manifest["required_fields"]:
        errors.append(finding("SEMANTIC_VALIDATION", "SOURCE-MANIFEST-BOUNDARY", "Orchestration Manifest must remain a non-authoritative interface"))
    if manifest.get("format_binding") != expected_manifest["format_binding"]:
        errors.append(finding("SEMANTIC_VALIDATION", "BOUNDARY-MANIFEST-FORMAT-BINDING", "Orchestration Manifest format binding must identify manifest_version v1.0"))
    expected_package = {
        "interface_id": "HUMAN_REVIEW_PACKAGE",
        "artifact_type": "HUMAN_REVIEW_PACKAGE",
        "path_pattern": "cases/FILE-XXXX/human-review-package_v<version>.json",
        "direction": "REFERENCE_ONLY",
        "required_fields": {"case identity", "artifact identity and version references", "applicable audit references", "open issue or HOLD references when applicable"},
        "snapshot_contract": {
            "reference_only": True,
            "version_bound": True,
            "immutable": True,
            "material_change_requires_new_version": True,
        },
    }
    if package_count != 1 or any(package.get(key) != value for key, value in expected_package.items() if key not in {"required_fields", "snapshot_contract"}) or set(package.get("required_fields", [])) != expected_package["required_fields"]:
        errors.append(finding("SEMANTIC_VALIDATION", "SOURCE-REVIEW-PACKAGE-BOUNDARY", "Human Review Package structured interface contract is invalid"))
    if package.get("snapshot_contract") != expected_package["snapshot_contract"]:
        errors.append(finding("SEMANTIC_VALIDATION", "BOUNDARY-HRP-SNAPSHOT-CONTRACT", "Human Review Package snapshot contract must contain the four approved true properties"))

    for step in definition.get("steps", []):
        candidates = [step] + list(step.get("substates", [])) if isinstance(step, dict) else []
        for owner in candidates:
            for reference in owner.get("source_of_truth", []) if isinstance(owner, dict) else []:
                if not isinstance(reference, dict):
                    continue
                source_type = reference.get("source_type")
                result_kind = reference.get("result_kind")
                if source_type == "ORCHESTRATION_MANIFEST" and result_kind in DOMAIN_RESULT_KINDS:
                    errors.append(finding("SEMANTIC_VALIDATION", "BOUNDARY-MANIFEST-AUTHORITY", "Manifest cannot establish an authoritative domain result", str(owner.get("id"))))
                if source_type == "HUMAN_REVIEW_PACKAGE" and result_kind in {
                    "HUMAN_APPROVAL_DECISION", "REPOSITORY_INTEGRATION_RESULT", "PUBLICATION_COMPLETION", "PUBLICATION_STATUS"
                }:
                    errors.append(finding("SEMANTIC_VALIDATION", "BOUNDARY-HRP-AUTHORITY", "Human Review Package cannot establish approval, integration, or publication", str(owner.get("id"))))
            gate = owner.get("human_gate") if isinstance(owner, dict) else None
            source_type = gate.get("decision_source", {}).get("reference", {}).get("artifact_type") if isinstance(gate, dict) else None
            if source_type == "ORCHESTRATION_MANIFEST":
                errors.append(finding("SEMANTIC_VALIDATION", "BOUNDARY-MANIFEST-AUTHORITY", "Manifest cannot be an authoritative Human Gate decision source", str(owner.get("id"))))
            if source_type == "HUMAN_REVIEW_PACKAGE":
                errors.append(finding("SEMANTIC_VALIDATION", "BOUNDARY-HUMAN-REVIEW-PACKAGE-AUTHORITY", "Human Review Package existence cannot be an authoritative Human Gate decision source", str(owner.get("id"))))
    return errors


def validate_semantics(definition: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for check in (
        validate_identity,
        validate_cpw,
        validate_routes_and_graph,
        validate_human_gates,
        validate_rights,
        validate_image_and_final_flow,
        validate_publication,
        validate_boundaries,
    ):
        errors.extend(check(definition))
    return errors


def _observe_version(path: str, text: str) -> str | None:
    patterns = {
        "AGENTS.md": r"\*\*Current Official Version:\*\*\s*(v\d+(?:\.\d+)*)",
        "docs/ProjectORIGIN Repository Rule.md": r"\*\*Current Official Version:\*\*\s*(v\d+(?:\.\d+)*)",
        "docs/ProjectORIGIN Publication Bible.md": r"Current Official Version Identity:\s*(v\d+(?:\.\d+)*)",
        "docs/Case File Template.md": r"\*\*Version:\*\*\s*(v\d+(?:\.\d+)*)",
    }
    pattern = patterns.get(path)
    if pattern is None:
        return None
    match = re.search(pattern, text)
    return match.group(1) if match else None


def validate_governance(definition: dict[str, Any], repository_root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    errors, warnings = [], []
    declarations = definition.get("applicable_governance", [])
    observed: dict[str, str] = {}
    authority_ids: list[str] = []
    for item in declarations:
        if not isinstance(item, dict):
            errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-ENTRY-TYPE", "Governance entry must be an object"))
            continue
        path = item.get("document")
        version = item.get("version")
        authority_ids.append(str(item.get("authority_id")))
        if isinstance(path, str) and isinstance(version, str):
            if path in observed:
                errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-DUPLICATE", f"duplicate Governance document declaration: {path}"))
            observed[path] = version
    if len(authority_ids) != len(set(authority_ids)):
        errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-DUPLICATE-AUTHORITY", "duplicate Governance authority_id"))
    if observed != EXPECTED_GOVERNANCE:
        missing = sorted(set(EXPECTED_GOVERNANCE) - set(observed))
        extra = sorted(set(observed) - set(EXPECTED_GOVERNANCE))
        mismatch = sorted(path for path in set(observed) & set(EXPECTED_GOVERNANCE) if observed[path] != EXPECTED_GOVERNANCE[path])
        errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-DECLARATION-MISMATCH", f"missing={missing}; extra={extra}; version_mismatch={mismatch}"))
    for path, expected in EXPECTED_GOVERNANCE.items():
        candidate = repository_root / path
        if not candidate.is_file():
            errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-FILE-MISSING", f"required Governance file is absent: {path}"))
            continue
        text = candidate.read_text(encoding="utf-8")
        actual = _observe_version(path, text)
        if actual is None:
            warnings.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-VERSION-UNDETERMINED", f"VERSION OBSERVATION UNDETERMINED for {path}"))
        elif actual != expected:
            errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-VERSION-MISMATCH", f"{path}: declared {expected}, observed {actual}"))
    for warning in warnings:
        warning["blocking"] = False
    return errors, warnings


def validate_schema_optional(schema: dict[str, Any], definition: dict[str, Any]) -> tuple[str, list[dict[str, str]], list[dict[str, str]]]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return "UNAVAILABLE", [], [finding("SCHEMA_VALIDATION", "SCHEMA-CAPABILITY-UNAVAILABLE", "Python jsonschema Draft 2020-12 validation is unavailable")]
    errors = []
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for error in sorted(validator.iter_errors(definition), key=lambda item: list(item.absolute_path)):
            location = "/".join(str(part) for part in error.absolute_path)
            errors.append(finding("SCHEMA_VALIDATION", "SCHEMA-DEFINITION-NONCONFORMANT", error.message, location or "$"))
    except Exception as exc:
        return "FAIL", [finding("SCHEMA_VALIDATION", "SCHEMA-TOOL-ERROR", str(exc))], []
    return ("FAIL" if errors else "PASS"), errors, []


def run_validation(schema_path: Path, definition_path: Path, repository_root: Path | None, check_governance: bool, records: list[Path] | None = None, prospective: bool = False) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    schema = definition = None
    definition_raw = b""
    json_result = "PASS"
    try:
        schema, _ = load_json_strict(schema_path)
    except OSError:
        raise
    except Exception as exc:
        json_result = "FAIL"
        errors.append(finding("JSON_INTEGRITY", "JSON-SCHEMA-LOAD", str(exc)))
    try:
        definition, definition_raw = load_json_strict(definition_path)
    except OSError:
        raise
    except Exception as exc:
        json_result = "FAIL"
        errors.append(finding("JSON_INTEGRITY", "JSON-DEFINITION-LOAD", str(exc)))

    schema_result = "UNAVAILABLE"
    semantic_result = "FAIL"
    governance_result = "NOT_CHECKED"
    if schema is not None and definition is not None:
        schema_result, schema_errors, schema_warnings = validate_schema_optional(schema, definition)
        errors.extend(schema_errors)
        warnings.extend(schema_warnings)
        semantic_errors = validate_semantics(definition)
        errors.extend(semantic_errors)
        semantic_result = "FAIL" if semantic_errors else "PASS"
        if check_governance:
            if repository_root is None:
                errors.append(finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-ROOT-REQUIRED", "--repository-root is required with --check-governance"))
                governance_result = "FAIL"
            else:
                gov_errors, gov_warnings = validate_governance(definition, repository_root)
                errors.extend(gov_errors)
                warnings.extend(gov_warnings)
                governance_result = "FAIL" if gov_errors else "PASS"

    cross_result = "NOT_CHECKED"
    if definition is not None and schema is not None:
        cross_errors, limited = validate_adoption_set(schema_path, definition_path, definition, repository_root, records or [], prospective)
        errors.extend(cross_errors)
        cross_result = "FAIL" if cross_errors else ("UNAVAILABLE" if limited else "PASS")
        if limited:
            warnings.append(finding("CROSS_ARTIFACT_VALIDATION", "ADOPTION-CAPABILITY-UNAVAILABLE", "Required Git or record-schema capability unavailable; adoption eligibility is not established"))
    if errors:
        result, exit_code = "FAIL", 1
    elif schema_result == "UNAVAILABLE" or cross_result == "UNAVAILABLE":
        result, exit_code = "VALIDATION_LIMITED", 3
    elif warnings:
        result, exit_code = "PASS_WITH_WARNINGS", 0
    else:
        result, exit_code = "PASS", 0
    identity = {}
    if isinstance(definition, dict):
        identity = {key: definition.get(key) for key in EXPECTED_IDENTITY}
        identity["title"] = definition.get("title")
        identity["workflow_version"] = definition.get("workflow_version")
    return {
        "validator_result": result,
        "validation_scope": "PROSPECTIVE_ADOPTED_BYTES_ONLY" if prospective else "CURRENT_EXPLICIT_RECORD_SET",
        "formal_adoption_executed": False,
        "record_scope": "Explicit supplied records and their reference closure only; no undisclosed-record uniqueness claim.",
        "exit_code": exit_code,
        "layers": {
            "CROSS_ARTIFACT_VALIDATION": cross_result,
            "JSON_INTEGRITY": json_result,
            "SCHEMA_VALIDATION": schema_result,
            "SEMANTIC_VALIDATION": semantic_result,
            "GOVERNANCE_COMPATIBILITY": governance_result,
        },
        "errors": errors,
        "warnings": warnings,
        "definition_identity": identity,
        "definition_sha256": hashlib.sha256(definition_raw).hexdigest() if definition_raw else None,
        "digest_status": "REPORT_ONLY",
    }



class AdoptionInvalid(ValueError):
    """Invalid evidence or cross-artifact set; never an authority decision."""


class AdoptionCapabilityUnavailable(Exception):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AdoptionInvalid(message)


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _relative(root: Path, value: str) -> Path:
    _require(isinstance(value, str) and bool(value), "empty reference path")
    _require(not value.startswith("/") and not re.match(r"^[A-Za-z]:", value) and "\\" not in value,
             "absolute or non-portable reference path")
    _require(all(part not in {"", ".", ".."} for part in value.split("/")), "traversal/noncanonical reference path")
    path = root / value
    _require(path.resolve().is_relative_to(root.resolve()), "reference escapes repository")
    return path


def _time(value: str) -> datetime:
    _require(bool(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value)), "timestamp must be UTC seconds")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


class AdoptionSet:
    """Explicit bounded read-only record closure. No latest-record selection or writes.

    The caller supplies all applicable records via --record. Referenced records
    are also followed. Duplicate checking covers this closure, not undisclosed
    records elsewhere. Human actor declarations are checked, never authenticated
    or invented by this mechanical validator.
    """
    TYPES = {
        "WORKFLOW_FORMAL_ADOPTION": ("workflow-adoption-decision", "decision_id"),
        "WORKFLOW_FORMAL_ADOPTION_RECORD": ("workflow-adoption-record", "adoption_record_id"),
        "WORKFLOW_DEPRECATION_RECORD": ("workflow-deprecation-record", "deprecation_record_id"),
    }

    def __init__(self, root: Path, schema_path: Path):
        self.root = root.resolve()
        self.schema_path = schema_path
        self.schema, _ = load_json_strict(schema_path)
        self.seen = {}
        self.loaded = {}
        self.visiting = set()
        self.validated = set()
        self.deprecated = {}
        self.adopted = {}

    def record(self, path: Path, expected_sha: str | None = None):
        path = path.resolve()
        _require(path.is_relative_to(self.root), "record escapes repository")
        data, raw = load_json_strict(path)
        if expected_sha is not None:
            _require(_sha(raw) == expected_sha, "record SHA mismatch")
        if path in self.loaded:
            return self.loaded[path]
        kind = data.get("record_type", data.get("decision_type"))
        _require(kind in self.TYPES, "unknown record type")
        name, idkey = self.TYPES[kind]
        schema, _ = load_json_strict(self.schema_path.parent / (name + ".schema.json"))
        status, errors, _ = validate_schema_optional(schema, data)
        if status == "UNAVAILABLE":
            raise AdoptionCapabilityUnavailable("Draft 2020-12 unavailable")
        _require(status == "PASS", "record schema: " + str(errors))
        identity = data[idkey]
        _require(identity not in self.seen or self.seen[identity] == path, "duplicate record ID: " + identity)
        self.seen[identity] = path
        self.loaded[path] = data
        return data

    def reference(self, path: str, digest: str):
        return self.record(_relative(self.root, path), digest)

    def definition_checks(self, data):
        status, errors, _ = validate_schema_optional(self.schema, data)
        if status == "UNAVAILABLE":
            raise AdoptionCapabilityUnavailable("Draft 2020-12 unavailable")
        _require(status == "PASS", "definition schema: " + str(errors))
        _require(not validate_semantics(data), "definition semantic validation failed")
        errors, _ = validate_governance(data, self.root)
        _require(not errors, "definition governance validation failed")

    def candidate(self, target):
        commit = target["candidate_git_commit_sha"]
        _require(bool(re.fullmatch("[0-9a-f]{40}", commit)), "full candidate Git SHA required")
        _relative(self.root, target["workflow_path"])
        try:
            kind = subprocess.run(["git", "-C", str(self.root), "cat-file", "-t", commit], capture_output=True, check=False)
            _require(kind.returncode == 0 and kind.stdout.strip() == b"commit", "candidate commit missing or not a commit")
            recovered = subprocess.run(["git", "-C", str(self.root), "show", commit + ":" + target["workflow_path"]], capture_output=True, check=False)
        except FileNotFoundError as exc:
            raise AdoptionCapabilityUnavailable("Git executable unavailable") from exc
        _require(recovered.returncode == 0, "candidate path missing at commit")
        _require(_sha(recovered.stdout) == target["candidate_definition_sha256"], "candidate Git bytes SHA mismatch")
        data = json.loads(recovered.stdout.decode("utf-8"), object_pairs_hook=_strict_object)
        _require(isinstance(data, dict) and data.get("status") == "PROPOSED", "Git candidate must be PROPOSED")
        for field in ("workflow_version", "definition_format_version"):
            _require(data.get(field) == target[field], "candidate " + field + " mismatch")
        self.definition_checks(data)
        return data

    def evidence(self, evidence, digest):
        _require(evidence is not None and evidence["definition_sha256"] == digest, "validation evidence candidate SHA mismatch")
        tests = evidence["tests"]
        _require(tests["total"] == tests["passed"], "not all applicable tests passed")
        warnings = evidence["warnings"]
        _require((evidence["result"] == "PASS" and not warnings) or
                 (evidence["result"] == "PASS_WITH_WARNINGS" and bool(warnings) and all(w["blocking"] is False for w in warnings)),
                 "result/warnings mismatch")
        # Exact required validation/governance artifacts; extras are also hash-checked.
        required = {"scripts/validate-workflow.py", "tests/workflows/test_validate_workflow.py"}
        required.update(EXPECTED_GOVERNANCE)
        required.update("schemas/workflows/" + n + ".schema.json" for n in
                        ["case-production-workflow-definition", "workflow-adoption-decision", "workflow-adoption-record", "workflow-deprecation-record"])
        paths = set()
        for artifact in evidence["controlled_artifacts"]:
            _require(artifact["path"] not in paths, "duplicate controlled evidence path")
            paths.add(artifact["path"])
            p = _relative(self.root, artifact["path"])
            _require(_sha(p.read_bytes()) == artifact["sha256"], "stale controlled validation artifact: " + artifact["path"])
        _require(required <= paths, "required controlled validation artifacts missing")

    def decision(self, data):
        candidate = self.candidate(data["target"])
        if data["decision_value"] == "AUTHORIZE_ADOPTION":
            self.evidence(data["validation_evidence"], data["target"]["candidate_definition_sha256"])
        elif data["validation_evidence"] is not None:
            self.evidence(data["validation_evidence"], data["target"]["candidate_definition_sha256"])
        _time(data["decided_at"])
        return candidate

    def adoption(self, data):
        identity = data["adoption_record_id"]
        _require(identity not in self.visiting, "supersession/adoption reference cycle")
        if identity in self.validated:
            return
        self.visiting.add(identity)
        target = data["target"]
        reference = data["human_decision"]
        decision = self.reference(reference["decision_path"], reference["decision_sha256"])
        _require(decision.get("decision_id") == reference["decision_id"], "Decision ID mismatch")
        _require(decision.get("decision_type") == "WORKFLOW_FORMAL_ADOPTION" and decision.get("decision_value") == "AUTHORIZE_ADOPTION", "Decision does not authorize adoption")
        _require(decision["target"] == {k: target[k] for k in decision["target"]}, "Decision / Adoption target mismatch")
        candidate = self.decision(decision)
        current, raw = load_json_strict(_relative(self.root, target["workflow_path"]))
        _require(_sha(raw) == target["adopted_definition_sha256"], "adopted workflow SHA mismatch")
        _require(current.get("status") == "ADOPTED", "completed record requires current ADOPTED workflow")
        prospective = dict(candidate, status="ADOPTED")
        _require(current == prospective, "unauthorized adoption delta; only /status may change")
        self.definition_checks(current)
        _require(_time(data["adopted_at"]) >= _time(decision["decided_at"]), "adoption precedes decision")
        self.evidence(data["adopted_state_validation_evidence"], _sha(raw))
        key = (current["workflow_id"], target["workflow_version"])
        _require(key not in self.adopted or self.adopted[key] == identity, "conflicting adoption records")
        self.adopted[key] = identity
        predecessor = current.get("supersedes")
        if predecessor:
            _require(predecessor["repository_path"] != target["workflow_path"], "self-supersession")
            self.adoption_reference(dict(predecessor, workflow_path=predecessor["repository_path"]))
        self.visiting.remove(identity)
        self.validated.add(identity)

    def adoption_reference(self, ref):
        record = self.reference(ref["adoption_record_path"], ref["adoption_record_sha256"])
        _require(record.get("adoption_record_id") == ref["adoption_record_id"], "adoption reference ID mismatch")
        for field in ("workflow_path", "workflow_version", "adopted_definition_sha256"):
            _require(record["target"][field] == ref[field], "adoption reference " + field + " mismatch")
        self.adoption(record)
        return record

    def deprecation(self, data):
        target = self.adoption_reference(data["target"])
        _require(_time(data["deprecated_at"]) >= _time(target["adopted_at"]), "deprecation precedes adoption")
        authority = data["human_authority"]
        raw = _relative(self.root, authority["authority_path"]).read_bytes()
        _require(bool(raw) and _sha(raw) == authority["authority_sha256"], "Human authority artifact absent or SHA mismatch")
        # This verifies the explicit fixed reference, not the truth of Human authority.
        key = (data["target"]["workflow_path"], data["target"]["adopted_definition_sha256"])
        identity = data["deprecation_record_id"]
        _require(key not in self.deprecated or self.deprecated[key] == identity, "conflicting duplicate deprecation state")
        self.deprecated[key] = identity
        successor = data["successor"]
        if successor:
            _require(successor["workflow_path"] != data["target"]["workflow_path"], "self-successor")
            self.adoption_reference(successor)


def validate_adoption_set(schema_path, definition_path, definition, root, records, prospective):
    errors = []
    try:
        _require(not (prospective and records), "prospective validation cannot claim completed records")
        if prospective:
            _require(definition.get("status") == "ADOPTED", "prospective mode requires ADOPTED bytes")
            return [], False
        if not records and definition.get("status") == "PROPOSED" and not definition.get("supersedes"):
            return [], False
        _require(root is not None, "repository root required for adoption validation")
        context = AdoptionSet(root, schema_path)
        loaded = [context.record(p) for p in records]
        matched = []
        for data in loaded:
            kind = data.get("record_type", data.get("decision_type"))
            if kind == "WORKFLOW_FORMAL_ADOPTION":
                context.decision(data)
                if definition.get("status") == "PROPOSED" and _relative(root, data["target"]["workflow_path"]).resolve() == definition_path.resolve():
                    _require(_sha(definition_path.read_bytes()) == data["target"]["candidate_definition_sha256"], "Decision does not bind current PROPOSED candidate bytes")
            elif kind == "WORKFLOW_FORMAL_ADOPTION_RECORD":
                context.adoption(data)
                if _relative(root, data["target"]["workflow_path"]).resolve() == definition_path.resolve():
                    matched.append(data)
            else:
                context.deprecation(data)
        if definition.get("status") == "ADOPTED":
            _require(len(matched) == 1, "ADOPTED workflow requires one valid explicitly supplied Adoption Record")
        else:
            _require(not matched, "PROPOSED workflow cannot claim completed adoption")
        predecessor = definition.get("supersedes")
        if predecessor:
            _require(_relative(root, predecessor["repository_path"]).resolve() != definition_path.resolve(), "self-supersession")
            context.adoption_reference(dict(predecessor, workflow_path=predecessor["repository_path"]))
        return [], False
    except AdoptionCapabilityUnavailable:
        return [], True
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        errors.append(finding("CROSS_ARTIFACT_VALIDATION", "ADOPTION-CONTRACT", str(exc)))
        return errors, False

def _print_human(report: dict[str, Any]) -> None:
    print(f"Validator Result: {report['validator_result']}")
    for layer, result in report["layers"].items():
        print(f"{layer}: {result}")
    print(f"Definition SHA-256: {report['definition_sha256']}")
    print("Definition Digest Status: REPORT_ONLY")
    if report["errors"]:
        print("Errors:")
        for item in report["errors"]:
            suffix = f" [{item['path']}]" if "path" in item else ""
            print(f"  {item['id']}{suffix}: {item['message']}")
    if report["warnings"]:
        print("Warnings / Limitations:")
        for item in report["warnings"]:
            print(f"  {item['id']}: {item['message']}")
    print("Boundary: Validator results do not establish Audit PASS, Human Approval, Rights Verification, Publication, or formal Workflow Definition adoption.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only ProjectORIGIN static workflow validator. Schema capability absence returns VALIDATION_LIMITED and exit code 3.")
    parser.add_argument("--schema", required=True, type=Path, help="local Workflow Definition Schema JSON path")
    parser.add_argument("--definition", required=True, type=Path, help="local Workflow Definition JSON path")
    parser.add_argument("--repository-root", type=Path, help="repository root used only for local Governance compatibility checks")
    parser.add_argument("--check-governance", action="store_true", help="validate the exact required Governance declarations and local files")
    parser.add_argument("--record", action="append", default=[], type=Path, help="explicit read-only record-set member; repeat for all applicable decisions/adoptions/deprecations")
    parser.add_argument("--prospective-adopted", action="store_true", help="validate prospective ADOPTED bytes without claiming completed adoption; cannot be combined with records")
    parser.add_argument("--format", choices=("human", "json"), default="human", help="deterministic output format")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.check_governance and args.repository_root is None:
        report = {
            "validator_result": "FAIL",
            "exit_code": 2,
            "layers": {"JSON_INTEGRITY": "NOT_RUN", "SCHEMA_VALIDATION": "NOT_RUN", "SEMANTIC_VALIDATION": "NOT_RUN", "GOVERNANCE_COMPATIBILITY": "FAIL"},
            "errors": [finding("GOVERNANCE_COMPATIBILITY", "GOVERNANCE-ROOT-REQUIRED", "--repository-root is required with --check-governance")],
            "warnings": [], "definition_identity": {}, "definition_sha256": None, "digest_status": "REPORT_ONLY",
        }
    else:
        try:
            report = run_validation(args.schema, args.definition, args.repository_root, args.check_governance, args.record, args.prospective_adopted)
        except (OSError, ValueError) as exc:
            report = {
                "validator_result": "FAIL", "exit_code": 2,
                "layers": {"JSON_INTEGRITY": "FAIL", "SCHEMA_VALIDATION": "NOT_RUN", "SEMANTIC_VALIDATION": "NOT_RUN", "GOVERNANCE_COMPATIBILITY": "NOT_RUN"},
                "errors": [finding("JSON_INTEGRITY", "JSON-TOOL-ERROR", str(exc))], "warnings": [],
                "definition_identity": {}, "definition_sha256": None, "digest_status": "REPORT_ONLY",
            }
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        _print_human(report)
    return int(report["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
