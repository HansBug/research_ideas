"""Step 5 of MTI multistep pipeline: identify state lifecycle actions."""

from __future__ import annotations

from typing import Optional

from method.agents.multistep._common import build_user_message, call_step


def identify_action(
    requirements: str,
    state_list: list[dict],
    event_list: list[dict],
    variable_list: list[dict],
    transition_list: list[dict],
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[list[dict], dict]:
    """Run Step 5 — identify state lifecycle actions.

    Returns ``(actions, usage)`` where each action dict has keys ``state``,
    ``slot`` (``enter`` | ``during`` | ``exit``), ``kind`` (``operation`` |
    ``abstract``), ``content``, and ``description``.

    Transition effects (from Step 4) are NOT re-listed here — they live on
    the transition, not on a state.
    """
    user_msg = build_user_message(
        requirements=requirements,
        upstream={
            "States": state_list,
            "Events": event_list,
            "Variables": variable_list,
            "Transitions": transition_list,
        },
        opening_cue="Identified Action List:\n",
    )
    parsed, usage = call_step(
        step_name="identify_action",
        user_message=user_msg,
        seed=seed,
        model=model,
        force_json=True,
    )
    actions = parsed.get("actions", [])
    if not isinstance(actions, list):
        raise ValueError(f"identify_action: 'actions' must be a list, got {type(actions).__name__}")
    return actions, usage
