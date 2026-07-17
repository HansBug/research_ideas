from __future__ import annotations

import inspect
import json
import re
from dataclasses import replace
from pathlib import Path

from paper_stm_repair_loop.agents.discover import run_discover
from paper_stm_repair_loop.controller import _bind_drafts
from paper_stm_repair_loop.inputs import load_custom, load_pair, load_run_case, prepare_run_dir
from paper_stm_repair_loop.pyfcstm_adapter import sha256_text
from paper_stm_repair_loop.schemas import CheckDraftSubmission
from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm
from paper_stm_repair_loop.tools.run_scenarios import execute as run_scenarios
from paper_stm_repair_loop.tools.lookup_source_trace import execute as lookup_source_trace
from paper_stm_repair_loop.tools.validate_discovery_checks import execute as validate_discovery_checks
from paper_stm_repair_loop.tools.verify_static_consistency import execute as verify_static_consistency


ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "fixtures/discover_replay.json"


def test_discover_runtime_contains_exactly_one_agent_app_run_and_no_controller_agent():
    import paper_stm_repair_loop.agents.discover as discover_module
    import paper_stm_repair_loop.controller as controller_module

    controller_source = inspect.getsource(controller_module)
    discover_source = inspect.getsource(discover_module)
    assert "AgentApp" not in controller_source
    assert "AgentSpec" not in controller_source
    assert discover_source.count("result = app.run(") == 1
    assert "prepare_issue_checks" not in discover_source
    assert "retry_missing_structured_output=True" in discover_source
    assert 'SubmitDiscoveryResponse.__name__ = "submit_discovery"' in discover_source
    assert 'limits=manifest.get("agent_limits") or None' in discover_source


def test_pair_loader_uses_canonical_nl_and_prepared_fcstm():
    case = load_pair("llms_emp_stm_results_0000")
    assert case.pair_id == "llms_emp_stm_results_0000"
    assert "human driving" in case.nl.lower()
    assert "state llms_emp_gpt4o_hldcs" in case.fcstm


def test_pair_loader_rejects_any_external_model_or_trace_override(tmp_path: Path):
    model = tmp_path / "override.fcstm"
    trace = tmp_path / "trace.json"
    model.write_text("state Root { state Idle; [*] -> Idle; }\n", encoding="utf-8")
    trace.write_text(
        json.dumps(
            {
                "source_traceability": {
                    "fcstm_sha256": sha256_text(model.read_text(encoding="utf-8"))
                }
            }
        ),
        encoding="utf-8",
    )
    try:
        load_pair("llms_emp_stm_results_0000", fcstm_file=model, source_trace_file=trace)
    except ValueError as exc:
        assert "PAIR_INPUT_OVERRIDE_FORBIDDEN" in str(exc)
    else:
        raise AssertionError("external model and matching trace must use custom mode")


def test_replay_writes_all_outputs_under_one_outdir(tmp_path: Path):
    case = load_pair("llms_emp_stm_results_0000")
    prepare_run_dir(tmp_path, case, profile="gpt-5.5", content_language="zh-CN", renderer="quiet", replay_file=REPLAY)
    result = run_discover(tmp_path, object())
    assert result.no_issue_found is True
    assert result.agent_real_llm is False
    assert result.agent_academic_eligible is False
    assert result.test_replay is True
    assert result.main_result_eligible is False
    assert (tmp_path / "manifest.json").exists()
    capabilities = json.loads((tmp_path / "capability_manifest.json").read_text(encoding="utf-8"))
    required_capability_fields = {
        "tool_name",
        "adapter_name",
        "adapter_version",
        "upstream_version",
        "upstream_git_commit",
        "upstream_available",
        "adapter_available",
        "profile_required",
        "timeout",
        "retry_policy",
    }
    assert capabilities["pyfcstm_git_commit"] == "4ea23c9b153f47e5c4a2125d95b466eee6eed13e"
    assert all(required_capability_fields.issubset(item) for item in capabilities["tools"].values())
    assert (tmp_path / "inputs/STM_0.fcstm").exists()
    assert (tmp_path / "agent_audit/discover/audit.jsonl").exists()
    assert (tmp_path / "contexts/discover-attempt-001/context.json").exists()
    assert (tmp_path / "records").is_dir()
    report = tmp_path / "loops/discover.md"
    assert report.exists()
    report_text = report.read_text(encoding="utf-8")
    assert "Agent academic eligible: `false`" in report_text
    assert "test replay: `true`" in report_text
    assert "## Controller 必跑结果" in report_text
    assert "## 未形成 root 的 proposition" in report_text
    assert "`PROP-ROOT-SHAPE-REJECTED`" in report_text
    assert "accepted_fix_count=0" in report_text
    for target in re.findall(r"\]\(([^)]+)\)", report_text):
        assert (report.parent / target).resolve().is_file(), target
    records = sorted((tmp_path / "records").glob("*/record.json"))
    assert any(json.loads(p.read_text())["record_type"] == "discover_completed" for p in records)


def test_replay_requires_every_check_to_be_covered_by_root_or_rejected_proposition(tmp_path: Path):
    case = load_pair("llms_emp_stm_results_0000")
    replay = tmp_path / "uncovered-replay.json"
    data = json.loads(REPLAY.read_text(encoding="utf-8"))
    data["submission"]["rejected_propositions"] = []
    replay.write_text(json.dumps(data), encoding="utf-8")
    run_dir = tmp_path / "run"
    prepare_run_dir(run_dir, case, profile="gpt-5.5", content_language="zh-CN", renderer="quiet", replay_file=replay)
    try:
        run_discover(run_dir, object())
    except ValueError as exc:
        assert "proposition coverage mismatch" in str(exc)
    else:
        raise AssertionError("uncovered final checks must not publish Discover")
    record_types = [json.loads(path.read_text())["record_type"] for path in (run_dir / "records").glob("*/record.json")]
    assert "run_failed" in record_types
    assert "discover_completed" not in record_types


def test_confirmed_root_is_published_with_controller_execution_evidence(tmp_path: Path):
    case = replace(
        load_pair("llms_emp_stm_results_0000"),
        source_trace={
            "schema_version": "source_trace_base.v1",
            "relation_policy": "evidence_only",
            "entries": [
                {
                    "source_elements": ["source:root-operating-mode"],
                    "intermediate_elements": ["state:llms_emp_gpt4o_hldcs"],
                }
            ],
        },
    )
    replay = tmp_path / "confirmed-replay.json"
    data = json.loads(REPLAY.read_text(encoding="utf-8"))
    data["submission"].update(
        {
            "no_issue_found": False,
            "root_nodes": [
                {
                    "node_id": "ISS-root-shape@n0",
                    "issue_id": "ISS-root-shape",
                    "assessment": "confirmed",
                    "downstream_repair_allowed": True,
                    "statement": "The root state shape contradicts the declared behavior.",
                    "rationale": "The registered deterministic property check contradicts its typed expectation.",
                    "supporting_record_ids": [],
                    "required_check_ids": ["CHK-NL-001"],
                    "source_element_refs": ["state:llms_emp_gpt4o_hldcs"],
                }
            ],
            "rejected_propositions": [],
            "rationale": "One root is supported by the registered check batch.",
        }
    )
    replay.write_text(json.dumps(data), encoding="utf-8")
    run_dir = tmp_path / "run"
    prepare_run_dir(run_dir, case, profile="gpt-5.5", content_language="zh-CN", renderer="quiet", replay_file=replay)

    completed = run_discover(run_dir, object())
    records = {
        json.loads(path.read_text(encoding="utf-8"))["record_id"]: json.loads(path.read_text(encoding="utf-8"))
        for path in (run_dir / "records").glob("*/record.json")
    }
    supporting_types = {
        records[record_id]["record_type"]
        for record_id in completed.root_nodes[0].supporting_record_ids
    }
    assert "issue_check_preparation_completed" in supporting_types
    assert "verify_properties_completed" in supporting_types
    assert "validate_discovery_checks_completed" in supporting_types
    assert "discover_mandatory_preparation_completed" in supporting_types


def _confirmed_replay(tmp_path: Path) -> Path:
    replay = tmp_path / "confirmed-replay.json"
    data = json.loads(REPLAY.read_text(encoding="utf-8"))
    data["submission"].update(
        {
            "no_issue_found": False,
            "root_nodes": [
                {
                    "node_id": "ISS-root-shape@n0",
                    "issue_id": "ISS-root-shape",
                    "assessment": "confirmed",
                    "downstream_repair_allowed": True,
                    "statement": "The root state shape contradicts the declared behavior.",
                    "rationale": "The registered deterministic property check contradicts its typed expectation.",
                    "supporting_record_ids": [],
                    "required_check_ids": ["CHK-NL-001"],
                    "source_element_refs": ["state:llms_emp_gpt4o_hldcs"],
                }
            ],
            "rejected_propositions": [],
            "rationale": "One root is supported by the registered check batch.",
        }
    )
    replay.write_text(json.dumps(data), encoding="utf-8")
    return replay


def test_confirmed_root_requires_element_level_source_trace(tmp_path: Path):
    case = load_pair("llms_emp_stm_results_0000")
    run_dir = tmp_path / "run"
    prepare_run_dir(
        run_dir,
        case,
        profile="gpt-5.5",
        content_language="zh-CN",
        renderer="quiet",
        replay_file=_confirmed_replay(tmp_path),
    )

    try:
        run_discover(run_dir, object())
    except ValueError as exc:
        assert "lacks exact source attribution" in str(exc)
    else:
        raise AssertionError("empty element-level source trace must not publish a confirmed root")
    record_types = [json.loads(path.read_text())["record_type"] for path in (run_dir / "records").glob("*/record.json")]
    assert "run_failed" in record_types
    assert "discover_completed" not in record_types


def test_confirmed_root_rejects_ambiguous_source_trace(tmp_path: Path):
    case = replace(
        load_pair("llms_emp_stm_results_0000"),
        source_trace={
            "schema_version": "source_trace_base.v1",
            "relation_policy": "evidence_only",
            "entries": [
                {
                    "source_elements": ["source:root-a", "source:root-b"],
                    "intermediate_elements": ["state:llms_emp_gpt4o_hldcs"],
                }
            ],
        },
    )
    run_dir = tmp_path / "run"
    prepare_run_dir(
        run_dir,
        case,
        profile="gpt-5.5",
        content_language="zh-CN",
        renderer="quiet",
        replay_file=_confirmed_replay(tmp_path),
    )

    try:
        run_discover(run_dir, object())
    except ValueError as exc:
        assert "lacks exact source attribution" in str(exc)
    else:
        raise AssertionError("ambiguous source trace must not publish a confirmed root")
    record_types = [json.loads(path.read_text())["record_type"] for path in (run_dir / "records").glob("*/record.json")]
    assert "run_failed" in record_types
    assert "discover_completed" not in record_types


def test_custom_identity_input(tmp_path: Path):
    nl = tmp_path / "nl.txt"
    model = tmp_path / "model.fcstm"
    nl.write_text("The system starts in Idle.", encoding="utf-8")
    model.write_text('state Root { state Idle; [*] -> Idle; }\n', encoding="utf-8")
    case = load_custom("custom", nl, model)
    assert case.input_mode == "custom"
    assert case.raw_source_format == "fcstm-identity"


def test_custom_raw_source_trace_must_bind_both_source_and_fcstm(tmp_path: Path):
    nl = tmp_path / "nl.txt"
    raw = tmp_path / "source.puml"
    model = tmp_path / "model.fcstm"
    trace = tmp_path / "trace.json"
    nl.write_text("The system starts in Idle.", encoding="utf-8")
    raw.write_text("@startuml\n[*] --> Idle\n@enduml\n", encoding="utf-8")
    model.write_text('state Root { state Idle; [*] -> Idle; }\n', encoding="utf-8")
    trace.write_text(
        json.dumps(
            {
                "schema_version": "source_trace_base.v1",
                "entries": [],
                "source_traceability": {
                    "source_stm0_sha256": sha256_text(raw.read_text(encoding="utf-8")),
                    "fcstm_sha256": sha256_text(model.read_text(encoding="utf-8")),
                },
            }
        ),
        encoding="utf-8",
    )

    case = load_custom("custom-source", nl, model, raw_source_file=raw, source_trace_file=trace)
    assert case.raw_source == raw.read_text(encoding="utf-8")

    data = json.loads(trace.read_text(encoding="utf-8"))
    data["source_traceability"]["fcstm_sha256"] = "0" * 64
    trace.write_text(json.dumps(data), encoding="utf-8")
    try:
        load_custom("custom-source", nl, model, raw_source_file=raw, source_trace_file=trace)
    except ValueError as exc:
        assert "CUSTOM_FCSTM_TRACE_MISMATCH" in str(exc)
    else:
        raise AssertionError("custom source trace with a stale fcstm hash must fail")

    data["source_traceability"]["fcstm_sha256"] = sha256_text(model.read_text(encoding="utf-8"))
    data["source_traceability"]["source_stm0_sha256"] = "0" * 64
    trace.write_text(json.dumps(data), encoding="utf-8")
    try:
        load_custom("custom-source", nl, model, raw_source_file=raw, source_trace_file=trace)
    except ValueError as exc:
        assert "CUSTOM_SOURCE_TRACE_MISMATCH" in str(exc)
    else:
        raise AssertionError("custom source trace with a stale source hash must fail")


def test_run_manifest_rejects_absolute_or_escaping_input_paths(tmp_path: Path):
    nl = tmp_path / "nl.txt"
    model = tmp_path / "model.fcstm"
    nl.write_text("The system starts in Idle.", encoding="utf-8")
    model.write_text('state Root { state Idle; [*] -> Idle; }\n', encoding="utf-8")
    case = load_custom("custom", nl, model)
    run_dir = tmp_path / "run"
    prepare_run_dir(run_dir, case, profile="gpt-5.5", content_language="zh-CN", renderer="quiet")
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["input_files"]["nl"] = str(nl.resolve())
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    try:
        load_run_case(run_dir)
    except ValueError as exc:
        assert "must be relative" in str(exc)
    else:
        raise AssertionError("absolute manifest input path must fail before reading")


def test_scenarios_dispatch_initial_state_and_accept_binder_event_field():
    model = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""
    result = run_scenarios(model, [{"check_id": "SC-1", "check_kind": "scenario", "executable_spec": {"event": "Root.go"}}])
    assert result["execution_status"] == "completed"
    assert result["scenario_results"][0]["consumed_events"] == ["Root.go"]
    assert result["scenario_results"][0]["current_state"] == "Root.Done"


def test_source_trace_reports_partial_untraceability():
    trace = {"entries": [{"source_elements": ["source:a"], "intermediate_elements": ["fcstm:a"]}]}
    result = lookup_source_trace(trace, ["source:a", "source:b"], "source_to_fcstm")
    assert result["exact_matches"]
    assert result["untraceable_refs"] == ["source:b"]


def test_source_binder_supports_lowered_composite_entry_forced_transition_and_state_facts():
    case = load_pair("llms_emp_stm_results_0000")
    source = CheckDraftSubmission.model_validate(
        {
            "checks": [
                {
                    "check_id": "composite-entry",
                    "check_kind": "static_consistency",
                    "statement": "Autonomous returns to HumanDriving.",
                    "expected_outcome": {"consistency_status": "contradicts"},
                    "source_basis": ["Autonomous --> HumanDriving : Human Steering Cmd or Brake Pressed", "conflicting source assertion"],
                    "executable_spec": {
                        "kind": "transition_shape",
                        "source_label": "Autonomous",
                        "target_label": "HumanDriving",
                        "event_label": "Human Steering Cmd or Brake Pressed",
                    },
                },
                {
                    "check_id": "forced-power-off",
                    "check_kind": "static_consistency",
                    "statement": "Power Off reaches FinalState from HumanDriving.",
                    "expected_outcome": {"consistency_status": "contradicts"},
                    "source_basis": ["HumanDriving --> FinalState : Power Off", "conflicting source assertion"],
                    "executable_spec": {
                        "kind": "transition_shape",
                        "source_label": "HumanDriving",
                        "target_label": "FinalState",
                        "event_label": "Power Off",
                    },
                },
                {
                    "check_id": "state-declaration",
                    "check_kind": "static_consistency",
                    "statement": "Autonomous is composite.",
                    "expected_outcome": {"consistency_status": "contradicts"},
                    "source_basis": ["state Autonomous {", "conflicting source assertion"],
                    "executable_spec": {"kind": "state_declaration", "state_label": "Autonomous", "state_kind": "composite"},
                },
                {
                    "check_id": "label-reuse",
                    "check_kind": "static_consistency",
                    "statement": "InitialState occurs in two scopes.",
                    "expected_outcome": {"consistency_status": "contradicts"},
                    "source_basis": ["HumanDriving.InitialState", "Autonomous.InitialState"],
                    "executable_spec": {"kind": "label_reuse", "state_label": "InitialState", "scopes": ["HumanDriving", "Autonomous"]},
                },
            ]
        }
    )
    checks = [item.model_dump(mode="json") for item in _bind_drafts(CheckDraftSubmission(checks=[]), source, check_fcstm(case.fcstm)["inspect"])]
    assert [item["executable_spec"]["kind"] for item in checks] == [
        "transition_shape",
        "forced_transition_shape",
        "state_shape",
        "state_label_scopes",
    ]
    result = verify_static_consistency(checks, check_result=check_fcstm(case.fcstm))
    assert all(item["status"] in {"passed", "failed"} for item in result["static_results"])
    assert not any(item["status"] == "not_implemented" for item in result["static_results"])


def test_invalid_fcstm_cannot_publish_discover_completed(tmp_path: Path):
    nl = tmp_path / "nl.txt"
    model = tmp_path / "bad.fcstm"
    nl.write_text("The system starts in Idle.", encoding="utf-8")
    model.write_text("not fcstm", encoding="utf-8")
    case = load_custom("invalid", nl, model)
    run_dir = tmp_path / "run"
    prepare_run_dir(run_dir, case, profile="gpt-5.5", content_language="zh-CN", renderer="quiet", replay_file=REPLAY)
    try:
        run_discover(run_dir, object())
    except RuntimeError as exc:
        assert "fcstm_not_executable" in str(exc)
    else:
        raise AssertionError("invalid fcstm must not complete Discover")
    record_types = [json.loads(p.read_text())["record_type"] for p in (run_dir / "records").glob("*/record.json")]
    assert "run_failed" in record_types
    assert "discover_completed" not in record_types


def test_empty_check_set_cannot_publish_zero_root_replay(tmp_path: Path):
    case = load_pair("llms_emp_stm_results_0000")
    replay = tmp_path / "empty-replay.json"
    replay.write_text(json.dumps({"issue_checks": [], "submission": {"no_issue_found": True, "rationale": "No checks were available."}}), encoding="utf-8")
    run_dir = tmp_path / "run"
    prepare_run_dir(run_dir, case, profile="gpt-5.5", content_language="zh-CN", renderer="quiet", replay_file=replay)
    try:
        run_discover(run_dir, object())
    except Exception as exc:
        assert "check_drafts" in str(exc) or "at least 1" in str(exc)
    else:
        raise AssertionError("empty check set must not publish zero-root Discover output")


def test_source_basis_does_not_bypass_invalid_model_binding():
    case = load_pair("llms_emp_stm_results_0000")
    from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm

    result = validate_discovery_checks(
        [{
            "check_id": "PROP-BAD-BINDING",
            "check_kind": "property",
            "source_basis": ["source:requirement-1"],
            "binding_refs": ["state:does.not.exist"],
            "executable_spec": {"kind": "state_shape", "state": "does.not.exist", "expect": {"is_leaf": True}},
        }],
        check_fcstm(case.fcstm),
    )
    assert result["mechanically_eligible"] is False
    assert result["checks"][0]["mechanically_eligible"] is False


def test_static_consistency_unsupported_contract_is_explicit():
    case = load_pair("llms_emp_stm_results_0000")
    from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm

    result = verify_static_consistency(
        [{
            "check_id": "STATIC-UNSUPPORTED",
            "check_kind": "static_consistency",
            "source_basis": ["source:element-1"],
            "executable_spec": {"kind": "invented_kind"},
        }],
        check_result=check_fcstm(case.fcstm),
    )
    assert result["static_results"][0]["status"] == "not_implemented"
