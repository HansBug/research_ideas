# A1-DT v2 主线程裁决：llm4se-systematic-review

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm4se-systematic-review` |
| 论文标题 | Large Language Models for Software Engineering: A Systematic Literature Review |
| codex result | [llm4se-systematic-review__codex.md](../results/llm4se-systematic-review__codex.md) |
| claude result | [llm4se-systematic-review__claude.md](../results/llm4se-systematic-review__claude.md) |
| deepseek result | [llm4se-systematic-review__deepseek.md](../results/llm4se-systematic-review__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SLR | SLR（Kitchenham-style；明确声明遵循 Kitchenham et al. [197,198] 方法学，§2 首段） | SLR（Systematic Literature Review）。遵循 Kitchenham 方法学；有系统检索、纳排标准、质量评估、数据抽取表（Table 5）、编码方案、统计分析与附录全文引用表。 | SLR（Kitchenham-style；明确声明遵循 Kitchenham et al. [197,198] 方法学，§2 首段） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | LLM4SE primary study / research paper；最终纳入 395 篇，部分字段允许一篇论文有多个取值或任务实例。 | primary study（一篇被纳入的 LLM4SE research paper），最终 N=395。 | primary study（单篇 LLM4SE 研究论文）。最终纳入 395 篇，覆盖 2017-01 至 2024-01-31。 | primary study（一篇被纳入的 LLM4SE research paper），最终 N=395。 | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 395 篇总样本；质量评估后 382 篇 + snowballing 追加 13 篇。若字段缺失，作者使用局部分母，例如 dataset source 明示 374 篇、input form 明示 355 篇。 | 主分母 N=395。子分母：N=374（显式说明 dataset）；N=355（显式说明 input form）；N=154（peer-reviewed）+ 241（arXiv）；按年 7/13/56/273/46（2020–2024.01）。 | 395（检索 218,765 条 → 自动筛选 → 全文扫描 594 → 质量评估 382 → snowballing +13 = 395）。其中 peer-reviewed venue 154 篇，arXiv 241 篇。 | 主分母 N=395。子分母：N=374（显式说明 dataset）；N=355（显式说明 input form）；N=154（peer-reviewed）+ 241（arXiv）；按年 7/13/56/273/46（2020–2024.01）。 | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：RQ 驱动的多棵分类/统计树，核心为“LLM 模型—数据—优化/评价—SE 任务”，并辅以检索/质量门与 challenges/roadmap。 | 维度森林。根为 4 个 RQ，每个 RQ 各自展开一棵编码树（RQ1 模型、RQ2 数据、RQ3 优化与评价、RQ4 任务），通过 Table 5 的 8 项 data items 串联。 | **维度森林**（Dimension Forest）。以四个 RQ 为主干、每个 RQ 挂载 2--6 个编码层级的分类学（taxonomy）/ 抽取字段表（extraction form），叶子分布在 LLM 架构、数据源/类型/预处理/输入形式、优化/评价策略、SE activity/task 四个维度域中，互相正交但同源（同一批 395 篇 primary studies）。 | 维度森林。根为 4 个 RQ，每个 RQ 各自展开一棵编码树（RQ1 模型、RQ2 数据、RQ3 优化与评价、RQ4 任务），通过 Table 5 的 8 项 data items 串联。 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计。可进入“系统综述如何构造字段树/统计表”的方法学统计池；不得作为 Paper2 目标领域 final finding 或 LLM4STM 领域事实池直接使用。 | 是（局部可统计）。该文是 systematic_review，有明确分母、纳排、QAC 与 Appendix 锚定；其分类频次（如 architecture × year、data_source、input_form、SDLC activity、metric × problem_type）可作为正式可统计 schema。但当前单篇 review.md 中具体数字未逐一回 Table 13–17 精核，部分百分比口径（task instance vs paper count）仍存在分母歧义，须 A2a 锚定。 | **是**。该文是一级 SLR（非 tertiary/umbrella review、非 roadmap/guideline，有系统样本库与编码方案），可参与跨论文 schema 统计。但注意：其领域是 LLM4SE，不是 LLM4STM/formal methods；其统计值只能作为「SLR 字段设计模式」和「SE SLR 编码树结构样本」迁移，领域结论不可迁移。 | 是（局部可统计）。该文是 systematic_review，有明确分母、纳排、QAC 与 Appendix 锚定；其分类频次（如 architecture × year、data_source、input_form、SDLC activity、metric × problem_type）可作为正式可统计 schema。但当前单篇 review.md 中具体数字未逐一回 Table 13–17 精核，部分百分比口径（task instance vs paper count）仍存在分母歧义，须 A2a 锚定。 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | primary study（一篇被纳入的 LLM4SE research paper），最终 N=395。 |
| 样本数量 / 分母 | 主分母 N=395。子分母：N=374（显式说明 dataset）；N=355（显式说明 input form）；N=154（peer-reviewed）+ 241（arXiv）；按年 7/13/56/273/46（2020–2024.01）。 |
| 原文类型 | SLR（Kitchenham-style；明确声明遵循 Kitchenham et al. [197,198] 方法学，§2 首段） |
| 原生树 / 森林类型 | 维度森林。根为 4 个 RQ，每个 RQ 各自展开一棵编码树（RQ1 模型、RQ2 数据、RQ3 优化与评价、RQ4 任务），通过 Table 5 的 8 项 data items 串联。 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / text_verified 管理 |
| 主统计池资格 | 是（局部可统计）。该文是 systematic_review，有明确分母、纳排、QAC 与 Appendix 锚定；其分类频次（如 architecture × year、data_source、input_form、SDLC activity、metric × problem_type）可作为正式可统计 schema。但当前单篇 review.md 中具体数字未逐一回 Table 13–17 精核，部分百分比口径（task instance vs paper count）仍存在分母歧义，须 A2a 锚定。 |
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
