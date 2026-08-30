#!/usr/bin/env python3
"""Build a deterministic inventory of Paper1 documentation and release entries.

The inventory is a review aid.  It never reads or changes semantic decisions,
raw artifacts, or reference data, and it does not infer a new research result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DocumentationInventoryRow(BaseModel):
    """One repository documentation or manifest entry and its publication assessment."""

    path: str = Field(description="Repository-relative path of the scanned documentation or manifest file.")
    file_type: str = Field(description="Detected file category such as markdown, manifest, or entrance script.")
    publication_surface: bool = Field(description="Whether the file is intended to be reachable as a current publication entry.")
    historical_or_archive: bool = Field(description="Whether the path is explicitly historical, archived, or superseded.")
    headline_sources: list[str] = Field(description="Canonical or legacy result sources named by the file, possibly empty.")
    versions_found: list[str] = Field(description="Version and generation markers found in the file.")
    legacy_numbers_found: list[str] = Field(description="Known legacy headline number fragments found in the file.")
    old_protocols_found: list[str] = Field(description="Legacy protocol identifiers or names found in the file.")
    absolute_paths: list[str] = Field(description="Absolute filesystem paths found in the file, excluding ordinary URLs.")
    broken_relative_links: list[str] = Field(description="Relative markdown links whose local target cannot be resolved.")
    duplicate_headline_signals: list[str] = Field(description="Signals that the file repeats a current headline table or metric set.")
    missing_unit_or_formula_signals: list[str] = Field(description="Metric prose that appears to omit an expected unit or formula marker.")
    recommended_action: str = Field(description="Disposition: canonical, redirect, historical archive, protocol-only, or preserve.")
    sha256: str = Field(description="SHA-256 digest of scanned bytes; manifest rows use the explicit dynamic-manifest marker to avoid a self-referential hash cycle.")


class DocumentationInventory(BaseModel):
    """Deterministic document inventory used by the v4 publication-surface review."""

    model_config = ConfigDict(populate_by_name=True)

    schema_version: str = Field(alias="schema", description="Versioned inventory schema identifier serialized as schema.")
    repository_root: str = Field(description="Repository-relative scope root used for this inventory.")
    generated_by: str = Field(description="Provider-free command or script that generated the inventory.")
    current_sources: dict[str, str] = Field(description="The only current headline source for each side and comparison layer.")
    rows: list[DocumentationInventoryRow] = Field(description="All scanned markdown, manifest, and entrance-script rows.")


LEGACY_NUMBERS = (
    "306/435",
    "118/145",
    "84/145",
    "1165/1271",
    "721/444/106",
    "279/132/101",
    "411/512",
    "101/512",
)
OLD_PROTOCOLS = (
    "issue-189-195-manual-evidence-v1",
    "v3.2",
)
ARCHIVE_PROVENANCE_PATHS = {
    "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/reviews/academic_citation_review.md",
    "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/reviews/numeric_recompute_review_v3.md",
}
VERSION_RE = re.compile(r"\b(?:v(?:2|3|4|27|46|60)|v\d+\.\d+|X1v2|x1v2)\b", re.IGNORECASE)
ABSOLUTE_RE = re.compile(r"(?<![A-Za-z0-9_:/])/(?:home|data|tmp|mnt|opt|srv|workspace)/[^\s`\]\)>,;]+")
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")


def _is_candidate(path: Path) -> bool:
    name = path.name.upper()
    return path.suffix.lower() in {".md", ".json", ".py"} and (
        path.suffix.lower() == ".md"
        or "MANIFEST" in name
        or name in {"README.JSON", "STATUS.JSON"}
        or (path.suffix.lower() == ".py" and ("scripts" in path.parts or "release" in path.parts))
    )


def _classification(path: Path, paper_root: Path, text: str) -> tuple[bool, bool, str]:
    rel = path.relative_to(paper_root).as_posix()
    if rel in ARCHIVE_PROVENANCE_PATHS or rel.startswith(
        "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/proposals/"
    ):
        return False, True, "archive provenance"
    historical = any(token in rel.lower() for token in ("archive/", "history", "superseded", "/v27", "/v46", "manual_adjudication_v2"))
    current_layer = any(token in rel for token in ("manual_adjudication_v4_current_reaudit", "manual_adjudication_v3_baseline_ni", "fair_comparison_v4"))
    publication = rel in {
        "SUMMARY.md",
        "README.md",
        "STATUS.md",
        "final_results/v60_current_vs_x1v2_baseline/README.md",
        "final_results/v60_current_vs_x1v2_baseline/SCHEMA.md",
        "final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md",
    } or current_layer and not historical
    if rel == "final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md":
        return False, True, "redirect"
    if historical:
        return False, True, "historical archive"
    if rel.startswith("discover_matrix/docs/protocol/") or rel.startswith("method/") or rel.startswith("judge/"):
        return publication, False, "protocol-only"
    if publication:
        return True, False, "canonical"
    return False, False, "preserve"


def _resolve_link(path: Path, target: str, repository_root: Path) -> str | None:
    target = target.strip().strip("<>")
    if not target or target.startswith(("#", "http:", "https:", "mailto:", "data:")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    candidate = (path.parent / target).resolve()
    try:
        candidate.relative_to(repository_root.resolve())
    except ValueError:
        return None
    return None if candidate.exists() else target


def _headline_sources(text: str) -> list[str]:
    candidates = (
        "manual_adjudication_v4_current_reaudit",
        "manual_adjudication_v3_baseline_ni",
        "fair_comparison_v4",
        "manual_adjudication_v2",
        "v60_current_vs_x1v2_baseline_v4_cn.md",
        "v60_current_vs_x1v2_baseline_cn.md",
    )
    return [item for item in candidates if item in text]


def _row(path: Path, paper_root: Path, repository_root: Path) -> DocumentationInventoryRow:
    rel = path.relative_to(paper_root).as_posix()
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    publication, historical, action = _classification(path, paper_root, text)
    broken = sorted({bad for target in LINK_RE.findall(text) if path.suffix.lower() == ".md" and (bad := _resolve_link(path, target, repository_root))})
    legacy = sorted({number for number in LEGACY_NUMBERS if number in text})
    versions = sorted(set(VERSION_RE.findall(text)), key=str.lower)
    old_protocols = sorted({protocol for protocol in OLD_PROTOCOLS if protocol in text})
    abs_paths = sorted(set(ABSOLUTE_RE.findall(text)))
    duplicate = []
    if publication and rel != "final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md" and "| v60/current |" in text:
        duplicate.append("current headline metrics are present; keep only the canonical report as the paper table")
    missing = []
    if publication and ("hit@" in text or "precision" in text) and not any(marker in text for marker in ("/", "denom", "分母", "denominator")):
        missing.append("metric text has no nearby numerator/denominator marker")
    file_type = (
        "markdown"
        if path.suffix.lower() == ".md"
        else "manifest"
        if "MANIFEST" in path.name.upper()
        else "inventory"
        if path.name == "publication_docs_inventory_v4.json"
        else "entrance script"
        if path.suffix.lower() == ".py"
        else "json"
    )
    digest = (
        "sha256:dynamic-manifest-see-manifest"
        if file_type in {"manifest", "inventory"}
        else "sha256:" + hashlib.sha256(raw).hexdigest()
    )
    return DocumentationInventoryRow(
        path=rel,
        file_type=file_type,
        publication_surface=publication,
        historical_or_archive=historical,
        headline_sources=_headline_sources(text),
        versions_found=versions,
        legacy_numbers_found=legacy,
        old_protocols_found=old_protocols,
        absolute_paths=abs_paths,
        broken_relative_links=broken,
        duplicate_headline_signals=duplicate,
        missing_unit_or_formula_signals=missing,
        recommended_action=action,
        sha256=digest,
    )


def _tracked_candidates(paper_root: Path, repository_root: Path) -> list[Path]:
    """Return only Git-tracked files under the paper root.

    This prevents unrelated local run products or work-in-progress files from
    silently entering a publication inventory. Newly added publication files
    must be staged before this mode is used.
    """

    relative_root = paper_root.relative_to(repository_root).as_posix()
    output = subprocess.check_output(
        ("git", "ls-files", "-z", "--", relative_root),
        cwd=repository_root,
    )
    return [repository_root / item.decode("utf-8") for item in output.split(b"\0") if item]


def _write_tsv(path: Path, rows: list[DocumentationInventoryRow]) -> None:
    columns = list(DocumentationInventoryRow.model_fields)
    lines = ["\t".join(columns)]
    for row in rows:
        data = row.model_dump(mode="json")
        lines.append("\t".join(json.dumps(data[column], ensure_ascii=False, sort_keys=True) for column in columns))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-tsv", type=Path, required=True)
    parser.add_argument(
        "--tracked-only",
        action="store_true",
        help="Scan only Git-tracked files so unrelated local artifacts cannot enter the inventory.",
    )
    args = parser.parse_args()
    paper_root = args.paper_root.resolve()
    repository_root = args.repository_root.resolve()
    candidates = _tracked_candidates(paper_root, repository_root) if args.tracked_only else list(paper_root.rglob("*"))
    rows = [_row(path, paper_root, repository_root) for path in sorted(candidates) if path.is_file() and _is_candidate(path)]
    inventory = DocumentationInventory(
        schema_version="paper1.publication-docs-inventory.v4",
        repository_root=paper_root.relative_to(Path.cwd().resolve()).as_posix(),
        generated_by=(
            "build_publication_docs_inventory.py --tracked-only; provider-free Git-tracked scan"
            if args.tracked_only
            else "build_publication_docs_inventory.py; provider-free filesystem scan"
        ),
        current_sources={
            "current": "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit",
            "baseline": "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni",
            "comparison": "final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4",
            "narrative": "final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md",
        },
        rows=rows,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(inventory.model_dump_json(indent=2, by_alias=True) + "\n", encoding="utf-8")
    _write_tsv(args.output_tsv, rows)
    print(json.dumps({"rows": len(rows), "publication_rows": sum(row.publication_surface for row in rows), "broken_link_rows": sum(bool(row.broken_relative_links) for row in rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
