from __future__ import annotations

import json

from .batch import BatchReviewItem, export_batch_run, load_batch_items, run_batch_review


def _good_item() -> BatchReviewItem:
    return BatchReviewItem(
        item_id="good-1",
        prompt="Review the predicted printer state machine and focus on requirement coverage and unsupported extras.",
        input_text=(
            "R1: login moves the system from Idle to Ready.\n"
            "R2: start moves the system from Ready to Printing.\n"
            "R3: paper jam suspends printing and allows resume."
        ),
        pred_output="""
        {
          "states": [{"name": "Idle"}, {"name": "Ready"}, {"name": "Printing"}, {"name": "Suspended"}],
          "transitions": [
            {"source": "Idle", "target": "Ready", "event": "login", "guard": "", "action": ""},
            {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
            {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
            {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""}
          ]
        }
        """,
        ref_output="""
        {
          "states": [{"name": "Idle"}, {"name": "Ready"}, {"name": "Printing"}, {"name": "Suspended"}],
          "transitions": [
            {"source": "Idle", "target": "Ready", "event": "login", "guard": "", "action": ""},
            {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
            {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
            {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""}
          ]
        }
        """,
        metadata={"bucket": "good"},
    )


def _bad_item() -> BatchReviewItem:
    return BatchReviewItem(
        item_id="bad-1",
        prompt="Review the predicted printer state machine and focus on requirement coverage and unsupported extras.",
        input_text=(
            "R1: login moves the system from Idle to Ready.\n"
            "R2: start moves the system from Ready to Printing.\n"
            "R3: paper jam suspends printing and allows resume."
        ),
        pred_output="""
        {
          "states": [{"name": "Idle"}, {"name": "Maintenance"}],
          "transitions": [
            {"source": "Idle", "target": "Maintenance", "event": "selfCheck", "guard": "", "action": ""}
          ]
        }
        """,
        ref_output=_good_item().ref_output,
        metadata={"bucket": "bad"},
    )


def test_run_batch_review_produces_triage_and_observability() -> None:
    run = run_batch_review([_good_item(), _bad_item()], llm_mode="off", rerun_count=1)
    assert run.summary["total_items"] == 2
    assert run.summary["success_count"] == 2
    assert "latency_p95" in run.summary
    assert "triage_counts" in run.summary
    labels = {row.item_id: row.triage_label for row in run.rows}
    assert labels["good-1"] in {"direct_pass", "manual_review"}
    assert labels["bad-1"] in {"manual_review", "high_risk_reject"}
    assert run.summary["rerun_score_std"] >= 0.0


def test_batch_load_and_export_round_trip(tmp_path) -> None:
    input_path = tmp_path / "batch.json"
    input_path.write_text(
        json.dumps(
            {
                "items": [
                    {
                        "item_id": "good-1",
                        "prompt": _good_item().prompt,
                        "input_text": _good_item().input_text,
                        "pred_output": _good_item().pred_output,
                        "ref_output": _good_item().ref_output,
                        "metadata": {"bucket": "good"},
                    }
                ]
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    items = load_batch_items(input_path)
    assert len(items) == 1
    run = run_batch_review(items, llm_mode="off", rerun_count=1)
    json_path = tmp_path / "run.json"
    jsonl_path = tmp_path / "rows.jsonl"
    csv_path = tmp_path / "rows.csv"
    export_batch_run(run, output_json=json_path, output_jsonl=jsonl_path, output_csv=csv_path)
    assert json.loads(json_path.read_text(encoding="utf-8"))["summary"]["total_items"] == 1
    assert "good-1" in jsonl_path.read_text(encoding="utf-8")
    assert "item_id" in csv_path.read_text(encoding="utf-8")
