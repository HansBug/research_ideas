# ml4se-tertiary-study · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：是。`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并对照其 Evidence gate / Claim gate / Literature gate / Reviewer gate。`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` 由于本仓库当前会话已加载该 skill 的上层指引，未逐字 Read，但其口径（claim-evidence-engineering、reviewer 必须给出可复现证据并优先列影响学术结论的风险、self-review 必须对比真实 schema）已整合进本审计。
- 是否读取 `$research-planning`：是。已对照 `research-planning/SKILL.md` 的"先复原原文 schema 再做提取"和"避免通用 stub 冒充原文真值"两条主线。`references/planning-prompts.md` 同步指导我把审计写成"原文 schema 是什么 → review 还原到什么程度 → 缺什么"。
- 是否读取 `$oh-my-codex:autoresearch`：是，会话已加载 `oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` 的多源校验与"先逐页定位再升级结论"原则。
- 是否完整阅读 `paper_content.txt`：是。`wc -l` = 1774 行。已逐段阅读 Page 1–28 关键段落（摘要、§1 引言、§2 相关工作、§3 方法 §3.1–§3.6 全部、Table 1 关键词三组、Table 2 DARE-4、Table 3–4 全部 83 篇研究清单、§4.1 数据抽取、§4.2 RQ1 11 个 KA 子节、§4.3 RQ2 含 §4.3.1 General Recommendations 与 §4.3.2–§4.3.12、§4.4 RQ3 4 轴分类、Table 6 4 轴统计、Fig. 6 热力图、Table 7 ML 应用任务 8 类、§5 Discussion 含 Implication 1–7、§6 Threats to Validity 三轴 + Ampatzoglou 引用、§7 Conclusion and Recommendations）。未抽样阅读的部分仅为 §4.3.4–§4.3.12 后段 SE-task 级别小推荐文本与 §7 后段 practitioners 段落细节，但已掌握其字段结构。
- 是否核对 `paper.pdf`：否。本会话不具备 PDF 视觉渲染条件；但 `paper_content.txt` 含逐页 `--- Page N ---` 标记，可作为页码锚定替代，关键表/图编号（Fig. 1 Review Method、Fig. 2 Scopus 年度分布、Fig. 5 KA 年度分布、Fig. 6 KA×ML 4 轴热力图、Table 1 keywords、Table 2 DARE-4、Tables 3–4 study overview、Table 5 SWEBOK KA、Table 6 4 轴、Table 7 ML 应用任务）均能在文本流中直接定位。视觉层细节（颜色、版式微调）留待 A2a 人工 PDF 核对。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

- 显式 RQ（§3.1，paper_content.txt Page 6）：
  - **RQ1** What SE tasks have been tackled with ML techniques?
  - **RQ2** What SE knowledge areas could be better covered by ML techniques?
  - **RQ3** What ML techniques have been used in SE?
- 研究目标（§3.1 Page 5–6）：(1) 提供质量评估目录；(2) 汇总评估所有 ML4SE 二次研究；(3) 描述 ML4SE 当前研究现状；(4) 突出潜在研究机会。
- 摘要级贡献声明（Page 1）：系统收集、质量评估、汇总并分类 2009–2022 年 83 篇 reviews，覆盖 6 117 篇 primary studies；提出 ML4SE 研究挑战与行动（empirical validation/industrial studies/数据与 pipeline 文档化/工业数据共享/incremental ML）。
- 单位对象：以"secondary study"为分析单元，以 primary study 为隐含覆盖单元。

### 2.2 方法流程

整体三阶段（planning / conducting / reporting，§3 Page 6）对齐 Kitchenham & Charters 2007 guideline。

1. **Search Strategy（§3.2）**：四阶段 = automated search + manual search + backward snowballing + forward snowballing。
2. **Selection Criteria（§3.3）**：列出 IC / EC（含 taxonomies 6 项 planning characteristics、5 项排除条款）。
3. **Selection Process（§3.4）**：15 篇 sample + Cohen Kappa ≥ 0.8 + 余下 1552 篇 split-half review。
4. **Quality Assessment（§3.5）**：DARE-4 Y/P/N 评分；140→83；inter-rater 一致性 82%。
5. **Data Extraction（§3.6）**：每篇抽取 11 字段（见 §2.3）。
6. **Analysis**：按 SWEBOK V3 KAs+subareas + 4 轴 ML 分类 + 开放编码（SE tasks 1–3 个/篇）+ Qualitative Content Analysis 归并。

### 2.3 显式 extraction form / classification schema / taxonomy / coding scheme（核心 schema）

paper_content.txt Page 10–12 给出**完整 11 字段抽取表**：
1. Title and source（journal/workshop proc./conference proc./book chapter）
2. Publication year
3. Publication venue
4. Author names, institutions, countries
5. Study type（SLR / SMS / taxonomy / 等）
6. Research method（adopted guidelines）
7. Quality assessment score（DARE-4 0–4）
8. Number of primary studies
9. Application domain（SWEBOK KA + subarea + SE tasks，开放编码 1–3 个/篇）
10. Implications for further research + comments on ML in SE
11. Employed ML techniques

**SWEBOK V3 KAs 分类轴（Table 5，Page 15）**：封闭枚举 11 个 KA + 子领域：SW Quality / SW Testing / SE Process / SE Management / SW Requirements / SW Maintenance / SW Design / SW Configuration Management / SE Models & Methods / SE Professional Practice / Engineering Foundations。每 KA 进一步分子领域（如 SW Quality → Practical Considerations / Fundamentals / Management Processes 等）。

**ML 4-轴分类 scheme（§3.6 Page 11–12，Table 6 Page 23）**：
- Axis 1 **Role of AI in SE**（封闭 3 类）：SBSE / Fuzzy and probabilistic / Classification, learning and prediction。
- Axis 2 **Supervision**（封闭 4 类）：supervised / unsupervised / semi-supervised / reinforcement。
- Axis 3 **Incrementality**（封闭 2 类）：online/incremental / batch/offline。
- Axis 4 **Generalizability**（封闭 2 类）：instance-based / model-based。

**ML Application Task taxonomy（Table 7 Page 24）**：8 类 = Classification/Clustering/Regression、Pattern Discovery、Dimensionality Reduction、Information Retrieval、Stochastic Search、Generation、Hybrid、Miscellaneous。这是显式分类轴，不是自由文本。

**Search keyword 三组结构（Table 1 Page 7）**：SE 组（13 个，源自 SWEBOK V3 KAs 去除 3 项 Foundations）+ ML 组（27 个，源自 ACM CCS ML 概念调研）+ Secondary Studies 组（35 个 = Kitchenham 15 + 自构 20）。

**DARE-4 quality rubric（Table 2 Page 10）**：4 准则 × {Y=1 / P=0.5 / N=0}，总分 0–4，纳入阈值 ≥ 2：
1. IC/EC explicit
2. Search space（4+ DLs + extra strategies）
3. Quality assessment of primary studies
4. Information regarding primary studies

**Threats to Validity 三轴（§6 Page 27，Ampatzoglou 2020 引用 [12]）**：Study Selection Validity / Data Validity / Research Validity（+ lifecycle 扩展类）。

**SE Task 开放编码**：§3.6 Page 10–11，二作开放编码 SE tasks（如 test automation、software maintainability prediction、software defect prediction、bug prioritization），随后用 Qualitative Content Analysis 进行归并；每篇被指派 1–3 个 SE tasks。

### 2.4 finding / gap / recommendation / roadmap 形成方式

- **General Recommendations（§4.3.1 Page 19）**：跨 KA 通用建议，每条带研究数 n（13/12/16/21/18/3/3），是显式可统计 finding 块。
- **KA-specific 建议（§4.3.2–§4.3.12）**：按 11 个 KA 逐节给出 SE task 级 future work，明确引用具体 secondary studies。
- **Implications 1–7（§5 Page 24–27）**：从 RQ 结论升级的 7 条 numbered implications，每条都有明确支撑 RQ 与 KA。
- **Conclusion + 3 key findings + Recommendations for Researchers/Practitioners（§7 Page 28–29）**：明确 finding 三段 + 多层级 recommendation。
- **Replication package（Footnote 1 Page 3，DOI 10.5281/zenodo.7082429）**：开放代码与数据。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确 | 根节点 `Machine Learning for Software Engineering` 合理，但未在根问题映射表中显式列出 RQ1/RQ2/RQ3 三 RQ 与"质量目录贡献声明"，仅泛指"RQ / 贡献声明"。 | I |
| 主干分支是否覆盖原文 schema | 不覆盖 | 仅 5 个通用分支 b1..b5，没有任何分支专门承载：3-RQ 结构、11-字段抽取表、4-轴 ML scheme、11-KA SWEBOK 分类轴、8-类 ML 应用任务、DARE-4 4-准则、三轴 Threats。b3 "主题/对象分类"与 b4 "方法/技术/干预"是 interface stub，未把 SWEBOK 11 KAs 与 4-轴 ML 拆出。 | **C** |
| 叶子维度是否足够具体 | 严重不足 | 6 个 `leaf-*` 全部为通用接口（scope/corpus/taxonomy/method/evidence/finding），定义、取值空间、证据要求、统计用途、迁移边界 6 列在所有 6 行使用同一段模板文本，未做单篇差异化。`原文模式候选叶子映射` 只放 5 个种子，且全部 `not_verified`，未覆盖 4-轴 ML scheme、11-KA、Table 7 应用任务、Implications 1–7、Threats 3 轴。 | **C** |
| 取值空间是否可执行 | 不可执行 | 现有叶子取值空间写为"自由文本加 RQ / 贡献声明引用"或"层级枚举 / 关系值 / 开放 action point" 等模糊口径。原文实际有**封闭枚举**（4 轴 ML、11 KA、DARE-4 Y/P/N、3 类 role of AI、4 类 supervision、2/2 类 incrementality/generalizability、8 类 ML application task），却未在 review 中作为可执行取值空间冻结。 | **C** |
| 关系边是否缺失 | 缺失 | 原文存在多个跨维度关系：(a) 每篇 study × 多个 SE tasks（1–3 个），(b) SE task × 多个 KAs，(c) study × 4 轴 ML（每轴 1 类），(d) KA × 4 轴 ML 联合分布（Fig. 6 热力图），(e) 7 Implications × 支撑 KA。当前树无关系边描述。 | I |
| 统计用途 / 分母是否正确 | 不准确 | 全篇 review 把统计用途列为"当前 19 篇 survey-of-surveys 样本"，分母错误——本篇内部统计的分母是 83 篇 secondary studies / 6 117 primary studies / 274 authors / 140 institutions，且 4-轴 ML 子项分别有显式 n（54/17/12, 65/11/5/2, 82/1, 72/11），General Recommendations 也有 n=13/12/16/21/18/3/3。这些可直接进入定量统计，被误降为 schema seed not_verified。 | **C** |
| 候选 finding 路径是否完整 | 不完整 | 原文 finding 链路为：抽取字段 → KA 分布 → 4-轴 ML 分布 → §4.3 KA-recommendation → §4.3.1 General Recommendations（带 n）→ §5 Implications 1–7（结构化升级）→ §7 三条 key findings + Recommendations。当前 review 把 finding 路径压缩为单一 `leaf-finding` 通用接口，未保留 General Recommendations 显式 n、未保留 Implication 编号、未保留 §7 三条 key findings。 | **C** |
| A.1–A.4 证据链是否足够 | 严重不足 | A.1 三条来源 OK；A.2 仅 4 条 EV-001..004，全部 `not_verified` 且页码字段写"摘要 / 引言页；待 A2a 精确页码复核"。`paper_content.txt` 含 `--- Page N ---` 行级页标记，逐表逐图都可定位（如 RQ Page 6、Table 1 Page 7、Table 2 Page 10、Tables 3–4 Page 13–14、Table 5 Page 15、Table 6 Page 23、Table 7 Page 24、Implications Page 25–27、Threats Page 27），不存在"页码无法获取"的客观阻塞，却统一写 not_verified。A.3 8 条结论全部 weak/schema_seed，导致整个证据链没有可统计 anchor。A.4 仅 2 个检查，缺逐 KA / 逐轴的字段精核入口。 | **C** |
| 是否存在可能误导 A2a 的强主张 | 存在 | 候选叶子 `leaf-ml4se-tertiary-study-orig-data-source`（"数据来源：代码库、issue、commit、测试、需求、开发者活动和工业数据"）**在原文 §3.6 抽取表中没有对应字段**——原文抽取的是 "Title and source"（出版来源）与 "Publication venue"，并不存在独立的"primary-study 数据来源 taxonomy"。这是**把原文没有的 schema 字段当成原文候选叶子写入**，违反"不允许臆造原文没有的字段"原则；如果 A2a 据此扩库会产生错误对照。另外，`schema 历史观察` 字段在快速结论卡片中写"暴露挑战 / 行动建议类 finding pattern；已在 SUMMARY 中作为 A2a 重点候选"，是站得住的；但 §2 六类 pattern 抽取表里说"83 reviews/6117 primary studies 的数值需 PDF 表格核对后才能引用"——而这两个数字在 Page 1 摘要、Page 12 §4.1、Page 28 §7 三处均出现，足以引用，被过度降级。 | **C** |

## 4. 建议维度树骨架

以下骨架严格按原文 §3.1 / §3.2 / §3.5 / §3.6 / §4 / §5 / §6 / §7 复原。所有取值空间均可在 `paper_content.txt` 行内定位证据，A2a 可直接精核。

```text
[dim-ml4se-tertiary-study-root] ML4SE Tertiary Study（Kotti 2023）
├── [dim-b1] 研究问题与目标
│   ├── [leaf-rq1] RQ1: SE tasks tackled by ML
│   ├── [leaf-rq2] RQ2: SE KAs that could be better covered by ML
│   ├── [leaf-rq3] RQ3: ML techniques used in SE
│   ├── [leaf-objective] 4 项研究目标（catalog/summarize/state/opportunities）
│   └── [leaf-unit-of-analysis] 分析单元（secondary study；隐含 primary study）
├── [dim-b2] 语料收集与纳排
│   ├── [leaf-search-stages] 四阶段检索（automated / manual / backward / forward snowballing）
│   ├── [leaf-keyword-groups] 三组关键词（SE 13 / ML 27 / Secondary 35）  — Table 1 Page 7（封闭枚举）
│   ├── [leaf-time-window] 时间窗（automated 2015–2020；snowballing 扩展 1990–2022）
│   ├── [leaf-databases] 数据库（IEEE Xplore / ACM DL / Scopus）
│   ├── [leaf-iceec] IC/EC 条款（IC 3 条 + EC 5 条）  — Page 8–9
│   ├── [leaf-selection-process] 选择流程（15-sample Cohen Kappa ≥0.8；split-half 1552 篇；fulltext 兜底）
│   └── [leaf-corpus-counts] 语料漏斗数值（2316→1897→1566→1567→backward+16→forward+84→140→83）
├── [dim-b3] 抽取字段（Data Extraction Form, §3.6）
│   ├── [leaf-field-bib] 标题、来源、年份、venue、作者/机构/国别（前 4 字段）
│   ├── [leaf-field-study-type] Study type（SLR / SMS / taxonomy / survey / meta-analysis）
│   ├── [leaf-field-method] Research method（adopted guideline，封闭引用列表）
│   ├── [leaf-field-qa] DARE-4 QA score（0–4）
│   ├── [leaf-field-primary-count] Number of primary studies
│   ├── [leaf-field-application-domain] SWEBOK KA + subarea + SE tasks（开放编码 1–3/篇）
│   ├── [leaf-field-implications] Implications + comments
│   └── [leaf-field-ml-techniques] Employed ML techniques
├── [dim-b4] SWEBOK V3 知识领域分类（Table 5, Page 15）
│   └── [leaf-swebok-ka] 11 KA 封闭枚举（SW Quality / SW Testing / SE Process / SE Management / SW Requirements / SW Maintenance / SW Design / SW Configuration Management / SE Models & Methods / SE Professional Practice / Engineering Foundations）
│       └── [leaf-swebok-subarea] 子领域（22 行 KA×Subarea 矩阵，Table 5）
├── [dim-b5] ML 4-轴分类方案（§3.6 Page 11–12; Table 6 Page 23）
│   ├── [leaf-axis-role] Role of AI in SE（SBSE / Fuzzy-prob / Class-learn-predict）
│   ├── [leaf-axis-supervision] Supervision（supervised / unsupervised / semi-sup / RL）
│   ├── [leaf-axis-incrementality] Incrementality（online / offline）
│   └── [leaf-axis-generalizability] Generalizability（instance-based / model-based）
├── [dim-b6] ML Application Task 分类（Table 7 Page 24）
│   └── [leaf-ml-task-class] 8 类（Class/Clust/Regr; Pattern Discovery; Dim. Reduction; IR; Stochastic Search; Generation; Hybrid; Misc）
├── [dim-b7] 质量评估（DARE-4，Table 2 Page 10）
│   ├── [leaf-dare-criteria] 4 准则封闭枚举（IC/EC; Search space; QA of primary studies; Info on primary studies）
│   ├── [leaf-dare-scoring] Y/P/N 计分（1 / 0.5 / 0）+ 阈值（≥2）
│   └── [leaf-irr] inter-rater agreement（Cohen Kappa；QA 一致性 82%）
├── [dim-b8] 统计结果与 finding 链
│   ├── [leaf-stat-distribution] 分布统计（year / publisher / KA / 4 轴 / 4-axis×KA 热力图 Fig. 6）
│   ├── [leaf-general-rec] §4.3.1 General Recommendations（7 条带 n=13/12/16/21/18/3/3）
│   ├── [leaf-ka-rec] §4.3.2–§4.3.12 KA-specific recommendations
│   ├── [leaf-implications] §5 Implications 1–7（编号化升级）
│   └── [leaf-key-findings] §7 三条 key findings + Recommendations for Researchers/Practitioners
├── [dim-b9] 效度威胁（Ampatzoglou 2020 三轴，§6 Page 27）
│   ├── [leaf-validity-selection] Study Selection Validity
│   ├── [leaf-validity-data] Data Validity
│   └── [leaf-validity-research] Research Validity
└── [dim-b10] 复现资产
    └── [leaf-replication-package] Zenodo DOI 10.5281/zenodo.7082429 + 多个 .csv/.bib/.md/.txt artifact 引用
```

为什么当前 review 不够：当前 5-branch 6-leaf 接口只覆盖 b1/b2 的轮廓与 b3/b4/b5/b7/b8 的最弱版本，完全缺少 b6 / b9 / b10，且每个 b4/b5/b6/b7 都应有**封闭枚举叶子**而非自由文本。A2a 直接以当前树扩库会失去与原文 schema 对齐的能力。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 删除/重命名 `leaf-ml4se-tertiary-study-orig-data-source` | review.md §"原文模式候选叶子映射"表 | 原文 §3.6 抽取表中没有独立"数据来源"分类轴。应删除或改为 `leaf-orig-primary-study-source-info`（即 "Title and source"+"Publication venue" 的元信息字段），并在 EV 中明确引用 Page 10 第 1–3 条抽取字段。 | paper_content.txt Page 10 §3.6 列表（第 1、3 条） | **C** |
| 补齐 3 个 RQ 显式叶子 | review.md §"维度树结构" / §"叶子维度表" | 在 b1 下新增 `leaf-rq1` / `leaf-rq2` / `leaf-rq3` 三个封闭叶子，分别绑定 §4.2 / §4.3 / §4.4 与 Page 6 RQ 列表。 | paper_content.txt Page 6 RQ1–RQ3 | **C** |
| 新增 ML 4-轴分类子节点 | review.md §"维度树结构" b4 method 分支 | 在 b4 下显式列 4 个轴叶子（role / supervision / incrementality / generalizability），并给每个轴写**封闭取值空间**（如 supervision = {supervised, unsupervised, semi-supervised, reinforcement}），引用 Table 6 行内 n。 | paper_content.txt Page 11–12 §3.6；Page 23 Table 6 | **C** |
| 新增 SWEBOK V3 11-KA 枚举叶子 | review.md §"维度树结构" b3 taxonomy 分支 | 用 Table 5 的 11 KA + 22 子领域作为封闭枚举叶子，列出 Sec./Prim. 计数（如 SW Quality n=25/30%；SW Testing n=17/20%）。 | paper_content.txt Page 15 Table 5 | **C** |
| 新增 ML Application Task 分类叶子 | review.md b4 之下或新增 b6 | 把 Table 7 的 8 类（Class/Clust/Regr; Pattern Discovery; Dim. Reduction; IR; Stochastic Search; Generation; Hybrid; Misc）作为封闭叶子。 | paper_content.txt Page 24 Table 7 | I |
| 新增 DARE-4 4-准则 + 评分叶子 | review.md b5 evidence 分支 | 把 Table 2 4 个准则 + Y/P/N 评分 + 阈值≥2 + IRR 82% 写成封闭叶子（含取值空间），不再用泛指"质量评价"。 | paper_content.txt Page 10 §3.5 Table 2；Page 11 inter-rater 82% | **C** |
| 新增 Implications 1–7 叶子 | review.md b5/b8 finding 分支 | 把 §5 七条 numbered implications 列为单独叶子并保留编号 + 支撑 RQ；不应统统合并为 `candidate finding`。 | paper_content.txt Page 25–27 Implication 1–7 | I |
| 新增 §4.3.1 General Recommendations 计数叶子 | review.md b8 finding | 7 条通用建议 + 显式 n（13/12/16/21/18/3/3）应作为**已可统计**叶子，不应整体 `not_verified`。 | paper_content.txt Page 19 §4.3.1 | I |
| 新增 Threats 3-轴叶子 | review.md 新增 b9 validity 分支 | Selection / Data / Research Validity 三轴（Ampatzoglou 2020 引用 [12]）+ lifecycle 扩展。每轴列具体威胁条目（如 year-range 2015–2020、DARE-4 局限、role-of-AI axis 适配性、subjective manual processes）。 | paper_content.txt Page 27 §6 | I |
| 新增检索关键词三组叶子 + 漏斗计数 | review.md b2 corpus 分支 | SE 13 / ML 27 / Secondary 35 三组关键词来源（SWEBOK V3、ACM CCS、Kitchenham 2009、CSUR 标题挖掘）+ 漏斗数值（2316→1897→1566→1567→backward+16→forward+84→140→83）应作为**已可统计**叶子。 | paper_content.txt Page 6–9 §3.2；Table 1 Page 7 | I |
| 新增 replication package artifact 叶子 | review.md 新增 b10 或并入 evidence | Zenodo DOI 10.5281/zenodo.7082429 + 多个 .csv/.bib/.md/.txt artifact（cohen_kappa_agreement.csv、knowledge_areas.csv、further_research.csv、ml_techniques.csv、dare_assessment.csv、review-protocol.md 等）。 | paper_content.txt Page 3 footnote 1；§3 全章 footnote | I |
| 精确化所有 EV 页码 | review.md A.2 证据账本 | 对 EV-001..004 补齐精确页码（如 RQ→Page 6；Table 1→Page 7；Table 2→Page 10；Tables 3–4→Page 13–14；Table 5→Page 15；Table 6→Page 23；Table 7→Page 24；Implications 1–7→Page 25–27；§6 Threats→Page 27；§7 key findings→Page 28–29），并把 `not_verified` 升级为 `text_verified`（视觉级仍可留 `needs_manual_pdf_check`）。 | paper_content.txt 全文 `--- Page N ---` 行 | **C** |
| 修正统计分母 | review.md §"统计与候选发现链路" | 当前写"当前 19 篇 survey-of-surveys 样本"，应改为本篇内部统计的多套分母：83 secondary / 6117 primary / 274 authors / 140 institutions / 4-axis 子分母 / DARE-4 0–4 分布，并区分内部分母 vs 19 篇汇总分母。 | paper_content.txt Page 1 摘要；Page 12 §4.1；Page 28 §7 | **C** |
| 强化 §"原文模式候选叶子映射" | review.md 同节 | 把当前 5 条扩充为至少 25–30 条（覆盖 RQ ×3、抽取字段 ×11、SWEBOK KA ×11、ML 4 轴 ×4、ML 应用任务 ×8、DARE-4 准则 ×4、Threats ×3、Implications ×7、General Recommendations ×7、Replication artifact ×6）；只有这样才能真正复原原文 schema seed。 | paper_content.txt 全文 | **C** |
| 修正叶子表模板化重复 | review.md §"叶子维度表" | "统计用途 / 候选发现用途 / 迁移边界"列在 6 行使用同一段模板，应针对每个叶子写实质内容（如 scope 应说明 RQ 拆分；corpus 应给出漏斗数；taxonomy 应明确 SWEBOK V3 11 KA 枚举；method 应明确 4 轴 + 8 ML task；evidence 应明确 DARE-4 + Threats；finding 应明确 Implications 1–7）。 | 同上 | I |
| `schema 历史观察`/快速结论卡片中"83/6117 待 PDF 核对" | 快速结论卡片 § & §2 六类 pattern 抽取表 | 两数值在 Page 1 摘要、Page 12 §4.1、Page 28 §7 三处一致出现，可直接 text_verified；当前过度降级。 | paper_content.txt Page 1 / 12 / 28 | M |
| `证据等级`字段升级 | 快速结论卡片 | "图表/表格细节待人工原文核对"对部分关键数值已无必要；可拆为 `text_verified for {RQ, IC/EC, DARE-4 rubric, KA list, 4-axis list, application tasks, implications, threats}` 与 `needs_manual_pdf_check for {Fig. 6 热力图视觉、Fig. 1 流程图视觉}`。 | 同上 | M |

## 6. C/I/M 结论

- **C（直接破坏 Paper2 学术目标 / 证据链 / 后续 A2a 可靠性的问题）**：
  1. 主干分支只覆盖通用接口，未拆出 RQ1/RQ2/RQ3、4-轴 ML、11-KA SWEBOK、Table 7 ML 应用任务、DARE-4、Threats 三轴等本篇真实 schema 的核心维度。A2a 据此扩库会与原文 schema 对不齐。
  2. 叶子取值空间未冻结原文已有的封闭枚举（4 轴 ML、11 KA、DARE-4 Y/P/N、ML 任务 8 类），导致 A2a 无法用本篇做 schema 验证。
  3. 候选叶子 `leaf-orig-data-source` 在原文中无对应字段，是臆造的 schema 元素；存在直接污染 A2a 抽取 schema 的风险。
  4. 统计分母错误（用 19 篇 SoS 当成本篇分母），导致本篇本可贡献的 4-axis n 分布、KA n 分布、General Recommendations n 分布等真实可统计 finding 都被无谓降级。
  5. A.2 全部证据 `not_verified`，但 `paper_content.txt` 已有页级 marker 与全部关键表/图，本可 text_verified；当前证据链显著弱于原文允许的可审计水平。
  6. 候选 finding 路径不完整（缺 §4.3.1 General Recommendations 显式 n、缺 §5 Implications 1–7、缺 §7 三条 key findings），使本篇无法作为 finding heuristic 锚点。

- **I（实质影响维度树可用性 / 原文 schema 复原 / 证据可审计性的问题）**：
  - 缺 ML application task 8 类、DARE-4 IRR 82%、Threats 三轴 + lifecycle、Implications 编号、General Recommendations 显式 n、检索漏斗 / 三组关键词、replication package artifact 等条目（详见 §5 表）。
  - 叶子表 6 行模板化重复，未做单篇差异化。

- **M（不阻塞的清晰度或维护性建议）**：
  - 快速结论卡片中对 83/6117 两数值的"待 PDF 核对"已超出必要；可升级为 text_verified。
  - 证据等级字段可按 text_verified / needs_manual_pdf_check 分层。

- **最终建议**：**NEEDS FIX**。本 review 当前是合格的 schema **interface stub**，但远未达到 Paper2 A1-DT "复原原文真实 schema 作为 A2a 入口" 的目标。修复优先级：先处理 C 级 6 项（删除/重命名臆造叶子、拆出 RQ 三叶 + 4 轴 ML + 11 KA + DARE-4 + finding 链 + 精确页码 + 修正分母），再补 I 级清单。
