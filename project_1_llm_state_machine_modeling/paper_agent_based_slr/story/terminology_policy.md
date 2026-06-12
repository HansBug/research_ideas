# 术语策略：agent-based SLR 论文

## 1. 目的

本文术语容易与传统 SLR、systematic mapping、PRISMA reporting、自动筛选工具、LLM 生成综述文本混淆。本文件冻结 A0 阶段的术语口径，后续写 abstract、introduction、method、protocol、evaluation 或 PR comment 时应优先遵守。

## 2. 推荐术语

| 术语 | 推荐口径 | 避免误读 |
|---|---|---|
| agent-based SLR | 将 SLR / systematic mapping 多个环节组织成 agent-executed workflow，并设置 human audit gates。 | 不等于端到端无人自动 SLR。 |
| agent-executed workflow | agent 执行或辅助 query、screening、extraction、coding、synthesis、reporting，并写出 evidence package。 | 不等于单个 prompt 或单次 LLM response。 |
| human audit gate | 人类在 protocol approval、gold / silver audit、disagreement adjudication、final claim review 的显式审计节点。 | 不等于人工全文重做所有 SLR 环节。 |
| SLR | 围绕明确 RQ 系统识别、筛选、评价、抽取和综合证据的方法。 | 不等于普通 narrative review。 |
| systematic mapping | 更偏分类、taxonomy、覆盖分布和领域结构刻画。 | 不等于完整效果综合或 meta-analysis。 |
| evidence package | 包含 query log、screening ledger、extraction、coding、claim-evidence map、报告草案和审计状态的可复核制品。 | 不等于普通运行日志。 |
| traceability | 每个报告级 claim 能追溯到论文、检索、筛选、抽取、编码、证据定位与审计状态。 | 不等于只在文末放参考文献。 |
| provenance | 记录数据、全文、metadata、query、run、人工审计的来源和版本。 | 不等同于最终 claim 正确性。 |
| auditability | 第三方能复查流程、证据链、分歧、失败与修正。 | 不等于完全自动验证正确。 |
| factuality | 抽取字段、引用、venue、DOI、结论与来源事实一致。 | 不等于研究问题已被完整回答。 |
| hallucination | 生成不存在论文、错误引用、错误事实或无证据 claim 的问题统称。 | 应进一步分类，不要只泛泛写幻觉。 |
| unsupported claim | 没有可定位来源、抽取记录或审计状态支撑的 claim。 | 可能不是编造，但仍不可进入强结论。 |
| gold fact | 人工高置信核验或官方来源确认的事实锚点。 | 不等于完整 oracle。 |
| silver fact | 由可信 metadata、全文证据或半自动核验形成但仍需抽检的事实。 | 不等于可无条件作为最终真值。 |
| coverage proxy | known-item recall、seed recovery、database overlap 等覆盖代理。 | 禁止把它写成真实 recall 或 complete coverage。 |

## 3. PRISMA 相关术语

| 术语 | 使用规则 |
|---|---|
| PRISMA-compliant | 禁止在 A0 / 未闭合 checklist 前使用为正向 claim；只能出现在禁止 claim 或风险语境中。 |
| PRISMA-style | 可用于描述类似 PRISMA flow、排除理由台账、透明报告材料，但必须说明不是合规声明。 |
| PRISMA-informed | 可用于说明设计受 PRISMA 透明报告思想启发，但不替代 checklist。 |

## 4. 禁止或高风险写法

| 写法 | 处理 |
|---|---|
| agent 完全替代 SLR 专家 | 禁止 claim。 |
| 端到端无人自动产出合格 SLR | 禁止 claim。 |
| first automated SLR | 禁止 claim；已有 ASReview、RobotReviewer、review automation 等相关工作。 |
| complete coverage | 禁止 claim；只能报告 coverage proxy。 |
| PRISMA-compliant | 未完成 checklist 前禁止作为正向 claim。 |
| `sources/` corpus paper | 禁止作为第二篇主线；只能作为 case / scenario / evidence source。 |
| PR #97 已合入资产 | 禁止，除非 PR #97 状态变化并经 fact drift policy 更新。 |

## 5. 中文写作要求

正式 Markdown 说明以中文为主。必要英文术语可以保留，但应配中文解释；不要整段英文堆叠。论文后续英文稿另行维护，不在 A0 阶段生成。

## 6. PR #97 术语口径

PR #97 当前必须称为 OPEN / 未合入 / snapshot / branch-local evidence。除非后续 PR #97 merge 并按 [fact_drift_policy.md](../evidence/fact_drift_policy.md) 更新，否则不得称为 main 已合入资产。
