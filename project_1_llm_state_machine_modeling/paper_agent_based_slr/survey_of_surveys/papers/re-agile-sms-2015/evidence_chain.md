# re-agile-sms-2015：证据链与结论-证据映射

返回当前正文：[review.md](./review.md)。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见 [review.md](./review.md) 的“维度树复原”正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/re-agile-sms-2015.md](../../audits/a1dt-v2-19x3/adjudications/re-agile-sms-2015.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-re-agile-sms-2015-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-re-agile-sms-2015-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-re-agile-sms-2015-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-re-agile-sms-2015-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-re-agile-sms-2015-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-re-agile-sms-2015-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-re-agile-sms-2015-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/re-agile-sms-2015.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见 [review.md](./review.md) 的“维度树复原”叶子维度表和关系边表。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-re-agile-sms-2015-type | clm-re-agile-sms-2015-type | src-re-agile-sms-2015-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见 [review.md](./review.md) 的证据锚点 | 支撑原文类型：systematic 系统映射研究 (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 系统映射研究。 | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-re-agile-sms-2015-unit | clm-re-agile-sms-2015-unit | src-re-agile-sms-2015-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑样本单位：原始研究（28 篇敏捷 RE 原始研究，编号 S1–S28）。 | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-re-agile-sms-2015-denom | clm-re-agile-sms-2015-denom | src-re-agile-sms-2015-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑样本数量 / 分母：241（搜索命中）→ 187（去除非 journal/conference 与非英文）→ 65（标题/摘要筛选后）→ **28**（全文筛选后的最终纳入数 = 主统计分母）。 | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-re-agile-sms-2015-tree | clm-re-agile-sms-2015-tree | src-re-agile-sms-2015-text; src-re-agile-sms-2015-codex; src-re-agile-sms-2015-claude; src-re-agile-sms-2015-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑原生树类型：维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 schema。 | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-re-agile-sms-2015-pool | clm-re-agile-sms-2015-pool | src-re-agile-sms-2015-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见 [review.md](./review.md) 的叶子表 / 关系边表。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-re-agile-sms-2015-type | A1DT-re-agile-sms-2015-C01 | 本文原文类型为：systematic 系统映射研究 (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 系统映射研究。 | paper_type | type | ev-re-agile-sms-2015-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-re-agile-sms-2015-unit | A1DT-re-agile-sms-2015-C02 | 本文被编码样本单位为：原始研究（28 篇敏捷 RE 原始研究，编号 S1–S28）。 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-re-agile-sms-2015-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-re-agile-sms-2015-tree | A1DT-re-agile-sms-2015-C03 | 本文原生维度树 / 维度森林为：维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 schema。 | 树类型（tree_type） | native_tree | ev-re-agile-sms-2015-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-re-agile-sms-2015-pool | A1DT-re-agile-sms-2015-C04 | 本文统计池资格为：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见 [review.md](./review.md) 的叶子表 / 关系边表。 | eligibility | 统计池（statistical_pool） | ev-re-agile-sms-2015-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-re-agile-sms-2015-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-re-agile-sms-2015-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-re-agile-sms-2015-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
