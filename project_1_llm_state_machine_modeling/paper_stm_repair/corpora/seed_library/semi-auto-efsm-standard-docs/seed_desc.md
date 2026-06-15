# Semi-Automatic Generation of Extended Finite State Machines from Natural Language Standard Documents

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2015 |
| venue | IEEE DSN-W |
| URL / DOI | https://doi.org/10.1109/DSN-W.2015.17 |
| strict seed 结论 | 🟠 / 标准文档边界 |
| 当前角色 | standard-doc EFSM sentinel / aerospace related work |

## 一句话总结

论文提出半自动方法，从自然语言标准文档生成 EFSM，使用 NLP 工具抽取信息并人工处理表格/图形信息，prototype 输出可供 SMC/Graphviz/DiVinE。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 自然语言 standard documents；案例是 ECSS/PUS space standard。 |
| P2_T0_STM_FAMILY | EFSM；形式上在 T0 family，但领域是标准/协议服务。 |
| P3_GENERATION_RELATION | standard document -> EFSM；半自动 NLP + 人工数据库 + prototype。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；论文给方法和案例图，未给公开数据包或原始输出。 |

## 风险与 caveat

standard/protocol risk；人工数据库步骤显著；作者原生 pair/代码/license/hash 未公开。

## 使用建议

作为 standard-doc sentinel / related work，不计 R2。
