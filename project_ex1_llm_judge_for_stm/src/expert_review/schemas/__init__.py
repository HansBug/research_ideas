"""``schemas`` 子包入口 —— pipeline 内部状态的 dataclass 集合。

本子包与顶层 :mod:`expert_review.schema` 是 **职责分工** 而不是
"重复定义"：

* 顶层 :mod:`expert_review.schema`：对外稳定的 I/O 契约
  （:class:`ExpertReviewRequest` / :class:`ExpertReviewResult` /
  其评审结果嵌套字段），下游用户直接 import 这些；
* 本子包 :mod:`expert_review.schemas`：pipeline **内部** 各 stage
  之间传递的中间状态（dossier / regime / contract / graph state），
  上游用户一般不直接 import。

**作用**：

1. 集中存放 pipeline 中间产物 dataclass：
   :class:`schemas.dossiers.ReviewContract` /
   :class:`schemas.dossiers.EvidenceRegime` /
   :class:`schemas.dossiers.ArtifactDossier` /
   :class:`schemas.dossiers.InputDossier` 等；
2. 集中存放 graph runtime 共享的状态容器
   :class:`schemas.graph_state.ReviewGraphState`；
3. 通过 ``schemas/request.py`` / ``schemas/result.py`` 把对外的
   :class:`ExpertReviewRequest` / :class:`ExpertReviewResult` 也
   re-export 到本包，作为兼容入口。

**设计思路**：

* **避免循环 import**：``schemas/`` 内的 dataclass 仅依赖顶层
  :mod:`expert_review.schema` 的轻量类型（``EvidenceItem`` /
  ``RequirementTraceResult``），不反向依赖 agents / graph；
* **dataclass + slots**：所有 dataclass 都启用 slots 减少内存。
"""

from .dossiers import (
    ArtifactDossier,
    ArtifactElement,
    ArtifactRelation,
    EvidenceRegime,
    InputDossier,
    ReviewContract,
)
from .graph_state import ReviewGraphState
from .request import ExpertReviewRequest
from .result import ExpertReviewResult

__all__ = [
    "ArtifactDossier",
    "ArtifactElement",
    "ArtifactRelation",
    "EvidenceRegime",
    "ExpertReviewRequest",
    "ExpertReviewResult",
    "InputDossier",
    "ReviewContract",
    "ReviewGraphState",
]
