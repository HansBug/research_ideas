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

- `segments[*].note` —— **逐段判读提示**：该段对哪一类元素提出了要求（⛔ 写的是**原文要求了
  什么**，⛔ 不是某一份制品里那个元素长什么样 —— 见下方第 8 条纪律与
  [TRANSLATION_SPEC.md](./translations/TRANSLATION_SPEC.md) 的规格变更表，⚠️ 旧措辞里的
  「模型」二字正是 2026-08-13 那次材料事故的入口）、歧义点在哪、哪部分落在
  $M = (S, E, V, Tr, A)$ 边界之外。⭐ 判「违反」时先读它。
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

⛔⛔ **`note` / `translator_notes` 只能讲原文，一个字都不能讲被测制品。** ⚠️ 一份 NL 服务 6 个
pair，6 份制品各不相同；讲制品的句子会被逐字印进 6 份工作单，⛔ 于是它对其中 5 份必然是**假的**。
2026-08-13 的审计实测：79 条可核验的制品断言里 68 条（86%）在至少一个兄弟 pair 上为假，波及
40 份工作单。⭐ 详见 [README.md](./README.md) §十。本模块用 `artifact_leaks()` 在**装载期**
把词法可判定的那部分钉死，⛔ 语义部分靠
[TRANSLATION_SPEC.md](./translations/TRANSLATION_SPEC.md) 的纪律与人工评审。

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
import re

import sources as S

HERE = os.path.dirname(os.path.abspath(__file__))
TRANS_DIR = os.path.join(HERE, "translations")


class TranslationMismatch(RuntimeError):
    """译文与语料对不上。⛔ 只在装载时抛，⛔ 绝不降级成「跳过这一份」。

    ⭐ 静默跳过的后果是工作单里少了译文列而没人发现；抛出来的后果是 `generate.py`
    当场失败。⛔ 后者才是对的 —— 材料错了就不该产出工作单。
    """


class NoteArtifactLeak(RuntimeError):
    """`note` / `translator_notes` 里出现了对被测制品的指涉。⛔ 装载期即抛。

    ⭐ 与 `TranslationMismatch` 同理：材料错了就不该产出工作单。⛔ 这一条尤其不能降级 ——
    受污染的提示会被印在 6 份工作单上，而它们旁边还立着一句「提示只陈述原文」的免责声明，
    ⛔ 读者据此**不会去核**。
    """


# ⛔ 制品指涉的**词法**判据。按 [CLAUDE.md](../../../../../../CLAUDE.md) §11，
# 只有能被完美判定的约束才允许做成会一票否决的门，故这里放的全是**看字符串就能唯一判定**的东西：
#
# 1. `BANNED_IN_NOTES` —— 固定子串（ASCII 部分不区分大小写）。「模型」「制品」是制品指涉的
#    中文入口词；`plantuml` / `puml` / `fcstm` 是制品的文件与记法名（审计实测 `nl_0002` 的
#    观察里直接写出过文件名 `plantuml.puml`）；「生成侧」「参考侧」「作者源」是工作单里
#    制品两侧的固定称呼。⭐ 谈 UML 语义仍然可以 —— `UML` 不在表内。
# 2. `artifact_leaks()` 的标识符检查 —— 提示里出现的驼峰 / 下划线标识符，
#    必须在**同一份 JSON 自己的 `en`** 里逐字出现过。⭐ 这是同一文档内两个字段之间的
#    确定性一致性检查，⛔ 不需要任何语义解释。
#
# ⚠️ 两道判据都**只作用于 `note` 与 `translator_notes`**，⛔ 不碰 `zh`：译文必须逐字跟着原文走，
# 原文若真写了 `PlantUML` 或「模型」，译文照译。
BANNED_IN_NOTES = ("模型", "制品", "生成侧", "参考侧", "作者源",
                   "plantuml", "puml", "fcstm")

_IDENT = re.compile(r"[A-Za-z0-9_]+")
_SNAKE = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+$")
_CAMEL = re.compile(r"^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+$")


def artifact_leaks(payload):
    """列出一份译文 JSON 里所有**词法可判定**的制品指涉，⛔ 干净时返回空表。

    ⭐ 判据只有两条，都只看字符串，⛔ 不做任何语义解释（[CLAUDE.md] §11）：

    1. 命中 `BANNED_IN_NOTES` 里的固定子串；
    2. 提示里的驼峰 / 下划线标识符没有在本份 NL 的 `en` 里出现过 ——
       ⭐ 那说明它只可能来自某一份制品。⚠️ 反过来，`dist_to_front` / `DoorOpenWithItem`
       这类原文自己点名的标识符**必须**放行，⛔ 否则译文没法讲原文点了什么。

    ⛔ 只判「有没有」，⛔ 不判「这句话对不对」—— 后者是评审的事，见
    [TRANSLATION_SPEC.md](./translations/TRANSLATION_SPEC.md) 的第 8 条硬纪律。
    """
    segs = payload.get("segments") or []
    en = " ".join(s.get("en") or "" for s in segs)
    fields = [("translator_notes", payload.get("translator_notes") or "")]
    fields += [(f"segments[{s.get('seg')}].note", s.get("note") or "") for s in segs]

    out = []
    for where, text in fields:
        low = text.lower()
        for bad in BANNED_IN_NOTES:
            if bad.lower() in low:
                i = low.index(bad.lower())
                out.append(f"{where} 命中禁用词 `{bad}`：…{text[max(0, i - 30):i + 30]}…")
        seen = set()
        for tok in _IDENT.findall(text):
            if tok in seen or tok in en:
                continue
            if _SNAKE.match(tok) or _CAMEL.match(tok):
                seen.add(tok)
                out.append(f"{where} 出现标识符 `{tok}`，⛔ 但本份 NL 原文里没有它")
    return out


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

    ⭐ 四道对拍，⛔ 任何一道不过就抛：

    1. **孤儿文件** —— JSON 的 sha8 对不上任何在评 pair。⚠️ 这通常意味着 `nl.txt` 改了字节
       而译文没跟上，⛔ 此时若静默忽略，工作单会整份缺译。
    2. **段数不等** —— 分段口径变了（例如 `overrides.json` 改了切点）。
    3. **`en` 与原文不等** —— 译文对着另一版原文写的。⭐ 逐段逐字节比，⛔ 不比整篇哈希：
       整篇相等而段边界错位，逐段比才抓得住。
    4. **提示里指涉了制品** —— 见 `artifact_leaks()`。⚠️ 前三道管「译文对不对得上原文」，
       第四道管「提示有没有越界去讲原文之外的东西」，⛔ 两件事都会让工作单带错误事实。
    """
    by_sha8 = _pairs_by_sha8()
    trans, notes, tnotes = {}, {}, {}
    for sha8, (name, j) in _raw().items():
        pairs = by_sha8.get(sha8)
        if not pairs:
            raise TranslationMismatch(
                f"{name} 的 sha8 {sha8} 对不上任何在评 pair —— "
                f"要么 nl.txt 变了字节，要么这份译文本就不该在这里")
        leaks = artifact_leaks(j)
        if leaks:
            raise NoteArtifactLeak(
                f"{name} 的判读提示里指涉了被测制品（共 {len(leaks)} 处）—— "
                f"⛔ 一份 NL 服务 6 个 pair，制品各不相同，讲制品必然误导另外 5 份"
                f"（见 README §十）：\n  " + "\n  ".join(leaks))
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
