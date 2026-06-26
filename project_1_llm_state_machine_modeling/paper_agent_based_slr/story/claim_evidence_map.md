# 主张-证据映射：S0-v2 智能体式 SLR 支持方法

## 1. 使用规则

本文件是第二篇论文 PR-S0-v2 阶段的主张审查门。任何摘要、引言、贡献、结论、PR body 或 PR comment 中的强主张，都必须先在本文件中找到对应的证据状态和安全写法。若后续实验或相关工作新增证据，本文件必须同步更新。

状态口径：

- 🟢：PR-S0-v2 可作为任务定义、方法设计或边界约束使用，但不能写成已验证结果。
- 🟡：方向合理，但需要后续 A2/A3/A5/A6 补证后才能写成论文主结论。
- 🔴：禁止主张，只能出现在风险、限制或禁止写法语境。
- 🟣：依赖 PR #97 OPEN / 未合入 / snapshot / 分支局部证据，不能写成 `main` fact。

最高优先级边界：PR-B0 baseline 已经发现 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻；2026-06-15 与 2026-06-26 导师讨论进一步确认，第二篇不能写成“LLM/agent 自动完成 SLR”，而应写成 **researcher-guided、pattern-evolving、evidence-backed、finding-oriented agentic SLR support approach**。

## 2. 主张映射

| ID | 主张类型 | 状态 | 当前可写安全表述 | 当前证据 | 后续所需证据 | 禁止写法 |
|---|---|---:|---|---|---|---|
| C1 | 论文任务定义 | 🟢 | 本文研究一种面向 SE SLR/SMS 的研究者引导、模式演化、证据支撑、发现导向的智能体式支持方法：研究者定义 topic / RQ / scope / meta-model，agent 只在研究者批准的 dimension schema 下辅助收集、抽取、统计和提出候选发现信号，final target-domain findings 必须由研究者裁决。 | [paper_story.md](./paper_story.md)、[protocol.md](./protocol.md)、[terminology_policy.md](./terminology_policy.md)、PR #112 与 PR #123 导师记录。 | A2 schema、A3 pilot 场景、A4/A5 运行与评价。 | 本文证明 agent 可端到端自动生成合格 SLR；本文首次提出 agentic SLR。 |
| C2 | 三阶段 SLR 实践 | 🟢 | 本文把真实 SLR 实践拆为论文收集、维度模式驱动的论文分析、统计分析与 research finding 形成，并分别设置人机分工和证据边界。 | 2026-06-26 导师记录；[paper_story.md](./paper_story.md)。 | A2/A3 把三层拆成可执行 schema 与 pilot 制品。 | SLR 只是文献摘要；本文直接自动生成最终 research findings。 |
| C3 | Dimension pattern lifecycle | 🟡 | 论文计划把 dimension pattern / extraction schema 作为一等制品，记录字段、取值、证据要求、缺失值语义、schema revision、impact analysis 与 backfill 状态。 | PR #123 导师记录；[protocol.md](./protocol.md) §4。 | survey-of-surveys scaffold、seed-paper dry-run、schema revision log、backfill burden。 | 维度 pattern 是一次性平铺字段表；agent 可自行改 schema 后继续运行。 |
| C4 | Survey-of-surveys scaffold | 🟡 | survey-of-surveys 只作为低成本 scaffold mining / pattern prior，用于识别常见 dimension / finding / evidence-presentation patterns；其 pattern 需经研究者采纳才进入 operative schema。 | 2026-06-26 导师原话；[protocol.md](./protocol.md) §7。 | 后续 scaffold PR 抽样 SE / AI4SE / MDE / LLM4SE surveys 并审计 pattern。 | survey-of-surveys 是目标 SLR evidence pool；本文完成 PRISMA tertiary review；survey-of-surveys 证明目标领域结论。 |
| C5 | Field-level content evidence | 🟡 | 字段值、统计分析和 target-domain findings 必须回到目标论文中的 section/page/quote/table/figure/artifact URL/缺失原因/不确定说明等 content evidence。 | [terminology_policy.md](./terminology_policy.md)、[protocol.md](./protocol.md) §2。 | A2 evidence object schema、A5 source-anchor 准确性与断链统计。 | 普通摘要即可支撑字段值；无 source anchor 的强主张可进入结论。 |
| C6 | Process evidence 边界 | 🟢 | process evidence / audit trail 只支撑 method-evaluation findings，如可用性、审计性、交互成本、失败模式；不能支撑目标领域 findings。 | 2026-06-26 导师记录中 pilot / 硕士生过程数据建议；[protocol.md](./protocol.md) §8。 | A5 ethics / consent / redaction / interaction-log 评价协议。 | 用学生交互日志证明某个 SE 领域研究现状；process evidence supports target-domain finding。 |
| C7 | Statistical analysis 与 finding 分层 | 🟢 | statistical analysis 只产生频次、分布、交叉表、趋势、覆盖代理和矛盾信号等统计观察；进入 research finding 前必须经过 finding heuristic、content evidence、反例检查、主张强度控制和研究者裁决。 | 2026-06-26 导师原话；[paper_story.md](./paper_story.md) §8；[protocol.md](./protocol.md) §5。 | A5 统计协议、candidate finding ledger、challenge/adjudication 记录。 | statistical analysis reveals final finding；频次表直接等于 research finding。 |
| C8 | Candidate finding signal / final finding 边界 | 🟢 | agent 只能生成 candidate finding signals；final target-domain finding 必须由 content evidence、counter-evidence、uncertainty、scope、claim strength 与研究者 final adjudication 共同确定。 | PR #112 与 PR #123 导师记录；[terminology_policy.md](./terminology_policy.md)。 | A2/A5 finding 状态机、accepted/downgraded/rejected/unresolved 记录。 | LLM / agent produces final findings；candidate signal 直接进入摘要或结论。 |
| C9 | Human-in-the-loop gate | 🟢 | researcher 不是末端 reviewer，而是在 G0 meta-model、G1 schema、G2 revision/backfill、G3 statistical protocol、G4 challenge、G5 final adjudication、G6 process evidence boundary 中持续拥有裁决权。 | 2026-06-26 导师原话；[protocol.md](./protocol.md) §6。 | A2 gate schema、A3/A5 gate dry-run 与成本记录。 | researcher merely validates final report；人工只负责最后润色。 |
| C10 | 透明报告材料 | 🟡 | 论文计划生成 claim-evidence map、排除理由、schema revision、audit log、类 PRISMA flow 等透明材料；它们是审计投影，不是自动生成最终论文。 | [paper_story.md](./paper_story.md)、[protocol.md](./protocol.md)。 | A2/A5 checklist、报告制品与人工核验。 | 本文 PRISMA-compliant；透明材料等于自动写作。 |
| C11 | Pilot run 边界 | 🟡 | pilot run 用于验证 L0--L7 闭环、制品完整性、schema/backfill 可操作性和 finding challenge 可执行性。 | 2026-06-26 导师建议；[paper_outline.md](./paper_outline.md)。 | A3 主题选择、A4/A5 run record 与制品审计。 | pilot 证明方法跨主题泛化；pilot 证明优于人工 SLR。 |
| C12 | 硕士生过程数据 | 🟡 | 后续硕士生使用数据可用于 method-evaluation：交互轮次、人工修改、拒绝建议、时间成本、理解难点、失败模式；必须处理 consent、匿名化、脱敏与教学关系隔离。 | 2026-06-26 导师建议；[reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。 | A5 ethics / data boundary / redaction protocol。 | 学生日志证明目标领域 research findings；无脱敏即可发布 raw prompt log。 |
| C13 | 与强近邻差异 | 🟡 | 已有工作覆盖多阶段 SLR automation、HITL、provenance、screening/extraction、evidence synthesis 和 survey generation；本文安全差异收敛为 SE SLR/SMS 中 researcher-defined meta-model、pattern-evolving dimension schema、field-level content evidence、statistical/finding separation、researcher challenge/adjudication 与 process-evidence-based method evaluation 的组合。 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、[differential_novelty_matrix.md](./differential_novelty_matrix.md)。 | A6 related work 深化、PDF 图表核对、制品审计。 | 已有工作没有 agentic SLR / HITL / provenance；本文是 first agentic SLR。 |
| C14 | SE 社区 LLM-SLR 风险讨论 | 🟢 | WSESE@ICSE 2025 已讨论 SE 中用 LLM 支持 SLR conducting / replication 的困难；本文应把 prompt 敏感、随机性、模型漂移、成本、透明性和数据仓库缺口转成方法与评价义务。 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、[WSESE review](../baselines/papers/wsese-difficulties-replicating-slr-llms-se/review.md)。 | A6 related work；必要时核对 PDF。 | SE 社区尚未意识到 LLM-assisted SLR difficulties。 |
| C15 | PR #97 资产角色 | 🟣 | PR #97 只提供 OPEN / 未合入 / snapshot / 分支局部证据线索；不能写成 `main` 已有文库。 | [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。 | PR #97 merge 或冻结 SHA 后复核。 | PR #97 25 篇全文文库已经合入 main。 |
| C16 | 完整自动化 / 全生命周期 | 🔴 | 只能写“覆盖后续实验中明确定义的阶段子集，并报告未覆盖环节为 limitation”。 | B0 强近邻与 PR-S0-v2 不实现 runtime。 | 若未来声称阶段覆盖，必须逐阶段 schema、运行、评价和 limitation 闭合。 | fully automated SLR；complete lifecycle automation；end-to-end qualified SLR。 |
| C17 | 首创性 | 🔴 | 只能写“面向研究者裁决、维度模式演化和发现形成审计的研究”，不能写首次。 | ASReview、RobotReviewer、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、survey generation 等。 | 若未来要写强新颖性，必须经 A6 related-work gate。 | first automated SLR；first agentic SLR；first LLM-based systematic review。 |

## 3. 摘要 / 引言安全句式

可以作为后续英文稿前的中文安全句式：

1. 本文研究如何让 SE SLR/SMS 中的研究者把 topic / RQ / scope / meta-model 显式转化为可执行、可修订、可审计的 dimension schema，并让 agent 在该 schema 下辅助抽取字段级内容证据。
2. 本文区分统计观察、候选发现信号和最终目标领域研究发现；agent 只能提出 candidate finding signals，final findings 必须经过研究者 challenge 与 adjudication。
3. 本文把 process evidence 用于评价方法自身的可用性、审计性、人机协同成本和失败模式，而不是替代目标论文 content evidence。
4. 本文不把报告生成视为核心贡献；报告只是已接受 / 已降级 / 未解决 findings 的透明投影。
5. 本文只生成类 PRISMA 透明材料；禁止在 checklist 未闭合前声称 PRISMA-compliant。

## 4. 禁止短语与 grep 线索

以下短语若出现在正向主张语境，至少应列为 I 级问题；若出现在摘要、贡献或结论，通常应列为 C 级问题：

- `first automated SLR`
- `first agentic SLR`
- `complete coverage`
- `PRISMA-compliant`
- `LLM final finding`
- `agent-generated final finding`
- `statistical finding`（除非明确说明不是 research finding）
- `process evidence supports target-domain finding`
- `student data shows field state`
- `pilot proves generalization`
- `tertiary review`（若指 survey-of-surveys scaffold）
- `fully automated SLR`

## 5. 后续更新规则

- PR #97 状态变化时必须更新 C15 与 [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。
- A2 若冻结 meta-model / dimension schema / finding ledger / gate schema，必须更新 C3--C10。
- A3 若构造 pilot 场景、金事实 / 银事实与陷阱论文，必须更新 C5/C7/C8/C11。
- A4/A5 若产生真实运行与指标，才能把 🟡 中部分主张升级为结果主张。
- A6 / related work 若新增直接竞争工作，必须更新 C13--C17。
