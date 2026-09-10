"""Exercise A2 through the actual staged runner and repository input closure."""

import importlib.util
import json
from pathlib import Path
import re

import pytest

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.semantics import frontier, workflow
from paper_stm_method.semantics.no_predicates import SemanticContract, without_predicates


PAPER = Path(__file__).resolve().parents[2]
REPORT = PAPER / "pipeline/representation/reports/llms_emp_r45_java_60"
SOURCE_FIXTURE = PAPER / "pipeline/evidence_discovery/tests/test_input_closure_and_staged_flow.py"
if not SOURCE_FIXTURE.is_file() and runner._release_source_provenance() is not None:
    pytest.skip("repository closure and staged fixture are not shipped in the verified release", allow_module_level=True)
spec = importlib.util.spec_from_file_location("a2_staged_fixture", SOURCE_FIXTURE)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class SemanticRuntime(fixture.FixtureStructuredRuntime):
    def __init__(self, *, grounding="established"):
        super().__init__(include_second_candidate=True, omit_second_d_decision=True)
        self.requests = []
        self.grounding = grounding

    def call(self, **kwargs):
        schema = kwargs["schema"]
        self.requests.append({**kwargs, "schema": schema.model_json_schema()})
        full_schema = next(base for base in (
            workflow.NLContractResponse, workflow.ContractCompletionResponse,
            workflow.GroundingResponse, workflow.DAdjudicationResponse,
        ) if issubclass(schema, base))
        outcome = super().call(**{**kwargs, "schema": full_schema})
        payload = outcome.response.model_dump(mode="json")
        # Only the legacy test fixture uses full-shaped canned responses. The
        # production runtime receives and validates the A2 schema directly.
        for candidate in payload.get("candidates", []):
            candidate.pop("predicate_id")
            candidate.pop("predicate_inputs")
        for decision in payload.get("decisions", []):
            decision["grounding"] = self.grounding
        return outcome.model_copy(update={
            "response": schema.model_validate(payload),
            "real_llm": True,  # Enable completion/correction; no provider call.
        })


@pytest.mark.parametrize("grounding", ["established", "not_established"])
def test_a2_staged_calls_disable_the_entire_execution_mechanism(tmp_path, monkeypatch, grounding):
    def forbidden(*args, **kwargs):
        pytest.fail("A2 executed a disabled predicate step")

    for name in (
        "route_primary_candidates", "_apply_typed_predicate_boundary", "_enrich_candidate",
        "compile_plan", "validate_plan", "run_backend", "build_predicate_execution_receipt",
        "_prepared_is_finding_candidate", "_materialize_deterministic_execution_probes",
        "finalize_route_telemetry",
    ):
        monkeypatch.setattr(runner, name, forbidden)
    monkeypatch.setattr(frontier, "_materialize_group_post_states", forbidden)
    runtime = SemanticRuntime(grounding=grounding)
    cell = runner._method_cell(
        pair=load_pair(REPORT / "pairs/0000"), round_index=1, runtime=runtime, output_root=tmp_path,
        run_identity={"ablation": "no-predicates", "run_id": "0" * 32,
                      "run_contract_hash": "sha256:" + "0" * 64,
                      "source_provenance": runner._source_provenance()},
    )
    assert cell["ablation"] == "no-predicates"
    assert cell["predicate_execution_receipts"] == []
    execute = cell["stage_outputs"]["execute_batch"]
    assert execute["prepared_count"] == execute["candidate_count"] > 0
    assert execute["execution_probe_count"] == execute["satisfied_count"] == 0
    assert execute["domain_invariant_candidate_count"] > 0
    assert execute["primary_route_telemetry"] == []
    assert bool(cell["report_issue_clusters"]) is (grounding == "established")
    for record in cell["evidence_records"]:
        assert record["plan"] is record["receipt"] is record["execution_receipt"] is None
        assert record["witness_level"] in {"W0", "W1"}
    for stage in cell["stage_receipts"]:
        assert "predicate_registry" not in stage["input_artifact_roles"]
    kinds = [request["kind"] for request in runtime.requests]
    assert "contract_completion" in kinds and "d_adjudication_correction" in kinds
    for request in runtime.requests:
        text = request["system_prompt"] + request["prompt"] + json.dumps(request["schema"])
        # The retained inspect/SMT provenance explicitly excludes the legacy
        # inspect backend; that is not the removed candidate execution backend.
        text = text.replace("legacy inspect backend", "legacy inspect implementation")
        matches = list(re.finditer(r"\b(?:S[1-5]|G[1-3]|R[1-3]|V1)\b|predicate_id|predicate_inputs|frozen predicate|backend|registry", text))
        assert not matches, (request["kind"], [text[max(0, m.start()-80):m.end()+100] for m in matches])


@pytest.mark.parametrize("pair_id", ["0000", "0004", "0023", "0034"])
def test_a2_retains_the_full_input_closure(pair_id):
    pair = load_pair(REPORT / "pairs" / pair_id)
    view = without_predicates(pair)
    for name in type(pair).model_fields:
        assert getattr(view, name) == getattr(pair, name)
    assert view.model is pair.model
    assert view.inspection_facts is pair.inspection_facts


def contract_for(pair, **kwargs):
    return SemanticContract(
        segment_id="NL1", quote=pair.nl_segments[0].text,
        normative_statement="The fixture supplies one exact semantic obligation.",
        scope="Exact fixture locus", source_refs=["NL1"],
        reason="Provider-free semantic obligation.", basis="Exact input fixture.", **kwargs,
    )


def hint(role, value):
    return dict(role=role, value=value, reason="Exact fixture identity.", basis="Supplied artifact.")


def test_semantic_guards_keep_the_existing_report_aggregation():
    from paper_stm_method.semantics.author_source import build_author_index

    pair = without_predicates(load_pair(REPORT / "pairs/0009"))
    index = build_author_index(pair)
    carriers = [t for t in pair.model.transitions if index.is_compiler_owned_carrier(t) is False
                and (author := index.author_transition_for_carrier(t))
                and author.label.event and "=" in author.label.event][:3]
    assert len(carriers) >= 2
    release, contracts = [], {}
    for i, carrier in enumerate(carriers):
        contract = contract_for(
            pair, contract_id=f"NL-CONTRACT-NL1-GUARD{i}", locus_kind="transition",
            locus_names=[carrier.source, carrier.target], property="guard",
            expected_direction="must_exist", violation_direction="missing", evidence_types=["guard_fact"],
            binding_hints=[hint("guard", index.author_transition_for_carrier(carrier).label.event)],
        )
        contracts[contract.contract_id] = contract
        release.append(dict(
            issue_id=f"0009:r1:issue:{i}", predicate_id=None, predicate_inputs={},
            property="guard", violation_direction="missing", locus_names=list(contract.locus_names),
            element_refs=[carrier.ref], binding={"element_refs": [carrier.ref]}, source_refs=[],
            observed="guard=null", expected=contract.normative_statement, title="Required guard is absent",
            contract_id=contract.contract_id,
        ))
    kept, aggregated = runner._aggregate_guard_modality_issues(pair, release, contracts)
    assert len(kept) == 1 and len(aggregated) == len(carriers)-1
    assert len(kept[0]["folded_sub_claims"]) == len(carriers)-1
    assert all(issue["predicate_id"] is None and not issue["predicate_inputs"] for issue in release)


def test_semantic_root_preflight_uses_contract_identities():
    pair = without_predicates(load_pair(REPORT / "pairs/0056"))
    root, target = pair.inspection_facts.machine_root_ref, "state:SearchState:line:9"
    contract = contract_for(
        pair, contract_id="NL-CONTRACT-ROOT-WRAPPER-REACHABILITY", locus_kind="composite",
        locus_names=["SearchState"], property="reachability", expected_direction="must_reach",
        violation_direction="unreachable", evidence_types=["reachability_fact"],
        binding_hints=[hint("source", root), hint("target", target)],
    )
    candidate = runner.CandidateIssue(
        contract_id=contract.contract_id, locus_kind=contract.locus_kind, locus_names=contract.locus_names,
        property=contract.property, violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types, title="SearchState is unreachable from wrapper",
        requirement_quote=contract.quote, element_refs=[root, target], source_refs=["source:transition:tr_0001"],
        expected=contract.normative_statement, observed="Synthetic wrapper is marked unreachable.",
        strongest_rebuttal="A top-level initial transition reaches SearchState.",
        reason="Exact fixture claim.", basis="Source and inspection fixture.",
    )
    retained, dispositions = runner._preflight_synthetic_root_wrapper_reachability(
        pair, [candidate], {contract.contract_id: contract},
    )
    assert retained == [] and len(dispositions) == 1
    assert dispositions[0]["status"] == "suppressed_synthetic_root_wrapper_projection"


def test_semantic_domain_invariants_keep_exact_native_carriers_and_deduplication():
    from paper_stm_method.semantics.domain_invariants import materialize_domain_invariant_contracts

    full = load_pair(REPORT / "pairs/0000")
    full_contracts, _, _ = materialize_domain_invariant_contracts(full)
    pair = without_predicates(full)
    contracts, candidates, _ = materialize_domain_invariant_contracts(pair)
    assert {(c.property, c.transition_ref, c.authority_ref) for c in contracts} == {
        (c.property, c.transition_ref, c.authority_ref) for c in full_contracts
    }
    assert candidates
    for contract, candidate in zip(contracts, candidates):
        assert candidate.predicate_id is None and candidate.predicate_inputs == {}
        assert contract.candidate_mismatches(candidate) == ()
        bad = candidate.model_copy(update={"element_refs": []})
        assert "transition" in contract.candidate_mismatches(bad)
    _, repeated, dispositions = materialize_domain_invariant_contracts(pair, existing_candidates=candidates)
    assert repeated == ()
    assert any(d["status"] == "duplicate_exact_candidate" for d in dispositions)


def test_missing_edge_scout_keeps_semantic_candidate_and_exact_deduplication():
    from paper_stm_method.semantics.author_source import enclosing_endpoint_carriers

    pair = without_predicates(load_pair(REPORT / "pairs/0004"))
    source, target = next(
        (s, t) for s in pair.model.states for t in pair.model.states
        if s.ref != t.ref and not enclosing_endpoint_carriers(pair.model, s.ref, t.ref)
    )
    contract = contract_for(
        pair, contract_id="NL-CONTRACT-NL1-ABSENT", locus_kind="transition",
        locus_names=[source.name, target.name], property="transition_endpoints",
        expected_direction="must_exist", violation_direction="missing", evidence_types=["transition_fact"],
        binding_hints=[hint("source", source.ref), hint("target", target.ref)],
    )
    response = workflow.NLContractResponse(contracts=[contract], reason="Fixture", basis="Exact endpoints")
    candidates, receipts = runner._materialize_exact_s2_inventory_candidates(pair, response, [])
    assert len(candidates) == len(receipts) == 1
    assert candidates[0].predicate_id is None and not candidates[0].predicate_inputs
    assert set(candidates[0].element_refs) == {source.ref, target.ref}
    assert runner._materialize_exact_s2_inventory_candidates(pair, response, candidates) == ([], [])


def test_no_predicates_worker_records_and_resume(tmp_path):
    args = dict(report_root=REPORT, output_dir=tmp_path, profile="fixture", ablation="no-predicates",
                rounds=1, pair_ids=["0004", "0023"], workers=2, run_id="c" * 32)
    summary = runner.run_experiment(**args)
    root = Path(summary["artifact_root"])
    assert summary["ablation"] == "no-predicates"
    for pair_id in args["pair_ids"]:
        cell = json.loads((root / "method" / pair_id / "round-1.json").read_text())
        assert cell["ablation"] == "no-predicates"
        assert cell["stage_outputs"]["ablation"]["predicate_execution"] == "disabled_by_ablation"
        assert cell["predicate_execution_receipts"] == []
        assert not cell["eligible"], "fixture must not enter experimental metrics"
    runner.run_experiment(**args, resume=True)
    for mode in ("none", "no-inspect"):
        with pytest.raises(RuntimeError, match="resume contract mismatch"):
            runner.run_experiment(**{**args, "ablation": mode}, resume=True)
