"""Build batch-03a controls, corrected proposals, and pre-result requests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import ExactnessRelation, TypedInput, canonical_sha256, sha256_path, write_json
from paper_stm_evaluation.predicate_gold_composite import CompositeExecutionRequest
from paper_stm_evaluation.predicate_gold_execution import ArtifactRole, PredicateExecutionRequest, RelationScope
from paper_stm_evaluation.predicate_gold_native_contract import ArtifactRole as ContractRole
from paper_stm_evaluation.predicate_gold_native_contract import NativeContractId, NativeContractRequest
from paper_stm_evaluation.predicate_gold_oracle import ArtifactRole as NativeRole
from paper_stm_evaluation.predicate_gold_oracle import NativeOracleRequest
from paper_stm_evaluation.predicate_gold_relation_oracle import ArtifactRole as RelationRole
from paper_stm_evaluation.predicate_gold_relation_oracle import RelationOracleId, RelationOracleRequest
from paper_stm_evaluation.predicate_gold_review import TrackBProposalBatch


EXECUTION_PLANS = {
    "INS-0011-02": "CONTRACT_DEAD_CARRIER",
    "VU-0011-01": "RELATION_REQUIRED_SIGNATURE",
    "EIS-0012-01": "CONTRACT_EVENTLESS_ABSENT",
    "INS-0012-01": "CONTRACT_REQUIRED_CARRIER",
    "EIS-0014-01": "NATIVE_INITIAL",
    "EIS-0014-02": "S4",
    "EIS-0014-03": "S4",
    "EIS-0014-04": "CONTRACT_OUTPUT",
    "VU-0014-01": "CONTRACT_OUTPUT",
    "DIFF-0016-05": "COMPOSITE",
    "EIS-0016-01": "RELATION_DIRECT_CHILD",
    "INS-0017-01": "COMPOSITE",
}


def _source(paper_root: Path, pair_id: str) -> Path:
    return paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"


def _replace(text: str, before: str, after: str, ledger_id: str) -> tuple[str, dict[str, Any]]:
    count = text.count(before)
    if count != 1:
        raise ValueError(f"{ledger_id} expected one exact control match, got {count}")
    return text.replace(before, after, 1), {
        "before": before,
        "after": after,
        "before_sha256": canonical_sha256(before),
        "after_sha256": canonical_sha256(after),
        "match_count": count,
    }


def _control_text(ledger_id: str, source_text: str) -> tuple[str, list[dict[str, Any]], str]:
    changes: list[dict[str, Any]] = []
    def edit(before: str, after: str) -> None:
        nonlocal source_text
        source_text, change = _replace(source_text, before, after, ledger_id)
        changes.append(change)

    if ledger_id == "INS-0011-02":
        edit('    state ClampingLoseState named "ClampingLoseState\\n[PlantUML body] Clamping Lose State";\n', "")
        edit("    OperationalState -> ClampingLoseState : /Transition_to_Clamping_Lose_State;\n", "")
        intent = "Delete the NL-silent ClampingLoseState and its sole incoming carrier, one ledger-authorized repair branch; no recovery event or target is invented."
    elif ledger_id == "VU-0011-01":
        edit("    BrakingState -> InitialState : /Signal_Feedback_Sent;\n", "    BrakingState -> InitialState : /Signal_Feedback_Sent;\n    ClampingState -> InitialState : /Signal_Feedback_Sent;\n")
        intent = "Add the exact author-specified feedback reset from ClampingState to InitialState."
    elif ledger_id in {"EIS-0012-01", "INS-0012-01"}:
        edit("    Off -> Terminate;\n", "    Off -> [*];\n")
        intent = "Replace the erroneous ordinary Terminate target with the native root exit boundary while preserving the submitted Off branch."
    elif ledger_id == "EIS-0014-01":
        edit("    InMotion -> EmergencyStopping : if [R45RouteToken == 7] effect { R45RouteToken = 0; };\n    [*] -> UnspecifiedInitial;", "    InMotion -> EmergencyStopping : if [R45RouteToken == 7] effect { R45RouteToken = 0; };\n    [*] -> DoorsClosing;")
        intent = "Retarget only the root initial carrier to the exact author-required DoorsClosing state."
    elif ledger_id == "EIS-0014-02":
        edit('        state Accelerating named "Accelerating";\n', '        state Accelerating named "Accelerating" {\n            enter abstract Accelerate;\n        }\n')
        intent = "Attach the exact Accelerate token to the exact Accelerating entry lifecycle slot."
    elif ledger_id == "EIS-0014-03":
        edit('    state EmergencyStopping named "EmergencyStopping\\n[PlantUML body] Obstacle Detected" {\n', '    state EmergencyStopping named "EmergencyStopping\\n[PlantUML body] Obstacle Detected" {\n        enter abstract Emergency_Stop;\n')
        intent = "Attach the exact Emergency Stop action to EmergencyStopping entry; the accidental child remains so the control tests only the selected property."
    elif ledger_id == "EIS-0014-04":
        edit('        state Approaching named "Approaching\\n[PlantUML body] Nearing Destination\\n[PlantUML body] Ready to Stop/Decelerate";\n', '        state Approaching named "Approaching\\n[PlantUML body] Nearing Destination\\n[PlantUML body] Ready to Stop/Decelerate" {\n            enter abstract Send;\n        }\n')
        intent = "Add the exact author output token Send in one admitted lifecycle slot without inventing delivery or repetition semantics."
    elif ledger_id == "VU-0014-01":
        edit('    state EmergencyStopping named "EmergencyStopping\\n[PlantUML body] Obstacle Detected" {\n', '    state EmergencyStopping named "EmergencyStopping\\n[PlantUML body] Obstacle Detected" {\n        enter abstract Obstacle_Detected;\n')
        intent = "Add a distinct output-role action with the exact Obstacle Detected token; the same-named input event remains separate."
    elif ledger_id == "DIFF-0016-05":
        edit("    [*] -> SearchMission : /Start_Mission;\n", "    [*] -> SearchMission;\n")
        intent = "Remove only the event attachment from the root initial carrier; target and guard absence remain unchanged."
    elif ledger_id == "EIS-0016-01":
        source_text = '''state llms_emp_feedback_final_0016 named "llms_emp_feedback_final_0016" {
    state SearchMission named "SearchMission" {
        state Region1 named "Region1";
        state Region2 named "Region2";
        state Region3 named "Region3";
        [*] -> Region1;
    }
    [*] -> SearchMission;
}
'''
        changes.append({"replacement_kind": "SOURCE_BACKED_PROPERTY_MINIMAL_CONTROL", "required_direct_children": ["Region1", "Region2", "Region3"]})
        intent = "Retain only the exact SearchMission/Region1/Region2/Region3 hierarchy required by this issue; no concurrency or behavioral claim is tested."
    elif ledger_id == "INS-0017-01":
        for target in ("F", "R", "P"):
            edit(f"        [*] -> {target} : /collision_detected;\n", f"        [*] -> {target};\n")
        intent = "Remove only collision_detected from all three region-local initial carriers while preserving line order, targets and absent guards."
    else:
        raise KeyError(ledger_id)
    return source_text, changes, intent


def _write_controls(repo_root: Path, paper_root: Path, gold_root: Path, created_at: str) -> dict[str, Path]:
    from pyfcstm.model import load_state_machine_from_text

    controls: dict[str, Path] = {}
    for ledger_id in sorted(EXECUTION_PLANS):
        pair_id = ledger_id.split("-")[1]
        source = _source(paper_root, pair_id)
        text, changes, intent = _control_text(ledger_id, source.read_text(encoding="utf-8"))
        load_state_machine_from_text(text)
        root = gold_root / "controls" / ledger_id
        path = root / "independent_positive_control.fcstm"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        unsigned = {
            "schema_version": "paper1.predicate-gold.positive-control-provenance.v1",
            "ledger_id": ledger_id,
            "control_kind": "SOURCE_BACKED_INDEPENDENT_MINIMAL_CONTROL",
            "source_artifact_path": source.relative_to(repo_root).as_posix(),
            "source_artifact_sha256": sha256_path(source),
            "control_path": path.relative_to(repo_root).as_posix(),
            "control_sha256": sha256_path(path),
            "repair_intent": intent,
            "exact_changes": changes,
            "pyfcstm_parse_status": "PASS",
            "constructed_before_execution": True,
            "execution_results_visible": False,
            "v60_actual_visible": False,
            "created_at": created_at,
        }
        write_json(root / "control_provenance.json", {**unsigned, "provenance_sha256": canonical_sha256(unsigned)})
        controls[ledger_id] = path
    return controls


def _candidate(row: Any, candidate_id: str) -> Any:
    values = [item for item in row.candidate_properties if item.candidate_id == candidate_id]
    if len(values) != 1:
        raise ValueError(f"candidate {candidate_id} did not resolve uniquely")
    return values[0]


def _derived_input(template: TypedInput, name: str, value: Any, *, stable_id: str | None = None, reason: str | None = None) -> TypedInput:
    json_type = "null" if value is None else "boolean" if isinstance(value, bool) else "array" if isinstance(value, list) else "object" if isinstance(value, dict) else "string"
    return TypedInput(
        field_name=name,
        json_type=json_type,
        value=value,
        normalized_value=value,
        provenance_kind=template.provenance_kind,
        source_ref=template.source_ref,
        stable_object_id=stable_id,
        alias_resolution=template.alias_resolution,
        reason=reason or f"Track C projects the exact {name} field from the hash-bound Track B source binding.",
    )


def _predicate_fields(candidate: Any, predicate_id: str) -> tuple[TypedInput, ...]:
    wrapper = candidate.typed_inputs[0]
    payload = wrapper.value
    if not isinstance(payload, dict):
        raise TypeError("single predicate candidate must contain one typed object")
    names = {"S2": ("source", "target", "scope", "transition"), "S4": ("state", "phase", "action")}[predicate_id]
    result = []
    for name in names:
        value = payload.get(name)
        if candidate.candidate_id == "eis0014-03-s4-entry-only" and name == "action":
            result.append(TypedInput(
                field_name="action",
                json_type="string",
                value="Emergency Stop",
                normalized_value="Emergency_Stop",
                provenance_kind=wrapper.provenance_kind,
                source_ref=wrapper.source_ref,
                stable_object_id="llms_emp_feedback_final_0014.EmergencyStopping.Emergency_Stop",
                alias_resolution="Author display token 'Emergency Stop' maps to the legal pyfcstm native action identity Emergency_Stop; no fuzzy selection is used.",
                reason="Preserves the author action while binding the exact native identifier required by the frozen S4 backend.",
            ))
        else:
            result.append(_derived_input(wrapper, name, value, stable_id=wrapper.stable_object_id if name in {"state", "transition"} else None))
    return tuple(result)


def _predicate_request(candidate: Any, *, ledger_id: str, proposal_sha: str, relation: ExactnessRelation, role: ArtifactRole, artifact: Path, repo_root: Path, created_at: str, predicate_id: str, relation_scope: RelationScope = RelationScope.THIS_PROPERTY, property_id: str | None = None, inputs: tuple[TypedInput, ...] | None = None, expected: bool | None = None) -> PredicateExecutionRequest:
    request_inputs = inputs or _predicate_fields(candidate, predicate_id)
    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        "request_id": f"{ledger_id.lower()}-{role.value.lower()}-{predicate_id.lower()}-{canonical_sha256([item.model_dump(mode='json') for item in request_inputs])[7:15]}",
        "ledger_id": ledger_id,
        "property_id": property_id or candidate.candidate_id,
        "property_proposal_sha256": proposal_sha,
        "exactness_relation": relation,
        "relation_scope": relation_scope,
        "predicate_id": predicate_id,
        "artifact_role": role,
        "artifact_path": artifact.relative_to(repo_root).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in request_inputs],
        "assumptions": [*candidate.assumptions, "Execution cannot alter the pre-reviewed O/P relation."],
        "expected_boolean_for_acceptance": (role == ArtifactRole.POSITIVE_CONTROL) if expected is None else expected,
        "created_at": created_at,
    }
    return PredicateExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))


def _request_for(*, plan: str, ledger_id: str, candidate: Any, proposal_sha: str, relation: ExactnessRelation, role_name: str, artifact: Path, repo_root: Path, created_at: str) -> Any:
    is_control = role_name == "positive_control"
    if plan.startswith("CONTRACT_"):
        role = ContractRole.POSITIVE_CONTROL if is_control else ContractRole.DEFECTIVE
        template = candidate.typed_inputs[0]
        if plan == "CONTRACT_DEAD_CARRIER":
            values = {item.field_name: item.value for item in candidate.typed_inputs}
            inputs = tuple(_derived_input(item, item.field_name, item.value, stable_id=item.stable_object_id) for item in candidate.typed_inputs)
            contract = NativeContractId.UNREACHABLE_OR_OUTGOING_CARRIER
        elif plan in {"CONTRACT_EVENTLESS_ABSENT", "CONTRACT_REQUIRED_CARRIER"}:
            values = {item.field_name: item.value for item in candidate.typed_inputs}
            if plan == "CONTRACT_REQUIRED_CARRIER":
                payload = template.value
                if not isinstance(payload, dict):
                    raise TypeError("required-carrier candidate lacks typed S2 payload")
                owner = payload["scope"]
                source = f"{owner}.{payload['source']}"
                target = payload["target"]
            else:
                owner = str(values["source_state"]).rsplit(".", 1)[0]
                source = values["source_state"]
                target = values["forbidden_target"]
            inputs = (
                _derived_input(template, "owner", owner),
                _derived_input(template, "source", source, stable_id=str(source)),
                _derived_input(template, "target", target, stable_id="pyfcstm.dsl.EXIT_STATE" if target == "[*]" else str(target)),
            )
            contract = NativeContractId.FORBIDDEN_EVENTLESS_CARRIER_ABSENT if plan == "CONTRACT_EVENTLESS_ABSENT" else NativeContractId.REQUIRED_CARRIER_PRESENT
        else:
            values = {item.field_name: item.value for item in candidate.typed_inputs}
            inputs = (
                _derived_input(template, "owner_state", values["owner_state"], stable_id=str(values["owner_state"])),
                _derived_input(template, "required_output_token", values["required_output_token"]),
            )
            contract = NativeContractId.OUTPUT_ACTION_CARRIER_PRESENT
        unsigned = {
            "schema_version": "paper1.predicate-gold.native-contract-request.v1",
            "request_id": f"{ledger_id.lower()}-{role.value.lower()}-{contract.value.lower()}",
            "ledger_id": ledger_id,
            "property_id": candidate.candidate_id,
            "property_proposal_sha256": proposal_sha,
            "exactness_relation": relation,
            "contract_id": contract,
            "artifact_role": role,
            "artifact_path": artifact.relative_to(repo_root).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "typed_inputs": [item.model_dump(mode="json") for item in inputs],
            "assumptions": [*candidate.assumptions, "Execution uses public pyfcstm native objects and cannot strengthen the pre-reviewed relation."],
            "expected_boolean_for_acceptance": is_control,
            "created_at": created_at,
        }
        return NativeContractRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    if plan == "RELATION_REQUIRED_SIGNATURE":
        role = RelationRole.POSITIVE_CONTROL if is_control else RelationRole.DEFECTIVE
        values = {item.field_name: item.value for item in candidate.typed_inputs}
        template = candidate.typed_inputs[0]
        signature = {"owner": str(values["source_state"]).rsplit(".", 1)[0], "source": values["source_state"], "event": values["event_path"], "target": values["target_state"]}
        inputs = (_derived_input(template, "required_signature", signature),)
        oracle = RelationOracleId.REQUIRED_SIGNATURE_PRESENT
    elif plan == "RELATION_DIRECT_CHILD":
        role = RelationRole.POSITIVE_CONTROL if is_control else RelationRole.DEFECTIVE
        template = candidate.typed_inputs[0]
        parent = candidate.typed_inputs[1].value
        children = [str(path).rsplit(".", 1)[-1] for path in template.value]
        inputs = (_derived_input(template, "expected_hierarchy", {"parent": parent, "direct_children": children}),)
        oracle = RelationOracleId.DIRECT_CHILD_HIERARCHY
    else:
        role = None
    if role is not None:
        unsigned = {
            "schema_version": "paper1.predicate-gold.relation-oracle-request.v1",
            "request_id": f"{ledger_id.lower()}-{role.value.lower()}-{oracle.value.lower()}",
            "ledger_id": ledger_id,
            "property_id": candidate.candidate_id,
            "property_proposal_sha256": proposal_sha,
            "exactness_relation": relation,
            "oracle_id": oracle,
            "artifact_role": role,
            "artifact_path": artifact.relative_to(repo_root).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "typed_inputs": [item.model_dump(mode="json") for item in inputs],
            "assumptions": [*candidate.assumptions, "Native relation execution cannot strengthen the pre-reviewed O/P relation."],
            "expected_boolean_for_acceptance": is_control,
            "created_at": created_at,
        }
        return RelationOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    if plan == "NATIVE_INITIAL":
        role = NativeRole.POSITIVE_CONTROL if is_control else NativeRole.DEFECTIVE
        template = candidate.typed_inputs[0]
        inputs = (
            _derived_input(template, "owner_path", ["llms_emp_feedback_final_0014"]),
            _derived_input(template, "cardinality", "EXACTLY_ONE"),
            _derived_input(template, "required_target_path", ["llms_emp_feedback_final_0014", "DoorsClosing"]),
            _derived_input(template, "require_no_event", True),
            _derived_input(template, "require_no_guard", True),
        )
        unsigned = {
            "schema_version": "paper1.predicate-gold.native-oracle-request.v1",
            "request_id": f"{ledger_id.lower()}-{role.value.lower()}-native-initial",
            "ledger_id": ledger_id,
            "property_id": candidate.candidate_id,
            "property_proposal_sha256": proposal_sha,
            "exactness_relation": relation,
            "oracle_id": "NATIVE_INITIAL_TRANSITION_CONTRACT",
            "artifact_role": role,
            "artifact_path": artifact.relative_to(repo_root).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "typed_inputs": [item.model_dump(mode="json") for item in inputs],
            "assumptions": ["Complete root init_transitions inventory is inspected without runtime claims."],
            "expected_boolean_for_acceptance": is_control,
            "created_at": created_at,
        }
        return NativeOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    if plan in {"S2", "S4"}:
        role = ArtifactRole.POSITIVE_CONTROL if is_control else ArtifactRole.DEFECTIVE
        return _predicate_request(candidate, ledger_id=ledger_id, proposal_sha=proposal_sha, relation=relation, role=role, artifact=artifact, repo_root=repo_root, created_at=created_at, predicate_id=plan)
    if plan == "COMPOSITE":
        role = ArtifactRole.POSITIVE_CONTROL if is_control else ArtifactRole.DEFECTIVE
        wrapper = candidate.typed_inputs[0]
        child_requests = []
        for index, payload in enumerate(wrapper.value):
            predicate_id = payload["predicate_id"]
            names = ("transition", "triggers") if predicate_id == "S3" else ("transition", "guard")
            inputs = tuple(_derived_input(wrapper, name, payload[name], stable_id=payload["transition"] if name == "transition" else None) for name in names)
            child_requests.append(_predicate_request(candidate, ledger_id=ledger_id, proposal_sha=proposal_sha, relation=relation, role=role, artifact=artifact, repo_root=repo_root, created_at=created_at, predicate_id=predicate_id, relation_scope=RelationScope.PARENT_COMPOSITE, property_id=candidate.candidate_id, inputs=inputs, expected=True))
        unsigned = {
            "schema_version": "paper1.predicate-gold.composite-request.v1",
            "request_id": f"{ledger_id.lower()}-{role.value.lower()}-and",
            "ledger_id": ledger_id,
            "property_id": candidate.candidate_id,
            "property_proposal_sha256": proposal_sha,
            "exactness_relation": relation,
            "operator": "AND",
            "no_short_circuit": True,
            "artifact_role": role,
            "artifact_path": artifact.relative_to(repo_root).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "constituents": [item.model_dump(mode="json") for item in child_requests],
            "assumptions": ["Every finite S3/S5 constituent executes without short-circuiting."],
            "expected_boolean_for_acceptance": is_control,
            "created_at": created_at,
        }
        return CompositeExecutionRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    raise KeyError(plan)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    preflight_path = gold_root / "review/track_c_preflight/batch_03a.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    preflight_rows = {row["ledger_id"]: row for row in preflight["rows"]}
    executable = {key for key, value in preflight_rows.items() if value["execution_required"]}
    if executable != set(EXECUTION_PLANS):
        raise ValueError("preflight execution set differs from builder plans")
    b_path = gold_root / "review/track_b_independent/batch_03a.json"
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    controls = _write_controls(repo_root, paper_root, gold_root, args.created_at)
    manifest_rows = []
    for ledger_id in sorted(EXECUTION_PLANS):
        p_row = preflight_rows[ledger_id]
        b_row = b_rows[ledger_id]
        candidate = _candidate(b_row, p_row["selected_candidate_id"])
        selected = candidate.model_dump(mode="json")
        selected["selected"] = True
        selected["exactness_relation"] = p_row["accepted_relation"]
        selected["reason"] = p_row["implication_analysis"]["reason"] + " This relation was frozen before same-issue execution."
        if ledger_id == "INS-0011-02":
            selected["property_expression"] = "ClampingLoseState is absent/unreachable, or if reachable it has at least one authored outgoing carrier."
        elif ledger_id == "INS-0012-01":
            selected["mode"] = "EVALUATION_ONLY_ORACLE"
            selected["predicate_ids"] = []
            selected["semantic_gaps"] = [
                "The frozen S2 implementation rejects native [*] as outside its executable fragment; the isolated native carrier contract preserves the same direct-edge semantics."
            ]
        elif ledger_id == "EIS-0014-03":
            payload = selected["typed_inputs"][0]["value"]
            payload["action"] = "Emergency_Stop"
            selected["typed_inputs"][0]["normalized_value"]["action"] = "Emergency_Stop"
            selected["typed_inputs"][0]["alias_resolution"] = "Author display token 'Emergency Stop' is bound to exact native identifier Emergency_Stop."
        unsigned_proposal = {
            "schema_version": "paper1.predicate-gold.corrected-execution-proposal.v1",
            "ledger_id": ledger_id,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "track_c_preflight_row_sha256": p_row["audit_sha256"],
            "normalized_obligation_sha256": p_row["normalized_obligation_sha256"],
            "selected_candidate": selected,
            "final_pre_execution_relation": p_row["accepted_relation"],
            "execution_required": True,
            "v60_actual_visible": False,
            "same_issue_execution_result_visible": False,
            "created_at": args.created_at,
        }
        proposal = {**unsigned_proposal, "proposal_sha256": canonical_sha256(unsigned_proposal)}
        issue_root = gold_root / "receipts" / ledger_id
        write_json(issue_root / "proposal.json", proposal)
        roles = []
        for role_name, artifact in (("defective", _source(paper_root, ledger_id.split("-")[1])), ("positive_control", controls[ledger_id])):
            request = _request_for(plan=EXECUTION_PLANS[ledger_id], ledger_id=ledger_id, candidate=candidate, proposal_sha=proposal["proposal_sha256"], relation=ExactnessRelation(p_row["accepted_relation"]), role_name=role_name, artifact=artifact, repo_root=repo_root, created_at=args.created_at)
            request_path = issue_root / role_name / "request.json"
            write_json(request_path, request.model_dump(mode="json"))
            roles.append({"role": role_name, "request_path": request_path.relative_to(gold_root).as_posix(), "request_sha256": request.request_sha256, "request_kind": EXECUTION_PLANS[ledger_id]})
        manifest_rows.append({"ledger_id": ledger_id, "proposal_path": (issue_root / "proposal.json").relative_to(gold_root).as_posix(), "proposal_sha256": proposal["proposal_sha256"], "roles": roles})
    unsigned_manifest = {
        "schema_version": "paper1.predicate-gold.batch-execution-request-manifest.v1",
        "batch_id": "batch_03a",
        "track_c_preflight_path": preflight_path.relative_to(gold_root).as_posix(),
        "track_c_preflight_sha256": sha256_path(preflight_path),
        "rows": manifest_rows,
        "created_at": args.created_at,
        "v60_actual_visible": False,
        "execution_results_visible": False,
    }
    output = gold_root / "review/track_c_preflight/batch_03a_execution_manifest.json"
    write_json(output, {**unsigned_manifest, "manifest_sha256": canonical_sha256(unsigned_manifest)})
    print(f"wrote {output} ({len(manifest_rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
