from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from typing import Any, Mapping

from .context import freeze_task_snapshot, validate_reference_blind
from .coverage_requirements import (
    COVERAGE_REQUIREMENT_VERSION,
    build_coverage_requirements,
)
from .eval_env import EvalEnvironment
from .inputs import PreparedCase
from .nl_segmenter import SegmenterResult, segment_nl
from .pyfcstm_adapter import sha256_text
from .records import RecordStore, sha256_json
from .schemas.coverage import CoverageRequirement, InputSegment, SourceFact
from .source_inventory import build_source_inventory
from .tools.coverage_registry import (
    SOURCE_FACT_EVIDENCE_FAMILIES,
    CoverageRegistry,
    DirectEvalRuntime,
)
from .tools.guide_access import GuideAccessState


@dataclass(frozen=True)
class FrozenDiscoverInputs:
    """Controller-owned deterministic inputs for one B-discover attempt."""

    segmenter: SegmenterResult
    input_segments: tuple[InputSegment, ...]
    coverage_requirements: tuple[CoverageRequirement, ...]
    source_facts: tuple[SourceFact, ...]
    source_inventory_sha256: str
    source_mappings: tuple[dict[str, Any], ...]


class DiscoverController:
    """Deterministic boundary around the single B-discover LLM Agent.

    Purpose
    -------
    Freeze current-run inputs, mechanically segment NL, inventory structured
    source/FCSTM facts, own the append-only coverage/assertion registry, execute
    registered assertions in one frozen eval environment, and project the final
    runtime outcome.  This class is not an Agent and never interprets NL.

    Parameters
    ----------
    ``case`` is the immutable prepared input pair, ``manifest`` is the immutable
    run manifest, ``check_result`` is the current pyfcstm structured preflight,
    and ``store`` is the single-writer append-only run record store.

    Returns
    -------
    ``prepare`` returns the frozen deterministic input bundle; ``task_snapshot``
    returns the six-field Agent context; ``registry`` exposes only the registered
    coverage/eval workflow used by Agent-facing tools; ``projection`` returns the
    deterministic Root/run outcome.

    Execution
    ---------
    The Controller uses syntax-only NL segmentation and public structured
    pyfcstm/source-trace data.  It never creates CoverageUnits, semantic roles,
    Roots, or assertion expressions.  Those are declared by the single Agent and
    accepted only after reference/cardinality/coverage gates pass.

    Failure semantics
    -----------------
    Invalid FCSTM, malformed frozen facts, reference leakage, registry mismatch,
    missing latest assertions, or inconsistent submission fails closed.  No
    partial success is published.

    Evidence limitations
    --------------------
    Controller closure proves the generated major NL cue/dimension worklist and
    its selected evidence have been executed. It does not prove 100% semantic or
    path coverage, define a defect taxonomy, or predict which obligations are issues.

    Permissions
    -----------
    Read-only access to current-run frozen inputs and deterministic pyfcstm
    evaluation; append-only writes below the current run directory. No alternate
    case, hidden gold/reference, Repair, Confirm, or model edit.

    Examples
    --------
    ``DiscoverController(case, manifest, checked, store).prepare()`` creates the
    exact InputSegments/SourceFacts used by one subsequent ``AgentApp.run``.
    """

    def __init__(
        self,
        case: PreparedCase,
        manifest: Mapping[str, Any],
        check_result: Mapping[str, Any],
        store: RecordStore,
        *,
        guide_access: GuideAccessState | None = None,
    ) -> None:
        self.case = case
        self.manifest = copy.deepcopy(dict(manifest))
        self.check_result = copy.deepcopy(dict(check_result))
        self.store = store
        self.guide_access = guide_access or GuideAccessState()
        self.frozen: FrozenDiscoverInputs | None = None
        self.registry: CoverageRegistry | None = None
        self.snapshot: dict[str, Any] | None = None

    def prepare(self) -> FrozenDiscoverInputs:
        if self.frozen is not None:
            return self.frozen
        if not self.check_result.get("executable"):
            raise RuntimeError("fcstm_not_executable")

        source_language = str(self.case.metadata.get("nl_language") or "en-US")
        segmented = segment_nl(self.case.nl, language=source_language)
        segments = tuple(InputSegment.model_validate(item) for item in segmented.segments)
        requirements = build_coverage_requirements(segments)

        initial_inventory = build_source_inventory(
            self.check_result,
            source_trace_base=self.case.source_trace,
            relation_policy=None,
            producer_version=self._pyfcstm_version(),
        )
        identity_rows = self._identity_rows(initial_inventory["facts"])
        inventory = build_source_inventory(
            self.check_result,
            source_trace_base=self.case.source_trace,
            relation_policy=self.case.source_trace.get("relation_policy"),
            identity_refs=identity_rows,
            producer_version=self._pyfcstm_version(),
        )
        facts = tuple(SourceFact.model_validate(item) for item in inventory["facts"])
        mappings = tuple(self._mapping_rows(identity_rows))
        self.frozen = FrozenDiscoverInputs(
            segmenter=segmented,
            input_segments=segments,
            coverage_requirements=requirements,
            source_facts=facts,
            source_inventory_sha256=str(inventory["inventory_sha256"]),
            source_mappings=mappings,
        )

        input_sha256 = {
            role: self._input_sha256(role)
            for role in ("nl", "raw_source", "model", "source_trace", "case_metadata")
        }
        self.store.append(
            "inputs_frozen",
            {
                "nl_raw_sha256": input_sha256["nl"],
                "nl_normalized_sha256": segmented.normalized_sha256,
                "model_sha256": input_sha256["model"],
                "raw_source_sha256": input_sha256["raw_source"],
                "source_trace_sha256": input_sha256["source_trace"],
                "case_metadata_sha256": input_sha256["case_metadata"],
                "manifest_input_sha256": input_sha256,
            },
        )
        self.store.append(
            "input_segments_created",
            {
                "schema_version": "paper1.input_segments.v1",
                "segmenter_version": segmented.segmenter_version,
                "raw_sha256": segmented.raw_sha256,
                "normalized_sha256": segmented.normalized_sha256,
                "offset_map": segmented.offset_map,
                "segments": [item.model_dump(mode="json") for item in segments],
            },
        )
        self.store.append(
            "coverage_requirements_created",
            {
                "schema_version": COVERAGE_REQUIREMENT_VERSION,
                "requirements": [
                    item.model_dump(mode="json") for item in requirements
                ],
            },
        )
        self.store.append(
            "source_inventory_created",
            {
                "schema_version": "paper1.source_inventory.v1",
                "inventory_sha256": inventory["inventory_sha256"],
                "facts": [item.model_dump(mode="json") for item in facts],
                "behavior_relevant_fact_ids": [
                    item.fact_id for item in facts if item.behavior_relevant
                ],
            },
        )
        self.store.append(
            "operationalizability_preflight_completed",
            {
                "operationalizable": True,
                "model_sha256": self.case.fcstm_sha256,
                "parse_status": self.check_result.get("parse_status"),
                "semantic_status": self.check_result.get("semantic_status"),
                "inspect_status": self.check_result.get("inspect_status"),
                "limitations": [
                    "fcstm_executable_only",
                    "semantic_obligations_must_close_controller_requirements",
                ],
            },
        )

        fbmcq_limits = dict(self.manifest.get("fbmcq_limits") or {})
        formal_profile = bool(self.manifest.get("formal_profile", True))
        environment = EvalEnvironment(
            model_text=self.case.fcstm,
            model_path="inputs/STM_0.fcstm",
            inspect=self.check_result.get("inspect") or {},
            source_mappings=list(mappings),
            timeout_seconds=None,
            formal_verification_enabled=formal_profile,
            fbmcq_solver_timeout_ms=fbmcq_limits.get("solver_timeout_ms"),
            fbmcq_max_bound=fbmcq_limits.get("max_bound"),
            fbmcq_process_wall_seconds=fbmcq_limits.get(
                "process_wall_seconds"
            ),
        )
        evidence_policy = {
            "policy_id": "paper1-discover-issue165-v1",
            "formal_profile": formal_profile,
            "fbmcq_limits": fbmcq_limits,
            "tool_choice": "proposition_quantification_v1",
        }
        capability_record = self.store.latest("capability_manifest")
        capability_payload = (
            capability_record.get("payload", {})
            if isinstance(capability_record, Mapping)
            else {}
        )
        schema_hashes = (
            capability_payload.get("schema_hashes", {})
            if isinstance(capability_payload, Mapping)
            else {}
        )
        check_evidence_context = {
            "check_result_sha256": sha256_json(self.check_result),
            "check_record_id": self.check_result.get("record_id"),
            "model_sha256": self.case.fcstm_sha256,
            "tool_hash": environment.function_registry_hash,
        }
        if isinstance(schema_hashes, Mapping) and schema_hashes:
            check_evidence_context["tool_schema_hash"] = sha256_json(
                dict(schema_hashes)
            )
        relevant = [item for item in facts if item.behavior_relevant]
        self.registry = CoverageRegistry(
            input_segment_ids=[item.segment_id for item in segments],
            coverage_requirements={
                item.requirement_id: item.model_dump(mode="json")
                for item in requirements
            },
            source_fact_ids=[item.fact_id for item in relevant],
            known_source_fact_ids=[item.fact_id for item in facts],
            source_fact_refs={item.fact_id: item.qualified_refs for item in facts},
            source_fact_kinds={item.fact_id: item.fact_kind for item in facts},
            source_fact_details={
                item.fact_id: item.model_dump(mode="json") for item in facts
            },
            eval_runtime=DirectEvalRuntime(environment),
            model_sha256=self.case.fcstm_sha256,
            record_sink=lambda record_type, payload: self.store.append(
                record_type, payload
            ),
            issue_assessment_resolver=self._resolve_issue_assessment,
            fbmcq_guide_read=lambda: self.guide_access.has_read("fbmcq"),
            evidence_context={
                "check": check_evidence_context,
                "policy": {
                    **evidence_policy,
                    "policy_hash": sha256_json(evidence_policy),
                    "evidence_policy_fingerprint": sha256_json(
                        evidence_policy
                    ),
                },
            },
        )
        self.snapshot = self._build_task_snapshot()
        validate_reference_blind(self.snapshot)
        return self.frozen

    def task_snapshot(self) -> dict[str, Any]:
        self.prepare()
        assert self.snapshot is not None
        return copy.deepcopy(self.snapshot)

    def projection(self, *, record_gate: bool = True) -> dict[str, Any]:
        registry = self.require_registry()
        gate = registry.assert_submit_allowed(record=record_gate)
        if not gate.get("submit_allowed"):
            raise RuntimeError("discover_submit_not_allowed")
        return copy.deepcopy(gate["projection"])

    def require_registry(self) -> CoverageRegistry:
        self.prepare()
        assert self.registry is not None
        return self.registry

    def _build_task_snapshot(self) -> dict[str, Any]:
        assert self.frozen is not None
        formal_profile = bool(self.manifest.get("formal_profile", True))
        fbmcq_limits = dict(self.manifest.get("fbmcq_limits") or {})
        evidence_policy = {
            "policy_id": "paper1-discover-issue165-v1",
            "formal_profile": formal_profile,
            "fbmcq_limits": fbmcq_limits,
            "tool_choice": "proposition_quantification_v1",
        }
        current_records = {
            "nl": {
                "content": self.case.nl,
                "raw_sha256": self.frozen.segmenter.raw_sha256,
                "normalized_content": self.frozen.segmenter.normalized_text,
                "normalized_sha256": self.frozen.segmenter.normalized_sha256,
            },
            "raw_source": {
                "format": self.case.raw_source_format,
                "content": self.case.raw_source,
                "sha256": self._input_sha256("raw_source"),
            },
            "source_trace": copy.deepcopy(self.case.source_trace),
            "input_segments": [
                item.model_dump(mode="json") for item in self.frozen.input_segments
            ],
            "coverage_requirements": [
                item.model_dump(mode="json")
                for item in self.frozen.coverage_requirements
            ],
            "strict_coverage_policy": {
                "schema_version": COVERAGE_REQUIREMENT_VERSION,
                "success_requires": [
                    "all_input_segments_closed",
                    "all_coverage_requirements_closed",
                    "major_nl_behaviors_grounded_by_relevant_source_facts",
                    "all_latest_required_assertions_terminal",
                    "no_incomplete_roots",
                    "current_semantic_coverage_review_passed",
                ],
                "issue_taxonomy_policy": (
                    "Open-world: the Agent discovers issue categories; no fixed "
                    "defect family is Controller-owned or completeness-gating."
                ),
                "requirement_assertion_link_policy": (
                    "Each requirement ID must occur in at least one required "
                    "same-unit assertion basis with a permitted evidence route."
                ),
                "source_fact_direct_evidence_families": {
                    kind: sorted(families)
                    for kind, families in SOURCE_FACT_EVIDENCE_FAMILIES.items()
                },
                "source_fact_assertion_link_policy": (
                    "The complete SourceFact inventory is an exploration pool, not "
                    "a model-wide checklist. Each SourceFact explicitly cited as "
                    "assertion evidence must be directly verified by a compatible "
                    "predicate, and every major NL Root must have relevant grounding."
                ),
                "coverage_claim_boundary": (
                    "Closure means the Controller-generated major behavior worklist "
                    "was executed and reviewer-accepted. It is not a claim of 100% "
                    "coverage over every possible state-machine property or path."
                ),
            },
            "source_inventory": {
                "inventory_sha256": self.frozen.source_inventory_sha256,
                "facts": [
                    item.model_dump(mode="json") for item in self.frozen.source_facts
                ],
            },
            "eval_contract": {
                "positive_bool_principle": (
                    "True means the registered Root obligation is satisfied; "
                    "False means it is contradicted."
                ),
                "function_families": [
                    "structure",
                    "relation",
                    "effect",
                    "simulation",
                    "formal",
                    "mapping",
                ],
                "functions": [
                    "states",
                    "events",
                    "variables",
                    "initial_child",
                    "transitions",
                    "transition_exists",
                    "guards_overlap",
                    "effects",
                    "effect_delta",
                    "effect_deltas",
                    "topology",
                    "path",
                    "simulate",
                    "mapped_source_refs",
                    "mapped_fcstm_refs",
                    "bound_model_refs",
                ]
                + (["fbmcq"] if formal_profile else []),
                "pure_builtins": [
                    "abs",
                    "all",
                    "any",
                    "bool",
                    "float",
                    "int",
                    "iter",
                    "len",
                    "list",
                    "max",
                    "min",
                    "round",
                    "set",
                    "sorted",
                    "str",
                    "sum",
                    "tuple",
                ],
            },
            "run_policy": {
                "formal_profile": bool(self.manifest.get("formal_profile", True)),
                "agent_limits": copy.deepcopy(self.manifest.get("agent_limits") or {}),
                "fbmcq_limits": fbmcq_limits,
                "eval_timeout_seconds": None,
                "check_result_sha256": sha256_json(self.check_result),
                "evidence_policy": evidence_policy,
            },
        }
        return freeze_task_snapshot(
            model_text=self.case.fcstm,
            model_sha256=self.case.fcstm_sha256,
            normalized_inspect=self.check_result.get("inspect") or {},
            current_records=current_records,
        )

    def _input_sha256(self, role: str) -> str:
        manifest_hashes = self.manifest.get("input_sha256")
        if manifest_hashes:
            value = manifest_hashes.get(role)
            if not isinstance(value, str) or len(value) != 64:
                raise ValueError(f"run manifest input hash missing or invalid: {role}")
            return value

        serialized = {
            "nl": self.case.nl,
            "raw_source": self.case.raw_source,
            "model": self.case.fcstm,
            "source_trace": json.dumps(
                self.case.source_trace,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            "case_metadata": json.dumps(
                self.case.metadata,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
        }
        try:
            return sha256_text(serialized[role])
        except KeyError as exc:
            raise ValueError(f"unknown run input hash role: {role}") from exc

    def _identity_rows(self, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not (
            self.case.source_trace.get("relation_policy") == "exact_identity"
            and self.case.raw_source_format == "fcstm-identity"
            and self.case.raw_source == self.case.fcstm
        ):
            return []
        refs = sorted(
            {
                str(ref)
                for fact in facts
                if fact.get("behavior_relevant")
                for ref in fact.get("qualified_refs", [])
                if ref
            }
        )
        return [
            {
                "source_ref": ref,
                "model_ref": ref,
                "source_refs": [ref],
                "model_refs": [ref],
                "relation_policy": "exact_identity",
                "confidence": "exact",
                "producer": "paper1.controller",
            }
            for ref in refs
        ]

    def _mapping_rows(
        self, identity_rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        rows = [
            copy.deepcopy(item)
            for item in self.case.source_trace.get("entries", [])
            if isinstance(item, dict)
        ]
        rows.extend(copy.deepcopy(identity_rows))
        return rows

    def _resolve_issue_assessment(self, root: dict[str, Any]) -> tuple[str, bool]:
        registry = self.require_registry()
        unit = registry.coverage_units.get(str(root.get("coverage_unit_id")), {})
        has_explicit_basis = bool(unit.get("segment_ids") or unit.get("source_fact_ids"))
        model_refs = [str(item) for item in root.get("model_element_refs", []) if item]
        if not has_explicit_basis:
            return "candidate_only", False
        if (
            self.case.source_trace.get("relation_policy") == "exact_identity"
            and self.case.raw_source_format == "fcstm-identity"
            and self.case.raw_source == self.case.fcstm
        ):
            return "confirmed", True

        if not model_refs:
            return "candidate_only", False

        mappings = list(self.frozen.source_mappings if self.frozen else ())
        mapped = {
            str(row.get("model_ref"))
            for row in mappings
            if row.get("model_ref") and row.get("source_ref")
        }
        if model_refs and all(ref in mapped for ref in model_refs):
            return "confirmed", True
        return "candidate_only", False

    def _pyfcstm_version(self) -> str | None:
        capability = self.store.latest("capability_manifest")
        if capability:
            value = capability.get("payload", {}).get("pyfcstm_version")
            return str(value) if value else None
        return None


__all__ = ["DiscoverController", "FrozenDiscoverInputs"]
