"""Create a hash-sealed Track A view for an explicit pair subset."""

from __future__ import annotations

import argparse
from pathlib import Path

from paper_stm_evaluation.predicate_gold import canonical_sha256, write_json
from paper_stm_evaluation.predicate_gold_review import (
    TRACK_A_SCHEMA_VERSION,
    TrackAProposalBatch,
)


def slice_track_a_batch(
    source: TrackAProposalBatch,
    *,
    batch_id: str,
    excluded_pair_ids: set[str],
) -> TrackAProposalBatch:
    """Retain rows outside the excluded pairs without changing row payloads."""

    rows = tuple(
        row
        for row in source.rows
        if row.ledger_id.split("-")[1] not in excluded_pair_ids
    )
    if not rows:
        raise ValueError("Track A slice cannot be empty")
    pair_ids = tuple(sorted({row.ledger_id.split("-")[1] for row in rows}))
    unsigned = {
        "schema_version": TRACK_A_SCHEMA_VERSION,
        "batch_id": batch_id,
        "reviewer_id": source.reviewer_id,
        "input_manifest_sha256": source.input_manifest_sha256,
        "pair_ids": pair_ids,
        "rows": [row.model_dump(mode="json") for row in rows],
        "submitted_at": source.submitted_at,
    }
    return TrackAProposalBatch(**unsigned, batch_sha256=canonical_sha256(unsigned))


def main(argv: list[str] | None = None) -> int:
    """Write and validate one Track A subset view."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--exclude-pair", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    source = TrackAProposalBatch.model_validate_json(
        args.input.read_text(encoding="utf-8")
    )
    result = slice_track_a_batch(
        source,
        batch_id=args.batch_id,
        excluded_pair_ids=set(args.exclude_pair),
    )
    write_json(args.output, result.model_dump(mode="json"))
    TrackAProposalBatch.model_validate_json(args.output.read_text(encoding="utf-8"))
    print(f"wrote {args.output} ({len(result.rows)} rows, {result.batch_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
