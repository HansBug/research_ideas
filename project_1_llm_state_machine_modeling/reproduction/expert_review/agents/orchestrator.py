from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from ..schemas.graph_state import ReviewGraphState


PREPARATION_FANOUT = (
    "Input Analyst",
    "Prediction Extractor",
    "Reference Extractor",
)

ANALYSIS_FANOUT = (
    "Traceability Agent",
    "Equivalence and Difference Agent",
    "Pragmatic Quality Agent",
)

FINAL_FANIN = (
    "Missing-Evidence Critic",
    "Disagreement Arbiter",
    "Score Composer",
    "Final Synthesizer",
)


def record_agent_context(
    state: ReviewGraphState,
    agent_name: str,
    *,
    context_keys: list[str],
    summary: str,
) -> None:
    state.context_packets[agent_name] = {
        "context_keys": list(context_keys),
        "summary": summary,
    }


def record_fanout(state: ReviewGraphState, stage_name: str, agents: tuple[str, ...]) -> None:
    state.fanout_log.append(f"{stage_name}: " + " -> ".join(agents))


def run_parallel(
    tasks: dict[str, Callable[[], Any]],
    *,
    max_workers: int | None = None,
) -> dict[str, Any]:
    if not tasks:
        return {}
    worker_count = max_workers or len(tasks)
    results: dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {executor.submit(func): name for name, func in tasks.items()}
        for future, name in list(future_map.items()):
            results[name] = future.result()
    return results


__all__ = [
    "ANALYSIS_FANOUT",
    "FINAL_FANIN",
    "PREPARATION_FANOUT",
    "record_agent_context",
    "record_fanout",
    "run_parallel",
]
