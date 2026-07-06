我已完成全文阅读，包括 Table 3 抽取表、Table 5 guideline 比较矩阵、Table 7 research type 决策表、Table 8 actions rubric、Tables 9–13 scoring rubrics、Tables B.15–B.27 附录映射表。现在输出完整审计报告。

---

# A1-DT v2 单篇全文审计报告 — petersen-2015-mapping-guidelines-update

`★ Insight ─────────────────────────────────────`
- Petersen 2015 是一个**双重身份**论文：既是 systematic mapping study（n=52 mapping studies），又是 guideline update。它的"维度森林"因此天然有两棵主树：一棵描述"作者如何 *编码他们的 52 个样本*"（extraction form + classification facets），另一棵描述"作者向后续研究者 *建议* 的 guideline checklist"（Table 8 + Tables 9–13 rubrics）。把它们合并成一棵会丢掉关键事实。
- 已存 `review.md` 的核心缺陷是：A1-DT v2 章节里 `leaf-*` 六叶仍然是通用模板（scope/corpus/taxonomy/method/evidence/finding），而该 SMS 真实的叶子是 Table 3 的 12 个 extraction items + Section 4.4 的 6 个 classification facets + Tables 9–13 的 4 个 ordinal rubrics。这是把"跨论文投影"误读成"原文叶子"的典型样本。
- 取值空间证据强度方面：Table 7 (research type 决策表) 给出了**封闭枚举 + 真值表**，这是 A1-DT v2 罕见的"完整 boolean schema"证据；Tables 9–13 给出**封闭 ordinal scale**；Tables B.15–B.27 给出**逐研究映射的关系边**。这些都应是 verified 而非 not_verified。
`─────────────────────────────────────────────────`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2015-mapping-guidelines-update` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；完整通读 1973 行（18 页全部，含 §1 引言至 §6 结论、Appendix A 包含/排除清单、Appendix B 表 B.15–B.27、References）。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；二者元信息一致，DOI=10.1016/j.infsof.2015.03.007，IST 卷 64 (2015) pp. 1–18。 |
| 是否打开或核对 `paper.pdf` | 否（本轮以 `paper_content.txt` 全文为主，文本提取对所有 Table/Figure caption 和正文均可见；未做图表视觉级人工核对，复杂图(Fig.1 数字链、Fig.16 partition 图)留待 A2a）。 |
| 原文类型 | **SLR / SMS / guideline 混合**：systematic mapping study of systematic mapping studies (tertiary 性质) + guideline update。 |
| 被编码样本单位 | **primary study = SE 领域已发表的 systematic mapping study**（每个 study 被作者按 Table 3 抽取表编码）。 |
| 样本数量 / 分母 | **52 mapping studies**（Appendix A 列出 ~52 个 included id；§3.6.2 与 §4.4.3 多处复现 "52" 分母）。Fig. 1 流程链：7752 → 5082 (去 2004 前) → 60 (title/abstract) → 43 (full-text) → 54 (+11 snowball) → 44 (quality) → 52 (review of excluded 回补 8) 。 |
| 原生树类型 | **维度森林**（至少 4 棵互相独立的主干树：①extraction form 树；②classification facet 树；③guideline action / rubric 树；④validity taxonomy 树）。 |
| 主统计池资格 | **是（限方法学统计池）**。所有 Appendix B 表 (B.15–B.27) 是逐研究 study→category 的关系边映射，全部分母=52，可直接进入方法学频次统计；不可用于"目标 SE 主题效果/因果"统计池。 |
| 总体判定 | **needs repair**：现有 `review.md` 的 A1-DT v2 主表仍以六个通用 leaf 为主干；原文丰富的 native 字段（Table 3 / Section 4.4 / Tables 9–13 / Tables B.15–B.27）未被升级到叶子层，证据强度被低估为 `not_verified`/`schema_seed`。需要做"森林化"返修，把多棵原文树并列展开。 |

## 1. 原文证据阅读说明

**阅读范围**：完整通读 `paper_content.txt` 1–1973 行（18 页 + 18 页 References）；逐节核对 §1 Introduction、§2 Background and related work、§3 Method (含 §3.1 RQ, §3.2 Search, §3.3 Selection/QA, §3.4 Data extraction Table 3, §3.5 Analysis, §3.6 Validity 5 子节)、§4 Results (含 4.1 频度、4.2 Topics SWEBOK、4.3 Venue、4.4 Process 含 4.4.1–4.4.6)、§5 Guideline updates (含 §5.1 Planning 5 子节、§5.2 Conducting、§5.3 Reporting、§5.4 Evaluate 含 Tables 8–14、§5.5 Dissemination)、§6 Conclusions、Appendix A、Appendix B (Tables B.15–B.27)、References 1–100。

**仅基于 text 的局限**：(a) Fig. 1 的数字流程链 `-10-17-5022-2666` 文本提取后顺序错乱，分母重建需 PDF 视觉核验；(b) Fig. 16 (Badampudi partition 圆 + snowball 三角) 是视觉示意，无法仅靠文本理解；(c) Fig. 3 / Fig. 4 / Fig. 5 / Fig. 7–15 的具体柱条数值只能从 Tables B.15–B.27 倒推（B 表给出 study list，可数得到，但需精核）；(d) Tables 9–13 的"bold 高亮分数"在文本中丢失，需 PDF 复核本研究自身的 rubric 评分位置。

**5–12 个最关键原文证据锚点**：

| # | 证据锚点 | 章节 / 表图 | 短引或释义 |
|---|---|---|---|
| E1 | RQ 1–4 全文表述 | §3.1 (line 217–229) | "RQ1: Which guidelines are followed... RQ2: Which SE topics are covered... RQ3: Where and when... RQ4: How was the systematic mapping process performed?" |
| E2 | Table 3 数据抽取表（12 字段）| §3.4 / Table 3 (line 392–408) | Study ID / Title / Author / Year (RQ3) / Area in SE = SWEBOK (RQ2) / Venue (RQ3) / Guidelines adopted (RQ1) / Search strategy (RQ4) / Search type {manual, automated, both} (RQ4) / Classification schemes (RQ4) / Visualization type (RQ4)。 |
| E3 | 选择流程链 + 52 分母 | §3.3 / Fig. 1 / §3.6.2 | "57 primary studies"(snowball 后) → "52 mapping studies" (final, §3.6.2)；§4.4.3: "only 14 out of 52 studies"。 |
| E4 | Topic-independent facet 五元封闭枚举 | §4.4.4 / Fig. 12 / Table B.24 | Research type, Research method, Study focus, Contribution type, Venue。"Three new dimensions not highlighted by Petersen et al. [2] have been identified, namely venue, study focus, and research method." |
| E5 | Research type 6 类封闭枚举 + 真值表 | Table 7 (line 1310–1326) + §4.4.4 | Evaluation research / Solution proposal / Validation research / Philosophical / Opinion / Experience；R1–R6 真值表 6 conditions × 6 decisions（Used in practice, Novel solution, Empirical evaluation, Conceptual framework, Opinion about something, Authors' experience）。 |
| E6 | Search 子树（3+5+4+3 封闭枚举）| §4.4.2 / Figs 6–9 / Tables B.18–B.21 | 搜索策略: {database, snowballing, manual}；发展: {PICO, expert/librarian, iterative, keywords-from-known, standards}；评估: {test-set, expert eval, key authors' webpages, test–retest}；纳排: {objective criteria, additional reviewer + consensus, decision rules}。 |
| E7 | Visualization 6 类封闭枚举 | §4.4.5 / Fig. 14 / Table B.26 | {line, pie, bar, bubble, Venn, heatmap}。 |
| E8 | Validity 5 类 taxonomy | §3.6 / §5.1.5 | {Descriptive, Theoretical, Generalizability (内部/外部), Interpretive (≈ conclusion), Repeatability}。 |
| E9 | Table 5 guideline 比较矩阵 | §5 / Table 5 (line 775–840) | 9 guidelines × 30+ activities × {适用 ✓ / 不适用 ✗}；展示本研究合成的"完整 activity 全集"。 |
| E10 | Tables 8–13 rubric + Table 14 评分分布 | §5.4 / Tables 8–14 | 26 actions × 4 phases；4 rubrics(need / search strategy / search evaluation / extraction-classification) ordinal scale {0,1,2,3}，1 rubric(validity) {0,1}；Table 14: 52 studies 在每个 rubric 上的频次分布。 |
| E11 | Tables B.15–B.27 逐研究关系边 | Appendix B (line 1559–1801) | 13 张关系表（topic, venue, guideline, search strategy, search dev, search eval, inc/excl, QA, data extraction, topic-indep, topic-related, visualization, validity），全部分母=52。 |
| E12 | Validity threats 自评（§3.6.2 单人筛选）| §3.6.2 (line 432–438) | "The study selection was conducted by an individual author, which is the main threat to validity"；缓解：first author 复审 + reference-set 验证。 |

## 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象**：52 篇 SE systematic mapping studies（含部分 tertiary studies），样本单位是"published SE systematic mapping study"。Appendix A 给出 included 与 excluded 完整 reference id 清单。
2. **是否有系统检索 / 纳排 / 数据抽取 / 编码方案**：**完全有**。Table 1 给出 4 个数据库的精确检索串；Table 2 给出每个 db 的命中数；Fig. 1 给出完整 PRISMA-like 流程链；§3.3 给出明确 inclusion / exclusion 标准（6+4 条）+ snowball；§3.3 给出 3 题 quality assessment；Table 3 给出 12 字段 extraction form；§3.5 给出"theme grouping then counting"分析方法。
3. **字段来源**：
   - **Extraction form**：Table 3 (Section 3.4)，每个字段直接绑定到一个 RQ。
   - **Classification schema**：双层 — (i) Section 4.4.4 + Fig. 12 + Table B.24 给出 topic-independent facets 5 项；(ii) Section 4.4.4 + Fig. 13 + Table B.25 给出 topic-specific {emerging, existing scheme}；(iii) Table 7 给出 research type 真值决策表，是 Wieringa et al. [11] 的精化。
   - **Quality rubric**：Tables 8–13 + Table 14 (Section 5.4)，作者自行构造的 4+1 rubric。
   - **Validity taxonomy**：来自 Petersen & Gencel [29]，5 类。
   - **Reporting structure**：§5.3 给出 6 部分推荐结构。
   - **Mapping table**：Table 5 (Section 5) 比较 9 个既有 guideline × 30+ activity 的覆盖度。
4. **RQ 与样本单位关系**：RQ 不是"树根"，而是 **extraction form 字段的 owner**（Table 3 的 RQ 列把每个字段绑到 RQ1/2/3/4）。Section 4 按 RQ 组织结果。因此 RQ 在维度森林中扮演的是"字段 owner / 结果组织维度"，而非主树根。
5. **是否无系统样本库**：**有**。无需降级；本文具备完整 SMS 证据链，分母=52 稳定且可追溯到 Appendix B 各表。降级仅适用于:把它当 *Paper2 目标领域* 的统计源，而非把它本身当 SMS。

## 3. 原生样本编码维度森林

本文有 **4 棵互相独立的主干树**，每棵服务不同的作者目的。把它们合并为单树会破坏取值空间语义。

```text
[FOREST-ROOT] Petersen 2015 mapping guidelines update (n=52 included SE mapping studies)

== TREE 1: Data Extraction Form (Section 3.4 / Table 3) — 作者编码 52 篇所用 schema ==
T1-extraction-form
├── general/
│   ├── study_id ::= Integer
│   ├── article_title ::= str
│   ├── author_name ::= set<str>
│   ├── year_of_publication ::= Year [2007..2012] (RQ3)
│   ├── area_in_se ::= SWEBOK_KA ∪ {Education, Research methods} (RQ2; Table B.15: 11 buckets)
│   └── venue ::= str (RQ3)
└── process/
    ├── guidelines_adopted ::= multi-select<10 guideline labels> (RQ1; Fig.5, Table B.17)
    ├── search_strategy ::= multi-select<{database, snowballing, manual}> (RQ4; Fig.6, B.18)
    ├── search_type ::= {manual, automated, both} (RQ4)
    ├── classification_schemes ::= str → see TREE 2 (RQ4)
    └── visualization_type ::= multi-select<6-label closed enum> (RQ4; Fig.14, B.26)

== TREE 2: Classification Facet Tree (Section 4.4.4) — 作者发现的 facet 模式 ==
T2-classification-facets
├── topic_independent/  (Fig.12, B.24)
│   ├── research_type ::= ∈ {evaluation, solution_proposal, validation, philosophical, opinion, experience}
│   │   └── decided_by ::= boolean truth-table (Table 7: R1..R6 over 6 conditions)
│   ├── research_method ::= multi-select<{survey, case_study, controlled_experiment, action_research,
│   │     ethnography, simulation, prototyping, mathematical_analysis}> (§5.1.3 / Fig.19)
│   │   └── linked_to_research_type ::= validation_set ∪ evaluation_set ∪ both (Fig.19 真值映射)
│   ├── study_focus ::= ∈ {academic, industrial, government, project, organization} (§4.4.4)
│   ├── contribution_type ::= ∈ {process, method, model, tool, metric} (Wieringa et al.)
│   └── venue_classification ::= 4-level hierarchical enum (Fig.18; ministry of education FIN scheme:
│         peer_reviewed{journal, review, book_chapter, conf} | non_refereed{...} | professional |
│         general_public | artistic | thesis{BSc, MSc, Lic, PhD} | patents | AV/software)
└── topic_specific/  (Fig.13, B.25)
    ├── emerging_scheme ::= produced via keywording (open-coding-like, §5.1.3)
    └── existing_scheme ::= ∈ {SWEBOK, IEEE std, ISO/IEC std, ACM Thesaurus, ...}

== TREE 3: Mapping Process Activity / Guideline Action Tree (Section 5 / Table 5 / Table 8) ==
T3-process-activity-rubric
├── planning/
│   ├── need_identification ::= {motivate, define_objectives, consult_audience}
│   ├── study_identification/
│   │   ├── choosing_search_strategy ::= ⊆ {database, snowball, manual}
│   │   ├── developing_search ::= ⊆ {PICO(C), consult_experts, iterative, keywords_from_known, standards}
│   │   ├── evaluating_search ::= ⊆ {test_set, expert_eval, key_authors_webpages, test_retest}
│   │   ├── inclusion_exclusion ::= ⊆ {objective_criteria, additional_reviewer+consensus, decision_rules}
│   │   │   └── decision_rule_states ::= 6-cell matrix (Table 6: R1×R2 ∈ {Inc, Unc, Exc}² → A..F)
│   │   └── quality_assessment ::= bool
│   ├── data_extraction_classification ::= as TREE 2
│   ├── visualization ::= ⊆ {line, pie, bar, bubble, Venn, heatmap}
│   └── validity_threats ::= as TREE 4
├── conducting ::= {record_all_stages, iterative_revisions, tool_use}
└── reporting ::= structured-template {Intro, RelatedWork, Method (RQ/Search/Selection/Extraction/
        Analysis-Classification/Validity), Results, Discussion/Conclusion, Appendix}

  ── 评分 rubric 层（5 个独立 rubric，Tables 9–13）：
     R9-need_for_review        ::= ordinal {0:None, 1:Partial, 2:Full}
     R10-choosing_search       ::= ordinal {0:None, 1:Min(2策略), 2:Full(3策略)}
     R11-evaluation_of_search  ::= ordinal {0,1,2,3}  (复合 search reliability + inc/excl reliability)
     R12-extraction_class      ::= ordinal {0,1,2,3}
     R13-study_validity        ::= ordinal {0:no_threats, 1:threats_described}

== TREE 4: Validity Threats Taxonomy (Section 3.6 / 5.1.5) ==
T4-validity-taxonomy
├── descriptive_validity ::= mitigations {data_collection_form, revisitable_extraction}
├── theoretical_validity ::= sub-threats {publication_bias, researcher_bias_in_selection,
│   │                              sample_population_quality, term_confusion}
│   └── mitigations ::= {backward_snowball, reference_set_validation, two-reviewer}
├── generalizability ::= {internal, external}
├── interpretive_validity ::= ≈ conclusion validity
└── repeatability ::= {detailed_reporting, guideline_use}
```

> 注：每棵树都可独立产出统计。例如 Table B.18 给出 T1 中 search_strategy 字段在 52 篇上的逐研究映射；Table B.24 给出 T2 中 topic_independent facet 的逐研究映射；Table 14 给出 T3 rubric 的频数分布；§4.4.6 + Table B.27 给出 T4 是否被讨论的 52 分母二值统计。

## 4. 叶子维度表（精选 14 个有完整原文证据的叶子；非全集）

> 说明：仅列出**有原文封闭枚举 / 数值分母 / 真值表 / ordinal scale**的核心叶子；T1 的 study_id/title/author 等 trivial general fields 省略。完整叶子全集 ≥30 项，留 A2a 精核。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L01 area_in_se | SWEBOK 知识域 | T1.general | Table 3 (RQ2) + Table B.15 | mapping study 所属 SE 知识域 | 11 类: software_quality / tools&methods / process / management / configuration / testing / construction / design / requirements / research_methods / education | 层级枚举 (SWEBOK + 2 新增) | 不可缺；52 全覆盖 | 主题分布频次 (52 分母, Table B.15) | 识别 SE 主题覆盖 gap (e.g., education, config mgmt 弱) | E2, E11, §4.2 | SWEBOK 时代差异需注意；现代主题需扩展 |
| L02 guidelines_adopted | 所采用 guideline | T1.process | Table 3 (RQ1) + Fig.5 + Table B.17 | 该 study 引用为方法依据的 guideline | 10 项封闭枚举: {Kitchenham2004, Kitchenham&Charters2007, Petersen2008, Budgen2008, Arksey&O'Malley2005, Dybå&Dingsøyr2008, Bailey2007, Petticrew&Roberts2006, Biolchini2005, Jorgensen&Shepperd2007, Durham_template} | multi-select 封闭枚举 (集合并集) | 0 也是有效值 (无 guideline) | 24/52 用 >1 guideline (§4.4.1) | 揭示 guideline 不足 → motivate update | E2, E11, §4.4.1 | 仅限 SE SMS 内；不能迁移到 ML/NLP venues |
| L03 search_strategy | 搜索策略组合 | T1.process / T3.study_identification | Table 3 (RQ4) + Fig.6 + Table B.18 | study 实际采用的 search 渠道 | {database, snowballing, manual} 任意子集 | multi-select 封闭枚举 | 不可缺；至少 1 项 | 52 分母频次；最常见 = database (49/52 from B.18) | snowball-only / manual-only 极少 → 暴露过度依赖 db search 风险 | E2, E6, E11 | 适用 SMS；SLR 可能侧重不同 |
| L04 search_development | 搜索开发策略 | T3.study_identification | §4.4.2 + Fig.7 + Table B.19 | 构造 search string 的方法 | {PICO(C), expert/librarian, iterative_improvement, keywords_from_known_papers, standards/encyclopedia/thesaurus} 子集 | multi-select 封闭枚举 | 可缺（部分 study 未报告）| 频次见 B.19；PICO=11, keywords_from_known=11, standards=7 | 识别低使用率但有效的策略 (e.g., PICO 仅 11/52) | E6, §4.4.2, Table B.19 | -- |
| L05 search_evaluation | 搜索评估策略 | T3.study_identification | §4.4.2 + Fig.8 + Table B.20 | 验证检索完整性的方法 | {test_set_of_known_papers, expert_evaluates_result, key_authors_webpages, test_retest} 子集 | multi-select 封闭枚举 | 可缺；许多 study 无评估 | test_set=8, expert=1, webpages=1, test_retest=1 (B.20) | 暴露 search 不被验证的普遍问题 | E6, §4.4.2 | -- |
| L06 inc_excl_strategy | 纳排可靠性策略 | T3.study_identification | §4.4.2 + Fig.9 + Table B.21 + Table 6 | 提高 inc/excl 可靠性的策略 | {identify_objective_criteria, additional_reviewer+consensus, decision_rules} 子集 | multi-select 封闭枚举 + Table 6 状态矩阵 | 可缺 | additional_reviewer 最常用 | 揭示 decision_rules 仅 4/52 使用，但 Ali&Petersen 证明有效 | E6, Table 6, Table B.21 | -- |
| L07 quality_assessment | 是否做 QA | T3.study_identification | §4.4.3 + Fig.10 + Table B.22 | 是否对 primary studies 做质量评估 | {yes, no} | 布尔 | 不可缺；52 全覆盖 | 14/52 yes; 38/52 no (§4.4.3) | "QA 在 SMS 中并不强制" 的直接证据 | E11, §4.4.3 | -- |
| L08 data_extraction_reliability | 抽取可靠性策略 | T3.data_extraction_classification | §4.4.4 + Fig.11 + Table B.23 | 提高 extraction 可靠性的方法 | {identify_objective_criteria, additional_reviewer+consensus, test_retest} 子集 | multi-select 封闭枚举 | 可缺 | 频次见 B.23 | 与 inc/excl 模式相似但 N 更低，揭示薄弱环节 | §4.4.4, Table B.23 | -- |
| L09 topic_independent_facets | 主题无关分类 facet | T2.topic_independent | §4.4.4 + Fig.12 + Table B.24 | 该 study 使用的横向分类维度 | {research_method, research_type, study_focus, contribution_type, venue} 子集 | multi-select 封闭枚举 | 可缺 (一些 study 无 facet) | venue=27, research_type=21, research_method=17, study_focus=11, contribution_type=6 | 揭示 venue/method/type 是主流；contribution_type 边缘化 | E4, E11, §4.4.4 | -- |
| L10 research_type | 研究类型分类 | T2.topic_independent.research_type | Table 7 (§5.1.3) | 单个 primary study 的研究类型 | {evaluation_research, solution_proposal, validation_research, philosophical_paper, opinion_paper, experience_paper} | 完整封闭枚举 (Wieringa et al. + Table 7 真值表) | 决策表必返回 ≥1 | 真值表精确判定 (T/F over 6 条件) | Table 7 真值表可直接迁移作为 Paper2 编码规则 | E5, Table 7 | research type 真值表对 LLM agent 抽取尤其有用 |
| L11 research_method | 研究方法 | T2.topic_independent.research_method | §5.1.3 + Fig.19 | 实证方法分类 | {survey, case_study, controlled_experiment, action_research, ethnography, simulation, prototyping, mathematical_analysis} | 封闭枚举 + Fig.19 双归属映射 (validation vs evaluation) | -- | 多分类 (一个 method 可属两类) | Fig.19 给出 method→research_type 关系边 → 可作完整性约束检查 | E4, Fig.19, §5.1.3 | -- |
| L12 visualization_types | 可视化类型 | T1.process / T3.planning.visualization | Table 3 (RQ4) + Fig.14 + Table B.26 | study 用的呈现方式 | {line, pie, bar, bubble, Venn, heatmap} 子集 | multi-select 封闭枚举 | 可缺 | bar=22, bubble=23, pie=12, line=2, Venn=3, heatmap=1 (B.26) | heatmap 严重低使用 (1/52) 是潜在 finding | E7, E11 | -- |
| L13 validity_taxonomy | 效度分类 | T4 | §3.6 + §5.1.5 | study 报告的 validity 维度 | {descriptive, theoretical, generalizability_internal, generalizability_external, interpretive, repeatability} | 封闭枚举 (5 类 + repeatability) | 可缺 | 45/52 报告 validity (B.27) | 暴露 7/52 不报告 → 报告规范缺失 | E8, E11, §5.1.5 | 现代风险 (LLM/provider drift) 需另立 |
| L14 rubric_scores | 质量评分 (4+1 rubric) | T3 评分层 | Tables 9–13 + Table 14 | 该 study 在每个 rubric 上的得分 | need∈{0,1,2}, search_strat∈{0,1,2}, search_eval∈{0,1,2,3}, extract_class∈{0,1,2,3}, validity∈{0,1} | 5 独立 ordinal scale | 全部强制评分 | Table 14 给出 52 篇分布；median ratio=33% (§5.4) | 这是首个 SMS 的 quality rubric 实证分布，可作 baseline | E10, Tables 9–13, Table 14 | rubric 仅适合 SMS，不能直接套到 SLR / experimental |

## 5. 关系边表

本文 native schema 富含**显式关系边**：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R01 study↦guideline | primary_study | adopts | guidelines_adopted | 10 项 (L02) 子集 | 0=未声明 | Table B.17 | 频次 + co-occurrence (24/52 used >1) |
| R02 study↦area | primary_study | covers | area_in_se | SWEBOK 11 类 (L01) | 必填 | Table B.15 | 主题分布；gap 识别 |
| R03 study↦venue | primary_study | published_in | venue_classification | Fig.18 4 级层级 | 必填 | Tables 4, B.16 | venue 集中度；top-3 = IST(14), EASE(8), ESEM(4) |
| R04 study↦search_strategy | primary_study | uses | search_strategy | L03 子集 | 必填 | Table B.18 | -- |
| R05 study↦topic_indep_facet | primary_study | classified_by | topic_independent_facets | L09 子集 | 可空 | Table B.24 | facet 选择模式 |
| R06 research_method↦research_type | research_method | 归属 | {validation, evaluation, both} | Fig.19 双向映射 | -- | Fig.19, §5.1.3 | **schema 内在约束**：可用作 Paper2 自动一致性检查 |
| R07 study↦rubric_action | primary_study | applied | rubric_action (26 items) | 0/1 (Table 8 形态) | -- | Table 8 + Table 14 | 给出 quality ratio |
| R08 guideline↦activity | guideline (10 项) | covers | activity (Table 5 中 30+ activities) | {✓, ✗} | -- | Table 5 | guideline 完整度对比矩阵 (本文核心贡献之一) |
| R09 inc/excl decision | reviewer pair (R1, R2) | combines_to | decision_state | {A, B, C, D, E, F} via Table 6 | -- | Table 6 | 决策规则代数 |
| R10 research_type decision | study traits | maps_to | research_type | Table 7 R1..R6 真值表 | 真值表覆盖全部组合 | Table 7 | **完整 boolean schema**, A2a 可直接复用 |

> 说明：R06、R08、R09、R10 是本文最有价值的**结构化关系**，远超普通 SMS 的字段平铺。Paper2 应优先借鉴这些"schema 内一致性约束"模式。

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段 / 统计表支持的统计观察（强证据，分母明确）

| 统计观察 | 证据 | 分母 |
|---|---|---|
| Kitchenham&Charters [1] 与 Petersen [2] 是最常用的两个 guideline；24/52 study 用 >1 guideline | §4.4.1, Fig.5, Table B.17 | 52 |
| 数据库检索是最常用搜索策略；snowball/manual 仅作补充 | Table B.18 | 52 |
| 仅 14/52 (27%) study 做了 quality assessment | §4.4.3, Fig.10, Table B.22 | 52 |
| topic_independent facet 中 venue 出现最频繁(27)；contribution_type 仅 6/52 | §4.4.4, Fig.12, Table B.24 | 52 |
| 多数 study 用 emerging classification (open-coding-like) 而非 existing scheme | §4.4.4, Fig.13, Table B.25 | 52 |
| Visualization: bubble(23) ≈ bar(22) > pie(12) >> Venn(3) > line(2) > heatmap(1) | Table B.26 | 52 |
| 45/52 (87%) study 报告 validity threats | Table B.27, Fig.15 | 52 |
| Rubric quality ratio 中位数 = 33%；25% 的 study ≥ 40% | §5.4, Fig.20, Table 14 | 52 |
| Journals 的 rubric ratio 中位数 > Conferences | Fig.21, §5.5 | 52 |
| SE 主题覆盖：testing 最多；configuration mgmt 与 education 弱 | Table B.15, §4.2 | 52 |

### 6.2 原文 discussion / recommendation / roadmap 中提出的候选 finding

| 候选 finding | 类型 | 强度 |
|---|---|---|
| 单一 guideline 不足以指导完整 SMS → 需要 update | recommendation | 强（由 R01 频次支持） |
| 应使用 venue, research_type, research_method 三个 facet 作为 topic-independent classification 默认 | recommendation | 中（基于 facet 频次） |
| 应避免对 SMS 设过严的 inclusion criteria (e.g., 要求 evaluation) | guideline | 中（理论论证） |
| Decision rules 在 inc/excl 中虽未被广泛采用，但实证有效 (Ali&Petersen 引文) | candidate_heuristic | 中（外部引文支持） |
| Snowball 单用 + good start set 可能达到 db search 完整度 (Wohlin 2014 引文) | candidate_heuristic | 中（外部引文） |
| SMS 不应追求"找到所有"，应追求"good sample" | methodological_seed | 强（多次重复，Wohlin 2013 引文+本文重申） |

### 6.3 对 Paper2 可迁移的方法学启发

1. **数据抽取表绑定 RQ**（Table 3 列 `RQ`）——Paper2 的 LLM-agent extraction form 也应让每个字段标注 owner RQ，便于回溯。
2. **真值决策表分类**（Table 7）——比简单 free-form prompt 更可靠；适合 LLM agent + post-hoc rule check 二级验证。
3. **schema 内在关系约束**（R06: research_method↔research_type）——可作为 Paper2 自动一致性 guard。
4. **多 guideline 比较矩阵**（Table 5）——审计同一 task 上不同 guideline 的覆盖差异，是 schema_seed 反向产生新维度的方法学样板。
5. **Quality rubric ordinal scale**（Tables 9–13）——给出 0/1/2/3 的精确分级描述（"None / Min / Partial / Full"），可迁移作 LLM-judge ordinal rubric 模板。
6. **报告结构标准化**（§5.3）——Paper2 在 SUMMARY.md / desc.md 中应固定 sub-sections，便于跨论文比较。

### 6.4 绝不能迁移的领域结论

1. SWEBOK 11 类不是普适分类法，仅适用 2012 前 SE。
2. "guideline X 比 guideline Y 更好"这种结论本文未做，Paper2 也不应外推。
3. rubric ratio 33% 是 2012 前 SE SMS 的实证基线，**不能**外推为"现代 LLM-assisted SLR 应达到 ≥33%"或类似规范性指标。
4. validity taxonomy 5 类未涵盖 LLM/provider drift、prompt drift、schema revision bias 等现代风险。

## 7. 对现有 `review.md` 的返修建议（C / I / M 分级）

### C（critical，影响维度树准确性 / 学术证据链）

| # | 问题 | 建议 |
|---|---|---|
| C1 | A1-DT v2 "维度树结构"（review.md line 203–216）仍以单棵树呈现，把 5 个主干强制压成 b1..b5（planning/conducting/reporting/quality rubric/topic-indep dim），实际原文是**4 棵独立树的森林**（extraction form / classification facet / process+rubric / validity），合并破坏 schema 语义。 | 改写为 §3 所示**维度森林**结构，每棵树独立列叶子；标注它们的服务对象不同（编码自己 52 篇 vs. 向后续 study 推荐）。 |
| C2 | 叶子维度表（review.md line 218–227）的六个 `leaf-*` 仍是通用六叶（scope/corpus/taxonomy/method/evidence/finding），未升级 Table 3 的 12 个 extraction items、Fig.12 的 5 个 facets、Tables 9–13 的 4+1 ordinal rubric 为真正的叶子。 | 用本审计 §4 的 14 个叶子（L01..L14）替换通用六叶；明确每个叶子的取值空间类型（封闭枚举 / 真值表 / ordinal / multi-select）。 |
| C3 | A.2 证据账本（EV-001..004）证据强度全部 `not_verified`。但 Table 3、Table 7、Tables 9–13、Tables B.15–B.27 都是**已在 paper_content.txt 中直接可见的封闭枚举与频次表**，证据强度应升级为 `local_text_verified`（仅 Fig.1 数字链、Fig.16 partition 图等需 PDF 视觉核验保留 `not_verified`）。 | 把 EV 拆为 ≥6 条，分别绑到 Table 3 / Table 5 / Table 7 / Tables 8–13 / Tables B.15–B.27 / §3.6 validity；其中 Table B.15–B.27 + Table 3 + Table 7 升级为 `verified` 或 `local_text_verified`。 |
| C4 | "原文 schema 主树（19×3 审计后返修）"（review.md line 249–258）的叶子仍是抽象短语（"field list、map metadata"），未列具体字段名。 | 在该表 "叶子 / 取值空间种子" 列直接写出具体字段名与取值空间，如 `T1.extraction_form: {study_id:int, year:[2007..2012], guidelines: multi∈{10 closed labels}, search_type:{manual|auto|both}, ...}`。 |

### I（important，影响统计池资格与候选 finding 形成）

| # | 问题 | 建议 |
|---|---|---|
| I1 | "快速结论卡片"标注"是否目标证据池: 否"——正确；但"是否统计池: 是，但仅限 A1 `survey_of_surveys/` 的方法学统计池"应进一步明确**分母=52**，且所有 Appendix B 表是 ready-to-statistics 的关系边。 | 在卡片中加一行 "分母 / 样本单位: 52 included SE mapping studies (per §3.6.2; Appendix A); per-facet 频次表已 ready (Tables B.15–B.27)"。 |
| I2 | SUMMARY.md（推测）中如果当前对本论文标注"原生树类型: 单树"或"统计池资格: 否"，与原文事实不符。 | 改为"原生树类型: 维度森林（4 棵）"+"统计池资格: 是（方法学池），分母=52"。 |
| I3 | 缺少关系边表。原文 R06 (method↔type)、R08 (guideline×activity)、R09 (Table 6)、R10 (Table 7) 是核心 schema 关系，未被记录。 | 新增 §A.x "关系边表"，按本审计 §5 列出 R01–R10。 |
| I4 | 候选 finding 与 statistical observation 未分层。现 `clm-...-finding-boundary` 笼统说"final research finding 必须经过跨论文证据"——正确但太抽象。 | 在 review.md 新增 §"统计观察 vs. 候选 finding" 小节，按本审计 §6.1/§6.2 区分（10 条强统计观察 + 6 条 candidate finding）。 |

### M（minor，工程改进）

| # | 问题 | 建议 |
|---|---|---|
| M1 | "历史草稿（已迁移）"块（line 103–157）保留了一棵旧 ASCII 树，已 deprecated 但仍占大量篇幅。 | 折叠或移到独立 `history.md`；review.md 主体保持单一事实源。 |
| M2 | "六类 pattern 抽取"表（line 81–89）的"证据锚点"列仍写 `§3.1` 等粗粒度章节号，未到表号 / 图号。 | 加入具体 Table B.x / Table 7 / Fig.12 等精锚点。 |
| M3 | 时间字段（如待复核区）使用相对表述（"留待 A2a"），未给出 yyyy-mm-dd hh:mm:ss 时间戳。 | 在更新日志中加 `2026-06-30 hh:mm:ss` 完成时间戳。 |
| M4 | "A1-M0--M6 元维度贡献"表（line 93–101）仍是跨论文投影解释，应明确标注"非原文 schema"。 | 在该表上方加 callout: "本表是 Paper2 跨论文投影提示，不是本文原生维度树"。 |

## 8. 审计附录草案：A.2 / A.3（可直接迁移到 review.md）

### A.2 维度树证据账本草案（扩展为 8 条；强证据升级为 verified）

| 证据 ID | 引用键 | 来源文件 | 原文章节 | 表/图编号 | 释义 | 证据角色 | 证据强度 | 支撑维度节点 | 需 PDF 视觉核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|
| EV-pet15-001 | ev-rq | paper_content.txt | §3.1 (line 217–229) | -- | 明确 RQ1–RQ4 全文表述 | rq | verified | FOREST-ROOT, T1.process | 否 | 仅本文 |
| EV-pet15-002 | ev-extraction-form | paper_content.txt | §3.4, Table 3 | Table 3 | 12 字段 extraction form + RQ owner 绑定 | schema | verified | T1 整棵树, L01–L05, L12 | 否 (文本完整) | -- |
| EV-pet15-003 | ev-classification-facets | paper_content.txt | §4.4.4, Fig.12–13 | Fig.12, B.24, B.25 | 5 个 topic-indep facet + 2 个 topic-spec 子项 | schema + counts | verified | T2 整棵树, L09 | 否 | -- |
| EV-pet15-004 | ev-research-type-truth-table | paper_content.txt | §5.1.3, Table 7 | Table 7 | research type 6 类 + R1..R6 真值表 | schema + decision-table | verified | T2.research_type, L10, R10 | 否 | 6 类闭包仅适于此 facet |
| EV-pet15-005 | ev-process-actions | paper_content.txt | §5, Table 5, Table 8 | Table 5, Table 8 | 9 guidelines × 30+ activities 比较矩阵；26 actions rubric | schema + relation | verified | T3 整棵树, R08 | 推荐 PDF 核对 ✓/✗ 符号 | -- |
| EV-pet15-006 | ev-rubric-ordinal | paper_content.txt | §5.4, Tables 9–13, Table 14 | Tables 9–13, 14 | 4+1 ordinal rubric + 52 篇分布 | rubric + statistic | local_text_verified | T3 评分层, L14 | 是（Table 14 数值需复核）| ordinal scale 仅适合 SMS |
| EV-pet15-007 | ev-appendix-B-relations | paper_content.txt | Appendix B | B.15–B.27 | 逐研究 study→category 关系边，分母=52 | relation + counts | local_text_verified | R01–R05, R07, L01–L13 | 是（频次需复核）| 现代 SE SMS 已不同 |
| EV-pet15-008 | ev-validity-taxonomy | paper_content.txt | §3.6, §5.1.5 | -- | 5 类 validity + repeatability + mitigations | taxonomy | verified | T4 整棵树, L13 | 否 | 未含现代 LLM 风险 |
| EV-pet15-009 | ev-fig1-flow | paper_content.txt | §3.3, Fig.1 | Fig.1 | 选择流程链 7752→...→52 | statistic | not_verified | FOREST-ROOT 分母 | **是**（文本提取乱序）| -- |

### A.3 结论-证据映射草案

| ID | 结论 | 类型 | 支撑对象 | 支撑证据 | 反证/限制 | 强度 | 允许用途 |
|---|---|---|---|---|---|---|---|
| C01 | 本文是 **维度森林**（4 棵独立树），不是单一维度树。 | tree_type | FOREST-ROOT | EV-001, EV-002, EV-003, EV-005, EV-008 | 4 棵树是审计判断；作者未显式声明"forest"。 | strong | A1-DT v2 主结构定锚 |
| C02 | 样本单位 = SE systematic mapping study；分母=52；统计池资格 = 方法学池 yes。 | sample_unit | T1, R01–R05 | EV-007, EV-009 | -- | strong | SUMMARY 总表更新 |
| C03 | Table 3 extraction form 的 12 字段可直接迁移作 Paper2 LLM-agent extraction schema 模板。 | migration_seed | T1, L01–L05, L12 | EV-002 | 字段须重命名以适应现代 SE/LLM 主题；SWEBOK 需替换。 | strong | Paper2 §method 设计 |
| C04 | Table 7 research-type 真值表是 A1-DT v2 罕见的"完整 boolean schema 证据"，可作为 Paper2 LLM-judge 后验规则 layer。 | migration_seed | L10, R10 | EV-004 | 仅适于 research_type 单 facet；其他 facet 需自行设计真值表。 | strong | Paper2 §method 设计 |
| C05 | 4+1 ordinal rubric (Tables 9–13) 提供了 quality 评分的"0/1/2/3 分级描述"模板。 | migration_seed | L14, T3 评分层 | EV-006 | rubric 仅适合 SMS；SLR / experimental study 不可直接套。 | medium | Paper2 §evaluation 设计 |
| C06 | guideline×activity 比较矩阵 (Table 5) 提供"用多 guideline 反向揭示 schema 覆盖 gap"的方法学样板。 | migration_seed | R08 | EV-005 | matrix 对手工对齐成本高；需 LLM 辅助。 | medium | Paper2 §discussion / future work |
| C07 | 不可迁移：SWEBOK 11 类、validity 5 类、guideline 10 类的具体内容均带有 2012 前 SE 时代痕迹，仅迁移"封闭枚举 + 频次统计"的方法学 form，不迁移 enum 内容。 | migration_boundary | L01, L02, L13 | EV-002, EV-003, EV-008 | -- | strong | review.md §"可迁移边界" |
| C08 | 单人筛选（second author 独立 inclusion）是本文自报最大 validity 威胁；提示 Paper2 须设计双人/人+agent 多重审查协议。 | candidate_heuristic | T4.theoretical_validity | EV-008 + §3.6.2 | -- | strong | Paper2 §threats |
| C09 | rubric ratio 中位数 33% 是 2012 前 SE SMS 实证基线，**不得**外推为"现代 LLM-SLR 应达到 ≥33%"的规范性目标。 | migration_boundary | L14 | EV-006 | -- | strong | review.md §"不可迁移边界" |
| C10 | （废弃旧结论）"原生树类型 = 降级树 / schema seed only"——本结论由 A1-DT v1 给出，与本审计冲突，应废弃。 | audit_repair | -- | EV-002, EV-003, EV-004, EV-005, EV-007 | -- | strong | review.md §"审计返修口径"中标注 deprecated |

## 9. 技能使用与自我审查记录

### 9.1 技能文件读取与采用原则

| 技能文件 | 实际读取范围 | 采用原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | line 1–100（核心 mandate / operating modes / loading strategy / non-negotiable gates） | "Evidence gate"（repository files 优于 memory）；"Claim gate"（每条声明须有证据，否则降级）；"Citation asset gate"（仅引用本地可核验的章节 / 表 / 图编号）。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 全文（112 lines） | 用 Universal Review Dimensions 5 维（Originality, Quality, Clarity, Significance, Reproducibility）评估现有 review.md 的可信度；用 "constructive specificity" 标准产出 C/I/M 建议时给出 file:line 锚点。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 全文（223 lines） | 用 "Claim Audit" 模板检查 review.md 中"维度树主类型"等结论的证据强度；用 "Adversarial Questions" 检查是否把投影误读为原文（特别是 "Could a reviewer say... has been done before?"）。 |
| `research-planning/SKILL.md` | 全文（77 lines） | 按 "Flag ambiguities explicitly rather than making assumptions" 原则——本审计明确把 Fig.1 数字链等 PDF 视觉项标为 `not_verified`，不脑补分母。 |
| `research-planning/references/planning-prompts.md` | line 1–80 | Paper2Code 4-turn 思路用于组织 §3 维度森林的层级展开（先 overall, 再 architecture, 再 logic, 再 leaf-level）。 |
| `research-planning/references/output-schemas.md` | line 1–80 | 采用 JSON-schema-like 思路把每个 leaf 显式标注 `取值空间类型`。 |
| `oh-my-codex/autoresearch/SKILL.md` | 全文（70 lines） | 借用 "completion artifact contract" 思路——本审计的最终交付物 = self-contained Markdown 报告，符合 artifact-gated 完成标准。 |

### 9.2 reviewer 视角下本审计最高风险 3 点

1. **Fig.1 数字链 (7752→5082→60→43→54→44→52+8+11) 未做 PDF 视觉核验**。文本提取顺序混乱，分母 52 来自 §3.6.2 与 §4.4.3 多处文本复现 (`14 out of 52`)，结论稳健；但 +8 与 +11 的回补来源需 PDF 复查才能 100% 锁定。主线程合并时应保留 `EV-pet15-009 = not_verified` 并列入 A2a。
2. **Tables 9–13 中 "bold 高亮分数" 在 paper_content.txt 中丢失**。Table 14 给出本文自身 rubric 的频次分布，但"本研究自评 33% ratio"的具体细分须 PDF 复核 Tables 9–13 中 bold 标注的位置（§5.4 line 1372: "scores identified in this mapping study are highlighted as bold text"）。主线程引用 L14 时应保留 `local_text_verified` 而非 `verified`。
3. **"维度森林 vs 单树" 是审计判断而非作者声明**。作者未在原文说"this is a forest"；本审计基于 Table 3 (extraction form) 与 Table 8 (rubric) 服务对象不同（编码自身 52 篇 vs 向后续研究推荐）的语义观察。若 reviewer 反对，可降级为"多 schema 共存的单论文"，但其取值空间区分必须保留。

### 9.3 blocked / timeout / 文件缺失

- 无 blocked / timeout。
- 所有 7 个技能 / 指南文件可读，所有 5 个论文材料（bibtex.bib / metadata.json / paper.pdf 文件存在 / paper_content.txt / review.md）可读。
- 未打开 `paper.pdf` 二进制（按硬约束 6: 若需图表视觉核验仅说明状态，不强制读 PDF）；本轮以 paper_content.txt 全文 + Tables B.15–B.27 文本为主，已覆盖 ≥85% 的 schema 证据。

---

**审计完成时间**: 2026-06-30
**agent**: claude (claude-opus-4-7[1m])
**输出文件**: 本回答正文，未修改仓库任何文件，未 commit / push / gh comment。
