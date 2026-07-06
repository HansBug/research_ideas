# app-reviews-slr-se：S1--S8 四分栏审计补充

## 总体统计池裁决

**裁决：有条件候选入池。** 本文是正式 SLR，原文明确给出 RQ、检索 / 筛选链、182 篇原始研究分母、F1--F18 抽取表、三套 classification schema、reliability 检查和大量描述统计，因此适合作为 `survey_of_surveys` 的方法学 / 维度模式 / 报告结构候选统计池样本。但 `evidence_chain.md` 当前多处仍标为 `not_verified`，且复杂表格、PRISMA 图、搜索式和 supplementary spreadsheet 尚未 A2a 视觉核验；因此 A2a 前不应进入最终定量统计池，只能作为候选分母和 pattern seed 使用。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文说明研究目标是系统综述 app review analysis for SE，并给出 RQ1--RQ5：分析类型、技术、SE 活动、评价方法、评价结果。 | 对应维度树的顶层任务层：以“app reviews 如何支持 SE”为根任务，RQ 映射到 F6、F7、F8/F9、F10--F18、F13。 | 候选入池：强。可进入 RQ / task-setting pattern 池；不是领域结论池。 | 核对 PDF 页码与 RQ 原文位置；确认 DOI/出版页元数据。 |
| S2 语料收集与筛选 | 原文遵循 Kitchenham + PRISMA，给出 1656 初始命中、303 重复、1353 筛选、1225 排除、128 初始纳入、+14 manual、+40 snowballing、最终 182 篇。 | 对应语料构建子树：数据库检索、manual search、snowballing、纳排标准、数量链、最终样本单位。 | 候选入池：中到强。流程存在性强；最终分母链需 A2a 后才能作为最终统计分母。 | 视觉核对 Fig.1 PRISMA、Table 1 纳排、Table 2 venue、搜索式；尤其“six major digital libraries”文本抽取只清楚显示五个名称。 |
| S3 原生维度树/样本编码对象 | 原文说明 selected studies 被逐篇读取，Table 3 F1--F18 是 data extraction form；最终样本为 182 篇原始研究。 | 复原为“字段森林”：书目信息 F1--F5、analysis F6、technique F7、SE activity F8/F9、evaluation/artifact F10--F18，加三套 schema。 | 候选入池：强。可进入 sample-unit / native-dimension-tree pattern 池；不应说成原文给出单一 formal tree。 | 核对 Table 3 版面；检查 supplementary spreadsheet 是否可获得并与 F1--F18 对齐。 |
| S4 字段级证据 | Table 3 明列 F1--F18，覆盖标题、作者、年份、venue、citation、review analysis、mining technique、SE activity、justification、evaluation、annotated dataset、quality measure、replication package 等。 | 字段级叶子可复原为 F1--F18；其中 F6/F7/F8 是分类字段，F10--F18 是评价与复现资产字段。 | 候选入池：强（字段存在性）。适合作为 extraction-form 模式样本；具体叶子取值频次仍需核验。 | 核对 F10.1/F10.2、F14.1/F14.2 等子字段是否全部来自原文而非本地细化；核对 open enum 是否依赖 supplementary。 |
| S5 维度模式演化 | 原文说明三套 classification schema 由既有分类、content analysis、语义合并、删除无关项、补充 Recommendation、SWEBOK 映射形成，并报告 Table 4 reliability。 | 对应 schema-construction 子树：F6 app review analysis、F7 mining technique、F8 SE activity；含来源、合并规则、最终编码和 reliability。 | 候选入池：强，但限于“schema 构造模式”。不应解释为长期时间演化。 | 核对 Table 4 数值、20%/10% 抽样比例、外部 assessor 描述；确认 taxonomy 来源与最终类别数量。 |
| S6 统计分析 | 原文提供年度/venue、analysis 类型、technique、交叉表、SE activity、evaluation/results，并说明异质性太强不做 meta-analysis，而用 summarizing effect estimates。 | 统计层复原为频次、百分比、交叉表、five-number summary、range/median、qualitative synthesis；关系边包括 F6×F7、F6×F8、F12×F6、F13×F6/F6.2。 | 仅候选入池：中。统计呈现丰富，但 A2a 前不进入最终定量池；可先作为“统计呈现模式”样本。 | 高优先级核对所有复杂表格：Table 5--23、矩阵对齐、百分比、分母、多值编码、Table 21 range/median。 |
| S7 候选 finding | §4 将统计观察转为 findings / gaps：growing area、SE use cases 模糊、reference model 缺失、数据集小、replication packages 不足、practice impact 不清、scalability / efficiency 缺评等。 | 复原为“统计观察 → discussion gap → future work”派生层；不属于单篇样本编码字段。 | 候选入池：中。可进入 finding-construction pattern 池；具体 app-review 领域结论不能迁移到 Paper2。 | 逐条核对 §4.1--§4.10 是否有表格支撑；区分 evidence-backed finding、作者解释、作者假设。 |
| S8 研究者/作者质疑与裁决 | 原文报告 screening Cohen’s Kappa=0.9、data extraction inter/intra agreement、schema reliability、protocol panel review、threats mitigation。 | 复原为 quality-control / reliability / threats 子树：检索完整性、publication bias、screening/extraction/classification subjectivity、taxonomy reliability。 | 候选入池：中到强。若 S8 只要求 reliability/threat evidence，可强；若要求逐项 adjudication ledger，应降为中。 | 核对 Cohen’s Kappa 样本、percentage agreement、panel review 原文；确认是否有原始 disagreement / adjudication 记录。 |

## 建议降级 / 修正

1. 总体“是否统计池=是”建议修正为：有条件候选入池。A2a 前不得作为最终定量统计池证据。
2. S6 建议从“强”降为“中（统计存在性强，最终定量可用性中）”。复杂表格和 OCR/版面对齐风险尚未排除。
3. S7 建议从“强”降为“中（finding 形成模式强，领域 finding 不可迁移）”。§4 findings 是作者合成结论，需要逐条映射支撑表格。
4. S8 建议加条件说明。若只评估 reliability / threats，当前“强”可保留；若 S8 要求完整研究者裁决日志，则应降为“中”。
5. S5 建议措辞修正为“维度模式构造 / schema construction”，不要称为真正的时间演化。
