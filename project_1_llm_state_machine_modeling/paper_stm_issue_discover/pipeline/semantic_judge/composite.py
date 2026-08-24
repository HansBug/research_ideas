from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import Field

from .metrics import aggregate_outcomes
from .models import (
    FrozenModel,
    JudgeCallReceipt,
    PairJudgeResult,
    RunFailureSummary,
    RunManifest,
    RunPairFailure,
    RunSummary,
    SemanticMetrics,
)


class CompositeCallAudit(FrozenModel):
    """Deterministic call, retry, token, and cost totals across source runs."""

    logical_call_count: int = Field(
        ge=0, description="Number of primary or arbitration JudgeCallReceipt rows."
    )
    provider_request_count: int = Field(
        ge=0, description="Number of underlying usage rows, including schema repair requests."
    )
    completed_provider_request_count: int = Field(
        ge=0, description="Underlying usage rows whose normalized status is completed."
    )
    failed_provider_request_count: int = Field(
        ge=0, description="Underlying usage rows whose normalized status is not completed."
    )
    provider_error_attempt_count: int = Field(
        ge=0, description="Retry records explicitly owned by the provider or transport."
    )
    schema_validation_failure_count: int = Field(
        ge=0, description="Billable structured-output validation failures retained in retry receipts."
    )
    api_connection_error_count: int = Field(
        ge=0, description="Audited retry records containing APIConnectionError."
    )
    event_loop_closed_error_count: int = Field(
        ge=0, description="Audited retry records containing Event loop is closed."
    )
    input_tokens: int = Field(ge=0, description="All reported input tokens.")
    uncached_input_tokens: int = Field(
        ge=0, description="Input tokens after subtracting reported cache read and creation tokens."
    )
    cache_read_input_tokens: int = Field(
        ge=0, description="All normalized cache-read input tokens."
    )
    cache_creation_input_tokens: int = Field(
        ge=0, description="All normalized cache-creation or cache-write input tokens."
    )
    output_tokens: int = Field(ge=0, description="All reported output tokens.")
    cost_usd: float = Field(
        ge=0, description="Sum of all call costs, including billable schema repairs."
    )
    cost_eligible: bool = Field(
        description="Whether every source JudgeCallReceipt was eligible for pricing."
    )
    reason: str = Field(
        min_length=1, description="Deterministic interpretation of request and retry totals."
    )
    basis: str = Field(
        min_length=1, description="JudgeCallReceipt usage and retry records used for aggregation."
    )


class CompositeSourceRun(FrozenModel):
    """Immutable manifest and terminal receipt for one source Judge run."""

    run_id: str = Field(min_length=1, description="Original non-reusable Judge run ID.")
    manifest_path: str = Field(min_length=1, description="Exact RunManifest path.")
    manifest_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="RunManifest byte hash."
    )
    terminal_path: str = Field(
        min_length=1, description="Exact completed summary or failure-summary path."
    )
    terminal_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Terminal receipt byte hash."
    )
    terminal_status: Literal["completed", "failed"] = Field(
        description="Original source run terminal status; failed sources may be closed by a separate repair run."
    )
    judge_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Commit that executed this source run."
    )
    source_root: str = Field(
        min_length=1, description="Read-only historical method source root."
    )
    source_root_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Selected source-byte closure hash."
    )
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1, description="Pair selection frozen by this source manifest."
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="Round selection frozen by this source manifest."
    )
    completed_pair_count: int = Field(
        ge=0, description="PairJudgeResult receipts completed by this source run."
    )
    failure_count: int = Field(
        ge=0, description="Terminal pair failures preserved by this source run."
    )
    incurred_cost_usd: float = Field(
        ge=0, description="Original source terminal cost, including failed schema calls."
    )
    call_audit: CompositeCallAudit = Field(
        description="Complete call audit for successful and failed cells in this source run."
    )
    reason: str = Field(
        min_length=1, description="Why this source is included in the deterministic composite."
    )
    basis: str = Field(
        min_length=1, description="Manifest, terminal receipt, and byte-hash provenance."
    )


class CompositePairReceipt(FrozenModel):
    """One selected PairJudgeResult and its original source-run provenance."""

    pair_id: str = Field(pattern=r"^\d{4}$", description="Frozen pair ID.")
    round: int = Field(ge=1, description="Historical method round.")
    source_run_id: str = Field(
        min_length=1, description="Source run that produced this completed pair result."
    )
    result_path: str = Field(min_length=1, description="Exact PairJudgeResult path.")
    result_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="PairJudgeResult byte hash."
    )
    artifact_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Pair artifact-closure hash."
    )
    serialized_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Anonymous Judge input hash."
    )
    response_schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Dynamic response-schema closure hash."
    )
    prompt_template_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Frozen Judge prompt-template hash."
    )
    report_count: int = Field(ge=0, description="Raw released report count.")
    expected_count: int = Field(ge=0, description="Frozen expected denominator.")
    judge_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Commit that executed this pair result."
    )
    reason: str = Field(
        min_length=1, description="Selection and replacement status for this pair result."
    )
    basis: str = Field(
        min_length=1, description="Verified source receipt and PairJudgeResult byte hash."
    )


class RecoveredPairFailure(FrozenModel):
    """Original terminal pair failure closed by one later complete pair result."""

    pair_id: str = Field(pattern=r"^\d{4}$", description="Recovered pair ID.")
    round: int = Field(ge=1, description="Recovered historical round.")
    failed_run_id: str = Field(min_length=1, description="Original failed run ID.")
    failure_path: str = Field(min_length=1, description="Original RunPairFailure path owner.")
    failure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Stable hash of the RunPairFailure model."
    )
    original_failure_cost_usd: float = Field(
        ge=0, description="Billable cost incurred before the original terminal failure."
    )
    replacement_run_id: str = Field(
        min_length=1, description="Repair run that produced a complete PairJudgeResult."
    )
    replacement_result_path: str = Field(
        min_length=1, description="Replacement PairJudgeResult path."
    )
    replacement_result_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Replacement PairJudgeResult byte hash."
    )
    reason: str = Field(
        min_length=1, description="Why deterministic composition may replace the failed cell."
    )
    basis: str = Field(
        min_length=1, description="Same round/pair plus verified immutable input and artifact hashes."
    )


class CompositeRoundSummary(FrozenModel):
    """Deterministic metrics and cost for one complete 54-pair round."""

    round: int = Field(ge=1, description="Historical method round.")
    pair_count: int = Field(gt=0, description="Complete pair count in this round.")
    metrics: SemanticMetrics = Field(
        description="Issue #195 metrics recomputed from selected PairJudgeResult rows."
    )
    l2_expected_count: int = Field(ge=0, description="Ledger-side L2 denominator.")
    l2_full_hit_count: int = Field(ge=0, description="FULL-hit L2 expected positions.")
    l2_supported_count: int = Field(ge=0, description="FULL/PARTIAL-supported L2 positions.")
    selected_result_cost_usd: float = Field(
        ge=0, description="Cost of selected successful pair results, including repaired pairs."
    )
    reason: str = Field(
        min_length=1, description="Per-round completeness and metric conclusion."
    )
    basis: str = Field(
        min_length=1, description="Exact pair closure and deterministic metrics formula."
    )


class CrossRoundCoverage(FrozenModel):
    """Hit@3 and cross-round cluster view over one shared pair/ledger universe."""

    expected_issue_count: int = Field(
        ge=0, description="Unique expected issues in one ledger round."
    )
    full_hit_at_least_once_count: int = Field(
        ge=0, description="Expected issues FULL-hit in at least one selected round."
    )
    supported_at_least_once_count: int = Field(
        ge=0, description="Expected issues FULL/PARTIAL-supported in at least one round."
    )
    full_hit_all_rounds_count: int = Field(
        ge=0, description="Expected issues FULL-hit in every selected round."
    )
    raw_valid_novel_report_count: int = Field(
        ge=0, description="Raw VALID_NOVEL report rows across all rounds."
    )
    deduplicated_valid_novel_cluster_count: int = Field(
        ge=0, description="VALID_NOVEL shapes deduplicated by pair and root-cause key across rounds."
    )
    cross_round_cluster_count: int = Field(
        ge=0, description="All root-cause shapes deduplicated by pair and key across rounds."
    )
    cross_round_valid_cluster_count: int = Field(
        ge=0, description="Deduplicated shapes with at least one valid report."
    )
    cross_round_invalid_only_cluster_count: int = Field(
        ge=0, description="Deduplicated shapes represented only by INVALID reports."
    )
    cross_round_cluster_precision: float = Field(
        ge=0, le=1, description="Valid cross-round clusters divided by all cross-round clusters."
    )
    reason: str = Field(
        min_length=1, description="Distinction between raw reports, per-round metrics, and deduplicated shapes."
    )
    basis: str = Field(
        min_length=1, description="Expected ledger IDs and pair-namespaced root-cause keys."
    )


class CompositeRunSummary(FrozenModel):
    """Complete multi-source semantic Judge result with exact provenance closure."""

    schema_version: Literal["paper1.semantic-judge.composite-summary.v1"] = Field(
        default="paper1.semantic-judge.composite-summary.v1",
        description="Composite summary version that references immutable source runs without copying them into a false single-run identity.",
    )
    composite_id: str = Field(min_length=1, description="Unique deterministic aggregate ID.")
    source_runs: tuple[CompositeSourceRun, ...] = Field(
        min_length=1, description="Every source run, including failed runs and repair runs."
    )
    pair_receipts: tuple[CompositePairReceipt, ...] = Field(
        min_length=1, description="Exact selected pair-by-round result closure."
    )
    recovered_failures: tuple[RecoveredPairFailure, ...] = Field(
        description="Original failures closed by separate complete replacement runs."
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="Complete selected round set."
    )
    pair_ids: tuple[str, ...] = Field(
        min_length=1, description="Shared exact pair universe present in every round."
    )
    protocol_version: str = Field(min_length=1, description="Frozen issue #195 protocol.")
    protocol_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$", description="Frozen protocol snapshot hash."
    )
    judge_algorithm_version: str = Field(
        min_length=1, description="Frozen semantic Judge algorithm version."
    )
    semantic_judge_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Frozen semantic Judge commit."
    )
    execution_erratum_commit: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{40}$",
        description="Runtime-only schema-repair erratum commit; null means no source required repair."
    )
    execution_erratum_paths: tuple[str, ...] = Field(
        description="Exact tracked paths changed by the runtime-only erratum; empty when no erratum was used."
    )
    model_profile: str = Field(min_length=1, description="Arm-neutral Judge profile.")
    ledger_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Frozen 145-item ledger byte hash."
    )
    prompt_template_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Single prompt-template hash shared by every pair."
    )
    round_summaries: tuple[CompositeRoundSummary, ...] = Field(
        min_length=1, description="Deterministic metrics for every selected round."
    )
    overall: SemanticMetrics = Field(
        description="Raw pair-by-round aggregate metrics; clusters are namespaced by round and pair."
    )
    l2_expected_count: int = Field(
        ge=0, description="L2 expected positions across all selected rounds."
    )
    l2_full_hit_count: int = Field(
        ge=0, description="FULL-hit L2 positions across all selected rounds."
    )
    l2_supported_count: int = Field(
        ge=0, description="FULL/PARTIAL-supported L2 positions across all rounds."
    )
    cross_round: CrossRoundCoverage = Field(
        description="Hit@3 and deduplicated cross-round cluster summary."
    )
    call_audit: CompositeCallAudit = Field(
        description="All successful, failed, and repair call accounting."
    )
    selected_result_cost_usd: float = Field(
        ge=0, description="Cost attached to the complete selected PairJudgeResult closure."
    )
    original_failure_cost_usd: float = Field(
        ge=0, description="Cost of original failed cells retained for execution audit."
    )
    repair_result_cost_usd: float = Field(
        ge=0, description="Cost of successful replacement PairJudgeResult runs."
    )
    total_incurred_cost_usd: float = Field(
        ge=0, description="All source terminal costs without hiding failed attempts."
    )
    status: Literal["completed"] = Field(
        default="completed", description="Complete only after exact pair/round and failure-recovery closure."
    )
    reason: str = Field(
        min_length=1, description="Composite completeness, fairness, and result conclusion."
    )
    basis: str = Field(
        min_length=1, description="Source hashes, code commits, frozen protocol, and deterministic recomputation."
    )


def _byte_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _model_hash(model: FrozenModel) -> str:
    payload = json.dumps(
        model.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _retry_payloads(call: JudgeCallReceipt) -> Iterable[Mapping[str, Any]]:
    for retry in call.retries:
        try:
            value = json.loads(retry.raw_attempt_json)
        except json.JSONDecodeError:
            continue
        if isinstance(value, Mapping):
            yield value


def _call_audit(calls: Sequence[JudgeCallReceipt]) -> CompositeCallAudit:
    provider_requests = [usage for call in calls for usage in call.usage]
    retry_payloads = [payload for call in calls for payload in _retry_payloads(call)]
    retry_text = "\n".join(
        json.dumps(payload, sort_keys=True, ensure_ascii=True)
        for payload in retry_payloads
    ).lower()
    schema_failures = sum(
        len(value)
        for payload in retry_payloads
        for value in (payload.get("schema_validation_failures"),)
        if isinstance(value, list)
    )
    input_tokens = sum(usage.input_tokens or 0 for usage in provider_requests)
    cache_read = sum(usage.cache_read_input_tokens or 0 for usage in provider_requests)
    cache_creation = sum(
        usage.cache_write_input_tokens or 0 for usage in provider_requests
    )
    return CompositeCallAudit(
        logical_call_count=len(calls),
        provider_request_count=len(provider_requests),
        completed_provider_request_count=sum(
            usage.status == "completed" for usage in provider_requests
        ),
        failed_provider_request_count=sum(
            usage.status != "completed" for usage in provider_requests
        ),
        provider_error_attempt_count=sum(
            retry.provider_error for call in calls for retry in call.retries
        ),
        schema_validation_failure_count=schema_failures,
        api_connection_error_count=retry_text.count("apiconnectionerror"),
        event_loop_closed_error_count=retry_text.count("event loop is closed"),
        input_tokens=input_tokens,
        uncached_input_tokens=max(0, input_tokens - cache_read - cache_creation),
        cache_read_input_tokens=cache_read,
        cache_creation_input_tokens=cache_creation,
        output_tokens=sum(usage.output_tokens or 0 for usage in provider_requests),
        cost_usd=sum(call.cost_usd for call in calls),
        cost_eligible=all(call.cost_eligible for call in calls),
        reason="Counts preserve every successful request, billable schema repair, and provider-owned retry without converting failures into semantic outcomes.",
        basis="Deterministic aggregation of JudgeCallReceipt.usage and RetryRecord.raw_attempt_json.",
    )


def _replacement_result_cost(
    selected_cost_by_key: Mapping[tuple[int, str], float],
    recovered_keys: Iterable[tuple[int, str]],
) -> float:
    """Return selected-result cost for cells that replace recorded failures."""

    return sum(selected_cost_by_key[key] for key in recovered_keys)


def _ledger_l2_ids(path: Path) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items") if isinstance(payload, Mapping) else None
    if not isinstance(items, Mapping):
        raise TypeError("ledger items must be an object")
    return {
        str(item.get("id") or ledger_id)
        for ledger_id, item in items.items()
        if isinstance(item, Mapping) and item.get("L") == "L2"
    }


def _singleton(values: Iterable[str], label: str) -> str:
    unique = set(values)
    if len(unique) != 1:
        raise ValueError(f"{label} must have one value, got {sorted(unique)}")
    return next(iter(unique))


def build_composite(
    *,
    composite_id: str,
    source_roots: Sequence[Path],
    ledger_path: Path,
    semantic_judge_commit: str,
    execution_erratum_commit: str | None,
    execution_erratum_paths: tuple[str, ...],
    expected_pair_count: int,
) -> CompositeRunSummary:
    """Build one exact composite from immutable terminal Judge run artifacts."""

    source_audits: list[CompositeSourceRun] = []
    pair_results: dict[tuple[int, str], tuple[PairJudgeResult, CompositePairReceipt]] = {}
    failures: list[tuple[RunPairFailure, str, str]] = []
    all_calls: list[JudgeCallReceipt] = []
    manifests: list[RunManifest] = []
    total_incurred_cost = 0.0

    for source_root in source_roots:
        manifest_path = source_root / "run_manifest.json"
        summary_path = source_root / "summary.json"
        failure_path = source_root / "failure_summary.json"
        if summary_path.is_file() == failure_path.is_file():
            raise ValueError(
                f"{source_root} must contain exactly one summary.json or failure_summary.json"
            )
        manifest = RunManifest.model_validate_json(
            manifest_path.read_text(encoding="utf-8")
        )
        manifests.append(manifest)
        terminal_path = summary_path if summary_path.is_file() else failure_path
        if summary_path.is_file():
            terminal: RunSummary | RunFailureSummary = RunSummary.model_validate_json(
                summary_path.read_text(encoding="utf-8")
            )
            receipts = terminal.pair_receipts
            terminal_failures: tuple[RunPairFailure, ...] = ()
        else:
            terminal = RunFailureSummary.model_validate_json(
                failure_path.read_text(encoding="utf-8")
            )
            receipts = terminal.completed_pair_receipts
            terminal_failures = terminal.failures
        if terminal.run_id != manifest.run_id:
            raise ValueError(f"run ID mismatch under {source_root}")
        if terminal.manifest_hash != _byte_hash(manifest_path):
            raise ValueError(f"manifest hash mismatch under {source_root}")

        source_calls: list[JudgeCallReceipt] = []
        for receipt in receipts:
            result_path = Path(receipt.result_path)
            if _byte_hash(result_path) != receipt.result_hash:
                raise ValueError(f"result hash mismatch: {result_path}")
            result = PairJudgeResult.model_validate_json(
                result_path.read_text(encoding="utf-8")
            )
            if (result.pair_id, result.round) != (receipt.pair_id, receipt.round):
                raise ValueError(f"pair/round mismatch: {result_path}")
            if result.judge_code_commit != manifest.judge_code_commit:
                raise ValueError(f"result/manifest commit mismatch: {result_path}")
            key = (result.round, result.pair_id)
            if key in pair_results:
                raise ValueError(f"duplicate completed pair result: {key}")
            pair_receipt = CompositePairReceipt(
                pair_id=result.pair_id,
                round=result.round,
                source_run_id=manifest.run_id,
                result_path=str(result_path.resolve()),
                result_hash=receipt.result_hash,
                artifact_closure_hash=result.artifact_closure_hash,
                serialized_input_hash=result.serialized_input_hash,
                response_schema_hash=result.response_schema_hash,
                prompt_template_hash=result.prompt_template_hash,
                report_count=len(result.report_outcomes),
                expected_count=len(result.expected_outcomes),
                judge_code_commit=result.judge_code_commit,
                reason=(
                    "Complete replacement result from the runtime execution erratum."
                    if execution_erratum_commit is not None
                    and result.judge_code_commit == execution_erratum_commit
                    else "Complete result from the frozen semantic Judge run."
                ),
                basis=f"{manifest.run_id}; {receipt.result_hash}; immutable PairJudgeResult bytes",
            )
            pair_results[key] = (result, pair_receipt)
            source_calls.extend(result.call_receipts)
        for failure in terminal_failures:
            failures.append((failure, manifest.run_id, str(terminal_path.resolve())))
            source_calls.extend(failure.call_receipts)
        all_calls.extend(source_calls)
        source_cost = terminal.total_judge_cost_usd
        if abs(source_cost - sum(call.cost_usd for call in source_calls)) > 1e-9:
            raise ValueError(f"source cost does not close: {source_root}")
        total_incurred_cost += source_cost
        source_audits.append(
            CompositeSourceRun(
                run_id=manifest.run_id,
                manifest_path=str(manifest_path.resolve()),
                manifest_hash=_byte_hash(manifest_path),
                terminal_path=str(terminal_path.resolve()),
                terminal_hash=_byte_hash(terminal_path),
                terminal_status=terminal.status,
                judge_code_commit=manifest.judge_code_commit,
                source_root=manifest.source_root,
                source_root_hash=manifest.source_root_hash,
                selected_pair_ids=manifest.selected_pair_ids,
                selected_rounds=manifest.selected_rounds,
                completed_pair_count=len(receipts),
                failure_count=len(terminal_failures),
                incurred_cost_usd=source_cost,
                call_audit=_call_audit(source_calls),
                reason="Immutable terminal source retained as a separate provenance unit.",
                basis=f"{_byte_hash(manifest_path)}; {_byte_hash(terminal_path)}",
            )
        )

    allowed_commits = {semantic_judge_commit}
    if execution_erratum_commit is not None:
        allowed_commits.add(execution_erratum_commit)
    observed_commits = {manifest.judge_code_commit for manifest in manifests}
    if observed_commits != allowed_commits:
        raise ValueError(
            f"source commit closure {sorted(observed_commits)} != {sorted(allowed_commits)}"
        )
    protocol_version = _singleton(
        (manifest.protocol_version for manifest in manifests), "protocol_version"
    )
    protocol_sha256 = _singleton(
        (manifest.protocol_sha256 for manifest in manifests), "protocol_sha256"
    )
    algorithm = _singleton(
        (manifest.judge_algorithm_version for manifest in manifests),
        "judge_algorithm_version",
    )
    model_profile = _singleton(
        (manifest.model_profile for manifest in manifests), "model_profile"
    )
    ledger_hash = _singleton(
        (manifest.ledger_hash for manifest in manifests), "ledger_hash"
    )
    prompt_hash = _singleton(
        (result.prompt_template_hash for result, _receipt in pair_results.values()),
        "prompt_template_hash",
    )

    rounds = tuple(sorted({round_index for round_index, _pair_id in pair_results}))
    round_pair_ids = {
        round_index: {
            pair_id for result_round, pair_id in pair_results if result_round == round_index
        }
        for round_index in rounds
    }
    pair_ids = tuple(sorted(next(iter(round_pair_ids.values()))))
    if len(pair_ids) != expected_pair_count:
        raise ValueError(f"expected {expected_pair_count} pairs, got {len(pair_ids)}")
    for round_index, ids in round_pair_ids.items():
        if ids != set(pair_ids):
            raise ValueError(f"round {round_index} has a different pair universe")

    recovered: list[RecoveredPairFailure] = []
    for failure, failed_run_id, failure_owner_path in failures:
        replacement = pair_results.get((failure.round, failure.pair_id))
        if replacement is None:
            raise ValueError(
                f"unrecovered source failure: round={failure.round} pair={failure.pair_id}"
            )
        _result, replacement_receipt = replacement
        if replacement_receipt.source_run_id == failed_run_id:
            raise ValueError(f"failure was not replaced by a separate run: {failure.pair_id}")
        recovered.append(
            RecoveredPairFailure(
                pair_id=failure.pair_id,
                round=failure.round,
                failed_run_id=failed_run_id,
                failure_path=failure_owner_path,
                failure_hash=_model_hash(failure),
                original_failure_cost_usd=failure.total_judge_cost_usd,
                replacement_run_id=replacement_receipt.source_run_id,
                replacement_result_path=replacement_receipt.result_path,
                replacement_result_hash=replacement_receipt.result_hash,
                reason="The original schema-terminal cell remains failed; a separate complete run supplies this pair result.",
                basis=(
                    f"round={failure.round}; pair={failure.pair_id}; "
                    f"artifact_closure={replacement_receipt.artifact_closure_hash}"
                ),
            )
        )

    l2_ids = _ledger_l2_ids(ledger_path)
    round_summaries: list[CompositeRoundSummary] = []
    for round_index in rounds:
        results = [
            result
            for (result_round, _pair_id), (result, _receipt) in pair_results.items()
            if result_round == round_index
        ]
        metrics = aggregate_outcomes(
            (
                (result.pair_id, report)
                for result in results
                for report in result.report_outcomes
            ),
            (
                (result.pair_id, expected)
                for result in results
                for expected in result.expected_outcomes
            ),
        )
        l2_outcomes = [
            expected
            for result in results
            for expected in result.expected_outcomes
            if expected.ledger_id in l2_ids
        ]
        round_summaries.append(
            CompositeRoundSummary(
                round=round_index,
                pair_count=len(results),
                metrics=metrics,
                l2_expected_count=len(l2_outcomes),
                l2_full_hit_count=sum(item.hit for item in l2_outcomes),
                l2_supported_count=sum(item.supported for item in l2_outcomes),
                selected_result_cost_usd=sum(
                    call.cost_usd for result in results for call in result.call_receipts
                ),
                reason="Every pair in the shared universe contributes exactly one complete result.",
                basis=f"round={round_index}; pair_count={len(results)}; issue #195 aggregate_outcomes",
            )
        )

    ordered_results = [
        pair_results[key][0]
        for key in sorted(pair_results)
    ]
    overall = aggregate_outcomes(
        (
            (f"r{result.round}:{result.pair_id}", report)
            for result in ordered_results
            for report in result.report_outcomes
        ),
        (
            (f"r{result.round}:{result.pair_id}", expected)
            for result in ordered_results
            for expected in result.expected_outcomes
        ),
    )
    all_l2 = [
        expected
        for result in ordered_results
        for expected in result.expected_outcomes
        if expected.ledger_id in l2_ids
    ]
    expected_rounds: dict[tuple[str, str], list[tuple[bool, bool]]] = defaultdict(list)
    clusters: dict[tuple[str, str], set[str]] = defaultdict(set)
    novel_clusters: set[tuple[str, str]] = set()
    raw_novel_count = 0
    for result in ordered_results:
        for expected in result.expected_outcomes:
            expected_rounds[(result.pair_id, expected.ledger_id)].append(
                (expected.hit, expected.supported)
            )
        for report in result.report_outcomes:
            validity = report.validity.value
            clusters[(result.pair_id, report.root_cause_cluster_key)].add(validity)
            if validity == "VALID_NOVEL":
                raw_novel_count += 1
                novel_clusters.add((result.pair_id, report.root_cause_cluster_key))
    valid_clusters = sum(
        any(value != "INVALID" for value in validities)
        for validities in clusters.values()
    )
    cross_round = CrossRoundCoverage(
        expected_issue_count=len(expected_rounds),
        full_hit_at_least_once_count=sum(
            any(hit for hit, _supported in values)
            for values in expected_rounds.values()
        ),
        supported_at_least_once_count=sum(
            any(supported for _hit, supported in values)
            for values in expected_rounds.values()
        ),
        full_hit_all_rounds_count=sum(
            len(values) == len(rounds) and all(hit for hit, _supported in values)
            for values in expected_rounds.values()
        ),
        raw_valid_novel_report_count=raw_novel_count,
        deduplicated_valid_novel_cluster_count=len(novel_clusters),
        cross_round_cluster_count=len(clusters),
        cross_round_valid_cluster_count=valid_clusters,
        cross_round_invalid_only_cluster_count=len(clusters) - valid_clusters,
        cross_round_cluster_precision=(valid_clusters / len(clusters) if clusters else 1.0),
        reason="Raw novel reports remain report counts; pair-namespaced root-cause keys provide a separate cross-round shape count.",
        basis="FULL/support ledger IDs across rounds and pair-namespaced final root_cause_cluster_key values.",
    )
    selected_cost_by_key = {
        key: sum(call.cost_usd for call in result.call_receipts)
        for key, (result, _receipt) in pair_results.items()
    }
    selected_result_cost = sum(selected_cost_by_key.values())
    original_failure_cost = sum(
        failure.total_judge_cost_usd for failure, _run_id, _path in failures
    )
    repair_result_cost = _replacement_result_cost(
        selected_cost_by_key,
        ((item.round, item.pair_id) for item in recovered),
    )
    call_audit = _call_audit(all_calls)
    if abs(call_audit.cost_usd - total_incurred_cost) > 1e-9:
        raise ValueError("composite call cost does not equal source terminal cost")
    return CompositeRunSummary(
        composite_id=composite_id,
        source_runs=tuple(source_audits),
        pair_receipts=tuple(
            pair_results[key][1] for key in sorted(pair_results)
        ),
        recovered_failures=tuple(sorted(recovered, key=lambda item: (item.round, item.pair_id))),
        selected_rounds=rounds,
        pair_ids=pair_ids,
        protocol_version=protocol_version,
        protocol_sha256=protocol_sha256,
        judge_algorithm_version=algorithm,
        semantic_judge_commit=semantic_judge_commit,
        execution_erratum_commit=execution_erratum_commit,
        execution_erratum_paths=execution_erratum_paths,
        model_profile=model_profile,
        ledger_hash=ledger_hash,
        prompt_template_hash=prompt_hash,
        round_summaries=tuple(round_summaries),
        overall=overall,
        l2_expected_count=len(all_l2),
        l2_full_hit_count=sum(item.hit for item in all_l2),
        l2_supported_count=sum(item.supported for item in all_l2),
        cross_round=cross_round,
        call_audit=call_audit,
        selected_result_cost_usd=selected_result_cost,
        original_failure_cost_usd=original_failure_cost,
        repair_result_cost_usd=repair_result_cost,
        total_incurred_cost_usd=total_incurred_cost,
        reason="Every source run remains separately identified and every pair/round has one hash-verified complete result under the frozen semantic protocol.",
        basis=(
            f"{protocol_version}; {algorithm}; semantic_commit={semantic_judge_commit}; "
            f"execution_erratum={execution_erratum_commit}; source_runs={len(source_roots)}"
        ),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compose immutable semantic Judge runs without rerunning successful pairs."
    )
    parser.add_argument("--composite-id", required=True)
    parser.add_argument("--source-run-root", action="append", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--semantic-judge-commit", required=True)
    parser.add_argument("--execution-erratum-commit")
    parser.add_argument("--execution-erratum-path", action="append", default=[])
    parser.add_argument("--expected-pair-count", type=int, default=54)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate source closure and write one canonical composite summary."""

    args = _parser().parse_args(argv)
    summary = build_composite(
        composite_id=args.composite_id,
        source_roots=tuple(path.resolve() for path in args.source_run_root),
        ledger_path=args.ledger.resolve(),
        semantic_judge_commit=args.semantic_judge_commit,
        execution_erratum_commit=args.execution_erratum_commit,
        execution_erratum_paths=tuple(args.execution_erratum_path),
        expected_pair_count=args.expected_pair_count,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = summary.model_dump_json(indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
