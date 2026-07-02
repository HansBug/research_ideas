# A1 round3 单篇审计：kitchenham-2009-slr-tertiary

> 审计身份：A1 survey-of-surveys 单篇维度抽取 subagent；本轮只处理 `papers/kitchenham-2009-slr-tertiary/`，未开启 sub-subagent，未读取其他论文正文。
> 证据边界：本文件是 A1 文本级 / 局部 PDF spot-check 审计结果，只服务 S1--S8 schema 与单篇原生维度树复核；**不得写成 Paper2 的 final quantitative finding，也不得把本文 2004--2007.6 的具体计数外推到现代 SE / LLM4SE 领域。**

## 1. 全文阅读依据与核验边界

### 1.1 已读本地文件

| 文件 | 本轮使用方式 | 关键读取范围 / 作用 |
|---|---|---|
| `bibtex.bib` | 已读 | 锁定正式题名、作者、IST 51(1):7--15、2009、DOI `10.1016/j.infsof.2008.09.009`。 |
| `metadata.json` | 已读 | 核对本地把该文标为 `tertiary-like SLR`、`eligible_for_schema_seed=true`、`eligible_for_statistical_synthesis=true`；注意 CCF 为本地缓存 / 官方待复核。 |
| `paper_content.txt` | 已按文本全文阅读 | 共 962 行；覆盖摘要、§1--§5、Tables 1--5、Tables A1--A3、References。关键行号见下表。 |
| `review.md` | 已读 | 核对现有六类 pattern、A1-M0--M6、维度树复原、S1--S8 表与四分栏。 |
| `evidence_chain.md` | 已读 | 核对 A.1--A.4 的现有证据链；当前多条 A.2 仍为 `not_verified / 待 A2a`。 |
| `paper.pdf` | 局部核对 | 用 `pdftotext -layout` 与页面截图 spot-check 了 Table 2、Table 3、Table A1、Table A3 的版面；未完成逐单元格视觉复核。 |

### 1.2 关键原文锚点

| 锚点 | 位置 | 支撑内容 |
|---|---|---|
| 研究目的 / tertiary 类型 | `paper_content.txt` L88--104 | 作者明确把研究目标设为 review current EBSE status，并称本研究是评估 secondary studies 的 tertiary literature review。 |
| RQ 树 | L105--141 | RQ1 活动量、RQ2 主题、RQ3 主导者、RQ4 限制；RQ4.1--RQ4.4 覆盖主题限制、primary study 数量、质量、实践指南。 |
| 检索源与人工筛选 | L142--185；Table 1 L161--177 | 手工搜索特定期刊 / 会议；每个来源由一名研究者审查，另一名研究者检查 included / excluded 论文。 |
| 纳排标准 | L186--203 | 纳入 peer-reviewed SLR / MA；排除 informal literature surveys、EBSE/SLR procedure papers、duplicate reports。 |
| DARE QA | L204--242；Table 3 L465--489 | QA1--QA4、Y/P/N/Unknown 计分、Kitchenham + 其他作者独立评分、分歧讨论、unknown 经邮件询问后重评。 |
| 数据抽取字段 | L243--267 | 明列来源 / 引用、Type/Scope、topic、作者/机构/国家、summary/RQ answers、quality、EBSE/guideline refs、practitioner guidelines、primary studies 数。 |
| 数据分析字段到 RQ | L268--283 | 明确每类 tabulation 对应 RQ1--RQ4.4，是 RQ→字段→统计表的桥。 |
| protocol deviations | L284--295；L639--680 | 说明偏离指南之处：manual search、单人选择+他人检查、单人抽取+他人检查等。 |
| 检索漏斗与最终 N | L298--316；Table A1 L589--633 | `2506 total → 33 relevant → 19 selected articles → 18 unique studies → +2 external → N=20`。 |
| 主样本编码表 | Table 2 L335--390；PDF page 10 spot-check | 20 条 S1--S20，列出 Author、Date、Topic type、Topic area、Article type、Refs、practitioner guidelines、Num. primary studies。 |
| 质量统计表 | Table 3 L465--489；PDF page 11 spot-check | 20 条 × QA1--QA4 + total score + initial rater agreement。 |
| 附属机构表 | Table A3 L750--810；PDF page 14 spot-check | 作者、机构、国家，用于 RQ3；是作者机构辅助扩展表，不是独立主样本树。 |

## 2. S1--S8 五分栏抽取

> 等级口径：`强 / 中 / 弱 / 不适用` 只表示对 `survey_of_surveys/` 二级 schema 的可用度，不等于论文质量评分；统计池资格单列说明。所有“强”均仍受 A1 文本级和 A2a 表图精核边界约束。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定（强） | §1--§2 明确本文是评估 SE SLR/MA 的 tertiary literature review；RQ1--RQ4 与 RQ4.1--RQ4.4 完整给出任务、scope 与样本单位。 | 根对象应写为“2004-01-01 至 2007-06-30、主要国际 SE 期刊/会议中的二次研究（SLR/MA）”；RQ 树驱动字段抽取与结果章节。 | 可作为 tertiary-review 任务设定与 RQ-tree 的 schema seed；不可迁移其 2009 年领域状态结论。 | 核对 PDF 中 §2/§2.1 页码与 “tertiary literature review” 原文；确认年份窗口与 peer-reviewed 条件。 |
| S2 语料收集与筛选（强） | §2.2--§2.3 给出人工搜索、补检索、纳排；§3.1/Table A1 给出 `2506→33→19→18+2→20`；Table A2 给出未选候选及原因。 | 语料树不是主样本编码树，而是过程 / 分母链：来源×年份的 Total、Relevant、Selected，加上重复处理、外部补入、排除原因。 | 可作为后续主统计池候选的分母链模式；但 A1 不得把 `2506/33/19/20` 写入最终跨论文定量结论。 | Table 1 的“10 journals + 4 conference proceedings”与可见 conference series 枚举存在口径需精核；Table A1 总数、n/a、selected 合计、外部补入来源需逐格核对。 |
| S3 原生维度树 / 样本编码对象（强） | §2.5 明列数据抽取字段；Table 2 对 S1--S20 应用主编码；§2.4/Table 3 应用 DARE QA；Table A3 扩展作者机构。 | 主树是“20 篇 SLR/MA 的抽取编码表”；DARE QA 是附着在同一 S1--S20 样本上的质量辅助子树；Table A3 是作者/机构/国家辅助展开；Table A1/A2 是检索与排除过程辅助树。 | 可作为原生维度树 / 森林强 schema seed；只有完成 A2a 表图锚定后，具体叶子取值才可进入跨论文统计。 | 核对 Table 2 跨页无漏列；核对 Table 3 与 Table A3 是否完全映射到 review 的叶子；确认 Table A1/A2 不被误当作 20 篇样本的主编码字段。 |
| S4 字段级证据（强） | §2.5 的抽取项、Table 2、Table 3、Table A1--A3 支撑来源、年份、类型、范围、主题、作者/机构/国家、EBSE 引用、实践指南、一级研究数、QA 与漏斗字段。 | 字段级证据较强，但“Summary of the study including RQ and answers”只在 §2.5 声明并指向技术报告 Appendix 3，本地未见完整取值表。 | 可作为字段证据 schema seed；`summary/RQ answers` 叶子在本地只可标为 not_verified / value unavailable。 | 需补核技术报告 [24] Appendix 3 或在 review/evidence 中明确本地缺失；逐字段核对 OCR 残留与表格脚注。 |
| S5 维度模式演化（弱） | §2.7 记录 protocol deviations；§2.6 说明 RQ 与数据分析的关系；无 open coding、codebook version、分类迭代、冲突修订日志。 | 可复原为“RQ 驱动字段设计 + DARE 既有量规 + protocol deviation 说明”，不是维度模式演化树。 | 不建议进入主统计池；仅作“早期 tertiary SLR 未暴露 schema evolution”的边界提示。 | 核对技术报告是否有 protocol / Appendix 1；若无补充证据，不应把 S5 升为中/强。 |
| S6 统计分析（强） | §2.6 列出 8 个 tabulation；§3--§4、Table 4/5 给出类型、主题、机构/国家、质量得分、Spearman、ANOVA、实践指南等统计。 | 统计分析从字段树派生：年份/来源、Refs、范围/主题、机构国家、primary-study 数、QA score、practitioner guideline。 | 可作为“字段→统计观察→discussion”的强模式；A1 只保留候选，不写 final quantitative finding。 | 逐格复核 Table 4/5、Spearman `0.51 (p<0.023)`、ANOVA `F=0.37, p=0.55`；确认 duplicated study 采用 first publication date。 |
| S7 候选 finding（强） | §4--§5 从统计观察形成主题覆盖有限、成本估计集中、Simula/欧洲主导、实践指南不足、搜索范围限制、mapping study 价值等 discussion/conclusion。 | 应拆成三层：OBS 统计观察、作者候选 finding / recommendation、不可迁移历史领域结论。 | 可作为 finding 形成机制模式；不得迁移 “欧洲/Simula 主导”“ACM Surveys 无 SE SLR” 等历史快照。 | 核对每条 finding 与字段/统计表的回链；在 SUMMARY 中保持“模式先验”而非领域结论。 |
| S8 研究者 / 作者质疑与裁决（中） | §2.2 筛选由单人负责、另一人检查；§2.4 QA 为 Kitchenham + 其他作者独立评分并讨论分歧，unknown 邮件询问作者后重评；§2.5 数据抽取为单抽取+单检查；§4.5 承认偏离医学标准。 | 可复原为“筛选/抽取的 checker 机制 + QA 双人独立评分 + disagreement discussion + author query”；不是完整双人独立筛选/抽取 coding log。 | 可作为 researcher-gate / quality-control 中等级模式；不宜按“完整双人独立裁决日志”统计。 | 核对 Table 3 initial rater agreement 列；核对 §2.4/§2.5/§4.5，避免 SUMMARY 把 S8 写成强。 |

## 3. 原生维度树 / 维度森林裁决

### 3.1 样本单位与总体树型

- 原文类型：tertiary SLR / review of SLRs；本地可称 `tertiary-like SLR`。
- 主样本单位：一篇二次研究论文，即被纳入的 SLR 或 MA；最终 `S1--S20`，其中 19 篇 SLR、1 篇 MA。
- 主分母链：`2506 total records/articles → 33 relevant articles → 19 selected articles → 18 unique studies → +2 externally located peer-reviewed studies → N=20 studies`。
- 树型裁决：**主树 + 辅助森林**，而不是把所有表格都压成一棵普通字段树。

### 3.2 主树：20 篇 SLR/MA 的抽取编码表

```text
[主根] 2004--2007.6 SE 二次研究样本（N=20；S1--S20）
├── 书目信息 / 来源
│   ├── 样本编号：S1--S20
│   ├── 作者 / 引用：Table 2 的 Author 列
│   ├── 年份：2004 / 2005 / 2006 / 2007 / 双版本年份
│   └── 来源与完整引用：§2.5 声明抽取；完整引用需回 References 与正式 DOI
├── 研究类型与范围
│   ├── Article type：{SLR, MA}
│   ├── Topic type：{Research trends, Technology evaluation}
│   └── Topic area：开放枚举，如 cost estimation、unit testing、COTS、SE experiments 等
├── EBSE / guideline 连接
│   └── Refs：{Guideline TR, EBSE paper, No}
├── 实践影响
│   └── Include practitioner guidelines：{Yes, No, No* / footnote}
└── 一级研究数量
    └── Num. primary studies：整数；Table 2 给出 6--1485 范围
```

说明：§2.5 还声明抽取“study summary including main RQ and answers”与“research question/issue”，但当前本地 `paper_content.txt` 只说 summaries 在技术报告 [24] Appendix 3；若未补入该附录，不能把这两个叶子写成已有完整取值表。

### 3.3 辅助子树 / 辅助森林

```text
[AUX-QA] DARE 质量评价辅助子树（同一 S1--S20 样本）
├── QA1 纳排标准是否描述且合适：Y/P/N/Unknown → 1/0.5/0/unknown
├── QA2 搜索是否可能覆盖所有相关研究：Y/P/N/Unknown → 1/0.5/0/unknown
├── QA3 是否评价纳入研究质量 / validity：Y/P/N/Unknown → 1/0.5/0/unknown
├── QA4 基础数据 / 研究是否充分描述：Y/P/N/Unknown → 1/0.5/0/unknown
├── Total score：0..4
└── Initial rater agreement：0..4；Table 3 报告实际 2..4

[AUX-FUNNEL] 检索漏斗与纳排辅助树（过程单位为 source × year / candidate article）
├── Table A1：每个来源 × 年份的 Total / Relevant / Selected
├── Table A2：未选候选论文及排除原因
├── duplicate handling：19 selected articles → 18 unique studies
└── external additions：研究者询问 + Simula 网站补入 2 篇 peer-reviewed studies

[AUX-AFFILIATION] Table A3 作者机构辅助展开（同一 S1--S20 样本的 author-level expansion）
├── Authors：每篇研究的作者行
├── Institution：作者所属机构
└── Country of institution：机构国家；用于 RQ3 主导者 / 机构 / 国家统计

[AUX-PROCESS] 研究者质量控制与偏离协议辅助树
├── screening：单人选择 + 另一研究者检查 included/excluded
├── QA scoring：Kitchenham 评全部 + 其他作者独立评分子集；分歧讨论至一致
├── unknown QA：邮件询问原作者后重评
└── extraction：单人抽取 + 另一人检查；作者承认不完全符合医学 SLR 标准
```

### 3.4 主树与辅助树边界

1. **Table 2 / §2.5 是主样本编码树的事实源**：它描述 20 篇被纳入 SLR/MA 的核心字段。
2. **DARE QA 是强辅助子树**：它和主样本共享 S1--S20 样本单位，但字段语义是质量评价 rubric，不应与 topic/source 字段混成同一层。
3. **Table A1 / A2 是过程树**：它们支撑检索、纳排、排除理由与分母链；不应把 `Total/Relevant/Selected` 当作每篇 SLR 的叶子属性。
4. **Table A3 是 author-level expansion**：它是 RQ3 所需的作者-机构-国家展开表，可连接到主树的作者字段，但不是新的研究样本集合。
5. **技术报告 Appendix 3 是缺失外部证据**：若要声称每篇 SLR 的 summary/RQ answers 已逐项复原，必须补该附录或降级为“原文声明抽取但本地未见取值”。

## 4. 需修改 review / evidence_chain / SUMMARY 的 C/I/M 清单

### Critical（C）

- C0：本轮未发现必须立即阻断的单篇事实错误；但若后续把 A1 文本级的 `2506/33/19/20`、QA 分数、Spearman/ANOVA 或 2009 年 EBSE 领域判断直接写成 final quantitative finding，应视为 critical 证据链错误。当前本文件只作为预防性边界声明。

### Important（I）

| 编号 | 影响文件 | 问题 | 建议修改 |
|---|---|---|---|
| I1 | `SUMMARY.md` | 当前 S1--S8 覆盖矩阵中 Kitchenham 2009 的 S5 / S8 口径与单篇 `review.md` 不一致：单篇为 S5 弱、S8 中；SUMMARY 片段可读为 S5 中、S8 强。 | 将 SUMMARY 对该文的 S5 降为“弱：无显式 schema/codebook 演化，只保留 RQ 驱动字段与 protocol deviation 启发”；S8 降为“中：QA 有双人独立评分与分歧讨论，但筛选/抽取是 single+checker”。 |
| I2 | `review.md` / `evidence_chain.md` | “单树为主 + 双子树并列”仍容易让读者把 DARE QA、检索漏斗、Table A3 混为同级主树。 | 改成“主树 + 辅助森林”：主树 = 20 篇 SLR/MA 抽取编码表；辅助 = DARE QA、检索漏斗/排除、Table A3 作者机构、过程裁决。 |
| I3 | `review.md` / `evidence_chain.md` | §2.5 的 `Summary of the study including main research questions and the answers` 与 `Research question/issue` 目前在本地缺少完整 Appendix 3 取值；review 树中若作为普通叶子，会高估字段级证据。 | 将这两个叶子标注为“原文声明抽取；本地未见完整取值；需 [24] Appendix 3 / 技术报告补证”；在 evidence_chain A.2 增加缺失外部证据或 `not_verified` 行。 |
| I4 | `SUMMARY.md` / `review.md` 快速卡片 | `review.md` 快速卡片写“是否目标证据池：否；只作为脚手架模式先验”，但 `metadata.json` 和后文写 `eligible_for_statistical_synthesis=true` / 后续主统计池候选，容易混淆“目标领域证据池”和“survey_of_surveys 主统计池候选”。 | 改成“不是目标领域证据池；是 survey_of_surveys 后续主统计池候选 / schema_seed；A2a 前不进入最终定量统计”。 |
| I5 | `SUMMARY.md` / `evidence_chain.md` | S2 搜索源口径需保守：摘要称 10 journals + 4 conference proceedings，但 Table 1 可见命名 conference series 为 ICSE、Metrics、ISESE；当前 SUMMARY 若直接写“4 个会议”会被读成已完成枚举事实。 | SUMMARY 改为“摘要称 10 journals + 4 conference proceedings；Table 1 来源枚举与 proceedings 计数待 A2a 版面复核”。evidence_chain 可记录该口径差异。 |
| I6 | `evidence_chain.md` | A.2 目前是树级 claim map，多个核心证据仍写“待 A2a / 短引见 review.md”；对 S1--S8 尤其 S5/S8 的降级裁决缺少独立证据行。 | A2a 前不必升级为最终证据，但若要回填 SUMMARY，应至少新增 S5/S8 降级证据行，标明 §2.7、§4.5 与 Table 3 agreement。 |

### Minor（M）

| 编号 | 影响文件 | 问题 | 建议修改 |
|---|---|---|---|
| M1 | `review.md` | Table A2 是未选候选论文与排除原因，不是 20 篇已纳入研究的数据抽取表；当前叶子 `leaf-excl-reason` 已作辅助边界，但可再强调。 | 在 Table A2 相关叶子旁标注“candidate / excluded article unit，不参与 S1--S20 主样本统计”。 |
| M2 | `review.md` | Table A3 OCR 中存在人名 / 机构拼写残留，如 Galin/Gavin、Politécnica、Karahanović 等。 | 正式写作前以 PDF / DOI 页面或原文 References 复核人名机构，避免 OCR 残留进入论文。 |
| M3 | `evidence_chain.md` | A.4 复验命令提到结构门禁，但没有本轮 round3 的 PDF spot-check 记录。 | 后续若主线程采纳，可在 adjudication 而非本文件中记录本轮 spot-check：PDF page 10 Table 2、page 11 Table 3、page 14 Table A3。 |

## 5. 本轮可采纳的一句话裁决

Kitchenham et al. 2009 是本目录中强 tertiary-study schema seed：它有明确 RQ、检索漏斗、纳排、20 篇 SLR/MA 主样本编码表、DARE QA 与统计观察；但原生结构应写作“20 篇二次研究主编码树 + DARE / funnel / affiliation / process 辅助森林”，S5 只能弱化为 protocol/RQ-field 启发，S8 只能中等化为部分独立 QA + checker 机制；所有数值在 A2a 表图精核前只可作为文本级候选证据，不可成为 final quantitative finding。
