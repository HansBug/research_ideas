# Terminology Policy：命名与禁止用语

## 1. 核心原则

本论文主文不把 `fcstm`、`pyfcstm` 或“新 DSL”作为 paper-level novelty。它们只能作为 implementation / artifact / reproducibility 层面的内部载体出现。

推荐主文使用：**语义增强、可机检、可执行的状态机表示**。

## 2. 推荐用语

| 场景 | 推荐中文 | 推荐英文 |
|---|---|---|
| 状态机制品载体 | 语义增强的状态机表示 | semantically enriched state-machine representation |
| 工具可处理性 | 可机检的状态机制品 | machine-checkable state-machine artifact |
| 行为执行能力 | 可执行状态机表示 | executable state-machine representation |
| 诊断来源 | 确定性诊断 / 轻量形式化或静态检查 | deterministic diagnostics / lightweight formal or static checks |
| 方法任务 | 反馈驱动状态机修正 | feedback-driven state-machine repair/refinement |
| 输出目标 | 相对同一 `STM_0` 更优的候选 `STM_k` | a candidate `STM_k` that is better than the same `STM_0` under registered gates |

## 3. 禁止用语

| 禁止写法 | 原因 | 替代写法 |
|---|---|---|
| “首个 `NL -> STM` 方法” | 已有 direct / near baseline，且导师定调已转向修正任务。 | “研究 `<NL, STM_0> -> STM_k` 的反馈驱动修正”。 |
| “提出新 DSL / fcstm 是核心贡献” | 会把论文带偏成 DSL 设计论文。 | “使用一种可机检、可执行的状态机制品作为实验载体”。 |
| “完整形式化验证 / model checking guarantee” | 当前没有 soundness、性质集和模型检查器闭合证据。 | “轻量形式化 / 静态诊断与场景仿真反馈”。 |
| “自动修正提升质量 / outperform” | 结果尚未运行。 | “评估是否产生相对更优 STM，并报告失败模式”。 |
| “baseline 被排除 / 无需对照” | PR #100 要求保留有限对照和消融。 | “将 baseline 重排为 seed、converter、error source、limited comparison 和 related work”。 |
| “run record 是方法贡献” | run record 属于内部实验审计，不是论文方法主线。 | “必要实验披露和复现材料另行记录”。 |

## 4. `fcstm` / `pyfcstm` 允许出现位置

| 位置 | 是否允许 | 写法 |
|---|---:|---|
| 标题 | 否 | 不出现。 |
| Abstract | 否 | 不出现。 |
| Introduction contribution bullets | 否 | 不出现。 |
| Method 主线 | 原则上否 | 只写可机检、可执行状态机表示。 |
| Implementation / Artifact / Appendix | 是 | 可说明原型实现使用 `pyfcstm` 承载内部状态机制品。 |
| README / run guide | 是 | 作为复现工具名出现，不作为学术 novelty。 |

## 5. 自检建议

实现或写作 PR 中可使用以下 grep 作为粗筛；命中不一定错误，但必须逐条解释上下文：

```bash
git grep -nE "首个|最强|new DSL|fcstm.*贡献|pyfcstm.*贡献|完整形式化验证|outperform|提升质量" -- project_1_llm_state_machine_modeling/paper_v1/better_stm_repair_loop
```

若命中位于 forbidden wording 表、风险登记或旧资产说明中，可保留；若命中位于 thesis、abstract、contribution 或 method 主线，应视为高风险。
