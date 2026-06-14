# From Use Cases to Statecharts

## R1.5 strict seed 编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `from-use-cases-to-statecharts` |
| source_batch | baseline / local fulltext |
| local_source | [`../../../../baselines/from-use-cases-to-statecharts/`](../../../../baselines/from-use-cases-to-statecharts/) |
| paper_title | `An Approach to Building Object Models with UML in Embedded Systems` |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-3` |
| 排除码 | `NO_CODE_OR_MACHINE_READABLE_ARTIFACT`; `STATECHART_IS_INTERMEDIATE_OUTPUT`; `PAPER_ONLY_CASE_STUDY` |
| 当前结论 | 可作为 classic NL use case -> UML statechart 的弱冻结 seed；不能作为 SS-A，也不能直接进入自动化 artifact 复现实验。 |

## P1/P2/P3/P4 全文核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt` Page 1 摘要与引言说明方法从 use cases 出发；Page 3 `2.1. Use Cases` 定义 use case 文本模板，并在 Fig. 2 给出 elevator request 的自然语言步骤、alternatives 与 QoS。 |
| P2_T0_STM_FAMILY | pass with caveat | `paper_content.txt` Page 4-5 `2.2. Statecharts` 说明使用 UML statechart，含 state、transition、event、guard、hierarchy、concurrency 与 timing interval；这是 statechart/HSM/EFSM 家族，不是 protocol-only，也未出现连续物理动力学 hybrid automata。 caveat：该文扩展了 timing constraints，R2 使用时应保留为 timed annotation，而不是误写成纯 FSM。 |
| P3_GENERATION_RELATION | pass | `paper_content.txt` Page 6-7 `3.1. From Use Cases to Statecharts` 和 Table 1 明确给出从 use case text 到 Graph of Behavior Sequences 再到 statechart 的四轮 derivation/checking procedure；Page 8-9 展示 elevator 示例从步骤、guard、事件、缺失操作与 timing constraint 逐步形成 Fig. 7 statechart。 |
| P4_EVIDENCE_POINTER | pass | 主要证据位于 `paper_content.txt` Page 1, Page 3, Page 4-5, Page 6-9, Page 11；本地 PDF 与文本见同目录 `paper.pdf`、`paper_content.txt`、`bibtex.bib`。 |

## SS/SA 判定

- `SS-B`：输入是自然语言 use case，输出链路中确有 statechart，且论文给出较完整的手工 derivation procedure；但最终研究目标是 object model，statechart 是桥梁产物，不是论文的最终评测对象。
- `SA-3`：只有论文 PDF、文本提取和 BibTeX；未发现公开代码、XMI、statechart 源文件、数据集、supplementary artifact 或 license 声明。图 5-8 可人工转写，但不可直接自动 ingest。

## R2 可用性

| 项 | 判断 |
|---|---|
| R2_use | `limited_manual_transcription` |
| 可用内容 | Elevator request use case、GBS、iteration 2 statechart、final statechart、object identification procedure。 |
| 主要限制 | Fig. 6-8 是论文图，不是机器可读模型；timing constraints 和缺失操作来自正文叙述，R2 转换时需要人工建立 trace。 |
| 建议角色 | 作为“NL use case -> intermediate statechart”的历史/经典方法 seed；用于修复/验证实验时只适合做人工标注样例，不适合作为自动复现实验单元。 |

## pending / blocker

- blocker：无公开 machine-readable artifact 与 license；不得标 `SS-A`。
- pending：如后续需要 publisher DOI、正式出版社页面或可授权再分发状态，需要人工再核验外部来源；本轮未发现本地 `ASSETS.md`。
