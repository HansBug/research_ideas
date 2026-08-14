# A1-DT v2 单篇全文审计任务

你是 deepseek reviewer / auditor。本任务必须由真实 codex-deepseek exec 进程独立完成。

## 0. 绝对硬约束

1. 你只能处理本任务指定的 **一篇论文**：`research-artifacts-secondary-studies`。
2. 禁止启动 subagent、sub-subagent、nested agent、后台 agent 或让其他模型替你读文。
3. 禁止修改仓库文件、禁止 commit、禁止 push、禁止 gh comment；只输出本任务的 Markdown 审计结果。
4. 必须基于本地文件全文阅读；不能只看摘要、只 grep 关键词或只复述已有 `review.md`。
5. 必须显式使用并在输出中记录以下本地技能 / 指南文件：
   - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
   - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
   - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
   - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
   - `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
   - `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`
   - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
6. 你必须先读这些技能 / 指南文件的相关内容，再读本文献材料。若某文件无法读取，必须记录为 `blocked` 风险。
7. 严禁把 A1-M0--M6、patterns/ 或旧 v1 审计结果当成单篇原生树模板。A1-M0--M6 只能作为跨论文投影提示。
8. 如果原文证据不足，请降级为 `not_verified` / `weak` / `schema_seed`，不要编造表格、页码、取值空间或作者结论。
9. 输出必须中文为主；必要英文术语首次出现用“中文（English）”格式，之后优先中文。
10. **最终回答必须就是完整审计报告正文**，不能写“见上一条消息”“见前文”“完整报告已在上文”等不可审计引用；也不能只给摘要。若输出过长，也必须在最终回答中保留所有必填章节的实质内容。

## 1. 当前任务论文

- slug: `research-artifacts-secondary-studies`
- paper_dir: `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies`
- bibtex: `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies/bibtex.bib`
- metadata: `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies/metadata.json`
- text: `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies/paper_content.txt`
- pdf: `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies/paper.pdf`
- existing review: `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies/review.md`

你必须读取：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。若需要核对表格 / 图 / 附录，可以读取 `paper.pdf` 或用本地工具抽取，但必须说明是否做过 PDF 版面核验。

## 2. A1-DT v2 口径（必须遵守）

维度树 / 维度森林 = 这篇综述论文如何描述、编码、分类、统计它纳入的样本单位的层级化字段结构。

它不是：

- 不是所有论文共享模板；
- 不是 RQ 列表本身；
- 不是综述流程本身；
- 不是 discussion / conclusion finding 列表本身；
- 不是 A1-M0--M6 跨论文投影；
- 不是 reviewer 主观套上的“范围 / 语料 / 分类 / 方法 / 证据 / finding”六叶模板。

必须先判定样本单位，再复原字段结构。样本单位可以是 primary study、secondary study、tool、artifact、dataset、guideline item、roadmap action、claim / finding，或“无系统样本库”。

如果是 roadmap / vision / proposal / guideline 且无系统样本库，必须降级：可作 boundary anchor / methodological seed / candidate heuristic，不进入主统计池。

## 3. 你要输出的 Markdown 结构

请严格按以下结构输出。每一节都要写，不适用也要说明理由。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `research-artifacts-secondary-studies` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是 / 否 + 说明 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是 / 否 + 说明 |
| 是否打开或核对 `paper.pdf` | 是 / 否 + 说明 |
| 原文类型 | SLR / SMS / tertiary / MLR / guideline / roadmap / proposal / other |
| 被编码样本单位 | ... |
| 样本数量 / 分母 | ... |
| 原生树类型 | 单树 / 维度森林 / 降级树 / 无系统样本库 |
| 主统计池资格 | 是 / 否 / 局部可统计 + 理由 |
| 总体判定 | pass / needs repair / blocked |

### 1. 原文证据阅读说明

- 说明你实际读取了哪些文件、哪些章节、哪些表 / 图 / 附录。
- 说明是否只基于 text，哪些地方仍需 PDF 视觉核验。
- 列出 5--12 个最关键的原文证据锚点：章节名、段落线索、表图编号、短引或释义。注意短引每条控制在很短范围。

### 2. 样本单位与字段来源判定

必须回答：

1. 原文纳入和逐项描述的对象是什么？
2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？
3. 原文字段来自哪里：extraction form、classification schema、taxonomy、quality rubric、mapping table、appendix、replication package、roadmap / guideline item？
4. RQ 与样本单位是什么关系：RQ 是树根、字段用途，还是结果组织方式？
5. 若无系统样本库，如何降级？

### 3. 原生样本编码维度树 / 维度森林

用 text tree 或 Markdown 表给出该论文自己的原生维度树 / 维度森林。要求：

- 至少包含根对象、主干节点、叶子字段；
- 叶子字段必须尽量来自原文；
- 不要用六个通用接口叶子替代原文结构；
- 对每个叶子给出取值空间类型：完整枚举 / 层级枚举 / 布尔 / 数值或区间 / 关系值 / 外部分类法引用 / 自由文本加理由 / 待核验；
- 若原文树很大，可以列核心主干 + 代表性叶子，但必须说明缺失部分和 A2a 精核任务。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|

如果没有关系型 schema，也要说明“未发现显式关系边”，并列出为何不适用。

### 6. 统计观察、候选 finding 与 final finding 边界

区分：

- 原文中由字段 / 统计表支持的统计观察；
- 原文 discussion / recommendation / roadmap 提出的候选 finding；
- 对 Paper2 可迁移的方法学启发；
- 绝不能迁移的领域结论。

### 7. 对现有 `review.md` 的返修建议

以 C/I/M 分级给出最小返修建议。特别检查：

- 是否仍把六个通用 leaf 当成原文树；
- 是否需要重写“维度树复原”；
- 是否需要新增 / 删除 / 合并节点；
- 是否需要补 A.1--A.4；
- SUMMARY 当前表中“样本单位 / 样本数量 / 原生树类型 / 统计池资格”是否需要修正。

### 8. 审计附录草案：证据账本与结论映射

给出可直接迁移到 `review.md` 的 A.2 / A.3 草案。表头用中文。

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|

### 9. 技能使用与自我审查记录

- 列出你读取的技能文件和从中采用的原则。
- 用 reviewer 视角列出本输出最高风险的 3 点，以及如何在主线程合并时复核。
- 明确本任务是否出现 blocked / timeout / 文件缺失。

## 4. 输出质量要求

1. 证据优先：没有证据就降级。
2. 维度树要“像这篇论文自己的编码表 / 分类框架”，不要像通用 SLR checklist。
3. 结论要能被主线程直接用于重写 `review.md`。
4. 不要写成泛泛论文总结；重点是样本编码 schema、取值空间、证据链和返修建议。
5. 若你发现当前 PR body / GUIDE 规则本身有问题，也可在 C/I/M 中指出，但仍需完成该 paper 审计。
6. 最终输出必须是自包含完整报告；不得引用“上一条消息”或隐藏在工具调用 / 中间消息中的内容。
