# A1-DT v2 主线程裁决：research-artifacts-secondary-studies

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `research-artifacts-secondary-studies` |
| 论文标题 | Research artifacts in secondary studies: A systematic mapping in software engineering |
| codex result | [research-artifacts-secondary-studies__codex.md](../results/research-artifacts-secondary-studies__codex.md) |
| claude result | [research-artifacts-secondary-studies__claude.md](../results/research-artifacts-secondary-studies__claude.md) |
| deepseek result | [research-artifacts-secondary-studies__deepseek.md](../results/research-artifacts-secondary-studies__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `deepseek` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SMS（systematic mapping study）；对象是 SE secondary studies，带 tertiary-like 元研究性质。 | systematic mapping study（SMS），明确按 Petersen 等指南执行 | systematic mapping（系统映射）；对象为软件工程 secondary studies 的 research artifact 报告与可获得性 | systematic mapping（系统映射）；对象为软件工程 secondary studies 的 research artifact 报告与可获得性 | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 软件工程领域 secondary study 论文 / 文章。 | secondary study（SLR / SMS / scoping review / case survey / critical review / meta-analysis / meta-synthesis） | 每篇 secondary study（n = 537） | 每篇 secondary study（n = 537） | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | Scopus 初检 643 篇；最终纳入 537 篇；artifact 可得 169 / 537；permanent repository 65 / 169 或 65 / 537；2023 年分母 79。 | 主分母 537；衍生分母 169（提供 artifact 的子集）、79（2023 年度子集） | 537（初始检索 643 → 经 IC1/IC2/IC3 筛选 → 最终纳入 537） | 537（初始检索 643 → 经 IC1/IC2/IC3 筛选 → 最终纳入 537） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：语料筛选维度 + artifact availability / storage / reporting / trend 统计维度。 | **扁平字段表（flat extraction schema）+ 派生统计交叉表**；不是层级 taxonomy；可视为“小型维度森林”（artifact / persistence / reporting / covariate 四簇并列） | **单树**（single tree）：三主干（上下文元数据 × 制品可获得性 × 统计建模），每主干下 2–4 个叶子字段。结构简单、紧凑、可完整复原。 | **单树**（single tree）：三主干（上下文元数据 × 制品可获得性 × 统计建模），每主干下 2–4 个叶子字段。结构简单、紧凑、可完整复原。 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计：可进入“系统样本库 + 原生编码字段”统计池；但 artifact 内容质量、artifact 类型清单和 Paper2 领域结论只能作 seed / 启发，不能直接统计迁移。 | **是，局部已可统计**：本文字段口径明确、分母明确、Table 1 给出全部交叉统计；只是 *外推到 Paper2 目标领域时* 需作 boundary anchor，不可直接迁移数值。 | **是**。本文是一次系统映射研究（systematic mapping），有系统检索、纳排标准、一致性子评估（Krippendorff's Alpha = 0.776）、两轮数据抽取和 logistic regression 建模。537 个样本单位全部可追溯到纳入标准。 | **是**。本文是一次系统映射研究（systematic mapping），有系统检索、纳排标准、一致性子评估（Krippendorff's Alpha = 0.776）、两轮数据抽取和 logistic regression 建模。537 个样本单位全部可追溯到纳入标准。 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | 每篇 secondary study（n = 537） |
| 样本数量 / 分母 | 537（初始检索 643 → 经 IC1/IC2/IC3 筛选 → 最终纳入 537） |
| 原文类型 | systematic mapping（系统映射）；对象为软件工程 secondary studies 的 research artifact 报告与可获得性 |
| 原生树 / 森林类型 | **单树**（single tree）：三主干（上下文元数据 × 制品可获得性 × 统计建模），每主干下 2–4 个叶子字段。结构简单、紧凑、可完整复原。 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / text_verified 管理 |
| 主统计池资格 | **是**。本文是一次系统映射研究（systematic mapping），有系统检索、纳排标准、一致性子评估（Krippendorff's Alpha = 0.776）、两轮数据抽取和 logistic regression 建模。537 个样本单位全部可追溯到纳入标准。 |
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
