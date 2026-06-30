# A1-DT v2 主线程裁决：da-silva-2011-six-years-slr

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `da-silva-2011-six-years-slr` |
| 论文标题 | Six years of systematic literature reviews in software engineering: An updated tertiary study |
| codex result | [da-silva-2011-six-years-slr__codex.md](../results/da-silva-2011-six-years-slr__codex.md) |
| claude result | [da-silva-2011-six-years-slr__claude.md](../results/da-silva-2011-six-years-slr__claude.md) |
| deepseek result | [da-silva-2011-six-years-slr__deepseek.md](../results/da-silva-2011-six-years-slr__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | 更新型三级研究（updated tertiary study）；作者也称其为 review of secondary studies / mapping study of SLRs。 | SLR 的子型——**updated tertiary study**（temporal update + integration of two prior tertiary studies）；同时具备 mapping study 性质（本文自称"performed a mapping study of SLRs"） | SLR（updated tertiary study — 更新型三级研究） | SLR 的子型——**updated tertiary study**（temporal update + integration of two prior tertiary studies）；同时具备 mapping study 性质（本文自称"performed a mapping study of SLRs"） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 软件工程二级研究记录：SLR / mapping study / meta-analysis。主新增样本为 2008-07-01 至 2009-12-31 的 SE 集合；另与 OS/FE 前序集合比较合并。 | **已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 | 个体 SLR（secondary study / systematic literature review），以 `[SE01]` 至 `[SE77]` 唯一标识，最终入选 67 篇 | **已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 原始检索 1455 篇；去重后 154 篇候选；77 篇进入质量评价和数据抽取；67 篇进入后续分析；前序 OS/FE 为 53 篇；合并 OS/FE+SE 为 120 篇。 | SE=67；OS=20；FE=33；OS/FE=53；OS/FE+SE=120；QA assessment N=67（SE 自身）/ 120（整合） | SE 期：67 篇新 SLR；合并 OS/FE：120 篇（53+67） | SE=67；OS=20；FE=33；OS/FE=53；OS/FE+SE=120；QA assessment N=67（SE 自身）/ 120（整合） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：二级研究画像字段树 + DARE 质量评分树 + 外部课程/SWEBOK 映射树 + 前序更新/趋势统计树。 | **维度森林**：(1) 抽取表 schema 树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (predecessor relation: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→finding 路径 | **维度森林**（multi-table schema）：一个主编码表（Table 2）含 9 个数据抽取字段 + 3 个质量评估维度 + 教育/实践映射双外部分类体系（SE 2004 Curriculum + SWEBOK）+ 时间/作者/机构/国家/质量-年度趋势等跨维度分析 | **维度森林**：(1) 抽取表 schema 树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (predecessor relation: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→finding 路径 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计。原文有系统检索、纳排、质量评价和字段抽取，适合作为 A1-DT 原生 schema / tertiary-study pattern；但 2004--2009 EBSE 领域结论不可迁移为 Paper2 领域结论。 | **是**——具备完整系统检索（自动+人工+回溯）、显式纳排、quality assessment、可分母统计字段；当前 `review.md` 把它标 `schema_seed` 是低估 | 是；具备系统检索/纳排/编码方案、清晰分母、可归档编码字段与统计表，可作为 Paper2 维度森林的核心 schema seed | **是**——具备完整系统检索（自动+人工+回溯）、显式纳排、quality assessment、可分母统计字段；当前 `review.md` 把它标 `schema_seed` 是低估 | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | **已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 |
| 样本数量 / 分母 | SE=67；OS=20；FE=33；OS/FE=53；OS/FE+SE=120；QA assessment N=67（SE 自身）/ 120（整合） |
| 原文类型 | SLR 的子型——**updated tertiary study**（temporal update + integration of two prior tertiary studies）；同时具备 mapping study 性质（本文自称"performed a mapping study of SLRs"） |
| 原生树 / 森林类型 | **维度森林**：(1) 抽取表 schema 树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (predecessor relation: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→finding 路径 |
| 降级状态 | 后续主统计池候选；A2a 前仍按 schema_seed / text_verified 管理 |
| 主统计池资格 | **是**——具备完整系统检索（自动+人工+回溯）、显式纳排、quality assessment、可分母统计字段；当前 `review.md` 把它标 `schema_seed` 是低估 |
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
