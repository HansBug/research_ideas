"""``__init__`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.prompts` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from .contract_router import CONTRACT_ROUTER_SYSTEM_PROMPT
from .extraction import ARTIFACT_EXTRACTOR_SYSTEM_PROMPT
from .equivalence import EQUIVALENCE_SYSTEM_PROMPT
from .missing_evidence import MISSING_EVIDENCE_SYSTEM_PROMPT
from .quality_review import QUALITY_REVIEW_SYSTEM_PROMPT
from .review_policy import REVIEW_POLICY_SYSTEM_PROMPT
from .synthesis import FINAL_SYNTHESIS_SYSTEM_PROMPT
from .traceability import TRACEABILITY_SYSTEM_PROMPT

__all__ = [
    "ARTIFACT_EXTRACTOR_SYSTEM_PROMPT",
    "CONTRACT_ROUTER_SYSTEM_PROMPT",
    "EQUIVALENCE_SYSTEM_PROMPT",
    "FINAL_SYNTHESIS_SYSTEM_PROMPT",
    "MISSING_EVIDENCE_SYSTEM_PROMPT",
    "QUALITY_REVIEW_SYSTEM_PROMPT",
    "REVIEW_POLICY_SYSTEM_PROMPT",
    "TRACEABILITY_SYSTEM_PROMPT",
]