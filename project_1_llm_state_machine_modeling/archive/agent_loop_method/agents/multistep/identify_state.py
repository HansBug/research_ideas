"""Step 1 of MTI multistep pipeline: identify states.

Input:  natural-language requirements text
Output: list of states with nested + parallel hierarchy
"""

from __future__ import annotations

from typing import Optional

from method.agents.multistep._common import build_user_message, call_step


def identify_state(
    requirements: str,
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[list[dict], dict]:
    """Run Step 1 — identify states.

    Returns
    -------
    (states, usage)
        ``states``: a list of state dicts. Each state dict has keys
        ``name``, ``description``, ``is_pseudo``, ``sub_states``.
        Top-level siblings represent parallel regions (or a flat state set
        if the system has no hierarchy / no concurrency).
        ``usage``: token usage dict from ``gpt_client.chat``.
    """
    user_msg = build_user_message(
        requirements=requirements,
        opening_cue="Identified State List:\n",
    )
    parsed, usage = call_step(
        step_name="identify_state",
        user_message=user_msg,
        seed=seed,
        model=model,
        force_json=True,
    )
    states = parsed.get("states", [])
    if not isinstance(states, list):
        raise ValueError(f"identify_state: 'states' must be a list, got {type(states).__name__}")
    return states, usage
