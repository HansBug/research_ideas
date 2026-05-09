"""``expert_review`` 包入口 —— LLM-as-STM-Judge 评审系统的 Python API。

**作用**：

1. 把内部模块（``agent`` / ``schema`` / ``batch`` / ``compatibility``）
   的核心 class 与函数 re-export 到包顶层，让用户只需
   ``from expert_review import ExpertReviewAgent`` 即可使用；
2. 维护 ``__all__`` 显式声明对外稳定 API 列表，未列在其中的模块视作
   内部实现细节（如 ``benchmark`` / ``utils`` / ``agents`` / ``graph``）。

**设计思路**：

* **薄包装层**：本文件只 re-export 而不引入新逻辑；
* **保留 legacy API**：``heuristic_expert_review`` / ``review_model`` /
  ``review_artifacts`` 仍可用，但是 *deprecated* 入口（详见
  :mod:`.compatibility`）；
* **首选入口**：新代码应使用 :class:`agent.ExpertReviewAgent`
  与 :class:`schema.ExpertReviewRequest` /
  :class:`schema.ExpertReviewResult`。

**导入开销提示**：

import 本包会触发 ``compatibility`` → ``agent`` → ``graph.runtime`` 等
传递性 import；首次 import 需加载 ``langchain_openai`` 等较重依赖。
若仅需 dataclass schema，可改为 ``from expert_review.schema import ...``
单独 import 以减少启动延迟。

参考：

* 主讨论 §3 LLM-as-STM-Judge 方法
* :mod:`.agent` / :mod:`.schema` / :mod:`.batch`
"""

from .compatibility import heuristic_expert_review, review_artifacts, review_model
from .agent import ExpertReviewAgent
from .batch import (
    BatchReviewItem,
    BatchReviewRow,
    BatchReviewRun,
    BatchTriagePolicy,
    export_batch_run,
    load_batch_items,
    run_batch_review,
    triage_review_result,
)
from .schema import ExpertReviewRequest, ExpertReviewResult, result_to_flat_row

__all__ = [
    "BatchReviewItem",
    "BatchReviewRow",
    "BatchReviewRun",
    "BatchTriagePolicy",
    "ExpertReviewAgent",
    "ExpertReviewRequest",
    "ExpertReviewResult",
    "export_batch_run",
    "heuristic_expert_review",
    "load_batch_items",
    "review_artifacts",
    "review_model",
    "result_to_flat_row",
    "run_batch_review",
    "triage_review_result",
]
