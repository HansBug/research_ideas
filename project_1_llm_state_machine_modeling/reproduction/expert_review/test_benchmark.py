from __future__ import annotations

import pandas as pd

from .benchmark import (
    build_benchmark_split_bundle,
    build_lofo_task_bundles,
    summarize_benchmark_coverage,
)


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
            _record_row(
                review_record_id="component-1",
                paper_slug="paper-c",
                record_type="component_level_review",
                case_id="dishwasher",
                case_name="Dishwasher",
                diagram_type=None,
                llm_name="GPT-4o",
                review_target="States",
                input_text=None,
                ref_output_text=None,
                pred_output_text=None,
                human_review_score=0.7,
                human_review_score_unit="f1",
            ),
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

    assert coverage["main_eval_rows"] == {"record": 2, "summary": 2, "protocol": 2}
    assert coverage["deferred_rows"]["component"] == 1
    assert coverage["family_counts"]["record"] == 2
    assert coverage["family_counts"]["summary"] == 2
    assert coverage["family_counts"]["protocol"] == 2
    assert coverage["component_alignment_schema"]["canonical_components"] == ["States"]
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
    records = pd.DataFrame(sample_rows + summary_rows)
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

    for regime_name in ("record", "summary", "protocol"):
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
        ]
    )
    protocols = pd.DataFrame([_protocol_row(paper_slug="paper-a"), _protocol_row(paper_slug="paper-b")])
    availability = pd.DataFrame([_availability_row(paper_slug="paper-a"), _availability_row(paper_slug="paper-b")])

    lofo = build_lofo_task_bundles(records, protocols, availability)

    assert any(key.startswith("record::") for key in lofo["task_bundles"])
    assert any(key.startswith("summary::") for key in lofo["task_bundles"])
    assert any(key.startswith("protocol::") for key in lofo["task_bundles"])

    for namespaced_key, task_bundle in lofo["task_bundles"].items():
        manifest = lofo["manifest"]["families"][namespaced_key]
        non_empty_regimes = [regime for regime, tasks in task_bundle.items() if tasks]
        assert non_empty_regimes == [manifest["regime"]]
        assert manifest["rows"] == len(task_bundle[manifest["regime"]])
