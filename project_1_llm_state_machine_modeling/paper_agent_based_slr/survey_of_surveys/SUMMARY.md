# survey_of_surveys/SUMMARY.md：综述之综述文库总账

## 1. 当前文库状态与总判断

本目录是 Paper2 agentic SLR 工作的 **survey-of-surveys 文库**：它不直接回答某个目标软件工程主题的研究现状，而是从软件工程领域已有 SLR / SMS / tertiary study / MLR / guideline / roadmap 中抽取“如何设计综述元模型、维度模式、证据链、统计分析和 research finding 裁决”的可迁移先验。

| 项 | 当前值 |
|---|---:|
| 入账论文 | 19 |
| 完成 `review.md` | 19 |
| 完成 `evidence_chain.md` | 19 |
| 完成 `metadata.json` | 19 |
| 完成 `paper.pdf` + `paper_content.txt` | 19 |
| active `manual-download-needed.bib` 条目 | 0 |
| 可作 模式种子 | 19 |
| 后续主统计池候选 | 13 |
| 非后续主统计池候选 | 6（方法学参考 2 + 边界 / 启发 seed 4） |
| 真实 LLM / `.env` | A1 原始 dry-run 未运行；A1-DT v2 已完成 57/57 CLI 审计，日志保留命令/stdout/stderr与环境摘要，关于 `.env` 只记录 `.env exists`，不记录 secret |
| 四个真实例子 | 不运行；A1 只做文库 dry-run |

**总判断**：A1 当前已经从“最小脚手架”进入“可接力的长期文库起点”状态。19 篇均达到全文文本级，并且 A1-DT v2 已完成 57/57 三路 CLI 审计、19/19 主线程裁决、19/19 单篇 `review.md` 返修和 19/19 `evidence_chain.md` 证据链拆分，可用于验证字段抽取、证据等级、统计池候选过滤、A1-M0--M6 元维度、原生维度树 / 维度森林和失败路径闭环；但这些证据链当前仍按 `schema_seed` / `boundary_anchor` 管理，不能直接进入 Paper2 最终发现 或目标领域定量结论。后续 A2a/A2b 的重点应是扩大样本、补图表/页码级证据锚点、收敛字段取值空间，并记录 researcher adoption decision，完成后才可把候选主统计池升级为正式统计证据。

## 1.1 PR #135 A1-DT v2 抽取与审计口径

A1-DT v2 的核心修正是把“单篇论文原生维度树 / 维度森林”和“跨论文 A1-M0--M6 投影矩阵”分开：每篇 `review.md` 应优先复原原文自己的 RQ、样本单位、抽取字段、分类 schema、统计表、roadmap / guideline stage 与 finding path；A1-M0--M6 只作为跨论文投影层，用于比较和接力，不能反向冒充单篇原生树。v1 审计目录 [audits/a1dt-19x3/](./audits/a1dt-19x3/) 仅作为历史归档；v2 独立入口为 [audits/a1dt-v2-19x3/](./audits/a1dt-v2-19x3/)。

v2 当前总判断：19 篇均具备全文文本、`metadata.json`、`review.md` 与 `evidence_chain.md`，并已完成 57/57 三路 CLI 审计、19/19 人工 adjudication、19/19 单篇返修和 19/19 证据链拆分；其中 13 篇是后续主统计池候选，6 篇因 guideline / roadmap / proposal / theory-roadmap 等性质降级为方法学参考或 boundary seed。v2 表中的样本数量、树型和统计池资格已经回填到当前总账，但仍只能作为 `schema_seed` / `boundary_anchor`；在 A2a 完成页码 / 表图 / supplementary 精核前，不得写成 Paper2 最终发现。


## 1.2 A1 S1--S8 Round 3 独立审计状态

Round 3 是在 A1-DT v2 之后追加的 **19 篇一篇一 agent 独立审计**：每个 subagent 只处理一篇论文，单独阅读 `bibtex.bib`、`paper_content.txt`、`review.md`、`evidence_chain.md`，必要时核对 `paper.pdf`，并把 S1--S8、原生维度树 / 维度森林、统计池资格与 A2a 待核验项写入 [audits/a1-s1s8-19x1/round3/](./audits/a1-s1s8-19x1/round3/)。主线程裁决入口是 [round3-main-adjudication.md](./audits/a1-s1s8-19x1/round3/round3-main-adjudication.md)，任务映射见 [TASKS.tsv](./audits/a1-s1s8-19x1/round3/TASKS.tsv)。

| 项 | 当前状态 |
|---|---:|
| round3 单篇审计文件 | 19 / 19 |
| round3 subagent 状态 | 19 / 19 completed |
| 主线程裁决文件 | 1 |
| 已回填 `review.md` 的 S1--S8 四分栏 | 19 / 19 |
| 已回填 A1/A2a 非最终定量边界 | 19 / 19 |
| 仍需 A2a 精核 | PDF 页码 / 表图 / supplementary / Zenodo / replication package |

**Round 3 总判断**：本轮解决的是“每篇 survey 如何描述自己的样本集合、字段树、维度层级、叶子取值空间、关系边和 finding 路径”这一 schema 设计问题，不解决目标领域最终事实统计。当前 19 篇已经可以作为 Paper2 A3 设计 researcher-defined meta-model、维度树迭代、字段级证据链、统计观察和候选 finding ledger 的模式库；但任何数字、比例、趋势和领域结论仍须等 A2a 精确锚定后才能进入论文级结论。

## 1.3 A1-DT v2 统一总账表（按年份降序）

字段口径：`样本单位` 与 `样本数量` 只记录单篇论文原文自己的 corpus / evidence base；roadmap、vision、proposal、guideline 或 convenience evaluation 若无系统样本库，必须显式降级。`原生树类型` 是单篇原文 schema 的树型判断；A1-M0--M6 只用于后续投影，不在本表中充当原生树。

| 年份 | 论文 | 类型 | venue/source | CCF 大类/等级 | CCF 复核状态 | 样本单位 | 样本数量 | 原生树类型 | 字段来源 | 统计池资格 | v2 审计状态 | review 链接 |
|---:|---|---|---|---|---|---|---:|---|---|---|---|---|
| 2026 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | SLR + SMS | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 / A | 本地缓存；官方待人工复核（WAF） | peer-reviewed 原始研究 | 39 | RQ 驱动分类树 + SPACE/productivity 评价树 | `schema_seed`；全文文本级；表图待 A2a 精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/llm-assistants-developer-productivity/review.md) |
| 2026 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | vision / roadmap | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 / A | 本地缓存；官方待人工复核（WAF） | 无系统样本库；愿景与社区经验来源 | -- | SE 3.0 技术栈 / challenge roadmap 树 | `boundary_anchor`；全文文本级；无系统检索分母 | 否；roadmap 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/ai-native-se-roadmap/review.md) |
| 2025 | Research artifacts in secondary studies: A systematic mapping in software engineering | 系统映射 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | SE 二次研究 | 537 | 证据资产审计树 + artifact availability 统计树 | `schema_seed`；全文文本级；关键表格仍待最终版核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/research-artifacts-secondary-studies/review.md) |
| 2025 | On the road to interactive LLM-based systematic mapping studies | solution proposal | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | 无已执行系统样本库；方法流程 proposal | -- | LLM-supported SMS 方法流程树 | `boundary_anchor`；全文文本级；Fig. 1 / 阶段模型待精核 | 否；proposal 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/interactive-llm-systematic-mapping/review.md) |
| 2025 | Formal requirements engineering and large language models: A two-way roadmap | vision / roadmap | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | 无系统样本库；roadmap concern/action points | -- | concern / mechanism / action-point roadmap 树 | `boundary_anchor`；全文文本级；非系统综述 | 否；roadmap 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/formal-re-llm-roadmap/review.md) |
| 2024 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 系统映射 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | research proposals / MDSE assistant studies | 58 | 系统映射 分类树 + assistant strategy-goal-metric-user 树 | `schema_seed`；全文文本级；分类表待 A2a 精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/mdse-modelling-assistants-mapping/review.md) |
| 2024 | Model driven engineering for machine learning components: A systematic literature review | SLR | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | 原始研究 | 46 | MDE4ML lifecycle / motivation-solution-evaluation 树 | `schema_seed`；全文文本级；appendix / QA 表待精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/mde-ml-components-slr/review.md) |
| 2024 | Large Language Models for Software Engineering: A Systematic Literature Review | SLR | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 / A | 本地缓存；官方待人工复核（WAF） | LLM4SE studies | 395 | LLM4SE task-method-evidence 大规模分类树 | `schema_seed`；全文文本级；ACM final 与 replication package 待核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/llm4se-systematic-review/review.md) |
| 2024 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | MLR | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | white literature + grey literature | 147 | 关系型维度树 + CPTM / thematic synthesis 树 | `schema_seed`；全文文本级；Zenodo 工件待 A2a 精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/devsecops-primary-dimensions/review.md) |
| 2023 | Requirements quality research: a harmonized theory, evaluation, and roadmap | theory / evaluation / roadmap | [RE](https://link.springer.com/journal/766) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | convenience evaluation 原始研究 | 57 | RQT 理论 / 元模型概念树 + 状态评价树 | `boundary_anchor`；全文文本级；非标准 SLR/SMS | 否；theory-roadmap 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/requirements-quality-theory-roadmap/review.md) |
| 2023 | Machine Learning for Software Engineering: A Tertiary Study | tertiary study | [CSUR](https://dl.acm.org/journal/csur) | 待核验 / 待核验 | 官方待人工复核（WAF）；本地未建档 | reviews + traced 原始研究 | 83 reviews / 6,117 个非唯一原始研究覆盖计数 | tertiary 主题 / 挑战 / action recommendation 树 | `schema_seed`；全文文本级；ACM final / arXiv 差异待核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/ml4se-tertiary-study/review.md) |
| 2022 | Analysing app reviews for software engineering: a systematic literature review | SLR | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | 原始研究 | 182 | RQ 驱动分类树 + 评价 / 复现资产审计树 | `schema_seed`；全文文本级；F1--F18 与复杂表格待精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/app-reviews-slr-se/review.md) |
| 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | mapping guideline update / 系统映射之系统映射（systematic map of maps） | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | SE 系统映射 studies | 52 | mapping guideline update 维度森林 + topic-independent dimensions 树 | `schema_seed`；全文文本级；52 为最终 included mapping studies，57 仅为中间候选口径；Appendix A / B 待 A2a 精核 | 是；方法学统计样本 | completed；adjudicated；A2a 待精核 | [review](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | SMS | [SEAA](https://dsd-seaa.com/) | -- / -- | 本轮未定位 CCF 目录条目 | articles | 28 | SMS problem-benefit-solution 树 + Agile RE 主题分类树 | `schema_seed`；全文文本级；短文表格待核对 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/re-agile-sms-2015/review.md) |
| 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | tertiary study | [EmpiRE](https://empire2014.wordpress.com/) | -- / -- | 非 CCF workshop | distinct reviews / publications | 53 reviews / 64 publications | RE tertiary 主题统计树 + quality / impact 树 | `schema_seed`；全文文本级；workshop 短文需降级 | 是；短文边界 | completed；adjudicated；A2a 待精核 | [review](./papers/re-tertiary-study-2014/review.md) |
| 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | updated tertiary study | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | new SLRs in update window | 67 | tertiary 更新统计树 + predecessor/update 关系树 | `schema_seed`；全文文本级；与前序样本合并关系待精核 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/da-silva-2011-six-years-slr/review.md) |
| 2009 | Systematic literature reviews in software engineering – A systematic literature review | tertiary SLR / SE SLR 状态综述 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 / B | 本地缓存；官方待人工复核（WAF） | relevant SLR studies | 20 | early SE SLR 生态统计树 + quality evaluation 树 | `schema_seed`；全文文本级；早期 venue 手工搜索边界 | 是 | completed；adjudicated；A2a 待精核 | [review](./papers/kitchenham-2009-slr-tertiary/review.md) |
| 2008 | Systematic Mapping Studies in Software Engineering | SMS 方法论文 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 / C | 本地缓存；官方待人工复核（WAF） | 方法示例 / illustrative primary-study set | -- | SMS 方法流程树 + keywording / classification facet 树 | `schema_seed`；全文文本级；方法论文不作领域分母 | 否；方法学参考降级 | completed；adjudicated；A2a 待精核 | [review](./papers/petersen-2008-systematic-mapping/review.md) |
| 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | guideline | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- / -- | 非 CCF 技术报告 | 无系统样本库；方法指南 | -- | SLR protocol / search-selection-extraction-synthesis 方法树 | `schema_seed`；全文文本级；规范性指南 | 否；guideline 降级 | completed；adjudicated；A2a 待精核 | [review](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |

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
| 后续主统计池候选 | 论文自身已经执行完成 SLR / SMS / tertiary / MLR / 系统映射；有系统检索或等价语料构造、纳排 / 编码 / 数据抽取、可统计字段或结果；本地至少全文文本级 | A2a/A2b 完成精确锚定后，用于统计字段频次、覆盖度、维度饱和度和 finding 支撑；A1-DT 当前只作 `schema_seed` | 13 |
| 方法学参考池 | guideline、mapping guideline、方法论文；能定义流程、抽取、报告、效度或质量评价规则，但不是普通领域统计样本 | 指导方法设计、schema 设计、证据链设计；不与普通领域统计池混算 | 2 |
| 模式种子 / 边界池（boundary pool） | roadmap、vision、solution proposal、theory roadmap、非标准系统综述但有高价值维度或 finding heuristic | 启发维度、方法边界、人机协同和 finding heuristic；不得污染统计池 | 4 |

上述三类池按“主归属”计数，合计 13 + 2 + 4 = 19，避免同一论文在 SUMMARY 统计中重复计数。当前 `metadata.json` 中 13 篇 `eligible_for_statistical_synthesis=true`，表示它们是后续主统计池候选；6 篇为 `false`，并均写明 `statistical_pool_exclusion_reason`。其中 Kitchenham & Charters 2007 与 Petersen 2008 是非主统计池的方法学参考；Petersen 2015 虽然也是方法学高价值样本，但它本身执行了 系统映射之系统映射（systematic map of systematic maps），因此主归属放在后续主统计池候选，并在解释中标注为“方法学统计样本”。PR-A1-DT 当前 A.2/A.3 若仍含待 A2a 精确页码 / 表图核验，则一律不得作为 SUMMARY 定量统计证据。

### 2.3 出版形态、Venue 与 CCF 口径

本总账固定维护 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 和 `CCF 复核状态`。其中 `期刊/会议/预印本` 使用可点击短名链接；预印本统一写 `[arXiv](https://arxiv.org/)`。主表中的 `CCF 复核状态` 是事实口径的一部分，不得只依赖段落级 disclaimer；复制主表行时必须同时复制该列，避免把本地缓存误写成官方实时核验。

CCF 字段的目标口径是 **CCF 官方最新推荐目录**，不局限于本仓库 [../../../ccf_venues/](../../../ccf_venues/) 已建档范围。2026-06-29 本轮 HTTP/CLI 访问 CCF 官方 [软件工程 / 系统软件 / 程序设计语言目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 返回 Aliyun WAF 壳，当前表格暂采用本地 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 与 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 的已建档缓存作为工作口径；正式写作或投稿前必须人工打开 CCF 官方目录复核。

**本节结论**：本目录应把“是否可统计”和“是否有启发价值”分开管理。后续 A2a 不能因为 roadmap / proposal 学术价值高就把它们纳入统计池，也不能因为 guideline 不进统计池就忽略其方法学价值。

## 3. 统一论文总表（按年份降序）

| 状态 | 年份 | 标题 | 出版形态 | 期刊/会议/预印本 | CCF 大类 | CCF 等级 | CCF 复核状态 | 综述类型 | 模式种子 | 主统计池 | 证据角色 | 关键价值 | 详情 |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 🟢 | 2026 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR + SMS | 是 | 是 | `hybrid_slr_sms_pattern` | 现代 CCF-A LLM4SE SLR+SMS，提供 RQ / SPACE / benefit-risk / mapping hybrid 组织模式。 | [review.md](./papers/llm-assistants-developer-productivity/review.md) |
| 🟢 | 2026 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | vision / roadmap | 是 | 否 | `roadmap_boundary_anchor` | AI-native SE 愿景、技术栈和挑战路线图；启发 boundary / challenge / action 字段。 | [review.md](./papers/ai-native-se-roadmap/review.md) |
| 🟢 | 2025 | Research artifacts in secondary studies: A systematic mapping in software engineering | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | 系统映射 | 是 | 是 | `systematic_mapping_pattern` | 把 secondary-study research artifacts 操作化为可统计字段，支撑证据资产链设计。 | [review.md](./papers/research-artifacts-secondary-studies/review.md) |
| 🟢 | 2025 | On the road to interactive LLM-based systematic mapping studies | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | solution proposal | 是 | 否 | `solution_proposal_boundary_anchor` | LLM-supported 系统映射研究 阶段、人机角色、agent / prompt 风险锚点；不是已执行系统综述。 | [review.md](./papers/interactive-llm-systematic-mapping/review.md) |
| 🟢 | 2025 | Formal requirements engineering and large language models: A two-way roadmap | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | vision / roadmap | 是 | 否 | `roadmap_boundary_anchor` | Formal RE + LLM 双向路线图，启发 trustworthiness concern 与 action point 字段。 | [review.md](./papers/formal-re-llm-roadmap/review.md) |
| 🟢 | 2024 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | 系统映射 | 是 | 是 | `systematic_mapping_dimension_pattern` | MDSE modelling assistants 系统映射，贴近 LLM4modeling 维度树和 taxonomy 设计。 | [review.md](./papers/mdse-modelling-assistants-mapping/review.md) |
| 🟢 | 2024 | Model driven engineering for machine learning components: A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | 是 | 是 | `slr_dimension_pattern` | MDE4ML SLR，提供 motivation / solution / evaluation / limitation 字段模式。 | [review.md](./papers/mde-ml-components-slr/review.md) |
| 🟢 | 2024 | Large Language Models for Software Engineering: A Systematic Literature Review | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 本地缓存；官方待人工复核（WAF） | SLR | 是 | 是 | `slr_field_schema_pattern` | 大规模 LLM4SE SLR，提供任务树、模型/工具、数据/代码、限制和趋势字段。 | [review.md](./papers/llm4se-systematic-review/review.md) |
| 🟢 | 2024 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 期刊 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | MLR | 是 | 是 | `multivocal_review_dimension_pattern` | 多声部综述，提供 white/grey 证据、主题分析、CPTM 模型和开放工件模式。 | [review.md](./papers/devsecops-primary-dimensions/review.md) |
| 🟢 | 2023 | Requirements quality research: a harmonized theory, evaluation, and roadmap | 期刊 | [RE](https://link.springer.com/journal/766) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | theory / evaluation / roadmap | 是 | 否 | `theory_roadmap_schema_seed` | 以理论对象、57 篇状态评价和 roadmap 组织 requirements quality，启发 meta-model-first 写法。 | [review.md](./papers/requirements-quality-theory-roadmap/review.md) |
| 🟢 | 2023 | Machine Learning for Software Engineering: A Tertiary Study | 期刊 | [CSUR](https://dl.acm.org/journal/csur) | 待核验 | 待核验 | 待核验；官方待人工复核（WAF） | tertiary study | 是 | 是 | `tertiary_study_pattern` | 现代大规模 tertiary，提供挑战 / 行动建议 / ML4SE 分类和质量观察模式。 | [review.md](./papers/ml4se-tertiary-study/review.md) |
| 🟢 | 2022 | Analysing app reviews for software engineering: a systematic literature review | 期刊 | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | SLR | 是 | 是 | `slr_field_schema_pattern` | 完整现代 SLR 样本，提供 F1--F18 抽取表、分类 schema、评价质量和 replication package 字段。 | [review.md](./papers/app-reviews-slr-se/review.md) |
| 🟢 | 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | mapping guideline update | 是 | 是 | `mapping_guideline_update_pattern` | 以 系统映射之系统映射（系统映射之系统映射（systematic map of maps）） 更新 SMS guideline，支撑流程、质量、效度和报告结构字段。 | [review.md](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 🟢 | 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | 会议 | [SEAA](https://dsd-seaa.com/) | -- | -- | 本轮未定位 CCF 目录条目 | SMS | 是 | 是 | `systematic_mapping_pattern` | Agile RE SMS，提供 benefit / problem / solution / taxonomy 这类 mapping 字段。 | [review.md](./papers/re-agile-sms-2015/review.md) |
| 🟢 | 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | 工作坊 | [EmpiRE](https://empire2014.wordpress.com/) | -- | -- | 非 CCF workshop | tertiary study | 是 | 是 | `domain_tertiary_study_pattern` | RE 子领域 tertiary，验证 target SE subfield、topic taxonomy、future researcher relevance / roadmap impact / citation impact 字段。 | [review.md](./papers/re-tertiary-study-2014/review.md) |
| 🟢 | 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | updated tertiary study | 是 | 是 | `updated_tertiary_study_pattern` | 更新型 tertiary，提供前序关系、增长/质量、EBSE 实践缺口与候选 finding 模式。 | [review.md](./papers/da-silva-2011-six-years-slr/review.md) |
| 🟢 | 2009 | Systematic literature reviews in software engineering – A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 本地缓存；官方待人工复核（WAF） | tertiary SLR / SE SLR 状态综述 | 是 | 是 | `tertiary_study_pattern` | 早期 SE SLR 状态综述，提供 EBSE 领域的 RQ、质量、主题与报告结构基线。 | [review.md](./papers/kitchenham-2009-slr-tertiary/review.md) |
| 🟢 | 2008 | Systematic Mapping Studies in Software Engineering | 会议 | [EASE](https://conf.researchr.org/series/ease) | 软件工程 / 系统软件 / 程序设计语言 | C | 本地缓存；官方待人工复核（WAF） | SMS 方法论文 | 是 | 否 | `mapping_guideline_pattern` | SMS 方法母文，定义 mapping vs review、keywording、classification facet 和 map 可视化。 | [review.md](./papers/petersen-2008-systematic-mapping/review.md) |
| 🟢 | 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | 技术报告 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) | -- | -- | 非 CCF 技术报告 | guideline | 是 | 否 | `guideline_methodology_seed` | SE SLR 方法指南，提供 protocol、检索、纳排、质量评价、抽取和报告基础。 | [review.md](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |

**本节结论**：统一总表显示，当前 19 篇覆盖 2007--2026 年的软件工程二级研究方法、领域 SLR/SMS、现代 LLM4SE / MDE / DevSecOps / RE 综述和 roadmap 边界样本。后续扩库应继续按年份降序维护总表，不再按 PR 批次拆表。

## 4. 证据池分布与统计池解释

| 池 / 角色 | 当前主归属条目 / 数量 | 说明 |
|---|---|---|
| 后续主统计池候选 | 13 | 可在 A2a/A2b 完成精确页码、表图和字段锚定后，用于统计“综述论文如何组织维度、字段、证据和 finding”。包含 SLR、SMS、tertiary、MLR、系统映射，以及 Petersen 2015 这种已执行“系统映射之系统映射”（系统映射之系统映射（systematic map of maps）） 的方法学统计样本；PR-A1-DT 当前只提供 `schema_seed`。 |
| 方法学参考池 | 2：Kitchenham & Charters 2007、Petersen 2008 | 这些论文定义 SLR/SMS 的流程、keywording、classification、quality / validity 和 reporting 规则；不应与普通领域结果统计混算。Petersen 2015 也有方法学价值，但主归属为主统计池中的“方法学统计样本”，不在本池重复计数。 |
| 模式种子 / 边界池（boundary pool） | 4：AI-native SE roadmap、Formal RE + LLM roadmap、interactive LLM 系统映射 proposal、requirements quality theory roadmap | 这些论文适合启发字段树、人机协同、trustworthiness concern、finding heuristic 和方法边界；不得进入主统计池。 |
| 待人工下载 / metadata-only | 0 | 历史 3 条下载失败已由用户本地 Zotero PDF 补齐；后续新增失败条目必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。 |
| CCF 待官方复核 | TOSEM / IST / JSS / RE / ESE / EASE 本地缓存；CSUR 待核验 | 当前受 CCF 官方 WAF 限制，正式写作前需人工复核。 |

**本节结论**：A1 当前最重要的治理规则是“统计池与 模式种子 池分离”。这能防止 roadmap / proposal 的高价值观点污染统计结论，也能防止 guideline 的方法学价值被错误低估。

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
| A1-M6 | research finding 形成与裁决 | 论文如何从统计观察形成 候选发现、support / counter-evidence、claim strength、scope、researcher adjudication？ | 全文文本级 | finding 不是频次最高项，而是统计观察 + 缺口解释 + 反向证据 + 研究者裁决。 |

## 6. A1-M0--M6 逐篇覆盖矩阵

下表是 SUMMARY 级总账视图。每格只保留短语级贡献；详细证据、可迁移性和不可迁移点见对应单篇 `review.md`。

| 论文 | A1-M0 | A1-M1 | A1-M2 | A1-M3 | A1-M4 | A1-M5 | A1-M6 |
|---|---|---|---|---|---|---|---|
| [LLM assistants productivity](./papers/llm-assistants-developer-productivity/review.md) | LLM assistant 生产力综述元模型 | 39 篇 peer-reviewed studies 与时间窗 | SPACE / task / benefit-risk 分类 | LLM assistant 任务与使用场景 | 生产力指标与 empirical evidence | SLR+SMS 混合统计表 | productivity benefit / risk finding |
| [AI-native SE roadmap](./papers/ai-native-se-roadmap/review.md) | SE 3.0 愿景元模型 | 非系统检索；不采纳 M1 | 五层技术栈与挑战域 | AI teammate / FMware / intent-centric | 经验与社区互动作边界证据 | 不进统计池 | challenge roadmap / action heuristic |
| [Research artifacts in 二次研究](./papers/research-artifacts-secondary-studies/review.md) | secondary-study artifact 元模型 | 537 篇 二次研究 检索与筛选 | artifact reporting / availability 对象 | artifact repository / DOI / by-request 分类 | open artifact 与 dead-link 字段 | A2a 后可统计 artifact 可用性 | reproducibility gap finding |
| [Interactive LLM 系统映射](./papers/interactive-llm-systematic-mapping/review.md) | LLM-supported mapping 方法设想 | solution proposal；不采纳统计分母 | SMS 流程阶段与人机节点 | agents / prompts / interaction roles | traceability、model drift 风险 | 不进统计池 | LLM 介入 mapping 的边界启发 |
| [Formal RE + LLM roadmap](./papers/formal-re-llm-roadmap/review.md) | formal RE 与 LLM 双向路线 | roadmap；不采纳 M1 | formal specification / RE task concern | LLM agents + formal method roles | correctness / fairness / trustworthiness | 不进统计池 | 双向 roadmap 与 trustworthiness heuristic |
| [MDSE modelling assistants](./papers/mdse-modelling-assistants-mapping/review.md) | MDSE assistant landscape | 系统映射 检索与分类 | 策略 / 目标 / 限制 / 指标 / 用户树 | 建模辅助方法与工具 | 指标 / 用户 / 限制证据 | 分类轴可交叉统计 | MDSE assistant gap / opportunity |
| [MDE for ML components](./papers/mde-ml-components-slr/review.md) | MDE4ML 综述对象 | SLR protocol 与 原始研究 | motivations / solutions / lifecycle objects | MDE 方法、建模语言、工具 | evaluation / limitation / artifact | 字段频次与交叉统计 | ML component engineering gap |
| [LLM4SE SLR](./papers/llm4se-systematic-review/review.md) | LLM4SE 任务与效果元模型 | 395 篇研究检索 / 纳排 | SDLC task tree / model / data | LLM 应用方式、工具、模型 | dataset、artifact、evaluation 字段 | 大规模字段统计 | LLM4SE limitation / trend finding |
| [DevSecOps primary dimensions](./papers/devsecops-primary-dimensions/review.md) | DevSecOps primary dimensions | white / grey literature 双轨 MLR | aspect / theme / CPTM taxonomy | practice / tool / metric / lifecycle | Zenodo open artifacts / QA score | CPTM 与 TA 表可统计 | GSE 空白与 challenge-practice-tool-metric finding |
| [Requirements quality roadmap](./papers/requirements-quality-theory-roadmap/review.md) | requirements quality theory 元模型 | 非标准 SLR；57 篇状态评价 | artifact / agent / activity / impact theory | quality model / tool-support 架构 | evaluation status 与 theory evidence | 不进主统计池 | theory gap → roadmap / tool architecture |
| [ML4SE tertiary](./papers/ml4se-tertiary-study/review.md) | ML4SE tertiary 元模型 | tertiary search / 二次研究 | ML4SE topic / challenge 分类 | ML 方法与 SE task 分类 | quality / challenge / action evidence | 大规模 tertiary 统计 | challenge / action recommendation |
| [App reviews SLR](./papers/app-reviews-slr-se/review.md) | app reviews for SE 元模型 | 1656→182 纳排链条 | review type / technique / SE activity | mining technique 与 analysis type | F1--F18、evaluation、replication package | 多套 classification schema | support-to-SE finding 与评价缺口 |
| [Petersen 2015 mapping update](./papers/petersen-2015-mapping-guidelines-update/review.md) | SMS guideline update 元模型 | mapping studies 检索 / snowballing | topic-independent dimensions | SMS planning-conducting-reporting | quality rubric / validity taxonomy | systematic maps of maps | guideline update finding |
| [Agile RE SMS](./papers/re-agile-sms-2015/review.md) | Agile RE mapping scope | 28 articles mapping | benefit / problem / solution taxonomy | Agile RE practice categories | 短文证据与缺失 threat | 小规模 taxonomy 统计 | definition ambiguity / solution gap |
| [RE tertiary](./papers/re-tertiary-study-2014/review.md) | RE 子领域 tertiary scope | distinct reviews / publications | RE topics / 质量 / citation impact / future researchers | RE research method overview | quality / impact evidence | distinct review vs publication 分母 | RE SLR quality / impact finding |
| [da Silva 2011 updated tertiary](./papers/da-silva-2011-six-years-slr/review.md) | updated tertiary 元模型 | 新旧 tertiary 合并与增量检索 | SE topics / author / institution | EBSE practice and education dimensions | quality assessment / relevance evidence | longitudinal / update 统计 | growth + quality + practice gap |
| [Kitchenham 2009 tertiary SLR / SE SLR 状态综述](./papers/kitchenham-2009-slr-tertiary/review.md) | early SE SLR ecosystem | SLR collection and screening | topic / quality / method dimensions | EBSE method usage | quality and reporting evidence | early tertiary summary statistics | SE SLR adoption / quality finding |
| [Petersen 2008 SMS method](./papers/petersen-2008-systematic-mapping/review.md) | SMS vs SLR 方法元模型 | 方法示例；不进主统计池 | topic / contribution / research type facets | keywording 与 classification process | map / bubble plot / rationale evidence | 方法级频数示例 | mapping 用于识别研究空白 |
| [Kitchenham & Charters 2007 guideline](./papers/kitchenham-charters-2007-slr-guidelines/review.md) | SLR protocol 元模型 | guideline；不进主统计池 | RQ / population / intervention / outcome | search / selection / extraction / synthesis process | quality assessment / data extraction forms | 方法标准，不做统计池 | reporting / validity / protocol discipline |

**本节结论**：19 篇已经逐篇抽取 A1-M0--M6，并在单篇 `review.md` 中保留详细证据。SUMMARY 级矩阵说明当前样本已经覆盖元模型、检索分母、主题语义、方法干预、评价证据、统计就绪和 finding 裁决七层，但图表级证据和字段取值饱和仍需 A2a 深化。


## 6.1 survey_of_surveys 自身 S1--S8 schema

本节把 `survey_of_surveys/` 自身也当作一篇脚手架综述来维护：每篇样本论文不仅要复原自己的原生维度树，还要投影到 S1--S8，便于后续 A2a/A2b 汇总“SE 综述通常如何设定任务、构造语料、定义维度、形成统计观察和 research finding”。S1--S8 是二级汇总 schema，不替代单篇原生维度树，不产生目标领域最终发现。

本轮 S1--S8 抽取已按“一篇论文至少一个独立 subagent”完成 19/19 篇只读审计；批次证据入口为 [audits/a1-s1s8-19x1/](./audits/a1-s1s8-19x1/)，其中 [TASKS.tsv](./audits/a1-s1s8-19x1/TASKS.tsv) 记录 19 个唯一 agent 与任务状态，`results/<slug>.md` 保存独立审计输出或忠实压缩归档，`adjudications/<slug>.md` 保存主线程采纳 / 不采纳裁决。重复调度的 `research-artifacts-secondary-studies` 另有多路 sanity check，最终以主线程裁决后的 `review.md` 表格为当前事实口径。

**四分栏拆分纪律**：每篇单篇 `review.md` 的 S1--S8 小节除等级表外，必须额外保留 `S1--S8 四分栏证据拆分` 表，把 `原文证据`、`维度树复原`、`统计池资格` 和 `A2a 待核验` 分开。这样做是为了避免后续 A2a / A2b 把本地维度树解释、roadmap 启发或文本级统计观察误读为最终定量证据。

### 6.1.1 S1--S8 定义与判定标准

| 维度 | 操作化问题 | 强 | 中 | 弱 / 不适用 | 当前用途 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 原文如何定义综述对象、RQ、scope、review type 与样本单位？ | RQ / 目标 / scope / review type 明确且有证据。 | 目标明确但需本地降级解释。 | 仅愿景 / 议程 / 概念启发，或原文不支持。 | 判断后续是否能作为领域综述样本或边界锚点。 |
| S2 语料收集与筛选 | 原文如何建立语料、检索、纳排、质量评价和分母链？ | 系统检索或等价语料构造完整，分母链可复验。 | 有部分语料流程但分母、QA 或裁决不完整。 | 只有叙事来源或无语料流程。 | 控制主统计池资格，避免 roadmap/proposal 混入统计。 |
| S3 原生维度树 / 样本编码对象 | 原文如何描述每个样本：样本单位、抽取表、分类树、路线图 action 或 guideline item？ | 样本单位和维度树 / 森林清楚。 | 可复原但需 roadmap/guideline/proposal 降级。 | 只有概念分组或无编码对象。 | 建立后续维度模式库的核心入口。 |
| S4 字段级证据 | 原文是否给出字段、样本 ID、表格、附录、制品或证据锚点支撑抽取？ | 字段级证据能回链具体表格 / 样本 / ID。 | 字段存在但页码、图表或 supplementary 待 A2a 精核。 | 只有概念字段或无字段证据。 | 决定字段是否能进入可审计 claim map。 |
| S5 维度模式演化 | 原文是否说明维度如何通过先验、开放编码、主题分析、指南更新或作者讨论形成？ | 有明确编码 / 分类 / guideline update / thematic analysis 过程。 | 能推断演化但缺版本或分歧记录。 | 只有路线图链条或无演化说明。 | 支撑 Paper2 的 researcher-defined meta-model 迭代机制。 |
| S6 统计分析 | 原文是否把字段数据转成频次、比例、趋势、交叉表、模型或系统观察？ | 有分母清晰的统计结果。 | 只有局部统计或方法示例。 | 只有枚举、叙事总结或无统计。 | 区分统计观察与开放性 finding。 |
| S7 候选 finding | 原文是否从数据 / 统计 / 讨论形成 gap、challenge、roadmap、recommendation 或候选发现？ | finding 与字段 / 统计 / 证据关系清楚。 | 有 finding 模式但领域结论需降级。 | 只有愿景、proposal 或无 finding。 | 支撑 Paper2 的 finding heuristic 与 claim strength 设计。 |
| S8 研究者 / 作者质疑与裁决 | 原文如何记录筛选 / 编码分歧、复查、QA、threats、人工覆盖或 override？ | 有明确多研究者裁决、一致性或质量控制记录。 | 有 pilot、QA、会议、复核或 threats，但无完整裁决日志。 | 只有一般限制，或无裁决机制。 | 支撑 human-in-the-loop 与 evidence challenge 设计。 |

**本节结论**：S1--S8 把导师讨论中的“三阶段 SLR + 维度模式 + 统计分析 + research finding + 人类质疑裁决”落成可检查 schema。它的重点不是评价论文好坏，而是判断一篇综述能为 Paper2 方法的哪个环节提供可迁移模式、哪些只能作为边界启发。

### 6.1.2 S1--S4 逐篇覆盖矩阵

| 年份 | 论文 | S1 任务设定 | S2 语料筛选 | S3 原生树/编码对象 | S4 字段级证据 |
|---:|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文设定为围绕 LLM-assistants 对软件开发者生产力影响的 SLR+SMS，RQ0--RQ3 覆盖研究图景、方法实践、收益/风险和 SPACE 维度映射。 | 强：给出数据库、控制论文、五轮 query iteration、纳排标准、Rayyan 筛选、snowballing、QA 排除和 9756→8953→228→44→39 的分母链。 | 强：原生编码对象是 39 篇 peer-reviewed 原始研究 PS1--PS39，维度结构是以 PS-id 为主键的多根 RQ 维度森林。 | 强：字段级抽取覆盖 study goals、tools、strategy/design、tasks、settings、key results、instrument、metric、benefit/risk、SPACE mapping，并通过表格和 PS-id 保持可追踪。 |
| 2026 | [Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap](./papers/ai-native-se-roadmap/review.md#survey_of_surveys-自身-schema-抽取) | 弱：本文是 AI-native SE / SE 3.0 的愿景与挑战路线图，不是 SLR/SMS/tertiary；可作为边界启发和 roadmap 样本。 | 弱：作者提到学术/灰色文献、workshop、客户讨论、内部经验和 OPEA 工业互动，但未给检索式、数据库、纳排、筛选分母或质量评价。 | 中：原生对象不是论文样本，而是 3 个 SE 时代、5 层 SE 3.0 技术栈组件、5 个主挑战与 OQ1--OQ14；§4.6 是 OQ7--OQ14 附加开放问题，§4.6 不是第 6 个主挑战。 | 中：可抽取技术栈组件、挑战模板、影响范围、开放问题和证据来源类型等路线图字段，但这些字段服务于边界启发而非系统综述证据表。 |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是软件工程二次研究的系统映射，任务是审计 research artifact 的报告、可获得性、存放方式与时间/venue 影响。 | 强：使用 Scopus、16 个 ISSN token / 15 个期刊、标题综述类关键词与 2013--2023 年窗口检索，643 篇初始结果经 IC1--IC3 筛选后纳入 537 篇。 | 强：样本单位是每篇 secondary study；原生编码字段包括 year、venue、artifact availability、permanent repo、by request、dead link、dedicated section；logistic regression 属于派生统计输出，不是逐样本编码叶子。 | 中：正文支持聚合字段与统计表，但未核验 Zenodo 原始逐篇清单；当前强在 aggregate table，sample-level artifact list / sample ID / artifact link 待 A2a/Zenodo 核验。 |
| 2025 | [On the road to interactive LLM-based systematic mapping studies](./papers/interactive-llm-systematic-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文是 solution proposal，讨论如何以 human-in-the-loop 方式把 LLM 嵌入系统映射研究流程；无正式 RQ 表、已执行 SMS、样本单位或综述 protocol。 | 不适用：原文未执行系统检索、纳排或语料构建；10 条参考文献仅作叙事旁证，不能计入统计池。 | 中：原生对象是 LLM-supported SMS 流程阶段、角色和交互节点的降级概念维度森林，而非原始研究样本编码 schema。 | 中：可抽取阶段、研究者输入、interactive refinement、LLM output 和 search 三智能体；override、source location、borderline 等是 Paper2 本地审计增强字段，不是原文明示字段。 |
| 2025 | [Formal requirements engineering and large language models: A two-way roadmap](./papers/formal-re-llm-roadmap/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文是 vision/roadmap，任务设定为双向讨论 LLM 支持 formal RE/FM 与 FM 提升 LLM-based RE 的 correctness/fairness/trustworthiness。 | 不适用：原文无系统检索、纳排、质量评价、数据抽取或 PRISMA 风格流程；声明无数据使用，因此不进入统计池。 | 中：原生结构可降级复原为双根 roadmap 森林：Roadmap A 5 个 discussion topics / 7 条 Action Point statements，Roadmap B 7 个 discussion topics / 7 条 Action Point statements，另有 7 项 practical considerations；它不是样本编码树。 | 中：可抽取 action-point 级字段：direction、layer、action point、concern、mechanism、artifact in/out、recommendation、supporting refs 和 evidence strength。 |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文以“辅助人类在 MDSE 工具中完成软件建模任务”为主任务，采用 MRQ 统领文献侧 RQ1--RQ3 与实践侧 RQ4。 | 强：文献侧采用五个数据库检索、PICO search string、I/E criteria、QA 与滚雪球，形成 3176 条筛查记录到 58 个研究提案；实践侧覆盖 Gartner MQ 2023 相关平台文档。 | 强：原生结构是维度森林：文献侧以提案为编码对象，按策略、目标、限制、指标、目标用户五类树编码；实践侧把工具文档 quote 投影到同一编码体系。 | 中：有 RQ 驱动抽取规则、Table 2--5 和实践 quote，但当前证据链仍多为树级泛定位，尚未逐字段精确到页码、表号、样本 ID 或 Zenodo raw data。 |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是 Kitchenham-style SLR，任务设定为系统综述 MDE4ML 的 motivations、approaches/tools、evaluation、limitations/future work。 | 强：自动检索 7 个数据库，3934 条去重至 3570 条，经三轮筛选得 32 篇，再 snowballing 增补 14 篇，最终 46 篇。 | 强：样本编码对象为 P1--P46 原始研究；原生结构为 Fig. 5 单根 feature tree，并辅以纳排 schema 与 QA1--QA5 质量量规。 | 强：原文用 40-question Google Form、5 个 section 和 Table 3--8/QA 表把 RQ 映射为 goal、ML technique、domain、tool、evaluation、limitations 等字段；raw 40-question form 与完整 Fig. 5 树待数据仓库/PDF 精核。 |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md#survey_of_surveys-自身-schema-抽取) | 强：该文以 LLM4SE 为对象，设置 RQ1--RQ4 覆盖模型、数据、优化/评价和 SE 任务，并声明采用 Kitchenham-style SLR。 | 强：语料覆盖 2017 年 1 月至 2024 年 1 月，论文收集截止日为 2024-01-31；经 QGS、7 个数据库检索、多阶段过滤、QAC 质量评估和 snowballing，最终纳入 395 篇。 | 强：样本编码对象是一篇 LLM4SE primary study；原生结构是 4 个 RQ 展开的维度森林，并由 Table 5 的 8 项 data items 串联。 | 强：字段级证据由 Table 5 定义字段合同，并通过 Appendix A--E 将 data type、input form、prompt、metric、SE task 等取值回链到 primary-study references。 |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文明确设定为 DevSecOps 的多声部文献综述，RQ1 抽取 aspects/themes/links，RQ2 检查 GSE context 中的应用空白。 | 强：采用 white literature + grey literature 双轨检索、两套 search string、纳排、QA 和 snowballing；confirmatory search 只作新近验证，不进入 TA/CPTM 主统计语料。 | 强：原生结构是 5 个 aspect 构成的维度森林，并以 text segment/code/theme/category 到 CPTM 节点与关系边为编码对象。 | 强：字段级证据覆盖 definitions、challenges、practices、metrics、tools 的 text segment/code/theme/category 计数、ID、频次、source-ID 与关系映射；CPTM 关系边与 Zenodo full model 待 A2a 精核。 |
| 2023 | [Requirements quality research: a harmonized theory, evaluation, and roadmap](./papers/requirements-quality-theory-roadmap/review.md#survey_of_surveys-自身-schema-抽取) | 强：原文明确 VIEW POINT / research commentary 类型，并给出 RQT 理论统一、requirements quality literature survey、roadmap 三段式贡献；§4 还明确 RQ、target population 与 57 篇样本单位。 | 中：被评价语料为作者前作 quality-factor ontology 中继承来的 57 篇原始研究，样本单位和分母清楚，但属于 convenience sampling。 | 强：原生结构是维度森林：RQT 11 概念元模型、57 篇样本编码的 categorical-variable codebook、6 条 roadmap streams；其中只有树 B 是真正样本编码树。 | 中：字段结构与多项分母可复原，但若干 leaf/code 依赖 Fig. 4、Zenodo replication package 或 A2a 精核；当前不宜写成字段级证据充分。 |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是 ML4SE 三级研究，目标是系统收集、质量评价、汇总并分类二次研究，围绕 SE task 覆盖、欠研究 KA 与 ML technique 三个 RQ 展开。 | 强：语料链为 1567 去重结果 → 140 候选 → 83 篇 QA≥2.0 的二次研究，采用数据库检索、手工检索、snowballing、IC/EC、Kappa≥0.8 双人选择与 DARE-4 质量评估。 | 强：原生编码对象是 83 篇二次研究，维度树是共根维度森林：书目信息、研究设计、质量评价、primary 覆盖度、SWEBOK KA×SE task、ML 四轴、建议、威胁和复现制品。 | 中：字段清单充分，但多依赖 Table 3--7、Fig. 3--6 与 supplementary；当前图表/表格和部分 sample-level 字段待 A2a 精核。 |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文以 app reviews 如何支持软件工程活动为综述对象，RQ1--RQ5 覆盖分析类型、挖掘技术、SE activity、评价方法与评价结果。 | 强：本文遵循 Kitchenham 与 PRISMA 风格流程：1656 个初始命中减去 303 个重复后筛选 1353 个题摘，保留 128 篇初始纳入并经手工检索 14 篇、snowballing 40 篇扩展至 182 篇。 | 强：样本编码对象为 182 篇 peer-reviewed 原始研究；原生结构包括 F1--F18 抽取表、3 套分类 schema、SE activity 树和评价/复现资产字段。 | 强：Table 3 的 F1--F18 字段覆盖书目信息、分析类型、技术、SE 活动、评价流程/指标/结果、标注数据集、质量量规和 replication package。 |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文以“对 SE 系统映射研究做系统映射并更新 mapping guideline”为任务，RQ 覆盖 guideline 使用、SE topic、venue/year 与 mapping process 执行。 | 强：有数据库、检索式、时间窗、去重、题摘、全文、snowballing、QA 和回补排除研究；57 是 QA 中间候选，52 是 final included mapping studies 分母。 | 强：被编码样本单位是 52 篇 SE 系统映射研究，原生结构是抽取表单树、分类切面树、guideline action/rubric 树和 validity taxonomy 树组成的维度森林。 | 中：Table 3 与 Appendix B 支撑字段级编码，但当前核心证据多为 not_verified / 待 A2a 图表核验；字段存在性强，逐样本表格数值仍待精核。 |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是面向敏捷软件开发中需求工程的 SMS，显式提出 3 个 RQ：研究分布、收益、问题及对应解决方案。 | 强：作者使用 Scopus、给出检索式和 2014-09 时间窗，并保留 241→187→65→28 的筛选分母链。 | 强：被编码对象是 28 篇原始研究 S1--S28，原生结构为 venue/context/article-type/benefit/problem-solution 维度森林，其中 problem→solution 是显式关系边。 | 中：叶子字段覆盖检索库、检索式、分母链、venue、agile context、article type、B1--B6、P1--P6 与 solution 关系；短文表格和页码待 A2a PDF 视觉核验。 |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是 RE 领域三级研究，目标是综览 RE SLR，并回答覆盖领域、发表 SLR 质量、覆盖缺口 3 个 RQ。 | 强：作者采用 5 个数据库、snowball、手工 venue 扫描与 3 条纳入标准，形成 64 publications / 53 distinct SLR 的最终语料，QA 分母为 51。 | 强：原生编码对象是 distinct SLR study，维度森林包括 publication metadata、SLR 抽取信息、topic group、scope、QA rubric、citation/impact、gap taxonomy 和 publication type。 | 中：核心叶子字段、QA rubric 与 Appendix S-ID 可复原，但图表/页码/样本级精确证据待 A2a PDF 核验，当前不宜写强。 |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是更新型三级研究，新增检索窗口为 2008-07-01 至 2009-12-31，整合 OS/FE 后覆盖 2004-01-01 至 2009-12-31，设置 RQ1--RQ5 比较数量增长、主题覆盖、作者/机构、既有限制与质量提升。 | 强：语料通过 6 个自动数据库、13 个手工源和回溯引用收集；77 个 unique SLRs 进入 QA 与 data extraction，排除 10 篇后最终 SE 分析分母为 67，整合 OS/FE 后 N=120。 | 强：主样本单位是已发表二级研究，SE 新增 67 篇、整合 OS/FE 后 N=120；原生结构为抽取表、QA 量规、主题分类、人员关系和更新关系维度森林。 | 强：原文明示 10 个抽取字段和 QA1--QA4 评分量规，并在 Table 2/Table 3/Table 5 等表中实例化样本级编码。 |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文明确设定为对 2004 年以来 SE 领域 SLR/MA 的 tertiary SLR，RQ 覆盖活动量、主题、研究者/机构和研究限制。 | 强：语料通过 10 个期刊、4 个会议、个人/网站补检索形成，具备显式纳排标准和 2506→33→19、外部补入至 N=20 的分母链。 | 强：原生编码对象是 20 篇二次研究，主树为 SLR/MA 抽取编码表，并列 DARE 质量评价子树与检索漏斗子树。 | 强：叶子字段包括来源、年份、文章类型、主题类型、主题领域、作者/机构/国家、EBSE 引用、实践者指南、一级研究数、QA1--QA4、漏斗字段和排除原因。 |
| 2008 | [Systematic Mapping Studies in Software Engineering](./papers/petersen-2008-systematic-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文是 SMS 方法学论文/方法学种子，目标是说明如何开展 systematic mapping、比较 SMS 与 SLR，并给出指南；它自身不是 RQ-driven 普通综述统计样本。 | 中：内嵌 Tree A 的 10 篇 SE SLR 有 21 篇候选→8 篇并补 2 篇的检索与纳排链；Tree B 的 2 个 mapping 示例不是系统检索样本。 | 强：原生结构为维度森林：A=10 篇 SLR 特征化表，B=2 个 mapping 示例对比表，C=三 facet 分类方案，D=SMS 五步流程管线。 | 中：Table 4/5 对 n=10 SLR 有字段级表格和样本 ID；short rationale 是作者建议的证据链机制，原文未公开逐篇 rationale 表。 |
| 2007 | [Guidelines for performing Systematic Literature Reviews in Software Engineering](./papers/kitchenham-charters-2007-slr-guidelines/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文是 SE SLR 方法学指南，目标清楚但自身不是 RQ-driven SLR/SMS，缺少普通综述样本单位；主归属为方法学参考/模式种子。 | 中：主体没有系统检索/纳排样本库；Appendix 2 对 2004--2007 上半年 15 篇 SE SLR 有局部收录和 DARE 分数。 | 中：原生对象是 guideline item / 方法组件森林：RQ、PICOC、protocol、search-doc、bias、quality checklist、data extraction、synthesis、report structure 等；不是普通样本文献编码树。 | 强：叶子表列出 question type、PICOC、protocol components、search-doc、bias type、quality items、extraction fields、effect measures、report sections、Appendix 2 topic/DARE 字段。 |

**本节结论**：完成型 SLR/SMS/tertiary/MLR 普遍在 S1--S4 上较强；roadmap、vision、solution proposal 和 guideline 需要在 S1/S3/S4 中显式降级，不能因为能贡献结构种子就混入普通统计池。A2a 不应只扩论文数量，还要优先补强字段级证据可回链、图表/页码/制品可复验的样本。


### 6.1.3 S5--S8 逐篇覆盖矩阵

| 年份 | 论文 | S5 模式演化 | S6 统计分析 | S7 候选 finding | S8 质疑与裁决 |
|---:|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文体现外部分类法 + emergent thematic coding：先用既有 taxonomy/SPACE 框架，再经 targeted thematic analysis 形成 benefit/risk 与 SPACE sub-dimensions。 | 强：RQ0--RQ3 将字段表转化为频次、比例、分布、交叉关系、组合覆盖和缺口统计。 | 强：本文从统计观察与 discussion 形成候选发现，并保留 contested finding 与边界条件，例如 code quality 同时作为 benefit/risk。 | 中：本文没有正式裁决日志或一致性系数；有搜索式集体确认、excluded paper 复查、weekly meetings、citation-against-original-text 回查，但 initial screening/data extraction 主要由第一作者执行。 |
| 2026 | [Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap](./papers/ai-native-se-roadmap/review.md#survey_of_surveys-自身-schema-抽取) | 弱：原文只呈现从 SE 时代对照到技术栈再到挑战/OQ 的愿景链条，未报告编码、分类、开放编码或路线图修订过程。 | 弱：原文没有系统统计分析；只能记录技术栈组件、开放问题和挑战覆盖矩阵这类封闭枚举，不进入主统计池。 | 中：可作为候选 finding 启发的是 limitation → stack component → open question → vision 的路线图链条，所有领域主张均按愿景边界降级。 | 弱：原文没有系统综述式编码分歧和裁决机制；仅有开放讨论与限制提醒，可作为 Paper2 需要裁决日志的反面边界样本。 |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md#survey_of_surveys-自身-schema-抽取) | 弱：原文没有说明字段、代码本或分类方案如何形成/迭代；year trend 是 artifact availability 等字段取值变化，不是 schema 演化。 | 强：统计分析包括 venue/year 交叉表、537/169/79 等分母切换，以及以年份和期刊预测 artifact availability 的二元 logistic regression。 | 强：候选发现是二次研究 artifact availability 在增长，但永久仓库/DOI 采用不足，Data Availability section 的表面透明度风险（作者批评，强度低于 169/537、65/169 等统计 finding）。 | 中：原文有人工筛选、Krippendorff’s Alpha、一致性评估、人工检查关键词上下文和 limitations，但无完整 disagreement adjudication log。 |
| 2025 | [On the road to interactive LLM-based systematic mapping studies](./papers/interactive-llm-systematic-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 弱：原文没有 corpus coding saturation 或维度迭代记录，只能把方案迭代和端到端 prototype 路线作为边界启发。 | 不适用：本文无自身统计分析、数据表和分母；被引文献中的 recall/precision/prompt 表现只能作为旁证。 | 中：可作为候选 finding 的是方法学设计 claim：LLM 可辅助 SMS 各阶段，但必须保留专家在环、可复现检索、证据追踪和后续 SE-specific evaluation。 | 弱：原文有 human oversight、研究者验证 LLM 输出、rationale/citation/traceability 要求，但没有多研究者裁决协议、一致性、QA 日志或正式 override 机制。 |
| 2025 | [Formal requirements engineering and large language models: A two-way roadmap](./papers/formal-re-llm-roadmap/review.md#survey_of_surveys-自身-schema-抽取) | 弱：原文没有跨样本维度演化过程；可作为 concern → mechanism → artifact → action 的路线图字段种子。 | 不适用：无统计表、频次分布、样本分母或编码分布；Roadmap A/B 的 action points 只作候选启发。 | 中：可提取 prompt 即需求、formal verification/runtime monitoring/ethical requirements 作为控制机制等候选启发，但均按 roadmap 证据降级。 | 弱：原文无正式编码裁决；§7 practical considerations 只是专家协作、评价困难、overreliance、人类质量控制和技术演化的限制讨论。 |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 中：维度模式来自 RQ 驱动的数据抽取与术语聚类，并承认 tool/method/technique/framework 等边界存在主观解释。 | 强：原文给出分母链、策略比例、目标/限制报告率、指标/目标用户比例、实践侧文档缺失率，并用 bubble chart / comparative analysis 连接字段；最终定量需 A2a 精核。 | 强：限制、指标、目标用户报告不足有统计支撑；AI/LLM 改变 modelling assistance 的判断只作中/弱候选启发，不能与字段统计支撑 finding 混写。 | 中：原文具备多 reviewer 筛选、Kappa agreement、R3/R4 复核讨论、triangulation 和 threats 分析；数据抽取阶段裁决仍待 A2a 精核。 |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md#survey_of_surveys-自身-schema-抽取) | 中：原文说明 search string 多次修改、数据抽取前 pilot 6 篇并与其他作者对照，术语不一致经讨论达成共识；但缺少完整字段变更日志。 | 强：本文将字段表转化为 Venn、bubble chart、分布图、频次表、QA 分布和 RQ Answer Summary。 | 强：RQ Answer Summary 和 Discussion roadmap 形成候选发现，例如 effort reduction 主导、monitoring/documentation 被忽视、industrial/user study 不足和 responsible ML 需加强。 | 中：原文有 protocol review、cross-validation、pilot extraction、作者讨论和 threats，但没有双人独立编码比例、disagreement 统计或逐条裁决日志。 |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md#survey_of_surveys-自身-schema-抽取) | 中：RQ/字段形成参考 Kitchenham 与前序 DL4SE 综述，并在 full-text review 中抽取 Table 5 字段；原文未暴露 open coding、schema revision history 或 conflict log。 | 强：该文提供 N=395 主分母、数据源/输入形式子分母、架构年度趋势、SDLC 阶段分布、problem type 与 metric 分布。 | 强：原文将统计观察提升为 challenges、opportunities 与 roadmap；对 Paper2 只迁移 finding 生成模式，不迁移 LLM4SE 领域结论。 | 中：该文有 QAC、两名 reviewers secondary review、threats 和 replication package 作为质量控制机制，但缺少字段级 coder agreement 与冲突解决日志。 |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md#survey_of_surveys-自身-schema-抽取) | 强：明确呈现从 inductive thematic analysis 的 text → code → theme → category 到 lifecycle/CPTM model 的模式演化，并区分 WL 归纳与 GL 演绎分析。 | 强：提供各 aspect 的主样本分母、text segment/code/theme/category 数量、C/P/T/M 项数、频次和 WL/GL 差异；confirmatory search 仅作验证性补充。 | 强：候选发现包括实践最受关注、metrics 最薄弱、WL/GL 互补、Business challenges 在 WL 中存在、GL 中 business-related challenges = 0，business metric M20 来自 prior MLR 补入、GSE 缺失和 framework design 趋势；其中 confirmatory finding 单独降级。 | 中：原文没有独立质疑-裁决流程，但有 reflexive thematic analysis 的多作者审核协商、trustworthiness 讨论、threats 与开放材料审计。 |
| 2023 | [Requirements quality research: a harmonized theory, evaluation, and roadmap](./papers/requirements-quality-theory-roadmap/review.md#survey_of_surveys-自身-schema-抽取) | 中：维度模式体现为先由 RQT 概念派生抽取变量，再在第一轮 ad hoc 创建代码、第二轮通过讨论与理论背景精炼。 | 中：原文有 n=57、impact 子集 n=40、多项比例与 reliability 指标，能支撑本文内部 descriptive statistics；但样本为 inherited convenience sample，不能进入 Paper2 主统计池。 | 中：候选 finding 形态是字段覆盖缺口 → 方法风险 → roadmap/action stream，例如 artifact-centric 覆盖较好而 activity/context/economic 侧覆盖不足。 | 中：本文有等价质量控制机制：第一作者全量编码、第二作者约 10% 样本 instrument validation、reliability 报告和 threats 中的隐式抽取/convenience sample 风险。 |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文体现既有分类轴 + 开放编码/事后归纳的混合演化：SWEBOK 与 ML 四轴作为先验框架，SE task、ML application task 与 implications 经开放编码和讨论综合形成。 | 中：统计丰富，覆盖 83 篇 reviews 和 6,117 个非唯一 primary-study 覆盖计数，但表图页码与部分图表结构待 A2a 精核后才能升级为强。 | 强：候选发现来自 general recommendations 与 implications，包括更多实证/工业验证、开放数据、数据管线文档化、online/incremental ML、混合与跨域 ML。 | 中：原文有双人选择、Kappa≥0.8、双人数据抽取 with checker、QA 分歧记录与 threats 分类；本地三路审计只属于仓库审计机制，不作为原文 S8 证据。 |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md#survey_of_surveys-自身-schema-抽取) | 强：三套分类 schema 经既有分类引入、content analysis、语义合并、无关项删除、recommendation 补充和 SWEBOK 映射形成，且有 reliability 检查。 | 强：本文提供年度趋势、venue、频次、交叉表、数据集/工具表、five-number summary、range/median 和 qualitative synthesis。 | 强：§4.1--§4.10 将统计观察转化为候选发现，包括 SE use case 模糊、reference model 缺失、评价数据集偏小、复现资产不足与 practice impact 不清。 | 强：原文报告筛选样本 Cohen’s Kappa、抽取 inter/intra-rater agreement、分类 schema reliability、second coder cross-check、protocol panel review 和 threats mitigation。 |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文通过比较既有 guidelines 与实际 SMS 做法形成 guideline update，并强化 venue、study focus、research method 等 topic-independent facets。 | 强：对 guideline adoption、search、QA、classification、visualization、validity 和 rubric scores 有分母明确统计；A2a 前不作最终统计结论。 | 强：候选 finding 主要是方法学发现：单一 guideline 不足、需更新指南、topic-independent facets 可复用、SMS 应追求 good sample、rubric 可评价报告质量。 | 中：本文没有完整裁决日志，但讨论单人筛选/抽取偏差，并给出 first-author 复审、reference-set validation、additional reviewer + consensus、decision rules 等缓解机制。 |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文体现从 RQ 到分类表再到 finding 的模式演化：RQ1→分布字段，RQ2→benefit 枚举，RQ3→problem+solution 关系，并把空 solution set 作为缺口信号。 | 中：原文给出会议 15/28、未说明 agile context 20/28、含实证成分约 17/28、method proposal 8/28、无 solution problem 3/6 等小样本统计；表格待 A2a PDF 核验。 | 强：候选 finding 包括 agile RE 定义模糊、缺少主导 venue、user story 在大型复杂系统中不足、P3/P4/P6 缺少解决方案、方法提议缺少实证评估。 | 弱：原文有 V.D Limitations，覆盖 Scopus 单库与关键词范围限制；未呈现多研究者筛选/编码冲突裁决、一致性或 QA 协议。 |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md#survey_of_surveys-自身-schema-抽取) | 中：维度形成来自 search-term pilot、既有 tertiary/RE SLR 关键词扩展、标题摘要主题分析、第一作者分组与两位作者复核命名；不是 QA 年度趋势。 | 强：提供 publication type、SLR subtype、scope、#PS 极差与区间、QA 总分、年度发表量、Top-10 citation 等统计。 | 强：候选发现包括 QA 趋势下降、高引不等于高 QA、#PS 内部矛盾、RE 子主题覆盖缺口、半数 SLR 忽略 QA3/QA4。 | 中：原文有主题命名复核、limitations 与 QA guideline 依赖说明，但无完整多研究者筛选/编码裁决、分歧处理、kappa 或 QA 独立复核报告。 |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文显式建模 沿用 FE protocol、复用并调整 QA rubric、修改 QA2、采用既有 review-type 分类和 DCP 分歧裁决，但未给出完整 codebook 演化或冲突修订日志。 | 强：统计覆盖主题、质量趋势、指南引用与质量回归、实践者指南比例、原始研究 QA 比例和 primary 数量相关性；当前只作 A2a 主统计池候选，精核前不写最终定量结论。 | 中：候选发现包括 SLR 数量增长但质量评价仍不足、EBSE 实践缺口、MS 比例变化、欧洲集中性和覆盖空白，多项仍需跨论文复核。 | 强：本文有 DCP 多人编码裁决机制，并在限制讨论中记录 QA2 歧义、QA4 主观性和 protocol 描述不足等边界。 |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md#survey_of_surveys-自身-schema-抽取) | 中：原文没有显式 schema/codebook 演化；可迁移的是 RQ 驱动字段设计、DARE 质量评价与 RQ→抽取字段→统计表的分析模式。 | 强：统计分析覆盖样本数量、类型比例、主题集中度、机构/国家分布、质量得分、Spearman 相关、方差检验与检索漏斗。 | 强：候选发现包括主题覆盖偏窄、Simula 数据库策略可复用、美国 EBSE 参与不足、实践者指南不足和抽取-核对模式风险。 | 强：质量评价采用双人独立评分、分歧讨论至一致，unknown 经邮件询问作者后重评；数据抽取采用单抽取-单核对并讨论分歧。 |
| 2008 | [Systematic Mapping Studies in Software Engineering](./papers/petersen-2008-systematic-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 强：分类方案通过 keywording、聚类和数据抽取过程新增、合并、拆分类别。 | 中：原文有频数、Table 5 和 bubble plot，但这些是内嵌方法示例/小型方法学描述统计；本文保持方法学参考池，不进入普通领域统计合成池。 | 中：可抽取类别频数/交叉覆盖 → 覆盖缺口 → 后续 review 或指南建议的方法学启发，不作为目标领域事实。 | 弱：原文提供 adaptive reading、prototype/misclassification、validity consideration 与 short rationale 机制，但没有实际多 reviewer 裁决日志、agreement、disagreement log 或一致性统计。 |
| 2007 | [Guidelines for performing Systematic Literature Reviews in Software Engineering](./papers/kitchenham-charters-2007-slr-guidelines/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文体现从医学/社会科学 SLR 指南到 SE guideline 的迁移与适配，并通过 Table 9 做跨指南流程 step cross-walk。 | 弱：主体无统计分析；Appendix 2 的 15 篇 SE SLR 只作局部边界观察，方法组件枚举不是 empirical statistic，不能进入主统计池。 | 弱：可记录的 finding 多为方法学启发或二手候选；Appendix 2 的早期 SE SLR 主题/质量分布只能作边界锚点。 | 中：原文提供 inclusion reliability、data extractor/checker、quality assessment、protocol/report evaluation 等方法机制，但不是本文实际执行裁决日志。 |

**本节结论**：S5 与 S6 必须严格区分：字段取值随年份或主题变化属于统计分析，不等于维度模式演化；只有原文说明分类、编码、主题分析、指南更新、作者复核或 schema 修订过程时，才可作为 S5 的强等级支撑。S8 也必须区分一般 limitations 与正式多研究者裁决 / 一致性 / QA；本地 A1-DT 审计只能作为仓库证据链，不能冒充原文 S8 证据。


## 6.2 维度树模式总览

本节是 PR-A1-DT 后新增的跨论文入口；当前 v2 批次为 [A1-DT v2 19×3 原生维度树审计](./audits/a1dt-v2-19x3/README.md)。旧 [A1-DT v1 19×3 全文审计批次](./audits/a1dt-19x3/README.md) 仅为历史返修来源，不是当前事实口径。A1-M0--M6 说明“方法链条”，而维度树说明“单篇综述内部 schema 如何组织”。当前 19 篇均已在单篇 `review.md` 中保留 `维度树复原`，并把正式 A.1--A.4 审计附录集中迁入同目录 `evidence_chain.md`；下表只做总览和跳转，具体正文以 `review.md` 为准，具体证据链以 `evidence_chain.md` 为准。

| 年份 | 论文 | 主类型 | 辅助类型 | 后续主统计池候选 | A1-DT 当前允许用途 | 单篇结论标识 | 详情 |
|---:|---|---|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md) | RQ 驱动分类树 | 生产力 benefit-risk 评价树 | 是 | `schema_seed` | `A1DT-llm-assistants-developer-productivity-C03` | [review](./papers/llm-assistants-developer-productivity/review.md#维度树复原) |
| 2026 | [Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap](./papers/ai-native-se-roadmap/review.md) | roadmap / challenge 树 | 理论 / 元模型概念树 | 否 | `boundary_anchor` | `A1DT-ai-native-se-roadmap-C03` | [review](./papers/ai-native-se-roadmap/review.md#维度树复原) |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md) | 证据资产审计树 | artifact availability 统计树 | 是 | `schema_seed` | `A1DT-research-artifacts-secondary-studies-C03` | [review](./papers/research-artifacts-secondary-studies/review.md#维度树复原) |
| 2025 | [On the road to interactive LLM-based systematic mapping studies](./papers/interactive-llm-systematic-mapping/review.md) | 方法流程树 | human-in-the-loop boundary 树 | 否 | `boundary_anchor` | `A1DT-interactive-llm-systematic-mapping-C03` | [review](./papers/interactive-llm-systematic-mapping/review.md#维度树复原) |
| 2025 | [Formal requirements engineering and large language models: A two-way roadmap](./papers/formal-re-llm-roadmap/review.md) | roadmap / concern / action-point 树 | trustworthiness 边界树 | 否 | `boundary_anchor` | `A1DT-formal-re-llm-roadmap-C03` | [review](./papers/formal-re-llm-roadmap/review.md#维度树复原) |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md) | 系统映射 分类树 | assistant strategy-goal-metric-user 树 | 是 | `schema_seed` | `A1DT-mdse-modelling-assistants-mapping-C03` | [review](./papers/mdse-modelling-assistants-mapping/review.md#维度树复原) |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md) | MDE4ML 生命周期分类树 | 解决方案 / 动机 / 评价树 | 是 | `schema_seed` | `A1DT-mde-ml-components-slr-C03` | [review](./papers/mde-ml-components-slr/review.md#维度树复原) |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md) | 大规模 RQ 驱动分类树 | LLM4SE task-method-evidence 树 | 是 | `schema_seed` | `A1DT-llm4se-systematic-review-C03` | [review](./papers/llm4se-systematic-review/review.md#维度树复原) |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md) | 关系型维度树 | 多声部证据树 | 是 | `schema_seed` | `A1DT-devsecops-primary-dimensions-C03` | [review](./papers/devsecops-primary-dimensions/review.md#维度树复原) |
| 2023 | [Requirements quality research: a harmonized theory, evaluation, and roadmap](./papers/requirements-quality-theory-roadmap/review.md) | 理论 / 元模型概念树 | requirements quality roadmap 树 | 否 | `boundary_anchor` | `A1DT-requirements-quality-theory-roadmap-C03` | [review](./papers/requirements-quality-theory-roadmap/review.md#维度树复原) |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md) | tertiary 主题 / 挑战树 | action recommendation 树 | 是 | `schema_seed` | `A1DT-ml4se-tertiary-study-C03` | [review](./papers/ml4se-tertiary-study/review.md#维度树复原) |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md) | RQ 驱动分类树 | 评价 / 复现资产审计树 | 是 | `schema_seed` | `A1DT-app-reviews-slr-se-C03` | [review](./papers/app-reviews-slr-se/review.md#维度树复原) |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md) | SMS problem-benefit-solution 树 | Agile RE 主题分类树 | 是 | `schema_seed` | `A1DT-re-agile-sms-2015-C03` | [review](./papers/re-agile-sms-2015/review.md#维度树复原) |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md) | mapping guideline update 方法树 | topic-independent dimensions 树 | 是 | `schema_seed` | `A1DT-petersen-2015-mapping-guidelines-update-C03` | [review](./papers/petersen-2015-mapping-guidelines-update/review.md#维度树复原) |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md) | RE tertiary 主题统计树 | 质量 / impact 树 | 是 | `schema_seed` | `A1DT-re-tertiary-study-2014-C03` | [review](./papers/re-tertiary-study-2014/review.md#维度树复原) |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md) | tertiary 更新统计树 | 质量 / EBSE 实践缺口树 | 是 | `schema_seed` | `A1DT-da-silva-2011-six-years-slr-C03` | [review](./papers/da-silva-2011-six-years-slr/review.md#维度树复原) |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md) | tertiary 生态统计树 | 质量评价树 | 是 | `schema_seed` | `A1DT-kitchenham-2009-slr-tertiary-C03` | [review](./papers/kitchenham-2009-slr-tertiary/review.md#维度树复原) |
| 2008 | [Systematic Mapping Studies in Software Engineering](./papers/petersen-2008-systematic-mapping/review.md) | 方法流程树 | topic-independent taxonomy 示例树 | 否 | `schema_seed` | `A1DT-petersen-2008-systematic-mapping-C03` | [review](./papers/petersen-2008-systematic-mapping/review.md#维度树复原) |
| 2007 | [Guidelines for performing Systematic Literature Reviews in Software Engineering](./papers/kitchenham-charters-2007-slr-guidelines/review.md) | 方法流程树 | 质量 / 效度 guideline 树 | 否 | `schema_seed` | `A1DT-kitchenham-charters-2007-slr-guidelines-C03` | [review](./papers/kitchenham-charters-2007-slr-guidelines/review.md#维度树复原) |

**本节结论**：当前 19 篇不是一个同质字段表，而是至少覆盖六类可迁移树型：RQ 驱动分类树、方法流程树、关系型维度树、证据资产审计树、理论 / 元模型概念树、roadmap / challenge 树。对 Paper2 来说，这说明“维度模式”必须允许研究者从树和关系边中选择、批准和演化，而不能预设为单层表格。

## 6.3 维度树类型与 Paper2 L0--L7 的关系

| 维度树类型 | 支撑的 Paper2 阶段 | 当前样本 | 方法启发 |
|---|---|---|---|
| RQ 驱动分类树 | L0 主题与综述元模型设定；L4 字段级证据抽取；L5 统计分析 | app reviews、LLM4SE、LLM assistants | 先由 RQ 确定对象 / 方法 / 评价 / 结果层，再要求每个叶子绑定证据与分母。 |
| 方法流程树 | L1 脚手架挖掘；L2 维度模式批准；L3 论文收集与概览 | Kitchenham guideline、Petersen mapping guideline、interactive LLM mapping | 用流程阶段和 researcher gate 定义 agent-human 协同，而不是把 SLR 写成一次性自动化。 |
| 关系型维度树 | L4 字段抽取；L5 交叉统计；L6 候选发现形成 | DevSecOps、MDSE assistants、research artifacts | 主干树之外必须保留边表；缺失关系本身可成为 gap 候选。 |
| 证据资产审计树 | L4 证据链；L7 透明投影 | research artifacts、app reviews、DevSecOps | artifact、replication package、open science material 应是一等字段。 |
| 理论 / 元模型概念树 | L0 元模型设定；L6 候选发现启发 | requirements quality、AI-native SE | 可启发概念节点，但需降级为 模式种子 / 边界锚点。 |
| roadmap / challenge 树 | L6 候选发现；L7 研究者裁决 | formal RE + LLM、AI-native SE、interactive mapping | action point 只能是候选启发，不能污染主统计池或 最终发现。 |

**本节结论**：Paper2 后续实验不应只测“AI 能否抽字段”，而应测研究者如何定义 / 修改维度树、AI 如何给出证据链、统计观察如何被降级为候选发现并交给研究者裁决。

## 6.4 SUMMARY 结论-证据映射

| 归纳标识 | 引用键 | 归纳内容 | 归纳类型 | 分母 | 纳入结论标识列表 | 排除结论标识列表 | 证据强度过滤 | 外推限制 | 允许用于论文的位置 | 当前状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| [sum-A1DT-tree-types] | [sum-A1DT-tree-types] | 当前 19 篇已形成六类维度树类型，总体说明 survey-of-surveys 需要树型 schema 而不是单层字段表。 | tree_type_inventory | 19 篇 `review.md` | A1DT-llm-assistants-developer-productivity-C03, A1DT-ai-native-se-roadmap-C03, A1DT-research-artifacts-secondary-studies-C03, A1DT-interactive-llm-systematic-mapping-C03, A1DT-formal-re-llm-roadmap-C03, A1DT-mdse-modelling-assistants-mapping-C03, A1DT-mde-ml-components-slr-C03, A1DT-llm4se-systematic-review-C03, A1DT-devsecops-primary-dimensions-C03, A1DT-requirements-quality-theory-roadmap-C03, A1DT-ml4se-tertiary-study-C03, A1DT-app-reviews-slr-se-C03, A1DT-re-agile-sms-2015-C03, A1DT-petersen-2015-mapping-guidelines-update-C03, A1DT-re-tertiary-study-2014-C03, A1DT-da-silva-2011-six-years-slr-C03, A1DT-kitchenham-2009-slr-tertiary-C03, A1DT-petersen-2008-systematic-mapping-C03, A1DT-kitchenham-charters-2007-slr-guidelines-C03 | -- | 本行是树型索引，不作定量统计；允许纳入 `weak` 的 boundary / roadmap C03，但它们只可用于 `schema_seed` / `boundary_anchor`，不得进入主统计池或 最终发现。 | 这是 A1 样本的结构归纳，不代表 100+ 完整文库已饱和；弱证据只用于边界或启发。 | schema_seed | active |
| [sum-A1DT-statistical-pool] | [sum-A1DT-statistical-pool] | 13 篇完成型 SLR / SMS / tertiary / MLR / 系统映射 是后续主统计池候选，但 PR-A1-DT 当前维度树证据仍待 A2a 精确锚定，暂不进入 SUMMARY 定量统计。 | pool_candidate_index | 19 篇 `review.md` | A1DT-llm-assistants-developer-productivity-C04, A1DT-research-artifacts-secondary-studies-C04, A1DT-mdse-modelling-assistants-mapping-C04, A1DT-mde-ml-components-slr-C04, A1DT-llm4se-systematic-review-C04, A1DT-devsecops-primary-dimensions-C04, A1DT-ml4se-tertiary-study-C04, A1DT-app-reviews-slr-se-C04, A1DT-re-agile-sms-2015-C04, A1DT-petersen-2015-mapping-guidelines-update-C04, A1DT-re-tertiary-study-2014-C04, A1DT-da-silva-2011-six-years-slr-C04, A1DT-kitchenham-2009-slr-tertiary-C04 | A1DT-ai-native-se-roadmap-C04, A1DT-interactive-llm-systematic-mapping-C04, A1DT-formal-re-llm-roadmap-C04, A1DT-requirements-quality-theory-roadmap-C04, A1DT-petersen-2008-systematic-mapping-C04, A1DT-kitchenham-charters-2007-slr-guidelines-C04 | 本行是候选资格索引，不作定量统计；当前单篇 C04 只记录后续统计池候选或降级裁决；A1-DT v2 当前仍按 `schema_seed` / `boundary_anchor` 管理，待 A2a 完成精确页码 / 表图 / 字段锚定后才可升级。 | 统计池候选资格只服务后续 A2a/A2b，不支撑目标领域 最终发现；弱或待核验证据不得进入定量统计。 | schema_seed | active |
| [sum-A1DT-boundary-anchor] | [sum-A1DT-boundary-anchor] | roadmap / vision / proposal / guideline 的维度树可提供边界锚点和候选启发，但不得进入主统计池。 | downgrade_decision | 19 篇 `review.md` | A1DT-ai-native-se-roadmap-C04, A1DT-interactive-llm-systematic-mapping-C04, A1DT-formal-re-llm-roadmap-C04, A1DT-requirements-quality-theory-roadmap-C04, A1DT-petersen-2008-systematic-mapping-C04, A1DT-kitchenham-charters-2007-slr-guidelines-C04 | A1DT-llm-assistants-developer-productivity-C04, A1DT-research-artifacts-secondary-studies-C04, A1DT-mdse-modelling-assistants-mapping-C04, A1DT-mde-ml-components-slr-C04, A1DT-llm4se-systematic-review-C04, A1DT-devsecops-primary-dimensions-C04, A1DT-ml4se-tertiary-study-C04, A1DT-app-reviews-slr-se-C04, A1DT-re-agile-sms-2015-C04, A1DT-petersen-2015-mapping-guidelines-update-C04, A1DT-re-tertiary-study-2014-C04, A1DT-da-silva-2011-six-years-slr-C04, A1DT-kitchenham-2009-slr-tertiary-C04 | 本行专门记录降级后的 boundary 结论；允许 `weak`，但只用于边界锚点 / 风险提示 / 候选启发，不进入主统计池、SUMMARY 定量统计或 最终发现。 | 这些结论仅用于方法设计和风险提示，不能写成经验事实。 | boundary_anchor | active |

**本节结论**：SUMMARY 的跨论文归纳已经显式回链单篇 A.3 结论标识。后续若新增论文或修改树型，必须同步更新本表，否则 SUMMARY 归纳将失去证据链闭环。

**A1-DT v2 证据链边界**：当前正式 A.2 / A.3 是树级与核心裁决的最小 claim map，集中保存在各单篇 `evidence_chain.md`；单篇叶子取值空间、关系边、缺失值语义和图表待核验项仍以各 `review.md` 的“维度树复原”正文、叶子维度表和关系边表为细粒度说明。若两处发生冲突，以 `evidence_chain.md` 的 A.2 / A.3 与主线程裁决为准，并在 A2a 把 leaf / edge 逐项迁入统一审计附录；因此 SUMMARY 不把 A1-DT v2 写成叶子级最终统计证据。

## 7. 当前 pattern 总结与 A2a 接力建议

| pattern | 当前观察 | 来源样本 | A2a 处理建议 |
|---|---|---|---|
| RQ pattern | SE tertiary 常问规模、主题、主体、质量、限制、EBSE 实践缺口；现代 LLM4SE SLR 常先给 landscape / method / benefit-risk / dimension coverage。 | Kitchenham 2009、da Silva 2011、LLM assistant SLR、LLM4SE SLR | 建立 RQ 模式树，区分 landscape、method、impact、dimension coverage、gap/finding。 |
| dimension pattern | 维度应树状化而非平铺：strategy-goal-limitation-metric-user、aspect-theme-category、concept-activity-context-impact 等。 | MDSE assistant mapping、DevSecOps MLR、requirements quality roadmap | 把字段树版本化，并记录字段来源、缺失语义和 researcher adoption decision。 |
| finding pattern | finding 需从统计观察进一步形成质量缺口、EBSE 实践缺口、research challenges、roadmap、action recommendations；roadmap 只能提供启发式。 | da Silva 2011、ML4SE tertiary、DevSecOps MLR、requirements quality roadmap | 与 Paper2 的 候选发现 ledger 对齐，补 support / counter-evidence / claim strength。 |
| evidence presentation pattern | 常用搜索分母、纳排、quality assessment、topic taxonomy、review/primary-study 数量、artifact availability、replication package。 | Kitchenham guideline、research artifacts mapping、LLM4SE SLR | 每个字段必须有 source anchor、artifact link status 和回填状态。 |
| validity / threat pattern | 包含 search bias、inclusion reliability、quality assessment、protocol deviation、artifact dead link、model drift、human validation。 | Kitchenham guideline、interactive LLM mapping、research artifacts mapping | 设为强制字段，未报告时明确记录。 |
| report structure pattern | guideline、tertiary/SMS、SLR+SMS、MLR、roadmap 的结构不同；不能用一个模板压平。 | 全文样本 | 允许不同 `review_type` 对应不同报告结构和统计池资格。 |

A2a 第一优先级：不是补历史 PDF，而是对当前 19 篇做图表视觉核对、页码 / 表号证据锚定，并将 A1-M0--M6 与 S1--S8 两套矩阵共同转为更正式的 pattern library；随后扩展到 30--50 篇核心样本，检验字段取值空间、统计池规则、finding heuristic 与研究者裁决记录是否稳定。

### 7.1 schema 修订 / 回填日志

本节是 A1 字段合同演化的结构化审计入口。它只记录会影响后续 A2a/A2b schema、统计池或字段回填的变更；普通下载、排版或 PR 施工细节仍进入更新日志或 `search/` 审计文件。

| 时间 | 触发条目 / 样本 | 受影响字段 | 修订内容 | 回填状态 | 冻结理由 / 后续处理 |
|---|---|---|---|---|---|
| 2026-07-02 22:04:02 | 用户要求每篇 survey 的 S1--S8 维度信息由独立 subagent 抽取；19 篇全文样本 | S1--S8 二级汇总 schema、单篇 `review.md`、SUMMARY 覆盖矩阵、A2a handoff | 新增 `survey_of_surveys 自身 schema` 定义表、S1--S8 逐篇矩阵和单篇四分栏证据拆分；19/19 篇已回填 `review.md` 的 `survey_of_surveys 自身 schema 抽取` 小节；要求后续新增论文一篇一 subagent 抽取并显式拆清原文证据 / 维度树 / 统计池资格 / A2a 待核验 | 已回填 19/19 篇 review、GUIDE、SUMMARY、audit TASKS/results/adjudications；A2a 接力项写入审计裁决与风险表 | S1--S8 用于把综述之综述自身转成可审计模式库，支撑 researcher-defined meta-model、证据链、统计分析与 finding 裁决设计；不得写成目标领域 final finding。 |
| 2026-06-29 21:10:00 | PR-A1-DT 逐篇维度树复原；19 篇全文样本 | 维度树、叶子取值空间、关系边、结论-证据映射、SUMMARY 归纳回链 | 新增 GUIDE 维度树纪律、schema 字段合同、19 篇 `review.md` 的 `维度树复原` 与 19 篇 `evidence_chain.md` 的 A.1--A.4 审计附录；SUMMARY 新增维度树模式总览和 `[sum-A1DT-*]` 结论-证据映射 | 已回填 19/19 篇 review、GUIDE、pattern schema 与 SUMMARY | Paper2 方法贡献需要可审计维度树，而不是平铺字段矩阵；A2a 继续做页码 / 图表精核与样本扩展。 |
| 2026-06-29 17:48:49 | 用户复核 SUMMARY 批次化问题；19 篇全文样本 | SUMMARY 主表、证据池、A1-M0--M6 总账矩阵 | 取消按 PR 批次拆分主表，改为统一年份降序表；明确三类证据池主归属；新增 19 篇 × A1-M0--M6 覆盖矩阵 | 已回填 SUMMARY、GUIDE 与审计目录 | 长期文库必须按对象和当前事实维护，不能按施工批次维护；A2a/A2b 继续沿用统一总账结构。 |
| 2026-06-29 17:58:30 | 三路复审 C/I：CCF 复核状态、三池计数、schema 回修入口 | `ccf_verification_status`、三类证据池计数、schema change ledger | 主表新增 `CCF 复核状态` 列；三类证据池改为主归属计数；恢复本结构化 schema 修订 / 回填日志 | 已回填 SUMMARY、GUIDE、pattern schema 与审计目录 | 防止复制主表时丢失 CCF disclaimer；防止方法学样本与边界 seed 重复计数；保留字段回修可审计入口。 |
| 2026-06-29 16:59:12 | 用户补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 PDF | 阅读状态、`eligible_for_statistical_synthesis`、manual-download 状态 | 历史 metadata-only / manual-download 条目升级为全文文本级；active manual-download 清零；Petersen 2008 保持方法学参考池，Petersen 2015 作为方法学统计样本进入主统计池 | 已回填 3 篇 `paper.pdf`、`paper_content.txt`、`review.md`、`metadata.json`、SUMMARY 与 search log | 补齐全文后才能把题摘级候选升级为全文级 pattern；统计池仍按主归属和系统性证据状态控制。 |
| 2026-06-29 15:41:07 | issue #95 十篇现代锚点 | `review_type`、`eligible_for_schema_seed`、`eligible_for_statistical_synthesis`、`evidence_role`、A1-M0--M6 | 扩展 SLR+SMS、系统映射、MLR、solution proposal、vision/roadmap、theory/evaluation/roadmap；新增 模式种子 与统计池分离字段；新增 A1-M0--M6 元维度 | 已回填 19 篇 `metadata.json`、单篇 `review.md`、SUMMARY、candidate-pool、GUIDE 和 schema | 现代 roadmap / proposal 有高启发价值但不得污染主统计池；A1-M0--M6 是 A2a/A2b 的元维度接力骨架。 |
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
5. 对 roadmap / vision / proposal 保持 boundary / 模式种子 池，不混入主统计池。

A2b 建议：

1. 扩展到预计 100+ 篇完整文库闭合。
2. 形成第一个可引用快照。
3. 明确纳排分母、排除理由、人工下载清单、覆盖 / 饱和度判断。
4. 把完整文库快照交给 A3 消费，A3 不再混入大规模补文库。

## 10. 更新日志

| 时间 | 更新内容 | 验证 / 备注 |
|---|---|---|
| 2026-06-29 21:10:00 | 完成 PR-A1-DT 实现：补充 GUIDE 维度树复原规则、pattern schema 字段合同、19 篇单篇 `review.md` 的维度树复原与 19 篇 `evidence_chain.md` 的 A.1--A.4 审计附录，并在 SUMMARY 增加维度树模式总览和 SUMMARY 结论-证据映射。 | A1 原始阶段未读取 `.env`；A1-DT v2 批次已完成 57/57 CLI 审计，日志保留命令/stdout/stderr与环境摘要，关于 `.env` 只记录 `env_sourced=.env exists`，不记录 secret；A1-DT 仍保留 A2a 页码 / 表图精核边界。 |
| 2026-06-29 17:40:27 | 根据用户对 SUMMARY 缝合感和批次拆表问题的反馈，重构 SUMMARY 为长期文库总账：取消批次化主表，改为统一年份降序论文表；补充三类证据池标准；新增 19 篇 × A1-M0--M6 覆盖矩阵；把历史过程下沉为风险 / 日志。 | 本轮只重构总账和规则，不新增论文；后续需同步 GUIDE 与 PR body，并复验 19/19/19/19、active manual=0。 |
| 2026-06-29 16:59:12 | 用户提供 3 篇历史 manual-download PDF 后，补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 的 `paper.pdf`、`paper_content.txt`、全文级 `review.md` 和 `metadata.json`，并将 active 人工下载清单清零。 | 文件系统统计更新为 19 个 `review.md`、19 个 `metadata.json`、19 个 `paper.pdf`、19 个 `paper_content.txt`；3 篇历史失败路径已闭环，剩余风险转为 A2a 图表视觉核对和 CCF 官方人工复核。 |
| 2026-06-29 16:13:28 | 修复三路 reviewer 复审提出的 C/I：补齐早期 9 篇 `metadata.json`，统一 19 篇机器可读字段，修正 CSUR CCF 待核验口径，并清理 `paper_content.txt` 行尾空白。 | `git diff --check` 两点工作区口径通过；提交后需再用 PR 三点 diff 复验。 |
| 2026-06-29 15:41:07 | 根据内部复核修复 A1-M0--M6 命名、SUMMARY 19/16/3 历史总账、#95 metadata 全文状态、roadmap / proposal 统计池排除字段，并记录 CCF 官方页面 WAF 风险。 | 当时文件系统统计：19 个 `review.md`、19 个 `metadata.json`、16 个 `paper.pdf`、16 个 `paper_content.txt`、3 个 manual-download BibTeX 条目；后续 16:59 已补齐为 19/19/19/19。 |
| 2026-06-29 15:37:22 | 完成 #95 十篇现代锚点一致性复验：补 `issue95-selection-audit.md`，统一 `interactive-llm-systematic-mapping` 年份为正式卷期 2025，修复 19/16/3 历史总账，保持 CCF 字段为“本地缓存；官方待人工复核（WAF）”。 | 当时 `git diff --check` 与 A1 consistency 脚本通过；manual-download-needed 仍为 3 条旧失败路径，后续 16:59 已清零。 |
| 2026-06-29 13:20:00 | 按用户新增要求补充 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 四列，并同步单篇 review 快速卡片、候选池和字段 schema。 | CCF 字段按官方完整目录口径设计；本轮 HTTP/CLI 访问官方页受 WAF 限制，工作表暂用本地缓存并标注正式写作前需人工复核。 |
| 2026-06-29 02:18:07 | 建立 `survey_of_surveys/` README/GUIDE/SUMMARY/search/papers/patterns；完成 6 篇全文文本级 dry-run 和 3 篇 metadata-only 失败路径；回修 schema 字段。 | A1 奠基；未运行真实 LLM，未读取 `.env`，不跑四个真实例子。 |
