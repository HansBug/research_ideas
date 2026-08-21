from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.evidence_discovery.inputs import load_pair, parse_fcstm
from pipeline.evidence_discovery.inputs.context import context_payload
from pipeline.evidence_discovery.orchestration.runner import _method_cell, run_experiment
from pipeline.evidence_discovery.orchestration.runtime import StructuredCallOutcome
from pipeline.evidence_discovery.semantics import (
    DAdjudicationResponse,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    StageReceipt,
)


PAPER_ROOT = Path(__file__).parents[3]
REPORT_ROOT = PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"


class FixtureStructuredRuntime:
    """Provider-free runtime fixture that records every staged prompt."""

    def __init__(
        self,
        *,
        include_second_candidate: bool = False,
        omit_second_d_decision: bool = False,
    ) -> None:
        self.prompts: list[tuple[str, str]] = []
        self.include_second_candidate = include_second_candidate
        self.omit_second_d_decision = omit_second_d_decision
        self.d_call_count = 0

    def call(self, *, kind, schema, system_prompt, prompt, artifact_id, **kwargs):
        self.prompts.append((kind, prompt))
        pair_id = artifact_id.split("/")[1]
        if schema is NLContractResponse:
            response = NLContractResponse(
                contracts=[
                    NLContract(
                        contract_id="NL-CONTRACT-NL1",
                        segment_id="NL1",
                        quote="The supplied source clause.",
                        normative_statement="The supplied source clause is preserved.",
                        scope="source-supplied scope",
                        source_refs=["nl:NL1"],
                        reason="Fixture contract reason.",
                        basis="Fixture numbered NL basis.",
                    )
                ],
                segment_disposition={"NL1": "covered"},
                reason="Fixture contract response reason.",
                basis="Fixture contract response basis.",
            )
        elif schema is GroundingResponse:
            pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
            transition = pair.model.transitions[0]
            candidates = [
                {
                    "title": "Fixture grounded transition",
                    "requirement_quote": "The supplied source clause.",
                    "predicate_id": "S2",
                    "predicate_inputs": {
                        "source": transition.source,
                        "target": transition.target,
                        "scope": "closed_fcstm",
                    },
                    "element_refs": [transition.ref],
                    "source_refs": ["nl:NL1"],
                    "expected": "The transition is present.",
                    "observed": "The transition is present.",
                    "strongest_rebuttal": "none",
                    "reason": "Fixture branch reason.",
                    "basis": "Fixture exact FCSTM transition basis.",
                }
            ]
            if self.include_second_candidate:
                second_transition = pair.model.transitions[1]
                candidates.append(
                    {
                        "title": "Fixture grounded second transition",
                        "requirement_quote": "The second supplied source clause.",
                        "predicate_id": "S2",
                        "predicate_inputs": {
                            "source": second_transition.source,
                            "target": second_transition.target,
                            "scope": "closed_fcstm",
                        },
                        "element_refs": [second_transition.ref],
                        "source_refs": ["nl:NL2"],
                        "expected": "The second transition is present.",
                        "observed": "The second transition is present.",
                        "strongest_rebuttal": "none",
                        "reason": "Fixture second branch reason.",
                        "basis": "Fixture second exact FCSTM transition basis.",
                    }
                )
            response = GroundingResponse(
                branch="source" if kind == "source_grounding" else "model",
                candidates=candidates,
                rejected_contract_ids=[],
                reason="Fixture grounding response reason.",
                basis="Fixture grounding response basis.",
            )
        elif schema is DAdjudicationResponse:
            self.d_call_count += 1
            if self.omit_second_d_decision and kind == "d_adjudication_correction":
                decision_ids = [f"{pair_id}:r1:i1"]
            else:
                decision_ids = [f"{pair_id}:r1:i0"]
            if self.include_second_candidate and not self.omit_second_d_decision:
                decision_ids.append(f"{pair_id}:r1:i1")
            response = DAdjudicationResponse(
                decisions=[
                    {
                        "obligation_id": obligation_id,
                        "grounding": "established",
                        "violated_obligation": "The fixture obligation is semantically grounded.",
                        "strongest_defeater": None,
                        "defeater_kind": "none",
                        "defeater_disposition": "defeated",
                        "reason": "Fixture D reason cites the supplied obligation and exact binding.",
                        "basis": "Fixture semantic dossier and closed enum decision.",
                    }
                    for obligation_id in decision_ids
                ],
                reason="Fixture D response reason.",
                basis="Fixture D response basis.",
            )
        else:
            raise AssertionError(f"unexpected fixture schema: {schema}")
        return StructuredCallOutcome(
            kind=kind,
            status="success",
            response=response,
            result={"call_id": f"fixture:{kind}"},
            attempts=[],
            usage=[],
            cost={"eligible": True, "total_usd": 0.0, "attempts": []},
            context_budget={
                "mode": "provider_free_fixture",
                "projection_version": "stage-context-projection.v1",
                "prompt_characters": len(prompt),
                "estimated_prompt_tokens": (len(prompt) + 3) // 4,
                "provider_input_tokens": None,
                "context_window_tokens": None,
                "max_output_tokens": 8000,
                "truncation_applied": False,
                "projection_decision": "The test fixture used the complete serialized prompt.",
                "reason": "The provider-free test fixture records prompt size.",
                "basis": "test fixture runtime",
            },
            real_llm=False,
            reason="The provider-free test fixture returned a validated response.",
            basis="test fixture runtime",
        )


def test_v27_input_closure_is_loaded_and_role_separated() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    assert len(pair.nl_segments) >= 5
    assert pair.canonical_source_ir is not None
    assert pair.exact_source_inventory is not None
    assert pair.working_contract is not None
    assert pair.source_trace is not None
    assert pair.reference_inspection is not None
    assert pair.inspection_facts is not None
    assert pair.verify_facts is not None
    assert pair.smt_facts is not None
    assert pair.context_manifest is not None

    roles = {item.role for item in pair.context_manifest.artifacts}
    assert {
        "natural_language",
        "plantuml_source",
        "fcstm_model",
        "canonical_source_ir",
        "source_inventory",
        "working_contract",
        "source_trace",
        "reference_inspection_facts",
        "inspection_equivalent_facts",
        "verify_facts",
        "smt_facts",
    } <= roles
    assert pair.context_manifest.manifest_hash.startswith("sha256:")
    assert pair.hashes["canonical"] != pair.hashes["fcstm"]
    assert pair.canonical_source_ir.source_format == "plantuml"
    assert pair.exact_source_inventory.transitions
    assert pair.inspection_facts.transitions
    assert pair.verify_facts.terminal_state == "completed"
    assert pair.smt_facts.solver_status == "not_run"


def test_representative_v27_predecessor_pairs_have_complete_input_closure() -> None:
    for pair_id in ("0004", "0023", "0029", "0035", "0046", "0053"):
        pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
        assert pair.context_manifest is not None
        assert pair.canonical_source_ir is not None
        assert pair.exact_source_inventory is not None
        assert pair.working_contract is not None
        assert pair.source_trace is not None
        assert pair.reference_inspection is not None
        assert pair.inspection_facts is not None
        assert pair.verify_facts is not None
        assert pair.smt_facts is not None


def test_owned_fcstm_parser_preserves_semicolon_only_transitions() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    parsed = parse_fcstm(pair.fcstm_text)
    assert len(parsed.transitions) == 4
    assert {item.target for item in parsed.transitions} >= {
        "PumpControl",
        "PumpState",
        "WaterState",
        "MethaneState",
    }


def test_microwave_pair_keeps_source_and_closed_model_roles_separate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0035")

    assert pair.exact_source_inventory is not None
    assert len(pair.exact_source_inventory.states) == 6
    assert len(pair.exact_source_inventory.transitions) == 15
    assert len(pair.model.states) == 8
    assert len(pair.model.transitions) == 16
    assert pair.context_manifest is not None
    roles = {item.role for item in pair.context_manifest.artifacts}
    assert {"canonical_source_ir", "source_inventory", "fcstm_model", "inspection_equivalent_facts"} <= roles


def test_representative_pairs_staged_fixture_smoke(tmp_path: Path) -> None:
    for pair_id in ("0004", "0023", "0029", "0035", "0046", "0053"):
        pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
        runtime = FixtureStructuredRuntime()
        cell = _method_cell(
            pair=pair,
            round_index=1,
            runtime=runtime,
            previous=[],
            output_root=tmp_path / pair_id,
        )
        assert len(runtime.prompts) == 4
        assert cell["context_manifest"]["manifest_hash"] == pair.context_manifest.manifest_hash
        assert cell["evidence_records"]
        assert all(item["reason"] and item["basis"] for item in cell["stage_receipts"])
        assert all(item["input_manifest_hash"] == pair.context_manifest.manifest_hash for item in cell["stage_receipts"])


def test_method_context_excludes_historical_case_run_payloads() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    payload = context_payload(pair)
    case_report = payload["case_report"]
    assert case_report is not None
    case_fields = set(case_report["payload"])
    assert "comparison" not in case_fields
    assert "stage_lineage" not in case_fields
    assert "llm" not in case_fields
    assert "review" not in case_fields
    assert "canonical_sha256" in case_fields
    assert "fcstm_sha256" in case_fields


def test_incomplete_three_file_surface_is_rejected(tmp_path: Path) -> None:
    pair_dir = tmp_path / "pairs" / "0000"
    pair_dir.mkdir(parents=True)
    (pair_dir / "nl.txt").write_text("1 requirement", encoding="utf-8")
    (pair_dir / "plantuml.puml").write_text("@startuml\n@enduml\n", encoding="utf-8")
    (pair_dir / "fcstm.fcstm").write_text("state A\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="incomplete v27 input closure"):
        load_pair(pair_dir)


def test_staged_method_receives_full_context_and_writes_stage_receipts(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    runtime = FixtureStructuredRuntime()
    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        previous=[],
        output_root=tmp_path,
    )

    assert [kind for kind, _ in runtime.prompts] == [
        "nl_contract_extraction",
        "source_grounding",
        "model_grounding",
        "d_adjudication",
    ]
    prompts = dict(runtime.prompts)
    for prompt in prompts.values():
        assert "context_manifest" in prompt
        assert "artifact_refs" in prompt
        assert "source_roles" in prompt
        assert "frozen ledger answers" in prompt
        assert "baseline hit/FP results" in prompt
    assert '"numbered_nl": [' in prompts["nl_contract_extraction"]
    assert '"working_contract": {' in prompts["nl_contract_extraction"]
    assert '"fcstm_model": {' not in prompts["nl_contract_extraction"]
    assert '"plantuml_source": {' in prompts["source_grounding"]
    assert '"canonical_source_ir": {' in prompts["source_grounding"]
    assert '"exact_source_inventory": {' in prompts["source_grounding"]
    assert '"working_contract": {' in prompts["source_grounding"]
    assert '"source_trace": {' in prompts["source_grounding"]
    assert '"fcstm_model": {' not in prompts["source_grounding"]
    assert '"fcstm_model": {' in prompts["model_grounding"]
    assert '"reference_inspection_facts": {' in prompts["model_grounding"]
    assert '"inspection_equivalent_facts": {' in prompts["model_grounding"]
    assert '"verify_facts": {' in prompts["model_grounding"]
    assert '"smt_facts": {' in prompts["model_grounding"]
    assert '"plantuml_source": {' not in prompts["model_grounding"]
    assert '"dossier_input_policy": {' in prompts["d_adjudication"]
    assert '"plantuml_source": {' not in prompts["d_adjudication"]
    assert '"fcstm_model": {' not in prompts["d_adjudication"]

    receipt_names = [item["stage_name"] for item in cell["stage_receipts"]]
    for required in (
        "prepare",
        "nl_contract_extraction",
        "source_grounding",
        "model_grounding",
        "exact_binding",
        "predicate_compilation",
        "backend_execution",
        "d_adjudication",
        "w_publication",
    ):
        assert required in receipt_names
    assert all(item["input_manifest_hash"] == pair.context_manifest.manifest_hash for item in cell["stage_receipts"])
    assert all(item["reason"] and item["basis"] for item in cell["stage_receipts"])
    assert all(item["context_budget"]["reason"] and item["context_budget"]["basis"] for item in cell["stage_receipts"])
    llm_budgets = [
        item["context_budget"]
        for item in cell["stage_receipts"]
        if item["context_budget"]["mode"] == "structured_llm"
        or item["context_budget"]["mode"] == "provider_free_fixture"
    ]
    assert llm_budgets
    assert all(item["prompt_characters"] > 0 for item in llm_budgets)
    assert all(item["truncation_applied"] is False for item in llm_budgets)
    assert len(cell["llm_calls"]) == 4
    assert cell["context_manifest"]["manifest_hash"] == pair.context_manifest.manifest_hash
    assert cell["stage_outputs"]["nl_contract_extraction"]["reason"]
    assert cell["stage_outputs"]["source_grounding"]["basis"]
    assert cell["stage_outputs"]["model_grounding"]["reason"]
    assert all("l_level" not in record for record in cell["evidence_records"])
    for item in cell["stage_receipts"]:
        StageReceipt.model_validate(item)


def test_d_coverage_correction_is_in_node_and_no_silent_drop(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    runtime = FixtureStructuredRuntime(
        include_second_candidate=True,
        omit_second_d_decision=True,
    )

    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        previous=[],
        output_root=tmp_path,
    )

    assert runtime.d_call_count == 2
    assert [kind for kind, _ in runtime.prompts][-2:] == [
        "d_adjudication",
        "d_adjudication_correction",
    ]
    d_output = cell["stage_outputs"]["d_adjudication"]
    assert {
        decision["obligation_id"] for decision in d_output["decisions"]
    } == {"0000:r1:i0", "0000:r1:i1"}
    d_receipt = next(
        item for item in cell["stage_receipts"] if item["stage_name"] == "d_adjudication"
    )
    assert d_receipt["status"] == "completed"
    assert not any(
        error.get("stage") in {"d_adjudication", "d_adjudication_correction"}
        for error in cell["errors"]
    )
    assert len(cell["evidence_records"]) == 2
    assert all(record["semantic_adjudication"] for record in cell["evidence_records"])


def test_large_working_contract_is_role_scoped_before_prompt_serialization(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    runtime = FixtureStructuredRuntime()
    _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        previous=[],
        output_root=tmp_path,
    )

    assert max(len(prompt) for _, prompt in runtime.prompts) < 700_000
    model_prompt = dict(runtime.prompts)["model_grounding"]
    assert '"elements": [' in model_prompt
    assert '"excluded_element_ids": {' in model_prompt


def test_full_live_runner_requires_explicit_review_gate() -> None:
    with pytest.raises(RuntimeError, match="allow_live=True"):
        run_experiment(
            report_root=REPORT_ROOT,
            ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
            output_dir=PAPER_ROOT / "runs" / "should-not-start",
            profile="gpt-5.6-luna",
            allow_live=False,
        )


def test_full_live_runner_requires_second_explicit_gate() -> None:
    with pytest.raises(RuntimeError, match="allow_full_live=True"):
        run_experiment(
            report_root=REPORT_ROOT,
            ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
            output_dir=PAPER_ROOT / "runs" / "should-not-start-without-subset",
            profile="gpt-5.6-luna",
            allow_live=True,
        )


def test_live_runner_caps_diagnostic_subset_at_six_pairs() -> None:
    with pytest.raises(RuntimeError, match="capped at six"):
        run_experiment(
            report_root=REPORT_ROOT,
            ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
            output_dir=PAPER_ROOT / "runs" / "should-not-start-over-five",
            profile="gpt-5.6-luna",
            allow_live=True,
            pair_ids=["0000", "0001", "0002", "0003", "0004", "0005", "0006"],
        )


def test_live_runner_rejects_sol_during_luna_construction() -> None:
    with pytest.raises(RuntimeError, match="Sol execution is outside"):
        run_experiment(
            report_root=REPORT_ROOT,
            ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
            output_dir=PAPER_ROOT / "runs" / "should-not-start-sol",
            profile="gpt-5.6-sol",
            allow_live=True,
            pair_ids=["0004"],
        )
