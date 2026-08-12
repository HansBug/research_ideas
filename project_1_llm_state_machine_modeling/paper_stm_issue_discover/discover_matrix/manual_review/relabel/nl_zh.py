"""NL 规约的**中文严格翻译**装载层。

⭐ 译文不写在本文件里，而是逐份存放在 [translations/](./translations/)：一份 NL 一个
`nl_<编号>.json`，验收依据是同目录的
[TRANSLATION_SPEC.md](./translations/TRANSLATION_SPEC.md)。本模块只负责把它们装进内存、
按段 id 索引，并在装载时做**机械对拍**。

⭐ 这份译文是给人**判缺陷**用的，⛔ 不是给人读着舒服用的。翻译纪律（详见 SPEC）：

1. ⭐ **严格直译**，⛔ 不意译、⛔ 不润色、⛔ 不补充原文没有的信息。
2. ⛔ **保留原文的模糊性**。原文没说清的（谁是主语、条件之间是「且」还是「或」、
   源状态是哪个），译文**照样不说清**，只在末尾用 `〔译者存疑：…〕` 点出这里含糊，
   ⛔ 不替它消歧 —— 消歧就是替作者做了本轮要他自己做的判断。
3. ⭐ **技术术语保留英文原词**并在括号里给中文，如 `sub machine state`（子机状态）。
4. ⭐ **状态名 / 事件名 / 变量名一律保留英文原样**，⛔ 不翻译。
5. ⚠️ 原文有语法或拼写错误时**照直译**，并在译文后加 `〔原文如此：…〕` 说明错在哪。
6. ⭐ 段首的编号照抄原文（语料里编号本身就有重复与缺空格，那也是信息）。

⭐ 每份 JSON 除逐段 `zh` 外还带两样东西，⛔ 它们与译文同等重要：

- `segments[*].note` —— **逐段判读提示**：该段约束了模型的哪个元素、歧义点在哪、
  哪部分落在 $M = (S, E, V, Tr, A)$ 边界之外。⭐ 判「违反」时先读它。
- `translator_notes` —— **整份 NL 层面的观察**：术语表、跨句反复出现的歧义、原文质量问题。

⛔ **索引口径：JSON 的 `sha8` 是 NL 全文 sha256 的前 8 位**，不是 pair 号 —— 60 个 pair
由 10 份 NL 各生成 6 个制品，同一份 NL 的 6 个 pair 共用同一套译文。⛔ 段 id（`NL-M001` /
`NL-L001`）**不写在 JSON 里**：JSON 的 `seg` 只是序号，装载时按**位置**对到
`sources.nl_segments()` 给出的段上，并**逐段核对 `en` 与原文逐字节相等** —— 对不上就抛
`TranslationMismatch`，⛔ 不静默套用。若 `nl.txt` 的字节变了，sha8 随之变化，译文会**查不到**
而不是被套到改动后的文本上；[test_relabel.py](./test_relabel.py) 的
`test_every_nl_segment_has_a_chinese_translation` 会把这种情况打成失败。

⛔ 本模块只放译文与判读提示，**不放任何裁决**。`〔译者存疑〕`与 `note` 只陈述「原文这里没说清 /
这句约束了什么」，⛔ 不得写成「所以模型应该怎样」—— 那是重标时人要填的东西，不是材料该替他填的。

⚠️ `00x8` 组（sha8 `6af3966c`）的 NL 要求 fork/join 与秒级时间约束，按
[nl_scope_rule.md](../../docs/protocol/nl_scope_rule.md) 永久排除，⛔ 不生成工作单，
故 [translations/](./translations/) **不收**它的译文。
"""

from __future__ import annotations

import functools
import glob
import hashlib
import json
import os

import sources as S

HERE = os.path.dirname(os.path.abspath(__file__))
TRANS_DIR = os.path.join(HERE, "translations")


class TranslationMismatch(RuntimeError):
    """译文与语料对不上。⛔ 只在装载时抛，⛔ 绝不降级成「跳过这一份」。

    ⭐ 静默跳过的后果是工作单里少了译文列而没人发现；抛出来的后果是 `generate.py`
    当场失败。⛔ 后者才是对的 —— 材料错了就不该产出工作单。
    """


def digest(pair):
    """该 pair 的 NL 全文 sha256 前 12 位 —— 与 `overrides.json` 的键同口径。"""
    return hashlib.sha256(S.nl_text(pair).encode("utf-8")).hexdigest()[:12]


def digest8(pair):
    """该 pair 的 NL 全文 sha256 前 8 位 —— 与译文 JSON 的 `sha8` 字段同口径。"""
    return digest(pair)[:8]


@functools.lru_cache(maxsize=1)
def _raw():
    """读盘：`{sha8: (文件名, JSON)}`。⛔ 同一 sha8 出现两份文件即报错。"""
    out = {}
    for path in sorted(glob.glob(os.path.join(TRANS_DIR, "nl_*.json"))):
        name = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as fh:
            j = json.load(fh)
        sha8 = j.get("sha8")
        if not sha8:
            raise TranslationMismatch(f"{name} 缺 `sha8` 字段")
        if sha8 in out:
            raise TranslationMismatch(
                f"{name} 与 {out[sha8][0]} 的 sha8 都是 {sha8} —— 同一份 NL 有两套译文")
        out[sha8] = (name, j)
    return out


@functools.lru_cache(maxsize=1)
def _pairs_by_sha8():
    """`{sha8: [pair, …]}`，只统计在评的 54 个 pair。"""
    out = {}
    for pair in S.IN_SCOPE_PAIRS:
        out.setdefault(digest8(pair), []).append(pair)
    return out


@functools.lru_cache(maxsize=1)
def _store():
    """装载 + 机械对拍，返回 `{sha8: {seg_id: {"zh":…, "note":…}}}` 与整份观察。

    ⭐ 三道对拍，⛔ 任何一道不过就抛：

    1. **孤儿文件** —— JSON 的 sha8 对不上任何在评 pair。⚠️ 这通常意味着 `nl.txt` 改了字节
       而译文没跟上，⛔ 此时若静默忽略，工作单会整份缺译。
    2. **段数不等** —— 分段口径变了（例如 `overrides.json` 改了切点）。
    3. **`en` 与原文不等** —— 译文对着另一版原文写的。⭐ 逐段逐字节比，⛔ 不比整篇哈希：
       整篇相等而段边界错位，逐段比才抓得住。
    """
    by_sha8 = _pairs_by_sha8()
    trans, notes, tnotes = {}, {}, {}
    for sha8, (name, j) in _raw().items():
        pairs = by_sha8.get(sha8)
        if not pairs:
            raise TranslationMismatch(
                f"{name} 的 sha8 {sha8} 对不上任何在评 pair —— "
                f"要么 nl.txt 变了字节，要么这份译文本就不该在这里")
        segs, _mode = S.nl_segments(pairs[0])
        jsegs = j.get("segments") or []
        if len(jsegs) != len(segs):
            raise TranslationMismatch(
                f"{name} 有 {len(jsegs)} 段，而 {pairs[0]} 的 NL 分成 {len(segs)} 段")
        zh_map, note_map = {}, {}
        for (sid, txt), js in zip(segs, jsegs):
            if js.get("en") != txt:
                raise TranslationMismatch(
                    f"{name} 段 {js.get('seg')}（对应 {sid}）的 `en` 与原文不逐字节相等：\n"
                    f"  JSON: {js.get('en')!r}\n  语料: {txt!r}")
            zh = (js.get("zh") or "").strip()
            if not zh:
                raise TranslationMismatch(f"{name} 段 {js.get('seg')}（{sid}）译文为空")
            zh_map[sid] = zh
            note_map[sid] = (js.get("note") or "").strip()
        trans[sha8] = zh_map
        notes[sha8] = note_map
        tnotes[sha8] = (j.get("translator_notes") or "").strip()
    return trans, notes, tnotes


#: `{sha8: {seg_id: 中文严格翻译}}` —— ⭐ import 期即完成装载与对拍，
#: ⛔ 材料坏掉就在 import 处炸，不拖到某一份工作单渲染时才发现。
TRANSLATIONS, NOTES, TRANSLATOR_NOTES = _store()


def translate(pair, seg_id):
    """取译文。⛔ 查不到返回 `None`，⛔ 不返回占位符 —— 缺译必须显形。"""
    return _store()[0].get(digest8(pair), {}).get(seg_id)


def note(pair, seg_id):
    """取该段的判读提示。⛔ 查不到或译者未写时返回 `""`。"""
    return _store()[1].get(digest8(pair), {}).get(seg_id, "")


def translator_notes(pair):
    """取整份 NL 层面的观察（术语表、跨句歧义、原文质量）。⛔ 没有时返回 `""`。"""
    return _store()[2].get(digest8(pair), "")


def source_file(pair):
    """该 pair 的译文来自 [translations/](./translations/) 下的哪个文件（只给文件名）。

    ⭐ 工作单里挂这个链接，⛔ 使读者能一步跳到原始 JSON 复核，
    ⛔ 而不是只能看到渲染后的结果。同一份 NL 的 6 个 pair 指向同一个文件。
    """
    sha8 = digest8(pair)
    hit = _raw().get(sha8)
    if not hit:
        raise TranslationMismatch(f"{pair} 的 sha8 {sha8} 没有对应的译文 JSON")
    return hit[0]


def missing(pairs=None):
    """列出缺译文的 `(pair, seg_id)`。⭐ 供测试与 `generate.py --check` 使用。"""
    out = []
    for pair in (pairs if pairs is not None else S.IN_SCOPE_PAIRS):
        segs, _ = S.nl_segments(pair)
        for sid, _txt in segs:
            if not translate(pair, sid):
                out.append((pair, sid))
    return out


def missing_notes(pairs=None):
    """列出缺判读提示的 `(pair, seg_id)`。⚠️ 与 `missing()` 分开报 —— 译文缺是硬伤，
    提示缺只是这一段译者认为无可提示（⛔ 但按 SPEC 每段都该有，故测试仍钉住它为空）。
    """
    out = []
    for pair in (pairs if pairs is not None else S.IN_SCOPE_PAIRS):
        segs, _ = S.nl_segments(pair)
        for sid, _txt in segs:
            if not note(pair, sid):
                out.append((pair, sid))
    return out
