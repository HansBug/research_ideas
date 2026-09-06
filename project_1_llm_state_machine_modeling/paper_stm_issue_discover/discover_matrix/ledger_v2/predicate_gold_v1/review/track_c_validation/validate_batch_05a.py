"""Validate batch-05a portable Track C artifacts without provider calls."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pyfcstm.model import load_state_machine_from_text

from paper_stm_evaluation.predicate_gold import canonical_sha256, sha256_path, write_json
from paper_stm_evaluation.predicate_gold_composite import CompositeExecutionReceipt, CompositeExecutionRequest, CompositeReplayReceipt
from paper_stm_evaluation.predicate_gold_oracle import NativeOracleReceipt, NativeOracleReplayReceipt, NativeOracleRequest
from paper_stm_evaluation.predicate_gold_relation_oracle import RelationOracleReceipt, RelationOracleRequest, RelationReplayReceipt
from paper_stm_evaluation.predicate_gold_review import TrackAProposalBatch, TrackBProposalBatch, TrackCInputManifest, TrackCInputPacket, TrackCReviewBatch
from paper_stm_evaluation.predicate_gold_static_oracle import StaticOracleReceipt, StaticOracleReplayReceipt, StaticOracleRequest


def _repo_root() -> Path:
    return next(parent for parent in Path(__file__).resolve().parents if (parent / "pyfcstm").is_dir() and (parent / "project_1_llm_state_machine_modeling").is_dir())


def main() -> int:
    repo = _repo_root()
    gold = repo / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1"
    a = TrackAProposalBatch.model_validate_json((gold / "review/track_a_independent/batch_05a.json").read_text(encoding="utf-8"))
    b = TrackBProposalBatch.model_validate_json((gold / "review/track_b_independent/batch_05a.json").read_text(encoding="utf-8"))
    preflight_path = gold / "review/track_c_preflight/batch_05a.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    manifest_path = gold / "review/track_c_input/batch_05a_portable/manifest.json"
    manifest = TrackCInputManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    review_path = gold / "review/track_c_independent/batch_05a_portable.json"
    review = TrackCReviewBatch.model_validate_json(review_path.read_text(encoding="utf-8"))

    for row in preflight["rows"]:
        assert row["audit_sha256"] == canonical_sha256({key: value for key, value in row.items() if key != "audit_sha256"})
    assert preflight["batch_sha256"] == canonical_sha256({key: value for key, value in preflight.items() if key != "batch_sha256"})

    expected_ids = {row.ledger_id for row in a.rows}
    assert expected_ids == {row.ledger_id for row in b.rows} == set(manifest.ledger_ids) == {row.ledger_id for row in review.rows}
    assert len(expected_ids) == 24
    packet_artifacts = 0
    for packet_rel, file_hash, payload_hash in zip(manifest.packet_paths, manifest.packet_file_sha256, manifest.packet_payload_sha256, strict=True):
        packet_path = gold / packet_rel
        assert sha256_path(packet_path) == file_hash
        packet = TrackCInputPacket.model_validate_json(packet_path.read_text(encoding="utf-8"))
        assert packet.packet_sha256 == payload_hash
        assert packet.v60_actual_visible is False and len(packet.artifacts) >= 10
        for artifact in packet.artifacts:
            path = repo / artifact.repository_path
            assert path.is_file() and sha256_path(path) == artifact.sha256
            packet_artifacts += 1

    request_manifest = json.loads((gold / "receipts/batch_05a_request_manifest.json").read_text(encoding="utf-8"))
    models: dict[str, tuple[Any, Any, Any]] = {
        "relation": (RelationOracleRequest, RelationOracleReceipt, RelationReplayReceipt),
        "static": (StaticOracleRequest, StaticOracleReceipt, StaticOracleReplayReceipt),
        "native": (NativeOracleRequest, NativeOracleReceipt, NativeOracleReplayReceipt),
        "composite": (CompositeExecutionRequest, CompositeExecutionReceipt, CompositeReplayReceipt),
    }
    role_receipts = defective_false = control_true = replay_match = portable = 0
    for item in request_manifest["rows"]:
        control = gold / item["control_path"]
        assert sha256_path(control) == item["control_sha256"]
        load_state_machine_from_text(control.read_text(encoding="utf-8"))
        provenance_path = control.parent / "control_provenance.json"
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        assert provenance["provenance_sha256"] == canonical_sha256({key: value for key, value in provenance.items() if key != "provenance_sha256"})
        for role in item["roles"]:
            request_model, receipt_model, replay_model = models[role["runner_kind"]]
            request_path = gold / role["request_path"]
            request_model.model_validate_json(request_path.read_text(encoding="utf-8"))
            base = request_path.parent
            receipt = receipt_model.model_validate_json((base / "receipt.json").read_text(encoding="utf-8"))
            replay = replay_model.model_validate_json((base / "replay/replay_audit.json").read_text(encoding="utf-8"))
            state = receipt.state.value if hasattr(receipt.state, "value") else receipt.state
            assert state == "COMPLETED_BOOLEAN"
            assert receipt.acceptance_match and replay.overall_match
            expected = role["role"] == "POSITIVE_CONTROL"
            assert receipt.verdict is expected
            assert "--repo-root" in receipt.command and receipt.command[receipt.command.index("--repo-root") + 1] == "."
            role_receipts += 1
            defective_false += int(not expected and receipt.verdict is False)
            control_true += int(expected and receipt.verdict is True)
            replay_match += int(replay.overall_match)
            portable += 1

    statuses: dict[str, int] = {}
    for row in review.rows:
        statuses[row.proposed_status.value] = statuses.get(row.proposed_status.value, 0) + 1
        assert row.v60_actual_visible is False and row.contamination_check == "PASS"
    assert statuses == {"EXACT_FALSE": 7, "COMPOSITE_EXACT_FALSE": 1, "SOUND_FALSE_PROXY": 8, "UNSUPPORTED_EXACT": 8}
    assert role_receipts == defective_false + control_true == replay_match == portable == 32

    unsigned = {
        "schema_version": "paper1.predicate-gold.track-c-self-validation.v1",
        "batch_id": "batch_05a_portable",
        "validated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "checks": {
            "track_a_b_pydantic": "PASS",
            "preflight_row_and_batch_hashes": "PASS",
            "track_c_packets_pydantic_and_artifact_hashes": "PASS",
            "track_c_review_pydantic": "PASS",
            "control_pyfcstm_parse_and_provenance_hashes": "PASS",
            "request_receipt_replay_pydantic": "PASS",
            "portable_repo_root_commands": "PASS",
            "v60_actual_visibility": "PASS_FALSE_FOR_ALL",
            "blocked_execution": 0,
        },
        "coverage": {
            "ledger_ids": len(expected_ids),
            "packets": len(manifest.ledger_ids),
            "packet_artifacts_checked": packet_artifacts,
            "executable_issues": len(request_manifest["rows"]),
            "role_receipts": role_receipts,
            "defective_completed_false": defective_false,
            "positive_control_completed_true": control_true,
            "semantic_replay_match": replay_match,
            "portable_commands": portable,
            "status_distribution": statuses,
        },
        "inputs": {
            "preflight_sha256": sha256_path(preflight_path),
            "packet_manifest_sha256": sha256_path(manifest_path),
            "review_batch_sha256": sha256_path(review_path),
        },
        "provider_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "full_experiment_reruns": 0,
    }
    output = gold / "review/track_c_validation/batch_05a_self_validation.json"
    write_json(output, {**unsigned, "validation_sha256": canonical_sha256(unsigned)})
    print(json.dumps(unsigned["coverage"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
