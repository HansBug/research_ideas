# 术语策略：agent-based SLR 论文

## 1. 目的

本文术语容易与传统 SLR、systematic mapping、PRISMA reporting、自动筛选工具、LLM 生成综述文本混淆。本文件冻结 A0 / PR-S0 阶段的术语口径，后续写 abstract、introduction、method、protocol、evaluation 或 PR comment 时应优先遵守。

## 2. 推荐术语

| 术语 | 推荐口径 | 避免误读 |
|---|---|---|
| agent-based SLR | 将 SLR / systematic mapping 的多个环节组织成 agent-executed workflow，并设置 human audit gates。 | 不等于端到端无人自动 SLR。 |
| researcher-guided agentic SLR support workflow | researcher 基于 review meta-model scaffold 裁剪并实例化 topic-specific review meta-model，再让 agent 在该框架下提出 candidate findings 并接受审计。 | 不等于系统自动定义最终研究结论。 |
| review meta-model scaffold | 帮助 researcher 声明 / 裁剪 review objects、relations、evidence fields、finding types、scope constraints 的可配置模板。 | 不是 UML/MDE 意义上的完整 metamodel；不是作者预设的 universal SE ontology。 |
| topic-specific review meta-model | researcher 针对具体 SLR/SMS 主题实例化后的工作模型。 | 不是 LLM 自动最终决定的 schema。 |
| researcher-approved executable schema | 由系统辅助生成、经 researcher 确认后供 agent 执行的字段和约束。 | 不是自动编译出的不可审计黑箱规则。 |
| evidence object | 从论文中抽取、带 source anchor 的可复核证据单元。 | 不是普通摘要或模型自由总结。 |
| finding pattern scaffold | 约束 candidate finding 类型、结构和证据要求的模式集合。 | 不保证 finding 为真，只约束候选发现生成。 |
| candidate finding | agent 基于 evidence objects 和 finding patterns 提出的候选研究发现。 | 不能直接写成 final finding。 |
| final finding | researcher 接受 claim strength、scope、supporting/counter evidence 后确认的 finding。 | 不是 LLM 输出后的默认状态。 |
| researcher audit | researcher 对 schema、evidence chain、candidate finding、claim strength 的显式审计。 | 不等于最后润色报告。 |
| researcher challenge loop | researcher 对 candidate finding 发起质疑，系统补证、找反例、修订或降级的闭环。 | 不要求 PR-S0 实现 UI，但必须作为方法闭环。 |
| claim strength | finding 的主张强度等级，由 evidence 与 researcher audit 决定。 | 不是 LLM confidence。 |
| agent-executed workflow | agent 执行或辅助 query、screening、extraction、coding、finding proposal、evidence-chain construction、report projection。 | 不等于单个 prompt 或单次 LLM response。 |
| human audit gate | 人类在 protocol approval、meta-model approval、evidence audit、finding audit、final claim review 的显式审计节点。 | 不等于人工全文重做所有 SLR 环节。 |
| SLR | 围绕明确 RQ 系统识别、筛选、评价、抽取和综合证据的方法。 | 不等于普通 narrative review。 |
| systematic mapping | 更偏分类、taxonomy、覆盖分布和领域结构刻画。 | 不等于完整效果综合或 meta-analysis。 |
| evidence package | 围绕 candidate findings 组织的可复核证据制品，包括 evidence objects、source anchors、supporting / counter evidence、coding decisions、challenge logs、revision history 和 final status。 | 不等于普通运行日志。 |
| traceability | 每个报告级 claim 能追溯到论文、检索、筛选、抽取、编码、证据定位与审计状态。 | 不等于只在文末放参考文献。 |
| provenance | 记录数据、全文、metadata、query、run、人工审计的来源和版本。 | 不等同于最终 claim 正确性。 |
| auditability | 第三方能复查流程、证据链、分歧、失败与修正。 | 不等于完全自动验证正确。 |
| factuality | 抽取字段、引用、venue、DOI、结论与来源事实一致。 | 不等于研究问题已被完整回答。 |
| hallucination | 生成不存在论文、错误引用、错误事实或无证据 claim 的问题统称。 | 应进一步分类，不要只泛泛写幻觉。 |
| unsupported claim | 没有可定位来源、抽取记录或审计状态支撑的 claim。 | 可能不是编造，但仍不可进入强结论。 |
| gold fact | 人工高置信核验或官方来源确认的事实锚点。 | 不等于完整 oracle。 |
| silver fact | 由可信 metadata、全文证据或半自动核验形成但仍需抽检的事实。 | 不等于可无条件作为最终真值。 |
| coverage proxy | known-item recall、seed recovery、database overlap 等覆盖代理。 | 禁止把它写成真实 recall 或 complete coverage。 |

## 3. finding lifecycle 术语

| 术语 | 推荐口径 | 避免误读 |
|---|---|---|
| candidate | 处于候选状态、待审计的 finding 或 claim。 | 不是最终结论。 |
| challenged | researcher 已对证据、范围或主张强度提出质疑。 | 不是失败；只是进入复核。 |
| revised | 系统在 challenge 后补证、找反例或收窄 scope。 | 不是自动升级为 final。 |
| downgraded | finding 不能支撑原始强度，需弱化主张或缩小范围。 | 不是无价值；只是不能写强 claim。 |
| accepted | researcher 认可该 finding 及其 evidence chain。 | 只有此状态才可写成 final finding。 |
| unresolved | 证据不足或冲突过大，暂不进入结论。 | 不是错误；是审计结果的一种。 |

## 4. PRISMA 相关术语

| 术语 | 使用规则 |
|---|---|
| PRISMA-compliant | 禁止在 A0 / 未闭合 checklist 前使用为正向 claim；只能出现在禁止 claim 或风险语境中。 |
| PRISMA-style | 可用于描述类似 PRISMA flow、排除理由台账、透明报告材料，但必须说明不是合规声明。 |
| PRISMA-informed | 可用于说明设计受 PRISMA 透明报告思想启发，但不替代 checklist。 |

## 5. 禁止或高风险写法

| 写法 | 处理 |
|---|---|
| agent 完全替代 SLR 专家 | 禁止 claim。 |
| 端到端无人自动产出合格 SLR | 禁止 claim。 |
| first automated SLR | 禁止 claim；已有 ASReview、RobotReviewer、review automation 等相关工作。 |
| complete coverage | 禁止 claim；只能报告 coverage proxy。 |
| PRISMA-compliant | 未完成 checklist 前禁止作为正向 claim。 |
| `sources/` corpus paper | 禁止作为第二篇主线；只能作为 case / scenario / evidence source。 |
| PR #97 已合入资产 | 禁止，除非 PR #97 状态变化并经 fact drift policy 更新。 |
| AgentSLR / LatteReview / EviSearch / LR-Robot / TrialMind / WSESE@ICSE 2025 | 必须正面对齐的强近邻，不能写成与本文无关或仅做背景。 |
| LLM defines the review meta-model | 改为 system may suggest; researcher instantiates / approves. |
| generated findings | 若无 audit，必须写 candidate findings。 |
| final findings produced by agents | 禁止；final requires researcher audit。 |
| automated report generation as contribution | 降级为 downstream presentation。 |
| evidence chain proves truth | 改为 supports / challenges / scopes a finding。 |
| researcher merely validates final report | 改为 researcher owns meta-model and audits findings。 |

## 6. 中文写作要求

正式 Markdown 说明以中文为主。必要英文术语可以保留，但应配中文解释；不要整段英文堆叠。论文后续英文稿另行维护，不在 A0 / PR-S0 阶段生成。

## 7. PR #97 术语口径

PR #97 当前必须称为 OPEN / 未合入 / snapshot / branch-local evidence。除非后续 PR #97 merge 并按 [fact_drift_policy.md](../evidence/fact_drift_policy.md) 更新，否则不得称为 main 已合入资产。
