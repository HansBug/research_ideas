"""Aggregate the 60-pair manual review into an audit ledger plus readable reports.

Why the review is manual
------------------------
The obvious way to compare an author-generated STM_0 against the paper's reference
STM_0 is to diff their element sets.  I tried that first and it is not usable.
`mechanical_diff_baseline.py` derives the figures from the two released workbooks:
exact name matching reports 175 reference-only states, and normalising case,
separators and stock words cuts that to 127.  The 48 it removes were purely
lexical -- `avoid_frontend_collision`/`FrontendCollision`,
`Search_for_the_Target`/`Searching`.  The remaining 127 is still not the real gap
count: a near-name heuristic errs in both directions, correctly pairing
`EmergencyStoping`/`EmergencyStopping` (a typo on the reference side) while also
pairing `choice2`/`choice3` and `Join1`/`Join2`, which are genuinely distinct
pseudostates.  For scale: that one category alone reports 127, where the by-hand
review found 132 problems across *every* category.

The paper calls its own stage (2) SysML grammar and stage (3) SysML-standard
semantics manual.  Stage (4), requirements consistency, is never called manual --
it only states that the reference is assumed correct and an F1 computed, without
saying how elements were aligned, so its matching is not reproducible either.  So this pipeline consumes a review
where each difference was read and graded by hand, and its job is only to tally,
cross-check and render -- never to re-derive a verdict.

Grades (defined in `REVIEW_SPEC.md`, one per difference):

    correct     semantically equivalent, different spelling or shape
    similar     differs but defensible and not violating the NL
    problem     violates the NL, or drops semantics the reference carries
    extra       present in the generated model, in neither reference nor NL
    uncertain   evidence insufficient; the blocker is recorded

`out_of_scope` marks a difference as `concurrency` or `timing` so the two classes
this study's problem definition excludes (see `docs/protocol/ground_truth_limitations.md`) can be
counted separately rather than silently dropped or silently included.

Usage:
    PYTHONPATH=<repo root> python aggregate_manual_review.py <review_dir> <out_dir>
        <review_dir>  holds NL*.json written by the review agents
        <out_dir>     receives audit/ and readable/ bundles
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
_TOOLS = HERE.parents[2] / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from unwrap_markdown import unwrap as _unwrap  # noqa: E402
ROOT = HERE.resolve().parents[2]
LEDGER = (
    ROOT / ".omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json"
)
PAPER = HERE / "paper_reported_problems.json"

GRADES = ("correct", "similar", "problem", "extra", "uncertain")
SCOPES = ("concurrency", "timing")


def load_reviews(review_dir: pathlib.Path) -> list[dict]:
    """Every reviewed pair, with the source file recorded for traceability."""

    out: list[dict] = []
    for path in sorted(review_dir.glob("NL*.json")):
        payload = json.loads(path.read_text())
        if not isinstance(payload, list):
            raise SystemExit(f"{path.name}: expected a JSON array, got {type(payload).__name__}")
        for entry in payload:
            entry["_source_file"] = path.name
            out.append(entry)
    return out


def validate(reviews: list[dict]) -> list[str]:
    """Problems that would make the tally misleading.  Reported, never silently fixed."""

    complaints: list[str] = []
    seen = Counter(r.get("case") for r in reviews)
    expected = {f"{n:04d}" for n in range(60)}
    got = set(seen)
    if missing := sorted(expected - got):
        complaints.append(f"未审阅的 case（其缺席会被读成「无问题」）: {missing}")
    if dupes := sorted(c for c, n in seen.items() if n > 1):
        complaints.append(f"重复审阅的 case: {dupes}")
    if unknown := sorted(got - expected):
        complaints.append(f"不在 60 例中的 case: {unknown}")
    for review in reviews:
        case = review.get("case", "?")
        diffs = review.get("diffs")
        if not isinstance(diffs, list):
            complaints.append(f"{case}: diffs 缺失或非数组")
            continue
        for index, diff in enumerate(diffs):
            verdict = diff.get("verdict")
            if verdict not in GRADES:
                complaints.append(f"{case} diff[{index}]: 未知档位 {verdict!r}")
            if not str(diff.get("reason") or "").strip():
                complaints.append(f"{case} diff[{index}]: 缺理由（判定不可复核）")
            scope = diff.get("out_of_scope")
            if scope not in (None, *SCOPES):
                complaints.append(f"{case} diff[{index}]: 未知 out_of_scope {scope!r}")
        # The reviewer states a count; recompute it and flag disagreement rather
        # than trusting either side.
        for field, grade in (("problem_count", "problem"), ("extra_count", "extra")):
            stated = review.get(field)
            actual = sum(1 for d in diffs if d.get("verdict") == grade)
            if stated is not None and stated != actual:
                complaints.append(
                    f"{case}: {field}={stated} 与逐条统计 {actual} 不一致"
                )
    return complaints


def _predicate_complaints(reviews: list[dict]) -> list[str]:
    """Gate the `assertable` field against the closed predicate vocabulary.

    Every one of these was found by hand after publication, and each is mechanically
    detectable, which is the argument for gating rather than reviewing:

      * `transition_exists` is a facade primitive, not one of the 19 registered
        predicates.  Naming it and setting `predicate_exists: true` overstates
        vocabulary coverage -- 9 diffs did.
      * `any(edge_declared(...))` cannot run at all: `edge_declared` returns `bool`
        and `any` needs an iterable, so the expression raises `TypeError`.  3 diffs
        carried it, all marked `predicate_exists: true`.
      * A `problem` with no `assertable` contradicts the spec's requirement that every
        problem be expressible; 2 diffs had none.
      * An `extra` with `predicate_exists: true` but a blank `assertable` reads, in the
        rollup, as "no predicate can express this" -- a vocabulary gap that is not one.
        3 diffs did this.

    Reported as complaints, never silently repaired: which predicate applies is the
    reviewer's judgement, and rewriting it here would launder a wrong claim into a
    right-looking one.
    """
    CLOSED = {
        "state_declared", "variable_declared", "event_declared", "containment",
        "initial_target", "edge_declared", "effect_declared", "action_declared",
        "guard_distinguishable", "cardinality", "occupancy_after", "event_consumed",
        "stays_in", "variable_delta_after", "reaches", "terminates", "invariant",
        "response_within", "persists_until",
    }
    out: list[str] = []
    for review in reviews:
        case = review.get("case", "?")
        for index, diff in enumerate(review.get("diffs") or []):
            verdict = diff.get("verdict")
            if verdict not in {"problem", "extra"}:
                continue
            text = str(diff.get("assertable") or "").strip()
            exists = diff.get("predicate_exists")
            if not text:
                if verdict == "problem":
                    out.append(f"{case} diff[{index}]: problem 缺 assertable（规范要求每条 problem 可表达）")
                elif exists is True:
                    out.append(
                        f"{case} diff[{index}]: extra 标 predicate_exists=true 但 assertable 为空"
                        "——会被汇总读成词表缺口"
                    )
                continue
            # Strip quoted spans before looking for call names.  `invariant` and
            # `persists_until` take an fbmcq condition *string*, and that language has
            # its own calls -- `active(...)`, `in(...)`.  Reading those as predicate
            # names produced 12 false complaints on the published corpus, which would
            # have trained the next reader to ignore this gate.
            bare = __import__("re").sub(r"(['\"]).*?\1", "''", text, flags=__import__("re").S)
            named = {
                m.rstrip("( ").strip("`\"' ")
                for m in __import__("re").findall(r"[A-Za-z_][A-Za-z_0-9]*\s*\(", bare)
            }
            for name in sorted(named - CLOSED - {"any", "all", "not", "len", "bool", "sum", "str", "int"}):
                out.append(
                    f"{case} diff[{index}]: `{name}` 不在 19 个封闭谓词中"
                    f"（{'且标了 predicate_exists=true' if exists is True else '需重映射'}）"
                )
            if __import__("re").search(r"\bany\s*\(\s*(?:not\s+)?edge_declared\s*\(", bare):
                out.append(
                    f"{case} diff[{index}]: `any(edge_declared(...))` 无法执行"
                    "——edge_declared 返回 bool，any 需要可迭代对象，会抛 TypeError"
                )
    return out


def cross_reference(reviews: list[dict]) -> dict:
    """Tie each reviewed pair to the paper's record and to the ledger's E1s."""

    paper = json.loads(PAPER.read_text())
    ledger = json.loads(LEDGER.read_text())
    e1_by_case: dict[str, list[dict]] = defaultdict(list)
    for finding in ledger["findings"]:
        e1_by_case[finding["issue_id"].split("-")[1]].append(finding)
    cases = {c["case_id"]: c for c in ledger["cases"]}

    out = {}
    for review in reviews:
        case = review["case"]
        record = paper.get(case, {})
        e1 = e1_by_case.get(case, [])
        counts = Counter(d.get("verdict") for d in review.get("diffs", []))
        in_scope_problems = sum(
            1
            for d in review.get("diffs", [])
            if d.get("verdict") in {"problem", "extra"} and not d.get("out_of_scope")
        )
        out[case] = {
            "case": case,
            "group": review.get("group"),
            "llm": review.get("llm"),
            "counts": {g: counts.get(g, 0) for g in GRADES},
            "out_of_scope": Counter(
                d["out_of_scope"] for d in review.get("diffs", []) if d.get("out_of_scope")
            ),
            "problems_in_scope": in_scope_problems,
            "paper": {
                "format": record.get("format_hallucinations"),
                "grammar": record.get("grammar_hallucinations"),
                "semantic": record.get("semantic_hallucinations"),
                "semantic_resolved": record.get("semantic_resolved"),
                "f1_phase1": record.get("f1_phase1"),
                "f1_phase2": record.get("f1_phase2"),
            },
            "ledger": {
                "status": (cases.get(case) or {}).get("status"),
                "e1_ids": [f["issue_id"] for f in e1],
                "e1_categories": [f.get("category") for f in e1],
            },
            "assertable_problems": sum(
                1
                for d in review.get("diffs", [])
                if d.get("verdict") == "problem" and d.get("predicate_exists")
            ),
        }
    return out


def _flow(text: str | None, fallback: str = "—") -> str:
    """A reviewer's free text, with any hard wrapping inside it folded away.

    The reviewers wrote these fields across several lines. In Markdown that renders a
    soft break as a space, which between two CJK characters is a stray space nobody
    typed; and it makes the paragraph awkward to re-read in the published report. Folded
    here rather than in the stored judgement, so the primary record keeps exactly what
    the reviewer wrote.
    """
    if not text or not str(text).strip():
        return fallback
    return _unwrap(str(text).strip())


def readable(review: dict, cross: dict) -> str:
    """One human-facing report per pair."""

    case = review["case"]
    info = cross[case]
    lines = [
        f"# `{case}` × `{info['llm']}` — 作者 STM_0 vs 参考 STM_0 人工审阅",
        "",
        f"NL 组 `{info['group']}`。判定口径见审阅规范：**语义等价即标 `correct` / `similar`，"
        "不做机械的元素存在性比对**；本研究问题定义外的差异（正交并发、时间约束）单独标记，"
        "既不计入问题也不静默丢弃。",
        "",
        "## 判定汇总",
        "",
        "| 档位 | 条数 |",
        "| --- | ---: |",
    ]
    for grade in GRADES:
        lines.append(f"| `{grade}` | {info['counts'][grade]} |")
    lines += [
        "",
        f"**计入问题**（`problem` + `extra`，已排除问题定义外的差异）：**{info['problems_in_scope']}**",
    ]
    if info["out_of_scope"]:
        detail = "、".join(f"`{k}` {v} 条" for k, v in sorted(info["out_of_scope"].items()))
        # Blank line first: without it this is the *same* Markdown paragraph as the
        # count above, so it renders as one run-on line and any reflow pass folds the
        # two statements together.  They are independent facts and want their own paragraph.
        lines += ["", f"问题定义外的差异：{detail}"]
    lines += ["", "## 三方对照", "", "| 来源 | 记录 |", "| --- | --- |"]
    paper = info["paper"]
    lines += [
        f"| 论文 格式栏 | {paper['format'] or '—'} |",
        f"| 论文 语法栏 | {paper['grammar'] or '—'} |",
        f"| 论文 语义栏（SysML 规范） | {paper['semantic'] or '—'}"
        f"（resolved={paper['semantic_resolved']}） |",
        f"| 论文 F1 | Phase-I {paper['f1_phase1']} → Phase-II {paper['f1_phase2']} |",
        f"| 台帐 status | {info['ledger']['status']} |",
        f"| 台帐 E1 | {', '.join(info['ledger']['e1_ids']) or '无'} |",
        "",
        f"审阅者对照结论 — 相对论文：{_flow(review.get('vs_paper'), '（未填）')}",
        "",
        f"审阅者对照结论 — 相对台帐：{_flow(review.get('vs_ledger'), '（未填）')}",
        "",
        "## 逐条差异",
        "",
    ]
    for index, diff in enumerate(review.get("diffs", []), 1):
        scope = f" · 问题定义外：`{diff['out_of_scope']}`" if diff.get("out_of_scope") else ""
        lines += [
            f"### {index}. `{diff.get('verdict')}`{scope}",
            "",
            f"- 参考侧：`{diff.get('ref') or '—'}`",
            f"- 生成侧：`{diff.get('gen') or '—'}`",
            f"- 理由：{_flow(diff.get('reason'))}",
        ]
        if diff.get("assertable"):
            exists = diff.get("predicate_exists")
            mark = "谓词存在" if exists else ("谓词不存在" if exists is False else "未判定")
            lines.append(f"- 可断言形式（{mark}）：`{diff['assertable']}`")
        lines.append("")
    if review.get("notes"):
        lines += ["## 审阅者备注", "", _flow(review["notes"]), ""]
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    review_dir, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    audit, human = out / "audit", out / "readable"
    audit.mkdir(parents=True, exist_ok=True)
    human.mkdir(parents=True, exist_ok=True)

    reviews = load_reviews(review_dir)
    complaints = validate(reviews)
    # Two severities, and the split is deliberate.  `complaints` are things that make the
    # statistics wrong -- a missing case reads as "no problems there", a mismatched count
    # means one of the two numbers is a lie -- so they block.  `warnings` are annotation
    # defects that leave every headline count intact and only degrade the secondary
    # "expressible with an existing predicate" figure.  Blocking on those would have
    # stopped a bundle whose 418 judgements are fine, which is how a gate gets disabled.
    warnings = _predicate_complaints(reviews)
    cross = cross_reference(reviews)

    for review in reviews:
        case = review["case"]
        (audit / f"{case}-review.json").write_text(
            json.dumps({**review, "cross_reference": cross[case]}, ensure_ascii=False, indent=1) + "\n"
        )
        (human / f"{case}-readable.md").write_text(readable(review, cross))

    totals = Counter()
    scope_totals = Counter()
    for info in cross.values():
        for grade in GRADES:
            totals[grade] += info["counts"][grade]
        scope_totals.update(info["out_of_scope"])
    summary = {
        "schema": "paper1.manual_ref_review.v1",
        "what_this_is": (
            "60 个 pair 的逐条人工审阅结果：作者生成 STM_0 相对论文参考 STM_0 的差异，"
            "按语义而非元素存在性判定。语义等价的写法差异标为 correct/similar，不计问题。"
        ),
        "why_not_mechanical": (
            "机械元素比对不可用：参考独有状态 229 个中绝大多数是同一状态的不同命名"
            "（human_mode/HumanDrivingMode、avoid_frontend_collision/F 等），规范化后仍余 191 个"
            "假缺失。论文自身也把这一阶段标为人工执行。"
        ),
        "oracle_caveat": (
            "参考模型是论文作者人工重建的产物，论文 §7 自认 subjective、§4.2(4) 说 "
            "we assume the reference model is semantically correct——其正确性未经独立验证。"
            "因此本审阅的结论是「相对该参考模型」的，不等于绝对缺陷集。"
        ),
        "cases_reviewed": len(cross),
        "grade_totals": dict(totals),
        "out_of_scope_totals": dict(scope_totals),
        "problems_in_scope_total": sum(i["problems_in_scope"] for i in cross.values()),
        "assertable_problems_total": sum(i["assertable_problems"] for i in cross.values()),
        "validation_complaints": complaints,
        "assertable_warnings": warnings,
        "assertable_warning_note": (
            "标注质量问题，不阻塞发布：谓词名不在 19 个封闭谓词中、写法不可执行、"
            "problem 缺 assertable、extra 空 assertable 却标 predicate_exists。"
            "它们不改变任何档位计数，只影响「可用现有谓词正面断言」这个次要指标——"
            "引用该指标时应按此清单折减。"
        ),
        "per_case": {c: {k: v for k, v in i.items() if k != "out_of_scope"} | {"out_of_scope": dict(i["out_of_scope"])} for c, i in sorted(cross.items())},
    }
    (audit / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n")

    print(f"审阅 {len(cross)} 个 case -> {out}")
    print(f"  档位合计: {dict(totals)}")
    print(f"  问题定义外: {dict(scope_totals)}")
    print(f"  计入问题合计: {summary['problems_in_scope_total']}")
    if warnings:
        print(f"  ⚠ 标注质量警告 {len(warnings)} 条（不阻塞，「可断言」指标应按此折减）:")
        for line in warnings[:8]:
            print(f"    {line}")
        if len(warnings) > 8:
            print(f"    …另 {len(warnings) - 8} 条见 _summary.json 的 assertable_warnings")
    if complaints:
        print(f"  ✗ 阻塞级校验问题 {len(complaints)} 条:")
        for line in complaints[:12]:
            print(f"    {line}")
    return 1 if complaints else 0


if __name__ == "__main__":
    raise SystemExit(main())
