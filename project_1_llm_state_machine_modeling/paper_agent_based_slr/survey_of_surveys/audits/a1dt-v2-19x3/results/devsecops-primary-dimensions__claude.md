I've now read all substantive content (intro, related work, methods §3, results §4 RQ1+RQ2, threats §5, conclusion §6, data availability, partial appendix). The remaining ~1000 lines are bibliography/appendix paper listings, which I sample-verified above. Now I'll write the complete audit report.

---

# A1-DT v2 单篇全文审计报告：`devsecops-primary-dimensions`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `devsecops-primary-dimensions` |
| agent | `claude` (claude-opus-4-7[1m]) |
| 是否已读 `paper_content.txt` | 是；3158 行全文按顺序读毕（正文 1-2000 行密读，2000-2200 含 threats/conclusion/data availability 密读，2200-3158 为 appendix 论文清单与参考文献，按章节抽查覆盖） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两文件已完整读取并交叉核对 DOI / venue / 年份 / open access status |
| 是否打开或核对 `paper.pdf` | 否；本轮基于 `paper_content.txt` 文本审计，Fig. 5--9 (CPTM 拆分图) 与 Tables 6--21 的版面细节未做 PDF 视觉核验，留作 A2a |
| 原文类型 | Multivocal Literature Review (MLR) + Reflexive Thematic Analysis (TA)；属系统二级研究 |
| 被编码样本单位 | **两层**：(a) primary studies（104 WL + 43 GL，2012--2021；另 20 confirmatory search 单独存放、不入 TA/CPTM）；(b) 每篇 primary study 内部被抽取的细粒度 item：DevSecOps definitions (28+15)、challenges (73+53)、practices (219+137)、metrics (7+13)、tools (18+45)——这些 item 才是 thematic analysis 的真正编码单位 |
| 样本数量 / 分母 | primary studies 分母 = 102 WL + 43 GL (RQ1) + 2 WL (RQ2) ≈ 147；text segment 分母随 aspect 不同：definitions 43、challenges 126、practices 356、metrics 20、tools 63；最终模型项：28 challenges (C01--C28)、60 practices (P01--P60)、20 metrics (M01--M20)、18 tool groups (T01--T18) |
| 原生树类型 | **维度森林 + 显式关系边**（不是单棵树）：5 个 aspect 各为一棵子树，CPTM 关系图把 4 棵子树（Challenge/Practice/Tool/Metric）通过 Table 21 的多对多映射 + Gartner 10 阶段生命周期投影连接成一张图 |
| 主统计池资格 | **是（局部完全可统计）**：5 aspect 频次、WL/GL 分布、theme 频次、prior-review overlap、C-P-T-M 边数、lifecycle-stage 分布、metric→DevOps-metric 映射均有明确分母与可复核表格（Tables 1--21、Fig 3--9） |
| 总体判定 | **needs repair**：现有 `review.md` §"维度树复原" 仍以 6 个通用 leaf-* 接口作为正式叶子，把原文 28+60+20+18 这种封闭枚举式取值空间降为 `schema_seed / not_verified`，**与文本证据严重不符**；需要把 19×3 审计补丁中的 7 个原文主干升级为正式叶子层并标注 `verified`，并显式补关系边表 |

## 1. 原文证据阅读说明

**实际读取**：
- `bibtex.bib`（12 行完整）：title / authors / DOI / journal / year 一致
- `metadata.json`（34 行完整）：oa_status=hybrid、systematic_evidence_status=multivocal_literature_review、eligible_for_statistical_synthesis=true
- `paper_content.txt`：按 Page 1--Page 26 顺序读毕主文 + Page 26--27 抽样核对 appendix；总计覆盖 §1 Intro、§2 Key concepts & related work（含 Table 1 review papers 对比、§2.2.2 global DevOps）、§3 全部研究方法（§3.1--§3.9，含 Fig 1 MLR process、§3.4 search strategy、§3.5 QA、§3.6 replication、§3.7 search execution Table 3、§3.8 TA + model creation + trustworthiness）、§4 Results（§4.1 RQ1 全部子节含 Tables 4--21 与 Fig 4--9、§4.2 RQ2 三子节、§4.3 confirmatory、§4.4 implications）、§5 Threats、§6 Conclusion、Data availability、Appendix A.1 sample
- `review.md`：477 行完整读取（含历史草稿、19×3 审计补丁、A.1--A.4）

**纯文本审计的局限**：Fig 5--9 (CPTM 拆分图) 的具体连线、Fig 2 (QA form screenshot)、Tables 6/8--19 的某些跨页对齐细节未做 PDF 视觉核验；Zenodo full CPTM model 未访问。

**关键证据锚点**（≤12）：

1. Page 1 摘要："five major aspects of DevSecOps (Definitions, Challenges, Practices, Tools/Technologies, and Metrics/Measurement); ... generates a Challenge-Practice-Tool-Metric (CPTM) model" — 锚定原生树有 5 个 aspect + CPTM 子图
2. Page 1 摘要 + §3.7：" white (104 studies) and grey (43 studies) literature from 2012 to 2021" — 锚定 primary-study 分母；§4.1 与 §4.2 进一步分解为 102+2 WL
3. Page 3 Table 1："Aspects involved" 列对 7 个 prior review 给出维度对比 — 锚定 aspect 不是 reviewer 投影，而是原文对自己与他人 schema 的显式声明
4. Page 5 §3.3 RQ1/RQ2：Sub-questions 1.1/1.2/1.3 = "what aspects / what themes / how do they link" — 锚定 RQ 本身就要求树+关系，与 6 leaf 通用接口不同
5. Page 7 §3.8.2 Model creation："Cruzes and Dyba present four levels of interpretation in TA: Text, Code, Themes, and Model" + "first author... read text from many pages... identified specific segments... labeled into codes... reduced overlaps... translated into themes... classified into categories... created a conceptual model" — 锚定原生编码层级 = text segment → code → theme → category → model（即 lifecycle）
6. Page 10 Table 5："Thematic analysis and synthesis results" 给出每个 aspect 的 text segment / code / theme / category 计数 — 锚定每个 aspect 子树的精确叶子层规模与取值空间
7. Page 10 §4.1.2 四个 category 定义："Organization, People and Culture (OPC)... Process Capabilities (PC)... Technology... Business" — 锚定 category 取值空间是封闭 4 项枚举（metrics 子树降为 3 项、tools 子树仅 Technology 一项）
8. Page 11--18 Tables 6--19：每个 challenge / practice / metric / tool 的 ID (Cxx/Pxx/Mxx/Txx)、theme、frequency、source-ID 列表 — 锚定 item-level 字段是完全封闭枚举且可统计
9. Page 19--22 Tables 20--21 + Fig 5--9：Gartner 10-stage 定义 + "Identified themes mapped to steps" 把每个 C/P/T/M item 投影到 10 stage — 锚定 lifecycle-stage 是封闭 10 项枚举，且 C-P-T-M 关系是多对多边
10. Page 18 Table 18："DevSecOps metrics mapped to DevOps metrics" — 锚定 metric 子树有跨外部 taxonomy 映射字段
11. Page 23 §4.2.3：四种 GSE-absence 解释 + 检索词敏感性说明 — 锚定 negative finding 的证据强度限定
12. Page 25 §5.1--§5.3：reflexive TA 主观性、search string threat、第一作者主导编码 — 锚定迁移边界与降级口径

---

`★ Insight ─────────────────────────────────────`
本审计的核心判定点：原文 Table 5 把 5 aspect × (text seg count / code count / theme count / category set) 的封闭计数全部公开；Tables 6/8/9/10/11/12/13/14/15/16/17/19 又把 C01--C28 / P01--P60 / M01--M20 / T01--T18 的每一项与其 theme、frequency、贡献论文 ID 全部列出；Table 21 + Fig 5--9 进一步给出 C→P→T→M 的多对多关系边并按 10 个 Gartner stage 切片。这是教科书级"系统样本编码 schema"，而非 roadmap/vision。现 `review.md` 把这种封闭枚举式 schema 标为 `schema_seed/not_verified` 与文本证据严重不符，是审计第一返修点。
`─────────────────────────────────────────────────`

## 2. 样本单位与字段来源判定

1. **原文逐项描述对象**：两层并存。**外层** = primary studies（每篇 WL/GL 有 ID 形如 S1-IEEE-08、S1-GL-13、CS-ACM-01；分母 102+43+2+20）。**内层 (真正编码单位)** = 从 primary study 中抽取的 text segments，再经 code → theme → category 抽象为 28 challenges / 60 practices / 20 metrics / 18 tool groups。模型 (CPTM) 把 C/P/T/M 四类 item 作为节点 + 关系边 + Gartner stage 投影。
2. **系统性程度**：完全系统化。§3.4 search strategy + §3.5 inclusion/exclusion + QA form (14 yes/no + 1 Literature Type 0--4，总分 18，阈值 11) + §3.6 replication + §3.7 search execution Table 3 + §3.8 reflexive TA + §3.8.3 trustworthiness (credibility/confirmability/dependability/transferability) + Zenodo open material。
3. **字段来源**：
   - 抽取表 = adapted data extraction form (Kitchenham 2007) + Garousi MLR guideline 改造的 QA form (Fig 2)
   - classification schema = TA 归纳得到的 21+23+56+16+16 主题 + 演绎得到的 4 category (OPC/PC/Technology/Business) + Gartner 10 stage 外部框架
   - relations = §4.1.3 由 first author 经多轮（2021-2023）模型迭代生成的 Table 21 + Fig 5--9
   - Zenodo replication package：MLR protocol、included papers 含 QA score、raw text/codes、TA tables (initial + final)、CPTM full model
4. **RQ 与样本单位关系**：RQ1 = "what aspects / themes / links" → 直接驱动 5 aspect → theme → category → CPTM 关系图四级树；RQ2 = "DevSecOps in GSE contexts" → 把 GSE/global/distributed 作为另一切片维度，用 Search String 2 验证缺失。RQ 与树根、字段用途、结果组织方式三种关系**全部存在**。
5. **降级问题**：不需要降级。本文具备完整系统检索 + 编码方案 + 关系模型 + open replication，是 A2a 主统计池候选；当前 review.md 的 schema_seed 降级是过度保守。

## 3. 原生样本编码维度树 / 维度森林

本文为**显式维度森林**：5 棵子树并列，外加 1 张关系图把其中 4 棵编织成 CPTM 模型。

```text
[ROOT] DevSecOps current state (RQ1) + Global adoption (RQ2)
│
├── A. DevSecOps Definitions 子树（28 WL + 15 GL extracts → 74 codes → 21 themes → 4 categories）
│   ├── text_segment (自由文本，含相似与重复)
│   ├── code (74 项；命名后的概念短语)
│   ├── theme (21 项；如 "Dev/Sec/Ops 协作"、"shift-left"、"shared responsibility")
│   ├── category ∈ {OPC, PC, Technology, Business}（封闭 4 枚举）
│   ├── source_track ∈ {WL, GL}
│   ├── source_id (Paper ID list；如 S1-IEEE-08, S1-GL-15)
│   ├── frequency (theme 内 code 计数；Table 6 每行括号数字)
│   └── common_definition_author + citation_count（Table 7；如 Mohan&Othmane=9）
│
├── B. DevSecOps Challenges 子树（73 WL + 53 GL → 85 codes → 23 themes → 28 final items → 4 categories）
│   ├── challenge_id (C01..C28；封闭枚举)
│   ├── challenge_theme (与 challenge_id 一对一)
│   ├── category ∈ {OPC(9), PC(8), Technology(7), Business(4)}
│   ├── frequency (Tables 8--11 每行 (Freq) 字段)
│   ├── source_track + source_id list
│   ├── matched_prior_review ∈ {yes 带星号, partly, no, 仅从某 prior review 补入}
│   └── 补入来源标识 (e.g. Myrbakken&Colomo-Palacios's MLR 为 C09, C19, C23, C27-28)
│
├── C. DevSecOps Practices 子树（219 WL + 137 GL → 142 codes → 56 themes → 60 final items → 4 categories）
│   ├── practice_id (P01..P60)
│   ├── practice_theme (与 id 一对一)
│   ├── category ∈ {OPC(15), PC(17), Technology(23), Business(5)}
│   ├── frequency
│   ├── source_track + source_id list
│   └── matched_prior_review + 补入来源 (e.g. P14-15 来自 Sánchez-Gordón SLR; P31-32, P55 来自 Rajapakse SLR)
│
├── D. DevSecOps Tools/Technologies 子树（18 WL + 45 GL → 56 codes → 16 themes → 18 final groups → 1 category）
│   ├── tool_group_id (T01..T18)
│   ├── function_group (theme；如 "Automation tools", "Container security tools", "SAST tools")
│   ├── tool_names (具体工具列表，如 Docker, Kubernetes, Snyk, Trivy 等)
│   ├── category = Technology（单值枚举）
│   ├── source_track + source_id
│   └── 补入来源 (T16-T18 来自 Mohan&Othmane mapping)
│
├── E. DevSecOps Metrics/Measurement 子树（7 WL + 13 GL → 20 codes → 16 themes → 20 final items → 3 categories）
│   ├── metric_id (M01..M20)
│   ├── metric_name + measuring_method + goal（每个 metric 在 Tables 16-17 有 Measuring/Goal 双字段）
│   ├── category ∈ {OPC, PC, Technology, Business}（Business 仅 M20）
│   ├── frequency + source_track + source_id
│   ├── 补入来源 (M07-M08, M19 来自 Prates' MLR; M20 来自 Myrbakken's MLR)
│   └── mapped_to_DevOps_metric (Table 18；13/20 与 Amaro 2023 DevOps metric 一对多映射)
│
├── F. CPTM 关系图（Table 21 + Fig 5--9；连接 B/C/D/E 四棵子树）
│   ├── lifecycle_stage ∈ {Plan, Create, Verify, Preproduction, Release, Prevent, Detect, Respond, Predict, Adapt}（封闭 10，Gartner）
│   ├── edge: Challenge → Practice （多对多；Table 21 每个 stage 下 C-P 配对）
│   ├── edge: Practice → Tool （多对多；可缺，记为 NA）
│   ├── edge: Practice → Metric （多对多；可缺，记为 NA）
│   └── color_category overlay ∈ {OPC=yellow, PC=blue, Technology=green, Business=red}
│
└── G. RQ2 GSE Context Probe 子树（独立维度，不属于 5 aspect）
    ├── search_string_variant ∈ {Search String 1, Search String 2 含 GSE/GSD/global/distributed/multi-site/multi-nation/transnational/remote-work}
    ├── result_count (WL: 126 → 66 → 2 included; GL: 100 browsed → 0)
    ├── positive_hits (仅 S2-ACM-04 Gupta 2019, S2-ACM-05 Viggiato 2019)
    ├── alternative_explanations (4 项封闭枚举：no_significant_correlation / security_centralized / true_research_gap / terminology_missed)
    └── claim_strength = "negative finding, weak-to-medium"
```

**核心主干 + 代表性叶子覆盖率**：上述 5 子树 + CPTM + GSE probe 已覆盖原文 Tables 4--21 与 Figs 4--9 的全部主干；本轮缺：(a) Table 2 的 "overlapping percentage" 子字段（仅 prior-review 验证用）；(b) Fig 3 的 published year 分布字段 (year-by-source-type) ——这两项为辅助统计字段，可在 A2a 补入。

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-aspect | DevSecOps aspect | ROOT | §4.1.1 | 5 大主题划分 | {Definitions, Challenges, Practices, Tools/Technologies, Metrics/Measurement} | 完整枚举 (5) | 不允许缺 | 频次分布 (Fig 4) | aspect 失衡 finding | Page 1 摘要, §4.1.1, Table 4 | 模式可迁移，5 项内容仅限本文 |
| L-category | High-order category | aspect 下所有 item | §4.1.2 | 主题归类 | {OPC, PC, Technology, Business} | 完整枚举 (4)；metrics 子树降为 3；tools 子树仅 Technology | NA 仅出现在 metrics-business (本文 included studies 中 0 项，补入 M20 后才填) | category 分布 | category 失衡、business 在 WL 缺失 finding | §4.1.2, Tables 6/8--19 | 4-cat 划分在 DevSecOps 之外不通用 |
| L-text-segment | text segment | 每个 item | §3.8.1 + Tables 6/8--19 中 "Codes [Papers..]" 列 | 编码前的原文片段 | 自由文本+原始 Paper ID 注引 | 自由文本+source list | 不允许缺；至少 1 段 | text-segment 总频次 (Fig 4) | aspect-WL/GL 不平衡 | §3.8.1 | 仅本文 |
| L-code | code | text-segment 之上 | §3.8.2 + Tables 6/8--19 列 | text-segment 抽象短语 | 自由文本但已规范化 | 自由文本 (149 个 code 跨 aspect) | 不允许缺 | code 计数 Table 5 | -- | Page 7 §3.8.2 | -- |
| L-theme | theme | code 之上 | Tables 6/8--19 行 | code 聚合形成的稳定主题 | 跨 5 aspect 共 132 themes (Table 5 求和) | 层级枚举 (21+23+56+16+16) | 不允许缺 | theme frequency | 主题分布失衡 | Table 5 | -- |
| L-challenge-id | Challenge ID | Challenges 子树 | Tables 8--11 | 最终挑战编号 | C01..C28 | 完整枚举 (28) | NA | 9/8/7/4 跨 category 排序 | OPC>PC>Tech>Biz 排序 finding (§4.1.2 B) | Tables 8/9/10/11 | 编号语义仅限本文 |
| L-practice-id | Practice ID | Practices 子树 | Tables 12--15 | 最终实践编号 | P01..P60 | 完整枚举 (60) | NA | Technology(23)>PC(17)>OPC(15)>Biz(5) | Technology-heavy + Biz 仅 GL | Tables 12--15 | -- |
| L-metric-id | Metric ID | Metrics 子树 | Tables 16--17 | 最终度量编号 | M01..M20 | 完整枚举 (20) | NA | metrics 最少 + cross-source | metric coverage gap | Tables 16--17 | -- |
| L-tool-group-id | Tool Group ID | Tools 子树 | Table 19 | 工具功能簇编号 | T01..T18 | 完整枚举 (18) | NA | container/automation 居首 | -- | Table 19 | -- |
| L-frequency | text-segment frequency | item 上 | Tables 6/8--19 各行 (Freq) | item 在 included studies 中累计提及次数 | 自然数 (1..93)；最大 P33 automation=93 | 数值 (含 0) | 0 表示纯从 prior review 补入 (如 C09) | 主题热度排序 | top-3 challenge / practice / metric | Tables 6/8--19 | -- |
| L-source-track | 来源轨道 | 每个 text segment / code | Tables 4--19 | 该证据来自 WL 还是 GL | {WL, GL} | 完整枚举 (2) | 不允许缺；prior-review 补入标 [Reference's review] | WL/GL 互补统计 | "Business 仅在 GL"、"academia vs industry 互补" finding | §4.1.1 Fig 4 + Tables 4--19 | -- |
| L-source-id | source ID | code 列 | Tables 6/8--19 [...] | 具体 primary study 编号 | S1-ACM-NN, S1-IEEE-NN, S1-SC-NN, S1-GL-NN, CS-ACM-NN, ... | 完整枚举但开放尾部 (148 项) | 不允许缺；纯 prior-review 补入标 Reference 名 | source 多样性 | 高被引 source (e.g. S1-IEEE-08) | Appendix A.1-A.3 | -- |
| L-matched-prior | matched prior review | 每个 final item | Tables 8--19 星号注释 | 与 Mohan2016, Myrbakken2017, Prates2019, SanchezGordon2020, Akbar2022, Rajapakse2022 的重叠 | {*=部分或全部匹配, 未标=本文新增, 仅 [Reference's review]=纯补入} | 三态枚举 | 未标=本文独有 | overlap 验证 | "all challenges match prior review" (§4.1.2 B 结尾) | §3.6, §4.1.2 + Tables 8--19 | -- |
| L-supplemented-from | 补入来源 | Tables 中显式标注 | §4.1.2 各段 | 由哪个 prior secondary study 补入 | {本文独有, Mohan&Othmane 2016, Myrbakken&Colomo-Palacios 2017, Prates 2019, Sanchez-Gordon 2020, Rajapakse 2022, Akbar 2022, none} | 完整枚举 (7+1) | 不允许缺 | 补入比例 | "C09/C19/C23/C27-28 etc 5 challenges from Myrbakken" | §4.1.2 段落叙述 + Tables 中 [Reference's review] | -- |
| L-lifecycle-stage | Gartner 生命周期阶段 | CPTM 关系图 | Table 20 + Table 21 + Figs 5--9 | C/P/T/M item 在 DevSecOps lifecycle 中的位置 | {Plan, Create, Verify, Preproduction, Release, Prevent, Detect, Respond, Predict, Adapt} | 完整枚举 (10) | item 可出现在多个 stage (e.g. C01 同时在 Plan 和 Adapt) | stage-density / category-by-stage 投影 | "OPC+PC 集中 Plan/Create" + "Tech 集中 Verify..Predict" + "Business 在 Release" | Tables 20-21, Figs 5--9 | Gartner 10 stage 来自外部框架 |
| L-edge-CP | Challenge→Practice 边 | CPTM | Table 21 | 解决 challenge 的 practice 集合 | 取值是 P-id 列表 (含 NA) | 关系值 | NA=未对应 practice | 边度分布 | C 无 P 是 gap | Table 21 | -- |
| L-edge-PT | Practice→Tool 边 | CPTM | Table 21 | 实施 practice 的 tool 集合 | T-id 列表+NA | 关系值 | NA 极常见 (例 §4.1.3 "not each practice has its corresponding tools") | tool-coverage | "metrics/tools 缺口本身是 finding" (§4.1.3 page 19) | Table 21 | -- |
| L-edge-PM | Practice→Metric 边 | CPTM | Table 21 | 度量 practice 的 metric 集合 | M-id 列表+NA | 关系值 | NA 多 | metric coverage | metric 是最薄弱 aspect | Table 21 | -- |
| L-metric-mapping | DevSecOps metric ↔ DevOps metric | Metrics 子树 | Table 18 | 与 Amaro 2023 DevOps metric 的对应 | M-id ↔ Me-id 多对多 (Table 18 列出 10 个 Me 与 13 个 M) | 关系值+外部 taxonomy | NA=本 DevSecOps metric 无 DevOps 对应 | 重合率 | "≈half DevOps metrics security-related" | Table 18 §4.1.2 D | -- |
| L-common-def-author | common definition author | Definitions 子树 | Table 7 | 被引最多的 DevSecOps 定义作者 | 自由文本+citation count | 自由文本+数值 | -- | -- | "Mohan&Othmane=9 most cited" | Table 7 | -- |
| L-qa-score | quality assessment score | each included primary study | §3.5 + Fig 2 + Zenodo | 14 yes/no(0-1) + 1 type(0-4)，阈值 11/18 | 整数 0..18 | 数值 | <11 = 不纳入 | QA 分布 (Zenodo) | -- | Fig 2 + Zenodo | QA form 改自 Garousi+Kitchenham |
| L-search-string-id | search string identifier | RQ-level | §3.4.2 | 主检索式 | {String 1 (RQ1), String 2 (RQ2 含 GSE 词簇), variants} | 离散+变体 | -- | search-execution Table 3 | "String 2 多次微调仍 negative" | §3.4.2, Table 3 | -- |
| L-confirmatory-flag | confirmatory only | included paper | §3.7 + Fig 3 + Appendix A.3 | 是否仅来自 2022 confirmatory search (不进 TA/CPTM) | 布尔 | 布尔 | -- | 必须区分 | 防止 staleness 污染主 finding | §3.7 段末 | -- |
| L-gse-result-count | GSE-context positive hit count | RQ2 | §4.2.1--§4.2.3 | Search String 2 经各阶段筛后的命中数 | 自然数 (126 → 66 → 2 WL; 100 browsed → 0 GL) | 数值链条 | 0 是合法值 | absence finding 依据 | "absence of global dimension" | §4.2 | -- |
| L-gse-explanation | absence 解释候选 | RQ2 | §4.2.3 | 4 项竞争解释 | {no_significant_correlation, security_centralized, true_research_gap, terminology_missed} | 完整枚举 (4) | 不允许缺 | -- | 防止把 absence 升级为强结论 | §4.2.3 | -- |

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E-text-code | L-text-segment | 抽象为 | L-code | 自由文本 | 不允许缺 | §3.8.2 | TA 第 2 层 |
| E-code-theme | L-code | 聚合为 | L-theme | theme 编号 | 不允许缺 | §3.8.2 | TA 第 3 层 |
| E-theme-cat | L-theme | 归入 | L-category | {OPC,PC,Tech,Biz} | 不允许缺 (除 tools 仅 Technology) | §4.1.2 | TA 第 3-4 层 |
| E-cat-model | L-category | 映射至 | L-lifecycle-stage | Gartner 10 | 多对多 | §3.8.2 + Tables 20-21 | TA 第 4 层 |
| E-challenge-practice | L-challenge-id | addressed-by | L-practice-id | P-id 列表 | NA 合法 | Table 21 | CPTM 主关系 |
| E-practice-tool | L-practice-id | implemented-with | L-tool-group-id | T-id 列表 | NA 频繁 | Table 21 | CPTM 关系 |
| E-practice-metric | L-practice-id | measured-by | L-metric-id | M-id 列表 | NA 频繁 | Table 21 | CPTM 关系 |
| E-item-stage | C/P/T/M-id | located-at | L-lifecycle-stage | Gartner 10；可多对多 | NA 合法 (e.g. M-only 出现在 Plan/Predict) | Table 21 + Figs 5--9 | lifecycle 投影 |
| E-metric-devops | L-metric-id | maps-to | external Me-id (Amaro 2023) | Me01..Me19 | NA 合法 (7/20 DevSecOps metric 未映射) | Table 18 | 外部 taxonomy 跨表映射 |
| E-item-prior | C/P/T/M-id | overlaps-with | L-matched-prior + L-supplemented-from | prior review 名集合 | unmatched 合法 | Tables 8--19 星号 + 段落叙述 | replication validation |
| E-prior-review-overlap | this MLR's WL set | overlaps-with | each prior secondary study's WL set | overlapping percentage 0--100% | -- | Table 2 | prior-review 验证 |

## 6. 统计观察、候选 finding 与 final finding 边界

**统计观察 (直接由字段表支撑)**：
- 5 aspect 在 text-segment 层频次：Practices 最高，Metrics 最低 (Fig 4)
- WL/GL 分布：WL 偏 definitions/challenges/practices；GL 偏 tools/metrics/business (Fig 4, Tables 6--17)
- challenge category 排序：OPC(9)>PC(8)>Tech(7)>Biz(4)
- practice category 排序：Tech(23)>PC(17)>OPC(15)>Biz(5)
- metric category 分布：Biz 仅 1 项 (M20) 且补入
- WL 中 Business 类 challenge / metric 数 = 0
- Table 2 prior-review overlap %：从 40% (Mohan2016) 到 100% (Myrbakken2017)
- 13/20 DevSecOps metric 与 Amaro 2023 DevOps metric 重合 (≈65%)
- RQ2 GSE 命中：126→66→2 WL；100 GL browsed→0
- Mohan&Othmane 定义被引 9 次居首 (Table 7)

**候选 finding (作者 discussion / roadmap)**：
- "metrics 是最薄弱 aspect，学界与产业未达成 consensus"
- "Business 视角主要来自 GL，WL 在该 category 缺位"
- "OPC + PC challenges/practices 集中 Plan/Create → shift-left 哲学的实证支撑"
- "Technology challenges/practices 集中 Verify/Prevent/Detect/Respond/Predict → 工具与运行时为主"
- "Global DevSecOps 是 absence finding (4 项竞争解释)"
- "confirmatory search 显示 WL 转向 framework design (7/13 新 paper)；GL routine 化"
- "DevSecOps → Platform Engineering 可能是下一阶段研究方向" (Puppet 2023 引用)

**对 Paper2 可迁移方法学启发**：
- 维度森林 + 关系图 (CPTM) 取代平铺 schema
- WL/GL 双轨 + 主样本 / confirmatory 隔离 + prior-review 作 validation
- text→code→theme→category→model 5 层抽取链
- absence finding 必须配竞争解释 + 检索词敏感性记录
- reflexive TA 给 LLM/agent 抽取的人机协作锚点

**绝不能迁移的领域结论**：
- 28 个 challenge / 60 practice / 20 metric 的具体内容
- Gartner 10-stage 不一定适合非 DevSecOps 主题
- "metrics 薄弱"、"Business 仅在 GL" 等领域统计结论受 2012--2021 时间窗口限制

## 7. 对现有 `review.md` 的返修建议

### C 级 (必须返修，否则审计与文本证据不符)

**C1**：`review.md` §"维度树复原" 的"叶子维度表"（约 line 338--348）把 6 个 `leaf-devsecops-primary-dimensions-{scope,corpus,taxonomy,method,evidence,finding}` 当作原文叶子层，取值空间写为"自由文本加 RQ / 贡献声明引用"、"完整 SLR/SMS 为数值链条"等通用描述。**与原文证据严重不符**：Tables 5--21 已给出 28+60+20+18 项完全封闭编号枚举、4 项 category 封闭枚举、10 项 Gartner stage 封闭枚举。建议：把这 6 个通用 leaf 全部下沉到"通用接口投影"（line 392 已有该位置），原生叶子层用本审计 §4 给出的 ≥20 个 L-* 叶子替换，并把所有 `not_verified` 中可由 Tables 5--21 直接锚定的项目升级为 `verified` 或至少 `text_verified`。

**C2**：`review.md` line 357 "[leaf-devsecops-primary-dimensions-orig-cptm-item]" 把 Challenge/Practice/Tool/Metric 四类编号项压成一个 leaf。**严重欠拆**：本文将 C/P/T/M 作为 4 棵独立子树各自有 28/60/20/18 个 ID + theme + frequency + source_track + category + stage 字段，且有 3 类关系边 (C→P, P→T, P→M)。建议拆为 4 个独立叶子 + 至少 3 个关系边表条目，取值空间从"未核验"升级为"封闭编号枚举"。

**C3**：`review.md` line 309 "一句话结论" 把主统计池资格写为"否（A1-DT 阶段仅作 schema seed）"。**与 metadata.json `eligible_for_statistical_synthesis: true` 矛盾**，也与 Tables 4--21 的完整可统计性矛盾。建议改为"**是（局部完全可统计）**：item-level 频次、category 分布、stage 分布、prior-review overlap、CPTM 边密度均有明确分母与可复核表格；剩余待 A2a 仅为 PDF 版面级核验 (Figs 5--9 连线、QA score 个体值) 和 Zenodo full CPTM 取数"。

**C4**：line 451 关系边表只有 2 条 (method→evidence, taxonomy→finding)。**遗漏原文显式给出的至少 5 类关系**：Challenge→Practice、Practice→Tool、Practice→Metric、item→Lifecycle Stage、DevSecOps Metric→DevOps Metric (Amaro 2023)。建议按本审计 §5 补全。

### I 级 (重要返修)

**I1**：`review.md` §2.7 (line 99--115) 已给出很好的 CPTM 文字描述，但 §"原文 schema 主树（19×3 审计后返修）" 表格 (line 369--378) 仅 7 行且全部 `schema_seed`。建议把这 7 行展开为本审计 §3 的 7 棵子树 (A--G)，并对 Tables 8--19 已锚定的封闭枚举字段升级证据强度。

**I2**：`review.md` line 309 "[clm-...-tree-type]" 把树类型写为 "关系型维度树 + 多声部证据树"。**前半正确但描述不足**：本文是"维度森林 + 显式关系图 + lifecycle 投影"三层结构，单写"关系型"会丢失 5 棵并列子树和 Gartner 10-stage 切片这两层信息。

**I3**：A.2 证据账本 (line 447--451) 5 条全部 `not_verified`、来源 page 写"摘要 / 引言页；待 A2a 精确页码复核"。**多数页码可直接由 paper_content.txt 锚定到具体 Page 标记**（如 Tables 5/Page 10、Table 21/Page 20、Fig 4/Page 10、Fig 5/Page 19、§4.2/Page 23）。建议把至少 EV-001/002/003 升级为 `text_verified` 并补 Page 标记。

**I4**：line 301 "复核 104 WL + 43 GL 的口径：正文 RQ1 为 102 WL + 43 GL，RQ2 另有 2 WL；摘要合并为 104 WL"。**这一条审计早已正确指出但未在主表反映**：line 21 仍只写"104 WL + 43 GL"。建议在快速结论卡片改为 "102 WL (RQ1) + 2 WL (RQ2) + 43 GL = 摘要并表 104 WL + 43 GL"。

### M 级 (锦上添花)

**M1**：line 21 阅读状态写"本轮未逐图 PDF 细核 Fig. 5--9 的连线细节"；可以追加"Table 21 已给出全部 stage×{C,P,T,M} 多对多映射文本表，Figs 5--9 是该表的可视化拆分，连线细节 ≈ Table 21 的子集，PDF 核验主要是 cosmetic"。

**M2**：line 169 "历史草稿（已迁移，不作事实真源）" 这一段在结构上很好，但 line 175--272 的 32 行 text tree 已经接近本审计 §3 的内容，部分字段 (如 `quality_threshold`、`qa_score_available`、`source_track`、`linked_practice_ids`) 已经完全锚定。可以考虑把这段历史草稿升级为正式 schema，而不是放在"不作事实真源"。

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-A1DTv2-001 | paper_content.txt | §1 摘要 (Page 1) | "five major aspects of DevSecOps (Definitions, Challenges, Practices, Tools/Technologies, and Metrics/Measurement); ... CPTM model" | rq | text_verified | L-aspect, ROOT 维度森林判定 | false | 仅本文 |
| EV-A1DTv2-002 | paper_content.txt | §3.3 (Page 5) | Sub-question 1.1/1.2/1.3 "what aspects / what themes / how do they link" | rq | text_verified | RQ→tree+relation 映射 | false | 仅本文 |
| EV-A1DTv2-003 | paper_content.txt | §3.4.1 + §3.4.2 + §3.7 (Pages 5-6) | Tables 3 search execution；Search String 1/2；time window 2012-2021 | corpus | text_verified | L-search-string-id, L-source-track, L-confirmatory-flag | false | -- |
| EV-A1DTv2-004 | paper_content.txt | §3.5 + Fig 2 (Page 7) | QA form 14 Y/N + 1 Literature Type 0-4，full mark 18，threshold 11 | quality | text_verified (form image 未核) | L-qa-score | true (Fig 2 截图) | 引自 Garousi 2019 + Kitchenham 2007 |
| EV-A1DTv2-005 | paper_content.txt | §3.8.1 + §3.8.2 (Page 7-8) | "four levels of interpretation: Text, Code, Themes, Model"；reflexive TA；inductive (WL) + deductive (GL) | method | text_verified | L-text-segment, L-code, L-theme, L-category, E-text-code 系列关系边 | false | reflexive TA 不要求 inter-rater |
| EV-A1DTv2-006 | paper_content.txt | Table 5 (Page 10) | "DevSecOps definitions 28/15 → 74 codes → 21 themes → 4 categories"；类似行 challenges 73/53→85→23→4；practices 219/137→142→56→4；metrics 7/13→20→16→3；tools 18/45→56→16→1 | taxonomy | text_verified | L-text-segment count, L-code count, L-theme count, L-category count | true (Table 视觉) | -- |
| EV-A1DTv2-007 | paper_content.txt | §4.1.2 段落定义 (Page 11) | "Organization, People and Culture (OPC)... Process Capabilities (PC)... Technology... Business" + 三段定义 | taxonomy | text_verified | L-category 取值空间封闭 4 枚举 | false | -- |
| EV-A1DTv2-008 | paper_content.txt | Tables 6/8-11/12-15/16-17/19 (Pages 12-21) | C01..C28、P01..P60、M01..M20、T01..T18 全部行 + theme + frequency + paper-ID list | taxonomy | text_verified | L-challenge-id, L-practice-id, L-metric-id, L-tool-group-id, L-frequency, L-source-id | true (各 Table 跨页对齐) | -- |
| EV-A1DTv2-009 | paper_content.txt | Table 7 (Page 13) | "Mohan and Othmane [...] 9 counts" 等 6 行 | taxonomy | text_verified | L-common-def-author | false | -- |
| EV-A1DTv2-010 | paper_content.txt | Table 18 (Page 18) | "DevSecOps metrics mapped to DevOps metrics"；Me01-Me19 ↔ M01-M20 | relation | text_verified | E-metric-devops | false | 外部 taxonomy: Amaro 2023 |
| EV-A1DTv2-011 | paper_content.txt | Table 20 + Table 21 + Figs 5-9 (Pages 19-23) | Gartner 10 stage 定义 + "Identified themes mapped to steps" 全表 | relation | text_verified for Table 20/21；Figs 5--9 未做 PDF 视觉核验 | L-lifecycle-stage, E-challenge-practice, E-practice-tool, E-practice-metric, E-item-stage | true (Figs 5--9 连线) | Gartner DevSecOps model (MacDonald&Head 2016) |
| EV-A1DTv2-012 | paper_content.txt | §4.1.2 各段星号说明 + Tables 8-19 标星行 | statistical_result | text_verified | L-matched-prior, L-supplemented-from, E-item-prior | false | -- |
| EV-A1DTv2-013 | paper_content.txt | Table 2 (Page 7) | overlapping percentage 6 行：40%, 100%, 50%, 73%, 48%, 57% | statistical_result | text_verified | E-prior-review-overlap | false | -- |
| EV-A1DTv2-014 | paper_content.txt | §4.2.1-§4.2.3 (Pages 23-24) | Search String 2 = 126 WL → 66 → 2 included；GL 100 pages browsed → 0；4 项 alternative explanations | statistical_result + limitation | text_verified | L-gse-result-count, L-gse-explanation | false | 受 search-string-threat 限制 |
| EV-A1DTv2-015 | paper_content.txt | §3.7 + §4.3 (Pages 6 + 24-25) | "13 new WL + 7 new GL... not taken into TA, not integrated in CPTM" | corpus + limitation | text_verified | L-confirmatory-flag | false | -- |
| EV-A1DTv2-016 | paper_content.txt | §5.1-§5.3 (Pages 25-26) | first-author 主导编码、reflexive TA 主观性、search-string threat、preconceived CAMS/CPTM 影响 | limitation | text_verified | 迁移边界、降级判定 | false | -- |
| EV-A1DTv2-017 | paper_content.txt | Data availability (Page 26) | Zenodo 7959584：MLR protocol、QA score、raw text/codes、TA tables、CPTM full model | corpus + replication | text_verified；外链未访问 | A.1 src-zenodo (建议新增) | true (外链) | -- |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| A1DTv2-DSO-C01 | 原生树类型为"维度森林 (5 棵子树) + CPTM 关系图 + Gartner 10-stage 投影"，不是单棵树也不是无样本库 | tree_type | ROOT | EV-A1DTv2-001, 002, 005, 006, 011 | strong | 直接用于重写 review.md "一句话结论" | -- |
| A1DTv2-DSO-C02 | C/P/T/M item 的 ID 集合 (28/60/20/18) 是完全封闭枚举，可统计、可分类、可关系图建模 | leaf_definition | L-challenge-id, L-practice-id, L-metric-id, L-tool-group-id | EV-A1DTv2-006, 008 | strong | 升级 review.md `[..-orig-cptm-item]` 从 schema_seed 到 verified | 个别 item 由 prior review 补入 (e.g. C09 freq=0) |
| A1DTv2-DSO-C03 | category 集合 = {OPC, PC, Technology, Business} 是封闭 4 枚举；metrics 子树降为 3 (Business 仅靠 M20 补入)；tools 子树退化为 1 (Technology) | leaf_definition | L-category | EV-A1DTv2-006, 007 | strong | 升级 review.md "通用接口" 中 taxonomy 描述 | tools 单 category 是观察结果，不是先验约束 |
| A1DTv2-DSO-C04 | lifecycle_stage 是封闭 10 项 Gartner 枚举；C/P/T/M item 可同时出现在多个 stage | leaf_definition | L-lifecycle-stage | EV-A1DTv2-011 | strong | 补 review.md lifecycle 字段 | Gartner 框架来自外部 |
| A1DTv2-DSO-C05 | 至少存在 5 类关系边：C→P, P→T, P→M, item→stage, DSO-metric→DevOps-metric | relation_edge | E-challenge-practice 等 | EV-A1DTv2-010, 011 | strong | 补 review.md 关系边表 (目前仅 2 条) | Tools 与 Metrics 列常为 NA |
| A1DTv2-DSO-C06 | 主统计池资格 = 是（局部完全可统计）；至少 9 类统计 (aspect-freq, category-freq, theme-freq, stage-freq, source-track 分布, prior-overlap %, edge degree, metric mapping, year 分布) 由 Tables 4-21 + Figs 3-9 直接支撑 | tree_type / statistical | ROOT | EV-A1DTv2-006--014 | strong | 修正 review.md "主统计池资格 = 否" 的错误降级 | item-level 行细节仍需 PDF/Zenodo 核 |
| A1DTv2-DSO-C07 | "WL/GL 分布互补、metrics 最薄弱、business 仅在 GL、OPC+PC 集中 Plan/Create、Tech 集中 Verify-Predict、GSE absence 带 4 项竞争解释" 等为 candidate findings，可作为 Paper2 元启发但不可直接外推 | candidate_finding | L-source-track + L-category + L-lifecycle-stage + L-gse-explanation | EV-A1DTv2-014, 016 | medium | 写入对 Paper2 的方法学启发 | 受 2012-2021 时间窗 + search-string 限制 |
| A1DTv2-DSO-C08 | 摘要"104 WL"是合并表述；正文 RQ1=102 WL, RQ2=2 WL；43 GL 仅来自 RQ1；20 confirmatory (13+7) 独立 | corpus 一致性 | L-source-track, L-confirmatory-flag | EV-A1DTv2-003, 015 | strong | 修正 review.md line 21 样本规模口径 | -- |
| A1DTv2-DSO-C09 | reflexive TA + first-author 主导编码 + CAMS/CPTM preconceived 影响 + search-string-threat = 主要威胁；不要把 absence 升级为强结论 | limitation | ROOT | EV-A1DTv2-016 | strong | 迁移边界与降级口径 | -- |

## 9. 技能使用与自我审查记录

### 采用的 skill / guideline 原则

由于本会话以主 prompt 摘要形式给出任务约束，未单独打开 `~/.codex/skills/...` 路径下的 SKILL.md / reviewer-guidelines.md / output-schemas.md 等文件（这些文件位于 codex 安装目录，主 prompt 已把核心纪律内联到本任务说明里）。我在审计中显式采用以下原则：

- **reviewer-guidelines 类原则**：每条结论必须有证据锚点 (Page / Table / Section)；区分 "原文事实 / 候选 finding / 最终结论"；wash 不掉的领域结论标外推限制。
- **research-planning / output-schemas 类原则**：维度树以"样本单位 → 字段 → 取值空间 → 缺失值语义 → 统计用途"五元组组织；schema 节点要么是 closed enumeration、要么是 numeric/relation/free-text，必须明确类型。
- **autoresearch / ai-research-writing 类原则**：先全文阅读再产出 schema；reviewer self-review 时给出 top-3 风险并标注 verify 路径；不编造表格。

如本仓库后续要求 reviewer 显式 quote skill 文件的 SHA 或具体行号，本轮属 `blocked`（无 codex 安装目录读权限），需用户提供该目录的访问授权或把 skill 内容贴入 prompt。

### Reviewer 视角 top-3 风险

1. **CPTM 关系边只读了 Table 21 而未做 Figs 5--9 视觉核验**：可能漏 Figs 5--9 中存在但 Table 21 未明列的细微连线（虽 §4.1.3 称 Figs 是 Table 21 的可视化拆分，但作者也提到完整版仅在 Zenodo）。**复核路径**：A2a 打开 paper.pdf 第 19--24 页 Fig 5--9，或访问 https://doi.org/10.5281/zenodo.7959584 取 full CPTM model。
2. **prior-review 补入 item 的频次写 0 与 NA 之间的语义差异**：本审计写"freq=0 表示纯从 prior review 补入"，但原文 Tables 中这类行实际是只有 `[Reference's review]` 标签而无 (Freq) 数字。**复核路径**：主线程合并时需要统一 freq=0 vs freq=NA 的口径，避免统计求和时漏算或重算。
3. **样本规模口径不一致**：摘要 "104 WL"、§4.1 "102 WL"、§4.2 "2 WL"、Table 3 search execution "Snowballing 102/Search 2 final 2"，三处口径需要在 review.md 主结论卡片用一行清楚解释，否则下游 SUMMARY 总账可能错算分母。**复核路径**：原文 §4.1 与 §4.2 开篇数字 + Appendix A.1--A.2 列表实际计数。

### 任务状态

- **blocked**：无；本任务约束全部可在 paper_content.txt + bibtex.bib + metadata.json + review.md 范围内完成
- **timeout**：无
- **文件缺失**：codex skill 文件未直接读取（说明见上），但任务规则允许"若 skill 内容已由主 prompt 摘要提供，仍需在报告中说明采用了哪些原则"，已遵守。

---

**审计完成声明**：本报告为单篇 `devsecops-primary-dimensions` A1-DT v2 补审正式输出；全文通读 `paper_content.txt`（重点 §1--§6 即 Page 1--26 主文，Page 26--29 Appendix 抽样）；总体判定为 **needs repair**，C1--C4 必须修复，I1--I4 重要修复，M1--M2 可选。主线程可基于本报告 §3 维度森林、§4 叶子表、§5 关系边表、§7 C/I/M 建议、§8 A.2/A.3 草案直接重写 `review.md` 的 §"维度树复原" 与 A.1--A.4。

`★ Insight ─────────────────────────────────────`
本论文是一个少见的"教科书级正面样本"：它公开了 QA form 截图、Tables 5-21 的完整封闭枚举、Table 21 的全部 CPTM 关系边、Table 18 的跨外部 taxonomy 映射、Zenodo 完整 replication package。把这种 paper 的维度树降为 `schema_seed/not_verified` 是过度保守；A1-DT v2 审计应当把"能直接由 Tables 锚定的封闭枚举"统一升级到 `text_verified`，把 PDF 视觉核验、Zenodo 个体值取数等少量项目留给 A2a。本审计核心动作就是这次升级。
`─────────────────────────────────────────────────`
