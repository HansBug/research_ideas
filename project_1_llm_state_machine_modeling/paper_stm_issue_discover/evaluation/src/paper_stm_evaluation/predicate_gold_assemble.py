"""Assemble the canonical predicate-gold overlay from active reviewed evidence.

The assembler is deliberately mechanical.  It accepts only hash-selected A/B/C
reviews, pane5 arbitration, and repository-resident execution evidence.  It does
not choose a predicate, reinterpret an obligation, or execute the method/Judge.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    CandidateProperty,
    Confidence,
    ExecutableProperty,
    ExecutionRecord,
    ExecutionState,
    GoldMode,
    GoldStatus,
    PositiveControl,
    PositiveControlStatus,
    PredicateGoldAnnotation,
    PredicateGoldDataset,
    PropertyComposition,
    ReviewOpinion,
    ReviewTrack,
    SourceRef,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_release import ActiveReviewManifest
from paper_stm_evaluation.predicate_gold_review import (
    HighRiskReviewBatch,
    HighRiskReviewRow,
    Pane5ArbitrationBatch,
    PreExecutionDisposition,
    TrackAProposalBatch,
    TrackAProposalRow,
    TrackBProposalBatch,
    TrackBProposalRow,
    TrackCReviewBatch,
    TrackCReviewRow,
)


def _ref(
    repo_root: Path,
    path: Path,
    *,
    pointer: str | None = None,
    element: str | None = None,
) -> SourceRef:
    """Build one stable repository source reference."""

    return SourceRef(
        repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        line_start=None,
        line_end=None,
        model_element=element,
        excerpt=None,
    )


def _load_rows(
    review_root: Path,
    selected: tuple[Any, ...],
    model: type[Any],
) -> tuple[dict[str, Any], dict[str, str]]:
    """Load unique rows and the reviewer identity from selected batch files."""

    rows: dict[str, Any] = {}
    reviewers: dict[str, str] = {}
    for entry in selected:
        path = review_root / entry.repository_path
        if sha256_path(path) != entry.sha256:
            raise ValueError(f"active review changed after selection: {entry.repository_path}")
        batch = model.model_validate_json(path.read_text(encoding="utf-8"))
        reviewer_id = getattr(batch, "reviewer_id", "pane5:manual-supervised-adjudicator")
        for row in batch.rows:
            if row.ledger_id in rows:
                raise ValueError(f"duplicate active review row: {row.ledger_id}")
            rows[row.ledger_id] = row
            reviewers[row.ledger_id] = reviewer_id
    return rows, reviewers


def _b_status(disposition: PreExecutionDisposition) -> GoldStatus:
    """Map a pre-execution conditional disposition to its status name."""

    return {
        PreExecutionDisposition.EXACT_EXECUTION_CANDIDATE: GoldStatus.EXACT_FALSE,
        PreExecutionDisposition.COMPOSITE_EXACT_EXECUTION_CANDIDATE: GoldStatus.COMPOSITE_EXACT_FALSE,
        PreExecutionDisposition.PROXY_EXECUTION_CANDIDATE: GoldStatus.SOUND_FALSE_PROXY,
        PreExecutionDisposition.UNSUPPORTED_EXACT_CANDIDATE: GoldStatus.UNSUPPORTED_EXACT,
    }[disposition]


def _opinion_a(reviewer_id: str, batch_input_hash: str, row: TrackAProposalRow) -> ReviewOpinion:
    """Project one blind Track A row into canonical review evidence."""

    unsigned = {
        "opinion_id": f"{reviewer_id}:{row.ledger_id}",
        "reviewer_id": reviewer_id,
        "track": ReviewTrack.A_OBLIGATION,
        "input_sha256": canonical_sha256(
            {"batch_input": batch_input_hash, "proposal": row.proposal_sha256}
        ),
        "normalized_obligation_sha256": canonical_sha256(
            row.normalized_obligation.model_dump(mode="json")
        ),
        "property_proposal_sha256": None,
        "proposed_status": None,
        "proposed_exactness_relation": None,
        "proposed_predicate_ids": [],
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": False,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _opinion_b(reviewer_id: str, row: TrackBProposalRow) -> ReviewOpinion:
    """Project one blind Track B row into canonical review evidence."""

    selected = next(
        (item for item in row.candidate_properties if item.candidate_id == row.selected_candidate_id),
        None,
    )
    unsigned = {
        "opinion_id": f"{reviewer_id}:{row.ledger_id}",
        "reviewer_id": reviewer_id,
        "track": ReviewTrack.B_PROPERTY,
        "input_sha256": canonical_sha256(
            {"packet": row.packet_sha256, "proposal": row.proposal_sha256}
        ),
        "normalized_obligation_sha256": canonical_sha256(
            row.normalized_obligation.model_dump(mode="json")
        ),
        "property_proposal_sha256": row.proposal_sha256,
        "proposed_status": _b_status(row.proposed_disposition),
        "proposed_exactness_relation": row.proposed_exactness_relation,
        "proposed_predicate_ids": list(selected.predicate_ids) if selected else [],
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": False,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _opinion_c(reviewer_id: str, row: TrackCReviewRow) -> ReviewOpinion:
    """Project one post-execution Track C row into canonical review evidence."""

    unsigned = {
        "opinion_id": f"{reviewer_id}:{row.ledger_id}",
        "reviewer_id": reviewer_id,
        "track": ReviewTrack.C_EXECUTION,
        "input_sha256": row.input_packet_sha256,
        "normalized_obligation_sha256": row.normalized_obligation_sha256,
        "property_proposal_sha256": row.property_proposal_sha256,
        "proposed_status": row.proposed_status,
        "proposed_exactness_relation": row.proposed_exactness_relation,
        "proposed_predicate_ids": [],
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": True,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _opinion_high_risk(
    reviewer_id: str, row: HighRiskReviewRow
) -> ReviewOpinion:
    """Project one independent fourth-review row into canonical evidence."""

    unsigned = {
        "opinion_id": f"{reviewer_id}:{row.ledger_id}",
        "reviewer_id": reviewer_id,
        "track": ReviewTrack.EXTRA_HIGH_RISK,
        "input_sha256": row.input_sha256,
        "normalized_obligation_sha256": row.normalized_obligation_sha256,
        "property_proposal_sha256": row.property_proposal_sha256,
        "proposed_status": row.proposed_status,
        "proposed_exactness_relation": row.proposed_exactness_relation,
        "proposed_predicate_ids": list(row.proposed_predicate_ids),
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": True,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _project_candidates(
    row: TrackBProposalRow,
    *,
    repo_root: Path,
    final_status: GoldStatus,
    final_relation: Any,
    selected_candidate_id: str | None = None,
    sealed_selected_candidate: dict[str, Any] | None = None,
) -> tuple[CandidateProperty, ...]:
    """Retain all candidates while applying the final decision to selected P."""

    executable = final_status in {
        GoldStatus.EXACT_FALSE,
        GoldStatus.COMPOSITE_EXACT_FALSE,
        GoldStatus.SOUND_FALSE_PROXY,
    }
    selected_id = selected_candidate_id or row.selected_candidate_id
    projected: list[CandidateProperty] = []
    for candidate in row.candidate_properties:
        payload = candidate.model_dump(mode="json")
        if candidate.candidate_id == selected_id:
            if sealed_selected_candidate is not None:
                for field_name in CandidateProperty.model_fields:
                    if field_name in {"candidate_id", "selected"}:
                        continue
                    if field_name in sealed_selected_candidate:
                        payload[field_name] = sealed_selected_candidate[field_name]
            payload["selected"] = executable
            payload["exactness_relation"] = final_relation.value
            if final_status == GoldStatus.COMPOSITE_EXACT_FALSE:
                payload["mode"] = GoldMode.COMPOSITE.value
            if candidate.exactness_relation != final_relation:
                payload["semantic_gaps"] = [
                    *payload["semantic_gaps"],
                    "Pane5 arbitration corrected the pre-execution implication direction after independent source/execution review.",
                ]
                payload["reason"] = (
                    f"{candidate.reason} Final arbitration set the relation to {final_relation.value}; "
                    "the persisted Track C evidence gives the issue-specific boundary."
                )
        code_ref_migrations: list[str] = []
        for source_ref in payload["source_refs"]:
            repository_path = source_ref["repository_path"]
            if "/evaluation/src/paper_stm_evaluation/predicate_gold_" not in repository_path:
                continue
            current_path = repo_root / repository_path
            if not current_path.is_file():
                continue
            current_sha256 = sha256_path(current_path)
            if source_ref["sha256"] != current_sha256:
                code_ref_migrations.append(
                    f"{repository_path}: {source_ref['sha256']} -> {current_sha256}"
                )
                source_ref["sha256"] = current_sha256
        if code_ref_migrations:
            migration_note = (
                "Canonical projection refreshed an evaluation-code locator after the "
                "reviewed oracle was extended: "
                + "; ".join(code_ref_migrations)
                + ". The immutable Track B row retains its historical hash; this locator "
                "refresh does not upgrade the O/P relation."
            )
            payload["reason"] = f"{payload['reason']} {migration_note}"
            payload["basis"] = f"{payload['basis']} {migration_note}"
        projected.append(CandidateProperty.model_validate(payload))
    return tuple(projected)


def _sealed_execution_selection(
    *,
    gold_root: Path,
    ledger_id: str,
    b_row: TrackBProposalRow,
    c_row: TrackCReviewRow,
    final_status: GoldStatus,
) -> tuple[str | None, dict[str, Any] | None]:
    """Recover a post-Track-B selection only from hash-closed execution evidence."""

    executable = final_status in {
        GoldStatus.EXACT_FALSE,
        GoldStatus.COMPOSITE_EXACT_FALSE,
        GoldStatus.SOUND_FALSE_PROXY,
    }
    if not executable or b_row.selected_candidate_id is not None:
        return b_row.selected_candidate_id, None

    receipt_root = gold_root / "receipts" / ledger_id
    proposal_path = receipt_root / "proposal.json"
    request_path = receipt_root / "defective" / "request.json"
    receipt_path = receipt_root / "defective" / "receipt.json"
    replay_path = receipt_root / "defective" / "replay" / "replay_audit.json"
    for path in (proposal_path, request_path, receipt_path, replay_path):
        if not path.is_file():
            raise ValueError(
                f"{ledger_id} executable selection lacks sealed evidence: {path}"
            )

    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    request = json.loads(request_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    proposal_sha256 = proposal.get("proposal_sha256")
    if proposal_sha256 != c_row.property_proposal_sha256:
        raise ValueError(f"{ledger_id} sealed proposal does not bind active Track C")
    selected = proposal.get("selected_candidate")
    if not isinstance(selected, dict) or not selected.get("candidate_id"):
        raise ValueError(f"{ledger_id} sealed proposal has no selected candidate")
    selected_id = selected["candidate_id"]
    candidate_ids = {item.candidate_id for item in b_row.candidate_properties}
    if selected_id not in candidate_ids:
        raise ValueError(
            f"{ledger_id} sealed selection is absent from persisted Track B candidates"
        )
    if request.get("property_proposal_sha256") != proposal_sha256:
        raise ValueError(f"{ledger_id} defective request does not bind sealed proposal")
    if request.get("property_id") != selected_id:
        raise ValueError(f"{ledger_id} defective request selected a different property")
    if receipt.get("request_sha256") != request.get("request_sha256"):
        raise ValueError(f"{ledger_id} defective receipt does not bind saved request")
    if replay.get("overall_match") is not True:
        raise ValueError(f"{ledger_id} sealed-selection replay does not match")
    return selected_id, selected


def _code_hash(receipt: dict[str, Any]) -> str:
    """Select the code-byte hash for the runner/oracle that produced a receipt."""

    hashes = receipt["code_hashes"]
    if isinstance(hashes, list):
        priorities = ("composite_runner", "predicate_backend", "evaluation_oracle")
        for role in priorities:
            for item in hashes:
                if item["role"] == role:
                    return item["sha256"]
        return hashes[0]["sha256"]
    candidates = [
        (path, digest)
        for path, digest in hashes.items()
        if "predicate_gold_" in path and path.endswith(".py")
    ]
    if not candidates:
        candidates = sorted(hashes.items())
    return min(candidates)[1]


def _receipt_refs(
    repo_root: Path,
    receipt_root: Path,
    receipt: dict[str, Any],
) -> tuple[SourceRef, ...]:
    """Reference the parent receipt, replay audit and every child receipt."""

    refs = [
        _ref(repo_root, receipt_root / "receipt.json", element="completed receipt"),
        _ref(
            repo_root,
            receipt_root / "replay" / "replay_audit.json",
            element="provider-free replay audit",
        ),
    ]
    raw = receipt_root / "raw_receipt.json"
    if raw.is_file():
        refs.append(_ref(repo_root, raw, element="raw backend receipt"))
    for constituent in receipt.get("constituents") or []:
        child = constituent.get("receipt_path")
        if child:
            refs.append(
                _ref(
                    repo_root,
                    receipt_root / child,
                    element=constituent.get("request_id") or constituent.get("constituent_id"),
                )
            )
    return tuple(refs)


def _counterexample_refs(
    repo_root: Path,
    receipt_root: Path,
    receipt: dict[str, Any],
) -> tuple[SourceRef, ...]:
    """Expose the persisted false observation without calling it a proof of O/P equivalence."""

    raw = receipt_root / "raw_receipt.json"
    if raw.is_file():
        return (
            _ref(
                repo_root,
                raw,
                pointer=receipt.get("counterexample_json_pointer") or "/counterexample",
                element="defective false observation",
            ),
        )
    if receipt.get("constituents") is not None:
        return (
            _ref(
                repo_root,
                receipt_root / "receipt.json",
                pointer="/constituents",
                element="constituent truth table",
            ),
        )
    return ()


def _input_value(request: dict[str, Any], name: str) -> Any:
    """Return one named typed input value when the query declares it."""

    for item in request.get("typed_inputs", []):
        if item["field_name"] == name:
            return item["normalized_value"]
    return None


def _execution_record(
    *,
    repo_root: Path,
    gold_root: Path,
    receipt_root: Path,
    expected_artifact_sha256: str,
) -> ExecutionRecord:
    """Project one completed false receipt and matching replay into canonical form."""

    request = json.loads((receipt_root / "request.json").read_text(encoding="utf-8"))
    receipt = json.loads((receipt_root / "receipt.json").read_text(encoding="utf-8"))
    replay = json.loads(
        (receipt_root / "replay" / "replay_audit.json").read_text(encoding="utf-8")
    )
    if receipt["state"] != "COMPLETED_BOOLEAN" or receipt["verdict"] is not False:
        raise ValueError(f"{receipt_root} is not completed Boolean false")
    if receipt["artifact_sha256"] != expected_artifact_sha256:
        raise ValueError(f"{receipt_root} used the wrong defective artifact")
    if replay["overall_match"] is not True:
        raise ValueError(f"{receipt_root} replay does not match")
    query_path = receipt_root / "query.json"
    backend_id = (
        receipt.get("backend")
        or receipt.get("oracle_id")
        or receipt["schema_version"].removesuffix("-receipt.v1")
    )
    refs = _receipt_refs(repo_root, receipt_root, receipt)
    return ExecutionRecord(
        state=ExecutionState.COMPLETED_BOOLEAN,
        verdict=False,
        query_path=query_path.relative_to(gold_root).as_posix(),
        query_sha256=sha256_path(query_path),
        command=tuple(receipt["command"]),
        backend_id=backend_id,
        backend_version=receipt["source_commit"],
        backend_code_sha256=_code_hash(receipt),
        artifact_sha256=receipt["artifact_sha256"],
        domain=_input_value(request, "domain"),
        bound=_input_value(request, "bound") or _input_value(request, "horizon"),
        seed=_input_value(request, "seed"),
        started_at=receipt["started_at"],
        completed_at=receipt["completed_at"],
        receipt_refs=refs,
        counterexample_refs=_counterexample_refs(repo_root, receipt_root, receipt),
        replay_status="REPLAY_MATCH",
        reason=(
            "The provider-free evaluation completed with Boolean false and the saved replay matched. "
            "This execution establishes P=false only; exactness remains the separately reviewed O/P relation."
        ),
    )


def _composition(request: dict[str, Any]) -> PropertyComposition | None:
    """Recover explicit non-short-circuit composition from a saved request."""

    if "constituents" not in request:
        return None
    constituent_ids = tuple(
        item.get("request_id") or item.get("constituent_id")
        for item in request["constituents"]
    )
    operator = request["operator"]
    return PropertyComposition(
        operator=operator,
        constituent_ids=constituent_ids,
        truth_definition=(
            f"Evaluate every listed constituent and combine the complete Boolean vector with {operator}; "
            "no false constituent suppresses another receipt."
        ),
        no_short_circuit=True,
    )


def _property(
    candidate: CandidateProperty,
    obligation: Any,
    request_path: Path,
) -> ExecutableProperty:
    """Build the selected exact or proxy property from its frozen proposal/query."""

    request = json.loads(request_path.read_text(encoding="utf-8"))
    return ExecutableProperty(
        property_id=candidate.candidate_id,
        mode=candidate.mode,
        predicate_ids=candidate.predicate_ids,
        expression=candidate.property_expression,
        typed_inputs=candidate.typed_inputs,
        assumptions=candidate.assumptions,
        semantic_scope=obligation.semantic_scope,
        timing=obligation.timing,
        rtc_semantics=obligation.rtc_semantics,
        composition=_composition(request),
        proposal_sha256=request["property_proposal_sha256"],
    )


def _positive_control(
    *,
    repo_root: Path,
    gold_root: Path,
    ledger_id: str,
    c_row: TrackCReviewRow,
) -> PositiveControl:
    """Project a true minimal-repair control and matching replay."""

    receipt_root = gold_root / "receipts" / ledger_id / "positive_control"
    receipt = json.loads((receipt_root / "receipt.json").read_text(encoding="utf-8"))
    replay = json.loads(
        (receipt_root / "replay" / "replay_audit.json").read_text(encoding="utf-8")
    )
    provenance_path = gold_root / "controls" / ledger_id / "control_provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if receipt["state"] != "COMPLETED_BOOLEAN" or receipt["verdict"] is not True:
        raise ValueError(f"{ledger_id} positive control is not completed Boolean true")
    if replay["overall_match"] is not True:
        raise ValueError(f"{ledger_id} positive-control replay does not match")
    artifact_path = receipt["artifact_path"]
    artifact_sha256 = receipt["artifact_sha256"]
    if sha256_path(repo_root / artifact_path) != artifact_sha256:
        raise ValueError(f"{ledger_id} positive-control artifact hash changed")
    reason = (
        provenance.get("reason")
        or provenance.get("repair_intent")
        or provenance.get("change")
        or "The versioned provenance records the minimal repair used as the true-side control."
    )
    return PositiveControl(
        status=PositiveControlStatus.COMPLETED_TRUE,
        control_kind="source-provenanced minimal-repair positive control",
        artifact_path=artifact_path,
        artifact_sha256=artifact_sha256,
        verdict=True,
        receipt_refs=(
            *_receipt_refs(repo_root, receipt_root, receipt),
            _ref(repo_root, provenance_path, element=f"{ledger_id} control provenance"),
        ),
        contamination_check=(
            "PASS: the control provenance records pre-execution selection or excludes method/Judge output; "
            f"Track C contamination disposition is {c_row.contamination_check}."
        ),
        vacuity_check=(
            f"Track C vacuity disposition is {c_row.vacuity_check}; the control query completed true and replayed identically."
        ),
        reason=reason,
    )


def assemble_dataset(
    *,
    repo_root: Path,
    gold_root: Path,
    review_root: Path,
    active_manifest_path: Path,
    generated_at: str,
    source_commit: str,
    pyfcstm_commit: str,
) -> PredicateGoldDataset:
    """Assemble all 145 final annotations from the hash-selected evidence set."""

    manifest = ActiveReviewManifest.model_validate_json(
        active_manifest_path.read_text(encoding="utf-8")
    )
    a_rows, a_reviewers = _load_rows(
        review_root, manifest.track_a, TrackAProposalBatch
    )
    b_rows, b_reviewers = _load_rows(
        review_root, manifest.track_b, TrackBProposalBatch
    )
    c_rows, c_reviewers = _load_rows(
        review_root, manifest.track_c, TrackCReviewBatch
    )
    high_risk_rows, high_risk_reviewers = _load_rows(
        review_root, manifest.high_risk, HighRiskReviewBatch
    )
    arbitration_rows, _ = _load_rows(
        review_root, manifest.arbitration, Pane5ArbitrationBatch
    )
    if not (
        set(a_rows)
        == set(b_rows)
        == set(c_rows)
        == set(high_risk_rows)
        == set(arbitration_rows)
    ):
        raise ValueError("active A/B/C/high-risk/arbitration coverage differs")

    inventory_path = gold_root / "inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    pair_inventory = {item["pair_id"]: item for item in inventory["pairs"]}
    ledger = json.loads(
        (repo_root / inventory["ledger_path"]).read_text(encoding="utf-8")
    )
    items: dict[str, PredicateGoldAnnotation] = {}
    for ledger_id in sorted(a_rows):
        a_row = a_rows[ledger_id]
        b_row = b_rows[ledger_id]
        c_row = c_rows[ledger_id]
        high_risk_row = high_risk_rows[ledger_id]
        arbitration_row = arbitration_rows[ledger_id]
        arbitration = arbitration_row.arbitration
        if arbitration_row.track_a_opinion_sha256 != a_row.proposal_sha256:
            raise ValueError(f"{ledger_id} arbitration does not bind active Track A")
        if arbitration_row.track_b_opinion_sha256 != b_row.proposal_sha256:
            raise ValueError(f"{ledger_id} arbitration does not bind active Track B")
        if arbitration_row.track_c_opinion_sha256 != c_row.opinion_sha256:
            raise ValueError(f"{ledger_id} arbitration does not bind active Track C")
        if (
            arbitration_row.high_risk_opinion_sha256
            != high_risk_row.opinion_sha256
        ):
            raise ValueError(
                f"{ledger_id} arbitration does not bind active fourth review"
            )

        selected_candidate_id, sealed_selected_candidate = _sealed_execution_selection(
            gold_root=gold_root,
            ledger_id=ledger_id,
            b_row=b_row,
            c_row=c_row,
            final_status=arbitration.final_status,
        )
        candidates = _project_candidates(
            b_row,
            repo_root=repo_root,
            final_status=arbitration.final_status,
            final_relation=arbitration.final_exactness_relation,
            selected_candidate_id=selected_candidate_id,
            sealed_selected_candidate=sealed_selected_candidate,
        )
        selected = next((item for item in candidates if item.selected), None)
        executable = arbitration.final_status in {
            GoldStatus.EXACT_FALSE,
            GoldStatus.COMPOSITE_EXACT_FALSE,
            GoldStatus.SOUND_FALSE_PROXY,
        }
        if executable and selected is None:
            raise ValueError(f"{ledger_id} executable final status has no selected property")

        gold_property = None
        proxy_property = None
        execution = None
        proxy_execution = None
        positive_control = None
        predicate_ids: tuple[str, ...] = ()
        false_refs: tuple[SourceRef, ...] = ()
        counterexample_refs: tuple[SourceRef, ...] = ()
        if executable and selected is not None:
            defect_root = gold_root / "receipts" / ledger_id / "defective"
            selected_property = _property(
                selected,
                a_row.normalized_obligation,
                defect_root / "request.json",
            )
            selected_execution = _execution_record(
                repo_root=repo_root,
                gold_root=gold_root,
                receipt_root=defect_root,
                expected_artifact_sha256=pair_inventory[ledger_id.split("-")[1]][
                    "fcstm_sha256"
                ],
            )
            positive_control = _positive_control(
                repo_root=repo_root,
                gold_root=gold_root,
                ledger_id=ledger_id,
                c_row=c_row,
            )
            if arbitration.final_status == GoldStatus.SOUND_FALSE_PROXY:
                proxy_property = selected_property
                proxy_execution = selected_execution
            else:
                gold_property = selected_property
                execution = selected_execution
                predicate_ids = selected_property.predicate_ids
                false_refs = selected_execution.receipt_refs
                counterexample_refs = selected_execution.counterexample_refs

        pair_id = ledger_id.split("-")[1]
        pair = pair_inventory[pair_id]
        opinions = (
            _opinion_a(a_reviewers[ledger_id], a_row.packet_sha256, a_row),
            _opinion_b(b_reviewers[ledger_id], b_row),
            _opinion_c(c_reviewers[ledger_id], c_row),
            _opinion_high_risk(
                high_risk_reviewers[ledger_id], high_risk_row
            ),
        )
        capability_gap = tuple(b_row.capability_gaps)
        unsupported_reason = None
        if arbitration.final_status == GoldStatus.UNSUPPORTED_EXACT:
            unsupported_reason = arbitration.reason
            if not capability_gap:
                capability_gap = tuple(c_row.conflicts) or (c_row.reason,)
        if arbitration.final_status == GoldStatus.SOUND_FALSE_PROXY:
            gold_mode = GoldMode.PROXY_ONLY
        elif arbitration.final_status == GoldStatus.UNSUPPORTED_EXACT:
            gold_mode = GoldMode.UNSUPPORTED
        elif selected is not None:
            gold_mode = selected.mode
        else:
            raise ValueError(f"{ledger_id} final mode cannot be derived")

        annotation = PredicateGoldAnnotation(
            ledger_id=ledger_id,
            pair_id=pair_id,
            family=ledger_id.split("-")[0],
            ledger_sha256=inventory["ledger_sha256"],
            nl_path=pair["nl_path"],
            nl_sha256=pair["nl_sha256"],
            artifact_path=pair["fcstm_path"],
            artifact_sha256=pair["fcstm_sha256"],
            author_source_path=pair["plantuml_path"],
            author_source_sha256=pair["plantuml_sha256"],
            d_tier=ledger["items"][ledger_id]["D"],
            l_tier=ledger["items"][ledger_id]["L"],
            normalized_obligation=a_row.normalized_obligation,
            obligation_source_refs=a_row.normalized_obligation.source_refs,
            alternative_readings=a_row.alternative_readings,
            candidate_properties=candidates,
            rejected_candidate_ids=tuple(
                item.candidate_id for item in candidates if not item.selected
            ),
            exactness_relation=arbitration.final_exactness_relation,
            gold_status=arbitration.final_status,
            gold_mode=gold_mode,
            gold_property=gold_property,
            predicate_ids=predicate_ids,
            execution=execution,
            false_receipt_refs=false_refs,
            counterexample_refs=counterexample_refs,
            positive_control=positive_control,
            proxy_property=proxy_property,
            proxy_execution=proxy_execution,
            unsupported_reason=unsupported_reason,
            capability_gap=capability_gap,
            reason=arbitration.reason,
            basis=arbitration.basis,
            review_opinions=opinions,
            reviewer_ids=tuple(opinion.reviewer_id for opinion in opinions),
            conflicts=arbitration_row.conflicts,
            arbitration=arbitration,
            confidence=Confidence(c_row.confidence.value),
            created_at=generated_at,
        )
        items[ledger_id] = annotation

    return PredicateGoldDataset(
        generated_at=generated_at,
        source_commit=source_commit,
        ledger_path=inventory["ledger_path"],
        ledger_sha256=inventory["ledger_sha256"],
        registry_path=inventory["registry_path"],
        registry_sha256=inventory["registry_sha256"],
        inventory_path="inventory.json",
        inventory_sha256=sha256_path(inventory_path),
        pyfcstm_commit=pyfcstm_commit,
        items=items,
        provider_experiment_calls=0,
        method_reruns=0,
        judge_reruns=0,
        full_experiment_reruns=0,
    )


def main(argv: list[str] | None = None) -> int:
    """Assemble and write the canonical predicate-gold JSON."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--gold-root", type=Path, required=True)
    parser.add_argument("--review-root", type=Path, required=True)
    parser.add_argument("--active-review-manifest", type=Path, required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    dataset = assemble_dataset(
        repo_root=args.repo_root.resolve(),
        gold_root=args.gold_root.resolve(),
        review_root=args.review_root.resolve(),
        active_manifest_path=args.active_review_manifest.resolve(),
        generated_at=args.generated_at,
        source_commit=args.source_commit,
        pyfcstm_commit=args.pyfcstm_commit,
    )
    write_json(args.output, dataset.model_dump(mode="json"))
    PredicateGoldDataset.model_validate_json(args.output.read_text(encoding="utf-8"))
    print(f"wrote {args.output} ({len(dataset.items)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
