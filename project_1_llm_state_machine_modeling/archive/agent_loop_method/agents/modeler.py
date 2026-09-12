"""Modeler agent: structured JSON spec → pyfcstm DSL.

The second stage of the agent loop. Reads the ``SpecJson`` produced by
SpecExtractor and produces a pyfcstm DSL text. The DSL output then goes
through the four deterministic feedback sources (Parse / Semantic / Sim /
Judge).
"""

from __future__ import annotations

from typing import Optional

from archive.agent_loop_method.gpt_client import chat
from archive.agent_loop_method.schema import ModelArtifact, SpecJson
from archive.agent_loop_method.stages.sl_initial_modeling_prompt import (
    build_sl1_initial_modeling_prompt,
    extract_candidate_dsl_or_legacy,
)


def generate_model(
    spec: SpecJson,
    *,
    nl: str = "",
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[ModelArtifact, dict]:
    """Run Modeler on a SpecJson.

    Parameters
    ----------
    spec
        The structured spec from SpecExtractor.
    nl
        Original natural-language requirement text.  SL-1 uses this as the
        primary evidence anchor for grounding seeds.  Older callers may omit it,
        but loop integrations should pass the original NL through explicitly.
    seed
        Optional integer for LLM-call determinism (some providers honor this).
    model
        Override the default ``LLM_MODEL`` env var. ``None`` => use env.

    Returns
    -------
    (artifact, usage)
        ``artifact``: ``ModelArtifact`` with the generated DSL text.
        ``usage``: token usage dict from ``gpt_client.chat``.
    """
    spec_payload = spec.raw if spec.raw else _spec_to_dict(spec)
    messages = build_sl1_initial_modeling_prompt(
        nl=nl,
        spec_json=spec_payload,
    )
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
    )
    dsl_text = extract_candidate_dsl_or_legacy(content)
    artifact = ModelArtifact(
        dsl_text=dsl_text,
        iteration=0,
        produced_by="modeler",
    )
    return artifact, usage


def _spec_to_dict(spec: SpecJson) -> dict:
    """Fallback if spec.raw was not populated."""
    return {
        "states": spec.states,
        "events": spec.events,
        "variables": spec.variables,
        "transitions": spec.transitions,
        "hierarchy": spec.hierarchy,
    }
