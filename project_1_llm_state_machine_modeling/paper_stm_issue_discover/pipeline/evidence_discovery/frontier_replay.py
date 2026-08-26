"""Provider-free replay of the deterministic typed frontier.

This replay intentionally stops short of reconstructing the complete runner.
It reads saved contract extraction and grounding outputs, rematerializes only
the deterministic frontier, and executes only obligations newly exposed by the
current frontier implementation. It never calls a provider or Judge and never
rewrites the immutable source method run.
"""

from __future__ import annotations

import argparse
import hashlib
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

from .backends import run_backend
from .compiler import compile_plan
from .evidence.audit_bundle import build_audit_bundle
from .evidence.receipts import build_predicate_execution_receipt
from .evidence.source_attribution import build_source_attribution
from .inputs import load_pair
from .registry import load_registry
from .reporting.export import write_json
from .semantics import (
    FrontierBatch,
    FrontierObligation,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    assemble_method_response,
    bind_candidate,
    contract_semantic_key,
    materialize_typed_frontier,
    suppress_closed_route_controller_candidates,
)
from .semantics.predicate_routing import route_primary_candidates

FRONTIER_REPLAY_SCHEMA = "evidence-discovery.frontier_replay.v1"
FRONTIER_REPLAY_POLICY_VERSION = "saved-extraction-grounding-frontier-only.v1"
_IMPLEMENTATION_FILES = (
    Path(__file__),
    Path(__file__).parent / "semantics" / "frontier.py",
    Path(__file__).parent / "semantics" / "predicate_routing.py",
    Path(__file__).parent / "compiler" / "lowering.py",
    Path(__file__).parent / "backends" / "fcstm_native.py",
    Path(__file__).parent / "backends" / "trajectory.py",
    Path(__file__).parent / "backends" / "bounded_verification.py",
)
_REPORT_ROOT = (
    Path(__file__).parent.parent / "representation" / "reports" / "llms_emp_r45_java_60"
)


class FrontierReplayExecution(BaseModel):
    """One newly materialized frontier obligation routed and executed currently."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    obligation_key: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Stable typed semantic identity of the rematerialized obligation.",
    )
    frontier_id: str = Field(
        min_length=1,
        description="Deterministic frontier obligation ID retained for artifact joins.",
    )
    predicate_id: str | None = Field(
        default=None,
        description="Frozen predicate selected by current routing, or null when exact inputs remain open.",
    )
    route_telemetry: dict[str, Any] = Field(
        description="Current deterministic route decision with non-empty reason and basis.",
    )
    candidate: dict[str, Any] = Field(
        description="Current candidate after deterministic primary routing.",
    )
    binding: dict[str, Any] | None = Field(
        default=None,
        description="Exact current binding, or null when no predicate route closed.",
    )
    plan: dict[str, Any] | None = Field(
        default=None,
        description="Typed compiled predicate plan, or null when no execution was attempted.",
    )
    receipt: dict[str, Any] | None = Field(
        default=None,
        description="Real native backend receipt, or null when no execution was attempted.",
    )
    execution_receipt: dict[str, Any] | None = Field(
        default=None,
        description="Orthogonal W/execution/failure audit, or null for an unclosed route.",
    )
    witness_level: Literal["W0", "W1", "W2"] = Field(
        description="Current witness level; execution failure never becomes W2.",
    )
    audit_bundle: dict[str, Any] | None = Field(
        default=None,
        description="Complete W2 audit bundle, or null for W0/W1.",
    )
    reason: str = Field(
        min_length=1,
        description="Why this added frontier obligation did or did not execute.",
    )
    basis: str = Field(
        min_length=1,
        description="Saved-input and current deterministic implementation basis.",
    )


class FrontierReplayPairRecord(BaseModel):
    """Per-pair A/B record for one saved method cell's frontier rematerialization."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pair_id: str = Field(
        pattern=r"^[0-9]{4}$",
        description="Frozen pair identifier from the immutable source method cell.",
    )
    source_file: str = Field(
        min_length=1,
        description="Method-cell path relative to the immutable source run.",
    )
    source_file_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the complete immutable source method-cell JSON.",
    )
    baseline_algorithm_version: str = Field(
        min_length=1,
        description="Frontier algorithm version stored in the source method cell.",
    )
    current_algorithm_version: str | None = Field(
        default=None,
        description="Current rematerialized frontier version, or null after a captured local failure.",
    )
    baseline_error: dict[str, Any] | None = Field(
        default=None,
        description="Saved deterministic_frontier_error diagnostic, when present.",
    )
    current_error: dict[str, Any] | None = Field(
        default=None,
        description="Captured current frontier exception, when present; it never fabricates evidence.",
    )
    prefrontier_diagnostics: list[dict[str, Any]] = Field(
        description="Deterministic contract merge and candidate preflight diagnostics reproduced before frontier materialization.",
    )
    baseline_obligation_count: int = Field(
        ge=0,
        description="Number of frontier obligations stored in the source method cell.",
    )
    current_obligation_count: int = Field(
        ge=0,
        description="Number of obligations produced from the same saved extraction/grounding now.",
    )
    added_obligation_count: int = Field(
        ge=0,
        description="Current typed obligation identities absent from the saved frontier.",
    )
    removed_obligation_count: int = Field(
        ge=0,
        description="Saved typed obligation identities absent from current rematerialization.",
    )
    baseline_kinds: dict[str, int] = Field(
        description="Saved frontier obligation distribution by kind.",
    )
    current_kinds: dict[str, int] = Field(
        description="Current rematerialized frontier obligation distribution by kind.",
    )
    added_obligations: list[dict[str, Any]] = Field(
        description="Complete newly materialized typed obligations before routing.",
    )
    executions: list[FrontierReplayExecution] = Field(
        description="Current route and native execution records for added obligations only.",
    )
    reason: str = Field(
        min_length=1,
        description="Scope and interpretation of this pair-local deterministic A/B.",
    )
    basis: str = Field(
        min_length=1,
        description="Immutable source hashes and current implementation basis.",
    )


class FrontierReplayManifest(BaseModel):
    """Immutable provenance manifest for one deterministic frontier replay."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.frontier_replay_manifest.v1"] = Field(
        description="Versioned frontier replay manifest schema identifier.",
    )
    replay_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Deterministic immutable replay identity.",
    )
    generated_at: datetime = Field(
        description="Timezone-aware artifact creation time.",
    )
    source_run_path: str = Field(
        min_length=1,
        description="Absolute immutable source method-run directory.",
    )
    source_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Run identity declared by every source method cell.",
    )
    source_run_manifest_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the immutable source run manifest.",
    )
    source_summary_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the immutable source summary.",
    )
    registry_version: str = Field(
        min_length=1,
        description="Frozen 19-predicate registry version used by compilation.",
    )
    registry_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Frozen 19-predicate registry hash.",
    )
    policy_version: str = Field(
        min_length=1,
        description="Replay isolation policy identifier.",
    )
    implementation_hashes: dict[str, str] = Field(
        description="Hashes of frontier, route, compiler, and native backend implementations.",
    )
    provider_calls: Literal[0] = Field(
        description="Provider call count, fixed to zero.",
    )
    judge_calls: Literal[0] = Field(
        description="Judge call count, fixed to zero.",
    )
    reason: str = Field(
        min_length=1,
        description="Why this replay is provider-free and evaluation-isolated.",
    )
    basis: str = Field(
        min_length=1,
        description="Immutable source and deterministic implementation provenance.",
    )


class FrontierReplaySummary(BaseModel):
    """Aggregate acceptance and delta accounting for frontier rematerialization."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.frontier_replay_summary.v1"] = Field(
        description="Versioned replay summary schema identifier.",
    )
    replay_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Immutable identity shared by all replay outputs.",
    )
    source_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Historical method run whose saved deterministic inputs were replayed.",
    )
    pair_count: int = Field(
        ge=0,
        description="Number of immutable source method cells replayed.",
    )
    baseline_frontier_error_count: int = Field(
        ge=0,
        description="Saved deterministic frontier failures in the source run.",
    )
    current_frontier_error_count: int = Field(
        ge=0,
        description="Current deterministic frontier failures from the same saved inputs.",
    )
    added_obligation_count: int = Field(
        ge=0,
        description="Total newly materialized typed obligation identities.",
    )
    removed_obligation_count: int = Field(
        ge=0,
        description="Total saved typed obligation identities absent currently.",
    )
    added_kinds: dict[str, int] = Field(
        description="New obligation distribution by deterministic frontier kind.",
    )
    routed_predicates: dict[str, int] = Field(
        description="Frozen predicate distribution among newly routed obligations.",
    )
    execution_states: dict[str, int] = Field(
        description="Orthogonal execution-state distribution for newly routed obligations.",
    )
    witness_levels: dict[str, int] = Field(
        description="W0/W1/W2 distribution across added obligations.",
    )
    w2_audit_bundle_count: int = Field(
        ge=0,
        description="Number of added W2 obligations with complete audit bundles.",
    )
    provider_calls: Literal[0] = Field(
        description="Provider call count, fixed to zero.",
    )
    judge_calls: Literal[0] = Field(
        description="Judge call count, fixed to zero.",
    )
    acceptance: dict[str, bool] = Field(
        description="Machine-checkable replay isolation and audit-closure gates.",
    )
    reason: str = Field(
        min_length=1,
        description="What this replay establishes and what it does not reconstruct.",
    )
    basis: str = Field(
        min_length=1,
        description="Saved extraction/grounding and current deterministic implementation basis.",
    )


def _canonical_hash(value: Any) -> str:
    """Return a stable SHA-256 for JSON-compatible content."""

    return (
        "sha256:"
        + hashlib.sha256(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
    )


def _file_hash(path: Path) -> str:
    """Return the SHA-256 of one exact file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    """Read one object-shaped JSON artifact."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"expected JSON object: {path}")
    return payload


def _obligation_key(obligation: FrontierObligation) -> str:
    """Identify one frontier obligation by typed semantics, not prose or ID spelling."""

    return _canonical_hash(
        {
            "kind": obligation.kind,
            "contract": contract_semantic_key(obligation.contract).model_dump(
                mode="json"
            ),
            "candidate": {
                "property": obligation.candidate.property,
                "violation_direction": obligation.candidate.violation_direction,
                "element_refs": obligation.candidate.element_refs,
            },
        }
    )


def _saved_inputs(
    cell: dict[str, Any],
) -> tuple[NLContractResponse, dict[str, NLContract], tuple[GroundingResponse, ...]]:
    """Recover saved extraction and grounding without regenerating candidates."""

    stages = cell.get("stage_outputs")
    if not isinstance(stages, dict):
        raise TypeError("source method cell has no stage_outputs object")
    extraction = stages.get("contract_extraction")
    grounding_stage = stages.get("discovery_grounding")
    if not isinstance(extraction, dict):
        raise TypeError("source method cell has no contract_extraction object")
    if not isinstance(grounding_stage, dict) or not isinstance(
        grounding_stage.get("branches"), list
    ):
        raise TypeError("source method cell has no discovery_grounding branches")
    contracts = NLContractResponse.model_validate(extraction)
    grounding = tuple(
        GroundingResponse.model_validate(row) for row in grounding_stage["branches"]
    )
    contracts_by_id = {row.contract_id: row for row in contracts.contracts}
    for response in grounding:
        for contract in response.additional_contracts:
            prior = contracts_by_id.setdefault(contract.contract_id, contract)
            if contract_semantic_key(prior) != contract_semantic_key(contract):
                raise ValueError(
                    f"conflicting saved contract identity: {contract.contract_id}"
                )
    return contracts, contracts_by_id, grounding


def _saved_frontier(cell: dict[str, Any]) -> FrontierBatch:
    """Recover the exact deterministic frontier stored in one source method cell."""

    stages = cell.get("stage_outputs")
    execute_batch = stages.get("execute_batch") if isinstance(stages, dict) else None
    frontier = (
        execute_batch.get("frontier_batch") if isinstance(execute_batch, dict) else None
    )
    if not isinstance(frontier, dict):
        raise TypeError("source method cell has no execute_batch.frontier_batch")
    return FrontierBatch.model_validate(frontier)


def _saved_frontier_error(cell: dict[str, Any]) -> dict[str, Any] | None:
    """Return one saved deterministic-frontier diagnostic when present."""

    errors = cell.get("errors")
    if not isinstance(errors, list):
        return None
    matches = [
        row
        for row in errors
        if isinstance(row, dict) and row.get("class") == "deterministic_frontier_error"
    ]
    if len(matches) > 1:
        raise ValueError(
            "source method cell has multiple deterministic frontier errors"
        )
    return matches[0] if matches else None


def _reconstruct_prefrontier_inputs(
    pair: Any,
    extraction: NLContractResponse,
    grounding: tuple[GroundingResponse, ...],
) -> tuple[dict[str, NLContract], list[Any], list[dict[str, Any]]]:
    """Replay the runner's deterministic normalization immediately before frontier.

    This chain is part of the frontier input contract. In particular, admitted
    unresolved rows may carry exact owner refs needed by cardinality materialization;
    flattening only ``GroundingResponse.candidates`` would under-reconstruct the
    saved method cell and create a false A/B removal.
    """

    # Delayed import keeps deterministic frontier/backend unit tests independent
    # of the AgentApp/provider runtime used only by the full orchestration module.
    from .orchestration.runner import (
        _admit_grounding_unresolved,
        _merge_grounding_contracts,
        _normalize_state_retention_carriers,
        _preflight_existing_endpoint_candidates,
        _preflight_synthetic_root_wrapper_reachability,
    )

    contracts_by_id, diagnostics = _merge_grounding_contracts(
        pair, extraction, grounding
    )
    response = assemble_method_response(
        list(grounding),
        reason="Provider-free replay merges saved grounding candidates.",
        basis="immutable saved grounding branches",
    )
    unresolved, unresolved_dispositions = _admit_grounding_unresolved(
        pair,
        contracts_by_id,
        grounding,
        response.issues,
    )
    initial, retention_dispositions = _normalize_state_retention_carriers(
        pair,
        [*response.issues, *unresolved],
        contracts_by_id,
    )
    initial, endpoint_dispositions = _preflight_existing_endpoint_candidates(
        pair,
        initial,
        contracts_by_id,
    )
    initial, root_dispositions = _preflight_synthetic_root_wrapper_reachability(
        pair,
        initial,
    )
    initial, route_dispositions = suppress_closed_route_controller_candidates(
        pair,
        initial,
    )
    audit = [
        *diagnostics,
        *unresolved_dispositions,
        *retention_dispositions,
        *endpoint_dispositions,
        *root_dispositions,
        *route_dispositions,
    ]
    return contracts_by_id, initial, audit


def _source_attribution(
    pair: Any,
    obligation_id: str,
    plan_id: str,
    receipt_id: str,
) -> dict[str, Any]:
    """Build current artifact attribution for one frontier replay execution."""

    return build_source_attribution(
        pair_id=pair.pair_id,
        obligation_id=obligation_id,
        nl_path=pair.pair_dir / "nl.txt",
        model_path=pair.pair_dir / "fcstm.fcstm",
        model_hash=pair.hashes["fcstm"],
        plan_id=plan_id,
        receipt_id=receipt_id,
    )


def _execute_added(
    *,
    pair: Any,
    contracts_by_id: dict[str, NLContract],
    grounding: tuple[GroundingResponse, ...],
    added: list[FrontierObligation],
    replay_id: str,
    registry: Any,
) -> list[FrontierReplayExecution]:
    """Route and execute only obligations absent from the saved frontier."""

    if not added:
        return []
    for obligation in added:
        contracts_by_id.setdefault(obligation.contract.contract_id, obligation.contract)
    projection = route_primary_candidates(
        pair,
        contracts_by_id,
        grounding,
        tuple(obligation.candidate for obligation in added),
    )
    telemetry = {row.contract_id: row for row in projection.telemetry}
    records: list[FrontierReplayExecution] = []
    for obligation, candidate in zip(added, projection.candidates, strict=True):
        key = _obligation_key(obligation)
        route = telemetry.get(candidate.contract_id)
        route_payload = (
            route.model_dump(mode="json")
            if route is not None
            else {
                "reason": "No current deterministic route telemetry was emitted.",
                "basis": "added frontier obligation and exact contract identity",
            }
        )
        if candidate.predicate_id is None:
            records.append(
                FrontierReplayExecution(
                    obligation_key=key,
                    frontier_id=obligation.frontier_id,
                    predicate_id=None,
                    route_telemetry=route_payload,
                    candidate=candidate.model_dump(mode="json"),
                    witness_level="W1",
                    reason="The newly materialized semantic obligation remains precise, but current routing did not close a legal predicate execution.",
                    basis=str(route_payload["basis"]),
                )
            )
            continue
        obligation_id = f"{pair.pair_id}:frontier-replay:{key[-16:]}"
        binding = bind_candidate(candidate, pair.model)
        plan = compile_plan(
            candidate,
            binding,
            registry,
            obligation_id=obligation_id,
            round_index=1,
            model=pair.model,
        )
        receipt = run_backend(plan, pair.model, f"{obligation_id}:receipt")
        attribution = _source_attribution(
            pair, obligation_id, plan.plan_id, receipt.receipt_id
        )
        execution_receipt = build_predicate_execution_receipt(
            pair_id=pair.pair_id,
            run_id=replay_id,
            contract_id=candidate.contract_id,
            obligation_id=obligation_id,
            plan=plan,
            receipt=receipt,
            source_attribution=attribution,
            retry_records=[],
            independent_semantic_basis=False,
            binding_precise=binding.precise,
        )
        witness_level = execution_receipt["witness_level"]
        audit_bundle = None
        if witness_level == "W2":
            audit_bundle = build_audit_bundle(
                pair=pair,
                obligation_id=obligation_id,
                binding=binding,
                plan=plan,
                receipt=receipt,
                source_attribution=attribution,
                reason="Provider-free frontier replay reached a legal current typed/native Boolean execution.",
                basis="saved extraction and grounding; current frontier and route; real native backend receipt",
                retry_records=[],
                execution_receipt=execution_receipt,
            )
        records.append(
            FrontierReplayExecution(
                obligation_key=key,
                frontier_id=obligation.frontier_id,
                predicate_id=candidate.predicate_id,
                route_telemetry=route_payload,
                candidate=candidate.model_dump(mode="json"),
                binding=binding.model_dump(mode="json"),
                plan=plan.model_dump(mode="json"),
                receipt=receipt.model_dump(mode="json"),
                execution_receipt=execution_receipt,
                witness_level=witness_level,
                audit_bundle=audit_bundle,
                reason="The added obligation executed through the production typed compiler and native backend without provider or Judge input.",
                basis="saved extraction/grounding, current frontier/route, frozen registry, and real backend receipt",
            )
        )
    return records


def _render_readme(manifest: dict[str, Any], summary: dict[str, Any]) -> str:
    """Render a concise Chinese boundary note for the immutable replay."""

    return "\n".join(
        [
            "# Deterministic Frontier Provider-Free A/B",
            "",
            f"- source run: `{manifest['source_run_id']}`",
            f"- replay id: `{manifest['replay_id']}`",
            f"- pairs: `{summary['pair_count']}`",
            f"- saved/current frontier errors: `{summary['baseline_frontier_error_count']}/{summary['current_frontier_error_count']}`",
            f"- added/removed obligations: `{summary['added_obligation_count']}/{summary['removed_obligation_count']}`",
            f"- W0/W1/W2 over added obligations: `{summary['witness_levels']}`",
            "",
            "This artifact replays only saved contract extraction and grounding before running the current deterministic frontier, primary route, and required native backends. It does not call a method provider or Judge, read ledger expected values, L, answers, other-pair output, or future output, or claim to reconstruct the complete runner. Saved-candidate route replay remains a separate artifact and statistic.",
            "",
        ]
    )


def run_frontier_replay(
    *,
    source_run: str | Path,
    output_parent: str | Path,
) -> dict[str, Any]:
    """Run one immutable saved-extraction/grounding frontier replay."""

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
        path.relative_to(Path(__file__).parent).as_posix()
        if path != Path(__file__)
        else path.name: _file_hash(path)
        for path in _IMPLEMENTATION_FILES
    }
    replay_id = _canonical_hash(
        {
            "schema": FRONTIER_REPLAY_SCHEMA,
            "source_manifest": _file_hash(manifest_path),
            "source_summary": _file_hash(summary_path),
            "registry_hash": registry.registry_hash,
            "policy": FRONTIER_REPLAY_POLICY_VERSION,
            "implementation": implementation_hashes,
        }
    ).removeprefix("sha256:")[:32]
    final_parent = Path(output_parent).expanduser().resolve()
    final_parent.mkdir(parents=True, exist_ok=True)
    final_root = final_parent / replay_id
    if final_root.exists():
        raise FileExistsError(f"immutable frontier replay output exists: {final_root}")
    stage_root = Path(tempfile.mkdtemp(prefix=f".{replay_id}.", dir=final_parent))
    try:
        manifest = FrontierReplayManifest(
            schema="evidence-discovery.frontier_replay_manifest.v1",
            replay_id=replay_id,
            generated_at=datetime.now(timezone.utc),
            source_run_path=str(source_root),
            source_run_id=source_run_id,
            source_run_manifest_sha256=_file_hash(manifest_path),
            source_summary_sha256=_file_hash(summary_path),
            registry_version=registry.version,
            registry_hash=registry.registry_hash,
            policy_version=FRONTIER_REPLAY_POLICY_VERSION,
            implementation_hashes=implementation_hashes,
            provider_calls=0,
            judge_calls=0,
            reason="The replay consumes only immutable saved deterministic inputs and current local deterministic implementations.",
            basis="source run manifest/summary/cell hashes, frozen registry, and implementation hashes",
        ).model_dump(mode="json")
        records: list[FrontierReplayPairRecord] = []
        for method_path in method_paths:
            cell = _read_json(method_path)
            if cell.get("run_id") != source_run_id:
                raise ValueError(f"mixed source run identity in {method_path}")
            pair_id = str(cell.get("pair_id"))
            if not re.fullmatch(r"[0-9]{4}", pair_id):
                raise ValueError(f"invalid source pair identity in {method_path}")
            pair = load_pair(_REPORT_ROOT / "pairs" / pair_id)
            historical_hashes = cell.get("input_hashes")
            if not isinstance(historical_hashes, dict) or any(
                isinstance(value, str) and pair.hashes.get(name) != value
                for name, value in historical_hashes.items()
            ):
                raise ValueError(f"current-pair input drift for {pair_id}")
            extraction, _raw_contracts_by_id, grounding = _saved_inputs(cell)
            contracts_by_id, initial_candidates, prefrontier_diagnostics = (
                _reconstruct_prefrontier_inputs(pair, extraction, grounding)
            )
            baseline = _saved_frontier(cell)
            baseline_error = _saved_frontier_error(cell)
            current_error: dict[str, Any] | None = None
            try:
                current = materialize_typed_frontier(
                    pair,
                    extraction,
                    contracts_by_id,
                    grounding,
                    initial_candidates,
                )
            except Exception as exc:  # noqa: BLE001 - replay records local failure.
                current_error = {
                    "failure_kind": "backend_error",
                    "failure_stage": "deterministic_frontier",
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                    "reason": "Current frontier rematerialization failed locally; no obligation or verdict was fabricated.",
                    "basis": "saved extraction/grounding and local deterministic failure downgrade",
                }
                current = FrontierBatch(
                    reason="Current replay retained a deterministic frontier failure.",
                    basis=f"error_type={type(exc).__name__}; message={exc}",
                )
            baseline_by_key = {
                _obligation_key(row): row for row in baseline.obligations
            }
            current_by_key = {_obligation_key(row): row for row in current.obligations}
            added_keys = sorted(set(current_by_key) - set(baseline_by_key))
            removed_keys = sorted(set(baseline_by_key) - set(current_by_key))
            added = [current_by_key[key] for key in added_keys]
            executions = _execute_added(
                pair=pair,
                contracts_by_id=contracts_by_id,
                grounding=grounding,
                added=added,
                replay_id=replay_id,
                registry=registry,
            )
            records.append(
                FrontierReplayPairRecord(
                    pair_id=pair_id,
                    source_file=method_path.relative_to(source_root).as_posix(),
                    source_file_sha256=_file_hash(method_path),
                    baseline_algorithm_version=baseline.algorithm_version,
                    current_algorithm_version=(
                        current.algorithm_version if current_error is None else None
                    ),
                    baseline_error=baseline_error,
                    current_error=current_error,
                    prefrontier_diagnostics=prefrontier_diagnostics,
                    baseline_obligation_count=len(baseline.obligations),
                    current_obligation_count=len(current.obligations),
                    added_obligation_count=len(added_keys),
                    removed_obligation_count=len(removed_keys),
                    baseline_kinds=dict(
                        Counter(row.kind for row in baseline.obligations)
                    ),
                    current_kinds=dict(
                        Counter(row.kind for row in current.obligations)
                    ),
                    added_obligations=[row.model_dump(mode="json") for row in added],
                    executions=executions,
                    reason="The A/B compares typed frontier identities from one immutable saved extraction/grounding input; route and backend run only for added obligations.",
                    basis="source cell SHA-256, saved frontier batch, current frontier implementation, and current native execution receipts",
                )
            )
        executions = [
            execution for record in records for execution in record.executions
        ]
        added_kinds = Counter(
            obligation["kind"]
            for record in records
            for obligation in record.added_obligations
        )
        routed = [row for row in executions if row.predicate_id is not None]
        acceptance = {
            "provider_calls_zero": True,
            "judge_calls_zero": True,
            "all_current_frontiers_completed": all(
                record.current_error is None for record in records
            ),
            "every_routed_row_has_execution_audit": all(
                row.execution_receipt is not None for row in routed
            ),
            "every_w2_has_audit_bundle": all(
                row.witness_level != "W2" or row.audit_bundle is not None
                for row in executions
            ),
            "no_failure_claims_w2": all(
                row.execution_receipt is None
                or row.execution_receipt["execution_state"] == "completed"
                or row.witness_level != "W2"
                for row in executions
            ),
        }
        summary = FrontierReplaySummary(
            schema="evidence-discovery.frontier_replay_summary.v1",
            replay_id=replay_id,
            source_run_id=source_run_id,
            pair_count=len(records),
            baseline_frontier_error_count=sum(
                record.baseline_error is not None for record in records
            ),
            current_frontier_error_count=sum(
                record.current_error is not None for record in records
            ),
            added_obligation_count=sum(
                record.added_obligation_count for record in records
            ),
            removed_obligation_count=sum(
                record.removed_obligation_count for record in records
            ),
            added_kinds=dict(added_kinds),
            routed_predicates=dict(Counter(str(row.predicate_id) for row in routed)),
            execution_states=dict(
                Counter(
                    row.execution_receipt["execution_state"]
                    for row in routed
                    if row.execution_receipt is not None
                )
            ),
            witness_levels=dict(Counter(row.witness_level for row in executions)),
            w2_audit_bundle_count=sum(
                row.audit_bundle is not None for row in executions
            ),
            provider_calls=0,
            judge_calls=0,
            acceptance=acceptance,
            reason="The replay isolates deterministic frontier changes over saved extraction/grounding. It does not reconstruct runner preflight/publication or measure FULL hit.",
            basis="immutable source cells plus current frontier, route, compiler, and native backend hashes",
        ).model_dump(mode="json")
        write_json(stage_root / "frontier_replay_manifest.json", manifest)
        write_json(
            stage_root / "frontier_replay_records.json",
            {
                "schema": FRONTIER_REPLAY_SCHEMA,
                "records": [row.model_dump(mode="json") for row in records],
            },
        )
        audit_index: dict[str, dict[str, Any]] = {}
        for record in records:
            for index, execution in enumerate(record.executions):
                if execution.audit_bundle is None:
                    continue
                name = f"{record.pair_id}__added_{index}.json"
                write_json(stage_root / "audit_bundles" / name, execution.audit_bundle)
                audit_index[f"{record.pair_id}:{index}"] = {
                    "path": f"audit_bundles/{name}",
                    "audit_hash": execution.audit_bundle["audit_hash"],
                    "predicate_id": execution.predicate_id,
                    "reason": "Added frontier W2 audit is external to the immutable source method run.",
                    "basis": "FrontierReplayExecution.audit_bundle",
                }
        write_json(stage_root / "audit_index.json", audit_index)
        write_json(stage_root / "summary.json", summary)
        (stage_root / "README.md").write_text(
            _render_readme(manifest, summary), encoding="utf-8"
        )
        os.rename(stage_root, final_root)
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return {
        "replay_root": str(final_root),
        "replay_id": replay_id,
        "summary": summary,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the deterministic frontier replay CLI."""

    parser = argparse.ArgumentParser(
        description="Replay saved extraction/grounding through the current frontier."
    )
    parser.add_argument(
        "--source-run",
        required=True,
        help="Immutable completed source method-run directory.",
    )
    parser.add_argument(
        "--output-parent",
        required=True,
        help="Immutable frontier-replay output parent.",
    )
    args = parser.parse_args(argv)
    result = run_frontier_replay(
        source_run=args.source_run,
        output_parent=args.output_parent,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
