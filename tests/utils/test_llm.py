from __future__ import annotations

from pathlib import Path

import pytest

from utils.llm import LLMConfig, LLMRegistry, load_llm_registry


def test_load_registry_keeps_direct_values_and_redacts_public_data(
    tmp_path: Path,
) -> None:
    path = tmp_path / "llm.yml"
    path.write_text(
        """
default: gpt-5.5
profiles:
  gpt-5.5:
    base_url: https://example.invalid/api
    api_key: secret-value
    model: gpt-5.5
    context_window_tokens: 1050000
    max_output_tokens: 128000
""",
        encoding="utf-8",
    )

    registry = load_llm_registry(path)

    assert isinstance(registry, LLMRegistry)
    assert registry.default_name == "gpt-5.5"
    config = registry["gpt-5.5"]
    assert config.api_key is not None
    assert config.api_key.get_secret_value() == "secret-value"
    public = config.public_dict()
    assert "secret-value" not in repr(public)
    assert public["api_key_configured"] is True
    assert public["model"] == "gpt-5.5"


def test_config_rejects_unknown_provider_field() -> None:
    with pytest.raises(ValueError):
        LLMConfig.model_validate({"model": "gpt-5.5", "provider": "openai"})


def test_config_adapter_defaults_to_openai_and_is_public() -> None:
    config = LLMConfig(model="claude-opus-4-7")

    assert config.adapter == "openai"
    assert config.public_dict()["adapter"] == "openai"


def test_stream_usage_profile_override_is_recorded_without_changing_legacy_identity() -> None:
    legacy = LLMConfig(model="local-model")
    explicit = LLMConfig(model="local-model", stream_usage=True)
    assert "stream_usage" not in legacy.public_dict()
    assert explicit.public_dict()["stream_usage"] is True
    assert legacy.fingerprint() != explicit.fingerprint()


def test_config_loads_auditable_token_pricing() -> None:
    config = LLMConfig.model_validate(
        {
            "model": "claude-opus-4-7",
            "pricing": {
                "prices": {
                    "input_usd_per_million_tokens": 5,
                    "output_usd_per_million_tokens": 25,
                    "cache_read_usd_per_million_tokens": 0.5,
                    "cache_write_usd_per_million_tokens": 6.25,
                },
                "source_url": "https://docs.anthropic.com/en/docs/about-claude/pricing",
                "verified_on": "2026-08-18",
                "basis": "official_list_price",
                "scope_note": "Standard-context list price.",
            },
        }
    )

    assert config.pricing is not None
    assert config.pricing.prices.cache_write_usd_per_million_tokens == 6.25
    assert config.public_dict()["pricing"]["verified_on"] == "2026-08-18"


@pytest.mark.parametrize(
    "adapter", ["openai", "openai-responses", "anthropic", "deepseek"]
)
def test_config_accepts_supported_adapters(adapter: str) -> None:
    config = LLMConfig.model_validate({"model": "test-model", "adapter": adapter})

    assert config.adapter == adapter


def test_config_rejects_unknown_adapter() -> None:
    with pytest.raises(ValueError):
        LLMConfig.model_validate({"model": "gpt-5.5", "adapter": "openai-compatible"})


def test_config_rejects_userinfo_in_base_url() -> None:
    with pytest.raises(ValueError, match="userinfo"):
        LLMConfig(model="gpt-5.5", base_url="https://user:password@example.invalid/v1")


def test_public_base_url_reference_contains_only_host_and_port() -> None:
    config = LLMConfig(model="gpt-5.5", base_url="https://example.invalid:8443/v1")
    assert config.public_dict()["base_url_ref"] == "https://example.invalid:8443"


def test_public_base_url_reference_preserves_ipv6_brackets() -> None:
    config = LLMConfig(model="gpt-5.5", base_url="https://[::1]:8443/v1")
    assert config.public_dict()["base_url_ref"] == "https://[::1]:8443"


def test_registry_path_can_be_selected_by_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = tmp_path / "selected.yml"
    path.write_text(
        "default: local\nprofiles:\n  local:\n    model: local-model\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("LLM_CONFIG_FILE", str(path))

    assert load_llm_registry().default.model == "local-model"


def test_missing_api_key_is_not_filled_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-be-read")
    config = LLMConfig(model="gpt-5.5")
    assert config.api_key is None
