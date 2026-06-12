# baselines/GUIDE.md：自动化综述近邻对照规则

## 1. 目标

本目录用于支撑第二篇 agent-based SLR 论文的 Related Work 与 reviewer challenge。后续新增条目时，应判断它与本文在以下维度上的关系：覆盖环节、是否 human-in-the-loop、是否生成可审计 evidence package、是否显式评估 factuality / hallucination、是否适用于 SE SLR / systematic mapping。

## 2. 纳入范围

优先纳入：

1. 软件工程 SLR / systematic mapping 方法学基线。
2. PRISMA / 透明报告规范。
3. ASReview、RobotReviewer 等综述自动化工具或系统。
4. systematic review automation 的方法学或实践指南。
5. LLM-assisted screening / extraction / evidence synthesis / related-work writing 的实证研究。

暂不纳入：

1. 只生成普通摘要、没有 SLR / SMS 任务语境的泛化 LLM 写作工具。
2. 没有论文、官方文档或可核验仓库入口的宣传性网页。
3. 不能帮助界定本文 novelty 或评估边界的远距离工具。

## 3. 核验口径

状态列只写 emoji：🟢 = A0 已有可靠入口和 BibTeX / DOI 级元数据；🟡 = 已发现入口但待 A1 系统核验；🔴 = 不得作为事实依据。

每条正式对照至少要记录：标题、年份、类型、入口、与本文关系、不能 claim 的边界。涉及 DOI 的条目优先从 DOI / Crossref / 出版页获取 BibTeX；若命令行 `curl` 因 WAF / 403 失败但浏览器或 DOI metadata 可解析，应记录访问异常而不是断言来源不存在。

## 4. 写作禁令

- 不得写“本文是 first automated SLR”。
- 不得写 ASReview / RobotReviewer 与本文无关。
- 不得把 PRISMA-style 写成 PRISMA-compliant。
- 不得把 LLM-assisted synthesis 本身写成本论文 novelty；本文 novelty 必须落在 evidence package、traceability 与 human audit gates。
