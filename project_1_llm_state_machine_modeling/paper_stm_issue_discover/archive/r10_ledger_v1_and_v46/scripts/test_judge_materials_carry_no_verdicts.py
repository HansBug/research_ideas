"""交给判定者的材料**不得含往轮判定**。

## 为什么这条必须是可执行检查

同一类泄漏漏了**三次**，每次修的都是「这个实例」：

1. v24 发布核验：指令文件**自身的改动日志**逐字写着某命题「应判 `grounded-extra`（A 的判定正确）」，
   而禁读清单列了十来项独独漏了指令文件自身。
2. v25 公平性 review：`docs/protocol/hit_criterion.md` 在**必读白名单**上，且两份指令都承诺它「不含任何分组信息」——
   该承诺为假（§3 的四种形态各配一个真实语料实例，带 `EXP-` 标识符与真实状态名）。
3. 同一次 review：刚入库的 `annotation_*.json`（上一轮**完整答案**）不在禁读清单内。

**按形态列举永远漏**（仓库纪律 §3.5.-1 自己说过）。所以：

- 读取侧改成**白名单**（只允许 `{{SAMPLE_PATH}}` + 一份清洗过的判据文件）
- 内容侧改成**本测试**（机械扫描，不依赖我记得）

## 一个必须保留的区分

`PAIR-Z-*` / `C999-*` 这类**占位 id** 允许出现 —— 它们是输出格式示例。判据是：示例的 id 在样本里
**不存在**。原先示例用的是 `C001-I01` / `PAIR-A-REC-02`，那些是真实 id，示例里的标签会被当成提示。
"""

from __future__ import annotations

import pathlib
import re

import pytest

# ⛔ 归档后脚本与测试同在 `scripts/`，原先的 `…/ "discover_matrix"` 指向不存在的目录。
MATRIX = pathlib.Path(__file__).resolve().parent

#: 交给判定者的材料（白名单本身）。
JUDGE_FACING = ("docs/judges/hit_criterion_for_judges.md",)

#: 指令文件：只有 `## ⛔` 之前的部分交给判定者。
INSTRUCTION_FILES = ("docs/judges/onepass_instructions.md", "docs/judges/blind_judge_prompt.md")

#: 往轮判定的指纹。三类：台账/issue 标识符、pair 编号、裁定动词。
_VERDICT = re.compile(
    r"EIS-\d{4}"                       # 台账记录 id
    r"|EXP-\d{4}"                      # 往轮 expected issue id
    r"|ISSUE-[a-z0-9]"                 # 已发布 issue id
    r"|PAIR-[A-Y]-REC"                 # 真实别名（PAIR-Z 是占位，见 docstring）
    r"|\b(?:0000|0006|0018|0029|0032|0035|0038|0043|0047|0048|0050)\b"   # grid pair 编号
    r"|应判|判定正确|前提为假|一方的事实"     # 裁定动词
)


def _instruction_part(text: str) -> str:
    """指令文件交给判定者的那一段 —— 第一个 `## ⛔` 之前。

    按 `## ⛔` 标题划界而**不按节名**：上一版把边界写成「只读到『### 输出格式』结束」，而「### 注意」
    在它之后，于是一条防猜指令被切出了指令范围。按节名划界会随文件结构变化失效。
    """

    return text.split("## ⛔")[0]


@pytest.mark.parametrize("name", JUDGE_FACING)
def test_judge_facing_material_has_no_verdicts(name: str) -> None:
    path = MATRIX / name
    if not path.is_file():
        pytest.skip(f"no {name}")
    hits = _VERDICT.findall(path.read_text())
    assert not hits, (
        f"{name} 含往轮判定指纹 {sorted(set(hits))}。\n"
        "交给判定者的材料必须只含**原则**与**合成实例**（`Sys.*` 占位名）。\n"
        "真实语料实例留在维护版本 `docs/protocol/hit_criterion.md`，它永不进入判定者的白名单。"
    )


@pytest.mark.parametrize("name", INSTRUCTION_FILES)
def test_instruction_section_has_no_verdicts(name: str) -> None:
    path = MATRIX / name
    if not path.is_file():
        pytest.skip(f"no {name}")
    part = _instruction_part(path.read_text())
    hits = _VERDICT.findall(part)
    assert not hits, (
        f"{name} 的**指令段**（第一个 `## ⛔` 之前）含往轮判定指纹 {sorted(set(hits))}。\n"
        "指令段逐字交给判定者，含具体裁定即预装答案。\n"
        "把这些内容移到 `## ⛔` 分隔之下（那里是维护记录，不交给判定者）。"
    )


@pytest.mark.parametrize("name", INSTRUCTION_FILES)
def test_instruction_file_has_the_boundary_marker(name: str) -> None:
    """没有 `## ⛔` 分隔的指令文件 = 整份文件都交给判定者。

    这条防的是「新建一份指令文件时忘了加分隔」—— 那时上面两条测试会把整份文件当指令段扫，
    但若文件恰好还没写维护记录，它会**通过**，而分隔的缺失不会被发现。
    """

    path = MATRIX / name
    if not path.is_file():
        pytest.skip(f"no {name}")
    assert "## ⛔" in path.read_text(), (
        f"{name} 缺 `## ⛔` 分隔标记。指令文件必须显式划出「交给判定者」与「维护记录」的边界，"
        "否则整份文件都会被逐字交出去。"
    )
