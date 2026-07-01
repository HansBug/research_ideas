# A1-DT v2 主线程裁决：devsecops-primary-dimensions

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `devsecops-primary-dimensions` |
| 论文标题 | Identifying the primary dimensions of DevSecOps: A multi-vocal literature review |
| codex result | [devsecops-primary-dimensions__codex.md](../results/devsecops-primary-dimensions__codex.md) |
| claude result | [devsecops-primary-dimensions__claude.md](../results/devsecops-primary-dimensions__claude.md) |
| deepseek result | [devsecops-primary-dimensions__deepseek.md](../results/devsecops-primary-dimensions__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | 多声部文献综述（Multi-vocal Literature Review, MLR） | Multivocal Literature Review (MLR) + Reflexive Thematic Analysis (TA)；属系统二级研究 | MLR（multivocal literature review），属于 tertiary / secondary study。不属 primary study。 | Multivocal Literature Review (MLR) + Reflexive Thematic Analysis (TA)；属系统二级研究 | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 主样本为纳入的 white literature / grey literature 文献条目；实际编码观察单位为文献中的 text segment，经 code、theme、category、CPTM item 与 lifecycle stage 聚合 | **两层**：(a) primary studies（104 WL + 43 GL，2012--2021；另 20 confirmatory search 单独存放、不入 TA/CPTM）；(b) 每篇 primary study 内部被抽取的细粒度 item：DevSecOps definitions (28+15)、challenges (73+53)、practices (219+137)、metrics (7+13)、tools (18+45)——这些 item 才是 thematic analysis 的真正编码单位 | 纳入的 white literature 104 篇 + grey literature 43 篇 = **147 个 primary source**。每篇经标题/摘要筛选、全文审查、质量评价（QA 评分 ≥ 11/18），最终进入 Thematic Analysis。另有 confirmatory search 13 篇 WL + 7 篇 GL 未被纳入 TA 和 CPTM 模型。 | **两层**：(a) primary studies（104 WL + 43 GL，2012--2021；另 20 confirmatory search 单独存放、不入 TA/CPTM）；(b) 每篇 primary study 内部被抽取的细粒度 item：DevSecOps definitions (28+15)、challenges (73+53)、practices (219+137)、metrics (7+13)、tools (18+45)——这些 item 才是 thematic analysis 的真正编码单位 | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 主 MLR：104 篇 WL + 43 篇 GL = 147；其中 RQ1 为 102 WL + 43 GL，RQ2 另有 2 WL + 0 GL；confirmatory search 13 WL + 7 GL 不进入 TA/CPTM | primary studies 分母 = 102 WL + 43 GL (RQ1) + 2 WL (RQ2) ≈ 147；text segment 分母随 aspect 不同：definitions 43、challenges 126、practices 356、metrics 20、tools 63；最终模型项：28 challenges (C01--C28)、60 practices (P01--P60)、20 metrics (M01--M20)、18 tool groups (T01--T18) | 147（主 MLR 池）；confirmatory search 的 20 个额外条目未被编码，不计入主统计。 | primary studies 分母 = 102 WL + 43 GL (RQ1) + 2 WL (RQ2) ≈ 147；text segment 分母随 aspect 不同：definitions 43、challenges 126、practices 356、metrics 20、tools 63；最终模型项：28 challenges (C01--C28)、60 practices (P01--P60)、20 metrics (M01--M20)、18 tool groups (T01--T18) | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林 + 关系型模型；核心是 aspect -> text segment/code -> theme/category -> C/P/T/M item -> lifecycle stage/edge | **维度森林 + 显式关系边**（不是单棵树）：5 个 aspect 各为一棵子树，CPTM 关系图把 4 棵子树（Challenge/Practice/Tool/Metric）通过 Table 21 的多对多映射 + Gartner 10 阶段生命周期投影连接成一张图 | **维度森林**。该论文本身是 secondary/tertiary study（对 primary study 的综述），因此其原生维度树是两层：第一层是对 primary source 抽取的 Aspects → Themes（5 aspects，总计 132 themes）；第二层是跨 aspects 的 Categories → Lifecycle stages → CPTM 模型。这是一个多级、多面向的复杂编码框架，而非简单单树。 | **维度森林 + 显式关系边**（不是单棵树）：5 个 aspect 各为一棵子树，CPTM 关系图把 4 棵子树（Challenge/Practice/Tool/Metric）通过 Table 21 的多对多映射 + Gartner 10 阶段生命周期投影连接成一张图 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计；可进入 A1-DT schema / 维度树统计池，不可把 DevSecOps 领域结论迁移为 Paper2 final finding | **是（局部完全可统计）**：5 aspect 频次、WL/GL 分布、theme 频次、prior-review overlap、C-P-T-M 边数、lifecycle-stage 分布、metric→DevOps-metric 映射均有明确分母与可复核表格（Tables 1--21、Fig 3--9） | **局部可统计**。本文的 147 个 primary source 按 aspect 被编码为 themes，theme 频率（frequency count）可统计。但需注意：(1) 一个 primary source 可能跨多个 aspect 贡献多个 themes，分母非独立；(2) Metrics/Measurement 仅 7 WL + 13 GL = 20 themes，指标面薄弱；(3) Business category 主要由 GL 贡献，WL 几乎空白；(4) RQ2（Global DevSecOps）结论为"absence"，无正统计。对该论文本身的维度树统计与对 primary source 的跨论文统计是不同层级操作，必须区分。 | **是（局部完全可统计）**：5 aspect 频次、WL/GL 分布、theme 频次、prior-review overlap、C-P-T-M 边数、lifecycle-stage 分布、metric→DevOps-metric 映射均有明确分母与可复核表格（Tables 1--21、Fig 3--9） | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | **两层**：(a) primary studies（104 WL + 43 GL，2012--2021；另 20 confirmatory search 单独存放、不入 TA/CPTM）；(b) 每篇 primary study 内部被抽取的细粒度 item：DevSecOps definitions (28+15)、challenges (73+53)、practices (219+137)、metrics (7+13)、tools (18+45)——这些 item 才是 thematic analysis 的真正编码单位 |
| 样本数量 / 分母 | primary studies 分母 = 102 WL + 43 GL (RQ1) + 2 WL (RQ2) ≈ 147；text segment 分母随 aspect 不同：definitions 43、challenges 126、practices 356、metrics 20、tools 63；最终模型项：28 challenges (C01--C28)、60 practices (P01--P60)、20 metrics (M01--M20)、18 tool groups (T01--T18) |
| 原文类型 | Multivocal Literature Review (MLR) + Reflexive Thematic Analysis (TA)；属系统二级研究 |
| 原生树 / 森林类型 | **维度森林 + 显式关系边**（不是单棵树）：5 个 aspect 各为一棵子树，CPTM 关系图把 4 棵子树（Challenge/Practice/Tool/Metric）通过 Table 21 的多对多映射 + Gartner 10 阶段生命周期投影连接成一张图 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / 待原文版面核验 管理；不得视为已完成核验 |
| 主统计池资格 | **是（局部完全可统计）**：5 aspect 频次、WL/GL 分布、theme 频次、prior-review overlap、C-P-T-M 边数、lifecycle-stage 分布、metric→DevOps-metric 映射均有明确分母与可复核表格（Tables 1--21、Fig 3--9） |
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
