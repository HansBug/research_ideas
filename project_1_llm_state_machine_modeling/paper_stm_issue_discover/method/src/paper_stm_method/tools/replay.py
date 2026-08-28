"""Provider-free W-state replay for immutable evidence-discovery method runs.

The replay layer intentionally reads only completed method artifacts.  It does
not call a provider, re-run a backend, inspect a ledger, or invoke the external
Judge.  Its job is limited to applying the current typed execution protocol to
the original candidate, binding, plan inputs, compiled program, raw receipt,
and semantic D facts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..compiler import assess_soundness_fragment
from ..compiler.inputs import (
    UnsupportedPredicateInputs,
    project_predicate_input_values,
    validate_predicate_inputs,
)
from ..compiler.lowering import PredicatePlan, SUPPORTED_PREDICATES
from ..evidence.audit_bundle import validate_and_hash_w2_audit_bundle
from ..evidence.receipts import RawReceipt, build_predicate_execution_receipt
from ..registry import load_registry
from utils.artifact_io import write_json
from ..semantics.adjudication import SemanticAdjudication, adjudicate_disposition
from ..semantics.binding import BindingResult
from ..semantics.obligations import CandidateIssue


REPLAY_SCHEMA = "evidence-discovery.provider_free_w_replay.v1"
REPLAY_POLICY_VERSION = "three-level-w-runtime-execution.v1"


class HistoricalRecordRef(BaseModel):
    """Immutable location and content identity of one source evidence record."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Run identity of the immutable method artifact supplying the record.",
    )
    source_file: str = Field(
        min_length=1,
        description="Path of the source method receipt relative to the immutable source run root.",
    )
    source_file_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the complete source method receipt file.",
    )
    source_record_index: int = Field(
        ge=0,
        description="Zero-based index of the evidence record within the source method receipt.",
    )
    source_record_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the exact source evidence record before replay derivation.",
    )


class ReplayEvidenceRecord(BaseModel):
    """One current W/D result derived from a frozen historical evidence record."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.provider_free_w_replay_record.v1"] = Field(
        description="Versioned provider-free replay record schema identifier."
    )
    historical_record: HistoricalRecordRef = Field(
        description="Immutable source record identity; replay never overwrites that record."
    )
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen pair owning the candidate.")
    obligation_id: str = Field(min_length=1, description="Stable source obligation identity retained during replay.")
    contract_id: str = Field(min_length=1, description="Atomic NL contract identity retained during replay.")
    issue_id: str = Field(min_length=1, description="Stable semantic report identity from the source method artifact.")
    historical_witness_level: Literal["W0", "W1", "W2"] = Field(
        description="Original W result retained only for before/after auditing."
    )
    historical_issue_emitted: bool = Field(
        description="Whether the immutable source method published this record before W-state replay."
    )
    witness_level: Literal["W0", "W1", "W2"] = Field(
        description="Current three-level W result derived without bibliography runtime gating."
    )
    d_level: Literal["D0", "D1", "D2", "D_UNRESOLVED"] = Field(
        description="Current deterministic D disposition derived from preserved semantic facts and execution state."
    )
    issue_emitted: bool = Field(
        description="Whether the current W/D result remains a method publication candidate for the external Judge."
    )
    replay_change: Literal[
        "unchanged",
        "completed_boolean_recovered",
        "invalid_typed_input_rejected",
        "execution_failure_degraded",
        "other_protocol_update",
    ] = Field(description="Deterministic category explaining the W-state transition.")
    candidate: dict[str, Any] = Field(
        description="Original LLM candidate fields needed to reproduce deterministic D adjudication; no evaluation answer is added."
    )
    binding: dict[str, Any] = Field(
        description="Preserved exact binding result used by the replayed W state machine."
    )
    plan: dict[str, Any] = Field(
        description="Current typed plan derived from frozen registry semantics and preserved typed values."
    )
    receipt: dict[str, Any] = Field(
        description="Preserved raw backend receipt; replay never substitutes a newly executed result."
    )
    execution_receipt: dict[str, Any] = Field(
        description="Current orthogonal execution/failure audit receipt derived from the preserved raw receipt."
    )
    source_attribution: dict[str, Any] = Field(
        description="Preserved NL, PlantUML, canonical IR, FCSTM, facts, program, and raw-receipt attribution chain."
    )
    semantic_adjudication: dict[str, Any] | None = Field(
        default=None,
        description="Preserved typed semantic D facts; they are independent of execution failure when established."
    )
    audit_bundle: dict[str, Any] | None = Field(
        default=None,
        description="Complete W2 audit bundle, or null for W0/W1 records."
    )
    report_semantic_identity: dict[str, Any] = Field(
        description="Stable source report identity and typed semantic key, without copying old runtime-gate metadata."
    )
    reason: str = Field(min_length=1, description="Non-empty replay explanation for the final W/D/publication state.")
    basis: str = Field(min_length=1, description="Non-empty frozen-registry, typed-input, raw-receipt, and attribution basis.")


class ReplayManifest(BaseModel):
    """Immutable provenance manifest for one provider-free W-state replay."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.provider_free_w_replay_manifest.v1"] = Field(
        description="Versioned replay manifest schema identifier."
    )
    replay_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Deterministic identity of this replay protocol and source artifact set.")
    generated_at: datetime = Field(description="Timezone-aware replay artifact creation timestamp.")
    source_run_path: str = Field(min_length=1, description="Absolute immutable method run root read by this replay.")
    source_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Immutable source method run identity.")
    source_commit: str = Field(min_length=1, description="Source commit recorded by the immutable method run.")
    source_run_manifest_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the source run manifest.")
    source_summary_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the source summary.")
    registry_version: str = Field(min_length=1, description="Frozen registry version used to revalidate typed plans.")
    registry_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Current frozen registry content hash.")
    policy_version: str = Field(min_length=1, description="Frozen three-level runtime witness replay policy identifier.")
    replay_implementation_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the replay implementation used for this immutable output.")
    provider_calls: Literal[0] = Field(description="Replay provider call count; provider-free replay is always zero.")
    backend_reexecutions: Literal[0] = Field(description="Backend re-execution count; stored raw receipts are never re-run during replay.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the replay isolation boundary.")
    basis: str = Field(min_length=1, description="Non-empty source artifact, registry, and policy basis for the replay.")


class ReplaySummary(BaseModel):
    """Aggregate acceptance audit for one provider-free W-state replay."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.provider_free_w_replay_summary.v1"] = Field(
        description="Versioned replay summary schema identifier."
    )
    replay_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Replay identity shared with the manifest and every record.")
    source_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Immutable source method run identity.")
    evidence_record_count: int = Field(ge=0, description="Total source evidence records replayed without resampling.")
    historical_witness_levels: dict[str, int] = Field(description="Historical W0/W1/W2 distribution for before/after comparison.")
    witness_levels: dict[str, int] = Field(description="Current W0/W1/W2 distribution after typed replay.")
    per_pair: dict[str, dict[str, Any]] = Field(description="Per-pair W/D/publication and replay-change accounting.")
    completed_boolean_recoveries: int = Field(ge=0, description="Historical W1 completed Boolean records restored to legal W2.")
    invalid_typed_input_rejections: int = Field(ge=0, description="Historical Boolean records rejected because current strict typed validation is invalid.")
    bibliography_runtime_w1_count: Literal[0] = Field(description="Number of W1 results caused by bibliography runtime state; it is structurally zero.")
    legal_completed_boolean_w1_count: int = Field(ge=0, description="Count of valid completed true/false results still W1; must be zero for acceptance.")
    invalid_typed_w2_count: int = Field(ge=0, description="Count of W2 results with invalid current typed inputs; must be zero.")
    failure_as_violation_count: int = Field(ge=0, description="Count of failed/non-attempted execution records published as violations without independent semantics; must be zero.")
    w2_audit_bundle_count: int = Field(ge=0, description="Number of W2 records carrying complete replay audit bundles.")
    w2_audit_closure_complete: bool = Field(description="Whether every W2 record has code, inputs, raw result, attribution, reason, basis, and a valid audit hash.")
    semantic_identity_changed_report_ids: list[str] = Field(description="Source report IDs whose publication identity changed; empty permits Judge relation reuse.")
    acceptance: dict[str, bool] = Field(description="Machine-checkable replay acceptance results.")
    reason: str = Field(min_length=1, description="Non-empty summary interpretation of W changes and retained boundaries.")
    basis: str = Field(min_length=1, description="Non-empty source record, typed schema, raw receipt, and audit-bundle basis.")


def _canonical_hash(value: Any) -> str:
    """Return a stable SHA-256 identity for one JSON-compatible value."""

    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _file_hash(path: Path) -> str:
    """Return a SHA-256 identity for an immutable artifact file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    """Load one object-shaped JSON artifact or fail before writing replay output."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object at {path}")
    return payload


def _candidate_from_record(record: dict[str, Any]) -> CandidateIssue:
    """Recover the original candidate surface required for deterministic D replay."""

    payload = {
        field_name: record[field_name]
        for field_name in CandidateIssue.model_fields
        if field_name in record
    }
    payload["reason"] = record.get("candidate_reason", payload.get("reason"))
    payload["basis"] = record.get("candidate_basis", payload.get("basis"))
    return CandidateIssue.model_validate(payload)


def _normalise_retry_records(rows: Any) -> list[dict[str, Any]]:
    """Preserve retry rows while making billing disposition explicit for the new audit schema."""

    if not isinstance(rows, list):
        return []
    normalized: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        item["billable"] = bool(
            item.get("billable")
            or item.get("billing_disposition") == "billable"
        )
        normalized.append(item)
    return normalized


def _missing_inputs(predicate_id: str, required_inputs: tuple[str, ...], values: dict[str, Any]) -> tuple[str, ...]:
    """Apply the compiler's frozen minimal-input accounting to preserved values."""

    missing: list[str] = []
    for input_name in required_inputs:
        value = values.get(input_name)
        required_null = not (
            predicate_id in {"V1", "V2"}
            and input_name == "trigger"
            and input_name in values
        )
        empty_sequence_is_missing = not (
            predicate_id == "S3" and input_name == "triggers"
        )
        if input_name not in values or (value in (None, "") and required_null):
            missing.append(input_name)
        elif value == [] and empty_sequence_is_missing:
            missing.append(input_name)
    return tuple(missing)


def _replay_plan(record: dict[str, Any], registry: Any) -> PredicatePlan:
    """Rebuild a current typed plan without reading historical bibliography runtime fields."""

    binding = BindingResult.model_validate(record["binding"])
    predicate_id = record.get("predicate_id")
    if not isinstance(predicate_id, str) or registry.get(predicate_id) is None:
        raw_values = record.get("predicate_inputs")
        if not isinstance(raw_values, dict):
            raw_values = {}
        typed_inputs = validate_predicate_inputs(None, raw_values)
        return PredicatePlan(
            plan_id=f"{record['obligation_id']}:replay:plan",
            predicate_id=None,
            registry_version=registry.version,
            inputs=typed_inputs,
            soundness_fragment="none",
            assumptions=(),
            predicate_registered=False,
            binding_precise=binding.precise,
            input_shape_valid=False,
            binding_complete=False,
            backend_available=False,
            soundness_fragment_satisfied=False,
            artifact_attribution_complete=False,
            supported=False,
            executable=False,
            reason="The preserved candidate has no frozen predicate route; a precise semantic candidate remains W1.",
            basis="immutable source candidate plus frozen registry lookup",
        )

    predicate = registry.require(predicate_id)
    historical_plan = record.get("plan")
    historical_plan = historical_plan if isinstance(historical_plan, dict) else {}
    historical_inputs = historical_plan.get("inputs")
    historical_inputs = historical_inputs if isinstance(historical_inputs, dict) else {}
    raw_values = {
        key: value
        for key, value in historical_inputs.items()
        if key not in {"schema_version", "predicate_id"}
    }
    projected_values = project_predicate_input_values(predicate_id, raw_values)
    typed_inputs = validate_predicate_inputs(predicate_id, projected_values)
    input_shape_valid = not isinstance(typed_inputs, UnsupportedPredicateInputs)
    missing_inputs = _missing_inputs(predicate_id, predicate.inputs, projected_values)
    binding_complete = not missing_inputs
    model_hash = getattr(typed_inputs, "model_hash", None)
    fragment_ok, fragment_reason = assess_soundness_fragment(
        predicate_id,
        projected_values,
        model_hash=model_hash if isinstance(model_hash, str) else None,
    )
    formal_program = historical_plan.get("formal_program")
    formal_program_hash = historical_plan.get("formal_program_hash")
    source_attribution = record.get("source_attribution")
    source_attribution = source_attribution if isinstance(source_attribution, dict) else {}
    attribution_complete = bool(
        formal_program
        and formal_program_hash
        and model_hash
        and {"requirement", "model", "plan", "receipt"}.issubset(source_attribution)
    )
    backend_available = predicate_id in SUPPORTED_PREDICATES
    executable = all(
        (
            binding.precise,
            input_shape_valid,
            binding_complete,
            backend_available,
            fragment_ok,
            attribution_complete,
        )
    )
    if not input_shape_valid:
        reason = "The preserved values fail the current exact typed predicate schema; this semantic candidate is W1 and the historical Boolean is not admitted."
        basis = f"current typed validation errors={list(typed_inputs.validation_errors)}"
    elif not binding_complete:
        reason = "The preserved typed binding is incomplete under the frozen predicate contract; retain the precise candidate as W1."
        basis = f"frozen required inputs missing={list(missing_inputs)}"
    elif not fragment_ok:
        reason = "The preserved typed binding is shaped but outside the frozen executable soundness fragment; retain the precise candidate as W1."
        basis = f"current executable-fragment validation: {fragment_reason}"
    elif not attribution_complete:
        reason = "The preserved backend result lacks a complete current-artifact attribution chain, so it cannot be admitted as W2."
        basis = "program/hash/model/source-attribution closure check"
    else:
        reason = "The frozen predicate, preserved exact binding, current typed schema, execution fragment, and stored artifact attribution are ready for W-state replay."
        basis = "frozen registry, current Pydantic input schema, executable-fragment check, native backend availability, and preserved artifact chain"
    return PredicatePlan(
        plan_id=f"{record['obligation_id']}:replay:plan",
        predicate_id=predicate_id,
        registry_version=registry.version,
        inputs=typed_inputs,
        soundness_fragment=predicate.soundness_fragment,
        assumptions=tuple(historical_plan.get("assumptions", ())),
        formal_program=formal_program if isinstance(formal_program, str) else None,
        formal_program_hash=formal_program_hash if isinstance(formal_program_hash, str) else None,
        predicate_registered=True,
        binding_precise=binding.precise,
        input_shape_valid=input_shape_valid,
        binding_complete=binding_complete,
        backend_available=backend_available,
        soundness_fragment_satisfied=fragment_ok,
        artifact_attribution_complete=attribution_complete,
        supported=executable,
        executable=executable,
        reason=reason,
        basis=basis,
        predicate_name=predicate.name,
        family=predicate.family,
        semantics=predicate.semantics,
        source_ids=predicate.sources,
        missing_inputs=missing_inputs,
    )


def _replay_audit_bundle(
    *,
    pair_id: str,
    record: dict[str, Any],
    plan: PredicatePlan,
    receipt: RawReceipt,
    execution_receipt: dict[str, Any],
    reason: str,
    basis: str,
    retry_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a W2 bundle using only preserved source artifacts and current replay derivation."""

    source_attribution = dict(record["source_attribution"])
    input_context = source_attribution.get("input_context")
    if not isinstance(input_context, dict):
        input_context = {}
    model_hash = plan.inputs.model_hash
    if not isinstance(model_hash, str):
        raise ValueError("W2 replay plan lacks the closed FCSTM model hash")
    if not isinstance(plan.formal_program, str) or not isinstance(plan.formal_program_hash, str):
        raise ValueError("W2 replay plan lacks the preserved compiled program and hash")
    payload = {
        "schema": "evidence-discovery.w2_audit_bundle.v3",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pair_id": pair_id,
        "obligation_id": record["obligation_id"],
        "input_context": {
            "historical_context": input_context,
            "source_roles": source_attribution.get("roles", {}),
            "reason": "The replay retains the source method's closed input-context identity without reloading or modifying its artifacts.",
            "basis": "immutable source_attribution.input_context",
        },
        "predicate_id": plan.predicate_id,
        "registry_version": plan.registry_version,
        "predicate_logic": {
            "predicate_id": plan.predicate_id,
            "name": plan.predicate_name,
            "family": plan.family,
            "semantics": plan.semantics,
            "inputs": plan.inputs.model_dump(mode="json"),
            "soundness_fragment": plan.soundness_fragment,
            "assumptions": list(plan.assumptions),
            "source_ids": list(plan.source_ids),
            "academic_provenance": "All 19 frozen predicates have completed scholarly eligibility review. Bibliography metadata is not a runtime W or execution condition.",
            "binding_complete": plan.binding_complete,
            "missing_inputs": list(plan.missing_inputs),
        },
        "binding": dict(record["binding"]),
        "compiled_program": {"source": plan.formal_program, "sha256": plan.formal_program_hash},
        "model_hash": model_hash,
        "program_hash": plan.formal_program_hash,
        "backend_result": receipt.to_dict(),
        "execution_receipt": execution_receipt,
        "structured_run_summary": {
            "backend": receipt.backend,
            "terminal_state": receipt.terminal_state,
            "verdict": receipt.verdict,
            "run_metadata": receipt.run_metadata,
            "reason": "The replay preserves the stored deterministic backend result and does not perform a new backend execution.",
            "basis": "immutable source RawReceipt",
        },
        "execution_environment": {
            "mode": "provider_free_replay",
            "reason": "A provider-free replay derives W from stored typed inputs, compiled program, raw receipt, and attribution only.",
            "basis": REPLAY_POLICY_VERSION,
        },
        "terminal_state": receipt.terminal_state,
        "counterexample": receipt.counterexample,
        "trace": receipt.trace,
        "semantic_adjudication": record.get("semantic_adjudication"),
        "retry_records": retry_records,
        "source_attribution": source_attribution,
        "method_receipt": {
            "status": "replayed_from_immutable_method_cell",
            "reason": "The source method receipt is immutable; replay creates a separate W-state audit artifact.",
            "basis": "HistoricalRecordRef in the enclosing replay record",
        },
        "judge_receipt": {
            "status": "not_invoked_by_provider_free_replay",
            "protocol": "semantic-judge.two-stage.v3.2",
            "reason": "Judge semantics and requests are outside this method-only replay boundary.",
            "basis": "method/evaluation physical isolation boundary",
        },
        "pre_finalization_audit_hash": None,
        "audit_finalization": None,
        "issue_emitted": None,
        "reason": reason,
        "basis": basis,
        "audit_hash": "sha256:" + "0" * 64,
    }
    return validate_and_hash_w2_audit_bundle(payload)


def _report_semantic_identity(record: dict[str, Any], clusters: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep source report identity auditable without importing obsolete runtime-gate fields."""

    issue_id = record["issue_id"]
    cluster = next(
        (
            row
            for row in clusters
            if issue_id in row.get("facet_issue_ids", [])
            or issue_id == row.get("issue_id")
        ),
        None,
    )
    semantic_key = cluster.get("deduplication", {}).get("semantic_key", {}) if isinstance(cluster, dict) else {}
    return {
        "source_issue_id": issue_id,
        "source_cluster_issue_id": cluster.get("issue_id") if isinstance(cluster, dict) else None,
        "semantic_key": semantic_key,
        "reason": "Replay retains the source report's typed semantic identity; no new report wording or mapping is generated.",
        "basis": "immutable source report_issue_clusters and evidence issue_id",
    }


def _replay_record(
    *,
    source_run_id: str,
    pair_id: str,
    source_file: Path,
    source_root: Path,
    source_file_hash: str,
    source_record_index: int,
    record: dict[str, Any],
    clusters: list[dict[str, Any]],
    registry: Any,
) -> dict[str, Any]:
    """Replay one source record with current typed W/D and no external reads beyond registry metadata."""

    candidate = _candidate_from_record(record)
    binding = BindingResult.model_validate(record["binding"])
    plan = _replay_plan(record, registry)
    receipt = RawReceipt.model_validate(record["receipt"])
    semantic_payload = record.get("semantic_adjudication")
    semantic = (
        SemanticAdjudication.model_validate(semantic_payload)
        if isinstance(semantic_payload, dict)
        else None
    )
    retry_records = _normalise_retry_records(record.get("retry_records"))
    source_attribution = record.get("source_attribution")
    if not isinstance(source_attribution, dict):
        source_attribution = {}
    independent_semantic_basis = bool(
        semantic is not None and semantic.grounding == "established"
    )
    execution_receipt = build_predicate_execution_receipt(
        pair_id=pair_id,
        run_id=source_run_id,
        contract_id=record["contract_id"],
        obligation_id=record["obligation_id"],
        plan=plan,
        receipt=receipt,
        source_attribution=source_attribution,
        retry_records=retry_records,
        independent_semantic_basis=independent_semantic_basis,
        binding_precise=binding.precise,
    )
    disposition = adjudicate_disposition(candidate, binding, semantic, receipt=receipt)
    if (
        binding.precise
        and execution_receipt["execution_state"] != "completed"
        and not independent_semantic_basis
    ):
        disposition = {
            **disposition,
            "d_level": "D0",
            "reason": str(disposition["reason"]) + " The execution audit is not independent violation evidence, so replay publication is D0.",
            "basis": str(disposition["basis"]) + "; failed or unavailable execution requires independent established semantic basis for D1/D2",
        }
    witness_level = execution_receipt["witness_level"]
    issue_emitted = bool(
        disposition["d_level"] in {"D1", "D2"}
        and (witness_level == "W1" or (witness_level == "W2" and receipt.verdict == "false"))
    )
    if (
        execution_receipt["failure_kind"] == "invalid_input"
        and receipt.terminal_state == "completed"
        and receipt.verdict in {"true", "false"}
    ):
        replay_change = "invalid_typed_input_rejected"
    elif (
        record.get("witness_level") == "W1"
        and witness_level == "W2"
        and receipt.terminal_state == "completed"
        and receipt.verdict in {"true", "false"}
    ):
        replay_change = "completed_boolean_recovered"
    elif execution_receipt["execution_state"] == "failed":
        replay_change = "execution_failure_degraded"
    elif record.get("witness_level") == witness_level:
        replay_change = "unchanged"
    else:
        replay_change = "other_protocol_update"
    reason = str(disposition["reason"])
    basis = str(disposition["basis"])
    audit_bundle = (
        _replay_audit_bundle(
            pair_id=pair_id,
            record=record,
            plan=plan,
            receipt=receipt,
            execution_receipt=execution_receipt,
            reason=reason,
            basis=basis,
            retry_records=retry_records,
        )
        if witness_level == "W2"
        else None
    )
    result = ReplayEvidenceRecord(
        schema="evidence-discovery.provider_free_w_replay_record.v1",
        historical_record=HistoricalRecordRef(
            source_run_id=source_run_id,
            source_file=str(source_file.relative_to(source_root)),
            source_file_sha256=source_file_hash,
            source_record_index=source_record_index,
            source_record_sha256=_canonical_hash(record),
        ),
        pair_id=pair_id,
        obligation_id=record["obligation_id"],
        contract_id=record["contract_id"],
        issue_id=record["issue_id"],
        historical_witness_level=record["witness_level"],
        historical_issue_emitted=bool(record.get("issue_emitted")),
        witness_level=witness_level,
        d_level=disposition["d_level"],
        issue_emitted=issue_emitted,
        replay_change=replay_change,
        candidate=candidate.model_dump(mode="json"),
        binding=binding.model_dump(mode="json"),
        plan=plan.to_dict(),
        receipt=receipt.to_dict(),
        execution_receipt=execution_receipt,
        source_attribution=source_attribution,
        semantic_adjudication=semantic.model_dump(mode="json") if semantic is not None else None,
        audit_bundle=audit_bundle,
        report_semantic_identity=_report_semantic_identity(record, clusters),
        reason=reason,
        basis=basis,
    )
    return result.model_dump(mode="json")


def _w2_audit_complete(record: dict[str, Any]) -> bool:
    """Verify that a replayed W2 record has every mandatory audit-chain component."""

    bundle = record.get("audit_bundle")
    execution = record.get("execution_receipt", {})
    plan = record.get("plan", {})
    if not isinstance(bundle, dict) or not isinstance(execution, dict) or not isinstance(plan, dict):
        return False
    return bool(
        bundle.get("audit_hash")
        and bundle.get("compiled_program", {}).get("source")
        and bundle.get("compiled_program", {}).get("sha256")
        and execution.get("typed_inputs")
        and execution.get("backend_result")
        and execution.get("artifact_attribution_complete")
        and record.get("source_attribution")
        and record.get("reason")
        and record.get("basis")
        and plan.get("formal_program_hash")
    )


def _build_summary(replay_id: str, source_run_id: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build aggregate acceptance checks from already replayed records only."""

    historical = Counter(record["historical_witness_level"] for record in records)
    current = Counter(record["witness_level"] for record in records)
    per_pair_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        per_pair_rows[record["pair_id"]].append(record)
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id, pair_records in sorted(per_pair_rows.items()):
        per_pair[pair_id] = {
            "evidence_records": len(pair_records),
            "historical_witness_levels": dict(Counter(row["historical_witness_level"] for row in pair_records)),
            "witness_levels": dict(Counter(row["witness_level"] for row in pair_records)),
            "d_levels": dict(Counter(row["d_level"] for row in pair_records)),
            "published_issue_count": sum(bool(row["issue_emitted"]) for row in pair_records),
            "replay_changes": dict(Counter(row["replay_change"] for row in pair_records)),
            "reason": "Per-pair counts are derived from immutable source evidence records and deterministic provider-free replay.",
            "basis": "ReplayEvidenceRecord collection",
        }
    completed_boolean_recoveries = sum(
        row["replay_change"] == "completed_boolean_recovered" for row in records
    )
    invalid_rejections = sum(
        row["replay_change"] == "invalid_typed_input_rejected" for row in records
    )
    legal_completed_boolean_w1 = sum(
        row["witness_level"] == "W1"
        and row["receipt"]["terminal_state"] == "completed"
        and row["receipt"]["verdict"] in {"true", "false"}
        and row["execution_receipt"]["failure_kind"] is None
        for row in records
    )
    invalid_typed_w2 = sum(
        row["witness_level"] == "W2"
        and row["execution_receipt"]["failure_kind"] == "invalid_input"
        for row in records
    )
    failure_as_violation = sum(
        row["issue_emitted"]
        and row["execution_receipt"]["execution_state"] != "completed"
        and not row["execution_receipt"]["independent_semantic_basis"]
        for row in records
    )
    w2_records = [row for row in records if row["witness_level"] == "W2"]
    closure_complete = all(_w2_audit_complete(row) for row in w2_records)
    changed_report_ids = sorted(
        {
            row["issue_id"]
            for row in records
            if bool(row["issue_emitted"]) != bool(row["historical_issue_emitted"])
        }
    )
    acceptance = {
        "bibliography_runtime_w1_zero": True,
        "legal_completed_boolean_w1_zero": legal_completed_boolean_w1 == 0,
        "invalid_typed_w2_zero": invalid_typed_w2 == 0,
        "failure_as_violation_zero": failure_as_violation == 0,
        "w2_audit_closure_complete": closure_complete,
    }
    summary = ReplaySummary(
        schema="evidence-discovery.provider_free_w_replay_summary.v1",
        replay_id=replay_id,
        source_run_id=source_run_id,
        evidence_record_count=len(records),
        historical_witness_levels=dict(historical),
        witness_levels=dict(current),
        per_pair=per_pair,
        completed_boolean_recoveries=completed_boolean_recoveries,
        invalid_typed_input_rejections=invalid_rejections,
        bibliography_runtime_w1_count=0,
        legal_completed_boolean_w1_count=legal_completed_boolean_w1,
        invalid_typed_w2_count=invalid_typed_w2,
        failure_as_violation_count=failure_as_violation,
        w2_audit_bundle_count=len(w2_records),
        w2_audit_closure_complete=closure_complete,
        semantic_identity_changed_report_ids=changed_report_ids,
        acceptance=acceptance,
        reason="The replay applies the frozen W0/W1/W2 protocol solely to predicate registration, exact typed binding, executable-fragment legality, closed artifact attribution, and a stored terminal Boolean receipt. Bibliography provenance remains scholarly metadata and does not participate in runtime W.",
        basis="immutable method evidence records, current strict predicate schemas, frozen registry, preserved raw backend receipts, and replay W2 bundles",
    )
    return summary.model_dump(mode="json")


def _render_readme(manifest: dict[str, Any], summary: dict[str, Any]) -> str:
    """Render a concise Chinese protocol note alongside the immutable replay JSON."""

    template = Path(__file__).with_name("PROVIDER_FREE_REPLAY_TEMPLATE.md").read_text(
        encoding="utf-8"
    )
    return template.format(
        source_run_id=manifest["source_run_id"],
        source_commit=manifest["source_commit"],
        replay_id=manifest["replay_id"],
        registry_version=manifest["registry_version"],
        registry_hash=manifest["registry_hash"],
        historical_witness_levels=summary["historical_witness_levels"],
        witness_levels=summary["witness_levels"],
        completed_boolean_recoveries=summary["completed_boolean_recoveries"],
        invalid_typed_input_rejections=summary["invalid_typed_input_rejections"],
    )


def run_provider_free_replay(
    *,
    source_run: str | Path,
    output_parent: str | Path | None = None,
) -> dict[str, Any]:
    """Replay one immutable method run and atomically publish a separate audit artifact."""

    source_root = Path(source_run).expanduser().resolve()
    source_manifest_path = source_root / "run_manifest.json"
    source_summary_path = source_root / "summary.json"
    if not source_manifest_path.is_file() or not source_summary_path.is_file():
        raise FileNotFoundError("source run must contain run_manifest.json and summary.json")
    source_manifest = _read_json(source_manifest_path)
    source_summary = _read_json(source_summary_path)
    source_run_id = str(source_manifest["run_id"])
    registry = load_registry()
    implementation_hash = _file_hash(Path(__file__).resolve())
    replay_identity = _canonical_hash(
        {
            "schema": REPLAY_SCHEMA,
            "source_run_id": source_run_id,
            "source_manifest": _file_hash(source_manifest_path),
            "source_summary": _file_hash(source_summary_path),
            "registry_hash": registry.registry_hash,
            "policy_version": REPLAY_POLICY_VERSION,
            "implementation": implementation_hash,
        }
    ).removeprefix("sha256:")[:32]
    default_parent = source_root.parent.parent / "evidence-discovery-15x1-w-state-replay-05699769"
    final_parent = Path(output_parent).expanduser().resolve() if output_parent else default_parent
    final_parent.mkdir(parents=True, exist_ok=True)
    final_root = final_parent / replay_identity
    if final_root.exists():
        raise FileExistsError(f"immutable replay output already exists: {final_root}")
    method_root = source_root / "method"
    method_paths = sorted(method_root.glob("*/round-1.json"))
    if not method_paths:
        raise FileNotFoundError(f"source run has no method/*/round-1.json files: {method_root}")
    stage_root = Path(tempfile.mkdtemp(prefix=f".{replay_identity}.", dir=final_parent))
    try:
        manifest = ReplayManifest(
            schema="evidence-discovery.provider_free_w_replay_manifest.v1",
            replay_id=replay_identity,
            generated_at=datetime.now(timezone.utc).isoformat(),
            source_run_path=str(source_root),
            source_run_id=source_run_id,
            source_commit=str(source_summary["source_commit"]),
            source_run_manifest_sha256=_file_hash(source_manifest_path),
            source_summary_sha256=_file_hash(source_summary_path),
            registry_version=registry.version,
            registry_hash=registry.registry_hash,
            policy_version=REPLAY_POLICY_VERSION,
            replay_implementation_sha256=implementation_hash,
            provider_calls=0,
            backend_reexecutions=0,
            reason="Provider-free replay recomputes W/D/publication from immutable method artifacts without sampling or execution.",
            basis="source run manifest/summary, current frozen registry, strict Pydantic schemas, and replay implementation hash",
        ).model_dump(mode="json")
        records: list[dict[str, Any]] = []
        for method_path in method_paths:
            cell = _read_json(method_path)
            if cell.get("run_id") != source_run_id:
                raise ValueError(f"mixed source run identity in {method_path}")
            pair_id = cell.get("pair_id")
            if not isinstance(pair_id, str) or len(pair_id) != 4 or not pair_id.isdigit():
                raise ValueError(f"method cell lacks a frozen pair_id: {method_path}")
            source_records = cell.get("evidence_records")
            if not isinstance(source_records, list):
                raise ValueError(f"method cell has no evidence_records list: {method_path}")
            clusters = cell.get("report_issue_clusters")
            clusters = clusters if isinstance(clusters, list) else []
            method_hash = _file_hash(method_path)
            for index, record in enumerate(source_records):
                if not isinstance(record, dict):
                    raise ValueError(f"non-object evidence record at {method_path} index {index}")
                records.append(
                    _replay_record(
                        source_run_id=source_run_id,
                        pair_id=pair_id,
                        source_file=method_path,
                        source_root=source_root,
                        source_file_hash=method_hash,
                        source_record_index=index,
                        record=record,
                        clusters=clusters,
                        registry=registry,
                    )
                )
        records.sort(key=lambda row: (row["pair_id"], row["obligation_id"]))
        summary = _build_summary(replay_identity, source_run_id, records)
        if not all(summary["acceptance"].values()):
            raise ValueError(f"provider-free replay acceptance failed: {summary['acceptance']}")
        if source_run_id == "683f09b788374a73bd17f5efcfe23395":
            if summary["completed_boolean_recoveries"] != 55:
                raise ValueError(
                    "78506646 replay must recover exactly 55 legally completed Boolean W1 records; "
                    f"got {summary['completed_boolean_recoveries']}"
                )
            if summary["invalid_typed_input_rejections"] != 11:
                raise ValueError(
                    "78506646 replay must reject exactly 11 historical invalid S4 Boolean records; "
                    f"got {summary['invalid_typed_input_rejections']}"
                )
        audit_index: dict[str, dict[str, Any]] = {}
        for record in records:
            audit = record.get("audit_bundle")
            if not isinstance(audit, dict):
                continue
            filename = f"{record['pair_id']}__{record['obligation_id'].replace(':', '_')}.json"
            write_json(stage_root / "audit_bundles" / filename, audit)
            audit_index[record["obligation_id"]] = {
                "path": f"audit_bundles/{filename}",
                "audit_hash": audit["audit_hash"],
                "predicate_id": record["plan"]["predicate_id"],
                "witness_level": record["witness_level"],
                "reason": "The W2 bundle is stored separately from source method artifacts.",
                "basis": "ReplayEvidenceRecord.audit_bundle",
            }
        write_json(stage_root / "replay_manifest.json", manifest)
        write_json(stage_root / "replay_evidence.json", {"schema": REPLAY_SCHEMA, "records": records})
        write_json(stage_root / "audit_index.json", audit_index)
        write_json(stage_root / "summary.json", summary)
        (stage_root / "README.md").write_text(_render_readme(manifest, summary), encoding="utf-8")
        os.rename(stage_root, final_root)
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return {
        "replay_root": str(final_root),
        "replay_id": replay_identity,
        "summary": summary,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the provider-free replay command without permitting provider execution."""

    parser = argparse.ArgumentParser(description="Replay immutable evidence-discovery W state without provider or backend calls.")
    parser.add_argument("--source-run", required=True, help="Immutable source method run root containing summary.json and method cells.")
    parser.add_argument("--output-parent", help="Parent directory for the immutable replay group; defaults beside the source run group.")
    args = parser.parse_args(argv)
    result = run_provider_free_replay(source_run=args.source_run, output_parent=args.output_parent)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
