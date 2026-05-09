"""``__init__`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.compatibility` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from .legacy_api import heuristic_expert_review, review_artifacts, review_model

__all__ = ["heuristic_expert_review", "review_artifacts", "review_model"]