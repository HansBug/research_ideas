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

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 leaf / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生 schema。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__codex.md](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__codex.md)、[../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__claude.md](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__claude.md)、[../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__deepseek.md](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md](../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md)。

### v2 主线程采用说明

本节采用 `deepseek` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修 / needs repair”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 supplementary 精核。

#### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `research-artifacts-secondary-studies` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是；已逐段通读 358 行全文（含 abstract、introduction、methods、results、discussion、limitations、conclusion、references） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；`bibtex.bib` 确认期刊 IST vol 187 / 2025-11，`metadata.json` 确认 DOI、出版日期 2025-07-07、arXiv v3 / 2026-04-16 及 eligibility meta |
| 是否打开或核对 `paper.pdf` | 是；已用 `pdftotext -layout` 逐页提取 PDF（共 6 页），核对了 Table 1(a)/(b)/(c) 的完整行列值与正文统计数字的一致性。未做视觉截图级人工核验（OCR 面检）。 |
| 原文类型 | systematic mapping（系统映射）；对象为软件工程 secondary studies 的 research artifact 报告与可获得性 |
| 被编码样本单位 | 每篇 secondary study（n = 537） |
| 样本数量 / 分母 | 537（初始检索 643 → 经 IC1/IC2/IC3 筛选 → 最终纳入 537） |
| 原生树类型 | **单树**（single tree）：三主干（上下文元数据 × 制品可获得性 × 统计建模），每主干下 2–4 个叶子字段。结构简单、紧凑、可完整复原。 |
| 主统计池资格 | **是**。本文是一次系统映射研究（systematic mapping），有系统检索、纳排标准、一致性子评估（Krippendorff's Alpha = 0.776）、两轮数据抽取和 logistic regression 建模。537 个样本单位全部可追溯到纳入标准。 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 needs repair；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、supplementary 风险进入 A2a。 |

---

#### 1. 原文证据阅读说明

##### 1.1 实际读取文件清单

| 文件 | 读取方式 | 读取范围 |
|---|---|---|
| `paper_content.txt` | 全文通读（358 行） | Abstract → Introduction → Methods (§2.1–2.3) → Results (§3, RQ1–RQ4) → Limitations (§4) → Conclusion (§5) → References [1]–[10] |
| `bibtex.bib` | 全文读取 | 完整 BibTeX entry |
| `metadata.json` | 全文读取 | 所有字段（含 eligibility meta） |
| `review.md` | 全文读取（375 行） | 快速结论卡片 → 论文内容详读 → A.1–A.4 |
| `paper.pdf` | `pdftotext -layout -f 1 -l 6` 逐页提取 | 完整 6 页；特别核验 Table 1(a)/(b)/(c) 行列值 |

##### 1.2 PDF 版面核验状态

PDF 共 6 页。已通过 `pdftotext -layout` 核对以下内容与 `paper_content.txt` 一致性：
- Table 1(a)：15 个期刊 × 6 列（Total / Yes / Permanent repo / No / By Request / Dead Link）—数值完整核验
- Table 1(b)：11 年 × 7 行（Yes / No / By req. / Dead / Permanent repo / Dedicated section / Total）—数值完整核验
- Table 1(c)：logistic regression 系数、标准误、z-value、p-value、odds ratio —完整核验

**仍需 PDF 视觉截图核验**：论文仅 6 页，没有复杂彩色图表；但 Table 1(a) 中 Permanent repo 列的百分比计算基准（是 Yes 的子集还是 Total 的子集）和 Dead Link 的合计逻辑（22 of 537 = 4.1%，但行内百分比不同）值得视觉确认；建议 A2a 做一次 PDF 页面截图人工核验。

##### 1.3 12 个关键原文证据锚点

| # | 锚点 | 原文位置 | 短引或释义 |
|---|---|---|---|
| 1 | 研究目标与动机 | Abstract + §1 Introduction | 评估 SE secondary studies 如何 report research artifacts，给出四大理由：replicability、trust、updates、pathway to automation |
| 2 | 检索策略 | §2.1 Search process | Scopus 单数据库；15 个 ISSN（13 SE + 2 CS review）；标题限定 review/mapping/meta-analysis/scoping/critical；2013–2023 |
| 3 | 纳排标准 IC1–IC3 | §2.2 Study selection | IC1: 2013–2023；IC2: secondary study；IC3: SE-related |
| 4 | 一致性子评估 | §2.2 | Krippendorff's Alpha = 0.776（95% CI），强一致 |
| 5 | 初始与最终样本数 | §2.2 | 初始检索 643 → 最终纳入 537 |
| 6 | 数据抽取两轮方案 | §2.3 Data extraction | Round 1: 人工全文筛查 dedicated section；Round 2: Python keyword search + 100-char 上下文人工核验 |
| 7 | RQ1 核心统计 | §3 Results / §2.3 / Table 1(a) | 169 / 537 (31.5%) 包含 research artifact |
| 8 | RQ2 permanent repository 统计 | Table 1(a)/(b) | 65 / 169 (38.5%) 使用永久仓库；占全部 537 的 12.1% |
| 9 | RQ3 reporting mechanism 统计 | §3 / Table 1(b) | 50 / 169 (29.6%) 有 dedicated data availability section；2023 年升至 46 / 79 = 58.2% |
| 10 | RQ4 logistic regression | Table 1(c) | Year 作为 scaled ordered factor：每 3 年 odds ratio = 2.31，p < 0.001 |
| 11 | Dead link 统计 | Table 1(a)/(b) / §5 | 22 / 537 (4.1%)；2023 年仍 2 / 19 个 non-permanent link 已死 |
| 12 | "no data used" / "upon request" 异常发现 | §5 / Discussion | 部分含 "Data Availability" section 的论文声称 "no data was used" 或 "available upon request"——被作者标记为 alarming |

---

#### 2. 样本单位与字段来源判定

##### 2.1 原文纳入和逐项描述的对象是什么？

**每篇已发表的软件工程 secondary study**（系统综述/系统映射/meta-analysis/scoping review 等），发表于 2013–2023 年间，源自 15 个期刊（13 个 SE 相关 + 2 个更广义 CS 综述期刊）。纳入后共 537 篇。

每篇 secondary study 被编码的**不是其研究内容本身**（不涉及 SE 子领域、方法学、RQ 等），而是其**研究工件的可获得性与报告方式**。

##### 2.2 作者有没有系统检索/纳排/数据抽取/编码方案？

有，且较为完整：

1. **检索**：Scopus 单一数据库；ISSN 限定 15 个期刊；标题关键词限定 review/mapping/meta-analysis 等 9 个术语；年份限定 2013–2023（因为 Zenodo 2013 年上线、Figshare 2011 年上线）。初始 643 篇。
2. **纳排**：IC1（年份）、IC2（是否为 secondary study）、IC3（是否 SE 相关）。title-abstract screening + 人工判定（对 ACM Computing Surveys 和 Computer Science Review 非纯 SE 期刊）。
3. **质量/一致性子评估**：Krippendorff's Alpha = 0.776，正文标注为强一致。
4. **数据抽取**：两轮——Round 1 人工全文筛查 dedicated artifact availability section；Round 2 自动化 Python keyword search + 100 字符上下文人工核验。
5. **编码方案**：检查每篇是否引用外部 research artifact、是否在永久仓库存放、是否有 DOI。

##### 2.3 原文字段来自哪里？

字段直接来自**数据抽取方案**（§2.3）和 **Table 1 统计表**：
- **artifact_availability**：Yes / No / By Request（§2.3 描述 + Table 1(a) 列）
- **permanent_repository**：Permanent repo 列（Table 1(a)）——"if it is located in a permanent repository, such as Figshare, Zenodo or Mendeley"（§2.3）
- **dedicated_section**：Dedicated section 行（Table 1(b)）——"dedicated sections indicating the availability of research artifacts"（§2.3）
- **link_health**：Dead Link 列（Table 1(a)）
- **year**：Table 1(b) 列（2013–2023）
- **venue**：Table 1(a) 行（15 个期刊）
- **regression_odds**：Table 1(c) logistic regression 模型输出

**完整逐篇原始编码数据**存储于 Zenodo 工件（DOI: `10.5281/zenodo.15488074`），不在正文内，正文仅呈现聚合统计表。目前 A1-DT 审计**未访问该 Zenodo 工件**——这是一个重要的证据缺口。

##### 2.4 RQ 与样本单位是什么关系？

RQ 是**结果组织方式**，不是树根也不是字段本身：

- RQ1（有多少篇有 artifact）→ 使用字段 `artifact_availability`
- RQ2（存放在哪）→ 使用字段 `permanent_repository`
- RQ3（如何报告）→ 使用字段 `dedicated_section` + 定性发现（"no data used" / "upon request"）
- RQ4（年份/venue 影响）→ 使用字段 `year` × `venue` × `artifact_availability`，输出 logistic regression model

RQ 是一组**围绕"制品可获得性"单一主题的问题**，它们共享同一个样本池（537 篇），使用同一套数据抽取字段的不同子集。

##### 2.5 是否有降级必要？

**不需要降级**。本文是完整的 systematic mapping study，具有系统样本库、明确纳排标准、一致性子评估和统计建模。完全满足主统计池资格。

---

#### 3. 原生样本编码维度树/维度森林

本文是**单树**（single tree）结构，非维度森林。每个样本单位（secondary study）被编码为一条记录，共享同一套字段。字段分属三个主干节点。

```
[dim-research-artifacts-secondary-studies-root] Secondary Study (n=537)
│
├── [node-ctx] 上下文元数据（Context Metadata）
│   ├── [leaf-year] publication_year
│   │   取值空间：2013 | 2014 | 2015 | ... | 2023（共 11 个离散整数值）
│   │   取值空间类型：完整枚举（ordinal）
│   │
│   └── [leaf-venue] publication_venue
│       取值空间：ACM Computing Surveys | ACM TOSEM | Automated Software Engineering |
│                Computer Science Review | Empirical Software Engineering | IEEE Software |
│                IEEE TSE | IST | JSEP | JSS | Requirements Engineering |
│                Software: Practice & Experience | SoSyM | Software Quality Journal |
│                Software Testing: Verification & Reliability（共 15 个值）
│       取值空间类型：完整枚举（categorical，nominal）
│
├── [node-artifact] 研究制品可获得性（Artifact Availability）
│   ├── [leaf-availability] has_research_artifact
│   │   取值空间：Yes | No | By Request（3 个值）
│   │   取值空间类型：层级枚举（tiered categorical；By Request 与 No 统计上分开处理，但讨论中合并为"无直接公开工件"）
│   │
│   ├── [leaf-permanent] uses_permanent_repository  [条件分支：仅当 has_research_artifact = Yes]
│   │   取值空间：Yes（permanent with DOI）| No（non-permanent：personal page, institutional page, GitHub, etc.）
│   │   取值空间类型：布尔（binary，条件可见）
│   │   注：Table 1(a) 的 Permanent repo 列为 Yes 的子集，百分比以 Yes = 169 为分母
│   │
│   ├── [leaf-section] has_dedicated_data_availability_section  [条件分支：仅当 has_research_artifact = Yes]
│   │   取值空间：Yes | No
│   │   取值空间类型：布尔（binary，条件可见）
│   │   注：Table 1(b) Dedicated section 行的值以当年 Total 为分母（非仅 Yes 子集）
│   │
│   └── [leaf-link] link_is_dead
│       取值空间：Yes（dead）| No（alive）
│       取值空间类型：布尔（binary）
│
└── [node-model] 统计建模输出（Statistical Model Output）
    └── [leaf-regression] logistic_regression_coefficient
        取值空间：Table 1(c) 中每个 journal 的 Coef、Std.E、z value、p value、Odds ratio
        取值空间类型：数值或区间（numerical with SE and p-value）
        注：这是对 [leaf-availability] 的统计建模结果，不是每篇样本的直接编码字段。
```

**缺失部分说明**：
- 逐篇原始编码数据（Zenodo DOI: `10.5281/zenodo.15488074`）未在 A1-DT 审计中访问。该工件可能包含更细粒度的字段（如 artifact 具体类型分类、repository provider 分类：Zenodo / Figshare / Mendeley / GitHub / personal page 等），以及每篇论文的标题、DOI、作者等元数据。这些需要 **A2a 精核任务** 从 Zenodo 工件中提取补充。
- 原文未对 artifact **内容质量**做任何评估（作者在 §5 Conclusion and Future work 中明确将此列为"important future study area"），因此不存在 artifact 质量维度。

---

#### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `[leaf-year]` | 发表年份 | `[node-ctx]` | §2.1（纳入标准 IC1）/ Table 1(b) 表头 | secondary study 的出版年份 | 2013, 2014, ..., 2023（11 个值） | 完整枚举（ordinal） | 不可能缺失（所有纳入文献都有年份） | RQ4：作为 logistic regression 的 ordered factor；Table 1(b) 年度趋势统计 | Paper2 可将"发表年份"作为制品可获得性的时间趋势分析锚点 | 锚点 2, 5；Table 1(b) | 通用字段，可迁移到任何 survey-of-surveys |
| `[leaf-venue]` | 发表期刊 | `[node-ctx]` | §2.1（ISSN 搜索限定）/ Table 1(a) 行标签 | secondary study 发表的期刊名称 | 15 个期刊名称（完整枚举） | 完整枚举（nominal） | 不可能缺失（检索即按 ISSN 限定） | RQ4：作为 logistic regression 的 reference category 比较 | Paper2 可按 venue 分析制品报告规范差异 | 锚点 2；Table 1(a) | SE 期刊限定；Paper2 若跨领域需扩展 venue 列表 |
| `[leaf-availability]` | 是否有研究制品 | `[node-artifact]` | §2.3（data extraction 描述）/ Table 1(a) Yes/No/By Request 列 | 该 secondary study 是否提供外部可访问的 research artifact | Yes \| No \| By Request | 层级枚举（tiered categorical） | 不存在缺失；所有 537 篇全部编码 | RQ1 主统计（169/537 = 31.5%） | Paper2 审计制品资产表的核心布尔字段 | 锚点 6, 7；Table 1(a) | 定义依赖"什么是 research artifact"——原文未形式化定义，依赖人工判断 |
| `[leaf-permanent]` | 是否使用永久仓库 | `[node-artifact]` | §2.3（"permanent repository, such as Figshare, Zenodo or Mendeley"）/ Table 1(a) Permanent repo 列 | 制品的存储位置是否为永久仓库且有 DOI | Yes（permanent with DOI）\| No（non-permanent） | 布尔（条件可见：仅当 `has_research_artifact = Yes`） | 当 `has_research_artifact ≠ Yes` 时字段不适用 | RQ2：65/169 (38.5%) of Yes = 12.1% of all | Paper2 审计制品资产的"链接稳定性"代理指标 | 锚点 8；Table 1(a) Permanent repo 列 | 能迁移；需注意原文未对 GitHub（public 但非 DOI）做额外分类 |
| `[leaf-section]` | 是否有专用数据可用性章节 | `[node-artifact]` | §2.3（"dedicated sections indicating the availability"）/ Table 1(b) Dedicated section 行 | 论文正文是否包含专门章节声明数据/制品可用性 | Yes \| No | 布尔 | 不存在缺失；"无 dedicated section" 视为 No | RQ3：72/537 (13.4%) overall；2023 年 46/79 (58.2%) | Paper2 可检查纳入论文是否有明确的数据可用性声明 | 锚点 9；Table 1(b) Dedicated section 行 | 高度可迁移；Dedicated data availability section 是跨领域 open science 实践 |
| `[leaf-link]` | 链接是否失效 | `[node-artifact]` | §5（"2 out of 19 links to non-permanent repositories are already dead"）/ Table 1(a) Dead Link 列 | 制品的外部链接是否能正常访问 | Yes（dead）\| No（alive） | 布尔 | 当没有外部链接时字段不适用 | 作为制品可获得性的可靠性侧面证据 | Paper2 可追踪纳入工件的链接健康度 | 锚点 11；Table 1(a) Dead Link 列 | 取决于检查时间点；原文未记录检查日期 |
| `[leaf-regression]` | logistic 回归系数 | `[node-model]` | §3 RQ4 / Table 1(c) | binary logistic regression 对 has_research_artifact 建模的输出 | Coef: -∞ to +∞；Odds ratio: 0 to +∞；p value: 0–1 | 数值或区间（含 SE 和 p-value） | 不适用 | RQ4 全部分析 | Paper2 可参考 logistic regression 作为跨论文趋势分析方法 | 锚点 10；Table 1(c) | 统计方法可迁移；系数值不可迁移 |

---

#### 5. 关系边表

本论文的编码 schema 是扁平单表结构（flat single-table），每个样本单位为一行，字段之间没有在原文中显式建模的关系边（没有外键、一对多、多对多等关系型结构）。

但是，论文中有以下**统计关系**值得记录为隐式关系边（可作为 Paper2 方法的 schema seed）：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `[edge-year-availability]` | `[leaf-year]` | 时间趋势（logistic regression predictor） | `[leaf-availability]` | Yes/No/By Request | N/A | Table 1(b)/(c)：year 为 ordered factor，odds ratio = 2.31 per 3 years | Paper2 方法学参考：可在自己的 survey-of-surveys 中对"制品可获得性是否随时间改善"做类似建模 |
| `[edge-venue-availability]` | `[leaf-venue]` | 期刊效应（logistic regression predictor） | `[leaf-availability]` | Yes/No/By Request | N/A | Table 1(c)：各期刊 vs reference (IEEE TSE) 的 odds ratio | Paper2 方法学参考：vennue 层面制品报告规范的差异分析 |
| `[edge-availability-permanent]` | `[leaf-availability]` | 条件子字段（conditional sub-field） | `[leaf-permanent]` | Yes/No | 条件不可见（仅当 availability = Yes） | Table 1(a) Permanent repo 列为 Yes 子集 | schema seed：条件字段在 Paper2 的审计资产表中是常见模式 |

**未发现显式关系边**：原文没有在样本单位之间建立引用、依赖或层级关系；也不存在跨表外键、nested hierarchy 或 graph 结构。这是一个经典的横截面统计设计（cross-sectional mapping），不是关系型/网络型研究。若 Paper2 的 coding schema 需要样本间关系边，必须从其他论文引入，不能从此文导出。

---

#### 6. 统计观察、候选 finding 与 final finding 边界

##### 6.1 原文中由字段/统计表支持的统计观察

以下直接来自 Table 1(a)/(b)/(c) 和 §3 Results：

| 统计观察 | 来源 | 证据强度 |
|---|---|---|
| 169 / 537（31.5%）的 SE secondary studies 包含 research artifact | Table 1(a) | strong（直接计数） |
| 65 / 169（38.5%）的含 artifact 论文使用永久仓库+DOI；即全体 537 篇的 12.1% | Table 1(a)/(b) | strong（直接计数） |
| 22 / 537（4.1%）的论文链接已失效 | Table 1(a) | moderate（链接检查时间点未记录） |
| 16 / 537（3.0%）的论文声称 artifact "upon request" | Table 1(a) | strong（直接计数） |
| 2023 年 artifact availability 升至 62.0%（49/79） | Table 1(b) | strong |
| 2023 年 permanent repository 使用率升至 30.4%（24/79） | Table 1(b) | strong |
| 2023 年 dedicated section 拥有率升至 58.2%（46/79） | Table 1(b) | strong |
| Publication year 是 artifact availability 的显著预测因子（ordered factor, odds ratio = 2.31 per 3 years, p < 0.001） | Table 1(c) | strong（模型已报告） |
| 部分期刊（CS Review, SP&E, JSEP, IST）的 artifact availability 显著低于 reference category（IEEE TSE） | Table 1(c) | strong |

##### 6.2 原文 discussion/recommendation 提出的候选 finding

以下来自 §4 Limitations 和 §5 Conclusion and Future work：

| 候选 finding | 类型 | 证据支持状态 |
|---|---|---|
| "both 'no data was used' and 'available upon request' are alarming for secondary studies" | 方法学批评（methodological critique） | moderate：基于观察事实（16 篇 "upon request"），但未量化 "no data was used" 的频次 |
| "journals should enforce the reporting practices of research artifacts" | 政策建议（policy recommendation） | weak：作者主张，非实验证据 |
| "identifying which research artifacts have sufficient quality is an important future study area" | 未来研究方向（future work direction） | weak：方向性建议 |
| "links to non-permanent repositories can become inaccessible"（2023 年仍有 2/19 dead） | 经验观察（empirical observation） | moderate：基于 2023 年 19 个链接中 2 个失效的观察，但样本量小 |

##### 6.3 对 Paper2 可迁移的方法学启发

| 启发 | 迁移方式 |
|---|---|
| 将"artifact availability"操作化为多值分类（Yes / No / By Request），而非简单二分 | Paper2 审计资产表的 `availability_status` 字段可参考 |
| 区分 permanent repository（带 DOI）与 non-permanent（personal/institutional page/GitHub 无 DOI），并记录 dead link | Paper2 资产表的 `storage_type` 和 `link_health` 字段 |
| 检查纳入论文是否包含 dedicated data availability section | Paper2 可作为 review 质量的一个代理指标 |
| logistic regression 作为跨论文趋势/venue 分析的方法 | Paper2 方法学参考 |
| 报告逐篇原始数据（Zenodo 工件）并声明 FAIR 数据原则 | Paper2 应遵循相同实践 |

##### 6.4 绝不能迁移的领域结论

本文是 **software engineering secondary studies** 的领域特定研究，以下内容绝不能直接迁移到 Paper2（LLM + 状态机形式化建模领域）：

- **任何具体百分比**（31.5%、62.0%、30.4%、38.5%、12.1% 等）——这些是 SE 领域的统计值
- **logistic regression 的具体系数和 odds ratio**
- **"SE community is improving" 的时间趋势陈述**
- **对特定 SE 期刊（IST、JSS、TSE 等）的 venue 级发现**
- **对 Scopus 检索和 ISSN 检索策略的方法学偏好**

可迁移的仅是**维度树结构**（三主干：上下文 / 可获得性 / 统计建模）、**字段定义模式**和**方法学设计**。

---

#### 7. 对旧版 `review.md` 的返修来源

##### 7.1 问题诊断

旧版 `review.md` 的核心问题是**维度树被跨论文通用六叶投影覆盖，原文真实编码 schema 被架空**：

1. **"范围"叶**（A1DT-research-artifacts-secondary-studies-C01）：将原文的样本单位、纳排标准和检索策略提炼为"范围"是合理的，但把 15 个期刊、ISSN 检索、IC1–IC3 全部收入一个叶子过于宽泛。原文实际上有独立的 `[leaf-year]`、`[leaf-venue]` 和 `[leaf-availability]`（含纳排过滤），它们不是"范围"的子树，而是**编码维度本身**。

2. **"语料"叶**（A1DT-research-artifacts-secondary-studies-C02）：将 537 篇 secondary studies 作为"语料"描述主体，但原文不区分"语料"和"样本"——537 篇就是样本，没有外部语料概念。这是把 NLP/DL 论文的"语料"概念强行套用到 systematic mapping 上。

3. **"分类"叶**（A1DT-research-artifacts-secondary-studies-C03）：把 artifact availability 的 Yes/No/By Request 和 permanent repository 归为"分类"是合理的覆盖，但缺失了 dedicated section、link health 和 regression output。

4. **"方法"叶**（A1DT-research-artifacts-secondary-studies-C04）：原文的方法是 systematic mapping + logistic regression，但方法本身不是"维度树"的叶子——它是生产维度树的**过程**。在维度树中混入方法节点会混淆"样本被编码成什么"和"样本怎么被编码"。

5. **"证据"叶**（A1DT-research-artifacts-secondary-studies-C05）：原文的所有叶子字段都可支撑统计观察，不存在独立的"证据"叶子。

6. **"发现"叶**（A1DT-research-artifacts-secondary-studies-C07）：原文的讨论结论是"候选 finding"，不是维度树的编码维度。

7. **A.1–A.4 结构**：现有 A.1/A.2/A.3/A.4 使用了大量跨论文的抽象标识符（`A1DT-research-artifacts-secondary-studies-C01` 至 `C13`），这些标识符把原文事实封装在了跨论文投影的语言中，导致"样本编码 schema"不可直接阅读。

##### 7.2 按 C/I/M 分级的返修建议

###### C（Critical，阻塞级）

| # | 问题 | 建议 |
|---|---|---|
| C1 | 维度树仍然是六叶通用投影，不是原文真实编码 schema | 用本报告 §3 的三主干单树重写"维度树复原"章节。删除六叶通用接口节点。维度树应描述：root = Secondary Study (n=537) → 三主干（上下文 / 制品可获得性 / 统计建模）→ 每个主干的叶子字段。 |
| C2 | A.1--A.4 使用了跨论文抽象标识符，原文事实被封装在投影语言中 | A.1 维度树定义应从跨论文投影标识符（C01–C13）中解耦，用原文术语和原文表编号重构。A.2 证据账本应与 Table 1(a)/(b)/(c) 的行列锚点对齐。 |
| C3 | SUMMARY 表中"样本单位/样本数量/原生树类型/统计池资格"需要修正 | 样本单位 = 每篇 secondary study（非"研究工件"）；原生树类型 = 单树（非维度森林）；统计池资格 = 是（非局部可统计）。当前 review.md 中若已有 SUMMARY 表，需同步更新。 |

###### I（Important，重要级）

| # | 问题 | 建议 |
|---|---|---|
| I1 | review.md 未提及 Table 1(a) 中 Permanent repo 列的百分比计算基准差异 | 补充说明：Permanent repo 列以 `has_research_artifact = Yes`（169）为分母，不是以 Total（537）为分母。该差异影响 Paper2 字段的取值空间类型判定。 |
| I2 | review.md 未区分"原文统计观察"与"候选 finding" | 增加一节明确列出：哪些是直接来自 Table 1 的统计事实（strong evidence），哪些是 discussion/recommendation 的候选 finding（weak/moderate）。 |
| I3 | review.md 提到 "no data was used" 但未给出频次 | 原文本身也**未给出 "no data was used" 的频次**（仅提及为 qualitative observation）。review.md 应注明此为原文中的定性提及，非可统计字段。 |
| I4 | Zenodo 工件未检查 | A.4 应新增一项：check Zenodo artifact (`10.5281/zenodo.15488074`) 获取逐篇原始编码表，补充可能被正文省略的细粒度字段（repository provider 分类、paper title/DOI/author metadata 等）。标记为 A2a 精核任务。 |

###### M（Minor，建议级）

| # | 问题 | 建议 |
|---|---|---|
| M1 | review.md 中 "A1 角色" 一栏写的"审计制品链 / 可复现证据资产"偏笼统 | 精化为："A1 角色：为 Paper2 的 artifact availability schema 提供三字段锚点（has_artifact × permanent_repo × dedicated_section），尤其是条件字段设计（permanent_repo 仅在 has_artifact=Yes 时有效）和 link health 跟踪模式。" |
| M2 | review.md 引用 arXiv v3 / 2026-04-16 但出版日期为 2025-07-07 | 在版本号处加注：正式出版（IST vol 187 / 2025-11）与开放预印本（arXiv v3 / 2026-04-16）的版本差异，避免读者混淆 |
| M3 | 缺少明确的"非目标证据池"声明 | 已在 review.md 第 1 节注明"是否目标证据池 = 否"，但可加强为："本文是 SE 领域的方法学映射研究，所有统计数字不能迁移到 LLM+状态机领域，仅 schema 结构可迁移。" |

---

#### 8. 审计附录草案：证据账本与结论映射

##### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt / paper.pdf | §2.1 Search process | "resulting in 643 articles" | 初始检索得到 643 篇文章 | 样本池来源 | strong | [dim-root] 样本数量 | 否（文本明确） | Scopus 单一数据库，SE 期刊限定 |
| EV-002 | paper_content.txt / paper.pdf | §2.2 Study selection | "After applying the inclusion criteria, 537 secondary studies remained" | 经 IC1–IC3 筛选后 537 篇纳入 | 样本池数量确认 | strong | [dim-root] 样本数量 | 否 | 排除 conference proceedings |
| EV-003 | paper_content.txt / paper.pdf | §2.2 | "Krippendorff's Alpha ... 0.776 on a 95% confidence interval" | 评定者间一致性为 0.776（强一致） | 编码质量代理 | strong | [dim-root] 编码可靠性 | 否 | 仅一人工作时间段的 agreement |
| EV-004 | paper_content.txt / paper.pdf | §2.3 Data extraction | "two rounds: (1) manually and (2) automatically" | 两轮数据抽取：人工全文 + 自动关键词 | 编码方案描述 | strong | [leaf-availability], [leaf-permanent], [leaf-section] | 否 | 未描述具体 keyword list |
| EV-005 | paper.pdf (Table 1a) | Table 1(a) | "Total 537, Yes 169 (31.5%), Permanent repo 65 of 169 (38.5%), No 330 (61.5%), By Request 16 (3.0%), Dead Link 22 (4.1%)" | 制品可获得性的全表统计 | 核心统计事实 | strong | [leaf-availability], [leaf-permanent], [leaf-link] | 是（Permanent repo 百分比分母需视觉确认） | SE 领域限定 |
| EV-006 | paper.pdf (Table 1b) | Table 1(b) | "2023: Yes 49 (62.0%), Permanent repo 24 (30.4%), Dedicated section 46 (58.2%)" | 2023 年度细分统计 | 年度趋势事实 | strong | [leaf-year], [leaf-availability], [leaf-permanent], [leaf-section] | 是（行排列对齐需确认） | 仅 2013–2023 |
| EV-007 | paper.pdf (Table 1c) | Table 1(c) | "Year (Ordered factor): Coef 0.84, Std.E 0.12, z value 7.21, p = 5.79e-13, Odds ratio = 2.31" | 出版年份显著预测 artifact availability | 统计建模事实 | strong | [leaf-regression], [leaf-year] → [leaf-availability] | 否（数字明确） | 期刊限定、reference category = IEEE TSE |
| EV-008 | paper_content.txt | §5 / Discussion | "2 out of 19 links to non-permanent repositories are already dead" (2023 年) | 2023 年仍有 dead link | 链接可靠性证据 | moderate | [leaf-link] | 否 | 样本量小（n=19 for 2023 non-permanent） |
| EV-009 | paper_content.txt | §5 / Discussion | "some papers with their 'Data Availability' section simply state that 'no data was used'" | 部分含 dedicated section 的论文声称无数据 | 数据可用性声明质量问题 | weak（定性提及，未量化频次） | [leaf-section] 的质量侧面 | 否 | 频次未知 |
| EV-010 | paper_content.txt | §2.1 | ISSN list: 0928-8910, 1382-3256, ..., 1574-0137（15 个） | 检索限定的 15 个期刊 ISSN | venue 范围证据 | strong | [leaf-venue] | 否 | SE 期刊限定，排除 conference |
| EV-011 | metadata.json | metadata.json | "Zenodo DOI: 10.5281/zenodo.15488074" | 本文自身的研究工件位置 | 可复现性证据 | strong | 全部维度树——逐篇原始数据在 Zenodo | N/A（需下载 Zenodo） | 当前 A1-DT 未访问 |
| EV-012 | bibtex.bib | bibtex.bib | "journal = {Information and Software Technology}, volume = {187}, pages = {107830}" | IST 正式出版信息 | 出版事实确认 | strong | 论文元数据 | 否 | — |

##### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-01 | 本文的维度树是单树、三主干结构（上下文 / 制品可获得性 / 统计建模） | 维度树分类 | [dim-root], [node-ctx], [node-artifact], [node-model] | EV-004, EV-005, EV-006, EV-007 | strong | 直接写入 review.md 的维度树复原 | 正文未呈现逐篇编码表的全部字段；Zenodo 工件可能补充额外叶子 |
| CLM-02 | 样本单位是每篇 secondary study (n=537)，不是 research artifact | 样本单位判定 | [dim-root] | EV-001, EV-002 | strong | SUMMARY 表"样本单位"字段修正 | 无 |
| CLM-03 | 原生维度树不是"六叶通用投影"，review.md 现有 C01–C13 结构需重写 | 审计返修判定 | 全部维度树节点 | EV-004, EV-005, EV-006, EV-007（对比旧版 review.md 的 C01–C13） | strong | C 级返修建议 | 六叶投影在跨论文对齐场景中仍有投影价值，但不能替代本文自身的维度树 |
| CLM-04 | [leaf-availability] 的三个值（Yes/No/By Request）与 [leaf-permanent] 之间存在条件依赖：permanent 仅在 Yes 时适用 | 叶子间关系 | [leaf-availability] → [leaf-permanent] | EV-005（Table 1a 中 Permanent repo 列为 Yes 子集） | strong | Paper2 audit asset 表的条件字段设计 | 无 |
| CLM-05 | 2023 年 artifact availability 升至 62.0%，但这一数字不能迁移到 LLM+状态机领域 | 迁移边界 | [leaf-year] → [leaf-availability] | EV-006 | strong（原文）/ N/A（迁移） | 仅说明迁移边界规则 | SE 领域限定 |
| CLM-06 | 本文可迁移的是 schema 结构（三主干 + 叶子字段定义），不是任何具体百分比 | 迁移边界 | 全部维度树 | EV-005, EV-006, EV-007 | strong | Paper2 方法设计参考 | 所有数值不可迁移 |
| CLM-07 | Zenodo 工件（10.5281/zenodo.15488074）待 A2a 检查，可能补充细粒度叶子 | 证据缺口声明 | [dim-root] 的完整字段集 | EV-011 | moderate | A2a 精核任务入口 | 当前证据仅限于正文 Table 1 |
| CLM-08 | 原文未量化 "no data was used" 的频次，该发现不能作为可统计维度 | 证据强度降级 | [leaf-section] 的质量侧面 | EV-009 | weak | 标记为"原文定性提及，不可统计" | 频次未知 |

---

#### 9. 技能使用与自我审查记录

##### 9.1 已读取的技能文件

| 文件 | 采用原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | "Every major claim must be backed by evidence. If evidence is missing, weaken the claim or mark the gap explicitly." 指导本报告所有降级决策。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | "A reviewer-quality objection should be specific enough that an author can act on it." 指导返修建议按 C/I/M 分级并给出具体重写方向。"Reproducibility: Can results be checked?" 驱动 Zenodo 工件待查标识。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | Claim Audit 规则："Strong claims need direct evidence." 指导将所有 statistical observation 与 candidate finding 分离。 |
| `research-planning/SKILL.md` | "Flag ambiguities explicitly rather than making assumptions." 指导在叶子维度表中区分"原文明确给出的字段"和"我们推断的字段"。 |
| `research-planning/references/planning-prompts.md` | 未直接使用；本文不建议实现，仅审计。 |
| `research-planning/references/output-schemas.md` | 未直接使用；schema 仅供参考。 |
| `autoresearch/SKILL.md` | "Completion is artifact-gated." 指导将 Zenodo 工件标注为 pending evidence。 |

##### 9.2 最高风险 3 点（主线程合并时需复核）

1. **风险 A — Zenodo 工件盲区**：本审计报告基于正文 Table 1 构建维度树。Zenodo 工件（`10.5281/zenodo.15488074`）可能包含更细粒度的编码字段（如 repository provider 具体分类：Zenodo/Figshare/GitHub/Mendeley/personal page 等、paper 级 DOI/标题/作者、额外抽取字段）。若这些字段与正文 Table 1 的聚合统计不同，维度树需调整。**合并复核**：下载 Zenodo 工件并做逐字段比对。

2. **风险 B — Table 1(a) Permanent repo 列分母歧义**：Table 1(a) 中 Permanent repo 列的百分比（如 IST "19 (39.6%)"）以 Yes 列（48）为分母而不是以 Total（194）为分母。这个判定来自数值推导（48 × 0.396 ≈ 19），但未在正文中显式声明。若推导错误，[leaf-permanent] 的取值空间定义需要修正。**合并复核**：PDF 视觉核验或 Zenodo 工件交叉验证。

3. **风险 C — "六叶投影"清理不彻底**：如果 reviewer 在主线程合并时仅简化为"用单树替换六叶"，但没有逐字段重写 A.1/A.2/A.3/A.4，新的维度树定义可能和旧的 A.2 证据账本标识符（C01–C13）形成事实冲突。**合并复核**：确保 A.2 证据账本、A.3 结论映射、A.1 维度树定义三个模块用同一套标识符体系，且全部对齐 Table 1 原文锚点。

##### 9.3 Blocked / Timeout / 文件缺失

- **未 blocked**：所有必需文件（bibtex、metadata、paper_content.txt、review.md、paper.pdf）均成功读取。
- **未 timeout**：所有命令均在合理时间内返回。
- **文件缺失项**：Zenodo 工件（`10.5281/zenodo.15488074`）未下载；这不属于本审计的文件缺失（任务仅要求读取指定本地文件），但属于**证据缺口**，已在 A.2（EV-011）和 §3（缺失部分说明）中标注。
- **技能文件**：全部 7 个技能文件成功读取。

---

**审计完成。** 本报告是自包含的完整审计输出，所有章节均已按 A1-DT v2 口径填充。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md](../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-research-artifacts-secondary-studies-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-research-artifacts-secondary-studies-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-research-artifacts-secondary-studies-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-research-artifacts-secondary-studies-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-research-artifacts-secondary-studies-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-research-artifacts-secondary-studies-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/research-artifacts-secondary-studies__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-research-artifacts-secondary-studies-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/research-artifacts-secondary-studies.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-research-artifacts-secondary-studies-type | clm-research-artifacts-secondary-studies-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：systematic mapping（系统映射）；对象为软件工程 secondary studies 的 research artifact 报告与可获得性 | paper_type | text_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-research-artifacts-secondary-studies-unit | clm-research-artifacts-secondary-studies-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：每篇 secondary study（n = 537） | sample_unit | text_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-research-artifacts-secondary-studies-denom | clm-research-artifacts-secondary-studies-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：537（初始检索 643 → 经 IC1/IC2/IC3 筛选 → 最终纳入 537） | denominator | text_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-research-artifacts-secondary-studies-tree | clm-research-artifacts-secondary-studies-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**单树**（single tree）：三主干（上下文元数据 × 制品可获得性 × 统计建模），每主干下 2–4 个叶子字段。结构简单、紧凑、可完整复原。 | schema | text_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-research-artifacts-secondary-studies-pool | clm-research-artifacts-secondary-studies-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：**是**。本文是一次系统映射研究（systematic mapping），有系统检索、纳排标准、一致性子评估（Krippendorff's Alpha = 0.776）、两轮数据抽取和 logistic regression 建模。537 个样本单位全部可追溯到纳入标准。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 final finding |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-research-artifacts-secondary-studies-type | A1DT-research-artifacts-secondary-studies-C01 | 本文原文类型为：systematic mapping（系统映射）；对象为软件工程 secondary studies 的 research artifact 报告与可获得性 | paper_type | type | ev-research-artifacts-secondary-studies-type | 正式写作前需核对出版页和 PDF 版式 | text_verified | schema_seed / 背景方法样本描述 | 否 | -- |
| clm-research-artifacts-secondary-studies-unit | A1DT-research-artifacts-secondary-studies-C02 | 本文被编码样本单位为：每篇 secondary study（n = 537） | sample_unit | sample_unit | ev-research-artifacts-secondary-studies-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | text_verified | schema_seed / A2a 抽取表设计 | 否 | -- |
| clm-research-artifacts-secondary-studies-tree | A1DT-research-artifacts-secondary-studies-C03 | 本文原生维度树 / 维度森林为：**单树**（single tree）：三主干（上下文元数据 × 制品可获得性 × 统计建模），每主干下 2–4 个叶子字段。结构简单、紧凑、可完整复原。 | tree_type | native_tree | ev-research-artifacts-secondary-studies-tree | 不代表跨论文通用模板 | text_verified | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-research-artifacts-secondary-studies-pool | A1DT-research-artifacts-secondary-studies-C04 | 本文统计池资格为：**是**。本文是一次系统映射研究（systematic mapping），有系统检索、纳排标准、一致性子评估（Krippendorff's Alpha = 0.776）、两轮数据抽取和 logistic regression 建模。537 个样本单位全部可追溯到纳入标准。 | eligibility | statistical_pool | ev-research-artifacts-secondary-studies-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-research-artifacts-secondary-studies-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-research-artifacts-secondary-studies-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-research-artifacts-secondary-studies-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
