from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pyfcstm.bmc.parse import parse_bmc_query

from paper_stm_repair_loop.eval_env import EvalEnvironment
from paper_stm_repair_loop.eval_env.runtime import ALLOWED_FUNCTION_FAMILIES
from paper_stm_repair_loop.pyfcstm_adapter import check_fcstm
from paper_stm_repair_loop.tools.coverage_registry import DirectEvalRuntime

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "discover_capability"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _case_dirs():
    return sorted(path for path in FIXTURES.iterdir() if path.is_dir() and path.name.startswith("D"))


def _fake_bmc_runner(_model_path, query_path, **_kwargs):
    parsed = parse_bmc_query(Path(query_path).read_text(encoding="utf-8"))
    return (
        '{"result":{"status":"sat","property_satisfied":true,"outcome":"property_satisfied"},'
        f'"property":{{"kind":"{parsed.property.kind}",'
        f'"bound":{parsed.property.bound},"polarity":"exists"}},'
        '"replay":{"ok":true}}',
        0,
    )


def _direct_eval(case: Path, twin: str, expression: str, required_families: list[str]) -> dict:
    root = case / twin
    source_trace = _read_json(root / "source_trace_base.json")
    manifest = _read_json(root / "manifest.json")
    env = EvalEnvironment(
        model_text=(root / "STM_0.fcstm").read_text(encoding="utf-8"),
        model_path=str(root / "STM_0.fcstm"),
        source_mappings=source_trace.get("mappings", []),
        coverage_bindings=manifest.get("coverage_bindings", {}),
        timeout_seconds=None,
        bmc_runner=_fake_bmc_runner,
    )
    return DirectEvalRuntime(env).evaluate(
        expression,
        required_function_families=set(required_families),
        reason=f"{case.name}/{twin} capability twin evaluation",
        reason_context={"fixture_id": case.name[:3], "twin": twin},
    )


def test_d01_d12_fixture_directories_and_required_inputs_are_complete():
    assert [path.name[:3] for path in _case_dirs()] == [f"D{i:02d}" for i in range(1, 13)]
    for case in _case_dirs():
        assert (case / "evaluator_gold.json").is_file()
        for twin in ("positive", "negative_twin"):
            root = case / twin
            assert sorted(p.name for p in root.iterdir()) == ["STM_0.fcstm", "manifest.json", "nl.txt", "source_trace_base.json"]


def test_agent_visible_manifests_record_hashes_and_do_not_leak_gold():
    forbidden = set(_read_json(FIXTURES / "_schema.json")["agent_visible_manifest_forbidden_keys"])
    forbidden_fragments = (
        "evaluator_gold",
        "expected_positive_status",
        "expected_negative_twin_status",
        "positive_assertion",
        "negative_twin_assertion",
    )
    for case in _case_dirs():
        for twin in ("positive", "negative_twin"):
            root = case / twin
            manifest_text = (root / "manifest.json").read_text(encoding="utf-8")
            manifest = json.loads(manifest_text)
            assert forbidden.isdisjoint(manifest)
            assert not any(fragment in manifest_text for fragment in forbidden_fragments)
            assert manifest["agent_visible"] is True
            for filename in ("nl.txt", "STM_0.fcstm", "source_trace_base.json"):
                assert manifest["input_hashes_sha256"][filename] == _sha(root / filename)


def test_all_models_parse_inspect_and_can_bind_canonical_eval_environment():
    for case in _case_dirs():
        for twin in ("positive", "negative_twin"):
            model_path = case / twin / "STM_0.fcstm"
            checked = check_fcstm(model_path.read_text(encoding="utf-8"), str(model_path))
            assert checked["parse_status"] == "ok"
            assert checked["inspect_status"] == "ok"
            payload = checked["inspect"]
            assert payload["root_state_path"] == "Root"
            assert payload.get("states")
            assert payload.get("transitions")
            EvalEnvironment(model_text=model_path.read_text(encoding="utf-8"), model_path=str(model_path))


def test_fixture_family_labels_use_only_issue_164_function_family_enum():
    allowed = set(ALLOWED_FUNCTION_FAMILIES)
    assert allowed == {"structure", "relation", "effect", "simulation", "formal", "mapping"}
    schema = _read_json(FIXTURES / "_schema.json")
    assert set(schema["function_families"]) == allowed
    for case in _case_dirs():
        gold = _read_json(case / "evaluator_gold.json")
        unit = gold["gold_units"][0]
        assert unit["issue_family"] in allowed
        assert set(unit["required_function_families"]) <= allowed
        for twin in ("positive", "negative_twin"):
            manifest = _read_json(case / twin / "manifest.json")
            assert manifest["capability_family"] in allowed
            assert set(manifest["required_function_families"]) <= allowed
            assert set(manifest["assertion_route"]["required_function_families"]) <= allowed


def test_evaluator_gold_is_offline_only_and_assertion_routes_match_required_families():
    for case in _case_dirs():
        gold = _read_json(case / "evaluator_gold.json")
        unit = gold["gold_units"][0]
        assert unit["expected_positive_status"] in {"issue", "candidate_only"}
        assert unit["expected_negative_twin_status"] == "ok"
        for twin, assertion_key in (("positive", "positive_assertion"), ("negative_twin", "negative_twin_assertion")):
            manifest = _read_json(case / twin / "manifest.json")
            assert manifest["required_function_families"] == unit["required_function_families"]
            assert manifest["assertion_route"]["required_function_families"] == unit["required_function_families"]
            assert manifest["assertion_route"]["primary_expression"] == unit[assertion_key]


def test_positive_negative_twins_execute_through_canonical_direct_eval_runtime():
    for case in _case_dirs():
        unit = _read_json(case / "evaluator_gold.json")["gold_units"][0]
        positive = _direct_eval(case, "positive", unit["positive_assertion"], unit["required_function_families"])
        negative = _direct_eval(case, "negative_twin", unit["negative_twin_assertion"], unit["required_function_families"])
        assert positive["execution_status"] == "completed", (case.name, positive)
        assert positive["match_status"] == "contradicts", case.name
        assert positive["python_value"] is False, case.name
        assert negative["execution_status"] == "completed", (case.name, negative)
        assert negative["match_status"] == "matches", case.name
        assert negative["python_value"] is True, case.name
        assert set(unit["required_function_families"]) <= set(positive["observed_function_families"]), case.name
        assert set(unit["required_function_families"]) <= set(negative["observed_function_families"]), case.name


def test_d03_d04_have_explicit_hard_gate_assertions_and_expected_truth_values():
    d03 = next(path for path in _case_dirs() if path.name.startswith("D03"))
    d04 = next(path for path in _case_dirs() if path.name.startswith("D04"))
    d03_unit = _read_json(d03 / "evaluator_gold.json")["gold_units"][0]
    d04_unit = _read_json(d04 / "evaluator_gold.json")["gold_units"][0]
    assert "states(parent='Root.Searching'" in d03_unit["positive_assertion"]
    assert "bound_model_refs" not in d03_unit["positive_assertion"]
    assert _direct_eval(d03, "positive", d03_unit["positive_assertion"], d03_unit["required_function_families"])["match_status"] == "contradicts"
    assert _direct_eval(d03, "negative_twin", d03_unit["negative_twin_assertion"], d03_unit["required_function_families"])["match_status"] == "matches"
    assert d04_unit["amount_policy"] == "any_negative"
    assert "effect_delta" in d04_unit["positive_assertion"]
    assert "< 0" in d04_unit["positive_assertion"]
    assert "== -1" not in d04_unit["positive_assertion"]
    assert _direct_eval(d04, "positive", d04_unit["positive_assertion"], d04_unit["required_function_families"])["match_status"] == "contradicts"
    assert _direct_eval(d04, "negative_twin", d04_unit["negative_twin_assertion"], d04_unit["required_function_families"])["match_status"] == "matches"


def test_d09_and_d12_keep_runtime_attribution_separate_from_evaluator_only_gold():
    d09 = next(path for path in _case_dirs() if path.name.startswith("D09"))
    d12 = next(path for path in _case_dirs() if path.name.startswith("D12"))
    d09_trace = _read_json(d09 / "positive" / "source_trace_base.json")
    d12_trace = _read_json(d12 / "positive" / "source_trace_base.json")
    assert d09_trace["attribution_mode"] == "unmapped_conversion"
    assert d09_trace["runtime_attribution"]["max_runtime_issue_assessment"] == "candidate_only"
    assert d09_trace["runtime_attribution"]["repair_allowed_if_assertion_false"] is False
    assert _read_json(d09 / "evaluator_gold.json")["gold_units"][0]["evaluator_only"] is True
    assert _read_json(d09 / "evaluator_gold.json")["gold_units"][0]["issue_family"] == "mapping"
    assert d12_trace["attribution_mode"] == "exact_identity"
    assert d12_trace["runtime_attribution"]["max_runtime_issue_assessment"] == "confirmed"
    assert d12_trace["runtime_attribution"]["repair_allowed_if_assertion_false"] is True
    assert _read_json(d12 / "evaluator_gold.json")["gold_units"][0]["issue_family"] == "mapping"


def test_a_stage_boundary_families_are_not_mixed_into_d_fixtures():
    all_text = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURES.rglob("*.json"))
    assert "input_not_operationalizable" not in all_text
    assert "A01" not in all_text and "A02" not in all_text and "A03" not in all_text


def test_runtime_capability_manifest_freezes_issue165_nonformal_metadata_before_dispatch(tmp_path):
    from paper_stm_repair_loop.agents.discover import _write_capability_manifest
    from paper_stm_repair_loop.records import RecordStore, sha256_json
    from paper_stm_repair_loop.tools.check_fcstm import execute as runtime_check_fcstm

    from v2_helpers import make_case, make_manifest

    case = make_case()
    manifest = make_manifest()
    manifest.update(
        {
            "formal_profile": False,
            "agent_limits": {"turns": 1},
            "reviewer_limits": {"turns": 1},
            "fbmcq_limits": {"max_bound": 4, "solver_timeout_ms": 1000},
        }
    )
    store = RecordStore(tmp_path)
    checked = runtime_check_fcstm(case.fcstm, "inputs/STM_0.fcstm")
    check_record = store.append("check_fcstm_completed", checked)
    frozen_check = {
        **checked,
        "record_id": check_record["record_id"],
        "record_sha256": check_record["record_sha256"],
    }

    capability = _write_capability_manifest(tmp_path, manifest, case, frozen_check)

    assert capability["schema_version"] == "paper1.capability_manifest.v3"
    assert capability["issue_contract_ref"] == "Issue #165 §11.2"
    assert capability["formal_verification_available"] is False
    assert isinstance(capability["bmc_backend_available"], bool)
    assert capability["formal_claim_eligible"] is False
    assert "fbmcq" not in capability["eval_functions"]
    assert "read_fbmcq_guide" not in capability["agent_tools"]
    assert capability["frozen_check_result"]["check_record_id"] == check_record["record_id"]
    assert capability["frozen_check_result"]["check_result_sha256"] == sha256_json(frozen_check)
    assert capability["schema_hashes"]["InspectModelResult"] == capability["inspect_model_result_schema_hash"]
    assert capability["hot_start_capability"]["missing_or_partial_initial_vars_policy"] == "fail_closed"
    assert capability["cold_start_capability"] == {
        "available": True,
        "mode": "default_state_with_optional_partial_variable_overrides",
        "omitted_variable_policy": "use_declaration_initializers",
        "leading_empty_cycle_required": True,
    }
    assert capability["topology_path_backend"]["available"] is True
    assert capability["process_isolation_policy"]["fbmcq_backend"] == "multiprocessing_spawn"
    assert (
        capability["process_isolation_policy"]["result_transport"]
        == "private_temporary_json_file"
    )
    assert capability["cli_resource_profile"]["fbmcq_limits"] == manifest["fbmcq_limits"]
    assert capability["prompt_evidence_policy_fingerprint"]
    assert capability["evidence_policy"]["evidence_policy_fingerprint"]
    assert capability["diagnostic_schema_code_registry_identity"]["registry_size"] > 0
    assert capability["inspect_model_result_sha256"]

    records = store.all()
    assert [record["record_type"] for record in records] == [
        "check_fcstm_completed",
        "capability_manifest",
    ]
    assert _read_json(tmp_path / "capability_manifest.json") == capability
