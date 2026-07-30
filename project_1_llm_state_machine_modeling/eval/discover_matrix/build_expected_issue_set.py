"""Build the consolidated expected-issue set: one authoritative record per finding.

Why this exists rather than pointing at the old ledger: the frozen ledger at
`.omx/specs/.../ledger.json` was lost in the 2026-07-29 machine rebuild, was never tracked
by git, and is not recoverable. Only 5 of its 47 entries were ever reconstructed with a
machine-checkable `eval_assert` (the four pairs the 8-cell audit needed); the other 42 exist
solely as natural-language statements in issue #166. So a binding-level merge of old and new
is not possible -- the data for it does not exist.

The set is therefore built the other way round: **this set is the ledger**, and issue #166's
47 statements become a coverage checklist this set must account for, one by one.

Each record carries:

  id                  stable `EIS-<pair>-<seq>` identifier
  pair / group / llm  which cell of the 10 NL x 6 LLM design it belongs to
  statement           what is wrong, in natural language, quoting the NL clause it violates
  layer               which of the four admissible strata proves attributability
  direction           what kind of defect it is
  assertions[]        the assertion GROUP -- primary (from the predicate-coverage
                      batch, re-run), plus any corroborating or negative-control
                      expression recovered from the reviewer's notes
  upstream            ledger id / issue-166 statement / 8-cell issue ids / review diff index
  homogeneity_group    findings that describe one defect share a group; hit-rate counts
                      groups, not issue rows, so a model that splits one defect into three
                      reports does not inflate its own score

`assertions` is a list because a finding often needs more than one: the primary assertion
states the defect, a corroborating one pins a second consequence, and a negative control
proves the primary is not vacuously false. A single expression without a control is weak
evidence -- five of the 18 benign `extra` rows were rejected precisely because their
assertion also returns False on a correct model.

Usage: build_expected_issue_set.py [--json OUT] [--verify] [--limit N]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
MR = HERE / "manual_review"
PROJECT = HERE.parents[1]
CORPUS = (PROJECT / "paper_stm_repair/pipeline/representation/reports/llms_emp_r45_java_60")
FEEDBACK_SRC = PROJECT / "paper_stm_repair/pipeline/feedback_loop/src"

FAMILY = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S", "occupancy_after": "B", "event_consumed": "B",
    "stays_in": "B", "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}
#: The four strata that admit a finding, each naming *how* attributability is proven.
LAYER_BASIS = {
    "wellformedness": "模型自身即可判定，不需要 NL 也不需要参考模型",
    "nl_named": "NL 点名了那个缺失或错位的元素",
    "nl_contradiction": "与 NL 的显式义务矛盾",
    "over_specification": "生成方凭空多出，且造成可断言的负面后果",
}
_PATH = re.compile(r"llms_emp_feedback_final_\d{4}[\w.]*")
_CALL = re.compile(r"([A-Za-z_][A-Za-z_0-9]*)\s*\(")


def predicates_in(expr: str) -> list[str]:
    """Closed-vocabulary predicate names, outside quoted spans. Quoted spans matter:
    `invariant` takes a condition *string* whose own calls are not predicates."""
    bare = re.sub(r"(['\"]).*?\1", "''", expr or "", flags=re.S)
    out: list[str] = []
    for m in _CALL.finditer(bare):
        n = m.group(1)
        if n in FAMILY and n not in out:
            out.append(n)
    return out


def elements_in(expr: str) -> list[str]:
    return sorted(set(_PATH.findall(expr or "")))


def assertion_group(row: dict, batch: dict) -> list[dict]:
    """Assemble the assertion group for one finding.

    primary            the batch's rewritten, re-run expression (authoritative)
    negative_control   an expression the batch's note names as the control, which must
                       return True -- otherwise the primary is vacuously false
    corroborating      a second measured consequence, where the reviewer recorded one
    """
    out: list[dict] = []
    expr = (batch.get("assertion") or "").strip()
    if expr:
        preds = predicates_in(expr)
        out.append({
            "role": "primary", "expression": expr, "predicates": preds,
            "families": sorted({FAMILY[p] for p in preds}),
            "elements": elements_in(expr),
            "measured_by_batch": batch.get("measured_raw", batch.get("measured")),
            "source": f"predicate_coverage/result{batch.get('batch')}.json",
            "rewrote_from": (batch.get("rewrote_from") or "").strip() or None,
        })
    # Controls and corroborations live in free text; recover the expressions from it rather
    # than dropping them, but mark them as recovered so nobody mistakes them for structured
    # fields the batch guaranteed.
    for field, why in (("note", batch.get("note")),
                       ("harm_verified", row.get("harm_verified")),
                       ("harm_assertion", row.get("harm_assertion"))):
        text = (why or "")
        if not text:
            continue
        for m in re.finditer(r"((?:not\s+)?[A-Za-z_][A-Za-z_0-9]*\([^()]*(?:\([^()]*\))?[^()]*\))",
                             text):
            e = m.group(1).strip()
            if not predicates_in(e) or any(a["expression"] == e for a in out):
                continue
            ctx = text[max(0, m.start() - 60):m.start()]
            role = ("negative_control" if re.search(r"负控|control|对照|正控", ctx)
                    else "corroborating")
            out.append({
                "role": role, "expression": e, "predicates": predicates_in(e),
                "families": sorted({FAMILY[p] for p in predicates_in(e)}),
                "elements": elements_in(e), "source": f"recovered_from:{field}",
                "context": re.sub(r"\s+", " ", ctx)[-90:],
            })
    # Primary first, so a consumer reading `assertions[0]` always gets the assertion of
    # record rather than whichever expression happened to be recovered first.
    out.sort(key=lambda a: {"primary": 0, "negative_control": 1,
                            "corroborating": 2}.get(a["role"], 3))
    return out


def load_predicate_batches():
    """The assertion of record comes from the predicate-coverage batches, not from the
    reviewer's original `assertable` field.

    That distinction matters and cost a wrong number once: the original `assertable` was
    written during the pair review as shorthand -- often prose, often an unqualified path --
    and re-running those yields 37 `None`. The batches later rewrote each one into a runnable
    closed-vocabulary expression and recorded its measured value; that rewrite is what the
    123/153 coverage figure is about. Using the original field here would have silently
    reported a different, worse number for the same findings."""
    out = {}
    for n in range(1, 6):
        f = MR / f"predicate_coverage/result{n}.json"
        if not f.exists():
            continue
        for item in json.loads(f.read_text()).get("items") or []:
            out[(item["case"], item["diff_index"])] = item
    return out


def load_upstream():
    """Ledger ids, issue-166 statements and the 8-cell published issue ids, per pair."""
    ledger_stmt, ledger_assert = {}, {}
    recon = HERE / "expected_issues_reconstructed.json"
    if recon.exists():
        def walk(o):
            if isinstance(o, dict):
                if "issue_id" in o:
                    iid = o["issue_id"]
                    if o.get("issue_166_statement"):
                        ledger_stmt[iid] = o["issue_166_statement"]
                    if o.get("eval_assert"):
                        ledger_assert[iid] = o["eval_assert"]
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(json.loads(recon.read_text()))

    cell_pub = defaultdict(list)
    cells = MR / "loop_audit/cells.json"
    if cells.exists():
        for c in json.loads(cells.read_text()).get("cells") or []:
            for p in c.get("published") or []:
                iid = p.get("issue_id") or p.get("id") if isinstance(p, dict) else str(p)
                if iid:
                    cell_pub[c["pair"]].append({"cell": c["cell"], "issue_id": iid})
    return ledger_stmt, ledger_assert, cell_pub


def build() -> dict:
    fin = json.loads((MR / "final_stratification.json").read_text())
    admissible = set(fin["admissible_strata"])
    verified = json.loads((MR / "predicate_coverage/verified_assertions.json").read_text())
    vidx = {(r["case"], r["diff_index"]): r
            for r in verified.get("rows", []) + verified.get("not_expressible", [])}
    defects = json.loads((MR / "defect_classification.json").read_text())
    didx = {(r["case"], r["diff_index"]): r for r in defects["rows"]}
    scope = json.loads((MR / "loop_audit/scope.json").read_text())
    sidx = {(r["case"], r["diff_index"]): r for r in scope.get("items") or []}

    reviews = {}
    for path in sorted(MR.glob("*-review.json")):
        r = json.loads(path.read_text())
        reviews[r["case"]] = r

    ledger_stmt, ledger_assert, cell_pub = load_upstream()
    batches = load_predicate_batches()

    records, seq = [], Counter()
    for row in fin["rows"]:
        if row["stratum"] not in admissible:
            continue
        case, ix = row["case"], row["diff_index"]
        review = reviews[case]
        diff = review["diffs"][ix]
        cross = review.get("cross_reference") or {}
        seq[case] += 1
        batch = batches.get((case, ix)) or {}
        group = assertion_group(row, batch)
        v = vidx.get((case, ix)) or {}
        d = didx.get((case, ix)) or {}
        s = sidx.get((case, ix)) or {}
        e1 = ((cross.get("ledger") or {}).get("e1_ids") or [])
        records.append({
            "id": f"EIS-{case}-{seq[case]:02d}",
            "pair": case, "group": cross.get("group"), "llm": cross.get("llm"),
            "statement": (diff.get("reason") or "").strip(),
            "reference_side": (diff.get("ref") or "").strip(),
            "generated_side": (diff.get("gen") or "").strip(),
            "verdict": diff["verdict"],
            "layer": row["stratum"],
            "layer_basis": LAYER_BASIS[row["stratum"]],
            "decided_by": row.get("decided_by"),
            "nl_evidence": row.get("nl_evidence") or "",
            "direction": d.get("direction"),
            "element_of_M": s.get("element_of_M") or s.get("element"),
            "in_scope": s.get("ruling") != "out_of_scope",
            "assertions": group,
            "primary_predicate": (group[0]["predicates"][0]
                                  if group and group[0]["predicates"] else None),
            "assertion_count": len(group),
            "has_negative_control": any(a["role"] == "negative_control" for a in group),
            "expressible_with_closed_vocabulary": bool(group),
            "replay": {"verdict": v.get("verified_verdict"), "value": v.get("verified_raw")},
            "superseded_assertion": row.get("assertable_superseded"),
            "parent_ruling": bool(row.get("parent_ruling")),
            "upstream": {
                "review_file": f"{case}-review.json", "diff_index": ix,
                "ledger_e1_ids_on_this_pair": e1,
                "ledger_statements": {i: ledger_stmt[i] for i in e1 if i in ledger_stmt},
                "ledger_eval_asserts": {i: ledger_assert[i] for i in e1 if i in ledger_assert},
                "eight_cell_published": cell_pub.get(case, []),
                "paper_f1_phase2": (cross.get("paper") or {}).get("f1_phase2"),
            },
        })

    # Homogeneity groups: identical binding (same predicate + same element set) on the same
    # pair is one defect described twice. This is the machine-decidable half of the
    # "same defect?" question; anything subtler stays a human call and is not grouped here.
    by_binding = defaultdict(list)
    for r in records:
        a = r["assertions"][0] if r["assertions"] else None
        key = (r["pair"], a["predicates"][0] if a and a["predicates"] else None,
               tuple(a["elements"]) if a else ())
        by_binding[key].append(r["id"])
    hg = {}
    per_pair = Counter()
    for key, ids in sorted(by_binding.items(), key=lambda kv: kv[1]):
        per_pair[key[0]] += 1          # sequence within the pair, not across the corpus
        gid = f"HG-{key[0]}-{per_pair[key[0]]:02d}"
        for i in ids:
            hg[i] = gid
    for r in records:
        r["homogeneity_group"] = hg[r["id"]]
        r["homogeneity_group_size"] = sum(1 for x in records
                                          if hg[x["id"]] == hg[r["id"]])

    groups = {g for g in hg.values()}
    return {
        "schema": "paper1.expected_issue_set.v1",
        "what_this_is":
            "LLMS-EMP 60 对的合并 expected issue 集合。每条含自然语言描述、归因层、"
            "缺陷方向、断言组（primary / corroborating / negative_control）与上游关联。"
            "旧台帐 ledger.json 已在 2026-07-29 机器重建中丢失且不可恢复，其 47 条中仅 5 条"
            "被重建出机器可比的 eval_assert，故本集合不与旧台帐做 binding 级合并，"
            "而是以本集合为台帐、以 issue #166 的 47 条陈述作为需逐条交代的覆盖清单。",
        "counting_conventions": {
            "records": "一条 expected issue 一条记录",
            "homogeneity_group":
                "同 pair 上 primary 谓词与元素集合完全相同者视为同一缺陷。"
                "命中率的分子与分母都应按同质组计，不按记录条数计，"
                "否则把一个缺陷报成三条的模型会虚高。",
            "assertion_group":
                "断言组内 primary 陈述缺陷，corroborating 补第二个后果，"
                "negative_control 证明 primary 不是恒假。无负控的单表达式是弱证据。",
        },
        "totals": {
            "records": len(records),
            "homogeneity_groups": len(groups),
            "pairs_covered": len({r["pair"] for r in records}),
            "by_layer": dict(Counter(r["layer"] for r in records)),
            "by_direction": dict(Counter(r["direction"] for r in records)),
            "by_primary_predicate": dict(Counter(r["primary_predicate"] for r in records)),
            "by_llm": dict(Counter(r["llm"] for r in records)),
            "by_group": dict(Counter(r["group"] for r in records)),
            "assertion_count_distribution": dict(Counter(r["assertion_count"]
                                                         for r in records)),
            "with_negative_control": sum(1 for r in records if r["has_negative_control"]),
            "with_parent_ruling": sum(1 for r in records if r["parent_ruling"]),
            "on_pairs_with_ledger_e1": sum(
                1 for r in records if r["upstream"]["ledger_e1_ids_on_this_pair"]),
        },
        "records": records,
    }


def verify(payload: dict, limit: int | None = None) -> dict:
    """Re-evaluate every primary assertion. A set whose assertions were never re-run is a
    claim, not evidence."""
    if str(FEEDBACK_SRC) not in sys.path:
        sys.path.insert(0, str(FEEDBACK_SRC))
    from paper_stm_feedback_loop.assertions import build_eval_environment

    envs: dict[str, object] = {}

    def env(case: str):
        if case not in envs:
            stem = f"llms_emp_feedback_final_{case}"
            trace = json.loads((CORPUS / f"source_traces/{stem}.json").read_text())
            envs[case] = build_eval_environment(
                model_text=(CORPUS / f"fcstm/{stem}.fcstm").read_text(),
                source_mappings=trace.get("mappings") or [],
                source_exclusions=trace.get("attribution_exclusions") or [],
                timeout_seconds=60, fbmcq_solver_timeout_ms=5000,
                fbmcq_max_bound=3, fbmcq_process_wall_seconds=15.0)
        return envs[case]

    tally = Counter()
    rows = payload["records"][:limit] if limit else payload["records"]
    for r in rows:
        for a in r["assertions"]:
            expr = a["expression"]
            # Only bare expressions are runnable; prose-wrapped ones are recorded, not run.
            if not re.match(r"^(not\s+)?[A-Za-z_][A-Za-z_0-9]*\s*\(", expr):
                a["measured"] = "not_a_bare_expression"
                tally["skipped_prose"] += 1
                continue
            try:
                a["measured"] = repr(env(r["pair"]).eval_assert(expr, r["id"]).value)
            except Exception as exc:  # noqa: BLE001
                a["measured"] = f"{type(exc).__name__}: {exc}"[:150]
            tally[a["role"] + ":" + str(a["measured"])[:5]] += 1
    # A control is only a control if it actually holds. The role was assigned from prose
    # context, so demote anything that did not measure True -- an unverifiable "control"
    # provides no protection against a vacuously-false primary, and counting it as one would
    # overstate the evidence.
    demoted = 0
    for r in payload["records"]:
        for a in r["assertions"]:
            if a["role"] == "negative_control" and a.get("measured") != "True":
                a["role"] = "recovered_unverified"
                a["demoted_because"] = f"负控须实测为 True，实测 {a.get('measured')}"
                demoted += 1
            elif a["role"] == "corroborating" and a.get("measured") not in ("False", "True"):
                a["role"] = "recovered_unverified"
                a["demoted_because"] = f"从散文恢复的表达式不可求值（{a.get('measured')}）"
        r["has_negative_control"] = any(a["role"] == "negative_control"
                                       for a in r["assertions"])
        prim = [a for a in r["assertions"] if a["role"] == "primary"]
        r["automatable"] = bool(prim) and prim[0].get("measured") == "False"
    payload["totals"]["with_negative_control"] = sum(
        1 for r in payload["records"] if r["has_negative_control"])
    payload["totals"]["automatable"] = sum(1 for r in payload["records"] if r["automatable"])
    payload["totals"]["needs_human_judgement"] = sum(
        1 for r in payload["records"] if not r["automatable"])
    payload["verification"] = {
        "demoted_recovered_expressions": demoted,
        "what_ran": "对每条记录的断言组逐条重新求值。primary 返回 False 才算该缺陷被捕获；"
                    "negative_control 应返回 True，否则该 primary 是恒假、不成立。",
        "tally": dict(tally),
        "records_checked": len(rows),
    }
    return payload


def main() -> int:
    payload = build()
    if "--verify" in sys.argv:
        lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
        payload = verify(payload, lim)
    t = payload["totals"]
    print(f"expected issue set：**{t['records']}** 条记录，"
          f"归入 **{t['homogeneity_groups']}** 个同质组，覆盖 {t['pairs_covered']} 个 pair\n")
    print("| 归因层 | 条数 | 判据 |")
    print("| --- | ---: | --- |")
    for k, v in sorted(t["by_layer"].items(), key=lambda kv: -kv[1]):
        print(f"| `{k}` | {v} | {LAYER_BASIS[k]} |")
    print(f"\n断言组规模分布：{t['assertion_count_distribution']}")
    print(f"带（实测有效）负控的记录：{t['with_negative_control']} / {t['records']}")
    if "automatable" in t:
        print(f"可自动验收（primary 实测 False）：{t['automatable']} / {t['records']}")
        print(f"须人工判定（19 谓词表述不出）：{t['needs_human_judgement']}")
    print(f"经主裁定的记录：{t['with_parent_ruling']}")
    if "verification" in payload:
        print(f"\n复跑：{json.dumps(payload['verification']['tally'], ensure_ascii=False)}")
    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
