# Expert Review V1

本目录保存 `expert_review` 下一轮重构设计资料。

## 当前文档

- [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
- [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md)
- [TODO.md](./TODO.md)
- [V1_ALIGNMENT_REPORT.md](./V1_ALIGNMENT_REPORT.md)

## 作用

`v1` 不是当前代码说明，而是下一轮重构蓝图。

当前设计重点包括：

1. 默认始终有 LLM
2. 使用 LangGraph 编排
3. 引入真正的多智能体系统
4. 主智能体调度、子智能体上下文可隔离
5. 保持当前外部接口兼容
6. reviewer 运行时自包含，但允许离线用真实人工评审 benchmark 做自我迭代

## 阅读顺序

1. 先读 [GUIDE.md](./GUIDE.md)
2. 再读 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
3. 再读 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md)
4. 再读 [TODO.md](./TODO.md)
5. 最后读 [V1_ALIGNMENT_REPORT.md](./V1_ALIGNMENT_REPORT.md)
