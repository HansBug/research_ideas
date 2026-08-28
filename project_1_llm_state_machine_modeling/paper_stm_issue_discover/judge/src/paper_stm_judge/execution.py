"""Process-isolated bounded execution for semantic-Judge batch calls."""

from __future__ import annotations

import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from multiprocessing.util import Finalize
from pathlib import Path
from time import monotonic, sleep
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self
from utils.llm import load_llm_registry

from utils.structured_runtime import (
    PublicStructuredRuntime,
    StructuredCallOutcome,
)

from .models import RelationBatchJudgeInput, ValidityBatchJudgeInput
from .schema import (
    build_exact_relation_batch_model,
    build_exact_validity_batch_model,
)


class BatchSchemaRecipe(BaseModel):
    """Serializable recipe for rebuilding one dynamic exact batch schema."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["validity_batch", "relation_batch"] = Field(
        description="Dynamic schema family rebuilt inside the process-local worker."
    )
    input: dict[str, Any] = Field(
        description="Complete validated batch input serialized as JSON-compatible data."
    )


class ProcessCallTask(BaseModel):
    """Serializable public-runtime call submitted to one isolated worker process."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_recipe: BatchSchemaRecipe = Field(
        description="Recipe used to reconstruct the exact response schema without pickling a dynamic class."
    )
    kind: str = Field(
        min_length=1, description="Public structured runtime operation kind."
    )
    system_prompt: str = Field(
        min_length=1, description="Exact frozen system prompt for this batch call."
    )
    prompt: str = Field(
        min_length=1, description="Exact serialized user prompt for this batch call."
    )
    artifact_id: str = Field(
        min_length=1,
        description="Stable parent-relative artifact identity unique to this batch, stage, and reading.",
    )
    retry_cell_on_provider_error: bool = Field(
        description="Whether the public runtime may repeat the same cell after a terminal provider error."
    )
    streaming: bool | None = Field(
        default=None, description="Optional per-call streaming override."
    )
    max_output_tokens: int = Field(
        gt=0, description="Bounded structured output budget for this batch call."
    )


class ProcessCallResult(BaseModel):
    """Serializable worker result with auditable process and wall-clock metadata."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    outcome: dict[str, Any] = Field(
        description="Complete JSON-compatible PublicStructuredRuntime outcome."
    )
    process_id: int = Field(
        gt=0, description="Operating-system process ID that owned this provider call."
    )
    started_at_utc: str = Field(
        min_length=1, description="UTC timestamp immediately before the runtime call."
    )
    ended_at_utc: str = Field(
        min_length=1, description="UTC timestamp immediately after the runtime call."
    )
    duration_seconds: float = Field(
        ge=0,
        description="Monotonic elapsed seconds for this complete logical batch call.",
    )
    worker_artifact_id: str = Field(
        min_length=1,
        description="Process-qualified artifact identity used by the public runtime.",
    )


class ConcurrencyProbeInterval(BaseModel):
    """One provider-free process interval and its isolated artifact receipt."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    call_id: str = Field(
        min_length=1, description="Stable provider-free probe call identity."
    )
    process_id: int = Field(
        gt=0, description="Worker process that executed this controlled call."
    )
    started_monotonic: float = Field(
        ge=0, description="Worker monotonic start timestamp."
    )
    ended_monotonic: float = Field(ge=0, description="Worker monotonic end timestamp.")
    artifact_path: str = Field(
        min_length=1, description="Unique artifact written only by this probe call."
    )


class ConcurrencyProbeAudit(BaseModel):
    """Provider-free proof of process overlap and artifact-path isolation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    workers: int = Field(
        ge=2, description="Bounded process-worker count used by the probe."
    )
    intervals: tuple[ConcurrencyProbeInterval, ...] = Field(
        min_length=2, description="Complete controlled-call interval closure."
    )
    maximum_overlap: int = Field(
        ge=1, description="Largest number of simultaneously active intervals."
    )
    reason: str = Field(
        min_length=1, description="English explanation of the concurrency result."
    )
    basis: str = Field(
        min_length=1,
        description="Spawn process pool, monotonic intervals, process IDs, and unique artifact paths.",
    )


_WORKER_RUNTIME: PublicStructuredRuntime | None = None
_WORKER_RUNTIME_FINALIZER: Finalize | None = None


def _close_worker_runtime() -> None:
    """Close the process-local async client before the pool worker exits."""

    global _WORKER_RUNTIME
    if _WORKER_RUNTIME is not None:
        _WORKER_RUNTIME.close()
        _WORKER_RUNTIME = None


def _initialize_worker(
    profile: str,
    artifact_root: str,
    transport_retries: int,
    streaming: bool,
) -> None:
    """Create one persistent public runtime and transport per worker process."""

    global _WORKER_RUNTIME, _WORKER_RUNTIME_FINALIZER
    process_root = Path(artifact_root) / "workers" / f"pid-{os.getpid()}"
    _WORKER_RUNTIME = PublicStructuredRuntime(
        profile,
        process_root,
        transport_retries=transport_retries,
        streaming=streaming,
    )
    _WORKER_RUNTIME_FINALIZER = Finalize(
        _WORKER_RUNTIME,
        _close_worker_runtime,
        exitpriority=10,
    )


def _schema_from_recipe(recipe: BatchSchemaRecipe) -> type[BaseModel]:
    """Rebuild a dynamic exact batch schema from validated static input data."""

    if recipe.kind == "validity_batch":
        batch_input = ValidityBatchJudgeInput.model_validate(recipe.input)
        return build_exact_validity_batch_model(batch_input)
    batch_input = RelationBatchJudgeInput.model_validate(recipe.input)
    return build_exact_relation_batch_model(batch_input)


def _run_process_call(task_payload: dict[str, Any]) -> dict[str, Any]:
    """Execute one call using only process-local runtime state and artifacts."""

    if _WORKER_RUNTIME is None:
        raise RuntimeError("semantic Judge process worker was not initialized")
    task = ProcessCallTask.model_validate(task_payload)
    schema = _schema_from_recipe(task.schema_recipe)
    started_at = datetime.now(timezone.utc)
    started = monotonic()
    worker_artifact_id = task.artifact_id
    outcome = _WORKER_RUNTIME.call(
        kind=task.kind,
        schema=schema,
        system_prompt=task.system_prompt,
        prompt=task.prompt,
        artifact_id=worker_artifact_id,
        retry_cell_on_provider_error=task.retry_cell_on_provider_error,
        streaming=task.streaming,
        max_output_tokens=task.max_output_tokens,
    )
    ended = monotonic()
    ended_at = datetime.now(timezone.utc)
    return ProcessCallResult(
        outcome=outcome.to_dict(),
        process_id=os.getpid(),
        started_at_utc=started_at.isoformat(),
        ended_at_utc=ended_at.isoformat(),
        duration_seconds=ended - started,
        worker_artifact_id=worker_artifact_id,
    ).model_dump(mode="json")


def _run_concurrency_probe_call(payload: dict[str, Any]) -> dict[str, Any]:
    """Run one controlled provider-free delay and persist an isolated receipt."""

    call_id = str(payload["call_id"])
    delay_seconds = float(payload["delay_seconds"])
    artifact_root = Path(str(payload["artifact_root"]))
    process_id = os.getpid()
    artifact_path = artifact_root / f"pid-{process_id}" / f"{call_id}.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    started = monotonic()
    sleep(delay_seconds)
    ended = monotonic()
    artifact_path.write_text(
        f'{{"call_id":"{call_id}","process_id":{process_id}}}\n',
        encoding="utf-8",
    )
    return ConcurrencyProbeInterval(
        call_id=call_id,
        process_id=process_id,
        started_monotonic=started,
        ended_monotonic=ended,
        artifact_path=str(artifact_path),
    ).model_dump(mode="json")


def run_provider_free_process_probe(
    artifact_root: Path,
    *,
    workers: int = 4,
    call_count: int = 4,
    delay_seconds: float = 0.2,
) -> ConcurrencyProbeAudit:
    """Prove real spawn-process overlap without loading a profile or provider."""

    if workers < 2 or call_count < 2 or delay_seconds <= 0:
        raise ValueError(
            "concurrency probe requires at least two workers/calls and a positive delay"
        )
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=workers, mp_context=context) as executor:
        futures = tuple(
            executor.submit(
                _run_concurrency_probe_call,
                {
                    "call_id": f"probe-{index}",
                    "delay_seconds": delay_seconds,
                    "artifact_root": str(artifact_root),
                },
            )
            for index in range(1, call_count + 1)
        )
        intervals = tuple(
            ConcurrencyProbeInterval.model_validate(future.result())
            for future in futures
        )
    points = sorted(
        [(item.started_monotonic, 1) for item in intervals]
        + [(item.ended_monotonic, -1) for item in intervals],
        key=lambda item: (item[0], -item[1]),
    )
    active = 0
    maximum_overlap = 0
    for _timestamp, delta in points:
        active += delta
        maximum_overlap = max(maximum_overlap, active)
    return ConcurrencyProbeAudit(
        workers=workers,
        intervals=intervals,
        maximum_overlap=maximum_overlap,
        reason=(
            f"{maximum_overlap} controlled provider-free calls overlapped across "
            f"{len({item.process_id for item in intervals})} worker processes."
        ),
        basis="spawn ProcessPoolExecutor; monotonic intervals; process-qualified unique JSON artifacts",
    )


class ProcessStructuredRuntime:
    """Thread-safe parent dispatcher backed by isolated persistent worker runtimes."""

    real_llm = True

    def __init__(
        self,
        profile: str,
        artifact_root: Path,
        *,
        workers: int,
        transport_retries: int,
        streaming: bool,
    ) -> None:
        if workers < 1:
            raise ValueError("workers must be positive")
        self.profile = profile
        self.artifact_root = artifact_root
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        self.config = load_llm_registry().require(profile)
        self.workers = workers
        context = multiprocessing.get_context("spawn")
        self._executor = ProcessPoolExecutor(
            max_workers=workers,
            mp_context=context,
            initializer=_initialize_worker,
            initargs=(
                profile,
                str(self.artifact_root),
                transport_retries,
                streaming,
            ),
        )

    @staticmethod
    def _task_from_call(call: dict[str, Any]) -> ProcessCallTask:
        schema = call["schema"]
        recipe_payload = getattr(schema, "__semantic_judge_recipe__", None)
        if recipe_payload is None:
            raise TypeError(
                "process execution requires a dynamic semantic-Judge batch schema recipe"
            )
        return ProcessCallTask(
            schema_recipe=BatchSchemaRecipe.model_validate(recipe_payload),
            kind=call["kind"],
            system_prompt=call["system_prompt"],
            prompt=call["prompt"],
            artifact_id=call["artifact_id"],
            retry_cell_on_provider_error=call.get("retry_cell_on_provider_error", True),
            streaming=call.get("streaming"),
            max_output_tokens=call["max_output_tokens"],
        )

    @staticmethod
    def _restore_outcome(
        raw: dict[str, Any], schema: type[BaseModel]
    ) -> StructuredCallOutcome[Any]:
        result = ProcessCallResult.model_validate(raw)
        outcome = StructuredCallOutcome[Any].model_validate(result.outcome)
        response = (
            schema.model_validate(outcome.response)
            if outcome.response is not None
            else None
        )
        dispatch = {
            "process_id": result.process_id,
            "started_at_utc": result.started_at_utc,
            "ended_at_utc": result.ended_at_utc,
            "duration_seconds": result.duration_seconds,
            "worker_artifact_id": result.worker_artifact_id,
        }
        return outcome.model_copy(
            update={
                "response": response,
                "result": {**outcome.result, "dispatch": dispatch},
            }
        )

    def call_many(
        self, calls: tuple[dict[str, Any], ...]
    ) -> tuple[StructuredCallOutcome[Any], ...]:
        """Submit all independent calls before waiting, preserving input order."""

        tasks = tuple(self._task_from_call(call) for call in calls)
        futures = tuple(
            self._executor.submit(_run_process_call, task.model_dump(mode="json"))
            for task in tasks
        )
        return tuple(
            self._restore_outcome(future.result(), call["schema"])
            for future, call in zip(futures, calls, strict=True)
        )

    def call(self, **call: Any) -> StructuredCallOutcome[Any]:
        """Compatibility path for one batch call through the same process pool."""

        return self.call_many((call,))[0]

    def close(self) -> None:
        """Wait for submitted calls and release all worker processes."""

        self._executor.shutdown(wait=True, cancel_futures=False)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()
