# Statechart-Based Use Case Requirement Validation of Event-Driven Systems

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2012 |
| venue | ACM SAC |
| URL / DOI | https://doi.org/10.1145/2245276.2231947 |
| strict seed 结论 | 🟡 / 条件 strict |
| 当前角色 | validation-oriented use case -> statechart evidence |

## 一句话总结

论文把每个 use case 映射为 UML Statechart，再组合 statecharts 做需求验证；核心是 validation，但确实包含 use case requirements -> Statechart 的建模规则。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 结构化 use case 模板，含 pre/postconditions、events、main flow 等。 |
| P2_T0_STM_FAMILY | UML Statechart；T0 基本符合。 |
| P3_GENERATION_RELATION | use case 文档 -> 单 use case Statechart -> combined Statechart；生成关系存在但偏验证流程。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；case study 为 RealState game，链接 http://openseminar.org/se/ 可访问；未发现作者原生机读 pair 或代码。 |

## 风险与 caveat

偏 validation，不是一般生成 benchmark；作者原生 pair/代码/license/hash 未公开。

## 使用建议

作为 paper-only strict/conditional evidence，不计 R2。
