"""SC control-node registration for LG-M1-D3.

The node closures are still built in ``archive.agent_loop_method.langgraph.core._build_graph`` so
they can close over runtime-local transient store state without a large parameter
object.  This module owns the SC lane node identifiers and physical
``graph.add_node`` registration step.
"""

from __future__ import annotations

from typing import Any, Callable

SC_NODE_IDS = (
    "sc0_start",
    "iteration_gate",
    "validation_decision",
    "repair_decision",
    "waiver_continue",
    "sc12_budget_exhausted",
    "sc13_trace_audit",
)


def register_sc_nodes(
    graph: Any,
    *,
    sc0_start: Callable[..., Any],
    iteration_gate: Callable[..., Any],
    validation_decision: Callable[..., Any],
    repair_decision: Callable[..., Any],
    waiver_continue: Callable[..., Any],
    sc12_budget_exhausted: Callable[..., Any],
    sc13_trace_audit: Callable[..., Any],
) -> None:
    graph.add_node("sc0_start", sc0_start)
    graph.add_node("iteration_gate", iteration_gate)
    graph.add_node("validation_decision", validation_decision)
    graph.add_node("repair_decision", repair_decision)
    graph.add_node("waiver_continue", waiver_continue)
    graph.add_node("sc12_budget_exhausted", sc12_budget_exhausted)
    graph.add_node("sc13_trace_audit", sc13_trace_audit)


__all__ = ["SC_NODE_IDS", "register_sc_nodes"]
