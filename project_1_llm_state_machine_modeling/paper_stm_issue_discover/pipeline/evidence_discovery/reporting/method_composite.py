"""Compose immutable method runs after one or more pair-local recovery runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..orchestration.contracts import MethodCellReceipt, PairRunStatus
from ..orchestration.runner import _cost_total, _method_metrics
from .export import write_json, write_markdown_summary

COMPOSITE_SCHEMA = "evidence-discovery.method-composite.v1"
COMPOSITE_SUMMARY_SCHEMA = "evidence-discovery.method-composite-summary.v1"


class CompositeFileReceipt(BaseModel):
    """Hash-closed source and hardlink identity for one selected artifact."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source_path: str = Field(
        min_length=1, description="Absolute immutable source artifact path."
    )
    source_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the source artifact bytes before composition.",
    )
    composite_path: str = Field(
        min_length=1, description="Absolute hardlinked path in the composite root."
    )
    composite_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the selected artifact bytes in the composite root.",
    )
    hardlink_identity_preserved: bool = Field(
        description="Whether source and composite paths resolve to the same inode."
    )
    reason: str = Field(
        min_length=1, description="Why this artifact is included in the composite."
    )
    basis: str = Field(
        min_length=1, description="Byte hash and inode evidence closing the selection."
    )


class CompositeRetryAudit(BaseModel):
    """Deterministic retry and repair counts retained from method call receipts."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    logical_call_count: int = Field(
        ge=0, description="Number of staged structured method calls."
    )
    outer_attempt_count: int = Field(
        ge=0, description="Number of recorded outer structured-call attempts."
    )
    transport_retry_record_count: int = Field(
        ge=0, description="Number of provider or transport retry records."
    )
    provider_error_attempt_count: int = Field(
        ge=0, description="Number of outer attempts explicitly marked provider_error."
    )
    schema_validation_failure_count: int = Field(
        ge=0, description="Number of structured schema-repair failure rows."
    )
    usage_row_count: int = Field(
        ge=0, description="Number of normalized provider usage rows."
    )
    reason: str = Field(
        min_length=1, description="Interpretation of the retained retry counters."
    )
    basis: str = Field(
        min_length=1,
        description="Exact llm_calls attempts, retries, repairs, and usage rows.",
    )


class CompositeSourceRun(BaseModel):
    """Immutable identity, terminal cost, and retry closure for one source method run."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$", description="Original immutable source run ID."
    )
    source_root: str = Field(
        min_length=1, description="Absolute immutable source method run root."
    )
    manifest_path: str = Field(
        min_length=1, description="Absolute source run_manifest.json path."
    )
    manifest_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the original source manifest bytes.",
    )
    summary_path: str = Field(
        min_length=1, description="Absolute source summary.json path."
    )
    summary_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the original source summary bytes.",
    )
    source_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$",
        description="Repository commit that generated this source run.",
    )
    source_status: str = Field(
        min_length=1, description="Terminal status retained from the source summary."
    )
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1, description="Pair selection frozen by the source run."
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="Rounds represented by the source run."
    )
    method_cell_count: int = Field(
        ge=1, description="Complete method cells found under the source run."
    )
    method_cost_usd: float = Field(
        ge=0, description="Total billable method cost incurred by this source run."
    )
    retry_audit: CompositeRetryAudit = Field(
        description="Retry and schema-repair closure across all source cells."
    )
    reason: str = Field(
        min_length=1, description="Why this source run participates in composition."
    )
    basis: str = Field(
        min_length=1, description="Manifest, summary, cell, cost, and retry evidence."
    )


class CompositeCellReceipt(BaseModel):
    """One selected pair-round cell and all method-owned artifact provenance."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    pair_id: str = Field(
        pattern=r"^[0-9]{4}$", description="Frozen pair represented by this cell."
    )
    round: int = Field(ge=1, description="Method round represented by this cell.")
    source_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$", description="Run that produced the selected cell."
    )
    source_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Commit that produced the selected cell."
    )
    pair_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Complete pair context hash retained by the selected cell.",
    )
    status: str = Field(
        min_length=1, description="Original terminal method-cell status."
    )
    eligible: bool = Field(
        description="Original method eligibility; composition never reinterprets it."
    )
    report_count: int = Field(
        ge=0, description="Published report count in the selected cell."
    )
    evidence_count: int = Field(
        ge=0, description="Evidence-record count in the selected cell."
    )
    predicate_receipt_count: int = Field(
        ge=0, description="Predicate execution receipt count in the selected cell."
    )
    method_cost_usd: float = Field(
        ge=0, description="Billable method cost attributable to the selected cell."
    )
    retry_audit: CompositeRetryAudit = Field(
        description="Retry and schema-repair closure for the selected cell."
    )
    method_artifact: CompositeFileReceipt = Field(
        description="Hash and hardlink closure for the method cell JSON."
    )
    pair_status_artifact: CompositeFileReceipt = Field(
        description="Hash and hardlink closure for the source pair status JSON."
    )
    audit_bundle_artifacts: tuple[CompositeFileReceipt, ...] = Field(
        description="Selected method-owned W2 audit bundles for this pair-round."
    )
    reason: str = Field(
        min_length=1, description="Why this source cell is selected for the composite."
    )
    basis: str = Field(
        min_length=1,
        description="Source run, pair-round identity, hashes, and hardlinks.",
    )


class CompositeReplacementReceipt(BaseModel):
    """One base pair-round cell explicitly superseded by a recovery source cell."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Recovered pair ID.")
    round: int = Field(ge=1, description="Recovered method round.")
    base_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$", description="Run containing the superseded cell."
    )
    base_cell_path: str = Field(
        min_length=1, description="Absolute superseded method cell path."
    )
    base_cell_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the superseded method cell bytes.",
    )
    base_cell_cost_usd: float = Field(
        ge=0, description="Billable cost incurred by the superseded method cell."
    )
    base_retry_audit: CompositeRetryAudit = Field(
        description="Retry and repair counts retained from the superseded cell."
    )
    replacement_run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Recovery run supplying the selected cell.",
    )
    replacement_cell_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the selected recovery method cell bytes.",
    )
    replacement_cell_cost_usd: float = Field(
        ge=0, description="Billable cost incurred by the selected recovery cell."
    )
    input_identity_equal: bool = Field(
        description="Whether base and replacement cells use the exact same pair input hash."
    )
    reason: str = Field(
        min_length=1, description="Why this pair-local replacement is admissible."
    )
    basis: str = Field(
        min_length=1,
        description="Pair-round identity, input hash, source hashes, and costs.",
    )


class CompositeBuildProvenance(BaseModel):
    """Clean repository identity used only to build the evaluator-side composite."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$",
        description="Clean commit containing the composite implementation.",
    )
    source_branch: str = Field(
        min_length=1, description="Branch from which the composite was built."
    )
    source_dirty: Literal[False] = Field(
        default=False,
        description="Tracked worktree cleanliness required for composition.",
    )
    reason: str = Field(
        min_length=1,
        description="Clarifies that this identity built but did not generate cells.",
    )
    basis: str = Field(
        min_length=1, description="git status, rev-parse, and branch commands."
    )


class MethodCompositeManifest(BaseModel):
    """Source-explicit immutable manifest for a base run plus pair-local recoveries."""

    model_config = ConfigDict(
        extra="forbid", frozen=True, populate_by_name=True, str_strip_whitespace=True
    )

    schema_version: Literal["evidence-discovery.method-composite.v1"] = Field(
        default=COMPOSITE_SCHEMA,
        alias="schema",
        description="Versioned evaluator-side method composite schema.",
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$", description="Immutable composite identity."
    )
    status: Literal["completed"] = Field(
        default="completed", description="All selected pair-round cells are terminal."
    )
    source_provenance: CompositeBuildProvenance = Field(
        description="Repository identity of composition code, not method generation."
    )
    method_source_commits: tuple[str, ...] = Field(
        min_length=1,
        description="Distinct commits that generated selected method cells.",
    )
    registry_version: str = Field(
        min_length=1, description="Frozen registry version shared by all sources."
    )
    registry_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Frozen registry hash shared by all source runs.",
    )
    profile: str = Field(
        min_length=1, description="Method profile shared by all source runs."
    )
    workers: tuple[int, ...] = Field(
        min_length=1, description="Exact worker counts recorded by source runs."
    )
    rounds: Literal[1, 3] = Field(
        description="Method round count represented by the composite."
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="Exact method rounds represented in the composite."
    )
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1, description="Exact ordered base-run pair selection."
    )
    scope: Literal["diagnostic_subset", "full_protocol"] = Field(
        description="Base-run method scope retained for evaluator reporting."
    )
    pair_input_hashes: dict[str, str] = Field(
        min_length=1,
        description="Pair-keyed input identities validated across replacements.",
    )
    source_runs: tuple[CompositeSourceRun, ...] = Field(
        min_length=2,
        description="Base and recovery source runs with full cost/retry closure.",
    )
    cell_receipts: tuple[CompositeCellReceipt, ...] = Field(
        min_length=1,
        description="Exactly one selected source for every pair-round key.",
    )
    replacements: tuple[CompositeReplacementReceipt, ...] = Field(
        min_length=1, description="Explicit base-to-recovery replacement decisions."
    )
    reason: str = Field(
        min_length=1, description="Why deterministic pair-local composition is used."
    )
    basis: str = Field(
        min_length=1,
        description="Source manifests, hashes, hardlinks, input parity, and costs.",
    )


class MethodCompositeSummary(BaseModel):
    """Selected-result metrics and all-incurred method costs for one composite."""

    model_config = ConfigDict(
        extra="forbid", frozen=True, populate_by_name=True, str_strip_whitespace=True
    )

    schema_version: Literal["evidence-discovery.method-composite-summary.v1"] = Field(
        default=COMPOSITE_SUMMARY_SCHEMA,
        alias="schema",
        description="Versioned composite summary schema.",
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$", description="Owning composite identity."
    )
    status: Literal["completed"] = Field(
        default="completed",
        description="All selected cells and source audits are closed.",
    )
    artifact_root: str = Field(
        min_length=1, description="Absolute composite artifact root."
    )
    source_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$",
        description="Composite builder commit retained for reporting compatibility.",
    )
    method_source_commits: tuple[str, ...] = Field(
        min_length=1, description="Commits that generated selected method cells."
    )
    registry_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Frozen registry hash."
    )
    pair_count: int = Field(ge=1, description="Selected pair count.")
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1, description="Ordered selected pair IDs."
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="Selected method rounds."
    )
    method_cell_count: int = Field(
        ge=1, description="Selected terminal method-cell count."
    )
    selected_result_cost_usd: float = Field(
        ge=0, description="Cost of the  selected cells used for evaluation."
    )
    superseded_cell_cost_usd: float = Field(
        ge=0, description="Cost of base cells replaced after a diagnosed failure."
    )
    unselected_source_cost_usd: float = Field(
        ge=0,
        description="Other source-run cost not represented by selected or superseded cells.",
    )
    method_cost_usd: float = Field(
        ge=0, description="All method cost actually incurred across every source run."
    )
    metrics: dict[str, Any] = Field(
        description="Method-only W/D, publication, execution, coverage, and cost metrics."
    )
    per_pair: dict[str, dict[str, Any]] = Field(
        description="Selected-result method metrics for every pair."
    )
    method_cells_with_diagnostics: tuple[str, ...] = Field(
        description="Selected pair-round identities retaining method diagnostics."
    )
    source_runs: tuple[CompositeSourceRun, ...] = Field(
        min_length=2,
        description="Source cost and retry audits retained in the summary.",
    )
    replacements: tuple[CompositeReplacementReceipt, ...] = Field(
        min_length=1, description="Explicit recovery replacement receipts."
    )
    reason: str = Field(
        min_length=1,
        description="Interpretation of selected metrics and total incurred cost.",
    )
    basis: str = Field(
        min_length=1,
        description="Composite manifest and deterministic method aggregation.",
    )


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def _rounds(manifest: dict[str, Any]) -> tuple[int, ...]:
    selected = manifest.get("selected_rounds")
    if isinstance(selected, list | tuple) and selected:
        return tuple(sorted({int(value) for value in selected}))
    count = int(manifest.get("rounds") or 0)
    if count not in {1, 3}:
        raise ValueError("source manifest rounds must be 1 or 3")
    return tuple(range(1, count + 1))


def _cell_paths(root: Path) -> dict[tuple[str, int], Path]:
    result: dict[tuple[str, int], Path] = {}
    for path in sorted((root / "method").glob("*/round-*.json")):
        pair_id = path.parent.name
        round_text = path.stem.removeprefix("round-")
        if not round_text.isdigit():
            raise ValueError(f"invalid method cell path: {path}")
        key = (pair_id, int(round_text))
        if key in result:
            raise ValueError(f"duplicate method cell key: {key}")
        result[key] = path
    if not result:
        raise FileNotFoundError(f"no method cells under {root}")
    return result


def _retry_audit(cell: dict[str, Any]) -> CompositeRetryAudit:
    calls = cell.get("llm_calls")
    if not isinstance(calls, list):
        calls = []
    outer_attempt_count = 0
    transport_retry_count = 0
    provider_error_count = 0
    schema_failure_count = 0
    usage_count = 0
    for call in calls:
        if not isinstance(call, dict):
            continue
        attempts = call.get("attempts")
        if not isinstance(attempts, list):
            attempts = []
        usage = call.get("usage")
        if isinstance(usage, list):
            usage_count += len(usage)
        for attempt in attempts:
            if not isinstance(attempt, dict):
                continue
            outer_attempt_count += 1
            provider_error_count += int(bool(attempt.get("provider_error")))
            retries = attempt.get("retry_records")
            if isinstance(retries, list):
                transport_retry_count += len(retries)
            failures = attempt.get("schema_validation_failures")
            if isinstance(failures, list):
                schema_failure_count += len(failures)
    return CompositeRetryAudit(
        logical_call_count=sum(isinstance(call, dict) for call in calls),
        outer_attempt_count=outer_attempt_count,
        transport_retry_record_count=transport_retry_count,
        provider_error_attempt_count=provider_error_count,
        schema_validation_failure_count=schema_failure_count,
        usage_row_count=usage_count,
        reason="Counts preserve provider retries and billable schema-repair rows without changing their source receipts.",
        basis="method cell llm_calls[].attempts, retry_records, schema_validation_failures, and usage",
    )


def _sum_retry_audits(values: Sequence[CompositeRetryAudit]) -> CompositeRetryAudit:
    return CompositeRetryAudit(
        logical_call_count=sum(value.logical_call_count for value in values),
        outer_attempt_count=sum(value.outer_attempt_count for value in values),
        transport_retry_record_count=sum(
            value.transport_retry_record_count for value in values
        ),
        provider_error_attempt_count=sum(
            value.provider_error_attempt_count for value in values
        ),
        schema_validation_failure_count=sum(
            value.schema_validation_failure_count for value in values
        ),
        usage_row_count=sum(value.usage_row_count for value in values),
        reason="Counters are summed across disjoint immutable method cells.",
        basis="Cell-local CompositeRetryAudit receipts.",
    )


def _hardlink(source: Path, target: Path, *, reason: str) -> CompositeFileReceipt:
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, target)
    source_hash = _sha256(source)
    target_hash = _sha256(target)
    same_inode = source.stat().st_ino == target.stat().st_ino
    if not same_inode or source_hash != target_hash:
        raise RuntimeError(f"hardlink closure failed: {source} -> {target}")
    return CompositeFileReceipt(
        source_path=str(source.resolve()),
        source_hash=source_hash,
        composite_path=str(target.resolve()),
        composite_hash=target_hash,
        hardlink_identity_preserved=same_inode,
        reason=reason,
        basis=f"source={source_hash}; composite={target_hash}; inode={source.stat().st_ino}",
    )


def _git_value(repository_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ("git", *args), cwd=repository_root, text=True
    ).strip()


def _build_provenance(repository_root: Path) -> CompositeBuildProvenance:
    dirty = _git_value(repository_root, "status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise RuntimeError("method composition requires a clean tracked commit")
    return CompositeBuildProvenance(
        source_commit=_git_value(repository_root, "rev-parse", "HEAD"),
        source_branch=_git_value(repository_root, "branch", "--show-current")
        or "detached",
        reason="This clean commit built the evaluator composite; source_runs identify the commits that generated method cells.",
        basis="git status --porcelain --untracked-files=no; git rev-parse HEAD; git branch --show-current",
    )


def _source_run(
    root: Path,
) -> tuple[CompositeSourceRun, dict[tuple[str, int], dict[str, Any]]]:
    manifest_path = root / "run_manifest.json"
    summary_path = root / "summary.json"
    manifest = _load(manifest_path)
    summary = _load(summary_path)
    run_id = str(manifest.get("run_id") or "")
    if summary.get("run_id") != run_id:
        raise ValueError(f"source manifest/summary run mismatch: {root}")
    source_commit = str(
        manifest.get("source_provenance", {}).get("source_commit") or ""
    )
    paths = _cell_paths(root)
    cells: dict[tuple[str, int], dict[str, Any]] = {}
    for key, path in paths.items():
        model = MethodCellReceipt.model_validate_json(path.read_text(encoding="utf-8"))
        if (model.pair_id, model.round) != key or model.run_id != run_id:
            raise ValueError(f"source cell identity mismatch: {path}")
        if model.source_provenance.source_commit != source_commit:
            raise ValueError(f"source cell commit mismatch: {path}")
        cells[key] = model.model_dump(mode="json")
    cell_cost = sum(_cost_total(cell) for cell in cells.values())
    summary_cost = float(summary.get("method_cost_usd") or 0.0)
    if abs(cell_cost - summary_cost) > 1e-9:
        raise ValueError(
            f"source method cost mismatch: root={root}, cells={cell_cost}, summary={summary_cost}"
        )
    rounds = _rounds(manifest)
    expected_keys = {
        (str(pair_id), round_no)
        for pair_id in manifest.get("selected_pair_ids", ())
        for round_no in rounds
    }
    if set(cells) != expected_keys:
        raise ValueError(
            f"source method closure mismatch: missing={sorted(expected_keys - set(cells))}, "
            f"extra={sorted(set(cells) - expected_keys)}"
        )
    retry_audits = [_retry_audit(cell) for cell in cells.values()]
    receipt = CompositeSourceRun(
        run_id=run_id,
        source_root=str(root.resolve()),
        manifest_path=str(manifest_path.resolve()),
        manifest_hash=_sha256(manifest_path),
        summary_path=str(summary_path.resolve()),
        summary_hash=_sha256(summary_path),
        source_commit=source_commit,
        source_status=str(summary.get("status") or ""),
        selected_pair_ids=tuple(str(value) for value in manifest["selected_pair_ids"]),
        selected_rounds=rounds,
        method_cell_count=len(cells),
        method_cost_usd=summary_cost,
        retry_audit=_sum_retry_audits(retry_audits),
        reason="The run supplies base or recovery method cells without rewriting any source artifact.",
        basis="Hash-verified manifest and summary plus validated terminal method cells and exact cell-cost sum.",
    )
    return receipt, cells


def build_method_composite(
    *,
    composite_id: str,
    base_run_root: Path,
    replacement_run_roots: Sequence[Path],
    output_root: Path,
    build_provenance: CompositeBuildProvenance,
) -> tuple[MethodCompositeManifest, MethodCompositeSummary]:
    """Build one source-explicit evaluator root from a base run and recoveries."""

    base_run_root = base_run_root.expanduser().resolve()
    roots = (base_run_root,) + tuple(
        root.expanduser().resolve() for root in replacement_run_roots
    )
    if len(roots) < 2:
        raise ValueError("at least one replacement run root is required")
    if len(set(roots)) != len(roots):
        raise ValueError("source run roots must be distinct")
    output_root = output_root.expanduser().resolve()
    if output_root.exists() and any(output_root.iterdir()):
        raise FileExistsError(f"composite output root is non-empty: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)

    source_runs: list[CompositeSourceRun] = []
    source_cells: list[dict[tuple[str, int], dict[str, Any]]] = []
    source_paths: list[dict[tuple[str, int], Path]] = []
    source_manifests: list[dict[str, Any]] = []
    for root in roots:
        source_run, cells = _source_run(root)
        source_runs.append(source_run)
        source_cells.append(cells)
        source_paths.append(_cell_paths(root))
        source_manifests.append(_load(root / "run_manifest.json"))

    base_manifest = source_manifests[0]
    shared_fields = ("registry_version", "registry_hash", "profile")
    for manifest in source_manifests[1:]:
        for field in shared_fields:
            if manifest.get(field) != base_manifest.get(field):
                raise ValueError(f"source runs disagree on {field}")

    selected: dict[tuple[str, int], int] = {key: 0 for key in source_cells[0]}
    replacements: list[CompositeReplacementReceipt] = []
    for source_index, cells in enumerate(source_cells[1:], start=1):
        for key, replacement in sorted(cells.items()):
            if key not in source_cells[0]:
                raise ValueError(f"replacement key is absent from base run: {key}")
            if selected[key] != 0:
                raise ValueError(f"replacement key supplied more than once: {key}")
            base = source_cells[0][key]
            input_equal = base.get("pair_input_hash") == replacement.get(
                "pair_input_hash"
            )
            if not input_equal:
                raise ValueError(f"replacement pair input mismatch: {key}")
            selected[key] = source_index
            replacements.append(
                CompositeReplacementReceipt(
                    pair_id=key[0],
                    round=key[1],
                    base_run_id=source_runs[0].run_id,
                    base_cell_path=str(source_paths[0][key].resolve()),
                    base_cell_hash=_sha256(source_paths[0][key]),
                    base_cell_cost_usd=_cost_total(base),
                    base_retry_audit=_retry_audit(base),
                    replacement_run_id=source_runs[source_index].run_id,
                    replacement_cell_hash=_sha256(source_paths[source_index][key]),
                    replacement_cell_cost_usd=_cost_total(replacement),
                    input_identity_equal=True,
                    reason="A complete pair-local recovery cell replaces the diagnosed base cell without resampling any other pair.",
                    basis=(
                        f"pair={key[0]}; round={key[1]}; input={base.get('pair_input_hash')}; "
                        f"base={_sha256(source_paths[0][key])}; replacement={_sha256(source_paths[source_index][key])}"
                    ),
                )
            )

    pair_ids = tuple(str(value) for value in base_manifest["selected_pair_ids"])
    selected_rounds = _rounds(base_manifest)
    expected_keys = {
        (pair_id, round_no) for pair_id in pair_ids for round_no in selected_rounds
    }
    if set(selected) != expected_keys:
        raise ValueError("base run does not close the declared pair-round grid")
    for pair_id in pair_ids:
        pair_sources = {selected[(pair_id, round_no)] for round_no in selected_rounds}
        if len(pair_sources) != 1:
            raise ValueError(
                f"all rounds of one pair must use one source pair status: {pair_id}"
            )

    cell_receipts: list[CompositeCellReceipt] = []
    selected_cells: dict[str, list[dict[str, Any]]] = {
        pair_id: [] for pair_id in pair_ids
    }
    selected_statuses: dict[str, dict[str, Any]] = {}
    status_artifacts: dict[str, CompositeFileReceipt] = {}
    for pair_id in pair_ids:
        for round_no in selected_rounds:
            key = (pair_id, round_no)
            source_index = selected[key]
            source_root = roots[source_index]
            source_run = source_runs[source_index]
            cell = source_cells[source_index][key]
            source_path = source_paths[source_index][key]
            method_artifact = _hardlink(
                source_path,
                output_root / "method" / pair_id / f"round-{round_no}.json",
                reason="This exact source method cell was selected for external evaluation.",
            )
            if pair_id not in status_artifacts:
                status_source = source_root / "pairs" / pair_id / "status.json"
                status_model = PairRunStatus.model_validate_json(
                    status_source.read_text(encoding="utf-8")
                )
                if (
                    status_model.pair_id != pair_id
                    or status_model.run_id != source_run.run_id
                ):
                    raise ValueError(
                        f"source pair status identity mismatch: {status_source}"
                    )
                status_artifacts[pair_id] = _hardlink(
                    status_source,
                    output_root / "pairs" / pair_id / "status.json",
                    reason="The selected source pair status retains its original run identity.",
                )
                selected_statuses[pair_id] = status_model.model_dump(mode="json")
            status_artifact = status_artifacts[pair_id]
            bundle_receipts = tuple(
                _hardlink(
                    bundle,
                    output_root / "audit_bundles" / bundle.name,
                    reason="This method-owned W2 audit bundle belongs to the selected pair-round cell.",
                )
                for bundle in sorted(
                    (source_root / "audit_bundles").glob(
                        f"{pair_id}:r{round_no}:*.json"
                    )
                )
            )
            retry_audit = _retry_audit(cell)
            cell_receipts.append(
                CompositeCellReceipt(
                    pair_id=pair_id,
                    round=round_no,
                    source_run_id=source_run.run_id,
                    source_commit=source_run.source_commit,
                    pair_input_hash=str(cell["pair_input_hash"]),
                    status=str(cell["status"]),
                    eligible=bool(cell["eligible"]),
                    report_count=len(cell.get("report_issue_clusters", ())),
                    evidence_count=len(cell.get("evidence_records", ())),
                    predicate_receipt_count=len(
                        cell.get("predicate_execution_receipts", ())
                    ),
                    method_cost_usd=_cost_total(cell),
                    retry_audit=retry_audit,
                    method_artifact=method_artifact,
                    pair_status_artifact=status_artifact,
                    audit_bundle_artifacts=bundle_receipts,
                    reason=(
                        "The recovery source supplies this key."
                        if source_index
                        else "The base source supplies this unchanged key."
                    ),
                    basis=(
                        f"source_run={source_run.run_id}; source_commit={source_run.source_commit}; "
                        f"cell={method_artifact.source_hash}"
                    ),
                )
            )
            selected_cells[pair_id].append(cell)

    metrics = _method_metrics(
        pair_method=selected_cells,
        selected_pair_ids=pair_ids,
        ineligible_pair_ids=tuple(
            pair_id
            for pair_id, status in selected_statuses.items()
            if int(status.get("audit_errors") or 0) > 0
        ),
    )
    selected_cost = sum(receipt.method_cost_usd for receipt in cell_receipts)
    superseded_cost = sum(receipt.base_cell_cost_usd for receipt in replacements)
    total_incurred_cost = sum(run.method_cost_usd for run in source_runs)
    unselected_source_cost = total_incurred_cost - selected_cost - superseded_cost
    if unselected_source_cost < -1e-9:
        raise ValueError("source cost accounting is not additive")
    unselected_source_cost = max(0.0, unselected_source_cost)
    metrics["cost"] = {
        "eligible": all(
            bool(status.get("method_cost_eligible"))
            for status in selected_statuses.values()
        ),
        "selected_result_usd": selected_cost,
        "superseded_cell_usd": superseded_cost,
        "unselected_source_usd": unselected_source_cost,
        "total_incurred_usd": total_incurred_cost,
        "reason": "Evaluation metrics use selected cells, while experiment cost retains every base and recovery call actually incurred.",
        "basis": "Validated cell llm_call cost receipts and immutable source run summaries.",
    }

    method_source_commits = tuple(
        sorted({receipt.source_commit for receipt in cell_receipts})
    )
    pair_input_hashes = {
        pair_id: str(base_manifest["pair_input_hashes"][pair_id])
        for pair_id in pair_ids
    }
    manifest = MethodCompositeManifest(
        run_id=composite_id,
        source_provenance=build_provenance,
        method_source_commits=method_source_commits,
        registry_version=str(base_manifest["registry_version"]),
        registry_hash=str(base_manifest["registry_hash"]),
        profile=str(base_manifest["profile"]),
        workers=tuple(
            sorted({int(value.get("workers") or 1) for value in source_manifests})
        ),
        rounds=int(base_manifest["rounds"]),
        selected_rounds=selected_rounds,
        selected_pair_ids=pair_ids,
        scope=str(base_manifest["scope"]),
        pair_input_hashes=pair_input_hashes,
        source_runs=tuple(source_runs),
        cell_receipts=tuple(cell_receipts),
        replacements=tuple(replacements),
        reason="The composite replaces only explicitly recovered pair-round cells and preserves all other source bytes by hardlink.",
        basis="Source-explicit cell selection, equal pair input hashes, shared registry/profile, byte hashes, hardlinks, and complete cost/retry audits.",
    )
    summary = MethodCompositeSummary(
        run_id=composite_id,
        artifact_root=str(output_root),
        source_commit=build_provenance.source_commit,
        method_source_commits=method_source_commits,
        registry_hash=manifest.registry_hash,
        pair_count=len(pair_ids),
        selected_pair_ids=pair_ids,
        selected_rounds=selected_rounds,
        method_cell_count=len(cell_receipts),
        selected_result_cost_usd=selected_cost,
        superseded_cell_cost_usd=superseded_cost,
        unselected_source_cost_usd=unselected_source_cost,
        method_cost_usd=total_incurred_cost,
        metrics=metrics,
        per_pair=metrics["per_pair"],
        method_cells_with_diagnostics=tuple(
            f"{receipt.pair_id}:r{receipt.round}"
            for receipt in cell_receipts
            if receipt.status != "completed"
        ),
        source_runs=tuple(source_runs),
        replacements=tuple(replacements),
        reason="Selected-result metrics are separated from superseded and total incurred costs; no source method result was rewritten.",
        basis="Validated MethodCompositeManifest plus the existing deterministic method metrics aggregator.",
    )
    manifest_payload = manifest.model_dump(mode="json", by_alias=True)
    summary_payload = summary.model_dump(mode="json", by_alias=True)
    write_json(output_root / "run_manifest.json", manifest_payload)
    write_json(output_root / "method_composite_audit.json", manifest_payload)
    write_json(output_root / "summary.json", summary_payload)
    write_markdown_summary(output_root / "SUMMARY.md", summary_payload)
    return manifest, summary


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--composite-id", required=True)
    parser.add_argument("--base-run-root", type=Path, required=True)
    parser.add_argument(
        "--replacement-run-root", action="append", type=Path, required=True
    )
    parser.add_argument("--output-root", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate source runs and write one immutable evaluator-side method root."""

    args = _parser().parse_args(argv)
    repository_root = Path(__file__).resolve().parents[5]
    provenance = _build_provenance(repository_root)
    manifest, summary = build_method_composite(
        composite_id=args.composite_id,
        base_run_root=args.base_run_root,
        replacement_run_roots=tuple(args.replacement_run_root),
        output_root=args.output_root,
        build_provenance=provenance,
    )
    print(
        json.dumps(
            {
                "output_root": str(args.output_root.expanduser().resolve()),
                "run_id": manifest.run_id,
                "cell_count": len(manifest.cell_receipts),
                "replacement_count": len(manifest.replacements),
                "selected_result_cost_usd": summary.selected_result_cost_usd,
                "total_incurred_cost_usd": summary.method_cost_usd,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
