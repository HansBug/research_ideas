# Unified Use Case Statecharts: Case Studies

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2007 |
| venue | Requirements Engineering |
| URL / DOI | https://doi.org/10.1007/s00766-007-0053-1 |
| strict seed 结论 | `SS-B` |
| artifact 可用性 | `SA-3` |
| 当前角色 | classic paper-only / manual unified UC statechart seed |

## 一句话总结

研究如何把多个 use cases 统一为 CBS domain behavior 的 unified use case statechart，论文强调可从 UCs 直接构造 unified UC statechart，但主要是人工/方法论 case studies。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 输入为 use cases 描述 CBS 行为。 |
| P2_T0_STM_FAMILY | 输出为 unified UC statechart / UML statechart-like behavioral domain model。 |
| P3_GENERATION_RELATION | UCUM 方法：unifying use cases into a unified UC statechart；有些学生跳过单个 UC statechart 直接从 UCs 到 unified UC statechart。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；case studies 与 diagrams；无机器可读模型或工具 artifact。 |

## 风险与 caveat

人工构造方法，非自动化生成；可作 related/manual reconstruction，不计 SA-1/2。

## R1.7 使用建议

- 若为 `SS-A/SS-B + SA-3`：可作为 strict seed 文献证据、manual reconstruction 线索或 related work，但不得计入 R1.7 主 / 条件主 seed 成功门。
- 若为 `NN-D`：保留为边界负例，防止把 testbench / GN-driven / co-exist-only 工作误收为 strict seed。
