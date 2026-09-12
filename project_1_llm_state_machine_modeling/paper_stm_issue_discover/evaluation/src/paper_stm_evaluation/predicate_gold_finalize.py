"""Finalize pane5 predicate-gold arbitration after independent fourth review.

The draft builder deliberately follows Track C. This module closes the later
fourth-review boundary: agreements are confirmed, while every C/fourth status
or implication disagreement must have an explicit source-based pane5 decision.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from paper_stm_evaluation.predicate_gold import (
    ArbitrationRecord,
    ExactnessRelation,
    GoldStatus,
    canonical_sha256,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    HighRiskReviewBatch,
    Pane5ArbitrationBatch,
    Pane5ArbitrationRow,
    TrackCReviewBatch,
)


@dataclass(frozen=True)
class FinalOverride:
    """One evidence-based resolution of a Track C/fourth-review disagreement."""

    status: GoldStatus
    relation: ExactnessRelation
    rationale: str


OVERRIDES: dict[str, FinalOverride] = {
    "DIFF-0039-04": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "One direct initial carrier is sufficient for a sequential implementation, but it is not necessary because the source also permits an orthogonal repair. Its absence therefore cannot falsify O.",
    ),
    "DIFF-0053-01": FinalOverride(
        GoldStatus.SOUND_FALSE_PROXY,
        ExactnessRelation.O_IMPLIES_P,
        "The source expressly requires transition capability among the three operating states. PumpState-to-WaterState topology reachability is therefore necessary, although it omits the other states, triggers and runtime conditions and is not equivalent.",
    ),
    "EIS-0007-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "fcstm_meta explicitly withholds whole-model behavior equivalence and simulation. G1 over the converted topology is therefore not a source-guaranteed necessary condition for the author-level activation obligation.",
    ),
    "EIS-0012-01": FinalOverride(
        GoldStatus.SOUND_FALSE_PROXY,
        ExactnessRelation.O_IMPLIES_P,
        "Stable unbounded waiting in Off requires absence of the observed eventless Off-to-Terminate carrier, but that one forbidden signature is not equivalent to waiting because a different eventless Off departure could still violate O.",
    ),
    "EIS-0013-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "Exactly the three named direct members is a sufficient strict encoding, but the adopted D1 reading permits A/B regional variants of the three main kinds. O therefore does not imply the direct-set candidate.",
    ),
    "EIS-0014-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "One unique direct initial carrier to DoorsClosing is sufficient but not necessary for cold-entry activation; a legal compound initial descent can satisfy O in the same initialization macrostep.",
    ),
    "EIS-0014-02": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "Track A adopts behavioral execution of Accelerate on every entry. A sole incoming-transition effect can satisfy that reading while strict S4 entry-slot membership remains false.",
    ),
    "EIS-0014-03": FinalOverride(
        GoldStatus.SOUND_FALSE_PROXY,
        ExactnessRelation.O_IMPLIES_P,
        "The full obligation requires the Emergency Stop entry action and rejects structural substitution by an accidental Entry child. Missing S4 entry membership falsifies the action conjunct, but S4 true alone is not equivalent to the full obligation.",
    ),
    "EIS-0016-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "The adopted D1 reading requires three distinct usable areas but permits nested topology. Direct-parent equality is neither necessary for that reading nor sufficient for progression and usability.",
    ),
    "INS-0012-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "The obligation permits either genuine termination semantics or removal of the unsupported path. One direct Off-to-root-exit carrier is neither necessary across those repairs nor sufficient for executable termination.",
    ),
    "EIS-0029-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "The obligation requires containment under a source-named owner, not the candidate's stronger immediate-child depth. Falsity of the stronger structural property cannot falsify O.",
    ),
    "EIS-0029-05": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "The obligation requires the source-compatible shared target relation, not one exact direct parent. The candidate narrows valid containment structures and is not O-implied.",
    ),
    "EIS-0034-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "The source fixes containment/shared ownership but does not require the candidate's immediate-child depth. The stronger direct-parent check cannot serve as an exact or sound false proxy.",
    ),
    "EIS-0035-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "A direct authored carrier is not necessary for the RTC obligation because a source-compatible compound pseudostate route may satisfy it in one macrostep.",
    ),
    "EIS-0035-02": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "The direct-edge candidate does not preserve the obligation's event and RTC semantics; a compound pseudostate route can satisfy O while the candidate is false.",
    ),
    "EIS-0044-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "The proposed direct carrier is not necessary under source-compatible compound-transition semantics, so its falsity does not establish the RTC obligation's failure.",
    ),
    "EIS-0046-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "The candidate reduces an event-scoped RTC response to one authored direct edge. Valid pseudostate composition can satisfy O without that edge.",
    ),
    "EIS-0047-02": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.P_IMPLIES_O,
        "One initial carrier is sufficient for the sequential reading but not necessary under the retained orthogonal reading; false cannot reject the valid alternative repair.",
    ),
    "VU-0009-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "fcstm_meta withholds whole-model behavior equivalence, simulation and concurrent-region closure. Root G1 reachability on the converted topology is not an O-implied author-level initialization property.",
    ),
    "VU-0011-01": FinalOverride(
        GoldStatus.UNSUPPORTED_EXACT,
        ExactnessRelation.UNRELATED,
        "A same-RTC response may use a compound pseudostate route, so O does not require one direct event/target carrier. A guarded direct carrier also does not establish feasible event consumption or the next stable configuration.",
    ),
}


def _rows(paths: list[Path], model: type) -> dict[str, object]:
    """Load unique rows from one review track."""

    result: dict[str, object] = {}
    for path in paths:
        batch = model.model_validate_json(path.read_text(encoding="utf-8"))
        for row in batch.rows:
            if row.ledger_id in result:
                raise ValueError(f"duplicate row {row.ledger_id}")
            result[row.ledger_id] = row
    return result


def finalize_batch(
    *,
    draft_path: Path,
    track_c_paths: list[Path],
    high_risk_paths: list[Path],
    arbitrated_at: str,
) -> Pane5ArbitrationBatch:
    """Return a final batch with all fourth-review disagreements resolved."""

    draft = Pane5ArbitrationBatch.model_validate_json(
        draft_path.read_text(encoding="utf-8")
    )
    c_rows = _rows(track_c_paths, TrackCReviewBatch)
    high_risk_rows = _rows(high_risk_paths, HighRiskReviewBatch)
    draft_ids = {row.ledger_id for row in draft.rows}
    if draft_ids != set(c_rows) or draft_ids != set(high_risk_rows):
        raise ValueError("draft, Track C and fourth-review coverage differs")

    rows: list[Pane5ArbitrationRow] = []
    for draft_row in draft.rows:
        ledger_id = draft_row.ledger_id
        c = c_rows[ledger_id]
        high_risk = high_risk_rows[ledger_id]
        disagree = (
            c.proposed_status != high_risk.proposed_status
            or c.proposed_exactness_relation
            != high_risk.proposed_exactness_relation
        )
        override = OVERRIDES.get(ledger_id)
        if disagree and override is None:
            raise ValueError(
                f"{ledger_id} has an unresolved Track C/fourth-review disagreement"
            )
        if not disagree and override is not None:
            raise ValueError(f"{ledger_id} has a stale override despite review agreement")

        if override is None:
            final_status = c.proposed_status
            final_relation = c.proposed_exactness_relation
            decision = (
                "Track C and the independent fourth review agree on this boundary. "
                f"Track C: {c.reason} Independent confirmation: {high_risk.reason}"
            )
        else:
            final_status = override.status
            final_relation = override.relation
            decision = (
                f"Track C proposed {c.proposed_status.value}/{c.proposed_exactness_relation.value}; "
                f"the fourth review proposed {high_risk.proposed_status.value}/{high_risk.proposed_exactness_relation.value}. "
                f"Pane5 resolves the difference as follows: {override.rationale} "
                f"Fourth-review evidence: {high_risk.reason}"
            )

        arbitration = ArbitrationRecord(
            arbitration_id=draft_row.arbitration.arbitration_id,
            adjudicator_id=draft_row.arbitration.adjudicator_id,
            input_sha256=draft_row.arbitration.input_sha256,
            final_status=final_status,
            final_exactness_relation=final_relation,
            reason=(
                f"Pane5 final disposition is {final_status.value}/{final_relation.value}. "
                + decision
            ),
            basis=draft_row.arbitration.basis,
            source_refs=draft_row.arbitration.source_refs,
            sensitivity=draft_row.arbitration.sensitivity,
            arbitrated_at=arbitrated_at,
        )
        conflicts = []
        for conflict in draft_row.conflicts:
            payload = conflict.model_dump(mode="json")
            payload["resolution"] = (
                f"Pane5 final disposition is {final_status.value}/{final_relation.value}. "
                + (override.rationale if override is not None else "The two post-execution semantic reviews agree; the listed position remains a disclosed sensitivity only.")
            )
            conflicts.append(type(conflict).model_validate(payload))
        unsigned = {
            "ledger_id": ledger_id,
            "track_a_opinion_sha256": draft_row.track_a_opinion_sha256,
            "track_b_opinion_sha256": draft_row.track_b_opinion_sha256,
            "track_c_opinion_sha256": draft_row.track_c_opinion_sha256,
            "high_risk_opinion_sha256": draft_row.high_risk_opinion_sha256,
            "conflicts": [item.model_dump(mode="json") for item in conflicts],
            "arbitration": arbitration.model_dump(mode="json"),
        }
        rows.append(
            Pane5ArbitrationRow(
                **unsigned, row_sha256=canonical_sha256(unsigned)
            )
        )

    unsigned_batch = {
        "schema_version": draft.schema_version,
        "batch_id": draft.batch_id.replace("-draft", "-final"),
        "pair_ids": list(draft.pair_ids),
        "rows": [row.model_dump(mode="json") for row in rows],
        "arbitrated_at": arbitrated_at,
    }
    return Pane5ArbitrationBatch(
        **unsigned_batch, batch_sha256=canonical_sha256(unsigned_batch)
    )


def main(argv: list[str] | None = None) -> int:
    """Finalize one hash-bound arbitration draft."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--track-c", type=Path, action="append", required=True)
    parser.add_argument("--high-risk", type=Path, action="append", required=True)
    parser.add_argument("--arbitrated-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    batch = finalize_batch(
        draft_path=args.draft,
        track_c_paths=args.track_c,
        high_risk_paths=args.high_risk,
        arbitrated_at=args.arbitrated_at,
    )
    write_json(args.output, batch.model_dump(mode="json"))
    print(f"wrote {args.output} ({len(batch.rows)} rows, {batch.batch_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
