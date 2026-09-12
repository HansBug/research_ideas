"""Freeze pair-0000 source-static proxy requests before their execution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paper_stm_evaluation.predicate_gold import (
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import TrackBProposalBatch
from paper_stm_evaluation.predicate_gold_static_oracle import (
    ArtifactRole,
    StaticOracleId,
    StaticOracleRequest,
)

CREATED_AT = "2026-08-30T20:20:00Z"
ISSUES = {
    "EIS-0000-01": {
        "property_id": "eis0000-01-native-static-running-poweroff-consumers",
        "oracle_id": StaticOracleId.RUNNING_EVENT_ROOT_EXIT_CONSUMERS,
    },
    "EIS-0000-02": {
        "property_id": "eis0000-02-native-static-separated-condition-consumers",
        "oracle_id": StaticOracleId.SEPARATED_CONDITION_TAKEOVER_CONSUMERS,
    },
}


def _request(
    *,
    row: object,
    candidate: object,
    oracle_id: StaticOracleId,
    artifact_role: ArtifactRole,
    artifact_path: str,
    artifact_sha256: str,
) -> StaticOracleRequest:
    """Build one hash-sealed request from the selected blind proposal."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.static-oracle-request.v1",
        "request_id": f"{row.ledger_id.lower()}-{artifact_role.value.lower()}-{oracle_id.value.lower()}",
        "ledger_id": row.ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": row.proposal_sha256,
        "exactness_relation": "O_IMPLIES_P",
        "oracle_id": oracle_id,
        "artifact_role": artifact_role,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "typed_inputs": [item.model_dump(mode="json") for item in candidate.typed_inputs],
        "assumptions": list(candidate.assumptions),
        "expected_boolean_for_acceptance": artifact_role == ArtifactRole.POSITIVE_CONTROL,
        "created_at": CREATED_AT,
    }
    return StaticOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def build(repo_root: Path) -> dict[str, object]:
    """Validate Track B and save two defective/control request pairs."""

    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    track_b_path = gold_root / "review/pilot_independent/track_b_pair_0000.json"
    batch = TrackBProposalBatch.model_validate_json(track_b_path.read_text(encoding="utf-8"))
    source = paper_root / "selected_seed_examples/llms_emp_feedback_final_0000/model.fcstm"
    issue_manifests: list[dict[str, object]] = []
    for ledger_id, spec in ISSUES.items():
        row = next(item for item in batch.rows if item.ledger_id == ledger_id)
        candidate = next(item for item in row.candidate_properties if item.candidate_id == row.selected_candidate_id)
        if candidate.candidate_id != spec["property_id"] or candidate.exactness_relation.value != "O_IMPLIES_P":
            raise ValueError(f"{ledger_id} no longer selects the expected source-static sound proxy")
        if candidate.mode.value != "EVALUATION_ONLY_ORACLE" or candidate.predicate_ids:
            raise ValueError(f"{ledger_id} selected candidate is not an isolated evaluation-only oracle")
        control = gold_root / f"controls/{ledger_id}/minimal_repair.fcstm"
        requests = (
            _request(
                row=row,
                candidate=candidate,
                oracle_id=spec["oracle_id"],
                artifact_role=ArtifactRole.DEFECTIVE,
                artifact_path=source.relative_to(repo_root).as_posix(),
                artifact_sha256=sha256_path(source),
            ),
            _request(
                row=row,
                candidate=candidate,
                oracle_id=spec["oracle_id"],
                artifact_role=ArtifactRole.POSITIVE_CONTROL,
                artifact_path=control.relative_to(repo_root).as_posix(),
                artifact_sha256=sha256_path(control),
            ),
        )
        request_rows: list[dict[str, object]] = []
        for request in requests:
            role_dir = "defective" if request.artifact_role == ArtifactRole.DEFECTIVE else "positive_control"
            path = gold_root / f"receipts/{ledger_id}/{role_dir}/request.json"
            write_json(path, request.model_dump(mode="json"))
            request_rows.append(
                {
                    "artifact_role": request.artifact_role.value,
                    "path": path.relative_to(gold_root).as_posix(),
                    "sha256": sha256_path(path),
                    "request_sha256": request.request_sha256,
                }
            )
        unsigned_issue = {
            "ledger_id": ledger_id,
            "proposal_sha256": row.proposal_sha256,
            "selected_candidate_id": candidate.candidate_id,
            "oracle_id": spec["oracle_id"].value,
            "requests": request_rows,
        }
        issue_manifests.append({**unsigned_issue, "issue_manifest_sha256": canonical_sha256(unsigned_issue)})
    unsigned = {
        "schema_version": "paper1.predicate-gold.static-pilot-request-manifest.v1",
        "created_at": CREATED_AT,
        "track_b_path": track_b_path.relative_to(repo_root).as_posix(),
        "track_b_sha256": sha256_path(track_b_path),
        "execution_results_read": False,
        "same_issue_execution_results_existed": False,
        "v60_actual_visible": False,
        "issues": issue_manifests,
    }
    manifest = {**unsigned, "manifest_sha256": canonical_sha256(unsigned)}
    write_json(gold_root / "receipts/pair_0000_static_request_manifest.json", manifest)
    return manifest


def main() -> int:
    """CLI entry point for deterministic source-static request generation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.repo_root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
