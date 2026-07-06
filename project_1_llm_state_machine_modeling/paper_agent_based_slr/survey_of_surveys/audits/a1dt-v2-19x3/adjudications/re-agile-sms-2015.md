# A1-DT v2 主线程裁决：re-agile-sms-2015

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-agile-sms-2015` |
| 论文标题 | A Mapping Study on Requirements Engineering in Agile Software Development |
| codex result | [re-agile-sms-2015__codex.md](../results/re-agile-sms-2015__codex.md) |
| claude result | [re-agile-sms-2015__claude.md](../results/re-agile-sms-2015__claude.md) |
| deepseek result | [re-agile-sms-2015__deepseek.md](../results/re-agile-sms-2015__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SMS / systematic mapping study。 | systematic mapping study (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 mapping study。 | SMS（systematic mapping study）。作者自述 method 为 "mapping study [18]"（[18] = Kitchenham & Charters, 2007），符合 Petersen et al. 的 SMS 方法论。 | systematic mapping study (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 mapping study。 | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 纳入的 28 篇 primary articles / primary studies，即文中 `[S1]`--`[S28]`。 | primary study（28 篇敏捷 RE 原始研究，编号 S1–S28）。 | primary study（研究文章）。纳入 28 篇 peer-reviewed 文章，对每篇文章进行元数据提取 + 主题分类 + benefit/problem/solution 编码。 | primary study（28 篇敏捷 RE 原始研究，编号 S1–S28）。 | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | Scopus 初检 241；去除非 journal/conference 46、非英语 8 后标题摘要筛 187；排除 123 后全文候选 65；全文排除 37；最终纳入 28。 | 241（搜索命中）→ 187（去除非 journal/conference 与非英文）→ 65（标题/摘要筛选后）→ **28**（全文筛选后的最终纳入数 = 主统计分母）。 | **28** / 初始搜索 241 → 去除非 English/非 article 54 → 标题摘要筛选 187 → 全文筛选 65 → 最终纳入 28。 | 241（搜索命中）→ 187（去除非 journal/conference 与非英文）→ 65（标题/摘要筛选后）→ **28**（全文筛选后的最终纳入数 = 主统计分母）。 | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林。核心为“纳入论文 metadata/context/methods/results 抽取”加“benefit/problem/solution 主题编码”和若干 article-level 分类表。 | 维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 schema。 | **维度森林（dimension forest）**。论文对同一组 28 个样本沿多个独立分类轴进行编码：出版属性轴、研究方法轴、敏捷方法上下轴、RE 主题分类轴、收益轴（B1–B6）、问题轴（P1–P6）、方案轴（与问题多对多映射）。各轴之间非树形 strict hierarchy，而是平行分类 + 交叉统计。 | 维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 schema。 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计。28 篇样本、纳排链、Table I--V 的分类和多对多 article-code 关系可统计；discussion 中领域解释与未来研究建议只能作候选 finding。 | **是**（局部可统计）：venue 频次、agile-method context、article-type、B1–B6 频次与引用集合、P1–P6 频次与引用集合、P→solution 关系覆盖，均可基于原文表统计；分母清晰 N=28。Definition 与 future-work 仅作 candidate finding，不入主统计。 | **是**。SMS 有系统检索策略（Scopus）、显式纳排标准、结构化数据抽取表单、主题编码方案、统计分布报告（N=28 的频次和百分比）。可进入统计池，但需注意样本小（28）、单数据库（Scopus）、无质量评价（no quality appraisal），不宜做效应量合成。 | **是**（局部可统计）：venue 频次、agile-method context、article-type、B1–B6 频次与引用集合、P1–P6 频次与引用集合、P→solution 关系覆盖，均可基于原文表统计；分母清晰 N=28。Definition 与 future-work 仅作 candidate finding，不入主统计。 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | primary study（28 篇敏捷 RE 原始研究，编号 S1–S28）。 |
| 样本数量 / 分母 | 241（搜索命中）→ 187（去除非 journal/conference 与非英文）→ 65（标题/摘要筛选后）→ **28**（全文筛选后的最终纳入数 = 主统计分母）。 |
| 原文类型 | systematic mapping study (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 mapping study。 |
| 原生树 / 森林类型 | 维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 schema。 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / 待原文版面核验 管理；不得视为已完成核验 |
| 主统计池资格 | **是**（局部可统计）：venue 频次、agile-method context、article-type、B1–B6 频次与引用集合、P1–P6 频次与引用集合、P→solution 关系覆盖，均可基于原文表统计；分母清晰 N=28。Definition 与 future-work 仅作 candidate finding，不入主统计。 |
| 不确定项 | 三路审计在核心方向上基本一致；若树型/分母存在细节差异，主线程采用原文证据更具体且与 metadata/正文一致的一路。 |

## 3. review.md 必改清单

| 小节 | 必改动作 | 证据来源 | 完成状态 |
|---|---|---|---|
| `## 维度树复原` | 删除六叶通用接口作为主树的写法，改为原文原生样本编码树 / 维度森林。 | 三路 result §3--§5 | 已在本 PR 重写 |
| 叶子维度表 | 写清每个核心叶子的定义、取值空间、缺失值语义、统计用途和迁移边界。 | 三路 result §4 | 已在本 PR 重写 |
| 关系边表 | 对多维度交叉、sample→field、theme→finding、roadmap→action 等关系显式表化。 | 三路 result §5 | 已在本 PR 重写 |
| 统计观察 / finding 边界 | 区分统计观察、候选 finding、final finding 禁区和可迁移方法学启发。 | 三路 result §6 | 已在本 PR 重写 |
| A.1--A.4 审计附录 | 保留来源、证据账本、结论-证据映射和复验命令；证据强度不足处降级。 | 三路 result §8 | 已在本 PR 重写 |

## 4. SUMMARY / patterns 回填触发

| 目标文件 | 触发条件 | 应改字段 | 当前动作 | 风险 |
|---|---|---|---|---|
| `SUMMARY.md` | A1-DT v2 三路审计完成且主线程裁决落地。 | v2 审计状态、样本单位、树型、统计池资格。 | 已统一将 v2 状态回填为 `completed`，并保留 A2a 精核边界。 | 若 A2a 精核修正页码或分母，需再次回填。 |
| `patterns/pattern-field-schema.md` | 单篇 A.3 结论可跨论文复用。 | 暂不新增实证 pattern，只维持 schema 接口。 | 本 PR 不新增跨论文 final pattern。 | 过早归纳会污染 Paper2 story。 |

## 5. 未解决风险与 A2a 接力

| 风险 | 等级 | 为什么不能在 A1-DT v2 关闭 | A2a 接力动作 |
|---|---|---|---|
| PDF 页码 / 表图版面未逐项人工核验 | I | v2 目标是冻结原生树和证据链，不承担完整页码级最终审计。 | 对关键表、图、附录和 replication package 做视觉核验。 |
| 三路 agent 个别分母或树型判断冲突 | I | 已由主线程裁决当前采用口径，但正式定量统计前仍需人工复核。 | 在 A2a 使用 `paper.pdf` / supplementary 复核冲突行。 |
| 领域结论误迁移风险 | C（若发生） | 本 PR 只学习综述如何建模样本，不迁移目标领域事实。 | SUMMARY 和 paper story 中只使用 schema / 方法学启发。 |

## 6. 复验命令

| 检查 | 命令 / 人工动作 | 通过条件 | 当前状态 |
|---|---|---|---|
| v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 19 个 adjudication、57 个 result、57 个 log 和 19 篇 review 均存在且路径正确。 | 待最终运行 |
| Markdown 基础检查 | `git diff --check` | 无尾随空白和冲突标记。 | 待最终运行 |
