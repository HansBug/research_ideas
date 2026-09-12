"""Build hash-bound pane5 arbitration batches from four independent reviews.

This module is evaluation-only.  It never imports the method pipeline, reads v60
actual predicate output, or executes a provider.  The generated batch is an
auditable draft: pane5 must read every row and may amend the evidence-based
decision before the batch is selected by the active review manifest.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    ArbitrationRecord,
    ConflictRecord,
    GoldStatus,
    SourceRef,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    ARBITRATION_SCHEMA_VERSION,
    HighRiskReviewBatch,
    HighRiskReviewRow,
    Pane5ArbitrationBatch,
    Pane5ArbitrationRow,
    PreExecutionDisposition,
    TrackAProposalBatch,
    TrackAProposalRow,
    TrackBProposalBatch,
    TrackBProposalRow,
    TrackCReviewBatch,
    TrackCReviewRow,
)


def _repo_ref(
    repo_root: Path,
    path: Path,
    *,
    pointer: str | None,
    element: str,
) -> SourceRef:
    """Return a stable reference to one selected review or source packet."""

    return SourceRef(
        repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        line_start=None,
        line_end=None,
        model_element=element,
        excerpt=None,
    )


def _rows(paths: list[Path], model: type[Any]) -> tuple[dict[str, Any], dict[str, tuple[Path, int]]]:
    """Load unique review rows and retain their file/pointer locations."""

    values: dict[str, Any] = {}
    locations: dict[str, tuple[Path, int]] = {}
    for path in paths:
        batch = model.model_validate_json(path.read_text(encoding="utf-8"))
        for index, row in enumerate(batch.rows):
            if row.ledger_id in values:
                raise ValueError(f"duplicate review row {row.ledger_id}")
            values[row.ledger_id] = row
            locations[row.ledger_id] = (path, index)
    return values, locations


def _b_status(disposition: PreExecutionDisposition) -> GoldStatus:
    """Map Track B's conditional pre-result disposition to a final-status name."""

    return {
        PreExecutionDisposition.EXACT_EXECUTION_CANDIDATE: GoldStatus.EXACT_FALSE,
        PreExecutionDisposition.COMPOSITE_EXACT_EXECUTION_CANDIDATE: GoldStatus.COMPOSITE_EXACT_FALSE,
        PreExecutionDisposition.PROXY_EXECUTION_CANDIDATE: GoldStatus.SOUND_FALSE_PROXY,
        PreExecutionDisposition.UNSUPPORTED_EXACT_CANDIDATE: GoldStatus.UNSUPPORTED_EXACT,
    }[disposition]


def _conflicts(
    *,
    ledger_id: str,
    a: TrackAProposalRow,
    b: TrackBProposalRow,
    c: TrackCReviewRow,
    high_risk: HighRiskReviewRow,
    refs: tuple[SourceRef, ...],
    a_reviewer: str,
    b_reviewer: str,
    c_reviewer: str,
    high_risk_reviewer: str,
) -> tuple[ConflictRecord, ...]:
    """Retain substantive review differences without treating them as a vote."""

    records: list[ConflictRecord] = []
    b_status = _b_status(b.proposed_disposition)
    if b_status != c.proposed_status or b.proposed_exactness_relation != c.proposed_exactness_relation:
        records.append(
            ConflictRecord(
                conflict_id=f"predicate-gold-v1:{ledger_id}:property-disposition",
                opinion_ids=(
                    f"{b_reviewer}:{ledger_id}",
                    f"{c_reviewer}:{ledger_id}",
                ),
                disputed_fields=("gold_status", "exactness_relation"),
                positions=(
                    f"Track B froze {b_status.value}/{b.proposed_exactness_relation.value} before execution: {b.reason}",
                    f"Track C concluded {c.proposed_status.value}/{c.proposed_exactness_relation.value} after source, binding, execution/control and replay review: {c.reason}",
                ),
                additional_evidence_refs=refs,
                resolution=(
                    "Pane5 adopts the post-execution implication analysis only because its cited source and backend evidence resolves the O/P boundary; "
                    f"the Boolean result itself is not the reason. {c.basis}"
                ),
            )
        )
    if (
        c.proposed_status != high_risk.proposed_status
        or c.proposed_exactness_relation != high_risk.proposed_exactness_relation
    ):
        records.append(
            ConflictRecord(
                conflict_id=f"predicate-gold-v1:{ledger_id}:fourth-review-disposition",
                opinion_ids=(
                    f"{c_reviewer}:{ledger_id}",
                    f"{high_risk_reviewer}:{ledger_id}",
                ),
                disputed_fields=("gold_status", "exactness_relation"),
                positions=(
                    f"Track C proposed {c.proposed_status.value}/{c.proposed_exactness_relation.value}: {c.reason}",
                    f"The independent fourth review proposed {high_risk.proposed_status.value}/{high_risk.proposed_exactness_relation.value}: {high_risk.reason}",
                ),
                additional_evidence_refs=refs,
                resolution=(
                    "The generated arbitration row retains both source-backed positions for pane5's issue-specific decision; "
                    "neither reviewer count nor the observed Boolean result resolves the O/P implication direction."
                ),
            )
        )
    if not c.obligation_accepted:
        records.append(
            ConflictRecord(
                conflict_id=f"predicate-gold-v1:{ledger_id}:obligation-reading",
                opinion_ids=(
                    f"{a_reviewer}:{ledger_id}",
                    f"{b_reviewer}:{ledger_id}",
                    f"{c_reviewer}:{ledger_id}",
                ),
                disputed_fields=("normalized_obligation", "alternative_readings"),
                positions=(a.reason, b.reason, c.reason),
                additional_evidence_refs=refs,
                resolution=(
                    "Pane5 retains Track A's source-first normalized obligation and records Track C's objection as sensitivity; "
                    "the selected property is not upgraded beyond Track C's defensible relation."
                ),
            )
        )
    failed_checks = [
        name
        for name, accepted in (
            ("property_relation", c.property_relation_accepted),
            ("typed_inputs", c.typed_inputs_accepted),
            ("completed_false", c.completed_false_accepted),
            ("positive_control", c.positive_control_accepted),
            ("replay", c.replay_accepted),
            ("counterexample", c.counterexample_accepted),
        )
        if not accepted
    ]
    if failed_checks:
        records.append(
            ConflictRecord(
                conflict_id=f"predicate-gold-v1:{ledger_id}:execution-closure",
                opinion_ids=(
                    f"{b_reviewer}:{ledger_id}",
                    f"{c_reviewer}:{ledger_id}",
                ),
                disputed_fields=tuple(failed_checks),
                positions=(b.reason, c.reason),
                additional_evidence_refs=refs,
                resolution=(
                    "Pane5 does not promote a property whose semantic binding or execution closure failed independent review; "
                    f"the final disposition follows the source-backed Track C boundary: {c.basis}"
                ),
            )
        )
    high_risk_failed_checks = [
        name
        for name, accepted in (
            ("obligation", high_risk.obligation_accepted),
            ("property_relation", high_risk.property_relation_accepted),
            ("typed_inputs", high_risk.typed_inputs_accepted),
            ("execution_closure", high_risk.execution_closure_accepted),
        )
        if not accepted
    ]
    if high_risk_failed_checks:
        records.append(
            ConflictRecord(
                conflict_id=f"predicate-gold-v1:{ledger_id}:fourth-review-closure",
                opinion_ids=(
                    f"{c_reviewer}:{ledger_id}",
                    f"{high_risk_reviewer}:{ledger_id}",
                ),
                disputed_fields=tuple(high_risk_failed_checks),
                positions=(c.reason, high_risk.reason),
                additional_evidence_refs=refs,
                resolution=(
                    "Pane5 must resolve each failed fourth-review check from the cited author source, semantics, proposal, and execution evidence "
                    "before this draft can enter the active review manifest."
                ),
            )
        )
    if high_risk.conflicts:
        records.append(
            ConflictRecord(
                conflict_id=f"predicate-gold-v1:{ledger_id}:fourth-review-sensitivity",
                opinion_ids=(
                    f"{c_reviewer}:{ledger_id}",
                    f"{high_risk_reviewer}:{ledger_id}",
                ),
                disputed_fields=("retained_sensitivity",),
                positions=(
                    (
                        "Track C's selected boundary was "
                        f"{c.proposed_status.value}/{c.proposed_exactness_relation.value}: "
                        f"{c.reason}"
                    ),
                    *high_risk.conflicts,
                ),
                additional_evidence_refs=refs,
                resolution=(
                    "Pane5 retains these fourth-review sensitivities in the issue arbitration and must state whether each changes status, relation, or only confidence."
                ),
            )
        )
    return tuple(records)


def build_arbitration_batch(
    *,
    repo_root: Path,
    gold_root: Path,
    batch_id: str,
    a_paths: list[Path],
    b_paths: list[Path],
    c_paths: list[Path],
    high_risk_paths: list[Path],
    arbitrated_at: str,
) -> Pane5ArbitrationBatch:
    """Build one complete draft arbitration batch for matching four-track rows."""

    a_rows, a_locations = _rows(a_paths, TrackAProposalBatch)
    b_rows, b_locations = _rows(b_paths, TrackBProposalBatch)
    c_rows, c_locations = _rows(c_paths, TrackCReviewBatch)
    high_risk_rows, high_risk_locations = _rows(
        high_risk_paths, HighRiskReviewBatch
    )
    if not (
        set(a_rows)
        == set(b_rows)
        == set(c_rows)
        == set(high_risk_rows)
    ):
        raise ValueError(
            "A/B/C/high-risk arbitration coverage differs: "
            f"A={len(a_rows)}, B={len(b_rows)}, C={len(c_rows)}, "
            f"high-risk={len(high_risk_rows)}"
        )

    rows: list[Pane5ArbitrationRow] = []
    for ledger_id in sorted(a_rows):
        a = a_rows[ledger_id]
        b = b_rows[ledger_id]
        c = c_rows[ledger_id]
        high_risk = high_risk_rows[ledger_id]
        expected_bindings = {
            "Track A": (high_risk.track_a_opinion_sha256, a.proposal_sha256),
            "Track B": (high_risk.track_b_opinion_sha256, b.proposal_sha256),
            "Track C": (high_risk.track_c_opinion_sha256, c.opinion_sha256),
            "normalized obligation": (
                high_risk.normalized_obligation_sha256,
                c.normalized_obligation_sha256,
            ),
            "property proposal": (
                high_risk.property_proposal_sha256,
                c.property_proposal_sha256,
            ),
        }
        changed = [
            name for name, (observed, expected) in expected_bindings.items()
            if observed != expected
        ]
        if changed:
            raise ValueError(
                f"{ledger_id} fourth review does not bind active "
                + ", ".join(changed)
            )
        a_path, a_index = a_locations[ledger_id]
        b_path, b_index = b_locations[ledger_id]
        c_path, c_index = c_locations[ledger_id]
        high_risk_path, high_risk_index = high_risk_locations[ledger_id]
        a_reviewer = TrackAProposalBatch.model_validate_json(
            a_path.read_text()
        ).reviewer_id
        b_reviewer = TrackBProposalBatch.model_validate_json(
            b_path.read_text()
        ).reviewer_id
        c_reviewer = TrackCReviewBatch.model_validate_json(
            c_path.read_text()
        ).reviewer_id
        high_risk_reviewer = HighRiskReviewBatch.model_validate_json(
            high_risk_path.read_text()
        ).reviewer_id
        if len({a_reviewer, b_reviewer, c_reviewer, high_risk_reviewer}) != 4:
            raise ValueError(
                f"{ledger_id} requires four distinct review identities"
            )
        pair_path = gold_root / "review" / "input_packets" / "pairs" / f"{ledger_id.split('-')[1]}.json"
        refs = (
            _repo_ref(repo_root, pair_path, pointer="/ledger_items", element=f"{ledger_id} blind source packet"),
            _repo_ref(repo_root, a_path, pointer=f"/rows/{a_index}", element=f"{ledger_id} Track A opinion"),
            _repo_ref(repo_root, b_path, pointer=f"/rows/{b_index}", element=f"{ledger_id} Track B proposal"),
            _repo_ref(repo_root, c_path, pointer=f"/rows/{c_index}", element=f"{ledger_id} Track C opinion"),
            _repo_ref(
                repo_root,
                high_risk_path,
                pointer=f"/rows/{high_risk_index}",
                element=f"{ledger_id} independent fourth opinion",
            ),
        )
        conflicts = _conflicts(
            ledger_id=ledger_id,
            a=a,
            b=b,
            c=c,
            high_risk=high_risk,
            refs=refs,
            a_reviewer=a_reviewer,
            b_reviewer=b_reviewer,
            c_reviewer=c_reviewer,
            high_risk_reviewer=high_risk_reviewer,
        )
        retained = tuple(
            reading.reading
            for reading in a.alternative_readings
            if reading.source_compatible
            and reading.disposition in {"ADOPTED", "RETAINED_SENSITIVITY"}
        )
        sensitivity = tuple(
            dict.fromkeys(
                (*retained, *b.capability_gaps, *c.conflicts, *high_risk.conflicts)
            )
        )
        input_sha256 = canonical_sha256(
            {
                "track_a": a.proposal_sha256,
                "track_b": b.proposal_sha256,
                "track_c": c.opinion_sha256,
                "high_risk": high_risk.opinion_sha256,
                "packet": c.input_packet_sha256,
            }
        )
        arbitration = ArbitrationRecord(
            arbitration_id=f"predicate-gold-v1:{ledger_id}",
            adjudicator_id="pane5:manual-supervised-adjudicator",
            input_sha256=input_sha256,
            final_status=c.proposed_status,
            final_exactness_relation=c.proposed_exactness_relation,
            reason=(
                f"Pane5 draft starts from Track C's {c.proposed_status.value}/{c.proposed_exactness_relation.value} proposal "
                "and requires issue-specific confirmation against the fourth opinion. "
                f"Track C: {c.reason} Fourth review: {high_risk.reason}"
            ),
            basis=(
                f"Track A source basis: {a.basis} Track B property basis: {b.basis} "
                f"Track C execution/semantic basis: {c.basis} "
                f"Fourth-review basis: {high_risk.basis}"
            ),
            source_refs=refs,
            sensitivity=sensitivity,
            arbitrated_at=arbitrated_at,
        )
        unsigned = {
            "ledger_id": ledger_id,
            "track_a_opinion_sha256": a.proposal_sha256,
            "track_b_opinion_sha256": b.proposal_sha256,
            "track_c_opinion_sha256": c.opinion_sha256,
            "high_risk_opinion_sha256": high_risk.opinion_sha256,
            "conflicts": [item.model_dump(mode="json") for item in conflicts],
            "arbitration": arbitration.model_dump(mode="json"),
        }
        rows.append(Pane5ArbitrationRow(**unsigned, row_sha256=canonical_sha256(unsigned)))

    unsigned_batch = {
        "schema_version": ARBITRATION_SCHEMA_VERSION,
        "batch_id": batch_id,
        "pair_ids": sorted({ledger_id.split("-")[1] for ledger_id in a_rows}),
        "rows": [row.model_dump(mode="json") for row in rows],
        "arbitrated_at": arbitrated_at,
    }
    return Pane5ArbitrationBatch(
        **unsigned_batch,
        batch_sha256=canonical_sha256(unsigned_batch),
    )


def main(argv: list[str] | None = None) -> int:
    """Build and validate one pane5 arbitration batch."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--gold-root", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--track-a", action="append", type=Path, required=True)
    parser.add_argument("--track-b", action="append", type=Path, required=True)
    parser.add_argument("--track-c", action="append", type=Path, required=True)
    parser.add_argument("--high-risk", action="append", type=Path, required=True)
    parser.add_argument("--arbitrated-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    batch = build_arbitration_batch(
        repo_root=args.repo_root.resolve(),
        gold_root=args.gold_root.resolve(),
        batch_id=args.batch_id,
        a_paths=[path.resolve() for path in args.track_a],
        b_paths=[path.resolve() for path in args.track_b],
        c_paths=[path.resolve() for path in args.track_c],
        high_risk_paths=[path.resolve() for path in args.high_risk],
        arbitrated_at=args.arbitrated_at,
    )
    write_json(args.output, batch.model_dump(mode="json"))
    Pane5ArbitrationBatch.model_validate_json(args.output.read_text(encoding="utf-8"))
    print(f"wrote {args.output} ({len(batch.rows)} rows, {batch.batch_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
