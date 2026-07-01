# Systematic Reviews in Requirements Engineering: A Tertiary Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic Reviews in Requirements Engineering: A Tertiary Study |
| 年份 | 2014 |
| 类型 | tertiary study |
| 出版形态 | 工作坊 |
| 期刊/会议/预印本 | [EmpiRE](https://empire2014.wordpress.com/) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| CCF 复核状态 | 非 CCF venue / workshop |
| 来源等级 | EmpiRE 2014 workshop；非顶级会议；IEEE DOI |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | Requirements Engineering 领域 tertiary study |
| SE 子领域 | Requirements Engineering |
| A1 角色 | 领域专门化 tertiary study 样本，用于验证“特定 SE 子领域如何定义 topic / quality / impact / practitioners”。 |
| 是否目标证据池 | 否。 |
| schema 历史观察 | 暴露“领域专门化”字段：目标 SE 子领域、topic taxonomy、教育/实践影响。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 目标是给出 RE 领域 SLR 的 comprehensive overview，并评估 quality、topics、impact for education/practice。 | `paper_content.txt` Page 2 摘要。 | 可迁移为“特定 SE 子领域的综述元模型”。 | RE 子领域样本，不能直接代表 testing/MDE/LLM4SE 等主题。 |
| dimension pattern | 维度包括 automated/manual search、53 distinct reviews、64 publications、quality、topics、education/practice relevance。 | `paper_content.txt` Page 2 摘要与方法段。 | 可迁移到 A2a 的领域专门字段。 | 教育/实践影响字段可参考，但字段树需由目标主题研究者裁定。 |
| finding pattern | finding 关注 RE SLR 数量、主题与质量；具体结论需进一步深读结果章节。 | `paper_content.txt` Page 2 摘要。 | 候选可迁移。 | 当前只读摘要级结果，具体 finding 需 A2a 深读结果章节。 |
| evidence presentation pattern | 使用 distinct reviews / publications 分母、自动与手工搜索来源、质量评估结果。 | `paper_content.txt` Page 2 摘要。 | 可迁移为候选池和去重字段。 | distinct reviews/publications 分母可迁移，细节需 PDF 表格核对。 |
| validity / threat pattern | 本轮未完整定位 threat section；需 A2a 深读。 | `paper_content.txt` Page 2--9。 | 待核验。 | threat section 未完整定位，不能作为已饱和 threat 模板。 |
| report structure pattern | 短 workshop tertiary study，结构紧凑；适合压测短文档字段缺失情况。 | `paper_content.txt` Page 1--9。 | 可迁移为“短论文也要记录缺失字段”。 | 短 workshop 结构紧凑，不能当成完整期刊综述结构。 |

## 3. 对 PR-A1 schema 的启发

1. `target_se_subfield` 应成为候选字段，避免把所有 SE SLR 混为一个领域。
2. `publication_count` 与 `distinct_study_count` 应分开，避免多篇报告同一 SLR 造成重复。
3. 需要 `education_practice_relevance` 字段，承接导师强调的 research finding / practical impact。

## 4. 待复核

- PDF 表格与质量评价细节待人工核对。
- EmpiRE 是 workshop，不能写成顶级 venue。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 将 Requirements Engineering 二次研究作为 tertiary study 对象。 | 可迁移“SE 子领域 tertiary”元模型。 |
| A1-M1 语料收集与纳排 | 提供 RE 三级研究的搜索与选择流程。 | EmpiRE workshop 来源需标注非顶级 venue。 |
| A1-M2 研究对象与主题语义 | 提供 RE 子领域 topic / evidence 分类样本。 | 可作为 RE 子领域 模式种子。 |
| A1-M3 方法 / 技术 / 干预 | 主要关注 RE review 类型和主题，不是具体技术干预。 | 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 可迁移 quality / reporting / evidence-presentation 字段。 | 表格需后续核对。 |
| A1-M5 统计分析就绪 | 可形成 RE 二次研究 的分布统计。 | 小样本与 workshop 语境需降级。 |
| A1-M6 research finding 形成与裁决 | 可从 RE review 覆盖缺口形成候选 finding。 | 不支撑 Paper2 目标领域结论。 |

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__codex.md](../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__codex.md)、[../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__claude.md](../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__claude.md)、[../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__deepseek.md](../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/re-tertiary-study-2014.md](../../audits/a1dt-v2-19x3/adjudications/re-tertiary-study-2014.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `re-tertiary-study-2014` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是。一次性读取全文 9 页 OCR 文本（行 1–967），已覆盖摘要、计划（Planning）、Execution、RQ1–RQ3 结果、Limitations、Conclusion、References 与 Appendix A 完整 S1–S53 名录 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`bibtex.bib`（@inproceedings, EmpiRE 2014, pp.9–16, DOI 10.1109/EmpiRE.2014.6890110）与 `metadata.json` 均已读取，并交叉核对 venue / 年份 / SLR 单位口径 |
| 是否打开或核对 `paper.pdf` | 否。本轮只做 `paper_content.txt` 文本级审计；Figure 1–4 的视觉版面、QA score 直方图分布的精确柱高、Table III–VI 的版面对齐需 A2a 用 `paper.pdf` 进一步核对 |
| 原文类型 | tertiary 研究（系统映射 tertiary 研究；按 §II 标题"系统映射 Tertiary Study"，作者明确按 Kitchenham EBSE 指南 执行）|
| 被编码样本单位 | **distinct SLR（研究）**。作者把"同一项 SLR 的多份发表"用 `S-ID + [A][B][C]` 合并为一个 研究；分子粒度是 研究，分母两套：64 publications 与 53 studies |
| 样本数量 / 分母 | 53 distinct SLR（含 12 SMS、1 元分析（meta-analysis）、其余 conventional SLR）/ 64 publications（31 conf + 16 journal + 4 workshop + 4 tech 报告 + 8 thesis + 1 unknown）；QA 仅在 51 个 研究 上施加（S3、S8 全文不可获得） |
| 原生树类型 | **维度森林**：①抽取表（出版元数据（publication metadata）+ 原始研究数量（#PS）+ 关注点（focus））；②scope 分类（Table IV）；③topic-group 分类法（Table V）；④QA rubric（Table I, QA1–QA4 三档 是/Partial/否）；⑤citation/impact 评估（Table VI）；⑥缺口（gap） 分类法（anomalies / lack-of-PS / ignored-areas，§III RQ3）；⑦publication-type 分类（Table III） |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

- 实读文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`（全 9 页 967 行）、`review.md`（221 行）。技能文件读取 `reviewer-guidelines.md` 全文、`ai-research-writing-skill/SKILL.md` 与 `research-planning/SKILL.md` 关键段落。
- 仅文本级审计；以下 4 处仍需 A2a 用 `paper.pdf` 视觉核验：
  1. Figure 1（yearly distribution）的柱高 vs §III 描述"2009 之后骤增"；
  2. Figure 2 质量-score distribution（"42/51 ≥ 2"）的柱高；
  3. Figure 3 QA1–QA4 各档计数（OCR 把 y 轴数列读成"`0510 15 20 25 30 35 40 45`"，已断版）；
  4. Figure 4 averaged QA score-vs-year 曲线的具体年份取值。

关键原文证据锚点（编号供后文 A.2 引用）：

| # | 章节 / 表 | 行范围 | 短引或释义 |
|---|---|---|---|
| E1 | §I Abstract / Introduction | L23–105 | "53 distinct systematic reviews ... reported in 64 publications"；目标含 质量 / coverage / 缺口（gaps） |
| E2 | §II.A 计划（Planning） — 3 个 RQ | L117–123 | RQ1=areas covered；RQ2=质量 of published SLR；RQ3=缺口（gaps） in coverage |
| E3 | Table I QA rubric (QA1–QA4, 是/Partial/否, 1/0.5/0) | L147–178 | DARE 改编；4 项 × 3 档；citation 来自 [8,9,11] |
| E4 | §II.A 搜索串与 5 库 + snowball + manual venue 扫 | L184–220 | IEEE/ACM/SD/GS/EI Compendex + snowball [8-11] + RE/EASE/ESEM/REFSQ/REJ/ESE/IST 自 2004 |
| E5 | §II.A 三项 纳入标准 | L226–230 | 英语 / SLR-SMS-meta / RE 焦点 |
| E6 | Table II 检索执行汇总 | L273–288 | 5 库 267→91→58→+6→64 publications→53 studies |
| E7 | Table III 发表类型 | L317–331 | 31/16/4/4/8/1 |
| E8 | Table IV scope-of-RE-SLR 6 档 | L364–375 | state-of-the-art 33, 方法 7, techniques 7, 工具 4, 框架 1, 技术 1 |
| E9 | Table V topic-group × focus × #PS × year | L376–429 | 18 个 topic group；含 "Non-Functional 需求","Complete RE 过程","Model Driven Development","Knowledge Management and RE","RE in GSD" 等 |
| E10 | §III RQ2 + Figures 2/3/4 | L433–479 | 42/51 ≥2；QA3/QA4 半数被忽略；年度均分 2009 后下降 |
| E11 | Table VI Top-10 cited | L482–493 | S-ID × GS Citations × Pub channel × QA Score |
| E12 | §III RQ3 三类 缺口（gap） | L505–576 | (1) anomalies in #PS, (2) lack of PS, (3) ignored RE areas with reference to 路线图 [1][2] |
| E13 | §IV Limitations | L577–615 | 检索覆盖缺口、S40 缺 venue 元信息、topic grouping 主观、QA rubric 受 EBSE 指南 限制 |
| E14 | Appendix A S1–S53 名录 | L697–967 | 完整 reference + 引用次数；含 [A][B][C] 子发表合并方式 |

### 2. 样本单位与字段来源判定

1. **纳入对象**：focus 在 RE 任一子主题的 二次研究（SLR / SMS / 元分析（meta-analysis）），由 研究 而非 publication 计数。
2. **系统性**：是。作者明确遵循 Kitchenham EBSE 指南（[7]），有 protocol、5 库自动检索、snowball、手工 venue 扫、inclusion/exclusion、QA、数据抽取与 主题分析（[12]）。
3. **字段来源**：
   - publication 元信息字段（title / authors / year / 发表类型 / venue / citations）—— §II.A 第 3 页明确"based on the guidance provided in [12], we extracted publication details"；
   - SLR 抽取字段（# of 原始研究, focus of SLR）—— 同段；
   - topic grouping —— §II.A "主题分析 of titles and abstracts"，Table V 第一列；
   - QA rubric —— Table I 4 项，源自 DARE 经 [8,9,11] 改编；
   - publication-level impact —— Google Scholar 引用次数（2014-05-19 截止）。
4. **RQ↔样本单位关系**：3 个 RQ 都以 研究 为单位（53 SLR），RQ1=topic 分布，RQ2=QA 得分分布（51 研究），RQ3=候选 缺口（gap） 列表；RQ 是字段用途与结果组织口径，不是 模式 根。
5. **降级判定**：无需降级。系统检索、QA、抽取表、分类法 均齐全。但 S40 缺 publication 元信息、S3/S8 全文不可得，需以 `missing` 缺失值语义记录。

### 3. 原生样本编码维度树 / 维度森林

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
根节点：需求工程三级研究抽取模式（RE tertiary 抽取 模式；样本单位 = 去重后的 SLR 研究（distinct SLR 研究））
│
├── F1 [发表元数据]  发表级字段（发表元数据；按发表条目，64）
│   ├── 标题                              自由文本
│   ├── 作者                            自由文本
│   ├── 年份                               整数 2006–2014
│   ├── 发表类型                   枚举{会议（conference）、期刊（journal）、工作坊（workshop）、
│   │                                            技术报告（technical report）、学位论文（thesis）、未知（unknown）}            ← Table III
│   ├── 发表源名称                         自由文本 (RE, REJ, IST, ESE, EASE, …)
│   ├── 谷歌学术引用数                  整数 (cut-off 2014-05-19)                   ← Table VI
│   └── 研究编号分组                  S-ID with suffix [A][B][C]
│
├── F2 [SLR 抽取信息]  SLR 级字段（SLR 抽取信息；按研究条目，53）
│   ├── 原始研究数量 (#PS)    整数 ∈ [5, 4089] ∪ {NF, NM}                 ← Table V
│   ├── SLR 关注点                       自由文本                                      ← Table V 第 3 列
│   ├── SLR 类型                           枚举{常规 SLR（conventional SLR）、SMS、元分析（meta-analysis）}      ← §III
│   └── 原始研究时间窗                  可选整数区间（optional integer interval） (e.g., 1996–2007)
│
├── F3 [主题分组]  主题分类法（Topic Grouping；按研究条目；主题可多归属，S26/S39 标 *）
│   主题组 取值 ∈ {                                                                       ← Table V col 1
│       非功能需求,
│       完整需求工程过程,
│       模型驱动开发,
│       知识管理与需求工程,
│       全球软件开发中的需求工程,
│       软件产品线中的需求工程,
│       需求管理,
│       多智能体系统,
│       需求复用,
│       基于价值的需求工程（Value based RE）,
│       虚拟现实系统,
│       Web 工程,
│       需求工程中的创造力,
│       需求获取,
│       干系人与用户,
│       需求优先级排序,
│       元建模,
│       软件需求规格说明,
│       需求验证 / 确认 / 评价,
│       需求追踪,
│       需求变更管理,
│       需求工程教育,
│       移动学习,
│       需求工程检查清单
│   }  → 24 个观察到的分组（group）；重叠归属（overlap）用 "*" 注脚
│
├── F4 [范围分类]  方法学外延（范围分类（Scope 分类）；按研究条目）                                     ← Table IV
│   研究范围（scope，后续简称“范围”）∈ 枚举{
│       RE 领域现状（state of the art within RE）、方法、技术（techniques）、
│       工具、框架、技术
│   }
│
├── F5 [质量量规]  DARE 改造后的 4 题质量评价（质量量规（质量量规）；按研究条目，n=51，S3/S8 排除）                  ← Table I
│   ├── QA1 纳入 / 排除标准  取值 ∈ {是（Yes）=1, 部分（Partial）=0.5, 否（No）=0}
│   │     - 是（Yes）：显式定义纳排标准（explicit IE criteria defined）
│   │     - Partial：隐式研究筛选（implicit 研究 selection）
│   │     - 否（No）： no criteria defined
│   ├── QA2 检索 空间充分性（空间充分性）        取值 ∈ {是（Yes）=1, 部分（Partial）=0.5, 否（No）=0}
│   │     - 是（Yes）： ≥4 DL + extra strategies
│   │     - 部分（Partial）： 3–4 DL, no extra
│   │     - 否（No）： ≤2 DL or restricted
│   ├── QA3 原始研究质量评价（原始研究质量评价）     取值 ∈ {是（Yes）=1, 部分（Partial）=0.5, 否（No）=0}
│   │     - 是（Yes）：显式描述并应用 QA（explicit QA described & applied）
│   │     - 部分（Partial）： implicit QA
│   │     - 否（No）： no QA
│   ├── QA4 原始研究信息充分性（原始研究信息充分性）            取值 ∈ {是（Yes）=1, 部分（Partial）=0.5, 否（No）=0}
│   │     - 是（Yes）： complete info per PS
│   │     - 部分（Partial）： summary
│   │     - 否（No）： 未说明
│   └── 总分（total_score）取值 ∈ {0, 0.5, …, 4}
│
├── F6 [检索执行]  检索执行（检索执行；按来源聚合，per source aggregate；非按研究条目）                            ← Table II
│   检索来源（source）取值 ∈ {Google Scholar, IEEE Xplore, ACM DL, Science Direct, EI Compendex,
│             二次检索（secondary search）[8,9,10,11]、手工检索 REJ（manual REJ）、手工检索 ESE（manual ESE）}
│   ├── 找到论文数（papers_found）：整数
│   └── 纳入论文数（papers_included）：整数
│
└── F7 [缺口分类法]  派生候选发现（derived 候选发现）；按缺口条目（per 缺口（gap）-item），不是按研究条目）           ← §III RQ3
    缺口类型（gap type）∈ 枚举{
        原始研究数量不一致（anomaly: inconsistent primary-研究 计数）,
        缺少原始研究（lack of 原始研究）,
        被忽视的需求工程领域（ignored RE area）
    }
    + 交叉引用目标对象（cross reference target）取值 ∈ {
        Nuseibeh&Easterbrook 2000 路线图[1],
        Cheng&Atlee 2007 路线图[2]
    }
```

### 4. 叶子维度表（核心叶子，足以重写 review.md）

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leaf-orig-publication-type` | 出版类型 | F1 | Table III | 每篇 publication 的载体类别 | 会议（conference）/ 期刊（journal）/ 工作坊（workshop）/ 技术报告（tech_report）/ 学位论文（thesis）/ 未知（unknown） | 完整枚举（6 档，含 unknown 兜底）| `unknown`：S40 缺 venue 信息 | 类型频次分布 | 出版类型 vs QA 得分交叉表 | E7 | 通用：任何 SLR/tertiary 都可复用此 6 档枚举 |
| `leaf-orig-slr-type` | 综述子类型 | F2 | §III L311–314 | 53 个 研究 内部子类型 | 常规 SLR（conventional_SLR） / SMS / 元分析（meta-analysis） | 完整枚举（3 档）| 不允许缺失 | 53 研究 的子类型分布（12 SMS, 1 meta, 40 SLR）| 不同子类型 QA 表现差异 | E1, E2 | 可迁移 |
| `leaf-orig-pub-citation` | 引用数 | F1 | Table VI + Appendix A | Google Scholar 引用（2014-05-19 截止）| 整数 ≥ 0 | 数值 | `0` 与"未查到"需区分（Appendix 中均写具体数字） | 中位数 / Top-N | 高引 SLR 是否同时高 QA（Table VI 反证：S2[A] cite=154 但 QA=3, S46 cite=41 QA=1.5）| E11, E14 | 受时间窗影响，可迁移结构 |
| `leaf-orig-ps-count` | 纳入 原始研究 数 | F2 | Table V col `# of PS` | 该 SLR 自报的 PS 总数 | 整数 ∈ [5, 4089] ∪ {NM, NF} | 数值或区间 + 哨兵 | `NM`=未提及；`NF`=not found | 直方图 / 极差 | "anomaly" 发现 直接依赖该字段（S1=8 vs S4=240 同主题）| E9 | 高度可迁移，但 #PS 不一定反映工作量 |
| `leaf-orig-focus-text` | SLR focus | F2 | Table V col 2 | SLR 自报研究焦点的自由文本 | 自由文本 | 自由文本加理由 | 不允许缺失 | thematic clustering 输入 | topic grouping 上层来源 | E9 | 文本字段，需分类才能统计 |
| `leaf-orig-topic-group` | 主题分组 | F3 | Table V col 1 | 由作者 主题分析 形成的 24 个 topic group | 24 项枚举（见 §3 F3 列表）| 层级枚举（开放，可由后续工作扩充）| `overlap` 用 "*" 标记 (S26/S39) | 主题覆盖直方图 | RQ1 主结果；RQ3 ignored area 反向推导 | E9 | 不可饱和（作者自承"neither exhaustive nor complete"）；A2a 不应当成封闭枚举使用 |
| `leaf-orig-scope` | scope-of-RE 分类 | F4 | Table IV | SLR 评估对象的方法学外延 | state_of_the_art / 方法 / techniques / 工具 / 框架 / 技术 | 完整枚举（6 档）| 不允许缺失 | 6 档分布（33/7/7/4/1/1）| 是否多数 SLR 仅描述现状缺乏方法学评价 | E8 | 可迁移；6 档自身较稳定 |
| `leaf-orig-qa1` 至 `leaf-orig-qa4` | DARE QA 四题 | F5 | Table I | DARE 改编 4 题 | 每题 ∈ {是（Yes）=1, 部分（Partial）=0.5, 否（No）=0} | 完整枚举（每题 3 档）| `excluded`：S3/S8（n=51 而非 53）| 各题档次频次（Figure 3）；总分分布（Figure 2）| QA3/QA4 半数被忽略 → 候选发现 | E3, E10 | 可作为 RE 之外 SLR-QA 评估的复用模板 |
| `leaf-orig-qa-total` | QA 总分 | F5 | §III RQ2 + Figure 2 | 4 题之和 | ∈ {0, 0.5, 1.0, 1.5, …, 4} | 数值 | 同 QA1–QA4 | "42/51 ≥ 2"；按年度均分 trend | 整体趋势 → final 候选发现 (decline since 2009) | E10 | 可迁移 |
| `leaf-orig-search-source` | 检索源 | F6 | Table II | 检索源与命中量 | 5 库 + 4 secondary + manual venues | 关系值 / 数值 | snowball 来源单独列 | 单源命中率 / 漏检风险 | secondary 找到 6 篇（占 9.4%）→ 单一检索口径不充分 | E4, E6 | 可迁移 |
| `leaf-orig-gap-type` | 候选 缺口（gap） 类别 | F7 | §III RQ3 | 三类 缺口（gap） | 异常（anomaly）/ 缺少原始研究（lack_of_PS）/ 被忽视领域（ignored_area） | 完整枚举（3 档）| -- | 每类 缺口（gap） 列表大小 | RQ3 主结果 + 与 路线图[1,2] 对照 | E12 | 可迁移作 缺口（gap）-分类法 模板 |
| `leaf-orig-路线图-ref` | 路线图 参照 | F7 | §III RQ3 + Refs [1][2] | RQ3 与既有 路线图 的对照锚 | {Nuseibeh&Easterbrook2000, Cheng&Atlee2007} | 外部分类法引用 | -- | 是否覆盖 路线图 topic 的二值矩阵 | 列出 4 个 covered + 4 个 not-covered + 2 个 Nuseibeh-area not covered | E12 | 不可迁移到 RE 之外（路线图 是 RE-specific）|
| `leaf-orig-limitation-text` | 自报 limitations | ROOT | §IV | 作者自报的 4 类局限 | 4 项（检索完整性 / S40 元信息缺失 / topic-grouping 主观 / EBSE 指南 限定）| 自由文本加理由 | -- | 作 威胁-to-效度 字段 | 反证当前 #PS 异常 发现 的强度 | E13 | 通用 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel-grouping` | publication（F1）| `belongs_to_研究` | 研究（F2） | S-ID（S1–S53）+ 后缀 [A][B][C] | 不允许缺失 | E14 | 把 64 publications 归并到 53 研究 |
| `rel-topic-overlap` | 研究 × topic_group | `is_overlap_with` | 另一 topic_group | 至少出现 1 次（S26/S39 同时属于 Knowledge Management 与 RE in GSD）| 默认无 overlap | Table V 注脚 "*" | 提示 topic_group 非互斥 |
| `rel-citation-vs-qa` | 研究 | `top_cited_with_qa` | (citation, qa_total) 二元组 | 数值对 | -- | E11 | Table VI 直接验证"高引≠高质量" |
| `rel-gap-vs-roadmap` | 缺口（gap） | `references_roadmap` | roadmap_topic | covered / not-covered | -- | E12 | 桥接 RQ3 与外部分类法[1][2] |
| `rel-search-source` | source | `feeds` | publications_found / included | 数值对 | -- | E6 | 检索漏检反证 |

### 6. 统计观察、候选发现 与 最终发现边界

**A. 字段/统计表直接支撑的统计观察**（可在 53/51/64 分母下重算）：

1. 出版类型分布：31 conf + 16 journal + 4 workshop + 4 tech 报告 + 8 thesis + 1 unknown = 64（E7）。
2. SLR 子类型分布：12 SMS + 1 元分析（meta-analysis） + 40 conventional SLR = 53（E1，§III）。
3. scope 分布：33/7/7/4/1/1（E8）。
4. #PS 极差：max=4089 (S42 元分析（meta-analysis） 1963–2006), min=5 (S27)；>200 共 4 篇（S21, S25, S24, S4）；100–200 共 5 篇；<10 共 4 篇（E9, §III L344–363）。
5. QA：42/51 ≥ 2；QA3/QA4 各档分布见 Figure 3（待 A2a 视觉读取精确柱高）。
6. 年度发表量：2006–2014，2009 后骤增（Figure 1，A2a 待核）。
7. citation Top-10：见 Table VI（E11）。

**B. 候选发现（discussion / RQ3 / limitations）**：

1. RE SLR 的整体 QA 年均分自 2009 起下降，与 SE-wide tertiary [8,9] 的"QA 上升"形成对比（§III + Figure 4，候选趋势发现（candidate trend 发现），需视觉核 Figure 4 + 跨论文反证）。
2. 高引 ≠ 高 QA：S2[A] cite=154 但 QA=3；S46 cite=41 QA=1.5（E11）。
3. #PS 内部矛盾：S1 vs S4（同 prioritization）、S24 vs {S4,S21,S25}（state-of-the-art 子集异常）（E12 ①）。
4. RE 子主题覆盖 缺口（gap）：未被任一 SLR 覆盖的 = {需求 Scaling, RE for self-management systems, system environment effects, RE research-in-practice effectiveness, conflict resolution, requirements negotiation, goal-oriented RE, RE in law, requirements modeling notations}（E12 ③）。
5. 半数 SLR 忽略 QA3/QA4（E10），可能威胁结果可靠性。

**C. 对 Paper2（LLM 状态机建模综述）可迁移的方法学启发**：

- F1+F2 抽取表 + F5 DARE rubric 是 RE 之外仍稳定的元结构；可作 Paper2 single-paper 抽取 form 的模板骨架（publication-level vs 研究-level 分层；统一处理 [A][B][C] 同 研究 多发表）。
- F7 三类 缺口（gap） 分类法（anomaly / lack-of-PS / ignored-area）与 路线图 cross-ref 模式可作 Paper2 缺口（gap）-analysis 章节的输出形态参考。
- §IV "Limitations of the 研究" 4 类局限可作 威胁-to-效度 复用清单。
- S40 缺 venue 元信息但仍纳入的做法 → "不完整元信息可保留但应显式标注"的处理范例。

**D. 绝不能迁移**：

- RE-specific topic 分类法（24 项）、scope 6 档、Nuseibeh / Cheng-Atlee 路线图 的具体 topic 名单 —— 这些是 RE 领域 模式，对 LLM4SE / 状态机建模没有直接映射。
- "QA 自 2009 起下降"这一年度趋势仅限 RE SLR 子集，不能外推到 SE-wide 或其他子领域。
- citation Top-10 名单是 2014-05-19 快照，已过时。

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
