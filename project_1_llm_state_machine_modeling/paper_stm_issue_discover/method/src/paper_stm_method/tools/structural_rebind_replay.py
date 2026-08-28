"""Provider-free audit replay for saved selected structural predicate candidates.

This replay is intentionally separate from ``route_replay``.  The latter has a
fixed predicate-null W1 cohort, whereas this module audits the safety of
rebuilding already selected S2--S6 candidates through the current native typed
binder.  It does not call a provider or Judge, read evaluation artifacts, or
rewrite the immutable source method run.
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
from ..registry import load_registry
from utils.artifact_io import write_json
from .route_replay import (
    _canonical_hash,
    _contracts_and_grounding,
    _file_hash,
    _load_current_pair_for_source_cell,
    _read_json,
    _saved_candidate_envelopes,
    _source_attribution,
    merge_saved_frontier_contracts,
)
from ..semantics import (
    CandidateIssue,
    ContractBindingHint,
    NLContract,
    bind_candidate,
)
from ..semantics.predicate_routing import route_primary_candidates

_METHOD_ROOT = Path(__file__).resolve().parents[1]

STRUCTURAL_REBIND_REPLAY_SCHEMA = "evidence-discovery.structural_rebind_replay.v1"
STRUCTURAL_REBIND_REPLAY_POLICY_VERSION = "saved-selected-s2-s6-native-rebind.v1"
STRUCTURAL_PREDICATES = frozenset({"S2", "S3", "S4", "S5", "S6"})
_STRUCTURAL_PROPERTY_BY_PREDICATE = {
    "S2": frozenset({"initial_entry", "transition_endpoints"}),
    "S3": frozenset({"trigger_set"}),
    "S4": frozenset({"state_action"}),
    "S5": frozenset({"guard"}),
    "S6": frozenset({"effect"}),
}
_STRUCTURAL_EXPECTED_DIRECTION = {
    "initial_entry": "must_enter",
    "transition_endpoints": "must_exist",
    "trigger_set": "must_equal",
    "state_action": "must_occur",
    "guard": "must_equal",
    "effect": "must_occur",
}
_NL_SEGMENT_REF = re.compile(r"(?<![A-Za-z0-9])NL[0-9]+(?:\.[0-9]+)?(?![A-Za-z0-9])")
_IMPLEMENTATION_FILES = (
    Path(__file__),
    _METHOD_ROOT / "semantics" / "predicate_routing.py",
    Path(__file__).with_name("route_replay.py"),
    _METHOD_ROOT / "compiler" / "lowering.py",
    _METHOD_ROOT / "backends" / "fcstm_native.py",
    _METHOD_ROOT / "backends" / "source_static.py",
)


class StructuralRebindReplayRecord(BaseModel):
    """One selected S2--S6 candidate replayed through current native closure."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.structural_rebind_replay_record.v1"] = Field(
        description="Versioned structural-rebind replay record schema identifier."
    )
    pair_id: str = Field(
        pattern=r"^[0-9]{4}$",
        description="Frozen current-pair identifier whose saved method candidate is replayed.",
    )
    source_file: str = Field(
        min_length=1,
        description="Historical method-cell path relative to the immutable source run.",
    )
    source_file_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the complete immutable source method-cell JSON.",
    )
    source_candidate_index: int = Field(
        ge=0,
        description="Zero-based execute_batch candidate position retained for source joins.",
    )
    source_candidate_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the exact source candidate envelope before current rebinding.",
    )
    source_obligation_id: str = Field(
        min_length=1,
        description="Historical obligation identifier retained only for immutable-artifact joinability.",
    )
    contract_id: str = Field(
        min_length=1,
        description="Typed current-pair NL contract used by the deterministic binder.",
    )
    contract_origin: Literal[
        "saved_contract", "saved_selected_candidate", "unavailable"
    ] = Field(
        description="Whether replay used an immutable saved NL/frontier contract, reconstructed one replay-only contract from a complete selected structural candidate, or could not obtain a legal contract. The latter never executes.",
    )
    baseline_predicate_id: Literal["S2", "S3", "S4", "S5", "S6"] = Field(
        description="Saved selected structural predicate before current native rebinding.",
    )
    baseline_candidate: dict[str, Any] = Field(
        description="Immutable saved candidate before rebind; retained for A/B audit only.",
    )
    baseline_plan: dict[str, Any] | None = Field(
        default=None,
        description="Saved compiled plan when present in the source envelope, or null for incomplete history.",
    )
    baseline_receipt: dict[str, Any] | None = Field(
        default=None,
        description="Saved raw backend receipt when present in the source envelope, or null for incomplete history.",
    )
    baseline_binding_precise: bool = Field(
        description="Whether the saved binding was marked precise before this deterministic replay.",
    )
    route_status: Literal["route_unclosed", "routed_executed", "routed_execution_degraded"] = Field(
        description="Whether current native input closure remained open, completed, or ended in a structured execution failure.",
    )
    route_telemetry: dict[str, Any] = Field(
        description="Current exact route decision with non-empty reason and basis.",
    )
    candidate: dict[str, Any] = Field(
        description="Current routed candidate after native path/carrier/AST rebinding.",
    )
    binding: dict[str, Any] | None = Field(
        default=None,
        description="Current deterministic binding, or null if exact route closure failed.",
    )
    plan: dict[str, Any] | None = Field(
        default=None,
        description="Current compiled predicate plan, or null if exact route closure failed.",
    )
    receipt: dict[str, Any] | None = Field(
        default=None,
        description="Current real native backend receipt, or null if no execution was attempted.",
    )
    execution_receipt: dict[str, Any] | None = Field(
        default=None,
        description="Current orthogonal execution/failure/W audit, or null for an unclosed route.",
    )
    witness_level: Literal["W0", "W1", "W2"] = Field(
        description="Current W result; failures and unclosed routes never produce W2.",
    )
    audit_bundle: dict[str, Any] | None = Field(
        default=None,
        description="Complete W2 audit bundle for a legal terminal Boolean result, otherwise null.",
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the structural rebind and execution outcome.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty saved-artifact, current typed-input, and native-backend basis.",
    )


class StructuralRebindReplayManifest(BaseModel):
    """Immutable provenance manifest for one selected-structural replay."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.structural_rebind_replay_manifest.v1"] = Field(
        description="Versioned structural-rebind replay manifest schema identifier."
    )
    replay_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Deterministic immutable replay identity shared by all output files.",
    )
    generated_at: datetime = Field(
        description="Timezone-aware artifact generation time."
    )
    source_run_path: str = Field(
        min_length=1,
        description="Absolute immutable source method-run directory read by this replay.",
    )
    source_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Run identity declared by all source method cells.",
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
        description="Frozen registry version used by current compilation.",
    )
    registry_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Frozen registry hash used by current compilation.",
    )
    policy_version: str = Field(
        min_length=1,
        description="Selected-structural native-rebind policy version.",
    )
    implementation_hashes: dict[str, str] = Field(
        description="SHA-256 hashes of rebind, compiler, and native backend implementations.",
    )
    provider_calls: Literal[0] = Field(
        description="Provider call count; this replay never invokes an LLM provider."
    )
    judge_calls: Literal[0] = Field(
        description="Judge call count; evaluation is physically outside this replay."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the replay isolation boundary.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty immutable source-run, frozen-registry, and implementation basis.",
    )


class StructuralRebindReplaySummary(BaseModel):
    """Aggregate accounting for saved selected S2--S6 native rebinding."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["evidence-discovery.structural_rebind_replay_summary.v1"] = Field(
        description="Versioned structural-rebind replay summary schema identifier."
    )
    replay_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Immutable replay identity shared with the manifest and every record.",
    )
    source_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Historical method run whose selected structural candidates were replayed.",
    )
    provider_calls: Literal[0] = Field(
        description="Provider call count, fixed to zero for this replay."
    )
    judge_calls: Literal[0] = Field(
        description="Judge call count, fixed to zero for this replay."
    )
    selected_structural_candidate_count: int = Field(
        ge=0,
        description="Number of immutable saved candidates whose predicate is one of S2--S6.",
    )
    baseline_predicates: dict[str, int] = Field(
        description="Saved selected-predicate distribution before rebinding."
    )
    current_predicates: dict[str, int] = Field(
        description="Current selected-predicate distribution after exact native closure; null routes use key null.",
    )
    route_statuses: dict[str, int] = Field(
        description="Current route-unclosed/executed/degraded distribution."
    )
    witness_levels: dict[str, int] = Field(
        description="Current W0/W1/W2 distribution for the fixed selected-structural cohort."
    )
    baseline_verdicts: dict[str, int] = Field(
        description="Saved raw receipt verdict distribution; absent receipts use key missing."
    )
    current_verdicts: dict[str, int] = Field(
        description="Current raw receipt verdict distribution; unclosed routes use key not_attempted."
    )
    route_changed_count: int = Field(
        ge=0,
        description="Rows whose selected predicate or full typed input payload changed after native rebinding.",
    )
    w2_audit_bundle_count: int = Field(
        ge=0,
        description="Current W2 records carrying complete audit bundles."
    )
    historical_frontier_items_excluded: dict[str, int] = Field(
        description="Counts of saved frontier items excluded because their retired kind is no longer legal production input; this is historical replay compatibility, not a new frontier result."
    )
    per_pair: dict[str, dict[str, Any]] = Field(
        description="Per-pair fixed-cohort route, execution, W, and reason/basis accounting."
    )
    acceptance: dict[str, bool] = Field(
        description="Machine-checkable provider, Judge, terminal-audit, and W2-closure gates."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty statement of what this replay audits and excludes.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty saved candidate, exact route/compiler, and native backend basis.",
    )


def _record_unclosed(
    *,
    pair_id: str,
    source_file: str,
    source_file_hash: str,
    candidate_index: int,
    envelope: dict[str, Any],
    baseline: CandidateIssue,
    routed: CandidateIssue,
    telemetry: dict[str, Any],
    contract_origin: Literal[
        "saved_contract", "saved_selected_candidate", "unavailable"
    ],
) -> dict[str, Any]:
    """Record an exact but unexecuted structural route without fabricating a verdict."""

    precise = bool(envelope.get("binding", {}).get("precise"))
    return StructuralRebindReplayRecord(
        schema="evidence-discovery.structural_rebind_replay_record.v1",
        pair_id=pair_id,
        source_file=source_file,
        source_file_sha256=source_file_hash,
        source_candidate_index=candidate_index,
        source_candidate_sha256=_canonical_hash(envelope),
        source_obligation_id=str(envelope["obligation_id"]),
        contract_id=baseline.contract_id,
        contract_origin=contract_origin,
        baseline_predicate_id=baseline.predicate_id,
        baseline_candidate=baseline.model_dump(mode="json"),
        baseline_plan=envelope.get("plan") if isinstance(envelope.get("plan"), dict) else None,
        baseline_receipt=envelope.get("receipt") if isinstance(envelope.get("receipt"), dict) else None,
        baseline_binding_precise=precise,
        route_status="route_unclosed",
        route_telemetry=telemetry,
        candidate=routed.model_dump(mode="json"),
        witness_level="W1" if precise else "W0",
        reason="The saved selected structural candidate could not be rebuilt with complete current native typed inputs, so it is retained as a precise unexecuted route instead of reusing a legacy input or manufacturing a Boolean verdict.",
        basis=str(telemetry["basis"]),
    ).model_dump(mode="json")


def _saved_selected_structural_contract(
    candidate: CandidateIssue,
) -> NLContract | None:
    """Reconstruct one strict replay-only contract from a selected S2--S6 row.

    Older immutable method artifacts can contain deterministic execution probes
    appended after the primary route.  Those probes deliberately have no
    extraction or frontier ``NLContract`` row, but their saved candidate carries
    the complete typed structural inputs that the original compiler executed.
    This helper turns that immutable input envelope into a constrained replay
    contract so the *current* primary route can rebind every native identity.
    It never infers an input from prose, a model observation, an evaluation
    artifact, or another candidate.  Any incomplete or property-incoherent row
    remains unavailable and is recorded as an unexecuted W1/W0 replay row.
    """

    predicate = candidate.predicate_id
    if predicate not in STRUCTURAL_PREDICATES:
        return None
    if candidate.property not in _STRUCTURAL_PROPERTY_BY_PREDICATE[predicate]:
        return None

    # The contract ID and supplied source refs are method-owned provenance, not
    # FCSTM text.  A replay-only contract may use them only when they identify
    # exactly one numbered requirement segment; cross-segment probes remain
    # unclosed rather than inheriting an arbitrary NL1 identity.
    segment_ids = {
        match
        for value in (*candidate.source_refs, candidate.contract_id)
        for match in _NL_SEGMENT_REF.findall(value)
    }
    if len(segment_ids) != 1:
        return None
    segment_id = next(iter(segment_ids))

    inputs = candidate.predicate_inputs

    def one_string(name: str) -> str | None:
        value = inputs.get(name)
        return value if isinstance(value, str) and value.strip() else None

    def one_effect() -> str | None:
        value = inputs.get("effect")
        if isinstance(value, str) and value.strip():
            return value
        if (
            isinstance(value, (list, tuple))
            and len(value) == 1
            and isinstance(value[0], str)
            and value[0].strip()
        ):
            return value[0]
        return None

    hints: list[ContractBindingHint] = []

    def hint(role: str, value: str) -> None:
        hints.append(
            ContractBindingHint(
                role=role,
                value=value,
                source_ref=segment_id,
                reason=(
                    "The immutable selected structural candidate carries this "
                    "typed input for replay-only native rebinding."
                ),
                basis=(
                    f"candidate_contract={candidate.contract_id}; "
                    f"predicate={predicate}; input={role}"
                ),
            )
        )

    if predicate == "S2":
        target = one_string("target")
        if candidate.property == "initial_entry":
            owner = one_string("scope")
            if owner is None or target is None:
                return None
            hint("owner", owner)
            hint("target", target)
        else:
            source = one_string("source")
            if source is None or target is None:
                return None
            hint("source", source)
            hint("target", target)
    elif predicate == "S3":
        transition = one_string("transition") or one_string("transition_ref")
        triggers = inputs.get("triggers")
        if (
            transition is None
            or not isinstance(triggers, (list, tuple))
            or not all(isinstance(item, str) and item.strip() for item in triggers)
        ):
            return None
        hint("transition", transition)
        for trigger in triggers:
            hint("event", trigger)
    elif predicate == "S4":
        state = one_string("state")
        phase = one_string("phase")
        action = one_string("action")
        if state is None or phase not in {"entry", "do", "exit"} or action is None:
            return None
        hint("state", state)
        hint("phase", phase)
        hint("action", action)
    elif predicate == "S5":
        transition = one_string("transition") or one_string("transition_ref")
        guard = one_string("guard") or one_string("expected_guard")
        if transition is None or guard is None:
            return None
        hint("transition", transition)
        hint("guard", guard)
    else:
        transition = one_string("transition") or one_string("transition_ref")
        effect = one_effect()
        if transition is None or effect is None:
            return None
        hint("transition", transition)
        hint("effect", effect)

    return NLContract(
        contract_id=candidate.contract_id,
        segment_id=segment_id,
        quote=candidate.requirement_quote,
        normative_statement=candidate.expected,
        locus_kind=candidate.locus_kind,
        locus_names=candidate.locus_names,
        property=candidate.property,
        expected_direction=_STRUCTURAL_EXPECTED_DIRECTION[candidate.property],
        violation_direction=candidate.violation_direction,
        evidence_types=candidate.evidence_types,
        binding_hints=tuple(hints),
        scope=(
            one_string("scope")
            or "saved_selected_structural_candidate_replay"
        ),
        source_refs=tuple(dict.fromkeys((segment_id, *candidate.source_refs))),
        reason=(
            "A complete immutable selected structural candidate lacks a saved "
            "NL/frontier contract, so replay reconstructs only its typed inputs "
            "for strict current native rebinding."
        ),
        basis=(
            f"candidate_contract={candidate.contract_id}; predicate={predicate}; "
            "saved execute_batch candidate inputs; replay-only contract reconstruction"
        ),
    )


def _record_routed(
    *,
    pair: Any,
    source_file: str,
    source_file_hash: str,
    candidate_index: int,
    envelope: dict[str, Any],
    baseline: CandidateIssue,
    routed: CandidateIssue,
    telemetry: dict[str, Any],
    contract_origin: Literal["saved_contract", "saved_selected_candidate"],
    replay_id: str,
    registry: Any,
) -> dict[str, Any]:
    """Compile and execute one re-bound structural candidate through pyfcstm."""

    obligation_id = f"{pair.pair_id}:structural-rebind:{candidate_index}"
    binding = bind_candidate(routed, pair.model)
    plan = compile_plan(
        routed,
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
        contract_id=routed.contract_id,
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
            reason="Provider-free structural-rebind replay reached one legal native terminal Boolean evaluation.",
            basis="saved selected candidate; current exact structural binder/compiler; real pyfcstm backend receipt",
            retry_records=[],
            execution_receipt=execution_receipt,
        )
    return StructuralRebindReplayRecord(
        schema="evidence-discovery.structural_rebind_replay_record.v1",
        pair_id=pair.pair_id,
        source_file=source_file,
        source_file_sha256=source_file_hash,
        source_candidate_index=candidate_index,
        source_candidate_sha256=_canonical_hash(envelope),
        source_obligation_id=str(envelope["obligation_id"]),
        contract_id=baseline.contract_id,
        contract_origin=contract_origin,
        baseline_predicate_id=baseline.predicate_id,
        baseline_candidate=baseline.model_dump(mode="json"),
        baseline_plan=envelope.get("plan") if isinstance(envelope.get("plan"), dict) else None,
        baseline_receipt=envelope.get("receipt") if isinstance(envelope.get("receipt"), dict) else None,
        baseline_binding_precise=bool(envelope.get("binding", {}).get("precise")),
        route_status=(
            "routed_executed"
            if execution_receipt["execution_state"] == "completed"
            else "routed_execution_degraded"
        ),
        route_telemetry=telemetry,
        candidate=routed.model_dump(mode="json"),
        binding=binding.model_dump(mode="json"),
        plan=plan.model_dump(mode="json"),
        receipt=receipt.model_dump(mode="json"),
        execution_receipt=execution_receipt,
        witness_level=witness_level,
        audit_bundle=audit_bundle,
        reason="The replay replaced only the saved structural input spelling with current exact native closure, then executed the production deterministic backend without a provider, Judge, ledger, or answer.",
        basis="immutable saved contract/grounding/candidate; frozen registry; strict typed compiler; pyfcstm-native backend receipt",
    ).model_dump(mode="json")


def _summary(
    replay_id: str,
    source_run_id: str,
    records: list[dict[str, Any]],
    *,
    historical_frontier_items_excluded: Counter[str] | None = None,
) -> dict[str, Any]:
    """Build fixed-cohort accounting without treating this audit as a hit metric."""

    baseline_verdicts = Counter(
        str(row["baseline_receipt"].get("verdict", "missing"))
        if isinstance(row.get("baseline_receipt"), dict)
        else "missing"
        for row in records
    )
    current_verdicts = Counter(
        str(row["receipt"].get("verdict", "not_attempted"))
        if isinstance(row.get("receipt"), dict)
        else "not_attempted"
        for row in records
    )
    changed = [
        row
        for row in records
        if row["baseline_predicate_id"] != row["candidate"].get("predicate_id")
        or row["baseline_candidate"].get("predicate_inputs")
        != row["candidate"].get("predicate_inputs")
    ]
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id in sorted({str(row["pair_id"]) for row in records}):
        rows = [row for row in records if row["pair_id"] == pair_id]
        per_pair[pair_id] = {
            "selected_structural_candidate_count": len(rows),
            "baseline_predicates": dict(Counter(row["baseline_predicate_id"] for row in rows)),
            "current_predicates": dict(
                Counter(str(row["candidate"].get("predicate_id")) for row in rows)
            ),
            "route_statuses": dict(Counter(row["route_status"] for row in rows)),
            "witness_levels": dict(Counter(row["witness_level"] for row in rows)),
            "route_changed_count": sum(row in changed for row in rows),
            "reason":"Per-pair rows keep the immutable selected-structural cohort separate from predicate-null route recovery, hit, and Judge metrics.",
            "basis":"StructuralRebindReplayRecord rows for this frozen pair.",
        }
    acceptance = {
        "provider_calls_zero": True,
        "judge_calls_zero": True,
        "all_rows_are_saved_selected_structural_candidates": all(
            row["baseline_predicate_id"] in STRUCTURAL_PREDICATES for row in records
        ),
        "every_routed_row_has_terminal_execution_audit": all(
            row["route_status"] == "route_unclosed"
            or isinstance(row.get("execution_receipt"), dict)
            and row["execution_receipt"].get("execution_state")
            in {"completed", "not_attempted", "failed"}
            for row in records
        ),
        "every_w2_has_audit_bundle": all(
            row["witness_level"] != "W2" or isinstance(row.get("audit_bundle"), dict)
            for row in records
        ),
        "no_unclosed_or_failed_row_claims_w2": all(
            row["route_status"] == "routed_executed" or row["witness_level"] != "W2"
            for row in records
        ),
    }
    return StructuralRebindReplaySummary(
        schema="evidence-discovery.structural_rebind_replay_summary.v1",
        replay_id=replay_id,
        source_run_id=source_run_id,
        provider_calls=0,
        judge_calls=0,
        selected_structural_candidate_count=len(records),
        baseline_predicates=dict(Counter(row["baseline_predicate_id"] for row in records)),
        current_predicates=dict(
            Counter(str(row["candidate"].get("predicate_id")) for row in records)
        ),
        route_statuses=dict(Counter(row["route_status"] for row in records)),
        witness_levels=dict(Counter(row["witness_level"] for row in records)),
        baseline_verdicts=dict(baseline_verdicts),
        current_verdicts=dict(current_verdicts),
        route_changed_count=len(changed),
        w2_audit_bundle_count=sum(
            isinstance(row.get("audit_bundle"), dict) for row in records
        ),
        historical_frontier_items_excluded=dict(
            historical_frontier_items_excluded or Counter()
        ),
        per_pair=per_pair,
        acceptance=acceptance,
        reason="This fixed-cohort replay audits only whether saved selected S2--S6 candidates remain legal after native typed rebinding. It is not a method rerun, publication decision, hit metric, or Judge result.",
        basis="immutable saved selected candidates plus current exact route/compiler/native backend implementations",
    ).model_dump(mode="json")


def _render_readme(manifest: dict[str, Any], summary: dict[str, Any]) -> str:
    """Render a concise English boundary statement for the immutable artifact."""

    return "\n".join(
        (
            "# Selected Structural Native-Rebind Replay",
            "",
            f"- source run: `{manifest['source_run_id']}`",
            f"- replay id: `{manifest['replay_id']}`",
            f"- provider calls: `{manifest['provider_calls']}`",
            f"- Judge calls: `{manifest['judge_calls']}`",
            f"- saved selected S2--S6 candidates: `{summary['selected_structural_candidate_count']}`",
            f"- route/input changed: `{summary['route_changed_count']}`",
            f"- W0/W1/W2: `{summary['witness_levels']}`",
            f"- excluded retired historical frontier items: `{summary['historical_frontier_items_excluded']}`",
            "",
            "This artifact audits only whether saved selected S2--S6 candidates retain legal typed inputs after current exact native rebinding, and preserves the current plan, pyfcstm receipt, W, and audit bundle. It does not read ledger expected items, L, Judge results, answers, or other pair outputs; call a provider or Judge; rewrite source method artifacts; or report hit, precision, or publication results. Predicate-null route replay and frontier replay remain separate artifacts and must not be combined with this result.",
            "",
        )
    )


def run_selected_structural_rebind_replay(
    *,
    source_run: str | Path,
    output_parent: str | Path,
) -> dict[str, Any]:
    """Replay saved selected S2--S6 candidates with current native typed closure."""

    source_root = Path(source_run).expanduser().resolve()
    manifest_path = source_root / "run_manifest.json"
    summary_path = source_root / "summary.json"
    if not manifest_path.is_file() or not summary_path.is_file():
        raise FileNotFoundError("source run must contain run_manifest.json and summary.json")
    source_manifest = _read_json(manifest_path)
    _read_json(summary_path)
    source_run_id = str(source_manifest.get("run_id"))
    if len(source_run_id) != 32 or any(character not in "0123456789abcdef" for character in source_run_id):
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
            "schema": STRUCTURAL_REBIND_REPLAY_SCHEMA,
            "source_manifest": _file_hash(manifest_path),
            "source_summary": _file_hash(summary_path),
            "registry_hash": registry.registry_hash,
            "policy": STRUCTURAL_REBIND_REPLAY_POLICY_VERSION,
            "implementation": implementation_hashes,
        }
    ).removeprefix("sha256:")[:32]
    final_parent = Path(output_parent).expanduser().resolve()
    final_parent.mkdir(parents=True, exist_ok=True)
    final_root = final_parent / replay_id
    if final_root.exists():
        raise FileExistsError(f"immutable structural-rebind replay output exists: {final_root}")
    stage_root = Path(tempfile.mkdtemp(prefix=f".{replay_id}.", dir=final_parent))
    try:
        manifest = StructuralRebindReplayManifest(
            schema="evidence-discovery.structural_rebind_replay_manifest.v1",
            replay_id=replay_id,
            generated_at=datetime.now(timezone.utc),
            source_run_path=str(source_root),
            source_run_id=source_run_id,
            source_run_manifest_sha256=_file_hash(manifest_path),
            source_summary_sha256=_file_hash(summary_path),
            registry_version=registry.version,
            registry_hash=registry.registry_hash,
            policy_version=STRUCTURAL_REBIND_REPLAY_POLICY_VERSION,
            implementation_hashes=implementation_hashes,
            provider_calls=0,
            judge_calls=0,
            reason="The replay preserves saved selected structural candidates and evaluates only the current deterministic native binder/compiler/backend chain.",
            basis="immutable source method cells, frozen registry, current structural binder/compiler/backend hashes, and no evaluation artifacts",
        ).model_dump(mode="json")
        records: list[dict[str, Any]] = []
        historical_frontier_items_excluded: Counter[str] = Counter()
        for method_path in method_paths:
            cell = _read_json(method_path)
            if cell.get("run_id") != source_run_id:
                raise ValueError(f"mixed source run identity in {method_path}")
            pair_id = cell.get("pair_id")
            if not isinstance(pair_id, str) or not pair_id.isdigit() or len(pair_id) != 4:
                raise ValueError(f"method cell has no valid frozen pair_id: {method_path}")
            pair = _load_current_pair_for_source_cell(pair_id, cell)
            contracts, grounding = _contracts_and_grounding(cell)
            historical_frontier_items_excluded.update(
                merge_saved_frontier_contracts(cell, contracts)
            )
            envelopes = _saved_candidate_envelopes(cell)
            candidates = tuple(
                CandidateIssue.model_validate(row["candidate"])
                for row in envelopes
                if isinstance(row.get("candidate"), dict)
            )
            if len(candidates) != len(envelopes):
                raise ValueError(f"method cell has a candidate envelope without a candidate object: {method_path}")
            replay_contracts = dict(contracts)
            reconstructed_origins: dict[
                str, Literal["saved_contract", "saved_selected_candidate"]
            ] = {
                contract_id: "saved_contract" for contract_id in replay_contracts
            }
            candidate_contract_origins: list[
                Literal["saved_contract", "saved_selected_candidate", "unavailable"]
            ] = []
            for baseline in candidates:
                known_origin = reconstructed_origins.get(baseline.contract_id)
                if known_origin is not None:
                    candidate_contract_origins.append(known_origin)
                    continue
                reconstructed = _saved_selected_structural_contract(baseline)
                if reconstructed is None:
                    candidate_contract_origins.append("unavailable")
                    continue
                replay_contracts[reconstructed.contract_id] = reconstructed
                reconstructed_origins[reconstructed.contract_id] = (
                    "saved_selected_candidate"
                )
                candidate_contract_origins.append("saved_selected_candidate")
            projection = route_primary_candidates(
                pair, replay_contracts, grounding, candidates
            )
            if len(projection.candidate_telemetry) != len(candidates):
                raise ValueError(
                    f"primary route emitted {len(projection.candidate_telemetry)} candidate telemetry rows for {len(candidates)} candidates in {method_path}"
                )
            source_file = method_path.relative_to(source_root).as_posix()
            source_file_hash = _file_hash(method_path)
            for index, (envelope, baseline, routed, route) in enumerate(
                zip(
                    envelopes,
                    candidates,
                    projection.candidates,
                    projection.candidate_telemetry,
                    strict=True,
                )
            ):
                if baseline.predicate_id not in STRUCTURAL_PREDICATES:
                    continue
                contract_origin = candidate_contract_origins[index]
                telemetry = route.model_dump(mode="json")
                if (
                    route.candidate_index != index
                    or route.contract_id != baseline.contract_id
                ):
                    raise ValueError(
                        "primary route candidate telemetry does not match its exact structural replay candidate: "
                        f"index={index}; contract={baseline.contract_id}; "
                        f"telemetry_index={route.candidate_index}; "
                        f"telemetry_contract={route.contract_id}"
                    )
                if not route.route_attempted:
                    routed = baseline.model_copy(
                        update={"predicate_id": None, "predicate_inputs": {}}
                    )
                    records.append(
                        _record_unclosed(
                            pair_id=pair_id,
                            source_file=source_file,
                            source_file_hash=source_file_hash,
                            candidate_index=index,
                            envelope=envelope,
                            baseline=baseline,
                            routed=routed,
                            telemetry={
                                "reason": (
                                    "The saved selected structural candidate has no "
                                    "extraction, grounding, saved-frontier, or complete "
                                    "replay-only typed contract available for current native rebinding."
                                ),
                                "basis": (
                                    "immutable execute_batch candidate plus complete saved "
                                    "contract/frontier lookup and constrained structural-input "
                                    "reconstruction"
                                ),
                            },
                            contract_origin=contract_origin,
                        )
                    )
                    continue
                if route.selected_predicate != routed.predicate_id:
                    raise ValueError(
                        "attempted primary route telemetry does not match its exact "
                        "structural replay candidate: "
                        f"index={index}; contract={baseline.contract_id}; "
                        f"origin={contract_origin}; "
                        f"telemetry_selected={route.selected_predicate}; "
                        f"candidate_selected={routed.predicate_id}"
                    )
                if routed.predicate_id is None:
                    records.append(
                        _record_unclosed(
                            pair_id=pair_id,
                            source_file=source_file,
                            source_file_hash=source_file_hash,
                            candidate_index=index,
                            envelope=envelope,
                            baseline=baseline,
                            routed=routed,
                            telemetry=telemetry,
                            contract_origin=contract_origin,
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
                        baseline=baseline,
                        routed=routed,
                        telemetry=telemetry,
                        contract_origin=contract_origin,
                        replay_id=replay_id,
                        registry=registry,
                    )
                )
        records.sort(key=lambda row: (row["pair_id"], row["source_candidate_index"]))
        summary = _summary(
            replay_id,
            source_run_id,
            records,
            historical_frontier_items_excluded=historical_frontier_items_excluded,
        )
        if not all(summary["acceptance"].values()):
            raise ValueError(f"structural-rebind replay acceptance failed: {summary['acceptance']}")
        audit_index: dict[str, dict[str, Any]] = {}
        for record in records:
            audit = record.get("audit_bundle")
            if not isinstance(audit, dict):
                continue
            name = f"{record['pair_id']}__selected_{record['source_candidate_index']}.json"
            write_json(stage_root / "audit_bundles" / name, audit)
            audit_index[f"{record['pair_id']}:{record['source_candidate_index']}"] = {
                "path": f"audit_bundles/{name}",
                "audit_hash": audit["audit_hash"],
                "predicate_id": record["candidate"]["predicate_id"],
                "reason": "Current selected-structural W2 audit is stored outside the immutable source method run.",
                "basis": "StructuralRebindReplayRecord.audit_bundle",
            }
        write_json(stage_root / "structural_rebind_replay_manifest.json", manifest)
        write_json(
            stage_root / "structural_rebind_replay_records.json",
            {"schema": STRUCTURAL_REBIND_REPLAY_SCHEMA, "records": records},
        )
        write_json(stage_root / "audit_index.json", audit_index)
        write_json(stage_root / "summary.json", summary)
        (stage_root / "README.md").write_text(
            _render_readme(manifest, summary), encoding="utf-8"
        )
        os.rename(stage_root, final_root)
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return {"replay_root": str(final_root), "replay_id": replay_id, "summary": summary}


def main(argv: list[str] | None = None) -> int:
    """Run the selected-structural native-rebind replay without external calls."""

    parser = argparse.ArgumentParser(
        description="Replay saved selected S2--S6 candidates through native typed rebinding."
    )
    parser.add_argument("--source-run", required=True, help="Immutable completed source method-run directory.")
    parser.add_argument("--output-parent", required=True, help="Immutable structural-rebind replay output parent.")
    args = parser.parse_args(argv)
    result = run_selected_structural_rebind_replay(
        source_run=args.source_run,
        output_parent=args.output_parent,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
