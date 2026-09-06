from __future__ import annotations

import importlib.util
import sys
import types
from dataclasses import dataclass
from typing import Any

import pytest

_STUBBED_MODULES: dict[str, types.ModuleType | None] = {}
_STUB_NAMES = ("utils", "utils.agent", "utils.llm")


@dataclass(frozen=True)
class _AgentSpec:
    name: str
    system_prompt: str
    tools: tuple[Any, ...] = ()
    output_schema: Any = None
    limits: dict[str, int | float] | None = None
    require_tool_call: bool = False
    retry_missing_structured_output: bool = False


class _AgentApp:
    @classmethod
    def from_registry(cls, *_args: Any, **_kwargs: Any) -> "_AgentApp":
        return cls()

    def run(
        self, *_args: Any, **_kwargs: Any
    ) -> Any:  # pragma: no cover - tests monkeypatch this.
        raise NotImplementedError("test AgentApp stub must be monkeypatched before use")


class _LLMRegistry:
    pass


def _load_llm_registry(*_args: Any, **_kwargs: Any) -> _LLMRegistry:
    return _LLMRegistry()


def _has_importable_utils() -> bool:
    try:
        return (
            importlib.util.find_spec("utils.agent") is not None
            and importlib.util.find_spec("utils.llm") is not None
        )
    except ModuleNotFoundError:
        return False


def _install_utils_stubs() -> None:
    if (
        "utils.agent" in sys.modules
        and "utils.llm" in sys.modules
    ) or _has_importable_utils():
        return
    for name in _STUB_NAMES:
        _STUBBED_MODULES.setdefault(name, sys.modules.get(name))
    utils_pkg = sys.modules.get("utils") or types.ModuleType("utils")
    if not hasattr(utils_pkg, "__path__"):
        utils_pkg.__path__ = []  # type: ignore[attr-defined]
    agent_mod = types.ModuleType("utils.agent")
    agent_mod.AgentApp = _AgentApp
    agent_mod.AgentSpec = _AgentSpec
    llm_mod = types.ModuleType("utils.llm")
    llm_mod.LLMRegistry = _LLMRegistry
    llm_mod.load_llm_registry = _load_llm_registry
    sys.modules.update(
        {"utils": utils_pkg, "utils.agent": agent_mod, "utils.llm": llm_mod}
    )


def pytest_configure(config: pytest.Config) -> None:
    _install_utils_stubs()


def pytest_unconfigure(config: pytest.Config) -> None:
    for name in reversed(_STUB_NAMES):
        original = _STUBBED_MODULES.get(name)
        if original is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = original
