# A1-DT v2 主线程裁决：mdse-modelling-assistants-mapping

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `mdse-modelling-assistants-mapping` |
| 论文标题 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping |
| codex result | [mdse-modelling-assistants-mapping__codex.md](../results/mdse-modelling-assistants-mapping__codex.md) |
| claude result | [mdse-modelling-assistants-mapping__claude.md](../results/mdse-modelling-assistants-mapping__claude.md) |
| deepseek result | [mdse-modelling-assistants-mapping__deepseek.md](../results/mdse-modelling-assistants-mapping__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SMS / systematic mapping；另含 practice documentation review，不是 tertiary review | SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） | SLR（Systematic Literature Review）/ SMS（Systematic Mapping Study）混合——作者自称 "multivocal literature mapping" | SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 主单位：literature 中的 modelling assistance proposal；实践侧辅单位：GMQ 工具文档中的 documented modelling assistance proposal / feature | (a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） | primary studies（论文 / 工具 / 方法论文） | (a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | literature：3,176 screened records -> 58 included proposals；practice：17 GMQ low-code tools -> 7 tools with documentation -> 15 documented proposals | 文献侧：3,176 screened records → 77 possible → 58 included；K=0.634（inclusion）/ 0.651（clustering）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 practice proposals | 51 篇 primary studies（search 阶段检出 1867 → screening 后 51） | 文献侧：3,176 screened records → 77 possible → 58 included；K=0.634（inclusion）/ 0.651（clustering）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 practice proposals | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：literature proposal 编码森林 + practice documentation proposal 编码森林 + quality rubric / cross-tab 关系层 | **维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） | 维度森林（multi-facet classification，每组分类维度独立成树，不是一棵单一大一统树） | **维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计：可统计原文 58 proposals 与 15 practice proposals 的原文维度；对 Paper2 只能作 schema_seed / boundary anchor，不得迁移领域结论 | 局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 | 是——有系统检索、纳排、逐篇数据抽取和编码框架 | 局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | (a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） |
| 样本数量 / 分母 | 文献侧：3,176 screened records → 77 possible → 58 included；K=0.634（inclusion）/ 0.651（clustering）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 practice proposals |
| 原文类型 | SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） |
| 原生树 / 森林类型 | **维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / 待原文版面核验 管理；不得视为已完成核验 |
| 主统计池资格 | 局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 |
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
