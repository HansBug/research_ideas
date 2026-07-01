# A1-DT v2 主线程裁决：kitchenham-2009-slr-tertiary

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `kitchenham-2009-slr-tertiary` |
| 论文标题 | Systematic literature reviews in software engineering – A systematic literature review |
| codex result | [kitchenham-2009-slr-tertiary__codex.md](../results/kitchenham-2009-slr-tertiary__codex.md) |
| claude result | [kitchenham-2009-slr-tertiary__claude.md](../results/kitchenham-2009-slr-tertiary__claude.md) |
| deepseek result | [kitchenham-2009-slr-tertiary__deepseek.md](../results/kitchenham-2009-slr-tertiary__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | tertiary；文中明确称本研究为 tertiary literature review，方法上是系统文献综述（SLR） | tertiary SLR（作者自称 "tertiary literature review"，§2 Method 开头） | tertiary-like SLR（三级研究：对 SE 领域已发表 SLR 进行系统文献综述） | tertiary SLR（作者自称 "tertiary literature review"，§2 Method 开头） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 纳入的二级研究，即软件工程领域 SLR / meta-analysis 研究条目；Table 2 中为 S1--S20 | secondary study（systematic literature review 或 meta-analysis 论文，每条对应一篇 SLR/MA） | 2004--2007 年间发表的 SE 领域 SLR（systematic literature review），每篇 SLR 是一个样本单位（primary study of this tertiary review） | secondary study（systematic literature review 或 meta-analysis 论文，每条对应一篇 SLR/MA） | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 检索分母：Table A1 统计 2506 篇源内文章、33 篇 relevant、19 篇 selected；去重后 18 个唯一研究，再加 2 个源外 peer-reviewed 研究，最终 20 个相关研究 | 主样本 `N=20`（S1--S20，§4.1 与 Table 2）；候选漏斗分母 `2506`（Table A1 Total），相关候选 `33`，最终选入 `19+2=20`（其中 1 篇通过研究者询问 + 1 篇通过 Simula 网站补入） | N = 20（manual search 10 journals + 4 conference proceedings，初始命中 53 篇，经纳排后得到 20 篇 relevant SLR） | 主样本 `N=20`（S1--S20，§4.1 与 Table 2）；候选漏斗分母 `2506`（Table A1 Total），相关候选 `33`，最终选入 `19+2=20`（其中 1 篇通过研究者询问 + 1 篇通过 Simula 网站补入） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：语料检索与筛选树 + 纳入研究数据抽取树 + DARE 质量评价树 + 作者/机构关系树 + 结果统计/局限树 | **单树为主 + 双子树并列**：主树为「20 篇 SLR 的抽取编码表」（§2.5 数据抽取项 + Table 2 列），并列子树为「DARE 质量评价 rubric」（§2.4 QA1--QA4 + Table 3） | **维度森林**（dual-layer schema）：Layer 1 为 data extraction form 的 9 个编码字段组成的主维度树；Layer 2 为 quality assessment rubric 的 4 个评分项组成的质量评价子树 | **单树为主 + 双子树并列**：主树为「20 篇 SLR 的抽取编码表」（§2.5 数据抽取项 + Table 2 列），并列子树为「DARE 质量评价 rubric」（§2.4 QA1--QA4 + Table 3） | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计；原文有系统检索、纳排、抽取字段、质量评分与统计表，适合作为 tertiary-study schema seed 和后续 A2a 主统计池候选；但 2004--2007 EBSE 领域结论不得迁移为 Paper2 final finding | **是（局部可统计）**：样本单位、分母、字段、取值空间、计数表都已封闭；但具体数值（QA 评分、SLR 计数）入主统计前需 A2a 对照 PDF 版面核验 | 是；原文有系统检索、纳排、数据抽取和编码方案，样本单位明确可追溯 | **是（局部可统计）**：样本单位、分母、字段、取值空间、计数表都已封闭；但具体数值（QA 评分、SLR 计数）入主统计前需 A2a 对照 PDF 版面核验 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | secondary study（systematic literature review 或 meta-analysis 论文，每条对应一篇 SLR/MA） |
| 样本数量 / 分母 | 主样本 `N=20`（S1--S20，§4.1 与 Table 2）；候选漏斗分母 `2506`（Table A1 Total），相关候选 `33`，最终选入 `19+2=20`（其中 1 篇通过研究者询问 + 1 篇通过 Simula 网站补入） |
| 原文类型 | tertiary SLR（作者自称 "tertiary literature review"，§2 Method 开头） |
| 原生树 / 森林类型 | **单树为主 + 双子树并列**：主树为「20 篇 SLR 的抽取编码表」（§2.5 数据抽取项 + Table 2 列），并列子树为「DARE 质量评价 rubric」（§2.4 QA1--QA4 + Table 3） |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / 待原文版面核验 管理；不得视为已完成核验 |
| 主统计池资格 | **是（局部可统计）**：样本单位、分母、字段、取值空间、计数表都已封闭；但具体数值（QA 评分、SLR 计数）入主统计前需 A2a 对照 PDF 版面核验 |
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
