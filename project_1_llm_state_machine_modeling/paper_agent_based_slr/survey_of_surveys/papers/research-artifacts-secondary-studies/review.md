# Research artifacts in secondary studies: A systematic mapping in software engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Research artifacts in secondary studies: A systematic mapping in software engineering |
| 作者 | Aleksi Huotala; Miikka Kuutila; Mika Mäntylä |
| 年份 | 2025 |
| 出版形态 | 期刊；`metadata.json` 记录正式出版日期为 2025-07-07，`bibtex.bib` 记录 IST volume 187 / 2025-11，开放全文为 arXiv v3 / 2026-04-16。 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology)；开放 PDF 来自 arXiv。 |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 综述类型大类 | 🟦 SMS |
| 细分类型 / 原文自称 | 系统映射；对象是 SE 二次研究 artifact |
| 本文角色 | 🔵 类SLR |
| 统计池资格 | 🟢 入池 |
| 证据成熟度 | 🟡 全文 |
| 样本单位 / 分母链 | 📚 综述 / 537 |
| 原生维度树类型 | 🧱 资产树 |
| DOI | [10.1016/j.infsof.2025.107830](https://doi.org/10.1016/j.infsof.2025.107830) |
| 本文自有开放工件 | Zenodo DOI：`10.5281/zenodo.15488074`；正文脚注与 Data availability 均指向该工件。 |
| SE 子领域 | 横向方法学：二次研究 artifacts / open science / reproducibility。 |
| 阅读状态 | 已读 `bibtex.bib`、`metadata.json`、`paper_content.txt` 全文；已用 `paper.pdf` 的 layout 文本核对 Table 1 关键数值与排版。 |
| 证据等级 | 全文文本级；关键表格已回 PDF 文本核对，但未做视觉截图级人工核验。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| A1 角色 | 为 Paper2 的“审计制品链 / 可复现证据资产”提供强相关字段锚点：artifact availability、permanent repository、DOI、dead link、by request、dedicated data availability section。 |
| 是否目标证据池 | 否；只作为 survey-of-surveys 脚手架和 Paper2 方法设计的模式先验。 |
| 一句话结论 | 这篇短映射研究把 二次研究 的开放研究工件从“口号”操作化为可统计字段，尤其适合迁移到 Paper2 的审计制品资产表；但它只统计有无与存放方式，未评估工件内容质量。 |

## 2. 论文内容详读

### 2.1 背景 / 问题

论文关注软件工程系统综述、系统映射和其他 二次研究 的 research artifacts。作者给出四个动机：可重复 / 可复现、信任、后续更新、通向自动化。对 Paper2 最关键的是第四点：作者明确指出自动化系统综述需要既有研究工件来开发与验证质量，因此工件不只是“补充材料”，而是后续方法与工具的训练、验证和审计基础。

本文没有给出复杂的研究工件类型本体；它更偏操作化判断：一篇 二次研究 是否提供外部 research artifact，是否在永久仓库存放，是否有 DOI，是否在正文中用专门章节说明数据 / 工件可用性，链接是否失效，是否仅“upon request”。

### 2.2 研究目标

目标是评估软件工程 二次研究 如何报告 research artifacts，并给出这些 artifacts 的总体可获得性图景。摘要中声称要提供 comprehensive list；但正文主体主要呈现统计表与方法，具体逐篇清单和更完整方法细节依赖其 Zenodo 工件。

### 2.3 方法概览

作者按 Petersen 等系统映射指南和 SIGSOFT Empirical Standards checklist 执行 系统映射。检索在 2024-10-02 结束，只使用 Scopus；检索范围由 13 个软件工程相关期刊与 2 个更广义计算机科学综述期刊的 ISSN 组成，并在标题中限定 review / mapping / meta-analysis / scoping review / critical review 等词。年份范围为 2013--2023，因为 Zenodo、Figshare 等关键仓库在这一时期后已可用。

### 2.4 RQ

正文以四个 RQ 组织结果：

1. 有多少 二次研究 包含 research artifact。
2. research artifacts 存放在哪里，特别是是否使用带 DOI 的永久仓库。
3. 数据 / 工件可用性在论文中如何陈述，尤其是否有 dedicated section。
4. 出版年份和出版论坛如何影响 research artifact availability。

这个 RQ 组合不是领域主题型，而是“制品资产可获得性 + 报告方式 + 时间 / venue 影响”的方法学审计型 RQ。

### 2.5 语料 / 纳排 / 抽取

- 初始检索得到 643 篇文章。
- 纳入标准：2013--2023 年发表；属于 二次研究；与软件工程相关。
- 对 ACM Computing Surveys 和 Computer Science Review 中的条目，作者人工判断是否属于软件工程，因为这两个期刊并不只发软件工程论文。
- 作者用 Krippendorff’s Alpha 评估人工判断一致性，结果为 0.776（95% 置信区间），正文称为强一致。
- 最终纳入 537 篇 二次研究。
- 数据抽取分两轮：先人工全文筛查，识别专门说明 research artifacts 可用性的章节；再用 Python 脚本做关键词搜索，打印每个关键词命中前后 100 个字符，由人工检查。
- 抽取判断包括：论文是否引用外部资源；外部资源是否位于永久仓库，例如 Figshare、Zenodo、Mendeley Data。

### 2.6 统计分析

核心统计是 Table 1：

1. 按 publication channel 统计总数、Yes、Permanent repo、No、By Request、Dead Link。
2. 按年份统计 Yes / No / By request / Dead / Permanent repo / Dedicated section。
3. 用二元 logistic regression 建模 artifact 是否可用，解释变量为年份和期刊；年份作为 缩放后的有序因子，TSE 作为参考期刊；少于 10 篇样本的期刊被排除。

主要回归结果：年份是显著预测因子；每增加约 3 年，包含 research artifact 的 odds 增加 2.31 倍。相对于 TSE，若干期刊的系数为负且部分显著。这个结果可作为“趋势统计 → 解释性 finding”的例子，但不应被迁移为 Paper2 的领域事实。

### 2.7 主要结果

- 537 篇中 169 篇提供 research artifact，占 31.5%。
- 在提供 research artifact 的 169 篇中，65 篇位于永久仓库，占 38.5%；若以全部 537 篇为分母，永久仓库比例仅 12.1%。
- 2023 年 二次研究 中 49 / 79 篇提供 artifact，占 62.0%；24 / 79 篇使用永久仓库，占 30.4%。
- 169 篇有 artifact 的论文中，50 篇有 dedicated section 声明数据或 research artifact 可用性，占 29.6%。Table 1 的 Dedicated section 总计为 72 / 537，因此 dedicated section 与真实开放 artifact 不是同一个概念，分母不能混用。
- 总体上开放实践在增长，但永久仓库和 DOI 的采用仍明显不足。
- 作者特别警示：即使在 2023 年，非永久仓库链接也可能很快失效；有些 Data Availability section 只写“no data was used”或“available upon request”，这对 二次研究 来说是令人担忧的。

### 2.8 效度威胁 / 限制

作者列出三类限制：

1. 排除了会议论文。理由是高质量 二次研究 多发表在期刊，且会议 proceedings 的 ISSN 与质量年度波动会带来噪声；作者认为这不太可能改变结论，但该判断仍限制外推。
2. 只使用 Scopus。作者认为 Scopus 已包含相关数据库的元数据；但如果研究目标是全文内容搜索，则多个数据库会是必要条件。
3. 只纳入 2013--2023。理由是要确保 Zenodo、Figshare 等永久仓库已进入可用期。

对 Paper2 来说，这些限制提示：如果要评估审计制品链，检索范围、全文可得性和平台生态时间点必须作为外推边界写清楚。

### 2.9 开放工件

本文本身提供 Zenodo 工件：正文脚注称 full details of research methods are available in research artifact，Data availability 也声明研究数据可在 Zenodo 获取。当前 review 只核验到正文和本地 PDF 中存在该 DOI；未打开 Zenodo 检查内部文件清单。因此，本文可作为“论文内 Data availability + DOI 工件”的正例，但其工件内容质量仍待复核。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 以“artifact 是否存在、存放在哪里、如何声明、年份/venue 如何影响”为核心；属于 evidence-asset audit 型 RQ。 | `paper_content.txt` Page 2--4 的 RQ1--RQ4。 | 高度可迁移到 Paper2：可把审计制品链拆成 availability、persistence、reporting、trend/context 四类问题。 | 不迁移具体比例到 Paper2 目标领域；该文对象是 SE 二次研究。 |
| dimension pattern | 字段包括 publication venue、year、artifact availability Yes/No、permanent repo、by request、dead link、dedicated section。 | `paper_content.txt` Page 2 Data extraction；Page 3 Table 1；PDF layout Table 1。 | 可作为候选 Paper2 制品资产字段树的初始锚点。 | 字段较粗，只统计有无与位置，不评估工件是否完整、可执行、脱敏、版本化。 |
| finding pattern | 以比例、年度趋势和 gap 形成 finding：artifact availability 改善，但永久仓库 / DOI 不足；Data Availability section 可能产生虚假透明度。 | `paper_content.txt` Page 3--5 Results / Conclusion。 | 可迁移为“统计观察 → 缺口 → 改进建议”的 finding 模板。 | 该文没有深入解释为什么不同期刊差异显著，也没有质量评分，不能迁移因果结论。 |
| evidence presentation pattern | 单个大表同时呈现 venue 分布、年度统计和 logistic regression；分母清晰，按 537 总体、169 artifacts 子集、79 篇 2023 子集切换。 | `paper_content.txt` Page 3 Table 1；`paper.pdf` layout 核对。 | 可迁移到 Paper2 的 audit asset dashboard：总样本、开放制品、永久仓库、断链、仅请求获取、专门声明章节。 | Table 1 很紧凑，若复用不当可能混淆分母；Paper2 需要把分母显式写进字段名或图注。 |
| validity / threat pattern | 限制集中在 venue scope、数据库 scope、年份窗口；并解释每个选择的理由。 | `paper_content.txt` Page 4 Limitations。 | 可迁移为 Paper2 的外推边界模板。 | 未讨论关键词漏检、keyword script recall、链接检查时间戳、artifact 内容质量误判等更细风险。 |
| report structure pattern | 短文结构：Introduction → Methods → Results → Limitations → Conclusion/Future Work → Data availability；结果严格按 RQ 展开。 | `paper_content.txt` Page 1--5。 | 可迁移为短方法学 evidence audit paper 的结构；Data availability 单列尤其重要。 | Paper2 还需要加入人机协同、schema 演化、内容证据 / 过程证据分离等方法贡献章节。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 综述元模型 | 把研究对象定义为“二次研究 + research artifact + 报告位置 + 存储位置 + 持久标识”。 | 对 Paper2，可把对象定义为“目标论文 + 审计制品 + 内容证据 + 过程证据 + 持久入口”。 | 不要把 artifact availability 等同于 artifact quality。 |
| A1-M1 脚手架与种子探测 | 用 open science、FAIR、replicability、trust、updates、automation 解释为什么工件是研究对象。 | 可作为 Paper2 论证审计制品链必要性的背景先验。 | 需要与 Paper2 的 LLM/agent 审计语境重新表述，避免泛泛开放科学口号。 |
| A1-M2 维度模式批准 | 提供一组可执行字段：Yes / No / By request / Dead link / Permanent repo / DOI / Dedicated section。 | 可变成 Paper2 字段合同的 evidence-asset 模块。 | 字段必须加缺失语义和证据锚点；不能只让 agent 勾选。 |
| A1-M3 论文收集与概览 | 展示用期刊 ISSN、题名关键词、年份窗口和纳排标准构造 二次研究 语料。 | 可迁移为候选池总账与检索边界记录。 | 本文排除会议，不适合直接套到 Paper2 的所有 SE 研究对象。 |
| A1-M4 字段级内容证据抽取 | 采用人工全文筛查 + 关键词脚本 + 人工检查 100 字上下文。 | 可迁移为 Paper2 对 Data availability、artifact link、repository/DOI 字段的半自动抽取流程。 | 需要记录关键词、命中上下文、人工裁决理由和链接检查时间。 |
| A1-M5 统计分析 | 对可获得性做 venue/year 交叉统计与 logistic regression。 | 可迁移为 Paper2 的审计制品覆盖率、持久化率、断链率、版本化率统计。 | 统计观察不能直接变成领域发现；要保留分母和字段版本。 |
| A1-M6 候选发现 | 从统计结果形成改进建议：强制发布工件、使用永久仓库、设置 Data availability section。 | 可迁移为候选发现启发式：覆盖率缺口、持久性缺口、声明质量缺口、自动化支撑缺口。 | Paper2 的最终发现必须回到内容证据和研究者裁决，不可只由过程证据或统计表推出。 |

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **把审计制品作为研究对象，而不是附录**：本文把 research artifact availability 放在 RQ 层，Paper2 也应把“审计制品链是否存在、是否持久、是否可检查”作为一等方法对象。
2. **永久仓库 / DOI 是最低可复现资产字段**：Paper2 的 run record、字段证据表、候选发现台账、质疑 / 裁决日志如果只保存在普通路径或临时链接中，论文主张会弱于本文建议的开放科学最低线。
3. **Data availability section 不能替代真实工件**：本文指出有些论文在数据可用性章节中写“no data was used”或“upon request”；Paper2 应避免把“有章节”误算为“有审计资产”。
4. **自动化需要工件资产支撑**：本文明确将 artifact 与 SLR automation 关联。Paper2 可据此论证：agent-assisted SLR 的评估不能只看最终报告，还要发布可复核的提示、抽取表、统计表、候选发现、人工裁决和错误记录。
5. **可复现性统计可以服务方法评价**：Paper2 可设计类似覆盖率指标：artifact availability rate、persistent repository rate、field evidence anchor completeness、dead-link rate、replay/run-record completeness。

### 6.2 风险

1. **本文统计“有无”，不统计“好坏”**：如果 Paper2 只证明有 review.md、run record 或 DOI，而不证明内容完整、字段可审计、可复核，就会重复本文指出的浅层开放问题。
2. **仅请求获取不应算开放**：Paper2 若出于伦理或隐私只能部分发布过程证据，需要明确区分 open、restricted、redacted、upon request，并说明哪些主张受影响。
3. **断链是时间敏感事实**：Paper2 的 DOI / repo / release 需要版本和检查日期；不能用一次本地路径证明长期可访问。
4. **会议和非期刊语料不可直接外推**：本文排除会议，Paper2 若覆盖会议论文、预印本或工具论文，需要重新校准 artifact availability 口径。
5. **Data availability 的语言可能误导 agent**：自动抽取时不能只看到 “Data availability” 标题就判定为可用；必须解析其内容是否为 no data / upon request / repository link / DOI。
6. **该文未给出细粒度 artifact taxonomy**：Paper2 需要自建内容质量与审计角色字段，不能指望本文提供完整分类。

## 7. 待复核

1. 打开并检查 Zenodo DOI `10.5281/zenodo.15488074` 的内部文件清单，确认是否包含逐篇编码表、关键词、脚本和链接检查记录。
2. 正式引用 Table 1 前，建议做视觉级 PDF 核对；当前已用 PDF layout 文本核对主要数值。
3. Table 1 中 Information and Software Technology 的 By Request 显示为 8，但百分比疑似与分母不一致；正式写作前应核对最终出版版表格。
4. `paper_content.txt` 中 RQ3 写 50 / 169 有 artifact 的论文包含 dedicated section，而 Table 1 Dedicated section 总计 72 / 537；使用时必须说明分母差异。
5. 摘要称提供 comprehensive list of artifacts，但正文未展开清单；该清单可能在 Zenodo 工件中，待复核后再决定是否迁移 artifact type 字段。
6. 当前未比较 arXiv v3 与 IST 最终排版版本差异；正式引用页码和表格前应以出版商版本为准。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__codex.md](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__codex.md)、[../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__claude.md](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__claude.md)、[../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__deepseek.md](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md](../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md)。

### v2 主线程采用说明

本节采用 `deepseek` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

#### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `research-artifacts-secondary-studies` |
| 审计代理 | `deepseek` |
| 是否已读 `paper_content.txt` | 是；已逐段通读 358 行全文（含 abstract、introduction、方法、results、discussion、limitations、conclusion、references） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；`bibtex.bib` 确认期刊 IST vol 187 / 2025-11，`metadata.json` 确认 DOI、出版日期 2025-07-07、arXiv v3 / 2026-04-16 及 eligibility meta |
| 是否打开或核对 `paper.pdf` | 是；已用 `pdftotext -layout` 逐页提取 PDF（共 6 页），核对了 Table 1(a)/(b)/(c) 的完整行列值与正文统计数字的一致性。未做视觉截图级人工核验（OCR 面检）。 |
| 原文类型 | 系统映射（系统映射）；对象为软件工程 二次研究 的 研究制品 报告与可获得性 |
| 被编码样本单位 | 每篇 二次研究（n = 537） |
| 样本数量 / 分母 | 537（初始检索 643 → 经 IC1/IC2/IC3 筛选 → 最终纳入 537） |
| 原生树类型 | **单表树**：上下文元数据 × 工件可获得性 / 报告字段；统计建模是 S6 派生分析输出，不属于 S3 原生样本编码叶子。 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

---

#### 1. 原文证据阅读说明

##### 1.1 实际读取文件清单

| 文件 | 读取方式 | 读取范围 |
|---|---|---|
| `paper_content.txt` | 全文通读（358 行） | Abstract → Introduction → Methods (§2.1–2.3) → Results (§3, RQ1–RQ4) → Limitations (§4) → Conclusion (§5) → References [1]–[10] |
| `bibtex.bib` | 全文读取 | 完整 BibTeX entry |
| `metadata.json` | 全文读取 | 所有字段（含 eligibility meta） |
| `review.md` | 全文读取（当前正文） | 快速结论卡片 → 论文内容详读 → 维度树复原；证据链已迁至 evidence_chain.md |
| `paper.pdf` | `pdftotext -layout -f 1 -l 6` 逐页提取 | 完整 6 页；特别核验 Table 1(a)/(b)/(c) 行列值 |

##### 1.2 PDF 版面核验状态

PDF 共 6 页。已通过 `pdftotext -layout` 核对以下内容与 `paper_content.txt` 一致性：
- Table 1(a)：15 个期刊 × 6 列（Total / 是 / 永久仓库（Permanent repo） / 否 / By Request / Dead Link）—数值完整核验
- Table 1(b)：11 年 × 7 行（是 / 否 / By req. / Dead / 永久仓库（Permanent repo） / 专门数据可获得性章节（Dedicated section） / Total）—数值完整核验
- Table 1(c)：logistic 回归 系数、标准误、z-value、p-value、odds ratio —完整核验

**仍需 PDF 视觉截图核验**：论文仅 6 页，没有复杂彩色图表；但 Table 1(a) 中 永久仓库（Permanent repo） 列的百分比计算基准（是（Yes）的子集还是 Total 的子集）和 Dead Link 的合计逻辑（22 of 537 = 4.1%，但行内百分比不同）值得视觉确认；建议 A2a 做一次 PDF 页面截图人工核验。

##### 1.3 12 个关键原文证据锚点

| # | 锚点 | 原文位置 | 短引或释义 |
|---|---|---|---|
| 1 | 研究目标与动机 | Abstract + §1 Introduction | 评估 SE 二次研究 如何 报告 研究制品，给出四大理由：replicability、trust、updates、pathway to automation |
| 2 | 检索策略 | §2.1 Search 流程 | Scopus 单数据库；16 个 ISSN token，覆盖 13 个 SE 相关期刊 + 2 个更广义 CS 综述期刊，共 15 个期刊；标题限定 review/mapping/元分析（meta-analysis）/scoping/critical；2013–2023 |
| 3 | 纳排标准 IC1–IC3 | §2.2 Study selection | IC1: 2013–2023；IC2: 二次研究；IC3: SE-related |
| 4 | 一致性子评估 | §2.2 | Krippendorff's Alpha = 0.776（95% CI），强一致 |
| 5 | 初始与最终样本数 | §2.2 | 初始检索 643 → 最终纳入 537 |
| 6 | 数据抽取两轮方案 | §2.3 数据抽取（数据抽取） | Round 1: 人工全文筛查 dedicated section；Round 2: Python keyword search + 100-char 上下文人工核验 |
| 7 | RQ1 核心统计 | §3 Results / §2.3 / Table 1(a) | 169 / 537 (31.5%) 包含 研究制品 |
| 8 | RQ2 permanent 仓库 统计 | Table 1(a)/(b) | 65 / 169 (38.5%) 使用永久仓库；占全部 537 的 12.1% |
| 9 | RQ3 报告方式 mechanism 统计 | §3 / Table 1(b) | 50 / 169 (29.6%) 有 dedicated data 可获得性 section；2023 年升至 46 / 79 = 58.2% |
| 10 | RQ4 logistic 回归 | Table 1(c) | Year 作为 缩放后的有序因子：每 3 年 odds ratio = 2.31，p < 0.001 |
| 11 | Dead link 统计 | Table 1(a)/(b) / §5 | 22 / 537 (4.1%)；2023 年仍 2 / 19 个 non-permanent link 已死 |
| 12 | "no data used" / "upon request" 异常发现 | §5 / Discussion | 部分含 "数据可获得性（Data Availability）" section 的论文声称 "no data was used" 或 "available upon request"——被作者标记为 alarming |

---

#### 2. 样本单位与字段来源判定

##### 2.1 原文纳入和逐项描述的对象是什么？

**每篇已发表的软件工程 二次研究**（系统综述/系统映射/元分析（meta-analysis）/scoping review 等），发表于 2013–2023 年间，源自 15 个期刊（13 个 SE 相关 + 2 个更广义 CS 综述期刊）。纳入后共 537 篇。

每篇 二次研究 被编码的**不是其研究内容本身**（不涉及 SE 子领域、方法学、RQ 等），而是其**研究工件的可获得性与报告方式**。

##### 2.2 作者有没有系统检索/纳排/数据抽取/编码方案？

有，且较为完整：

1. **检索**：Scopus 单一数据库；16 个 ISSN token 限定 15 个期刊；标题关键词限定 review/mapping/元分析（meta-analysis） 等 9 个术语；年份限定 2013–2023（因为 Zenodo 2013 年上线、Figshare 2011 年上线）。初始 643 篇。
2. **纳排**：IC1（年份）、IC2（是否为 二次研究）、IC3（是否 SE 相关）。title-abstract screening + 人工判定（对 ACM Computing Surveys 和 Computer Science Review 非纯 SE 期刊）。
3. **质量/一致性子评估**：Krippendorff's Alpha = 0.776，正文标注为强一致。
4. **数据抽取**：两轮——Round 1 人工全文筛查 dedicated 制品 可获得性 section；Round 2 自动化 Python keyword search + 100 字符上下文人工核验。
5. **编码方案**：检查每篇是否引用外部 研究制品、是否在永久仓库存放、是否有 DOI。

##### 2.3 原文字段来自哪里？

字段直接来自**数据抽取方案**（§2.3）和 **Table 1 统计表**：
- **研究制品可获得性（artifact_availability）**：是 / 否 / 按请求提供（是 / 否 / By Request）；§2.3 描述 + Table 1(a) 列）
- **永久仓库（permanent_repository）**：永久仓库（Permanent repo）列（Table 1(a)）——"if it is located in a permanent 仓库, such as Figshare, Zenodo or Mendeley"（§2.3）
- **专门数据可获得性章节（dedicated_section）**：专门数据可获得性章节（Dedicated section）行（Table 1(b)）——"dedicated sections indicating the 可获得性 of 研究制品"（§2.3）
- **链接健康状态（link_health）**：失效链接（Dead Link）列（Table 1(a)）
- **发表年份（year）**：Table 1(b) 列（2013–2023）
- **发表期刊（venue）**：Table 1(a) 行（15 个期刊）
- **回归优势比（回归_odds）**：Table 1(c) 逻辑回归（logistic 回归）模型输出

**完整逐篇原始编码数据**存储于 Zenodo 工件（DOI: `10.5281/zenodo.15488074`），不在正文内，正文仅呈现聚合统计表。目前 A1-DT 审计**未访问该 Zenodo 工件**——这是一个重要的证据缺口。

##### 2.4 RQ 与样本单位是什么关系？

RQ 是**结果组织方式**，不是树根也不是字段本身：

- RQ1（有多少篇有 制品）→ 使用字段 `artifact_availability`
- RQ2（存放在哪）→ 使用字段 `permanent_repository`
- RQ3（如何报告）→ 使用字段 `dedicated_section` + 定性发现（"no data used" / "upon request"）
- RQ4（年份/venue 影响）→ 使用字段 `year` × `venue` × `artifact_availability`，输出 logistic 回归 模型

RQ 是一组**围绕"制品可获得性"单一主题的问题**，它们共享同一个样本池（537 篇），使用同一套数据抽取字段的不同子集。

##### 2.5 是否有降级必要？

**不需要降级**。本文是完整的 系统映射研究，具有系统样本库、明确纳排标准、一致性子评估和统计建模。原文内部统计证据强；作为 survey_of_surveys 跨论文统计池只在 A2a 精核后候选，不进入 Paper2 目标领域统计池。

---

#### 3. 原生样本编码维度树/维度森林

> 中文化导读：本维度树复原的是二次研究中研究制品可获取性、可复现性和报告完整性的编码方式。它服务于 Paper2 对证据链和过程制品的设计，而不是直接给出领域技术结论。英文文件名、数据包名和制品类型保留为可复验锚点；中文节点用于说明制品在综述证据链中的角色、缺失语义和复用边界。可迁移的是“把制品状态纳入维度树并与可复现性 claim 绑定”的做法。

本文是**单树**结构，非维度森林。每个样本单位（二次研究）被编码为一条记录，共享同一套字段。字段分属三个主干节点。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[dim-research-制品-secondary-studies-根节点] 二次研究（二次研究；首次术语；n=537；稳定根节点标识保留）
│
├── [节点-ctx] 上下文元数据
│   ├── [leaf-year] 发表年份（稳定叶子标识保留）
│   │   取值空间：2013 | 2014 | 2015 | ... | 2023（共 11 个离散整数值）
│   │   取值空间类型：完整枚举（有序）
│   │
│   └── [leaf-venue] 发表期刊 / 发表源（稳定叶子标识保留）
│       取值空间：ACM Computing Surveys | ACM TOSEM | Automated Software Engineering |
│                Computer Science Review | Empirical Software Engineering | IEEE Software |
│                IEEE TSE | IST | JSEP | JSS | Requirements Engineering |
│                Software: Practice & Experience | SoSyM | Software Quality Journal |
│                Software Testing: Verification & Reliability（共 15 个值）
│       取值空间类型：完整枚举（类别 / 名义）
│
├── [节点-artifact] 研究制品可获得性
│   ├── [leaf-availability] 是否有研究制品
│   │   取值空间：是（Yes） | 否（No） | 按请求提供（By Request）（3 个值）
│   │   取值空间类型：层级枚举（分层类别；按请求提供（By Request）与否（No）统计上分开处理，但讨论中合并为"无直接公开工件"）
│   │
│   ├── [leaf-permanent] 是否使用永久仓库  [全样本字段：适用于全部 537 篇]
│   │   取值空间：是（是；永久仓库且带 DOI（permanent with DOI））| 否（否；非永久仓库：个人主页、机构主页、GitHub 等（non-permanent））
│   │   取值空间类型：布尔（二值，条件可见）
│   │   注：Table 1(a) 的 永久仓库（Permanent repo） 列为 是（Yes）的子集，百分比以 是（Yes）= 169 为分母
│   │
│   ├── [leaf-section] 是否有专门数据可获得性章节  [全样本字段：适用于全部 537 篇]
│   │   取值空间：是（Yes） | 否（No）
│   │   取值空间类型：布尔（二值，全样本可见）
│   │   注：Table 1(b) 专门数据可获得性章节（Dedicated section） 行的值以当年 总数（Total）为分母（非仅 是 子集）
│   │
│   └── [leaf-link] 链接是否失效
│       取值空间：是，失效（dead）| 否，存活（alive）
│       取值空间类型：布尔（二值）
│
└── [节点-model] 统计建模输出
    └── [leaf-回归] 逻辑回归系数（应移入 S6 统计分析层）
        取值空间：Table 1(c) 中每个 期刊的系数（Coef）、标准误（Std.E）、z 值（z value）、p 值（p value）、优势比（Odds ratio）
        取值空间类型：数值或区间（带标准误与 p 值的数值）
        注：这是对 [leaf-availability] 是否有研究制品 的统计建模结果，不是每篇样本的直接编码字段。
```

**缺失部分说明**：
- 逐篇原始编码数据（Zenodo DOI: `10.5281/zenodo.15488074`）未在 A1-DT 审计中访问。该工件可能包含更细粒度的字段（如 制品 具体类型分类、仓库 提供方分类：Zenodo / Figshare / Mendeley / GitHub / personal page 等），以及每篇论文的标题、DOI、作者等元数据。这些需要 **A2a 精核任务** 从 Zenodo 工件中提取补充。
- 原文未对 制品 **内容质量**做任何评估（作者在 §5 Conclusion and Future work 中明确将此列为"important future 研究 area"），因此不存在 制品 质量维度。

---

#### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `[leaf-year]` | 发表年份 | `[节点-ctx]` | §2.1（纳入标准 IC1）/ Table 1(b) 表头 | 二次研究 的出版年份 | 2013, 2014, ..., 2023（11 个值） | 完整枚举（有序） | 不可能缺失（所有纳入文献都有年份） | RQ4：作为 逻辑回归的有序因子；Table 1(b) 年度趋势统计 | Paper2 可将"发表年份"作为制品可获得性的时间趋势分析锚点 | 锚点 2, 5；Table 1(b) | 通用字段，可迁移到任何 survey-of-surveys |
| `[leaf-venue]` | 发表期刊 | `[节点-ctx]` | §2.1（ISSN 搜索限定）/ Table 1(a) 行标签 | 二次研究 发表的期刊名称 | 15 个期刊名称（完整枚举） | 完整枚举（名义类别） | 不可能缺失（检索即按 ISSN 限定） | RQ4：作为 逻辑回归的参照类别 比较 | Paper2 可按 venue 分析制品报告规范差异 | 锚点 2；Table 1(a) | SE 期刊限定；Paper2 若跨领域需扩展 venue 列表 |
| `[leaf-availability]` | 是否有研究制品 | `[节点-artifact]` | §2.3（数据抽取 描述）/ Table 1(a) 是 / 否 / 按请求提供（Yes/No/By Request） 列 | 该 二次研究 是否提供外部可访问的 研究制品 | 是（Yes）\| 否（No）\| 按请求提供（By Request） | 层级枚举 | 不存在缺失；所有 537 篇全部编码 | RQ1 主统计（169/537 = 31.5%） | Paper2 审计制品资产表的核心布尔字段 | 锚点 6, 7；Table 1(a) | 定义依赖"什么是 研究制品"——原文未形式化定义，依赖人工判断 |
| `[leaf-permanent]` | 是否使用永久仓库 | `[节点-artifact]` | §2.3（"permanent 仓库, such as Figshare, Zenodo or Mendeley"）/ Table 1(a) 永久仓库（Permanent repo） 列 | 制品的存储位置是否为永久仓库且有 DOI | 是（是；永久仓库且带 DOI（permanent with DOI））\| 否（否；非永久仓库（non-permanent）） | 布尔（条件可见：仅当“是否有研究制品”= 是（原字段标识保留于审计附录）） | 当“是否有研究制品”≠ 是时字段不适用 | RQ2：65/169 (38.5%) of Yes= 12.1% of all | Paper2 审计制品资产的"链接稳定性"代理指标 | 锚点 8；Table 1(a) 永久仓库（Permanent repo） 列 | 能迁移；需注意原文未对 GitHub（public 但非 DOI）做额外分类 |
| `[leaf-section]` | 是否有专用数据可用性章节 | `[节点-artifact]` | §2.3（"dedicated sections indicating the 可获得性"）/ Table 1(b) 专门数据可获得性章节（Dedicated section） 行 | 论文正文是否包含专门章节声明数据/制品可用性 | 是（Yes）\| 否（No） | 布尔 | 不存在缺失；"无 dedicated section" 视为 否（No） | RQ3：72/537 (13.4%) overall；2023 年 46/79 (58.2%) | Paper2 可检查纳入论文是否有明确的数据可用性声明 | 锚点 9；Table 1(b) 专门数据可获得性章节（Dedicated section） 行 | 高度可迁移；Dedicated data 可获得性 section 是跨领域 open science 实践 |
| `[leaf-link]` | 链接是否失效 | `[节点-artifact]` | §5（"2 out of 19 links to non-permanent 仓库 are already dead"）/ Table 1(a) Dead Link 列 | 制品的外部链接是否能正常访问 | 是，失效（是, dead）\| 否，存活（否, alive） | 布尔 | 当没有外部链接时字段不适用 | 作为制品可获得性的可靠性侧面证据 | Paper2 可追踪纳入工件的链接健康度 | 锚点 11；Table 1(a) Dead Link 列 | 取决于检查时间点；原文未记录检查日期 |
| `[leaf-回归]` | logistic 回归系数 | `[节点-model]` | §3 RQ4 / Table 1(c) | 二元逻辑回归（binary logistic 回归）对“是否有研究制品”（原字段标识保留于审计附录）建模的输出 | 系数（Coef）: -∞ to +∞；优势比（Odds ratio）: 0 to +∞；p 值（p value）: 0–1 | 数值或区间（含 SE 和 p-value） | 不适用 | RQ4 全部分析 | Paper2 可参考 logistic 回归 作为跨论文趋势分析方法 | 锚点 10；Table 1(c) | 统计方法可迁移；系数值不可迁移 |

---

#### 5. 关系边表

本论文的编码模式 是扁平单表结构（扁平单表），每个样本单位为一行，字段之间没有在原文中显式建模的关系边（没有外键、一对多、多对多等关系型结构）。

但是，论文中有以下**统计关系**值得记录为隐式关系边（可作为 Paper2 方法的 模式种子）：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `[edge-year-availability]` | `[leaf-year]` | 时间趋势（logistic 回归 predictor） | `[leaf-availability]` | 是 / 否 / 按请求提供（Yes/No/By Request） | N/A | Table 1(b)/(c)：year 为 有序因子，odds ratio = 2.31 per 3 years | Paper2 方法学参考：可在自己的 survey-of-surveys 中对"制品可获得性是否随时间改善"做类似建模 |
| `[edge-venue-availability]` | `[leaf-venue]` | 期刊效应（logistic 回归 predictor） | `[leaf-availability]` | 是 / 否 / 按请求提供（Yes/No/By Request） | N/A | Table 1(c)：各期刊 vs reference (IEEE TSE) 的 odds ratio | Paper2 方法学参考：发表源（venue）层面制品报告规范的差异分析 |
| `[edge-availability-permanent]` | `[leaf-availability]` | 条件子字段（conditional sub-field） | `[leaf-permanent]` | 是 / 否（是/否） | 条件不可见（仅当 可获得性 = 是（Yes）） | Table 1(a) 永久仓库（Permanent repo） 列为 是 子集 | 模式种子：条件字段在 Paper2 的审计资产表中是常见模式 |

**未发现显式关系边**：原文没有在样本单位之间建立引用、依赖或层级关系；也不存在跨表外键、nested hierarchy 或 graph 结构。这是一个经典的横截面统计设计（cross-sectional mapping），不是关系型/网络型研究。若 Paper2 的 coding 模式 需要样本间关系边，必须从其他论文引入，不能从此文导出。

---

#### 6. 统计观察、候选发现 与 最终发现边界

##### 6.1 原文中由字段/统计表支持的统计观察

以下直接来自 Table 1(a)/(b)/(c) 和 §3 Results：

| 统计观察 | 来源 | 证据强度 |
|---|---|---|
| 169 / 537（31.5%）的 SE 二次研究 包含 研究制品 | Table 1(a) | strong（直接计数） |
| 65 / 169（38.5%）的含 制品 论文使用永久仓库+DOI；即全体 537 篇的 12.1% | Table 1(a)/(b) | strong（直接计数） |
| 22 / 537（4.1%）的论文链接已失效 | Table 1(a) | moderate（链接检查时间点未记录） |
| 16 / 537（3.0%）的论文声称 制品 "upon request" | Table 1(a) | strong（直接计数） |
| 2023 年 制品 可获得性 升至 62.0%（49/79） | Table 1(b) | not_verified；待 A2a 表格复核 |
| 2023 年 permanent 仓库 使用率升至 30.4%（24/79） | Table 1(b) | not_verified；待 A2a 表格复核 |
| 2023 年 dedicated section 拥有率升至 58.2%（46/79） | Table 1(b) | not_verified；待 A2a 表格复核 |
| Publication year 是 制品 可获得性 的显著预测因子（有序因子, odds ratio = 2.31 per 3 years, p < 0.001） | Table 1(c) | strong（模型已报告） |
| 部分期刊（CS Review, SP&E, JSEP, IST）的 制品 可获得性 显著低于 参照类别（IEEE TSE） | Table 1(c) | not_verified；待 A2a 表格复核 |

##### 6.2 原文 discussion/推荐 提出的候选发现

以下来自 §4 Limitations 和 §5 Conclusion and Future work：

| 候选发现 | 类型 | 证据支持状态 |
|---|---|---|
| "both 'no data was used' and 'available upon request' are alarming for 二次研究" | 方法学批评（methodological critique） | moderate：基于观察事实（16 篇 "upon request"），但未量化 "no data was used" 的频次 |
| "journals should enforce the 报告方式 practices of 研究制品" | 政策建议（policy 推荐） | weak：作者主张，非实验证据 |
| "identifying which 研究制品 have sufficient 质量 is an important future 研究 area" | 未来研究方向（future work direction） | weak：方向性建议 |
| "links to non-permanent 仓库 can become inaccessible"（2023 年仍有 2/19 dead） | 经验观察（经验研究（empirical） observation） | moderate：基于 2023 年 19 个链接中 2 个失效的观察，但样本量小 |

##### 6.3 对 Paper2 可迁移的方法学启发

| 启发 | 迁移方式 |
|---|---|
| 将"制品 可获得性"操作化为多值分类（是 / 否 / 按请求提供（是 / 否 / By Request）），而非简单二分 | Paper2 审计资产表的 `availability_status` 字段可参考 |
| 区分 permanent 仓库（带 DOI）与 non-permanent（personal/institutional page/GitHub 无 DOI），并记录 dead link | Paper2 资产表的 `storage_type` 和 `link_health` 字段 |
| 检查纳入论文是否包含 dedicated data 可获得性 section | Paper2 可作为 review 质量的一个代理指标 |
| logistic 回归 作为跨论文趋势/venue 分析的方法 | Paper2 方法学参考 |
| 报告逐篇原始数据（Zenodo 工件）并声明 FAIR 数据原则 | Paper2 应遵循相同实践 |

##### 6.4 绝不能迁移的领域结论

本文是 **software engineering 二次研究** 的领域特定研究，以下内容绝不得迁移到 Paper2（LLM + 状态机形式化建模领域）：

- **任何具体百分比**（31.5%、62.0%、30.4%、38.5%、12.1% 等）——这些是 SE 领域的统计值
- **logistic 回归 的具体系数和 odds ratio**
- **"SE community is improving" 的时间趋势陈述**
- **对特定 SE 期刊（IST、JSS、TSE 等）的 venue 级发现**
- **对 Scopus 检索和 ISSN 检索策略的方法学偏好**

可迁移的仅是**维度树结构**（上下文 / 可获得性与报告字段；统计建模单独作为 S6 派生分析层）、**字段定义模式**和**方法学设计**。

---

## survey_of_surveys 自身 schema 抽取

本节把该论文投影到本目录自己的脚手架综述 schema（S1--S8）。判定等级只说明该维度在原文和本地证据链中的可用程度：`强` = 有明确原文结构和证据锚点；`中` = 有可复用结构但存在范围、裁决或精核限制；`弱` = 只作边界启发或风险提示；`不适用` = 原文类型不支持该维度进入统计池。

| 维度 | 判定等级 | 一句话抽取结果 | 证据位置 |
|---|---|---|---|
| S1 综述任务设定 | 强 | 本文是软件工程二次研究的系统映射，任务是审计 research artifact 的报告、可获得性、存放方式与时间/venue 影响。 | `review.md` §2.1--§2.4；`evidence_chain.md` A.3 `clm-research-artifacts-secondary-studies-type` |
| S2 语料收集与筛选 | 强 | 使用 Scopus、16 个 ISSN token / 15 个期刊、标题综述类关键词与 2013--2023 年窗口检索，643 篇初始结果经 IC1--IC3 筛选后纳入 537 篇。 | `review.md` §2.3、§2.5、维度树 §2.2；`evidence_chain.md` A.3 `clm-research-artifacts-secondary-studies-unit` |
| S3 原生维度树/样本编码对象 | 强 | 样本单位是每篇 secondary study；原生编码字段包括 year、venue、artifact availability、permanent repo、by request、dead link、dedicated section；logistic regression 属于派生统计输出，不是逐样本编码叶子。 | `paper_content.txt` §3--§4；`review.md` 维度树 §3--§5 |
| S4 字段级证据 | 中 | 正文支持聚合字段与统计表，但未核验 Zenodo 原始逐篇清单；当前强在 aggregate table，sample-level artifact list / sample ID / artifact link 待 A2a/Zenodo 核验。 | `paper_content.txt` Table 1；`review.md` §7 待复核、维度树 §3 |
| S5 维度模式演化 | 弱 | 原文没有说明字段、代码本或分类方案如何形成/迭代；year trend 是 artifact availability 等字段取值变化，不是 schema 演化。 | `paper_content.txt` 抽取流程与趋势统计；`GUIDE.md` §6.4 S5 定义 |
| S6 统计分析 | 强 | 统计分析包括 venue/year 交叉表、537/169/79 等分母切换，以及以年份和期刊预测 artifact availability 的二元 logistic regression。 | `review.md` §2.6--§2.7；`evidence_chain.md` A.2 `ev-research-artifacts-secondary-studies-denom` |
| S7 候选 finding | 强 | 候选发现是二次研究 artifact availability 在增长，但永久仓库/DOI 采用不足，Data Availability section 的表面透明度风险（作者批评，强度低于 169/537、65/169 等统计 finding）。 | `review.md` §2.7、§3、§6.1--§6.2 |
| S8 研究者/作者质疑与裁决 | 中 | 原文有人工筛选、Krippendorff’s Alpha、一致性评估、人工检查关键词上下文和 limitations，但无完整 disagreement adjudication log。 | `paper_content.txt` 方法与 threats；`review.md` §2.5、§2.8 |

### S1--S8 四分栏证据拆分

#### 总体统计池裁决

裁决：**后续主统计池候选，但当前仅按 `schema_seed` / `boundary_anchor` 使用；A2a 完成页码、Table 1、publisher final 与 Zenodo 原始逐篇清单精核前，不进入最终定量统计或目标领域 finding。** 该文是软件工程二次研究 research artifact 可获得性的系统映射，样本单位清楚（每篇 secondary study，n=537），具备 Scopus 检索、ISSN/标题/年份窗口、IC1--IC3 纳排、一致性评估、字段抽取、聚合表和 logistic regression；它适合进入 survey_of_surveys 的“字段树 + 统计分析 + 开放工件审计”方法模式池。限制是：正文主要给聚合统计，摘要声称的 comprehensive list 与逐篇编码表位于 Zenodo，当前尚未核验；本文统计对象是 SE 二次研究的 artifact availability，不能外推为 LLM/state-machine 领域事实。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要和 §1--§3 明确目标是评估 SE secondary studies 如何报告 research artifacts，并回答 RQ1 artifact 比例、RQ2 存放位置、RQ3 data availability 声明方式、RQ4 年份/venue 影响。 | 复原为“二次研究 artifact reporting / availability audit”的任务树：对象是 SE secondary studies，核心轴是 artifact 是否存在、是否持久存储、如何声明、随时间/venue 如何变化。 | **强；合格候选。** 可作为综述任务设定、RQ-to-field contract 与 artifact-audit 主题的统计池样本；只贡献方法模式，不贡献目标领域结论。 | 核对 IST publisher final 与 arXiv v3 对摘要、RQ 表述、标题和页码是否一致。 |
| S2 语料收集与筛选 | §2.1--§2.2：2024-10-02 在 Scopus 检索；16 个 ISSN token / 15 个期刊，标题限定 review/mapping/meta-analysis/scoping/critical 等词，2013--2023 年；643 篇初始结果经 IC1 年份、IC2 secondary study、IC3 SE-related 筛选后剩 537 篇；Krippendorff's Alpha=0.776。 | 复原为完整分母链：Scopus/ISSN/标题关键词/年份窗口 → title-abstract screening → 对 ACM CSUR 与 Computer Science Review 做 SE 相关人工判断 → 最终 N=537。 | **强；合格候选。** 可进入“是否有系统语料构造与可复核分母链”的统计池；中间数 643 不得冒充最终样本。 | 视觉核验检索式、16 个 ISSN token 与“15 个期刊”之间的对应；核对人工筛选和 alpha 的原文页码。 |
| S3 原生维度树/样本编码对象 | §2.3 与 Table 1(a)(b) 给出每篇 secondary study 的编码对象和字段：year、venue、artifact availability（Yes/No/By Request）、permanent repo、dead link、dedicated section；正文说明检查是否引用 external resource、是否位于 Figshare/Zenodo/Mendeley 等 permanent repository。 | 复原为扁平单表单树：上下文元数据（year、venue）× artifact 可获得性字段（availability、permanent repo、dedicated section、link health）。**logistic regression 属于 S6 派生统计分析，不是 S3 原生逐样本编码叶子。** | **强；合格候选但带边界。** S3 可统计为有明确样本单位和可复原字段树；不能把 Table 1(c) 回归系数当作原生编码字段。 | Zenodo 原始逐篇清单待核验：确认是否包含 sample ID、每篇标题/DOI、artifact URL、repository type、关键词命中与链接检查记录；核对是否存在正文未展开的更细 artifact 类型。 |
| S4 字段级证据 | 正文 Table 1 给出 venue/year 聚合计数与比例，§2.3 给出人工全文筛查 + Python keyword search + 100 字符上下文人工检查；Data availability 声明数据在 Zenodo。 | 字段级证据当前分两层：正文聚合表证据较强；逐样本字段证据依赖 Zenodo supplementary，尚未本地打开核验。 | **中；有条件候选。** 可统计为“有字段与聚合表”，但 sample-level evidence、sample ID 和 artifact link 不能在 A2a 前升级为已核验。 | 重点打开 Zenodo DOI `10.5281/zenodo.15488074`，核验逐篇编码表、字段名、脚本、关键词、链接检查日期、license 与版本；核对 Table 1 百分比分母。 |
| S5 维度模式演化 | 原文只说明按 Petersen guidelines 与 SIGSOFT Empirical Standards checklist 执行，并描述两轮数据抽取；没有说明字段/codebook 如何通过 open coding、pilot、迭代讨论或版本修订形成。 | 可复原为“先验字段 + 人工/脚本抽取”的静态编码方案；year trend 是字段取值随时间变化，不是 schema/维度模式演化。 | **弱；不建议进入主统计池强项。** 可作为“未报告维度演化过程”的边界样本，不应统计为有完整 schema evolution。 | 核验 Zenodo 中是否有 protocol、codebook revision、pilot notes 或 disagreement log；若没有，维持 S5=弱。 |
| S6 统计分析 | Table 1(a) venue 交叉表、Table 1(b) 年度统计、Table 1(c) binary logistic regression；§3 报告 169/537=31.5%、65/169=38.5%、65/537=12.1%、2023 年 49/79=62.0%、24/79=30.4%，year odds ratio=2.31。 | 复原为从 S3 字段派生出的统计分析层：frequency/proportion、year trend、venue comparison、binary logistic regression（year + journal 预测 artifact availability）。 | **强；合格候选。** 可作为“字段级数据 → 聚合统计/模型”的统计池样本；但所有具体比例、odds ratio 和 venue 发现只属于 SE secondary studies。 | PDF 视觉核验 Table 1(a)(b)(c) 行列、百分比分母、IST By Request 百分比疑点、less-than-10 publications 排除规则与 publisher final 差异。 |
| S7 候选 finding | §3、§5 从统计结果推出 artifact availability 增长、permanent repository/DOI 使用不足、non-permanent links 易失效、Data Availability section 可能只写 “no data was used” 或 “available upon request”，并建议强制发布 artifact。 | 复原为“统计观察 → gap/风险 → 政策建议”的 finding 链：availability gap、persistence gap、reporting-quality gap、automation-support rationale。 | **强但限界。** 可作为候选 finding 生成模式；不得把 31.5%、62.0%、30.4% 或具体 SE 期刊差异迁移为 Paper2 目标领域 finding。 | 核验每个 discussion claim 与 Table 1 的支撑关系；特别核验 “no data was used” 是否有频次或只是定性观察。 |
| S8 研究者/作者质疑与裁决 | §2.2 报告对部分期刊的人工 SE-related 判断和 Krippendorff's Alpha=0.776；§2.3 报告人工全文筛查、脚本关键词上下文由人工检查；§4 讨论排除会议、只用 Scopus、2013--2023 年窗口等限制。 | 复原为质量控制/人工裁决树：人工筛选、inter-rater reliability、人工上下文核验、limitations；但没有公开完整 disagreement adjudication log 或字段级双人编码一致性。 | **中；有限候选。** 可统计为存在研究者复核与质量控制，但不能统计为完整双人独立筛选/抽取/裁决日志。 | 核验 Zenodo 是否提供 reviewer 分工、冲突裁决、关键词列表、人工 override 记录、link-check 时间戳；若缺失，S8 不升为强。 |

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
