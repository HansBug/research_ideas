# A1 S1--S8 round3 独立审计：app-reviews-slr-se

> 角色边界：本文件仅是 A1 survey-of-surveys 单篇维度抽取审计结果；只处理 `papers/app-reviews-slr-se`，未开启 sub-subagent，未混读其他论文。本文所有判断均为文本级 / 局部 PDF 核对结果，**不得写成 Paper2 的 final quantitative finding**。

## 0. 是否已全文阅读与依据

| 项 | 审计结论 |
|---|---|
| 单篇路径 | `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/app-reviews-slr-se` |
| 已读文件 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`、`evidence_chain.md` |
| PDF 核对 | 已用 `pdfinfo` 核对 `paper.pdf` 为 63 页；用 `pdftotext -layout -f 4 -l 5` 局部核对搜索 / PRISMA 附近版面，确认当前文本抽取对检索式仍不完整。未做全表格视觉级核对。 |
| 全文阅读依据 | `paper_content.txt` 已覆盖摘要、§1 Introduction、§2 Research Method、§3.1--§3.6 Results、§4 Discussion、§5 Threats、§6 Related Work、§7 Conclusion 与 References 区段；重点核对行 79--127、130--171、182--341、361--440、639--871、885--1490、1490--1700、1693--1885、1939--1971。 |
| 审计强度 | 全文文本级 + 局部 PDF 文本核对；复杂表格、PRISMA 图、搜索式、supplementary spreadsheet 仍为 A2a。 |

关键阅读证据：BibTeX 确认正式题名、作者、ESE、DOI；正文明确为 Kitchenham 风格 SLR，目标是综述 app review analysis 如何支持软件工程；§2.1 给出 RQ1--RQ5；§2.2 给出系统检索、纳排与 182 篇样本分母链；§2.3 Table 3 给出 F1--F18 抽取字段；§2.4 给出三套 classification schema 的构造与 reliability；§3--§4 给出结果表和 discussion finding；§5 给出 threats 与缓解。

## 1. 总体裁决

1. **原文类型**：正式 SLR。
2. **原文样本单位**：原始研究论文（primary studies），最终 $n=182$，发表时间 2012--2020；检索时间窗为 2010-01 到 2020-12。
3. **原生维度结构**：不是单一通用六叶模板，而是 RQ 驱动的字段森林：RQ1--RQ5 通过 Table 3 的 F1--F18 字段连接到三套分类 schema、评价 / 复现资产字段、统计表和 discussion finding。
4. **统计池资格**：作为 `survey_of_surveys` 的 SLR 方法 / 维度模式 / 统计呈现 / finding 形成模式，具备后续主统计池候选资格；但当前 A1 仍是文本级审计，`evidence_chain.md` 多处证据为 `not_verified`，A2a 精核前不得进入最终定量统计。
5. **主要 A2a 风险**：搜索式在当前文本抽取中为空白；Fig. 1、Tables 5--23 的复杂数值、矩阵对齐和 supplementary spreadsheet 尚未视觉核对；Table 12 等 OCR 百分比存在明显错位风险。

## 2. S1--S8 独立判定表

| 维度 | 等级 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 强 | 摘要和 §1 说明覆盖 182 篇 app review analysis 论文；§2.1 明确 RQ1--RQ5：分析类型、挖掘技术、支持的 SE 活动、评价方法、评价结果。 | 根任务为“分析 app reviews 如何支持软件工程”；RQ1--RQ5 是顶层任务分支，并显式映射到 F6、F7、F8/F9、F10--F18、F13。 | 可作为 task-setting / RQ-to-field 模式样本；不是 app-review 领域最终发现。 | 精确页码 / RQ 原文位置、出版页元数据。 |
| S2 语料收集与筛选 | 中 | §2.2 给出 Kitchenham + PRISMA 流程、2010-01--2020-12 时间窗、数据库检索、manual search、snowballing、纳排标准和 1656→303 dup→1353 screened→1225 excluded→128→+14→+40→182 分母链；筛选样本 Cohen’s Kappa=0.9。 | 语料构建子树包括：数据库集合、specific/general query、纳排、去重、manual venue search、backward/forward snowballing、最终样本。 | 作为 corpus-construction 模式候选可用；最终分母链和检索式不得在 A2a 前作为 final quantitative denominator。 | Fig.1 PRISMA 视觉核对；搜索式目前在 `paper_content.txt` 和局部 `pdftotext -layout` 中缺失；“six major digital libraries”实际名称只清楚抽到 5 个，需视觉核对是否漏掉库名。 |
| S3 原生维度树 / 样本编码对象 | 强 | §2.3 明确 selected studies 被逐篇抽取，Table 3 给出 F1--F18 data extraction form；§2.4 说明 F6/F7/F8 三套 schema；§3 按 RQ 展开统计结果。 | 复原为字段森林：书目元数据 F1--F5、分析类型 F6、技术 F7、SE activity 与理由 F8/F9、评价 / 资产 F10--F18、result/discussion 派生层。 | 可作为 native field forest / extraction-form 模式样本；原文没有给出名为“维度树”的 formal tree，本地树形化是复原。 | Table 3 版面、supplementary spreadsheet 字段与样本级编码是否一一对应。 |
| S4 字段级证据 | 中 | Table 3 明列 F1--F18，并在表后解释 F6.1/F6.2/F6.3、F7.1/F7.2、F10.1/F10.2、F14.1/F14.2、F18 内容；§3.5 进一步展示公开数据集、工具、标注者、质量量规、复现包。 | 叶子字段可较完整复原，但部分取值空间依赖结果表和 supplementary：F6.2、F7.2、F12、F13、F14/F18。 | 可作为 extraction-field schema seed；字段存在性强，字段取值频次和样本级证据暂不进入最终统计。 | F10.1/F10.2、F14.1/F14.2 等子字段是否全部原文明示；Table 16--23 与 supplementary 链接 / 可获取性。 |
| S5 维度模式演化 | 强 | §2.4 明确三套分类 schema 的来源和形成：继承既有分类、content analysis、语义合并、删除无关项、补 Recommendation、SWEBOK 术语映射；Table 4 报告 intra/inter-rater agreement。 | schema-construction 子树：schema 来源 → 初始类别 → 迭代编码 → 合并 / 删除 / 增补 → 最终类别 → reliability。 | 可作为 dimension-evolution / coding-rubric 模式样本；不应解释成长期时间演化或自动 schema learning 结果。 | Table 4 数值、20%/10% 抽样比例、外部 assessor 与全部作者讨论细节。 |
| S6 统计分析 | 中 | §3 提供年度、venue、分析类型、技术、SE activity、评价数据集、工具、five-number summary、range/median 与 qualitative synthesis；§3.6 明确异质性太强，不做 meta-analysis，改用 summarizing effect estimates。 | 统计层是字段森林的结果投影：频次 / 百分比、交叉表、组合表、五数概括、range/median、定性 synthesis；关键关系包括 F6×F7、F6×F8、F12/F13×F6/F6.2。 | 仅作为统计呈现模式候选；A2a 前不得把具体频次、百分比、median/range 写入 final quantitative finding。 | Tables 5--23 全部复杂表格视觉核对；尤其 Table 10--15 矩阵、Table 18 五数、Table 21 range/median、OCR 错位。 |
| S7 候选 finding | 中 | §4.1--§4.10 将统计观察和讨论转为 gaps / future work：SE use case 模糊、reference model 缺失、评价数据集小、复现资产不足、practice impact 不清、practitioner needs 缺失、efficiency/scalability 缺评、ML training drift 等。 | finding 层是“统计观察 → 作者解释 → future direction”的派生层；不属于原始研究逐篇编码字段。 | 可作为 finding-construction 模式候选；具体 app-review 领域 gaps 不迁移到 Paper2 目标领域。 | 逐条核对 §4 finding 与具体表格 / RQ 的支撑关系；区分 evidence-backed finding、作者假设和外部常识。 |
| S8 研究者 / 作者质疑与裁决 | 中 | §2.2 报告四作者筛选样本与 Cohen’s Kappa=0.9；§2.3/§2.4 报告 inter/intra-rater agreement；§5 给出 incompleteness、publication bias、subjectivity、taxonomy reliability 等 threats 与缓解。 | quality-control 子树包括 protocol review、pilot、screening reliability、data extraction reliability、classification reliability、threats / mitigation；但没有完整 disagreement log。 | 可作为 reviewer-quality-control 模式候选；若 S8 要求完整逐项 adjudication ledger，应降级为中。 | 核对 Kappa 样本、percentage agreement、panel review、外部 assessor 角色、是否有原始分歧和裁决记录。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 树型声明

- **原文明示**：RQ1--RQ5、Table 3 F1--F18、三套 classification schema、结果表、Discussion gaps、Threats。
- **本地复原**：将上述结构组织为“RQ 驱动字段森林”，并把 result/discussion/threats 标为派生层，而不是把它们混入 primary-study coding field。
- **禁止套模板**：不能把该文压成“对象 / 方法 / 数据 / 评价 / 发现 / 威胁”六叶通用模板；原文实际核心是 F1--F18 + schema construction + cross-tab/result synthesis。

```text
[根] app review analysis for software engineering 的原始研究集合（原文明示：primary studies，n=182）
├── [T0] 综述任务与 RQ（原文明示）
│   ├── RQ1：app review analysis 类型 → F6
│   ├── RQ2：挖掘技术 → F7
│   ├── RQ3：支持的软件工程活动 → F8 + F9
│   ├── RQ4：实证评价方式 → F10 + F11 + F12 + F14 + F15 + F16 + F17 + F18
│   └── RQ5：评价结果 → F13
├── [T1] 语料构建（原文明示；检索式待 A2a）
│   ├── 时间窗：2010-01--2020-12；实际样本发表 2012--2020
│   ├── 数据源：ACM、IEEE、Springer、Wiley、Elsevier；原文称 six major digital libraries，缺一项待核
│   ├── 查询：specific query + general query（文本抽取缺失，需 PDF 视觉核对）
│   ├── 纳排：Table 1 peer-reviewed / SE-related / app reviews supporting SE activities；排除非英文、非 SE、secondary/tertiary 等
│   └── 分母链：1656 → 去重 303 → 1353 screened → 排除 1225 → 128 + manual 14 + snowballing 40 = 182
├── [T2] 数据抽取字段森林（原文明示 Table 3；本地按分支复原）
│   ├── [A] 书目元数据 F1--F5
│   │   ├── F1 标题：自由文本
│   │   ├── F2 作者：列表
│   │   ├── F3 年份：2012--2020 年度值
│   │   ├── F4 发表源：开放枚举，Top venues 见 Table 5，完整列表在 supplementary
│   │   └── F5 引用数：数值，Google Scholar snapshot 2021-08-04
│   ├── [B] 评论分析类型 F6（原文明示 schema #1）
│   │   ├── F6.1 分析类型：{Information Extraction, Classification, Clustering, Search and Information Retrieval, Sentiment Analysis, Content Analysis, Recommendation, Summarization, Visualization}
│   │   ├── F6.2 挖掘信息：开放 / 层级取值，如 feature、bug report、NFR、opinion、topic、user request、user story
│   │   └── F6.3 补充描述：自由文本
│   ├── [C] 挖掘技术 F7（原文明示 schema #2）
│   │   ├── F7.1 技术大类：{Manual Analysis, Natural Language Processing, Machine Learning, Statistical Analysis}
│   │   └── F7.2 技术名：开放枚举；Table 12 给出常见 ML 技术，如 Naïve Bayes、SVM、Decision Tree、LDA、K-Means 等
│   ├── [D] 软件工程活动与理由 F8--F9（原文明示 schema #3）
│   │   ├── F8 活动：Requirements / Design / Testing / Maintenance 下 14 项活动，加 not specified
│   │   └── F9 理由：自由文本；原文明示有些论文没有 justification
│   └── [E] 实证评价与复现资产 F10--F18（原文明示字段；结果表展开）
│       ├── F10 评价目标：effectiveness 或 user-perceived quality，并绑定被评价的 F6.1
│       ├── F11 评价流程：自由文本；§3.5.1 抽象出四步 effectiveness evaluation 流程
│       ├── F12 指标 / 准则：precision、recall、F1、accuracy、MojoFM、BLEU-4、usefulness、accuracy、usability、efficiency、informativeness 等
│       ├── F13 评价结果：数值区间 / 中位数 / 定性结果
│       ├── F14 标注数据集：store 来源 + 标注评论数量
│       ├── F15 标注任务：自由文本，通常绑定 F6.1
│       ├── F16 标注者数量：1--5，中位数 2（文本级）
│       ├── F17 质量量规：Cohen’s Kappa、Percentage Agreement、Jaccard、Fleiss’ Kappa、未报告
│       └── F18 复现包：是否可用 + 数据集 / 工具 / 脚本等内容；作者还联系 primary-study 作者核查
├── [T3] schema 构造与 reliability（原文明示；本地整理为演化子树）
│   ├── F6 schema：Martin 2017 + mining tasks + text analytics → 合并 / 删除 / 补 Recommendation → 9 类
│   ├── F7 schema：Tavakoli 2018 + text analytics → 删除 feature extraction → 4 类
│   ├── F8 schema：SWEBOK 258 terms → 58 candidate → 14 final activities
│   └── reliability：数据抽取与三套 schema 均做 inter/intra-rater agreement；完整 disagreement log 未给出
├── [T4] 统计结果层（原文明示结果表；本地标为派生层）
│   ├── demographics：年份、venue 类型、top venues、highly cited papers
│   ├── RQ1/RQ2/RQ3：频次、百分比、交叉表、组合表
│   ├── RQ4：公开数据集 / 工具、标注者、质量量规、five-number summary、user-study criteria / participants
│   └── RQ5：effectiveness range/median、user-study qualitative synthesis
└── [T5] discussion / threats 派生层（原文明示；本地标为候选 finding 与风险层）
    ├── §4.1--§4.10：growth、use case、reference model、dataset size、replication、practice impact、practitioner needs、industrial need、efficiency/scalability、ML training drift
    └── §5：incompleteness、publication bias、screening/extraction/classification subjectivity、taxonomy reliability
```

### 3.2 核心叶子取值空间审计

| 叶子 | 原文明示程度 | 取值空间 | 审计判断 |
|---|---|---|---|
| F1--F5 书目字段 | 明示 | 自由文本 / 年份 / venue 开放枚举 / citation 数值 | 可作通用 SLR 元数据字段；F5 有 snapshot 日期，跨论文统计需固定时间口径。 |
| F6.1 分析类型 | 明示 | 9 类封闭枚举 | A2a 核验 Table 7 后可进入字段级统计；领域语义不可迁移到 LLM4STM。 |
| F6.2 挖掘信息 | 部分明示 | 开放 / 层级枚举 | 需要 supplementary 才能确认完整取值；当前只作 schema seed。 |
| F7.1 技术大类 | 明示 | 4 类封闭枚举 | 可迁移“技术大类 + 具体技术名”结构；具体技术取值随时代变化。 |
| F7.2 具体技术名 | 部分明示 | 开放枚举；Table 12 列常见 ML 技术 | 当前 OCR 数值有错位风险，A2a 前不统计。 |
| F8 SE activity | 明示 | Requirements / Design / Testing / Maintenance 下 14 项 + not specified | 结构可迁移，具体活动因领域和 SWEBOK 版本需重建；not specified 是显式缺失值。 |
| F9 Justification | 明示字段，值不封闭 | 自由文本；可派生是否提供理由 | 对 Paper2 很重要：需记录“作者声称支持某活动”与“如何支持”的解释边。 |
| F10--F13 评价字段 | 明示 | 目标、流程、指标、结果；含数值与自由文本 | 可迁移为 evidence / evaluation 模块；具体结果必须 A2a 表格核验。 |
| F14--F18 复现资产字段 | 明示 | store、review 数、annotation task、annotator 数、quality measure、replication package | 可迁移为 artifact completeness rubric；但不能把“有包”直接等同于“可复现质量高”。 |

### 3.3 关系边审计

| 关系边 | 原文明示 / 本地复原 | 来源 | 关系含义 | A2a 风险 |
|---|---|---|---|---|
| RQ → F 字段 | 原文明示 | Table 3 `Use` 列 | RQ1=F6；RQ2=F7；RQ3=F8/F9；RQ4=F10--F12/F14--F18；RQ5=F13 | 低；核对表格版面即可。 |
| F6.1 × F7.1 | 原文明示 | Table 10 | 分析类型与技术类型交叉频次 | 高；矩阵 OCR / 对齐需视觉核验。 |
| F7.1 组合 × F6.1 | 原文明示 | Table 11 | 多技术组合如何实现分析类型 | 高；多列表格对齐需视觉核验。 |
| F6.1 × F8 | 原文明示 | Table 14 | 分析类型如何支持 SE activity | 高；Table 14 视觉核对。 |
| F6.1 组合 × F8 | 原文明示 | Table 15 | 多分析组合如何支持 SE activity | 高；Table 15 视觉核对。 |
| F6.1 × F12 user-study criteria | 原文明示 | Table 19 | 用户研究按评价准则和分析类型映射 | 中；需核对表格。 |
| F6/F6.2 × F13 results | 原文明示 | Table 21--22 | 不同分析和 mined information 的效果区间 / 定性结果 | 高；不得文本级直接统计。 |
| review × external artifact | 原文明示 | Table 8 | Search/IR 中 app reviews 与 app description、Git commit、goal model、issue、source code 等外部制品连接 | 中；字段存在强，表格细节需核对。 |
| 统计观察 → discussion gap | 本地复原 | §4.1--§4.10 回指 RQ/Table | 作者把结果解释为 gap / future work | 高；A2a 需逐条判定证据强度。 |
| 本文维度 × prior surveys | 原文明示 | Table 23 | 与 4 篇相关综述比较覆盖维度 | 中；用于 related-work positioning，不进入主统计池。 |

## 4. 对现有 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 问题清单

### C 级

- 暂未发现需要立即阻断的 C 级问题。现有 `review.md` 已有“四分栏证据拆分”和 A2a 限制，基本避免把 A1 文本级结果直接写成最终统计结论。

### I 级

1. **S1--S8 等级过强风险**：`review.md` 和 `SUMMARY.md` 当前把 S1--S8 多数写为“强”。按本轮审计，S2/S4/S6/S7/S8 至少应在 A2a 前降为“中”或在矩阵单元中显式加“文本级强、最终统计前待 A2a”。否则后续 agent 容易把搜索式、复杂表格和 finding 支撑关系误读为 final evidence。
2. **证据链强度与正文等级不一致**：`evidence_chain.md` A.2 对 type/unit/denom/tree 等证据多写 `not_verified`，但 `review.md` S1--S8 第一张表和 `SUMMARY.md` 覆盖矩阵没有同步体现这种降级。建议在 `review.md` S1--S8 表中增加“文本级 / A2a 前”限定，或把 S6/S7/S8 的等级改为“中”。
3. **搜索式与数据库数量待核未充分影响 S2 等级**：原文称 six major digital libraries，但当前文本和局部 `pdftotext -layout` 只清楚显示五个名称，且 two search queries 内容缺失。S2 不宜无条件标“强”；至少应在 `review.md` / `SUMMARY.md` 的 S2 单元标明“exact query 待 PDF 视觉核对”。
4. **`review.md` “已可信赖入分母候选”措辞可能过强**：维度树复原 §6 说“原文字段/统计表支撑的统计观察（已可信赖入分母候选）”。鉴于表格仍未 A2a，建议改为“文本级候选统计观察 / A2a 后方可进入最终定量”。
5. **`evidence_chain.md` 对 S1--S8 的证据粒度不足**：当前 A.2/A.3 只有 type/unit/denom/tree/pool 级核心证据，没有逐项 S1--S8 证据 ID。若后续要把 S1--S8 写入 SUMMARY 统计矩阵，建议新增 S1--S8 级 evidence/claim 或在本 round3 audit 被采纳后回链本文件。

### M 级

1. **维度树表述有轻微重复**：`review.md` 说“3 套 classification schema + 1 棵 SE activity 树”，但 SE activity 本身就是三套 schema 之一（F8）。建议改成“3 套 classification schema，其中 F8 是 SE activity 树”，避免双计。
2. **Table 12 OCR 错位风险可在待复核中更具体**：`paper_content.txt` 中 Decision Tree / Random Forest 百分比明显异常，建议在 `review.md` 待复核第 5 条中点名 Table 12 百分比 OCR 风险。
3. **S7 可更明确分三类 finding**：建议把 §4 finding 拆成 evidence-backed observation、作者解释、future-work recommendation 三类，方便后续 A2a 判断哪些可进 finding-construction pattern，哪些只能作背景讨论。

## 5. 禁止升级声明

- 本文件不产生 Paper2 的最终定量发现。
- `182`、`109/105/23/87`、各表频次、percent、range、median、five-number summary 目前只能作为“原文文本级待 A2a 核验的候选统计观察”。
- 可迁移的是：RQ→字段→schema 构造→统计呈现→discussion finding→threat mitigation 的方法结构；不可迁移的是 app review 领域具体分类、具体效果数值和领域 gap。
