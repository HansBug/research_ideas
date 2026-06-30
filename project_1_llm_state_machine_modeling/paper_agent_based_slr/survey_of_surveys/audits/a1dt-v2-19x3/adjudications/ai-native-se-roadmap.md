# A1-DT v2 主线程裁决：ai-native-se-roadmap

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `ai-native-se-roadmap` |
| 论文标题 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap |
| codex result | [ai-native-se-roadmap__codex.md](../results/ai-native-se-roadmap__codex.md) |
| claude result | [ai-native-se-roadmap__claude.md](../results/ai-native-se-roadmap__claude.md) |
| deepseek result | [ai-native-se-roadmap__deepseek.md](../results/ai-native-se-roadmap__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | roadmap / vision；不是 SLR、SMS、tertiary 或 MLR | **vision / roadmap / proposal**（自我定位）；不是 SLR、SMS、tertiary、MLR、guideline 检索研究 | **vision / roadmap**（非 SLR、SMS、tertiary、MLR、guideline） | **vision / roadmap / proposal**（自我定位）；不是 SLR、SMS、tertiary、MLR、guideline 检索研究 | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 无系统样本库；可降级描述为 vision item、technology-stack component、roadmap challenge、open question | 不存在系统样本库；原生编码对象是 **{SE 1.0/2.0/3.0 三时代 baseline}**、**{Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next 五层技术栈组件}** 和 **{6 个主 challenge + OQ1–OQ14 共 14 个 open question}** | **无系统样本库**——论文以作者愿景和经验组织叙事，没有检索、纳排、数据抽取或质量评价协议 | 不存在系统样本库；原生编码对象是 **{SE 1.0/2.0/3.0 三时代 baseline}**、**{Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next 五层技术栈组件}** 和 **{6 个主 challenge + OQ1–OQ14 共 14 个 open question}** | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 无系统统计分母；原文可描述对象包括 5 个技术栈组件、5 个主挑战段落、OQ1--OQ14，但这些不是纳排样本 | 不适用为统计分母；可记录的"原生项数"：3 个时代、5 个 stack component、6 个主 challenge、14 个 OQ；引用 [1]–[117] 共 117 条，但作者未声明任何检索 / 纳排，因此 117 不是 SLR 分母 | **不适用**——不存在系统样本分母 | 不适用为统计分母；可记录的"原生项数"：3 个时代、5 个 stack component、6 个主 challenge、14 个 OQ；引用 [1]–[117] 共 117 条，但作者未声明任何检索 / 纳排，因此 117 不是 SLR 分母 | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 降级树 / 维度森林：SE evolution 概念树 + SE 3.0 技术栈树 + challenge roadmap 树 | **降级树（roadmap/challenge 树）+ 辅助"era baseline 对照树"**；不是 SLR 维度森林 | **降级树**（roadmap / challenge 分类树）——论文以自身的“SE 演化基线 → SE 2.0 局限 → SE 3.0 五层技术栈 → 五大挑战 + 8 个其他开放问题”为原生组织 schema | **降级树（roadmap/challenge 树）+ 辅助"era baseline 对照树"**；不是 SLR 维度森林 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 否；无系统检索、纳排、质量评价、数据抽取表或可统计 primary / secondary study 分母 | **否**；与 `metadata.json` 中 `eligible_for_statistical_synthesis: false`、`evidence_role: roadmap_boundary_anchor`、`systematic_evidence_status: non_systematic_or_boundary_anchor` 一致 | **否**——不可进入主统计池；仅作 `boundary_anchor` + `schema_seed`。理由是：vision/roadmap 类文献无系统检索、纳排、质量评价或数据综合 | **否**；与 `metadata.json` 中 `eligible_for_statistical_synthesis: false`、`evidence_role: roadmap_boundary_anchor`、`systematic_evidence_status: non_systematic_or_boundary_anchor` 一致 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | 不存在系统样本库；原生编码对象是 **{SE 1.0/2.0/3.0 三时代 baseline}**、**{Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next 五层技术栈组件}** 和 **{6 个主 challenge + OQ1–OQ14 共 14 个 open question}** |
| 样本数量 / 分母 | 不适用为统计分母；可记录的"原生项数"：3 个时代、5 个 stack component、6 个主 challenge、14 个 OQ；引用 [1]–[117] 共 117 条，但作者未声明任何检索 / 纳排，因此 117 不是 SLR 分母 |
| 原文类型 | **vision / roadmap / proposal**（自我定位）；不是 SLR、SMS、tertiary、MLR、guideline 检索研究 |
| 原生树 / 森林类型 | **降级树（roadmap/challenge 树）+ 辅助"era baseline 对照树"**；不是 SLR 维度森林 |
| 降级状态 | 不进入主统计池；仅作 boundary / schema seed |
| 主统计池资格 | **否**；与 `metadata.json` 中 `eligible_for_statistical_synthesis: false`、`evidence_role: roadmap_boundary_anchor`、`systematic_evidence_status: non_systematic_or_boundary_anchor` 一致 |
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
