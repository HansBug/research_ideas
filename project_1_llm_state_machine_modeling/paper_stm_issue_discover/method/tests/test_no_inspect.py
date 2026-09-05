"""A1 removes precomputed facts, not author mapping or candidate predicates."""

import importlib.util
import json
from pathlib import Path

import pytest

from paper_stm_method.inputs import FROZEN_PAIR_IDS, load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.semantics import frontier, workflow
from paper_stm_method.semantics.ablation import (
    INSPECTION_ROLES, NoInspectInput, pair_system_prompt, prompt_context_payload,
    without_inspection,
)


PAPER = Path(__file__).resolve().parents[2]
REPORT = PAPER / "pipeline/representation/reports/llms_emp_r45_java_60"
SOURCE_FIXTURE = PAPER / "pipeline/evidence_discovery/tests/test_input_closure_and_staged_flow.py"
if not SOURCE_FIXTURE.is_file() and runner._release_source_provenance() is not None:
    pytest.skip("repository input closure and staged fixture are not shipped in the verified release", allow_module_level=True)
spec = importlib.util.spec_from_file_location(
    "staged_fixture", SOURCE_FIXTURE
)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


@pytest.mark.parametrize("pair_id", FROZEN_PAIR_IDS)
def test_all_pair_projections_keep_source_and_remove_check_side_channels(pair_id):
    pair = load_pair(REPORT / "pairs" / pair_id)
    original = pair.working_contract.model_dump(mode="json")
    view = without_inspection(pair)
    assert isinstance(view, NoInspectInput)
    assert view.model is pair.model
    assert view.exact_source_inventory is pair.exact_source_inventory
    assert view.source_trace is pair.source_trace
    assert view.fcstm_text == pair.fcstm_text
    assert view.plantuml_text == pair.plantuml_text
    assert view.context_manifest is pair.context_manifest
    assert pair.working_contract.model_dump(mode="json") == original
    assert view.working_contract.payload["elements"] == pair.working_contract.payload["elements"]
    assert view.working_contract.payload["macros"] == pair.working_contract.payload["macros"]
    assert not any(getattr(view, name) for name in ("reference_inspection", "inspection_facts", "verify_facts", "smt_facts"))
    for stage in ("nl_contract_extraction", "discovery_grounding", "d_adjudication"):
        payload = prompt_context_payload(view, stage=stage)
        assert INSPECTION_ROLES.isdisjoint(payload)
        assert INSPECTION_ROLES.isdisjoint(payload["source_roles"])
        assert all(not r["prompt_included"] for r in payload["artifact_refs"] if r["role"] in INSPECTION_ROLES)
        assert "artifact_status" not in payload["case_report"]["payload"]
        assert "inspection_facts" not in payload["case_report"]["payload"]["source_hashes"]
        text = json.dumps(payload)
        for key in ("diagnostic_record_count", "diagnostic_binding_status", "diagnostic_attribution_receipt"):
            assert key not in text
        assert payload["ablation"]["status"] == "disabled_by_ablation"


def test_no_inspect_disables_producers_through_completion_and_correction(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("A1 executed an inspection-derived producer")

    for name in ("_materialize_root_reachability", "_materialize_dead_ends", "_materialize_cross_wrapper",
                 "_materialize_event_consumers", "_materialize_inspection_diagnostics"):
        monkeypatch.setattr(frontier, name, forbidden)
    monkeypatch.setattr(runner, "materialize_domain_invariant_contracts", forbidden)
    monkeypatch.setattr(runner, "_preflight_synthetic_root_wrapper_reachability", forbidden)
    source_calls = []
    source_divergence = frontier._materialize_source_divergence

    def source_spy(*args, **kwargs):
        source_calls.append(True)
        return source_divergence(*args, **kwargs)

    monkeypatch.setattr(frontier, "_materialize_source_divergence", source_spy)

    class Runtime(fixture.FixtureStructuredRuntime):
        def call(self, **kwargs):
            system = kwargs["system_prompt"]
            assert "inspection" not in system.lower()
            assert "SMT formula summaries" not in system
            # Fixture provenance enables production completion/correction branches;
            # no provider is called and no output is an experimental result.
            return super().call(**kwargs).model_copy(update={"real_llm": True})

    runtime = Runtime(include_second_candidate=True, omit_second_d_decision=True)
    cell = runner._method_cell(
        pair=load_pair(REPORT / "pairs/0000"), round_index=1, runtime=runtime, output_root=tmp_path,
        run_identity={"ablation": "no-inspect", "run_id": "0" * 32,
                      "run_contract_hash": "sha256:" + "0" * 64,
                      "source_provenance": runner._source_provenance()},
    )
    kinds = [kind for kind, _ in runtime.prompts]
    assert "contract_completion" in kinds
    assert "d_adjudication_correction" in kinds
    assert source_calls
    assert cell["ablation"] == "no-inspect"
    assert cell["predicate_execution_receipts"]
    assert cell["stage_outputs"]["execute_batch"]["domain_invariant_candidate_count"] == 0
    for stage in cell["stage_receipts"]:
        assert INSPECTION_ROLES.isdisjoint(stage["input_artifact_roles"])
    audit = json.loads((tmp_path / "input_audits/0000.json").read_text())
    assert audit["inspection_equivalent_facts"]
    for _, prompt in runtime.prompts:
        for key in ("diagnostic_record_count", "diagnostic_binding_status", '"inspection_equivalent_facts": {', '"verify_facts": {', '"smt_facts": {'):
            assert key not in prompt


def test_shared_full_projection_and_prompts_stay_identical():
    from paper_stm_method.inputs.context import prompt_context_payload as original

    pair = load_pair(REPORT / "pairs/0004")
    for stage in ("nl_contract_extraction", "discovery_grounding", "d_adjudication"):
        assert prompt_context_payload(pair, stage=stage) == original(pair, stage=stage)
    for prompt in (workflow.CONTRACT_SYSTEM_PROMPT, workflow.DISCOVERY_GROUNDING_SYSTEM_PROMPT, workflow.D_SYSTEM_PROMPT):
        assert pair_system_prompt(pair, prompt) is prompt
    assert runner._prompt_schema_hash() == runner._prompt_schema_hash("none")
    assert runner._prompt_schema_hash("none") != runner._prompt_schema_hash("no-inspect")


def test_no_inspect_candidate_native_execution_and_w2_are_preserved():
    from paper_stm_method.evidence.audit_bundle import build_audit_bundle
    from paper_stm_method.evidence.receipts import build_predicate_execution_receipt

    pair = load_pair(REPORT / "pairs/0004")
    transition = next(t for t in pair.model.transitions if t.triggers)
    candidate = workflow.CandidateIssue(
        contract_id="NL-CONTRACT-NL1", locus_kind="transition",
        locus_names=(transition.source, transition.target), property="trigger_set",
        violation_direction="mismatched", evidence_types=("source_identity", "transition_fact"),
        title="Exact trigger check", requirement_quote=pair.nl_segments[0].text,
        predicate_id="S3", predicate_inputs={"transition": transition.ref, "triggers": list(transition.triggers)},
        element_refs=[transition.ref], source_refs=["nl:NL1"], expected="Exact supplied trigger set.",
        observed="The bound carrier has a directly executable trigger set.", strongest_rebuttal="none",
        reason="Native execution fixture, not an experimental finding.", basis="Exact parsed transition identity.",
    )
    full = runner._prepare_candidate(pair, candidate, 1, 0)
    ablated = runner._prepare_candidate(without_inspection(pair), candidate, 1, 0)
    assert full["plan"] == ablated["plan"]
    assert full["receipt"].verdict == ablated["receipt"].verdict == "true"
    assert ablated["receipt"].terminal_state == "completed"
    assert ablated["source_attribution"]["input_context"]["ablation"] == "no-inspect"
    for role in ("inspection_facts", "verify_facts", "smt_facts"):
        assert ablated["source_attribution"]["roles"][role] == "disabled_by_ablation"
    execution = build_predicate_execution_receipt(
        pair_id=pair.pair_id, run_id="0" * 32, contract_id=candidate.contract_id,
        obligation_id=ablated["obligation_id"], plan=ablated["plan"], receipt=ablated["receipt"],
        source_attribution=ablated["source_attribution"], model_hash=pair.hashes["fcstm"],
    )
    assert execution["witness_level"] == "W2"
    assert not runner._prepared_is_finding_candidate(ablated), "true receipts must still suppress findings"
    audit = build_audit_bundle(
        pair=without_inspection(pair), obligation_id=ablated["obligation_id"],
        binding=ablated["binding"], plan=ablated["plan"], receipt=ablated["receipt"],
        source_attribution=ablated["source_attribution"], reason="A1 fixture", basis="Native receipt",
        retry_records=[], execution_receipt=execution,
    )
    assert audit["input_context"]["ablation"] == "no-inspect"
    assert audit["input_context"]["source_roles"]["inspection_facts"] == "disabled_by_ablation"

    state = next(s for s in pair.model.states if s.ref == transition.source_ref)
    prepared = {**ablated, "candidate": candidate.model_copy(update={
        "property": "deadlock_freedom", "violation_direction": "dead_end",
    }), "binding": ablated["binding"].model_copy(update={"element_refs": [state.ref]})}
    decision = runner.SemanticAdjudication(
        obligation_id=ablated["obligation_id"], grounding="established",
        violated_obligation="Fixture dead-end claim", defeater_kind="none",
        defeater_disposition="defeated", reason="A1 D-consumer fixture", basis="Bound state",
    )
    assert any("outgoing-transition" in error for error in runner._d_decision_consistency_errors(
        decision, prepared=prepared, pair=pair,
    ))
    assert runner._d_decision_consistency_errors(decision, prepared=prepared, pair=without_inspection(pair)) == []


def test_no_inspect_worker_records_and_resume(tmp_path):
    args = dict(report_root=REPORT, output_dir=tmp_path, profile="fixture", ablation="no-inspect",
                rounds=1, pair_ids=["0004", "0023"], workers=2, run_id="b" * 32)
    summary = runner.run_experiment(**args)
    root = Path(summary["artifact_root"])
    assert summary["ablation"] == "no-inspect"
    for pair_id in args["pair_ids"]:
        cell = json.loads((root / "method" / pair_id / "round-1.json").read_text())
        assert cell["ablation"] == "no-inspect"
        assert cell["stage_outputs"]["ablation"]["predicate_execution"] == "enabled"
        assert cell["stage_outputs"]["execute_batch"]["domain_invariant_candidate_count"] == 0
        assert not cell["eligible"], "fixture must not enter experimental metrics"
    runner.run_experiment(**args, resume=True)
    with pytest.raises(RuntimeError, match="resume contract mismatch"):
        runner.run_experiment(**{**args, "ablation": "none"}, resume=True)
