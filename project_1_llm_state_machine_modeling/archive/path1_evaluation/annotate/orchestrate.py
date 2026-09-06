"""Pair Claude + Codex annotators on the same input, persist both raw JSONs.

Public entry: ``annotate_pair(case_id, condition, component_kind, nl_text,
ref_text, pred_text, ref_instances, pred_instances, raw_dir)`` returns
``(claude_result, codex_result)`` and writes the two raw JSONs to disk
for audit.

The orchestrator runs both annotators sequentially (not parallel — keeps
stderr / cost accounting clean for now). Switch to threading if total
wall-clock matters.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from . import claude as claude_mod
from . import codex as codex_mod


_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "annotate.txt"


def _load_system_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _build_user_prompt(
    *,
    case_id: str,
    condition: str,
    component_kind: str,
    nl_text: str,
    ref_text: str,
    pred_text: str,
    ref_instances: list[dict[str, Any]],
    pred_instances: list[dict[str, Any]],
) -> str:
    return (
        f"# case_id: {case_id}\n"
        f"# condition: {condition}\n"
        f"# component_kind: {component_kind}\n\n"
        f"## nl_requirement\n\n{nl_text.strip()}\n\n"
        f"## ref_model_text\n\n```\n{ref_text.strip()}\n```\n\n"
        f"## pred_model_text\n\n```\n{pred_text.strip()}\n```\n\n"
        f"## ref_instances (kind={component_kind})\n\n```json\n"
        f"{json.dumps(ref_instances, ensure_ascii=False, indent=2)}\n```\n\n"
        f"## pred_instances (kind={component_kind})\n\n```json\n"
        f"{json.dumps(pred_instances, ensure_ascii=False, indent=2)}\n```\n\n"
        "Produce the JSON annotation per the protocol described in the system message."
    )


def annotate_pair(
    *,
    case_id: str,
    condition: str,
    component_kind: str,
    nl_text: str,
    ref_text: str,
    pred_text: str,
    ref_instances: list[dict[str, Any]],
    pred_instances: list[dict[str, Any]],
    raw_dir: Path,
    skip_claude: bool = False,
    skip_codex: bool = False,
) -> dict[str, Optional[dict[str, Any]]]:
    """Run both annotators, persist raws, return them as a dict.

    Each saved file:
        ``raw_dir/{case_id}/{condition}/{component_kind}/{annotator}.json``
    """
    system = _load_system_prompt()
    user = _build_user_prompt(
        case_id=case_id,
        condition=condition,
        component_kind=component_kind,
        nl_text=nl_text,
        ref_text=ref_text,
        pred_text=pred_text,
        ref_instances=ref_instances,
        pred_instances=pred_instances,
    )

    out_dir = Path(raw_dir) / case_id / condition / component_kind
    out_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, Optional[dict[str, Any]]] = {"claude": None, "codex": None}

    if not skip_claude:
        try:
            r = claude_mod.annotate(system_prompt=system, user_prompt=user)
            results["claude"] = r
            (out_dir / "claude.json").write_text(
                json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as e:
            err = {"error": f"{type(e).__name__}: {e}", "_meta": {"annotator": "claude"}}
            results["claude"] = err
            (out_dir / "claude.json").write_text(
                json.dumps(err, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    if not skip_codex:
        try:
            r = codex_mod.annotate(system_prompt=system, user_prompt=user)
            results["codex"] = r
            (out_dir / "codex.json").write_text(
                json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as e:
            err = {"error": f"{type(e).__name__}: {e}", "_meta": {"annotator": "codex"}}
            results["codex"] = err
            (out_dir / "codex.json").write_text(
                json.dumps(err, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    return results
