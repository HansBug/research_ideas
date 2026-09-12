"""Build a provider-free raw report inventory for manual adjudication v2."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from paper_stm_evaluation.manual_adjudication import RawInventory, RawReportRef


def sha256_file(path: Path) -> str:
    """Hash one immutable input file without reading credentials or provider streams."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_json(path: Path) -> dict:
    """Load one raw JSON object and reject malformed archive inputs."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def build_inventory(archive: Path) -> RawInventory:
    """Enumerate both frozen method arms and preserve exact raw JSON pointers."""

    raw = archive / "raw"
    items: list[RawReportRef] = []
    cells: dict[str, int] = {}
    reports: dict[str, int] = {}
    by_round: dict[str, dict[str, int]] = {}

    current_paths = sorted((raw / "v60_current" / "method" / "method").glob("*/*.json"))
    cells["v60_current"] = len(current_paths)
    for path in current_paths:
        data = load_json(path)
        pair_id = str(data["pair_id"])
        round_no = int(data["round"])
        issues = data.get("report_issue_clusters")
        if not isinstance(issues, list):
            raise ValueError(f"v60 cell lacks report_issue_clusters: {path}")
        for index, issue in enumerate(issues):
            if not isinstance(issue, dict) or not issue.get("issue_id"):
                raise ValueError(f"v60 report lacks issue_id: {path}#{index}")
            items.append(RawReportRef(
                side="v60_current", pair_id=pair_id, round=round_no,
                report_id=str(issue["issue_id"]), report_index=index,
                raw_method_path=str(path.relative_to(archive)),
                raw_json_pointer=f"/report_issue_clusters/{index}",
                raw_sha256=sha256_file(path),
                claim_pointer=f"/report_issue_clusters/{index}/issue_id",
                where_pointer=f"/report_issue_clusters/{index}/element_refs",
                identity_basis="report_issue_clusters[index].issue_id is the frozen method publication identity.",
            ))

    baseline_paths = sorted((raw / "x1v2_baseline" / "method").glob("run*/*/record.json"))
    cells["x1v2_baseline"] = len(baseline_paths)
    baseline_identity: dict[tuple[str, int, int], str] = {}
    witness_file = archive / "derived" / "x1v2_witness_level_audit.json"
    if not witness_file.is_file():
        raise ValueError("X1v2 witness provenance is required to assign stable report identities")
    witness = load_json(witness_file)
    for record in witness.get("records", []):
        work_item = record.get("work_item", {})
        record_path = str(work_item.get("method_record_repository_path", ""))
        marker = "final_results/v60_current_vs_x1v2_baseline/"
        if marker in record_path:
            record_path = record_path.split(marker, 1)[1]
            record_path = "final_results/v60_current_vs_x1v2_baseline/" + record_path
        prefix = "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
        if record_path.startswith(prefix):
            record_path = record_path.removeprefix(prefix)
        if record_path.startswith("final_results/v60_current_vs_x1v2_baseline/"):
            record_path = record_path.removeprefix("final_results/v60_current_vs_x1v2_baseline/")
        key = (record_path, int(work_item.get("round", 0)), int(work_item.get("original_finding_index", -1)))
        report_id = work_item.get("original_report_id")
        if key[0] and key[1] > 0 and key[2] >= 0 and report_id:
            baseline_identity[key] = str(report_id)
    for path in baseline_paths:
        data = load_json(path)
        pair_id = str(data["case"])
        round_no = int(data["round"])
        issues = data.get("parsed_output", {}).get("issues")
        if not isinstance(issues, list):
            raise ValueError(f"baseline cell lacks parsed_output.issues: {path}")
        relative = str(path.relative_to(archive))
        for index, issue in enumerate(issues):
            if not isinstance(issue, dict):
                raise ValueError(f"baseline finding is not an object: {path}#{index}")
            report_id = baseline_identity.get((relative, round_no, index))
            if report_id is None:
                raise ValueError(f"baseline witness provenance does not close over {relative}#{index}")
            identity_basis = "Identity is cross-checked against the archived X1v2 witness work_item path/index; it is not a semantic label."
            items.append(RawReportRef(
                side="x1v2_baseline", pair_id=pair_id, round=round_no,
                report_id=report_id, report_index=index, raw_method_path=relative,
                raw_json_pointer=f"/parsed_output/issues/{index}", raw_sha256=sha256_file(path),
                claim_pointer=f"/parsed_output/issues/{index}/issue",
                where_pointer=f"/parsed_output/issues/{index}/where",
                identity_basis=identity_basis,
            ))

    items.sort(key=lambda item: (item.side.value, item.raw_method_path, item.report_index))
    for side in ("v60_current", "x1v2_baseline"):
        side_items = [item for item in items if item.side.value == side]
        reports[side] = len(side_items)
        by_round[side] = {str(round_no): sum(item.round == round_no for item in side_items) for round_no in (1, 2, 3)}

    # The two raw-arm manifests are frozen inputs.  The top-level archive and
    # publication manifests describe this mutable release surface, so treating
    # them as inventory inputs creates a circular hash dependency at finalize.
    manifest_paths = {
        str(path.relative_to(archive)): sha256_file(path)
        for path in (
            raw / "v60_current" / "archive_manifest.json",
            raw / "x1v2_baseline" / "archive_manifest.json",
        )
        if path.is_file()
    }
    return RawInventory(
        archive_relative_root="final_results/v60_current_vs_x1v2_baseline",
        generated_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        source_manifests=manifest_paths, cells=cells, reports=reports, by_round=by_round, items=tuple(items)
    )


def main() -> None:
    """Run the deterministic inventory command."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inventory = build_inventory(args.archive_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"schema": inventory.schema, "cells": inventory.cells, "reports": inventory.reports, "by_round": inventory.by_round}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
