"""Provider-free replay for newly materialized deterministic execution probes.

This artifact is deliberately separate from saved-candidate route replay and
frontier replay.  It rebuilds the production deterministic chain from saved
contract extraction and grounding, then audits frozen domain-invariant and
transition-group probes that did not exist in the immutable source candidate
set.  It never calls an LLM provider or the external Judge and never reports a
publication, hit, or precision result.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..backends import run_backend
from ..compiler import compile_plan
from ..evidence.audit_bundle import build_audit_bundle
from ..evidence.receipts import build_predicate_execution_receipt
from ..evidence.source_attribution import build_source_attribution
from .frontier_replay import (
    _canonical_hash,
    _file_hash,
    _read_json,
    _reconstruct_prefrontier_inputs,
    _saved_inputs,
)
from ..inputs import load_pair
from ..registry import load_registry
from utils.artifact_io import write_json
from ..semantics import (
    CandidateIssue,
    assemble_method_response,
    bind_candidate,
    evaluate_source_transition_closure,
    materialize_domain_invariant_contracts,
    materialize_typed_frontier,
    suppress_contradicted_ambiguous_source_candidates,
    suppress_satisfied_source_transition_candidates,
)
from ..semantics.predicate_routing import route_primary_candidates

_METHOD_ROOT = Path(__file__).resolve().parents[1]
_PAPER_ROOT = Path(__file__).resolve().parents[4]

EXECUTION_PROBE_REPLAY_SCHEMA = "evidence-discovery.execution_probe_replay.v1"
EXECUTION_PROBE_REPLAY_POLICY_VERSION = "saved-input-current-deterministic-probes.v1"
_REPORT_ROOT = (
    _PAPER_ROOT / "pipeline"
    / "representation"
    / "reports"
    / "llms_emp_r45_java_60"
)
_IMPLEMENTATION_FILES = (
    Path(__file__),
    _METHOD_ROOT / "orchestration" / "runner.py",
    _METHOD_ROOT / "semantics" / "domain_invariants.py",
    _METHOD_ROOT / "semantics" / "frontier.py",
    _METHOD_ROOT / "semantics" / "predicate_routing.py",
    _METHOD_ROOT / "compiler" / "lowering.py",
    _METHOD_ROOT / "backends" / "fcstm_native.py",
)


class ExecutionProbeReplayRecord(BaseModel):
    """One current deterministic probe evaluated from immutable saved method inputs."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pair_id: str = Field(
        pattern=r"^[0-9]{4}$",
        description="Frozen pair identifier whose saved extraction and grounding were replayed.",
    )
    source_file: str = Field(
        min_length=1,
        description="Method-cell path relative to the immutable source run.",
    )
    source_file_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 hash of the complete immutable source method cell.",
    )
    probe_origin: Literal["domain_invariant", "deterministic_execution_probe"] = Field(
        description="Whether the candidate comes from a frozen domain invariant or a current runner execution-probe projection.",
    )
    candidate_previously_materialized: bool = Field(
        description="Whether the exact candidate contract ID was already present in the immutable source execute batch; false identifies a newly materialized current probe.",
    )
    candidate: dict[str, Any] = Field(
        description="Full current exact candidate preserving the obligation and native carrier identity.",
    )
    binding: dict[str, Any] | None = Field(
        default=None,
        description="Current exact binding, or null when the deterministic probe cannot legally close a predicate input.",
    )
    plan: dict[str, Any] | None = Field(
        default=None,
        description="Current compiled frozen-predicate plan, or null when no legal execution plan was formed.",
    )
    receipt: dict[str, Any] | None = Field(
        default=None,
        description="Current real native backend receipt, or null before execution closure.",
    )
    execution_receipt: dict[str, Any] | None = Field(
        default=None,
        description="Orthogonal execution/failure audit derived from the current plan and receipt, or null before plan formation.",
    )
    witness_level: Literal["W0", "W1", "W2"] = Field(
        description="Three-level witness result. A failure or incomplete input never becomes W2.",
    )
    execution_state: Literal["not_attempted", "completed", "failed"] = Field(
        description="Orthogonal current execution state for the probe, including failures before a backend receipt exists.",
    )
    failure_kind: Literal[
        "provider_error",
        "timeout",
        "backend_error",
        "invalid_input",
        "unsupported_backend",
        "attribution_failure",
    ] | None = Field(
        default=None,
        description="Structured failure category independent of W, or null after a completed Boolean execution or a route that was not attempted.",
    )
    audit_bundle: dict[str, Any] | None = Field(
        default=None,
        description="Complete W2 audit bundle, or null for W0/W1 records.",
    )
    failure_stage: Literal["binding", "compile", "backend"] | None = Field(
        default=None,
        description="Local deterministic stage that failed before a complete receipt, or null after normal closure.",
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the final execution and witness state.",
    )
    basis: str = Field(
        min_length=1,
        description="Saved-input, native-model, frozen-registry, and current implementation basis.",
    )


class ExecutionProbeReplayPairRecord(BaseModel):
    """Per-pair deterministic-probe replay result preserving local diagnostics."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen pair identifier.")
    source_file: str = Field(min_length=1, description="Immutable source method-cell path relative to the source run.")
    source_file_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 hash of the immutable source method cell.")
    source_candidate_contract_ids: list[str] = Field(description="Exact candidate contract IDs retained in the immutable source execute batch for new-versus-existing probe accounting.")
    current_frontier_error: dict[str, Any] | None = Field(default=None, description="Captured current deterministic-frontier failure; no probe is fabricated when it is non-null.")
    domain_invariant_dispositions: list[dict[str, Any]] = Field(description="Current frozen-domain-invariant admission or exclusion audit rows.")
    execution_probe_dispositions: list[dict[str, Any]] = Field(description="Current runner execution-probe admission audit rows.")
    records: list[ExecutionProbeReplayRecord] = Field(description="Current domain-invariant and deterministic execution-probe evaluations for this pair.")
    reason: str = Field(min_length=1, description="Non-empty explanation of this pair-local replay scope.")
    basis: str = Field(min_length=1, description="Immutable method-input hash and current deterministic-chain basis.")


class ExecutionProbeReplayManifest(BaseModel):
    """Immutable provenance manifest for one execution-probe replay artifact."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.execution_probe_replay_manifest.v1"] = Field(description="Versioned execution-probe replay manifest schema identifier.")
    replay_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Deterministic immutable replay identity.")
    generated_at: datetime = Field(description="Timezone-aware creation time for this replay artifact.")
    source_run_path: str = Field(min_length=1, description="Absolute immutable source method-run directory read by this replay.")
    source_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Immutable method run identity declared by the source manifest.")
    source_run_manifest_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the immutable source run manifest.")
    source_summary_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the immutable source summary.")
    registry_version: str = Field(min_length=1, description="Frozen predicate registry version used for current compilation.")
    registry_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Frozen predicate registry content hash.")
    implementation_hashes: dict[str, str] = Field(description="Current replay, runner, native semantic, compiler, and backend implementation hashes.")
    provider_calls: Literal[0] = Field(description="Provider call count, fixed to zero for this replay.")
    judge_calls: Literal[0] = Field(description="External Judge call count, fixed to zero for this replay.")
    reason: str = Field(min_length=1, description="Non-empty replay isolation explanation.")
    basis: str = Field(min_length=1, description="Immutable source hashes and frozen current implementation basis.")


class ExecutionProbeReplaySummary(BaseModel):
    """Aggregate acceptance audit for current deterministic execution-probe replay."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.execution_probe_replay_summary.v1"] = Field(description="Versioned execution-probe replay summary schema identifier.")
    replay_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Immutable identity shared with all replay files.")
    source_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Immutable source method run identity.")
    pair_count: int = Field(ge=0, description="Number of source method pairs replayed.")
    probe_count: int = Field(ge=0, description="Number of current deterministic domain/probe candidates audited.")
    newly_materialized_probe_count: int = Field(ge=0, description="Probe count absent from the immutable source execute candidate IDs.")
    probe_origins: dict[str, int] = Field(description="Probe count grouped by domain-invariant versus deterministic execution-probe origin.")
    predicates: dict[str, int] = Field(description="Current frozen predicate IDs selected by the audited probes.")
    execution_states: dict[str, int] = Field(description="Orthogonal execution-state distribution for closed plans.")
    witness_levels: dict[str, int] = Field(description="W0/W1/W2 distribution over current deterministic probes.")
    false_receipt_count: int = Field(ge=0, description="Completed false receipt count; these are replay observations only, not publications.")
    true_receipt_count: int = Field(ge=0, description="Completed true receipt count retained as satisfaction audit only.")
    w2_audit_bundle_count: int = Field(ge=0, description="W2 record count with complete audit bundles.")
    acceptance: dict[str, bool] = Field(description="Machine-checkable replay closure conditions.")
    reason: str = Field(min_length=1, description="Non-empty aggregate replay interpretation.")
    basis: str = Field(min_length=1, description="Current deterministic-chain and real native-receipt basis.")


def _source_attribution(pair: Any, obligation_id: str, plan: Any, receipt_id: str) -> dict[str, Any]:
    """Build complete current artifact attribution for one deterministic probe."""

    return build_source_attribution(
        pair_id=pair.pair_id,
        obligation_id=obligation_id,
        nl_path=pair.pair_dir / "nl.txt",
        model_path=pair.pair_dir / "fcstm.fcstm",
        model_hash=pair.hashes["fcstm"],
        plan_id=plan.plan_id,
        receipt_id=receipt_id,
        plan=plan,
    )


def _saved_candidate_ids(cell: dict[str, Any]) -> set[str]:
    """Return exact immutable execute-batch candidate IDs without semantic reparse."""

    stages = cell.get("stage_outputs")
    execute = stages.get("execute_batch") if isinstance(stages, dict) else None
    rows = execute.get("candidates") if isinstance(execute, dict) else None
    if not isinstance(rows, list):
        raise TypeError("source method cell has no execute_batch.candidates list")
    return {
        str(row["contract_id"])
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("contract_id"), str)
    }


def _current_probe_candidates(pair: Any, cell: dict[str, Any]) -> tuple[list[tuple[str, CandidateIssue]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any] | None]:
    """Replay the runner's deterministic candidate chain through execution probes.

    The function consumes only saved extraction/grounding and current native model
    facts. It intentionally stops before D adjudication and publication.
    """

    from .orchestration.runner import (
        _admit_frontier_unresolved,
        _materialize_deterministic_execution_probes,
        _materialize_exact_s2_inventory_candidates,
    )

    extraction, contracts_by_id, grounding = _saved_inputs(cell)
    contracts_by_id, initial_candidates, _ = _reconstruct_prefrontier_inputs(
        pair, extraction, grounding
    )
    response = assemble_method_response(
        list(grounding),
        reason="Provider-free execution-probe replay merges immutable grounding branches.",
        basis="immutable saved grounding branches",
    )
    try:
        frontier_batch = materialize_typed_frontier(
            pair, extraction, contracts_by_id, grounding, initial_candidates
        )
    except Exception as exc:  # noqa: BLE001 - a local failure must remain auditable
        return [], [], [], {
            "failure_kind": "backend_error",
            "failure_stage": "frontier",
            "error_type": type(exc).__name__,
            "message": str(exc),
            "reason": "Current deterministic frontier failed before probe materialization; no candidate was fabricated.",
            "basis": "provider-free current deterministic frontier invocation",
        }
    frontier_candidates = [obligation.candidate for obligation in frontier_batch.obligations]
    for obligation in frontier_batch.obligations:
        contracts_by_id.setdefault(obligation.contract.contract_id, obligation.contract)
    unresolved, _ = _admit_frontier_unresolved(
        pair, contracts_by_id, frontier_batch, initial_candidates
    )
    frontier_candidates.extend(unresolved)
    domain_contracts, domain_candidates, domain_dispositions = materialize_domain_invariant_contracts(
        pair, existing_candidates=[*initial_candidates, *frontier_candidates]
    )
    domain_ids = {contract.contract_id for contract in domain_contracts}
    frontier_candidates.extend(domain_candidates)
    source_closures = {
        contract_id: evaluate_source_transition_closure(pair, contract)
        for contract_id, contract in contracts_by_id.items()
        if contract.property == "transition_endpoints"
        and contract.expected_direction == "must_exist"
    }
    raw_llm = [
        candidate
        for candidate in initial_candidates
        if candidate.contract_id not in frontier_batch.superseded_candidate_contract_ids
    ]
    raw_llm, _ = suppress_contradicted_ambiguous_source_candidates(pair, raw_llm, grounding)
    admitted_llm, _ = suppress_satisfied_source_transition_candidates(
        raw_llm, source_closures, candidate_origin="grounding"
    )
    frontier_candidates, _ = suppress_satisfied_source_transition_candidates(
        frontier_candidates, source_closures, candidate_origin="deterministic_frontier"
    )
    primary = route_primary_candidates(
        pair, contracts_by_id, grounding, [*admitted_llm, *frontier_candidates]
    )
    routed = list(primary.candidates)
    exact_s2, _ = _materialize_exact_s2_inventory_candidates(
        pair, extraction, routed, source_closures
    )
    probes, _, probe_dispositions = _materialize_deterministic_execution_probes(
        pair,
        contracts_by_id,
        grounding,
        [*routed, *exact_s2],
        transition_groups=(
            *extraction.transition_groups,
            *[
                group
                for grounding_response in grounding
                for group in grounding_response.additional_transition_groups
            ],
        ),
        frontier_batch=frontier_batch,
    )
    domain_routed = [candidate for candidate in routed if candidate.contract_id in domain_ids]
    return [
        ("domain_invariant", candidate) for candidate in domain_routed
    ] + [
        ("deterministic_execution_probe", candidate) for candidate in probes
    ], domain_dispositions, probe_dispositions, None


def _execute_probe(*, pair: Any, source_file: str, source_hash: str, replay_id: str, origin: Literal["domain_invariant", "deterministic_execution_probe"], candidate: CandidateIssue, historical_ids: set[str], registry: Any, ordinal: int) -> ExecutionProbeReplayRecord:
    """Bind, compile, execute, and audit one current deterministic probe."""

    prior = candidate.contract_id in historical_ids
    if candidate.predicate_id is None:
        return ExecutionProbeReplayRecord(
            pair_id=pair.pair_id,
            source_file=source_file,
            source_file_sha256=source_hash,
            probe_origin=origin,
            candidate_previously_materialized=prior,
            candidate=candidate.model_dump(mode="json"),
            witness_level="W1",
            execution_state="not_attempted",
            reason="The exact deterministic probe has no legal current predicate route, so it remains precise W1 without an execution claim.",
            basis="saved extraction/grounding and current native deterministic-probe projection",
        )
    try:
        binding = bind_candidate(candidate, pair.model)
    except Exception as exc:  # noqa: BLE001 - preserve a local binding downgrade
        return ExecutionProbeReplayRecord(
            pair_id=pair.pair_id,
            source_file=source_file,
            source_file_sha256=source_hash,
            probe_origin=origin,
            candidate_previously_materialized=prior,
            candidate=candidate.model_dump(mode="json"),
            witness_level="W1",
            execution_state="not_attempted",
            failure_kind="invalid_input",
            failure_stage="binding",
            reason="Current deterministic probe binding failed; no Boolean result or violation was created.",
            basis=f"binding_error={type(exc).__name__}; saved extraction/grounding and current native model",
        )
    obligation_id = f"{pair.pair_id}:execution-probe-replay:{ordinal}"
    try:
        plan = compile_plan(
            candidate, binding, registry, obligation_id=obligation_id, round_index=1, model=pair.model
        )
    except Exception as exc:  # noqa: BLE001 - compilation failure is a W1 audit fact
        return ExecutionProbeReplayRecord(
            pair_id=pair.pair_id,
            source_file=source_file,
            source_file_sha256=source_hash,
            probe_origin=origin,
            candidate_previously_materialized=prior,
            candidate=candidate.model_dump(mode="json"),
            binding=binding.model_dump(mode="json"),
            witness_level="W1" if binding.precise else "W0",
            execution_state="failed",
            failure_kind="invalid_input",
            failure_stage="compile",
            reason="Current deterministic probe compilation failed; a failure cannot form a Boolean violation.",
            basis=f"compile_error={type(exc).__name__}; frozen registry and exact native binding",
        )
    try:
        receipt = run_backend(plan, pair.model, f"{obligation_id}:receipt")
    except Exception as exc:  # noqa: BLE001 - keep parent replay terminal and auditable
        return ExecutionProbeReplayRecord(
            pair_id=pair.pair_id,
            source_file=source_file,
            source_file_sha256=source_hash,
            probe_origin=origin,
            candidate_previously_materialized=prior,
            candidate=candidate.model_dump(mode="json"),
            binding=binding.model_dump(mode="json"),
            plan=plan.model_dump(mode="json"),
            witness_level="W1" if binding.precise else "W0",
            execution_state="failed",
            failure_kind="backend_error",
            failure_stage="backend",
            reason="Current native backend raised before returning a receipt; no Boolean violation was created.",
            basis=f"backend_error={type(exc).__name__}; frozen native backend execution",
        )
    attribution = _source_attribution(pair, obligation_id, plan, receipt.receipt_id)
    execution_receipt = build_predicate_execution_receipt(
        pair_id=pair.pair_id,
        run_id=replay_id,
        contract_id=candidate.contract_id,
        obligation_id=obligation_id,
        plan=plan,
        receipt=receipt,
        source_attribution=attribution,
        model_hash=pair.hashes["fcstm"],
        retry_records=[],
        independent_semantic_basis=False,
        binding_precise=binding.precise,
    )
    witness = execution_receipt["witness_level"]
    audit_bundle = None
    if witness == "W2":
        audit_bundle = build_audit_bundle(
            pair=pair,
            obligation_id=obligation_id,
            binding=binding,
            plan=plan,
            receipt=receipt,
            source_attribution=attribution,
            reason="Provider-free deterministic execution-probe replay reached one legal current native Boolean evaluation.",
            basis="saved extraction/grounding; current runner projection; frozen registry; native backend receipt",
            retry_records=[],
            execution_receipt=execution_receipt,
        )
    return ExecutionProbeReplayRecord(
        pair_id=pair.pair_id,
        source_file=source_file,
        source_file_sha256=source_hash,
        probe_origin=origin,
        candidate_previously_materialized=prior,
        candidate=candidate.model_dump(mode="json"),
        binding=binding.model_dump(mode="json"),
        plan=plan.model_dump(mode="json"),
        receipt=receipt.model_dump(mode="json"),
        execution_receipt=execution_receipt,
        witness_level=witness,
        execution_state=execution_receipt["execution_state"],
        failure_kind=execution_receipt["failure_kind"],
        audit_bundle=audit_bundle,
        reason="The deterministic probe executed through the current production compiler and native backend without provider or Judge input.",
        basis="saved extraction/grounding, current deterministic projection, frozen registry, and real native receipt",
    )


def _render_readme(manifest: dict[str, Any], summary: dict[str, Any]) -> str:
    """Render the human-readable replay boundary without evaluation claims."""

    return "\n".join(
        [
            "# Deterministic Execution-Probe Provider-Free Replay",
            "",
            f"- source run: `{manifest['source_run_id']}`",
            f"- replay id: `{manifest['replay_id']}`",
            f"- pairs: `{summary['pair_count']}`",
            f"- probes/new probes: `{summary['probe_count']}/{summary['newly_materialized_probe_count']}`",
            f"- W0/W1/W2: `{summary['witness_levels']}`",
            "",
            "This artifact uses immutable saved extraction/grounding plus the current production deterministic chain to audit native domain-invariant and execution-probe candidates. It does not resample an LLM, call the Judge, read any ledger/expected answer, publish issues, or report hit/precision. Its records must not be merged with saved-candidate route, frontier, structural-rebind, or W-state replay cohorts.",
            "",
        ]
    )


def run_execution_probe_replay(*, source_run: str | Path, output_parent: str | Path) -> dict[str, Any]:
    """Create one immutable provider-free current deterministic-probe replay."""

    source_root = Path(source_run).expanduser().resolve()
    manifest_path = source_root / "run_manifest.json"
    summary_path = source_root / "summary.json"
    source_manifest = _read_json(manifest_path)
    _read_json(summary_path)
    source_run_id = str(source_manifest.get("run_id"))
    if not re.fullmatch(r"[0-9a-f]{32}", source_run_id):
        raise ValueError("source run manifest has no valid immutable run_id")
    method_paths = sorted((source_root / "method").glob("*/round-1.json"))
    if not method_paths:
        raise FileNotFoundError("source run has no method/*/round-1.json artifacts")
    registry = load_registry()
    implementation_hashes = {
        path.relative_to(_METHOD_ROOT).as_posix(): _file_hash(path)
        for path in _IMPLEMENTATION_FILES
    }
    replay_id = _canonical_hash(
        {
            "schema": EXECUTION_PROBE_REPLAY_SCHEMA,
            "source_manifest": _file_hash(manifest_path),
            "source_summary": _file_hash(summary_path),
            "registry_hash": registry.registry_hash,
            "policy": EXECUTION_PROBE_REPLAY_POLICY_VERSION,
            "implementation": implementation_hashes,
        }
    ).removeprefix("sha256:")[:32]
    output_root = Path(output_parent).expanduser().resolve() / replay_id
    if output_root.exists():
        raise FileExistsError(f"immutable execution-probe replay output exists: {output_root}")
    output_root.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=f".{replay_id}.", dir=output_root.parent))
    try:
        manifest = ExecutionProbeReplayManifest(
            schema="evidence-discovery.execution_probe_replay_manifest.v1",
            replay_id=replay_id,
            generated_at=datetime.now(timezone.utc),
            source_run_path=str(source_root),
            source_run_id=source_run_id,
            source_run_manifest_sha256=_file_hash(manifest_path),
            source_summary_sha256=_file_hash(summary_path),
            registry_version=registry.version,
            registry_hash=registry.registry_hash,
            implementation_hashes=implementation_hashes,
            provider_calls=0,
            judge_calls=0,
            reason="The replay rebuilds only deterministic candidate projection from immutable saved extraction/grounding and then executes current native probes.",
            basis="immutable source cells, frozen registry, and current runner/domain/native implementation hashes",
        ).model_dump(mode="json")
        pairs: list[ExecutionProbeReplayPairRecord] = []
        for method_path in method_paths:
            cell = _read_json(method_path)
            pair_id = str(cell.get("pair_id") or method_path.parent.name)
            pair = load_pair(_REPORT_ROOT / "pairs" / pair_id)
            source_file = method_path.relative_to(source_root).as_posix()
            source_hash = _file_hash(method_path)
            historical_ids = _saved_candidate_ids(cell)
            candidates, domain_dispositions, probe_dispositions, frontier_error = _current_probe_candidates(pair, cell)
            records = [
                _execute_probe(
                    pair=pair,
                    source_file=source_file,
                    source_hash=source_hash,
                    replay_id=replay_id,
                    origin=origin,
                    candidate=candidate,
                    historical_ids=historical_ids,
                    registry=registry,
                    ordinal=index,
                )
                for index, (origin, candidate) in enumerate(candidates)
            ]
            pairs.append(
                ExecutionProbeReplayPairRecord(
                    pair_id=pair_id,
                    source_file=source_file,
                    source_file_sha256=source_hash,
                    source_candidate_contract_ids=sorted(historical_ids),
                    current_frontier_error=frontier_error,
                    domain_invariant_dispositions=domain_dispositions,
                    execution_probe_dispositions=probe_dispositions,
                    records=records,
                    reason="The pair replay keeps saved extraction/grounding fixed and evaluates only current deterministic domain/probe candidates.",
                    basis="immutable source method cell plus current native FCSTM projection",
                )
            )
        records = [record for pair in pairs for record in pair.records]
        acceptance = {
            "provider_free": True,
            "judge_free": True,
            "all_current_frontiers_closed": all(pair.current_frontier_error is None for pair in pairs),
            "every_w2_has_audit_bundle": all(record.witness_level != "W2" or record.audit_bundle is not None for record in records),
            "no_failed_execution_claims_w2": all(
                record.execution_state == "completed"
                or record.witness_level != "W2"
                for record in records
            ),
            "no_output_is_publication": True,
        }
        summary = ExecutionProbeReplaySummary(
            schema="evidence-discovery.execution_probe_replay_summary.v1",
            replay_id=replay_id,
            source_run_id=source_run_id,
            pair_count=len(pairs),
            probe_count=len(records),
            newly_materialized_probe_count=sum(not record.candidate_previously_materialized for record in records),
            probe_origins=dict(Counter(record.probe_origin for record in records)),
            predicates=dict(Counter(str(record.candidate.get("predicate_id")) for record in records)),
            execution_states=dict(Counter(record.execution_state for record in records)),
            witness_levels=dict(Counter(record.witness_level for record in records)),
            false_receipt_count=sum(record.receipt is not None and record.receipt.get("terminal_state") == "completed" and record.receipt.get("verdict") == "false" for record in records),
            true_receipt_count=sum(record.receipt is not None and record.receipt.get("terminal_state") == "completed" and record.receipt.get("verdict") == "true" for record in records),
            w2_audit_bundle_count=sum(record.audit_bundle is not None for record in records),
            acceptance=acceptance,
            reason="The replay isolates newly materialized deterministic probes. It is not a historical-candidate replay or an evaluation result.",
            basis="saved extraction/grounding, current production deterministic chain, and real native backend receipts",
        ).model_dump(mode="json")
        write_json(stage_root / "execution_probe_replay_manifest.json", manifest)
        write_json(stage_root / "execution_probe_replay_records.json", {"schema": EXECUTION_PROBE_REPLAY_SCHEMA, "pairs": [pair.model_dump(mode="json") for pair in pairs]})
        audit_index: dict[str, dict[str, Any]] = {}
        for index, record in enumerate(records):
            if record.audit_bundle is None:
                continue
            filename = f"{record.pair_id}__probe_{index}.json"
            write_json(stage_root / "audit_bundles" / filename, record.audit_bundle)
            audit_index[f"{record.pair_id}:{index}"] = {"path": f"audit_bundles/{filename}", "audit_hash": record.audit_bundle["audit_hash"], "predicate_id": record.candidate.get("predicate_id"), "reason": "Current W2 deterministic-probe audit bundle.", "basis": "ExecutionProbeReplayRecord.audit_bundle"}
        write_json(stage_root / "audit_index.json", audit_index)
        write_json(stage_root / "summary.json", summary)
        (stage_root / "README.md").write_text(_render_readme(manifest, summary), encoding="utf-8")
        os.rename(stage_root, output_root)
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return {"replay_root": str(output_root), "replay_id": replay_id, "summary": summary}


def main(argv: list[str] | None = None) -> int:
    """Run the deterministic execution-probe replay CLI."""

    parser = argparse.ArgumentParser(description="Replay current deterministic execution probes without provider or Judge calls.")
    parser.add_argument("--source-run", required=True, help="Immutable completed source method-run directory.")
    parser.add_argument("--output-parent", required=True, help="Immutable execution-probe replay output parent.")
    args = parser.parse_args(argv)
    result = run_execution_probe_replay(source_run=args.source_run, output_parent=args.output_parent)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
