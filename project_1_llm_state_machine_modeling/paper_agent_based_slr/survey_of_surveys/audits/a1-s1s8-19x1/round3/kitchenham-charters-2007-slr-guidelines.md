# kitchenham-charters-2007-slr-guidelines：A1 S1--S8 round3 独立审计

> 角色声明：本文件仅为 A1 survey_of_surveys 单篇维度抽取 subagent 的文本级独立审计结果；未开启 sub-subagent。本文是 guideline，不是普通统计样本。本报告只能作为 review / evidence / SUMMARY 返修输入，**严禁把这里的 S1--S8 判定或 Appendix 2 局部复算写成 final quantitative finding**。

## 1. 全文阅读依据与边界

### 1.1 已读材料

- 已读指定技能与规则：`ai-research-writing-skill/SKILL.md`、`research-planning/SKILL.md`、`survey_of_surveys/GUIDE.md` §6.3/§6.4。
- 已读本篇基础文件：
  - `bibtex.bib`：确认本文为 2007 年 EBSE 技术报告 `Kitchenham2007SLRGuidelines`。
  - `paper_content.txt`：3091 行全文文本已覆盖阅读；重点覆盖 front matter、§1--§9、Appendix 1--3。
  - `review.md`：334 行已读，重点检查“维度树复原”和“survey_of_surveys 自身 schema 抽取”。
  - `evidence_chain.md`：47 行已读，重点检查 A.1--A.4 与 `not_verified` / 统计池裁决。
- PDF 核对：因 20 分钟限制，仅用 `pdfinfo` 做元数据核对：本地 `paper.pdf` 为 65 页 A4 PDF；未视觉逐页核对表格、图和跨页 Appendix，相关项仍应进入 A2a。

### 1.2 关键原文锚点

- 目标与类型：Executive Summary 明确目标是提出适合软件工程研究者和博士生的系统综述指南；并声明指南覆盖 planning / conducting / reporting 三阶段，且不详述 meta-analysis 机制（`paper_content.txt` Page vi，约 lines 240--258）。
- 指南来源与构建过程：§1.1 列出 Cochrane、Australian NHMR、CRD、Petticrew & Roberts、Fink、跨学科专家会议、EBSE 项目经验等来源；§1.2 说明从单作者初稿到双作者更新、内部评审、外部专家独立评审、再修订的 guideline construction process（约 lines 316--356）。
- 综述概念：§2 定义 systematic literature review、systematic mapping study、tertiary review，并强调 protocol、search strategy、inclusion / exclusion criteria、quality criteria 和 data extraction（约 lines 404--512）。
- SLR 流程：§4 将流程拆成 Planning / Conducting / Reporting 三阶段，并说明 commissioning、protocol evaluation、report evaluation 的可选性和流程迭代性（约 lines 535--585）。
- RQ / PICOC / protocol：§5.3--§5.5 给出问题类型、PICOC、protocol 组件与 protocol evaluation（约 lines 707--946）。
- 检索与筛选：§6.1--§6.2 给出 search strategy、publication bias、search documentation Table 2、study selection、Cohen Kappa 与单研究者替代检查（约 lines 967--1304）。
- 质量评价：§6.3 给出 quality concepts、evidence hierarchy、bias types Table 4、quantitative checklist Table 5、qualitative checklist Table 6、quality data 的两类用途与限制（约 lines 1305--1705）。
- 数据抽取与综合：§6.4--§6.5 给出 extraction form、extractor/checker、duplicate publication、missing data、narrative / quantitative / qualitative / mixed synthesis、effect measures、forest / funnel plot、sensitivity analysis（约 lines 1710--2300）。
- 报告结构：§7 和 Table 8 给出 dissemination、report format、report evaluation、included/excluded studies、conflict of interest、appendices 等报告结构（约 lines 2312--2467）。
- Appendix 1：Table 9 是跨 6 个医学 / 社会科学系统综述指南来源的 process step cross-walk（约 lines 2635--2724）。
- Appendix 2：列出 2004--2007 年 6 月之间 15 篇 DARE ≥ 2 的 SE SLR；这是局部样本表，不是主体 guideline 的系统语料构建结果（约 lines 2725--2855）。
- Appendix 3：是一个 tertiary study protocol，包含 RQ、sources、纳排、DARE 质量评分、data collection、data analysis、dissemination；它是计划性 protocol，不是本文已经完成的 tertiary study 结果（约 lines 2860--3091）。

## 2. 总体裁决

- 原文类型：方法学 guideline / technical report。
- 主体样本单位：不是 primary study / included review，而是 guideline item、process step、protocol component、quality checklist item、extraction form field、synthesis / reporting component 等方法学构件。
- 降级口径：按 GUIDE §6.3.4 的 guideline / checklist / reporting standard 降级为 `methodological_seed`、`schema_seed`、`risk_only`；不进入主统计池。
- Appendix 2 边界：可作为“早期 SE SLR selected list”的局部 boundary anchor；可做文本级复算候选，但不得成为 survey_of_surveys 主分母，也不得写成 final quantitative finding。
- Appendix 3 边界：是 tertiary study protocol 示例；可提供 protocol / collection / quality / analysis 字段树，不能当作已完成 tertiary review 结果。

## 3. S1--S8 五分栏抽取

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定（中） | Executive Summary 与 §1 明确本文目标是提出 SE SLR guidelines；§2 定义 SLR / SMS / tertiary review；但本文自身不是 RQ-driven SLR/SMS。 | 根对象应写作“方法学指南任务”：为 SE 研究者提供 planning / conducting / reporting 的规范组件，而不是围绕自身 RQ 编码一组研究样本。 | 不进主统计池；仅作 `methodological_seed` / `schema_seed`。 | 核对 PDF 首页、报告号 EBSE-2007-01、Version 2.3、日期与机构；确认正式引用形态。 |
| S2 语料收集与筛选（中，降级） | 主体无完整数据库检索、初筛、全文筛、去重和分母链；§1.1 是 guideline 来源材料；Appendix 2 列 15 篇 DARE≥2 SE SLR；Appendix 3 给出计划性 tertiary protocol 的 sources、纳排和质量评价。 | 主体树中的 search / selection 是“指南建议和记录模板”；Appendix 2 是局部 selected list；Appendix 3 是 protocol 模板。三者不能合并为本文自己的完成型语料库。 | 主体不进主池；Appendix 2 只能是 boundary anchor；Appendix 3 不产生完成样本统计。 | 逐页核对 Appendix 2 是否恰为 15 行、DARE 分数是否完整；确认 Appendix 3 无执行后结果、无最终纳排流。 |
| S3 原生维度树 / 样本编码对象（中） | §4--§7 与 Tables 2--8 展开 SLR 阶段、RQ/PICOC、protocol、search documentation、selection、bias、quality checklist、data extraction、synthesis、report structure；Appendix 1/2/3 分别补 cross-walk、selected list、protocol。 | 应复原为“方法组件维度森林 + Appendix 2 小型局部编码池”，不是普通 included paper 的样本编码树。 | 不进主池；方法组件森林可作为字段设计种子。 | 核对 Tables 2--8 的标题、跨页完整性和层级；避免把指南枚举当 empirical categories。 |
| S4 字段级证据（中） | 原文提供多个字段容器：protocol 10 组件、Table 2 search documentation、Table 4 bias、Tables 5--6 quality checklist、Table 7 data collection form、§6.5 effect measures、Table 8 report structure、Appendix 2 topic/DARE 字段。 | 字段级结构丰富，但大部分是规范性模板 / checklist；Appendix 2 字段是局部样本表。字段可迁移为 schema，但不能自动成为统计证据。 | 不进主池；只允许作为字段模板或 A2a 抽取表候选。 | SUMMARY 当前如仍写 S4 “强”，应降为“中”；A2a 需精核 protocol 10 项、Tables 5--7 条目与 Table 8 章节。 |
| S5 维度模式演化（中） | §1.1 说明从医学、社会科学和 EBSE 经验引入来源；§1.2 说明指南从单作者、双作者更新、内部评审、外部专家评审到修订；front matter 有版本控制；Appendix 1 Table 9 做跨指南 process step cross-walk。 | 可复原为“跨学科指南来源 → SE 适配 → review/update”的演化树；它说明 guideline component 如何被迁移和调整，但不是开放编码生成的实证 taxonomy。 | 不进主池；可作为 schema lineage / methodological seed。 | 核对版本控制表、development team、Table 9 六个来源列；区分原作者适配意见与被转述来源观点。 |
| S6 统计分析（弱） | 主体说明 meta-analysis、effect measures、forest plot、funnel plot、sensitivity analysis 等统计方法；自身没有完成型统计分析。Appendix 2 可局部复算 15 篇 selected list 的 topic / DARE 分布。 | “统计”必须拆两层：方法枚举不是 empirical statistic；Appendix 2 是局部 selected-list 描述性复算，不代表 survey_of_surveys 目标语料。 | 不进主池；Appendix 2 只可作为局部候选观察，且不得进入 final quantitative finding。 | 复算 Appendix 2 前必须核对 PDF 跨页表格；确认是否存在另一个完成报告，不得把 15 篇写成主分母。 |
| S7 候选 finding（弱） | 主体给出方法学建议；§6.5/§7 等示例引用其他 SLR 的结论；Table 1 的跨学科相似度来自 Budgen et al.；Appendix 2 的主题 / DARE 分布只是局部边界。 | finding 层应写为“方法启发 / 二手候选 / Appendix 2 局部边界”，不是本文原创领域 finding。 | 不进主池；仅作写作背景、方法动机或待复核候选。 | 对二手 finding 追溯原始引用；确认 review / SUMMARY 不把 Appendix 2 观察写成普遍 SE SLR 结论。 |
| S8 研究者 / 作者质疑与裁决（中） | §1.2 和 development team 显示内部 / 外部 reviewer；§5.5 讲 protocol evaluation；§6.2.3 讲 Cohen Kappa、分歧解决、单研究者替代检查；§6.4.3 讲 data extractor / checker、consensus / arbitration；Appendix 3 计划单人选择加他人检查、一人抽取一人检查。 | 可复原为“裁决机制模板 + 指南构建评审过程”：有质量控制设计和 reviewers，但没有本文主体样本级裁决日志。 | 不进主池；可作为 audit workflow / reviewer override 机制种子。 | 核对 front matter reviewer 角色与 Appendix 3 checker 角色；避免把规范建议误写成本文实际执行的逐样本裁决。 |

## 4. 原生维度树 / 维度森林复原

```text
[forest-kitchenham-charters-2007] Kitchenham & Charters 2007 SE SLR 指南
│
├── G0 指南构建与来源谱系（guideline construction）
│   ├── 来源材料：Cochrane / Australian NHMR / CRD / Petticrew & Roberts / Fink / 相关医学与社会科学资料
│   ├── 经验来源：跨学科 evidence-based practice 专家会议 + Keele / Durham EBSE 项目经验
│   ├── 构建流程：单作者初稿 → 双作者更新 → EBSE 内部评审 → 外部专家独立评审 → 修订
│   └── 版本轨迹：0.1 到 2.3 的 document version control
│
├── G1 SLR 概念与类型树
│   ├── systematic literature review：secondary study，围绕 specific research question 识别、评价、解释证据
│   ├── systematic mapping study / scoping study：宽域证据分布与 evidence clusters / deserts
│   └── tertiary review：review of secondary studies
│
├── G2 SLR 流程树
│   ├── Planning：need、commissioning、research question、protocol、protocol evaluation
│   ├── Conducting：research identification、study selection、quality assessment、data extraction、data synthesis
│   └── Reporting：dissemination、main report formatting、report evaluation
│
├── G3 RQ 与 protocol 树
│   ├── question types：干预效果、频率/比率、诊断测试、病因/风险、可预测性、经济价值；SE 中 diagnostic 等价项不清
│   ├── PICOC：Population、Intervention、Comparison、Outcome、Context；另含 study designs
│   └── protocol components：background、RQ、search strategy、selection criteria/procedures、quality checklist/procedures、data extraction strategy、synthesis、dissemination、timetable
│
├── G4 语料收集与筛选模板树
│   ├── search strategy：digital libraries、journals、conference proceedings、grey literature、experts、reference lists
│   ├── search documentation：Table 2 的 data source × documentation 字段
│   ├── study selection：纳排标准、实际过滤轴、excluded studies list
│   └── reliability：Cohen Kappa、advisor / expert panel / test-retest 等替代检查
│
├── G5 质量评价树
│   ├── quality concepts：bias、internal validity、external validity
│   ├── evidence hierarchy：设计类型与问题适配；作者反对机械套医学 hierarchy
│   ├── bias taxonomy：selection / performance / measurement / attrition bias × protection mechanism
│   ├── quantitative checklist：Table 5，按 design / conduct / analysis / conclusions 与 study type 组织
│   ├── qualitative checklist：Table 6，18 个质性研究评价条目
│   └── quality data usage：用于 selection 或用于 analysis/synthesis；不建议简单质量分加权 meta-analysis
│
├── G6 数据抽取树
│   ├── form design：围绕 RQ 与 quality criteria；protocol 阶段定义并 pilot
│   ├── standard fields：reviewer、date、title、authors、journal、publication details、notes
│   ├── exemplar fields：Table 7 Maxwell 1998 extraction form，含 dataset、model、accuracy、statistical test、summary 等字段
│   └── procedures：two researchers / extractor-checker / consensus / arbitration / single-researcher alternatives
│
├── G7 数据综合与报告树
│   ├── synthesis modes：descriptive/narrative、quantitative/meta-analysis、qualitative、mixed
│   ├── effect measures：binary outcomes 的 odds/risk/OR/RR/ARR；continuous outcomes 的 mean difference/WMD/SMD
│   ├── presentation：tables、forest plot、funnel plot
│   ├── sensitivity：high-quality-only、by study type、by extraction difficulty、by experimental method
│   └── report structure：Table 8 的 title/authorship/structured summary/background/RQ/methods/results/discussion/conclusions/conflict/references/appendices
│
├── G8 Appendix 1 cross-walk 树
│   └── Table 9：Berkeley、Australian NHMR、Cochrane、CRD、Petticrew & Roberts、Fink 六类来源的 SLR process step 对照
│
├── G9 Appendix 2 局部 selected-list 编码池（降级）
│   ├── 样本单位：15 篇 2004--2007.06、DARE ≥ 2 的 SE SLR
│   ├── 字段：Author、Date、Title、Reference details、Topic type、Topic area、Quality score
│   └── 边界：局部历史列表；不可作为 survey_of_surveys 主统计池或最终经验发现
│
└── G10 Appendix 3 tertiary protocol 模板（计划性）
    ├── RQ：activity、topics、leaders、limitations
    ├── search process：指定 journals / conferences + named researchers
    ├── inclusion / exclusion：SLR / MA；排除 informal surveys、process-of-EBSE papers、非 peer-reviewed papers
    ├── quality：DARE 4 题及 Y/P/N 评分
    ├── data collection / analysis：source、year、classification、topic、authors、RQ、guideline reference、primary-study count、summary、quality score；counts by year/topic/org 等
    └── 边界：protocol 示例，不是完成的 tertiary study 结果
```

## 5. 需修改 review / evidence / SUMMARY 的 C/I/M 清单

| 等级 | 目标文件 | 问题 | 影响 | 建议修改 |
|---|---|---|---|---|
| C | -- | 未发现必须立即阻断的 Critical。 | -- | -- |
| I | `SUMMARY.md` | 当前覆盖矩阵中本篇 S4 仍显示“强”，但 `review.md` 已降为“中”，且本文字段来源主要是 guideline checklist / template，表图仍待 A2a。 | 若不降级，容易把字段级模板误读成最终统计证据，违反 GUIDE §6.4.8/§6.4.10 的文本级证据边界。 | 将本篇 S4 从“强”改为“中”，并保留“字段丰富但不进入主统计池；表图/Appendix 待 A2a”说明。 |
| I | `review.md` | §6.1 使用“统计观察”并给出 Appendix 2 的 6/15、40%、DARE 分布等表述；虽有边界说明，但标题和“可统计”字样仍可能被后续 agent 抽成主统计 finding。 | 可能把 Appendix 2 局部 selected list 写成 final quantitative finding。 | 将该小节改名为“Appendix 2 局部描述性复算 / boundary anchor”，所有比例前加“局部、非主池、文本级待 A2a”。 |
| I | `evidence_chain.md` | A.2/A.3 目前主要是 A1-DT 树级 claim map，S1--S8 的具体证据（§1.1/§1.2、Appendix 2、Appendix 3、Table 9）没有独立证据键；多处仍为“待 A2a”。 | review 的 S1--S8 若直接引用 evidence_chain，会缺少逐维度回链；尤其 S5/S8 容易混淆“指南构建评审过程”和“SLR 样本裁决机制”。 | A2a 或回填阶段新增 S1--S8 证据键，至少覆盖 source material / construction process、Appendix 2 selected list、Appendix 3 protocol、Table 9 cross-walk、extractor/checker 机制。 |
| I | `review.md` | 原生维度树主干较充分，但 G0“指南构建与来源谱系”没有作为树节点显式入树；S5 仅在四分栏中解释，S8 的实际 reviewer 证据与方法建议也未完全分离。 | 会削弱 S5 “维度模式演化”和 S8 “研究者/作者质疑与裁决”的可审计性。 | 在维度森林中补一棵“指南来源/构建/内部外部评审/版本控制”子树，并在 S8 明确区分 guideline construction reviewers 与 SLR execution checker。 |
| M | `review.md` | §6.1 的 DARE 句子含“Zannier 2006 / Glass 2004 不在最高？实际最高...”这类审计残留口吻。 | 不影响主体裁决，但会降低正式 review 可读性。 | 改为确定性、保守的文本级描述；若未精核则写“最高项待 A2a 复算”。 |
| M | `review.md` | 快速卡片 / 审计结论中有“主体：不适用（不适用）”“数据抽取（数据抽取）”“第 9 节风险登记”等不够干净或可能无对应章节的表述。 | 主要是可读性与可维护性问题。 | 后续清理重复词和不存在的章节引用。 |
| M | `evidence_chain.md` | A.2 中所有核心文本证据仍以 `not_verified` 和“短引见 review.md”管理，尚未精确到页码/表号/行号。 | 当前符合 A1-DT v2 冻结边界，但不适合升级为最终统计证据。 | A2a 精核时补精确页码、表号和原文短引；精核前不得提升证据强度。 |

## 6. 不足与后续接力

- 本轮没有视觉打开 PDF 逐页核对 Tables 2--9、Figures 1--2、Appendix 2 跨页完整性；所有涉及表格行数、比例、分数分布的结论仍是文本级候选。
- 本轮只产出单篇审计，不修改 `review.md`、`evidence_chain.md` 或 `SUMMARY.md`；上表 C/I/M 是返修清单，不是已完成修改。
- 本篇的可用价值主要是方法学脚手架和 schema seed；任何面向 Paper2 的定量结论必须回到后续 A2a/A2b 的主统计池样本，而不是从本 guideline 的方法枚举或 Appendix 2 局部列表外推。
