# A1-DT v2 主线程裁决：mde-ml-components-slr

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `mde-ml-components-slr` |
| 论文标题 | Model driven engineering for machine learning components: A systematic literature review |
| codex result | [mde-ml-components-slr__codex.md](../results/mde-ml-components-slr__codex.md) |
| claude result | [mde-ml-components-slr__claude.md](../results/mde-ml-components-slr__claude.md) |
| deepseek result | [mde-ml-components-slr__deepseek.md](../results/mde-ml-components-slr__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SLR | **SLR**（Kitchenham guidelines 显式声明，protocol → planning/conducting/reporting） | SLR（Systematic Literature Review），遵循 Kitchenham guidelines | **SLR**（Kitchenham guidelines 显式声明，protocol → planning/conducting/reporting） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 46 篇 primary studies，编号 P1--P46。 | **primary study**，编号 P1–P46，46 篇 | 46 篇 primary study（P1–P46），来自系统数据库检索（32 篇）+ 前向/后向 snowballing（14 篇） | **primary study**，编号 P1–P46，46 篇 | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 自动检索 3934 条，去重后 3570 条，三轮筛选到 32 篇，snowballing 增补 14 篇，最终 46 篇；结论节另写 3496，疑似与方法节不一致，需保留为风险。 | 自动检索 3934 → 去重 3570 → title/abstract 72 → brief full-paper 55 → detailed reading 32 → snowballing +14（前向 8 + 后向 6）→ **46**（其中 conclusion §7 误写为 “3,496 papers”，与方法 §3.3.2 中 3934 不一致） | 初始 3934 → 去重 3570 → 三轮筛选得 32 → snowballing 增补 14 → **最终 46** | 自动检索 3934 → 去重 3570 → title/abstract 72 → brief full-paper 55 → detailed reading 32 → snowballing +14（前向 8 + 后向 6）→ **46**（其中 conclusion §7 误写为 “3,496 papers”，与方法 §3.3.2 中 3934 不一致） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：以 Fig. 5 “MDE Solution for ML” 特征树为核心，外加 Google Form 5 个 section / 40 个问题驱动的 RQ1--RQ4 字段森林。 | **单根维度树**（Fig. 5 "Features of selected primary studies"，根节点为 MDE Solution for ML），辅以 Table 1 纳排 schema 与 QA1–QA5 质量 rubric 两个并列 schema；不构成维度森林 | **维度森林**（多子树）：一棵以 Google Form 40 题 5 section 为抽取根的特征树（Fig. 5）+ 四棵 RQ 回答子树，彼此之间存在显式交叉引用与统计关系 | **单根维度树**（Fig. 5 "Features of selected primary studies"，根节点为 MDE Solution for ML），辅以 Table 1 纳排 schema 与 QA1–QA5 质量 rubric 两个并列 schema；不构成维度森林 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计。原文自身可对 46 篇 primary studies 做字段统计；迁移到 Paper2 时只能作为 schema/method pattern，MDE4ML 领域结论不得进入主统计池。 | 局部可统计；本文 RQ1–RQ4 章节给出的 frequencies（如 43/46、35/46、38/46、89%、75%、88%）可作为 A2a 待核候选字段分布；A1-DT 阶段所有数字仍需回到 PDF 精核，精核前不得进入最终定量统计（特别是 Fig. 4 publication type 分布、Fig. 10 metric 分布与 Table 9 QA 矩阵） | **是**：具备系统检索、纳排 protocol、data extraction form、显式编码方案、pilot test、名义 quality assessment、及每 RQ 的显式统计报告。46 篇 primary study 可进入 A2a 精核后的主统计池 | 局部可统计；本文 RQ1–RQ4 章节给出的 frequencies（如 43/46、35/46、38/46、89%、75%、88%）可作为 A2a 待核候选字段分布；A1-DT 阶段所有数字仍需回到 PDF 精核，精核前不得进入最终定量统计（特别是 Fig. 4 publication type 分布、Fig. 10 metric 分布与 Table 9 QA 矩阵） | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | **primary study**，编号 P1–P46，46 篇 |
| 样本数量 / 分母 | 自动检索 3934 → 去重 3570 → title/abstract 72 → brief full-paper 55 → detailed reading 32 → snowballing +14（前向 8 + 后向 6）→ **46**（其中 conclusion §7 误写为 “3,496 papers”，与方法 §3.3.2 中 3934 不一致） |
| 原文类型 | **SLR**（Kitchenham guidelines 显式声明，protocol → planning/conducting/reporting） |
| 原生树 / 森林类型 | **单根维度树**（Fig. 5 "Features of selected primary studies"，根节点为 MDE Solution for ML），辅以 Table 1 纳排 schema 与 QA1–QA5 质量 rubric 两个并列 schema；不构成维度森林 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / 待原文版面核验 管理；不得视为已完成核验 |
| 主统计池资格 | 局部可统计；本文 RQ1–RQ4 章节给出的 frequencies（如 43/46、35/46、38/46、89%、75%、88%）可作为 A2a 待核候选字段分布；A1-DT 阶段所有数字仍需回到 PDF 精核，精核前不得进入最终定量统计（特别是 Fig. 4 publication type 分布、Fig. 10 metric 分布与 Table 9 QA 矩阵） |
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
