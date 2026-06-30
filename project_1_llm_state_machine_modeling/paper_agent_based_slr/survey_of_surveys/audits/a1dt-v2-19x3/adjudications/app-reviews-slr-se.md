# A1-DT v2 主线程裁决：app-reviews-slr-se

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `app-reviews-slr-se` |
| 论文标题 | Analysing app reviews for software engineering: a systematic literature review |
| codex result | [app-reviews-slr-se__codex.md](../results/app-reviews-slr-se__codex.md) |
| claude result | [app-reviews-slr-se__claude.md](../results/app-reviews-slr-se__claude.md) |
| deepseek result | [app-reviews-slr-se__deepseek.md](../results/app-reviews-slr-se__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | SLR | SLR（明确遵循 Kitchenham 2004，PRISMA 流程） | SLR（Systematic Literature Review） | SLR（明确遵循 Kitchenham 2004，PRISMA 流程） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 182 篇 primary studies，发表时间覆盖 2012--2020；检索时间窗为 2010-01 至 2020-12。 | primary study（共 182 篇 peer-reviewed 论文，2012–2020 发表） | primary studies（单篇研究论文），最终纳入 182 篇（2012--2020） | primary study（共 182 篇 peer-reviewed 论文，2012–2020 发表） | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 主样本分母 182；经验评价分母 109；effectiveness evaluation 105；user-perceived quality 23；RQ5 结果分母 87。 | 182 primary studies（初始 1656→去重 303→筛选 1353→排除 1225→128 通过+ 14 manual + 40 snowballing = 182） | 182 篇 primary studies；初始检索 1656 篇→去重 303 篇→筛选 1353 篇→排除 1225 篇→手工增补 54 篇→最终 182 篇 | 182 primary studies（初始 1656→去重 303→筛选 1353→排除 1225→128 通过+ 14 manual + 40 snowballing = 182） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：以 primary study record 为根，包含 F1--F18 数据抽取字段、三套分类 schema、评价/复现资产 schema、交叉关系表。 | RQ-驱动的多 schema 抽取森林（F1–F18 数据抽取表 + 3 套分类 schema + RQ 结果层），不是单一统一树 | **维度森林**（dimension forest）：三套独立分类 schema（analysis type / mining technique / SE activity）+ 一套数据抽取字段表（F1--F18）+ 一套评价字段体系 + 一套讨论发现体系；schema 之间存在交叉表关系 | RQ-驱动的多 schema 抽取森林（F1–F18 数据抽取表 + 3 套分类 schema + RQ 结果层），不是单一统一树 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计。原文是系统 SLR 且分母清楚，可统计其原生字段与表格观察；但 app review 领域结论不能迁移为 Paper2 领域 final finding。 | 是；该论文具有完整 SLR 流程、显式封闭枚举字段、reliability 报告、五数概括与交叉表，可作为 A1 schema 模式统计池的高等级样本 | **是**；具备完整系统检索 / 纳排 / 抽取 / 分类 / 统计 / discussion 闭环，可作为 survey_of_surveys 的 SLR 方法学统计池样本。但当前 A1-DT 阶段仅作 schema_seed，A2a 精核后方可进入定量统计 | 是；该论文具有完整 SLR 流程、显式封闭枚举字段、reliability 报告、五数概括与交叉表，可作为 A1 schema 模式统计池的高等级样本 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | primary study（共 182 篇 peer-reviewed 论文，2012–2020 发表） |
| 样本数量 / 分母 | 182 primary studies（初始 1656→去重 303→筛选 1353→排除 1225→128 通过+ 14 manual + 40 snowballing = 182） |
| 原文类型 | SLR（明确遵循 Kitchenham 2004，PRISMA 流程） |
| 原生树 / 森林类型 | RQ-驱动的多 schema 抽取森林（F1–F18 数据抽取表 + 3 套分类 schema + RQ 结果层），不是单一统一树 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / text_verified 管理 |
| 主统计池资格 | 是；该论文具有完整 SLR 流程、显式封闭枚举字段、reliability 报告、五数概括与交叉表，可作为 A1 schema 模式统计池的高等级样本 |
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
