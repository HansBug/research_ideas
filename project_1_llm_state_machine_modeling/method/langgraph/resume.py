"""LG-M1-D3 / LG-F1 durable checkpoint-resume implementation.

The historical facade ``method.langgraph_runtime`` still exposes compatibility
wrappers, but experiments and new code import this implementation module so
``method/experiments`` no longer reverse-imports the facade.
"""

from __future__ import annotations

from method.langgraph.core import *  # noqa: F403 - LG-F1 shares the default runtime implementation helpers.

def _lg_f1_actual_interrupt_node(interrupt_after: str) -> str:
    """Map LG-F1 human/stage breakpoints onto the parent graph checkpoint boundary.

    LG-F1 deliberately supports controlled node-boundary resume on the parent
    graph.  Nested repair/validation subgraphs still run with ``checkpointer=False``
    because they carry live Python objects; therefore a request such as
    ``repair_sl10_review`` is recorded as requested evidence but executed at the
    nearest durable parent checkpoint, ``repair_path``.
    """

    requested = str(interrupt_after or "").strip()
    if requested in {
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "repair_path",
        "repair_decision",
        "waiver_continue",
        "sc12_budget_exhausted",
        "sc13_trace_audit",
    }:
        return requested
    repair_aliases = {
        "SD-8",
        "SD_8",
        StageId.SD_8_FIX_PLAN.value,
        "SL-9",
        "SL_9",
        StageId.SL_9_REPAIR.value,
        "SL-10",
        "SL_10",
        StageId.SL_10_REPAIR_REVIEW.value,
        "SC-11",
        "SC_11",
        StageId.SC_11_ACCEPT_CANDIDATE.value,
        "repair_enter",
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
        "repair_finalize",
    }
    if requested in repair_aliases or requested.startswith("repair_"):
        return "repair_path"
    validation_aliases = {
        StageId.SD_2_PARSE.value,
        StageId.SD_3_SEMANTIC.value,
        StageId.SD_4_DESIGN.value,
        StageId.SL_5_SCENARIO_GENERATION.value,
        StageId.SD_5A_SCENARIO_COVERAGE.value,
        StageId.SD_6_SIM.value,
        StageId.SL_7_MODEL_REVIEW.value,
    }
    if requested in validation_aliases or requested.startswith("validation_"):
        return "validation_pass"
    raise ValueError(f"unsupported LG-F1 interrupt_after breakpoint: {interrupt_after!r}")


def _lg_f1_path_hash(path: str | Path) -> str:
    return _hash_text(str(Path(path).expanduser().resolve()))


def _lg_f1_checkpoint_id_hash(checkpoint: Any) -> str:
    config = getattr(checkpoint, "config", {}) or {}
    configurable = config.get("configurable", {}) if isinstance(config, dict) else {}
    checkpoint_id = str(configurable.get("checkpoint_id") or "")
    if not checkpoint_id:
        return "sha256:<missing-checkpoint-id>"
    return _hash_text(checkpoint_id)


def _lg_f1_graph_config(
    *,
    config: LoopConfig,
    registry: dict[str, Any],
    planned: dict[str, Any],
    resolved: dict[str, Any],
    checkpoint_path: str | Path,
    requested_interrupt_after: str,
    actual_interrupt_after: str,
    operator_stream_enabled: bool,
    toolnode_wrapper_enabled: bool,
) -> dict[str, Any]:
    return {
        "registry": registry,
        "planned_stage_graph": planned,
        "resolved_config": resolved,
        "condition_hash": resolved.get("condition_hash"),
        "condition_id": config.condition_id,
        "max_iterations": config.max_iterations,
        "scenario_max_retries": config.scenario_max_retries,
        "min_sl10_rework_attempts": int(config.budget_policy.get("min_sl10_rework_attempts", 1)) if isinstance(config.budget_policy, dict) else 1,
        "policy_profile": config.policy_profile,
        "llm_provider_mode": config.llm_provider_mode,
        "runtime_backend": "langgraph_lg_f1_resume_experiment",
        "checkpoint_backend": "sqlite",
        "checkpoint_backend_type": "SqliteSaver",
        "checkpoint_serde": "pickle",
        "checkpoint_path_hash": _lg_f1_path_hash(checkpoint_path),
        "runtime_schema_version": GRAPH_RUNTIME_SCHEMA_VERSION,
        "node_edge_schema_version": NODE_EDGE_SCHEMA_VERSION,
        "lg_d1_operator_stream_enabled": bool(operator_stream_enabled),
        "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
        "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "lg_f1_schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "lg_f1_requested_interrupt_after": requested_interrupt_after,
        "lg_f1_actual_interrupt_after": actual_interrupt_after,
        "lg_f1_scope": "controlled_parent_node_boundary_resume",
    }


def _lg_f1_runtime_config(
    *,
    nl: str,
    config: LoopConfig,
    planned: dict[str, Any],
    resolved: dict[str, Any],
    registry: dict[str, Any],
    consistency: dict[str, Any],
    compat: dict[str, Any],
    graph_config_hash: str,
    initial_dsl: str,
    run_id: str,
    checkpoint_path: str | Path,
    requested_interrupt_after: str,
    actual_interrupt_after: str,
    resumed_from_checkpoint: bool,
    resume_checkpoint_id_hash: str | None = None,
    resume_diff_report_path: str | None = None,
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
) -> FullStagedRuntimeConfig:
    checkpoint_metadata = {
        "checkpoint_backend": "sqlite",
        "checkpoint_backend_type": "SqliteSaver",
        "checkpoint_serde": "pickle",
        "checkpoint_serde_mode": _LG_C1_CHECKPOINT_SERDE_MODE,
        "checkpoint_path_hash": _lg_f1_path_hash(checkpoint_path),
        "checkpoint_backend_status": "enabled",
        "checkpoint_path": str(checkpoint_path),
        "resumed_from_checkpoint": bool(resumed_from_checkpoint),
        "resume_checkpoint_id_hash": resume_checkpoint_id_hash,
        "real_agent_loop_resume_supported": True,
        "real_agent_loop_resume_support_level": "controlled_parent_node_boundary_only",
        "real_agent_loop_resume_scope": "controlled_parent_node_boundary_resume; nested subgraphs are not mid-node crash checkpoints",
        "real_agent_loop_arbitrary_mid_node_resume_supported": False,
        "real_agent_loop_nested_subgraph_resume_supported": False,
        "real_agent_loop_json_checkpoint_supported": False,
        "resume_run_main_result_eligible": False,
        "resume_cli_entrypoint": "python -m project_1_llm_state_machine_modeling.method.experiments.checkpoint_resume",
        "resume_cli_workdir": "repo_root",
        "resume_cli_requires_pythonpath": False,
        "resume_cli_pythonpath_entrypoint": "PYTHONPATH=project_1_llm_state_machine_modeling python -m method.experiments.checkpoint_resume",
        "resume_cli_legacy_entrypoint": "PYTHONPATH=project_1_llm_state_machine_modeling python -m method.pr_lg_f1_resume_experiment",
        "resume_cli_legacy_package_entrypoint": "python -m project_1_llm_state_machine_modeling.method.pr_lg_f1_resume_experiment",
        "resume_diff_report_path": resume_diff_report_path,
        "resume_diff_report_schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "lg_f1_requested_interrupt_after": requested_interrupt_after,
        "lg_f1_actual_interrupt_after": actual_interrupt_after,
        "lg_f1_mid_node_crash_supported": False,
        "lg_f1_transient_store_durable": False,
        "lg_f1_scope_note": (
            "SQLite persists the parent LangGraph checkpoint.  LG-F1 does not claim "
            "arbitrary mid-node crash recovery because nested subgraphs and transient "
            "Store objects are still live-object boundaries."
        ),
    }
    metadata = _graph_runtime_metadata(
        registry=registry,
        compat=compat,
        graph_config_hash=graph_config_hash,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        checkpoint_metadata=checkpoint_metadata,
    )
    initial_lg_d1_stream_metadata = lg_d1_llm_stream_runtime_metadata(real_llm_provider_api=config.llm_provider_mode == "real_env")
    return FullStagedRuntimeConfig(
        initial_dsl=initial_dsl,
        run_id=run_id,
        output_dir=config.output_dir,
        max_iterations=config.max_iterations,
        scenario_max_retries=config.scenario_max_retries,
        min_sl10_rework_attempts=int(config.budget_policy.get("min_sl10_rework_attempts", 1)) if isinstance(config.budget_policy, dict) else 1,
        policy_profile=config.policy_profile,
        write_run_record=config.write_run_record,
        adapter_mode=config.llm_provider_mode,
        # LG-F1 resume runs are evidence-only and must never become Path1/Path2 main results.
        allow_main_result_eligible=False,
        resolved_loop_config=resolved,
        run_config_extra={
            "runtime_implementation": "method.langgraph_runtime.run_lg_f1_resume_experiment",
            "langgraph_called_from_loop": False,
            "canonical_runtime_backend": "langgraph",
            "graph_node_registry": registry,
            "graph_registry_consistency": consistency,
            "graph_config_hash": graph_config_hash,
            "instrumentation_layer": "langgraph",
            "lg_d1_operator_log_enabled": bool(operator_stream_enabled),
            "lg_d1_instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
            "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
            "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "lg_e3_toolnode_wrapper_registry": build_lg_e3_toolnode_wrapper_registry(),
            "lg_e3_toolnode_wrapper_llm_tool_choice_exposed": False,
            "llm_stream_required": initial_lg_d1_stream_metadata["llm_stream_required"],
            "stage_semantics_module": "method.staged_runtime",
            "lg_f1_resume_experiment": True,
            "resume_run_main_result_eligible": False,
            "resumed_from_checkpoint": bool(resumed_from_checkpoint),
            "resume_checkpoint_id_hash": resume_checkpoint_id_hash,
            "checkpoint_backend": "sqlite",
            "checkpoint_backend_type": "SqliteSaver",
            "checkpoint_path_hash": _lg_f1_path_hash(checkpoint_path),
            "resume_diff_report_path": resume_diff_report_path,
            "resume_diff_report_schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        },
        environment_extra={
            **metadata,
            "runner": "method.langgraph_runtime.run_lg_f1_resume_experiment",
            "stage_semantics_module": "method.staged_runtime",
            "loop_entrypoint": "method.langgraph_runtime.run_lg_f1_resume_experiment",
            "record_schema_version": "pr-c.default-full-staged-runtime.v1",
            "lg_d1_operator_log_enabled": bool(operator_stream_enabled),
            "lg_d1_instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
            "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
            "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "lg_e3_toolnode_wrapper_registry_hash": _hash_payload(build_lg_e3_toolnode_wrapper_registry()),
            "lg_e3_toolnode_wrapper_llm_tool_choice_exposed": False,
            **initial_lg_d1_stream_metadata,
        },
        real_llm_provider_api=config.llm_provider_mode == "real_env",
        provider_config_read=_provider_config_read(config),
        provider_model_redacted=_provider_model_redacted(config, provider),
        default_loop_config_entry_integrated=False,
    )


def _lg_f1_prepare_runtime(
    *,
    config: LoopConfig,
    checkpoint_path: str | Path,
    requested_interrupt_after: str,
    operator_stream_enabled: bool,
    toolnode_wrapper_enabled: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], str, str]:
    config.validate_for_run()
    registry = build_langgraph_node_registry()
    planned = _planned_stage_graph_from_config(config)
    consistency = graph_registry_consistency(planned, registry)
    if not consistency["ok"]:
        raise ValueError(f"LangGraph registry does not cover planned stage graph: {consistency}")
    compat = langgraph_compat_smoke()
    if not compat.get("ok"):
        raise RuntimeError(f"LangGraph compatibility smoke failed: {compat}")
    resolved = config.resolved_config()
    actual_interrupt_after = _lg_f1_actual_interrupt_node(requested_interrupt_after)
    graph_config = _lg_f1_graph_config(
        config=config,
        registry=registry,
        planned=planned,
        resolved=resolved,
        checkpoint_path=checkpoint_path,
        requested_interrupt_after=requested_interrupt_after,
        actual_interrupt_after=actual_interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
    )
    return registry, planned, consistency, compat, resolved, _hash_payload(graph_config), actual_interrupt_after


def _lg_f1_sqlite_saver(checkpoint_path: str | Path) -> tuple[Any, sqlite3.Connection]:
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
    except Exception as exc:  # pragma: no cover - depends on optional package installation.
        raise RuntimeError(
            "LG-F1 durable resume requires langgraph-checkpoint-sqlite; "
            "install langgraph-checkpoint-sqlite and do not silently fall back to memory"
        ) from exc

    path = Path(checkpoint_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    saver = SqliteSaver(conn, serde=_PickleCheckpointSerde())
    saver.setup()
    return saver, conn


def _lg_f1_state_snapshot(state: dict[str, Any] | None) -> dict[str, Any]:
    state = dict(state or {})
    runtime_state = state.get("runtime_state")
    if isinstance(runtime_state, _RunState):
        return {
            "stage_records": _jsonable(runtime_state.stage_records),
            "stage_ids": _stage_ids(runtime_state.stage_records),
            "fix_log": _jsonable(runtime_state.fix_log),
            "llm_interactions": _jsonable(runtime_state.llm_interactions),
            "scenario_history": _jsonable(runtime_state.scenario_history),
            "repair_history": _jsonable(runtime_state.repair_history),
            "final_dsl_hash": _hash_text(runtime_state.current_dsl),
            "verdict": runtime_state.final_verdict,
            "result_status": runtime_state.result_status,
        }
    return {
        "stage_records": [],
        "stage_ids": [],
        "fix_log": [],
        "llm_interactions": [],
        "scenario_history": [],
        "repair_history": [],
        "final_dsl_hash": None,
        "verdict": None,
        "result_status": None,
    }


def _lg_f1_record_snapshot(record: Any) -> dict[str, Any]:
    return {
        "stage_records": _jsonable(record.stage_records),
        "stage_ids": [str(item.get("stage_id") if isinstance(item, dict) else getattr(item, "stage_id", "")) for item in record.stage_records],
        "fix_log": _jsonable(record.fix_log),
        "llm_interactions": _jsonable(record.llm_interactions),
        "scenario_history": _jsonable(record.scenario_history),
        "repair_history": _jsonable(record.repair_history),
        "final_dsl_hash": record.final_artifacts.get("final_dsl_hash"),
        "verdict": record.final_artifacts.get("verdict"),
        "result_status": record.final_artifacts.get("agent_loop_result_status"),
    }


def _lg_f1_prefix_preserved(prefix: list[Any], full: list[Any]) -> bool:
    return list(full[: len(prefix)]) == list(prefix)


def _lg_f1_append_only_audit(prefix: dict[str, Any], resumed: dict[str, Any]) -> dict[str, Any]:
    fix_log = list(resumed.get("fix_log") or [])
    fix_ids = [
        str(item.get("entry_id") or item.get("fix_log_entry_id") or item.get("candidate_dsl_hash") or _hash_payload(item))
        for item in fix_log
        if isinstance(item, dict)
    ]
    return {
        "stage_records_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("stage_records") or [], resumed.get("stage_records") or []),
        "fix_log_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("fix_log") or [], resumed.get("fix_log") or []),
        "llm_interactions_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("llm_interactions") or [], resumed.get("llm_interactions") or []),
        "scenario_history_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("scenario_history") or [], resumed.get("scenario_history") or []),
        "repair_history_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("repair_history") or [], resumed.get("repair_history") or []),
        "duplicate_fix_log_entry_detected": len(fix_ids) != len(set(fix_ids)),
    }


def _lg_f1_stage_replay_audit(
    *,
    prefix: dict[str, Any],
    resumed: dict[str, Any],
    actual_interrupt_after: str,
    next_nodes_after_interrupt: list[str],
) -> dict[str, Any]:
    """Explain repeated stage ids after resume instead of treating all repeats as replay bugs.

    LG-F1 may intentionally resume at a parent boundary after the repair
    subgraph has produced SD-8/SL-9/SL-10/SC-11 evidence.  The next parent node
    is then ``repair_decision`` which routes to a full post-repair validation
    pass.  That means resumed records are expected to contain a prefix ending
    at SC-11 followed by SD-2/SD-3/.../SC-13.  This helper makes that route
    machine-readable so reviewers can distinguish expected post-repair
    revalidation from accidental replay / duplicate ledger pollution.
    """

    prefix_ids = [str(item) for item in (prefix.get("stage_ids") or [])]
    resumed_ids = [str(item) for item in (resumed.get("stage_ids") or [])]
    prefix_preserved = _lg_f1_prefix_preserved(prefix_ids, resumed_ids)
    suffix = resumed_ids[len(prefix_ids) :] if prefix_preserved else resumed_ids
    repeated_after_resume = [stage_id for stage_id in suffix if stage_id in set(prefix_ids)]
    post_repair_full_revalidation_expected = (
        bool(prefix_preserved)
        and actual_interrupt_after == "repair_path"
        and "repair_decision" in set(next_nodes_after_interrupt)
        and suffix[:3] == ["SD-2", "SD-3", "SD-4"]
    )
    unexpected_stage_replay_detected = bool(repeated_after_resume) and not post_repair_full_revalidation_expected
    explanation = (
        "Expected: interrupt_after mapped to parent node repair_path; after resume the pending repair_decision "
        "routes into a full post-repair validation pass, so SD-2/SD-3/... appear after the preserved repair prefix."
        if post_repair_full_revalidation_expected
        else (
            "No repeated stage ids after the preserved prefix."
            if not repeated_after_resume
            else "Repeated stage ids after resume are not explained by a known LG-F1 parent-boundary route."
        )
    )
    return {
        "schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "prefix_stage_ids": prefix_ids,
        "resumed_stage_ids": resumed_ids,
        "suffix_after_resume": suffix,
        "repeated_stage_ids_after_resume": repeated_after_resume,
        "prefix_preserved": prefix_preserved,
        "post_repair_full_revalidation_expected": post_repair_full_revalidation_expected,
        "unexpected_stage_replay_detected": unexpected_stage_replay_detected,
        "actual_interrupt_after": actual_interrupt_after,
        "next_nodes_after_interrupt": list(next_nodes_after_interrupt),
        "explanation": explanation,
    }


def _lg_f1_compare_hash(value: Any) -> str:
    """Hash a comparison payload after dropping known run-local bookkeeping."""

    def scrub(item: Any) -> Any:
        if isinstance(item, dict):
            cleaned: dict[str, Any] = {}
            for key, value in item.items():
                key_s = str(key)
                lowered = key_s.lower()
                if any(fragment in lowered for fragment in ("run_id", "timestamp", "created_at", "updated_at", "path", "checkpoint_id")):
                    cleaned[key_s] = "<allowed-run-local-diff>"
                else:
                    cleaned[key_s] = scrub(value)
            return cleaned
        if isinstance(item, list):
            return [scrub(value) for value in item]
        return item

    return _hash_payload(scrub(value))


def _lg_f1_comparison_checks(
    prefix: dict[str, Any],
    resumed: dict[str, Any],
    uninterrupted: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    baseline_available = uninterrupted is not None
    comparison_basis = "independent_uninterrupted_baseline" if baseline_available else "no_independent_baseline"
    comparison_method = "independent_uninterrupted_baseline" if baseline_available else "not_available"
    comparison_target = "uninterrupted_vs_resumed" if baseline_available else "baseline_unavailable"
    for field in ("stage_ids", "fix_log", "llm_interactions", "scenario_history", "repair_history", "final_dsl_hash", "verdict", "result_status"):
        prefix_value = prefix.get(field)
        resumed_value = resumed.get(field)
        resumed_hash = _lg_f1_compare_hash(resumed_value)
        uninterrupted_hash = _lg_f1_compare_hash(uninterrupted.get(field)) if baseline_available else None
        verdict = (
            "consistent"
            if baseline_available and uninterrupted_hash == resumed_hash
            else ("unacceptable_diff" if baseline_available else "not_applicable")
        )
        note = (
            "LG-F1 compares an independent uninterrupted baseline against the resumed final evidence; "
            "prefix hash is recorded separately for append-only resume auditing."
            if baseline_available
            else (
                "No independent uninterrupted baseline was provided; this check only records resumed/prefix hashes "
                "and must not be cited as independent baseline equivalence."
            )
        )
        checks.append(
            {
                "field": field,
                "uninterrupted_value_hash": uninterrupted_hash,
                "resumed_value_hash": resumed_hash,
                "prefix_value_hash": _lg_f1_compare_hash(prefix_value),
                "verdict": verdict,
                "comparison_method": comparison_method,
                "comparison_basis": comparison_basis,
                "comparison_target": comparison_target,
                "baseline_available": baseline_available,
                "uninterrupted_baseline_available": baseline_available,
                "note": note,
            }
        )
    return checks


def _lg_f1_finalize_result(
    *,
    result: AgentLoopResult,
    state: _GraphLoopState,
    operator_events: list[dict[str, Any]],
    graph_stream_status: str,
    operator_stream_enabled: bool,
    toolnode_wrapper_enabled: bool,
    resolved: dict[str, Any],
    planned: dict[str, Any],
) -> None:
    graph_trace = list(state.get("graph_trace", []) or [])
    _augment_run_record_with_graph_trace(result, graph_trace)
    toolnode_events = list(state.get("toolnode_wrapper_events", []) or [])
    _augment_run_record_with_lg_e3_toolnode_trace(
        result,
        events=toolnode_events,
        enabled=bool(toolnode_wrapper_enabled),
    )
    lg_e2_events = list(state.get("lg_e2_send_parallel_events", []) or [])
    _augment_run_record_with_lg_e2_send_parallel_trace(
        result,
        events=lg_e2_events,
        enabled=True,
    )
    operator_events = _merge_operator_events(operator_events, state.get("operator_events"))
    _augment_run_record_with_lg_d1_operator_log(
        result,
        operator_events=operator_events,
        graph_stream_status=graph_stream_status,
        operator_stream_enabled=bool(operator_stream_enabled),
    )
    _refresh_graph_state_readiness_after_operator_log(result, state)
    result.resolved_config = resolved
    result.planned_stage_graph = planned


def _lg_f1_patch_record_with_report(record_path: str | Path, report: dict[str, Any]) -> None:
    record = read_agent_loop_run_record(record_path)
    record.environment.update(
        {
            "checkpoint_backend": "sqlite",
            "checkpoint_backend_type": "SqliteSaver",
            "checkpoint_path_hash": report["checkpoint_path_hash"],
            "resumed_from_checkpoint": True,
            "resume_checkpoint_id_hash": report["resume"]["checkpoint_id_hash"],
            "real_agent_loop_resume_supported": True,
            "real_agent_loop_resume_support_level": report["real_agent_loop_resume_support_level"],
            "real_agent_loop_resume_scope": report["real_agent_loop_resume_scope"],
            "real_agent_loop_arbitrary_mid_node_resume_supported": False,
            "real_agent_loop_nested_subgraph_resume_supported": False,
            "resume_run_main_result_eligible": False,
            "resume_diff_report_path": report["resume_diff_report_path"],
            "resume_diff_report_schema_version": report["schema_version"],
            "baseline_comparison_method": report["baseline_comparison_method"],
            "baseline_comparison_verdict": report["baseline_comparison_verdict"],
            "baseline_comparison_note": report["baseline_comparison_note"],
            "verdict_scope": report["verdict_scope"],
            "lg_f1_mid_node_crash_supported": False,
            "lg_f1_stage_replay_explanation": report["stage_replay_audit"]["explanation"],
        }
    )
    record.run_config.update(
        {
            "lg_f1_resume_experiment": True,
            "checkpoint_backend": "sqlite",
            "checkpoint_backend_type": "SqliteSaver",
            "checkpoint_path_hash": report["checkpoint_path_hash"],
            "resumed_from_checkpoint": True,
            "resume_checkpoint_id_hash": report["resume"]["checkpoint_id_hash"],
            "resume_run_main_result_eligible": False,
            "resume_diff_report_path": report["resume_diff_report_path"],
            "resume_diff_report_schema_version": report["schema_version"],
            "baseline_comparison_method": report["baseline_comparison_method"],
            "baseline_comparison_verdict": report["baseline_comparison_verdict"],
            "verdict_scope": report["verdict_scope"],
        }
    )
    record.final_artifacts["main_result_eligible"] = False
    record.final_artifacts["main_result_eligibility_reason"] = "LG-F1 resume run is evidence-only; resume artifacts are excluded from main-result statistics"
    record.final_artifacts["resume_run_main_result_eligible"] = False
    record.final_artifacts["resume_diff_report_path"] = report["resume_diff_report_path"]
    record.final_artifacts["lg_f1_resume_verdict"] = report["verdict"]
    record.final_artifacts["lg_f1_baseline_comparison_method"] = report["baseline_comparison_method"]
    record.final_artifacts["lg_f1_baseline_comparison_verdict"] = report["baseline_comparison_verdict"]
    record.final_artifacts["lg_f1_verdict_scope"] = report["verdict_scope"]
    record.logs.append(
        {
            "event": "lg_f1_resume_reconciliation",
            "schema_version": report["schema_version"],
            "resume_diff_report_path": report["resume_diff_report_path"],
            "verdict": report["verdict"],
            "baseline_comparison_method": report["baseline_comparison_method"],
            "baseline_comparison_verdict": report["baseline_comparison_verdict"],
            "verdict_scope": report["verdict_scope"],
            "main_result_eligible": False,
        }
    )
    write_agent_loop_run_record(record, record_path)


def resume_lg_f1_from_checkpoint(
    *,
    checkpoint_path: str | Path,
    thread_id: str,
    expected_graph_config_hash: str,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    nl: str = "LG-F1 resume from durable checkpoint.",
    initial_dsl: str = "",
    interrupt_after: str = "repair_path",
    checkpoint_id_hash: str | None = None,
    resume_diff_report_path: str | None = None,
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
) -> dict[str, Any]:
    """Resume a controlled LG-F1 parent-graph checkpoint and fail loud on mismatch."""

    path = Path(checkpoint_path)
    if not path.exists():
        raise FileNotFoundError(f"LG-F1 checkpoint missing: {path}")
    registry, planned, consistency, compat, resolved, graph_config_hash, actual_interrupt_after = _lg_f1_prepare_runtime(
        config=config,
        checkpoint_path=path,
        requested_interrupt_after=interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
    )
    if expected_graph_config_hash and expected_graph_config_hash != graph_config_hash:
        raise ValueError(
            f"LG-F1 graph_config_hash mismatch: expected {expected_graph_config_hash}, actual {graph_config_hash}; "
            "refusing to resume from an incompatible checkpoint"
        )
    saver, conn = _lg_f1_sqlite_saver(path)
    try:
        runtime_cfg = _lg_f1_runtime_config(
            nl=nl,
            config=config,
            planned=planned,
            resolved=resolved,
            registry=registry,
            consistency=consistency,
            compat=compat,
            graph_config_hash=graph_config_hash,
            initial_dsl=initial_dsl,
            run_id=thread_id,
            checkpoint_path=path,
            requested_interrupt_after=interrupt_after,
            actual_interrupt_after=actual_interrupt_after,
            resumed_from_checkpoint=True,
            resume_checkpoint_id_hash=checkpoint_id_hash,
            resume_diff_report_path=resume_diff_report_path,
            operator_stream_enabled=operator_stream_enabled,
            toolnode_wrapper_enabled=toolnode_wrapper_enabled,
            provider=provider,
        )
        app = _build_graph(runtime_cfg=runtime_cfg, adapters=adapters, checkpointer=saver)
        checkpoint = app.get_state({"configurable": {"thread_id": thread_id}})
        if checkpoint is None or not getattr(checkpoint, "values", None):
            raise RuntimeError(f"LG-F1 checkpoint not found for thread_id={thread_id!r}; refusing to rerun from scratch")
        if not getattr(checkpoint, "next", None):
            raise RuntimeError(f"LG-F1 checkpoint for thread_id={thread_id!r} has no pending next node; refusing ambiguous resume")
        actual_checkpoint_hash = _lg_f1_checkpoint_id_hash(checkpoint)
        if checkpoint_id_hash and checkpoint_id_hash != actual_checkpoint_hash:
            raise ValueError(
                f"LG-F1 checkpoint id mismatch for thread_id={thread_id!r}: expected {checkpoint_id_hash}, actual {actual_checkpoint_hash}"
            )
        state = app.invoke(None, config=checkpoint.config)
        if not isinstance(state, dict) or "runtime_result" not in state:
            raise RuntimeError("LG-F1 resume did not reach SC-13 runtime_result; refusing to report success")
        result = state.get("runtime_result")
        if not isinstance(result, AgentLoopResult):
            raise TypeError("LG-F1 resumed graph did not return an AgentLoopResult")
        _lg_f1_finalize_result(
            result=result,
            state=state,
            operator_events=[],
            graph_stream_status="disabled",
            operator_stream_enabled=operator_stream_enabled,
            toolnode_wrapper_enabled=toolnode_wrapper_enabled,
            resolved=resolved,
            planned=planned,
        )
        return {
            "state": state,
            "result": result,
            "record_path": result.run_record_path,
            "checkpoint_id_hash": actual_checkpoint_hash,
            "graph_config_hash": graph_config_hash,
        }
    finally:
        conn.close()


def run_lg_f1_resume_experiment(
    nl: str,
    *,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    initial_dsl: str = "",
    checkpoint_path: str | Path,
    interrupt_after: str = "repair_path",
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
    uninterrupted_adapters: FullStagedRuntimeAdapters | None = None,
    uninterrupted_provider: ChatProvider | None = None,
) -> dict[str, Any]:
    """Run a deterministic LG-F1 durable checkpoint/resume reconciliation experiment.

    The helper is intentionally evidence-only: it writes ``resume_diff_report.json``
    and patches the resumed run record so ``main_result_eligible`` remains false.
    """

    path = Path(checkpoint_path)
    run_id = config.run_id or f"lg-f1-{hashlib.sha256(nl.encode('utf-8')).hexdigest()[:12]}"
    uninterrupted_snapshot: dict[str, Any] | None = None
    uninterrupted_record_path: str | None = None
    uninterrupted_run_id = f"{run_id}-uninterrupted"
    if uninterrupted_adapters is not None:
        baseline_cfg = replace(config, run_id=uninterrupted_run_id)
        baseline_result = run_full_staged_langgraph_runtime(
            nl,
            config=baseline_cfg,
            adapters=uninterrupted_adapters,
            initial_dsl=initial_dsl,
            run_id=uninterrupted_run_id,
            provider=uninterrupted_provider if uninterrupted_provider is not None else provider,
            called_from_loop=False,
            operator_stream_enabled=bool(operator_stream_enabled),
            toolnode_wrapper_enabled=bool(toolnode_wrapper_enabled),
        )
        if not baseline_result.run_record_path:
            raise RuntimeError("LG-F1 uninterrupted baseline did not write an AgentLoopRunRecord")
        uninterrupted_record_path = str(baseline_result.run_record_path)
        uninterrupted_snapshot = _lg_f1_record_snapshot(read_agent_loop_run_record(baseline_result.run_record_path))
    registry, planned, consistency, compat, resolved, graph_config_hash, actual_interrupt_after = _lg_f1_prepare_runtime(
        config=config,
        checkpoint_path=path,
        requested_interrupt_after=interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
    )
    report_path = path.parent / "resume_diff_report.json"
    saver, conn = _lg_f1_sqlite_saver(path)
    try:
        runtime_cfg = _lg_f1_runtime_config(
            nl=nl,
            config=config,
            planned=planned,
            resolved=resolved,
            registry=registry,
            consistency=consistency,
            compat=compat,
            graph_config_hash=graph_config_hash,
            initial_dsl=initial_dsl,
            run_id=run_id,
            checkpoint_path=path,
            requested_interrupt_after=interrupt_after,
            actual_interrupt_after=actual_interrupt_after,
            resumed_from_checkpoint=False,
            resume_checkpoint_id_hash=None,
            resume_diff_report_path=str(report_path),
            operator_stream_enabled=operator_stream_enabled,
            toolnode_wrapper_enabled=toolnode_wrapper_enabled,
            provider=provider,
        )
        app = _build_graph(runtime_cfg=runtime_cfg, adapters=adapters, checkpointer=saver)
        initial_state: _GraphLoopState = {
            "nl": nl,
            "graph_trace": [],
            "operator_events": [],
            "operator_stream_enabled": bool(operator_stream_enabled),
            "toolnode_wrapper_events": [],
            "stage_record_events": [],
            "llm_interaction_events": [],
            "fix_log_events": [],
            "scenario_history_events": [],
            "repair_history_events": [],
            "toolnode_wrapper_enabled": bool(toolnode_wrapper_enabled),
            "run_id": run_id,
        }
        prefix_state = app.invoke(
            initial_state,
            config={"configurable": {"thread_id": run_id}},
            interrupt_after=[actual_interrupt_after],
        )
        checkpoint = app.get_state({"configurable": {"thread_id": run_id}})
        if checkpoint is None or not getattr(checkpoint, "values", None) or not getattr(checkpoint, "next", None):
            raise RuntimeError(
                f"LG-F1 interrupt_after={actual_interrupt_after!r} did not leave a resumable checkpoint; "
                "refusing to report durable resume success"
            )
        checkpoint_id_hash = _lg_f1_checkpoint_id_hash(checkpoint)
        prefix_snapshot = _lg_f1_state_snapshot(prefix_state if isinstance(prefix_state, dict) else getattr(checkpoint, "values", {}))
    finally:
        conn.close()

    resumed = resume_lg_f1_from_checkpoint(
        checkpoint_path=path,
        thread_id=run_id,
        expected_graph_config_hash=graph_config_hash,
        config=config,
        adapters=adapters,
        nl=nl,
        initial_dsl=initial_dsl,
        interrupt_after=interrupt_after,
        checkpoint_id_hash=checkpoint_id_hash,
        resume_diff_report_path=str(report_path),
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        provider=provider,
    )
    record_path = resumed["record_path"]
    if not record_path:
        raise RuntimeError("LG-F1 resumed run did not write an AgentLoopRunRecord")
    record = read_agent_loop_run_record(record_path)
    resumed_snapshot = _lg_f1_record_snapshot(record)
    next_nodes_after_interrupt = list(getattr(checkpoint, "next", ()) or [])
    append_only_audit = _lg_f1_append_only_audit(prefix_snapshot, resumed_snapshot)
    stage_replay_audit = _lg_f1_stage_replay_audit(
        prefix=prefix_snapshot,
        resumed=resumed_snapshot,
        actual_interrupt_after=actual_interrupt_after,
        next_nodes_after_interrupt=next_nodes_after_interrupt,
    )
    comparison_checks = _lg_f1_comparison_checks(prefix_snapshot, resumed_snapshot, uninterrupted_snapshot)
    uninterrupted_baseline_available = uninterrupted_snapshot is not None
    baseline_comparison_method = (
        "independent_uninterrupted_baseline" if uninterrupted_baseline_available else "not_available"
    )
    baseline_comparison_verdict = (
        "unacceptable_diff"
        if any(item.get("verdict") == "unacceptable_diff" for item in comparison_checks)
        else ("consistent" if uninterrupted_baseline_available else "not_applicable")
    )
    unacceptable = [
        key for key, value in append_only_audit.items() if key != "duplicate_fix_log_entry_detected" and value is not True
    ]
    if append_only_audit["duplicate_fix_log_entry_detected"]:
        unacceptable.append("duplicate_fix_log_entry_detected")
    if stage_replay_audit["unexpected_stage_replay_detected"]:
        unacceptable.append("unexpected_stage_replay_detected")
    unacceptable.extend(
        f"comparison:{item['field']}" for item in comparison_checks if item.get("verdict") == "unacceptable_diff"
    )
    verdict = "consistent" if not unacceptable else "unacceptable_diff"
    report: dict[str, Any] = {
        "schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "resume_experiment_id": run_id,
        "thread_id": run_id,
        "checkpoint_backend": "sqlite",
        "checkpoint_backend_type": "SqliteSaver",
        "checkpoint_path": str(path),
        "checkpoint_path_hash": _lg_f1_path_hash(path),
        "checkpoint_backend_status": "enabled",
        "graph_config_hash": graph_config_hash,
        "uninterrupted_run_id": uninterrupted_run_id if uninterrupted_baseline_available else None,
        "uninterrupted_run_record_path": uninterrupted_record_path,
        "interrupted_run_id": run_id,
        "resumed_run_id": run_id,
        "artifact_hash_scope": "academic_evidence_snapshot",
        "uninterrupted_artifact_hash": _hash_payload(uninterrupted_snapshot) if uninterrupted_baseline_available else None,
        "resumed_artifact_hash": _hash_payload(resumed_snapshot),
        "interrupt": {
            "requested_after": interrupt_after,
            "actual_after": actual_interrupt_after,
            "checkpoint_id_hash": checkpoint_id_hash,
            "next_nodes_after_interrupt": next_nodes_after_interrupt,
            "prefix_stage_ids": prefix_snapshot["stage_ids"],
        },
        "resume": {
            "resumed_from_checkpoint": True,
            "checkpoint_id_hash": resumed["checkpoint_id_hash"],
            "record_path": str(record_path),
            "resumed_stage_ids": resumed_snapshot["stage_ids"],
        },
        "append_only_audit": append_only_audit,
        "stage_replay_audit": stage_replay_audit,
        "comparison_checks": comparison_checks,
        "uninterrupted_baseline_available": uninterrupted_baseline_available,
        "baseline_comparison_method": baseline_comparison_method,
        "baseline_comparison_verdict": baseline_comparison_verdict,
        "baseline_comparison_note": (
            "Independent uninterrupted baseline was compared with the resumed evidence snapshot."
            if uninterrupted_baseline_available
            else (
                "No independent uninterrupted baseline was produced for this run; comparison_checks are "
                "not_applicable and the top-level verdict only covers resume append-only/stage-replay audits."
            )
        ),
        "verdict_scope": (
            "append_only_stage_replay_and_independent_baseline_comparison"
            if uninterrupted_baseline_available
            else "append_only_stage_replay_only_no_independent_baseline"
        ),
        "allowed_diff_keys": [
            "run_id",
            "timestamps",
            "checkpoint_id",
            "checkpoint_path",
            "resume_diff_report_path",
            "operator_log_path",
        ],
        "acceptable_diffs": [],
        "unacceptable_diff_findings": unacceptable,
        "verdict": verdict,
        "main_result_eligible": False,
        "resume_run_main_result_eligible": False,
        "resume_run_main_result_eligible_assertion": {
            "expected": False,
            "actual": bool(record.final_artifacts.get("main_result_eligible")),
            "ok": record.final_artifacts.get("main_result_eligible") is False,
        },
        "run_record_path": str(record_path),
        "resume_diff_report_path": str(report_path),
        "real_agent_loop_resume_supported": True,
        "real_agent_loop_resume_support_level": "controlled_parent_node_boundary_only",
        "real_agent_loop_resume_scope": "controlled_parent_node_boundary_resume",
        "real_agent_loop_arbitrary_mid_node_resume_supported": False,
        "real_agent_loop_nested_subgraph_resume_supported": False,
        "mid_node_crash_supported": False,
        "transient_store_durable": False,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(_jsonable(report), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    _lg_f1_patch_record_with_report(record_path, report)
    return report


__all__ = [name for name in globals() if not name.startswith("__")]
