from __future__ import annotations

import hashlib
import json
from typing import Any, Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator


class LLMConfig(BaseModel):
    """One direct-value connection profile.

    The loader is intentionally permissive about omitted optional values, while the
    agent runtime refuses to silently source credentials from the environment.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    adapter: Literal["openai", "anthropic", "deepseek"] = "openai"
    base_url: str | None = None
    api_key: SecretStr | None = None
    model: str = Field(min_length=1)
    context_window_tokens: int | None = Field(default=None, gt=0)
    max_output_tokens: int | None = Field(default=None, gt=0)

    @field_validator("model", mode="before")
    @classmethod
    def _strip_model(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()
        return value

    @field_validator("base_url", mode="before")
    @classmethod
    def _normalize_base_url(cls, value: Any) -> Any:
        if value is None:
            return None
        if not isinstance(value, str):
            return value
        value = value.strip()
        if not value:
            return None
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute http(s) URL")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("base_url must not contain userinfo")
        try:
            parsed.port
        except ValueError as exc:
            raise ValueError("base_url must contain a valid port") from exc
        return value.rstrip("/")

    @field_validator("api_key", mode="before")
    @classmethod
    def _reject_empty_key(cls, value: Any) -> Any:
        if value is None or isinstance(value, SecretStr):
            return value
        if isinstance(value, str) and value.strip():
            return value
        if value == "":
            return None
        return value

    @model_validator(mode="after")
    def _check_token_bounds(self) -> "LLMConfig":
        if (
            self.context_window_tokens is not None
            and self.max_output_tokens is not None
            and self.context_window_tokens < self.max_output_tokens
        ):
            raise ValueError("context_window_tokens must be >= max_output_tokens")
        return self

    def connection_kwargs(self) -> dict[str, Any]:
        """Return kwargs for the internal model constructor; never log this."""

        values: dict[str, Any] = {"model": self.model}
        if self.base_url is not None:
            values["base_url"] = self.base_url
        if self.api_key is not None:
            values["api_key"] = self.api_key.get_secret_value()
        return values

    def public_dict(self) -> dict[str, Any]:
        endpoint_ref: str | None = None
        if self.base_url:
            parsed = urlsplit(self.base_url)
            # Rebuild from the parsed host rather than echoing ``netloc``.  The
            # validator rejects userinfo, and this remains defensive if a
            # model is constructed through a future deserialization path.
            host = parsed.hostname
            if host:
                port = parsed.port
                display_host = f"[{host}]" if ":" in host else host
                endpoint_ref = f"{parsed.scheme}://{display_host}{f':{port}' if port is not None else ''}"
        return {
            "adapter": self.adapter,
            "model": self.model,
            "base_url_ref": endpoint_ref,
            "api_key_configured": self.api_key is not None,
            "context_window_tokens": self.context_window_tokens,
            "max_output_tokens": self.max_output_tokens,
        }

    def fingerprint(self) -> str:
        payload = json.dumps(self.public_dict(), sort_keys=True, separators=(",", ":"))
        return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
