"""Step 3 of MTI multistep pipeline: identify variables (depends on state_list)."""

from __future__ import annotations

from typing import Optional

from method.agents.multistep._common import build_user_message, call_step


def identify_variable(
    requirements: str,
    state_list: list[dict],
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[list[dict], dict]:
    """Run Step 3 — identify variables.

    Variables depend on the state list because of the "state vs variable
    redundancy" rule: a Boolean status like "door open / door closed" should
    be expressed as either two parallel states OR a Boolean variable, but
    not both. The state list is injected so the LLM can avoid duplicating
    semantics already captured as states.

    Returns ``(variables, usage)`` where each variable dict has keys
    ``name``, ``type`` (``int`` | ``float``), ``init`` (string literal),
    and ``description``.
    """
    user_msg = build_user_message(
        requirements=requirements,
        upstream={"States": state_list},
        opening_cue="Identified Variable List:\n",
    )
    parsed, usage = call_step(
        step_name="identify_variable",
        user_message=user_msg,
        seed=seed,
        model=model,
        force_json=True,
    )
    variables = parsed.get("variables", [])
    if not isinstance(variables, list):
        raise ValueError(f"identify_variable: 'variables' must be a list, got {type(variables).__name__}")
    return variables, usage
