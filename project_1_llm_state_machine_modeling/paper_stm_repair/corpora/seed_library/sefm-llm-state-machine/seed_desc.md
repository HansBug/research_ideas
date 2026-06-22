# Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models

## R1.5 strict seed 编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `sefm-llm-state-machine` |
| source_batch | baseline / local fulltext |
| local_source | [`baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/`](../../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) |
| paper | Abdulkarim et al., arXiv:2604.00275, 2026-03-31 |
| strict_seed_grade | `SS-A` |
| artifact_usability | `SA-2` |
| exclusion_code | `NONE` |
| 当前结论 | 纳入 strict seed；适合作为“非结构化 NL -> UML state machine”直接生成 baseline，但 artifact 需先冻结并补 license/稳定性审计后再进入正式 R2。 |

## P1/P2/P3/P4 核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt` Page 1 Abstract 明确从 `non-structured NL requirements` 自动生成 UML state machine；Page 1 Problem Statement 写明给定 `non-structured NL system descriptions`，目标是自动 derive state machine；Page 5 Dataset and Setup 说明 8 个 reactive-system scenarios 含非结构化 NL behavior description。 |
| P2_T0_STM_FAMILY | pass | Page 2 Background 定义 UML state machines，包含 states、transitions、guard conditions、hierarchical states、orthogonal regions、history states；Page 2 Approach 写明输出 UML state machine model；Page 4 Table I 和 Page 5 Evaluation Scheme 按 states/transitions/guards/actions/hierarchical/parallel/history 等状态机元素评测。属于 T0 UML state machine / statechart family，不是协议源码抽取、混合系统或 T1+ 验证/修复主任务。 |
| P3_GENERATION_RELATION | pass | Page 1 Problem Statement 写明目标是 `fully automated state machine generation`；Page 2 Approach 形式化为系统描述 $d$ 到生成状态机 $sm' = f(d)$；Page 3-4 描述 Single-Prompt、Structure-Driven、Event-Driven、Hybrid 四条 generation strategies，其中 Hybrid 是先生成完整 Umple 草稿再细化，不是以已知缺陷 repair 为核心。 |
| P4_EVIDENCE_POINTER | pass | 本地 `bibtex.bib` 给出 arXiv/DOI；`paper_content.txt` Page 1-6 给出任务、输入、输出、数据和评测；源目录 [ASSETS.md](../../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/ASSETS.md) 给出 4open artifact、ZIP、关键文件 hash、数据集和结果 workbook 核验记录。 |

## SS/SA 判定

### SS-A

该论文直接命中 strict seed 的核心形态：输入为非结构化自然语言 reactive-system/system requirements，输出为 UML state machine，并且论文主体问题就是 LLM state machine generation。它不是只做状态机评审、补全、repair、verification、protocol implementation mining、日志抽取或 GWT 结构化输入转换。

可作为 Project 1 / R1.5 的强 seed baseline，尤其适合支撑以下对比：

1. 单提示直接生成 Umple 状态机。
2. 结构驱动多步生成状态机元素。
3. 事件驱动多步生成与合并。
4. Hybrid：先生成完整草稿，再按结构化步骤细化。

### SA-2

artifact 对复现实验有实际价值，但暂不应标为 SA-1。源目录 `ASSETS.md` 已核到 4open 浏览器入口、ZIP 下载入口、源码、prompt/example、8 个 reference solutions、生成图片和 F1 workbook；还记录了关键文件大小和 SHA-256。主要风险是 artifact 位于 Anonymous Github / 4open，未见稳定 Git commit、正式 release、Zenodo DOI 或 license 文件快照，且尚未在本仓库真实安装复跑。

因此当前可用性为：可下载、可冻结、可人工/脚本审计，适合进入 R2 前准备；但正式 R2 需要先冻结本地副本、补全逐文件 hash、确认 license/redistribution，并记录 LLM API/model drift。

## 排除码

| 排除码 | 结论 | 说明 |
|---|---|---|
| `EX-NOT-STM` | no | 输出明确是 UML state machine。 |
| `EX-NO-NL` | no | 输入明确是 non-structured NL requirements / system descriptions。 |
| `EX-NO-GEN` | no | 主任务明确是 automated generation / derivation。 |
| `EX-STRUCTURED-ONLY` | no | 论文强调不同于 GWT/structured requirements，目标是 non-structured NL。 |
| `EX-PROTOCOL-MINING` | no | 相关工作提到 ProtocolGPT，但本文不是从协议源码推断状态机。 |
| `EX-REPAIR-ONLY` | no | Hybrid 有 refinement，但基于生成草稿的生成策略，不是已知缺陷 repair 主论文。 |
| `EX-VERIFICATION-ONLY` | no | 没有以模型检查/形式验证为主任务。 |
| `EX-T1PLUS-HYBRID` | no | 不建模连续动力学/混合自动机；状态机含层次、并发、history，但仍属 UML state machine family。 |

## R2 可用性

| 项 | 当前判断 |
|---|---|
| 输入样例 | 可用；8 个非结构化系统描述在 4open artifact 和 `state_machine_descriptions.py` 中已由源目录核到。 |
| 参考解 | 可用；8 个 reference solutions 含 `.txt` 与 `.png`。 |
| 生成代码 | 可用但待复跑；源目录核到 Python code、prompt、examples、后处理与依赖。 |
| 结果对账 | 可用；`Final Detailed F1-Scores.xlsx` 已核到大小与 hash，含 TP/FN/FP、precision、recall、F-score。 |
| license / redistribution | blocker；源目录未记录已确认 license 文件或正式发布许可。 |
| URL 稳定性 | risk；4open hashbang 和 ZIP 当前可用，但不是 DOI/release 级长期归档。 |
| 运行复现 | pending；未安装运行，真实复跑需要 API key、provider 版本、Graphviz/Java/Umple 等环境记录。 |

## reviewer 结论

纳入 `SS-A / SA-2 / NONE`。该论文可以作为 strict seed 中最贴近“非结构化自然语言到状态机生成”的样本之一；但在进入正式 R2 或四例冻结样本前，应完成 artifact 本地冻结、license 核验、逐文件 hash、运行环境和真实 smoke 记录。

## R2.0 registry 口径更新

一手 registry 口径起，本条目不得把 `Reference Solutions/*.txt` 计为 generated `STM_0`。真正可候选的 generated seed 必须来自 4open ZIP 中 `backend/resources/state_machine_descriptions.py` 的 NL 描述与 `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt` 等作者生成输出的可回溯配对。当前本条目 `assets/` 只登记 4open metadata pointer，ZIP 尚未 committed，因此 eligible generated seed count 仍为 0；reference solutions 只能作为评价参考。
