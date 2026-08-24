from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import utils.agent.runtime as agent_runtime
from pydantic import ValidationError

from pipeline.evidence_discovery.orchestration import runtime as structured_runtime
from pipeline.evidence_discovery.orchestration.runtime import PublicStructuredRuntime
from pipeline.semantic_judge import execution as judge_execution
from pipeline.semantic_judge.artifacts import build_artifact_closure, stable_model_hash
from pipeline.semantic_judge.execution import run_provider_free_process_probe
from pipeline.semantic_judge.models import (
    ArtifactRole,
    RelationBatchJudgeInput,
    ValidityBatchJudgeInput,
)
from pipeline.semantic_judge.protocol import VALIDITY_SYSTEM_PROMPT
from pipeline.semantic_judge.runner import _validity_report_groups, judge_pair
from pipeline.semantic_judge.schema import (
    build_exact_relation_batch_model,
    build_exact_validity_batch_model,
    build_relation_batch_input,
    build_validity_batch_input,
    build_validity_input,
    materialize_validity_certificate,
    relation_item_input,
    validity_item_input,
)

from .test_models_and_schema import PROJECT_ROOT, minimal_input
from .test_runner import adapter_audit, relation_payload, validity_payload


def _validity_batch_payload(batch_input: ValidityBatchJudgeInput) -> dict:
    return {
        "schema_version": "semantic-judge.validity-batch-response.v1",
        "batch_id": batch_input.batch_id,
        **{
            f"item{index}": validity_payload(validity_item_input(batch_input, index))
            for index, _report in enumerate(batch_input.reports)
        },
    }


def _relation_batch_payload(batch_input: RelationBatchJudgeInput) -> dict:
    return {
        "schema_version": "semantic-judge.relation-batch-response.v1",
        "batch_id": batch_input.batch_id,
        **{
            f"item{index}": relation_payload(relation_item_input(batch_input, index))
            for index, _report in enumerate(batch_input.reports)
        },
    }


def test_validity_batch_has_one_artifact_closure_and_exact_report_slots() -> None:
    judge_input = minimal_input(report_count=3, expected_count=2)
    batch_input = build_validity_batch_input(
        judge_input,
        tuple(item.report_id for item in judge_input.reports),
        batch_id="VB-fixture",
    )
    serialized = batch_input.model_dump_json()
    model = build_exact_validity_batch_model(batch_input)
    payload = _validity_batch_payload(batch_input)

    assert serialized.count('"artifact_closure"') == 1
    assert "expected_issues" not in serialized
    assert '"expected_id"' not in serialized
    validated = model.model_validate(payload)
    assert [getattr(validated, f"item{index}").report_id for index in range(3)] == [
        "R0001",
        "R0002",
        "R0003",
    ]

    missing = json.loads(json.dumps(payload))
    missing.pop("item1")
    with pytest.raises(ValidationError, match="item1"):
        model.model_validate(missing)
    extra = json.loads(json.dumps(payload))
    extra["item3"] = extra["item2"]
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        model.model_validate(extra)


def test_expected_changes_do_not_change_validity_batch_or_item_hashes() -> None:
    first = minimal_input(report_count=2, expected_count=2)
    second = first.model_copy(
        update={
            "expected_issues": tuple(
                item.model_copy(
                    update={"expected_id": f"E{3 - index:04d}", "summary": "decoy"}
                )
                for index, item in enumerate(reversed(first.expected_issues), start=1)
            )
        }
    )
    report_ids = ("R0001", "R0002")
    first_batch = build_validity_batch_input(first, report_ids, batch_id="VB-isolation")
    second_batch = build_validity_batch_input(
        second, report_ids, batch_id="VB-isolation"
    )

    assert first_batch == second_batch
    assert stable_model_hash(first_batch) == stable_model_hash(second_batch)
    assert validity_item_input(first_batch, 0) == validity_item_input(second_batch, 0)


def test_dense_validity_rows_use_bounded_eight_report_batches() -> None:
    judge_input = minimal_input(report_count=24, expected_count=8)
    two_clauses = "Primary technical assertion. Supporting technical assertion."
    dense_reports = tuple(
        report.model_copy(
            update={
                "claim": two_clauses,
                "violated_obligation": two_clauses,
                "expected": two_clauses,
                "observed": two_clauses,
                "reason": two_clauses,
            }
        )
        for report in judge_input.reports
    )
    dense_input = judge_input.model_copy(update={"reports": dense_reports})

    groups = _validity_report_groups(dense_input)

    assert tuple(len(group) for group in groups) == (8, 8, 8)
    assert tuple(report_id for group in groups for report_id in group) == tuple(
        report.report_id for report in dense_reports
    )


def test_relation_batch_requires_complete_report_by_expected_matrix() -> None:
    judge_input = minimal_input(report_count=2, expected_count=3)
    certificates = []
    for report in judge_input.reports:
        validity_input = build_validity_input(judge_input, report.report_id)
        certificates.append(
            materialize_validity_certificate(
                build_exact_validity_batch_model(
                    build_validity_batch_input(
                        judge_input,
                        (report.report_id,),
                        batch_id=f"VB-{report.report_id}",
                    )
                )
                .model_validate(
                    _validity_batch_payload(
                        build_validity_batch_input(
                            judge_input,
                            (report.report_id,),
                            batch_id=f"VB-{report.report_id}",
                        )
                    )
                )
                .item0,
                validity_input,
            )
        )
    batch_input = build_relation_batch_input(
        judge_input, tuple(certificates), batch_id="RB-fixture"
    )
    model = build_exact_relation_batch_model(batch_input)
    payload = _relation_batch_payload(batch_input)
    validated = model.model_validate(payload)

    assert len(validated.item0.relation_decisions) == 3
    assert len(validated.item1.relation_decisions) == 3
    missing_report = json.loads(json.dumps(payload))
    missing_report.pop("item1")
    with pytest.raises(ValidationError, match="item1"):
        model.model_validate(missing_report)
    missing_expected = json.loads(json.dumps(payload))
    missing_expected["item0"]["relation_decisions"].pop()
    with pytest.raises(ValidationError):
        model.model_validate(missing_expected)


class _SplittingFixtureRuntime:
    """Provider-free runtime that fails one initial batch before recovery split."""

    real_llm = False
    profile = "fixture"
    config = SimpleNamespace(max_output_tokens=24_000)

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.failed_once = False

    @staticmethod
    def _outcome(*, response=None, succeeded: bool):
        return SimpleNamespace(
            succeeded=succeeded,
            response=response,
            result={},
            usage=[],
            attempts=[],
            cost={"total_usd": 0.0, "eligible": True},
            reason=(
                "Provider-free structured fixture succeeded."
                if succeeded
                else "Controlled batch failure requires deterministic splitting."
            ),
            basis="Provider-free split and resume fixture.",
        )

    def call(self, **kwargs):
        self.calls.append(kwargs)
        recipe = kwargs["schema"].__semantic_judge_recipe__
        if (
            not self.failed_once
            and recipe["kind"] == "validity_batch"
            and len(recipe["input"]["reports"]) > 1
            and "validity_primary_1" in kwargs["artifact_id"]
        ):
            self.failed_once = True
            return self._outcome(succeeded=False)
        if recipe["kind"] == "validity_batch":
            batch_input = ValidityBatchJudgeInput.model_validate(recipe["input"])
            payload = _validity_batch_payload(batch_input)
        else:
            batch_input = RelationBatchJudgeInput.model_validate(recipe["input"])
            payload = _relation_batch_payload(batch_input)
        response = kwargs["schema"].model_validate(payload)
        return self._outcome(response=response, succeeded=True)


def test_failed_batch_splits_without_rerunning_successful_peer() -> None:
    judge_input = minimal_input(report_count=3, expected_count=1)
    runtime = _SplittingFixtureRuntime()

    result = judge_pair(
        run_id="batch-split-fixture",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(3, 1),
        runtime=runtime,
        judge_code_commit="f" * 40,
    )

    validity_primary_2 = [
        item for item in runtime.calls if "validity_primary_2" in item["artifact_id"]
    ]
    assert len(validity_primary_2) == 1
    assert len(result.call_receipts) == 6
    assert sum(item.status == "failed" for item in result.call_receipts) == 1
    assert {item.report_id for item in result.final_reading.report_assessments} == {
        "R0001",
        "R0002",
        "R0003",
    }
    assert any(".s1" in item.batch_id for item in result.call_receipts)
    assert any(".s2" in item.batch_id for item in result.call_receipts)


def test_typed_authority_projection_separates_body_action_and_scoped_entry() -> None:
    report_root = PROJECT_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"
    closure = build_artifact_closure(report_root, "0053")
    inspection = next(
        item
        for item in closure.artifacts
        if item.role == ArtifactRole.INSPECTION_EQUIVALENT_FACTS
    )
    payload = json.loads(inspection.content)
    typed = payload["judge_typed_semantics"]
    pump_state = next(
        item
        for item in typed["state_carriers"]
        if str(item["state_id"]).endswith(".PumpState")
    )
    initial_refs = {item["transition_ref"] for item in typed["initial_entries"]}
    runtime_refs = {item["transition_ref"] for item in typed["runtime_transitions"]}

    assert pump_state["body_lines"]
    assert pump_state["lifecycle_actions"] == []
    assert pump_state["body_lines_are_executable"] is False
    assert initial_refs.isdisjoint(runtime_refs)
    assert all(item["requires_owner_active"] for item in typed["initial_entries"])
    assert all(not item["runtime_continuation"] for item in typed["initial_entries"])
    assert typed["containment_implies_runtime_reachability"] is False
    assert typed["child_initial_requires_owner_entry"] is True


def test_public_runtime_reuses_one_process_local_transport_model() -> None:
    runtime = PublicStructuredRuntime.__new__(PublicStructuredRuntime)
    runtime.profile = "fixture"
    runtime.config = SimpleNamespace(adapter="openai")
    runtime.transport_retries = 1
    runtime.transport_retry_delays = (0.1,)
    runtime.streaming = True
    transport_model = object()
    runtime._transport_model = transport_model

    app = runtime._app(
        "fixture",
        build_exact_validity_batch_model(
            build_validity_batch_input(
                minimal_input(), ("R0001",), batch_id="VB-transport"
            )
        ),
        VALIDITY_SYSTEM_PROMPT,
        streaming=True,
    )

    assert app.model is transport_model


def test_public_runtime_owns_one_loop_and_closes_its_async_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class LifecycleResponse(structured_runtime.BaseModel):
        """Minimal structured response for event-loop lifecycle testing."""

        value: str = structured_runtime.Field(
            min_length=1, description="Fixture response value."
        )

    construction_loops: list[int] = []
    call_loops: list[int] = []
    close_loops: list[int] = []
    sync_closes: list[bool] = []
    timeout_values: list[object] = []

    class AsyncClient:
        async def close(self) -> None:
            close_loops.append(id(asyncio.get_running_loop()))

    class SyncClient:
        def close(self) -> None:
            sync_closes.append(True)

    transport_model = SimpleNamespace(
        root_async_client=AsyncClient(),
        root_client=SyncClient(),
    )

    config = SimpleNamespace(
        adapter="openai",
        context_window_tokens=272_000,
        max_output_tokens=128_000,
        pricing=None,
    )

    class Registry:
        def require(self, _profile: str):
            return config

    class FakeAgentApp:
        def __init__(self, spec, app_config, model, *, profile: str) -> None:
            self.spec = spec
            self.config = app_config
            self.model = model
            self.profile = profile

        @classmethod
        def from_registry(
            cls,
            spec,
            registry,
            *,
            profile: str,
            model_options: dict,
        ):
            construction_loops.append(id(asyncio.get_running_loop()))
            timeout_values.append(model_options["timeout"])
            return cls(spec, registry.require(profile), transport_model, profile=profile)

        def run(self, *_args, **_kwargs):
            raise AssertionError("cell execution must not call AgentApp.run()")

        async def arun(self, _prompt: str, **_options):
            call_loops.append(id(asyncio.get_running_loop()))
            output = self.spec.output_schema(value="ok")
            return SimpleNamespace(
                status="success",
                output=output,
                error=None,
                usage=[],
                to_dict=lambda: {
                    "status": "success",
                    "output": output.model_dump(mode="json"),
                    "error": None,
                    "usage": [],
                },
            )

    monkeypatch.setattr(structured_runtime, "load_llm_registry", Registry)
    monkeypatch.setattr(structured_runtime, "AgentApp", FakeAgentApp)
    runtime = PublicStructuredRuntime(
        "fixture",
        tmp_path,
        transport_retries=0,
        streaming=True,
    )
    try:
        outcomes = tuple(
            runtime.call(
                kind="lifecycle_fixture",
                schema=LifecycleResponse,
                system_prompt="Fixture system prompt.",
                prompt=f"Fixture prompt {index}.",
                artifact_id=f"lifecycle-{index}",
                retry_cell_on_provider_error=False,
            )
            for index in range(3)
        )
    finally:
        runtime.close()

    assert all(outcome.succeeded for outcome in outcomes)
    assert len(construction_loops) == 1
    assert len(call_loops) == 3
    assert set(construction_loops + call_loops + close_loops) == {
        construction_loops[0]
    }
    assert sync_closes == [True]
    assert not runtime._event_loop_thread.is_alive()
    with pytest.raises(TypeError):
        hash(timeout_values[0])


def test_process_worker_close_delegates_to_public_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    closed: list[bool] = []
    runtime = SimpleNamespace(close=lambda: closed.append(True))
    monkeypatch.setattr(judge_execution, "_WORKER_RUNTIME", runtime)

    judge_execution._close_worker_runtime()

    assert closed == [True]
    assert judge_execution._WORKER_RUNTIME is None


def test_api_connection_setup_retry_is_short_but_rate_limit_backoff_is_not(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Ledger:
        def reserve(self, _count: int) -> None:
            return None

    delays: list[float] = []
    monkeypatch.setattr(agent_runtime.time, "sleep", delays.append)
    scheduled = []
    middleware = agent_runtime._TransportRetryMiddleware(
        Ledger(), delays=(5.0,), on_retry=scheduled.append
    )
    APIConnectionError = type("APIConnectionError", (Exception,), {})
    attempts = 0

    def connection_handler(_request):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise APIConnectionError("Connection error.")
        return "recovered"

    assert middleware.wrap_model_call(object(), connection_handler) == "recovered"
    assert delays == [0.1]
    assert scheduled[0]["retry_delay_policy"] == ("immediate_connection_setup_recovery")

    delays.clear()
    scheduled.clear()
    RateLimitError = type("RateLimitError", (Exception,), {})
    rate_error = RateLimitError("rate limit")
    rate_error.status_code = 429
    attempts = 0

    def rate_handler(_request):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise rate_error
        return "recovered"

    assert middleware.wrap_model_call(object(), rate_handler) == "recovered"
    assert delays == [5.0]
    assert scheduled[0]["retry_delay_policy"] == "configured_transport_backoff"


def test_spawn_process_probe_overlaps_and_isolates_artifacts(tmp_path: Path) -> None:
    audit = run_provider_free_process_probe(
        tmp_path, workers=4, call_count=4, delay_seconds=0.2
    )

    assert audit.maximum_overlap >= 3
    assert len({item.process_id for item in audit.intervals}) >= 3
    paths = [Path(item.artifact_path) for item in audit.intervals]
    assert len(paths) == len(set(paths)) == 4
    assert all(path.is_file() for path in paths)
    for interval, path in zip(audit.intervals, paths, strict=True):
        persisted = json.loads(path.read_text(encoding="utf-8"))
        assert persisted == {
            "call_id": interval.call_id,
            "process_id": interval.process_id,
        }


def test_semantic_judge_production_modules_do_not_import_inspect() -> None:
    module_root = Path(__file__).resolve().parents[1]
    for path in module_root.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "import inspect" not in source
        assert "from inspect import" not in source
