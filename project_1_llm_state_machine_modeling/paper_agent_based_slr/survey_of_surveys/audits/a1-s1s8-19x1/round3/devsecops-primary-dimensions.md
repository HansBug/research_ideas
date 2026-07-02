# A1 S1--S8 独立审计：devsecops-primary-dimensions

- 审计对象：`papers/devsecops-primary-dimensions/`
- 输出文件：`audits/a1-s1s8-19x1/round3/devsecops-primary-dimensions.md`
- 审计身份：A1 survey-of-surveys 单篇维度抽取 subagent；未开启 sub-subagent。
- 审计边界：只做 A1 文本级维度树 / S1--S8 独立抽取与返修建议；**不得把本文件中的 A1 文本级判断写成 final quantitative finding**。

## 1. 全文阅读状态与依据

### 1.1 已阅读文件

| 文件 | 阅读状态 | 依据与局限 |
|---|---:|---|
| `bibtex.bib` | 已完整读取 | 12 行；确认题名、作者、JSS 2024、DOI `10.1016/j.jss.2024.112063`。 |
| `metadata.json` | 已完整读取 | 34 行；用于核对 `review_type=multivocal literature review`、`eligible_for_statistical_synthesis=true`、open PDF 与本地状态。 |
| `paper_content.txt` | 已按全文顺序阅读 | 3158 行；覆盖摘要、§1--§6、Data availability、Appendix A.1--A.3 与参考文献。关键锚点包括 RQ 与检索方法（约 L418--L616）、TA 与模型创建（约 L617--L779）、结果与表格（约 L796--L2040）、威胁与结论（约 L2083--L2221）、附录样本清单（约 L2222--L2859）。 |
| `review.md` | 已完整读取 | 451 行；重点核对 `## 维度树复原` 与 `## survey_of_surveys 自身 schema 抽取`。 |
| `evidence_chain.md` | 已完整读取 | 47 行；重点核对 A.1--A.4、证据强度、统计池资格和 A2a 复验项。 |
| `paper.pdf` | 本轮未视觉打开 | `paper_content.txt` 已覆盖正文文本；但 Fig. 2、Fig. 4--9、Tables 6--21 的版面、跨页对齐和 Zenodo full CPTM model 仍需 A2a PDF / Zenodo 精核。 |

### 1.2 阅读后总体判断

本文是系统性很强的 DevSecOps 多声部文献综述（MLR）：原文有明确 RQ、white / grey 双轨检索、纳排、QA、snowballing、confirmatory search 隔离、reflexive TA、五大 aspect、C/P/T/M 编号化条目、Gartner 十阶段生命周期投影、CPTM 关系边、open science material。A1 可以把它作为“关系型维度森林 + 多声部证据链”的强 schema seed；但 A2a 前不能把其字段数值或领域发现写成最终定量结论。

## 2. S1--S8 独立判定总表

> 等级只表示这篇论文对 `survey_of_surveys/` 二级 schema 的可用度，不是论文质量评分，也不是 final statistical synthesis 许可。`强` 均按“文本级强证据”理解；涉及表图、具体连线、Zenodo 附件或最终数值时仍需 A2a。

| 维度 | 等级 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 强 | 原文目标是 review/document/analyze DevSecOps current state 并调查 GSE contexts；RQ1 拆为 aspects、themes、links，RQ2 问 DevSecOps in GSE contexts（`paper_content.txt` L418--L433）。摘要也明确 MLR、WL/GL、TA 与 CPTM（L26--L41）。 | 树根为“DevSecOps 当前状态 + GSE 全球采用探测”；RQ1 是主维度森林，RQ2 是 context/absence probe。 | 可作为强 schema seed；不支撑 Paper2 目标领域最终发现。 | PDF 页码与 §3.3 原文页码；确认 RQ2 在后续回填中不被并入五大 aspect。 |
| S2 语料收集与筛选 | 强 | WL 数据库 ACM/IEEE/Scopus、GL 使用 Google；Search String 1/2、时间窗 2012--2021、英文、metadata/title/abstract/keywords 限制、前 18 页 GL、前 10 页 GSE GL、纳排和 QA 阈值均有说明（L443--L561）；Table 3 给出分母链（L657--L665）；confirmatory search 不进 TA/CPTM（L592--L604、L1993--L2003）。 | 语料树包含：主 RQ1 样本 102 WL + 43 GL、RQ2 额外 2 WL、confirmatory 13 WL + 7 GL（仅验证）、先前二级研究（只作验证/补入）。 | 主统计池候选；但 A1 只能记录“候选资格”和分母结构，不能汇总为最终数字。 | Table 3、Fig. 3、Appendix A.1--A.3 与 Zenodo protocol / QA score；统一 104 WL + 43 GL 摘要口径与 102+2 WL 结果口径。 |
| S3 原生维度树 / 样本编码对象 | 强 | RQ1.1--RQ1.3 明确要求 aspects / themes / links（L424--L431）；五大 aspects 明示为 Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement（L810--L826）；TA 层级 Text→Code→Themes→Model 明示（L691--L731）；CPTM 说明四类元素与关系边（L1728--L1748）。 | 原生结构是维度森林：五棵 aspect 子树 + 一张 CPTM 关系图 + 一棵 RQ2 GSE absence probe；样本单位外层是 included papers/articles，内层是 text segments/codes/themes/items。 | 强 schema seed；CPTM 具体关系边在 A2a 精核前只作候选关系模型。 | PDF/Zenodo full CPTM；核 definitions 子树是否只作 aspect/tree 而不进入 C/P/T/M 图。 |
| S4 字段级证据 | 中 | Table 5 给出每个 aspect 的 extracted data / codes / themes / categories（L944--L951）；Tables 6--19 给出 categories、themes/items、frequency、source IDs（如 L1087--L1162、L1176--L1320、L1325--L1562、L1567--L1727、L1796--L1824）；Table 21 给 C/P/T/M 映射（L1960--L1983）。 | 叶子字段可复原为 aspect、source track、source ID、text segment、code、theme、category、C/P/M/T ID、frequency、prior-review match/supplement、lifecycle stage、edge、missing relation。 | 文本级字段充分，但当前还不能作为 final quantitative pool：表格跨页、Fig. 5--9 连线与 Zenodo 原始表未核。 | PDF 表格跨页对齐；Zenodo raw text/codes、TA tables、full CPTM；区分 Table 5 三类 metrics 与补入 M20 Business metrics。 |
| S5 维度模式演化 | 强 | 原文说明 WL 初始 inductive coding/theming，GL 主要基于 WL codes/themes 做 deductive analysis，再引入 DevSecOps lifecycle framework 映射到最终 CPTM（L714--L731）；模型迭代 2021--2023，经三作者协商达成 consensus（L732--L755）。 | 演化链为：text segment → code → theme → category → lifecycle projection → CPTM；并保留 inductive/deductive 与作者协商节点。 | 可作为方法学 schema seed；不进入领域统计。 | Zenodo 的 TA 初版/完成版是否能支持“演化”细节；是否存在版本日志或仅论文叙述。 |
| S6 统计分析 | 强 | 原文提供检索分母链（Table 3）、aspect 频次分布（Fig. 4 叙述 L836--L852）、Table 5 计数、C/P/M/T 最终项数（L998--L1003、L1069--L1082、L1468--L1488、L1619--L1628、L1845--L1863）、RQ2 126→66→2 / GL 0（L1906--L1946）。 | 统计层包括 source-track 频次、aspect 分布、category 排序、prior-review overlap、CPTM edge coverage、GSE absence count、confirmatory-only trend。 | 文本级强候选；A2a 前不得汇总进 SUMMARY final quantitative finding。 | Fig. 4 数值、Tables 2/3/5/8--21、Zenodo QA score 与 raw tables；confirmatory search 必须保持 `confirmatory_only`。 |
| S7 候选 finding | 中 | 原文从统计和模型形成候选发现：Practices 最广、Metrics 最少（L836--L852）；challenges/practices category 排序（L998--L1004、L1077--L1083）；metrics 缺 consensus（L1468--L1495）；CPTM 可显示 practices/tools/metrics 关系和缺口（L1740--L1748）；GSE absence 与四种解释（L1947--L1992）；confirmatory trend（L1993--L2039）。 | finding 应挂接到 supporting observation、source scope、counter explanation、confirmatory-only 标志和 future validation；GSE absence 是负向发现，不是强事实。 | 只可作为 candidate finding pattern / claim-evidence heuristic；不可作为 Paper2 目标领域 finding。 | 每条 finding 对应的表图、分母、时间窗、竞争解释；尤其核 GSE absence 是否受 search-string 术语遗漏影响。 |
| S8 研究者 / 作者质疑与裁决 | 中 | 原文承认 reflexive TA 不要求 inter-rater reliability（L681--L690），编码主要第一作者完成但第二/第三作者 weekly/bi-weekly review 并协商 consensus（L732--L755），trustworthiness 按 credibility/confirmability/dependability/transferability 评估（L756--L775），threats 明示 selection/QA/extraction/coding/search-string 风险（L2094--L2155）。 | 可复原为“研究者协商与信度控制”节点；不是 adversarial adjudication，也不是完整 coder-decision log。 | 可统计为 trustworthiness / author-consensus pattern；不宜计为完整质疑-裁决机制。 | Zenodo 是否包含 coder notes、review protocol update log、会议/决策记录；若没有，S8 保持中。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 树型判定

- 树型：**维度森林 + 显式关系边图**。
- 原文明示部分：RQ1/RQ2、五大 aspects、Text→Code→Themes→Model、四类 high-order categories、C/P/M/T 编号化条目、Gartner 十阶段、CPTM 四列与连接线、RQ2 GSE absence probe。
- 本地复原部分：把上述结构整理为统一“树干--叶子--取值空间--关系边”表达；把 RQ2 单独写成 context probe；把 confirmatory search、prior reviews、open science material 作为边界/证据资产节点。

```text
[根] DevSecOps 当前状态与全球采用探测
├── [明示] RQ1：DevSecOps 在 white + grey literature 中的当前状态
│   ├── [明示] RQ1.1 aspects：{Definitions, Challenges, Practices, Tools/Technologies, Metrics/Measurement}
│   ├── [明示] RQ1.2 themes：每个 aspect 内部做 text segment → code → theme → category
│   └── [明示] RQ1.3 links：CPTM 关系模型，回答 aspects/themes 如何互相链接
├── [明示] RQ2：DevSecOps 在 GSE contexts 中如何被采用
│   └── [本地复原] GSE absence probe：Search String 2 + GL 搜索失败 + 2 篇边缘 WL + 4 个竞争解释
├── [明示] 语料与筛选子树
│   ├── WL 来源：ACM / IEEE / Scopus；主 RQ1 最终 102；RQ2 额外 2
│   ├── GL 来源：Google；主 RQ1 最终 43；RQ2 100 条浏览后 0
│   ├── prior reviews：排除出主样本，但用于 overlap、validation、supplement
│   └── confirmatory search：13 WL + 7 GL；不进入 TA/CPTM，只作新近验证
├── [明示] 五大 aspect 子树
│   ├── Definitions：28 WL + 15 GL definitions → 74 codes → 21 themes → 4 categories
│   ├── Challenges：73 WL + 53 GL challenges → 85 codes → 23 themes → C01--C28 → 4 categories
│   ├── Practices：219 WL + 137 GL practices → 142 codes → 56 themes → P01--P60 → 4 categories
│   ├── Tools/Technologies：18 WL + 45 GL tools → 56 tool codes → 16 themes → T01--T18 → Technology category
│   └── Metrics/Measurement：7 WL + 13 GL metrics → 20 codes → 16 themes；Table 5 为 OPC/PC/Technology 三类，后续补入 M20 Business metric
├── [明示] CPTM 关系图
│   ├── stages：{Plan, Create, Verify, Preproduction, Release, Prevent, Detect, Respond, Predict, Adapt}
│   ├── edge C→P：challenge 可对应多个 practice
│   ├── edge P→T：practice 可对应 tool group，也可 NA / not reported
│   ├── edge P→M：practice 可对应 metric，也可 NA / not reported
│   └── category color：OPC / PC / Technology / Business 作为叠加属性
└── [明示+本地复原] 证据与裁决子树
    ├── QA score：14 yes/no + literature type 0--4，总分 18，阈值 11
    ├── TA trustworthiness：credibility / confirmability / dependability / transferability
    ├── open science material：protocol、included papers + QA score、raw text/codes、TA tables、full CPTM
    └── threats：selection/QA/extraction bias、first-author coding、preconception、search-string construction
```

### 3.2 叶子取值空间

| 叶子/字段 | 原文明示或本地复原 | 取值空间 | 缺失值语义 | 统计用途 |
|---|---|---|---|---|
| source track | 明示 | `{WL, GL, prior-review validation, confirmatory-only}` | 不允许混写；prior / confirmatory 不进主 TA | WL/GL 对比、主样本隔离 |
| search string | 明示 | `{String 1, String 2, variants}` | variants 需记录失败路径 | absence finding 审计 |
| aspect | 明示 | 5 项完整枚举 | 不应新增第六项；GSE 是 context probe | aspect 分布 |
| text segment | 明示 | 自由文本片段 + source ID | 未抽取则不得编码 | Fig. 4 / Table 5 分母 |
| code | 明示 | 每个 aspect 内部自由文本规范化代码 | 不允许无 text segment | code 计数 |
| theme | 明示 | Definitions 21、Challenges 23、Practices 56、Metrics 16、Tools 16 | 不应合并跨 aspect | theme 分布 |
| category | 明示 | OPC / PC / Technology / Business；Tools 单 Technology；Metrics Table 5 为三类，补入后含 M20 Business | 必须区分“主 included studies”与“prior-review 补入” | category 排序 |
| item ID | 明示 | C01--C28、P01--P60、M01--M20、T01--T18 | Definitions 无 C/P/M/T ID，另有 common definition author | CPTM 节点 |
| frequency | 明示 | 自然数；部分补入项来自 prior review | 0 或无频次必须说明是否为补入 | 热度 / 覆盖度 |
| source ID | 明示 | S1-ACM/IEEE/SC/GL、S2-ACM、CS-* | Appendix 与表格需核对，不能脑补总数 | traceability |
| prior-review match | 明示 | 星号匹配、未标、或来自某 prior review 补入 | unmatched 不等于低质量 | validation / replication |
| lifecycle stage | 明示 | Gartner 10 阶段 | item 可多阶段；NA 合法 | stage projection |
| CPTM relation | 明示 | C→P、P→T、P→M，多对多 | NA / no linked tool / no linked metric 是有效缺失关系 | relation coverage / gap |
| DevOps metric mapping | 明示 | M-id ↔ Amaro Me-id | 未映射需保留 | 外部 taxonomy 对齐 |
| GSE absence explanation | 明示 | 无显著相关 / 安全集中化 / 真实 gap / 术语漏检 | 不允许只写“0 papers” | negative finding 边界 |

### 3.3 关系边

| 关系边 | 明示/复原 | 说明 | A2a 风险 |
|---|---|---|---|
| RQ→field | 明示 | RQ1.1/1.2/1.3 分别驱动 aspect、theme、link；RQ2 驱动 GSE probe。 | 需核 PDF 页码。 |
| paper/article→text segment→code→theme→category | 明示 | §3.8.2 和 Tables 5--19 支撑。 | Zenodo raw tables 待核。 |
| challenge→practice | 明示 | CPTM 中 practice address challenge。 | Fig. 5--9 / Table 21 连线需视觉核。 |
| practice→tool | 明示 | 并非每个 practice 都有 tool；NA 是缺失关系。 | Table 21 全量边需核。 |
| practice→metric | 明示 | 并非每个 practice 都有 metric；metrics 缺口可形成 candidate finding。 | Table 21 全量边需核。 |
| metric→DevOps metric | 明示 | Table 18 映射 DevSecOps metrics 到 DevOps metrics。 | 需核表格完整性。 |
| item→prior review | 明示 | 星号和补入来源表示与既有 review 的 overlap / supplement。 | 各表星号含义需逐表核。 |
| RQ2 search path→absence finding→four explanations | 明示+本地复原 | 原文给四种解释并承认 search-string 风险。 | A2a 可复核 search log / protocol。 |

## 4. 与现有 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的差异审计

### 4.1 总体采纳判断

现有 `review.md` 对原生树主干（维度森林 + CPTM 关系图）总体复原正确，`survey_of_surveys 自身 schema 抽取` 也基本满足 §6.4 的两表要求。但存在若干会影响后续 A2a 合并和 SUMMARY 读者理解的问题，尤其是“强等级”和“not_verified / schema_seed”之间的口径解释、证据链 A.2 的精确证据不足、以及个别分母/取值空间细节。

### 4.2 C/I/M 问题清单

#### Critical（C）

- 无。当前材料没有发现会立即破坏 A1 单篇树型判断的错误；但以下 I 级问题若被用于 A2a 定量统计前不修，会影响证据链可靠性。

#### Important（I）

1. **`evidence_chain.md` A.2 证据锚点过粗，不能单独支撑 S1--S8 强/中判定。** 现有 A.2 多数写“短引见 review.md”“待 A2a”，证据强度为 `not_verified`。这可以作为 A1-DT v2 暂存，但 A2a 前应把本轮已定位的 `paper_content.txt` 行段（如 RQ L418--L433、Table 3 L657--L665、TA L691--L755、Table 5 L944--L951、CPTM L1728--L1748、RQ2 L1906--L1992、Threats L2094--L2155）迁入正式 A.2，避免 evidence_chain 反而弱于 review/audit。
2. **`review.md` 维度树复原中的旧“Insight”段落疑似过时且自相矛盾。** 该段称“现 `review.md` 把这种封闭枚举式模式标为 `schema_seed` / `not_verified` 与文本证据严重不符，是审计第一返修点”。当前 `review.md` 和 `evidence_chain.md` 已明确 A1/A2a 冻结边界；继续保留这句话会误导读者以为 `schema_seed` / `not_verified` 是错误，而 GUIDE §6.3.8 恰恰要求 A2a 前不得升级。建议删除或改写为“文本级结构强，证据强度仍待 A2a”。
3. **S1--S8 `强` 等级在 SUMMARY 中容易被误读为 final quantitative 资格。** `review.md` 四分栏已有 A2a 待核验说明，但 `SUMMARY.md` S1--S8 表行把多个维度写成“强：...”时，读者可能忽略这是“文本级强”。建议在 SUMMARY 对该行或表头补一句：“强/中仅为 A1 文本级 schema 可用度；DevSecOps 数字和 finding A2a 前不得用于最终定量统计”。
4. **source ID / 样本数量口径需统一。** `review.md` 叶子表中 `L-source-id` 写“完整枚举但开放尾部 (148 项)”缺乏原文支撑；原文主 MLR 为 102 WL + 43 GL + RQ2 2 WL = 147，confirmatory 另 20，不进入 TA/CPTM。建议改成“主 MLR 147；confirmatory 20；source ID 编号非连续，实际清单以 Appendix A.1--A.3 为准”。
5. **Metrics category 取值空间需要显式拆分“主 included studies”与“prior-review 补入”。** Table 5 写 metrics 为 OPC/PC/Technology 三类；§4.1.2 又把 M20 Business metrics 从 Myrbakken 2017 补入并归入 Business。现有 review 同时写“metrics 三类”和“Business 仅 M20”，建议补一句：`Business` 不来自本文 included WL/GL metric text segments，而是 final metric list 中 prior-review supplement。

#### Minor（M）

1. `review.md` 的树代码块较长，但中文化总体达标；可在后续整理时拆成“语料树 / aspect 树 / CPTM 边表 / GSE probe”四段，提高可读性。
2. `SUMMARY.md` 顶部总表的样本量 `147` 建议加脚注或括号说明为 “102 WL + 43 GL for RQ1, plus 2 WL for RQ2；confirmatory 20 excluded from TA/CPTM”。
3. `review.md` S7 可把 “framework design 趋势”单独标为 `confirmatory_only finding pattern`，避免与主 MLR 统计观察同级。
4. `evidence_chain.md` A.4 已列 PDF 与 SUMMARY 复验，但未列 Zenodo protocol / QA score / raw tables / full CPTM；建议 A2a 加一行 Zenodo 工件核验。

## 5. 本轮 A2a 接力清单

1. 打开 `paper.pdf` 核对 Fig. 2、Fig. 4--9、Tables 2--21 的页码、表号、跨页行对齐和 CPTM 连线。
2. 访问或本地保存 Zenodo `10.5281/zenodo.7959584` 中的 protocol、included papers + QA score、raw data/text and codes、TA tables、full CPTM model。
3. 将本审计中的关键 `paper_content.txt` 行段迁入 `evidence_chain.md` A.2/A.3；保留旧 `not_verified` 行，新增替代证据后再按规则升级。
4. 在 `review.md` / `SUMMARY.md` 中保留“主 MLR / RQ2 / confirmatory / prior-review supplement”四类证据的分母隔离。
5. 所有 A1 S1--S8 结果只可作为 schema seed、candidate finding pattern 或 A2a 待核验入口；**不得写成 final quantitative finding**。
