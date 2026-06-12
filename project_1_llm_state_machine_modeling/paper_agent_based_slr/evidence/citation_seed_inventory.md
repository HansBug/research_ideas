# Citation Seed Inventory

## 1. 目的

本文件登记 A0 阶段已知的相关工作和方法学入口。它不是最终 `references.bib`，也不意味着所有条目已完成 BibTeX 核验。后续 Related Work 写作必须补齐 authoritative metadata。

## 2. 来源优先级

引用和 BibTeX 获取优先级：

1. 出版商页面 / DOI / 官方 PDF。
2. 官方工具网站或官方 GitHub。
3. DBLP / arXiv / PubMed / PMC 等稳定索引。
4. Semantic Scholar / OpenAlex 等聚合入口。
5. 搜索摘要只能作为发现线索，不能作为事实依据。

## 3. Seed table

核验状态口径：🟢 = 已有可靠入口可继续核验；🟡 = 发现入口但仍需 BibTeX / 原文核验；🔴 = 不得作为事实依据。

| 方向 | 条目 | 状态 | 当前入口 | A0 可用法 | 后续要求 |
|---|---|---:|---|---|---|
| SE SLR 方法学 | Kitchenham & Charters 2007 SLR guideline | 🟢 | <https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf> | 方法学背景。 | 获取完整 BibTeX / 技术报告元数据。 |
| Systematic mapping | Petersen et al. 2008 | 🟢 | <https://doi.org/10.14236/ewic/EASE2008.8> / <https://dl.acm.org/doi/10.5555/2227115.2227123> | SMS 背景。 | 核验 DOI / venue / BibTeX。 |
| Systematic mapping | Petersen et al. 2015 | 🟢 | <https://doi.org/10.1016/j.infsof.2015.03.007> | mapping guideline。 | 核验 BibTeX。 |
| PRISMA | PRISMA 2020 statement | 🟢 | <https://www.prisma-statement.org/prisma-2020-statement> / <https://doi.org/10.1136/bmj.n71> | 透明报告参考。 | 核验 BMJ BibTeX。 |
| PRISMA | PRISMA 2020 explanation and elaboration | 🟢 | <https://www.prisma-statement.org/prisma-2020-explanation-elaboration> / <https://doi.org/10.1136/bmj.n160> | checklist 解释。 | 核验 BMJ BibTeX。 |
| Screening automation | ASReview | 🟢 | <https://www.nature.com/articles/s42256-020-00287-7> / <https://asreview.nl/> / <https://github.com/asreview/asreview> | 主动学习筛选近邻。 | 核验 paper / tool 版本。 |
| Evidence automation | RobotReviewer | 🟢 | <https://pubmed.ncbi.nlm.nih.gov/26104742/> / <https://pmc.ncbi.nlm.nih.gov/articles/PMC4713900/> / <https://www.robotreviewer.net/> | clinical risk-of-bias 自动化边界。 | 明确 clinical-domain origin。 |
| Review automation | Marshall & Wallace 2019 practical guide | 🟢 | <https://doi.org/10.1186/s13643-019-1074-9> | 自动综述实践边界。 | 核验 BibTeX。 |
| LLM-assisted SLR | LLM screening / extraction / synthesis 近两年工作 | 🟡 | 待 A1 系统检索 | 只能写“待调研”。 | A1 / related-work PR 补齐。 |
| SE tertiary study | SE 领域自动化综述 / tertiary study | 🟡 | 待 A1 系统检索 | 只能写“待调研”。 | A1 / related-work PR 补齐。 |

## 4. 禁止用法

- 不得用搜索摘要作为正文事实来源。
- 不得把 🟡 条目写成已核验引用。
- 不得在未读原文或可靠 metadata 前拼造 BibTeX。
- 不得把 ASReview / RobotReviewer 写成“无关”，它们必须进入 novelty boundary。
