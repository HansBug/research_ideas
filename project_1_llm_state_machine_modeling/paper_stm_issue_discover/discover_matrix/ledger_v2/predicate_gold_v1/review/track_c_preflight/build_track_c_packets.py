"""Build hash-bound final Track C packets from A/B proposals and semantic preflight."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    ExactnessRelation,
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
    role: str,
    path: Path,
    reason: str,
    pointer: str | None = None,
) -> TrackCInputArtifact:
    """Create one exact Track C artifact binding."""

    return TrackCInputArtifact(
        role=role,
        repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        reason=reason,
    )


def _row_index(rows: tuple[Any, ...], ledger_id: str) -> int:
    """Return the unique row index for one ledger ID."""

    matches = [index for index, row in enumerate(rows) if row.ledger_id == ledger_id]
    if len(matches) != 1:
        raise ValueError(f"expected one row for {ledger_id}, found {matches}")
    return matches[0]


def main() -> int:
    """Write issue-local packets and one sealed packet manifest."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--track-a", type=Path, required=True)
    parser.add_argument("--track-b", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = (
        repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    )
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    a_path = args.track_a.resolve()
    b_path = args.track_b.resolve()
    preflight_path = args.preflight.resolve()
    a_batch = TrackAProposalBatch.model_validate_json(
        a_path.read_text(encoding="utf-8")
    )
    b_batch = TrackBProposalBatch.model_validate_json(
        b_path.read_text(encoding="utf-8")
    )
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    inventory = json.loads((gold_root / "inventory.json").read_text(encoding="utf-8"))
    pair_inventory = {pair["pair_id"]: pair for pair in inventory["pairs"]}
    preflight_rows = {
        row["ledger_id"]: (index, row) for index, row in enumerate(preflight["rows"])
    }
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    a_rows = {row.ledger_id: row for row in a_batch.rows}
    if set(a_rows) != set(b_rows) or set(a_rows) != set(preflight_rows):
        raise ValueError("Track A/B/preflight ledger IDs differ")

    common_paths = (
        (
            "capability_audit",
            gold_root / "predicate_semantics_capability_audit.json",
            "Frozen 19-predicate semantics and issue-level capability boundaries.",
        ),
        (
            "gold_protocol",
            gold_root / "predicate_gold_protocol.md",
            "Exactness, execution and unsupported release rules.",
        ),
        (
            "frozen_registry",
            paper_root
            / "method/src/paper_stm_method/resources/predicate_registry.json",
            "Frozen registry semantics and planned-snapshot boundary.",
        ),
        (
            "source_static_backend",
            paper_root / "method/src/paper_stm_method/backends/source_static.py",
            "Exact frozen S1-S6 implementation used by accepted static queries.",
        ),
        (
            "topology_backend",
            paper_root / "method/src/paper_stm_method/backends/topology.py",
            "Guard-agnostic topology implementation checked for rejected G candidates.",
        ),
        (
            "typed_input_schema",
            paper_root / "method/src/paper_stm_method/compiler/inputs.py",
            "Frozen typed input contracts.",
        ),
        (
            "pyfcstm_model_api",
            repo_root / "pyfcstm/pyfcstm/model/model.py",
            "Native state, transition, owner and event object semantics.",
        ),
    )
    output_root = gold_root / "review/track_c_input" / args.batch_id
    packet_paths: list[str] = []
    packet_file_hashes: list[str] = []
    packet_payload_hashes: list[str] = []
    ledger_ids: list[str] = []

    for ledger_id in sorted(a_rows):
        pair_id = ledger_id.split("-")[1]
        source_packet_path = (
            gold_root / "review/input_packets/pairs" / f"{pair_id}.json"
        )
        source_packet = json.loads(source_packet_path.read_text(encoding="utf-8"))
        pair_record = pair_inventory[pair_id]
        a_row = a_rows[ledger_id]
        b_row = b_rows[ledger_id]
        preflight_index, preflight_row = preflight_rows[ledger_id]
        a_index = _row_index(a_batch.rows, ledger_id)
        b_index = _row_index(b_batch.rows, ledger_id)
        artifacts = [
            _artifact(
                repo_root=repo_root,
                role="blind_source_packet",
                path=source_packet_path,
                pointer=f"/ledger_items/{next(i for i, item in enumerate(source_packet['ledger_items']) if item['ledger_id'] == ledger_id)}",
                reason="Complete blind NL/source/ledger packet for this issue.",
            ),
            _artifact(
                repo_root=repo_root,
                role="author_nl",
                path=repo_root / source_packet["nl"]["repository_path"],
                reason="Complete author NL bytes.",
            ),
            _artifact(
                repo_root=repo_root,
                role="author_plantuml",
                path=repo_root / source_packet["plantuml"]["repository_path"],
                reason="Complete author PlantUML bytes.",
            ),
            _artifact(
                repo_root=repo_root,
                role="defective_fcstm",
                path=repo_root / pair_record["fcstm_path"],
                reason="Exact executable defective FCSTM bytes.",
            ),
            _artifact(
                repo_root=repo_root,
                role="track_a_opinion",
                path=a_path,
                pointer=f"/rows/{a_index}",
                reason="Blind source-first obligation proposal.",
            ),
            _artifact(
                repo_root=repo_root,
                role="track_b_proposal",
                path=b_path,
                pointer=f"/rows/{b_index}",
                reason="Blind pre-result property/input proposal.",
            ),
            _artifact(
                repo_root=repo_root,
                role="track_c_semantic_preflight",
                path=preflight_path,
                pointer=f"/rows/{preflight_index}",
                reason="Independent pre-result relation, binding and eligibility screen.",
            ),
        ]
        artifacts.extend(
            _artifact(repo_root=repo_root, role=role, path=path, reason=reason)
            for role, path, reason in common_paths
        )
        if preflight_row["execution_required"]:
            issue_root = gold_root / "receipts" / ledger_id
            artifacts.append(
                _artifact(
                    repo_root=repo_root,
                    role="corrected_pre_execution_proposal",
                    path=issue_root / "proposal.json",
                    reason="Relation-corrected property and inputs frozen before execution.",
                )
            )
            for index, path in enumerate(
                sorted(path for path in issue_root.rglob("*") if path.is_file())
            ):
                if path.name == "proposal.json":
                    continue
                artifacts.append(
                    _artifact(
                        repo_root=repo_root,
                        role=f"execution_artifact_{index:03d}",
                        path=path,
                        reason="Defective/control query, receipt, counterexample or semantic replay evidence.",
                    )
                )
            control_root = gold_root / "controls" / ledger_id
            for index, path in enumerate(
                sorted(path for path in control_root.rglob("*") if path.is_file())
            ):
                artifacts.append(
                    _artifact(
                        repo_root=repo_root,
                        role=f"positive_control_artifact_{index:03d}",
                        path=path,
                        reason="Precommitted positive-control bytes or provenance.",
                    )
                )

        selected_candidate = (
            preflight_row["selected_candidate_id"]
            or "UNSUPPORTED_NO_EXECUTABLE_PROPERTY"
        )
        unsigned = {
            "schema_version": "paper1.predicate-gold.track-c-input-packet.v1",
            "ledger_id": ledger_id,
            "pair_id": pair_id,
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "selected_candidate_id": selected_candidate,
            "proposed_exactness_relation": ExactnessRelation(
                preflight_row["accepted_relation"] or ExactnessRelation.UNRELATED.value
            ),
            "artifacts": [item.model_dump(mode="json") for item in artifacts],
            "prior_tracks_visible": True,
            "execution_results_visible": True,
            "v60_actual_visible": False,
            "created_at": args.created_at,
        }
        packet = TrackCInputPacket(**unsigned, packet_sha256=canonical_sha256(unsigned))
        output = output_root / f"{ledger_id}.json"
        write_json(output, packet.model_dump(mode="json"))
        TrackCInputPacket.model_validate_json(output.read_text(encoding="utf-8"))
        packet_paths.append(output.relative_to(gold_root).as_posix())
        packet_file_hashes.append(sha256_path(output))
        packet_payload_hashes.append(packet.packet_sha256)
        ledger_ids.append(ledger_id)

    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.track-c-input-manifest.v1",
        "batch_id": args.batch_id,
        "packet_paths": packet_paths,
        "packet_file_sha256": packet_file_hashes,
        "packet_payload_sha256": packet_payload_hashes,
        "ledger_ids": ledger_ids,
        "created_at": args.created_at,
        "notes": [
            "Track C sees frozen A/B proposals and preflight; v60 actual predicate/input output remains excluded.",
            "execution_results_visible=true means the packet may explicitly show no execution after semantic preflight rejection; it never implies every row was run.",
            "Executed rows include corrected proposal, defective/control receipts, counterexamples and replays; rejected rows retain source/capability evidence without fabricated receipts.",
        ],
    }
    manifest = TrackCInputManifest(
        **unsigned_manifest, manifest_sha256=canonical_sha256(unsigned_manifest)
    )
    output = output_root / "manifest.json"
    write_json(output, manifest.model_dump(mode="json"))
    TrackCInputManifest.model_validate_json(output.read_text(encoding="utf-8"))
    print(f"wrote {output} ({len(ledger_ids)} packets, {manifest.manifest_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
