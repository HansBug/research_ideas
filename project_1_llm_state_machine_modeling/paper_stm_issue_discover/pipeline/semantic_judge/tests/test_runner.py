from __future__ import annotations

from types import SimpleNamespace

from pipeline.semantic_judge.metrics import compute_semantic_metrics
from pipeline.semantic_judge.models import (
    AdapterAudit,
    AdapterIdMap,
    MatchStrength,
    ReportValidity,
)
from pipeline.semantic_judge.runner import (
    build_conflict_records,
    build_primary_prompt,
    detect_disagreements,
    judge_pair,
)

from .test_models_and_schema import minimal_input, reading_payload


class FakeRuntime:
    real_llm = False
    profile = "gpt-5.6-luna"

    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []
        self.config = SimpleNamespace(max_output_tokens=128_000)

    def call(self, **kwargs):
        self.calls.append(kwargs)
        payload = self.payloads.pop(0)
        response = kwargs["schema"].model_validate(payload)
        return SimpleNamespace(
            succeeded=True,
            response=response,
            usage=[],
            attempts=[],
            cost={"total_usd": 0.0, "eligible": True},
            reason="Provider-free structured fixture succeeded.",
            basis="FakeRuntime exact Pydantic validation.",
        )


def adapter_audit(report_count: int, expected_count: int) -> AdapterAudit:
    return AdapterAudit(
        source_format="x1v2_record",
        source_path="/fixture/source.json",
        source_hash="sha256:" + "3" * 64,
        report_id_map=tuple(
            AdapterIdMap(
                anonymous_id=f"R{index:04d}", original_id=f"original-report-{index}"
            )
            for index in range(1, report_count + 1)
        ),
        expected_id_map=tuple(
            AdapterIdMap(
                anonymous_id=f"E{index:04d}", original_id=f"LEDGER-{index}"
            )
            for index in range(1, expected_count + 1)
        ),
        projected_field_names=("report_id", "claim"),
        excluded_field_names=("arm", "witness_level", "d_level"),
        reason="fixture adapter",
        basis="provider-free fixture",
    )


def test_primary_prompt_has_no_adapter_or_method_metadata() -> None:
    judge_input = minimal_input()
    prompt = build_primary_prompt(judge_input)
    assert "x1v2_record" not in prompt
    assert "evidence_discovery_release" not in prompt
    assert '"arm"' not in prompt
    assert '"witness_level"' not in prompt
    assert '"d_level"' not in prompt
    assert '"predicate_id"' not in prompt


def test_conflict_detection_ignores_reason_wording_but_catches_semantics() -> None:
    judge_input = minimal_input()
    schema_payload_1 = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    schema_payload_2 = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.PARTIAL_MATCH},
    )
    from pipeline.semantic_judge.schema import build_exact_reading_model

    schema = build_exact_reading_model(judge_input)
    first = schema.model_validate(schema_payload_1)
    second = schema.model_validate(schema_payload_2)
    conflicts = detect_disagreements(first, second)
    assert {item.kind.value for item in conflicts} == {"relation"}
    records = build_conflict_records(conflicts, first)
    assert records[0].final_value == "FULL_MATCH"


def test_single_entry_runs_both_readings_and_arbitration() -> None:
    judge_input = minimal_input()
    first = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    second = reading_payload(
        judge_input,
        validity={"R0001": ReportValidity.INVALID},
        clusters={"R0001": "invalid-claim"},
    )
    final = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    runtime = FakeRuntime((first, second, final))
    result = judge_pair(
        run_id="fixture-run",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 1),
        runtime=runtime,
        judge_code_commit="a" * 40,
    )
    assert len(runtime.calls) == 3
    assert runtime.calls[0]["prompt"] == runtime.calls[1]["prompt"]
    assert result.arbitration_reading is not None
    assert result.metrics.full_hit_count == 1
    assert result.metrics.invalid_count == 0
    assert result.report_outcomes[0].original_report_id == "original-report-1"
    assert result.expected_outcomes[0].ledger_id == "LEDGER-1"


def test_no_conflict_uses_two_calls_and_deterministic_metrics() -> None:
    judge_input = minimal_input()
    payload = reading_payload(judge_input)
    runtime = FakeRuntime((payload, payload))
    result = judge_pair(
        run_id="fixture-run",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 1),
        runtime=runtime,
        judge_code_commit="b" * 40,
    )
    assert len(runtime.calls) == 2
    assert result.arbitration_reading is None
    assert not result.conflicts
    assert result.metrics == compute_semantic_metrics(result.final_reading)
