# Modeling Dependable Product-Families: From Use Cases to State Machine Models

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2016 |
| venue | LADC |
| URL / DOI | https://doi.org/10.1109/LADC.2016.28 |
| strict seed 结论 | 🟡 / 条件 strict |
| 当前角色 | product-family seed 方法 / variability 边界 |

## 一句话总结

论文扩展 MARITACA 思路，从受限格式 use cases 自动抽取 product-specific state machine / EFSM，并处理 product-family variability 和 exceptions。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 受限格式 use cases，含 variability、exception handling 和 traceability matrix。 |
| P2_T0_STM_FAMILY | product-specific state machine / EFSM；T0 需切掉 product-line variability 后判断。 |
| P3_GENERATION_RELATION | use case descriptions -> state machine model；生成关系清楚但有 product-family variability。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；无公开代码、完整数据包或机器可读 pair。 |

## 风险与 caveat

variability 和 product family 特性可能超出当前四例 T0；原生 pair / 版本 / hash 未公开。

## 使用建议

作为条件 strict seed / related work；不计 R2。
