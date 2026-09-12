"""Freeze batch-04a controls, corrected proposals, and execution requests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    ExactnessRelation,
    TypedInput,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_execution import (
    ArtifactRole as PredicateArtifactRole,
)
from paper_stm_evaluation.predicate_gold_execution import (
    PredicateExecutionRequest,
    RelationScope,
)
from paper_stm_evaluation.predicate_gold_native_composite import (
    NativeCompositeRequest,
)
from paper_stm_evaluation.predicate_gold_oracle import (
    ArtifactRole as NativeArtifactRole,
)
from paper_stm_evaluation.predicate_gold_oracle import NativeOracleRequest
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    ArtifactRole as RelationArtifactRole,
)
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    RelationOracleId,
    RelationOracleRequest,
)
from paper_stm_evaluation.predicate_gold_review import TrackBProposalBatch

CONTROL_TRANSFORMS: dict[str, tuple[str, tuple[tuple[str, str], ...], str]] = {
    "DIFF-0019-05": (
        "0019",
        (
            (
                "        [*] -> InitialState : /Start_of_autonomous_driving_mode;",
                "        [*] -> InitialState;",
            ),
            (
                "    [*] -> AutonomousMode : /Autonomous_mode_start;",
                "    [*] -> AutonomousMode;",
            ),
        ),
        "Remove only the two event attachments from the source-fixed root and AutonomousMode initial carriers; retain targets, owner scopes and every unrelated carrier.",
    ),
    "EIS-0019-02": (
        "0019",
        (
            (
                '        state UnspecifiedInitial named "Unspecified initial";\n',
                "",
            ),
            (
                "        [*] -> UnspecifiedInitial;",
                "        [*] -> collision_avoidance_deactive;",
            ),
        ),
        "Replace the converter placeholder with the exact NL-specified collision_avoidance_deactive default target; no subsystem reachability repair is claimed.",
    ),
    "DIFF-0024-04": (
        "0024",
        (("    EmergencyStopping -> InMotion : /exit_Send_Obstacle_Detected;\n", ""),),
        "Remove only the disputed EmergencyStopping-to-InMotion recovery carrier. This property-specific control does not claim to repair the separate output-action obligation.",
    ),
    "EIS-0024-01": (
        "0024",
        (
            (
                '        state Accelerating named "Accelerating\\n[PlantUML body] Accelerating";',
                (
                    '        state Accelerating named "Accelerating\\n[PlantUML body] '
                    'Accelerating" {\n'
                    "            enter abstract Accelerate;\n"
                    "        }"
                ),
            ),
        ),
        "Attach the exact author token Accelerate to the exact entry lifecycle slot of Accelerating; no physical action effect is invented.",
    ),
    "EIS-0024-03": (
        "0024",
        (("        Approaching -> [*] : /exit_Send effect { R45RouteToken = 7; };\n", ""),),
        "Remove only the source-attributed unauthorized Approaching exit/Send first-leg carrier; this proxy control does not prove the full unbounded remain-until obligation.",
    ),
}


def _write_controls(
    repo_root: Path, paper_root: Path, gold_root: Path, created_at: str
) -> dict[str, Path]:
    """Apply exact count-checked edits and prove every control parses in pyfcstm."""

    from pyfcstm.model import load_state_machine_from_text

    outputs: dict[str, Path] = {}
    for ledger_id, (pair_id, replacements, repair_intent) in CONTROL_TRANSFORMS.items():
        source = paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        source_text = source.read_text(encoding="utf-8")
        control_text = source_text
        changes: list[dict[str, Any]] = []
        for before, after in replacements:
            match_count = control_text.count(before)
            if match_count != 1:
                raise ValueError(
                    f"{ledger_id} control edit expected one exact match, got {match_count}"
                )
            control_text = control_text.replace(before, after, 1)
            changes.append(
                {
                    "before": before,
                    "after": after,
                    "before_sha256": canonical_sha256(before),
                    "after_sha256": canonical_sha256(after),
                    "match_count": match_count,
                }
            )
        load_state_machine_from_text(control_text)
        control_root = gold_root / "controls" / ledger_id
        artifact = control_root / "minimal_repair.fcstm"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(control_text, encoding="utf-8")
        unsigned = {
            "schema_version": "paper1.predicate-gold.positive-control-provenance.v1",
            "ledger_id": ledger_id,
            "source_artifact_path": source.relative_to(repo_root).as_posix(),
            "source_artifact_sha256": sha256_path(source),
            "control_artifact_path": artifact.relative_to(repo_root).as_posix(),
            "control_artifact_sha256": sha256_path(artifact),
            "repair_intent": repair_intent,
            "exact_text_changes": changes,
            "pyfcstm_parse_status": "PASS",
            "method_or_judge_output_used": False,
            "same_issue_execution_result_visible": False,
            "created_at": created_at,
        }
        write_json(
            control_root / "control_provenance.json",
            {**unsigned, "provenance_sha256": canonical_sha256(unsigned)},
        )
        outputs[ledger_id] = artifact
    return outputs


def _candidate(row: Any, candidate_id: str) -> Any:
    """Return exactly one candidate from a frozen Track B row."""

    matches = [item for item in row.candidate_properties if item.candidate_id == candidate_id]
    if len(matches) != 1:
        raise ValueError(f"expected one candidate {candidate_id}, got {len(matches)}")
    return matches[0]


def _corrected_proposal(
    *,
    ledger_id: str,
    b_row: Any,
    preflight_row: dict[str, Any],
    candidate: Any,
    child_candidates: tuple[Any, ...],
    created_at: str,
    repo_root: Path,
    paper_root: Path,
) -> tuple[dict[str, Any], str]:
    """Freeze the accepted property, child scope and current execution code hashes."""

    relation = ExactnessRelation(preflight_row["accepted_relation"])
    selected = candidate.model_dump(mode="json")
    selected["exactness_relation"] = relation.value
    selected["selected"] = True
    selected["semantic_gaps"] = [
        gap
        for gap in selected["semantic_gaps"]
        if "runner" not in gap.lower() and "unimplemented" not in gap.lower()
    ]
    selected["reason"] = (
        preflight_row["implication_analysis"]["reason"]
        + " This relation was frozen before same-issue execution."
    )
    if child_candidates:
        selected["mode"] = "EVALUATION_ONLY_ORACLE"
        selected["composition"] = {
            "operator": "AND",
            "no_short_circuit": True,
            "constituents": [
                {
                    **child.model_dump(mode="json"),
                    "exactness_relation": ExactnessRelation.EQUIVALENT.value,
                    "relation_scope": "EXACT_OWNER_LOCAL_SUB_OBLIGATION",
                }
                for child in child_candidates
            ],
            "parent_relation_scope": "COMPLETE_LEDGER_OBLIGATION",
        }
    code_paths = (
        paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_execution.py",
        paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_oracle.py",
        paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_native_composite.py",
        paper_root / "evaluation/src/paper_stm_evaluation/predicate_gold_relation_oracle.py",
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.corrected-execution-proposal.v1",
        "ledger_id": ledger_id,
        "track_b_proposal_sha256": b_row.proposal_sha256,
        "track_c_preflight_row_sha256": preflight_row["audit_sha256"],
        "selected_candidate": selected,
        "final_pre_execution_relation": relation.value,
        "execution_required": True,
        "execution_code_refs": [
            {
                "repository_path": path.relative_to(repo_root).as_posix(),
                "sha256": sha256_path(path),
            }
            for path in code_paths
        ],
        "v60_actual_visible": False,
        "same_issue_execution_result_visible": False,
        "created_at": created_at,
    }
    digest = canonical_sha256(unsigned)
    return {**unsigned, "proposal_sha256": digest}, digest


def _native_request(
    *,
    ledger_id: str,
    property_id: str,
    typed_inputs: tuple[TypedInput, ...],
    assumptions: tuple[str, ...],
    proposal_sha256: str,
    relation: ExactnessRelation,
    role: NativeArtifactRole,
    artifact: Path,
    repo_root: Path,
    request_id: str,
    created_at: str,
) -> NativeOracleRequest:
    """Build one exact native initial-transition query without evaluating it."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.native-oracle-request.v1",
        "request_id": request_id,
        "ledger_id": ledger_id,
        "property_id": property_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": relation,
        "oracle_id": "NATIVE_INITIAL_TRANSITION_CONTRACT",
        "artifact_role": role,
        "artifact_path": artifact.relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": [
            *assumptions,
            "Execution uses complete pyfcstm State.init_transitions inventories and exact native paths.",
            "Execution cannot upgrade or alter the pre-reviewed O/P relation.",
        ],
        "expected_boolean_for_acceptance": role == NativeArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return NativeOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def _native_composite_request(
    *,
    ledger_id: str,
    parent_candidate: Any,
    children: tuple[Any, ...],
    proposal_sha256: str,
    role: NativeArtifactRole,
    artifact: Path,
    repo_root: Path,
    created_at: str,
) -> NativeCompositeRequest:
    """Build a complete two-owner AND with exact child sub-obligations."""

    child_requests = tuple(
        _native_request(
            ledger_id=ledger_id,
            property_id=child.candidate_id,
            typed_inputs=tuple(child.typed_inputs),
            assumptions=tuple(child.assumptions),
            proposal_sha256=proposal_sha256,
            relation=ExactnessRelation.EQUIVALENT,
            role=role,
            artifact=artifact,
            repo_root=repo_root,
            request_id=f"{ledger_id.lower()}-{role.value.lower()}-native-initial-{index}",
            created_at=created_at,
        )
        for index, child in enumerate(children)
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.native-composite-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-native-and",
        "ledger_id": ledger_id,
        "property_id": parent_candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": ExactnessRelation.EQUIVALENT,
        "operator": "AND",
        "no_short_circuit": True,
        "artifact_role": role,
        "artifact_path": artifact.relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "constituents": [item.model_dump(mode="json") for item in child_requests],
        "assumptions": [
            "The ledger obligation is exactly the finite conjunction of the root-owner and AutonomousMode-owner initial contracts.",
            "Every child executes without short-circuiting; the parent adds only Boolean AND.",
        ],
        "expected_boolean_for_acceptance": role == NativeArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return NativeCompositeRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def _relation_request(
    *,
    ledger_id: str,
    candidate: Any,
    proposal_sha256: str,
    relation: ExactnessRelation,
    role: RelationArtifactRole,
    artifact: Path,
    repo_root: Path,
    created_at: str,
) -> RelationOracleRequest:
    """Build one source-static forbidden-signature request."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.relation-oracle-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-forbidden-signature",
        "ledger_id": ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": relation,
        "oracle_id": RelationOracleId.FORBIDDEN_SIGNATURES_ABSENT,
        "artifact_role": role,
        "artifact_path": artifact.relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in candidate.typed_inputs],
        "assumptions": [
            *candidate.assumptions,
            "Execution enumerates exact pyfcstm native carriers and cannot upgrade the pre-reviewed relation.",
        ],
        "expected_boolean_for_acceptance": role == RelationArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return RelationOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def _predicate_request(
    *,
    ledger_id: str,
    candidate: Any,
    proposal_sha256: str,
    relation: ExactnessRelation,
    role: PredicateArtifactRole,
    artifact: Path,
    repo_root: Path,
    created_at: str,
) -> PredicateExecutionRequest:
    """Build the single accepted frozen S4 request."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-s4",
        "ledger_id": ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": relation,
        "relation_scope": RelationScope.THIS_PROPERTY,
        "predicate_id": "S4",
        "artifact_role": role,
        "artifact_path": artifact.relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in candidate.typed_inputs],
        "assumptions": [
            *candidate.assumptions,
            "The query checks exact lifecycle attachment only; it makes no physical-action execution claim.",
        ],
        "expected_boolean_for_acceptance": role == PredicateArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return PredicateExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def main() -> int:
    """Write every proposal, control, request and the no-execution manifest."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    controls = _write_controls(repo_root, paper_root, gold_root, args.created_at)
    b_path = gold_root / "review/track_b_independent/batch_04a.json"
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    preflight_path = args.preflight.resolve()
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    preflight_rows = {row["ledger_id"]: row for row in preflight["rows"]}
    executable = sorted(
        ledger_id for ledger_id, row in preflight_rows.items() if row["execution_required"]
    )
    if executable != sorted(CONTROL_TRANSFORMS):
        raise ValueError("batch_04a execution set differs from the pre-reviewed control set")

    manifest_rows: list[dict[str, Any]] = []
    for ledger_id in executable:
        row = b_rows[ledger_id]
        preflight_row = preflight_rows[ledger_id]
        candidate = _candidate(row, preflight_row["selected_candidate_id"])
        child_candidates: tuple[Any, ...] = ()
        if ledger_id == "DIFF-0019-05":
            child_candidates = (
                _candidate(row, "DIFF-0019-05-B-P1"),
                _candidate(row, "DIFF-0019-05-B-P2"),
            )
        proposal, proposal_sha256 = _corrected_proposal(
            ledger_id=ledger_id,
            b_row=row,
            preflight_row=preflight_row,
            candidate=candidate,
            child_candidates=child_candidates,
            created_at=args.created_at,
            repo_root=repo_root,
            paper_root=paper_root,
        )
        issue_root = gold_root / "receipts" / ledger_id
        write_json(issue_root / "proposal.json", proposal)
        relation = ExactnessRelation(preflight_row["accepted_relation"])
        pair_id = ledger_id.split("-")[1]
        defective = paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        role_rows: list[dict[str, str]] = []
        for role_name, artifact in (
            ("defective", defective),
            ("positive_control", controls[ledger_id]),
        ):
            if ledger_id == "DIFF-0019-05":
                native_role = (
                    NativeArtifactRole.DEFECTIVE
                    if role_name == "defective"
                    else NativeArtifactRole.POSITIVE_CONTROL
                )
                request: Any = _native_composite_request(
                    ledger_id=ledger_id,
                    parent_candidate=candidate,
                    children=child_candidates,
                    proposal_sha256=proposal_sha256,
                    role=native_role,
                    artifact=artifact,
                    repo_root=repo_root,
                    created_at=args.created_at,
                )
                request_kind = "EVALUATION_ONLY_NATIVE_COMPOSITE"
            elif ledger_id == "EIS-0019-02":
                native_role = (
                    NativeArtifactRole.DEFECTIVE
                    if role_name == "defective"
                    else NativeArtifactRole.POSITIVE_CONTROL
                )
                request = _native_request(
                    ledger_id=ledger_id,
                    property_id=candidate.candidate_id,
                    typed_inputs=tuple(candidate.typed_inputs),
                    assumptions=tuple(candidate.assumptions),
                    proposal_sha256=proposal_sha256,
                    relation=relation,
                    role=native_role,
                    artifact=artifact,
                    repo_root=repo_root,
                    request_id=f"{ledger_id.lower()}-{native_role.value.lower()}-native-initial",
                    created_at=args.created_at,
                )
                request_kind = "EVALUATION_ONLY_NATIVE_ORACLE"
            elif ledger_id in {"DIFF-0024-04", "EIS-0024-03"}:
                relation_role = (
                    RelationArtifactRole.DEFECTIVE
                    if role_name == "defective"
                    else RelationArtifactRole.POSITIVE_CONTROL
                )
                request = _relation_request(
                    ledger_id=ledger_id,
                    candidate=candidate,
                    proposal_sha256=proposal_sha256,
                    relation=relation,
                    role=relation_role,
                    artifact=artifact,
                    repo_root=repo_root,
                    created_at=args.created_at,
                )
                request_kind = "EVALUATION_ONLY_RELATION"
            else:
                predicate_role = (
                    PredicateArtifactRole.DEFECTIVE
                    if role_name == "defective"
                    else PredicateArtifactRole.POSITIVE_CONTROL
                )
                request = _predicate_request(
                    ledger_id=ledger_id,
                    candidate=candidate,
                    proposal_sha256=proposal_sha256,
                    relation=relation,
                    role=predicate_role,
                    artifact=artifact,
                    repo_root=repo_root,
                    created_at=args.created_at,
                )
                request_kind = "FROZEN_PREDICATE"
            request_path = issue_root / role_name / "request.json"
            write_json(request_path, request.model_dump(mode="json"))
            role_rows.append(
                {
                    "artifact_sha256": sha256_path(artifact),
                    "request_kind": request_kind,
                    "request_path": request_path.relative_to(gold_root).as_posix(),
                    "request_file_sha256": sha256_path(request_path),
                    "request_payload_sha256": request.request_sha256,
                }
            )
        manifest_rows.append(
            {
                "ledger_id": ledger_id,
                "final_pre_execution_relation": relation.value,
                "proposal_path": (issue_root / "proposal.json").relative_to(gold_root).as_posix(),
                "proposal_file_sha256": sha256_path(issue_root / "proposal.json"),
                "proposal_payload_sha256": proposal_sha256,
                "control_provenance_path": f"controls/{ledger_id}/control_provenance.json",
                "roles": role_rows,
            }
        )
    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.execution-request-manifest.v1",
        "batch_id": "batch_04a",
        "track_c_preflight_path": preflight_path.relative_to(gold_root).as_posix(),
        "track_c_preflight_file_sha256": sha256_path(preflight_path),
        "track_c_preflight_batch_sha256": preflight["batch_sha256"],
        "rows": manifest_rows,
        "created_at": args.created_at,
        "no_execution_performed_by_builder": True,
        "v60_actual_visible": False,
    }
    output = gold_root / "receipts/batch_04a_request_manifest.json"
    write_json(
        output,
        {**unsigned_manifest, "manifest_sha256": canonical_sha256(unsigned_manifest)},
    )
    print(f"wrote {output} ({len(manifest_rows)} issues, no execution)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
