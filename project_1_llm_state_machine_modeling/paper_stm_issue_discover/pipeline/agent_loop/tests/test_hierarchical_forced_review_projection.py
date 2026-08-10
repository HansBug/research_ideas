from __future__ import annotations

from pathlib import Path

from paper_stm_repair_loop.controller import DiscoverController
from paper_stm_repair_loop.inputs import PreparedCase
from paper_stm_repair_loop.records import RecordStore
from paper_stm_repair_loop.schemas.coverage_review import CoverageReviewVerdict
from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm
from paper_stm_repair_loop.tools.review_discovery_coverage import CoverageReviewGate


FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures/discover_integrated/0000_hldcs_manual_identity/STM_0.fcstm"
)
ROOT = "HighLevelDrivingModule"
SOURCE = f"{ROOT}.Autonomous.AutoFinal"
DECLARING_SOURCE = f"{ROOT}.Autonomous"
EVENT = f"{ROOT}.HumanSteeringCommand"
TARGET = f"{ROOT}.HumanDriving"


def _controller(tmp_path: Path) -> DiscoverController:
    model = FIXTURE.read_text(encoding="utf-8")
    case = PreparedCase(
        case_id="manual-0000-forced-review",
        pair_id=None,
        nl=(
            "Transit to human driving mode when receiving a human steering "
            "command in AutoFinal."
        ),
        raw_source=model,
        raw_source_format="fcstm-identity",
        fcstm=model,
        source_trace={
            "schema_version": "source_trace_base.v1",
            "trace_scope": "test",
            "relation_policy": "exact_identity",
            "entries": [],
        },
        metadata={"nl_language": "en-US"},
        input_mode="custom",
    )
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
        {"schema_hashes": {"test_fixture": "hierarchical-forced-review-v1"}},
    )
    return DiscoverController(
        case,
        {
            "run_id": "manual-0000-forced-review",
            "profile": "test",
            "content_language": "zh-CN",
            "renderer": "quiet",
            "formal_profile": True,
            "agent_limits": {},
            "input_sha256": {},
        },
        checked,
        store,
    )


def _plan(controller: DiscoverController) -> dict:
    frozen = controller.prepare()
    segment_ids = [segment.segment_id for segment in frozen.input_segments]
    requirements = list(frozen.coverage_requirements)
    requirement_ids = [item.requirement_id for item in requirements]
    structure_requirement_ids = [
        item.requirement_id for item in requirements if item.dimension == "structure"
    ]
    behavior_requirement_ids = [
        item.requirement_id for item in requirements if item.dimension != "structure"
    ]

    declaring = next(
        fact
        for fact in frozen.source_facts
        if fact.fact_kind == "forced_transition"
        and fact.source == DECLARING_SOURCE
        and fact.event == EVENT
        and fact.target == TARGET
        and fact.payload.get("forced_expansion_role") == "declaring_edge"
    )
    relay = next(
        fact
        for fact in frozen.source_facts
        if fact.fact_kind == "forced_transition"
        and fact.source == SOURCE
        and fact.event == EVENT
        and fact.target == "[*]"
        and fact.payload.get("forced_expansion_role") == "inherited_exit_relay"
    )
    source_fact_ids = [declaring.fact_id, relay.fact_id]
    model_refs = sorted({*declaring.qualified_refs, *relay.qualified_refs})
    relation_expression = (
        f"transition_exists(source='{SOURCE}', event='{EVENT}', target='[*]') "
        f"and transition_exists(source='{DECLARING_SOURCE}', event='{EVENT}', "
        f"target='{TARGET}')"
    )
    simulation_expression = (
        f"simulate(initial_state='{SOURCE}', initial_vars={{}}, "
        f"cycles=[['{EVENT}']]).final.is_active('{TARGET}')"
    )

    return {
        "segment_dispositions": [],
        "fact_dispositions": [],
        "coverage_units": [
            {
                "coverage_unit_id": "CU-TAKEOVER",
                "unit_kind": "behavior_obligation",
                "segment_ids": segment_ids,
                "source_fact_ids": source_fact_ids,
                "requirement_ids": requirement_ids,
                "dimensions": sorted({item.dimension for item in requirements}),
                "statement": "AutoFinal 中收到人工转向命令后进入人工驾驶。",
                "rationale": "该事件因果义务需要层次静态链与运行行为共同支撑。",
                "record_language": "zh-CN",
                "in_scope": True,
            }
        ],
        "proposition_roots": [
            {
                "node_id": "ROOT-TAKEOVER",
                "previous_node_id": None,
                "coverage_unit_id": "CU-TAKEOVER",
                "statement": "人工转向命令使 AutoFinal 返回 HumanDriving。",
                "model_element_refs": model_refs,
                "source_element_refs": [f"source:requirement:{segment_ids[0]}"],
                "rationale": "正向命题必须由真实层次语义和事件周期共同验证。",
                "record_language": "zh-CN",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-STRUCTURE",
                "root_node_id": "ROOT-TAKEOVER",
                "coverage_unit_id": "CU-TAKEOVER",
                "required": True,
                "assert": (
                    f"len(states(name='{SOURCE}')) == 1 and "
                    f"len(states(name='{TARGET}')) == 1"
                ),
                "basis_ids": [*segment_ids, *structure_requirement_ids],
                "obligation_signature": "takeover-state-scope",
                "required_function_families": ["structure"],
                "evidence_scope": {
                    "semantic_profile": "hierarchical_forced_transition_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "named_state_scope",
                },
                "rationale": "锁定 NL 明示的源状态和目标状态。",
                "record_language": "zh-CN",
            },
            {
                "assertion_chain_id": "ASSERT-STATIC-CHAIN",
                "root_node_id": "ROOT-TAKEOVER",
                "coverage_unit_id": "CU-TAKEOVER",
                "required": True,
                "assert": relation_expression,
                "basis_ids": [
                    *segment_ids,
                    *behavior_requirement_ids,
                    *source_fact_ids,
                ],
                "obligation_signature": "takeover-relay-and-declaration",
                "required_function_families": ["relation"],
                "evidence_scope": {
                    "semantic_profile": "hierarchical_forced_transition_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "forced_expansion_static_chain",
                },
                "rationale": "静态 grounding 必须同时包含子层接力与父层声明边。",
                "record_language": "zh-CN",
            },
            {
                "assertion_chain_id": "ASSERT-RUNTIME",
                "root_node_id": "ROOT-TAKEOVER",
                "coverage_unit_id": "CU-TAKEOVER",
                "required": True,
                "assert": simulation_expression,
                "basis_ids": [*segment_ids, *behavior_requirement_ids],
                "obligation_signature": "takeover-event-causal-runtime",
                "required_function_families": ["simulation"],
                "evidence_scope": {
                    "semantic_profile": "hierarchical_forced_transition_v1",
                    "max_steps": 1,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "hot_start_event_causality",
                },
                "rationale": "从完整 hot start 在首个周期执行事件并检查运行目标。",
                "record_language": "zh-CN",
            },
        ],
        "rationale": "层次静态链和事件周期共同闭合单一接管义务。",
    }


def test_forced_relay_chain_and_runtime_project_to_reviewer_accepted_zero_issue(
    tmp_path: Path,
) -> None:
    controller = _controller(tmp_path)
    plan = _plan(controller)
    registry = controller.require_registry()
    registered = registry.register_plan(plan, reason="注册层次接管义务。")
    assert registered["accepted"] is True, registered

    for assertion in plan["logical_assertions"]:
        evaluated = registry.eval_assert(
            assertion["assert"], reason="执行层次接管义务的当前断言。"
        )
        assert evaluated["match_status"] == "matches", evaluated

    def runner(kind: str, payload: dict, _attempt: int) -> CoverageReviewVerdict:
        expressions = {
            item["assert"] for item in payload["registered_plan"]["latest_assertions"]
        }
        assert not any(
            f"source='{SOURCE}', event='{EVENT}', target='{TARGET}'" in expression
            for expression in expressions
        )
        assert any(
            f"source='{SOURCE}', event='{EVENT}', target='[*]'" in expression
            and f"source='{DECLARING_SOURCE}', event='{EVENT}', target='{TARGET}'"
            in expression
            and " and " in expression
            for expression in expressions
        )

        evaluations = list(payload["latest_evaluations"].values())
        simulation_evaluation = next(
            item
            for item in evaluations
            if "simulation" in item["observed_function_families"]
        )
        simulation_call = next(
            item
            for item in simulation_evaluation["function_calls"]
            if item["function"] == "simulate"
        )
        simulation = simulation_call["result"]["data"]
        initialization = simulation["effective_initialization"]["data"]
        cycle = simulation["cycles"][0]["data"]
        assert initialization["mode"] == "hot"
        assert initialization["state"] == SOURCE
        assert SOURCE in initialization["active_states"]
        assert EVENT in cycle["consumed_events"]
        assert EVENT not in cycle["unconsumed_events"]
        assert TARGET in cycle["active_states"]
        assert cycle["is_ended"] is False

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
                "Static evidence preserves the relay AND declaring edge, while "
                "the hot-start event cycle consumes the command and reaches the "
                "declared business target without terminating the root machine."
            ),
            rationale=(
                "The current ledger contains hierarchy-aware static grounding and "
                "matching executable event-causality evidence for every frozen ID."
            ),
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=runner,
    )
    registry.semantic_review_gate = gate
    reviewed = gate.review(reason="审查层次接力和运行行为的完整证据链。")

    assert reviewed["passed"] is True, reviewed
    assert gate.current_passed() is True
    projection = registry.project_roots()
    assert projection["run_outcome"] == "reviewer_accepted_zero_issue"
    assert projection["registered_worklist_complete"] is True
    assert projection["issue_root_projection"] == []
    assert projection["incomplete_root_projection"] == []
    assert [item["status"] for item in projection["proposition_roots"]] == ["ok"]
    assert [item["node_id"] for item in projection["regression_guard_projection"]] == [
        "ROOT-TAKEOVER"
    ]
    assert registry.assert_submit_allowed()["submit_allowed"] is True
