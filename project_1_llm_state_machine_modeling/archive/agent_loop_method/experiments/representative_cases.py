"""PR-D representative full-run evidence helpers.

This module is intentionally small and stdlib-only.  PR-D needs two things:

1. run the canonical ``archive.agent_loop_method.loop.run_agent_loop(nl, LoopConfig())`` entry on
   the two representative NL inputs that #14 exposed; and
2. turn the resulting ``AgentLoopRunRecord`` files into an issue-comment-ready,
   secret-safe evidence summary.

The runner never reads ``.env`` by itself.  It only checks process environment
variables, matching the project rule that shell/CI is responsible for sourcing
``.env`` before invoking Python.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

if __package__ and __package__.startswith("project_1_llm_state_machine_modeling."):
    # Allow repo-root package execution, for example
    # ``python -m project_1_llm_state_machine_modeling.archive.agent_loop_method.experiments.representative_cases``.
    # The method implementation keeps absolute ``archive.agent_loop_method.*`` imports to preserve
    # the historical ``PYTHONPATH=project_1_llm_state_machine_modeling`` workflow;
    # package-mode execution therefore needs the project package root on sys.path.
    # This bootstrap does not read ``.env`` and does not touch provider config.
    _PROJECT_ROOT = Path(__file__).resolve().parents[3]
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))

from archive.agent_loop_method.loop import LoopConfig, run_agent_loop
from archive.agent_loop_method.run_record import is_path_result_eligible, read_agent_loop_run_record
from archive.agent_loop_method.schema import AgentLoopResult, AgentLoopRunRecord


PATH1_CARA_NL = """At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target."""


PATH2_LNG_EMS_NL = """The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice."""


@dataclass(frozen=True)
class RepresentativeCase:
    """One PR-D representative NL case."""

    case_key: str
    path: str
    case_id: str
    title: str
    issue14_comment_url: str
    nl: str


@dataclass(frozen=True)
class RepresentativeRunSummary:
    """Secret-safe summary for one completed PR-D representative run."""

    case: RepresentativeCase
    result_status: str
    error_message: str | None
    run_record_id: str | None
    run_record_path: str
    record_status: str
    verdict: str | None
    verdict_source_stage_id: str | None
    verdict_reason: str | None
    final_dsl_length: int
    stage_ids: list[str]
    planned_stage_ids: list[str]
    executed_stage_ids: list[str]
    executed_missing_stage_ids: list[str]
    llm_stage_ids: list[str]
    iteration_count: int
    repair_count: int
    scenario_history_count: int
    scenario_set_id: str | None
    scenario_epoch: int | None
    oracle_weak: bool
    main_result_eligible: bool
    inclusion_reason: str | None
    exclusion_reason: str | None
    provider_mode: str | None
    provider_model_redacted: str | None
    provider_config_read: bool | None
    real_llm_provider_api: bool | None
    git_commit: str | None
    config_hash: str | None
    condition_id: str | None
    policy_profile: str | None
    schema_valid: bool
    schema_validation_error: str | None
    secret_redacted: bool
    redaction_report_count: int
    planned_stage_graph_full_staged: bool
    executed_trace_full_staged: bool
    no_legacy_scenario_unavailable: bool


RunAgentLoopFn = Callable[[str, LoopConfig], AgentLoopResult]


REQUIRED_ENV_KEYS = ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL")


FULL_STAGED_REQUIRED_STAGE_IDS = [
    "SC-0",
    "SL-1",
    "SD-2",
    "SD-3",
    "SD-4",
    "SL-5",
    "SD-5A",
    "SC-5F",
    "SD-6",
    "SL-7",
    "SD-8",
    "SL-9",
    "SD-10",
    "SL-10B",
    "SC-11",
    "SC-12",
    "SC-13",
]


def representative_cases() -> list[RepresentativeCase]:
    """Return the two mandatory #14 representative NL cases."""

    return [
        RepresentativeCase(
            case_key="path1_cara",
            path="path1",
            case_id="cara-infusion-pump-formal-spec__01",
            title="Path1 CARA representative NL",
            issue14_comment_url="https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890685",
            nl=PATH1_CARA_NL,
        ),
        RepresentativeCase(
            case_key="path2_lng_ems",
            path="path2",
            case_id="state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship",
            title="Path2 LNG-ship EMS representative NL",
            issue14_comment_url="https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890799",
            nl=PATH2_LNG_EMS_NL,
        ),
    ]


def missing_provider_env(env: dict[str, str] | None = None) -> list[str]:
    """Return missing real-provider environment keys without exposing values."""

    source = env if env is not None else os.environ
    return [key for key in REQUIRED_ENV_KEYS if not source.get(key)]


def make_pr_d_config(case: RepresentativeCase, output_dir: str | Path) -> LoopConfig:
    """Build the canonical default config for one PR-D representative run."""

    return LoopConfig(output_dir=str(output_dir), run_id=f"pr-d-{case.case_key}")


def assert_pr_d_provider_env(env: dict[str, str] | None = None) -> None:
    missing = missing_provider_env(env)
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"PR-D real-provider evidence requires process environment keys: {joined}")


def run_representative_cases(
    *,
    output_dir: str | Path,
    run_agent_loop_fn: RunAgentLoopFn = run_agent_loop,
    cases: Sequence[RepresentativeCase] | None = None,
    require_provider_env: bool = True,
) -> list[RepresentativeRunSummary]:
    """Run the mandatory PR-D cases and return validated summaries."""

    if require_provider_env:
        assert_pr_d_provider_env()

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    summaries: list[RepresentativeRunSummary] = []
    for case in cases or representative_cases():
        config = make_pr_d_config(case, out)
        result = run_agent_loop_fn(case.nl, config)
        if not result.run_record_path:
            raise RuntimeError(f"{case.case_key} did not produce an AgentLoopRunRecord: {result.error_message}")
        record = read_agent_loop_run_record(result.run_record_path)
        summaries.append(summarize_run(case, result, record, result.run_record_path))
    return summaries


def summarize_run(
    case: RepresentativeCase,
    result: AgentLoopResult,
    record: AgentLoopRunRecord,
    run_record_path: str | Path,
) -> RepresentativeRunSummary:
    """Validate and summarize a PR-D representative run record."""

    final = record.final_artifacts
    environment = record.environment
    resolved = environment.get("resolved_config") if isinstance(environment.get("resolved_config"), dict) else {}
    planned_stage_ids = _planned_stage_ids_from_record(record)
    executed_stage_ids = _executed_stage_ids_from_record(record)
    executed_missing_stage_ids = _missing_required_stage_ids(executed_stage_ids)
    schema_validation_error = _schema_validation_error(record)
    final_dsl = str(final.get("final_dsl") or result.final_dsl or "")
    payload_text = _record_public_text(record)
    no_legacy_scenario_unavailable = "scenario generation unavailable because initial DSL parse failed" not in payload_text
    return RepresentativeRunSummary(
        case=case,
        result_status=result.status,
        error_message=result.error_message,
        run_record_id=result.run_record_id,
        run_record_path=str(run_record_path),
        record_status=record.status,
        verdict=_optional_str(final.get("verdict")),
        verdict_source_stage_id=_optional_str(final.get("verdict_source_stage_id")),
        verdict_reason=_optional_str(final.get("verdict_reason")),
        final_dsl_length=len(final_dsl),
        stage_ids=executed_stage_ids,
        planned_stage_ids=planned_stage_ids,
        executed_stage_ids=executed_stage_ids,
        executed_missing_stage_ids=executed_missing_stage_ids,
        llm_stage_ids=_llm_stage_ids(record),
        iteration_count=len(record.iteration_records),
        repair_count=len(record.repair_history),
        scenario_history_count=len(record.scenario_history),
        scenario_set_id=_latest_scenario_value(record, "scenario_set_id"),
        scenario_epoch=_latest_scenario_int(record, "epoch"),
        oracle_weak=bool(final.get("oracle_weak")),
        main_result_eligible=bool(final.get("main_result_eligible")) and is_path_result_eligible(record),
        inclusion_reason=_optional_str(final.get("inclusion_reason")),
        exclusion_reason=_optional_str(final.get("exclusion_reason")),
        provider_mode=_optional_str(environment.get("provider_mode")),
        provider_model_redacted=_optional_str(environment.get("provider_model_redacted")),
        provider_config_read=_optional_bool(environment.get("provider_config_read")),
        real_llm_provider_api=_optional_bool(environment.get("real_llm_provider_api")),
        git_commit=_optional_str(environment.get("git_commit")),
        config_hash=_optional_str(environment.get("config_hash")),
        condition_id=_optional_str(resolved.get("condition_id")),
        policy_profile=_optional_str(resolved.get("policy_profile")),
        schema_valid=schema_validation_error is None,
        schema_validation_error=schema_validation_error,
        secret_redacted=not _contains_obvious_secret(payload_text),
        redaction_report_count=len(record.redaction_report),
        planned_stage_graph_full_staged=_contains_full_staged_path(planned_stage_ids),
        executed_trace_full_staged=_contains_full_staged_path(executed_stage_ids),
        no_legacy_scenario_unavailable=no_legacy_scenario_unavailable,
    )


def render_issue_comment(summaries: Sequence[RepresentativeRunSummary]) -> str:
    """Render a GitHub issue comment for PR-D representative evidence."""

    lines = [
        "## PR-D representative full staged run evidence",
        "",
        "本 comment 汇总 PR-D 对 #14 两条 representative NL 的真实默认入口复跑结果。",
        "",
        "### 总体结论",
        "",
        "| Case | verdict | record status | main result eligible | oracle weak | planned graph | executed trace | wiring断链 | run record |",
        "|---|---|---|---:|---:|---|---|---|---|",
    ]
    for summary in summaries:
        lines.append(
            "| {case} | `{verdict}` | `{record_status}` | {eligible} | {oracle_weak} | {planned_graph} | {executed_trace} | {wiring} | `{path}` |".format(
                case=summary.case.title,
                verdict=summary.verdict,
                record_status=summary.record_status,
                eligible=_yes_no(summary.main_result_eligible),
                oracle_weak=_yes_no(summary.oracle_weak),
                planned_graph="✅" if summary.planned_stage_graph_full_staged else "⚠️",
                executed_trace=_executed_trace_cell(summary),
                wiring="✅ 未出现" if summary.no_legacy_scenario_unavailable else "❌ 仍出现",
                path=summary.run_record_path,
            )
        )
    for summary in summaries:
        lines.extend(_render_case_section(summary))
    lines.extend(
        [
            "",
            "### PR-D 解释边界",
            "",
            "- 若 verdict 为 `not_converged`，本 evidence 只能说明默认入口与 run-record 基础设施可审计执行，不能解释为模型质量已经达到高可信主结果。",
            "- 只有 verdict 为 `success` 且 `main_result_eligible=true` 时，才可作为 Path1/Path2 后续高可信主结果候选。",
            "- `planned graph` 表示默认 staged path 的计划图是否齐备；`executed trace` 表示本次实际执行轨迹是否覆盖全部 stage。若 run 在 pre-scenario repair 阶段停止，后续 scenario / sim / review stage 会被列为未执行，不能误读为已完整执行。",
            "- 本 comment 不包含 provider secret；provider/model 仅以 run record 中的脱敏标识呈现。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def summaries_to_jsonable(summaries: Sequence[RepresentativeRunSummary]) -> list[dict[str, object]]:
    """Return a compact JSON-serializable summary payload."""

    payload: list[dict[str, object]] = []
    for summary in summaries:
        payload.append(
            {
                "case_key": summary.case.case_key,
                "path": summary.case.path,
                "case_id": summary.case.case_id,
                "result_status": summary.result_status,
                "record_status": summary.record_status,
                "verdict": summary.verdict,
                "verdict_source_stage_id": summary.verdict_source_stage_id,
                "verdict_reason": summary.verdict_reason,
                "run_record_id": summary.run_record_id,
                "run_record_path": summary.run_record_path,
                "stage_ids": summary.stage_ids,
                "planned_stage_ids": summary.planned_stage_ids,
                "executed_stage_ids": summary.executed_stage_ids,
                "executed_missing_stage_ids": summary.executed_missing_stage_ids,
                "llm_stage_ids": summary.llm_stage_ids,
                "iteration_count": summary.iteration_count,
                "repair_count": summary.repair_count,
                "scenario_history_count": summary.scenario_history_count,
                "scenario_set_id": summary.scenario_set_id,
                "scenario_epoch": summary.scenario_epoch,
                "oracle_weak": summary.oracle_weak,
                "main_result_eligible": summary.main_result_eligible,
                "provider_mode": summary.provider_mode,
                "provider_model_redacted": summary.provider_model_redacted,
                "provider_config_read": summary.provider_config_read,
                "real_llm_provider_api": summary.real_llm_provider_api,
                "git_commit": summary.git_commit,
                "config_hash": summary.config_hash,
                "condition_id": summary.condition_id,
                "policy_profile": summary.policy_profile,
                "schema_valid": summary.schema_valid,
                "schema_validation_error": summary.schema_validation_error,
                "secret_redacted": summary.secret_redacted,
                "redaction_report_count": summary.redaction_report_count,
                "planned_stage_graph_full_staged": summary.planned_stage_graph_full_staged,
                "executed_trace_full_staged": summary.executed_trace_full_staged,
                "no_legacy_scenario_unavailable": summary.no_legacy_scenario_unavailable,
            }
        )
    return payload


def _render_case_section(summary: RepresentativeRunSummary) -> list[str]:
    return [
        "",
        f"### {summary.case.title}",
        "",
        f"- 上游 #14 诊断：{summary.case.issue14_comment_url}",
        f"- case_id：`{summary.case.case_id}`",
        f"- 输入 NL 长度：`{len(summary.case.nl)}`",
        f"- run_id：`{summary.run_record_id}`",
        f"- run record：`{summary.run_record_path}`",
        f"- git commit：`{summary.git_commit}`",
        f"- resolved config：condition_id=`{summary.condition_id}`，policy_profile=`{summary.policy_profile}`，config_hash=`{summary.config_hash}`",
        f"- provider/model：mode=`{summary.provider_mode}`，real_api=`{summary.real_llm_provider_api}`，config_read=`{summary.provider_config_read}`，model=`{summary.provider_model_redacted}`",
        f"- verdict：`{summary.verdict}`，record_status=`{summary.record_status}`，source_stage=`{summary.verdict_source_stage_id}`",
        f"- verdict reason：{summary.verdict_reason or '<none>'}",
        f"- planned stage graph：full_staged=`{summary.planned_stage_graph_full_staged}`，stage_count=`{len(summary.planned_stage_ids)}`",
        f"- executed trace：full_staged=`{summary.executed_trace_full_staged}`，executed_count=`{len(summary.executed_stage_ids)}`，missing_required=`{', '.join(summary.executed_missing_stage_ids) or '<none>'}`",
        f"- stage 摘要：iterations=`{summary.iteration_count}`，repairs=`{summary.repair_count}`，scenario_history=`{summary.scenario_history_count}`，LLM stages=`{', '.join(summary.llm_stage_ids) or '<none>'}`",
        f"- scenario：scenario_set_id=`{summary.scenario_set_id}`，epoch=`{summary.scenario_epoch}`，oracle_weak=`{summary.oracle_weak}`",
        f"- eligibility：main_result_eligible=`{summary.main_result_eligible}`，inclusion_reason=`{summary.inclusion_reason}`，exclusion_reason=`{summary.exclusion_reason}`",
        f"- redaction/schema：schema_valid=`{summary.schema_valid}`，schema_error=`{summary.schema_validation_error}`，secret_redacted=`{summary.secret_redacted}`，redaction_report_count=`{summary.redaction_report_count}`",
        f"- 旧 wiring 断链检查：`scenario generation unavailable because initial DSL parse failed` 出现？`{not summary.no_legacy_scenario_unavailable}`",
        f"- final DSL length：`{summary.final_dsl_length}`",
    ]


def _planned_stage_ids_from_record(record: AgentLoopRunRecord) -> list[str]:
    ids: list[str] = []
    planned = record.stage_graph.get("planned") if isinstance(record.stage_graph, dict) else None
    if isinstance(planned, list):
        ids.extend(_unique_stage_ids(planned))
    return ids


def _executed_stage_ids_from_record(record: AgentLoopRunRecord) -> list[str]:
    ids: list[str] = []
    executed = record.stage_graph.get("executed") if isinstance(record.stage_graph, dict) else None
    if isinstance(executed, list):
        ids.extend(_unique_stage_ids(executed))
    for stage_id in _stage_record_ids(record):
        if stage_id not in ids:
            ids.append(stage_id)
    return ids


def _stage_ids_from_record(record: AgentLoopRunRecord) -> list[str]:
    """Return executed stage IDs without mixing planned graph evidence.

    A complete ``stage_graph.planned`` only proves that the default staged path
    is wired.  PR-D summaries must not use planned IDs as evidence that a stage
    actually ran.
    """

    return _executed_stage_ids_from_record(record)


def _stage_record_ids(record: AgentLoopRunRecord) -> list[str]:
    ids: list[str] = []
    for meta in record.stage_records:
        if isinstance(meta, dict):
            stage_id = meta.get("stage_id")
        else:
            stage_id = getattr(meta, "stage_id", None)
        if stage_id:
            ids.append(str(stage_id))
    return ids


def _unique_stage_ids(stage_ids: Iterable[object]) -> list[str]:
    ids: list[str] = []
    for stage_id in stage_ids:
        if stage_id and str(stage_id) not in ids:
            ids.append(str(stage_id))
    return ids


def _missing_required_stage_ids(stage_ids: Iterable[str]) -> list[str]:
    present = set(stage_ids)
    return [stage_id for stage_id in FULL_STAGED_REQUIRED_STAGE_IDS if stage_id not in present]


def _llm_stage_ids(record: AgentLoopRunRecord) -> list[str]:
    ids: list[str] = []
    for interaction in record.llm_interactions:
        if isinstance(interaction, dict) and interaction.get("stage_id"):
            ids.append(str(interaction["stage_id"]))
    return ids


def _latest_scenario_value(record: AgentLoopRunRecord, key: str) -> str | None:
    for item in reversed(record.scenario_history):
        if isinstance(item, dict) and item.get(key) is not None:
            return str(item[key])
    return None


def _latest_scenario_int(record: AgentLoopRunRecord, key: str) -> int | None:
    value = _latest_scenario_value(record, key)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _contains_full_staged_path(stage_ids: Iterable[str]) -> bool:
    present = set(stage_ids)
    return all(stage_id in present for stage_id in FULL_STAGED_REQUIRED_STAGE_IDS)


def _schema_validation_error(record: AgentLoopRunRecord) -> str | None:
    try:
        AgentLoopRunRecord(**asdict(record))
    except (TypeError, ValueError) as exc:
        return str(exc)
    return None


def _executed_trace_cell(summary: RepresentativeRunSummary) -> str:
    total = len(FULL_STAGED_REQUIRED_STAGE_IDS)
    if summary.executed_trace_full_staged:
        return f"✅ {len(summary.executed_stage_ids)}/{total}"
    return f"⚠️ {len(summary.executed_stage_ids)}/{total}"


def _record_public_text(record: AgentLoopRunRecord) -> str:
    payload = {
        "input_bundle": record.input_bundle,
        "run_config": record.run_config,
        "environment": record.environment,
        "stage_graph": record.stage_graph,
        "stage_records": record.stage_records,
        "iteration_records": record.iteration_records,
        "llm_interactions": record.llm_interactions,
        "deterministic_feedback": record.deterministic_feedback,
        "repair_history": record.repair_history,
        "scenario_history": record.scenario_history,
        "final_artifacts": record.final_artifacts,
        "logs": record.logs,
        "replay_index": record.replay_index,
        "redaction_report": record.redaction_report,
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)


def _contains_obvious_secret(text: str) -> bool:
    lowered = text.lower()
    if "authorization: bearer" in lowered:
        return True
    if re.search(r"\bsk-[A-Za-z0-9][A-Za-z0-9._-]{7,}", text):
        return True
    for key in REQUIRED_ENV_KEYS:
        value = os.environ.get(key)
        if value and len(value) >= 8 and value in text:
            return True
    return False


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def _yes_no(value: bool) -> str:
    return "✅" if value else "❌"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run PR-D representative full staged evidence cases.")
    parser.add_argument("--output-dir", default="runs/pr_d_representative", help="Directory for run records and summaries.")
    parser.add_argument("--summary-json", default=None, help="Optional JSON summary path.")
    parser.add_argument("--issue-comment-md", default=None, help="Optional issue comment markdown path.")
    parser.add_argument("--allow-missing-provider-env", action="store_true", help="Only for dry testing; real PR-D evidence must not use this.")
    args = parser.parse_args(argv)

    summaries = run_representative_cases(
        output_dir=args.output_dir,
        require_provider_env=not args.allow_missing_provider_env,
    )

    if args.summary_json:
        Path(args.summary_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.summary_json).write_text(
            json.dumps(summaries_to_jsonable(summaries), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.issue_comment_md:
        Path(args.issue_comment_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.issue_comment_md).write_text(render_issue_comment(summaries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
