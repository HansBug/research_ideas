# A1 候选池

emoji 口径：🟢 = 已完成全文文本级 dry-run；🟡 = metadata-only / 需人工下载；⚪ = 排除；⏳ = 待补。emoji 列只写 emoji。

| 状态 | 标题 | 年份 | 出版形态 | 期刊/会议/预印本 | CCF 官方大类 | CCF 官方等级 | CCF 复核状态 | 来源等级 | 综述类型 | SE 子领域 | 全文状态 | 候选理由 | 目录 |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 | Machine Learning for Software Engineering: A Tertiary Study | 2023 | 期刊 | [CSUR](https://dl.acm.org/journal/csur) | 待核验（疑似非软件工程大类；官方页 WAF） | 待核验 | 官方待人工复核（WAF）；本地未建 CSUR 条目 | ACM Computing Surveys | tertiary study | ML4SE | PDF + `paper_content.txt` | 现代高等级 tertiary study，适合抽取分类体系、挑战和行动建议；arXiv 只作为开放全文来源。 | [review.md](../papers/ml4se-tertiary-study/review.md) |
| 🟢 | Systematic Reviews in Requirements Engineering: A Tertiary Study | 2014 | 工作坊 | [EmpiRE](https://empire2014.wordpress.com/) | -- | -- | 非 CCF venue / workshop | EmpiRE workshop | tertiary study | Requirements Engineering | PDF + `paper_content.txt` | 特定 SE 子领域 tertiary study，适合抽取子领域和实践影响字段。 | [review.md](../papers/re-tertiary-study-2014/review.md) |
| 🟢 | A Mapping Study on Requirements Engineering in Agile Software Development | 2015 | 会议 | [SEAA](https://dsd-seaa.com/) | -- | -- | 本轮未定位 CCF 目录条目 | SEAA conference | SMS | Agile RE | PDF + `paper_content.txt` | SMS 样本，适合验证 taxonomy/problem/solution pattern。 | [review.md](../papers/re-agile-sms-2015/review.md) |
| 🟢 | Guidelines for performing Systematic Literature Reviews in Software Engineering | 2007 | 技术报告 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- | -- | 非 CCF venue；技术报告 | EBSE 技术报告 | guideline | EBSE 方法学 | PDF + `paper_content.txt` | 基础 guideline，覆盖 SLR protocol/search/selection/extraction/synthesis/reporting。 | [review.md](../papers/kitchenham-charters-2007-slr-guidelines/review.md) |
| 🟢 | Systematic literature reviews in software engineering – A systematic literature review | 2009 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | IST 期刊 | tertiary-like SLR | EBSE / SE SLR 状态 | PDF + `paper_content.txt` | 早期 SE SLR tertiary study，RQ/finding/report 结构完整。 | [review.md](../papers/kitchenham-2009-slr-tertiary/review.md) |
| 🟢 | Six years of systematic literature reviews in software engineering: An updated tertiary study | 2011 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | IST 期刊 | updated tertiary study | EBSE / SE SLR 状态 | PDF + `paper_content.txt` | 扩展前序研究，提供 update / integration pattern。 | [review.md](../papers/da-silva-2011-six-years-slr/review.md) |
| 🟡 | Analysing app reviews for software engineering: a systematic literature review | 2022 | 期刊 | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | Empirical Software Engineering | SLR | App reviews / mobile feedback | PDF 未自动获取 | 高等级现代 SLR 候选；本轮 Springer 链接返回 HTML，需人工下载。 | [review.md](../papers/app-reviews-slr-se/review.md) |
| 🟡 | Systematic Mapping Studies in Software Engineering | 2008 | 会议 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 | C | 本地缓存；官方待人工复核（WAF） | EASE / BCS | SMS 方法论文 | SMS 方法学 | PDF 未自动获取 | 压测 mapping study 与 manual-download-needed 失败路径。 | [review.md](../papers/petersen-2008-systematic-mapping/review.md) |
| 🟡 | Guidelines for conducting systematic mapping studies in software engineering: An update | 2015 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | IST 期刊 | mapping guideline update | SMS 方法学 | PDF 未自动获取 | 高等级 update guideline；压测 update relation 与人工下载路径。 | [review.md](../papers/petersen-2015-mapping-guidelines-update/review.md) |

## 覆盖矩阵

> 说明：以下覆盖矩阵对应 A1 初始 9 篇 dry-run 与失败路径，用于说明 scaffold 的最小验收；#95 十篇现代锚点的覆盖与统计池资格见下一节和 [../SUMMARY.md](../SUMMARY.md) 总账。

| 验收项 | 当前覆盖 | 结论 |
|---|---|---|
| 3--5 篇 dry-run | 6 篇全文文本级 + 3 篇 metadata-only；A1 主 dry-run 使用前 5 篇，早期/失败样本作补充 | 超额通过；不会声称完整覆盖 |
| 至少 3 篇全文文本级 | ML4SE tertiary、RE tertiary、Agile RE SMS、Kitchenham guideline、Kitchenham 2009、da Silva 2011 | 通过 |
| 至少 2 类综述类型 | tertiary study、updated tertiary、SMS、guideline、metadata-only SLR | 通过 |
| 至少 1 篇高等级来源 | ACM Computing Surveys、IST、ESE metadata-only；其中 IST / ESE 为 CCF B，CSUR 需按 CCF 其他大类人工复核 | 通过 |
| 至少 1 篇非 A / 非顶级来源 | EmpiRE、SEAA、EBSE 技术报告 | 通过 |
| 至少 1 篇非 LLM4SE 的 SE 子领域 | ML4SE、RE、Agile RE、EBSE 方法学 | 通过 |
| 至少 1 个失败 / 降级路径 | app reviews SLR、Petersen 2008、Petersen 2015 metadata-only | 通过 |
| 六类 pattern 至少 4 类被填充 | 6 篇全文文本级均至少填充 RQ/dimension/finding/evidence presentation/report structure；部分 validity 待深读 | 通过 |
| 至少 1 个“不适用 / 证据不足”降级记录 | guideline 的 finding 不适用；metadata-only 三条无法抽取六类 pattern | 通过 |


## #95 十篇现代维度锚点纳入状态

以下条目来自 issue [#95](https://github.com/HansBug/research_ideas/issues/95) 与其 Gist 候选总表。本节用于 A1 scaffold hardening，不表示 A2a/A2b 完整文库已完成。

| 状态 | 标题 | 年份 | 出版形态 | 期刊/会议/预印本 | CCF 官方大类 | CCF 官方等级 | CCF 复核状态 | 综述类型 | SE 子领域 / 角色 | 全文状态 | 候选理由 | 目录 |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 | On the road to interactive LLM-based systematic mapping studies | 2025 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | 系统映射 / solution proposal | LLM-supported mapping study | PDF + `paper_content.txt` | LLM-supported mapping study 阶段与 agent role 锚点；online first 为 2024-10-31/2024-11-01，正式卷期与引用年份按 2025 处理。 | [review.md](../papers/interactive-llm-systematic-mapping/review.md) |
| 🟢 | Research artifacts in secondary studies: A systematic mapping in software engineering | 2025 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | systematic mapping | secondary study artifacts | PDF + `paper_content.txt` | secondary study artifact / reproducibility 字段锚点。 | [review.md](../papers/research-artifacts-secondary-studies/review.md) |
| 🟢 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 2026 | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR + SMS | LLM assistants / developer productivity | PDF + `paper_content.txt` | 现代 CCF-A LLM4SE SLR+SMS 的 RQ / SPACE / benefit-risk 组织锚点。 | [review.md](../papers/llm-assistants-developer-productivity/review.md) |
| 🟢 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 2026 | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | vision / roadmap | AI-native SE roadmap | PDF + `paper_content.txt` | AI-native SE roadmap / challenge / vision 边界锚点；非 SLR/SMS。 | [review.md](../papers/ai-native-se-roadmap/review.md) |
| 🟢 | Large Language Models for Software Engineering: A Systematic Literature Review | 2024 | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR | LLM4SE | PDF + `paper_content.txt` | 大规模 LLM4SE SLR 字段体系与 artifact 锚点。 | [review.md](../papers/llm4se-systematic-review/review.md) |
| 🟢 | Formal requirements engineering and large language models: A two-way roadmap | 2025 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | vision / roadmap | formal RE + LLM | PDF + `paper_content.txt` | Formal RE + LLM 双向 roadmap 与 trustworthiness 维度锚点。 | [review.md](../papers/formal-re-llm-roadmap/review.md) |
| 🟢 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 2024 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | systematic mapping | MDSE modelling assistants | PDF + `paper_content.txt` | MDSE modelling assistants systematic mapping，贴近 LLM4modeling 维度树。 | [review.md](../papers/mdse-modelling-assistants-mapping/review.md) |
| 🟢 | Model driven engineering for machine learning components: A systematic literature review | 2024 | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | MDE4ML | PDF + `paper_content.txt` | MDE4ML SLR 的 motivations / solutions / evaluation / limitation 字段锚点。 | [review.md](../papers/mde-ml-components-slr/review.md) |
| 🟢 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 2024 | 期刊 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | multivocal literature review | DevSecOps dimensions | PDF + `paper_content.txt` | 多声部文献综述与 primary dimensions / CPTM 模型锚点。 | [review.md](../papers/devsecops-primary-dimensions/review.md) |
| 🟢 | Requirements quality research: a harmonized theory, evaluation, and roadmap | 2023 | 期刊 | [RE](https://link.springer.com/journal/766) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | theory / evaluation / roadmap | requirements quality | PDF + `paper_content.txt` | requirements quality theory / evaluation / roadmap 元模型锚点。 | [review.md](../papers/requirements-quality-theory-roadmap/review.md) |
