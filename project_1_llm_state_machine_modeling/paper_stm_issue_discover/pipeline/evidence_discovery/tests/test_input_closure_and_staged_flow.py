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
    _contract_completion_required,
    _merge_contract_completion,
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
    ContractBindingHint,
    ContractCompletionResponse,
    DAdjudicationResponse,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    StageReceipt,
    build_contract_prompt,
    build_contract_completion_prompt,
    build_d_adjudication_batches,
    build_d_correction_prompt,
    build_d_adjudication_prompt,
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
        elif schema is ContractCompletionResponse:
            response = ContractCompletionResponse(
                additional_contracts=[],
                additional_transition_groups=[],
                reason="The provider-free completion fixture adds no semantic obligation.",
                basis="provider-free bounded completion fixture",
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
                marker = "repair_ids:\n"
                id_start = prompt.index(marker) + len(marker)
                decision_ids, _ = json.JSONDecoder().raw_decode(prompt[id_start:])
            elif kind == "d_adjudication":
                marker = "Required obligation IDs, exactly once each:\n"
                id_start = prompt.index(marker) + len(marker)
                decision_ids, _ = json.JSONDecoder().raw_decode(prompt[id_start:])
                if self.omit_second_d_decision:
                    decision_ids = decision_ids[:1]
            else:
                decision_ids = [f"{pair_id}:r1:i0"]
            if self.duplicate_first_d_decision and kind == "d_adjudication":
                decision_ids.append(decision_ids[0])
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


def test_contract_completion_unions_new_typed_rows_without_overwrite() -> None:
    """A low-count primary plan retains its rows while adding one new typed key."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    fallback = fallback_contracts(pair, "provider-free bounded completion fixture")
    primary = fallback.model_copy(
        update={
            "contracts": [fallback.contracts[0]],
            "segment_disposition": {fallback.contracts[0].segment_id: "covered"},
        }
    )
    additional = fallback.contracts[1].model_copy(
        update={"contract_id": "NL-CONTRACT-NL2-COMPLETION-FIXTURE"}
    )
    completion = ContractCompletionResponse(
        additional_contracts=[additional],
        additional_transition_groups=[],
        reason="The fixture supplies one independent omitted numbered-NL contract.",
        basis="provider-free bounded completion fixture",
    )

    assert _contract_completion_required(pair, primary) is True
    prompt = build_contract_completion_prompt(pair, 1, primary)
    assert "contract-completion-correction" in prompt
    assert "Primary typed plan" in prompt
    assert "evaluation ground truth" in prompt

    merged, diagnostics = _merge_contract_completion(pair, primary, completion)

    assert primary.contracts == [fallback.contracts[0]]
    assert len(merged.contracts) == 2
    assert merged.contracts[0].contract_id == fallback.contracts[0].contract_id
    assert merged.contracts[1].contract_id.startswith("NL-CONTRACT-NL2-DERIVED-")
    assert [item["class"] for item in diagnostics] == [
        "admitted_completion_contract"
    ]


def test_contract_completion_deduplicates_exact_primary_identity() -> None:
    """A completion response cannot revise a primary contract under a new ID."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    fallback = fallback_contracts(pair, "provider-free duplicate completion fixture")
    primary = fallback.model_copy(
        update={
            "contracts": [fallback.contracts[0]],
            "segment_disposition": {fallback.contracts[0].segment_id: "covered"},
        }
    )
    duplicate = fallback.contracts[0].model_copy(
        update={"contract_id": "NL-CONTRACT-NL1-DUPLICATE-COMPLETION"}
    )
    completion = ContractCompletionResponse(
        additional_contracts=[duplicate],
        additional_transition_groups=[],
        reason="The fixture deliberately repeats the primary typed identity.",
        basis="provider-free duplicate completion fixture",
    )

    merged, diagnostics = _merge_contract_completion(pair, primary, completion)

    assert merged.contracts == primary.contracts
    assert diagnostics[0]["class"] == "duplicate_completion_contract_semantic_key"


def test_contract_completion_checks_property_coverage_for_high_count_primary_plan() -> None:
    """Multiple primary contracts never prove every independent NL property is present."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    fallback = fallback_contracts(pair, "provider-free high-count completion fixture")
    extra_property = fallback.contracts[0].model_copy(
        update={
            "contract_id": "NL-CONTRACT-NL1-INDEPENDENT-PROPERTY",
            "property": "state_action",
            "state_role": "operating_state",
            "evidence_types": ("action_fact",),
        }
    )
    primary = fallback.model_copy(
        update={"contracts": [*fallback.contracts, extra_property]}
    )

    assert len(primary.contracts) >= len(pair.nl_segments)
    assert extra_property.property != fallback.contracts[0].property
    assert _contract_completion_required(pair, primary) is True
    prompt = build_contract_completion_prompt(pair, 1, primary)
    assert "property-coverage correction" in prompt
    assert "multiple independently violable obligations" in prompt


def test_real_low_count_contract_extraction_runs_one_completion_without_overwrite(
    tmp_path: Path,
) -> None:
    """A live-provenance primary plan gets one additive correction call."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class LiveCompletionRuntime(FixtureStructuredRuntime):
        """Return deterministic typed rows while exercising real-call provenance."""

        def call(self, **kwargs):
            outcome = super().call(**kwargs)
            if kwargs["schema"] is ContractCompletionResponse:
                omitted = fallback_contracts(
                    pair,
                    "live-provenance contract-completion fixture",
                ).contracts[1].model_copy(
                    update={"contract_id": "NL-CONTRACT-NL2-LIVE-COMPLETION"}
                )
                response = ContractCompletionResponse(
                    additional_contracts=[omitted],
                    additional_transition_groups=[],
                    reason="The fixture adds one omitted independently violable contract.",
                    basis="typed numbered-NL completion fixture",
                )
                return outcome.model_copy(
                    update={"response": response, "real_llm": True}
                )
            return outcome.model_copy(update={"real_llm": True})

    runtime = LiveCompletionRuntime()
    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        output_root=tmp_path,
    )

    assert [kind for kind, _ in runtime.prompts].count("contract_completion") == 1
    completion = cell["stage_outputs"]["contract_completion"]
    assert completion["triggered"] is True
    assert len(completion["admitted_contract_ids"]) == 1
    assert completion["merge_dispositions"][0]["class"] == "admitted_completion_contract"
    assert len(cell["stage_outputs"]["contract_extraction"]["contracts"]) == 1
    completion_receipt = next(
        item
        for item in cell["stage_receipts"]
        if item["stage_name"] == "contract_completion"
    )
    assert completion_receipt["status"] == "completed"
    assert completion_receipt["diagnostics"] == []
    grounding_prompts = [
        prompt
        for kind, prompt in runtime.prompts
        if kind in {"contract_structure_contrast", "behavior_consequence"}
    ]
    assert grounding_prompts
    assert all(
        completion["admitted_contract_ids"][0] in prompt
        for prompt in grounding_prompts
    )
    assert cell["status"] == "completed"


def test_contract_completion_unknown_segment_is_a_cell_diagnostic(
    tmp_path: Path,
) -> None:
    """Only an invalid completion identity propagates beyond merge audit."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class LiveInvalidCompletionRuntime(FixtureStructuredRuntime):
        """Return one completion row outside the current numbered-NL closure."""

        def call(self, **kwargs):
            outcome = super().call(**kwargs)
            if kwargs["schema"] is ContractCompletionResponse:
                invalid = fallback_contracts(
                    pair,
                    "provider-free invalid completion segment fixture",
                ).contracts[0].model_copy(
                    update={
                        "contract_id": "NL-CONTRACT-NL999-OUTSIDE-CLOSURE",
                        "segment_id": "NL999",
                    }
                )
                return outcome.model_copy(
                    update={
                        "response": ContractCompletionResponse(
                            additional_contracts=[invalid],
                            additional_transition_groups=[],
                            reason="The fixture intentionally violates segment closure.",
                            basis="provider-free invalid completion segment fixture",
                        ),
                        "real_llm": True,
                    }
                )
            return outcome.model_copy(update={"real_llm": True})

    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=LiveInvalidCompletionRuntime(),
        output_root=tmp_path,
    )

    completion_receipt = next(
        item
        for item in cell["stage_receipts"]
        if item["stage_name"] == "contract_completion"
    )
    assert completion_receipt["status"] == "completed_with_diagnostics"
    assert completion_receipt["diagnostics"][0]["class"] == (
        "unknown_completion_contract_segment"
    )
    assert cell["status"] == "completed_with_diagnostics"
    assert any(
        item.get("class") == "unknown_completion_contract_segment"
        for item in cell["errors"]
    )


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


def test_native_projection_preserves_semicolon_only_transitions() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    parsed = parse_fcstm(pair.fcstm_text)
    assert len(parsed.transitions) == 4
    assert {item.target for item in parsed.transitions} >= {
        "PumpControl",
        "PumpState",
        "WaterState",
        "MethaneState",
    }


def test_native_projection_preserves_forced_authored_provenance() -> None:
    parsed = parse_fcstm((REPORT_ROOT / "pairs" / "0004" / "fcstm.fcstm").read_text())

    forced = [item for item in parsed.transitions if item.is_forced]
    assert len(forced) == 1
    assert forced[0].source == "DoorsClosing"
    assert forced[0].target == "InMotion"
    assert forced[0].triggers == ("Closed_SendDeparted",)
    assert forced[0].ref.startswith("transition:forced:")


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
        "0053": {"UnspecifiedInitial"},
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
        if pair_id == "0053":
            unreachable_names = {
                state.name
                for state in facts.states
                if not state.reachable_from_initial
            }
            assert {"PumpState", "WaterState", "MethaneState"} <= unreachable_names

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
    assert "a predicate-null route, incomplete typed input, or unavailable execution does not erase a precise issue" in D_SYSTEM_PROMPT

    receipt_names = [item["stage_name"] for item in cell["stage_receipts"]]
    assert receipt_names == [
        "prepare",
        "contract_extraction",
        "contract_completion",
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
    llm_release = next(
        record
        for record in cell["report_issue_clusters"]
        if record["contract_id"].startswith("NL-CONTRACT-")
    )
    assert llm_release["witness_level"] == "W1"
    assert llm_release["d_level"] == "D2"
    domain_releases = [
        record
        for record in cell["report_issue_clusters"]
        if record["contract_id"].startswith("DOMAIN-INVARIANT-")
    ]
    assert domain_releases
    assert all(record["witness_level"] == "W2" for record in domain_releases)
    assert any(
        error.get("stage") == "discovery_grounding"
        and error.get("lens") == "contract_structure_contrast"
        for error in cell["errors"]
    )


def test_unresolved_w0_record_is_an_eligible_diagnostic_result(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class UnresolvedRuntime(FixtureStructuredRuntime):
        def call(self, **kwargs):
            outcome = super().call(**kwargs).model_copy(update={"real_llm": True})
            if isinstance(outcome.response, GroundingResponse):
                response = outcome.response.model_copy(
                    update={
                        "candidates": [
                            candidate.model_copy(
                                update={
                                    "predicate_id": None,
                                    "predicate_inputs": {},
                                    "element_refs": [],
                                }
                            )
                            for candidate in outcome.response.candidates
                        ]
                    }
                )
                return outcome.model_copy(update={"response": response})
            if not isinstance(outcome.response, DAdjudicationResponse):
                return outcome
            response = outcome.response.model_copy(
                update={
                    "decisions": [
                        decision.model_copy(
                            update={
                                "grounding": "unresolved",
                                "strongest_defeater": "The supplied fixture cannot close the semantic reading.",
                                "defeater_kind": "undercutting",
                                "defeater_disposition": "unresolved",
                            }
                        )
                        for decision in outcome.response.decisions
                    ]
                }
            )
            return outcome.model_copy(update={"response": response})

    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=UnresolvedRuntime(),
        output_root=tmp_path,
    )

    assert cell["eligible"] is True
    assert cell["status"] == "completed"
    assert cell["eligibility_reasons"] == [
        "real_contract_output",
        "at_least_one_completed_grounding_lens",
        "auditable_semantic_result",
        "method_receipt_complete",
    ]
    assert cell["evidence_records"]
    assert {record["d_level"] for record in cell["evidence_records"]} == {
        "D_UNRESOLVED"
    }
    assert any(
        record["witness_level"] == "W0"
        and record["contract_id"].startswith("NL-CONTRACT-")
        for record in cell["evidence_records"]
    )
    assert any(
        record["witness_level"] == "W2"
        and record["contract_id"].startswith("DOMAIN-INVARIANT-")
        for record in cell["evidence_records"]
    )


def test_successful_zero_llm_finding_cell_retains_frozen_domain_invariants(
    tmp_path: Path,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class ZeroFindingRuntime(FixtureStructuredRuntime):
        def call(self, **kwargs):
            outcome = super().call(**kwargs).model_copy(update={"real_llm": True})
            if isinstance(outcome.response, NLContractResponse):
                base = outcome.response.contracts[0]
                contract = base.model_copy(
                    update={
                        "locus_kind": "other",
                        "locus_names": ("provider-free passing check",),
                        "property": "other",
                        "expected_direction": "must_exist",
                        "violation_direction": "other",
                        "evidence_types": ("semantic_comparison",),
                        "binding_hints": (),
                    }
                )
                return outcome.model_copy(
                    update={
                        "response": outcome.response.model_copy(
                            update={"contracts": [contract]}
                        )
                    }
                )
            if isinstance(outcome.response, GroundingResponse):
                return outcome.model_copy(
                    update={
                        "response": outcome.response.model_copy(
                            update={"candidates": [], "additional_contracts": []}
                        )
                    }
                )
            return outcome

    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=ZeroFindingRuntime(),
        output_root=tmp_path,
    )

    assert cell["eligible"] is True
    assert cell["status"] == "completed"
    assert cell["stage_outputs"]["execute_batch"]["llm_candidate_count"] == 0
    assert cell["stage_outputs"]["execute_batch"]["domain_invariant_candidate_count"] > 0
    assert cell["evidence_records"]
    assert all(
        record["contract_id"].startswith("DOMAIN-INVARIANT-")
        for record in cell["evidence_records"]
    )
    assert all(
        record["witness_level"] == "W2" for record in cell["evidence_records"]
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
    } == set(cell["stage_outputs"]["validate_d"]["expected_obligation_ids"])
    d_receipt = next(
        item for item in cell["stage_receipts"] if item["stage_name"] == "d_adjudication"
    )
    assert d_receipt["status"] == "completed"
    assert not any(
        error.get("stage") in {"d_adjudication", "d_adjudication_correction"}
        for error in cell["errors"]
    )
    assert len(cell["evidence_records"]) == len(
        cell["stage_outputs"]["validate_d"]["expected_obligation_ids"]
    )
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
    assert len(cell["evidence_records"]) == len(
        cell["stage_outputs"]["validate_d"]["expected_obligation_ids"]
    )
    correction_prompt = next(
        prompt
        for kind, prompt in runtime.prompts
        if kind == "d_adjudication_correction"
    )
    assert 'duplicate_ids_to_repair:\n["0000:r1:i0"]' in correction_prompt
    assert '"obligation_id": "0000:r1:i0"' in correction_prompt


def test_d_correction_prompt_uses_one_unambiguous_repair_id_contract() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    prompt = build_d_correction_prompt(
        pair,
        [
            {"obligation_id": "0000:r1:i0"},
            {"obligation_id": "0000:r1:i5"},
        ],
        missing_ids=["0000:r1:i5"],
        duplicate_ids=["0000:r1:i0"],
        extra_ids=[],
    )

    assert 'repair_ids:\n["0000:r1:i0", "0000:r1:i5"]' in prompt
    assert "Return decisions\nonly for the repair IDs below" in prompt
    assert "only for the missing IDs below" not in prompt
    assert "Return exactly one decision for every ID in repair_ids" in prompt


def test_d_prompt_keeps_raw_fbmcq_formulas_receipt_only() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    raw_formula_marker = "RAW-FBMCQ-FORMULA-MUST-STAY-RECEIPT-ONLY"
    raw_formula = raw_formula_marker + ("x" * 300_000)
    dossier = {
        "obligation_id": "0000:r1:i0",
        "candidate": {
            "reason": "The candidate supplies one exact semantic allegation.",
            "basis": "provider-free D projection fixture",
        },
        "binding": {
            "precise": True,
            "element_refs": ["state:Fixture:line:1"],
            "source_refs": ["nl:NL1"],
            "reason": "The fixture binding is exact.",
            "basis": "provider-free D projection fixture",
        },
        "plan": {
            "formal_program": "G2(source='Fixture', target='Target')",
            "formal_program_hash": "sha256:" + ("a" * 64),
            "reason": "The frozen predicate plan is supplied.",
            "basis": "provider-free D projection fixture",
        },
        "receipt": {
            "receipt_id": "fixture-receipt",
            "backend": "fbmcq:G2",
            "terminal_state": "completed",
            "verdict": "false",
            "counterexample": [],
            "trace": [{"state": "Fixture"}],
            "run_metadata": {
                "algorithm_version": "pyfcstm.fbmcq.isolated.v2",
                "fbmcq_query_hash": "sha256:" + ("b" * 64),
                "fbmcq_formula": {
                    "bound": 2,
                    "kind": "must_reach",
                    "formulas": {"solve": raw_formula},
                },
            },
            "reason": "The native backend completed with a replayed result.",
            "basis": "provider-free D projection fixture",
        },
    }

    prompt = build_d_adjudication_prompt(pair, [dossier])

    assert raw_formula_marker not in prompt
    assert '"prompt_included": false' in prompt
    assert '"formula_hash": "sha256:' in prompt
    assert '"serialized_characters": 300' in prompt
    assert "pyfcstm.fbmcq.isolated.v2" in prompt
    assert '"verdict": "false"' in prompt


def test_d_prompt_batches_are_stable_complete_and_bounded() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    payload_by_id = {
        obligation_id: f"PAYLOAD-{obligation_id}-" + (character * 8_000)
        for obligation_id, character in (
            ("0000:r1:i2", "a"),
            ("0000:r1:i0", "b"),
            ("0000:r1:i1", "c"),
        )
    }
    dossiers = [
        {
            "obligation_id": obligation_id,
            "candidate": {
                "reason": payload,
                "basis": "provider-free stable batching fixture",
            },
            "binding": {
                "precise": True,
                "element_refs": [],
                "source_refs": [],
                "reason": "The fixture binding is exact.",
                "basis": "provider-free stable batching fixture",
            },
            "plan": {},
            "receipt": {},
        }
        for obligation_id, payload in payload_by_id.items()
    ]
    singleton_budget = max(
        len(build_d_adjudication_prompt(pair, [dossier])) for dossier in dossiers
    )

    batches = build_d_adjudication_batches(
        pair,
        dossiers,
        character_budget=singleton_budget,
    )

    assert [
        obligation_id for batch in batches for obligation_id in batch.obligation_ids
    ] == sorted(payload_by_id)
    assert len(batches) >= 2
    assert all(not batch.exceeds_budget for batch in batches)
    assert all(batch.prompt_characters <= singleton_budget for batch in batches)
    for batch in batches:
        for obligation_id in batch.obligation_ids:
            assert payload_by_id[obligation_id] in batch.prompt


def test_one_failed_d_batch_degrades_only_its_obligations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    probe_runtime = FixtureStructuredRuntime(include_second_candidate=True)
    _method_cell(
        pair=pair,
        round_index=1,
        runtime=probe_runtime,
        output_root=tmp_path / "probe",
    )
    full_prompt = next(
        prompt for kind, prompt in probe_runtime.prompts if kind == "d_adjudication"
    )
    monkeypatch.setattr(
        "pipeline.evidence_discovery.orchestration.runner._d_prompt_character_budget",
        lambda _runtime: len(full_prompt) - 1,
    )

    class SecondBatchFailureRuntime(FixtureStructuredRuntime):
        """Return one successful D batch followed by one audited batch failure."""

        def call(self, **kwargs):
            outcome = super().call(**kwargs)
            if kwargs["kind"] == "d_adjudication" and self.d_call_count == 2:
                return outcome.model_copy(
                    update={
                        "status": "failed",
                        "response": None,
                        "result": {"error": "controlled D batch failure"},
                        "reason": "The controlled second D batch failed.",
                        "basis": "provider-free batch degradation fixture",
                    }
                )
            return outcome

    runtime = SecondBatchFailureRuntime(include_second_candidate=True)
    cell = _method_cell(
        pair=pair,
        round_index=1,
        runtime=runtime,
        output_root=tmp_path / "failure",
    )

    batches = cell["stage_outputs"]["validate_d"]["initial_batches"]
    assert runtime.d_call_count == 2
    assert [batch["status"] for batch in batches] == [
        "completed",
        "failed_with_receipt",
    ]
    assert cell["stage_outputs"]["validate_d"]["final_unresolved_ids"] == []
    d_receipt = next(
        receipt
        for receipt in cell["stage_receipts"]
        if receipt["stage_name"] == "d_adjudication"
    )
    assert d_receipt["status"] == "completed_with_diagnostics"
    assert len(cell["evidence_records"]) == len(
        cell["stage_outputs"]["validate_d"]["expected_obligation_ids"]
    )
    failed_batch_ids = set(batches[1]["obligation_ids"])
    unresolved = {
        record["obligation_id"]
        for record in cell["evidence_records"]
        if record["d_level"] == "D_UNRESOLVED"
    }
    assert failed_batch_ids <= unresolved
    assert all(
        record["d_level"] == "D_UNRESOLVED"
        for record in cell["evidence_records"]
        if record["obligation_id"] in failed_batch_ids
    )
    released_count = sum(
        record["d_level"] in {"D1", "D2"}
        for record in cell["evidence_records"]
    )
    assert len(cell["report_issue_clusters"]) == released_count
    assert any(
        error.get("stage") == "d_adjudication"
        and error.get("batch_index") == 2
        for error in cell["errors"]
    )


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
            output_dir=PAPER_ROOT / "runs" / "should-not-start",
            profile="gpt-5.6-luna",
            allow_live=False,
        )


def test_full_live_runner_requires_second_explicit_gate() -> None:
    with pytest.raises(RuntimeError, match="allow_full_live=True"):
        run_experiment(
            report_root=REPORT_ROOT,
            output_dir=PAPER_ROOT / "runs" / "should-not-start-without-subset",
            profile="gpt-5.6-luna",
            allow_live=True,
        )


def test_live_runner_caps_diagnostic_subset_at_fifteen_pairs() -> None:
    with pytest.raises(RuntimeError, match="capped at 15"):
        run_experiment(
            report_root=REPORT_ROOT,
            output_dir=PAPER_ROOT / "runs" / "should-not-start-over-twelve",
            profile="gpt-5.6-luna",
            allow_live=True,
            pair_ids=[
                "0004",
                "0023",
                "0029",
                "0035",
                "0046",
                "0053",
                "0001",
                "0002",
                "0010",
                "0012",
                "0024",
                "0056",
                "0011",
                "0013",
                "0049",
                "0054",
            ],
        )


def test_live_runner_rejects_profile_outside_construction_protocol() -> None:
    with pytest.raises(RuntimeError, match="outside the frozen construction"):
        run_experiment(
            report_root=REPORT_ROOT,
            output_dir=PAPER_ROOT / "runs" / "should-not-start-sol",
            profile="gpt-5.6-sol",
            allow_live=True,
            pair_ids=["0004"],
        )
