# Paper1 术语政策

本表是 `paper_outline.md` 的可机检术语合同。首次出现位置以大纲 section anchor 为准；后续正文使用「后续允许形式」。代码、公式、路径、正式论文/工具名称和表中 `protected exceptions` 不参加英文全称检查。自然语言输入统一称「自然语言描述」，不称「需求」；上游数据集作者的 requirement description 只在 §5.1 交代一次。

| term_id | 中文 | English | 缩写 | 首次出现位置 | 后续允许形式 | protected exceptions |
| --- | --- | --- | --- | --- | --- | --- |
| natural_language | 自然语言 | natural language | NL | `outline-0` | 自然语言、自然语言描述；`NL` 仅在公式、表列或代码字段 | `NL` 字段与任务合同 |
| state_machine | 状态机 | state machine | STM | `outline-0` | 状态机；`STM` 仅在任务合同、表列、代码或文献题名 | `STM`、论文与工具正式题名、反引号内的英文题目候选 |
| large_language_model | 大语言模型 | large language model | LLM | `outline-0` | 大语言模型；`LLM` 仅在公式、表列或代码字段 | `LLM`、`LLM-as-a-Judge`、论文与工具正式题名 |
| fcstm | 有限控制状态机 | finite control state machine | FCSTM | `outline-0` | 有限控制状态机；`FCSTM` 在代码、公式、表列和字段中保留 | `FCSTM`、`fcstm`、路径和 API 名 |
| plantuml_adapter | PlantUML 适配器 | PlantUML adapter | 无 | `outline-0` | PlantUML 适配器 | `PlantUML` 正式语言名和源文件扩展名 |
| provenance | 来源归属 | provenance | 无 | `outline-0` | 来源归属、来源映射 | 文件/字段名与链接目标 |
| inspect_facts | 确定性检查事实 | deterministic inspect facts | 无 | `outline-0` | 确定性检查事实、检查事实 | `inspect facts`、代码、字段和图标签 |
| typed_predicate | 类型化谓词 | typed predicate | 无 | `outline-0` | 类型化谓词、谓词 | predicate ID、代码字段 |
| replay_receipt | 回放回执 | replay receipt | 无 | `outline-0` | 回放回执、回执 | 代码字段 |
| problem_depth | 问题深度 | problem depth | L | `outline-2` | 问题深度；`L0/L1/L2` 在表、公式和字段中保留 | `L0`、`L1`、`L2` |
| witness_strength | 见证强度 | witness strength | W | `outline-2` | 见证强度、证据强度；`W0/W1/W2` 在表、公式和字段中保留 | `W0`、`W1`、`W2` |
| use_case_specification | 用例规约 | use-case specification | UCS | `outline-2` | 用例规约；`UCS` 在文献比较、表列或字段中保留 | `UCS`、论文题名和原文引述 |
| llfsm | 轻量级有限状态机 | Lightweight Finite State Machine | LLFSM | `outline-2` | 轻量级有限状态机；`LLFSM` 在文献比较、表列或字段中保留 | `LLFSM`、论文题名和原文引述 |
| adjudication | 人工裁定 | human adjudication | D/A | `outline-5` | 人工裁定；`D0/D1/D2/A0` 在表、公式和字段中保留 | `D0`、`D1`、`D2`、`A0` |
| relation | 对应关系 | relation | 无 | `outline-5` | 对应关系；`FULL/PARTIAL/NO` 在表、公式和字段中保留 | `FULL_MATCH`、`PARTIAL_MATCH`、`NO_MATCH` |
| bookkeeping | 记账类别 | bookkeeping category | K/N/I | `outline-5` | 记账类别；`K/N/I` 在表、公式和字段中保留 | `VALID_KNOWN`、`VALID_NOVEL`、`INVALID` |
| nadc | 非缺陷主张 | not-a-defect claim | NADC | `outline-5` | 非缺陷主张；`NADC` 在表、公式和字段中保留 | `NOT_A_DEFECT_CLAIM` |
| divergence_checks | 源–语义分歧检查 | source–semantics divergence checks | 无 | `outline-0` | 源–语义分歧检查、分歧检查、分歧审计 | 代码字段、`source_divergence` frontier kind |
| author_source_index | 作者源索引 | author-source index | 无 | `outline-4` | 作者源索引；作者拥有 / 编译器拥有的载体 | 代码字段 |
| carrier_attribution_gate | 载体归属门 | carrier-attribution gate | 无 | `outline-4` | 载体归属门 | `skipped_compiler_owned_carrier` |
| causal_fold | 因果折叠 | causal fold | 无 | `outline-4` | 因果折叠、子主张 | 代码字段 |
| guard_modality_aggregation | 守卫模态聚合 | guard-modality aggregation | 无 | `outline-4` | 守卫模态聚合、聚合根 | 代码字段 |
| lossy_normalization | 有损规范化 | lossy normalization | 无 | `outline-4` | 有损规范化 | — |
| semantic_judge | 语义 judge | semantic judge | 无 | `outline-0` | 语义 judge、judge、校准 judge | 配置名 `semantic-judge.two-stage.v3.11`、路径 |

责任边界（v61 口径）：D/A、有效性与对应关系的定义来自人工裁定协议，执行者是校准的语义 judge（两臂同一仪器）；程序只在 judge 已完成的字段上确定性闭合 K/N/I 并汇总；C2 的回执不替代有效性或对应关系的裁定；方法侧 903 条报告尚无人工复核，基线侧 512 条另有完整人工裁定，仪器偏移在大纲 §5.3 与 §8 交代。W2 同时要求受支持片段、精确实例绑定、pair/obligation/plan/model/program/receipt 的身份链、非空可核验引文与完成的原生布尔回执；323 个 FULL 命中单元的 W0/W1/W2 为 `0/196/127`（根报告口径）或 `0/186/137`（含折叠子主张回执），报告级为 `0/636/267`（分母 903）。
