"""Step 4 of MTI multistep pipeline: identify transitions."""

from __future__ import annotations

from typing import Optional

from method.agents.multistep._common import build_user_message, call_step


def identify_transition(
    requirements: str,
    state_list: list[dict],
    event_list: list[dict],
    variable_list: list[dict],
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[list[dict], dict]:
    """Run Step 4 — identify transitions.

    Returns ``(transitions, usage)`` where each transition dict has keys
    ``from``, ``to``, ``event`` (str | None), ``guard`` (str | None),
    ``effect`` (str | None), ``is_forced`` (bool), ``description``.

    Note: ``event`` and ``guard`` are mutually exclusive per pyfcstm DSL —
    at most one can be non-null on any given transition.
    """
    user_msg = build_user_message(
        requirements=requirements,
        upstream={
            "States": state_list,
            "Events": event_list,
            "Variables": variable_list,
        },
        opening_cue="Identified Transition List:\n",
    )
    parsed, usage = call_step(
        step_name="identify_transition",
        user_message=user_msg,
        seed=seed,
        model=model,
        force_json=True,
    )
    transitions = parsed.get("transitions", [])
    if not isinstance(transitions, list):
        raise ValueError(f"identify_transition: 'transitions' must be a list, got {type(transitions).__name__}")
    return transitions, usage
