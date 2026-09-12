"""Build the hash-bound pane5 arbitration record for predicate-gold pilot pair 0000."""

from __future__ import annotations

import argparse
from pathlib import Path

from paper_stm_evaluation.predicate_gold import (
    ArbitrationRecord,
    ConflictRecord,
    ExactnessRelation,
    GoldStatus,
    SourceRef,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    ARBITRATION_SCHEMA_VERSION,
    Pane5ArbitrationBatch,
    Pane5ArbitrationRow,
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCReviewBatch,
)


def _ref(
    repo_root: Path,
    path: Path,
    *,
    pointer: str | None = None,
    lines: tuple[int, int] | None = None,
    element: str | None = None,
) -> SourceRef:
    """Create one stable reference to evidence read during arbitration."""

    return SourceRef(
        repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        line_start=lines[0] if lines else None,
        line_end=lines[1] if lines else None,
        model_element=element,
        excerpt=None,
    )


def _conflict(
    *,
    conflict_id: str,
    opinion_ids: tuple[str, ...],
    disputed_fields: tuple[str, ...],
    positions: tuple[str, ...],
    refs: tuple[SourceRef, ...],
    resolution: str,
) -> ConflictRecord:
    """Build one explicit conflict without collapsing positions by vote."""

    return ConflictRecord(
        conflict_id=conflict_id,
        opinion_ids=opinion_ids,
        disputed_fields=disputed_fields,
        positions=positions,
        additional_evidence_refs=refs,
        resolution=resolution,
    )


def main() -> int:
    """Read pilot reviews, write arbitration JSON, and validate its hashes."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--arbitrated-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix" / "ledger_v2" / "predicate_gold_v1"
    a_path = gold_root / "review" / "pilot_independent" / "track_a_pair_0000.json"
    b_path = gold_root / "review" / "pilot_independent" / "track_b_pair_0000.json"
    c_path = gold_root / "review" / "track_c_independent" / "pilot_pair_0000.json"
    packet_path = gold_root / "review" / "input_packets" / "pairs" / "0000.json"
    nl_path = paper_root / "selected_seed_examples" / "llms_emp_feedback_final_0000" / "nl.txt"
    artifact_path = paper_root / "selected_seed_examples" / "llms_emp_feedback_final_0000" / "model.fcstm"
    a_batch = TrackAProposalBatch.model_validate_json(a_path.read_text(encoding="utf-8"))
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    c_batch = TrackCReviewBatch.model_validate_json(c_path.read_text(encoding="utf-8"))
    a_rows = {row.ledger_id: row for row in a_batch.rows}
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    c_rows = {row.ledger_id: row for row in c_batch.rows}
    if set(a_rows) != set(b_rows) or set(a_rows) != set(c_rows):
        raise ValueError("pilot Track A/B/C ledger IDs differ")

    shared_refs = (
        _ref(repo_root, packet_path, pointer="/ledger_items", element="pair 0000 blind source packet"),
        _ref(repo_root, nl_path, lines=(1, 1), element="pair 0000 author NL"),
        _ref(repo_root, artifact_path, lines=(1, 22), element="pair 0000 defective FCSTM"),
        _ref(repo_root, a_path, pointer="/rows", element="pilot Track A opinions"),
        _ref(repo_root, b_path, pointer="/rows", element="pilot Track B proposals"),
        _ref(repo_root, c_path, pointer="/rows", element="pilot Track C opinions"),
    )
    rows: list[Pane5ArbitrationRow] = []

    for ledger_id in sorted(a_rows):
        a_row = a_rows[ledger_id]
        b_row = b_rows[ledger_id]
        c_row = c_rows[ledger_id]
        input_sha = canonical_sha256(
            {
                "ledger_id": ledger_id,
                "track_a": a_row.proposal_sha256,
                "track_b": b_row.proposal_sha256,
                "track_c": c_row.opinion_sha256,
                "evidence": [ref.sha256 for ref in shared_refs],
            }
        )
        opinion_ids = (
            f"{a_batch.reviewer_id}:{ledger_id}",
            f"{b_batch.reviewer_id}:{ledger_id}",
            f"{c_batch.reviewer_id}:{ledger_id}",
        )

        if ledger_id == "EIS-0000-01":
            conflicts = (
                _conflict(
                    conflict_id="predicate-gold-v1:EIS-0000-01:relation",
                    opinion_ids=opinion_ids[1:],
                    disputed_fields=("exactness_relation", "gold_status", "execution_interpretation"),
                    positions=(
                        "Track B proposed O_IMPLIES_P: every running mode needs a direct root-owned Power_Off-to-exit carrier.",
                        "Track C found UNRELATED: O permits semantically equivalent compound/leaf-local RTC termination routes and P ignores reachability, guards and dispatch.",
                    ),
                    refs=shared_refs,
                    resolution="Track C's implication analysis is adopted. A required response does not entail one direct-carrier encoding, so the completed false receipt is evidence only against the rejected P.",
                ),
                _conflict(
                    conflict_id="predicate-gold-v1:EIS-0000-01:final-observable",
                    opinion_ids=(opinion_ids[0], opinion_ids[1]),
                    disputed_fields=("normalized_obligation", "alternative_reading"),
                    positions=(
                        "Track A rejects an ordinary named FinalState as satisfying final-state semantics.",
                        "Track B retains the named FinalState reading as source-compatible sensitivity while adopting true root termination.",
                    ),
                    refs=shared_refs[:3],
                    resolution="True completion/termination remains the adopted ledger reading. The ordinary named-state interpretation is retained only as a D2-adjacent source-language sensitivity and does not supply an executable exact property.",
                ),
            )
            final_status = GoldStatus.UNSUPPORTED_EXACT
            relation = ExactnessRelation.UNRELATED
            reason = "No reviewed executable property is equivalent to the runtime Power_Off-to-true-termination obligation. The executed root-direct-carrier oracle adds an encoding constraint that O does not require, so its completed false result cannot serve even as a sound false proxy."
            basis = "Author NL requires a runtime Power Off response; the source and FCSTM distinguish initial, running and named FinalState objects. Track C verified the static execution/control/replay but demonstrated that direct root-owned carriers neither follow from nor establish the RTC termination obligation."
            sensitivity = (
                "The author phrase 'final state' can be read as a named business state, but the ledger and formal-semantics reading requires actual state-machine completion.",
                "An exact future oracle needs reachable-configuration quantification, Power_Off dispatch, guard/priority semantics and whole-machine termination observation.",
            )
        elif ledger_id == "EIS-0000-02":
            conflicts = (
                _conflict(
                    conflict_id="predicate-gold-v1:EIS-0000-02:connective",
                    opinion_ids=opinion_ids,
                    disputed_fields=("normalized_obligation", "typed_inputs", "exactness_relation", "gold_status"),
                    positions=(
                        "Track A retains disjunctive and conjunctive source-compatible readings because the comma supplies no connective.",
                        "Track B adopts disjunction and proposes exact independent event tokens plus an AutoFinal route as O_IMPLIES_P.",
                        "Track C finds the connective unresolved and the exact tokens/three-route encoding neither source-bound nor implied by either retained reading.",
                    ),
                    refs=shared_refs,
                    resolution="Track A's dual-reading D1 obligation is retained. The static three-route property is UNRELATED because it invents canonical event identities and one representation; the valid false/control/replay receipts do not resolve the connective or source binding.",
                ),
            )
            final_status = GoldStatus.UNSUPPORTED_EXACT
            relation = ExactnessRelation.UNRELATED
            reason = "The source does not decide whether the steering, brake and AutoFinal conditions are disjunctive or conjunctive, and it does not mandate the oracle's exact event tokens or three separate carriers. The executed property therefore cannot be exact or a sound necessary-condition proxy."
            basis = "The D1 packet preserves both complete readings. Track C checked that the static oracle and its control/replay executed correctly, then showed that literal token equality, independent event declarations and eventless AutoFinal routing are representation choices absent from O and insufficient for RTC feasibility."
            sensitivity = (
                "Disjunctive and conjunctive takeover readings remain source-compatible and lead to different executable response properties.",
                "An exact future oracle needs a source-authorized connective, input vocabulary and RTC observation model rather than FCSTM token invention.",
            )
        else:
            conflicts = (
                _conflict(
                    conflict_id="predicate-gold-v1:INS-0000-04:cardinality",
                    opinion_ids=opinion_ids,
                    disputed_fields=("normalized_obligation", "property_scope"),
                    positions=(
                        "Track A limits O to trigger/guard absence on the complete two-carrier root inventory and does not add uniqueness.",
                        "Track B describes a nonempty default-entry clause while selecting the same two-carrier S3/S5 conjunction.",
                        "Track C accepts only the Track A reading and verifies exactness for the frozen two-carrier inventories, without generalizing cardinality.",
                    ),
                    refs=shared_refs,
                    resolution="Track A's obligation is adopted. The four constituents quantify over exactly the independently enumerated root carriers at FCSTM lines 19 and 21; no uniqueness or future-model claim is added.",
                ),
            )
            final_status = GoldStatus.COMPOSITE_EXACT_FALSE
            relation = ExactnessRelation.EQUIVALENT
            reason = "For the hash-bound defective artifact, the complete root initial-carrier inventory is lines 19 and 21. The non-short-circuit conjunction applies S3(event set is empty) and S5(guard is absent) to both carriers, exactly matching O without adding a cardinality rule."
            basis = "Track C independently reconstructed root.init_transitions, excluded the nested line-12 carrier, accepted every native binding, and verified defective [false,true,false,true], control [true,true,true,true], all child receipts, parent verdict and matching replay."
            sensitivity = (
                "Exactness is artifact-scoped; any changed FCSTM must re-enumerate root.init_transitions before reuse.",
                "The current false is caused by event attachments on both carriers; the true S5 constituents do not assert a guard defect.",
                "Future Track C packets should enumerate every receipt code_hash dependency directly, although all referenced receipt bytes and semantic replays were verified here.",
            )

        arbitration = ArbitrationRecord(
            arbitration_id=f"predicate-gold-v1:{ledger_id}",
            adjudicator_id="pane5:manual-supervised-adjudicator",
            input_sha256=input_sha,
            final_status=final_status,
            final_exactness_relation=relation,
            reason=reason,
            basis=basis,
            source_refs=shared_refs,
            sensitivity=sensitivity,
            arbitrated_at=args.arbitrated_at,
        )
        unsigned_row = {
            "ledger_id": ledger_id,
            "track_a_opinion_sha256": a_row.proposal_sha256,
            "track_b_opinion_sha256": b_row.proposal_sha256,
            "track_c_opinion_sha256": c_row.opinion_sha256,
            "conflicts": [item.model_dump(mode="json") for item in conflicts],
            "arbitration": arbitration.model_dump(mode="json"),
        }
        rows.append(Pane5ArbitrationRow(**unsigned_row, row_sha256=canonical_sha256(unsigned_row)))

    unsigned_batch = {
        "schema_version": ARBITRATION_SCHEMA_VERSION,
        "batch_id": "pilot_pair_0000",
        "pair_ids": ["0000"],
        "rows": [row.model_dump(mode="json") for row in rows],
        "arbitrated_at": args.arbitrated_at,
    }
    batch = Pane5ArbitrationBatch(**unsigned_batch, batch_sha256=canonical_sha256(unsigned_batch))
    output = gold_root / "review" / "arbitration" / "pilot_pair_0000.json"
    write_json(output, batch.model_dump(mode="json"))
    Pane5ArbitrationBatch.model_validate_json(output.read_text(encoding="utf-8"))
    print(f"wrote {output} ({len(batch.rows)} rows, {batch.batch_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
