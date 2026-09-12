"""Summarize the pair-0029 Luna effort probe into a reproducible JSON artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from utils.llm import estimate_usage_cost_usd, load_llm_registry

EFFORTS = ("omitted", "none", "low", "medium", "high", "xhigh", "max")
EXPECTED_MODEL = "gpt-5.6-luna"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _requested_effort(label: str) -> str | None:
    return None if label == "omitted" else label


def _usage(usage: dict[str, Any]) -> dict[str, int]:
    return {
        key: int(usage.get(key) or 0)
        for key in ("input_tokens", "output_tokens", "reasoning_tokens", "total_tokens")
    }


def _observation_summary(
    observations: list[dict[str, Any]], pricing: Any
) -> dict[str, Any]:
    usage = {
        key: 0
        for key in ("input_tokens", "output_tokens", "reasoning_tokens", "total_tokens")
    }
    observed_models: set[str] = set()
    calls = len(observations)
    attempts = 0
    non_billable_provider_attempts = 0
    configured_cost_usd = 0.0
    for observation in observations:
        model = observation.get("observed_model")
        if isinstance(model, str):
            observed_models.add(model)
        for attempt in observation.get("attempts", []):
            attempts += 1
            if attempt.get("cost_counted") is not True:
                non_billable_provider_attempts += 1
                continue
            attempt_usage = attempt.get("usage") or {}
            for key in usage:
                usage[key] += int(attempt_usage.get(key) or 0)
            cost = estimate_usage_cost_usd(attempt_usage, pricing)
            if not cost["eligible"]:
                raise ValueError(f"unpriceable attempt: {cost['errors']}")
            configured_cost_usd += float(cost["total_usd"])
    return {
        "usage": usage,
        "configured_cost_usd": configured_cost_usd,
        "observed_models": sorted(observed_models),
        "llm_calls": calls,
        "attempts": attempts,
        "non_billable_provider_attempts": non_billable_provider_attempts,
    }


def _quality(judgement: dict[str, Any]) -> dict[str, Any]:
    rows = judgement["judgement"]
    ledger = rows["ledger_assessments"]
    emissions = rows["emission_assessments"]

    def hit_ids(cell: str) -> list[str]:
        return sorted(
            str(row["ledger_id"])
            for row in ledger
            if row.get(cell, {}).get("hit") is True
        )

    def emission_counts(arm: str) -> dict[str, Any]:
        selected = [
            row for row in emissions if str(row.get("cell", "")).startswith(f"{arm}_")
        ]
        false_positive_ids = sorted(
            str(row["emitted_id"])
            for row in selected
            if row.get("false_positive") is True
        )
        return {
            "emitted": len(selected),
            "false_positive": len(false_positive_ids),
            "false_positive_ids": false_positive_ids,
        }

    method_hit_ids = hit_ids("method_run1")
    baseline_hit_ids = hit_ids("baseline_run1")
    return {
        "ledger_total": len(ledger),
        "method_ledger_hits": len(method_hit_ids),
        "method_ledger_hit_ids": method_hit_ids,
        "baseline_ledger_hits": len(baseline_hit_ids),
        "baseline_ledger_hit_ids": baseline_hit_ids,
        "method_emissions": emission_counts("method"),
        "baseline_emissions": emission_counts("baseline"),
    }


def summarize(raw_root: Path, profile: str) -> dict[str, Any]:
    config = load_llm_registry().require(profile)
    if config.model != EXPECTED_MODEL:
        raise ValueError(f"expected {EXPECTED_MODEL}, got {config.model}")
    if config.pricing is None:
        raise ValueError(f"profile {profile!r} has no pricing")

    rows: list[dict[str, Any]] = []
    source_hashes: dict[str, str] = {}
    observed_models: set[str] = set()
    for label in EFFORTS:
        effort_root = raw_root / label
        baseline_path = effort_root / "baseline/run1/0029-luna-x1v2/record.json"
        method_path = effort_root / "method/run1/0029-luna/record.json"
        judge_manifest_path = effort_root / "judge-medium/manifest.json"
        judgement_path = effort_root / "judge-medium/0029.json"
        for path in (baseline_path, method_path, judge_manifest_path, judgement_path):
            source_hashes[str(path)] = _sha256(path)

        expected_effort = _requested_effort(label)
        baseline = _read_json(baseline_path)
        method = _read_json(method_path)
        judge_manifest = _read_json(judge_manifest_path)
        judgement = _read_json(judgement_path)

        if baseline.get("requested_effort") != expected_effort:
            raise ValueError(f"{label}: baseline requested_effort mismatch")
        if method.get("requested_effort") != expected_effort:
            raise ValueError(f"{label}: method requested_effort mismatch")
        if baseline.get("configured_model") != EXPECTED_MODEL:
            raise ValueError(f"{label}: baseline configured model mismatch")
        if baseline.get("observed_model") != EXPECTED_MODEL:
            raise ValueError(f"{label}: baseline observed model mismatch")

        baseline_usage = _usage(baseline["usage"])
        baseline_cost = estimate_usage_cost_usd(baseline["usage"], config.pricing)
        if not baseline_cost["eligible"]:
            raise ValueError(
                f"{label}: unpriceable baseline: {baseline_cost['errors']}"
            )
        method_summary = _observation_summary(
            method["llm_observations"], config.pricing
        )
        judge_observations = [
            observation
            for pair in judge_manifest["pairs"]
            for observation in pair.get("observations", [])
        ]
        judge_summary = _observation_summary(judge_observations, config.pricing)

        row_models = {
            baseline["observed_model"],
            *method_summary["observed_models"],
            *judge_summary["observed_models"],
        }
        observed_models.update(row_models)
        if row_models != {EXPECTED_MODEL}:
            raise ValueError(
                f"{label}: unexpected observed models: {sorted(row_models)}"
            )
        if judge_manifest.get("requested_effort") != "medium":
            raise ValueError(f"{label}: judge effort was not fixed at medium")

        rows.append(
            {
                "effort_label": label,
                "requested_effort": expected_effort,
                "baseline": {
                    "usage": baseline_usage,
                    "elapsed_seconds": float(baseline["elapsed_ms"]) / 1000,
                    "configured_cost_usd": float(baseline_cost["total_usd"]),
                    "configured_model": baseline["configured_model"],
                    "observed_model": baseline["observed_model"],
                },
                "method": {
                    **method_summary,
                    "elapsed_seconds": float(method["elapsed_ms"]) / 1000,
                },
                "judge": {
                    **judge_summary,
                    "requested_effort": judge_manifest["requested_effort"],
                    "elapsed_seconds": float(judge_manifest["elapsed_seconds"]),
                    "status": judgement["status"],
                },
                "quality": _quality(judgement),
            }
        )

    return {
        "schema": "paper1.luna_effort_pair_probe.v2",
        "experiment_date": "2026-08-20",
        "pair": "0029",
        "raw_root": str(raw_root),
        "profile": {
            "name": profile,
            "adapter": config.adapter,
            "configured_model": config.model,
            "fingerprint": config.fingerprint(),
            "pricing": config.pricing.model_dump(mode="json"),
        },
        "effort": {
            "supported": ["none", "low", "medium", "high", "xhigh", "max"],
            "omitted_request_value": None,
            "official_effective_default": "medium",
        },
        "billing": {
            "reasoning_is_output_subset": True,
            "formula": "input classes + output_tokens; do not add reasoning_tokens again",
        },
        "observed_models": sorted(observed_models),
        "sol_observed": "gpt-5.6-sol" in observed_models,
        "rows": rows,
        "source_sha256": source_hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--profile", default=EXPECTED_MODEL)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = summarize(args.raw_root, args.profile)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
