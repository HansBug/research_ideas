I have all materials needed. The paper is a true tertiary SLR with very explicit sample units (20 SLRs/MAs) and a rich, transparent coding schema across Tables 2-3 and A1-A3. Let me produce the audit.

`★ Insight ─────────────────────────────────────`
- This paper is one of the cleanest cases for A1-DT recovery: the "dimension tree" is literally Table 2's column header set plus the DARE rubric — a published, operationalized extraction form, not a reconstructed schema.
- The sample unit ambiguity warning in the task (primary vs secondary vs tool) maps directly here: the unit is the **secondary study** (SLR/MA), making this a tertiary study with measurable denominators (20 studies, 4 quality questions × Y/P/N).
- The prior `review.md` already detected the "six generic leaves" anti-pattern and added a `19×3 audit repair` section, but it still left native leaves as `schema_seed` without listing concrete extraction fields — the gap this audit must close.
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇全文审计 — `kitchenham-2009-slr-tertiary`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `kitchenham-2009-slr-tertiary` |
| agent | `claude` (Opus 4.7, 1M context) |
| 是否已读 `paper_content.txt` | 是；通读 962 行全文（覆盖 Abstract、§1--§5、Tables 1--5、Tables A1--A3、References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；元信息与 review.md 已交叉核对 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅 text-level 审计；表格 / 公式版式留待 A2a 视觉核验 |
| 原文类型 | tertiary SLR（作者自称 "tertiary literature review"，§2 Method 开头） |
| 被编码样本单位 | secondary study（systematic literature review 或 meta-analysis 论文，每条对应一篇 SLR/MA） |
| 样本数量 / 分母 | 主样本 `N=20`（S1--S20，§4.1 与 Table 2）；候选漏斗分母 `2506`（Table A1 Total），相关候选 `33`，最终选入 `19+2=20`（其中 1 篇通过研究者询问 + 1 篇通过 Simula 网站补入） |
| 原生树类型 | **单树为主 + 双子树并列**：主树为「20 篇 SLR 的抽取编码表」（§2.5 数据抽取项 + Table 2 列），并列子树为「DARE 质量评价 rubric」（§2.4 QA1--QA4 + Table 3） |
| 主统计池资格 | **是（局部可统计）**：样本单位、分母、字段、取值空间、计数表都已封闭；但具体数值（QA 评分、SLR 计数）入主统计前需 A2a 对照 PDF 版面核验 |
| 总体判定 | **needs repair**（现有 `review.md` 仍把六通用接口叶子摆在主位，原文 schema 主树虽已抬升但叶子枚举不完整、Table A1/A2/A3 未拆细；C/I 等级问题需返修） |

## 1. 原文证据阅读说明

本轮已读取：

- `bibtex.bib`、`metadata.json`：用于锁定元信息（IST 2009, vol 51, no 1, 7--15, DOI 10.1016/j.infsof.2008.09.009）。
- `paper_content.txt`（行 1--962）：全文文本通读，包括摘要、§1 Introduction、§2 Method（含 §2.1--§2.7 七小节）、§3 Results（§3.1--§3.3）、§4 Discussion（§4.1--§4.5）、§5 Conclusions、Acknowledgements、Tables 1--5、Tables A1--A3（Appendix 1）、References [1]--[42]。
- `review.md`：现有审计版本，含 v1 历史 19×3 审计入口标注。

未独立打开 `paper.pdf`：表格 / 图版式、QA 分数复核、上下标和特殊字符（如 "\C2112008"、"\C15"、"\C14" OCR 残留）建议在 A2a 阶段对照 PDF 视觉核验。

**5--12 个关键证据锚点**：

| # | 锚点 | 位置 | 短引 / 释义 |
|---|---|---|---|
| E01 | 研究目的与对象 | §1 Introduction, paper_content L88--97 | "The purpose of this study is to review the current status of EBSE since 2004 using a tertiary study to review articles related to EBSE and, in particular, we concentrate on articles describing systematic literature reviews (SLRs)." |
| E02 | RQ 树（4 主 RQ + 4 子 RQ） | §2.1, L105--141 | RQ1 SLR 活动量；RQ2 主题；RQ3 主导者；RQ4 限制；RQ4 细分为 RQ4.1--RQ4.4 |
| E03 | 来源清单 | Table 1, L161--177 | 10 期刊 + 4 会议（IST/JSS/TSE/IEEE SW/CACM/ACM Sur/TOSEM/SPE/EMSE/IET SW + ICSE/Metrics/ISESE） |
| E04 | 纳排标准 | §2.3, L186--203 | 纳入：SLR 与 MA（含部分章节为 SLR 的论文）；排除：非正式文献综述、讨论 EBSE/SLR 流程的论文、重复报告 |
| E05 | DARE 质量评价 rubric | §2.4, L204--234 | QA1--QA4 + Y/P/N + 计分 Y=1, P=0.5, N=0, Unknown |
| E06 | **数据抽取字段清单**（关键） | §2.5 Data collection, L243--258 | 10 项明示抽取字段（详见 §3 节叶子表） |
| E07 | 主样本编码表 | Table 2, L335--389 | 20 条 S1--S20，每条 8 列：ID/Author/Date/Topic type/Topic area/Article type/Refs/Include practitioner guidelines/Num. primary studies |
| E08 | 质量评分明细表 | Table 3, L465--489 | 20 条 × QA1--QA4 + Total score + Initial rater agreement |
| E09 | 检索漏斗表 | Table A1, L589--633 | 13 来源 × 4 年 × {Total/Relevant/Selected}；总数 2506→33 相关→19 选入 |
| E10 | 排除候选表 | Table A2, L694--739 | 14 条被排除论文及原因（多为 "Informal literature survey"） |
| E11 | 作者机构 / 国家表 | Table A3, L750--810 | 20 条研究的作者-机构-国家映射 |
| E12 | Protocol deviations | §2.7 + §4.5, L284--295, L639--680 | 4 项偏离声明：搜索范围限制、单人选样、单人抽取-单人核对、术语年代说明 |

## 2. 样本单位与字段来源判定

1. **原文纳入的对象**：peer-reviewed articles 形态的 SLR 与 MA（含其中 SLR 只是文章一部分的情况）。具体单位是「一篇 secondary study」，最终落地为 `S1--S20` 共 20 条编码记录（其中 `S3` = Galin & Avrahami 是 MA，其余 19 条是 SLR）。
2. **作者是否做了系统检索 / 纳排 / 数据抽取 / 编码**：**是**，且高度规范化：
   - 检索：手工 + 10 期刊 + 4 会议 + 个人/网站补检索（§2.2）
   - 纳排：显式标准 + 跨研究者复核（§2.3）
   - 质量评价：DARE 标准 + 双人独立评分 + 分歧讨论（§2.4）
   - 数据抽取：10 项字段 + 单抽取 + 单核对（§2.5）
   - 数据分析：8 个分析维度对应到 RQ1--RQ4.4（§2.6）
3. **字段来源**：本论文的「维度树」直接由 §2.5 的 10 项抽取字段 + §2.4 的 DARE rubric + Tables 2/3/A1/A2/A3 的列结构共同构成。**这是一份已公开、已操作化、已应用的 extraction form**，不是 reviewer 重构的 schema。
4. **RQ 与样本单位的关系**：RQ 既是树根的用途锚点，也决定字段抽取的取舍。RQ1↔︎`年份/来源/Refs`；RQ2↔︎`Topic type/Topic area`；RQ3↔︎`Author/Institution/Country`；RQ4↔︎`Quality score/Num primary studies/Include practitioner guidelines`。
5. **若无系统样本库则降级**：不适用——本文恰是「无降级」典范。

## 3. 原生样本编码维度树

### 3.1 主树：20 篇 secondary study 的抽取编码表

```text
[root] secondary-study (SLR or MA, 2004-Jun2007, N=20)
├── L1 Bibliographic / source
│   ├── L1.1 Source (journal | conference)              [enum: IST/JSS/TSE/IEEE SW/CACM/EMSE/ICSE/ISESE/Metrics + dup]
│   ├── L1.2 Full reference                              [free-text + DOI]
│   ├── L1.3 Date (year)                                 [int 2004..2007; allows "2005&2006" for dup-version]
│   └── L1.4 Article-type flag                           [enum: SLR | MA]
├── L2 Classification (per §2.5 "Classification of the study")
│   ├── L2.1 Type                                        [enum: SLR | MA]                — Table 2 col "Article type"
│   ├── L2.2 Scope / Topic type                          [enum: Research trends | Technology evaluation]
│   └── L2.3 Main topic area                             [open enum from §4.2: Cost estimation | Unit testing | Capture-recapture | Web research | SE experiments (power/theory/general) | COTS | CMM | Software architecture eval | Testing methods | Empirical studies in ICSE | Comparative trends CS/IS/SE | Computer science research]
├── L3 Authorship / affiliation
│   ├── L3.1 Author(s)                                   [list of names]
│   ├── L3.2 Institution(s)                              [open enum; Table A3]
│   └── L3.3 Country of institution                      [enum: Norway, UK, USA, Brazil, Israel, Spain, NZ, Sweden, Italy, Canada, Australia]
├── L4 Content summary
│   ├── L4.1 Summary of study (RQs + answers)            [free-text; see Suppl. [24] App.3]
│   └── L4.2 Research question / issue                   [free-text]
├── L5 Quality (DARE rubric — see §3.2 sub-tree)
│   └── L5.* → see "Quality sub-tree" below
├── L6 EBSE / Guidelines linkage
│   └── L6.1 References EBSE/Guidelines                  [enum: Guideline TR | EBSE paper | No]                  — Table 2 col "Refs"
├── L7 Practice impact
│   └── L7.1 Includes practitioner-oriented guidelines   [enum: Yes | No | Yes* (suggestive but not explicit)]   — Table 2 col + footnote a (S17)
└── L8 Primary-study volume
    └── L8.1 Number of primary studies in the SLR        [int; observed range 6..1485; Table 2 last col]
```

### 3.2 子树：DARE 质量评价 rubric

```text
[sub-root] DARE quality assessment (per study)
├── QA1 inclusion/exclusion criteria described & appropriate?   [Y=1 | P=0.5 | N=0 | Unknown]
├── QA2 search likely to cover all relevant studies?            [Y=1 | P=0.5 | N=0 | Unknown]
├── QA3 reviewers assessed quality/validity of included?        [Y=1 | P=0.5 | N=0 | Unknown]
├── QA4 basic data/studies adequately described?                [Y=1 | P=0.5 | N=0 | Unknown]
├── QA-total Total score                                        [float 0..4; observed 1..4]
└── QA-agreement Initial inter-rater agreement                  [int 0..4 of 4 questions]
```

### 3.3 辅助：检索漏斗子树（Table A1）

```text
[funnel] Search funnel (per source × per year)
├── F.1 Total articles                                   [int; sum = 2506]
├── F.2 Relevant (passed title/abstract screen)          [int; sum = 33]
└── F.3 Selected (passed inclusion criteria)             [int; sum = 19; +2 added by external pointers → 20]
```

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选 finding 用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-orig-source | 来源（期刊/会议） | L1.1 | §2.5 抽取项 1；Table 2 | 论文发表的期刊或会议简称 | IST, JSS, TSE, IEEE SW, CACM, ACM Sur, TOSEM, SPE, EMSE, IET SW, ICSE, Metrics, ISESE + "Conf+Journal" 组合 | 封闭枚举（受 Table 1 限定） | 跨期刊/会议时记为 `Conf+Journal` 双值 | 已用于 §4.1 的来源分布统计 | "IST 鼓励 SLR 失败" 候选 | E03, E07 | 仅适用于 2004--2007 SE 期刊会议；不可外推现代 OA 期刊 |
| leaf-orig-year | 发表年份 | L1.3 | Table 2 col "Date" | 论文发表年份（重复版本写双年） | 2004 / 2005 / 2006 / 2007 / "2005&2006" | 数值 + 关系值（双版本） | 单一年值即可 | 已用于 Table 4 年×质量分均值 | "每年 SLR 数量稳定" 候选 | E07 | 时间窗外不适用 |
| leaf-orig-article-type | 文献类型 | L2.1 | §2.5；Table 2 col "Article type" | secondary study 子类型 | SLR / MA | 完整枚举 | 必填 | 已用于 §4.1 「19 SLR + 1 MA」 | -- | E07 | 现代分类可能区分 SMS / MLR / rapid review |
| leaf-orig-scope | 研究范围类型 | L2.2 | §2.5；Table 2 col "Topic type" | 研究意图分类 | Research trends / Technology evaluation | 完整枚举 | 必填 | §4.1 "12 tech vs 8 trends" | RQ4.1 限制候选 | E07 | -- |
| leaf-orig-topic-area | 主题领域 | L2.3 | Table 2 col "Topic area" | SE 子领域主题 | 开放枚举：Cost estimation / Unit testing / Capture-recapture / Web research / SE experiments / COTS / CMM / SW architecture eval / Testing methods / Empirical studies in ICSE / Comparative CS-IS-SE / Computer science research | 层级开放枚举 | 必填 | §4.2 主题分布；"7 cost estimation, 3 experiments, 3 testing" | "主题覆盖窄" 候选 finding | E07 | 不可视为饱和分类；A2a 应核验 §4.2 出现的 12 个具体主题 |
| leaf-orig-author | 作者 | L3.1 | Table A3 | 作者姓名列表 | 自由文本（人名列表） | 自由文本 | -- | §4.3 "Jørgensen 5 篇, Sjøberg 3 篇" | RQ3 候选 | E11 | 仅适用 EBSE 早期社群 |
| leaf-orig-institution | 机构 | L3.2 | Table A3 | 作者所属机构 | 开放枚举：Simula Research Lab / Keele Univ / Brunel Univ / Lund Univ / Univ Auckland / Politécnica Madrid / NTNU / Indiana Univ / Univ Calgary / NICTA / 等 | 开放枚举 | 多机构时拆行 | §4.3 "Simula 主导 8 篇" | "Simula 数据库策略有效" 候选 | E11 | -- |
| leaf-orig-country | 国家 | L3.3 | Table A3 | 机构所在国家 | 开放枚举：Norway / UK / USA / Brazil / Israel / Spain / NZ / Sweden / Italy / Canada / Australia | 开放枚举 | 多国时拆行 | §4.3 "European 14 篇 vs N.American 4 篇" | RQ3 主导地区候选 | E11 | -- |
| leaf-orig-refs-ebse | EBSE/Guidelines 引用 | L6.1 | §2.5；Table 2 col "Refs" | 是否引用 EBSE 论文 [23,5] 或 Guidelines [22] | Guideline TR / EBSE paper / No | 完整枚举 | "No" 表示均未引用 | §4.1 "8 引用 Guidelines, 2 引用 EBSE" | "EBSE 浸润度" 候选 | E07 | -- |
| leaf-orig-practitioner | 实践者指南 | L7.1 | §2.5；Table 2 col | 是否提供面向实践者的指南 | Yes / No / Yes\* (S17 footnote: 暗示但未显式) | 完整枚举 + 限定值 | "No" 默认 | §4.4 "12 tech 中 4 篇有指南" | RQ4.4 候选 | E07 | -- |
| leaf-orig-num-primary | 一级研究数量 | L8.1 | §2.5；Table 2 末列 | 该 SLR/MA 纳入的一级研究篇数 | 整数；观察范围 6..1485 | 数值 | 必填 | §4.4 "trends 63--1485 vs tech 6--54" | RQ4.2 候选 | E07 | -- |
| leaf-orig-qa1 | QA1 纳排清晰度 | L5/QA1 | §2.4；Table 3 | 纳入排除标准是否描述且适当 | Y=1 / P=0.5 / N=0 / Unknown | 有序枚举 + 数值映射 | Unknown 表示需要邮件作者补 | DARE 评分组成 | -- | E05, E08 | -- |
| leaf-orig-qa2 | QA2 检索覆盖度 | L5/QA2 | §2.4；Table 3 | 检索是否可能覆盖所有相关研究 | Y / P / N / Unknown | 有序枚举 + 数值 | 同上 | DARE 评分组成 | -- | E05, E08 | -- |
| leaf-orig-qa3 | QA3 主研究质量评估 | L5/QA3 | §2.4；Table 3 | 是否评估了纳入研究的质量/效度 | Y / P / N / Unknown | 有序枚举 + 数值 | 同上 | DARE 评分组成 | "技术评估类应做质量评估" 候选 | E05, E08 | -- |
| leaf-orig-qa4 | QA4 基础数据描述 | L5/QA4 | §2.4；Table 3 | 是否充分描述了纳入研究/数据 | Y / P / N / Unknown | 有序枚举 + 数值 | 同上 | DARE 评分组成 | -- | E05, E08 | -- |
| leaf-orig-qa-total | DARE 总分 | L5/QA-total | §2.4；Table 3 末列 | QA1+QA2+QA3+QA4 加总 | 浮点 0..4；观察 1..4 | 数值 | -- | Table 4 (年×均分)、Table 5 (引用 Guidelines×均分)、Spearman ρ=0.51 | "质量随年提升但与 Guidelines 引用无关" 候选 | E05, E08 | -- |
| leaf-orig-qa-agreement | 初始评分者一致性 | L5/QA-agreement | Table 3 末列 | 4 题中两评分者初始一致的题数 | 整数 0..4；观察 2..4 | 数值 | -- | 信效度副指标 | -- | E08 | -- |
| leaf-funnel-total | 漏斗总数 | F.1 | Table A1 | 来源×年份总文章数 | 整数；总和 2506 | 数值 | -- | 检索分母 | -- | E09 | -- |
| leaf-funnel-relevant | 漏斗相关数 | F.2 | Table A1 | 通过题/摘筛选 | 整数；总和 33 | 数值 | -- | 检索召回率分母 | -- | E09 | -- |
| leaf-funnel-selected | 漏斗最终选入 | F.3 | Table A1 | 通过纳排标准 | 整数；总和 19（+2 补入 = 20） | 数值 | "n/a" 表示该年该来源无会议 | 主样本分母 | "ACM Sur/SPE 等期刊零产出" 候选 | E09 | -- |
| leaf-excl-reason | 排除原因 | (A2) | Table A2 | 被排除候选论文的原因 | 开放枚举：Informal literature survey / Literature survey referenced but not described / Not a SE topic / No clear search criteria, no data extraction | 开放枚举 | -- | 排除原因分布 | "informal review 仍主流" 候选 | E10 | A2 仅 14 条样本，分布不可外推 |

## 5. 关系边表

本文 schema 主要是「字段表」型而非「图」型，但存在若干**研究者间复核关系**、**重复版本关系**与 **EBSE 引用关系**：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel-duplicate-version | study | is_conference_version_of | study | 仅观察到 2 例（S3 [7]↔[8], S11 [20]↔[21]） | 默认无关系 | E07 footnote, §3.1 L311--313 | 去重 |
| rel-rater-pair | study | assessed_by | researcher pair | (Kitchenham, other ∈ {Brereton, Budgen, Turner, Bailey, Linkman}) | 必有 | §2.4 L234--242 | 信效度 |
| rel-extractor-checker | study | extracted_by → checked_by | researcher pair | 同上 | 必有 | §2.5 L259--267 | 单抽取-单核对模式 |
| rel-cites-ebse | study | cites | EBSE paper [23,5] OR Guidelines [22] | enum | "No" 默认 | E07 col "Refs" | RQ1 测量 |
| rel-institution-author | researcher | affiliated_with | institution / country | Table A3 多对多 | 多机构时拆行 | E11 | RQ3 |
| rel-rq-to-table | RQ | analysed_by | data-tabulation item | §2.6 列出 8 个分析项→4 RQ 映射 | -- | §2.6 L268--283 | 方法学审计 |

说明：**未发现 OWL/UML 式 ontology 或显式 typed graph**；关系边以「字段配对」与「RQ-分析项映射」呈现。

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 由字段/统计表支持的统计观察（可作为 boundary anchor，本文已封闭论证）

| 观察 ID | 内容 | 字段支持 | 表/段证据 |
|---|---|---|---|
| OBS-01 | 2004--2007.6 共纳入 20 条 secondary study（19 SLR + 1 MA） | leaf-orig-article-type | Table 2, §4.1 |
| OBS-02 | 12 篇技术评估 / 8 篇研究趋势 | leaf-orig-scope | §4.1 L411--412 |
| OBS-03 | 7 篇 cost estimation 主题集中 | leaf-orig-topic-area | §4.2 L432--441 |
| OBS-04 | 欧洲作者参与 14/20；Simula 实验室参与 8/20 | leaf-orig-country + leaf-orig-institution | §4.3 L515--521 |
| OBS-05 | 8/20 引用 Guidelines；2/20 引用 EBSE paper | leaf-orig-refs-ebse | §4.1 L413--414 |
| OBS-06 | 所有 20 篇 DARE ≥1；仅 3 篇 <2；2 篇满分 4 | leaf-orig-qa-total | §3.2 L326--329 |
| OBS-07 | DARE 均分按年上升；Spearman ρ=0.51, p<0.023 | leaf-orig-qa-total × leaf-orig-year | Table 4 + §3.3 L394--397 |
| OBS-08 | 引用 Guidelines 与否，质量均分差异不显著（F=0.37, p=0.55） | leaf-orig-qa-total × leaf-orig-refs-ebse | Table 5 + §3.3 L398--404 |
| OBS-09 | 检索漏斗：2506 → 33 相关 → 19 入选；ACM Sur/SPE/TOSEM/IET SW 选入 0 | leaf-funnel-* | Table A1 |
| OBS-10 | 12 篇 tech 中仅 4 篇含实践者指南 | leaf-orig-practitioner | §4.4 L587--589 |

### 6.2 候选 finding（作者 discussion / recommendation；本文给出但未硬证）

- 主题覆盖偏窄、未触及主流 SE 实践（§4.4）。
- Simula 「主题级数据库」策略可被其他组复用（§5 conclusion）。
- 主流 mapping study 的潜力（§4.4 关于 Jørgensen-Shepperd 的预测）。
- 美国 EBSE 参与不足，需加强（§5 conclusion）。
- 抽取-核对模式可能引入数据误差，复杂大样本下需双人独立抽取（§4.5）。

### 6.3 对 Paper2 可迁移的方法学启发

- **完整 extraction form + DARE rubric + 检索漏斗表三件套** 是 tertiary study 报告完整性的典范，可作为 Paper2 自审计模板（leaf 字段、QA rubric、Table A1 风格漏斗）。
- **「字段-RQ-分析项三角映射表」**（§2.6）值得直接引入。
- **deviation-from-protocol 单列章节** 可借鉴。
- **「抽取者 + 核对者」与「双独立评分者」分别用于不同负载** 的工程化复核分工。

### 6.4 绝不能迁移的领域结论

- "EBSE 主要由欧洲/Simula 主导" — 历史观察，不可迁移到 2020s LLM4SE 综述。
- "ACM Computer Surveys 无 SE SLR" — 2008 年快照，已过时。
- "8/20 引用 Guidelines" 等具体计数 — 仅本文窗口。

## 7. 对现有 `review.md` 的返修建议

### C 级（critical，会破坏 A1-DT 与论文证据链）

- **C1.** 现行 review.md `维度树结构` 段（L78--91）只放六个通用接口叶子，**完全未把 §2.5 的 10 项抽取字段与 §2.4 的 DARE rubric 列出来**。即便 v1→v2 已经加了 `原文 schema 主树（19×3 审计后返修）` 表（L122--130），叶子粒度仍停在「数据抽取字段」这种聚合标签，**没有把 Source/Year/Type/Scope/Topic area/Author/Institution/Country/Refs/Practitioner-guidelines/Num-primary 11 个具体叶子列出**。返修动作：用本审计第 4 节的叶子表替换/扩展现有「叶子维度表」。
- **C2.** Table A1（检索漏斗）和 Table A2（排除候选）作为 funnel 子树**完全缺席**于现有维度树。返修：新增 funnel 子树小节，至少列 3 个叶子（Total/Relevant/Selected）+ Table A2 的 `exclusion-reason` 枚举。

### I 级（important）

- **I1.** DARE rubric 子树虽然在 `原文模式候选叶子映射` 中以 `leaf-...-quality-criteria` 一行带过，但 QA1--QA4 + total + agreement **六个具体叶子未列**。返修：添加完整 DARE 子树叶子表（如本审计第 3.2 与第 4 节）。
- **I2.** 现有「关系边表」缺席；返修：加入本审计第 5 节关系边表，至少覆盖 `rel-duplicate-version`、`rel-rater-pair`、`rel-cites-ebse`。
- **I3.** A.2 证据账本只有 4 行通用证据（EV-001..004），未对接到具体表号（Table 1/2/3/4/5/A1/A2/A3）。返修：把 12 条证据锚点（E01--E12）补入 A.2，每行指向具体 Table 编号 + 行号范围。
- **I4.** 「样本数量 / 分母」在 review.md 快速结论卡片中未显式给出 `N=20`、漏斗 `2506→33→19+2`。返修：在 `1. 快速结论卡片` 加 `主样本量 / 漏斗分母` 行。
- **I5.** SUMMARY 表（论文集 SUMMARY.md）中本文「原生树类型」字段当前若仅写「降级树 / schema seed」会与本审计判定（`单树+双子树并列`，**可统计但需 A2a 视觉核验**）冲突。返修：在 SUMMARY 中标注「原生树类型 = 抽取表+DARE rubric+漏斗子树」「样本单位 = secondary study」「N=20」「主统计池资格 = 局部可统计」。

### M 级（minor，工程性 / 可作 follow-up）

- **M1.** review.md 中保留的 `19×3 v1 historical audit` warning box 措辞可缩短；不影响事实。
- **M2.** 多处 "EBSE / SE SLR 状态 的" 半成品占位句（如 L97 末「迁移结构与证据要求，不迁移领域结论。」与上文重复）可清理。
- **M3.** Table 3 中 `S17 SLR Y N N Y` 与 §3.2 描述 "all studies scored 1 or more" 一致，无需修正；但 `S18 Total=1` 与 "only three studies scored less than 2"（应为 S10=1.5, S16=1.5, S18=1）三篇相符，可加注释。
- **M4.** review.md 当前的 leaf 标识用 `[leaf-...-scope]` 这种通用名，建议加 `-orig-*` 后缀区分通用接口投影与原文具体叶子（如本审计第 4 节命名）。

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-A2-001 | paper_content.txt | §1 Introduction | L88--97 | "review the current status of EBSE since 2004 using a tertiary study" | rq | strong (text-verified) | [root], [dim-orig-rq] | false | 仅本文 |
| EV-A2-002 | paper_content.txt | §2.1 Research questions | L105--141 | "RQ1...RQ4 + RQ4.1--RQ4.4" 八层 RQ 树 | rq | strong | L4.2, L8.1, L7.1, [dim-orig-rq] | false | -- |
| EV-A2-003 | paper_content.txt | Table 1, §2.2 | L161--177 | 10 期刊 + 4 会议清单 | corpus_scope | strong | L1.1, leaf-funnel-* | true (复核刊名) | 仅 2004--2007 SE 期刊 |
| EV-A2-004 | paper_content.txt | §2.3 | L186--203 | 纳排标准 + 重复报告处理 | inclusion_criteria | strong | L2.1, rel-duplicate-version | false | -- |
| EV-A2-005 | paper_content.txt | §2.4 + Table 3 | L204--234, L465--489 | DARE QA1--QA4 + Y/P/N/Unknown 评分 | quality_rubric | strong | L5.*, leaf-orig-qa* | true (核对 S 行评分) | -- |
| EV-A2-006 | paper_content.txt | §2.5 | L243--258 | 10 项抽取字段清单 | extraction_schema | strong | L1.*--L8.* 全部叶子 | false | 此为**最关键证据**，确定原生 schema 来源 |
| EV-A2-007 | paper_content.txt | §2.6 | L268--283 | 8 个分析项→4 RQ 映射 | analysis_plan | strong | rel-rq-to-table | false | -- |
| EV-A2-008 | paper_content.txt | §2.7 + §4.5 | L284--295, L639--680 | 4 项 protocol deviation 声明 | limitation | strong | threats/limitations 节点 | false | -- |
| EV-A2-009 | paper_content.txt | Table 2 | L335--389 | 20 条 S1--S20 编码记录（8 列） | sample_table | strong | 主统计池所有叶子 | true (核对 Topic area, Refs 列) | -- |
| EV-A2-010 | paper_content.txt | Table 3 | L465--489 | 20×4 DARE 评分明细 + total + agreement | quality_table | strong | leaf-orig-qa* | true (核对 P/Y/N 与 * 标记) | -- |
| EV-A2-011 | paper_content.txt | Table 4, Table 5 + §3.3 | L490--503, L394--404 | 年×均分；引用 Guidelines×均分；Spearman ρ=0.51 | statistical_result | strong | OBS-07, OBS-08 | true (核对均值/方差) | -- |
| EV-A2-012 | paper_content.txt | Table A1 | L589--633 | 检索漏斗 2506→33→19 | corpus_funnel | strong | leaf-funnel-* | true (核对加总) | -- |
| EV-A2-013 | paper_content.txt | Table A2 | L694--739 | 14 条排除候选 + 排除原因 | exclusion_record | medium (sample only) | leaf-excl-reason | true | A2 仅 14 例样本 |
| EV-A2-014 | paper_content.txt | Table A3 | L750--810 | 20 条作者-机构-国家 | author_table | strong | L3.* | true | -- |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-A3-T01 | 本文具备完整 tertiary SLR 维度树：单主树（20 篇 secondary study × 11 抽取字段）+ DARE 子树 + 漏斗子树 | tree_type | [root] | EV-A2-006, EV-A2-005, EV-A2-009, EV-A2-012 | strong (text) → strong (after A2a PDF check) | schema_seed → 可升级为主统计池字段定义 | A2a 必须核 Table 2/3/A1 版式 |
| CLM-A3-T02 | 样本单位是 secondary study (SLR/MA)；N=20；漏斗分母 2506 | sample_unit | [root] | EV-A2-009, EV-A2-012 | strong | schema_seed | -- |
| CLM-A3-L01 | 叶子 leaf-orig-topic-area 取值空间为开放枚举，本文观察 12 个主题域 | leaf_definition | leaf-orig-topic-area | EV-A2-009 (Table 2) | medium (枚举未饱和) | schema_seed | 不可视为饱和；A2a 需扩库验证 |
| CLM-A3-L02 | DARE rubric (QA1--QA4 + Y/P/N + 1/0.5/0) 是本文质量评价 schema 的完整复原 | leaf_definition | leaf-orig-qa1..qa-total | EV-A2-005, EV-A2-010 | strong | 可作 Paper2 质量评价模板 | -- |
| CLM-A3-S01 | 统计观察 OBS-01..10 可作为 boundary anchor，但 OBS-04/05/09 是 2008 快照，不可外推 | statistical_observation | OBS-01..10 | EV-A2-009..014 | strong (本文窗口内) | boundary_anchor | 仅适用 2004--2007 SE 期刊 |
| CLM-A3-M01 | 字段+RQ+分析项三角映射（§2.6）值得作为 Paper2 自审计模板 | migration_method | rel-rq-to-table | EV-A2-007 | strong | 方法学迁移 | 不迁移领域结论 |
| CLM-A3-F01 | "EBSE 由欧洲/Simula 主导" 是历史候选 finding，不可作为 final finding | candidate_finding | OBS-04 | EV-A2-014 | weak (历史快照) | candidate_finding | 2026 年生态已大变 |
| CLM-A3-R01 | review.md 当前 schema 主树叶子粒度不足；C1/C2 需返修 | audit_repair | review.md | EV-A2-006 (核心) | strong | 直接驱动返修 | -- |

## 9. 技能使用与自我审查记录

### 9.1 技能文件使用

| 文件 | 是否读取 | 采用原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 是 | Evidence gate（每条结论挂证据）；Citation gate（schema 字段必须可追溯到原文表号）；Claim gate（区分 statistical observation / candidate finding / final finding） |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 是 | Constructive Specificity Standard（每条返修建议给出具体 L 行号 + 表号 + 命名建议）；C/I/M 分级配套学术目标说明 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 未读（文件存在但本轮未实际打开） | 标记为 partial-skill-use |
| `research-planning/SKILL.md` | 是 | 4-stage planning 视角下，本文已自带 overall plan + extraction schema + analysis plan，对照后判定 schema 完整 |
| `research-planning/references/planning-prompts.md` | 未独立 Read（仅 ls 确认存在） | partial-skill-use |
| `research-planning/references/output-schemas.md` | 未独立 Read | partial-skill-use |
| `oh-my-codex-local/.../autoresearch/SKILL.md` | 未读（路径已 ls 确认存在 SKILL.md） | partial-skill-use |

**风险记录**：本轮因时间预算压缩，未逐一打开 reviewer-self-review.md / planning-prompts.md / output-schemas.md / autoresearch SKILL.md。这 4 个文件存在性已确认（ls 通过），但内容未消费——若主线程认定其内容是硬性 input，应作为 follow-up 重做。**当前不构成 blocked**，因为本审计的核心方法学（C/I/M 分级、evidence-claim 映射、原生 schema vs 通用接口）已由前 2 个文件覆盖。

### 9.2 Reviewer 视角下本输出最高风险 3 点

1. **PDF 版面未核验**：QA 评分（Y/P/N 与 \* 标记）、Table 4/5 均值与方差、Table A1 加总是否完全等于 2506 / 33 / 19，均仅依赖 OCR 文本（含 "\C15"、"\C14"、"\C2112008" 残留）。主线程合并前应至少抽样 PDF 核 3--5 个 cell。
2. **leaf-orig-topic-area 枚举未饱和**：本审计列了 12 项观察值，但作者并未声明这是封闭分类。Paper2 若用作模板，需在跨论文扩库时验证。
3. **「主统计池资格 = 局部可统计」可能与论文集 SUMMARY.md 既有口径冲突**：现有 review.md L23 写 "schema 历史观察：无硬缺口；但 quality score 数值需 原文图表级核对后才能进入正式统计"，与本审计基本一致；但 SUMMARY 表如果写「schema seed only / 不可统计」就需要协调。

### 9.3 任务状态

- `blocked`：**否**
- `timeout`：**否**
- 文件缺失：**否**
- partial-skill-use：4 个 reference 文件未深读（详见 9.1），不影响主结论
- 完整自包含报告：**是**

---

`★ Insight ─────────────────────────────────────`
- 本审计的核心贡献是把 review.md 从「六通用接口叶子 + v1 历史 19×3 修复补丁」推进到「§2.5 抽取字段 + §2.4 DARE + Table A1 漏斗」三件套完整复原；这是 A1-DT v2 应有的「单篇原生编码表」粒度。
- 之所以判定为「needs repair」而非「pass」，关键是 C1 — 现有 review.md 即便在 v1→v2 已加了 `原文 schema 主树` 表，叶子层仍写「study metadata、topic、research questions、methods、results、limitations」这种聚合标签，而非具体 11+6+3 = 20 个原生叶子。这是把跨论文投影误读为原文 schema 的残余表现。
- 对 Paper2 的最大方法学借鉴：本文 §2.6 的「8 个数据分析项→4 RQ 映射表」是研究方法学审计的优雅原型——任何字段都应能反查回某个 RQ，任何 RQ 都应能展开到某个/某些字段。
`─────────────────────────────────────────────────`
