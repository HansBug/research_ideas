from __future__ import annotations

import pandas as pd

from . import benchmark as benchmark_module
from .benchmark import (
    BenchmarkTask,
    _agent_critical_issue_set,
    _agent_issue_set,
    _build_phase14_lofo_gate,
    _build_phase14_lockbox_gate,
    _build_phase14_promotion_evaluation,
    _build_phase15_report_comparison,
    _evaluate_task_bundle,
    _evidence_locator_metrics,
    _judgement_metrics,
    _summarize_lockbox_residual_clusters,
    build_benchmark_split_bundle,
    build_full_available_task_bundle,
    build_lofo_task_bundles,
    summarize_benchmark_coverage,
)
from .schema import ElementIssue, EvidenceItem, ExpertReviewResult


def _record_row(**overrides):
    row = {
        "paper_slug": "paper-a",
        "paper_title": "Paper A",
        "record_source": "synthetic",
        "record_type": "sample_level_review",
        "review_record_id": "row-0",
        "case_id": None,
        "case_name": None,
        "split_name": None,
        "sheet_name": "STM Results",
        "diagram_type": "stm",
        "strategy_name": None,
        "llm_name": "GPT-4o",
        "review_target": "generated_behavior_model",
        "review_index": None,
        "component": None,
        "input_text": "R1: x",
        "ref_output_text": '{"states":[{"name":"A"}],"transitions":[]}',
        "ref_output_format": "json",
        "ref_output_artifact_path": None,
        "pred_output_text": '{"states":[{"name":"A"}],"transitions":[]}',
        "pred_output_format": "json",
        "pred_output_artifact_path": None,
        "human_review_score": 0.8,
        "human_review_score_unit": "semantic_f1",
        "human_review_summary": "Manual review.",
        "human_review_details_json": "{}",
        "human_review_source_record_json": "{}",
        "human_review_original_text": "looks okay",
        "human_review_original_text_json": "{}",
        "paper_method_verbatim_excerpt": "",
        "paper_method_verbatim_excerpt_json": "[]",
        "verbatim_extraction_verified": True,
        "review_rubric_text": "rubric",
        "public_artifact_limitations": "",
    }
    row.update(overrides)
    return row


def _protocol_row(**overrides):
    row = {
        "paper_slug": "paper-a",
        "paper_title": "Paper A",
        "paper_local_path": "/tmp/paper-a",
        "public_human_review_status": "sample_level_available",
        "human_review_artifact": "/tmp/artifact",
        "reviewer_pool": "experts",
        "reference_basis": "reference",
        "artifact_under_review": "artifact",
        "review_dimensions_json": "[]",
        "execution_steps_markdown": "manual inspection then verification",
        "matching_rules_markdown": "match by semantics",
        "public_gap_notes": "limited raw evidence",
        "paper_method_verbatim_excerpt": "",
        "paper_method_verbatim_excerpt_json": "[]",
        "paper_method_verbatim_verified": True,
    }
    row.update(overrides)
    return row


def _availability_row(**overrides):
    row = {
        "paper_slug": "paper-a",
        "paper_title": "Paper A",
        "public_human_review_status": "sample_level_available",
        "extracted_record_count": 10,
        "raw_artifact_path": "/tmp/raw",
        "input_available": True,
        "reference_output_available": True,
        "prediction_available": True,
        "notes": "",
    }
    row.update(overrides)
    return row


def _component_row(**overrides):
    row = _record_row(
        record_type="component_level_review",
        review_record_id="component-0",
        paper_slug="paper-c",
        case_id="dishwasher",
        case_name="Dishwasher",
        diagram_type=None,
        llm_name="GPT-4o",
        review_target="States",
        component="States",
        input_text="Problem description",
        ref_output_text=None,
        pred_output_text=None,
        human_review_score=0.8,
        human_review_score_unit="f1",
        human_review_details_json='{"tp": 6, "fn": 3, "fp": 0, "f1_score": 0.8}',
        human_review_source_record_json=(
            '{"source_kind": "xlsx_row", "sheet_name": "SinglePrompt", "strategy_name": "single_prompt", '
            '"system_name_normalized": "Dishwasher", "image_reference_raw": "dishwasher.png", "llm_name": "GPT-4o"}'
        ),
        human_review_original_text_json='[{"text": "Dishwasher\\tStates\\t6\\t3\\t0", "label": "States"}]',
        ref_output_artifact_path="/tmp/does-not-exist/dishwasher.png",
    )
    row.update(overrides)
    return row


def _component_row_without_public_counts(**overrides):
    row = _component_row(
        review_record_id="component-missing",
        human_review_score=float("nan"),
        human_review_details_json='{"tp": null, "fn": null, "fp": null, "f1_score": null}',
        human_review_original_text_json='[{"text": "Dishwasher\\tActions", "label": "Actions"}]',
        review_target="Actions",
        component="Actions",
    )
    row.update(overrides)
    return row


def test_judgement_metrics_track_kappa_and_flip_rate() -> None:
    rows = [
        {"human_judgement": "good", "agent_judgement": "good", "eval_bucket": "record", "rerun_judgement_flip": False},
        {"human_judgement": "acceptable", "agent_judgement": "acceptable", "eval_bucket": "summary", "rerun_judgement_flip": True},
    ]
    metrics = _judgement_metrics(rows)
    assert metrics["rows"] == 2
    assert metrics["macro_f1"] == 1.0
    assert metrics["weighted_kappa"] == 1.0
    assert metrics["judgement_flip_rate"] == 0.5


def test_agent_critical_issue_set_recovers_action_effect_from_raw_issue_text() -> None:
    result = ExpertReviewResult(
        prompt="prompt",
        overall_score=0.52,
        overall_judgement="weak",
        overall_reason_text="The generated transition keeps a brake action that is unsupported.",
        used_review_backend="deterministic",
        unsupported_model_elements=[
            ElementIssue(
                element_id="rel-1",
                element_kind="relation",
                element_text="Ready -> Stop : Brake Pressed",
                issue_type="extra",
                reason_text="The visible effect is unsupported by the requirements.",
            )
        ],
    )
    tags = _agent_critical_issue_set(result)
    assert "unsupported_extra_structure" in tags
    assert "wrong_action_or_effect" in tags


def test_evidence_locator_metrics_validate_summary_locators() -> None:
    result = ExpertReviewResult(
        prompt="prompt",
        overall_score=0.8,
        overall_judgement="good",
        overall_reason_text="reason",
        used_review_backend="deterministic",
        evidence_summary=[
            EvidenceItem(
                source="input",
                locator="input:requirement:r1",
                snippet="R1: start moves to Running",
                explanation="Requirement anchor.",
            ),
            EvidenceItem(
                source="prediction",
                locator=None,
                snippet="Running",
                explanation="Missing locator on purpose.",
            ),
        ],
    )
    metrics = _evidence_locator_metrics([{"result": result}])
    assert metrics["evidence_summary_items"] == 2
    assert metrics["evidence_locator_coverage"] == 0.5
    assert metrics["evidence_locator_validity"] == 0.5


def test_benchmark_coverage_summary_tracks_main_and_deferred_pools() -> None:
    records = pd.DataFrame(
        [
            _record_row(review_record_id="sample-1", diagram_type="stm", llm_name="GPT-4o"),
            _record_row(review_record_id="sample-2", diagram_type="act", llm_name="Claude"),
            _record_row(
                review_record_id="summary-1",
                record_type="summary_level_run_score",
                case_id="case-a",
                case_name="Case A",
                llm_name=None,
                input_text="public summary",
                ref_output_text=None,
                pred_output_text="summary artifact",
                review_target="SMD",
                human_review_score=82,
                human_review_score_unit="/100",
            ),
            _record_row(
                review_record_id="summary-2",
                record_type="case_aggregate_stat",
                case_id="case-b",
                case_name="Case B",
                llm_name=None,
                input_text="public summary",
                ref_output_text=None,
                pred_output_text="summary artifact",
                review_target="BD",
                human_review_score=76,
                human_review_score_unit="/100",
            ),
            _component_row(
                review_record_id="component-1",
                human_review_score=0.7,
                review_target="States",
                component="States",
            ),
            _component_row_without_public_counts(),
        ]
    )
    protocols = pd.DataFrame(
        [
            _protocol_row(paper_slug="paper-a"),
            _protocol_row(paper_slug="paper-b", public_human_review_status="summary_only_available"),
        ]
    )
    availability = pd.DataFrame(
        [
            _availability_row(paper_slug="paper-a"),
            _availability_row(paper_slug="paper-b", public_human_review_status="summary_only_available"),
            _availability_row(paper_slug="paper-c", public_human_review_status="sample_level_available"),
        ]
    )

    coverage = summarize_benchmark_coverage(records, protocols, availability)

    assert coverage["main_eval_rows"] == {"record": 2, "summary": 2, "component": 1, "protocol": 2}
    assert coverage["deferred_rows"]["component"] == 1
    assert coverage["family_counts"]["record"] == 2
    assert coverage["family_counts"]["summary"] == 2
    assert coverage["family_counts"]["protocol"] == 2
    assert coverage["component_alignment_schema"]["canonical_components"] == ["States"]
    assert coverage["component_alignment_schema"]["source_kind_counts"] == {"xlsx_row": 1}
    assert any("component_level_review" in item for item in coverage["coverage_gaps"])


def test_benchmark_split_bundle_keeps_family_keys_disjoint() -> None:
    sample_rows = []
    for diagram_type, llm_name in [("stm", "GPT-4o"), ("stm", "Claude"), ("act", "GPT-4o"), ("sd", "Claude")]:
        for idx in range(2):
            sample_rows.append(
                _record_row(
                    review_record_id=f"sample-{diagram_type}-{llm_name}-{idx}",
                    diagram_type=diagram_type,
                    llm_name=llm_name,
                )
            )
    summary_rows = []
    for case_id, review_target in [("case-a", "BD"), ("case-b", "BD"), ("case-c", "SMD"), ("case-d", "SMD")]:
        summary_rows.append(
            _record_row(
                review_record_id=f"summary-{case_id}-{review_target}",
                paper_slug="paper-b",
                record_type="summary_level_run_score",
                case_id=case_id,
                case_name=case_id.upper(),
                llm_name=None,
                input_text="summary",
                ref_output_text=None,
                pred_output_text="artifact",
                review_target=review_target,
                human_review_score=70,
                human_review_score_unit="/100",
            )
        )
    component_rows = []
    for case_id, llm_name in [("dishwasher", "GPT-4o"), ("printer", "Claude")]:
        component_rows.append(
            _component_row(
                review_record_id=f"component-{case_id}-{llm_name}",
                case_id=case_id,
                case_name=case_id.title(),
                llm_name=llm_name,
                review_target="States",
                component="States",
            )
        )
    records = pd.DataFrame(sample_rows + summary_rows + component_rows)
    protocols = pd.DataFrame(
        [
            _protocol_row(paper_slug="paper-a"),
            _protocol_row(paper_slug="paper-b"),
            _protocol_row(paper_slug="paper-c"),
            _protocol_row(paper_slug="paper-d"),
        ]
    )
    availability = pd.DataFrame(
        [
            _availability_row(paper_slug="paper-a"),
            _availability_row(paper_slug="paper-b"),
            _availability_row(paper_slug="paper-c"),
            _availability_row(paper_slug="paper-d"),
        ]
    )

    bundle = build_benchmark_split_bundle(records, protocols, availability, seed=13)
    manifest = bundle["manifest"]["regimes"]

    for regime_name in ("record", "summary", "component", "protocol"):
        seen: set[str] = set()
        for split_name in ("train", "dev", "validation", "lockbox"):
            family_keys = set(manifest[regime_name][split_name]["family_keys"])
            assert not (seen & family_keys)
            seen |= family_keys

    for split_name in ("train", "dev", "validation", "lockbox"):
        assert manifest["protocol"][split_name]["family_count"] == 1


def test_lofo_task_bundles_namespace_family_holdouts_by_regime() -> None:
    records = pd.DataFrame(
        [
            _record_row(review_record_id="sample-stm-gpt4o", diagram_type="stm", llm_name="GPT-4o"),
            _record_row(review_record_id="sample-act-claude", diagram_type="act", llm_name="Claude"),
            _record_row(
                review_record_id="summary-case-a-bd",
                paper_slug="paper-b",
                record_type="summary_level_run_score",
                case_id="case-a",
                case_name="Case A",
                llm_name=None,
                input_text="summary",
                ref_output_text=None,
                pred_output_text="artifact",
                review_target="BD",
                human_review_score=70,
                human_review_score_unit="/100",
            ),
            _component_row(
                review_record_id="component-dishwasher-gpt4o",
                case_id="dishwasher",
                case_name="Dishwasher",
                llm_name="GPT-4o",
            ),
        ]
    )
    protocols = pd.DataFrame([_protocol_row(paper_slug="paper-a"), _protocol_row(paper_slug="paper-b")])
    availability = pd.DataFrame([_availability_row(paper_slug="paper-a"), _availability_row(paper_slug="paper-b")])

    lofo = build_lofo_task_bundles(records, protocols, availability)

    assert any(key.startswith("record::") for key in lofo["task_bundles"])
    assert any(key.startswith("summary::") for key in lofo["task_bundles"])
    assert any(key.startswith("component::") for key in lofo["task_bundles"])
    assert any(key.startswith("protocol::") for key in lofo["task_bundles"])

    for namespaced_key, task_bundle in lofo["task_bundles"].items():
        manifest = lofo["manifest"]["families"][namespaced_key]
        non_empty_regimes = [regime for regime, tasks in task_bundle.items() if tasks]
        assert non_empty_regimes == [manifest["regime"]]
        assert manifest["rows"] == len(task_bundle[manifest["regime"]])


def test_full_task_bundle_builds_component_tasks_with_structured_public_counts() -> None:
    records = pd.DataFrame([_component_row()])
    protocols = pd.DataFrame([_protocol_row(paper_slug="paper-a")])
    availability = pd.DataFrame([_availability_row(paper_slug="paper-a")])

    bundle = build_full_available_task_bundle(records, protocols, availability)

    assert len(bundle["component"]) == 1
    task = bundle["component"][0]
    assert task.eval_bucket == "component"
    assert task.metadata["component_target"] == "States"
    assert task.metadata["component_public_tp"] == 6
    assert task.metadata["component_public_fp"] == 0
    assert task.metadata["component_public_fn"] == 3
    assert '"tp": 6' in task.pred_output
    assert "public_image_reference" not in task.pred_output
    assert "Public image reference" not in task.input_text


def test_full_task_bundle_defers_component_rows_without_structured_public_counts() -> None:
    records = pd.DataFrame([_component_row_without_public_counts()])
    protocols = pd.DataFrame([_protocol_row(paper_slug="paper-a")])
    availability = pd.DataFrame([_availability_row(paper_slug="paper-a")])

    bundle = build_full_available_task_bundle(records, protocols, availability)
    coverage = summarize_benchmark_coverage(records, protocols, availability)

    assert bundle["component"] == []
    assert coverage["main_eval_rows"]["component"] == 0
    assert coverage["deferred_rows"]["component"] == 1


def test_component_task_derives_human_score_from_public_counts_when_score_cell_missing() -> None:
    records = pd.DataFrame(
        [
            _component_row(
                review_record_id="component-derived-score",
                human_review_score=float("nan"),
                human_review_details_json='{"tp": 0, "fn": 0, "fp": 2, "f1_score": null}',
                review_target="Parallel Regions",
                component="Parallel Regions",
                human_review_original_text_json='[{"text": "Dishwasher\\tParallel Regions\\t0\\t0\\t2", "label": "Parallel Regions"}]',
            )
        ]
    )
    protocols = pd.DataFrame([_protocol_row(paper_slug="paper-a")])
    availability = pd.DataFrame([_availability_row(paper_slug="paper-a")])

    bundle = build_full_available_task_bundle(records, protocols, availability)

    assert len(bundle["component"]) == 1
    task = bundle["component"][0]
    assert task.metadata["component_evidence_status"] == "structured_counts_available"
    assert task.metadata["component_human_score_source"] == "derived_from_counts"
    assert task.human_score == 0.0


def test_phase14_lockbox_gate_limits_core_metric_degrade() -> None:
    split_reports = {
        "validation": {
            "HAI": 86.0,
            "record_metrics": {"RAS": 84.0},
            "summary_metrics": {"SAS": 82.0},
            "component_metrics": {"CRAS": 100.0},
            "protocol_metrics": {"PDS": 100.0},
        },
        "lockbox": {
            "HAI": 83.5,
            "record_metrics": {"RAS": 80.5},
            "summary_metrics": {"SAS": 79.0},
            "component_metrics": {"CRAS": 97.5},
            "protocol_metrics": {"PDS": 98.0},
        },
    }

    gate = _build_phase14_lockbox_gate(split_reports)

    assert gate["status"] == "passed"
    assert gate["core_metric_deltas"]["RAS"]["degrade"] == 3.5
    assert gate["core_metric_deltas"]["CRAS"]["passed"] is True


def test_phase14_lofo_gate_exposes_generalization_gap_payload() -> None:
    gate = _build_phase14_lofo_gate(
        {
            "record": {"avg_gap_vs_full": 2.0, "worst_holdout_gap_vs_full": 5.5, "worst_family": "record::a"},
            "summary": {"avg_gap_vs_full": 1.0, "worst_holdout_gap_vs_full": 3.0, "worst_family": "summary::b"},
        }
    )

    assert gate["status"] == "passed"
    assert gate["LOFO_generalization_gap"]["record"]["worst_family"] == "record::a"
    assert gate["max_avg_gap_vs_full"] == 2.0
    assert gate["max_worst_holdout_gap_vs_full"] == 5.5


def test_lockbox_residual_clusters_group_by_bucket_and_focus() -> None:
    report = {
        "normalized_rows": [
            {
                "task_id": "record-1",
                "eval_bucket": "record",
                "human_score": 0.2,
                "agent_score": 0.5,
                "issue_f1": 0.25,
                "error_buckets": ["calibration_error"],
                "metadata": {"diagram_type": "stm", "family_key": "paper-a::case-1"},
            },
            {
                "task_id": "record-2",
                "eval_bucket": "record",
                "human_score": 0.3,
                "agent_score": 0.55,
                "issue_f1": 0.35,
                "error_buckets": ["calibration_error"],
                "metadata": {"diagram_type": "stm", "family_key": "paper-a::case-2"},
            },
            {
                "task_id": "summary-1",
                "eval_bucket": "summary",
                "human_score": 0.7,
                "agent_score": 0.4,
                "issue_f1": 0.4,
                "error_buckets": ["contract_understanding_error"],
                "metadata": {"review_target": "BD", "family_key": "paper-b::case-3"},
            },
        ]
    }

    residuals = _summarize_lockbox_residual_clusters(report, top_k=4)

    assert residuals["status"] == "passed"
    assert residuals["residual_rows"] == 3
    assert residuals["bucket_counts"]["calibration_error"] == 2
    assert residuals["clusters"][0]["focus_key"] == "stm"
    assert residuals["clusters"][0]["rows"] == 2


def test_phase14_promotion_evaluation_requires_validation_lockbox_lofo_and_residuals() -> None:
    split_reports = {
        "validation": {
            "HAI": 86.0,
            "record_metrics": {"RAS": 84.0},
            "summary_metrics": {"SAS": 82.0},
            "component_metrics": {"CRAS": 100.0},
            "protocol_metrics": {"PDS": 100.0},
        },
        "lockbox": {
            "HAI": 83.5,
            "record_metrics": {"RAS": 80.5},
            "summary_metrics": {"SAS": 79.0},
            "component_metrics": {"CRAS": 97.5},
            "protocol_metrics": {"PDS": 98.0},
        },
    }
    evaluation = _build_phase14_promotion_evaluation(
        candidate_version="candidate-1",
        split_reports=split_reports,
        lofo_generalization={
            "record": {"avg_gap_vs_full": 2.0, "worst_holdout_gap_vs_full": 5.5, "worst_family": "record::a"}
        },
        lockbox_residuals={
            "status": "passed",
            "residual_rows": 3,
            "residual_row_rate": 0.2,
            "clusters": [{"eval_bucket": "record"}],
        },
    )

    assert evaluation["promotion_status"] == "promoted_to_phase14_default"
    assert evaluation["generalization_evidence_ready"] is True
    assert evaluation["stages"]["lockbox"]["status"] == "passed"


def test_evaluate_task_bundle_reuses_deterministic_review_cache(monkeypatch) -> None:
    call_counter = {"count": 0}

    class FakeAgent:
        def __init__(self, provider_order=None):
            self.provider_order = provider_order

        def review(self, request):
            call_counter["count"] += 1
            return ExpertReviewResult(
                prompt=request.prompt,
                overall_score=0.8,
                overall_judgement="good",
                overall_reason_text="reason",
                used_review_backend="deterministic",
            )

    monkeypatch.setattr(benchmark_module, "ExpertReviewAgent", FakeAgent)
    task = BenchmarkTask(
        task_id="cache-task",
        eval_bucket="record",
        regime_expected="record_level",
        prompt="Review this model.",
        input_text="R1: x",
        pred_output='{"states":[{"name":"A"}],"transitions":[]}',
        ref_output='{"states":[{"name":"A"}],"transitions":[]}',
        human_score=0.8,
        human_score_unit="semantic_f1",
        human_issue_set=set(),
        group_key="family-a",
        metadata={"family_key": "family-a", "diagram_type": "stm"},
    )
    review_cache = {}

    _evaluate_task_bundle(
        {"record": [task], "summary": [], "component": [], "protocol": []},
        llm_mode="off",
        rerun_count=0,
        report_label="first",
        review_cache=review_cache,
    )
    _evaluate_task_bundle(
        {"record": [task], "summary": [], "component": [], "protocol": []},
        llm_mode="off",
        rerun_count=0,
        report_label="second",
        review_cache=review_cache,
    )

    assert call_counter["count"] == 1


def test_phase15_report_comparison_exposes_runtime_and_alignment_deltas() -> None:
    baseline = {
        "HAI": 86.0,
        "record_metrics": {"RAS": 84.0, "spearman_rho": 0.70, "pairwise_order_accuracy": 0.78},
        "summary_metrics": {"SAS": 81.0, "spearman_rho": 0.60, "pairwise_order_accuracy": 0.72, "rerun_score_std": 0.01, "issue_jaccard_across_runs": 0.95},
        "component_metrics": {"CRAS": 100.0},
        "protocol_metrics": {"PDS": 100.0},
        "judgement_metrics": {"weighted_kappa": 0.60},
        "runtime_metrics": {
            "confidence_mean": 0.55,
            "latency_p50": 0.10,
            "latency_p95": 0.20,
            "token_cost_per_record": 0.0,
            "llm_effective_record_rate": 0.0,
            "llm_fallback_only_record_rate": 0.0,
        },
    }
    candidate = {
        "HAI": 87.5,
        "record_metrics": {"RAS": 85.0, "spearman_rho": 0.73, "pairwise_order_accuracy": 0.80},
        "summary_metrics": {"SAS": 82.0, "spearman_rho": 0.63, "pairwise_order_accuracy": 0.75, "rerun_score_std": 0.02, "issue_jaccard_across_runs": 0.96},
        "component_metrics": {"CRAS": 100.0},
        "protocol_metrics": {"PDS": 100.0},
        "judgement_metrics": {"weighted_kappa": 0.64},
        "runtime_metrics": {
            "confidence_mean": 0.60,
            "latency_p50": 0.45,
            "latency_p95": 0.90,
            "token_cost_per_record": 3200.0,
            "llm_effective_record_rate": 0.92,
            "llm_fallback_only_record_rate": 0.08,
        },
    }
    comparison = _build_phase15_report_comparison(baseline, candidate)
    assert comparison["delta"]["HAI"] == 1.5
    assert comparison["delta"]["token_cost_per_record"] == 3200.0
    assert comparison["delta"]["llm_effective_record_rate"] == 0.92
    assert comparison["default_path_recommendation"] == "llm_optional_gain_visible"
