from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from paper_stm_evaluation.manual_adjudication import (
    A0Type,
    AdjudicationStatus,
    FactStatus,
    GroupDecision,
    HumanReview,
    Relation,
    RelationDecision,
    ReportDecision,
    ReportValidity,
    RawInventory,
    RawReportRef,
    Side,
    SourceRef,
    StrictDA,
    Witness,
    WitnessLevel,
    derive_kni,
    validate_decision_set,
    validate_tsv_mirror,
    write_tsv_mirror,
)


SCRIPT_DIRECTORY = Path(__file__).resolve().parents[3] / "scripts" / "evaluation"
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from build_reviewer_projection import FORBIDDEN_KEYS, SEMANTIC_FORBIDDEN_KEYS, canonical_bytes  # noqa: E402
from generate_manual_adjudication import parse_reference_relation_ids  # noqa: E402
from validate_manual_adjudication import validate_reviewer_projection  # noqa: E402


def _ref(name: str) -> SourceRef:
    return SourceRef(repository_path=name, sha256="sha256:" + "a" * 64)


def _review() -> HumanReview:
    return HumanReview(
        primary_reviewer_id="human-primary",
        independent_reviewer_id="human-independent",
        final_adjudicator_id="human-adjudicator",
        human_confirmation=True,
        human_supervised_session=True,
        authorization_reference="user-authorization-2026-08-29",
        authorization_message_sha256="sha256:" + "d" * 64,
        authorization_time_utc="2026-08-29T00:00:00Z",
        attestation="The authorized human-supervised session read the cited evidence and confirmed the final record.",
        independent_is_subagent_proposal=False,
        confirmed_at="2026-08-29T00:00:00Z",
        confirmation_basis="Human read the raw report, author source, and expected-specific evidence.",
        primary_reason="Primary human review completed.",
        primary_basis="raw/report.json#/parsed_output/issues/0",
        independent_reason="Independent human review completed.",
        independent_basis="raw/source.puml:1",
        arbitration_reason="No unresolved disagreement remained.",
        arbitration_basis="Both reviews cite the same immutable source closure.",
        reviewer_ids=("human-primary", "human-independent", "human-adjudicator"),
        review_status=AdjudicationStatus.FINAL,
        reference_visible=False,
        primary_visible=False,
        submission_hash="sha256:" + "b" * 64,
        independent_submission_at="2026-08-29T00:00:30Z",
        primary_submission_at="2026-08-29T00:00:45Z",
        blind_event_sequence=(
            "blind:independent:raw-first:test",
            "blind:primary:pane5:test",
            "blind:unblind:pane5:test",
        ),
        unblinded_at="2026-08-29T00:01:00Z",
    )


def _decision(*, da: StrictDA = StrictDA.D2, relation: Relation = Relation.FULL_MATCH, a0=None) -> ReportDecision:
    return ReportDecision(
        side=Side.V60_CURRENT,
        pair_id="0001",
        round=1,
        report_id="0001:r1:issue:0",
        report_index=0,
        raw_method_path="raw/v60_current/method/method/0001/round-1.json",
        raw_json_pointer="/report_issue_clusters/0",
        raw_sha256="sha256:" + "c" * 64,
        claim_pointer="/report_issue_clusters/0/issue_id",
        where_pointer="/report_issue_clusters/0/element_refs/0",
        fact_status=FactStatus.REFUTED if da == StrictDA.A0 else FactStatus.ESTABLISHED,
        strict_da=da,
        a0_type=a0,
        validity=ReportValidity.VALID_KNOWN if relation != Relation.NO_MATCH and da in {StrictDA.D1, StrictDA.D2} else (ReportValidity.INVALID if da in {StrictDA.D0, StrictDA.A0} else ReportValidity.VALID_NOVEL),
        corrected_kni="K" if relation != Relation.NO_MATCH and da in {StrictDA.D1, StrictDA.D2} else ("I" if da in {StrictDA.D0, StrictDA.A0} else "N"),
        relations=(RelationDecision(expected_id="EIS-0001-01", relation=relation, reason="Expected-specific reason.", basis="Expected-specific basis.", source_refs=(_ref("reference/ledger.json"),), report_owned_field_refs=("/report_issue_clusters/0",)),),
        ledger_ids=("EIS-0001-01",) if relation == Relation.FULL_MATCH and da in {StrictDA.D1, StrictDA.D2} else (),
        witness=Witness(level=WitnessLevel.W1, concrete_location="transition:line:1"),
        reason="Human reason states the fact, obligation, D/A, and validity.",
        basis="reference/ledger.json and raw report pointer.",
        source_refs=(_ref("raw/v60_current/method/method/0001/round-1.json"), _ref("reference/x1v2_input_closure/pairs/0001/plantuml.puml")),
        review=_review(),
        scoring=True,
        diagnostic_only=False,
    )


def test_kni_is_deterministic_and_partial_is_known_not_fp() -> None:
    assert derive_kni(StrictDA.D1, [Relation.PARTIAL_MATCH]) == ("K", ReportValidity.VALID_KNOWN)
    assert derive_kni(StrictDA.D0, [Relation.NO_MATCH]) == ("I", ReportValidity.INVALID)
    assert derive_kni(StrictDA.D2, [Relation.NO_MATCH]) == ("N", ReportValidity.VALID_NOVEL)


def test_partial_relation_is_not_a_report_fp() -> None:
    decision = _decision(relation=Relation.PARTIAL_MATCH)
    assert decision.validity == ReportValidity.VALID_KNOWN
    assert decision.corrected_kni == "K"


def test_reference_list_ids_respect_the_preserved_relation() -> None:
    """A list-valued legacy ID must not silently turn a partial row into FULL."""

    assert parse_reference_relation_ids(["EIS-0045-01"], "PARTIAL_MATCH") == (set(), {"EIS-0045-01"})
    assert parse_reference_relation_ids(["EIS-0045-01"], "FULL_MATCH") == ({"EIS-0045-01"}, set())
    assert parse_reference_relation_ids(["EIS-0045-01"], "NO_MATCH") == (set(), set())


def test_d0_cannot_carry_positive_relation() -> None:
    with pytest.raises(ValidationError, match="D0/A0"):
        _decision(da=StrictDA.D0, relation=Relation.FULL_MATCH)


def test_x1v2_rejects_not_a_defect_claim() -> None:
    with pytest.raises(ValidationError, match="X1v2"):
        values = _decision(da=StrictDA.A0, relation=Relation.NO_MATCH, a0=A0Type.NOT_A_DEFECT_CLAIM).model_dump()
        values.update({"side": Side.X1V2_BASELINE, "report_id": "0001:r1:baseline_issue_1"})
        ReportDecision.model_validate(values)


def test_w2_requires_original_terminal_receipt() -> None:
    with pytest.raises(ValidationError, match="W2"):
        Witness(level=WitnessLevel.W2, concrete_location="transition:line:1")


def test_group_identity_is_explicit_and_can_be_checked_for_boundaries() -> None:
    group = GroupDecision(
        side=Side.V60_CURRENT,
        pair_id="0023",
        canonical_group_key="0023:zero-behavior:owner-entry",
        report_ids=("0023:r1:issue:0", "0023:r2:issue:1"),
        substantive_property="zero behavior",
        author_source_locus="state:Owner",
        repair_obligation="owner entry must be reachable",
        substantive_cause="missing owner entry",
        group_verdict="N",
        reason="The same property and source locus were independently confirmed.",
        basis="Human group review over the two report decisions.",
        source_refs=(_ref("reference/ledger.json"),),
    )
    assert group.pair_id == "0023"


def test_exact_raw_closure_checks_report_index_and_sha() -> None:
    decision = _decision()
    raw = decision.model_dump(mode="json")
    validate_decision_set(
        [decision],
        expected_ids=["EIS-0001-01"],
        raw_report_index={decision.report_id: raw},
    )
    with pytest.raises(ValueError, match="raw closure mismatch"):
        validate_decision_set(
            [decision.model_copy(update={"raw_sha256": "sha256:" + "d" * 64})],
            expected_ids=["EIS-0001-01"],
            raw_report_index={decision.report_id: raw},
        )


def test_tsv_mirror_is_an_exact_canonical_projection(tmp_path) -> None:
    decision = _decision()
    path = tmp_path / "decisions.tsv"
    write_tsv_mirror(path, [decision])
    validate_tsv_mirror(path, [decision])
    path.write_text(path.read_text(encoding="utf-8").replace("\t0\t", "\t999\t", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="TSV mirror"):
        validate_tsv_mirror(path, [decision])


def test_reviewer_projection_rejects_producer_schema_leakage_and_requires_slot_symmetry(tmp_path) -> None:
    """Raw-first input must not reveal a producer schema or omit a sealed arm slot."""

    archive = tmp_path / "archive"
    directory = archive / "derived" / "manual_adjudication_v2"
    directory.mkdir(parents=True)
    refs = tuple(
        RawReportRef(
            side=side,
            pair_id="0001",
            round=1,
            report_id=report_id,
            report_index=0,
            raw_method_path=f"raw/{side.value}/record.json",
            raw_json_pointer="/report/0",
            raw_sha256="sha256:" + digest * 64,
            claim_pointer="/report/0/claim",
            where_pointer="/report/0/where",
            identity_basis="fixture",
        )
        for side, report_id, digest in (
            (Side.V60_CURRENT, "0001:r1:issue:0", "a"),
            (Side.X1V2_BASELINE, "0001:r1:baseline_issue_1", "b"),
        )
    )
    inventory = RawInventory(
        archive_relative_root="archive",
        generated_at_utc="2026-08-29T00:00:00Z",
        source_manifests={"raw/v60_current/archive_manifest.json": "sha256:" + "c" * 64},
        cells={"v60_current": 1, "x1v2_baseline": 1},
        reports={"v60_current": 1, "x1v2_baseline": 1},
        by_round={"v60_current": {"1": 1}, "x1v2_baseline": {"1": 1}},
        items=refs,
    )

    def projection_row(arm: str) -> dict:
        row = {
            "schema": "paper1.manual-adjudication.reviewer-projection-row.v1",
            "review_key": f"report-{arm}",
            "arm_token": arm,
            "pair_token": "pair-fixture",
            "round": 1,
            "slot": 0,
            "report_evidence": {"claim_text": "claim", "reason_text": "reason", "location_text": ""},
            "author_source": {"nl": "requirement", "plantuml": "@startuml", "nl_sha256": "sha256:" + "d" * 64, "plantuml_sha256": "sha256:" + "e" * 64},
            "redactions_applied": True,
        }
        row["projection_sha256"] = "sha256:" + hashlib.sha256(canonical_bytes(row)).hexdigest()
        return row

    rows = [projection_row("arm-a"), projection_row("arm-b")]
    projection_path = directory / "reviewer_input_projection.jsonl"
    projection_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    audit = {
        "projection_path": str(projection_path.relative_to(archive)),
        "projection_sha256": "sha256:" + hashlib.sha256(projection_path.read_bytes()).hexdigest(),
        "row_count": 2,
        "projected_report_count": 2,
        "padded_slot_count": 0,
        "provider_calls": 0,
        "forbidden_keys": sorted(FORBIDDEN_KEYS | SEMANTIC_FORBIDDEN_KEYS),
    }
    (directory / "reviewer_projection_audit.json").write_text(json.dumps(audit), encoding="utf-8")
    unblind = {
        "schema": "paper1.manual-adjudication.reviewer-unblind-map.v1",
        "raw_first_visible": False,
        "arm_tokens": {"v60_current": "arm-a", "x1v2_baseline": "arm-b"},
        "pair_tokens": {"0001": "pair-fixture"},
        "report_tokens": {"0001:r1:issue:0": "report-arm-a", "0001:r1:baseline_issue_1": "report-arm-b"},
        "padded_tokens": {},
        "rows": [
            {"review_key": "report-arm-a", "side": "v60_current", "pair_id": "0001", "round": 1, "slot": 0, "report_id": "0001:r1:issue:0", "raw_target_sha256": "sha256:" + "f" * 64, "padded": False},
            {"review_key": "report-arm-b", "side": "x1v2_baseline", "pair_id": "0001", "round": 1, "slot": 0, "report_id": "0001:r1:baseline_issue_1", "raw_target_sha256": "sha256:" + "e" * 64, "padded": False},
        ],
    }
    # The fixture uses simple raw objects so its unblind target hashes are exact.
    raw_values = {
        "v60_current": {"report": [{"fixture": "v60"}]},
        "x1v2_baseline": {"report": [{"fixture": "x1v2"}]},
    }
    for side, raw in raw_values.items():
        path = archive / "raw" / side / "record.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(raw), encoding="utf-8")
    for row in unblind["rows"]:
        raw = raw_values[row["side"]]
        row["raw_target_sha256"] = "sha256:" + hashlib.sha256(canonical_bytes(raw["report"][0])).hexdigest()
    (directory / "reviewer_unblind_mapping.json").write_text(json.dumps(unblind), encoding="utf-8")
    validate_reviewer_projection(directory, inventory)

    location_leak = dict(rows[0])
    location_leak["report_evidence"] = dict(location_leak["report_evidence"], location_text="locus")
    location_leak["projection_sha256"] = "sha256:" + hashlib.sha256(
        canonical_bytes({key: value for key, value in location_leak.items() if key != "projection_sha256"})
    ).hexdigest()
    projection_path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in [location_leak, rows[1]]) + "\n", encoding="utf-8")
    audit["projection_sha256"] = "sha256:" + hashlib.sha256(projection_path.read_bytes()).hexdigest()
    (directory / "reviewer_projection_audit.json").write_text(json.dumps(audit), encoding="utf-8")
    with pytest.raises(ValueError, match="producer-specific location"):
        validate_reviewer_projection(directory, inventory)

    producer_claim_leak = dict(rows[0])
    producer_claim_leak["report_evidence"] = dict(
        producer_claim_leak["report_evidence"],
        claim_text="llms_emp_feedback_final_0001 claim",
    )
    producer_claim_leak["projection_sha256"] = "sha256:" + hashlib.sha256(
        canonical_bytes({key: value for key, value in producer_claim_leak.items() if key != "projection_sha256"})
    ).hexdigest()
    projection_path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in [producer_claim_leak, rows[1]]) + "\n", encoding="utf-8")
    audit["projection_sha256"] = "sha256:" + hashlib.sha256(projection_path.read_bytes()).hexdigest()
    (directory / "reviewer_projection_audit.json").write_text(json.dumps(audit), encoding="utf-8")
    with pytest.raises(ValueError, match="producer-specific claim or reason"):
        validate_reviewer_projection(directory, inventory)

    leaked = dict(rows[0])
    leaked["report_index"] = 0
    leaked["projection_sha256"] = "sha256:" + hashlib.sha256(
        canonical_bytes({key: value for key, value in leaked.items() if key != "projection_sha256"})
    ).hexdigest()
    projection_path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in [leaked, rows[1]]) + "\n", encoding="utf-8")
    audit["projection_sha256"] = "sha256:" + hashlib.sha256(projection_path.read_bytes()).hexdigest()
    (directory / "reviewer_projection_audit.json").write_text(json.dumps(audit), encoding="utf-8")
    with pytest.raises(ValueError, match="row shape"):
        validate_reviewer_projection(directory, inventory)
