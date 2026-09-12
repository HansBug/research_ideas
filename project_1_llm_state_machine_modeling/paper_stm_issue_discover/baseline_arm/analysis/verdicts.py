"""判定表：骨架生成 · C 层闸校验 · 格式 A → 格式 B 转换。

## 两种判定表格式，⛔ 不可混

* **格式 A（逐位人工判定）**：键 `"<record_id>|run<N>/<pair>-<arm>"`，值
  `{hit, equivalence_form, argument}`。⭐ 这是判定者实际填的东西，与主臂 `v46_human.json` 逐字同构。
* **格式 B（度量输入）**：`{"verdicts": {"<record_id>": {"<arm>": [r1, r2, r3], "direction": {...}}}}`。
  ⭐ 这是 `discover_matrix/metrics_at_k.py` 吃的东西。

⚠️ 两套 `equivalence_form` 字面量不同：格式 A 用**中文**四形态，格式 B 的 `direction` 用**英文**
枚举。⛔ 主臂的转换链根本不产出 `direction`（v46 复算因此带 `--no-direction-check`）。⭐ 本模块做
显式映射，⛔ 不靠跳过校验。

## ⛔ 为什么不 import `metrics_at_k`

隔离测试（`tests/test_isolation.py`）把 X1 的依赖面钉死在 `utils` / `pydantic` / `langchain_core`。
⭐ 于是算指标一律**用 subprocess 调 `metrics_at_k.py`**——这不是绕路，⭐ 而是更强的保证：
**两臂的指标由同一份代码算出**，同口径由机械而非记忆保证。

⚠️ 代价是本模块自己实现了一份「98 条 REPORTABLE」的筛选（与 `present.load_reportable()` 同源）。
⛔ 那是第二真源风险，由 `tests/test_denominator_matches_authority.py` 断言它与
`metrics_at_k.REPORTABLE` **逐条相等**来兜住——⭐ 漂移会在测试里炸，⛔ 不会在论文数字里静默发生。

## A 层在 X1 上不存在

主臂 588 位中有 20 位靠 A 层（断言候选自动确认）确认、无逐格 `argument`。⛔ X1 无断言、A 层结构上
无法运行，⭐ **所以 588 位必须 100% 逐位人工填满，一位都不能兜底**。⚠️ 这反而使 X1 的判定覆盖比
主臂**更完整**（588/588 有 argument vs 574/588），但两臂判定机制因此不同质——已登记为不对称。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from present import BOUNDARY_RULED, LEDGER, OUT_OF_SCOPE_PAIRS  # noqa: E402

#: 格式 A 的 `equivalence_form` 闭集，逐字取自 `docs/protocol/hit_criterion.md` §3。
#: ⭐ 「一个不属于任何形态的『等价性论证』就是没有论证」——闭集是这道闸的全部力量所在。
EQUIVALENCE_FORMS: tuple[str, ...] = (
    "直接对应",
    "合取项之一",
    "负向命题的正向对偶",
    "蕴含更根本的原因",
)

#: 中文形态 → `metrics_at_k` 的英文 `direction` 枚举。
FORM_TO_DIRECTION: dict[str, str] = {
    "直接对应": "direct",
    "合取项之一": "conjunct",
    "负向命题的正向对偶": "dual",
    "蕴含更根本的原因": "implies",
}

#: ⭐ `hit=true` 时 `argument` 的最小长度。与主臂 C 层闸同值：书面交代是这道闸的存在理由。
MIN_ARGUMENT_CHARS = 20

ARMS = ("claude", "gpt")
ROUNDS = (1, 2, 3)

_KEY = re.compile(r"^(?P<record>EIS-\d{4}-\d{2})\|run(?P<round>[123])/(?P<pair>\d{4})-(?P<arm>gpt|claude)$")


def reportable_records() -> list[dict[str, Any]]:
    """98 条：台账 126 − `00x8` 27 − 逐条边界裁定 1。

    ⛔ 不用台账的 `in_scope` 字段——它对 126 条全为 True，记的不是这件事。
    """

    payload = json.loads(LEDGER.read_text(encoding="utf-8"))
    kept = [
        r
        for r in payload["records"]
        if str(r["pair"])[-4:] not in OUT_OF_SCOPE_PAIRS and r["id"] not in BOUNDARY_RULED
    ]
    if len(kept) != 98:
        raise SystemExit(f"REPORTABLE should be 98, got {len(kept)}")
    return kept


def expected_keys() -> list[str]:
    """588 个位键，顺序固定（便于 diff）。"""

    keys: list[str] = []
    for record in sorted(reportable_records(), key=lambda r: r["id"]):
        pair = str(record["pair"])[-4:]
        for round_index in ROUNDS:
            for arm in ARMS:
                keys.append(f"{record['id']}|run{round_index}/{pair}-{arm}")
    return keys


def skeleton() -> dict[str, Any]:
    """空判定表骨架。⛔ 刻意不预填 `hit`——预填 false 与「判过是 false」不可区分。"""

    return {
        "_schema": "x1-baseline-arm-verdicts-A/1",
        "_note": (
            "逐位人工判定。hit 必填；hit=true 时 equivalence_form 必填（四形态之一）"
            f"且 argument ≥ {MIN_ARGUMENT_CHARS} 字。未判 = 键的值为 null，⛔ 不是 hit:false。"
            "格失败/未落盘的位填 {\"hit\": null}。"
        ),
        "_equivalence_forms": list(EQUIVALENCE_FORMS),
        "verdicts": {key: None for key in expected_keys()},
    }


def validate(table: dict[str, Any]) -> list[str]:
    """C 层闸。返回问题清单；空 = 通过。

    ⚠️ 未判位必须报错而不是默认为 0——**一个只判了一半的审计文件与判完的在形状上无从区分**。
    """

    problems: list[str] = []
    entries = table.get("verdicts", table)
    if not isinstance(entries, dict) or not entries:
        return ["判定表为空——零输出与「全部未命中」不可区分，拒绝校验"]

    wanted = set(expected_keys())
    seen = set(entries)
    for key in sorted(wanted - seen):
        problems.append(f"{key}: 该位缺失（未判就是键不存在，这是硬错误）")
    for key in sorted(seen - wanted):
        problems.append(f"{key}: 不在 588 位之内——网格或分母被改错了")

    for key in sorted(seen & wanted):
        entry = entries[key]
        if entry is None:
            problems.append(f"{key}: 该位未判（值为 null 而非判定对象）")
            continue
        if not isinstance(entry, dict):
            problems.append(f"{key}: 值不是对象")
            continue
        hit = entry.get("hit")
        if hit is None:
            # ⭐ 合法：格失败 / 未落盘。⚠️ 但必须写明理由，否则与漏判不可区分。
            if not str(entry.get("argument") or "").strip():
                problems.append(f"{key}: hit=null 但没写理由（格失败？未落盘？）")
            continue
        if not isinstance(hit, bool):
            problems.append(f"{key}: hit 必须是 true/false/null，得到 {hit!r}")
            continue
        if not hit:
            continue
        form = entry.get("equivalence_form")
        if form not in EQUIVALENCE_FORMS:
            problems.append(
                f"{key}: 判命中但 equivalence_form={form!r} 不在闭集内 {EQUIVALENCE_FORMS}"
            )
        argument = str(entry.get("argument") or "").strip()
        if len(argument) < MIN_ARGUMENT_CHARS:
            problems.append(
                f"{key}: 判命中但等价性论证过短（{len(argument)} 字）—— C 层要求书面交代"
            )
    return problems


def to_format_b(table: dict[str, Any], *, generation: str) -> dict[str, Any]:
    """格式 A → 格式 B，供 `metrics_at_k.py` 消费。

    ⚠️ `null` 与 `0` 的区别是硬的：`1` 命中、`0` 未命中、`null` **无判定**。
    ⛔ 把 null 读成 0 会让分母虚高而分子不变，即无声压低命中率。
    """

    entries = table.get("verdicts", table)
    series: dict[str, dict[str, list[Any]]] = defaultdict(
        lambda: {arm: [None] * len(ROUNDS) for arm in ARMS}
    )
    directions: dict[str, dict[str, str | None]] = defaultdict(
        lambda: {arm: None for arm in ARMS}
    )
    for key, entry in entries.items():
        match = _KEY.match(key)
        if match is None:
            raise SystemExit(f"unparseable verdict key: {key!r}")
        record = match.group("record")
        index = int(match.group("round")) - 1
        arm = match.group("arm")
        if entry is None:
            continue
        hit = entry.get("hit")
        series[record][arm][index] = None if hit is None else (1 if hit else 0)
        form = entry.get("equivalence_form")
        if hit and form in FORM_TO_DIRECTION:
            # 同一 (record, arm) 的多轮若形态不同，取第一个非空；形态差异不影响度量。
            directions[record][arm] = directions[record][arm] or FORM_TO_DIRECTION[form]

    out: dict[str, Any] = {"generation": generation, "rounds": len(ROUNDS), "verdicts": {}}
    for record in sorted(series):
        value: dict[str, Any] = dict(series[record])
        dirs = {arm: d for arm, d in directions[record].items() if d}
        if dirs:
            value["direction"] = dirs
        out["verdicts"][record] = value
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Skeleton / validate / convert X1 verdicts.")
    sub = parser.add_subparsers(dest="command", required=True)

    sk = sub.add_parser("skeleton", help="print an empty 588-position table")
    sk.add_argument("--out", default=None)

    va = sub.add_parser("validate", help="run the C-layer gate")
    va.add_argument("table", type=Path)

    cv = sub.add_parser("convert", help="format A -> format B for metrics_at_k.py")
    cv.add_argument("table", type=Path)
    cv.add_argument("--out", required=True)
    cv.add_argument("--generation", default="x1-baseline-v1")

    args = parser.parse_args(argv)

    if args.command == "skeleton":
        text = json.dumps(skeleton(), ensure_ascii=False, indent=2) + "\n"
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"wrote skeleton with {len(expected_keys())} positions to {args.out}")
        else:
            print(text)
        return 0

    table = json.loads(Path(args.table).read_text(encoding="utf-8"))

    if args.command == "validate":
        problems = validate(table)
        if problems:
            print(f"⛔ {len(problems)} 个问题：")
            for problem in problems[:80]:
                print(f"  - {problem}")
            if len(problems) > 80:
                print(f"  ... 另有 {len(problems) - 80} 条")
            return 1
        print(f"✅ C 层闸通过：{len(expected_keys())} 位全部有判定且论证合规")
        return 0

    converted = to_format_b(table, generation=args.generation)
    Path(args.out).write_text(
        json.dumps(converted, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(converted['verdicts'])} records to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
