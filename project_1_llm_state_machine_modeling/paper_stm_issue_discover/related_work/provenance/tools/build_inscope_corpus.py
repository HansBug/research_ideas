"""按边界门筛出 `sources/` 的界内条目，并抽出每条的「原文摘录」节。

界内判据三条全合取（伞 PR #179 §4.0.2 + `CONTINGENCY_L2.md` §1.4）：

1. `状态机类型 ∈ {FSM, EFSM, HSM}` —— 排除 Protocol / Resource-flow / Hybrid
2. `时间级别 = T0` —— T1 及以上带显式时钟，落在 $M = (S, E, V, Tr, A)$ 之外
3. `结构标签` 不含「并行」—— 正交区并发在建模对象之外

抽取的只有 `### 1. 原文摘录` 节。这不是省事：`### 2. 基于原文整理后的自然语言描述`
是我们自己写的英文转述，拿它当外部依据等于自证（`CONTINGENCY_L2.md` §1.4 的反面样例
就死在这一步）。`### 0.` 是判定、`### 3.` 是溯源，同样是我们写的。

⛔ 筛法是**准入门**，不是任何比例的分母。见
`discover_matrix/docs/protocol/method_provenance_policy.md` §一.5：`sources/` 的收录标准
恰好选中了要测的那个性质，比例在因变量上做选择，不成立。

用法：

    python -m related_work.provenance.tools.build_inscope_corpus --out-dir /tmp/l2/corpus
    python build_inscope_corpus.py --shards 12 --out-dir /tmp/l2/corpus
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

def _find_sources() -> Path:
    """向上搜 `sources/SUMMARY.md` 锚点，⛔ 不数 `parents[N]` 层级。

    按仓库根 `CLAUDE.md` §9.5 第 3 条：目录深度锚点在搬迁后会**静默**解析到错误目录，
    评测类代码尤其危险——空输入会被读成「没有命中」而不是「路径错了」。
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "sources" / "SUMMARY.md"
        if candidate.is_file():
            return candidate.parent
    raise RuntimeError("向上未找到 sources/SUMMARY.md；请用 --sources 显式指定")

IN_SCOPE_TYPES = frozenset({"FSM", "EFSM", "HSM"})
IN_SCOPE_TIME = "T0"
OUT_OF_SCOPE_STRUCT = "并行"

#: SUMMARY 案例清单的数据行：`| 序号 | 文件号 | 领域 | 条目标题 | 控制对象 | ...`
_ROW = re.compile(r"^\|\s*\d+\s*\|\s*\d+\s*\|")
#: 条目标题行：`## 条目 3: Pump manual/autocontrol modes`
_ENTRY_HEAD = re.compile(r"^## 条目\s*\d+\s*[:：]\s*(.+?)\s*$")
#: 摘录节标题
_EXCERPT_HEAD = re.compile(r"^### 1\.\s*原文摘录\s*$")
_ANY_H3 = re.compile(r"^### ")
_ANY_H2 = re.compile(r"^## ")


@dataclass
class Case:
    """一条界内案例：`sources/` 的一个条目，不是一篇论文。"""

    directory: str
    domain: str
    stm_type: str
    entry_title: str
    controlled_object: str
    excerpt: str = ""
    #: 未能在 STM.md 里定位到条目标题时记原因，交付时必须如实报告
    defect: str = ""

    def to_json(self) -> dict[str, object]:
        return {
            "directory": self.directory,
            "domain": self.domain,
            "stm_type": self.stm_type,
            "entry_title": self.entry_title,
            "controlled_object": self.controlled_object,
            "excerpt_chars": len(self.excerpt),
            "defect": self.defect,
        }


@dataclass
class Corpus:
    cases: list[Case] = field(default_factory=list)
    total_rows: int = 0

    @property
    def in_scope(self) -> int:
        return len(self.cases)

    @property
    def unique_papers(self) -> int:
        return len({c.directory for c in self.cases})


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.split("|")]


def _strip_code(text: str) -> str:
    return text.replace("`", "").strip()


def _link_dir(cell: str) -> str | None:
    m = re.search(r"\(\./([^)]*)/STM\.md\)", cell)
    return m.group(1) if m else None


def collect_in_scope(summary: Path) -> Corpus:
    """从 `sources/SUMMARY.md` 的案例清单里取界内条目。"""
    corpus = Corpus()
    for line in summary.read_text(encoding="utf-8").splitlines():
        if not _ROW.match(line):
            continue
        cells = _cells(line)
        if len(cells) < 14:
            continue
        corpus.total_rows += 1
        domain, title, obj = cells[3], cells[4], cells[5]
        stm_type = _strip_code(cells[6])
        time_level = _strip_code(cells[7])
        struct = cells[8]
        if stm_type not in IN_SCOPE_TYPES:
            continue
        if time_level != IN_SCOPE_TIME:
            continue
        if OUT_OF_SCOPE_STRUCT in struct:
            continue
        directory = _link_dir(cells[12])
        if directory is None:
            continue
        corpus.cases.append(
            Case(
                directory=directory,
                domain=domain,
                stm_type=stm_type,
                entry_title=title,
                controlled_object=obj,
            )
        )
    return corpus


def _normalize_title(text: str) -> str:
    """标题归一：SUMMARY 用 Title Case、STM.md 用 sentence case，两边大小写不一致。

    只做大小写与非字母数字字符的归一，⛔ 不做同义词或截断匹配——那会把两个不同条目
    错配到一起，而错配的后果是引文锚点指向另一个案例。
    """
    return re.sub(r"[^0-9a-z一-鿿]+", "", text.lower())


def extract_excerpt(stm_md: Path, entry_title: str) -> tuple[str, str]:
    """取指定条目的 `### 1. 原文摘录` 节全文。返回 (正文, 缺陷说明)。"""
    if not stm_md.is_file():
        return "", f"STM.md 不存在：{stm_md}"
    lines = stm_md.read_text(encoding="utf-8").splitlines()

    heads = [(i, m.group(1)) for i, line in enumerate(lines) if (m := _ENTRY_HEAD.match(line))]
    start = next((i for i, t in heads if t == entry_title), None)
    if start is None:
        want = _normalize_title(entry_title)
        hits = [i for i, t in heads if _normalize_title(t) == want]
        if len(hits) == 1:
            start = hits[0]
    if start is None and len(heads) == 1:
        # SUMMARY 与 STM.md 的条目标题偶有措辞漂移。文件只有一个条目时不存在歧义，
        # ⛔ 但两个及以上时一律判失败——错配的后果是引文锚点指向另一个案例。
        start = heads[0][0]
    if start is None:
        return "", f"未定位到条目标题：{entry_title!r}（该文件的条目：{[t for _, t in heads]}）"

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if _ANY_H2.match(lines[i]):
            end = i
            break

    ex_start = None
    for i in range(start + 1, end):
        if _EXCERPT_HEAD.match(lines[i]):
            ex_start = i + 1
            break
    if ex_start is None:
        return "", "该条目没有「### 1. 原文摘录」节"

    ex_end = end
    for i in range(ex_start, end):
        if _ANY_H3.match(lines[i]):
            ex_end = i
            break

    body = "\n".join(lines[ex_start:ex_end]).strip()
    if not body:
        return "", "「### 1. 原文摘录」节为空"
    return body, ""


def render_shard(cases: list[Case], index: int, total: int) -> str:
    parts = [
        f"# 界内案例语料 · 分片 {index}/{total}（{len(cases)} 条）",
        "",
        "> 本分片每条给出：目录 slug · 领域 · 状态机类型 · 条目标题 · 控制对象 · **原文摘录节全文**。",
        "> ⛔ 摘录节之外的内容（判定、英文转述、逐句溯源）**未收进本文件**，因为它们是我们自己写的。",
        "",
    ]
    for case in cases:
        parts.extend(
            [
                "---",
                "",
                f"## `{case.directory}` · {case.domain} · {case.stm_type}",
                "",
                f"- **条目标题**：{case.entry_title}",
                f"- **控制对象**：{case.controlled_object}",
                f"- **引用锚点**：`sources/{case.directory}/STM.md` → 条目「{case.entry_title}」→ `### 1. 原文摘录`",
                "",
                case.excerpt if case.excerpt else f"⛔ **抽取失败**：{case.defect}",
                "",
            ]
        )
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--shards", type=int, default=12)
    args = parser.parse_args(argv)

    sources = args.sources if args.sources is not None else _find_sources()
    summary = sources / "SUMMARY.md"
    if not summary.is_file():
        print(f"找不到 {summary}", file=sys.stderr)
        return 2

    corpus = collect_in_scope(summary)
    for case in corpus.cases:
        case.excerpt, case.defect = extract_excerpt(
            sources / case.directory / "STM.md", case.entry_title
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)

    # 按领域轮转分片，让每一路都看到多个领域 —— 领域多样性是 ① 类证据的质量维度，
    # 分片若按领域聚块，单路 agent 就无法自行判断某条义务是否跨领域出现。
    by_domain: dict[str, list[Case]] = {}
    for case in corpus.cases:
        by_domain.setdefault(case.domain, []).append(case)
    domain_counts = {d: len(v) for d, v in sorted(by_domain.items())}
    interleaved: list[Case] = []
    pools = [list(v) for v in by_domain.values()]
    while any(pools):
        for pool in pools:
            if pool:
                interleaved.append(pool.pop(0))

    shards: list[list[Case]] = [[] for _ in range(args.shards)]
    for i, case in enumerate(interleaved):
        shards[i % args.shards].append(case)

    for i, shard in enumerate(shards, start=1):
        if not shard:
            continue
        path = args.out_dir / f"shard_{i:02d}.md"
        path.write_text(render_shard(shard, i, args.shards), encoding="utf-8")

    manifest = {
        "total_rows": corpus.total_rows,
        "in_scope_cases": corpus.in_scope,
        "unique_papers": corpus.unique_papers,
        "shards": args.shards,
        "defects": [c.to_json() for c in corpus.cases if c.defect],
        "domains": domain_counts,
    }
    (args.out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"案例总数={corpus.total_rows} 界内={corpus.in_scope} 唯一论文={corpus.unique_papers}")
    print(f"抽取失败={len(manifest['defects'])} 分片={args.shards} → {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
