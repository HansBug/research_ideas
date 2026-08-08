"""How many corpus models a gate can fire on, computed rather than asserted.

A gate's defence against being a special case is the set of models it acts on: a rule that
only ever fires on the samples it was written from is a special case however generally it is
worded. That set is the one quantitative part of the claim, and it is the part that has been
wrong every time it was written by hand.

The v21 `B1` commit body is the worked example. It claimed `37/60` pairs with `29` outside
both measured sets. Two independent recomputations produced `24/60` and `42/60`; a third,
using a different definition, produced the trivially-true `60/60`. Four numbers, none
reproducing another, for a claim that was the sole evidence that the rule generalises. The
error was using nesting depth as a proxy: depth 3 guarantees one composite, while the pair
the rule newly catches needs two *distinct* composite branches.

So the measurement moves out of prose and into here, read through the same `pyfcstm` facade
`corpus_census.py` uses -- no regex over the DSL, no depth proxies. Each rule states the
structural precondition it needs; this reports which pairs satisfy it, split by whether the
pair took part in authoring any rule.

Grouping matters as much as the count. `holdout.json` records that the 60 models are 10 NL
specifications crossed with 6 producers, and that a rule written against one member of an NL
group acts on every member -- same requirement text, same reference model. A count of pair
ids that ignores groups can report out-of-sample coverage that does not exist, so both are
printed and the group figure is the one to quote.

Usage: measure_rule_surface.py [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
REPORTS = (
    REPO
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation"
    / "reports/llms_emp_r45_java_60"
)
FL_SRC = (
    REPO
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src"
)
if str(FL_SRC) not in sys.path:
    sys.path.insert(0, str(FL_SRC))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402

# hold-out 与分带机制已于 2026-08-09 永久移除：方法在这批 pair 上迭代，全部记录同等参与度量。
HELD: set[str] = set()
#: The four pairs eighteen generations of gates and prompts were written against.
TUNED = {"0000", "0006", "0029", "0050"}


def _nl_groups() -> dict[str, str]:
    """pair id -> digest of its NL text, so members of one group can be seen as one."""
    groups: dict[str, str] = {}
    for nl in sorted(REPORTS.glob("pairs/*/nl.txt")):
        groups[nl.parent.name[-4:]] = hashlib.md5(nl.read_bytes()).hexdigest()[:8]
    return groups


def _states(pair_path: pathlib.Path) -> list:
    trace_path = REPORTS / f"source_traces/{pair_path.stem}.json"
    trace = json.loads(trace_path.read_text()) if trace_path.exists() else {}
    env = build_eval_environment(
        model_text=pair_path.read_text(encoding="utf-8"),
        source_mappings=trace.get("mappings") or [],
        source_exclusions=trace.get("attribution_exclusions") or [],
        timeout_seconds=60,
        fbmcq_solver_timeout_ms=5_000,
        fbmcq_max_bound=3,
        fbmcq_process_wall_seconds=15.0,
    )
    entry = env._raw_functions["occupancy_after"]
    api = next(
        x.__self__
        for x in (entry if isinstance(entry, tuple) else (entry,))
        if hasattr(x, "__self__")
    )
    return list(api.structure.states())


def _nested(a: str, b: str) -> bool:
    return a.startswith(f"{b}.") or b.startswith(f"{a}.")


def _surfaces(states: list) -> dict[str, bool]:
    """Which rules have something to act on in this model.

    `a1_transient_subject` -- at least one node the projection renders as a pseudo-state.
        Where a `<<fork>>` carries a body it projects to a composite and `is_pseudo` is
        False, so this counts triggers, not occurrences of the modelling concept.

    `b1_nonnested_pair_new` -- at least one non-nested pair with *different* parents. The
        same-parent case is what the rule already caught before the generalisation, so
        counting it would report the old rule's surface as the new one's.
    """
    paths = [str(getattr(s, "path", "")) for s in states]
    paths = [p for p in paths if p]
    pseudo = any(bool(getattr(s, "is_pseudo", False)) for s in states)
    new_pair = False
    for index, left in enumerate(paths):
        for right in paths[index + 1 :]:
            if _nested(left, right) or left == right:
                continue
            if "." not in left and "." not in right:
                continue
            if left.rsplit(".", 1)[0] != right.rsplit(".", 1)[0]:
                new_pair = True
                break
        if new_pair:
            break
    return {"a1_transient_subject": pseudo, "b1_nonnested_pair_new": new_pair}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    groups = _nl_groups()
    per_pair: dict[str, dict[str, bool]] = {}
    for path in sorted((REPORTS / "fcstm").glob("*.fcstm")):
        pair = path.stem.replace("llms_emp_feedback_final_", "")
        per_pair[pair] = _surfaces(_states(path))

    report: dict[str, dict] = {"total_pairs": len(per_pair), "rules": {}}
    for rule in ("a1_transient_subject", "b1_nonnested_pair_new"):
        firing = {p for p, s in per_pair.items() if s[rule]}
        outside = firing - HELD - TUNED
        authoring_groups = {groups.get(p) for p in (HELD | TUNED) & firing}
        # A pair outside the measured sets is still not independent evidence if it shares an
        # NL group with a pair that is: same requirement text, same reference model.
        clean = {p for p in outside if groups.get(p) not in authoring_groups}
        report["rules"][rule] = {
            "fires_on_pairs": sorted(firing),
            "count": len(firing),
            "in_holdout": sorted(firing & HELD),
            "in_tuned": sorted(firing & TUNED),
            "outside_by_pair_id": sorted(outside),
            "outside_and_in_a_clean_nl_group": sorted(clean),
            "verdict": (
                "no out-of-sample trigger evidence"
                if not clean
                else f"{len(clean)} pair(s) outside every authoring NL group"
            ),
        }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    print(f"corpus: {report['total_pairs']} pairs\n")
    for rule, data in report["rules"].items():
        print(f"{rule}")
        print(f"  fires on            : {data['count']} / {report['total_pairs']}")
        print(f"  in hold-out         : {data['in_holdout']}")
        print(f"  in tuned four       : {data['in_tuned']}")
        print(f"  outside by pair id  : {len(data['outside_by_pair_id'])}")
        print(f"  outside AND in a clean NL group : {data['outside_and_in_a_clean_nl_group']}")
        print(f"  -> {data['verdict']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
