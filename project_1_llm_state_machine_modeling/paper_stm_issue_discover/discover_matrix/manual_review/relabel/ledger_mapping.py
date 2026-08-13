"""既有台账条目 → 新缺陷座标系的**映射**：装载、校验、渲染取数。

真源是同目录的 [ledger_mapping.json](./ledger_mapping.json)，工作单 §2 从它渲染。

为什么要有这份中间产物
----------------------
99 条映射是一次**大规模判定**。若它只存在于渲染结果里，事后既无法复核也无法重算 ——
「这一条为什么判成 `pair` + `nondeterminism`」这个问题会没有答案。所以逐条落盘：
记录 id · 五个轴的取值 · **依据 statement 里的哪一句话** · 映射不上时卡在哪。

三条硬纪律
----------
1. **映射从 `statement` 正文推导，不从旧的 `layer` / `direction` / `element_of_M`
   字段机械转换。** 旧字段是我们自家词表，新取值有文献出处；拿旧字段换算等于把自家
   框架重新贴个标签，出处链会被污染。判定时给映射者的输入里**故意不含**那些旧字段。
2. **映射不上就标 `mappable: false` 并写清卡在哪个轴。** 不许为了表格整齐硬塞 ——
   映射不上的比例本身是有价值的数据：它度量新座标系对现有台账的覆盖度。
3. **映射是我方推断，不是事实。** 工作单里必须标明这一点；判读者不同意时，
   他的 `裁决` 与 `理由` 优先。

装载期机械门（对不上就**抛**，不静默跳过）
------------------------------------------
- id 集合必须与 **54 个在评 pair 的全部台账记录（99 条）逐一对上**，不多不少。
  少一条 = 有记录没被映射过，而工作单会照常渲染出一个空白格。
  ⛔ `00x8` 六个永久排除 pair 的 27 条**不在**映射范围内：它们不生成工作单、不进网格
  也不进分母，映射它们没有消费者。
- 取值必须在 `newfields.ENUMS` 内。
- 条件式一致性：`element` 支必须给 A + B 且 D 为空；逻辑支必须给 D 且 A / B 为空。
- `evidence` 必须是该条 `statement` 的**逐字子串**（按去空白后比对）。⚠️ 这一条是防伪造的
  唯一机械手段：改写过的「依据」看起来同样通顺，但它证明不了映射者真的读过原文。
- `mappable: false` 时五个轴全空，且 `note` 非空。
"""

from __future__ import annotations

import json
import os
import re

import newfields as NF
import sources as S

HERE = os.path.dirname(os.path.abspath(__file__))
MAPPING_FILE = os.path.join(HERE, "ledger_mapping.json")

SCHEMA = "paper1.relabel.ledger_mapping.v1"

AXES = ["defect_locus", "defect_element", "defect_qualifier",
        "defect_logic_kind", "defect_reference"]

OTHER_NOTE_FIELD = NF.OTHER_NOTE_FIELD


class MappingError(RuntimeError):
    """映射文件与台账 / 座标系对不上。⛔ 一律抛，不降级 —— 见模块 docstring。"""


def _squash(text):
    return re.sub(r"\s+", "", text or "")


def _check_one(rec, ledger):
    rid = rec.get("id")
    if rid not in ledger:
        raise MappingError(f"映射里的 `{rid}` 不在台账里")
    stmt = ledger[rid].get("statement") or ""
    ev = (rec.get("evidence") or "").strip()
    if not ev:
        raise MappingError(f"{rid} 没给 `evidence` —— 给不出逐字依据就是在猜")
    if _squash(ev) not in _squash(stmt):
        raise MappingError(
            f"{rid} 的 `evidence` 不是 statement 的逐字子串：{ev[:60]!r}")

    if not rec.get("mappable"):
        for axis in AXES:
            if rec.get(axis):
                raise MappingError(f"{rid} 标了无法映射，却给了 `{axis}`")
        if not (rec.get("note") or "").strip():
            raise MappingError(f"{rid} 标了无法映射，却没写卡在哪一个轴上")
        return

    for axis in AXES:
        val = rec.get(axis)
        if val is not None and val not in NF.ENUMS[axis]:
            raise MappingError(f"{rid} 的 `{axis} = {val}` 不在枚举内")
    locus = rec.get("defect_locus")
    if not locus:
        raise MappingError(f"{rid} 没给 `defect_locus`")
    if not rec.get("defect_reference"):
        raise MappingError(f"{rid} 没给 `defect_reference`")
    want = set(NF.required_axes_for(locus))
    forbid = set(NF.forbidden_axes_for(locus))
    for axis in want:
        if not rec.get(axis):
            raise MappingError(f"{rid} 走 `{locus}` 支却没给 `{axis}`")
    for axis in forbid:
        if rec.get(axis):
            raise MappingError(f"{rid} 走 `{locus}` 支却给了 `{axis}`")

    # ⭐ 任一轴取 `other` 必须附一句说明（类型学 §3.7.1）。
    # ⛔ 判据只看字段值，与 [validate.py](./validate.py) 对新增登记那条门是同一条规则 ——
    # 两处口径必须一致，否则「我方映射」可以留空出口、而判读者不许，那道门就没有说服力。
    picked = [a for a in AXES if rec.get(a) == "other"]
    if picked and not (rec.get(OTHER_NOTE_FIELD) or "").strip():
        raise MappingError(
            f"{rid} 的 " + "、".join(f"`{a}`" for a in picked)
            + f" 取了 `other`，却没写 `{OTHER_NOTE_FIELD}` —— 出口不写清等于没分类")


_CACHE = {}


def load(path=None):
    """读并校验整份映射，返回 {id: 映射记录}。校验不过直接抛。"""
    path = path or MAPPING_FILE
    if path in _CACHE:
        return _CACHE[path]
    if not os.path.exists(path):
        raise MappingError(
            f"缺 {os.path.basename(path)} —— 工作单 §2 的座标映射从它渲染，"
            "没有它就只能渲染出一批空白格")
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    rows = payload.get("mappings") or []
    # ⛔ 只认在评 pair 的 99 条 —— `00x8` 的 27 条不生成工作单，映射它们没有消费者。
    ledger = {r["id"]: r for p in S.IN_SCOPE_PAIRS for r in S.ledger_records(p)}
    seen = set()
    for rec in rows:
        _check_one(rec, ledger)
        if rec["id"] in seen:
            raise MappingError(f"{rec['id']} 在映射文件里出现了两次")
        seen.add(rec["id"])
    missing = sorted(set(ledger) - seen)
    if missing:
        raise MappingError(
            f"{len(missing)} 条台账记录没有映射：{missing[:5]}… "
            "—— 每条都必须有取值或明确标「无法映射」")
    out = {r["id"]: r for r in rows}
    _CACHE[path] = out
    return out


def for_record(rid):
    """取一条映射；台账里有而映射里没有的会在 `load()` 阶段就抛，故这里必然命中。"""
    return load()[rid]


def stats():
    """映射成功 / 无法映射的条数，以及各轴的取值分布。报告与总账用。"""
    from collections import Counter
    rows = list(load().values())
    ok = [r for r in rows if r.get("mappable")]
    bad = [r for r in rows if not r.get("mappable")]
    dist = {axis: Counter(r.get(axis) for r in ok if r.get(axis)) for axis in AXES}
    return {
        "total": len(rows),
        "mapped": len(ok),
        "unmapped": len(bad),
        "unmapped_ids": sorted(r["id"] for r in bad),
        "by_axis": {k: dict(sorted(v.items())) for k, v in dist.items()},
    }
