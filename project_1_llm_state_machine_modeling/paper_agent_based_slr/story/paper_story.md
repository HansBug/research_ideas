# Paper Story：带人工审计门的 agent-based SLR

## 1. Working title

候选中文标题：**面向软件工程证据综合的可审计 agent-based SLR 工作流与评价框架**。

候选英文标题只作为后续写作入口：**Toward Auditable Agent-Based Systematic Reviews in Software Engineering**。

标题边界：不得暗示端到端无人、完全自动、完整覆盖；禁止暗示 PRISMA-compliant。

## 2. Thesis

本文研究带人工审计门的 agent-based SLR：将软件工程 systematic literature review / systematic mapping 的检索、筛选、全文获取状态记录、抽取、编码、综合和报告环节组织成可审计的 agent-executed workflow，并用结论到来源的可追踪性、事实准确性、幻觉控制、筛选一致性、透明报告、覆盖代理、成本效率和人工审计通过率评价其可靠性。


## 2.1 Story 成熟度与更新策略

A0 的 story 是为了防止主线回滑和过强 claim 的 **v0 种子**，不是最终论文叙事。当前 thesis、contribution 和 outline 仍然偏保守、偏薄，属于有意留白：后续 A1 的 baseline / related-work 调研可能发现 LLM-based SLR、LLM-assisted screening / extraction / synthesis 或 agentic review workflow 的更近工作；A3 的场景设计、A4/A5 的真实运行结果也可能改变可主张的贡献强度、评价维度和 threat model。因此后续 PR 若新增证据或发现近邻打穿当前 novelty，必须同步更新本文档、[paper_outline.md](./paper_outline.md)、[claim_evidence_map.md](./claim_evidence_map.md)、[differential_novelty_matrix.md](./differential_novelty_matrix.md) 与 [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。

更新原则：宁可先把 story 写成可审计、可降级、可迭代的研究假设，也不要在 A0 阶段把它写成已被实验证明的最终结论。

## 3. Task Boundary

| 项 | A0 冻结口径 |
|---|---|
| 输入 | 研究主题、研究问题 seed、检索协议、数据库 / source scope、候选论文池、全文可获取性记录、抽取 / 编码 schema、人工审计政策。 |
| 输出 | 可审计 evidence package：query log、screening ledger、fulltext status、extraction table、coding decision、claim-evidence map、PRISMA-style flow / 透明报告草案、最终报告草案。 |
| 人的角色 | protocol approval、gold / silver fact audit、分歧裁决、final claim review。 |
| agent 的角色 | 执行或辅助检索、筛选、抽取、编码、综合、报告与证据链写出。 |
| 不属于 A0 | 真实 pipeline 实现、真实 LLM 运行、四个真实例子、最终评价指标公式、完整论文正文。 |
| 不属于本文强 claim | 禁止写完全替代 SLR 专家、端到端无人自动产出合格 SLR、PRISMA-compliant、complete coverage、first automated SLR。 |

## 4. Problem Gap

传统软件工程 SLR / systematic mapping 依赖高度人工的 protocol、search、screening、extraction、coding、synthesis 与 reporting 流程。已有自动化工具和实践指南已经覆盖部分环节，例如主动学习辅助筛选、特定证据抽取或风险评估、机器学习辅助综述自动化。当前缺口不是“没有任何自动化”，而是：**当 LLM / agent 被用于多环节证据综合时，如何把每一步变成可追踪、可复核、可审计、能被人工 gate 拦截错误的 evidence package**。

因此本文不主张发明 SLR，也不主张首次自动化 SLR；本文聚焦 agent 化之后的 **可靠性和审计性问题**。

## 5. Technical Challenge

1. **多环节漂移**：检索、筛选、抽取、编码、综合每一步都可能引入 scope drift，单点正确不能保证最终报告可信。
2. **claim-to-source 断链**：报告级结论若不能回溯到论文元数据、筛选理由、抽取记录、证据定位和审计状态，就难以被复核。
3. **幻觉与无证据 claim**：LLM / agent 可能编造论文、误写 DOI / venue、误读全文、生成没有证据支撑的 gap 或 conclusion。
4. **覆盖不可直接证明**：真实 recall 往往不可知；禁止写 complete coverage，只能用 known-item recall、seed recovery、database overlap 等覆盖代理。
5. **人工审计成本与一致性**：human audit gates 能提升可靠性，但必须记录成本、分歧、裁决和剩余错误，而不是把人工审计当成黑箱兜底。

## 6. Method Insight

核心设计原则：**把 agent-based SLR 从“生成一篇综述文本”改写成“生成可审计证据包”**。

每个 agent 阶段都必须输出可复核中间产物；每个报告级 claim 都必须连接到来源、筛选、抽取、编码和审计状态；人工不是在最后润色文本，而是在 protocol approval、gold / silver audit、disagreement adjudication 和 final claim review 处形成显式 gate。

## 7. System / Method Stages

| 阶段 | 目标 | A0 证据包要求 |
|---|---|---|
| Protocol setup | 定义 RQ、scope、纳排、数据库入口 | protocol 草案、审计批准状态、版本日志。 |
| Query / search | 形成检索式并记录命中 | query log、检索日期、数据库、raw result、去重规则。 |
| Screening | title / abstract / metadata 纳排 | screening ledger、include / exclude reason、人工抽检状态。 |
| Fulltext status | 记录全文可用性与合法获取状态 | availability log、失败记录、用户提供全文标记。 |
| Extraction | 抽取字段与证据定位 | extraction table、locator、负证据、uncertain 标记。 |
| Coding | 给论文打标签或评分 | coding schema、决策理由、分歧与裁决。 |
| Synthesis | 形成跨论文矩阵与 gap | claim-evidence map、unsupported claim 检查。 |
| Reporting | 生成报告草案 | PRISMA-style flow、透明报告、threats、artifact checklist。 |

## 8. Contributions

A0 只冻结候选贡献，后续 A3/A5 必须用证据支持后才能进入摘要或引言。

| 候选贡献 | 当前状态 | 所需证据 |
|---|---|---|
| 带 human audit gates 的 agent-based SLR workflow | 方法设计候选 | A2 工作流合同、A4 运行骨架、A5 证据包审计结果。 |
| claim-to-source 不可断链 evidence package | 方法 / artifact 候选 | 断链率、证据定位错误率、无证据 claim 率。 |
| 面向幻觉与事实错误的审计协议 | 评价候选 | gold / silver fact、trap papers、人工审计日志。 |
| 多场景 benchmark / case study | 实证候选 | A3 场景设计、A4/A5 pilot 运行、覆盖代理。 |
| 与已有自动化工具的差异化定位 | related-work 候选 | differential novelty matrix 与已核验 citation seed。 |

## 9. Evidence Plan

| 证据类型 | 当前 A0 状态 | 后续落点 |
|---|---|---|
| 方法学依据 | 已登记 SLR / SMS / PRISMA / ASReview / RobotReviewer / review automation seed | A0 citation seed，A1/A5 扩充。 |
| `sources/` 文库 | `main` 已有，可作为 domain scenario 线索 | A1 资产盘点，A3 场景设计。 |
| PR #97 438→69→25 与 25 篇全文 | PR #97 OPEN / 未合入 / snapshot evidence | A1 merge 或冻结 SHA 后复核。 |
| agent workflow | A0 不实现 | A2/A4。 |
| 真实运行 | A0 不运行 | A3/A4/A5，真实 LLM 必须 `source .env`。 |
| 评价指标 | A0 只给维度种子 | A5 冻结公式、阈值、统计协议。 |

## 10. Related Work Positioning

本文应正面对齐以下方向：

1. 软件工程 SLR / SMS 方法学：本文继承 protocol、search、screening、extraction、synthesis、reporting 的基本规范。
2. PRISMA 透明报告：本文可生成 PRISMA-style 材料，但不得在 checklist 未闭合前写 PRISMA-compliant。
3. ASReview / 主动学习筛选：本文不是只优化筛选排序，而是关注多环节 agent workflow 与 evidence package。
4. RobotReviewer / 特定证据自动化：RobotReviewer 源于 clinical trials / risk-of-bias 自动化，本文应把它作为跨域自动化边界，而不是 SE 同域直接 competitor。
5. Systematic review automation practical guide：本文必须承认综述自动化已有成熟讨论，禁止写 first automated SLR。
6. LLM-assisted screening / extraction / synthesis：本文差异应落在可审计 evidence package、human audit gates 和幻觉 / fact drift 控制。

## 11. Claims to Make

这些 claim 只有在后续证据闭合后才能进入摘要 / 引言；A0 仅登记安全方向。

- 我们研究 agent-executed SLR / mapping workflow 的可审计性，而不是只生成综述文本。
- 我们把 human audit gates 显式放入 protocol approval、gold / silver audit、disagreement adjudication 和 final claim review。
- 我们以 claim-to-source traceability、factuality、hallucination、screening consistency、coverage proxy 和 cost-efficiency 评价可靠性。
- `sources/` 与 PR #97 可作为真实 case / evidence-package 场景，而不是论文主贡献本身。

## 12. Claims to Be Careful About

| 谨慎 claim | 风险 | 安全写法 |
|---|---|---|
| agent-based SLR workflow 有效 | 样本和场景不足时不能泛化 | 在若干 pilot scenarios 中观察 workflow 的可审计性和失败模式。 |
| 人工审计门能降低幻觉 | 需要审计日志和剩余错误统计 | 报告 audit interception 与 residual unsupported-claim rate。 |
| 覆盖较好 | 真实 recall 不可知 | 报告 known-item recall / seed recovery / overlap proxy。 |
| PRISMA-style report 可生成 | 不等于 checklist 合规 | 写“生成 PRISMA-style 透明材料”，不写合规。 |

## 13. Claims to Avoid

- 禁止写 agent 完全替代 SLR 专家。
- 禁止写端到端无人自动产出合格 SLR。
- 禁止写 PRISMA-compliant，除非后续 checklist 与 reporting 要求全部闭合。
- 禁止写 complete coverage 或 first automated SLR。
- 禁止把 PR #97 OPEN / 未合入资产写成 `main` 已有事实。
- 禁止把 `sources/` 文库规模写成论文 novelty 本身。
- 禁止把 A0 的评价维度种子写成 A5 已经验证的指标协议。

## 14. Reviewer Risks

核心风险已结构化记录在 [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。A0 阶段最高优先级风险包括：

1. novelty 被已有 SLR automation / ASReview / RobotReviewer / LLM-assisted review 工作打穿；
2. 方法像工程流水线而非 paper-level contribution；
3. 评价场景不足以支撑结论；
4. PR #97 事实漂移或资产版权边界不清；
5. audit gates 只作为口号，没有成本、分歧和剩余错误统计。
