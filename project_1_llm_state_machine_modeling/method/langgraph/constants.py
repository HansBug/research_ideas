"""Foundation constants for the project_1 LangGraph runtime.

LG-M1-D1 intentionally keeps only runtime/registry identity constants here.
Instrumentation, context-engineering, Send fan-out, ToolNode wrapper, and other
C/E/D2/D3 lane constants remain in ``method.langgraph_runtime`` until their
own focused sub-PRs migrate the corresponding behavior and evidence gates.
"""

from __future__ import annotations

LANGGRAPH_RUNTIME_BACKEND = "langgraph"
GRAPH_RUNTIME_SCHEMA_VERSION = "pr-langgraph.stategraph.v1"
NODE_EDGE_SCHEMA_VERSION = "pr-langgraph.stage-nodes.v1"
GRAPH_RUNTIME_ID = f"{LANGGRAPH_RUNTIME_BACKEND}:{GRAPH_RUNTIME_SCHEMA_VERSION}"

__all__ = [
    "GRAPH_RUNTIME_ID",
    "GRAPH_RUNTIME_SCHEMA_VERSION",
    "LANGGRAPH_RUNTIME_BACKEND",
    "NODE_EDGE_SCHEMA_VERSION",
]
