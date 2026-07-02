# Identifying the primary dimensions of DevSecOps: A multi-vocal literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review |
| 作者 | Xiaofan Zhao; Tony Clear; Ramesh Lal |
| 年份 | 2024；online 2024-04-23；JSS 214:112063 |
| DOI | <https://doi.org/10.1016/j.jss.2024.112063> |
| 类型 | multivocal literature review；Thematic Analysis；DevSecOps primary dimensions |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 阅读状态 | 已读全文文本-paper_content核验；本轮未逐图 PDF 细核 Fig. 5--9 的连线细节 |
| 证据等级 | 全文文本级；图表/数值细节待 PDF / Zenodo full CPTM 复核 |
| 研究对象 | DevSecOps 的定义、挑战、实践、工具/技术、指标/度量，以及 DevSecOps 在 Global Software Engineering, GSE 中的应用空白 |
| 样本规模 | 主 MLR：white literature 104 篇、灰色文献（grey literature） 43 篇，时间范围 2012--2021；另有 2022 年前后的 confirmatory search 13 篇 WL + 7 篇 GL，但未进入 TA 与最终 CPTM 模型 |
| 核心方法 | white/grey 双轨检索；Search String 1 处理 DevSecOps 全局现状，Search String 2 加入 GSE/global/distributed 词簇；质量评价；snowballing；reflexive thematic analysis；生命周期框架映射 |
| 核心产物 | 五大方面；OPC / PC / Technology / Business 四类高阶主题；C/P/T/M 编号化主题；Gartner 十阶段生命周期；Challenge-Practice-Tool-Metric, CPTM 模型 |
| Open Science | 论文声明 JSS Open Science Board 已验证开放材料；Zenodo 入口包含 protocol、included papers + QA score、raw text/codes、thematic synthesis、TA tables、full CPTM model |
| 对 Paper2 的一句话价值 | 这篇文献是“维度树 + 多声部证据链 + 主题到模型”的强样本：可把 Paper2 的维度模式从平铺字段推进到“字段树、证据来源、质量门槛、跨字段 link、生命周期投影、发现缺口”的可审计结构。 |
| 是否目标证据池 | 否；只作为 survey-of-surveys 脚手架和维度模式先验，不支撑 Paper2 目标领域最终 finding。 |

## 2. 全文内容详读

### 2.1 背景 / 问题设定

论文从 DevOps 中安全需求被低估这一问题切入：安全常被视为降低交付速度的阻碍，而云、容器、serverless、多云、SaaS、快速交付和全球分布式系统又让安全前置更加必要。DevSecOps 被定义为 DevOps 的安全导向扩展，核心目标是在不显著牺牲速度与质量的前提下，把安全实践整合进 development、operations、security 团队协作过程，并通过 shift-left 和 continuous security 降低后期修复成本。

这篇文献的第二条问题线是 GSE。作者认为 DevOps/DevSecOps 与 GSE 都属于 collaborative software engineering，均依赖 communication、coordination、cooperation；因此，如果 DevSecOps 要在全球分布式环境中落地，就应当能观察到 GSE 维度。但全文最后的关键负面发现恰恰是：现有 white 和 灰色文献（grey literature） 几乎没有真正覆盖 Global DevSecOps。

### 2.2 与既有 DevSecOps review 的关系

原文系统比较了 Mohan and Othmane 2016 系统映射研究、Myrbakken and Colomo-Palacios 2017 MLR、Prates et al. 2019 MLR、Sanchez-Gordon and Colomo-Palacios 2020 SLR、Mao et al. 2020 GLR、Akbar et al. 2022 MLR + survey、Rajapakse et al. 2022 SLR + TA 等相关综述。作者对自身工作的定位不是“最早综述”，而是：

1. 用更完整的 white + grey 双轨来源覆盖 DevSecOps 第一个十年。
2. 不只停留在 challenge / practice / tool 等单一方面，而是把 aspects、themes 和 links 一起建模。
3. 使用 Thematic Analysis 的四级抽象：text -> code -> theme -> model；并强调既有相近综述多停在 theme 层。
4. 显式检查 DevSecOps 在 GSE 场景中的研究空白。
5. 通过 confirmatory search 与既有二级研究交叉验证，而不是把旧综述直接纳入主样本。

对 Paper2 来说，这种“前序综述关系”很重要：单篇 review 不应只记录本研究做了什么，还应记录它如何复现、验证、扩展、整合或区别于已有 二次研究。

### 2.3 RQ1 / RQ2

原文两个研究问题非常适合作为 Paper2 的 RQ pattern 先验：

| RQ | 内容 | 可迁移模式 |
|---|---|---|
| RQ1 | DevSecOps 在现有 white + 灰色文献（grey literature） 中的当前状态是什么，包括涉及哪些 aspects、每个 aspect 有哪些 themes、这些 aspects/themes 如何互相链接？ | “现状 + 维度 + 主题 + 关系”的复合型 RQ；不仅统计类别，还要求建立 link/model。 |
| RQ1.1 | 现有文献中可以发现哪些 DevSecOps aspects？ | primary dimension discovery。 |
| RQ1.2 | 这些 aspects 包含哪些 themes？ | aspect 内部主题抽取与分类。 |
| RQ1.3 | 识别出的 aspects 和 themes 如何互相链接？ | 从 taxonomy 走向 model / cross-field relation。 |
| RQ2 | DevSecOps 如何在 GSE contexts 中被采用？ | 用目标领域维度检查特定 context 是否缺失，形成 negative finding / research gap。 |

### 2.4 White + 灰色文献（grey literature） 与 dual-track search

论文采用 MLR 而非普通 SLR，理由是 DevSecOps 属于实践快速演化主题，很多经验先出现在技术报告、网站、博客、厂商材料等 灰色文献（grey literature） 中。其检索设计具有可迁移价值：

1. **White literature 来源**：ACM Digital Library、IEEE Xplore、Scopus。ScienceDirect 和 Springer 没作为主检索库，但用于 snowballing 与 confirmatory search。
2. **Grey literature 来源**：Google；作者浏览 Search String 1 的前 18 页结果，因为第 19 页后相关性显著变弱；Search String 2 的 GL 搜索浏览前 10 页且未发现同时覆盖 GSE、DevOps、security 的材料。
3. **Search String 1**：围绕 `devops` 与 `security/secure/safe`，并加入 `secdevops` / `devsecops`。作者解释了为何把 `safe` 纳入：安全与安全性在若干语境中有交叉，且 security flaws 可能 compromise safety。
4. **Search String 2**：在 String 1 基础上加入 GSE/GSD/global/distributed/multi-site/multi-nation/transnational/remote work 等词簇，用于捕捉 RQ2。
5. **时间范围**：2012--2021；DevSecOps 概念早期出现于 2012 附近，实际最早相关论文约 2013。
6. **纳排与 QA**：纳入条件要求涉及 DevSecOps primary aspects、英文、2012 年后、方法/研究设计清楚、来源可信；排除无全文、领域外、方法不严谨、重复、二次研究 等。QA 表包含 14 个 yes/no 问题加 literature type 0--4 分，总分 18，阈值 11。
7. **Snowballing / replication**：二次研究 不进主 MLR，但被用来验证 overlap 和补充 findings；这相当于把前序综述作为“验证源”而非“主证据源”。
8. **Confirmatory search**：主收集到 2021 年 7 月结束；之后为了避免 staleness 到 2022 年做 confirmatory search，加入 13 WL + 7 GL，但明确不进入 TA 与 CPTM。

该设计对 Paper2 的启发是：检索日志不能只记录最终 included set，还应记录主样本、补充验证样本、确认性搜索样本、排除二级研究但用作验证的策略，以及为什么某些来源不进入最终模型。

### 2.5 Thematic Analysis：text -> code -> theme -> model

方法部分最值得抽取的是 TA 的分层过程：

1. 研究立场是 pragmatic，前半段检索 / 筛选 / QA 更偏 positivist，后半段 synthesis / interpretation 更偏 interpretive。
2. 使用 reflexive TA，而非 coding reliability TA；作者明确说明 reflexive TA 不要求独立编码者一致性，因为研究者主观性被视为知识生产资源，而非必须被压制的噪声。
3. 编码主要由第一作者完成，但第二、第三作者通过 weekly / bi-weekly meeting 审核、协商和达成共识。
4. WL 先用 inductive approach 生成 codes/themes；GL 后续主要以 WL 产生的 codes/themes 为基础做 deductive analysis。
5. 作者意识到纯 TA 若没有理论框架会停留在描述层，因此把 theme 分类映射到 DevSecOps lifecycle framework，最终形成 CPTM model。

对 Paper2 来说，这提示维度模式演化可以显式区分：**归纳产生字段 / 主题** 与 **演绎投影到框架 / 生命周期 / 元模型**。这比一次性让 LLM 生成扁平 schema 更可审计。

### 2.6 RQ1：五大方面与四类高阶主题

原文识别出 DevSecOps 的五大方面：Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement。进一步，definitions / challenges / practices / metrics 多被分类到四类高阶主题：Organization, People and Culture, OPC；Process Capabilities, PC；Technology；Business。Tools 则全部先归入 Technology，再在 CPTM 中按实践关系出现在不同阶段。

| Aspect | 原文抽取规模 / 主题结果 | 关键观察 | 对 Paper2 的字段启发 |
|---|---|---|---|
| Definitions | 28 WL + 15 GL definitions；74 codes；21 themes；4 类别（categories） | 定义不仅是句子，还可拆成 collaboration、shared responsibility、shift-left、automation、quality/business 等 theme；Mohan and Othmane 2016 的定义最常被引用。 | `definition_source`、`definition_text_segment`、`definition_code`、`definition_theme`、`definition_category`、`common_definition_author`、`citation_frequency`。 |
| Challenges | 73 WL + 53 GL challenges；85 codes；23 themes；最终 28 challenges | OPC 挑战最多；collaboration/communication/coordination、security skill/training、security integration without losing speed、cloud/serverless complications、mature tools 缺失是高频问题。 | `challenge_id`、`challenge_theme`、`challenge_category`、`frequency`、`source_type`、`matched_previous_review`、`linked_practice`。 |
| Practices | 219 WL + 137 GL practices；142 codes；56 themes；最终 60 practices | Technology practices 最多；automation 是最强 theme；shift-left 是 PC 核心实践；business practices 主要来自 GL。 | `practice_id`、`practice_theme`、`practice_category`、`addresses_challenge`、`source_type`、`linked_tool`、`linked_metric`。 |
| Metrics / Measurement | 7 WL + 13 GL metrics；20 codes；16 themes；最终 20 metrics | 度量是最薄弱方面；WL 很少，GL 提供更多；可映射到若干 DevOps metrics。 | `metric_id`、`metric_name`、`measuring_method`、`goal`、`category`、`mapped_devops_metric`、`linked_practice`。 |
| Tools / Technologies | 18 WL + 45 GL tools；56 tool codes；16 themes，补充后 18 tool groups | Docker/Kubernetes 等 container tools、Chef/Jenkins/Puppet 等 automation platform、SAST/DAST/IAST/SCA、vulnerability management tools 等成为功能组。 | `tool_id`、`tool_name`、`tool_function_group`、`source_type`、`linked_practice`、`生命周期阶段（lifecycle_stage）`。 |

### 2.7 CPTM model：从主题表到生命周期模型

论文最核心的模型贡献是 Challenge-Practice-Tool-Metric, CPTM model。它把四类元素放入 Gartner DevSecOps 十阶段生命周期：Plan、Create、Verify、Preproduction、Release、Prevent、Detect、Respond、Predict、Adapt，并用连线表示：

```text
Challenge -> Practice -> Tool -> Metric
```

模型的关键解释包括：

1. **Plan / Create** 集中承载 OPC 与 PC 相关挑战和实践，体现 shift-left：许多安全与组织问题要在最早阶段计划和创建。
2. **Verify / Preproduction / Release / Prevent / Detect / Respond / Predict** 更集中出现 Technology 相关挑战、工具和实践，说明 DevSecOps 落地高度依赖自动化、安全测试、运行时监控、云和容器安全工具。
3. **Business** 不只出现在 Plan / Adapt，也出现在 Release，提示业务约束与发布、客户 readiness、成本、连续性相关。
4. CPTM 不是简单 taxonomy，而是“字段间关系模型”：每个 C/P/T/M 项目有编号、类别、生命周期 stage 和互相映射关系。
5. 并不是所有 实践条目并不都有关联工具或指标；这种缺口本身就是发现：字段树必须允许 `未报告`、`无关联指标`、`无关联工具`。

对 Paper2 来说，CPTM 是非常强的“维度模式不应平铺”的例子：一个可用的综述 schema 应支持实体、属性、证据、阶段、关系、缺失和模型投影。

### 2.8 RQ2：GSE 空白

RQ2 得到的是典型 negative finding。Search String 1 没找到 DevSecOps + GSE 相关文献；Search String 2 加入 GSE/global/distributed 词后，最终只有 2 篇 WL 同时涉及 GSE、DevOps 和 security，但它们也不是完整 Global DevSecOps 研究；GL 方向浏览前 10 页没有找到同时覆盖三者的材料。

作者给出四种解释可能：

1. GSE 与 DevSecOps 之间可能没有显著差异性关系。
2. 安全可能在组织中偏集中和控制导向，因此 global aspects 不突出。
3. 这是一个真实 research gap。
4. 也可能是 search string 漏掉了特定术语，尽管作者已多次调整词串。

这对 Paper2 的启发是：absence/gap 类发现必须保留检索式、变体、失败路径和解释竞争项，不能把“没搜到”升级为强结论。

### 2.9 Quality / validity / trustworthiness

原文报告的质量与效度处理有三层：

1. **主样本质量评价**：QA 表总分 18、阈值 11；QA score 随开放材料发布。
2. **TA trustworthiness**：按 credibility、confirmability、dependability、transferability 组织；credibility 依赖 原始研究 quality 与合适 text segments；confirmability 依赖多作者讨论与资深作者审核；dependability 通过与其他 SLR/MLR 比较验证；transferability 计划通过后续 Delphi study 验证。
3. **Threats to validity**：包括 study selection / QA / data extraction bias，coding/theming 由第一作者主导导致的 synthesis threat，既有 CAMS / DevOps 元素可能影响编码，search string 构造可能漏掉 GSE 术语。

这里的可迁移点不是“必须有 inter-rater reliability”，而是要把方法选择与信度口径一致起来：如果采用 reflexive TA，就不能机械要求 coding agreement；但必须记录主观性来源、协商过程、开放材料和验证路径。

### 2.10 Open Science material

论文在摘要首页和 Data availability 中都强调开放材料。Zenodo 入口包含：MLR protocol、included papers + quality assessment score、raw data/text and codes、white/grey thematic synthesis、thematic analysis tables 初版与完成版、full CPTM model。JSS Open Science Board 已验证这些材料。

对 Paper2 来说，这可作为“开放审计制品链”的参照：不是只在论文中画流程图，而是要把 protocol、抽取表、编码表、模型、QA score 和缺失/排除记录作为可复核材料发布或至少内部归档。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 采用“现状 + aspects + themes + links”作为 RQ1，并用 RQ2 专门检查特定 context 的缺失。 | `paper_content.txt` §3.3 Objectives and research questions；§4.1；§4.2。 | 可迁移到 Paper2：RQ 不只问“有哪些论文”，还问“字段树是什么、字段间如何链接、缺失 context 是什么”。 | DevSecOps/GSE 的领域内容不可迁移为 Paper2 目标发现。 |
| Dimension pattern | 五大 aspect -> text segments/codes/themes -> OPC/PC/Technology/Business -> Gartner lifecycle -> CPTM。 | §4.1.1、§4.1.2、Tables 5--19、§4.1.3、Table 21、Figs. 5--9。 | 强可迁移：支持多层字段树、编号化主题、source type、frequency、category、stage、cross-link。 | 图表连线与 full CPTM 需 PDF / Zenodo 核对；不能把 CPTM 直接变成所有 SE SLR 的通用 schema。 |
| Finding pattern | 从统计与主题合成导出：实践最受关注、metrics 最薄弱、WL/GL 关注互补、Business challenges 在 WL 中存在、GL 中 business-related challenges = 0，business metric M20 来自 prior MLR 补入、GSE 维度缺失、近年研究转向 framework design。 | §4.1.4、§4.2.3、§4.3、§4.4。 | 可迁移为 Paper2 的 候选发现 heuristic：频次分布 + 来源差异 + 缺失关系 + confirmatory trend。 | 原文 finding 仍需研究者解释；负面 finding 受 search string 与时间窗口影响。 |
| Evidence presentation pattern | 使用 search execution 表、overlap 表、aspect-source 表、TA count 表、C/P/T/M 主题表、工具组表、metric mapping 表、生命周期映射表与开放材料。 | Tables 1--5、8--21；Data availability。 | 可迁移为“从检索分母到模型元素”的证据链模板；每个 field 应能回到 source ID / table / QA。 | 本轮未逐项核对所有 C/P/T/M 表格原始来源；正式引用需页码/表号核对。 |
| Validity / threat pattern | 明确报告 selection/QA/extraction bias、synthesis trustworthiness、search string 构造威胁；承认第一作者主导编码与既有框架先验影响。 | §3.8.3、§5.1--§5.3。 | 可迁移为 Paper2 的威胁模板：字段抽取偏差、模式先验污染、负面发现检索词敏感性、人工裁决主观性。 | Reflexive TA 的信度口径与 Paper2 若采用的 LLM/agent 抽取不同，不能照搬。 |
| Report structure pattern | Introduction -> key concepts / related work -> MLR method -> results/discussion by RQ -> implications -> threats -> conclusion -> open materials / appendix。 | 全文目录与章节结构。 | 可迁移为 secondary-study review 的报告骨架；尤其是 related work 对前序综述的比较和 RQ 对齐结果。 | Paper2 是方法论文，不应完全按 DevSecOps MLR 结果论文组织。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 / 启发 | 可审计字段建议 | 风险控制 |
|---|---|---|---|
| A1-M0 主题 / RQ / 范围 / 综述元模型 | 用“DevSecOps 当前状态 + global application”拆出主题、对象、context、关系和缺失检查。 | `topic_scope`、`object_of_review`、`context_dimension`、`rq_to_object_mapping`、`negative_context_probe`。 | 不把 DevSecOps 的主题范围误当 Paper2 pilot 范围；只迁移 RQ 结构。 |
| A1-M1 脚手架挖掘 / 种子探测 | 标题直接强调 primary dimensions；全文提供前序综述比较、五大方面、CPTM 和 GSE gap。 | `scaffold_source_type`、`predecessor_relation`、`candidate_dimension`、`candidate_link_model`、`candidate_gap_pattern`。 | 标注“脚手架样本”，不得支撑目标领域发现。 |
| A1-M2 维度模式准备 / 批准 | 维度不是平铺字段，而是 aspect -> theme -> category -> stage -> cross-link。 | `field_tree_version`、`field_level`、`value_space`、`missing_semantics`、`evidence_requirement`、`cross_link_type`。 | 需要研究者批准，不应自动把 C/P/T/M 固化为所有主题 schema。 |
| A1-M3 论文收集 / 概览 | 双轨检索、WL/GL 分流、Search String 1/2、QA 阈值、snowballing、confirmatory search 都可转为概览卡字段。 | `source_track`、`database`、`search_string_id`、`preselection_count`、`included_count`、`qa_score`、`confirmatory_only`。 | 主样本与 confirmatory 样本必须隔离，避免统计污染。 |
| A1-M4 字段级证据抽取 / 模式演化 | text segment -> code -> theme -> category -> model，是字段证据抽取链；source IDs 和 frequency 支撑回溯。 | `text_segment_anchor`、`code`、`theme`、`category`、`source_id`、`frequency`、`coder_note`、`model_mapping`。 | 本文许多表格来自 text extraction；正式复用需 PDF/Zenodo 核对。 |
| A1-M5 统计分析 | 使用分布、频次、source type 差异、overlap、metric mapping 产生统计观察。 | `analysis_dataset_version`、`count_by_source_type`、`frequency_by_theme`、`overlap_with_prior_review`、`cross_table`。 | 统计观察不能直接变最终发现；需要记录样本范围、年份截止和 QA 过滤。 |
| A1-M6 候选发现形成 | 由统计观察和模型缺口生成候选发现：metrics 薄弱、WL/GL 互补、GSE 缺失、framework-design 趋势。 | `候选发现（candidate_finding）`、`supporting_observation`、`counter_explanation`、`claim_strength`、`followup_validation`。 | 特别是 absence finding 要记录反向解释和检索词敏感性。 |

## 6. 对 Paper2 的启发与风险

### 6.1 主要启发

1. **维度模式要从“字段表”升级为“字段树 + 关系图”**：本文的五大 aspects、四类 category、C/P/T/M 编号、生命周期 stage、元素连线共同说明，综述 schema 应能表示层级、跨字段链接和缺失关系。
2. **多声部证据链必须显式区分 WL / GL**：WL 更偏 definitions/challenges/practices 的学术概念化；GL 更偏 tools/metrics/business 的实践线索。Paper2 如果处理灰色材料，需要记录 source_track、可信度和用途，不应把 GL 与 WL 无差别统计。
3. **主题抽取链应可审计**：text segment -> code -> theme -> category -> model 是 A1-M4 字段证据抽取的好模板；每个主题最好保留来源标识、频次和是否由前序综述验证。
4. **发现生成不等于频次统计**：本文从 frequency、source-type contrast、prior-review validation、lifecycle mapping 和 missing links 共同形成 finding；这适合 Paper2 的 A1-M5 -> A1-M6 候选发现规则。
5. **negative finding 需要竞争解释**：GSE 空白不是一句“没有文献”，而是 Search String 2、GL 搜索失败、少数边缘 WL、confirmatory search 和四种解释共同构成的弱/中等强度 gap。
6. **Open Science 是审计制品链样板**：protocol、QA score、raw text/codes、TA tables、full model 都发布到 Zenodo，并被 JSS Open Science Board 验证；这可作为 Paper2 透明材料设计的对照。
7. **reflexive TA 给人机协作一个方法学锚点**：如果 Paper2 后续使用 LLM/agent 做候选编码，不应只追求“自动一致性”，而要记录研究者主观判断、修订、协商、拒绝和回填。

### 6.2 主要风险

1. **领域迁移风险**：DevSecOps 的 C/P/T/M 结构非常适合安全运营主题，但不一定适合所有 SE SLR；Paper2 只能迁移元模式，不应迁移具体字段值。
2. **GL promotional bias**：原文也观察到 GL 往往呈现更积极的实践/工具叙事，business challenges 在 GL 中缺失；Paper2 若用 GL 需记录偏差。
3. **主样本与 confirmatory search 混用风险**：confirmatory search 只用于新近验证，不进入 TA/CPTM；Paper2 的统计表也必须区分正式样本、补充样本和验证样本。
4. **单一主编码者风险**：作者用 reflexive TA 合理化第一作者主导编码，但仍承认 synthesis threat；Paper2 若用 agent 抽取，更要保留人工裁决和反向证据检查。
5. **图表级细节风险**：CPTM full model 因版面限制在论文中拆成 Fig. 5--9，完整版本在 Zenodo；本轮只做全文文本级阅读，正式使用连线和 stage mapping 前要核对 PDF/Zenodo。
6. **时间窗口风险**：主 MLR 到 2021，confirmatory 到 2022，文章 2024 发表；若用于“当前 DevSecOps 现状”会过期，但用于 Paper2 schema pattern 仍有价值。
7. **absence finding 外推风险**：GSE 空白可能来自术语遗漏或产业非公开实践；Paper2 应把这类发现标为候选/有限强度，而非最终事实。

## 7. 待复核

- [ ] 如需正式引用 CPTM 连线，打开 [paper.pdf](./paper.pdf) 核对 Fig. 5--9 与 Table 21，并进一步核对 Zenodo full CPTM model。
- [ ] 打开 Zenodo <https://doi.org/10.5281/zenodo.7959584> 核验 protocol、QA score、raw text/codes、TA tables 是否与论文叙述一致。
- [ ] 复核 “摘要口径 104 WL + 43 GL；RQ1 主 TA 池 102 WL + 43 GL，RQ2 另 2 WL，confirmatory 13 WL + 7 GL 不进入 TA/CPTM” 的口径：正文 RQ1 为 102 WL + 43 GL，RQ2 另有 2 WL；摘要合并为 104 WL。
- [ ] 如后续把本文纳入 [patterns/pattern-field-schema.md](../../patterns/pattern-field-schema.md) 的正式字段来源，需要另开任务更新 schema / SUMMARY；本次按用户约束只编辑本 `review.md`。
- [ ] 若 Paper2 后续选择 DevSecOps / security-oriented SE 作为 pilot topic，需要重新检索 2022--2026 文献，不能用本文的 2012--2021 样本当作当前全貌。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/devsecops-primary-dimensions__codex.md](../../audits/a1dt-v2-19x3/results/devsecops-primary-dimensions__codex.md)、[../../audits/a1dt-v2-19x3/results/devsecops-primary-dimensions__claude.md](../../audits/a1dt-v2-19x3/results/devsecops-primary-dimensions__claude.md)、[../../audits/a1dt-v2-19x3/results/devsecops-primary-dimensions__deepseek.md](../../audits/a1dt-v2-19x3/results/devsecops-primary-dimensions__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/devsecops-primary-dimensions.md](../../audits/a1dt-v2-19x3/adjudications/devsecops-primary-dimensions.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `devsecops-primary-dimensions` |
| 审计代理 | `claude` (claude-opus-4-7[1m]) |
| 是否已读 `paper_content.txt` | 是；3158 行全文按顺序读毕（正文 1-2000 行密读，2000-2200 含 威胁/conclusion/data 可获得性 密读，2200-3158 为 appendix 论文清单与参考文献，按章节抽查覆盖） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两文件已完整读取并交叉核对 DOI / venue / 年份 / open access status |
| 是否打开或核对 `paper.pdf` | 否；本轮基于 `paper_content.txt` 文本审计，Fig. 5--9 (CPTM 拆分图) 与 Tables 6--21 的版面细节未做 PDF 视觉核验，留作 A2a |
| 原文类型 | Multivocal Literature Review (MLR) + Reflexive Thematic Analysis (TA)；属系统二级研究 |
| 被编码样本单位 | **两层**：(a) 原始研究（摘要口径 104 WL + 43 GL；RQ1 主 TA 池 102 WL + 43 GL，RQ2 另 2 WL，confirmatory 13 WL + 7 GL 不进入 TA/CPTM，2012--2021；另 20 confirmatory search 单独存放、不入 TA/CPTM）；(b) 每篇 原始研究 内部被抽取的细粒度 item：DevSecOps definitions (28+15)、挑战 (73+53)、practices (219+137)、指标 (7+13)、工具 (18+45)——这些 item 才是 主题分析 的真正编码单位 |
| 样本数量 / 分母 | 原始研究 分母 = 102 WL + 43 GL (RQ1) + 2 WL (RQ2) ≈ 147；text segment 分母随 aspect 不同：definitions 43、挑战 126、practices 356、指标 20、工具 63；最终模型项：28 挑战 (C01--C28)、60 practices (P01--P60)、20 指标 (M01--M20)、18 工具 groups (T01--T18) |
| 原生树类型 | **维度森林 + 显式关系边**（不是单棵树）：5 个 aspect 各为一棵子树，CPTM 关系图把 4 棵子树（Challenge/Practice/Tool/Metric）通过 Table 21 的多对多映射 + Gartner 10 阶段生命周期投影连接成一张图 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**实际读取**：
- `bibtex.bib`（12 行完整）：title / authors / DOI / journal / year 一致
- `metadata.json`（34 行完整）：oa_status=混合（混合）、systematic_evidence_status=multivocal_literature_review、eligible_for_statistical_synthesis=true
- `paper_content.txt`：按 Page 1--Page 26 顺序读毕主文 + Page 26--27 抽样核对 appendix；总计覆盖 §1 Intro、§2 Key concepts & related work（含 Table 1 review papers 对比、§2.2.2 global DevOps）、§3 全部研究方法（§3.1--§3.9，含 Fig 1 MLR 流程、§3.4 search strategy、§3.5 QA、§3.6 replication、§3.7 search execution Table 3、§3.8 TA + 模型 creation + trustworthiness）、§4 Results（§4.1 RQ1 全部子节含 Tables 4--21 与 Fig 4--9、§4.2 RQ2 三子节、§4.3 confirmatory、§4.4 implications）、§5 Threats、§6 Conclusion、数据可获得性（Data 可获得性）、Appendix A.1 sample
- `review.md`：477 行完整读取（含维度树复原；证据链已迁至 evidence_chain.md）

**纯文本审计的局限**：Fig 5--9 (CPTM 拆分图) 的具体连线、Fig 2 (QA form screenshot)、Tables 6/8--19 的某些跨页对齐细节未做 PDF 视觉核验；Zenodo 完整 CPTM 模型 未访问。

**关键证据锚点**（≤12）：

1. Page 1 摘要："five major aspects of DevSecOps (Definitions, Challenges, Practices, Tools/Technologies, and Metrics/Measurement); ... generates a Challenge-Practice-Tool-Metric (CPTM) 模型" — 锚定原生树有 5 个 aspect + CPTM 子图
2. Page 1 摘要 + §3.7：" white (104 studies) and grey (43 studies) literature from 2012 to 2021" — 锚定 primary-研究 分母；§4.1 与 §4.2 进一步分解为 102+2 WL
3. Page 3 Table 1："Aspects involved" 列对 7 个 先前综述（prior review） 给出维度对比 — 锚定 aspect 不是 reviewer 投影，而是原文对自己与他人 模式 的显式声明
4. Page 5 §3.3 RQ1/RQ2：Sub-questions 1.1/1.2/1.3 = "what aspects / what themes / how do they link" — 锚定 RQ 本身就要求树+关系，与 6 叶子 通用接口不同
5. Page 7 §3.8.2 Model creation："Cruzes and Dyba present four levels of interpretation in TA: Text, Code, Themes, and Model" + "first author... read text from many pages... identified specific segments... labeled into 代码... reduced overlaps... translated into themes... classified into 类别（类别）... created a conceptual 模型" — 锚定原生编码层级 = text segment → code → theme → category → 模型（即 lifecycle）
6. Page 10 Table 5："主题分析（主题分析） and synthesis results" 给出每个 aspect 的 text segment / code / theme / category 计数 — 锚定每个 aspect 子树的精确叶子层规模与取值空间
7. Page 10 §4.1.2 四个 category 定义："Organization, People and Culture (OPC)... 过程 Capabilities (PC)... 技术... 业务" — 锚定 category 取值空间是封闭 4 项枚举（指标 子树降为 3 项、工具 子树仅 技术 一项）
8. Page 11--18 Tables 6--19：每个 挑战 / practice / 指标 / 工具 的 ID (Cxx/Pxx/Mxx/Txx)、theme、频次、source-ID 列表 — 锚定 item-level 字段是完全封闭枚举且可统计
9. Page 19--22 Tables 20--21 + Fig 5--9：Gartner 10-阶段 定义 + "Identified themes mapped to steps" 把每个 C/P/T/M item 投影到 10 阶段 — 锚定 lifecycle-阶段 是封闭 10 项枚举，且 C-P-T-M 关系是多对多边
10. Page 18 Table 18："DevSecOps 指标 mapped to DevOps 指标" — 锚定 指标 子树有跨外部 分类法 映射字段
11. Page 23 §4.2.3：四种 GSE-absence 解释 + 检索词敏感性说明 — 锚定 负向发现（negative 发现） 的证据强度限定
12. Page 25 §5.1--§5.3：reflexive TA 主观性、search string 威胁、第一作者主导编码 — 锚定迁移边界与降级口径

---

`★ Insight ─────────────────────────────────────`
本审计的核心判定点：原文 Table 5 把 5 aspect × (text seg 计数 / code 计数 / theme 计数 / category set) 的封闭计数全部公开；Tables 6/8/9/10/11/12/13/14/15/16/17/19 又把 C01--C28 / P01--P60 / M01--M20 / T01--T18 的每一项与其 theme、频次、贡献论文 ID 全部列出；Table 21 + Fig 5--9 进一步给出 C→P→T→M 的多对多关系边并按 10 个 Gartner 阶段 切片。这是教科书级"系统样本编码模式"，而非 路线图/愿景。现 `review.md` 把这种封闭枚举式 模式 标为 `模式种子（schema_seed） / not_verified` 与文本证据严重不符，是审计第一返修点。
`─────────────────────────────────────────────────`

### 2. 样本单位与字段来源判定

1. **原文逐项描述对象**：两层并存。**外层** = 原始研究（每篇 WL/GL 有 ID 形如 S1-IEEE-08、S1-GL-13、CS-ACM-01；分母 102+43+2+20）。**内层 (真正编码单位)** = 从 原始研究 中抽取的 text segments，再经 code → theme → category 抽象为 28 挑战 / 60 practices / 20 指标 / 18 工具 groups。模型 (CPTM) 把 C/P/T/M 四类 item 作为节点 + 关系边 + Gartner 阶段 投影。
2. **系统性程度**：完全系统化。§3.4 search strategy + §3.5 inclusion/exclusion + QA form (14 yes/no + 1 Literature Type 0--4，总分 18，阈值 11) + §3.6 replication + §3.7 search execution Table 3 + §3.8 reflexive TA + §3.8.3 trustworthiness (credibility/confirmability/dependability/transferability) + Zenodo open material。
3. **字段来源**：
   - 抽取表 = adapted 数据抽取 form (Kitchenham 2007) + Garousi MLR 指南 改造的 QA form (Fig 2)
   - 分类方案（classification scheme；首次术语） = TA 归纳得到的 21+23+56+16+16 主题 + 演绎得到的 4 category (OPC/PC/技术/业务) + Gartner 10 阶段 外部框架
   - relations = §4.1.3 由 first author 经多轮（2021-2023）模型迭代生成的 Table 21 + Fig 5--9
   - Zenodo 复现包：MLR protocol、included papers 含 QA score、raw text/代码、TA tables (initial + final)、CPTM 完整 模型
4. **RQ 与样本单位关系**：RQ1 = "what aspects / themes / links" → 对应 5 aspect → theme → category → CPTM 关系图四级树；RQ2 = "DevSecOps in GSE contexts" → 把 GSE/global/distributed 作为另一切片维度，用 Search String 2 验证缺失。RQ 与树根、字段用途、结果组织方式三种关系**全部存在**。
5. **降级问题**：不需要降级。本文具备完整系统检索 + 编码方案 + 关系模型 + open replication，是 A2a 主统计池候选；当前 review.md 的 模式种子（schema_seed） 降级是过度保守。

### 3. 原生样本编码维度树 / 维度森林

本文为**显式维度森林**：5 棵子树并列，外加 1 张关系图把其中 4 棵编织成 CPTM 模型。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] DevSecOps 当前状态（当前状态, RQ1）+ 全球采用（全球采用, RQ2）
│
├── A. DevSecOps 定义 子树（28 白色文献（WL）+ 15 条灰色文献（GL）抽取片段 → 74 代码→ 21 主题 → 4 类别（类别））
│   ├── 文本片段 (自由文本，含相似与重复)
│   ├── 代码（74 项；命名后的概念短语)
│   ├── 主题（21 项；如“Dev/Sec/Ops 协作”、“左移（shift-left）”、“共享责任（shared responsibility）”）
│   ├── 类别 取值 ∈ {组织、人员与文化（OPC）, 过程能力（PC）, 技术, 业务（业务）}（封闭 4 枚举）
│   ├── 来源轨道 取值 ∈ {WL, GL}
│   ├── 来源编号 (Paper ID 列表；如 S1-IEEE-08, S1-GL-15)
│   ├── 频次 (主题 内 代码 计数；Table 6 每行括号数字)
│   └── 常用定义作者 + 引用次数（常用定义作者 + 引用次数）（Table 7；如 Mohan&Othmane=9）
│
├── B. DevSecOps 挑战 子树（73 WL + 53 GL → 85 代码→ 23 主题 → 28 最终条目（最终条目） → 4 类别（类别））
│   ├── 挑战编号 (C01..C28；封闭枚举)
│   ├── 挑战主题 (与 挑战编号 一对一)
│   ├── 类别 取值 ∈ {OPC(9), PC(8), 技术(7), 业务(4)}
│   ├── 频次 (Tables 8--11 每行 (Freq) 字段)
│   ├── 来源轨道 + 来源编号 列表
│   ├── 与先前综述匹配状态（与先前综述匹配状态） 取值 ∈ {是（yes，带星号）、部分（partly）、否（no）、仅从先前综述补入}
│   └── 补入来源标识（例如 Myrbakken 与 Colomo-Palacios 的 MLR 补入 C09、C19、C23、C27–C28）
│
├── C. DevSecOps 实践 子树（219 WL + 137 GL → 142 代码→ 56 主题 → 60 最终条目（最终条目） → 4 类别（类别））
│   ├── 实践编号 (P01..P60)
│   ├── 实践主题 (与 id 一对一)
│   ├── 类别 取值 ∈ {OPC(15), PC(17), 技术(23), 业务(5)}
│   ├── 频次
│   ├── 来源轨道 + 来源编号 列表
│   └── 与先前综述匹配状态（与先前综述匹配状态） + 补入来源（例如 P14–P15 来自 Sánchez-Gordón SLR；P31–P32、P55 来自 Rajapakse SLR）
│
├── D. DevSecOps 工具 / 技术 子树（18 WL + 45 GL → 56 代码→ 16 主题 → 18 最终分组（最终分组） → 1 类别）
│   ├── 工具组编号 (T01..T18)
│   ├── 功能组 (主题；如 "自动化工具（Automation 工具）", "容器安全工具（Container security 工具）", "静态应用安全测试工具（SAST 工具）")
│   ├── 工具名称 (具体工具列表，如 Docker, Kubernetes, Snyk, Snyk 等)
│   ├── 类别 = 技术（单值枚举）
│   ├── 来源轨道 + 来源编号
│   └── 补入来源 (T16-T18 来自 Mohan&Othmane mapping）
│
├── E. DevSecOps 指标 / 度量 子树（7 WL + 13 GL → 20 代码→ 16 主题 → 20 最终条目（最终条目） → 3 类别（类别））
│   ├── 指标编号 (M01..M20)
│   ├── 指标名称 + 测量方法 + 目标（每个 指标 在 Tables 16-17 有 Measuring/Goal 双字段）
│   ├── 类别 取值 ∈ {组织、人员与文化（OPC）, 过程能力（PC）, 技术, 业务（业务）}（业务 仅 M20）
│   ├── 频次 + 来源轨道 + 来源编号
│   ├── 补入来源（M07–M08、M19 来自 Prates 的 MLR；M20 来自 Myrbakken 的 MLR）
│   └── 映射到 DevOps 指标 (Table 18；13/20 与 Amaro 2023 DevOps 指标 一对多映射)
│
├── F. CPTM 关系图（Table 21 + Fig 5--9；连接 B/C/D/E 四棵子树）
│   ├── 生命周期阶段（生命周期阶段） 取值 ∈ {计划（Plan）, 创建（Create）, 验证（Verify）, 预生产（Preproduction）, 发布（Release）, 预防（Prevent）, 检测（Detect）, 响应（Respond）, 预测（Predict）, 适应（Adapt）}（封闭 10，Gartner）
│   ├── 关系边：挑战 → 实践（Challenge → Practice） （多对多；Table 21 每个 阶段 下 C-P 配对）
│   ├── 关系边：实践（Practice）→ 工具（Tool）（多对多；可缺，记为不适用（NA））
│   ├── 关系边：实践（Practice）→ 指标（Metric）（多对多；可缺，记为不适用（NA））
│   └── 颜色类别叠加层（颜色类别叠加层） 取值 ∈ {OPC=黄色, PC=蓝色, 技术=绿色, 业务=红色}
│
└── G. RQ2 GSE 上下文探测（Context Probe）子树（独立维度，不属于 5 个方面）
    ├── 检索式变体（检索式变体） 取值 ∈ {检索式 1, 检索式 2 含 GSE/GSD/全球（global）/ 分布式（distributed）/ 多站点（multi-site）/ 多国家（multi-nation）/ 跨国（transnational）/ 远程工作（remote-work）}
    ├── 结果计数（result_count）；WL: 126 → 66 → 2 纳入；GL: 100 浏览 → 0）
    ├── 正向命中（正向命中）；仅 S2-ACM-04 Gupta 2019、S2-ACM-05 Viggiato 2019）
    ├── 替代解释（替代解释） (4 项封闭枚举：无显著相关（no significant correlation） / 安全集中化（security centralized） / 真实研究空白（true research gap） / 术语漏检（terminology missed）)
    └── 结论强度（结论强度）= "负向发现（negative 发现），弱到中等强度（weak-to-medium）"
```

**核心主干 + 代表性叶子覆盖率**：上述 5 子树 + CPTM + GSE probe 已覆盖原文 Tables 4--21 与 Figs 4--9 的全部主干；本轮缺：(a) Table 2 的 "overlapping percentage" 子字段（仅 prior-review 验证用）；(b) Fig 3 的 published year 分布字段 (year-by-source-type) ——这两项为辅助统计字段，可在 A2a 补入。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-aspect | DevSecOps aspect | ROOT | §4.1.1 | 5 大主题划分 | {Definitions, Challenges, Practices, Tools/Technologies, Metrics/Measurement} | 完整枚举 (5) | 不允许缺 | 频次分布 (Fig 4) | aspect 失衡 发现 | Page 1 摘要, §4.1.1, Table 4 | 模式可迁移，5 项内容仅限本文 |
| L-category | High-order category | aspect 下所有 item | §4.1.2 | 主题归类 | {组织、人员与文化（OPC）, 过程能力（PC）, 技术, 业务（业务）} | 完整枚举 (4)；指标 子树降为 3；工具 子树仅 技术 | NA 仅出现在 指标-业务 (本文 included studies 中 0 项，补入 M20 后才填) | category 分布 | category 失衡、业务 在 WL 缺失 发现 | §4.1.2, Tables 6/8--19 | 4-cat 划分在 DevSecOps 之外不通用 |
| L-text-segment | text segment | 每个 item | §3.8.1 + Tables 6/8--19 中 "Codes [Papers..]" 列 | 编码前的原文片段 | 自由文本+原始 Paper ID 注引 | 自由文本+source list | 不允许缺；至少 1 段 | text-segment 总频次 (Fig 4) | aspect-WL/GL 不平衡 | §3.8.1 | 仅本文 |
| L-code | code | text-segment 之上 | §3.8.2 + Tables 6/8--19 列 | text-segment 抽象短语 | 自由文本但已规范化 | 自由文本 (149 个 code 跨 aspect) | 不允许缺 | code 计数 Table 5 | -- | Page 7 §3.8.2 | -- |
| L-theme | theme | code 之上 | Tables 6/8--19 行 | code 聚合形成的稳定主题 | 跨 5 aspect 共 132 themes (Table 5 求和) | 层级枚举 (21+23+56+16+16) | 不允许缺 | theme 频次 | 主题分布失衡 | Table 5 | -- |
| L-挑战-id | Challenge ID | Challenges 子树 | Tables 8--11 | 最终挑战编号 | C01..C28 | 完整枚举 (28) | NA | 9/8/7/4 跨 category 排序 | OPC>PC>Tech>Biz 排序 发现 (§4.1.2 B) | Tables 8/9/10/11 | 编号语义仅限本文 |
| L-practice-id | Practice ID | Practices 子树 | Tables 12--15 | 最终实践编号 | P01..P60 | 完整枚举 (60) | NA | 技术(23)>PC(17)>OPC(15)>Biz(5) | 技术-heavy + Biz 仅 GL | Tables 12--15 | -- |
| L-指标-id | Metric ID | Metrics 子树 | Tables 16--17 | 最终度量编号 | M01..M20 | 完整枚举 (20) | NA | 指标 最少 + cross-source | 指标 coverage 缺口（gap） | Tables 16--17 | -- |
| L-工具-group-id | Tool Group ID | Tools 子树 | Table 19 | 工具功能簇编号 | T01..T18 | 完整枚举 (18) | NA | container/automation 居首 | -- | Table 19 | -- |
| L-频次 | text-segment 频次 | item 上 | Tables 6/8--19 各行 (Freq) | item 在 included studies 中累计提及次数 | 自然数 (1..93)；最大 P33 automation=93 | 数值 (含 0) | 0 表示纯从 先前综述（prior review） 补入 (如 C09) | 主题热度排序 | top-3 挑战 / practice / 指标 | Tables 6/8--19 | -- |
| L-source-track | 来源轨道 | 每个 text segment / code | Tables 4--19 | 该证据来自 WL 还是 GL | {WL, GL} | 完整枚举 (2) | 不允许缺；prior-review 补入标 [Reference's review] | WL/GL 互补统计 | "业务 仅在 GL"、"academia vs industry 互补" 发现 | §4.1.1 Fig 4 + Tables 4--19 | -- |
| L-source-id | source ID | code 列 | Tables 6/8--19 [...] | 具体 原始研究 编号 | S1-ACM-NN, S1-IEEE-NN, S1-SC-NN, S1-GL-NN, CS-ACM-NN, ... | 完整枚举但开放尾部 (148 项) | 不允许缺；纯 prior-review 补入标 Reference 名 | source 多样性 | 高被引 source (e.g. S1-IEEE-08) | Appendix A.1-A.3 | -- |
| L-matched-prior | matched 先前综述（prior review） | 每个 final item | Tables 8--19 星号注释 | 与 Mohan2016, Myrbakken2017, Prates2019, SanchezGordon2020, Akbar2022, Rajapakse2022 的重叠 | {*=部分或全部匹配, 未标=本文新增, 仅 [Reference's review]=纯补入} | 三态枚举 | 未标=本文独有 | overlap 验证 | "all 挑战 match 先前综述（prior review）" (§4.1.2 B 结尾) | §3.6, §4.1.2 + Tables 8--19 | -- |
| L-supplemented-from | 补入来源 | Tables 中显式标注 | §4.1.2 各段 | 由哪个 prior 二次研究 补入 | {本文独有, Mohan&Othmane 2016, Myrbakken&Colomo-Palacios 2017, Prates 2019, Sanchez-Gordon 2020, Rajapakse 2022, Akbar 2022, 无更新} | 完整枚举 (7+1) | 不允许缺 | 补入比例 | "C09/C19/C23/C27-28 etc 5 挑战 from Myrbakken" | §4.1.2 段落叙述 + Tables 中 [Reference's review] | -- |
| L-lifecycle-阶段 | Gartner 生命周期阶段 | CPTM 关系图 | Table 20 + Table 21 + Figs 5--9 | C/P/T/M item 在 DevSecOps lifecycle 中的位置 | {计划（Plan）, 创建（Create）, 验证（Verify）, 预生产（Preproduction）, 发布（Release）, 预防（Prevent）, 检测（Detect）, 响应（Respond）, 预测（Predict）, 适应（Adapt）} | 完整枚举 (10) | item 可出现在多个 阶段 (e.g. C01 同时在 Plan 和 Adapt) | 阶段-density / category-by-阶段 投影 | "OPC+PC 集中 Plan/Create" + "Tech 集中 Verify..Predict" + "业务 在 Release" | Tables 20-21, Figs 5--9 | Gartner 10 阶段 来自外部框架 |
| L-关系边-CP | Challenge→Practice 边 | CPTM | Table 21 | 解决 挑战 的 practice 集合 | 取值是 P-id 列表 (含 不适用（NA)) | 关系值 | NA=未对应 practice | 边度分布 | C 无 P 是 缺口（gap） | Table 21 | -- |
| L-关系边-PT | Practice→Tool 边 | CPTM | Table 21 | 实施 practice 的 工具 集合 | T-id 列表+NA | 关系值 | NA 极常见 (例 §4.1.3 "not each practice has its corresponding 工具") | 工具-coverage | "指标/工具 缺口本身是 发现" (§4.1.3 page 19) | Table 21 | -- |
| L-关系边-PM | Practice→Metric 边 | CPTM | Table 21 | 度量 practice 的 指标 集合 | M-id 列表+NA | 关系值 | NA 多 | 指标 coverage | 指标 是最薄弱 aspect | Table 21 | -- |
| L-指标-mapping | DevSecOps 指标 ↔ DevOps 指标 | Metrics 子树 | Table 18 | 与 Amaro 2023 DevOps 指标 的对应 | M-id ↔ Me-id 多对多 (Table 18 列出 10 个 Me 与 13 个 M) | 关系值+外部 分类法 | NA=本 DevSecOps 指标 无 DevOps 对应 | 重合率 | "≈half DevOps 指标 security-related" | Table 18 §4.1.2 D | -- |
| L-common-def-author | 常用定义作者 | Definitions 子树 | Table 7 | 被引最多的 DevSecOps 定义作者 | 自由文本+引用次数 | 自由文本+数值 | -- | -- | "Mohan&Othmane=9 most cited" | Table 7 | -- |
| L-qa-score | 质量评价 score | each included 原始研究 | §3.5 + Fig 2 + Zenodo | 14 yes/no(0-1) + 1 type(0-4)，阈值 11/18 | 整数 0..18 | 数值 | <11 = 不纳入 | QA 分布 (Zenodo) | -- | Fig 2 + Zenodo | QA form 改自 Garousi+Kitchenham |
| L-search-string-id | search string identifier | RQ-level | §3.4.2 | 主检索式 | {String 1 (RQ1), String 2 (RQ2 含 GSE 词簇), variants} | 离散+变体 | -- | search-execution Table 3 | "String 2 多次微调仍 negative" | §3.4.2, Table 3 | -- |
| L-confirmatory-flag | confirmatory only | included paper | §3.7 + Fig 3 + Appendix A.3 | 是否仅来自 2022 confirmatory search (不进 TA/CPTM) | 布尔 | 布尔 | -- | 必须区分 | 防止 staleness 污染主 发现 | §3.7 段末 | -- |
| L-gse-result-计数 | GSE-context positive hit 计数 | RQ2 | §4.2.1--§4.2.3 | Search String 2 经各阶段筛后的命中数 | 自然数 (126 → 66 → 2 WL; 100 browsed → 0 GL) | 数值链条 | 0 是合法值 | absence 发现 依据 | "absence of global dimension" | §4.2 | -- |
| L-gse-explanation | absence 解释候选 | RQ2 | §4.2.3 | 4 项竞争解释 | {无显著相关（no significant correlation）, 安全集中化（security centralized）, 真实研究空白（true research gap）, 术语漏检（terminology missed）} | 完整枚举 (4) | 不允许缺 | -- | 防止把 absence 升级为强结论 | §4.2.3 | -- |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E-text-code | L-text-segment | 抽象为 | L-code | 自由文本 | 不允许缺 | §3.8.2 | TA 第 2 层 |
| E-code-theme | L-code | 聚合为 | L-theme | theme 编号 | 不允许缺 | §3.8.2 | TA 第 3 层 |
| E-theme-cat | L-theme | 归入 | L-category | {OPC,PC,Tech,Biz} | 不允许缺 (除 工具 仅 技术) | §4.1.2 | TA 第 3-4 层 |
| E-cat-模型 | L-category | 映射至 | L-lifecycle-阶段 | Gartner 10 | 多对多 | §3.8.2 + Tables 20-21 | TA 第 4 层 |
| E-挑战-practice | L-挑战-id | addressed-by | L-practice-id | P-id 列表 | 不适用（NA）合法 | Table 21 | CPTM 主关系 |
| E-practice-工具 | L-practice-id | implemented-with | L-工具-group-id | T-id 列表 | NA 频繁 | Table 21 | CPTM 关系 |
| E-practice-指标 | L-practice-id | measured-by | L-指标-id | M-id 列表 | NA 频繁 | Table 21 | CPTM 关系 |
| E-item-阶段 | C/P/T/M-id | located-at | L-lifecycle-阶段 | Gartner 10；可多对多 | 不适用（NA）合法 (e.g. M-only 出现在 Plan/Predict) | Table 21 + Figs 5--9 | lifecycle 投影 |
| E-指标-devops | L-指标-id | maps-to | external Me-id (Amaro 2023) | Me01..Me19 | 不适用（NA）合法 (7/20 DevSecOps 指标 未映射) | Table 18 | 外部 分类法 跨表映射 |
| E-item-prior | C/P/T/M-id | overlaps-with | L-matched-prior + L-supplemented-from | 先前综述（prior review） 名集合 | unmatched 合法 | Tables 8--19 星号 + 段落叙述 | replication 验证 |
| E-prior-review-overlap | this MLR's WL set | overlaps-with | each prior 二次研究's WL set | overlapping percentage 0--100% | -- | Table 2 | prior-review 验证 |

### 6. 统计观察、候选发现 与 最终发现边界

**统计观察（由字段表支撑）**：
- 5 aspect 在 text-segment 层频次：Practices 最高，Metrics 最低 (Fig 4)
- WL/GL 分布：WL 偏 definitions/挑战/practices；GL 偏 工具/指标/业务 (Fig 4, Tables 6--17)
- 挑战 category 排序：OPC(9)>PC(8)>Tech(7)>Biz(4)
- practice category 排序：Tech(23)>PC(17)>OPC(15)>Biz(5)
- 指标 category 分布：Biz 仅 1 项 (M20) 且补入
- GL 中 business-related challenges = 0；business metric M20 来自 prior MLR 补入
- Table 2 prior-review overlap %：从 40% (Mohan2016) 到 100% (Myrbakken2017)
- 13/20 DevSecOps 指标 与 Amaro 2023 DevOps 指标 重合 (≈65%)
- RQ2 GSE 命中：126→66→2 WL；100 GL browsed→0
- Mohan&Othmane 定义被引 9 次居首 (Table 7)

**候选发现 (作者 discussion / 路线图)**：
- "指标 是最薄弱 aspect，学界与产业未达成 consensus"
- "业务 视角主要来自 GL，WL 在该 category 缺位"
- "OPC + PC 挑战/practices 集中 Plan/Create → shift-left 哲学的实证支撑"
- "技术 挑战/practices 集中 Verify/Prevent/Detect/Respond/Predict → 工具与运行时为主"
- "Global DevSecOps 是 absence 发现 (4 项竞争解释)"
- "confirmatory search 显示 WL 转向 框架 design (7/13 新 paper)；GL routine 化"
- "DevSecOps → Platform Engineering 可能是下一阶段研究方向" (Puppet 2023 引用)

**对 Paper2 可迁移方法学启发**：
- 维度森林 + 关系图 (CPTM) 取代平铺 模式
- WL/GL 双轨 + 主样本 / confirmatory 隔离 + prior-review 作 验证
- text→code→theme→category→模型 5 层抽取链
- absence 发现 必须配竞争解释 + 检索词敏感性记录
- reflexive TA 给 LLM/智能体 抽取的人机协作锚点

**绝不能迁移的领域结论**：
- 28 个 挑战 / 60 practice / 20 指标 的具体内容
- Gartner 10-阶段 不一定适合非 DevSecOps 主题
- "指标 薄弱"、"业务 仅在 GL" 等领域统计结论受 2012--2021 时间窗口限制

## survey_of_surveys 自身 schema 抽取

本节把该论文投影到本目录自己的脚手架综述 schema（S1--S8）。判定等级只说明该维度在原文和本地证据链中的可用程度：`强` = 有明确原文结构和证据锚点；`中` = 有可复用结构但存在范围、裁决或精核限制；`弱` = 只作边界启发或风险提示；`不适用` = 原文类型不支持该维度进入统计池。

| 维度 | 判定等级 | 一句话抽取结果 | 证据位置 |
|---|---|---|---|
| S1 综述任务设定 | 强 | 本文明确设定为 DevSecOps 的多声部文献综述，RQ1 抽取 aspects/themes/links，RQ2 检查 GSE context 中的应用空白。 | `review.md` §2.1、§2.3；`evidence_chain.md` A.2 `ev-devsecops-primary-dimensions-type` |
| S2 语料收集与筛选 | 强 | 采用 white literature + grey literature 双轨检索、两套 search string、纳排、QA 和 snowballing；confirmatory search 只作新近验证，不进入 TA/CPTM 主统计语料。 | `review.md` §2.4；`evidence_chain.md` A.2 `ev-devsecops-primary-dimensions-unit`、`ev-devsecops-primary-dimensions-denom` |
| S3 原生维度树/样本编码对象 | 强 | 原生结构是 5 个 aspect 构成的维度森林，并以 text segment/code/theme/category 到 CPTM 节点与关系边为编码对象。 | `review.md` 维度树复原 §0、§2；`evidence_chain.md` A.3 `clm-devsecops-primary-dimensions-unit`、`clm-devsecops-primary-dimensions-tree` |
| S4 字段级证据 | 强 | 字段级证据覆盖 definitions、challenges、practices、metrics、tools 的 text segment/code/theme/category 计数、ID、频次、source-ID 与关系映射；CPTM 关系边与 Zenodo full model 待 A2a 精核。 | `review.md` §2.6、§2.7、维度树复原关键证据锚点；`evidence_chain.md` A.2 `ev-devsecops-primary-dimensions-denom`、`ev-devsecops-primary-dimensions-tree` |
| S5 维度模式演化 | 强 | 明确呈现从 inductive thematic analysis 的 text → code → theme → category 到 lifecycle/CPTM model 的模式演化，并区分 WL 归纳与 GL 演绎分析。 | `review.md` §2.5、§2.7、§3；`evidence_chain.md` A.3 `clm-devsecops-primary-dimensions-tree` |
| S6 统计分析 | 强 | 提供各 aspect 的主样本分母、text segment/code/theme/category 数量、C/P/T/M 项数、频次和 WL/GL 差异；confirmatory search 仅作验证性补充。 | `review.md` §2.6、§3、维度树复原 §0；`evidence_chain.md` A.2 `ev-devsecops-primary-dimensions-denom` |
| S7 候选 finding | 强 | 候选发现包括实践最受关注、metrics 最薄弱、WL/GL 互补、Business challenges 在 WL 中存在、GL 中 business-related challenges = 0，business metric M20 来自 prior MLR 补入、GSE 缺失和 framework design 趋势；其中 confirmatory finding 单独降级。 | `review.md` §2.8、§3、§6；`evidence_chain.md` A.3 `clm-devsecops-primary-dimensions-pool` |
| S8 研究者/作者质疑与裁决 | 中 | 原文没有独立质疑-裁决流程，但有 reflexive thematic analysis 的多作者审核协商、trustworthiness 讨论、threats 与开放材料审计。 | `review.md` §2.5、§2.9；`evidence_chain.md` A.2 `ev-devsecops-primary-dimensions-type` |

### S1--S8 四分栏证据拆分

#### 总体统计池裁决

本文是 A2a 主统计池候选 / A1 阶段仅作模式种子。理由：原文具备系统 MLR、WL/GL 双轨检索、QA、TA 编码链、CPTM 关系模型与开放材料；但当前审计仍未逐项核验 PDF 表图页码、Fig. 5--9 连线、Table 21 全关系边与 Zenodo full CPTM。因此可进入后续精核队列，不应在 A2a 前进入最终定量统计或支撑 Paper2 目标领域最终 finding。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文明确为 DevSecOps MLR；RQ1 问 aspects / themes / links，RQ2 问 GSE contexts。 | 根节点可复原为“DevSecOps 当前状态 + 全球采用探测”，下接 RQ1 维度森林与 RQ2 context probe。 | 候选可用：任务设定清晰，可统计为“现状 + 维度 + 关系 + 缺失探测”型综述。 | 核对 PDF 中 §3.3 RQ 原文页码；确认 RQ2 是否只作 gap probe，不并入五大 aspect。 |
| S2 语料收集与筛选 | 原文报告 WL 104、GL 43；RQ1 主池为 102 WL + 43 GL，RQ2 另 2 WL；confirmatory 13 WL + 7 GL 不进 TA/CPTM。 | 样本单位需拆两层：外层 primary studies，内层 text segments / codes / themes / model items。 | 候选可用但需分母隔离：主 MLR、RQ2、confirmatory 必须分开统计。 | 精核 Table 3、Fig. 3、Appendix A.1--A.3；统一 104/102+2/147/20 confirmatory 口径。 |
| S3 原生维度树/样本编码对象 | 摘要与 §4.1 明确五大 aspects；§3.8.2 明确 Text → Code → Themes → Model。 | 复原为 5 棵 aspect 子树：Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement；C/P/T/M 再接 CPTM 关系图。 | 强候选：有原生树和编码对象，不是 reviewer 后验投影。 | 核验 Table 5 的 text segment / code / theme / category 计数；确认 definitions 是否不进入 CPTM。 |
| S4 字段级证据 | Tables 5--19 给出 aspect、code、theme、category、ID、频次、source IDs；Table 21 给 C/P/T/M 映射。 | 叶子字段可复原为 aspect、category、text segment、code、theme、C/P/M/T ID、frequency、source track、source ID、prior-review match、lifecycle stage、关系边。 | 候选可用但暂不最终入池：字段丰富，可统计；但关系边需版面/补充材料精核。 | 打开 PDF 核 Tables 6--21 跨页对齐；核 Zenodo raw text/codes、TA tables、full CPTM。 |
| S5 维度模式演化 | 原文说明 WL 先归纳编码，GL 主要基于 WL codes/themes 演绎分析，再映射 Gartner lifecycle 形成 CPTM。 | 模式演化链为 inductive WL → deductive GL → category → lifecycle projection → CPTM model。 | 候选可用：可统计为“归纳-演绎混合模式演化”。 | 核 §3.8.2 对 WL/GL 分工和 Gartner lifecycle 的表述；核 Fig. 5 模型生成链。 |
| S6 统计分析 | 原文提供 aspect 分布、WL/GL 差异、C/P/T/M 项数、频次、category 排序、RQ2 命中链。 | 可复原统计层：aspect 频次、category 分布、source-track 差异、prior-review overlap、CPTM edge coverage、GSE absence count。 | 候选可用但需限制：只统计原文内部样本，不外推为当前 DevSecOps 全貌。 | 精核 Fig. 4、Table 2、Tables 8--21；确认 confirmatory search 不混入主统计。 |
| S7 候选 finding | 原文讨论 practices 最多、metrics 最薄弱、WL/GL 互补、GSE 缺失、framework design 趋势等。 | finding 应挂接到统计观察、CPTM 缺口、RQ2 absence probe 与 confirmatory-only 标志。 | 中等候选：可作为作者候选发现池；不能直接作为 Paper2 目标领域最终 finding。 | 对每条 finding 标注主样本 / confirmatory / prior-review 补入；尤其核 GSE negative finding 的竞争解释。 |
| S8 研究者/作者质疑与裁决 | 原文没有独立“质疑-裁决”机制；但有 reflexive TA、多作者 weekly/bi-weekly 协商、trustworthiness、threats、open material。 | 可复原为“研究者协商与信度控制”节点，而不是正式 adversarial adjudication 节点。 | 仅弱/中候选：可统计为 trustworthiness / author-consensus evidence，不宜计为完整裁决流程。 | 核 §3.8.2、§3.8.3、§5.1--§5.3；确认是否存在 Zenodo 中额外 reviewer/coder decision log。 |

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
