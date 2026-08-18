#!/usr/bin/env python3
"""IDE-equivalent lint for pyfcstm DSL.

Reimplements the key warning categories that jsfcstm (TypeScript IDE) exposes,
based on pyfcstm.model introspection (root_state walk + transitions / events /
defines).

Categories detected:
  - unreachable_state    : state never reached from initial transitions
  - dead_transition      : transition whose source is unreachable, or guard
                           literally false
  - unused_event         : event declared on a state but never used as
                           `event=...` on any transition
  - unused_variable      : variable in sm.defines but neither read nor written
                           in any guard/effect/initialization
  - write_only_variable  : variable written but never read (suspicious dead
                           assignment)

The structural semantic errors (undefined_variable, unresolved_state,
duplicate_variable) are already caught by pyfcstm.model.parse_dsl_node_to_state_machine
and surface as exceptions earlier in the pipeline; this lint runs AFTER that
passes.

Usage:
  lint_pyfcstm.py <path.fcstm>

Exit codes:
  0  no warnings
  1  parse/sem fail (delegated to caller's verifier)
  2  warnings present (printed as JSON)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("usage: lint_pyfcstm.py <path.fcstm>", file=sys.stderr)
        sys.exit(99)

    path = Path(sys.argv[1])
    src = path.read_text()

    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.model import parse_dsl_node_to_state_machine
        ast = parse_with_grammar_entry(src, "state_machine_dsl")
        sm = parse_dsl_node_to_state_machine(ast)
    except Exception as e:
        print(json.dumps({"error": f"parse/sem failed: {type(e).__name__}: {e}"}, ensure_ascii=False))
        sys.exit(1)

    warnings = []

    # ---- Collect all states + events + variables ----
    all_states = list(sm.walk_states())  # includes root
    state_by_path = {tuple(s.path): s for s in all_states}
    leaf_paths = {tuple(s.path) for s in all_states if s.is_leaf_state and not s.is_pseudo}

    # All declared events: state-path → set of event names
    declared_events: dict[tuple, set[str]] = {}
    for s in all_states:
        ev = getattr(s, "events", {}) or {}
        if ev:
            declared_events[tuple(s.path)] = set(ev.keys())

    # Used events: walk all transitions, collect (state_path, event_name) used
    used_events: set[tuple[tuple, str]] = set()
    all_transitions = list(getattr(sm.root_state, "transitions", []) or [])

    for t in all_transitions:
        ev = getattr(t, "event", None)
        if ev is not None:
            ev_name = getattr(ev, "name", None)
            ev_path = getattr(ev, "state_path", None)
            if ev_name and ev_path is not None:
                used_events.add((tuple(ev_path), ev_name))

    # ---- Check 1: unreachable_state ----
    # BFS from init_transitions on root + any composite child's init
    reachable: set[tuple] = set()
    queue: list[tuple] = []
    # Seed from root init transitions
    for t in getattr(sm.root_state, "init_transitions", []) or []:
        target = getattr(t, "to_state", None)
        # target is a State object referenced by name; need to resolve to path
        if isinstance(target, str):
            # Resolve relative to root substates
            tgt_state = sm.root_state.substates.get(target) if hasattr(sm.root_state.substates, "get") else None
            if tgt_state:
                queue.append(tuple(tgt_state.path))
        elif hasattr(target, "path"):
            queue.append(tuple(target.path))

    # Also seed root entry via transitions list with from=INIT_STATE
    for t in all_transitions:
        from_s = getattr(t, "from_state", None)
        from_name = getattr(from_s, "name", "") if not isinstance(from_s, str) else from_s
        if from_name == "INIT_STATE":
            to_s = getattr(t, "to_state", None)
            if isinstance(to_s, str):
                tgt = sm.root_state.substates.get(to_s) if hasattr(sm.root_state.substates, "get") else None
                if tgt:
                    queue.append(tuple(tgt.path))
            elif hasattr(to_s, "path"):
                queue.append(tuple(to_s.path))

    # BFS
    while queue:
        p = queue.pop(0)
        if p in reachable:
            continue
        reachable.add(p)
        # Find outgoing transitions
        s = state_by_path.get(p)
        if s is None:
            continue
        # Composite state: also reachable via init_transitions
        for t in getattr(s, "init_transitions", []) or []:
            to_s = getattr(t, "to_state", None)
            if isinstance(to_s, str):
                tgt = s.substates.get(to_s) if hasattr(getattr(s, "substates", None), "get") else None
                if tgt:
                    queue.append(tuple(tgt.path))
            elif hasattr(to_s, "path"):
                queue.append(tuple(to_s.path))
        # Normal outgoing transitions
        for t in getattr(s, "transitions_from", []) or []:
            to_s = getattr(t, "to_state", None)
            if isinstance(to_s, str):
                # Resolve in parent scope
                parent = s.parent if hasattr(s, "parent") else sm.root_state
                tgt = parent.substates.get(to_s) if hasattr(getattr(parent, "substates", None), "get") else None
                if tgt:
                    queue.append(tuple(tgt.path))
            elif hasattr(to_s, "path"):
                queue.append(tuple(to_s.path))

    unreachable_leaves = leaf_paths - reachable
    for p in sorted(unreachable_leaves):
        warnings.append({
            "code": "unreachable_state",
            "severity": "warning",
            "state_path": ".".join(p),
            "message": f"State {'.'.join(p)!r} is not reachable from any initial transition.",
        })

    # ---- Check 2: unused_event ----
    for state_path, event_names in declared_events.items():
        for ev_name in event_names:
            if (state_path, ev_name) not in used_events:
                warnings.append({
                    "code": "unused_event",
                    "severity": "warning",
                    "state_path": ".".join(state_path),
                    "event_name": ev_name,
                    "message": f"Event {ev_name!r} declared on state {'.'.join(state_path)} but never used in any transition.",
                })

    # ---- Check 3: dead_transition (always-false guard literal) ----
    for t in all_transitions:
        guard = getattr(t, "guard", None)
        if guard is None:
            continue
        guard_str = str(guard).strip().lower()
        if guard_str in ("false", "0", "(false)"):
            from_s = getattr(t, "from_state", None)
            from_name = getattr(from_s, "name", str(from_s)) if not isinstance(from_s, str) else from_s
            to_s = getattr(t, "to_state", None)
            to_name = getattr(to_s, "name", str(to_s)) if not isinstance(to_s, str) else to_s
            warnings.append({
                "code": "dead_transition_false_guard",
                "severity": "warning",
                "from": from_name,
                "to": to_name,
                "message": f"Transition {from_name} -> {to_name} has an always-false guard ({guard_str!r}).",
            })

    # ---- Check 3b: dead_transition due to unreachable source ----
    for t in all_transitions:
        from_s = getattr(t, "from_state", None)
        if isinstance(from_s, str):
            continue  # likely INIT_STATE special
        if hasattr(from_s, "path") and from_s.is_leaf_state and tuple(from_s.path) in unreachable_leaves:
            to_s = getattr(t, "to_state", None)
            to_name = getattr(to_s, "name", str(to_s)) if not isinstance(to_s, str) else to_s
            warnings.append({
                "code": "dead_transition_unreachable_source",
                "severity": "warning",
                "from": ".".join(from_s.path),
                "to": to_name,
                "message": f"Transition source {'.'.join(from_s.path)} is unreachable; this transition is dead.",
            })

    # ---- Check 4: unused_variable / write_only_variable ----
    # Scan DSL source text for variable reads/writes.
    # Reads: any identifier reference in guard expressions or RHS of effects.
    # Writes: identifier on LHS of `=` in effects or enter/during/exit blocks.
    # Simple heuristic: regex over source text, excluding declarations.
    defines = getattr(sm, "defines", {}) or {}
    decl_line_pattern = re.compile(r"^\s*def\s+(?:int|float|bool)\s+(\w+)\s*=")
    # Build per-var read/write counts using AST is complex; use text scan
    # 1) Strip `def TYPE name = ...;` lines
    src_no_decl = []
    for line in src.splitlines():
        if decl_line_pattern.match(line):
            continue
        src_no_decl.append(line)
    body = "\n".join(src_no_decl)

    for var_name in defines.keys():
        # Look for any occurrence (read or write) in body
        # Word-boundary match
        pattern = re.compile(rf"\b{re.escape(var_name)}\b")
        matches = pattern.findall(body)
        if len(matches) == 0:
            warnings.append({
                "code": "unused_variable",
                "severity": "warning",
                "variable": var_name,
                "message": f"Variable {var_name!r} declared but never read nor written.",
            })
            continue
        # Write check: `var_name = <expr>` or `var_name = <expr>;` (not `==`)
        write_pattern = re.compile(rf"\b{re.escape(var_name)}\s*=(?!=)")
        writes = write_pattern.findall(body)
        # Read check: occurrences minus writes (approximate)
        n_reads = len(matches) - len(writes)
        if len(writes) > 0 and n_reads <= 0:
            warnings.append({
                "code": "write_only_variable",
                "severity": "info",
                "variable": var_name,
                "message": f"Variable {var_name!r} is written but never read (dead assignment).",
            })

    # ---- Output ----
    report = {
        "path": str(path),
        "total": len(warnings),
        "by_code": {},
        "warnings": warnings,
    }
    for w in warnings:
        c = w["code"]
        report["by_code"][c] = report["by_code"].get(c, 0) + 1

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if warnings:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
