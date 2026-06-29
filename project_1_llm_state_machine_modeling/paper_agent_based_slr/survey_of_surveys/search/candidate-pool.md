# A1 候选池

emoji 口径：🟢 = 已完成全文文本级 dry-run；🟡 = metadata-only / 需人工下载；⚪ = 排除；⏳ = 待补。emoji 列只写 emoji。

| 状态 | 标题 | 年份 | 出版形态 | 期刊/会议/预印本 | CCF 官方大类 | CCF 官方等级 | 来源等级 | 综述类型 | SE 子领域 | 全文状态 | 候选理由 | 目录 |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|
| 🟢 | Machine Learning for Software Engineering: A Tertiary Study | 2023 | 期刊 | [CSUR](https://dl.acm.org/journal/csur) | -- | -- | ACM Computing Surveys | tertiary study | ML4SE | PDF + `paper_content.txt` | 现代高等级 tertiary study，适合抽取分类体系、挑战和行动建议；arXiv 只作为开放全文来源。 | [review.md](../papers/ml4se-tertiary-study/review.md) |
| 🟢 | Systematic Reviews in Requirements Engineering: A Tertiary Study | 2014 | 工作坊 | [EmpiRE](https://empire2014.wordpress.com/) | -- | -- | EmpiRE workshop | tertiary study | Requirements Engineering | PDF + `paper_content.txt` | 特定 SE 子领域 tertiary study，适合抽取子领域和实践影响字段。 | [review.md](../papers/re-tertiary-study-2014/review.md) |
| 🟢 | A Mapping Study on Requirements Engineering in Agile Software Development | 2015 | 会议 | [SEAA](https://dsd-seaa.com/) | -- | -- | SEAA conference | SMS | Agile RE | PDF + `paper_content.txt` | SMS 样本，适合验证 taxonomy/problem/solution pattern。 | [review.md](../papers/re-agile-sms-2015/review.md) |
| 🟢 | Guidelines for performing Systematic Literature Reviews in Software Engineering | 2007 | 技术报告 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- | -- | EBSE 技术报告 | guideline | EBSE 方法学 | PDF + `paper_content.txt` | 基础 guideline，覆盖 SLR protocol/search/selection/extraction/synthesis/reporting。 | [review.md](../papers/kitchenham-charters-2007-slr-guidelines/review.md) |
| 🟢 | Systematic literature reviews in software engineering – A systematic literature review | 2009 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | IST 期刊 | tertiary-like SLR | EBSE / SE SLR 状态 | PDF + `paper_content.txt` | 早期 SE SLR tertiary study，RQ/finding/report 结构完整。 | [review.md](../papers/kitchenham-2009-slr-tertiary/review.md) |
| 🟢 | Six years of systematic literature reviews in software engineering: An updated tertiary study | 2011 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | IST 期刊 | updated tertiary study | EBSE / SE SLR 状态 | PDF + `paper_content.txt` | 扩展前序研究，提供 update / integration pattern。 | [review.md](../papers/da-silva-2011-six-years-slr/review.md) |
| 🟡 | Analysing app reviews for software engineering: a systematic literature review | 2022 | 期刊 | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 | B | Empirical Software Engineering | SLR | App reviews / mobile feedback | PDF 未自动获取 | 高等级现代 SLR 候选；本轮 Springer 链接返回 HTML，需人工下载。 | [review.md](../papers/app-reviews-slr-se/review.md) |
| 🟡 | Systematic Mapping Studies in Software Engineering | 2008 | 会议 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 | C | EASE / BCS | SMS 方法论文 | SMS 方法学 | PDF 未自动获取 | 压测 mapping study 与 manual-download-needed 失败路径。 | [review.md](../papers/petersen-2008-systematic-mapping/review.md) |
| 🟡 | Guidelines for conducting systematic mapping studies in software engineering: An update | 2015 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | IST 期刊 | mapping guideline update | SMS 方法学 | PDF 未自动获取 | 高等级 update guideline；压测 update relation 与人工下载路径。 | [review.md](../papers/petersen-2015-mapping-guidelines-update/review.md) |

## 覆盖矩阵

| 验收项 | 当前覆盖 | 结论 |
|---|---|---|
| 3--5 篇 dry-run | 6 篇全文文本级 + 3 篇 metadata-only；A1 主 dry-run 使用前 5 篇，早期/失败样本作补充 | 超额通过；不会声称完整覆盖 |
| 至少 3 篇全文文本级 | ML4SE tertiary、RE tertiary、Agile RE SMS、Kitchenham guideline、Kitchenham 2009、da Silva 2011 | 通过 |
| 至少 2 类综述类型 | tertiary study、updated tertiary、SMS、guideline、metadata-only SLR | 通过 |
| 至少 1 篇高等级来源 | ACM Computing Surveys、IST、ESE metadata-only；其中 IST / ESE 为 CCF B，CSUR 不写 CCF 等级 | 通过 |
| 至少 1 篇非 A / 非顶级来源 | EmpiRE、SEAA、EBSE 技术报告 | 通过 |
| 至少 1 篇非 LLM4SE 的 SE 子领域 | ML4SE、RE、Agile RE、EBSE 方法学 | 通过 |
| 至少 1 个失败 / 降级路径 | app reviews SLR、Petersen 2008、Petersen 2015 metadata-only | 通过 |
| 六类 pattern 至少 4 类被填充 | 6 篇全文文本级均至少填充 RQ/dimension/finding/evidence presentation/report structure；部分 validity 待深读 | 通过 |
| 至少 1 个“不适用 / 证据不足”降级记录 | guideline 的 finding 不适用；metadata-only 三条无法抽取六类 pattern | 通过 |
