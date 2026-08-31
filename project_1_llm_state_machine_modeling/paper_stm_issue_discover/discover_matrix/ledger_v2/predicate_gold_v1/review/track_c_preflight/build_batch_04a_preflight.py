"""Build the hash-sealed, pre-execution Track C semantic audit for batch 04a."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    BlindReviewInputPacket,
    TrackAProposalBatch,
    TrackBProposalBatch,
)


@dataclass(frozen=True)
class Decision:
    """One issue-specific semantic decision made before execution."""

    obligation: str
    implication: str
    input_audit: str
    eligibility: str
    conflicts: tuple[str, ...] = ()
    candidate_id: str | None = None
    relation: str | None = None
    disposition: str = "UNSUPPORTED_EXACT"
    execution_mode: str | None = None
    model_lines: tuple[int, int] | None = None


DECISIONS: dict[str, Decision] = {
    "DIFF-0019-05": Decision(
        obligation="Accept Track A's artifact-bound conjunction: the root and AutonomousMode must each have exactly one target-fixed, triggerless and guardless native initial carrier, traversed as structural initialization.",
        implication="The non-short-circuit AND of the two complete owner-local native initial-transition contracts is equivalent to this finite two-owner obligation. Each child checks cardinality, target, event absence and guard absence over the complete native init_transitions inventory; neither child alone is sufficient.",
        input_audit="PASS: both owner paths and target paths are exact author identities; no-event/no-guard and single-initial cardinality come from UML initial-pseudostate semantics. P1 and P2 supply complete disjoint child inputs.",
        eligibility="PASS: pyfcstm State.init_transitions is within the attribution-scoped source-static boundary. The evaluation-only parent contributes only an explicit AND and requires both children to run.",
        conflicts=("Track B correctly identifies the equivalent P3 conjunction but leaves it unsupported solely because the prior composite runner admitted only frozen-predicate children; the evaluation-only native composite closes that engineering gap without adding semantics.",),
        candidate_id="DIFF-0019-05-B-P3",
        relation="EQUIVALENT",
        disposition="EXECUTE_COMPOSITE_EXACT",
        execution_mode="EVALUATION_ONLY_NATIVE_COMPOSITE",
        model_lines=(63, 75),
    ),
    "EIS-0019-01": Decision(
        obligation="Accept Track A's least-strengthening D1 reading: the shared condition permits cruise or lane_change, while deterministic arbitration remains a retained sensitivity rather than a source-fixed obligation.",
        implication="Track B's V1 property formalizes only the retained deterministic-disambiguation reading. It is unrelated to the adopted obligation, and the artifact contains free-text event labels rather than source-backed typed guards or a closed variable domain.",
        input_audit="FAIL: no complete guard multiset, mutual-exclusion rule, priority, or dist_to_front/extra_lane domain is source-bound.",
        eligibility="FAIL: V1 cannot be issued with invented guard ASTs or domains; no alternative exact or sound falsifier is closed for the adopted D1 reading.",
        conflicts=("Track B adopts the retained deterministic sensitivity as O, while Track A adopts source-permitted nondeterminism; Track C follows the source-minimal Track A reading and preserves the stronger reading as sensitivity.",),
        model_lines=(24, 25),
    ),
    "EIS-0019-02": Decision(
        obligation="Accept the explicit NL obligation that every entry to CollisionAvoidanceSystem initializes its local region uniquely and unconditionally in collision_avoidance_deactive during the same entry RTC.",
        implication="The complete native owner-local initial contract is equivalent: exactly one initial carrier, the source-fixed target, no event and no guard jointly capture the entire local default-entry obligation.",
        input_audit="PASS: owner and target paths resolve exactly; cardinality and trigger/guard absence are formal-semantic requirements, not values inferred from the defective result.",
        eligibility="PASS: NATIVE_INITIAL_TRANSITION_CONTRACT uses pyfcstm State.init_transitions and exact paths only; whole-model simulation is not used.",
        candidate_id="EIS-0019-02-B-P1",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="EVALUATION_ONLY_NATIVE_ORACLE",
        model_lines=(67, 73),
    ),
    "EIS-0019-03": Decision(
        obligation="Accept Track A's D1 reading that auto_finished completes each mode from its source-described exit phase; retain mode-global enablement from every nested leaf as sensitivity.",
        implication="Track B's ancestor-wide direct-target coverage encodes the stronger mode-global sensitivity and also rejects valid compound RTC realizations. It is unrelated to the adopted exit-phase obligation.",
        input_audit="FAIL: the required source set depends on the unresolved D1 reading, and direct FinishState targets are not required for a compound exit/continuation realization.",
        eligibility="FAIL: the attribution-scoped artifact cannot support hierarchical event-dispatch/RTC equivalence, and a source-static direct-carrier oracle would overconstrain O.",
        conflicts=("Track B adopts mode-global enablement; Track A adopts exit-phase completion. The author text supports both, so Track C does not promote the stronger reading into executable gold.",),
        model_lines=(18, 62),
    ),
    "INS-0019-01": Decision(
        obligation="Accept that collision avoidance must be reachable or concurrently active so its described lifecycle can occur; the source does not fix the composition mechanism.",
        implication="A guard-agnostic G1 path to collision_avoidance_deactive is at most a necessary topology symptom and does not capture concurrency, default entry, event dispatch or runtime configuration semantics.",
        input_audit="PARTIAL: the named subsystem and local state exist, but a unique source and composition mechanism are absent.",
        eligibility="FAIL: metadata permits source-static attribution only and explicitly withholds whole-model behavior equivalence; executing G1 here would turn an ineligible projection into gold evidence.",
        model_lines=(67, 75),
    ),
    "EIS-0020-02": Decision(
        obligation="Accept Track A's D1 reading that steering and brake are independent takeover stimuli in the applicable AutoFinal scope; retain AutoFinal occupancy as a third standalone alternative sensitivity.",
        implication="Track B's three-alternative static contract is stronger than the adopted reading. Separate native event identities and an eventless AutoFinal takeover carrier do not exist and cannot be bound without choosing an unprovided normalization.",
        input_audit="FAIL: the source provides free text but no FCSTM-native aliases, complete source-state set, or decision on whether AutoFinal is a qualifier or third trigger.",
        eligibility="FAIL: no exact or sound property with complete typed bindings survives both D1 readings; fabricated event aliases or an eventless carrier are prohibited.",
        conflicts=("Track B normalizes the retained three-alternative reading, whereas Track A treats AutoFinal as a source-state qualifier. Track C keeps the ambiguity explicit.",),
        model_lines=(8, 27),
    ),
    "INS-0023-01": Decision(
        obligation="PumpState is a reachable continuing operating state and must permit later source-authorized operating change rather than become an undeclared absorbing dead end.",
        implication="V4 one-step model progress is only a necessary proxy; it neither proves eventual lifecycle continuation nor supplies the missing condition and destination.",
        input_audit="FAIL: no exit condition, target, fairness assumption or legitimate termination policy is source-bound.",
        eligibility="FAIL: simulation/behavior is academically ineligible for this attribution-scoped FCSTM, and no source-backed positive control can be made without inventing a transition.",
        model_lines=(2, 10),
    ),
    "INS-0023-02": Decision(
        obligation="WaterState is a reachable continuing monitoring state and must permit later source-authorized operating change rather than become an undeclared absorbing dead end.",
        implication="V4 one-step model progress is only a necessary proxy and does not express eventual change among operating conditions.",
        input_audit="FAIL: no exit condition, target, priority, timing or termination policy is supplied.",
        eligibility="FAIL: the FCSTM is not behavior/simulation eligible, and a control transition would invent missing author semantics.",
        model_lines=(2, 10),
    ),
    "INS-0023-03": Decision(
        obligation="MethaneState is a reachable continuing monitoring state and must permit later source-authorized operating change rather than become an undeclared absorbing dead end.",
        implication="V4 one-step progress is only a necessary proxy and cannot prove the source's continuing multi-condition lifecycle.",
        input_audit="FAIL: the author gives no exit condition, target, priority, timing or termination policy.",
        eligibility="FAIL: behavior execution is ineligible, and constructing a true control requires inventing the missing transition semantics.",
        model_lines=(2, 10),
    ),
    "DIFF-0024-04": Decision(
        obligation="Under the adopted issue-local D1 reading, the exact EmergencyStopping-to-InMotion carrier labelled exit/Send Obstacle Detected is an unauthorized recovery carrier; recovery policy remains otherwise unspecified.",
        implication="For this artifact-bound added-carrier issue, absence of the exact owner/source/event/target signature is equivalent to removing the disputed carrier. The property makes no claim that the resulting model fully implements emergency output or every possible recovery policy.",
        input_audit="PASS: owner, source, event and target are exact attribution-preserving native identities from source line 19 and the FCSTM projection.",
        eligibility="PASS: FORBIDDEN_SIGNATURES_ABSENT inspects the complete pyfcstm native carrier inventory without runtime claims.",
        conflicts=("Track A retains intentional recovery as a D1 sensitivity; equivalence is therefore explicitly issue-local and conditional on the adopted malformed-action reading, not a closed-world claim about all future recovery designs.",),
        candidate_id="DIFF-0024-04-B-P1",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="EVALUATION_ONLY_RELATION",
        model_lines=(28, 34),
    ),
    "EIS-0024-01": Decision(
        obligation="Every entry to Accelerating must carry the explicit author action Accelerate in the entry lifecycle slot.",
        implication="S4 membership of Accelerate in the exact native Accelerating.on_enters collection is equivalent to this attachment obligation; it does not claim physical acceleration execution semantics.",
        input_audit="PASS: state, entry phase and action token are all literal author-source bindings and resolve without fuzzy matching.",
        eligibility="PASS: S4 is exact for one parseable native lifecycle-slot attachment and is within source-static eligibility.",
        candidate_id="EIS-0024-01-B-P1",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="FROZEN_S4",
        model_lines=(10, 18),
    ),
    "EIS-0024-02": Decision(
        obligation="Approaching must emit Send as system output while continuing the approach; both output and retention are required.",
        implication="No candidate is equivalent or a sound executable falsifier because the source leaves the lifecycle phase and output representation unspecified, and a bounded retention scenario would add events and a window.",
        input_audit="FAIL: entry/do/exit phase, exact action encoding, output receiver and release interval are absent.",
        eligibility="FAIL: neither S4 nor R4 can be issued without invented inputs; the composite runner cannot repair semantic omissions.",
        model_lines=(10, 29),
    ),
    "EIS-0024-03": Decision(
        obligation="At every stable pre-release configuration, Approaching must remain active until a source-authorized ready-to-stop or decelerate condition permits exit.",
        implication="O entails absence of the exact unrelated exit/Send leaf-exit carrier, so false soundly falsifies O. P does not imply O because other unauthorized exits or unbounded violations may remain and the continuation RTC is not executed.",
        input_audit="PASS: the forbidden owner/source/event/exit signature is an exact attribution-preserving identity; no release event, bound or state alias is invented.",
        eligibility="PASS: the relation oracle is used only as a source-static O_IMPLIES_P proxy and does not claim full remain-until execution.",
        candidate_id="EIS-0024-03-B-P1",
        relation="O_IMPLIES_P",
        disposition="EXECUTE_PROXY",
        execution_mode="EVALUATION_ONLY_RELATION",
        model_lines=(10, 29),
    ),
    "EIS-0024-04": Decision(
        obligation="EmergencyStopping must perform Emergency Stop and emit Obstacle Detected as behavior attributable to the episode; the source leaves lifecycle phase open.",
        implication="S4 requires an unprovided phase and S6 would bind the obligation to one exit carrier and operation syntax. Neither candidate is entailed by the phase-agnostic O.",
        input_audit="FAIL: exact entry/do/exit phase, operation syntax and output delivery semantics are missing.",
        eligibility="FAIL: executing a guessed lifecycle slot or effect would manufacture the decisive typed input.",
        model_lines=(28, 34),
    ),
    "INS-0024-01": Decision(
        obligation="Stopping is an operational arrival state and must preserve a later legitimate lifecycle path or be explicitly declared a true system-final condition.",
        implication="V4 one-step progress is a necessary proxy only; it does not express the disjunction between continuing lifecycle and legitimate finality.",
        input_audit="FAIL: post-arrival destination, event, timing and finality policy are all unspecified.",
        eligibility="FAIL: whole-model behavior is ineligible and no source-backed positive control can add a particular continuation or final declaration.",
        model_lines=(26, 34),
    ),
    "EIS-0025-01": Decision(
        obligation="Accept Track A's minimal sufficient-condition D1 reading: zero-time close must be able to reach DoorShutWithItem, but the source does not establish the converse or require an explicit guard representation.",
        implication="Track B's S5 exact-guard property encodes the retained exclusive-routing reading and is unrelated to the adopted sufficient-condition obligation.",
        input_audit="FAIL: no variable identity, type, domain or parseable zero-time guard is author-supplied.",
        eligibility="FAIL: choosing time, cooking_time, or any guard AST would invent representation and strengthen the adopted D1 reading.",
        conflicts=("The ledger detail argues for exclusive routing, but Track A's source-minimal reading treats the clause as sufficient. Track C preserves exclusivity as sensitivity rather than executable gold.",),
        model_lines=(16, 31),
    ),
    "EIS-0025-02": Decision(
        obligation="Cooking time must be observably displayed and updateable in ReadytoCook, with the stated cancellation/update behavior, without assuming one internal representation.",
        implication="No frozen predicate or evaluation-only property can be equivalent without a variable, data type, update function, lifecycle phase and operation identities.",
        input_audit="FAIL: every decisive data/action input is absent, and the external-HMI reading remains a D1 sensitivity.",
        eligibility="FAIL: a static absence check would show a symptom but cannot bind the representation-independent observable obligation or support a non-invented true control.",
        model_lines=(1, 31),
    ),
    "EIS-0026-01": Decision(
        obligation="Accept Track A's less-structural D1 reading that three state areas denote the three sibling operating modes; retain three orthogonal regions as sensitivity.",
        implication="DIRECT_CHILD_HIERARCHY counts child states, not regions, and would be true on the defective artifact for the wrong reason. It is unrelated to either a genuine region-count property or the adopted mode reading.",
        input_audit="FAIL: region contents, names, initial states and whether orthogonality is intended are absent.",
        eligibility="FAIL: executing child-count cannot answer region semantics and would create a false positive gold result.",
        conflicts=("Track B normalizes 'state areas' as regions, while Track A adopts sibling modes. The source does not resolve the term, so Track C keeps region count unsupported.",),
        model_lines=(6, 17),
    ),
    "EIS-0026-02": Decision(
        obligation="Every completed attack must produce an observable strict decrease in swarm count in the next stable configuration; decrement magnitude is not fixed.",
        implication="S6 needs one exact parseable operation and therefore cannot express a representation-independent strict decrease when no count variable, type, domain or decrement operation exists.",
        input_audit="FAIL: variable name, type/domain, initial value, decrement and zero behavior are missing.",
        eligibility="FAIL: no exact/proxy query or true positive control can be built without inventing the data model.",
        model_lines=(6, 17),
    ),
    "EIS-0026-03": Decision(
        obligation="After interception and formation adjustment, the mission must remain capable of resuming search or another progress state before mission completion; exact exit details are unspecified.",
        implication="G1 to one chosen target and V4 one-step progress are necessary symptoms only and do not capture eventual mission continuation, events, guards or fairness.",
        input_audit="FAIL: completion event, continuation target, duration, priority and failure behavior are not source-bound.",
        eligibility="FAIL: behavior/topology equivalence is ineligible and a positive control would have to invent the missing continuation.",
        model_lines=(6, 17),
    ),
    "EIS-0027-01": Decision(
        obligation="After each collision-avoidance activation, the three-region episode must eventually leave its terminal regional configuration and re-establish detection or another continuing safe configuration.",
        implication="G1 to DetectingState and V4 local progress are only necessary approximations; neither expresses orthogonal synchronization, deactivation/rearm, safe configuration or eventuality.",
        input_audit="FAIL: rearm event, synchronization rule, exit target, invariant and deadlines are absent.",
        eligibility="FAIL: whole-model behavior is ineligible, and constructing a true control requires inventing the missing multi-region protocol.",
        model_lines=(3, 23),
    ),
    "INS-0027-04": Decision(
        obligation="All three orthogonal controls must initiate behaviorally nonempty control work and may complete only after meaningful control completion.",
        implication="S4 needs exact actions and lifecycle phases; V4 observes only successor existence. Neither candidate proves that control behavior occurred before completion.",
        input_audit="FAIL: brake, steering and sensor action identities, phases, completion events/guards and durations are absent.",
        eligibility="FAIL: simulation is ineligible and a control would invent all behavior needed to make the property true.",
        model_lines=(3, 18),
    ),
}


def _catalog_entry(repo_root: Path, path: Path, *, payload: str | None = None) -> dict[str, str]:
    """Build one repository-relative hash-bound source catalog entry."""

    result = {
        "repository_path": path.resolve().relative_to(repo_root.resolve()).as_posix(),
        "sha256": sha256_path(path),
    }
    if payload is not None:
        result["payload_sha256"] = payload
    return result


def main() -> int:
    """Validate all inputs and write the sealed semantic preflight."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    a_path = gold_root / "review/track_a_independent/batch_04a.json"
    b_path = gold_root / "review/track_b_independent/batch_04a.json"
    a_batch = TrackAProposalBatch.model_validate_json(a_path.read_text(encoding="utf-8"))
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    a_rows = {row.ledger_id: (index, row) for index, row in enumerate(a_batch.rows)}
    b_rows = {row.ledger_id: (index, row) for index, row in enumerate(b_batch.rows)}
    if set(a_rows) != set(b_rows) or set(a_rows) != set(DECISIONS):
        raise ValueError("A/B/Track C batch_04a ledger identities differ")

    pair_ids = tuple(sorted({ledger_id.split("-")[1] for ledger_id in DECISIONS}))
    packets: dict[str, tuple[Path, BlindReviewInputPacket]] = {}
    for pair_id in pair_ids:
        path = gold_root / f"review/input_packets/pairs/{pair_id}.json"
        packet = BlindReviewInputPacket.model_validate_json(path.read_text(encoding="utf-8"))
        if packet.pair_id != pair_id:
            raise ValueError(f"packet pair mismatch for {pair_id}")
        packets[pair_id] = (path, packet)

    source_paths = {
        "capability_audit": gold_root / "predicate_semantics_capability_audit.json",
        "gold_protocol": gold_root / "predicate_gold_protocol.md",
        "predicate_registry": paper_root / "method/src/paper_stm_method/resources/predicate_registry.json",
        "source_static_backend": paper_root / "method/src/paper_stm_method/backends/source_static.py",
        "topology_backend": paper_root / "method/src/paper_stm_method/backends/topology.py",
        "typed_inputs_source": paper_root / "method/src/paper_stm_method/compiler/inputs.py",
        "native_initial_oracle": paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_oracle.py",
        "native_composite": paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_native_composite.py",
        "relation_oracle": paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_relation_oracle.py",
        "execution_runner": paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_execution.py",
        "pyfcstm_model": repo_root / "pyfcstm/pyfcstm/model/model.py",
    }
    source_catalog: dict[str, dict[str, str]] = {
        "track_a_batch": _catalog_entry(repo_root, a_path, payload=a_batch.batch_sha256),
        "track_b_batch": _catalog_entry(repo_root, b_path, payload=b_batch.batch_sha256),
    }
    for source_id, path in source_paths.items():
        source_catalog[source_id] = _catalog_entry(repo_root, path)
    for pair_id, (path, packet) in packets.items():
        source_catalog[f"packet_{pair_id}"] = _catalog_entry(
            repo_root, path, payload=packet.packet_sha256
        )
        model_path = paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        source_catalog[f"model_{pair_id}"] = _catalog_entry(repo_root, model_path)

    rows: list[dict[str, Any]] = []
    for ledger_id in sorted(DECISIONS):
        decision = DECISIONS[ledger_id]
        pair_id = ledger_id.split("-")[1]
        a_index, a_row = a_rows[ledger_id]
        b_index, b_row = b_rows[ledger_id]
        _, packet = packets[pair_id]
        packet_index = next(
            index
            for index, item in enumerate(packet.ledger_items)
            if item.ledger_id == ledger_id
        )
        selected = None
        if decision.candidate_id is not None:
            selected = next(
                item
                for item in b_row.candidate_properties
                if item.candidate_id == decision.candidate_id
            )
        model_ref: dict[str, Any] = {"source_id": f"model_{pair_id}"}
        if decision.model_lines is not None:
            model_ref.update(
                {"line_start": decision.model_lines[0], "line_end": decision.model_lines[1]}
            )
        refs: list[dict[str, Any]] = [
            {"source_id": f"packet_{pair_id}", "json_pointer": f"/ledger_items/{packet_index}"},
            {"source_id": f"packet_{pair_id}", "json_pointer": "/metadata_refs/1/selected_fields"},
            {"source_id": "track_a_batch", "json_pointer": f"/rows/{a_index}"},
            {"source_id": "track_b_batch", "json_pointer": f"/rows/{b_index}"},
            model_ref,
            {"source_id": "capability_audit", "json_pointer": "/predicates"},
        ]
        if decision.execution_mode == "EVALUATION_ONLY_NATIVE_COMPOSITE":
            refs.extend(
                [
                    {"source_id": "native_initial_oracle", "line_start": 1, "line_end": 530},
                    {"source_id": "native_composite", "line_start": 1, "line_end": 520},
                    {"source_id": "pyfcstm_model", "line_start": 1020, "line_end": 1100},
                ]
            )
        elif decision.execution_mode == "EVALUATION_ONLY_NATIVE_ORACLE":
            refs.extend(
                [
                    {"source_id": "native_initial_oracle", "line_start": 1, "line_end": 530},
                    {"source_id": "pyfcstm_model", "line_start": 1020, "line_end": 1100},
                ]
            )
        elif decision.execution_mode == "EVALUATION_ONLY_RELATION":
            refs.append({"source_id": "relation_oracle", "line_start": 1, "line_end": 947})
        elif decision.execution_mode == "FROZEN_S4":
            refs.extend(
                [
                    {"source_id": "source_static_backend", "line_start": 84, "line_end": 196},
                    {"source_id": "typed_inputs_source", "line_start": 96, "line_end": 108},
                    {"source_id": "execution_runner", "line_start": 36, "line_end": 390},
                ]
            )
        row = {
            "ledger_id": ledger_id,
            "pair_id": pair_id,
            "accepted_obligation_source": "TRACK_A_WITH_TRACK_C_CLARIFICATION",
            "normalized_obligation_sha256": canonical_sha256(
                a_row.normalized_obligation.model_dump(mode="json")
            ),
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "selected_candidate_id": decision.candidate_id,
            "selected_candidate_sha256": (
                canonical_sha256(selected.model_dump(mode="json")) if selected else None
            ),
            "track_b_relation": (
                selected.exactness_relation.value
                if selected is not None
                else b_row.proposed_exactness_relation.value
            ),
            "accepted_relation": decision.relation,
            "disposition": decision.disposition,
            "execution_required": decision.candidate_id is not None,
            "execution_mode": decision.execution_mode,
            "implication_analysis": {
                "o_implies_p": decision.relation in {"EQUIVALENT", "O_IMPLIES_P"} if decision.relation else None,
                "p_implies_o": decision.relation == "EQUIVALENT" if decision.relation else None,
                "reason": decision.implication,
            },
            "typed_input_provenance": {
                "status": decision.input_audit.split(":", 1)[0],
                "reason": decision.input_audit,
            },
            "artifact_eligibility": {
                "source_static_eligible": True,
                "simulation_eligible": False,
                "candidate_eligible": decision.candidate_id is not None,
                "reason": decision.eligibility,
            },
            "accepted_obligation": decision.obligation,
            "conflicts": list(decision.conflicts),
            "source_refs": refs,
        }
        row["audit_sha256"] = canonical_sha256(row)
        rows.append(row)

    execution_ids = sorted(
        ledger_id for ledger_id, decision in DECISIONS.items() if decision.candidate_id
    )
    unsupported_ids = sorted(set(DECISIONS) - set(execution_ids))
    unsigned = {
        "schema_version": "paper1.predicate-gold.track-c-preflight.local.v1",
        "schema_documentation": {
            "purpose": "Independent batch_04a semantic preflight frozen before any same-batch property execution; this is not a final TrackCReviewBatch.",
            "row_contract": "Each row adopts one source-first O, checks both implication directions, audits every typed binding and artifact eligibility boundary, and permits execution only for EQUIVALENT or O_IMPLIES_P properties.",
            "relation_values": ["EQUIVALENT", "O_IMPLIES_P", "UNRELATED"],
            "disposition_values": ["EXECUTE_EXACT", "EXECUTE_COMPOSITE_EXACT", "EXECUTE_PROXY", "UNSUPPORTED_EXACT"],
            "execution_boundary": "No provider, method, Judge, 54x3 or v60 actual output is consulted. Evaluation-only oracles use pyfcstm native objects and add no parser or runtime semantics.",
            "canonical_hash_contract": "SHA-256 over canonical UTF-8 JSON with sorted keys, compact separators and ensure_ascii=false; row audit excludes audit_sha256 and batch audit excludes batch_sha256.",
        },
        "batch_id": "batch_04a",
        "reviewer_id": "track_c_semantic_preflight_batch04",
        "reviewed_at": args.reviewed_at,
        "pair_ids": list(pair_ids),
        "ledger_ids": sorted(DECISIONS),
        "visibility": {
            "prior_tracks_visible": True,
            "execution_results_visible": False,
            "v60_actual_visible": False,
            "planned_registry_mapping_visible": False,
            "other_track_c_conclusions_visible": False,
            "final_track_c_rows_created": False,
        },
        "execution_performed": False,
        "source_catalog": source_catalog,
        "input_validation": {
            "raw_file_hashes": "PASS",
            "packet_payload_hashes": "PASS",
            "track_batch_payload_hashes": "PASS",
            "track_proposal_hashes": "PASS",
            "referenced_source_hashes": "PASS",
            "json_pointers": "PASS",
            "row_order_and_identity": "PASS",
            "v60_actual_absence": "PASS",
        },
        "accepted_execution_ids": execution_ids,
        "rejected_relation_ids": unsupported_ids,
        "rows": rows,
    }
    payload = {**unsigned, "batch_sha256": canonical_sha256(unsigned)}
    output = args.output.resolve()
    write_json(output, payload)
    reloaded = json.loads(output.read_text(encoding="utf-8"))
    for row in reloaded["rows"]:
        unsigned_row = {key: value for key, value in row.items() if key != "audit_sha256"}
        if row["audit_sha256"] != canonical_sha256(unsigned_row):
            raise ValueError(f"row seal failed for {row['ledger_id']}")
    unsigned_batch = {
        key: value for key, value in reloaded.items() if key != "batch_sha256"
    }
    if reloaded["batch_sha256"] != canonical_sha256(unsigned_batch):
        raise ValueError("batch_04a preflight seal failed")
    print(f"wrote {output} ({len(rows)} rows, {payload['batch_sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
