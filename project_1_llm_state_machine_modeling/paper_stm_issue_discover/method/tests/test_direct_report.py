"""A3 isolation and real deterministic backend checks; no provider is called."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.orchestration.direct_report import (
    DISABLED_STEPS, DirectReport, DirectReportResponse, build_prompt,
    execution_candidate,
)
from paper_stm_method.orchestration.runtime import FixtureStructuredRuntime

PAPER = Path(__file__).resolve().parents[2]
REPORT = PAPER / "pipeline/representation/reports/llms_emp_r45_java_60"


def reports(pair):
    states = {s.name: s.ref for s in pair.model.states}
    common = dict(
        title="Fixture claim", requirement_quote=pair.nl_text,
        source_quote="HumanDrivingMode --> AutonomousMode : front_distance > 10",
        source_refs=["plantuml:line:12"], locus_kind="state",
        locus_names=["HumanDrivingMode"], property="element_declaration",
        violation_direction="missing", expected="Fixture required fact",
        observed="Fixture observed fact", reason="Fixture source comparison",
        basis="Fixture only, no live model", predicate_id="S1",
        predicate_inputs={"kind": "state", "element": "HumanDrivingMode", "scope": "closed_fcstm"},
        element_refs=[states["HumanDrivingMode"]],
    )
    passed = DirectReport(**common)
    failed = passed.model_copy(update={
        "predicate_id": "S2", "property": "transition_endpoints", "locus_kind": "transition",
        "locus_names": ("HumanDrivingMode", "FinalState"),
        "element_refs": [states["HumanDrivingMode"], states["FinalState"]],
        "predicate_inputs": {"source": "HumanDrivingMode", "target": "FinalState", "scope": "closed_fcstm"},
    })
    unsupported = passed.model_copy(update={
        "predicate_id": None, "predicate_inputs": {}, "property": "other",
        "expected": "A concrete unsupported fixture property",
    })
    unbound = unsupported.model_copy(update={"element_refs": ["state:no-such-carrier"], "expected": "Unbound fixture"})
    return [passed, failed, unsupported, unsupported.model_copy(), unbound]


class Runtime(FixtureStructuredRuntime):
    def __init__(self, issues):
        self.issues = issues
        self.calls = []

    def call(self, **kwargs):
        self.calls.append(kwargs)
        assert kwargs["kind"] == "direct_report"
        assert kwargs["retry_cell_on_provider_error"] is False
        result = super().call(**kwargs)
        return result.model_copy(update={
            "response": DirectReportResponse(issues=self.issues, reason="Fixture", basis="Fixture"),
            # Simulate eligibility only; all data remains inside pytest tmp_path.
            "real_llm": True,
        })


def test_one_generation_real_execution_and_no_full_consumers(monkeypatch, tmp_path):
    pair = load_pair(REPORT / "pairs/0000")
    def forbidden(*args, **kwargs):
        pytest.fail("A3 entered a disabled Full consumer")
    for name in (*DISABLED_STEPS, "build_contract_prompt", "build_grounding_prompt",
                 "build_d_adjudication_batches", "_deterministic_candidate",
                 "_annotate_author_anchors", "_preflight_existing_endpoint_candidates",
                 "suppress_satisfied_source_transition_candidates"):
        if hasattr(runner, name):
            monkeypatch.setattr(runner, name, forbidden)
    runtime = Runtime(reports(pair))
    cell = runner._method_cell(pair=pair, round_index=1, runtime=runtime, output_root=tmp_path,
                               run_identity={"ablation": "direct-report", "run_id": "a" * 32,
                                             "run_contract_hash": "sha256:" + "b" * 64,
                                             "source_provenance": runner._source_provenance()})
    assert len(runtime.calls) == len(cell["llm_calls"]) == 1
    prompt = json.loads(runtime.calls[0]["prompt"])
    assert prompt["natural_language"] == pair.nl_text
    assert prompt["author_state_machine"] == pair.plantuml_text
    assert prompt["inspection"]["reference"]
    assert set(prompt) == {"natural_language", "author_state_machine", "inspection", "execution_representation", "model_identity_catalog", "predicates", "input_conventions", "runtime_scenario_schema"}
    records = cell["evidence_records"]
    assert [r["publication_status"] for r in records] == [
        "filtered_true", "published", "published", "folded_exact_duplicate", "coverage_gap",
    ]
    assert [r["receipt"]["verdict"] for r in records[:3]] == ["true", "false", "unknown"]
    assert records[2]["execution_receipt"]["execution_status"] == "unsupported"
    assert len(cell["report_issue_clusters"]) == 2
    assert all(r["d_level"] is None and r["semantic_adjudication"] is None for r in records)
    assert cell["stage_outputs"]["execute_batch"]["new_candidate_count"] == 0
    assert records[3]["final_report_id"] == records[2]["issue_id"]
    assert len(cell["predicate_execution_receipts"]) == 5
    assert cell["eligible"]
    for record in records:
        original = runtime.issues[record["generation_index"]]
        assert record["expected"] == original.expected
        assert record["observed"] == original.observed
    runner._finalize_w2_audit_links(output_root=tmp_path, pair_id=pair.pair_id, rounds_data=[cell])
    from paper_stm_judge.artifacts import adapt_evidence_discovery_release
    projected, audit, round_no, pair_id = adapt_evidence_discovery_release(
        tmp_path / "method/0000/round-1.json", (),
    )
    assert len(projected) == len(audit.report_id_map) == 2
    assert (round_no, pair_id) == (1, "0000")
    for report in projected:
        assert not {"receipt", "predicate_id", "predicate_inputs", "d_level", "witness_level", "execution_receipt"} & report.model_dump().keys()
        assert report.reason == "Fixture source comparison"


def test_zero_report_and_reserved_verdict(tmp_path):
    pair = load_pair(REPORT / "pairs/0000")
    runtime = Runtime([])
    identity = {"ablation": "direct-report", "run_id": "a" * 32,
                "run_contract_hash": "sha256:" + "b" * 64,
                "source_provenance": runner._source_provenance()}
    cell = runner._method_cell(pair=pair, round_index=1, runtime=runtime, output_root=tmp_path, run_identity=identity)
    assert cell["eligible"] and cell["status"] == "completed"
    assert not cell["report_issue_clusters"]
    value = reports(pair)[0].model_dump()
    with pytest.raises(ValidationError):
        DirectReport.model_validate({**value, "verdict": "false"})
    with pytest.raises(ValidationError, match="answers"):
        DirectReport.model_validate({**value, "predicate_inputs": {"verdict": "false"}})
    assert "case_report" not in json.loads(build_prompt(pair))


def test_full_hash_and_a3_resume_identity(tmp_path):
    assert runner._prompt_schema_hash() == "sha256:744e7f489591904a08e9919ded9f99ec73c2d55d81225fbd8a9ec18dca8fefe2"
    assert runner._prompt_schema_hash("direct-report") != runner._prompt_schema_hash()
    args = dict(report_root=REPORT, output_dir=tmp_path, profile="fixture", ablation="direct-report",
                rounds=1, pair_ids=["0000", "0001"], workers=2, run_id="c" * 32)
    summary = runner.run_experiment(**args)
    assert summary["method_cell_count"] == 2
    root = Path(summary["artifact_root"])
    assert json.loads((root / "run_manifest.json").read_text())["ablation"] == "direct-report"
    for pair in args["pair_ids"]:
        cell = json.loads((root / f"method/{pair}/round-1.json").read_text())
        assert cell["ablation"] == "direct-report"
        assert len(cell["llm_calls"]) == 1
    with pytest.raises(RuntimeError, match="resume contract mismatch"):
        runner.run_experiment(**{**args, "ablation": "none"}, resume=True)


def test_backend_error_degrades_and_missing_subject_is_not_invented(monkeypatch, tmp_path):
    pair = load_pair(REPORT / "pairs/0000")
    candidate = reports(pair)[0].candidate(0).model_copy(update={"predicate_inputs": {"scope": "closed_fcstm", "kind": "state"}})
    binding = runner.bind_candidate(candidate, pair.model)
    assert "element" in runner._enrich_candidate(candidate, binding, pair).predicate_inputs
    assert "element" not in runner._enrich_candidate(candidate, binding, pair, infer_missing_subject=False).predicate_inputs
    def failed_backend(*args, **kwargs):
        raise RuntimeError("fixture backend failure")
    monkeypatch.setattr(runner, "run_backend", failed_backend)
    cell = runner._method_cell(
        pair=pair, round_index=1, runtime=Runtime([reports(pair)[1]]), output_root=tmp_path,
        run_identity={"ablation": "direct-report", "run_id": "a" * 32,
                      "run_contract_hash": "sha256:" + "b" * 64,
                      "source_provenance": runner._source_provenance()},
    )
    record = cell["evidence_records"][0]
    assert record["receipt"]["verdict"] == "unknown"
    assert record["witness_level"] == "W1"
    assert record["publication_status"] == "published"
    assert record["expected"] == reports(pair)[1].expected


def test_exact_state_refs_execute_in_native_graph_backend():
    pair = load_pair(REPORT / "pairs/0000")
    states = {s.name: s for s in pair.model.states}
    candidate = reports(pair)[0].candidate(0).model_copy(update={
        "predicate_id": "G1", "property": "reachability", "violation_direction": "unreachable",
        "predicate_inputs": {"source": states["HumanDrivingMode"].ref, "target": states["FinalState"].ref},
        "element_refs": [states["HumanDrivingMode"].ref, states["FinalState"].ref],
    })
    adapted = execution_candidate(candidate, pair)
    assert adapted.predicate_inputs == {"source": states["HumanDrivingMode"].canonical_path, "target": states["FinalState"].canonical_path}
    assert adapted.expected == candidate.expected
    prepared = runner._prepare_candidate(pair, adapted, 1, 0, infer_missing_subject=False)
    assert prepared["receipt"].terminal_state == "completed"
    assert prepared["receipt"].verdict in ("true", "false")


def test_audit_write_failure_does_not_claim_publication(monkeypatch, tmp_path):
    from paper_stm_method.orchestration import direct_report

    pair = load_pair(REPORT / "pairs/0000")
    write = direct_report.write_json

    def fail_audit(path, value):
        if "audit_bundles" in path.parts:
            raise OSError("fixture audit write failure")
        return write(path, value)

    monkeypatch.setattr(direct_report, "write_json", fail_audit)
    cell = runner._method_cell(
        pair=pair, round_index=1, runtime=Runtime([reports(pair)[1]]), output_root=tmp_path,
        run_identity={"ablation": "direct-report", "run_id": "a" * 32,
                      "run_contract_hash": "sha256:" + "b" * 64,
                      "source_provenance": runner._source_provenance()},
    )
    assert cell["eligible"] and cell["status"] == "completed_with_diagnostics"
    assert not cell["report_issue_clusters"]
    record = cell["evidence_records"][0]
    assert record["receipt"]["verdict"] == "false"
    assert not record["issue_emitted"] and record["final_report_id"] is None
    assert record["publication_status"] == "coverage_gap" and record["witness_level"] == "W0"
    assert record["diagnostic"]["error_type"] == "OSError"
