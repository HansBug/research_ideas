from __future__ import annotations

import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

from ..report import sha256_file, write_json


def build_recovery_workdir_archive(*, repo_root: Path, workdir: Path, archive_dir: Path, report: dict[str, Any]) -> dict[str, Any]:
    """Package high-cardinality R3.1 recovery artifacts into one zip archive."""

    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / "workdir.zip"
    sha_path = archive_dir / "workdir.zip.sha256"
    manifest_path = archive_dir / "manifest.json"
    files = sorted(p for p in workdir.rglob("*") if p.is_file())
    by_top = Counter(p.relative_to(workdir).parts[0] for p in files if p.relative_to(workdir).parts)
    by_suffix = Counter(p.suffix or "<noext>" for p in files)
    with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            zf.write(path, path.relative_to(workdir).as_posix())
    archive_sha = sha256_file(archive_path)
    sha_path.write_text(f"{archive_sha}  {archive_path.name}\n", encoding="utf-8")
    manifest = {
        "manifest_version": "r3.1.plantuml_recovery_workdir_manifest.v0",
        "archive_path": _rel(archive_path, repo_root),
        "archive_sha256": archive_sha,
        "archive_sha256_path": _rel(sha_path, repo_root),
        "workdir_source_path": _rel(workdir, repo_root),
        "file_count": len(files),
        "by_top_level_dir": dict(sorted(by_top.items())),
        "by_suffix": dict(sorted(by_suffix.items())),
        "report_path": "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/plantuml_recovery_report.json",
        "normalization_ledger_path": report.get("normalization_ledger_path"),
        "run_id": report.get("run_id"),
        "created_at": report.get("created_at"),
        "generator_code_commit": report.get("generator_code_commit"),
        "usage": {
            "verify_sha256": f"cd {_rel(archive_dir, repo_root)} && sha256sum -c {sha_path.name}",
            "list": f"unzip -l {_rel(archive_path, repo_root)} | head",
            "extract": f"mkdir -p /tmp/r3_1_workdir && unzip -q {_rel(archive_path, repo_root)} -d /tmp/r3_1_workdir",
            "path_mapping": "Report item paths under normalized_candidates/ and official_scxml/ are zip member paths relative to the extracted directory.",
        },
    }
    write_json(manifest_path, manifest)
    return manifest


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)
