# 主张-证据映射：研究者引导的智能体式 SLR 支持工作流

## 1. 使用规则

本文件是第二篇论文 PR-S0 阶段的主张审查门。任何摘要、引言、贡献、结论、PR body 或 PR comment 中的强主张，都必须先在本文件中找到对应的证据状态和安全写法。

状态口径：

- 🟢：PR-S0 可作为任务定义 / 方法设计主张使用，但仍需避免结果化表述。
- 🟡：方向合理，但需要后续 A2/A3/A5/A6 补证后才能写成论文主结论。
- 🔴：禁止主张，只能出现在风险、限制或禁止写法语境。
- 🟣：依赖 PR #97 OPEN / 未合入 / snapshot / branch-local evidence，不能写成 `main` fact。

重要边界：PR-B0 baseline 文库已经形成 35 篇全文文本级近邻 review，并明确暴露 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻。后续不能再把 LLM / 智能体辅助 SLR、HITL、provenance、筛选 / 抽取或综述生成写成空白。

## 2. 主张映射

| ID | 主张类型 | 状态 | 当前可写安全表述 | 当前证据 | 后续所需证据 | 禁止写法 |
|---|---|---:|---|---|---|---|
| C1 | 论文任务定义 | 🟢 | 本文研究研究者引导、发现导向、可审计的智能体式 SLR 支持工作流：研究者基于 scaffold 实例化 meta-model，智能体提出 candidate findings，研究者通过 evidence challenge loop 审计与修订。 | PR #101、PR #112 导师讨论记录、[paper_story.md](./paper_story.md)、[terminology_policy.md](./terminology_policy.md)。 | A2 scaffold/schema、A3 场景、A4/A5 运行与评价。 | 本文已经证明智能体可端到端生成合格 SLR；本文首次提出智能体辅助 SLR 工作流。 |
| C2 | `sources/` 资产角色 | 🟢 | `sources/` 可作为 domain scenario / stress test / evidence package 来源。 | `main` 已有 `sources/` 文库与导师定调。 | A3 场景定义。 | `sources/` 文库规模本身就是第二篇论文新颖性。 |
| C3 | PR #97 资产角色 | 🟣 | PR #97 提供 OPEN / 未合入 / snapshot / branch-local 的 related-work 筛选与全文抽取证据线索。 | [PR #97 comment](https://github.com/HansBug/research_ideas/pull/97#issuecomment-4682737117)、当前 OPEN 状态与 snapshot `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727`。 | PR #97 merge 或冻结 SHA 后复核。 | PR #97 25 篇全文文库已经是 `main` 已有正式资产。 |
| C4 | 研究者定义的 meta-model | 🟡 | 论文计划把研究者基于 scaffold 裁剪并实例化 topic-specific review meta-model 作为 review frame 起点；这一步由 researcher audit 把关。 | PR #112 导师讨论记录；[terminology_policy.md](./terminology_policy.md)。 | survey-of-surveys、scaffold 字段、实例化案例、researcher approval log。 | LLM 自动定义可靠 meta-model；本文定义 universal SE review ontology。 |
| C5 | finding pattern scaffold | 🟡 | 论文计划用 finding patterns 约束 candidate findings 的类型、结构和证据要求。 | PR #112 导师讨论记录；[paper_story.md](./paper_story.md)。 | pattern 来源、示例、人工审计可理解性、finding type coverage。 | 智能体自由生成 final findings；finding pattern 已被证明提高 quality。 |
| C6 | candidate / final finding 边界 | 🟢 | candidate finding 只有经过来源锚定 evidence、反向证据 / uncertainty 检查、范围和主张强度由研究者确认后，才可升级为 final finding。 | PR #112 导师讨论记录；[terminology_policy.md](./terminology_policy.md)。 | A2/A5 finding ledger schema、audit examples、accepted / downgraded / unresolved 记录。 | LLM / 智能体直接产出 final finding。 |
| C7 | 以研究发现为中心的证据包 | 🟡 | 论文计划围绕 candidate findings 组织支持性 / 反向证据、source anchors、challenge logs、revision history 和 final status；最终 final finding 仍需 researcher audit。 | PR #112、[paper_story.md](./paper_story.md)、B0 关于 provenance / audit 近邻的风险结论。 | A2 schema、A4 写出器、A5 断链率 / 定位错误率 / unsupported finding 统计。 | 我们已经实现每条 finding 完全可追踪；evidence chain 证明 finding 为真。 |
| C8 | researcher challenge loop | 🟡 | 论文计划让研究者对 candidate finding 发起证据不足、范围过宽、反例缺失或主张强度过强等 challenge，并记录修订、降级、unresolved 或 accepted。 | PR #112 导师讨论记录；[terminology_policy.md](./terminology_policy.md)。 | challenge 协议、log schema、revision / downgrade / unresolved rate、审计成本。 | challenge loop 必然提高 finding quality；人工审计保证最终报告完全正确。 |
| C9 | 幻觉 / unsupported finding 控制 | 🟡 | 论文计划通过 gold / silver facts、trap papers、claim-to-source audit 与 challenge loop 评估 unsupported / overclaimed findings。 | PR #101、PR-B0 baseline 总账、A0/PR-S0 评价维度。 | A3 fact/trap set、A5 taxonomy、残余 unsupported finding 统计。 | 智能体式 SLR 完全无幻觉；所有 unsupported claims 都能自动消除。 |
| C10 | 透明报告 | 🟡 | 论文计划生成 PRISMA-style flow、排除理由、协议偏离日志等透明报告材料；合规性需 checklist 与人工专家核验。 | PR #101、[protocol.md](./protocol.md)。 | A2 schema、A5 checklist / report artifact。 | 本文 PRISMA-compliant。 |
| C11 | 覆盖代理 | 🟡 | 论文计划报告 known-item recall、seed recovery、database overlap 等 coverage proxy。 | PR #101 RQ7、[../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。 | A3 known set、A5 计算协议。 | 本文实现 complete coverage。 |
| C12 | 成本效率 | 🟡 | 论文计划记录 agent time、token / API cost、人工审计时间、challenge 成本和修正成本。 | PR #101 RQ4、B0 baseline 对成本差异和人工复核成本的提醒。 | A4 运行记录、A5 cost analysis。 | 智能体一定显著降低总成本；challenge loop 免费。 |
| C13 | 与 P0 强近邻差异 | 🟡 | 已有 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 等强近邻；本文差异只能收窄为 SE SLR/SMS 中 researcher-instantiated meta-model、finding pattern、finding-level evidence chain 与 challenge loop 的组合。 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、各单篇 `review.md`。 | A1/A6 related-work 深化、PDF 图表核对、artifact audit。 | prior work 没有 agentic SLR / HITL / provenance / evidence synthesis。 |
| C14 | SE 社区已有 LLM-SLR 风险讨论 | 🟢 | WSESE@ICSE 2025 已讨论在 SE 中使用 LLM 支持 SLR conducting / replication 的困难；本文应把 prompt 敏感性、随机性、模型漂移、成本、透明性和数据仓库缺口转成方法与评价义务。 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、[wsese review](../baselines/papers/wsese-difficulties-replicating-slr-llms-se/review.md)。 | A1/A6 related-work 写作；必要时核对 PDF。 | SE 社区尚未讨论 LLM-assisted SLR difficulties。 |
| C15 | 完整自动化 / 全生命周期 | 🔴 | 只能写“覆盖后续实验中明确定义的阶段子集，并将未覆盖环节列为 limitation”。 | B0 baseline 已发现多个多阶段 pipeline；PR-S0 不实现 runtime。 | 若未来声称生命周期覆盖，必须逐阶段 schema、运行、评价和 limitation 闭合。 | fully automated SLR；complete lifecycle automation；end-to-end qualified SLR。 |
| C16 | 首创性 | 🔴 | 只能写“面向 finding-centered audit 与 researcher challenge 的研究”，不能写首次。 | 已知 ASReview、RobotReviewer、review automation、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、survey generation 等近邻。 | 若未来要写 novelty，必须经 systematic related-work gate。 | first automated SLR；first agentic SLR；first LLM-based systematic review。 |
| C17 | 专家替代 | 🔴 | 本文保留 researcher ownership 和 human audit gates，研究人机分工。 | 导师定调与 PR-S0 story。 | 不适用。 | 智能体完全替代 SLR 专家；researcher 只做最终润色。 |

## 3. 摘要 / 引言安全句式

可以作为后续英文稿前的中文安全句式：

1. 本文研究如何让 researcher 在 SE SLR/SMS 中显式化 review frame，并让智能体在该 frame 下提出可审计的 candidate findings。
2. 本文不把报告生成视为核心贡献；报告只是 accepted / downgraded / unresolved findings 的下游投影。
3. 本文以 finding-centered evidence package 为核心，要求每个 candidate finding 能追溯到 evidence objects、source anchors、supporting / counter evidence、challenge history 和 final status。
4. 本文把 PRISMA-style flow 和排除理由台账作为透明报告材料；禁止在 checklist 未闭合前声称 PRISMA-compliant。
5. 本文使用 coverage proxy 描述覆盖情况；禁止声称 complete coverage。

## 4. 后续更新规则

- PR #97 状态变化时必须更新 C3。
- A2 若冻结 meta-model / finding / challenge schema，必须更新 C4--C8。
- A3 若构造 scenarios、gold / silver facts 与 trap papers，必须更新 C9 / C11。
- A4/A5 若产生真实运行与指标，才能把 🟡 中部分主张升级为结果主张。
- A6 / Related Work 若新增 direct competitor，必须更新 C13--C16。
