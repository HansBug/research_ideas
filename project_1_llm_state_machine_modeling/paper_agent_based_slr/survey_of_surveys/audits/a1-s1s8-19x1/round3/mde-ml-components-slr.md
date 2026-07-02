# mde-ml-components-slr：A1 S1--S8 round3 独立抽取审计

> 角色：A1 survey-of-surveys 单篇维度抽取 subagent。
> 范围：仅处理 `papers/mde-ml-components-slr`。未开启 sub-subagent。
> 重要边界：本报告是 A1 文本级 / 局部 PDF 视觉核验结果，只能作为 `schema_seed`、A2a 精核入口和 review/evidence/SUMMARY 返修建议；不得直接写成 Paper2 的 final quantitative finding。

## 1. 全文阅读依据

### 1.1 已读取文件

| 文件 | 本轮读取情况 | 用途 | 主要限制 |
|---|---|---|---|
| `bibtex.bib` | 完整读取 | 核对题名、作者、IST 2024、DOI `10.1016/j.infsof.2024.107423` | 未联网复核出版页 |
| `metadata.json` | 完整读取 | 核对本地 review_type、样本池资格标注、PDF URL 与仓库状态 | 元数据不是原文证据 |
| `paper_content.txt` | 按顺序通读 1--2123 行，覆盖正文、Appendix A/B 与参考文献入口 | 作为 S1--S8、Fig.5 主树、Table 1 gate、QA rubric、RQ--字段关系的主证据 | 图形/表格版式仍需 A2a PDF 精核 |
| `paper.pdf` | 局部视觉核验第 7 页：Fig.4、Fig.5、Fig.6 与 Table 2 起始 | 核对 Fig.5 feature tree 的节点、必选/可选标记和主干结构 | 未逐页核对 Fig.7--10、Table 3--9 |
| `review.md` | 完整读取 | 审计现有“维度树复原”与 `survey_of_surveys` S1--S8 表述 | 发现“单根树/维度小森林”表述需要统一 |
| `evidence_chain.md` | 完整读取 | 审计 A.1--A.4 证据链、C03/C04 结论与 A2a 限制 | 当前 A.2 多为 `not_verified` 泛定位，叶子级证据未完整迁入 |

### 1.2 关键原文锚点

- 摘要与 §3：本文是遵循 Kitchenham 指南的 SLR，检索 7 个数据库，初始 3934 条，最终 46 篇 primary studies。
- §3.1：4 个 RQ 分别问 motivation、MDE approaches/tools、evaluation、limitations/future work。
- §3.2 与 Table 1：I01--I04 纳入标准、E01--E10 排除标准，是筛选 gate schema。
- §3.3：检索式多轮 refinement；3934 → 3570 → 72 → 55 → 32，snowballing +14 → 46。
- §3.4：Google Form 40 个问题、5 个 section、23 short answer、10 long answer、2 checkbox、14 radio button；pilot 6 篇并与其他作者对照。
- §3.5 与 Appendix B Table 9：QA1--QA5，1--5 分和 NA；19 good / 15 average / 12 poor；低质量不排除。
- §4.1 与 PDF Fig.5：feature tree 根为 `MDE Solution for ML`，一层节点是 Goal、Domain、End Users、Modeling、Supported ML Aspects、Tool Support、Evaluation、Scalability、Responsible ML；Modeling 与 Tool Support 有二级/三级结构。
- §4.2--§4.5：RQ1--RQ4 不是四棵完整树，而是对同一 primary-study corpus 和 Fig.5/抽取字段的四个报告视角。
- §5：protocol review、cross-validation、pilot extraction、讨论达成共识；但无 Cohen $\kappa$、完整双人独立编码比例或 disagreement log。
- §6--§7：Discussion roadmap / recommendations 是作者解释性候选发现，不是本仓库目标领域的最终结论。
- §7：出现 “initial pool of 3,496 papers”，与摘要/§3.3 的 3934 冲突，应记录为原文内部数字冲突。

## 2. S1--S8 五分栏抽取

总体裁决：本文可作为 **schema/method 模式统计池候选**，因为它有系统检索、明确样本单位、抽取表、字段化结果、QA 和 RQ Answer Summary；但 MDE4ML 领域数字与 roadmap 只能作为方法脚手架样本，不得作为本仓库目标领域 final quantitative finding。A2a 前，具体频次和图表数值一律保持“文本级可用 / 最终统计前待 PDF 与数据仓库精核”。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要、§3 与 §3.1 明确本文是 MDE4ML 的 SLR，目标是分析 motivations、MDE solutions、evaluation techniques、benefits/limitations，并提出四个 RQ。 | 根对象是“面向机器学习组件的 MDE 方案（MDE Solution for ML）”；RQ1--RQ4 是报告视角，分别驱动动机、方案/工具、评价、限制/未来工作字段。 | **强（schema/method 候选）**：任务、scope、review type、样本单位均清楚；领域发现仅限 MDE4ML。 | 复核 RQ 原文页码和正式引文措辞；写 SUMMARY 时避免把 MDE4ML 领域结论迁移到 LLM4STM。 |
| S2 语料收集与筛选 | §3.2--§3.3 与 Fig.3/Table1：7 数据库、检索式、无时间限制、去重脚本、三轮筛选、snowballing；分母链为 3934 → 3570 → 72 → 55 → 32 → +14 → 46。 | Table 1 是独立 gate schema；样本单位为 P1--P46 primary studies。筛选 gate 不属于 Fig.5 主树的领域 feature，而是进入样本池前的门禁。 | **强（检索/筛选模式候选）**：分母链和 gate 明确；但 3934/3496 冲突限制最终定量使用。 | PDF 核对 Fig.3、Table 1、§7 3496 笔误；若数据仓库保留筛选表，应核对最终采用 3934 还是另有来源。 |
| S3 原生维度树/样本编码对象 | §4.1 明说 Fig.5 features derived from data extraction categories based on RQs；PDF 第 7 页 Fig.5 可见主树节点与必选/可选标记；Appendix A 列 P1--P46。 | 原生结构应写为“主 feature tree + 两个正交辅助 schema”：Fig.5 是主树；Table 1 是 gate；QA1--QA5 是质量 rubric。不要把 RQ1--RQ4误作四棵完整树。 | **强（schema 候选）**：Fig.5 主树可复原，gate/rubric 边界清楚；当前只到文本+局部 PDF 级。 | 完整视觉核验 Fig.5 层级与 optional/mandatory/OR/alternate 标记；review/evidence 中统一“单根主树 + 并列 gate/rubric”口径。 |
| S4 字段级证据 | §3.4 抽取表 40 问/5 section；Table 3--8 将 goal、ML technique、end user、contribution、framework/tool/metric 等字段映射到 P 编号；Table 9 给 QA 分数。 | 字段分支来自抽取表和 Fig.5，而不是 reviewer 主观分类。RQ1 对应 goal/domain/user/contribution/ML technique；RQ2 对应 modeling/tool/ML aspect；RQ3 对应 evaluation；RQ4 对应 limitation/future work。 | **强（文本级字段候选）**：字段和 P 编号明确，可进入 A2a 字段清单；A1 阶段不得升级为最终统计。 | 核验 GitHub data 是否含原始 Google Form/coding sheet；PDF 校正 Table 3--9 行列错位、P 编号、NA 语义。 |
| S5 维度模式演化 | §3.3.1 检索式多轮 refinement；§3.4 pilot 6 篇后 small updates；§5 提到 ML 术语不一致通过讨论达成共识。 | 可复原为“检索式 refinement + 抽取表 pilot 修订 + 术语裁决”的轻量演化链；没有完整 schema version history。 | **中（方法启发）**：可用于说明 schema 会在 pilot 后修订，但不足以统计字段演化路径。 | 查数据仓库是否有表单版本、pilot 记录或 change log；若没有，保持中，不升强。 |
| S6 统计分析 | §4 各 RQ 使用 Venn、bubble chart、分布图、频次表、RQ Answer Summary；§3.5 给 QA 分布。 | 字段表转为统计观察，再转为 RQ Answer Summary；Fig.7 是 goal/contribution × ML aspect 的关系型投影。 | **强（统计呈现模式候选）**：适合抽取“字段 → 图表/频次 → Answer Summary”的模式；数字 A2a 前不得 final。 | 逐项核验 Fig.4--10、Table 2--9 的数值、分母、百分比和图例；尤其图形 OCR/文本抽取不完整处。 |
| S7 候选 finding | RQ Answer Summary 与 §6 roadmap 提出 data first-class、solution focus、maturity、domain experts、terminology、scalability、responsible ML、evaluation rigor 等建议。 | finding 链条是“统计观察 → RQ summary → Discussion roadmap/recommendation”；这是作者解释性综合，非外部裁决后的最终事实。 | **强（候选 finding 方法池）**：可迁移 finding 生成模式；MDE4ML 具体 roadmap 不迁移为本研究结论。 | 为每条候选 finding 补分母、反证或限制；A2a 前只写 candidate_finding / boundary_anchor。 |
| S8 研究者/作者质疑与裁决 | §3、§5：其他作者 review protocol、cross-validation、pilot extraction、ambiguity discussion、threats；§3.4 又说明剩余论文主要由第一作者抽取。 | 可复原为作者级质量控制机制，而非完整审计裁决链。QA rubric 评估 primary-study 质量，不等于编码者一致性证据。 | **中（边界锚点）**：支持“有质控”，不支持“强研究者裁决日志”。 | 查 supplementary/data repo 是否有 disagreement log、inter-rater agreement、双人抽取比例；若无，review/SUMMARY 维持中。 |

## 3. 原生维度树 / 森林复原

### 3.1 树型裁决

本轮建议采用以下精确表述：

> 本文的原生编码结构是 **一个 Fig.5 主 feature tree，加两个正交辅助 schema（Table 1 筛选 gate 与 QA1--QA5 质量 rubric）**。如果使用“维度森林”一词，应限定为“主树 + gate + rubric 的轻量森林”；如果使用“单根树”一词，应限定为“单根主 feature tree”。四个 RQ 是对主树字段的报告视角 / section driver，不是四棵独立完整树。

理由：

1. Fig.5 有唯一根 `MDE Solution for ML`，并由 data extraction categories 派生，是原文面向 primary studies 的主要 feature tree。
2. Table 1 的 I/E 标准作用于样本纳入前门禁，不描述 MDE solution 的内部特征。
3. QA1--QA5 作用于 primary-study 质量评价，与 Fig.5 字段正交。
4. RQ1--RQ4 共享同一 P1--P46 样本单位和同一抽取表，不应拆成四个不相干语料池；但每个 RQ 对应不同字段分支和结果小节。

### 3.2 主 feature tree（Fig.5，文本级 + PDF 第 7 页局部核验）

```text
[主树根] MDE Solution for ML（面向机器学习组件的 MDE 方案；样本单位 P1--P46）
├── Goal（目标 / 动机）
├── Domain（应用领域）
├── End Users（目标用户）
├── Modeling（建模特征）
│   ├── Model Representation（模型表示）
│   │   ├── Textual（文本化）
│   │   └── Graphical（图形化）
│   ├── Model Type（模型类型）
│   ├── Model Level（CIM/PIM/PSM 等模型层级）
│   └── Modeling Language（建模语言）
│       ├── General Purpose Language（通用建模/编程语言）
│       ├── Domain-specific Language（DSL）
│       └── Language Extension（语言扩展）
├── Supported ML Aspects（支持的机器学习环节）
├── Tool Support（工具支持）
│   ├── Meta Tool（元工具）
│   ├── Transformations（模型转换）
│   │   ├── Model to Model（M2M）
│   │   └── Model to Text（M2T）
│   ├── Generated Artifacts（生成制品）
│   └── Automation Level（自动化程度）
│       ├── Partial Automation（部分自动化）
│       └── Full Automation（全自动化）
├── Evaluation（评价）
├── Scalability（可扩展性；cross-cutting concern）
└── Responsible ML（负责任机器学习；cross-cutting concern）
```

说明：PDF Fig.5 还给出 Mandatory / Optional / OR / Alternate 图例。当前报告只确认主干节点与部分层级，未逐项抽取每个节点的 feature-model 约束语义；A2a 应补 mandatory/optional/OR/alternate 的精确记录。

### 3.3 Table 1 gate schema（不要并入 Fig.5 主树）

```text
[辅助 schema A] Study-selection gate（筛选门禁；作用对象是候选论文）
├── Inclusion I01--I04
│   ├── I01：MDE for systems with ML components
│   ├── I02：全文可得
│   ├── I03：peer-reviewed / academic / with literature references
│   └── I04：英文
└── Exclusion E01--E10
    ├── E01/E02/E04/E10：主题边界排除（ML 无 MDE、非 ML 的 AI、AI4MDE、其他主题）
    ├── E03：pre-deployment model-based testing 排除
    ├── E05/E06/E07：篇幅、扩展版、信息不足排除
    ├── E08：secondary/tertiary 排除
    └── E09：vision / grey literature / book / poster / opinion / keynote / magazine / experience / comparison 等排除
```

### 3.4 QA rubric schema（不要当作 RQ 分支）

```text
[辅助 schema B] Primary-study quality assessment（质量评价量规；作用对象是 P1--P46）
├── QA1：aims clearly stated
├── QA2：solution clearly defined
├── QA3：measures used clearly defined（无 evaluation 时 NA）
├── QA4：implications for practice（无 evaluation 时 NA）
├── QA5：adds to literature（无 evaluation 时 NA）
├── 单项取值：1, 2, 3, 4, 5, NA
└── 聚合：good / average / poor（文本级记录为 19/15/12，A2a 前不作 final quantitative finding）
```

### 3.5 RQ 与字段分支关系

| RQ | 角色 | 主要字段分支 | 不应误读为 |
|---|---|---|---|
| RQ1 Motivation | 驱动 goal/domain/end-user/contribution/ML technique 等字段的报告视角 | Goal、Domain、End Users、Supported ML Aspects 的部分字段、Contribution 表 | 独立完整树或独立样本池 |
| RQ2 Approaches/tools | 驱动 Modeling、Tool Support、ML framework/library、generated artifact、automation 字段 | Modeling、Tool Support、Supported ML Aspects | 与 Fig.5 并列的新树 |
| RQ3 Evaluation | 驱动 evaluation context/method/metrics/datasets 字段 | Evaluation、ML metrics、MDE metrics、Dataset | QA rubric；RQ3 评价字段与 QA 质量量规不同 |
| RQ4 Limitations/future work | 驱动 limitation/future-work 分类 | Limitations、Future work、roadmap recommendation | Discussion roadmap 的最终裁决 |

## 4. 需修改 review / evidence / SUMMARY 的 C/I/M 清单

### C / critical

- **无确定 C 级问题**：当前 review 已多次声明 A2a 前不进入 final finding，且 evidence_chain 多数树级证据标为 `not_verified`。但如果后续 SUMMARY 或论文正文把本篇 A1 文本级数字（如 43/46、35/46、19/15/12、88%）直接写成 Paper2 final quantitative finding，应立即升级为 C，因为这会破坏研究证据链和结论可复现性。

### I / important

| 编号 | 影响文件 | 问题 | 学术风险 | 建议修改 |
|---|---|---|---|---|
| I-01 | `review.md`、`evidence_chain.md`、`SUMMARY.md` | 树型口径需要统一：现有 `review.md` 既说“单根维度树”，又在树代码块中说“维度小森林”；`evidence_chain.md` C03 写“Table 1 与 QA 并列 schema；不构成维度森林”。 | 后续 agent 可能把 RQ、gate、QA、Fig.5 主树混成一个事实真源，影响跨论文树型统计。 | 统一成“Fig.5 单根主 feature tree + Table1 gate + QA rubric 两个正交辅助 schema；可称轻量森林但必须说明主树/辅助 schema 边界”。 |
| I-02 | `review.md` | `RQ1--RQ4 直接对应四棵结果子树` 这类表述容易被误读为四棵完整树。 | 会违反 GUIDE §6.3 多 RQ 规则：多 RQ 共享样本单位和抽取表时，应写主树下字段分支 / 报告视角，而非强行森林化。 | 改为“RQ1--RQ4 是共享 P1--P46 样本与抽取表的四个报告视角，每个视角驱动若干字段分支”。 |
| I-03 | `evidence_chain.md` | A.2 `ev-*-tree` 的来源混入三路审计结果；原文证据仍是泛定位“待 A2a”，未把 PDF 第 7 页 Fig.5、Table1、QA rubric 的具体锚点拆成独立证据。 | 审计输入可能被误当原文证据；叶子/辅助 schema 的证据回链不足，削弱可复验性。 | 新增或后续 A2a 拆分 `ev-fig5-main-tree`、`ev-table1-gate`、`ev-qa-rubric`、`ev-form-40q`；审计结果只作 corroboration，不作主证据。 |
| I-04 | `SUMMARY.md` | `统计池资格` 若只写“是”，读者可能误解为 A1 已允许进入最终定量统计。 | 违背 GUIDE §6.4.10 与本任务“严禁 A1 文本级结果写成 final quantitative finding”。 | 对本篇统一写“schema/method 候选：是；目标领域结论池：否；A2a 精核前不得 final quantitative”。 |
| I-05 | `review.md`、`SUMMARY.md` | S4/S6 写“强”时应显式带“文本级强 / A2a 前不 final”的限定。 | 图表和表格错位未精核时，强等级可能被误读为最终数字证据。 | 在 S1--S8 表和矩阵中保留“强（文本级）/具体数值待 PDF 与数据仓库精核”。 |
| I-06 | `review.md`、`evidence_chain.md` | 3934 vs 3496 原文冲突虽已记录，但应在所有使用分母的 summary/claim 中绑定冲突说明。 | 若后续引用 3496 或混用两个初始池数字，会直接污染检索分母链。 | 正式采用 §3.3 与摘要的 3934，同时在 A.2/A.3/SUMMARY 对应行保留 §7 3496 疑似笔误。 |

### M / minor

| 编号 | 影响文件 | 问题 | 建议 |
|---|---|---|---|
| M-01 | `review.md` | 少数小节仍混用“Stalkeholder”等拼写或中英夹杂过多。 | 后续中文化时保守修正，不改变事实口径。 |
| M-02 | `review.md` | 叶子表较长且部分字段名如 `L-rq2-工具` 中英/中文混合不完全一致。 | A2a 迁入统一叶子表时统一 stable id 命名；当前不阻塞。 |
| M-03 | `evidence_chain.md` | A.4 仍写结构门禁命令状态“已通过 / 待最终 PR 前复验”，对 round3 读者不够具体。 | 后续 PR 前补一次实际命令输出或手工复验时间戳。 |
| M-04 | `SUMMARY.md` | 本篇在 S1--S8 矩阵中内容较长，阅读负担高。 | 可压缩为“结论 + caveat”，细节回链本 round3 审计和 `review.md`。 |

## 5. 本轮不足与交接

- 已局部打开 PDF 核对 Fig.5，但没有逐页核验 Fig.7--10 和 Table 3--9；所有具体频次只可作为文本级候选。
- 未联网打开 `MDE4ML-SLR-Data` GitHub 仓库，不能确认 raw Google Form、coding sheet、license、commit 或当前可访问性。
- 未修改 `review.md`、`evidence_chain.md`、`SUMMARY.md`；本报告只写入 round3 指定文件。
- 后续若回填，应优先处理 I-01/I-02/I-04，避免“RQ 四棵树”和“A1 文本级 final quantitative finding”两类误读。
