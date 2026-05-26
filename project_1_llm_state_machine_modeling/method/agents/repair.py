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

import json
from dataclasses import asdict
from pathlib import Path
from typing import Literal, Optional

from method.gpt_client import chat
from method.schema import FeedbackBundle, ModelArtifact, TestScenario


_PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts" / "repair"

RepairTarget = Literal["parse", "semantic", "sim", "judge"]

_PROMPT_FILES: dict[RepairTarget, str] = {
    "parse":    "fix_parse.txt",
    "semantic": "fix_sem.txt",
    "sim":      "fix_sim.txt",
    "judge":    "fix_judge.txt",  # Phase H placeholder
}


def _load_subprompt(target: RepairTarget) -> str:
    p = _PROMPT_DIR / _PROMPT_FILES[target]
    if not p.exists():
        raise FileNotFoundError(f"Repair sub-prompt not found: {p}")
    return p.read_text(encoding="utf-8")


def _strip_dsl_fence(content: str) -> str:
    s = content.strip()
    if not s.startswith("```"):
        return s
    parts = s.split("```")
    if len(parts) >= 2:
        body = parts[1]
        first_nl = body.find("\n")
        if first_nl != -1:
            first_line = body[:first_nl].strip().lower()
            if first_line in ("fcstm", "pyfcstm", "dsl", "text", ""):
                body = body[first_nl + 1:]
        return body.rstrip().rstrip("`").rstrip()
    return s


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


def _build_user_msg(
    target: RepairTarget,
    current_dsl: str,
    feedback: FeedbackBundle,
    nl: str,
    scenarios: Optional[list[TestScenario]] = None,
) -> str:
    """Build a focused user message containing only the relevant diagnostic."""
    payload: dict = {}
    if target == "parse":
        payload["parse"] = asdict(feedback.parse)
    elif target == "semantic":
        payload["semantic"] = asdict(feedback.semantic)
    elif target == "sim":
        sim_dict = asdict(feedback.sim)
        # Drop already-passing scenarios to keep prompt tight.
        sim_dict["scenario_results"] = [
            sr for sr in sim_dict["scenario_results"] if sr["status"] != "pass"
        ]
        payload["sim"] = sim_dict
    elif target == "judge":
        payload["judge"] = asdict(feedback.judge)

    diag_json = json.dumps(payload, ensure_ascii=False, indent=2, default=str)

    parts = [
        f"## NL requirements\n\n{nl.strip()}\n",
        f"## Current DSL\n\n```\n{current_dsl}\n```\n",
        f"## {target.capitalize()} diagnostic\n\n```\n{diag_json}\n```\n",
    ]

    if target == "sim" and scenarios is not None:
        # Include the frozen scenario set so the LLM knows what 'ground truth' looks like.
        sc_json = json.dumps(
            [
                {
                    "name": s.name,
                    "description": s.description,
                    "initial_state": s.initial_state,
                    "initial_vars": s.initial_vars,
                    "steps": [
                        {
                            "name": st.name,
                            "before_cycles": st.before_cycles,
                            "events": st.events,
                            "expected_state": st.expected_state,
                            "expected_vars": st.expected_vars,
                        }
                        for st in s.steps
                    ],
                }
                for s in scenarios
            ],
            ensure_ascii=False, indent=2, default=str,
        )
        parts.append(f"## Frozen scenarios (ground truth — DO NOT EDIT)\n\n```\n{sc_json}\n```\n")

    parts.append("Output the corrected pyfcstm DSL only.")
    return "\n".join(parts)


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
    user_msg = _build_user_msg(target, current_dsl, feedback, nl, scenarios)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    content, usage = chat(messages=messages, model=model, temperature=0.0, seed=seed)
    dsl_text = _strip_dsl_fence(content)
    artifact = ModelArtifact(
        dsl_text=dsl_text,
        iteration=iteration,
        produced_by="repair",
    )
    return artifact, usage, target
