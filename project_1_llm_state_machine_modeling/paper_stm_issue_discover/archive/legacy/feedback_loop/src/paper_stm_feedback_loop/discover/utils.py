from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any


def canonical_data(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return canonical_data(value.model_dump(mode="json"))
    if isinstance(value, dict):
        return {str(k): canonical_data(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [canonical_data(v) for v in value]
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonical_data(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def sha256_data(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def prompt_data(value: Any) -> Any:
    """Normalise a payload for an LLM prompt while preserving author order."""

    if hasattr(value, "model_dump"):
        return prompt_data(value.model_dump(mode="json"))
    if isinstance(value, dict):
        return {str(k): prompt_data(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [prompt_data(v) for v in value]
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def prompt_json(value: Any) -> str:
    """Serialise a prompt payload in declared key order.

    ``canonical_json`` sorts keys because it feeds hashes.  Reusing it for
    prompts silently reordered the payload alphabetically, which put
    ``inspect_digest`` (tool diagnostics) ahead of ``natural_language`` in the
    Requirement Splitter input -- directly contradicting that prompt's opening
    instruction to read the specification first, and burying the semantic source
    of truth at roughly a tenth of the payload behind 20 KB of model facts.
    Dict insertion order is deterministic in Python, so this stays reproducible.

    :param value: the payload to render.
    :return: compact JSON in declared order.
    """

    return json.dumps(
        prompt_data(value), ensure_ascii=False, sort_keys=False, separators=(",", ":")
    )
