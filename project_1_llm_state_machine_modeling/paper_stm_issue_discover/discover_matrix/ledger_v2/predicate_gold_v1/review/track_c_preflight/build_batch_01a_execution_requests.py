"""Freeze corrected proposals and executable proxy requests for batch 01a."""

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
from paper_stm_evaluation.predicate_gold_composite import CompositeExecutionRequest
from paper_stm_evaluation.predicate_gold_execution import (
    ArtifactRole,
    PredicateExecutionRequest,
    RelationScope,
)
from paper_stm_evaluation.predicate_gold_review import TrackBProposalBatch


def _proposal(
    *,
    ledger_id: str,
    b_row: Any,
    preflight_row: dict[str, Any],
    candidate: Any,
    created_at: str,
) -> tuple[dict[str, Any], str]:
    """Build the post-preflight, pre-result property proposal payload."""

    candidate_payload = candidate.model_dump(mode="json")
    candidate_payload["exactness_relation"] = ExactnessRelation.O_IMPLIES_P.value
    candidate_payload["semantic_gaps"] = [
        *candidate_payload["semantic_gaps"],
        preflight_row["relation_reason"],
    ]
    candidate_payload["reason"] = (
        candidate_payload["reason"]
        + " Track C preflight corrected the relation to O_IMPLIES_P before execution; this query is a sound proxy, not exact gold."
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.corrected-execution-proposal.v1",
        "ledger_id": ledger_id,
        "track_b_proposal_sha256": b_row.proposal_sha256,
        "track_c_preflight_row_sha256": preflight_row["row_sha256"],
        "selected_candidate": candidate_payload,
        "final_pre_execution_relation": ExactnessRelation.O_IMPLIES_P.value,
        "execution_required": True,
        "v60_actual_visible": False,
        "created_at": created_at,
    }
    digest = canonical_sha256(unsigned)
    return {**unsigned, "proposal_sha256": digest}, digest


def _single_request(
    *,
    request_id: str,
    ledger_id: str,
    property_id: str,
    proposal_sha256: str,
    predicate_id: str,
    role: ArtifactRole,
    artifact_path: str,
    artifact_sha256: str,
    typed_inputs: tuple[Any, ...],
    expected: bool,
    created_at: str,
    relation_scope: RelationScope = RelationScope.THIS_PROPERTY,
) -> PredicateExecutionRequest:
    """Build one sealed frozen-predicate request."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        "request_id": request_id,
        "ledger_id": ledger_id,
        "property_id": property_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": ExactnessRelation.O_IMPLIES_P,
        "relation_scope": relation_scope,
        "predicate_id": predicate_id,
        "artifact_role": role,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": [
            "Track C preflight accepted only O_IMPLIES_P; execution cannot upgrade this property to exact gold.",
            "The query and positive-control artifact were hash-frozen before same-issue execution.",
        ],
        "expected_boolean_for_acceptance": expected,
        "created_at": created_at,
    }
    return PredicateExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def _not_request(
    *,
    request_id: str,
    child: PredicateExecutionRequest,
    expected: bool,
    created_at: str,
) -> CompositeExecutionRequest:
    """Build one transparent unary NOT parent around an S1 membership query."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.composite-request.v1",
        "request_id": request_id,
        "ledger_id": child.ledger_id,
        "property_id": child.property_id,
        "property_proposal_sha256": child.property_proposal_sha256,
        "exactness_relation": ExactnessRelation.O_IMPLIES_P,
        "operator": "NOT",
        "no_short_circuit": True,
        "artifact_role": child.artifact_role,
        "artifact_path": child.artifact_path,
        "artifact_sha256": child.artifact_sha256,
        "constituents": [child.model_dump(mode="json")],
        "assumptions": [
            "The exact packet-attributed InvalidInitialtr_0002 identity is checked without name inference.",
            "NOT has exactly one fully executed S1 constituent; parent false means the sentinel exists.",
        ],
        "expected_boolean_for_acceptance": expected,
        "created_at": created_at,
    }
    return CompositeExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def main() -> int:
    """Write all batch-01a requests without executing them."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    b_batch = TrackBProposalBatch.model_validate_json((gold_root / "review/track_b_independent/batch_01a.json").read_text(encoding="utf-8"))
    preflight = json.loads(args.preflight.resolve().read_text(encoding="utf-8"))
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    preflight_rows = {row["ledger_id"]: row for row in preflight["rows"]}
    plans = {
        "EIS-0002-01": {
            "defective": paper_root / "selected_seed_examples/llms_emp_feedback_final_0002/model.fcstm",
            "control": gold_root / "controls/EIS-0002-01/minimal_repair.fcstm",
            "predicate_id": "S2",
            "composite": False,
        },
        "EIS-0004-01": {
            "defective": paper_root / "selected_seed_examples/llms_emp_feedback_final_0004/model.fcstm",
            "control": gold_root / "controls/EIS-0004-01/minimal_repair.fcstm",
            "predicate_id": "S1",
            "composite": True,
        },
    }
    manifest_rows: list[dict[str, Any]] = []

    for ledger_id, plan in plans.items():
        b_row = b_rows[ledger_id]
        preflight_row = preflight_rows[ledger_id]
        if preflight_row["execution_required"] is not True or preflight_row["accepted_relation"] != "O_IMPLIES_P":
            raise ValueError(f"{ledger_id} is not accepted for O_IMPLIES_P execution")
        candidate = next(item for item in b_row.candidate_properties if item.candidate_id == b_row.selected_candidate_id)
        proposal, proposal_sha256 = _proposal(
            ledger_id=ledger_id,
            b_row=b_row,
            preflight_row=preflight_row,
            candidate=candidate,
            created_at=args.created_at,
        )
        issue_root = gold_root / "receipts" / ledger_id
        write_json(issue_root / "proposal.json", proposal)
        role_outputs: list[dict[str, str]] = []
        for role_name, role, expected in (
            ("defective", ArtifactRole.DEFECTIVE, False),
            ("positive_control", ArtifactRole.POSITIVE_CONTROL, True),
        ):
            artifact = plan["defective"] if role == ArtifactRole.DEFECTIVE else plan["control"]
            relative = artifact.resolve().relative_to(repo_root).as_posix()
            root = issue_root / role_name
            if plan["composite"]:
                child = _single_request(
                    request_id=f"{ledger_id.lower()}-{role_name}-s1-sentinel-membership",
                    ledger_id=ledger_id,
                    property_id=candidate.candidate_id,
                    proposal_sha256=proposal_sha256,
                    predicate_id=plan["predicate_id"],
                    role=role,
                    artifact_path=relative,
                    artifact_sha256=sha256_path(artifact),
                    typed_inputs=candidate.typed_inputs,
                    expected=not expected,
                    created_at=args.created_at,
                    relation_scope=RelationScope.PARENT_COMPOSITE,
                )
                request = _not_request(
                    request_id=f"{ledger_id.lower()}-{role_name}-not-s1-sentinel",
                    child=child,
                    expected=expected,
                    created_at=args.created_at,
                )
            else:
                request = _single_request(
                    request_id=f"{ledger_id.lower()}-{role_name}-{plan['predicate_id'].lower()}",
                    ledger_id=ledger_id,
                    property_id=candidate.candidate_id,
                    proposal_sha256=proposal_sha256,
                    predicate_id=plan["predicate_id"],
                    role=role,
                    artifact_path=relative,
                    artifact_sha256=sha256_path(artifact),
                    typed_inputs=candidate.typed_inputs,
                    expected=expected,
                    created_at=args.created_at,
                )
            write_json(root / "request.json", request.model_dump(mode="json"))
            role_outputs.append(
                {
                    "artifact_sha256": sha256_path(artifact),
                    "request_path": (root / "request.json").relative_to(gold_root).as_posix(),
                    "request_file_sha256": sha256_path(root / "request.json"),
                    "request_payload_sha256": request.request_sha256,
                }
            )
        manifest_rows.append(
            {
                "ledger_id": ledger_id,
                "proposal_path": (issue_root / "proposal.json").relative_to(gold_root).as_posix(),
                "proposal_file_sha256": sha256_path(issue_root / "proposal.json"),
                "proposal_payload_sha256": proposal_sha256,
                "roles": role_outputs,
            }
        )
    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.execution-request-manifest.v1",
        "batch_id": "batch_01a",
        "track_c_preflight_batch_sha256": preflight["batch_sha256"],
        "rows": manifest_rows,
        "created_at": args.created_at,
        "no_execution_performed_by_builder": True,
    }
    manifest = {**unsigned_manifest, "manifest_sha256": canonical_sha256(unsigned_manifest)}
    output = gold_root / "receipts/batch_01a_request_manifest.json"
    write_json(output, manifest)
    print(f"wrote {output} ({len(manifest_rows)} issues, {manifest['manifest_sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
