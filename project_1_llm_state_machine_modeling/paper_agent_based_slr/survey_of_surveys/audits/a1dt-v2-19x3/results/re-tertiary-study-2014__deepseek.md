Now I have all the evidence. Let me construct the complete A1-DT v2 audit report.

---

# A1-DT v2 单篇全文审计报告：`re-tertiary-study-2014`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-tertiary-study-2014` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。全文 966 行，已逐段通读 I--V 节及 Appendix A（参考文献列表） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。二者均已完整读取 |
| 是否打开或核对 `paper.pdf` | 否。全部阅读基于 `paper_content.txt` 文本提取；Table I--VI、Figure 1--4 的内容已从文本中定位，但未做 PDF 版面视觉核验（如图表行列精确对齐、OCR 可能的 S-ID/数字误识别） |
| 原文类型 | **tertiary study**（三级研究：系统综述的系统综述） |
| 被编码样本单位 | **individual systematic review (SLR) in Requirements Engineering**——即每一篇纳入的 RE 领域系统文献综述 / 系统映射研究 / 元分析 |
| 样本数量 / 分母 | **53 篇 distinct SLR**（报告于 64 篇出版物中）；2 篇 SLR 无法获取全文（S3, S8），1 篇 SLR 无法确定出版渠道（S40） |
| 原生树类型 | **单树**（每个样本单位共享同一套 extraction form 字段，个别字段存在缺失值） |
| 主统计池资格 | **是**——有明确系统检索 / 纳排 / 数据抽取流程，53 个样本单位有完整的 per-unit 编码方案，且大部分字段有可量化取值空间 |
| 总体判定 | **needs repair**——现有 review.md 中"维度树复原"一节已部分修正了六叶问题，但仍有多处把通用六叶接口残余写入了维度树和证据账本；叶子维度表需要按原文 extraction form 重写 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取文件

- `paper_content.txt`：全文 966 行，覆盖 Page 1（版权声明）至 Page 9（附录 A 参考文献列表），包括 I. Introduction、II. Systematic Mapping Tertiary Study（含 Planning / Execution）、III. Results and Discussion、IV. Limitations of the Study、V. Conclusion and Future Work、References、Appendix A
- `bibtex.bib`：BibTeX 条目，含 DOI `10.1109/EmpiRE.2014.6890110`
- `metadata.json`：完整元数据，确认 tertiary study、EmpiRE 2014 workshop、CCF 非 venue
- `review.md`：现有 220 行 review，含结论卡片、六叶 pattern、A1-M0--M6 贡献、维度树复原、A.1--A.4

### 1.2 是否需 PDF 视觉核验

以下内容已从 `paper_content.txt` 中定位，但**建议后续进行 PDF 版面核验**：
- Table I（QA Criteria）的评分细则与行对应关系
- Table II（Search Execution and Study Selection Summary）的数字合计
- Table IV（Scope Classification）的 S-ID 列表完整性
- Table V（Topics and Primary Studies）的 S-ID、# of PS、Year 对应——OCR 提取中部分特殊字符可能误识别（如 `→` 写为 `barb2right`），需 PDF 确认
- Table VI（Top 10 Highly Cited SLR）的 citation count
- Figure 1--4 的图形数据点精确值

### 1.3 关键原文证据锚点（10 个）

| 编号 | 原文位置 | 锚点内容 |
|---|---|---|
| EV-001 | Abstract（Page 2） | "identified 53 distinct systematic reviews published from 2006 to 2014 and reported in 64 publications" — 样本总量声明 |
| EV-002 | §II.A Planning（Page 3） | 三个 RQ 的完整文本：RQ1（coverage areas）、RQ2（quality）、RQ3（gaps） |
| EV-003 | §II.A Planning（Page 3） | Table I 的 QA Criteria：QA1（Inclusion/Exclusion）、QA2（Search Space Adequacy）、QA3（Quality Assessment of Primary Studies）、QA4（Information regarding Primary Studies），每项 Yes=1 / Partial=0.5 / No=0 |
| EV-004 | §II.A Planning（Page 3--4） | 数据抽取字段描述："publication details showing characteristics of the included SLR (i.e. title, authors, year of publication, type of publication, conference/journal name and complete reference, and number of citations to that paper) and information required to answer our three RQs (i.e. number of primary studies, focus of SLR)" |
| EV-005 | §II.A（Page 4） | "grouping of main topics ... was done by applying thematic analysis [12] of the titles and abstracts" — 主题分组方法 |
| EV-006 | §II.B Execution（Page 4） | Table II 搜索执行摘要：primary searches 267→91→58（去重后），secondary searches +6，最终 64 publications / 53 studies |
| EV-007 | §III Results（Page 4--5） | Table IV Scope Classification：state of the art (33)、methods (7)、techniques (7)、tools (4)、frameworks (1)、technology (1) |
| EV-008 | §III Results（Page 5--6） | Table V Topics and # of PS：主题分组 + S-ID + per-SLR primary study count + year |
| EV-009 | §III RQ2（Page 6） | "42 studies out of 51 have scored 2 or above out of 4" + Figure 3 的 QA 分项分布描述 |
| EV-010 | §III RQ3（Page 6--7） | 三类 gap 的完整阐述：anomalies（S1 vs S4 的 primary study 数量矛盾）、lack of primary studies（<10 的 SLR）、ignored RE areas（goal-oriented RE、RE in law、requirements modeling notations） |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**对象是每一篇以 Requirements Engineering 为主题的系统文献综述（SLR）、系统映射研究（Systematic Mapping Study）或元分析（meta-analysis）。**

证据：§II.A 的 study selection criteria 要求每篇入选文献必须同时满足：(1) 英文、(2) 为 Systematic Review / Systematic Mapping Study / meta-analysis、(3) 聚焦 RE 领域内任何子主题。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**有，且完整描述了流程：**

- **检索**：automated search（Google Scholar、IEEE Xplore、ACM DL、Science Direct、EI Compendex）+ manual search（4 篇既往 tertiary study 参考文献 + RE/SLR 相关会议期刊）
- **纳排**：标题/摘要扫描排除无关文献 → 三项 selection criteria → 去重 → 多版本出版物归并到同一 study ID
- **数据抽取**：extraction form 包含 publication details（title/authors/year/type/venue/reference/citation count）+ per-RQ 信息（number of primary studies, focus of SLR）
- **编码方案**：
  - Scope classification：6 类（state of the art / methods / techniques / tools / frameworks / technology）
  - Topic classification：thematic analysis 分组（Non Functional Requirements、Complete RE Process、Model Driven Development 等）
  - Quality assessment：4 项 QA criteria，每项 0/0.5/1 分

### 2.3 原文字段来自哪里？

- **Extraction form 字段**：§II.A 明确描述了 per-study 抽取的数据项（EV-004）
- **Quality rubric**：Table I（EV-003），改编自 [8, 9, 11]，根源于 CDR DARE（York University）
- **Scope taxonomy**：Table IV（EV-007）——作者自建的 6 类分类法
- **Topic taxonomy**：Table V（EV-008）——基于 thematic analysis 的自下而上分组，非预定义分类法
- **Publication type taxonomy**：Table III——conference / journal / workshop / technical report / thesis / unknown

### 2.4 RQ 与样本单位的关系

RQ 驱动了 extraction form 的设计：
- **RQ1**（coverage areas）→ 抽取 `focus of SLR` + `number of primary studies`，然后通过 thematic analysis 生成 Table V 的 topic grouping；同时使用 Table IV 的 scope classification
- **RQ2**（quality）→ 对每个 SLR 整体应用 Table I 的 QA criteria 打分；同时抽取 per-publication 的 Google Scholar citation count
- **RQ3**（gaps）→ 跨样本单位综合分析（anomaly detection、low-PS-count identification、roadmap 对照），**不是 per-unit 编码字段，而是 cross-unit synthesis**

RQ 是**树的设计意图和结果组织方式**，不是树的根节点。树的根节点是"纳入的 SLR"本身。

### 2.5 降级必要性

**不需要降级。** 本文有明确的系统样本库（53 个 SLR）、明确的数据抽取方案、明确的 per-unit 编码字段和取值空间。完全具备主统计池资格。

但需注意：
- 2 篇 SLR（S3, S8）全文不可获取，其 QA score 可能不完全
- 1 篇 SLR（S40）出版渠道未知
- Topic grouping 是作者自下而上的 thematic analysis 产物，不是引用外部标准分类法

---

## 3. 原生样本编码维度树 / 维度森林

### 3.1 树类型判定

**单树**——所有 53 个 SLR 样本使用同一套 extraction form 字段编码。不存在多个独立编码方案。

### 3.2 原生维度树（完整 text tree）

```
纳入 SLR（53 units）
│
├── [B1] 书目元数据（Bibliographic）
│   ├── L1.1 作者（authors）                        [自由文本]
│   ├── L1.2 出版年份（year）                        [数值：2006--2014]
│   ├── L1.3 出版类型（publication_type）            [完整枚举：conference/journal/workshop/technical report/thesis/unknown]
│   ├── L1.4 出版渠道（venue_name）                  [自由文本 + 外部分类法引用（会议/期刊名）]
│   ├── L1.5 完整引用（full_reference）              [自由文本]
│   ├── L1.6 Study ID                               [自由文本：S1--S53，多版本加 A/B/C 后缀]
│   └── L1.7 多版本标记（multi_publication_flag）    [布尔：单版本/多版本]
│
├── [B2] 综述类型（Review Type）
│   └── L2.1 综述类型（review_type）                 [完整枚举：conventional SLR / systematic mapping study / meta-analysis]
│
├── [B3] 范围分类（Scope Classification）
│   └── L3.1 研究范围（scope）                      [完整枚举：state of the art / methods / techniques / tools / frameworks / technology]
│
├── [B4] 主题分类（Topic Classification）
│   ├── L4.1 主题分组（topic_group）                 [层级枚举：thematic analysis 产生的分组名，如 "Non Functional Requirements" → 可细分 "Security RE" / "Quality Requirements" / "Cloud Computing Security" 等]
│   └── L4.2 子主题聚焦（focus_within_topic）        [自由文本：每篇 SLR 的具体聚焦描述]
│
├── [B5] 实证覆盖度（Empirical Coverage）
│   └── L5.1 纳入初级研究数量（num_primary_studies） [数值或区间：5--4089]
│
├── [B6] 质量评估（Quality Assessment）
│   ├── L6.1 QA1 纳排标准（qa_inclusion_exclusion）  [完整枚举：0 / 0.5 / 1]
│   ├── L6.2 QA2 检索充分性（qa_search_adequacy）   [完整枚举：0 / 0.5 / 1]
│   ├── L6.3 QA3 初级研究质量评估（qa_ps_quality）  [完整枚举：0 / 0.5 / 1]
│   ├── L6.4 QA4 初级研究信息完整性（qa_ps_info）   [完整枚举：0 / 0.5 / 1]
│   └── L6.5 QA 总分（qa_total_score）              [数值：0--4，步长 0.5]
│
└── [B7] 引用影响力（Citation Impact）
    └── L7.1 Google Scholar 引用数（gs_citation_count） [数值：0--154]
```

### 3.3 说明

1. **B1 Bibliographic** 是 per-publication 字段；当一篇 SLR 有多个 publication 时，这些字段按 publication 粒度记录，但在 quality assessment 时归并到 study 级别
2. **B4 Topic Classification** 的取值空间来自作者自下而上的 thematic analysis，不是引用外部预定义分类法（如 SWEBOK），因此取值空间是"作者观察产生的层级枚举"
3. **B6 Quality Assessment** 对 53 个 SLR 中 51 个完成了评分（S3 和 S8 全文不可获取，推断 QA 不完整或缺失）
4. **B7 Citation Impact** 的引用数截至于 2014 年 5 月 19 日，是时间快照值
5. **关系边**：RQs 作为分析维度跨接字段——RQ1 使用 B3+B4+B5，RQ2 使用 B6+B7，RQ3 跨 B5+B4 做 cross-unit anomaly detection（见第 5 节关系边表）

### 3.4 A2a 精核任务

以下叶子字段的取值空间需要 A2a 进一步精核：
- L4.1 `topic_group` 的完整取值全集（当前 Table V 列出约 15 个分组，但原文承认"neither exhaustive nor complete"）
- L6.1--L6.4 各 QA 分项的 per-study 分布（当前仅知 Figure 3 的分布趋势，非逐 S-ID 值）
- L7.1 `gs_citation_count` 仅 Table VI 列出 Top 10；其余 43 篇 SLR 的引用数未逐篇公布

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1.1 | 作者 | B1 书目元数据 | extraction form §II.A | SLR 的作者列表 | 自由文本 | 自由文本 | 部分 thesis 可能缺少完整作者信息 | 不直接统计 | 可用于 co-authorship network | EV-004 | 所有 tertiary/SLR 通用 |
| L1.2 | 出版年份 | B1 书目元数据 | extraction form §II.A | SLR 出版年份 | 2006--2014 | 数值 | S40 年份为 NF（Not Found） | 年度趋势统计（Figure 1） | 识别领域兴趣爆发点（2009 年激增） | EV-004, Figure 1 | 通用 |
| L1.3 | 出版类型 | B1 书目元数据 | extraction form §II.A | SLR 出版物的渠道类型 | conference / journal / workshop / technical report / thesis / unknown（6 类） | 完整枚举 | S40 为 unknown | 按渠道统计分布（Table III） | 评估领域 SLR 的发表成熟度 | EV-004, Table III | 通用 |
| L1.4 | 出版渠道名 | B1 书目元数据 | extraction form §II.A | 会议/期刊/工作坊名称 | 自由文本（如 REJ、IST、ESEM、REFSQ 等） | 自由文本 + 外部分类法引用 | 部分 SLR 为 thesis 无会议/期刊名 | 按 venue 统计 | 识别 RE SLR 的 target venue 集中度 | EV-004, Appendix A | SE 子领域特定 |
| L1.5 | 完整引用 | B1 书目元数据 | extraction form §II.A | 完整文献引用字符串 | 自由文本 | 自由文本 | 无 | 审计追踪 | 可复现性 | EV-004, Appendix A | 通用 |
| L1.6 | Study ID | B1 书目元数据 | §II.B execution | 分配给每篇 SLR 的唯一 ID | S1--S53（多版本加 A/B/C 后缀） | 标识符 | S40 出版渠道未知但 ID 存在 | 去重 + cross-reference | 跨表引用一致性 | §II.B, Table IV/V/VI | 通用 |
| L1.7 | 多版本标记 | B1 书目元数据 | §II.A selection criteria | 单篇 SLR 是否有多个出版物版本 | 单版本 / 多版本（2--3 publications） | 布尔 | 默认 false | 多版本归并（53 studies ≠ 64 publications） | 防止重复计数 | EV-004, EV-005 | 通用 |
| L2.1 | 综述类型 | B2 综述类型 | §III Results | SLR 的方法论类型 | conventional SLR / systematic mapping study / meta-analysis（3 类） | 完整枚举 | 可推断为 conventional SLR（默认） | 按类型统计分布 | 评估 RE 领域 SLR 的方法论多样性 | §III Results（"12 Systematic Mapping Studies...one Meta-Analysis (S42)"） | 通用 |
| L3.1 | 研究范围 | B3 范围分类 | Table IV §III RQ1 | SLR 的研究目的范围分类 | state of the art / methods / techniques / tools / frameworks / technology（6 类） | 完整枚举 | 每篇 SLR 均有分类 | 按 scope 统计分布 | 识别研究方法论偏重（33/53 为 state of the art） | Table IV, EV-007 | 可迁移但 scope 分类标准需适配目标领域 |
| L4.1 | 主题分组 | B4 主题分类 | Table V §III RQ1 | 基于 thematic analysis 的 RE 子主题分组 | Non Functional Requirements / Complete RE Process / Model Driven Development / Knowledge Management and RE / RE in GSD / RE in Software Product Lines / Requirements Management / Multi Agent Systems / Requirements Reuse / Value based RE / Virtual Reality Systems 等约 15 组 | 层级枚举（作者观察产生） | 每篇 SLR 均有分组 | 识别 RE 研究热点与冷门 | RQ3 gap analysis（ignored areas） | Table V, EV-008 | **不可直接迁移**——topic taxonomy 高度 RE 子领域特定；可迁移的是"自下而上 thematic analysis + 对照 roadmap 找 gap"的方法学模式 |
| L4.2 | 子主题聚焦 | B4 主题分类 | Table V §III RQ1 | 每篇 SLR 在主题分组内的具体聚焦描述 | 自由文本（如 "Data Quality Requirements in a Software Product Development"） | 自由文本 | 无 | 语义理解 | A2a 可能需要 NLP 聚类以扩展分组 | Table V Column "Focus of SLR" | 高度领域特定 |
| L5.1 | 纳入初级研究数 | B5 实证覆盖度 | extraction form §II.A | SLR 纳入的 primary studies 数量 | 5--4089（整数） | 数值 | 个别 SLR 标注 NM（Not Mentioned） | RQ1 coverage 统计（Table V） | RQ3 anomaly detection（S1:8 vs S4:240 on same topic） | Table V Column "# of PS", EV-008 | 通用；需注意不同 SLR 的 primary study 归口标准差异 |
| L6.1 | QA1 纳排标准 | B6 质量评估 | Table I §II.A | 是否定义了纳入/排除标准 | 0 / 0.5 / 1 | 完整枚举（3 值有序） | S3, S8 全文不可获取，QA 不完整或缺失 | Figure 3 分项分布 | RQ2 quality trend（过半 SLR 忽略了 QA3 和 QA4） | Table I, EV-003, Figure 3 | 通用 QA rubric，可迁移 |
| L6.2 | QA2 检索充分性 | B6 质量评估 | Table I §II.A | 检索的数字图书馆数量和附加策略 | 0 / 0.5 / 1 | 完整枚举（3 值有序） | 同上 S3, S8 | Figure 3 分项分布 | 同上 | Table I, EV-003 | 通用 QA rubric，可迁移 |
| L6.3 | QA3 初级研究质量评估 | B6 质量评估 | Table I §II.A | 是否评估了纳入初级研究的质量 | 0 / 0.5 / 1 | 完整枚举（3 值有序） | 同上 S3, S8 | Figure 3 分项分布 | **关键 finding**：过半 SLR 忽略了 QA3 | Table I, EV-003, Figure 3 | 通用 QA rubric |
| L6.4 | QA4 初级研究信息完整性 | B6 质量评估 | Table I §II.A | 是否提供了初级研究的完整信息或摘要 | 0 / 0.5 / 1 | 完整枚举（3 值有序） | 同上 S3, S8 | Figure 3 分项分布 | **关键 finding**：过半 SLR 忽略了 QA4 | Table I, EV-003, Figure 3 | 通用 QA rubric |
| L6.5 | QA 总分 | B6 质量评估 | §III RQ2 | 四项 QA 的总分 | 0--4（步长 0.5） | 数值（有序区间） | S3, S8 缺失；2 篇 SLR 用 QA score 0（S41, S52 from Table VI） | Figure 2 分布、Figure 4 年度趋势 | 主要统计结论："quality decreasing since 2009" | Figure 2, Figure 4, EV-009 | 通用 |
| L7.1 | 引用数 | B7 引用影响力 | §II.A, Table VI | Google Scholar citation count（截至 2014-05-19） | 0--154（整数） | 数值 | 仅 Table VI 列出 Top 10；其余 43 篇未逐篇公布 | Table VI Top 10 排序 | 发现"highest cited ≠ highest quality"（S2[A]:154 cites vs QA=3） | Table VI, EV-004 | 通用，但时间快照值不可迁移 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| RE-01 | RQ1（coverage areas） | 驱动编码 | B3 scope + B4 topic + B5 num_primary_studies | per-unit 编码 | -- | EV-002, EV-004 | 确定哪些字段用于回答 RQ1 |
| RE-02 | RQ2（quality） | 驱动编码 | B6 quality assessment（QA1--QA4 + total）+ B7 citation count | per-unit 编码 | S3, S8 QA 不完整 | EV-002, EV-003, EV-009 | 确定哪些字段用于回答 RQ2 |
| RE-03 | RQ3（gaps） | 跨单位综合分析 | B4 topic + B5 num_primary_studies（cross-unit） | cross-unit anomaly / gap | -- | EV-002, EV-010 | RQ3 不是 per-unit 编码，而是跨 S-ID 的对比分析 |
| RE-04 | L4.1 topic_group | 归类关系 | L4.2 focus_within_topic | 多对一：一个 topic_group 下可有多个 SLR 的 focus | -- | Table V, EV-008 | 主题层级结构 |
| RE-05 | L1.7 multi_publication_flag | 聚合关系 | L6.1--L6.5 QA scores | 多版本出版物 QA 归并到 study 级别评分 | 单版本 SLR 无需归并 | §II.A ("grouping multiple publications together where applicable") | QA 评分的粒度选择 |
| RE-06 | B5 num_primary_studies | 对比关系 | B5 num_primary_studies（不同 S-ID） | cross-unit anomaly detection | -- | EV-010 (§III RQ3 "Anomalies") | S1(8) vs S4(240) 同主题矛盾 |
| RE-07 | L1.2 year | 时间序列关系 | L6.5 qa_total_score | annual average quality trend | S3, S8 缺失值插入 | Figure 4, EV-009 | "quality decreasing since 2009" 的时间趋势结论 |
| RE-08 | B4 topic_group | 对照关系 | 外部 roadmap [1][2] | Chang & Atlee (2007) + Nuseibeh & Easterbrook (2000) 提出的 RE research agenda | -- | §III RQ3 ("Ignored RE areas"), EV-010 | gap identification：goal-oriented RE / RE in law / requirements modeling notations / conflict resolution / requirements negotiation 无 SLR 覆盖 |

**说明**：未发现原文定义了显式关系型 schema（如 ER 图、relational table、ontology mapping）。上述关系边是从作者的分析逻辑和结果组织中推断的**隐含关系边**。原文的 extraction form 本质上是扁平字段集合 + per-RQ 分析维度，没有 inter-field 关系约束。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文由字段 / 统计表支持的统计观察

| 编号 | 统计观察 | 支撑字段 | 证据锚点 | 类型 |
|---|---|---|---|---|
| SO-01 | 53 篇 distinct SLR / 64 篇 publications，时间跨度 2006--2014 | L1.2, L1.7 | EV-001, Table II | 描述性统计 |
| SO-02 | 2009 年起 SLR 数量激增 | L1.2 | Figure 1 | 趋势观察 |
| SO-03 | 出版类型分布：conference(31) > journal(16) > thesis(8) > workshop(4) = technical report(4) | L1.3 | Table III | 描述性统计 |
| SO-04 | Scope 分布：state of the art(33) >> methods(7) = techniques(7) > tools(4) | L3.1 | Table IV | 描述性统计 |
| SO-05 | Primary studies 数量范围 5--4089，4 篇 SLR 报告 >200 primary studies | L5.1 | Table V, EV-008 | 描述性统计 |
| SO-06 | 42/51 SLR QA 总分 ≥2/4 | L6.5 | EV-009 | 描述性统计 |
| SO-07 | **2009 年起 average QA score 下降** | L1.2 + L6.5 | Figure 4, EV-009 | **趋势发现** |
| SO-08 | **过半 SLR 忽略 QA3（primary study quality）和 QA4（primary study info）** | L6.3, L6.4 | Figure 3, EV-009 | **质量发现** |
| SO-09 | Top cited ≠ highest quality（S2[A]:154 cites, QA=3） | L7.1 + L6.5 | Table VI | 反直觉观察 |

### 6.2 原文 discussion / recommendation 提出的候选 finding

| 编号 | 候选 finding | 来源章节 | 证据锚点 | 可迁移性 |
|---|---|---|---|---|
| CF-01 | RE SLR 的质量自 2009 年以来下降，需要社区关注 | §III RQ2 | EV-009, Figure 4 | **可迁移**：SLR 质量随时间下降的模式可能在所有 SE 子领域都存在 |
| CF-02 | 存在同行 SLR 在同一主题上报告差异极大的 primary study 数量（S1:8 vs S4:240），暗示 SLR 方法执行不一致，需要 replication | §III RQ3 "Anomalies" | EV-010 | **可迁移**：cross-SLR anomaly detection 是一种通用 tertiary study 分析方法 |
| CF-03 | goal-oriented RE、RE in law、requirements modeling notations、conflict resolution、requirements negotiation 等已知 RE 重要领域无 SLR 覆盖 | §III RQ3 "Ignored RE areas" | EV-010 | **不可迁移具体领域结论**——可迁移的是"对照 roadmap 找 gap"的方法学模式 |
| CF-04 | 少数 SLR 只报告 <10 primary studies，可能是 neglected area 或 SLR 检索不充分 | §III RQ3 "Lack of primary studies" | EV-010 | **可迁移**：low-PS-count 的 dual-interpretation 分析框架 |
| CF-05 | 需要 replication studies 以验证已有 SLR 结果的可靠性 | §III RQ3 + §V Conclusion | EV-010 | **可迁移**：tertiary study 应产出 replication recommendation |

### 6.3 对 Paper2 可迁移的方法学启发

| 编号 | 启发 | 迁移方式 |
|---|---|---|
| MH-01 | **Tertiary study 的 extraction form 字段结构**：bibliographic + type + scope + topic + empirical_coverage + quality + impact——这七分支可作为 Paper2 "survey of SLR on LLM4StateMachine" 的 extraction form 骨架 | 直接迁移字段结构，替换 topic taxonomy |
| MH-02 | **QA rubric 的四项标准**（QA1 inclusion/exclusion, QA2 search adequacy, QA3 primary study quality, QA4 primary study info completeness）可直接用于评估 LLM4StateMachine 相关 SLR 的质量 | 直接迁移 QA rubric |
| MH-03 | **Cross-study anomaly detection 方法**：同一子主题不同 SLR 的 primary study 数量差异揭示方法学不一致 | 直接迁移分析方法 |
| MH-04 | **对照领域 roadmap/expert review 找 gap** 的方法学模式 | 迁移方法学 |
| MH-05 | **thematic analysis 作为 topic grouping 方法**：不依赖外部预定义分类法，自下而上从 title/abstract 中抽取 | 迁移方法学 |

### 6.4 绝不能迁移的领域结论

- RE 子领域的任何具体 topic、gap、hotspot：如"Security RE 已被 SLR 覆盖""goal-oriented RE 缺乏 SLR"——这些是 RE 领域特定结论
- Google Scholar citation count 的具体数值（2014 年时间快照）
- 任何关于 RE SLR 质量下降的数值趋势（仅适用于 RE 领域在该时间段）
- Table V 中任何具体的 topic grouping 名称和分类体系

---

## 7. 对现有 `review.md` 的返修建议

### C 级（Critical——阻塞统计池资格或维度树正确性）

| 编号 | 问题 | 建议 | 严重性 |
|---|---|---|---|
| C-01 | §2 "六类 pattern 抽取" 中，`dimension pattern`、`finding pattern`、`evidence presentation pattern` 把通用 SLR meta 分类当成原文编码树，而不是原文实际 extraction form 字段 | **重写 §2**：将六类 pattern 替换为本文的七大分支（bibliographic / review type / scope / topic / empirical coverage / quality / citation impact）的 per-branch pattern 摘要 | C |
| C-02 | §5 "A1-M0--M6 脚手架元维度贡献" 表将 A1-M0--M6 六叶作为外部投影覆盖在原文上，导致 review.md 有两条互相竞争的"树"描述。A1-M0--M6 跨论文投影应降级为**附录性参考**，不应与 §维度树复原 并列作为树的定义 | **移除 §5 或将其降级为附录 footnote**：在显眼位置声明 A1-M0--M6 是跨论文投影而非本文维度树 | C |
| C-03 | 当前 "维度树复原" 一节虽然承认了修复目标（C13: "19×3 全文审计表明本文必须以'原文 schema 主树'作为维度树事实源"），但其中的叶子节点标识如 `leaf-re-tertiary-study-2014-corpus`（语料收集与纳排）、`leaf-re-tertiary-study-2014-taxonomy`（主题与维度分类）等仍带有六叶残余语义 | **重写维度树**：用本审计 §3 的原生树替换现有维度树；叶子标识使用 paper-native 字段名（如 `leaf-re-tertiary-study-2014-qa-inclusion-exclusion` 而非 `leaf-re-tertiary-study-2014-corpus`） | C |

### I 级（Important——影响证据可审计性或统计可用性）

| 编号 | 问题 | 建议 | 严重性 |
|---|---|---|---|
| I-01 | 叶子维度表（review.md 中的大表）使用 `leaf_definition` 作为叶子类型，但 7 个叶子中有 6 个是 "来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构" 的笼统描述，缺少原文 extraction form 字段的精确对应 | **用本审计 §4 的叶子维度表替换**，确保每个叶子有明确的原文字段来源和取值空间 | I |
| I-02 | A.2 证据账本中的 `leaf-re-tertiary-study-2014-corpus`、`leaf-re-tertiary-study-2014-taxonomy` 等叶子标识使用了 "语料收集与纳排""主题与维度分类" 等六叶汉语标签，不是原文字段名 | **重做 A.2 证据账本**：证据标识应映射到本审计 §3 的原生叶子（如 `qa_inclusion_exclusion`），证据锚点应引用 EV-001 -- EV-010 | I |
| I-03 | review.md §1 快速结论卡片中 "A1 角色" 和 "schema 历史观察" 字段缺少对 "原生树类型=单树" 和 "样本单位=individual SLR" 的显式说明 | **补充**：在结论卡片中增加 `样本单位`、`样本数量`、`原生树类型`、`主统计池资格` 行 | I |
| I-04 | 当前 review.md 中 SUMMARY 相关的提到 "全部仍为 schema_seed，不得进入当前 SUMMARY 定量统计"（C13），但本审计发现本文**有充分证据进入主统计池**——53 个样本有明确的 per-unit 编码和取值空间 | **升级统计池资格**：在 SUMMARY 中将本文标注为 "统计池就绪"，字段取值空间大部分已知，仅 topic_group 和 gs_citation_count 的 per-unit 值需要 A2a 补全 | I |

### M 级（Moderate——改善可读性或长期可维护性）

| 编号 | 问题 | 建议 | 严重性 |
|---|---|---|---|
| M-01 | review.md §4 "待复核" 中 "PDF 表格与质量评价细节待人工核对" 未指定具体哪些表/图/数字需要核对 | **细化**：列明 Table I--VI + Figure 1--4 的待核对项（参见本审计 §1.2） | M |
| M-02 | review.md 未区分 "关系边" 概念，缺少关系边表 | **新增关系边表**：可基于本审计 §5 的关系边表 | M |
| M-03 | §3 "对 PR-A1 schema 的启发" 中的 `target_se_subfield`、`publication_count` vs `distinct_study_count`、`education_practice_relevance` 启示有价值但混在 review 正文中 | **保留但移入独立小节** "对 Paper2 schema 的跨论文迁移建议"，与原生维度树清晰分开 | M |
| M-04 | EmpiRE 是 workshop 但 review.md 未充分讨论 workshop paper 对证据强度的限制 | **补充 workshop 降级说明**：短 workshop paper 的 extraction form 可能不如完整期刊论文详实，quality assessment 细节（per-SLR QA 分项值）可能未完整发表于本文中 | M |

### 7.1 关于 GUIDE 规则的 C/I/M 反馈

本审计过程中未发现当前 PR body / GUIDE 规则本身的实质性问题。本审计依据的 A1-DT v2 口径（§2 口径定义）明确且可执行。

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | Abstract (Page 2) | 摘要段 | "identified 53 distinct systematic reviews published from 2006 to 2014 and reported in 64 publications" | 样本总量声明 | strong | 所有叶子 | 否（数字明确） | 无 |
| EV-002 | paper_content.txt | §II.A Planning (Page 3) | 三个 RQ 的显式列表 | "RQ1: What are the main areas... RQ2: What is the quality... RQ3: What are the gaps..." | RQ 驱动字段设计的意图证据 | strong | 关系边 RE-01, RE-02, RE-03 | 否 | 无 |
| EV-003 | paper_content.txt | §II.A Planning (Page 3) | Table I | QA1 Inclusion/Exclusion Criteria, QA2 Search Space Adequacy, QA3 Quality Assessment of Primary Studies, QA4 Information regarding Primary Studies；每项 Yes=1/Partial=0.5/No=0 | B6 quality assessment 的取值空间与评分规则定义 | strong | L6.1--L6.5 | **是**——Table I 的行列对应需 PDF 核对 | 通用 QA rubric，独立于 SE 子领域 |
| EV-004 | paper_content.txt | §II.A Planning (Page 3--4) | "we extracted publication details showing characteristics of the included SLR (i.e. title, authors, year of publication, type of publication, conference/journal name and complete reference, and number of citations to that paper) and information required to answer our three RQs (i.e. number of primary studies, focus of SLR)" | extraction form 的完整字段列表 | strong | B1 Bibliographic, B5 Empirical Coverage, B7 Citation Impact | 否 | 无 |
| EV-005 | paper_content.txt | §II.A Planning (Page 4) | "grouping of main topics ... was done by applying thematic analysis [12] of the titles and abstracts" | B4 Topic Classification 的分组方法 | strong | L4.1, L4.2 | 否 | thematic analysis 是常见方法，但具体分组结果不可迁移 |
| EV-006 | paper_content.txt | §II.B Execution (Page 4) | Table II | primary searches 267→91→58（去重后），secondary searches +6，最终 64 publications / 53 studies | 搜索执行与选择过程的量化摘要 | strong | 样本库完整性证明 | 否 | 无 |
| EV-007 | paper_content.txt | §III RQ1 (Page 4--5) | Table IV | Scope classification: state of the art(33), methods(7), techniques(7), tools(4), frameworks(1), technology(1) | B3 Scope Classification 的取值全集与分布 | strong | L3.1 | **是**——Table IV 的 S-ID 列表需 PDF 核对完整性 | scope classification 的具体分类标准可能不适合所有 SE 子领域 |
| EV-008 | paper_content.txt | §III RQ1 (Page 5--6) | Table V | 主题分组 + S-ID + per-SLR primary study count + year | B4 Topic + B5 num_primary_studies per-unit 值 | strong | L4.1, L4.2, L5.1 | **是**——Table V 是大表，OCR 可能有个别数字或 S-ID 误识别 | topic grouping 不可迁移；num_primary_studies 可迁移 |
| EV-009 | paper_content.txt | §III RQ2 (Page 6) | Figure 2, Figure 3, Figure 4 + 文字描述 | "42 studies out of 51 have scored 2 or above out of 4" + "over half of the SLR have ignored to assess the quality of the included primary studies (QA3)" + "average quality of the published SLR has decreased starting from [2009]" | B6 quality assessment 的分布与趋势统计 | strong | L6.1--L6.5 | **是**——Figure 2/3/4 的精确数据点需 PDF 核对 | quality trend 是 RE 领域特定时间段的观察 |
| EV-010 | paper_content.txt | §III RQ3 (Page 6--7) | 三类 gap 的完整阐述段落 | anomalies (S1:8 vs S4:240)、lack of primary studies (<10)、ignored RE areas（goal-oriented RE, RE in law, requirements modeling notations, conflict resolution, requirements negotiation） | RQ3 cross-unit synthesis 的证据 | strong | 关系边 RE-03, RE-06, RE-08 | 否（文本证据明确） | 具体 gap 内容不可迁移；gap-finding 方法学可迁移 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CL-01 | 本文使用 7 分支 extraction form 编码 53 篇 RE SLR | 原生树复原 | dim-re-tertiary-study-2014-root | EV-001, EV-003, EV-004, EV-007, EV-008 | strong | Paper2 extraction form 骨架设计 | topic taxonomy 不可迁移 |
| CL-02 | 样本单位为 individual SLR，N=53，来自 2006--2014 | 样本单位定义 | dim-re-tertiary-study-2014-root | EV-001, EV-006 | strong | Paper2 统计池设计 | 领域和时间窗口特定 |
| CL-03 | QA rubric（QA1--QA4）可作为 Paper2 的 SLR 质量评估标准 | 方法学迁移 | L6.1--L6.5 | EV-003 | strong | Paper2 质量评估维度 | 评分阈值可能需要针对新领域调整 |
| CL-04 | Cross-study anomaly detection（同一主题不同 SLR 的 primary study 数量矛盾）揭示方法学不一致 | 候选 finding | 关系边 RE-06 | EV-010 | medium | Paper2 的 cross-SLR 验证方法 | 需要 >=2 篇 SLR 覆盖同一子主题才能触发 |
| CL-05 | RE SLR 质量自 2009 年以来下降 + 过半 SLR 忽略 primary study quality assessment | 统计发现 | L6.3, L6.4, L6.5 | EV-009 | strong（针对 RE 领域） | 作为 tertiary study finding 模式的参考 | 不可迁移到 Paper2 目标领域的具体数值 |
| CL-06 | 对照领域 roadmap 找 SLR coverage gap 是有效的 tertiary study 分析方法 | 方法学启发 | 关系边 RE-08 | EV-010 | strong | Paper2 gap analysis 方法 | 需要目标领域有可对照的 roadmap 或 expert review |
| CL-07 | Tertiary study 应产出 replication recommendation | 方法论规范 | CF-05 | EV-010 | medium | Paper2 recommendation 部分 | 需要在 SLR 数据充足时才能做 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取技能文件与采用原则

| 技能文件 | 采用原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | §Core Mandate（claim-evidence-engineering workflow）、§Non-Negotiable Gates（evidence gate、citation gate）、§Evidence Policy（exact numbers from source tables） |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | §Core Reviewer Questions（what problem, approach, experiments support, significance）、§Common Reviewer Concerns（claims exceeding evidence、missing limitations）、§Constructive Specificity Standard |
| `ai-research-writing-skill/references/reviewer-self-review.md` | §Five-Dimension Review（contribution, writing, experiments, evaluation, method soundness, responsibility）、§Claim Audit（each claim needs evidence/citation/risk/revision）、§Rejection-Risk Audit |
| `research-planning/SKILL.md` | §Research context understanding（identify core research question and significance）、§Risk flagging（explicit ambiguities） |
| `research-planning/references/planning-prompts.md` | §AI-Researcher Plan Agent 的 dataset/model/training/testing plan 分解方法（类比应用于 SLR 的 extraction form 分解） |
| `research-planning/references/output-schemas.md` | §Complete Research Plan Schema 的 structured output 规范（类比应用于维度树的层次化结构描述） |
| `autoresearch/SKILL.md` | §Completion artifact contract——artifact must exist and record passing validator result；应用于本审计的 self-review gate |

### 9.2 本输出最高风险 3 点

| 风险 | 说明 | 主线程合并时复核方式 |
|---|---|---|
| **R1：叶子维度表中 Table V 的 topic_group 取值全集未完整还原** | Table V 在 paper_content.txt 中约有 15 个分组，但 OCR 可能遗漏部分行或 mis-parse S-ID 列表。A2a 需要用 PDF 视觉方式逐行核对 Table V，确认 topic_group 的完整取值空间和每个 group 下的 S-ID 列表 | 合并时检查 A2a 的 PDF 核对结果是否与本文 §4 的 L4.1 取值空间一致，若不完整则补充 |
| **R2：现有 review.md 的 A.2/A.3 有大量六叶残留需要替换，可能产生合并冲突** | 现有 review.md 的 A.2 证据账本中约 12 条结论行使用了六叶标签（corpus/taxonomy/method/evidence/finding），而本审计的 A.2 使用了 EV-001--010 和原生叶子标识。合并时需决定：是用本审计的 A.2 完全替换旧版，还是保留旧版作为历史记录并以新版为主事实源 | 合并前 diff 对比两版 A.2，明确删除旧版六叶标签行；保留旧版中价值独立的 C12/C13 审计修复记录作为历史 footnote |
| **R3：未做 PDF 版面核验，Table I--VI 和 Figure 1--4 的像素级精度未确认** | 本审计完全基于 paper_content.txt 文本提取。对于质量评估（Table I 的评分细则）、搜索执行（Table II 的合计数字）、主题分类（Table V 的大表行列对应）、引用统计（Table VI 的 citation count）、图形（Figure 1--4 的精确 x/y 数据点），OCR 提取可能引入误识别 | A2a 精核时必须打开 paper.pdf 逐表核对至少：Table I 的行列对应、Table II 的合计、Table V 的每个 S-ID 行、Table VI 的 citation count、Figure 4 的 annual quality trend 是否与文字描述一致 |

### 9.3 Blocked / Timeout / 文件缺失记录

- **无 blocked**：所有必读文件均可访问且完整读取
- **无 timeout**：本任务在单轮内完成
- **无文件缺失**：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md` 均存在且内容完整
- **未读取 `paper.pdf`**：属于本审计的设计选择（基于 text），不是 blocked；已在 §1.2 和 §9.2 R3 中明确标注需要 A2a 做 PDF 视觉核验

---

**审计完成时间**：2026-06-30（基于 `current_date` 上下文）
**审计 agent**：`deepseek`（Codex CLI attached tmux runtime）
**可迁移到 review.md 的最小交付物**：§0（审计结论卡片，含样本单位 / 主统计池资格）、§3（原生维度树）、§4（叶子维度表）、§5（关系边表）、§8（A.2/A.3 草案）