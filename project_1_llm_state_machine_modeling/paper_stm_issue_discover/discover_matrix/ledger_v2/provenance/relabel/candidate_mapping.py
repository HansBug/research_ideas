"""候选线索（§3）→ 新缺陷座标系的**映射**：装载、校验、渲染取数。

真源是同目录的 [candidate_mapping.json](./candidate_mapping.json)，工作单 §3 从它渲染。
台账侧的同名件是 [ledger_mapping.py](./ledger_mapping.py)，两者规则一致、对象不同。

⛔ 候选**不是**台账条目。它们没有经过人工确认，可能本身就不成立 —— 判读者要判的正是这件事。
所以这里映射的是「**如果**它成立，它属于座标系的哪一格」，⛔ 不是「它成立」。
工作单渲染时必须把这一点写在每一格旁边，否则判读者会以为它们已被认定。

三类候选的**结构不同构**，⛔ 不要当成同一种东西
--------------------------------------------------
| 前缀 | 条数 | 一条 = 什么 | 能不能用一格座标代表 |
| :-- | --: | :-- | :-- |
| `VU-` | 15 | 一个多报簇 = 一个主张 | 能 |
| `DIFF-` | 77 | 一条审阅 diff = 一个主张 | 能 |
| `UM-` | 49 | **整张表**（一个 pair 的全部未匹配 issue）= 一个填写块 | ⛔ 多数不能 |

`UM-xxxx` 底下坐着 1 到 35 个互不相同的线索组（全语料 619 组，中位 11 组/桶）。
⚠️ 它是**登记单位**层面的对象，不是主张层面的对象。给整桶挑一格座标会让判读者
以为整桶都是那一格，故桶内各组座标不一致时一律 `mappable: false`，
并在 `note` 里举出至少两组、各自给出座标，证明它们确实不同。

⚠️⚠️ **`mappable: false` 有三种卡点，⛔ 混写会污染「座标系覆盖度」这个数字。
⛔ 只有第三种才是座标系的问题**：

- `blocker = "unit_of_record"` —— 卡在**登记单位**：一个 id 底下坐着多条异质主张，
  逐条各自都能落格，只是一格代表不了整体。⛔ 这**不是**座标系覆盖不到。
- `blocker = "not_a_defect_claim"` —— 它**根本不是一条缺陷形态主张**。典型三族：
  ① `gen` 字段逐字写「—」或「(不可能生成)」，即否认作者制品有问题，主张的是
  参考模型 / 真值的有效性；② 语料元数据与实验独立性（两份制品 md5 相同之类）；
  ③ 制品来源（provenance）。座标系的判定测试全部锚在**作者源 PlantUML** 上，
  这类在制品内指不出任何一处，卡在轴 0。⛔ 这同样**不是**座标系覆盖不到 ——
  ⛔ 不得拿去当「新座标表达不了」的证据。
- `blocker = "taxonomy"` —— 卡在**座标系**：某个轴给不出不失真的取值。
  ⭐ 这才是新座标系的真缺口。

⭐ 实测（240 个对象全量）：`taxonomy` 卡点**全部**是同一处 —— **正交区域及其数量**。
轴 A 的 7 个取值里没有 region，且类型学 §3.7 明写正交区并发语义界外、
「不得取为维度取值」。台账侧 4 条 + 候选侧 8 条，⛔ 由三批互不通气的判定者独立撞到，
⭐ 故它是座标系的**真缺口**，⛔ 不是判读噪声。

装载期机械门（对不上就**抛**，不静默跳过）
------------------------------------------
- key 集合必须与 `candidate_index()` 枚举出的 **141 个候选逐一对上**，不多不少。
  少一个 = 有候选没被映射过，而工作单会照常渲染出一个空白格。
- 取值必须在 `newfields.ENUMS` 内。
- 条件式一致性：`element` 支必须给 A + B 且 D 为空；逻辑支必须给 D 且 A / B 为空。
- `evidence` 必须是该候选**任一描述字段**的**逐字子串**（按去空白后比对）。
  ⚠️ 这一条是防伪造的唯一机械手段：改写过的「依据」看起来同样通顺，
  但它证明不了映射者真的读过原文。
- `mappable: false` 时五个轴全空，且 `note` 非空。
- `blocker` 可选；给了就必须在 `BLOCKERS` 内，且只允许出现在 `mappable: false` 的条目上。
"""

from __future__ import annotations

import functools
import json
import os
import re

import newfields as NF
import sources as S

HERE = os.path.dirname(os.path.abspath(__file__))
MAPPING_FILE = os.path.join(HERE, "candidate_mapping.json")

SCHEMA = "paper1.relabel.candidate_mapping.v1"

AXES = ["defect_locus", "defect_element", "defect_qualifier",
        "defect_logic_kind", "defect_reference"]

OTHER_NOTE_FIELD = NF.OTHER_NOTE_FIELD

#: `mappable: false` 的三种卡点。⛔ 见模块 docstring —— 三者不得混写。
#: ⛔ 只有 `taxonomy` 能算作「新座标系覆盖不到」。
BLOCKERS = ("unit_of_record", "not_a_defect_claim", "taxonomy")

BLOCKER_ZH = {
    "unit_of_record": (
        "登记单位",
        "这一个 id 底下坐着多条异质主张，逐条各自都能落格，只是一格代表不了整体。"
        "座标系本身没有覆盖不到。",
    ),
    "not_a_defect_claim": (
        "不是缺陷形态主张",
        "它主张的是参考模型 / 真值的有效性、语料元数据或制品来源，"
        "而不是作者制品里的某处有毛病。判定测试锚在作者源 PlantUML 上，"
        "这类在制品内指不出任何一处。座标系本身没有覆盖不到。",
    ),
    "taxonomy": (
        "座标系",
        "某个轴给不出不失真的取值 —— 这才是新座标系的真缺口。",
    ),
}

#: 每类候选的**描述字段**。`evidence` 的逐字子串在这些字段的并集里查。
#: ⛔ 顺序即渲染顺序，⛔ 不要按字典序重排。
TEXT_FIELDS = {
    "valid_unrecorded": ("claim", "fact", "nl", "note"),
    "review_diff": ("ref", "gen", "reason"),
    "unmatched_issue": ("issue", "reason"),
}


class MappingError(RuntimeError):
    """映射文件与候选 / 座标系对不上。⛔ 一律抛，不降级 —— 见模块 docstring。"""


def _squash(text):
    return re.sub(r"\s+", "", text or "")


# ---------------------------------------------------------------- 候选枚举

@functools.lru_cache(maxsize=1)
def candidate_index():
    """`{key: {"pair", "kind", "texts"}}` —— 141 个候选的**唯一**枚举口径。

    ⛔ 这里的 key 生成规则必须与 [generate.py](./generate.py) 的 §3 渲染逐字一致；
    ⭐ `test_the_candidate_index_matches_what_the_worksheets_render` 把两者钉在一起，
    ⛔ 任何一侧改了编号规则都会立刻报错，而不是留下一批对不上的空白格。
    """
    out = {}
    for pair in S.IN_SCOPE_PAIRS:
        for i, r in enumerate(S.valid_unrecorded(pair), 1):
            out[f"VU-{pair}-{i:02d}"] = {
                "pair": pair, "kind": "valid_unrecorded",
                "texts": [r.get(f) for f in TEXT_FIELDS["valid_unrecorded"]],
            }
        for i, d in S.unadopted_diffs(pair):
            if d.get("verdict") in ("problem", "extra", "uncertain"):
                out[f"DIFF-{pair}-{i:02d}"] = {
                    "pair": pair, "kind": "review_diff",
                    "texts": [d.get(f) for f in TEXT_FIELDS["review_diff"]],
                }
        um = S.unmatched_issues(pair)
        if um:
            out[f"UM-{pair}"] = {
                "pair": pair, "kind": "unmatched_issue",
                "texts": [e.get(f) for e in um for f in TEXT_FIELDS["unmatched_issue"]],
            }
    return out


def _corpus(key):
    return _squash(" ".join(t for t in candidate_index()[key]["texts"] if t))


# ---------------------------------------------------------------- 校验

def _check_one(rec, index):
    key = rec.get("id")
    if key not in index:
        raise MappingError(f"映射里的 `{key}` 不是本轮的候选")
    ev = (rec.get("evidence") or "").strip()
    if not ev:
        raise MappingError(f"{key} 没给 `evidence` —— 给不出逐字依据就是在猜")
    if _squash(ev) not in _corpus(key):
        raise MappingError(
            f"{key} 的 `evidence` 不是该候选描述正文的逐字子串：{ev[:60]!r}")

    blocker = rec.get("blocker")
    if blocker is not None and blocker not in BLOCKERS:
        raise MappingError(f"{key} 的 `blocker = {blocker}` 不在 {BLOCKERS} 内")

    if not rec.get("mappable"):
        for axis in AXES:
            if rec.get(axis):
                raise MappingError(f"{key} 标了无法映射，却给了 `{axis}`")
        if not (rec.get("note") or "").strip():
            raise MappingError(f"{key} 标了无法映射，却没写卡在哪一个轴上")
        return

    if blocker is not None:
        raise MappingError(
            f"{key} 已映射成功却带着 `blocker` —— 卡点只描述 `mappable: false` 的条目")
    for axis in AXES:
        val = rec.get(axis)
        if val is not None and val not in NF.ENUMS[axis]:
            raise MappingError(f"{key} 的 `{axis} = {val}` 不在枚举内")
    locus = rec.get("defect_locus")
    if not locus:
        raise MappingError(f"{key} 没给 `defect_locus`")
    if not rec.get("defect_reference"):
        raise MappingError(f"{key} 没给 `defect_reference`")
    for axis in NF.required_axes_for(locus):
        if not rec.get(axis):
            raise MappingError(f"{key} 走 `{locus}` 支却没给 `{axis}`")
    for axis in NF.forbidden_axes_for(locus):
        if rec.get(axis):
            raise MappingError(f"{key} 走 `{locus}` 支却给了 `{axis}`")

    # ⭐ 任一轴取 `other` 必须附一句说明（类型学 §3.7.1）。
    # ⛔ 判据只看字段值，与 [validate.py](./validate.py) 对新增登记那条门是同一条规则 ——
    # 两处口径必须一致，否则「我方映射」可以留空出口、而判读者不许，那道门就没有说服力。
    picked = [a for a in AXES if rec.get(a) == "other"]
    if picked and not (rec.get(OTHER_NOTE_FIELD) or "").strip():
        raise MappingError(
            f"{key} 的 " + "、".join(f"`{a}`" for a in picked)
            + f" 取了 `other`，却没写 `{OTHER_NOTE_FIELD}` —— 出口不写清等于没分类")


_CACHE = {}


def load(path=None):
    """读并校验整份映射，返回 `{key: 映射记录}`。校验不过直接抛。"""
    path = path or MAPPING_FILE
    if path in _CACHE:
        return _CACHE[path]
    if not os.path.exists(path):
        raise MappingError(
            f"缺 {os.path.basename(path)} —— 工作单 §3 的座标映射从它渲染，"
            "没有它就只能渲染出一批空白格")
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    rows = payload.get("mappings") or []
    index = candidate_index()
    seen = set()
    for rec in rows:
        _check_one(rec, index)
        if rec["id"] in seen:
            raise MappingError(f"{rec['id']} 在映射文件里出现了两次")
        seen.add(rec["id"])
    missing = sorted(set(index) - seen)
    if missing:
        raise MappingError(
            f"{len(missing)} 个候选没有映射：{missing[:5]}… "
            "—— 每个都必须有取值或明确标「无法映射」")
    out = {r["id"]: r for r in rows}
    _CACHE[path] = out
    return out


def for_candidate(key):
    """取一条映射。候选里有而映射里没有的会在 `load()` 阶段就抛，故这里必然命中。"""
    return load().get(key)


def stats():
    """映射成功 / 无法映射的条数，按前缀与卡点分开 —— ⛔ 两种卡点不得合并计数。"""
    from collections import Counter
    rows = list(load().values())

    def prefix(key):
        return key.split("-")[0]

    ok = [r for r in rows if r.get("mappable")]
    bad = [r for r in rows if not r.get("mappable")]
    return {
        "total": len(rows),
        "mapped": len(ok),
        "unmapped": len(bad),
        "by_prefix": {p: {"total": sum(1 for r in rows if prefix(r["id"]) == p),
                          "mapped": sum(1 for r in ok if prefix(r["id"]) == p),
                          "unmapped": sum(1 for r in bad if prefix(r["id"]) == p)}
                      for p in ("VU", "DIFF", "UM")},
        "by_blocker": dict(Counter(r.get("blocker") or "unlabelled" for r in bad)),
        "by_axis": {axis: dict(sorted(Counter(
            r.get(axis) for r in ok if r.get(axis)).items())) for axis in AXES},
    }
