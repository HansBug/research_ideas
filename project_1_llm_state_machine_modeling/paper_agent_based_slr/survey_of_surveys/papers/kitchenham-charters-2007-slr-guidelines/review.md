# Guidelines for performing Systematic Literature Reviews in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Guidelines for performing Systematic Literature Reviews in Software Engineering |
| 年份 | 2007 |
| 类型 | 方法学 guideline / SLR 指南 |
| 出版形态 | 技术报告 |
| 期刊/会议/预印本 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| CCF 复核状态 | 非 CCF venue；技术报告 |
| 来源等级 | 方法学基准；非 CCF 论文；技术报告 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | SLR guideline；同时定义 系统映射研究 与 tertiary review |
| SE 子领域 | 软件工程证据综合方法学 |
| A1 角色 | 提供 PR-A1 的基础术语、流程阶段、研究问题、protocol、搜索、选择、质量评价、数据抽取、数据综合与报告结构先验。 |
| Paper2 目标领域证据池 | 否；不支撑 Paper2 目标领域 final finding。 |
| survey_of_surveys 方法参考池 | 是；作为 guideline / 方法学参考样本，不进入普通主统计池。 |
| schema 历史观察 | 暴露“guideline 类文献没有普通研究结果 RQ 表”的差异；已在 schema 中使用 `综述 / 指南类型` 与 `不适用` 缺失值语义处理。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 研究问题是 SLR 最重要的 protocol 元素；可按 population/intervention/comparison/outcome/context 等结构化。 | `paper_content.txt` Page 2--3 目录列出 §5.3 Research Questions；Page 12 附近说明 protocol 应包含 research questions。 | 可迁移到 Paper2 的“研究者定义综述元模型”和维度模式初始化。 | 这是 guideline，不代表任一 SE 子领域的真实 RQ 分布。 |
| dimension pattern | SLR protocol 至少需要 review need、research questions、search strategy、study selection、quality assessment、data extraction、data synthesis、reporting。 | `paper_content.txt` Page 2--3 目录列出 §5--§7；Page 30 附近讨论 data extraction forms。 | 可作为 `pattern-field-schema.md` 的阶段字段候选。 | 只能作为流程字段先验，不能直接冻结目标主题字段树。 |
| finding pattern | guideline 本身不生成领域 finding；它提供流程规范与质量判据。 | `paper_content.txt` Page 2--3 目录；Page 40 附近 reporting/evaluating review reports。 | 对 Paper2 的 finding 启发式不可直接采信，只能迁移报告与评价结构。 | guideline 不产生领域 finding，只迁移 finding 报告约束。 |
| evidence presentation pattern | 强调 documenting search、selection criteria、quality checklists、data extraction forms、synthesis 和 reporting。 | `paper_content.txt` Page 2--3 目录；Page 16 附近 documenting search；Page 29--34 data extraction。 | 高度可迁移到审计制品链。 | 规范建议需由后续真实论文样本验证。 |
| validity / threat pattern | 明确讨论 inclusion decision reliability、publication bias、quality assessment、sensitivity analysis。 | `paper_content.txt` Page 2--3 目录；Page 20 reliability；Page 38--39 sensitivity/publication bias。 | 可迁移为后续 A5 风险指标。 | 可迁移为风险清单，但具体权重需按 pilot 数据校准。 |
| report structure pattern | reporting review 部分要求 dissemination strategy、main report formatting、review report evaluation。 | `paper_content.txt` Page 3 目录 §7。 | 可迁移为 Paper2 输出材料结构。 | 报告建议偏 guideline，不等同于 paper2 最终论文结构。 |

## 3. 对 PR-A1 schema 的启发

1. `综述 / 指南类型` 必须允许 `guideline`，否则该文无法自然归类。
2. `finding pattern` 对 guideline 可能为“不适用”，不能误记为缺失或低质量。
3. `evidence presentation pattern` 应覆盖 protocol、表单、checklist 和报告结构，而不仅是论文结果表。
4. 后续 A2a 若纳入更多 guideline，需要单独区分“规范性文献”和“经验性 tertiary study”。

## 4. 待复核

- PDF 表格和 checklists 尚未逐页人工核对。
- 技术报告不是 peer-reviewed venue，正式引用时需说明来源性质。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 用 review need、research question、population/intervention/outcome/context 等要素定义系统综述协议。 | 可作为元模型初始化规范；不能直接代表任一 SE 子领域的主题结构。 |
| A1-M1 语料收集与纳排 | 提供 search strategy、study selection、quality assessment 和 data extraction 的流程字段。 | 可作为检索/纳排台账字段模板；具体数据库和检索式需由目标主题重建。 |
| A1-M2 研究对象与主题语义 | 仅提供通用 PICO / scope 组织方式，不提供具体 SE 子领域 taxonomy。 | 可候选，不作为已采纳领域语义字段。 |
| A1-M3 方法 / 技术 / 干预 | 指南强调 intervention / comparison 等变量，但不是技术综述样本。 | 对方法分类只提供形式约束，不提供具体取值空间。 |
| A1-M4 评价、证据与复现资产 | 强调质量评价、数据抽取表、搜索记录、报告结构和 sensitivity analysis。 | 可迁移到 Paper2 的 evidence anchor / run record / extraction-form 要求。 |
| A1-M5 统计分析就绪 | 说明 data synthesis 可叙述、定量或混合，并要求记录分母与合成方式。 | 可作为统计分析协议的最低规则，不提供现代字段树。 |
| A1-M6 research finding 形成与裁决 | guideline 本身不生成领域 finding，只提供报告和评价约束。 | 只作为 finding 报告规范；不进入目标领域 finding。 |

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__codex.md](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__codex.md)、[../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__claude.md](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__claude.md)、[../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__deepseek.md](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md](../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `kitchenham-charters-2007-slr-guidelines` |
| 审计代理 | `claude`（Claude Opus 4.7 1M context；非 claude -p 独立进程，详见第 9 节风险登记） |
| 是否已读 `paper_content.txt` | 是；已逐段阅读 §0-§9、Appendix 1-3，覆盖 Tables 1-9、Figures 1-2、Maxwell 1998 抽取实例 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是 |
| 是否打开或核对 `paper.pdf` | 否（仅通过 `paper_content.txt` 进行版面/页码核验，未单独 OCR / 视觉核对 PDF；详见 §1） |
| 原文类型 | **指南**（EBSE Technical Report；EBSE-2007-01；同时在文中定义了 SLR / 系统映射研究 / Tertiary Review 三种综述类型，并在 Appendix 3 内嵌一个 tertiary 研究 的 protocol） |
| 被编码样本单位 | **主体不编码样本**；指南 文本以"流程阶段 / 协议字段 / 表单字段 / 偏倚类型 / 质量条目 / 综合方法 / 报告章节"为描述对象（模式 而非 sample）；**仅 Appendix 2 例外**，对 2004-2007 年间 15 篇 SE SLR 进行了真实编码 |
| 样本数量 / 分母 | 主体：`不适用（不适用）`（指南 无系统样本库）；Appendix 2：**n = 15**（DARE 评分 ≥ 2 的 SE SLR） |
| 原生树类型 | **维度森林**（multi-模式：question / PICOC / protocol / search-doc / bias / 质量-instrument / 抽取-form / synthesis / sensitivity / 报告-structure 等并列），叠加一个小型 Appendix 2 编码池 |
| 主统计池资格 | 否；不进入后续主统计池。A1-DT v2 仅允许其作为方法学种子、模式种子或边界锚点；若原文内部存在 convenience sample / guideline 示例统计，也不得混入 Paper2 主统计池。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**实际读取**：

- `bibtex.bib`、`metadata.json`
- `paper_content.txt`：逐段读完目录（§0.1）→ Executive Summary / Glossary（§0.4-0.5，pp.vi-vii）→ §2 SLR/SMS/Tertiary 定义 → §3 Table 1 SE vs other disciplines → §4 三阶段流程 → §5 计划（Planning）（含 §5.3.1 6 类 question types + §5.3.2 PICOC）→ §6.1 Search（Table 2 search 文档）→ §6.2 Selection（含 §6.2.3 Cohen κ）→ §6.3 Quality（Tables 3-6：bias 4 类 + 量化检查表 ~50 项 + 质性检查表 18 项）→ §6.4 数据抽取（数据抽取）（Table 7 实例：Maxwell 1998）→ §6.5 Synthesis（5 binary + 3 continuous effect measures、森林图、funnel plot、3 类 定性 synthesis）→ §6.5.6 sensitivity 4 类 subset → §7 报告（Reporting）（Table 8 报告结构）→ §8 Mapping Studies → §9 PhD-light version → Appendix 1（Table 9 跨 6 源 流程 steps）→ Appendix 2（15 SE SLR 编码表）→ Appendix 3 tertiary protocol

**版面核验**：仅基于 `paper_content.txt` 的 `--- Page N ---` 分页标记定位页码；`paper.pdf` 未单独打开做视觉核验，Tables 2/5/7/8/9 的精确表格版式、Figures 1-2（森林图 / funnel plot）的图示边界、Appendix 2 跨页表格的行数完整性仍需 A2a 精核。

**关键证据锚点（10 条）**：

| # | 内容 | 文件 / 页 / 区位 |
|---|---|---|
| E1 | "Specifying the research questions is the most important part of any 系统综述" | `paper_content.txt` Page 17, §5.3 (line 707-715) |
| E2 | 6 类 question types（adapted from Australian NHMR）+ SE 改写 | Page 17-18, §5.3.1 (line 719-734) |
| E3 | PICOC = Population / Intervention / Comparison / Outcome / Context（Petticrew & Roberts） | Page 18-20, §5.3.2 (line 797-863) |
| E4 | Protocol 10 components 列表 | Page 20-21, §5.4 (line 893-922) |
| E5 | Table 2 Search 流程 文档（4 类 source × ~3-4 fields） | Page 24, §6.1.4 (line 1068-1086) |
| E6 | Table 4 Types of Bias（4 类 × {synonyms, definition, protection}） | Page 30, §6.3.2 (line 1390-1426) |
| E7 | Table 5 Quality Checklist（量化研究，~50 条 × {Empirical, Correlation, 调查, 实验} × Source；分 设计/Conduct/Analysis/Conclusions 4 阶段） | Page 33-35, §6.3.2 (line 1514-1620) |
| E8 | Table 6 质性研究质量 checklist（18 条 × source） | Page 36, §6.3.2 (line 1626-1658) |
| E9 | Table 7 数据抽取表实例（Maxwell 1998；~30 fields incl. data extractor/checker, 研究 identifier, application domain, 数据集 stats, cross-company 模型, within-company 模型, comparison, data summary） | Page 38-40, §6.4.2 (line 1751-1968) |
| E10 | Effect measures：5 binary（Odds/Risk/OR/RR/ARR）+ 3 continuous（Mean difference/WMD/SMD） | Page 43-44, §6.5.2 (line 2120-2170) |
| E11 | Table 8 Report structure（~10 sections × subsections × scope × comments） | Page 50-52, §7.2 (line 2379-2464) |
| E12 | Appendix 2：15 SE SLR coded by {Author, Date, Title, Reference, 主题类型, Topic area, Quality Score (DARE)} | Page 58-60 (line 2732-2855) |
| E13 | Appendix 1 Table 9：跨 6 个 medical / social-science 指南源 流程 steps 对照 | Page 56-58 (line 2635-2724) |

### 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象是什么？**
   - 主体：**SLR 综述流程的"协议字段族 + 表单族 + 检查表族 + 方法族 + 报告结构族"**。被逐项描述的"单位"不是 原始研究，而是**方法学构件**（field、checklist item、bias type、synthesis 方法、报告 section）。
   - 例外：Appendix 2 真正编码了 **15 篇 SE SLR**（2004-2007，DARE ≥ 2）。

2. **作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**
   - 对 指南 主体：**没有**。本文是 prescriptive 文档，从既有医学 / 社会科学指南（CRD、Cochrane、Australian NHMR、Petticrew & Roberts、Fink、Greenhalgh、Crombie、Shaddish 等 ≥ 8 个源）综合编写，不是 SLR 也不是 SMS。
   - 对 Appendix 2：**有最低限度的纳排**：venue = SE，year ∈ [2004, 2007-06]，由 Keele/Durham EBSE 项目人员用 York-CRD DARE 量表（4 题）评分，仅收录 DARE ≥ 2 者。但**没有报告检索式、数据库、初筛/全文筛流程**。

3. **原文字段来自哪里？**
   - 来自**多种 模式 容器**：
     - 抽取 form（§6.4.2、Table 7）
     - 分类方案（classification scheme；首次术语）（§5.3.1 question types、§5.3.2 PICOC、§6.5.1 synthesis modes、§6.5.4 定性 synthesis 3 类、§6.5.6 sensitivity 4 subset）
     - 质量量规（Table 5、Table 6、DARE 4-question）
     - bias 分类法（Table 4）
     - mapping table（Table 9 跨 6 源 流程 steps 对照）
     - 报告 template（Table 8）
     - search 文档 模式（Table 2）
     - 内嵌的 protocol 示例（Appendix 3 tertiary 研究 protocol）
     - 局部编码 appendix（Appendix 2 = 15 SE SLR）

4. **RQ 与样本单位的关系？**
   - 本文不是 RQ-driven 研究。其"研究目标"是 Executive Summary 一句："propose comprehensive 指南 for 系统文献综述 appropriate for software engineering 研究者, including PhD students."（Page vi, line 241-246）
   - 因此 RQ 与 样本单位 是"作者立场 / contribution claim"关系，不是"问题驱动样本编码"关系。

5. **若无系统样本库，如何降级？**
   - 主体 → **方法学种子 / 边界锚点**：可为 Paper2 的"综述维度树"提供：① question type 6-枚举；② PICOC 框架；③ Protocol 10-component；④ search-doc 模式；⑤ bias 4-枚举；⑥ 质量量规 grid（研究-type × 阶段）；⑦ 抽取 form 标准字段；⑧ synthesis 3-modal + 子枚举；⑨ 报告-structure 8 章模板；⑩ DARE 4-question 评分。**这些都是 模式种子（schema_seed），不是 发现**。
   - Appendix 2 → **局部 候选发现 边界**："2004-2007 上半年 SE SLR 主要集中在 Cost Estimation / 研究（Research） Trends / 技术 Evaluation 三大 topic type，每篇 DARE 评分 2-3.5 之间" 可作为 候选发现 但分母 n=15 且非系统采样，不得迁移到 Paper2 的主统计池。

### 3. 原生样本编码维度树 / 维度森林

> 中文化导读：本节复原的是指南文本中的方法组件森林，而不是一组被纳入论文的统计样本。树中包括综述流程、综述类型、研究问题、协议组件、检索记录、选择过程、偏倚类型、证据层级、质量工具、数据抽取表单、效应量、综合方法、敏感性分析和报告结构。英文术语多为指南原文中的固定方法名或医学/社会科学迁移来的术语；中文节点用于说明这些方法组件之间的层级和边界。可迁移的是“指南可为维度 pattern 提供脚手架”，不是把指南条目当作实证统计结果。

这是一个**维度森林**（多模式，multi-模式）+ **小型 Appendix 2 编码池**。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[维度森林] Kitchenham & Charters 2007 SLR 指南
│
├── T1 SLR 流程阶段模式（§4）
│   ├── 阶段：{计划（Planning）, 执行（Conducting）, 报告（Reporting）}；封闭 3 类
│   └── 子阶段：13 个阶段（阶段），并标记强制 / 可选（mandatory / optional）
│
├── T2 综述类型模式（§2.5）
│   └── 类型：{系统文献综述（系统文献综述）, 系统映射研究, 三级综述（Tertiary Review）}
│       + 术语表：元分析（meta-analysis）、原始研究、二次研究、敏感性分析（sensitivity analysis）、协议（protocol）
│
├── T3 研究问题模式（§5.3）
│   ├── 问题类型：6 类，源自 Australian NHMR 并做 SE 改写
│   │   └── {干预效果（effect of intervention）, 条件频率 / 比率（条件频率 / 比率（rate of condition））, 诊断测试性能（diagnostic-test performance）, 病因 / 风险因素（aetiology/risk factors）, 可预测性（predictability）, 经济价值（economic value）}
│   └── 问题结构：PICOC = {人群（Population）、干预（Intervention）、比较（Comparison）、结果（Outcome）、上下文（Context）}；附 实验设计（Experimental设计）
│
├── T4 协议组件模式（§5.4）
│   └── 10 个组件：背景（Background）、研究问题（ResearchQuestion）、检索策略（SearchStrategy）、研究选择标准（StudySelectionCriteria）、研究选择流程（StudySelectionProcedures）、质量评价清单（QualityAssessmentChecklist）、数据抽取策略（DataExtractionStrategy）、数据综合（DataSynthesis）、传播策略（DisseminationStrategy）、项目时间表（ProjectTimetable）
│
├── T5 检索记录模式（Table 2）
│   ├── 数字图书馆：数据库名、检索策略、日期、覆盖年份
│   ├── 期刊手工检索：期刊名、年份、未检索 issue
│   ├── 会议论文集：标题、会议名、译名、期刊名
│   ├── 未发表资料识别：联系的 group / 研究者、网站、日期
│   └── 其他来源：日期、URL、特定条件
│
├── T6 文献选择过程模式（§6.2）
│   ├── 纳排标准：开放文本 + pilot
│   ├── 实用过滤轴：语言（Language）、期刊（期刊）、作者（Authors）、场景（Setting）、参与者（Participants）、研究设计（Research 设计）、抽样方法（Sampling 方法）、发表日期（Date of publication）
│   └── 可靠性统计：Cohen κ
│
├── T7 偏倚分类法（Table 4）
│   └── {选择偏倚（Selection bias）、执行偏倚（Performance bias）、测量偏倚（Measurement bias）、流失偏倚（Attrition bias）} × {同义词（Synonyms）、定义（Definition）、保护机制（Protection mechanism）}
│
├── T8 证据层级模式（§6.3.1）
│   └── {系统综述 / 随机对照试验（SLR / RCT）、准实验（Quasi-experiment）、观察 / 相关研究（Observational / Correlation）、专家意见（Expert opinion）}
│
├── T9 质量工具模式（Tables 5–6）
│   ├── 定量研究检查表：约 50 条 × {通用经验研究（EmpiricalGeneric）, 相关研究, 调查, 实验} × 来源引用（原文研究类型枚举已中文化）；按设计 / 执行 / 分析 / 结论分阶段
│   └── 定性研究检查表：18 条 × source reference
│
├── T10 数据抽取表单模式（Table 7 实例）
│   ├── 标准字段：评审者姓名、抽取日期、标题、作者、期刊、发表细节、备注（括号内原字段名见原文 Table 7）
│   └── 综述专属字段：开放字段，需要 pilot；Maxwell 1998 实例约 30 行字段
│
├── T11 质量数据使用方式模式（§6.3.3）
│   └── {AssistSelection, AssistAnalysisAndSynthesis}，两者可叠加
│
├── T12 数据综合模式（§6.5）
│   ├── 综合模式：{描述 / 叙事（Descriptive / Narrative）, 定量 / 元分析（Quantitative / Meta-analysis）, 定性（Qualitative）, 混合（Mixed）}
│   ├── 二值效果度量：{赔率（Odds）, 风险（Risk）, OR, RR, ARR}
│   ├── 连续效果度量：{均值差（MeanDifference）, WMD, SMD}
│   ├── 呈现方式：森林图（森林图）、漏斗图（funnel plot）、汇总表（汇总表）
│   └── 定性综合方法：{互惠翻译（Reciprocal translation）、反驳式综合（Refutational synthesis）、论证线综合（Line of argument synthesis）}
│
├── T13 敏感性分析模式（§6.5.6）
│   └── 子集类型：{仅高质量研究（HighQualityOnly）、按研究类型（ByStudyType）、按数据抽取难度（ByExtractionDifficulty）、按实验方法（ByExperimentalMethod）}
│
├── T14 发表偏倚模式（§6.5.7）
│   └── 主要依赖 funnel plot 的视觉判定
│
├── T15 报告结构模式（Table 8）
│   └── 标题（Title）、署名（Authorship）、执行摘要（ExecutiveSummary）、背景（Background）、综述问题（ReviewQuestions）、综述方法（ReviewMethods）、纳入与排除研究（Included&ExcludedStudies）、结果（Results）、讨论（Discussion）、结论（Conclusions）、致谢（Acknowledgements）、利益冲突（ConflictOfInterest）、参考文献与附录（References&Appendices）
│
├── T16 流程步骤映射（Table 9 / Appendix 1）
│   └── 对照来源（原文组织 / 作者名保留）：Berkeley Systematic Reviews Group、Australian NHMR、Cochrane、CRD、Petticrew & Roberts、Fink
│
├── T17 博士轻量版（§9）
│   └── 单人研究者必须执行的 8 个 mandatory steps
│
└── T18 Appendix 2 局部经验编码池（唯一真实样本编码）
    ├── 样本：15 篇 SE SLR
    ├── 字段：作者（Author）、日期（Date）、标题（Title）、引用细节（ReferenceDetails）、主题类型（TopicType）、主题领域（TopicArea）、质量分数（QualityScore） (DARE)
    ├── 观察到的主题类型（TopicType）：技术评价（technology evaluation）、研究趋势（研究趋势）、技术
    └── 迁移边界：仅作早期 SE SLR 状态边界，不进入 Paper2 主统计池
```

### 4. 叶子维度表

> 篇幅限制下，本表只列出**最具代表性的、被原文显式封闭枚举的叶子**；其余叶子（如 Table 5 的 ~50 条 质量 items、Table 7 的 ~30 条 抽取 fields、Table 9 的 6×6 mapping 单元格）应在 A2a 精核时逐项展开。`E*` = §1 中的证据锚点 ID。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1-question-type | 综述问题类型 | T3 | §5.3.1 Australian NHMR 6 类 + SE 改写 5 类 | 综述意图归类 | {干预效果（effect）, 条件频率/比率（频次）, 诊断测试（diagnostic*）, 病因/风险因素（aetiology/risk）, 可预测性（predictability）, 经济价值（economic-value）}；SE 不适用 diagnostic | 完整枚举（封闭 6） | 若无 RQ，写 contribution_claim | 模式种子（schema_seed） | 可统计 Paper2 综述样本的问题类型分布 | E2 | 6-枚举源自医学；SE 不适用 diagnostic |
| L2-picoc | PICOC 元素 | T3 | §5.3.2 Petticrew & Roberts | 框定 RQ 五要素 | {人群（Population）、干预（Intervention）、比较（Comparison）、结果（Outcome）、上下文（Context）} | 完整枚举（封闭 5） | 指南 可不全填 | 模式种子（schema_seed） | 用于 RQ 结构化抽取 | E3 | 候选使用（需裁决） |
| L3-protocol-comp | Protocol 组件 | T4 | §5.4 | 协议必含字段 | {背景（Background）, RQ, 检索策略（SearchStrategy）, 选择标准（SelectionCriteria）, 选择流程（SelectionProcedure）, 质量清单（QualityChecklist）, 抽取策略（ExtractionStrategy）, 综合策略（Synthesis）, 传播策略（Dissemination）, 时间表（Timetable）} | 完整枚举（封闭 10） | optional 项可缺 | 模式种子（schema_seed） | 可统计目标语料的 protocol 完备度 | E4 | 可迁移 |
| L4-search-doc | 检索文档化 模式 | T5 | Table 2 | 检索过程记录 4 类 source × 字段 | (数字图书馆（DigitalLibrary）, 期刊手检（期刊 HandSearch）, 会议（会议）, 未发表材料（Unpublished）, 其他（Other）) × 各自字段 | 层级枚举（4 × 3-5） | 来源未用则不填 | 模式种子（schema_seed） | 可统计语料检索透明度 | E5 | 可迁移 |
| L5-bias-type | 偏倚类型 | T7 | Table 4 | 偏倚 4-枚举 | {选择偏倚（Selection）, 执行偏倚（Performance）, 测量偏倚（Measurement）, 流失偏倚（Attrition）} × {同义词（syn）, 定义（def）, 防护措施（protection）} | 完整枚举（封闭 4） | 不评偏倚→not_assessed | 模式种子（schema_seed） | 可统计研究的偏倚控制覆盖 | E6 | 部分医学概念在 SE 不易适用（blinding） |
| L6-质量-item-quant | 量化研究质量条目 | T9 | Table 5 | 量化质量检查表 ~50 条 | 自由文本条目 × {通用经验研究, 相关研究, 调查, 实验} × 来源引用（原文研究类型枚举已中文化） | 层级枚举 + 关系值（应用研究类型） | 不适用项打 -- | 模式种子（schema_seed） | 可统计目标语料的质量条目分布 | E7 | 选择适用子集（作者建议） |
| L7-质量-item-qual | 质性研究质量条目 | T9 | Table 6 | 质性质量检查表 18 条 | 18 条自由文本条目 × Source ref | 完整枚举（封闭 18） | 不适用项打 -- | 模式种子（schema_seed） | 可统计质性综述质量 | E8 | 候选使用（需裁决） |
| L8-抽取-field | 数据抽取标准字段 | T10 | §6.4.2 + Table 7 | 抽取表标准 + 综述特定字段 | 标准字段 = {评审者姓名、日期、标题、作者、期刊、出版细节、备注}（封闭 7；原字段名见原文）+ 综述特定字段开放 | 完整枚举（部分） + 自由文本 | -- | 模式种子（schema_seed） | 可作为 Paper2 抽取表模板 | E9 | 可迁移 |
| L9-effect-binary | 二元效应度量 | T12 | §6.5.2 | 二元结局合成度量 | {赔率（Odds）, 风险（Risk）, OR, RR, ARR} | 完整枚举（封闭 5） | 非二元结局→不适用（不适用） | 模式种子（schema_seed） | 元分析（meta-analysis） 必备 | E10 | 可迁移 |
| L10-effect-continuous | 连续效应度量 | T12 | §6.5.2 | 连续结局合成度量 | {均值差（MeanDifference）, WMD, SMD} | 完整枚举（封闭 3） | 非连续结局→不适用（不适用） | 模式种子（schema_seed） | 元分析（meta-analysis） 必备 | E10 | 可迁移 |
| L11-qual-synth | 质性合成方法 | T12 | §6.5.4 Noblit & Hare | 质性综合 3 类 | {互惠式（Reciprocal）, 反驳式（Refutational）, 论证线式（LineOfArgument）} | 完整枚举（封闭 3） | -- | 模式种子（schema_seed） | 质性综述方法学统计 | line 2208-2224 | 可迁移 |
| L12-sensitivity-axis | 敏感性分析 subset 轴 | T13 | §6.5.6 | 敏感性 4 类 | {仅高质量研究（HighQualityOnly）, 按研究类型（ByStudyType）, ByExtractionDifficulty, 按实验方法（ByExperimentalMethod）} | 完整枚举（封闭 4） | -- | 模式种子（schema_seed） | 可统计 sensitivity 透明度 | line 2253-2258 | 可迁移 |
| L13-报告-section | 报告章节 | T15 | Table 8 | 报告结构 ~10 章 | {标题（Title*）, 署名（Authorship*）, 执行摘要（ExecSummary）, 背景（Background）, RQ, 方法（Methods）, 纳入与排除研究（Included&Excluded）, 结果（Results）, 讨论（Discussion）, 结论（Conclusions）, 致谢（Acknowledgements*）, 利益冲突（ConflictOfInterest）, 参考文献与附录（References&Appendices）} | 完整枚举（封闭） + *=PhD可省 | 章节缺失→未报告 | 模式种子（schema_seed） | 可统计目标语料报告完备度 | E11 | 可迁移 |
| L14-流程-step-source | 过程-step 来源源 | T16 | Table 9 | Appendix 1 跨源对照 6 源 | {Berkeley, ANHMR, Cochrane, CRD, Petticrew&Roberts, Fink} | 完整枚举（封闭 6） | -- | 模式种子（schema_seed） | 可建跨指南源 cross-walk | E13 | 可迁移结构 |
| **L15-appx2-topic-type** | **Appendix 2 主题类型** | **T18** | **Appendix 2** | **15 SE SLR 编码列** | {技术评价（technology evaluation）, 研究趋势（研究趋势）, 技术} | **层级枚举（观察 3 类，未完全饱和）** | -- | **可统计（n=15）但分母小且非系统采样** | 候选发现（cost-estimation 占主导） | E12 | **慎用**：仅 2004-2007 上半年 SE SLR |
| **L16-appx2-topic-area** | **Appendix 2 主题区** | **T18** | **Appendix 2** | **15 SE SLR 编码列** | 13+ open-ended labels（Cost Estimation 出现 6 次最多） | 自由文本（高频项可统计） | -- | **可统计 候选发现** | "cost estimation 是 2004-07 SE SLR 主导主题"是可生成的 candidate | E12 | 不可迁移到 Paper2 主统计池 |
| **L17-appx2-dare-score** | **Appendix 2 DARE 评分** | **T18** | **DARE 4-question** | **0-4 区间** | {2.0, 2.5, 3.0, 3.5} | 数值（区间） | -- | **可统计 mean/median** | candidate：当时 SE SLR 质量约 2.5-3.0 中位 | E12 | 评分员主观（Keele/Durham 自评） |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R1 | L1-question-type | drives | T6 selection criteria | (open-ended) | -- | Page 17, line 708-715 | 问题类型驱动选择策略 |
| R2 | L2-picoc | provides_search_切面（facets）_for | T5 search-doc | per-facet keywords | -- | Page 22, line 983-988 | PICOC → 搜索串构造 |
| R3 | L5-bias-type | mitigated_by | L6/L7 质量 items | 质量 checklist 子集 | -- | Page 30, line 1428-1432 | bias 类型 ↔ 质量条目 |
| R4 | T10 抽取-form fields | derived_from | L1 question + L6 质量 items | -- | -- | Page 37, line 1716-1721 | 抽取字段必同时服务于 RQ 与 QA |
| R5 | L11-质量-data-use | governs | L8-抽取-field 组织方式 | {single-form, separate-form} | -- | Page 36, line 1663-1671 | QA-as-selection vs QA-as-analysis 决定表单结构 |
| R6 | T13 sensitivity subset | partitions | T18 sample池 | 研究-level subset | -- | Page 46, line 2253-2258 | sensitivity 切分原 sample |
| R7 | L9/L10 effect measures | input_to | 森林图 / funnel plot | 视觉图示 | -- | Page 44-47, Figures 1-2 | 效应度量 → 视觉呈现 |
| R8 | L14-流程-step-source | cross_walks_to | L14（其它源） | 跨源同义 step | -- | Table 9, Appendix 1 | 跨指南 流程-step 同义映射 |
| R9 | L17-appx2-dare-score | computed_from | DARE 4-question | {0,1,2,3,4} 四题加权 | <2 即排除 | Page 16-17, line 648-655 | DARE 评分构造 |

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段 / 统计表支持的"统计观察"

- **唯一来自原文样本编码池的统计观察（n=15，Appendix 2）**：
  - Cost Estimation 是 2004-2007 上半年 SE SLR 最多见的 topic area（15 篇中 6 篇直接标注 Cost Estimation，占 40%）
  - DARE 评分集中在 2.0-3.5 之间，最高 3.5（Zannier 2006 / Glass 2004 不在最高？实际最高 3.5 = Zannier 2006）
  - Topic Type 在 3 类标签内（技术评价（technology evaluation） / 研究趋势（研究趋势） / 技术）覆盖全部 15 篇
- **方法学构件级统计**（仅是 模式 计数，不是 发现）：
  - bias 4-类、effect measure 5+3、定性 synthesis 3-类、PICOC 5-元素、protocol 10-组件 — 均为**作者引入的枚举大小**，不是研究结果。

#### 6.2 原文 discussion / 推荐 提出的"候选发现"

- "SE 与 Social Sciences 的研究方法相似度 = 0.83，与 Clinical Medicine 仅 0.17"（Table 1，来自 Budgen et al. [6] 调研，不是本文实证） — 是 **derived candidate**，不可作为本文独立 发现。
- "SE 论文摘要质量不足以用于 SLR 筛选"（Brereton et al. [5]） — **二手候选**。
- "PhD-light SLR 是单一研究者可行的"（§9） — **作者主张**，非实证 发现。
- "Cochrane / 医学指南**不推荐**用质量分加权 元分析（meta-analysis）"（§6.3.3） — 是**对既有指南立场的复述**，非本文实证。

#### 6.3 对 Paper2 可迁移的方法学启发

- T3-T17 几乎全部可作为 **Paper2 维度树 模式种子（schema_seed）**（即"综述如何被结构化描述"的字段先验）。
- 特别有用：
  - **T18 (Appendix 2 编码表)**：是本文唯一展示"如何把一组 SLR 编码成可统计行"的实例 — Paper2 的"综述总账表"可作为候选参考其字段架构（Author / Year / Title / Reference / 主题类型（TopicType） / TopicArea / 质量分数（QualityScore）），但需补 venue、CCF-rank、systematic-证据-status、sample-unit、树-type 等字段。
  - **Table 9 (流程-step cross-walk)**：是 Paper2 跨综述方法学比较的**模板**（跨指南 step 同义映射）。

#### 6.4 绝不能迁移的"领域结论"

- 本文是 **2007 年技术报告**，对 SE 的方法学诊断已经过时（2009 之后 Kitchenham 自己已多次更新指南）。
- Table 1 的 SE↔其他学科相似度 0.17-0.83 是 Budgen et al. 2006 一篇定性访谈结论，**不可作为 Paper2 跨学科可比性结论的证据**。
- DARE 评分均值 = 2.5 仅基于 15 篇，且评分者是评分对象的合作者群体（Keele/Durham EBSE 团队），存在**评分者-评分对象耦合 risk**。

## survey_of_surveys 自身 schema 抽取

本节把该论文投影到本目录自己的脚手架综述 schema（S1--S8）。判定等级只说明该维度在原文和本地证据链中的可用程度：`强` = 有明确原文结构和证据锚点；`中` = 有可复用结构但存在范围、裁决或精核限制；`弱` = 只作边界启发或风险提示；`不适用` = 原文类型不支持该维度进入统计池。
边界声明：本节所有 S1--S8 与维度树判断均为 A1 文本级 `schema_seed` / 方法模式审计结果；A2a 完成页码、表图和制品精核前，不得写成 final quantitative finding / 最终定量发现。


| 维度 | 判定等级 | 一句话抽取结果 | 证据位置 |
|---|---|---|---|
| S1 综述任务设定 | 中 | 本文是 SE SLR 方法学指南，目标清楚但自身不是 RQ-driven SLR/SMS，缺少普通综述样本单位；主归属为方法学参考/模式种子。 | `review.md` §1、§2；`evidence_chain.md` A.3 `clm-kitchenham-charters-2007-slr-guidelines-type`、`clm-kitchenham-charters-2007-slr-guidelines-pool` |
| S2 语料收集与筛选 | 中 | 主体没有系统检索/纳排样本库；Appendix 2 对 2004--2007 上半年 15 篇 SE SLR 有局部收录和 DARE 分数。 | `review.md` §2、§6.1；`evidence_chain.md` A.2 `ev-kitchenham-charters-2007-slr-guidelines-denom` |
| S3 原生维度树/样本编码对象 | 中 | 原生对象是 guideline item / 方法组件森林：RQ、PICOC、protocol、search-doc、bias、quality checklist、data extraction、synthesis、report structure 等；不是普通样本文献编码树。 | `review.md` §3；`evidence_chain.md` A.3 `clm-kitchenham-charters-2007-slr-guidelines-unit`、`clm-kitchenham-charters-2007-slr-guidelines-tree` |
| S4 字段级证据 | 中 | 叶子表列出 question type、PICOC、protocol components、search-doc、bias type、quality items、extraction fields、effect measures、report sections、Appendix 2 topic/DARE 字段；字段结构丰富，但表图/附录行完整性仍待 PDF 精核。 | `review.md` §4；`evidence_chain.md` A.2 `ev-kitchenham-charters-2007-slr-guidelines-tree`；`audits/a1-s1s8-19x1/adjudications/kitchenham-charters-2007-slr-guidelines.md` |
| S5 维度模式演化 | 中 | 本文体现从医学/社会科学 SLR 指南到 SE guideline 的迁移与适配，并通过 Table 9 做跨指南流程 step cross-walk。 | `review.md` §3 T16、§5 R8、§6.3 |
| S6 统计分析 | 弱 | 主体无统计分析；Appendix 2 的 15 篇 SE SLR 只作局部边界观察，方法组件枚举不是 empirical statistic，不能进入主统计池。 | `review.md` §6.1、§4；`evidence_chain.md` A.3 `clm-kitchenham-charters-2007-slr-guidelines-pool` |
| S7 候选 finding | 弱 | 可记录的 finding 多为方法学启发或二手候选；Appendix 2 的早期 SE SLR 主题/质量分布只能作边界锚点。 | `review.md` §6.2、§6.4 |
| S8 研究者/作者质疑与裁决 | 中 | 原文提供 inclusion reliability、data extractor/checker、quality assessment、protocol/report evaluation 等方法机制，但不是本文实际执行裁决日志。 | `review.md` §3 T6/T10/T11、§5 R4/R5/R9 |

### S1--S8 四分栏证据拆分

#### 总体统计池裁决

- **主统计池资格：否。** 本文是 EBSE-2007-01 方法学 guideline / 技术报告，主体目标是提出适合软件工程 SLR 的指南；它从医学指南、社会科学书籍和跨学科讨论中综合方法，而不是一篇按自身 RQ 系统检索、纳排并编码样本文献的经验性 SLR/SMS。
- **可保留身份：schema_seed / 方法学脚手架 / boundary_anchor。** 可迁移 SLR 流程、PICOC、protocol、检索记录、质量评价、数据抽取、综合与报告结构等维度模式；不得把这些规范性枚举当作 survey_of_surveys 主统计样本。
- **Appendix 2 / Appendix 3 边界：** Appendix 2 的 15 篇 SE SLR 表只能作早期 SE SLR 局部边界观察；Appendix 3 是 tertiary study 的计划性 protocol 示例，不是本文已经完成的独立 tertiary study 结果。因此 **guideline 不得进入主统计池**。

读取依据：[bibtex.bib](../../../papers/kitchenham-charters-2007-slr-guidelines/bibtex.bib)、[paper_content.txt](../../../papers/kitchenham-charters-2007-slr-guidelines/paper_content.txt)、[review.md](../../../papers/kitchenham-charters-2007-slr-guidelines/review.md)、[evidence_chain.md](../../../papers/kitchenham-charters-2007-slr-guidelines/evidence_chain.md)。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | Executive Summary 明确目标是提出 software engineering SLR guidelines；BibTeX 标为 technical report；正文说明指南来自既有医学指南、社会科学书籍与跨学科讨论。 | 不是 RQ-driven 的二级研究；应复原为“方法学指南任务”，其研究意图节点只提供 SLR 计划、执行、报告的脚手架。 | 不进主池；仅作方法学背景和 schema_seed。 | 核对 PDF 首页、报告号 EBSE-2007-01、出版机构与引用格式；确认摘要目标没有被误写成经验性 survey 目标。 |
| S2 语料收集与筛选 | 主体没有完整数据库检索、候选集、筛选流；Appendix 2 只列 2004--2007 上半年 DARE 评分大于等于 2 的 15 篇 SE SLR；Appendix 3 只是计划性 protocol，列出待检索期刊会议、纳排标准和单人选择加他人检查。 | 主体树中“检索/纳排”是指南建议和记录模板；唯一局部样本表为 Appendix 2 的 selected list，不构成主文本完成的系统语料库。 | 不进主池；Appendix 2 仅 boundary_anchor，不得作为 A1 主分母。 | 逐页核对 Appendix 2 是否确为 15 行、质量分是否完整；核对 Appendix 3 是否无执行结果和最终纳排流。 |
| S3 原生维度树/样本编码对象 | §5--§7 与 Tables 2--8 展开 RQ、PICOC、protocol、search documentation、selection、bias、quality checklist、data extraction、synthesis、report structure；evidence_chain 裁决为“主体不编码样本”。 | 应复原为多棵方法组件树/维度森林，而非“纳入论文样本编码树”；节点包括 question/PICOC/protocol/search-doc/bias/quality/extraction/synthesis/report。 | 不进主池；维度森林可作为字段设计种子。 | PDF 版面核对 Tables 2--8 的标题、层级和跨页完整性；避免把指南字段误当成实证分类结果。 |
| S4 字段级证据 | review 叶子表列出 question type、PICOC、10 个 protocol components、search-doc、bias type、质量条目、抽取字段、effect measures、report sections、Appendix 2 topic/DARE 字段；既有裁决要求 S4 从强降中。 | 字段很多但来源是规范性指南/模板；Appendix 2 字段是局部小表。S4 应为“中”：可复用字段强，但统计证据资格弱。 | 不进主池；只允许字段模板级引用。 | 精核 protocol components 为 10 项；核对 Tables 5--7 条目数量和 Table 8 章节；如现有总账仍写“强”，建议降级为“中”。 |
| S5 维度模式演化 | 原文说明指南改编自医学与社会科学来源；Table 9 对 Berkeley、Australian NHMR、Cochrane、CRD、Petticrew & Roberts、Fink 等流程步骤做 cross-walk。 | 可复原为“跨学科 SLR 指南向 SE 适配”的模式演化树，核心是流程步骤同义映射和 SE 特定问题适配。 | 不进主池；可作为演化/来源谱系 schema_seed。 | 核对 Table 9 六个来源列与步骤对应；区分作者适配意见和被转述来源原观点。 |
| S6 统计分析 | 主体没有自身统计分析；Appendix 2 可数 15 篇、topic type/area、DARE 分数；正文还给出 effect measure 和 sensitivity analysis 的方法说明。 | “统计”分两层：指南中的 effect/sensitivity 是方法枚举；Appendix 2 是很小的局部列表统计，不能代表 survey_of_surveys 目标语料。 | 不进主池；Appendix 2 统计只可标为局部候选观察。 | 复算 Appendix 2 的 topic area、topic type、DARE 分数；核对是否存在隐藏执行报告；不得把 15 篇作为主分母。 |
| S7 候选 finding | 原文主体产生的是方法建议；review 已标明 SE 相似度、摘要质量、PhD-light、质量加权等多为二手候选或作者主张；Appendix 2 的主题/质量分布只是早期边界。 | 应复原为“方法学启发/二手候选 finding”层，而非本文原创实证 finding 树。 | 不进主池；只能作为写作背景、方法动机或待复核候选，不进入 final research finding。 | 追溯二手 finding 的原始引用；确认 Appendix 2 观察不被写成普遍 SE SLR 结论。 |
| S8 研究者/作者质疑与裁决 | 原文规范了 protocol evaluation、selection reliability、Cohen kappa、data extractor/checker、quality assessment 和报告评价；Appendix 3 计划一人抽取、一人检查；但这不是本文实际执行的裁决日志。 | 可复原为“裁决机制模板”：协议评审、双人/检查者机制、质量量规、偏倚与敏感性分析；不是本文样本级争议解决记录。 | 不进主池；可作为 audit/review 工作流设计种子。 | 核对 front matter reviewer、Appendix 3 checker 与正文建议之间的角色差异；确认没有把方法建议误当成已执行审计证据。 |

## 证据链入口

详见 [evidence_chain.md](./evidence_chain.md)；A.1--A.4 证据链与结论-证据映射已迁出，当前证据状态（如 `not_verified`、待 A2a、`schema_seed`）保持原样。
