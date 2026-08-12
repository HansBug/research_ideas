"""填写块（FILL block）的格式定义、提取与再注入。

工作单是**机器生成 + 人工填写**混合的文件，所以必须能在不丢失人工内容的前提下重跑
生成器。做法是把每个待填区包在一对 HTML 注释哨兵之间：

    <!-- FILL:BEGIN key=EIS-0000-01 kind=ledger -->
    ~~~
    裁决: [ ] 保留  ...
    ~~~
    <!-- FILL:END key=EIS-0000-01 -->

重跑时先把旧文件里所有 `key -> 块内容` 抽出来，重新渲染骨架，再把旧内容按 key 注回。
⭐ 因此**生成器是幂等的**：材料变了就更新材料，人工填写原样保留。

⚠️ 围栏用 `~~~` 而不是 ``` —— 作者在理由里贴代码时通常用 ```，用同一种围栏会截断。
"""

from __future__ import annotations

import re

import newfields as NF

FENCE = "~~~"
_RE_BEGIN = re.compile(r"^<!--\s*FILL:BEGIN\s+key=(?P<key>\S+)\s+kind=(?P<kind>\S+)\s*-->\s*$")
_RE_END = re.compile(r"^<!--\s*FILL:END\s+key=(?P<key>\S+)\s*-->\s*$")

LEDGER_TEMPLATE = """裁决: [ ] 保留  [ ] 修正  [ ] 删除  [ ] 拆分
深度: [ ] 表层(单点存在性/拼写)  [ ] 中层(单点关系)  [ ] 深层(跨状态推理/隐含冲突/运行时后果)
理由:
修正后的 statement:"""

CANDIDATE_TEMPLATE = """裁决: [ ] 采纳(补入台账)  [ ] 不采纳  [ ] 待议  [ ] 并入现有条目
深度: [ ] 表层  [ ] 中层  [ ] 深层
并入到:
理由:
补入后的 statement:"""

# ⭐ 新增 issue 的字段与模板由 [newfields.py](./newfields.py) 定义 —— 那里同时放着
# 枚举、填写指引和脚本推导，⛔ 不要在本文件里另开一份，两处会立刻走偏。
def new_template(pair, count=2):
    return NF.template(pair, count)


# ⛔ 历史模板。⭐ 留着**只为识别「原样未填的旧模板」** —— 幂等注回是按 key 做的，
# 若不认出旧模板，字段表改版后旧骨架会被当成「人工内容」永久保留，
# 新字段永远出不来（实测：改版后重跑 54 份，§5 全部还是旧的 10 字段表）。
# ⚠️ 只做**逐字全等**匹配：作者若已经在旧模板上填了任何东西，就不算旧模板，原样保留。
LEGACY_NEW_TEMPLATES = ["""### NEW-{pair}-01
statement:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction
direction:
element_of_M: [ ] S  [ ] E  [ ] V  [ ] Tr  [ ] A
nl_evidence:
depth: [ ] 表层  [ ] 中层  [ ] 深层
primary_predicate:
证据(作者源行号):
来源: [ ] §3候选  [ ] §4清单  [ ] 自行发现

### NEW-{pair}-02
statement:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction
direction:
element_of_M: [ ] S  [ ] E  [ ] V  [ ] Tr  [ ] A
nl_evidence:
depth: [ ] 表层  [ ] 中层  [ ] 深层
primary_predicate:
证据(作者源行号):
来源: [ ] §3候选  [ ] §4清单  [ ] 自行发现"""]


def is_stale_template(body, kind, pair=""):
    """⭐ 该块是不是某个**历史版本的空模板**（因而可以安全换成当前模板）。"""
    if body is None or kind != "new":
        return False
    return any(body.strip() == t.format(pair=pair).strip() for t in LEGACY_NEW_TEMPLATES)

PAIR_TEMPLATE = """本 pair 整体判断: [ ] 台账在本 pair 上够用  [ ] 偏浅但方向对  [ ] 有实质遗漏  [ ] 需推倒重写
台账现有条目是否偏浅（整体）: [ ] 否  [ ] 部分  [ ] 是
本轮新增条目数:
耗时(分钟):
备注:"""


def extract(text):
    """从既有工作单里抽出 {key: 块内容（不含围栏）}。"""
    out = {}
    if not text:
        return out
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = _RE_BEGIN.match(lines[i])
        if not m:
            i += 1
            continue
        key = m.group("key")
        j = i + 1
        body = []
        while j < len(lines) and not _RE_END.match(lines[j]):
            body.append(lines[j])
            j += 1
        # 去掉首尾围栏行
        while body and body[0].strip() == FENCE:
            body.pop(0)
        while body and body[-1].strip() == FENCE:
            body.pop()
        out[key] = "\n".join(body)
        i = j + 1
    return out


def render(key, kind, default_body, saved=None):
    body = saved if saved is not None and saved.strip() else default_body
    return "\n".join([
        f"<!-- FILL:BEGIN key={key} kind={kind} -->",
        FENCE,
        body.rstrip(),
        FENCE,
        f"<!-- FILL:END key={key} -->",
    ])


def is_untouched(body, kind, pair=""):
    """块是否仍为模板原样（没有任何勾选、没有任何自由文本）。"""
    defaults = {
        "ledger": LEDGER_TEMPLATE,
        "candidate": CANDIDATE_TEMPLATE,
        "new": new_template(pair),
        "pair": PAIR_TEMPLATE,
    }
    d = defaults.get(kind)
    if d is not None and body.strip() == d.strip():
        return True
    if "[x]" in body.lower():
        return False
    # 检查有没有在冒号后写了东西
    for line in body.splitlines():
        if ":" in line:
            tail = line.split(":", 1)[1].strip()
            if tail and not tail.startswith("["):
                return False
    return "[x]" not in body.lower()
