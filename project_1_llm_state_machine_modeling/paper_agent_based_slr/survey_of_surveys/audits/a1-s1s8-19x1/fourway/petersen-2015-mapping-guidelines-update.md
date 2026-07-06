# petersen-2015-mapping-guidelines-update：A1-S1S8 四分栏提取

## 总体统计池裁决

**裁决：保留为 `survey_of_surveys` S1--S8 主统计池候选，但只进入方法学 / schema 统计池；A2a 页码、表图和 Appendix B 逐研究映射精核前，不进入最终定量发现。**

理由：本文不是纯 guideline 文本。摘要和 §3 明确说明作者执行了 **systematic mapping study of systematic maps**，最终样本单位是 **52 篇 SE 系统映射研究**，并用 Table 3 抽取表、§4 统计结果、Appendix B 逐研究关系表支撑 RQ1--RQ4；同时 §5 将这些统计与既有 SLR/SMS 指南比较后形成 **guideline update**。因此它可以统计“综述之综述如何抽取字段、形成维度、做方法学统计与修订指南”，但不能作为 Paper2 目标 SE 领域效果 / 因果结论的统计来源。分母口径应使用 final included **N=52 mapping studies**；57 只是 quality assessment 中间候选。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要写明目标是识别 systematic mapping process 如何执行并据此更新 guideline；§3.1 给出 RQ1--RQ4，覆盖采用哪些 guidelines、SE topics、发表时间地点、mapping process 如何执行。 | 顶层任务是“对 SE systematic maps 做 systematic map，并将统计结果转化为 mapping guideline update”；RQ 是字段 owner，不是单一树根。 | **强，合格候选**；可统计为 mapping-of-maps / guideline-update 型任务设定，但仅限方法学池。 | 核对摘要、§1 contribution、§3.1 RQ 的正式页码与原文排版；确认 DOI final 与本地 PDF 一致。 |
| S2 语料收集与筛选 | §3.2 给出 IEEE、ACM、Scopus、Inspec/Compendex 检索式和命中数；§3.3 给出纳排、title/abstract、full-text、backward snowballing、QA、first-author validation 与排除研究回查；Fig. 1 给出流程链。 | 检索漏斗树包括数据库检索、去重与时间窗、题摘筛选、全文筛选、滚雪球、质量评价、validation set 与 excluded review 回补。 | **强，合格候选**；可入“语料筛选流程 / 分母链”统计池；最终分母应为 52，不应把 57 写成 included studies。 | 视觉核对 Fig. 1 的 7752、5082、60、43、54、44、52 等数字链；复核 Table 1/2 和 Appendix A included/excluded 清单。 |
| S3 原生维度树/样本编码对象 | §3.4 Table 3 给出抽取表；§4 按 RQ 汇总；Appendix B Tables B.15--B.27 给出逐研究映射；`review.md` 已裁决样本单位为 52 篇 SE systematic mapping studies。 | 原生结构是维度森林：数据抽取表单树、classification facet 树、guideline action / rubric 树、validity taxonomy 树，共享“52 篇 mapping studies”样本单位。 | **强，合格候选**；可作为“同一样本单位上的多根维度森林”统计样本。 | 核对 Table 3 列名、RQ 绑定关系、Appendix B 全部表格是否均以同一 52 分母展开；检查表格跨页无漏项。 |
| S4 字段级证据 | Table 3 字段包括 study id、title、author、year、SWEBOK area、venue、guidelines、search strategy、search type、classification schemes、visualization type；Appendix B 给出 topic、venue、guideline、search、QA、facet、visualization、validity 等逐研究关系。 | 字段层可复原为 bibliographic fields、SE topic fields、process fields、classification fields、visualization fields、validity fields 和 rubric fields。 | **中到强，文本级候选**；字段存在性强，但逐样本取值和计数需 A2a 后才能进入最终统计。 | 精核 Tables B.15--B.27 每张表的行数、列名、缺失值语义和 OCR 残留；复核 Figure 3--15 与 Appendix B 倒推计数是否一致。 |
| S5 维度模式演化 | §4.4.4 识别 topic-independent facets，指出 Petersen 2008 未强调的新维度为 venue、study focus、research method；§5 与 Table 5 比较既有 guidelines，§5.1.3 最终鼓励使用 venue、research type、research method。 | 模式演化不是代码本迭代日志，而是“已有指南覆盖差异 + 实际 SMS 统计实践 → 更新后的通用 facet 与活动清单”。需区分新识别维度和最终推荐 facet。 | **强，合格候选**；可入“方法实践统计如何驱动 schema/guideline 修订”统计池。 | 复核 Table 5 guideline comparison matrix、Fig. 12、Table B.24、§5.1.3 相关段落；避免把 contribution type 或 study focus 误写为最终推荐三元组。 |
| S6 统计分析 | §3.5 明确 tabulate、visualize、theme grouping and counting；§4 对 guideline adoption、topics、venues、search、QA、classification、visualization、validity 做频数统计；§5.4 Table 14 与 Fig. 20--21 报告 rubric 分布。 | 统计从字段树派生：52 分母上的 guideline、topic、venue、search、QA、facet、visualization、validity 和 rubric ratio 等方法学统计。 | **强，合格候选**；可作为方法学统计池样本，A2a 前不得并入最终跨论文定量发现。 | 逐项核对 §4 图表、Table 14、Fig. 20--21 的数值；确认 median quality ratio、25% threshold、journal/conference 对比等表述。 |
| S7 候选 finding | §6 总结多指南并用、单一 guideline 不足、需要 updated guideline；§5.1.3 推荐通用 facets；§5.4 提出 evaluation rubric；§6 强调 good sample / representation 比单纯更多研究更重要。 | 候选 finding 链条是“字段统计观察 → 方法学解释 → guideline update / rubric / reporting 建议”，不是 SE 目标领域技术效果结论。 | **强但限界**；可入“统计观察转方法学 finding”模式池；不得迁移为 LLM4STM 或其他目标领域发现。 | 将每个 finding 回连到 RQ、图表或 Table 5/8/14；核对作者 discussion 与我们方法启发之间的边界。 |
| S8 研究者/作者质疑与裁决 | §3.3 承认 title/abstract 筛选由单一作者完成，是 reliability threat；随后用 first-author validation sets、回查排除研究缓解；§3.4 说明第二作者抽取、第一作者 trace-back review；§3.6 系统讨论 validity。 | 可复原为 threat-aware validation / checker 机制和 guideline-level consensus 建议；不是完整双人独立筛选、完整 coding adjudication 或 inter-rater 日志。 | **中，候选但需降级**；可统计为“有复核与效度缓解”，不能统计为“完整人工裁决日志”。 | 核对 §3.3、§3.4、§3.6、Fig. 17、Table 6；确认单人筛选风险与 first-author validation 的边界表述。 |

## 建议降级 / 修正

- **不应整体排除出统计池**：它虽是 guideline update，但有完整 systematic map of maps 证据链，适合作为方法学 / schema 统计池候选。
- **必须限制统计池类型**：仅统计 survey_of_surveys 方法维度、字段与 guideline-update 模式；不得进入 Paper2 目标领域效果池。
- **S4 保持文本级中到强**：字段存在性强，但 Appendix B 与图表计数需 A2a 精核后才能升级为最终定量证据。
- **S5 表述需精确**：新识别维度是 venue、study focus、research method；最终鼓励的 topic-independent facets 是 venue、research type、research method。
- **S8 建议保持中**：有复核、trace-back 和 validity mitigation，但没有完整双人独立裁决日志或一致性系数。
