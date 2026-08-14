# mdse-modelling-assistants-mapping：证据链与结论-证据映射

返回当前正文：[review.md](./review.md)。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见 [review.md](./review.md) 的“维度树复原”正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md](../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-mdse-modelling-assistants-mapping-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-mdse-modelling-assistants-mapping-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-mdse-modelling-assistants-mapping-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-mdse-modelling-assistants-mapping-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mdse-modelling-assistants-mapping-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mdse-modelling-assistants-mapping-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mdse-modelling-assistants-mapping-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见 [review.md](./review.md) 的“维度树复原”叶子维度表和关系边表。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-mdse-modelling-assistants-mapping-type | clm-mdse-modelling-assistants-mapping-type | src-mdse-modelling-assistants-mapping-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见 [review.md](./review.md) 的证据锚点 | 支撑原文类型：SMS（systematic 系统映射研究）+ 实践侧 grey-文献 文档审查（混合：SMS + 实践审查） | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-mdse-modelling-assistants-mapping-unit | clm-mdse-modelling-assistants-mapping-unit | src-mdse-modelling-assistants-mapping-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑样本单位：(a) 原始研究 / 提案（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 文档，产出 15 个 实践 提案） | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-mdse-modelling-assistants-mapping-denom | clm-mdse-modelling-assistants-mapping-denom | src-mdse-modelling-assistants-mapping-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑样本数量 / 分母：文献侧：3,176 筛查 记录 → 77 可能相关→ 58 included；K=0.634（inclusion）/ 0.651（聚类）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 实践 提案 | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-mdse-modelling-assistants-mapping-tree | clm-mdse-modelling-assistants-mapping-tree | src-mdse-modelling-assistants-mapping-text; src-mdse-modelling-assistants-mapping-codex; src-mdse-modelling-assistants-mapping-claude; src-mdse-modelling-assistants-mapping-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见 [review.md](./review.md) 的证据锚点 | 支撑原生树类型：**维度森林**：文献侧系统映射编码模式 一棵树（策略 / 目标 / 限制 / 指标 / 目标用户）+ 实践侧文档编码同一模式 投影一棵子树，外接 Gartner 魔力象限分类（GMQ；首次术语）（LE/C/V/NP）与 文档 状态（D/NF） | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-mdse-modelling-assistants-mapping-limitation-conflict | clm-mdse-modelling-assistants-mapping-limitation-conflict | src-mdse-modelling-assistants-mapping-text | paper_content.txt | 待 A2a | §4.3 / Table 3 | 待 A2a | Table 3 | “five 限制 聚类”与 L1--L6 表格口径不一致 | 支撑 `leaf.limitation_cluster` 的内部冲突：正文称 five，表格列出 6 类限制加 L-NS；A2a 必须回 PDF / Zenodo 精核后才能统计该叶子 | internal_inconsistency | not_verified | leaf.limitation_cluster | 是 | 否 | -- | 不得把 limitation_cluster 写成 final 统计结论 |
| ev-mdse-modelling-assistants-mapping-pool | clm-mdse-modelling-assistants-mapping-pool | src-mdse-modelling-assistants-mapping-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见 [review.md](./review.md) 的叶子表 / 关系边表。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-mdse-modelling-assistants-mapping-type | A1DT-mdse-modelling-assistants-mapping-C01 | 本文原文类型为：SMS（systematic 系统映射研究）+ 实践侧 grey-文献 文档审查（混合：SMS + 实践审查） | paper_type | type | ev-mdse-modelling-assistants-mapping-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-mdse-modelling-assistants-mapping-unit | A1DT-mdse-modelling-assistants-mapping-C02 | 本文被编码样本单位为：(a) 原始研究 / 提案（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 文档，产出 15 个 实践 提案） | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-mdse-modelling-assistants-mapping-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-mdse-modelling-assistants-mapping-tree | A1DT-mdse-modelling-assistants-mapping-C03 | 本文原生维度树 / 维度森林为：**维度森林**：文献侧系统映射编码模式 一棵树（策略 / 目标 / 限制 / 指标 / 目标用户）+ 实践侧文档编码同一模式 投影一棵子树，外接 Gartner 魔力象限分类（GMQ；首次术语）（LE/C/V/NP）与 文档 状态（D/NF） | 树类型（tree_type） | native_tree | ev-mdse-modelling-assistants-mapping-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-mdse-modelling-assistants-mapping-limitation-conflict | A1DT-mdse-modelling-assistants-mapping-C05 | 本文限制聚类存在正文“五类”与 Table 3 “L1--L6”不一致；该叶子当前只能作为待核验冲突证据，A2a 前不得进入定量统计。 | internal_inconsistency | leaf.limitation_cluster | ev-mdse-modelling-assistants-mapping-limitation-conflict | A2a 需回 PDF / Zenodo 精核 | not_verified；待 A2a 原文版面锚定 | A2a 精核清单 / 风险提示 | 否 | -- |
| clm-mdse-modelling-assistants-mapping-pool | A1DT-mdse-modelling-assistants-mapping-C04 | 本文统计池资格为：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见 [review.md](./review.md) 的叶子表 / 关系边表。 | eligibility | 统计池（statistical_pool） | ev-mdse-modelling-assistants-mapping-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-mdse-modelling-assistants-mapping-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-mdse-modelling-assistants-mapping-limitation-conflict | 限制聚类 five / L1--L6 口径冲突 | 人工打开 `paper.pdf` 与 Zenodo / supplementary，核对 §4.3 与 Table 3 是否有脚注解释 L6 | 明确采用 5 类、6 类或作者勘误口径，并回填 `leaf.limitation_cluster` | A2a 待办 |
| chk-mdse-modelling-assistants-mapping-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-mdse-modelling-assistants-mapping-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
