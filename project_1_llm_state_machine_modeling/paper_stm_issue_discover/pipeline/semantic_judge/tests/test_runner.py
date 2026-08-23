from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from pipeline.semantic_judge import cli, runner
from pipeline.semantic_judge.metrics import compute_semantic_metrics
from pipeline.semantic_judge.models import (
    AdapterAudit,
    AdapterIdMap,
    MatchStrength,
    ReportValidity,
)
from pipeline.semantic_judge.protocol import SYSTEM_PROMPT
from pipeline.semantic_judge.runner import (
    JudgeExecutionFailure,
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
            AdapterIdMap(anonymous_id=f"E{index:04d}", original_id=f"LEDGER-{index}")
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


def test_system_prompt_carries_frozen_scope_and_carrier_boundaries() -> None:
    assert "Audit each report's core technical claim" in SYSTEM_PROMPT
    assert "every relation to every expected issue is NO_MATCH" in SYSTEM_PROMPT
    assert "allowed equivalent authored carrier" in SYSTEM_PROMPT
    assert "generated lowering members" in SYSTEM_PROMPT
    assert "Infer hierarchy, concurrency, reachability, ownership" in SYSTEM_PROMPT
    assert "Do not invent undeclared runtime semantics" in SYSTEM_PROMPT
    assert "summary and complete detail together" in SYSTEM_PROMPT
    assert "explicit core facet" in SYSTEM_PROMPT
    assert "exact schema order" in SYSTEM_PROMPT
    assert "minimal explicit NO_MATCH row" in SYSTEM_PROMPT
    assert "never the reason or basis you generate" in SYSTEM_PROMPT
    for benchmark_term in ("0053", "0035", "0046", "PumpState", "cooking-time"):
        assert benchmark_term not in SYSTEM_PROMPT


def test_primary_projection_preserves_a_refuted_causal_certificate_for_audit() -> None:
    judge_input = minimal_input()
    report = judge_input.reports[0].model_copy(
        update={
            "claim": "The required first state is not ensured.",
            "where": "Sibling composites with local initial transitions.",
            "reason": "The sibling composites activate concurrently.",
        }
    )
    judge_input = judge_input.model_copy(update={"reports": (report,)})

    prompt = build_primary_prompt(judge_input)

    assert '"claim": "The required first state is not ensured."' in prompt
    assert '"where": "Sibling composites with local initial transitions."' in prompt
    assert '"reason": "The sibling composites activate concurrently."' in prompt
    assert "Do not replace a false mechanism" in SYSTEM_PROMPT


def test_cli_uses_one_runtime_and_persists_failure_without_partial_summary(
    tmp_path: Path, monkeypatch
) -> None:
    source_root = tmp_path / "source"
    source_root.mkdir()
    source_path = source_root / "record.json"
    source_path.write_text("{}", encoding="utf-8")
    ledger = tmp_path / "ledger.json"
    ledger.write_text("{}", encoding="utf-8")
    output = tmp_path / "output"
    runtimes = []

    class RuntimeFixture:
        def __init__(self, *args, **kwargs):
            runtimes.append((args, kwargs))

    monkeypatch.setattr(cli, "verify_snapshot", lambda _root: None)
    monkeypatch.setattr(cli, "_require_clean_commit", lambda _root: "a" * 40)
    monkeypatch.setattr(cli, "_source_path", lambda *_args: source_path)
    monkeypatch.setattr(cli, "_source_root_hash", lambda *_args: "sha256:" + "b" * 64)
    monkeypatch.setattr(cli, "PublicStructuredRuntime", RuntimeFixture)
    monkeypatch.setattr(cli, "load_expected_issues", lambda *_args: ((), ()))

    def fail_adapter(*_args):
        raise RuntimeError("fixture pair failure")

    monkeypatch.setattr(cli, "adapt_x1v2_record", fail_adapter)
    status = cli.main(
        [
            "--report-root",
            str(tmp_path / "reports"),
            "--ledger",
            str(ledger),
            "--source-format",
            "x1v2_record",
            "--source-root",
            str(source_root),
            "--output-dir",
            str(output),
            "--run-id",
            "fixture-failure",
            "--round",
            "1",
            "--pair-id",
            "0004",
            "--allow-live",
        ]
    )
    artifact_root = output / "fixture-failure"
    failure = json.loads(
        (artifact_root / "failure_summary.json").read_text(encoding="utf-8")
    )
    assert status == 1
    assert len(runtimes) == 1
    assert failure["status"] == "failed"
    assert failure["failures"][0]["pair_id"] == "0004"
    assert failure["failures"][0]["error_message"] == "fixture pair failure"
    assert failure["failures"][0]["call_receipts"] == []
    assert failure["failures"][0]["total_judge_cost_usd"] == 0.0
    assert failure["total_judge_cost_usd"] == 0.0
    assert not (artifact_root / "summary.json").exists()


def test_failed_primary_retains_billable_usage_and_cost_receipt() -> None:
    judge_input = minimal_input()

    class FailedRuntime:
        real_llm = True
        profile = "gpt-5.6-luna"
        config = SimpleNamespace(max_output_tokens=128_000)

        def call(self, **_kwargs):
            return SimpleNamespace(
                succeeded=False,
                response=None,
                usage=[
                    {
                        "model_call_id": "call-failed-schema",
                        "status": "success",
                        "model": "gpt-5.6-luna",
                        "input_tokens": 1000,
                        "output_tokens": 200,
                        "input_token_details": {
                            "cache_read": 800,
                            "cache_creation": 50,
                        },
                        "cost_counted": True,
                        "billing_disposition": "billable",
                    }
                ],
                attempts=[
                    {
                        "outer_attempt": 1,
                        "status": "failed",
                        "provider_error": False,
                        "billing_disposition": "billable",
                    }
                ],
                cost={"total_usd": 0.0125, "eligible": True},
                reason="Schema handling failed after a billable model response.",
                basis="Provider-free failure accounting fixture.",
            )

    with pytest.raises(JudgeExecutionFailure) as caught:
        judge_pair(
            run_id="fixture-failed-run",
            round_no=1,
            judge_input=judge_input,
            adapter_audit=adapter_audit(1, 1),
            runtime=FailedRuntime(),
            judge_code_commit="f" * 40,
        )
    receipts = caught.value.call_receipts
    assert len(receipts) == 1
    assert receipts[0].status == "failed"
    assert receipts[0].cost_usd == 0.0125
    assert receipts[0].usage[0].cache_read_input_tokens == 800
    assert receipts[0].usage[0].cache_write_input_tokens == 50
    assert receipts[0].usage[0].billing_disposition == "billable"


def test_post_provider_materialization_failure_retains_billable_receipt(
    monkeypatch,
) -> None:
    judge_input = minimal_input()
    payload = reading_payload(judge_input)

    class BillableRuntime(FakeRuntime):
        def call(self, **kwargs):
            outcome = super().call(**kwargs)
            outcome.usage = [
                {
                    "model_call_id": "call-success-before-local-failure",
                    "status": "success",
                    "model": "gpt-5.6-luna",
                    "input_tokens": 1200,
                    "output_tokens": 300,
                    "input_token_details": {"cache_read": 900},
                    "cost_counted": True,
                    "billing_disposition": "billable",
                }
            ]
            outcome.cost = {"total_usd": 0.02, "eligible": True}
            return outcome

    def fail_materialization(*_args):
        raise ValueError("fixture deterministic materialization failure")

    monkeypatch.setattr(runner, "materialize_reading", fail_materialization)
    with pytest.raises(JudgeExecutionFailure) as caught:
        judge_pair(
            run_id="fixture-post-provider-failure",
            round_no=1,
            judge_input=judge_input,
            adapter_audit=adapter_audit(1, 1),
            runtime=BillableRuntime((payload,)),
            judge_code_commit="f" * 40,
        )

    assert str(caught.value) == "fixture deterministic materialization failure"
    assert len(caught.value.call_receipts) == 1
    assert caught.value.call_receipts[0].status == "success"
    assert caught.value.call_receipts[0].cost_usd == 0.02
    assert caught.value.call_receipts[0].usage[0].input_tokens == 1200


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
    from pipeline.semantic_judge.schema import (
        build_exact_response_model,
        materialize_reading,
    )

    schema = build_exact_response_model(judge_input)
    first = materialize_reading(schema.model_validate(schema_payload_1), judge_input)
    second = materialize_reading(schema.model_validate(schema_payload_2), judge_input)
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
    final_reading = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    final = {
        "schema_version": "semantic-judge.arbitration-response.v3",
        "report_judgments": final_reading["report_judgments"],
        "reason": "Targeted arbitration selects the artifact-supported valid report.",
        "basis": "Fixture common artifacts and both primary report judgments.",
        "source_refs": ["artifact:natural_language"],
    }
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


def test_targeted_arbitration_is_invariant_to_id_renaming_and_input_order() -> None:
    base_input = minimal_input(report_count=2, expected_count=2)
    report_a = base_input.reports[0].model_copy(
        update={"claim": "alpha defect", "reason": "alpha causal certificate"}
    )
    report_b = base_input.reports[1].model_copy(
        update={"claim": "beta defect", "reason": "beta causal certificate"}
    )
    expected_x = base_input.expected_issues[0].model_copy(
        update={"summary": "expected alpha", "detail": "alpha obligation"}
    )
    expected_y = base_input.expected_issues[1].model_copy(
        update={"summary": "expected beta", "detail": "beta obligation"}
    )
    first_input = type(base_input).model_validate(
        {
            **base_input.model_dump(mode="json"),
            "reports": [report_a.model_dump(mode="json"), report_b.model_dump(mode="json")],
            "expected_issues": [
                expected_x.model_dump(mode="json"),
                expected_y.model_dump(mode="json"),
            ],
        }
    )
    second_input = type(base_input).model_validate(
        {
            **base_input.model_dump(mode="json"),
            "reports": [
                report_b.model_copy(update={"report_id": "R0001"}).model_dump(mode="json"),
                report_a.model_copy(update={"report_id": "R0002"}).model_dump(mode="json"),
            ],
            "expected_issues": [
                expected_y.model_copy(update={"expected_id": "E0001"}).model_dump(
                    mode="json"
                ),
                expected_x.model_copy(update={"expected_id": "E0002"}).model_dump(
                    mode="json"
                ),
            ],
        }
    )

    def run_with_targeted_arbitration(judge_input, alpha_report_id, alpha_expected_id):
        beta_report_id = "R0002" if alpha_report_id == "R0001" else "R0001"
        beta_expected_id = "E0002" if alpha_expected_id == "E0001" else "E0001"
        clusters = {
            alpha_report_id: "alpha actionable root cause",
            beta_report_id: "beta actionable root cause",
        }
        final_matches = {
            (alpha_report_id, alpha_expected_id): MatchStrength.FULL_MATCH,
            (beta_report_id, beta_expected_id): MatchStrength.PARTIAL_MATCH,
        }
        conflicting_matches = {
            **final_matches,
            (alpha_report_id, alpha_expected_id): MatchStrength.PARTIAL_MATCH,
        }
        primary_1 = reading_payload(
            judge_input, matches=final_matches, clusters=clusters
        )
        primary_2 = reading_payload(
            judge_input, matches=conflicting_matches, clusters=clusters
        )
        arbitration_full = reading_payload(
            judge_input, matches=final_matches, clusters=clusters
        )
        arbitration = {
            "schema_version": "semantic-judge.arbitration-response.v3",
            "report_judgments": [
                row
                for row in arbitration_full["report_judgments"]
                if row["report_id"] == alpha_report_id
            ],
            "reason": "Targeted arbitration restores the artifact-supported semantic relation.",
            "basis": "Both primary judgments and the unchanged common artifact closure.",
            "source_refs": ["artifact:natural_language"],
        }
        return judge_pair(
            run_id="metamorphic-fixture",
            round_no=1,
            judge_input=judge_input,
            adapter_audit=adapter_audit(2, 2),
            runtime=FakeRuntime((primary_1, primary_2, arbitration)),
            judge_code_commit="c" * 40,
        )

    first_result = run_with_targeted_arbitration(first_input, "R0001", "E0001")
    second_result = run_with_targeted_arbitration(second_input, "R0002", "E0002")

    def semantic_signature(result, judge_input):
        report_claims = {item.report_id: item.claim for item in judge_input.reports}
        expected_summaries = {
            item.expected_id: item.summary for item in judge_input.expected_issues
        }
        relations = tuple(
            sorted(
                (
                    report_claims[row.report_id],
                    expected_summaries[row.expected_id],
                    row.match.value,
                )
                for row in result.final_reading.relations
            )
        )
        reports = tuple(
            sorted(
                (
                    report_claims[row.report_id],
                    row.core_truth.value,
                    row.validity.value,
                    row.root_cause_cluster_key,
                )
                for row in result.final_reading.report_assessments
            )
        )
        expected = tuple(
            sorted(
                (
                    expected_summaries[row.expected_id],
                    row.hit,
                    row.supported,
                )
                for row in result.final_reading.expected_assessments
            )
        )
        return relations, reports, expected

    assert first_result.arbitration_reading is not None
    assert second_result.arbitration_reading is not None
    assert semantic_signature(first_result, first_input) == semantic_signature(
        second_result, second_input
    )
    assert first_result.metrics.model_dump(exclude={"reason", "basis"}) == (
        second_result.metrics.model_dump(exclude={"reason", "basis"})
    )
