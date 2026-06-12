# Claim-Evidence Map：agent-based SLR

## 1. 使用规则

本文件是第二篇论文 A0 阶段的 claim gate。任何 abstract、Introduction、contribution、Conclusion 或 PR comment 中的强主张，都必须先在本文件中找到对应的证据状态和安全写法。

状态口径：

- 🟢：A0 可作为任务定义 / 方法设计 claim 使用，但仍需避免结果化表述。
- 🟡：方向合理，但需要 A1-A5 补证后才能写成论文主结论。
- 🔴：禁止 claim，只能出现在风险、限制或禁止写法语境。
- 🟣：依赖 PR #97 OPEN / 未合入 / snapshot / 分支局部证据，不能写成 `main` fact。

## 2. Claim map

| ID | Claim 类型 | 状态 | 当前可写安全表述 | 当前证据 | 后续所需证据 | 禁止写法 |
|---|---|---:|---|---|---|---|
| C1 | 论文任务定义 | 🟢 | 本文研究带 human audit gates 的 agent-based SLR / systematic mapping workflow。 | PR #101、2026-06-12 导师讨论记录、A0 story。 | A2 工作流合同、A3 场景、A4/A5 运行与评价。 | 本文已经证明 agent 可端到端生成合格 SLR。 |
| C2 | `sources/` 资产角色 | 🟢 | `sources/` 可作为 domain scenario / stress test / evidence package 来源。 | `main` 已有 `sources/` 文库与导师定调。 | A1 资产盘点、A3 场景定义。 | `sources/` 文库规模本身就是第二篇论文 novelty。 |
| C3 | PR #97 资产角色 | 🟣 | PR #97 提供 OPEN / 未合入 / snapshot / 分支局部的 related-work screening 与全文抽取证据线索。 | [PR #97 comment](https://github.com/HansBug/research_ideas/pull/97#issuecomment-4682737117)、当前 OPEN 状态与 snapshot `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727`。 | A1 merge 或冻结 SHA 后复核。 | PR #97 25 篇全文文库已经是 `main` 已有正式资产。 |
| C4 | 可追踪 evidence package | 🟡 | 论文计划把 claim-to-source traceability 作为核心评价维度。 | PR #101 §5、A0 protocol。 | A2 schema、A4 写出器、A5 断链率 / 定位错误率统计。 | 我们已经实现每条 claim 完全可追踪。 |
| C5 | 幻觉控制 | 🟡 | 论文计划通过 gold / silver facts、trap papers 和 human audit gates 评估 unsupported claims。 | PR #101 §5.2、A0 protocol。 | A3 fact/trap set、A5 hallucination taxonomy 和残余错误统计。 | agent-based SLR 完全无幻觉。 |
| C6 | 人工审计门 | 🟡 | 人工审计门用于 protocol approval、抽样审计、分歧裁决和 final claim review。 | 导师定调、A0 protocol。 | A3/A5 审计日志、成本、分歧率、裁决记录。 | 人工审计门保证最终报告完全正确。 |
| C7 | 透明报告 | 🟡 | 论文计划生成 PRISMA-style flow、排除理由、协议偏离日志等透明报告材料。 | PR #101、A0 protocol。 | A2 schema、A5 checklist / report artifact。 | 禁止写本文 PRISMA-compliant。 |
| C8 | 覆盖代理 | 🟡 | 论文计划报告 known-item recall、seed recovery、database overlap 等 coverage proxy。 | PR #101 RQ7、A0 evaluation dimensions。 | A3 known set、A5 计算协议。 | 禁止写本文实现 complete coverage。 |
| C9 | 成本效率 | 🟡 | 论文计划记录 agent time、token / API cost、人工审计时间和修正成本。 | PR #101 RQ4、A0 evaluation dimensions。 | A4 run record、A5 cost analysis。 | agent 一定显著降低总成本。 |
| C10 | 与 ASReview 的差异 | 🟡 | ASReview 是重要筛选自动化近邻；本文关注多环节 evidence package 与 human audit gates。 | citation seed、novelty matrix。 | A0/A1 进一步核验 ASReview 文献与功能边界。 | ASReview 不能做系统综述自动化。 |
| C11 | 与 RobotReviewer 的差异 | 🟡 | RobotReviewer 源于 clinical trials / risk-of-bias 自动化，本文不是单一偏倚分类器。 | citation seed、novelty matrix。 | A0/A1 核验 RobotReviewer 论文和适用领域。 | RobotReviewer 是 SE SLR 同域直接 competitor。 |
| C12 | 首创性 | 🔴 | 只能写“面向可审计 agent workflow 与 evidence package 的研究”，不能写首次。 | 已知 ASReview、RobotReviewer、review automation。 | 若未来要写 novelty，必须经 systematic related-work gate。 | 禁止写本文是 first automated SLR。 |
| C13 | 专家替代 | 🔴 | 本文保留 human audit gates，研究人机分工。 | 导师定调与 A0 protocol。 | 不适用。 | 禁止写 agent 完全替代 SLR 专家。 |

## 3. 摘要 / 引言安全句式

可以作为后续英文稿前的中文安全句式：

1. 本文研究如何将软件工程 SLR / systematic mapping 的多阶段流程组织为可审计的 agent-executed workflow；禁止声称 agent 完全替代人类综述专家。
2. 本文以证据包为中心，要求报告级 claim 能追溯到检索、筛选、抽取、编码、证据定位和审计状态。
3. 本文把 PRISMA-style flow 和排除理由台账作为透明报告材料；禁止在 checklist 未闭合前声称 PRISMA-compliant。
4. 本文使用 coverage proxy 描述覆盖情况；禁止声称 complete coverage。

## 4. 后续更新规则

- A1 若合入或冻结 PR #97 snapshot，必须更新 C3。
- A2 若冻结 workflow schema，必须更新 C4 / C7。
- A3 若构造 gold / silver facts 与 trap papers，必须更新 C5 / C8。
- A4/A5 若产生真实运行与指标，才能把 🟡 中部分 claim 升级为结果 claim。
