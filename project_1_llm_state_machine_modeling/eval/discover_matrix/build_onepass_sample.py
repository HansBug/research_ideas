"""一次标注、两侧派生：判定单元改为 (格, 轮)，判定者对**每一条 issue** 恰好给一个标签。

## 为什么换结构，而不是加一道检查

上一代次的 `台账命中 / 台账外` 划分**不闭合**：覆盖侧用人工判定表、多报侧用机械匹配的补集，两个
不同的匹配器切同一批已发布 issue，实测 **23/82 = 28.0%** 的多报项其底层 issue 在判定表里已被记为该轮
命中。而 `metrics_at_k.validate()` 里没有任何校验能发现这件事。

加一道检查（`check_partition_closure.py` 已经加了）只能**事后发现**。要让它**不可能发生**，得改判定
的形状：

    判定单元 = (格, 轮)
    每个 item = 该 pair 的全部台账条目 + 该格该轮**全部**已发布 issue（带稳定 `issue_uid`）
    判定者对**每一条 issue** 恰好给一个标签：
        hits:<EIS-id> | grounded-extra | boundary | fabricated | duplicate-of:<issue_uid>

派生：

    覆盖侧  H(记录, 臂, 轮) = 1  ⟺  存在 issue 标 `hits:<该记录>`
    多报侧  over@1 = `fabricated` 计数

于是不变量 `hit-evidence ∩ 台账外 = ∅` **靠构造成立** —— 一条 issue 只有一个标签，它不可能同时落进
两个计数。「同一份判据、同一批判定者」也自动满足，因为**两侧不再是两个任务**。

## 与逐带盲判样本的关系

`blind_resample.py` 建的是「每个台账记录 × 臂」为单元的样本，问「这条缺陷被发现了吗」。本工具建的是
「每格每轮」为单元的样本，问「这条 issue 是什么」。**后者能派生前者，前者不能派生后者** —— 这是换
结构的实质收益，也是为什么不能靠给旧结构打补丁。

盲化沿用同一套：pair id、台账记录 id、模型路径前缀替别名，带标签不出现，`sample_id` 含代次。

## issue_uid 的稳定性

`(run, cell, index)` —— index 是该轮 issues 列表里的位置。它在冻结的 run record 上是稳定的，且
`duplicate-of` 需要一个能指向另一条 issue 的键。**不用 title**：title 由模型写、轮间会变，而这正是
`round_variance` 的 docstring 记着不能用它做身份的原因。
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "onepass_sample"
RUNS = HERE.parents[2] / "runs" / "paper1"
_LEAK = re.compile(r"\b\d{4}\b|EIS-|llms_emp_feedback_final")
_BAND_WORDS = ("调优", "留出", "已烧毁", "可报", "hold-out", "holdout", "tuned", "burned")
TUNED_PAIRS = ("0000", "0006", "0029", "0050")


def _scrub(text: str) -> str:
    text = re.sub(r"llms_emp_feedback_final_\d{4}", "M", text)
    return re.sub(r"\b\d{4}\b", "NNNN", text)


def _ledger() -> dict[str, list[dict]]:
    payload = json.loads((HERE / "manual_review" / "expected_issue_set.json").read_text())
    records = payload.get("records") or next(
        v for v in payload.values()
        if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]
    )
    out: dict[str, list[dict]] = collections.defaultdict(list)
    for record in records:
        # 只收**可判定**记录，与 `blind_resample` 同一条口径：把闭词表表达不了的记录放进分母，
        # 会**把方法边界报成能力缺口**（`holdout.py` 规则 4 的 rationale 明写禁止）。
        if not (record.get("in_scope") is True
                and record.get("expressible_with_closed_vocabulary") is True):
            continue
        out[str(record.get("pair", ""))[-4:]].append(record)
    return dict(out)


def _band(pair: str, record_id: str, reportable: set[str]) -> str:
    if pair in TUNED_PAIRS:
        return "hist"
    return "reportable" if record_id in reportable else "burned"


def build(generation: str) -> tuple[dict, dict]:
    base = RUNS / f"matrix-{generation}"
    if not base.is_dir():
        raise SystemExit(f"ERROR: no {base}")
    ledger = _ledger()
    frozen = json.loads((HERE / "holdout.json").read_text())
    reportable = set(frozen.get("reportable_records") or [])

    units = []
    for run_dir in sorted(base.glob("run*")):
        if not (run_dir.name.startswith("run") and run_dir.name[3:].isdigit()):
            continue
        for cell in sorted(p for p in run_dir.iterdir() if p.is_dir() and ".try" not in p.name):
            final = cell / "discover-completed.json"
            if not final.is_file() or "-" not in cell.name:
                continue
            pair, arm = cell.name.rsplit("-", 1)
            entries = ledger.get(pair) or []
            if not entries:
                continue
            payload = json.loads(final.read_text())
            issues = payload.get("issues") or []
            units.append({
                "run": run_dir.name, "pair": pair, "arm": arm,
                "entries": entries, "issues": issues,
            })
    if not units:
        raise SystemExit(f"ERROR: no judgeable (cell, round) units under {base}")

    alias: dict[str, str] = {}
    for unit in units:
        alias.setdefault(unit["pair"], f"PAIR-{chr(65 + len(alias))}")

    mapping = "\n".join(
        f"{u['run']}|{u['pair']}|{u['arm']}|{len(u['issues'])}" for u in units
    )
    sample_id = hashlib.sha256(f"onepass:{generation}\n{mapping}".encode()).hexdigest()[:16]

    sample = {
        "schema": "OnePassAnnotation/v1",
        "generation_alias": "GEN",
        "sample_id": sample_id,
        "unit_count": len(units),
        "task": (
            "对每个 unit 里的**每一条** issue 恰好给一个标签："
            "`hits:<record_id>`（它主张的缺陷与该台账条目语义同一，按 HIT_CRITERION.md 的四种形态）"
            " / `grounded-extra`（对着 NL 站得住，但不对应本 unit 任何台账条目）"
            " / `boundary`（涉时钟、时间约束或正交区并发 —— 不在建模对象内）"
            " / `fabricated`（在模型上不成立，或 NL 上无依据）"
            " / `duplicate-of:<issue_uid>`（与本 unit 另一条 issue 是同一命题）。"
            "**一条 issue 只能有一个标签。** 台账条目没有任何 issue 标 `hits:` 的，即该轮未被发现。"
        ),
        "items": [],
    }
    key = {"schema": "OnePassAnnotation/v1", "sample_id": sample_id,
           "pair_alias": alias, "items": []}

    for index, unit in enumerate(units, 1):
        unit_id = f"C{index:03d}"
        a = alias[unit["pair"]]
        sample["items"].append({
            "unit_id": unit_id,
            "model_alias": a,
            "arm": unit["arm"],
            "round_alias": f"R{unit['run'][3:]}",
            "expected_defects": [
                {"record_alias": f"{a}-REC-{n:02d}",
                 "layer": e.get("layer"),
                 "statement": _scrub(str(e.get("statement") or ""))}
                for n, e in enumerate(unit["entries"], 1)
            ],
            "published_issues": [
                {"issue_uid": f"{unit_id}-I{n:02d}",
                 "title": _scrub(str(i.get("title") or i.get("summary") or "")),
                 "detail": _scrub(str(i.get("detail") or i.get("rationale") or ""))[:700]}
                for n, i in enumerate(unit["issues"], 1)
            ],
        })
        key["items"].append({
            "unit_id": unit_id, "run": unit["run"], "pair": unit["pair"], "arm": unit["arm"],
            "record_aliases": {
                f"{a}-REC-{n:02d}": {
                    "record_id": e["id"],
                    "band": _band(unit["pair"], e["id"], reportable),
                }
                for n, e in enumerate(unit["entries"], 1)
            },
            "issue_count": len(unit["issues"]),
        })
    return sample, key


def verify(path: pathlib.Path) -> list[str]:
    text = path.read_text()
    problems = [f"残留 pair 指纹：{m!r}" for m in set(_LEAK.findall(text)) if m != "NNNN"]
    problems += [f"残留带名称：{w!r}" for w in _BAND_WORDS if w in text]
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation", required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)

    if args.verify:
        path = OUT / "sample.json"
        if not path.is_file():
            print(f"no {path}", file=sys.stderr)
            return 2
        problems = verify(path)
        if problems:
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print(f"ok: {path} 无 pair 指纹、无带名称残留")
        return 0

    sample, key = build(args.generation)
    OUT.mkdir(exist_ok=True)
    existing = OUT / "key.json"
    if existing.is_file():
        old = json.loads(existing.read_text()).get("sample_id")
        if old and old != key["sample_id"]:
            archive = OUT / f"key.{old}.json"
            if not archive.is_file():
                archive.write_text(existing.read_text())
                print(f"  已归档上一份 key（sample_id={old}）→ {archive.name}")
    (OUT / "sample.json").write_text(json.dumps(sample, ensure_ascii=False, indent=1))
    existing.write_text(json.dumps(key, ensure_ascii=False, indent=1))

    issues = sum(len(i["published_issues"]) for i in sample["items"])
    records = sum(len(i["expected_defects"]) for i in sample["items"])
    bands = collections.Counter(
        v["band"] for i in key["items"] for v in i["record_aliases"].values()
    )
    print(f"(格, 轮) 单元 {sample['unit_count']} 个，sample_id={sample['sample_id']}")
    print(f"  待标注 issue {issues} 条；台账条目位 {records} 个")
    print(f"  按带（仅在 key 里）：{dict(bands)}")
    problems = verify(OUT / "sample.json")
    print("  盲化自检：" + ("✅ 干净" if not problems else f"❌ {len(problems)} 处残留"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
