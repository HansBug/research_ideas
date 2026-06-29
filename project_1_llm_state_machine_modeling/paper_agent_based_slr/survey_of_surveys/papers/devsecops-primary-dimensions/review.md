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
| 样本规模 | 主 MLR：white literature 104 篇、grey literature 43 篇，时间范围 2012--2021；另有 2022 年前后的 confirmatory search 13 篇 WL + 7 篇 GL，但未进入 TA 与最终 CPTM 模型 |
| 核心方法 | white/grey 双轨检索；Search String 1 处理 DevSecOps 全局现状，Search String 2 加入 GSE/global/distributed 词簇；质量评价；snowballing；reflexive thematic analysis；生命周期框架映射 |
| 核心产物 | 五大方面；OPC / PC / Technology / Business 四类高阶主题；C/P/T/M 编号化主题；Gartner 十阶段生命周期；Challenge-Practice-Tool-Metric, CPTM 模型 |
| Open Science | 论文声明 JSS Open Science Board 已验证开放材料；Zenodo 入口包含 protocol、included papers + QA score、raw text/codes、thematic synthesis、TA tables、full CPTM model |
| 对 Paper2 的一句话价值 | 这篇文献是“维度树 + 多声部证据链 + 主题到模型”的强样本：可把 Paper2 的维度模式从平铺字段推进到“字段树、证据来源、质量门槛、跨字段 link、生命周期投影、发现缺口”的可审计结构。 |
| 是否目标证据池 | 否；只作为 survey-of-surveys 脚手架和维度模式先验，不支撑 Paper2 目标领域最终 finding。 |

## 2. 全文内容详读

### 2.1 背景 / 问题设定

论文从 DevOps 中安全需求被低估这一问题切入：安全常被视为降低交付速度的阻碍，而云、容器、serverless、多云、SaaS、快速交付和全球分布式系统又让安全前置更加必要。DevSecOps 被定义为 DevOps 的安全导向扩展，核心目标是在不显著牺牲速度与质量的前提下，把安全实践整合进 development、operations、security 团队协作过程，并通过 shift-left 和 continuous security 降低后期修复成本。

这篇文献的第二条问题线是 GSE。作者认为 DevOps/DevSecOps 与 GSE 都属于 collaborative software engineering，均依赖 communication、coordination、cooperation；因此，如果 DevSecOps 要在全球分布式环境中落地，就应当能观察到 GSE 维度。但全文最后的关键负面发现恰恰是：现有 white 和 grey literature 几乎没有真正覆盖 Global DevSecOps。

### 2.2 与既有 DevSecOps review 的关系

原文系统比较了 Mohan and Othmane 2016 mapping study、Myrbakken and Colomo-Palacios 2017 MLR、Prates et al. 2019 MLR、Sanchez-Gordon and Colomo-Palacios 2020 SLR、Mao et al. 2020 GLR、Akbar et al. 2022 MLR + survey、Rajapakse et al. 2022 SLR + TA 等相关综述。作者对自身工作的定位不是“最早综述”，而是：

1. 用更完整的 white + grey 双轨来源覆盖 DevSecOps 第一个十年。
2. 不只停留在 challenge / practice / tool 等单一方面，而是把 aspects、themes 和 links 一起建模。
3. 使用 Thematic Analysis 的四级抽象：text -> code -> theme -> model；并强调既有相近综述多停在 theme 层。
4. 显式检查 DevSecOps 在 GSE 场景中的研究空白。
5. 通过 confirmatory search 与既有二级研究交叉验证，而不是把旧综述直接纳入主样本。

对 Paper2 来说，这种“前序综述关系”很重要：单篇 review 不应只记录本研究做了什么，还应记录它如何复现、验证、扩展、整合或区别于已有 secondary studies。

### 2.3 RQ1 / RQ2

原文两个研究问题非常适合作为 Paper2 的 RQ pattern 先验：

| RQ | 内容 | 可迁移模式 |
|---|---|---|
| RQ1 | DevSecOps 在现有 white + grey literature 中的当前状态是什么，包括涉及哪些 aspects、每个 aspect 有哪些 themes、这些 aspects/themes 如何互相链接？ | “现状 + 维度 + 主题 + 关系”的复合型 RQ；不仅统计类别，还要求建立 link/model。 |
| RQ1.1 | 现有文献中可以发现哪些 DevSecOps aspects？ | primary dimension discovery。 |
| RQ1.2 | 这些 aspects 包含哪些 themes？ | aspect 内部主题抽取与分类。 |
| RQ1.3 | 识别出的 aspects 和 themes 如何互相链接？ | 从 taxonomy 走向 model / cross-field relation。 |
| RQ2 | DevSecOps 如何在 GSE contexts 中被采用？ | 用目标领域维度检查特定 context 是否缺失，形成 negative finding / research gap。 |

### 2.4 White + grey literature 与 dual-track search

论文采用 MLR 而非普通 SLR，理由是 DevSecOps 属于实践快速演化主题，很多经验先出现在技术报告、网站、博客、厂商材料等 grey literature 中。其检索设计具有可迁移价值：

1. **White literature 来源**：ACM Digital Library、IEEE Xplore、Scopus。ScienceDirect 和 Springer 没作为主检索库，但用于 snowballing 与 confirmatory search。
2. **Grey literature 来源**：Google；作者浏览 Search String 1 的前 18 页结果，因为第 19 页后相关性显著变弱；Search String 2 的 GL 搜索浏览前 10 页且未发现同时覆盖 GSE、DevOps、security 的材料。
3. **Search String 1**：围绕 `devops` 与 `security/secure/safe`，并加入 `secdevops` / `devsecops`。作者解释了为何把 `safe` 纳入：安全与安全性在若干语境中有交叉，且 security flaws 可能 compromise safety。
4. **Search String 2**：在 String 1 基础上加入 GSE/GSD/global/distributed/multi-site/multi-nation/transnational/remote work 等词簇，用于捕捉 RQ2。
5. **时间范围**：2012--2021；DevSecOps 概念早期出现于 2012 附近，实际最早相关论文约 2013。
6. **纳排与 QA**：纳入条件要求涉及 DevSecOps primary aspects、英文、2012 年后、方法/研究设计清楚、来源可信；排除无全文、领域外、方法不严谨、重复、secondary studies 等。QA 表包含 14 个 yes/no 问题加 literature type 0--4 分，总分 18，阈值 11。
7. **Snowballing / replication**：secondary studies 不进主 MLR，但被用来验证 overlap 和补充 findings；这相当于把前序综述作为“验证源”而非“主证据源”。
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
| Definitions | 28 WL + 15 GL definitions；74 codes；21 themes；4 categories | 定义不仅是句子，还可拆成 collaboration、shared responsibility、shift-left、automation、quality/business 等 theme；Mohan and Othmane 2016 的定义最常被引用。 | `definition_source`、`definition_text_segment`、`definition_code`、`definition_theme`、`definition_category`、`common_definition_author`、`citation_frequency`。 |
| Challenges | 73 WL + 53 GL challenges；85 codes；23 themes；最终 28 challenges | OPC 挑战最多；collaboration/communication/coordination、security skill/training、security integration without losing speed、cloud/serverless complications、mature tools 缺失是高频问题。 | `challenge_id`、`challenge_theme`、`challenge_category`、`frequency`、`source_type`、`matched_previous_review`、`linked_practice`。 |
| Practices | 219 WL + 137 GL practices；142 codes；56 themes；最终 60 practices | Technology practices 最多；automation 是最强 theme；shift-left 是 PC 核心实践；business practices 主要来自 GL。 | `practice_id`、`practice_theme`、`practice_category`、`addresses_challenge`、`source_type`、`linked_tool`、`linked_metric`。 |
| Metrics / Measurement | 7 WL + 13 GL metrics；20 codes；16 themes；最终 20 metrics | 度量是最薄弱方面；WL 很少，GL 提供更多；可映射到若干 DevOps metrics。 | `metric_id`、`metric_name`、`measuring_method`、`goal`、`category`、`mapped_devops_metric`、`linked_practice`。 |
| Tools / Technologies | 18 WL + 45 GL tools；56 tool codes；16 themes，补充后 18 tool groups | Docker/Kubernetes 等 container tools、Chef/Jenkins/Puppet 等 automation platform、SAST/DAST/IAST/SCA、vulnerability management tools 等成为功能组。 | `tool_id`、`tool_name`、`tool_function_group`、`source_type`、`linked_practice`、`lifecycle_stage`。 |

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
5. 并不是所有 practice 都有对应 tool / metric，这个缺口本身是 finding：字段树必须允许 `not reported` / `no linked metric` / `no linked tool`。

对 Paper2 来说，CPTM 是非常强的“维度模式不应平铺”的例子：一个可用的综述 schema 应支持实体、属性、证据、阶段、关系、缺失和模型投影。

### 2.8 RQ2：GSE 空白

RQ2 得到的是典型 negative finding。Search String 1 没找到 DevSecOps + GSE 相关文献；Search String 2 加入 GSE/global/distributed 词后，最终只有 2 篇 WL 同时涉及 GSE、DevOps 和 security，但它们也不是完整 Global DevSecOps 研究；GL 方向浏览前 10 页没有找到同时覆盖三者的材料。

作者给出四种解释可能：

1. GSE 与 DevSecOps 之间可能没有显著差异性关系。
2. 安全可能在组织中偏集中和控制导向，因此 global aspects 不突出。
3. 这是一个真实 research gap。
4. 也可能是 search string 漏掉了特定术语，尽管作者已多次调整词串。

这对 Paper2 的启发是：absence/gap 类发现必须保留检索式、变体、失败路径和解释竞争项，不能把“没搜到”直接升级为强结论。

### 2.9 Quality / validity / trustworthiness

原文报告的质量与效度处理有三层：

1. **主样本质量评价**：QA 表总分 18、阈值 11；QA score 随开放材料发布。
2. **TA trustworthiness**：按 credibility、confirmability、dependability、transferability 组织；credibility 依赖 primary study quality 与合适 text segments；confirmability 依赖多作者讨论与资深作者审核；dependability 通过与其他 SLR/MLR 比较验证；transferability 计划通过后续 Delphi study 验证。
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
| Finding pattern | 从统计与主题合成导出：实践最受关注、metrics 最薄弱、WL/GL 关注互补、Business 在 WL 中弱、GSE 维度缺失、近年研究转向 framework design。 | §4.1.4、§4.2.3、§4.3、§4.4。 | 可迁移为 Paper2 的 candidate finding heuristic：频次分布 + 来源差异 + 缺失关系 + confirmatory trend。 | 原文 finding 仍需研究者解释；负面 finding 受 search string 与时间窗口影响。 |
| Evidence presentation pattern | 使用 search execution 表、overlap 表、aspect-source 表、TA count 表、C/P/T/M 主题表、工具组表、metric mapping 表、生命周期映射表与开放材料。 | Tables 1--5、8--21；Data availability。 | 可迁移为“从检索分母到模型元素”的证据链模板；每个 field 应能回到 source ID / table / QA。 | 本轮未逐项核对所有 C/P/T/M 表格原始来源；正式引用需页码/表号核对。 |
| Validity / threat pattern | 明确报告 selection/QA/extraction bias、synthesis trustworthiness、search string 构造威胁；承认第一作者主导编码与既有框架先验影响。 | §3.8.3、§5.1--§5.3。 | 可迁移为 Paper2 的威胁模板：字段抽取偏差、模式先验污染、负面发现检索词敏感性、人工裁决主观性。 | Reflexive TA 的信度口径与 Paper2 若采用的 LLM/agent 抽取不同，不能照搬。 |
| Report structure pattern | Introduction -> key concepts / related work -> MLR method -> results/discussion by RQ -> implications -> threats -> conclusion -> open materials / appendix。 | 全文目录与章节结构。 | 可迁移为 secondary-study review 的报告骨架；尤其是 related work 对前序综述的比较和 RQ 对齐结果。 | Paper2 是方法论文，不应完全按 DevSecOps MLR 结果论文组织。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 / 启发 | 可审计字段建议 | 风险控制 |
|---|---|---|---|
| A1-M0 主题 / RQ / 范围 / 综述元模型 | 用“DevSecOps current state + global application”拆出主题、对象、context、关系和缺失检查。 | `topic_scope`、`object_of_review`、`context_dimension`、`rq_to_object_mapping`、`negative_context_probe`。 | 不把 DevSecOps 的主题范围误当 Paper2 pilot 范围；只迁移 RQ 结构。 |
| A1-M1 脚手架挖掘 / 种子探测 | 标题直接强调 primary dimensions；全文提供前序综述比较、五大方面、CPTM 和 GSE gap。 | `scaffold_source_type`、`predecessor_relation`、`candidate_dimension`、`candidate_link_model`、`candidate_gap_pattern`。 | 标注“脚手架样本”，不得支撑目标领域发现。 |
| A1-M2 维度模式准备 / 批准 | 维度不是平铺字段，而是 aspect -> theme -> category -> stage -> cross-link。 | `field_tree_version`、`field_level`、`value_space`、`missing_semantics`、`evidence_requirement`、`cross_link_type`。 | 需要研究者批准，不应自动把 C/P/T/M 固化为所有主题 schema。 |
| A1-M3 论文收集 / 概览 | 双轨检索、WL/GL 分流、Search String 1/2、QA 阈值、snowballing、confirmatory search 都可转为概览卡字段。 | `source_track`、`database`、`search_string_id`、`preselection_count`、`included_count`、`qa_score`、`confirmatory_only`。 | 主样本与 confirmatory 样本必须隔离，避免统计污染。 |
| A1-M4 字段级证据抽取 / 模式演化 | text segment -> code -> theme -> category -> model，是字段证据抽取链；source IDs 和 frequency 支撑回溯。 | `text_segment_anchor`、`code`、`theme`、`category`、`source_id`、`frequency`、`coder_note`、`model_mapping`。 | 本文许多表格来自 text extraction；正式复用需 PDF/Zenodo 核对。 |
| A1-M5 统计分析 | 使用分布、频次、source type 差异、overlap、metric mapping 产生统计观察。 | `analysis_dataset_version`、`count_by_source_type`、`frequency_by_theme`、`overlap_with_prior_review`、`cross_table`。 | 统计观察不能直接变最终发现；需要记录样本范围、年份截止和 QA 过滤。 |
| A1-M6 候选发现形成 | 由统计观察和模型缺口生成候选发现：metrics 薄弱、WL/GL 互补、GSE 缺失、framework-design 趋势。 | `candidate_finding`、`supporting_observation`、`counter_explanation`、`claim_strength`、`followup_validation`。 | 特别是 absence finding 要记录反向解释和检索词敏感性。 |

## 5. 可迁移字段树草案

下面是从本文抽取出的可迁移字段树。它适合进入 Paper2 的 schema 候选池，但需要后续研究者裁决后才能成为正式 A1-M2 维度模式。

```text
ReviewRecord
├── BibliographicMeta
│   ├── title / authors / year / venue / DOI
│   ├── publication_type / venue_short_link / CCF_category / CCF_rank
│   └── open_science_material_status
├── ReviewProtocol
│   ├── review_type = MLR / SLR / SMS / tertiary / guideline / other
│   ├── objectives
│   ├── research_questions
│   │   ├── rq_id
│   │   ├── rq_scope = current_state / dimension_discovery / link_model / context_gap
│   │   └── sub_questions
│   ├── search_strategy
│   │   ├── source_track = WL / GL / confirmatory
│   │   ├── database_or_engine
│   │   ├── search_string_id / search_string_text
│   │   ├── time_window
│   │   ├── preselection_count / selected_count / included_count
│   │   └── snowballing_role
│   ├── selection_and_quality
│   │   ├── inclusion_criteria / exclusion_criteria
│   │   ├── quality_assessment_form
│   │   ├── quality_threshold
│   │   └── qa_score_available
│   └── synthesis_method
│       ├── synthesis_type = thematic_analysis / mapping / narrative / mixed
│       ├── stance = positivist / interpretive / pragmatic / reflexive
│       ├── coder_process
│       └── trustworthiness_measures
├── PrimaryDimensionTree
│   ├── Definition
│   │   ├── text_segment
│   │   ├── code
│   │   ├── theme
│   │   ├── category = OPC / PC / Technology / Business
│   │   ├── source_track = WL / GL
│   │   ├── source_id
│   │   ├── frequency
│   │   └── common_definition_author / cited_definition_source
│   ├── Challenge
│   │   ├── challenge_id = Cxx
│   │   ├── challenge_theme
│   │   ├── category = OPC / PC / Technology / Business
│   │   ├── frequency
│   │   ├── source_track / source_id
│   │   ├── matched_prior_review = yes / partly / no
│   │   ├── lifecycle_stage
│   │   └── linked_practice_ids
│   ├── Practice
│   │   ├── practice_id = Pxx
│   │   ├── practice_theme
│   │   ├── category
│   │   ├── frequency
│   │   ├── source_track / source_id
│   │   ├── addresses_challenge_ids
│   │   ├── linked_tool_ids
│   │   ├── linked_metric_ids
│   │   └── lifecycle_stage
│   ├── ToolOrTechnology
│   │   ├── tool_group_id = Txx
│   │   ├── function_group
│   │   ├── tool_names
│   │   ├── source_track / source_id
│   │   ├── linked_practice_ids
│   │   └── lifecycle_stage
│   ├── MetricOrMeasurement
│   │   ├── metric_id = Mxx
│   │   ├── metric_name
│   │   ├── measuring_method
│   │   ├── measurement_goal
│   │   ├── category
│   │   ├── source_track / source_id
│   │   ├── mapped_external_metric
│   │   ├── linked_practice_ids
│   │   └── lifecycle_stage
│   └── ContextGap
│       ├── context_name = GSE / distributed / global / domain-specific
│       ├── search_string_variants
│       ├── positive_hits
│       ├── negative_result
│       ├── alternative_explanations
│       └── claim_strength
├── EvidencePresentation
│   ├── search_execution_table
│   ├── included_study_list
│   ├── overlap_with_prior_reviews
│   ├── thematic_count_table
│   ├── source_track_comparison
│   ├── lifecycle_mapping_table
│   └── open_artifact_links
└── ValidityAndRisk
    ├── selection_bias
    ├── data_extraction_bias
    ├── synthesis_subjectivity
    ├── search_string_threat
    ├── staleness / confirmatory_status
    └── transferability_limit
```

## 6. 对 Paper2 的启发与风险

### 6.1 主要启发

1. **维度模式要从“字段表”升级为“字段树 + 关系图”**：本文的五大 aspects、四类 category、C/P/T/M 编号、生命周期 stage、元素连线共同说明，综述 schema 应能表示层级、跨字段链接和缺失关系。
2. **多声部证据链必须显式区分 WL / GL**：WL 更偏 definitions/challenges/practices 的学术概念化；GL 更偏 tools/metrics/business 的实践线索。Paper2 如果处理灰色材料，需要记录 source_track、可信度和用途，不应把 GL 与 WL 无差别统计。
3. **主题抽取链应可审计**：text segment -> code -> theme -> category -> model 是 A1-M4 字段证据抽取的好模板；每个主题最好保留来源 ID、频次和是否由前序综述验证。
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
- [ ] 复核 “104 WL + 43 GL” 的口径：正文 RQ1 为 102 WL + 43 GL，RQ2 另有 2 WL；摘要合并为 104 WL。
- [ ] 如后续把本文纳入 [patterns/pattern-field-schema.md](../../patterns/pattern-field-schema.md) 的正式字段来源，需要另开任务更新 schema / SUMMARY；本次按用户约束只编辑本 `review.md`。
- [ ] 若 Paper2 后续选择 DevSecOps / security-oriented SE 作为 pilot topic，需要重新检索 2022--2026 文献，不能用本文的 2012--2021 样本当作当前全貌。

## 维度树复原

### 一句话结论

本文的维度树主类型为“关系型维度树”，辅助类型为“多声部证据树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-devsecops-primary-dimensions-tree-type]

旧有“可迁移字段树 / 字段树 / schema 缺口”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-devsecops-primary-dimensions-root] | Identifying the primary dimensions of DevSecOps 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-devsecops-primary-dimensions-b1] DevSecOps aspect；[dim-devsecops-primary-dimensions-b2] theme / category；[dim-devsecops-primary-dimensions-b3] CPTM item；[dim-devsecops-primary-dimensions-b4] lifecycle stage；[dim-devsecops-primary-dimensions-b5] GSE context gap | [ev-devsecops-primary-dimensions-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-devsecops-primary-dimensions-root] Identifying the primary dimensions of DevSecOps
├── [dim-devsecops-primary-dimensions-b1] DevSecOps aspect
│   └── [leaf-devsecops-primary-dimensions-scope] 研究范围与单位对象
├── [dim-devsecops-primary-dimensions-b2] theme / category
│   └── [leaf-devsecops-primary-dimensions-corpus] 语料与纳排链条
├── [dim-devsecops-primary-dimensions-b3] CPTM item
│   └── [leaf-devsecops-primary-dimensions-taxonomy] 主题与维度分类
├── [dim-devsecops-primary-dimensions-b4] lifecycle stage
│   └── [leaf-devsecops-primary-dimensions-method] 方法 / 技术 / 干预分类
└── [dim-devsecops-primary-dimensions-b5] GSE context gap
    └── [leaf-devsecops-primary-dimensions-evidence] 评价、证据与复现资产
    └── [leaf-devsecops-primary-dimensions-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-devsecops-primary-dimensions-scope] | 研究范围与单位对象 | [dim-devsecops-primary-dimensions-b1] | 定义 DevSecOps dimensions 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-devsecops-primary-dimensions-leaf-scope] |
| [leaf-devsecops-primary-dimensions-corpus] | 语料与纳排链条 | [dim-devsecops-primary-dimensions-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-devsecops-primary-dimensions-leaf-corpus] |
| [leaf-devsecops-primary-dimensions-taxonomy] | 主题与维度分类 | [dim-devsecops-primary-dimensions-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-devsecops-primary-dimensions-leaf-taxonomy] |
| [leaf-devsecops-primary-dimensions-method] | 方法 / 技术 / 干预分类 | [dim-devsecops-primary-dimensions-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-devsecops-primary-dimensions-leaf-method] |
| [leaf-devsecops-primary-dimensions-evidence] | 评价、证据与复现资产 | [dim-devsecops-primary-dimensions-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-devsecops-primary-dimensions-leaf-evidence] |
| [leaf-devsecops-primary-dimensions-finding] | 统计观察与候选发现 | [dim-devsecops-primary-dimensions-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-devsecops-primary-dimensions-leaf-finding] |

### 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据引用 | 结论引用 |
|---|---|---|---|---|---|---|---|
| [edge-devsecops-primary-dimensions-method-evidence] | [leaf-devsecops-primary-dimensions-method] | 支撑 / 度量 | [leaf-devsecops-primary-dimensions-evidence] | 工具 / 指标 / 数据集 / artifact / not_reported | 未报告评价或复现资产时写 `not_reported` | [ev-devsecops-primary-dimensions-taxonomy] | [clm-devsecops-primary-dimensions-edge-method-evidence] |
| [edge-devsecops-primary-dimensions-taxonomy-finding] | [leaf-devsecops-primary-dimensions-taxonomy] | 导出候选发现 | [leaf-devsecops-primary-dimensions-finding] | gap / recommendation / trend / limitation | 无 discussion 支撑时写 `not_reported` | [ev-devsecops-primary-dimensions-stat] | [clm-devsecops-primary-dimensions-edge-taxonomy-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-devsecops-primary-dimensions-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 是 | 识别可迁移的维度模式类型 | 可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 |
| [leaf-devsecops-primary-dimensions-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 是 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-devsecops-primary-dimensions-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-devsecops-primary-dimensions-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | DevSecOps dimensions 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-devsecops-primary-dimensions-transfer] |
| [leaf-devsecops-primary-dimensions-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-devsecops-primary-dimensions-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-devsecops-primary-dimensions-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-devsecops-primary-dimensions-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-devsecops-primary-dimensions-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-devsecops-primary-dimensions-001 | [ev-devsecops-primary-dimensions-root] | [src-devsecops-primary-dimensions-text], [src-devsecops-primary-dimensions-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | strong | [dim-devsecops-primary-dimensions-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-devsecops-primary-dimensions-002 | [ev-devsecops-primary-dimensions-taxonomy] | [src-devsecops-primary-dimensions-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度。 | taxonomy | medium | [dim-devsecops-primary-dimensions-b1], [dim-devsecops-primary-dimensions-b2], [dim-devsecops-primary-dimensions-b3], [dim-devsecops-primary-dimensions-b4], [dim-devsecops-primary-dimensions-b5], [leaf-devsecops-primary-dimensions-taxonomy], [leaf-devsecops-primary-dimensions-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-devsecops-primary-dimensions-003 | [ev-devsecops-primary-dimensions-stat] | [src-devsecops-primary-dimensions-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | statistical_result | medium | [leaf-devsecops-primary-dimensions-evidence], [leaf-devsecops-primary-dimensions-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-devsecops-primary-dimensions-004 | [ev-devsecops-primary-dimensions-risk] | [src-devsecops-primary-dimensions-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | medium | [dim-devsecops-primary-dimensions-root], [leaf-devsecops-primary-dimensions-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |
| EV-devsecops-primary-dimensions-005 | [ev-devsecops-primary-dimensions-relation] | [src-devsecops-primary-dimensions-text] | paper_content.txt | 结果 / 讨论相关页；待 A2a 精确页码复核 | 关系 / 交叉表 / discussion 邻近段落 | 关系型表或交叉统计 | -- | 见释义 | 原文将分类字段与评价、工具、指标、artifact 或 discussion finding 连接，本记录用于支撑关系边。 | taxonomy | medium | [edge-devsecops-primary-dimensions-method-evidence], [edge-devsecops-primary-dimensions-taxonomy-finding] | true | false | -- | 关系边只表示本文中的字段联系，不能外推为目标领域因果关系。 |

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-devsecops-primary-dimensions-tree-type] | A1DT-devsecops-primary-dimensions-C01 | 本文的维度树主类型为“关系型维度树”，辅助类型为“多声部证据树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-devsecops-primary-dimensions-tree-type] | tree_type | [dim-devsecops-primary-dimensions-root] | EV-devsecops-primary-dimensions-001, EV-devsecops-primary-dimensions-004 | 树型判断仅限本文，不代表所有 DevSecOps dimensions 综述。 | strong | statistical_synthesis | false | -- |
| [clm-devsecops-primary-dimensions-leaf-scope] | A1DT-devsecops-primary-dimensions-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-devsecops-primary-dimensions-scope] | EV-devsecops-primary-dimensions-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-devsecops-primary-dimensions-leaf-corpus] | A1DT-devsecops-primary-dimensions-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-devsecops-primary-dimensions-corpus] | EV-devsecops-primary-dimensions-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-devsecops-primary-dimensions-leaf-taxonomy] | A1DT-devsecops-primary-dimensions-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-devsecops-primary-dimensions-taxonomy] | EV-devsecops-primary-dimensions-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-devsecops-primary-dimensions-leaf-method] | A1DT-devsecops-primary-dimensions-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-devsecops-primary-dimensions-method] | EV-devsecops-primary-dimensions-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-devsecops-primary-dimensions-leaf-evidence] | A1DT-devsecops-primary-dimensions-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-devsecops-primary-dimensions-evidence] | EV-devsecops-primary-dimensions-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-devsecops-primary-dimensions-leaf-finding] | A1DT-devsecops-primary-dimensions-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-devsecops-primary-dimensions-finding] | EV-devsecops-primary-dimensions-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-devsecops-primary-dimensions-transfer] | A1DT-devsecops-primary-dimensions-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-devsecops-primary-dimensions-root] | EV-devsecops-primary-dimensions-002, EV-devsecops-primary-dimensions-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | medium | schema_seed | false | -- |
| [clm-devsecops-primary-dimensions-finding-boundary] | A1DT-devsecops-primary-dimensions-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-devsecops-primary-dimensions-finding] | EV-devsecops-primary-dimensions-003, EV-devsecops-primary-dimensions-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | medium | candidate_finding | false | -- |
| [clm-devsecops-primary-dimensions-edge-method-evidence] | A1DT-devsecops-primary-dimensions-C10 | 方法 / 技术节点与评价 / 证据节点之间存在可审计关系，适合作为 Paper2 字段间关系的 schema seed。 | relation_edge | [edge-devsecops-primary-dimensions-method-evidence] | EV-devsecops-primary-dimensions-005 | 关系含义限于本文分类和统计表，不代表因果关系。 | medium | schema_seed | false | -- |
| [clm-devsecops-primary-dimensions-edge-taxonomy-finding] | A1DT-devsecops-primary-dimensions-C11 | 主题 / 分类节点可通过统计观察或 discussion 支撑候选发现，但不能绕过研究者裁决。 | relation_edge | [edge-devsecops-primary-dimensions-taxonomy-finding] | EV-devsecops-primary-dimensions-005 | 候选发现仍需反证、scope 与 claim strength 审核。 | medium | candidate_finding | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-devsecops-primary-dimensions-structure-check] | [dim-devsecops-primary-dimensions-root], A1DT-devsecops-primary-dimensions-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-devsecops-primary-dimensions-visual-check] | EV-devsecops-primary-dimensions-002, EV-devsecops-primary-dimensions-003, EV-devsecops-primary-dimensions-005 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
