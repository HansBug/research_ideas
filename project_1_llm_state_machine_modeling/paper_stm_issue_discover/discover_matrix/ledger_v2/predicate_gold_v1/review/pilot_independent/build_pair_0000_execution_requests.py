"""Freeze pair-0000 pilot requests before any predicate execution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paper_stm_evaluation.predicate_gold import (
    JsonType,
    TypedInput,
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

LEDGER_ID = "INS-0000-04"
PROPERTY_ID = "ins0000-04-composite-s3-s5-root-initial-carriers"
CREATED_AT = "2026-08-30T20:10:00Z"


def _selected_row(batch: TrackBProposalBatch) -> tuple[object, object]:
    """Return the hash-validated pilot row and selected composite candidate."""

    row = next(item for item in batch.rows if item.ledger_id == LEDGER_ID)
    candidate = next(item for item in row.candidate_properties if item.candidate_id == row.selected_candidate_id)
    if candidate.candidate_id != PROPERTY_ID or candidate.exactness_relation.value != "EQUIVALENT":
        raise ValueError("the frozen Track B selection is not the expected exact pilot composite")
    if candidate.mode.value != "COMPOSITE" or set(candidate.predicate_ids) != {"S3", "S5"}:
        raise ValueError("the frozen Track B selection does not contain the expected S3/S5 composite")
    return row, candidate


def _predicate_inputs(wrapper: TypedInput) -> tuple[str, tuple[TypedInput, ...]]:
    """Expand one pre-execution wrapper into the frozen predicate input fields."""

    value = wrapper.normalized_value
    if not isinstance(value, dict):
        raise TypeError("the Track B composite wrapper must contain one object")
    predicate_id = str(wrapper.value["predicate_id"]) if isinstance(wrapper.value, dict) else ""
    if predicate_id not in {"S3", "S5"}:
        raise ValueError("the pilot composite admits only S3 and S5 constituents")
    value_name = "triggers" if predicate_id == "S3" else "guard"
    typed = (
        TypedInput(
            field_name="transition",
            json_type=JsonType.STRING,
            value=value["transition"],
            normalized_value=value["transition"],
            provenance_kind=wrapper.provenance_kind,
            source_ref=wrapper.source_ref,
            stable_object_id=wrapper.stable_object_id,
            alias_resolution=wrapper.alias_resolution,
            reason=f"Expanded from frozen Track B input {wrapper.field_name}; the exact native carrier identity is unchanged.",
        ),
        TypedInput(
            field_name=value_name,
            json_type=JsonType.ARRAY if predicate_id == "S3" else JsonType.STRING,
            value=value[value_name],
            normalized_value=value[value_name],
            provenance_kind=wrapper.provenance_kind,
            source_ref=wrapper.source_ref,
            stable_object_id=None,
            alias_resolution=None,
            reason=f"Expanded from frozen Track B input {wrapper.field_name}; the deliberate empty {value_name} value is unchanged.",
        ),
    )
    return predicate_id, typed


def _child_request(
    *,
    wrapper: TypedInput,
    proposal_sha256: str,
    artifact_role: ArtifactRole,
    artifact_path: str,
    artifact_sha256: str,
    expected: bool,
) -> PredicateExecutionRequest:
    """Build one hash-sealed child query without consulting execution output."""

    predicate_id, typed_inputs = _predicate_inputs(wrapper)
    request_id = f"ins0000-04-{artifact_role.value.lower()}-{wrapper.stable_object_id.removeprefix('transition:')}-{predicate_id.lower()}"
    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        "request_id": request_id,
        "ledger_id": LEDGER_ID,
        "property_id": PROPERTY_ID,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": "EQUIVALENT",
        "relation_scope": RelationScope.PARENT_COMPOSITE,
        "predicate_id": predicate_id,
        "artifact_role": artifact_role,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": [
            "The complete root-owned initial-carrier inventory is transition:line:19 and transition:line:21.",
            "The constituent exactness relation applies to the parent non-short-circuit AND property.",
        ],
        "expected_boolean_for_acceptance": expected,
        "created_at": CREATED_AT,
    }
    return PredicateExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def _parent_request(
    *,
    candidate: object,
    proposal_sha256: str,
    artifact_role: ArtifactRole,
    artifact_path: str,
    artifact_sha256: str,
    expected_children: tuple[bool, ...],
) -> CompositeExecutionRequest:
    """Build the complete pre-result AND request in frozen candidate order."""

    constituents = tuple(
        _child_request(
            wrapper=wrapper,
            proposal_sha256=proposal_sha256,
            artifact_role=artifact_role,
            artifact_path=artifact_path,
            artifact_sha256=artifact_sha256,
            expected=expected,
        )
        for wrapper, expected in zip(candidate.typed_inputs, expected_children, strict=True)
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.composite-request.v1",
        "request_id": f"ins0000-04-{artifact_role.value.lower()}-root-initial-composite",
        "ledger_id": LEDGER_ID,
        "property_id": PROPERTY_ID,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": "EQUIVALENT",
        "operator": "AND",
        "no_short_circuit": True,
        "artifact_role": artifact_role,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "constituents": [item.model_dump(mode="json") for item in constituents],
        "assumptions": list(candidate.assumptions),
        "expected_boolean_for_acceptance": artifact_role == ArtifactRole.POSITIVE_CONTROL,
        "created_at": CREATED_AT,
    }
    return CompositeExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def build(repo_root: Path) -> dict[str, object]:
    """Validate the blind proposal and write defective/control request bytes."""

    gold_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1"
    track_b_path = gold_root / "review/pilot_independent/track_b_pair_0000.json"
    batch = TrackBProposalBatch.model_validate_json(track_b_path.read_text(encoding="utf-8"))
    row, candidate = _selected_row(batch)
    defective = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/selected_seed_examples/llms_emp_feedback_final_0000/model.fcstm"
    control = gold_root / "controls/INS-0000-04/minimal_repair.fcstm"
    defective_path = defective.relative_to(repo_root).as_posix()
    control_path = control.relative_to(repo_root).as_posix()
    defective_request = _parent_request(
        candidate=candidate,
        proposal_sha256=row.proposal_sha256,
        artifact_role=ArtifactRole.DEFECTIVE,
        artifact_path=defective_path,
        artifact_sha256=sha256_path(defective),
        expected_children=(False, True, False, True),
    )
    control_request = _parent_request(
        candidate=candidate,
        proposal_sha256=row.proposal_sha256,
        artifact_role=ArtifactRole.POSITIVE_CONTROL,
        artifact_path=control_path,
        artifact_sha256=sha256_path(control),
        expected_children=(True, True, True, True),
    )
    output_root = gold_root / "receipts/INS-0000-04"
    defective_request_path = output_root / "defective/request.json"
    control_request_path = output_root / "positive_control/request.json"
    write_json(defective_request_path, defective_request.model_dump(mode="json"))
    write_json(control_request_path, control_request.model_dump(mode="json"))
    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.pilot-request-manifest.v1",
        "ledger_id": LEDGER_ID,
        "track_b_path": track_b_path.relative_to(repo_root).as_posix(),
        "track_b_sha256": sha256_path(track_b_path),
        "proposal_sha256": row.proposal_sha256,
        "selected_candidate_id": candidate.candidate_id,
        "created_at": CREATED_AT,
        "execution_results_visible": False,
        "v60_actual_visible": False,
        "requests": [
            {
                "artifact_role": "DEFECTIVE",
                "path": defective_request_path.relative_to(gold_root).as_posix(),
                "sha256": sha256_path(defective_request_path),
                "request_sha256": defective_request.request_sha256,
            },
            {
                "artifact_role": "POSITIVE_CONTROL",
                "path": control_request_path.relative_to(gold_root).as_posix(),
                "sha256": sha256_path(control_request_path),
                "request_sha256": control_request.request_sha256,
            },
        ],
    }
    manifest = {**unsigned_manifest, "manifest_sha256": canonical_sha256(unsigned_manifest)}
    write_json(output_root / "request_manifest.json", manifest)
    return manifest


def main() -> int:
    """CLI entry point for deterministic pilot request generation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.repo_root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
