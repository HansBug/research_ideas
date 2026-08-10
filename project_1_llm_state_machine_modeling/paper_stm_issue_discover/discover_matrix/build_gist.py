"""Render the 8-cell matrix into a publishable Gist bundle.

Two files per cell, as requested:

``PAIR-MODEL-readable.md``  a human-readable account of that single run --
    what was expected, what came out, every requirement with its predicate and
    bindings, every assertion with its role and sealed outcome, the attribution
    decision per False, the adjudication, the revision history and telemetry.
    The pair's NL / PlantUML / FCSTM inputs are embedded verbatim with SHA-256
    so the file can be checked without the repo.

``PAIR-MODEL-audit.json``  the machine-checkable counterpart: the terminal
    artifact plus every derived fact the readable file asserts, so a reader can
    recompute the tables rather than trust them.

Everything is read straight from the run bundle.  Nothing here is hand-written
per cell, so the narrative cannot drift from the evidence.

Usage: build_gist.py <matrix_dir> <out_dir>
"""

import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from audit_v4 import _segment_macro_sources, _walk  # noqa: E402
from issue_compat import requirement_ids_of, requirement_label  # noqa: E402

# Derived, not hardcoded: this script used to carry an absolute path that only
# worked on one machine, and it lives under version control now precisely so a
# rebuilt machine still has it.
HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(__file__).resolve().parents[3]
REPORT = (
    ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60"
)
PROFILE = {"gpt": "gpt-5.5", "claude": "claude-opus-4-7"}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def latest(blobs, key):
    """Return the last non-empty value seen for a key across the record stream."""

    out = None
    for b in blobs:
        for v in _walk(b, key):
            if v:
                out = v
    return out


def load_cell(d: pathlib.Path) -> dict:
    case, _, short = d.name.partition("-")
    rec = {"dir": d, "case": case, "short": short, "profile": PROFILE.get(short, short)}
    comp, fail = d / "discover-completed.json", d / "discover-failed.json"
    if comp.exists():
        rec["terminal"] = "completed"
        rec["final"] = json.loads(comp.read_text())
    elif fail.exists():
        rec["terminal"] = "failed"
        rec["final"] = json.loads(fail.read_text())
    else:
        rec["terminal"] = "missing"
        rec["final"] = {}
    blobs = []
    for f in sorted((d / "records").rglob("*.json")) if (d / "records").is_dir() else []:
        try:
            blobs.append(json.loads(f.read_text()))
        except Exception:
            pass
    rec["blobs"] = blobs

    rec["requirements"] = latest(blobs, "requirements") or []
    rec["assertions"] = latest(blobs, "assertions") or []
    rec["results"] = latest(blobs, "results") or []
    rec["bindings"] = latest(blobs, "bindings") or []
    rec["checks"] = latest(blobs, "executions") or []

    # Path taint is a property of the live simulation view, not something the
    # record stream carries: `_note_simulation` only leaves a marker when the
    # fired-transition derivation came back `ambiguous`, because a clean path
    # needs no annotation.  Counting a `path_taint` key in the records therefore
    # always yielded `{}` and made a working mechanism look inert.  Count the
    # markers that do get recorded, and count the calls that produced a usable
    # path alongside them so the ratio is visible.
    taint = collections.Counter()
    for b in blobs:
        for refs in _walk(b, "model_refs"):
            if not isinstance(refs, (list, tuple)):
                continue
            for ref in refs:
                if isinstance(ref, str) and ref.startswith("simulation:path_taint:"):
                    taint[ref.rsplit(":", 1)[-1]] += 1
                elif isinstance(ref, str) and ref.startswith("transition:"):
                    taint["fired_transition_refs"] += 1
    rec["taint"] = dict(taint)

    tel = collections.Counter()
    calls = 0
    for b in blobs:
        if b.get("schema_name") == "LLMCallRecord" or "llm_call_id" in b:
            calls += 1
            for k in (
                "input_tokens",
                "output_tokens",
                "total_tokens",
                "cache_read_input_tokens",
                "reasoning_tokens",
            ):
                v = b.get(k)
                if isinstance(v, (int, float)):
                    tel[k] += int(v)
    rec["llm_calls"] = calls
    rec["tokens"] = dict(tel)
    rec["elapsed_ms"] = sum(
        b.get("elapsed_ms", 0) or 0 for b in blobs if isinstance(b.get("elapsed_ms"), (int, float))
    )
    rec["node_failures"] = [
        {"node": b.get("node_name"), "revision": b.get("revision"), "failure": b.get("failure")}
        for b in blobs
        if isinstance(b.get("failure"), str)
    ]
    rec["gate_d"] = [
        f for f in rec["node_failures"] if "is decided by" in (f["failure"] or "")
    ]
    return rec


#: Model paths each expected issue is about, read out of its `eval_assert` in the
#: frozen ledger.  This is the judgement the whole matrix rests on, so it is
#: derived from the ledger rather than restated here.
_EXPECTED_PATHS: dict[str, dict[str, frozenset[str]]] = {}


#: The frozen ledger, and the reconstruction that stands in when it is absent.
#:
#: The ledger was lost in the 2026-07-29 machine rebuild -- never tracked by git,
#: not recoverable from the published bundles, which preserve verdicts but not the
#: `eval_assert` texts the hit criterion parses.  The reconstruction rebuilds only
#: those texts, from issue #166's authoritative inventory resolved against each
#: pair's own FCSTM, and covers four pairs.
#:
#: The real ledger wins whenever it is present, and which one was used is recorded
#: in every audit artifact.  A hit rate is a headline number; a reader has to be
#: able to see that it rested on a reconstruction without taking anyone's word.
LEDGER = (
    ROOT / ".omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json"
)
RECONSTRUCTED_LEDGER = (
    pathlib.Path(__file__).resolve().parent / "expected_issues_reconstructed.json"
)


def _expected_ledger_path() -> pathlib.Path:
    if LEDGER.exists():
        return LEDGER
    if RECONSTRUCTED_LEDGER.exists():
        return RECONSTRUCTED_LEDGER
    raise FileNotFoundError(
        f"no expected-issue ledger: neither {LEDGER} nor {RECONSTRUCTED_LEDGER}. "
        "Refusing to report hit rates without ground truth."
    )


def expected_ledger_provenance() -> str:
    """`frozen` or `reconstructed`, for the record every artifact carries."""

    return "frozen" if LEDGER.exists() else "reconstructed"


def _expected_paths(case: str) -> dict[str, frozenset[str]]:
    """`{expected_issue_id: paths its eval_assert names}` for one pair."""

    import re

    if case in _EXPECTED_PATHS:
        return _EXPECTED_PATHS[case]
    ledger = json.loads(_expected_ledger_path().read_text())
    found: dict[str, frozenset[str]] = {}

    def walk(node):
        if isinstance(node, dict):
            issue_id = str(node.get("issue_id", ""))
            if issue_id.startswith(f"EXP-{case}-"):
                assert_text = str(node.get("eval_assert", ""))
                pat = r"llms_emp_feedback_final_\d+\.[A-Za-z0-9_.]+"
                # Argument position separates the two kinds.  The event is what
                # makes an expected issue identifiable: each names a different
                # trigger, whereas their states overlap heavily -- both of pair
                # 0029's relation defects are about `HighwayMode` substates.
                events = {
                    m.rstrip(".")
                    for m in re.findall(r"event\s*=\s*'(" + pat + r")'", assert_text)
                }
                # `'...AutonomousMode.' + name` leaves a trailing dot behind.
                everything = {m.rstrip(".") for m in re.findall(pat, assert_text)}
                found[issue_id] = {
                    "events": frozenset(events),
                    "states": frozenset(everything - events),
                    "families": frozenset(node.get("required_function_families") or ()),
                }
            else:
                for value in node.values():
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(ledger)
    _EXPECTED_PATHS[case] = found
    return found



def _path_matches(bound: str, expected: str) -> bool:
    """Do these two paths denote the same model element for this purpose?

    Exact equality is too strict.  Pair 0006's expected assert names the leaf
    `UAVSwarmStateMachine.Attack.AttackingTarget`, while both models bound the
    enclosing composite `UAVSwarmStateMachine.Attack` -- the same defect, since
    `Attack_Complete` leaves the composite through that leaf, and marking it a
    miss would have understated the result.

    Plain prefix matching is too loose in the other direction: with it,
    `UAVSwarmStateMachine` alone would match, and 0006's unrelated cardinality
    finding is bound to exactly that.  One level of tolerance separates the two --
    a parent stands in for its child, a grandparent does not.
    """

    if bound == expected:
        return True
    for shorter, longer in ((bound, expected), (expected, bound)):
        if longer.startswith(shorter + "."):
            return longer[len(shorter) + 1 :].count(".") == 0
    return False


def _overlap(bound: set[str], expected: frozenset[str]) -> int:
    """How many of `expected` some binding denotes."""

    return sum(1 for e in expected if any(_path_matches(b, e) for b in bound))


#: 判定与记账两侧共用的那一份台账。发布层此前读的是另一份，见
#: `expected_records_for_judgment` 的说明。
EIS_LEDGER = HERE / "manual_review" / "expected_issue_set.json"


def _eis_records() -> list[dict]:
    payload = json.loads(EIS_LEDGER.read_text())
    records = payload.get("records")
    if not records:
        records = next(
            value
            for value in payload.values()
            if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0]
        )
    return [record for record in records if isinstance(record, dict)]


def _eis_sha256() -> str:
    """台账文件的哈希，写进审计包，使「读的是哪一份」可核验而不必相信一句 provenance。"""

    return hashlib.sha256(EIS_LEDGER.read_bytes()).hexdigest()


# hold-out 与分带机制已于 2026-08-09 永久移除：方法在这批 pair 上迭代，全部记录同等参与度量。
_REPORTABLE = frozenset()


def _round_tag(src: pathlib.Path) -> str:
    """`run1` / `run2` / `run3` from the source directory, or `""` when it is not a round dir.

    Needed because the bundle used to key files by `PAIR-PROFILE` alone, so building three rounds
    into one output directory silently kept only the last one -- and printed a success line three
    times while doing it.
    """

    name = src.resolve().name
    return name if _ROUND_DIR.match(name) else ""


_ROUND_DIR = re.compile(r"^run\d+$")


def expected_records_for_judgment(rec) -> list[tuple[str, str, str]]:
    """List this pair's ledger records with their eligibility. **No verdict.**

    This used to decide hit/miss mechanically, and shipping that in the published bundle was
    wrong twice over.

    First, it is the judgement `present_for_judgment.py` exists to forbid: two products in one
    generation touched the right elements and reached the *opposite* conclusion from the ledger,
    and any overlap-based matcher credits both as hits. The division of labour is that a human
    judges and scripts do arithmetic; a machine verdict in the audit bundle reinstates the thing
    the division was drawn to prevent.

    Second, it read a *different ledger*. `expected_verdicts` resolved through
    `.omx/specs/.../ledger.json` (`EXP-*`, 16 records inside the grid) while judging, the
    hold-out bookkeeping and `metrics_at_k.py` all read `manual_review/expected_issue_set.json`
    (`EIS-*`, 34). The consequence in the published bundle: pair `0032`, which holds the
    reportable record `EIS-0032-02`, got `"(本 pair 无期望问题)" / "0 confirmed 即为正解"`, beside
    an `expected_ledger_provenance: "frozen"` that reads as "this is the authoritative ledger".
    Two versions of one conclusion, and the optimistic one shipped.

    So this yields the raw material and stops: each `EIS-*` record for the pair, its layer, and
    its eligibility (reportable / burned / co-evolution observation). The verdict lives in the
    hand-written `verdicts.json` that `metrics_at_k.py` validates, and nowhere else.
    """

    rows = []
    pair = str(rec["case"])[-4:]
    for record in _eis_records():
        if str(record.get("pair", ""))[-4:] != pair:
            continue
        rid = str(record["id"])
        # 只剩两种资格。分带随 hold-out 于 2026-08-09 一并废止，「共演化观测」这个标签
        # 不再有对应的对象——留着它只会把越界记录贴成「参与过规则编写」，而那是两回事。
        if rid in _REPORTABLE:
            eligibility = "★可报——承载能力主张"
        elif record.get("boundary_ruling") == "out_of_scope":
            eligibility = "边界裁定剔除（表示层产物而非作者缺陷），不进能力分母"
        else:
            eligibility = "NL 越界（00x8），先验不进网格也不进分母"
        rows.append((rid, str(record.get("layer") or "?"), eligibility))
    if not rows:
        rows.append(("（本 pair 在 EIS 台账里无记录）", "—", "—"))
    return rows


def _legacy_binding_overlap_verdicts(rec) -> list[tuple[str, str, str]]:
    """No longer published. Still called by `test_ledger_reconstruction.py`, and only there.

    Removing it from the bundle was the point; removing it outright was not. Whether the
    reconstructed `EXP-*` ledger reproduces the frozen one's verdicts is a real consistency
    question, and this is how that test asks it -- inside the repository, never in a published
    artifact. The underscore marks the boundary: internal comparison, not a conclusion.

    Decide hit/miss per expected issue, by binding overlap rather than wording.

    The earlier version matched keywords against the issue *title*, which is
    LLM-written prose.  That is too loose to carry the matrix's headline claim:
    pair 0006's keyword set includes `数量`, and 0006-claude's unrelated
    cardinality finding is titled "直接子状态数量不等于三", so a finding about
    substate counts would have been credited as a hit for the expected
    *effect-absence* defect.

    The bindings are machine-checkable instead.  Each expected issue names a set
    of model paths in its `eval_assert`; a confirmed issue counts as hitting it
    when its requirement binds at least two of them -- or the single one, for an
    expected issue whose assert names only one.  Two overlapping paths is enough
    to fix identity (a source and a trigger, say) and few enough that a genuine
    hit is not rejected for using a different but equivalent predicate.
    """

    out = []
    final = rec["final"]
    issues = final.get("issues") or []
    # `rec["requirements"]` is the list the splitter emitted; index it here.
    reqs = {
        r.get("requirement_id"): r
        for r in (rec.get("requirements") or [])
        if isinstance(r, dict)
    }
    families = {
        a.get("assertion_id"): a.get("evidence_family")
        for a in (rec.get("assertions") or [])
        if isinstance(a, dict)
    }
    for eid, spec in sorted(_expected_paths(rec["case"]).items()):
        if rec["terminal"] != "completed":
            out.append((eid, "run 未完成", ""))
            continue
        want_events, want_states = spec["events"], spec["states"]
        hit = ""
        for issue in issues:
            # A merged issue rests on the bindings of every Requirement it covers, so the
            # bound-element set is their union rather than one Requirement's.
            bound = {
                str(v)
                for rid in requirement_ids_of(issue)
                for v in ((reqs.get(rid) or {}).get("predicate_bindings") or {}).values()
                if str(v) not in {"[*]", "<undeclared>"}
            }
            if want_events:
                # Every trigger the expected assert names must be bound exactly.
                # Without this, 0029's `initial_target` finding matched the guard
                # defect: its `HighwayMode` binding sits one level above both
                # `enter_hwy` and `lane_change`, so shape alone credited it with
                # two overlaps for an obligation it says nothing about.
                if not want_events <= bound:
                    continue
                if _overlap(bound, want_states) < 1:
                    continue
            else:
                # No trigger to key on, so the state must match and the evidence
                # must be of the kind the expected issue is about -- otherwise
                # 0029's structural defect gets credited to a behavioural finding
                # that merely mentions the same state.
                if _overlap(bound, want_states) < len(want_states):
                    continue
                observed = {
                    families.get(aid) for aid in (issue.get("assertion_ids") or [])
                }
                if spec["families"] and not (observed & spec["families"]):
                    continue
            hit = issue.get("title") or issue.get("issue_id") or ""
            break
        if hit:
            out.append((eid, "命中", hit))
        elif final.get("excluded_findings"):
            out.append((eid, "仅 excluded", ""))
        else:
            out.append((eid, "漏", ""))
    if not _expected_paths(rec["case"]):
        out.append(("（本 pair 无期望问题）", "0 confirmed 即为正解", ""))
    return out


def readable(rec, commit: str) -> str:
    case, prof = rec["case"], rec["profile"]
    final = rec["final"]
    L = []
    A = L.append
    A(f"# `{case}` × `{prof}` — Discover 单格可读报告\n")
    A("本文件由 `build_gist.py` 从该格 run bundle 确定性生成；每一项都能在同目录 "
      f"`{case}-{prof}-audit.json` 中复算。\n")

    A("## 1. 冻结身份\n")
    A("| 项 | 值 |")
    A("| --- | --- |")
    A(f"| pair | `{case}` |")
    A(f"| profile | `{prof}` |")
    A(f"| run_id | `{final.get('run_id', 'n/a')}` |")
    A(f"| 终态 | **{rec['terminal']}** |")
    A(f"| git commit | `{commit}` |")
    A("| 分支 | `paper1/pr-feedback-loop-discover-acceptance` |")
    A("| PR | [#169](https://github.com/HansBug/research_ideas/pull/169) |")
    A("| 谓词设计 | [Issue #170](https://github.com/HansBug/research_ideas/issues/170) |")
    A(f"| 覆盖 | `{final.get('coverage_status', 'n/a')}` |")
    A("")

    A("## 2. 本 pair 的台账记录与其资格（**不含判定**）\n")
    A("判定必须人工逐条做，理由见 `present_for_judgment.py`：同一代次有两条产出触及了正确的"
      "元素却得出与台账**相反**的结论，任何按重叠或措辞对齐的脚本都会把它们判成命中。"
      "本表只给判定所需的原材料；结论在人工 `verdicts.json` 里，由 `metrics_at_k.py` 校验。\n")
    A("| EIS 记录 | 层 | 资格 |")
    A("| --- | --- | --- |")
    for rid, layer, eligibility in expected_records_for_judgment(rec):
        A(f"| `{rid}` | {layer} | {eligibility} |")
    A("")

    A("## 3. 裁决\n")
    issues = final.get("issues") or []
    A(f"- confirmed issues: **{len(issues)}**")
    A(f"- excluded findings: **{len(final.get('excluded_findings') or [])}**")
    A(f"- satisfied requirements: **{len(final.get('satisfied_requirement_ids') or [])}**")
    A(f"- coverage gaps: **{len(final.get('coverage_gaps') or [])}**")
    A("")
    if issues:
        A("| issue | requirement | 归因 | 标题 |")
        A("| --- | --- | --- | --- |")
        for i in issues:
            A(f"| `{i.get('issue_id')}` | `{requirement_label(i)}` "
              f"| **{i.get('attribution_status')}** | {i.get('title')} |")
        A("")
    for e in final.get("excluded_findings") or []:
        A(f"- **excluded** `{e.get('requirement_id')}` "
          f"（{e.get('attribution_status')}）：{(e.get('title') or '')}")
    for g in final.get("coverage_gaps") or []:
        A(f"- **gap** `{g.get('gap_id')}` stage=`{g.get('stage')}` "
          f"reason=`{g.get('reason_code')}`：{(g.get('reason') or '')[:160]}")
    A("")

    A("## 4. 需求（含谓词与绑定）\n")
    A("| requirement | predicate | 派生 kind | bindings |")
    A("| --- | --- | --- | --- |")
    for r in rec["requirements"]:
        if not isinstance(r, dict):
            continue
        b = r.get("predicate_bindings") or {}
        bt = ", ".join(f"`{k}`=`{v}`" for k, v in b.items()) or "—"
        A(f"| `{r.get('requirement_id')}` | `{r.get('predicate') or '—'}` "
          f"| {r.get('verification_kind')} | {bt} |")
    A("")
    for r in rec["requirements"]:
        if isinstance(r, dict) and r.get("statement"):
            A(f"- `{r.get('requirement_id')}`：{r['statement']}")
            for lim in r.get("limitations") or []:
                A(f"    - limitation: {lim}")
    A("")

    A("## 5. 断言与执行\n")
    # `executions` carries the precheck status; the released results carry the
    # sealed truth value.  They are different stages and both matter.
    status = {
        c.get("assertion_id"): c.get("status")
        for c in rec["checks"] if isinstance(c, dict)
    }
    truth = {
        r.get("assertion_id"): r.get("truth_value")
        for r in rec["results"] if isinstance(r, dict)
    }
    A("| assertion | role | family | precheck | 结果 | 表达式 |")
    A("| --- | --- | --- | --- | --- | --- |")
    for a in rec["assertions"]:
        if not isinstance(a, dict):
            continue
        aid = a.get("assertion_id")
        tv = truth.get(aid)
        shown = "—" if tv is None else ("**False**" if tv is False else "True")
        expr = str(a.get("expression") or "").replace("|", "\\|")
        A(f"| `{aid}` | {a.get('role')} | {a.get('evidence_family')} "
          f"| {status.get(aid) or '—'} | {shown} | `{expr[:150]}` |")
    A("")

    A("## 6. 归因\n")
    if rec["bindings"]:
        A("| assertion | 归因 | source_refs | exclusion_refs |")
        A("| --- | --- | --- | --- |")
        for b in rec["bindings"]:
            if not isinstance(b, dict):
                continue
            A(f"| `{b.get('assertion_id')}` | **{b.get('status')}** "
              f"| {len(b.get('source_refs') or [])} 条 "
              f"| {', '.join(f'`{x}`' for x in (b.get('exclusion_refs') or [])) or '—'} |")
    else:
        A("*该格没有 False 断言需要归因。*")
    A("")
    A(f"路径污染分布：`{rec['taint'] or '（无仿真调用）'}`\n")

    A("## 7. 运行过程\n")
    A(f"- LLM 调用：**{rec['llm_calls']}** 次")
    A(f"- token：`{rec['tokens'] or 'n/a'}`")
    A(f"- 节点累计耗时：约 **{rec['elapsed_ms'] / 1000:.0f}s**")
    A(f"- 节点级失败（均由修复回路吸收）：**{len(rec['node_failures'])}** 次")
    for f in rec["node_failures"]:
        A(f"    - `{f['node']}` r{f['revision']}: {(f['failure'] or '')[:150]}")
    if rec["gate_d"]:
        A(f"- 其中谓词↔过程门（Issue #170 C3）拒绝：**{len(rec['gate_d'])}** 次")
    A("")

    A("## 8. 输入原文与哈希\n")
    for label, rel in (
        ("NL", f"pairs/{case}/nl.txt"),
        ("PlantUML STM_0", f"pairs/{case}/plantuml.puml"),
        ("FCSTM STM_0", f"pairs/{case}/fcstm.fcstm"),
    ):
        p = REPORT / rel
        text = p.read_text() if p.exists() else "(缺失)"
        A(f"### {label}  `sha256={sha(text)}`\n")
        A("```")
        A(text.rstrip())
        A("```\n")
    return "\n".join(L)


def audit_json(rec, commit: str) -> dict:
    final = rec["final"]
    inputs = {}
    for label, rel in (
        ("nl", f"pairs/{rec['case']}/nl.txt"),
        ("plantuml", f"pairs/{rec['case']}/plantuml.puml"),
        ("fcstm", f"pairs/{rec['case']}/fcstm.fcstm"),
    ):
        p = REPORT / rel
        inputs[label] = {"path": rel, "sha256": sha(p.read_text()) if p.exists() else None}
    return {
        "schema": "paper1.discover.cell_audit.v1",
        "generated_by": "runs/paper1/audit-20260727-claudecode/build_gist.py",
        "git_commit": commit,
        "pair": rec["case"],
        "profile": rec["profile"],
        "terminal": rec["terminal"],
        "inputs": inputs,
        # No verdict field. It used to carry a machine hit/miss decision computed off a second
        # ledger, which put an optimistic duplicate of the headline conclusion in the published
        # audit bundle. What ships now is the material a human needs and nothing more.
        "expected_records_for_judgment": [
            {"record": r, "layer": l, "eligibility": e}
            for r, l, e in expected_records_for_judgment(rec)
        ],
        "terminal_artifact": final,
        "requirements": rec["requirements"],
        "assertions": rec["assertions"],
        "sealed_executions": rec["checks"],
        "released_results": rec["results"],
        "attribution_bindings": rec["bindings"],
        "path_taint_distribution": rec["taint"],
        "telemetry": {
            "llm_calls": rec["llm_calls"],
            "tokens": rec["tokens"],
            "node_elapsed_ms": rec["elapsed_ms"],
        },
        "node_failures": rec["node_failures"],
        "predicate_procedure_gate_rejections": rec["gate_d"],
        # Which ledger the rows above came from, spelled out. The old field said `frozen` while
        # the rows came from a different file than every other consumer read.
        "expected_ledger": "manual_review/expected_issue_set.json",
        "expected_ledger_sha256": _eis_sha256(),
        "verdicts_live_in": "人工 verdicts.json（见 metrics_at_k.py --template）",
        "segment_macro_source_ids": sorted(_segment_macro_sources(rec["case"])),
    }


def write_fabrication_scan(data_dir: pathlib.Path, commit: str) -> int:
    """Write the audit bundle's fabrication scan; return how many findings it has.

    A gist that says "no fabricated findings" should carry the check, not the claim.
    Its own file rather than folded into each cell, because the scan is per run and
    needs the predicate layer -- which the per-cell audit deliberately does not.

    A scan that raises writes an `error` instead of a `findings` list, because an
    empty list and a missing file read identically to someone counting zeros.
    Returns -1 in that case, so a caller cannot mistake failure for zero.
    """

    scan_path = data_dir / "_fabrication_scan.json"
    cells = sorted(
        path.name.removesuffix("-audit.json")
        for path in data_dir.glob("*-audit.json")
    )
    try:
        import detect_fabrications

        findings = detect_fabrications.scan(data_dir)
    except Exception as exc:
        scan_path.write_text(
            json.dumps(
                {
                    "schema": "paper1.discover.fabrication_scan.v1",
                    "error": f"{type(exc).__name__}: {exc}",
                    "note": (
                        "The scan did not run, so this bundle carries no evidence "
                        "either way. Do not read its absence as a clean result."
                    ),
                    "git_commit": commit,
                    "cells_scanned": cells,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        print(f"  fabrication scan FAILED: {type(exc).__name__}: {exc}")
        return -1
    scan_path.write_text(
        json.dumps(
            {
                "schema": "paper1.discover.fabrication_scan.v1",
                "what_it_asks": (
                    "For every published issue: does its primary assertion still "
                    "re-derive to False against the current predicates, and does the "
                    "evidence that False rests on avoid every attribution_exclusions "
                    "entry? An issue failing either is not one the current layer "
                    "stands behind."
                ),
                "limitation": (
                    "It cannot distinguish a fabricated issue from one a later bug "
                    "made unanswerable. What it establishes is agreement between the "
                    "published issues and the predicates as they are."
                ),
                "git_commit": commit,
                "cells_scanned": cells,
                "findings": findings,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(f"  fabrication scan: {len(findings)} finding(s) -> {scan_path.name}")
    return len(findings)


def main() -> None:
    """Emit two separate bundles.

    The readable reports and the audit JSON go to different Gists on purpose:
    the prose bundle stays small enough to browse in one page, while the audit
    bundle is megabytes of machine-checkable evidence that would bury it.
    """

    # 最后一个参数是 out，其余全是轮次目录。上一版只取 argv[1] 与 argv[2]，于是文档里那条
    # `build_gist.py runs/.../run{1,2,3} <out>` 被 shell 展开成三个路径后，**run2 变成了输出
    # 目录**、run3 被丢弃、`<out>` 从未创建 —— 而它打印的是成功信息。那同时违反了「不回写
    # runs/」这条自己定的纪律。
    if len(sys.argv) < 3:
        raise SystemExit("usage: build_gist.py <round_dir> [<round_dir> ...] <out_dir>")
    sources = [pathlib.Path(a) for a in sys.argv[1:-1]]
    out = pathlib.Path(sys.argv[-1])
    # 三种都要拦，而上一版只拦了第二种：out 等于某个轮次目录、out 是它的祖先、out 落在 `runs/`
    # 之下的任何位置。最后一条是关键 —— 第一次写这个守卫时我漏了它，负控立刻用 §六 那条命令的
    # 真实故障形态打回来：`build_gist.py run1 run2` 把 run2 当成了 out 并**写进去了**。
    runs_root = ROOT / "runs"
    resolved_out = out.resolve()
    for source in sources:
        resolved_source = source.resolve()
        if resolved_out == resolved_source or resolved_out in resolved_source.parents:
            raise SystemExit(
                f"refusing to write into {out} -- it is (or contains) the run directory "
                f"{source}. Analysis products must not land in `runs/`."
            )
    if runs_root.exists() and (
        resolved_out == runs_root.resolve() or runs_root.resolve() in resolved_out.parents
    ):
        raise SystemExit(
            f"refusing to write into {out}: it is under `runs/`. Run bundles are evidence and "
            "analysis products must not be mixed into them -- see the same rule in "
            "V21_PREREGISTERED_CALIBRE.md §二.5."
        )
    combined: list[dict] = []
    for source in sources:
        combined += _build(source, out) or []
    if len(sources) > 1:
        # README 必须按**累计** index 重写一次。
        #
        # ## 为什么这是修复而不是又一次披露
        #
        # `_build` 每轮各写一次 README，后覆盖前 —— 于是一次传三个轮目录后，README 头部写的是
        # 「Cells completed: 22/22」而包里有 66 格。文件数是对的（数据完整），**只有摘要行被覆盖**。
        #
        # 我在 v23 的 PR comment 里**披露**过这件事（「README 头部是单轮口径」），但没修工具。结果
        # 它在 v24 又出现了 —— 而下一个读 gist 的人若没读到那句说明，就会以为只跑了 22 格。
        #
        # **披露不等于修复。** 当时选了便宜的那个，成本是每代次重复披露 + 依赖读者读到那句话。
        _rewrite_readmes(out, combined)
        print(f"wrote {len(sources)} rounds ({len(combined)} cells total) -> {out}")


def _rewrite_readmes(out: pathlib.Path, index: list[dict]) -> None:
    """按累计 index 重写两个 bundle 的 README 摘要行。

    只改**摘要那几行**（Matrix / Cells completed / Confirmed issues），其余散文与 commit 引用由
    `_build` 写好后保持不变 —— 那些内容与轮次无关。
    """

    import re as _re

    total_conf = sum(r.get("confirmed", 0) for r in index)
    done = sum(1 for r in index if r.get("terminal") == "completed")
    grid = sorted({str(r.get("pair"))[-4:] for r in index})
    profiles = sorted({str(r.get("profile")) for r in index})
    for name in ("readable", "audit"):
        path = out / name / "README.md"
        if not path.is_file():
            continue
        text = path.read_text()
        text = _re.sub(
            r"Matrix: [^\n]*\nCells completed: \d+/\d+\. Confirmed issues: \d+\.",
            (f"Matrix: {' / '.join(grid)} ({len(grid)} pairs), "
             f"under {' and '.join(profiles)}.\n"
             f"Cells completed: {done}/{len(index)}. Confirmed issues: {total_conf}."),
            text, count=1,
        )
        path.write_text(text)


def _build(matrix: pathlib.Path, out: pathlib.Path) -> list[dict]:
    """一轮的包。文件名带轮次前缀，`run-index.tsv` 追加而非覆盖。"""

    md_dir, data_dir = out / "readable", out / "audit"
    md_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()

    # `.try<N>` 是失败重试留下的作废目录，**必须排除**。首版没排，于是 `claude.try2` 被当成第三
    # 条臂，README 写出「under claude-opus-4-7 and claude.try2 and gpt-5.5」，且格数从 66 掉到 24、
    # confirmed issues 从 246 掉到 82 —— **没有任何报错**。
    #
    # 这是第 7 处按 `"try"` 排除作废目录的地方。我在决定「不改 `.try` 命名」时查了 6 处
    # （anchor_shift / count_refusals / generation_history / check_model_drift / blind_resample /
    # round_variance），**漏了这一处** —— 而它的症状恰好印证了当时的判断依据：改名会让每一处都
    # 静默出错，而我数不全有多少处。
    cells = [load_cell(d) for d in sorted(
        p for p in matrix.iterdir() if p.is_dir() and ".try" not in p.name)]
    # 轮次进文件名与索引。上一版 stem 是 `PAIR-PROFILE`，于是把三轮写进同一个 out 目录时
    # 后一轮覆盖前一轮：三次调用各打印 `wrote 11 cells`、无任何告警，最终 `run-index.tsv`
    # 只剩 run3。也就是说「一个可审计包」按文档入口**无法表示一个 3 轮代次**。
    round_tag = _round_tag(matrix)
    index = []
    for rec in cells:
        stem = f"{round_tag}-{rec['case']}-{rec['profile']}" if round_tag else f"{rec['case']}-{rec['profile']}"
        md = readable(rec, commit)
        aj = json.dumps(audit_json(rec, commit), ensure_ascii=False, indent=2, sort_keys=True)
        (md_dir / f"{stem}-readable.md").write_text(md)
        (data_dir / f"{stem}-audit.json").write_text(aj)
        f = rec["final"]
        index.append(
            {
                "round": round_tag or "?",
                "pair": rec["case"],
                "profile": rec["profile"],
                "terminal": rec["terminal"],
                "run_id": f.get("run_id", ""),
                "requirements": len(rec["requirements"]),
                "assertions": len(rec["assertions"]),
                "confirmed": len(f.get("issues") or []),
                "excluded": len(f.get("excluded_findings") or []),
                "satisfied": len(f.get("satisfied_requirement_ids") or []),
                "gaps": len(f.get("coverage_gaps") or []),
                "coverage": f.get("coverage_status", ""),
                "gate_d_rejections": len(rec["gate_d"]),
                "node_failures": len(rec["node_failures"]),
                "llm_calls": rec["llm_calls"],
                "total_tokens": rec["tokens"].get("total_tokens", 0),
                "node_elapsed_ms": round(rec["elapsed_ms"]),
                "taint_clean": rec["taint"].get("clean", 0),
                "taint_tainted": rec["taint"].get("tainted", 0),
                "taint_no_path": rec["taint"].get("no_path", 0),
                "taint_ambiguous": rec["taint"].get("ambiguous", 0),
                "readable_sha256": sha(md),
                "audit_sha256": sha(aj),
            }
        )
    # 跨轮**追加**。只写当前轮会让第二轮覆盖第一轮的索引，于是包里 33 份 audit 文件而索引
    # 只有 11 行 —— 而这份索引正是审计者用来确认「包里有几格」的东西。
    existing = []
    index_path = data_dir / "run-index.tsv"
    if index_path.is_file():
        lines = index_path.read_text().splitlines()
        if len(lines) > 1:
            header = lines[0].split("\t")
            existing = [dict(zip(header, line.split("\t"))) for line in lines[1:]]
    cols = list(index[0])
    merged = {}
    for row in existing + [{c: str(r[c]) for c in cols} for r in index]:
        merged[(row.get("round", "?"), row.get("pair", ""), row.get("profile", ""))] = row
    ordered = [merged[k] for k in sorted(merged)]
    tsv = (
        "\t".join(cols) + "\n"
        + "\n".join("\t".join(str(row.get(c, "")) for c in cols) for row in ordered) + "\n"
    )
    (md_dir / "run-index.tsv").write_text(tsv)
    index_path.write_text(tsv)
    # A per-cell mapping table for the PR comment.  The two gist ids are filled
    # in after publishing; keeping the row order and file names here means the
    # table cannot drift from what was actually uploaded.
    rows = [
        "| pair | model | 终态 | confirmed | 可读报告 | 审计数据 |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for r in index:
        stem = f"{r['pair']}-{r['profile']}"
        rows.append(
            f"| `{r['pair']}` | `{r['profile']}` | {r['terminal']} | {r['confirmed']} "
            f"| [`{stem}-readable.md`](READABLE_GIST#file-{stem.replace('.', '-').lower()}-readable-md) "
            f"| [`{stem}-audit.json`](AUDIT_GIST#file-{stem.replace('.', '-').lower()}-audit-json) |"
        )
    (out / "cell-table.md").write_text("\n".join(rows) + "\n")

    # Each bundle carries its own README: the readable gist explains how to read
    # a cell, the audit gist explains how to recompute one.  They are separate
    # gists because the audit JSON is megabytes and would bury the prose.
    total_conf = sum(r["confirmed"] for r in index)
    done = sum(1 for r in index if r["terminal"] == "completed")
    # Derived, not typed. The literal here said "0000 / 0006 / 0029 / 0050 ... under gpt-5.5 and
    # claude-opus-4-7" and "Cells completed: 11/11" while the bundle held eleven pairs under one
    # model -- so the audit package's self-declared scope disagreed with the data inside it. Same
    # class of error as the measurement script that carried its grid as a literal.
    grid = sorted({str(r["pair"])[-4:] for r in index})
    profiles = sorted({str(r["profile"]) for r in index})
    common = (
        f"Matrix: {' / '.join(grid)} ({len(grid)} pairs), "
        f"under {' and '.join(profiles)}.\n"
        f"Cells completed: {done}/{len(index)}. Confirmed issues: {total_conf}.\n\n"
        # 取用方式必须写在 **gist 自己的 README** 里，不能只写在 PR comment 里。
        #
        # v23 时我把这条截断警告只放进了 comment。但拿到 gist 链接的人（审计者最可能这样）看不到
        # comment —— 与同代次那个「指令正文说样本不含 NL 而实际含了」是同一类错误：**说明放在了
        # 读者看不到的地方**。
        "## ⚠️ Reading this gist through the API\n\n"
        "Large files here exceed the GitHub gist API's per-file `content` cap (~200 KB), so "
        "`.files[X].content` comes back **truncated** with `.files[X].truncated = true`. "
        "Note that the top-level `.truncated` (which reports whether the *file list* was "
        "truncated) is a **different field** and will read `false` -- reading that one instead "
        "is how the truncation gets missed.\n\n"
        "The raw URLs are complete. Fetch through them:\n\n"
        "```bash\n"
        "RAW=$(gh api gists/<id> -q '.files[\"<name>\"].raw_url')\n"
        "curl -sL \"$RAW\" | python3 -c 'import json,sys; json.load(sys.stdin)'\n"
        "```\n\n"
        f"Git commit `{commit}`, branch `paper1/pr-feedback-loop-discover-acceptance`, "
        "[PR #169](https://github.com/HansBug/research_ideas/pull/169), "
        "predicate design [Issue #170](https://github.com/HansBug/research_ideas/issues/170).\n\n"
        "This is an acceptance matrix for the predicate-only assertion layer, not a "
        "60-pair effectiveness result, and must not be read as one.\n\n"
        "## Read this before reading any number below\n\n"
        "**One run per cell, and a cell is not deterministic.** Pair 0000 under "
        "gpt-5.5 was run twice on code whose relevant paths were identical, and "
        "the two runs reported a different number of issues -- two "
        "(`HumanDrivingMode` and `AutonomousMode` separately) and then one "
        "(`HumanDrivingMode` only). Both hit the expected defect; they differed in "
        "how finely the splitter decomposed the sentence. Three consequences:\n\n"
        "1. **Issue counts are not a measurement.** `confirmed` varies between "
        "runs of the same cell, so it cannot be read as a measure of how well the "
        "method works.\n"
        "2. **Expected-defect hit/miss is the more stable signal**, and is the "
        "judgement this matrix is built to support.\n"
        "3. **A single before/after comparison cannot establish causation.** Every "
        "fix listed in the PR comment has a mechanism recorded in the run records "
        "that explains it, but distinguishing \"the fix worked\" from \"the sample "
        "moved\" needs repeated runs of the same configuration, which this matrix "
        "does not have.\n\n"
        "All eight cells were run on one commit; that removes code variance and "
        "does nothing about run-to-run variance.\n"
    )
    (md_dir / "README.md").write_text(
        "# Discover acceptance matrix - readable reports\n\n"
        + common
        + "\n## What is here\n\n"
        "One `PAIR-MODEL-readable.md` per cell: expected-issue outcome, adjudication, "
        "every requirement with its predicate and bindings, every assertion with its "
        "role and sealed verdict, per-False attribution, path-taint distribution, and "
        "telemetry. Each file embeds that pair's NL, PlantUML STM_0 and FCSTM STM_0 "
        "verbatim with SHA-256, so a cell can be checked without the repository.\n\n"
        "`run-index.tsv` is the ledger across all cells.\n\n"
        "The machine-checkable counterpart lives in a separate gist (see the PR "
        "comment); every table here can be recomputed from it.\n"
    )
    (data_dir / "README.md").write_text(
        "# Discover acceptance matrix - audit data\n\n"
        + common
        + "\n## What is here\n\n"
        "One `PAIR-MODEL-audit.json` per cell, schema "
        "`paper1.discover.cell_audit.v1`: the terminal artifact plus every derived "
        "fact the readable report asserts -- requirements, assertions, sealed "
        "executions, released results, attribution bindings, path-taint "
        "distribution, telemetry, node failures, predicate-procedure gate "
        "rejections, and the segment-macro source ids used for the taint "
        "blind-spot cross-check.\n\n"
        "`_fabrication_scan.json` carries the check behind any claim that the run "
        "published no fabricated findings: for every issue, whether its primary "
        "assertion still re-derives to False against the predicates at the recorded "
        "commit, and whether the evidence that False rests on avoids every "
        "`attribution_exclusions` entry. A `findings` list that is empty is the "
        "evidence; an `error` field means the scan did not run, and its absence must "
        "not be read as a clean result.\n\n"
        "The point is that a reader can recompute the published tables rather than "
        "trust them. `run-index.tsv` repeats the ledger so this gist stands alone.\n"
    )
    write_fabrication_scan(data_dir, commit)
    print(f"wrote {len(cells)} cells -> {out}")
    print(f"  readable bundle: {md_dir}")
    print(f"  audit bundle   : {data_dir}")
    return index


if __name__ == "__main__":
    main()
