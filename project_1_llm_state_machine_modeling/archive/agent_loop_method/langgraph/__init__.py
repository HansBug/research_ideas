"""LangGraph foundation package for project_1 agent-loop runtime.

LG-M1-D1 exposes only low-risk foundation objects here.  The public runtime
compatibility facade remains ``archive.agent_loop_method.langgraph_runtime``.
"""

from __future__ import annotations

from archive.agent_loop_method.langgraph.constants import (
    GRAPH_RUNTIME_ID,
    GRAPH_RUNTIME_SCHEMA_VERSION,
    LANGGRAPH_RUNTIME_BACKEND,
    NODE_EDGE_SCHEMA_VERSION,
)
from archive.agent_loop_method.langgraph.registry import build_langgraph_node_registry, canonical_stage_ids, graph_registry_consistency
from archive.agent_loop_method.langgraph.state import CompatState, _CompatState

__all__ = [
    "CompatState",
    "GRAPH_RUNTIME_ID",
    "GRAPH_RUNTIME_SCHEMA_VERSION",
    "LANGGRAPH_RUNTIME_BACKEND",
    "NODE_EDGE_SCHEMA_VERSION",
    "_CompatState",
    "build_langgraph_node_registry",
    "canonical_stage_ids",
    "graph_registry_consistency",
]
