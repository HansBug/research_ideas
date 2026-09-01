"""Build batch-05a controls, corrected proposals, and pre-result requests.

The builder consumes the already sealed semantic preflight.  It writes no
execution result and never reads v60 output or planned issue mappings.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import ExactnessRelation, canonical_sha256, sha256_path, write_json
from paper_stm_evaluation.predicate_gold_composite import CompositeExecutionRequest
from paper_stm_evaluation.predicate_gold_execution import ArtifactRole, PredicateExecutionRequest, RelationScope
from paper_stm_evaluation.predicate_gold_oracle import NativeOracleRequest
from paper_stm_evaluation.predicate_gold_relation_oracle import RelationOracleRequest
from paper_stm_evaluation.predicate_gold_review import TrackBProposalBatch
from paper_stm_evaluation.predicate_gold_static_oracle import StaticOracleRequest


CONTROL_MODELS: dict[str, str] = {
    "DIFF-0029-06": '''state llms_emp_feedback_final_0029 named "llms_emp_feedback_final_0029" {
    event auto_finished_true named "auto_finished=true";
    state AutonomousMode named "AutonomousMode";
    state HighwayMode named "HighwayMode";
    [*] -> AutonomousMode;
}
''',
    "EIS-0029-01": '''state llms_emp_feedback_final_0029 named "llms_emp_feedback_final_0029" {
    state AutonomousMode named "AutonomousMode" {
        state InitialState named "InitialState";
        state HighwayMode named "HighwayMode";
        state UrbanMode named "UrbanMode";
        [*] -> InitialState;
    }
    [*] -> AutonomousMode;
}
''',
    "EIS-0029-03": '''state llms_emp_feedback_final_0029 named "llms_emp_feedback_final_0029" {
    event dist_to_exit_2 named "dist_to_exit<2";
    state HighwayMode named "HighwayMode" {
        state cruise named "cruise";
        state exit_hwy named "exit_hwy";
        [*] -> cruise;
        cruise -> exit_hwy : /dist_to_exit_2;
    }
    [*] -> HighwayMode;
}
''',
    "EIS-0029-05": '''state llms_emp_feedback_final_0029 named "llms_emp_feedback_final_0029" {
    state AutonomousMode named "AutonomousMode" {
        state FinishState named "FinishState";
        [*] -> FinishState;
    }
    [*] -> AutonomousMode;
}
''',
    "INS-0029-05": '''state llms_emp_feedback_final_0029 named "llms_emp_feedback_final_0029" {
    event auto_finished_true named "auto_finished=true";
    state HighwayMode named "HighwayMode" {
        state enter_hwy named "enter_hwy";
        state cruise named "cruise";
        state lane_change named "lane_change";
        state exit_hwy named "exit_hwy";
        [*] -> enter_hwy;
    }
    state UrbanMode named "UrbanMode" {
        state enter_urban named "enter_urban";
        state lane_change_urban named "lane_change_urban";
        state straight named "straight";
        state intersection named "intersection";
        state exit_urban named "exit_urban";
        [*] -> enter_urban;
    }
    [*] -> HighwayMode;
    HighwayMode -> [*] : /auto_finished_true;
    UrbanMode -> [*] : /auto_finished_true;
}
''',
    "EIS-0030-02": '''state llms_emp_feedback_final_0030 named "llms_emp_feedback_final_0030" {
    event Power_Off named "Power Off";
    state HumanDriving named "HumanDriving";
    state Autonomous named "Autonomous" {
        state Navigating named "Navigating";
        state Parking named "Parking";
        [*] -> Navigating;
    }
    [*] -> HumanDriving;
    HumanDriving -> [*] : /Power_Off;
    Autonomous -> [*] : /Power_Off;
}
''',
    "INS-0030-01": '''state llms_emp_feedback_final_0030 named "llms_emp_feedback_final_0030" {
    state HumanDriving named "HumanDriving";
    state Autonomous named "Autonomous";
    [*] -> HumanDriving;
}
''',
    "DIFF-0032-03": '''state llms_emp_feedback_final_0032 named "llms_emp_feedback_final_0032" {
    event start named "start";
    state OffState named "OffState";
    state OperateState named "OperateState";
    [*] -> OffState;
    OffState -> OperateState : /start;
}
''',
    "EIS-0032-01": '''state llms_emp_feedback_final_0032 named "llms_emp_feedback_final_0032" {
    state OperateState named "OperateState" {
        state IdleRegion named "IdleRegion" {
            state IdleState named "IdleState";
            [*] -> IdleState;
        }
        state AccelerateRegion named "AccelerateRegion" {
            state AcceleratingState named "AcceleratingState";
            state CruisingState named "CruisingState";
            [*] -> AcceleratingState;
        }
        state BrakeRegion named "BrakeRegion" {
            state BrakingState named "BrakingState";
            [*] -> BrakingState;
        }
        [*] -> IdleRegion;
    }
    [*] -> OperateState;
}
''',
    "EIS-0033-02": '''state llms_emp_feedback_final_0033 named "llms_emp_feedback_final_0033" {
    state PumpControl named "PumpControl" {
        state PumpState named "PumpState";
        state WaterState named "WaterState";
        state MethaneState named "MethaneState";
        [*] -> PumpState;
    }
    [*] -> PumpControl;
}
''',
    "INS-0033-01": '''state llms_emp_feedback_final_0033 named "llms_emp_feedback_final_0033" {
    state PumpControl named "PumpControl" {
        state PumpState named "PumpState";
        [*] -> PumpState;
    }
    [*] -> PumpControl;
}
''',
    "EIS-0034-01": '''state llms_emp_feedback_final_0034 named "llms_emp_feedback_final_0034" {
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating";
        state Cruising named "Cruising";
        state Approaching named "Approaching";
        [*] -> Accelerating;
    }
    [*] -> InMotion;
}
''',
    "EIS-0034-02": '''state llms_emp_feedback_final_0034 named "llms_emp_feedback_final_0034" {
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating";
        state Cruising named "Cruising";
        state Approaching named "Approaching";
        [*] -> Accelerating;
    }
    [*] -> InMotion;
}
''',
    "EIS-0034-03": '''state llms_emp_feedback_final_0034 named "llms_emp_feedback_final_0034" {
    state DoorsClosing named "DoorsClosing";
    state Accelerating named "Accelerating" {
        enter abstract Accelerate;
    }
    [*] -> DoorsClosing;
}
''',
    "EIS-0034-04": '''state llms_emp_feedback_final_0034 named "llms_emp_feedback_final_0034" {
    state Cruising named "Cruising";
    state Approaching named "Approaching";
    [*] -> Cruising;
    Cruising -> Approaching;
}
''',
    "EIS-0034-06": '''state llms_emp_feedback_final_0034 named "llms_emp_feedback_final_0034" {
    event Destination_Missed named "Destination Missed";
    state Approaching named "Approaching";
    state Stopping named "Stopping";
    [*] -> Approaching;
    Approaching -> Stopping;
}
''',
}


PLANS: dict[str, tuple[str, str]] = {
    "DIFF-0029-06": ("relation", "FORBIDDEN_SIGNATURES_ABSENT"),
    "EIS-0029-01": ("relation", "DIRECT_CHILD_HIERARCHY"),
    "EIS-0029-03": ("relation", "REQUIRED_SIGNATURE_PRESENT"),
    "EIS-0029-05": ("relation", "UNIQUE_STATE_DIRECT_PARENT"),
    "INS-0029-05": ("static", "RUNNING_EVENT_ROOT_EXIT_CONSUMERS"),
    "EIS-0030-02": ("static", "RUNNING_EVENT_ROOT_EXIT_CONSUMERS"),
    "INS-0030-01": ("native", "NATIVE_INITIAL_TRANSITION_CONTRACT"),
    "DIFF-0032-03": ("composite", "S1"),
    "EIS-0032-01": ("composite", "S1"),
    "EIS-0033-02": ("native", "NATIVE_INITIAL_TRANSITION_CONTRACT"),
    "INS-0033-01": ("native", "NATIVE_INITIAL_TRANSITION_CONTRACT"),
    "EIS-0034-01": ("relation", "DIRECT_CHILD_HIERARCHY"),
    "EIS-0034-02": ("native", "NATIVE_INITIAL_TRANSITION_CONTRACT"),
    "EIS-0034-03": ("composite", "S4"),
    "EIS-0034-04": ("composite", "S4"),
    "EIS-0034-06": ("relation", "FORBIDDEN_SIGNATURES_ABSENT"),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _repo_root() -> Path:
    return next(parent for parent in Path(__file__).resolve().parents if (parent / "pyfcstm").is_dir() and (parent / "project_1_llm_state_machine_modeling").is_dir())


def _write_control(*, repo_root: Path, gold_root: Path, ledger_id: str, source_path: Path, created_at: str) -> Path:
    root = gold_root / "controls" / ledger_id
    control_path = root / "independent_positive_control.fcstm"
    control_path.parent.mkdir(parents=True, exist_ok=True)
    control_path.write_text(CONTROL_MODELS[ledger_id], encoding="utf-8")
    unsigned = {
        "schema_version": "paper1.predicate-gold.positive-control-provenance.v1",
        "ledger_id": ledger_id,
        "control_kind": "SOURCE_BACKED_INDEPENDENT_MINIMAL_CONTROL",
        "source_artifact_path": source_path.relative_to(repo_root).as_posix(),
        "source_artifact_sha256": sha256_path(source_path),
        "control_path": control_path.relative_to(repo_root).as_posix(),
        "control_sha256": sha256_path(control_path),
        "repair_intent": "Retain only author-named identities needed to make the pre-registered issue-local property true; this control is not claimed to repair unrelated defects or establish whole-model equivalence.",
        "constructed_before_execution": True,
        "execution_results_visible": False,
        "v60_actual_visible": False,
        "created_at": created_at,
    }
    write_json(root / "control_provenance.json", {**unsigned, "provenance_sha256": canonical_sha256(unsigned)})
    return control_path


def _proposal(*, b_row: Any, preflight_row: dict[str, Any], candidate: Any, created_at: str) -> tuple[dict[str, Any], str]:
    candidate_payload = candidate.model_dump(mode="json")
    accepted = preflight_row["accepted_relation"]
    if candidate_payload["exactness_relation"] != accepted:
        candidate_payload["semantic_gaps"] = [
            *candidate_payload["semantic_gaps"],
            preflight_row["implication_analysis"]["reason"],
        ]
        candidate_payload["reason"] += " Track C corrected the relation before execution; a false result cannot upgrade this property."
        candidate_payload["exactness_relation"] = accepted
    unsigned = {
        "schema_version": "paper1.predicate-gold.corrected-execution-proposal.v1",
        "ledger_id": b_row.ledger_id,
        "track_b_proposal_sha256": b_row.proposal_sha256,
        "track_c_preflight_row_sha256": preflight_row["audit_sha256"],
        "normalized_obligation_sha256": preflight_row["normalized_obligation_sha256"],
        "selected_candidate": candidate_payload,
        "final_pre_execution_relation": accepted,
        "execution_required": True,
        "v60_actual_visible": False,
        "created_at": created_at,
    }
    digest = canonical_sha256(unsigned)
    return {**unsigned, "proposal_sha256": digest}, digest


def _request(*, kind: str, oracle_or_predicate: str, ledger_id: str, candidate: Any, proposal_sha256: str, relation: str, role: ArtifactRole, artifact: Path, repo_root: Path, expected: bool, created_at: str) -> Any:
    artifact_path = artifact.relative_to(repo_root).as_posix()
    common = {
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-{oracle_or_predicate.lower()}",
        "ledger_id": ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": ExactnessRelation(relation),
        "artifact_role": role,
        "artifact_path": artifact_path,
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in candidate.typed_inputs],
        "assumptions": [
            *candidate.assumptions,
            "The proposal and independent positive-control bytes were hash-frozen before same-issue execution.",
            "No v60 actual predicate or result was visible to this request builder.",
        ],
        "expected_boolean_for_acceptance": expected,
        "created_at": created_at,
    }
    if kind == "relation":
        unsigned = {"schema_version": "paper1.predicate-gold.relation-oracle-request.v1", **common, "oracle_id": oracle_or_predicate}
        return RelationOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    if kind == "static":
        unsigned = {"schema_version": "paper1.predicate-gold.static-oracle-request.v1", **common, "oracle_id": oracle_or_predicate}
        return StaticOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    if kind == "native":
        unsigned = {"schema_version": "paper1.predicate-gold.native-oracle-request.v1", **common, "oracle_id": oracle_or_predicate}
        return NativeOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    child_unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        **common,
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-{oracle_or_predicate.lower()}-constituent",
        "relation_scope": RelationScope.PARENT_COMPOSITE,
        "predicate_id": oracle_or_predicate,
        "expected_boolean_for_acceptance": not expected,
    }
    child = PredicateExecutionRequest(**child_unsigned, request_sha256=canonical_sha256(child_unsigned))
    parent_unsigned = {
        "schema_version": "paper1.predicate-gold.composite-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-not-{oracle_or_predicate.lower()}",
        "ledger_id": ledger_id,
        "property_id": candidate.candidate_id,
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": ExactnessRelation(relation),
        "operator": "NOT",
        "no_short_circuit": True,
        "artifact_role": role,
        "artifact_path": artifact_path,
        "artifact_sha256": sha256_path(artifact),
        "constituents": [child.model_dump(mode="json")],
        "assumptions": common["assumptions"],
        "expected_boolean_for_acceptance": expected,
        "created_at": created_at,
    }
    return CompositeExecutionRequest(**parent_unsigned, request_sha256=canonical_sha256(parent_unsigned))


def main() -> int:
    repo_root = _repo_root()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    preflight_path = gold_root / "review/track_c_preflight/batch_05a.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    if preflight["execution_performed"] or preflight["visibility"]["execution_results_visible"]:
        raise ValueError("preflight is not pre-result")
    if set(preflight["accepted_execution_ids"]) != set(PLANS):
        raise ValueError("preflight execution set differs from the frozen plan")
    b_path = gold_root / "review/track_b_independent/batch_05a.json"
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    p_rows = {row["ledger_id"]: row for row in preflight["rows"]}
    created_at = _now()
    manifest_rows: list[dict[str, Any]] = []
    for ledger_id in sorted(PLANS):
        b_row = b_rows[ledger_id]
        p_row = p_rows[ledger_id]
        candidate = next(item for item in b_row.candidate_properties if item.candidate_id == p_row["selected_candidate_id"])
        pair_id = ledger_id.split("-")[1]
        source = paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        control = _write_control(repo_root=repo_root, gold_root=gold_root, ledger_id=ledger_id, source_path=source, created_at=created_at)
        proposal, proposal_sha256 = _proposal(b_row=b_row, preflight_row=p_row, candidate=candidate, created_at=created_at)
        issue_root = gold_root / "receipts" / ledger_id
        write_json(issue_root / "proposal.json", proposal)
        kind, oracle_or_predicate = PLANS[ledger_id]
        role_rows: list[dict[str, str]] = []
        for role_name, role, artifact, expected in (
            ("defective", ArtifactRole.DEFECTIVE, source, False),
            ("positive_control", ArtifactRole.POSITIVE_CONTROL, control, True),
        ):
            request = _request(
                kind=kind,
                oracle_or_predicate=oracle_or_predicate,
                ledger_id=ledger_id,
                candidate=candidate,
                proposal_sha256=proposal_sha256,
                relation=p_row["accepted_relation"],
                role=role,
                artifact=artifact,
                repo_root=repo_root,
                expected=expected,
                created_at=created_at,
            )
            request_path = issue_root / role_name / "request.json"
            write_json(request_path, request.model_dump(mode="json"))
            role_rows.append({
                "role": role.value,
                "artifact_path": artifact.relative_to(repo_root).as_posix(),
                "artifact_sha256": sha256_path(artifact),
                "request_path": request_path.relative_to(gold_root).as_posix(),
                "request_file_sha256": sha256_path(request_path),
                "request_payload_sha256": request.request_sha256,
                "runner_kind": kind,
            })
        manifest_rows.append({
            "ledger_id": ledger_id,
            "proposal_path": (issue_root / "proposal.json").relative_to(gold_root).as_posix(),
            "proposal_file_sha256": sha256_path(issue_root / "proposal.json"),
            "proposal_payload_sha256": proposal_sha256,
            "control_path": control.relative_to(gold_root).as_posix(),
            "control_sha256": sha256_path(control),
            "roles": role_rows,
        })
    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request-manifest.v1",
        "batch_id": "batch_05a",
        "track_c_preflight_batch_sha256": preflight["batch_sha256"],
        "rows": manifest_rows,
        "created_at": created_at,
        "no_execution_performed_by_builder": True,
    }
    output = gold_root / "receipts/batch_05a_request_manifest.json"
    write_json(output, {**unsigned, "manifest_sha256": canonical_sha256(unsigned)})
    print(f"wrote {output} ({len(manifest_rows)} controls and request pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
