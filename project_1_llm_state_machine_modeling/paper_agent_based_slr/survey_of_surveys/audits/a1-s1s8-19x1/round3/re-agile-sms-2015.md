# A1 survey_of_surveys S1--S8 独立审计：re-agile-sms-2015

> 角色：A1 survey-of-surveys 单篇维度抽取 subagent（未开启 sub-subagent）。
> 范围：只审计 `papers/re-agile-sms-2015/`。
> 重要边界：本文件是 A1 文本级 / 局部 PDF 表格级审计结果，只能作为 `review.md`、`evidence_chain.md`、`SUMMARY.md` 返修输入；**不得写成 Paper2 final quantitative finding**。

## 1. 全文阅读依据

| 材料 | 本轮阅读 / 核验范围 | 用途 | 剩余不足 |
|---|---|---|---|
| `bibtex.bib` | 已读全文；确认题名、作者、SEAA 2015、DOI `10.1109/SEAA.2015.70`。 | 元数据与引用身份核验。 | 未外查 publisher 页面。 |
| `metadata.json` | 已读全文；确认 `review_type=SMS`、`eligible_for_statistical_synthesis=true`、证据角色为 systematic mapping pattern。 | 与本地统计池口径对照。 | CCF 与 venue 字段未外查，本轮不处理。 |
| `paper_content.txt` | 已通读 1--954 行：摘要、引言、背景、方法、结果、讨论、限制、结论、参考文献与 Primary Sources S1--S28。 | 抽取 RQ、检索分母链、S1--S28、Table I--V、B1--B6、P1--P6、solution prose、limitations。 | 文本抽取存在排版断裂；精确页码 / 表格单元仍应由 A2a 建正式证据链。 |
| `paper.pdf` | 已人工查看第 3--7 页截图，核对 Methodology、Table I--V、Discussion / Limitations 的版面存在性与主要数值 / S-id 列表。 | 对表 I--V 做最小视觉核验，尤其是 Table II/III/IV/V 的 S-id 与 N。 | 未逐字核对第 1--9 页全部版面；未与 IEEE publisher final 页面交叉核验。 |
| `review.md` | 已读全文，重点核对“维度树复原”和“survey_of_surveys 自身 schema 抽取”。 | 审计当前 S1--S8 与原生树/森林是否忠实。 | 不修改，只给返修清单。 |
| `evidence_chain.md` | 已读全文 A.1--A.4。 | 审计证据链是否把原文证据、本地复原、三路审计输入分清。 | 当前 A.2/A.3 仍是树级 claim map，尚未逐叶子 / 逐关系边展开。 |

## 2. 原文事实底座

### 2.1 研究任务与语料链

- 原文是 Requirements Engineering in Agile Software Development 的 systematic mapping study；作者明确说明该研究按 mapping study 执行。
- 三个 RQ：RQ1 关注 agile context 中 RE 已被研究了什么；RQ2 关注 agile RE 的 reported benefits；RQ3 关注 agile RE 的 reported problems 及 corresponding solutions。
- 语料链：Scopus；检索时间 2014-09；检索式围绕 `requirements analysis` / `requirements engineering` 与 `agile` / `scrum`，排除 `agile manufacturing`；分母链为 241 → 187 → 65 → 28。
- 最终样本单位是 28 篇 primary sources，原文用 S1--S28 编号。

### 2.2 S1--S28 编号使用情况

原文 Primary Sources 列出 S1--S28；Table II--V 使用这些 S-id 作为字段值或证据集合。当前本轮不逐篇重写每篇 primary source 摘要，但确认这些编号是原文样本 ID，而不是本地审计新造 ID。

### 2.3 原文表格与维度

| 维度簇 | 原文承载 | 本轮审计结论 |
|---|---|---|
| 发表源 / venue | Table I：按 Conference proceedings / Journal / Magazine 汇总 venue 名称与数量。 | Table I 是 formal summary table；但它没有逐 S-id 显示每篇所属 venue，若要写 `S_i -> venue` 关系，应同时回链 Primary Sources 列表，而不能只引用 Table I。 |
| Agile context | Table II：Unspecified agile / Scrum / FDD，并列出 S-id 与 N。 | 这是明确字段级表，可支撑 `S_i -> agile context` 关系。 |
| Article type | Table III：multiple case study、single case study、experience report、tool evaluation、method evaluation、method proposal、position paper，并列出 S-id 与 N。 | 这是明确字段级表，可支撑 `S_i -> article type` 关系。 |
| Benefits | Table IV：B1--B6 benefit code、benefit 名称、articles。 | 这是明确字段级表，可支撑 `benefit -> S-id set`；反向 `S_i -> benefit set` 是本地可机械反转。 |
| Problems | Table V：P1--P6 problem theme、articles。 | 这是明确字段级表，可支撑 `problem -> S-id set`；反向 `S_i -> problem set` 是本地可机械反转。 |
| Problem→solution | §IV.D 每个 problem 小节下的 solution prose；P3/P4/P6 明说没有 solutions。 | **不是原文 formal relation table**。它是本地从作者按 P1--P6 组织的散文段落复原出的关系边；可作为 A1 schema seed，但必须标为 local reconstruction。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 树型判定

本篇应写为“维度森林 + 关系边”，而不是单棵平面字段表。根对象是 28 篇 agile RE primary studies；RQ1/RQ2/RQ3 是字段用途锚点。原文的强证据来自系统检索、Table I--V 与 §IV.D/§V 的主题讨论。

```text
[根] RE in ASD systematic mapping corpus（28 篇 primary studies, S1--S28）
├── [任务锚] RQ1/RQ2/RQ3
│   ├── RQ1：研究图景 / 已研究内容
│   ├── RQ2：reported benefits
│   └── RQ3：reported problems and corresponding solutions
├── [语料链] Scopus search and screening
│   ├── 数据库：Scopus
│   ├── 时间：2014-09
│   ├── 检索式：RE / requirements analysis × agile / scrum，排除 agile manufacturing
│   └── 分母链：241 → 187 → 65 → 28
├── [发表源维度] Table I：venue type + venue name summary
│   ├── Conference proceedings：15
│   ├── Journal：8
│   └── Magazine：5
├── [上下文维度] Table II：agile method context
│   ├── Unspecified agile：20，S-id 列表由原文表给出
│   ├── Scrum：7，S-id 列表由原文表给出
│   └── FDD：1，S-id 列表由原文表给出
├── [文章类型维度] Table III：article type
│   ├── Multiple case study：6
│   ├── Single case study：5
│   ├── Experience report：3
│   ├── Tool evaluation：1
│   ├── Method evaluation：2
│   ├── Method proposal：8
│   └── Position paper：3
├── [收益维度] Table IV：B1--B6 benefit themes
│   └── 每个 B-code 关联一个 S-id 集合
├── [问题维度] Table V：P1--P6 problem themes
│   └── 每个 P-code 关联一个 S-id 集合
└── [关系边：本地复原] problem → proposed solution evidence
    ├── P1：有 solution prose，涉及 S11/S5/S26/S12/S20/S15/S17/S10
    ├── P2：有 solution prose，涉及 S5/S27/S1/S9/S8/S24
    ├── P3：原文明确 no solutions
    ├── P4：原文明确 no solutions
    ├── P5：有 solution prose，涉及 S20
    └── P6：原文明确 no solutions
```

### 3.2 problem→solution 关系的审计裁决

- 可以复原 `P-code -> solution-supporting S-id set / ∅`，因为 §IV.D 按 P1--P6 组织 solution 段，且 P3/P4/P6 对 no solutions 有明确文本证据。
- 但原文没有一张 formal `problem × solution` relation table，也没有把 solution 作为 Table V 的列。因此 `R-solution-of` 只能写成“本地复原关系边 / schema seed”。
- “空集是显式缺口信号”是合理的 A1 方法启发，但不能把 3/6 写成最终跨论文经验比例；它只是在这篇 agile RE SMS 内部成立。

## 4. S1--S8 五分栏证据拆分

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 标题、摘要和引言均表明这是 RE in ASD 的 mapping study；引言给出 3 个 RQ。 | 根对象为 28 篇 RE-in-ASD primary studies；RQ1/RQ2/RQ3 分别锚定研究分布、benefits、problems+solutions。 | 强：可作为 exploratory SMS task-setting 样本；不支撑效果评价或因果 finding。 | 精确页码、RQ 原文 wording、是否存在 publisher final 版本差异。 |
| S2 语料收集与筛选 | Methodology 给出 Scopus、2014-09、检索式、题摘筛选、全文筛选、排除标准与 241→187→65→28 分母链。 | “语料链”是原生树主干之一，字段包括数据库、时间窗、检索式、过滤节点、排除原因、最终分母。 | 强：有系统检索与可复验分母链；但单库 Scopus 与关键词窄化必须随统计一起保留。 | 精确核验检索式脚注、排除标准编号、分母链是否与 PDF / publisher final 完全一致。 |
| S3 原生维度树 / 样本编码对象 | 方法段说明抽取 metadata、context、methods、results，并将 results 归入 definition、benefits、problems、solutions；Table I--V 使用 28 篇 S-id。 | 应复原为维度森林：venue、context、article type、benefit、problem，以及本地复原的 problem→solution 关系边。 | 强：原文有明确样本单位与多组编码维度；但 problem→solution 不是 formal table，必须标为 local reconstruction。 | A2a 应逐项核验 Table I--V 与 §IV.D solution prose；尤其核验 `R-solution-of` 的来源角色。 |
| S4 字段级证据 | Table II/III/IV/V 提供 S-id 级字段；Table I 提供 venue type/name summary；Primary Sources 给每个 S-id 的 venue 线索；§IV.D 给 solution prose。 | 字段可分为：语料字段、venue summary、context、article type、B-code、P-code、problem→solution relation、limitations。 | 中到强：context/type/benefit/problem 字段级较强；venue-to-S 与 solution relation 需要本地复原，故整体不宜写成 final 字段级统计。 | 把 venue relation 的证据从 Table I 扩展到 Primary Sources；把 solution relation 逐条映射到 §IV.D 段落。 |
| S5 维度模式演化 | 原文展示 RQ → 数据抽取 → Table I--V → Discussion / Conclusion 的报告链；benefits、problems、solutions 被作者称为 thematic areas。 | 可复原为“RQ 驱动的主题归类 + 描述统计 + gap finding”演化链；没有详细编码手册、开放编码日志或研究者分歧记录。 | 中：可作为 mapping-study 维度形成模式 seed；不能声称作者提供了完整 coding evolution protocol。 | 核验作者是否在未提取到的附录 / supplementary 中给出编码过程；本地不可脑补 open coding 细节。 |
| S6 统计分析 | 原文给出多个 N/百分比：venue type、agile context、article type、B/P coverage，以及 discussion 中的 empirical part / method proposal 等观察。 | 统计分支是 descriptive mapping，不是效果综合；`P3/P4/P6 no solutions` 可作为本篇内部 gap observation。 | 强（仅限 A1 schema 可用度）：有明确分母和描述统计；**不得升级为 final quantitative finding**，也不得外推到所有 agile RE 研究。 | 对所有百分比、四舍五入、表格对齐与 `17/28≈60%` 重新做 A2a 证据链；标注小样本和单库限制。 |
| S7 候选 finding | 摘要、Discussion、Conclusion 给出定义模糊、无主导 venue、context 未说明、method proposal 缺评估、solutions 集中在 P1/P2/P5、P3/P4/P6 缺 solution 等发现。 | findings 由 field statistics 与 thematic synthesis 形成；可映射到 `definition clarity`、`venue dispersion`、`article type gap`、`problem-solution gap`。 | 强（作为本篇 SMS 内部候选 finding）：可启发 Paper2 finding heuristic；不可迁移 agile RE 领域结论到 STM/LLM 主题。 | 每条 finding 需独立回链到表格或段落；区分作者明说、审计复原和后续方法启发。 |
| S8 研究者 / 作者质疑与裁决 | 原文有 Limitations，主要说明 Scopus 单库和检索词限制；本轮未发现多研究者筛选、编码冲突裁决、一致性、QA checklist。 | 应复原为“limitations 存在，但裁决机制未报告 / weak evidence”。本地 A1 多路审计不能替代原文 S8。 | 弱：可记录 negative evidence；不支持强 QA / human arbitration pattern。 | PDF 全文再次检索是否存在 reviewer oversight、double screening、coder agreement、quality assessment；若仍无，保持弱或未报告。 |

## 5. 对现有 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 返修清单

### Critical（C）

- 无。当前材料没有发现会立即破坏本篇 A1 作为 schema seed 的致命问题；但下列 Important 项若不修，会让后续 A2a/A2b 误把本地复原关系写成原文 formal schema。

### Important（I）

1. **`problem→solution` 关系的来源层级需要统一改写。**
   - 影响文件：`review.md` 的“审计结论卡片”“原生样本编码维度树”“关系边表”，`evidence_chain.md` 的 `ev-re-agile-sms-2015-tree` / `clm-re-agile-sms-2015-tree`，`SUMMARY.md` S3 行。
   - 问题：部分位置写成“显式关系 schema / 显式关系边”，容易被读成原文 formal relation table。
   - 建议：统一写为“作者在 §IV.D 按 P1--P6 组织 solution prose；`problem→solution` 是本地复原关系边，不是原文 formal table”。

2. **venue relation 的证据锚点不足。**
   - 影响文件：`review.md` 关系边表 `R-venue-of`，必要时 `evidence_chain.md` A.2。
   - 问题：Table I 只给 venue type/name/count，不给每篇 S-id 的 venue；若写 `研究（S1..S28） -> published_in -> venue`，证据还需要 Primary Sources S1--S28。
   - 建议：把 `R-venue-of` 证据锚点改成 “Table I + Primary Sources [S1]--[S28]”，并区分 formal summary 与 local per-study reconstruction。

3. **S6 等级与 non-final 边界需在 `review.md` / `SUMMARY.md` 中 harmonize。**
   - 影响文件：`review.md` S1--S8 第一表、`SUMMARY.md` S5--S8 覆盖矩阵。
   - 问题：`review.md` 将 S6 写“强”，`SUMMARY.md` 写“中”；两者都可解释，但需要同一口径，避免后续矩阵统计混乱。
   - 建议：若保留“强”，必须同格写明“仅限 A1 schema 可用度；A2a 前不进入 final quantitative finding”；若坚持文本级保守，则两处都降为“中”。

4. **`evidence_chain.md` 仍是树级 claim map，缺少 S1--S8 与关键叶子 / 关系边的逐项证据。**
   - 影响文件：`evidence_chain.md` A.2/A.3/A.4。
   - 问题：当前 A.2 多数证据是 `not_verified` 且泛写“短引见 review”，不够支撑 A2a 的字段级复验，尤其是 Table II--V、Primary Sources、§IV.D solution prose。
   - 建议：A2a 时新增逐项 evidence rows：Table I venue summary、Primary Sources venue-of、Table II context、Table III type、Table IV benefits、Table V problems、§IV.D P1/P2/P5 solution prose、§IV.D P3/P4/P6 no-solution negative evidence。

### Minor（M）

1. **`review.md` 中个别中文/英文混排可清理。**
   - 例：`无解决方案（无解决方案_PROPOSED）`、`会议（会议）/ 期刊（期刊）/ 杂志（杂志）` 等表达略冗余。
   - 不影响事实，但降低可读性。

2. **`S20=2003` 与结论中 “2004--2014” 的年份跨度差异值得保留为注脚。**
   - 当前 `review.md` 已注意到这一点；A2a 可确认是否为作者结论笔误或出版年份口径差异。

3. **本地审计来源不应进入原文 S8。**
   - `review.md` 当前大体已区分；后续写作时仍需避免把三路 A1-DT 审计、主线程 adjudication 当成原文 researcher arbitration。

## 6. 本轮结论

- 本篇是强可用的 A1 SMS schema seed：S1/S2/S3/S6/S7 在 A1 二级 schema 意义上较强，S4 因局部关系边需复原而为中到强，S5 为中，S8 为弱。
- 最关键的返修点不是数字本身，而是**关系来源分层**：Table V 是 problem theme formal table；solution 只在 prose 中按 problem 讨论；`problem→solution` 关系边是本地复原，不是原文 formal relation table。
- 本文件不生成最终定量结论；所有 15/28、20/28、8/28、3/6 等数字只能作为本篇 SMS 内部描述统计和 A2a 候选字段，不能写成 Paper2 final empirical finding。
