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
| DOI | [10.1016/j.infsof.2025.107830](https://doi.org/10.1016/j.infsof.2025.107830) |
| 本文自有开放工件 | Zenodo DOI：`10.5281/zenodo.15488074`；正文脚注与 Data availability 均指向该工件。 |
| 综述类型 | systematic mapping；对象是软件工程 secondary studies 的 research artifact 报告与可获得性。 |
| SE 子领域 | 横向方法学：secondary study artifacts / open science / reproducibility。 |
| 阅读状态 | 已读 `bibtex.bib`、`metadata.json`、`paper_content.txt` 全文；已用 `paper.pdf` 的 layout 文本核对 Table 1 关键数值与排版。 |
| 证据等级 | 全文文本级；关键表格已回 PDF 文本核对，但未做视觉截图级人工核验。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| A1 角色 | 为 Paper2 的“审计制品链 / 可复现证据资产”提供强相关字段锚点：artifact availability、permanent repository、DOI、dead link、by request、dedicated data availability section。 |
| 是否目标证据池 | 否；只作为 survey-of-surveys 脚手架和 Paper2 方法设计的模式先验。 |
| 一句话结论 | 这篇短映射研究把 secondary study 的开放研究工件从“口号”操作化为可统计字段，尤其适合迁移到 Paper2 的审计制品资产表；但它只统计有无与存放方式，未评估工件内容质量。 |

## 2. 论文内容详读

### 2.1 背景 / 问题

论文关注软件工程系统综述、系统映射和其他 secondary studies 的 research artifacts。作者给出四个动机：可重复 / 可复现、信任、后续更新、通向自动化。对 Paper2 最关键的是第四点：作者明确指出自动化系统综述需要既有研究工件来开发与验证质量，因此工件不只是“补充材料”，而是后续方法与工具的训练、验证和审计基础。

本文没有给出复杂的研究工件类型本体；它更偏操作化判断：一篇 secondary study 是否提供外部 research artifact，是否在永久仓库存放，是否有 DOI，是否在正文中用专门章节说明数据 / 工件可用性，链接是否失效，是否仅“upon request”。

### 2.2 研究目标

目标是评估软件工程 secondary studies 如何报告 research artifacts，并给出这些 artifacts 的总体可获得性图景。摘要中声称要提供 comprehensive list；但正文主体主要呈现统计表与方法，具体逐篇清单和更完整方法细节依赖其 Zenodo 工件。

### 2.3 方法概览

作者按 Petersen 等系统映射指南和 SIGSOFT Empirical Standards checklist 执行 systematic mapping。检索在 2024-10-02 结束，只使用 Scopus；检索范围由 13 个软件工程相关期刊与 2 个更广义计算机科学综述期刊的 ISSN 组成，并在标题中限定 review / mapping / meta-analysis / scoping review / critical review 等词。年份范围为 2013--2023，因为 Zenodo、Figshare 等关键仓库在这一时期后已可用。

### 2.4 RQ

正文以四个 RQ 组织结果：

1. 有多少 secondary studies 包含 research artifact。
2. research artifacts 存放在哪里，特别是是否使用带 DOI 的永久仓库。
3. 数据 / 工件可用性在论文中如何陈述，尤其是否有 dedicated section。
4. 出版年份和出版论坛如何影响 research artifact availability。

这个 RQ 组合不是领域主题型，而是“制品资产可获得性 + 报告方式 + 时间 / venue 影响”的方法学审计型 RQ。

### 2.5 语料 / 纳排 / 抽取

- 初始检索得到 643 篇文章。
- 纳入标准：2013--2023 年发表；属于 secondary study；与软件工程相关。
- 对 ACM Computing Surveys 和 Computer Science Review 中的条目，作者人工判断是否属于软件工程，因为这两个期刊并不只发软件工程论文。
- 作者用 Krippendorff’s Alpha 评估人工判断一致性，结果为 0.776（95% 置信区间），正文称为强一致。
- 最终纳入 537 篇 secondary studies。
- 数据抽取分两轮：先人工全文筛查，识别专门说明 research artifacts 可用性的章节；再用 Python 脚本做关键词搜索，打印每个关键词命中前后 100 个字符，由人工检查。
- 抽取判断包括：论文是否引用外部资源；外部资源是否位于永久仓库，例如 Figshare、Zenodo、Mendeley Data。

### 2.6 统计分析

核心统计是 Table 1：

1. 按 publication channel 统计总数、Yes、Permanent repo、No、By Request、Dead Link。
2. 按年份统计 Yes / No / By request / Dead / Permanent repo / Dedicated section。
3. 用二元 logistic regression 建模 artifact 是否可用，解释变量为年份和期刊；年份作为 scaled ordered factor，TSE 作为参考期刊；少于 10 篇样本的期刊被排除。

主要回归结果：年份是显著预测因子；每增加约 3 年，包含 research artifact 的 odds 增加 2.31 倍。相对于 TSE，若干期刊的系数为负且部分显著。这个结果可作为“趋势统计 → 解释性 finding”的例子，但不应被迁移为 Paper2 的领域事实。

### 2.7 主要结果

- 537 篇中 169 篇提供 research artifact，占 31.5%。
- 在提供 research artifact 的 169 篇中，65 篇位于永久仓库，占 38.5%；若以全部 537 篇为分母，永久仓库比例仅 12.1%。
- 2023 年 secondary studies 中 49 / 79 篇提供 artifact，占 62.0%；24 / 79 篇使用永久仓库，占 30.4%。
- 169 篇有 artifact 的论文中，50 篇有 dedicated section 声明数据或 research artifact 可用性，占 29.6%。Table 1 的 Dedicated section 总计为 72 / 537，因此 dedicated section 与真实开放 artifact 不是同一个概念，分母不能混用。
- 总体上开放实践在增长，但永久仓库和 DOI 的采用仍明显不足。
- 作者特别警示：即使在 2023 年，非永久仓库链接也可能很快失效；有些 Data Availability section 只写“no data was used”或“available upon request”，这对 secondary studies 来说是令人担忧的。

### 2.8 效度威胁 / 限制

作者列出三类限制：

1. 排除了会议论文。理由是高质量 secondary studies 多发表在期刊，且会议 proceedings 的 ISSN 与质量年度波动会带来噪声；作者认为这不太可能改变结论，但该判断仍限制外推。
2. 只使用 Scopus。作者认为 Scopus 已包含相关数据库的元数据；但如果研究目标是全文内容搜索，则多个数据库会是必要条件。
3. 只纳入 2013--2023。理由是要确保 Zenodo、Figshare 等永久仓库已进入可用期。

对 Paper2 来说，这些限制提示：如果要评估审计制品链，检索范围、全文可得性和平台生态时间点必须作为外推边界写清楚。

### 2.9 开放工件

本文本身提供 Zenodo 工件：正文脚注称 full details of research methods are available in research artifact，Data availability 也声明研究数据可在 Zenodo 获取。当前 review 只核验到正文和本地 PDF 中存在该 DOI；未打开 Zenodo 检查内部文件清单。因此，本文可作为“论文内 Data availability + DOI 工件”的正例，但其工件内容质量仍待复核。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 以“artifact 是否存在、存放在哪里、如何声明、年份/venue 如何影响”为核心；属于 evidence-asset audit 型 RQ。 | `paper_content.txt` Page 2--4 的 RQ1--RQ4。 | 高度可迁移到 Paper2：可把审计制品链拆成 availability、persistence、reporting、trend/context 四类问题。 | 不迁移具体比例到 Paper2 目标领域；该文对象是 SE secondary studies。 |
| dimension pattern | 字段包括 publication venue、year、artifact availability Yes/No、permanent repo、by request、dead link、dedicated section。 | `paper_content.txt` Page 2 Data extraction；Page 3 Table 1；PDF layout Table 1。 | 可直接作为 Paper2 制品资产字段树的初始锚点。 | 字段较粗，只统计有无与位置，不评估工件是否完整、可执行、脱敏、版本化。 |
| finding pattern | 以比例、年度趋势和 gap 形成 finding：artifact availability 改善，但永久仓库 / DOI 不足；Data Availability section 可能产生虚假透明度。 | `paper_content.txt` Page 3--5 Results / Conclusion。 | 可迁移为“统计观察 → 缺口 → 改进建议”的 finding 模板。 | 该文没有深入解释为什么不同期刊差异显著，也没有质量评分，不能迁移因果结论。 |
| evidence presentation pattern | 单个大表同时呈现 venue 分布、年度统计和 logistic regression；分母清晰，按 537 总体、169 artifacts 子集、79 篇 2023 子集切换。 | `paper_content.txt` Page 3 Table 1；`paper.pdf` layout 核对。 | 可迁移到 Paper2 的 audit asset dashboard：总样本、开放制品、永久仓库、断链、仅请求获取、专门声明章节。 | Table 1 很紧凑，若直接复用可能混淆分母；Paper2 需要把分母显式写进字段名或图注。 |
| validity / threat pattern | 限制集中在 venue scope、数据库 scope、年份窗口；并解释每个选择的理由。 | `paper_content.txt` Page 4 Limitations。 | 可迁移为 Paper2 的外推边界模板。 | 未讨论关键词漏检、keyword script recall、链接检查时间戳、artifact 内容质量误判等更细风险。 |
| report structure pattern | 短文结构：Introduction → Methods → Results → Limitations → Conclusion/Future Work → Data availability；结果严格按 RQ 展开。 | `paper_content.txt` Page 1--5。 | 可迁移为短方法学 evidence audit paper 的结构；Data availability 单列尤其重要。 | Paper2 还需要加入人机协同、schema 演化、内容证据 / 过程证据分离等方法贡献章节。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 综述元模型 | 把研究对象定义为“secondary study + research artifact + 报告位置 + 存储位置 + 持久标识”。 | 对 Paper2，可把对象定义为“目标论文 + 审计制品 + 内容证据 + 过程证据 + 持久入口”。 | 不要把 artifact availability 等同于 artifact quality。 |
| A1-M1 脚手架与种子探测 | 用 open science、FAIR、replicability、trust、updates、automation 解释为什么工件是研究对象。 | 可作为 Paper2 论证审计制品链必要性的背景先验。 | 需要与 Paper2 的 LLM/agent 审计语境重新表述，避免泛泛开放科学口号。 |
| A1-M2 维度模式批准 | 提供一组可执行字段：Yes / No / By request / Dead link / Permanent repo / DOI / Dedicated section。 | 可变成 Paper2 字段合同的 evidence-asset 模块。 | 字段必须加缺失语义和证据锚点；不能只让 agent 勾选。 |
| A1-M3 论文收集与概览 | 展示用期刊 ISSN、题名关键词、年份窗口和纳排标准构造 secondary study 语料。 | 可迁移为候选池总账与检索边界记录。 | 本文排除会议，不适合直接套到 Paper2 的所有 SE 研究对象。 |
| A1-M4 字段级内容证据抽取 | 采用人工全文筛查 + 关键词脚本 + 人工检查 100 字上下文。 | 可迁移为 Paper2 对 Data availability、artifact link、repository/DOI 字段的半自动抽取流程。 | 需要记录关键词、命中上下文、人工裁决理由和链接检查时间。 |
| A1-M5 统计分析 | 对可获得性做 venue/year 交叉统计与 logistic regression。 | 可迁移为 Paper2 的审计制品覆盖率、持久化率、断链率、版本化率统计。 | 统计观察不能直接变成领域发现；要保留分母和字段版本。 |
| A1-M6 候选发现 | 从统计结果形成改进建议：强制发布工件、使用永久仓库、设置 Data availability section。 | 可迁移为候选发现启发式：覆盖率缺口、持久性缺口、声明质量缺口、自动化支撑缺口。 | Paper2 的最终发现必须回到内容证据和研究者裁决，不可只由过程证据或统计表推出。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

面向 Paper2 的审计制品链，可从本文抽象出如下字段树：

```text
research_artifact_asset
├── artifact_availability_status
│   ├── yes_open_link
│   ├── no_artifact_found
│   ├── available_upon_request
│   ├── dead_link
│   └── unclear_or_not_checked
├── artifact_location
│   ├── repository_url
│   ├── repository_provider          # Zenodo / Figshare / Mendeley Data / GitHub / OSF / institutional / personal / other
│   ├── permanent_repository_flag    # yes / no / unknown
│   └── persistent_identifier_type   # DOI / none / other persistent ID / unknown
├── reporting_anchor
│   ├── dedicated_section_flag       # Data Availability / Artifact Availability / Replication Package 等
│   ├── section_name
│   ├── page_or_line_anchor
│   └── short_evidence_excerpt
├── link_health
│   ├── checked_at
│   ├── alive_dead_status
│   └── access_error_or_redirect_note
├── artifact_content_scope
│   ├── search_strategy_or_query
│   ├── screening_decisions
│   ├── included_study_list
│   ├── extraction_table
│   ├── analysis_script_or_notebook
│   ├── raw_outputs_or_logs
│   └── readme_or_reuse_instruction
├── access_and_license
│   ├── open_access
│   ├── license
│   ├── access_constraint
│   └── sensitive_or_redacted_content
└── audit_role
    ├── supports_replication
    ├── supports_trust
    ├── supports_update
    └── supports_automation_or_reanalysis
```

最值得直接采纳的维度锚点：

1. **可获得性不是二元变量**：至少区分开放可得、未提供、仅请求、断链、未检查。
2. **永久性要独立统计**：有链接不等于有持久仓库；有仓库也不等于有 DOI。
3. **报告位置要独立统计**：Data availability section 是定位信号，不保证真的有可复现工件。
4. **分母必须写死**：全部论文、提供 artifact 的论文、某一年论文是不同分母。
5. **链接检查要有时间戳**：dead link 是随时间变化的事实，必须保留 checked_at。
6. **工件质量另设字段**：本文没有评估 artifact quality；Paper2 若要支撑审计制品链，必须继续记录完整性、可执行性、版本、脱敏、README、字段覆盖率。

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

### 一句话结论

本文的维度树主类型为“证据资产审计树”，辅助类型为“artifact availability 统计树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-research-artifacts-secondary-studies-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-research-artifacts-secondary-studies-root] | Research artifacts in secondary studies 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-research-artifacts-secondary-studies-b1] secondary study corpus；[dim-research-artifacts-secondary-studies-b2] artifact type；[dim-research-artifacts-secondary-studies-b3] availability status；[dim-research-artifacts-secondary-studies-b4] repository / DOI evidence；[dim-research-artifacts-secondary-studies-b5] reproducibility gap | [ev-research-artifacts-secondary-studies-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-research-artifacts-secondary-studies-root] Research artifacts in secondary studies
├── [dim-research-artifacts-secondary-studies-b1] secondary study corpus
│   └── [leaf-research-artifacts-secondary-studies-scope] 研究范围与单位对象
├── [dim-research-artifacts-secondary-studies-b2] artifact type
│   └── [leaf-research-artifacts-secondary-studies-corpus] 语料与纳排链条
├── [dim-research-artifacts-secondary-studies-b3] availability status
│   └── [leaf-research-artifacts-secondary-studies-taxonomy] 主题与维度分类
├── [dim-research-artifacts-secondary-studies-b4] repository / DOI evidence
│   └── [leaf-research-artifacts-secondary-studies-method] 方法 / 技术 / 干预分类
└── [dim-research-artifacts-secondary-studies-b5] reproducibility gap
    └── [leaf-research-artifacts-secondary-studies-evidence] 评价、证据与复现资产
    └── [leaf-research-artifacts-secondary-studies-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-research-artifacts-secondary-studies-scope] | 研究范围与单位对象 | [dim-research-artifacts-secondary-studies-b1] | 定义 secondary study artifacts 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-research-artifacts-secondary-studies-leaf-scope] |
| [leaf-research-artifacts-secondary-studies-corpus] | 语料与纳排链条 | [dim-research-artifacts-secondary-studies-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-research-artifacts-secondary-studies-leaf-corpus] |
| [leaf-research-artifacts-secondary-studies-taxonomy] | 主题与维度分类 | [dim-research-artifacts-secondary-studies-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-research-artifacts-secondary-studies-leaf-taxonomy] |
| [leaf-research-artifacts-secondary-studies-method] | 方法 / 技术 / 干预分类 | [dim-research-artifacts-secondary-studies-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-research-artifacts-secondary-studies-leaf-method] |
| [leaf-research-artifacts-secondary-studies-evidence] | 评价、证据与复现资产 | [dim-research-artifacts-secondary-studies-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-research-artifacts-secondary-studies-leaf-evidence] |
| [leaf-research-artifacts-secondary-studies-finding] | 统计观察与候选发现 | [dim-research-artifacts-secondary-studies-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-research-artifacts-secondary-studies-leaf-finding] |

### 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据引用 | 结论引用 |
|---|---|---|---|---|---|---|---|
| [edge-research-artifacts-secondary-studies-method-evidence] | [leaf-research-artifacts-secondary-studies-method] | 支撑 / 度量 | [leaf-research-artifacts-secondary-studies-evidence] | 工具 / 指标 / 数据集 / artifact / not_reported | 未报告评价或复现资产时写 `not_reported` | [ev-research-artifacts-secondary-studies-taxonomy] | [clm-research-artifacts-secondary-studies-edge-method-evidence] |
| [edge-research-artifacts-secondary-studies-taxonomy-finding] | [leaf-research-artifacts-secondary-studies-taxonomy] | 导出候选发现 | [leaf-research-artifacts-secondary-studies-finding] | gap / recommendation / trend / limitation | 无 discussion 支撑时写 `not_reported` | [ev-research-artifacts-secondary-studies-stat] | [clm-research-artifacts-secondary-studies-edge-taxonomy-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-research-artifacts-secondary-studies-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-research-artifacts-secondary-studies-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-research-artifacts-secondary-studies-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-research-artifacts-secondary-studies-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | secondary study artifacts 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-research-artifacts-secondary-studies-transfer] |
| [leaf-research-artifacts-secondary-studies-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-research-artifacts-secondary-studies-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-research-artifacts-secondary-studies-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-research-artifacts-secondary-studies-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-research-artifacts-secondary-studies-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-research-artifacts-secondary-studies-001 | [ev-research-artifacts-secondary-studies-root] | [src-research-artifacts-secondary-studies-text], [src-research-artifacts-secondary-studies-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-research-artifacts-secondary-studies-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-research-artifacts-secondary-studies-002 | [ev-research-artifacts-secondary-studies-taxonomy] | [src-research-artifacts-secondary-studies-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-research-artifacts-secondary-studies-b1], [dim-research-artifacts-secondary-studies-b2], [dim-research-artifacts-secondary-studies-b3], [dim-research-artifacts-secondary-studies-b4], [dim-research-artifacts-secondary-studies-b5], [leaf-research-artifacts-secondary-studies-taxonomy], [leaf-research-artifacts-secondary-studies-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-research-artifacts-secondary-studies-003 | [ev-research-artifacts-secondary-studies-stat] | [src-research-artifacts-secondary-studies-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-research-artifacts-secondary-studies-evidence], [leaf-research-artifacts-secondary-studies-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-research-artifacts-secondary-studies-004 | [ev-research-artifacts-secondary-studies-risk] | [src-research-artifacts-secondary-studies-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-research-artifacts-secondary-studies-root], [leaf-research-artifacts-secondary-studies-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |
| EV-research-artifacts-secondary-studies-005 | [ev-research-artifacts-secondary-studies-relation] | [src-research-artifacts-secondary-studies-text] | paper_content.txt | 结果 / 讨论相关页；待 A2a 精确页码复核 | 关系 / 交叉表 / discussion 邻近段落 | 关系型表或交叉统计 | -- | 见释义 | 原文将分类字段与评价、工具、指标、artifact 或 discussion finding 连接，本记录用于支撑关系边；本行在 A1-DT 仅作关系边 seed，待 A2a 精确页码 / 表图核验后才能升级。 | taxonomy | not_verified | [edge-research-artifacts-secondary-studies-method-evidence], [edge-research-artifacts-secondary-studies-taxonomy-finding] | true | false | -- | 关系边只表示本文中的字段联系，不能外推为目标领域因果关系。 |

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-research-artifacts-secondary-studies-tree-type] | A1DT-research-artifacts-secondary-studies-C01 | 本文的维度树主类型为“证据资产审计树”，辅助类型为“artifact availability 统计树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-research-artifacts-secondary-studies-tree-type] | tree_type | [dim-research-artifacts-secondary-studies-root] | EV-research-artifacts-secondary-studies-001, EV-research-artifacts-secondary-studies-004 | 树型判断仅限本文，不代表所有 secondary study artifacts 综述。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-leaf-scope] | A1DT-research-artifacts-secondary-studies-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-research-artifacts-secondary-studies-scope] | EV-research-artifacts-secondary-studies-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-leaf-corpus] | A1DT-research-artifacts-secondary-studies-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-research-artifacts-secondary-studies-corpus] | EV-research-artifacts-secondary-studies-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-leaf-taxonomy] | A1DT-research-artifacts-secondary-studies-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-research-artifacts-secondary-studies-taxonomy] | EV-research-artifacts-secondary-studies-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-leaf-method] | A1DT-research-artifacts-secondary-studies-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-research-artifacts-secondary-studies-method] | EV-research-artifacts-secondary-studies-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-leaf-evidence] | A1DT-research-artifacts-secondary-studies-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-research-artifacts-secondary-studies-evidence] | EV-research-artifacts-secondary-studies-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-leaf-finding] | A1DT-research-artifacts-secondary-studies-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-research-artifacts-secondary-studies-finding] | EV-research-artifacts-secondary-studies-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-transfer] | A1DT-research-artifacts-secondary-studies-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-research-artifacts-secondary-studies-root] | EV-research-artifacts-secondary-studies-002, EV-research-artifacts-secondary-studies-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-finding-boundary] | A1DT-research-artifacts-secondary-studies-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-research-artifacts-secondary-studies-finding] | EV-research-artifacts-secondary-studies-003, EV-research-artifacts-secondary-studies-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |
| [clm-research-artifacts-secondary-studies-edge-method-evidence] | A1DT-research-artifacts-secondary-studies-C10 | 方法 / 技术节点与评价 / 证据节点之间存在可审计关系，适合作为 Paper2 字段间关系的 schema seed。 | relation_edge | [edge-research-artifacts-secondary-studies-method-evidence] | EV-research-artifacts-secondary-studies-005 | 关系含义限于本文分类和统计表，不代表因果关系。 | weak | schema_seed | false | -- |
| [clm-research-artifacts-secondary-studies-edge-taxonomy-finding] | A1DT-research-artifacts-secondary-studies-C11 | 主题 / 分类节点可通过统计观察或 discussion 支撑候选发现，但不能绕过研究者裁决。 | relation_edge | [edge-research-artifacts-secondary-studies-taxonomy-finding] | EV-research-artifacts-secondary-studies-005 | 候选发现仍需反证、scope 与 claim strength 审核。 | weak | candidate_finding | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-research-artifacts-secondary-studies-structure-check] | [dim-research-artifacts-secondary-studies-root], A1DT-research-artifacts-secondary-studies-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-research-artifacts-secondary-studies-visual-check] | EV-research-artifacts-secondary-studies-002, EV-research-artifacts-secondary-studies-003, EV-research-artifacts-secondary-studies-005 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
