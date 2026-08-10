from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if hasattr(value, "to_json"):
        try:
            return _jsonable(value.to_json())
        except Exception:
            pass
    if hasattr(value, "model_dump"):
        try:
            return _jsonable(value.model_dump(mode="json"))
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        return {str(k): _jsonable(v) for k, v in vars(value).items() if not str(k).startswith("_")}
    return str(value)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_and_inspect(source: str, path: str = "<memory>") -> tuple[Any, dict[str, Any]]:
    from pyfcstm.diagnostics import inspect_model
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine

    ast = parse_with_grammar_entry(source, "state_machine_dsl")
    model = parse_dsl_node_to_state_machine(ast, path=path)
    return model, _jsonable(inspect_model(model).to_json())


def check_fcstm(source: str, path: str = "<memory>") -> dict[str, Any]:
    try:
        model, inspect = parse_and_inspect(source, path)
    except Exception as exc:
        return {
            "execution_status": "completed",
            "parse_status": "failed",
            "semantic_status": "failed",
            "inspect_status": "not_run",
            "executable": False,
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }
    diagnostics = inspect.get("diagnostics", [])
    return {
        "execution_status": "completed",
        "parse_status": "ok",
        "semantic_status": "ok",
        "inspect_status": "ok",
        "executable": True,
        "diagnostics": diagnostics,
        "inspect": inspect,
        "metrics": inspect.get("metrics", {}),
        "model_sha256": sha256_text(source),
        "model_type": type(model).__name__,
    }


def load_model_for_simulation(source: str, path: str = "<memory>") -> Any:
    return parse_and_inspect(source, path)[0]
