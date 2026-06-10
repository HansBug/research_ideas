#!/usr/bin/env python3
"""Extract 5-component IR from a pyfcstm DSL file.

Wraps `eval/extract/pyfcstm.py` (the canonical PATH1 extractor) and emits a
JSON aligned with the existing demo `eval/data/refs/<case>/ref_components.json`
schema (the one used by `abs-fsm-brake-control` + `automatic-elevator-controller`).

Usage:  extract_components.py <case_id> <path.fcstm> <output.json>

The schema is:
{
  "source": "codex_draft+manual_audit",
  "case_id": "<id>",
  "model_text_path": "ref_model.txt",
  "states":              [{"id","name","parent","text"}],
  "transitions":         [{"id","src","tgt","event","guard","action","is_forced","text"}],
  "guards":              [{"id","transition_id","expr","text"}],
  "actions":             [{"id","transition_id","expr","text"}],
  "hierarchical_states": [{"id","name","children","text"}]
}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
EVAL_DIR = REPO_ROOT / "project_1_llm_state_machine_modeling" / "eval"
sys.path.insert(0, str(EVAL_DIR))


def main() -> None:
    if len(sys.argv) != 4:
        print("usage: extract_components.py <case_id> <path.fcstm> <output.json>",
              file=sys.stderr)
        sys.exit(99)
    cid, src_path, out_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    if not src_path.exists():
        print(f"FILE_NOT_FOUND: {src_path}", file=sys.stderr)
        sys.exit(98)

    from extract.pyfcstm import extract_pyfcstm

    src = src_path.read_text(encoding="utf-8")
    cs = extract_pyfcstm(src)

    # ComponentSet → ref_components.json schema (aligned with existing demos)
    def _list_or_empty(attr: str) -> list:
        v = getattr(cs, attr, None)
        if v is None:
            return []
        try:
            return list(v)
        except TypeError:
            return []

    states = _list_or_empty("states")
    transitions = _list_or_empty("transitions")
    guards = _list_or_empty("guards")
    actions = _list_or_empty("actions")
    hierarchical = _list_or_empty("hierarchical_states")

    def _norm_state(s, i: int) -> dict:
        if isinstance(s, dict):
            return {
                "id": s.get("id", f"s{i}"),
                "name": s.get("name", ""),
                "parent": s.get("parent"),
                "text": s.get("text") or s.get("name", ""),
            }
        # plain string
        name = str(s)
        return {"id": f"s{i}", "name": name, "parent": None, "text": name}

    def _norm_trans(t, i: int) -> dict:
        if isinstance(t, dict):
            return {
                "id": t.get("id", f"t{i}"),
                "src": t.get("src", ""),
                "tgt": t.get("tgt", ""),
                "event": t.get("event", "") or "",
                "guard": t.get("guard", "") or "",
                "action": t.get("action", "") or "",
                "is_forced": bool(t.get("is_forced", False)),
                "text": t.get("text", ""),
            }
        return {"id": f"t{i}", "src": "?", "tgt": "?", "event": "", "guard": "",
                "action": "", "is_forced": False, "text": str(t)}

    def _norm_guard(g, i: int) -> dict:
        if isinstance(g, dict):
            return {
                "id": g.get("id", f"g{i}"),
                "transition_id": g.get("transition_id", ""),
                "expr": g.get("expr", "") or g.get("text", ""),
                "text": g.get("text", ""),
            }
        return {"id": f"g{i}", "transition_id": "", "expr": str(g), "text": str(g)}

    def _norm_action(a, i: int) -> dict:
        if isinstance(a, dict):
            return {
                "id": a.get("id", f"a{i}"),
                "transition_id": a.get("transition_id", ""),
                "expr": a.get("expr", "") or a.get("code", "") or a.get("text", ""),
                "text": a.get("text", ""),
            }
        return {"id": f"a{i}", "transition_id": "", "expr": str(a), "text": str(a)}

    def _norm_hier(h, i: int) -> dict:
        if isinstance(h, dict):
            return {
                "id": h.get("id", f"h{i}"),
                "name": h.get("name", ""),
                "children": h.get("children", []),
                "text": h.get("text", ""),
            }
        return {"id": f"h{i}", "name": str(h), "children": [], "text": str(h)}

    out = {
        "source": "codex_draft+manual_audit",
        "case_id": cid,
        "model_text_path": "ref_model.txt",
        "states":              [_norm_state(s, i)  for i, s  in enumerate(states)],
        "transitions":         [_norm_trans(t, i)  for i, t  in enumerate(transitions)],
        "guards":              [_norm_guard(g, i)  for i, g  in enumerate(guards)],
        "actions":             [_norm_action(a, i) for i, a  in enumerate(actions)],
        "hierarchical_states": [_norm_hier(h, i)   for i, h  in enumerate(hierarchical)],
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = {
        "states": len(out["states"]),
        "transitions": len(out["transitions"]),
        "guards": len(out["guards"]),
        "actions": len(out["actions"]),
        "hierarchical_states": len(out["hierarchical_states"]),
    }
    print(f"EXTRACT_OK {counts}")


if __name__ == "__main__":
    main()
