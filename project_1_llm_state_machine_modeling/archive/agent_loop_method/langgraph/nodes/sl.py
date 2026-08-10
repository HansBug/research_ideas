"""SL LLM-stage-node registration for LG-M1-D3."""

from __future__ import annotations

from typing import Any, Callable

SL_NODE_IDS = ("sl1_initial_modeling",)


def register_sl_nodes(graph: Any, *, sl1_initial_modeling: Callable[..., Any]) -> None:
    graph.add_node("sl1_initial_modeling", sl1_initial_modeling)


__all__ = ["SL_NODE_IDS", "register_sl_nodes"]
