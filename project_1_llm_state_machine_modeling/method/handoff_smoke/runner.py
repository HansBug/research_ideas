"""PR-3 Path1/Path2 handoff smoke runner.

This module is deliberately small and experiment-scoped.  It does not compute
Path 1 component F1 or Path 2 feature-utilization metrics.  Its only purpose is
to prove that representative upstream Path1/Path2 artifacts can be fed into the
agent-loop infrastructure and produce schema-valid, self-contained
``AgentLoopRunRecord`` files.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from method.gpt_client import get_default_model
from method.experiments.ablation.deterministic_loop import DeterministicLoopConfig, ReviewPolicy, run_deterministic_ablation_loop
from method.run_record import is_path_result_eligible, read_agent_loop_run_record
from method.schema import GroundedElement, GroundingMap, TestScenario
from method.stages.ids import StageId
from method.stages.sl_model_review_prompt import parse_sl7_model_review_response


@dataclass
class HandoffSmokeConfig:
    """Config loaded from ``configs/path*_representative.json``."""

    schema_version: str
    path: str
    description: str
    source_snapshot: dict[str, Any]
    case_selector: dict[str, Any]
    loop: dict[str, Any]
    scenario: dict[str, Any]
    compatibility_checks: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.path not in {"path1", "path2"}:
            raise ValueError("HandoffSmokeConfig.path must be path1 or path2")
        if self.schema_version != "agent-loop-pr3-handoff-config.v1":
            raise ValueError(f"unsupported handoff config schema: {self.schema_version}")


@dataclass
class HandoffSmokeResult:
    """Summary returned by one PR-3 representative smoke run."""

    path: str
    case_id: str
    run_id: str
    run_record_path: str
    record_status: str
    main_result_eligible: bool
    final_dsl_hash: str
    stage_ids: list[str]
    llm_review_provider: str
    llm_review_model: str
    llm_review_decision: str
    llm_review_retry_count: int
    llm_review_attempt_statuses: list[str]
    checks: dict[str, bool]


def load_handoff_config(path: str | Path) -> HandoffSmokeConfig:
    """Load a PR-3 representative smoke config JSON."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return HandoffSmokeConfig(**payload)


def _git_show(ref: str, repo_path: str, *, cwd: str | Path | None = None) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{repo_path}"], cwd=cwd)


def _load_snapshot_text(snapshot: dict[str, Any], key: str, *, cwd: str | Path | None = None) -> str:
    return _git_show(str(snapshot["commit"]), str(snapshot[key]), cwd=cwd).decode("utf-8")


def _load_snapshot_parquet(snapshot: dict[str, Any], *, cwd: str | Path | None = None) -> pd.DataFrame:
    data = _git_show(str(snapshot["commit"]), str(snapshot["parquet_path"]), cwd=cwd)
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=True) as f:
        f.write(data)
        f.flush()
        return pd.read_parquet(f.name)


def _select_row(df: pd.DataFrame, selector: dict[str, Any]) -> dict[str, Any]:
    case_id = selector.get("case_id")
    if case_id is not None and "case_id" in df.columns:
        matches = df[df["case_id"].astype(str) == str(case_id)]
        if len(matches) > 0:
            return dict(matches.iloc[0].to_dict())
    index = int(selector.get("fallback_row_index", 0))
    if len(df) <= index:
        raise IndexError(f"fallback_row_index {index} out of range for parquet with {len(df)} rows")
    return dict(df.iloc[index].to_dict())


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    return str(value)


def _scenario_from_config(payload: dict[str, Any]) -> TestScenario:
    return TestScenario(
        name=str(payload.get("name") or "handoff_hot_start"),
        description=str(payload.get("description") or ""),
        initial_state=payload.get("initial_state"),
        initial_vars=dict(payload.get("initial_vars") or {}),
        steps=list(payload.get("steps") or []),
    )


def _grounding_from_row(row: dict[str, Any], path_name: str) -> GroundingMap:
    case_id = str(row.get("case_id") or row.get("sample_id") or "unknown-case")
    nl = str(row.get("nl_text") or row.get("requirement") or row.get("requirements") or "")
    return GroundingMap(
        elements=[
            GroundedElement(
                element_id=f"{path_name}:{case_id}:requirement",
                element_kind="state",
                element_ref="Root",
                source_stage="PR-3-handoff-smoke",
                evidence_text=nl[:500] if nl else f"Representative {path_name} smoke case {case_id}.",
                requiredness="unknown",
            )
        ],
        source_summary={
            "path": path_name,
            "case_id": case_id,
            "source_dir": str(row.get("source_dir") or ""),
            "stm_md_path": str(row.get("stm_md_path") or ""),
        },
    )


def _review_policy_from_config(payload: dict[str, Any]) -> ReviewPolicy:
    return ReviewPolicy(**dict(payload.get("review_policy") or {}))


def _require_llm_env() -> dict[str, str]:
    required = ["LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"]
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise KeyError("missing LLM env vars; run `source .env` first: " + ", ".join(missing))
    return {key: os.environ[key] for key in required}


def _record_stage_ids(record: Any) -> list[str]:
    return [str(row.get("stage_id")) for row in record.stage_records]


def _first_sl7_interaction(record: Any) -> dict[str, Any]:
    for item in record.llm_interactions:
        if item.get("stage_id") == StageId.SL_7_MODEL_REVIEW.value:
            return item
    raise AssertionError("missing SL-7 interaction in run record")


def run_handoff_smoke(
    config: HandoffSmokeConfig,
    *,
    output_dir: str | Path,
    real_llm: bool = False,
    llm_model: str | None = None,
    max_tokens: int = 1000,
    max_retries: int = 2,
    cwd: str | Path | None = None,
) -> HandoffSmokeResult:
    """Run one representative Path1/Path2 agent-loop handoff smoke."""
    df = _load_snapshot_parquet(config.source_snapshot, cwd=cwd)
    row = _select_row(df, config.case_selector)
    nl = str(row.get("nl_text") or row.get("requirement") or row.get("requirements") or "")
    if len(nl) <= 20:
        raise ValueError(f"representative NL is too short for {config.path}: {nl!r}")
    initial_dsl = _load_snapshot_text(config.source_snapshot, "fcstm_path", cwd=cwd)
    scenario = _scenario_from_config(config.scenario)
    grounding = _grounding_from_row(row, config.path)

    loop_payload = config.loop
    run_id = str(loop_payload.get("run_id") or f"pr3-{config.path}-smoke")
    review_policy = _review_policy_from_config(loop_payload)
    path_context = {
        "pr": "PR-3",
        "issue": "#14",
        "path": config.path,
        "case_row": _jsonable(row),
        "source_snapshot": _jsonable(config.source_snapshot),
        "compatibility_checks": list(config.compatibility_checks),
        "not_formal_path_metric": True,
    }
    cfg = DeterministicLoopConfig(
        initial_dsl=initial_dsl,
        scenarios=[scenario],
        repair_candidates=[],
        grounding_map=grounding,
        run_id=run_id,
        output_dir=output_dir,
        max_iterations=int(loop_payload.get("max_iterations", 1)),
        policy_profile=str(loop_payload.get("policy_profile") or "path_smoke"),
        seed=loop_payload.get("seed"),
        path_context=path_context,
        review_policy=review_policy,
        review_provider_mode="real_env" if real_llm else "fake_replay",
        review_model=llm_model,
        review_max_tokens=max_tokens if real_llm else None,
        review_max_retries=max_retries,
    )

    if real_llm:
        env = _require_llm_env()
        path_context["real_llm_smoke"] = {
            "provider_env": "LLM_ENDPOINT",
            "model": llm_model or get_default_model(),
            "real_provider_called_inside_agent_loop": True,
            "endpoint_host_recorded": env["LLM_ENDPOINT"].split("//")[-1].split("/")[0],
        }
    elif review_policy.enable_model_review and not cfg.review_replay_responses:
        cfg.review_replay_responses = {
            f"{StageId.SL_7_MODEL_REVIEW.value}:0": json.dumps(
                {"decision": "audit_only", "risk_level": "none", "findings": [], "blocking_findings": []},
                ensure_ascii=False,
            )
        }

    result = run_deterministic_ablation_loop(nl, cfg)
    if result.run_record_path is None:
        raise AssertionError("agent-loop did not write a run record")
    record = read_agent_loop_run_record(result.run_record_path)
    sl7 = _first_sl7_interaction(record) if review_policy.enable_model_review else {}
    stage_ids = _record_stage_ids(record)

    checks = {
        "schema_valid_agent_loop_run_record": True,
        "status_success_and_path_eligible": record.status == "success" and is_path_result_eligible(record),
        "path_context_contains_snapshot_and_case_id": bool(
            record.input_bundle.get("path_context", {}).get("source_snapshot")
            and record.input_bundle.get("path_context", {}).get("case_row", {}).get("case_id")
        ),
        "sl7_real_llm_interaction_recorded": bool(
            sl7
            and sl7.get("schema_validation_ok") is True
            and sl7.get("raw_output")
            and (not real_llm or record.input_bundle.get("path_context", {}).get("real_llm_smoke", {}).get("real_provider_called_inside_agent_loop") is True)
            and (not real_llm or sl7.get("provider") == "openai-compatible-env")
        ),
        "run_record_redaction_report_present_if_needed": isinstance(record.redaction_report, list),
        "has_path_stage_coverage": all(
            stage in stage_ids
            for stage in [
                StageId.SD_2_PARSE.value,
                StageId.SD_3_SEMANTIC.value,
                StageId.SD_4_DESIGN.value,
                StageId.SD_6_SIM.value,
                StageId.SL_7_MODEL_REVIEW.value,
                StageId.SC_13_TRACE_AUDIT.value,
            ]
        ),
    }
    if config.path == "path1":
        checks["ref_components_rowwise_metadata_available"] = bool(config.source_snapshot.get("ref_components_path"))
    if config.path == "path2":
        checks["path2_bucket_metadata_available"] = bool(row.get("bucket") or row.get("meta"))

    return HandoffSmokeResult(
        path=config.path,
        case_id=str(row.get("case_id") or config.case_selector.get("case_id") or ""),
        run_id=run_id,
        run_record_path=str(result.run_record_path),
        record_status=record.status,
        main_result_eligible=is_path_result_eligible(record),
        final_dsl_hash=str(record.final_artifacts.get("final_dsl_hash") or ""),
        stage_ids=stage_ids,
        llm_review_provider=str(sl7.get("provider") or ""),
        llm_review_model=str(sl7.get("model_id") or ""),
        llm_review_decision=str(sl7.get("parsed_output", {}).get("decision") or ""),
        llm_review_retry_count=int(sl7.get("retry_count") or 0),
        llm_review_attempt_statuses=[str(attempt.get("status") or "") for attempt in sl7.get("attempts", [])],
        checks=checks,
    )


def run_many(
    configs: Iterable[HandoffSmokeConfig],
    *,
    output_dir: str | Path,
    real_llm: bool = False,
    llm_model: str | None = None,
    max_tokens: int = 1000,
    max_retries: int = 2,
    cwd: str | Path | None = None,
) -> list[HandoffSmokeResult]:
    return [
        run_handoff_smoke(
            cfg,
            output_dir=output_dir,
            real_llm=real_llm,
            llm_model=llm_model,
            max_tokens=max_tokens,
            max_retries=max_retries,
            cwd=cwd,
        )
        for cfg in configs
    ]


def _default_config_paths() -> list[Path]:
    root = Path(__file__).resolve().parent / "configs"
    return [root / "path1_representative.json", root / "path2_representative.json"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run PR-3 Path1/Path2 agent-loop handoff smoke.")
    parser.add_argument("--config", action="append", type=Path, help="Config JSON path. Defaults to Path1+Path2 representative configs.")
    parser.add_argument("--out", type=Path, default=Path("runs/pr3_handoff_smoke"), help="Directory for *.agent_loop.json.gz outputs.")
    parser.add_argument("--summary", type=Path, default=None, help="Optional JSON summary output path.")
    parser.add_argument("--real-llm", action="store_true", help="Call real .env LLM once per config for SL-7, then replay that output into the agent loop.")
    parser.add_argument("--model", default=None, help="Optional LLM model override. Defaults to LLM_MODEL from env.")
    parser.add_argument("--max-tokens", type=int, default=1000, help="Max completion tokens for real SL-7 calls.")
    parser.add_argument("--max-retries", type=int, default=2, help="Bounded retry count for real LLM provider/schema noise.")
    args = parser.parse_args(argv)

    config_paths = args.config or _default_config_paths()
    configs = [load_handoff_config(path) for path in config_paths]
    results = run_many(configs, output_dir=args.out, real_llm=args.real_llm, llm_model=args.model, max_tokens=args.max_tokens, max_retries=args.max_retries)
    payload = [asdict(result) for result in results]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary is not None:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    failed = [result for result in results if not all(result.checks.values())]
    return 1 if failed else 0


if __name__ == "__main__":  # pragma: no cover - CLI exercised in PR-3 smoke tests
    raise SystemExit(main())
