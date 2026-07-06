# interactive-llm-systematic-mapping：A1 S1--S8 round3 独立审计

> 角色与边界：本文件只处理 `papers/interactive-llm-systematic-mapping/` 这一篇；未开启 sub-subagent。本文档是 A1 文本级审计输入，**不得直接写成 final quantitative finding**，也不得把 proposal / interactive SMS 方法图当作完成型统计样本。

## 0. 一句话裁决

Petersen & Gerken (2025) 是作者自述的解决方案提案（solution proposal），不是已执行的 SLR/SMS/tertiary study。它能为 Paper2 提供“交互式 LLM 支持系统映射研究”的阶段化方法种子、字段种子和风险边界，但没有系统检索、纳排分母、样本编码表或自身统计分析；因此 **S2/S6 不成立，不进入主统计池**。

## 1. 全文阅读与核验依据

| 来源 | 本轮读取 / 核验范围 | 对本审计的作用 | 备注 |
|---|---|---|---|
| `bibtex.bib` | 全文读取；题名、作者、IST、卷 178、页码 107611、年份 2025、DOI。 | 锁定文献身份与正式引用年份。 | 与 `metadata.json` 的 online-first 日期区分。 |
| `metadata.json` | 全文读取；`review_type=系统映射 / solution proposal`、`eligible_for_statistical_synthesis=false`、`evidence_role=solution_proposal_boundary_anchor`。 | 核对本地 eligibility 已将其排除出统计合成。 | metadata 本身不是原文事实源，需回到 PDF / text。 |
| `paper_content.txt` | 全文 1--280 行通读：摘要、引言、§2 各阶段、§3 reflections、data availability、references。 | 主要原文依据：Method 自述为 solution proposal；§2 给出流程与 agent；Data availability 写明未使用数据。 | 文本提取足以支持大部分文本级判断。 |
| `paper.pdf` | 本轮视觉核对 Page 2 Fig. 1。 | 核实 Fig. 1 不是统计表，而是 5 个顶层流程列的交互式方法图；图中含 user input / interactive refinement / LLM-output 三槽。 | 图中文字仍建议 A2a 做精确页码与字段级锚定。 |
| `review.md` | 全文读取；重点读快速结论、维度树复原、叶子维度表、关系边表、S1--S8 表。 | 审计现有抽取是否过强、是否混入 Paper2 增强字段。 | 发现若干需修正点见 §5。 |
| `evidence_chain.md` | 全文读取 A.1--A.4。 | 核对 A.2/A.3 对类型、样本单位、分母、树型、统计池资格的证据强度与可用位置。 | 目前 evidence_chain 是树级 claim map，叶子字段尚未完全迁入。 |

关键原文锚点：

1. 摘要 Method：原文自述为 solution proposal，方案由作者基于 LLM 与 literature review 经验迭代设计和讨论。
2. §2 开头：Fig. 1 展示 mapping process 每一步的用户输入 / 用户动作 / LLM 输出；研究者应已有初始 search terms、inclusion criteria 或 extraction items 来验证输出。
3. Fig. 1：顶层列为 “Establish a need for the review / Study identification / Data extraction / Visualization / Reporting”；不是 PRISMA、不是样本分母图、不是结果统计图。
4. §2.2.2：原文明示分类为 `relevant` / `not relevant`，并要求 LLM 解释 inclusion/exclusion 的理由；citations 用于验证论证并增加 traceability。
5. Fig. 1 的 Study identification 输出：结构化输出可含 criteria fulfilment、final verdict `include/exclude` 与 confidence value。
6. §2.3：data extraction/classification 分为 inductive coding 与 deductive coding；归纳端使用 topic modeling，演绎端可用 extraction scheme、one/few-shot 与 RAG。
7. §3：风险包括 publication bias、LLM reliability 证据有限、模型快速演化、非 SE 研究外推不足，并提出单步骤优化与端到端 prototype 两条研究方向。
8. Data availability：原文明确 `No data was used for the research described in the article.`

## 2. S1--S8 建议等级总表

| 维度 | 建议等级 | 审计结论 | 统计池边界 |
|---|---|---|---|
| S1 综述任务设定 | 中 | 有明确 objective 和 solution-proposal 类型；无正式 RQ 表、protocol 或已执行 SMS 样本单位。 | 只作方法任务设定种子。 |
| S2 语料收集与筛选 | 不适用 | 无数据库、检索式、纳排分母、去重、质量评价或样本链；references 只是叙事旁证。 | 不进入主统计池。 |
| S3 原生维度树 / 样本编码对象 | 中（降级） | 可复原为流程阶段 + 人机交互 + agent / 技术机制 + 风险路线图的降级维度森林；不是 primary-study 编码树。 | 只作 schema_seed / boundary_anchor。 |
| S4 字段级证据 | 中（需拆分） | 阶段、三槽、search agents、include/exclude、confidence、reasons、citations、traceability 有原文依据；borderline、locator、override log 是 Paper2 增强字段。 | 字段候选可用，但不得混作原文字段统计。 |
| S5 维度模式演化 | 弱 | 原文只有作者经验迭代设计 proposal 和未来 prototype 路线；无 coding saturation、codebook evolution 或分类修订日志。 | 只作路线图启发。 |
| S6 统计分析 | 不适用 | 本文没有自身统计分析；被引研究的 recall/precision/GPT 表现不是本文结果。 | 不进入主统计池。 |
| S7 候选 finding | 弱--中 | 有方法学 design claim：LLM 可辅助 SMS 各阶段，但需 HITL、可复现检索、traceability 与 SE-specific evaluation；不是经验证 finding。 | 只能作候选方法启发 / 边界锚点。 |
| S8 研究者 / 作者质疑与裁决 | 弱 | 有 human oversight、专家在环、理由与 citation 要求；无多评审者裁决协议、一致性统计或 QA 日志。 | 只作审计机制启发。 |

## 3. S1--S8 五分栏证据拆分

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1（中）综述任务设定 | Objective 是讨论 LLM 在 mapping study process 中的可能性与下一步；Method 自述 solution proposal。 | 根对象是“交互式 LLM 支持 SMS 流程设想”，可用作任务设定与 paper story 边界。 | 不进主统计池；可作 method scaffold seed。 | 精确页码与 Fig. 1 标题 / 阶段名称锚定。 |
| S2（不适用）语料收集与筛选 | 原文没有数据库、检索式、PRISMA、纳排分母、质量评价；Data availability 明确未使用数据。 | “Search / inclusion-exclusion” 是 proposed strategy 阶段，不是已执行 corpus pipeline。 | 不进主统计池；references 不得当作样本库。 | 补充材料只定义下划线术语，即便核验也不改变无分母裁决。 |
| S3（中，降级）原生维度树 / 样本编码对象 | §2 与 Fig. 1 逐阶段描述 user input、interactive refinement、LLM output；§2.2.1 给出三 search agents。 | 降级维度森林：流程阶段树、交互三槽树、search agent 子树、抽取 / 技术机制树、risk / roadmap 树。 | 不进统计池；可作 schema_seed。 | Fig. 1 字段逐项抄录与 §2 文本对齐。 |
| S4（中，需拆分）字段级证据 | 原文明示：relevant/not relevant；final verdict include/exclude；confidence value；reasons；citations；traceability；topic model；extraction items；csv/JSON structured output。 | 原文字段应与 Paper2 增强字段分层：原文层只收显式字段；Paper2 层可追加 borderline、locator、override log、source span。 | 可作字段设计候选；不得把增强字段计为原文已报告。 | A2a 需修正 leaf table：补 confidence value，移出 borderline / locator 到 Paper2 enhancement。 |
| S5（弱）维度模式演化 | 原文只说方案由作者基于经验迭代设计和讨论；末尾建议先改进单步骤、再建整体 prototype。 | 仅可复原成 proposal formation 与 roadmap，不是 codebook / taxonomy evolution。 | 不进统计池；作 future-work / process-risk seed。 | 核对是否 supplementary 只含术语定义；不要脑补成演化日志。 |
| S6（不适用）统计分析 | 无自身数据、表格、实验指标；recall、precision、GPT-4 优势等来自 Wang / Huotala / Guo / Petersen 等被引研究。 | 原生树无统计 synthesis 分支；相关研究只能作为背景证据，不是本文统计节点。 | 不进主统计池；严禁二次引用误归属。 | A2a 标注每个被引结果的来源归属。 |
| S7（弱--中）候选 finding | 作者提出 LLM 可支持 SMS 各阶段，同时强调 HITL、Boolean reproducibility、traceability、model drift、SE-specific evaluation。 | 可挂入 B5 audit / B6 risk / B7 roadmap，但只能是 design claim 和 method rationale。 | 不进 empirical finding 池；不得写成“已证明有效”。 | review / SUMMARY 中的 S7 等级建议降为“弱--中”或“弱（方法启发）”。 |
| S8（弱）研究者 / 作者质疑与裁决 | 原文要求 reviewer 懂 mapping method 且是 topic expert；纳排需解释、citation、traceability。 | 可映射为 HITL gate 与 evidence-grounded rationale；没有 adjudication workflow。 | 不进统计池；可作人工审计字段启发。 | 区分 human-in-the-loop 原则与正式多评审者裁决 / override 日志。 |

## 4. 原生维度树 / 维度森林复原（round3）

```text
根：交互式 LLM 支持的系统映射研究方法设想
  类型：解决方案提案 / 概念蓝图；无系统样本库；无主统计池资格
  样本单位（降级）：流程阶段、交互槽、agent 角色、方法建议、风险 / 路线图条目

  树 A：流程阶段树（Fig. 1 + §2）
    A1 建立综述 / map 需求
       - 任务：形成 gap、research goals、research questions
       - LLM 输出：支持研究目标的一组 RQ 候选
    A2 研究识别（Study identification）
       - A2a 检索：search terms、search strings、Boolean / semantic search strategy
       - A2b 纳入 / 排除：criteria fulfilment、final verdict include/exclude、confidence value
    A3 数据抽取与分类
       - A3a 归纳式编码：topic model、topic categories、topic-defining terms
       - A3b 演绎式编码：extraction items、csv/JSON structured extracted information
    A4 可视化
       - 表格和图形表示：bubble plots、bar charts、tabular summaries 等
    A5 报告
       - 总结数据、解释 findings、提示 patterns / insights

  树 B：逐阶段人机交互三槽树（Fig. 1）
    B1 User input：研究者提供目标、问题、criteria、articles metadata、data tables 等
    B2 Interactive refinement：研究者编辑、试运行、调整、确认或补充
    B3 LLM-output：LLM 给候选 RQ、检索式、criteria、verdict、topic model、extraction JSON、图表与报告建议

  树 C：检索阶段三 agent 子树（§2.2.1）
    C1 Keyword Identification Agent：识别相关术语、近义词、历史术语、概念层级
    C2 Semantic Search Agent：RAG + 可选 graph database，建议相关文献并调整检索策略，不直接完成选择
    C3 Search Strategy Agent：生成实际用于研究的检索策略

  树 D：字段 / 审计要求树（§2.2.2 + Fig. 1）
    D1 原文明示分类字段：relevant / not relevant；include / exclude final verdict
    D2 原文明示辅助字段：criteria fulfilment、confidence value、reasons / explanations、citations、traceability
    D3 Paper2 增强字段（非原文明示）：borderline / uncertain、source locator、page-line span、override log、adjudicator identity

  树 E：风险与路线图树（§3）
    E1 风险：publication bias、limited studies、model evolution / provider drift、non-SE transfer risk
    E2 研究方向：evaluate individual steps；build end-to-end prototype
```

关键降级说明：树 A--E 都是 proposal 的概念组织结构，不是从一组 primary studies 中开放编码得到的 taxonomy；它们可以服务 A1/A2a/A2b 的 schema 设计，不能作为 completed SMS 的定量样本。

## 5. 需修改 review / evidence / SUMMARY 的 C/I/M 清单

### C / critical

1. **C1：S7 等级和措辞仍有过强风险。** `review.md` 与 `SUMMARY.md` 当前把 S7 写成“中：可作为候选 finding...”。建议改成“弱--中”或“弱（方法启发）”，并显式写明它只是 design claim / methodological insight，不是 empirical finding。否则后续合并时容易把 proposal 结论误写成 Paper2 final finding。

### I / important

1. **I1：原文字段与 Paper2 增强字段需要硬分层。** `review.md` 维度树 / 叶子表中 `audit.decision` 出现 include/exclude/borderline 或 uncertain，`audit.source_loc` 也被写作原文隐含字段；但原文明示的是 relevant/not relevant、include/exclude final verdict、confidence value、reasons、citations、traceability。`borderline/uncertain`、精确 locator、override log 应移到 Paper2 enhancement，不应算原生字段。
2. **I2：Fig. 1 原文明示的 confidence value 应补入 S4 / 叶子表。** 当前 review 强调 rationale / citation / source location，但漏掉图中 structured output 的 `confidence value`；这比本地 `borderline` 更接近原文字段。
3. **I3：PDF 核验状态在 review 内部不一致。** 快速结论卡片称已回 PDF 核对 Fig. 1，但维度树审计卡片仍写“未用 Read 打开 PDF；Fig. 1 只能依赖 caption”。建议更新为：round3 已视觉核对 Fig. 1 的顶层结构；A2a 仍需做精确字段抄录和页码锚定。
4. **I4：`evidence_chain.md` 目前是树级 claim map，尚未承接字段级修正。** 若后续 A2a 迁入叶子字段，应新增或替代证据来区分 `D1/D2 原文明示字段` 与 `D3 Paper2 增强字段`，避免用 `ev-...-tree` 一条证据承载过多字段结论。
5. **I5：SUMMARY 的 S4/S7 单元格应同步收紧。** SUMMARY 现有 S4 已提到 override、source location、borderline 是增强字段，这是正确方向；建议进一步把 “source location” 写成 “精确 locator / page-line span 为增强字段”，并把 S7 同步降级为 proposal 方法启发。

### M / minor

1. **M1：维度树中文化可继续清理。** 例如重复中英标签、`阶段.报告` 等混合标识可保留 stable id，但旁边中文释义应更一致。
2. **M2：工具名风险可统一放在开放枚举说明中。** BERTopic、LIDA、LangSmith、WebVoyager 都是示例工具，不宜在 SUMMARY 中被误读为必须实现的组件。
3. **M3：被引文献结果建议统一标注“二手旁证”。** review 已基本做到，但 A2a 若抽数字，必须避免归属到 Petersen & Gerken 本文。

## 6. 不足与接力

- 本轮在 20 分钟约束内完成文本全文阅读、现有 review/evidence 审计和 PDF Page 2 Fig. 1 视觉核对；未打开 DOI supplementary material。
- 本文件只给 A1 round3 独立审计结论；未修改 `review.md`、`evidence_chain.md` 或 `SUMMARY.md`。
- 后续主线程若采纳，应只把本文件作为审计输入，再按 GUIDE §6.4 回填正式表格与证据链；不得把本文件中的等级计为最终定量统计。
