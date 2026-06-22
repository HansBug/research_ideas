#!/usr/bin/env python3
"""Validate seed_library first-source registry assets.

The repository intentionally keeps this validator small but evidence-oriented:
it checks registry/manifest required fields, manifest raw hashes, pairs.jsonl
source_asset_id/source_sha256 consistency, validation_summary count
consistency, and—when a supported locator type is used—verifies that the
extracted NL/STM text and hashes really round-trip to the committed raw asset.

At the moment the strongest supported raw-text trace is
``source_locator_type=parquet_row_columns``. Unsupported locator types are
accepted only for non-trace-verified rows; a row cannot count as trace-verified
or eligible unless this validator can independently check its raw locator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

BASE = Path(os.environ.get("SEED_LIBRARY_BASE", Path(__file__).resolve().parent.parent)).resolve()
ROLE_ENUM = {
    "final_pool_ready",
    "conditional_final_pool",
    "pipeline_only",
    "reference_only",
    "paper_reconstructable",
    "related_only",
    "excluded",
}
ASSET_STATUS_ENUM = {"downloaded", "partially_downloaded", "metadata_only", "blocked", "not_applicable"}
STORAGE_ENUM = {"committed", "local_only", "metadata_only", "skipped"}
DOWNLOAD_ENUM = {"downloaded", "skipped", "blocked", "metadata_only", "local_only"}


class RawTableCache:
    """Lazy cache for table-like raw assets used by locator validation."""

    def __init__(self) -> None:
        self._parquet: dict[Path, Any] = {}

    def parquet(self, path: Path):
        if path not in self._parquet:
            try:
                import pandas as pd
            except Exception as exc:  # pragma: no cover - environment guard
                raise RuntimeError("pandas/pyarrow are required for parquet locator validation") from exc
            self._parquet[path] = pd.read_parquet(path)
        return self._parquet[path]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(p: Path):
    return json.loads(p.read_text())


def iter_pairs(p: Path):
    if not p or str(p) == "." or not p.exists():
        return []
    rows = []
    with p.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def require(obj: dict, keys: list[str], label: str, errors: list[str]):
    for key in keys:
        if key not in obj:
            errors.append(f"{label} missing required field {key}")


def validate_registry_shape(reg: dict, errors: list[str]):
    require(
        reg,
        [
            "schema_version",
            "seed_id",
            "source_work",
            "asset_summary",
            "pair_sets",
            "reference_sets",
            "extracted_summary",
            "downstream_selection",
            "recommended_role",
            "blockers",
            "legacy_audit_refs",
        ],
        "registry",
        errors,
    )
    if reg.get("schema_version") != "seed-resource-registry.v1":
        errors.append("registry schema_version must be seed-resource-registry.v1")
    if reg.get("recommended_role") not in ROLE_ENUM:
        errors.append(f"unknown recommended_role {reg.get('recommended_role')}")
    asset_summary = reg.get("asset_summary", {})
    require(
        asset_summary,
        ["manifest_path", "first_source_status", "license_status", "redistribution_status", "version_pin"],
        "asset_summary",
        errors,
    )
    if asset_summary.get("first_source_status") not in ASSET_STATUS_ENUM:
        errors.append(f"unknown first_source_status {asset_summary.get('first_source_status')}")
    ds = reg.get("downstream_selection", {})
    require(
        ds,
        [
            "r2_smoke_recommendation",
            "source_coverage_class",
            "input_format_class",
            "conversion_pressure",
            "defect_risk_class",
            "selection_caveat",
        ],
        "downstream_selection",
        errors,
    )
    for i, pair_set in enumerate(reg.get("pair_sets", [])):
        require(
            pair_set,
            [
                "pair_set_id",
                "nl_role",
                "stm0_role",
                "raw_pair_count",
                "eligible_pair_count",
                "canonical_case_count",
                "reference_pair_count",
                "generation_actor",
                "generation_model_or_method",
                "stm_family",
                "stm_time_level",
                "eligibility_state",
                "must_not_count_as_generated",
                "excluded_outputs",
                "extracted_pairs_path",
            ],
            f"pair_sets[{i}]",
            errors,
        )
        if pair_set.get("eligibility_state") not in ROLE_ENUM:
            errors.append(f"pair_sets[{i}] unknown eligibility_state {pair_set.get('eligibility_state')}")


def validate_manifest_shape(manifest: dict, errors: list[str]):
    require(
        manifest,
        ["schema_version", "seed_id", "source_work", "manifest_created_at", "first_source_policy", "assets", "derived_assets", "skipped_assets"],
        "manifest",
        errors,
    )
    if manifest.get("schema_version") != "seed-assets-manifest.v1":
        errors.append("manifest schema_version must be seed-assets-manifest.v1")
    for i, asset in enumerate(manifest.get("assets", [])):
        require(
            asset,
            [
                "asset_id",
                "role",
                "source_url",
                "source_url_type",
                "download_status",
                "accessed_at",
                "local_path",
                "storage_mode",
                "license_status",
                "redistribution_status",
                "version_pin",
                "sha256",
                "bytes",
                "notes",
            ],
            f"assets[{i}]",
            errors,
        )
        if asset.get("download_status") not in DOWNLOAD_ENUM:
            errors.append(f"assets[{i}] unknown download_status {asset.get('download_status')}")
        if asset.get("storage_mode") not in STORAGE_ENUM:
            errors.append(f"assets[{i}] unknown storage_mode {asset.get('storage_mode')}")


def _parse_parquet_locator(locator: str) -> tuple[int, list[str]] | None:
    """Parse locator like 'row=0; columns=input,uml_code,reasoning'."""
    row_match = re.search(r"(?:^|;)\s*row\s*=\s*(\d+)\s*(?:;|$)", locator)
    cols_match = re.search(r"(?:^|;)\s*columns\s*=\s*([^;]+)", locator)
    if not row_match or not cols_match:
        return None
    cols = [c.strip() for c in cols_match.group(1).split(",") if c.strip()]
    return int(row_match.group(1)), cols


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def validate_pair_trace(seed_dir: Path, row: dict, asset: dict, raw_path: Path, cache: RawTableCache, errors: list[str]) -> bool:
    """Return whether this row is independently trace-verified.

    A row's self-reported ``trace_verified`` flag is treated as a claim to audit,
    not as evidence. For eligible count, the validator uses this function's
    result instead of the row's self-report.
    """

    pair_id = row.get("pair_id")
    locator_type = row.get("source_locator_type")
    locator = row.get("source_locator", "")

    if asset.get("storage_mode") != "committed" or asset.get("download_status") != "downloaded":
        if row.get("trace_verified"):
            errors.append(f"pair {pair_id} claims trace_verified but source asset is not committed/downloaded")
        return False

    if row.get("source_sha256") != sha256_file(raw_path):
        errors.append(f"pair {pair_id} source_sha256 mismatch")
        return False

    if locator_type != "parquet_row_columns":
        if row.get("trace_verified"):
            errors.append(f"pair {pair_id} claims trace_verified with unsupported locator type {locator_type}")
        return False

    parsed = _parse_parquet_locator(locator)
    if parsed is None:
        errors.append(f"pair {pair_id} invalid parquet locator: {locator}")
        return False
    row_index, columns = parsed
    try:
        table = cache.parquet(raw_path)
    except Exception as exc:
        errors.append(f"pair {pair_id} cannot read parquet raw asset {raw_path}: {exc}")
        return False
    if row_index < 0 or row_index >= len(table):
        errors.append(f"pair {pair_id} parquet row out of range: {row_index}")
        return False
    missing = [c for c in ("input", "uml_code") if c not in table.columns]
    if missing:
        errors.append(f"pair {pair_id} parquet raw missing required columns: {','.join(missing)}")
        return False
    for required_col in ("input", "uml_code"):
        if required_col not in columns:
            errors.append(f"pair {pair_id} locator columns missing {required_col}: {columns}")
            return False

    raw_nl = _as_text(table.iloc[row_index]["input"])
    raw_stm = _as_text(table.iloc[row_index]["uml_code"])
    ok = True
    if row.get("nl_text") != raw_nl:
        errors.append(f"pair {pair_id} nl_text does not match raw parquet row {row_index}")
        ok = False
    if row.get("stm0_text") != raw_stm:
        errors.append(f"pair {pair_id} stm0_text does not match raw parquet row {row_index}")
        ok = False
    expected_nl_hash = sha256_text(raw_nl)
    expected_stm_hash = sha256_text(raw_stm)
    if row.get("nl_sha256") != expected_nl_hash:
        errors.append(f"pair {pair_id} nl_sha256 mismatch: {row.get('nl_sha256')} != {expected_nl_hash}")
        ok = False
    if row.get("stm0_sha256") != expected_stm_hash:
        errors.append(f"pair {pair_id} stm0_sha256 mismatch: {row.get('stm0_sha256')} != {expected_stm_hash}")
        ok = False
    if row.get("source_local_path") and seed_dir / "assets" / row.get("source_local_path") != raw_path:
        errors.append(f"pair {pair_id} source_local_path does not match manifest raw path")
        ok = False
    return ok


def validate_seed(seed_id: str) -> int:
    seed_dir = BASE / seed_id
    reg_path = seed_dir / "seed_resource_registry.json"
    errors = []
    if not reg_path.exists():
        print(f"ERROR missing registry: {reg_path}", file=sys.stderr)
        return 1
    reg = load_json(reg_path)
    validate_registry_shape(reg, errors)
    manifest_rel = reg.get("asset_summary", {}).get("manifest_path", "")
    manifest_path = seed_dir / manifest_rel if manifest_rel else None
    if manifest_rel and (not manifest_path or not manifest_path.exists() or manifest_path.is_dir()):
        errors.append(f"manifest_path does not point to file: {manifest_rel}")
        manifest = {"assets": []}
    elif manifest_path:
        manifest = load_json(manifest_path)
        validate_manifest_shape(manifest, errors)
    else:
        manifest = {"assets": []}
    asset_by_id = {a["asset_id"]: a for a in manifest.get("assets", []) if "asset_id" in a}
    raw_hash_cache: dict[str, str] = {}
    for asset in manifest.get("assets", []):
        if asset.get("storage_mode") == "committed" and asset.get("download_status") == "downloaded":
            p = seed_dir / "assets" / asset.get("local_path", "")
            if not p.exists() or p.is_dir():
                errors.append(f"missing raw asset {asset.get('asset_id')}: {p}")
                continue
            actual = sha256_file(p)
            raw_hash_cache[asset.get("asset_id")] = actual
            if actual != asset.get("sha256"):
                errors.append(f"asset hash mismatch {asset.get('asset_id')}: {actual} != {asset.get('sha256')}")
    pairs_rel = reg.get("extracted_summary", {}).get("pairs_jsonl", "")
    pairs_path = seed_dir / pairs_rel if pairs_rel else Path("")
    pairs = iter_pairs(pairs_path)
    trace_verified = 0
    eligible = 0
    cache = RawTableCache()
    for row in pairs:
        aid = row.get("source_asset_id")
        asset = asset_by_id.get(aid)
        if not asset:
            errors.append(f"pair {row.get('pair_id')} unknown source_asset_id {aid}")
            continue
        raw_path = seed_dir / "assets" / asset.get("local_path", "")
        row_trace_verified = validate_pair_trace(seed_dir, row, asset, raw_path, cache, errors)
        if row.get("trace_verified") and not row_trace_verified:
            errors.append(f"pair {row.get('pair_id')} claims trace_verified but raw trace validation failed")
        if (not row.get("trace_verified")) and row_trace_verified:
            errors.append(f"pair {row.get('pair_id')} has valid raw trace but trace_verified is false")
        if row_trace_verified:
            trace_verified += 1
        if row_trace_verified and row.get("is_generated_stm0") and not row.get("is_reference") and not row.get("is_postprocessed"):
            eligible += 1
    vs_rel = reg.get("extracted_summary", {}).get("validation_summary", "")
    vs_path = seed_dir / vs_rel if vs_rel else Path("")
    if vs_path and str(vs_path) != "." and vs_path.exists():
        vs = load_json(vs_path)
        if vs.get("trace_verified_pair_count") != trace_verified:
            errors.append(f"validation_summary trace count mismatch: {vs.get('trace_verified_pair_count')} != {trace_verified}")
        if vs.get("eligible_generated_pair_count") != eligible:
            errors.append(f"validation_summary eligible count mismatch: {vs.get('eligible_generated_pair_count')} != {eligible}")
    if reg.get("extracted_summary", {}).get("eligible_generated_pair_count") != eligible:
        errors.append(f"registry eligible count mismatch: {reg.get('extracted_summary', {}).get('eligible_generated_pair_count')} != {eligible}")
    if reg.get("extracted_summary", {}).get("trace_verified_pair_count") != trace_verified:
        errors.append(f"registry trace count mismatch: {reg.get('extracted_summary', {}).get('trace_verified_pair_count')} != {trace_verified}")
    if reg.get("recommended_role") == "final_pool_ready":
        if eligible == 0:
            errors.append("final_pool_ready registry must have at least one eligible generated pair")
        if reg.get("asset_summary", {}).get("redistribution_status") in {"metadata_only", "unknown", "restricted"}:
            errors.append("final_pool_ready cannot use metadata_only/unknown/restricted redistribution status")
    if errors:
        for e in errors:
            print("ERROR", seed_id, e, file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "seed_id": seed_id,
                "pair_count": len(pairs),
                "trace_verified_pair_count": trace_verified,
                "eligible_generated_pair_count": eligible,
            },
            ensure_ascii=False,
        )
    )
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed_id", nargs="+")
    args = ap.parse_args()
    code = 0
    for seed in args.seed_id:
        code |= validate_seed(seed)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
