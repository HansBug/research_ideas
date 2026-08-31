"""Build hash-bound post-execution Track C packets for the pair-0000 pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paper_stm_evaluation.predicate_gold import (
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCInputArtifact,
    TrackCInputManifest,
    TrackCInputPacket,
)


def _artifact(
    *,
    repo_root: Path,
    path: Path,
    role: str,
    reason: str,
    json_pointer: str | None = None,
) -> TrackCInputArtifact:
    """Hash one repository artifact intentionally visible to Track C."""

    return TrackCInputArtifact(
        role=role,
        repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(path),
        json_pointer=json_pointer,
        reason=reason,
    )


def build(
    repo_root: Path, *, batch_id: str, created_at: str
) -> TrackCInputManifest:
    """Write three issue packets and one aligned manifest."""

    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    review_root = gold_root / "review"
    track_a_path = review_root / "pilot_independent/track_a_pair_0000.json"
    track_b_path = review_root / "pilot_independent/track_b_pair_0000.json"
    track_a = TrackAProposalBatch.model_validate_json(track_a_path.read_text(encoding="utf-8"))
    track_b = TrackBProposalBatch.model_validate_json(track_b_path.read_text(encoding="utf-8"))
    output_root = review_root / "track_c_input" / batch_id
    packet_paths: list[str] = []
    packet_file_hashes: list[str] = []
    packet_payload_hashes: list[str] = []
    ledger_ids: list[str] = []
    common_paths = (
        (gold_root / "review/input_packets/pairs/0000.json", "blind_source_packet", "Author NL, PlantUML, ledger, provenance, and FCSTM source packet used by A/B."),
        (gold_root / "predicate_semantics_capability_audit.json", "capability_audit", "Frozen source-level capability boundaries for the 19 predicates."),
        (repo_root / "pyfcstm/pyfcstm/model/model.py", "pyfcstm_model_semantics", "Native State, Event, Transition, hierarchy, and initial-transition semantics."),
    )
    for ledger_id in ("EIS-0000-01", "EIS-0000-02", "INS-0000-04"):
        a_index, a_row = next((index, row) for index, row in enumerate(track_a.rows) if row.ledger_id == ledger_id)
        b_index, b_row = next((index, row) for index, row in enumerate(track_b.rows) if row.ledger_id == ledger_id)
        selected = next(candidate for candidate in b_row.candidate_properties if candidate.candidate_id == b_row.selected_candidate_id)
        artifacts = [
            _artifact(repo_root=repo_root, path=track_a_path, role="track_a_proposal", reason="Blind normalized-obligation proposal.", json_pointer=f"/rows/{a_index}"),
            _artifact(repo_root=repo_root, path=track_b_path, role="track_b_proposal", reason="Blind pre-execution candidate, typed-input, and O/P proposal.", json_pointer=f"/rows/{b_index}"),
            _artifact(
                repo_root=repo_root,
                path=paper_root / "selected_seed_examples/llms_emp_feedback_final_0000/model.fcstm",
                role="defective_fcstm",
                reason="Exact defective FCSTM bytes evaluated by the frozen request.",
            ),
        ]
        artifacts.extend(
            _artifact(repo_root=repo_root, path=path, role=role, reason=reason)
            for path, role, reason in common_paths
        )
        control_root = gold_root / f"controls/{ledger_id}"
        artifacts.extend(
            (
                _artifact(repo_root=repo_root, path=control_root / "minimal_repair.fcstm", role="positive_control_fcstm", reason="Independently justified true-side artifact saved before same-issue execution."),
                _artifact(repo_root=repo_root, path=control_root / "control_provenance.json", role="positive_control_provenance", reason="Byte-level repair, contamination, and vacuity rationale."),
            )
        )
        if ledger_id == "INS-0000-04":
            code_paths = (
                paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_composite.py",
                paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_execution.py",
                paper_root / "method/src/paper_stm_method/backends/source_static.py",
                paper_root / "method/src/paper_stm_method/compiler/inputs.py",
            )
        else:
            code_paths = (
                paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_static_oracle.py",
                repo_root / "utils/stm_artifacts/fcstm_native_projection.py",
            )
        artifacts.extend(
            _artifact(
                repo_root=repo_root,
                path=path,
                role=f"execution_code:{path.name}",
                reason="Exact provider-free code bytes used by the request and receipt.",
            )
            for path in code_paths
        )
        receipt_root = gold_root / f"receipts/{ledger_id}"
        for path in sorted(item for item in receipt_root.rglob("*") if item.is_file()):
            relative = path.relative_to(receipt_root).as_posix()
            artifacts.append(
                _artifact(
                    repo_root=repo_root,
                    path=path,
                    role=f"execution_artifact:{relative}",
                    reason="Frozen defective/control query, raw receipt, normalized receipt, counterexample/trace payload, or replay audit.",
                )
            )
        unsigned = {
            "schema_version": "paper1.predicate-gold.track-c-input-packet.v1",
            "ledger_id": ledger_id,
            "pair_id": "0000",
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "selected_candidate_id": selected.candidate_id,
            "proposed_exactness_relation": selected.exactness_relation,
            "artifacts": [item.model_dump(mode="json") for item in artifacts],
            "prior_tracks_visible": True,
            "execution_results_visible": True,
            "v60_actual_visible": False,
            "created_at": created_at,
        }
        packet = TrackCInputPacket(**unsigned, packet_sha256=canonical_sha256(unsigned))
        path = output_root / f"{ledger_id}.json"
        write_json(path, packet.model_dump(mode="json"))
        packet_paths.append(path.relative_to(gold_root).as_posix())
        packet_file_hashes.append(sha256_path(path))
        packet_payload_hashes.append(packet.packet_sha256)
        ledger_ids.append(ledger_id)
    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.track-c-input-manifest.v1",
        "batch_id": batch_id,
        "packet_paths": packet_paths,
        "packet_file_sha256": packet_file_hashes,
        "packet_payload_sha256": packet_payload_hashes,
        "ledger_ids": ledger_ids,
        "created_at": created_at,
        "notes": [
            "Track C sees frozen A/B proposals only after their hashes and all execution requests were frozen.",
            "Track C sees complete defective/control/replay artifacts and must not infer exactness from false alone.",
            "v60 actual predicate IDs, inputs, reports, and outcomes are absent from every packet.",
        ],
    }
    manifest = TrackCInputManifest(
        **unsigned_manifest,
        manifest_sha256=canonical_sha256(unsigned_manifest),
    )
    write_json(output_root / "manifest.json", manifest.model_dump(mode="json"))
    return manifest


def main() -> int:
    """CLI entry point for deterministic Track C packet generation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            build(
                args.repo_root.resolve(),
                batch_id=args.batch_id,
                created_at=args.created_at,
            ).model_dump(mode="json"),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
