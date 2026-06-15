# Executable State Machines Derived from Structured Textual Requirements

## R1.5 strict seed 编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `executable-state-machines-structured-text` |
| source_batch | baseline / local fulltext |
| local_source | [`../../../../baselines/executable-state-machines-derived-from-structured-textual-requirements/`](../../../../baselines/executable-state-machines-derived-from-structured-textual-requirements/) |
| paper_title | `Executable State Machines Derived from Structured Textual Requirements - Connecting Requirements and Formal System Design` |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-3` |
| 排除码 | `NONE`；soft risk: `R_STRUCTURED_INPUT`, `R_MANUAL_NL_TO_SPS`, `NO_CODE_OR_MACHINE_READABLE_ARTIFACT`, `LICENSE_UNKNOWN` |
| 当前结论 | 可作为“结构化文本需求 -> 可执行 FSM”的经典弱 seed / related-work 证据；不应作为 R2 主冻结样本，因为入口依赖人工 `NL -> SPS` 结构化步骤，且未发现公开机器可读 artifact、代码、AOLC 数据包、eTrice 模型或 license。 |

## P1/P2/P3/P4 全文核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass with caveat | `paper_content.txt:20-24` 摘要说明 requirements documented as structured text 被映射到 logic space；`paper_content.txt:122-129` 说明从 structured textual requirements 派生 static models / executable state machines；`paper_content.txt:144-156` 给出自然语言 high-beam requirement、SPS 表达和 LTL 表达。 caveat：`paper_content.txt:129` 与 `paper_content.txt:144-146` 明确第一步 `NL to SPS` 是人工步骤，不是自由 NL 端到端自动生成。 |
| P2_T0_STM_FAMILY | pass | `paper_content.txt:94-107` 定义 Moore DFSM；`paper_content.txt:176-224` 定义 requirement FSM、atomic requirement FSM、system FSM，并通过 atomization / minimization / generalization 合成 system FSM；`paper_content.txt:234-239` 说明将 FSM 导出到 `eTrice` 并添加执行层。输出属于 FSM/DFSM/state-machine 家族，不是 protocol-only、BPMN/process、Petri/CSP/Event-B/TLA+、hybrid automata 或 T1+ timed automata。 |
| P3_GENERATION_RELATION | pass with caveat | `paper_content.txt:122-129` 说明流程为 requirements -> LTL -> FSM -> system FSM，除 `NL to SPS` 外自动；`paper_content.txt:196-224` 说明从 requirement FSM 合成 system FSM；`paper_content.txt:238-239` 说明导出到 `eTrice` 形成可执行模型；`paper_content.txt:504-512` 结论再次声明从 structured textual requirements 生成 executable finite state machines。 caveat：该文是初始建模 / 执行化，不是已知缺陷驱动 repair。 |
| P4_EVIDENCE_POINTER | pass | 本地候选目录含 `bibtex.bib`、`paper_content.txt`、`paper.pdf`；主要证据位于 Page 1-6 与 Page 7-8。源 `DESC.md` 明确原文未提供公开代码/仓库链接，也未提供公开数据集获取链接。源目录未发现 `ASSETS.md`。 |

## SS/SA 判定

### SS-B

该文满足 P1/P2/P3/P4 的核心文献证据：输入是结构化文本需求，输出是 system FSM / executable FSM，且生成链路清楚。但降为 `SS-B`，原因有三点：

1. 入口不是自由自然语言需求，而是人工整理后的 SPS / structured textual requirements。
2. 自动化链条明确排除了第一步 `NL -> SPS`。
3. 论文评估重心是 requirement-to-design 的可执行建模链路，不是 R2 所需的可复验 `<NL, STM_0>` 样本包。

### SA-3

artifact 不足以进入 R2 主样本。论文公开了方法、图示、AOLC 规模统计和测试步结果，但本地材料与源 `DESC.md` 均未给出公开代码、数据集下载、eTrice / Design Cockpit 模型、ReqIF、XML/XMI、完整测试用例、license、commit、release 或 DOI artifact。

## 排除码与边界

| 排除码 / 风险 | 状态 | 说明 |
|---|---|---|
| `X_PROTOCOL` | no | 案例是汽车 Adaptive Outside Light Control，不是协议 FSM 抽取。 |
| `X_T1_PLUS_OR_HYBRID` | no | 文中使用 LTL 作为中间形式，但输出是 DFSM/system FSM/executable FSM；未建模连续动力学或 timed automata。 |
| `X_FORMAL_SPEC_ONLY` | no with caveat | 输入仍是 structured textual requirements；但 SPS/LTL 前置较强，R2 使用时必须标注人工结构化步骤。 |
| `X_REPAIR_ONLY` | no | 该文是初始建模与执行化，不是 repair-only。 |
| `X_COEXIST_ONLY` | no | 文中给出从需求到 FSM 的 derivation/synthesis 链路，不只是需求和模型共存。 |
| `NO_CODE_OR_MACHINE_READABLE_ARTIFACT` | yes for artifact | 不影响文献相关性，但阻止进入可复验 R2 主样本。 |
| `LICENSE_UNKNOWN` | yes for artifact | 未发现代码/数据/model artifact license，不能推断可再分发。 |

## R2 可用性

| 项 | 判断 |
|---|---|
| R2_use | `related_work_or_manual_reconstruction_only` |
| 可用内容 | 方法链、SPS/LTL/FSM 合成步骤、high-beam 与 hazard-warning 示例、AOLC 38 条功能需求 / 38 个测试用例 / 47 states / 256 transitions / 63 passed + 8 blocked + 9 failed test steps 的论文级统计。 |
| 主要限制 | 无公开机器可读 AOLC requirement/test/model bundle；`NL -> SPS` 人工步骤无法从 artifact 复验；`eTrice` 接口存在 bounded-existence counter 限制。 |
| 建议角色 | 作为 structured-requirements-to-executable-FSM 的经典方法基线；不计入 `SS-A/SS-B + SA-1/SA-2` 的 R2 主 seed 下限。 |

## pending / blocker

- blocker：无公开代码、AOLC 数据包、ReqIF、eTrice 模型、完整测试用例、machine-readable FSM 和 artifact license。
- pending：若后续要人工重建，可从论文图 2-7 与 AOLC 统计出发，但需要另建数据来源、转写记录、hash 清单和授权口径。
