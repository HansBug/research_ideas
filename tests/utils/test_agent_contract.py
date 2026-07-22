from __future__ import annotations

from pathlib import Path

import pytest

from utils.agent import AgentSpec
from utils.agent.runtime import (
    _build_context_manifest,
    _default_stream_usage,
    _normalize_context,
    _validate_adapter_call_options,
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


def test_anthropic_rejects_openai_only_call_options() -> None:
    config = LLMConfig(model="claude-opus-4-7", adapter="anthropic")

    _validate_adapter_call_options(config, {"temperature": 0, "max_tokens": 100})
    for key in ("seed", "verbosity"):
        with pytest.raises(ValueError, match="adapter=anthropic"):
            _validate_adapter_call_options(config, {key: 1 if key == "seed" else "low"})


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


def test_missing_structured_output_retry_needs_output_schema() -> None:
    with pytest.raises(ValueError, match="retry_missing_structured_output"):
        AgentSpec(
            name="invalid-structured-retry",
            system_prompt="answer",
            retry_missing_structured_output=True,
        )


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

    deepseek_config = LLMConfig(
        model="deepseek-v4-flash",
        adapter="deepseek",
        base_url="https://api.deepseek.com",
    )
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
        LLMConfig(
            model="deepseek-v4-flash",
            adapter="deepseek",
            base_url="https://api.deepseek.com",
            api_key="test-key",
        ),
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


def test_anthropic_profiles_use_the_official_langchain_adapter() -> None:
    from utils.agent import AgentApp

    app = AgentApp.from_config(
        AgentSpec(name="anthropic", system_prompt="answer"),
        LLMConfig(
            model="claude-opus-4-7",
            adapter="anthropic",
            base_url="https://api.anthropic.com",
            api_key="test-key",
            max_output_tokens=128_000,
        ),
        profile="claude-opus-4-7-official",
    )

    assert type(app.model).__module__.split(".", 1)[0] == "langchain_anthropic"
    assert app.adapter_name == "langchain-anthropic/messages"
    assert app.model.streaming is True
    assert app.model.max_tokens == 128_000
    assert app.model.anthropic_api_url == "https://api.anthropic.com"


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        (LLMConfig(model="gpt-5.5"), True),
        (
            LLMConfig(
                model="gpt-5.5",
                adapter="openai",
                base_url="https://relay.example/v1",
            ),
            False,
        ),
        (
            LLMConfig(
                model="claude-opus-4-7",
                adapter="anthropic",
                base_url="https://relay.example",
            ),
            True,
        ),
        (
            LLMConfig(
                model="deepseek-v4-flash",
                adapter="deepseek",
                base_url="https://api.deepseek.com",
            ),
            False,
        ),
    ],
)
def test_stream_usage_default_is_owned_by_the_adapter_runtime(
    config: LLMConfig,
    expected: bool,
) -> None:
    assert _default_stream_usage(config) is expected


def test_explicit_stream_usage_overrides_the_adapter_default() -> None:
    from utils.agent import AgentApp

    app = AgentApp.from_config(
        AgentSpec(name="explicit-stream-usage", system_prompt="answer"),
        LLMConfig(
            model="deepseek-v4-flash",
            adapter="deepseek",
            base_url="https://api.deepseek.com",
            api_key="test-key",
        ),
        model_options={"stream_usage": True},
    )

    assert app.model.stream_usage is True


def test_adapter_default_does_not_infer_from_model_or_endpoint() -> None:
    from utils.agent import AgentApp

    app = AgentApp.from_config(
        AgentSpec(name="explicit-adapter", system_prompt="answer"),
        LLMConfig(
            model="claude-opus-4-7",
            base_url="https://api.anthropic.com",
            api_key="test-key",
        ),
    )

    assert type(app.model).__module__.split(".", 1)[0] == "langchain_openai"
    assert app.adapter_name == "langchain-openai/chat-completions"


def test_dependency_versions_record_all_provider_adapters() -> None:
    from utils.agent.runtime import _dependency_versions

    versions = _dependency_versions()
    assert "langchain-openai" in versions
    assert "langchain-anthropic" in versions
    assert "langchain-deepseek" in versions
    assert "anthropic" in versions
