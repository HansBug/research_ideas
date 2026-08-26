"""Provider-free A/B replay for deterministic primary predicate routing.

The replay reads one immutable completed method run.  It reuses only that
run's contract extraction, grounding, and candidate artifacts with the current
pair input closure.  It never calls an LLM, reads a ledger/Judge artifact, or
rewrites the source method run.  Newly routed candidates may execute their
normal deterministic native backend so the A/B result records real typed
plans, receipts, and W states rather than a predicate-ID projection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import Counter, defaultdict
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
    CandidateIssue,
    GroundingResponse,
    NLContract,
    bind_candidate,
    contract_semantic_key,
)
from .semantics.predicate_routing import PredicateRouteTelemetry, route_primary_candidates


ROUTE_REPLAY_SCHEMA = "evidence-discovery.primary_route_replay.v1"
ROUTE_REPLAY_POLICY_VERSION = "primary-route-current-pair-only.v1"
_IMPLEMENTATION_FILES = (
    Path(__file__),
    Path(__file__).parent / "semantics" / "predicate_routing.py",
    Path(__file__).parent / "compiler" / "lowering.py",
    Path(__file__).parent / "backends" / "fcstm_native.py",
    Path(__file__).parent / "backends" / "trajectory.py",
    Path(__file__).parent / "backends" / "bounded_verification.py",
)
_REPORT_ROOT = (
    Path(__file__).parent.parent
    / "representation"
    / "reports"
    / "llms_emp_r45_java_60"
)


class RouteReplayRecord(BaseModel):
    """One predicate-null historical candidate assessed by current primary routing."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.primary_route_replay_record.v1"] = Field(
        description="Versioned route-replay record schema identifier."
    )
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen current-pair identifier whose saved method artifacts are replayed.")
    source_file: str = Field(min_length=1, description="Historical method-cell JSON path relative to the immutable source run root.")
    source_file_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the complete immutable source method-cell file.")
    source_candidate_index: int = Field(ge=0, description="Zero-based execute_batch candidate index in the immutable source method cell.")
    source_candidate_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the exact source candidate envelope before A/B routing.")
    source_evidence_index: int = Field(ge=0, description="Zero-based final evidence-record index proving that this historical predicate-null candidate belongs to the 88-row target cohort.")
    source_evidence_record_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the source final evidence record used to select this A/B row.")
    source_obligation_id: str = Field(min_length=1, description="Historical candidate obligation identifier retained only for source-artifact joinability.")
    contract_id: str = Field(min_length=1, description="Atomic current-pair NL contract identifier used by the route replay.")
    baseline_predicate_id: None = Field(default=None, description="Historical predicate selection, fixed to null because this artifact measures predicate-null route recovery only.")
    route_status: Literal["route_unclosed", "routed_executed", "routed_execution_degraded"] = Field(description="Whether exact primary inputs remained open, reached a terminal backend receipt, or reached a non-Boolean execution failure.")
    route_telemetry: dict[str, Any] = Field(description="Per-contract deterministic routing telemetry produced without evaluation inputs.")
    candidate: dict[str, Any] = Field(description="Current routed candidate preserving the historical semantic identity and source-facing reason/basis.")
    binding: dict[str, Any] | None = Field(default=None, description="Current deterministic binding for a routed candidate, or null when no route closed.")
    plan: dict[str, Any] | None = Field(default=None, description="Current typed compiled plan for a routed candidate, or null when no route closed.")
    receipt: dict[str, Any] | None = Field(default=None, description="Real deterministic backend receipt for a routed candidate, or null when no route closed.")
    execution_receipt: dict[str, Any] | None = Field(default=None, description="Normalized W/execution audit for a routed candidate, or null when no route closed.")
    witness_level: Literal["W0", "W1", "W2"] = Field(description="Current W result; a precise but unclosed route remains W1 and no failure becomes a violation.")
    audit_bundle: dict[str, Any] | None = Field(default=None, description="Complete W2 audit bundle when the route reaches a legal terminal Boolean result, otherwise null.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the route and execution result.")
    basis: str = Field(min_length=1, description="Non-empty saved-artifact, typed-input, and native-backend basis for this A/B row.")


class RouteReplayManifest(BaseModel):
    """Immutable provenance manifest for one primary-route replay artifact."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.primary_route_replay_manifest.v1"] = Field(description="Versioned route-replay manifest schema identifier.")
    replay_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Deterministic immutable replay identity.")
    generated_at: datetime = Field(description="Timezone-aware route-replay artifact creation time.")
    source_run_path: str = Field(min_length=1, description="Absolute immutable source method-run directory read by the replay.")
    source_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Run identity declared by every source method cell.")
    source_run_manifest_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the source run manifest.")
    source_summary_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the source summary.")
    registry_version: str = Field(min_length=1, description="Frozen registry version used by current compilation.")
    registry_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Frozen registry hash used by current compilation.")
    policy_version: str = Field(min_length=1, description="Current-pair-only primary routing policy identifier.")
    implementation_hashes: dict[str, str] = Field(description="SHA-256 hashes of route, compiler, and native backend implementations used by this replay.")
    provider_calls: Literal[0] = Field(description="Provider call count; route replay never invokes an LLM provider.")
    judge_calls: Literal[0] = Field(description="Judge call count; independent evaluation is physically outside this replay.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the replay isolation boundary.")
    basis: str = Field(min_length=1, description="Non-empty immutable source-run, frozen-registry, and implementation basis.")


class RouteReplaySummary(BaseModel):
    """Aggregate acceptance and delta accounting for a primary-route A/B replay."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.primary_route_replay_summary.v1"] = Field(description="Versioned route-replay summary schema identifier.")
    replay_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Immutable replay identity shared with the manifest and every output file.")
    source_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Historical method run whose saved contracts, grounding, and candidates were replayed.")
    provider_calls: Literal[0] = Field(description="Provider call count, fixed to zero for this replay.")
    judge_calls: Literal[0] = Field(description="Judge call count, fixed to zero for this replay.")
    source_predicate_null_candidates: int = Field(ge=0, description="Number of saved execute_batch candidates with predicate_id=null considered by A/B replay.")
    routed_candidate_count: int = Field(ge=0, description="Number of predicate-null candidates for which current deterministic primary routing selected a frozen predicate.")
    route_unclosed_count: int = Field(ge=0, description="Number of predicate-null candidates retained without a legal exact route.")
    routed_predicates: dict[str, int] = Field(description="Count of selected frozen predicates among newly routed candidates.")
    execution_states: dict[str, int] = Field(description="Orthogonal completed/not_attempted/failed distribution for newly routed candidates.")
    witness_levels: dict[str, int] = Field(description="W0/W1/W2 distribution across every historical predicate-null candidate after A/B routing.")
    w2_audit_bundle_count: int = Field(ge=0, description="Count of newly routed W2 records carrying complete audit bundles.")
    per_pair: dict[str, dict[str, Any]] = Field(description="Per-pair route, execution, W, and reason/basis accounting.")
    acceptance: dict[str, bool] = Field(description="Machine-checkable provider, Judge, source-immutability, and W2-audit acceptance results.")
    reason: str = Field(min_length=1, description="Non-empty summary of what the A/B replay measures and does not measure.")
    basis: str = Field(min_length=1, description="Non-empty saved contract/grounding/candidate, typed compiler, and native backend basis.")


def _canonical_hash(value: Any) -> str:
    """Return a stable SHA-256 for JSON-compatible immutable replay content."""

    return "sha256:" + hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _file_hash(path: Path) -> str:
    """Return the SHA-256 of one exact source or implementation file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    """Load one object-shaped JSON artifact before any replay output is created."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _contracts_and_grounding(cell: dict[str, Any]) -> tuple[dict[str, NLContract], tuple[GroundingResponse, ...]]:
    """Recover saved typed contract/grounding input without candidate regeneration."""

    stage_outputs = cell.get("stage_outputs")
    if not isinstance(stage_outputs, dict):
        raise ValueError("method cell has no stage_outputs object")
    extraction = stage_outputs.get("contract_extraction")
    if not isinstance(extraction, dict) or not isinstance(extraction.get("contracts"), list):
        raise ValueError("method cell has no saved contract_extraction.contracts list")
    contracts = {
        contract.contract_id: contract
        for contract in (NLContract.model_validate(row) for row in extraction["contracts"])
    }
    grounding_stage = stage_outputs.get("discovery_grounding")
    if not isinstance(grounding_stage, dict) or not isinstance(grounding_stage.get("branches"), list):
        raise ValueError("method cell has no saved discovery_grounding.branches list")
    grounding = tuple(
        GroundingResponse.model_validate(row)
        for row in grounding_stage["branches"]
    )
    for response in grounding:
        for contract in response.additional_contracts:
            prior = contracts.setdefault(contract.contract_id, contract)
            if contract_semantic_key(prior) != contract_semantic_key(contract):
                raise ValueError(f"conflicting saved contract identity: {contract.contract_id}")
    return contracts, grounding


def _saved_candidate_envelopes(cell: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the immutable execute-batch candidate envelopes in source order."""

    stage_outputs = cell.get("stage_outputs")
    execute_batch = stage_outputs.get("execute_batch") if isinstance(stage_outputs, dict) else None
    candidates = execute_batch.get("candidates") if isinstance(execute_batch, dict) else None
    if not isinstance(candidates, list):
        raise ValueError("method cell has no saved execute_batch.candidates list")
    if not all(isinstance(row, dict) for row in candidates):
        raise ValueError("method cell execute_batch candidates must all be objects")
    return candidates


def _predicate_null_evidence_rows(cell: dict[str, Any]) -> dict[str, tuple[int, dict[str, Any]]]:
    """Select only final saved W1 predicate-null evidence for the route A/B cohort."""

    evidence = cell.get("evidence_records")
    if not isinstance(evidence, list):
        raise ValueError("method cell has no final evidence_records list")
    selected: dict[str, tuple[int, dict[str, Any]]] = {}
    for index, row in enumerate(evidence):
        if not isinstance(row, dict):
            raise ValueError(f"non-object source evidence record at index {index}")
        plan = row.get("plan")
        if not isinstance(plan, dict) or plan.get("predicate_id") is not None:
            continue
        if row.get("witness_level") != "W1":
            continue
        obligation_id = row.get("obligation_id")
        if not isinstance(obligation_id, str) or not obligation_id:
            raise ValueError(f"predicate-null W1 evidence record lacks obligation_id at index {index}")
        if obligation_id in selected:
            raise ValueError(f"duplicate predicate-null W1 evidence obligation_id: {obligation_id}")
        selected[obligation_id] = (index, row)
    return selected


def _source_attribution(pair: Any, obligation_id: str, plan_id: str, receipt_id: str) -> dict[str, Any]:
    """Build current artifact attribution for one newly routed backend execution."""

    return build_source_attribution(
        pair_id=pair.pair_id,
        obligation_id=obligation_id,
        nl_path=pair.pair_dir / "nl.txt",
        model_path=pair.pair_dir / "fcstm.fcstm",
        model_hash=pair.hashes["fcstm"],
        plan_id=plan_id,
        receipt_id=receipt_id,
    )


def _load_current_pair_for_source_cell(pair_id: str, cell: dict[str, Any]) -> Any:
    """Load the exact current-pair closure and reject any source-artifact drift."""

    pair = load_pair(_REPORT_ROOT / "pairs" / pair_id)
    historical_hashes = cell.get("input_hashes")
    if not isinstance(historical_hashes, dict):
        raise ValueError(f"source method cell {pair_id} has no input_hashes object")
    mismatches = {
        name: {"historical": value, "current": pair.hashes.get(name)}
        for name, value in historical_hashes.items()
        if isinstance(value, str) and pair.hashes.get(name) != value
    }
    if mismatches:
        raise ValueError(
            f"provider-free route replay refuses current-pair artifact drift for {pair_id}: {mismatches}"
        )
    return pair


def _record_unclosed(
    *,
    pair_id: str,
    source_file: str,
    source_file_hash: str,
    candidate_index: int,
    envelope: dict[str, Any],
    evidence_index: int,
    evidence_record: dict[str, Any],
    candidate: CandidateIssue,
    telemetry: PredicateRouteTelemetry | None,
) -> dict[str, Any]:
    """Record a precise W1 predicate-null route without fabricating execution."""

    route_telemetry = telemetry.model_dump(mode="json") if telemetry is not None else {
        "reason": "The saved candidate has no current typed contract row available to primary routing.",
        "basis": "immutable execute_batch candidate and saved contract extraction membership",
    }
    precise = bool(envelope.get("binding", {}).get("precise"))
    witness_level: Literal["W0", "W1", "W2"] = "W1" if precise else "W0"
    return RouteReplayRecord(
        schema="evidence-discovery.primary_route_replay_record.v1",
        pair_id=pair_id,
        source_file=source_file,
        source_file_sha256=source_file_hash,
        source_candidate_index=candidate_index,
        source_candidate_sha256=_canonical_hash(envelope),
        source_evidence_index=evidence_index,
        source_evidence_record_sha256=_canonical_hash(evidence_record),
        source_obligation_id=str(envelope.get("obligation_id") or f"{pair_id}:route-replay:{candidate_index}"),
        contract_id=candidate.contract_id,
        route_status="route_unclosed",
        route_telemetry=route_telemetry,
        candidate=candidate.model_dump(mode="json"),
        witness_level=witness_level,
        reason="The current deterministic primary route did not close every required typed input, so this saved semantic candidate remains unexecuted rather than receiving a fabricated scenario, domain, carrier, or verdict.",
        basis=str(route_telemetry["basis"]),
    ).model_dump(mode="json")


def _record_routed(
    *,
    pair: Any,
    source_file: str,
    source_file_hash: str,
    candidate_index: int,
    envelope: dict[str, Any],
    evidence_index: int,
    evidence_record: dict[str, Any],
    candidate: CandidateIssue,
    telemetry: PredicateRouteTelemetry,
    replay_id: str,
    registry: Any,
) -> dict[str, Any]:
    """Compile and execute one newly closed route through its native backend."""

    obligation_id = f"{pair.pair_id}:route-replay:{candidate_index}"
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
    attribution = _source_attribution(pair, obligation_id, plan.plan_id, receipt.receipt_id)
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
    route_status: Literal["routed_executed", "routed_execution_degraded"] = (
        "routed_executed"
        if execution_receipt["execution_state"] == "completed"
        else "routed_execution_degraded"
    )
    audit_bundle = None
    if witness_level == "W2":
        audit_bundle = build_audit_bundle(
            pair=pair,
            obligation_id=obligation_id,
            binding=binding,
            plan=plan,
            receipt=receipt,
            source_attribution=attribution,
            reason="Provider-free primary-route replay reached a legal current typed/native Boolean execution.",
            basis="saved contracts and grounding; current primary route; current compiler; real deterministic native backend receipt",
            retry_records=[],
            execution_receipt=execution_receipt,
        )
    return RouteReplayRecord(
        schema="evidence-discovery.primary_route_replay_record.v1",
        pair_id=pair.pair_id,
        source_file=source_file,
        source_file_sha256=source_file_hash,
        source_candidate_index=candidate_index,
        source_candidate_sha256=_canonical_hash(envelope),
        source_evidence_index=evidence_index,
        source_evidence_record_sha256=_canonical_hash(evidence_record),
        source_obligation_id=str(envelope.get("obligation_id") or f"{pair.pair_id}:route-replay:{candidate_index}"),
        contract_id=candidate.contract_id,
        route_status=route_status,
        route_telemetry=telemetry.model_dump(mode="json"),
        candidate=candidate.model_dump(mode="json"),
        binding=binding.model_dump(mode="json"),
        plan=plan.model_dump(mode="json"),
        receipt=receipt.model_dump(mode="json"),
        execution_receipt=execution_receipt,
        witness_level=witness_level,
        audit_bundle=audit_bundle,
        reason="The replay rerouted only a saved predicate-null candidate, then obtained its result from the production deterministic backend; no provider, Judge, or evaluation answer participated.",
        basis="saved current-pair contracts/grounding/candidate; frozen registry; strict typed compiler; native backend receipt",
    ).model_dump(mode="json")


def _summary(replay_id: str, source_run_id: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build aggregate A/B accounting after all current route attempts terminate."""

    routed = [row for row in records if row["route_status"] != "route_unclosed"]
    unclosed = [row for row in records if row["route_status"] == "route_unclosed"]
    execution_states = Counter(
        row["execution_receipt"]["execution_state"]
        for row in routed
        if isinstance(row.get("execution_receipt"), dict)
    )
    witness_levels = Counter(row["witness_level"] for row in records)
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id in sorted({row["pair_id"] for row in records}):
        rows = [row for row in records if row["pair_id"] == pair_id]
        pair_routed = [row for row in rows if row["route_status"] != "route_unclosed"]
        per_pair[pair_id] = {
            "source_predicate_null_candidates": len(rows),
            "routed_candidate_count": len(pair_routed),
            "route_unclosed_count": len(rows) - len(pair_routed),
            "routed_predicates": dict(Counter(str(row["candidate"].get("predicate_id")) for row in pair_routed)),
            "execution_states": dict(
                Counter(
                    row["execution_receipt"]["execution_state"]
                    for row in pair_routed
                    if isinstance(row.get("execution_receipt"), dict)
                )
            ),
            "witness_levels": dict(Counter(row["witness_level"] for row in rows)),
            "reason": "Per-pair counts use only saved predicate-null candidates and current deterministic primary route execution.",
            "basis": "RouteReplayRecord rows for this frozen pair",
        }
    audit_rows = [row for row in records if isinstance(row.get("audit_bundle"), dict)]
    acceptance = {
        "provider_calls_zero": True,
        "judge_calls_zero": True,
        "all_rows_preserve_predicate_null_baseline": all(row["baseline_predicate_id"] is None for row in records),
        "every_routed_row_has_terminal_execution_audit": all(
            isinstance(row.get("execution_receipt"), dict)
            and row["execution_receipt"]["execution_state"] in {"completed", "not_attempted", "failed"}
            for row in routed
        ),
        "every_w2_has_audit_bundle": all(row["witness_level"] != "W2" or isinstance(row.get("audit_bundle"), dict) for row in records),
        "no_unclosed_row_claims_w2": all(row["witness_level"] != "W2" for row in unclosed),
    }
    return RouteReplaySummary(
        schema="evidence-discovery.primary_route_replay_summary.v1",
        replay_id=replay_id,
        source_run_id=source_run_id,
        provider_calls=0,
        judge_calls=0,
        source_predicate_null_candidates=len(records),
        routed_candidate_count=len(routed),
        route_unclosed_count=len(unclosed),
        routed_predicates=dict(Counter(str(row["candidate"].get("predicate_id")) for row in routed)),
        execution_states=dict(execution_states),
        witness_levels=dict(witness_levels),
        w2_audit_bundle_count=len(audit_rows),
        per_pair=per_pair,
        acceptance=acceptance,
        reason="The A/B compares saved predicate-null candidates with the current exact primary route. It is not a method rerun, a Judge run, or a hit metric.",
        basis="immutable source contract/grounding/candidate artifacts plus current route/compiler/native backend implementations",
    ).model_dump(mode="json")


def _render_readme(manifest: dict[str, Any], summary: dict[str, Any]) -> str:
    """Render the concise Chinese protocol note accompanying the immutable JSON."""

    return "\n".join(
        [
            "# Primary Route Provider-Free A/B",
            "",
            f"- source run: `{manifest['source_run_id']}`",
            f"- replay id: `{manifest['replay_id']}`",
            f"- provider calls: `{manifest['provider_calls']}`",
            f"- Judge calls: `{manifest['judge_calls']}`",
            f"- historical predicate-null candidates: `{summary['source_predicate_null_candidates']}`",
            f"- newly routed candidates: `{summary['routed_candidate_count']}`",
            f"- route-unclosed candidates: `{summary['route_unclosed_count']}`",
            f"- W0/W1/W2: `{summary['witness_levels']}`",
            "",
            "This artifact reads only saved contract extraction, grounding, and predicate-null candidates. It never reads ledger expected values, L, Judge output, answers, other-pair output, or future output; it invokes the existing deterministic FCSTM backend only for inputs newly closed by current code. W2 bundles are stored outside the immutable method artifact, and the external Judge does not participate in this A/B.",
            "",
        ]
    )


def run_primary_route_replay(
    *,
    source_run: str | Path,
    output_parent: str | Path | None = None,
) -> dict[str, Any]:
    """Run immutable saved-artifact primary-route A/B without provider or Judge calls."""

    source_root = Path(source_run).expanduser().resolve()
    manifest_path = source_root / "run_manifest.json"
    summary_path = source_root / "summary.json"
    if not manifest_path.is_file() or not summary_path.is_file():
        raise FileNotFoundError("source run must contain run_manifest.json and summary.json")
    source_manifest = _read_json(manifest_path)
    source_summary = _read_json(summary_path)
    source_run_id = str(source_manifest.get("run_id"))
    if not re.fullmatch(r"[0-9a-f]{32}", source_run_id):
        raise ValueError("source run manifest has no valid immutable run_id")
    method_paths = sorted((source_root / "method").glob("*/round-1.json"))
    if not method_paths:
        raise FileNotFoundError("source run has no method/*/round-1.json artifacts")
    registry = load_registry()
    implementation_hashes = {
        path.relative_to(Path(__file__).parent).as_posix() if path != Path(__file__) else path.name: _file_hash(path)
        for path in _IMPLEMENTATION_FILES
    }
    replay_id = _canonical_hash(
        {
            "schema": ROUTE_REPLAY_SCHEMA,
            "source_run_manifest": _file_hash(manifest_path),
            "source_summary": _file_hash(summary_path),
            "registry_hash": registry.registry_hash,
            "policy": ROUTE_REPLAY_POLICY_VERSION,
            "implementation": implementation_hashes,
        }
    ).removeprefix("sha256:")[:32]
    default_parent = source_root.parent.parent / "evidence-discovery-15x1-primary-route-replay-05699769"
    final_parent = Path(output_parent).expanduser().resolve() if output_parent else default_parent
    final_parent.mkdir(parents=True, exist_ok=True)
    final_root = final_parent / replay_id
    if final_root.exists():
        raise FileExistsError(f"immutable primary-route replay output already exists: {final_root}")
    stage_root = Path(tempfile.mkdtemp(prefix=f".{replay_id}.", dir=final_parent))
    try:
        manifest = RouteReplayManifest(
            schema="evidence-discovery.primary_route_replay_manifest.v1",
            replay_id=replay_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            source_run_path=str(source_root),
            source_run_id=source_run_id,
            source_run_manifest_sha256=_file_hash(manifest_path),
            source_summary_sha256=_file_hash(summary_path),
            registry_version=registry.version,
            registry_hash=registry.registry_hash,
            policy_version=ROUTE_REPLAY_POLICY_VERSION,
            implementation_hashes=implementation_hashes,
            provider_calls=0,
            judge_calls=0,
            reason="Route replay preserves saved LLM output and evaluates only deterministic current-pair routing plus native backend execution.",
            basis="immutable source method cells, frozen registry, current primary route/compiler/backend hashes, and no evaluation artifacts",
        ).model_dump(mode="json")
        records: list[dict[str, Any]] = []
        telemetry_by_pair: dict[str, list[dict[str, Any]]] = {}
        for method_path in method_paths:
            cell = _read_json(method_path)
            if cell.get("run_id") != source_run_id:
                raise ValueError(f"mixed source run identity in {method_path}")
            pair_id = cell.get("pair_id")
            if not isinstance(pair_id, str) or not pair_id.isdigit() or len(pair_id) != 4:
                raise ValueError(f"method cell has no valid frozen pair_id: {method_path}")
            pair = _load_current_pair_for_source_cell(pair_id, cell)
            contracts, grounding = _contracts_and_grounding(cell)
            envelopes = _saved_candidate_envelopes(cell)
            target_evidence = _predicate_null_evidence_rows(cell)
            candidates = tuple(CandidateIssue.model_validate(row["candidate"]) for row in envelopes if isinstance(row.get("candidate"), dict))
            if len(candidates) != len(envelopes):
                raise ValueError(f"method cell has a candidate envelope without a candidate object: {method_path}")
            projection = route_primary_candidates(pair, contracts, grounding, candidates)
            telemetry_by_contract = {row.contract_id: row for row in projection.telemetry}
            telemetry_by_pair[pair_id] = [row.model_dump(mode="json") for row in projection.telemetry]
            source_file = method_path.relative_to(source_root).as_posix()
            source_file_hash = _file_hash(method_path)
            represented_obligation_ids: set[str] = set()
            for index, (envelope, baseline, routed) in enumerate(zip(envelopes, candidates, projection.candidates, strict=True)):
                source_obligation_id = envelope.get("obligation_id")
                if not isinstance(source_obligation_id, str) or source_obligation_id not in target_evidence:
                    continue
                if baseline.predicate_id is not None:
                    raise ValueError(
                        "predicate-null evidence cohort maps to a non-null execute_batch "
                        f"candidate: {source_obligation_id}"
                    )
                represented_obligation_ids.add(source_obligation_id)
                evidence_index, evidence_record = target_evidence[source_obligation_id]
                telemetry = telemetry_by_contract.get(baseline.contract_id)
                if routed.predicate_id is None or telemetry is None:
                    records.append(
                        _record_unclosed(
                            pair_id=pair_id,
                            source_file=source_file,
                            source_file_hash=source_file_hash,
                            candidate_index=index,
                            envelope=envelope,
                            evidence_index=evidence_index,
                            evidence_record=evidence_record,
                            candidate=routed,
                            telemetry=telemetry,
                        )
                    )
                    continue
                records.append(
                    _record_routed(
                        pair=pair,
                        source_file=source_file,
                        source_file_hash=source_file_hash,
                        candidate_index=index,
                        envelope=envelope,
                        evidence_index=evidence_index,
                        evidence_record=evidence_record,
                        candidate=routed,
                        telemetry=telemetry,
                        replay_id=replay_id,
                        registry=registry,
                    )
                )
            unrepresented = sorted(set(target_evidence) - represented_obligation_ids)
            if unrepresented:
                raise ValueError(
                    f"predicate-null W1 evidence rows have no execute_batch source candidate in {method_path}: {unrepresented}"
                )
        records.sort(key=lambda row: (row["pair_id"], row["source_candidate_index"]))
        summary = _summary(replay_id, source_run_id, records)
        if not all(summary["acceptance"].values()):
            raise ValueError(f"primary route replay acceptance failed: {summary['acceptance']}")
        audit_index: dict[str, dict[str, Any]] = {}
        for record in records:
            audit = record.get("audit_bundle")
            if not isinstance(audit, dict):
                continue
            name = f"{record['pair_id']}__route_{record['source_candidate_index']}.json"
            write_json(stage_root / "audit_bundles" / name, audit)
            audit_index[f"{record['pair_id']}:{record['source_candidate_index']}"] = {
                "path": f"audit_bundles/{name}",
                "audit_hash": audit["audit_hash"],
                "predicate_id": record["candidate"]["predicate_id"],
                "reason": "Current route replay W2 audit bundle is kept outside the immutable source method run.",
                "basis": "RouteReplayRecord.audit_bundle",
            }
        write_json(stage_root / "route_replay_manifest.json", manifest)
        write_json(stage_root / "route_replay_records.json", {"schema": ROUTE_REPLAY_SCHEMA, "records": records})
        write_json(stage_root / "route_telemetry.json", telemetry_by_pair)
        write_json(stage_root / "audit_index.json", audit_index)
        write_json(stage_root / "summary.json", summary)
        (stage_root / "README.md").write_text(_render_readme(manifest, summary), encoding="utf-8")
        os.rename(stage_root, final_root)
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return {"replay_root": str(final_root), "replay_id": replay_id, "summary": summary}


def main(argv: list[str] | None = None) -> int:
    """Run the primary-route A/B CLI without provider or external Judge access."""

    parser = argparse.ArgumentParser(description="Replay saved primary predicate routes without LLM or Judge calls.")
    parser.add_argument("--source-run", required=True, help="Immutable completed source method-run directory.")
    parser.add_argument("--output-parent", help="Optional immutable route-replay output parent.")
    args = parser.parse_args(argv)
    result = run_primary_route_replay(source_run=args.source_run, output_parent=args.output_parent)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
