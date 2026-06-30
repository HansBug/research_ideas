# survey_of_surveys/SUMMARY.md：综述之综述文库总账

## 1. 当前文库状态与总判断

本目录是 Paper2 agentic SLR 工作的 **survey-of-surveys 文库**：它不直接回答某个目标软件工程主题的研究现状，而是从软件工程领域已有 SLR / SMS / tertiary study / MLR / guideline / roadmap 中抽取“如何设计综述元模型、维度模式、证据链、统计分析和 research finding 裁决”的可迁移先验。

| 项 | 当前值 |
|---|---:|
| 入账论文 | 19 |
| 完成 `review.md` | 19 |
| 完成 `metadata.json` | 19 |
| 完成 `paper.pdf` + `paper_content.txt` | 19 |
| active `manual-download-needed.bib` 条目 | 0 |
| 可作 schema seed | 19 |
| 后续主统计池候选 | 13 |
| 非后续主统计池候选 | 6（方法学参考 2 + 边界 / 启发 seed 4） |
| 真实 LLM / `.env` | A1 原始 dry-run 未运行；A1-DT v2 已完成 57/57 CLI 审计，日志保留命令/stdout/stderr与环境摘要，关于 `.env` 只记录 `.env exists`，不记录 secret |
| 四个真实例子 | 不运行；A1 只做文库 dry-run |

**总判断**：A1 当前已经从“最小脚手架”进入“可接力的长期文库起点”状态。19 篇均达到全文文本级，并且 A1-DT v2 已完成 57/57 三路 CLI 审计、19/19 主线程裁决和 19/19 单篇 `review.md` 返修，可用于验证字段抽取、证据等级、统计池候选过滤、A1-M0--M6 元维度、原生维度树 / 维度森林和失败路径闭环；但这些证据链当前仍按 `schema_seed` / `boundary_anchor` 管理，不能直接进入 Paper2 final finding 或目标领域定量结论。后续 A2a/A2b 的重点应是扩大样本、补图表/页码级证据锚点、收敛字段取值空间，并记录 researcher adoption decision，完成后才可把候选主统计池升级为正式统计证据。

## 1.1 PR #135 A1-DT v2 抽取与审计口径

A1-DT v2 的核心修正是把“单篇论文原生维度树 / 维度森林”和“跨论文 A1-M0--M6 投影矩阵”分开：每篇 `review.md` 应优先复原原文自己的 RQ、样本单位、抽取字段、分类 schema、统计表、roadmap / guideline stage 与 finding path；A1-M0--M6 只作为跨论文投影层，用于比较和接力，不能反向冒充单篇原生树。v1 审计目录 [audits/a1dt-19x3/](./audits/a1dt-19x3/) 仅作为历史归档；v2 独立入口为 [audits/a1dt-v2-19x3/](./audits/a1dt-v2-19x3/)。

v2 当前总判断：19 篇均具备全文文本、`metadata.json` 与 `review.md`，并已完成 57/57 三路 CLI 审计、19/19 人工 adjudication 和 19/19 单篇返修；其中 13 篇是后续主统计池候选，6 篇因 guideline / roadmap / proposal / theory-roadmap 等性质降级为方法学参考或 boundary seed。v2 表中的样本数量、树型和统计池资格已经回填到当前总账，但仍只能作为 `schema_seed` / `boundary_anchor`；在 A2a 完成页码 / 表图 / supplementary 精核前，不得写成 Paper2 final finding。

## 1.2 A1-DT v2 统一总账表（按年份降序）

字段口径：`样本单位` 与 `样本数量` 只记录单篇论文原文自己的 corpus / evidence base；roadmap、vision、proposal、guideline 或 convenience evaluation 若无系统样本库，必须显式降级。`原生树类型` 是单篇原文 schema 的树型判断；A1-M0--M6 只用于后续投影，不在本表中充当原生树。

| 年份 | 论文 | 类型 | venue/source | CCF 大类/等级 | 样本单位 | 样本数量 | 原生树类型 | 字段来源 | 统计池资格 | v2 审计状态 | review 链接 |
|---:|---|---|---|---|---|---:|---|---|---|---|---|
| 2026 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | SLR + SMS | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 / A | peer-reviewed primary studies | 39 | RQ 驱动分类树 + SPACE/productivity 评价树 | `schema_seed`；全文文本级；表图待 A2a 精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/llm-assistants-developer-productivity/review.md) |
| 2026 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | vision / roadmap | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 / A | 无系统样本库；愿景与社区经验来源 | -- | SE 3.0 技术栈 / challenge roadmap 树 | `boundary_anchor`；全文文本级；无系统检索分母 | 否；roadmap 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/ai-native-se-roadmap/review.md) |
| 2025 | Research artifacts in secondary studies: A systematic mapping in software engineering | systematic mapping | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | SE secondary studies | 537 | 证据资产审计树 + artifact availability 统计树 | `schema_seed`；全文文本级；关键表格仍待最终版核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/research-artifacts-secondary-studies/review.md) |
| 2025 | On the road to interactive LLM-based systematic mapping studies | solution proposal | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 无已执行系统样本库；方法流程 proposal | -- | LLM-supported SMS 方法流程树 | `boundary_anchor`；全文文本级；Fig. 1 / 阶段模型待精核 | 否；proposal 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/interactive-llm-systematic-mapping/review.md) |
| 2025 | Formal requirements engineering and large language models: A two-way roadmap | vision / roadmap | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 无系统样本库；roadmap concern/action points | -- | concern / mechanism / action-point roadmap 树 | `boundary_anchor`；全文文本级；非系统综述 | 否；roadmap 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/formal-re-llm-roadmap/review.md) |
| 2024 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | systematic mapping | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | research proposals / MDSE assistant studies | 58 | systematic mapping 分类树 + assistant strategy-goal-metric-user 树 | `schema_seed`；全文文本级；分类表待 A2a 精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/mdse-modelling-assistants-mapping/review.md) |
| 2024 | Model driven engineering for machine learning components: A systematic literature review | SLR | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | primary studies | 46 | MDE4ML lifecycle / motivation-solution-evaluation 树 | `schema_seed`；全文文本级；appendix / QA 表待精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/mde-ml-components-slr/review.md) |
| 2024 | Large Language Models for Software Engineering: A Systematic Literature Review | SLR | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 / A | LLM4SE studies | 395 | LLM4SE task-method-evidence 大规模分类树 | `schema_seed`；全文文本级；ACM final 与 replication package 待核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/llm4se-systematic-review/review.md) |
| 2024 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | MLR | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 / B | white literature + grey literature | 147 | 关系型维度树 + CPTM / thematic synthesis 树 | `schema_seed`；全文文本级；Zenodo 工件待 A2a 精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/devsecops-primary-dimensions/review.md) |
| 2023 | Requirements quality research: a harmonized theory, evaluation, and roadmap | theory / evaluation / roadmap | [RE](https://link.springer.com/journal/766) | 软件工程 / 系统软件 / 程序设计语言 / B | convenience evaluation primary studies | 57 | RQT 理论 / 元模型概念树 + 状态评价树 | `boundary_anchor`；全文文本级；非标准 SLR/SMS | 否；theory-roadmap 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/requirements-quality-theory-roadmap/review.md) |
| 2023 | Machine Learning for Software Engineering: A Tertiary Study | tertiary study | [CSUR](https://dl.acm.org/journal/csur) | 待核验 / 待核验 | reviews + traced primary studies | 83 reviews / 6117 primary studies | tertiary 主题 / 挑战 / action recommendation 树 | `schema_seed`；全文文本级；ACM final / arXiv 差异待核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/ml4se-tertiary-study/review.md) |
| 2022 | Analysing app reviews for software engineering: a systematic literature review | SLR | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 / B | primary studies | 182 | RQ 驱动分类树 + 评价 / 复现资产审计树 | `schema_seed`；全文文本级；F1--F18 与复杂表格待精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/app-reviews-slr-se/review.md) |
| 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | mapping guideline update / systematic map of maps | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | SE systematic mapping studies | 52 | mapping guideline update 维度森林 + topic-independent dimensions 树 | `schema_seed`；全文文本级；52 为最终 included mapping studies，57 仅为中间候选口径；Appendix A / B 待 A2a 精核 | 是；方法学统计样本 | completed；adjudicated；A2a 待精核 | [review](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | SMS | [SEAA](https://dsd-seaa.com/) | -- / -- | articles | 28 | SMS problem-benefit-solution 树 + Agile RE 主题分类树 | `schema_seed`；全文文本级；短文表格待核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/re-agile-sms-2015/review.md) |
| 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | tertiary study | [EmpiRE](https://empire2014.wordpress.com/) | -- / -- | distinct reviews / publications | 53 reviews / 64 publications | RE tertiary 主题统计树 + quality / impact 树 | `schema_seed`；全文文本级；workshop 短文需降级 | 是；短文边界 | completed；adjudicated；A2a 待精核 | [review](./papers/re-tertiary-study-2014/review.md) |
| 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | updated tertiary study | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | new SLRs in update window | 67 | tertiary 更新统计树 + predecessor/update 关系树 | `schema_seed`；全文文本级；与前序样本合并关系待精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/da-silva-2011-six-years-slr/review.md) |
| 2009 | Systematic literature reviews in software engineering – A systematic literature review | tertiary-like SLR | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | relevant SLR studies | 20 | early SE SLR 生态统计树 + quality evaluation 树 | `schema_seed`；全文文本级；早期 venue 手工搜索边界 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/kitchenham-2009-slr-tertiary/review.md) |
| 2008 | Systematic Mapping Studies in Software Engineering | SMS 方法论文 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 / C | 方法示例 / illustrative primary-study set | -- | SMS 方法流程树 + keywording / classification facet 树 | `schema_seed`；全文文本级；方法论文不作领域分母 | 否；方法学参考降级 | completed；adjudicated；A2a 待精核 | [review](./papers/petersen-2008-systematic-mapping/review.md) |
| 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | guideline | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- / -- | 无系统样本库；方法指南 | -- | SLR protocol / search-selection-extraction-synthesis 方法树 | `schema_seed`；全文文本级；规范性指南 | 否；guideline 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |

**本节结论**：v2 表把 19 篇统一放回对象总账，并把 roadmap / proposal / guideline 的样本单位写成 `--` 或非系统样本来源，防止它们混入主统计池。当前表已经回填 A1-DT v2 审计与 adjudication 结果；后续 A2a 若通过 PDF / supplementary 精核修正某篇原生树类型、样本数量或分母链，应先改单篇 `review.md` 与 adjudication，再回填本表。

## 2. 核心口径：阅读状态、证据池与统计池

### 2.1 阅读状态与证据等级

emoji 口径：🟢 = 已完成全文文本级；🟡 = metadata-only / 需人工下载；⚪ = 排除；⏳ = 待补。正式表格中 emoji 列只写 emoji。

| 阅读状态 | 含义 | 可写边界 |
|---|---|---|
| `未读原文-仅题摘粗筛` | 只读题名、摘要、元数据 | 只能写候选相关性，不能采纳 pattern。 |
| `已读全文文本-paper_content核验` | 已读 `paper_content.txt` 的摘要、方法、结果、讨论、结论等关键部分 | 可写 A1 pattern；图表、表格、页码和精确数值仍需 PDF 核对。 |
| `已回PDF核对图表` | 已人工打开 PDF 核对关键图表、表格、公式或版式 | 可支撑图表/数值级 pattern。 |
| `全文不可得-待人工下载` | 合法 PDF 未获取，或下载到 HTML / 登录页 | 只能保留元数据、下载尝试和候选理由。 |

### 2.2 三类证据池与 A1-DT 当前用途

`eligible_for_statistical_synthesis` 只表示“按论文类型和系统性证据看，后续是否可作为主统计池候选”，不表示 PR-A1-DT 当前维度树证据已经可进入 SUMMARY 定量统计。guideline、roadmap、proposal 可能非常重要，但不能与完成型 SLR/SMS/MLR 混算；而即使是后续主统计池候选，在 A2a 完成精确页码 / 表图 / 字段锚定前，当前 A1-DT 结论也只允许作为 `schema_seed`。

| 池 | 可进入条件 | 当前用途 | 当前数量 |
|---|---|---|---:|
| 后续主统计池候选 | 论文自身已经执行完成 SLR / SMS / tertiary / MLR / systematic mapping；有系统检索或等价语料构造、纳排 / 编码 / 数据抽取、可统计字段或结果；本地至少全文文本级 | A2a/A2b 完成精确锚定后，用于统计字段频次、覆盖度、维度饱和度和 finding 支撑；A1-DT 当前只作 `schema_seed` | 13 |
| 方法学参考池 | guideline、mapping guideline、方法论文；能定义流程、抽取、报告、效度或质量评价规则，但不是普通领域统计样本 | 指导方法设计、schema 设计、证据链设计；不与普通领域统计池混算 | 2 |
| schema seed / boundary pool | roadmap、vision、solution proposal、theory roadmap、非标准系统综述但有高价值维度或 finding heuristic | 启发维度、方法边界、人机协同和 finding heuristic；不得污染统计池 | 4 |

上述三类池按“主归属”计数，合计 13 + 2 + 4 = 19，避免同一论文在 SUMMARY 统计中重复计数。当前 `metadata.json` 中 13 篇 `eligible_for_statistical_synthesis=true`，表示它们是后续主统计池候选；6 篇为 `false`，并均写明 `statistical_pool_exclusion_reason`。其中 Kitchenham & Charters 2007 与 Petersen 2008 是非主统计池的方法学参考；Petersen 2015 虽然也是方法学高价值样本，但它本身执行了 systematic mapping of systematic maps，因此主归属放在后续主统计池候选，并在解释中标注为“方法学统计样本”。PR-A1-DT 当前 A.2/A.3 若仍含待 A2a 精确页码 / 表图核验，则一律不得作为 SUMMARY 定量统计证据。

### 2.3 出版形态、Venue 与 CCF 口径

本总账固定维护 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 和 `CCF 复核状态`。其中 `期刊/会议/预印本` 使用可点击短名链接；预印本统一写 `[arXiv](https://arxiv.org/)`。主表中的 `CCF 复核状态` 是事实口径的一部分，不得只依赖段落级 disclaimer；复制主表行时必须同时复制该列，避免把本地缓存误写成官方实时核验。

CCF 字段的目标口径是 **CCF 官方最新推荐目录**，不局限于本仓库 [../../../ccf_venues/](../../../ccf_venues/) 已建档范围。2026-06-29 本轮 HTTP/CLI 访问 CCF 官方 [软件工程 / 系统软件 / 程序设计语言目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 返回 Aliyun WAF 壳，当前表格暂采用本地 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 与 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 的已建档缓存作为工作口径；正式写作或投稿前必须人工打开 CCF 官方目录复核。

**本节结论**：本目录应把“是否可统计”和“是否有启发价值”分开管理。后续 A2a 不能因为 roadmap / proposal 学术价值高就把它们纳入统计池，也不能因为 guideline 不进统计池就忽略其方法学价值。

## 3. 统一论文总表（按年份降序）

| 状态 | 年份 | 标题 | 出版形态 | 期刊/会议/预印本 | CCF 大类 | CCF 等级 | CCF 复核状态 | 综述类型 | schema seed | 主统计池 | 证据角色 | 关键价值 | 详情 |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 🟢 | 2026 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR + SMS | 是 | 是 | `hybrid_slr_sms_pattern` | 现代 CCF-A LLM4SE SLR+SMS，提供 RQ / SPACE / benefit-risk / mapping hybrid 组织模式。 | [review.md](./papers/llm-assistants-developer-productivity/review.md) |
| 🟢 | 2026 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | vision / roadmap | 是 | 否 | `roadmap_boundary_anchor` | AI-native SE 愿景、技术栈和挑战路线图；启发 boundary / challenge / action 字段。 | [review.md](./papers/ai-native-se-roadmap/review.md) |
| 🟢 | 2025 | Research artifacts in secondary studies: A systematic mapping in software engineering | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | systematic mapping | 是 | 是 | `systematic_mapping_pattern` | 把 secondary-study research artifacts 操作化为可统计字段，支撑证据资产链设计。 | [review.md](./papers/research-artifacts-secondary-studies/review.md) |
| 🟢 | 2025 | On the road to interactive LLM-based systematic mapping studies | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | solution proposal | 是 | 否 | `solution_proposal_boundary_anchor` | LLM-supported mapping study 阶段、人机角色、agent / prompt 风险锚点；不是已执行系统综述。 | [review.md](./papers/interactive-llm-systematic-mapping/review.md) |
| 🟢 | 2025 | Formal requirements engineering and large language models: A two-way roadmap | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | vision / roadmap | 是 | 否 | `roadmap_boundary_anchor` | Formal RE + LLM 双向路线图，启发 trustworthiness concern 与 action point 字段。 | [review.md](./papers/formal-re-llm-roadmap/review.md) |
| 🟢 | 2024 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | systematic mapping | 是 | 是 | `systematic_mapping_dimension_pattern` | MDSE modelling assistants 系统映射，贴近 LLM4modeling 维度树和 taxonomy 设计。 | [review.md](./papers/mdse-modelling-assistants-mapping/review.md) |
| 🟢 | 2024 | Model driven engineering for machine learning components: A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | 是 | 是 | `slr_dimension_pattern` | MDE4ML SLR，提供 motivation / solution / evaluation / limitation 字段模式。 | [review.md](./papers/mde-ml-components-slr/review.md) |
| 🟢 | 2024 | Large Language Models for Software Engineering: A Systematic Literature Review | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR | 是 | 是 | `slr_field_schema_pattern` | 大规模 LLM4SE SLR，提供任务树、模型/工具、数据/代码、限制和趋势字段。 | [review.md](./papers/llm4se-systematic-review/review.md) |
| 🟢 | 2024 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 期刊 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | MLR | 是 | 是 | `multivocal_review_dimension_pattern` | 多声部综述，提供 white/grey 证据、主题分析、CPTM 模型和开放工件模式。 | [review.md](./papers/devsecops-primary-dimensions/review.md) |
| 🟢 | 2023 | Requirements quality research: a harmonized theory, evaluation, and roadmap | 期刊 | [RE](https://link.springer.com/journal/766) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | theory / evaluation / roadmap | 是 | 否 | `theory_roadmap_schema_seed` | 以理论对象、57 篇状态评价和 roadmap 组织 requirements quality，启发 meta-model-first 写法。 | [review.md](./papers/requirements-quality-theory-roadmap/review.md) |
| 🟢 | 2023 | Machine Learning for Software Engineering: A Tertiary Study | 期刊 | [CSUR](https://dl.acm.org/journal/csur) | 待核验 | 待核验 | 待核验；官方待人工复核（WAF） | tertiary study | 是 | 是 | `tertiary_study_pattern` | 现代大规模 tertiary，提供挑战 / 行动建议 / ML4SE 分类和质量观察模式。 | [review.md](./papers/ml4se-tertiary-study/review.md) |
| 🟢 | 2022 | Analysing app reviews for software engineering: a systematic literature review | 期刊 | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | 是 | 是 | `slr_field_schema_pattern` | 完整现代 SLR 样本，提供 F1--F18 抽取表、分类 schema、评价质量和 replication package 字段。 | [review.md](./papers/app-reviews-slr-se/review.md) |
| 🟢 | 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | mapping guideline update | 是 | 是 | `mapping_guideline_update_pattern` | 以 systematic mapping of maps 更新 SMS guideline，支撑流程、质量、效度和报告结构字段。 | [review.md](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 🟢 | 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | 会议 | [SEAA](https://dsd-seaa.com/) | -- | -- | 本轮未定位 CCF 目录条目 | SMS | 是 | 是 | `systematic_mapping_pattern` | Agile RE SMS，提供 benefit / problem / solution / taxonomy 这类 mapping 字段。 | [review.md](./papers/re-agile-sms-2015/review.md) |
| 🟢 | 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | 工作坊 | [EmpiRE](https://empire2014.wordpress.com/) | -- | -- | 非 CCF workshop | tertiary study | 是 | 是 | `domain_tertiary_study_pattern` | RE 子领域 tertiary，验证 target SE subfield、topic taxonomy、教育/实践影响字段。 | [review.md](./papers/re-tertiary-study-2014/review.md) |
| 🟢 | 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | updated tertiary study | 是 | 是 | `updated_tertiary_study_pattern` | 更新型 tertiary，提供 predecessor relation、增长/质量/实践影响 finding 模式。 | [review.md](./papers/da-silva-2011-six-years-slr/review.md) |
| 🟢 | 2009 | Systematic literature reviews in software engineering – A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | tertiary-like SLR | 是 | 是 | `tertiary_study_pattern` | 早期 SE SLR 总览，提供 EBSE 领域的 RQ、质量、主题与报告结构基线。 | [review.md](./papers/kitchenham-2009-slr-tertiary/review.md) |
| 🟢 | 2008 | Systematic Mapping Studies in Software Engineering | 会议 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 | C | 本地缓存；官方待人工复核（WAF） | SMS 方法论文 | 是 | 否 | `mapping_guideline_pattern` | SMS 方法母文，定义 mapping vs review、keywording、classification facet 和 map 可视化。 | [review.md](./papers/petersen-2008-systematic-mapping/review.md) |
| 🟢 | 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | 技术报告 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- | -- | 非 CCF 技术报告 | guideline | 是 | 否 | `guideline_methodology_seed` | SE SLR 方法指南，提供 protocol、检索、纳排、质量评价、抽取和报告基础。 | [review.md](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |

**本节结论**：统一总表显示，当前 19 篇覆盖 2007--2026 年的软件工程二级研究方法、领域 SLR/SMS、现代 LLM4SE / MDE / DevSecOps / RE 综述和 roadmap 边界样本。后续扩库应继续按年份降序维护总表，不再按 PR 批次拆表。

## 4. 证据池分布与统计池解释

| 池 / 角色 | 当前主归属条目 / 数量 | 说明 |
|---|---|---|
| 后续主统计池候选 | 13 | 可在 A2a/A2b 完成精确页码、表图和字段锚定后，用于统计“综述论文如何组织维度、字段、证据和 finding”。包含 SLR、SMS、tertiary、MLR、systematic mapping，以及 Petersen 2015 这种已执行 systematic mapping of maps 的方法学统计样本；PR-A1-DT 当前只提供 `schema_seed`。 |
| 方法学参考池 | 2：Kitchenham & Charters 2007、Petersen 2008 | 这些论文定义 SLR/SMS 的流程、keywording、classification、quality / validity 和 reporting 规则；不应与普通领域结果统计混算。Petersen 2015 也有方法学价值，但主归属为主统计池中的“方法学统计样本”，不在本池重复计数。 |
| schema seed / boundary pool | 4：AI-native SE roadmap、Formal RE + LLM roadmap、interactive LLM systematic mapping proposal、requirements quality theory roadmap | 这些论文适合启发字段树、人机协同、trustworthiness concern、finding heuristic 和方法边界；不得进入主统计池。 |
| 待人工下载 / metadata-only | 0 | 历史 3 条下载失败已由用户本地 Zotero PDF 补齐；后续新增失败条目必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。 |
| CCF 待官方复核 | TOSEM / IST / JSS / RE / ESE / EASE 本地缓存；CSUR 待核验 | 当前受 CCF 官方 WAF 限制，正式写作前需人工复核。 |

**本节结论**：A1 当前最重要的治理规则是“统计池与 schema seed 池分离”。这能防止 roadmap / proposal 的高价值观点污染统计结论，也能防止 guideline 的方法学价值被错误低估。

## 5. A1-M0--M6 元维度定义

A1-M0--M6 是 `survey_of_surveys/` 的脚手架元维度，用于把“研究者定义综述元模型 → 维度模式演化 → 字段证据 → 统计观察 → 候选 finding → 研究者裁决”变成可审计链条。它不是最终 A3 schema，也不是某个具体 SE 主题的固定字段表。

| 元维度 | 中文名 | 操作化问题 | 最低证据 | 当前主要启发 |
|---|---|---|---|---|
| A1-M0 | 研究意图与综述元模型 | 论文如何定义 topic、RQ、scope、review type、unit of analysis、researcher gate？ | 题摘级可候选；全文文本级可采纳 | 先定义研究对象与解释框架，再抽字段。 |
| A1-M1 | 语料收集与纳排 | 论文如何定义数据库、检索式、时间范围、venue、去重、筛选、全文状态、排除理由？ | 全文文本级 | 分母链条和 exclusion code 是统计池资格基础。 |
| A1-M2 | 研究对象与主题语义 | 论文如何划分 SE 子领域、生命周期阶段、研究对象、工件、任务、场景？ | 全文文本级 | 维度应树状化，并由 researcher-defined meta-model 约束。 |
| A1-M3 | 方法 / 技术 / 干预 | 论文如何分类方法、工具链、LLM / agent 角色、自动化程度、human-in-the-loop 点？ | 全文文本级 | 现代 LLM4SE / MDSE / MDE / DevSecOps 综述能提供方法 / 工具 / agent role 分类。 |
| A1-M4 | 评价、证据与复现资产 | 论文如何记录 metrics、dataset、baseline、artifact、source anchor、replication package、evidence strength？ | 全文文本级；artifact 字段需链接核验 | research artifact、replication package、dead link、by request 等应成为一等字段。 |
| A1-M5 | 统计分析就绪 | 字段是否有版本、取值空间、缺失值语义、可交叉统计字段、回填状态？ | 全文文本级 | 字段表需要可统计、可回填、可记录缺失语义。 |
| A1-M6 | research finding 形成与裁决 | 论文如何从统计观察形成 candidate finding、support / counter-evidence、claim strength、scope、researcher adjudication？ | 全文文本级 | finding 不是频次最高项，而是统计观察 + 缺口解释 + 反向证据 + 研究者裁决。 |

## 6. A1-M0--M6 逐篇覆盖矩阵

下表是 SUMMARY 级总账视图。每格只保留短语级贡献；详细证据、可迁移性和不可迁移点见对应单篇 `review.md`。

| 论文 | A1-M0 | A1-M1 | A1-M2 | A1-M3 | A1-M4 | A1-M5 | A1-M6 |
|---|---|---|---|---|---|---|---|
| [LLM assistants productivity](./papers/llm-assistants-developer-productivity/review.md) | LLM assistant 生产力综述元模型 | 39 篇 peer-reviewed studies 与时间窗 | SPACE / task / benefit-risk 分类 | LLM assistant 任务与使用场景 | 生产力指标与 empirical evidence | SLR+SMS 混合统计表 | productivity benefit / risk finding |
| [AI-native SE roadmap](./papers/ai-native-se-roadmap/review.md) | SE 3.0 愿景元模型 | 非系统检索；不采纳 M1 | 五层技术栈与挑战域 | AI teammate / FMware / intent-centric | 经验与社区互动作边界证据 | 不进统计池 | challenge roadmap / action heuristic |
| [Research artifacts in secondary studies](./papers/research-artifacts-secondary-studies/review.md) | secondary-study artifact 元模型 | 537 篇 secondary studies 检索与筛选 | artifact reporting / availability 对象 | artifact repository / DOI / by-request 分类 | open artifact 与 dead-link 字段 | 可直接统计 artifact 可用性 | reproducibility gap finding |
| [Interactive LLM systematic mapping](./papers/interactive-llm-systematic-mapping/review.md) | LLM-supported mapping 方法设想 | solution proposal；不采纳统计分母 | SMS 流程阶段与人机节点 | agents / prompts / interaction roles | traceability、model drift 风险 | 不进统计池 | LLM 介入 mapping 的边界启发 |
| [Formal RE + LLM roadmap](./papers/formal-re-llm-roadmap/review.md) | formal RE 与 LLM 双向路线 | roadmap；不采纳 M1 | formal specification / RE task concern | LLM agents + formal method roles | correctness / fairness / trustworthiness | 不进统计池 | 双向 roadmap 与 trustworthiness heuristic |
| [MDSE modelling assistants](./papers/mdse-modelling-assistants-mapping/review.md) | MDSE assistant landscape | systematic mapping 检索与分类 | strategy / goal / limitation / metric / user tree | modelling assistant 方法与工具 | metric / user / limitation evidence | 分类轴可交叉统计 | MDSE assistant gap / opportunity |
| [MDE for ML components](./papers/mde-ml-components-slr/review.md) | MDE4ML 综述对象 | SLR protocol 与 primary studies | motivations / solutions / lifecycle objects | MDE 方法、建模语言、工具 | evaluation / limitation / artifact | 字段频次与交叉统计 | ML component engineering gap |
| [LLM4SE SLR](./papers/llm4se-systematic-review/review.md) | LLM4SE 任务与效果元模型 | 395 篇研究检索 / 纳排 | SDLC task tree / model / data | LLM 应用方式、工具、模型 | dataset、artifact、evaluation 字段 | 大规模字段统计 | LLM4SE limitation / trend finding |
| [DevSecOps primary dimensions](./papers/devsecops-primary-dimensions/review.md) | DevSecOps primary dimensions | white / grey literature 双轨 MLR | aspect / theme / CPTM taxonomy | practice / tool / metric / lifecycle | Zenodo open artifacts / QA score | CPTM 与 TA 表可统计 | GSE 空白与 challenge-practice-tool-metric finding |
| [Requirements quality roadmap](./papers/requirements-quality-theory-roadmap/review.md) | requirements quality theory 元模型 | 非标准 SLR；57 篇状态评价 | artifact / agent / activity / impact theory | quality model / tool-support 架构 | evaluation status 与 theory evidence | 不进主统计池 | theory gap → roadmap / tool architecture |
| [ML4SE tertiary](./papers/ml4se-tertiary-study/review.md) | ML4SE tertiary 元模型 | tertiary search / secondary studies | ML4SE topic / challenge 分类 | ML 方法与 SE task 分类 | quality / challenge / action evidence | 大规模 tertiary 统计 | challenge / action recommendation |
| [App reviews SLR](./papers/app-reviews-slr-se/review.md) | app reviews for SE 元模型 | 1656→182 纳排链条 | review type / technique / SE activity | mining technique 与 analysis type | F1--F18、evaluation、replication package | 多套 classification schema | support-to-SE finding 与评价缺口 |
| [Petersen 2015 mapping update](./papers/petersen-2015-mapping-guidelines-update/review.md) | SMS guideline update 元模型 | mapping studies 检索 / snowballing | topic-independent dimensions | SMS planning-conducting-reporting | quality rubric / validity taxonomy | systematic maps of maps | guideline update finding |
| [Agile RE SMS](./papers/re-agile-sms-2015/review.md) | Agile RE mapping scope | 28 articles mapping | benefit / problem / solution taxonomy | Agile RE practice categories | 短文证据与缺失 threat | 小规模 taxonomy 统计 | definition ambiguity / solution gap |
| [RE tertiary](./papers/re-tertiary-study-2014/review.md) | RE 子领域 tertiary scope | distinct reviews / publications | RE topics / education / practice | RE research method overview | quality / impact evidence | distinct review vs publication 分母 | RE SLR quality / impact finding |
| [da Silva 2011 updated tertiary](./papers/da-silva-2011-six-years-slr/review.md) | updated tertiary 元模型 | 新旧 tertiary 合并与增量检索 | SE topics / author / institution | EBSE practice and education dimensions | quality assessment / relevance evidence | longitudinal / update 统计 | growth + quality + practice gap |
| [Kitchenham 2009 tertiary-like SLR](./papers/kitchenham-2009-slr-tertiary/review.md) | early SE SLR ecosystem | SLR collection and screening | topic / quality / method dimensions | EBSE method usage | quality and reporting evidence | early tertiary summary statistics | SE SLR adoption / quality finding |
| [Petersen 2008 SMS method](./papers/petersen-2008-systematic-mapping/review.md) | SMS vs SLR 方法元模型 | 方法示例；不进主统计池 | topic / contribution / research type facets | keywording 与 classification process | map / bubble plot / rationale evidence | 方法级频数示例 | mapping 用于识别研究空白 |
| [Kitchenham & Charters 2007 guideline](./papers/kitchenham-charters-2007-slr-guidelines/review.md) | SLR protocol 元模型 | guideline；不进主统计池 | RQ / population / intervention / outcome | search / selection / extraction / synthesis process | quality assessment / data extraction forms | 方法标准，不做统计池 | reporting / validity / protocol discipline |

**本节结论**：19 篇已经逐篇抽取 A1-M0--M6，并在单篇 `review.md` 中保留详细证据。SUMMARY 级矩阵说明当前样本已经覆盖元模型、检索分母、主题语义、方法干预、评价证据、统计就绪和 finding 裁决七层，但图表级证据和字段取值饱和仍需 A2a 深化。


## 6.1 维度树模式总览

本节是 PR-A1-DT 后新增的跨论文入口；当前 v2 批次为 [A1-DT v2 19×3 原生维度树审计](./audits/a1dt-v2-19x3/README.md)。旧 [A1-DT v1 19×3 全文审计批次](./audits/a1dt-19x3/README.md) 仅为历史返修来源，不是当前事实口径。A1-M0--M6 说明“方法链条”，而维度树说明“单篇综述内部 schema 如何组织”。当前 19 篇均已在单篇 `review.md` 中新增 `维度树复原` 与 A.1--A.4 审计附录；下表只做总览和跳转，具体证据以单篇为准。

| 年份 | 论文 | 主类型 | 辅助类型 | 后续主统计池候选 | A1-DT 当前允许用途 | 单篇结论标识 | 详情 |
|---:|---|---|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md) | RQ 驱动分类树 | 生产力 benefit-risk 评价树 | 是 | `schema_seed` | `A1DT-llm-assistants-developer-productivity-C01` | [review](./papers/llm-assistants-developer-productivity/review.md#维度树复原) |
| 2026 | [Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap](./papers/ai-native-se-roadmap/review.md) | roadmap / challenge 树 | 理论 / 元模型概念树 | 否 | `boundary_anchor` | `A1DT-ai-native-se-roadmap-C01` | [review](./papers/ai-native-se-roadmap/review.md#维度树复原) |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md) | 证据资产审计树 | artifact availability 统计树 | 是 | `schema_seed` | `A1DT-research-artifacts-secondary-studies-C01` | [review](./papers/research-artifacts-secondary-studies/review.md#维度树复原) |
| 2025 | [On the road to interactive LLM-based systematic mapping studies](./papers/interactive-llm-systematic-mapping/review.md) | 方法流程树 | human-in-the-loop boundary 树 | 否 | `boundary_anchor` | `A1DT-interactive-llm-systematic-mapping-C01` | [review](./papers/interactive-llm-systematic-mapping/review.md#维度树复原) |
| 2025 | [Formal requirements engineering and large language models: A two-way roadmap](./papers/formal-re-llm-roadmap/review.md) | roadmap / concern / action-point 树 | trustworthiness 边界树 | 否 | `boundary_anchor` | `A1DT-formal-re-llm-roadmap-C01` | [review](./papers/formal-re-llm-roadmap/review.md#维度树复原) |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md) | systematic mapping 分类树 | assistant strategy-goal-metric-user 树 | 是 | `schema_seed` | `A1DT-mdse-modelling-assistants-mapping-C01` | [review](./papers/mdse-modelling-assistants-mapping/review.md#维度树复原) |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md) | MDE4ML 生命周期分类树 | 解决方案 / 动机 / 评价树 | 是 | `schema_seed` | `A1DT-mde-ml-components-slr-C01` | [review](./papers/mde-ml-components-slr/review.md#维度树复原) |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md) | 大规模 RQ 驱动分类树 | LLM4SE task-method-evidence 树 | 是 | `schema_seed` | `A1DT-llm4se-systematic-review-C01` | [review](./papers/llm4se-systematic-review/review.md#维度树复原) |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md) | 关系型维度树 | 多声部证据树 | 是 | `schema_seed` | `A1DT-devsecops-primary-dimensions-C01` | [review](./papers/devsecops-primary-dimensions/review.md#维度树复原) |
| 2023 | [Requirements quality research: a harmonized theory, evaluation, and roadmap](./papers/requirements-quality-theory-roadmap/review.md) | 理论 / 元模型概念树 | requirements quality roadmap 树 | 否 | `boundary_anchor` | `A1DT-requirements-quality-theory-roadmap-C01` | [review](./papers/requirements-quality-theory-roadmap/review.md#维度树复原) |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md) | tertiary 主题 / 挑战树 | action recommendation 树 | 是 | `schema_seed` | `A1DT-ml4se-tertiary-study-C01` | [review](./papers/ml4se-tertiary-study/review.md#维度树复原) |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md) | RQ 驱动分类树 | 评价 / 复现资产审计树 | 是 | `schema_seed` | `A1DT-app-reviews-slr-se-C01` | [review](./papers/app-reviews-slr-se/review.md#维度树复原) |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md) | SMS problem-benefit-solution 树 | Agile RE 主题分类树 | 是 | `schema_seed` | `A1DT-re-agile-sms-2015-C01` | [review](./papers/re-agile-sms-2015/review.md#维度树复原) |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md) | mapping guideline update 方法树 | topic-independent dimensions 树 | 是 | `schema_seed` | `A1DT-petersen-2015-mapping-guidelines-update-C01` | [review](./papers/petersen-2015-mapping-guidelines-update/review.md#维度树复原) |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md) | RE tertiary 主题统计树 | 质量 / impact 树 | 是 | `schema_seed` | `A1DT-re-tertiary-study-2014-C01` | [review](./papers/re-tertiary-study-2014/review.md#维度树复原) |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md) | tertiary 更新统计树 | 质量 / 实践影响树 | 是 | `schema_seed` | `A1DT-da-silva-2011-six-years-slr-C01` | [review](./papers/da-silva-2011-six-years-slr/review.md#维度树复原) |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md) | tertiary 生态统计树 | 质量评价树 | 是 | `schema_seed` | `A1DT-kitchenham-2009-slr-tertiary-C01` | [review](./papers/kitchenham-2009-slr-tertiary/review.md#维度树复原) |
| 2008 | [Systematic Mapping Studies in Software Engineering](./papers/petersen-2008-systematic-mapping/review.md) | 方法流程树 | topic-independent taxonomy 示例树 | 否 | `schema_seed` | `A1DT-petersen-2008-systematic-mapping-C01` | [review](./papers/petersen-2008-systematic-mapping/review.md#维度树复原) |
| 2007 | [Guidelines for performing Systematic Literature Reviews in Software Engineering](./papers/kitchenham-charters-2007-slr-guidelines/review.md) | 方法流程树 | 质量 / 效度 guideline 树 | 否 | `schema_seed` | `A1DT-kitchenham-charters-2007-slr-guidelines-C01` | [review](./papers/kitchenham-charters-2007-slr-guidelines/review.md#维度树复原) |

**本节结论**：当前 19 篇不是一个同质字段表，而是至少覆盖六类可迁移树型：RQ 驱动分类树、方法流程树、关系型维度树、证据资产审计树、理论 / 元模型概念树、roadmap / challenge 树。对 Paper2 来说，这说明“维度模式”必须允许研究者从树和关系边中选择、批准和演化，而不能预设为单层表格。

## 6.2 维度树类型与 Paper2 L0--L7 的关系

| 维度树类型 | 支撑的 Paper2 阶段 | 当前样本 | 方法启发 |
|---|---|---|---|
| RQ 驱动分类树 | L0 主题与综述元模型设定；L4 字段级证据抽取；L5 统计分析 | app reviews、LLM4SE、LLM assistants | 先由 RQ 确定对象 / 方法 / 评价 / 结果层，再要求每个叶子绑定证据与分母。 |
| 方法流程树 | L1 脚手架挖掘；L2 维度模式批准；L3 论文收集与概览 | Kitchenham guideline、Petersen mapping guideline、interactive LLM mapping | 用流程阶段和 researcher gate 定义 agent-human 协同，而不是把 SLR 写成一次性自动化。 |
| 关系型维度树 | L4 字段抽取；L5 交叉统计；L6 候选发现形成 | DevSecOps、MDSE assistants、research artifacts | 主干树之外必须保留边表；缺失关系本身可成为 gap 候选。 |
| 证据资产审计树 | L4 证据链；L7 透明投影 | research artifacts、app reviews、DevSecOps | artifact、replication package、open science material 应是一等字段。 |
| 理论 / 元模型概念树 | L0 元模型设定；L6 候选发现启发 | requirements quality、AI-native SE | 可启发概念节点，但需降级为 schema seed / boundary anchor。 |
| roadmap / challenge 树 | L6 候选发现；L7 研究者裁决 | formal RE + LLM、AI-native SE、interactive mapping | action point 只能是候选启发，不能污染主统计池或 final finding。 |

**本节结论**：Paper2 后续实验不应只测“AI 能否抽字段”，而应测研究者如何定义 / 修改维度树、AI 如何给出证据链、统计观察如何被降级为候选发现并交给研究者裁决。

## 6.3 SUMMARY 结论-证据映射

| 归纳标识 | 引用键 | 归纳内容 | 归纳类型 | 分母 | 纳入结论标识列表 | 排除结论标识列表 | 证据强度过滤 | 外推限制 | 允许用于论文的位置 | 当前状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| [sum-A1DT-tree-types] | [sum-A1DT-tree-types] | 当前 19 篇已形成六类维度树类型，总体说明 survey-of-surveys 需要树型 schema 而不是单层字段表。 | tree_type_inventory | 19 篇 `review.md` | A1DT-llm-assistants-developer-productivity-C01, A1DT-ai-native-se-roadmap-C01, A1DT-research-artifacts-secondary-studies-C01, A1DT-interactive-llm-systematic-mapping-C01, A1DT-formal-re-llm-roadmap-C01, A1DT-mdse-modelling-assistants-mapping-C01, A1DT-mde-ml-components-slr-C01, A1DT-llm4se-systematic-review-C01, A1DT-devsecops-primary-dimensions-C01, A1DT-requirements-quality-theory-roadmap-C01, A1DT-ml4se-tertiary-study-C01, A1DT-app-reviews-slr-se-C01, A1DT-re-agile-sms-2015-C01, A1DT-petersen-2015-mapping-guidelines-update-C01, A1DT-re-tertiary-study-2014-C01, A1DT-da-silva-2011-six-years-slr-C01, A1DT-kitchenham-2009-slr-tertiary-C01, A1DT-petersen-2008-systematic-mapping-C01, A1DT-kitchenham-charters-2007-slr-guidelines-C01 | -- | 本行是树型索引，不作定量统计；允许纳入 `weak` 的 boundary / roadmap C01，但它们只可用于 `schema_seed` / `boundary_anchor`，不得进入主统计池或 final finding。 | 这是 A1 样本的结构归纳，不代表 100+ 完整文库已饱和；弱证据只用于边界或启发。 | schema_seed | active |
| [sum-A1DT-statistical-pool] | [sum-A1DT-statistical-pool] | 13 篇完成型 SLR / SMS / tertiary / MLR / systematic mapping 是后续主统计池候选，但 PR-A1-DT 当前维度树证据仍待 A2a 精确锚定，暂不进入 SUMMARY 定量统计。 | pool_candidate_index | 19 篇 `review.md` | A1DT-llm-assistants-developer-productivity-C01, A1DT-research-artifacts-secondary-studies-C01, A1DT-mdse-modelling-assistants-mapping-C01, A1DT-mde-ml-components-slr-C01, A1DT-llm4se-systematic-review-C01, A1DT-devsecops-primary-dimensions-C01, A1DT-ml4se-tertiary-study-C01, A1DT-app-reviews-slr-se-C01, A1DT-re-agile-sms-2015-C01, A1DT-petersen-2015-mapping-guidelines-update-C01, A1DT-re-tertiary-study-2014-C01, A1DT-da-silva-2011-six-years-slr-C01, A1DT-kitchenham-2009-slr-tertiary-C01 | A1DT-ai-native-se-roadmap-C01, A1DT-interactive-llm-systematic-mapping-C01, A1DT-formal-re-llm-roadmap-C01, A1DT-requirements-quality-theory-roadmap-C01, A1DT-petersen-2008-systematic-mapping-C01, A1DT-kitchenham-charters-2007-slr-guidelines-C01 | 本行是候选资格索引，不作定量统计；当前单篇 C01 允许用途为 `schema_seed`，待 A2a 完成精确页码 / 表图 / 字段锚定后才可升级。 | 统计池候选资格只服务后续 A2a/A2b，不支撑目标领域 final finding；弱或待核验证据不得进入定量统计。 | schema_seed | active |
| [sum-A1DT-boundary-anchor] | [sum-A1DT-boundary-anchor] | roadmap / vision / proposal / guideline 的维度树可提供边界锚点和候选启发，但不得进入主统计池。 | downgrade_decision | 19 篇 `review.md` | A1DT-ai-native-se-roadmap-C01, A1DT-interactive-llm-systematic-mapping-C01, A1DT-formal-re-llm-roadmap-C01, A1DT-requirements-quality-theory-roadmap-C01, A1DT-petersen-2008-systematic-mapping-C01, A1DT-kitchenham-charters-2007-slr-guidelines-C01 | A1DT-llm-assistants-developer-productivity-C01, A1DT-research-artifacts-secondary-studies-C01, A1DT-mdse-modelling-assistants-mapping-C01, A1DT-mde-ml-components-slr-C01, A1DT-llm4se-systematic-review-C01, A1DT-devsecops-primary-dimensions-C01, A1DT-ml4se-tertiary-study-C01, A1DT-app-reviews-slr-se-C01, A1DT-re-agile-sms-2015-C01, A1DT-petersen-2015-mapping-guidelines-update-C01, A1DT-re-tertiary-study-2014-C01, A1DT-da-silva-2011-six-years-slr-C01, A1DT-kitchenham-2009-slr-tertiary-C01 | 本行专门记录降级后的 boundary 结论；允许 `weak`，但只用于边界锚点 / 风险提示 / 候选启发，不进入主统计池、SUMMARY 定量统计或 final finding。 | 这些结论仅用于方法设计和风险提示，不能写成经验事实。 | boundary_anchor | active |

**本节结论**：SUMMARY 的跨论文归纳已经显式回链单篇 A.3 结论标识。后续若新增论文或修改树型，必须同步更新本表，否则 SUMMARY 归纳将失去证据链闭环。

## 7. 当前 pattern 总结与 A2a 接力建议

| pattern | 当前观察 | 来源样本 | A2a 处理建议 |
|---|---|---|---|
| RQ pattern | SE tertiary 常问规模、主题、主体、质量、限制、实践影响；现代 LLM4SE SLR 常先给 landscape / method / benefit-risk / dimension coverage。 | Kitchenham 2009、da Silva 2011、LLM assistant SLR、LLM4SE SLR | 建立 RQ 模式树，区分 landscape、method、impact、dimension coverage、gap/finding。 |
| dimension pattern | 维度应树状化而非平铺：strategy-goal-limitation-metric-user、aspect-theme-category、concept-activity-context-impact 等。 | MDSE assistant mapping、DevSecOps MLR、requirements quality roadmap | 把字段树版本化，并记录字段来源、缺失语义和 researcher adoption decision。 |
| finding pattern | finding 需从统计观察进一步形成质量缺口、实践影响、research challenges、roadmap、action recommendations；roadmap 只能提供启发式。 | da Silva 2011、ML4SE tertiary、DevSecOps MLR、requirements quality roadmap | 与 Paper2 的 candidate finding ledger 对齐，补 support / counter-evidence / claim strength。 |
| evidence presentation pattern | 常用搜索分母、纳排、quality assessment、topic taxonomy、review/primary-study 数量、artifact availability、replication package。 | Kitchenham guideline、research artifacts mapping、LLM4SE SLR | 每个字段必须有 source anchor、artifact link status 和回填状态。 |
| validity / threat pattern | 包含 search bias、inclusion reliability、quality assessment、protocol deviation、artifact dead link、model drift、human validation。 | Kitchenham guideline、interactive LLM mapping、research artifacts mapping | 设为强制字段，未报告时明确记录。 |
| report structure pattern | guideline、tertiary/SMS、SLR+SMS、MLR、roadmap 的结构不同；不能用一个模板压平。 | 全文样本 | 允许不同 `review_type` 对应不同报告结构和统计池资格。 |

A2a 第一优先级：不是补历史 PDF，而是对当前 19 篇做图表视觉核对、页码 / 表号证据锚定，并将 A1-M0--M6 矩阵转为更正式的 pattern library；随后扩展到 30--50 篇核心样本，检验字段取值空间和统计池规则是否稳定。

### 7.1 schema 修订 / 回填日志

本节是 A1 字段合同演化的结构化审计入口。它只记录会影响后续 A2a/A2b schema、统计池或字段回填的变更；普通下载、排版或 PR 施工细节仍进入更新日志或 `search/` 审计文件。

| 时间 | 触发条目 / 样本 | 受影响字段 | 修订内容 | 回填状态 | 冻结理由 / 后续处理 |
|---|---|---|---|---|---|
| 2026-06-29 21:10:00 | PR-A1-DT 逐篇维度树复原；19 篇全文样本 | 维度树、叶子取值空间、关系边、结论-证据映射、SUMMARY 归纳回链 | 新增 GUIDE 维度树纪律、schema 字段合同、19 篇 `review.md` 的 `维度树复原` 与 A.1--A.4 审计附录；SUMMARY 新增维度树模式总览和 `[sum-A1DT-*]` 结论-证据映射 | 已回填 19/19 篇 review、GUIDE、pattern schema 与 SUMMARY | Paper2 方法贡献需要可审计维度树，而不是平铺字段矩阵；A2a 继续做页码 / 图表精核与样本扩展。 |
| 2026-06-29 17:48:49 | 用户复核 SUMMARY 批次化问题；19 篇全文样本 | SUMMARY 主表、证据池、A1-M0--M6 总账矩阵 | 取消按 PR 批次拆分主表，改为统一年份降序表；明确三类证据池主归属；新增 19 篇 × A1-M0--M6 覆盖矩阵 | 已回填 SUMMARY、GUIDE、progress 与 task packet | 长期文库必须按对象和当前事实维护，不能按施工批次维护；A2a/A2b 继续沿用统一总账结构。 |
| 2026-06-29 17:58:30 | 三路复审 C/I：CCF 复核状态、三池计数、schema 回修入口 | `ccf_verification_status`、三类证据池计数、schema change ledger | 主表新增 `CCF 复核状态` 列；三类证据池改为主归属计数；恢复本结构化 schema 修订 / 回填日志 | 已回填 SUMMARY、GUIDE、pattern schema、task packet 和 progress | 防止复制主表时丢失 CCF disclaimer；防止方法学样本与边界 seed 重复计数；保留字段回修可审计入口。 |
| 2026-06-29 16:59:12 | 用户补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 PDF | 阅读状态、`eligible_for_statistical_synthesis`、manual-download 状态 | 历史 metadata-only / manual-download 条目升级为全文文本级；active manual-download 清零；Petersen 2008 保持方法学参考池，Petersen 2015 作为方法学统计样本进入主统计池 | 已回填 3 篇 `paper.pdf`、`paper_content.txt`、`review.md`、`metadata.json`、SUMMARY 与 search log | 补齐全文后才能把题摘级候选升级为全文级 pattern；统计池仍按主归属和系统性证据状态控制。 |
| 2026-06-29 15:41:07 | issue #95 十篇现代锚点 | `review_type`、`eligible_for_schema_seed`、`eligible_for_statistical_synthesis`、`evidence_role`、A1-M0--M6 | 扩展 SLR+SMS、systematic mapping、MLR、solution proposal、vision/roadmap、theory/evaluation/roadmap；新增 schema seed 与统计池分离字段；新增 A1-M0--M6 元维度 | 已回填 19 篇 `metadata.json`、单篇 `review.md`、SUMMARY、candidate-pool、GUIDE 和 schema | 现代 roadmap / proposal 有高启发价值但不得污染主统计池；A1-M0--M6 是 A2a/A2b 的元维度接力骨架。 |
| 2026-06-29 13:20:00 | 用户要求补充出版 / venue / CCF 字段 | `publication_type`、`venue_short_link`、`ccf_official_category`、`ccf_official_rank`、`ccf_verification_status` | 将来源字段拆成出版形态、可点击 venue、CCF 大类、CCF 等级和复核状态；官方 WAF 时显式标本地缓存 / 待人工复核 | 已回填 SUMMARY、candidate-pool、单篇 review 和 schema；主表现已补独立 `CCF 复核状态` 列 | 投稿决策需要事实来源可追溯；不能把本地缓存写成官方实时核验。 |
| 2026-06-29 02:18:07 | 初始 6 篇全文 + 3 篇失败路径 dry-run | `review_type`、`predecessor_relation`、`target_se_subfield`、`challenge_action_pattern`、`taxonomy_axis`、`problem_solution_pattern` | 建立六类 pattern 字段；识别 guideline、updated tertiary、SE 子领域和 SMS taxonomy / problem-solution 等候选字段 | 已回填初始 review、pattern schema 与 SUMMARY；后续 3 篇失败路径已在 16:59 补齐 | 证明 schema 不是先验冻结，而是由真实 dry-run 暴露缺口后回修；A2a 继续扩展取值空间。 |

**本节结论**：schema 回修有明确入口、触发条目、受影响字段、回填状态和冻结理由。后续 A2a/A2b 若新增字段或改变统计池规则，必须先在单篇 `review.md` 记录触发原因，再回修 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md)，最后在本节追加结构化记录。

## 8. 失败、风险与待复核

| 风险 | 当前处理 | 后续动作 |
|---|---|---|
| 图表 / 表格未全部视觉核对 | 多数条目已读 `paper_content.txt`，但并非所有图表、表格、页码和 publisher final 差异都核对 | A2a 深读时补页码、表号、图表截图或 source anchors。 |
| CCF 官方目录 WAF | 当前按本地 `ccf_venues/` 缓存标注 TOSEM=A，IST/JSS/RE/ESE=B，EASE=C；CSUR 待核验 | 正式写作 / 投稿前人工打开 CCF 官方页面复核。 |
| roadmap / proposal 误入统计池风险 | 已用 `eligible_for_statistical_synthesis=false` 与排除理由分离 | A2a 扩库时继续执行三池规则。 |
| 方法学样本与领域样本混算风险 | Kitchenham 2007、Petersen 2008 不进主统计池；Petersen 2015 标为方法学统计样本 | A2a 报告统计时分层展示。 |
| 历史 manual-download 路径 | 历史 3 条已由用户本地 Zotero PDF 补齐；[search/manual-download-needed.bib](./search/manual-download-needed.bib) active=0 | 后续新增失败条目继续进入该 BibTeX，补齐后清零或只保留未解决条目。 |

## 9. 后续 A2a / A2b 入口

A2a 建议：

1. 以当前 19 篇为起点，先做图表视觉核对、页码 / 表号锚定和字段证据 source anchors。
2. 扩展到 30--50 篇核心样本，优先覆盖 2020 年后 SE tertiary / SLR / SMS / MLR / survey。
3. 每个 SE 子领域至少覆盖一批样本：Requirements Engineering、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE、SE secondary-study artifacts。
4. 把 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 拆成正式 pattern library，并记录字段来源、取值空间、缺失语义、统计池资格和 researcher adoption decision。
5. 对 roadmap / vision / proposal 保持 boundary / schema seed 池，不混入主统计池。

A2b 建议：

1. 扩展到预计 100+ 篇完整文库闭合。
2. 形成第一个可引用快照。
3. 明确纳排分母、排除理由、人工下载清单、覆盖 / 饱和度判断。
4. 把完整文库快照交给 A3 消费，A3 不再混入大规模补文库。

## 10. 更新日志

| 时间 | 更新内容 | 验证 / 备注 |
|---|---|---|
| 2026-06-29 21:10:00 | 完成 PR-A1-DT 实现：补充 GUIDE 维度树复原规则、pattern schema 字段合同、19 篇单篇 `review.md` 的维度树复原与 A.1--A.4 审计附录，并在 SUMMARY 增加维度树模式总览和 SUMMARY 结论-证据映射。 | A1 原始阶段未读取 `.env`；A1-DT v2 批次已完成 57/57 CLI 审计，日志保留命令/stdout/stderr与环境摘要，关于 `.env` 只记录 `env_sourced=.env exists`，不记录 secret；A1-DT 仍保留 A2a 页码 / 表图精核边界。 |
| 2026-06-29 17:40:27 | 根据用户对 SUMMARY 缝合感和批次拆表问题的反馈，重构 SUMMARY 为长期文库总账：取消批次化主表，改为统一年份降序论文表；补充三类证据池标准；新增 19 篇 × A1-M0--M6 覆盖矩阵；把历史过程下沉为风险 / 日志。 | 本轮只重构总账和规则，不新增论文；后续需同步 GUIDE 与 PR body，并复验 19/19/19/19、active manual=0。 |
| 2026-06-29 16:59:12 | 用户提供 3 篇历史 manual-download PDF 后，补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 的 `paper.pdf`、`paper_content.txt`、全文级 `review.md` 和 `metadata.json`，并将 active 人工下载清单清零。 | 文件系统统计更新为 19 个 `review.md`、19 个 `metadata.json`、19 个 `paper.pdf`、19 个 `paper_content.txt`；3 篇历史失败路径已闭环，剩余风险转为 A2a 图表视觉核对和 CCF 官方人工复核。 |
| 2026-06-29 16:13:28 | 修复三路 reviewer 复审提出的 C/I：补齐早期 9 篇 `metadata.json`，统一 19 篇机器可读字段，修正 CSUR CCF 待核验口径，并清理 `paper_content.txt` 行尾空白。 | `git diff --check` 两点工作区口径通过；提交后需再用 PR 三点 diff 复验。 |
| 2026-06-29 15:41:07 | 根据内部复核修复 A1-M0--M6 命名、SUMMARY 19/16/3 历史总账、#95 metadata 全文状态、roadmap / proposal 统计池排除字段，并记录 CCF 官方页面 WAF 风险。 | 当时文件系统统计：19 个 `review.md`、19 个 `metadata.json`、16 个 `paper.pdf`、16 个 `paper_content.txt`、3 个 manual-download BibTeX 条目；后续 16:59 已补齐为 19/19/19/19。 |
| 2026-06-29 15:37:22 | 完成 #95 十篇现代锚点一致性复验：补 `issue95-selection-audit.md`，统一 `interactive-llm-systematic-mapping` 年份为正式卷期 2025，修复 progress / task packet 19/16/3 历史总账，保持 CCF 字段为“本地缓存；官方待人工复核（WAF）”。 | 当时 `git diff --check` 与 A1 consistency 脚本通过；manual-download-needed 仍为 3 条旧失败路径，后续 16:59 已清零。 |
| 2026-06-29 13:20:00 | 按用户新增要求补充 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 四列，并同步单篇 review 快速卡片、候选池和字段 schema。 | CCF 字段按官方完整目录口径设计；本轮 HTTP/CLI 访问官方页受 WAF 限制，工作表暂用本地缓存并标注正式写作前需人工复核。 |
| 2026-06-29 02:18:07 | 建立 `survey_of_surveys/` README/GUIDE/SUMMARY/search/papers/patterns；完成 6 篇全文文本级 dry-run 和 3 篇 metadata-only 失败路径；回修 schema 字段。 | A1 奠基；未运行真实 LLM，未读取 `.env`，不跑四个真实例子。 |
