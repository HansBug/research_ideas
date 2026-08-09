"""判定层的横向一致性检查：同一形态不得有两套标准。

## 为什么这个脚本必须存在

v41 的逐位判定里有 6 位判错，全部是「命中被判成未命中」：

- `EIS-0040-01` 五格发布了「Autonomous 中 Power_Off 不终止运行」，判成未命中；而**同一句话**
  在 v40 的 `EIS-0030-02` 上判的是命中——两条台账的措辞几乎逐字相同。
- `EIS-0040-03` 的 `run3/0040-gpt` 发布了「front_distance_10 未在运行时使系统进入 Autonomous」，
  判成未命中；同代 `run1`/`run2` 的**同一句话**判的是命中。

误差方向是单向的，原因可推测：逐格判定时容易顺着 primary 谓词的**字面**去找对应 issue，
而 issue 的措辞是从**结果面**写的（「不终止运行」），不是从**谓词面**写的（「事件未被消费」）。
谓词名对不上，就误判成没报。

修正前 ⑤ 判定层占未命中的 12/89，其中 6 位是判定错误而非产出缺陷——**判定层误差一度占到该段
的一半**。判定层是一个独立的、量级不小的误差源，必须有工具压制。

## 这个脚本做什么，不做什么

**做**：把「同一形态判出两种结果」的位挑出来，交给人读原文。
**不做**：不改判、不给结论、不算命中率。

这条边界是硬的。本仓库已有教训：机械代理只能定位，不能裁定。两个 issue 标题字面接近，
不等于陈述的是同一个缺陷；判定必须人读台账原文与 issue 原文。这个脚本只负责把**值得人再读一遍
的那几十位**从几百位里捞出来，把人的注意力放到最可能出错的地方。

用法::

    python adjudication_recheck.py --generation matrix-v41 --audit /tmp/v41_audit.json
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import verdict_tiers as V  # noqa: E402

RUNS = HERE.parents[2] / "runs" / "paper1"

#: 台账 primary 里的路径前缀，比对时要剥掉——它在每个标识符上都出现，留着会让所有位都「高度重合」。
_CORPUS_PREFIX = re.compile(r"llms_emp_feedback_final_\d+\.")

#: 单独出现无区分力的路径片段。
_WEAK = frozenset({"any", "state", "event", "kind", "true", "false"})

#: 低于这个覆盖率的不进工作清单——否则人要读的量和不用工具一样多。
DEFAULT_THRESHOLD = 0.6


def primary_elements(expression: str) -> frozenset[str]:
    """台账 primary 绑定的元素标识符，切成可在 issue 文本里找到的片段。

    **为什么比对的是 primary 而不是 statement**：第一版拿台账散文和 issue 标题做词元重合，
    在 v41 那两处真实判错上得分接近 0 —— 台账写「自动驾驶激活期间无法断电」，issue 写
    「Power_Off 在 Autonomous 中未使系统终止」。两句讲的是同一件事，共同的汉字却几乎没有：
    断电↔Power_Off、自动驾驶↔Autonomous 是**语义**对应，不是字面对应。

    primary 表达式里绑的恰恰是那组标识符本身（`Power_Off`、`Autonomous.AutoInitial`），
    而 issue 为了指认具体元素必然把它们写出来。**同一个缺陷，散文可以换着说，元素名不能。**
    """

    return frozenset(element_forms(expression))


def element_forms(expression: str) -> dict[str, frozenset[str]]:
    """元素名 → 它在 issue 文本里可能的写法。

    目前只认**全名**。试过放宽到 CamelCase 段（让 `AutonomousActive` 被「Autonomous」命中，
    因为 issue 常用父状态名指代子状态），实测是在两类假阳性之间换手而不是消除：
    严格版把「Autonomous 下缺 Power_Off 出边」与「HumanDriving 中 Power_Off 未终止」
    看成同一形态（v37 上 8 对）；放宽版让 `AutonomousFinal` 被任何提到「Autonomous」的
    父状态级 issue 命中（v37 上 13 对）。

    这类作用域歧义没有词法解法。既然本工具只定位不裁定，就取更简单、失败模式更好解释的
    严格版，并把「作用域级假阳性属预期，必须人读原文分辨」写在这里。
    """

    stripped = _CORPUS_PREFIX.sub("", expression or "")
    forms: dict[str, set[str]] = {}
    for value in re.findall(r"[\"']([^\"']+)[\"']", stripped):
        for chunk in re.split(r"[.\s]+", value):
            for name in [chunk, *chunk.split("_")]:
                key = name.lower()
                if not key or key in _WEAK or len(key) < 2:
                    continue
                forms.setdefault(key, {key})
    return {key: frozenset(value) for key, value in forms.items()}


def predicate_of(expression: str) -> str:
    match = re.search(r"([a-z_][a-z0-9_]*)\s*\(", expression or "")
    return match.group(1) if match else ""


def coverage(
    elements: dict[str, frozenset[str]] | frozenset[str], title: str
) -> tuple[float, frozenset[str]]:
    """issue 标题覆盖了 primary 的几成绑定元素，以及具体覆盖了哪些。

    返回覆盖集合而不只是比值，是因为「同一形态」要用**覆盖了哪些元素**来判定：两位覆盖的
    元素集合相同，才说明两处 issue 指认的是同一组对象。
    """

    if not isinstance(elements, dict):
        elements = {name: frozenset({name}) for name in elements}
    if not elements:
        return 0.0, frozenset()
    lowered = (title or "").lower()
    found = frozenset(
        name for name, forms in elements.items() if any(form in lowered for form in forms)
    )
    return len(found) / len(elements), found


def published_titles(generation: str, cell: str) -> list[str]:
    run, name = cell.split("/")
    path = RUNS / generation / run / name / "discover-completed.json"
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return []
    return [str(issue.get("title") or "") for issue in payload.get("issues") or ()]


def best_match(
    expression: str, titles: list[str]
) -> tuple[str, float, frozenset[str]]:
    """覆盖 primary 绑定元素最多的那条已发布 issue。"""

    elements = element_forms(expression)
    if not titles or not elements:
        return "", 0.0, frozenset()
    scored = [(title,) + coverage(elements, title) for title in titles]
    return max(scored, key=lambda item: item[1])


def _describe(
    generation: str, entry: dict, ledger: dict, threshold: float
) -> dict | None:
    record = ledger.get(entry["record_id"]) or {}
    expression = str(record.get("primary_expression") or "")
    title, score, found = best_match(
        expression, published_titles(generation, entry["cell"])
    )
    if score < threshold:
        return None
    return {
        "record_id": entry["record_id"],
        "cell": entry["cell"],
        "hit": bool(entry["hit"]),
        "predicate": predicate_of(expression),
        "statement": str(record.get("statement") or "")[:180],
        "matched_issue": title,
        "score": round(score, 3),
        "_covered": found,
    }


def inconsistencies(
    generation: str,
    audit: list[dict],
    ledger: dict,
    threshold: float = DEFAULT_THRESHOLD,
    also: tuple[tuple[str, list[dict]], ...] = (),
) -> list[dict]:
    """同一形态（同谓词 × issue 指认同一组元素）却判出两种结果的位。

    形态由两侧共同决定：只看台账相同不行——不同格的制品不同，一格报了另一格没报，命中不同是
    正常的；只看 issue 相同也不行——同一句 issue 可能对应不同台账条目。**同一个谓词、issue
    指认的元素集合又完全相同**，两位却判出不同结果，才是判定标准不一致。

    注意这里跨的是 record：`EIS-0030-02` 与 `EIS-0040-01` 是两条台账，绑的元素不同
    （`Autonomous.Navigating` vs `Autonomous.AutoInitial`），但两处 issue 都只指认了
    `Autonomous` + `Power_Off`——**在已发布文本这一层它们是同一句话**，理应同判。
    """

    enriched = []
    for gen, entries in ((generation, audit), *also):
        for entry in entries:
            if entry.get("decided_by") == "tier_a":
                continue  # A 层确定性判据，无人的口径漂移
            described = _describe(gen, entry, ledger, threshold)
            if described is None:
                continue
            described["generation"] = gen
            if also:  # 只在跨代比时给 cell 加代次前缀，单代输出保持原样
                described["cell"] = f"{gen}:{described['cell']}"
            enriched.append(described)
    flagged: list[dict] = []
    for index, left in enumerate(enriched):
        for right in enriched[index + 1 :]:
            if left["hit"] == right["hit"]:
                continue
            if left["predicate"] != right["predicate"]:
                continue
            if left["_covered"] != right["_covered"]:
                continue
            hit_side, miss_side = (left, right) if left["hit"] else (right, left)
            flagged.append(
                {
                    "hit_side": {k: v for k, v in hit_side.items() if k != "_covered"},
                    "miss_side": {k: v for k, v in miss_side.items() if k != "_covered"},
                }
            )
    return flagged


def worklist(
    generation: str, audit: list[dict], ledger: dict, threshold: float
) -> list[dict]:
    """判未命中、但该格发布过一条指认了同一组元素的 issue —— 值得人再读一遍。"""

    out = [
        {k: v for k, v in described.items() if k not in {"_covered", "hit"}}
        for entry in audit
        if not entry["hit"]
        and entry.get("decided_by") != "tier_a"
        and (described := _describe(generation, entry, ledger, threshold)) is not None
    ]
    return sorted(out, key=lambda item: -item["score"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generation", required=True)
    parser.add_argument("--audit", required=True, type=pathlib.Path)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument(
        "--also",
        nargs=2,
        action="append",
        metavar=("GENERATION", "AUDIT"),
        default=[],
        help="再纳入一代一起比。跨代次的口径漂移单代扫不出来——同一形态在 v37 判未命中、"
        "在 v41 判命中，两次单代扫描各自都是自洽的。",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    audit = json.loads(args.audit.read_text())["audit"]
    ledger = V.ledger_claims()
    also = tuple(
        (gen, json.loads(pathlib.Path(path).read_text())["audit"]) for gen, path in args.also
    )
    pairs = inconsistencies(args.generation, audit, ledger, args.threshold, also)
    items = worklist(args.generation, audit, ledger, args.threshold)

    if args.json:
        print(json.dumps({"inconsistencies": pairs, "worklist": items},
                         ensure_ascii=False, indent=1))
        return 0

    print(f"# {args.generation} 判定层横向一致性\n")
    print("⚠️ 本工具只定位，不裁定。下列每一位都必须人读台账原文与 issue 原文后再决定。\n")
    print(f"## 同形态判出两种结果：{len(pairs)} 对\n")
    for pair in pairs:
        hit, miss = pair["hit_side"], pair["miss_side"]
        print(f"- 命中 `{hit['record_id']}` @ {hit['cell']} ← 「{hit['matched_issue']}」")
        print(f"  未命中 `{miss['record_id']}` @ {miss['cell']} ← 「{miss['matched_issue']}」\n")
    print(f"## 判未命中但该格有高重合 issue（阈值 {args.threshold}）：{len(items)} 位\n")
    counts: collections.Counter = collections.Counter(item["record_id"] for item in items)
    for item in items:
        print(f"- {item['score']:.2f} `{item['record_id']}` @ {item['cell']}")
        print(f"      台账: {item['statement'][:110]}")
        print(f"      issue: {item['matched_issue'][:110]}")
    if counts:
        print("\n集中在: " + " ｜ ".join(f"{k} {v}" for k, v in counts.most_common(6)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
