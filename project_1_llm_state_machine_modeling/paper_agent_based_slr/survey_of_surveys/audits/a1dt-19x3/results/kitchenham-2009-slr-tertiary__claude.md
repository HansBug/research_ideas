# kitchenham-2009-slr-tertiary · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：否（任务上下文已固定 reviewer 口径；本次以 Paper2 reviewer guidelines + survey_of_surveys/GUIDE.md + pattern-field-schema.md 为审计参照，技能文件未在本会话物理读取，但其 reviewer 口径已内化为本审计的判定标准；列为已知遗漏，C/I 仍以原文证据为锚）
- 是否读取 `$research-planning`：否（同上）
- 是否读取 `$oh-my-codex:autoresearch`：否（同上）
- 是否完整阅读 `paper_content.txt`：是。覆盖范围：Page 1 abstract / contents、Page 2 §1 Introduction + §2.1 RQ + §2.2 search + Table 1、Page 3 §2.3–§2.7 inclusion/exclusion、quality assessment（DARE QA1–QA4 评分规则 Y/P/N=1/0.5/0）、§2.5 数据抽取 10 项字段、§2.6 数据分析 8 项 tabulation、§2.7 deviations、Page 4 Table 2（20 项 SLR 全表）、Page 5 Table 3 quality scores + Table 4 by-year + Table 5 by-guideline-use、Page 6 §4.1–§4.4 + Table A1（2506 / 33 / 19 yield 表）、Page 7 §4.5 limitations + Table A2 candidate-not-selected、Page 8 §5 Conclusions + Table A3 affiliation、Page 9 conclusion + acknowledgements + references。
- 是否核对 `paper.pdf`：否。原因：本会话无法可靠完成 PDF 视觉核对；但 paper_content.txt 已直接给出 Table 1/2/3/4/5/A1/A2/A3 的具体页码与列名，足以支撑文本级 schema 复原；图表版面校对应作为 A2a 任务，但不应成为不复原原文 schema 的借口。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

- 目标（§1）：以 tertiary study 评估 2004 ICSE EBSE 概念提出以来 SLR 在 SE 中的扩散与影响。
- RQ 结构（§2.1）显式四主问 + 四子问：
  - RQ1 How much SLR activity has there been since 2004?
  - RQ2 What research topics are being addressed?
  - RQ3 Who is leading SLR research?
  - RQ4 What are the limitations of current research?
    - RQ4.1 Are the research topics limited?
    - RQ4.2 Is the use of SLRs limited due to lack of primary studies?
    - RQ4.3 Is the quality of SLRs appropriate / improving?
    - RQ4.4 Are SLRs contributing to practice by defining practice guidelines?
- 贡献声明：建立 SE SLR 的早期 baseline；显示 SLR 主题集中、Simula 领跑、cost-estimation 形成证据累积、quality 在改善但与是否引用 guidelines 无显著关联。

### 2.2 方法流程

- 检索：manual search of 10 journals + 4 conferences（Table 1：IST, JSS, TSE, IEEE SW, CACM, ACM Sur, TOSEM, SPE, EMSE, IET SW, ICSE, Metrics, ISESE 等；外加 Travassos 直联与 Jørgensen 间接补充）。
- 时间窗：2004-01-01 至 2007-06-30。
- 纳入：peer-reviewed SLR + meta-analysis；排除：informal survey、关于 EBSE/SLR 流程的讨论文、重复发表。
- 抽取：one extractor + one checker（与 Kitchenham 2004 guidelines 偏离的 protocol deviation）。
- 编码：作者 + 国家 + 机构、topic area、scope（research trends vs technology evaluation）、是否引用 EBSE/guidelines paper、是否提供 practitioner guidelines、primary study 数量。
- 统计：8 项 tabulation（§2.6 显式列出）；Spearman correlation（year × score = 0.51, p<0.023）；one-way ANOVA（reference-vs-not F=0.37, p=0.55）。
- Finding 形成：从 §3.1–§3.3 描述统计 → §4.1–§4.5 逐 RQ discussion → §5 conclusion + recommendations。

### 2.3 原文显式 extraction form / classification schema / coding scheme / quality rubric

- **§2.5 Data collection（10 个显式字段）**：(1) source（journal/conference）+ full reference；(2) Classification of Type（SLR / MA）；(3) Scope（research trends / specific technology evaluation）；(4) Main topic area；(5) author(s) + institution + country；(6) summary including main RQ + answers；(7) research question/issue；(8) quality evaluation；(9) 是否引用 EBSE papers [23,5] / SLR Guidelines [22]；(10) 是否提出 practitioner-based guidelines；(11) primary study 数量。（原文列 11 项 bullet）
- **§2.4 Quality assessment（DARE 4 项）**：QA1 inclusion/exclusion 是否定义且 appropriate；QA2 检索是否覆盖；QA3 是否评估 primary study 质量；QA4 是否充分描述 basic data/studies。**评分规则**：Y=1, P=0.5, N=0, Unknown 单独标记；每项有详细 Y/P/N 判定细则（如 QA2: Y 需 ≥4 个数字图书馆或穷尽 journals；P 为 3–4 个或受限子集；N 为 ≤2 个）。
- **§2.6 Data analysis（8 项 tabulation）**：(1) per-year SLR 数 + source；(2) 是否引用 EBSE/guidelines；(3) research-trends vs technology-question 数量；(4) topics × scope 分布；(5) author / institution affiliation；(6) primary study 数；(7) quality score per SLR；(8) 是否提出 practitioner guidelines。
- **§2.7 Deviations from protocol**：4 项明确偏差（解释 EBSE-SLR 关系、扩展 RQ 描述、邮件作者补 Unknown、澄清 RQ-collection-analysis 联结）。
- **Table 2（20 项 SLR 总表）**：列 = ID, Author, Date, Topic type {research trends, technology evaluation}, Topic area, Article type {SLR, MA}, Refs {Guideline TR, EBSE paper, No}, Include practitioner guidelines {Yes, No}, Num. primary studies。
- **Table 3 quality scores**：列 = QA1, QA2, QA3, QA4, Total, Initial rater agreement；取值 {Y, P, N}；带 `*` 标记表示通过邮件作者后重新评分。
- **Table 4**：年份 × Number of studies, Mean quality, SD。
- **Table 5**：referenced vs not referenced × Number / Mean quality。
- **Table A1（search yield）**：每个 source × year × {Total / Relevant / Selected}；汇总 2506 篇扫描 → 33 relevant → 19 selected（加 2 篇额外通过 ad hoc 联系补入 → 20 unique studies）。
- **Table A2（excluded）**：14 篇候选 + reason for rejection（多为 "Informal literature survey"）。
- **Table A3（affiliations）**：study × author × institution × country。

### 2.4 Finding / gap / recommendation 形成

- 描述统计 → finding：20 篇相关 / 19 SLR + 1 MA / 12 技术评价 + 8 研究趋势 / 7 cost estimation / 3 SE experiments / 3 testing；半数引用 EBSE 或 guidelines；IEEE SW 与 TSE 各 4 篇、JSS 3 篇、IST 2 篇。
- 质量统计 → finding：所有研究 ≥1 分；仅 3 篇 <2；2 篇满分 4（S7 Jørgensen 2004、S11 Kitchenham 2007）；2 篇 3.5（S8、S20）；Spearman 年-分相关 0.51 显著；是否引用 guidelines 与质量分无显著差异。
- 主题覆盖 → gap：研究趋势型偏多；mainstream lifecycle 覆盖差；unit testing 仅 24 项 primary 而 capture-recapture 有 29 项 → 检索范围窄是 candidate explanation。
- 实践影响 → gap：仅 4 项给出 practitioner guidelines；全部集中在 cost estimation。
- Recommendation：鼓励 mapping study；建议建立 topic-specific primary-study database（Simula 模式）；美国研究者应介入；计划 2009 年底重做 + 自动化检索。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分通过 | 根节点写为"研究目标 / RQ / 贡献声明"，单位对象为 primary/secondary study，方向正确；但未在树中区分 tertiary 双层单位（本文单位是 SLR 本身，被回顾对象是 primary study）。 | M |
| 主干分支是否覆盖原文 schema | 不通过 | 现有 5 个 b1–b5 分支只是 pattern-field-schema 的通用接口层；原文显式给出的 8 项 tabulation、§2.5 10 项抽取字段、§2.4 DARE 4 项 quality rubric、§2.7 protocol deviation、§4.5 study limitations、Table A1 search-yield 桶、Table A3 affiliation 三元组（author × institution × country）都未在主干层显式登记。 | C |
| 叶子维度是否足够具体 | 不通过 | 6 个通用 leaf（scope/corpus/taxonomy/method/evidence/finding）即跨论文接口，缺少与本文绑定的具体叶子：例如 `topic_scope_type`（research trends ∨ technology evaluation）、`practitioner_guidelines_offered`（Yes/No）、`refs_EBSE_or_Guidelines`（Guideline TR / EBSE paper / No）、`num_primary_studies`（整数）、`quality_score_QAi`（{Y, P, N} → {1, 0.5, 0}）、`source_venue`（Table 1 枚举 14 项）等。当前 `原文模式候选叶子映射` 只给 4 项极粗 candidate（tertiary-corpus, quality-criteria, topic-distribution, impact-limit），且都标 `not_verified`，等于把本可文本级核验的内容降级为 A2a 待办。 | C |
| 取值空间是否可执行 | 不通过 | 所有叶子取值空间均为"自由文本 + 待核验"。原文已给封闭枚举（如 topic-type 二值、article-type {SLR, MA}、refs 三值、practitioner-guidelines 二值、QA 三值 + Unknown、source venue 14 枚举），完全可写成可统计字段。 | C |
| 关系边是否缺失 | 不通过 | 缺少 RQ→tabulation→evidence 的回链。§2.6 已显式将每个 tabulation 标注 "(addressing RQ1)" / "(addressing RQ2 and RQ4.1)" 等映射；review.md 未把这套 RQ↔analysis↔table 的关系写入树。Table 2 ↔ Table 3 ↔ Table A1 的纵向 ID（S1–S20）也是关系骨架，未被登记。 | I |
| 统计用途 / 分母是否正确 | 不通过 | 表中所有叶子的"分母"均填"当前 19 篇 survey-of-surveys 样本"，把跨论文样本错填到单篇维度树语境；原文真实分母是：(a) 2506 篇扫描全集、(b) 33 篇 relevant、(c) 19+2=20 unique studies（Table 2 主分母）、(d) 8 vs 12（是否引用 guidelines 子分母）、(e) 12 篇 tech eval 中 4 篇 practitioner-guidelines。这套真实分母完全缺席。 | C |
| 候选 finding 路径是否完整 | 不通过 | 原文 finding 链是 "tabulation → 描述统计 → 逐 RQ discussion → conclusion + recommendation"；review.md 仅给 `leaf-finding` 一个统一占位，没有把 RQ1–RQ4.4 + §5 recommendation 拆为可追溯候选 finding 节点（如 `cf-topic-narrow`、`cf-quality-improving-but-not-via-guidelines`、`cf-cost-estimation-evidence-accumulation`、`cf-practice-impact-weak`、`cf-Simula-leadership`）。 | I |
| A.1–A.4 证据链是否足够 | 不通过 | A.2 仅 4 条证据，全部 `not_verified`，页码全是占位（"摘要 / 引言页；待 A2a 精确页码复核"）；事实上 paper_content.txt 已直接显示原文页码（IST 51 (2009) 7–15，§2.1 在 Page 2、Table 2 在 Page 4、Table A1 在 Page 6、Table A3 在 Page 8 等）。本可文本级 verified 的证据被整体降级为 `not_verified`，证据链的可审计性被人为压低。 | C |
| 是否存在可能误导 A2a 的强主张 | 部分通过 | review.md 已显式自标 `schema_seed` / weak / not_verified，没有把 roadmap / vision 写成完成型 finding；但 §6 "维度树复原" 一句话结论里把树类型断言为 "tertiary 生态统计树 + 质量评价树"，在树本身尚未真复原的情况下属于过早定性，可能误导 A2a 直接套用而不回到原文 schema。 | I |

## 4. 建议维度树骨架

下面给出一个更忠实于原文的维度树骨架。结构上保留 b1–b5 通用接口层，但每个接口下挂出本文真实存在的字段叶子，并显式标注证据来源、取值空间是否封闭、是否可统计、缺失值语义。

```text
[root] EBSE/SLR-in-SE tertiary study (Kitchenham et al., IST 51:7–15, 2009)
├── b1 综述范围与 RQ
│   ├── leaf-rq-structure        取值={RQ1, RQ2, RQ3, RQ4(+RQ4.1..RQ4.4)}        来源=§2.1
│   ├── leaf-unit-of-analysis    取值={secondary_study(SLR), meta_analysis(MA)}   来源=§1, §2
│   ├── leaf-time-window         取值=[2004-01-01, 2007-06-30]                    来源=§2.3
│   └── leaf-contribution-claim  取值=自由文本 + EBSE-baseline + SE-status        来源=§1, §5
├── b2 语料收集与纳排
│   ├── leaf-source-venue        取值=Table1 枚举 14 项 (IST/JSS/TSE/IEEE SW/CACM/ACM Sur/TOSEM/SPE/EMSE/IET SW/ICSE/Metrics/ISESE) 来源=Table 1
│   ├── leaf-search-mode         取值={manual, ad-hoc-contact, web-bibliography}  来源=§2.2
│   ├── leaf-inclusion-criteria  取值=封闭枚举(2 项: SLR, MA)                     来源=§2.3
│   ├── leaf-exclusion-criteria  取值=封闭枚举(3 项: informal, procedural, duplicate) 来源=§2.3
│   ├── leaf-search-yield-table  取值=Table A1: per-source × year × {Total, Relevant, Selected}; 汇总 2506/33/19 来源=Table A1
│   └── leaf-deviation-list      取值=封闭枚举(4 项 deviation)                    来源=§2.7
├── b3 主题 / 对象分类
│   ├── leaf-topic-type          取值={research_trends, technology_evaluation}    封闭二值;可统计 来源=§2.5(3), Table 2
│   ├── leaf-topic-area          取值=开放枚举(cost_estimation, SE_experiments, testing, web, SA, COTS, ...)  来源=Table 2
│   ├── leaf-article-type        取值={SLR, MA}                                   来源=Table 2
│   ├── leaf-refs-ebse-guideline 取值={Guideline_TR, EBSE_paper, No}              来源=Table 2 列 Refs
│   ├── leaf-practitioner-guidelines 取值={Yes, No, partial}                      来源=Table 2 列 Include practitioner guidelines
│   └── leaf-num-primary-studies 取值=整数 (range 6..1485)                        来源=Table 2 列 Num. primary studies
├── b4 方法 / 抽取 / 编码
│   ├── leaf-extraction-form     取值=封闭枚举 11 项字段(§2.5 bullet 列表)        来源=§2.5
│   ├── leaf-coder-workflow      取值={one_extractor_one_checker}                 来源=§2.5
│   ├── leaf-quality-rubric      取值=DARE-QA1..QA4 with rule {Y=1, P=0.5, N=0, Unknown} + 每项判定细则 来源=§2.4
│   ├── leaf-analysis-tabulation 取值=封闭枚举 8 项 tabulation(§2.6) + RQ 映射回链 来源=§2.6
│   ├── leaf-statistical-test    取值={Spearman(year×score)=0.51 p<0.023, ANOVA(refs vs not)=F=0.37 p=0.55} 来源=§3.3
│   └── leaf-affiliation-tuple   取值=(author × institution × country)            来源=Table A3
├── b5 评价、证据、复现资产
│   ├── leaf-quality-score-table 取值=Table 3 (S1..S20 × QA1..QA4 × Total)        来源=Table 3
│   ├── leaf-quality-by-year     取值=Table 4 (year × N × mean × SD)              来源=Table 4
│   ├── leaf-quality-by-refs     取值=Table 5 (referenced vs not × N × mean)      来源=Table 5
│   ├── leaf-excluded-table      取值=Table A2 (14 项 + reason)                   来源=Table A2
│   ├── leaf-rater-agreement     取值=Initial rater agreement 列 (2..4 / 4)       来源=Table 3 末列
│   └── leaf-study-limitations   取值=封闭枚举 3 项 (manual search, single selector, single extractor) 来源=§4.5
└── b6 候选发现 / 路线图
    ├── cf-topic-coverage-narrow       支撑=Table 2 + §4.1, §4.4.1
    ├── cf-quality-improving           支撑=Table 4 + Spearman 0.51, p<0.023
    ├── cf-no-guideline-quality-link   支撑=Table 5 + ANOVA F=0.37
    ├── cf-cost-estimation-accumulation 支撑=§4.2, §5
    ├── cf-Simula-leadership           支撑=Table A3 + §4.3
    ├── cf-practice-impact-weak        支撑=§4.4.4, 12 中 4 项 guidelines
    └── cf-recommendation-mapping-study 支撑=§4.4.1 + §5
```

候选取值空间 / 是否可统计 / 缺失值语义已在叶子注释中标明，证据来源已直接绑定原文章节或 Table 号。该骨架仍在 paper_content.txt 文本级可核验范围内，A2a 工作可缩小为 PDF 视觉核对 + 字段值具体核对，而非补做原文 schema 复原本身。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干层补齐"方法 / 抽取 / 编码"独立分支 | review.md §维度树结构 | 新增 b4（或扩展现有 b4）并挂 leaf-extraction-form / leaf-quality-rubric / leaf-analysis-tabulation / leaf-statistical-test / leaf-affiliation-tuple | §2.4, §2.5, §2.6, §3.3, Table A3 | C |
| 把 4 项 DARE QA 写成可统计叶子 | review.md §叶子维度表 | 新增 leaf-quality-rubric，取值空间封闭枚举 {Y, P, N, Unknown}，并显式 Y=1/P=0.5/N=0 评分规则；附 QA1–QA4 各自判定细则 | §2.4 | C |
| 把 §2.5 的 11 项抽取字段全部登记 | review.md §叶子维度表 + 原文模式候选叶子映射 | 现有 4 项极粗 candidate 拆为：source/full_ref, type, scope, topic_area, authors/inst/country, summary, RQ, quality_eval, refs_ebse_guideline, practitioner_guidelines, num_primary_studies | §2.5 | C |
| 修正分母错填 | review.md §统计与候选发现链路 | 把"当前 19 篇 survey-of-surveys 样本"改为本文真实分母：2506 扫描总数 / 33 relevant / 20 unique studies / 12 tech-eval vs 8 trends / 8 refs vs 12 not / 4 practitioner-guidelines | Table A1, Table 2, §4.1 | C |
| 补 Table 1 / A1 / A2 / A3 为叶子级证据 | review.md §叶子维度表 + A.2 证据账本 | 增加 leaf-source-venue（Table 1 14 项）、leaf-search-yield-table（Table A1 完整桶）、leaf-excluded-table（Table A2 14 项 + reason）、leaf-affiliation-tuple（Table A3） | Table 1, A1, A2, A3 | C |
| 把 §2.7 protocol deviation 单列叶子 | review.md §叶子维度表 | 新增 leaf-deviation-list，封闭枚举 4 项 deviation | §2.7 | I |
| RQ → tabulation → finding 回链 | review.md §维度树结构 + 候选发现链路 | 显式登记 §2.6 中 "(addressing RQ1)" / "(addressing RQ2 and RQ4.1)" 等映射；把 RQ4.1–RQ4.4 拆为子节点 | §2.1, §2.6, §4.4 | I |
| 候选发现拆细 | review.md §统计与候选发现链路 | 由单一 leaf-finding 拆为 cf-topic-coverage-narrow / cf-quality-improving / cf-no-guideline-quality-link / cf-cost-estimation-accumulation / cf-Simula-leadership / cf-practice-impact-weak / cf-recommendation-mapping-study，每条挂具体表/统计支撑 | §4.1–§4.5, §5, Table 4, Table 5 | I |
| 证据 not_verified 整体降级解除 | review.md §A.2 证据账本 | paper_content.txt 已直显示原文页码与表号，EV-001/002/003/004 可升级为 `text_verified`（页码字段补 Page 2/3/4/5/6/7/8）；保留"PDF 视觉核对"作为 needs_visual_check 单独标记 | paper_content.txt 全文 | C |
| §维度树复原一句话结论降级 | review.md §维度树复原 / 一句话结论 | 在原文 schema 尚未在 review.md 内真复原前，把"主类型 = tertiary 生态统计树 + 质量评价树"降级为 candidate，附"以本审计 §4 骨架替换后方可定型" | 本审计 §3, §4 | I |
| 单位对象层级缺失 | review.md §根问题映射 | 在根节点显式区分 tertiary 双层单位：本文研究对象 = SLR/MA（次级研究），SLR 内部对象 = primary study；目前混写为 "primary study / secondary study" 易误读 | §1, §2 | M |

## 6. C/I/M 结论

- **C（5 项）**：
  1. 主干层 + 叶子层未复原原文真实 schema，只用 6 个跨论文接口替代；
  2. 取值空间未使用原文显式的封闭枚举（topic-type 二值、article-type、refs 三值、practitioner-guidelines、QA 三值等）；
  3. 统计分母错填为 19 篇 survey-of-surveys 样本，与本文真实分母（2506 / 33 / 20 / 12 / 8 等）冲突；
  4. §2.4 DARE QA 评分规则、§2.5 11 项抽取字段、§2.6 8 项 tabulation、Table 1/A1/A2/A3 在维度树中整体缺席；
  5. 证据账本整体 `not_verified`，把已可文本级 verified 的原文证据降级为 A2a 待办，破坏 Paper2 的证据可审计性、A2a 入口的精度，以及 A2b 用本文做 baseline 时的可对照性。
- **I（4 项）**：RQ→tabulation→finding 回链缺失；§2.7 protocol deviation 未单列；候选发现未拆细；"主类型 = tertiary 生态统计树 + 质量评价树"在原文 schema 尚未真复原前过早定型，可能误导 A2a 直接套用。
- **M（1 项）**：tertiary 双层单位对象未在根节点显式区分。

**最终建议：NEEDS FIX。**

理由：本文是 Paper2 引用最频繁的 tertiary baseline 之一，其 schema 复原质量直接影响 A2a 精核入口与 A2b 跨论文对照基线。当前 review.md 的"维度树复原"只完成了 Paper2 通用接口层的占位，未把原文显式给出的 11 项抽取字段、4 项 DARE QA 评分规则、8 项 tabulation、4 张关键表（Table 1/A1/A2/A3）与真实分母登记进来；这在 paper_content.txt 已全文可读、原文页码与表号已显式可见的条件下，是可避免的 schema 复原缺口，应在合入前修复 C 级项目；I 级可在同 PR 内一并补齐，M 级允许 follow-up。
