我已读完所需技能文件关键章节，证据充足。下面给出完整审计报告。

---

# A1-DT v2 单篇全文审计报告 — `re-tertiary-study-2014`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-tertiary-study-2014` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是。一次性读取全文 9 页 OCR 文本（行 1–967），已覆盖摘要、Planning、Execution、RQ1–RQ3 结果、Limitations、Conclusion、References 与 Appendix A 完整 S1–S53 名录 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`bibtex.bib`（@inproceedings, EmpiRE 2014, pp.9–16, DOI 10.1109/EmpiRE.2014.6890110）与 `metadata.json` 均已读取，并交叉核对 venue / 年份 / SLR 单位口径 |
| 是否打开或核对 `paper.pdf` | 否。本轮只做 `paper_content.txt` 文本级审计；Figure 1–4 的视觉版面、QA score 直方图分布的精确柱高、Table III–VI 的版面对齐需 A2a 用 `paper.pdf` 进一步核对 |
| 原文类型 | tertiary study（systematic mapping tertiary study；按 §II 标题"Systematic Mapping Tertiary Study"，作者明确按 Kitchenham EBSE guidelines 执行）|
| 被编码样本单位 | **distinct SLR（study）**。作者把"同一项 SLR 的多份发表"用 `S-ID + [A][B][C]` 合并为一个 study；分子粒度是 study，分母两套：64 publications 与 53 studies |
| 样本数量 / 分母 | 53 distinct SLR（含 12 SMS、1 meta-analysis、其余 conventional SLR）/ 64 publications（31 conf + 16 journal + 4 workshop + 4 tech report + 8 thesis + 1 unknown）；QA 仅在 51 个 study 上施加（S3、S8 全文不可获得） |
| 原生树类型 | **维度森林**：①抽取表（publication metadata + #PS + focus）；②scope 分类（Table IV）；③topic-group taxonomy（Table V）；④QA rubric（Table I, QA1–QA4 三档 Yes/Partial/No）；⑤citation/impact 评估（Table VI）；⑥gap taxonomy（anomalies / lack-of-PS / ignored-areas，§III RQ3）；⑦publication-type 分类（Table III） |
| 主统计池资格 | **局部可统计**。Table II–VI、Figure 1–4 在 53 study / 51 QA 分母下结构清晰、字段封闭，可用于跨论文方法学统计；但所有领域结论（RE 子主题覆盖、与 roadmap[1,2] 比对的 gap 名单）只能作 candidate finding，不进入 Paper2 主统计池 |
| 总体判定 | **needs repair**（现有 `review.md` C1–C2 级问题需返修；详见 §7） |

## 1. 原文证据阅读说明

- 实读文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`（全 9 页 967 行）、`review.md`（221 行）。技能文件读取 `reviewer-guidelines.md` 全文、`ai-research-writing-skill/SKILL.md` 与 `research-planning/SKILL.md` 关键段落。
- 仅文本级审计；以下 4 处仍需 A2a 用 `paper.pdf` 视觉核验：
  1. Figure 1（yearly distribution）的柱高 vs §III 描述"2009 之后骤增"；
  2. Figure 2 quality-score distribution（"42/51 ≥ 2"）的柱高；
  3. Figure 3 QA1–QA4 各档计数（OCR 把 y 轴数列读成"`0510 15 20 25 30 35 40 45`"，已断版）；
  4. Figure 4 averaged QA score-vs-year 曲线的具体年份取值。

关键原文证据锚点（编号供后文 A.2 引用）：

| # | 章节 / 表 | 行范围 | 短引或释义 |
|---|---|---|---|
| E1 | §I Abstract / Introduction | L23–105 | "53 distinct systematic reviews ... reported in 64 publications"；目标含 quality / coverage / gaps |
| E2 | §II.A Planning — 3 个 RQ | L117–123 | RQ1=areas covered；RQ2=quality of published SLR；RQ3=gaps in coverage |
| E3 | Table I QA rubric (QA1–QA4, Yes/Partial/No, 1/0.5/0) | L147–178 | DARE 改编；4 项 × 3 档；citation 来自 [8,9,11] |
| E4 | §II.A 搜索串与 5 库 + snowball + manual venue 扫 | L184–220 | IEEE/ACM/SD/GS/EI Compendex + snowball [8-11] + RE/EASE/ESEM/REFSQ/REJ/ESE/IST 自 2004 |
| E5 | §II.A 三项 inclusion criteria | L226–230 | 英语 / SLR-SMS-meta / RE 焦点 |
| E6 | Table II 检索执行汇总 | L273–288 | 5 库 267→91→58→+6→64 publications→53 studies |
| E7 | Table III publication type | L317–331 | 31/16/4/4/8/1 |
| E8 | Table IV scope-of-RE-SLR 6 档 | L364–375 | state-of-the-art 33, methods 7, techniques 7, tools 4, frameworks 1, technology 1 |
| E9 | Table V topic-group × focus × #PS × year | L376–429 | 18 个 topic group；含 "Non-Functional Requirements","Complete RE Process","Model Driven Development","Knowledge Management and RE","RE in GSD" 等 |
| E10 | §III RQ2 + Figures 2/3/4 | L433–479 | 42/51 ≥2；QA3/QA4 半数被忽略；年度均分 2009 后下降 |
| E11 | Table VI Top-10 cited | L482–493 | S-ID × GS Citations × Pub channel × QA Score |
| E12 | §III RQ3 三类 gap | L505–576 | (1) anomalies in #PS, (2) lack of PS, (3) ignored RE areas with reference to roadmaps [1][2] |
| E13 | §IV Limitations | L577–615 | 检索覆盖缺口、S40 缺 venue 元信息、topic grouping 主观、QA rubric 受 EBSE guidelines 限制 |
| E14 | Appendix A S1–S53 名录 | L697–967 | 完整 reference + citation count；含 [A][B][C] 子发表合并方式 |

## 2. 样本单位与字段来源判定

1. **纳入对象**：focus 在 RE 任一子主题的 secondary studies（SLR / SMS / meta-analysis），由 study 而非 publication 计数。
2. **系统性**：是。作者明确遵循 Kitchenham EBSE guidelines（[7]），有 protocol、5 库自动检索、snowball、手工 venue 扫、inclusion/exclusion、QA、数据抽取与 thematic analysis（[12]）。
3. **字段来源**：
   - publication 元信息字段（title / authors / year / publication type / venue / citations）—— §II.A 第 3 页明确"based on the guidance provided in [12], we extracted publication details"；
   - SLR 抽取字段（# of primary studies, focus of SLR）—— 同段；
   - topic grouping —— §II.A "thematic analysis of titles and abstracts"，Table V 第一列；
   - QA rubric —— Table I 4 项，源自 DARE 经 [8,9,11] 改编；
   - publication-level impact —— Google Scholar citation count（2014-05-19 截止）。
4. **RQ↔样本单位关系**：3 个 RQ 都以 study 为单位（53 SLR），RQ1=topic 分布，RQ2=QA 得分分布（51 study），RQ3=候选 gap 列表；RQ 是字段用途与结果组织口径，不是 schema 根。
5. **降级判定**：无需降级。系统检索、QA、抽取表、taxonomy 均齐全。但 S40 缺 publication 元信息、S3/S8 全文不可得，需以 `missing` 缺失值语义记录。

## 3. 原生样本编码维度树 / 维度森林

```text
ROOT  RE Tertiary Study extraction schema (sample unit = distinct SLR study)
│
├── F1 [PublicationMetadata]  publication-level 字段（per publication, 64）
│   ├── title                              free_text
│   ├── authors                            free_text
│   ├── year                               integer 2006–2014
│   ├── publication_type                   enum{conference, journal, workshop,
│   │                                            tech_report, thesis, unknown}            ← Table III
│   ├── venue_name                         free_text (RE, REJ, IST, ESE, EASE, …)
│   ├── gs_citation_count                  integer (cut-off 2014-05-19)                   ← Table VI
│   └── study_id_grouping                  S-ID with suffix [A][B][C]
│
├── F2 [SLRExtraction]  SLR-level 字段（per study, 53）
│   ├── number_of_primary_studies (#PS)    integer ∈ [5, 4089] ∪ {NF, NM}                 ← Table V
│   ├── focus_of_SLR                       free_text                                      ← Table V col 3
│   ├── slr_type                           enum{conventional_SLR, SMS, meta-analysis}      ← §III
│   └── time_window_of_PS                  optional integer interval (e.g., 1996–2007)
│
├── F3 [TopicGrouping]  thematic taxonomy（per study；topic 可多归属，S26/S39 标 *）
│   topic_group ∈ {                                                                       ← Table V col 1
│       Non-Functional Requirements,
│       Complete RE Process,
│       Model Driven Development,
│       Knowledge Management and RE,
│       RE in GSD,
│       RE in Software Product Lines,
│       Requirements Management,
│       Multi Agent Systems,
│       Requirements Reuse,
│       Value based RE,
│       Virtual Reality Systems,
│       Web Engineering,
│       Creativity in RE,
│       Requirements Elicitation,
│       Stakeholders and users,
│       Requirements Prioritization,
│       Meta Modelling,
│       Software Requirements Specifications,
│       Requirements Verification/Validation/Evaluation,
│       Requirements Traceability,
│       Requirements Change Management,
│       RE Education,
│       Mobile Learning,
│       Checklist for RE
│   }  → 24 个观察到的 group；overlap 用 "*" 注脚
│
├── F4 [ScopeClassification]  方法学外延（per study）                                     ← Table IV
│   scope ∈ enum{
│       state_of_the_art_within_RE,  methods,  techniques,
│       tools,  frameworks,  technology
│   }
│
├── F5 [QualityRubric]  DARE-adapted 4 题（per study, n=51, S3/S8 排除）                  ← Table I
│   ├── QA1 Inclusion/Exclusion Criteria  ∈ {Yes=1, Partial=0.5, No=0}
│   │     - Yes: explicit IE criteria defined
│   │     - Partial: implicit study selection
│   │     - No: no criteria defined
│   ├── QA2 Search Space Adequacy        ∈ {Yes=1, Partial=0.5, No=0}
│   │     - Yes: ≥4 DL + extra strategies
│   │     - Partial: 3–4 DL, no extra
│   │     - No: ≤2 DL or restricted
│   ├── QA3 Quality Assessment of PS     ∈ {Yes=1, Partial=0.5, No=0}
│   │     - Yes: explicit QA described & applied
│   │     - Partial: implicit QA
│   │     - No: no QA
│   ├── QA4 Information on PS            ∈ {Yes=1, Partial=0.5, No=0}
│   │     - Yes: complete info per PS
│   │     - Partial: summary
│   │     - No: not specified
│   └── total_score                      ∈ {0, 0.5, …, 4}
│
├── F6 [SearchExecution]  per source aggregate（非 per study）                            ← Table II
│   source ∈ {Google Scholar, IEEE Xplore, ACM DL, Science Direct, EI Compendex,
│             secondary_search[8,9,10,11], manual_REJ, manual_ESE}
│   ├── papers_found                       integer
│   └── papers_included                    integer
│
└── F7 [GapTaxonomy]  derived candidate findings（per gap-item，不是 per study）           ← §III RQ3
    gap_type ∈ enum{
        anomaly_inconsistent_PS_count,
        lack_of_primary_studies,
        ignored_RE_area
    }
    + cross_reference_target ∈ {
        Nuseibeh&Easterbrook 2000 roadmap[1],
        Cheng&Atlee 2007 roadmap[2]
    }
```

## 4. 叶子维度表（核心叶子，足以重写 review.md）

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leaf-orig-publication-type` | 出版类型 | F1 | Table III | 每篇 publication 的载体类别 | conference / journal / workshop / tech_report / thesis / unknown | 完整枚举（6 档，含 unknown 兜底）| `unknown`：S40 缺 venue 信息 | 类型频次分布 | 出版类型 vs QA 得分交叉表（candidate finding） | E7 | 通用：任何 SLR/tertiary 都可复用此 6 档枚举 |
| `leaf-orig-slr-type` | 综述子类型 | F2 | §III L311–314 | 53 个 study 内部子类型 | conventional_SLR / SMS / meta-analysis | 完整枚举（3 档）| 不允许缺失 | 53 study 的子类型分布（12 SMS, 1 meta, 40 SLR）| 不同子类型 QA 表现差异 | E1, E2 | 可迁移 |
| `leaf-orig-pub-citation` | 引用数 | F1 | Table VI + Appendix A | Google Scholar 引用（2014-05-19 截止）| 整数 ≥ 0 | 数值 | `0` 与"未查到"需区分（Appendix 中均写具体数字） | 中位数 / Top-N | 高引 SLR 是否同时高 QA（Table VI 反证：S2[A] cite=154 但 QA=3, S46 cite=41 QA=1.5）| E11, E14 | 受时间窗影响，可迁移结构 |
| `leaf-orig-ps-count` | 纳入 primary study 数 | F2 | Table V col `# of PS` | 该 SLR 自报的 PS 总数 | 整数 ∈ [5, 4089] ∪ {NM, NF} | 数值或区间 + 哨兵 | `NM`=not mentioned；`NF`=not found | 直方图 / 极差 | "anomaly" finding 直接依赖该字段（S1=8 vs S4=240 同主题）| E9 | 高度可迁移，但 #PS 不一定反映工作量 |
| `leaf-orig-focus-text` | SLR focus | F2 | Table V col 2 | SLR 自报研究焦点的自由文本 | 自由文本 | 自由文本加理由 | 不允许缺失 | thematic clustering 输入 | topic grouping 上层来源 | E9 | 文本字段，需分类才能统计 |
| `leaf-orig-topic-group` | 主题分组 | F3 | Table V col 1 | 由作者 thematic analysis 形成的 24 个 topic group | 24 项枚举（见 §3 F3 列表）| 层级枚举（开放，可由后续工作扩充）| `overlap` 用 "*" 标记 (S26/S39) | 主题覆盖直方图 | RQ1 主结果；RQ3 ignored area 反向推导 | E9 | 不可饱和（作者自承"neither exhaustive nor complete"）；A2a 不应当成封闭枚举使用 |
| `leaf-orig-scope` | scope-of-RE 分类 | F4 | Table IV | SLR 评估对象的方法学外延 | state_of_the_art / methods / techniques / tools / frameworks / technology | 完整枚举（6 档）| 不允许缺失 | 6 档分布（33/7/7/4/1/1）| 是否多数 SLR 仅描述现状缺乏方法学评价 | E8 | 可迁移；6 档自身较稳定 |
| `leaf-orig-qa1` 至 `leaf-orig-qa4` | DARE QA 四题 | F5 | Table I | DARE 改编 4 题 | 每题 ∈ {Yes=1, Partial=0.5, No=0} | 完整枚举（每题 3 档）| `excluded`：S3/S8（n=51 而非 53）| 各题档次频次（Figure 3）；总分分布（Figure 2）| QA3/QA4 半数被忽略 → 候选 finding | E3, E10 | 可作为 RE 之外 SLR-QA 评估的复用模板 |
| `leaf-orig-qa-total` | QA 总分 | F5 | §III RQ2 + Figure 2 | 4 题之和 | ∈ {0, 0.5, 1.0, 1.5, …, 4} | 数值 | 同 QA1–QA4 | "42/51 ≥ 2"；按年度均分 trend | 整体趋势 → final candidate finding (decline since 2009) | E10 | 可迁移 |
| `leaf-orig-search-source` | 检索源 | F6 | Table II | 检索源与命中量 | 5 库 + 4 secondary + manual venues | 关系值 / 数值 | snowball 来源单独列 | 单源命中率 / 漏检风险 | secondary 找到 6 篇（占 9.4%）→ 单一检索口径不充分 | E4, E6 | 可迁移 |
| `leaf-orig-gap-type` | 候选 gap 类别 | F7 | §III RQ3 | 三类 gap | anomaly / lack_of_PS / ignored_area | 完整枚举（3 档）| -- | 每类 gap 列表大小 | RQ3 主结果 + 与 roadmap[1,2] 对照 | E12 | 可迁移作 gap-taxonomy 模板 |
| `leaf-orig-roadmap-ref` | roadmap 参照 | F7 | §III RQ3 + Refs [1][2] | RQ3 与既有 roadmap 的对照锚 | {Nuseibeh&Easterbrook2000, Cheng&Atlee2007} | 外部分类法引用 | -- | 是否覆盖 roadmap topic 的二值矩阵 | 列出 4 个 covered + 4 个 not-covered + 2 个 Nuseibeh-area not covered | E12 | 不可迁移到 RE 之外（roadmap 是 RE-specific）|
| `leaf-orig-limitation-text` | 自报 limitations | ROOT | §IV | 作者自报的 4 类局限 | 4 项（检索完整性 / S40 元信息缺失 / topic-grouping 主观 / EBSE guideline 限定）| 自由文本加理由 | -- | 作 threats-to-validity 字段 | 反证当前 #PS 异常 finding 的强度 | E13 | 通用 |

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel-grouping` | publication（F1）| `belongs_to_study` | study（F2） | S-ID（S1–S53）+ 后缀 [A][B][C] | 不允许缺失 | E14 | 把 64 publications 归并到 53 study |
| `rel-topic-overlap` | study × topic_group | `is_overlap_with` | 另一 topic_group | 至少出现 1 次（S26/S39 同时属于 Knowledge Management 与 RE in GSD）| 默认无 overlap | Table V 注脚 "*" | 提示 topic_group 非互斥 |
| `rel-citation-vs-qa` | study | `top_cited_with_qa` | (citation, qa_total) 二元组 | 数值对 | -- | E11 | Table VI 直接验证"高引≠高质量" |
| `rel-gap-vs-roadmap` | gap | `references_roadmap` | roadmap_topic | covered / not-covered | -- | E12 | 桥接 RQ3 与外部分类法[1][2] |
| `rel-search-source` | source | `feeds` | publications_found / included | 数值对 | -- | E6 | 检索漏检反证 |

## 6. 统计观察、候选 finding 与 final finding 边界

**A. 字段/统计表直接支撑的统计观察**（可在 53/51/64 分母下重算）：

1. 出版类型分布：31 conf + 16 journal + 4 workshop + 4 tech report + 8 thesis + 1 unknown = 64（E7）。
2. SLR 子类型分布：12 SMS + 1 meta-analysis + 40 conventional SLR = 53（E1，§III）。
3. scope 分布：33/7/7/4/1/1（E8）。
4. #PS 极差：max=4089 (S42 meta-analysis 1963–2006), min=5 (S27)；>200 共 4 篇（S21, S25, S24, S4）；100–200 共 5 篇；<10 共 4 篇（E9, §III L344–363）。
5. QA：42/51 ≥ 2；QA3/QA4 各档分布见 Figure 3（待 A2a 视觉读取精确柱高）。
6. 年度发表量：2006–2014，2009 后骤增（Figure 1，A2a 待核）。
7. citation Top-10：见 Table VI（E11）。

**B. 候选 finding（discussion / RQ3 / limitations）**：

1. RE SLR 的整体 QA 年均分自 2009 起下降，与 SE-wide tertiary [8,9] 的"QA 上升"形成对比（§III + Figure 4，候选 trend finding，需视觉核 Figure 4 + 跨论文反证）。
2. 高引 ≠ 高 QA：S2[A] cite=154 但 QA=3；S46 cite=41 QA=1.5（E11）。
3. #PS 内部矛盾：S1 vs S4（同 prioritization）、S24 vs {S4,S21,S25}（state-of-the-art 子集异常）（E12 ①）。
4. RE 子主题覆盖 gap：未被任一 SLR 覆盖的 = {Requirements Scaling, RE for self-management systems, system environment effects, RE research-in-practice effectiveness, conflict resolution, requirements negotiation, goal-oriented RE, RE in law, requirements modeling notations}（E12 ③）。
5. 半数 SLR 忽略 QA3/QA4（E10），可能威胁结果可靠性。

**C. 对 Paper2（LLM 状态机建模综述）可迁移的方法学启发**：

- F1+F2 抽取表 + F5 DARE rubric 是 RE 之外仍稳定的元结构；可作 Paper2 single-paper extraction form 的模板骨架（publication-level vs study-level 分层；统一处理 [A][B][C] 同 study 多发表）。
- F7 三类 gap taxonomy（anomaly / lack-of-PS / ignored-area）与 roadmap cross-ref 模式可作 Paper2 gap-analysis 章节的输出形态参考。
- §IV "Limitations of the study" 4 类局限可作 threats-to-validity 复用清单。
- S40 缺 venue 元信息但仍纳入的做法 → "不完整元信息可保留但应显式标注"的处理范例。

**D. 绝不能迁移**：

- RE-specific topic taxonomy（24 项）、scope 6 档、Nuseibeh / Cheng-Atlee roadmap 的具体 topic 名单 —— 这些是 RE 领域 schema，对 LLM4SE / 状态机建模没有直接映射。
- "QA 自 2009 起下降"这一年度趋势仅限 RE SLR 子集，不能外推到 SE-wide 或其他子领域。
- citation Top-10 名单是 2014-05-19 快照，已过时。

## 7. 对现有 `review.md` 的返修建议（C/I/M 分级）

### C 级（critical — 直接影响维度树作为单篇 schema seed 的可信度）

- **C1. §维度树复原 / §叶子维度表 内容仍以 6 个通用接口叶子 `leaf-*-scope/corpus/taxonomy/method/evidence/finding` 为主，未把原文真实抽取字段（F1–F7 中的 publication_type / SLR 子类型 / #PS / scope-6 档 / QA1–QA4 / topic_group-24 项 / 三类 gap）写入叶子维度表。**
   - 影响：把跨论文通用接口冒充原文 schema，违反 A1-DT v2 "禁止用六个通用 leaf 替代原文结构"硬约束。
   - 返修动作：用本报告 §3 维度森林 + §4 叶子维度表整体替换现有 §维度树复原 / 叶子维度表。保留 §通用接口投影作为附属说明而非主源。

- **C2. §1 快速结论卡片 "阅读状态 / 证据等级 / 是否目标证据池"未反映原文实际已提供完整 Table II–VI + Appendix A 名录 + DARE rubric，仍写"图表/表格细节待人工核对"虽不算错，但"否（A1-DT 阶段仅作 schema seed）"对 F5/F1/F2 这类字段过度悲观。**
   - 影响：SUMMARY 将该论文统计池资格判定为"否"，但原文在 53 study / 51 QA / 64 publications 分母下结构封闭、可统计；正确判定应为"局部可统计"。
   - 返修动作：把 SUMMARY 中"主统计池资格"由"否"改为"局部可统计（F1+F2+F4+F5+F7 可，F3 topic_group 不饱和）"。

### I 级（important — 影响下游 finding 评估和 A2a 任务范围）

- **I1. §快速结论卡片"被编码样本单位"未单独说明 publication vs study 双分母**；现有文本只笼统写"primary study / secondary study"。返修：明确写"sample unit = distinct SLR study (n=53)；publication-level 辅 unit (n=64)；QA 仅 n=51"。

- **I2. §6 类 pattern 抽取 中 "validity / threat pattern: 本轮未完整定位 threat section；需 A2a 深读"是事实错误。** 原文 §IV "Limitations of the study"（paper_content L577–615）已经提供 4 类清晰 limitations。返修：改为"已定位，列 4 项 limitation"。

- **I3. §维度树复原 中"统计与候选发现链路"把 `[dim-...-root]` 标记为"否（A1-DT 阶段仅作 schema seed）"过于一刀切**，与本节 C2 重合。返修：F1 publication_type、F4 scope、F5 QA total、F6 search source 这 4 个维度应升级为"是（在本文分母下可统计）"。

- **I4. §A.2 证据账本仅 4 行（EV-001..004）且全部 `not_verified`**。原文已有 8 张表 + 4 张图直接支撑；应至少为 Table I/II/III/IV/V/VI、Figure 1/2/3/4 各建一行证据条目（合计 ≥10 行），并把 Table I/II/III/IV/V/VI 标 `verified-text-only`、Figure 1–4 标 `needs_pdf_visual_check`。

- **I5. §维度树复原 中 "原文模式候选叶子映射（A1 种子）"仅给出 4 个 `leaf-orig-*-re-topic / secondary-study-quality / impact / method-gap`**，但原文真实抽取字段至少 ≥12 项（见本报告 §4）。返修：用本报告 §4 整表替换 4 项种子。

### M 级（minor — 不阻塞，但建议）

- M1. §1 "CCF 复核状态: 非 CCF venue / workshop" 与"出版形态: 工作坊"重复表述，可保留任一处。
- M2. §3 启发 #2 "`publication_count` 与 `distinct_study_count` 应分开" 已在原文 Table II 落实，可改为"已在原文 Table II 显式区分，验证 schema 是否需要 study_id_grouping 字段"。
- M3. §A.3 全部结论 `weak / schema_seed`，建议至少对 F5 QA rubric / F4 scope 6 档升级为 `medium / verified-text-only`。
- M4. §"原文 schema 主树（19×3 审计后返修）" 表头使用了模糊词（"二级研究质量字段"等），可替换为 F1/F2/.../F7 命名以与本报告一致。
- M5. §"v1-deprecated" warning block 可保留，但建议在其上方加一行"本节 §维度树复原已按 A1-DT v2 单篇审计完整重写，下方两条链接仅作历史参考"。

### SUMMARY 当前表的修正建议

| SUMMARY 字段 | 当前值 | 建议修正值 | 理由 |
|---|---|---|---|
| 样本单位 | （未单独列）| `study (n=53) / publication (n=64) / QA-subset (n=51)` | I1 |
| 样本数量 | （未单独列）| 同上 | I1 |
| 原生树类型 | （未单独列）| `维度森林（F1–F7 七棵子树）` | C1 |
| 统计池资格 | （未单独列）| `局部可统计（F1/F2/F4/F5/F6 可；F3 topic 不饱和；F7 候选）` | C2 |

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-RE-T01 | paper_content.txt | §I Abstract+Intro (L23–105) | 摘要 + 引言目标段 | "53 distinct systematic reviews ... 64 publications" + 三类 SLR 定义 | rq_definition | verified-text | ROOT, F2 | 否 | 仅 RE 子领域 |
| EV-RE-T02 | paper_content.txt | §II.A Planning RQ1–RQ3 (L117–123) | RQ 明文 | RQ1=areas, RQ2=quality, RQ3=gaps | rq_field | verified-text | ROOT, F3, F5, F7 | 否 | -- |
| EV-RE-T03 | paper_content.txt | Table I (L147–178) | QA rubric 4 题 3 档 | DARE 改编；Yes=1/Partial=0.5/No=0 | extraction_form | verified-text | F5 (QA1–QA4) | 否（表已 OCR 完整）| 通用 |
| EV-RE-T04 | paper_content.txt | §II.A 搜索串 + 5 库 (L184–220) | 完整 Boolean 串 + 8 venues snowball | 5 库 + secondary + manual venues | corpus_protocol | verified-text | F4, F6 | 否 | 检索时间 2013-10–2014-05 |
| EV-RE-T05 | paper_content.txt | Table II (L273–288) | 5 库命中数 + 264→91→58→64 + 53 studies | 检索执行汇总 | corpus_chain | verified-text | F6, ROOT | 否 | -- |
| EV-RE-T06 | paper_content.txt | Table III (L317–331) | 31/16/4/4/8/1 | publication type 分布 | statistical_result | verified-text | F1 (publication_type) | 否 | -- |
| EV-RE-T07 | paper_content.txt | Table IV (L364–375) | scope 6 档 33/7/7/4/1/1 | scope of RE SLR | classification_schema | verified-text | F4 | 否 | RE-specific scope 6 档 |
| EV-RE-T08 | paper_content.txt | Table V (L376–429) | topic-group × focus × #PS × year | thematic taxonomy | classification_schema | verified-text | F3, F2 (#PS, focus) | 否（建议 PDF 复核字符 NF/NM 替代字符 `barb2right` OCR 杂讯） | topic_group 非饱和 |
| EV-RE-T09 | paper_content.txt | Table VI (L482–493) | Top-10 cited × QA score | citation vs QA | candidate_finding_support | verified-text | rel-citation-vs-qa, F1, F5 | 否 | 2014-05-19 截止 |
| EV-RE-T10 | paper_content.txt + paper.pdf | Figure 1 (L316) | yearly distribution 柱状图 | 2009 后骤增 | statistical_result | needs_pdf_visual_check | F1 (year), trend | 是 | -- |
| EV-RE-T11 | paper_content.txt + paper.pdf | Figure 2 (L443–449) | QA total score 分布 | 42/51 ≥ 2 | statistical_result | needs_pdf_visual_check | F5 (qa_total) | 是（OCR y 轴断版） | -- |
| EV-RE-T12 | paper_content.txt + paper.pdf | Figure 3 (L444–449) | QA1–QA4 各档计数 | QA3/QA4 半数忽略 | statistical_result | needs_pdf_visual_check | F5 (QA1–QA4) | 是 | -- |
| EV-RE-T13 | paper_content.txt + paper.pdf | Figure 4 (L481) | 年度均分曲线 | 自 2009 起下降 | candidate_finding_support | needs_pdf_visual_check | F5 (qa_total) × year | 是 | trend 仅限 RE SLR |
| EV-RE-T14 | paper_content.txt | §III RQ3 (L505–576) | 三类 gap + roadmap 对照 | anomaly / lack_of_PS / ignored_area | candidate_finding | verified-text | F7, rel-gap-vs-roadmap | 否 | 不可迁移 ignored-area 具体名单 |
| EV-RE-T15 | paper_content.txt | §IV Limitations (L577–615) | 4 类局限 | 检索/S40/grouping/EBSE | limitation | verified-text | ROOT, F7 | 否 | 通用 |
| EV-RE-T16 | paper_content.txt | Appendix A (L697–967) | S1–S53 完整名录 | study + publication 列表 | corpus_inventory | verified-text | F1, F2, rel-grouping | 否 | -- |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-RE-T01 | 本文是按 EBSE guidelines 执行的 systematic mapping tertiary study，样本单位为 distinct SLR study（n=53），辅以 publication（n=64）；QA 在 n=51 上施加 | study_type | ROOT | EV-RE-T01, T02, T04, T05, T16 | strong | 可直接迁移至 Paper2 single-paper schema | S40 元信息不全；S3/S8 全文不可得 |
| C-RE-T02 | 原生编码 schema 是 F1–F7 七棵子树构成的维度森林，叶子层至少 12 项原文真实字段 | tree_type | ROOT, F1–F7 | EV-RE-T03, T05–T09, T14 | strong | 替换 review.md 通用六叶 | F3 topic_group 非饱和 |
| C-RE-T03 | DARE-adapted QA rubric (Table I, 4×3 档) 是稳定可复用的 SLR-QA 评估元模型 | classification_schema | F5 | EV-RE-T03 | strong | 可直接迁移至 Paper2 QA 评估 | EBSE guideline 受限于 2007 版 |
| C-RE-T04 | scope 6 档分类（Table IV）在 RE 之外仍部分可迁移（state_of_the_art / methods / techniques / tools / frameworks / technology 六分） | classification_schema | F4 | EV-RE-T07 | medium | 可作 Paper2 单篇 scope 字段候选 | 6 档自身是 SLR 抽象类，但具体含义须本地化 |
| C-RE-T05 | topic-group taxonomy (24 项) 是 RE-specific 非饱和分类，不可外推 | taxonomy_local | F3 | EV-RE-T08 | medium | 仅作 Paper2 "topic_grouping = 自由文本 + 后处理 cluster" 的设计参考 | 作者自承 not exhaustive |
| C-RE-T06 | 候选 finding"RE SLR QA 自 2009 起下降，与 SE-wide [8,9] 趋势相反"基于 Figure 4 趋势 | candidate_finding | F5 × year | EV-RE-T11, T13 | weak | 不进入主统计池；A2a 视觉读 Figure 4 后可升级 | 仅 RE 子领域 |
| C-RE-T07 | 高引 ≠ 高 QA（Table VI 反证：S2[A] cite=154 QA=3 vs S46 QA=1.5）| candidate_finding | rel-citation-vs-qa | EV-RE-T09 | medium | 可作 Paper2 "citation 不能替代 QA" 论证 | citation 是 2014-05-19 快照 |
| C-RE-T08 | 三类 gap taxonomy（anomaly / lack_of_PS / ignored_area）+ 与 roadmap cross-ref 模式可作 Paper2 gap 章节模板 | candidate_finding_template | F7, rel-gap-vs-roadmap | EV-RE-T14 | medium | 通用模板可迁移 | 具体 RE ignored-area 名单不可迁移 |
| C-RE-T09 | publication-level 字段（type, year, venue, citations）与 study-level 字段（#PS, focus, slr_type）应分层；同 study 多发表用 [A][B][C] 合并是稳定模式 | extraction_form | F1, F2, rel-grouping | EV-RE-T03 (form ref), T16 | strong | 可直接复用 | -- |
| C-RE-T10 | 自报 limitations 的 4 类清单（检索 / 元信息缺失 / grouping 主观 / EBSE 限定）反证若干候选 finding 强度 | limitation_anchor | ROOT, F7 | EV-RE-T15 | strong | 可作 Paper2 threats-to-validity 复用清单 | -- |

## 9. 技能使用与自我审查记录

### 技能文件使用记录

| 文件 | 读取状态 | 采用要点 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | partial（L1–50）| 采用"claim-evidence-engineering workflow"原则，所有候选 finding 必须显式标证据；不发明引用 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | full（L1–111）| 采用"Constructive Specificity Standard"——审计意见须 specific 到节/字段/表号，C/I/M 分级以"是否影响研究目标 / 实验可靠性 / 复现性"为锚 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | blocked | 本轮未读全文（222 行），仅靠 reviewer-guidelines 推得自审风险三点（见下）；记录为 partial-blocked |
| `research-planning/SKILL.md` | partial（L1–50）| 采用"data → model → training → evaluation → writing"依赖顺序观，作为 A2a 精核任务依赖排序的元参考 |
| `research-planning/references/planning-prompts.md` | not_read | blocked（本任务深度足以从 SKILL.md 推得；如下游需更细 prompt 模板再读）|
| `research-planning/references/output-schemas.md` | not_read | 同上 |
| `oh-my-codex/.../autoresearch/SKILL.md` | not_read | blocked：本机文件存在性未校验；记录为风险项 |

### Reviewer 自审：本输出最高 3 项风险

1. **图表视觉级数据未核（C 级潜在风险）**：本审计完全基于 `paper_content.txt`，未打开 `paper.pdf` 检视 Figure 1–4。EV-RE-T10..T13 均标 `needs_pdf_visual_check`。候选 finding C-RE-T06 "QA 自 2009 起下降" 严重依赖 Figure 4 视觉读数，若 A2a PDF 复核发现年度均分实际只是噪声波动而非单调下降，则 C-RE-T06 应降级为 `not_verified` 或废弃。主线程合并时复核入口：A.4 应新增 `cmd-pdf-figures-check`。
2. **topic-group taxonomy 饱和度判断主观**：F3 列出 24 项是 OCR 文本统计结果（Table V 第一列），但 Table V 跨页且 OCR 中混入了 "*" 注脚、`barb2right` 替代字符等杂讯，可能漏数 1–2 个 group。建议 A2a 用 PDF 重新计数并比对作者自承 "neither exhaustive nor complete"（§III L552–555）。
3. **C/I/M 分级可能高估了 C2**：把 "review.md 主统计池资格判'否'" 标 C 级或许偏激进——按本仓库《学术研究仓库 Review 口径规范》§3，单篇 schema seed 在 A1-DT 阶段保守判'否'本身不直接破坏学术目标，是否应降为 I 级取决于 SUMMARY 是否真在该口径下漏掉了可统计 sample。主线程合并时建议复读 SUMMARY 当前对该 paper 的统计字段，再决定是否接受 C2 升级建议。

### 任务状态

- 未出现 blocked / timeout / 文件缺失致命问题。
- `reviewer-self-review.md` 与 `research-planning/references/*` 与 `oh-my-codex autoresearch/SKILL.md` 标记为部分未读，不影响本审计核心结论；若后续审计要求更细化的 self-review 流程，建议在 A2a 阶段补读。
- 本报告不修改任何仓库文件，不执行 git commit / push / gh，仅作为 main session 重写 `review.md` 的事实输入。

---

`★ Insight ─────────────────────────────────────`
1. 这篇 2014 RE tertiary study 是难得的"教科书级"清晰原生 schema：publication 与 study 双分母、DARE 4×3 档 QA rubric、scope 6 档 + topic 24 项、Appendix A 完整 S1–S53 名录 + citation。这种结构让 single-paper schema 几乎可以 1:1 复用为 Paper2 single-paper extraction form 的骨架——也正因为如此，旧 `review.md` 把它折叠成六个通用 leaf 是最大的损失。
2. 关键提醒：F3 topic_group 是 thematic-analysis 结果（开放 / 非互斥 / 非饱和），与 F4 scope（先验 6 档枚举）属于结构上完全不同的两种 taxonomy；审计返修必须保留这一差异，不能简化为同一种"分类字段"。
3. C-RE-T07（"高引 ≠ 高 QA"）是 Paper2 Related Work / Discussion 可直接引用的方法学论点——Table VI 自带的 S2[A] vs S46 对比比 reviewer 自己造例子更有说服力。
`─────────────────────────────────────────────────`
