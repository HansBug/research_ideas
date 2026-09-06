"""Check fixed report denominators, multi-target hits, and cluster resampling."""

import importlib.util
import json
from pathlib import Path
import shutil
import sys

import pytest


spec = importlib.util.spec_from_file_location("a2_analysis", Path(__file__).with_name("analyze.py"))
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def test_frozen_metrics_preserve_report_denominators_and_distinct_hit_units():
    items = {"a": {"L": "L0"}, "b": {"L": "L2"}}
    reports = []
    for i, (rnd, validity, tier, targets) in enumerate((
        (1, "VALID_KNOWN", "D0", ["a", "b"]),
        (1, "VALID_KNOWN", "D2", ["a"]),
        (2, "VALID_KNOWN", "D1", ["a"]),
        (3, "VALID_NOVEL", "D2", []),
        (3, "INVALID", None, []),
    )):
        reports.append(dict(original_report_id=str(i), pair_id="0000", round=rnd,
                            validity=validity, d_tier=tier, a0_subtype=None if tier else "FALSE_POSITIVE",
                            full_ledger_ids=targets, partial_ledger_ids=[]))
    result = analysis.quality(reports, items)
    assert [result[k] for k in ("reports", "K", "N", "I")] == [5, 3, 1, 1]
    assert result["precision"] == analysis.ratio(4, 5)
    assert result["hit1"] == analysis.ratio(3, 6)
    assert result["hit3"] == analysis.ratio(2, 2)
    assert result["hitall"] == analysis.ratio(0, 2)
    assert result["strict"]["precision"] == analysis.ratio(3, 5)
    assert result["strict"]["hit1"] == analysis.ratio(2, 6)
    same = dict(per_cluster={str(i): result for i in range(9)})
    compared = analysis.paired_uncertainty(same, same)
    for metric in compared["metrics"].values():
        assert metric["a2_minus_v61"] == 0 and metric["percentile95"] == [0, 0]
        assert metric["defined_replicates"] == 10000
    empty = analysis.quality([], items)
    zero = dict(per_cluster={str(i): empty for i in range(9)})
    undefined = analysis.paired_uncertainty(zero, same)
    assert undefined["metrics"]["precision"]["undefined_replicates"] == 10000
    assert undefined["metrics"]["precision"]["percentile95"] is None
    json.dumps(undefined, allow_nan=False)


def test_judge_loader_preserves_failures_and_rejects_protocol_drift(tmp_path):
    source = tmp_path / "method.json"
    source.write_text("{}\n")
    root = tmp_path / "judge"
    (root / "pairs").mkdir(parents=True)
    (root / "failures").mkdir()
    manifest = dict(judge_algorithm_version="semantic-judge.two-stage.v3.11",
                    protocol_sha256="d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210",
                    k_closure="relation_first", closure_profile="full", validity_readings=2,
                    validity_aggregation="arbitration", validity_arbitration_trigger="any",
                    model_profile="gpt-5.6-luna", selected_pair_ids=["0000", "0001"],
                    selected_rounds=[1], run_id="test")
    manifest_path = root / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    failure_path = root / "failures/0001.json"
    failure_path.write_text(json.dumps(dict(pair_id="0001", round=1, error_type="RuntimeError")))
    result_path = root / "pairs/0000.json"
    result_path.write_text(json.dumps(dict(pair_id="0000", round=1, run_id="test", status="completed",
                                         adapter_audit=dict(source_hash=analysis.digest(source)),
                                         report_outcomes=[], expected_outcomes=[])))
    cells = {(p, 1): dict(eligible=True, source=str(source)) for p in ("0000", "0001")}
    reports, expected, judged, hashes, failures = analysis.load_judges([root], cells, {}, {})
    assert reports == expected == {} and judged == {("0000", 1)}
    assert set(cells) - judged == {("0001", 1)}
    assert failures[0]["pair_id"] == "0001" and hashes[str(failure_path)] == analysis.digest(failure_path)
    manifest["model_profile"] = "aizzz-luna-eval"
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(FileNotFoundError):
        analysis.load_judges([root], cells, {}, {})
    provider = dict(run_id="test", profile="aizzz-luna-eval", model="gpt-5.6-luna",
                    model_config_hash=analysis.LUNA_CONFIGS["aizzz-luna-eval"], endpoint="https://api.aizzz.xyz/v1")
    (root / "provider_identity.json").write_text(json.dumps(provider))
    assert analysis.load_judges([root], cells, {}, {})[2] == judged
    provider["model_config_hash"] = "unregistered endpoint"
    (root / "provider_identity.json").write_text(json.dumps(provider))
    with pytest.raises(AssertionError):
        analysis.load_judges([root], cells, {}, {})
    manifest["model_profile"] = "gpt-5.6-luna"
    manifest["protocol_sha256"] = "different protocol"
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(AssertionError):
        analysis.load_judges([root], cells, {}, {})


def test_provider_sensitivity_pairs_the_same_cells_and_keeps_unknowns():
    current = dict(cells=[dict(pair_id="0000", round=1, model_profile="old", eligible=True),
                          dict(pair_id="0000", round=2, model_profile="new", eligible=True)],
                   reports=[dict(pair_id="0000", round=1, validity="VALID_NOVEL")],
                   expected=[dict(pair_id="0000", round=1, hit=False, observed=True),
                             dict(pair_id="0000", round=2, hit=None, observed=False)],
                   coverage=dict(missing_judge_cells=[["0000", 2]]))
    reference = dict(reports=[dict(pair_id="0000", round=1, validity="INVALID"),
                             dict(pair_id="0000", round=2, validity="VALID_KNOWN")],
                     expected=[dict(pair_id="0000", round=1, hit=False, observed=True),
                               dict(pair_id="0000", round=2, hit=True, observed=True)])
    result = analysis.provider_paired_sensitivity(current, reference)["segments"]
    assert result["old"]["differences"] == dict(precision=1, hit=0)
    assert result["old"]["v61"]["reports"] == 1
    assert result["new"]["a2"]["hit"] == analysis.ratio(0, 1)
    assert result["new"]["v61"]["hit"] == analysis.ratio(1, 1)
    assert result["new"]["differences"] == dict(precision=None, hit=None)
    current["cells"][0]["eligible"] = False
    assert not analysis.provider_paired_sensitivity(current, reference)["segments"]["old"]["complete"]


def test_shared_text_audit_requires_exact_text_and_does_not_relabel():
    common = dict(pair_id="0000", round=1, title="shared", expected="one", observed="two",
                  a0_subtype=None, partial_ledger_ids=[], judge_source="source")
    old = dict(common, original_report_id="old", validity="INVALID", d_tier="D0", full_ledger_ids=[])
    new = dict(common, original_report_id="new", validity="VALID_KNOWN", d_tier="D2", full_ledger_ids=["a"])
    result = analysis.shared_report_text_audit(dict(reports=[new]), dict(reports=[old]))
    assert result["matched_text_groups"] == result["classification_changed_groups"] == result["full_targets_changed_groups"] == 1
    assert old["validity"] == "INVALID" and new["validity"] == "VALID_KNOWN"
    new["observed"] = "two "
    assert analysis.shared_report_text_audit(dict(reports=[new]), dict(reports=[old]))["matched_text_groups"] == 0


def test_cell_selection_preserves_attempts_and_rejects_changed_reused_bytes(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    paths = []
    for root, status in ((old, "failed_with_receipt"), (new, "completed")):
        (root / "method/0000").mkdir(parents=True)
        identity = dict(ablation="no-predicates", run_id=root.name, run_contract_hash="contract-" + root.name,
                        source_provenance={"source_commit": root.name})
        (root / "run_manifest.json").write_text(json.dumps(dict(**identity, pair_input_hashes={"0000": "input"})))
        path = root / "method/0000/round-1.json"
        path.write_text(json.dumps(dict(**identity, pair_id="0000", round=1, status=status, eligible=root == new,
                                       pair_input_hash="input", predicate_execution_receipts=[], report_issue_clusters=[])))
        paths.append(path)
    with pytest.raises(AssertionError, match="duplicate method cell"):
        analysis.load_cells([old, new])
    selected = {("0000", 1): dict(path=paths[1].resolve(), expected_hash=analysis.digest(paths[1]), action="reuse")}
    cells, reports, quarantined, hashes, attempts = analysis.load_cells([old, new], selection=selected)
    assert cells["0000", 1]["source"] == str(paths[1]) and cells["0000", 1]["eligible"]
    assert reports == {} and quarantined == [] and len(attempts) == 1
    assert attempts[0]["path"] == str(paths[0]) and str(paths[0]) in hashes
    paths[1].write_text(paths[1].read_text() + "\n")
    with pytest.raises(AssertionError):
        analysis.load_cells([old, new], selection=selected)


def test_frozen_selection_relocates_without_rewriting_original_identity(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    pairs = [f"{p:04d}" for p in range(60) if p % 10 != 8]
    common = dict(ablation="no-predicates", selected_pair_ids=pairs, rounds=3,
                  model_config_hash="model", prompt_schema_hash="prompt", input_data_hash="data",
                  pair_input_hashes={p: "input" for p in pairs}, registry_hash="registry")
    for root in (old, new):
        root.mkdir()
        manifest = dict(**common, run_id=root.name, source_provenance={"source_commit": root.name}, run_contract_hash=root.name)
        (root / "run_manifest.json").write_text(json.dumps(manifest))
    cell = old / "method/0000/round-1.json"
    cell.parent.mkdir(parents=True)
    cell.write_text("{}\n")
    rows = [dict(pair_id=p, round=r, action="recover", old_path=None, old_hash=None) for p in pairs for r in (1, 2, 3)]
    rows[0].update(action="reuse", old_path=str(cell), old_hash=analysis.digest(cell))
    plan = dict(schema="a2.transport-continuation.v1", root=str(new), run_id=new.name, source_roots=[str(old)],
                identity={k: manifest[k] for k in ("source_provenance", "run_contract_hash")}, selection=rows, planned_cells=162)
    path = new / "continuation_plan.json"
    path.write_text(json.dumps(plan))
    archive = tmp_path / "archive"
    for root in (old, new):
        shutil.copytree(root, archive / root.name)
    _, original, _ = analysis.load_selection(path)
    _, relocated, hashes = analysis.load_selection(archive / "new/continuation_plan.json", sources_dir=archive)
    assert set(original) == set(relocated) and len(relocated) == 162
    assert relocated["0000", 1]["path"] == archive / "old/method/0000/round-1.json"
    assert relocated["0000", 2]["path"] == archive / "new/method/0000/round-2.json"
    assert set(hashes.values()) == {analysis.digest(path)}
    plan["schema"] = "a2.provider-cutover.v1"
    for source, profile in ((old, "gpt-5.6-luna"), (new, "aizzz-luna-eval")):
        mp = archive / source.name / "run_manifest.json"
        value = json.loads(mp.read_text())
        value.update(profile=profile, model_config_hash=analysis.LUNA_CONFIGS[profile])
        mp.write_text(json.dumps(value))
    migrated = archive / "new/continuation_plan.json"
    migrated.write_text(json.dumps(plan))
    analysis.load_selection(migrated, sources_dir=archive)
    mp = archive / "new/run_manifest.json"
    value["model_config_hash"] = "unregistered endpoint"
    mp.write_text(json.dumps(value))
    with pytest.raises(AssertionError, match="unregistered model configuration"):
        analysis.load_selection(migrated, sources_dir=archive)
    value["model_config_hash"] = analysis.LUNA_CONFIGS["aizzz-luna-eval"]
    mp.write_text(json.dumps(value))
    cell.write_text("changed original\n")
    analysis.load_selection(archive / "new/continuation_plan.json", sources_dir=archive)
    with pytest.raises(AssertionError, match="frozen predecessor changed"):
        analysis.load_selection(path)


def test_archive_retains_partial_transport_evidence_and_detects_inventory_drift(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "analyze", analysis)
    spec = importlib.util.spec_from_file_location("a2_archive", Path(__file__).with_name("archive.py"))
    archive = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(archive)
    source = tmp_path / "source"
    (source / "llm").mkdir(parents=True)
    trace = source / "llm/.audit.jsonl.interrupted.part"
    trace.write_text(json.dumps(dict(seq=1, record_type="model", status="completed",
                                    usage={"input_tokens": 12}, system_prompt="private prompt")) + "\n" +
                     json.dumps(dict(seq=2, error={"code": "provider_timeout"}, attempt_no=1, operation="scheduled")) + "\n{" )
    index = archive.transport_index(source)
    row = index["traces"][0]
    assert row["records"] == 2 and row["unreadable_lines"] == [3]
    assert row["events"][0]["usage"] == {"input_tokens": 12}
    assert row["events"][1]["error"] == {"code": "provider_timeout"}
    assert row["events"][1]["operation"] == "scheduled"
    assert "private prompt" not in json.dumps(index)
    destination = tmp_path / "archive"
    coverage = dict(terminal_cells=162, eligible_cells=162, judged_cells=162,
                    planned_expected_rounds=435, observed_expected_rounds=435,
                    eligible_reports=1, judged_reports=1)
    archive._write(destination / "derived/analysis.json", dict(a2=dict(precision_complete=True, coverage=coverage), changes=[]))
    archive._write(destination / "derived/change_audit.json", dict(rows=[]))
    input_value = dict(artifact_closure=dict(artifacts=[dict(artifact_id="nl", content="source", authority="author")]),
                       expected_issues=[dict(ledger_id="known")])
    changed = json.loads(json.dumps(input_value))
    changed["artifact_closure"]["closure_hash"] = "path-dependent hash"
    changed["reports"] = [dict(claim="different method result")]
    assert archive.judge_input_fingerprints(input_value) == archive.judge_input_fingerprints(changed)
    changed["artifact_closure"]["artifacts"][0]["authority"] = "converter"
    assert archive.judge_input_fingerprints(input_value) != archive.judge_input_fingerprints(changed)
    input_rows = []
    for pair in range(54):
        for rnd in (1, 2, 3):
            path = destination / f"raw/judge/r{rnd}/inputs/{pair:04d}.json"
            archive._write(path, input_value)
            input_rows.append(dict(pair_id=f"{pair:04d}", round=rnd, run_id=f"r{rnd}",
                                   a2_input_sha256=analysis.digest(path), fingerprints=archive.judge_input_fingerprints(input_value)))
    archive._write(destination / "derived/judge_input_audit.json", dict(rows=input_rows))
    archive.finalize(destination)
    archive.validate(destination)
    (destination / "unexpected.json").write_text("{}")
    with pytest.raises(AssertionError):
        archive.validate(destination)
