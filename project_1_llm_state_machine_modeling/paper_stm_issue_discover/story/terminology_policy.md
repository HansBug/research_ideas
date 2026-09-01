# Paper1 术语政策

本表是 `paper_outline.md` 的可机检术语合同。首次出现位置以大纲 section anchor 为准；后续正文使用“后续允许形式”。代码、公式、路径、正式论文/工具名称和表中 `protected exceptions` 不参加英文全称检查。

| term_id | 中文 | English | 缩写 | 首次出现位置 | 后续允许形式 | protected exceptions |
| --- | --- | --- | --- | --- | --- | --- |
| natural_language | 自然语言 | natural language | NL | `outline-0` | 自然语言；`NL` 仅在公式、表列或代码字段 | `<free-form NL requirements, ...>` 任务合同与 `NL` 字段 |
| state_machine | 状态机 | state machine | STM | `outline-0` | 状态机；`STM` 仅在任务合同、表列、代码或文献题名 | `STM`、`source STM`、论文与工具正式题名 |
| source_stm | 源状态机制品 | source-attributed state-machine artifact | 无 | `outline-0` | 源状态机制品 | `<..., pre-existing source-attributed STM held fixed>`、`source STM` |
| large_language_model | 大语言模型 | large language model | LLM | `outline-0` | 大语言模型；`LLM` 仅在公式、表列或代码字段 | `LLM`、论文与工具正式题名 |
| fcstm | 有限控制状态机 | finite control state machine | FCSTM | `outline-0` | 有限控制状态机；`FCSTM` 在代码、公式、表列和字段中保留 | `FCSTM`、`fcstm`、路径和 API 名 |
| plantuml_adapter | PlantUML 适配器 | PlantUML adapter | 无 | `outline-0` | PlantUML 适配器 | `PlantUML` 正式语言名和源文件扩展名 |
| provenance | 来源归属 | provenance | 无 | `outline-0` | 来源归属 | `provenance-preserving`、`source attribution`、文件/字段名 |
| inspect_facts | 确定性检查事实 | deterministic inspect facts | 无 | `outline-0` | 确定性检查事实 | `inspect facts`、代码、字段和图标签 |
| typed_predicate | 类型化谓词 | typed predicate | 无 | `outline-0` | 类型化谓词 | predicate ID、`typed predicate plan`、代码字段 |
| replay_receipt | 回放回执 | replay receipt | 无 | `outline-0` | 回放回执 | `source-bound replay receipt`、代码字段 |
| witness_strength | 见证强度 | witness strength | W | `outline-3` | 见证强度；`W0/W1/W2` 在表、公式和字段中保留 | `W0`、`W1`、`W2` |
| ledger_depth | 台账信息层级 | ledger depth | L | `outline-3` | 台账信息层级；`L0/L1/L2` 在表、公式和字段中保留 | `L0`、`L1`、`L2` |
| adjudication | 人工裁定 | human adjudication | D/A | `outline-3` | 人工裁定；`D0/D1/D2/A0` 在表、公式和字段中保留 | `D0`、`D1`、`D2`、`A0` |
| relation | 对应关系 | relation | 无 | `outline-3` | 对应关系；`FULL/PARTIAL/NONE` 在表、公式和字段中保留 | `FULL_MATCH`、`PARTIAL_MATCH`、`NO_MATCH` |
| bookkeeping | 记账类别 | bookkeeping category | K/N/I | `outline-3` | 记账类别；`K/N/I` 在表、公式和字段中保留 | `VALID_KNOWN`、`VALID_NOVEL`、`INVALID` |
| nadc | 非缺陷主张 | not-a-defect claim | NADC | `outline-9-3` | 非缺陷主张；`NADC` 在表、公式和字段中保留 | `NOT_A_DEFECT_CLAIM` |
| current_baseline | 当前方法/基线 | current/baseline | 无 | `outline-0` | 当前方法、基线 | `current`、`baseline`、canonical artifact keys |

责任边界保持不变：人工完成 D/A、有效性、对应关系和最终确认；程序只在已完成的人工字段上确定性闭合 K/N/I 并复算汇总；C2 的回执不替代人工有效性或对应关系。PlantUML 是唯一已实现并评测的适配器，有限控制状态机是通用方法架构的工作表示，不是语言范围的限定。
