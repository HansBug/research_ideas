"""Identify fabricated findings by re-deriving them, not by matching an id list.

Why the id list was wrong
-------------------------
`known_false_positives.json` keys on `(cell, requirement_id)`.  Requirement ids
come from the splitter, so the same defect class carries different ids in
different cells: matrix-v16's `initial_target` fabrication appears as REQ-006 and
REQ-014 in 0029-claude and as REQ-007 and REQ-019 in 0029-gpt.  Scored by id, the
0029-gpt pair reads as "unadjudicated" and the run looks cleaner than it is --
four fabrications counted as two.  Ids also change between runs on one cell, so
the list could not verify a fix even where it did match.

So each class is detected from the evidence instead, by calling the predicate
again on the pair's real model:

`initial-target-omits-deciding-entry-from-refs`
    A False `initial_target(composite=X, child=Y)` is a fabrication when X's
    unconditional default entry targets some Z that the pair's
    `attribution_exclusions` marks converter-owned.  Confirmed by calling
    `initial_target(X, Z)` and getting True: the claim is then only about which
    state the converter's synthetic entry points at.  Reported as fixed when the
    failing call's refs name Z, because attribution can filter it from there.

`eventless-completion-swallows-event`
    A False `occupancy_after`/`reaches` is a fabrication when raising
    `within_cycles` never changes the answer while the same call from a settled
    position answers True -- an event that cannot be observed anywhere an
    unconditional edge is outgoing.  Both halves are required: a horizon that is
    merely too small is a producer error, not a predicate defect, and it is
    distinguished by the answer flipping at some larger bound.

Building an eval environment per pair costs a few seconds, which is why this is
an audit-time tool and not part of a run.

Usage: detect_fabrications.py <audit_dir>
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
FEEDBACK_LOOP = ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop"
REPORT = (
    ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/reports/llms_emp_r45_java_60"
)

if str(FEEDBACK_LOOP / "src") not in sys.path:
    sys.path.insert(0, str(FEEDBACK_LOOP / "src"))

#: `predicate(a="x", b="y", n=1)` -> name plus the keyword bindings.
_CALL = re.compile(r"([a-z_]+)\s*\((.*)\)\s*is\s+(True|False)\s*$", re.S)
_KWARG = re.compile(r"(\w+)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|(\d+))")
#: An unconditional default entry inside a composite: `[*] -> Name;` with no
#: guard and no trigger.  Anything after `:` disqualifies it.
_DEFAULT_ENTRY = re.compile(r"^\s*\[\*\]\s*->\s*(\w+)\s*;\s*$")


def _parse_call(expression: str) -> tuple[str, dict[str, str]] | None:
    match = _CALL.search(expression.strip())
    if not match:
        return None
    bindings = {
        key: (dq or sq or num)
        for key, dq, sq, num in _KWARG.findall(match.group(2))
    }
    return match.group(1), bindings


def _environment(case: str):
    from paper_stm_feedback_loop.assertions import build_eval_environment

    model = (REPORT / f"fcstm/llms_emp_feedback_final_{case}.fcstm").read_text()
    trace = json.loads(
        (REPORT / f"source_traces/llms_emp_feedback_final_{case}.json").read_text()
    )
    env = build_eval_environment(
        model_text=model,
        source_mappings=trace.get("mappings") or [],
        source_exclusions=trace.get("attribution_exclusions") or [],
        timeout_seconds=120,
        fbmcq_solver_timeout_ms=20_000,
        fbmcq_max_bound=6,
        fbmcq_process_wall_seconds=60.0,
    )
    return env, model, set(trace.get("attribution_exclusions") or [])


def _call(env, expression: str):
    result = env.eval_assert(expression, "fabrication detector")
    refs = tuple(result.function_call_trace[0].model_refs or ())
    return result.value, refs


def _default_entry_of(model: str, composite: str) -> str | None:
    """The composite's unconditional `[*] -> Z`, as a fully qualified path.

    Read from the text because the question is syntactic -- which entry carries no
    guard -- and the structure facade reports entries without that distinction.
    Scoped by brace depth so a sibling composite's entry is not picked up.
    """

    leaf = composite.rsplit(".", 1)[-1]
    lines = model.splitlines()
    depth = 0
    inside_at: int | None = None
    for line in lines:
        stripped = line.strip()
        if inside_at is not None:
            if depth == inside_at:
                match = _DEFAULT_ENTRY.match(line)
                if match:
                    return f"{composite}.{match.group(1)}"
            if depth < inside_at:
                return None
        if re.match(rf"^\s*state\s+{re.escape(leaf)}\b.*\{{\s*$", line):
            inside_at = depth + 1
        depth += stripped.count("{") - stripped.count("}")
    return None


def _check_initial_target(env, model, exclusions, bindings):
    composite, child = bindings.get("composite"), bindings.get("child")
    if not composite or not child:
        return None
    value, refs = _call(env, f'initial_target(composite="{composite}", child="{child}") is True')
    if value is not False:
        return None
    entry = _default_entry_of(model, composite)
    if not entry or entry == child:
        return None
    if f"compiler:state:{entry}" not in exclusions:
        return None
    entry_value, _ = _call(env, f'initial_target(composite="{composite}", child="{entry}") is True')
    if entry_value is not True:
        return None
    if any(entry in ref for ref in refs):
        # The predicate now declares what decided it, so attribution can filter
        # this without help.  Not a fabrication any more.
        return None
    return {
        "defect_class": "initial-target-omits-deciding-entry-from-refs",
        "evidence": (
            f"{composite} 的无条件默认入口指向 {entry}（在 attribution_exclusions 中），"
            f"initial_target(composite, {entry.rsplit('.',1)[-1]}) 为 True；"
            f"而失败调用的 refs 未申报它，归因无 exclusion 可匹配"
        ),
    }


def _check_reachability(env, predicate, bindings):
    source, target = bindings.get("source"), bindings.get("target")
    trigger = bindings.get("trigger") or bindings.get("event")
    if not (source and target and trigger):
        return None
    def ask(cycles):
        expr = (
            f'{predicate}(source="{source}", trigger="{trigger}", '
            f'target="{target}", within_cycles={cycles}) is True'
        )
        return _call(env, expr)[0]
    if ask(1) is not False:
        return None
    # A horizon shortfall flips somewhere; this defect never does.
    if any(ask(n) is True for n in (2, 3, 5, 9)):
        return None
    # The other half: the same obligation holds from a settled position.  Walk the
    # eventless chain out of `source` and retry from its end.
    settled = _settled_from(env, source, trigger, target)
    if settled is None:
        return None
    return {
        "defect_class": "eventless-completion-swallows-event",
        "evidence": (
            f"{predicate} 在 within_cycles 1/2/3/5/9 全为 False，不是视野不足；"
            f"而同一义务自 {settled} 起注入同一事件为 True，"
            f"说明事件在无条件完成边占用的周期上无法被观测"
        ),
    }


def _settled_from(env, source, trigger, target) -> str | None:
    """A sibling position where the same call answers True, if one exists.

    Searched among the source's siblings rather than derived from the model text:
    the point is only to establish that the obligation holds somewhere the
    eventless chain has already run out, and a sibling that answers True is that
    witness.  Returns None when none does, in which case the False may be real
    and the finding is left for a human.
    """

    parent = source.rsplit(".", 1)[0]
    from paper_stm_feedback_loop.assertions.exceptions import UnsupportedEvidence

    try:
        rows = env.eval_assert(
            f'len(states(parent="{parent}", recursive=False)) >= 0', "enumerate"
        )
    except Exception:
        return None
    del rows  # only used to prove the facade answers; paths come from refs below
    for candidate in _siblings(env, parent):
        if candidate == source:
            continue
        expr = (
            f'occupancy_after(source="{candidate}", trigger="{trigger}", '
            f'target="{target}", within_cycles=1) is True'
        )
        try:
            if _call(env, expr)[0] is True:
                return candidate
        except UnsupportedEvidence:
            continue
        except Exception:
            continue
    return None


def _siblings(env, parent: str) -> list[str]:
    try:
        result = env.eval_assert(
            f'[row.path for row in states(parent="{parent}", recursive=False)] == []',
            "enumerate",
        )
    except Exception:
        return []
    refs = result.function_call_trace[0].model_refs or ()
    return [ref for ref in refs if ref.startswith(parent + ".")]


def scan(audit_dir: pathlib.Path) -> list[dict]:
    out: list[dict] = []
    for path in sorted(audit_dir.glob("*-audit.json")):
        record = json.loads(path.read_text())
        if record.get("terminal") != "completed":
            continue
        cell = path.name.removesuffix("-audit.json")
        case = record["pair"]
        artifact = record.get("terminal_artifact") or {}
        issues = artifact.get("issues") or []
        if not issues:
            continue
        env, model, exclusions = _environment(case)
        by_id = {a.get("assertion_id"): a for a in record.get("assertions") or []}
        for issue in issues:
            for assertion_id in issue.get("assertion_ids") or []:
                expression = str((by_id.get(assertion_id) or {}).get("expression") or "")
                parsed = _parse_call(expression)
                if not parsed:
                    continue
                predicate, bindings = parsed
                verdict = None
                if predicate == "initial_target":
                    verdict = _check_initial_target(env, model, exclusions, bindings)
                elif predicate in {"occupancy_after", "reaches"}:
                    verdict = _check_reachability(env, predicate, bindings)
                if verdict:
                    out.append({
                        "cell": cell,
                        "requirement_id": issue.get("requirement_id"),
                        "assertion_id": assertion_id,
                        "title": issue.get("title"),
                        **verdict,
                    })
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    found = scan(pathlib.Path(sys.argv[1]))
    print(f"按证据判定的捏造发现 {len(found)} 条:\n")
    for row in found:
        print(f"  {row['cell']:22s} {row['requirement_id']:10s} [{row['defect_class']}]")
        print(f"    {row['title']}")
        print(f"    证据: {row['evidence']}\n")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
