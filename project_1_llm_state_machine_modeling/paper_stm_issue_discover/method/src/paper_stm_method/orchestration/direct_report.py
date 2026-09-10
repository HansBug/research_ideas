"""A3: one report generation, instance execution, deterministic publication."""

from __future__ import annotations

import json
from collections import Counter
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..backends.trajectory import FCSTMRuntimeScenario
from ..compiler.inputs import predicate_input_schema
from ..evidence.audit_bundle import build_audit_bundle, validate_and_hash_w2_audit_bundle
from ..evidence.receipts import build_predicate_execution_receipt
from ..registry import load_registry
from ..semantics.obligations import (
    CandidateIssue, ObligationLocusKind, ObligationProperty, PredicateId,
    ViolationDirection,
)
from utils.artifact_io import write_json

VERSION = "a3-direct-report.v1"
INPUT_CONVENTIONS = {
    "scope": "S1 requires scope=closed_fcstm. S2 accepts closed_fcstm or one exact state scope.",
    "identities": "Use exact model refs or canonical paths from the execution identity catalog; transitions use transition:line:<n>.",
    "S1_kind": ["state", "event", "transition", "edge"],
    "G2_source": "One exact native leaf state; target is an exact native leaf state or set.",
    "R1": "event is the native short event name; step equals scenario.selected_step. All five attribution fields (selected_step, selected_event_path, selected_transition_ref, expected_active_before, expected_active_after) in the scenario must be supplied together.",
    "R2": "stimulus is the exact dispatched event path. window=[start,end] is inclusive, with 0<=start<=end<len(schedule).",
    "R3": "interval=[start,end] is inclusive, with 0<=start<=end<len(schedule).",
    "scenario": "Use cold initialization and the exact model root canonical path. Schedule steps are contiguous from zero; scheduled event paths must be listed in event_queue.",
    "V1": "initial_scope is closed_fcstm, cold, or an exact state scope.",
}
SYSTEM_PROMPT = """Given the supplied natural-language requirements, original author
state machine and inspection, return a complete list of concrete issue reports.
Use the structured response only. Preserve exact requirement and author-source
quotations and identify the location of each claim. Do not invent source facts.
The model scope is finite-control FSM/HSM/EFSM; clocks, timed invariants, orthogonal
concurrency, hybrid and unbounded temporal semantics are outside this scope.
For an applicable registered check, provide its ID and named inputs. Predicate
true means that check is satisfied; false means it is not satisfied. These are
computed by execution, never supplied by you. If the claim is unsupported by the
registered checks, use predicate_id=null and retain the concrete report.
The execution representation and identity catalog serve only exact parameter
binding; author-model claims must cite the original author source. Use the
declared input types. Do not output executable code or evaluation labels.
"""

DISABLED_STEPS = (
    "contract_extraction", "contract_completion", "materialize_segment_coverage",
    "discovery_grounding.contract_structure_contrast",
    "discovery_grounding.behavior_consequence", "materialize_typed_frontier",
    "materialize_domain_invariant_contracts", "source_divergence_candidates",
    "evaluate_source_transition_closure", "route_primary_candidates",
    "_materialize_exact_s2_inventory_candidates",
    "_materialize_deterministic_execution_probes", "_admit_grounding_unresolved",
    "_admit_frontier_unresolved", "coverage_repair", "d_adjudication",
    "d_adjudication_correction", "validate_d", "_fold_consequence_issues",
    "_aggregate_guard_modality_issues",
)

Text = Annotated[str, Field(min_length=1)]


class DirectReport(BaseModel):
    """A claim and its optional registered check, without discovery scaffolding."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: Text
    requirement_quote: Text = Field(description="Exact quotation from supplied NL.")
    source_quote: Text = Field(description="Exact quotation from the original author STM.")
    source_refs: list[Text] = Field(description="Exact supplied source locations.")
    locus_kind: ObligationLocusKind
    locus_names: tuple[Text, ...] = Field(min_length=1)
    property: ObligationProperty
    violation_direction: ViolationDirection
    expected: Text
    observed: Text
    reason: Text
    basis: Text
    predicate_id: PredicateId | None = Field(description="Registered check ID, or null for unsupported.")
    predicate_inputs: dict[str, Any] = Field(description="Named inputs with types from the supplied predicate schema; empty for unsupported. No verdict fields.")
    element_refs: list[Text] = Field(description="Exact executable model references for this instance.")

    @field_validator("predicate_inputs")
    @classmethod
    def reject_answer_fields(cls, values):
        if {"verdict", "predicate_verdict", "result", "d_level", "witness_level"} & values.keys():
            raise ValueError("predicate inputs cannot contain execution or evaluation answers")
        return values

    def candidate(self, index: int) -> CandidateIssue:
        values = self.model_dump(exclude={"source_quote"})
        return CandidateIssue(
            **values, contract_id=f"NL-CONTRACT-A3-{index}",
            evidence_types=("source_identity",),
            strongest_rebuttal="Not requested in direct-report generation.",
        )


class DirectReportResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    issues: list[DirectReport]
    reason: Text
    basis: Text

    @model_validator(mode="before")
    @classmethod
    def decode_complete_tool_parameter(cls, value):
        # Some tool responses embed the complete issues JSON in the reason slot.
        # Decode only this exact envelope; the ordinary schema still checks every field.
        if isinstance(value, dict) and set(value) == {"reason", "basis"} and isinstance(value["reason"], str):
            reason, marker, encoded = value["reason"].partition('</reason>\n<parameter name="issues">')
            if marker:
                return {"reason": reason, "basis": value["basis"], "issues": json.loads(encoded)}
        return value


def predicate_catalog() -> list[dict[str, Any]]:
    return [
        {"id": p.id, "name": p.name, "semantics": p.semantics,
         "required_inputs": p.inputs, "soundness_fragment": p.soundness_fragment,
         "input_schema": predicate_input_schema(p.id)}
        for p in load_registry().predicates.values()
    ]


def prompt_schema_contract() -> dict[str, Any]:
    return {"version": VERSION, "system_prompt": SYSTEM_PROMPT,
            "schema": DirectReportResponse.model_json_schema(),
            "predicates": predicate_catalog(), "input_conventions": INPUT_CONVENTIONS,
            "runtime_scenario_schema": FCSTMRuntimeScenario.model_json_schema()}


def build_prompt(pair) -> str:
    return json.dumps({
        "natural_language": pair.nl_text,
        "author_state_machine": pair.plantuml_text,
        "inspection": {
            "reference": pair.reference_inspection.model_dump(mode="json") if pair.reference_inspection else None,
            "native": pair.inspection_facts.model_dump(mode="json") if pair.inspection_facts else None,
        },
        "execution_representation": pair.fcstm_text,
        "model_identity_catalog": pair.model.to_dict(),
        "predicates": predicate_catalog(),
        "input_conventions": INPUT_CONVENTIONS,
        "runtime_scenario_schema": FCSTMRuntimeScenario.model_json_schema(),
    }, ensure_ascii=False, sort_keys=True)


def execution_candidate(candidate, pair):
    # The prompt's exact projection refs and native paths identify the same state.
    paths = {state.ref: state.canonical_path for state in pair.model.states}
    event_paths = {event.ref: event.canonical_path for event in pair.model.events}
    event_names = {key: event.name for event in pair.model.events for key in (event.ref, event.canonical_path)}

    def native(value, identities):
        if isinstance(value, str):
            return identities.get(value, value)
        if isinstance(value, (list, tuple)):
            return [native(item, identities) for item in value]
        return value

    inputs = dict(candidate.predicate_inputs)
    for key in ("source", "target", "scope", "initial_scope", "state", "roots", "marked"):
        if key in inputs:
            inputs[key] = native(inputs[key], paths)
    if candidate.predicate_id == "S1" and "element" in inputs:
        identities = paths if inputs.get("kind") == "state" else event_paths if inputs.get("kind") == "event" else {}
        inputs["element"] = native(inputs["element"], identities)
    for key in ("triggers", "event"):
        if key in inputs:
            inputs[key] = native(inputs[key], event_names)
    if "stimulus" in inputs:
        inputs["stimulus"] = native(inputs["stimulus"], event_paths)
    if isinstance(inputs.get("scenario"), dict):
        scenario = dict(inputs["scenario"])
        for key in ("root_state", "expected_active_before", "expected_active_after"):
            if key in scenario:
                scenario[key] = native(scenario[key], paths)
        for key in ("event_queue", "selected_event_path"):
            if key in scenario:
                scenario[key] = native(scenario[key], event_paths)
        if isinstance(scenario.get("schedule"), list):
            scenario["schedule"] = [
                {**step, "event_paths": native(step["event_paths"], event_paths)}
                if isinstance(step, dict) and "event_paths" in step else step
                for step in scenario["schedule"]
            ]
        inputs["scenario"] = scenario
    return candidate.model_copy(update={"predicate_inputs": inputs})


def direct_report_cell(*, pair, round_index, runtime, output_root, run_identity):
    # Import only shared execution/receipt helpers; the Full stage graph is never entered.
    from . import runner

    prompt = build_prompt(pair)
    outcome = runtime.call(
        kind="direct_report", schema=DirectReportResponse, system_prompt=SYSTEM_PROMPT,
        prompt=prompt, artifact_id=f"method/{pair.pair_id}/round-{round_index}/direct-report",
        retry_cell_on_provider_error=False,
    )
    response = outcome.response if outcome.succeeded else DirectReportResponse(
        issues=[], reason="Generation failed; no empty success is inferred.",
        basis="provider/schema failure preserved in the call audit",
    )
    retries = [{"stage": outcome.kind, **item} for item in outcome.attempts]
    records, executions, errors = [], [], []
    release_by_key = {}
    for index, report in enumerate(response.issues):
        candidate = report.candidate(index)
        issue_id = f"{pair.pair_id}:r{round_index}:issue:{index}"
        record = {
            **candidate.model_dump(mode="json"), "issue_id": issue_id,
            "source_quote": report.source_quote, "generation_index": index,
            "generation_hash": runner._hash_json(report.model_dump(mode="json")),
            "candidate_reason": report.reason, "candidate_basis": report.basis,
            "d_level": None, "semantic_adjudication": None,
            "internal_d_status": "disabled_by_ablation",
            "issue_emitted": False, "witness_level": "W0",
            "publication_status": "coverage_gap", "final_report_id": None,
        }
        try:
            prepared = runner._prepare_candidate(pair, execution_candidate(candidate, pair), round_index, index, infer_missing_subject=False)
            binding, plan, receipt = (prepared[k] for k in ("binding", "plan", "receipt"))
            execution = build_predicate_execution_receipt(
                pair_id=pair.pair_id, run_id=run_identity["run_id"],
                contract_id=candidate.contract_id, obligation_id=prepared["obligation_id"],
                plan=plan, receipt=receipt, source_attribution=prepared["source_attribution"],
                model_hash=pair.hashes["fcstm"], retry_records=retries,
                independent_semantic_basis=False, binding_precise=binding.precise,
            )
            executions.append(execution)
            source_closed = report.source_quote in pair.plantuml_text and report.requirement_quote in pair.nl_text
            witness = execution["witness_level"] if source_closed else "W0"
            record.update({
                "obligation_id": prepared["obligation_id"],
                "binding": binding.model_dump(mode="json"), "plan": plan.to_dict(),
                "receipt": receipt.to_dict(), "execution_receipt": execution,
                "source_attribution": prepared["source_attribution"],
                "adapted_candidate": prepared["candidate"].model_dump(mode="json"),
                "witness_level": witness, "source_quotes_exact": source_closed,
            })
            passed = not runner._prepared_is_finding_candidate(prepared)
            record["publication_status"] = "filtered_true" if passed else "published" if witness != "W0" else "coverage_gap"
            record["issue_emitted"] = record["publication_status"] == "published"
            record["coverage_class"] = "executable_evidence" if witness == "W2" else "source_backed_unverified" if witness == "W1" else "coverage_gap"
            if witness == "W2":
                bundle = build_audit_bundle(
                    pair=pair, obligation_id=prepared["obligation_id"], binding=binding,
                    plan=plan, receipt=receipt, source_attribution=prepared["source_attribution"],
                    reason=report.reason, basis=report.basis, retry_records=retries,
                    semantic_adjudication=None, execution_receipt=execution,
                )
                bundle["issue_emitted"] = record["issue_emitted"]
                record["audit_bundle"] = validate_and_hash_w2_audit_bundle(bundle)
                path = output_root / "audit_bundles" / f"{issue_id}.json"
                write_json(path, record["audit_bundle"])
                record["audit_bundle_path"] = str(path)
            if record["issue_emitted"]:
                # Merge only identical substantive claims, preserving every generated origin.
                key = runner._hash_json(report.model_dump(exclude={"title", "reason", "basis", "predicate_id", "predicate_inputs", "element_refs"}))
                if key in release_by_key:
                    previous = release_by_key[key]
                    previous["facet_issue_ids"].append(issue_id)
                    record["publication_status"] = "folded_exact_duplicate"
                    record["final_report_id"] = previous["issue_id"]
                else:
                    record["final_report_id"] = issue_id
                    release_by_key[key] = {**record, "facet_issue_ids": [issue_id]}
        except Exception as exc:
            errors.append({"candidate_index": index, "error_type": type(exc).__name__,
                           "message": str(exc), "reason": "Instance execution/publication degraded; original claim retained.",
                           "basis": "A3 candidate-local diagnostic"})
            record["diagnostic"] = errors[-1]
            record.update(issue_emitted=False, publication_status="coverage_gap",
                          final_report_id=None, witness_level="W0", coverage_class="coverage_gap")
        records.append(record)

    release = list(release_by_key.values())
    eligible = bool(outcome.real_llm and outcome.succeeded)
    if not outcome.succeeded:
        errors.append({"stage": "direct_report", "reason": response.reason, "basis": response.basis})
    stages = {
        "ablation": {"mode": "direct-report", "version": VERSION,
                     "disabled_steps": [{"function": name, "status": "disabled_by_ablation"} for name in DISABLED_STEPS]},
        "direct_report": response.model_dump(mode="json"),
        "execute_batch": {"candidate_count": len(records), "execution_count": len(executions),
                          "verdicts": dict(Counter(e["verdict"] for e in executions)),
                          "new_candidate_count": 0},
        "publish": {"report_issue_count": len(release), "report_issue_ids": [r["issue_id"] for r in release],
                    "dispositions": dict(Counter(r["publication_status"] for r in records)),
                    "mapping": [{k: r[k] for k in ("generation_index", "generation_hash", "issue_id", "publication_status", "final_report_id")} for r in records]},
    }
    receipts = [runner._stage_receipt(
        pair=pair, stage_id=f"{pair.pair_id}:r{round_index}:{name}", stage_name=name,
        status="completed" if outcome.succeeded else "failed_with_receipt",
        artifact_roles=("natural_language", "plantuml_source", "fcstm_model", "predicate_registry"),
        output=stages[name], outcome=outcome if name == "direct_report" else None,
        projection_version=VERSION, reason=response.reason, basis=response.basis,
    ) for name in ("direct_report", "execute_batch", "publish")]
    cell = {
        "schema": runner.METHOD_CELL_SCHEMA, "ablation": "direct-report",
        **{k: run_identity[k] for k in ("run_id", "run_contract_hash", "source_provenance")},
        "pair_id": pair.pair_id, "pair_input_hash": pair.context_manifest.manifest_hash,
        "round": round_index,
        "status": "completed_with_diagnostics" if eligible and errors else "completed" if eligible else "failed_with_receipt",
        "prompt_hash": runner._hash_json(prompt),
        "context_manifest": pair.context_manifest.model_dump(mode="json"),
        "input_hashes": dict(pair.hashes), "stage_outputs": stages, "stage_receipts": receipts,
        "model_output": response.model_dump(mode="json"), "llm_calls": [outcome.to_dict()],
        "llm_call": runner._aggregate_outcomes([outcome]), "eligible": eligible,
        "eligibility_reasons": ["real_direct_report_output" if eligible else "generation_unavailable_or_fixture"],
        "evidence_records": records, "predicate_execution_receipts": executions,
        "report_issue_clusters": release, "errors": errors, "reason": response.reason, "basis": response.basis,
    }
    cell = runner.MethodCellReceipt.model_validate(cell).model_dump(mode="json")
    write_json(output_root / "method" / pair.pair_id / f"round-{round_index}.json", cell)
    return cell
