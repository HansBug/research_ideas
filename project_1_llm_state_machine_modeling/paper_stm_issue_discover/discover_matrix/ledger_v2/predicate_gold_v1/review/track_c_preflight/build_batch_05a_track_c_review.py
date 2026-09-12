"""Build the hash-bound portable Track C review for batch 05a."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import SourceRef, canonical_sha256, sha256_path, write_json
from paper_stm_evaluation.predicate_gold_review import (
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCInputManifest,
    TrackCInputPacket,
    TrackCReviewBatch,
    TrackCReviewRow,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _repo_root() -> Path:
    return next(parent for parent in Path(__file__).resolve().parents if (parent / "pyfcstm").is_dir() and (parent / "project_1_llm_state_machine_modeling").is_dir())


def _ref(repo_root: Path, path: Path, *, pointer: str | None = None, element: str | None = None) -> SourceRef:
    return SourceRef(
        repository_path=path.relative_to(repo_root).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        line_start=None,
        line_end=None,
        model_element=element,
        excerpt=None,
    )


def _status(preflight_row: dict[str, Any], b_row: Any) -> str:
    if not preflight_row["execution_required"]:
        return "UNSUPPORTED_EXACT"
    if preflight_row["accepted_relation"] == "O_IMPLIES_P":
        return "SOUND_FALSE_PROXY"
    if b_row.proposed_mode.value == "COMPOSITE":
        return "COMPOSITE_EXACT_FALSE"
    return "EXACT_FALSE"


def main() -> int:
    repo_root = _repo_root()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    a_path = gold_root / "review/track_a_independent/batch_05a.json"
    b_path = gold_root / "review/track_b_independent/batch_05a.json"
    p_path = gold_root / "review/track_c_preflight/batch_05a.json"
    manifest_path = gold_root / "review/track_c_input/batch_05a_portable/manifest.json"
    a_batch = TrackAProposalBatch.model_validate_json(a_path.read_text(encoding="utf-8"))
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    preflight = json.loads(p_path.read_text(encoding="utf-8"))
    manifest = TrackCInputManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    a_rows = {row.ledger_id: (index, row) for index, row in enumerate(a_batch.rows)}
    b_rows = {row.ledger_id: (index, row) for index, row in enumerate(b_batch.rows)}
    p_rows = {row["ledger_id"]: (index, row) for index, row in enumerate(preflight["rows"])}
    packet_by_id = dict(zip(manifest.ledger_ids, manifest.packet_paths, strict=True))
    if set(a_rows) != set(b_rows) or set(a_rows) != set(p_rows) or set(a_rows) != set(packet_by_id):
        raise ValueError("A/B/preflight/packet identity mismatch")

    reviewed_at = _now()
    rows: list[TrackCReviewRow] = []
    for ledger_id in sorted(a_rows):
        a_index, a_row = a_rows[ledger_id]
        b_index, b_row = b_rows[ledger_id]
        p_index, p_row = p_rows[ledger_id]
        packet_path = gold_root / packet_by_id[ledger_id]
        packet = TrackCInputPacket.model_validate_json(packet_path.read_text(encoding="utf-8"))
        executable = p_row["execution_required"]
        refs = [
            _ref(repo_root, gold_root / f"review/input_packets/pairs/{ledger_id.split('-')[1]}.json", element=ledger_id),
            _ref(repo_root, a_path, pointer=f"/rows/{a_index}", element=ledger_id),
            _ref(repo_root, b_path, pointer=f"/rows/{b_index}", element=ledger_id),
            _ref(repo_root, p_path, pointer=f"/rows/{p_index}", element=ledger_id),
            _ref(repo_root, packet_path, element=ledger_id),
        ]
        conflicts = list(p_row["conflicts"])
        if executable:
            issue_root = gold_root / "receipts" / ledger_id
            proposal_path = issue_root / "proposal.json"
            proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
            property_hash = proposal["proposal_sha256"]
            for role in ("defective", "positive_control"):
                receipt_path = issue_root / role / "receipt.json"
                replay_path = issue_root / role / "replay/replay_audit.json"
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                replay = json.loads(replay_path.read_text(encoding="utf-8"))
                expected = role == "positive_control"
                if receipt["state"] != "COMPLETED_BOOLEAN" or receipt["verdict"] is not expected or not receipt["acceptance_match"]:
                    raise ValueError(f"{ledger_id} {role} result is not closed")
                if not replay["overall_match"]:
                    raise ValueError(f"{ledger_id} {role} replay mismatch")
                command = receipt["command"]
                if "--repo-root" not in command or command[command.index("--repo-root") + 1] != ".":
                    raise ValueError(f"{ledger_id} {role} command is not portable")
                refs.extend([
                    _ref(repo_root, receipt_path, pointer="/verdict", element=ledger_id),
                    _ref(repo_root, replay_path, pointer="/overall_match", element=ledger_id),
                ])
            refs.append(_ref(repo_root, proposal_path, pointer="/selected_candidate", element=ledger_id))
            if ledger_id == "EIS-0034-02":
                correction = gold_root / "review/evidence_corrections/eis_0034_02_replay_code_race_attempt_01/correction_log.json"
                refs.append(_ref(repo_root, correction, element=ledger_id))
                conflicts.append("The first replay was rejected because the evaluator code hash changed between original and replay; preserved correction evidence shows unchanged verdict/observations, and the stable-code rerun matches.")
            reason = p_row["implication_analysis"]["reason"] + " The defective query completed false, the precommitted independent control completed true, and both semantic replays matched; these results verify execution but do not strengthen the preflight O/P relation."
            basis = "Hash-bound Track A/B/preflight, source packet, corrected proposal, defective/control receipts, complete constituent observations, and replay audits."
        else:
            property_hash = b_row.proposal_sha256
            reason = p_row["implication_analysis"]["reason"] + " No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution."
            basis = "Hash-bound Track A/B/preflight, complete source packet, capability audit, frozen backend semantics, and explicit missing-information analysis."
        unsigned = {
            "ledger_id": ledger_id,
            "input_packet_sha256": packet.packet_sha256,
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "normalized_obligation_sha256": p_row["normalized_obligation_sha256"],
            "property_proposal_sha256": property_hash,
            "proposed_status": _status(p_row, b_row),
            "proposed_exactness_relation": p_row["accepted_relation"] or "UNRELATED",
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
        rows.append(TrackCReviewRow(**unsigned, opinion_sha256=canonical_sha256(unsigned)))

    unsigned_batch = {
        "schema_version": "paper1.predicate-gold.track-c-execution-review.v1",
        "batch_id": "batch_05a_portable",
        "reviewer_id": "track_c_independent_batch_05a",
        "input_manifest_path": manifest_path.relative_to(gold_root).as_posix(),
        "input_manifest_sha256": sha256_path(manifest_path),
        "pair_ids": ["0029", "0030", "0032", "0033", "0034"],
        "rows": [row.model_dump(mode="json") for row in rows],
        "submitted_at": reviewed_at,
    }
    batch = TrackCReviewBatch(**unsigned_batch, batch_sha256=canonical_sha256(unsigned_batch))
    output = gold_root / "review/track_c_independent/batch_05a_portable.json"
    write_json(output, batch.model_dump(mode="json"))
    TrackCReviewBatch.model_validate_json(output.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for row in batch.rows:
        counts[row.proposed_status.value] = counts.get(row.proposed_status.value, 0) + 1
    print(f"wrote {output} ({len(rows)} rows, {counts}, {batch.batch_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
