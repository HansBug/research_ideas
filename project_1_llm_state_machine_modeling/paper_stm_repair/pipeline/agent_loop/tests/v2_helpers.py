from __future__ import annotations

from pathlib import Path
from typing import Any

from paper_stm_repair_loop.controller import DiscoverController
from paper_stm_repair_loop.inputs import PreparedCase
from paper_stm_repair_loop.records import RecordStore
from paper_stm_repair_loop.schemas.coverage_review import CoverageReviewVerdict
from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm
from paper_stm_repair_loop.tools.review_discovery_coverage import CoverageReviewGate


MODEL = """state Root {
    event Power_Off;
    state Off;
    state Active;
    [*] -> Active;
    Active -> Off : Power_Off;
}
"""

NL = "While Active, Power_Off must move the controller to Off."


def make_case() -> PreparedCase:
    return PreparedCase(
        case_id="v2-smoke",
        pair_id=None,
        nl=NL,
        raw_source=MODEL,
        raw_source_format="fcstm-identity",
        fcstm=MODEL,
        source_trace={
            "schema_version": "source_trace_base.v1",
            "trace_scope": "test",
            "relation_policy": "exact_identity",
            "entries": [],
        },
        metadata={"nl_language": "en-US"},
        input_mode="custom",
    )


def make_manifest() -> dict[str, Any]:
    return {
        "run_id": "v2-smoke",
        "profile": "test",
        "content_language": "zh-CN",
        "renderer": "quiet",
        "formal_profile": True,
        "agent_limits": {},
        "input_sha256": {},
    }


def make_controller(root: Path) -> DiscoverController:
    case = make_case()
    store = RecordStore(root)
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
        make_manifest(),
        checked,
        store,
    )


def make_plan(controller: DiscoverController) -> dict[str, Any]:
    frozen = controller.prepare()
    source_fact_ids = [fact.fact_id for fact in frozen.source_facts]
    transition_ref = next(
        ref
        for fact in frozen.source_facts
        if fact.fact_kind == "transition"
        for ref in fact.qualified_refs
    )
    segment_ids = [segment.segment_id for segment in frozen.input_segments]
    requirement_ids = [
        requirement.requirement_id for requirement in frozen.coverage_requirements
    ]
    dimensions = sorted(
        {requirement.dimension for requirement in frozen.coverage_requirements}
    )
    relation_expression = (
        "transition_exists(source='Root.Active', event='Root.Power_Off', "
        "target='Root.Off')"
    )
    source_audit_expression = (
        "all(["
        "len(states(name='Root')) == 1, "
        "len(states(name='Root.Active')) == 1, "
        "len(states(name='Root.Off')) == 1, "
        "len(states(parent='Root', recursive=False, name='Root.Active')) == 1, "
        "len(states(parent='Root', recursive=False, name='Root.Off')) == 1, "
        "len(events(name='Root.Power_Off')) == 1, "
        "initial_child('Root') == 'Root.Active', "
        "transition_exists(source='Root.Active', event='Root.Power_Off', target='Root.Off')"
        "])"
    )
    return {
        "segment_dispositions": [],
        "fact_dispositions": [],
        "coverage_units": [
            {
                "coverage_unit_id": "CU-REQ-001",
                "unit_kind": "behavior_obligation",
                "segment_ids": segment_ids,
                "source_fact_ids": source_fact_ids,
                "requirement_ids": requirement_ids,
                "dimensions": dimensions,
                "statement": "Power_Off 后从 Active 进入 Off。",
                "rationale": "该要求可独立验证和修复。",
                "record_language": "zh-CN",
                "in_scope": True,
            }
        ],
        "proposition_roots": [
            {
                "node_id": "ROOT-001",
                "previous_node_id": None,
                "coverage_unit_id": "CU-REQ-001",
                "statement": "模型处理 Active 状态下的 Power_Off。",
                "model_element_refs": [transition_ref],
                "source_element_refs": [f"source:requirement:{segment_ids[0]}"],
                "rationale": "对目标迁移建立一个正向命题。",
                "record_language": "zh-CN",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-001",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-REQ-001",
                "required": True,
                "assert": relation_expression,
                "basis_ids": [*segment_ids, *requirement_ids],
                "obligation_signature": "active-power-off-target-off",
                "required_function_families": ["relation"],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "deterministic_transition_fact",
                },
                "rationale": "True 才表示目标迁移存在。",
                "record_language": "zh-CN",
            },
            {
                "assertion_chain_id": "ASSERT-002",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-REQ-001",
                "required": True,
                "assert": source_audit_expression,
                "basis_ids": source_fact_ids,
                "obligation_signature": "complete-structure-audit",
                "required_function_families": ["structure", "relation"],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "complete_structure_inventory",
                },
                "rationale": "结构清单进入同一覆盖审计。",
                "record_language": "zh-CN",
            },
            {
                "assertion_chain_id": "ASSERT-003",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-REQ-001",
                "required": True,
                "assert": "not effects(source='Root.Active', event='Root.Power_Off')",
                "basis_ids": source_fact_ids,
                "obligation_signature": "complete-effect-audit",
                "required_function_families": ["effect"],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "complete_effect_inventory",
                },
                "rationale": "效果清单进入同一覆盖审计。",
                "record_language": "zh-CN",
            },
            {
                "assertion_chain_id": "ASSERT-004",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-REQ-001",
                "required": True,
                "assert": "simulate(cycles=[[], ['Root.Power_Off']]).final.is_active('Root.Off')",
                "basis_ids": [*segment_ids, *requirement_ids],
                "obligation_signature": "active-power-off-simulation",
                "required_function_families": ["simulation"],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": 2,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "bounded_scenario",
                },
                "rationale": "显式初始化后执行目标事件。",
                "record_language": "zh-CN",
            },
            {
                "assertion_chain_id": "ASSERT-005",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-REQ-001",
                "required": True,
                "assert": "bool(bound_model_refs('CU-REQ-001'))",
                "basis_ids": source_fact_ids,
                "obligation_signature": "exact-identity-attribution",
                "required_function_families": ["mapping"],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "exact_identity",
                    "claim_strength": "mapping_fact",
                },
                "rationale": "覆盖单元必须绑定当前 source/model identity refs。",
                "record_language": "zh-CN",
            },
        ],
        "rationale": "全部片段和行为事实均已进入同一最小测试义务。",
    }


def expression_from_plan(plan: dict[str, Any]) -> str:
    return str(plan["logical_assertions"][0]["assert"])


def expressions_from_plan(plan: dict[str, Any]) -> list[str]:
    return [str(item["assert"]) for item in plan["logical_assertions"]]


def attach_passing_review(controller: DiscoverController) -> CoverageReviewGate:
    registry = controller.require_registry()

    def passing_runner(kind, payload, _attempt):
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
                "已逐条检查完整 NL 义务、行为事实、断言语义、执行结果和 issue 投影，"
                "没有发现遗漏、弱化、误报或漏报风险。"
            ),
            rationale="独立审查确认当前冻结台账满足全部严格通过条件。",
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=passing_runner,
    )
    registry.semantic_review_gate = gate
    return gate
