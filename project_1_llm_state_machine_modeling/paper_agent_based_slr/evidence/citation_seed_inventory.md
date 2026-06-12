# Citation Seed Inventory

## 1. 目的

本文件登记 A0 阶段已知的相关工作和方法学入口。A0 已把可通过 DOI / 出版页 metadata 核验的核心条目写入 [references.bib](./references.bib)，但它仍不是最终论文 `references.bib`；后续 Related Work 写作必须继续补齐原文阅读、上下文定位和 A1 系统检索增量。

## 2. 来源优先级

引用和 BibTeX 获取优先级：

1. 出版商页面 / DOI / 官方 PDF。
2. 官方工具网站或官方 GitHub。
3. DBLP / arXiv / PubMed / PMC 等稳定索引。
4. Semantic Scholar / OpenAlex 等聚合入口。
5. 搜索摘要只能作为发现线索，不能作为事实依据。

## 3. Seed table

核验状态口径：🟢 = A0 已有可靠入口且核心元数据 / BibTeX 种子已入 [references.bib](./references.bib)；🟡 = 发现入口但仍需 BibTeX / 原文核验；🔴 = 不得作为事实依据。

| 方向 | 条目 | 状态 | 当前入口 | A0 可用法 | 后续要求 |
|---|---|---:|---|---|---|
| SE SLR 方法学 | Kitchenham & Charters 2007 SLR guideline | 🟡 | <https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf> | 方法学背景。 | A1 需补技术报告权威元数据；A0 不把该 PDF 当最终出版来源。 |
| Systematic mapping | Petersen et al. 2008 | 🟢 | <https://doi.org/10.14236/ewic/EASE2008.8> / <https://dl.acm.org/doi/10.5555/2227115.2227123> | SMS 背景。 | BibTeX seed 已入 [references.bib](./references.bib)；A1 继续读原文。 |
| Systematic mapping | Petersen et al. 2015 | 🟢 | <https://doi.org/10.1016/j.infsof.2015.03.007> | mapping guideline。 | BibTeX seed 已入 [references.bib](./references.bib)；A1 继续读原文。 |
| PRISMA | PRISMA 2020 statement | 🟢 | <https://www.prisma-statement.org/prisma-2020-statement> / <https://doi.org/10.1136/bmj.n71> | 透明报告参考。 | BibTeX seed 已入 [references.bib](./references.bib)；仅支持 PRISMA-style / informed，不能支持合规 claim。 |
| PRISMA | PRISMA 2020 explanation and elaboration | 🟢 | <https://www.prisma-statement.org/prisma-2020-explanation-elaboration> / <https://doi.org/10.1136/bmj.n160> | checklist 解释。 | BibTeX seed 已入 [references.bib](./references.bib)；A5 才能决定 checklist 口径。 |
| Screening automation | ASReview | 🟢 | <https://www.nature.com/articles/s42256-020-00287-7> / <https://asreview.nl/> / <https://github.com/asreview/asreview> | 主动学习筛选近邻。 | BibTeX seed 已入 [references.bib](./references.bib)；A1 继续核验工具版本。 |
| Evidence automation | RobotReviewer | 🟢 | <https://pubmed.ncbi.nlm.nih.gov/26104742/> / <https://pmc.ncbi.nlm.nih.gov/articles/PMC4713900/> / <https://doi.org/10.1093/jamia/ocv044> / <https://doi.org/10.18653/v1/P17-4002> / <https://www.robotreviewer.net/> | clinical trials / biomedical evidence synthesis 自动化边界。 | JAMIA evaluation 与 ACL system demo 的 BibTeX seed 已入 [references.bib](./references.bib)。 |
| Review automation | Marshall & Wallace 2019 practical guide | 🟢 | <https://doi.org/10.1186/s13643-019-1074-9> | 自动综述实践边界。 | BibTeX seed 已入 [references.bib](./references.bib)；A1 继续读原文定位工具谱系。 |
| LLM-assisted SLR | LLM screening / extraction / synthesis 近两年工作 | 🟡 | 待 A1 系统检索 | 只能写“待调研”。 | A1 / related-work PR 补齐。 |
| SE tertiary study | SE 领域自动化综述 / tertiary study | 🟡 | 待 A1 系统检索 | 只能写“待调研”。 | A1 / related-work PR 补齐。 |

## 4. 禁止用法

- 不得用搜索摘要作为正文事实来源。
- 不得把 🟡 条目写成已核验引用。
- 不得在未读原文或可靠 metadata 前拼造 BibTeX；A0 [references.bib](./references.bib) 只收录已从 DOI / 出版页 metadata 获取的种子。
- 不得把 ASReview / RobotReviewer 写成“无关”，它们必须进入 novelty boundary。
