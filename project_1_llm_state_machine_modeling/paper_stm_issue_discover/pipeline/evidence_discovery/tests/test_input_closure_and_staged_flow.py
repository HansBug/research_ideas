from __future__ import annotations

import json
from pathlib import Path

import pytest
from pipeline.evidence_discovery.inputs import load_pair, parse_fcstm
from pipeline.evidence_discovery.inputs.context import (
    build_numbered_nl_segments,
    context_payload,
    prompt_context_payload,
)
from pipeline.evidence_discovery.orchestration.runner import (
    _method_cell,
    run_experiment,
)
from pipeline.evidence_discovery.orchestration.runtime import (
    MAX_STRUCTURED_OUTPUT_TOKENS,
    StructuredCallOutcome,
)
from pipeline.evidence_discovery.semantics import (
    D_SYSTEM_PROMPT,
    DISCOVERY_GROUNDING_SYSTEM_PROMPT,
    DAdjudicationResponse,
    ContractBindingHint,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    StageReceipt,
    build_contract_prompt,
    fallback_contracts,
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
        duplicate_first_d_decision: bool = False,
    ) -> None:
        self.prompts: list[tuple[str, str]] = []
        self.include_second_candidate = include_second_candidate
        self.omit_second_d_decision = omit_second_d_decision
        self.duplicate_first_d_decision = duplicate_first_d_decision
        self.d_call_count = 0

    def call(self, *, kind, schema, system_prompt, prompt, artifact_id, **kwargs):
        recorded_kind = (
            "contract_structure_contrast"
            if artifact_id.endswith("/contract_structure_contrast")
            else "behavior_consequence"
            if artifact_id.endswith("/behavior_consequence")
            else kind
        )
        self.prompts.append((recorded_kind, prompt))
        pair_id = artifact_id.split("/")[1]
        if schema is NLContractResponse:
            context_marker = "Stage-scoped context projection and complete artifact manifest:\n"
            context_start = prompt.index(context_marker) + len(context_marker)
            context, _ = json.JSONDecoder().raw_decode(prompt[context_start:])
            segment_id = context["numbered_nl"][0]["segment_id"]
            segment = next(
                item
                for item in load_pair(REPORT_ROOT / "pairs" / pair_id).nl_segments
                if item.segment_id == segment_id
            )
            response = NLContractResponse(
                contracts=[
                    NLContract(
                        contract_id=f"NL-CONTRACT-{segment_id}",
                        segment_id=segment_id,
                        quote=segment.text,
                        normative_statement=segment.text,
                        locus_kind="transition",
                        locus_names=("Synthetic.Source", "Synthetic.Target"),
                        property="transition_endpoints",
                        expected_direction="must_exist",
                        violation_direction="missing",
                        evidence_types=("source_identity", "transition_fact"),
                        binding_hints=(
                            ContractBindingHint(
                                role="source",
                                value="Synthetic.Source",
                                source_ref=segment_id,
                                reason="Fixture exact transition source.",
                                basis="provider-free source binding",
                            ),
                            ContractBindingHint(
                                role="target",
                                value="Synthetic.Target",
                                source_ref=segment_id,
                                reason="Fixture exact transition target.",
                                basis="provider-free target binding",
                            ),
                        ),
                        scope="source-supplied scope",
                        source_refs=[f"nl:{segment_id}"],
                        reason="Fixture contract reason.",
                        basis="Fixture numbered NL basis.",
                    )
                ],
                segment_disposition={segment_id: "covered"},
                reason="Fixture contract response reason.",
                basis="Fixture contract response basis.",
            )
        elif issubclass(schema, GroundingResponse):
            pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
            existing_endpoints = {
                (transition.source, transition.target)
                for transition in pair.model.transitions
            }
            missing_endpoints = [
                (source, target)
                for source in pair.model.states
                for target in pair.model.states
                if source.ref != target.ref
                and (source.name, target.name) not in existing_endpoints
            ]
            assert len(missing_endpoints) >= 2
            source, target = missing_endpoints[0]
            candidates = [
                {
                    "contract_id": "NL-CONTRACT-NL1",
                    "locus_kind": "transition",
                    "locus_names": ["Synthetic.Source", "Synthetic.Target"],
                    "property": "transition_endpoints",
                    "violation_direction": "missing",
                    "evidence_types": ["closed_model_inventory", "transition_fact"],
                    "title": "Fixture grounded transition",
                    "requirement_quote": "The supplied source clause.",
                    "predicate_id": "S2",
                    "predicate_inputs": {
                        "source": source.name,
                        "target": target.name,
                        "scope": "closed_fcstm",
                    },
                    "element_refs": [source.ref, target.ref],
                    "source_refs": ["nl:NL1"],
                    "expected": "The required transition is present.",
                    "observed": "The required transition is absent.",
                    "strongest_rebuttal": "none",
                    "reason": "Fixture branch reason.",
                    "basis": "Fixture exact FCSTM endpoint binding and missing-edge basis.",
                }
            ]
            if self.include_second_candidate:
                second_source, second_target = missing_endpoints[1]
                candidates.append(
                    {
                        "contract_id": "NL-CONTRACT-NL1",
                        "locus_kind": "transition",
                        "locus_names": ["Synthetic.Source", "Synthetic.OtherTarget"],
                        "property": "transition_endpoints",
                        "violation_direction": "missing",
                        "evidence_types": ["closed_model_inventory", "transition_fact"],
                        "title": "Fixture grounded second transition",
                        "requirement_quote": "The second supplied source clause.",
                        "predicate_id": "S2",
                        "predicate_inputs": {
                            "source": second_source.name,
                            "target": second_target.name,
                            "scope": "closed_fcstm",
                        },
                        "element_refs": [second_source.ref, second_target.ref],
                        "source_refs": ["nl:NL2"],
                        "expected": "The second required transition is present.",
                        "observed": "The second required transition is absent.",
                        "strongest_rebuttal": "none",
                        "reason": "Fixture second branch reason.",
                        "basis": "Fixture second exact FCSTM endpoint binding and missing-edge basis.",
                    }
                )
            response = schema(
                lens=(
                    "behavior_consequence"
                    if artifact_id.endswith("/behavior_consequence")
                    else "contract_structure_contrast"
                ),
                additional_contracts=[],
                candidates=candidates,
                unresolved=[],
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
            if self.duplicate_first_d_decision and kind == "d_adjudication":
                decision_ids.append(f"{pair_id}:r1:i0")
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
                "max_output_tokens": kwargs.get(
                    "max_output_tokens", MAX_STRUCTURED_OUTPUT_TOKENS
                ),
                "truncation_applied": False,
                "projection_decision": "The test fixture used the complete serialized prompt.",
                "reason": "The provider-free test fixture records prompt size.",
                "basis": "test fixture runtime",
            },
            real_llm=False,
            reason="The provider-free test fixture returned a validated response.",
            basis="test fixture runtime",
        )


def test_complete_input_closure_is_loaded_and_role_separated() -> None:
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


def test_0029_numbered_nl_does_not_split_numeric_quantities() -> None:
    nl_path = REPORT_ROOT / "pairs" / "0029" / "nl.txt"
    text = nl_path.read_text(encoding="utf-8")

    segments = build_numbered_nl_segments(text)

    assert [item.segment_id for item in segments] == [f"NL{number}" for number in range(1, 14)]
    assert "25 meters" in next(item.text for item in segments if item.segment_id == "NL5")
    assert "15 meters" in next(item.text for item in segments if item.segment_id == "NL7")
    assert "2 kilometers" in next(item.text for item in segments if item.segment_id == "NL4")
    assert "0.7 kilometers" in next(item.text for item in segments if item.segment_id == "NL8")
    assert all(item.basis.startswith("nl-segmentation.v2") for item in segments)
    for item in segments:
        assert text[item.raw_start :].startswith(str(item.source_number))
        assert item.raw_start < item.raw_end <= len(text)


def test_0046_line_start_markers_without_periods_are_preserved() -> None:
    nl_path = REPORT_ROOT / "pairs" / "0046" / "nl.txt"

    segments = build_numbered_nl_segments(nl_path.read_text(encoding="utf-8"))

    assert [item.segment_id for item in segments] == ["NL1", "NL2", "NL3", "NL4"]
    assert all("physical-line-start" in item.basis for item in segments)


def test_line_start_numeric_quantities_do_not_become_source_markers() -> None:
    text = (
        "1. First clause starts here.\n"
        "25 meters remains a continuation quantity.\n"
        "2 Second clause starts here.\n"
        "15 meters remains another continuation quantity.\n"
        "3. Third clause starts here."
    )

    segments = build_numbered_nl_segments(text)

    assert [item.segment_id for item in segments] == ["NL1", "NL2", "NL3"]
    assert "25 meters" in segments[0].text
    assert "15 meters" in segments[1].text


def test_single_line_numbered_nl_uses_constrained_legacy_delimiters() -> None:
    text = (
        "1. First clause keeps 25 meters and 0.7 kilometers. "
        "2. Second clause keeps 15 meters and 2 kilometers. "
        "3 when the final explicit legacy clause applies"
    )

    segments = build_numbered_nl_segments(text)

    assert [item.segment_id for item in segments] == ["NL1", "NL2", "NL3"]
    assert "25 meters" in segments[0].text
    assert "0.7 kilometers" in segments[0].text
    assert "15 meters" in segments[1].text
    assert "2 kilometers" in segments[1].text
    assert segments[2].text == "when the final explicit legacy clause applies"
    assert all("constrained one-line legacy delimiter" in item.basis for item in segments)


def test_0029_contract_extraction_is_one_whole_cell_call() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")

    prompt = build_contract_prompt(pair, 1)

    assert "Stage: contract-extraction" in prompt
    assert "Contract chunk:" not in prompt
    assert all(f'"segment_id": "NL{number}"' in prompt for number in range(1, 14))


def test_contract_fallback_preserves_all_numbered_nl_without_merge_protocol() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    fallback = fallback_contracts(pair, "provider-free whole-cell fixture")

    assert [item.segment_id for item in fallback.contracts] == [
        f"NL{number}" for number in range(1, 14)
    ]
    assert list(fallback.segment_disposition) == [f"NL{number}" for number in range(1, 14)]
    assert len({item.contract_id for item in fallback.contracts}) == 13
    assert fallback.reason and fallback.basis


def test_representative_diagnostic_cases_have_complete_input_closure() -> None:
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


def test_owned_fcstm_parser_preserves_forced_source_marker() -> None:
    parsed = parse_fcstm("state Root;\nstate Target;\n!Root -> Target : /Closed;")

    assert len(parsed.transitions) == 1
    assert parsed.transitions[0].source == "!Root"
    assert parsed.transitions[0].target == "Target"
    assert parsed.transitions[0].triggers == ("Closed",)


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


def test_representative_inspection_routes_use_exact_hierarchical_loci() -> None:
    expected_leaf_names = {
        "0004": {"EmergencyStopping", "Stopping"},
        "0023": {"PumpState", "WaterState", "MethaneState"},
        "0053": {"PumpState", "WaterState", "MethaneState"},
    }
    for pair_id, expected_names in expected_leaf_names.items():
        pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
        facts = pair.inspection_facts
        assert facts is not None
        leaf_refs = {
            diagnostic.refs[0]
            for diagnostic in facts.diagnostics
            if diagnostic.code == "LEAF_WITHOUT_OUTGOING"
        }
        leaf_names = {
            state.name for state in facts.states if state.state_ref in leaf_refs
        }
        assert expected_names <= leaf_names
        assert not any(
            state.is_composite and state.state_ref in leaf_refs
            for state in facts.states
        )

    pair_0029 = load_pair(REPORT_ROOT / "pairs" / "0029")
    facts_0029 = pair_0029.inspection_facts
    assert facts_0029 is not None
    collision_ref = next(
        state.state_ref
        for state in facts_0029.states
        if state.name == "CollisionAvoidance"
    )
    assert collision_ref not in {
        diagnostic.refs[0]
        for diagnostic in facts_0029.diagnostics
        if diagnostic.code == "LEAF_WITHOUT_OUTGOING"
    }
    assert any(
        diagnostic.code == "STATE_UNREACHABLE_FROM_INITIAL"
        and diagnostic.refs == (collision_ref,)
        for diagnostic in facts_0029.diagnostics
    )

    pair_0035 = load_pair(REPORT_ROOT / "pairs" / "0035")
    facts_0035 = pair_0035.inspection_facts
    assert facts_0035 is not None
    assert next(state for state in facts_0035.states if state.name == "DoorShut").reachable_from_initial is False

    pair_0046 = load_pair(REPORT_ROOT / "pairs" / "0046")
    facts_0046 = pair_0046.inspection_facts
    assert facts_0046 is not None
    intercepted = next(item for item in facts_0046.event_consumers if item.event == "Intercepted")
    assert intercepted.consumer_transition_refs
    assert not intercepted.reachable_consumer_transition_refs


def test_generated_fact_paths_are_materialized_and_hash_addressed() -> None:
    import hashlib

    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    assert pair.context_manifest is not None
    generated_roles = {
        "source_inventory",
        "inspection_equivalent_facts",
        "verify_facts",
        "smt_facts",
    }
    for artifact in pair.context_manifest.artifacts:
        if artifact.role not in generated_roles:
            continue
        path = Path(artifact.path)
        assert path.is_file(), artifact.role
        digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == artifact.sha256, artifact.role


def test_representative_pairs_staged_fixture_smoke(tmp_path: Path) -> None:
    calls_per_cell: list[int] = []
    for pair_id in ("0004", "0023", "0029", "0035", "0046", "0053"):
        pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
        runtime = FixtureStructuredRuntime()
        cell = _method_cell(
            pair=pair,
            round_index=1,
            runtime=runtime,
            output_root=tmp_path / pair_id,
        )
        assert len(runtime.prompts) == 4
        calls_per_cell.append(len(runtime.prompts))
        assert sum(
            kind == "contract_extraction"
            for kind, _ in runtime.prompts
        ) == 1
        assert cell["context_manifest"]["manifest_hash"] == pair.context_manifest.manifest_hash
        assert cell["evidence_records"]
        execute_output = cell["stage_outputs"]["execute_batch"]
        assert execute_output["llm_candidate_count"] == 1
        assert execute_output["exact_s2_scout_candidate_count"] == 0
        assert execute_output["exact_s2_scout_receipts"] == []
    assert calls_per_cell == [4, 4, 4, 4, 4, 4]
    assert sum(calls_per_cell) * 3 == 72
    assert all(item["reason"] and item["basis"] for item in cell["stage_receipts"])
    assert all(item["input_manifest_hash"] == pair.context_manifest.manifest_hash for item in cell["stage_receipts"])
    for branch in cell["stage_outputs"]["discovery_grounding"]["branches"]:
        assert branch["additional_contracts"] == []
        assert branch["unresolved"] == []
        assert "contract_dispositions" not in branch


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
    assert case_fields == {"case_id", "case_index", "source_hashes", "artifact_status"}
    assert {"canonical_source", "closed_model"}.issubset(
        case_report["payload"]["source_hashes"]
    )

    grounding = prompt_context_payload(pair, stage="discovery_grounding")
    source_trace_text = json.dumps(grounding["source_trace"], sort_keys=True)
    assert "required_for_issue_ids" not in source_trace_text


def test_provider_context_uses_public_artifact_schema_names() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    for stage in (
        "nl_contract_extraction",
        "discovery_grounding",
        "d_adjudication",
    ):
        payload = prompt_context_payload(pair, stage=stage)
        serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        assert "paper1" not in serialized.casefold()
        working_refs = [
            item
            for item in payload["artifact_refs"]
            if item["role"] == "working_contract"
        ]
        assert len(working_refs) == 1
        assert working_refs[0]["schema_version"] == "working-model-contract.v2"
        if "working_contract" in payload:
            assert payload["working_contract"]["ref"]["schema_version"] == (
                "working-model-contract.v2"
            )


def test_incomplete_three_file_surface_is_rejected(tmp_path: Path) -> None:
    pair_dir = tmp_path / "pairs" / "0000"
    pair_dir.mkdir(parents=True)
    (pair_dir / "nl.txt").write_text("1 requirement", encoding="utf-8")
    (pair_dir / "plantuml.puml").write_text("@startuml\n@enduml\n", encoding="utf-8")
    (pair_dir / "fcstm.fcstm").write_text("state A\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="incomplete method input closure"):
        load_pair(pair_dir)


def test_staged_method_receives_full_context_and_writes_stage_receipts(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    runtime = FixtureStructuredRuntime()
    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        output_root=tmp_path,
    )

    assert [kind for kind, _ in runtime.prompts] == [
        "contract_extraction",
        "contract_structure_contrast",
        "behavior_consequence",
        "d_adjudication",
    ]
    prompts = dict(runtime.prompts)
    for prompt in prompts.values():
        assert "context_manifest" in prompt
        assert "artifact_refs" in prompt
        assert "source_roles" in prompt
        assert "evaluation ground truth" in prompt
        assert "evaluation scores or error classifications" in prompt
        assert str(pair.pair_dir) not in prompt
        assert '"example_id"' not in prompt
        assert '"seed_id"' not in prompt
        assert '"artifact_bindings"' not in prompt
        assert '"canonical_path"' not in prompt
        assert '"fcstm_path"' not in prompt
    assert '"numbered_nl": [' in prompts["contract_extraction"]
    assert '"working_contract": {' in prompts["contract_extraction"]
    assert '"fcstm_model": {' not in prompts["contract_extraction"]
    for grounding_stage in (
        "contract_structure_contrast",
        "behavior_consequence",
    ):
        assert '"plantuml_source": {' in prompts[grounding_stage]
        assert '"canonical_source_ir": {' in prompts[grounding_stage]
        assert '"exact_source_inventory": {' in prompts[grounding_stage]
        assert '"working_contract": {' in prompts[grounding_stage]
        assert '"source_trace": {' in prompts[grounding_stage]
        assert '"fcstm_model": {' in prompts[grounding_stage]
        assert '"reference_inspection_facts": {' in prompts[grounding_stage]
        assert '"inspection_equivalent_facts": {' in prompts[grounding_stage]
        assert '"verify_facts": {' in prompts[grounding_stage]
        assert '"smt_facts": {' in prompts[grounding_stage]
        assert '"projection_version": "contract-grounding-projection.v2"' in prompts[grounding_stage]
        assert '"full_contract_response_hash": "sha256:' in prompts[grounding_stage]
        assert '"contract_id": "NL-CONTRACT-NL1"' in prompts[grounding_stage]
        assert "Fixture contract reason." not in prompts[grounding_stage]
        assert "Fixture contract response reason." not in prompts[grounding_stage]
        assert "Use V4(initial_scope) for a supplied finite deadlock-frontier" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
        assert "Use G1 for a finite path-existence or unreachable-target claim" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
        assert "Use S1 only for closed-model declaration membership" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert '"dossier_input_policy": {' in prompts["d_adjudication"]
    assert '"plantuml_source": {' not in prompts["d_adjudication"]
    assert '"fcstm_model": {' not in prompts["d_adjudication"]
    assert "an unsupported or W1-only predicate does not erase a precise issue" in D_SYSTEM_PROMPT

    receipt_names = [item["stage_name"] for item in cell["stage_receipts"]]
    assert receipt_names == [
        "prepare",
        "contract_extraction",
        "discovery_grounding",
        "execute_batch",
        "d_adjudication",
        "validate_d",
        "publish",
    ]
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
    assert all(
        item["max_output_tokens"] == MAX_STRUCTURED_OUTPUT_TOKENS
        for item in llm_budgets
    )
    grounding_receipt = next(
        item for item in cell["stage_receipts"]
        if item["stage_name"] == "discovery_grounding"
    )
    assert (
        grounding_receipt["context_budget"]["projection_version"]
        == "complementary-grounding-projection.v2"
    )
    assert len(cell["llm_calls"]) == 4
    assert cell["context_manifest"]["manifest_hash"] == pair.context_manifest.manifest_hash
    assert cell["stage_outputs"]["contract_extraction"]["reason"]
    grounding_branches = cell["stage_outputs"]["discovery_grounding"]["branches"]
    assert [branch["lens"] for branch in grounding_branches] == [
        "contract_structure_contrast",
        "behavior_consequence",
    ]
    assert all(branch["reason"] and branch["basis"] for branch in grounding_branches)
    assert all("l_level" not in record for record in cell["evidence_records"])
    for item in cell["stage_receipts"]:
        StageReceipt.model_validate(item)


def test_one_grounding_failure_does_not_erase_closed_w1_release(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class OneBranchFailureRuntime(FixtureStructuredRuntime):
        def call(self, **kwargs):
            outcome = super().call(**kwargs).model_copy(update={"real_llm": True})
            artifact_id = kwargs["artifact_id"]
            if artifact_id.endswith("/contract_structure_contrast"):
                return outcome.model_copy(
                    update={
                        "status": "failed_with_receipt",
                        "response": None,
                        "result": {"error": "fixture source grounding provider failure"},
                        "reason": "The source lens failed in this provider-shaped fixture.",
                        "basis": "provider-free branch-local failure fixture",
                    }
                )
            if artifact_id.endswith("/behavior_consequence"):
                response = outcome.response.model_copy(
                    update={
                        "candidates": [
                            candidate.model_copy(
                                update={"predicate_id": None, "predicate_inputs": {}}
                            )
                            for candidate in outcome.response.candidates
                        ]
                    }
                )
                return outcome.model_copy(update={"response": response})
            return outcome

    runtime = OneBranchFailureRuntime()
    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        output_root=tmp_path,
    )

    assert cell["eligible"] is True
    assert cell["status"] == "completed_with_diagnostics"
    assert len(cell["report_issue_clusters"]) == 1
    assert cell["report_issue_clusters"][0]["witness_level"] == "W1"
    assert cell["report_issue_clusters"][0]["d_level"] == "D2"
    assert any(
        error.get("stage") == "discovery_grounding"
        and error.get("lens") == "contract_structure_contrast"
        for error in cell["errors"]
    )


def test_sparse_grounding_omission_is_normal_but_unknown_derived_segment_is_audited(
    tmp_path: Path,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class SparseGroundingRuntime(FixtureStructuredRuntime):
        def call(self, **kwargs):
            outcome = super().call(**kwargs).model_copy(update={"real_llm": True})
            if kwargs["schema"] is NLContractResponse:
                first = outcome.response.contracts[0]
                second = first.model_copy(
                    update={"contract_id": "NL-CONTRACT-NL1-SECOND"}
                )
                response = outcome.response.model_copy(
                    update={"contracts": [first, second]}
                )
                return outcome.model_copy(update={"response": response})
            if not issubclass(kwargs["schema"], GroundingResponse):
                return outcome
            unknown = NLContract(
                contract_id="NL-CONTRACT-NL999-DERIVED-UNKNOWN",
                segment_id="NL999",
                quote="A structurally valid but unsupplied segment fixture.",
                normative_statement="The unavailable segment would require a transition.",
                locus_kind="transition",
                locus_names=("Synthetic.Source", "Synthetic.Target"),
                property="transition_endpoints",
                expected_direction="must_exist",
                violation_direction="missing",
                evidence_types=("transition_fact",),
                binding_hints=(
                    ContractBindingHint(
                        role="source",
                        value="Synthetic.Source",
                        source_ref="NL999",
                        reason="Fixture exact transition source.",
                        basis="provider-free unknown-segment source binding",
                    ),
                    ContractBindingHint(
                        role="target",
                        value="Synthetic.Target",
                        source_ref="NL999",
                        reason="Fixture exact transition target.",
                        basis="provider-free unknown-segment target binding",
                    ),
                ),
                scope="fixture scope",
                source_refs=("nl:NL999",),
                reason="The fixture deliberately names an unavailable segment.",
                basis="provider-free unknown derived segment fixture",
            )
            response = outcome.response.model_copy(
                update={"additional_contracts": [unknown]}
            )
            return outcome.model_copy(update={"response": response})

    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=SparseGroundingRuntime(),
        output_root=tmp_path,
    )

    grounding_receipt = next(
        item
        for item in cell["stage_receipts"]
        if item["stage_name"] == "discovery_grounding"
    )
    assert grounding_receipt["status"] == "completed_with_diagnostics"
    diagnostics = grounding_receipt["diagnostics"]
    assert any(
        item.get("class") == "unknown_additional_contract_segment"
        and item.get("segment_id") == "NL999"
        for item in diagnostics
    )
    assert cell["eligible"] is True
    assert cell["status"] == "completed_with_diagnostics"
    assert any(
        item.get("class") == "unknown_additional_contract_segment"
        for item in cell["errors"]
    )
    assert not any(
        item.get("class") == "exact_contract_accounting_incomplete"
        for item in diagnostics
    )


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


def test_d_duplicate_id_is_targeted_and_valid_decisions_remain_frozen(
    tmp_path: Path,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    runtime = FixtureStructuredRuntime(duplicate_first_d_decision=True)

    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        output_root=tmp_path,
    )

    validation = cell["stage_outputs"]["validate_d"]
    assert runtime.d_call_count == 2
    assert validation["initial_duplicate_ids"] == ["0000:r1:i0"]
    assert validation["repair_attempted"] is True
    assert validation["repair_missing_ids"] == []
    assert validation["repair_extra_ids"] == []
    assert validation["repair_duplicate_ids"] == []
    assert validation["repair_invalid_decisions"] == {}
    assert validation["final_unresolved_ids"] == []
    assert len(cell["evidence_records"]) == 1
    correction_prompt = next(
        prompt
        for kind, prompt in runtime.prompts
        if kind == "d_adjudication_correction"
    )
    assert 'duplicate_ids_to_repair:\n["0000:r1:i0"]' in correction_prompt
    assert '"obligation_id": "0000:r1:i0"' in correction_prompt


def test_large_working_contract_is_role_scoped_before_prompt_serialization(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    runtime = FixtureStructuredRuntime()
    _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        output_root=tmp_path,
    )

    assert max(len(prompt) for _, prompt in runtime.prompts) < 350_000
    grounding_prompt = dict(runtime.prompts)["behavior_consequence"]
    assert '"elements": {' in grounding_prompt
    assert '"source_to_model": [' in grounding_prompt
    assert '"capability_eligibility_detail_receipt": {' in grounding_prompt
    assert '"excluded_element_ids": {' not in grounding_prompt
    assert '"row_rationale_receipts": {' in grounding_prompt
    assert '"row_rationale_receipt": {' in grounding_prompt
    grounding_context = prompt_context_payload(pair, stage="discovery_grounding")
    grounding_context_text = json.dumps(
        grounding_context,
        ensure_ascii=False,
        sort_keys=True,
    )
    assert len(grounding_context_text) < 150_000
    assert grounding_context["prompt_projection_version"] == "stage-context-projection.v8"
    assert '"model_refs"' in grounding_context_text
    assert '"raw_ref"' in grounding_context_text
    for role in (
        "reference_inspection_facts",
        "inspection_equivalent_facts",
        "verify_facts",
        "smt_facts",
    ):
        assert role in grounding_context
    assert grounding_context["working_contract"]["payload"]["elements"]["source_to_model"]
    assert "review_subject" not in grounding_context["working_contract"]["payload"]
    assert "source_trace" in grounding_context
    transition_row = grounding_context["inspection_equivalent_facts"]["transitions"][0]
    for field_name in (
        "source",
        "target",
        "triggers",
        "guard",
        "effects",
        "line",
        "scope",
        "resolved_source_ref",
        "resolved_target_ref",
    ):
        assert field_name in transition_row


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


def test_live_runner_rejects_profile_outside_construction_protocol() -> None:
    with pytest.raises(RuntimeError, match="outside the frozen construction"):
        run_experiment(
            report_root=REPORT_ROOT,
            ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
            output_dir=PAPER_ROOT / "runs" / "should-not-start-sol",
            profile="gpt-5.6-sol",
            allow_live=True,
            pair_ids=["0004"],
        )
