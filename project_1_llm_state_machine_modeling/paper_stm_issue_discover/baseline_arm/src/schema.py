"""朴素基线对照臂的输出契约：**最小可切分**，⛔ 不携带任何 contribution 能力。

⭐ 设计判据只有一条（伞 PR #179 §4B.3）：判定 hit 需要「一条一条」，所以输出必须能切分成
离散 issue；⛔ 但一旦给出我们的字段（谓词名、绑定、证据族），就把 C-② / C-③ 白送了。

所以这里只有自由文本字段，⛔ 没有枚举、没有字段约束、没有任何谓词措辞。

⚠️ **`Field(description=...)` 也是 prompt 的一部分**——它进 `model_json_schema()`，因而进入
生产者上下文。所以这些 description 与 `prompt/naive_v1.txt` 同受泄漏审查（见
`prompt/README.md` §4），措辞必须保持中性：⛔ 不举例、⛔ 不暗示该找哪一类问题。

⛔ **本模块不加任何 validator。** 按仓库根 `CLAUDE.md` §11「schema validator 的准入边界」，
只有能被完美判定的约束才允许进 validator。这里三个字段的「非空」虽然可完美判定，但它带来的
收益（挡住空串）小于风险：某条发现的 `where` 确实可能难以定位到具体片段（例如「整个模型缺少
终态」），一道非空门会把这个合法边界情况逼成解析失败并触发重试，白烧预算。空串在人工判定时
一眼可见，⛔ 不需要门。

⭐ `issues` 允许为空列表：**「这份模型符合需求」是一个合法答案**，不是失败。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class NaiveIssue(BaseModel):
    """基线报出的一条不符之处。三个字段全是自由文本。"""

    issue: str = Field(description="What the non-conformance is.")
    where: str = Field(description="Which part of the model this concerns.")
    reason: str = Field(description="Why you consider this a non-conformance.")


class NaiveReview(BaseModel):
    """一次基线评审的完整产出。

    ⭐ 两个字段的目的不同，⛔ 不要合并：

    * ``analysis`` 是**推理空间的对等**。主臂是八阶段循环、每阶段有 rationale，推理有大量
      落脚点；X1 是单次调用，若必须直接填列表，跨 issue 的全局比对就没有落脚点，那会在
      §4B.2 的「⛔ 不许禁止它逐步思考」一栏上形成不对等。它是**可选**的。
    * ``issues[].reason`` 是**实验可分析性**。主臂做了五类多报分类；要对基线的多报做同口径
      分类并并排，判定者必须知道它为什么认为那是问题。它是**必填**的。
      ⛔ 它不是 C-③：我们问「为什么」，⛔ 不问「依据需求的哪一条」；归因仍然全部由人工完成。
    """

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
