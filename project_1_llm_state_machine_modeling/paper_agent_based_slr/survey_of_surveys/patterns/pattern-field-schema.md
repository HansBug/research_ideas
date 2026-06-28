# pattern-field-schema.md：脚手架字段模式合同

## 1. 目的

本文件定义 A1 `survey_of_surveys/` 的最小字段合同。它的目标是让后续 A2a / A2b 能把单篇 SLR/SMS/survey/guideline review 汇总为可演化维度模式，而不是只堆自然语言摘要。

## 2. 字段使用边界

- 本 schema 只服务脚手架模式先验，不支撑目标领域发现。
- 字段定义必须可执行：读者应能判断一篇论文是否能填该字段。
- `metadata-only` 条目不能把字段升级为已采纳，只能进入候选或待核验。
- 缺失值必须区分 `原文未报告`、`文本提取缺失`、`尚未阅读`、`不适用`，不得统一写成 `无`。

## 3. 证据等级枚举

| 枚举 | 含义 | 是否可采纳 pattern |
|---|---|---|
| `题摘级` | 只读题名、摘要、元数据 | 否；只能候选。 |
| `全文文本级；图表待人工核对` | 已读 `paper_content.txt` 关键正文 | 可以作为 A1 dry-run 采纳，但正式数值待 PDF 核对。 |
| `PDF图表级` | 已人工核对关键表格/图形/公式 | 可以支撑图表/数值级 pattern。 |
| `全文不可得` | PDF 未获取或无法合法访问 | 否；只能进入人工下载清单。 |

## 4. 六类 pattern 字段总表

| 字段 ID | 中文字段名 | 英文字段名 | 操作化定义 | 取值空间 | 最低证据要求 | 缺失值语义 | 来源锚点 |
|---|---|---|---|---|---|---|---|
| `rq_pattern` | 研究问题模式 | RQ pattern | 论文如何组织研究问题，例如规模、主题、主体、限制、效果、趋势、实践影响。 | 自由文本 + 受控标签 | 全文文本级 | `原文未报告` / `guideline不适用` / `尚未阅读` | 必须 |
| `dimension_pattern` | 维度模式 | dimension pattern | 论文为抽取、分类或统计设置了哪些字段和类别。 | 字段树 / 表格 / 分类轴 | 全文文本级 | `原文未报告` / `metadata-only` / `不适用` | 必须 |
| `finding_pattern` | 研究发现模式 | finding pattern | 论文如何从统计或抽取结果形成 finding、gap、建议或实践影响。 | 增长、覆盖、质量、缺口、实践影响、方法限制等 | 全文文本级 | `guideline不适用` / `原文未报告` | 必须，guideline 可说明不适用 |
| `evidence_presentation_pattern` | 证据呈现模式 | evidence presentation pattern | 论文用哪些表格、分母、搜索日志、质量表、抽取表或图形支撑结论。 | 搜索分母、筛选流程、质量表、主题表、引用表、报告结构 | 全文文本级 | `文本提取缺失` / `尚未阅读` | 必须 |
| `validity_threat_pattern` | 效度威胁模式 | validity / threat pattern | 论文如何报告搜索偏倚、纳排可靠性、质量评价、protocol 偏离、外推限制等。 | bias、selection、quality、protocol deviation、external validity、publication bias | 全文文本级 | `原文未报告` / `尚未阅读` | 必须 |
| `report_structure_pattern` | 报告结构模式 | report structure pattern | 论文整体章节如何组织，以及 RQ 与结果/讨论如何映射。 | IMRaD、Previous studies + Method + Results、Guideline sections 等 | 全文文本级或目录级 | `文本提取缺失` / `尚未阅读` | 建议必须 |
| `review_type` | 综述 / 指南类型 | review type | 条目属于 SLR、SMS、tertiary study、guideline、mapping guideline update 等哪类。 | `SLR` / `SMS` / `tertiary study` / `guideline` / `mapping guideline update` / `other` | 题摘级 | `尚未阅读` | 必须 |
| `predecessor_relation` | 前序综述关系 | predecessor relation | 是否扩展、复现、更新、整合已有综述或 guideline。 | `none` / `extends` / `updates` / `replicates` / `integrates` / `unknown` | 全文文本级；metadata 可候选 | `原文未报告` / `尚未阅读` | 建议必须 |
| `target_se_subfield` | 目标软件工程子领域 | target SE subfield | 论文面向哪个 SE 子领域或横向方法学主题。 | RE、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE、EBSE guideline 等 | 题摘级可候选；全文文本级可采纳 | `尚未阅读` / `横向方法学` / `无法判定` | 必须 |
| `challenge_action_pattern` | 挑战与行动建议模式 | challenge / action pattern | 论文是否把统计观察进一步组织成 research challenge、open issue、future direction 或 action recommendation。 | challenge、open issue、future work、practice recommendation、education recommendation、无 | 全文文本级 | `原文未报告` / `guideline不适用` / `尚未阅读` | 建议必须 |
| `taxonomy_axis` | 分类轴模式 | taxonomy axis pattern | SMS / tertiary 是否建立分类轴或分类树，以及分类轴如何支撑后续统计分析。 | topic、method、artifact、context、benefit、problem、solution、evidence type 等 | 全文文本级 | `原文未报告` / `非SMS不适用` / `尚未阅读` | 建议必须 |
| `problem_solution_pattern` | 问题-方案模式 | problem / solution pattern | 论文是否把领域现状组织为 problem、benefit、solution、practice implication 等可复用 finding pattern。 | problem、benefit、solution、implication、limitation、无 | 全文文本级 | `原文未报告` / `不适用` / `尚未阅读` | 候选 |
| `adoption_status` | 采纳状态 | adoption status | 该字段或 pattern 是否进入后续候选模式库。 | `🟢 已采纳` / `🟡 候选` / `⚪ 未采纳` / `⏳ 待核验` | 取决于字段 | `待核验` | 必须 |

## 5. 字段变更规则

字段变更必须记录：触发论文、触发原因、变更类型、受影响字段、是否需要回填、回填状态和冻结理由。A1 dry-run 已触发 4 类核心回修，并把 2 类 SMS 候选字段留给 A2a 扩展：

1. `review_type`：Kitchenham & Charters 2007 是 guideline，不适合按普通 tertiary study 处理。
2. `predecessor_relation`：da Silva 2011 是 updated tertiary study，需要记录与前序研究的扩展/整合关系。
3. `target_se_subfield`：Bano 2014、Heikkilä 2015、Kotti 2023 表明不同 SE 子领域会产生不同维度模式，必须显式记录。
4. `challenge_action_pattern`：Kotti 2023 显示现代 tertiary study 常把统计观察升级为挑战和行动建议，需要与 Paper2 后续 finding ledger 衔接。
5. `taxonomy_axis` / `problem_solution_pattern`：Heikkilä 2015 暴露 SMS 常见的 taxonomy、problem、solution 结构；A1 先列为候选字段，A2a 用更多 SMS 样本确认取值空间。

## 6. 回填规则

1. 新字段加入后，必须检查所有 A1 dry-run 条目是否需要回填。
2. metadata-only 条目只能回填题摘级字段，例如标题、年份、来源、review type 候选。
3. 已读全文文本条目至少回填六类 pattern 中 4 类。
4. 若回填失败，必须在 [../SUMMARY.md](../SUMMARY.md) 的 schema 修订 / 回填日志中记录。

## 7. dry-run 检查清单

- [x] 至少 3 篇全文文本级 dry-run。
- [x] 至少 1 个 metadata-only / manual-download-needed 失败路径。
- [x] 六类 pattern 中至少 4 类被实际填充。
- [x] 至少 1 个“不适用 / 证据不足”降级记录。
- [x] dry-run 暴露 schema 缺口并已回修字段合同。
