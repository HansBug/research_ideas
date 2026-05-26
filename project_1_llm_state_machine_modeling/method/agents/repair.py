"""Repair agent: (current DSL, structured feedback) → new DSL.

The third stage of the agent loop, invoked when at least one of the four
feedback sources signaled a problem. Reads the current pyfcstm DSL and the
structured ``FeedbackBundle`` and produces a corrected DSL text.

Design principles:

- **Minimal change**: the prompt instructs the model to touch only what
  feedback identifies, not to reformat / rename / re-order.
- **Priority cascade**: parse > semantic > sim > judge. The repair prompt
  encodes this so the model fixes syntax before semantics before runtime
  before LLM judgment.
- **Repair is a single LLM call per iteration**, not a tool-use chain. The
  feedback bundle is serialized as JSON into the user message.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from method.gpt_client import chat
from method.schema import FeedbackBundle, ModelArtifact


_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "repair.txt"


def _load_prompt() -> str:
    if not _PROMPT_PATH.exists():
        raise FileNotFoundError(f"Repair prompt not found: {_PROMPT_PATH}")
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _strip_dsl_fence(content: str) -> str:
    """Same fence stripping as modeler.py — keep them in sync."""
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


def _serialize_feedback(fb: FeedbackBundle) -> str:
    """Serialize FeedbackBundle to compact JSON for the prompt.

    Only includes non-None sources to keep the prompt focused on actionable
    feedback.
    """
    payload: dict = {}
    if fb.parse is not None:
        payload["parse"] = asdict(fb.parse)
    if fb.semantic is not None:
        payload["semantic"] = asdict(fb.semantic)
    if fb.sim is not None:
        payload["sim"] = asdict(fb.sim)
    if fb.judge is not None:
        # Judge can be large (evidence_spans) — keep it but truncate long fields
        j = asdict(fb.judge)
        if "evidence_spans" in j and len(j["evidence_spans"]) > 10:
            j["evidence_spans"] = j["evidence_spans"][:10]
            j["_truncated"] = True
        payload["judge"] = j
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str)


def repair_model(
    current_dsl: str,
    feedback: FeedbackBundle,
    *,
    iteration: int = 1,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[ModelArtifact, dict]:
    """Run Repair on a current DSL + structured feedback.

    Parameters
    ----------
    current_dsl
        The current pyfcstm DSL text (output of Modeler or previous Repair).
    feedback
        ``FeedbackBundle`` from the deterministic + judge feedback sources.
        At least one source should have ``ok=False`` (otherwise no repair is
        needed and the caller should skip).
    iteration
        Which loop iteration this repair belongs to (recorded on the
        ``ModelArtifact``).
    seed
        Optional integer for LLM-call determinism.
    model
        Override the default ``LLM_MODEL`` env var.

    Returns
    -------
    (artifact, usage)
        ``artifact``: ``ModelArtifact`` with the corrected DSL and
        ``produced_by='repair'``.
        ``usage``: token usage dict from ``gpt_client.chat``.
    """
    if not feedback.has_any_signal():
        raise ValueError("Repair called with an empty FeedbackBundle — nothing to fix.")

    system_prompt = _load_prompt()
    feedback_json = _serialize_feedback(feedback)

    user_msg = (
        f"## Current DSL\n\n```\n{current_dsl}\n```\n\n"
        f"## Feedback bundle\n\n```\n{feedback_json}\n```\n\n"
        "Output the corrected pyfcstm DSL only."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
    )
    dsl_text = _strip_dsl_fence(content)
    artifact = ModelArtifact(
        dsl_text=dsl_text,
        iteration=iteration,
        produced_by="repair",
    )
    return artifact, usage
