"""Cascaded Repair agent: dispatch on the earliest-failing feedback source.

Per Phase E design decision: each feedback channel has a focused fix sub-prompt
(``fix_parse.txt`` / ``fix_sem.txt`` / ``fix_sim.txt`` / ``fix_judge.txt``)
that sees only its own diagnostic plus NL context. The cascade order is

    parse → semantic → sim → judge

— the dispatcher picks the FIRST source whose ``ok=False`` and routes the
repair through its sub-prompt. Other channels are not shown to the LLM,
keeping each repair focused.

This module preserves the public entry ``repair_model(...)`` used by the
existing tests; behavior is now cascaded internally instead of a single
union-prompt call.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal, Optional

from method.gpt_client import chat
from method.schema import FeedbackBundle, ModelArtifact, TestScenario
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.sl_prompt_common import strip_fence


_PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts" / "repair"

RepairTarget = Literal["parse", "semantic", "sim", "judge"]

_PROMPT_FILES: dict[RepairTarget, str] = {
    "parse":    "fix_parse.txt",
    "semantic": "fix_sem.txt",
    "sim":      "fix_sim.txt",
    "judge":    "fix_judge.txt",  # Phase H placeholder
}


def _load_subprompt(target: RepairTarget) -> str:
    """Load the focused repair sub-prompt for ``target``.

    The shared pyfcstm grammar is appended once by the canonical SL-9 prompt
    generator, not here, so the final system prompt does not contain duplicate
    or empty grammar sections.
    """
    p = _PROMPT_DIR / _PROMPT_FILES[target]
    if not p.exists():
        raise FileNotFoundError(f"Repair sub-prompt not found: {p}")
    return p.read_text(encoding="utf-8")


def select_repair_target(feedback: FeedbackBundle) -> Optional[RepairTarget]:
    """Pick the earliest failing source in cascade order.

    Returns None if all present sources are ok or none are present.
    """
    if feedback.parse is not None and not feedback.parse.ok:
        return "parse"
    if feedback.semantic is not None and not feedback.semantic.ok:
        return "semantic"
    if feedback.sim is not None and not feedback.sim.ok:
        return "sim"
    if feedback.judge is not None and not feedback.judge.ok:
        return "judge"
    return None


def _scenario_to_dict(scenario: TestScenario) -> dict[str, Any]:
    return {
        "name": scenario.name,
        "description": scenario.description,
        "initial_state": scenario.initial_state,
        "initial_vars": scenario.initial_vars,
        "steps": [
            {
                "name": step.name,
                "before_cycles": step.before_cycles,
                "events": step.events,
                "expected_state": step.expected_state,
                "expected_vars": step.expected_vars,
            }
            for step in scenario.steps
        ],
    }


def _build_repair_context(
    target: RepairTarget,
    feedback: FeedbackBundle,
    scenarios: Optional[list[TestScenario]] = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build structured SL-9 diagnostics and scenario summary.

    For target='sim' the message also surfaces a **passing-scenarios list**
    (a regression-prevention guardrail per Phase E (c) decision): the LLM
    is reminded that those scenarios currently pass and the edit must not
    break them.
    """
    if target == "sim":
        # Split scenario results into passing vs failing for explicit display.
        all_results = list(feedback.sim.scenario_results)
        passing_names = [sr.name for sr in all_results if sr.status == "pass"]
        failing_results = [sr for sr in all_results if sr.status != "pass"]

        # Build sim diagnostic JSON containing only the failing scenarios
        sim_payload = asdict(feedback.sim)
        sim_payload["scenario_results"] = [asdict(sr) for sr in failing_results]
        sim_payload["passing_scenario_names"] = passing_names
        selected_diagnostics = [{"source": "sim", "feedback": sim_payload}]
        scenario_summary: dict[str, Any] = {
            "passing_scenario_names": passing_names,
            "failing_scenario_names": [sr.name for sr in failing_results],
            "do_not_regress_passing_scenarios": True,
        }
        if scenarios is not None:
            scenario_summary["frozen_scenarios"] = [_scenario_to_dict(s) for s in scenarios]
        return selected_diagnostics, scenario_summary

    payload: dict[str, Any] = {}
    if target == "parse":
        payload = asdict(feedback.parse)
    elif target == "semantic":
        payload = asdict(feedback.semantic)
    elif target == "judge":
        payload = asdict(feedback.judge)
    else:
        raise ValueError(f"unknown repair target: {target}")
    return [{"source": target, "feedback": payload}], {}


def repair_model(
    current_dsl: str,
    feedback: FeedbackBundle,
    *,
    nl: str = "",
    scenarios: Optional[list[TestScenario]] = None,
    iteration: int = 1,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[ModelArtifact, dict, Optional[RepairTarget]]:
    """Run one cascaded repair round.

    Selects the earliest-failing feedback source, loads its dedicated
    sub-prompt, and runs a single LLM call to produce a corrected DSL.

    Parameters
    ----------
    current_dsl
        The current pyfcstm DSL text (output of Modeler or previous Repair).
    feedback
        ``FeedbackBundle`` with at least one source reporting ``ok=False``.
    nl
        The original NL requirement document (used by every sub-prompt for
        intent context).
    scenarios
        The frozen scenario list. Required when the repair target is ``sim``.
    iteration
        Loop iteration number (stamped onto the returned ``ModelArtifact``).
    seed, model
        Standard LLM-call knobs.

    Returns
    -------
    (artifact, usage, target)
        ``artifact`` is the new DSL (``produced_by='repair'``), ``usage`` is
        the LLM token usage dict, ``target`` is the cascade source picked
        (``None`` only if nothing was failing — caller should not invoke
        repair in that case).
    """
    if not feedback.has_any_signal():
        raise ValueError("Repair called with an empty FeedbackBundle — nothing to fix.")

    target = select_repair_target(feedback)
    if target is None:
        raise ValueError("Repair called with all-ok feedback — caller should have skipped.")

    system_prompt = _load_subprompt(target)
    selected_diagnostics, scenario_summary = _build_repair_context(target, feedback, scenarios)

    messages = build_sl9_repair_prompt(
        nl=nl,
        current_dsl=current_dsl,
        fix_plan=None,
        grounding_map=None,
        selected_diagnostics=selected_diagnostics,
        grammar_digest=None,
        preserve_list=[],
        scenario_summary=scenario_summary,
        repair_target=target,
        system_prompt=system_prompt,
    )
    content, usage = chat(messages=messages, model=model, temperature=0.0, seed=seed)
    dsl_text = strip_fence(content)
    artifact = ModelArtifact(
        dsl_text=dsl_text,
        iteration=iteration,
        produced_by="repair",
    )
    return artifact, usage, target
