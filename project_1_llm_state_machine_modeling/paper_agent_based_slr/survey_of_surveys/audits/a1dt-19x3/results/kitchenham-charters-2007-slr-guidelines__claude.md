# kitchenham-charters-2007-slr-guidelines · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：是。读取路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`；`references/reviewer-self-review.md` 已通过目录列举确认存在并按 SKILL.md "Loading Strategy" 按需检索（reviewer mode）。
- 是否读取 `$research-planning`：是。读取路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`；`references/planning-prompts.md` 通过目录列举确认存在。
- 是否读取 `$oh-my-codex:autoresearch`：是。读取路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。
- 是否完整阅读 `paper_content.txt`：是。3091 行全文逐段阅读，重点覆盖目录（pp.i--iii）、Executive Summary、Glossary（pp.vi--vii）、§1 Introduction、§2 SLR 类型与变体（含 mapping、tertiary）、§3 EBSE in Context（Table 1）、§4 Review Process 三阶段、§5 Planning（含 §5.3.1 6 类 question types、§5.3.2 PICOC、§5.4 protocol components、§5.6 lessons learned）、§6.1 Identification of Research（含 Table 2 Search documentation、7 个 electronic sources、publication bias）、§6.2 Study Selection（Cohen Kappa、test-retest）、§6.3 Quality Assessment（Table 3 quality definitions、§6.3.1 hierarchy of evidence、Table 4 4 类 bias、§6.3.2 generic/specific items、4 阶段 study stages）、§6.4 Data Extraction（form 设计、标准字段、Table 7 完整抽取表样例、multi-publication、missing data）、§6.5 Data Synthesis（descriptive、quantitative effect measures: Odds/Risk/OR/RR/ARR/Mean diff/WMD/SMD、Figure 1 forest plot、Noblit & Hare 3 种 qualitative 综合：reciprocal/refutational/line-of-argument、qual+quant 综合、sensitivity analysis、§6.5.7 funnel plot/publication bias）、§7 Reporting（dissemination、Table 8 完整报告结构、evaluating reports、IST 接受性说明）、§8 Mapping Studies、§9 PhD light version、Appendix 1 Table 9 6 源 process 交叉表、Appendix 2 高质量 SLR 名录及 schema（Author/Date/Title/Reference/Topic type/Topic area/Quality score）、Appendix 3 Tertiary protocol（RQ、Sources、Inclusion/Exclusion、Primary study selection、Quality Assessment 4 DARE 评分细则、Data Collection 10 字段、Data Analysis 4 RQ 对应分析）、§10 References（29 条）。
- 是否核对 `paper.pdf`：否。本轮以全文文本级审计为主，仅在 `paper_content.txt` 提取出现明显断裂（如 Table 4/5/6/8/9 多列表头与行内容因 PDF 提取错位）时回到原文锚定；Table 5 量化质量 checklist 中 X/空白列字符已部分还原。复杂表格的版面级校验（精确页码、表格栏宽、Figure 1/2 视觉）留给 A2a，符合 GUIDE.md §6.3.7 的 A1-DT 证据强度边界。

## 2. 原文真实结构复原

### 2.1 文献身份与单位对象

EBSE-2007-01 是 **方法学 guideline / 技术报告**，不是 SLR/SMS/tertiary study 的执行样本。其单位对象是 "SLR 方法学规则 / protocol 字段 / quality checklist 条目 / 报告结构条目 / 跨 SR guideline 流程步骤"，不是 primary studies。

### 2.2 原文 RQ / 目标 / 贡献声明

- Executive Summary（p.vi）：**The objective of this report is to propose comprehensive guidelines for systematic literature reviews appropriate for software engineering researchers, including PhD students**.
- §1 Introduction（p.1）：明确说"goal of this document is to introduce the methodology for performing rigorous reviews of current empirical evidence to the software engineering community"；明确两点不覆盖：meta-analysis 细节、不同 question types 对 procedure 的影响。
- 贡献声明：基于 3 套医学/社科 SR guideline（Cochrane Handbook、CRD、Australian NHMRC、Petticrew & Roberts、Fink、Hart）做 SE-adapted guideline；以 EBSE 项目经验补充。
- 因此 **本文没有"SLR 研究问题"，只有 guideline objective + adaptation principles**。该差异在原 review.md 快速卡片已识别，但 dim-root 的维度树并没有显式区分 "guideline objective" 与 "research question" 这两种树根。

### 2.3 原文方法流程与三阶段结构

原文 §4 明确把 review 流程归为 **3 个 macro 阶段**：

1. **Planning the Review** = §5（need / commissioning / RQ / protocol dev / protocol eval / lessons）；
2. **Conducting the Review** = §6（identification of research / study selection / quality assessment / data extraction / data synthesis）；
3. **Reporting the Review** = §7（dissemination strategy / formatting main report / evaluating report / lessons）。

每个 macro 阶段下都有 lessons learned 子节，且 Appendix 1 / Table 9 提供 **6 源 guideline 的 process step 交叉对照表**，是原文显式跨方法学比较的 schema。

### 2.4 原文显式 extraction form / schema / taxonomy / coding scheme / roadmap / quality rubric

下面列出原文中所有具备"维度树叶子"地位的显式 schema：

1. **§5.3.1 Question Types**（医学 6 类 → SE 5 类适配）：
   - 6 medical: Effect of intervention / Frequency or rate / Diagnostic test / Aetiology & risk / Predictability / Economic value；
   - 5 SE-adapted：technology effect / project factor frequency / cost & risk identification / technology impact on models / cost-benefit analysis。

2. **§5.3.2 PICOC**（Population / Intervention / Comparison / Outcome / Context）+ 第六维 **Experimental designs**。每维都有 SE-specific 取值示例（如 Population 5 种角色 / category / domain / industry group；Outcome 强调避免 surrogate measures；Context 包括 academia/industry × practitioner/student × small/large scale）。

3. **§5.4 Review Protocol Components**（9 项）：Background、RQ、Search strategy、Study selection criteria、Study selection procedures、Quality assessment checklists & procedures、Data extraction strategy、Synthesis、Dissemination strategy、Project timetable。

4. **§5.5 protocol 内部一致性 3 条**：search strings ↔ RQ、data ↔ RQ、analysis ↔ RQ。

5. **§5.6 lessons learned 4 条**：pre-review mapping / expect revision / team active in protocol / pilot essential；+ Staples & Niazi 关于 narrow RQ。

6. **§6.1 Search**：
   - 4 种搜索行为（preliminary / trial / known-study check / expert consult）；
   - **Table 2 Search process documentation schema**：5 类 Data Source（Digital Library / Journal Hand Searches / Conference proceedings / Efforts to identify unpublished studies / Other sources）× 各自字段（database name / strategy / date / years 等）；
   - **7 个 electronic sources 枚举**（IEEExplore / ACM DL / Google Scholar / Citeseer / Inspec / ScienceDirect / EI Compendex）+ Springer / Scopus 补充；
   - 4 条 publication bias mitigations（grey literature / conference proceedings / contact experts / statistical analysis）。

7. **§6.2 Study Selection**：
   - 实务级 inclusion/exclusion criteria 8 维（Language / Journal / Authors / Setting / Participants / Research Design / Sampling method / Date of publication）；
   - **Cohen Kappa**（[9]）用作 inter-rater reliability，且要求文档化 initial Kappa value；
   - test-retest 协议、PhD 单 researcher 替代策略。

8. **§6.3 Study Quality Assessment**：
   - 5 种 quality data 用途（细化 inclusion / 解释结果差异 / 加权合成 / 解释 strength of inferences / 指导未来研究）；
   - **Table 3 Quality concept definitions**：Bias / Internal validity / External validity（含 Synonyms 与 SE-adapted Definition）；
   - §6.3.1 **Hierarchy of Evidence**（SR/RCT 顶 → quasi-experiment / expert opinion 底）+ Petticrew & Roberts 的修正（design-question 匹配优先于 hierarchy）；
   - **Table 4 Types of Bias**：Selection / Performance / Measurement / Attrition × Synonyms / Definition / Protection mechanism；
   - generic items（按 study design：survey / experiment / qualitative）+ specific items（按主题）；
   - 4 阶段 study stages：Design / Conduct / Analysis / Conclusions；
   - **Table 5 Quantitative Quality Checklist**（~40 条 question × 4 study type 列：Empirical 通用 / Correlation 观察 / Surveys / Experiments × Source 引用列）—— 这是一张**完整可执行的字段表**，按 Design / Conduct / Analysis / Conclusions 4 段组织；
   - **Table 6 Qualitative Checklist**（18 条 numbered question + Source 引用列）；
   - §6.3.3 quality data 两种使用方式（pre-selection vs. analysis-stage）；
   - §6.3.4 quality assessment 的 4 类局限。

9. **§6.4 Data Extraction**：
   - 标准字段：Reviewer name / Date / Title-Authors-Journal-Pub details / Notes；
   - **Table 7 Data Collection Form（完整 30+ 字段）**：Data Extractor / Data Checker / Study Identifier / Application domain / Database name / Number of projects（总 / cross-company / within-company）/ Size metric (FP/LOC/Others) / Number of companies / Number of countries / Quality controls / Accuracy measures / Cross-company model 子表（Technique / Best model selection / Transformations / Variables / Cross-validation method / Baseline comparison / Benchmark measures）/ Within-company model 子表（同 7 项）/ Comparison 子表（accuracy results）/ Data Summary（effort min/max/mean/median × size 同）；
   - data extraction procedures 4 种（2-researcher independent / data extractor + data checker / random sample double-coded / PhD test-retest）；
   - multiple publications 处理、unpublished/missing/manipulated data 处理。

10. **§6.5 Data Synthesis**：
    - 3 种 synthesis：Descriptive (narrative) / Quantitative (meta-analysis) / 混合；
    - quantitative 部分要求 4 类 tabular items（sample size / effect size + SE / mean diff + CI / units）；
    - **Binary outcome effect measures 5 类**：Odds / Risk / Odds Ratio (OR) / Relative Risk (RR) / Absolute Risk Reduction (ARR)，每类有判读规则；
    - **Continuous outcome effect measures 3 类**：Mean difference / Weighted mean difference (WMD) / Standardised mean difference (SMD)；
    - **Forest plot（Figure 1）** 作为 quantitative presentation 标准；
    - **Qualitative synthesis 3 种**（Noblit & Hare）：Reciprocal translation / Refutational synthesis / Line of argument synthesis；
    - §6.5.5 qual + quant 混合综合 3 步骤（separate → integrate → cross-study）；
    - §6.5.6 Sensitivity analysis 5 类（high-quality only / study type / data extraction agreement / experimental method / 描述性下排序）；
    - §6.5.7 **Funnel plot（Figure 2）** 用于 publication bias 检测。

11. **§7 Reporting**：
    - 6 种 dissemination 渠道；
    - **Table 8 Structure and Contents of Reports**（完整层级）：Title* / Authorship* / Executive Summary or Structured Abstract*（Context / Objectives / Methods / Results / Conclusions）/ Background / Review questions / Review Methods（Data sources & search / Study selection / Study quality / Data extraction / Data synthesis）/ Included and excluded studies / Findings（Description / Quantitative summaries / Meta-analysis / Sensitivity analysis）/ Discussion（Principal findings / Strengths & Weaknesses / Meaning of findings / Practical implications）/ Conclusions（Recommendations / Unanswered questions）/ Acknowledgements* / Conflict of Interest / References & Appendices；
    - §7.3 evaluating reports（DARE / Greenhalgh checklists 复用）；
    - §7.4 reporting lessons（Brereton：record decisions / longer-paper challenge；Staples & Niazi：record protocol deviations；IST 接受 SLR）。

12. **§8 Systematic Mapping Studies**：5 条与 SLR 的关键差异（broader RQ / less-focussed search / classification-style extraction / summary-only analysis / 受限 dissemination）。

13. **§9 Final remarks PhD light version**：8 个最小步骤。

14. **Appendix 1 / Table 9**：6 SR guideline source（Berkeley SR Group / Australian NHMRC / Cochrane / CRD / Petticrew & Roberts / Fink）的 process step 跨表对照——这是 **跨 guideline 维度对齐 schema**。

15. **Appendix 2 SE SLR 名录 schema**：Author / Date / Title / Reference Details / **Topic type**（Technology evaluation / Research trends / Technology）/ **Topic area** / **Quality score**（DARE 0--4）—— 这是已经被原文应用过的真实 catalog schema，对 A2a 极其重要。

16. **Appendix 3 Tertiary Protocol** 完整字段：Background / **Research Questions（4 个）**/ Sources to be Searched（13 venues + responsible researcher）/ Specific researchers contacted / Inclusion criteria（SLR + MA + 时间窗）/ Exclusion criteria（4 条）/ Primary study selection process / **Quality Assessment**（DARE 4 题，每题 Y/P/N 评分细则）/ **Data Collection 10 字段**（source / year / classification {type, scope} / topic area / authors+affiliation / RQ / EBSE reference / practitioner guidelines / number of primary studies / summary / quality score）/ Data Analysis（4 RQ ↔ 4 分析路径，含 quality-vs-time、guidelines-reference 对照）/ Dissemination plan。

### 2.5 原文如何从字段形成 finding / gap / recommendation

由于本文是 guideline，**不形成领域 finding**，但形成：

1. **方法学 finding**：通过 EBSE 项目（Brereton et al. 2007 [5]、Staples & Niazi [27]）的 reflective lessons 形成 11 条 lessons learned（散布在 §5.6 / §6.1.5 / §6.4.6 / §6.5.8 / §7.4）。
2. **跨学科适应 finding**：Table 1（SE 与 6 学科相似度对比）→ 结论 "SE 更接近社科而非医学"，并据此引入 social-science guidelines。
3. **方法学 recommendation**：§9 PhD light version；Appendix 3 protocol example。
4. **roadmap action**：§6.1.1 "SE researchers need to develop and publish pre-packaged search strategies"、§6.1.5 "current SE search engines are not designed to support SLRs"。

这些都是 **方法学候选 finding**，按 GUIDE §6.3.5 默认降级为 `boundary_anchor` / `schema_seed`，不进入主统计池——这部分当前 review.md 处理正确。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确 | dim-root 写作"研究目标 / RQ / 贡献声明"是泛接口；未显式区分原文是 guideline objective 而非 SLR RQ；未把 6 SR source adaptation、social-science alignment、PhD-targeted scope 写入根节点定义。 | I |
| 主干分支是否覆盖原文 schema | 严重不足 | 主干 b1--b5 把原文 3 macro 阶段（Planning / Conducting / Reporting）压成 5 个平面分支；§5 Planning 与 §6.1 Identification 合并为 b1+b2；§6.2 Study Selection 与 §6.3 Quality 合并为 b4；§6.5 Data Synthesis 完全缺失独立分支；§7 Reporting 与 threats 合并为 b5；Appendix 1 跨 guideline 6 源对照、Appendix 2 SE SLR catalog、Appendix 3 tertiary protocol 完全未出现在主干。 | C |
| 叶子维度是否足够具体 | 严重不足 | "叶子维度表"6 个 leaf 是项目通用接口（scope/corpus/taxonomy/method/evidence/finding），不是原文叶子；原文有 9 个显式表格（Table 1--9）、2 张图（Figure 1--2）、3 个 Appendix，至少应映射 30+ 候选叶子（6 question types、PICOC 6 维、Table 2 documentation 5 类、7 electronic sources、Table 3 quality 3 概念、Table 4 4 类 bias、Table 5 ~40 个量化 quality items × 4 study types、Table 6 18 个 qualitative items、Table 7 30+ extraction fields、Table 8 报告结构 ~20 节、Table 9 6 源对照、binary/continuous effect measures 8 类、Noblit-Hare 3 类 qualitative synthesis、sensitivity 5 类、Appendix 2 catalog 6 字段、Appendix 3 protocol 10+ 字段）；"原文模式候选叶子映射"只有 4 行，覆盖极度稀疏。 | C |
| 取值空间是否可执行 | 不足 | 现有 6 leaf 取值空间是模板化短语（"自由文本加 RQ 引用"等），未引用原文具体类别集合；Table 4 4 类 bias、Table 5 4 列 study type、binary effect measures 5 类等是 **完整可枚举封闭集合**，应直接写出而非泛化为"层级枚举/自由文本"。 | I |
| 关系边是否缺失 | 是 | 原文 §5.5 protocol 内部一致性（search ↔ RQ、data ↔ RQ、analysis ↔ RQ）是显式关系约束；Table 4 bias × protection mechanism、Table 5 question × study type、Table 9 process step × source 都是关系型 schema；review.md 未列出任何关系边。 | I |
| 统计用途 / 分母是否正确 | 通过 | 维度树整体降级为 schema_seed / 不进入主统计池，与 GUIDE §6.3.5（guideline 默认）一致；分母语义写为 `not_applicable`，合理。 | 通过 |
| 候选 finding 路径是否完整 | 不足 | finding-boundary 路径仅描述"discussion → 候选发现 → 研究者裁决"通用接口，未列出原文具体候选 finding：Table 1 学科相似度结论、Brereton 11 条 lessons learned、§6.1.5 SE search engine roadmap action、§6.1.1 pre-packaged search strategy roadmap、§9 PhD light heuristics、Appendix 3 quality-vs-time / guidelines-reference 分析路径等都未入候选发现台账。 | I |
| A.1--A.4 证据链是否足够 | 不足 | A.1 入口完整（3 源）；A.2 仅 4 行 evidence，原文 9 表 + 2 图 + 3 appendix 至少应有 9--15 行独立证据（Table 2、Table 3、Table 4、Table 5、Table 6、Table 7、Table 8、Table 9、Appendix 2、Appendix 3、Figure 1 forest plot、Figure 2 funnel plot 各应独立挂证据并指向具体支撑节点）；A.3 9 条结论全部 weak / schema_seed 合理，但支撑对象只回链到 6 通用叶子，未回链原文表格；A.4 仅 2 条复验项，未把 9 表的视觉核验逐表入账。 | I |
| 是否存在可能误导 A2a 的强主张 | 否 | 全部标记 `not_verified` / `weak` / `schema_seed`；明确"不进入主统计池"；"A1-DT 叶子层口径校准"段落显式说明 6 leaf 是通用接口；这一处理符合 §6.3.7 边界，未出现误导。 | 通过 |

## 4. 建议维度树骨架

按 GUIDE §6.3.2--§6.3.5 与原文结构，推荐 **更忠实于原文** 的维度树骨架如下（仍以 schema_seed / not_verified 处理，不强求 PDF 精核）：

### 4.1 根节点

- 名称：EBSE-2007-01 系统综述方法学 guideline
- 单位对象：guideline 元素（protocol 字段 / quality checklist item / 报告结构条目 / process step / SE-adaptation rationale）
- 树类型：**方法学 guideline 树**，辅助类型：**报告 / 质量 rubric 树** + **跨 guideline 对照 schema**
- 显式标注：本文为 **objective + adaptation principles**，无 SLR RQ，不可与执行 SLR 的 RQ pattern 混算

### 4.2 推荐主干分支（按原文 §4 三阶段 + 跨 guideline 对照）

| 主干标识 | 名称 | 服务的 RQ / objective | 原文锚点 |
|---|---|---|---|
| b-planning | Planning the Review | guideline objective / SE-adaptation | §5 全章 |
| b-conducting-search | Conducting · Identification of Research | rigorous search strategy | §6.1、Table 2、7 sources |
| b-conducting-selection | Conducting · Study Selection | inclusion/exclusion + reliability | §6.2、Cohen Kappa |
| b-conducting-quality | Conducting · Quality Assessment | bias / validity control | §6.3、Table 3/4/5/6 |
| b-conducting-extraction | Conducting · Data Extraction | data form rigor | §6.4、Table 7 |
| b-conducting-synthesis | Conducting · Data Synthesis | descriptive + quantitative + qualitative + sensitivity + publication bias | §6.5、Figure 1/2 |
| b-reporting | Reporting the Review | dissemination + report structure + evaluation | §7、Table 8 |
| b-mapping | Mapping Study Variant | broad-coverage scoping | §8 |
| b-phd-light | PhD Light Version | single-researcher operationalization | §9 |
| b-cross-guideline | Cross-guideline Process Alignment | adaptation rationale | Appendix 1、Table 9 |
| b-se-slr-catalog | SE SLR Catalog Schema | 已应用的高质量 SLR 目录字段 | Appendix 2 |
| b-tertiary-protocol | Tertiary Review Protocol Template | 完整 protocol 实例 | Appendix 3 |

### 4.3 推荐叶子维度（节选，按原文优先级）

每个叶子均建议以 **完整枚举** 取值空间冻结种子；缺失值统一写 `not_applicable_to_guideline` 或 `待 A2a 表图精核`。下面只列对 A2a 最有价值的 10 个，完整 30+ 叶子留给修复 PR 一次性补齐：

1. `leaf-question-types`（父 b-planning）：6 medical + 5 SE-adapted question types（完整枚举）。
2. `leaf-picoc`（父 b-planning）：Population / Intervention / Comparison / Outcome / Context + Experimental designs（封闭 6 维）+ 各维 SE 取值示例。
3. `leaf-protocol-components`（父 b-planning）：9 项 protocol 字段（封闭枚举）。
4. `leaf-search-documentation`（父 b-conducting-search）：Table 2 的 5 类 Data Source × 字段（关系边表）。
5. `leaf-electronic-sources`（父 b-conducting-search）：7 sources 枚举 + 2 supplement（封闭 9 项 + 可扩展）。
6. `leaf-quality-bias-types`（父 b-conducting-quality）：Table 4 4 类 bias × {Synonyms, Definition, Protection mechanism}（关系边表）。
7. `leaf-quality-checklist-quant`（父 b-conducting-quality）：Table 5 约 40 个 question × 4 study type × Source（关系边表 / 矩阵）。
8. `leaf-quality-checklist-qual`（父 b-conducting-quality）：Table 6 18 numbered questions（封闭枚举）。
9. `leaf-extraction-form`（父 b-conducting-extraction）：Table 7 30+ 字段（封闭枚举 + 子表）。
10. `leaf-report-structure`（父 b-reporting）：Table 8 完整层级（封闭层级枚举）。

补充必备的关系边：

| 关系边 | 源 | 关系类型 | 目标 |
|---|---|---|---|
| `edge-protocol-internal-consistency` | leaf-protocol-components | aligns_with | leaf-question-types / leaf-search-documentation / leaf-extraction-form / leaf-synthesis-methods |
| `edge-bias-protection` | leaf-quality-bias-types | mitigated_by | Table 4 各行 Protection mechanism |
| `edge-checklist-study-type` | leaf-quality-checklist-quant | applies_to | Empirical/Correlation/Survey/Experiment |
| `edge-process-cross-source` | b-cross-guideline | aligns_step_of | 6 SR sources（Berkeley/NHMRC/Cochrane/CRD/P&R/Fink） |

如果当前 review 仅保留 6 通用叶子（scope/corpus/taxonomy/method/evidence/finding），就**不足以**让 A2a 复原原文 schema：原文 9 张可执行表格的字段全部丢失。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支重排 | 维度树结构 + 根问题映射表 | 把 b1--b5 重组为 §4.2 推荐的 12 个主干（Planning / Search / Selection / Quality / Extraction / Synthesis / Reporting / Mapping / PhD-light / Cross-guideline / SE-SLR-catalog / Tertiary-protocol）；至少恢复 Synthesis、Mapping、Cross-guideline、Appendix 2/3 这 4 大缺失分支 | paper_content.txt §4 / §6.5 / §8 / §9 / Appendix 1--3 | C |
| 原文模式候选叶子表扩充 | "原文模式候选叶子映射（A1 种子）" | 由当前 4 行扩到 ≥ 30 行；至少补齐 question types / PICOC / protocol components / Table 2 documentation / 7 electronic sources / Table 3 quality concepts / Table 4 bias / Table 5 quant checklist / Table 6 qual checklist / Table 7 extraction form / 5 binary effect measures / 3 continuous effect measures / Noblit-Hare 3 qualitative synthesis / sensitivity 5 类 / Table 8 报告结构 / Table 9 cross-source / Appendix 2 catalog / Appendix 3 tertiary 10 字段 | paper_content.txt §5.3.1/§5.3.2/§5.4/§6.1/§6.3.2/§6.4.2/§6.5.2/§6.5.3/§6.5.4/§6.5.6/§7.2/Appendix 1--3 | C |
| 叶子取值空间收紧 | 叶子维度表 + 候选叶子表 | 凡原文给出封闭枚举的字段（6 question types、PICOC 6 维、Table 4 4 类、Table 6 18 项、effect measures 8 类、Noblit-Hare 3 种、Table 8 节级）应在取值空间列写出完整枚举或显式回链原文表号，而不是统一写"层级枚举 / 自由文本" | paper_content.txt 各表 | I |
| 引入关系边表 | "关系边表"（GUIDE §6.3.4 要求） | 新建 A1-DT 关系边表，至少记录 §4.3 列出的 4 条关系边；尤其 protocol 内部一致性约束、bias × protection、checklist × study type、cross-guideline process 对齐 | paper_content.txt §5.5/§6.3.2/Table 4/5/Table 9 | I |
| 根节点定义补全 | 一句话结论 / 根问题映射表 | 显式声明：本文是 guideline / 技术报告，objective 而非 RQ；以 6 SR sources 为来源；SE-adaptation 基于社科取向（Table 1 学科相似度）；目标受众包括 PhD 单 researcher | paper_content.txt Executive Summary p.vi、§1.1、§3 Table 1、§9 | I |
| 候选 finding 台账扩充 | 统计与候选发现链路 / leaf-finding 行 | 把 11 条 Brereton/Staples lessons、§6.1.1/§6.1.5 roadmap action（pre-packaged search strategy、SE search engine 不足）、§9 PhD light 8 步骤、Table 1 跨学科结论、Appendix 3 quality-vs-time 与 guidelines-reference 分析路径作为候选发现条目入账，全部标 `boundary_anchor` / `schema_seed` | paper_content.txt §5.6/§6.1.5/§6.4.6/§6.5.8/§7.4/§9/Appendix 3 | I |
| A.2 证据账本细化 | A.2 维度树证据账本 | 由 4 行扩到 ≥ 9 行：Table 2/3/4/5/6/7/8/9 每表至少 1 行独立证据，Figure 1（forest plot）与 Figure 2（funnel plot）各 1 行，Appendix 2 / Appendix 3 各 1 行；每行的"支撑的维度节点"必须回链具体新主干 / 叶子而非通用接口 | paper_content.txt 各表 | I |
| A.4 视觉核验清单补全 | A.4 本地复验命令与人工核验清单 | 把 Table 2/3/4/5/6/7/8/9 每张表与 Figure 1/2 列为独立 `needs_manual_check` 行；A2a 必须按表号逐张回 PDF 核验 | paper_content.txt p.16/p.20/p.21--22/p.25--27/p.27/p.30--32/p.42--43/p.49 邻近 | M |
| 标识纪律一致性检查 | 现有 b1--b5 与 leaf-* | 若采用 §4.2 新主干，原 b1--b5 / leaf-scope..finding 不应直接删除；按 GUIDE §6.3.6 在审计附录标"已废弃 + 替代证据"，保留键稳定，避免下游回链断裂 | GUIDE §6.3.6 | I |

## 6. C/I/M 结论

### C（直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性）

1. **主干分支严重错位 + 多个 macro 阶段整体缺失（Synthesis / Mapping / Cross-guideline / Appendix 2 catalog / Appendix 3 tertiary protocol 全部不在树中）**。这是 Paper2 在 SLR 方法学锚点上唯一的高强度方法学 guideline 样本；如果 A2a 据当前 5 主干直接初始化字段合同，将丢失 binary/continuous effect measures、forest/funnel plot、Noblit-Hare qualitative synthesis、Table 8 完整报告结构、Table 9 跨 guideline 对照、Appendix 2/3 已被原文应用的真实 schema 这一整批 schema seed，直接影响 A2a 字段饱和度判定与后续 cross-paper synthesis pattern 复原。
2. **"原文模式候选叶子映射"仅 4 行**，原文至少有 30+ 显式叶子（含 4 张大表 + 多张分类表 + 2 张 protocol 表 + 2 张 plot）。当前粒度让 A1-DT 等同于"只确认本文有 4 类模块"，不构成可被 A2a 升级的 schema seed；这是 Paper2 把本文当作 schema seed 的核心证据池萎缩问题。

### I（实质影响维度树可用性、原文 schema 复原、证据可审计性）

1. 根节点未区分 guideline objective vs SLR RQ；SE-adaptation rationale（Table 1 跨学科相似度）未入树。
2. 叶子取值空间过度泛化，未冻结原文的封闭枚举（6 question types / PICOC / 5 binary + 3 continuous effect measures / 3 qualitative synthesis / Table 4 4 bias / Table 6 18 items / Table 8 节级）。
3. 缺失关系边表，protocol 内部一致性、bias × protection、checklist × study type、cross-guideline process 对齐 4 条关键关系全部丢失。
4. 候选 finding 台账只写通用接口，未把 11 条 lessons learned、2 条 roadmap action、PhD light 8 步骤、Table 1 跨学科结论作为候选条目入账，无法支撑 A2a 形成方法学 candidate finding。
5. A.2 证据账本只挂 1 行 `EV-002` 同时支撑 b1--b5 + 2 个 leaf，粒度过粗，按表号细化才能让 A2a 逐表精核。
6. 标识废弃纪律：若按 §4.2 重建主干，需保留旧键稳定，避免向后兼容断裂。

### M（不阻塞的清晰度 / 维护性建议）

1. A.4 视觉核验清单按 9 表 + 2 图逐项展开。
2. "维度树结构"代码块当前 b5 同时挂 leaf-evidence 与 leaf-finding，可拆为独立分支或显式说明 evidence ≠ reporting。
3. 快速结论卡片中"schema 历史观察"可一并迁出到维度树复原小节，避免与新事实源并列。

### 最终建议

**NEEDS FIX**。

降级理由：当前 `review.md` 满足 GUIDE §6.3.7 的 A1-DT 证据强度边界（全部 `not_verified` / `weak` / `schema_seed`），不破坏 Paper2 已采纳事实链；但当前维度树是 19 篇通用接口的复用，**没有完成原文 schema 复原**，"原文模式候选叶子映射"4 行无法支撑后续 A2a 把 EBSE-2007-01 作为方法学 schema seed 使用。两项 C 级问题必须在合并前修复或在 PR body 中显式记录为 follow-up，并把当前文件标注为"A1-DT 维度树骨架，原文 schema 30+ 叶子待 A2a 补全"，避免下游误把当前 6 叶子接口当成 EBSE-2007-01 的原文叶子全集。
