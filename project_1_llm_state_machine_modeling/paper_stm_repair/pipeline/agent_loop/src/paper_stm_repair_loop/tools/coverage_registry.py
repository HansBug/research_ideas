from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol

from .. import assertion_policy as assertion_contract
from ..assertion_policy import validate_assertion_semantic_policy
from ..eval_env import EvalEnvironment
from pyfcstm.bmc.parse import parse_bmc_query


FUNCTION_FAMILIES: dict[str, str] = {
    "states": "structure",
    "events": "structure",
    "variables": "structure",
    "initial_child": "structure",
    "transitions": "relation",
    "transition_exists": "relation",
    "guards_overlap": "relation",
    "effects": "effect",
    "effect_delta": "effect",
    "effect_deltas": "effect",
    "topology": "structure",
    "path": "structure",
    "simulate": "simulation",
    "fbmcq": "formal",
    "mapped_source_refs": "mapping",
    "mapped_fcstm_refs": "mapping",
    "bound_model_refs": "mapping",
}
ALLOWED_FUNCTION_FAMILY_VALUES = {"structure", "relation", "effect", "simulation", "formal", "mapping"}

PURE_BUILTINS: dict[str, Any] = {
    "len": len,
    "all": all,
    "any": any,
    "min": min,
    "max": max,
    "sum": sum,
    "set": set,
    "tuple": tuple,
    "sorted": sorted,
    "abs": abs,
    "bool": bool,
}

ALLOWED_VIEW_NAMES = {"nl", "stm", "source", "source_trace", "policy"}
ALLOWED_OBSERVATION_ATTRIBUTES = {
    "cycles",
    "final",
    "model_sha256",
    "index",
    "is_ended",
    "active_states",
    "variables",
    "input_events",
    "consumed_events",
    "unconsumed_events",
    "fired_transitions",
    "canonical_query",
    "status",
    "holds",
    "bound",
    "witness",
    "replay_status",
    "requested_initialization",
    "effective_initialization",
    "mode",
    "state",
    "initial_closure",
    "unreachable_leaves",
    "strongly_connected_components",
    "dead_ends",
    "root_exit_reachable",
    "topological_finite",
    "topological_inevitable_terminator",
    "guard_agnostic",
    "limitations",
    "exists",
    "nodes",
    "hop_count",
    "transition_refs",
    "source_macro_refs",
    "compiler_owned_nodes",
    "formal_property_kind",
    "formal_bound",
    "controller_max_bound",
    "query_origin",
    "assumption_basis",
    "process_isolation",
}
ALLOWED_OBSERVATION_METHODS = {"is_active"}

SOURCE_FACT_EVIDENCE_FAMILIES: dict[str, frozenset[str]] = {
    "state": frozenset({"structure"}),
    "event": frozenset({"structure", "relation"}),
    "variable": frozenset({"structure", "effect"}),
    "transition": frozenset({"relation"}),
    "forced_transition": frozenset({"relation"}),
    "guard": frozenset({"relation"}),
    "effect": frozenset({"effect"}),
    "initial_relation": frozenset({"structure"}),
    "hierarchy": frozenset({"structure"}),
    "region": frozenset({"structure"}),
}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deepcopy_jsonish(value: Any) -> Any:
    return copy.deepcopy(value)


class EvalRuntimeProtocol(Protocol):
    def evaluate(
        self,
        expression: str,
        *,
        required_function_families: set[str],
        reason: str,
        reason_context: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate one registered assertion expression and return a record payload."""


class DirectEvalRuntime:
    """Adapt the canonical ``EvalEnvironment`` to the coverage registry protocol."""

    def __init__(self, environment: EvalEnvironment) -> None:
        self.environment = environment

    def evaluate(
        self,
        expression: str,
        *,
        required_function_families: set[str],
        reason: str,
        reason_context: dict[str, Any],
    ) -> dict[str, Any]:
        raw = self.environment.eval_assert(
            expression,
            reason,
            required_function_families=sorted(required_function_families),
        )
        payload = raw.to_json()
        function_calls = payload["function_call_trace"]
        simulation_calls = [
            item
            for item in function_calls
            if item.get("function") == "simulate"
            and item.get("status") == "completed"
        ]
        formal_calls = [
            item
            for item in function_calls
            if item.get("function") == "fbmcq"
            and item.get("status") == "completed"
        ]
        initialization = {
            "calls": [
                {
                    "requested": (item.get("result") or {})
                    .get("data", {})
                    .get("requested_initialization"),
                    "effective": (item.get("result") or {})
                    .get("data", {})
                    .get("effective_initialization"),
                    "cycles": (item.get("kwargs") or {}).get("cycles"),
                    "final": (item.get("result") or {}).get("data", {}).get("final"),
                }
                for item in simulation_calls
            ]
        }
        formal = {
            "calls": [
                {
                    "query": (item.get("args") or [None])[0]
                    if item.get("args")
                    else (item.get("kwargs") or {}).get("query"),
                    **((item.get("result") or {}).get("data") or {}),
                }
                for item in formal_calls
            ]
        }
        completed = raw.match_status in {"matches", "contradicts"}
        return {
            "execution_status": "completed" if completed else "inconclusive",
            "python_value_type": "bool" if isinstance(raw.value, bool) else None,
            "python_value": raw.value,
            "match_status": raw.match_status,
            "inconclusive_reason": None if completed else raw.result,
            "function_calls": function_calls,
            "observed_function_families": payload["actual_function_families"],
            "limitations": [] if completed else [raw.result],
            "exception": raw.error,
            "producer_versions": {},
            "model_sha256": sha256_text(self.environment.model_text or ""),
            "dependency_provenance": payload["audit"],
            "eval_vars_hash_before": raw.vars_hash_before,
            "eval_vars_hash_after": raw.vars_hash_after,
            "function_registry_hash": raw.function_registry_hash,
            "reason": reason,
            "reason_context": reason_context,
            "initialization": initialization,
            "formal": formal,
        }


@dataclass
class AssertionVersion:
    assertion_chain_id: str
    assertion_version_id: str
    root_node_id: str
    coverage_unit_id: str
    required: bool
    assert_text: str
    assert_sha256: str
    basis_ids: tuple[str, ...] = ()
    obligation_signature: str | None = None
    required_function_families: tuple[str, ...] = ()
    evidence_scope: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    record_language: str | None = None
    formal_property_kind: str | None = None
    formal_bound: int | None = None
    formal_bound_origin: str | None = None
    formal_assumption_basis_ids: tuple[str, ...] = ()
    supersedes_version_id: str | None = None
    accepted: bool = True

    def to_record(self) -> dict[str, Any]:
        return {
            "assertion_chain_id": self.assertion_chain_id,
            "assertion_version_id": self.assertion_version_id,
            "root_node_id": self.root_node_id,
            "coverage_unit_id": self.coverage_unit_id,
            "required": self.required,
            "assert": self.assert_text,
            "assert_sha256": self.assert_sha256,
            "basis_ids": list(self.basis_ids),
            "obligation_signature": self.obligation_signature,
            "required_function_families": list(self.required_function_families),
            "evidence_scope": _deepcopy_jsonish(self.evidence_scope),
            "rationale": self.rationale,
            "record_language": self.record_language,
            "formal_property_kind": self.formal_property_kind,
            "formal_bound": self.formal_bound,
            "formal_bound_origin": self.formal_bound_origin,
            "formal_assumption_basis_ids": list(
                self.formal_assumption_basis_ids
            ),
            "supersedes_version_id": self.supersedes_version_id,
            "accepted": self.accepted,
        }


class DefaultEvalRuntime:
    """Small direct-eval runtime used by contract tests and local controllers."""

    def __init__(
        self,
        *,
        vars: Mapping[str, Any] | None = None,
        funcs: Mapping[str, Callable[..., Any]] | None = None,
        model_sha256: str = "unknown",
        producer_versions: Mapping[str, Any] | None = None,
    ) -> None:
        self.vars = dict(vars or {})
        self.funcs = dict(funcs or {})
        self.model_sha256 = model_sha256
        self.producer_versions = dict(producer_versions or {})

    def _audit(self, expression: str) -> tuple[bool, list[str], list[dict[str, Any]]]:
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            return False, [f"syntax_error:{exc.__class__.__name__}"], []
        allowed_names = set(PURE_BUILTINS) | set(ALLOWED_VIEW_NAMES) | set(self.vars) | set(self.funcs)
        local_bindings: set[str] = set()
        rejected: list[str] = []
        nodes: list[dict[str, Any]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.comprehension):
                if isinstance(node.target, ast.Name):
                    local_bindings.add(node.target.id)
                elif isinstance(node.target, (ast.Tuple, ast.List)):
                    local_bindings.update(item.id for item in node.target.elts if isinstance(item, ast.Name))
        allowed_names |= local_bindings
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                ok = node.id in allowed_names
                nodes.append({"kind": "Name", "value": node.id, "allowed": ok})
                if not ok:
                    rejected.append(f"untracked_name:{node.id}")
            elif isinstance(node, ast.Attribute):
                attr = node.attr
                dunder = attr.startswith("__") or attr.endswith("__")
                ok = (attr in ALLOWED_OBSERVATION_ATTRIBUTES or attr in ALLOWED_OBSERVATION_METHODS) and not dunder
                nodes.append({"kind": "Attribute", "value": attr, "allowed": ok})
                if dunder:
                    rejected.append(f"dunder_attribute:{attr}")
                elif not ok:
                    rejected.append(f"untracked_attribute:{attr}")
            elif isinstance(node, ast.Call):
                ok = False
                call_name = None
                if isinstance(node.func, ast.Name):
                    call_name = node.func.id
                    ok = call_name in PURE_BUILTINS or call_name in self.funcs
                elif isinstance(node.func, ast.Attribute):
                    call_name = node.func.attr
                    ok = call_name in ALLOWED_OBSERVATION_METHODS
                nodes.append({"kind": "Call", "value": call_name, "allowed": ok})
                if not ok:
                    rejected.append(f"untracked_call:{call_name or type(node.func).__name__}")
        return not rejected, rejected, nodes

    def evaluate(
        self,
        expression: str,
        *,
        required_function_families: set[str],
        reason: str,
        reason_context: dict[str, Any],
    ) -> dict[str, Any]:
        audit_ok, audit_rejections, audit_nodes = self._audit(expression)
        if not audit_ok:
            return {
                "execution_status": "inconclusive",
                "python_value_type": None,
                "python_value": None,
                "match_status": "inconclusive",
                "inconclusive_reason": "untracked_dependency",
                "function_calls": [],
                "observed_function_families": [],
                "limitations": ["dependency_provenance_audit_failed", *audit_rejections],
                "exception": None,
                "producer_versions": self.producer_versions,
                "model_sha256": self.model_sha256,
                "dependency_provenance": {"expression": expression, "nodes": audit_nodes, "accepted": False},
                "reason": reason,
                "reason_context": reason_context,
            }
        calls: list[dict[str, Any]] = []

        def wrap(name: str, func: Callable[..., Any]) -> Callable[..., Any]:
            def instrumented(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                calls.append(
                    {
                        "function_name": name,
                        "family": FUNCTION_FAMILIES.get(name, "unknown"),
                        "arguments_repr": repr({"args": args, "kwargs": kwargs}),
                        "result_repr": repr(result),
                    }
                )
                return result

            instrumented.__name__ = name
            return instrumented

        locals_env = {**self.vars, **{name: wrap(name, func) for name, func in self.funcs.items()}}
        try:
            value = eval(expression, {"__builtins__": PURE_BUILTINS}, locals_env)  # noqa: S307 - direct eval is the contract.
        except Exception as exc:
            return {
                "execution_status": "inconclusive",
                "python_value_type": None,
                "python_value": None,
                "match_status": "inconclusive",
                "inconclusive_reason": "exception",
                "function_calls": calls,
                "observed_function_families": sorted({call["family"] for call in calls}),
                "limitations": ["eval_exception", type(exc).__name__],
                "exception": {"type": type(exc).__name__, "message": str(exc)},
                "producer_versions": self.producer_versions,
                "model_sha256": self.model_sha256,
                "dependency_provenance": {"expression": expression, "nodes": audit_nodes, "accepted": True},
                "reason": reason,
                "reason_context": reason_context,
            }
        observed_families = {call["family"] for call in calls}
        if not isinstance(value, bool):
            status = "non_bool"
            match = "inconclusive"
            limitations = ["assertion_did_not_return_strict_bool"]
        elif not calls:
            status = "inconclusive"
            match = "inconclusive"
            limitations = ["no_model_evidence"]
        elif not required_function_families.issubset(observed_families):
            status = "inconclusive"
            match = "inconclusive"
            missing = sorted(required_function_families - observed_families)
            limitations = ["required_function_family_not_observed", *missing]
        else:
            status = "completed"
            match = "matches" if value is True else "contradicts"
            limitations = []
        return {
            "execution_status": status,
            "python_value_type": type(value).__name__,
            "python_value": value if isinstance(value, bool) else None,
            "match_status": match,
            "function_calls": calls,
            "observed_function_families": sorted(observed_families),
            "limitations": limitations,
            "exception": None,
            "producer_versions": self.producer_versions,
            "model_sha256": self.model_sha256,
            "dependency_provenance": {"expression": expression, "nodes": audit_nodes, "accepted": True},
            "reason": reason,
            "reason_context": reason_context,
        }


class CoverageRegistry:
    """Append-only Discover coverage plan and assertion execution registry."""

    def __init__(
        self,
        *,
        input_segment_ids: list[str] | tuple[str, ...] | None = None,
        coverage_requirements: Mapping[str, Mapping[str, Any]] | None = None,
        source_fact_ids: list[str] | tuple[str, ...] | None = None,
        known_source_fact_ids: list[str] | tuple[str, ...] | None = None,
        source_fact_refs: Mapping[str, list[str] | tuple[str, ...]] | None = None,
        source_fact_kinds: Mapping[str, str] | None = None,
        source_fact_details: Mapping[str, Mapping[str, Any]] | None = None,
        eval_runtime: EvalRuntimeProtocol | None = None,
        eval_vars: Mapping[str, Any] | None = None,
        eval_funcs: Mapping[str, Callable[..., Any]] | None = None,
        model_sha256: str = "unknown",
        record_sink: Callable[[str, Mapping[str, Any]], Mapping[str, Any]] | None = None,
        issue_assessment_resolver: Callable[[dict[str, Any]], tuple[str, bool]] | None = None,
        fbmcq_guide_read: Callable[[], bool] | None = None,
        evidence_context: Mapping[str, Any] | None = None,
    ) -> None:
        self.input_segment_ids = set(input_segment_ids or [])
        self.strict_coverage_enabled = coverage_requirements is not None
        self.coverage_requirements = {
            str(requirement_id): _deepcopy_jsonish(dict(requirement))
            for requirement_id, requirement in (coverage_requirements or {}).items()
        }
        # ``source_fact_ids`` is the deterministic behavior-relevant subset that
        # must be covered. Supporting diagnostic/mapping facts remain known and
        # may be dispositioned, but their omission does not fail coverage.
        self.source_fact_ids = set(source_fact_ids or [])
        self.known_source_fact_ids = set(known_source_fact_ids or source_fact_ids or [])
        self.source_fact_refs = {
            str(fact_id): tuple(str(ref) for ref in refs)
            for fact_id, refs in (source_fact_refs or {}).items()
        }
        self.source_fact_kinds = {
            str(fact_id): str(kind)
            for fact_id, kind in (source_fact_kinds or {}).items()
        }
        self.source_fact_details = {
            str(fact_id): _deepcopy_jsonish(dict(detail))
            for fact_id, detail in (source_fact_details or {}).items()
        }
        self.eval_runtime = eval_runtime or DefaultEvalRuntime(vars=eval_vars, funcs=eval_funcs, model_sha256=model_sha256)
        self.record_sink = record_sink
        self.issue_assessment_resolver = issue_assessment_resolver
        self.fbmcq_guide_read = fbmcq_guide_read or (lambda: False)
        self.evidence_context = _deepcopy_jsonish(dict(evidence_context or {}))
        self.plan_registered = False
        self.coverage_units: dict[str, dict[str, Any]] = {}
        self.semantic_review_gate: Any | None = None
        self.segment_dispositions: dict[str, dict[str, Any]] = {}
        self.fact_dispositions: dict[str, dict[str, Any]] = {}
        self.roots: dict[str, dict[str, Any]] = {}
        self.chains: dict[str, list[AssertionVersion]] = {}
        self.requirement_assertion_chains: dict[str, set[str]] = {}
        self.source_fact_assertion_chains: dict[str, set[str]] = {}
        self.evaluations: dict[str, list[dict[str, Any]]] = {}
        self.records: list[dict[str, Any]] = []
        self.latest_projection: dict[str, Any] | None = None
        self.registered_plan_reason: str | None = None

    def append_record(self, record_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        if self.record_sink is not None:
            record = dict(self.record_sink(record_type, payload))
            self.records.append(_deepcopy_jsonish(record))
            return record
        record = {
            "record_id": f"LOCAL-REC-{len(self.records) + 1:06d}",
            "record_type": record_type,
            "payload": _deepcopy_jsonish(dict(payload)),
        }
        self.records.append(record)
        return record

    def latest_versions(self) -> list[AssertionVersion]:
        return [versions[-1] for _, versions in sorted(self.chains.items()) if versions]

    def latest_by_expression(self, expression: str) -> list[AssertionVersion]:
        return [version for version in self.latest_versions() if version.assert_text == expression]

    def selected_source_fact_ids(self) -> set[str]:
        """Return SourceFacts explicitly selected as executable assertion evidence."""

        return {
            fact_id
            for fact_id, chain_ids in self.source_fact_assertion_chains.items()
            if chain_ids
        }

    def _make_reason_context(self, version: AssertionVersion) -> dict[str, Any]:
        return {
            "phase": "assertion_execution",
            "related_segment_ids": list(version.basis_ids),
            "related_coverage_unit_ids": [version.coverage_unit_id],
            "related_root_node_ids": [version.root_node_id],
            "related_assertion_chain_ids": [version.assertion_chain_id],
            "related_assertion_version_ids": [version.assertion_version_id],
            "assert_sha256": version.assert_sha256,
            "expected_fact_kind": "assertion_result",
        }

    def register_plan(self, plan: Mapping[str, Any], *, reason: str) -> dict[str, Any]:
        if self.plan_registered:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "limitations": ["coverage_plan_already_registered", "append_only_registry"],
            }
            self.append_record("coverage_plan_registration_rejected", {**result, "reason": reason})
            return result
        errors: list[str] = []
        try:
            units = _as_list(plan.get("coverage_units"))
            dispositions = _as_list(plan.get("segment_dispositions"))
            fact_dispositions = _as_list(plan.get("fact_dispositions"))
            roots = _as_list(plan.get("proposition_roots") or plan.get("roots"))
            assertions = _as_list(plan.get("logical_assertions") or plan.get("assertions"))
        except TypeError as exc:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "errors": [f"malformed_plan:{exc}"],
                "limitations": ["coverage_plan_rejected", "old_latest_preserved"],
            }
            self.append_record("coverage_plan_registration_rejected", {**result, "reason": reason, "plan": _deepcopy_jsonish(plan)})
            return result
        forbidden_controller_fields = sorted(
            set(plan) & {"input_segments", "coverage_requirements", "source_facts"}
        )
        if forbidden_controller_fields:
            errors.append("controller_owned_fields_not_agent_writable:" + ",".join(forbidden_controller_fields))
        if not units:
            errors.append("no_coverage_units")
        unit_ids: set[str] = set()
        segment_covered: set[str] = set()
        fact_covered: set[str] = set()
        requirement_covered: set[str] = set()
        requirement_units: dict[str, set[str]] = {
            requirement_id: set() for requirement_id in self.coverage_requirements
        }
        for unit in units:
            unit_id = str(unit.get("coverage_unit_id") or unit.get("unit_id") or "")
            if not unit_id:
                errors.append("coverage_unit_missing_id")
                continue
            if unit_id in unit_ids:
                errors.append(f"duplicate_coverage_unit:{unit_id}")
            unit_ids.add(unit_id)
            unit_segments = {str(item) for item in unit.get("segment_ids", []) if item}
            unit_requirements = {
                str(item) for item in unit.get("requirement_ids", []) if item
            }
            unit_dimensions = {str(item) for item in unit.get("dimensions", []) if item}
            segment_covered.update(unit_segments)
            fact_covered.update(str(item) for item in unit.get("source_fact_ids", []) if item)
            requirement_covered.update(unit_requirements)
            for requirement_id in unit_requirements:
                requirement_units.setdefault(requirement_id, set()).add(unit_id)
                requirement = self.coverage_requirements.get(requirement_id)
                if requirement is None:
                    continue
                expected_segment = str(requirement.get("segment_id"))
                if expected_segment not in unit_segments:
                    errors.append(
                        f"coverage_requirement_segment_basis_missing:{requirement_id}:{unit_id}:{expected_segment}"
                    )
                dimension = str(requirement.get("dimension"))
                if dimension not in unit_dimensions:
                    errors.append(
                        f"coverage_requirement_dimension_missing:{requirement_id}:{unit_id}:{dimension}"
                    )
            unit_kind = str(unit.get("unit_kind") or "")
            if (
                self.strict_coverage_enabled
                and unit_kind == "behavior_obligation"
                and not unit_requirements
            ):
                errors.append(f"behavior_obligation_without_coverage_requirement:{unit_id}")
            if (
                self.strict_coverage_enabled
                and self.source_fact_ids
                and unit_kind == "behavior_obligation"
                and not unit.get("source_fact_ids")
            ):
                errors.append(f"behavior_obligation_without_source_fact_grounding:{unit_id}")
            if unit_kind == "source_behavior" and unit_segments:
                errors.append(f"source_behavior_claims_nl_basis:{unit_id}")
        unknown_segments = sorted(segment_covered - self.input_segment_ids)
        if unknown_segments:
            errors.append("unknown_input_segments:" + ",".join(unknown_segments))
        unknown_facts = sorted(fact_covered - self.known_source_fact_ids)
        if unknown_facts:
            errors.append("unknown_source_facts:" + ",".join(unknown_facts))
        unknown_requirements = sorted(
            requirement_covered - set(self.coverage_requirements)
        )
        if unknown_requirements:
            errors.append(
                "unknown_coverage_requirements:" + ",".join(unknown_requirements)
            )
        missing_requirements = sorted(
            set(self.coverage_requirements) - requirement_covered
        )
        if missing_requirements:
            errors.append(
                "uncovered_coverage_requirements:" + ",".join(missing_requirements)
            )
        for requirement_id, linked_units in sorted(requirement_units.items()):
            if len(linked_units) != 1:
                errors.append(
                    f"coverage_requirement_unit_cardinality:{requirement_id}:{len(linked_units)}"
                )
        clause_units: dict[str, set[str]] = {}
        for requirement_id, requirement in self.coverage_requirements.items():
            clause_id = str(requirement.get("clause_id") or "")
            if clause_id:
                clause_units.setdefault(clause_id, set()).update(
                    requirement_units.get(requirement_id, set())
                )
        for clause_id, linked_units in sorted(clause_units.items()):
            if len(linked_units) != 1:
                errors.append(
                    f"semantic_clause_unit_cardinality:{clause_id}:{len(linked_units)}"
                )
        disposition_segments = {str(item.get("segment_id")) for item in dispositions if item.get("segment_id")}
        unknown_disposition_segments = sorted(disposition_segments - self.input_segment_ids)
        if unknown_disposition_segments:
            errors.append(
                "unknown_disposition_segments:" + ",".join(unknown_disposition_segments)
            )
        if segment_covered & disposition_segments:
            errors.append("segment_has_both_coverage_unit_and_disposition")
        required_segments = {
            str(item.get("segment_id"))
            for item in self.coverage_requirements.values()
        }
        disposed_required_segments = sorted(required_segments & disposition_segments)
        if disposed_required_segments:
            errors.append(
                "required_segment_cannot_be_dispositioned:"
                + ",".join(disposed_required_segments)
            )
        if self.input_segment_ids:
            missing_segments = sorted(self.input_segment_ids - segment_covered - disposition_segments)
            if missing_segments:
                errors.append("uncovered_input_segments:" + ",".join(missing_segments))
        disposition_facts = {str(item.get("fact_id") or item.get("source_fact_id")) for item in fact_dispositions if item.get("fact_id") or item.get("source_fact_id")}
        unknown_disposition_facts = sorted(
            disposition_facts - self.known_source_fact_ids
        )
        if unknown_disposition_facts:
            errors.append(
                "unknown_disposition_facts:" + ",".join(unknown_disposition_facts)
            )
        disposed_behavior_facts = sorted(disposition_facts & self.source_fact_ids)
        if disposed_behavior_facts:
            errors.append(
                "behavior_source_facts_cannot_be_dispositioned:"
                + ",".join(disposed_behavior_facts)
            )
        known_basis_ids = (
            self.input_segment_ids
            | self.known_source_fact_ids
            | set(self.coverage_requirements)
        )
        unit_to_roots: dict[str, list[str]] = {unit_id: [] for unit_id in unit_ids}
        root_ids: set[str] = set()
        for root in roots:
            root_id = str(root.get("node_id") or root.get("root_node_id") or "")
            unit_id = str(root.get("coverage_unit_id") or "")
            if not root_id:
                errors.append("root_missing_id")
                continue
            if root_id in root_ids:
                errors.append(f"duplicate_root:{root_id}")
            root_ids.add(root_id)
            if unit_id not in unit_ids:
                errors.append(f"root_unknown_coverage_unit:{root_id}:{unit_id}")
            else:
                unit_to_roots[unit_id].append(root_id)
                unit = next(
                    (
                        item
                        for item in units
                        if str(item.get("coverage_unit_id") or item.get("unit_id"))
                        == unit_id
                    ),
                    {},
                )
                allowed_root_refs = {
                    ref
                    for fact_id in unit.get("source_fact_ids", [])
                    for ref in self.source_fact_refs.get(str(fact_id), ())
                }
                unknown_root_refs = sorted(
                    {
                        str(ref)
                        for ref in root.get("model_element_refs", [])
                        if ref
                    }
                    - allowed_root_refs
                )
                if unknown_root_refs:
                    errors.append(
                        f"root_model_refs_not_grounded_by_unit_facts:{root_id}:"
                        + ",".join(unknown_root_refs)
                    )
        for unit_id, roots_for_unit in unit_to_roots.items():
            if len(roots_for_unit) != 1:
                errors.append(f"coverage_unit_root_cardinality:{unit_id}:{len(roots_for_unit)}")
        required_count_by_root = {root_id: 0 for root_id in root_ids}
        root_unit_by_id = {
            str(root.get("node_id") or root.get("root_node_id")): str(
                root.get("coverage_unit_id") or ""
            )
            for root in roots
        }
        root_model_refs_by_id = {
            str(root.get("node_id") or root.get("root_node_id")): {
                str(ref) for ref in root.get("model_element_refs", []) if ref
            }
            for root in roots
        }
        units_by_id = {
            str(unit.get("coverage_unit_id") or unit.get("unit_id")): unit
            for unit in units
        }
        expression_sha_by_chain: dict[str, str] = {}
        expression_texts: dict[str, str] = {}
        chain_ids: set[str] = set()
        assertion_families_by_unit: dict[str, set[str]] = {
            unit_id: set() for unit_id in unit_ids
        }
        assertion_texts_by_root: dict[str, list[str]] = {
            root_id: [] for root_id in root_ids
        }
        requirement_assertion_chains: dict[str, set[str]] = {
            requirement_id: set() for requirement_id in self.coverage_requirements
        }
        source_fact_assertion_chains: dict[str, set[str]] = {
            fact_id: set() for fact_id in self.source_fact_ids
        }
        assertion_families_by_chain: dict[str, set[str]] = {}
        assertions_by_chain: dict[str, dict[str, Any]] = {}
        unit_requirements_by_id = {
            str(unit.get("coverage_unit_id") or unit.get("unit_id")): [
                self.coverage_requirements[str(requirement_id)]
                for requirement_id in unit.get("requirement_ids", [])
                if str(requirement_id) in self.coverage_requirements
            ]
            for unit in units
        }
        for assertion in assertions:
            chain_id = str(assertion.get("assertion_chain_id") or assertion.get("chain_id") or "")
            root_id = str(assertion.get("root_node_id") or "")
            unit_id = str(assertion.get("coverage_unit_id") or "")
            expr = assertion.get("assert") if "assert" in assertion else assertion.get("assert_text")
            if not chain_id or not root_id or not unit_id or not isinstance(expr, str):
                errors.append("assertion_missing_required_field")
                continue
            if chain_id in chain_ids:
                errors.append(f"duplicate_assertion_chain:{chain_id}")
            chain_ids.add(chain_id)
            assertions_by_chain[chain_id] = assertion
            if root_id not in root_ids:
                errors.append(f"assertion_unknown_root:{chain_id}:{root_id}")
            if unit_id not in unit_ids:
                errors.append(f"assertion_unknown_coverage_unit:{chain_id}:{unit_id}")
            if root_unit_by_id.get(root_id) not in {None, unit_id}:
                errors.append(
                    f"assertion_root_unit_mismatch:{chain_id}:{root_id}:{unit_id}"
                )
            if assertion.get("required", True) is True:
                required_count_by_root[root_id] = required_count_by_root.get(root_id, 0) + 1
                assertion_texts_by_root.setdefault(root_id, []).append(expr)
            families = [str(item) for item in assertion.get("required_function_families", [])]
            assertion_families_by_chain[chain_id] = set(families)
            assertion_families_by_unit.setdefault(unit_id, set()).update(families)
            if not families:
                errors.append(f"assertion_requires_function_family:{chain_id}")
            invalid_families = sorted(set(families) - ALLOWED_FUNCTION_FAMILY_VALUES)
            if invalid_families:
                errors.append(f"invalid_required_function_family:{chain_id}:{','.join(invalid_families)}")
            digest = sha256_text(expr)
            if digest in expression_sha_by_chain.values():
                errors.append(f"duplicate_latest_expression_sha:{chain_id}:{digest}")
            if expr in expression_texts.values():
                errors.append(f"duplicate_latest_expression_text:{chain_id}")
            expression_sha_by_chain[chain_id] = digest
            expression_texts[chain_id] = expr
            if not assertion.get("basis_ids"):
                errors.append(f"assertion_requires_basis:{chain_id}")
            assertion_basis = {
                str(item) for item in assertion.get("basis_ids", []) if item
            }
            if assertion.get("required", True) is True:
                for requirement_id in assertion_basis & set(self.coverage_requirements):
                    if unit_id in requirement_units.get(requirement_id, set()):
                        requirement_assertion_chains[requirement_id].add(chain_id)
                for fact_id in assertion_basis & self.source_fact_ids:
                    source_fact_assertion_chains[fact_id].add(chain_id)
            unknown_assertion_basis = sorted(assertion_basis - known_basis_ids)
            if unknown_assertion_basis:
                errors.append(
                    f"assertion_unknown_basis:{chain_id}:"
                    + ",".join(unknown_assertion_basis)
                )
            if "fbmcq(" in expr and not self.fbmcq_guide_read():
                errors.append(f"fbmcq_guide_required_before_registration:{chain_id}")
            errors.extend(
                _formal_metadata_errors(
                    assertion,
                    expression=expr,
                    coverage_requirements=self.coverage_requirements,
                    known_basis_ids=known_basis_ids,
                    assertion_basis_ids=assertion_basis,
                )
            )
            linked_requirements = [
                requirement
                for requirement in unit_requirements_by_id.get(unit_id, [])
                if str(requirement.get("requirement_id")) in assertion_basis
            ]
            policy_errors = validate_assertion_semantic_policy(
                expr,
                linked_requirements,
            )
            errors.extend(
                f"assertion_semantic_policy:{chain_id}:{error}"
                for error in policy_errors
            )
            if any(
                str(requirement.get("dimension")) == "cardinality"
                for requirement in linked_requirements
            ):
                for parent in _cardinality_state_parent_bindings(expr):
                    if f"state:{parent}" not in root_model_refs_by_id.get(
                        root_id, set()
                    ):
                        errors.append(
                            "assertion_cardinality_parent_not_grounded_by_root:"
                            f"{chain_id}:{parent}:{root_id}"
                        )
            if self.source_fact_details:
                model_variables = _model_variable_names(self.source_fact_details)
                for variable in sorted(
                    _literal_effect_delta_variables(expr) - model_variables
                ):
                    errors.append(
                        f"assertion_effect_variable_not_in_model:{chain_id}:{variable}"
                    )
                unit_fact_ids = {
                    str(item)
                    for item in units_by_id.get(unit_id, {}).get(
                        "source_fact_ids", []
                    )
                }
                for source, event, target in _effect_deltas_transition_bindings(expr):
                    if not _unit_facts_contain_transition_binding(
                        unit_fact_ids,
                        self.source_fact_details,
                        source=source,
                        event=event,
                        target=target,
                    ):
                        errors.append(
                            "assertion_effect_transition_not_grounded_by_unit_facts:"
                            f"{chain_id}:{source}:{event}:{target}"
                        )
        if self.source_fact_details:
            for root in roots:
                root_id = str(root.get("node_id") or root.get("root_node_id") or "")
                unit_id = str(root.get("coverage_unit_id") or "")
                unit = units_by_id.get(unit_id, {})
                combined_expression = "\n".join(
                    assertion_texts_by_root.get(root_id, [])
                )
                unit_fact_ids = {
                    str(fact_id) for fact_id in unit.get("source_fact_ids", [])
                }
                for model_ref in root.get("model_element_refs", []):
                    matching_facts = [
                        self.source_fact_details[fact_id]
                        for fact_id in unit_fact_ids
                        if fact_id in self.source_fact_details
                        and str(model_ref)
                        in self.source_fact_details[fact_id].get(
                            "qualified_refs", []
                        )
                    ]
                    if any(
                        str(fact.get("fact_kind")) == "source_fcstm_mapping"
                        for fact in matching_facts
                    ):
                        continue
                    tokens = {
                        token
                        for fact in matching_facts
                        for token in _fact_binding_tokens(fact, str(model_ref))
                    }
                    if tokens and not any(
                        token in combined_expression for token in tokens
                    ):
                        errors.append(
                            f"root_model_ref_not_used_by_assertion:{root_id}:{model_ref}"
                        )
        for root_id, count in required_count_by_root.items():
            if count < 1:
                errors.append(f"root_without_required_assertion:{root_id}")
        for requirement_id, requirement in self.coverage_requirements.items():
            linked_chain_ids = requirement_assertion_chains.get(requirement_id, set())
            if not linked_chain_ids:
                errors.append(
                    f"coverage_requirement_assertion_basis_missing:{requirement_id}"
                )
            options = [
                set(str(item) for item in option)
                for option in requirement.get(
                    "required_function_family_options", []
                )
            ]
            linked_families = set().union(
                *(assertion_families_by_chain.get(chain_id, set()) for chain_id in linked_chain_ids),
                set(),
            )
            if not any(option <= linked_families for option in options):
                errors.append(
                    f"coverage_requirement_evidence_family_unsatisfied:{requirement_id}:"
                    + ",".join(sorted(linked_families))
                )
        if self.strict_coverage_enabled and self.source_fact_details:
            verified_fact_chains: dict[str, set[str]] = {
                fact_id: set() for fact_id in self.source_fact_ids
            }
            cited_fact_ids = {
                fact_id
                for fact_id, chain_ids in source_fact_assertion_chains.items()
                if chain_ids
            }
            for fact_id in sorted(cited_fact_ids):
                fact = self.source_fact_details.get(fact_id)
                if fact is None:
                    errors.append(f"source_fact_detail_missing:{fact_id}")
                    continue
                for chain_id in source_fact_assertion_chains.get(fact_id, set()):
                    assertion = assertions_by_chain.get(chain_id, {})
                    expression = assertion.get("assert")
                    if not isinstance(expression, str):
                        continue
                    if _assertion_directly_verifies_source_fact(
                        expression,
                        assertion_families_by_chain.get(chain_id, set()),
                        fact,
                    ):
                        verified_fact_chains[fact_id].add(chain_id)
                if not verified_fact_chains[fact_id]:
                    errors.append(f"source_fact_not_directly_verified:{fact_id}")
            source_fact_assertion_chains = verified_fact_chains
        if errors:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "errors": errors,
                "required_actions": _registration_required_actions(
                    errors,
                    source_fact_details=self.source_fact_details,
                    coverage_requirements=self.coverage_requirements,
                ),
                "limitations": ["coverage_plan_rejected", "old_latest_preserved"],
            }
            self.append_record("coverage_plan_registration_rejected", {**result, "reason": reason, "plan": _deepcopy_jsonish(plan)})
            return result
        self.coverage_units = {str(unit.get("coverage_unit_id") or unit.get("unit_id")): _deepcopy_jsonish(unit) for unit in units}
        self.segment_dispositions = {str(item.get("segment_id")): _deepcopy_jsonish(item) for item in dispositions}
        self.fact_dispositions = {str(item.get("fact_id") or item.get("source_fact_id")): _deepcopy_jsonish(item) for item in fact_dispositions}
        self.roots = {str(root.get("node_id") or root.get("root_node_id")): _deepcopy_jsonish(root) for root in roots}
        for assertion in assertions:
            chain_id = str(assertion.get("assertion_chain_id") or assertion.get("chain_id"))
            expr = str(assertion.get("assert") if "assert" in assertion else assertion.get("assert_text"))
            version = AssertionVersion(
                assertion_chain_id=chain_id,
                assertion_version_id=f"{chain_id}@v1",
                root_node_id=str(assertion.get("root_node_id")),
                coverage_unit_id=str(assertion.get("coverage_unit_id")),
                required=bool(assertion.get("required", True)),
                assert_text=expr,
                assert_sha256=sha256_text(expr),
                basis_ids=tuple(str(item) for item in assertion.get("basis_ids", [])),
                obligation_signature=assertion.get("obligation_signature"),
                required_function_families=tuple(sorted(str(item) for item in assertion.get("required_function_families", []))),
                evidence_scope=_deepcopy_jsonish(assertion.get("evidence_scope", {})),
                rationale=str(assertion.get("rationale", "")),
                record_language=assertion.get("record_language"),
                formal_property_kind=assertion.get("formal_property_kind"),
                formal_bound=assertion.get("formal_bound"),
                formal_bound_origin=assertion.get("formal_bound_origin"),
                formal_assumption_basis_ids=tuple(
                    str(item)
                    for item in assertion.get("formal_assumption_basis_ids", [])
                ),
            )
            self.chains[chain_id] = [version]
        self.plan_registered = True
        self.requirement_assertion_chains = requirement_assertion_chains
        self.source_fact_assertion_chains = source_fact_assertion_chains
        self.registered_plan_reason = reason
        environment = getattr(self.eval_runtime, "environment", None)
        mapping = getattr(environment, "mapping", None)
        if mapping is not None:
            mapping.bindings = {
                unit_id: sorted(
                    {
                        ref
                        for fact_id in unit.get("source_fact_ids", [])
                        for ref in self.source_fact_refs.get(str(fact_id), ())
                    }
                )
                for unit_id, unit in self.coverage_units.items()
            }
        self.latest_projection = None
        result = {
            "execution_status": "completed",
            "accepted": True,
            "coverage_plan_accepted": True,
            "registered_reference_closure": True,
            "registered_worklist_complete": False,
            "coverage_unit_count": len(self.coverage_units),
            "root_count": len(self.roots),
            "assertion_chain_count": len(self.chains),
            "coverage_requirement_count": len(self.coverage_requirements),
            "covered_coverage_requirement_count": len(requirement_covered),
            "segment_dispositions": [
                item for _, item in sorted(self.segment_dispositions.items())
            ],
            "fact_dispositions": [
                item for _, item in sorted(self.fact_dispositions.items())
            ],
            "coverage_units": [
                item for _, item in sorted(self.coverage_units.items())
            ],
            "proposition_roots": [
                item for _, item in sorted(self.roots.items())
            ],
            "latest_assertions": [version.to_record() for version in self.latest_versions()],
            "strict_coverage_certificate": {
                "status": "registered_pending_execution",
                "coverage_requirement_total": len(self.coverage_requirements),
                "coverage_requirement_covered": len(requirement_covered),
            },
            "limitations": [],
        }
        self.append_record("coverage_plan_registered", {**result, "reason": reason})
        return result

    def revise_assertion(
        self,
        assertion_chain_id: str,
        assert_text: str,
        *,
        reason: str,
        formal_property_kind: str | None = None,
        formal_bound: int | None = None,
        formal_bound_origin: str | None = None,
        formal_assumption_basis_ids: list[str] | None = None,
        required_function_families: list[str] | None = None,
    ) -> dict[str, Any]:
        if assertion_chain_id not in self.chains:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "limitations": ["unknown_assertion_chain", "old_latest_preserved"],
            }
            self.append_record("assertion_revision_rejected", {**result, "assertion_chain_id": assertion_chain_id, "reason": reason})
            return result
        latest = self.chains[assertion_chain_id][-1]
        next_function_families = tuple(
            sorted(
                str(item)
                for item in (
                    required_function_families
                    if required_function_families is not None
                    else latest.required_function_families
                )
            )
        )
        family_errors: list[str] = []
        if not next_function_families:
            family_errors.append(
                f"assertion_requires_function_family:{assertion_chain_id}"
            )
        invalid_families = sorted(
            set(next_function_families) - ALLOWED_FUNCTION_FAMILY_VALUES
        )
        if invalid_families:
            family_errors.append(
                "invalid_required_function_family:"
                f"{assertion_chain_id}:{','.join(invalid_families)}"
            )
        if family_errors:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "assertion_chain_id": assertion_chain_id,
                "latest_preserved_assertion_version_id": latest.assertion_version_id,
                "errors": family_errors,
                "limitations": [
                    "function_family_route_rejected",
                    "old_latest_preserved",
                ],
            }
            self.append_record(
                "assertion_revision_rejected", {**result, "reason": reason}
            )
            return result
        unit = self.coverage_units.get(latest.coverage_unit_id, {})
        policy_errors = validate_assertion_semantic_policy(
            assert_text,
            [
                self.coverage_requirements[str(requirement_id)]
                for requirement_id in unit.get("requirement_ids", [])
                if str(requirement_id) in self.coverage_requirements
                and str(requirement_id) in latest.basis_ids
            ],
        )
        if policy_errors:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "assertion_chain_id": assertion_chain_id,
                "latest_preserved_assertion_version_id": latest.assertion_version_id,
                "errors": policy_errors,
                "limitations": [
                    "assertion_semantic_policy_rejected",
                    "old_latest_preserved",
                ],
            }
            self.append_record("assertion_revision_rejected", {**result, "reason": reason})
            return result
        formal_metadata = {
            "basis_ids": list(latest.basis_ids),
            "required_function_families": list(next_function_families),
            "formal_property_kind": formal_property_kind,
            "formal_bound": formal_bound,
            "formal_bound_origin": formal_bound_origin,
            "formal_assumption_basis_ids": list(
                formal_assumption_basis_ids or []
            ),
            "rationale": reason,
        }
        formal_errors = _formal_metadata_errors(
            formal_metadata,
            expression=assert_text,
            coverage_requirements=self.coverage_requirements,
            known_basis_ids=(
                self.input_segment_ids
                | set(self.coverage_requirements)
                | self.known_source_fact_ids
            ),
            assertion_basis_ids=set(latest.basis_ids),
        )
        if formal_errors:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "assertion_chain_id": assertion_chain_id,
                "latest_preserved_assertion_version_id": latest.assertion_version_id,
                "errors": formal_errors,
                "limitations": [
                    "formal_metadata_rejected",
                    "old_latest_preserved",
                ],
            }
            self.append_record(
                "assertion_revision_rejected", {**result, "reason": reason}
            )
            return result
        weakened_fact_ids = [
            fact_id
            for fact_id in latest.basis_ids
            if fact_id in self.source_fact_ids
            and fact_id in self.source_fact_details
            and _assertion_directly_verifies_source_fact(
                latest.assert_text,
                set(latest.required_function_families),
                self.source_fact_details.get(fact_id, {}),
            )
            and not _assertion_directly_verifies_source_fact(
                assert_text,
                set(latest.required_function_families),
                self.source_fact_details.get(fact_id, {}),
            )
        ]
        if weakened_fact_ids:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "assertion_chain_id": assertion_chain_id,
                "latest_preserved_assertion_version_id": latest.assertion_version_id,
                "errors": [
                    "source_fact_direct_evidence_weakened:"
                    + ",".join(sorted(weakened_fact_ids))
                ],
                "limitations": [
                    "semantic_weakening_rejected",
                    "old_latest_preserved",
                ],
            }
            self.append_record(
                "assertion_revision_rejected", {**result, "reason": reason}
            )
            return result
        if "fbmcq(" in assert_text and not self.fbmcq_guide_read():
            result = {
                "execution_status": "prerequisite_required",
                "accepted": False,
                "assertion_chain_id": assertion_chain_id,
                "latest_preserved_assertion_version_id": latest.assertion_version_id,
                "limitations": [
                    "read_fbmcq_guide_before_registering_or_revising_fbmcq"
                ],
            }
            self.append_record("assertion_revision_rejected", {**result, "reason": reason})
            return result
        digest = sha256_text(assert_text)
        for other in self.latest_versions():
            if other.assertion_chain_id != assertion_chain_id and (other.assert_text == assert_text or other.assert_sha256 == digest):
                result = {
                    "execution_status": "invalid_arguments",
                    "accepted": False,
                    "assertion_chain_id": assertion_chain_id,
                    "attempted_assert_sha256": digest,
                    "conflicting_assertion_chain_id": other.assertion_chain_id,
                    "latest_preserved_assertion_version_id": latest.assertion_version_id,
                    "limitations": ["duplicate_latest_expression", "old_latest_preserved"],
                }
                self.append_record("assertion_revision_rejected", {**result, "reason": reason})
                return result
        if latest.assert_text == assert_text:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "assertion_chain_id": assertion_chain_id,
                "latest_preserved_assertion_version_id": latest.assertion_version_id,
                "limitations": ["same_expression_revision_rejected", "old_latest_preserved"],
            }
            self.append_record("assertion_revision_rejected", {**result, "reason": reason})
            return result
        version_no = len(self.chains[assertion_chain_id]) + 1
        version = AssertionVersion(
            assertion_chain_id=assertion_chain_id,
            assertion_version_id=f"{assertion_chain_id}@v{version_no}",
            root_node_id=latest.root_node_id,
            coverage_unit_id=latest.coverage_unit_id,
            required=latest.required,
            assert_text=assert_text,
            assert_sha256=digest,
            basis_ids=latest.basis_ids,
            obligation_signature=latest.obligation_signature,
            required_function_families=next_function_families,
            evidence_scope=_deepcopy_jsonish(latest.evidence_scope),
            rationale=reason,
            record_language=latest.record_language,
            formal_property_kind=formal_property_kind,
            formal_bound=formal_bound,
            formal_bound_origin=formal_bound_origin,
            formal_assumption_basis_ids=tuple(formal_assumption_basis_ids or []),
            supersedes_version_id=latest.assertion_version_id,
        )
        self.chains[assertion_chain_id].append(version)
        self.latest_projection = None
        result = {
            "execution_status": "completed",
            "accepted": True,
            "assertion_chain_id": assertion_chain_id,
            "assertion_version_id": version.assertion_version_id,
            "assert_sha256": digest,
            "inherited": {
                "required": version.required,
                "root_node_id": version.root_node_id,
                "coverage_unit_id": version.coverage_unit_id,
                "basis_ids": list(version.basis_ids),
                "evidence_scope": _deepcopy_jsonish(version.evidence_scope),
                "required_function_families": list(version.required_function_families),
                "previous_required_function_families": list(
                    latest.required_function_families
                ),
                "required_function_families_changed": (
                    version.required_function_families
                    != latest.required_function_families
                ),
                "formal_property_kind": version.formal_property_kind,
                "formal_bound": version.formal_bound,
                "formal_bound_origin": version.formal_bound_origin,
                "formal_assumption_basis_ids": list(
                    version.formal_assumption_basis_ids
                ),
            },
            "limitations": ["append_only_revision", "semantic_weakening_not_automatically_proven"],
        }
        self.append_record(
            "assertion_revision_registered",
            {**result, "reason": reason, "assert": assert_text},
        )
        return result

    def eval_assert(self, assert_text: str, *, reason: str) -> dict[str, Any]:
        matches = self.latest_by_expression(assert_text)
        if len(matches) != 1:
            result = {
                "execution_status": "invalid_arguments",
                "accepted": False,
                "assert_sha256": sha256_text(assert_text),
                "match_count": len(matches),
                "limitations": ["assert_must_match_exactly_one_latest_registered_expression"],
                "reason": reason,
            }
            self.append_record("assertion_evaluation_rejected", result)
            return result
        version = matches[0]
        reason_context = self._make_reason_context(version)
        self.latest_projection = None
        prepared = self.append_record(
            "eval_assert_call_prepared",
            {
                "assertion_chain_id": version.assertion_chain_id,
                "assertion_version_id": version.assertion_version_id,
                "assert_sha256": version.assert_sha256,
                "assert": version.assert_text,
                "formal_property_kind": version.formal_property_kind,
                "formal_bound": version.formal_bound,
                "formal_bound_origin": version.formal_bound_origin,
                "formal_assumption_basis_ids": list(
                    version.formal_assumption_basis_ids
                ),
                "check": _deepcopy_jsonish(
                    self.evidence_context.get("check") or {}
                ),
                "policy": _deepcopy_jsonish(
                    self.evidence_context.get("policy") or {}
                ),
                "reason": reason,
                "reason_context": reason_context,
            },
        )
        runtime_result = self.eval_runtime.evaluate(
            assert_text,
            required_function_families=set(version.required_function_families),
            reason=reason,
            reason_context=reason_context,
        )
        legacy_runtime_hash = sha256_text(type(self.eval_runtime).__name__)
        runtime_result.setdefault("eval_vars_hash_before", legacy_runtime_hash)
        runtime_result.setdefault("eval_vars_hash_after", legacy_runtime_hash)
        runtime_result.setdefault("function_registry_hash", legacy_runtime_hash)
        result = {
            "assertion_chain_id": version.assertion_chain_id,
            "assertion_version_id": version.assertion_version_id,
            "assert_sha256": version.assert_sha256,
            "root_node_id": version.root_node_id,
            "coverage_unit_id": version.coverage_unit_id,
            "prepared_record_id": prepared["record_id"],
            "formal_property_kind": version.formal_property_kind,
            "formal_bound": version.formal_bound,
            "formal_bound_origin": version.formal_bound_origin,
            "formal_assumption_basis_ids": list(
                version.formal_assumption_basis_ids
            ),
            **runtime_result,
        }
        result["formal"] = {
            **_deepcopy_jsonish(result.get("formal") or {}),
            "formal_property_kind": version.formal_property_kind,
            "formal_bound": version.formal_bound,
            "formal_bound_origin": version.formal_bound_origin,
            "formal_assumption_basis_ids": list(
                version.formal_assumption_basis_ids
            ),
        }
        result["check"] = _deepcopy_jsonish(
            self.evidence_context.get("check") or {}
        )
        result["policy"] = _deepcopy_jsonish(
            self.evidence_context.get("policy") or {}
        )
        record = self.append_record("eval_assert_completed", result)
        result["record_id"] = record["record_id"]
        self.evaluations.setdefault(version.assertion_version_id, []).append(result)
        pending = self.missing_latest_required_assertions()
        incomplete = self.incomplete_latest_required_assertions()
        result["missing_latest_required_assertions"] = pending
        result["incomplete_latest_required_assertions"] = incomplete
        result["submit_allowed"] = not pending and not incomplete
        if not pending:
            result["controller_projection"] = self.project_roots()
        return result

    def missing_latest_required_assertions(self) -> list[dict[str, Any]]:
        missing: list[dict[str, Any]] = []
        for version in self.latest_versions():
            if not version.required:
                continue
            if not self.evaluations.get(version.assertion_version_id):
                missing.append(version.to_record())
        return missing

    def incomplete_latest_required_assertions(self) -> list[dict[str, Any]]:
        """Return evaluated latest required assertions without a stable bool verdict."""

        incomplete: list[dict[str, Any]] = []
        for version in self.latest_versions():
            if not version.required:
                continue
            attempts = self.evaluations.get(version.assertion_version_id, [])
            if not attempts:
                continue
            latest = attempts[-1]
            if latest.get("match_status") in {"matches", "contradicts"}:
                continue
            incomplete.append(
                {
                    **version.to_record(),
                    "latest_execution_status": latest.get("execution_status"),
                    "latest_match_status": latest.get("match_status"),
                    "latest_inconclusive_reason": latest.get("inconclusive_reason"),
                    "latest_record_id": latest.get("record_id"),
                }
            )
        return incomplete

    def project_roots(self) -> dict[str, Any]:
        """Project every registered Root from its latest required assertion results."""

        projected: list[dict[str, Any]] = []
        for root_id, raw_root in sorted(self.roots.items()):
            versions = [
                version
                for version in self.latest_versions()
                if version.root_node_id == root_id and version.required
            ]
            results = [
                self.evaluations.get(version.assertion_version_id, [])[-1]
                if self.evaluations.get(version.assertion_version_id)
                else None
                for version in versions
            ]
            incomplete = any(
                result is None or result.get("match_status") == "inconclusive"
                for result in results
            )
            contradicted = any(
                result is not None and result.get("match_status") == "contradicts"
                for result in results
            )
            if incomplete:
                status = "incomplete"
            elif contradicted:
                status = "issue"
            else:
                status = "ok"
            assessment: str | None = None
            repair_allowed = False
            if status == "issue":
                if self.issue_assessment_resolver is None:
                    assessment = "candidate_only"
                else:
                    assessment, repair_allowed = self.issue_assessment_resolver(raw_root)
                repair_allowed = bool(repair_allowed and assessment == "confirmed")
            projected.append(
                {
                    **_deepcopy_jsonish(raw_root),
                    "node_id": root_id,
                    "status": status,
                    "runtime_issue_assessment": assessment,
                    "repair_allowed": repair_allowed,
                    "regression_guard": status == "ok",
                    "assertion_chain_ids": [version.assertion_chain_id for version in versions],
                    "supporting_record_ids": [
                        result["record_id"] for result in results if result is not None
                    ],
                    "rationale": (
                        "Controller projection: at least one required assertion is incomplete."
                        if status == "incomplete"
                        else "Controller projection: at least one required assertion contradicts the positive obligation."
                        if status == "issue"
                        else "Controller projection: all latest required assertions match the positive obligation."
                    ),
                }
            )
        incomplete_roots = [root for root in projected if root["status"] == "incomplete"]
        issue_roots = [root for root in projected if root["status"] == "issue"]
        ok_roots = [root for root in projected if root["status"] == "ok"]
        terminal_chain_ids = {
            version.assertion_chain_id
            for version in self.latest_versions()
            if self._latest_terminal_evaluation(version) is not None
        }
        terminal_requirement_ids = {
            requirement_id
            for requirement_id, chain_ids in self.requirement_assertion_chains.items()
            if chain_ids and bool(chain_ids & terminal_chain_ids)
        }
        terminal_source_fact_ids = {
            fact_id
            for fact_id, chain_ids in self.source_fact_assertion_chains.items()
            if chain_ids and bool(chain_ids & terminal_chain_ids)
        }
        strict_certificate_closed = (
            self.plan_registered
            and (
                not self.strict_coverage_enabled
                or (
                    terminal_requirement_ids == set(self.coverage_requirements)
                )
            )
        )
        review_passed = bool(
            self.semantic_review_gate is not None
            and self.semantic_review_gate.current_passed()
        )
        registered_complete = (
            strict_certificate_closed and not incomplete_roots and review_passed
        )
        run_outcome = (
            "coverage_incomplete"
            if incomplete_roots
            else "issues_found"
            if issue_roots
            else "reviewer_accepted_zero_issue"
        )
        payload = {
            "run_outcome": run_outcome,
            "registered_worklist_complete": registered_complete,
            "major_behavior_coverage_assurance": (
                "controller_closed_dual_llm_reviewed"
                if self.strict_coverage_enabled
                else "agent_declared"
            ),
            "input_segment_coverage": {
                "total": len(self.input_segment_ids),
                "covered": len(self.input_segment_ids),
            },
            "selected_source_fact_evidence_coverage": {
                "total": len(self.selected_source_fact_ids()),
                "covered": len(terminal_source_fact_ids),
                "fact_ids": sorted(terminal_source_fact_ids),
                "scope": "source_facts_selected_as_assertion_evidence",
            },
            "coverage_requirement_coverage": {
                "total": len(self.coverage_requirements),
                "covered": len(terminal_requirement_ids),
                "ratio": (
                    len(terminal_requirement_ids) / len(self.coverage_requirements)
                    if self.coverage_requirements
                    else 1.0
                ),
                "scope": "controller_generated_major_behavior_obligations",
                "requirement_ids": sorted(terminal_requirement_ids),
            },
            "assertion_execution_coverage": {
                "total_required": len(
                    [version for version in self.latest_versions() if version.required]
                ),
                "completed_latest": len(
                    [
                        version
                        for version in self.latest_versions()
                        if version.required
                        and self.evaluations.get(version.assertion_version_id)
                        and self.evaluations[version.assertion_version_id][-1].get(
                            "match_status"
                        )
                        in {"matches", "contradicts"}
                    ]
                ),
            },
            "major_behavior_coverage_review": {
                "required": True,
                "passed": review_passed,
                "reviewed_state_fingerprint": (
                    self.semantic_review_gate.latest_result.get(
                        "reviewed_state_fingerprint"
                    )
                    if self.semantic_review_gate is not None
                    and self.semantic_review_gate.latest_result
                    else None
                ),
                "record_id": (
                    self.semantic_review_gate.latest_result.get("record_id")
                    if self.semantic_review_gate is not None
                    and self.semantic_review_gate.latest_result
                    else None
                ),
            },
            "proposition_roots": projected,
            "issue_root_projection": [
                root
                for root in issue_roots
                if root.get("runtime_issue_assessment") == "confirmed"
                and root.get("repair_allowed") is True
            ],
            "regression_guard_projection": ok_roots,
            "incomplete_root_projection": incomplete_roots,
            "rationale": (
                "Deterministic projection from Controller-closed NL obligations, "
                "source facts, and latest assertion execution evidence."
            ),
        }
        self.append_record("root_projection_completed", payload)
        self.latest_projection = _deepcopy_jsonish(payload)
        return payload

    def _latest_terminal_evaluation(
        self, version: AssertionVersion
    ) -> dict[str, Any] | None:
        attempts = self.evaluations.get(version.assertion_version_id, [])
        if not attempts:
            return None
        latest = attempts[-1]
        if latest.get("match_status") not in {"matches", "contradicts"}:
            return None
        return latest

    def assert_submit_allowed(self, *, record: bool = True) -> dict[str, Any]:
        missing = self.missing_latest_required_assertions()
        if missing:
            result = {
                "execution_status": "prerequisite_required",
                "submit_allowed": False,
                "missing_latest_required_assertions": missing,
                "limitations": ["all_latest_required_assertions_must_be_evaluated_before_submit"],
            }
        else:
            projection = self.latest_projection or self.project_roots()
            incomplete = self.incomplete_latest_required_assertions()
            if incomplete:
                result = {
                    "execution_status": "prerequisite_required",
                    "submit_allowed": False,
                    "missing_latest_required_assertions": [],
                    "incomplete_latest_required_assertions": incomplete,
                    "projection": projection,
                    "limitations": [
                        "all_latest_required_assertions_must_be_terminal",
                        "revise_each_inconclusive_assertion_without_weakening",
                    ],
                }
            else:
                review_passed = bool(
                    self.semantic_review_gate is not None
                    and self.semantic_review_gate.current_passed()
                )
                result = {
                    "execution_status": (
                        "completed" if review_passed else "prerequisite_required"
                    ),
                    "submit_allowed": review_passed,
                    "missing_latest_required_assertions": [],
                    "incomplete_latest_required_assertions": [],
                    "projection": projection,
                    "limitations": (
                        []
                        if review_passed
                        else ["current_semantic_coverage_review_must_pass"]
                    ),
                }
        if record:
            self.append_record("discovery_submit_gate_checked", result)
        return result


def _fact_binding_tokens(fact: Mapping[str, Any], model_ref: str) -> set[str]:
    tokens = {
        str(value)
        for key in ("source", "event", "target")
        if (value := fact.get(key))
    }
    ref_body = model_ref.split(":", 1)[-1]
    tokens.update(
        part
        for part in re.split(r"->|[|,]", ref_body)
        if "." in part and not part.isdigit()
    )
    return tokens


def _assertion_directly_verifies_source_fact(
    expression: str,
    declared_families: set[str],
    fact: Mapping[str, Any],
) -> bool:
    """Require a fact-specific executable predicate, not a cited fact ID alone."""

    kind = str(fact.get("fact_kind") or "")
    if not (declared_families & _source_fact_evidence_families(fact)):
        return False
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return False
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    source = _fact_value(fact, "source")
    event = _fact_value(fact, "event")
    target = _fact_value(fact, "target")

    if kind == "state":
        state_ref = _qualified_ref_body(fact, "state:")
        return any(
            _call_name(call) == "states"
            and (
                _call_kw_string(call, "name") == state_ref
                or _call_kw_string(call, "parent") == state_ref
            )
            for call in calls
        ) or (
            state_ref is not None
            and _has_initial_child_comparison(tree, target=state_ref)
        )
    if kind == "event":
        event_ref = _qualified_ref_body(fact, "event:")
        return any(
            (
                _call_name(call) == "events"
                and _call_kw_string(call, "name") == event_ref
            )
            or (
                _call_name(call) in {"transitions", "transition_exists"}
                and _call_kw_string(call, "event") == event_ref
            )
            for call in calls
        )
    if kind == "variable":
        variable_ref = _qualified_ref_body(fact, "variable:")
        short_name = variable_ref.rsplit(".", 1)[-1] if variable_ref else None
        return any(
            (
                _call_name(call) == "variables"
                and _call_kw_string(call, "name") in {variable_ref, short_name}
            )
            or (
                _call_name(call) in {"effects", "effect_delta"}
                and _call_kw_string(call, "variable") in {variable_ref, short_name}
            )
            for call in calls
        )
    if kind in {"transition", "forced_transition"}:
        if source == "[*]":
            return target is not None and _has_initial_child_comparison(tree, target=target)
        return any(
            _call_name(call) in {"transitions", "transition_exists"}
            and _call_kw_string(call, "source") == source
            and _call_kw_string(call, "target") == target
            and (
                _call_kw_string(call, "event") == event
                if event is not None
                else (
                    _call_kw_is_none(call, "event")
                    or _call_result_checks_eventless(tree, call)
                )
            )
            for call in calls
        )
    if kind == "initial_relation":
        return source is not None and target is not None and any(
            _call_name(call) == "initial_child"
            and _call_pos_string(call, 0) == source
            and _comparison_contains_string(tree, call, target)
            for call in calls
        )
    if kind == "hierarchy":
        return source is not None and target is not None and (
            any(
                _call_name(call) == "states"
                and _call_kw_string(call, "parent") == source
                and _call_kw_string(call, "name") == target
                and _call_kw_bool(call, "recursive") is False
                for call in calls
            )
            or _states_parent_path_comparison(
                tree,
                state_ref=target,
                parent_ref=source,
            )
        )
    if kind == "region":
        region_ref = _qualified_ref_body(fact, "region:")
        return any(
            _call_name(call) == "states"
            and _call_kw_string(call, "parent") == source
            and region_ref is not None
            and region_ref in _string_literals(tree)
            for call in calls
        )
    if kind == "guard":
        guard = _fact_value(fact, "guard")
        return guard is not None and guard in _string_literals(tree) and any(
            _call_name(call) == "transitions"
            and _call_kw_string(call, "source") == source
            and _call_kw_string(call, "target") == target
            and (event is None or _call_kw_string(call, "event") == event)
            for call in calls
        )
    if kind == "effect":
        effects = {str(item) for item in fact.get("effects", []) if item}
        return bool(effects & _string_literals(tree)) and any(
            _call_name(call) in {"effects", "effect_delta", "transitions"}
            and _call_kw_string(call, "source") == source
            and _call_kw_string(call, "target") == target
            and (event is None or _call_kw_string(call, "event") == event)
            for call in calls
        )
    return False


def _registration_required_actions(
    errors: list[str],
    *,
    source_fact_details: Mapping[str, Mapping[str, Any]],
    coverage_requirements: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Turn terse rejection codes into exact, controller-grounded next actions."""

    actions: list[dict[str, Any]] = []
    for ordinal, error in enumerate(errors, start=1):
        if error.startswith("source_fact_not_directly_verified:"):
            fact_id = error.rsplit(":", 1)[-1]
            fact = source_fact_details.get(fact_id, {})
            fact_kind = str(fact.get("fact_kind") or "unknown")
            actions.append(
                {
                    "action_id": f"REG-ACTION-{ordinal:03d}",
                    "error": error,
                    "related_ids": [fact_id],
                    "problem": "A cited behavior SourceFact has no exact executable predicate.",
                    "fact_kind": fact_kind,
                    "fact_snapshot": _deepcopy_jsonish(fact),
                    "compatible_function_families": sorted(
                        _source_fact_evidence_families(fact)
                    ),
                    "accepted_predicate_examples": _source_fact_predicate_examples(fact),
                    "recommended_tools": ["register_coverage_plan"],
                    "recommended_action": (
                        "Add the fact ID to one required assertion basis and use an "
                        "exact predicate matching the frozen fact tuple; keep the "
                        "fact in its CoverageUnit."
                    ),
                    "pass_criteria": (
                        "The next complete plan directly verifies this exact fact "
                        "with a compatible family and no weaker wildcard predicate."
                    ),
                }
            )
            continue
        if error.startswith("uncovered_coverage_requirements:"):
            requirement_ids = [item for item in error.split(":", 1)[-1].split(",") if item]
            actions.append(
                {
                    "action_id": f"REG-ACTION-{ordinal:03d}",
                    "error": error,
                    "related_ids": requirement_ids,
                    "problem": "One or more frozen coverage requirements are absent from the registered Unit/Root/assertion coverage.",
                    "requirement_snapshots": [
                        _deepcopy_jsonish(coverage_requirements.get(requirement_id, {}))
                        for requirement_id in requirement_ids
                    ],
                    "recommended_tools": ["register_coverage_plan"],
                    "recommended_action": (
                        "Expand the complete plan: for each listed requirement, add it "
                        "to exactly one same-clause CoverageUnit, include it in that "
                        "Unit's dimensions/statement, and cite the requirement ID in "
                        "at least one required same-Unit assertion basis whose evidence "
                        "family satisfies the requirement options."
                    ),
                    "coverage_improvement": (
                        "This increases hard NL/cue coverage by converting omitted "
                        "frozen requirements into executable positive assertions."
                    ),
                    "pass_criteria": (
                        "The next complete registration covers every listed requirement "
                        "exactly once at Unit level and has at least one required same-Unit "
                        "assertion basis/evidence route for each listed ID."
                    ),
                }
            )
            continue
        if error.startswith("assertion_semantic_policy:"):
            actions.append(
                _semantic_policy_required_action(
                    error,
                    ordinal=ordinal,
                    coverage_requirements=coverage_requirements,
                )
            )
            continue
        if error.startswith("assertion_effect_variable_not_in_model:"):
            _, chain_id, variable = error.split(":", 2)
            actions.append(
                {
                    "action_id": f"REG-ACTION-{ordinal:03d}",
                    "error": error,
                    "related_ids": [chain_id],
                    "problem": (
                        f"Assertion {chain_id} probes literal variable {variable!r}, "
                        "which is absent from the frozen model inventory."
                    ),
                    "recommended_tools": ["register_coverage_plan"],
                    "recommended_action": (
                        "Remove the invented literal variable. If the frozen model "
                        "contains a source-grounded variable, use its exact name with "
                        "effect_delta; otherwise use effect_deltas over the exact "
                        "source/event/target tuple so absence remains a traced False."
                    ),
                    "accepted_predicate_examples": [
                        "any(delta < 0 for _, delta in effect_deltas("
                        "source='Root.Attack', event='Root.Done', target='Root.Searching'))"
                    ],
                    "coverage_improvement": (
                        "The revised assertion covers the complete observed effect "
                        "inventory instead of manufacturing evidence through a probe name."
                    ),
                    "pass_criteria": (
                        "Every literal effect_delta variable exists in the frozen model, "
                        "or the assertion uses effect_deltas without a variable-name probe."
                    ),
                }
            )
            continue
        if error.startswith(
            "assertion_effect_transition_not_grounded_by_unit_facts:"
        ):
            _, chain_id, source, event, target = error.split(":", 4)
            actions.append(
                {
                    "action_id": f"REG-ACTION-{ordinal:03d}",
                    "error": error,
                    "related_ids": [chain_id],
                    "problem": (
                        f"Assertion {chain_id} queries effect deltas on transition "
                        f"{source} / {event} / {target}, but that exact transition "
                        "is absent from the CoverageUnit's frozen SourceFacts."
                    ),
                    "recommended_tools": ["register_coverage_plan"],
                    "recommended_action": (
                        "Use the frozen SourceFact snapshot and read_task inventory to identify the exact transition implementing "
                        "the linked NL obligation. Bind effect_deltas to that literal "
                        "source/event/target tuple and include its transition/effect "
                        "SourceFact in the same CoverageUnit before registering again."
                    ),
                    "coverage_improvement": (
                        "This prevents an unrelated decrement elsewhere in the model "
                        "from satisfying the current effect Root."
                    ),
                    "pass_criteria": (
                        "The queried effect_deltas tuple exactly matches one transition "
                        "or effect SourceFact in the same CoverageUnit."
                    ),
                }
            )
            continue
        if error.startswith("assertion_cardinality_parent_not_grounded_by_root:"):
            _, chain_id, parent, root_id = error.split(":", 3)
            actions.append(
                {
                    "action_id": f"REG-ACTION-{ordinal:03d}",
                    "error": error,
                    "related_ids": [chain_id, root_id],
                    "problem": (
                        f"Assertion {chain_id} counts direct children under {parent}, "
                        f"but Root {root_id} does not exactly ground state:{parent}."
                    ),
                    "recommended_tools": ["register_coverage_plan"],
                    "recommended_action": (
                        "Use the frozen requirement and SourceFact inventory to identify the exact parent state denoted by "
                        "the NL cardinality obligation. Count its complete direct child "
                        "scope and bind the same exact state ref in the Root; do not use "
                        "a prefix-sharing or nested unrelated parent."
                    ),
                    "coverage_improvement": (
                        "This aligns the counted hierarchy scope with the Root's frozen "
                        "model element instead of relying on substring coincidence."
                    ),
                    "pass_criteria": (
                        f"The assertion parent is exactly one state ref in {root_id}, "
                        "with recursive=False and no name filter."
                    ),
                }
            )
            continue
        if error.startswith("coverage_requirement_evidence_family_unsatisfied:"):
            parts = error.split(":", 2)
            requirement_id = parts[1] if len(parts) > 1 else "unknown"
            requirement = coverage_requirements.get(requirement_id, {})
            actions.append(
                {
                    "action_id": f"REG-ACTION-{ordinal:03d}",
                    "error": error,
                    "related_ids": [requirement_id],
                    "problem": "The requirement is linked only to incompatible evidence families.",
                    "required_function_family_options": _deepcopy_jsonish(
                        requirement.get("required_function_family_options", [])
                    ),
                    "recommended_tools": ["register_coverage_plan"],
                    "recommended_action": (
                        "Link the requirement ID in basis_ids to a same-Unit required "
                        "assertion whose declared families satisfy one complete option."
                    ),
                    "pass_criteria": (
                        "At least one linked required assertion declares every family "
                        "from one allowed option without weakening the NL proposition."
                    ),
                }
            )
            continue
        actions.append(
            {
                "action_id": f"REG-ACTION-{ordinal:03d}",
                "error": error,
                "related_ids": [],
                "problem": "The complete coverage plan violates a deterministic registration gate.",
                "recommended_tools": ["register_coverage_plan"],
                "recommended_action": (
                    "Correct the named contract violation in the complete plan; do "
                    "not delete the implicated requirement, fact, Unit, Root, or chain. "
                    "If the error names omitted IDs, expand the plan with same-clause "
                    "Units, positive Roots, required assertion bases, and compatible "
                    "evidence instead of narrowing scope."
                ),
                "coverage_improvement": (
                    "The correction must add or repair executable coverage for the "
                    "implicated frozen obligation; pure wording changes or deletion do not count."
                ),
                "pass_criteria": (
                    "The next complete registration no longer returns this exact "
                    "error and preserves all frozen obligations."
                ),
            }
        )
    for action in actions:
        action.setdefault(
            "coverage_improvement",
            "Following this action turns the named rejected obligation into "
            "executable evidence without narrowing the major-behavior scope.",
        )
    return actions


def _source_fact_evidence_families(fact: Mapping[str, Any]) -> frozenset[str]:
    """Return the executable family that can prove this exact fact shape."""

    kind = str(fact.get("fact_kind") or "")
    if kind in {"transition", "forced_transition"} and _fact_value(fact, "source") == "[*]":
        return frozenset({"structure"})
    return SOURCE_FACT_EVIDENCE_FAMILIES.get(kind, frozenset())


def _semantic_policy_required_action(
    error: str,
    *,
    ordinal: int,
    coverage_requirements: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Explain one semantic-policy rejection as an executable coverage repair."""

    parts = error.split(":")
    chain_id = parts[1] if len(parts) > 1 else "unknown"
    code = parts[2] if len(parts) > 2 else "unknown"
    requirement_id = parts[3] if len(parts) > 3 else ""
    requirement = coverage_requirements.get(requirement_id, {})
    templates: dict[str, tuple[list[str], str, list[str], str]] = {
        assertion_contract.ERROR_ASSERTION_DIRECT_SHAPE_REQUIRED: (
            ["register_coverage_plan"],
            "Replace the disjunctive, filtered, or nested bypass with one direct positive proposition whose top-level bool is determined by the implicated cardinality/effect check. Split unrelated alternatives into separate Roots instead of joining them with or.",
            ["len(states(parent='Root.Searching', recursive=False)) == 3"],
            "The revised assertion has one direct top-level positive comparison (or one unfiltered open effect any-expression), so no unrelated branch can make it pass.",
        ),
        assertion_contract.ERROR_SYNTAX_INVALID: (
            ["register_coverage_plan"],
            "Rewrite the named assertion as one valid Python expression before resubmitting the complete plan.",
            ["len(states(name='Root.Searching')) == 1"],
            "The named assertion parses in eval mode and the complete plan preserves every obligation.",
        ),
        assertion_contract.ERROR_SIMULATE_FIRST_CYCLE_REQUIRED: (
            ["register_coverage_plan"],
            "Use one complete simulation setup: a cold start begins with an explicit empty initialization cycle, while a hot start supplies one exact literal initial_state and complete literal initial_vars and needs no leading empty cycle. For a local event-causality proposition, put the event in the first hot-start caller cycle so completion cannot leave the source state before the event.",
            [
                "simulate(cycles=[[], ['Root.Start']]).final.is_active('Root.Active')",
                "simulate(initial_state='Root.Idle', initial_vars={}, cycles=[['Root.Start']]).final.is_active('Root.Active')",
            ],
            "Every simulate call uses either a valid cold initialization or a complete exact hot start, and a local event-causality check does not insert an empty cycle before its tested event.",
        ),
        assertion_contract.ERROR_EFFECTS_BOOL_SUBSTITUTE: (
            ["register_coverage_plan"],
            "Do not treat bool(effects(...)) as proof of a directional update. Replace it with an exact variable-specific effect_delta comparison.",
            ["(effect_delta(source='Root.Attack', event='Root.Done', variable='count') or 0) < 0"],
            "The assertion checks the required variable and update direction, rather than effect presence alone.",
        ),
        assertion_contract.ERROR_EFFECT_DELTA_DIRECTION_REQUIRED: (
            ["register_coverage_plan"],
            "Add an effect_delta comparison whose sign matches the NL cue: use < 0 for a decrease and > 0 for an increase, bound to the exact source, event, and real model variable. If the variable is unclear, query the model/effect inventory first; prefer the open-ended effect_deltas route when available instead of probing made-up variable names.",
            ["any(delta < 0 for _, delta in effect_deltas(source='Root.Attack', event='Root.Done', target='Root.Searching'))"],
            "The named assertion contains a direction-sensitive predicate over the complete observed effect inventory for the implicated requirement.",
        ),
        assertion_contract.ERROR_EFFECT_DELTA_SENTINEL_VARIABLE: (
            ["register_coverage_plan"],
            "Remove literal sentinel/probe variables from effect_delta. First inspect real model variables or use open-ended effect_deltas to enumerate observed deltas, then bind the assertion to an actual variable that exists in the current model.",
            ["any(delta < 0 for _, delta in effect_deltas(source='Root.Attack', event='Root.Done', target='Root.Searching'))"],
            "The revised assertion no longer probes a made-up variable and its effect evidence is bound to an actual current-model variable or an open-ended observed delta.",
        ),
        assertion_contract.ERROR_EFFECT_DELTA_LITERAL_VARIABLE_REQUIRED: (
            ["register_coverage_plan"],
            "Do not compute, concatenate, or indirectly select effect_delta.variable. Use one exact literal variable name returned by the frozen model inventory, or replace the probe with an unfiltered effect_deltas expression.",
            ["any(delta < 0 for _, delta in effect_deltas(source='Root.Attack', event='Root.Done', target='Root.Searching'))"],
            "Every effect_delta call uses one exact literal current-model variable, or the direct assertion uses unfiltered effect_deltas without a variable selector.",
        ),
        assertion_contract.ERROR_EFFECT_DELTAS_TRANSITION_BINDING_REQUIRED: (
            ["register_coverage_plan"],
            "Bind every open effect_deltas call to one exact frozen transition using literal source and target plus a literal event (or explicit event=None for an eventless transition). An unqualified model-wide effect search cannot prove the current Root.",
            ["any(delta < 0 for _, delta in effect_deltas(source='Root.Attack', event='Root.Done', target='Root.Searching'))"],
            "The open effect assertion names one exact source/event/target transition and no unrelated model effect can make it pass.",
        ),
        assertion_contract.ERROR_CONTINUITY_EVIDENCE_REQUIRED: (
            ["read_fbmcq_guide", "register_coverage_plan"],
            "Strengthen this single assertion with a continuity matrix. Put at least two distinct initialized progress paths in the same expression, each using simulate(cycles=[[], ...]) with at least two cycles; alternatively, combine at least two distinct FBMCQ response checks in the same expression. Splitting one path per assertion does not satisfy this per-assertion gate.",
            [
                "all([simulate(cycles=[[], ['Root.Path_A']]).final.is_active('Root.Searching'), simulate(cycles=[[], ['Root.Path_B']]).final.is_active('Root.Searching')])",
                "all([fbmcq('check response <= 4: trigger event(\"Root.Path_A\", current) -> within 2 active(\"Root.Searching\");').holds is True, fbmcq('check response <= 4: trigger event(\"Root.Path_B\", current) -> within 2 active(\"Root.Searching\");').holds is True])",
            ],
            "The named assertion itself contains at least two distinct initialized simulation paths or at least two response properties and preserves the full continuity obligation.",
        ),
        assertion_contract.ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK: (
            ["read_fbmcq_guide", "register_coverage_plan"],
            "Replace exists_always with path-sensitive response obligations. Existential survival on one path cannot prove continuity across the relevant progress paths.",
            ["all([fbmcq('check response <= 4: trigger event(\"Root.Path_A\", current) -> within 2 active(\"Root.Searching\");').holds is True, fbmcq('check response <= 4: trigger event(\"Root.Path_B\", current) -> within 2 active(\"Root.Searching\");').holds is True])"],
            "The assertion uses non-existential response evidence covering the relevant progress paths.",
        ),
        assertion_contract.ERROR_CARDINALITY_COMPARISON_REQUIRED: (
            ["register_coverage_plan"],
            "Use a direct len(states(...)) comparison with the exact number and direction stated by the NL, and set recursive=False when counting direct children.",
            ["len(states(parent='Root.Searching', recursive=False)) == 3"],
            "The assertion performs the required exact, lower-bound, or upper-bound structural count over the implicated model scope.",
        ),
        assertion_contract.ERROR_CARDINALITY_STABLE_SCOPE_REQUIRED: (
            ["register_coverage_plan"],
            "Do not make cardinality pass by filtering or enumerating exactly the expected names. Count one complete stable model-definition scope, such as direct child states under one parent with recursive=False, and compare that full scope to the NL quantity.",
            ["len(states(parent='Root.Searching', recursive=False)) == 3"],
            "The assertion counts the complete stable scope that the NL quantity ranges over; it does not use name filters, literal lists, set membership filters, or hand-picked known elements to force len(...) to equal the expected number.",
        ),
        assertion_contract.ERROR_CARDINALITY_OBJECT_SCOPE_REQUIRED: (
            ["register_coverage_plan"],
            "Bind the quantity to the model object named by the frozen NL clause: areas/modes/regions map to states, events to events, variables/counters to variables, and explicit transitions to transitions. Do not count bound_model_refs or a different object kind.",
            ["len(states(parent='Root.Searching', recursive=False)) == 3"],
            "The direct len(...) operand is the complete model-definition collection for the NL-named object kind, not a plan-derived binding set or an unrelated inventory.",
        ),
        assertion_contract.ERROR_TRANSITION_TARGET_REQUIRED: (
            ["register_coverage_plan"],
            "Bind the transition check to both an exact source and target; include the event when the NL provides a trigger.",
            ["transition_exists(source='Root.Searching', event='Root.Start', target='Root.Active')"],
            "The assertion checks the intended source-to-target behavior rather than event presence alone.",
        ),
        assertion_contract.ERROR_CONDITION_TRIGGER_REQUIRED: (
            ["register_coverage_plan"],
            "Bind the condition to its executable trigger: include the exact event in a transition query, an event-bearing simulation cycle, or an equivalent formal response trigger.",
            ["transition_exists(source='Root.Searching', event='Root.Start', target='Root.Active')"],
            "The assertion explicitly connects the NL condition or trigger to the checked behavior.",
        ),
    }
    tools, action, examples, criteria = templates.get(
        code,
        (
            ["register_coverage_plan"],
            "Correct the named semantic-policy violation without deleting or weakening the implicated obligation.",
            [],
            "The next complete registration no longer returns this exact error and preserves all frozen obligations.",
        ),
    )
    related_ids = [chain_id]
    if requirement_id:
        related_ids.append(requirement_id)
    return {
        "action_id": f"REG-ACTION-{ordinal:03d}",
        "error": error,
        "related_ids": related_ids,
        "problem": (
            f"Assertion {chain_id} does not provide the evidence strength required "
            f"by {requirement_id or 'its linked requirement'}."
        ),
        "requirement_snapshot": _deepcopy_jsonish(requirement),
        "recommended_tools": tools,
        "recommended_action": action,
        "accepted_predicate_examples": examples,
        "coverage_improvement": (
            "Following this action adds direct evidence for the implicated semantic "
            "dimension instead of merely changing wording or deleting a hard case."
        ),
        "pass_criteria": criteria,
    }


def _model_variable_names(
    source_fact_details: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    names: set[str] = set()
    for fact in source_fact_details.values():
        if str(fact.get("fact_kind") or "") != "variable":
            continue
        ref = _qualified_ref_body(fact, "variable:")
        if ref:
            names.update({ref, ref.rsplit(".", 1)[-1]})
    return names


def _literal_effect_delta_variables(expression: str) -> set[str]:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return set()
    return {
        value
        for call in ast.walk(tree)
        if isinstance(call, ast.Call) and _call_name(call) == "effect_delta"
        if (value := _call_kw_string(call, "variable")) is not None
    }


def _effect_deltas_transition_bindings(
    expression: str,
) -> tuple[tuple[str, str | None, str], ...]:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return ()
    bindings: list[tuple[str, str | None, str]] = []
    for call in ast.walk(tree):
        if not isinstance(call, ast.Call) or _call_name(call) != "effect_deltas":
            continue
        source = _call_kw_string(call, "source")
        target = _call_kw_string(call, "target")
        event = _call_kw_string(call, "event")
        event_is_none = any(
            keyword.arg == "event"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is None
            for keyword in call.keywords
        )
        if source and target and (event is not None or event_is_none):
            bindings.append((source, event, target))
    return tuple(bindings)


def _cardinality_state_parent_bindings(expression: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return ()
    parents = {
        parent
        for call in ast.walk(tree)
        if isinstance(call, ast.Call) and _call_name(call) == "states"
        if (parent := _call_kw_string(call, "parent")) is not None
    }
    return tuple(sorted(parents))


def _unit_facts_contain_transition_binding(
    fact_ids: set[str],
    source_fact_details: Mapping[str, Mapping[str, Any]],
    *,
    source: str,
    event: str | None,
    target: str,
) -> bool:
    for fact_id in fact_ids:
        fact = source_fact_details.get(fact_id, {})
        if str(fact.get("fact_kind", "")) not in {
            "transition",
            "forced_transition",
            "effect",
        }:
            continue
        if (
            _fact_value(fact, "source") == source
            and _fact_value(fact, "event") == event
            and _fact_value(fact, "target") == target
        ):
            return True
    return False


def _source_fact_predicate_examples(fact: Mapping[str, Any]) -> list[str]:
    kind = str(fact.get("fact_kind") or "")
    source = _fact_value(fact, "source")
    event = _fact_value(fact, "event")
    target = _fact_value(fact, "target")
    if kind == "state":
        ref = _qualified_ref_body(fact, "state:")
        return [f"len(states(name={ref!r})) == 1"] if ref else []
    if kind == "event":
        ref = _qualified_ref_body(fact, "event:")
        return [f"len(events(name={ref!r})) == 1"] if ref else []
    if kind == "variable":
        ref = _qualified_ref_body(fact, "variable:")
        return [f"len(variables(name={ref!r})) == 1"] if ref else []
    if kind in {"transition", "forced_transition"}:
        if source == "[*]" and target:
            owner = target.rsplit(".", 1)[0] if "." in target else target
            return [f"initial_child({owner!r}) == {target!r}"]
        if source and target:
            return [
                "transition_exists("
                f"source={source!r}, event={event!r}, target={target!r})"
            ]
        return []
    if kind == "initial_relation" and source and target:
        return [f"initial_child({source!r}) == {target!r}"]
    if kind == "hierarchy" and source and target:
        return [
            "len(states("
            f"parent={source!r}, recursive=False, name={target!r})) == 1"
        ]
    if kind == "guard" and source and target:
        guard = _fact_value(fact, "guard")
        return [
            "any(item.guard == "
            f"{guard!r} for item in transitions(source={source!r}, "
            f"event={event!r}, target={target!r}))"
        ]
    if kind == "effect" and source and target:
        effects = [str(item) for item in fact.get("effects", []) if item]
        if effects:
            return [
                f"{effects[0]!r} in effects(source={source!r}, "
                f"event={event!r}, target={target!r})"
            ]
    return []


def _fact_value(fact: Mapping[str, Any], key: str) -> str | None:
    value = fact.get(key)
    return str(value) if value is not None else None


def _qualified_ref_body(fact: Mapping[str, Any], prefix: str) -> str | None:
    for ref in fact.get("qualified_refs", []):
        value = str(ref)
        if value.startswith(prefix):
            return value.removeprefix(prefix)
    return None


def _call_kw_string(call: ast.Call, name: str) -> str | None:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            return keyword.value.value if isinstance(keyword.value.value, str) else None
    return None


def _call_kw_is_none(call: ast.Call, name: str) -> bool:
    return any(
        keyword.arg == name
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is None
        for keyword in call.keywords
    )


def _call_kw_bool(call: ast.Call, name: str) -> bool | None:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            value = keyword.value.value
            return value if isinstance(value, bool) else None
    return None


def _call_name(call: ast.Call) -> str | None:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def _call_pos_string(call: ast.Call, index: int) -> str | None:
    if len(call.args) <= index or not isinstance(call.args[index], ast.Constant):
        return None
    value = call.args[index].value
    return value if isinstance(value, str) else None


def _string_literals(tree: ast.AST) -> set[str]:
    return {
        str(node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }


def _comparison_contains_string(tree: ast.AST, target: ast.AST, value: str) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        members = [node.left, *node.comparators]
        if target not in members:
            continue
        if any(
            isinstance(member, ast.Constant) and member.value == value
            for member in members
        ):
            return True
    return False


def _has_initial_child_comparison(tree: ast.AST, *, target: str) -> bool:
    return any(
        _call_name(call) == "initial_child"
        and _comparison_contains_string(tree, call, target)
        for call in ast.walk(tree)
        if isinstance(call, ast.Call)
    )


def _states_parent_path_comparison(
    tree: ast.AST,
    *,
    state_ref: str,
    parent_ref: str,
) -> bool:
    """Recognize ``states(name=...)[i].parent_path == parent`` predicates."""

    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        members = [node.left, *node.comparators]
        if not any(
            isinstance(member, ast.Constant) and member.value == parent_ref
            for member in members
        ):
            continue
        for member in members:
            if not isinstance(member, ast.Attribute) or member.attr != "parent_path":
                continue
            owner = member.value
            if not isinstance(owner, ast.Subscript) or not isinstance(owner.value, ast.Call):
                continue
            call = owner.value
            if (
                _call_name(call) == "states"
                and _call_kw_string(call, "name") == state_ref
            ):
                return True
    return False


def _call_result_checks_eventless(tree: ast.AST, call: ast.Call) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        if not any(isinstance(op, (ast.Is, ast.Eq)) for op in node.ops):
            continue
        members = [node.left, *node.comparators]
        if not any(
            isinstance(member, ast.Attribute)
            and member.attr == "event"
            and _attribute_owner_contains_call(member, call)
            or (
                isinstance(member, ast.Attribute)
                and member.attr == "event"
                and _attribute_owner_is_comprehension_item_from_call(
                    tree, node, member, call
                )
            )
            for member in members
        ):
            continue
        if any(isinstance(member, ast.Constant) and member.value is None for member in members):
            return True
    return False


def _attribute_owner_contains_call(attribute: ast.Attribute, call: ast.Call) -> bool:
    """Return True when ``attribute`` reads ``.event`` from this exact call result.

    This deliberately does not accept arbitrary ``something.event is None``
    elsewhere in the expression: eventless SourceFact grounding must come from
    the same source/target-bound transition/effect call currently being checked.
    """

    return any(node is call for node in ast.walk(attribute.value))


def _attribute_owner_is_comprehension_item_from_call(
    tree: ast.AST,
    comparison: ast.Compare,
    attribute: ast.Attribute,
    call: ast.Call,
) -> bool:
    """Bind ``item.event`` to this call's comprehension iterator."""

    if not isinstance(attribute.value, ast.Name):
        return False
    owner = attribute.value.id
    for node in ast.walk(tree):
        if not isinstance(
            node,
            (ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp),
        ):
            continue
        if not any(member is comparison for member in ast.walk(node)):
            continue
        for generator in node.generators:
            target_names = {
                member.id
                for member in ast.walk(generator.target)
                if isinstance(member, ast.Name)
            }
            if owner not in target_names:
                continue
            if any(member is call for member in ast.walk(generator.iter)):
                return True
    return False


def _formal_metadata_errors(
    assertion: Mapping[str, Any],
    *,
    expression: str,
    coverage_requirements: Mapping[str, Mapping[str, Any]],
    known_basis_ids: set[str],
    assertion_basis_ids: set[str] | None = None,
) -> list[str]:
    """Validate the one-FBMCQ-per-assertion contract from Issue #165."""

    chain_id = str(assertion.get("assertion_chain_id") or "unknown")
    fields = {
        "formal_property_kind": assertion.get("formal_property_kind"),
        "formal_bound": assertion.get("formal_bound"),
        "formal_bound_origin": assertion.get("formal_bound_origin"),
    }
    basis_ids = [
        str(item)
        for item in assertion.get("formal_assumption_basis_ids", [])
        if item
    ]
    assertion_basis = {
        str(item)
        for item in (
            assertion_basis_ids
            if assertion_basis_ids is not None
            else assertion.get("basis_ids", [])
        )
        if item
    }
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return []
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node) == "fbmcq"
    ]
    if not calls:
        errors = [
            f"formal_metadata_without_fbmcq:{chain_id}:{name}"
            for name, value in fields.items()
            if value is not None
        ]
        if basis_ids:
            errors.append(f"formal_basis_without_fbmcq:{chain_id}")
        return errors
    if len(calls) != 1:
        return [f"formal_fbmcq_call_cardinality:{chain_id}:{len(calls)}"]
    call = calls[0]
    if len(call.args) != 1 or call.keywords:
        return [f"formal_fbmcq_exact_query_required:{chain_id}"]
    query_node = call.args[0]
    if not isinstance(query_node, ast.Constant) or not isinstance(
        query_node.value, str
    ):
        return [f"formal_fbmcq_literal_query_required:{chain_id}"]
    missing = [name for name, value in fields.items() if value is None]
    errors = [f"formal_metadata_missing:{chain_id}:{name}" for name in missing]
    if "formal" not in {
        str(item) for item in assertion.get("required_function_families", [])
    }:
        errors.append(f"formal_function_family_missing:{chain_id}")
    try:
        parsed = parse_bmc_query(query_node.value)
        prop = parsed.property
        parsed_kind = str(prop.kind)
        parsed_bound = int(prop.bound)
        assumptions = tuple(getattr(parsed, "assumptions", ()) or ())
    except Exception as exc:
        errors.append(
            f"formal_query_parse_failed:{chain_id}:{type(exc).__name__}"
        )
        return errors
    if fields["formal_property_kind"] != parsed_kind:
        errors.append(
            f"formal_property_kind_mismatch:{chain_id}:"
            f"declared={fields['formal_property_kind']}:parsed={parsed_kind}"
        )
    if fields["formal_bound"] != parsed_bound:
        errors.append(
            f"formal_bound_mismatch:{chain_id}:"
            f"declared={fields['formal_bound']}:parsed={parsed_bound}"
        )
    unknown_basis = sorted(
        item
        for item in basis_ids
        if item not in known_basis_ids
    )
    if unknown_basis:
        errors.append(
            f"formal_assumption_basis_unknown:{chain_id}:"
            + ",".join(unknown_basis)
        )
    out_of_assertion_basis = sorted(set(basis_ids) - assertion_basis)
    if out_of_assertion_basis:
        errors.append(
            f"formal_assumption_basis_not_in_assertion_basis:{chain_id}:"
            + ",".join(out_of_assertion_basis)
        )
    if assumptions and not basis_ids:
        errors.append(f"formal_assumption_basis_missing:{chain_id}")
    origin = fields["formal_bound_origin"]
    if origin == "requirement_bound":
        requirement_ids = [
            item for item in basis_ids if item in coverage_requirements
        ]
        matching = [
            item
            for item in requirement_ids
            if str(coverage_requirements[item].get("dimension")) == "timing"
            and re.search(
                rf"(?<!\d){parsed_bound}(?!\d)",
                " ".join(
                    str(coverage_requirements[item].get(key) or "")
                    for key in ("clause_text", "cue_text")
                ),
            )
        ]
        if not matching:
            errors.append(
                f"formal_requirement_bound_not_grounded:{chain_id}:{parsed_bound}"
            )
    elif origin == "analysis_bound":
        rationale = str(assertion.get("rationale") or "")
        if str(parsed_bound) not in rationale or not re.search(
            r"\b(?:analysis|bound|finite|horizon)\b", rationale, re.IGNORECASE
        ):
            errors.append(
                f"formal_analysis_bound_rationale_missing:{chain_id}:{parsed_bound}"
            )
    elif origin is not None:
        errors.append(f"formal_bound_origin_invalid:{chain_id}:{origin}")
    return errors


def _as_list(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    raise TypeError(f"expected list, got {type(value).__name__}")


def callable_docstring_has_required_sections(func: Callable[..., Any]) -> bool:
    doc = inspect.getdoc(func) or ""
    required = [
        "Purpose",
        "When to use",
        "When not to use",
        "Parameters",
        "Returns",
        "Execution",
        "Failure semantics",
        "Evidence limitations",
        "Permissions",
        "Examples",
    ]
    return all(section in doc for section in required)
