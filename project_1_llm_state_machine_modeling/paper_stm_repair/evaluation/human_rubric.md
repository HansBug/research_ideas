# Human rubric v0

## 1. 定位

Human rubric v0 是 R4 对后续 R7/R8 人工裁决的草案化定义。它用于检查评价维度是否足以覆盖 NL fidelity、diagnostic closure、regression safety 与 semantic drift，不在 R4 执行正式人工评测。

## 2. 维度

| 维度 | 问题 | 建议评分 |
|---|---|---|
| NL fidelity / requirement coverage | `STM_k` 是否覆盖 `NL` 中关键状态、事件、约束和禁止行为？ | `improved / unchanged / degraded / unknown` |
| Diagnostic closure | 预注册 diagnostics 是否被关闭，是否引入新 blocking issue？ | `closed / partially_closed / not_closed / regressed / unknown` |
| Regression safety | 冻结场景 / 回归是否保持不退化？ | `pass / fail / unknown` |
| Guard/action/state semantics preservation | guard、action、状态层级是否保持需求语义？ | `preserved / changed_with_reason / drifted / unknown` |
| Traceability and auditability | 每项判断是否能追到 NL、STM、scenario、diagnostic 或人工 note？ | `complete / partial / missing` |
| Semantic drift / overfitting risk | 是否为通过测试删除需求行为或过拟合场景？ | `low / medium / high / unknown` |
| Confidence and adjudication notes | 裁决者置信度与冲突说明。 | `high / medium / low` + free text |

## 3. 人在回路边界

人类可参与评价构造、reference / adjudication 与最终审计；repair loop 运行内部不能把人工临时干预写成无人化方法贡献。

## 4. JSON schema

Rubric 结构由 [schemas/human_rubric.schema.json](./schemas/human_rubric.schema.json) 约束。R4 当前只提交 schema 与 Markdown 草案，不提交正式人工评分数据。
