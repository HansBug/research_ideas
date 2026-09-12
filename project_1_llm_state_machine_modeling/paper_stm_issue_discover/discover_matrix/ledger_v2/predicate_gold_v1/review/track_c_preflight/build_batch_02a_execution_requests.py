"""Freeze batch-02a controls, corrected proposals, and execution requests."""

# ruff: noqa: ISC004 -- adjacent literals keep audited FCSTM replacement blocks readable

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    ExactnessRelation,
    JsonType,
    TypedInput,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_composite import CompositeExecutionRequest
from paper_stm_evaluation.predicate_gold_execution import (
    ArtifactRole as PredicateArtifactRole,
)
from paper_stm_evaluation.predicate_gold_execution import (
    PredicateExecutionRequest,
    RelationScope,
)
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    ArtifactRole as RelationArtifactRole,
)
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    RelationOracleId,
    RelationOracleRequest,
)
from paper_stm_evaluation.predicate_gold_review import TrackBProposalBatch

CONTROL_TRANSFORMS: dict[str, tuple[str, tuple[tuple[str, str], ...], str]] = {
    "EIS-0007-01": (
        "0007",
        (
            (
                "    [*] -> InitialState;\n}",
                "    InitialState -> CollisionDetection;\n    [*] -> InitialState;\n}",
            ),
        ),
        "Add the missing re-arm/activation topology carrier from InitialState to CollisionDetection; preserve all other authored carriers.",
    ),
    "EIS-0007-02": (
        "0007",
        (
            (
                "        [*] -> AutomaticBraking : /Start_Braking;",
                "        [*] -> AutomaticBraking;",
            ),
            (
                "        [*] -> SteeringControl : /Steering_Engaged;",
                "        [*] -> SteeringControl;",
            ),
            (
                "        [*] -> AlertSystem : /Alerts_Activated;",
                "        [*] -> AlertSystem;",
            ),
        ),
        "Remove only the three event attachments from the complete native region-initial carrier set.",
    ),
    "EIS-0009-01": (
        "0009",
        (
            (
                "            cruise -> FinishState : /dist_to_exit_2;",
                "            cruise -> [*] : /dist_to_exit_2;",
            ),
            (
                "            lane_change -> FinishState : /dist_to_exit_2;",
                "            lane_change -> [*] : /dist_to_exit_2;",
            ),
        ),
        "Remove the two forbidden HighwayMode dist_to_exit_2-to-FinishState signatures without inventing a replacement target.",
    ),
    "EIS-0009-02": (
        "0009",
        (
            (
                '            state intersection named "intersection";',
                '            state intersection named "intersection";\n            state exit_urban named "exit_urban";',
            ),
            (
                "            lane_change_urban -> [*] : /dist_to_exit_0_7 effect { R45RouteToken = 17; };",
                "            lane_change_urban -> exit_urban : /dist_to_exit_0_7;",
            ),
        ),
        "Declare exit_urban in UrbanMode and retarget only the clause-8 dist_to_exit_0_7 carrier to it.",
    ),
    "EIS-0009-03": (
        "0009",
        (
            (
                '        state HighwayMode named "HighwayMode" {',
                '        state FinishState named "FinishState";\n        state HighwayMode named "HighwayMode" {',
            ),
            ('            state FinishState named "FinishState";\n', ""),
            (
                "            [*] -> FinishState : if [R45RouteToken == 17] effect { R45RouteToken = 0; };\n"
                "            [*] -> FinishState : if [R45RouteToken == 20] effect { R45RouteToken = 0; };\n"
                "            [*] -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; };\n",
                "",
            ),
            (
                "            cruise -> FinishState : /dist_to_exit_2;",
                "            cruise -> [*] : /dist_to_exit_2 effect { R45RouteToken = 17; };",
            ),
            (
                "            lane_change -> FinishState : /dist_to_exit_2;",
                "            lane_change -> [*] : /dist_to_exit_2 effect { R45RouteToken = 17; };",
            ),
            (
                "            FinishState -> [*] : /auto_finished_true effect { R45RouteToken = 20; };\n",
                "",
            ),
            (
                "            FinishState -> [*] : /urban_way_true effect { R45RouteToken = 22; };\n",
                "",
            ),
            (
                "        UrbanMode -> HighwayMode : if [R45RouteToken == 17];\n"
                "        HighwayMode -> HighwayMode : if [R45RouteToken == 20];\n"
                "        UrbanMode -> HighwayMode : if [R45RouteToken == 21];",
                "        HighwayMode -> FinishState : if [R45RouteToken == 17] effect { R45RouteToken = 0; };\n"
                "        UrbanMode -> FinishState : if [R45RouteToken == 17] effect { R45RouteToken = 0; };\n"
                "        HighwayMode -> FinishState : if [R45RouteToken == 20] effect { R45RouteToken = 0; };\n"
                "        UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; };",
            ),
        ),
        "Move the sole FinishState declaration to the shared AutonomousMode owner and retarget the affected owner-exit continuations so the control remains pyfcstm-valid.",
    ),
    "VU-0009-01": (
        "0009",
        (
            (
                "    [*] -> AutonomousMode;",
                "    [*] -> AutonomousMode;\n    !AutonomousMode -> CollisionAvoidanceSystem;",
            ),
        ),
        "Add one pyfcstm-native forced carrier from every active AutonomousMode descendant to CollisionAvoidanceSystem; this is only a source-static topology control and makes no concurrency claim.",
    ),
    "EIS-0010-02": (
        "0010",
        (
            (
                '    state Autonomous named "Autonomous\\n[PlantUML body] Autonomous Mode\\n[PlantUML body] <<submachine>>";\n'
                '    state AutonomousIdle named "AutonomousIdle\\n[PlantUML body] Autonomous Idle Mode";\n'
                '    state AutonomousActive named "AutonomousActive\\n[PlantUML body] Autonomous Active Mode";',
                '    state Autonomous named "Autonomous\\n[PlantUML body] Autonomous Mode\\n[PlantUML body] <<submachine>>" {\n'
                '        state AutonomousIdle named "AutonomousIdle\\n[PlantUML body] Autonomous Idle Mode";\n'
                '        state AutonomousActive named "AutonomousActive\\n[PlantUML body] Autonomous Active Mode";\n'
                "        [*] -> AutonomousIdle;\n"
                "        AutonomousIdle -> AutonomousActive : /Front_Distance_10_2;\n"
                "    }",
            ),
            (
                "    Autonomous -> AutonomousIdle : /Front_Distance_10;\n"
                "    AutonomousIdle -> AutonomousActive : /Front_Distance_10_2;\n"
                "    AutonomousActive -> HumanDriving : /Human_Steering_Cmd;\n"
                "    AutonomousActive -> HumanDriving : /Brake_Pressed;",
                "    Autonomous -> HumanDriving : /Human_Steering_Cmd;\n"
                "    Autonomous -> HumanDriving : /Brake_Pressed;",
            ),
        ),
        "Make Autonomous a compound state with AutonomousIdle and AutonomousActive as its direct native children; preserve a parsable source-static control without claiming full behavioral repair.",
    ),
    "EIS-0010-05": (
        "0010",
        (
            (
                "    HumanDriving -> AutonomousFinal : /Power_Off;",
                "    HumanDriving -> AutonomousFinal : /Power_Off;\n"
                "    Autonomous -> AutonomousFinal : /Power_Off;\n"
                "    AutonomousIdle -> AutonomousFinal : /Power_Off;\n"
                "    AutonomousActive -> AutonomousFinal : /Power_Off;",
            ),
        ),
        "Add only the three missing Power_Off-to-AutonomousFinal source cells required by the finite static coverage property.",
    ),
    "VU-0010-01": (
        "0010",
        (
            (
                "    AutonomousActive -> HumanDriving : /Brake_Pressed;",
                "    AutonomousActive -> HumanDriving : /Brake_Pressed;\n"
                "    Autonomous -> HumanDriving : /Human_Steering_Cmd;\n"
                "    Autonomous -> HumanDriving : /Brake_Pressed;\n"
                "    AutonomousIdle -> HumanDriving : /Human_Steering_Cmd;\n"
                "    AutonomousIdle -> HumanDriving : /Brake_Pressed;",
            ),
        ),
        "Add only the four missing source/event takeover cells; retain the two existing AutonomousActive carriers.",
    ),
}


ORACLE_IDS = {
    "EIS-0009-01": RelationOracleId.FORBIDDEN_SIGNATURES_ABSENT,
    "EIS-0009-02": RelationOracleId.REQUIRED_SIGNATURE_PRESENT,
    "EIS-0009-03": RelationOracleId.UNIQUE_STATE_DIRECT_PARENT,
    "EIS-0010-02": RelationOracleId.DIRECT_CHILD_HIERARCHY,
    "EIS-0010-05": RelationOracleId.ANCESTOR_EVENT_TARGET_COVERAGE,
    "VU-0010-01": RelationOracleId.ANCESTOR_EVENT_TARGET_COVERAGE,
}


def _write_controls(
    repo_root: Path, paper_root: Path, gold_root: Path, created_at: str
) -> dict[str, Path]:
    """Apply exact, count-checked control edits and prove pyfcstm acceptance."""

    from pyfcstm.model import load_state_machine_from_text

    outputs: dict[str, Path] = {}
    for ledger_id, (pair_id, replacements, repair_intent) in CONTROL_TRANSFORMS.items():
        source = (
            paper_root
            / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        )
        source_text = source.read_text(encoding="utf-8")
        control_text = source_text
        changes: list[dict[str, Any]] = []
        for before, after in replacements:
            count = control_text.count(before)
            if count != 1:
                raise ValueError(
                    f"{ledger_id} control edit expected one exact match, got {count}"
                )
            control_text = control_text.replace(before, after, 1)
            changes.append(
                {
                    "before_sha256": canonical_sha256(before),
                    "after_sha256": canonical_sha256(after),
                    "before": before,
                    "after": after,
                    "match_count": count,
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
            "source_artifact_path": source.resolve().relative_to(repo_root).as_posix(),
            "source_artifact_sha256": sha256_path(source),
            "control_artifact_path": artifact.resolve()
            .relative_to(repo_root)
            .as_posix(),
            "control_artifact_sha256": sha256_path(artifact),
            "repair_intent": repair_intent,
            "exact_text_changes": changes,
            "pyfcstm_parse_status": "PASS",
            "method_or_judge_output_used": False,
            "created_at": created_at,
        }
        write_json(
            control_root / "control_provenance.json",
            {**unsigned, "provenance_sha256": canonical_sha256(unsigned)},
        )
        outputs[ledger_id] = artifact
    return outputs


def _normalized_candidate_inputs(
    ledger_id: str, candidate: Any
) -> tuple[TypedInput, ...]:
    """Apply only source-preserving input-shape normalization required by an oracle contract."""

    result: list[TypedInput] = []
    for item in candidate.typed_inputs:
        if ledger_id in {"EIS-0009-01", "EIS-0009-02"}:
            result.append(item.model_copy(update={"normalized_value": item.value}))
        elif ledger_id == "EIS-0010-05" and item.field_name == "event":
            result.append(
                item.model_copy(
                    update={
                        "field_name": "events",
                        "json_type": JsonType.ARRAY,
                        "value": [item.value],
                        "normalized_value": [item.normalized_value],
                        "reason": item.reason
                        + " The relation oracle normalizes the singleton event into the same finite-array shape used for multi-event coverage.",
                    }
                )
            )
        else:
            result.append(item)
    return tuple(result)


def _corrected_proposal(
    ledger_id: str,
    b_row: Any,
    preflight_row: dict[str, Any],
    candidate: Any,
    typed_inputs: tuple[TypedInput, ...],
    created_at: str,
) -> tuple[dict[str, Any], str]:
    """Freeze Track C's relation correction and input canonicalization before execution."""

    relation = ExactnessRelation(preflight_row["accepted_relation"])
    selected = candidate.model_dump(mode="json")
    selected["exactness_relation"] = relation.value
    selected["typed_inputs"] = [item.model_dump(mode="json") for item in typed_inputs]
    selected["semantic_gaps"] = [
        *selected["semantic_gaps"],
        preflight_row["implication_analysis"]["reason"],
    ]
    selected["reason"] = (
        candidate.reason
        + " Track C preflight fixed this relation and input shape before any execution result was visible."
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.corrected-execution-proposal.v1",
        "ledger_id": ledger_id,
        "track_b_proposal_sha256": b_row.proposal_sha256,
        "track_c_preflight_row_sha256": preflight_row["audit_sha256"],
        "selected_candidate": selected,
        "final_pre_execution_relation": relation.value,
        "execution_required": True,
        "v60_actual_visible": False,
        "created_at": created_at,
    }
    digest = canonical_sha256(unsigned)
    return {**unsigned, "proposal_sha256": digest}, digest


def _child_input(
    template: TypedInput, *, name: str, value: Any, stable_id: str
) -> TypedInput:
    """Project one composite wrapper member into a frozen predicate input."""

    json_type = JsonType.ARRAY if isinstance(value, list) else JsonType.STRING
    return TypedInput(
        field_name=name,
        json_type=json_type,
        value=value,
        normalized_value=value,
        provenance_kind=template.provenance_kind,
        source_ref=template.source_ref,
        stable_object_id=stable_id,
        alias_resolution=template.alias_resolution,
        reason=f"Composite member {name} is bound directly from the pre-execution finite input inventory for {template.stable_object_id}.",
    )


def _predicate_child(
    *,
    ledger_id: str,
    property_id: str,
    proposal_sha256: str,
    relation: ExactnessRelation,
    predicate_id: str,
    role: PredicateArtifactRole,
    artifact: Path,
    repo_root: Path,
    typed_inputs: tuple[TypedInput, ...],
    request_id: str,
    created_at: str,
) -> PredicateExecutionRequest:
    """Build one fully executed constituent of a parent AND property."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        "request_id": request_id,
        "ledger_id": ledger_id,
        "property_id": property_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": relation,
        "relation_scope": RelationScope.PARENT_COMPOSITE,
        "predicate_id": predicate_id,
        "artifact_role": role,
        "artifact_path": artifact.resolve().relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": [
            "Every composite constituent executes; a prior false result cannot skip this request.",
            "The parent property retains Track C's pre-execution O/P relation.",
        ],
        "expected_boolean_for_acceptance": role
        == PredicateArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return PredicateExecutionRequest(
        **unsigned, request_sha256=canonical_sha256(unsigned)
    )


def _predicate_composite(
    ledger_id: str,
    candidate: Any,
    typed_inputs: tuple[TypedInput, ...],
    proposal_sha256: str,
    relation: ExactnessRelation,
    role: PredicateArtifactRole,
    artifact: Path,
    repo_root: Path,
    created_at: str,
) -> CompositeExecutionRequest:
    """Build G1 or S3 AND requests from the pre-reviewed finite member inventory."""

    template = typed_inputs[0]
    members = template.value
    if not isinstance(members, list):
        raise TypeError(f"{ledger_id} composite member inventory is not an array")
    children: list[PredicateExecutionRequest] = []
    if ledger_id == "EIS-0007-01":
        for index, member in enumerate(members):
            children.append(
                _predicate_child(
                    ledger_id=ledger_id,
                    property_id=candidate.candidate_id,
                    proposal_sha256=proposal_sha256,
                    relation=relation,
                    predicate_id="G1",
                    role=role,
                    artifact=artifact,
                    repo_root=repo_root,
                    typed_inputs=(
                        _child_input(
                            template,
                            name="source",
                            value=member["source"],
                            stable_id=member["source"],
                        ),
                        _child_input(
                            template,
                            name="target",
                            value=member["target"],
                            stable_id=member["target"],
                        ),
                    ),
                    request_id=f"{ledger_id.lower()}-{role.value.lower()}-g1-{index}",
                    created_at=created_at,
                )
            )
    else:
        for index, member in enumerate(members):
            transition = member["transition"]
            children.append(
                _predicate_child(
                    ledger_id=ledger_id,
                    property_id=candidate.candidate_id,
                    proposal_sha256=proposal_sha256,
                    relation=relation,
                    predicate_id="S3",
                    role=role,
                    artifact=artifact,
                    repo_root=repo_root,
                    typed_inputs=(
                        _child_input(
                            template,
                            name="transition",
                            value=transition,
                            stable_id=transition,
                        ),
                        _child_input(
                            template,
                            name="triggers",
                            value=member["triggers"],
                            stable_id=transition,
                        ),
                    ),
                    request_id=f"{ledger_id.lower()}-{role.value.lower()}-s3-{index}",
                    created_at=created_at,
                )
            )
    unsigned = {
        "schema_version": "paper1.predicate-gold.composite-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-and",
        "ledger_id": ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": relation,
        "operator": "AND",
        "no_short_circuit": True,
        "artifact_role": role,
        "artifact_path": artifact.resolve().relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "constituents": [item.model_dump(mode="json") for item in children],
        "assumptions": [
            "The finite constituent inventory is source-provenanced and frozen before execution.",
            "The AND parent is true iff every child is true; all children execute without short-circuiting.",
        ],
        "expected_boolean_for_acceptance": role
        == PredicateArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return CompositeExecutionRequest(
        **unsigned, request_sha256=canonical_sha256(unsigned)
    )


def _relation_request(
    ledger_id: str,
    candidate: Any,
    typed_inputs: tuple[TypedInput, ...],
    proposal_sha256: str,
    relation: ExactnessRelation,
    role: RelationArtifactRole,
    artifact: Path,
    repo_root: Path,
    created_at: str,
) -> RelationOracleRequest:
    """Build one narrow evaluation-only native relation request."""

    unsigned = {
        "schema_version": "paper1.predicate-gold.relation-oracle-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-native-relation",
        "ledger_id": ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": relation,
        "oracle_id": ORACLE_IDS[ledger_id],
        "artifact_role": role,
        "artifact_path": artifact.resolve().relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": [
            *candidate.assumptions,
            "Execution uses pyfcstm native objects and provenance-preserving carrier projection only.",
            "Execution cannot upgrade the pre-reviewed O/P relation.",
        ],
        "expected_boolean_for_acceptance": role
        == RelationArtifactRole.POSITIVE_CONTROL,
        "created_at": created_at,
    }
    return RelationOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def main() -> int:
    """Write all batch-02a inputs without evaluating any property."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = (
        repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    )
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    controls = _write_controls(repo_root, paper_root, gold_root, args.created_at)
    b_path = gold_root / "review/track_b_independent/batch_02a.json"
    preflight_path = args.preflight.resolve()
    b_batch = TrackBProposalBatch.model_validate_json(
        b_path.read_text(encoding="utf-8")
    )
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    preflight_rows = {row["ledger_id"]: row for row in preflight["rows"]}
    executable = sorted(
        ledger_id
        for ledger_id, row in preflight_rows.items()
        if row["execution_required"] is True
    )
    if executable != sorted(CONTROL_TRANSFORMS):
        raise ValueError(
            "batch-02a execution set differs from the pre-reviewed control set"
        )
    manifest_rows: list[dict[str, Any]] = []
    for ledger_id in executable:
        b_row = b_rows[ledger_id]
        preflight_row = preflight_rows[ledger_id]
        candidate = next(
            item
            for item in b_row.candidate_properties
            if item.candidate_id == b_row.selected_candidate_id
        )
        typed_inputs = _normalized_candidate_inputs(ledger_id, candidate)
        proposal, proposal_sha256 = _corrected_proposal(
            ledger_id,
            b_row,
            preflight_row,
            candidate,
            typed_inputs,
            args.created_at,
        )
        issue_root = gold_root / "receipts" / ledger_id
        write_json(issue_root / "proposal.json", proposal)
        relation = ExactnessRelation(preflight_row["accepted_relation"])
        pair_id = ledger_id.split("-")[1]
        defective = (
            paper_root
            / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        )
        request_rows: list[dict[str, str]] = []
        for role_name, artifact in (
            ("defective", defective),
            ("positive_control", controls[ledger_id]),
        ):
            root = issue_root / role_name
            if ledger_id in {"EIS-0007-01", "EIS-0007-02", "VU-0009-01"}:
                if ledger_id == "VU-0009-01":
                    predicate_role = (
                        PredicateArtifactRole.DEFECTIVE
                        if role_name == "defective"
                        else PredicateArtifactRole.POSITIVE_CONTROL
                    )
                    unsigned = {
                        "schema_version": "paper1.predicate-gold.execution-request.v1",
                        "request_id": f"{ledger_id.lower()}-{role_name}-g1",
                        "ledger_id": ledger_id,
                        "property_id": candidate.candidate_id,
                        "property_proposal_sha256": proposal_sha256,
                        "exactness_relation": relation,
                        "relation_scope": RelationScope.THIS_PROPERTY,
                        "predicate_id": "G1",
                        "artifact_role": predicate_role,
                        "artifact_path": artifact.resolve()
                        .relative_to(repo_root)
                        .as_posix(),
                        "artifact_sha256": sha256_path(artifact),
                        "typed_inputs": [
                            item.model_dump(mode="json") for item in typed_inputs
                        ],
                        "assumptions": [
                            *candidate.assumptions,
                            "G1 remains a guard/event-agnostic necessary topology proxy.",
                        ],
                        "expected_boolean_for_acceptance": role_name
                        == "positive_control",
                        "created_at": args.created_at,
                    }
                    request: Any = PredicateExecutionRequest(
                        **unsigned, request_sha256=canonical_sha256(unsigned)
                    )
                    request_kind = "FROZEN_PREDICATE"
                else:
                    predicate_role = (
                        PredicateArtifactRole.DEFECTIVE
                        if role_name == "defective"
                        else PredicateArtifactRole.POSITIVE_CONTROL
                    )
                    request = _predicate_composite(
                        ledger_id,
                        candidate,
                        typed_inputs,
                        proposal_sha256,
                        relation,
                        predicate_role,
                        artifact,
                        repo_root,
                        args.created_at,
                    )
                    request_kind = "FROZEN_PREDICATE_COMPOSITE"
            else:
                relation_role = (
                    RelationArtifactRole.DEFECTIVE
                    if role_name == "defective"
                    else RelationArtifactRole.POSITIVE_CONTROL
                )
                request = _relation_request(
                    ledger_id,
                    candidate,
                    typed_inputs,
                    proposal_sha256,
                    relation,
                    relation_role,
                    artifact,
                    repo_root,
                    args.created_at,
                )
                request_kind = "EVALUATION_ONLY_RELATION"
            write_json(root / "request.json", request.model_dump(mode="json"))
            request_rows.append(
                {
                    "artifact_sha256": sha256_path(artifact),
                    "request_kind": request_kind,
                    "request_path": (root / "request.json")
                    .relative_to(gold_root)
                    .as_posix(),
                    "request_file_sha256": sha256_path(root / "request.json"),
                    "request_payload_sha256": request.request_sha256,
                }
            )
        manifest_rows.append(
            {
                "ledger_id": ledger_id,
                "final_pre_execution_relation": relation.value,
                "proposal_path": (issue_root / "proposal.json")
                .relative_to(gold_root)
                .as_posix(),
                "proposal_file_sha256": sha256_path(issue_root / "proposal.json"),
                "proposal_payload_sha256": proposal_sha256,
                "control_provenance_path": f"controls/{ledger_id}/control_provenance.json",
                "roles": request_rows,
            }
        )
    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.execution-request-manifest.v1",
        "batch_id": "batch_02a",
        "track_c_preflight_batch_sha256": preflight["batch_sha256"],
        "rows": manifest_rows,
        "created_at": args.created_at,
        "no_execution_performed_by_builder": True,
    }
    output = gold_root / "receipts/batch_02a_request_manifest.json"
    write_json(
        output,
        {**unsigned_manifest, "manifest_sha256": canonical_sha256(unsigned_manifest)},
    )
    print(f"wrote {output} ({len(manifest_rows)} issues)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
