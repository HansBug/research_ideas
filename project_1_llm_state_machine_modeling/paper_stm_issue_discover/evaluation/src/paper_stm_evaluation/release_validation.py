"""Provider-free release-candidate reference extraction and regression analysis.

This evaluator module is deliberately outside the method and Semantic Judge
packages.  It reads immutable v60 archive bytes and newly written release
validation artifacts, then calculates comparison metrics without providing
any value to discovery, grounding, routing, execution, or Judge decisions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .stage_loss import build_stage_loss_audit


FIXED_PAIR_IDS = (
    "0001", "0002", "0004", "0010", "0012", "0013", "0023", "0024",
    "0029", "0035", "0046", "0049", "0053", "0054", "0056",
)
WITNESS_RANK = {"W0": 0, "W1": 1, "W2": 2}
VALIDITIES = ("VALID_KNOWN", "VALID_NOVEL", "INVALID")


class ArtifactReference(BaseModel):
    """Repository-relative, SHA-256-addressed read-only input artifact."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str = Field(description="Repository-relative path to the immutable input artifact.")
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the exact referenced bytes.")
    reason: str = Field(min_length=1, description="Why this artifact is required for the evaluator-only release comparison.")
    basis: str = Field(min_length=1, description="Mechanical integrity and selection basis for the reference.")


class Ratio(BaseModel):
    """A count, explicit denominator, and mechanically derived rate."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    count: int = Field(ge=0, description="Numerator count under the stated metric definition.")
    denominator: int = Field(ge=0, description="Exact population denominator; it is never inferred from a percentage.")
    rate: float | None = Field(description="Count divided by denominator, or null only when denominator is zero.")


class FixedCellReference(BaseModel):
    """One fixed pair-round's method and composite-selected Judge bytes."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen state-machine pair identifier.")
    round: int = Field(ge=1, description="Method and Judge round number in the archived v60 run.")
    method: ArtifactReference = Field(description="Exact archived method cell JSON used by the reference.")
    judge: ArtifactReference = Field(description="Exact composite-selected Judge PairJudgeResult JSON used by the reference.")
    judge_source_run_id: str = Field(min_length=1, description="Archived Judge source run selected by the v60 composite for this cell.")
    expected_count: int = Field(ge=0, description="Expected issue rows in the selected Judge pair result.")
    report_count: int = Field(ge=0, description="Method-generated reports consumed by the selected Judge pair result.")
    reason: str = Field(min_length=1, description="Why these paired cell artifacts form one v60 reference observation.")
    basis: str = Field(min_length=1, description="Composite receipt mapping and SHA-256 closure basis.")


class RunMetrics(BaseModel):
    """Evaluator-only metrics for one fixed pair set and one or more rounds."""

    model_config = ConfigDict(extra="forbid")

    pair_ids: tuple[str, ...] = Field(min_length=1, description="Exact ordered frozen pair set included in this summary.")
    rounds: tuple[int, ...] = Field(min_length=1, description="Method/Judge rounds represented by this summary.")
    method_terminal_cells: Ratio = Field(description="Terminal method cells divided by expected selected cells.")
    expected_rows: int = Field(ge=0, description="Number of Judge expected-issue rows over all included rounds.")
    expected_issues: int = Field(ge=0, description="Unique expected ledger issues represented by the fixed pair set.")
    overall_full: Ratio = Field(description="Round-level FULL expected hits over expected rows.")
    l2_full: Ratio = Field(description="Round-level L2 FULL expected hits over L2 expected rows.")
    hit_at_3: Ratio | None = Field(description="Unique expected issues with at least one FULL across exactly three rounds; null for a one-round run.")
    hit_at_all: Ratio | None = Field(description="Unique expected issues FULL in all exactly three rounds; null for a one-round run.")
    semantic_precision: Ratio = Field(description="VALID_KNOWN plus VALID_NOVEL reports over all Judge reports.")
    root_cause_cluster_precision: Ratio = Field(description="Valid root-cause clusters over all root-cause clusters.")
    report_validity: dict[str, int] = Field(description="Report-level VALID_KNOWN, VALID_NOVEL, and INVALID counts.")
    cluster_validity: dict[str, int] = Field(description="Root-cause-cluster VALID_KNOWN, VALID_NOVEL, VALID, and INVALID counts.")
    full_hit_max_witness: dict[str, Ratio] = Field(description="FULL-hit maximum W2/W1/W0 counts with the shared FULL-hit denominator.")
    w2_all_expected: Ratio = Field(description="Expected rows whose FULL or PARTIAL support has maximum W2, over all expected rows.")
    predicate_usage: dict[str, Any] = Field(description="Terminal predicate receipt usage, verdicts, failures, and FULL-hit contributions over the fixed set.")
    d_levels: dict[str, int] = Field(description="Method evidence-record D0/D1/D2/D_UNRESOLVED distribution.")
    stage_loss: dict[str, int] = Field(description="Evaluator-derived expected-row root-cause owner counts.")
    method_billing: dict[str, Any] = Field(description="Method call, token, cache, retry, cost, and eligibility audit.")
    judge_billing: dict[str, Any] = Field(description="Judge call, token, cache, retry, cost, and eligibility audit.")
    per_round: list[dict[str, Any]] = Field(description="Separate fixed-denominator aggregate metrics for every represented round.")
    reason: str = Field(min_length=1, description="Metric-scope explanation that keeps method evidence and Judge evaluation separate.")
    basis: str = Field(min_length=1, description="Method cell, Judge result, ledger, receipt, and evaluator-stage-loss basis.")


class V60ReferenceArtifact(BaseModel):
    """Persisted fixed-15-pair v60 reference derived solely from final archive bytes."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["paper1.release-validation.v60-15pair-reference.v1"] = Field(default="paper1.release-validation.v60-15pair-reference.v1", description="Versioned schema identifier for the fixed v60 release-validation reference.")
    fixed_pair_ids: tuple[str, ...] = Field(min_length=1, description="Pre-registered release-validation pair order.")
    internal_rc_commit: str = Field(pattern=r"^[0-9a-f]{40}$", description="Internal technical release candidate commit being validated against v60.")
    v60_method_commit: str = Field(pattern=r"^[0-9a-f]{40}$", description="Immutable v60 method execution commit, not the refactor commit.")
    v60_judge_commit: str = Field(pattern=r"^[0-9a-f]{40}$", description="Immutable Semantic Judge execution commit, not the refactor commit.")
    method_manifest: ArtifactReference = Field(description="Archived v60 method run manifest reference.")
    judge_composite: ArtifactReference = Field(description="Archived v60 composite summary reference.")
    ledger: ArtifactReference = Field(description="Archived expected-issue ledger reference.")
    method_configuration: dict[str, Any] = Field(description="Mechanically selected v60 method profile, retries, streaming, worker, and immutable hash configuration.")
    judge_configuration: dict[str, Any] = Field(description="Mechanically selected v60 Judge profile, protocol, batching, retry, and worker configuration.")
    cells: tuple[FixedCellReference, ...] = Field(min_length=1, description="All 15 pairs by all three archived v60 rounds with selected raw references.")
    metrics: RunMetrics = Field(description="Provider-free fixed-15-pair v60 aggregate and per-round reference metrics.")
    stage_loss_audit: ArtifactReference = Field(description="Provider-free evaluator stage-loss output written outside the frozen archive.")
    reason: str = Field(min_length=1, description="Why the v60 subset is retained as an immutable three-round comparison reference.")
    basis: str = Field(min_length=1, description="Final archive bytes, composite selection, SHA-256 validation, and offline evaluator basis.")


class ReleaseComparisonArtifact(BaseModel):
    """Release-candidate versus v60 fixed-subset comparison without causal overclaim."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["paper1.release-validation.comparison.v1"] = Field(default="paper1.release-validation.comparison.v1", description="Versioned schema identifier for one release-validation comparison.")
    reference: ArtifactReference = Field(description="Fixed v60 reference JSON used as the before side.")
    release_method_manifest: ArtifactReference = Field(description="New installed-release method run manifest used as the after side.")
    release_judge_manifest: ArtifactReference = Field(description="New installed-release Judge run manifest used as the after side.")
    release_metrics: RunMetrics = Field(description="Provider-free aggregate metrics from the one new 15x1 method plus Judge run.")
    deterministic_invariants: dict[str, dict[str, Any]] = Field(description="Hash, input-closure, protocol, terminal-cell, and carrier invariant checks.")
    matched_carriers: dict[str, Any] = Field(description="Exact typed carrier intersection, zero-flip check, and one-sided carrier counts.")
    stochastic_comparison: dict[str, Any] = Field(description="v60 round envelope, mean, soft-band checks, and non-causal interpretation for stochastic metrics.")
    conclusion: str = Field(min_length=1, description="Evidence-bounded release-regression conclusion, not a new experiment result claim.")
    reason: str = Field(min_length=1, description="Why this comparison is post-hoc evaluator-only and never feeds either arm.")
    basis: str = Field(min_length=1, description="Stable raw artifact references, receipt hashes, and mechanical metric derivation.")


class InternalValidationManifest(BaseModel):
    """Pre-provider contract for the one authorized internal 15-pair validation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["paper1.release-validation.internal-manifest.v1"] = Field(default="paper1.release-validation.internal-manifest.v1", description="Versioned schema identifier for the pre-provider internal validation contract.")
    internal_rc_tag: str = Field(min_length=1, description="Annotated internal technical release-candidate tag used to build both packages.")
    internal_rc_commit: str = Field(pattern=r"^[0-9a-f]{40}$", description="Exact release-candidate commit, distinct from the historical experiment commits.")
    method_release_manifest: ArtifactReference = Field(description="Byte-copy-only method package manifest built from the internal RC.")
    judge_release_manifest: ArtifactReference = Field(description="Byte-copy-only Judge package manifest built from the internal RC.")
    v60_reference: ArtifactReference = Field(description="Fixed v60 15-pair three-round reference selected before any new provider call.")
    method_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Fresh exact run ID reserved for the single method 15x1 execution.")
    judge_run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Fresh exact run ID reserved for the single Judge pass over method terminal artifacts.")
    fixed_pair_ids: tuple[str, ...] = Field(min_length=1, description="Pre-registered pair order; no pair may be added or substituted after this manifest is written.")
    input_closure_root: str = Field(min_length=1, description="Repository-relative v60 input closure root supplied to the installed method/Judge packages.")
    method_configuration: dict[str, Any] = Field(description="Mechanically copied v60 profile, worker, retry, streaming, and hash configuration with the new one-round scope.")
    judge_configuration: dict[str, Any] = Field(description="Mechanically copied v60 Judge profile, protocol, batching, retry, and one-round configuration.")
    provider_authorization: dict[str, int] = Field(description="Hard upper bounds for the authorized method/Judge run count; zero denotes no additional run is allowed.")
    provider_call_count_before_live: Literal[0] = Field(default=0, description="Provider calls performed to prepare this manifest; always zero.")
    billable_call_count_before_live: Literal[0] = Field(default=0, description="Billable calls performed to prepare this manifest; always zero.")
    reason: str = Field(min_length=1, description="Why this is an internal technical regression contract rather than public distribution or a new research experiment.")
    basis: str = Field(min_length=1, description="RC release manifests, v60 reference, fixed pair set, and frozen archived run configuration basis.")


class InputClosurePreflight(BaseModel):
    """Read-only hash proof that the live input closure matches every v60 cell reference."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["paper1.release-validation.input-closure-preflight.v1"] = Field(default="paper1.release-validation.input-closure-preflight.v1", description="Versioned schema identifier for the pre-provider input-closure hash audit.")
    reference: ArtifactReference = Field(description="Fixed v60 reference JSON whose method-cell context manifests are checked.")
    input_closure_root: str = Field(min_length=1, description="Repository-relative input closure root supplied to the installed release packages.")
    checked_cells: int = Field(ge=0, description="Number of archived v60 method cells whose complete context manifest was read.")
    checked_artifacts: int = Field(ge=0, description="Number of individual input artifact path/hash checks performed.")
    pair_manifest_hashes: dict[str, dict[str, str]] = Field(description="Per-pair archived context manifest hashes and the repeated rounds used to verify closure stability.")
    mismatches: tuple[str, ...] = Field(description="Exact absent, path, or SHA-256 mismatches; empty is required before the one live run.")
    passed: bool = Field(description="Whether every referenced artifact path and hash matches the v60 context manifests.")
    provider_call_count: Literal[0] = Field(default=0, description="Provider calls made by this preflight; always zero.")
    billable_call_count: Literal[0] = Field(default=0, description="Billable calls made by this preflight; always zero.")
    reason: str = Field(min_length=1, description="Why exact input closure is checked before the internal release regression.")
    basis: str = Field(min_length=1, description="Archived context-manifest ArtifactRef paths and SHA-256 values compared directly to the supplied closure bytes.")


def _repository_root() -> Path:
    """Return the repository root owning the release-validation output."""

    return Path(subprocess.check_output(("git", "rev-parse", "--show-toplevel"), text=True).strip())


def _load(path: Path) -> dict[str, Any]:
    """Load exactly one JSON object from an immutable or newly written audit file."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _items(value: Any) -> list[dict[str, Any]]:
    """Normalize a JSON list or mapping to object rows without semantic inference."""

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [item for item in value.values() if isinstance(item, dict)]
    return []


def _sha256(path: Path) -> str:
    """Return a SHA-256 identity for one file without rewriting it."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_hash(value: Any) -> str:
    """Hash a JSON value using the frozen runner's canonical JSON projection."""

    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: BaseModel | dict[str, Any]) -> None:
    """Write deterministic UTF-8 JSON outside frozen experiment artifacts."""

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _relativize_repository_paths(value: Any, repository: Path) -> Any:
    """Replace only repository-owned absolute paths in derived reporting data."""

    if isinstance(value, dict):
        return {str(key): _relativize_repository_paths(item, repository) for key, item in value.items()}
    if isinstance(value, list):
        return [_relativize_repository_paths(item, repository) for item in value]
    if isinstance(value, tuple):
        return tuple(_relativize_repository_paths(item, repository) for item in value)
    if isinstance(value, str) and value.startswith(str(repository.resolve()) + "/"):
        return Path(value).resolve().relative_to(repository.resolve()).as_posix()
    return value


def _reference(repository: Path, path: Path, reason: str) -> ArtifactReference:
    """Create a repository-relative reference and refuse paths outside the repository."""

    resolved = path.resolve()
    try:
        relative = resolved.relative_to(repository.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"release-validation reference escapes repository: {path}") from error
    return ArtifactReference(
        path=relative,
        sha256=_sha256(resolved),
        reason=reason,
        basis="SHA-256 over exact UTF-8 artifact bytes and a repository-relative path; evaluator reads but never rewrites the source.",
    )


def _ratio(count: int, denominator: int) -> Ratio:
    """Construct a ratio that never hides its population denominator."""

    return Ratio(count=count, denominator=denominator, rate=(count / denominator if denominator else None))


def _ledger_levels(path: Path) -> dict[str, str]:
    """Read ledger L labels only in evaluator/reporting code."""

    return {
        str(issue_id): str(item.get("L"))
        for issue_id, item in _load(path).get("items", {}).items()
        if isinstance(item, dict) and item.get("L") is not None
    }


def _judge_paths(judge_root: Path, pairs: tuple[str, ...], rounds: tuple[int, ...]) -> dict[tuple[str, int], Path]:
    """Resolve selected Judge pair results, preferring archive-local composite storage."""

    summary = _load(judge_root / "summary.json")
    if str(summary.get("schema_version") or "").endswith("semantic-judge.composite-summary.v1"):
        receipts = {
            (str(item["pair_id"]), int(item["round"])): item
            for item in _items(summary.get("pair_receipts"))
        }
        resolved: dict[tuple[str, int], Path] = {}
        for pair_id in pairs:
            for round_no in rounds:
                receipt = receipts.get((pair_id, round_no))
                if receipt is None:
                    raise ValueError(f"composite has no selected receipt for {pair_id}:r{round_no}")
                raw_path = Path(str(receipt["result_path"])).expanduser()
                if not raw_path.is_file():
                    raw_path = judge_root.parent / "source_runs" / str(receipt["source_run_id"]) / "pairs" / f"{pair_id}.json"
                if not raw_path.is_file():
                    raise FileNotFoundError(raw_path)
                expected_hash = str(receipt.get("result_hash") or "")
                if expected_hash and _sha256(raw_path) != expected_hash:
                    raise ValueError(f"composite receipt hash mismatch: {raw_path}")
                resolved[(pair_id, round_no)] = raw_path.resolve()
        return resolved
    resolved = {}
    for pair_id in pairs:
        for round_no in rounds:
            path = judge_root / "pairs" / f"{pair_id}.json"
            if not path.is_file():
                raise FileNotFoundError(path)
            payload = _load(path)
            if str(payload.get("pair_id")) != pair_id or int(payload.get("round")) != round_no:
                raise ValueError(f"Judge pair/round identity mismatch: {path}")
            resolved[(pair_id, round_no)] = path.resolve()
    return resolved


def _method_cells(method_root: Path, pairs: tuple[str, ...], rounds: tuple[int, ...]) -> dict[tuple[str, int], tuple[Path, dict[str, Any]]]:
    """Load and identity-check every selected terminal method cell."""

    cells: dict[tuple[str, int], tuple[Path, dict[str, Any]]] = {}
    for pair_id in pairs:
        for round_no in rounds:
            path = method_root / "method" / pair_id / f"round-{round_no}.json"
            payload = _load(path)
            if str(payload.get("pair_id")) != pair_id or int(payload.get("round")) != round_no:
                raise ValueError(f"method pair/round identity mismatch: {path}")
            cells[(pair_id, round_no)] = (path.resolve(), payload)
    return cells


def _method_billing(cells: dict[tuple[str, int], tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    """Aggregate recorded method usage without estimating missing provider metadata."""

    logical = attempts = provider_retries = non_provider_retries = 0
    input_tokens = output_tokens = cache_read = cache_write = 0
    cost = 0.0
    eligible = True
    for _, payload in cells.values():
        for call in _items(payload.get("llm_calls")):
            logical += 1
            call_cost = call.get("cost") if isinstance(call.get("cost"), dict) else {}
            cost += float(call_cost.get("total_usd") or 0.0)
            eligible = eligible and bool(call_cost.get("eligible", False))
            for attempt in _items(call_cost.get("attempts")):
                attempts += 1
                categories = attempt.get("categories") if isinstance(attempt.get("categories"), dict) else {}
                for name, target in (("input", "input"), ("output", "output"), ("cache_read", "cache_read"), ("cache_write", "cache_write")):
                    category = categories.get(name) if isinstance(categories.get(name), dict) else {}
                    value = int(category.get("tokens") or 0)
                    if target == "input":
                        input_tokens += value
                    elif target == "output":
                        output_tokens += value
                    elif target == "cache_read":
                        cache_read += value
                    else:
                        cache_write += value
            for attempt in _items(call.get("attempts")):
                provider_retries += sum(bool(item.get("provider_error")) for item in _items(attempt.get("retry_records")))
                non_provider_retries += len(_items(attempt.get("schema_validation_failures")))
    return {
        "logical_call_count": logical,
        "attempt_count": attempts,
        "input_tokens_excluding_cache": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read,
        "cache_write_tokens": cache_write,
        "recorded_cost_usd": cost,
        "cost_eligible": eligible,
        "provider_retry_count": provider_retries,
        "schema_validation_failure_count": non_provider_retries,
        "reason": "Totals are sums of preserved method llm_calls cost/attempt receipts; missing usage is never priced by evaluator inference.",
        "basis": "method cell llm_calls[].cost and attempts[] receipts",
    }


def _judge_billing(paths: dict[tuple[str, int], Path]) -> dict[str, Any]:
    """Aggregate recorded Judge usage without using provider streams or estimates."""

    logical = attempts = provider_retries = non_provider_retries = 0
    input_tokens = output_tokens = cache_read = cache_write = 0
    cost = 0.0
    eligible = True
    for path in paths.values():
        for call in _items(_load(path).get("call_receipts")):
            logical += 1
            cost += float(call.get("cost_usd") or 0.0)
            eligible = eligible and bool(call.get("cost_eligible", False))
            retries = _items(call.get("retries"))
            attempts += len(retries) or 1
            provider_retries += sum(bool(item.get("provider_error")) for item in retries)
            non_provider_retries += sum(
                not bool(item.get("provider_error")) and int(item.get("attempt_no") or 1) > 1
                for item in retries
            )
            for usage in _items(call.get("usage")):
                input_tokens += int(usage.get("input_tokens") or 0)
                output_tokens += int(usage.get("output_tokens") or 0)
                cache_read += int(usage.get("cache_read_input_tokens") or 0)
                cache_write += int(usage.get("cache_write_input_tokens") or 0)
    return {
        "logical_call_count": logical,
        "attempt_count": attempts,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read,
        "cache_write_tokens": cache_write,
        "recorded_cost_usd": cost,
        "cost_eligible": eligible,
        "provider_retry_count": provider_retries,
        "non_provider_outer_retry_count": non_provider_retries,
        "reason": "Totals are sums of preserved Judge CallReceipt usage/retry rows; ineligible usage remains ineligible rather than estimated.",
        "basis": "selected Judge PairJudgeResult call_receipts[]",
    }


def _terminal_predicate_usage(cells: dict[tuple[str, int], tuple[Path, dict[str, Any]]], expected: list[dict[str, Any]]) -> dict[str, Any]:
    """Count only terminal deterministic predicate receipts and their FULL-hit links."""

    report_predicates: dict[str, str] = {}
    terminal: Counter[str] = Counter()
    verdicts: dict[str, Counter[str]] = defaultdict(Counter)
    errors: dict[str, Counter[str]] = defaultdict(Counter)
    for _, payload in cells.values():
        for report in _items(payload.get("report_issue_clusters")):
            report_id = report.get("issue_id")
            predicate_id = report.get("predicate_id")
            if isinstance(report_id, str) and isinstance(predicate_id, str):
                report_predicates[report_id] = predicate_id
        receipts = _items(payload.get("predicate_execution_receipts"))
        if not receipts:
            receipts = _items((payload.get("stage_outputs") or {}).get("execute_batch", {}).get("predicate_execution_receipts"))
        for receipt in receipts:
            predicate_id = receipt.get("predicate_id")
            if not isinstance(predicate_id, str):
                continue
            verdict = str(receipt.get("verdict") or receipt.get("predicate_verdict") or "unknown")
            is_terminal = (
                receipt.get("execution_status") == "executed"
                and receipt.get("terminal_state") == "completed"
                and verdict in {"pass", "violation"}
            )
            if is_terminal:
                terminal[predicate_id] += 1
                verdicts[predicate_id][verdict] += 1
            else:
                errors[predicate_id][str(receipt.get("failure_kind") or receipt.get("execution_status") or receipt.get("terminal_state") or verdict)] += 1
    contribution: Counter[str] = Counter()
    for row in expected:
        if not row["full"]:
            continue
        for report_id in row["full_report_ids"]:
            predicate_id = report_predicates.get(report_id)
            if predicate_id:
                contribution[predicate_id] += 1
    planned = ("S1", "S2", "S3", "S4", "S5", "S6", "G1", "G4", "R1", "R4", "V1", "V4")
    terminal_predicates = sorted(terminal)
    planned_terminal_predicates = [predicate_id for predicate_id in planned if predicate_id in terminal]
    return {
        "planned_predicates": list(planned),
        "planned_terminal_distinct_count": len(planned_terminal_predicates),
        "planned_terminal_predicates": planned_terminal_predicates,
        "planned_zero_use_predicates": [predicate_id for predicate_id in planned if predicate_id not in terminal],
        "terminal_distinct_count": len(terminal),
        "terminal_distinct_predicates": terminal_predicates,
        "terminal_nonplanned_predicates": [predicate_id for predicate_id in terminal_predicates if predicate_id not in planned],
        "terminal_receipt_counts": dict(sorted(terminal.items())),
        "true_false": {predicate_id: dict(sorted(counts.items())) for predicate_id, counts in sorted(verdicts.items())},
        "error_timeout_degradation": {predicate_id: dict(sorted(counts.items())) for predicate_id, counts in sorted(errors.items())},
        "full_hit_contribution": dict(sorted(contribution.items())),
        "reason": "Usage requires execution_status=executed, terminal_state=completed, and pass/violation; planned usage is counted only over the fixed 12-predicate scope, while nonplanned terminal receipts remain separately visible.",
        "basis": "method predicate_execution_receipts and Judge full_report_ids joined through original method issue IDs",
    }


def _planned_terminal_distinct_count(usage: dict[str, Any]) -> int:
    """Read planned terminal usage while supporting the first reference schema."""

    explicit = usage.get("planned_terminal_distinct_count")
    if isinstance(explicit, int):
        return explicit
    planned = {str(value) for value in usage.get("planned_predicates", ())}
    terminal = {str(value) for value in usage.get("terminal_distinct_predicates", ())}
    return len(planned.intersection(terminal))


def _stage_loss(
    method_root: Path,
    judge_root: Path,
    pairs: tuple[str, ...],
    rounds: tuple[int, ...],
) -> dict[str, Any]:
    """Build an evaluator stage-loss audit with the fixed diagnostic predicate denominator."""

    return build_stage_loss_audit(
        method_root=method_root,
        judge_root=judge_root,
        planned_predicate_scope="diagnostic-12",
        selected_pair_ids=pairs,
        selected_rounds=rounds,
    )


def _aggregate_run(
    *,
    method_root: Path,
    judge_root: Path,
    ledger: Path,
    pairs: tuple[str, ...],
    rounds: tuple[int, ...],
    stage_loss: dict[str, Any],
) -> RunMetrics:
    """Mechanically compute release-validation metrics from selected raw method/Judge bytes."""

    levels = _ledger_levels(ledger)
    cells = _method_cells(method_root, pairs, rounds)
    judge_paths = _judge_paths(judge_root, pairs, rounds)
    expected: list[dict[str, Any]] = []
    reports: list[dict[str, Any]] = []
    report_witness: dict[tuple[str, int, str], str] = {}
    d_levels: Counter[str] = Counter()
    for (pair_id, round_no), (_, cell) in cells.items():
        for report in _items(cell.get("report_issue_clusters")):
            report_id = report.get("issue_id")
            witness = report.get("witness_level")
            if isinstance(report_id, str) and witness in WITNESS_RANK:
                report_witness[(pair_id, round_no, report_id)] = str(witness)
        for evidence in _items(cell.get("evidence_records")):
            value = evidence.get("d_level")
            if value in {"D0", "D1", "D2", "D_UNRESOLVED"}:
                d_levels[str(value)] += 1
        judge = _load(judge_paths[(pair_id, round_no)])
        reports.extend({"pair_id": pair_id, "round": round_no, **row} for row in _items(judge.get("report_outcomes")))
        for row in _items(judge.get("expected_outcomes")):
            full_report_ids = tuple(str(value) for value in row.get("full_report_ids", ()) if value)
            partial_report_ids = tuple(str(value) for value in row.get("partial_report_ids", ()) if value)
            expected.append({
                "pair_id": pair_id,
                "round": round_no,
                "expected_id": str(row["ledger_id"]),
                "full": bool(row.get("hit")),
                "supported": bool(row.get("supported")),
                "full_report_ids": full_report_ids,
                "partial_report_ids": partial_report_ids,
            })
    by_expected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expected:
        by_expected[row["expected_id"]].append(row)
    if any(len(rows) != len(rounds) for rows in by_expected.values()):
        raise ValueError("selected expected issue rows do not close over every represented round")
    l2_ids = {issue_id for issue_id in by_expected if levels.get(issue_id) == "L2"}
    full_count = sum(row["full"] for row in expected)
    l2_rows = [row for row in expected if row["expected_id"] in l2_ids]
    report_counts = Counter(str(row.get("validity")) for row in reports)
    clusters: dict[str, set[str]] = defaultdict(set)
    for row in reports:
        clusters[f"{row['pair_id']}:r{row['round']}::{row.get('root_cause_cluster_key')}"] .add(str(row.get("validity")))
    known_clusters = sum("VALID_KNOWN" in values for values in clusters.values())
    novel_clusters = sum("VALID_KNOWN" not in values and "VALID_NOVEL" in values for values in clusters.values())
    invalid_clusters = sum(values == {"INVALID"} for values in clusters.values())
    full_witness: Counter[str] = Counter()
    w2_all = 0
    for row in expected:
        support_levels = [
            report_witness[(row["pair_id"], row["round"], report_id)]
            for report_id in (*row["full_report_ids"], *row["partial_report_ids"])
            if (row["pair_id"], row["round"], report_id) in report_witness
        ]
        if support_levels and max(support_levels, key=WITNESS_RANK.__getitem__) == "W2":
            w2_all += 1
        if row["full"]:
            full_levels = [
                report_witness.get((row["pair_id"], row["round"], report_id))
                for report_id in row["full_report_ids"]
            ]
            if not full_levels or any(level not in WITNESS_RANK for level in full_levels):
                raise ValueError(f"FULL expected row has no mapped audited witness: {row['pair_id']}:r{row['round']}:{row['expected_id']}")
            full_witness[max(full_levels, key=WITNESS_RANK.__getitem__)] += 1
    owner_counts = Counter(str(row.get("root_cause_owner")) for row in _items(stage_loss.get("rows")))
    per_round: list[dict[str, Any]] = []
    for round_no in rounds:
        round_rows = [row for row in expected if row["round"] == round_no]
        round_reports = [row for row in reports if row["round"] == round_no]
        round_l2 = [row for row in round_rows if row["expected_id"] in l2_ids]
        valid = sum(str(row.get("validity")) in {"VALID_KNOWN", "VALID_NOVEL"} for row in round_reports)
        per_round.append({
            "round": round_no,
            "overall_full": _ratio(sum(row["full"] for row in round_rows), len(round_rows)).model_dump(mode="json"),
            "l2_full": _ratio(sum(row["full"] for row in round_l2), len(round_l2)).model_dump(mode="json"),
            "semantic_precision": _ratio(valid, len(round_reports)).model_dump(mode="json"),
            "report_validity": {key: sum(str(row.get("validity")) == key for row in round_reports) for key in VALIDITIES},
        })
    hit_at_3 = hit_at_all = None
    if len(rounds) == 3:
        hit_at_3 = _ratio(sum(any(row["full"] for row in rows) for rows in by_expected.values()), len(by_expected))
        hit_at_all = _ratio(sum(all(row["full"] for row in rows) for rows in by_expected.values()), len(by_expected))
    valid_reports = report_counts["VALID_KNOWN"] + report_counts["VALID_NOVEL"]
    return RunMetrics(
        pair_ids=pairs,
        rounds=rounds,
        method_terminal_cells=_ratio(sum(cell[1].get("status") == "completed" for cell in cells.values()), len(pairs) * len(rounds)),
        expected_rows=len(expected),
        expected_issues=len(by_expected),
        overall_full=_ratio(full_count, len(expected)),
        l2_full=_ratio(sum(row["full"] for row in l2_rows), len(l2_rows)),
        hit_at_3=hit_at_3,
        hit_at_all=hit_at_all,
        semantic_precision=_ratio(valid_reports, len(reports)),
        root_cause_cluster_precision=_ratio(known_clusters + novel_clusters, len(clusters)),
        report_validity={key: report_counts[key] for key in VALIDITIES},
        cluster_validity={"VALID_KNOWN": known_clusters, "VALID_NOVEL": novel_clusters, "VALID": known_clusters + novel_clusters, "INVALID": invalid_clusters},
        full_hit_max_witness={level: _ratio(full_witness[level], full_count) for level in ("W2", "W1", "W0")},
        w2_all_expected=_ratio(w2_all, len(expected)),
        predicate_usage=_terminal_predicate_usage(cells, expected),
        d_levels={level: d_levels[level] for level in ("D2", "D1", "D0", "D_UNRESOLVED")},
        stage_loss=dict(sorted(owner_counts.items())),
        method_billing=_method_billing(cells),
        judge_billing=_judge_billing(judge_paths),
        per_round=per_round,
        reason="FULL hits, W-on-hits, W2/all-expected, K/N/I, predicate receipts, D, stage loss, and billing retain their own denominators and raw audit paths.",
        basis="selected method round JSON, composite-selected or standalone Judge PairJudgeResult JSON, frozen ledger L labels, and provider-free stage-loss evaluation",
    )


def _write_reference_markdown(path: Path, reference: V60ReferenceArtifact) -> None:
    """Write a concise Chinese reference note whose numbers come from reference JSON."""

    metrics = reference.metrics
    hit_at_3 = (
        f"{metrics.hit_at_3.count}/{metrics.hit_at_3.denominator} ({metrics.hit_at_3.rate:.2%})"
        if metrics.hit_at_3 is not None and metrics.hit_at_3.rate is not None
        else "不适用"
    )
    hit_at_all = (
        f"{metrics.hit_at_all.count}/{metrics.hit_at_all.denominator} ({metrics.hit_at_all.rate:.2%})"
        if metrics.hit_at_all is not None and metrics.hit_at_all.rate is not None
        else "不适用"
    )
    lines = [
        "# v60 固定 15-pair 三轮对照",
        "",
        "本文件由 `v60_15pair_reference.json` 机械生成；所有 raw 引用都位于永久 `final_results` 归档。",
        "",
        "| 指标 | 三轮合并 |",
        "| --- | ---: |",
        f"| overall FULL | {metrics.overall_full.count}/{metrics.overall_full.denominator} ({metrics.overall_full.rate:.2%}) |",
        f"| L2 FULL | {metrics.l2_full.count}/{metrics.l2_full.denominator} ({metrics.l2_full.rate:.2%}) |",
        f"| hit@3 | {hit_at_3} |",
        f"| hit@all | {hit_at_all} |",
        f"| semantic precision | {metrics.semantic_precision.count}/{metrics.semantic_precision.denominator} ({metrics.semantic_precision.rate:.2%}) |",
        f"| FULL-hit max-W2/W1/W0 | {metrics.full_hit_max_witness['W2'].count}/{metrics.full_hit_max_witness['W1'].count}/{metrics.full_hit_max_witness['W0'].count}，分母 {metrics.overall_full.count} |",
        f"| planned terminal predicate usage | {_planned_terminal_distinct_count(metrics.predicate_usage)}/12 |",
        "",
        "新 15x1 只报告 hit@1；`hit@3` 与 `hit@all` 只在本三轮 v60 参考中计算，不能用一轮结果替代。",
        "",
        "| round | overall FULL | L2 FULL | semantic precision |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in metrics.per_round:
        overall = row["overall_full"]
        l2 = row["l2_full"]
        precision = row["semantic_precision"]
        lines.append(f"| {row['round']} | {overall['count']}/{overall['denominator']} ({overall['rate']:.2%}) | {l2['count']}/{l2['denominator']} ({l2['rate']:.2%}) | {precision['count']}/{precision['denominator']} ({precision['rate']:.2%}) |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_reference(args: argparse.Namespace) -> int:
    """Extract and persist the fixed v60 15-pair x 3-round reference without provider access."""

    repository = _repository_root()
    archive = Path(args.archive_root).resolve()
    output = Path(args.output_root).resolve()
    method_root = archive / "raw" / "v60_current" / "method"
    judge_root = archive / "raw" / "v60_current" / "judge" / "composite"
    ledger = archive / "reference" / "ledger.json"
    method_manifest_path = method_root / "run_manifest.json"
    composite_path = judge_root / "summary.json"
    manifest = _load(method_manifest_path)
    composite = _load(composite_path)
    rounds = (1, 2, 3)
    stage_loss = _relativize_repository_paths(_stage_loss(method_root, judge_root, FIXED_PAIR_IDS, rounds), repository)
    stage_loss_path = output / "derived" / "v60_15pair_stage_loss.json"
    _write_json(stage_loss_path, stage_loss)
    metrics = _aggregate_run(method_root=method_root, judge_root=judge_root, ledger=ledger, pairs=FIXED_PAIR_IDS, rounds=rounds, stage_loss=stage_loss)
    receipt_index = {(str(item["pair_id"]), int(item["round"])): item for item in _items(composite.get("pair_receipts"))}
    cells: list[FixedCellReference] = []
    for pair_id in FIXED_PAIR_IDS:
        for round_no in rounds:
            method_path = method_root / "method" / pair_id / f"round-{round_no}.json"
            receipt = receipt_index[(pair_id, round_no)]
            judge_path = _judge_paths(judge_root, (pair_id,), (round_no,))[(pair_id, round_no)]
            judge_payload = _load(judge_path)
            cells.append(FixedCellReference(
                pair_id=pair_id,
                round=round_no,
                method=_reference(repository, method_path, "Immutable v60 method cell selected by the pre-registered 15-pair release-validation set."),
                judge=_reference(repository, judge_path, "Composite-selected immutable v60 Semantic Judge result for the same pair and round."),
                judge_source_run_id=str(receipt["source_run_id"]),
                expected_count=len(_items(judge_payload.get("expected_outcomes"))),
                report_count=len(_items(judge_payload.get("report_outcomes"))),
                reason="One v60 method cell is paired to the exact Judge result chosen by the frozen composite.",
                basis="composite summary pair_receipts source_run_id/result_hash and archive-local source_runs fallback",
            ))
    source_manifests = [
        _load(judge_root.parent / "source_runs" / str(item["run_id"]) / "run_manifest.json")
        for item in _items(composite.get("source_runs"))
        if (judge_root.parent / "source_runs" / str(item["run_id"]) / "run_manifest.json").is_file()
    ]
    if not source_manifests:
        raise ValueError("archived composite has no readable Judge source-run manifests")
    reference = V60ReferenceArtifact(
        fixed_pair_ids=FIXED_PAIR_IDS,
        internal_rc_commit=args.internal_rc_commit,
        v60_method_commit=str(manifest["source_provenance"]["source_commit"]),
        v60_judge_commit=str(composite["semantic_judge_commit"]),
        method_manifest=_reference(repository, method_manifest_path, "Immutable v60 method configuration and pair input hashes."),
        judge_composite=_reference(repository, composite_path, "Immutable v60 composite selection and protocol record."),
        ledger=_reference(repository, ledger, "Frozen expected-issue ledger used only by evaluator aggregation."),
        method_configuration={key: manifest.get(key) for key in ("profile", "workers", "transport_retries", "streaming", "retry_policy", "registry_hash", "prompt_schema_hash", "input_data_hash", "run_contract_hash", "pair_input_hashes")},
        judge_configuration={
            "model_profile": composite.get("model_profile"),
            "protocol_version": composite.get("protocol_version"),
            "protocol_sha256": composite.get("protocol_sha256"),
            "judge_algorithm_version": composite.get("judge_algorithm_version"),
            "max_reports_per_batch": sorted({item.get("max_reports_per_batch") for item in source_manifests}),
            "workers": sorted({item.get("workers") for item in source_manifests}),
            "transport_retries": sorted({item.get("transport_retries") for item in source_manifests}),
        },
        cells=tuple(cells),
        metrics=metrics,
        stage_loss_audit=_reference(repository, stage_loss_path, "Provider-free stage-loss derivation for the v60 15-pair reference; it is outside final_results."),
        reason="The fixed 15-pair reference retains all three v60 rounds and composite-selected raw artifacts before the single new 15x1 run.",
        basis="permanent v60 final-results archive, SHA-256-closed composite pair receipts, exact selected pair order, and provider-free evaluator aggregation",
    )
    json_path = output / "v60_15pair_reference.json"
    _write_json(json_path, reference)
    _write_reference_markdown(output / "v60_15pair_reference_cn.md", reference)
    print(json.dumps({"reference": str(json_path), "cell_count": len(cells), "provider_call_count": 0, "billable_call_count": 0}, ensure_ascii=False))
    return 0


def prepare_manifest(args: argparse.Namespace) -> int:
    """Write the pre-provider internal RC contract from existing release/reference manifests."""

    repository = _repository_root()
    output = Path(args.output).resolve()
    reference_path = Path(args.reference).resolve()
    reference = V60ReferenceArtifact.model_validate_json(reference_path.read_text(encoding="utf-8"))
    method_release = Path(args.method_release_manifest).resolve()
    judge_release = Path(args.judge_release_manifest).resolve()
    for release_manifest in (method_release, judge_release):
        value = _load(release_manifest)
        if value.get("source_commit") != args.internal_rc_commit:
            raise ValueError(f"release manifest was not built from internal RC: {release_manifest}")
        if int(value.get("provider_call_count", -1)) != 0 or int(value.get("billable_call_count", -1)) != 0:
            raise ValueError(f"release manifest has nonzero provider/billable build count: {release_manifest}")
    input_root = Path(args.input_closure_root).resolve()
    try:
        input_relative = input_root.relative_to(repository).as_posix()
    except ValueError as error:
        raise ValueError("input closure root must be under the repository for stable technical provenance") from error
    manifest = InternalValidationManifest(
        internal_rc_tag=args.internal_rc_tag,
        internal_rc_commit=args.internal_rc_commit,
        method_release_manifest=_reference(repository, method_release, "RC method release manifest copied before the one authorized live execution."),
        judge_release_manifest=_reference(repository, judge_release, "RC Judge release manifest copied before the one authorized live execution."),
        v60_reference=_reference(repository, reference_path, "Fixed v60 15-pair three-round raw reference selected before live execution."),
        method_run_id=args.method_run_id,
        judge_run_id=args.judge_run_id,
        fixed_pair_ids=FIXED_PAIR_IDS,
        input_closure_root=input_relative,
        method_configuration={
            **reference.method_configuration,
            "rounds": 1,
            "selected_pair_ids": list(FIXED_PAIR_IDS),
            "source_commit_expected": args.internal_rc_commit,
        },
        judge_configuration={
            **reference.judge_configuration,
            "round": 1,
            "selected_pair_ids": list(FIXED_PAIR_IDS),
            "source_commit_expected": args.internal_rc_commit,
        },
        provider_authorization={"method_runs": 1, "judge_runs": 1, "full_54x3_runs": 0, "additional_smoke_runs": 0},
        reason="The manifest freezes the sole authorized internal 15-pair x 1 method execution and one subsequent issue #195 Judge pass; it is not an external public release or a new result-optimization loop.",
        basis="internal RC tag, independently built package release manifests, permanent v60 reference, and mechanical v60 configuration extraction",
    )
    _write_json(output, manifest)
    print(json.dumps({"manifest": str(output), "provider_call_count": 0, "billable_call_count": 0}, ensure_ascii=False))
    return 0


def validate_input_closure(args: argparse.Namespace) -> int:
    """Verify archived v60 context-manifest paths and hashes without loading or writing method inputs."""

    repository = _repository_root()
    reference_path = Path(args.reference).resolve()
    reference = V60ReferenceArtifact.model_validate_json(reference_path.read_text(encoding="utf-8"))
    input_root = Path(args.input_closure_root).resolve()
    try:
        input_relative = input_root.relative_to(repository).as_posix()
    except ValueError as error:
        raise ValueError("input closure root must remain under the repository") from error
    mismatches: list[str] = []
    checked_artifacts = 0
    pair_hashes: dict[str, dict[str, str]] = {}
    for cell in reference.cells:
        method_path = repository / cell.method.path
        context = _load(method_path).get("context_manifest")
        if not isinstance(context, dict):
            mismatches.append(f"{cell.pair_id}:r{cell.round}:missing context_manifest")
            continue
        manifest_hash = str(context.get("manifest_hash") or "")
        existing = pair_hashes.setdefault(cell.pair_id, {"expected": manifest_hash, "rounds": ""})
        if existing["expected"] != manifest_hash:
            mismatches.append(f"{cell.pair_id}:context manifest differs across v60 rounds")
        existing["rounds"] = ",".join(filter(None, (existing["rounds"], str(cell.round))))
        for artifact in _items(context.get("artifacts")):
            path_text = artifact.get("path")
            expected_hash = artifact.get("sha256")
            if not isinstance(path_text, str) or not isinstance(expected_hash, str):
                mismatches.append(f"{cell.pair_id}:r{cell.round}:malformed ArtifactRef")
                continue
            actual_path = Path(path_text)
            if not actual_path.is_file():
                mismatches.append(f"{cell.pair_id}:r{cell.round}:missing {actual_path}")
                continue
            checked_artifacts += 1
            actual_hash = _sha256(actual_path)
            if actual_hash != expected_hash:
                mismatches.append(f"{cell.pair_id}:r{cell.round}:hash {actual_path}: expected={expected_hash} actual={actual_hash}")
    preflight = InputClosurePreflight(
        reference=_reference(repository, reference_path, "Fixed v60 reference supplying all expected context-manifest input paths and hashes."),
        input_closure_root=input_relative,
        checked_cells=len(reference.cells),
        checked_artifacts=checked_artifacts,
        pair_manifest_hashes=pair_hashes,
        mismatches=tuple(mismatches),
        passed=not mismatches,
        reason="The installed RC method is permitted to run only after every archived v60 input closure artifact for the fixed set remains byte-identical at its recorded absolute provenance path.",
        basis="method cell context_manifest.artifacts[] path/SHA-256 values and direct read-only SHA-256 of the current frozen input closure",
    )
    _write_json(Path(args.output).resolve(), preflight)
    print(json.dumps({"preflight": str(Path(args.output).resolve()), "passed": preflight.passed, "mismatch_count": len(mismatches), "provider_call_count": 0, "billable_call_count": 0}, ensure_ascii=False))
    return 0 if preflight.passed else 2


def _carrier_inventory(method_root: Path, pairs: tuple[str, ...], rounds: tuple[int, ...]) -> dict[str, set[str]]:
    """Map exact typed terminal carrier keys to verdict sets without prose matching."""

    inventory: dict[str, set[str]] = defaultdict(set)
    for (pair_id, _), (_, payload) in _method_cells(method_root, pairs, rounds).items():
        receipts = _items(payload.get("predicate_execution_receipts"))
        if not receipts:
            receipts = _items((payload.get("stage_outputs") or {}).get("execute_batch", {}).get("predicate_execution_receipts"))
        for receipt in receipts:
            if receipt.get("execution_status") != "executed" or receipt.get("terminal_state") != "completed":
                continue
            verdict = str(receipt.get("verdict") or "")
            if verdict not in {"pass", "violation"}:
                continue
            typed_inputs = receipt.get("typed_inputs") if isinstance(receipt.get("typed_inputs"), dict) else {}
            key = json.dumps({
                "pair_id": pair_id,
                "predicate_id": receipt.get("predicate_id"),
                "typed_inputs": typed_inputs,
                "typed_inputs_hash": receipt.get("typed_inputs_hash"),
            }, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            inventory[key].add(verdict)
    return inventory


def _round_vector(reference: RunMetrics, field: str) -> list[float]:
    """Read one per-round rate vector from a v60 reference metric field."""

    return [float(row[field]["rate"]) for row in reference.per_round if row[field]["rate"] is not None]


def _soft_metric(new: Ratio, values: list[float], decrement: float) -> dict[str, Any]:
    """Evaluate one stochastic metric against v60 envelope and permitted mean decrease."""

    mean = fmean(values)
    return {
        "new": new.model_dump(mode="json"),
        "v60_min": min(values),
        "v60_max": max(values),
        "v60_mean": mean,
        "within_v60_round_envelope": min(values) <= (new.rate or 0.0) <= max(values),
        "mean_degradation": mean - (new.rate or 0.0),
        "soft_degradation_limit": decrement,
        "within_soft_limit": mean - (new.rate or 0.0) <= decrement,
    }


def _ratio_text(value: Ratio | dict[str, Any] | None) -> str:
    """Render one ratio without concealing the denominator."""

    if value is None:
        return "不适用"
    row = value.model_dump(mode="json") if isinstance(value, Ratio) else value
    rate = row.get("rate")
    return f"{row.get('count')}/{row.get('denominator')}" + (
        f" ({float(rate):.2%})" if rate is not None else ""
    )


def _write_comparison_markdown(
    path: Path,
    comparison: ReleaseComparisonArtifact,
    reference: V60ReferenceArtifact,
) -> None:
    """Write a complete Chinese comparison tied to machine-readable audits."""

    metrics = comparison.release_metrics
    previous = reference.metrics
    lines = [
        "# internal RC 固定 15-pair x 1 回归对照",
        "",
        "本对照只用于发布结构迁移的技术回归，不构成新的论文主实验。v60 三轮是历史参考；新 run 是一次独立 LLM/Judge 采样，不能把全部观察差异严格归因于结构整理。",
        "",
        "固定 pair 为 `0001, 0002, 0004, 0010, 0012, 0013, 0023, 0024, 0029, 0035, 0046, 0049, 0053, 0054, 0056`。v60 参考含 45 个 method/Judge cells、180 个 round-level expected rows 和 60 个跨轮 expected issues；新 RC 含 15 个 cells、60 个 expected rows。原始对应关系、SHA-256、report ID 和 ledger ID 见 `v60_15pair_reference.json` 的 `cells`、`release_15x1_comparison.json` 及 `raw/`。",
        "",
        "## 主指标",
        "",
        "| 指标 | v60 R1 | v60 R2 | v60 R3 | v60 三轮合并 | internal RC 15x1 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for field, label in (("overall_full", "overall FULL / hit@1"), ("l2_full", "L2 FULL / hit@1"), ("semantic_precision", "semantic precision")):
        values = " | ".join(_ratio_text(row[field]) for row in previous.per_round)
        lines.append(f"| {label} | {values} | {_ratio_text(getattr(previous, field))} | {_ratio_text(getattr(metrics, field))} |")
    lines.extend([
        f"| hit@3（60 个跨轮 expected issues） | 不适用 | 不适用 | 不适用 | {_ratio_text(previous.hit_at_3)} | 不适用 |",
        f"| hit@all（60 个跨轮 expected issues） | 不适用 | 不适用 | 不适用 | {_ratio_text(previous.hit_at_all)} | 不适用 |",
        "",
        "`hit@3` 与 `hit@all` 的样本单位是跨三轮 expected issue，不能用新 15x1 的单轮数据替代。",
        "",
        "## W、K/N/I、D 与阶段损失",
        "",
        "| 指标 | v60 三轮合并 | internal RC 15x1 |",
        "| --- | ---: | ---: |",
    ])
    for level in ("W2", "W1", "W0"):
        lines.append(f"| FULL-hit max-{level} | {_ratio_text(previous.full_hit_max_witness[level])} | {_ratio_text(metrics.full_hit_max_witness[level])} |")
    lines.append(f"| W2 / 全部 expected | {_ratio_text(previous.w2_all_expected)} | {_ratio_text(metrics.w2_all_expected)} |")
    for validity in VALIDITIES:
        lines.append(f"| report-level {validity} | {previous.report_validity.get(validity, 0)} | {metrics.report_validity.get(validity, 0)} |")
    for validity in ("VALID_KNOWN", "VALID_NOVEL", "INVALID", "VALID"):
        lines.append(f"| root-cause cluster {validity} | {previous.cluster_validity.get(validity, 0)} | {metrics.cluster_validity.get(validity, 0)} |")
    lines.append(f"| root-cause cluster precision | {_ratio_text(previous.root_cause_cluster_precision)} | {_ratio_text(metrics.root_cause_cluster_precision)} |")
    for level in ("D2", "D1", "D0", "D_UNRESOLVED"):
        lines.append(f"| {level} evidence records | {previous.d_levels.get(level, 0)} | {metrics.d_levels.get(level, 0)} |")
    for owner in sorted(set(previous.stage_loss) | set(metrics.stage_loss)):
        lines.append(f"| stage-loss: {owner} | {previous.stage_loss.get(owner, 0)} | {metrics.stage_loss.get(owner, 0)} |")
    lines.extend([
        "",
        "FULL-hit max-W 只从 `expected_outcomes[].full_report_ids` 的 supporting reports 取最高等级；`partial_report_ids` 不会抬高 FULL hit。W2/全部 expected 的分母为 round-level expected rows，因此与 W-on-hits 分母不同。K/N/I 与 hit、W、D 均为正交审计轴。",
        "",
        "## Predicate usage",
        "",
        "计划分母固定为 12：`S1,S2,S3,S4,S5,S6,G1,G4,R1,R4,V1,V4`。终态 receipt 可出现计划外 predicate，但不以观察到的集合缩小计划分母。",
        "",
        "| planned predicate | v60 terminal receipts | RC terminal receipts | RC pass/violation | RC FULL-hit contribution | RC error/timeout/degradation |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ])
    for predicate_id in metrics.predicate_usage["planned_predicates"]:
        verdicts = metrics.predicate_usage["true_false"].get(predicate_id, {})
        failures = metrics.predicate_usage["error_timeout_degradation"].get(predicate_id, {})
        lines.append(
            f"| {predicate_id} | {previous.predicate_usage['terminal_receipt_counts'].get(predicate_id, 0)} | "
            f"{metrics.predicate_usage['terminal_receipt_counts'].get(predicate_id, 0)} | "
            f"pass={verdicts.get('pass', 0)}, violation={verdicts.get('violation', 0)} | "
            f"{metrics.predicate_usage['full_hit_contribution'].get(predicate_id, 0)} | "
            f"{json.dumps(failures, ensure_ascii=False, sort_keys=True) if failures else '-'} |"
        )
    lines.extend([
        "",
        f"planned terminal predicate usage：v60 {_planned_terminal_distinct_count(previous.predicate_usage)}/12；RC {_planned_terminal_distinct_count(metrics.predicate_usage)}/12。全部终态谓词集合分别为 {previous.predicate_usage['terminal_distinct_count']} 与 {metrics.predicate_usage['terminal_distinct_count']}；RC 的非计划终态谓词为 `{','.join(metrics.predicate_usage['terminal_nonplanned_predicates']) or '-'}`。",
        "",
        "## 调用、token 与成本",
        "",
        "| 项目 | v60 三轮合并 | internal RC 15x1 |",
        "| --- | ---: | ---: |",
    ])
    for side, before, after in (("method", previous.method_billing, metrics.method_billing), ("Judge", previous.judge_billing, metrics.judge_billing)):
        for label, key in (("logical calls", "logical_call_count"), ("attempts", "attempt_count"), ("input tokens", "input_tokens"), ("input tokens excluding cache", "input_tokens_excluding_cache"), ("output tokens", "output_tokens"), ("cache read tokens", "cache_read_tokens"), ("cache write tokens", "cache_write_tokens"), ("provider retries", "provider_retry_count"), ("recorded cost USD", "recorded_cost_usd"), ("cost eligible", "cost_eligible")):
            lines.append(f"| {side} {label} | {before.get(key, '-')} | {after.get(key, '-')} |")
    lines.extend([
        "",
        "## 确定性与采样审计",
        "",
        "| 确定性检查 | 结果 |",
        "| --- | --- |",
    ])
    for name, row in sorted(comparison.deterministic_invariants.items()):
        lines.append(f"| {name} | {'通过' if row.get('passed') else '失败'} |")
    carrier = comparison.matched_carriers
    lines.extend([
        "",
        f"精确 typed carrier 交集为 {carrier['matched_input_carrier_count']}；same-input terminal verdict flips 为 {carrier['matched_input_verdict_flip_count']}；v60-only/new-only 分别为 {carrier['before_only_carrier_count']}/{carrier['after_only_carrier_count']}。one-sided carrier 仅表示独立采样的 candidate/route surface 差异，不能解释为 backend 对相同输入改变真值。",
        "",
        "| 随机指标 | RC 15x1 | v60 min | v60 max | v60 mean | 包络内 | 软带内 |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ])
    for name in ("overall_full", "l2_full", "semantic_precision", "max_w2_on_hits"):
        row = comparison.stochastic_comparison[name]
        lines.append(f"| {name} | {float(row['new']['rate']):.2%} | {float(row['v60_min']):.2%} | {float(row['v60_max']):.2%} | {float(row['v60_mean']):.2%} | {'是' if row['within_v60_round_envelope'] else '否'} | {'是' if row['within_soft_limit'] else '否'} |")
    lines.extend([
        "",
        f"结论：{comparison.conclusion}",
        "",
        "该目录位于 `release_validation/`，不属于冻结 `final_results`，且被 method release allowlist 排除。",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def compare(args: argparse.Namespace) -> int:
    """Compare the one authorized release run to the persisted v60 three-round reference offline."""

    repository = _repository_root()
    reference_path = Path(args.reference).resolve()
    reference = V60ReferenceArtifact.model_validate_json(reference_path.read_text(encoding="utf-8"))
    method_root = Path(args.method_root).resolve()
    judge_root = Path(args.judge_root).resolve()
    ledger = Path(args.ledger).resolve()
    output = Path(args.output_root).resolve()
    manifest = _load(method_root / "run_manifest.json")
    pairs = tuple(str(value) for value in manifest.get("selected_pair_ids", ()))
    rounds = tuple(range(1, int(manifest.get("rounds") or 1) + 1))
    if pairs != FIXED_PAIR_IDS or rounds != (1,):
        raise ValueError("release comparison only accepts the one pre-registered fixed 15-pair x 1 method run")
    stage_loss = _relativize_repository_paths(_stage_loss(method_root, judge_root, pairs, rounds), repository)
    stage_loss_path = output / "derived" / "release_15x1_stage_loss.json"
    _write_json(stage_loss_path, stage_loss)
    metrics = _aggregate_run(method_root=method_root, judge_root=judge_root, ledger=ledger, pairs=pairs, rounds=rounds, stage_loss=stage_loss)
    reference_method_config = reference.method_configuration
    judge_manifest = _load(judge_root / "run_manifest.json")
    checks: dict[str, dict[str, Any]] = {
        "method_terminal_cells": {"passed": metrics.method_terminal_cells.count == 15 and metrics.method_terminal_cells.denominator == 15, "actual": metrics.method_terminal_cells.model_dump(mode="json"), "basis": "new method summary/cell closure"},
        "registry_hash": {"passed": manifest.get("registry_hash") == reference_method_config.get("registry_hash"), "before": reference_method_config.get("registry_hash"), "after": manifest.get("registry_hash"), "basis": "v60 and release method run manifests"},
        "prompt_schema_hash": {"passed": manifest.get("prompt_schema_hash") == reference_method_config.get("prompt_schema_hash"), "before": reference_method_config.get("prompt_schema_hash"), "after": manifest.get("prompt_schema_hash"), "basis": "v60 and release method run manifests"},
        "profile": {"passed": manifest.get("profile") == reference_method_config.get("profile"), "before": reference_method_config.get("profile"), "after": manifest.get("profile"), "basis": "v60 and release method run manifests"},
        "streaming": {"passed": manifest.get("streaming") == reference_method_config.get("streaming"), "before": reference_method_config.get("streaming"), "after": manifest.get("streaming"), "basis": "v60 and release method run manifests"},
        "transport_retries": {"passed": manifest.get("transport_retries") == reference_method_config.get("transport_retries"), "before": reference_method_config.get("transport_retries"), "after": manifest.get("transport_retries"), "basis": "v60 and release method run manifests"},
        "judge_protocol_sha256": {"passed": judge_manifest.get("protocol_sha256") == reference.judge_configuration.get("protocol_sha256"), "before": reference.judge_configuration.get("protocol_sha256"), "after": judge_manifest.get("protocol_sha256"), "basis": "v60 reference and new Judge run manifests"},
    }
    v60_hashes = reference_method_config.get("pair_input_hashes") or {}
    release_hashes = manifest.get("pair_input_hashes") or {}
    subset_v60_hashes = {pair: v60_hashes.get(pair) for pair in FIXED_PAIR_IDS}
    checks["pair_input_closure_hashes"] = {"passed": all(release_hashes.get(pair) == v60_hashes.get(pair) for pair in FIXED_PAIR_IDS), "before": subset_v60_hashes, "after": {pair: release_hashes.get(pair) for pair in FIXED_PAIR_IDS}, "basis": "pair context-manifest hashes from v60 and release method manifests"}
    expected_subset_input_data_hash = _canonical_hash({"pair_input_hashes": subset_v60_hashes})
    checks["scoped_input_data_hash"] = {
        "passed": manifest.get("input_data_hash") == expected_subset_input_data_hash,
        "historical_full_run_hash": reference_method_config.get("input_data_hash"),
        "expected_15pair_subset_hash": expected_subset_input_data_hash,
        "after": manifest.get("input_data_hash"),
        "basis": "The historical full run hashes all 54 pairs, while the RC hashes exactly the fixed 15-pair mapping; pair-level equality is the experimental input invariant.",
    }
    checks["scoped_run_contract_identity"] = {
        "passed": (
            manifest.get("source_provenance", {}).get("source_commit") == reference.internal_rc_commit
            and manifest.get("scope") == "diagnostic_subset"
            and manifest.get("rounds") == 1
            and isinstance(manifest.get("run_contract_hash"), str)
            and manifest.get("run_contract_hash", "").startswith("sha256:")
        ),
        "historical_full_run_contract_hash": reference_method_config.get("run_contract_hash"),
        "after": manifest.get("run_contract_hash"),
        "basis": "run_contract_hash intentionally includes source provenance, pair set, rounds, and scope; the RC is validated as the frozen 15-pair/1-round contract rather than falsely equated to v60's 54-pair/3-round contract.",
    }
    archive_method_root = reference_path.parents[0].parents[0] / "final_results" / "v60_current_vs_x1v2_baseline" / "raw" / "v60_current" / "method"
    if not archive_method_root.is_dir():
        archive_method_root = repository / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method"
    before_carriers = _carrier_inventory(archive_method_root, FIXED_PAIR_IDS, (1, 2, 3))
    after_carriers = _carrier_inventory(method_root, FIXED_PAIR_IDS, (1,))
    matched = set(before_carriers).intersection(after_carriers)
    flips = sorted(key for key in matched if before_carriers[key] != after_carriers[key])
    checks["matched_typed_carrier_verdicts"] = {"passed": not flips, "matched_input_carrier_count": len(matched), "matched_input_verdict_flip_count": len(flips), "basis": "exact predicate_id + typed_inputs + typed_inputs_hash carrier keys and terminal pass/violation verdict sets"}
    full_mean_denominator = reference.metrics.overall_full.denominator // 3
    stochastic = {
        "overall_full": _soft_metric(metrics.overall_full, _round_vector(reference.metrics, "overall_full"), 3 / full_mean_denominator),
        "l2_full": _soft_metric(metrics.l2_full, _round_vector(reference.metrics, "l2_full"), 2 / (reference.metrics.l2_full.denominator // 3)),
        "semantic_precision": _soft_metric(metrics.semantic_precision, _round_vector(reference.metrics, "semantic_precision"), 0.05),
        "max_w2_on_hits": _soft_metric(metrics.full_hit_max_witness["W2"], [reference.metrics.full_hit_max_witness["W2"].rate or 0.0], 0.10),
        "predicate_usage": {
            "new_planned_distinct": _planned_terminal_distinct_count(metrics.predicate_usage),
            "required_minimum": 10,
            "v60_minimum_planned_distinct": _planned_terminal_distinct_count(reference.metrics.predicate_usage),
            "passed": (
                _planned_terminal_distinct_count(metrics.predicate_usage) >= 10
                and _planned_terminal_distinct_count(metrics.predicate_usage)
                >= _planned_terminal_distinct_count(reference.metrics.predicate_usage) - 2
            ),
            "reason": "The 10/12 soft band applies only to the fixed planned predicate set; extra terminal predicates remain reported but cannot inflate this denominator.",
        },
    }
    all_deterministic = all(bool(row.get("passed")) for row in checks.values())
    soft_pass = all(row.get("within_v60_round_envelope") or row.get("within_soft_limit") for name, row in stochastic.items() if name != "predicate_usage") and bool(stochastic["predicate_usage"]["passed"])
    conclusion = (
        "未发现结构性语义变化；确定性不变量与 matched same-input carrier 均通过，随机指标处于 v60 轮间包络或预注册软容差内，因此没有要求重跑 54x3/162-cell 的结构性证据。"
        if all_deterministic and soft_pass
        else "存在需要独立审查的确定性不变量失败或超出软回归带的结果；不得将其解释为随机抖动。"
    )
    comparison = ReleaseComparisonArtifact(
        reference=_reference(repository, reference_path, "Persisted v60 three-round fixed-15 reference used for the release regression."),
        release_method_manifest=_reference(repository, method_root / "run_manifest.json", "One authorized installed-release method run manifest."),
        release_judge_manifest=_reference(repository, judge_root / "run_manifest.json", "One authorized installed-release Judge run manifest."),
        release_metrics=metrics,
        deterministic_invariants=checks,
        matched_carriers={
            "matched_input_carrier_count": len(matched),
            "matched_input_verdict_flip_count": len(flips),
            "matched_input_verdict_flips": flips,
            "before_only_carrier_count": len(set(before_carriers) - set(after_carriers)),
            "after_only_carrier_count": len(set(after_carriers) - set(before_carriers)),
            "reason": "One-sided carriers are independent LLM candidate/route/report surfaces and are excluded from same-input backend-verdict claims.",
            "basis": "carrier intersection requires exact typed inputs and terminal pass/violation receipts; v60 spans three independent rounds while release has one round",
        },
        stochastic_comparison=stochastic,
        conclusion=conclusion,
        reason="This is a release-structure regression audit after immutable method and Judge artifacts have terminalized; it never supplies scores or labels to either system.",
        basis="fixed v60 reference, new standalone method/Judge run bytes, raw report IDs, ledger IDs, receipt hashes, and provider-free evaluator calculations",
    )
    comparison_path = output / "release_15x1_comparison.json"
    _write_json(comparison_path, comparison)
    _write_comparison_markdown(output / "release_15x1_comparison_cn.md", comparison, reference)
    _write_json(output / "derived" / "release_15x1_metrics.json", metrics)
    print(json.dumps({"comparison": str(comparison_path), "deterministic_pass": all_deterministic, "soft_band_pass": soft_pass, "provider_call_count": 0, "billable_call_count": 0}, ensure_ascii=False))
    return 0 if all_deterministic and soft_pass else 2


def build_parser() -> argparse.ArgumentParser:
    """Create the provider-free release-validation command-line interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    reference = subcommands.add_parser("extract-reference", help="Extract fixed v60 15-pair x 3-round references from final_results.")
    reference.add_argument("--archive-root", required=True)
    reference.add_argument("--output-root", required=True)
    reference.add_argument("--internal-rc-commit", required=True)
    reference.set_defaults(func=extract_reference)
    manifest = subcommands.add_parser("prepare-manifest", help="Write the pre-provider internal RC validation contract.")
    manifest.add_argument("--reference", required=True)
    manifest.add_argument("--method-release-manifest", required=True)
    manifest.add_argument("--judge-release-manifest", required=True)
    manifest.add_argument("--input-closure-root", required=True)
    manifest.add_argument("--internal-rc-tag", required=True)
    manifest.add_argument("--internal-rc-commit", required=True)
    manifest.add_argument("--method-run-id", required=True)
    manifest.add_argument("--judge-run-id", required=True)
    manifest.add_argument("--output", required=True)
    manifest.set_defaults(func=prepare_manifest)
    closure = subcommands.add_parser("validate-input-closure", help="Read-only verify all v60 fixed-set context-manifest paths and hashes.")
    closure.add_argument("--reference", required=True)
    closure.add_argument("--input-closure-root", required=True)
    closure.add_argument("--output", required=True)
    closure.set_defaults(func=validate_input_closure)
    comparison = subcommands.add_parser("compare", help="Compare one completed release 15x1 method/Judge run to the fixed v60 reference.")
    comparison.add_argument("--reference", required=True)
    comparison.add_argument("--method-root", required=True)
    comparison.add_argument("--judge-root", required=True)
    comparison.add_argument("--ledger", required=True)
    comparison.add_argument("--output-root", required=True)
    comparison.set_defaults(func=compare)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one explicitly selected provider-free release-validation operation."""

    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
