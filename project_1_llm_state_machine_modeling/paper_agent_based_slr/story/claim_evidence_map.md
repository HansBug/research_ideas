# 主张-证据映射：研究者引导的智能体式 SLR 支持工作流

## 1. 使用规则

本文件是第二篇论文 PR-S0 阶段的主张审查门。任何摘要、引言、贡献、结论、PR body 或 PR comment 中的强主张，都必须先在本文件中找到对应的证据状态和安全写法。

状态口径：

- 🟢：PR-S0 可作为任务定义 / 方法设计主张使用，但仍需避免结果化表述。
- 🟡：方向合理，但需要后续 A2/A3/A5/A6 补证后才能写成论文主结论。
- 🔴：禁止主张，只能出现在风险、限制或禁止写法语境。
- 🟣：依赖 PR #97 OPEN / 未合入 / 快照 / 分支局部证据，不能写成 `main` 事实。

重要边界：PR-B0 基线文库已经形成 35 篇全文文本级近邻 review，并明确暴露 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻。后续不能再把 LLM / 智能体辅助 SLR、人在回路、来源追溯、筛选 / 抽取或综述生成写成空白。

## 2. 主张映射

| ID | 主张类型 | 状态 | 当前可写安全表述 | 当前证据 | 后续所需证据 | 禁止写法 |
|---|---|---:|---|---|---|---|
| C1 | 论文任务定义 | 🟢 | 本文研究研究者引导、发现导向、可审计的智能体式 SLR 支持工作流：研究者基于脚手架实例化综述元模型，智能体提出候选研究发现，研究者通过证据质疑闭环审计与修订。 | PR #101、PR #112 导师讨论记录、[paper_story.md](./paper_story.md)、[terminology_policy.md](./terminology_policy.md)。 | A2 脚手架 / schema、A3 场景、A4/A5 运行与评价。 | 本文已经证明智能体可端到端生成合格 SLR；本文首次提出智能体辅助 SLR 工作流。 |
| C2 | `sources/` 资产角色 | 🟢 | `sources/` 可作为领域场景、压力测试或证据包来源。 | `main` 已有 `sources/` 文库与导师定调。 | A3 场景定义。 | `sources/` 文库规模本身就是第二篇论文新颖性。 |
| C3 | PR #97 资产角色 | 🟣 | PR #97 提供 OPEN / 未合入 / 快照 / 分支局部的相关工作筛选与全文抽取证据线索。 | [PR #97 comment](https://github.com/HansBug/research_ideas/pull/97#issuecomment-4682737117)、当前 OPEN 状态与快照 `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727`。 | PR #97 merge 或冻结 SHA 后复核。 | PR #97 25 篇全文文库已经是 `main` 已有正式资产。 |
| C4 | 研究者定义的元模型 | 🟡 | 论文计划把研究者基于脚手架裁剪并实例化主题特定综述元模型作为综述框架起点；这一步由研究者审计把关。 | PR #112 导师讨论记录；[terminology_policy.md](./terminology_policy.md)。 | survey-of-surveys、脚手架字段、实例化案例、研究者批准日志。 | 禁止写：LLM 自动定义可靠元模型；禁止写：本文定义通用软件工程综述本体。 |
| C5 | 研究发现模式脚手架 | 🟡 | 论文计划用研究发现模式约束候选研究发现的类型、结构和证据要求。 | PR #112 导师讨论记录；[paper_story.md](./paper_story.md)。 | 模式来源、示例、人工审计可理解性、研究发现类型覆盖。 | 智能体自由生成最终研究发现；研究发现模式已被证明提高质量。 |
| C6 | 候选 / 最终研究发现边界 | 🟢 | 候选研究发现只有经过来源锚定证据、反向证据 / 不确定性检查、范围和主张强度由研究者确认后，才可升级为最终研究发现。 | PR #112 导师讨论记录；[terminology_policy.md](./terminology_policy.md)。 | A2/A5 研究发现台账 schema、审计示例、接受 / 降级 / 未解决记录。 | LLM / 智能体直接产出最终研究发现。 |
| C7 | 以研究发现为中心的证据包 | 🟡 | 论文计划围绕候选研究发现组织支持性 / 反向证据、来源锚点、质疑日志、修订历史和最终状态；最终研究发现仍需研究者审计。 | PR #112、[paper_story.md](./paper_story.md)、B0 关于来源追溯 / 审计近邻的风险结论。 | A2 schema、A4 写出器、A5 断链率 / 定位错误率 / 无证据支撑研究发现统计。 | 我们已经实现每条研究发现完全可追踪；证据链证明研究发现为真。 |
| C8 | 研究者质疑闭环 | 🟡 | 论文计划让研究者对候选研究发现发起证据不足、范围过宽、反例缺失或主张强度过强等质疑，并记录修订、降级、未解决或接受。 | PR #112 导师讨论记录；[terminology_policy.md](./terminology_policy.md)。 | 质疑协议、日志 schema、修订 / 降级 / 未解决率、审计成本。 | 质疑闭环必然提高研究发现质量；人工审计保证最终报告完全正确。 |
| C9 | 幻觉 / 无证据支撑研究发现控制 | 🟡 | 论文计划通过金事实 / 银事实、陷阱论文、主张到来源审计与质疑闭环评估无证据支撑或过强候选研究发现。 | PR #101、PR-B0 基线总账、A0/PR-S0 评价维度。 | A3 事实 / 陷阱集、A5 分类体系、残余无证据支撑研究发现统计。 | 智能体式 SLR 完全无幻觉；所有无证据支撑主张都能自动消除。 |
| C10 | 透明报告 | 🟡 | 论文计划生成类 PRISMA 流程、排除理由、协议偏离日志等透明报告材料；合规性需 checklist 与人工专家核验。 | PR #101、[protocol.md](./protocol.md)。 | A2 schema、A5 checklist / 报告制品。 | 禁止写：本文 PRISMA-compliant。 |
| C11 | 覆盖代理 | 🟡 | 论文计划报告已知条目召回、种子论文恢复、数据库重叠等覆盖代理。 | PR #101 RQ7、[../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。 | A3 已知集合、A5 计算协议。 | 禁止写：本文实现完整覆盖。 |
| C12 | 成本效率 | 🟡 | 论文计划记录智能体时间、token / API 成本、人工审计时间、质疑成本和修正成本。 | PR #101 RQ4、B0 基线对成本差异和人工复核成本的提醒。 | A4 运行记录、A5 成本分析。 | 智能体一定显著降低总成本；质疑闭环免费。 |
| C13 | 与 P0 强近邻差异 | 🟡 | 已有 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 等强近邻；本文差异只能收窄为 SE SLR/SMS 中研究者实例化的元模型、研究发现模式、研究发现级证据链与质疑闭环的组合。 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、各单篇 `review.md`。 | A1/A6 相关工作深化、PDF 图表核对、制品审计。 | 已有工作没有智能体式 SLR / 人在回路 / 来源追溯 / 证据综合。 |
| C14 | SE 社区已有 LLM-SLR 风险讨论 | 🟢 | WSESE@ICSE 2025 已讨论在 SE 中使用 LLM 支持 SLR 执行与复现的困难；本文应把提示词敏感性、随机性、模型漂移、成本、透明性和数据仓库缺口转成方法与评价义务。 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、[WSESE review](../baselines/papers/wsese-difficulties-replicating-slr-llms-se/review.md)。 | A1/A6 相关工作写作；必要时核对 PDF。 | SE 社区尚未讨论 LLM-assisted SLR difficulties。 |
| C15 | 完整自动化 / 全生命周期 | 🔴 | 只能写“覆盖后续实验中明确定义的阶段子集，并将未覆盖环节列为 limitation”。 | B0 基线已发现多个多阶段 pipeline；PR-S0 不实现运行时。 | 若未来声称生命周期覆盖，必须逐阶段 schema、运行、评价和 limitation 闭合。 | fully automated SLR；complete lifecycle automation；end-to-end qualified SLR。 |
| C16 | 首创性 | 🔴 | 只能写“面向研究发现级审计与研究者质疑的研究”，不能写首次。 | 已知 ASReview、RobotReviewer、综述自动化、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、综述生成等近邻。 | 若未来要写新颖性，必须经系统性相关工作 gate。 | first automated SLR；first agentic SLR；first LLM-based systematic review。 |
| C17 | 专家替代 | 🔴 | 本文保留研究者所有权和人工审计门，研究人机分工。 | 导师定调与 PR-S0 story。 | 不适用。 | 智能体完全替代 SLR 专家；研究者只做最终润色。 |

## 3. 摘要 / 引言安全句式

可以作为后续英文稿前的中文安全句式：

1. 本文研究如何让研究者在 SE SLR/SMS 中显式化综述框架，并让智能体在该框架下提出可审计的候选研究发现。
2. 本文不把报告生成视为核心贡献；报告只是已接受 / 已降级 / 未解决研究发现的下游投影。
3. 本文以研究发现为中心的证据包为核心，要求每个候选研究发现能追溯到证据对象、来源锚点、支持性 / 反向证据、质疑历史和最终状态。
4. 本文把类 PRISMA 流程和排除理由台账作为透明报告材料；禁止在 checklist 未闭合前声称 PRISMA-compliant。
5. 本文使用覆盖代理描述覆盖情况；禁止声称完整覆盖。

## 4. 后续更新规则

- PR #97 状态变化时必须更新 C3。
- A2 若冻结元模型 / 研究发现 / 质疑 schema，必须更新 C4--C8。
- A3 若构造场景、金事实 / 银事实与陷阱论文，必须更新 C9 / C11。
- A4/A5 若产生真实运行与指标，才能把 🟡 中部分主张升级为结果主张。
- A6 / 相关工作若新增直接竞争工作，必须更新 C13--C16。
