"""Canonical staged agent-loop façade for project_1.

PR-A intentionally stops using the old A0-A4 implementation as the default
``method.loop.run_agent_loop`` entry.  The old implementation lives in
``method.legacy_loop`` and emits a deprecation warning when called.

This module currently provides the shared contract layer needed by PR-B1/B2/C:

- ``LoopConfig()`` resolves to ``experiment_default/full_staged_v1``.
- ``build_planned_stage_graph`` exposes the full SC/SL/SD stage graph with
  per-stage trace semantics.
- ``run_agent_loop`` is a canonical staged façade that records the resolved
  config and planned graph without dispatching to legacy/fake runtime.

The real full staged runtime is deliberately integrated in later PRs.  Until
then, this façade returns ``status='contract_only'`` and any run record it writes
is marked ``main_result_eligible=false`` so Path1/Path2 cannot accidentally treat
contract smoke output as experimental evidence.
"""

from __future__ import annotations

import hashlib
import platform
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Optional

from method.run_record import agent_loop_run_record_path, write_agent_loop_run_record
from method.schema import AgentLoopResult, AgentLoopRunRecord, LoopConfig, StageResultMeta
from method.stages.ids import ALL_STAGE_SPECS, StageId, StageStatus

RUN_RECORD_SCHEMA_VERSION = "pr-a.config-contract.v1"

_STAGE_SWITCH_BY_ID: dict[str, str | None] = {
    StageId.SC_0_START.value: None,
    StageId.SL_1_INITIAL_MODELING.value: "enable_initial_modeling",
    StageId.SD_2_PARSE.value: "enable_parse",
    StageId.SD_3_SEMANTIC.value: "enable_semantic",
    StageId.SD_4_DESIGN.value: "enable_design_inspect",
    StageId.SL_5_SCENARIO_GENERATION.value: "enable_scenario_generation",
    StageId.SD_5A_SCENARIO_COVERAGE.value: "enable_scenario_coverage",
    StageId.SC_5F_SCENARIO_FREEZE.value: "enable_scenario_generation",
    StageId.SD_6_SIM.value: "enable_simulation",
    StageId.SL_7_MODEL_REVIEW.value: "enable_model_review",
    StageId.SD_8_FIX_PLAN.value: "enable_fix_plan",
    StageId.SL_9_REPAIR.value: "enable_repair",
    StageId.SD_10_REPAIR_REVIEW.value: "enable_repair_review",
    StageId.SL_10B_DELTA_REVIEW.value: "enable_delta_review",
    StageId.SC_11_ACCEPT_CANDIDATE.value: "enable_repair",
    StageId.SC_12_EXIT.value: None,
    StageId.SC_13_TRACE_AUDIT.value: "enable_run_record",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def _environment_snapshot(cfg: LoopConfig) -> dict[str, Any]:
    return {
        "git_commit": _git_commit(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "provider_mode": cfg.llm_provider_mode,
        "llm_model_redacted": cfg.llm_model or "<env:LLM_MODEL>",
        "condition_hash": cfg.resolved_config()["condition_hash"],
    }


def _stage_enabled(stage_id: str, cfg: LoopConfig) -> bool:
    switch = _STAGE_SWITCH_BY_ID.get(stage_id)
    if switch is None:
        return True
    return bool(cfg.stage_switches.get(switch, False))


def build_planned_stage_graph(config: Optional[LoopConfig] = None) -> dict[str, Any]:
    """Return the canonical full staged graph planned for a resolved config.

    Each node has the same trace fields that later runtime stage records must
    expose: ``enabled``, ``ran``, ``status`` and ``skipped_reason``.  PR-A uses
    ``ran=false`` / ``status=skipped`` because this is a planning contract rather
    than the full runtime implementation.
    """
    cfg = config or LoopConfig()
    nodes: list[dict[str, Any]] = []
    for index, spec in enumerate(ALL_STAGE_SPECS):
        enabled = _stage_enabled(spec.stage_id, cfg)
        nodes.append(
            {
                "index": index,
                "stage_id": spec.stage_id,
                "stage_kind": spec.kind.value,
                "name": spec.name,
                "doc_filename": spec.doc_filename,
                "enabled": enabled,
                "ran": False,
                "status": StageStatus.SKIPPED.value,
                "skipped_reason": "planned_not_yet_run" if enabled else "disabled_by_condition",
            }
        )
    return {
        "schema_version": RUN_RECORD_SCHEMA_VERSION,
        "condition_id": cfg.condition_id,
        "condition_hash": cfg.resolved_config()["condition_hash"],
        "planned": [node["stage_id"] for node in nodes],
        "nodes": nodes,
    }


def _planned_stage_metas(graph: dict[str, Any]) -> list[StageResultMeta]:
    return [
        StageResultMeta(
            stage_id=node["stage_id"],
            stage_kind=node["stage_kind"],
            enabled=node["enabled"],
            ran=node["ran"],
            status=node["status"],
            ok=not node["enabled"],
            skipped_reason=node["skipped_reason"],
        )
        for node in graph["nodes"]
    ]


def _write_contract_run_record(*, nl: str, cfg: LoopConfig, run_id: str, graph: dict[str, Any], result: AgentLoopResult) -> str:
    stage_metas = _planned_stage_metas(graph)
    resolved_config = cfg.resolved_config()
    record = AgentLoopRunRecord(
        schema_version=RUN_RECORD_SCHEMA_VERSION,
        run_id=run_id,
        created_at=_utc_now(),
        status="contract_only",
        input_bundle={
            "nl_hash": _hash_text(nl),
            "nl_preview": nl[:240],
            "contract_only": True,
        },
        run_config={
            **resolved_config,
            "contract_only": True,
            "runtime_implementation": "pending_pr_b1_b2_c",
        },
        environment=_environment_snapshot(cfg),
        stage_graph={
            "planned": graph["planned"],
            "executed": [],
            "nodes": graph["nodes"],
        },
        stage_records=[asdict(meta) for meta in stage_metas],
        iteration_records=[],
        final_artifacts={
            "verdict": "contract_only_not_runtime",
            "main_result_eligible": False,
            "inclusion_reason": None,
            "exclusion_reason": "PR-A façade records only config/stage-graph contract; full runtime lands in PR-C.",
            "final_dsl": "",
        },
        logs=[
            {
                "ts": _utc_now(),
                "level": "info",
                "event": "canonical_staged_facade_contract_only",
                "message": "run_agent_loop did not call legacy/fake runtime in PR-A",
            }
        ],
    )
    path = write_agent_loop_run_record(record, agent_loop_run_record_path(cfg.output_dir, run_id))
    result.run_record_path = str(path)
    return str(path)


def run_agent_loop(
    nl: str,
    config: Optional[LoopConfig] = None,
    *,
    seed_dsl: Optional[str] = None,
) -> AgentLoopResult:
    """Canonical staged entry point.

    PR-A exposes the default experiment contract but does not run the full
    staged driver yet.  It also deliberately rejects ``seed_dsl`` in the default
    condition because snapshot/hot-start DSL is not allowed on the future
    Path1/Path2 main experiment path.
    """
    cfg = config or LoopConfig()
    if seed_dsl is not None and cfg.condition_id == "full_staged_v1":
        raise ValueError(
            "LoopConfig() default full_staged_v1 must not use seed_dsl/hot-start DSL; "
            "use method.legacy_loop for historical diagnostics or an explicit replay condition."
        )

    resolved_config = cfg.resolved_config()
    run_id = cfg.run_id or "pr-a-" + hashlib.sha256(f"{nl}\n{resolved_config['condition_hash']}".encode("utf-8")).hexdigest()[:12]
    graph = build_planned_stage_graph(cfg)
    result = AgentLoopResult(
        status="contract_only",
        llm_model=cfg.llm_model,
        run_record_id=run_id,
        error_message="PR-A canonical staged façade only; full runtime integration is deferred to PR-C.",
    )
    result.resolved_config = resolved_config
    result.planned_stage_graph = graph
    if cfg.write_run_record:
        _write_contract_run_record(nl=nl, cfg=cfg, run_id=run_id, graph=graph, result=result)
    return result
