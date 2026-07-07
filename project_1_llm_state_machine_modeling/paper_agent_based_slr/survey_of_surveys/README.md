# survey_of_surveys/：综述之综述脚手架文库

## 0. 当前事实口径：A1-DT v2

> [!IMPORTANT]
> A1-DT v2 是当前维度树事实口径。开始处理本目录前，必须先读 [GUIDE.md](./GUIDE.md) §6.3，再进入单篇 `papers/<slug>/review.md`；需要审计证据时再读同目录 `evidence_chain.md` 或批次级 [audits/](./audits/)。

A1-DT v2 的边界是“统一抽取纪律 + 每篇论文原生样本编码维度树 / 维度森林 + 跨论文投影层”：

1. 单篇 `review.md` 必须从原文 RQ、贡献声明、抽取表、编码方案、taxonomy、roadmap action、guideline item 或证据呈现结构复原原生树 / 森林；正式 A.1--A.4 证据链集中在同目录 `evidence_chain.md`。
2. [patterns/](./patterns/) 只做结果侧跨论文投影 / 归纳，不能反向作为单篇原生树模板。
3. v2 新审计与新返修产物写入 `audits/a1dt-v2-19x3/`。
4. [audits/a1dt-19x3/](./audits/a1dt-19x3/) 是 v1 历史归档，只能作为返修来源和历史证据，不是当前事实口径。

> [!WARNING] v1-deprecated: `audits/a1dt-19x3/` 是 A1-DT v1 历史审计归档。不得把其中结论直接当作 A1-DT v2 当前事实；v2 新产物必须进入 `audits/a1dt-v2-19x3/`。


## 0.A A2a 语料主候选入口

> [!IMPORTANT]
> PR-A2a 已新增 [corpus/](./corpus/) 作为后续 100+ 综述语料候选的主入口。A1 的 [search/](./search/) 保留为历史检索与 dry-run 归档；A2a 以后仍然活跃的候选账本、主候选、替补、边界池、PDF 状态和人工下载清单以 [corpus/README.md](./corpus/README.md) 为入口。

当前 A2a 语料状态：全量候选 438，系统化候选 293，主候选 120，替补 / 留出 40，边界池 145；其中 core + reserve 已取得 PDF / 文本 69 篇，仍需人工下载 91 篇。详见 [corpus/source-audit.md](./corpus/source-audit.md)、[corpus/selection.md](./corpus/selection.md) 与 [corpus/pdf-acquisition.md](./corpus/pdf-acquisition.md)。这些只是候选语料，不代表 120 篇全文深读完成，也不代表最终统计分母。

## 1. 定位

本目录服务于第二篇论文的**综述之综述脚手架**。它从已有软件工程系统综述（Systematic Literature Review, SLR）、系统映射研究（Systematic Mapping Study, SMS）、三级研究（tertiary study）和方法学指南中抽取：

1. 研究问题模式。
2. 维度模式。
3. 研究发现启发式。
4. 证据呈现方式。
5. 效度威胁与报告结构先验。

这些内容只用于支撑后续 A2a / A2b / A3 构造可演化维度模式和审计制品链。它不是目标领域证据池，不支撑目标领域研究发现，也不声称完成完整三级综述或 PRISMA 透明报告框架合规三级综述。

## 2. 当前边界

A1 scaffold 与 A1-DT v2 需要分开理解：A1 scaffold 仍只是文库奠基、候选池、字段合同和有限 dry-run；PR #135 / A1-DT v2 已在此基础上完成 19 篇 × 3 路 CLI 审计和单篇 `review.md` 返修，用来冻结“原生样本编码维度树 / 维度森林”的当前事实口径。

- 当前资产为 19 篇全文文本级 dry-run / 维度锚点：其中 9 篇来自 A1 初始 dry-run，10 篇来自 issue #95 现代 CCF-A/B 综述候选池扩展。
- A1 历史 active metadata-only / 需人工下载条目为 0；A2a 当前 core / reserve 仍有 91 篇需要人工下载，活跃清单转到 [corpus/manual-download-needed.bib](./corpus/manual-download-needed.bib)。
- A1 scaffold 主验收仍按 3--5 篇 dry-run 口径判断；新增 10 篇只用于加固现代维度 scaffold、A1-M0--M6 元维度和失败 / 边界口径，不代表扩展为完整文库。
- A1-DT v2 已完成 57/57 三路 CLI 审计、19/19 主线程裁决和 19/19 单篇返修；运行日志保留命令、时间、returncode、stdout/stderr 与环境摘要，关于 `.env` 只记录 `env_sourced=.env exists`，不记录任何 secret。
- 这些样本用于验证脚手架可执行性，不代表覆盖完整 SE 综述文献空间。
- 不完成 100+ 篇完整文库。
- 不冻结 A3 schema / stage contract / validator。
- 不跑四个真实例子；A1-DT v2 只审计 survey-of-surveys 维度树，不执行 Paper2 目标方法的真实案例实验。

## 3. 纳入与排除范围

优先纳入：

1. 软件工程领域 SLR / SMS / tertiary study / survey。
2. 讨论 SLR/SMS 方法、质量评价、报告结构、纳排、搜索和数据抽取的 guideline。
3. 能提供 RQ、维度字段、finding、证据表、validity threat 或报告结构 pattern 的综述论文。
4. 对后续 Paper2 审计优先证据工程主线有方法学启发的跨域 systematic review automation guideline。

排除或降级：

1. 只做普通 topic survey、没有系统检索 / 纳排 / 抽取 / 质量评价信息的论文。
2. 目标领域一次研究论文；除非它本身是 SLR/SMS/survey。
3. 只有搜索摘要、宣传网页或不可核验元数据的条目。
4. 只与自动综述生成相关但没有 SLR/SMS 方法学内容的近邻；这类条目应优先放在 [../baselines/](../baselines/)。

## 4. 文件说明

| 文件 / 目录 | 作用 |
|---|---|
| [GUIDE.md](./GUIDE.md) | 检索、筛选、单篇目录、证据等级、schema 回修和 dry-run 维护规则。 |
| [SUMMARY.md](./SUMMARY.md) | 当前总账、候选池、dry-run 覆盖矩阵、脚手架模式、schema 缺口和更新日志。 |
| [search/](./search/) | A1 历史检索日志、候选池和人工下载清单；#95 十篇来源审计见 [search/issue95-selection-audit.md](./search/issue95-selection-audit.md)。A2a 后续活跃语料事实真源转到 [corpus/](./corpus/)。 |
| [corpus/](./corpus/) | A2a 综述语料主候选入口；维护全量候选账本、系统化候选池、主候选 120、替补 40、边界池、PDF 状态和人工下载清单。 |
| [papers/](./papers/) | 单篇 dry-run 目录；每篇至少有 `bibtex.bib`、`metadata.json`、`review.md` 与 `evidence_chain.md`，全文可得时还应有 `paper.pdf`、`paper_content.txt`。`review.md` 是当前正文入口，`evidence_chain.md` 是正式 A.1--A.4 证据链。 |
| [patterns/](./patterns/) | 结果侧跨论文投影 / 归纳入口；只能汇总单篇原生树之后的可迁移字段，不能作为单篇树模板。 |
| [audits/](./audits/) | 专项审计批次入口；v2 新产物写入 `audits/a1dt-v2-19x3/`，v1 [audits/a1dt-19x3/](./audits/a1dt-19x3/) 仅历史归档。 |

## 5. 推荐阅读顺序

1. 先读本 [README.md](./README.md) 明确边界。
2. 再读 [GUIDE.md](./GUIDE.md)，尤其 §6.3，明确 A1-DT v2 的证据等级、单篇原生树 / 维度森林、样本单位降级和 schema 回修规则。
3. 再读 [SUMMARY.md](./SUMMARY.md) 看当前 A1 状态和 dry-run 结论。
4. 需要字段合同时读 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md)。
5. 需要理解单篇当前结论时进入 [papers/](./papers/) 并优先读 `review.md`；需要核验证据链时读同目录 `evidence_chain.md`，再回到 `paper_content.txt` / `paper.pdf`。

## 6. 与 S0-v2 主线的关系

本目录只为 [../story/paper_story.md](../story/paper_story.md) 中的“研究者定义综述元模型 → 维度模式演化 → 字段证据 → 统计观察 → 候选发现 → 研究者裁决”提供模式先验。任何从本目录抽取出的字段、启发式或报告结构，都必须经过后续研究者采纳、schema 版本化、字段证据和回填验证，才能进入 A3 / A4 / A5。

## 6.1 #95 十篇现代维度锚点

本轮将 issue [#95](https://github.com/HansBug/research_ideas/issues/95) 中 10 篇与本论文方法高度相关的现代 survey / SLR / SMS / roadmap 纳入 A1 文库，目的不是扩成完整文库，而是让脚手架接受现代软件工程综述、LLM4SE、MDE、RE、DevSecOps 和开放制品研究的真实检验。每篇 A1 新增条目必须有独立单论文目录，并在全文可得时保留 `paper.pdf` 与 `paper_content.txt`；A1 历史全文不可得条目进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)，A2a 及以后新增 core / reserve 失败条目统一进入 [corpus/manual-download-needed.bib](./corpus/manual-download-needed.bib)。

这些条目必须服务于 A1-M0--M6 元维度：A1-M0 研究意图与综述元模型，A1-M1 语料收集与纳排，A1-M2 研究对象与主题语义，A1-M3 方法 / 技术 / 干预，A1-M4 评价、证据与复现资产，A1-M5 统计分析就绪，A1-M6 research finding 形成与裁决。roadmap / vision 条目可以作为边界与启发式锚点，但不得被计为完整 SLR/SMS 模式证据。当前 19 篇均已具备 `paper.pdf` 与 `paper_content.txt`；A1 的 [search/manual-download-needed.bib](./search/manual-download-needed.bib) 保留为 active=0 的历史归档，A2a 及以后新增条目若全文不可得，必须进入 [corpus/manual-download-needed.bib](./corpus/manual-download-needed.bib) 并在补齐后通过 [corpus/tables/pdf-status.csv](./corpus/tables/pdf-status.csv) 更新状态。


## 6.2 A1-DT v2 19×3 三路全文审计

A1-DT v2 是当前事实口径。v2 要求把 19 篇 `review.md` 统一到“单篇原生样本编码维度树 / 维度森林 + 跨论文投影层”的结构：先从原文复原每篇自己的 RQ / 样本单位 / 编码字段 / 关系边，再把可迁移部分投影到 [patterns/](./patterns/) 和 [SUMMARY.md](./SUMMARY.md)。

v2 批次级过程产物必须写入 [audits/a1dt-v2-19x3/](./audits/a1dt-v2-19x3/)；该目录已经落地。当前读者入口以单篇 `review.md` 为准，正式证据链以单篇 `evidence_chain.md` 和 v2 prompt / result / log / adjudication 为准。任何后续工作都不得再把 v1 归档当作当前完成证据。

> [!WARNING] v1-deprecated: PR-A1-DT v1 曾对 19 篇 `review.md` 形成 57 份 codex / claude / deepseek 全文审计，入口为 [audits/a1dt-19x3/README.md](./audits/a1dt-19x3/README.md)，逐篇审计汇总为 [audits/a1dt-19x3/SUMMARY.md](./audits/a1dt-19x3/SUMMARY.md)。该批次现在只作为历史归档和返修来源，不是 A1-DT v2 当前事实口径。

注意：A1-DT v2 仍是结构化返修，不等于 A2a 精确页码、表号、图号和 supplementary 核验完成。所有 `schema_seed`、`not_verified`、`needs_manual_check` 口径必须保留，不能被 SUMMARY 或论文写作误读成已完成统计证据。

## 7. 禁止误读

- 不得把本目录写成目标领域 evidence pool。
- 不得声称本目录完成完整 tertiary review。
- 不得声称 PRISMA 透明报告框架合规。
- 不得把 metadata-only 条目的候选 pattern 写成已采纳 pattern。
- 不得把 guideline 的规范建议直接写成目标领域发现。
- 不得用本目录中的早期 EBSE 文献支撑“当前 SE SLR/SMS 全貌”这类强主张。
