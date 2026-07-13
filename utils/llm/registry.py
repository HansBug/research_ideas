from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from .config import LLMConfig


class LLMRegistry(Mapping[str, LLMConfig]):
    def __init__(self, profiles: Mapping[str, LLMConfig], default_name: str):
        if not profiles:
            raise ValueError("config_error: profiles must not be empty")
        if default_name not in profiles:
            raise ValueError(f"config_error: default profile not found: {default_name}")
        self._profiles = MappingProxyType(dict(profiles))
        self.default_name = default_name

    def __getitem__(self, name: str) -> LLMConfig:
        return self._profiles[name]

    def __iter__(self) -> Iterator[str]:
        return iter(self._profiles)

    def __len__(self) -> int:
        return len(self._profiles)

    @property
    def configs(self) -> Mapping[str, LLMConfig]:
        return self._profiles

    @property
    def default(self) -> LLMConfig:
        return self[self.default_name]

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._profiles))

    def require(self, name: str) -> LLMConfig:
        try:
            return self[name]
        except KeyError as exc:
            raise ValueError(f"config_error: profile not found: {name}") from exc

    def public_summary(self, name: str | None = None) -> dict[str, Any]:
        config = self.default if name is None else self.require(name)
        summary = config.public_dict()
        summary["profile"] = self.default_name if name is None else name
        summary["fingerprint"] = config.fingerprint()
        return summary


def _repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def resolve_config_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path).expanduser().resolve()
    if env_path := os.environ.get("LLM_CONFIG_FILE"):
        return Path(env_path).expanduser().resolve()
    return _repo_root() / ".llmconfig.yml"


def load_llm_registry(path: str | Path | None = None) -> LLMRegistry:
    config_path = resolve_config_path(path)
    if not config_path.is_file():
        raise ValueError(f"config_error: file not found: {config_path}")
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"config_error: invalid YAML: {config_path}") from exc
    if not isinstance(raw, Mapping):
        raise ValueError("config_error: top-level YAML value must be a mapping")
    default_name = raw.get("default")
    profiles_raw = raw.get("profiles")
    if not isinstance(default_name, str) or not default_name.strip():
        raise ValueError("config_error: default must be a non-empty profile name")
    if not isinstance(profiles_raw, Mapping):
        raise ValueError("config_error: profiles must be a mapping")
    profiles: dict[str, LLMConfig] = {}
    for name, values in profiles_raw.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("config_error: profile names must be non-empty strings")
        if not isinstance(values, Mapping):
            raise ValueError(f"config_error: profile must be a mapping: {name}")
        try:
            profiles[name] = LLMConfig.model_validate(dict(values))
        except Exception as exc:
            raise ValueError(f"config_error: invalid profile: {name}") from exc
    return LLMRegistry(profiles, default_name.strip())
