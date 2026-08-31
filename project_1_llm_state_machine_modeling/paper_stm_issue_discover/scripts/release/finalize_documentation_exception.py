"""Refresh the bounded final-results documentation hash exception offline.

This intentionally does not modify the immutable release baseline or expand
the exception surface. It only recomputes the current bytes and SHA-256 for
the six documentation paths already approved by the release validator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PAPER_ROOT = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover")
ARCHIVE = PAPER_ROOT / "final_results" / "v60_current_vs_x1v2_baseline"
BASELINE = PAPER_ROOT / "release" / "baseline_manifest.json"
RECORD = PAPER_ROOT / "release" / "documentation_audit" / "final_archive_documentation_changes.json"
PROTECTED_PREFIXES = ("raw/", "derived/", "reference/")
ALLOWED_PATHS = (
    ARCHIVE / "README.md",
    ARCHIVE / "SCHEMA.md",
    ARCHIVE / "archive_manifest.json",
    ARCHIVE / "publication_manifest.json",
    ARCHIVE / "report/v60_current_vs_x1v2_baseline_cn.md",
    ARCHIVE / "reviews/01_numeric_recomputation_review.md",
)


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def finalize(repository_root: Path) -> dict[str, object]:
    """Refresh approved documentation hashes after validating immutable scope."""

    baseline_path = repository_root / BASELINE
    record_path = repository_root / RECORD
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("schema") != "paper1.final-archive-documentation-changes.v1":
        raise ValueError("unexpected documentation exception schema")
    if record.get("archive_root") != ARCHIVE.as_posix() or record.get("baseline_manifest") != BASELINE.as_posix():
        raise ValueError("documentation exception targets the wrong archive or baseline")
    if tuple(record.get("protected_prefixes", ())) != PROTECTED_PREFIXES:
        raise ValueError("documentation exception weakens protected archive prefixes")

    baseline_files = {
        item["path"]: item
        for item in baseline["frozen_archive_files"]
        if isinstance(item, dict)
    }
    changes = record.get("allowed_changes")
    if not isinstance(changes, list):
        raise ValueError("documentation exception allowed_changes must be a list")
    allowed_paths = tuple(path.as_posix() for path in ALLOWED_PATHS)
    actual_paths = tuple(change.get("path") for change in changes if isinstance(change, dict))
    if len(actual_paths) != len(changes) or set(actual_paths) != set(allowed_paths):
        raise ValueError("documentation exception has an unexpected allowed path set")

    protected_count = 0
    archive_prefix = ARCHIVE.as_posix() + "/"
    for path in baseline_files:
        if any(path.startswith(archive_prefix + prefix) for prefix in PROTECTED_PREFIXES):
            protected_count += 1
    if record.get("protected_file_count") != protected_count:
        raise ValueError("documentation exception has the wrong protected file count")

    refreshed: list[dict[str, object]] = []
    for change in changes:
        assert isinstance(change, dict)
        path_text = change["path"]
        baseline_item = baseline_files.get(path_text)
        if baseline_item is None:
            raise ValueError(f"approved documentation path is absent from the release baseline: {path_text}")
        if any(path_text.startswith(archive_prefix + prefix) for prefix in PROTECTED_PREFIXES):
            raise ValueError(f"protected evidence cannot be refreshed: {path_text}")
        if change.get("baseline_bytes") != baseline_item.get("bytes") or change.get("baseline_sha256") != baseline_item.get("sha256"):
            raise ValueError(f"documentation exception baseline mismatch: {path_text}")
        current_path = repository_root / path_text
        if not current_path.is_file():
            raise FileNotFoundError(current_path)
        change["current_bytes"] = current_path.stat().st_size
        change["current_sha256"] = _sha256(current_path)
        refreshed.append(
            {
                "path": path_text,
                "bytes": change["current_bytes"],
                "sha256": change["current_sha256"],
            }
        )

    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "PASS",
        "allowed_paths": len(refreshed),
        "protected_file_count": protected_count,
        "provider_call_count": 0,
        "billable_call_count": 0,
        "refreshed": refreshed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    print(json.dumps(finalize(arguments.repository_root.resolve()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
