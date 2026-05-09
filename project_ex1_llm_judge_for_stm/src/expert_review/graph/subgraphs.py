"""Pipeline 阶段顺序组装。

**作用**：提供 :func:`ordered_stage_groups` 把 3 个 stage 元组按执行顺序
打包，供 :func:`graph.runtime.run_expert_review_workflow` 与 logging
代码统一遍历。

**设计思路**：和 :mod:`graph.edges` 配套——edges 提供 *是什么*，
subgraphs 提供 *按什么顺序执行*；这种 "数据 / 顺序" 解耦让未来引入
DAG-style 调度（不再线性）只需改本文件。
"""

from .edges import ANALYSIS_STAGE, FINAL_STAGE, PREPARATION_STAGE


def ordered_stage_groups() -> list[tuple[str, tuple[str, ...]]]:
    """返回 pipeline 3 个 stage 的有序列表。

    :return: 列表，每个元素是 ``(stage_label, agent_names_tuple)``
        二元组；按 ``preparation`` → ``analysis`` → ``finalization``
        顺序排列
    :rtype: list[tuple[str, tuple[str, ...]]]

    Examples::

        >>> from expert_review.graph.subgraphs import ordered_stage_groups
        >>> groups = ordered_stage_groups()
        >>> [label for label, _ in groups]
        ['preparation', 'analysis', 'finalization']
        >>> 'Contract Router' in groups[0][1]
        True
        >>> 'Disagreement Arbiter' in groups[2][1]  # 已删除
        False
    """
    return [
        ("preparation", PREPARATION_STAGE),
        ("analysis", ANALYSIS_STAGE),
        ("finalization", FINAL_STAGE),
    ]


__all__ = ["ordered_stage_groups"]
