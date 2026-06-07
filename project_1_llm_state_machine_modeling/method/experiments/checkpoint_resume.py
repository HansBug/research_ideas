"""LG-F1 durable checkpoint / resume experiment runner.

This runner is deliberately separate from the PR-E1 four-case matrix.  LG-F1
resume runs are evidence-only hardening artifacts: they exercise controlled
LangGraph parent-node checkpoints, write ``resume_diff_report.json``, and keep
``main_result_eligible=false`` in the resumed run record.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Sequence

if __package__ and __package__.startswith("project_1_llm_state_machine_modeling."):
    # Allow the PR body / run record entrypoint to be executed from the repo
    # root as ``python -m project_1_llm_state_machine_modeling.method...``.
    # The method package itself intentionally keeps absolute ``method.*``
    # imports for compatibility with the existing ``PYTHONPATH=project_1...``
    # workflow, so this shim only extends sys.path; it never reads ``.env``.
    _PROJECT_ROOT = Path(__file__).resolve().parents[2]
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))

from method.langgraph_runtime import run_lg_f1_resume_experiment
from method.llm_stages import RealEnvLLMProvider
from method.loop import _build_runtime_adapters, _llm_stage_config
from method.experiments.real_run_matrix import condition_specs, make_pr_e1_config, pr_e1_cases
from method.schema import (
    DesignDiagnosticItem,
    DesignFeedback,
    LoopConfig,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from method.staged_runtime import FullStagedRuntimeAdapters, RepairRequest, ScenarioGenerationRequest
from method.stages.ids import STAGE_SPECS_BY_ID, StageId, StageStatus


_CASE_ALIASES = {
    "ABS": "path1_abs",
    "abs": "path1_abs",
    "path1_abs": "path1_abs",
    "Elevator": "path1_elevator",
    "elevator": "path1_elevator",
    "path1_elevator": "path1_elevator",
    "CARA": "path1_cara",
    "cara": "path1_cara",
    "path1_cara": "path1_cara",
    "LNG": "path2_lng_ems",
    "lng": "path2_lng_ems",
    "path2_lng_ems": "path2_lng_ems",
}


def _meta(stage_id: StageId, *, ok: bool = True, status: StageStatus | None = None) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status or (StageStatus.OK if ok else StageStatus.FAIL),
        ok=ok,
    )


def _stable_dsl() -> str:
    return """
state Root {
    state Idle;
    [*] -> Idle;
    Idle -> [*];
}
"""


def _ok_parse(_dsl: str, _context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
    return ParseFeedback(ok=True), _meta(StageId.SD_2_PARSE)


def _ok_semantic(_dsl: str, _context: StageContext) -> tuple[SemanticFeedback, StageResultMeta]:
    return SemanticFeedback(ok=True), _meta(StageId.SD_3_SEMANTIC)


def _blocking_design_once():
    calls = {"count": 0}

    def design(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        calls["count"] += 1
        if calls["count"] == 1:
            return (
                DesignFeedback(
                    ok=False,
                    blocking_items=[
                        DesignDiagnosticItem(
                            code="LG_F1_FIXABLE_DESIGN_BLOCKER",
                            pyfcstm_severity="error",
                            policy_action="budgeted_repair",
                            instance_key="lg-f1:design-once",
                            rationale="force one generic repair path so checkpoint evidence includes repair ledgers",
                        )
                    ],
                ),
                _meta(StageId.SD_4_DESIGN, ok=False),
            )
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    return design


def _scenario_generate(_request: ScenarioGenerationRequest) -> list[TestScenario]:
    return [TestScenario(name="empty_smoke", steps=[])]


def _ok_coverage(_dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
    return {"coverage_report": {"ok": True, "n_scenarios": len(scenarios)}, "coverage_gap": False}, _meta(
        StageId.SD_5A_SCENARIO_COVERAGE
    )


def _ok_sim(_dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
    n = len(getattr(scenarios_or_set, "scenarios", []) or [])
    return SimFeedback(ok=True, n_scenarios=n, n_scenarios_passed=n), _meta(StageId.SD_6_SIM)


def _ok_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
    return ModelReviewFeedback(ok=True, decision="pass", risk_level="none"), _meta(StageId.SL_7_MODEL_REVIEW)


def _ok_repair_review(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
    return RepairReviewFeedback(ok=True, target_resolved=True, drift_risk="none"), _meta(StageId.SD_10_REPAIR_REVIEW)


def build_lg_f1_mock_adapters() -> FullStagedRuntimeAdapters:
    """Return deterministic mock adapters that force one repair path."""

    return FullStagedRuntimeAdapters(
        parse=_ok_parse,
        semantic=_ok_semantic,
        design=_blocking_design_once(),
        scenario_generate=_scenario_generate,
        scenario_coverage=_ok_coverage,
        sim=_ok_sim,
        model_review=_ok_model_review,
        repair=lambda _request: _stable_dsl(),
        repair_review=_ok_repair_review,
    )


def _case_key(raw: str) -> str:
    key = _CASE_ALIASES.get(raw, raw)
    allowed = {case.case_key for case in pr_e1_cases("all")}
    if key not in allowed:
        raise ValueError(f"unknown LG-F1 case {raw!r}; allowed: {', '.join(sorted(_CASE_ALIASES))}")
    return key


def _case_nl(case_key: str) -> str:
    case = {case.case_key: case for case in pr_e1_cases("all")}[case_key]
    return case.nl


def _require_real_env() -> None:
    missing = [key for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL") if not os.environ.get(key)]
    if missing:
        raise RuntimeError(
            "LG-F1 real mode requires provider env; run `set -a; source .env; set +a` first. "
            f"Missing: {', '.join(missing)}"
        )


def _build_real_config(*, output_dir: Path, run_id: str, condition_id: str) -> LoopConfig:
    spec = condition_specs()[condition_id]
    return make_pr_e1_config(spec, output_dir=output_dir, run_id=run_id)


def _build_real_adapters(cfg: LoopConfig) -> tuple[FullStagedRuntimeAdapters, RealEnvLLMProvider]:
    provider = RealEnvLLMProvider()
    llm_cfg = _llm_stage_config(cfg)
    adapters = _build_runtime_adapters(cfg, llm_cfg=llm_cfg, provider=provider)
    return adapters, provider


def _write_markdown_summary(report: dict[str, Any], output_dir: Path, *, mode: str, case_key: str, condition_id: str) -> None:
    lines = [
        "# LG-F1 durable checkpoint / resume evidence",
        "",
        f"- mode: `{mode}`",
        f"- case_key: `{case_key}`",
        f"- condition_id: `{condition_id}`",
        f"- verdict: `{report.get('verdict')}`",
        f"- checkpoint_backend: `{report.get('checkpoint_backend')}` / `{report.get('checkpoint_backend_type')}`",
        f"- interrupt requested/actual: `{report.get('interrupt', {}).get('requested_after')}` / `{report.get('interrupt', {}).get('actual_after')}`",
        f"- run_record_path: `{report.get('run_record_path')}`",
        f"- resume_diff_report_path: `{report.get('resume_diff_report_path')}`",
        f"- resume_run_main_result_eligible: `{report.get('resume_run_main_result_eligible')}`",
        f"- uninterrupted_baseline_available: `{report.get('uninterrupted_baseline_available')}`",
        f"- baseline_comparison_method: `{report.get('baseline_comparison_method')}`",
        f"- baseline_comparison_verdict: `{report.get('baseline_comparison_verdict')}`",
        f"- verdict_scope: `{report.get('verdict_scope')}`",
        f"- support_level: `{report.get('real_agent_loop_resume_support_level')}`",
        f"- scope: `{report.get('real_agent_loop_resume_scope')}`；mid_node_crash_supported=`{report.get('mid_node_crash_supported')}`；nested_subgraph_resume_supported=`{report.get('real_agent_loop_nested_subgraph_resume_supported')}`",
        "",
        "## Append-only audit",
        "",
    ]
    for key, value in sorted((report.get("append_only_audit") or {}).items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Comparison checks", ""])
    if not report.get("uninterrupted_baseline_available"):
        lines.extend(
            [
                "> No independent uninterrupted baseline is available for this run.",
                "> The following checks are `not_applicable` for baseline equivalence and only keep resumed/prefix hashes for audit.",
                "",
            ]
        )
    for item in report.get("comparison_checks") or []:
        lines.append(
            f"- `{item.get('field')}`: `{item.get('verdict')}` "
            f"(basis=`{item.get('comparison_basis') or item.get('comparison_method')}`)"
        )
    stage_replay = report.get("stage_replay_audit") or {}
    lines.extend(
        [
            "",
            "## Stage replay audit",
            "",
            f"- unexpected_stage_replay_detected: `{stage_replay.get('unexpected_stage_replay_detected')}`",
            f"- post_repair_full_revalidation_expected: `{stage_replay.get('post_repair_full_revalidation_expected')}`",
            f"- explanation: {stage_replay.get('explanation') or '<none>'}",
        ]
    )
    lines.extend(
        [
            "",
            "## PR comment snippet",
            "",
            "LG-F1 resume run 是 evidence-only hardening 证据，不进入主四例统计；真实运行如使用 provider，命令前必须 `set -a; source .env; set +a`，且不得回显密钥。",
        ]
    )
    (output_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "pr_comment.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run LG-F1 durable checkpoint/resume experiment.")
    parser.add_argument("--mode", choices=["mock", "real"], default="mock")
    parser.add_argument("--case", default="ABS", help="ABS/Elevator/CARA/LNG or PR-E1 case_key.")
    parser.add_argument("--condition", default="default", choices=sorted(condition_specs().keys()))
    parser.add_argument("--output-dir", default="runs/pr_lg_f1_resume_experiment")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--checkpoint-path", default="")
    parser.add_argument("--interrupt-after", default="", help="Default: repair_sl10_review for mock, sl1_initial_modeling for real.")
    parser.add_argument("--include-uninterrupted-baseline", action="store_true", help="Run a separate uninterrupted baseline; default only for mock mode.")
    parser.add_argument("--no-uninterrupted-baseline", action="store_true")
    parser.add_argument("--stream", action="store_true", help="Enable LangGraph operator stream instrumentation for this experiment.")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    case_key = _case_key(args.case)
    run_id = args.run_id or f"lg-f1-{args.mode}-{case_key}-{args.condition}"
    checkpoint_path = Path(args.checkpoint_path) if args.checkpoint_path else output_dir / "checkpoints.sqlite"
    interrupt_after = args.interrupt_after or ("repair_sl10_review" if args.mode == "mock" else "sl1_initial_modeling")

    if args.mode == "mock":
        cfg = LoopConfig(
            condition_id=run_id,
            condition_family="lg_f1_resume_experiment",
            base_condition_id="full_staged_v1",
            changed_factors=["llm_provider_mode=mock", "checkpoint_backend=sqlite", "resume_experiment=lg_f1"],
            llm_provider_mode="mock",
            academic_question="LG-F1 deterministic durable checkpoint/resume contract; excluded from main results",
            output_dir=str(output_dir / "records"),
            run_id=run_id,
            max_iterations=2,
            compatibility_mode="langgraph_stategraph",
        )
        nl = "The controller starts in Idle and should survive one durable resume."
        adapters = build_lg_f1_mock_adapters()
        provider = None
        uninterrupted_adapters = build_lg_f1_mock_adapters()
        uninterrupted_provider = None
        initial_dsl = _stable_dsl()
    else:
        _require_real_env()
        cfg = _build_real_config(output_dir=output_dir / "records", run_id=run_id, condition_id=args.condition)
        nl = _case_nl(case_key)
        adapters, provider = _build_real_adapters(cfg)
        uninterrupted_adapters = None
        uninterrupted_provider = None
        initial_dsl = ""

    if args.include_uninterrupted_baseline:
        if args.mode == "real":
            uninterrupted_adapters, uninterrupted_provider = _build_real_adapters(cfg)
        elif uninterrupted_adapters is None:
            uninterrupted_adapters = build_lg_f1_mock_adapters()
    if args.no_uninterrupted_baseline:
        uninterrupted_adapters = None
        uninterrupted_provider = None

    report = run_lg_f1_resume_experiment(
        nl,
        config=cfg,
        adapters=adapters,
        uninterrupted_adapters=uninterrupted_adapters,
        uninterrupted_provider=uninterrupted_provider,
        initial_dsl=initial_dsl,
        checkpoint_path=checkpoint_path,
        interrupt_after=interrupt_after,
        operator_stream_enabled=bool(args.stream),
        provider=provider,
    )
    report["mode"] = args.mode
    report["case_key"] = case_key
    report["condition_id"] = args.condition
    Path(report["resume_diff_report_path"]).write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )
    (output_dir / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str), encoding="utf-8")
    _write_markdown_summary(report, output_dir, mode=args.mode, case_key=case_key, condition_id=args.condition)
    print(json.dumps({"summary_json": str(output_dir / "summary.json"), "resume_diff_report": report["resume_diff_report_path"], "verdict": report["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
