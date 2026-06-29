# A1 检索日志

## 2026-06-29 02:08:00

本轮目的：为 PR-A1 `survey_of_surveys/` 建立 3--5 篇 dry-run，验证 README/GUIDE/SUMMARY/schema 是否能指导真实抽取。

| 查询 / 来源 | 结果 | 处理 |
|---|---|---|
| `Kitchenham Charters 2007 SLR guideline PDF` / Elsevier legacy file | 成功下载 `Guidelines for performing Systematic Literature Reviews in Software Engineering` PDF | 建立 [../papers/kitchenham-charters-2007-slr-guidelines/review.md](../papers/kitchenham-charters-2007-slr-guidelines/review.md)。 |
| `Systematic literature reviews in software engineering Kitchenham 2009 PDF` / Romi Satria Wahono mirror + DOI metadata | 成功下载 IST 2009 PDF | 建立 [../papers/kitchenham-2009-slr-tertiary/review.md](../papers/kitchenham-2009-slr-tertiary/review.md)。 |
| `Six years of systematic literature reviews in software engineering updated tertiary study PDF` / Romi Satria Wahono mirror + DOI metadata | 起初下载到投稿草稿；随后替换为 IST 2011 正式 PDF | 建立 [../papers/da-silva-2011-six-years-slr/review.md](../papers/da-silva-2011-six-years-slr/review.md)。 |
| `Systematic Mapping Studies in Software Engineering Petersen 2008 PDF` / SciSpace | 返回 HTML，不是 PDF；已删除伪 PDF | 作为 metadata-only 条目进入人工下载清单。 |
| `Petersen 2015 mapping guidelines update PDF` / DOI metadata | 本轮未自动下载 PDF | 作为 metadata-only 条目进入人工下载清单。 |
| `Machine Learning for Software Engineering: A Tertiary Study` / arXiv PDF + DOI metadata | 成功下载 arXiv PDF 并提取全文文本 | 建立 [../papers/ml4se-tertiary-study/review.md](../papers/ml4se-tertiary-study/review.md)。 |
| `Systematic Reviews in Requirements Engineering: A Tertiary Study` / UTS open PDF + DOI metadata | 成功下载 PDF 并提取全文文本 | 建立 [../papers/re-tertiary-study-2014/review.md](../papers/re-tertiary-study-2014/review.md)。 |
| `A Mapping Study on Requirements Engineering in Agile Software Development` / 作者课程镜像 PDF + DOI metadata | 成功下载 PDF 并提取全文文本 | 建立 [../papers/re-agile-sms-2015/review.md](../papers/re-agile-sms-2015/review.md)。 |
| `Analysing app reviews for software engineering` / Springer PDF URL + DOI metadata | URL 返回 HTML，`pdf_extractor` 报 `EOF marker not found`；已删除伪 PDF | 作为 metadata-only 条目进入人工下载清单。 |

## 当前检索边界

本轮是种子检索，不是 A2b 的完整闭合检索。A2a/A2b 需要继续扩展近年 SE SLR/SMS/survey、软件工程各子领域 survey 和最新 guideline / reporting checklist。


## 2026-06-29 16:30:00

本轮目的：按用户要求，把 issue [#95](https://github.com/HansBug/research_ideas/issues/95) 的 10 篇现代维度锚点纳入 A1 文库，用于加固 A1-M0--M6 元维度和现代 CCF-A/B 综述 / roadmap 样本覆盖。候选总表来自公开 Gist：<https://gist.github.com/HansBug/2310896ff4921f3d4809001571228820>；全文审计表包括 `issue95_fulltext_download_audit_438papers.csv` 和 `issue95_fulltext_structure_analysis_87papers.csv`。

| 条目 | DOI | 本轮公开 PDF 来源 | 处理 |
|---|---|---|---|
| On the road to interactive LLM-based systematic mapping studies | 10.1016/j.infsof.2024.107611 | https://bth.diva-portal.org/smash/get/diva2:1913976/FULLTEXT01 | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Research artifacts in secondary studies: A systematic mapping in software engineering | 10.1016/j.infsof.2025.107830 | https://arxiv.org/pdf/2504.12646 | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 10.1145/3809494 | https://arxiv.org/pdf/2507.03156 | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 10.1145/3807901 | https://arxiv.org/pdf/2410.06107 | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Large Language Models for Software Engineering: A Systematic Literature Review | 10.1145/3695988 | https://arxiv.org/pdf/2308.10620 | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Formal requirements engineering and large language models: A two-way roadmap | 10.1016/j.infsof.2025.107697 | https://iris.cnr.it/retrieve/81ce8ff5-7b2c-46c8-84d6-9fc5a08951bb/Ferrari-Spoletini_Formal%20Requirements_2025.pdf | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 10.1016/j.infsof.2024.107492 | https://digitalcollection.zhaw.ch/bitstreams/9271a1e8-2a44-4254-9f93-7d5c8166b805/download | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Model driven engineering for machine learning components: A systematic literature review | 10.1016/j.infsof.2024.107423 | https://researchmgt.monash.edu/ws/files/593466283/575784880_oa.pdf | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 10.1016/j.jss.2024.112063 | https://openrepository.aut.ac.nz/bitstreams/4f4965ea-029e-4a47-92c8-e13352e273b9/download | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |
| Requirements quality research: a harmonized theory, evaluation, and roadmap | 10.1007/s00766-023-00405-y | https://link.springer.com/content/pdf/10.1007/s00766-023-00405-y.pdf | PDF + `paper_content.txt` 已生成；已完成一篇一 subagent 全文 review |

本轮 10 篇均已找到公开 PDF 或开放预印本版本并用 `tools.pdf_extractor.py` 生成 `paper_content.txt`，因此 `manual-download-needed.bib` 暂无新增条目；原有 3 篇 metadata-only 失败路径继续保留。
