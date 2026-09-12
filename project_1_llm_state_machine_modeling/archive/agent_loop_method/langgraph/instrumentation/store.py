"""LangGraph Store helpers for transient runtime objects."""

from __future__ import annotations

import uuid
from typing import Any, TypedDict

from langgraph.config import get_store
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore

from archive.agent_loop_method.langgraph.instrumentation.common import _package_version

def langgraph_store_compat_smoke() -> dict[str, Any]:
    """Run a focused LangGraph Store smoke for LG-A2 transient object storage.

    LG-A2 relies on ``StateGraph.compile(store=...)`` and node-local
    ``get_store()`` rather than a module-level Python dict.  This smoke is kept
    separate from the generic checkpoint smoke so CI can fail fast if the
    installed LangGraph version changes Store APIs in a way that would make
    transient validation objects disappear between nodes.
    """

    result: dict[str, Any] = {
        "ok": False,
        "langgraph_version": _package_version("langgraph"),
        "inmemory_store_ok": False,
        "namespace_isolation_ok": False,
        "compile_store_ok": False,
        "get_store_ok": False,
        "delete_ok": False,
    }
    try:
        store = InMemoryStore()
        ns_a = ("lg-a2-store-smoke", "a")
        ns_b = ("lg-a2-store-smoke", "b")
        store.put(ns_a, "same-key", {"value": 1})
        store.put(ns_b, "same-key", {"value": 2})
        item_a = store.get(ns_a, "same-key")
        item_b = store.get(ns_b, "same-key")
        result["inmemory_store_ok"] = bool(item_a and item_a.value == {"value": 1})
        result["namespace_isolation_ok"] = bool(item_b and item_b.value == {"value": 2})
        store.delete(ns_a, "same-key")
        result["delete_ok"] = store.get(ns_a, "same-key") is None and store.get(ns_b, "same-key") is not None

        class _StoreSmokeState(TypedDict, total=False):
            value: int

        graph = StateGraph(_StoreSmokeState)

        def node(state: _StoreSmokeState) -> _StoreSmokeState:
            active_store = get_store()
            active_store.put(("lg-a2-store-smoke", "node"), "value", {"value": int(state.get("value", 0)) + 1})
            item = active_store.get(("lg-a2-store-smoke", "node"), "value")
            return {"value": int((item.value if item is not None else {}).get("value", 0))}

        graph.add_node("store_node", node)
        graph.add_edge(START, "store_node")
        graph.add_edge("store_node", END)
        app = graph.compile(store=store)
        result["compile_store_ok"] = True
        output = app.invoke({"value": 41})
        result["get_store_ok"] = output.get("value") == 42 and store.get(("lg-a2-store-smoke", "node"), "value") is not None
        result["ok"] = all(
            bool(result[key])
            for key in ("inmemory_store_ok", "namespace_isolation_ok", "compile_store_ok", "get_store_ok", "delete_ok")
        )
    except Exception as exc:  # pragma: no cover - returned payload is enough for callers/tests.
        result["error"] = f"{type(exc).__name__}: {str(exc)[:300]}"
    return result

def _transient_namespace(run_id: str) -> tuple[str, str]:
    return ("transient", run_id)

def _transient_namespace_label(run_id: str) -> str:
    return f"transient/{run_id}"

def _put_transient(run_id: str, kind: str, iteration: int, value: Any, *, lifecycle: dict[str, Any] | None = None) -> str:
    """Store a transient object inside the active LangGraph Store context.

    This helper must only be called from compiled LangGraph nodes, because it
    depends on ``langgraph.config.get_store()`` being available in the current
    runnable context.  It deliberately does not write the historical module
    level ``_TRANSIENT_OBJECTS`` dict.
    """

    key = f"{kind}:{iteration}:{uuid.uuid4().hex[:8]}"
    get_store().put(
        _transient_namespace(run_id),
        key,
        {
            "_transient_wrapper": True,
            "object": value,
            "kind": kind,
            "iteration": iteration,
            "object_type": type(value).__name__,
            "run_id": run_id,
        },
    )
    if lifecycle is not None:
        lifecycle["put_count"] = int(lifecycle.get("put_count", 0)) + 1
    return key

def _get_transient(run_id: str, key: str, *, lifecycle: dict[str, Any] | None = None) -> Any:
    """Load a transient object from the active LangGraph Store context."""

    item = get_store().get(_transient_namespace(run_id), key)
    if item is None:
        raise KeyError(f"missing transient LangGraph runtime object: {key}")
    if lifecycle is not None:
        lifecycle["get_count"] = int(lifecycle.get("get_count", 0)) + 1
    value = item.value
    if isinstance(value, dict) and value.get("_transient_wrapper") is True and "object" in value:
        return value["object"]
    return value

def _drop_transient(run_id: str | None, key: str | None, *, lifecycle: dict[str, Any] | None = None) -> None:
    """Delete a transient Store object if it exists in the active graph node."""

    if key:
        try:
            namespace = _transient_namespace(str(run_id or ""))
            existed = get_store().get(namespace, key) is not None
            get_store().delete(namespace, key)
            if lifecycle is not None and existed:
                lifecycle["drop_count"] = int(lifecycle.get("drop_count", 0)) + 1
        except Exception as exc:
            if lifecycle is not None:
                lifecycle.setdefault("cleanup_errors", []).append(f"drop:{type(exc).__name__}:{str(exc)[:160]}")

def _drain_transients(run_id: str, *, lifecycle: dict[str, Any] | None = None) -> dict[str, Any]:
    """Final-drain all transient items in this run's Store namespace."""

    namespace = _transient_namespace(run_id)
    items = list(get_store().search(namespace))
    deleted = 0
    for item in items:
        get_store().delete(namespace, item.key)
        deleted += 1
    remaining = list(get_store().search(namespace))
    cleanup_status = "no_leak" if not remaining else f"partial_leak_{len(remaining)}_items"
    if lifecycle is not None:
        lifecycle["final_drain_count"] = int(lifecycle.get("final_drain_count", 0)) + 1
        lifecycle["final_item_count"] = len(remaining)
        lifecycle["cleanup_status"] = cleanup_status
        lifecycle["drained_item_count"] = int(lifecycle.get("drained_item_count", 0)) + deleted
    return {
        "drained_count": deleted,
        "final_item_count": len(remaining),
        "cleanup_status": cleanup_status,
    }

