"""SD deterministic-node registration for LG-M1-D3."""

from __future__ import annotations

from typing import Any, Callable

SD_NODE_IDS = ("validation_pass", "repair_path")


def register_sd_nodes(
    graph: Any,
    *,
    validation_pass: Callable[..., Any],
    repair_path: Callable[..., Any],
) -> None:
    graph.add_node("validation_pass", validation_pass)
    graph.add_node("repair_path", repair_path)


__all__ = ["SD_NODE_IDS", "register_sd_nodes"]
