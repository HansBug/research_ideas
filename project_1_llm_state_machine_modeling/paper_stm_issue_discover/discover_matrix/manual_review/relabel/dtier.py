"""三方 D 档判读结果 → 工作单区块与裁决区预填。

两个事实源，⛔ 职责不许混：

  [dtier_rulings.json](./dtier_rulings.json)  三臂全量判定 + 机械分桶（脚本产出）
  [dtier_meta.json](./dtier_meta.json)        争议条目的人工 meta review（人写，持久化）

⛔⛔ **本模块不生成任何判断。** 它只做三件事：按桶选版式、把三臂原话逐字引出、
把 `dtier_meta.json` 里人写的归纳渲进去。⚠️ 争议条目的推荐、理由、分歧点、关注建议
一律来自人工归纳 —— 理由见 [docs/protocol/dtier_triage.md](../../docs/protocol/dtier_triage.md) §5：
脚本能做的只有拼接与计票，⛔ 而「这两读的分歧点在哪」需要读懂三臂各自的 `basis`
并判断谁更站得住。脚本代劳会产出**看起来像结论的模板文本**，⛔ 比留空更坏。

## 两条硬约束，⛔ 改本文件前必须先读

**① 版式必须紧凑，不许用表格。** 表头 + 分隔行会按条目数重复，54 份工作单上千次出现，
直接顶穿 `test_the_field_guide_is_not_copied_back_into_the_worksheets` 那道门（它数的是
**行的出现次数**，不是不同行数）。⭐ 故三臂对照压成一行、长文本各占一行、说明放 HOWTO。

**② 预填必须可被识别为「未经人确认」。** `prefill()` 的产出被当作 `fb.render()` 的
`default_body`，⛔ 而 `fb.is_untouched()` 要能认出它 —— 否则 380 条预填一上线，
进度统计立刻全部变成「已填」，⚠️ 而那是 2026-08-13 已经栽过一次的同型 bug
（幂等注回把旧模板当人工内容保留）。⭐ 判据走**逐字全等**，与 `is_stale_template` 同机制。
"""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RULINGS = os.path.join(HERE, "dtier_rulings.json")
META = os.path.join(HERE, "dtier_meta.json")

#: 三臂的显示名与模型。⛔ 不写成「臂 1/2/3」——判读者需要知道分歧来自不同模型家族。
ARM_ZH = {
    "codex": ("codex", "GPT-5"),
    "claude": ("claude", "Opus 5"),
    "dsh": ("dsh", "deepseek-v4-pro"),
}

#: 需要人处理的三桶各自的标记与抬头。⛔ `auto_*` 不在此表 —— 它们不打标记。
#: ⭐ emoji 遵循「对比」而非「数量」：两边都打，标记就不再是信号。
BUCKET_MARK = {
    "ambiguous": ("🟡", "**两读并立，需你在两读之间选**"),
    "leaning": ("🟠", "**有偏向，需你认可或否决推荐**"),
    "chaotic": ("🔴", "**三方无偏向，需你亲自裁决**"),
}

#: meta review 的四个字段：json 键 → 工作单里的中文抬头。⭐ 顺序即渲染顺序。
META_FIELDS = (("recommend", "推荐"), ("brief", "一句话理由"), ("reason", "理由"),
               ("crux", "分歧点"), ("focus", "重点关注"))

#: 人工归纳里 `recommend` 的合法取值 → 各 kind 的勾选项。
#: ⛔ 只认这几个词：`prefill()` 要靠它机械决定勾哪个框，⚠️ 自由文本会静默勾错。
REC_TO_CHOICE = {
    "D2": "按 D2 采纳",
    "D1": "按 D1 采纳",
    "不采纳": "不采纳",
}

#: 桶 → 标记。⭐ **每个条目 id 都带标记**，⛔ 让「谁要你裁、有多要紧」一眼可见。
#: ✅/❌ = 已定（不需你动）；🟡/🟠/🔴 = 需你裁，三级递增。
BUCKET_ICON = {
    "auto_keep": "✅",
    "auto_drop": "❌",
    "auto_d1": "❓",
    "ambiguous": "🟡",
    "leaning": "🟠",
    "chaotic": "🔴",
}

_META_CACHE = None
_RULINGS_CACHE = None


def load_rulings():
    global _RULINGS_CACHE
    if _RULINGS_CACHE is None:
        if not os.path.exists(RULINGS):
            _RULINGS_CACHE = {}
        else:
            with open(RULINGS, encoding="utf-8") as fh:
                _RULINGS_CACHE = json.load(fh).get("rulings") or {}
    return _RULINGS_CACHE


def load_meta():
    """读人写的 meta review。⭐ 存 json 是为了持久化与机器可读，⛔ 不再用 md 手写格式。

    ⚠️ 缺字段一律当「没写」，⛔ 不补默认值：一条 meta review 少了 `recommend`，
    含义是「我不给推荐」，⭐ 那与「推荐保留」是两件完全不同的事。
    """
    global _META_CACHE
    if _META_CACHE is not None:
        return _META_CACHE
    out = {}
    if os.path.exists(META):
        with open(META, encoding="utf-8") as fh:
            out = json.load(fh).get("reviews") or {}
    _META_CACHE = out
    return out


def get(rid):
    return load_rulings().get(rid)


def mark(rid):
    """条目标题后缀的标记。⭐ **每个条目都有**，⛔ 便于全文搜索与一眼分级。

    ✅ 确定采纳 · ❌ 确定不采纳 · 🟡 两读并立待选 · 🟠 有偏向待认可 · 🔴 无偏向待亲裁。
    ⚠️ `UM-` 一族无三方判读、一律人工裁决，故打 🟠。
    """
    rec = load_rulings().get(rid)
    if not rec:
        return " 🟠" if rid in load_meta() else ""
    return " " + BUCKET_ICON.get(rec.get("bucket"), "")

def _arm_line(rec):
    """三臂档位的一行式摘要。⛔ 不用表格 —— 见模块 docstring 约束 ①。"""
    parts = []
    for key in ("codex", "claude", "dsh"):
        a = (rec.get("arms") or {}).get(key) or {}
        extra = f"·{a.get('a0')}" if a.get("a0") else ""
        parts.append(f"{ARM_ZH[key][0]} `{a.get('tier') or '?'}{extra}`")
    return " / ".join(parts)


def _readings(rec):
    """第二种读法与设计意图主张，逐字。⭐ 这两样是「两读并立」的实体，⛔ 不许省。"""
    out = []
    for field, label in (("alternative_reading", "第二种读法"),
                         ("design_rationale", "作者可主张的设计意图")):
        for key in ("codex", "claude", "dsh"):
            a = (rec.get("arms") or {}).get(key) or {}
            v = (a.get(field) or "").strip().replace("\n", " ")
            if v:
                out.append(f"- {label}（{ARM_ZH[key][0]} 原话）：{v}")
    return out


def _opinions(rec):
    """三臂各自的判定依据，逐字，折叠。⭐ 每臂一行 —— 长文本不占额外行数。"""
    out = ["<details><summary>三臂各自的判定依据（原话逐字）</summary>", ""]
    for key in ("codex", "claude", "dsh"):
        a = (rec.get("arms") or {}).get(key) or {}
        b = (a.get("basis") or "").replace("\n", " ").strip()
        out.append(f"- **{ARM_ZH[key][0]}**（判 `{a.get('tier')}`）：{b or '（未给）'}")
    out += ["", "</details>", ""]
    return out


def _meta_lines(rid, bucket):
    """人工 meta review。⛔ 缺失时如实说明，不编造。"""
    m = load_meta().get(rid)
    if not m:
        return ["- 人工 meta review **待补** —— 本条属需人裁桶，推荐与分歧点必须人工归纳"
                "（脚本不代劳，理由见 "
                "[dtier_triage.md](../../../docs/protocol/dtier_triage.md) §5）。"]
    out = []
    rv = (m.get("recommend") or "").strip()
    if rv:
        out.append(f"- 人工归纳推荐：**{rv}**（已按此预填下面的裁决区）")
    elif bucket == "chaotic":
        out.append("- 人工归纳**不给推荐**，裁决区留空 —— 三方无偏向，硬给一个等于替你决定。")
    for k, zh in META_FIELDS[1:]:
        v = (m.get(k) or "").strip()
        if v:
            out.append(f"- {zh}：{v}")
    return out


def block(rid):
    """一条条目的三方判读区块。⭐ 无争议的压到一行，⛔ 需人裁的才展开。"""
    rec = load_rulings().get(rid)
    if not rec:
        # ⭐ `UM-` 一族：无三方判定，只有人工 meta review。⛔ 一律人工裁决。
        m = load_meta().get(rid)
        if not m:
            return []
        out = ["**人工 meta review** 🟠 **本块无三方判读（不在判读包内），一律人工裁决**", ""]
        for k, zh in META_FIELDS:
            v = (m.get(k) or "").strip()
            if not v:
                continue
            out.append(f"- {'**推荐**' if k == 'recommend' else zh}：{v}")
        out.append("")
        return out
    bucket = rec.get("bucket") or "?"
    combo = rec.get("combo")
    if bucket == "auto_d1":
        return [f"**三方 D 档判读** ❓ **三臂一致判「两读并立」（`D1`）**：票面 `{combo}`。",
                "",
                "「这段内容本身就是模糊的」已是三方共识，⛔ 故不需你在两读之间选 —— "
                "裁决区已按 `D1` 预填。⚠️ 但它**不是**一条确定的缺陷，"
                "入账时必须带着那个第二读法一起记。", ""] + _readings(rec) + [""] + _opinions(rec)
    if bucket not in BUCKET_MARK:
        verdict = "保留" if bucket == "auto_keep" else "抛弃"
        return [f"**三方 D 档判读**：票面 `{combo}`（{_arm_line(rec)}），"
                f"三臂方向一致判「**{verdict}**」，裁决区已按此预填。", ""]
    mk, desc = BUCKET_MARK[bucket]
    out = [f"**三方 D 档判读** {mk} {desc}", "",
           f"票面 `{combo}`：{_arm_line(rec)}。", ""]
    out += _readings(rec)
    out += _meta_lines(rid, bucket)
    out.append("")
    out += _opinions(rec)
    return out


def compact(rid):
    """一行式摘要，给**没有自己裁决区**的条目用（inspect 补充证据那一族）。

    ⛔ 不展开完整区块：那些条目按设计不设裁决区（同一个问题只裁一次，裁决落在宿主条目上），
    ⚠️ 摆一整块「需你裁决」却没有可勾的地方，会让判读者以为漏了块。
    """
    rec = load_rulings().get(rid)
    if not rec:
        return []
    m = BUCKET_MARK.get(rec.get("bucket"))
    tail = ""
    if m:
        meta = load_meta().get(rid) or {}
        rv = (meta.get("recommend") or "").strip()
        crux = (meta.get("crux") or "").strip()
        tail = (f" 人工归纳推荐**{rv}**。" if rv else " 人工 meta review 待补。")
        if crux:
            tail += f"分歧点：{crux}"
    return [f"- 三方 D 档判读：票面 `{rec.get('combo')}`（{_arm_line(rec)}）。"
            f"{m[1] + '（裁决落在本条的宿主条目上）。' if m else '三臂方向一致。'}{tail}", ""]


# ------------------------------------------------------------------ 裁决区预填

#: 预填体的尾标。⭐ 它是「这份是我方预填、你还没确认」的唯一判据，
#: ⛔ 不许改动措辞 —— `fillblocks.is_untouched()` 靠逐字全等认它。
PREFILL_TAIL = "（此为我方预填，删除此括号内的内容后即视为已处理）"


def _choice_line(kind, choice):
    """把某个选项勾上，其余留空。⛔ 从 fillblocks 的模板取选项表，不另抄一份。"""
    import fillblocks as fb
    # ⭐ 2026-08-14 起两个 kind 共用同一个模板（采纳 / 不采纳 + 理由），故不再分支。
    head = fb.LEDGER_TEMPLATE.splitlines()[0]
    if not choice:
        return head
    out, hit = [], False
    for m in re.finditer(r"\[\s*\]\s*([^\[]+?)(?=\s{2,}\[|\s*$)", head):
        name = m.group(1).strip()
        box = "[x]" if (name == choice and not hit) else "[ ]"
        if name == choice:
            hit = True
        out.append(f"{box} {name}")
    if not hit:                       # ⛔ 选项名对不上就不勾，⚠️ 不许猜
        return head
    return "裁决: " + "  ".join(out)


def _auto_brief(rec, keep):
    """无争议条目的一句话理由。⭐ 取三臂一致认定的那条义务出处，拼成人话。

    ⛔ 不是套话：`nl_quote` / `obligation_sentence` / A0 出局口都是**这一条特有**的内容。
    ⚠️ 三样都取不到时才退回一句概括，并明写「三臂未给出可引的出处」——
    ⭐ 那本身是有信息的（说明这一条的判定没落在可复核的锚点上）。
    """
    arms = rec.get("arms") or {}
    if keep:
        for k in ("codex", "claude", "dsh"):
            q = ((arms.get(k) or {}).get("nl_quote") or "").strip()
            if q:
                return (f"**判 D2**：三臂一致认定它违反了 NL 里这句「{q[:90]}」，"
                        f"且三方都尝试过推翻、都没找到站得住的第二种读法 —— "
                        f"义务有成文条文可引、反驳不存活，是 `D2-lit`。")
        for k in ("codex", "claude", "dsh"):
            o = ((arms.get(k) or {}).get("obligation_sentence") or "").strip()
            if o:
                return (f"**判 D2**：三臂一致认定它违反了这条领域义务：{o[:110]}"
                        f"；没人拿出站得住的第二种读法 —— 义务已被陈述、反驳不存活，是 `D2-norm`。")
        g = {(arms.get(k) or {}).get("grounding") for k in arms}
        if "impl" in g:
            return ("**判 D2**：三臂一致认定它是死锁（进去出不来）——"
                    "这一类免领域知识、免形式规约即可判为失效，且没人拿出「作者显式声明合法终止」"
                    "的依据，是 `D2-impl`。")
        return ("**判 D2**：三臂一致判它成立，⚠️ 但都没给出可引的 NL 原句或领域义务 —— "
                "⛔ 建议你顺手核一眼它的义务出处，若拿不出出处应降到 D1。")
    a0 = [(arms.get(k) or {}).get("a0") for k in ("codex", "claude", "dsh")]
    a0 = [x for x in a0 if x]
    if len(a0) == 3:
        kinds = sorted(set(a0))
        why = {"非主张": "它评的不是作者写的那份模型（而是参考模型或评测真值）",
               "越界": "它涉及时钟、不变式或正交区并发，不在本研究的建模对象内",
               "误报": "它声称的结构事实在作者源上不成立"}
        return ("三臂一致认为它压根没进入缺陷判定：" +
                "；".join(why.get(x, x) for x in kinds) + " —— 不该留在台账。")
    for k in ("codex", "claude", "dsh"):
        d = ((arms.get(k) or {}).get("design_rationale") or "").strip()
        if d:
            return (f"三臂一致认为作者可以正当地说「这就是设计」：{d[:110]}"
                    f" —— 不构成缺陷。")
    return ("三臂一致判它不成立（找不出被违反的义务，或作者的设计说法站得住） —— 不该留在台账。")


def prefill(key, kind):
    """裁决区的预填体。无判定记录、或该桶不预填时返回 `None`（调用方回落到空模板）。

    ⛔⛔ **`chaotic` 桶不勾任何框。** 三方无偏向时勾一个等于替人决定，
    ⚠️ 而人一眼看到已勾就很可能直接放过 —— 那是把「最需要人判的一批」变成橡皮章。
    ⭐ 但理由行照样写满：分歧在哪、该重点看什么，那些是有依据的。
    """
    if kind not in ("ledger", "candidate"):
        return None
    rec = load_rulings().get(key)
    meta = load_meta().get(key) or {}
    # ⭐ `UM-` 一族没有三方 D 判定（它们不在判读包里），⛔ 但用户要求它们也必须有
    # 推荐与理由，且**一律人工裁决**。⚠️ 故有 meta review 就照它预填，不看有没有 ruling。
    if not rec:
        # ⭐ `UM-` 一族：无三方 D 判定（不在判读包内），⛔ 一律人工裁决 —— 故照需人裁那套走。
        if not meta:
            return None
        rv = (meta.get("recommend") or "").strip()
        ch = REC_TO_CHOICE.get(rv) if rv else None
        why = (meta.get("brief") or "").strip() or "人工 meta review 待补。"
        import fillblocks as fb
        return "\n".join([_choice_line(kind, ch), f"meta review 意见: {why}",
                           f"理由: {fb.REASON_PLACEHOLDER}"])
    bucket = rec.get("bucket")
    combo = rec.get("combo")
    src = f"三方独立判读票面 `{combo}`（{_arm_line(rec)}）"

    # ⭐⭐ 理由行必须是**一句自包含的人话**，说清为什么勾这个 yes/no。
    # ⛔ 不许只引票面（`票面 D2+D2+D2`）—— 那不是理由，是出处；⚠️ 读者还得自己去推。
    # ⭐ 需人裁的条目用人工 meta review 的 `brief`；⭐ 无争议的条目用三臂一致认定的
    # 那条义务出处拼一句（`_auto_brief()`），⛔ 仍然是本条特有的内容，不是模板套话。
    if bucket in BUCKET_MARK:
        rv = (meta.get("recommend") or "").strip()
        choice = rv or None
        why = (meta.get("brief") or "").strip()
        if not why:
            why = ("人工 meta review 待补 —— 请对照上面三臂原话自行判断。")
    elif bucket == "auto_d1":
        # ⭐ 三臂一致判「两读并立」⇒ 那本身就是共识，⛔ 不需人在两读之间选。
        choice = "D1"
        why = ((meta.get("brief") or "").strip()
               or _auto_brief(rec, True))
    elif bucket == "auto_keep":
        choice, why = "D2", _auto_brief(rec, True)
    elif bucket == "auto_drop":
        choice, why = "不采纳", _auto_brief(rec, False)
    else:
        return None

    ch = REC_TO_CHOICE.get(choice) if choice else None
    import fillblocks as fb
    lines = [_choice_line(kind, ch), f"meta review 意见: {why}"]
    # ⭐⭐ **只有需人裁的条目才带待填 `理由` 栏。**
    # ⛔ 无争议的条目不带 —— 我方已给决议与意见，⚠️ 让人去删一个括号纯属白做，
    # ⭐ 而「不需要人动」正是它与需人裁那批的实质区别，版式上必须体现出来。
    if bucket in BUCKET_MARK or not rec:
        lines.append(f"理由: {fb.REASON_PLACEHOLDER}")
    return "\n".join(lines)


# ------------------------------------------------------------------ 速览与统计

def pair_overview(pair):
    """一份工作单顶部的待处理速览。⭐ 让人不必逐节翻就知道这份要花多少工夫。

    ⛔ 必须极短：NL 表必须留在第一屏（`test_nl_table_sits_on_the_first_screen`
    要求它在第 45 行以内），⚠️ 本节每多一行就把 NL 往下推一行。
    """
    R = {rid: rec for rid, rec in load_rulings().items() if rec.get("pair") == pair}
    if not R:
        return []
    need = []
    for b in ("chaotic", "leaning", "ambiguous"):
        ids = sorted(rid for rid, rec in R.items() if rec.get("bucket") == b)
        if ids:
            need.append(f"{BUCKET_MARK[b][0]} {len(ids)} 条（" +
                        "、".join(f"`{i}`" for i in ids) + "）")
    n = sum(1 for rec in R.values() if rec.get("bucket") in BUCKET_MARK)
    out = [f"**三方 D 档判读速览**：本 pair {len(R)} 条进了判读，其中 **{n} 条需你处理** —— "
           + ("；".join(need) if need else "无") +
           f"。其余 {len(R) - n} 条三臂方向一致，裁决区已预填。"
           f"标记含义与分桶判据见 "
           f"[dtier_triage.md](../../../docs/protocol/dtier_triage.md)。", ""]
    return out


def stats():
    return dict(collections.Counter(v.get("bucket") for v in load_rulings().values()))


def missing_meta(extra_keys=()):
    """**没有**人工 meta review 的条目 id（排序后）。⭐ 这是欠账清单。

    ⚠️⚠️ **2026-08-14 口径扩到全部条目。** 用户裁定：「全部条目都得有 meta review 意见，
    包括没有争议的，也都得有对应针对性的 meta review 文本」——⛔ 所以这里不再只数
    需人裁的那几桶。⭐ 无争议的条目虽然不需要人做动作，但仍需一句**针对本条**的说明，
    ⚠️ 否则读者只看到一个 ✅ 而不知道它凭什么成立。

    `extra_keys` 用来把没有 D 判定的键（`UM-` 一族）也纳进来。
    """
    meta = load_meta()
    out = [rid for rid in load_rulings() if rid not in meta]
    out += [k for k in extra_keys if k not in meta and k not in load_rulings()]
    return sorted(set(out))
