#!/usr/bin/env python3
"""Validate seed_library first-source registry assets.

The repository intentionally keeps this validator small but evidence-oriented:
it checks registry/manifest required fields, manifest raw hashes, pairs.jsonl
source_asset_id/source_sha256 consistency, validation_summary count
consistency, and—when a supported locator type is used—verifies that the
extracted NL/STM text and hashes really round-trip to the committed raw asset.

At the moment the strongest supported raw-text traces are:

- ``source_locator_type=parquet_row_columns`` for HF/parquet style datasets.
- ``source_locator_type=xlsx_sheet_row_columns`` for spreadsheet rows such as
  Google Drive workbook exports.
- ``source_locator_type=zip_python_symbol_and_text_file`` for a committed ZIP
  asset where the NL comes from a Python string symbol and ``STM_0`` comes from
  a text file member in the same ZIP.
- ``source_locator_type=zip_member_pair`` for a committed ZIP asset where both
  NL and ``STM_0`` are stored as explicit archive members.

Unsupported locator types are accepted only for non-trace-verified rows; a row
cannot count as trace-verified or eligible unless this validator can
independently check its raw locator.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:  # Optional in old local envs, required by requirements.txt for CI.
    from jsonschema import Draft202012Validator
except Exception:  # pragma: no cover - dependency guard
    Draft202012Validator = None

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
LICENSE_STATUS_ENUM = {
    "clear",
    "paper_only",
    "unknown",
    "missing",
    "restricted",
    "proprietary",
    "not_applicable",
    "paper_public_resource",
}
REDISTRIBUTION_STATUS_ENUM = {
    "redistributable",
    "local_only",
    "metadata_only",
    "restricted",
    "unknown",
    "not_applicable",
    "cite_original_work",
}
R2_SMOKE_ENUM = {
    "prefer",
    "usable_with_caveat",
    "rerun_required",
    "do_not_use_as_seed",
    "reference_only",
}
RESOURCE_CATEGORY_ENUM = {
    "first_source_nl_stm",
    "nl_only",
    "nl_code_reproducible",
    "reference_only",
    "paper_reconstructable",
    "related_only",
    "excluded",
}
RESOURCE_CATEGORY_LABEL = {
    "first_source_nl_stm": "NL+STM一手",
    "nl_only": "仅NL",
    "nl_code_reproducible": "NL+源码可复跑",
    "reference_only": "仅参考STM",
    "paper_reconstructable": "论文可重建",
    "related_only": "仅相关",
    "excluded": "排除",
}
SOURCE_CODE_AVAILABILITY_ENUM = {
    "available_pinned",
    "available_unpinned",
    "partial_or_snippet",
    "not_published",
    "blocked",
    "not_applicable",
    "unknown",
}
SOURCE_CODE_LABEL = {
    "available_pinned": "🟢固定源码",
    "available_unpinned": "🟡源码未冻",
    "partial_or_snippet": "🟠片段/部分",
    "not_published": "🔴未公开",
    "blocked": "❓受阻",
    "not_applicable": "⚪不适用",
    "unknown": "❓待核",
}
PAPER_USES_LLM_ENUM = {"yes", "no", "possible", "not_applicable", "unknown"}
LLM_AVAILABILITY_ENUM = {
    "available_same_model",
    "available_alias_or_successor",
    "api_discontinued",
    "proxy_or_compatible_endpoint_required",
    "local_weight_available",
    "local_weight_or_proxy_available",
    "mixed_available_and_retired",
    "not_applicable",
    "unknown",
}
LLM_AVAILABILITY_LABEL = {
    "available_same_model": "🟢原模型可用",
    "available_alias_or_successor": "🟡继任/别名",
    "api_discontinued": "🔴已退役",
    "proxy_or_compatible_endpoint_required": "🟠需代理/替代",
    "local_weight_available": "🟢开权重可用",
    "local_weight_or_proxy_available": "🟡本地/代理可用",
    "mixed_available_and_retired": "🟡混合",
    "not_applicable": "⚪不适用",
    "unknown": "❓待核",
}
CODE_REPRODUCIBILITY_ENUM = {
    "not_applicable",
    "not_attempted",
    "initial_generation_smoke_ok_via_openai_compatible_proxy",
    "single_system_smoke_ok_via_ollama_compatible_proxy",
    "blocked",
    "failed",
}

UNKNOWN_COUNT_VALUES = {"unknown", "未知"}

ROLE_EMOJI_BY_ROLE = {
    "final_pool_ready": "🟢",
    "conditional_final_pool": "🟡",
    "pipeline_only": "🟠",
    "reference_only": "🔵",
    "paper_reconstructable": "⚪",
    "related_only": "🔴",
    "excluded": "🔴",
}


def _strip_md(cell: str) -> str:
    """Return a compact cell value for simple REGISTRY.md table checks."""

    return cell.strip().replace("<br>", "\n")


def _extract_registry_seed_id(cell: str) -> str | None:
    """Extract seed_id from a REGISTRY.md first column cell.

    Supported forms are `` `seed-id` `` and ``[`seed-id`](./seed-id/assets/README.md)``.
    """

    link_match = re.search(r"\[`([^`]+)`\]\(([^)]+)\)", cell)
    if link_match:
        return link_match.group(1)
    code_match = re.search(r"`([^`]+)`", cell)
    if code_match:
        return code_match.group(1)
    return None


def _parse_markdown_table(path: Path, heading: str) -> tuple[list[str], list[dict[str, str]]]:
    """Parse the first markdown table after ``heading``.

    This intentionally supports only the simple pipe-table shape used by
    REGISTRY.md; it is not a general Markdown parser.
    """

    lines = path.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return [], []
    header_index = None
    for i in range(start, len(lines)):
        if lines[i].lstrip().startswith("| "):
            header_index = i
            break
    if header_index is None or header_index + 1 >= len(lines):
        return [], []
    headers = [h.strip() for h in lines[header_index].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.lstrip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return headers, rows


def _pair_set_nl_count_label(reg: dict[str, Any]) -> str:
    """Derive the human REGISTRY 'NL 数' label from structured registry facts."""

    if not reg.get("pair_sets"):
        return "0 / 未知"
    # Current R2 registries have one pair set per seed.  If future entries carry
    # multiple sets, use source_inventory when present; otherwise sum best-known
    # raw/unique fields conservatively.
    inv = reg.get("source_inventory", {})
    if "raw_nl_count" in inv and "unique_nl_count" in inv:
        return f"{inv['raw_nl_count']} / {inv['unique_nl_count']}"
    raw_total = 0
    unique_total = 0
    raw_known = False
    unique_known = False
    for pair_set in reg.get("pair_sets", []):
        counts = pair_set.get("nl_count", {})
        raw = (
            counts.get("raw")
            or counts.get("raw_rows")
            or counts.get("raw_requirements")
            or counts.get("raw_nl_descriptions_in_zip")
        )
        unique = (
            counts.get("unique")
            or counts.get("unique_requirement_descriptions")
            or counts.get("unique_requirements")
            or counts.get("unique_nl_descriptions_in_zip")
        )
        if isinstance(raw, int):
            raw_total += raw
            raw_known = True
        if isinstance(unique, int):
            unique_total += unique
            unique_known = True
    raw_label = str(raw_total) if raw_known else "0"
    unique_label = str(unique_total) if unique_known else "未知"
    return f"{raw_label} / {unique_label}"


def _nl_only_label(reg: dict[str, Any]) -> str:
    inv = reg.get("source_inventory", {})
    if "nl_only_count" in inv and "nl_only_unique_count" in inv:
        count = inv["nl_only_count"]
        unique = inv["nl_only_unique_count"]
        if count in {"unknown", "未知"} and unique in {"unknown", "未知"}:
            return "未知 / 未知"
        return f"{count} / {unique}"
    if not reg.get("pair_sets"):
        return "未知 / 未知"
    total = 0
    known = False
    for pair_set in reg.get("pair_sets", []):
        counts = pair_set.get("nl_count", {})
        value = (
            counts.get("nl_only_without_generated_output")
            or counts.get("nl_only_generation_failure")
            or counts.get("nl_only_pipeline_requirements")
        )
        if isinstance(value, int):
            total += value
            known = True
    if known:
        return f"{total} / {total}"
    eligible = reg.get("extracted_summary", {}).get("eligible_generated_pair_count")
    raw = None
    label = _pair_set_nl_count_label(reg)
    if " / " in label:
        maybe_raw = label.split(" / ", 1)[0]
        if maybe_raw.isdigit():
            raw = int(maybe_raw)
    if isinstance(raw, int) and isinstance(eligible, int):
        value = max(0, raw - eligible)
        return f"{value} / {value}"
    return "未知 / 未知"


def _reference_count(reg: dict[str, Any]) -> int:
    refs = sum(int(r.get("reference_pair_count", 0)) for r in reg.get("reference_sets", []))
    if refs:
        return refs
    return sum(int(p.get("reference_pair_count", 0)) for p in reg.get("pair_sets", []))


def _count_value_from_nl_count(pair_set: dict[str, Any], *keys: str) -> Any:
    counts = pair_set.get("nl_count", {})
    for key in keys:
        if key in counts:
            return counts[key]
    return None


def _sum_known_counts(values: list[Any]) -> Any:
    if not values:
        return None
    if all(isinstance(v, int) for v in values):
        return sum(values)
    if any(v in UNKNOWN_COUNT_VALUES for v in values):
        return "unknown"
    return None


def _normalise_nl(text: Any) -> str:
    return " ".join(_as_text(text).split())


def _unknown_equivalent(value: Any) -> bool:
    return value in UNKNOWN_COUNT_VALUES


def _compare_inventory_count(
    seed_id: str,
    key: str,
    actual: Any,
    expected: Any,
    errors: list[str],
) -> None:
    if expected is None:
        return
    if expected == "unknown":
        if not _unknown_equivalent(actual):
            errors.append(f"source_inventory {key} mismatch for {seed_id}: {actual} != {expected}")
        return
    if actual != expected:
        errors.append(f"source_inventory {key} mismatch for {seed_id}: {actual} != {expected}")


def validate_registry_markdown_row(seed_id: str, reg: dict[str, Any], seed_dir: Path, errors: list[str]) -> None:
    """Check REGISTRY.md's human-facing row against structured facts.

    The JSON + raw assets remain the machine source of truth.  This check exists
    because REGISTRY.md is the human-facing decision table; stale counts or links
    would mislead R2 sample selection even if raw trace validation still passes.
    """

    registry_md = BASE / "REGISTRY.md"
    if not registry_md.exists():
        return
    headers, rows = _parse_markdown_table(registry_md, "## 2. 一手资源主表")
    if not rows:
        errors.append("REGISTRY.md missing parsable §2 resource table")
        return
    required_headers = {
        "条目",
        "角色",
        "资源类别",
        "源码",
        "论文LLM",
        "NL 数",
        "可计生成对",
        "已回溯验证",
        "参考解",
        "NL-only",
        "结构化记录",
        "备注",
    }
    missing_headers = required_headers.difference(headers)
    if missing_headers:
        errors.append(f"REGISTRY.md table missing required columns: {sorted(missing_headers)}")
        return
    row = next((r for r in rows if _extract_registry_seed_id(r.get("条目", "")) == seed_id), None)
    if row is None:
        errors.append(f"REGISTRY.md missing row for {seed_id}")
        return

    expected_role = ROLE_EMOJI_BY_ROLE.get(reg.get("recommended_role"))
    if expected_role and _strip_md(row.get("角色", "")) != expected_role:
        errors.append(f"REGISTRY.md role mismatch for {seed_id}: {row.get('角色')} != {expected_role}")

    assets_readme = seed_dir / "assets" / "README.md"
    item_cell = row.get("条目", "")
    expected_assets_link = f"./{seed_id}/assets/README.md"
    if assets_readme.exists() and expected_assets_link not in item_cell:
        errors.append(f"REGISTRY.md item cell for {seed_id} must link to {expected_assets_link}")
    if not assets_readme.exists() and "assets/README.md" in item_cell:
        errors.append(f"REGISTRY.md item cell for {seed_id} links to missing assets/README.md")

    profile = reg.get("resource_profile", {})
    expected_resource_category = RESOURCE_CATEGORY_LABEL.get(profile.get("resource_category"))
    if expected_resource_category and _strip_md(row.get("资源类别", "")) != expected_resource_category:
        errors.append(
            f"REGISTRY.md 资源类别 mismatch for {seed_id}: "
            f"{row.get('资源类别')} != {expected_resource_category}"
        )
    expected_source_code = SOURCE_CODE_LABEL.get(profile.get("source_code_availability"))
    if expected_source_code and _strip_md(row.get("源码", "")) != expected_source_code:
        errors.append(f"REGISTRY.md 源码 mismatch for {seed_id}: {row.get('源码')} != {expected_source_code}")
    expected_llm = LLM_AVAILABILITY_LABEL.get(profile.get("paper_llm_availability_status"))
    if expected_llm and _strip_md(row.get("论文LLM", "")) != expected_llm:
        errors.append(f"REGISTRY.md 论文LLM mismatch for {seed_id}: {row.get('论文LLM')} != {expected_llm}")

    expected_nl = _pair_set_nl_count_label(reg)
    if _strip_md(row.get("NL 数", "")) != expected_nl:
        errors.append(f"REGISTRY.md NL 数 mismatch for {seed_id}: {row.get('NL 数')} != {expected_nl}")
    expected_eligible = str(reg.get("extracted_summary", {}).get("eligible_generated_pair_count", 0))
    if _strip_md(row.get("可计生成对", "")) != expected_eligible:
        errors.append(
            f"REGISTRY.md 可计生成对 mismatch for {seed_id}: "
            f"{row.get('可计生成对')} != {expected_eligible}"
        )
    expected_trace = str(reg.get("extracted_summary", {}).get("trace_verified_pair_count", 0))
    if _strip_md(row.get("已回溯验证", "")) != expected_trace:
        errors.append(
            f"REGISTRY.md 已回溯验证 mismatch for {seed_id}: "
            f"{row.get('已回溯验证')} != {expected_trace}"
        )
    expected_ref = str(_reference_count(reg))
    if _strip_md(row.get("参考解", "")) != expected_ref:
        errors.append(f"REGISTRY.md 参考解 mismatch for {seed_id}: {row.get('参考解')} != {expected_ref}")
    expected_nl_only = _nl_only_label(reg)
    if _strip_md(row.get("NL-only", "")) != expected_nl_only:
        errors.append(f"REGISTRY.md NL-only mismatch for {seed_id}: {row.get('NL-only')} != {expected_nl_only}")
    expected_json_link = f"./{seed_id}/seed_resource_registry.json"
    if expected_json_link not in row.get("结构化记录", ""):
        errors.append(f"REGISTRY.md structured record for {seed_id} must link to {expected_json_link}")
    if not _strip_md(row.get("备注", "")):
        errors.append(f"REGISTRY.md 备注 must be non-empty for {seed_id}")
ASSET_STATUS_ENUM = {"downloaded", "partially_downloaded", "metadata_only", "blocked", "not_applicable"}
STORAGE_ENUM = {"committed", "local_only", "metadata_only", "skipped"}
DOWNLOAD_ENUM = {"downloaded", "skipped", "blocked", "metadata_only", "local_only"}


class RawTableCache:
    """Lazy cache for table-like raw assets used by locator validation."""

    def __init__(self) -> None:
        self._parquet: dict[Path, Any] = {}
        self._xlsx: dict[tuple[Path, str], Any] = {}
        self._zip_text: dict[tuple[Path, str], str] = {}

    def parquet(self, path: Path):
        if path not in self._parquet:
            try:
                import pandas as pd
            except Exception as exc:  # pragma: no cover - environment guard
                raise RuntimeError("pandas/pyarrow are required for parquet locator validation") from exc
            self._parquet[path] = pd.read_parquet(path)
        return self._parquet[path]

    def xlsx(self, path: Path, sheet: str):
        key = (path, sheet)
        if key not in self._xlsx:
            try:
                import pandas as pd
            except Exception as exc:  # pragma: no cover - environment guard
                raise RuntimeError("pandas/openpyxl are required for xlsx locator validation") from exc
            self._xlsx[key] = pd.read_excel(path, sheet_name=sheet)
        return self._xlsx[key]

    def zip_text(self, path: Path, member: str) -> str:
        key = (path, member)
        if key not in self._zip_text:
            with zipfile.ZipFile(path) as zf:
                self._zip_text[key] = zf.read(member).decode("utf-8")
        return self._zip_text[key]


@dataclass
class PairTraceResult:
    """Granular trace outcome for one extracted pair.

    The validator uses these fields to recompute ``validation_summary.json``.
    They intentionally separate hash, locator, and text/hash checks so that a
    summary cannot claim stronger audit evidence than the raw trace supports.
    """

    pair_id: str
    source_hash_match: bool = False
    locator_resolved: bool = False
    text_or_hash_match: bool = False
    trace_verified: bool = False
    eligible_generated: bool = False
    repo_or_external_reproducible_eligible: bool = False
    local_only_trace: bool = False
    metadata_only_trace: bool = False
    errors: list[str] = field(default_factory=list)


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
            "source_inventory",
            "data_construction",
            "quality_audit",
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
    if asset_summary.get("license_status") not in LICENSE_STATUS_ENUM:
        errors.append(f"unknown asset_summary license_status {asset_summary.get('license_status')}")
    if asset_summary.get("redistribution_status") not in REDISTRIBUTION_STATUS_ENUM:
        errors.append(
            f"unknown asset_summary redistribution_status {asset_summary.get('redistribution_status')}"
        )
    source_inventory = reg.get("source_inventory", {})
    require(
        source_inventory,
        [
            "raw_nl_count",
            "unique_nl_count",
            "nl_only_count",
            "nl_only_unique_count",
            "generated_pair_count",
            "eligible_generated_pair_count",
            "reference_pair_count",
            "canonical_case_count",
            "unique_generated_stm0_count",
            "one_to_many_shape",
            "count_status",
            "count_basis",
            "notes",
        ],
        "source_inventory",
        errors,
    )
    if source_inventory.get("count_status") not in {
        "verified",
        "unknown",
        "paper_only",
        "not_applicable",
        "artifact_reviewed",
    }:
        errors.append(f"unknown source_inventory count_status {source_inventory.get('count_status')}")
    if source_inventory.get("eligible_generated_pair_count") != reg.get("extracted_summary", {}).get(
        "eligible_generated_pair_count"
    ):
        errors.append(
            "source_inventory eligible_generated_pair_count mismatch: "
            f"{source_inventory.get('eligible_generated_pair_count')} != "
            f"{reg.get('extracted_summary', {}).get('eligible_generated_pair_count')}"
        )
    if source_inventory.get("reference_pair_count") != _reference_count(reg):
        errors.append(
            "source_inventory reference_pair_count mismatch: "
            f"{source_inventory.get('reference_pair_count')} != {_reference_count(reg)}"
        )
    data_construction = reg.get("data_construction", {})
    require(
        data_construction,
        [
            "paper_read_status",
            "paper_claim_summary",
            "artifact_source",
            "generation_or_construction_pipeline",
            "what_is_raw_nl",
            "what_is_stm0",
            "evidence_paths",
        ],
        "data_construction",
        errors,
    )
    if not isinstance(data_construction.get("evidence_paths", []), list):
        errors.append("data_construction evidence_paths must be a list")
    quality_audit = reg.get("quality_audit", {})
    require(
        quality_audit,
        [
            "audit_status",
            "sample_size",
            "sampled_items",
            "quality_findings",
            "domain_fit_caveat",
            "evidence_paths",
        ],
        "quality_audit",
        errors,
    )
    if not isinstance(quality_audit.get("sampled_items", []), list):
        errors.append("quality_audit sampled_items must be a list")
    if not isinstance(quality_audit.get("evidence_paths", []), list):
        errors.append("quality_audit evidence_paths must be a list")
    resource_profile = reg.get("resource_profile", {})
    require(
        resource_profile,
        [
            "resource_category",
            "source_code_availability",
            "paper_uses_llm",
            "paper_llm_models",
            "paper_llm_availability_status",
            "paper_llm_availability_checked_at",
            "paper_llm_availability_evidence_urls",
            "code_reproducibility",
            "code_reproducibility_evidence_paths",
            "resource_profile_notes",
        ],
        "resource_profile",
        errors,
    )
    if resource_profile.get("resource_category") not in RESOURCE_CATEGORY_ENUM:
        errors.append(f"unknown resource_category {resource_profile.get('resource_category')}")
    if resource_profile.get("source_code_availability") not in SOURCE_CODE_AVAILABILITY_ENUM:
        errors.append(f"unknown source_code_availability {resource_profile.get('source_code_availability')}")
    if resource_profile.get("paper_uses_llm") not in PAPER_USES_LLM_ENUM:
        errors.append(f"unknown paper_uses_llm {resource_profile.get('paper_uses_llm')}")
    if resource_profile.get("paper_llm_availability_status") not in LLM_AVAILABILITY_ENUM:
        errors.append(
            f"unknown paper_llm_availability_status {resource_profile.get('paper_llm_availability_status')}"
        )
    if resource_profile.get("code_reproducibility") not in CODE_REPRODUCIBILITY_ENUM:
        errors.append(f"unknown code_reproducibility {resource_profile.get('code_reproducibility')}")
    if not isinstance(resource_profile.get("paper_llm_models", []), list):
        errors.append("resource_profile paper_llm_models must be a list")
    if not isinstance(resource_profile.get("paper_llm_availability_evidence_urls", []), list):
        errors.append("resource_profile paper_llm_availability_evidence_urls must be a list")
    if not isinstance(resource_profile.get("code_reproducibility_evidence_paths", []), list):
        errors.append("resource_profile code_reproducibility_evidence_paths must be a list")
    if resource_profile.get("paper_uses_llm") == "yes" and not resource_profile.get("paper_llm_models"):
        errors.append("resource_profile paper_uses_llm=yes requires non-empty paper_llm_models")
    if resource_profile.get("paper_uses_llm") == "yes" and resource_profile.get("paper_llm_availability_status") == "not_applicable":
        errors.append("resource_profile paper_uses_llm=yes cannot use paper_llm_availability_status=not_applicable")
    if resource_profile.get("paper_uses_llm") in {"no", "not_applicable"} and resource_profile.get("paper_llm_availability_status") not in {"not_applicable", "unknown"}:
        errors.append("resource_profile non-LLM work should use LLM availability not_applicable/unknown")
    if resource_profile.get("resource_category") == "first_source_nl_stm" and reg.get("extracted_summary", {}).get("eligible_generated_pair_count", 0) <= 0:
        errors.append("resource_category first_source_nl_stm requires eligible generated pairs")
    if resource_profile.get("resource_category") == "nl_code_reproducible":
        if resource_profile.get("source_code_availability") in {"not_published", "not_applicable"}:
            errors.append("resource_category nl_code_reproducible requires available source code")
        if not reg.get("source_work", {}).get("code_urls"):
            errors.append("resource_category nl_code_reproducible requires source_work.code_urls")
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
    if ds.get("r2_smoke_recommendation") not in R2_SMOKE_ENUM:
        errors.append(f"unknown r2_smoke_recommendation {ds.get('r2_smoke_recommendation')}")
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
                "nl_count",
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
        if asset.get("license_status") not in LICENSE_STATUS_ENUM:
            errors.append(f"assets[{i}] unknown license_status {asset.get('license_status')}")
        if asset.get("redistribution_status") not in REDISTRIBUTION_STATUS_ENUM:
            errors.append(f"assets[{i}] unknown redistribution_status {asset.get('redistribution_status')}")


def _validate_against_json_schema(obj: dict[str, Any], schema_name: str, errors: list[str]) -> None:
    """Run a JSON Schema when jsonschema is available.

    Hand-written checks below provide friendly diagnostics and local semantic
    invariants.  The schema check prevents enum / field drift in PR review so
    that schema files are not merely documentation.
    """

    schema_path = BASE / "schemas" / schema_name
    if not schema_path.exists():
        return
    if Draft202012Validator is None:
        errors.append(f"jsonschema is required to validate {schema_name}")
        return
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(obj), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(p) for p in error.absolute_path) or "<root>"
        errors.append(f"{schema_name} validation error at {path}: {error.message}")


def validate_registry_against_schema(reg: dict[str, Any], errors: list[str]) -> None:
    _validate_against_json_schema(reg, "seed_resource_registry.schema.json", errors)


def validate_manifest_against_schema(manifest: dict[str, Any], errors: list[str]) -> None:
    _validate_against_json_schema(manifest, "assets_manifest.schema.json", errors)


def _parse_parquet_locator(locator: str) -> tuple[int, list[str]] | None:
    """Parse locator like 'row=0; columns=input,uml_code,reasoning'."""
    row_match = re.search(r"(?:^|;)\s*row\s*=\s*(\d+)\s*(?:;|$)", locator)
    cols_match = re.search(r"(?:^|;)\s*columns\s*=\s*([^;]+)", locator)
    if not row_match or not cols_match:
        return None
    cols = [c.strip() for c in cols_match.group(1).split(",") if c.strip()]
    return int(row_match.group(1)), cols


def _parse_kv_locator(locator: str) -> dict[str, str]:
    """Parse a semicolon-separated locator with key=value fragments."""

    result: dict[str, str] = {}
    for part in locator.split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def _python_string_symbol(source: str, symbol: str) -> str:
    """Extract a module-level Python string literal assigned to ``symbol``."""

    tree = ast.parse(source)
    for node in tree.body:
        targets = []
        value = None
        if isinstance(node, ast.Assign):
            targets = node.targets
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value = node.value
        if value is None:
            continue
        if not any(isinstance(t, ast.Name) and t.id == symbol for t in targets):
            continue
        literal = ast.literal_eval(value)
        if not isinstance(literal, str):
            raise ValueError(f"symbol {symbol} is not a string literal")
        return literal
    raise KeyError(f"symbol {symbol} not found")


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def validate_pair_trace(seed_dir: Path, row: dict, asset: dict, raw_path: Path, cache: RawTableCache) -> PairTraceResult:
    """Return granular independent trace evidence for this row.

    A row's self-reported ``trace_verified`` flag is treated as a claim to audit,
    not as evidence. For eligible count, the validator uses this function's
    result instead of the row's self-report.
    """

    pair_id = row.get("pair_id") or "<missing_pair_id>"
    result = PairTraceResult(pair_id=pair_id)
    locator_type = row.get("source_locator_type")
    locator = row.get("source_locator", "")
    storage_mode = asset.get("storage_mode")
    download_status = asset.get("download_status")

    if storage_mode == "local_only":
        result.local_only_trace = bool(row.get("trace_verified"))
    if storage_mode == "metadata_only" or download_status == "metadata_only":
        result.metadata_only_trace = bool(row.get("trace_verified"))

    if storage_mode != "committed" or download_status != "downloaded":
        if row.get("trace_verified"):
            result.errors.append(f"pair {pair_id} claims trace_verified but source asset is not committed/downloaded")
        return result

    if not raw_path.exists() or raw_path.is_dir():
        result.errors.append(f"pair {pair_id} source raw asset missing: {raw_path}")
        return result

    if row.get("source_sha256") != sha256_file(raw_path):
        result.errors.append(f"pair {pair_id} source_sha256 mismatch")
        return result
    result.source_hash_match = True

    if locator_type == "zip_python_symbol_and_text_file":
        fields = _parse_kv_locator(locator)
        nl_member = fields.get("nl_member", "")
        nl_symbol = fields.get("nl_symbol", "")
        stm0_member = fields.get("stm0_member", "")
        if not nl_member or not nl_symbol or not stm0_member:
            result.errors.append(f"pair {pair_id} invalid ZIP locator: {locator}")
            return result
        try:
            nl_source = cache.zip_text(raw_path, nl_member)
            raw_nl = _python_string_symbol(nl_source, nl_symbol)
            raw_stm = cache.zip_text(raw_path, stm0_member)
        except Exception as exc:
            result.errors.append(f"pair {pair_id} cannot resolve ZIP locator {locator}: {exc}")
            return result
        result.locator_resolved = True

        text_ok = True
        if row.get("nl_text") != raw_nl:
            result.errors.append(f"pair {pair_id} nl_text does not match ZIP Python symbol {nl_symbol}")
            text_ok = False
        if row.get("stm0_text") != raw_stm:
            result.errors.append(f"pair {pair_id} stm0_text does not match ZIP member {stm0_member}")
            text_ok = False
        expected_nl_hash = sha256_text(raw_nl)
        expected_stm_hash = sha256_text(raw_stm)
        if row.get("nl_sha256") != expected_nl_hash:
            result.errors.append(f"pair {pair_id} nl_sha256 mismatch: {row.get('nl_sha256')} != {expected_nl_hash}")
            text_ok = False
        if row.get("stm0_sha256") != expected_stm_hash:
            result.errors.append(f"pair {pair_id} stm0_sha256 mismatch: {row.get('stm0_sha256')} != {expected_stm_hash}")
            text_ok = False
        if row.get("source_local_path") and seed_dir / "assets" / row.get("source_local_path") != raw_path:
            result.errors.append(f"pair {pair_id} source_local_path does not match manifest raw path")
            text_ok = False
        result.text_or_hash_match = text_ok
        result.trace_verified = result.source_hash_match and result.locator_resolved and result.text_or_hash_match
        result.eligible_generated = (
            result.trace_verified
            and bool(row.get("is_generated_stm0"))
            and not bool(row.get("is_reference"))
            and not bool(row.get("is_postprocessed"))
        )
        result.repo_or_external_reproducible_eligible = (
            result.eligible_generated and storage_mode == "committed" and download_status == "downloaded"
        )
        return result

    if locator_type == "zip_member_pair":
        fields = _parse_kv_locator(locator)
        nl_member = fields.get("nl_member", "")
        stm0_member = fields.get("stm0_member", "")
        if not nl_member or not stm0_member:
            result.errors.append(f"pair {pair_id} invalid ZIP member-pair locator: {locator}")
            return result
        try:
            raw_nl = cache.zip_text(raw_path, nl_member)
            raw_stm = cache.zip_text(raw_path, stm0_member)
        except Exception as exc:
            result.errors.append(f"pair {pair_id} cannot resolve ZIP member-pair locator {locator}: {exc}")
            return result
        result.locator_resolved = True

        text_ok = True
        if row.get("nl_text") != raw_nl:
            result.errors.append(f"pair {pair_id} nl_text does not match ZIP member {nl_member}")
            text_ok = False
        if row.get("stm0_text") != raw_stm:
            result.errors.append(f"pair {pair_id} stm0_text does not match ZIP member {stm0_member}")
            text_ok = False
        expected_nl_hash = sha256_text(raw_nl)
        expected_stm_hash = sha256_text(raw_stm)
        if row.get("nl_sha256") != expected_nl_hash:
            result.errors.append(f"pair {pair_id} nl_sha256 mismatch: {row.get('nl_sha256')} != {expected_nl_hash}")
            text_ok = False
        if row.get("stm0_sha256") != expected_stm_hash:
            result.errors.append(f"pair {pair_id} stm0_sha256 mismatch: {row.get('stm0_sha256')} != {expected_stm_hash}")
            text_ok = False
        if row.get("source_local_path") and seed_dir / "assets" / row.get("source_local_path") != raw_path:
            result.errors.append(f"pair {pair_id} source_local_path does not match manifest raw path")
            text_ok = False
        result.text_or_hash_match = text_ok
        result.trace_verified = result.source_hash_match and result.locator_resolved and result.text_or_hash_match
        result.eligible_generated = (
            result.trace_verified
            and bool(row.get("is_generated_stm0"))
            and not bool(row.get("is_reference"))
            and not bool(row.get("is_postprocessed"))
        )
        result.repo_or_external_reproducible_eligible = (
            result.eligible_generated and storage_mode == "committed" and download_status == "downloaded"
        )
        return result

    if locator_type == "xlsx_sheet_row_columns":
        fields = _parse_kv_locator(locator)
        sheet = fields.get("sheet", "")
        row_value = fields.get("row", "")
        columns_value = fields.get("columns", "")
        if not sheet or not row_value.isdigit() or not columns_value:
            result.errors.append(f"pair {pair_id} invalid XLSX locator: {locator}")
            return result
        row_index = int(row_value)
        columns = [c.strip() for c in columns_value.split(",") if c.strip()]
        nl_col = row.get("nl_source_column") or "Requirement Description"
        stm_col = row.get("stm0_source_column") or "Generation PlantUML"
        try:
            table = cache.xlsx(raw_path, sheet)
        except Exception as exc:
            result.errors.append(f"pair {pair_id} cannot read XLSX raw asset {raw_path}: {exc}")
            return result
        if row_index < 0 or row_index >= len(table):
            result.errors.append(f"pair {pair_id} XLSX row out of range: {row_index}")
            return result
        missing = [c for c in (nl_col, stm_col) if c not in table.columns]
        if missing:
            result.errors.append(f"pair {pair_id} XLSX raw missing required columns: {','.join(missing)}")
            return result
        for required_col in (nl_col, stm_col):
            if required_col not in columns:
                result.errors.append(f"pair {pair_id} locator columns missing {required_col}: {columns}")
                return result
        result.locator_resolved = True

        raw_row = table.iloc[row_index]
        raw_nl = _as_text(raw_row[nl_col])
        raw_stm = _as_text(raw_row[stm_col])
        text_ok = True
        if row.get("nl_text") != raw_nl:
            result.errors.append(f"pair {pair_id} nl_text does not match raw XLSX row {row_index}")
            text_ok = False
        if row.get("stm0_text") != raw_stm:
            result.errors.append(f"pair {pair_id} stm0_text does not match raw XLSX row {row_index}")
            text_ok = False
        expected_nl_hash = sha256_text(raw_nl)
        expected_stm_hash = sha256_text(raw_stm)
        if row.get("nl_sha256") != expected_nl_hash:
            result.errors.append(f"pair {pair_id} nl_sha256 mismatch: {row.get('nl_sha256')} != {expected_nl_hash}")
            text_ok = False
        if row.get("stm0_sha256") != expected_stm_hash:
            result.errors.append(f"pair {pair_id} stm0_sha256 mismatch: {row.get('stm0_sha256')} != {expected_stm_hash}")
            text_ok = False

        # The XLSX seed entries carry case identity and reference-boundary
        # evidence in addition to NL/STM_0 text.  Validate these fields too so
        # that LLM distribution, case mapping, and reference leakage controls
        # cannot drift silently while the raw generated pair still passes.
        metadata_checks = {
            "llm": "LLMs",
            "model_source": "Model Source",
            "model_name": "Model Name",
        }
        for row_key, col_name in metadata_checks.items():
            if row_key in row:
                if col_name not in table.columns:
                    result.errors.append(f"pair {pair_id} XLSX raw missing metadata column: {col_name}")
                    text_ok = False
                    continue
                raw_value = _as_text(raw_row[col_name])
                if row.get(row_key) != raw_value:
                    result.errors.append(f"pair {pair_id} {row_key} does not match raw XLSX row {row_index}")
                    text_ok = False
        if "reference_plantuml_sha256" in row:
            ref_col = "PlantUML"
            if ref_col not in table.columns:
                result.errors.append(f"pair {pair_id} XLSX raw missing reference column: {ref_col}")
                text_ok = False
            else:
                expected_ref_hash = sha256_text(_as_text(raw_row[ref_col]))
                if row.get("reference_plantuml_sha256") != expected_ref_hash:
                    result.errors.append(
                        f"pair {pair_id} reference_plantuml_sha256 mismatch: "
                        f"{row.get('reference_plantuml_sha256')} != {expected_ref_hash}"
                    )
                    text_ok = False
        if row.get("source_local_path") and seed_dir / "assets" / row.get("source_local_path") != raw_path:
            result.errors.append(f"pair {pair_id} source_local_path does not match manifest raw path")
            text_ok = False
        result.text_or_hash_match = text_ok
        result.trace_verified = result.source_hash_match and result.locator_resolved and result.text_or_hash_match
        result.eligible_generated = (
            result.trace_verified
            and bool(row.get("is_generated_stm0"))
            and not bool(row.get("is_reference"))
            and not bool(row.get("is_postprocessed"))
        )
        result.repo_or_external_reproducible_eligible = (
            result.eligible_generated and storage_mode == "committed" and download_status == "downloaded"
        )
        return result

    if locator_type != "parquet_row_columns":
        if row.get("trace_verified"):
            result.errors.append(f"pair {pair_id} claims trace_verified with unsupported locator type {locator_type}")
        return result

    parsed = _parse_parquet_locator(locator)
    if parsed is None:
        result.errors.append(f"pair {pair_id} invalid parquet locator: {locator}")
        return result
    row_index, columns = parsed
    try:
        table = cache.parquet(raw_path)
    except Exception as exc:
        result.errors.append(f"pair {pair_id} cannot read parquet raw asset {raw_path}: {exc}")
        return result
    if row_index < 0 or row_index >= len(table):
        result.errors.append(f"pair {pair_id} parquet row out of range: {row_index}")
        return result
    missing = [c for c in ("input", "uml_code") if c not in table.columns]
    if missing:
        result.errors.append(f"pair {pair_id} parquet raw missing required columns: {','.join(missing)}")
        return result
    for required_col in ("input", "uml_code"):
        if required_col not in columns:
            result.errors.append(f"pair {pair_id} locator columns missing {required_col}: {columns}")
            return result
    result.locator_resolved = True

    raw_nl = _as_text(table.iloc[row_index]["input"])
    raw_stm = _as_text(table.iloc[row_index]["uml_code"])
    text_ok = True
    if row.get("nl_text") != raw_nl:
        result.errors.append(f"pair {pair_id} nl_text does not match raw parquet row {row_index}")
        text_ok = False
    if row.get("stm0_text") != raw_stm:
        result.errors.append(f"pair {pair_id} stm0_text does not match raw parquet row {row_index}")
        text_ok = False
    expected_nl_hash = sha256_text(raw_nl)
    expected_stm_hash = sha256_text(raw_stm)
    if row.get("nl_sha256") != expected_nl_hash:
        result.errors.append(f"pair {pair_id} nl_sha256 mismatch: {row.get('nl_sha256')} != {expected_nl_hash}")
        text_ok = False
    if row.get("stm0_sha256") != expected_stm_hash:
        result.errors.append(f"pair {pair_id} stm0_sha256 mismatch: {row.get('stm0_sha256')} != {expected_stm_hash}")
        text_ok = False
    if row.get("source_local_path") and seed_dir / "assets" / row.get("source_local_path") != raw_path:
        result.errors.append(f"pair {pair_id} source_local_path does not match manifest raw path")
        text_ok = False
    result.text_or_hash_match = text_ok
    result.trace_verified = result.source_hash_match and result.locator_resolved and result.text_or_hash_match
    result.eligible_generated = (
        result.trace_verified
        and bool(row.get("is_generated_stm0"))
        and not bool(row.get("is_reference"))
        and not bool(row.get("is_postprocessed"))
    )
    result.repo_or_external_reproducible_eligible = (
        result.eligible_generated and storage_mode == "committed" and download_status == "downloaded"
    )
    return result


def expected_raw_asset_count(manifest: dict) -> int:
    """Count raw assets that the repo can currently re-check by hash.

    Metadata-only and skipped assets are intentionally not counted here: they
    can be recorded in the manifest, but cannot support committed raw evidence.
    """

    return sum(
        1
        for asset in manifest.get("assets", [])
        if asset.get("storage_mode") == "committed" and asset.get("download_status") == "downloaded"
    )


def compare_validation_summary(
    seed_id: str,
    vs: dict,
    expected: dict[str, Any],
    errors: list[str],
) -> None:
    """Compare validation_summary.json against independently recomputed facts."""

    if vs.get("schema_version") != "seed-validation-summary.v1":
        errors.append(f"validation_summary schema_version mismatch: {vs.get('schema_version')}")
    if vs.get("seed_id") != seed_id:
        errors.append(f"validation_summary seed_id mismatch: {vs.get('seed_id')} != {seed_id}")
    for key, expected_value in expected.items():
        actual = vs.get(key)
        if actual != expected_value:
            errors.append(f"validation_summary {key} mismatch: {actual} != {expected_value}")


def derive_inventory_from_pairs(
    reg: dict[str, Any],
    pairs: list[dict[str, Any]],
    eligible: int,
) -> dict[str, Any]:
    """Derive auditable source_inventory counts from extracted pairs/pair_sets.

    This intentionally uses only committed structured evidence.  For paper-only
    entries with no extracted pairs, it falls back to the registry pair_set
    counts so that unknown values remain explicit instead of guessed.
    """

    pair_sets = reg.get("pair_sets", [])
    if pairs:
        raw_values = [
            _count_value_from_nl_count(
                pair_set,
                "raw",
                "raw_rows",
                "raw_requirements",
                "raw_nl_descriptions_in_zip",
            )
            for pair_set in pair_sets
        ]
        unique_values = [
            _count_value_from_nl_count(
                pair_set,
                "unique",
                "unique_requirement_descriptions",
                "unique_requirements",
                "unique_nl_descriptions_in_zip",
            )
            for pair_set in pair_sets
        ]
        nl_only_values = [
            _count_value_from_nl_count(
                pair_set,
                "nl_only_generation_failure",
                "nl_only_without_generated_output",
                "nl_only_pipeline_requirements",
            )
            for pair_set in pair_sets
        ]
        raw_values = [v for v in raw_values if v is not None]
        unique_values = [v for v in unique_values if v is not None]
        nl_only_values = [v for v in nl_only_values if v is not None]
        raw_nl_count = _sum_known_counts(raw_values) if raw_values else len(pairs)
        unique_nl_count = (
            _sum_known_counts(unique_values)
            if unique_values
            else len({_normalise_nl(row.get("nl_text")) for row in pairs})
        )
        nl_only_rows = [row for row in pairs if not bool(row.get("is_generated_stm0"))]
        eligible_rows = [
            row
            for row in pairs
            if bool(row.get("is_generated_stm0"))
            and not bool(row.get("is_reference"))
            and not bool(row.get("is_postprocessed"))
        ]
        # ``unique_generated_stm0_count`` is defined as unique real generated
        # STM_0 texts. Excluded failure sentinels such as
        # ``No valid PlantUML code found.`` are NL-only audit rows and must not
        # inflate generated STM_0 diversity.
        return {
            "raw_nl_count": raw_nl_count,
            "unique_nl_count": unique_nl_count,
            "nl_only_count": _sum_known_counts(nl_only_values) if nl_only_values else len(nl_only_rows),
            "nl_only_unique_count": _sum_known_counts(nl_only_values)
            if nl_only_values
            else len({_normalise_nl(row.get("nl_text")) for row in nl_only_rows}),
            "generated_pair_count": sum(int(pair_set.get("raw_pair_count", 0)) for pair_set in pair_sets),
            "eligible_generated_pair_count": eligible,
            "reference_pair_count": _reference_count(reg),
            "canonical_case_count": _sum_known_counts(
                [pair_set.get("canonical_case_count") for pair_set in pair_sets if "canonical_case_count" in pair_set]
            ),
            "unique_generated_stm0_count": len({_as_text(row.get("stm0_text")) for row in eligible_rows}),
        }

    raw_values = [
        _count_value_from_nl_count(pair_set, "raw", "raw_rows", "raw_requirements", "raw_nl_descriptions_in_zip")
        for pair_set in pair_sets
    ]
    unique_values = [
        _count_value_from_nl_count(
            pair_set,
            "unique",
            "unique_requirement_descriptions",
            "unique_requirements",
            "unique_nl_descriptions_in_zip",
        )
        for pair_set in pair_sets
    ]
    nl_only_values = [
        _count_value_from_nl_count(
            pair_set,
            "nl_only_generation_failure",
            "nl_only_without_generated_output",
            "nl_only_pipeline_requirements",
        )
        for pair_set in pair_sets
    ]
    raw_values = [v for v in raw_values if v is not None]
    unique_values = [v for v in unique_values if v is not None]
    nl_only_values = [v for v in nl_only_values if v is not None]

    return {
        "raw_nl_count": _sum_known_counts(raw_values) if raw_values else 0,
        "unique_nl_count": _sum_known_counts(unique_values) if unique_values else "unknown",
        "nl_only_count": _sum_known_counts(nl_only_values) if nl_only_values else "unknown",
        "nl_only_unique_count": _sum_known_counts(nl_only_values) if nl_only_values else "unknown",
        "generated_pair_count": sum(int(pair_set.get("raw_pair_count", 0)) for pair_set in pair_sets),
        "eligible_generated_pair_count": eligible,
        "reference_pair_count": _reference_count(reg),
        "canonical_case_count": sum(int(pair_set.get("canonical_case_count", 0)) for pair_set in pair_sets),
        "unique_generated_stm0_count": 0,
    }


def validate_source_inventory_counts(
    seed_id: str,
    reg: dict[str, Any],
    pairs: list[dict[str, Any]],
    eligible: int,
    errors: list[str],
) -> None:
    """Keep machine source_inventory counts tied to extracted evidence."""

    inventory = reg.get("source_inventory", {})
    expected = derive_inventory_from_pairs(reg, pairs, eligible)
    for key, expected_value in expected.items():
        _compare_inventory_count(seed_id, key, inventory.get(key), expected_value, errors)


def validate_seed(seed_id: str) -> int:
    seed_dir = BASE / seed_id
    reg_path = seed_dir / "seed_resource_registry.json"
    errors = []
    if not reg_path.exists():
        print(f"ERROR missing registry: {reg_path}", file=sys.stderr)
        return 1
    reg = load_json(reg_path)
    validate_registry_against_schema(reg, errors)
    validate_registry_shape(reg, errors)
    manifest_rel = reg.get("asset_summary", {}).get("manifest_path", "")
    manifest_path = seed_dir / manifest_rel if manifest_rel else None
    if manifest_rel and (not manifest_path or not manifest_path.exists() or manifest_path.is_dir()):
        errors.append(f"manifest_path does not point to file: {manifest_rel}")
        manifest = {"assets": []}
    elif manifest_path:
        manifest = load_json(manifest_path)
        validate_manifest_against_schema(manifest, errors)
        validate_manifest_shape(manifest, errors)
    else:
        manifest = {"assets": []}
    asset_by_id = {a["asset_id"]: a for a in manifest.get("assets", []) if "asset_id" in a}
    pair_set_role_by_id = {
        pair_set.get("pair_set_id"): pair_set.get("eligibility_state")
        for pair_set in reg.get("pair_sets", [])
        if pair_set.get("pair_set_id")
    }
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
    pair_results: list[PairTraceResult] = []
    cache = RawTableCache()
    for row in pairs:
        aid = row.get("source_asset_id")
        asset = asset_by_id.get(aid)
        if not asset:
            pair_id = row.get("pair_id") or "<missing_pair_id>"
            pair_error = f"pair {pair_id} unknown source_asset_id {aid}"
            errors.append(pair_error)
            pair_results.append(PairTraceResult(pair_id=pair_id, errors=[pair_error]))
            continue
        raw_path = seed_dir / "assets" / asset.get("local_path", "")
        row_result = validate_pair_trace(seed_dir, row, asset, raw_path, cache)
        pair_results.append(row_result)
        errors.extend(row_result.errors)
        pair_id = row.get("pair_id") or "<missing_pair_id>"
        row_state = row.get("eligibility_state")
        if row_state not in ROLE_ENUM:
            errors.append(f"pair {pair_id} unknown eligibility_state {row_state}")
        pair_set_id = row.get("pair_set_id")
        expected_pair_set_state = pair_set_role_by_id.get(pair_set_id)
        if row_result.eligible_generated and not pair_set_id:
            errors.append(f"pair {pair_id} eligible generated row must carry pair_set_id")
        if pair_set_id and expected_pair_set_state is None:
            errors.append(f"pair {pair_id} references unknown pair_set_id {pair_set_id}")
        if row_result.eligible_generated:
            if expected_pair_set_state is None:
                errors.append(f"pair {pair_id} eligible generated row must reference a known pair_set_id")
            elif row_state != expected_pair_set_state:
                errors.append(
                    f"pair {pair_id} eligibility_state mismatch with pair set: "
                    f"{row_state} != {expected_pair_set_state}"
                )
            if row.get("exclusion_reason") not in (None, ""):
                errors.append(f"pair {pair_id} eligible generated row must not carry exclusion_reason")
        else:
            if row_state in {"final_pool_ready", "conditional_final_pool"}:
                errors.append(f"pair {pair_id} is not eligible generated but uses pool eligibility_state {row_state}")
            if row_state == "excluded" and row.get("exclusion_reason") in (None, ""):
                errors.append(f"pair {pair_id} excluded row must carry exclusion_reason")
        if row.get("trace_verified") and not row_result.trace_verified:
            errors.append(f"pair {row.get('pair_id')} claims trace_verified but raw trace validation failed")
        if (not row.get("trace_verified")) and row_result.trace_verified:
            errors.append(f"pair {row.get('pair_id')} has valid raw trace but trace_verified is false")
    trace_verified = sum(1 for r in pair_results if r.trace_verified)
    eligible = sum(1 for r in pair_results if r.eligible_generated)
    expected_summary = {
        "raw_asset_count": expected_raw_asset_count(manifest),
        "pair_count": len(pairs),
        "hash_match_count": sum(1 for r in pair_results if r.source_hash_match),
        "locator_resolved_count": sum(1 for r in pair_results if r.locator_resolved),
        "text_or_hash_match_count": sum(1 for r in pair_results if r.text_or_hash_match),
        "trace_verified_pair_count": trace_verified,
        "eligible_generated_pair_count": eligible,
        "repo_or_external_reproducible_eligible_count": sum(
            1 for r in pair_results if r.repo_or_external_reproducible_eligible
        ),
        "local_only_trace_count": sum(1 for r in pair_results if r.local_only_trace),
        "metadata_only_trace_count": sum(1 for r in pair_results if r.metadata_only_trace),
        "failed_pair_ids": [r.pair_id for r in pair_results if r.errors],
        "excluded_pair_ids": [
            row.get("pair_id") or "<missing_pair_id>"
            for row, result in zip(pairs, pair_results)
            if not result.eligible_generated and row.get("eligibility_state") == "excluded"
        ],
    }
    vs_rel = reg.get("extracted_summary", {}).get("validation_summary", "")
    vs_path = seed_dir / vs_rel if vs_rel else Path("")
    if vs_path and str(vs_path) != "." and vs_path.exists():
        vs = load_json(vs_path)
        compare_validation_summary(seed_id, vs, expected_summary, errors)
    if reg.get("extracted_summary", {}).get("eligible_generated_pair_count") != eligible:
        errors.append(f"registry eligible count mismatch: {reg.get('extracted_summary', {}).get('eligible_generated_pair_count')} != {eligible}")
    if reg.get("extracted_summary", {}).get("trace_verified_pair_count") != trace_verified:
        errors.append(f"registry trace count mismatch: {reg.get('extracted_summary', {}).get('trace_verified_pair_count')} != {trace_verified}")
    validate_source_inventory_counts(seed_id, reg, pairs, eligible, errors)
    validate_registry_markdown_row(seed_id, reg, seed_dir, errors)
    if reg.get("recommended_role") == "final_pool_ready":
        if eligible == 0:
            errors.append("final_pool_ready registry must have at least one eligible generated pair")
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
