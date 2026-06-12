# Differential Novelty Matrix：相关工作边界

## 1. 目的

关键词覆盖：systematic review automation、LLM-assisted screening / extraction / synthesis。

本文件冻结 A0 阶段的差异化 novelty gate。它不是完整 Related Work，也不声称已经排除所有 direct competitor；它用于明确禁止第二篇论文误写成 first automated SLR、PRISMA-compliant 工具或 `sources/` corpus paper。

## 2. 矩阵口径

| 方向 / 工具 | 覆盖环节 | 与本文关系 | 本文差异 | 不能 claim | A0 状态 |
|---|---|---|---|---|---|
| 软件工程 SLR 方法学 | planning、conducting、reporting | 本文的流程与规范基础。 | 本文研究如何把这些环节 agent 化并形成可审计 evidence package。 | 不能声称替代 SLR 方法学。 | 已登记 seed，待 A1/A5 深化。 |
| Systematic mapping studies | taxonomy、分类、领域覆盖统计 | 本文可能采用 mapping 场景作为 benchmark。 | 本文关注 agent workflow 与 auditability，而不是单次 mapping 结果。 | 不能把 mapping 结果本身写成 A0 贡献。 | 已登记 seed，待场景设计。 |
| PRISMA 2020 | 透明报告、流程图、排除理由 | 可作为 report transparency 参考。 | 本文只生成 PRISMA-style / PRISMA-informed 材料；合规性需 checklist 闭合。 | 不能写 PRISMA-compliant。 | 已登记官方入口。 |
| ASReview | 主动学习 / ML 辅助筛选 | 重要近邻，尤其 title / abstract screening。 | 本文关注多阶段 agent workflow、claim-to-source evidence package、human audit gates 和幻觉控制，不只做筛选排序。 | 不能写 ASReview 不属于自动化综述；不能写本文首次辅助筛选。 | 已登记 Nature / official / GitHub 入口。 |
| RobotReviewer | clinical trials / risk-of-bias 自动化 | 跨域重要近邻，代表特定证据抽取 / 偏倚风险自动化。 | 本文不是单一 risk-of-bias 分类器，也不是 clinical trials 同域工具；本文关注 SE SLR / mapping 多环节证据包。 | 不能把 RobotReviewer 写成 SE SLR 同域直接 competitor；不能忽略它说明自动化早已有之。 | 已登记 PubMed / PMC / DOI / 官网入口。 |
| Systematic review automation practical guide | 机器学习辅助证据综合实践 | 方法学边界与自动化 landscape。 | 本文需在该谱系内定位 agent / LLM 工作流的审计机制。 | 不能写首次自动化 SLR。 | 已登记 DOI 入口。 |
| LLM-assisted screening | LLM 用于 title / abstract 筛选 | 近邻任务。 | 本文不只评估筛选准确率，还记录筛选理由、审计状态和下游 claim 影响。 | 不能把所有 LLM screening 工作说成无审计。 | 待 A1 系统检索。 |
| LLM-assisted extraction | LLM 抽取字段、证据、metadata | 近邻任务。 | 本文要求 evidence locator、uncertain、negative evidence 和 audit gate。 | 不能声称 LLM 抽取从未用于综述。 | 待 A1 系统检索。 |
| LLM-assisted synthesis | LLM 生成 summary / related work / evidence synthesis | 高风险近邻。 | 本文要求 claim-evidence map 和 unsupported claim 检查，限制无来源综合。 | 不能写 LLM synthesis 本身就是本文 novelty。 | 待 A1 系统检索。 |
| 本仓库 `sources/` 文库 | 控制系统 STM domain asset | 可作为真实 case / stress test。 | 本文贡献不是文库规模，而是 agent-based SLR workflow 如何审计此类文献证据链。 | 不能写 `sources` corpus paper 是主线。 | `main` 已有，需 A1 复核总账。 |
| PR #97 baseline 文库 | OPEN / 未合入 / snapshot 证据线索 | 可作为 related-work screening / fulltext extraction 的案例。 | 必须按 snapshot evidence 使用，不能升级为 `main` fact。 | 不能写 PR #97 资产已合入。 | 🟣 分支局部，待 A1。 |

## 3. 最低 related-work gate

A0 后续任何 story / outline 若要写 novelty，必须至少回答：

1. 与传统 SE SLR / SMS 方法学的关系是什么？
2. 本文为什么只写 PRISMA-style，并禁止写 PRISMA-compliant？
3. 与 ASReview 的筛选辅助差异是什么？
4. 与 RobotReviewer 这类特定证据自动化工具的差异是什么？
5. 与 review automation practical guide 的关系是什么？
6. 与 LLM-assisted screening / extraction / synthesis 的差异是什么？
7. `sources/` 和 PR #97 是 evidence source 还是论文主贡献？

## 4. 禁止 novelty 写法

- 禁止写 first automated SLR。
- 禁止写 prior work 只做人工综述、没有自动化。
- 禁止写 ASReview / RobotReviewer 与本文无关。
- 禁止写 PRISMA-compliant。
- 禁止把 PR #97 OPEN / 未合入 snapshot 当成已合入 dataset。

## 5. A1 待补

A1 或相关 related-work PR 应继续补：

1. SE 领域 LLM-assisted SLR / SMS / tertiary study 近两年工作。
2. LLM screening / extraction / summarization 的实证评估。
3. Human-in-the-loop / auditability / provenance for evidence synthesis。
4. 自动综述工具的功能覆盖矩阵。
