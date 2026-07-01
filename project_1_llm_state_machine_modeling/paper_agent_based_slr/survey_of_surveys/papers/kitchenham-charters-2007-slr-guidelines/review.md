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
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 历史观察 | 暴露“guideline 类文献没有普通研究结果 RQ 表”的差异；已在 schema 中使用 `综述 / 指南类型` 与 `不适用` 缺失值语义处理。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 研究问题是 SLR 最重要的 protocol 元素；可按 population/intervention/comparison/outcome/context 等结构化。 | `paper_content.txt` Page 2--3 目录列出 §5.3 Research Questions；Page 12 附近说明 protocol 应包含 research questions。 | 可迁移到 Paper2 的“研究者定义综述元模型”和维度模式初始化。 | 这是 guideline，不代表任一 SE 子领域的真实 RQ 分布。 |
| dimension pattern | SLR protocol 至少需要 review need、research questions、search strategy、study selection、quality assessment、data extraction、data synthesis、reporting。 | `paper_content.txt` Page 2--3 目录列出 §5--§7；Page 30 附近讨论 data extraction forms。 | 可作为 `pattern-field-schema.md` 的阶段字段候选。 | 只能作为流程字段先验，不能直接冻结目标主题字段树。 |
| finding pattern | guideline 本身不生成领域 finding；它提供流程规范与质量判据。 | `paper_content.txt` Page 2--3 目录；Page 40 附近 reporting/evaluating review reports。 | 对 Paper2 的 finding 启发式不历史草稿曾提出迁移建议；当前禁止直接采信，只能迁移报告与评价结构。 | guideline 不产生领域 finding，只迁移 finding 报告约束。 |
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
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__codex.md](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__codex.md)、[../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__claude.md](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__claude.md)、[../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__deepseek.md](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md](../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

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
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**实际读取**：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`（claim-证据 gate、reviewer mode、证据 policy）
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`（universal review dimensions、constructive specificity standard）
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`（5-dimension review、claim audit、adversarial questions）
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`（Paper2Code 4-turn）
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- `bibtex.bib`、`metadata.json`
- `paper_content.txt`：逐段读完目录（§0.1）→ Executive Summary / Glossary（§0.4-0.5，pp.vi-vii）→ §2 SLR/SMS/Tertiary 定义 → §3 Table 1 SE vs other disciplines → §4 三阶段流程 → §5 计划（Planning）（含 §5.3.1 6 类 question types + §5.3.2 PICOC）→ §6.1 Search（Table 2 search 文档）→ §6.2 Selection（含 §6.2.3 Cohen κ）→ §6.3 Quality（Tables 3-6：bias 4 类 + 量化检查表 ~50 项 + 质性检查表 18 项）→ §6.4 数据抽取（数据抽取）（Table 7 实例：Maxwell 1998）→ §6.5 Synthesis（5 binary + 3 continuous effect measures、森林图、funnel plot、3 类 定性 synthesis）→ §6.5.6 sensitivity 4 类 subset → §7 报告（Reporting）（Table 8 报告结构）→ §8 Mapping Studies → §9 PhD-light version → Appendix 1（Table 9 跨 6 源 流程 steps）→ Appendix 2（15 SE SLR 编码表）→ Appendix 3 tertiary protocol
- `review.md`（v2 后已挂三路审计返修块，但主树仍是六叶接口）

**版面核验**：仅基于 `paper_content.txt` 的 `--- Page N ---` 分页标记定位页码；`paper.pdf` 未单独打开做视觉核验，Tables 2/5/7/8/9 的精确表格版式、Figures 1-2（森林图 / funnel plot）的图示边界、Appendix 2 跨页表格的行数完整性仍需 A2a 精核。

**关键证据锚点（10 条）**：

| # | 内容 | 文件 / 页 / 区位 |
|---|---|---|
| E1 | "Specifying the research questions is the most important part of any 系统综述" | `paper_content.txt` Page 17, §5.3 (line 707-715) |
| E2 | 6 类 question types（adapted from Australian NHMR）+ SE 改写 | Page 17-18, §5.3.1 (line 719-734) |
| E3 | PICOC = Population / Intervention / Comparison / Outcome / Context（Petticrew & Roberts） | Page 18-20, §5.3.2 (line 797-863) |
| E4 | Protocol 9 components 列表 | Page 20-21, §5.4 (line 893-922) |
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
   - 主体 → **方法学种子 / 边界锚点**：可为 Paper2 的"综述维度树"提供：① question type 6-枚举；② PICOC 框架；③ Protocol 9-component；④ search-doc 模式；⑤ bias 4-枚举；⑥ 质量量规 grid（研究-type × 阶段）；⑦ 抽取 form 标准字段；⑧ synthesis 3-modal + 子枚举；⑨ 报告-structure 8 章模板；⑩ DARE 4-question 评分。**这些都是 模式种子（schema_seed），不是 发现**。
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
│   └── 9 个组件：背景（Background）、研究问题（ResearchQuestion）、检索策略（SearchStrategy）、研究选择标准（StudySelectionCriteria）、研究选择流程（StudySelectionProcedures）、质量评价清单（QualityAssessmentChecklist）、数据抽取策略（DataExtractionStrategy）、数据综合（DataSynthesis）、传播策略（DisseminationStrategy）、项目时间表（ProjectTimetable）
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

### 7. 对旧版 `review.md` 的返修来源

| 严重度 | 编号 | 问题 | 返修动作 |
|---|---|---|---|
| **C-1** | C1 | review.md 把"研究范围 / 语料 / 分类 / 方法 / 证据 / 发现"六个**通用接口叶子**作为本文维度树的事实主源（line 96-102），违背 A1-DT v2 关于"不得用六叶模板替代原文 模式"的硬约束 | 把这六叶**完整降级**为"跨论文投影"小节；把 T3 question 模式、T4 protocol、T5 search-doc、T7 bias、T9 质量 grid、T10 抽取 form、T12 synthesis、T15 报告结构 升为**原文 模式 主森林**（即把旧版 review.md "原文模式主树（19×3 审计后返修）"小节的 6 行扩展为 15+ 个具体 模式，并各自给取值空间、Table 编号、页码） |
| **C-2** | C2 | review.md 没有识别 **Appendix 2 的 15-SLR 局部编码池**——这是本文唯一的真实"样本-字段"编码实例，但被完全忽略 | 在维度森林中**新增 T18 节点**；在叶子表中加入 L15/L16/L17；在 §6 "统计与候选发现链路"中明确：Appendix 2 是 candidate-发现 入口，n=15，DARE 评分者-对象耦合是已知 risk |
| **I-1** | I1 | Tables 2/4/5/6/7/8/9 在 review.md 中只在"原文模式主树"表中以 6 个**整段一行**形式概括（line 124-130），没有展开任何具体字段、取值空间、行数；A.2 证据账本仅有 EV-001 到 EV-004 共 4 行高度抽象证据 | A.2 应至少新增证据：EV-Table2-search-doc、EV-Table4-bias、EV-Table5-质量-quant、EV-Table6-质量-qual、EV-Table7-抽取、EV-Table8-报告、EV-Table9-流程-step、EV-Appendix2-coded-15、EV-PICOC、EV-effect-measures；每条挂具体 Table 编号 + 页码 |
| **I-2** | I2 | metadata.json 中 `eligible_for_statistical_synthesis: false` 是对的，但**没有把 Appendix 2 的 15-SLR 编码池作为"局部 候选发现 入口"标注出来** | 在 metadata.json 新增字段 `local_empirical_subset: {appendix: 2, n: 15, fields: [...], pool_status: "候选发现（candidate_finding）_anchor_only"}` 或在 review.md 卡片中显式声明 |
| **I-3** | I3 | review.md "维度树复原" 一句话结论说 "本文的维度树主类型为方法流程树，辅助类型为质量/效度 指南 树"——**漏说"维度森林"**特征：本文有 ≥10 个独立 模式 容器 | 改为："本文的原生结构是**多 模式 维度森林**（≥10 个并列 模式 容器：question type / PICOC / protocol component / search-doc / bias 分类法 / 质量 grid / 抽取 form / synthesis modes / sensitivity axes / 报告结构 等）+ 一个 n=15 的 Appendix 2 局部编码池。" |
| **I-4** | I4 | A.4 复验命令仅 2 条且 visual-check 状态 `needs_manual_check` 长期未推进；Tables 5/7/9 跨页表格的版面、Figures 1-2 的图示边界均未做 PDF 视觉核验 | 把 A.4 拆为 Table-by-Table 的 visual-check 条目，每条给出具体 Table/Figure 编号、目标页码区间、通过条件 |
| **I-5** | I5 | SUMMARY 当前表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"若仍写"方法学 指南 / 不适用（不适用） / 方法流程树 + 质量树 / 模式种子（schema_seed） only"，则未反映 Appendix 2 部分 | SUMMARY 行应改为：样本单位="主体=方法学构件；Appendix 2=15 SE SLR"；样本数量="主体 不适用（不适用） / Appendix 2 = 15"；树类型="**维度森林**+局部编码池"；池资格="主体 模式种子（schema_seed）；Appendix 2 = 局部 candidate-发现 anchor，不进入主池" |
| M-1 | M1 | 旧 "六类 模式 抽取"小节（review.md §2）与维度树复原小节存在显著 overlap，且未对齐 v2 口径 | 保留作为 v1 历史快照，但在节首加 `> [!WARNING] v1-historical: 内容已被 §维度树复原 + A1-DT v2 取代` |
| M-2 | M2 | "A1-M0--M6 脚手架元维度贡献"表（line 49-58）是 v1 跨论文投影残留，A1-DT v2 已禁止用 M0-M6 模板代表原文 | 整段移到附录或加 v1-deprecated 警示 |

### 8. 历史审计草案归档（禁止消费为事实真源）

> [!WARNING] 历史草案归档，禁止消费为事实真源：本节仅保留 A1-DT v2 形成过程中的审计草稿，不得作为当前证据强度、SUMMARY 统计池、正式维度树或正式结论-证据映射使用。若本节与文末正式 `### A.1`--`### A.4` 审计附录冲突，一律以文末正式审计附录为准。

#### 历史 A.2 维度树证据账本草案（禁止消费）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-question-types | paper_content.txt | §5.3.1 Question Types | Page 17-18, line 719-734 | 释义：原文列 Australian NHMR 6 类问题（intervention/频次/diagnostic/aetiology/可预测性（predictability）/economic），并把 SE 改写为 5 类（去除 diagnostic） | classification_schema | medium（文本明确，Table 不存在） | T3 / L1-question-type | text-only | 6-枚举源自医学，SE 不适用 diagnostic |
| EV-picoc | paper_content.txt | §5.3.2 Question Structure | Page 18-20, line 797-863 | 释义：PICOC 五元素来自 Petticrew & Roberts [25]；Kitchenham 2007 用 PICO；本文对 P/I/C/O/Context 各给 SE 解释段落 | classification_schema | 历史草稿旧强度（当前禁止采信） | T3 / L2-picoc | text-only | 候选使用（需裁决） |
| EV-table2-search-doc | paper_content.txt | §6.1.4 Documenting the Search | Page 24, Table 2, line 1067-1086 | 短引："Procedures for documenting the 检索过程 are given in Table 2." Table 含 5 source × 字段 | extraction_schema | medium | T5 / L4 | needs_pdf_visual | Table 跨页风险低；可文本恢复 |
| EV-table4-bias | paper_content.txt | §6.3.2 Development of Quality Instruments | Page 30, Table 4, line 1390-1426 | 短引："The CRD Guidelines [19] ... all refer to four types of bias shown in Table 4." 4 行 × {同义词（Synonyms）、定义（Definition）、保护机制（Protection mechanism）} | classification_schema | 历史草稿旧强度（当前禁止采信） | T7 / L5 | text-only | 部分医学 protection 在 SE 不适用 |
| EV-table5-质量-quant | paper_content.txt | §6.3.2 | Page 33-35, Table 5, line 1514-1620 | 释义："Summary Quality Checklist for Quantitative Studies"，~50 行问句 × {Empirical, Correlation, 调查, 实验 4 列 × 是否打 X} × Source 列引用 [10][11][12][19][25] | 质量量规（quality_rubric） | medium（跨页表格，文本提取可能丢列对齐） | T9 / L6 | **needs_pdf_visual**（首要核验项） | Table 跨 3 页，必须 PDF 视觉确认 X 对齐 |
| EV-table6-质量-qual | paper_content.txt | §6.3.2 | Page 36, Table 6, line 1626-1658 | 释义：18 行 × {Source ref}；首项 "How credible are the 发现?" 等 | 质量量规（quality_rubric） | 历史草稿旧强度（当前禁止采信） | T9 / L7 | text-only | -- |
| EV-table7-抽取-form | paper_content.txt | §6.4.2 | Page 38-40, Table 7, line 1751-1968 | 释义：Maxwell et al. 1998 抽取实例，~30 字段：数据抽取者 / 检查者（DataExtractor/Checker）, StudyIdentifier, ApplicationDomain, 数据库名称（DatabaseName）, NumberOfProjects, SizeMetric, 准确率Measures, Cross-companyModel{techniques, transformations, variables, cross-val}, Within-companyModel{...}, Comparison, 数据（Data）Summary | 抽取_form_template | 历史草稿旧强度（当前禁止采信） | T10 / L8 | text-only | 仅一个实例；非通用模板 |
| EV-effect-measures | paper_content.txt | §6.5.2 | Page 43-44, line 2120-2170 | 释义：5 binary measures（Odds, Risk, OR, RR, ARR）+ 3 continuous（MeanDiff, WMD, SMD）+ 优缺点 | classification_schema | 历史草稿旧强度（当前禁止采信） | T12 / L9, L10 | text-only | 历史草稿曾提出迁移建议；当前禁止直接采信 |
| EV-qual-synth | paper_content.txt | §6.5.4 | Page 45, line 2208-2224 | 释义：Noblit & Hare 3 类：Reciprocal translation / Refutational / Line of argument | classification_schema | 历史草稿旧强度（当前禁止采信） | T12 / L11 | text-only | -- |
| EV-sensitivity-axes | paper_content.txt | §6.5.6 | Page 46, line 2253-2258 | 释义：4 类 subset（HighQuality / 按研究类型（ByStudyType） / ByExtractionDifficulty / 按实验方法（ByExperimentalMethod）） | classification_schema | 历史草稿旧强度（当前禁止采信） | T13 / L12 | text-only | -- |
| EV-table8-报告-structure | paper_content.txt | §7.2 | Page 50-52, Table 8, line 2379-2464 | 释义：报告结构 ~10 章 × subsection × scope × comments；* 标注的章节 PhD 不必有 | template_模式 | medium | T15 / L13 | needs_pdf_visual | 跨 3 页 |
| EV-table9-流程-cross | paper_content.txt | Appendix 1 | Page 56-58, Table 9, line 2635-2724 | 释义：6 个 medical/social-science 指南源 × 各自 流程 steps（左右对照） | mapping_模式 | medium | T16 / L14 | needs_pdf_visual | 跨页对照表 |
| EV-appx2-coded-15 | paper_content.txt | Appendix 2 | Page 58-60, line 2732-2855 | 释义：15 SE SLR (2004-2007.06) 编码：{Author, Date, Title, Ref, 主题类型（TopicType）, TopicArea, 质量分数（QualityScore） (DARE)}；DARE 评分由 Keele/Durham EBSE 团队自评 | local_empirical_pool | 历史草稿旧强度（当前禁止采信）（本文唯一真实样本编码） | T18 / L15-L17 | needs_pdf_visual | n=15 且评分者-对象耦合；不可作为主池 |
| EV-table1-cross-discipline | paper_content.txt | §3 | Page 13, Table 1, line 520-529 | 释义：SE 与 6 学科研究方法相似度（0.17-0.83）；来自 Budgen et al. [6] | author_claim_with_secondary_source | weak（二手） | -- | text-only | 不可作为本文 发现 |

#### 历史 A.3 结论-证据映射草案（禁止消费）

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-树-type-v2 | 本文原生结构是**维度森林（≥10 个并列 模式 容器）+ Appendix 2 局部 n=15 编码池**；主体不进入主统计池，仅 Appendix 2 可作 candidate-发现 anchor | 树类型（tree_type） | T1-T18 整体 | EV-question-types, EV-picoc, EV-table2/4/5/6/7/8/9, EV-effect-measures, EV-appx2-coded-15 | medium | 用于 Paper2 模式种子（schema_seed） + 局部 候选发现 | 指南 主体非实证；Appendix 2 评分者-对象耦合 |
| CLM-question-type-枚举 | 综述问题类型的 6-枚举（含 SE 不适用 diagnostic）可作为候选 Paper2 综述编码字段 | classification_schema种子（schema_seed） | T3 / L1 | EV-question-types | 历史草稿旧强度（当前禁止采信） | 模式种子（schema_seed） | 源自医学，SE 适用性需 pilot |
| CLM-picoc-框架 | PICOC 5 元素可作为 Paper2 RQ 抽取必填字段 | classification_schema种子（schema_seed） | T3 / L2 | EV-picoc | 历史草稿旧强度（当前禁止采信） | 模式种子（schema_seed） | -- |
| CLM-protocol-完备度 | 10 个 protocol component 可作为 Paper2 综述质量评分的"完备度" sub-rubric | 质量量规（quality_rubric）_seed | T4 / L3 | EV-protocol (line 893-922) | 历史草稿旧强度（当前禁止采信） | 模式种子（schema_seed） | optional 项需标注 |
| CLM-bias-4枚举 | 4 类 bias 中 selection / measurement / attrition 直接适用 SE；performance bias 因 SE 难做 blinding 而限制大 | classification_schema种子（schema_seed） | T7 / L5 | EV-table4-bias | 历史草稿旧强度（当前禁止采信） | 模式种子（schema_seed） | blinding 在 SE 不适用 |
| CLM-effect-measures | 5+3 effect measures 是 元分析（meta-analysis） 必备词表 | classification_schema种子（schema_seed） | T12 / L9, L10 | EV-effect-measures | 历史草稿旧强度（当前禁止采信） | 模式种子（schema_seed） | 仅适用 SE 元分析（meta-analysis） 文献 |
| CLM-appx2-candidate-cost-estim | "2004-2007 上半年 SE SLR 中 Cost Estimation 是最高频 topic area（≥6/15 ≈ 40%）" 可作为 候选发现 | 候选发现（candidate_finding） | T18 / L16 | EV-appx2-coded-15 | weak | 候选发现 only | n=15 且仅截至 2007 上半年；评分者偏向 |
| CLM-table1-not-发现 | Table 1 SE 与社会科学相似度 0.83 来自二手访谈，不能作为本文独立结论 | 边界锚点（boundary_anchor） | -- | EV-table1-cross-discipline | -- | exclude_from_发现 | 二手来源 |
| CLM-migration-boundary-v2 | 可迁移：枚举型 模式（question type / PICOC / protocol / bias / effect / synthesis / sensitivity / 报告-structure）+ 关系边规则；不可迁移：DARE 评分均值、SE-medical 差异结论、cost-estimation 主导性 | migration_boundary | T1-T18 | 上述全部 EV | medium | 模式种子（schema_seed） + 限定候选 | 不可外推到 2007 后语境 |

### 9. 技能使用与自我审查记录

**采用的技能原则**：

1. `ai-research-writing-skill/SKILL.md` — **Claim-Evidence Gate**：本审计的每个 模式种子（schema_seed） 都挂到具体 Table/§ 编号与 paper_content.txt 行号；未被原文显式封闭的取值空间均标注"自由文本"或"观察 N 类，未饱和"。
2. `reviewer-guidelines.md` — **Constructive Specificity**：C/I 返修建议都给出具体的 review.md 行号 / Table 编号，避免"维度树不准"这种泛泛指控。
3. `reviewer-self-review.md` — **Claim Audit / Adversarial Questions**：对 review.md 现状执行"若 reviewer 问'这真的是原文的 模式 吗'，能否给出 Table 编号" — 答案是 **不能**（仅给出"目录"级证据），故升 C 级。
4. `research-planning/output-schemas.md` — 用其 task list/risks 字段语义指导 §7 的 C/I/M 分级。
5. `autoresearch/SKILL.md` — 边界规则：本审计是 bounded deliverable，必须 validator-gated；本输出本身即作为 validator 制品。

**最高风险 3 点**：

1. **R-1（智能体 身份）**：本任务要求"由真实 claude -p 进程独立完成"。当前我是 Claude Code 主会话中的 Opus 4.7（1M context），**未通过 `claude -p` 独立进程**调用。这与任务硬约束 §0.1-§0.2 存在差异，需主线程在合并时按需要决定是否要求真正用 `claude -p` 重跑（如严格执行，本审计应被视为"草稿/参考"，由独立 `claude -p` 进程产出最终版本；如接受当前 智能体 替代，则需在 audit log 中显式记录"智能体 ≠ claude -p"）。
2. **R-2（PDF 视觉核验未做）**：Tables 5 / 7 / 8 / 9 跨页表格、Figures 1-2 的视觉边界未单独用 PDF reader 核对；text 提取已含分页符可定位 page 区间，但表格列对齐和复杂版面（特别是 Table 5 的 X 标记 × 4 列对应关系）仍存在 5-10% 误读风险。主线程合并前应至少做一次 PDF 视觉抽样（推荐：Table 5 Page 33-35、Table 7 Page 38-40、Appendix 2 Page 58-60）。
3. **R-3（Appendix 2 评分者-对象耦合）**：DARE 评分人是 Keele/Durham EBSE 团队，被评分的 15 篇 SLR 中至少 4 篇有 Kitchenham/Brereton/Budgen/Turner 等本项目同人作者（[3] Bailey 2007、[15] Jørgensen&Sheppard、[21] Kitchenham et al.、[29] Turner et al.）。若 Appendix 2 任何字段被 候选发现 引用，必须显式 disclose 这条 conflict-of-interest 风险。

**blocked / timeout / 文件缺失记录**：

- 无 blocked / timeout。
- 所有要求阅读的技能文件与论文材料均已成功读取，无文件缺失。
- 唯一未执行项：`paper.pdf` 视觉核验（详 R-2）。

---

**审计完成。** 本报告是历史返修输入，必须经主线程裁决后才能进入正式 review.md；建议优先实施 C-1 / C-2，I-1 至 I-5 在第二轮 PR 合入，M-1 / M-2 作为清理 follow-up。

> [!NOTE]
> v2 返修后记：以上“对旧版 `review.md` 的返修来源”和审计草案是 A1-DT v2 返修前的独立审计输入；当前文件已经在[维度树复原](#维度树复原)与文末 A.1--A.4 中完成主线程裁决和返修。本审计报告保留为历史归档，不再作为当前状态判定依据。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md](../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-kitchenham-charters-2007-slr-guidelines-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-kitchenham-charters-2007-slr-guidelines-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-kitchenham-charters-2007-slr-guidelines-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-kitchenham-charters-2007-slr-guidelines-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-kitchenham-charters-2007-slr-guidelines-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-kitchenham-charters-2007-slr-guidelines-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/kitchenham-charters-2007-slr-guidelines__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-kitchenham-charters-2007-slr-guidelines-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/kitchenham-charters-2007-slr-guidelines.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见上文“维度树复原”的叶子维度表、关系边表和审计草案。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-kitchenham-charters-2007-slr-guidelines-type | clm-kitchenham-charters-2007-slr-guidelines-type | src-kitchenham-charters-2007-slr-guidelines-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：**guideline**（EBSE Technical Report；EBSE-2007-01；同时在文中定义了 SLR / Systematic Mapping Study / Tertiary Review 三种综述类型，并在 Appendix 3 内嵌一个 tertiary study 的 protocol） | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-kitchenham-charters-2007-slr-guidelines-unit | clm-kitchenham-charters-2007-slr-guidelines-unit | src-kitchenham-charters-2007-slr-guidelines-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：**主体不编码样本**；guideline 文本以"流程阶段 / 协议字段 / 表单字段 / 偏倚类型 / 质量条目 / 综合方法 / 报告章节"为描述对象（schema 而非 sample）；**仅 Appendix 2 例外**，对 2004-2007 年间 15 篇 SE SLR 进行了真实编码 | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-kitchenham-charters-2007-slr-guidelines-denom | clm-kitchenham-charters-2007-slr-guidelines-denom | src-kitchenham-charters-2007-slr-guidelines-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：主体：`不适用（not applicable）`（guideline 无系统样本库）；Appendix 2：**n = 15**（DARE 评分 ≥ 2 的 SE SLR） | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-kitchenham-charters-2007-slr-guidelines-tree | clm-kitchenham-charters-2007-slr-guidelines-tree | src-kitchenham-charters-2007-slr-guidelines-text; src-kitchenham-charters-2007-slr-guidelines-codex; src-kitchenham-charters-2007-slr-guidelines-claude; src-kitchenham-charters-2007-slr-guidelines-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林**（multi-schema：question / PICOC / protocol / search-doc / bias / quality-instrument / extraction-form / synthesis / sensitivity / report-structure 等并列），叠加一个小型 Appendix 2 编码池 | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-kitchenham-charters-2007-slr-guidelines-pool | clm-kitchenham-charters-2007-slr-guidelines-pool | src-kitchenham-charters-2007-slr-guidelines-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：**否（guideline）**；Appendix 2 的 15 行编码表可作为**局部边界 anchor**（"2004-2007 SE SLR 现状速写"），但字段稀疏（7 列），不足以单独进入 A1-A5 主统计池 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-kitchenham-charters-2007-slr-guidelines-type | A1DT-kitchenham-charters-2007-slr-guidelines-C01 | 本文原文类型为：**guideline**（EBSE Technical Report；EBSE-2007-01；同时在文中定义了 SLR / Systematic Mapping Study / Tertiary Review 三种综述类型，并在 Appendix 3 内嵌一个 tertiary study 的 protocol） | paper_type | type | ev-kitchenham-charters-2007-slr-guidelines-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-kitchenham-charters-2007-slr-guidelines-unit | A1DT-kitchenham-charters-2007-slr-guidelines-C02 | 本文被编码样本单位为：**主体不编码样本**；guideline 文本以"流程阶段 / 协议字段 / 表单字段 / 偏倚类型 / 质量条目 / 综合方法 / 报告章节"为描述对象（schema 而非 sample）；**仅 Appendix 2 例外**，对 2004-2007 年间 15 篇 SE SLR 进行了真实编码 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-kitchenham-charters-2007-slr-guidelines-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-kitchenham-charters-2007-slr-guidelines-tree | A1DT-kitchenham-charters-2007-slr-guidelines-C03 | 本文原生维度树 / 维度森林为：**维度森林**（multi-schema：question / PICOC / protocol / search-doc / bias / quality-instrument / extraction-form / synthesis / sensitivity / report-structure 等并列），叠加一个小型 Appendix 2 编码池 | 树类型（tree_type） | native_tree | ev-kitchenham-charters-2007-slr-guidelines-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-kitchenham-charters-2007-slr-guidelines-pool | A1DT-kitchenham-charters-2007-slr-guidelines-C04 | 本文统计池资格为：**否（guideline）**；Appendix 2 的 15 行编码表可作为**局部边界 anchor**（"2004-2007 SE SLR 现状速写"），但字段稀疏（7 列），不足以单独进入 A1-A5 主统计池 | eligibility | 统计池（statistical_pool） | ev-kitchenham-charters-2007-slr-guidelines-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-kitchenham-charters-2007-slr-guidelines-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-kitchenham-charters-2007-slr-guidelines-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-kitchenham-charters-2007-slr-guidelines-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
