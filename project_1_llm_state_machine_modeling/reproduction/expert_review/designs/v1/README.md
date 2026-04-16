# Expert Review V1

本目录保存 `expert_review` 下一轮重构设计资料。

## 当前文档

- [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)

## 作用

`v1` 不是当前代码说明，而是下一轮重构蓝图。

当前设计重点包括：

1. 默认始终有 LLM
2. 使用 LangGraph 编排
3. 引入真正的多智能体系统
4. 主智能体调度、子智能体上下文可隔离
5. 保持当前外部接口兼容

## 阅读顺序

1. 先读 [GUIDE.md](./GUIDE.md)
2. 再读 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
