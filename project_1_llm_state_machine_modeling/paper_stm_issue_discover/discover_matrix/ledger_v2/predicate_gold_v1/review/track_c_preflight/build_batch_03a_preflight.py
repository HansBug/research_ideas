"""Build the independent source-first Track C semantic preflight for batch 03a."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from paper_stm_evaluation.predicate_gold import canonical_sha256, sha256_path, write_json
from paper_stm_evaluation.predicate_gold_review import TrackAProposalBatch, TrackBProposalBatch


@dataclass(frozen=True)
class Decision:
    """Track C decision frozen before same-issue execution output is visible."""

    obligation: str
    implication: str
    input_audit: str
    eligibility: str
    candidate_id: str | None = None
    relation: str | None = None
    disposition: str = "UNSUPPORTED_EXACT"
    execution_mode: str = "NONE"
    conflicts: tuple[str, ...] = ()


DECISIONS: dict[str, Decision] = {
    "INS-0011-02": Decision(
        obligation="A reachable ClampingLoseState may be removed or must expose a genuine continuation/termination; no event, destination, fairness rule or finite runtime bound is supplied.",
        implication="The source-static property 'state absent/unreachable OR at least one authored outgoing carrier' is necessary for the adopted nonblocking obligation. It is not sufficient because carrier feasibility and scheduling are not executed.",
        input_audit="PASS: exact state and root paths come from the author FCSTM; deletion is an explicit ledger-supported repair, and no recovery event or target is invented.",
        eligibility="PASS as O_IMPLIES_P only: the oracle uses pyfcstm state/carrier objects and guard-agnostic reachability solely as a falsifier.",
        candidate_id="ins0011-02-native-static-outgoing-carrier",
        relation="O_IMPLIES_P",
        disposition="EXECUTE_PROXY",
        execution_mode="EVALUATION_ONLY_NATIVE_CONTRACT",
        conflicts=("Track C makes the deletion branch explicit so the positive control does not invent an unsupported recovery transition; the property remains a proxy, not runtime nonblocking proof.",),
    ),
    "VU-0011-01": Decision(
        obligation="While reachable ClampingState is active, Signal_Feedback_Sent must support the author-specified reset to InitialState in the response RTC.",
        implication="An exact ClampingState/Signal_Feedback_Sent/InitialState carrier is necessary but cannot prove guard feasibility, event dispatch or next-stable-state behavior.",
        input_audit="PASS: source, event and target are exact author identities with no guessed bound or alias.",
        eligibility="PASS as O_IMPLIES_P: REQUIRED_SIGNATURE_PRESENT enumerates complete native carriers without claiming execution semantics.",
        candidate_id="vu0011-01-native-static-feedback-carrier",
        relation="O_IMPLIES_P",
        disposition="EXECUTE_PROXY",
        execution_mode="EVALUATION_ONLY_RELATION",
    ),
    "EIS-0012-01": Decision(
        obligation="Off must remain a stable waiting state and therefore must not expose the exact eventless Off-to-ordinary-Terminate completion carrier.",
        implication="Absence of that exact owner/source/target/empty-event carrier is equivalent to the adopted artifact-bound prohibition; it does not define an alternative shutdown trigger.",
        input_audit="PASS: owner, Off, ordinary Terminate and the empty native event set are exact submitted identities.",
        eligibility="PASS: the native contract enumerates pyfcstm carriers and checks the empty event collection directly.",
        candidate_id="eis0012-01-native-no-eventless-off-terminate",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="EVALUATION_ONLY_NATIVE_CONTRACT",
    ),
    "INS-0012-01": Decision(
        obligation="The submitted final branch must be an exact root-owner authored direct carrier from Off to the native [*] exit boundary.",
        implication="S2 with source Off, target [*] and root scope is equivalent to this explicitly direct source obligation; ordinary state display text cannot satisfy it.",
        input_audit="PASS: source, true-exit marker and owner scope are exact and require no fabricated transition identity.",
        eligibility="PASS: frozen S2 checks authored direct carriers only, matching the obligation granularity.",
        candidate_id="ins0012-01-s2-off-root-exit",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="FROZEN_PREDICATE",
    ),
    "EIS-0013-01": Decision(
        obligation="PumpControl must preserve exactly the three main semantic kinds PumpState, WaterState and MethaneState; the source does not settle concrete-vertex or region cardinality.",
        implication="Track B's exact direct-child set is stronger than the adopted kind-level D1 obligation. O permits A/B regional variants, so O does not imply that property and its false result cannot establish O false.",
        input_audit="FAIL: no source-backed classifier maps variant vertices to main kinds or fixes concrete-vertex/region cardinality.",
        eligibility="FAIL: exact child-set execution would answer the retained strict-vertex sensitivity, not the adopted obligation.",
        conflicts=("Track A adopts main kinds while Track B selects exactly three direct concrete members; Track C preserves the material D1 distinction and does not execute the stronger property.",),
    ),
    "EIS-0014-01": Decision(
        obligation="The root must have exactly one triggerless and guardless native initial carrier targeting DoorsClosing.",
        implication="The complete native initial-transition contract is equivalent because it checks owner, cardinality, target, event absence and guard absence together.",
        input_audit="PASS: root and DoorsClosing paths and absent event/guard are exact source facts.",
        eligibility="PASS: the evaluation-only native oracle reads State.init_transitions and exact pyfcstm identities.",
        candidate_id="eis0014-01-native-root-initial-target",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="EVALUATION_ONLY_NATIVE_ORACLE",
    ),
    "EIS-0014-02": Decision(
        obligation="Accelerate must be attached to the entry lifecycle slot of Accelerating.",
        implication="S4 on the exact state, entry phase and action token is equivalent to this source-static attachment obligation; no physical execution claim is added.",
        input_audit="PASS: state, phase and action are explicitly authored.",
        eligibility="PASS: frozen S4 reads the exact native entry collection.",
        candidate_id="eis0014-02-s4-accelerating-entry",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="FROZEN_PREDICATE",
    ),
    "EIS-0014-03": Decision(
        obligation="On entry to EmergencyStopping, the model must attach the Emergency Stop action; an accidental Entry child is not a substitute.",
        implication="Under Track A's source reading, entry-S4 is equivalent. Track B's any-phase OR is weaker because do/exit attachment would not satisfy the same-entry RTC obligation.",
        input_audit="PASS: EmergencyStopping, entry and Emergency Stop come from the author NL/PlantUML role statement.",
        eligibility="PASS: frozen S4 checks exact lifecycle attachment; Track C corrects the candidate relation before execution.",
        candidate_id="eis0014-03-s4-entry-only",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="FROZEN_PREDICATE",
        conflicts=("Track B treats phase as unspecified and selects an OR over entry/do/exit; Track A's RTC reading fixes entry. Track C adopts the source-anchored entry reading and records the disagreement.",),
    ),
    "EIS-0014-04": Decision(
        obligation="Every Approaching episode must emit Send while active; phase, repetition and delivery details are not supplied.",
        implication="A lifecycle/effect carrier with the Send token is a necessary source-static representation condition, but its presence does not prove runtime emission or delivery.",
        input_audit="PASS: owner and output token are author identities; all lifecycle/effect slots are inspected without choosing one.",
        eligibility="PASS as O_IMPLIES_P only: native action/effect inspection is a sound static falsifier under the in-artifact output representation.",
        candidate_id="eis0014-04-native-output-carrier",
        relation="O_IMPLIES_P",
        disposition="EXECUTE_PROXY",
        execution_mode="EVALUATION_ONLY_NATIVE_CONTRACT",
        conflicts=("Track B calls static carrier presence equivalent; Track C retains the runtime occurrence/delivery gap and downgrades the relation before execution.",),
    ),
    "VU-0014-01": Decision(
        obligation="Obstacle Detected input must lead to a distinct Obstacle Detected output attributable to EmergencyStopping; the input event declaration cannot satisfy the output role.",
        implication="An EmergencyStopping lifecycle/effect output carrier is necessary but does not prove same-RTC output occurrence or delivery.",
        input_audit="PASS: owner and output token are explicit; the oracle excludes event declarations by construction.",
        eligibility="PASS as O_IMPLIES_P only: native action/effect inspection preserves role but remains source-static.",
        candidate_id="vu0014-01-native-role-sensitive-output-carrier",
        relation="O_IMPLIES_P",
        disposition="EXECUTE_PROXY",
        execution_mode="EVALUATION_ONLY_NATIVE_CONTRACT",
        conflicts=("Track B treats carrier presence as equivalent; Track C preserves the RTC occurrence/delivery dimension and records only a sound falsifier.",),
    ),
    "EIS-0015-01": Decision(
        obligation="Cooking-time value, display and update/cancel behavior must be observable, while representation, type, domain and operation identities remain unspecified.",
        implication="The existence of any variable and any action is not a sound issue-specific falsifier without a binding to cooking time; unrelated declarations could make it true while O remains false.",
        input_audit="FAIL: variable identity, type/domain, display/update operation, lifecycle slot and external-HMI boundary are absent.",
        eligibility="FAIL: a positive control would have to invent decisive data and action identities; no query is executed.",
        conflicts=("Track B proposes a generic inventory proxy. Track C rejects it because 'capable of carrying' has no native, source-bound relation to cooking-time semantics.",),
    ),
    "DIFF-0016-05": Decision(
        obligation="The root initial carrier must have an empty trigger set and no guard AST.",
        implication="The non-short-circuit conjunction S3(empty triggers) AND S5(absent guard) is equivalent to the finite two-field language obligation.",
        input_audit="PASS: transition:line:61 is the exact native root initial carrier and both expected fields are explicit absences.",
        eligibility="PASS: frozen S3/S5 execute independently and the composite persists every constituent.",
        candidate_id="diff0016-05-composite-s3-s5",
        relation="EQUIVALENT",
        disposition="EXECUTE_COMPOSITE_EXACT",
        execution_mode="FROZEN_COMPOSITE",
    ),
    "EIS-0016-01": Decision(
        obligation="Region1, Region2 and Region3 must each be direct sibling states under SearchMission.",
        implication="Checking the exact parent and all three required direct children is equivalent to this adopted hierarchy obligation; no concurrency runtime claim is added.",
        input_audit="PASS: all four state identities are explicitly authored.",
        eligibility="PASS: DIRECT_CHILD_HIERARCHY uses pyfcstm parent/substate identity and does not infer by names or topology.",
        candidate_id="eis0016-01-native-parent-map",
        relation="EQUIVALENT",
        disposition="EXECUTE_EXACT",
        execution_mode="EVALUATION_ONLY_RELATION",
    ),
    "EIS-0016-02": Decision(
        obligation="Each required region needs a source-defined valid initial target, but the target identities are absent.",
        implication="Placeholder identities and one global Search declaration do not express the owner-local target obligations.",
        input_audit="FAIL: Region2/Region3 intended target names and valid owner-local bindings are missing.",
        eligibility="FAIL: any executable query or positive control would invent target identities or treat projection diagnostics as requirements.",
    ),
    "EIS-0016-03": Decision(
        obligation="Search must continue until a source-defined mission-completion condition and then reach a source-defined outcome; Region3 completion equivalence remains D1-sensitive.",
        implication="No candidate binds the missing completion proposition, post-condition, unbounded scope or fairness assumptions.",
        input_audit="FAIL: antecedent, response/termination, bound, schedule and fairness are missing.",
        eligibility="FAIL: substituting Finished_Region3_Search would erase the retained D1 reading; no execution occurs.",
    ),
    "INS-0017-01": Decision(
        obligation="All three region-local initial carriers must be triggerless and guardless during parent entry.",
        implication="The non-short-circuit conjunction of S3(empty) and S5(absent) for lines 12, 14 and 16 is equivalent to the six-field finite obligation.",
        input_audit="PASS: the three exact carrier refs and both absence values are source-bound.",
        eligibility="PASS: every S3/S5 constituent executes and is persisted regardless of earlier false values.",
        candidate_id="ins0017-01-composite-all-s3-s5",
        relation="EQUIVALENT",
        disposition="EXECUTE_COMPOSITE_EXACT",
        execution_mode="FROZEN_COMPOSITE",
    ),
    "VU-0017-01": Decision(
        obligation="Collision detections activate the sub-machine, but the adopted source-minimal reading permits activation by an external parent not present in this file.",
        implication="A local incoming/root carrier is not necessary under the adopted external-entry reading, so the Track B property is unrelated to O rather than equivalent.",
        input_audit="FAIL: local source, external parent, entry point and ownership boundary are unspecified.",
        eligibility="FAIL: executing a self-contained incoming-carrier check would answer only the retained D1 sensitivity.",
        conflicts=("Track A adopts external sub-machine entry while Track B selects a local incoming-carrier property. Track C follows the adopted reading and leaves local reachability as sensitivity.",),
    ),
}


def _repo_root(path: Path) -> Path:
    return next(parent for parent in path.resolve().parents if (parent / "pyfcstm").is_dir())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--reviewed-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    a_path = gold_root / "review/track_a_independent/batch_03a.json"
    b_path = gold_root / "review/track_b_independent/batch_03a.json"
    a_batch = TrackAProposalBatch.model_validate_json(a_path.read_text(encoding="utf-8"))
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    a_rows = {row.ledger_id: (index, row) for index, row in enumerate(a_batch.rows)}
    b_rows = {row.ledger_id: (index, row) for index, row in enumerate(b_batch.rows)}
    if set(a_rows) != set(b_rows) or set(a_rows) != set(DECISIONS):
        raise ValueError("Track A/B/decision identity mismatch")
    rows = []
    for ledger_id in sorted(DECISIONS):
        decision = DECISIONS[ledger_id]
        a_index, a_row = a_rows[ledger_id]
        b_index, b_row = b_rows[ledger_id]
        pair_id = ledger_id.split("-")[1]
        packet = gold_root / f"review/input_packets/pairs/{pair_id}.json"
        model = paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        normalized_hash = canonical_sha256(a_row.normalized_obligation.model_dump(mode="json"))
        selected_hash = None
        if decision.candidate_id:
            candidates = [item for item in b_row.candidate_properties if item.candidate_id == decision.candidate_id]
            if len(candidates) != 1:
                raise ValueError(f"{ledger_id} candidate resolution failed")
            selected_hash = canonical_sha256(candidates[0].model_dump(mode="json"))
        unsigned = {
            "ledger_id": ledger_id,
            "pair_id": pair_id,
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "normalized_obligation_sha256": normalized_hash,
            "accepted_obligation": decision.obligation,
            "accepted_obligation_source": "TRACK_A_WITH_TRACK_C_ARBITRATION",
            "selected_candidate_id": decision.candidate_id,
            "selected_candidate_sha256": selected_hash,
            "track_b_relation": b_row.proposed_exactness_relation.value,
            "accepted_relation": decision.relation,
            "implication_analysis": {
                "o_implies_p": decision.relation in {"EQUIVALENT", "O_IMPLIES_P"},
                "p_implies_o": decision.relation == "EQUIVALENT",
                "reason": decision.implication,
            },
            "typed_input_provenance": {"status": "PASS" if decision.disposition != "UNSUPPORTED_EXACT" else "FAIL", "reason": decision.input_audit},
            "artifact_eligibility": {
                "candidate_eligible": decision.disposition != "UNSUPPORTED_EXACT",
                "source_static_eligible": decision.disposition != "UNSUPPORTED_EXACT",
                "simulation_eligible": False,
                "reason": decision.eligibility,
            },
            "disposition": decision.disposition,
            "execution_mode": decision.execution_mode,
            "execution_required": decision.disposition != "UNSUPPORTED_EXACT",
            "conflicts": list(decision.conflicts),
            "source_refs": [
                {"source_id": "pair_packet", "json_pointer": f"/ledger_items/{next(i for i,item in enumerate(json.loads(packet.read_text(encoding='utf-8'))['ledger_items']) if item['ledger_id']==ledger_id)}"},
                {"source_id": "track_a_batch", "json_pointer": f"/rows/{a_index}"},
                {"source_id": "track_b_batch", "json_pointer": f"/rows/{b_index}"},
                {"source_id": "author_fcstm", "line_start": 1, "line_end": len(model.read_text(encoding="utf-8").splitlines())},
            ],
        }
        rows.append({**unsigned, "audit_sha256": canonical_sha256(unsigned)})
    source_catalog = {
        "pair_packet_pattern": "review/input_packets/pairs/{pair_id}.json",
        "track_a_batch": {"path": a_path.relative_to(repo_root).as_posix(), "sha256": sha256_path(a_path), "batch_sha256": a_batch.batch_sha256},
        "track_b_batch": {"path": b_path.relative_to(repo_root).as_posix(), "sha256": sha256_path(b_path), "batch_sha256": b_batch.batch_sha256},
        "capability_audit": {"path": "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/predicate_semantics_capability_audit.json", "sha256": sha256_path(gold_root / "predicate_semantics_capability_audit.json")},
    }
    unsigned_batch = {
        "schema_version": "paper1.predicate-gold.track-c-preflight.local.v1",
        "batch_id": "batch_03a",
        "reviewer_id": "track_c_independent_batch_03a",
        "review_contract": {
            "purpose": "Independent source-first O/P and typed-input audit before any same-issue execution result is visible.",
            "v60_actual_visible": False,
            "execution_results_visible": False,
            "boolean_false_establishes_exactness": False,
        },
        "source_catalog": source_catalog,
        "rows": rows,
        "reviewed_at": args.reviewed_at,
    }
    output = gold_root / "review/track_c_preflight/batch_03a.json"
    write_json(output, {**unsigned_batch, "batch_sha256": canonical_sha256(unsigned_batch)})
    print(f"wrote {output} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
