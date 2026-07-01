# A1-DT v2 主线程裁决：llm-assistants-developer-productivity

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm-assistants-developer-productivity` |
| 论文标题 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study |
| codex result | [llm-assistants-developer-productivity__codex.md](../results/llm-assistants-developer-productivity__codex.md) |
| claude result | [llm-assistants-developer-productivity__claude.md](../results/llm-assistants-developer-productivity__claude.md) |
| deepseek result | [llm-assistants-developer-productivity__deepseek.md](../results/llm-assistants-developer-productivity__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SLR + SMS | SLR + SMS 混合（作者自称 "systematic review and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + thematic synthesis）。 | **SLR + SMS**（systematic literature review + systematic mapping study） | SLR + SMS 混合（作者自称 "systematic review and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + thematic synthesis）。 | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 主要单位是最终纳入的 peer-reviewed primary study；辅助单位是检索记录 / 全文报告 / QA 候选报告 | **primary study**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 | **peer-reviewed primary study**（单篇实证研究论文），经过数据库检索→去重→标题摘要筛选→全文筛选→snowballing→质量评估后纳入 | **primary study**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 初检 9,756；去重后 8,953；全文筛选 228；snowballing 后 QA 44；最终纳入 39 primary studies | 9756 → 8953 → 228 → 44 → **39**；snowballing 加入 5；QA 排除 5。 | 最终纳入 **39** 篇（全文筛选后 39 篇 + snowballing 获得 5 篇 = 44 篇进入 QA，但只有 39 篇被统计报告；QA 不淘汰论文——原文 §3.3 明确"no study was excluded on the basis of low quality scores"——因此报告基数仍为通过全文筛选的 39 篇） | 9756 → 8953 → 228 → 44 → **39**；snowballing 加入 5；QA 排除 5。 | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：检索纳排流 + 质量评价树 + 方法分类树 + 工具/景观树 + benefit/risk 主题树 + SPACE 映射树 | **多根维度森林**：每个 RQ 对应一棵 extraction subtree；底层共享 PS-id 这一样本单位主键，使所有 subtree 可交叉关联。 | **维度森林**（多表多分类框架并存，不是单一 tree） | **多根维度森林**：每个 RQ 对应一棵 extraction subtree；底层共享 PS-id 这一样本单位主键，使所有 subtree 可交叉关联。 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 是，但限于“该文原生编码维度 / 统计观察”层面；LLM-assistant productivity 的领域结论不能直接迁移为 Paper2 final finding | **是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；benefit/risk 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 fine-grained 字段须等 A2a 精核精确数字。 | **是**。有系统检索、系统纳排、系统数据抽取、QA 表和 replication package；满足 SLR/SMS 统计池要求 | **是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；benefit/risk 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 fine-grained 字段须等 A2a 精核精确数字。 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | **primary study**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 |
| 样本数量 / 分母 | 9756 → 8953 → 228 → 44 → **39**；snowballing 加入 5；QA 排除 5。 |
| 原文类型 | SLR + SMS 混合（作者自称 "systematic review and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + thematic synthesis）。 |
| 原生树 / 森林类型 | **多根维度森林**：每个 RQ 对应一棵 extraction subtree；底层共享 PS-id 这一样本单位主键，使所有 subtree 可交叉关联。 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / 待原文版面核验 管理；不得视为已完成核验 |
| 主统计池资格 | **是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；benefit/risk 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 fine-grained 字段须等 A2a 精核精确数字。 |
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
