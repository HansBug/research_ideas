"""Validate batch-04a portable Track C artifacts without provider calls."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_execution import (
    PredicateExecutionRequest,
    PredicateGoldExecutionReceipt,
    PredicateReplayAudit,
)
from paper_stm_evaluation.predicate_gold_native_composite import (
    NativeCompositeReceipt,
    NativeCompositeReplayReceipt,
    NativeCompositeRequest,
)
from paper_stm_evaluation.predicate_gold_oracle import (
    NativeOracleReceipt,
    NativeOracleReplayReceipt,
    NativeOracleRequest,
)
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    RelationOracleReceipt,
    RelationOracleRequest,
    RelationReplayReceipt,
)
from paper_stm_evaluation.predicate_gold_review import (
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCInputManifest,
    TrackCInputPacket,
    TrackCReviewBatch,
)
from pyfcstm.model import load_state_machine_from_text


def _repo_root() -> Path:
    """Resolve the checkout root without assuming a fixed parent depth."""

    return next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "pyfcstm").is_dir()
        and (parent / "project_1_llm_state_machine_modeling").is_dir()
    )


def main() -> int:
    """Validate identities, hashes, contracts, controls, and execution closure."""

    repo = _repo_root()
    gold = (
        repo
        / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
        / "discover_matrix/ledger_v2/predicate_gold_v1"
    )
    a = TrackAProposalBatch.model_validate_json(
        (gold / "review/track_a_independent/batch_04a.json").read_text(
            encoding="utf-8"
        )
    )
    b = TrackBProposalBatch.model_validate_json(
        (gold / "review/track_b_independent/batch_04a.json").read_text(
            encoding="utf-8"
        )
    )
    preflight_path = gold / "review/track_c_preflight/batch_04a.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    manifest_path = gold / "review/track_c_input/batch_04a_portable/manifest.json"
    manifest = TrackCInputManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    review_path = gold / "review/track_c_independent/batch_04a_portable.json"
    review = TrackCReviewBatch.model_validate_json(
        review_path.read_text(encoding="utf-8")
    )

    for row in preflight["rows"]:
        assert row["audit_sha256"] == canonical_sha256(
            {key: value for key, value in row.items() if key != "audit_sha256"}
        )
    assert preflight["batch_sha256"] == canonical_sha256(
        {key: value for key, value in preflight.items() if key != "batch_sha256"}
    )

    expected_ids = {row.ledger_id for row in a.rows}
    assert expected_ids == {row.ledger_id for row in b.rows}
    assert expected_ids == set(manifest.ledger_ids)
    assert expected_ids == {row.ledger_id for row in review.rows}
    assert len(expected_ids) == 22

    packet_artifacts = 0
    minimum_packet_artifacts = 10_000
    for packet_rel, file_hash, payload_hash in zip(
        manifest.packet_paths,
        manifest.packet_file_sha256,
        manifest.packet_payload_sha256,
        strict=True,
    ):
        packet_path = gold / packet_rel
        assert sha256_path(packet_path) == file_hash
        packet = TrackCInputPacket.model_validate_json(
            packet_path.read_text(encoding="utf-8")
        )
        assert packet.packet_sha256 == payload_hash
        assert packet.v60_actual_visible is False
        assert len(packet.artifacts) >= 10
        minimum_packet_artifacts = min(minimum_packet_artifacts, len(packet.artifacts))
        for artifact in packet.artifacts:
            artifact_path = repo / artifact.repository_path
            assert artifact_path.is_file()
            actual_sha256 = sha256_path(artifact_path)
            if actual_sha256 != artifact.sha256:
                raise ValueError(
                    f"packet artifact hash drift: {artifact.repository_path}: "
                    f"expected {artifact.sha256}, got {actual_sha256}"
                )
            packet_artifacts += 1

    request_manifest_path = gold / "receipts/batch_04a_request_manifest.json"
    request_manifest = json.loads(
        request_manifest_path.read_text(encoding="utf-8")
    )
    assert request_manifest["manifest_sha256"] == canonical_sha256(
        {
            key: value
            for key, value in request_manifest.items()
            if key != "manifest_sha256"
        }
    )
    models: dict[str, tuple[Any, Any, Any]] = {
        "EVALUATION_ONLY_NATIVE_COMPOSITE": (
            NativeCompositeRequest,
            NativeCompositeReceipt,
            NativeCompositeReplayReceipt,
        ),
        "EVALUATION_ONLY_NATIVE_ORACLE": (
            NativeOracleRequest,
            NativeOracleReceipt,
            NativeOracleReplayReceipt,
        ),
        "EVALUATION_ONLY_RELATION": (
            RelationOracleRequest,
            RelationOracleReceipt,
            RelationReplayReceipt,
        ),
        "FROZEN_PREDICATE": (
            PredicateExecutionRequest,
            PredicateGoldExecutionReceipt,
            PredicateReplayAudit,
        ),
    }
    role_receipts = 0
    defective_false = 0
    control_true = 0
    replay_match = 0
    portable = 0
    for item in request_manifest["rows"]:
        proposal_path = gold / item["proposal_path"]
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        assert sha256_path(proposal_path) == item["proposal_file_sha256"]
        assert proposal["proposal_sha256"] == item["proposal_payload_sha256"]
        control_provenance_path = gold / item["control_provenance_path"]
        control_provenance = json.loads(
            control_provenance_path.read_text(encoding="utf-8")
        )
        assert control_provenance["provenance_sha256"] == canonical_sha256(
            {
                key: value
                for key, value in control_provenance.items()
                if key != "provenance_sha256"
            }
        )
        control_path = repo / control_provenance["control_artifact_path"]
        assert sha256_path(control_path) == control_provenance[
            "control_artifact_sha256"
        ]
        load_state_machine_from_text(control_path.read_text(encoding="utf-8"))
        for role in item["roles"]:
            request_model, receipt_model, replay_model = models[
                role["request_kind"]
            ]
            request_path = gold / role["request_path"]
            assert sha256_path(request_path) == role["request_file_sha256"]
            request = request_model.model_validate_json(
                request_path.read_text(encoding="utf-8")
            )
            assert request.request_sha256 == role["request_payload_sha256"]
            assert request.artifact_sha256 == role["artifact_sha256"]
            receipt_root = request_path.parent
            receipt = receipt_model.model_validate_json(
                (receipt_root / "receipt.json").read_text(encoding="utf-8")
            )
            replay = replay_model.model_validate_json(
                (receipt_root / "replay/replay_audit.json").read_text(
                    encoding="utf-8"
                )
            )
            state = receipt.state.value if hasattr(receipt.state, "value") else receipt.state
            assert state == "COMPLETED_BOOLEAN"
            assert receipt.acceptance_match
            assert replay.overall_match
            expected = request.artifact_role.value == "POSITIVE_CONTROL"
            assert receipt.verdict is expected
            assert "--repo-root" in receipt.command
            assert receipt.command[receipt.command.index("--repo-root") + 1] == "."
            role_receipts += 1
            defective_false += int(not expected and receipt.verdict is False)
            control_true += int(expected and receipt.verdict is True)
            replay_match += int(replay.overall_match)
            portable += 1

    statuses: dict[str, int] = {}
    for row in review.rows:
        statuses[row.proposed_status.value] = statuses.get(
            row.proposed_status.value, 0
        ) + 1
        assert row.v60_actual_visible is False
        assert row.contamination_check == "PASS"
    assert statuses == {
        "COMPOSITE_EXACT_FALSE": 1,
        "EXACT_FALSE": 3,
        "SOUND_FALSE_PROXY": 1,
        "UNSUPPORTED_EXACT": 17,
    }
    assert role_receipts == 10
    assert defective_false == control_true == 5
    assert replay_match == portable == 10

    unsigned = {
        "schema_version": "paper1.predicate-gold.track-c-self-validation.v1",
        "batch_id": "batch_04a_portable",
        "validated_at": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
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
            "minimum_artifacts_per_packet": minimum_packet_artifacts,
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
            "request_manifest_sha256": sha256_path(request_manifest_path),
        },
        "provider_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "full_experiment_reruns": 0,
    }
    output = gold / "review/track_c_validation/batch_04a_self_validation.json"
    write_json(
        output,
        {**unsigned, "validation_sha256": canonical_sha256(unsigned)},
    )
    print(json.dumps(unsigned["coverage"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
