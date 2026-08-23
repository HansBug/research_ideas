from __future__ import annotations

from pipeline.semantic_judge.metrics import compute_semantic_metrics
from pipeline.semantic_judge.models import MatchStrength, ReportValidity
from pipeline.semantic_judge.schema import (
    build_exact_response_model,
    materialize_reading,
)

from .test_models_and_schema import minimal_input, reading_payload


def validate(judge_input, payload):
    response = build_exact_response_model(judge_input).model_validate(payload)
    return materialize_reading(response)


def test_0023_one_global_report_can_full_three_atomic_dead_ends() -> None:
    judge_input = minimal_input(report_count=1, expected_count=3)
    matches = {
        ("R0001", "E0001"): MatchStrength.FULL_MATCH,
        ("R0001", "E0002"): MatchStrength.FULL_MATCH,
        ("R0001", "E0003"): MatchStrength.FULL_MATCH,
    }
    reading = validate(judge_input, reading_payload(judge_input, matches=matches))
    metrics = compute_semantic_metrics(reading)
    assert metrics.full_hit_count == 3
    assert metrics.supported_count == 3
    assert metrics.invalid_count == 0


def test_free_text_report_without_typed_property_can_full() -> None:
    judge_input = minimal_input()
    assert judge_input.reports[0].property is None
    assert judge_input.reports[0].basis is None
    reading = validate(
        judge_input,
        reading_payload(
            judge_input,
            matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
        ),
    )
    assert compute_semantic_metrics(reading).full_hit_count == 1


def test_partial_is_supported_but_never_hit_or_fp() -> None:
    judge_input = minimal_input()
    reading = validate(
        judge_input,
        reading_payload(
            judge_input,
            matches={("R0001", "E0001"): MatchStrength.PARTIAL_MATCH},
        ),
    )
    metrics = compute_semantic_metrics(reading)
    assert metrics.full_hit_count == 0
    assert metrics.supported_count == 1
    assert metrics.invalid_count == 0
    assert metrics.semantic_precision == 1.0
    assert metrics.ledger_unmatched_count == 1


def test_valid_novel_is_neither_hit_nor_fp() -> None:
    judge_input = minimal_input()
    reading = validate(judge_input, reading_payload(judge_input))
    metrics = compute_semantic_metrics(reading)
    assert metrics.valid_novel_count == 1
    assert metrics.invalid_count == 0
    assert metrics.full_hit_count == 0
    assert metrics.semantic_precision == 1.0


def test_existing_carrier_misreported_missing_is_invalid_only() -> None:
    judge_input = minimal_input()
    reading = validate(
        judge_input,
        reading_payload(
            judge_input,
            validity={"R0001": ReportValidity.INVALID},
            clusters={"R0001": "false-missing-carrier"},
        ),
    )
    metrics = compute_semantic_metrics(reading)
    assert metrics.invalid_count == 1
    assert metrics.full_hit_count == 0
    assert metrics.semantic_precision == 0.0


def test_wrong_source_0053_report_cannot_be_repaired_by_judge() -> None:
    judge_input = minimal_input()
    reading = validate(
        judge_input,
        reading_payload(
            judge_input,
            validity={"R0001": ReportValidity.INVALID},
            clusters={"R0001": "wrong-transition-source"},
        ),
    )
    expected = reading.expected_assessments[0]
    assert not expected.hit
    assert not expected.supported
    assert compute_semantic_metrics(reading).invalid_count == 1


def test_duplicate_valid_reports_are_redundancy_not_false_positives() -> None:
    judge_input = minimal_input(report_count=2, expected_count=1)
    matches = {
        ("R0001", "E0001"): MatchStrength.FULL_MATCH,
        ("R0002", "E0001"): MatchStrength.FULL_MATCH,
    }
    reading = validate(
        judge_input,
        reading_payload(
            judge_input,
            matches=matches,
            clusters={"R0001": "same-root-cause", "R0002": "same-root-cause"},
        ),
    )
    metrics = compute_semantic_metrics(reading)
    assert metrics.full_hit_count == 1
    assert metrics.invalid_count == 0
    assert metrics.cluster_count == 1
    assert metrics.redundancy_rate == 0.5


def test_order_and_opaque_id_renaming_do_not_change_metrics() -> None:
    first_input = minimal_input(report_count=2, expected_count=2)
    first_matches = {
        ("R0001", "E0001"): MatchStrength.FULL_MATCH,
        ("R0002", "E0002"): MatchStrength.PARTIAL_MATCH,
    }
    first_payload = reading_payload(first_input, matches=first_matches)
    first_payload["relations"].reverse()
    first_payload["report_judgments"].reverse()
    first_payload["expected_judgments"].reverse()
    first = compute_semantic_metrics(validate(first_input, first_payload))

    second_input = minimal_input(report_count=2, expected_count=2)
    second_matches = {
        ("R0002", "E0002"): MatchStrength.FULL_MATCH,
        ("R0001", "E0001"): MatchStrength.PARTIAL_MATCH,
    }
    second = compute_semantic_metrics(
        validate(second_input, reading_payload(second_input, matches=second_matches))
    )
    assert first.model_dump(exclude={"reason", "basis"}) == second.model_dump(
        exclude={"reason", "basis"}
    )
