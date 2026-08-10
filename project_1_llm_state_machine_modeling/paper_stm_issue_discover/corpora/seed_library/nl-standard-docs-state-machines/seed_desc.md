# From Natural Language Standard Documents to State Machines: Advantages and Drawbacks

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2018 |
| venue | Journal of Aerospace Information Systems |
| URL / DOI | https://doi.org/10.2514/1.I010525 |
| strict seed 结论 | 🟠 / 标准文档边界 |
| 当前角色 | standard-doc EFSM/FSM sentinel / aerospace related work |

## 一句话总结

扩展 2015 TXT2SMM 工作，把 PUS 标准需求半自动转成 EFSM，并与文献中人工 FSM 模型比较；关注标准文档、variability 和 space mission 服务。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | ECSS Packet Utilization Standard 需求文本。 |
| P2_T0_STM_FAMILY | EFSM / FSM；形式符合 T0 family，但属于标准服务/协议式行为。 |
| P3_GENERATION_RELATION | standard document -> semi-automatically generated EFSM；含人工检查/选择步骤。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；引用的手工模型在文献中，PUS 标准和工具入口可追踪；未发现可直接下载的 TXT2SMM 数据包/输出包。 |

## 风险与 caveat

standard/protocol/space service 边界；原生 pair、代码、license、hash 未公开。

## 使用建议

作为 standard-doc sentinel / method related work，不计 R2。
