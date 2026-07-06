# A1-DT v2 主线程裁决：requirements-quality-theory-roadmap

## 0. 裁决卡片

| 项 | 结论 |
|---|---|
| paper slug | `requirements-quality-theory-roadmap` |
| 论文标题 | Requirements quality research: a harmonized theory, evaluation, and roadmap |
| codex result | [requirements-quality-theory-roadmap__codex.md](../results/requirements-quality-theory-roadmap__codex.md) |
| claude result | [requirements-quality-theory-roadmap__claude.md](../results/requirements-quality-theory-roadmap__claude.md) |
| deepseek result | [requirements-quality-theory-roadmap__deepseek.md](../results/requirements-quality-theory-roadmap__deepseek.md) |
| 主线程裁决 | completed / review.md 已按 A1-DT v2 口径重写 |
| 是否重写 review.md | 是 |
| 是否更新 SUMMARY | 是 |
| 是否更新 patterns | 暂不新增跨论文 pattern；仅保留回填入口 |
| 采纳主干 | 采用 `claude` 结果作为主干，并用另外两路结果校正分母、降级边界和证据强度。 |

## 1. 三路 verdict 对照

| 审计问题 | codex | claude | deepseek | 主线程采纳结论 | 采纳 / 拒绝理由 | 证据依据 |
|---|---|---|---|---|---|---|
| 原文类型 | other：research commentary / theory + survey-based evaluation + roadmap；不是标准 SLR/SMS/tertiary。 | research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） | **research commentary / VIEW POINT**（期刊明确标注）。非 SLR、非 SMS、非 tertiary、非 MLR。属于「theory + evaluation + roadmap」三合一。 | research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） | 以原文自我定位、方法章节和 metadata 共同裁决。 | `bibtex.bib`、`metadata.json`、`paper_content.txt`、三路 result |
| 被编码样本单位 | 57 篇 requirements quality primary studies/publications，来自作者先前 systematic study 的 convenience sample。 | primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） | **57 篇 primary studies**（需求质量因子文献），来自作者此前系统研究 [7] 的便利样本（convenience sample）。 | primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） | 优先采纳能明确区分主样本、辅助样本、降级对象和局部示例对象的表述。 | 三路 result §2；必要时回到 `paper_content.txt` |
| 样本数量 / 分母 | 原生 survey 分母为 57 篇；impact 子分母常为 40 篇；activities 子分母常为 40 篇。 | n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-reported 子集为 40） | 57（编码母体）/ 无系统检索纳排流程（便利样本）。辅助编码一致性检验使用其中 6 篇（≈10%）。 | n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-reported 子集为 40） | 分母必须与原文筛选流、结果表和附录列表一致；中间候选数不得冒充最终统计分母。 | 三路 result §0/§1；`paper_content.txt` 方法和结果表 |
| 原生树 / 森林类型 | 维度森林：RQT 理论概念关系树 + 基于 RQT concept 的 publication-level categorical coding scheme；roadmap 是候选 action forest，不是样本编码主树。 | **维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 | **单树（codebook 树）**，以 RQT 概念模型为框架，对每篇 primary study 做 categorical coding。不是维度森林（无多棵并列分类树）。 | **维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 | 优先保留原文自己的抽取表、taxonomy、质量表、roadmap/action、关系边，而不是六叶通用模板。 | 三路 result §3--§5 |
| 主统计池资格 | 局部可统计：可统计“57 篇需求质量文献如何报告 RQT 概念”；但对本项目 A1 主统计池应降级为 `schema_seed` / `boundary_anchor`，因为本文不是标准 SLR/SMS/tertiary 且样本为 convenience sampling。 | **局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` | **局部可统计**。57 篇编码统计可用于描述性观察（descriptive statistics），不能进入 SLR/SMS 的跨论文定量合成池。理由：(a) 样本为便利样本，非系统检索纳排；(b) 编码方案 ad hoc 迭代生成，IRR 中等（S-Score 76.8%）；(c) 论文本身是 research commentary，其统计服务于 gap identification 和 roadmap 论证，不是独立的 SLR/SMS 结果。 | **局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` | 区分“局部可统计 / 方法学统计池候选”和“目标领域 final finding”；roadmap/guideline/proposal 默认降级。 | 三路 result §6 与 metadata eligibility 字段 |

## 2. 样本单位与原生树裁决

| 项 | 裁决 |
|---|---|
| 被编码样本单位 | primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） |
| 样本数量 / 分母 | n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-reported 子集为 40） |
| 原文类型 | research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） |
| 原生树 / 森林类型 | **维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 |
| 降级状态 | 不进入主统计池；仅作 boundary / schema seed |
| 主统计池资格 | **局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` |
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
