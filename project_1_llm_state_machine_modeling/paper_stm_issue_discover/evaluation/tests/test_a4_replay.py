"""Source-backed A4 masking and deterministic accounting, with no provider calls."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from paper_stm_evaluation.a4_accounting import account_cell, claim, report_projection
from paper_stm_evaluation.a4_replay import mask_prepared, restore_plan, TailRuntime
from paper_stm_method.orchestration.runner import _prepared_is_finding_candidate
from paper_stm_method.semantics.adjudication import SemanticAdjudication, adjudicate_disposition
from paper_stm_method.semantics.adjudication import DAdjudicationResponse
from utils.structured_runtime import FixtureStructuredRuntime


PAPER = Path(__file__).resolve().parents[2]
RAW = PAPER / "final_results/v61_source_divergence_vs_x1v2_baseline/raw"


@pytest.fixture(scope="module")
def source():
    return json.loads((RAW / "v61_current/method/method/0000/round-1.json").read_text())


@pytest.fixture(scope="module")
def judge():
    return json.loads((RAW / "judge_v3.11_iter6cfg/current-r1/pairs/0000.json").read_text())


def test_all_verdicts_have_identical_mask_and_static_inputs_survive(source):
    raw = source["stage_outputs"]["execute_batch"]["candidates"][0]
    before = deepcopy(raw)
    views = []
    for verdict in ("true", "false", "unknown"):
        variant = deepcopy(raw)
        variant["receipt"].update(verdict=verdict, reason="SECRET RESULT", basis="SECRET RESULT",
                                  trace=[{"value": "SECRET RESULT"}], counterexample=[{"secret": True}],
                                  run_metadata={"secret": "SECRET RESULT"})
        variant["old_d"] = "SECRET RESULT"
        view = mask_prepared(variant)
        assert _prepared_is_finding_candidate(view)
        assert view["candidate"].model_dump(mode="json") == raw["candidate"]
        assert view["plan"].model_dump(mode="json") == raw["plan"]
        assert view["binding"].model_dump(mode="json") == raw["binding"]
        views.append({key: value.model_dump(mode="json") if hasattr(value, "model_dump") else value
                      for key, value in view.items()})
    assert views[0] == views[1] == views[2]
    assert "SECRET RESULT" not in json.dumps(views)
    assert raw == before


def test_true_override_is_removed_but_independent_semantic_rejection_survives(source):
    raw = next(item for item in source["stage_outputs"]["execute_batch"]["candidates"]
               if item["receipt"]["verdict"] == "true" and item["binding"]["precise"])
    item = mask_prepared(raw)
    semantic = SemanticAdjudication(
        obligation_id=item["obligation_id"], grounding="established",
        violated_obligation="Synthetic test-only decision", strongest_defeater=None,
        defeater_kind="none", defeater_disposition="defeated",
        reason="Test fixture, not an experimental result.", basis="Synthetic enum branch.",
    )
    disposition = adjudicate_disposition(item["candidate"], item["binding"], semantic, item["receipt"])
    assert disposition["d_level"] == "D2"
    rejected = semantic.model_copy(update={"grounding": "not_established"})
    assert adjudicate_disposition(item["candidate"], item["binding"], rejected, item["receipt"])["d_level"] == "D0"


def test_tail_runtime_rejects_upstream_calls():
    class Runtime:
        def call(self, **kwargs):
            pytest.fail("Upstream request reached provider")
    with pytest.raises(RuntimeError, match="upstream"):
        TailRuntime(Runtime()).call(kind="discovery_grounding")


def test_full_wording_only_reuses_but_changed_claim_does_not(source, judge):
    replay = deepcopy(source)
    for report in replay["report_issue_clusters"]:
        report["reason"] = "Rephrased explanation."
        report["basis"] = "Rephrased input basis."
    accounting = account_cell(source, judge, replay)
    assert {row["route"] for row in accounting["reports"]} == {"reused_full"}
    assert accounting["pending"] == 0
    replay["report_issue_clusters"][0]["expected"] = "A different substantive requirement."
    changed = account_cell(source, judge, replay)
    assert changed["reports"][0]["route"] == "residual"


def test_oracle_precedes_reuse_and_mixed_facets_count_once(source, judge):
    original = deepcopy(source)
    report = original["report_issue_clusters"][0]
    obligation = report["obligation_id"]
    candidate = next(item for item in original["stage_outputs"]["execute_batch"]["candidates"]
                     if item["obligation_id"] == obligation)
    candidate["receipt"]["verdict"] = "true"
    replay = deepcopy(source)
    row = account_cell(original, judge, replay)["reports"][0]
    assert row["route"] == "oracle_true_I"
    assert row["outcome"]["validity"] == "INVALID"
    assert row["oracle_true_obligation_ids"] == [obligation]
    root, child = deepcopy(replay["report_issue_clusters"][:2])
    root["folded_sub_claims"] = [{"issue_id": child["issue_id"]}]
    replay["report_issue_clusters"] = [root]
    rows = account_cell(original, judge, replay)["reports"]
    assert len(rows) == 1 and rows[0]["route"] == "oracle_true_I"
    evidence = next(item for item in replay["evidence_records"] if item["obligation_id"] == obligation)
    evidence["observed"] = "A reversed and unrelated substantive claim."
    assert account_cell(original, judge, replay)["reports"][0]["route"] == "residual"


def test_audit_probe_does_not_trigger_oracle_and_zero_reports_have_zero_denominator(source, judge):
    replay = deepcopy(source)
    report = replay["report_issue_clusters"][0]
    report["audit_probe"] = {"verdict": "true"}
    assert account_cell(source, judge, replay)["reports"][0]["route"] == "reused_full"
    replay["report_issue_clusters"] = []
    result = account_cell(source, judge, replay)
    assert result["reports"] == [] and result["pending"] == 0
    assert result["completed_zero_report_cell"]
    assert len(result["disappeared_or_changed_full_report_ids"]) == len(source["report_issue_clusters"])


def test_extra_facet_prevents_reuse(source):
    replay = deepcopy(source)
    a, b = replay["report_issue_clusters"][:2]
    a.setdefault("folded_sub_claims", []).append({"issue_id": b["issue_id"]})
    assert report_projection(source, source["report_issue_clusters"][0]) != report_projection(replay, a)


def test_stage_cache_is_namespace_bound_and_rejects_corruption(tmp_path):
    class TestRuntime(FixtureStructuredRuntime):
        count = 0

        def call(self, **kwargs):
            self.count += 1
            # Test-only provenance exercises the live-cache gate without a provider.
            return super().call(**kwargs).model_copy(update={"real_llm": True})

    inner = TestRuntime()
    args = dict(kind="d_adjudication", schema=DAdjudicationResponse, system_prompt="Fixture",
                prompt="Fixture", artifact_id="method/0000/round-1/d-adjudication")
    runtime = TailRuntime(inner, tmp_path, "source-A")
    runtime.call(**args)
    runtime.call(**args)
    assert inner.count == 1 and runtime.calls[-1]["reused"]
    TailRuntime(inner, tmp_path, "source-B").call(**args)
    assert inner.count == 2
    cache = tmp_path / (runtime.calls[0]["cache_key"].removeprefix("sha256:") + ".json")
    saved = json.loads(cache.read_text())
    saved["identity"]["namespace"] = "full-old-cache"
    cache.write_text(json.dumps(saved))
    with pytest.raises(ValueError, match="provenance mismatch"):
        runtime.call(**args)
