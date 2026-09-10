"""A4 controller: restore frozen inputs, then hand only neutral views to the method.

This module is evaluation-owned. The shared method tail receives neither the Full
cell nor its labels/oracle. Historical predicate labels remain unchanged on disk.
"""

from __future__ import annotations

from copy import deepcopy
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
from typing import Any, Literal
from unittest.mock import patch

from pydantic import JsonValue, RootModel

from paper_stm_method.compiler.lowering import PredicatePlan
from paper_stm_method.compiler.inputs import PredicateInputsBase
from paper_stm_method.evidence.receipts import RawReceipt
from paper_stm_method.inputs.models import PairInput, parse_fcstm
from paper_stm_method.orchestration import runner
from paper_stm_method.semantics.binding import BindingResult
from paper_stm_method.semantics.obligations import CandidateIssue, PredicateId
from paper_stm_method.semantics.adjudication import DAdjudicationResponse
from utils.artifact_io import write_json
from utils.structured_runtime import StructuredCallOutcome
from utils.stm_artifacts.context import (
    ContextManifest, ExactSourceInventory, InspectionEquivalentFacts,
    SMTFacts, StructuredArtifact, VerificationFacts, _canonical_source_ir,
    build_numbered_nl_segments,
)

from .predicate_id_mapping import current_predicate_id


TREATMENT = "paper1.a4.all-unknown-tail.v1"


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


class HistoricalCandidate(CandidateIssue):
    """Read-only IDs used by the three retained pre-P1 predicate definitions."""

    predicate_id: PredicateId | Literal["S6", "G4", "R4", "V4"] | None = None


class HistoricalS6Inputs(PredicateInputsBase):
    """Read-only ea6141607 S6 schema; no retired backend is restored."""

    predicate_id: Literal["S6"]
    transition: str | None = None
    effect: tuple[JsonValue, ...] = ()


class HistoricalInputs(RootModel[dict[str, Any]]):
    """Preserve validated historical input bytes without relabeling the payload."""


class HistoricalPlan(PredicatePlan):
    inputs: HistoricalInputs


def restore_plan(raw: dict[str, Any]) -> PredicatePlan:
    mapped = current_predicate_id(raw["registry_version"], raw["predicate_id"])
    if raw["predicate_id"] == "S6":
        HistoricalS6Inputs.model_validate(raw["inputs"])
        plan = HistoricalPlan.model_validate(raw)
    elif raw["predicate_id"] in {"G4", "R4", "V4"}:
        # Validate the retained definition's typed shape under its current label,
        # then restore the original labels. No compiler or backend is called.
        validation = deepcopy(raw)
        validation["predicate_id"] = mapped
        validation["inputs"]["predicate_id"] = mapped
        PredicatePlan.model_validate(validation)
        plan = HistoricalPlan.model_validate(raw)
    else:
        plan = PredicatePlan.model_validate(raw)
    if plan.model_dump(mode="json") != raw:
        raise ValueError("Historical plan deserialization changed its frozen content")
    if plan.execution_state != "not_attempted" or plan.predicate_verdict is not None:
        raise ValueError("Frozen plan unexpectedly contains a runtime result")
    return plan


def restore_pair(source: dict[str, Any], input_root: Path) -> PairInput:
    """Read all twelve hash-bound artifacts; never regenerate inspection facts."""
    manifest = ContextManifest.model_validate(source["context_manifest"])
    if manifest.manifest_hash != source["pair_input_hash"]:
        raise ValueError("Source context identity mismatch")
    payloads, paths, refs = {}, {}, {}
    for ref in manifest.artifacts:
        parts = Path(ref.path).parts
        if parts.count(input_root.name) != 1:
            raise ValueError(f"Cannot relocate frozen input role: {ref.role}")
        relative = Path(*parts[parts.index(input_root.name) + 1:])
        path = (input_root / relative).resolve()
        if not path.is_relative_to(input_root.resolve()):
            raise ValueError("Frozen input escaped its declared root")
        raw = path.read_bytes()
        if "sha256:" + hashlib.sha256(raw).hexdigest() != ref.sha256:
            raise ValueError(f"Frozen input hash mismatch: {ref.role}: {path}")
        payloads[ref.role] = raw.decode() if ref.role in {
            "natural_language", "plantuml_source", "fcstm_model"
        } else json.loads(raw)
        paths[ref.role], refs[ref.role] = path, ref

    def artifact(role: str) -> StructuredArtifact:
        return StructuredArtifact(ref=refs[role], payload=payloads[role])

    pair = PairInput(
        pair_id=source["pair_id"], pair_dir=paths["natural_language"].parent,
        nl_text=payloads["natural_language"], plantuml_text=payloads["plantuml_source"],
        fcstm_text=payloads["fcstm_model"], model=parse_fcstm(payloads["fcstm_model"]),
        hashes=source["input_hashes"], context_manifest=manifest,
        nl_segments=build_numbered_nl_segments(payloads["natural_language"]),
        canonical_source_ir=_canonical_source_ir(payloads["canonical_source_ir"]),
        exact_source_inventory=ExactSourceInventory.model_validate(payloads["source_inventory"]),
        working_contract=artifact("working_contract"), source_trace=artifact("source_trace"),
        case_report=artifact("case_report"), reference_inspection=artifact("reference_inspection_facts"),
        inspection_facts=InspectionEquivalentFacts.model_validate(payloads["inspection_equivalent_facts"]),
        verify_facts=VerificationFacts.model_validate(payloads["verify_facts"]),
        smt_facts=SMTFacts.model_validate(payloads["smt_facts"]),
    )
    for field, role in {
        "nl": "natural_language", "fcstm": "fcstm_model", "plantuml": "plantuml_source",
        "canonical": "canonical_source_ir", "parse_inspect": "reference_inspection_facts",
        "source_trace": "source_trace", "working_contract": "working_contract", "case_report": "case_report",
    }.items():
        if pair.hashes[field] != refs[role].sha256:
            raise ValueError(f"Input hash/manifest disagreement: {field}")
    return pair


def mask_prepared(raw: dict[str, Any]) -> dict[str, Any]:
    """Construct a result-independent receipt; discard all unlisted downstream state."""
    candidate = HistoricalCandidate.model_validate(raw["candidate"])
    binding = BindingResult.model_validate(raw["binding"])
    plan = restore_plan(raw["plan"])
    if candidate.model_dump(mode="json") != raw["candidate"]:
        raise ValueError("Historical candidate deserialization changed frozen content")
    receipt = RawReceipt(
        receipt_id=f"{raw['obligation_id']}:a4-unknown",
        backend="withheld", terminal_state="unknown", verdict="unknown",
        reason="No execution outcome is available in this view.",
        basis="The candidate, binding and plan remain available for independent semantic assessment.",
    )
    original = raw["source_attribution"]
    # These attribution sections are assembled from input/plan identity, not the
    # backend outcome. Old receipt IDs, arbitrary extra fields and metadata do not cross.
    attribution = {key: deepcopy(original[key]) for key in (
        "requirement", "model", "plan", "roles", "instance_authority", "input_context"
    )}
    attribution["receipt"] = {
        "receipt_id": receipt.receipt_id,
        "reason": "Execution outcomes are unavailable in this view.",
    }
    attribution["reason"] = "Frozen source attribution with a neutral execution view."
    attribution["basis"] = "Original requirement, source, binding and plan identities."
    return {
        "obligation_id": raw["obligation_id"], "candidate": candidate,
        "binding": binding, "plan": plan, "receipt": receipt,
        "source_attribution": attribution,
    }


class TailRuntime:
    """A provider boundary that rejects every upstream call kind."""

    def __init__(self, runtime: Any, cache_root: Path | None = None, namespace: str = ""):
        self.runtime = runtime
        self.config = getattr(runtime, "config", None)
        self.calls = []
        self.cache_root = cache_root
        self.namespace = namespace

    def call(self, **kwargs):
        if kwargs["kind"] not in {"d_adjudication", "d_adjudication_correction"}:
            raise RuntimeError("A4 attempted an upstream generation call")
        identity = {key: value for key, value in kwargs.items() if key != "schema"}
        identity.update(namespace=self.namespace, schema=kwargs["schema"].model_json_schema())
        key = digest(identity)
        path = self.cache_root / (key.removeprefix("sha256:") + ".json") if self.cache_root else None
        audit = {"kind": kwargs["kind"], "artifact_id": kwargs["artifact_id"],
                 "prompt_hash": digest(kwargs["prompt"]), "cache_key": key, "reused": False}
        if path is not None and path.exists():
            saved = json.loads(path.read_text())
            if saved["identity"] != identity:
                raise ValueError("A4 stage cache provenance mismatch")
            outcome = StructuredCallOutcome[DAdjudicationResponse].model_validate(saved["outcome"])
            if not outcome.succeeded or not outcome.real_llm:
                raise ValueError("A4 cache contains an ineligible stage")
            audit["reused"] = True
        else:
            outcome = self.runtime.call(**kwargs)
            if path is not None and outcome.succeeded and outcome.real_llm:
                write_json(path, {"identity": identity, "outcome": outcome.to_dict()})
        self.calls.append(audit)
        return outcome


def replay_tail(*, pair: PairInput, prepared: list[dict[str, Any]], runtime: Any,
                output_root: Path, run_identity: dict[str, Any], round_index: int,
                cache_root: Path | None = None, namespace: str = "") -> dict:
    """Execute the shared method tail using only the caller's masked input view."""
    if any(item["receipt"].verdict != "unknown" for item in prepared):
        raise ValueError("A4 tail received an unmasked receipt")
    runtime = TailRuntime(runtime, cache_root, namespace)
    outputs, stages, outcomes, errors = {}, [], [], []
    forbidden_calls = []

    def forbidden(*args, **kwargs):
        forbidden_calls.append(True)
        raise RuntimeError("A4 attempted candidate preparation or backend execution")

    with ExitStack() as guards:
        guards.enter_context(patch.object(runner, "_prepare_candidate", forbidden))
        guards.enter_context(patch.object(runner, "run_backend", forbidden))
        records, reports, prompts, corrections = runner._adjudicate_and_publish(
            pair=pair, round_index=round_index, runtime=runtime, output_root=output_root,
            run_identity=run_identity, finding_candidates=prepared, stage_outputs=outputs,
            stage_receipts=stages, all_outcomes=outcomes, errors=errors,
        )
    if forbidden_calls:
        raise RuntimeError("A4 execution guard was invoked, including a swallowed invocation")
    expected = [item["obligation_id"] for item in prepared]
    if outputs["validate_d"]["expected_obligation_ids"] != expected:
        raise ValueError("A4 lost or reordered a masked candidate before D")
    return {
        "schema": "paper1.a4.method-tail.v1", "treatment": TREATMENT,
        "pair_id": pair.pair_id, "round": round_index, "run_id": run_identity["run_id"],
        "stage_outputs": outputs, "stage_receipts": stages,
        "evidence_records": records, "report_issue_clusters": reports,
        "llm_calls": [outcome.to_dict() for outcome in outcomes], "errors": errors,
        "call_audit": runtime.calls,
        "eligible": len(records) == len(prepared) and (not prepared or bool(outcomes)) and all(
            outcome.succeeded and outcome.real_llm for outcome in outcomes
        ) and all(batch["status"] == "completed" for batch in outputs["validate_d"]["initial_batches"]),
        "prompts": {"d_adjudication": prompts, "d_adjudication_correction": corrections},
        "all_candidates_reached_d": expected,
        "counters": {"upstream_generation_calls": 0, "backend_execution_calls": 0,
                     "terminal_structured_calls": len(runtime.calls)},
    }
