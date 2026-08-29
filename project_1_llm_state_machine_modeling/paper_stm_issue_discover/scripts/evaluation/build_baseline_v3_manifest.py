#!/usr/bin/env python3
"""Build versioned archive and publication manifests for baseline v3."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAL_FILES = (
    "README.md",
    "schema.md",
    "protocol_freeze_v3_baseline_ni.md",
    "inventory.json",
    "frozen_k_snapshot_v3.json",
    "pane5_adjudications_v3.json",
    "pane5_decision_register.json",
    "pane5_evidence_reads_v3.json",
    "baseline_report_decisions_v3.json",
    "baseline_report_decisions_v3.tsv",
    "baseline_relation_decisions_v3.json",
    "baseline_relation_decisions_v3.tsv",
    "baseline_relation_projection_v3.json",
    "baseline_relation_projection_v3.tsv",
    "baseline_n_groups_v3.json",
    "baseline_n_groups_v3.tsv",
    "baseline_combined_512_v3.json",
    "reference_ledger_aggregate_v3.json",
    "summary_v3.json",
    "recomputed_summary_v3.json",
    "baseline_audit_log_v3.json",
    "review_log_v3.json",
    "proposals/track_a_0000_0019.json",
    "proposals/track_a_0000_0019.manifest.json",
    "proposals/track_a_0000_0019.md",
    "proposals/track_a_0020_0039.json",
    "proposals/track_a_0040_0059.json",
    "proposals/track_b_0000_0019.json",
    "proposals/track_b_0000_0019_missing_non_k.json",
    "proposals/track_b_0020_0039.json",
    "proposals/track_b_0040_0059.json",
)

EXCLUDED_FILES = {
    "proposals/track_b_full_0000_0059.json": "Broad legacy envelope contains a v2 proposal source and is excluded by the canonical builder.",
    "proposals/track_b_full_legacy.json": "Historical duplicate of the broad v2-derived envelope; retained but excluded from formal review input.",
    "proposals/raw_scope_probe_0000_0019.json": "Raw scope diagnostic, not a reviewer proposal or final decision input.",
    "proposals/track_b_0020_0059.json": "Broad pair-range proposal; exact pair batches are the only admissible Track B inputs.",
}


def sha256(path: Path) -> str:
    """Return a prefixed SHA-256 digest for exact file bytes."""
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def file_entry(root: Path, relative: str) -> dict[str, Any]:
    """Describe one existing output file."""
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError(relative)
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    """Write two manifests without including either manifest in its own file list."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    outputs = [file_entry(v3, item) for item in FORMAL_FILES]
    reviews = []
    review_root = v3 / "reviews"
    for path in sorted(review_root.glob("*")):
        if path.is_file():
            reviews.append(file_entry(v3, path.relative_to(v3).as_posix()))
    inputs = []
    for relative in (
        "reference/ledger.json",
        "reference/x1v2_input_closure/manifest.json",
        "raw/x1v2_baseline/archive_manifest.json",
        "derived/manual_adjudication_v2/MANIFEST",
        "derived/manual_adjudication_v2/x1v2_report_decisions.json",
        "derived/manual_adjudication_v2/summary.json",
    ):
        inputs.append(file_entry(archive, relative))
    manifest = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.manifest",
        "artifact_id": "x1v2-baseline-non-k-v3",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": "Frozen X1v2 baseline K rows plus the complete v3 re-review of the 233 non-K rows; no v60/current rows are canonical outputs here.",
        "superseded_v2": {
            "status": "preserved_historical_input",
            "path": "derived/manual_adjudication_v2",
            "not_used_as_independent_v3_opinion": True,
        },
        "inputs": inputs,
        "outputs": outputs,
        "review_outputs": reviews,
        "excluded_outputs": [{"path": path, "reason": reason} for path, reason in sorted(EXCLUDED_FILES.items())],
        "execution_boundary": {
            "provider_calls": 0,
            "method_reruns": 0,
            "judge_reruns": 0,
            "raw_modified": False,
            "current_modified": False,
        },
        "recompute_command": "PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_baseline_v3_summary.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json",
    }
    for name, artifact_id in (
        ("archive_manifest_v3_baseline_ni.json", "x1v2-baseline-non-k-v3-archive"),
        ("publication_manifest_v3_baseline_ni.json", "x1v2-baseline-non-k-v3-publication"),
    ):
        value = dict(manifest)
        value["artifact_id"] = artifact_id
        (v3 / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "outputs": len(outputs), "reviews": len(reviews), "excluded": len(EXCLUDED_FILES), "provider_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
