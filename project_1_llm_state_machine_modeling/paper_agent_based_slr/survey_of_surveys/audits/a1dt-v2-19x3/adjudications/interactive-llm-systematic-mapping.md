# A1-DT v2 主线程裁决：interactive-llm-systematic-mapping

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `interactive-llm-systematic-mapping` |
| 论文标题 | On the road to interactive LLM-based systematic mapping studies |
| codex result | [interactive-llm-systematic-mapping__codex.md](../results/interactive-llm-systematic-mapping__codex.md) |
| claude result | [interactive-llm-systematic-mapping__claude.md](../results/interactive-llm-systematic-mapping__claude.md) |
| deepseek result | [interactive-llm-systematic-mapping__deepseek.md](../results/interactive-llm-systematic-mapping__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | proposal；原文自称 solution proposal，不是已执行的 SLR/SMS/tertiary/MLR | solution proposal（作者自述："The research can be classified as a solution proposal"，Page 1 §Method）；既不是 SLR、也不是 SMS、tertiary、MLR；可被视为 vision / roadmap | **solution proposal**（非实证 SLR/SMS/tertiary） | solution proposal（作者自述："The research can be classified as a solution proposal"，Page 1 §Method）；既不是 SLR、也不是 SMS、tertiary、MLR；可被视为 vision / roadmap | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 无系统样本库；降级对象是“LLM-supported mapping process”的流程阶段、agent 角色、交互动作和 proposal guideline item | **无系统样本库**。原文样本单位是"假想 LLM-supported mapping 工作流中的流程阶段 / agent 角色 / 人机交互节点"，不是 primary study | **无系统样本库**。原文没有对任何 primary study / secondary study / tool / artifact / dataset 执行系统检索、纳排、数据抽取或逐单位编码。§2 中各步骤引用的 "Relevant literature" 是说明性例证（illustrative examples），不是通过系统检索与纳排产生的样本集。 | **无系统样本库**。原文样本单位是"假想 LLM-supported mapping 工作流中的流程阶段 / agent 角色 / 人机交互节点"，不是 primary study | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 无 primary/secondary study 分母；可记录的设计元素包括 Fig. 1 的 5 个流程阶段、§2.2.1 的 3 个 search agents、§2.3 的 2 类 coding modes，但这些不是实证样本数 | `not_applicable`。论文 References 仅 10 条，全部以叙事 "Relevant literature" 形式被引，不构成 coded sample；`Data availability: No data was used`（Page 3） | **N/A**。无检索式、无纳入排除流程、无 PRISMA-style 流程图、无样本数量报告。参考文献列表共 10 条，均为介绍性引用或背景支撑。 | `not_applicable`。论文 References 仅 10 条，全部以叙事 "Relevant literature" 形式被引，不构成 coded sample；`Data availability: No data was used`（Page 3） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 降级树 / 方法流程维度森林 | **维度森林（降级）**：①方法流程树（6 阶段） + ②agent/role 树（含 search 阶段 3 agent + 各阶段 LLM/人 双轨） + ③validity/risk 树（Reflections）。无样本编码 schema | **降级树 / 无系统样本库**。原文唯一的"结构"是 mapping study 的 5-step 流程（Fig. 1），以及各步骤的 proposed strategy / agent 角色 / 输入输出 / human-in-the-loop 交互模式。这不是对样本单位的编码维度树，而是对方法流程的分解。 | **维度森林（降级）**：①方法流程树（6 阶段） + ②agent/role 树（含 search 阶段 3 agent + 各阶段 LLM/人 双轨） + ③validity/risk 树（Reflections）。无样本编码 schema | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 否；只能作 `boundary_anchor` / `schema_seed` / 方法学启发，不进入主统计池 | 否。理由：solution proposal；无系统检索、纳排、抽取；与 `metadata.json eligible_for_statistical_synthesis=false`、`evidence_role=solution_proposal_boundary_anchor` 一致。**局部仅可作 schema_seed / boundary_anchor / methodological seed** | **否** — solution proposal；没有已执行的系统检索、纳排与实证合成；`metadata.json` 中 `eligible_for_statistical_synthesis: false` 和 `statistical_pool_exclusion_reason` 的判定与本审计一致。 | 否。理由：solution proposal；无系统检索、纳排、抽取；与 `metadata.json eligible_for_statistical_synthesis=false`、`evidence_role=solution_proposal_boundary_anchor` 一致。**局部仅可作 schema_seed / boundary_anchor / methodological seed** | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | **无系统样本库**。原文样本单位是"假想 LLM-supported mapping 工作流中的流程阶段 / agent 角色 / 人机交互节点"，不是 primary study |
| 样本数量 / 分母 | `not_applicable`。论文 References 仅 10 条，全部以叙事 "Relevant literature" 形式被引，不构成 coded sample；`Data availability: No data was used`（Page 3） |
| 原文类型 | solution proposal（作者自述："The research can be classified as a solution proposal"，Page 1 §Method）；既不是 SLR、也不是 SMS、tertiary、MLR；可被视为 vision / roadmap |
| 原生树 / 森林类型 | **维度森林（降级）**：①方法流程树（6 阶段） + ②agent/role 树（含 search 阶段 3 agent + 各阶段 LLM/人 双轨） + ③validity/risk 树（Reflections）。无样本编码 schema |
| 降级状态 | 不进入主统计池；仅作 boundary / schema seed |
| 主统计池资格 | 否。理由：solution proposal；无系统检索、纳排、抽取；与 `metadata.json eligible_for_statistical_synthesis=false`、`evidence_role=solution_proposal_boundary_anchor` 一致。**局部仅可作 schema_seed / boundary_anchor / methodological seed** |
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
