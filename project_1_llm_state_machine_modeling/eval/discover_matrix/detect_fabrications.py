"""Re-derive every published issue against the current predicates.

Why this replaced a per-class detector
--------------------------------------
The first version had one branch per known defect class -- an `initial_target`
check, a reachability check -- and each branch re-implemented enough of the
predicate to second-guess it.  Three problems followed.  The branches could only
find defects already known, so a new class would score as clean.  They crashed on
inputs the real predicates handle (a `states()` call with no recorded trace entry
took `function_call_trace[0]` out of range).  And they duplicated logic that the
predicate layer owns, so a fix there left the detector stale.

What actually decides whether a published issue is fabricated is not which class
it belongs to.  It is two questions that can be asked of any issue:

  1. Does its primary assertion still come back False?  A True says the model
     satisfies the obligation, so the issue was never a defect.  An `unsupported`
     says the predicate now refuses to answer -- which is what the horizon and
     search-budget guards do to the answers they used to fabricate.

  2. Does the evidence that False rests on touch a converter-owned element?  If
     the pair's `attribution_exclusions` match the call's refs, the finding is
     representation debt by policy and must not be published as a confirmed
     defect.

Both are asked by calling the predicate, so there is nothing to keep in sync: the
detector reports what the current layer says, and its verdict moves when the layer
moves.  That is also its limitation, stated plainly -- it cannot tell a fabricated
issue from one that a *later* bug made unanswerable.  What it establishes is that
the run's published issues are the ones the current predicates still stand behind.

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

#: `predicate(a="x", b=1)` -> name plus keyword bindings.  Kept because the audit
#: bundle stores expressions as text, and the parse is what decides whether a call
#: gets re-derived at all -- a miss here is a silent pass, so it is unit-tested.
_CALL = re.compile(r"([a-z_]+)\s*\((.*)\)\s*is\s+(True|False)\s*$", re.S)
_KWARG = re.compile(r"(\w+)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|(\d+))")
#: An unconditional default entry inside a composite: `[*] -> Name;`, no guard and
#: no trigger.  Anything after `:` disqualifies it.
_DEFAULT_ENTRY = re.compile(r"^\s*\[\*\]\s*->\s*(\w+)\s*;\s*$")


def _parse_call(expression: str) -> tuple[str, dict[str, str]] | None:
    match = _CALL.search(expression.strip())
    if not match:
        return None
    bindings = {
        key: (dq or sq or num) for key, dq, sq, num in _KWARG.findall(match.group(2))
    }
    return match.group(1), bindings


def _default_entry_of(model: str, composite: str) -> str | None:
    """The composite's unconditional `[*] -> Z`, fully qualified, or None.

    Read from the text because the question is syntactic -- which entry carries no
    guard -- and the structure facade reports entries without that distinction.
    Scoped by brace depth so a sibling composite's entry is not picked up.
    Reported for context on a representation-debt verdict, not used to decide one.
    """

    leaf = composite.rsplit(".", 1)[-1]
    depth = 0
    inside_at: int | None = None
    for line in model.splitlines():
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


def _environment(case: str):
    from paper_stm_feedback_loop.assertions import build_eval_environment

    trace = json.loads(
        (REPORT / f"source_traces/llms_emp_feedback_final_{case}.json").read_text()
    )
    exclusions = list(trace.get("attribution_exclusions") or [])
    env = build_eval_environment(
        model_text=(REPORT / f"fcstm/llms_emp_feedback_final_{case}.fcstm").read_text(),
        source_mappings=trace.get("mappings") or [],
        source_exclusions=exclusions,
        timeout_seconds=120,
        fbmcq_solver_timeout_ms=20_000,
        fbmcq_max_bound=6,
        fbmcq_process_wall_seconds=60.0,
    )
    model = (REPORT / f"fcstm/llms_emp_feedback_final_{case}.fcstm").read_text()
    return env, model, exclusions


def _rederive(env, expression: str):
    """`(verdict, refs)` for one assertion expression, re-run now.

    `verdict` is `"false"`, `"true"`, `"unsupported"` or `"error"`; refs are the
    model elements the call declared it rested on, which is what an exclusion is
    matched against.
    """

    result = env.eval_assert(expression, "fabrication detector")
    trace = result.function_call_trace or ()
    refs: tuple[str, ...] = ()
    if trace:
        refs = tuple(trace[0].model_refs or ())
    if result.value is True:
        return "true", refs
    if result.value is False:
        return "false", refs
    if result.result == "unsupported":
        return "unsupported", refs
    return "error", refs


def scan(audit_dir: pathlib.Path) -> list[dict]:
    from paper_stm_feedback_loop.common.refs import reference_matches

    out: list[dict] = []
    for path in sorted(audit_dir.glob("*-audit.json")):
        record = json.loads(path.read_text())
        if record.get("terminal") != "completed":
            continue
        cell = path.name.removesuffix("-audit.json")
        artifact = record.get("terminal_artifact") or {}
        issues = artifact.get("issues") or []
        if not issues:
            continue
        env, model, exclusions = _environment(record["pair"])
        by_id = {a.get("assertion_id"): a for a in record.get("assertions") or []}
        for issue in issues:
            for assertion_id in issue.get("assertion_ids") or []:
                assertion = by_id.get(assertion_id) or {}
                expression = str(assertion.get("expression") or "")
                if not _parse_call(expression):
                    out.append({
                        "cell": cell,
                        "requirement_id": issue.get("requirement_id"),
                        "assertion_id": assertion_id,
                        "title": issue.get("title"),
                        "defect_class": "unparseable-assertion",
                        "evidence": (
                            "无法解析该断言表达式，因此无法重算；这条必须人工核对，"
                            f"不能计入干净结果：{expression[:120]}"
                        ),
                    })
                    continue
                verdict, refs = _rederive(env, expression)
                if verdict != "false":
                    out.append({
                        "cell": cell,
                        "requirement_id": issue.get("requirement_id"),
                        "assertion_id": assertion_id,
                        "title": issue.get("title"),
                        "defect_class": f"published-issue-no-longer-false:{verdict}",
                        "evidence": (
                            f"该 issue 的主断言现在重算为 {verdict}，"
                            "说明它不是当前谓词层认可的缺陷"
                        ),
                    })
                    continue
                touched = [e for e in exclusions if reference_matches(e, refs)]
                if touched:
                    composite = (
                        _parse_call(expression)[1].get("composite")
                        or _parse_call(expression)[1].get("source")
                        or ""
                    )
                    entry = _default_entry_of(model, composite) if composite else None
                    out.append({
                        "cell": cell,
                        "requirement_id": issue.get("requirement_id"),
                        "assertion_id": assertion_id,
                        "title": issue.get("title"),
                        "defect_class": "false-rests-on-converter-owned-element",
                        "evidence": (
                            f"该 False 依赖的元素命中归因排除 {touched}"
                            + (f"（该组合状态的无条件默认入口为 {entry}）" if entry else "")
                            + "，按策略属表征债，不应作为 confirmed issue 发布"
                        ),
                    })
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    found = scan(pathlib.Path(sys.argv[1]))
    print(f"按当前谓词重算后站不住的已发布 issue：{len(found)} 条\n")
    for row in found:
        print(f"  {row['cell']:22s} {row['requirement_id']:10s} [{row['defect_class']}]")
        print(f"    {row['title']}")
        print(f"    证据: {row['evidence']}\n")
    if not found:
        print("  （无）每条已发布 issue 的主断言仍重算为 False，且其证据未触及归因排除元素。")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
