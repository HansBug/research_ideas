#!/usr/bin/env python3
"""Build and validate the provider-free Paper1 method-cost audit for final talk v1.

The script reads archived receipts only.  It never imports a provider adapter,
replays a method cell, or changes a frozen decision, relation, or raw record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml


ARCHIVE_RELATIVE = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline")
OUTPUT_RELATIVE = Path("derived/final_talk_cost_section7_v1")
PRICE_CARD_RELATIVE = Path(".llmconfig.example.yml")
PRICE_CARD_PROFILE = "gpt-5.6-luna"
PRICE_SOURCE_RELATIVES = (
    PRICE_CARD_RELATIVE,
    Path("utils/llm/pricing.py"),
    Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src/paper_stm_evaluation/cost_correction.py"),
)
TOKEN_CLASSES = (
    "uncached_input",
    "cache_read",
    "cache_creation",
    "output",
)
EXPECTED_RATES = {
    "uncached_input": Decimal("0.20"),
    "cache_read": Decimal("0.02"),
    "cache_creation": Decimal("0.25"),
    "output": Decimal("1.20"),
}
EXPECTED_PRICING_PROVENANCE = {
    "source_url": "https://developers.openai.com/api/docs/pricing",
    "verified_on": "2026-08-18",
    "basis": "official_list_price",
}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def repository_root(archive: Path) -> Path:
    root = archive.resolve().parents[3]
    if root / ARCHIVE_RELATIVE != archive.resolve():
        raise ValueError(f"archive root is not the canonical Paper1 archive: {archive}")
    return root


def source_artifact(path: Path, *, root: str, relative_to: Path, role: str) -> dict[str, Any]:
    return {
        "root": root,
        "path": path.relative_to(relative_to).as_posix(),
        "role": role,
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
    }


def source_closure_sha256(sources: list[dict[str, Any]]) -> str:
    normalized = sorted(
        (
            {
                "root": row["root"],
                "path": row["path"],
                "role": row["role"],
                "sha256": row["sha256"],
                "size_bytes": row["size_bytes"],
            }
            for row in sources
        ),
        key=lambda row: (row["root"], row["path"], row["role"]),
    )
    if len({(row["root"], row["path"], row["role"]) for row in normalized}) != len(normalized):
        raise ValueError("source closure contains duplicate source paths")
    encoded = json.dumps(normalized, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def frozen_pricing(archive: Path) -> tuple[dict[str, Any], dict[str, Decimal], list[dict[str, Any]]]:
    """Read the published price card and return the four frozen billing rates."""

    root = repository_root(archive)
    card_path = root / PRICE_CARD_RELATIVE
    raw_card = yaml.safe_load(card_path.read_text(encoding="utf-8"))
    if not isinstance(raw_card, dict):
        raise TypeError(f"price card is not a mapping: {card_path}")
    profiles = raw_card.get("profiles")
    if not isinstance(profiles, dict) or not isinstance(profiles.get(PRICE_CARD_PROFILE), dict):
        raise ValueError(f"price card has no {PRICE_CARD_PROFILE!r} profile")
    profile = profiles[PRICE_CARD_PROFILE]
    pricing = profile.get("pricing")
    if not isinstance(pricing, dict) or profile.get("model") != PRICE_CARD_PROFILE:
        raise ValueError("frozen profile/model/pricing closure failed")
    prices = pricing.get("prices")
    if not isinstance(prices, dict):
        raise ValueError("frozen profile has no price mapping")
    fields = {
        "uncached_input": "input_usd_per_million_tokens",
        "cache_read": "cache_read_usd_per_million_tokens",
        "cache_creation": "cache_write_usd_per_million_tokens",
        "output": "output_usd_per_million_tokens",
    }
    rates: dict[str, Decimal] = {}
    for token_class, field in fields.items():
        value = prices.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"frozen price card has no numeric {field}")
        rates[token_class] = Decimal(str(value))
    source_url = pricing.get("source_url")
    verified_on = pricing.get("verified_on")
    basis = pricing.get("basis")
    if rates != EXPECTED_RATES:
        raise ValueError(f"frozen pricing values changed: {rates}")
    if {
        "source_url": source_url,
        "verified_on": str(verified_on),
        "basis": basis,
    } != EXPECTED_PRICING_PROVENANCE:
        raise ValueError("frozen price-card provenance changed")
    sources = [
        source_artifact(
            root / relative,
            root="repository",
            relative_to=root,
            role="pricing_card" if relative == PRICE_CARD_RELATIVE else "pricing_implementation",
        )
        for relative in PRICE_SOURCE_RELATIVES
    ]
    return ({
        "model": PRICE_CARD_PROFILE,
        "source_url": source_url,
        "verified_on": str(verified_on),
        "basis": basis,
        "source_artifacts": sources,
        "source_closure_sha256": source_closure_sha256(sources),
        "usd_per_million_tokens": {key: f"{value:.2f}" for key, value in rates.items()},
        "formula": "uncached_input=(input_tokens-cache_read-cache_creation); cost=uncached_input*uncached_input_rate/1M+cache_read*cache_read_rate/1M+cache_creation*cache_creation_rate/1M+output*output_rate/1M; output already includes reasoning tokens",
    }, rates, sources)


def cost(tokens: dict[str, int], rates: dict[str, Decimal]) -> Decimal:
    return sum(Decimal(tokens[key]) * rates[key] / Decimal(1_000_000) for key in TOKEN_CLASSES)


def token_breakdown(rows: list[dict[str, Any]]) -> dict[str, int]:
    values = {key: 0 for key in TOKEN_CLASSES}
    for row in rows:
        categories = row["categories"]
        values["uncached_input"] += int(categories["input"]["tokens"])
        values["cache_read"] += int(categories["cache_read"]["tokens"])
        values["cache_creation"] += int(categories["cache_write"]["tokens"])
        values["output"] += int(categories["output"]["tokens"])
    return values


def baseline(archive: Path, rates: dict[str, Decimal]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root = archive / "raw/x1v2_baseline/method"
    records = sorted(root.rglob("record.json"))
    if len(records) != 162:
        raise ValueError(f"expected 162 baseline records, found {len(records)}")
    usage_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    for path in records:
        record = load(path)
        sources.append(source_artifact(path, root="archive", relative_to=archive, role="baseline_method_receipt"))
        usage = record.get("usage")
        if not isinstance(usage, dict) or usage.get("status") != "completed":
            raise ValueError(f"baseline final record lacks a completed usage receipt: {path}")
        usage_rows.append({
            "categories": {
                "input": {"tokens": int(usage["input_tokens"]) - int(usage.get("cache_read_input_tokens") or 0) - int(usage.get("cache_creation_input_tokens") or 0)},
                "cache_read": {"tokens": int(usage.get("cache_read_input_tokens") or 0)},
                "cache_write": {"tokens": int(usage.get("cache_creation_input_tokens") or 0)},
                "output": {"tokens": int(usage["output_tokens"])},
            }
        })
        for attempt in record.get("attempts", []):
            if not isinstance(attempt, dict):
                raise TypeError(f"invalid attempt in {path}")
            attempts.append(attempt)
            if attempt.get("status") == "schema_error" and attempt.get("billing_disposition") == "counted":
                missing.append({
                    "cell_id": str(record["cell_id"]),
                    "pair_id": str(record["pair_id"]),
                    "round": str(record["round"]),
                    "attempt": str(attempt["attempt"]),
                    "status": "schema_error",
                    "billing_disposition": "counted",
                    "reason": "The archived record retains a billable schema-retry attempt but no provider usage receipt for that first attempt.",
                    "recoverability": "not recoverable from the archived record.json surface",
                })
    tokens = token_breakdown(usage_rows)
    subtotal = cost(tokens, rates)
    dispositions = Counter(str(item.get("billing_disposition")) for item in attempts)
    if len(attempts) != 223 or dispositions != Counter({"counted": 163, "provider_error_retry_exempt": 60}):
        raise ValueError(f"unexpected baseline attempt closure: {len(attempts)} {dict(dispositions)}")
    if len(missing) != 1:
        raise ValueError(f"expected one billable baseline usage gap, found {len(missing)}")
    if tokens != {"uncached_input": 633844, "cache_read": 143744, "cache_creation": 0, "output": 79658}:
        raise ValueError(f"unexpected baseline token totals: {tokens}")
    if subtotal != Decimal("0.22523328"):
        raise ValueError(f"unexpected baseline subtotal: {subtotal}")
    return ({
        "side": "baseline",
        "method_cells": 162,
        "receipt_scope": "162 final successful method-cell records; provider-error retry attempts are exempt under the frozen retry policy.",
        "attempts": {"total": len(attempts), "counted": dispositions["counted"], "provider_error_retry_exempt": dispositions["provider_error_retry_exempt"], "schema_error_billable_missing_usage": len(missing)},
        "tokens": tokens,
        "known_recorded_subtotal_usd": f"{subtotal:.8f}",
        "complete_method_cost_usd": None,
        "method_cost_eligible": False,
        "missing_usage": missing,
        "complete_cost_expression": f"${subtotal:.8f} + missing schema-attempt cost",
        "interpretation": "The known recorded subtotal is not a complete baseline method cost. The missing billable schema-attempt usage must not be imputed as zero.",
    }, sources)


def current(archive: Path, rates: dict[str, Decimal]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root = archive / "raw/v60_current/method"
    summary_path = root / "summary.json"
    summary = load(summary_path)
    cells = sorted((root / "method").rglob("round-*.json"))
    if len(cells) != 162:
        raise ValueError(f"expected 162 current cells, found {len(cells)}")
    rows: list[dict[str, Any]] = []
    sources = [source_artifact(summary_path, root="archive", relative_to=archive, role="current_method_summary")]
    logical_calls = 0
    cost_attempts = 0
    provider_error_exempt = 0
    for path in cells:
        cell = load(path)
        sources.append(source_artifact(path, root="archive", relative_to=archive, role="current_method_receipt"))
        calls = cell.get("llm_calls")
        if not isinstance(calls, list):
            raise ValueError(f"current cell has no llm_calls list: {path}")
        logical_calls += len(calls)
        for call in calls:
            result = call.get("cost", {})
            for attempt in result.get("attempts", []):
                if not attempt.get("eligible"):
                    raise ValueError(f"current cost attempt is ineligible: {path}")
                disposition = attempt.get("billing_disposition")
                if disposition == "provider_error_retry_exempt":
                    provider_error_exempt += 1
                    continue
                if disposition != "billable":
                    raise ValueError(f"unexpected current billing disposition: {path}")
                rows.append(attempt)
                cost_attempts += 1
    tokens = token_breakdown(rows)
    total = cost(tokens, rates)
    reported = Decimal(str(summary["method_cost_usd"]))
    if total != reported.quantize(Decimal("0.00000001")):
        raise ValueError(f"current receipt cost does not close: {total} != {reported}")
    return ({
        "side": "ours",
        "method_cells": 162,
        "run_id": summary["run_id"],
        "source_commit": summary["source_commit"],
        "profile": summary["profile"],
        "logical_calls": logical_calls,
        "billable_provider_attempts": cost_attempts,
        "provider_error_retry_exempt_attempts": provider_error_exempt,
        "tokens": tokens,
        "complete_method_cost_usd": f"{total:.8f}",
        "method_cost_eligible": True,
        "interpretation": "All billable current method-call receipts close under the frozen pricing card.",
    }, sources)


def write_outputs(archive: Path, payload: dict[str, Any], sources: list[dict[str, str]]) -> None:
    output = archive / OUTPUT_RELATIVE
    audit = output / "method_cost_audit_v1.json"
    summary = output / "cost_summary_v1.json"
    tsv = output / "cost_summary_v1.tsv"
    readme = output / "README.md"
    manifest = output / "manifest_v1.json"
    dump(audit, payload)
    dump(summary, {key: payload[key] for key in ("schema", "scope", "pricing", "sides", "historical_misbound_audit", "execution_boundary")})
    tsv.write_text(
        "side\tmethod_cells\tcost_status\tknown_recorded_subtotal_usd\tcomplete_method_cost_usd\tmethod_cost_eligible\n"
        f"ours\t162\tcomplete\t\t{payload['sides']['ours']['complete_method_cost_usd']}\ttrue\n"
        f"baseline\t162\tknown_recorded_subtotal\t{payload['sides']['baseline']['known_recorded_subtotal_usd']}\t\tfalse\n",
        encoding="utf-8",
    )
    readme.write_text(
        "# Final talk method-cost audit v1\n\n"
        "This evaluation-only audit reads the archived method provider-usage receipts for the frozen 162 cells on each side. It excludes evaluator, human review, CPU, storage, waiting, and development costs. `output_tokens` already include reasoning tokens and are charged once.\n\n"
        f"The frozen `{payload['pricing']['model']}` price card records `{payload['pricing']['source_url']}`, verified on `{payload['pricing']['verified_on']}`, with `basis={payload['pricing']['basis']}`. Its three source artifacts and `source_closure_sha256` are recorded in `method_cost_audit_v1.json#/pricing`.\n\n"
        "`ours` has a complete receipt closure: `$7.18277320`. `baseline` has a known recorded subtotal: `$0.22523328`; one billed schema-error attempt has no retained usage receipt, so its complete cost is `$0.22523328 + missing schema-attempt cost`, not an exact total. The corresponding subtotal ratio is at most `31.8904x`, not a complete ratio.\n\n"
        "Rebuild: `python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_final_talk_cost_section7_v1.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline`\n\n"
        "Validate: append `--validate` to the same command.\n",
        encoding="utf-8",
    )
    output_hashes = {path.name: sha256(path) for path in (audit, summary, tsv, readme)}
    dump(manifest, {
        "schema": "paper1.final-talk-cost-section7.manifest.v1",
        "generated_at_utc": payload["generated_at_utc"],
        "generator": "build_final_talk_cost_section7_v1.py",
        "outputs": output_hashes,
        "source_artifacts": sources,
        "source_closure_sha256": source_closure_sha256(sources),
        "execution_boundary": payload["execution_boundary"],
        "purpose": "Provider-free receipt audit for Paper1 final-talk cost accounting; does not modify raw records or evaluation decisions.",
    })


def build(archive: Path) -> dict[str, Any]:
    pricing, rates, pricing_sources = frozen_pricing(archive)
    ours, current_sources = current(archive, rates)
    baseline_side, baseline_sources = baseline(archive, rates)
    historical = load(archive / "raw/x1v2_baseline/method/corrected_cost_audit.json")
    if historical.get("source_run_id") != "90d1c41e000000000000000000000162" or Decimal(str(historical.get("corrected_method_cost_usd"))).quantize(Decimal("0.00000001")) != Decimal("6.77501040"):
        raise ValueError("historical misbound cost audit identity changed")
    ratio = Decimal(ours["complete_method_cost_usd"]) / Decimal(baseline_side["known_recorded_subtotal_usd"])
    payload = {
        "schema": "paper1.final-talk-method-cost-audit.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": {"per_side_method_cells": 162, "matrix": "54 pair x 3 rounds", "cost_object": "actual method-generation provider inference attempts with retained usage receipts", "excluded": ["evaluator", "human review", "CPU", "storage", "network", "development time", "retry waiting"]},
        "pricing": pricing,
        "sides": {"ours": ours, "baseline": baseline_side},
        "comparison": {"known_subtotal_ratio_upper_bound": f"{ratio:.4f}", "interpretation": "Because the baseline denominator omits one positive but unknown billed schema-attempt cost, this ratio is an upper bound under the recorded subtotal, not a complete exact ratio."},
        "historical_misbound_audit": {"path": "raw/x1v2_baseline/method/corrected_cost_audit.json", "corrected_method_cost_usd": "6.77501040", "source_run_id": historical["source_run_id"], "source_commit": historical["source_commit"], "status": "historical_current_evidence_discovery_audit_misbound_to_baseline_archive", "replacement": "derived/final_talk_cost_section7_v1/method_cost_audit_v1.json#/sides/baseline"},
        "execution_boundary": {"provider_calls": 0, "billable_calls": 0, "method_reruns": 0, "judge_reruns": 0, "replay_runs": 0, "raw_modified": False},
    }
    historical_source = source_artifact(
        archive / "raw/x1v2_baseline/method/corrected_cost_audit.json",
        root="archive",
        relative_to=archive,
        role="archival_cost_provenance",
    )
    write_outputs(
        archive,
        payload,
        current_sources + baseline_sources + [historical_source] + pricing_sources,
    )
    return payload


def resolve_source_artifact(archive: Path, source: dict[str, Any]) -> Path:
    root = source.get("root")
    path = source.get("path")
    role = source.get("role")
    digest = source.get("sha256")
    size_bytes = source.get("size_bytes")
    if (
        root not in {"archive", "repository"}
        or not isinstance(path, str)
        or not isinstance(role, str)
        or not role
        or not isinstance(digest, str)
        or not isinstance(size_bytes, int)
        or size_bytes < 0
    ):
        raise ValueError("invalid source artifact record")
    base = archive if root == "archive" else repository_root(archive)
    resolved = (base / path).resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise ValueError(f"source artifact escapes declared root: {source}")
    if not resolved.is_file():
        raise ValueError(f"source artifact is missing: {source}")
    return resolved


def validate_source_hashes(archive: Path, sources: list[dict[str, Any]]) -> None:
    for source in sources:
        resolved = resolve_source_artifact(archive, source)
        if sha256(resolved) != source["sha256"]:
            raise ValueError(f"source hash changed: {source['root']}:{source['path']}")
        if resolved.stat().st_size != source["size_bytes"]:
            raise ValueError(f"source size changed: {source['root']}:{source['path']}")


def validate(archive: Path) -> None:
    archive = archive.resolve()
    output = archive / OUTPUT_RELATIVE
    audit = load(output / "method_cost_audit_v1.json")
    summary = load(output / "cost_summary_v1.json")
    for key in ("schema", "scope", "pricing", "sides", "historical_misbound_audit", "execution_boundary"):
        if audit[key] != summary[key]:
            raise ValueError(f"audit and summary {key} payloads differ")
    expected_pricing, rates, expected_pricing_sources = frozen_pricing(archive)
    if audit["pricing"] != expected_pricing:
        raise ValueError("audit pricing does not match the frozen price card")
    if audit["pricing"]["source_artifacts"] != expected_pricing_sources:
        raise ValueError("audit price-source artifact closure changed")
    validate_source_hashes(archive, expected_pricing_sources)
    if audit["pricing"]["source_closure_sha256"] != source_closure_sha256(expected_pricing_sources):
        raise ValueError("audit price-source closure hash changed")
    expected = {"ours": "7.18277320", "baseline": "0.22523328"}
    if audit["sides"]["ours"]["complete_method_cost_usd"] != expected["ours"]:
        raise ValueError("current method cost changed")
    if audit["sides"]["baseline"]["known_recorded_subtotal_usd"] != expected["baseline"] or audit["sides"]["baseline"]["method_cost_eligible"]:
        raise ValueError("baseline subtotal/ineligibility changed")
    if audit["execution_boundary"] != {"provider_calls": 0, "billable_calls": 0, "method_reruns": 0, "judge_reruns": 0, "replay_runs": 0, "raw_modified": False}:
        raise ValueError("execution boundary changed")
    if f"{cost(audit['sides']['ours']['tokens'], rates):.8f}" != expected["ours"]:
        raise ValueError("current receipt arithmetic no longer closes under the frozen price card")
    if f"{cost(audit['sides']['baseline']['tokens'], rates):.8f}" != expected["baseline"]:
        raise ValueError("baseline receipt arithmetic no longer closes under the frozen price card")
    manifest = load(output / "manifest_v1.json")
    for name, digest in manifest["outputs"].items():
        if sha256(output / name) != digest:
            raise ValueError(f"stale output hash: {name}")
    sources = manifest.get("source_artifacts")
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest has no source artifacts")
    validate_source_hashes(archive, sources)
    if manifest.get("source_closure_sha256") != source_closure_sha256(sources):
        raise ValueError("manifest source closure hash changed")
    manifest_pricing_sources = [source for source in sources if source.get("root") == "repository"]
    if manifest_pricing_sources != expected_pricing_sources:
        raise ValueError("manifest price-source artifacts do not close")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if args.validate:
        validate(args.archive_root)
    else:
        result = build(args.archive_root)
        print(json.dumps({"status": "PASS", "ours_complete_usd": result["sides"]["ours"]["complete_method_cost_usd"], "baseline_known_recorded_subtotal_usd": result["sides"]["baseline"]["known_recorded_subtotal_usd"], **result["execution_boundary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
