# survey_of_surveys/：综述之综述脚手架文库

## 1. 定位

本目录服务于第二篇论文的**综述之综述脚手架**。它从已有软件工程系统综述（Systematic Literature Review, SLR）、系统映射研究（Systematic Mapping Study, SMS）、三级研究（tertiary study）和方法学指南中抽取：

1. 研究问题模式。
2. 维度模式。
3. 研究发现启发式。
4. 证据呈现方式。
5. 效度威胁与报告结构先验。

这些内容只用于支撑后续 A2a / A2b / A3 构造可演化维度模式和审计制品链。它不是目标领域证据池，不支撑目标领域研究发现，也不声称完成完整三级综述或 PRISMA 透明报告框架合规三级综述。

## 2. 当前边界

A1 当前只完成文库奠基、候选池、字段合同和一组有限 dry-run：

- 当前资产为 16 篇全文文本级 dry-run / 维度锚点：其中 6 篇来自 A1 初始 dry-run，10 篇来自 issue #95 现代 CCF-A/B 综述候选池扩展。
- 当前资产另含 3 篇 metadata-only / 需人工下载 dry-run，用来压测失败路径。
- A1 主验收仍按 3--5 篇 dry-run 口径判断；新增 10 篇只用于加固现代维度 scaffold、A1-M0--M6 元维度和失败 / 边界口径，不代表扩展为完整文库。
- 这些样本用于验证脚手架可执行性，不代表覆盖完整 SE 综述文献空间。
- 不完成 100+ 篇完整文库。
- 不冻结 A3 schema / stage contract / validator。
- 不运行真实大语言模型，不读取 `.env`，不跑四个真实例子。

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
| [search/](./search/) | 检索日志、候选池、人工下载清单；#95 十篇来源审计见 [search/issue95-selection-audit.md](./search/issue95-selection-audit.md)。 |
| [papers/](./papers/) | 单篇 dry-run 目录；每篇至少有 `bibtex.bib` 和 `review.md`，全文可得时还应有 `paper.pdf`、`paper_content.txt`。 |
| [patterns/](./patterns/) | 字段 schema、字段变更和后续 A2a/A2b 汇总入口。 |

## 5. 推荐阅读顺序

1. 先读本 [README.md](./README.md) 明确边界。
2. 再读 [GUIDE.md](./GUIDE.md) 明确证据等级、单篇 review 和 schema 回修规则。
3. 再读 [SUMMARY.md](./SUMMARY.md) 看当前 A1 状态和 dry-run 结论。
4. 需要字段合同时读 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md)。
5. 需要核验单篇证据时进入 [papers/](./papers/) 并优先读 `review.md`，再回到 `paper_content.txt` / `paper.pdf`。

## 6. 与 S0-v2 主线的关系

本目录只为 [../story/paper_story.md](../story/paper_story.md) 中的“研究者定义综述元模型 → 维度模式演化 → 字段证据 → 统计观察 → 候选发现 → 研究者裁决”提供模式先验。任何从本目录抽取出的字段、启发式或报告结构，都必须经过后续研究者采纳、schema 版本化、字段证据和回填验证，才能进入 A3 / A4 / A5。

## 6.1 #95 十篇现代维度锚点

本轮将 issue [#95](https://github.com/HansBug/research_ideas/issues/95) 中 10 篇与本论文方法高度相关的现代 survey / SLR / SMS / roadmap 纳入 A1 文库，目的不是扩成完整文库，而是让脚手架接受现代软件工程综述、LLM4SE、MDE、RE、DevSecOps 和开放制品研究的真实检验。每篇新增条目必须有独立单论文目录，并在全文可得时保留 `paper.pdf` 与 `paper_content.txt`；全文不可得时必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。

这些条目必须服务于 A1-M0--M6 元维度：A1-M0 研究意图与综述元模型，A1-M1 语料收集与纳排，A1-M2 研究对象与主题语义，A1-M3 方法 / 技术 / 干预，A1-M4 评价、证据与复现资产，A1-M5 统计分析就绪，A1-M6 research finding 形成与裁决。roadmap / vision 条目可以作为边界与启发式锚点，但不得被计为完整 SLR/SMS 模式证据。

## 7. 禁止误读

- 不得把本目录写成目标领域 evidence pool。
- 不得声称本目录完成完整 tertiary review。
- 不得声称 PRISMA 透明报告框架合规。
- 不得把 metadata-only 条目的候选 pattern 写成已采纳 pattern。
- 不得把 guideline 的规范建议直接写成目标领域发现。
- 不得用本目录中的早期 EBSE 文献支撑“当前 SE SLR/SMS 全貌”这类强主张。
