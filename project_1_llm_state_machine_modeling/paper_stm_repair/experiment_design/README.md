# experiment_design/ — R0 评价约束草案

## 1. 职责

`experiment_design/` 在 R0 中只冻结评价设计的上游约束：研究问题草案、`Better STM` 最小定义、评价门顺序和后续 R4/R6 继承规则。它不替代 R4 的诊断 / 场景 / 评价量表 v0，也不替代 R6 的最终主实验协议。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [research_questions.md](./research_questions.md) | 给出 RQ 草案、证据类型、依赖 PR 和降级写法。 |
| [better_stm_definition.md](./better_stm_definition.md) | 定义 `Better(STM_k, STM_0 | NL, S, D, R)` 的最小必要条件和反例边界。 |
| [evaluation_gate.md](./evaluation_gate.md) | 冻结“评价门先于真实修正预演”的顺序规则。 |

## 3. R0 边界

- 不冻结具体指标阈值。
- 不定义完整评分表。
- 不选择四例样本。
- 不跑真实 LLM 或仿真。
- 不把 R0 草案写成主实验结论。
