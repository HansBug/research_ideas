# format conversion matrix：输出格式与转换需求矩阵

## 1. 为什么需要本矩阵

第一篇新主线把历史 baseline 重排为 `<NL, STM_0>` seed / converter pressure / limited comparison 资产。不同 prior artifact 的输出格式差异很大，R3 不能承诺通用转换器；只能先根据 R1 确认的格式压力定义最小转换合同。

## 2. 格式压力表

| 格式族 | 代表来源 | 是否接近内部 `STM_0` | 转换难度 | 主要信息损失风险 | R3 建议 |
|---|---|---|---|---|---|
| CSV DFSM / Mealy | `designing-fsm...` | 高 | 低-中 | 层次、并发、动作语义、时间约束缺失 | 可优先做 deterministic adapter。 |
| UML state machine slots / PNG reference | `structure-and-event-driven...` | 中-高 | 中 | 图片 reference 需要人工/视觉解释；guard/action 槽位需结构化。 | 先处理文本描述与 workbook；PNG 只作人工参考。 |
| PlantUML SysML STM | `llms_emp` STM 子集 | 高 | 中 | SysML 行为模型含 ACT/SD，需要过滤；PlantUML 方言差异。 | 优先抽 STM 子集，保留原始 PlantUML。 |
| TTool XML / SysML state machine | `ttool-ai` | 高 | 中-高 | TTool 模型含 block/internal/state 联合信息；工具版本影响解析。 | 先做 sample-level adapter，不承诺全量 TTool import。 |
| Mermaid statechart | `req` | 中 | 中 | 数据私有；Mermaid 表达可能缺 guard/action 正规字段。 | 暂不作为 R3 主压力，除非仅重建论文示例。 |
| Umple state machine code | `umple` | 高 | 中 | Umple 语义、嵌套、action、编译语义需映射。 | 可作为代码式 STM adapter 候选。 |
| protocol FSM / rulebook | FlowFSM / SpecGPT | 中 | 中-高 | 协议领域 event/message 与控制系统 event 语义不同；GT 未公开。 | 暂作 related-work，不进 R3 最小合同。 |
| Event-B / PAT / SAPIC+ / Rebeca / TLA+ / LTL/STL | #73/#82/#92 强近邻 | 低-中 | 高 | 输出是形式规格或过程模型，不是状态机族同构表示。 | 不进最小转换器；只作 feedback / verification related work。 |
| BPMN / POWL / Petri net / activity diagram / Simulink slice | #82/#92 近邻 | 低 | 高 | 流程 / 数据流 / 活动语义与 STM 差异大。 | 只作 converter boundary evidence。 |

## 3. R3 最小建议

R3 优先只覆盖 3--4 类格式：CSV DFSM、PlantUML/SysML STM、TTool XML 或 UML slot workbook、可选 Umple。所有转换必须记录：原始 seed、转换后 `STM_0`、修正后 `STM_k`，并区分转换规范化收益与修正循环收益。
