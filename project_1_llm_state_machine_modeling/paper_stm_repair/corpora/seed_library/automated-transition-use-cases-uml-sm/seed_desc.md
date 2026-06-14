# Automated Transition from Use Cases to UML State Machines to Support State-Based Testing

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2011 |
| venue | ECMFA 2011 / LNCS 6698 |
| URL / DOI | https://doi.org/10.1007/978-3-642-21470-7_9 |
| 种子结论 | 🟡 / 条件种子 |
| 当前角色 | use-case -> UML state machine seed evidence |

## 一句话总结

论文基于 RUCM / aToucan，把文本 use case specifications 自动转成 UML state machines，并建立 traceability；属于明确的 NL-to-STM-family 种子证据，但原生 pair / 代码 / 许可仍未冻结。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | RUCM textual use case specifications；输入是受限自然语言 use case。 |
| P2_T0_STM_FAMILY | UML State Machine；T0 基本符合。 |
| P3_GENERATION_RELATION | aToucan 从 UCMeta 到 UML state machine 自动转换，且建立 traceability。 |
| P4_EVIDENCE_POINTER | 本地已下载正文全文；aToucan / RUCM 作为上游链路可定位；未发现原生机读 pair 与代码冻结包。 |

## 风险与 caveat

原生 pair、代码、许可、hash 未公开；RUCM 需要受限模板，属于条件种子。

## 使用建议

作为条件种子 / 方法证据进入 seed 方法集合；**不计当前 R2 四例**。只有后续冻结作者原生 pair，或完成可审计的 Appendix 局部重建并明确许可 / 版本 / 哈希后，才可重新裁决是否进入 R2 候选池。
