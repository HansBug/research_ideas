#!/usr/bin/env python3
"""Count the assertions a gate refused to answer, per cell and per round.

A gate that refuses an assertion removes a finding that would otherwise have been published.
Precision metrics see that as an improvement -- `over@1`'s denominator is cells times rounds,
so a smaller numerator reads as fewer false reports -- while capability has not moved at all.
Nothing in the pipeline counted refusals, so the two were indistinguishable in the numbers.

That asymmetry is not hypothetical. v21's A1 refuses occupancy claims whose subject is a
pseudo-state, and on `0018` it turned ten answers per revision into nothing: the cell finished
with nine coverage gaps and `coverage_status: partial` where v20 had reported `full`. Read
through `over@k` alone, that cell got cleaner.

So the refusals are counted here and reported beside the precision figures. `refuse@1` shares
`over@1`'s denominator on purpose: when both move together, the precision gain was bought with
coverage and must not be described as capability.

Nothing new is recorded to produce this. Every refusal is already in the frozen run records --
`precheck_and_seal` persists each check's error string, and the records are append-only, so a
cell's whole revision history is recoverable after the fact. Adding a counter to the pipeline
would have bought nothing that is not already on disk, at the cost of changing a stage's
output schema.

Usage: count_refusals.py <matrix_dir> [--json]
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

#: 轮次目录，`smoke/` 与 `*.try*` 之类不算。
_ROUND = re.compile(r"^run\d+$")

#: Refusal messages, keyed by the rule that raised them. Matched on a distinctive prefix of
#: the message rather than on an exception type, because every one of these arrives as
#: `UnsupportedEvidence` and the point of the bucketing is to separate A1's effect from the
#: guards that were already in place. An unrecognised message is an error, not an `other`
#: bucket: a silent catch-all is how a rule's contribution goes unnoticed.
_RULES: tuple[tuple[str, str], ...] = (
    ("transient_subject", "cannot take a transient node for"),
    ("undiscriminating_root", "cannot take the model root"),
    ("horizon_probe", "but True over"),
    ("pseudo_initial", "pseudo-initial"),
    ("malformed_name", "is not a well-formed model name"),
    ("unsupported_binding", "predicate binding"),
    # Not a gate at all: the bounded solver gave up. Kept in its own bucket rather than
    # merged with the gates, because "a rule declined to answer" and "the solver could not"
    # call for entirely different responses, and summing them would hide both.
    ("fbmcq_solver_unstable", "fbmcq exited without stable result"),
    ("fbmcq_solver_timeout", "fbmcq solver timed out"),
    ("fbmcq_solver", "FBMCQUnsupportedEvidence"),
    # The predicate found nothing matching the binding, so there is no fact to report either
    # way. A gate in the same sense as the others -- it declines rather than answering False.
    ("no_matching_transition", "no declared transition leaves"),
    ("ambiguous_initial", "initial edges and none of them is taken unconditionally"),
    # 断言参数校验，与 `malformed_name` / `unsupported_binding` 同族：**作者写错了断言**，
    # 不是关于模型的判断。单开一桶而不并入前两者，因为三者的修法不同 —— 名字不合法要改绑定，
    # 绑定不受支持要换谓词，而 `within_cycles=0` 是转换器给了一个检查不了任何东西的预算。
    #
    # 这条是本工具在 v22 数据上**拒绝运行**才暴露的：它匹配不到任何规则，而工具的设计是
    # 「未识别的消息是错误，不是 `other` 桶」。若当初给了 catch-all，这个形态会一直不被看见 ——
    # `CLAUDE.md` §7 的「未分类 diagnostic 不能静默放过」在这里的具体形态。
    # 锚在这条校验的**不变部分**，不锚参数名。首版写的是 `"within_cycles must be at least 1"` ——
    # 而同一条校验对不同谓词用不同参数名（`within_cycles` / `bound`），于是规则只覆盖了一半，
    # 下一代次数据上又报一次未分类。
    #
    # 这是「枚举式匹配器」那个老毛病的复发：泄漏检测器曾同一错误连续七次以新拼写复发，正解是
    # 停止枚举、改按性质匹配。我记下了那条教训，然后在同一天又写了一个按拼写枚举的匹配器。
    # 「零或负预算什么也检查不了」这句与参数名无关，是这条校验的真正身份。
    ("invalid_step_budget", "a zero or negative budget checks nothing"),
)

#: Buckets that are the pipeline's own gates. `refuse@1` is about what the gates removed, so
#: solver failures are reported alongside rather than inside it.
GATE_RULES = frozenset(
    {"transient_subject", "undiscriminating_root", "horizon_probe",
     "pseudo_initial", "malformed_name", "unsupported_binding",
     "no_matching_transition", "ambiguous_initial",
     # 与 `malformed_name` 同理算门：它确实移除了一条断言，且移除的原因在管线自己一侧。
     "invalid_step_budget"}
)


def _classify(message: str) -> str | None:
    for rule, needle in _RULES:
        if needle in message:
            return rule
    return None


def _executions(record: object, depth: int = 0) -> list[dict]:
    if depth > 8:
        return []
    if isinstance(record, dict):
        found = record.get("executions")
        if isinstance(found, list):
            return found
        for value in record.values():
            got = _executions(value, depth + 1)
            if got:
                return got
    elif isinstance(record, list):
        for value in record:
            got = _executions(value, depth + 1)
            if got:
                return got
    return []


def _refusals(cell_dir: pathlib.Path) -> dict:
    """Refusals across every precheck revision of one cell.

    Every revision is read, not just the last. A refusal that the producer went on to repair
    still happened, still consumed budget, and is still the reason some requirement ended up
    quarantined -- counting only the final script would report zero for exactly the cells the
    gate acted on hardest.
    """
    records = sorted(cell_dir.glob("records/*precheck-and-seal-state-update/record.json"))
    if not records:
        raise SystemExit(
            f"{cell_dir}: no precheck-and-seal records. Refusing to report 0 refusals for a "
            "cell whose records could not be read -- an absent count and a zero count read "
            "identically to someone counting zeros."
        )
    by_rule: collections.Counter[str] = collections.Counter()
    total = 0
    unclassified: list[str] = []
    per_revision: list[int] = []
    for path in records:
        executions = _executions(json.loads(path.read_text(encoding="utf-8")))
        this_revision = 0
        for execution in executions:
            raw = execution.get("error")
            if not raw:
                continue
            text = raw if isinstance(raw, str) else str(raw)
            # A non-empty `error` is not necessarily a refusal: a dependent whose prerequisite
            # failed also lands here ("prerequisite(s) ... did not hold"), and counting those
            # would inflate the figure with something no gate did. `UnsupportedEvidence` is
            # what a gate raises, so it is the discriminator.
            if "UnsupportedEvidence" not in text:
                continue
            # The payload is `str(dict)` and is *not* reliably `ast.literal_eval`-able -- real
            # messages quote model paths and predicate arguments, and one of them produced
            # `leading zeros in decimal integer literals`. Matching the rule needles against
            # the raw text avoids inventing a Python-repr parser, and every needle is a phrase
            # only its own gate emits.
            total += 1
            this_revision += 1
            rule = _classify(text)
            if rule is None:
                unclassified.append(text[:200])
            else:
                by_rule[rule] += 1
        per_revision.append(this_revision)
    if unclassified:
        raise SystemExit(
            f"{cell_dir}: {len(unclassified)} refusal message(s) matched no rule. Add the "
            f"rule rather than an `other` bucket. First: {unclassified[0]!r}"
        )
    completed = cell_dir / "discover-completed.json"
    coverage: dict = {}
    if completed.exists():
        final = json.loads(completed.read_text(encoding="utf-8"))
        coverage = {
            "coverage_status": final.get("coverage_status"),
            "coverage_gaps": len(final.get("coverage_gaps") or []),
            "issues": len(final.get("issues") or []),
        }
    return {
        "total": total,
        "by_rule": dict(by_rule),
        "per_precheck_revision": per_revision,
        **coverage,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix_dir", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rounds: dict[str, dict[str, dict]] = {}
    # 只认 `run<N>`。上一版把 matrix_dir 下**每个**子目录当轮次，于是 `smoke/` 混进分母：
    # v21 上报 34 格而实为 33，同时输出里写着「same denominator as over@1」，而 `over@1` 由
    # 人工按 33 格给。两个被要求并列阅读的比率跑在不同分母上，脚本自己却断言它们相同。
    round_dirs = [p for p in sorted(args.matrix_dir.iterdir()) if p.is_dir() and _ROUND.match(p.name)]
    skipped = [p.name for p in sorted(args.matrix_dir.iterdir()) if p.is_dir() and not _ROUND.match(p.name)]
    if skipped:
        print(f"skipped non-round dirs: {', '.join(skipped)}", file=sys.stderr)
    for run_dir in round_dirs:
        cells = {}
        for cell in sorted(p for p in run_dir.iterdir() if p.is_dir() and "try" not in p.name):
            # Only finished cells. A cell still running has records but no verdict, and
            # counting its partial revision history would mix "the gate refused this" with
            # "we looked before it was done".
            if not (cell / "discover-completed.json").exists():
                continue
            cells[cell.name] = _refusals(cell)
        if cells:
            rounds[run_dir.name] = cells
    if not rounds:
        raise SystemExit(f"{args.matrix_dir}: no cells with records found")

    flat = [c for cells in rounds.values() for c in cells.values()]
    summary = {
        "cells_measured": len(flat),
        # Same denominator as `over@1`, deliberately: the two are meant to be read together.
        "refuse@1": round(sum(c["total"] for c in flat) / len(flat), 2),
        "refuse@any": sum(1 for c in flat if c["total"]),
        "refuse_by_rule": dict(
            sum((collections.Counter(c["by_rule"]) for c in flat), collections.Counter())
        ),
        "partial_coverage_cells": sum(1 for c in flat if c.get("coverage_status") == "partial"),
        "coverage_gaps_total": sum(c.get("coverage_gaps", 0) for c in flat),
    }
    report = {"summary": summary, "rounds": rounds}

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    print(f"cells measured : {summary['cells_measured']}")
    print(f"refuse@1       : {summary['refuse@1']}   (same denominator as over@1)")
    print(f"refuse@any     : {summary['refuse@any']} cells")
    print(f"by rule        : {summary['refuse_by_rule']}")
    print(f"partial cells  : {summary['partial_coverage_cells']}")
    print(f"coverage gaps  : {summary['coverage_gaps_total']}\n")
    print(f"{'cell':<22}{'refused':>8}{'gaps':>6}{'issues':>8}  coverage / by rule")
    for run, cells in rounds.items():
        for name, data in cells.items():
            print(f"{run + '/' + name:<22}{data['total']:>8}{data.get('coverage_gaps', 0):>6}"
                  f"{data.get('issues', 0):>8}  {data.get('coverage_status')} / {data['by_rule']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
