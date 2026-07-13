from __future__ import annotations

from pathlib import Path

import pytest

from utils.agent import AgentSpec
from utils.agent.runtime import (
    _build_context_manifest,
    _normalize_context,
    _validate_model_options,
)


def test_context_hash_is_verified_and_manifest_is_stable() -> None:
    pages = _normalize_context(
        [{"id": "r1", "snapshot": "s1", "text": "事实"}],
    )
    manifest = _build_context_manifest(pages)
    assert pages[0]["hash"].startswith("sha256:")
    assert manifest.startswith("sha256:")


def test_context_hash_mismatch_fails_closed() -> None:
    with pytest.raises(ValueError, match="context_hash_mismatch"):
        _normalize_context([{"id": "r1", "hash": "sha256:deadbeef", "text": "事实"}])


def test_model_options_have_a_small_explicit_allowlist() -> None:
    _validate_model_options({"streaming": True, "timeout": 10})
    with pytest.raises(ValueError, match="model_options_not_allowed"):
        _validate_model_options({"model": "other"})
    with pytest.raises(ValueError, match="model_options_not_allowed"):
        _validate_model_options({"api_key": "secret"})


def test_agent_spec_tools_are_the_registration_allowlist() -> None:
    def lookup(value: str) -> str:
        return value

    spec = AgentSpec(name="test", system_prompt="use the tool", tools=(lookup,))
    assert spec.tool_names == ("lookup",)
