# experiment_design/ — RQ 与评价门原则

## 1. 职责

`experiment_design/` 在 R0 只冻结研究问题草案、`Better STM` 最小定义和评价门顺序原则。它**不是**最终实验协议，也不创建样本、场景、转换器或真实运行记录。

## 2. 文件职责

| 文件 | 职责 |
|---|---|
| [research_questions.md](./research_questions.md) | RQ 草案、证据需求、依赖 PR 和降级写法。 |
| [better_stm_definition.md](./better_stm_definition.md) | `Better(STM_k, STM_0 | NL, S, D, R)` 的五条件、反例边界和转换归因原则。 |
| [evaluation_gate.md](./evaluation_gate.md) | 评价门必须先于修正预演冻结的原则；说明 R0 不等于 R4 评价门 v0。 |

## 3. 边界

1. R0 不冻结最终 metric threshold。
2. R0 不冻结人工评价量表终稿。
3. R0 不决定主实验样本或四例 `seed_id`。
4. R0 不运行任何真实 LLM 或四例样本。
5. R4/R6 必须继承 R0 的顺序原则，但具体指标和统计表由 R4/R6 冻结。
