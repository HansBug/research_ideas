# re-tertiary-study-2014：证据链与结论-证据映射

返回当前正文：[review.md](./review.md)。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见 [review.md](./review.md) 的“维度树复原”正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/re-tertiary-study-2014.md](../../audits/a1dt-v2-19x3/adjudications/re-tertiary-study-2014.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-re-tertiary-study-2014-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-re-tertiary-study-2014-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-re-tertiary-study-2014-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-re-tertiary-study-2014-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-re-tertiary-study-2014-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-re-tertiary-study-2014-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/re-tertiary-study-2014__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-re-tertiary-study-2014-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/re-tertiary-study-2014.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见 [review.md](./review.md) 的“维度树复原”叶子维度表和关系边表。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-re-tertiary-study-2014-type | clm-re-tertiary-study-2014-type | src-re-tertiary-study-2014-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见 [review.md](./review.md) 的证据锚点 | 支撑原文类型：tertiary study（系统映射 tertiary study；按 §II 标题"Systematic Mapping Tertiary Study"，作者明确按 Kitchenham EBSE guidelines 执行） | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-re-tertiary-study-2014-unit | clm-re-tertiary-study-2014-unit | src-re-tertiary-study-2014-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑样本单位：**distinct SLR（study）**。作者把"同一项 SLR 的多份发表"用 `S-ID + [A][B][C]` 合并为一个 study；分子粒度是 study，分母两套：64 publications 与 53 studies | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-re-tertiary-study-2014-denom | clm-re-tertiary-study-2014-denom | src-re-tertiary-study-2014-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑样本数量 / 分母：53 distinct SLR（含 12 SMS、1 meta-analysis、其余 conventional SLR）/ 64 publications（31 conf + 16 journal + 4 workshop + 4 tech report + 8 thesis + 1 unknown）；QA 仅在 51 个 study 上施加（S3、S8 全文不可获得） | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-re-tertiary-study-2014-tree | clm-re-tertiary-study-2014-tree | src-re-tertiary-study-2014-text; src-re-tertiary-study-2014-codex; src-re-tertiary-study-2014-claude; src-re-tertiary-study-2014-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑原生树类型：**维度森林**：①抽取表（出版元数据（publication metadata）+ 原始研究数量（#PS）+ 关注点（focus））；②scope 分类（Table IV）；③topic-group taxonomy（Table V）；④QA rubric（Table I, QA1–QA4 三档 Yes/Partial/No）；⑤citation/impact 评估（Table VI）；⑥缺口分类法（gap taxonomy：异常 / 缺少原始研究 / ignored-areas，§III RQ3）；⑦publication-type 分类（Table III） | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-re-tertiary-study-2014-pool | clm-re-tertiary-study-2014-pool | src-re-tertiary-study-2014-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见 [review.md](./review.md) 的叶子表 / 关系边表。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-re-tertiary-study-2014-type | A1DT-re-tertiary-study-2014-C01 | 本文原文类型为：tertiary study（系统映射 tertiary study；按 §II 标题"Systematic Mapping Tertiary Study"，作者明确按 Kitchenham EBSE guidelines 执行） | paper_type | type | ev-re-tertiary-study-2014-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-re-tertiary-study-2014-unit | A1DT-re-tertiary-study-2014-C02 | 本文被编码样本单位为：**distinct SLR（study）**。作者把"同一项 SLR 的多份发表"用 `S-ID + [A][B][C]` 合并为一个 study；分子粒度是 study，分母两套：64 publications 与 53 studies | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-re-tertiary-study-2014-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-re-tertiary-study-2014-tree | A1DT-re-tertiary-study-2014-C03 | 本文原生维度树 / 维度森林为：**维度森林**：①抽取表（出版元数据（publication metadata）+ 原始研究数量（#PS）+ 关注点（focus））；②scope 分类（Table IV）；③topic-group taxonomy（Table V）；④QA rubric（Table I, QA1–QA4 三档 Yes/Partial/No）；⑤citation/impact 评估（Table VI）；⑥缺口分类法（gap taxonomy：异常 / 缺少原始研究 / ignored-areas，§III RQ3）；⑦publication-type 分类（Table III） | 树类型（tree_type） | native_tree | ev-re-tertiary-study-2014-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-re-tertiary-study-2014-pool | A1DT-re-tertiary-study-2014-C04 | 本文统计池资格为：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见 [review.md](./review.md) 的叶子表 / 关系边表。 | eligibility | 统计池（statistical_pool） | ev-re-tertiary-study-2014-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-re-tertiary-study-2014-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-re-tertiary-study-2014-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-re-tertiary-study-2014-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
