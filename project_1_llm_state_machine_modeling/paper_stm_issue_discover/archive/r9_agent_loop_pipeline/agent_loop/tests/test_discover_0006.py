from __future__ import annotations

import json
from pathlib import Path

from paper_stm_repair_loop.controller import DiscoverController
from paper_stm_repair_loop.inputs import PreparedCase
from paper_stm_repair_loop.records import RecordStore
from paper_stm_repair_loop.schemas.coverage import CoveragePlan
from paper_stm_repair_loop.schemas.discovery import DiscoverOutcome
from paper_stm_repair_loop.schemas.coverage_review import CoverageReviewVerdict
from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm
from paper_stm_repair_loop.tools.review_discovery_coverage import CoverageReviewGate


FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "discover_integrated"
    / "0006_uav"
)


def _case() -> PreparedCase:
    model = (FIXTURE / "STM_0.fcstm").read_text(encoding="utf-8")
    return PreparedCase(
        case_id="0006-uav",
        pair_id=None,
        nl=(FIXTURE / "nl.txt").read_text(encoding="utf-8"),
        raw_source=model,
        raw_source_format="fcstm-identity",
        fcstm=model,
        source_trace={
            "schema_version": "source_trace_base.v1",
            "trace_scope": "development_integrated_smoke",
            "relation_policy": "exact_identity",
            "entries": [],
        },
        metadata={"nl_language": "en-US", "academic_eligible": False},
        input_mode="custom",
    )


def _assertion(
    chain: str,
    root: str,
    unit: str,
    expression: str,
    families: str | list[str],
    basis: list[str],
):
    return {
        "assertion_chain_id": chain,
        "root_node_id": root,
        "coverage_unit_id": unit,
        "required": True,
        "assert": expression,
        "basis_ids": basis,
        "obligation_signature": unit.lower(),
        "required_function_families": [families]
        if isinstance(families, str)
        else families,
        "evidence_scope": {
            "semantic_profile": "single_active_leaf_fcstm_v1",
            "max_steps": 8,
            "max_time": None,
            "abstraction": "discrete_event",
            "claim_strength": "development_integrated_smoke",
        },
        "rationale": "正向命题；True 表示当前义务满足。",
        "record_language": "zh-CN",
    }


def _plan(controller: DiscoverController) -> CoveragePlan:
    frozen = controller.prepare()
    segments = [item.segment_id for item in frozen.input_segments]
    requirements = {
        item.requirement_id: item for item in frozen.coverage_requirements
    }
    req_by_clause = {
        clause_id: [
            item.requirement_id
            for item in frozen.coverage_requirements
            if item.clause_id == clause_id
        ]
        for clause_id in {item.clause_id for item in frozen.coverage_requirements}
    }
    facts = list(frozen.source_facts)
    units = [
        (
            "CU-001",
            [segments[1]],
            [
                *req_by_clause["CLAUSE-002-02"],
            ],
            ["structure", "cardinality"],
            "三个可区分搜索区域",
        ),
        (
            "CU-002",
            [segments[2]],
            [
                *req_by_clause["CLAUSE-003-01"],
            ],
            ["transition", "condition"],
            "拦截后进入 FormationAdjustment",
        ),
        (
            "CU-003",
            [segments[3]],
            [
                *req_by_clause["CLAUSE-004-01"],
            ],
            ["transition", "condition"],
            "收到任务后进入 Attack",
        ),
        (
            "CU-004",
            [segments[4]],
            [
                *req_by_clause["CLAUSE-005-01"],
            ],
            ["effect", "ordering"],
            "Attack Complete 后 UAV 数量减少",
        ),
        ("CU-005", [], [], [], "完整 source inventory 与 exact identity 归因可执行审计"),
        (
            "CU-006",
            [segments[1]],
            [
                *req_by_clause["CLAUSE-002-01"],
            ],
            ["ordering", "continuity", "completion"],
            "任务完成前以 Searching 为默认搜索状态并在临时行为后返回",
        ),
    ]
    source_fact_ids = [item.fact_id for item in facts]
    coverage_units = [
        {
            "coverage_unit_id": unit_id,
            "unit_kind": "source_behavior" if unit_id == "CU-005" else "behavior_obligation",
            "segment_ids": segment_ids,
            "source_fact_ids": source_fact_ids,
            "requirement_ids": requirement_ids,
            "dimensions": sorted(
                {requirements[requirement_id].dimension for requirement_id in requirement_ids}
            ),
            "statement": statement,
            "rationale": "一个可独立失败和修复的行为义务。",
            "record_language": "zh-CN",
            "in_scope": True,
        }
        for unit_id, segment_ids, requirement_ids, dimensions, statement in units
    ]
    root_refs_by_unit = {
        "CU-001": ["state:Root.Searching"],
        "CU-002": [
            "event:Root.Interception_Detected",
            "state:Root.FormationAdjustment",
        ],
        "CU-003": ["event:Root.Task_Assignment_Received", "state:Root.Attack"],
        "CU-004": ["event:Root.Attack_Complete", "state:Root.Attack"],
        "CU-005": ["state:Root.Searching"],
        "CU-006": ["state:Root.Searching"],
    }
    roots = [
        {
            "node_id": f"ROOT-{index:03d}",
            "previous_node_id": None,
            "coverage_unit_id": unit_id,
            "statement": statement,
            "model_element_refs": root_refs_by_unit[unit_id],
            "source_element_refs": [
                f"source:requirement:{segment_ids[0]}"
                if segment_ids
                else "transition:4"
            ],
            "rationale": "该 Root 对应一个正向义务。",
            "record_language": "zh-CN",
        }
        for index, (unit_id, segment_ids, _requirement_ids, _dimensions, statement) in enumerate(units, start=1)
    ]
    assertions = [
        _assertion(
            "ASSERT-001",
            "ROOT-001",
            "CU-001",
            "len(states(parent='Root.Searching', recursive=False)) == 3",
            "structure",
            [
                segments[1],
                *req_by_clause["CLAUSE-002-02"],
            ],
        ),
        _assertion(
            "ASSERT-002",
            "ROOT-002",
            "CU-002",
            "simulate(cycles=[[], ['Root.Interception_Detected'], []]).final.is_active('Root.FormationAdjustment')",
            "simulation",
            [
                segments[2],
                *req_by_clause["CLAUSE-003-01"],
            ],
        ),
        _assertion(
            "ASSERT-003",
            "ROOT-003",
            "CU-003",
            "simulate(cycles=[[], ['Root.Task_Assignment_Received']]).final.is_active('Root.Attack')",
            "simulation",
            [
                segments[3],
                *req_by_clause["CLAUSE-004-01"],
            ],
        ),
        _assertion(
            "ASSERT-004",
            "ROOT-004",
            "CU-004",
            "any(delta < 0 for _, delta in effect_deltas(source='Root.Attack', event='Root.Attack_Complete', target='Root.Searching'))",
            "effect",
            [
                segments[4],
                *req_by_clause["CLAUSE-005-01"],
            ],
        ),
        _assertion(
            "ASSERT-005",
            "ROOT-005",
            "CU-005",
            "all([len(states(name='Root')) == 1, len(states(name='Root.Searching')) == 1, len(states(name='Root.Intercepted')) == 1, len(states(name='Root.FormationAdjustment')) == 1, len(states(name='Root.Attack')) == 1, len(states(parent='Root', recursive=False, name='Root.Searching')) == 1, len(states(parent='Root', recursive=False, name='Root.Intercepted')) == 1, len(states(parent='Root', recursive=False, name='Root.FormationAdjustment')) == 1, len(states(parent='Root', recursive=False, name='Root.Attack')) == 1, len(events(name='Root.Adjustment_Complete')) == 1, len(events(name='Root.Attack_Complete')) == 1, len(events(name='Root.Interception_Detected')) == 1, len(events(name='Root.Task_Assignment_Received')) == 1, initial_child('Root') == 'Root.Searching', transition_exists(source='Root.Searching', event='Root.Interception_Detected', target='Root.Intercepted'), any(t.event is None for t in transitions(source='Root.Intercepted', target='Root.FormationAdjustment')), transition_exists(source='Root.FormationAdjustment', event='Root.Adjustment_Complete', target='Root.Searching'), transition_exists(source='Root.Searching', event='Root.Task_Assignment_Received', target='Root.Attack'), transition_exists(source='Root.Attack', event='Root.Attack_Complete', target='Root.Searching'), bool(bound_model_refs('CU-005'))])",
            ["structure", "relation", "mapping"],
            source_fact_ids,
        ),
        _assertion(
            "ASSERT-006",
            "ROOT-006",
            "CU-006",
            "all([initial_child('Root') == 'Root.Searching', simulate(cycles=[[], ['Root.Interception_Detected'], [], ['Root.Adjustment_Complete']]).final.is_active('Root.Searching'), simulate(cycles=[[], ['Root.Task_Assignment_Received'], ['Root.Attack_Complete']]).final.is_active('Root.Searching')])",
            ["structure", "simulation"],
            [
                segments[1],
                *req_by_clause["CLAUSE-002-01"],
            ],
        ),
    ]
    return CoveragePlan.model_validate(
        {
            "segment_dispositions": [
                {
                    "segment_id": segments[0],
                    "disposition": "context_only",
                    "rationale": "该句只说明模型主题。",
                    "record_language": "zh-CN",
                }
            ],
            "fact_dispositions": [],
            "coverage_units": coverage_units,
            "proposition_roots": roots,
            "logical_assertions": assertions,
            "rationale": "六个原子义务、全部 coverage requirements 与行为事实均已登记。",
        }
    )


def _controller(tmp_path) -> DiscoverController:
    case = _case()
    store = RecordStore(tmp_path)
    checked = check_fcstm(case.fcstm, "inputs/STM_0.fcstm")
    check_record = store.append("check_fcstm_completed", checked)
    checked = {
        **checked,
        "record_id": check_record["record_id"],
        "record_sha256": check_record["record_sha256"],
    }
    store.append(
        "capability_manifest",
        {"schema_hashes": {"test_fixture": "test-schema-v1"}},
    )
    return DiscoverController(
        case,
        {
            "run_id": "0006",
            "profile": "test",
            "content_language": "zh-CN",
            "formal_profile": True,
            "agent_limits": {},
            "input_sha256": {},
        },
        checked,
        store,
    )


def test_0006_cardinality_parent_must_exactly_match_root_ref(tmp_path):
    controller = _controller(tmp_path)
    plan = _plan(controller).model_dump(mode="json", by_alias=True)
    plan["logical_assertions"][0]["assert"] = (
        "len(states(parent='Root.Searching.Unrelated', recursive=False)) == 3"
    )

    rejected = controller.require_registry().register_plan(
        plan, reason="拒绝仅共享前缀的错误 cardinality parent。"
    )

    assert any(
        error.startswith(
            "assertion_cardinality_parent_not_grounded_by_root:"
            "ASSERT-001:Root.Searching.Unrelated:ROOT-001"
        )
        for error in rejected["errors"]
    )


def test_0006_strict_coverage_assertions_find_two_issues(tmp_path):
    controller = _controller(tmp_path)
    plan = _plan(controller)
    registered = controller.require_registry().register_plan(
        plan.model_dump(mode="json", by_alias=True), reason="注册 0006 六项严格覆盖义务。"
    )
    assert registered["accepted"] is True
    results = [
        controller.require_registry().eval_assert(
            assertion.assert_, reason=f"执行 {assertion.assertion_chain_id}。"
        )
        for assertion in plan.logical_assertions
    ]
    assert [item["match_status"] for item in results] == [
        "contradicts",
        "matches",
        "matches",
        "contradicts",
        "matches",
        "matches",
    ]
    registry = controller.require_registry()

    def passing_reviewer(kind, payload, _attempt):
        contract = payload["review_contract"]
        return CoverageReviewVerdict(
            review_kind=kind,
            passed=True,
            reviewed_segment_ids=contract["required_segment_ids"],
            reviewed_requirement_ids=contract["required_requirement_ids"],
            reviewed_source_fact_ids=contract["required_source_fact_ids"],
            reviewed_root_ids=contract["required_root_ids"],
            findings=[],
            coverage_analysis=(
                "已逐条审计全部 NL 原子义务、行为事实、正向断言、真实执行结果与 issue 投影，"
                "未发现遗漏、弱化、误报或漏报风险。"
            ),
            rationale="两个独立审查角色在完整当前台账上均满足严格通过条件。",
        )

    review_gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=passing_reviewer,
    )
    registry.semantic_review_gate = review_gate
    assert review_gate.review(reason="审查 0006 主要行为覆盖台账。")["passed"] is True
    outcome = DiscoverOutcome.model_validate(controller.projection())
    gold = json.loads((FIXTURE / "evaluator_gold.json").read_text(encoding="utf-8"))
    assert outcome.run_outcome == "issues_found"
    assert len(outcome.issue_root_projection) == gold["expected_issue_count"]
    assert [item.node_id for item in outcome.issue_root_projection] == [
        "ROOT-001",
        "ROOT-004",
    ]
    assert [item.node_id for item in outcome.regression_guard_projection] == [
        "ROOT-002",
        "ROOT-003",
        "ROOT-005",
        "ROOT-006",
    ]
    assert len(outcome.regression_guard_projection) == len(
        gold["expected_ok_obligations"]
    )
    assert outcome.coverage_requirement_coverage["covered"] == outcome.coverage_requirement_coverage["total"]
    selected_facts = outcome.selected_source_fact_evidence_coverage
    assert selected_facts["covered"] == selected_facts["total"]
    assert outcome.major_behavior_coverage_review["passed"] is True
    assert {
        dimension
        for unit in plan.coverage_units
        for dimension in unit.dimensions
    } == set(gold["expected_coverage_dimensions"])
    assert not outcome.incomplete_root_projection
