# mde-ml-components-slr：A1-S1S8 四分栏提取

## 总体统计池裁决

- **论文类型**：SLR；原文明确遵循 Kitchenham 指南，系统检索 7 个数据库并结合 snowballing。
- **样本单位**：46 篇 primary studies，编号 P1--P46。
- **统计池裁决**：可进入 **schema / method 模式统计池候选**，因为 RQ、检索筛选链、40-question extraction form、Fig. 5 feature tree、Table 3--9 与 RQ Answer Summary 均有明确分母和字段化证据；但 **不得进入本仓库目标领域结论池**，MDE4ML 领域发现只能作为方法脚手架先验。
- **A2a 前限制**：A2a 完成页码、图表、PDF 版面与数据仓库精核前，不应把具体数值升级为最终定量发现；尤其需保留 3934 vs 3496 初始池数字冲突。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要与 §3 明确目标是系统综述 MDE4ML，分析 motivations、MDE solutions、evaluation、benefits、limitations；§3.1 设置 RQ1--RQ4。 | 对应根任务“面向机器学习组件的 MDE 方案”，RQ1--RQ4 分别投影为动机、方案工具、评价、限制未来工作四个主分支。 | **强，可入 schema/method 池**；任务边界清楚，但领域结论仅限 MDE4ML。 | 复核正式页码与 RQ 原文措辞；确认引用时不把 MDE4ML 结论迁移到 LLM4STM。 |
| S2 语料收集与筛选 | §3.2--§3.3：7 个数据库，自动检索 3934 条，去重 3570，筛到 72、55、32，再 snowballing +14，最终 46；Table 1 给 I01--I04 与 E01--E10。 | 纳排门禁是独立 schema；样本单位为 P1--P46 primary studies，筛选分母链可复原。 | **强，可入统计池候选**；分母链完整，适合统计检索筛选模式。 | 结论 §7 写 initial pool 3,496，与方法/摘要 3,934 冲突；需 PDF 与可能补充数据核定正式采用 3934 并记录冲突。 |
| S3 原生维度树/样本编码对象 | §4.1 明确 Fig. 5 是由 RQ-based extraction categories 派生的 feature tree；Appendix A 列 P1--P46。 | 复原为单根 Fig. 5 主树“Features of selected primary studies / MDE Solution for ML”，另有 Table 1 纳排 schema 与 QA1--QA5 质量 rubric 并列，不并入主树。 | **强，可入 schema 池**；主树和并列 gate/rubric 边界可辩护。 | 需回 PDF 核对 Fig. 5 完整节点、层级连接与图题；当前文本级复原不能替代图形版面精核。 |
| S4 字段级证据 | §3.4：Google Form 40 个问题、5 个 section、23 short answer、10 long answer、2 checkbox、14 radio button；Table 3--8 与 Table 9 实例化字段。 | 字段覆盖 publication、goal/sub-goal、ML technique、domain、end user、contribution、modeling、ML aspects、tool support、evaluation、metrics、limitations/future work、QA。 | **强，可入字段级统计池候选**；字段和分母基本明确。 | 需核验 GitHub SLR data 是否含原始 Google Form/coding sheet；需回 PDF 校正 Table 3--9 单元格与错位风险。 |
| S5 维度模式演化 | §3.3.1 说明 search string 多轮 refinement；§3.4 pilot 6 篇后 small updates 改进 Google Form；§5 提及术语不一致经讨论达成共识。 | 可复原为“检索式演化 + extraction form pilot 修订 + 术语归类裁决”的轻量演化链，但没有完整变更日志。 | **中，只作方法模式候选**；能证明有演化，但不足以统计细粒度 schema-change。 | A2a 查补充数据是否保留表单版本或编码修订记录；若无，应保持中等级，不上调为强。 |
| S6 统计分析 | §4 各 RQ 使用 Venn、bubble chart、分布图、频次表、QA 分布和 RQ Answer Summary；多处以 46 为分母报告 43/46、35/46、38/46 等。 | 字段表转为 A1-M5 统计观察：goal、ML technique、tool availability、evaluation method、limitations、QA 等频次与比例。 | **强，可入统计模式候选**；适合抽取“字段表到统计观察”的报告模式。 | Fig. 4--10、Table 2--9 的所有数值需 PDF 逐项复核；图形抽取不完整时不得直接作为最终数字。 |
| S7 候选 finding | RQ Answer Summary 与 §6 Discussion roadmap 将统计观察转为 data first-class、solution focus、maturity、terminology、scalability、responsible ML、evaluation rigor 等建议。 | 可复原为 A1-M6 候选发现链：统计观察 → RQ summary → roadmap/recommendation；但 finding 是作者解释性综合。 | **强，但仅限候选 finding 方法池**；不能把 MDE4ML 领域 roadmap 作为本仓库目标结论。 | 需为每个候选 finding 补支持计数、反例、分母和页码；A2a 前不升级为 final research finding。 |
| S8 研究者/作者质疑与裁决 | §3 与 §5：protocol review、cross-validation、pilot extraction、其他作者监督、ambiguities discussion、threats to validity；§3.4 说明第一作者抽剩余论文。 | 可复原为作者级审计与讨论机制，但缺少双人独立编码比例、Cohen kappa、逐条 disagreement/court record。 | **中，可作边界锚点**；支持“有质控”，不支持“强审计裁决链”。 | A2a 检查 supplementary 是否有 disagreement log 或 inter-rater 统计；若无，保持中，并建议在本研究方法中补强裁决日志。 |

## 建议降级 / 修正

- **S5 建议维持中**：原文只报告 pilot 后 small updates 与讨论共识，不能写成完整 schema evolution audit trail。
- **S8 建议维持中**：有作者交叉验证和 threats，但没有独立双人编码比例、分歧统计或逐项裁决日志。
- **统计池修正**：本篇应标为“schema/method 候选：是；目标领域结论池：否；A2a 精核前不得进入最终定量统计”。
- **分母修正**：正式写作优先采用方法节链条 3934 → 3570 → 72 → 55 → 32 → 46，同时显式记录结论处 3,496 疑似笔误。
