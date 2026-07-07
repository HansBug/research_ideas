# survey_of_surveys/SUMMARY.md：综述之综述文库总账

## 0.A A2a 语料主候选建设速读

**当前结论**：A2a 已把前序近年软件工程综述候选摸排整理成集中 `corpus/` 入口。这个阶段解决的是“后续 A2b 要读哪些、哪些已取得 PDF、哪些需要人工下载、候选分母怎么复算”的问题，不解决最终维度树、最终 research finding 或 100+ 全文深读闭合。

| 项 | 数量 | 入口 | 当前判断 |
|---|---:|---|---|
| 全量候选账本 | 438 | [corpus/tables/full-candidate-ledger.csv](./corpus/tables/full-candidate-ledger.csv) | 保留候选分母，防止 cherry-pick。 |
| 系统化候选池 | 293 | [corpus/tables/systematic-candidates.csv](./corpus/tables/systematic-candidates.csv) | 当前脚本识别的 SLR / SMS / MLR / tertiary 候选；最终以 A2b 全文核验为准。 |
| 主候选语料 | 120 | [corpus/tables/core-corpus.csv](./corpus/tables/core-corpus.csv) | A2b 优先深读对象；包含 A1 已有 13 篇入池候选。 |
| 替补 / 留出语料 | 40 | [corpus/tables/reserve-corpus.csv](./corpus/tables/reserve-corpus.csv) | 用于替换主候选中后续被排除或全文无法取得的条目。 |
| 边界 / 方法启发池 | 145 | [corpus/tables/boundary-pool.csv](./corpus/tables/boundary-pool.csv) | 不进入主统计池，只作方法启发或边界说明。 |
| 已取得 PDF / 文本 | 69 | [corpus/tables/pdf-status.csv](./corpus/tables/pdf-status.csv) | core 63 + reserve 6；只表示可进入 A2b 全文深读，不表示已完成 `review.md`。 |
| 需人工下载 | 91 | [corpus/manual-download-needed.md](./corpus/manual-download-needed.md) / [corpus/manual-download-needed.bib](./corpus/manual-download-needed.bib) | core 57 + reserve 34；PDF 不可得不等于排除。 |

PDF 状态速读：core + reserve 共 69 篇已有本地 `paper.pdf` / `paper_content.txt`，其中 13 篇来自 A1，2 篇由 A2a 自动从开放 PDF 链接获取，54 篇来自用户本地 Zotero 导出后显式复制入仓库；仍有 core 57 篇与 reserve 34 篇需要人工下载或后续合法开放来源补抓。本轮 Zotero 导出中有 2 篇附件存在但 PDF 结构损坏、内容错配或文本提取失败，已继续留在人工清单。`raw/` 为前序摸排快照，本 PR 只做换行符与行尾空白规范化，字段、行数与候选资格均未变；主候选优先级种子已显式固化为 [corpus/raw/selection-seed.csv](./corpus/raw/selection-seed.csv)。前序 `/tmp` 本地临时路径只保留为审计线索，不能触发 `downloaded` 状态或自动复制；只有仓库内真实存在的 `papers/<slug>/paper.pdf` 才计为已下载。详见 [corpus/pdf-acquisition.md](./corpus/pdf-acquisition.md) 与 [corpus/source-audit.md](./corpus/source-audit.md)。

A2b 启动前必须先读 [corpus/handoff-to-next-stage.md](./corpus/handoff-to-next-stage.md)。


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

## 1.3 后续主统计池候选主表（枚举速读版，按年份降序）

字段口径：本表是文库最靠前的论文级 story 速读表，只收 `统计池资格 = 🟢 入池` 的条目，优先回答“哪些论文可以作为后续 A2a/A2b 主统计池候选、它们是什么综述类型、原文样本单位是什么、原生维度树是什么”。`🟡 待核`、`⚪ 不入`、`🔴 排除` 不在本主干完整表中展开，统一下沉到后部非入池简表、候选池或失败记录。`CCF 复核状态` 不在本表展开，详见 §2.3 与单篇 `review.md` 快速卡片。

| 状态 | 年份 | 标题 | 出版形态 | 期刊/会议/预印本 | CCF 大类 | CCF 等级 | 综述类型大类 | 细分类型 / 原文自称 | 本文角色 | 统计池资格 | 证据成熟度 | 样本单位 / 分母链 | 原生维度树类型 | Paper2 关键贡献 | 详情 |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 🟢 | 2026 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 🟩 SLR+SMS | SLR + SMS；39 篇 peer-reviewed 原始研究，2014--2024 | 🟢 主样本 | 🟢 入池 | 🟡 全文 | 📄 原研 / 39 | 🌲 森林 | 现代 CCF-A LLM4SE SLR+SMS；展示 landscape→method→benefit/risk→SPACE 映射。 | [review.md](./papers/llm-assistants-developer-productivity/review.md) |
| 🟢 | 2025 | Research artifacts in secondary studies: A systematic mapping in software engineering | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟦 SMS | 系统映射；对象是 SE 二次研究 artifact | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📚 综述 / 537 | 🧱 资产树 | 把 artifact availability、永久仓库、DOI、dead link 等转为证据资产字段。 | [review.md](./papers/research-artifacts-secondary-studies/review.md) |
| 🟢 | 2024 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟦 SMS | 系统映射；MDSE assistant proposals + 工具文档 | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📄 原研 / 58 + 工具 17 | 🕸️ 关系树 | 贴近 LLM4modeling；提供 strategy-goal-limitation-metric-user 维度关系。 | [review.md](./papers/mdse-modelling-assistants-mapping/review.md) |
| 🟢 | 2024 | Model driven engineering for machine learning components: A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟩 SLR | Kitchenham-style SLR；MDE4ML 原始研究 | 🟢 主样本 | 🟢 入池 | 🟡 全文 | 📄 原研 / 46 | 🌲 森林 | 提供 motivation / solution / evaluation / limitation 与 RQ Answer Summary 模式。 | [review.md](./papers/mde-ml-components-slr/review.md) |
| 🟢 | 2024 | Large Language Models for Software Engineering: A Systematic Literature Review | 期刊 | [TOSEM](https://dl.acm.org/journal/tosem) | 软件工程 / 系统软件 / 程序设计语言 | A | 🟩 SLR | LLM4SE SLR；395 篇研究论文 | 🟢 主样本 | 🟢 入池 | 🟡 全文 | 📄 原研 / 395 | 🌲 森林 | 大规模 LLM4SE 字段树；提供模型、数据、任务、制品、限制和趋势字段。 | [review.md](./papers/llm4se-systematic-review/review.md) |
| 🟢 | 2024 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 期刊 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟨 MLR | 多声部综述；白色/灰色文献双轨 | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📄 原研 / 147 | 🕸️ 关系树 | 提供 thematic analysis、CPTM 关系模型、WL/GL 分层和开放材料模式。 | [review.md](./papers/devsecops-primary-dimensions/review.md) |
| 🟢 | 2023 | Machine Learning for Software Engineering: A Tertiary Study | 期刊 | [CSUR](https://dl.acm.org/journal/csur) | 待核验 | 待核验 | 🟪 三级 | tertiary study；83 篇 reviews，间接覆盖 6,117 个原始研究计数 | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📚 综述 / 83 | 🌲 森林 | 现代大规模 tertiary；提供挑战、行动建议和质量观察模式。 | [review.md](./papers/ml4se-tertiary-study/review.md) |
| 🟢 | 2022 | Analysing app reviews for software engineering: a systematic literature review | 期刊 | [ESE](https://link.springer.com/journal/10664) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟩 SLR | SLR；app reviews for SE 原始研究 | 🟢 主样本 | 🟢 入池 | 🟡 全文 | 📄 原研 / 182 | 🌳 RQ树 | 完整现代 SLR 样本；提供 F1--F18、分类 schema、评价和复制包字段。 | [review.md](./papers/app-reviews-slr-se/review.md) |
| 🟢 | 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟦 SMS | mapping guideline update / systematic map of maps；52 篇 SMS | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📚 综述 / 52 | 🔁 流程树 | 以系统映射之系统映射更新 guideline；支撑流程、质量、效度和报告结构字段。 | [review.md](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 🟢 | 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | 会议 | [SEAA](https://dsd-seaa.com/) | -- | -- | 🟦 SMS | SMS；Agile RE 原始研究 | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📄 原研 / 28 | 🕸️ 关系树 | 提供 benefit/problem/solution 关系边和小样本 SMS 边界。 | [review.md](./papers/re-agile-sms-2015/review.md) |
| 🟢 | 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | 工作坊 | [EmpiRE](https://empire2014.wordpress.com/) | -- | -- | 🟪 三级 | tertiary study；RE 领域 SLR | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📚 综述 / 53 | 🌲 森林 | 验证特定 SE 子领域如何组织 topic、quality、impact 和 practitioner relevance。 | [review.md](./papers/re-tertiary-study-2014/review.md) |
| 🟢 | 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟪 三级 | updated tertiary study；扩展前序 tertiary | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📚 综述 / 67 新增；整合 120 | 🕸️ 关系树 | 提供更新型 tertiary、前序关系、质量趋势和 EBSE 实践缺口模式。 | [review.md](./papers/da-silva-2011-six-years-slr/review.md) |
| 🟢 | 2009 | Systematic literature reviews in software engineering – A systematic literature review | 期刊 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | 软件工程 / 系统软件 / 程序设计语言 | B | 🟪 三级 | tertiary SLR / SE SLR 状态综述 | 🔵 类SLR | 🟢 入池 | 🟡 全文 | 📚 综述 / 20 | 🌲 森林 | 早期 EBSE 状态综述；提供 RQ、质量、主题和报告结构基线。 | [review.md](./papers/kitchenham-2009-slr-tertiary/review.md) |

**本节结论**：当前真正进入 SUMMARY 主干完整表的是 13 篇 `🟢 入池` 条目，覆盖 SLR、SMS、MLR、tertiary 和 systematic map of maps。它们仍只是 A2a/A2b 的后续主统计池候选；A1 当前不产生最终定量结论。

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

本总账固定维护 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 和 `CCF 复核状态`。其中 `期刊/会议/预印本` 使用可点击短名链接；预印本统一写 `[arXiv](https://arxiv.org/)`。第一张 story 速读表不再放置 `CCF 复核状态`，只保留 `CCF 大类` 与 `CCF 等级` 以支撑来源质量判断；`CCF 复核状态` 仍是事实审计口径的一部分，维护在本节说明、单篇 `review.md` 快速卡片或后续 CCF / venue 专门核验表中，避免把本地缓存误写成官方实时核验。

CCF 字段的目标口径是 **CCF 官方最新推荐目录**，不局限于本仓库 [../../../ccf_venues/](../../../ccf_venues/) 已建档范围。2026-06-29 本轮 HTTP/CLI 访问 CCF 官方 [软件工程 / 系统软件 / 程序设计语言目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 返回 Aliyun WAF 壳，当前表格暂采用本地 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 与 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 的已建档缓存作为工作口径；正式写作或投稿前必须人工打开 CCF 官方目录复核。

**本节结论**：本目录应把“是否可统计”和“是否有启发价值”分开管理。后续 A2a 不能因为 roadmap / proposal 学术价值高就把它们纳入统计池，也不能因为 guideline 不进统计池就忽略其方法学价值。

### 2.4 主表与快速结论卡片枚举口径

本目录的 [SUMMARY.md](./SUMMARY.md) 主干完整表和每篇 `review.md` 的快速结论卡片，使用受控的“emoji + 短文本”枚举表达关键类型维度。这里是本目录对仓库根级“emoji 列默认只写 emoji”规则的显式 override：只有本节规定的枚举列允许写成 `emoji + 短文本`；普通状态列仍保持 emoji-only。

执行纪律：

1. 枚举列不得临时自造标签；若需要新增类型，必须先更新本节、[GUIDE.md §4.2](./GUIDE.md#42-主表与快速结论卡片枚举口径) 和必要的门禁 / 总账。
2. `SUMMARY.md` 的主干完整表、逐篇覆盖矩阵、维度树总览、pattern 汇总和结论-证据映射等主要分析表，只统计 `统计池资格 = 🟢 入池` 的 13 篇。
3. `🟡 待核`、`⚪ 不入`、`🔴 排除` 不得占用主干分析表；只能进入后部风险 / 边界备忘、候选池或失败记录。
4. 一篇论文若有多个角色，主表只写“主角色”；次级用途写在 `review.md` 的详细说明中，避免双重计数。
5. `CCF 复核状态` 不作为第一张主表的核心枚举列；它应保留在 CCF / venue 审计说明、单篇快速卡片或后续专门核验表中。
6. 后续新增论文时，至少要同步填写：`综述类型大类`、`本文角色`、`统计池资格`、`证据成熟度`、`样本单位 / 分母链`、`原生维度树类型`，并在本节更新入池子集数量。

#### 2.4.1 综述类型大类

该维度回答“论文自身是什么类型”。它不等于论文质量，也不单独决定是否入池；最终是否进入 SUMMARY 主干完整表仍由 `统计池资格` 判定。`当前入池子集数量` 只统计 §1.3 的 13 篇，不把非入池 roadmap / guideline / proposal 计入。

| 枚举 | 定义 | 判定标准 | 当前入池子集数量 | 不得误用为 |
|---|---|---|---:|---|
| 🟩 SLR | 系统文献综述，或以 SLR 为主并兼有映射 / 主题综合的混合综述；本库把 `SLR+SMS` 归入该大类并在细分类型中说明。 | 原文明确报告系统检索、纳排、质量评价或数据抽取，并以回答证据综合型 RQ 为目标。 | 4（其中 SLR+SMS 1） | 不能把只写了“review / survey”但无系统流程的叙事综述写成 SLR。 |
| 🟦 SMS | 系统映射研究，重点是研究版图、分类、覆盖度和缺口。 | 原文强调 mapping、classification、keywording、研究类型/主题分布，而非深度效果综合。 | 4 | 不能把方案论文中“计划做 mapping”的方法设想写成已执行 SMS。 |
| 🟪 三级 | 三级研究、综述之综述或 review of reviews。 | 样本单位是 SLR/SMS/survey 等二次研究，而非普通原始研究。 | 4 | 不能把三级研究的统计外推为原始研究层面的频次。 |
| 🟨 MLR | 多声部文献综述，综合白色文献和灰色文献。 | 原文明确 white / grey literature 双轨来源、检索、质量或可信度控制。 | 1 | 不能混淆 peer-reviewed evidence 与 grey evidence 的证据强度。 |
| 🧰 指南 | 方法指南、报告规范、checklist 或方法论文。 | 原文主要给出如何做 SLR/SMS 的流程、表单、质量标准或报告规范。 | 0 | 不能把规范性建议当作经验统计 finding。 |
| 🧭 路线图 | vision、roadmap、agenda、challenge map 或开放问题图谱。 | 原文主要提出愿景、挑战、研究议程或 action items，缺少系统检索分母。 | 0 | 不能把作者观点、路线图行动项写成系统综述证据。 |
| 🧪 方案 | solution proposal、framework proposal 或未完成实证评估的方法设想。 | 原文主要提出流程、工具或框架设计，尚未完成系统检索、纳排和证据综合。 | 0 | 不能把“可以如何做”写成“已经系统验证”。 |

#### 2.4.2 本文角色

该维度回答“这篇论文在 Paper2 中怎么用”。它是本库用途分类，不是原文自称类型。

| 枚举 | 定义 | 判定标准 | 当前入池子集数量 | 需要写清的边界 |
|---|---|---|---:|---|
| 🟢 主样本 | Paper2 SLR 主目标的核心样本。 | 通常为 SLR，且具备系统流程、字段抽取、统计观察和 finding 形成路径。 | 4 | 只贡献方法模式，不把领域结论外推到 Paper2 目标领域。 |
| 🔵 类SLR | SMS、MLR、tertiary 等类 SLR 证据综合样本。 | 非纯 SLR，但有系统语料、编码字段、统计分母或证据综合。 | 9 | 必须注明样本单位和分母差异。 |
| 🟣 方法 | 方法学参考。 | guideline / 方法论文 / 报告规范，主要定义流程、质量评价、报告结构或审计纪律。 | 0 | 可支撑方法设计，不能支撑普通领域统计。 |
| 🟠 种子 | 维度树、字段、证据链或 finding heuristic 的启发来源。 | 有可迁移结构，但缺少系统样本库或不能进入普通统计池。 | 0 | 必须说明是启发，不是 final finding。 |
| ⚫ 边界 | 用于说明哪些文献类型不能混入统计池。 | roadmap / vision / proposal 等高价值但非系统证据综合的论文。 | 0 | 必须写清阻断入池的原因。 |
| ⚪ 候选 | 只完成题摘或元数据核验的线索。 | PDF / 全文 / 关键元数据尚未核验，或相关性未裁决。 | 0 | 不得采纳为已核验 pattern。 |

#### 2.4.3 统计池资格

该维度决定论文是否进入 SUMMARY 主干完整表和后续主要分析表。它是主表治理的最高优先级枚举。

| 枚举 | 定义 | 判定标准 | 全库数量 | 当前主干分析表数量 | SUMMARY 处理 |
|---|---|---|---:|---:|---|
| 🟢 入池 | 后续可作为主统计池候选的条目。 | 有系统检索或等价语料构造、纳排、编码 / 抽取、可统计字段或统计结果；本地至少全文文本级。 | 13 | 13 | 唯一允许进入 SUMMARY 主干完整表和主要分析矩阵。 |
| 🟡 待核 | 理论上可能入池，但当前证据不足。 | 题摘或全文显示可能有系统流程，但 PDF、表图、附录、复制包、分母链或字段表未核验。 | 0 | 0 | 不进入主干分析表；进入候选池或待核记录。 |
| ⚪ 不入 | 不进入主统计池，但可能仍有方法或启发价值。 | guideline、roadmap、vision、proposal，或无系统样本库 / 无可统计分母。 | 6 | 0 | 不进入主干分析表；只在风险 / 边界备忘或单篇 `review.md` 中保留。 |
| 🔴 排除 | 当前文库不再采纳。 | 类型误收、事实不可核验、重复条目、与本目录目标无关，或来源不合规。 | 0 | 0 | 不进入主干分析表；只留失败 / 排除记录。 |

#### 2.4.4 证据成熟度

该维度回答“当前证据链能支撑多强的写作”。它不决定是否入池，但限制该条目能在论文中被怎样使用。

| 枚举 | 定义 | 判定标准 | 当前入池子集数量 | 禁止用途 |
|---|---|---|---:|---|
| 🟢 精核 | PDF、关键表图、页码、附录或复制包已核验。 | 已完成文本 + 版面 / 表图 / supplementary 或 artifact 核验，并回链 `evidence_chain.md`。 | 0 | 不能省略分母、页码或证据限制。 |
| 🟡 全文 | 已读全文文本，但表图页码仍待 A2a 精核。 | `paper_content.txt` 覆盖摘要、方法、结果、讨论、结论等关键部分。 | 13 | 不得写成最终定量统计或最终 finding。 |
| 🟠 题摘 | 只读题名、摘要、元数据。 | 尚未获取或阅读全文。 | 0 | 不得采纳任何维度树、统计或 finding。 |
| ⚪ 待取 | PDF 或正文尚未获取。 | 只有 BibTeX、DOI、题录或待下载路径。 | 0 | 不得假装已读全文。 |
| 🔴 异常 | 来源、PDF 或文本提取有问题。 | PDF 是登录页 / HTML、文本乱码、关键元数据冲突或来源不可核验。 | 0 | 不得继续写模式结论。 |

#### 2.4.5 样本单位类型

该维度回答“原文实际描述和编码的对象是什么”。它是判断统计池资格和分母含义的关键。

| 枚举 | 定义 | 判定标准 | 当前入池子集数量 | 统计注意事项 |
|---|---|---|---:|---|
| 📄 原研 | 原始研究、primary studies 或研究论文。 | 每个样本是一篇原始研究 / 研究提案 / 研究论文。 | 7 | 不同研究类型、peer-reviewed / arXiv / grey literature 需分层。 |
| 📚 综述 | 二次研究、SLR/SMS/survey 样本。 | 每个样本是一篇综述或系统映射。 | 6 | 不得把综述样本统计外推为原始研究统计。 |
| 🧩 工件 | artifact、dataset、tool、replication package 或链接对象。 | 样本或核心字段围绕研究制品、数据集、工具、仓库、链接状态。 | 0 | 需区分 paper-level 与 artifact-level 分母。 |
| 🧰 指南项 | guideline item、checklist item、流程步骤。 | 原文是方法指南或规范，编码对象是条目而非经验样本。 | 0 | 默认不进入普通统计池。 |
| 🧭 行动项 | roadmap action、open question、challenge item。 | 原文组织为挑战、开放问题、行动项或愿景组件。 | 0 | 只能作启发或边界，不能当 empirical denominator。 |
| ❌ 无分母 | 无系统样本库或无法形成可统计分母。 | 原文没有检索、纳排、样本单位或可统计对象。 | 0 | 自动阻断主干完整表资格，除非后续发现独立系统样本部分。 |

#### 2.4.6 原生维度树类型

该维度回答“原文如何描述自己的样本集合或证据对象”。它是本库对 Paper2 最重要的 schema 资产。

| 枚举 | 定义 | 判定标准 | 当前入池子集数量 | 容易误判点 |
|---|---|---|---:|---|
| 🌳 RQ树 | 以 RQ / 子 RQ 为主干组织字段。 | 每个 RQ 对应一组抽取字段、结果表或 finding 段。 | 1 | 多个 RQ 若对应不同样本单位，应改写为森林。 |
| 🌲 森林 | 多个 RQ、多个样本单位或多个不共享根对象的编码结构。 | 原文同时有多个字段树、质量表、检索漏斗、评价树等。 | 6 | 不要为追求简洁强行压成单树。 |
| 🕸️ 关系树 | 重点是对象间关系。 | 字段包括 tool-task-metric、problem-solution、challenge-practice 等边。 | 4 | 不能把关系边压成普通枚举列。 |
| 🧱 资产树 | 以制品、数据集、复制包、链接状态等证据资产组织。 | 关注 artifact availability、repository、DOI、dead link、by request 等。 | 1 | 需区分制品层和论文层分母。 |
| 🔁 流程树 | 以检索、筛选、编码、报告、质量控制等流程组织。 | 原文主要贡献是方法流程、阶段、输入输出或 researcher gate。 | 1 | 流程树不等于已完成系统综述证据。 |
| 🧰 指南树 | 以指南项、checklist、报告规范组织。 | 节点来自 protocol、search、selection、QA、extraction、synthesis、reporting 等规范项。 | 0 | 不得把指南建议当成领域统计。 |
| 🧭 路线图树 | 以挑战、行动项、开放问题组织。 | 节点来自 roadmap action、vision component、challenge、open question。 | 0 | 不得把愿景主张写成经验 finding。 |
| 🧪 理论树 | 以理论概念、构念、评价框架组织。 | 节点来自 theory、concept、construct、taxonomy 或 evaluation framework。 | 0 | 如果样本来自 convenience evaluation，统计池资格仍需降级。 |

## 3. 入池子集证据池分布与统计解释

本节只解释 `统计池资格 = 🟢 入池` 的 13 篇。非入池条目不再出现在 SUMMARY 主干统计表、覆盖矩阵、维度树总览、pattern 表或结论-证据映射中；它们只作为边界 / 风险备忘保留在 §8.1。

| 入池子集切面 | 入池数量 | 解释 | A2a/A2b 用途 |
|---|---:|---|---|
| 后续主统计池候选 | 13 | 已完成型 SLR / SMS / tertiary / MLR / 系统映射或系统映射之系统映射；均有系统语料构造、纳排、编码 / 抽取和可统计字段。 | 后续做页码、表图、附录和复制包精核后，才可用于字段频次、覆盖度、维度饱和度和候选 finding 支撑。 |
| 主样本 | 4 | 以 SLR 或 SLR+SMS 为主，能体现完整综述问题、字段抽取、统计观察和 finding 形成路径。 | 支撑 Paper2 的主流程和主线 story。 |
| 类 SLR 样本 | 9 | SMS、MLR、tertiary、systematic map of maps 等类 SLR 证据综合样本。 | 支撑脚手架泛化、样本单位差异、二次研究分母链和映射型统计。 |
| 全文但未页码精核 | 13 | 当前 13 篇都达到 `paper_content.txt` 全文文本级，但仍待 A2a 逐项核验 PDF 页码、表图和 supplementary。 | A1 只能作为 schema seed；A2a 负责把候选统计证据升级为可写作证据。 |

**本节结论**：从本节开始，SUMMARY 的主要分析表默认只展示这 13 篇入池子集。6 篇非入池条目仍有方法学或边界启发价值，但不参与主干统计、矩阵覆盖或跨论文归纳分母。

## 4. A1-M0--M6 元维度定义

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

## 5. 入池子集 A1-M0--M6 逐篇覆盖矩阵

下表是 SUMMARY 级总账视图，只展示 `统计池资格 = 🟢 入池` 的 13 篇。每格只保留短语级贡献；详细证据、可迁移性和不可迁移点见对应单篇 `review.md`。非入池条目不参与本矩阵。

| 论文 | A1-M0 | A1-M1 | A1-M2 | A1-M3 | A1-M4 | A1-M5 | A1-M6 |
|---|---|---|---|---|---|---|---|
| [LLM assistants productivity](./papers/llm-assistants-developer-productivity/review.md) | LLM assistant 生产力综述元模型 | 39 篇 peer-reviewed studies 与时间窗 | SPACE / task / benefit-risk 分类 | LLM assistant 任务与使用场景 | 生产力指标与 empirical evidence | SLR+SMS 混合统计表 | productivity benefit / risk finding |
| [Research artifacts in 二次研究](./papers/research-artifacts-secondary-studies/review.md) | secondary-study artifact 元模型 | 537 篇 二次研究 检索与筛选 | artifact reporting / availability 对象 | artifact repository / DOI / by-request 分类 | open artifact 与 dead-link 字段 | A2a 后可统计 artifact 可用性 | reproducibility gap finding |
| [MDSE modelling assistants](./papers/mdse-modelling-assistants-mapping/review.md) | MDSE assistant landscape | 系统映射 检索与分类 | 策略 / 目标 / 限制 / 指标 / 用户树 | 建模辅助方法与工具 | 指标 / 用户 / 限制证据 | 分类轴可交叉统计 | MDSE assistant gap / opportunity |
| [MDE for ML components](./papers/mde-ml-components-slr/review.md) | MDE4ML 综述对象 | SLR protocol 与 原始研究 | motivations / solutions / lifecycle objects | MDE 方法、建模语言、工具 | evaluation / limitation / artifact | 字段频次与交叉统计 | ML component engineering gap |
| [LLM4SE SLR](./papers/llm4se-systematic-review/review.md) | LLM4SE 任务与效果元模型 | 395 篇研究检索 / 纳排 | SDLC task tree / model / data | LLM 应用方式、工具、模型 | dataset、artifact、evaluation 字段 | 大规模字段统计 | LLM4SE limitation / trend finding |
| [DevSecOps primary dimensions](./papers/devsecops-primary-dimensions/review.md) | DevSecOps primary dimensions | white / grey literature 双轨 MLR | aspect / theme / CPTM taxonomy | practice / tool / metric / lifecycle | Zenodo open artifacts / QA score | CPTM 与 TA 表可统计 | GSE 空白与 challenge-practice-tool-metric finding |
| [ML4SE tertiary](./papers/ml4se-tertiary-study/review.md) | ML4SE tertiary 元模型 | tertiary search / 二次研究 | ML4SE topic / challenge 分类 | ML 方法与 SE task 分类 | quality / challenge / action evidence | 大规模 tertiary 统计 | challenge / action recommendation |
| [App reviews SLR](./papers/app-reviews-slr-se/review.md) | app reviews for SE 元模型 | 1656→182 纳排链条 | review type / technique / SE activity | mining technique 与 analysis type | F1--F18、evaluation、replication package | 多套 classification schema | support-to-SE finding 与评价缺口 |
| [Petersen 2015 mapping update](./papers/petersen-2015-mapping-guidelines-update/review.md) | SMS guideline update 元模型 | mapping studies 检索 / snowballing | topic-independent dimensions | SMS planning-conducting-reporting | quality rubric / validity taxonomy | systematic maps of maps | guideline update finding |
| [Agile RE SMS](./papers/re-agile-sms-2015/review.md) | Agile RE mapping scope | 28 articles mapping | benefit / problem / solution taxonomy | Agile RE practice categories | 短文证据与缺失 threat | 小规模 taxonomy 统计 | definition ambiguity / solution gap |
| [RE tertiary](./papers/re-tertiary-study-2014/review.md) | RE 子领域 tertiary scope | distinct reviews / publications | RE topics / 质量 / citation impact / future researchers | RE research method overview | quality / impact evidence | distinct review vs publication 分母 | RE SLR quality / impact finding |
| [da Silva 2011 updated tertiary](./papers/da-silva-2011-six-years-slr/review.md) | updated tertiary 元模型 | 新旧 tertiary 合并与增量检索 | SE topics / author / institution | EBSE practice and education dimensions | quality assessment / relevance evidence | longitudinal / update 统计 | growth + quality + practice gap |
| [Kitchenham 2009 tertiary SLR / SE SLR 状态综述](./papers/kitchenham-2009-slr-tertiary/review.md) | early SE SLR ecosystem | SLR collection and screening | topic / quality / method dimensions | EBSE method usage | quality and reporting evidence | early tertiary summary statistics | SE SLR adoption / quality finding |

**本节结论**：13 篇入池论文已经逐篇投影到 A1-M0--M6，并在单篇 `review.md` 中保留详细证据。SUMMARY 级矩阵说明入池子集已经覆盖元模型、检索分母、主题语义、方法干预、评价证据、统计就绪和 finding 裁决七层；非入池条目只保留在边界备忘中，不参与本矩阵分母。


## 5.1 survey_of_surveys 自身 S1--S8 schema

本节把 `survey_of_surveys/` 自身也当作一篇脚手架综述来维护：每篇样本论文不仅要复原自己的原生维度树，还要投影到 S1--S8，便于后续 A2a/A2b 汇总“SE 综述通常如何设定任务、构造语料、定义维度、形成统计观察和 research finding”。S1--S8 是二级汇总 schema，不替代单篇原生维度树，不产生目标领域最终发现。

本轮 S1--S8 抽取已按“一篇论文至少一个独立 subagent”完成 19/19 篇只读审计；但 SUMMARY 主干 S1--S8 覆盖矩阵只展示 13 篇入池论文。批次证据入口为 [audits/a1-s1s8-19x1/](./audits/a1-s1s8-19x1/)，其中 [TASKS.tsv](./audits/a1-s1s8-19x1/TASKS.tsv) 记录 19 个唯一 agent 与任务状态，`results/<slug>.md` 保存独立审计输出或忠实压缩归档，`adjudications/<slug>.md` 保存主线程采纳 / 不采纳裁决。重复调度的 `research-artifacts-secondary-studies` 另有多路 sanity check，最终以主线程裁决后的 `review.md` 表格为当前事实口径。

**四分栏拆分纪律**：每篇单篇 `review.md` 的 S1--S8 小节除等级表外，必须额外保留 `S1--S8 四分栏证据拆分` 表，把 `原文证据`、`维度树复原`、`统计池资格` 和 `A2a 待核验` 分开。这样做是为了避免后续 A2a / A2b 把本地维度树解释、roadmap 启发或文本级统计观察误读为最终定量证据。

### 5.1.1 S1--S8 定义与判定标准

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

### 5.1.2 入池子集 S1--S4 逐篇覆盖矩阵

| 年份 | 论文 | S1 任务设定 | S2 语料筛选 | S3 原生树/编码对象 | S4 字段级证据 |
|---:|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文设定为围绕 LLM-assistants 对软件开发者生产力影响的 SLR+SMS，RQ0--RQ3 覆盖研究图景、方法实践、收益/风险和 SPACE 维度映射。 | 强：给出数据库、控制论文、五轮 query iteration、纳排标准、Rayyan 筛选、snowballing、QA 排除和 9756→8953→228→44→39 的分母链。 | 强：原生编码对象是 39 篇 peer-reviewed 原始研究 PS1--PS39，维度结构是以 PS-id 为主键的多根 RQ 维度森林。 | 强：字段级抽取覆盖 study goals、tools、strategy/design、tasks、settings、key results、instrument、metric、benefit/risk、SPACE mapping，并通过表格和 PS-id 保持可追踪。 |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是软件工程二次研究的系统映射，任务是审计 research artifact 的报告、可获得性、存放方式与时间/venue 影响。 | 强：使用 Scopus、16 个 ISSN token / 15 个期刊、标题综述类关键词与 2013--2023 年窗口检索，643 篇初始结果经 IC1--IC3 筛选后纳入 537 篇。 | 强：样本单位是每篇 secondary study；原生编码字段包括 year、venue、artifact availability、permanent repo、by request、dead link、dedicated section；logistic regression 属于派生统计输出，不是逐样本编码叶子。 | 中：正文支持聚合字段与统计表，但未核验 Zenodo 原始逐篇清单；当前强在 aggregate table，sample-level artifact list / sample ID / artifact link 待 A2a/Zenodo 核验。 |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文以“辅助人类在 MDSE 工具中完成软件建模任务”为主任务，采用 MRQ 统领文献侧 RQ1--RQ3 与实践侧 RQ4。 | 强：文献侧采用五个数据库检索、PICO search string、I/E criteria、QA 与滚雪球，形成 3176 条筛查记录到 58 个研究提案；实践侧覆盖 Gartner MQ 2023 相关平台文档。 | 强：原生结构是维度森林：文献侧以提案为编码对象，按策略、目标、限制、指标、目标用户五类树编码；实践侧把工具文档 quote 投影到同一编码体系。 | 中：有 RQ 驱动抽取规则、Table 2--5 和实践 quote，但当前证据链仍多为树级泛定位，尚未逐字段精确到页码、表号、样本 ID 或 Zenodo raw data。 |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是 Kitchenham-style SLR，任务设定为系统综述 MDE4ML 的 motivations、approaches/tools、evaluation、limitations/future work。 | 强：自动检索 7 个数据库，3934 条去重至 3570 条，经三轮筛选得 32 篇，再 snowballing 增补 14 篇，最终 46 篇。 | 强：样本编码对象为 P1--P46 原始研究；原生结构为 Fig. 5 单根 feature tree，并辅以纳排 schema 与 QA1--QA5 质量量规。 | 强：原文用 40-question Google Form、5 个 section 和 Table 3--8/QA 表把 RQ 映射为 goal、ML technique、domain、tool、evaluation、limitations 等字段；raw 40-question form 与完整 Fig. 5 树待数据仓库/PDF 精核。 |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md#survey_of_surveys-自身-schema-抽取) | 强：该文以 LLM4SE 为对象，设置 RQ1--RQ4 覆盖模型、数据、优化/评价和 SE 任务，并声明采用 Kitchenham-style SLR。 | 强：语料覆盖 2017 年 1 月至 2024 年 1 月，论文收集截止日为 2024-01-31；经 QGS、7 个数据库检索、多阶段过滤、QAC 质量评估和 snowballing，最终纳入 395 篇。 | 强：样本编码对象是一篇 LLM4SE primary study；原生结构是 4 个 RQ 展开的维度森林，并由 Table 5 的 8 项 data items 串联。 | 强：字段级证据由 Table 5 定义字段合同，并通过 Appendix A--E 将 data type、input form、prompt、metric、SE task 等取值回链到 primary-study references。 |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文明确设定为 DevSecOps 的多声部文献综述，RQ1 抽取 aspects/themes/links，RQ2 检查 GSE context 中的应用空白。 | 强：采用 white literature + grey literature 双轨检索、两套 search string、纳排、QA 和 snowballing；confirmatory search 只作新近验证，不进入 TA/CPTM 主统计语料。 | 强：原生结构是 5 个 aspect 构成的维度森林，并以 text segment/code/theme/category 到 CPTM 节点与关系边为编码对象。 | 强：字段级证据覆盖 definitions、challenges、practices、metrics、tools 的 text segment/code/theme/category 计数、ID、频次、source-ID 与关系映射；CPTM 关系边与 Zenodo full model 待 A2a 精核。 |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是 ML4SE 三级研究，目标是系统收集、质量评价、汇总并分类二次研究，围绕 SE task 覆盖、欠研究 KA 与 ML technique 三个 RQ 展开。 | 强：语料链为 1567 去重结果 → 140 候选 → 83 篇 QA≥2.0 的二次研究，采用数据库检索、手工检索、snowballing、IC/EC、Kappa≥0.8 双人选择与 DARE-4 质量评估。 | 强：原生编码对象是 83 篇二次研究，维度树是共根维度森林：书目信息、研究设计、质量评价、primary 覆盖度、SWEBOK KA×SE task、ML 四轴、建议、威胁和复现制品。 | 中：字段清单充分，但多依赖 Table 3--7、Fig. 3--6 与 supplementary；当前图表/表格和部分 sample-level 字段待 A2a 精核。 |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文以 app reviews 如何支持软件工程活动为综述对象，RQ1--RQ5 覆盖分析类型、挖掘技术、SE activity、评价方法与评价结果。 | 强：本文遵循 Kitchenham 与 PRISMA 风格流程：1656 个初始命中减去 303 个重复后筛选 1353 个题摘，保留 128 篇初始纳入并经手工检索 14 篇、snowballing 40 篇扩展至 182 篇。 | 强：样本编码对象为 182 篇 peer-reviewed 原始研究；原生结构包括 F1--F18 抽取表、3 套分类 schema、SE activity 树和评价/复现资产字段。 | 强：Table 3 的 F1--F18 字段覆盖书目信息、分析类型、技术、SE 活动、评价流程/指标/结果、标注数据集、质量量规和 replication package。 |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文以“对 SE 系统映射研究做系统映射并更新 mapping guideline”为任务，RQ 覆盖 guideline 使用、SE topic、venue/year 与 mapping process 执行。 | 强：有数据库、检索式、时间窗、去重、题摘、全文、snowballing、QA 和回补排除研究；57 是 QA 中间候选，52 是 final included mapping studies 分母。 | 强：被编码样本单位是 52 篇 SE 系统映射研究，原生结构是抽取表单树、分类切面树、guideline action/rubric 树和 validity taxonomy 树组成的维度森林。 | 中：Table 3 与 Appendix B 支撑字段级编码，但当前核心证据多为 not_verified / 待 A2a 图表核验；字段存在性强，逐样本表格数值仍待精核。 |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是面向敏捷软件开发中需求工程的 SMS，显式提出 3 个 RQ：研究分布、收益、问题及对应解决方案。 | 强：作者使用 Scopus、给出检索式和 2014-09 时间窗，并保留 241→187→65→28 的筛选分母链。 | 强：被编码对象是 28 篇原始研究 S1--S28，原生结构为 venue/context/article-type/benefit/problem-solution 维度森林，其中 problem→solution 是显式关系边。 | 中：叶子字段覆盖检索库、检索式、分母链、venue、agile context、article type、B1--B6、P1--P6 与 solution 关系；短文表格和页码待 A2a PDF 视觉核验。 |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是 RE 领域三级研究，目标是综览 RE SLR，并回答覆盖领域、发表 SLR 质量、覆盖缺口 3 个 RQ。 | 强：作者采用 5 个数据库、snowball、手工 venue 扫描与 3 条纳入标准，形成 64 publications / 53 distinct SLR 的最终语料，QA 分母为 51。 | 强：原生编码对象是 distinct SLR study，维度森林包括 publication metadata、SLR 抽取信息、topic group、scope、QA rubric、citation/impact、gap taxonomy 和 publication type。 | 中：核心叶子字段、QA rubric 与 Appendix S-ID 可复原，但图表/页码/样本级精确证据待 A2a PDF 核验，当前不宜写强。 |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文是更新型三级研究，新增检索窗口为 2008-07-01 至 2009-12-31，整合 OS/FE 后覆盖 2004-01-01 至 2009-12-31，设置 RQ1--RQ5 比较数量增长、主题覆盖、作者/机构、既有限制与质量提升。 | 强：语料通过 6 个自动数据库、13 个手工源和回溯引用收集；77 个 unique SLRs 进入 QA 与 data extraction，排除 10 篇后最终 SE 分析分母为 67，整合 OS/FE 后 N=120。 | 强：主样本单位是已发表二级研究，SE 新增 67 篇、整合 OS/FE 后 N=120；原生结构为抽取表、QA 量规、主题分类、人员关系和更新关系维度森林。 | 强：原文明示 10 个抽取字段和 QA1--QA4 评分量规，并在 Table 2/Table 3/Table 5 等表中实例化样本级编码。 |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文明确设定为对 2004 年以来 SE 领域 SLR/MA 的 tertiary SLR，RQ 覆盖活动量、主题、研究者/机构和研究限制。 | 强：语料通过 10 个期刊、4 个会议、个人/网站补检索形成，具备显式纳排标准和 2506→33→19、外部补入至 N=20 的分母链。 | 强：原生编码对象是 20 篇二次研究，主树为 SLR/MA 抽取编码表，并列 DARE 质量评价子树与检索漏斗子树。 | 强：叶子字段包括来源、年份、文章类型、主题类型、主题领域、作者/机构/国家、EBSE 引用、实践者指南、一级研究数、QA1--QA4、漏斗字段和排除原因。 |

**本节结论**：完成型 SLR/SMS/tertiary/MLR 普遍在 S1--S4 上较强；roadmap、vision、solution proposal 和 guideline 需要在 S1/S3/S4 中显式降级，不能因为能贡献结构种子就混入普通统计池。A2a 不应只扩论文数量，还要优先补强字段级证据可回链、图表/页码/制品可复验的样本。


### 5.1.3 入池子集 S5--S8 逐篇覆盖矩阵

| 年份 | 论文 | S5 模式演化 | S6 统计分析 | S7 候选 finding | S8 质疑与裁决 |
|---:|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文体现外部分类法 + emergent thematic coding：先用既有 taxonomy/SPACE 框架，再经 targeted thematic analysis 形成 benefit/risk 与 SPACE sub-dimensions。 | 强：RQ0--RQ3 将字段表转化为频次、比例、分布、交叉关系、组合覆盖和缺口统计。 | 强：本文从统计观察与 discussion 形成候选发现，并保留 contested finding 与边界条件，例如 code quality 同时作为 benefit/risk。 | 中：本文没有正式裁决日志或一致性系数；有搜索式集体确认、excluded paper 复查、weekly meetings、citation-against-original-text 回查，但 initial screening/data extraction 主要由第一作者执行。 |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md#survey_of_surveys-自身-schema-抽取) | 弱：原文没有说明字段、代码本或分类方案如何形成/迭代；year trend 是 artifact availability 等字段取值变化，不是 schema 演化。 | 强：统计分析包括 venue/year 交叉表、537/169/79 等分母切换，以及以年份和期刊预测 artifact availability 的二元 logistic regression。 | 强：候选发现是二次研究 artifact availability 在增长，但永久仓库/DOI 采用不足，Data Availability section 的表面透明度风险（作者批评，强度低于 169/537、65/169 等统计 finding）。 | 中：原文有人工筛选、Krippendorff’s Alpha、一致性评估、人工检查关键词上下文和 limitations，但无完整 disagreement adjudication log。 |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md#survey_of_surveys-自身-schema-抽取) | 中：维度模式来自 RQ 驱动的数据抽取与术语聚类，并承认 tool/method/technique/framework 等边界存在主观解释。 | 强：原文给出分母链、策略比例、目标/限制报告率、指标/目标用户比例、实践侧文档缺失率，并用 bubble chart / comparative analysis 连接字段；最终定量需 A2a 精核。 | 强：限制、指标、目标用户报告不足有统计支撑；AI/LLM 改变 modelling assistance 的判断只作中/弱候选启发，不能与字段统计支撑 finding 混写。 | 中：原文具备多 reviewer 筛选、Kappa agreement、R3/R4 复核讨论、triangulation 和 threats 分析；数据抽取阶段裁决仍待 A2a 精核。 |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md#survey_of_surveys-自身-schema-抽取) | 中：原文说明 search string 多次修改、数据抽取前 pilot 6 篇并与其他作者对照，术语不一致经讨论达成共识；但缺少完整字段变更日志。 | 强：本文将字段表转化为 Venn、bubble chart、分布图、频次表、QA 分布和 RQ Answer Summary。 | 强：RQ Answer Summary 和 Discussion roadmap 形成候选发现，例如 effort reduction 主导、monitoring/documentation 被忽视、industrial/user study 不足和 responsible ML 需加强。 | 中：原文有 protocol review、cross-validation、pilot extraction、作者讨论和 threats，但没有双人独立编码比例、disagreement 统计或逐条裁决日志。 |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md#survey_of_surveys-自身-schema-抽取) | 中：RQ/字段形成参考 Kitchenham 与前序 DL4SE 综述，并在 full-text review 中抽取 Table 5 字段；原文未暴露 open coding、schema revision history 或 conflict log。 | 强：该文提供 N=395 主分母、数据源/输入形式子分母、架构年度趋势、SDLC 阶段分布、problem type 与 metric 分布。 | 强：原文将统计观察提升为 challenges、opportunities 与 roadmap；对 Paper2 只迁移 finding 生成模式，不迁移 LLM4SE 领域结论。 | 中：该文有 QAC、两名 reviewers secondary review、threats 和 replication package 作为质量控制机制，但缺少字段级 coder agreement 与冲突解决日志。 |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md#survey_of_surveys-自身-schema-抽取) | 强：明确呈现从 inductive thematic analysis 的 text → code → theme → category 到 lifecycle/CPTM model 的模式演化，并区分 WL 归纳与 GL 演绎分析。 | 强：提供各 aspect 的主样本分母、text segment/code/theme/category 数量、C/P/T/M 项数、频次和 WL/GL 差异；confirmatory search 仅作验证性补充。 | 强：候选发现包括实践最受关注、metrics 最薄弱、WL/GL 互补、Business challenges 在 WL 中存在、GL 中 business-related challenges = 0，business metric M20 来自 prior MLR 补入、GSE 缺失和 framework design 趋势；其中 confirmatory finding 单独降级。 | 中：原文没有独立质疑-裁决流程，但有 reflexive thematic analysis 的多作者审核协商、trustworthiness 讨论、threats 与开放材料审计。 |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文体现既有分类轴 + 开放编码/事后归纳的混合演化：SWEBOK 与 ML 四轴作为先验框架，SE task、ML application task 与 implications 经开放编码和讨论综合形成。 | 中：统计丰富，覆盖 83 篇 reviews 和 6,117 个非唯一 primary-study 覆盖计数，但表图页码与部分图表结构待 A2a 精核后才能升级为强。 | 强：候选发现来自 general recommendations 与 implications，包括更多实证/工业验证、开放数据、数据管线文档化、online/incremental ML、混合与跨域 ML。 | 中：原文有双人选择、Kappa≥0.8、双人数据抽取 with checker、QA 分歧记录与 threats 分类；本地三路审计只属于仓库审计机制，不作为原文 S8 证据。 |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md#survey_of_surveys-自身-schema-抽取) | 强：三套分类 schema 经既有分类引入、content analysis、语义合并、无关项删除、recommendation 补充和 SWEBOK 映射形成，且有 reliability 检查。 | 强：本文提供年度趋势、venue、频次、交叉表、数据集/工具表、five-number summary、range/median 和 qualitative synthesis。 | 强：§4.1--§4.10 将统计观察转化为候选发现，包括 SE use case 模糊、reference model 缺失、评价数据集偏小、复现资产不足与 practice impact 不清。 | 强：原文报告筛选样本 Cohen’s Kappa、抽取 inter/intra-rater agreement、分类 schema reliability、second coder cross-check、protocol panel review 和 threats mitigation。 |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md#survey_of_surveys-自身-schema-抽取) | 强：本文通过比较既有 guidelines 与实际 SMS 做法形成 guideline update，并强化 venue、study focus、research method 等 topic-independent facets。 | 强：对 guideline adoption、search、QA、classification、visualization、validity 和 rubric scores 有分母明确统计；A2a 前不作最终统计结论。 | 强：候选 finding 主要是方法学发现：单一 guideline 不足、需更新指南、topic-independent facets 可复用、SMS 应追求 good sample、rubric 可评价报告质量。 | 中：本文没有完整裁决日志，但讨论单人筛选/抽取偏差，并给出 first-author 复审、reference-set validation、additional reviewer + consensus、decision rules 等缓解机制。 |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文体现从 RQ 到分类表再到 finding 的模式演化：RQ1→分布字段，RQ2→benefit 枚举，RQ3→problem+solution 关系，并把空 solution set 作为缺口信号。 | 中：原文给出会议 15/28、未说明 agile context 20/28、含实证成分约 17/28、method proposal 8/28、无 solution problem 3/6 等小样本统计；表格待 A2a PDF 核验。 | 强：候选 finding 包括 agile RE 定义模糊、缺少主导 venue、user story 在大型复杂系统中不足、P3/P4/P6 缺少解决方案、方法提议缺少实证评估。 | 弱：原文有 V.D Limitations，覆盖 Scopus 单库与关键词范围限制；未呈现多研究者筛选/编码冲突裁决、一致性或 QA 协议。 |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md#survey_of_surveys-自身-schema-抽取) | 中：维度形成来自 search-term pilot、既有 tertiary/RE SLR 关键词扩展、标题摘要主题分析、第一作者分组与两位作者复核命名；不是 QA 年度趋势。 | 强：提供 publication type、SLR subtype、scope、#PS 极差与区间、QA 总分、年度发表量、Top-10 citation 等统计。 | 强：候选发现包括 QA 趋势下降、高引不等于高 QA、#PS 内部矛盾、RE 子主题覆盖缺口、半数 SLR 忽略 QA3/QA4。 | 中：原文有主题命名复核、limitations 与 QA guideline 依赖说明，但无完整多研究者筛选/编码裁决、分歧处理、kappa 或 QA 独立复核报告。 |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md#survey_of_surveys-自身-schema-抽取) | 中：本文显式建模 沿用 FE protocol、复用并调整 QA rubric、修改 QA2、采用既有 review-type 分类和 DCP 分歧裁决，但未给出完整 codebook 演化或冲突修订日志。 | 强：统计覆盖主题、质量趋势、指南引用与质量回归、实践者指南比例、原始研究 QA 比例和 primary 数量相关性；当前只作 A2a 主统计池候选，精核前不写最终定量结论。 | 中：候选发现包括 SLR 数量增长但质量评价仍不足、EBSE 实践缺口、MS 比例变化、欧洲集中性和覆盖空白，多项仍需跨论文复核。 | 强：本文有 DCP 多人编码裁决机制，并在限制讨论中记录 QA2 歧义、QA4 主观性和 protocol 描述不足等边界。 |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md#survey_of_surveys-自身-schema-抽取) | 中：原文没有显式 schema/codebook 演化；可迁移的是 RQ 驱动字段设计、DARE 质量评价与 RQ→抽取字段→统计表的分析模式。 | 强：统计分析覆盖样本数量、类型比例、主题集中度、机构/国家分布、质量得分、Spearman 相关、方差检验与检索漏斗。 | 强：候选发现包括主题覆盖偏窄、Simula 数据库策略可复用、美国 EBSE 参与不足、实践者指南不足和抽取-核对模式风险。 | 强：质量评价采用双人独立评分、分歧讨论至一致，unknown 经邮件询问作者后重评；数据抽取采用单抽取-单核对并讨论分歧。 |

**本节结论**：在 13 篇入池论文中，S5 与 S6 必须严格区分：字段取值随年份或主题变化属于统计分析，不等于维度模式演化；只有原文说明分类、编码、主题分析、指南更新、作者复核或 schema 修订过程时，才可作为 S5 的强等级支撑。S8 也必须区分一般 limitations 与正式多研究者裁决 / 一致性 / QA；本地 A1-DT 审计只能作为仓库证据链，不能冒充原文 S8 证据。


## 5.2 入池子集维度树模式总览

本节是 PR-A1-DT 后新增的跨论文入口；当前 v2 批次为 [A1-DT v2 19×3 原生维度树审计](./audits/a1dt-v2-19x3/README.md)。旧 [A1-DT v1 19×3 全文审计批次](./audits/a1dt-19x3/README.md) 仅为历史返修来源，不是当前事实口径。A1-M0--M6 说明“方法链条”，而维度树说明“单篇综述内部 schema 如何组织”。当前 19 篇均已在单篇 `review.md` 中保留 `维度树复原`，但下表只展示 13 篇入池论文。正式 A.1--A.4 审计附录集中保存在同目录 `evidence_chain.md`；具体正文以 `review.md` 为准，具体证据链以 `evidence_chain.md` 为准。

| 年份 | 论文 | 主类型 | 辅助类型 | 后续主统计池候选 | A1-DT 当前允许用途 | 单篇结论标识 | 详情 |
|---:|---|---|---|---|---|---|---|
| 2026 | [The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study](./papers/llm-assistants-developer-productivity/review.md) | RQ 驱动分类树 | 生产力 benefit-risk 评价树 | 是 | `schema_seed` | `A1DT-llm-assistants-developer-productivity-C03` | [review](./papers/llm-assistants-developer-productivity/review.md#维度树复原) |
| 2025 | [Research artifacts in secondary studies: A systematic mapping in software engineering](./papers/research-artifacts-secondary-studies/review.md) | 证据资产审计树 | artifact availability 统计树 | 是 | `schema_seed` | `A1DT-research-artifacts-secondary-studies-C03` | [review](./papers/research-artifacts-secondary-studies/review.md#维度树复原) |
| 2024 | [Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping](./papers/mdse-modelling-assistants-mapping/review.md) | 系统映射 分类树 | assistant strategy-goal-metric-user 树 | 是 | `schema_seed` | `A1DT-mdse-modelling-assistants-mapping-C03` | [review](./papers/mdse-modelling-assistants-mapping/review.md#维度树复原) |
| 2024 | [Model driven engineering for machine learning components: A systematic literature review](./papers/mde-ml-components-slr/review.md) | MDE4ML 生命周期分类树 | 解决方案 / 动机 / 评价树 | 是 | `schema_seed` | `A1DT-mde-ml-components-slr-C03` | [review](./papers/mde-ml-components-slr/review.md#维度树复原) |
| 2024 | [Large Language Models for Software Engineering: A Systematic Literature Review](./papers/llm4se-systematic-review/review.md) | 大规模 RQ 驱动分类树 | LLM4SE task-method-evidence 树 | 是 | `schema_seed` | `A1DT-llm4se-systematic-review-C03` | [review](./papers/llm4se-systematic-review/review.md#维度树复原) |
| 2024 | [Identifying the primary dimensions of DevSecOps: A multi-vocal literature review](./papers/devsecops-primary-dimensions/review.md) | 关系型维度树 | 多声部证据树 | 是 | `schema_seed` | `A1DT-devsecops-primary-dimensions-C03` | [review](./papers/devsecops-primary-dimensions/review.md#维度树复原) |
| 2023 | [Machine Learning for Software Engineering: A Tertiary Study](./papers/ml4se-tertiary-study/review.md) | tertiary 主题 / 挑战树 | action recommendation 树 | 是 | `schema_seed` | `A1DT-ml4se-tertiary-study-C03` | [review](./papers/ml4se-tertiary-study/review.md#维度树复原) |
| 2022 | [Analysing app reviews for software engineering: a systematic literature review](./papers/app-reviews-slr-se/review.md) | RQ 驱动分类树 | 评价 / 复现资产审计树 | 是 | `schema_seed` | `A1DT-app-reviews-slr-se-C03` | [review](./papers/app-reviews-slr-se/review.md#维度树复原) |
| 2015 | [A Mapping Study on Requirements Engineering in Agile Software Development](./papers/re-agile-sms-2015/review.md) | SMS problem-benefit-solution 树 | Agile RE 主题分类树 | 是 | `schema_seed` | `A1DT-re-agile-sms-2015-C03` | [review](./papers/re-agile-sms-2015/review.md#维度树复原) |
| 2015 | [Guidelines for conducting systematic mapping studies in software engineering: An update](./papers/petersen-2015-mapping-guidelines-update/review.md) | mapping guideline update 方法树 | topic-independent dimensions 树 | 是 | `schema_seed` | `A1DT-petersen-2015-mapping-guidelines-update-C03` | [review](./papers/petersen-2015-mapping-guidelines-update/review.md#维度树复原) |
| 2014 | [Systematic Reviews in Requirements Engineering: A Tertiary Study](./papers/re-tertiary-study-2014/review.md) | RE tertiary 主题统计树 | 质量 / impact 树 | 是 | `schema_seed` | `A1DT-re-tertiary-study-2014-C03` | [review](./papers/re-tertiary-study-2014/review.md#维度树复原) |
| 2011 | [Six years of systematic literature reviews in software engineering: An updated tertiary study](./papers/da-silva-2011-six-years-slr/review.md) | tertiary 更新统计树 | 质量 / EBSE 实践缺口树 | 是 | `schema_seed` | `A1DT-da-silva-2011-six-years-slr-C03` | [review](./papers/da-silva-2011-six-years-slr/review.md#维度树复原) |
| 2009 | [Systematic literature reviews in software engineering – A systematic literature review](./papers/kitchenham-2009-slr-tertiary/review.md) | tertiary 生态统计树 | 质量评价树 | 是 | `schema_seed` | `A1DT-kitchenham-2009-slr-tertiary-C03` | [review](./papers/kitchenham-2009-slr-tertiary/review.md#维度树复原) |

**本节结论**：13 篇入池论文已经显示，主统计池不是一个同质字段表，而是覆盖 RQ 驱动分类树、多根维度森林、关系型维度树、证据资产审计树和流程 / 指南更新树等多类结构。对 Paper2 来说，“维度模式”必须允许研究者从树和关系边中选择、批准和演化，而不能预设为单层表格。

## 5.3 入池子集维度树类型与 Paper2 L0--L7 的关系

| 维度树类型 | 支撑的 Paper2 阶段 | 当前入池样本 | 方法启发 |
|---|---|---|---|
| RQ 驱动分类树 / 多根维度森林 | L0 主题与综述元模型设定；L4 字段级证据抽取；L5 统计分析 | app reviews、LLM4SE、LLM assistants、MDE for ML、ML4SE tertiary、RE tertiary、Kitchenham 2009 | 先由 RQ 确定对象 / 方法 / 评价 / 结果层，再要求每个叶子绑定证据与分母；多 RQ 或多样本单位时应保留森林结构。 |
| 关系型维度树 | L4 字段抽取；L5 交叉统计；L6 候选发现形成 | DevSecOps、MDSE assistants、Agile RE、da Silva 2011 | 主干树之外必须保留边表；缺失关系本身可成为 gap 候选。 |
| 证据资产审计树 | L4 证据链；L7 透明投影 | research artifacts、app reviews、DevSecOps、LLM4SE | artifact、replication package、open science material、dead link 和 by-request 状态应是一等字段。 |
| 流程 / 指南更新树 | L1 脚手架挖掘；L2 维度模式批准；L3 论文收集与概览 | Petersen 2015 mapping guideline update | 对“方法学统计样本”要同时保留流程贡献和系统映射分母，不能与纯 guideline 混算。 |

**本节结论**：Paper2 后续实验不应只测“AI 能否抽字段”，而应测研究者如何定义 / 修改维度树、AI 如何给出证据链、统计观察如何被降级为候选发现并交给研究者裁决。上述关系只基于 13 篇入池样本；非入池 roadmap / guideline / proposal 只作为边界备忘，不进入本表。

## 5.4 入池子集 SUMMARY 结论-证据映射

| 归纳标识 | 引用键 | 归纳内容 | 归纳类型 | 分母 | 纳入结论标识列表 | 排除结论标识列表 | 证据强度过滤 | 外推限制 | 允许用于论文的位置 | 当前状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| [sum-A1DT-tree-types] | [sum-A1DT-tree-types] | 13 篇入池论文已形成多类维度树 / 维度森林，说明 survey-of-surveys 主统计池需要树型 schema 而不是单层字段表。 | tree_type_inventory | 13 篇入池 `review.md` | A1DT-llm-assistants-developer-productivity-C03, A1DT-research-artifacts-secondary-studies-C03, A1DT-mdse-modelling-assistants-mapping-C03, A1DT-mde-ml-components-slr-C03, A1DT-llm4se-systematic-review-C03, A1DT-devsecops-primary-dimensions-C03, A1DT-ml4se-tertiary-study-C03, A1DT-app-reviews-slr-se-C03, A1DT-re-agile-sms-2015-C03, A1DT-petersen-2015-mapping-guidelines-update-C03, A1DT-re-tertiary-study-2014-C03, A1DT-da-silva-2011-six-years-slr-C03, A1DT-kitchenham-2009-slr-tertiary-C03 | -- | 本行是入池子集树型索引，不纳入非入池 roadmap / guideline / proposal 的 C03。 | 这是 A1 入池子集的结构归纳，不代表 100+ 完整文库已饱和；当前只可作为 schema_seed。 | schema_seed | active |
| [sum-A1DT-statistical-pool] | [sum-A1DT-statistical-pool] | 13 篇完成型 SLR / SMS / tertiary / MLR / 系统映射是后续主统计池候选，但 PR-A1-DT 当前维度树证据仍待 A2a 精确锚定，暂不进入最终定量统计。 | pool_candidate_index | 13 篇入池 `review.md` | A1DT-llm-assistants-developer-productivity-C04, A1DT-research-artifacts-secondary-studies-C04, A1DT-mdse-modelling-assistants-mapping-C04, A1DT-mde-ml-components-slr-C04, A1DT-llm4se-systematic-review-C04, A1DT-devsecops-primary-dimensions-C04, A1DT-ml4se-tertiary-study-C04, A1DT-app-reviews-slr-se-C04, A1DT-re-agile-sms-2015-C04, A1DT-petersen-2015-mapping-guidelines-update-C04, A1DT-re-tertiary-study-2014-C04, A1DT-da-silva-2011-six-years-slr-C04, A1DT-kitchenham-2009-slr-tertiary-C04 | -- | 本行只记录入池候选资格；A1-DT v2 当前仍按 `schema_seed` 管理，待 A2a 完成精确页码 / 表图 / 字段锚定后才可升级。 | 统计池候选资格只服务后续 A2a/A2b，不支撑目标领域最终发现；弱或待核验证据不得进入定量统计。 | schema_seed | active |

**本节结论**：SUMMARY 的主干跨论文归纳现在只回链 13 篇入池论文的单篇 A.3 结论标识。非入池条目的边界价值仍在单篇 `review.md` / `evidence_chain.md` 和 §7.1 中保留，但不进入本表分母。后续若新增入池论文或修改树型，必须同步更新本表，否则 SUMMARY 归纳将失去证据链闭环。

**A1-DT v2 证据链边界**：当前正式 A.2 / A.3 是树级与核心裁决的最小 claim map，集中保存在各单篇 `evidence_chain.md`；单篇叶子取值空间、关系边、缺失值语义和图表待核验项仍以各 `review.md` 的“维度树复原”正文、叶子维度表和关系边表为细粒度说明。若两处发生冲突，以 `evidence_chain.md` 的 A.2 / A.3 与主线程裁决为准，并在 A2a 把 leaf / edge 逐项迁入统一审计附录；因此 SUMMARY 不把 A1-DT v2 写成叶子级最终统计证据。

## 6. 入池子集 pattern 总结与 A2a 接力建议

| pattern | 当前观察 | 来源样本 | A2a 处理建议 |
|---|---|---|---|
| RQ pattern | SE tertiary 常问规模、主题、主体、质量、限制、EBSE 实践缺口；现代 LLM4SE SLR 常先给 landscape / method / benefit-risk / dimension coverage。 | Kitchenham 2009、da Silva 2011、LLM assistant SLR、LLM4SE SLR | 建立 RQ 模式树，区分 landscape、method、impact、dimension coverage、gap/finding。 |
| dimension pattern | 维度应树状化而非平铺：strategy-goal-limitation-metric-user、aspect-theme-category、concept-activity-context-impact 等。 | MDSE assistant mapping、DevSecOps MLR、app reviews SLR、MDE for ML SLR | 把字段树版本化，并记录字段来源、缺失语义和 researcher adoption decision。 |
| finding pattern | finding 需从统计观察进一步形成质量缺口、EBSE 实践缺口、research challenges、roadmap、action recommendations；roadmap 只能提供启发式。 | da Silva 2011、ML4SE tertiary、DevSecOps MLR、app reviews SLR | 与 Paper2 的 候选发现 ledger 对齐，补 support / counter-evidence / claim strength。 |
| evidence presentation pattern | 常用搜索分母、纳排、quality assessment、topic taxonomy、review/primary-study 数量、artifact availability、replication package。 | research artifacts mapping、LLM4SE SLR、app reviews SLR、DevSecOps MLR | 每个字段必须有 source anchor、artifact link status 和回填状态。 |
| validity / threat pattern | 包含 search bias、inclusion reliability、quality assessment、protocol deviation、artifact dead link、model drift、human validation。 | research artifacts mapping、LLM4SE SLR、app reviews SLR、MDE for ML SLR | 设为强制字段，未报告时明确记录。 |
| report structure pattern | guideline、tertiary/SMS、SLR+SMS、MLR、roadmap 的结构不同；不能用一个模板压平。 | 13 篇入池样本 | 允许不同 `review_type` 对应不同报告结构和统计池资格。 |

A2a 第一优先级：不是补历史 PDF，而是先对当前 13 篇入池论文做图表视觉核对、页码 / 表号证据锚定，并将 A1-M0--M6 与 S1--S8 两套矩阵共同转为更正式的 pattern library；随后扩展到 30--50 篇入池核心样本，检验字段取值空间、统计池规则、finding heuristic 与研究者裁决记录是否稳定。

### 6.1 schema 修订 / 回填日志

本节是 A1 字段合同演化的结构化审计入口。它只记录会影响后续 A2a/A2b schema、统计池或字段回填的变更；普通下载、排版或 PR 施工细节仍进入更新日志或 `search/` 审计文件。

| 时间 | 触发条目 / 样本 | 受影响字段 | 修订内容 | 回填状态 | 冻结理由 / 后续处理 |
|---|---|---|---|---|---|
| 2026-07-02 22:04:02 | 用户要求每篇 survey 的 S1--S8 维度信息由独立 subagent 抽取；19 篇全文样本（其中 13 篇入池） | S1--S8 二级汇总 schema、单篇 `review.md`、SUMMARY 覆盖矩阵、A2a handoff | 新增 `survey_of_surveys 自身 schema` 定义表、S1--S8 逐篇矩阵和单篇四分栏证据拆分；19/19 篇已回填 `review.md` 的 `survey_of_surveys 自身 schema 抽取` 小节；要求后续新增论文一篇一 subagent 抽取并显式拆清原文证据 / 维度树 / 统计池资格 / A2a 待核验 | 已回填 19/19 篇 review、GUIDE、SUMMARY、audit TASKS/results/adjudications；A2a 接力项写入审计裁决与风险表 | S1--S8 用于把综述之综述自身转成可审计模式库，支撑 researcher-defined meta-model、证据链、统计分析与 finding 裁决设计；不得写成目标领域 final finding。 |
| 2026-06-29 21:10:00 | PR-A1-DT 逐篇维度树复原；19 篇全文样本（其中 13 篇入池） | 维度树、叶子取值空间、关系边、结论-证据映射、SUMMARY 归纳回链 | 新增 GUIDE 维度树纪律、schema 字段合同、19 篇 `review.md` 的 `维度树复原` 与 19 篇 `evidence_chain.md` 的 A.1--A.4 审计附录；SUMMARY 新增维度树模式总览和 `[sum-A1DT-*]` 结论-证据映射 | 已回填 19/19 篇 review、GUIDE、pattern schema 与 SUMMARY | Paper2 方法贡献需要可审计维度树，而不是平铺字段矩阵；A2a 继续做页码 / 图表精核与样本扩展。 |
| 2026-06-29 17:48:49 | 用户复核 SUMMARY 批次化问题；19 篇全文样本（其中 13 篇入池） | SUMMARY 主表、证据池、A1-M0--M6 总账矩阵 | 取消按 PR 批次拆分主表，改为统一年份降序表；明确三类证据池主归属；新增 19 篇 × A1-M0--M6 覆盖矩阵 | 已回填 SUMMARY、GUIDE 与审计目录 | 长期文库必须按对象和当前事实维护，不能按施工批次维护；A2a/A2b 继续沿用统一总账结构。 |
| 2026-06-29 17:58:30 | 三路复审 C/I：CCF 复核状态、三池计数、schema 回修入口 | `ccf_verification_status`、三类证据池计数、schema change ledger | 主表新增 `CCF 复核状态` 列；三类证据池改为主归属计数；恢复本结构化 schema 修订 / 回填日志 | 已回填 SUMMARY、GUIDE、pattern schema 与审计目录 | 防止复制主表时丢失 CCF disclaimer；防止方法学样本与边界 seed 重复计数；保留字段回修可审计入口。 |
| 2026-06-29 16:59:12 | 用户补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 PDF | 阅读状态、`eligible_for_statistical_synthesis`、manual-download 状态 | 历史 metadata-only / manual-download 条目升级为全文文本级；active manual-download 清零；Petersen 2008 保持方法学参考池，Petersen 2015 作为方法学统计样本进入主统计池 | 已回填 3 篇 `paper.pdf`、`paper_content.txt`、`review.md`、`metadata.json`、SUMMARY 与 search log | 补齐全文后才能把题摘级候选升级为全文级 pattern；统计池仍按主归属和系统性证据状态控制。 |
| 2026-06-29 15:41:07 | issue #95 十篇现代锚点 | `review_type`、`eligible_for_schema_seed`、`eligible_for_statistical_synthesis`、`evidence_role`、A1-M0--M6 | 扩展 SLR+SMS、系统映射、MLR、solution proposal、vision/roadmap、theory/evaluation/roadmap；新增 模式种子 与统计池分离字段；新增 A1-M0--M6 元维度 | 已回填 19 篇 `metadata.json`、单篇 `review.md`、SUMMARY、candidate-pool、GUIDE 和 schema | 现代 roadmap / proposal 有高启发价值但不得污染主统计池；A1-M0--M6 是 A2a/A2b 的元维度接力骨架。 |
| 2026-06-29 13:20:00 | 用户要求补充出版 / venue / CCF 字段 | `publication_type`、`venue_short_link`、`ccf_official_category`、`ccf_official_rank`、`ccf_verification_status` | 将来源字段拆成出版形态、可点击 venue、CCF 大类、CCF 等级和复核状态；官方 WAF 时显式标本地缓存 / 待人工复核 | 已回填 SUMMARY、candidate-pool、单篇 review 和 schema；主表现已补独立 `CCF 复核状态` 列 | 投稿决策需要事实来源可追溯；不能把本地缓存写成官方实时核验。 |
| 2026-06-29 02:18:07 | 初始 6 篇全文 + 3 篇失败路径 dry-run | `review_type`、`predecessor_relation`、`target_se_subfield`、`challenge_action_pattern`、`taxonomy_axis`、`problem_solution_pattern` | 建立六类 pattern 字段；识别 guideline、updated tertiary、SE 子领域和 SMS taxonomy / problem-solution 等候选字段 | 已回填初始 review、pattern schema 与 SUMMARY；后续 3 篇失败路径已在 16:59 补齐 | 证明 schema 不是先验冻结，而是由真实 dry-run 暴露缺口后回修；A2a 继续扩展取值空间。 |

**本节结论**：schema 回修有明确入口、触发条目、受影响字段、回填状态和冻结理由。后续 A2a/A2b 若新增字段或改变统计池规则，必须先在单篇 `review.md` 记录触发原因，再回修 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md)，最后在本节追加结构化记录。

## 7. 失败、风险与待复核

### 7.1 非入池条目边界备忘（不进入主干统计表）

本小节只作为风险 / 边界备忘收纳 `统计池资格 != 🟢 入池` 的条目，避免它们占用 SUMMARY 主干完整表。它们不是“无价值论文”：guideline 可支撑方法学规则，roadmap / vision / proposal 可支撑边界和 finding heuristic，但不能与完成型 SLR/SMS/MLR/tertiary 混算。

| 年份 | 标题 | 综述类型大类 | 本文角色 | 统计池资格 | 简短收纳理由 | 详情 |
|---:|---|---|---|---|---|---|
| 2026 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 🧭 路线图 | ⚫ 边界 | ⚪ 不入 | AI-native SE 愿景和挑战路线图；用于提醒愿景类论文只能作边界和挑战启发。 | [review.md](./papers/ai-native-se-roadmap/review.md) |
| 2025 | On the road to interactive LLM-based systematic mapping studies | 🧪 方案 | 🟠 种子 | ⚪ 不入 | 提供 LLM 介入 SMS 流程、人机角色、traceability 和模型漂移风险种子。 | [review.md](./papers/interactive-llm-systematic-mapping/review.md) |
| 2025 | Formal requirements engineering and large language models: A two-way roadmap | 🧭 路线图 | ⚫ 边界 | ⚪ 不入 | 启发 concern→mechanism→action 结构和 trustworthiness 边界。 | [review.md](./papers/formal-re-llm-roadmap/review.md) |
| 2023 | Requirements quality research: a harmonized theory, evaluation, and roadmap | 🧭 理论路线图 | 🟠 种子 | ⚪ 不入 | 启发 researcher-defined meta-model、理论概念树和 gap→roadmap 结构。 | [review.md](./papers/requirements-quality-theory-roadmap/review.md) |
| 2008 | Systematic Mapping Studies in Software Engineering | 🧰 指南 | 🟣 方法 | ⚪ 不入 | 定义 SMS 流程、keywording、classification facet 和 map 可视化。 | [review.md](./papers/petersen-2008-systematic-mapping/review.md) |
| 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | 🧰 指南 | 🟣 方法 | ⚪ 不入 | 提供 SE SLR 方法底座、protocol、纳排、质量评价、抽取和报告基础。 | [review.md](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |

**本小节结论**：6 篇非入池条目承担方法学参考、维度种子和边界提醒职责；后续写作时可以引用其方法或启发，但不得把它们计入主统计池分母，也不得把其观点写成系统综述统计发现。

### 7.2 风险清单

| 风险 | 当前处理 | 后续动作 |
|---|---|---|
| 图表 / 表格未全部视觉核对 | 多数条目已读 `paper_content.txt`，但并非所有图表、表格、页码和 publisher final 差异都核对 | A2a 深读时补页码、表号、图表截图或 source anchors。 |
| CCF 官方目录 WAF | 当前按本地 `ccf_venues/` 缓存标注 TOSEM=A，IST/JSS/RE/ESE=B，EASE=C；CSUR 待核验 | 正式写作 / 投稿前人工打开 CCF 官方页面复核。 |
| roadmap / proposal 误入统计池风险 | 已用 `eligible_for_statistical_synthesis=false` 与排除理由分离 | A2a 扩库时继续执行三池规则。 |
| 方法学样本与领域样本混算风险 | Kitchenham 2007、Petersen 2008 不进主统计池；Petersen 2015 标为方法学统计样本 | A2a 报告统计时分层展示。 |
| 历史 manual-download 路径 | 历史 3 条已由用户本地 Zotero PDF 补齐；[search/manual-download-needed.bib](./search/manual-download-needed.bib) active=0，仅作 A1 历史归档 | A2a 及以后新增 core / reserve 失败条目进入 [corpus/manual-download-needed.bib](./corpus/manual-download-needed.bib)、[corpus/manual-download-needed.md](./corpus/manual-download-needed.md) 和 [corpus/tables/pdf-status.csv](./corpus/tables/pdf-status.csv)，避免双事实源。 |

## 8. 后续 A2a / A2b 入口

A2a 建议：

1. 以当前 13 篇入池论文为主干，先做图表视觉核对、页码 / 表号锚定和字段证据 source anchors；6 篇非入池条目只做边界 / 方法学备忘核查。
2. 扩展到 30--50 篇入池核心样本，优先覆盖 2020 年后 SE tertiary / SLR / SMS / MLR / survey。
3. 每个 SE 子领域至少覆盖一批样本：Requirements Engineering、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE、SE secondary-study artifacts。
4. 把 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 拆成正式 pattern library，并记录字段来源、取值空间、缺失语义、统计池资格和 researcher adoption decision。
5. 对 roadmap / vision / proposal 保持 boundary / 模式种子 池，不混入主统计池。

A2b 建议：

1. 扩展到预计 100+ 篇完整文库闭合。
2. 形成第一个可引用快照。
3. 明确纳排分母、排除理由、人工下载清单、覆盖 / 饱和度判断。
4. 把完整文库快照交给 A3 消费，A3 不再混入大规模补文库。

## 9. 更新日志

| 时间 | 更新内容 | 验证 / 备注 |
|---|---|---|
| 2026-07-07 18:58:00 | 用户提供 Zotero 导出目录后，PR-A2a 将 54 篇 core / reserve 人工下载 PDF 显式复制入对应 `papers/<slug>/paper.pdf`，生成 `paper_content.txt`、`bibtex.bib` 与 `metadata.json`；新增 Zotero 导入脚本与导入清单，2 篇损坏 / 错配附件继续留在人工下载清单。 | 已运行 `build_corpus_tables.py` 与 `validate_corpus.py`，当前输出 438/293/120/40/145/91/69；`manual-download-needed.bib` 从 145 条降为 91 条。 |
| 2026-07-06 23:27:24 | 加固 PR-A2a PDF 状态可复算性：禁止 `build_corpus_tables.py` / `acquire_pdfs.py` 因前序 `/tmp` 本地临时路径存在而把条目标为 `downloaded` 或复制仓库外 PDF；新增 `local_snapshot_only` 失败类型，并要求非 downloaded 行不得携带旧审计 `pdf_sha256`。 | 已运行 `build_corpus_tables.py`、`acquire_pdfs.py`、`validate_corpus.py`、`py_compile`、`git diff --check`；额外构造 `/tmp/issue95_all_pdfs_v2/10_1145_3708532.pdf` 假文件后复算，目标条目仍为 `manual_needed` / `local_snapshot_only`，说明外部临时路径不会污染正式统计。 |
| 2026-07-06 22:52:09 | 完成 PR-A2a 综述语料候选库建设：新增 [corpus/](./corpus/) 入口、[raw/selection-seed.csv](./corpus/raw/selection-seed.csv) 主候选选择种子、全量候选账本 438、系统化候选 293、主候选 120、替补 40、边界池 145；新增 2 篇 A2a 候选论文的 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`metadata.json`，并生成 145 条人工下载 BibTeX。 | `validate_corpus.py` 通过并输出 438/293/120/40/145/145/15；`py_compile` 通过；`git diff --check` 通过；A1 13 篇入池资产未被覆盖，A2a 新增论文仍标记 `a2a_review_status=not_started`，不计为 A2b 深读完成。 |
| 2026-06-29 21:10:00 | 完成 PR-A1-DT 实现：补充 GUIDE 维度树复原规则、pattern schema 字段合同、19 篇单篇 `review.md` 的维度树复原与 19 篇 `evidence_chain.md` 的 A.1--A.4 审计附录，并在 SUMMARY 增加维度树模式总览和 SUMMARY 结论-证据映射。 | A1 原始阶段未读取 `.env`；A1-DT v2 批次已完成 57/57 CLI 审计，日志保留命令/stdout/stderr与环境摘要，关于 `.env` 只记录 `env_sourced=.env exists`，不记录 secret；A1-DT 仍保留 A2a 页码 / 表图精核边界。 |
| 2026-06-29 17:40:27 | 根据用户对 SUMMARY 缝合感和批次拆表问题的反馈，重构 SUMMARY 为长期文库总账：取消批次化主表，改为统一年份降序论文表；补充三类证据池标准；新增 19 篇 × A1-M0--M6 覆盖矩阵；把历史过程下沉为风险 / 日志。 | 本轮只重构总账和规则，不新增论文；后续需同步 GUIDE 与 PR body，并复验 19/19/19/19、active manual=0。 |
| 2026-06-29 16:59:12 | 用户提供 3 篇历史 manual-download PDF 后，补齐 app reviews SLR 2022、Petersen 2008、Petersen 2015 的 `paper.pdf`、`paper_content.txt`、全文级 `review.md` 和 `metadata.json`，并将 active 人工下载清单清零。 | 文件系统统计更新为 19 个 `review.md`、19 个 `metadata.json`、19 个 `paper.pdf`、19 个 `paper_content.txt`；3 篇历史失败路径已闭环，剩余风险转为 A2a 图表视觉核对和 CCF 官方人工复核。 |
| 2026-06-29 16:13:28 | 修复三路 reviewer 复审提出的 C/I：补齐早期 9 篇 `metadata.json`，统一 19 篇机器可读字段，修正 CSUR CCF 待核验口径，并清理 `paper_content.txt` 行尾空白。 | `git diff --check` 两点工作区口径通过；提交后需再用 PR 三点 diff 复验。 |
| 2026-06-29 15:41:07 | 根据内部复核修复 A1-M0--M6 命名、SUMMARY 19/16/3 历史总账、#95 metadata 全文状态、roadmap / proposal 统计池排除字段，并记录 CCF 官方页面 WAF 风险。 | 当时文件系统统计：19 个 `review.md`、19 个 `metadata.json`、16 个 `paper.pdf`、16 个 `paper_content.txt`、3 个 manual-download BibTeX 条目；后续 16:59 已补齐为 19/19/19/19。 |
| 2026-06-29 13:20:00 | 按用户新增要求补充 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级` 四列，并同步单篇 review 快速卡片、候选池和字段 schema。 | CCF 字段按官方完整目录口径设计；本轮 HTTP/CLI 访问官方页受 WAF 限制，工作表暂用本地缓存并标注正式写作前需人工复核。 |
| 2026-06-29 02:18:07 | 建立 `survey_of_surveys/` README/GUIDE/SUMMARY/search/papers/patterns；完成 6 篇全文文本级 dry-run 和 3 篇 metadata-only 失败路径；回修 schema 字段。 | A1 奠基；未运行真实 LLM，未读取 `.env`，不跑四个真实例子。 |
