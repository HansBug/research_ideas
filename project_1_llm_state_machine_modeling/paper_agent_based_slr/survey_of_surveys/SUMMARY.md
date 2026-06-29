# survey_of_surveys/SUMMARY.md：综述之综述脚手架总账

## 1. 当前状态

本目录当前处于 **A1 文库奠基 + 现代维度锚点加固** 状态：已建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[search/](./search/)、[papers/](./papers/) 与 [patterns/](./patterns/) 结构，并把 issue [#95](https://github.com/HansBug/research_ideas/issues/95) 中 10 篇现代 survey / SLR / SMS / roadmap 锚点纳入文库。A1 的目标仍是验证脚手架能否指导后续 A2a/A2b，而不是声称完成 100+ 篇完整综述之综述文库。

| 项 | 当前值 |
|---|---:|
| 候选 / 入账条目 | 19 |
| 全文文本级 dry-run / 维度锚点 | 19 |
| metadata-only / 需人工下载 | 0 |
| 完成 `review.md` | 19 |
| 完成 `paper.pdf` + `paper_content.txt` | 19 |
| #95 现代锚点 | 10 |
| #95 已获取 PDF / 开放预印本并生成文本 | 10 |
| 机器可读统计池 / 证据角色字段 | 已补入 19 个 `metadata.json` |
| schema 回修记录 | 9 类 |
| 真实 LLM / `.env` | 未运行 / 未读取 |
| 四个真实例子 | 不运行；A1 只做文库 dry-run |

**本节结论**：A1 已从“6 篇全文 + 3 篇失败路径”的最小脚手架，扩展为“19 篇全文文本级、0 篇待人工下载”的现代锚点文库。历史 3 条人工下载路径已经由用户本地 Zotero PDF 解决，仍保留为失败路径管理机制的审计证据；当前文库足以证明 `survey_of_surveys/` 能承载真实样本、证据等级、A1-M0--M6 元维度、统计池排除规则和历史失败闭环，但仍不是完整三级综述，也不是目标领域证据池。

## 2. 证据等级、统计池与 CCF 口径

emoji 口径：🟢 = 已完成全文文本级 dry-run；🟡 = metadata-only / 需人工下载；⚪ = 排除；⏳ = 待补。正式表格中 emoji 列只写 emoji。

| 阅读状态 | 含义 | 可写边界 |
|---|---|---|
| `已读全文文本-paper_content核验` | 已读 `paper_content.txt` 的摘要、方法、结果、结论等关键部分 | 可写 A1 pattern；图表/表格数值待 PDF 核对。 |
| `已回PDF核对图表` | 已打开 PDF 核对关键图表 / 表格 | 可支撑图表级细节。 |
| `全文不可得-待人工下载` | 合法 PDF 未获取或下载到 HTML / 登录页 | 只能写候选理由和下载需求。 |
| `未读原文-仅题摘粗筛` | 只读标题 / 摘要 / 元数据 | 不能采纳 pattern。 |

| 统计 / schema 字段 | 含义 | 当前使用 |
|---|---|---|
| `eligible_for_schema_seed` | 该文是否可作为后续字段 / 维度 / 报告结构 seed | #95 十篇均为 `true`。 |
| `eligible_for_statistical_synthesis` | 该文是否能进入 SLR/SMS/MLR/systematic mapping 统计池 | #95 十篇中 6 篇为 `true`，4 篇 roadmap / proposal / commentary 为 `false`。 |
| `evidence_role` | 该文在文库中的证据角色 | 区分 `slr_field_schema_pattern`、`systematic_mapping_pattern`、`roadmap_boundary_anchor` 等。 |
| `statistical_pool_exclusion_reason` | 不能进入统计池的原因 | roadmap / vision / solution proposal 必须写明没有系统检索、纳排、质量评价或数据综合。 |

**本节结论**：当前 19 篇全文文本级样本均可支撑 A1 字段 dry-run；当前没有 active metadata-only / 待人工下载条目。历史 3 条下载失败仍作为流程审计样本保留在检索日志中，但不再阻塞字段采纳；roadmap / vision / solution proposal 可做 schema seed，仍必须从统计合成池中机器可读排除。

### 2.1 出版形态、Venue 与 CCF 官方字段口径

本总账固定 4 个来源字段：`出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级`。其中 `期刊/会议/预印本` 必须使用可点击短名链接；预印本条目统一写 `[arXiv](https://arxiv.org/)`。

CCF 字段的目标口径是 **CCF 官方最新推荐目录**，不应局限于本仓库 [../../../ccf_venues/](../../../ccf_venues/) 已建档范围。本轮在 2026-06-29 访问 CCF 官方 [软件工程 / 系统软件 / 程序设计语言目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 时，HTTP/CLI 均返回 Aliyun WAF 壳，无法从正文自动核验 TOSEM / IST / JSS / Requirements Engineering / ESE / EASE。当前表格暂采用本仓库 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 与 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 的已建档缓存作为工作口径；正式写作或投稿前必须人工打开 CCF 官方目录复核。

**本节结论**：A1 现有样本中，TOSEM、IST、JSS、Requirements Engineering、ESE、EASE 的等级按本地 CCF 情报库缓存填写，并显式标注官方待人工复核；CSUR 本轮改为 `待核验` 而不是 `--`，因为它不属于当前已建档的软件工程 venue 缓存但可能存在于 CCF 其他大类；EmpiRE、SEAA 与 EBSE 技术报告仍按非 CCF / 未定位 CCF venue 处理。这个口径比直接留空更便于投稿决策，但不能在论文或投稿材料中写成“官方页面已自动核验”。

## 3. A1-M0--M6 元维度设计

A1-M0--M6 是 `survey_of_surveys/` 内部脚手架元维度，不是 S0 方法阶段，也不是具体主题的最终字段表。它用于把“研究者定义综述元模型 → 维度模式演化 → 字段证据 → 统计观察 → 候选发现 → 研究者裁决”变成可审计链条。

| 元维度 | 中文名 | 操作化问题 | 最低证据 | 当前样本启发 |
|---|---|---|---|---|
| A1-M0 | 研究意图与综述元模型 | 论文如何定义 topic、RQ、scope、review type、unit of analysis、researcher gate？ | 题摘级可候选；全文文本级可采纳 | LLM4SE、MDE4ML、DevSecOps、requirements quality 都显示：先定义研究对象与解释框架，再抽字段。 |
| A1-M1 | 语料收集与纳排 | 论文如何定义数据库、检索式、时间范围、venue、去重、筛选、全文状态、排除理由？ | 全文文本级 | Kitchenham guideline、TOSEM LLM assistant SLR、MDE4ML SLR 提供分母链条与 exclusion code 模板。 |
| A1-M2 | 研究对象与主题语义 | 论文如何划分 SE 子领域、生命周期阶段、研究对象、工件、任务、场景？ | 全文文本级 | LLM4SE 的 SDLC/task tree、MDSE assistant 的 strategy/goal/limitation/metric/user tree、DevSecOps 的 aspect/theme/category tree 都说明维度应树状化。 |
| A1-M3 | 方法 / 技术 / 干预 | 论文如何分类方法、工具链、LLM / agent 角色、自动化程度、human-in-the-loop 点？ | 全文文本级 | interactive LLM mapping proposal 提供阶段化 human-LLM 角色；LLM4SE 与 LLM assistant SLR 提供模型/工具/方法分类。 |
| A1-M4 | 评价、证据与复现资产 | 论文如何记录 metrics、dataset、baseline、artifact、source anchor、replication package、evidence strength？ | 全文文本级；artifact 字段需链接核验 | secondary-study artifact mapping 证明 artifact availability / repository / DOI / dead link 可作为一等字段。 |
| A1-M5 | 统计分析就绪 | 字段是否有版本、取值空间、缺失值语义、可交叉统计字段、回填状态？ | 全文文本级 | MDE4ML、DevSecOps、requirements quality 都把字段表转成频次、交叉表、缺失率或回归分析。 |
| A1-M6 | research finding 形成与裁决 | 论文如何从统计观察形成 candidate finding、support / counter-evidence、claim strength、scope、researcher adjudication？ | 全文文本级 | 多篇样本说明 finding 不是简单频次最高项，而是统计观察 + 缺口解释 + 反向证据 + 研究者裁决。 |

**本节结论**：A1-M0--M6 是当前文库最关键的维度设计资产。A2a 不能只继续“读论文写摘要”，而应围绕这 7 层为每篇综述抽取可统计字段、证据锚点和裁决边界。

## 4. 检索关键词簇分析

### 4.1 当前推荐关键词簇

1. `software engineering systematic literature review tertiary study`。
2. `software engineering systematic mapping study guidelines`。
3. `software engineering survey systematic review quality assessment`。
4. `LLM software engineering systematic literature review mapping study`。
5. `research artifacts secondary studies software engineering systematic mapping`。
6. `model driven engineering systematic literature review software engineering`。
7. `requirements engineering roadmap theory evaluation systematic review`。

### 4.2 高命中特征

1. 题名含 `tertiary study`、`systematic mapping`、`systematic literature review` 的 SE 文献通常能直接提供 A1-M0--M6 的多层字段。
2. 标题直接出现 `dimensions`、`roadmap`、`artifacts`、`assistants` 的现代论文适合做 schema seed，但要区分是否进入统计池。
3. TOSEM / IST / JSS / Requirements Engineering / ESE 等高等级 venue 能提供现代方法学样本，但 PDF / official metadata 常需开放预印本或机构入口补齐。
4. issue #95 的现代样本证明：LLM4SE、MDSE、MDE4ML、DevSecOps、RE quality 都能为“树状维度 + 证据链 + finding 裁决”提供互补模式。

### 4.3 低命中特征

1. 只含 `survey` 的普通综述常缺少系统检索、纳排和质量评价，需降级为 narrative / roadmap / commentary。
2. 聚合 PDF 链接容易返回 HTML / 登录页；必须用 `file` 或 `pdf_extractor` 检查。
3. Vision / roadmap 论文可能学术价值很高，但不能混入 SLR/SMS 统计池。
4. 单篇领域 SLR 若没有全文，只能作为 metadata-only 候选，不能抽取 pattern；当前 A1 的历史 3 条 metadata-only 已补齐全文，但规则仍保留给 A2a/A2b。

### 4.4 检索倾向调整

A2a 应从当前 19 篇出发，优先扩展 2020 年后的 SE tertiary / SLR / SMS / MLR / guideline，覆盖 Requirements Engineering、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE、SE secondary-study artifact 等子领域；同时保留少量 guideline / roadmap / vision 作为 schema seed 和边界锚点，但统计合成池必须与 schema seed 池分离。

**本节结论**：下一步不应只补“更多综述论文”，而要刻意补齐不同 A1-M 层级：能提供检索分母的 SLR/SMS、能提供树状维度的 mapping、能提供 artifact 字段的开放科学研究、能提供 finding heuristic 的 roadmap / theory paper。

## 5. 论文列表

### 5.1 A1 初始 dry-run 与失败路径

| 状态 | 年份 | 标题 | 出版形态 | 期刊/会议/预印本 | CCF 官方大类 | CCF 官方等级 | CCF 复核状态 | 类型 | 关键价值 | 目录 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 | 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | 技术报告 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- | -- | 非 CCF venue；技术报告 | guideline | SLR protocol / search / selection / extraction / synthesis / reporting 基础。 | [review.md](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |
| 🟢 | 2008 | Systematic Mapping Studies in Software Engineering | 会议 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 | C | 本地缓存；官方待人工复核（WAF） | SMS 方法 | mapping study 方法学全文级种子；用户本地 Zotero PDF 已入库。 | [review.md](./papers/petersen-2008-systematic-mapping/review.md) |
| 🟢 | 2009 | Systematic literature reviews in software engineering – A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | tertiary-like SLR | 早期 SE SLR 总览，RQ/finding/report 结构完整。 | [review.md](./papers/kitchenham-2009-slr-tertiary/review.md) |
| 🟢 | 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | updated tertiary | update / integration / 前序研究关系 pattern。 | [review.md](./papers/da-silva-2011-six-years-slr/review.md) |
| 🟢 | 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | 工作坊 | [EmpiRE](https://empire2014.wordpress.com/) | -- | -- | 非 CCF venue / workshop | tertiary | RE 子领域 tertiary，提供领域专门化模式。 | [review.md](./papers/re-tertiary-study-2014/review.md) |
| 🟢 | 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | 会议 | [SEAA](https://dsd-seaa.com/) | -- | -- | 本轮未定位 CCF 目录条目 | SMS | SMS taxonomy / benefit / problem / solution pattern。 | [review.md](./papers/re-agile-sms-2015/review.md) |
| 🟢 | 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | guideline update | SMS guideline update 全文级核心锚点；用户本地 Zotero PDF 已入库。 | [review.md](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 🟢 | 2022 | Analysing app reviews for software engineering: a systematic literature review | 期刊 | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | 现代高等级 SLR 全文级样本；用户本地 Zotero PDF 已入库，并修正作者为 Dąbrowski 等。 | [review.md](./papers/app-reviews-slr-se/review.md) |
| 🟢 | 2023 | Machine Learning for Software Engineering: A Tertiary Study | 期刊 | [CSUR](https://dl.acm.org/journal/csur) | 待核验（疑似非软件工程大类；官方页 WAF） | 待核验 | 官方待人工复核（WAF）；本地未建 CSUR 条目 | tertiary | 现代高等级 tertiary，提供大规模分类、挑战和行动建议 pattern。 | [review.md](./papers/ml4se-tertiary-study/review.md) |

**本节结论**：初始 9 篇负责证明最小 GUIDE / schema / failure path 可执行；当前 9 篇均已升级为全文文本级。历史 3 条 metadata-only 记录不再是 active 阻塞，但仍说明 A1 曾真实压测过“自动下载失败 → 用户补 PDF → 证据升级 → 总账清零”的闭环。

### 5.2 #95 十篇现代维度锚点

| 状态 | 年份 | 标题 | 出版形态 | 期刊/会议/预印本 | CCF 官方大类 | CCF 官方等级 | CCF 复核状态 | 类型 | 可进统计池 | 证据角色 | 关键价值 | 目录 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 | 2025 | On the road to interactive LLM-based systematic mapping studies | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | solution proposal | 否 | `solution_proposal_boundary_anchor` | LLM-supported mapping study 阶段与人机角色锚点。 | [review.md](./papers/interactive-llm-systematic-mapping/review.md) |
| 🟢 | 2025 | Research artifacts in secondary studies: A systematic mapping in software engineering | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | systematic mapping | 是 | `systematic_mapping_pattern` | secondary study artifact / reproducibility 字段锚点。 | [review.md](./papers/research-artifacts-secondary-studies/review.md) |
| 🟢 | 2026 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR + SMS | 是 | `hybrid_slr_sms_pattern` | 现代 CCF-A LLM4SE SLR+SMS 的 RQ / SPACE / benefit-risk 组织锚点。 | [review.md](./papers/llm-assistants-developer-productivity/review.md) |
| 🟢 | 2026 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | vision / roadmap | 否 | `roadmap_boundary_anchor` | AI-native SE roadmap / challenge / vision 边界锚点；非 SLR/SMS。 | [review.md](./papers/ai-native-se-roadmap/review.md) |
| 🟢 | 2024 | Large Language Models for Software Engineering: A Systematic Literature Review | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR | 是 | `slr_field_schema_pattern` | 大规模 LLM4SE SLR 字段体系与 artifact 锚点。 | [review.md](./papers/llm4se-systematic-review/review.md) |
| 🟢 | 2025 | Formal requirements engineering and large language models: A two-way roadmap | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | vision / roadmap | 否 | `roadmap_boundary_anchor` | Formal RE + LLM 双向 roadmap 与 trustworthiness concern 锚点。 | [review.md](./papers/formal-re-llm-roadmap/review.md) |
| 🟢 | 2024 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | systematic mapping | 是 | `systematic_mapping_dimension_pattern` | MDSE modelling assistants systematic mapping，贴近 LLM4modeling 维度树。 | [review.md](./papers/mdse-modelling-assistants-mapping/review.md) |
| 🟢 | 2024 | Model driven engineering for machine learning components: A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | 是 | `slr_dimension_pattern` | MDE4ML SLR 的 motivations / solutions / evaluation / limitation 字段锚点。 | [review.md](./papers/mde-ml-components-slr/review.md) |
| 🟢 | 2024 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 期刊 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | MLR | 是 | `multivocal_review_dimension_pattern` | 多声部文献综述与 primary dimensions / CPTM 模型锚点。 | [review.md](./papers/devsecops-primary-dimensions/review.md) |
| 🟢 | 2023 | Requirements quality research: a harmonized theory, evaluation, and roadmap | 期刊 | [RE](https://link.springer.com/journal/766) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | theory / evaluation / roadmap | 否 | `theory_roadmap_schema_seed` | requirements quality theory / evaluation / roadmap 元模型锚点。 | [review.md](./papers/requirements-quality-theory-roadmap/review.md) |

**本节结论**：#95 十篇使 A1 从“早期方法学样本”升级为“现代 SE 综述维度锚点”。其中 6 篇可进入系统综述 / 映射 / 多声部综述统计池，4 篇只作为 schema seed 或边界锚点，避免 roadmap / proposal 污染统计合成。

## 6. dry-run 覆盖矩阵

| 验收项 | 当前覆盖 | 结论 |
|---|---|---|
| 3--5 篇 dry-run | 19 篇全文文本级；A1 主验收仍按 3--5 篇判断，#95 十篇用于 hardening，历史 3 条失败路径已闭环 | 通过；不声称完整覆盖 |
| 至少 3 篇全文文本级 | 初始 9 篇 + #95 10 篇，共 19 篇 | 通过 |
| 至少 2 类综述类型 | guideline、tertiary、updated tertiary、SLR、SMS、systematic mapping、MLR、solution proposal、vision/roadmap、theory/evaluation/roadmap | 通过 |
| 至少 1 篇高等级来源 | TOSEM、IST、JSS、ESE、Requirements Engineering、CSUR；TOSEM/IST/JSS/ESE/RE 按本地缓存，CSUR 待人工复核，官方目录受 WAF | 通过 |
| 至少 1 篇非 A / 非顶级来源 | EmpiRE、SEAA、EBSE 技术报告 | 通过 |
| 至少 1 篇非 LLM4SE 子领域 | ML4SE、RE、Agile RE、MDE4ML、MDSE、DevSecOps、requirements quality、secondary-study artifacts | 通过 |
| 至少 1 个失败 / 降级路径 | 历史 app reviews SLR、Petersen 2008、Petersen 2015 自动下载失败已闭环；roadmap/proposal 的统计池排除仍为 active 降级路径 | 通过 |
| 六类 pattern 至少 4 类被填充 | 19 篇全文样本均填充至少 4 类；metadata-only 不得采纳的规则保留给后续新增失败条目 | 通过 |
| A1-M0--M6 元维度 | 19 篇 `review.md` 均有 A1-M0--M6 小节；#95 metadata 有 schema seed / statistical synthesis 字段 | 通过 |
| 机器可读统计池过滤 | #95 十篇 `metadata.json` 已写 `eligible_for_statistical_synthesis` 与排除理由 | 通过 |

**本节结论**：A1 dry-run 已覆盖“可系统统计的综述样本”和“只能启发 schema 的边界样本”。这比只堆高等级 SLR 更适合后续 agentic SLR 方法，因为它提前定义了哪些文献能进统计池、哪些只能做维度启发。

## 7. 脚手架模式总表

| pattern | 当前观察 | 来源样本 | A2a 处理建议 |
|---|---|---|---|
| RQ pattern | SE tertiary 常问规模、主题、主体、质量、限制、实践影响；现代 LLM4SE SLR 常先给 landscape / method / benefit-risk / dimension coverage。 | Kitchenham 2009、da Silva 2011、LLM assistant SLR、LLM4SE SLR | 建立 RQ 模式树，区分 landscape、method、impact、dimension coverage、gap/finding。 |
| dimension pattern | 维度应树状化而非平铺：strategy-goal-limitation-metric-user、aspect-theme-category、concept-activity-context-impact 等。 | MDSE assistant mapping、DevSecOps MLR、requirements quality roadmap | A2a 应把字段树版本化，并记录字段来源、缺失语义和 researcher adoption decision。 |
| finding pattern | 从统计观察进一步形成质量缺口、实践影响、research challenges、roadmap、action recommendations；roadmap 文只能提供启发式。 | da Silva 2011、ML4SE tertiary、DevSecOps MLR、requirements quality roadmap | 与 Paper2 的 candidate finding ledger 对齐，补 support / counter-evidence / claim strength。 |
| evidence presentation pattern | 主要使用搜索分母、纳排、quality assessment、topic taxonomy、review/primary-study 数量、artifact availability、replication package。 | Kitchenham guideline、research artifacts mapping、LLM4SE SLR | 后续要求每个字段有 source anchor、artifact link status 和回填状态。 |
| validity / threat pattern | 包含 search bias、inclusion reliability、quality assessment、protocol deviation、artifact dead link、model drift、human validation。 | Kitchenham guideline、interactive LLM mapping、research artifacts mapping | A2a 应设为强制字段，未报告时明确记录。 |
| report structure pattern | guideline、tertiary/SMS、SLR+SMS、MLR、roadmap 的结构不同；不能用一个模板压平。 | 全文样本 | 允许不同 `review_type` 对应不同报告结构和统计池资格。 |

**本节结论**：A1 已经抽出可执行的模式先验：RQ 不只是 PICO；dimension 需要树状化；finding 必须分统计观察、缺口和行动建议；证据呈现、效度威胁、artifact 与统计池过滤是后续审计方法的核心。

## 8. 候选维度模式与采纳状态

emoji 口径：🟢 = A1 已采纳为后续候选字段；🟡 = 候选但需 A2a 扩展；⏳ = 待全文核验。

| 状态 | 字段 | 来源 | 说明 |
|---|---|---|---|
| 🟢 | `review_type` | guideline / tertiary / SLR / SMS / MLR / roadmap / solution proposal | 已扩展枚举，避免把 guideline、roadmap、solution proposal 当成普通 SLR。 |
| 🟢 | `target_se_subfield` | RE、ML4SE、MDE4ML、MDSE、DevSecOps、requirements quality、LLM4SE | 已采纳，支撑 researcher-defined meta-model。 |
| 🟢 | `predecessor_relation` | da Silva 2011、MDSE assistant mapping、DevSecOps MLR | 已采纳，记录 update / extends / validates / differentiates 关系。 |
| 🟢 | `eligible_for_schema_seed` | #95 十篇 | 已采纳，区分“可启发字段”与“可进统计池”。 |
| 🟢 | `eligible_for_statistical_synthesis` | #95 十篇 | 已采纳，roadmap / proposal / commentary 必须机器可读排除。 |
| 🟢 | `evidence_role` | #95 十篇 | 已采纳，区分 SLR 字段样本、mapping 样本、roadmap 边界样本、artifact 样本。 |
| 🟡 | `challenge_action_pattern` | ML4SE tertiary、DevSecOps、requirements quality、AI-native SE roadmap | 候选，A2a 需从更多现代 tertiary / roadmap 中验证取值空间。 |
| 🟡 | `taxonomy_axis` / `problem_solution_pattern` | Agile RE SMS、MDSE assistant mapping、DevSecOps MLR | 候选，适合 SMS / MLR 样本；A2a 再决定是否拆成更细子字段。 |
| 🟢 | `app_review_slr_dimension` | app reviews SLR 2022 | 已基于全文文本级 review 采纳为现代 SLR 字段样本，尤其支撑 F1--F18 抽取表、classification schema、评价质量和 replication package 字段。 |

**本节结论**：A1 的关键 schema 回修已经发生：从平铺六类 pattern 扩展出 review type、子领域、前序关系、统计池资格、证据角色、挑战/行动以及 taxonomy / problem-solution 等可执行字段。

## 9. schema 修订 / 回填日志

| 时间 | 触发条目 | 修订 | 回填状态 | 冻结理由 |
|---|---|---|---|---|
| 2026-06-29 16:59:12 | 用户提供本地 Zotero PDF 与 BibTeX | app reviews SLR 2022、Petersen 2008、Petersen 2015 从 historical metadata-only / manual-download 升级为全文文本级；`manual-download-needed.bib` active 条目清零 | 已复制 3 个 `paper.pdf`，用 `tools.pdf_extractor.py` 生成 3 个 `paper_content.txt`，重写 3 篇 `review.md` 与 `metadata.json`，回填 SUMMARY、candidate-pool、search-log、plan 和 evidence | 人工下载闭环是 A1 证据链重要验收：只有补齐 PDF/text/review 后才能把条目升级为可采纳 pattern。 |
| 2026-06-29 16:13:28 | 三路复审 C/I 修复 | 早期 9 篇补齐 `metadata.json`，使 19 篇都有 `publication_year_basis`、`online_first_date`、统计池资格、证据角色与 CCF 复核状态；CSUR 改为待核验 / 官方待人工复核；同步清理 `paper_content.txt` 行尾空白 | 已回填 19 个 metadata、SUMMARY、candidate-pool、GUIDE、task packet 和 progress | 机器可读字段断层与不可复现 `git diff --check` 会影响 A2a/A2b 聚合和审计。 |
| 2026-06-29 15:41:07 | CCF 官方目录访问异常 | HTTP/CLI 访问 CCF 官方软件工程 / 系统软件 / 程序设计语言目录返回 Aliyun WAF 壳，无法自动核验正文 | 已回填 SUMMARY、candidate-pool、单篇 review 和 metadata 复核状态为“本地缓存；官方待人工复核”；CSUR 因本地未建档改为待核验 | 不能把本地缓存口径冒充官方页面已核验。 |
| 2026-06-29 15:41:07 | #95 十篇现代锚点 | 将脚手架元维度统一为 `A1-M0--M6`，避免与 S0 方法阶段或单篇原文 L1--L6 limitation cluster 混淆 | 已回填 GUIDE、schema、SUMMARY、patterns README、单篇 review | 命名漂移会影响后续 agent 聚合与审查。 |
| 2026-06-29 15:41:07 | #95 roadmap / proposal / commentary | 新增 `eligible_for_schema_seed`、`eligible_for_statistical_synthesis`、`evidence_role`、`statistical_pool_exclusion_reason` | 已回填 10 个 `metadata.json`，后续复审已扩展为 19 个统一 metadata | schema seed 和统计池必须分离，否则会污染 finding 统计。 |
| 2026-06-29 15:41:07 | LLM4SE / MDSE / formal RE 三篇 | 拆分 `legacy_issue95_fulltext_status` 与 `current_fulltext_status` | 已回填 3 个 metadata 状态矛盾条目 | 保留历史获取失败记录，同时让当前本地全文状态可机读。 |
| 2026-06-29 15:37:22 | issue #95 十篇现代锚点 | 扩展 `review_type`：`SLR+SMS`、`systematic mapping`、`multivocal literature review`、`solution proposal`、`vision/roadmap`、`theory/evaluation/roadmap` | 已回填候选池、SUMMARY 与 metadata | 现代样本类型比初始 guideline/tertiary/SMS 更复杂。 |
| 2026-06-29 13:20:00 | 用户新增来源字段要求 | 新增 `publication_type`、`venue_short_link`、`ccf_official_category`、`ccf_official_rank` | 已回填总账、候选池、单篇 review 和 schema | 来源等级必须拆成可审计字段。 |
| 2026-06-29 02:18:07 | Kitchenham & Charters 2007 | 新增 `review_type=guideline` 与 `guideline不适用` 缺失值语义 | 已回填全部初始 review 卡片 | guideline 不生成普通领域 finding，必须允许不适用。 |
| 2026-06-29 02:18:07 | da Silva 2011 / Petersen 2015 | 新增 `predecessor_relation` | da Silva 已全文回填；Petersen 2015 现已由用户本地 PDF 补齐并完成全文回填 | update/extends/integrates 关系是 tertiary/guideline update 的核心。 |
| 2026-06-29 02:18:07 | Bano 2014 / Heikkilä 2015 | 新增 `target_se_subfield` 与 SMS taxonomy/problem/solution 候选 | 已回填 RE / Agile RE 样本 | 子领域化模式是导师讨论中“meta-model 由 researcher 设定”的关键前提。 |
| 2026-06-29 02:18:07 | app reviews SLR / Petersen 2008/2015 | 明确 `metadata-only` 不得升级已采纳 pattern | 历史上进入 manual-download-needed；现已由用户本地 Zotero PDF 补齐并升级为全文级 | 高等级来源也不能绕过证据等级；必须先补全文再升级。 |

**本节结论**：dry-run 已真实触发 schema 回修，不是先验字段表。当前回修足够支撑 A1，但 A2a 仍需用 30--50 篇核心样本继续检验和收敛字段取值空间。

## 10. 失败、阻塞与待复核

| 条目 | 问题 | 当前处理 | 后续动作 |
|---|---|---|---|
| app reviews SLR 2022 | 历史上 Springer PDF 链接返回 HTML，`pdf_extractor` 报 EOF marker not found | 用户已提供本地 Zotero PDF；已复制为 `paper.pdf`、生成 `paper_content.txt`、重写全文级 review；[search/manual-download-needed.bib](./search/manual-download-needed.bib) 当前无 active 条目 | A2a 只需补复杂表格 / 搜索式视觉核对。 |
| Petersen 2008 | 历史上 SciSpace 链接返回 HTML，不是 PDF | 用户已提供本地 Zotero PDF；已复制为 `paper.pdf`、生成 `paper_content.txt`、重写全文级 review | A2a 只需补图表 / 分类 facet 视觉核对。 |
| Petersen 2015 | 历史上 DOI 已有但 PDF 未自动获取 | 用户已提供本地 Zotero PDF；已复制为 `paper.pdf`、生成 `paper_content.txt`、重写全文级 review | A2a 只需补复杂图表 / 附录矩阵视觉核对。 |
| CCF 官方目录 | 2026-06-29 HTTP/CLI 访问 CCF 官方 [软件工程 / 系统软件 / 程序设计语言目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 返回 Aliyun WAF 壳 | 当前表格暂按本地 ccf_venues 缓存；TOSEM=A，IST/JSS/RE/ESE=B，EASE=C | 正式写作 / 投稿前人工打开官方页面核验。 |
| 现代样本图表 | 多数条目已读 `paper_content.txt`，但并非所有表格 / 图形逐页视觉核对 | 单篇 `review.md` 标为待复核 | A2a 深读补页码、表号、图表截图或 source anchors。 |

**本节结论**：失败路径已被显式管理并完成闭环：没有把不可获取 PDF 冒充已读全文，也没有把 roadmap / proposal 冒充系统综述统计证据。A2a 的第一件事不再是补齐这 3 篇，而是对 19 篇现有全文做图表视觉核对、页码/表号锚定，并继续扩大现代样本。

## 11. 后续 A2a / A2b 入口

A2a 建议：

1. 从本目录 19 个全文文本级条目出发，扩展到 30--50 篇核心样本。
2. 优先补 2020 年后 SE tertiary / SLR / SMS / MLR / survey。
3. 每个 SE 子领域至少覆盖一批样本：Requirements Engineering、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE、SE secondary-study artifacts。
4. 把 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 拆成更正式的 pattern library，并记录每个字段的 source anchors、缺失语义、统计池资格和 researcher adoption decision。
5. 对 roadmap / vision / proposal 单独建 `schema_seed_pool`，不要混入 `statistical_synthesis_pool`。

A2b 建议：

1. 扩展到预计 100+ 篇完整文库闭合。
2. 形成第一个可引用快照。
3. 明确纳排分母、排除理由、人工下载清单、覆盖 / 饱和度判断。
4. 把完整文库快照交给 A3 消费，A3 不再混入大规模补文库。

**本节结论**：A1 已建立可接力的脚手架，但学术价值真正成型要依赖 A2a/A2b 的规模化抽取、统计池过滤、字段饱和度判断和研究者裁决记录。

## 12. 更新日志

| 时间 | 更新内容 | 验证 / 备注 |
|---|---|---|
| 2026-06-29 16:59:12 | 用户提供 3 篇历史 manual-download PDF 后，补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 的 `paper.pdf`、`paper_content.txt`、全文级 `review.md` 和 `metadata.json`，并将 active 人工下载清单清零。 | 文件系统统计更新为 19 个 `review.md`、19 个 `metadata.json`、19 个 `paper.pdf`、19 个 `paper_content.txt`；3 篇历史失败路径已闭环，剩余风险转为 A2a 图表视觉核对和 CCF 官方人工复核。 |
| 2026-06-29 16:13:28 | 修复三路 reviewer 复审提出的 C/I：补齐早期 9 篇 `metadata.json`，统一 19 篇机器可读字段，修正 CSUR CCF 待核验口径，并清理 `paper_content.txt` 行尾空白。 | `git diff --check` 两点工作区口径通过；提交后需再用 PR 三点 diff 复验。 |
| 2026-06-29 15:41:07 | 根据内部复核修复 A1-M0--M6 命名、SUMMARY 19/16/3 历史总账、#95 metadata 全文状态、roadmap / proposal 统计池排除字段，并记录 CCF 官方页面 WAF 风险。 | 当时文件系统统计：19 个 `review.md`、19 个 `metadata.json`、16 个 `paper.pdf`、16 个 `paper_content.txt`、3 个 manual-download BibTeX 条目；后续 16:59 已补齐为 19/19/19/19。 |
| 2026-06-29 15:37:22 | 完成 #95 十篇现代锚点一致性复验：补 `issue95-selection-audit.md`，统一 `interactive-llm-systematic-mapping` 年份为正式卷期 2025，修复 progress / task packet 19/16/3 历史总账，保持 CCF 字段为“本地缓存；官方待人工复核（WAF）”。 | 当时 `git diff --check` 与 A1 consistency 脚本通过；manual-download-needed 仍为 3 条旧失败路径，后续 16:59 已清零。 |
| 2026-06-29 13:20:00 | 按用户新增要求补充 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 四列，并同步单篇 review 快速卡片、候选池和字段 schema。 | CCF 字段按官方完整目录口径设计；本轮 HTTP/CLI 访问官方页受 WAF 限制，工作表暂用本地缓存并标注正式写作前需人工复核。 |
| 2026-06-29 02:18:07 | 建立 `survey_of_surveys/` README/GUIDE/SUMMARY/search/papers/patterns；完成 6 篇全文文本级 dry-run 和 3 篇 metadata-only 失败路径；回修 schema 字段。 | A1 奠基；未运行真实 LLM，未读取 `.env`，不跑四个真实例子。 |
