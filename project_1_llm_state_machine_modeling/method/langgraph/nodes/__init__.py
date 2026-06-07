"""LG-M1-D3 node registration helpers for the default LangGraph runtime."""

from method.langgraph.nodes.sc import SC_NODE_IDS, register_sc_nodes
from method.langgraph.nodes.sd import SD_NODE_IDS, register_sd_nodes
from method.langgraph.nodes.sl import SL_NODE_IDS, register_sl_nodes

__all__ = [
    "SC_NODE_IDS",
    "SD_NODE_IDS",
    "SL_NODE_IDS",
    "register_sc_nodes",
    "register_sd_nodes",
    "register_sl_nodes",
]
