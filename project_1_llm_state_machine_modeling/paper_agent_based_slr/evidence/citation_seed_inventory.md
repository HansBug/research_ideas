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
| SE SLR 方法学 | Kitchenham & Charters 2007 SLR guideline | 🟢 | [../survey_of_surveys/papers/kitchenham-charters-2007-slr-guidelines/review.md](../survey_of_surveys/papers/kitchenham-charters-2007-slr-guidelines/review.md) | A1 已全文文本级 dry-run；方法学背景。 | 技术报告不是 peer-reviewed venue，正式写作需说明来源性质。 |
| Systematic mapping | Petersen et al. 2008 | 🟡 | [../survey_of_surveys/papers/petersen-2008-systematic-mapping/review.md](../survey_of_surveys/papers/petersen-2008-systematic-mapping/review.md) | SMS 背景；A1 已保留 metadata-only 和人工下载清单。 | PDF 未自动获取，A2a 优先补全文后再抽取模式。 |
| Systematic mapping | Petersen et al. 2015 | 🟡 | [../survey_of_surveys/papers/petersen-2015-mapping-guidelines-update/review.md](../survey_of_surveys/papers/petersen-2015-mapping-guidelines-update/review.md) | mapping guideline update；A1 已保留 metadata-only 和人工下载清单。 | PDF 未自动获取，A2a 优先补全文后再抽取模式。 |
| PRISMA | PRISMA 2020 statement | 🟢 | <https://www.prisma-statement.org/prisma-2020-statement> / <https://doi.org/10.1136/bmj.n71> | 透明报告参考。 | BibTeX seed 已入 [references.bib](./references.bib)；仅支持 PRISMA-style / informed，不能支持合规 claim。 |
| PRISMA | PRISMA 2020 explanation and elaboration | 🟢 | <https://www.prisma-statement.org/prisma-2020-explanation-elaboration> / <https://doi.org/10.1136/bmj.n160> | checklist 解释。 | BibTeX seed 已入 [references.bib](./references.bib)；A5 才能决定 checklist 口径。 |
| Screening automation | ASReview | 🟢 | <https://www.nature.com/articles/s42256-020-00287-7> / <https://asreview.nl/> / <https://github.com/asreview/asreview> | 主动学习筛选近邻。 | BibTeX seed 已入 [references.bib](./references.bib)；A1 继续核验工具版本。 |
| Evidence automation | RobotReviewer | 🟢 | <https://pubmed.ncbi.nlm.nih.gov/26104742/> / <https://pmc.ncbi.nlm.nih.gov/articles/PMC4713900/> / <https://doi.org/10.1093/jamia/ocv044> / <https://doi.org/10.18653/v1/P17-4002> / <https://www.robotreviewer.net/> | clinical trials / biomedical evidence synthesis 自动化边界。 | JAMIA evaluation 与 ACL system demo 的 BibTeX seed 已入 [references.bib](./references.bib)。 |
| Review automation | Marshall & Wallace 2019 practical guide | 🟢 | <https://doi.org/10.1186/s13643-019-1074-9> | 自动综述实践边界。 | BibTeX seed 已入 [references.bib](./references.bib)；A1 继续读原文定位工具谱系。 |
| LLM-assisted SLR | LLM screening / extraction / synthesis 近两年工作 | 🟢 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md) | PR-B0 已完成近邻 baseline 文库；A1 不重复该方向。 | 正式 Related Work 仍需回到单篇 baseline `review.md` 核验。 |
| SE tertiary study | Kitchenham et al. 2009 | 🟢 | [../survey_of_surveys/papers/kitchenham-2009-slr-tertiary/review.md](../survey_of_surveys/papers/kitchenham-2009-slr-tertiary/review.md) | A1 已全文文本级 dry-run。 | 正式写作前核对 PDF 表格与页码。 |
| SE tertiary study | da Silva et al. 2011 | 🟢 | [../survey_of_surveys/papers/da-silva-2011-six-years-slr/review.md](../survey_of_surveys/papers/da-silva-2011-six-years-slr/review.md) | A1 已全文文本级 dry-run。 | 正式写作前核对 PDF 表格与页码。 |
| SE tertiary study | Kotti et al. 2023 ML4SE tertiary study | 🟢 | [../survey_of_surveys/papers/ml4se-tertiary-study/review.md](../survey_of_surveys/papers/ml4se-tertiary-study/review.md) | A1 已全文文本级 dry-run。 | A2a 深读 RQ、threats 与分类表。 |
| Requirements Engineering tertiary study | Bano et al. 2014 | 🟢 | [../survey_of_surveys/papers/re-tertiary-study-2014/review.md](../survey_of_surveys/papers/re-tertiary-study-2014/review.md) | A1 已全文文本级 dry-run。 | A2a 深读质量评价表。 |
| Agile RE SMS | Heikkilä et al. 2015 | 🟢 | [../survey_of_surveys/papers/re-agile-sms-2015/review.md](../survey_of_surveys/papers/re-agile-sms-2015/review.md) | A1 已全文文本级 dry-run。 | 需核对出版社版本与表格。 |
| App reviews SLR | Martin et al. 2022 | 🟡 | [../survey_of_surveys/papers/app-reviews-slr-se/review.md](../survey_of_surveys/papers/app-reviews-slr-se/review.md) | 本轮未获取 PDF；进入人工下载清单。 | A2a 优先补全文。 |
| SE tertiary study | 更多 SE 领域自动化综述 / tertiary study | 🟡 | 待 A2a/A2b 扩展 | A1 已完成种子 dry-run，但不构成完整文库。 | A2a / A2b 补齐。 |

## 4. 禁止用法

- 不得用搜索摘要作为正文事实来源。
- 不得把 🟡 条目写成已核验引用。
- 不得在未读原文或可靠 metadata 前拼造 BibTeX；A0 [references.bib](./references.bib) 只收录已从 DOI / 出版页 metadata 获取的种子。
- 不得把 ASReview / RobotReviewer 写成“无关”，它们必须进入 novelty boundary。
