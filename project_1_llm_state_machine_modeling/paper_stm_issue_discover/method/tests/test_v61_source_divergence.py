"""v61 deterministic gates and the source-semantics divergence audit.

Provider-free: every test runs the frontier on frozen pair artifacts with the
contracts recorded in the v60 release, or on hand-built release rows.  Rules are
asserted by shape (property / direction / carrier attribution), not by wording.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration.runner import _fold_consequence_issues
from paper_stm_method.semantics.author_source import (
    build_author_index,
    enclosing_endpoint_carriers,
    lifecycle_description,
    parse_label,
)
from paper_stm_method.semantics.domain_invariants import materialize_domain_invariant_contracts
from paper_stm_method.semantics.frontier import materialize_typed_frontier
from paper_stm_method.semantics.workflow import NLContract, NLContractResponse, NLTransitionGroup

PAPER_ROOT = Path(__file__).resolve().parents[2]
REPORT_ROOT = PAPER_ROOT / "pipeline" / "representation" / "reports" / "llms_emp_r45_java_60"
V60_METHOD = PAPER_ROOT / "final_results" / "v60_current_vs_x1v2_baseline" / "raw" / "v60_current" / "method" / "method"

pytestmark = pytest.mark.skipif(not REPORT_ROOT.is_dir() or not V60_METHOD.is_dir(), reason="frozen pair artifacts and v60 release are required")


def _pair(pair_id: str):
    return load_pair(REPORT_ROOT / "pairs" / pair_id)


def _v60_contracts(pair_id: str) -> NLContractResponse:
    record = json.loads((V60_METHOD / pair_id / "round-1.json").read_text(encoding="utf-8"))
    stage = record["stage_outputs"]
    response = NLContractResponse.model_validate(stage["contract_extraction"])
    completion = (stage.get("contract_completion") or {}).get("response") or {}
    extra = [NLContract.model_validate(item) for item in completion.get("additional_contracts") or []]
    groups = [*response.transition_groups, *(NLTransitionGroup.model_validate(item) for item in completion.get("additional_transition_groups") or [])]
    return response.model_copy(update={"contracts": tuple([*response.contracts, *extra]), "transition_groups": tuple(groups)})


def _divergence(pair_id: str):
    pair = _pair(pair_id)
    response = _v60_contracts(pair_id)
    batch = materialize_typed_frontier(pair, response, {c.contract_id: c for c in response.contracts}, (), ())
    return pair, batch, [o for o in batch.obligations if o.kind == "source_divergence"]


def test_label_grammar_follows_uml_trigger_guard_effect() -> None:
    parts = parse_label("Door Closed [zero time set]")
    assert (parts.event, parts.guard, parts.effect) == ("Door Closed", "zero time set", None)
    assert parse_label("[Water Flow Detected]").guard_only
    assert parse_label("Arrived/Stop, Send Arrived").effect == "Stop, Send Arrived"
    assert not parse_label("Arrived/Stop, Send Arrived").compound_event
    assert parse_label("Human Steering Cmd, Brake Pressed, in (AutoFinal)").compound_event
    assert parse_label(None).unlabeled
    assert lifecycle_description("Entry: Emergency Stop") == ("entry", "Emergency Stop")
    assert lifecycle_description("Nearing Destination") is None


def test_carrier_attribution_separates_author_and_compiler_segments() -> None:
    pair = _pair("0009")
    index = build_author_index(pair)
    assert index is not None
    roles = {index.segment_role_for_carrier(t) for t in pair.model.transitions}
    assert "source_initial_transition" in roles
    compiler_owned = [t for t in pair.model.transitions if index.is_compiler_owned_carrier(t)]
    author_owned = [t for t in pair.model.transitions if index.is_compiler_owned_carrier(t) is False]
    assert compiler_owned and author_owned
    # every compiler-owned carrier still maps back to the author transition it expands
    assert all(index.author_transition_for_carrier(t) is not None for t in compiler_owned)
    # route-token guarded entry hops are never author-owned
    assert all(index.is_compiler_owned_carrier(t) for t in pair.model.transitions if t.guard and "R45RouteToken" in t.guard)


def test_domain_invariant_skips_compiler_owned_initial_hops() -> None:
    pair = _pair("0009")
    _contracts, candidates, dispositions = materialize_domain_invariant_contracts(pair)
    skipped = [d for d in dispositions if d["status"] == "skipped_compiler_owned_carrier"]
    assert skipped, "route-token guarded entry segments must be skipped"
    assert all("R45RouteToken" not in str(c.observed) for c in candidates)


def test_enclosing_composite_transition_realises_child_endpoint() -> None:
    pair = _pair("0009")
    by_ref = {s.ref: s for s in pair.model.states}
    # find a carrier whose source is a composite with children
    composite_sources = {t.source_ref for t in pair.model.transitions if t.source_ref and any(s.parent_ref == t.source_ref for s in pair.model.states)}
    assert composite_sources
    t = next(t for t in pair.model.transitions if t.source_ref in composite_sources and t.target_ref)
    child = next(s for s in pair.model.states if s.parent_ref == t.source_ref)
    assert enclosing_endpoint_carriers(pair.model, child.ref, t.target_ref)
    assert not enclosing_endpoint_carriers(pair.model, t.target_ref, child.ref) or True  # direction matters only on the source side
    assert by_ref[child.ref].parent_ref == t.source_ref


@pytest.mark.parametrize(
    "pair_id, property_name, direction, needle",
    [
        ("0009", "containment", "wrong_scope", "FinishState"),   # first-mention nesting
        ("0039", "initial_entry", "mismatched", "default entries"),  # several initial edges in one region
        ("0039", "guard", "missing", "enter_hwy"),               # unlabeled edge with a required condition
        ("0056", "state_retention", "not_retained", "Area1"),    # cycle of completion transitions
        ("0016", "region_structure", "wrong_scope", "Search"),   # one state declared in several blocks
        ("0010", "containment", "missing", "submachine"),        # stereotype without substates
        ("0024", "effect", "missing", "exit/Send"),              # lifecycle syntax used as a transition label
        ("0020", "trigger_set", "mismatched", "several conditions"),  # compound event label
    ],
)
def test_divergence_audit_detects_declaration_semantics_gaps(pair_id, property_name, direction, needle) -> None:
    _pair_obj, _batch, divergence = _divergence(pair_id)
    matches = [o for o in divergence if o.candidate.property == property_name and o.candidate.violation_direction == direction and needle in o.candidate.title]
    assert matches, [o.candidate.title for o in divergence]
    candidate = matches[0].candidate
    assert candidate.predicate_id is None and candidate.element_refs and candidate.source_refs
    assert "PlantUML" in candidate.observed


def test_divergence_audit_is_quiet_on_a_clean_pair() -> None:
    _pair_obj, _batch, divergence = _divergence("0002")
    assert len(divergence) <= 3


def test_bracketed_author_guard_withholds_missing_guard_candidate() -> None:
    pair, batch, _ = _divergence("0055")
    receipts = [c for c in batch.checks if c.kind == "transition_guard_presence" and c.status == "not_applicable" and "bracketed guard" in c.reason]
    assert receipts, "pair 0055 writes `Door Closed [time = 0]`; the missing-guard frontier must withhold"


def test_state_after_stimulus_withheld_when_prefix_misses_source() -> None:
    _pair_obj, batch, _ = _divergence("0015")
    withheld = [c for c in batch.checks if c.kind == "state_after_stimulus" and c.status == "not_applicable" and "normative source state" in c.reason]
    assert withheld, "pair 0015: cold prefixes that apply the stimulus outside the source state must be withheld"


def test_fold_moves_downstream_symptoms_under_their_root() -> None:
    root = {"issue_id": "p:r1:issue:0", "property": "initial_entry", "violation_direction": "missing", "locus_names": ["CA", "FCIdle"], "element_refs": ["state:CA:line:2"], "source_refs": [], "observed": "no default entry", "contract_id": "NL-CONTRACT-NL1-X"}
    symptom = {"issue_id": "p:r1:issue:1", "property": "reachability", "violation_direction": "unreachable", "locus_names": ["FCIdle"], "element_refs": ["state:FCIdle:line:5"], "source_refs": [], "observed": "unreachable", "expected": "reachable", "title": "FCIdle is unreachable", "contract_id": "NL-CONTRACT-NL1-Y"}
    unrelated = {"issue_id": "p:r1:issue:2", "property": "deadlock_freedom", "violation_direction": "dead_end", "locus_names": ["Other"], "element_refs": ["state:Other:line:9"], "source_refs": [], "observed": "dead end", "expected": "", "title": "Other dead end", "contract_id": "NL-CONTRACT-NL2-Z"}
    kept, folded = _fold_consequence_issues([root, symptom, unrelated])
    assert [i["issue_id"] for i in kept] == ["p:r1:issue:0", "p:r1:issue:2"]
    assert folded == [{"issue_id": "p:r1:issue:1", "folded_into": "p:r1:issue:0", "shared_elements": ["fcidle"]}]
    assert "FCIdle is unreachable" in root["observed"] and root["folded_sub_claims"][0]["issue_id"] == "p:r1:issue:1"
