"""⛔ 泄漏审查的机械部分：两个方向都查。

按伞 PR #179 §4B.7，X1 的泄漏可以往两个方向走，**两个都是学术问题**：

* ⛔ **给对照臂放水** → 高估朴素臂 → 低估我们的优势
* ⛔ **把对照臂做弱** → 低估朴素臂 → 虚高我们的优势，⚠️ **且一旦被审稿人看出来，主臂的数字
  会被连带否掉**

⚠️ **本文件只覆盖可机械判定的那部分**，⛔ 不能替代人工审查——按仓库根 `CLAUDE.md` §3.5.-1，
「文本审查的假阴性没有上界」，同一泄漏可以表现为不含任何标识符的「答案形状」。人工审查的记录
在 [../prompt/README.md](../prompt/README.md) §4。

⭐ **审查范围是全部进入模型的文本**，所以这里查三处，⛔ 不止 prompt 文件：

1. `prompt/naive_v1.txt`（system prompt 模板）
2. `schema.py` 的 `Field(description=...)`——它们进 `model_json_schema()`，因而进 prompt
3. 运行时生成的 schema 重试反馈——⚠️ 静态 grep prompt 常量抓不到它，单独断言

⛔ **注意边界**：这里查的是**模板与说明文本**，⛔ 不是注入后的完整 prompt。注入后的 prompt 里
当然含状态名与事件名（PlantUML 全文就在里面），那不是泄漏——泄漏是**我们**在模板里点名该找
什么。把注入后的文本拿来查禁词会得到一堆假阳性。
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ARM = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
PAPER = Path(__file__).resolve().parents[2]
MAIN_ARM_SRC = PAPER / "pipeline" / "feedback_loop" / "src"

sys.path.insert(0, str(ARM / "src"))

import schema as x1_schema  # noqa: E402
from runner import build_prompts, schema_retry_feedback  # noqa: E402


def _prompt_template() -> str:
    return (ARM / "prompt" / "naive_v1.txt").read_text(encoding="utf-8")


def _schema_descriptions() -> str:
    """schema 里全部会进入生产者上下文的说明文本。"""

    return json.dumps(x1_schema.NaiveReview.model_json_schema(), ensure_ascii=False)


def _predicate_names() -> frozenset[str]:
    """从主臂的**权威真源**取 19 条谓词名。

    ⚠️ 在子进程里取，⛔ 不在本进程 import——否则 `test_isolation.py` 的动态检查会看到主臂
    出现在 `sys.modules` 里。⭐ 用子进程而不是正则抽文本，是为了让禁词表**自动跟随**主臂改动：
    正则会随源码格式漂移而静默失配，而静默失配的禁词表等于没有禁词表。
    """

    program = (
        "import sys\n"
        f"sys.path.insert(0, {str(MAIN_ARM_SRC)!r})\n"
        f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
        "from paper_stm_feedback_loop.discover.predicates import PREDICATE_ORDER\n"
        "print('NAMES=' + ','.join(PREDICATE_ORDER))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, f"could not read predicate names:\n{result.stderr}"
    line = [ln for ln in result.stdout.splitlines() if ln.startswith("NAMES=")][-1]
    names = frozenset(n for n in line.removeprefix("NAMES=").split(",") if n)
    assert len(names) >= 19, f"expected at least 19 predicates, got {len(names)}"
    return names


#: ⛔ 方向一（放水）：这些一出现就是把「该找什么」告诉了对照臂。
LEDGER_PATTERNS = (
    r"EIS-\d{4}-\d{2}",
    r"EXP-\d{4}",
    r"REQ-\d{3}",
    r"expected[ _-]?issue",
    r"ground[ _-]?truth",
    r"ledger",
    r"台账",
    r"台帳",
    r"预期缺陷",
    r"期望缺陷",
)

#: ⛔ 方向一（放水）：检查清单式引导。给了它就等于给了 C-② 的闭合词表的一个弱版本。
CHECKLIST_PATTERNS = (
    r"checklist",
    r"check(?:\s+for)?\s+(?:the\s+)?following",
    r"look\s+for\s+the\s+following",
    r"common\s+(?:defect|error|mistake|issue)\s+types",
    r"for\s+example[,:]\s*(?:a\s+)?missing",
    r"缺陷类型",
    r"检查清单",
)

#: ⛔ 方向二（做弱）：保守措辞会显著压低召回，看起来像合理工程约束，实际是稻草人化。
#: ⚠️ 这一组是本文件最容易被忽略的：它读起来全是「好的工程实践」。
WEAKENING_PATTERNS = (
    r"only\s+report\s+.{0,40}\b(?:confident|certain|sure)\b",
    r"be\s+conservative",
    r"at\s+most\s+\d+\s+issues",
    r"no\s+more\s+than\s+\d+\s+issues",
    r"limit\s+your\s+(?:answer|response|report)\s+to",
    r"do\s+not\s+think\s+step",
    r"be\s+brief",
    r"keep\s+it\s+short",
    r"answer\s+directly\s+without",
    r"skim",
    r"truncat",
)


def _model_facing_texts() -> dict[str, str]:
    """全部会进入模型上下文的文本，逐处命名以便断言失败时指得出是哪一处。"""

    system, user = build_prompts(
        nl="<<NL>>", plantuml="<<PUML>>", content_language="zh-CN"
    )
    return {
        "prompt/naive_v1.txt": _prompt_template(),
        "schema.py descriptions": _schema_descriptions(),
        "runner.build_prompts(system)": system,
        # user prompt 只含标题与注入占位，注入内容本身不受禁词约束（见模块 docstring）。
        "runner.build_prompts(user, minus payload)": user.replace("<<NL>>", "").replace(
            "<<PUML>>", ""
        ),
        "runner.schema_retry_feedback": schema_retry_feedback(
            "1 validation error for NaiveReview\nissues.0.reason\n  Field required"
        ),
    }


def test_no_predicate_vocabulary_leaks() -> None:
    """⛔ 19 条谓词名一个都不许出现——那是 C-② 本身。"""

    names = _predicate_names()
    for where, text in _model_facing_texts().items():
        lowered = text.lower()
        hits = sorted(n for n in names if n.lower() in lowered)
        assert not hits, f"{where} leaks predicate name(s): {hits}"


def test_no_ledger_or_answer_leaks() -> None:
    """⛔ 台账、期望缺陷、需求条目编号体系都不许出现。"""

    for where, text in _model_facing_texts().items():
        for pattern in LEDGER_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            assert match is None, (
                f"{where} matches ledger pattern {pattern!r} at {match.group(0)!r}"
            )


def test_no_checklist_guidance() -> None:
    """⛔ 不给检查清单——对照臂必须自己决定找什么。"""

    for where, text in _model_facing_texts().items():
        for pattern in CHECKLIST_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            assert match is None, (
                f"{where} matches checklist pattern {pattern!r} at {match.group(0)!r}"
            )


def test_no_weakening_instructions() -> None:
    """⛔ 不许有压召回、压推理、压篇幅的措辞——那是把对照臂做弱。"""

    for where, text in _model_facing_texts().items():
        for pattern in WEAKENING_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            assert match is None, (
                f"{where} matches weakening pattern {pattern!r} at {match.group(0)!r}; "
                "see prompt/README.md §4.2 -- a weakened baseline invalidates the main arm."
            )


def test_task_statement_is_explicit() -> None:
    """⭐ 反向断言：任务陈述必须**明确**要求找不符之处。

    ⚠️ 前四条测试都是「不许有 X」。它们全绿的一个平凡解是 prompt 空白——所以必须有一条正向
    断言钉住诚意。按 §4B.2，「任务陈述的诚意」属⛔ 不许省的一栏。
    """

    system, _ = build_prompts(nl="x", plantuml="y", content_language="zh-CN")
    lowered = system.lower()
    assert "does not conform" in lowered or "non-conformance" in lowered, (
        "the task statement must explicitly ask for non-conformances between model and spec"
    )
    assert "specification" in lowered and "state machine" in lowered
    # ⭐ 断言的是**形式要求**（模型有权自行决定报几条），⛔ 不是某句措辞——按仓库根
    # `CLAUDE.md` §13 第 3 条，钉住措辞的测试会把旧形状锁死在原地。
    # ⚠️ 初版写的是 `"as many or as few" in lowered`，那正是钉措辞。
    free_count = any(
        re.search(pattern, lowered)
        for pattern in (
            r"as many or as few",
            r"however many",
            r"any number of",
            r"you decide how many",
        )
    )
    assert free_count, (
        "the task statement must leave the number of reported issues to the model; "
        "no phrasing in the recognised set was found"
    )
    # ⛔ 并且不得同时出现上限（那会抵消这条自由）
    assert not re.search(r"at most \d+|no more than \d+", lowered)


def test_retry_feedback_carries_only_structural_information() -> None:
    """⚠️ 运行时反馈也是 prompt 的一部分，⛔ 且静态 grep prompt 常量抓不到它。

    它只许携带**结构**信息（哪个字段、期望什么形状），⛔ 不许携带任何内容引导。
    """

    feedback = schema_retry_feedback(
        "1 validation error for NaiveReview\nissues.0.reason\n  Field required"
    )
    assert "issues.0.reason" in feedback, "feedback must name the offending field"
    lowered = feedback.lower()
    for banned in ("state", "event", "transition", "guard", "initial", "missing element"):
        assert banned not in lowered, (
            f"retry feedback mentions {banned!r}; it must stay purely structural"
        )
