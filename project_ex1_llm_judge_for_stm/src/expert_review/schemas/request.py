""":class:`ExpertReviewRequest` 的 schemas 子包别名。

仅 re-export 顶层 :class:`expert_review.schema.ExpertReviewRequest` —— 与
``schemas/result.py`` 配对，给图运行时与下游代码提供一个 "全部对外
schema 都从 schemas/ 取" 的统一入口风格。

**为什么不直接定义在这里**：避免双源真理；定义点保留在顶层
``schema.py``，本文件只是引用。
"""

from ..schema import ExpertReviewRequest

__all__ = ["ExpertReviewRequest"]
