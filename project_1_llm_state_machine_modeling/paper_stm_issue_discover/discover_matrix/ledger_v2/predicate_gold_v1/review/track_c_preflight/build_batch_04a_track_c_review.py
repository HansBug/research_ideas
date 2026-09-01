"""Build the hash-bound portable Track C review for batch 04a."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    SourceRef,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCInputManifest,
    TrackCInputPacket,
    TrackCReviewBatch,
    TrackCReviewRow,
)


def _now() -> str:
    """Return the current UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _repo_root() -> Path:
    """Resolve the repository root without relying on checkout depth."""

    return next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "pyfcstm").is_dir()
        and (parent / "project_1_llm_state_machine_modeling").is_dir()
    )


def _ref(
    repo_root: Path,
    path: Path,
    *,
    pointer: str | None = None,
    element: str | None = None,
) -> SourceRef:
    """Bind one review claim to exact repository bytes."""

    return SourceRef(
        repository_path=path.relative_to(repo_root).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        line_start=None,
        line_end=None,
        model_element=element,
        excerpt=None,
    )


def _status(ledger_id: str, preflight_row: dict[str, Any]) -> str:
    """Derive the final status without consulting execution outcomes."""

    if not preflight_row["execution_required"]:
        return "UNSUPPORTED_EXACT"
    if preflight_row["accepted_relation"] == "O_IMPLIES_P":
        return "SOUND_FALSE_PROXY"
    if ledger_id == "DIFF-0019-05":
        return "COMPOSITE_EXACT_FALSE"
    return "EXACT_FALSE"


def _validate_execution(
    repo_root: Path,
    gold_root: Path,
    ledger_id: str,
) -> tuple[list[SourceRef], str]:
    """Validate both roles, portable commands, replay, and control provenance."""

    issue_root = gold_root / "receipts" / ledger_id
    proposal_path = issue_root / "proposal.json"
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    refs = [
        _ref(
            repo_root,
            proposal_path,
            pointer="/selected_candidate",
            element=ledger_id,
        )
    ]
    for role in ("defective", "positive_control"):
        receipt_path = issue_root / role / "receipt.json"
        replay_path = issue_root / role / "replay/replay_audit.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        replay = json.loads(replay_path.read_text(encoding="utf-8"))
        expected = role == "positive_control"
        if (
            receipt["state"] != "COMPLETED_BOOLEAN"
            or receipt["verdict"] is not expected
            or not receipt["acceptance_match"]
        ):
            raise ValueError(f"{ledger_id} {role} result is not closed")
        if not replay["overall_match"]:
            raise ValueError(f"{ledger_id} {role} replay mismatch")
        command = receipt["command"]
        if "--repo-root" not in command:
            raise ValueError(f"{ledger_id} {role} command lacks --repo-root")
        if command[command.index("--repo-root") + 1] != ".":
            raise ValueError(f"{ledger_id} {role} command is not portable")
        refs.extend(
            (
                _ref(
                    repo_root,
                    receipt_path,
                    pointer="/verdict",
                    element=ledger_id,
                ),
                _ref(
                    repo_root,
                    replay_path,
                    pointer="/overall_match",
                    element=ledger_id,
                ),
            )
        )
    control_path = gold_root / f"controls/{ledger_id}/control_provenance.json"
    refs.append(_ref(repo_root, control_path, element=ledger_id))
    return refs, proposal["proposal_sha256"]


def main() -> int:
    """Build and validate all 22 final Track C review rows."""

    repo_root = _repo_root()
    paper_root = (
        repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    )
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    a_path = gold_root / "review/track_a_independent/batch_04a.json"
    b_path = gold_root / "review/track_b_independent/batch_04a.json"
    preflight_path = gold_root / "review/track_c_preflight/batch_04a.json"
    manifest_path = (
        gold_root / "review/track_c_input/batch_04a_portable/manifest.json"
    )
    a_batch = TrackAProposalBatch.model_validate_json(
        a_path.read_text(encoding="utf-8")
    )
    b_batch = TrackBProposalBatch.model_validate_json(
        b_path.read_text(encoding="utf-8")
    )
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    manifest = TrackCInputManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    a_rows = {
        row.ledger_id: (index, row) for index, row in enumerate(a_batch.rows)
    }
    b_rows = {
        row.ledger_id: (index, row) for index, row in enumerate(b_batch.rows)
    }
    preflight_rows = {
        row["ledger_id"]: (index, row)
        for index, row in enumerate(preflight["rows"])
    }
    packet_by_id = dict(zip(manifest.ledger_ids, manifest.packet_paths, strict=True))
    identities = (set(a_rows), set(b_rows), set(preflight_rows), set(packet_by_id))
    if len({frozenset(items) for items in identities}) != 1:
        raise ValueError("A/B/preflight/packet identity mismatch")

    reviewed_at = _now()
    rows: list[TrackCReviewRow] = []
    for ledger_id in sorted(a_rows):
        a_index, a_row = a_rows[ledger_id]
        b_index, b_row = b_rows[ledger_id]
        preflight_index, preflight_row = preflight_rows[ledger_id]
        packet_path = gold_root / packet_by_id[ledger_id]
        packet = TrackCInputPacket.model_validate_json(
            packet_path.read_text(encoding="utf-8")
        )
        executable = preflight_row["execution_required"]
        source_packet_path = (
            gold_root
            / f"review/input_packets/pairs/{ledger_id.split('-')[1]}.json"
        )
        refs = [
            _ref(repo_root, source_packet_path, element=ledger_id),
            _ref(
                repo_root,
                a_path,
                pointer=f"/rows/{a_index}",
                element=ledger_id,
            ),
            _ref(
                repo_root,
                b_path,
                pointer=f"/rows/{b_index}",
                element=ledger_id,
            ),
            _ref(
                repo_root,
                preflight_path,
                pointer=f"/rows/{preflight_index}",
                element=ledger_id,
            ),
            _ref(repo_root, packet_path, element=ledger_id),
        ]
        if executable:
            execution_refs, property_hash = _validate_execution(
                repo_root, gold_root, ledger_id
            )
            refs.extend(execution_refs)
            reason = (
                preflight_row["implication_analysis"]["reason"]
                + " The defective query completed false, the precommitted "
                "minimal-repair control completed true, and both semantic replays "
                "matched. These results close execution and binding only; they do "
                "not strengthen the preflight O/P relation."
            )
            basis = (
                "Hash-bound source packet, Track A/B/preflight, corrected "
                "pre-execution proposal, defective/control receipts, persisted "
                "native observations or counterexample, control provenance, and "
                "semantic replay audits."
            )
        else:
            property_hash = b_row.proposal_sha256
            reason = (
                preflight_row["implication_analysis"]["reason"]
                + " Track C did not manufacture missing events, states, phases, "
                "variables, domains, bounds, or controls; the disposition is "
                "unsupported exactness rather than blocked execution."
            )
            basis = (
                "Hash-bound source packet, independent Track A/B proposals, "
                "semantic preflight, capability audit, frozen backend contracts, "
                "and explicit missing-information or implication-gap analysis."
            )
        conflicts = tuple(preflight_row["conflicts"])
        unsigned = {
            "ledger_id": ledger_id,
            "input_packet_sha256": packet.packet_sha256,
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "normalized_obligation_sha256": preflight_row[
                "normalized_obligation_sha256"
            ],
            "property_proposal_sha256": property_hash,
            "proposed_status": _status(ledger_id, preflight_row),
            "proposed_exactness_relation": (
                preflight_row["accepted_relation"] or "UNRELATED"
            ),
            "obligation_accepted": True,
            "property_relation_accepted": executable,
            "typed_inputs_accepted": executable,
            "completed_false_accepted": executable,
            "positive_control_accepted": executable,
            "replay_accepted": executable,
            "counterexample_accepted": executable,
            "vacuity_check": "PASS" if executable else "NOT_APPLICABLE",
            "contamination_check": "PASS",
            "conflicts": conflicts,
            "reason": reason,
            "basis": basis,
            "source_refs": [item.model_dump(mode="json") for item in refs],
            "prior_tracks_visible": True,
            "v60_actual_visible": False,
            "confidence": "MEDIUM" if conflicts else "HIGH",
            "reviewed_at": reviewed_at,
        }
        rows.append(
            TrackCReviewRow(
                **unsigned,
                opinion_sha256=canonical_sha256(unsigned),
            )
        )

    unsigned_batch = {
        "schema_version": "paper1.predicate-gold.track-c-execution-review.v1",
        "batch_id": "batch_04a_portable",
        "reviewer_id": "track_c_independent_batch_04a",
        "input_manifest_path": manifest_path.relative_to(gold_root).as_posix(),
        "input_manifest_sha256": sha256_path(manifest_path),
        "pair_ids": ["0019", "0020", "0023", "0024", "0025", "0026", "0027"],
        "rows": [row.model_dump(mode="json") for row in rows],
        "submitted_at": reviewed_at,
    }
    batch = TrackCReviewBatch(
        **unsigned_batch,
        batch_sha256=canonical_sha256(unsigned_batch),
    )
    output = gold_root / "review/track_c_independent/batch_04a_portable.json"
    write_json(output, batch.model_dump(mode="json"))
    TrackCReviewBatch.model_validate_json(output.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for row in batch.rows:
        counts[row.proposed_status.value] = counts.get(row.proposed_status.value, 0) + 1
    print(
        f"wrote {output} ({len(rows)} rows, {counts}, {batch.batch_sha256})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
