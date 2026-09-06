"""Collect the completed A2 experiment and verify its immutable file inventory."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

import analyze
from paper_stm_evaluation.final_results_archive import (
    EXCLUDED_RULES, _copy_tree, _file_manifest, _write,
)
from paper_stm_judge.artifacts import stable_model_hash


RUN_ID = "af618190b34652b58ed0ae9ec231bdfe"
PAPER = analyze.PAPER
BASE = PAPER.parents[1] / "runs/paper1/a2_no_predicates_20260906"
DESTINATION = PAPER / "final_results/a2_no_predicates_vs_v61_20260906"


def judge_input_fingerprints(value):
    artifacts = value["artifact_closure"]["artifacts"]
    documents = {row["artifact_id"]: stable_model_hash(row) for row in artifacts}
    assert len(documents) == len(artifacts)
    return dict(documents=documents, expected_issues=stable_model_hash(value["expected_issues"]))


def judge_input_audit(judges):
    reference = {}
    frozen = PAPER / "final_results/v61_source_divergence_vs_x1v2_baseline/raw/judge_v3.11_iter6cfg"
    original = PAPER.parents[1] / "runs/paper1/judge-v61-full-ea6141607"
    for path in sorted(frozen.glob("current-r*/pairs/*.json")):
        pair = analyze.read(path)
        key = pair["pair_id"], pair["round"]
        assert key not in reference
        live = original / path.parents[1].name / "pairs" / path.name
        assert analyze.digest(live) == analyze.digest(path), ("v61 result changed", live)
        source = live.parent.parent / "inputs" / path.name
        value = analyze.read(source)
        assert stable_model_hash(value) == pair["serialized_input_hash"]
        reference[key] = source, value
    assert len(reference) == 162
    rows = []
    for root in judges:
        for path in sorted((root / "pairs").glob("*.json")):
            pair = analyze.read(path)
            source = root / "inputs" / path.name
            value = analyze.read(source)
            assert stable_model_hash(value) == pair["serialized_input_hash"]
            old_path, old = reference[pair["pair_id"], pair["round"]]
            current, baseline = map(judge_input_fingerprints, (value, old))
            assert current == baseline, ("judge evidence changed", source, old_path)
            rows.append(dict(pair_id=pair["pair_id"], round=pair["round"], run_id=root.name,
                             a2_input_sha256=analyze.digest(source), v61_input=str(old_path),
                             v61_input_sha256=analyze.digest(old_path), fingerprints=baseline,
                             closure_metadata_differences=[key for key in value["artifact_closure"]
                                 if key != "artifacts" and value["artifact_closure"][key] != old["artifact_closure"].get(key)]))
    return dict(schema="paper1.a2-judge-input-audit.v1", rows=rows,
                interpretation="Every completed pair's serialized input is verified against its result receipt. All fields of each evidence document and all expected issues match frozen v61 inputs. Reports and outer closure metadata are not asserted equal. Original v61 inputs remain in ignored runs; their file and structured fingerprints are retained here.")


def transport_index(root):
    """Keep observable usage and errors, without copying private prompt streams."""
    rows = []
    for path in sorted((root / "llm").rglob("*")):
        if not path.is_file() or not (path.name == "audit.jsonl" or
                                     path.name.startswith(".audit.jsonl.") and path.suffix == ".part"):
            continue
        events, unreadable = [], []
        for number, line in enumerate(path.read_text().splitlines(), 1):
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                unreadable.append(number)
        retained = []
        for event in events:
            if event.get("usage") or event.get("error") or event.get("status"):
                retained.append({key: event[key] for key in (
                    "seq", "record", "record_type", "operation", "recorded_at_utc", "turn", "status",
                    "model", "profile", "model_call_id", "failed_model_call_id",
                    "logical_model_call_id", "response_id", "usage", "error",
                    "attempt_no", "next_attempt_no", "max_attempts", "retry_after_seconds",
                    "request_fingerprint", "partial_response_observed", "partial_response_discarded",
                    "started_at_utc", "ended_at_utc", "duration_seconds",
                ) if key in event})
        rows.append(dict(path=str(path.relative_to(root)), sha256=analyze.digest(path),
                         records=len(events), unreadable_lines=unreadable,
                         record_types=dict(Counter(str(e.get("record_type", e.get("record"))) for e in events)),
                         events=retained))
    return dict(run_id=root.name, traces=rows,
                interpretation="Observable recorded usage only; interrupted or timed-out requests may have unknown usage. Repeated snapshots are not additive billing rows.")


def analysis_command(archive, output):
    command = [sys.executable, str(analyze.HERE / "analyze.py"),
               "--report-root", str(archive / "raw/inputs"),
               "--ledger", str(archive / "raw/ledger.json"),
               "--a2-selection", str(archive / f"raw/source_runs/{RUN_ID}/continuation_plan.json"),
               "--a2-sources-dir", str(archive / "raw/source_runs"),
               "--output", str(output)]
    for path in sorted((archive / "raw/judge").glob("*/run_manifest.json")):
        command.extend(["--a2-judge-root", str(path.parent)])
    return command


def build(base, archive):
    plan = base / f"method_aizzz/{RUN_ID}/continuation_plan.json"
    roots, selection, _ = analyze.load_selection(plan)
    cells, reports, quarantined, _, attempts = analyze.load_cells(roots, selection=selection)
    assert len(cells) == 162 and all(c["eligible"] for c in cells.values()) and not quarantined
    assert analyze.read(roots[-1] / "continuation_summary.json")["status"] == "terminal"
    judges = sorted(p.parent for parent in (base / "judge", base / "judge_aizzz")
                    for p in parent.glob("*/run_manifest.json"))
    items = analyze.read(PAPER / "discover_matrix/ledger_v2/ledger.json")["items"]
    judged, _, seen, _, _ = analyze.load_judges(judges, cells, reports, items)
    assert seen == set(cells) and set(judged) == set(reports), "A2 judge coverage is incomplete"
    assert not archive.exists(), "Never overwrite a prior archive; validate or finalize it explicitly"
    for source in roots:
        _copy_tree(source, archive / "raw/source_runs" / source.name)
    for source in judges:
        _copy_tree(source, archive / "raw/judge" / source.name)

    input_files = {}
    for row in selection.values():
        for artifact in analyze.read(row["path"])["context_manifest"]["artifacts"]:
            source = Path(artifact["path"])
            previous = input_files.setdefault(source, artifact["sha256"])
            assert previous == artifact["sha256"]
    input_root = next(path.parents[2] for path in input_files if path.name == "nl.txt")
    for source, expected_hash in input_files.items():
        assert analyze.digest(source) == expected_hash, ("input changed", source)
        target = archive / "raw/inputs" / source.relative_to(input_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(PAPER / "discover_matrix/ledger_v2/ledger.json", archive / "raw/ledger.json")

    for name in ("provider_configurations.json", "dependency_versions.json", "aizzz-cutover.json",
                 "runtime-cutover.json", "original_final_audit.json", "continuation_final_audit.json",
                 "aizzz_final_audit.json", "aizzz_method.py", "aizzz_judge.py", "audit_run.py"):
        source = base / "checks" / name
        target = archive / "raw/checks" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    _write(archive / "raw/transport_audit.json", [transport_index(root) for root in roots + judges])
    _write(archive / "provenance.json", dict(
        schema="paper1.a2-archive-provenance.v1", human_confirmations=0,
        source_roots=[str(root) for root in roots], judge_roots=[str(root) for root in judges],
        input_root=str(input_root), input_files=len(input_files), predecessor_attempts=attempts,
        selection_sha256=analyze.digest(plan), reference="../v61_source_divergence_vs_x1v2_baseline",
        raw_policy="Original bytes and run identities preserved. Inputs are relocated without rewriting historical manifest hashes. Provider streams stay in ignored runs; their hashes, usage and errors are indexed separately.",
    ))
    subprocess.run(analysis_command(archive, archive / "derived/analysis.json"), check=True, stdout=subprocess.DEVNULL)
    result = analyze.read(archive / "derived/analysis.json")
    assert result["a2"]["precision_complete"] and result["a2"]["coverage"]["judged_cells"] == 162
    _write(archive / "derived/judge_input_audit.json", judge_input_audit(judges))
    for name in ("case_audit.json", "change_audit.json"):
        shutil.copy2(analyze.HERE / name, archive / "derived" / name)
    finalize(archive)
    validate(archive)
    print(json.dumps(result["a2"]["metrics"], indent=2))


def finalize(archive):
    assert analyze.read(archive / "derived/analysis.json")["a2"]["precision_complete"]
    _write(archive / "archive_manifest.json", dict(
        schema="paper1.final-results-archive.v1", batch="a2_no_predicates_vs_v61_20260906",
        generated_at_utc=datetime.now(timezone.utc).isoformat(), generator=str(Path(__file__)),
        included_files=_file_manifest(archive, excluded_relative_paths={"archive_manifest.json"}),
        excluded_rules=[dict(row, reason="Interrupted provider streams remain in ignored runs; their hashes and observable errors/usage are retained in raw/transport_audit.json.")
                        if "*.part" in row["rule"] else row for row in EXCLUDED_RULES],
    ))


def validate(archive):
    manifest = analyze.read(archive / "archive_manifest.json")
    assert manifest["included_files"] == _file_manifest(archive, excluded_relative_paths={"archive_manifest.json"})
    result = analyze.read(archive / "derived/analysis.json")
    coverage = result["a2"]["coverage"]
    assert result["a2"]["precision_complete"]
    assert coverage["terminal_cells"] == coverage["eligible_cells"] == coverage["judged_cells"] == 162
    assert coverage["planned_expected_rounds"] == coverage["observed_expected_rounds"] == 435
    assert coverage["eligible_reports"] == coverage["judged_reports"]
    changes = {(r["ledger_id"], r["round"]): r["change"] for r in result["changes"]}
    reviewed = analyze.read(archive / "derived/change_audit.json")["rows"]
    assert len(reviewed) == len(changes), "Every changed expected-round needs a separate audit row"
    assert {(r["ledger_id"], r["round"]): r["change"] for r in reviewed} == changes
    inputs = analyze.read(archive / "derived/judge_input_audit.json")["rows"]
    assert len(inputs) == len({(r["pair_id"], r["round"]) for r in inputs}) == 162
    for row in inputs:
        path = archive / "raw/judge" / row["run_id"] / "inputs" / f"{row['pair_id']}.json"
        assert analyze.digest(path) == row["a2_input_sha256"]
        assert judge_input_fingerprints(analyze.read(path)) == row["fingerprints"]
    print(json.dumps(dict(verified_files=len(manifest["included_files"]), coverage=coverage), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "finalize", "validate"))
    parser.add_argument("--run-root", type=Path, default=BASE)
    parser.add_argument("--archive", type=Path, default=DESTINATION)
    args = parser.parse_args()
    if args.action == "build":
        build(args.run_root.resolve(), args.archive.resolve())
    elif args.action == "finalize":
        finalize(args.archive.resolve())
    else:
        validate(args.archive.resolve())
