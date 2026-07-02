# A1 round3：petersen-2008-systematic-mapping 单篇 S1--S8 与原生维度森林审计

> 本文件是 A1 survey-of-surveys 单篇维度抽取 subagent 的**独立文本级审计**，只服务后续主线程裁决与 A2a 精核；不得把本文中的 A1 核对值直接写成 Paper2 的 final quantitative finding。

## 0. 执行边界与全文阅读依据

- 工作对象：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/petersen-2008-systematic-mapping/`。
- 已读文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`、`evidence_chain.md` 全文。
- PDF 核对：使用 `pdfinfo` 确认为 10 页；对 `paper.pdf` 第 5 页 Figure 3 和第 7 页 Table 5 做了版面级视觉核对，并用 `pdftotext -layout/-bbox-layout` 辅助核对数字和列对齐。
- 未开启 sub-subagent；未读取其他论文内容；未修改 `review.md`、`evidence_chain.md` 或 `SUMMARY.md`。
- 关键原文依据：Abstract 定义 SMS 以 classification scheme 和 category frequencies 为核心；§2/Figure 1 给出五步 SMS 流程；§2.1--§2.3 给出两个 mapping 示例的 RQ、检索、纳排；§2.4/Figure 2/Table 3 给出 keywording 与三 facet 分类方案；§2.5/Figure 3 给出抽取表、short rationale、bubble plot；§3/Table 4--5 给出 10 篇 SE SLR 样本与特征表；§4--§5 给出 map/review 互补与指南建议。

## 1. 一句话裁决

Petersen 2008 是 SMS 方法学种子，不是普通主题领域统计样本；原生结构应复原为四棵树组成的**维度森林**：Tree A 为 10 篇 SE SLR 特征化表，Tree B 为 2 个 mapping 示例对比，Tree C 为处方型三 facet 分类方案，Tree D 为 SMS 五步流程。Tree A/B 的内部数字只能作为方法学描述统计 seed，Tree C/D 只能作为 schema/process seed，整体不得进入普通主统计池。

## 2. S1--S8 五分栏证据拆分

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定（中） | Abstract/§1/§5 明确目标是说明如何开展 SE systematic mapping、比较 maps 与 reviews，并给出 guidelines；本文没有以 RQ1/RQ2 形式声明自己的普通领域综述 RQ。Table 1 的 RQ 属于两个示例 mapping studies。 | 根对象应是“SMS 方法学论文目标声明”，而非普通 RQ-driven 主题综述；Tree B 才包含示例 RQ 字段。 | 不进入普通主统计池；可作方法学参考池 / SMS method seed。 | 精核时避免把 Table 1 示例 RQ 误写成 Petersen 2008 自己的主 RQ。 |
| S2 语料收集与筛选（中） | §3 对 10 篇 SE SLR 有检索串、数据库、纳排：`systematic review` AND `software engineering`，Inspec & Compendex、IEEExplore、ACM DL，21 篇候选，8 篇入选，再从 Kitchenham 2007 补 2 篇，总 n=10。§2.2--§2.3 只是对两个 mapping 示例说明各自检索/纳排。 | Tree A 有小型系统样本链；Tree B 是 2 个示例研究对比，不是由 Petersen 2008 独立检索出来的 mapping 样本库。 | Tree A 只可作为方法学描述性分母；Tree B 只作示例对照；二者均不进入普通主题统计池。 | 核对数据库名、21→8+2→10 链条、Table 1/2 示例性质。 |
| S3 原生维度树 / 样本编码对象（强，文本级） | §3.1/Table 5 对 10 篇 SLR 按研究目标、纳入要求、纳入数量、分析方式编码；§2/Table 1--2/Figure 3 对 2 个 mapping 示例对比；§2.4/Table 3/Figure 1 给出处方分类与流程。 | 原生结构是维度森林：A=10 篇 SLR 特征化表；B=2 个 mapping 示例对比表；C=三 facet 分类模式；D=SMS 五步流程。 | A/B 是内部方法学样本或示例；C/D 是处方 seed；整体不进普通主统计池。 | Table 5 列对齐、Figure 1 流程、Figure 3 数字需要在 A2a 写入精确证据链。 |
| S4 字段级证据（中） | Table 4 给 SLR ID，Table 5 给字段矩阵；§2.5 说明 Excel 表、每个 category、short rationale。原文未公开逐篇 rationale 表。 | Tree A 的字段级证据较清楚；short rationale 只能作为作者建议的 evidence-ledger 机制，不能当作本文公开数据。 | 可作字段证据链设计启发；不作 artifact completeness 统计。 | 核对 Table 4/5 所有 x、数值、`n.a.` 的列对齐；若引用 short rationale，标为处方建议。 |
| S5 维度模式演化（强，文本级） | §2.4 说明 abstract keywording、关键词聚类形成 categories；§2.5 明确数据抽取时 classification scheme 会新增、合并、拆分类别。 | Tree C/D 支持“schema 随阅读演化”的过程模式；这是方法过程，不是 Tree A 的样本观测字段。 | 可作为强 schema_seed / process_seed；不进入频数池。 | 核对 Figure 2 和 §2.5 中 add/merge/split categories 的精确位置。 |
| S6 统计分析（中） | Abstract/§2.5 强调 category publication frequencies；Table 5 给 n=10 SLR 的字段矩阵；Figure 3 给三 facet bubble plot。 | 统计节点只属于 Tree A 的 n=10 方法学样本和 Figure 3 的 SPL mapping 示例；不是目标领域 finding pool。 | 降级为“内部描述统计 seed”；严禁写成普通主统计池事实或最终 finding。 | A2a 必须核对 Table 5 中位数、x 分布，以及 Figure 3 的 118/128 两套分母和各类数字。 |
| S7 候选 finding（中） | §3.2--§4 比较 maps/reviews 的 goals、process、breadth/depth、validity，并提出 complementarity、adaptive reading depth、classify by evidence/novelty、visualization 等建议。 | 候选 finding 是方法学建议链：类别频数/交叉覆盖 → coverage/gap 观察 → 是否后续 SLR 深读。 | 可进入方法学启发池；不进入普通领域 finding 统计池。 | 正式写作时区分“作者基于经验/比较提出的建议”和“样本统计观察”。 |
| S8 研究者 / 作者质疑与裁决（弱） | §2.3 提到 prototyped exclusion technique 且未发现 misclassifications；§3.2 讨论术语误用、分类误判；§4 建议 adaptive reading depth。未报告多 reviewer disagreement log、一致性系数或裁决日志。 | 只能复原为“分类风险意识与缓解建议”节点，不能复原为实际 researcher adjudication 机制。 | 弱 / 不适用主统计；只作 threat/validation pattern seed。 | 避免把本仓库 A1/A2a 裁决链误归为 Petersen 2008 原文作者裁决链。 |

## 3. 原生维度森林复原

### 3.1 Tree A：10 篇 SE SLR 特征化表（被编码样本）

- 标识：`tree-petersen-2008-A`。
- 样本单位：1 篇 included SE systematic review；分母 n=10。
- 分母链：21 篇候选 systematic review papers → 排除非 SE / 非 Kitchenham&Charters-based / title-or-abstract 未明示 systematic review → 8 篇；再从 Kitchenham 2007 补 2 篇 → 10 篇。
- 字段树：
  - A1 引用身份：Reference ID 1--10 + 文献引用（Table 4）。
  - A2 研究目标：Identify Best and Typical Practices；Classification and Taxonomy；Emphasis on Topic Categories；Identify Publication Fora。
  - A3 纳入要求：Research is Within Focus Area；Empirical Methods Used。
  - A4 纳入数量：Potentially Relevant Studies；Relevant Studies (Included)。
  - A5 分析方式：Meta Study；Comparative Analysis；Thematic Analysis；Narrative Summary。
- 用途：方法学描述统计 seed；不作为普通领域统计池。

### 3.2 Tree B：2 个 mapping 示例研究对比（辅助示例样本）

- 标识：`tree-petersen-2008-B`。
- 样本单位：1 个 mapping 示例；n=2（Bailey 2007 OO design map；Mujtaba 2008 SPL variability map）。
- 字段：示例 RQ、search string、database/forum、inclusion/exclusion criteria、classification scheme、presentation/visualization。
- 用途：说明 SMS 宽检索、纳排与呈现方式如何随目标变化；不具备普通统计池资格。

### 3.3 Tree C：处方型三 facet 分类方案（schema seed）

- 标识：`tree-petersen-2008-C`。
- 类型：处方分类模式，不是 Petersen 2008 自己编码出的样本结果。
- 三 facet：
  - Topic facet：领域相关主题轴，如 SPL variability 中 requirements/architecture/implementation/verification and validation/variability management/orthogonal variability。
  - Contribution facet：process、method、model、tool、metric（metric 在 Figure 3 的 contribution axis 中出现）。
  - Research type facet：Wieringa 研究类型，Table 3 为 Validation Research、Evaluation Research、Solution Proposal、Philosophical Papers、Opinion Papers、Experience Papers。
- 用途：可迁移为 Paper2 的 schema seed，但 2008 年枚举不包含现代 LLM/agent 工件，后续必须扩展。

### 3.4 Tree D：SMS 五步流程（process seed）

- 标识：`tree-petersen-2008-D`。
- 流程节点：Definition of Research Questions / Review Scope → Conduct Search / All Papers → Screening of Papers / Relevant Papers → Keywording using Abstracts / Classification Scheme → Data Extraction and Mapping Process / Systematic Map。
- 用途：定义 SMS pipeline 与每步产物；它是过程树，不是样本编码树。

## 4. Figure 3 与 Table 5 数字核对（A1 文本/版面级，不得直接 final 化）

### 4.1 Figure 3 bubble plot 核对

PDF 第 5 页视觉核对显示 Figure 3 底部存在两套分母，不能混为一个总分母：

| Facet | 分母 | 类别数字 |
|---|---:|---|
| Contribution facet | 118 | Metric 4 (3.39%)；Tool 10 (8.48%)；Model 42 (35.59%)；Method 46 (38.98%)；Process 16 (13.56%)。 |
| Research facet | 128 | Evaluation Research 50 (39.06%)；Validation Research 0 (0%)；Solution Proposal 56 (43.75%)；Philosophical Paper 14 (10.95%)；Experience Report 8 (6.25%)；Opinion Paper 0 (0%)。 |

关键审计点：现有 `review.md` 中若写“验证型研究 = 56/128”，应改为“Solution Proposal = 56/128”；Validation Research 在 Figure 3 的 bottom summary 中为 0/128。Figure 3 这些数字属于 SPL variability mapping 示例，不得迁移为任何目标领域 final finding。

### 4.2 Table 5 数字与中位数核对

PDF 第 7 页 Table 5 视觉核对值：

- Potentially Relevant Studies：5453, 963, 5453, 5453, 1344, 353, 5453, n.a., 185, 564。
  - 若剔除 `n.a.`，n=9，排序为 185, 353, 564, 963, 1344, 5453, 5453, 5453, 5453，标准中位数 = 1344。
- Relevant Studies (Included)：78, 24, 24, 78, 10, 173, 103, 304, 10, 26。
  - n=10，排序为 10, 10, 24, 24, 26, 78, 78, 103, 173, 304，标准中位数 = (26+78)/2 = 52。
  - 若使用 lower median 才是 26；现有 `review.md` 中“中位数 ≈ 26”不能无说明地写作标准中位数。
- Means of Analysis：Meta Study = 2/10（ID 1,3）；Comparative Analysis = 1/10（ID 10）；Thematic Analysis = 2/10（ID 7,8）；Narrative Summary = 10/10。
- Research Goals 表格视觉核对：Identify Best and Typical Practices 的 x 出现在 ID 1,2,3,4,5,6,9,10，共 8/10；但原文正文段落随后写 majority reviews 为 Studies 2,5,6,8,9,10（6 篇）。这属于原文正文与表格之间的潜在不一致，A2a 应记录冲突；在冲突裁决前不要把 8/10 或 6/10 写成 final quantitative finding。

## 5. 需修改 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 清单

### C / critical

1. **`review.md` Figure 3 数字误标风险**：当前维度树 §6.1/统计观察若写“验证型研究 = 56/128 ≈ 43.75%”，与 PDF 第 5 页 Figure 3 不符；正确是 Validation Research = 0/128，Solution Proposal = 56/128。该错误会直接污染 S6 统计分析与后续可视化 pattern。
2. **`review.md` Table 5 中位数错误风险**：当前叶子表若写 Relevant Studies 中位数约 26，会被读作标准中位数；按 n=10 标准中位数应为 52，26 只能解释为 lower median。该错误会影响“SLR 入选规模”这类统计观察。
3. **`review.md` Table 5 最佳实践比例内部矛盾**：当前若保留“8/10=80%”同时写“约 60%”，内部自相矛盾；且原文正文与 Table 5 表格存在 6 篇 vs 8 篇的潜在冲突。应降级为“Table 5 视觉核对显示 8/10；原文正文列举 6 篇，待 A2a 裁决”，不得 final 化。

### I / important

1. **`evidence_chain.md` 需要新增/替代精核证据**：当前 A.2 多数仍为 `not_verified` 和“短引见 review.md”。若 `review.md` 修正 Figure 3 / Table 5 数字，应在 A.2 增加 PDF 第 5 页 Figure 3、PDF 第 7 页 Table 5 的具体证据记录，或继续明确为 A2a 待核，不能让正文数字看起来已经 final。
2. **`SUMMARY.md` 行级样本单位措辞需修正**：Petersen 2008 的行中若写 `illustrative primary-study set`，容易误导为 primary study 样本；本审计认为 Tree A 是 10 篇 secondary studies / systematic reviews，Tree B 是 2 个 mapping 示例，建议改成“方法示例 / secondary-study characterization + mapping examples”。
3. **`review.md` S6 等级说明需更保守**：S6 可写“中：内部描述统计 seed”，但所有具体比例、分母、中位数都应显式标注 A1 文本/版面级，最终统计前需 A2a 精核。
4. **`evidence_chain.md` 与 `review.md` 的 Tree C/C.2 来源边界需写清**：Contribution facet 中 `metric` 主要来自 Figure 3 axis，而 §2.4 文本只举 process/method/tool 等例子；若作为枚举，应说明是 Figure 3 实例化枚举，不是 §2.4 的封闭列表。

### M / minor

1. `review.md` 审计卡片写 `paper_content.txt` 537 行，而当前 `wc -l` 为 536 行；不影响结论，但建议统一。
2. `review.md` 与 `evidence_chain.md` 中 `IEEExplore` / `IEEE Xplore` 的写法可保留原文，但正式写作时建议加“原文写法/现代常用写法”说明，避免检索入口混淆。
3. `SUMMARY.md` S1--S8 矩阵目前未直接写入 Figure 3/Table 5 错误数字，暂未发现必须立即修正的定量项；但若后续回填数字，应使用本文件 §4 的保守口径并注明不是 final finding。
