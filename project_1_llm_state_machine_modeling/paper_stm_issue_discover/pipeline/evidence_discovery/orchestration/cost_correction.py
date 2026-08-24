from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from utils.llm import LLMPricing, load_llm_registry

from .runtime import _cost_for_usage, _usage_rows

ALGORITHM_VERSION = "evidence-discovery.corrected-method-cost.v1"
AGGREGATE_SCHEMA = "evidence-discovery.corrected_method_cost.v1"


class FrozenCostModel(BaseModel):
    """Strict immutable base for deterministic historical cost correction records."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class HashedSourceArtifact(FrozenCostModel):
    """One immutable historical artifact consumed by the correction aggregate."""

    role: Literal["run_manifest", "summary", "method_cell", "llm_result"] = Field(
        description="Artifact role in the historical method usage closure."
    )
    path: str = Field(min_length=1, description="Exact resolved source artifact path.")
    sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 digest of the source artifact bytes.",
    )
    size_bytes: int = Field(ge=0, description="Exact source artifact byte length.")


class CorrectedTokenCost(FrozenCostModel):
    """One normalized token class and its independently reproducible USD cost."""

    tokens: int = Field(ge=0, description="Billable tokens in this normalized class.")
    usd_per_million_tokens: float = Field(
        ge=0, description="Frozen price for one million tokens in this class."
    )
    cost_usd: float = Field(ge=0, description="Tokens multiplied by the frozen rate.")


class CorrectedCostBreakdown(FrozenCostModel):
    """Four-class method token and price breakdown after usage normalization."""

    uncached_input: CorrectedTokenCost = Field(
        description="Input tokens excluding cache-read and cache-creation tokens."
    )
    cache_read: CorrectedTokenCost = Field(
        description="Provider-reported cache-read input tokens."
    )
    cache_creation: CorrectedTokenCost = Field(
        description="Provider-reported cache-creation or cache-write input tokens."
    )
    output: CorrectedTokenCost = Field(
        description="Provider-reported output tokens, including reasoning when applicable."
    )


class CorrectedResultReceipt(FrozenCostModel):
    """Normalized cost and immutable provenance for one historical LLM result."""

    pair_id: str = Field(pattern=r"^\d{4}$", description="Historical method pair ID.")
    round: int = Field(ge=1, description="Historical independent method round.")
    call_kind: str = Field(min_length=1, description="Method structured-call stage name.")
    outer_attempt: int = Field(ge=1, description="Cell-level attempt owning this result.")
    billing_disposition: str = Field(
        min_length=1, description="Original attempt billing disposition, preserved verbatim."
    )
    provider_error: bool = Field(
        description="Whether the original attempt was explicitly provider-owned and exempt."
    )
    usage_row_count: int = Field(
        ge=0, description="Underlying provider requests retained in this result artifact."
    )
    cost_eligible: bool = Field(
        description="Whether every billable row has complete usage and configured prices."
    )
    corrected_cost_usd: float = Field(
        ge=0, description="Corrected cost for this result after cache normalization."
    )
    result_path: str = Field(min_length=1, description="Exact historical result path.")
    result_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 digest of the immutable result bytes.",
    )
    reason: str = Field(
        min_length=1, description="Deterministic billing interpretation for this result."
    )
    basis: str = Field(
        min_length=1, description="Usage, attempt, and pricing evidence used for this result."
    )


class CorrectedPairCost(FrozenCostModel):
    """Corrected method cost subtotal for one pair across selected historical rounds."""

    pair_id: str = Field(pattern=r"^\d{4}$", description="Historical method pair ID.")
    method_cell_count: int = Field(ge=1, description="Method cells included for this pair.")
    logical_call_count: int = Field(
        ge=0, description="Structured method calls included for this pair."
    )
    provider_request_count: int = Field(
        ge=0, description="Underlying normalized provider usage rows for this pair."
    )
    corrected_cost_usd: float = Field(
        ge=0, description="Corrected method cost subtotal for this pair."
    )


class CorrectedMethodCostAggregate(FrozenCostModel):
    """Auditable correction of one immutable historical method cost summary.

    This record never rewrites the source run. It reclassifies provider cache
    tokens through the shared ``utils.llm`` normalization and pricing boundary,
    while preserving original provider-error billing exemptions and making
    schema-repair usage billable.
    """

    schema: Literal["evidence-discovery.corrected_method_cost.v1"] = Field(
        description="Stable corrected-cost aggregate schema identifier."
    )
    algorithm_version: Literal[
        "evidence-discovery.corrected-method-cost.v1"
    ] = Field(description="Deterministic historical re-pricing algorithm version.")
    source_run_root: str = Field(
        min_length=1, description="Resolved read-only historical method run root."
    )
    source_run_id: str = Field(min_length=1, description="Historical non-reusable run ID.")
    source_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Commit recorded by the historical run."
    )
    profile: str = Field(min_length=1, description="Historical public LLM profile name.")
    source_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of sorted source artifact roles, paths, byte hashes, and sizes.",
    )
    source_artifacts: tuple[HashedSourceArtifact, ...] = Field(
        min_length=1, description="Complete manifest, summary, method-cell, and result closure."
    )
    original_reported_method_cost_usd: float = Field(
        ge=0, description="Method cost preserved from the historical summary without mutation."
    )
    corrected_method_cost_usd: float = Field(
        ge=0, description="Method cost recomputed from immutable normalized usage receipts."
    )
    correction_delta_usd: float = Field(
        description="Corrected cost minus the original reported method cost."
    )
    pricing: dict[str, Any] = Field(
        description="Public frozen pricing card used for deterministic re-pricing."
    )
    method_cell_count: int = Field(ge=1, description="Historical method cells consumed.")
    logical_call_count: int = Field(ge=0, description="Structured method calls consumed.")
    outer_attempt_count: int = Field(ge=0, description="Cell-level result attempts consumed.")
    provider_request_count: int = Field(
        ge=0, description="Underlying normalized provider usage rows consumed."
    )
    billable_provider_request_count: int = Field(
        ge=0, description="Usage rows included in corrected pricing."
    )
    provider_error_exempt_request_count: int = Field(
        ge=0, description="Usage rows excluded only by explicit provider-error ownership."
    )
    schema_validation_failure_count: int = Field(
        ge=0, description="Billable structured-output failures retained by method call receipts."
    )
    cost_eligible: bool = Field(
        description="Whether all non-exempt usage rows close under the frozen price card."
    )
    breakdown: CorrectedCostBreakdown = Field(
        description="Reproducible uncached/cache/output token and cost classes."
    )
    per_pair: tuple[CorrectedPairCost, ...] = Field(
        description="Deterministic pair subtotals in lexical pair order."
    )
    result_receipts: tuple[CorrectedResultReceipt, ...] = Field(
        description="Per-result provenance and corrected cost in method execution order."
    )
    reason: str = Field(
        min_length=1, description="Why the historical reported cost required correction."
    )
    basis: str = Field(
        min_length=1, description="Immutable receipt, normalization, pricing, and hash basis."
    )


def _hash_artifact(
    path: Path,
    role: Literal["run_manifest", "summary", "method_cell", "llm_result"],
) -> HashedSourceArtifact:
    data = path.read_bytes()
    return HashedSourceArtifact(
        role=role,
        path=str(path.resolve()),
        sha256="sha256:" + hashlib.sha256(data).hexdigest(),
        size_bytes=len(data),
    )


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def _category_breakdown(
    attempts: Sequence[dict[str, Any]], pricing: LLMPricing
) -> CorrectedCostBreakdown:
    token_keys = {
        "uncached_input": "input",
        "cache_read": "cache_read",
        "cache_creation": "cache_write",
        "output": "output",
    }
    tokens = {
        output_key: sum(
            int(attempt.get("categories", {}).get(cost_key, {}).get("tokens", 0))
            for attempt in attempts
        )
        for output_key, cost_key in token_keys.items()
    }
    rates = {
        "uncached_input": pricing.prices.input_usd_per_million_tokens,
        "cache_read": pricing.prices.cache_read_usd_per_million_tokens or 0.0,
        "cache_creation": pricing.prices.cache_write_usd_per_million_tokens or 0.0,
        "output": pricing.prices.output_usd_per_million_tokens,
    }
    values = {
        key: CorrectedTokenCost(
            tokens=tokens[key],
            usd_per_million_tokens=rates[key],
            cost_usd=tokens[key] * rates[key] / 1_000_000,
        )
        for key in token_keys
    }
    return CorrectedCostBreakdown(**values)


def build_corrected_method_cost(
    source_run_root: Path,
    *,
    pricing: LLMPricing | None = None,
) -> CorrectedMethodCostAggregate:
    """Re-price one historical method run without modifying any source artifact."""

    root = source_run_root.resolve()
    manifest_path = root / "run_manifest.json"
    summary_path = root / "summary.json"
    manifest = _load_object(manifest_path)
    summary = _load_object(summary_path)
    run_id = str(summary.get("run_id") or manifest.get("run_id") or "")
    if not run_id or manifest.get("run_id") != run_id:
        raise ValueError("summary and manifest run IDs do not close")
    profile = str(summary.get("profile") or manifest.get("profile") or "")
    if not profile or manifest.get("profile") != profile:
        raise ValueError("summary and manifest profiles do not close")
    source_commit = str(summary.get("source_commit") or "")
    manifest_commit = (manifest.get("source_provenance") or {}).get("source_commit")
    if not source_commit or manifest_commit != source_commit:
        raise ValueError("summary and manifest source commits do not close")
    selected_pricing = pricing or load_llm_registry().require(profile).pricing
    if selected_pricing is None:
        raise ValueError(f"profile {profile!r} has no pricing card")

    source_artifacts = [
        _hash_artifact(manifest_path, "run_manifest"),
        _hash_artifact(summary_path, "summary"),
    ]
    all_rows: list[dict[str, Any]] = []
    result_receipts: list[CorrectedResultReceipt] = []
    seen_results: set[Path] = set()
    logical_call_count = 0
    outer_attempt_count = 0
    schema_validation_failure_count = 0
    pair_totals: dict[str, dict[str, Any]] = {}
    method_paths = sorted((root / "method").glob("*/round-*.json"))
    if not method_paths:
        raise ValueError("historical run contains no method cells")

    for method_path in method_paths:
        source_artifacts.append(_hash_artifact(method_path, "method_cell"))
        cell = _load_object(method_path)
        pair_id = str(cell.get("pair_id") or "")
        round_index = int(cell.get("round") or 0)
        if cell.get("run_id") != run_id or not pair_id or round_index < 1:
            raise ValueError(f"method identity does not close: {method_path}")
        pair_total = pair_totals.setdefault(
            pair_id,
            {"method_cells": 0, "logical_calls": 0, "rows": 0, "cost": 0.0},
        )
        pair_total["method_cells"] += 1
        calls = cell.get("llm_calls")
        if not isinstance(calls, list):
            raise TypeError(f"method cell has no llm_calls list: {method_path}")
        for call in calls:
            if not isinstance(call, dict):
                raise TypeError(f"invalid llm_calls item: {method_path}")
            call_kind = str(call.get("kind") or "")
            if not call_kind:
                raise ValueError(f"method call has no kind: {method_path}")
            logical_call_count += 1
            pair_total["logical_calls"] += 1
            failures = call.get("schema_validation_failures") or []
            if not isinstance(failures, list):
                raise TypeError(f"invalid schema failure receipt: {method_path}")
            schema_validation_failure_count += len(failures)
            attempts = call.get("attempts")
            if not isinstance(attempts, list):
                raise TypeError(f"method call has no attempts list: {method_path}")
            for attempt in attempts:
                if not isinstance(attempt, dict):
                    raise TypeError(f"invalid attempt receipt: {method_path}")
                outer_attempt_count += 1
                result_path = Path(str(attempt.get("result_path") or "")).resolve()
                if result_path in seen_results:
                    raise ValueError(f"duplicate result artifact reference: {result_path}")
                if not result_path.is_relative_to(root):
                    raise ValueError(f"result artifact escapes source run: {result_path}")
                seen_results.add(result_path)
                result_artifact = _hash_artifact(result_path, "llm_result")
                source_artifacts.append(result_artifact)
                result = _load_object(result_path)
                outer_attempt = int(attempt.get("outer_attempt") or 0)
                if outer_attempt < 1:
                    raise ValueError(f"invalid outer attempt: {result_path}")
                rows = _usage_rows(result, outer_attempt=outer_attempt)
                disposition = str(attempt.get("billing_disposition") or "billable")
                provider_error = bool(attempt.get("provider_error")) or (
                    disposition == "provider_error_retry_exempt"
                )
                for row in rows:
                    row["billing_disposition"] = disposition
                    row["cost_counted"] = not provider_error
                result_cost = _cost_for_usage(rows, selected_pricing)
                all_rows.extend(rows)
                pair_total["rows"] += len(rows)
                pair_total["cost"] += float(result_cost["total_usd"])
                result_receipts.append(
                    CorrectedResultReceipt(
                        pair_id=pair_id,
                        round=round_index,
                        call_kind=call_kind,
                        outer_attempt=outer_attempt,
                        billing_disposition=disposition,
                        provider_error=provider_error,
                        usage_row_count=len(rows),
                        cost_eligible=bool(result_cost["eligible"]),
                        corrected_cost_usd=float(result_cost["total_usd"]),
                        result_path=result_artifact.path,
                        result_sha256=result_artifact.sha256,
                        reason=(
                            "Explicit provider-owned usage is retained but excluded from cost."
                            if provider_error
                            else "All provider usage, including schema-repair turns, is billable."
                        ),
                        basis=(
                            "Original attempt billing disposition, normalized result usage, "
                            "and the frozen public pricing card."
                        ),
                    )
                )

    corrected = _cost_for_usage(all_rows, selected_pricing)
    breakdown = _category_breakdown(corrected["attempts"], selected_pricing)
    category_sum = sum(
        item.cost_usd
        for item in (
            breakdown.uncached_input,
            breakdown.cache_read,
            breakdown.cache_creation,
            breakdown.output,
        )
    )
    if abs(category_sum - float(corrected["total_usd"])) > 1e-12:
        raise ValueError("corrected category costs do not add to the total")
    original_cost = summary.get("method_cost_usd")
    if not isinstance(original_cost, (int, float)) or isinstance(original_cost, bool):
        raise TypeError("historical summary has no numeric method_cost_usd")
    artifact_payload = sorted(
        (artifact.model_dump(mode="json") for artifact in source_artifacts),
        key=lambda item: (item["role"], item["path"]),
    )
    source_closure_hash = "sha256:" + hashlib.sha256(
        json.dumps(
            artifact_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
    ).hexdigest()
    per_pair = tuple(
        CorrectedPairCost(
            pair_id=pair_id,
            method_cell_count=int(values["method_cells"]),
            logical_call_count=int(values["logical_calls"]),
            provider_request_count=int(values["rows"]),
            corrected_cost_usd=float(values["cost"]),
        )
        for pair_id, values in sorted(pair_totals.items())
    )
    return CorrectedMethodCostAggregate(
        schema=AGGREGATE_SCHEMA,
        algorithm_version=ALGORITHM_VERSION,
        source_run_root=str(root),
        source_run_id=run_id,
        source_commit=source_commit,
        profile=profile,
        source_closure_hash=source_closure_hash,
        source_artifacts=tuple(source_artifacts),
        original_reported_method_cost_usd=float(original_cost),
        corrected_method_cost_usd=float(corrected["total_usd"]),
        correction_delta_usd=float(corrected["total_usd"]) - float(original_cost),
        pricing=selected_pricing.model_dump(mode="json"),
        method_cell_count=len(method_paths),
        logical_call_count=logical_call_count,
        outer_attempt_count=outer_attempt_count,
        provider_request_count=len(all_rows),
        billable_provider_request_count=sum(
            row.get("cost_counted") is not False for row in all_rows
        ),
        provider_error_exempt_request_count=sum(
            row.get("cost_counted") is False for row in all_rows
        ),
        schema_validation_failure_count=schema_validation_failure_count,
        cost_eligible=bool(corrected["eligible"]),
        breakdown=breakdown,
        per_pair=per_pair,
        result_receipts=tuple(result_receipts),
        reason=(
            "The historical runtime priced nested provider cache-read usage as ordinary "
            "input; this separate aggregate corrects only the token classification."
        ),
        basis=(
            "Immutable method/result bytes, original billing dispositions, shared "
            "utils.llm normalization, and the profile's frozen public pricing card."
        ),
    )


def write_corrected_method_cost(
    source_run_root: Path,
    output_path: Path,
) -> CorrectedMethodCostAggregate:
    """Build and write one standalone corrected aggregate without touching its source."""

    aggregate = build_corrected_method_cost(source_run_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(aggregate.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return aggregate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Re-price an immutable evidence-discovery method run."
    )
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for deterministic historical method cost correction."""

    args = _parser().parse_args(argv)
    aggregate = write_corrected_method_cost(args.source_run, args.output)
    print(
        json.dumps(
            {
                "source_run_id": aggregate.source_run_id,
                "original_reported_method_cost_usd": (
                    aggregate.original_reported_method_cost_usd
                ),
                "corrected_method_cost_usd": aggregate.corrected_method_cost_usd,
                "source_closure_hash": aggregate.source_closure_hash,
                "output": str(args.output.resolve()),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
