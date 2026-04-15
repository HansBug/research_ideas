# Expert Review 设计文档目录

本目录用于沉淀 `expert_review` agent 的版本化设计文档。

## 文档定位

- [`EXPERT_REVIEW_DESIGN_V0.md`](./EXPERT_REVIEW_DESIGN_V0.md)
  现有系统的基线整合文档。它把仓库中已有的研究说明、当前架构说明、以及 TTool 对齐实验结论收口成一个统一的 `v0` 版本描述。
- [`EXPERT_REVIEW_DESIGN_V1.md`](./EXPERT_REVIEW_DESIGN_V1.md)
  面向下一轮重构的 `v1` 设计稿。该版本明确采用“默认始终有 LLM、LangGraph 编排、真正的 agent 系统、支持多智能体且可上下文隔离、接口保持兼容”的设计方向。

## 推荐阅读顺序

1. 先读 [`EXPERT_REVIEW_DESIGN_V0.md`](./EXPERT_REVIEW_DESIGN_V0.md)，理解当前系统实际做了什么、哪些地方已经验证有效、哪些地方是结构性问题。
2. 再读 [`EXPERT_REVIEW_DESIGN_V1.md`](./EXPERT_REVIEW_DESIGN_V1.md)，理解下一版的目标架构、节点职责、工具层、状态组织和迁移路径。

## 来源文档

`v0` 整合时主要参考了仓库根下已有三份文档：

- [`../../EXPERT_REVIEW_RESEARCH.md`](../../EXPERT_REVIEW_RESEARCH.md)
- [`../../EXPERT_REVIEW_ARCHITECTURE.md`](../../EXPERT_REVIEW_ARCHITECTURE.md)
- [`../../EXPERT_ALIGNMENT_REPORT.md`](../../EXPERT_ALIGNMENT_REPORT.md)
