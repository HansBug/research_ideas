"""
## ⛔ 本文件的**按带报告**部分已作废（band 划分已废止）

用户裁定废止 hold-out 带划分（理由：它服务泛化性声明，而本研究的贡献是从真实模型归纳问题类型与判定
能力，语料即研究对象；且它把分母掐死到 2 条）。

| 本文件的部分 | 状态 |
| :-- | :-- |
| `ratio_gate()` | **仍是唯一归属地** —— `full_tables.py` 调它，不重实现 |
| `MEASURED_CHURN` / `MIN_POSITIONS` / `MIN_CLUSTERS` | 仍有效（已改为全分母口径） |
| 分带 | **已移除** —— hold-out 与分带机制已于 2026-08-09 永久废止；只剩 `REPORTABLE` 一个分母 |
| `main()` 的按带输出 | **作废**，改用 `full_tables.py` |

⚠️ **不要用本文件的 `main()` 报覆盖率。** 用：

    python3 full_tables.py --generation <gen> --verdicts <verdicts.json>

保留作废代码而不删，是因为历史 comment 引用过它的输出，删掉会使那些数字无法复算。但**当前正文一律以
`full_tables.py` 为准**。
从人工判定表算 metric@k。**脚本不做匹配、不读模型输出——只做算术。**

分工是刻意的：判定由人工做（见 present_for_judgment.py 的理由），算术由脚本做。脚本读不到
模型输出，所以它不可能"顺手"把判定也做了。

⚠️ 但「只做算术」不等于「不做校验」。上一版对输入零校验，于是手写判定表时漏掉一条不利记录
就能静默拿到 100%：

    {"verdicts": {"EIS-0035-01": [1,1,1], "EIS-0035-02": [1,1,1], "EIS-0047-03": [1,1,1]}}
    → 全部 条目=3  hit@1 = 9/9 = 100.0%

而可报记录当时是四条，`EIS-0032-02` 被整条省掉、分母从 4 变 3、无一句告警。这正是
`CLAUDE.md` §3.5 条款 4 的「更改分母 / 剔除不利样本」，且**不需要任何恶意** —— 手写三十几条
三元组漏一条即可。同一版还接受台账外的 id、长度不是 3 的数组、`2` 之类的值，并照常打印
`hit@1 = 8/7 = 114.3%`。

所以本版启动即对账，任一条不满足就**拒跑**：

  1. `reportable_records` 必须全部出现 —— 少一条即拒，因为那正是分母
  2. 台账外的 id 一律拒 —— 它会被按 id 前缀错分到某个带里并污染统计
  3. 值只能是 `0` / `1` / `null`，轮次数必须等于 `--rounds`（默认 3）
  4. `verdicts` 为空即非零退出 —— 零输出与「全部未命中」不可区分

用 `--template` 生成预填骨架（全部 id、值为 null），人工只需填值，漏填会被上面第 1 条抓住。

## 输入格式

    {
      "verdicts": {
        "EIS-0007-01": {"claude": [1, 0, 1], "gpt": [0, 0, 1]},
        "EIS-0007-02": [1, 1, 1]
      },
      "over": {"0007-claude": [2, 1, 0], "0007-gpt": [3, 3, 3]}
    }

三元组是 run1/run2/run3 的人工判定：`1`=命中，`0`=未命中，`null`=该轮该格失败（不计入分母）。
裸数组视为单臂，保留历史格式。`over` 是每轮的多报条数（人工认定为「不在台账内且确为误报」）。

**模型维度必须显式。** 上一版无处安放它，于是 `EIS-0035-01@claude` / `@gpt` 这种写法会把一条
台账记录算成两条、分母翻倍；而 `over` 的 `0035-claude` 因为不等于 `0035`，落进「历史格」兜底
带 —— hold-out pair 的多报被归入共演化观测，无告警。本版按 id 与 pair 前缀分带，臂只影响呈现
与分臂小计，不影响分带。

hit@1    = 命中数 / 有效(条目,轮次,臂)组数    —— 一次运行的期望产出
hit@3    = 至少一轮命中的(条目,臂)比例        —— 该缺陷是否在能力范围内
hit@all  = 全部有效轮次都命中的(条目,臂)比例  —— 稳定性
over@1   = 每轮平均多报数
over@any = 出现过多报的格子数
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`_PROVENANCE`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
# ⚠️ 2026-08-17 第二次搬迁：`manual_review/`（第一版台账 + 60 份复审 + relabel）已随台账证据链
# 搬到 `discover_matrix/ledger_v2/provenance/`，⛔ 不再是本归档的子目录。故单独锚一个常量，
# ⛔ 不许再写 `_PROVENANCE` —— 那会解析到不存在的目录并被读成空数据。
_PROVENANCE = (next(p for p in _F.parents if p.name == "paper_stm_issue_discover")
               / "discover_matrix" / "ledger_v2" / "provenance")
import nl_scope_filter  # noqa: E402

LEDGER = _PROVENANCE / "expected_issue_set.json"

# ⚠️ 这里有**两条互不相干**的策略，历史上被混为一谈过一次，代价是一次 360 格的误启动。
# 分清楚它们是本段注释存在的唯一理由。
#
# ── 策略一：不设 hold-out（已永久废止分带）────────────────────────────────────
# `holdout.json` 与「可报 / 已烧毁 / 历史」三带机制已于 2026-08-09 永久移除。方法就是在这批
# pair 上迭代出来的，评测口径据此统一：**没有哪一条记录因为参与过规则编写而被单独成带、降级或
# 剔出分母**。论文侧的表述见 docs/protocol/method_provenance_policy.md —— 谓词与 prompt 的由来一律陈述为
# 从真实设计与系统规约归纳，不以 pair 为依据，所以根本不需要 hold-out 来支撑什么。
#
# ── 策略二：`00x8` 不在 paper 的建模对象范畴内（先验排除）──────────────────────
# CLAUDE.md 把 project_1 的建模对象写死为 M = (S, E, V, Tr, A)，时钟、不变式、正交区并发**不在其中**。
# 60 个 pair 由 10 份 NL 各生成 6 个，其中 NL `6af3966c`（并发提及 11、计时提及 17）要求
# fork/join 与秒级约束，**其忠实模型在 M 中无法表示**。它对应的 6 个 pair 恰好末位为 8，
# 故简称「排除 `00x8`」。判据只读 nl.txt、先验、与任何运行结果无关，详见 docs/protocol/nl_scope_rule.md。
#
# 两者的区别是硬的：策略一说「不许因为样本表现或参与度而改分母」，策略二说「有些规约本来就
# 不是本方法要建模的东西」。**把策略一套到策略二上，就会得出「00x8 被排除 = 剔除不利样本」
# 这个错误结论** —— 事实相反，被排除集里 `0018` 的 hit@1 = 66.7%，高于全量均值。
#
# 所以分母 = 台账全部记录 − NL 越界记录。缺的若是越界记录，不是分母被篡改；缺的若是范围内
# 记录，那才是。下面的报错必须把这两种情况分开说，否则读者（和我）会再错一次。
def _all_record_ids() -> tuple[str, ...]:
    payload = json.loads(LEDGER.read_text())
    records = payload.get("records") or ()
    return tuple(str(record["id"]) for record in records)


def _out_of_scope_record_ids() -> tuple[str, ...]:
    """不进分母的记录：NL 越界（`00x8`）+ 台账已裁定 `boundary_ruling: out_of_scope` 的。

    两个来源，都必须扣，且都不算「缺失」：

    1. **NL 越界**：`00x8` 六个 pair 的规约要求 fork/join 与秒级时间约束，忠实模型在
       $M$ 中无法表示（docs/protocol/nl_scope_rule.md）。
    2. **逐条边界裁定**：台账记录自带 `boundary_ruling`，`out_of_scope` 者由独立裁定
       判为「表示层产物而非作者缺陷」，其 `boundary_effect` 明写「从能力分母剔除」。

    ⚠️ 第 2 条一度**没有被执行**：本模块原先只看 `pair`，而台账的 `in_scope` 字段对
    126 条全为 `True`（它记的不是这件事），于是 `EIS-0043-02` 虽被裁定剔除却仍进了分母，
    v46 首份报告的 `hit@1` 因此偏高 0.4pp。裁定写在数据里而工具不读，等于没裁定 ——
    所以这里直接读 `boundary_ruling`，而不是依赖任何人记得手工扣。
    """

    return _nl_out_of_scope_ids() + _boundary_ruled_ids()


def _nl_out_of_scope_ids() -> tuple[str, ...]:
    """`00x8` 家族：先验越界，从未进过网格。"""

    excluded_pairs = set(nl_scope_filter.excluded_pairs())
    payload = json.loads(LEDGER.read_text())
    return tuple(str(r["id"]) for r in payload.get("records") or ()
                 if str(r.get("pair", "")) in excluded_pairs)


def _boundary_ruled_ids() -> tuple[str, ...]:
    """逐条边界裁定剔除：跑过、判过，事后才被裁定为表示层产物。"""

    excluded_pairs = set(nl_scope_filter.excluded_pairs())
    payload = json.loads(LEDGER.read_text())
    return tuple(str(r["id"]) for r in payload.get("records") or ()
                 if str(r.get("pair", "")) not in excluded_pairs
                 and r.get("boundary_ruling") == "out_of_scope")


OUT_OF_SCOPE = _out_of_scope_record_ids()
REPORTABLE = tuple(r for r in _all_record_ids() if r not in set(OUT_OF_SCOPE))
# 干净但结构性不可达的记录。它若报未命中不是能力缺口，所以必须在输出里说出来，否则读者会把
# 门的抑制读成方法的失败。
BLOCKED: dict[str, str] = {
    # 空的，而空是判定的结果，不是遗漏。
    #
    # 预注册 §9.1 曾断言 `EIS-0047-03` 被 `initialization_anchored` 门**结构性封死**，理由是台账
    # 那两种编码（都绑 `source="[*]"` + trigger `Collision_Detected`）在八种 phase 组合下全被拒。
    # 机制论证没错，但从「这种写法被拒」推出「这个缺陷测不到」是错的：v22 实测 0047 六格
    # `UnsupportedEvidence` 拒答 0 条，门是以**修订反馈**形式起作用的，生产者据此改用
    # `event_consumed(source=<根复合态>, ...)` 并在 run1/claude 上命中（形态 `implies`）。
    #
    # 所以这里不能再标它「被封死」—— 那会把一条真命中的记录在报告里写成受抑制。§9.1 已就地更正，
    # 这张表随之清空。若将来发现新的结构性封死项，在此登记并同时更新预注册。
}


def _ledger_ids() -> set[str]:
    """台账里全部记录的 id。台账外的 id 一律拒收，它会污染分带。"""

    payload = json.loads((_PROVENANCE / "expected_issue_set.json").read_text())
    records = payload.get("records")
    if not records:
        records = next(
            value
            for value in payload.values()
            if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0]
        )
    return {str(record["id"]) for record in records}


def _arms(value) -> dict[str, list]:
    """判定值归一成 臂 -> 三元组。裸数组视为单臂，保留历史格式。"""

    if isinstance(value, dict):
        return {
            str(arm): list(rounds)
            for arm, rounds in value.items()
            if arm != "direction" and isinstance(rounds, list)
        }
    return {"-": list(value)}


#: `docs/protocol/hit_criterion.md` §3 的四种成立形态。命中必须落在其中之一。
DIRECTIONS = {
    "direct": "直接对应——两个命题说同一件事，只是谓词不同",
    "conjunct": "合取项之一——台账命题是 all(...)，我们证明其中一个合取项为假",
    "dual": "负向命题的正向对偶——台账说「不应存在错的边」，我们说「应存在对的边」",
    "implies": "蕴含更根本的原因——我们的命题为假蕴含台账命题为假，且定位更上游",
}


def _hit_directions(value) -> dict:
    """判定值里的方向标注。裸数组没有标注位，返回空。"""

    if isinstance(value, dict) and isinstance(value.get("direction"), dict):
        return value["direction"]
    return {}


def _has_any_hit(value) -> bool:
    return any(1 in series for series in _arms(value).values())


def validate(verdicts: dict, over: dict, rounds: int, require_direction: bool = True) -> list[str]:
    """输入是否能支撑一个可被引用的比率。返回全部问题，不是第一个。"""

    if not verdicts:
        return ["verdicts 为空。零输出与「全部未命中」不可区分，所以这是错误而不是 0%"]
    problems = []
    known = _ledger_ids()
    for record_id, value in sorted(verdicts.items()):
        if record_id not in known:
            problems.append(f"{record_id} 不在台账里。它会被按 id 前缀错分到某个带并污染统计")
        for arm, series in _arms(value).items():
            label = record_id if arm == "-" else f"{record_id}[{arm}]"
            if len(series) != rounds:
                problems.append(f"{label} 有 {len(series)} 轮，应为 {rounds}")
            for index, entry in enumerate(series, 1):
                if entry not in (0, 1, None):
                    problems.append(f"{label} 第 {index} 轮是 {entry!r}，只能是 0 / 1 / null")
    missing = [record for record in REPORTABLE if record not in verdicts]
    if missing:
        problems.append(
            f"范围内记录缺 {len(missing)} 条：{missing}。它们就是能力主张的分母，少一条就是"
            "「更改分母 / 剔除不利样本」（CLAUDE.md §3.5 条款 4），即便只是手写时漏填。"
            "⚠️ 这里说的**不是** `00x8`：那 27 条是 NL 越界记录，先验不在分母内，"
            "本检查已把它们扣除（见 docs/protocol/nl_scope_rule.md）"
        )
    # 两条排除来源在这里必须分开，因为它们的**合法性相反**。
    #
    # `00x8` 是先验越界：它们不该被跑、更不该被判，出现在判定表里就说明网格被改错了。
    # `boundary_ruling` 是事后裁定：那条记录**跑过也判过**，之后才被独立裁定判为表示层
    # 产物并剔出分母 —— 它留在判定表里是正常的，原始判定本就该保留。
    #
    # 合并成一句话报错的代价是实测过的：`EIS-0043-02` 触发了这条，报错却说「NL 越界 /
    # `00x8` / 网格被改错了」，与实际原因完全不符，且使真源工具对一份正确的判定表拒算，
    # 于是声称的数字只能靠别的脚本复现。
    nl_intruders = [r for r in _nl_out_of_scope_ids() if r in verdicts]
    if nl_intruders:
        problems.append(
            f"判定表里混入 {len(nl_intruders)} 条 NL 越界记录：{nl_intruders}。`00x8` 对应的 NL 要求 "
            "fork/join 与秒级时间约束，其忠实模型在 M = (S, E, V, Tr, A) 中无法表示，先验不进"
            "网格也不进分母（docs/protocol/nl_scope_rule.md）。它们出现在这里意味着网格被改错了"
        )
    ruled = sorted({r for r in OUT_OF_SCOPE if r in verdicts} - set(nl_intruders))
    if ruled:
        print(f"ℹ️ 判定表含 {len(ruled)} 条 boundary_ruling 剔除记录（{ruled}），"
              "其原始判定保留、不计入分母", file=sys.stderr)
    for cell, series in sorted(over.items()):
        if len(series) != rounds:
            problems.append(f"over[{cell}] 有 {len(series)} 轮，应为 {rounds}")
    if require_direction:
        problems.extend(_direction_problems(verdicts))
    return problems


def _direction_problems(verdicts: dict) -> list[str]:
    """命中必须写出它按哪一种形态成立。

    这是防「判反」的机械检查点，而判反是这条链上最容易犯、代价最大的错误：上一代次有两条模型
    产出触及了正确的元素、却得出与台账**相反**的结论，而唯一的防线（并列呈现）当时在真实路径
    上输出零行。

    要求填形态的作用不是记录，是**强制做一次方向比对**：填不出 `docs/protocol/hit_criterion.md` §3 四种形态
    里的哪一种，就说明没做过那次比对。空值即拒收。

    只对**能力主张带**强制。共演化带三十条逐条填形态的成本，换不来能被引用的结论。
    """

    problems = []
    for record_id in REPORTABLE:
        value = verdicts.get(record_id)
        if value is None or not _has_any_hit(value):
            continue
        directions = _hit_directions(value)
        for arm, series in _arms(value).items():
            if 1 not in series:
                continue
            label = record_id if arm == "-" else f"{record_id}[{arm}]"
            form = directions.get(arm) or directions.get("-") or directions.get("all")
            if not form:
                problems.append(
                    f"{label} 判为命中但没写方向形态。填 {sorted(DIRECTIONS)} 之一到 "
                    f'verdicts["{record_id}"]["direction"]["{arm}"] —— 填不出哪一种，'
                    "就说明没做过方向比对，而判反正是这条链上代价最大的错误"
                )
            elif form not in DIRECTIONS:
                problems.append(
                    f"{label} 的方向形态 {form!r} 不在 docs/protocol/hit_criterion.md §3 的四种里："
                    f"{sorted(DIRECTIONS)}"
                )
    return problems


#: 比率闸门（§3.5.2 补充条款）。覆盖率类指标**以比率形式**报出，须同时满足三条；任一不满足时该带
#: **只出逐条序列 + 全称/存在性陈述**，不出比率、不出 CI、不出代次间差值。
#:
#: 为什么需要它，而不是「小心解读」：
#:
#: 可报带的分母是 12 个判定位。实测（两代次逐位对齐、都用盲判 + 预注册判据 + 100% 覆盖）该带的
#: 代次间翻转率是 8.3%，全体 204 位是 **9.8%（20/204，方向对称 10:10）** —— 而 12 位上 `hit@1` 的
#: 粒度恰好也是 8.3%。**粒度与噪声同阶意味着任何「变化」只能是「翻了一位」。**
#:
#: 三条阈值的来源，逐条：
#:
#: (a) 独立簇数 ≥ 10 —— 簇 = **污染传播单元**，本语料是 NL 组（污染曾以 NL 组
#:     传播）。簇级 bootstrap 在簇数低于约 10 时无覆盖保证；实测可报带只有 2 个 NL 组，其「区间」
#:     支撑集只有 3 个点，那不是置信区间。
#: (b) 判定位 ≥ 100 —— 由 McNemar 反推：在实测 ψ = 9.8% 下，检出 8.3 pp 需 108 位。
#: (c) 粒度 ≤ 拟解读差异的 1/3 —— 当前 1/12 = 8.3% 而拟解读的差异恰是 8.3%。
#:
#: ## ⚠️ 首版把两种不同的主张混成了一条判据，已拆开
#:
#: 首版对**所有**比率施加同一条 `clusters >= 10`。后果是：本语料只有 **8 个 NL 组**（`group` 字段实测，
#: 34 条判定记录跨 NL03~NL10），这是**语料的固有属性、不是取样不足**，所以描述性比率**永远不可报**。
#: 那与刚废止的 hold-out 带划分是同型错误 —— 用一条纪律把可测量的东西变成不可测量。
#:
#: 正确的区分是主张类型，不是阈值高低：
#:
#: | 主张 | 例 | 需要什么 | 不需要什么 |
#: | :-- | :-- | :-- | :-- |
#: | **描述性比率** | 「本语料上 `hit@1` = 51.5%」 | 分母够大、粒度细于噪声 | **簇数** —— 没有向簇外推断 |
#: | **推断性主张** | 「v22→v23 的 +3.9pp 是真改进」 | **独立簇 ≥ 10** | —— |
#:
#: 污染在 NL 组内传播，组才是独立单元 —— 所以簇要求只对**推断**成立。描述研究对象本身时，样本就是
#: 总体，簇数不构成障碍。
#:
#: 实测本语料：**204 位 ✅ / 粒度 0.5% ✅ / 8 簇 ❌** → 描述性比率**可报**，跨代次差的显著性**不可断言**。
MIN_CLUSTERS = 10          # 仅用于推断性主张（跨代次差是否显著）
MIN_POSITIONS = 100        # 描述性比率的分母下限
#: 实测的代次间翻转率（全分母，v22↔v23）。粒度必须细于它的 1/3，否则比率的最小可分辨变化落在噪声里。
MEASURED_CHURN = {
    "all": "9.8%（20/204，10 升 10 降 —— 聚合值接近是抵消，不是稳定）",
}


def _clusters_of(ids: list[str]) -> int:
    """该带覆盖多少个 NL 组 —— 污染传播单元，也是推断的独立单元。"""

    payload = json.loads((_PROVENANCE / "expected_issue_set.json").read_text())
    records = payload.get("records") or next(
        v for v in payload.values()
        if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]
    )
    by_id = {str(r["id"]): r for r in records}
    return len({(by_id.get(i) or {}).get("group") for i in ids if by_id.get(i)} - {None})


def ratio_gate(ids: list[str], positions: int, band: str = "all",
               *, inferential: bool = False) -> list[str]:
    """返回不满足的闸门条件；空 = 允许报。

    `inferential=False`（默认）判**描述性比率**是否可报：只查分母与粒度。
    `inferential=True` 判**推断性主张**（跨代次差是否显著）是否可断言：额外要求独立簇 ≥ 10。

    两者分开是因为它们回答不同的问题 —— 描述研究对象时样本即总体，簇数不构成障碍；向簇外推断时，
    污染在 NL 组内传播，组才是独立单元。**首版对两者施加同一条簇要求，使描述性比率在本语料上永远
    不可报（只有 8 个 NL 组，是语料固有属性）。**
    """

    failed = []
    if positions < MIN_POSITIONS:
        failed.append(f"判定位 {positions} < {MIN_POSITIONS}")
    if positions:
        granularity = 100.0 / positions
        churn = MEASURED_CHURN.get(band) or MEASURED_CHURN.get("all")
        if churn:
            measured = float(churn.split("%")[0])
            if granularity > measured / 3:
                failed.append(
                    f"粒度 {granularity:.1f}% > 实测 churn {measured}% 的 1/3"
                )
    if inferential:
        clusters = _clusters_of(ids)
        if clusters < MIN_CLUSTERS:
            failed.append(
                f"独立簇（NL 组）{clusters} < {MIN_CLUSTERS} —— 描述性比率不受此限，"
                "但跨代次差的显著性不可断言"
            )
    return failed


def report_band(verdicts: dict, ids: list[str], name: str, rounds: int) -> None:
    """`rounds` 不是可选的 —— 见 `all_hit` 那行。

    `all(valid)` 在丢掉 `None` 之后回答的是「我观测到的那几轮都命中吗」，不是
    「三轮都命中吗」。一个只跑了两轮、两轮都中的单元会被计成三轮全中：缺测越多这个
    数字越好看，方向恰好是错的。下面 `len(valid) < 2` 那句只是把 n=1 标注出来，并
    没有把它挡在 `atall` 之外，所以 arity 必须在计数处约束。
    """

    if not ids:
        return
    triples = hits = items = at3 = atall = 0
    rows = []
    per_arm: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for record_id in sorted(ids):
        for arm, series in sorted(_arms(verdicts[record_id]).items()):
            label = record_id if arm == "-" else f"{record_id}[{arm}]"
            valid = [entry for entry in series if entry is not None]
            if not valid:
                rows.append((label, series, "全轮失败"))
                continue
            items += 1
            triples += len(valid)
            hits += sum(valid)
            any_hit = 1 if any(valid) else 0
            all_hit = 1 if len(valid) == rounds and all(valid) else 0
            at3 += any_hit
            atall += all_hit
            per_arm[arm][0] += sum(valid)
            per_arm[arm][1] += len(valid)
            if len(valid) < 2:
                # n=1 时 hit@all 与 hit@1 退化为同一个数，说「稳定」是从单点断言稳定性。
                kind = f"轮次不足({len(valid)}轮)，不得据此说稳定"
            else:
                kind = "稳定命中" if all_hit else ("hit@3 only" if any_hit else "全轮未命中")
            if record_id in BLOCKED:
                kind += f"  ⚠️ {BLOCKED[record_id]}"
            rows.append((label, series, kind))
    header = f"\n### {name}   条目={items}  有效(条目,轮次)={triples}"
    if not items:
        print(f"\n### {name}   条目=0（全部全轮失败）")
        for label, raw, kind in rows:
            print(f"   {label:24} {raw}  {kind}")
        return
    print(header)
    band_key = {"可报告记录": "reportable"}.get(name)
    if band_key is None:
        band_key = "hist" if "历史" in name else ("burned" if "烧毁" in name else "")
    failed = ratio_gate(sorted(ids), triples, band_key)
    if failed:
        # 闸门不通过：**只出逐条序列**。不出比率是为了让烧毁不再抬高任何东西 —— 见 `MIN_CLUSTERS`
        # 上方的说明。这里仍打印分子分母的原始计数，因为它们不是比率、也不会被当成比率引用。
        print(f"⛔ **比率闸门不通过，本带不出 hit@k 比率。** 未满足：{'；'.join(failed)}")
        print(f"   原始计数（**不得写成百分比**）：命中 {hits} / 位 {triples}；"
              f"至少一轮命中 {at3} / 条目 {items}；三轮全中 {atall} / 条目 {items}")
        churn = MEASURED_CHURN.get(band_key)
        if churn:
            print(f"   该带实测代次间翻转率：{churn}")
        print("   → 只以逐条序列与全称/存在性陈述报出（见下方逐条清单）")
    else:
        print(f"hit@1   = {hits}/{triples} = {hits / triples * 100:.1f}%")
        print(f"hit@3   = {at3}/{items} = {at3 / items * 100:.1f}%")
        print(f"hit@all = {atall}/{items} = {atall / items * 100:.1f}%")
    if len(per_arm) > 1:
        # 分臂小计。两条臂的数字必须能分开读，否则模型间比较消失。
        #
        # ⚠️ 但分臂的分母是全带的一半，所以**只要全带的闸门不通过，分臂必然更不通过** —— 首版把这
        # 两行漏在闸门外，于是在「本带不出比率」的正下方又打了两个百分比，而它们的分母只有 6 位、
        # 粒度 16.7%。闸门要拦的恰恰是这种东西。
        for arm, (arm_hits, arm_triples) in sorted(per_arm.items()):
            if failed:
                print(f"  按臂 {arm}: 命中 {arm_hits} / 位 {arm_triples}"
                      f"（**不得写成百分比**，分母仅 {arm_triples} 位）")
            else:
                print(f"  按臂 {arm}: hit@1 = {arm_hits}/{arm_triples} = "
                      f"{arm_hits / arm_triples * 100:.1f}%")
    thin = [
        label for label, series, _ in rows
        if 0 < len([x for x in series if x is not None]) < 3
    ]
    if thin:
        print(f"!! 轮次不足 3 的条目 {len(thin)} 个：{thin}。"
              "hit@all 在这些条目上不构成稳定性证据。")
    for label, raw, kind in rows:
        print(f"   {label:24} {raw}  {kind}")


def report_over(over: dict) -> None:
    if not over:
        return
    print("\n### 多报")
    grouped: dict[str, dict[str, list]] = collections.defaultdict(dict)
    for cell, series in over.items():
        # 不再分带：hold-out 机制已移除，全部格同等报出。
        grouped["全部"][cell] = series
    for band in ("全部",):
        cells = grouped.get(band) or {}
        values = [x for series in cells.values() for x in series if x is not None]
        if not values:
            continue
        any_n = sum(1 for series in cells.values() if any(x for x in series if x))
        print(f"  {band}: over@1 = {sum(values)}/{len(values)} = "
              f"{sum(values) / len(values):.2f} 条/轮   over@any = {any_n} 个格子")
        for cell, series in sorted(cells.items()):
            print(f"     {cell}: {series}")


def template(arms: list[str], rounds: int) -> str:
    """预填骨架：全部台账 id、值为 null。人工只填值，漏填由 validate 抓住。"""

    verdicts: dict[str, object] = {}
    for record_id in sorted(_ledger_ids()):
        entry: dict[str, object] = {arm: [None] * rounds for arm in arms}
        if record_id in REPORTABLE:
            # 可报记录预留方向位。命中而不填，`validate` 会拒。
            entry["direction"] = {arm: None for arm in arms}
        verdicts[record_id] = entry if len(arms) > 1 or record_id in REPORTABLE else [None] * rounds
    return json.dumps(
        {
            "_note": "1=命中 0=未命中 null=该轮该格失败。可报记录必须全部填写；"
                     "判为命中的可报记录还必须在 direction 里写出 docs/protocol/hit_criterion.md §3 的形态。",
            "_directions": DIRECTIONS,
            "_reportable_records": list(REPORTABLE),
            "_blocked": BLOCKED,
            "verdicts": verdicts,
            "over": {},
        },
        ensure_ascii=False,
        indent=1,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="从人工判定表算 metric@k，只做算术")
    parser.add_argument("verdicts_json", nargs="?", type=pathlib.Path)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--arms", default="claude,gpt", help="生成模板时的臂，逗号分隔")
    parser.add_argument("--template", action="store_true", help="打印预填骨架后退出")
    parser.add_argument(
        "--force", action="store_true", help="校验失败仍然计算。只用于诊断，结果不得引用"
    )
    parser.add_argument(
        "--no-direction-check", action="store_true",
        help="跳过命中的方向形态校验。只用于诊断中途状态，正式报告不得使用"
    )
    args = parser.parse_args(argv)

    if args.template:
        print(template([a for a in args.arms.split(",") if a], args.rounds))
        return 0
    if args.verdicts_json is None:
        parser.error("需要判定表路径，或用 --template 生成骨架")

    payload = json.loads(args.verdicts_json.read_text())
    verdicts = payload.get("verdicts") or {}
    over = payload.get("over") or {}
    problems = validate(verdicts, over, args.rounds, not args.no_direction_check)
    if problems:
        print(f"判定表有 {len(problems)} 处问题，拒绝计算：", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        if not args.force:
            print("修好后重跑，或用 --force 仅作诊断（结果不得引用）", file=sys.stderr)
            return 1
        print("!! --force：以下数字不得引用", file=sys.stderr)

    # 分母 = REPORTABLE，**不是判定表里出现的全部 id**。
    #
    # 这里原先按后者算，于是工具报 366/594 而全部文档报 360/588 —— 差的正是
    # `EIS-0043-02` 这条已被边界裁定剔除、但原始判定仍保留在表里的记录。后果不是
    # 「数字略有出入」，而是**声称的数字无法用真源工具复算**，审计者只能改用别的脚本。
    # 剔除口径写在 `_out_of_scope_record_ids()` 里，度量就必须用同一个口径。
    reportable = [r for r in verdicts if r in set(REPORTABLE)]
    dropped = [r for r in verdicts if r not in set(REPORTABLE)]
    if dropped:
        print(f"（已从分母剔除 {len(dropped)} 条：{sorted(dropped)}）")
    report_band(verdicts, reportable, "可报告记录", args.rounds)
    report_over(over)
    for record_id, why in BLOCKED.items():
        if record_id in verdicts:
            print(f"\n⚠️ {record_id} {why}：其未命中不构成能力缺口")
    return 0


if __name__ == "__main__":
    sys.exit(main())
