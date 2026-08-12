"""朴素基线对照臂的输出契约：**最小可切分**，⛔ 不携带任何 contribution 能力。

⭐ 设计判据只有一条（伞 PR #179 §4B.3）：判定 hit 需要「一条一条」，所以输出必须能切分成
离散 issue；⛔ 但一旦给出我们的字段（谓词名、绑定、证据族），就把 C-② / C-③ 白送了。

所以这里只有自由文本字段，⛔ 没有枚举、没有字段约束、没有任何谓词措辞。

⚠️⚠️ **进入 prompt 的有两样，⛔ 不是一样**：

1. `Field(description=...)` —— 它进 `model_json_schema()` 的**字段** `description`。
2. ⛔⛔ **类 docstring** —— pydantic 把 `cls.__doc__` 放进 `model_json_schema()` 的**顶层
   `description`**。⛔ 本文件初版漏了这一条，于是两个类 docstring（含「基线」「主臂」
   「八阶段循环」「X1 是单次调用」「五类多报分类」「C-③」）**随 schema 进了生产者上下文**，
   即**告诉了模型它是一个对照实验里的基线臂**。

⭐ 所以类级说明一律写成 `#` 注释（⛔ 注释不进 `__doc__`），⛔ 不写成 docstring。两者同受泄漏
审查（见 `prompt/README.md` §4），措辞必须中性：⛔ 不举例、⛔ 不暗示该找哪一类问题、
⛔ 不提及另一臂或实验设计。

⚠️ 回归测试 `tests/test_prompt_no_leakage.py` 必须同时扫**字段 description 与顶层
description**，且模式表必须含臂身份词——初版只扫了前者、模式表里也没有臂身份词，
所以它**放过了这次泄漏**。

⛔ **本模块不加任何 validator。** 按仓库根 `CLAUDE.md` §11「schema validator 的准入边界」，
只有能被完美判定的约束才允许进 validator。这里三个字段的「非空」虽然可完美判定，但它带来的
收益（挡住空串）小于风险：某条发现的 `where` 确实可能难以定位到具体片段（例如「整个模型缺少
终态」），一道非空门会把这个合法边界情况逼成解析失败并触发重试，白烧预算。空串在人工判定时
一眼可见，⛔ 不需要门。

⭐ `issues` 允许为空列表：**「这份模型符合需求」是一个合法答案**，不是失败。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# 一条不符之处。三个字段全是自由文本。
# ⛔ 不要写成 docstring：它会进 model_json_schema() 的顶层 description。
class NaiveIssue(BaseModel):
    issue: str = Field(description="What the non-conformance is.")
    where: str = Field(description="Which part of the model this concerns.")
    reason: str = Field(description="Why you consider this a non-conformance.")


# 一次评审的完整产出。
# ⛔⛔ 不要写成 docstring —— 它会随 model_json_schema() 进入生产者上下文，
#     而下面这段提及了另一臂与实验设计，属臂身份泄漏。
#
# 两个字段的目的不同，⛔ 不要合并：
#
# * analysis 是推理空间的对等。主臂是八阶段循环、每阶段有 rationale，推理有大量落脚点；
#   X1 是单次调用，若必须直接填列表，跨 issue 的全局比对就没有落脚点，那会在伞 PR
#   §4B.2 的「不许禁止它逐步思考」一栏上形成不对等。它是可选的。
# * issues[].reason 是实验可分析性。主臂做了五类多报分类；要对基线的多报做同口径分类
#   并并排，判定者必须知道它为什么认为那是问题。它是必填的。
#   它不是 C-③：我们问「为什么」，不问「依据需求的哪一条」；归因仍全部由人工完成。
class NaiveReview(BaseModel):
    analysis: str | None = Field(
        default=None,
        description="Optional: your overall analysis after reading both inputs.",
    )
    issues: list[NaiveIssue] = Field(
        default_factory=list,
        description=(
            "The non-conformances you found. Report as many or as few as you "
            "actually find; an empty list is a valid answer."
        ),
    )
