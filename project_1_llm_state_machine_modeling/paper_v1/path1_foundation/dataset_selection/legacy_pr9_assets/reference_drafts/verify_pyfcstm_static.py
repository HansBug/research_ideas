#!/usr/bin/env python3
"""Static analysis for pyfcstm DSL — catches logical dead-code that
parse / sem / sim_smoke can't see.

Output: prints a list of diagnostics, exits non-zero if any ERROR present.

Diagnostics:
  - ERROR  unwritten_read_var <name>   : variable read in guard/expr but never
                                          written by any action ⇒ guard
                                          permanently evaluates to the var's
                                          init value, transition is dead
  - ERROR  forced_unreachable <text>   : forced transition `! * -> X : if [...]`
                                          whose guard reads only never-written
                                          vars ⇒ never fires
  - WARN   write_only_var <name>       : variable written but never read in any
                                          guard / expression ⇒ fact-flag bloat,
                                          should usually be an abstract action
                                          or removed
  - WARN   deadlock_state <state>      : leaf state with 0 outgoing transitions
                                          AND not at the model root ⇒ once
                                          entered, machine halts
  - WARN   unreachable_state <state>   : state with 0 incoming transitions and
                                          not the initial target of any [*]
  - WARN   high_var_to_state_ratio     : len(vars) > 2 * len(leaf_states) ⇒
                                          likely fact-flag bloat

Usage:  verify_pyfcstm_static.py <path.fcstm> [--strict]

When --strict, WARNs are also treated as failures (exit 1).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable


def _strip_comments(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.DOTALL)
    src = re.sub(r"//[^\n]*", "", src)
    return src


def _walk_expr_ids(expr_text: str) -> set[str]:
    """Find identifiers in a guard / expression text.

    Crude: any [A-Za-z_]\w* that is not a keyword / literal / known builtin.
    """
    if not expr_text:
        return set()
    KEYWORDS = {
        "if", "else", "true", "false", "True", "False", "and", "or", "not",
        "AND", "OR", "NOT", "abs", "min", "max", "int", "float", "bool",
    }
    return {m for m in re.findall(r"\b[A-Za-z_]\w*\b", expr_text) if m not in KEYWORDS}


def _find_var_declarations(src: str) -> tuple[dict[str, str], set[str]]:
    """`def <type> <name> = <init>;` and `def <type> <name>;`.

    Returns (declarations, external_vars).
    A var is treated as `@external` (input from sensor/ground/sim runtime, not
    written by any DSL action) iff its def line has a trailing comment
    containing `@external` or `@input`. These vars are EXEMPT from
    `unwritten_read_var` ERROR — they're expected to be written by the host
    runtime via `runtime.vars[name] = value` between cycles.
    """
    out: dict[str, str] = {}
    external: set[str] = set()
    pat = re.compile(
        r"\bdef\s+(int|float|bool)\s+(\w+)\s*(?:=\s*([^;]+))?;([^\n]*)",
    )
    for m in pat.finditer(src):
        name = m.group(2)
        out[name] = m.group(3) or ""
        trailing = m.group(4) or ""
        if "@external" in trailing or "@input" in trailing:
            external.add(name)
    return out, external


def _find_state_blocks(src: str) -> dict[str, str]:
    """Map state name → its raw body (the text between { and matching }).

    Pyfcstm allows nested `state X { ... }`. We use a simple brace-counting
    walker to extract each `state Name { body }` (leaf: `state Name;`).
    """
    out: dict[str, str] = {}
    i = 0
    n = len(src)
    pat = re.compile(r"\bstate\s+(\w+)\s*(\{|;)")
    while i < n:
        m = pat.search(src, i)
        if not m:
            break
        name = m.group(1)
        if m.group(2) == ";":
            out.setdefault(name, "")
            i = m.end()
            continue
        # walk braces
        depth = 1
        j = m.end()
        while j < n and depth > 0:
            if src[j] == "{":
                depth += 1
            elif src[j] == "}":
                depth -= 1
            j += 1
        out.setdefault(name, src[m.end():j-1])
        # don't advance past block — there could be nested states inside, we
        # want to capture them on next iteration too
        i = m.end()
    return out


def _find_assignments(body: str) -> set[str]:
    """Return variable names assigned within action / effect bodies.

    Matches `<name> = <expr>;` outside of guards (guards live in `if [...]`).
    """
    out: set[str] = set()
    # Iterate over text, but skip what's inside `if [...]` (guards)
    masked = re.sub(r"if\s*\[[^\]]*\]", " ", body, flags=re.DOTALL)
    for m in re.finditer(r"\b(\w+)\s*=\s*[^=;]+;", masked):
        out.add(m.group(1))
    return out


def _find_transitions(body: str) -> list[dict]:
    """Find transition lines of the form  `Src -> Tgt [extras] ;` or `! ... ;`.

    Extras may include `:: Event`, `: if [guard]`, `effect { ... }`.
    Returns list of dicts with src/tgt/event/guard/effect/raw/is_forced.
    """
    out: list[dict] = []
    # Forced: ! <src or *> -> <tgt> ...
    forced_pat = re.compile(
        r"!\s*([\w\*]+(?:\s*\.\s*\w+)*)\s*->\s*(\w+)(.*?);",
        re.DOTALL,
    )
    for m in forced_pat.finditer(body):
        raw = m.group(0)
        rest = m.group(3) or ""
        out.append(_parse_extras(raw, m.group(1), m.group(2), rest, is_forced=True))
    # Regular: <src> -> <tgt> ...
    plain_pat = re.compile(
        r"(?<![!])\b(\w+)\s*->\s*(\w+)(.*?);",
        re.DOTALL,
    )
    for m in plain_pat.finditer(body):
        raw = m.group(0)
        if raw.lstrip().startswith("!"):
            continue
        rest = m.group(3) or ""
        out.append(_parse_extras(raw, m.group(1), m.group(2), rest, is_forced=False))
    return out


def _parse_extras(raw: str, src: str, tgt: str, rest: str, is_forced: bool) -> dict:
    ev = ""
    m = re.search(r"::\s*(\w+)", rest)
    if m:
        ev = m.group(1)
    g = ""
    m = re.search(r"if\s*\[([^\]]+)\]", rest)
    if m:
        g = m.group(1).strip()
    eff = ""
    m = re.search(r"effect\s*\{([^}]*)\}", rest, re.DOTALL)
    if m:
        eff = m.group(1).strip()
    return {"src": src, "tgt": tgt, "event": ev, "guard": g, "effect": eff,
            "raw": raw, "is_forced": is_forced}


def analyze(src_text: str) -> list[tuple[str, str, str]]:
    """Returns list of (severity, code, message).

    severity ∈ {"ERROR", "WARN"}
    """
    diags: list[tuple[str, str, str]] = []
    # IMPORTANT: parse var declarations BEFORE stripping comments
    # (we need to see trailing `// @external` annotations on def lines)
    vars_decl, external_vars = _find_var_declarations(src_text)
    src = _strip_comments(src_text)

    # ---- Variable usage ----
    state_blocks = _find_state_blocks(src)

    writes: dict[str, set[str]] = {v: set() for v in vars_decl}     # var -> {state where written}
    reads: dict[str, set[str]] = {v: set() for v in vars_decl}      # var -> {state where read}

    for stname, body in state_blocks.items():
        # writes in entry/during/exit blocks + transition effect blocks
        assigns = _find_assignments(body)
        for v in assigns & set(vars_decl):
            writes[v].add(stname)
        # reads in if-guards within this body
        for guard_m in re.finditer(r"if\s*\[([^\]]+)\]", body):
            for ident in _walk_expr_ids(guard_m.group(1)):
                if ident in vars_decl:
                    reads[ident].add(stname)
        # reads in assignment RHS: `LHS = <rhs>;` — `<rhs>` reads idents
        # (this catches self-read pattern like `boot_counter = boot_counter + 1;`)
        # Mask out if-guards first so guard exprs don't double-count.
        masked = re.sub(r"if\s*\[[^\]]*\]", " ", body, flags=re.DOTALL)
        for rhs_m in re.finditer(r"\b\w+\s*=\s*([^=;][^;]*);", masked):
            rhs_expr = rhs_m.group(1)
            for ident in _walk_expr_ids(rhs_expr):
                if ident in vars_decl:
                    reads[ident].add(stname)

    # Top-level / root-block reads & writes (root level outside state {...})
    # Crude: take everything not inside { ... } as root.
    # For simplicity, also scan whole src minus state-blocks.
    # We already scan state_blocks; the top-level transitions live inside the
    # root state which is one of the blocks. Good enough.

    # ---- Diagnostics ----

    # ERROR: read but never written (except for @external-marked vars)
    for v, rd_states in reads.items():
        if rd_states and not writes[v] and v not in external_vars:
            init = vars_decl.get(v, "").strip()
            diags.append(("ERROR", "unwritten_read_var",
                          f"variable `{v}` is read in guard(s) but never assigned "
                          f"by any action/effect (init={init!r}); transitions "
                          f"reading `{v}` are effectively dead unless init makes them true. "
                          f"If `{v}` is a sensor / ground / external input, mark the "
                          f"declaration with a trailing `// @external` comment."))

    # WARN: write_only var (encoded NL fact as flag)
    for v, wr_states in writes.items():
        if wr_states and not reads[v]:
            diags.append(("WARN", "write_only_var",
                          f"variable `{v}` is written but never read; likely "
                          "an NL-fact encoded as a boolean flag — use an "
                          "abstract action or remove if not gating any guard"))

    # WARN: high var-to-state ratio
    n_vars = len(vars_decl)
    n_states = len(state_blocks)
    if n_states > 0 and n_vars > 2 * n_states:
        diags.append(("WARN", "high_var_to_state_ratio",
                      f"declared {n_vars} variables for {n_states} states "
                      "(ratio>2x); likely NL-fact bloat — review variable purpose"))

    # ---- Transitions / states ----
    all_transitions: list[dict] = []
    state_outgoing: dict[str, int] = {st: 0 for st in state_blocks}
    state_incoming: dict[str, int] = {st: 0 for st in state_blocks}

    for stname, body in state_blocks.items():
        # transitions defined inside this block (its child transitions)
        for tr in _find_transitions(body):
            all_transitions.append({"owner": stname, **tr})
            if tr["src"] != "*" and tr["src"] in state_outgoing:
                state_outgoing[tr["src"]] += 1
            if tr["tgt"] in state_incoming:
                state_incoming[tr["tgt"]] += 1
            # also bump for initial transitions
        # initial `[*] -> X`
        for im in re.finditer(r"\[\*\]\s*->\s*(\w+)", body):
            init_tgt = im.group(1)
            if init_tgt in state_incoming:
                state_incoming[init_tgt] += 1

    # ERROR: forced * -> X with guard reading only-never-written non-external vars
    for tr in all_transitions:
        if not tr["is_forced"]:
            continue
        g = tr["guard"]
        if not g:
            continue
        ids = _walk_expr_ids(g) & set(vars_decl)
        non_external = ids - external_vars
        if non_external and all(
                (vars_decl.get(i, "").strip() in ("0", "false", "False") and not writes[i])
                for i in non_external):
            diags.append(("ERROR", "forced_unreachable",
                          f"forced transition `{tr['raw'].strip()[:80]}...`: "
                          f"guard reads only never-written non-external variables "
                          f"({sorted(non_external)}); this forced transition never fires"))

    # WARN: deadlock_state — state with 0 outgoing, not a designated final
    # Exclude states whose name starts with Done/End/Final/Sink (common conventions)
    final_re = re.compile(r"^(Done|End|Final|Sink|Halt|Stop)\b", re.IGNORECASE)
    # Also skip composite states (they have outgoing through children)
    composite_states = {st for st, body in state_blocks.items()
                        if re.search(r"\bstate\s+\w+\s*(\{|;)", body)}
    for st, out_count in state_outgoing.items():
        if out_count == 0 and st not in composite_states and not final_re.match(st):
            diags.append(("WARN", "deadlock_state",
                          f"state `{st}` has 0 outgoing transitions and "
                          "is not marked final; once entered the machine halts"))

    # WARN: unreachable_state — state with 0 incoming (and not root)
    # The root state of the file is incoming-less by design — find it.
    all_root_candidates = list(state_blocks.keys())
    root_state = ""
    for st in all_root_candidates:
        # root: appears at top level with non-empty body
        if state_blocks[st] and not any(re.search(rf"\bstate\s+{st}\s*\{{", state_blocks[other])
                                        for other in all_root_candidates if other != st):
            root_state = st
            break
    for st, in_count in state_incoming.items():
        if in_count == 0 and st != root_state:
            diags.append(("WARN", "unreachable_state",
                          f"state `{st}` has 0 incoming transitions; "
                          "no way to reach it (verify it's not orphaned)"))

    return diags


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: verify_pyfcstm_static.py <path.fcstm> [--strict]", file=sys.stderr)
        sys.exit(99)
    strict = "--strict" in sys.argv
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}", file=sys.stderr)
        sys.exit(98)

    src = path.read_text(encoding="utf-8")
    diags = analyze(src)
    errs = [d for d in diags if d[0] == "ERROR"]
    warns = [d for d in diags if d[0] == "WARN"]

    for sev, code, msg in diags:
        print(f"{sev} {code}: {msg}")

    print(f"---")
    print(f"STATIC_SUMMARY errors={len(errs)} warnings={len(warns)}")
    if errs or (strict and warns):
        print("STATIC_FAIL")
        sys.exit(1)
    print("STATIC_OK")


if __name__ == "__main__":
    main()
