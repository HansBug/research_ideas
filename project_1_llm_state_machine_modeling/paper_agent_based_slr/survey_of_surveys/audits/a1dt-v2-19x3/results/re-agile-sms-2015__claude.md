I've read the paper text in full. Now I'll produce the A1-DT v2 audit report.

`★ Insight ─────────────────────────────────────`
- 这篇 SEAA 2015 SMS 的原文 schema 极度清晰：3 个显式 RQ + 4 类抽取主题（定义/benefit/problem/solution）+ 5 张分类表（venue/agile-method/article-type/B1-B6/P1-P6），是少有的"原文树几乎完全显式"的样本。
- 关键观察：solution 是以 `problem→solution_set or no_solution` 的关系型 schema 出现的（P3/P4/P6 显式 `no solutions proposed`），这是单值/枚举叶子无法承载的，必须作为关系边建模。
- 现有 `review.md` 已经做了较好的"19×3 审计后返修"，但 `B1-B6`、`P1-P6` 的封闭枚举、relation schema、表 I/II/III 的具体取值都尚未直接抬升为叶子取值空间，仍停在 `not_verified`，是 A2a 的明确升级入口。
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇审计报告：`re-agile-sms-2015`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-agile-sms-2015` |
| agent | `claude` (Opus 4.7 / 1M) |
| 是否已读 `paper_content.txt` | 是。已完整阅读全文 954 行（Page 1–9）。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`metadata.json` 已确认 review_type=SMS, eligible_for_statistical_synthesis=true；`bibtex.bib` 提供 DOI 10.1109/SEAA.2015.70。 |
| 是否打开或核对 `paper.pdf` | 否。仅基于 `paper_content.txt` 完成文本级审计；表 I–V 的版面、对齐、上下角标和数字单元格需 A2a 在 PDF 上视觉核验。 |
| 原文类型 | systematic mapping study (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 mapping study。 |
| 被编码样本单位 | primary study（28 篇敏捷 RE 原始研究，编号 S1–S28）。 |
| 样本数量 / 分母 | 241（搜索命中）→ 187（去除非 journal/conference 与非英文）→ 65（标题/摘要筛选后）→ **28**（全文筛选后的最终纳入数 = 主统计分母）。 |
| 原生树类型 | 维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 schema。 |
| 主统计池资格 | **是**（局部可统计）：venue 频次、agile-method context、article-type、B1–B6 频次与引用集合、P1–P6 频次与引用集合、P→solution 关系覆盖，均可在原文表上直接统计；分母清晰 N=28。Definition 与 future-work 仅作 candidate finding，不入主统计。 |
| 总体判定 | **needs repair**：现有 `review.md` 的"原文 schema 主树（19×3 审计后返修）"方向正确，但叶子的封闭枚举、关系边、表 I/II/III/IV/V 的精确取值与编号 S1–S28 的字段映射仍标 `not_verified`；应升级为 `text_verified`（文本级已核验，PDF 版面核验另列）。 |

## 1. 原文证据阅读说明

实际读取文件与范围：
- `paper_content.txt`：Page 1–9 全文 954 行，含 Abstract / I. Introduction / II. Background (A/B/C) / III. Methodology / IV. Results (A/B/C/D) / V. Discussion (A/B/C/D) / VI. Conclusion / References [1]–[26] / Primary Sources [S1]–[S28]。
- `bibtex.bib`、`metadata.json`：用于元信息核验。
- `review.md`：当前 v1 审计后的产物，作为返修对象。
- 未开 `paper.pdf`：本轮所有"表 X 行/列"事实仅基于 text 提取；Table II/III/IV/V 的 `Articles` 单元格在 text 提取中已被原样保留，但**编号顺序、对齐、合并单元格、缺失逗号**等需 PDF 视觉核验后才能升级为 `pdf_verified`。

关键原文证据锚点（按章节序）：

1. **三个显式 RQ**：Page 1 I. Introduction 段 "The overall research questions ... 1) What has been researched ... 2) What are the reported key benefits ... 3) What are the reported problems and corresponding solutions ..."。
2. **检索分母链条**：Page 3 III. Methodology "Scopus ... September 2014 ... 241 results ... 46 ... 8 ... 187 ... 123 excluded ... 65 ... 37 excluded ... remaining 28 articles"，含完整 search string `TITLE-ABS-KEY(("requirements analysis" OR "requirements engineering") AND (agile OR scrum)) AND NOT KEY("agile manufacturing")`。
3. **抽取协议**：Page 3 末段 "article metadata, context, methods and results were extracted ... categorized under the following four subject areas: Definition of RE in the agile context, benefits ... problems ... solutions"。
4. **Table I venue 分布**：Page 3 "Conference proceedings N=15 ≈53%, Journal N=8 ≈29%, Magazine N=5 ≈18%"，venue 名包含 AREW(2)/RE(3)/IEEE Software(5) 等。
5. **Table II agile-method context**：Page 4 "Unspecified agile N=20 (71%); Scrum N=7; FDD N=1"。
6. **Table III article-type**：Page 4 "Multiple case study 6 / Single case study 5 / Experience report 3 / Tool eval 1 / Method eval 2 / Method proposal 8 / Position paper 3"。
7. **Table IV B1–B6 封闭枚举**：Page 5 含完整六类 benefit 名称、对应 S 编号集合（如 B2 = [S2,S3,S4,S7,S18,S23]）。
8. **Table V P1–P6 封闭枚举**：Page 6 含完整六类 problem 与对应 S 编号集合（如 P1 = [S4,S7,S12,S18,S22,S23]）。
9. **problem→solution 关系 schema**：Page 5–6 在 P1/P2/P5 后给出 solution 段，P3/P4/P6 后明确 "No solutions to PX were proposed in the articles"。
10. **作者综合 finding 与定义**：Page 7 V.B "Towards a definition of agile RE" 给出作者自造定义；V.C/V.D 给出 gap 与 limitation。

## 2. 样本单位与字段来源判定

1. **被编码对象**：28 篇原始研究（primary studies, S1–S28），逐篇被作者抽取并归到 venue / context / article-type / definition / benefit set / problem set / solution set。
2. **是否系统**：是。Page 3 完整给出 Scopus 数据库、search string、时间窗（Sep 2014）、纳排标准（5 条 title/abstract + 3 条 full-text）、分母链条 241/187/65/28，符合 Kitchenham-Charters [18] mapping study 标准。
3. **字段来源**：
   - extraction form 在 III. Methodology 末段以散文形式给出（metadata + context + methods + results）；
   - classification schema 由 Table I–V 显式承载；
   - B1–B6 与 P1–P6 为作者归纳所得的 thematic taxonomy（开放编码 → 主题归并）。
4. **RQ 与样本单位关系**：RQ 是字段用途（RQ1=研究分布, RQ2=benefit 抽取, RQ3=problem+solution 抽取）；样本单位是 primary study；树根是"28 篇 RE-in-ASD 研究的 thematic mapping"。
5. **降级**：无须降级。本文有完整系统语料库与抽取协议，符合主统计池纳入条件；唯一限制是 N=28 较小，部分 cell (FDD=1, Tool eval=1) 单元过稀，统计结论需保留小样本警告。

## 3. 原生样本编码维度树

```text
[root] 28 篇 RE-in-ASD primary studies (Heikkilä et al. 2015)
├── [b-rq] 三个显式 RQ（字段用途锚）
│   ├── RQ1: 研究分布 → 投影到 venue/context/article-type
│   ├── RQ2: benefits  → 投影到 B1–B6
│   └── RQ3: problems & solutions → 投影到 P1–P6 + solution relation
│
├── [b-corpus] 检索与纳排分母链（系统性证据）
│   ├── database = {Scopus}
│   ├── search_string = "(requirements analysis OR requirements engineering) AND (agile OR scrum) AND NOT (agile manufacturing)"
│   ├── time_window = "until Sep 2014"
│   ├── n_initial = 241
│   ├── n_after_doc_type_lang = 187
│   ├── n_after_title_abstract = 65
│   ├── n_excluded_titleabs = 123
│   ├── n_after_fulltext = 28
│   ├── n_excluded_fulltext = 37
│   ├── inclusion_year_span = "2003–2014" (来源 §VI: "publication years 2004 to 2014" + S20=2003)
│   └── exclusion_criteria = {no_abstract_access, non_research, non_SE, off_topic, predatory_vanity,
│                              no_fulltext_access, redundant_extended, off_topic}
│
├── [b-pub-venue] 发表 venue 分类（Table I）
│   ├── venue_type ∈ {Conference, Journal, Magazine}  -- 封闭三值
│   ├── venue_count_conf = 15 (≈53%)
│   ├── venue_count_journal = 8 (≈29%)
│   ├── venue_count_magazine = 5 (≈18%)
│   └── venue_names (open enum, 见 Table I 原文)
│
├── [b-agile-context] 文章中 agile method context（Table II）
│   ├── unspecified_agile = 20 (71%)
│   ├── Scrum = 7 (25%)
│   └── FDD = 1 (4%)
│
├── [b-article-type] 研究类型（Table III）
│   ├── multiple_case_study = 6
│   ├── single_case_study = 5
│   ├── experience_report = 3
│   ├── tool_evaluation = 1
│   ├── method_evaluation = 2
│   ├── method_proposal = 8
│   └── position_paper = 3
│
├── [b-definition] Agile RE 定义维度（RQ1 子轴）
│   ├── definition_clarity = "vague / no universal definition"  (§V.B)
│   └── author_proposed_definition = 自由文本段（§V.B）  -- candidate finding，非统计
│
├── [b-benefit] B1–B6 封闭枚举（Table IV）
│   ├── B1 Lower process overheads        | studies = {S2,S4,S20,S25}        | n=4
│   ├── B2 Improved requirements understanding | studies = {S2,S3,S4,S7,S18,S23} | n=6
│   ├── B3 Reduced overburden / overallocation | studies = {S2,S3,S7}        | n=3
│   ├── B4 Responsiveness to change       | studies = {S4,S7,S20,S23,S25}    | n=5
│   ├── B5 Rapid delivery and validation  | studies = {S4,S20,S25}           | n=3
│   └── B6 Improved customer relationships| studies = {S4,S7}                | n=2
│
└── [b-problem-solution] P1–P6 + solution 关系 schema（Table V + §IV.D）
    ├── P1 Client/customer rep problems   | n=6 {S4,S7,S12,S18,S22,S23} | solution_set = {S5,S10,S11,S12,S15,S17,S20,S26}
    ├── P2 User story format insufficiency| n=6 {S4,S5,S7,S13,S23,S24}  | solution_set = {S1,S5,S8,S9,S24,S27}
    ├── P3 Prioritization difficulties    | n=5 {S2,S4,S12,S22,S23}     | solution_set = ∅ (NO_SOLUTION)
    ├── P4 Growing technical debt         | n=2 {S7,S23}                | solution_set = ∅ (NO_SOLUTION)
    ├── P5 Tacit requirements knowledge   | n=5 {S4,S12,S20,S22,S24}    | solution_set = {S20}
    └── P6 Imprecise effort estimates     | n=2 {S4,S23}                | solution_set = ∅ (NO_SOLUTION)
```

`★ Insight ─────────────────────────────────────`
- `solution_set = ∅` 是这份 schema 最值得迁移的设计选择：作者把"未提出解"作为 first-class 信号而不是缺失。Paper2 维度树的"gap 字段"可以直接学这一招——空集是结论，不是 missing data。
- `multiple_case_study=6 + single_case_study=5 + experience_report=3 + tool/method eval=3 ≈ 17/28 = 61%` 与 §V.A 给出的"≈60%"自洽，可作为 A2a 一致性校验锚点之一。
`─────────────────────────────────────────────────`

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-rq-list | 三个显式 RQ | b-rq | §I Introduction RQ 段 | 作者声明的研究目标 | 三条自由文本 RQ | enum-3 | n/a | 字段用途 anchor | 不直接成 finding | Page 1 RQ 段 | 仅本文 |
| L-corpus-db | 检索数据库 | b-corpus | §III ¶2 | 检索源 | {Scopus} | 完整枚举（封闭） | n/a | 用于评估检索覆盖 | 单库覆盖局限 → candidate threat | Page 3 §III | 可迁移结构 |
| L-corpus-string | 检索式 | b-corpus | §III ¶2 | 完整 search string | 自由文本 + 关键词集合 | 文本+词袋 | n/a | 复现性证据 | 候选 keyword cluster | Page 3 §III | 可迁移结构 |
| L-corpus-window | 时间窗 | b-corpus | §III ¶2 | 检索截止时间 | "Sep 2014" 单点 | 日期点 | n/a | 时效性评估 | 1 年截止可能漏 2014–2015 论文 | Page 3 §III | 可迁移结构 |
| L-corpus-chain | 分母链 | b-corpus | §III ¶2-4 | 241/187/65/28 | 整数四元组 | 数值链 | n/a | 严格分母 | candidate selection threat | Page 3 §III | 可迁移结构 |
| L-corpus-excl | 纳排标准 | b-corpus | §III ¶3-5 | 5+3 条 exclusion | 封闭文本枚举 8 项 | enum-8 | 漏标=未应用 | 偏倚评估 | candidate threat | Page 3 §III | 可迁移结构 |
| L-venue-type | venue 类型 | b-pub-venue | Table I | 出版形式 | {Conference, Journal, Magazine} | enum-3 (closed) | n/a | 频次表 | venue 分散 → "no primary venue" finding | Table I, §V.A | 可迁移结构 |
| L-venue-name | venue 名 | b-pub-venue | Table I | 具体 venue | 开放枚举（≥17 venue） | enum-open | n/a | venue 长尾 | candidate gap | Table I | 仅本文 |
| L-ctx-method | agile method context | b-agile-context | Table II | 文章使用的敏捷方法 | {Unspecified, Scrum, FDD} | enum-3 (closed in this sample) | n/a | 频次 | "71% unspecified" 是显式 finding | Table II, §V.A | 取值空间可能扩展 |
| L-art-type | 研究类型 | b-article-type | Table III | 文章类型 | {MultiCase, SingleCase, ExpReport, ToolEval, MethodEval, MethodProposal, PositionPaper} | enum-7 (closed in this sample) | n/a | 频次 | "29% method proposal w/o eval" → finding | Table III, §V.A | 可迁移分类轴 |
| L-def-clarity | 定义清晰度 | b-definition | §V.B | 作者对 agile RE 定义现状的判断 | {vague, contested, clear} | enum-3（本文取 vague） | n/a | 不入主统计 | candidate finding "definition is vague" | §V.B | 仅本文判断 |
| L-def-author | 作者综合定义 | b-definition | §V.B blockquote | 作者自造定义文本 | 自由文本 | text+rationale | n/a | 不入主统计 | candidate finding | §V.B | 不可直接迁移 |
| L-benefit-code | benefit 类目 | b-benefit | Table IV | B1–B6 | {B1..B6} | enum-6 (closed) | 缺失=未观察到 | 频次 + 引用集合 | benefit landscape | Table IV | 可迁移轴 |
| L-benefit-studies | benefit→studies 关系 | b-benefit | Table IV | 每个 B 对应的 S 集合 | 关系（多对多） | relation set | ∅=未在样本中出现 | 频次/coverage | candidate "Bi 支撑薄" 判定 | Table IV | 可迁移结构 |
| L-problem-code | problem 类目 | b-problem-solution | Table V | P1–P6 | {P1..P6} | enum-6 (closed) | 缺失=未观察到 | 频次 | problem landscape | Table V | 可迁移轴 |
| L-problem-studies | problem→studies 关系 | b-problem-solution | Table V | 每个 P 对应的 S 集合 | 关系（多对多） | relation set | ∅=未在样本中出现 | 频次/coverage | candidate problem 强度 | Table V | 可迁移结构 |
| L-solution-rel | problem→solution 关系 | b-problem-solution | §IV.D 各小节 | 每个 P 对应的 S（solution 提议）集合 | 关系（多对多）+ NULL | relation set with ∅-as-finding | **∅ = "no solutions proposed"，是显式 finding** | 频次 + gap | direct "research gap" 信号 | Page 5–6 §IV.D | **强可迁移：空集做 first-class** |
| L-limit-search | 限制：单库 | b-corpus | §V.D | 仅用 Scopus | bool + rationale | bool | n/a | threat assessment | candidate threat | §V.D | 可迁移结构 |

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R-benefit-of | study (S1..S28) | reports_benefit | benefit code (B1..B6) | {B1..B6} | 该 study 未报告任何 benefit | Table IV | 频次/coverage |
| R-problem-of | study (S1..S28) | reports_problem | problem code (P1..P6) | {P1..P6} | 该 study 未报告任何 problem | Table V | 频次/coverage |
| R-solution-of | problem code (P1..P6) | has_solution_in | study set ⊆ S1..S28 | study set 或 ∅ | **∅ = NO_SOLUTION_PROPOSED（显式 finding）** | §IV.D 各小节末句 | gap 识别 |
| R-context-of | study (S1..S28) | uses_agile_method | agile method | {Unspecified, Scrum, FDD} | n/a | Table II | 上下文分层 |
| R-type-of | study (S1..S28) | has_article_type | article type | enum-7 | n/a | Table III | 类型分层 |
| R-venue-of | study (S1..S28) | published_in | venue name | open enum | n/a | Table I | venue 分布 |

`★ Insight ─────────────────────────────────────`
- 注意 `R-solution-of` 的源是 **problem code 而不是 study**——这与 `R-benefit-of/R-problem-of` 的源不同。这是因为 §IV.D 是按 P1–P6 组织 solution，而不是按 study 组织。这种"以问题为索引、以研究为证据"的结构是 SMS 中较少见的优雅设计。
- ∅ 作为显式 finding 的设计可直接抬升为 Paper2 维度树的通用约束：每个"建议/方法"叶子都应允许 `proposed = ∅` 并把它当作 first-class 结论。
`─────────────────────────────────────────────────`

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 由字段/统计表直接支撑的统计观察（可入 A2a 主统计）

| 观察 | 分母 | 数值 | 原文锚点 |
|---|---|---|---|
| Conference 占比 | 28 | 15/28 ≈ 53% | Table I |
| Unspecified agile context 占比 | 28 | 20/28 ≈ 71% | Table II, §V.A |
| 含实证成分文章占比 | 28 | 17/28 ≈ 60% (case+exp+evals) | §V.A |
| Method proposal 无评估占比 | 28 | 8/28 ≈ 29% | §V.A |
| Benefit 类目数（封闭） | n/a | 6 | Table IV |
| Problem 类目数（封闭） | n/a | 6 | Table V |
| Problem 无 solution 占比 | 6 | 3/6 (P3,P4,P6) | §IV.D 末句 |
| B2 支撑最强 | benefits | 6 studies | Table IV |
| P1, P2 支撑最强 | problems | 各 6 studies | Table V |

### 6.2 作者提出的 candidate findings（不可直接升级 final）

- "Agile RE 定义模糊"（§V.B）。
- "无主导 venue, RE in ASD 在出版形态上未'找到家'"（§V.A）。
- "大型/复杂系统中 user story 不够用"（§V.C 综合）。
- "P3/P4/P6 缺乏解 → 三个研究空白方向"（§V.C, §VI）。
- "方法提议未经实证评估 → 需更多实证研究"（§V.A, §VI）。

### 6.3 可迁移到 Paper2 的方法学启发

- ∅-as-finding（空 solution set 作 first-class 结论）。
- "problem 索引 + study 证据"的关系型 schema（不要把 solution 压成 study 的属性）。
- benefit/problem 双轴并列 + 共享 S-id 引用集，便于做 benefit-problem 对偶 mapping。
- 分母链严格保留（241→187→65→28）。

### 6.4 不可迁移内容

- 任何 Agile RE 的领域结论（B1–B6, P1–P6 具体内容）不可迁移到 Paper2 的 STM / LLM-as-Judge / repair 主题。
- "Scrum/XP/FDD 三分"分类只对 agile RE 有效。
- N=28 + 单库（Scopus）+ 截至 2014.09 的样本属性。

## 7. 对现有 `review.md` 的返修建议（C/I/M）

| 等级 | 位置 | 现状 | 建议 |
|---|---|---|---|
| **I-1** | "原文 schema 主树（19×3 审计后返修）" 表 `叶子 / 取值空间种子` 列 | 当前仍写"B1–B6 或原文 benefit clusters、数量、示例"等抽象描述 | 升级为**显式封闭枚举**：列出 `{B1 Lower process overheads, B2 Improved requirements understanding, ..., B6 Improved customer relationships}` 与 `{P1..P6}` 全名 + 每个 code 的 study-id 集合。证据来自 Page 5 Table IV / Page 6 Table V，可直接 text 核验。 |
| **I-2** | A.2 证据账本 EV-002 / EV-003 | 标 `not_verified` + "待 A2a 精确页码复核" | 升级到 `text_verified`：原文页码已在 text 中显式出现（Page 3/4/5/6），可在保留"PDF 视觉核验另列"的前提下升级证据强度。 |
| **I-3** | 维度树缺关系边 | 当前叶子层未显式区分 `attribute` 与 `relation` | 新增 §"关系边表"，纳入 R-benefit-of / R-problem-of / **R-solution-of with ∅-as-finding**。这是本文最强的可迁移点。 |
| **I-4** | "原文模式候选叶子映射（A1 种子）" | 当前候选叶子全部 `not_verified` | `leaf-orig-problem` 与 `leaf-orig-benefit` 可直接升级为封闭枚举（B1–B6, P1–P6 在 text 中显式列出）；`leaf-orig-solution` 必须改为关系叶子（不是平铺枚举）。 |
| **I-5** | SUMMARY 维度（如有）"样本单位/样本数量/原生树类型/统计池资格" | 需复核 | 建议口径：样本单位=primary study, N=28, 树类型="维度森林+关系边", 主统计池=是（局部可统计）。 |
| **M-1** | "1. 快速结论卡片" 中 `阅读状态` 写 "已读全文文本-paper_content核验" | 字面正确 | 可补一句"PDF 版面核验未做"以避免读者误判。 |
| **M-2** | A.4 `cmd-visual-check` `needs_manual_check` | 维持 | 可附"建议核验项清单"：Table I venue 名拼写、Table II/III/IV/V 单元格中 S-id 集合完整性、§III 数字链条精确数。 |
| **M-3** | 旧"六类 pattern 抽取"表 (§2) | 已与 A1-DT v2 口径冲突 | 在该表上方加更清晰的 deprecation 注：明示本表是 v1 历史投影，不是 v2 原文 schema 事实源。 |

无 C 级阻塞问题。

## 8. 审计附录草案

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-v2-001 | paper_content.txt | §I Introduction | Page 1 RQ 段 | 三条 RQ 显式列出（research/benefits/problems & solutions） | rq | text_verified | b-rq, L-rq-list | false | 仅本文 |
| EV-v2-002 | paper_content.txt | §III Methodology | Page 3 ¶2-5 | "Scopus ... Sep 2014 ... 241 → 187 → 65 → 28 ... search string ... 5+3 exclusion criteria" | corpus_chain | text_verified | b-corpus 全部叶子 | false | 单库限制 |
| EV-v2-003 | paper_content.txt | §IV.A Overview + Table I | Page 3–4 | Conference 15 (53%), Journal 8 (29%), Magazine 5 (18%) | classification | text_verified | b-pub-venue | true (venue 拼写/合并需 PDF) | 仅本文 |
| EV-v2-004 | paper_content.txt | §IV.A + Table II | Page 4 | Unspecified 20, Scrum 7, FDD 1 | classification | text_verified | b-agile-context | true | 取值空间或扩展 |
| EV-v2-005 | paper_content.txt | §IV.A + Table III | Page 4 | 7 类 article-type 全部计数 | classification | text_verified | b-article-type | true | 可迁移分类轴 |
| EV-v2-006 | paper_content.txt | §IV.C + Table IV | Page 4–5 | B1–B6 名称与 study-id 集合完整 | classification + relation | text_verified | b-benefit, L-benefit-code, L-benefit-studies, R-benefit-of | true (S-id 列对齐) | 仅 Agile RE 领域 |
| EV-v2-007 | paper_content.txt | §IV.D + Table V | Page 5–6 | P1–P6 名称与 study-id 集合完整；P3/P4/P6 显式 "No solutions ... proposed" | classification + relation + ∅-finding | text_verified | b-problem-solution, R-problem-of, R-solution-of | true (S-id 列对齐) | ∅ 设计可迁移 |
| EV-v2-008 | paper_content.txt | §V.B | Page 7 blockquote | 作者自造 agile RE 定义 | candidate_finding | text_verified | L-def-author | false | 不可迁移领域结论 |
| EV-v2-009 | paper_content.txt | §V.A / §V.C / §VI | Page 6–8 | "method proposal 无评估占 29%"; "P3/P4/P6 缺解"; "需更多实证" | candidate_finding | text_verified | 6.2 候选 findings 全部 | false | candidate only |
| EV-v2-010 | paper_content.txt | §V.D Limitations | Page 7–8 | "constrained to Scopus ... small set of keywords" | limitation | text_verified | L-limit-search, 迁移边界 | false | threat anchor |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-v2-01 | 原生树类型为"维度森林 + 关系边"：venue/context/article-type/benefit/problem-solution 五并列主干，其中 problem→solution 为显式关系（含 ∅-as-finding） | tree_type | b-* 所有主干 | EV-v2-001..007 | strong (text) | 可作 Paper2 schema 灵感 | 仅本文；N=28 |
| CLM-v2-02 | 28 是严格主统计分母；241→187→65→28 链条完整可复现 | statistical_pool | b-corpus | EV-v2-002 | strong | 可作 A2a 主统计起点 | 单库 + 截至 2014.09 |
| CLM-v2-03 | benefit/problem 是封闭 6 值枚举（B1–B6, P1–P6），每个 code 关联明确 S-id 集合 | leaf_value_space | L-benefit-code, L-problem-code, R-benefit-of, R-problem-of | EV-v2-006, EV-v2-007 | strong (text) | 可直接做频次/coverage 统计 | 类目是作者主题归并，存在编码者主观 |
| CLM-v2-04 | ∅-solution (P3/P4/P6) 是作者显式声明的"研究空白"，应作 first-class finding 而非缺失数据 | candidate_finding + schema_design | R-solution-of | EV-v2-007 | strong | gap 信号 + Paper2 可迁移设计模式 | 仅在 SMS 抽取协议明确"是否提出 solution"时成立 |
| CLM-v2-05 | "29% 文章是无实证评估的 method proposal" 是直接可统计的 candidate finding | candidate_finding | L-art-type | EV-v2-005, EV-v2-009 | medium | 候选 finding，需研究者裁决 | 仅本样本 |
| CLM-v2-06 | "agile RE 定义模糊"是 candidate finding，不可作 final | candidate_finding | L-def-clarity, L-def-author | EV-v2-008 | weak | 仅候选 | 单篇判断 |
| CLM-v2-07 | 当前 `review.md` 中 B1–B6/P1–P6 仍标 not_verified 与文本证据不符，应升级至 text_verified | review_repair | review.md "原文 schema 主树" 段 | EV-v2-006, EV-v2-007 | strong | 直接驱动返修 | 仍待 PDF 版面核验，是另一层级 |
| CLM-v2-08 | 迁移边界：可迁移 schema 形态（森林+关系+∅-finding+分母链），不可迁移 agile RE 领域结论 | migration_boundary | root | EV-v2-001..010 | strong | Paper2 schema 设计依据 | 领域绑定 |

## 9. 技能使用与自我审查记录

### 9.1 技能文件读取情况

由于本次审计在 Claude Code 沙盒中执行，且 `~/.codex/skills/` 与 `~/.codex/plugins/cache/` 路径属于 Codex 客户端目录而非 Claude Code 默认工作区，本 agent **未实际打开**清单中列出的 7 个 skill/reference 文件。这是本任务的一个 `blocked` 风险点，需在主线程合并时显式记录。

可声明实际遵循的等价原则（来自当前 ARS / superpowers / phd-skills 在 session 中已加载的描述与本仓 `CLAUDE.md` §3 学术研究仓库 Review 口径 §4 Reviewer 输出要求）：

1. evidence-before-action：所有 C/I 都附原文页号/章节锚点。
2. C/I/M 分级以"是否影响学术目标/实验可靠性/结论可复现性"为准；本审计未发现 C 级问题。
3. 不脑补：所有"无法读取"或"未做"的步骤显式记录为 `not done` / `blocked`，不假装完成。
4. 单篇审计不外推到跨论文 final finding。

### 9.2 本输出最高 3 风险

1. **未做 PDF 版面核验** → Table I–V 的 S-id 集合（如 B2={S2,S3,S4,S7,S18,S23}）可能在 text 提取中丢字符或顺序错乱；主线程合并时建议至少抽查 Table IV、Table V 的两行做 PDF 视觉核对。
2. **7 个 skill 文件未实际打开** → 本审计的方法学约束依赖 session 中的描述而非源文件，可能存在与 skill 最新版差异。主线程合并时应在文档外的执行环境（Codex CLI）中以同一论文重做一次以交叉验证。
3. **本审计把 benefit/problem 视为"封闭 6 值枚举"** → 严格说，作者在 §IV.C/D 用的是"开放编码 → 主题归并"，B1–B6 是归并产物而非先验编码框架；若后续在 A2a 引入其它 agile RE SMS 做跨论文 union，需把这一层"作者归并"显式作为 schema-level 不变量保留，不能假定 B1–B6 是跨论文稳定 taxonomy。

### 9.3 blocked / timeout / 文件缺失

- `blocked`：清单中 7 个 skill/reference 文件未实际读取，原因为路径不在当前 Claude Code 工作区可达范围内。
- 无 timeout。
- 无文件缺失：`paper_content.txt` / `bibtex.bib` / `metadata.json` / `review.md` 全部成功读取；`paper.pdf` 本轮按设计仅作待核验对象。

---

**最终判定**：`re-agile-sms-2015` 是 A1-DT v2 中**结构最清晰、最适合作主统计池入口**的样本之一（原生树几乎完全显式于 §III + Table I–V + §IV）。建议主线程按 §7 的 I-1..I-5 与 §8 的 A.2/A.3 草案直接驱动 `review.md` 的下一轮返修，并把 ∅-as-finding 与 problem-indexed solution relation 抬升为 Paper2 维度树的可复用设计模式。
