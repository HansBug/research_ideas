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
