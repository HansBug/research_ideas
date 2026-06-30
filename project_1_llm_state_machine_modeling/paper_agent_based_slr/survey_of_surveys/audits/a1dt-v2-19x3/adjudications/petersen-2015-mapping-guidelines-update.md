# A1-DT v2 主线程裁决：petersen-2015-mapping-guidelines-update

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2015-mapping-guidelines-update` |
| 论文标题 | Guidelines for conducting systematic mapping studies in software engineering: An update |
| codex result | [petersen-2015-mapping-guidelines-update__codex.md](../results/petersen-2015-mapping-guidelines-update__codex.md) |
| claude result | [petersen-2015-mapping-guidelines-update__claude.md](../results/petersen-2015-mapping-guidelines-update__claude.md) |
| deepseek result | [petersen-2015-mapping-guidelines-update__deepseek.md](../results/petersen-2015-mapping-guidelines-update__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SMS / tertiary-like methodological mapping / guideline update | **SLR / SMS / guideline 混合**：systematic mapping study of systematic mapping studies (tertiary 性质) + guideline update。 | systematic mapping study of systematic mapping studies（SMS 之 SMS，即 tertiary mapping / meta-mapping）；同时产出 guideline update | **SLR / SMS / guideline 混合**：systematic mapping study of systematic mapping studies (tertiary 性质) + guideline update。 | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 软件工程 systematic mapping study；最终结果统计分母为 52 篇 included mapping studies | **primary study = SE 领域已发表的 systematic mapping study**（每个 study 被作者按 Table 3 抽取表编码）。 | 单个已发表的 systematic mapping study（primary study） | SE systematic mapping studies；最终结果分母 52（57 为 QA 前/中间候选，不能采纳 deepseek 的 57） | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 检索 7752；去 2004 年前后 5082；title/abstract 后 60；全文后 43；snowball 后 54；quality 后 44；review excluded 后最终 52。另有 57 作为 quality assessment 前候选集合 | **52 mapping studies**（Appendix A 列出 ~52 个 included id；§3.6.2 与 §4.4.3 多处复现 "52" 分母）。Fig. 1 流程链：7752 → 5082 (去 2004 前) → 60 (title/abstract) → 43 (full-text) → 54 (+11 snowball) → 44 (quality) → 52 (review of excluded 回补 8) 。 | 57 篇 primary studies（初始检索 5569 → 去重 3708 → title/abstract 筛选 152 → full-text 后 46 → backward snowballing +11 = 57 → quality assessment 后仍 57 全计入） | **52 mapping studies**（Appendix A 列出 ~52 个 included id；§3.6.2 与 §4.4.3 多处复现 "52" 分母）。Fig. 1 流程链：7752 → 5082 (去 2004 前) → 60 (title/abstract) → 43 (full-text) → 54 (+11 snowball) → 44 (quality) → 52 (review of excluded 回补 8) 。 | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：样本抽取字段森林 + 过程策略分类森林 + quality/rubric 森林 + guideline action 综合树 | **维度森林**（至少 4 棵互相独立的主干树：①extraction form 树；②classification facet 树；③guideline action / rubric 树；④validity taxonomy 树）。 | **维度森林**（dimension forest）：一棵以"单篇 SMS 研究所执行的 mapping process"为核心的多层级编码森林，覆盖文献元数据树、检索策略子树、分类方案子树、可视化子树、效度子树 | **维度森林**（至少 4 棵互相独立的主干树：①extraction form 树；②classification facet 树；③guideline action / rubric 树；④validity taxonomy 树）。 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计：可进入 A1 方法学 / survey-of-surveys 统计池；不可作为目标领域效果或 Paper2 final finding 统计证据 | **是（限方法学统计池）**。所有 Appendix B 表 (B.15–B.27) 是逐研究 study→category 的关系边映射，全部分母=52，可直接进入方法学频次统计；不可用于"目标 SE 主题效果/因果"统计池。 | 是；属方法学统计池，非领域效果/因果统计池。其编码字段直接作为 A2a 对 SLR/SMS 类文献的 extraction form 种子 | 是，限 SMS 方法学统计池；不进入领域效果/因果统计池 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | SE systematic mapping studies；最终结果分母 52（57 为 QA 前/中间候选，不能采纳 deepseek 的 57） |
| 样本数量 / 分母 | **52 mapping studies**（Appendix A 列出 ~52 个 included id；§3.6.2 与 §4.4.3 多处复现 "52" 分母）。Fig. 1 流程链：7752 → 5082 (去 2004 前) → 60 (title/abstract) → 43 (full-text) → 54 (+11 snowball) → 44 (quality) → 52 (review of excluded 回补 8) 。 |
| 原文类型 | **SLR / SMS / guideline 混合**：systematic mapping study of systematic mapping studies (tertiary 性质) + guideline update。 |
| 原生树 / 森林类型 | **维度森林**（至少 4 棵互相独立的主干树：①extraction form 树；②classification facet 树；③guideline action / rubric 树；④validity taxonomy 树）。 |
| 降级状态 | 不进入主统计池；仅作 boundary / schema seed |
| 主统计池资格 | 是，限 SMS 方法学统计池；不进入领域效果/因果统计池 |
| 不确定项 | 三路中 deepseek 将最终分母误写为 57；主线程按 paper_content.txt:449-450、627-628、Appendix A 计数采纳 52。 |

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
