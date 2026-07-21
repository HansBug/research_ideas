from __future__ import annotations

import json
from pathlib import Path

from paper_stm_repair_loop.agents.discover import run_discover
from paper_stm_repair_loop.controller import DiscoverController
from paper_stm_repair_loop.inputs import prepare_run_dir
from paper_stm_repair_loop.records import RecordStore
from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm

from v2_helpers import expressions_from_plan, make_case, make_manifest, make_plan


def _write_replay(tmp_path: Path) -> tuple[Path, object]:
    case = make_case()
    planning_root = tmp_path / "planning"
    controller = DiscoverController(
        case,
        make_manifest(),
        check_fcstm(case.fcstm, "inputs/STM_0.fcstm"),
        RecordStore(planning_root),
    )
    plan = make_plan(controller)
    replay = tmp_path / "replay.json"
    replay.write_text(
        json.dumps(
            {
                "coverage_plan": plan,
                "plan_reason": "注册 replay 的完整覆盖计划。",
                "eval_assertions": [
                    {
                        "assert": expression,
                        "reason": "逐条执行 replay 的完整正向断言。",
                    }
                    for expression in expressions_from_plan(plan)
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return replay, case


def test_v2_replay_runs_controller_tools_records_and_renderer_end_to_end(tmp_path):
    replay, case = _write_replay(tmp_path)
    run_dir = tmp_path / "run"
    prepare_run_dir(
        run_dir,
        case,
        profile="test",
        content_language="zh-CN",
        renderer="quiet",
        formal_profile=True,
        replay_file=replay,
        agent_limits={},
    )
    completed = run_discover(run_dir, object())
    assert completed.schema_version == "paper1.discover_completed.v2"
    assert completed.outcome.run_outcome == "reviewer_accepted_zero_issue"
    assert completed.test_replay is True
    assert completed.agent_real_llm is False

    records = RecordStore(run_dir).all()
    record_types = [record["record_type"] for record in records]
    for required in (
        "inputs_frozen",
        "input_segments_created",
        "source_inventory_created",
        "coverage_plan_registered",
        "eval_assert_call_prepared",
        "eval_assert_completed",
        "root_projection_completed",
        "discover_completed",
        "discover_report_render_completed",
    ):
        assert required in record_types
    assert "evaluate_checks_attempts_completed" not in record_types
    RecordStore(run_dir).validate_chain()
    report = (run_dir / "loops/discover.md").read_text(encoding="utf-8")
    assert "ROOT-001" in report
    assert "ASSERT-001" in report
    assert "transition_exists" in report


def test_run_discover_rejects_non_fresh_record_prefix(tmp_path):
    replay, case = _write_replay(tmp_path)
    run_dir = tmp_path / "run"
    prepare_run_dir(
        run_dir,
        case,
        profile="test",
        content_language="zh-CN",
        renderer="quiet",
        formal_profile=True,
        replay_file=replay,
        agent_limits={},
    )
    RecordStore(run_dir).append("unexpected", {})
    try:
        run_discover(run_dir, object())
    except ValueError as exc:
        assert "fresh" in str(exc)
    else:
        raise AssertionError("non-fresh run must fail closed")
