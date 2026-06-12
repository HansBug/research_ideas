# baselines/SUMMARY.md：A0 对照总账

状态口径：🟢 = A0 已有可靠入口和 BibTeX / DOI 级元数据；🟡 = 已发现入口但待 A1 系统核验；🔴 = 不得作为事实依据。emoji 列只放 emoji。

## 1. A0 核心锚点

| 年份 | 方向 | 代表条目 | 状态 | 与本文关系 | 入口 |
|---:|---|---|---:|---|---|
| 2007 | SE SLR 方法学 | Kitchenham & Charters SLR guideline | 🟡 | 传统 SLR protocol / conduct / reporting 背景；技术报告元数据仍需 A1 复核。 | [citation_seed_inventory.md](../evidence/citation_seed_inventory.md) |
| 2008 | Systematic mapping | Petersen et al. systematic mapping | 🟢 | SMS 分类 / mapping 方法学锚点。 | [references.bib](../evidence/references.bib) |
| 2015 | Systematic mapping | Petersen et al. mapping guideline update | 🟢 | 更新版 SMS 指南。 | [references.bib](../evidence/references.bib) |
| 2015 | RobotReviewer | RobotReviewer bias assessment evaluation | 🟢 | clinical trials / risk-of-bias 自动化近邻。 | [references.bib](../evidence/references.bib) |
| 2017 | RobotReviewer | ACL system demonstration | 🟢 | 自动化 biomedical evidence synthesis 系统近邻。 | [references.bib](../evidence/references.bib) |
| 2019 | Review automation | Marshall & Wallace practical guide | 🟢 | systematic review automation landscape / 工具使用指南。 | [references.bib](../evidence/references.bib) |
| 2021 | PRISMA | PRISMA 2020 statement | 🟢 | 透明报告和 flow/exclusion ledger 参考，不是合规声明。 | [references.bib](../evidence/references.bib) |
| 2021 | PRISMA | PRISMA 2020 explanation and elaboration | 🟢 | checklist 解释和报告示例。 | [references.bib](../evidence/references.bib) |
| 2021 | ASReview | ASReview open-source ML framework | 🟢 | title / abstract screening 自动化近邻。 | [references.bib](../evidence/references.bib) |

## 2. A1 必须扩展的近邻

| 方向 | 状态 | A1 目标 | 风险 |
|---|---:|---|---|
| LLM-assisted screening | 🟡 | 系统检索近两年 LLM 辅助纳排决策论文。 | 不补会导致 novelty 边界不足。 |
| LLM-assisted extraction | 🟡 | 检索字段抽取、evidence locator、metadata extraction 相关论文。 | 不补会导致 factuality / extraction 评价缺少对照。 |
| LLM-assisted synthesis / related-work writing | 🟡 | 检索 LLM 证据综合、综述写作与幻觉评估工作。 | 不补会导致 unsupported claim 风险被低估。 |
| SE tertiary study / review automation | 🟡 | 检索 SE 内自动化综述、tertiary study 和 tool-supported SLR 经验。 | 不补会被 reviewer 质疑只看医学 / 通用工具。 |

## 3. 当前结论

A0 已能防止“first automated SLR”这类明显过强 claim，但还不能支撑完整 Related Work。A1 应把本文件扩展为可直接服务论文 §Related Work 的近邻矩阵，并将每个 🟡 方向收敛到可引用条目。
