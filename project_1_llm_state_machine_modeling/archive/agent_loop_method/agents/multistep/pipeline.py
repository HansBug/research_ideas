"""6-step orchestrator: NL requirements -> pyfcstm DSL via MTI multistep pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from archive.agent_loop_method.agents.multistep.identify_state import identify_state
from archive.agent_loop_method.agents.multistep.identify_event import identify_event
from archive.agent_loop_method.agents.multistep.identify_variable import identify_variable
from archive.agent_loop_method.agents.multistep.identify_transition import identify_transition
from archive.agent_loop_method.agents.multistep.identify_action import identify_action
from archive.agent_loop_method.agents.multistep.build_pyfcstm import build_pyfcstm
from archive.agent_loop_method.schema import ModelArtifact


@dataclass
class MultistepResult:
    """Full record of a 6-step multistep modeling run."""

    state_list: list[dict] = field(default_factory=list)
    event_list: list[dict] = field(default_factory=list)
    variable_list: list[dict] = field(default_factory=list)
    transition_list: list[dict] = field(default_factory=list)
    action_list: list[dict] = field(default_factory=list)
    final_dsl: str = ""
    artifact: Optional[ModelArtifact] = None
    token_usage: dict[str, int] = field(default_factory=lambda: {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "n_calls": 0,
    })
    step_usage: dict[str, dict] = field(default_factory=dict)


def _accumulate_usage(total: dict, step_usage: dict, step_name: str, all_step_usage: dict) -> None:
    """Add a single-step usage dict into the running total + per-step record."""
    total["prompt_tokens"] += step_usage.get("prompt_tokens", 0)
    total["completion_tokens"] += step_usage.get("completion_tokens", 0)
    total["total_tokens"] += step_usage.get("total_tokens", 0)
    total["n_calls"] += 1
    all_step_usage[step_name] = step_usage


def run_multistep_modeling(
    requirements: str,
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
    verbose: bool = False,
) -> MultistepResult:
    """Run the full 6-step MTI multistep modeling pipeline.

    Steps run sequentially:
      1. identify_state   - NL -> state list (nested/parallel hierarchy)
      2. identify_event   - NL -> event list
      3. identify_variable - NL + state_list -> variable list
      4. identify_transition - NL + state + event + variable -> transitions
      5. identify_action  - NL + all upstream -> actions
      6. build_pyfcstm    - all 5 lists -> complete pyfcstm DSL

    Returns a ``MultistepResult`` containing every intermediate list,
    the final DSL, a ``ModelArtifact``, per-step token usage, and the
    aggregate token usage across all 6 LLM calls.
    """
    result = MultistepResult()

    if verbose:
        print("[multistep] Step 1/6: identify_state ...")
    states, u1 = identify_state(requirements, seed=seed, model=model)
    result.state_list = states
    _accumulate_usage(result.token_usage, u1, "identify_state", result.step_usage)

    if verbose:
        print(f"[multistep] Step 2/6: identify_event ... (states: {len(states)})")
    events, u2 = identify_event(requirements, seed=seed, model=model)
    result.event_list = events
    _accumulate_usage(result.token_usage, u2, "identify_event", result.step_usage)

    if verbose:
        print(f"[multistep] Step 3/6: identify_variable ... (events: {len(events)})")
    variables, u3 = identify_variable(requirements, states, seed=seed, model=model)
    result.variable_list = variables
    _accumulate_usage(result.token_usage, u3, "identify_variable", result.step_usage)

    if verbose:
        print(f"[multistep] Step 4/6: identify_transition ... (variables: {len(variables)})")
    transitions, u4 = identify_transition(requirements, states, events, variables, seed=seed, model=model)
    result.transition_list = transitions
    _accumulate_usage(result.token_usage, u4, "identify_transition", result.step_usage)

    if verbose:
        print(f"[multistep] Step 5/6: identify_action ... (transitions: {len(transitions)})")
    actions, u5 = identify_action(requirements, states, events, variables, transitions, seed=seed, model=model)
    result.action_list = actions
    _accumulate_usage(result.token_usage, u5, "identify_action", result.step_usage)

    if verbose:
        print(f"[multistep] Step 6/6: build_pyfcstm ... (actions: {len(actions)})")
    dsl_text, u6 = build_pyfcstm(
        requirements,
        states,
        events,
        variables,
        transitions,
        actions,
        seed=seed,
        model=model,
    )
    result.final_dsl = dsl_text
    result.artifact = ModelArtifact(
        dsl_text=dsl_text,
        iteration=0,
        produced_by="modeler",
    )
    _accumulate_usage(result.token_usage, u6, "build_pyfcstm", result.step_usage)

    if verbose:
        print(f"[multistep] done. total tokens: {result.token_usage['total_tokens']}")

    return result
