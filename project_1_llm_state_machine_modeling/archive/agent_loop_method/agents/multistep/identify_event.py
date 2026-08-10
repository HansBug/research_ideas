"""Step 2 of MTI multistep pipeline: identify events."""

from __future__ import annotations

from typing import Optional

from method.agents.multistep._common import build_user_message, call_step


def identify_event(
    requirements: str,
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[list[dict], dict]:
    """Run Step 2 — identify events.

    Returns ``(events, usage)`` where ``events`` is a list of dicts with keys
    ``name``, ``type`` (``External`` | ``Internal``), and ``description``.
    Empty list is valid for pure guard-driven systems.
    """
    user_msg = build_user_message(
        requirements=requirements,
        opening_cue="Identified Event List:\n",
    )
    parsed, usage = call_step(
        step_name="identify_event",
        user_message=user_msg,
        seed=seed,
        model=model,
        force_json=True,
    )
    events = parsed.get("events", [])
    if not isinstance(events, list):
        raise ValueError(f"identify_event: 'events' must be a list, got {type(events).__name__}")
    return events, usage
