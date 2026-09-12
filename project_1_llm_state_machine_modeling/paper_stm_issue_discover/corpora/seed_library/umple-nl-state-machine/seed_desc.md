# Exploring How Well Llama3 can Generate State Machines Represented in Umple

## R1.5 strict seed 编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `umple-nl-state-machine` |
| source_batch | baseline / local fulltext |
| local_source | [`baselines/umple/`](../../../../baselines/umple/) |
| paper | Pathak, Master's Thesis, University of Ottawa, 2025 |
| strict_seed_grade | `SS-A` |
| artifact_usability | `SA-3` |
| exclusion_code | `NONE` |
| 当前结论 | 纳入 strict seed 文献证据；不作为 R2 主冻结样本，因为论文专属 benchmark bundle、逐次生成输出和评测脚本未公开，无法形成一手 `NL + generated STM_0` trace。 |

## P1/P2/P3/P4 核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt` Page 2 Abstract 明确用户只提供 short description / system requirements；Page 10-11 RQ 与 method 写明输入是 sets of requirements；Page 26-31 给出 Blackjack、Course Section、Credit Card Transaction、Driver License、Hotel Stay 五组自然语言 requirements；Page 40 prompt 模板为 `Write a state machine ... with the following requirements`。 |
| P2_T0_STM_FAMILY | pass | Page 1-2 明确目标是 Umple state machine modeling code；Page 6-7 展示 Umple textual state machine 与 nested state machine 语法；Page 7 说明 timed transitions、guards、concurrent do-activities、history 等高级特性不属于本文实验。输出属于 T0 Umple FSM/HSM/statechart family，不是 protocol FSM、formal spec、hybrid automata 或 T1+ timed automata。 |
| P3_GENERATION_RELATION | pass | Page 10-11 RQ1/RQ2/RQ3 均表述为 Llama 3 从 requirements 生成 corresponding state machine；Page 22-24 定义生成代码的 ICP/EUCP/Levenshtein/Pass@K 评测；Page 32-34 描述 zero-shot/one-shot/RAG prompt，Llama 3 生成 Umple code；Page 35、38、43 分别报告三个 generation experiments。 |
| P4_EVIDENCE_POINTER | pass | 本地 `bibtex.bib` 给出 RUOR thesis URL；`paper_content.txt` Page 2、10-11、22-35、38-50 给出任务、输入、输出、样例、prompt、评测和结果；源目录 [ASSETS.md](../../../../baselines/umple/ASSETS.md) 记录 RUOR PDF、DOI、Umple 工具链、未公开论文实验代码和 benchmark bundle 的 artifact 核验结论。 |

## SS/SA 判定

### SS-A

该论文直接满足 strict seed 文献资格：输入是自然语言系统描述 / requirements，输出是 Umple textual state machine code，核心任务是 Llama 3 在 zero-shot、one-shot、RAG 三种设置下进行 `NL -> T0 STM-family` 生成。它不是状态机修复、验证、协议抽取、已有图模型转换或 formal-spec 转换论文。

该文献适合作为 related work / seed 方向证据，尤其支持：

1. LLM 从短自然语言需求生成文本化状态机 DSL。
2. one-shot / RAG 示例对小众建模语言语法的帮助。
3. 编译有效性、extra code、人工修正距离等评估口径。

### SA-3

artifact 不足以进入 R2 主样本。论文公开了 PDF 与正文中的 5 个系统 requirements、若干图示、聚合表和方法说明；源目录记录可从 Umple 官方手册 / UmpleOnline 近似重建部分示例。但未发现论文专属实验仓库、RAG 文档库、逐次 Llama 3 输出、人工 corrected references、评测脚本、完整 benchmark bundle或可冻结 commit / DOI artifact。

因此当前可用性为 paper-only / reconstructable clues：可支撑文献叙述和手工重建参考，不应声称为可复验 R2 seed pair。

## 排除码

| 排除码 | 结论 | 说明 |
|---|---|---|
| `X_PROTOCOL` | no | 不是 RFC / 3GPP / network protocol FSM extraction。 |
| `X_RESOURCE_FLOW` | no | 不是资源流或调度资源生命周期建模。 |
| `X_PROCESS` | no | 输出不是 BPMN / process model。 |
| `X_SEQUENCE_CLASS` | no | 输出不是 sequence/class/goal/domain model；目标为 Umple state machine。 |
| `X_FORMAL_SPEC` | no | 输出不是 Petri net、CSP、Event-B、TLA+、LTL/STL 等形式规格。 |
| `X_T1_PLUS` | no | 论文明确未使用 timed transitions 等高级时间特性；主实验为 T0 状态机。 |
| `X_HYBRID` | no | 不涉及连续动力学或 hybrid automata。 |
| `X_NO_GEN_REL` | no | 明确存在 requirements -> Umple state machine generation。 |
| `X_REPAIR_ONLY` | no | 人工 corrected reference 用于评估生成结果，不是以已有缺陷 STM repair 为主任务。 |
| `X_ARTIFACT_UNCLEAR` | no for literature / yes for R2 artifact | 文献证据清楚；可复验 artifact 不完整，已在 `SA-3` 中处理。 |

## R2 可用性

| 项 | 当前判断 |
|---|---|
| 输入样例 | 部分可用；论文 Page 26-31 给出 5 组自然语言 requirements，可手工录入。 |
| 参考解 / STM 输出 | 不完整；论文有图示和局部示例，但没有可机器消费的完整 ground truth / corrected reference bundle。 |
| 生成输出 | 不可用；未公开逐次 zero-shot / one-shot / RAG Llama 3 输出。 |
| 评测脚本 | 不可用；论文只描述 ICP/EUCP/Levenshtein/CodeBLEU/Pass@K，未给脚本。 |
| 引用 / 来源说明 | 论文 PDF 属公开学术材料，后续引用原作即可；实验数据和脚本未公开，因此缺的是一手 trace / 版本 / hash，不是许可阻塞。 |
| URL 稳定性 | paper stable；artifact weak。RUOR item / DOI 稳定；Umple 官方示例是活网页，不能替代 thesis benchmark bundle。 |
| 运行复现 | 待补 / 高成本；需要自行重建 Llama 3 8B、Nomic embeddings、prompt、示例库、Umple 编译和人工修正评测。 |

## reviewer 结论

纳入 `SS-A / SA-3 / NONE`。该论文可作为“LLM requirements-to-Umple state machine generation”的 strong literature seed，但不能计入 `SS-A + SA-1/SA-2` 的 R2 主 seed 下限。若后续要复用，只能先作为手工重建任务：录入 5 组 requirements，另行建立 reference STM、来源说明、hash 清单和最小 smoke，不得把论文聚合表当作可复验 artifact。
