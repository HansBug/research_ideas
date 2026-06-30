# re-tertiary-study-2014 · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：是。读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`；时间预算所限未逐行展开 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`，但在判定 C/I/M、claim-evidence gate、reviewer 风险叙述时按 SKILL.md 中的 evidence gate / claim gate / reviewer gate 口径执行。
- 是否读取 `$research-planning`：是（按 SKILL 体系把本次审计当作单篇 task packet，参考 planning-prompts 中“以输入证据反推 schema 完整度”这一启发，但本次只输出 review，不写 plan）。
- 是否读取 `$oh-my-codex:autoresearch`：是（已知其强调“先证据后断言、再 fan-out 验证”的口径，本次审计沿用该原则，未启动子代理 fan-out）。
- 是否完整阅读 `paper_content.txt`：是。从 Page 1 IEEE 版权页一直到 Page 9 Appendix A 全文逐行核读，重点覆盖摘要、I. Introduction、II.A Planning（含 RQ1–RQ3、Table I QA1–QA4）、II.B Execution（含 Table II 搜索-筛选汇总）、III. Results & Discussion（含 Table III–VI、Figures 1–4 与 RQ1/RQ2/RQ3 三段叙事）、IV. Limitations、V. Conclusion 与 Appendix A 引用清单。
- 是否核对 `paper.pdf`：否。`paper_content.txt` 已含完整页码标记 `--- Page N ---`，本次审计在文本级即可定位关键 schema；Figure 1/2/3/4 与 Table I/II/V 的版面级（如柱图刻度、平均分变化趋势的具体数值）核验仍留给 A2a 在 PDF 上做。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明（Page 2--3）

原文明确三个 RQ：
- RQ1：哪些 RE 主题被已发表 SLR 覆盖（topic coverage）。
- RQ2：已发表 SLR 的质量如何（quality assessment）。
- RQ3：RE 主题在 SLR 中的覆盖缺口（gap analysis）。

贡献声明：第一个面向 RE 子领域的 tertiary study，识别 2006–2014 年间 53 个 distinct SLR / 64 篇 publication；作者把本研究定位为更大的“updated RE roadmap”计划的第一步（Page 2 末段 + Page 7 末段 + Page 8 conclusion）。

### 2.2 方法流程（Page 3--4）

方法严格遵循 Kitchenham/EBSE 三阶段：planning / execution / reporting。可被结构化的字段包括：

1. **Protocol 字段**：search strategy、selection process、quality assessment、data extraction、data synthesis、data analysis（Page 3 II.A 首段显式列出）。
2. **Search string 结构**：`(RE 同义词簇 AND review 同义词簇)`；RE 簇 16 词，review 簇 16 词；只在 title 上施加（用于压缩 IEEE / ACM / ScienceDirect / Google Scholar / EI Compendex 五库 noise）。
3. **Search 阶段分层**：primary automated search（5 库）+ secondary search（snowball 自 4 篇 tertiary studies + 手工浏览 RE / EASE / ESEM / REFSQ / REJ / ESE / IST 自 2004 起的 proceedings）。
4. **纳排条件**：仅 3 条 study selection criteria —— 英文 / SLR-or-SMS-or-meta-analysis / focus on RE area。
5. **去重 + 分组规则**：多 publication 同一 study 用同一 study ID + 后缀 A/B/C 分组（Page 4 “We assigned them IDs based on the study so that multiple publications from the same study are grouped under the same ID with suffix A, B and C”）。
6. **抽取字段**：基于 [12] 给出 publication 细节（title / authors / year / publication type / venue / 完整 reference / citation count）+ RQ 维度（number of primary studies、focus of SLR）。
7. **主题分组**：thematic analysis 应用于 title + abstract（Page 4 II.A 末段），Table V 第一列即“Grouping of main topics of SLR”。
8. **统计基准日期**：citation count cut-off = 19 May 2014（Page 3 末段，可审计的明确时间戳）。

### 2.3 原文显式 extraction form / classification schema / coding scheme

本文是一篇 schema 异常密集的 short workshop tertiary study，原文显式提供至少 6 套受控枚举：

1. **SLR 类型枚举（Page 2 末 / Page 4 第二段）**：Conventional SLR / Systematic Mapping Study / Tertiary study（+ Meta-Analysis 作为统计特例）。Page 4 Results 给出对应分布：53 中 12 SMS、1 Meta-Analysis、其余 SLR。
2. **Quality Assessment rubric（Table I, Page 3）**：QA1–QA4 四个问题，每题三级编码 Yes=1 / Partial=0.5 / No=0；rubric 沿用 CRD/DARE，via tertiary studies [8,9,11]。这是原文最具迁移价值的、可直接编码的 schema seed。
   - QA1: Inclusion / Exclusion Criteria（Explicit / Implicit / None）
   - QA2: Search Space Adequacy（≥4 库+额外策略 / 3–4 库无额外 / ≤2 库或非常受限）
   - QA3: Quality Assessment of Primary Studies（显式描述并应用 / 隐式 / 无）
   - QA4: Information regarding Primary Studies（完整信息 / 摘要 / 未说明）
3. **Publication Type 枚举（Table III, Page 4）**：Conference 31 / Journal 16 / Workshop 4 / Technical Report 4 / Theses 8 / Unknown 1 —— 共 6 类、明确分母 64。
4. **Scope 枚举（Table IV, Page 5）**：State of the art 33 / Methods 7 / Techniques 7 / Tools 4 / Frameworks 1 / Technology 1 —— 共 6 类、明确分母 53。
5. **Topic 分组（Table V, Page 5）**：thematic analysis 产出的 24 个主题分组（Non Functional Req / Complete RE Process / Model Driven Development / Knowledge Management and RE / RE in GSD / RE in SPL / Requirements Management / Multi Agent / Requirements Reuse / Value-based RE / VR Systems / Web Engineering / Creativity in RE / Requirements Elicitation / Stakeholders and Users / Requirements Prioritization / Meta Modelling / Software Requirements Specifications / Requirements Verification/Validation/Evaluation / Requirements Traceability / Requirements Change Management / RE Education / Mobile Learning / Checklist for RE），每行带 S-ID / focus 描述 / # of PS / year，是 RQ1 / RQ3 主统计载体。
6. **Gap 三型（Page 6--7 RQ3）**：①Anomalies（不同 SLR 在同一主题报告的 PS 数量冲突）；②Lack of primary studies（某主题 PS 数量过低，存在“neglected area”和“SLR 搜全率不足”两种解释）；③Ignored RE areas（与 Nuseibeh-Easterbrook 2000 [1] / Cheng-Atlee 2007 [2] 两份 RE roadmap 对照，identify 已覆盖 vs 未覆盖的 hotspot）。

### 2.4 图表与统计载体（Page 4--6）

| 图/表 | 内容 | 统计用途 |
|---|---|---|
| Table I | QA rubric 三级编码 | 质量评分基准 |
| Table II | 5 库命中数与 included 数、secondary search 命中数 | 描述检索 funnel：267→91→58→64 篇 / 53 study |
| Table III | publication type 分布 | RQ1 辅助 |
| Table IV | scope of SLR 分布 | RQ1 |
| Table V | 24 主题 × S-ID × #PS × year | RQ1 + RQ3 主载体 |
| Table VI | Top 10 highly cited SLR（S-ID / GS citation / pub channel / QA score） | 影响 + 质量交叉 |
| Figure 1 | SLR 年度分布 2006–2014 | RQ1 时间趋势 |
| Figure 2 | QA 总分（0–4）分布 | RQ2 |
| Figure 3 | QA1–QA4 每项 Yes/Partial/No 计数 | RQ2 细分 |
| Figure 4 | 每年平均 QA 分数 | RQ2 时间趋势 + 核心 finding（2009 后质量下降） |
| Appendix A | 64 个 publication 的完整 BibTeX-like 引用 + GS citation | 复现 / 工业影响代理 |

### 2.5 Finding 形成方式

paper 的 finding 链路非常清晰：

1. **统计观察 → 候选 finding**：例如 Table V 中 S1=8 vs S4=240（同主题 Requirements Prioritization）→ 直接断言“anomaly raises concerns on validity of SLR process”；Figure 4 平均分 2009 年后下降 → 直接断言 “the quality of SLR in RE has been decreasing over the recent years”（与 Abstract 完全一致）；Figure 3 显示半数研究忽视 QA3 / QA4 → 直接断言 “almost half of the selected SLR have ignored to evaluate the quality of the primary studies included in their reviews”（Page 8 conclusion 复述）。
2. **roadmap 对照 → gap finding**：把 Table V 主题集合与两份 RE roadmap 的 hotspot 集合做差，得到 “covered: Security Req / RE education / Req Reuse / Global & Distributed RE”、“not covered: Req Scaling / RE for self-management / system environment effects / RE research effectiveness in practice / conflict resolution / requirements negotiation / goal-oriented RE / RE in law / req modeling notations”。
3. **限制声明 → 候选 finding 降级**：作者明确承认 RQ3 gap 列表非穷尽、RQ1 主题分组主观（first author 命名，其余作者复核），并把这些写入 Section IV Limitations。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 不准确 | 当前根节点直接写为论文题名 “Systematic Reviews in Requirements Engineering”，但原文的根问题是 “针对 RE 子领域 SLR 的 tertiary characterization (RQ1 主题覆盖 / RQ2 质量 / RQ3 缺口)”；3 个 RQ 应成为根下直接主干，而不是被压缩进 b1。 | I |
| 主干分支是否覆盖原文 schema | 严重不足 | 当前 b1–b5 是“范围 / 语料 / 主题 / 方法干预 / 评价”的通用接口；原文 schema 至少包含 7 条互不重叠的可统计维度（SLR 类型 / publication type / scope of SLR / topic group / # of primary studies / QA1–QA4 rubric / GS citation + venue / 3 类 gap / roadmap 对照），其中“方法 / 技术 / 干预分类”这条 b4 在 tertiary study 语境下基本不适用，反而把 Table IV scope 与“干预”混为一谈。 | C |
| 叶子维度是否足够具体 | 不足 | 6 个 `leaf-*` 全部是跨论文通用接口（scope / corpus / taxonomy / method / evidence / finding），未对应原文的 QA1–QA4、6 类 publication type、6 类 scope、24 类 topic group、3 类 gap 等具体取值空间；原文模式候选叶子映射只列 4 项（RE topic / secondary study quality / impact / method gap），其中 “impact” 与原文（仅 GS citation count + venue 作代理）覆盖范围严重不匹配，存在概念膨胀。 | C |
| 取值空间是否可执行 | 不可执行 | 候选 4 个叶子的取值空间都是抽象描述（“学术影响、实践影响、工业采用和引用 / follow-up”、“方法报告不足、主题覆盖不足、数据缺失和 validity threat”），无法直接和原文 Table I / Table III / Table IV / Table V 对齐；A2a 会无从下手。 | C |
| 关系边是否缺失 | 缺失关键关系 | 至少 2 条关系边在原文清晰可见但未在树中体现：① “study ↔ publication” 的 1-N 分组（A/B/C 后缀），53 study vs 64 publication 的双分母关系决定了所有 Table 的分母正确性；② “Table V 主题 ↔ 两份 RE roadmap hotspot” 的对照关系，是 RQ3 形成 gap finding 的核心边。 | I |
| 统计用途 / 分母是否正确 | 部分不一致 | A.2 统计与候选发现链路把分母统一写为 “当前 19 篇 survey-of-surveys 样本”，但原文的真分母明确是 53（study 级）/ 64（publication 级）/ 51（去掉 S3、S8 后可评分 SLR）/ 24（topic groups），叶子层未保留这些分母会让 A2a 在统计合成时丢失关键计数语义。 | I |
| 候选 finding 路径是否完整 | 残缺 | 原文已经给出 3 条强 finding（quality 自 2009 年起下降 / 半数 SLR 忽视 QA3+QA4 / 同主题 SLR PS 数严重冲突 + 总-子关系倒置）+ 1 条 gap finding（与 2000/2007 roadmap 对照得出 4 个已覆盖 hotspot + 9 个未覆盖 hotspot），当前 leaf-finding 只写 “候选发现台账”、且 EV-003 全部标 `not_verified`，导致这些可文本核验的 finding 无路径进入 A2a 候选池。 | I |
| A.1--A.4 证据链是否足够 | 不足 | A.2 4 条证据 (EV-001..004) 的页码字段全部写 “待 A2a 精确页码复核”，但 `paper_content.txt` 已有 `--- Page N ---` 标记，可以直接给出 Page 2 / Page 3 / Page 3 Table I / Page 4 Table II / Page 5 Table IV–V / Page 6 Table VI + Figures 2-4 / Page 6–7 RQ3 / Page 7 Limitations 等文本级页码；EV-002 / EV-003 一刀切 `not_verified` 是过度保守，造成 A.3 全部结论强度 `weak` + schema_seed。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在 | “原文模式候选叶子映射” 把 “impact 字段” 取值空间写为 “学术影响、实践影响、工业采用和引用 / follow-up”，但原文仅以 “GS citation count（截至 19 May 2014）+ pub channel” 操作化 impact，并未涵盖工业采用 / follow-up；若 A2a 据此扩字段集会引入原文无法支撑的统计列。另一个潜在误导是把整篇 paper 的 evidence 全部降为 `not_verified` / `schema_seed`，会让下游误以为本文证据等级与纯 roadmap / vision 论文相当，事实上这是一篇有完整搜索 funnel + QA rubric + Table V 主题表的系统性 tertiary study。 | I |

## 4. 建议维度树骨架

下面给出本 reviewer 认为更忠实于原文的最小可执行骨架。它只在结构上对齐原文 Table I / III / IV / V / VI、Figure 1–4 与三类 gap，避免把跨论文通用接口当成原文 schema。

```text
[dim-re-tertiary-study-2014-root] RE 子领域 SLR 的 tertiary characterization (RQ1 topic / RQ2 quality / RQ3 gap)
├── [dim-b-protocol] 方法 / Protocol（EBSE 三阶段：planning / execution / reporting）
│   ├── [leaf-search-string] 检索串结构（RE 簇 16 词 × review 簇 16 词，仅 title 施加）
│   ├── [leaf-source] 主检索来源（IEEE / ACM / ScienceDirect / Google Scholar / EI Compendex；分母 = 267→91→58）
│   ├── [leaf-secondary-search] 二次检索（4 篇 tertiary 的 snowball + RE/EASE/ESEM/REFSQ/REJ/ESE/IST 自 2004 起手工浏览；新增 6 → 64 篇）
│   ├── [leaf-selection-criteria] 三条纳排（英文 / SLR-SMS-meta / focus on RE）
│   └── [leaf-study-publication-grouping] study↔publication 1-N 分组规则（A/B/C 后缀；53 study vs 64 publication）
├── [dim-b-typology] SLR 类型枚举
│   └── [leaf-slr-type] Conventional SLR / Systematic Mapping Study / Tertiary / Meta-Analysis（实际分布：SMS=12、Meta=1、其余 SLR；分母 53）
├── [dim-b-publication] 出版与影响特征
│   ├── [leaf-publication-type] {Conference, Journal, Workshop, Tech Report, Theses, Unknown}（Table III, 分母 64）
│   ├── [leaf-year] 年份 2006–2014（Figure 1）
│   ├── [leaf-citation-count] Google Scholar citation（cut-off 2014-05-19）
│   └── [leaf-pub-channel] venue（与 citation 在 Table VI 交叉）
├── [dim-b-scope] SLR 的研究对象 scope
│   └── [leaf-scope-class] {State of the art, Methods, Techniques, Tools, Frameworks, Technology}（Table IV, 分母 53）
├── [dim-b-topic] RE 主题分组（RQ1 核心）
│   ├── [leaf-topic-group] 24 类 thematic group（Table V 第一列）
│   ├── [leaf-topic-focus] 每篇在主题内的 focus 描述（Table V 第三列）
│   └── [leaf-primary-study-count] # of PS（数值，含 NF/NM；统计用途：极值、分布、与同主题 SLR 冲突检验）
├── [dim-b-quality] SLR 质量评估（RQ2 核心，源自 DARE/CRD）
│   ├── [leaf-qa1] Inclusion/Exclusion criteria {Yes=1, Partial=0.5, No=0}
│   ├── [leaf-qa2] Search Space Adequacy {≥4 库+额外, 3–4 库, ≤2 库}
│   ├── [leaf-qa3] QA of Primary Studies {Explicit, Implicit, None}
│   ├── [leaf-qa4] Information on Primary Studies {Complete, Summary, Not specified}
│   └── [leaf-qa-total] 0–4 分总分（51 个可评分 study；42/51 ≥ 2；Figure 2 / 4）
├── [dim-b-gap] RQ3 三类 gap
│   ├── [leaf-gap-anomaly] 同主题 PS 数量冲突（例 S1=8 vs S4=240）
│   ├── [leaf-gap-low-ps] PS 数过低（例 S14=8, S27=5）
│   └── [leaf-gap-uncovered] 与 RE roadmap [1,2] 对照得出的未覆盖 hotspot
└── [dim-b-roadmap-crossref] RE roadmap 对照（Nuseibeh-Easterbrook 2000、Cheng-Atlee 2007）
    ├── [leaf-covered-hotspot] {Security Req, RE education, Req Reuse, Global & Distributed RE}
    └── [leaf-uncovered-hotspot] {Req Scaling, RE for self-mgmt, env effects, practice effectiveness, conflict resolution, requirements negotiation, goal-oriented RE, RE in law, req modeling notations}

[edge-study-to-publication] study --N→1 publication 分组（53→64）
[edge-topic-to-roadmap] Table V 主题集合 ↔ roadmap hotspot 集合（差集 = uncovered gap）
[edge-quality-vs-year] QA 总分 ↔ 发表年（Figure 4：2009 后均分下降）
```

每个叶子的最低证据位置（文本级，可直接核验，无需 PDF 版面）：

| 叶子 | 取值空间是否可统计 | 缺失值语义 | 文本级证据来源 |
|---|---|---|---|
| leaf-search-string | 否（结构性） | -- | Page 3 II.A 中段“((requirements engineering OR ...) AND (review of studies OR ...))” |
| leaf-source | 是（5 库；分母 267→91） | not_reported 不适用 | Page 3 末段 + Page 4 Table II |
| leaf-secondary-search | 是（6 新增） | -- | Page 4 II.B + Table II |
| leaf-selection-criteria | 否（结构性） | -- | Page 3 末段 1./2./3. |
| leaf-study-publication-grouping | 是（53 vs 64；A/B/C） | -- | Page 4 II.B 首段 |
| leaf-slr-type | 是（SMS=12, Meta=1, SLR=40） | -- | Page 4 III 首段 |
| leaf-publication-type | 是（分母 64） | Unknown=S40 | Page 4 Table III |
| leaf-year | 是（2006–2014） | -- | Page 4 III 首段 + Figure 1 |
| leaf-citation-count | 是（数值，cut-off 2014-05-19） | 0 / 不可得 | Page 3 末段 + Table VI + Appendix A |
| leaf-pub-channel | 是 | -- | Table VI / Appendix A |
| leaf-scope-class | 是（分母 53） | -- | Page 5 Table IV |
| leaf-topic-group | 是（24 类） | -- | Page 5 Table V 第一列 |
| leaf-topic-focus | 否（自由文本） | -- | Table V 第三列 |
| leaf-primary-study-count | 是（数值） | NM / NF | Table V 第四列 |
| leaf-qa1 / qa2 / qa3 / qa4 | 是（3 级编码） | S3、S8 未评分（51 分母） | Table I + Page 6 III RQ2 + Figure 3 |
| leaf-qa-total | 是（0–4 分） | -- | Figure 2 + Figure 4 + Page 6 |
| leaf-gap-anomaly / -low-ps / -uncovered | 是（候选 finding 计数） | -- | Page 6–7 RQ3 三小节 |
| leaf-covered/uncovered-hotspot | 是（受控枚举） | -- | Page 7 RQ3 第三小节 |

当前 review.md 的 6 个通用 `leaf-*` 与 4 个候选叶子并不能替代以上结构，且取值空间不可执行。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 重构根节点表述与主干分支 | 维度树结构 + “根问题 / RQ 到主干分支映射” | 把根改为 “RE 子领域 SLR 的 tertiary characterization (RQ1/RQ2/RQ3)”；主干至少展开为 protocol / typology / publication / scope / topic / quality / gap / roadmap-crossref 八支，而非通用 b1–b5 五支。 | Page 2 RQ1–RQ3、Page 3 II.A、Page 4 II.B、Tables I/III/IV/V、Page 6–7 RQ3、Page 8 Conclusion | C |
| 补齐 QA1–QA4 + qa-total 五叶子并冻结取值空间 | 叶子维度表 + 原文模式候选叶子映射 | 新增 5 个 leaf 节点，取值空间分别为 Table I 的三级编码与 0–4 总分；分母 51（去 S3/S8）；明确缺失值语义。 | Table I (Page 3) + Page 6 Figures 2–3 + Section IV Limitations | C |
| 补齐 publication type / scope / topic group / primary study count 四叶子 | 叶子维度表 | 新增 4 个 leaf，取值空间分别为 6 / 6 / 24 / 数值，分母 64 / 53 / 53 / 53；标注 NM / NF / Unknown 的缺失语义。 | Tables III–V (Page 4–5) | C |
| 移除或重命名 “方法 / 技术 / 干预分类” 叶子 | 叶子维度表 b4 | 在 tertiary study 场景中 “方法 / 技术 / 干预” 不适用；建议或者把 b4 改为 “scope of SLR (Table IV)”，或者明确写 not_applicable + 说明。 | Table IV (Page 5) | I |
| 缩窄 “impact” 候选叶子的取值空间 | 原文模式候选叶子映射第 3 行 | 改为 `GS citation count (cut-off 2014-05-19) + publication venue`；删除 “工业采用”“follow-up” 等原文未操作化的项，避免 A2a 越界扩字段。 | Page 3 末段 + Table VI + Appendix A | I |
| 补 gap 三类与 roadmap 对照分支 | 维度树结构 + 关系边 | 新增 `[dim-b-gap]` 三个叶子（anomaly / low-ps / uncovered）与 `[dim-b-roadmap-crossref]` 两个叶子（covered / uncovered hotspot），并加 `[edge-topic-to-roadmap]` 关系边。 | Page 6–7 RQ3 三小节、Page 7 末段对 [1][2] 的对照 | C |
| 补 “study ↔ publication 1-N” 关系边与双分母 | 关系边 + 统计用途 | 显式记录 53 study / 64 publication 的双分母，并在所有相关叶子统计用途字段标注本叶子对应哪一个分母（如 publication type 用 64、scope/topic 用 53、QA 用 51）。 | Page 4 II.B 首段 + Tables II–V | I |
| 把 EV-001–004 的页码从 “待 A2a” 升级为文本级页码 | A.2 维度树证据账本 | 至少补到段落级，例如 EV-002 → Page 3 Table I / Page 4 Table II / Page 4–5 Tables III–V；EV-003 → Page 6 Figures 2–4 / Page 6–7 RQ3 / Page 8 Conclusion；EV-004 → Page 7 Section IV Limitations；保留对图形像素级的 PDF 核验留给 A2a，但文本可定位的事实不应统一 `not_verified`。 | `paper_content.txt` 显式 `--- Page N ---` 标记 | I |
| 把 3 条明确的统计 finding 列为 candidate finding | A.3 结论-证据映射 | 新增 3 条 `[clm-*-finding]`：①“RE SLR 平均 QA 分自 2009 起下降”、②“≈50% SLR 忽视 QA3+QA4”、③“同主题 SLR PS 数严重冲突 + 子集合 PS 数大于全局 state-of-the-art SLR（S24=242）的反常现象”。三条均允许写 `candidate_finding`（不是 final finding），并保留 Section IV Limitations 的反证字段。 | Page 6 RQ2、Page 6–7 RQ3、Page 8 Conclusion；反证为 Page 7 Section IV | I |
| 修正 Figure 1 / 时间维度遗漏 | 维度树结构 | 新增 `leaf-year` 叶子并把 Figure 1 / Figure 4 同时挂上 `[edge-quality-vs-year]` 关系边。 | Page 4 III 首段 + Figure 1 + Figure 4 | M |
| 标注 citation cut-off 时间戳 + DARE/CRD provenance | 叶子维度表 leaf-citation-count + leaf-qa* | 在 “证据要求 / 缺失值语义” 字段显式记录 “GS citation 截取于 2014-05-19”、“QA rubric 源自 CRD/DARE，via tertiary studies [8,9,11]”。 | Page 3 II.A 第 4–5 段 | M |
| metadata.json 与 review.md 一致性 | metadata.json | `eligible_for_statistical_synthesis=true` 与 review.md 中 “A1-DT 阶段仅作 schema seed、不进 SUMMARY 定量统计” 之间存在张力；建议在 metadata.json 增加 `statistical_pool_exclusion_reason=null` 之外补 `a1dt_phase_note`，明确 “A1-DT 阶段仅作 schema seed；A2a 完成版面核验后可升级为统计池成员” —— 避免 SUMMARY 误把本文计入定量。 | metadata.json + review.md 维度树章节 | M |

## 6. C/I/M 结论

- **C（直接破坏 Paper2 学术目标 / 证据链 / A2a 可靠性）**：
  1. 当前维度树根节点 + 主干分支 + 叶子层均为通用接口，未对应原文显式的 7 套受控枚举与三类 gap，A2a 无法据此完成 schema lock。
  2. 叶子取值空间不可执行；原文已经把 Table I / III / IV / V / VI 写得非常具体，但 review.md 未承接。
  3. RQ3 三类 gap 与 roadmap 对照这一 RQ3 主载体在维度树中完全缺失，会让 A2a 把本文当成无 gap finding 的弱样本。

- **I（实质影响维度树可用性、原文 schema 复原、证据可审计性）**：
  - b4 “方法 / 技术 / 干预分类” 在 tertiary study 语境中误用，需要重命名或显式 not_applicable。
  - “impact” 候选叶子取值空间膨胀到原文未支撑的工业采用 / follow-up，会引入越界字段。
  - EV-001..004 一刀切 `not_verified` 导致 3 条文本级可核验的统计 finding 全部困在 schema_seed，A2a 接管时会失去 candidate finding 路径。
  - “study ↔ publication 1-N” 双分母关系未在维度树中显式化，下游所有统计分母都可能错位。
  - 统计与候选发现链路把分母统一写为 “当前 19 篇 survey-of-surveys 样本”，丢失了原文 53 / 64 / 51 / 24 的真实分母。

- **M（不阻塞的清晰度 / 维护性建议）**：
  - 补 Figure 1 / Figure 4 对应的时间维度叶子与关系边。
  - 在叶子注明 citation cut-off 时间戳与 QA rubric 的 DARE/CRD provenance。
  - metadata.json 与 review.md 在 “是否可进入统计合成池” 上的措辞需要进一步对齐。

- **最终建议：NEEDS FIX**。当前 review.md 通过结构化合同与审计附录的形式上要求，但实质层面没有完成原文 schema 复原，会直接影响 PR2-A1 的 schema seed 质量与 A2a 后续的统计合成可靠性。建议至少完成上表中 5 条 C 修复（根节点重构 + QA 四叶子 + Tables III/IV/V 四叶子 + Gap 三叶子 + Roadmap-crossref 两叶子 + 移除/重命名 b4）后再申请 READY。
