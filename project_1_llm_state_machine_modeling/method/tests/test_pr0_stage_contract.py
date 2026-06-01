from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from method.schema import (
    AgentLoopRunRecord,
    BudgetState,
    FeedbackBundle,
    ParseFeedback,
    SemanticFeedback,
    StageResultMeta,
)
from method.stages.ids import ALL_STAGE_SPECS, STAGE_SPECS_BY_ID, FeedbackSource, StageId, StageKind


REPO = Path(__file__).resolve().parents[3]
METHOD_ROOT = REPO / "project_1_llm_state_machine_modeling" / "method"


def test_stage_ids_are_canonical_and_cover_pr0_loop_contract() -> None:
    stage_ids = [spec.stage_id for spec in ALL_STAGE_SPECS]

    assert len(stage_ids) == len(set(stage_ids))
    assert stage_ids == [
        "SC-0",
        "SL-1",
        "SD-2",
        "SD-3",
        "SD-4",
        "SL-5",
        "SD-5A",
        "SD-6",
        "SL-7",
        "SD-8",
        "SL-9",
        "SD-10",
        "SL-10B",
        "SC-11",
        "SC-12",
    ]
    assert STAGE_SPECS_BY_ID["SD-4"].kind == StageKind.DETERMINISTIC
    assert STAGE_SPECS_BY_ID["SL-9"].kind == StageKind.LLM
    assert STAGE_SPECS_BY_ID["SC-12"].kind == StageKind.CONTROL
    assert StageId.SD_4_DESIGN.value == "SD-4"
    assert FeedbackSource.DESIGN.value == "design"


def test_feedback_bundle_all_ok_respects_enabled_but_missing_contract() -> None:
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.PARSE.value, FeedbackSource.SEMANTIC.value],
        parse=ParseFeedback(ok=True),
    )

    assert not bundle.all_ok
    assert bundle.missing_enabled_sources() == [FeedbackSource.SEMANTIC.value]

    bundle.semantic = SemanticFeedback(ok=True)
    assert bundle.all_ok
    assert bundle.missing_enabled_sources() == []


def test_feedback_bundle_legacy_non_none_mode_stays_backward_compatible() -> None:
    bundle = FeedbackBundle(parse=ParseFeedback(ok=True))

    assert bundle.all_ok
    assert bundle.has_any_signal()

    bundle.semantic = SemanticFeedback(ok=False)
    assert not bundle.all_ok


def test_agent_loop_run_record_is_single_file_json_schema_fixture() -> None:
    meta = StageResultMeta(
        stage_id=StageId.SD_2_PARSE.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status="ok",
        ok=True,
        input_hash="sha256:input",
        output_hash="sha256:output",
        elapsed_ms=12,
    )
    record = AgentLoopRunRecord(
        schema_version="pr0.stage-contract.v1",
        run_id="run-test-0001",
        created_at="2026-06-01T00:00:00Z",
        status="success",
        input_bundle={"nl": "When Start occurs, move from Idle to Active."},
        run_config={"enabled_stages": [StageId.SD_2_PARSE.value]},
        environment={"git_commit": "test", "pyfcstm_version": "0.4.0"},
        stage_graph={"planned": [StageId.SD_2_PARSE.value], "executed": [StageId.SD_2_PARSE.value]},
        stage_records=[asdict(meta)],
        iteration_records=[{"iteration": 0, "stage_ids": [StageId.SD_2_PARSE.value]}],
        deterministic_feedback={"parse": {"ok": True}},
        final_artifacts={"final_dsl_hash": "sha256:final", "verdict": "success"},
        replay_index={"stage_by_id": {StageId.SD_2_PARSE.value: 0}},
    )

    payload = asdict(record)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    decoded = json.loads(encoded)

    assert decoded["run_id"] == "run-test-0001"
    assert decoded["stage_records"][0]["stage_id"] == "SD-2"
    assert decoded["redaction_report"] == []


def test_budget_state_is_json_serializable_and_instance_keyed() -> None:
    state = BudgetState(
        instance_key="W_DEADLOCK_LEAF:state=Root.Idle",
        diagnostic_code="W_DEADLOCK_LEAF",
        repair_count=1,
        budget_remaining=1,
        budget_exhausted=False,
        last_status="budgeted_repair",
        last_stage=StageId.SD_4_DESIGN.value,
    )

    payload = asdict(state)
    assert payload["instance_key"].startswith("W_DEADLOCK_LEAF")
    assert json.loads(json.dumps(payload))["budget_remaining"] == 1


def test_stage_docs_skill_links_and_minimal_fixtures_exist() -> None:
    docs_root = METHOD_ROOT / "stages" / "docs"
    fixtures_root = METHOD_ROOT / "stages" / "fixtures"
    skill_root = METHOD_ROOT / "agent_loop_skill"

    for spec in ALL_STAGE_SPECS:
        doc = docs_root / spec.doc_filename
        assert doc.exists(), f"missing stage doc: {doc}"
        text = doc.read_text(encoding="utf-8")
        for marker in ["## 目标", "## 输入", "## 输出", "## 函数名或 prompt generator 名", "## 最小示例", "## 失败语义"]:
            assert marker in text, f"{marker} missing in {doc}"

        fixture = fixtures_root / f"{spec.stage_id}.json"
        assert fixture.exists(), f"missing fixture: {fixture}"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["stage_id"] == spec.stage_id
        assert "input" in data and "output" in data

        skill_link = skill_root / "stages" / f"{spec.stage_id}.md"
        assert skill_link.exists(), f"missing skill stage link: {skill_link}"

    for link_name in ["SKILL.md", "CLAUDE.md"]:
        link = skill_root / link_name
        assert link.is_symlink(), f"{link} must be a symlink"
        assert link.resolve() == (skill_root / "AGENT_LOOP_SKILL.md").resolve()

    assert (skill_root / "tools.md").exists()
    assert (skill_root / "prompts.md").exists()
