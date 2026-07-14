from __future__ import annotations

from pathlib import Path

import pytest

from utils.agent import AgentSpec
from utils.agent.runtime import (
    _build_context_manifest,
    _normalize_context,
    _validate_model_options,
)
from utils.llm import LLMConfig


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


def test_model_call_options_cannot_change_tool_or_retry_contract() -> None:
    from utils.agent.runtime import _validate_model_call_options

    _validate_model_call_options({"temperature": 0})
    for key in ("parallel_tool_calls", "tool_choice", "response_format", "max_retries"):
        with pytest.raises(ValueError, match="model_call_options_not_allowed"):
            _validate_model_call_options({key: True})
    with pytest.raises(ValueError, match="model_call_options_not_allowed"):
        _validate_model_call_options({"reasoning_effort": "high"})


def test_output_symlink_loop_is_a_structured_config_error(tmp_path: Path) -> None:
    from utils.agent.runtime import AgentError, _validate_output_paths

    loop = tmp_path / "loop"
    loop.symlink_to(loop)
    with pytest.raises(AgentError) as error:
        _validate_output_paths(loop, None)
    assert getattr(error.value, "code", None) == "config_error"


def test_agent_spec_tools_are_the_registration_allowlist() -> None:
    def lookup(value: str) -> str:
        return value

    spec = AgentSpec(name="test", system_prompt="use the tool", tools=(lookup,))
    assert spec.tool_names == ("lookup",)


def test_think_off_pins_official_reasoning_defaults() -> None:
    from utils.agent.runtime import _resolve_inference_options

    openai_config = LLMConfig(model="gpt-5.5", base_url="https://api.openai.com/v1")
    options, enabled = _resolve_inference_options(
        openai_config,
        model_call_options=None,
        think_mode=False,
        reasoning_effort=None,
    )
    assert enabled is False
    assert options["reasoning_effort"] == "none"

    deepseek_config = LLMConfig(model="deepseek-v4-flash", base_url="https://api.deepseek.com")
    options, enabled = _resolve_inference_options(
        deepseek_config,
        model_call_options=None,
        think_mode=False,
        reasoning_effort=None,
    )
    assert enabled is False
    assert options["extra_body"] == {"thinking": {"type": "disabled"}}

    with pytest.raises(ValueError, match="reasoning_effort requires think_mode=True"):
        _resolve_inference_options(
            openai_config,
            model_call_options={"reasoning_effort": "medium"},
            think_mode=False,
            reasoning_effort=None,
        )


def test_deepseek_profiles_use_the_official_langchain_adapter() -> None:
    from utils.agent import AgentApp

    app = AgentApp.from_config(
        AgentSpec(name="deepseek", system_prompt="answer"),
        LLMConfig(model="deepseek-v4-flash", base_url="https://api.deepseek.com", api_key="test-key"),
        profile="deepseek-v4-flash",
    )
    assert type(app.model).__module__.split(".", 1)[0] == "langchain_deepseek"
    assert app.adapter_name == "langchain-deepseek/chat-completions"
    assert app.model.streaming is True
    from utils.agent.runtime import _model_capacity

    context, max_output, safe_input, sources = _model_capacity(app.model, app.config)
    assert context == 1_000_000
    assert max_output == 384_000
    assert safe_input == 1_000_000
    assert sources == {"context_window": "official_profile", "max_output": "official_profile"}


def test_dependency_versions_record_both_provider_adapters() -> None:
    from utils.agent.runtime import _dependency_versions

    versions = _dependency_versions()
    assert "langchain-openai" in versions
    assert "langchain-deepseek" in versions
