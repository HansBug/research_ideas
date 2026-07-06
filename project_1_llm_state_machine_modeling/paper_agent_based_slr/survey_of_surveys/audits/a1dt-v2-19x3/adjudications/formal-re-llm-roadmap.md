# A1-DT v2 主线程裁决：formal-re-llm-roadmap

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `formal-re-llm-roadmap` |
| 论文标题 | Formal requirements engineering and large language models: A two-way roadmap |
| codex result | [formal-re-llm-roadmap__codex.md](../results/formal-re-llm-roadmap__codex.md) |
| claude result | [formal-re-llm-roadmap__claude.md](../results/formal-re-llm-roadmap__claude.md) |
| deepseek result | [formal-re-llm-roadmap__deepseek.md](../results/formal-re-llm-roadmap__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | roadmap / vision / proposal；不是 SLR、SMS、tertiary 或 MLR。 | **vision / roadmap**（作者原文 Page 2 明确：“It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence”） | roadmap / vision paper | **vision / roadmap**（作者原文 Page 2 明确：“It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence”） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 无系统样本库。可抽取的原生单位是两条 roadmap 下的 action point、layer、artefact、mechanism、concern、practical limitation。 | **无系统样本单位**；最接近的可结构化单位是“**action point**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations | roadmap action / guideline item（非系统文献样本） | **无系统样本单位**；最接近的可结构化单位是“**action point**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 系统样本数量：不适用。路线图 action point 可作局部结构单位：Roadmap A 为 5 个，Roadmap B 为 7 个；这不是系统综述分母。 | 不存在系统样本分母；roadmap action 数固定为 5 + 7 = 12；如把 Section 7 视为辅助森林则 +7 = 19。**不可作为统计分母使用** | 无系统样本库；原文不声称基于 SLR/SMS 纳排 | 不存在系统样本分母；roadmap action 数固定为 5 + 7 = 12；如把 Section 7 视为辅助森林则 +7 = 19。**不可作为统计分母使用** | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 降级树 / 维度森林：双向 roadmap-action 森林 + concern / limitation 边界树。 | **降级森林**：双根 roadmap 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 | 无系统样本库 / 降级树 | **降级森林**：双根 roadmap 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 否；作者明示 vision paper，不提供 sound empirical evidence，且无系统检索、纳排、质量评价、数据抽取或统计综合。 | **否**；roadmap / vision；缺系统检索、纳排、质量评价、数据综合 | 否 — roadmap 无系统纳排、无 extraction form、无可审计编码 schema | **否**；roadmap / vision；缺系统检索、纳排、质量评价、数据综合 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | **无系统样本单位**；最接近的可结构化单位是“**action point**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations |
| 样本数量 / 分母 | 不存在系统样本分母；roadmap action 数固定为 5 + 7 = 12；如把 Section 7 视为辅助森林则 +7 = 19。**不可作为统计分母使用** |
| 原文类型 | **vision / roadmap**（作者原文 Page 2 明确：“It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence”） |
| 原生树 / 森林类型 | **降级森林**：双根 roadmap 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 |
| 降级状态 | 不进入主统计池；仅作 boundary / schema seed |
| 主统计池资格 | **否**；roadmap / vision；缺系统检索、纳排、质量评价、数据综合 |
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
