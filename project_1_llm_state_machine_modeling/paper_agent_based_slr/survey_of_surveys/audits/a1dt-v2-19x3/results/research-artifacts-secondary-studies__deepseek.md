所有文件已读取完毕。现在我拥有完整的论文内容、元数据和现有审查报告。让我基于详细的文本分析和 PDF 版面核验来构建审计报告。

---

# A1-DT v2 单篇全文审计报告

## 论文：`research-artifacts-secondary-studies`

---

### 0. 审计结论卡片

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
| 总体判定 | **needs repair**—现有 `review.md` 的维度树被覆盖了一层跨论文通用六叶投影（A1DT-research-artifacts-secondary-studies-C01 至 C13），导致原文真实编码 schema 被架空。需要重写维度树复原章节，用本文自己的三主干单树替换。 |

---

### 1. 原文证据阅读说明

#### 1.1 实际读取文件清单

| 文件 | 读取方式 | 读取范围 |
|---|---|---|
| `paper_content.txt` | 全文通读（358 行） | Abstract → Introduction → Methods (§2.1–2.3) → Results (§3, RQ1–RQ4) → Limitations (§4) → Conclusion (§5) → References [1]–[10] |
| `bibtex.bib` | 全文读取 | 完整 BibTeX entry |
| `metadata.json` | 全文读取 | 所有字段（含 eligibility meta） |
| `review.md` | 全文读取（375 行） | 快速结论卡片 → 论文内容详读 → A.1–A.4 |
| `paper.pdf` | `pdftotext -layout -f 1 -l 6` 逐页提取 | 完整 6 页；特别核验 Table 1(a)/(b)/(c) 行列值 |

#### 1.2 PDF 版面核验状态

PDF 共 6 页。已通过 `pdftotext -layout` 核对以下内容与 `paper_content.txt` 一致性：
- Table 1(a)：15 个期刊 × 6 列（Total / Yes / Permanent repo / No / By Request / Dead Link）—数值完整核验
- Table 1(b)：11 年 × 7 行（Yes / No / By req. / Dead / Permanent repo / Dedicated section / Total）—数值完整核验
- Table 1(c)：logistic regression 系数、标准误、z-value、p-value、odds ratio —完整核验

**仍需 PDF 视觉截图核验**：论文仅 6 页，没有复杂彩色图表；但 Table 1(a) 中 Permanent repo 列的百分比计算基准（是 Yes 的子集还是 Total 的子集）和 Dead Link 的合计逻辑（22 of 537 = 4.1%，但行内百分比不同）值得视觉确认；建议 A2a 做一次 PDF 页面截图人工核验。

#### 1.3 12 个关键原文证据锚点

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

### 2. 样本单位与字段来源判定

#### 2.1 原文纳入和逐项描述的对象是什么？

**每篇已发表的软件工程 secondary study**（系统综述/系统映射/meta-analysis/scoping review 等），发表于 2013–2023 年间，源自 15 个期刊（13 个 SE 相关 + 2 个更广义 CS 综述期刊）。纳入后共 537 篇。

每篇 secondary study 被编码的**不是其研究内容本身**（不涉及 SE 子领域、方法学、RQ 等），而是其**研究工件的可获得性与报告方式**。

#### 2.2 作者有没有系统检索/纳排/数据抽取/编码方案？

有，且较为完整：

1. **检索**：Scopus 单一数据库；ISSN 限定 15 个期刊；标题关键词限定 review/mapping/meta-analysis 等 9 个术语；年份限定 2013–2023（因为 Zenodo 2013 年上线、Figshare 2011 年上线）。初始 643 篇。
2. **纳排**：IC1（年份）、IC2（是否为 secondary study）、IC3（是否 SE 相关）。title-abstract screening + 人工判定（对 ACM Computing Surveys 和 Computer Science Review 非纯 SE 期刊）。
3. **质量/一致性子评估**：Krippendorff's Alpha = 0.776，正文标注为强一致。
4. **数据抽取**：两轮——Round 1 人工全文筛查 dedicated artifact availability section；Round 2 自动化 Python keyword search + 100 字符上下文人工核验。
5. **编码方案**：检查每篇是否引用外部 research artifact、是否在永久仓库存放、是否有 DOI。

#### 2.3 原文字段来自哪里？

字段直接来自**数据抽取方案**（§2.3）和 **Table 1 统计表**：
- **artifact_availability**：Yes / No / By Request（§2.3 描述 + Table 1(a) 列）
- **permanent_repository**：Permanent repo 列（Table 1(a)）——"if it is located in a permanent repository, such as Figshare, Zenodo or Mendeley"（§2.3）
- **dedicated_section**：Dedicated section 行（Table 1(b)）——"dedicated sections indicating the availability of research artifacts"（§2.3）
- **link_health**：Dead Link 列（Table 1(a)）
- **year**：Table 1(b) 列（2013–2023）
- **venue**：Table 1(a) 行（15 个期刊）
- **regression_odds**：Table 1(c) logistic regression 模型输出

**完整逐篇原始编码数据**存储于 Zenodo 工件（DOI: `10.5281/zenodo.15488074`），不在正文内，正文仅呈现聚合统计表。目前 A1-DT 审计**未访问该 Zenodo 工件**——这是一个重要的证据缺口。

#### 2.4 RQ 与样本单位是什么关系？

RQ 是**结果组织方式**，不是树根也不是字段本身：

- RQ1（有多少篇有 artifact）→ 使用字段 `artifact_availability`
- RQ2（存放在哪）→ 使用字段 `permanent_repository`
- RQ3（如何报告）→ 使用字段 `dedicated_section` + 定性发现（"no data used" / "upon request"）
- RQ4（年份/venue 影响）→ 使用字段 `year` × `venue` × `artifact_availability`，输出 logistic regression model

RQ 是一组**围绕"制品可获得性"单一主题的问题**，它们共享同一个样本池（537 篇），使用同一套数据抽取字段的不同子集。

#### 2.5 是否有降级必要？

**不需要降级**。本文是完整的 systematic mapping study，具有系统样本库、明确纳排标准、一致性子评估和统计建模。完全满足主统计池资格。

---

### 3. 原生样本编码维度树/维度森林

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

### 4. 叶子维度表

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

### 5. 关系边表

本论文的编码 schema 是扁平单表结构（flat single-table），每个样本单位为一行，字段之间没有在原文中显式建模的关系边（没有外键、一对多、多对多等关系型结构）。

但是，论文中有以下**统计关系**值得记录为隐式关系边（可作为 Paper2 方法的 schema seed）：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `[edge-year-availability]` | `[leaf-year]` | 时间趋势（logistic regression predictor） | `[leaf-availability]` | Yes/No/By Request | N/A | Table 1(b)/(c)：year 为 ordered factor，odds ratio = 2.31 per 3 years | Paper2 方法学参考：可在自己的 survey-of-surveys 中对"制品可获得性是否随时间改善"做类似建模 |
| `[edge-venue-availability]` | `[leaf-venue]` | 期刊效应（logistic regression predictor） | `[leaf-availability]` | Yes/No/By Request | N/A | Table 1(c)：各期刊 vs reference (IEEE TSE) 的 odds ratio | Paper2 方法学参考：vennue 层面制品报告规范的差异分析 |
| `[edge-availability-permanent]` | `[leaf-availability]` | 条件子字段（conditional sub-field） | `[leaf-permanent]` | Yes/No | 条件不可见（仅当 availability = Yes） | Table 1(a) Permanent repo 列为 Yes 子集 | schema seed：条件字段在 Paper2 的审计资产表中是常见模式 |

**未发现显式关系边**：原文没有在样本单位之间建立引用、依赖或层级关系；也不存在跨表外键、nested hierarchy 或 graph 结构。这是一个经典的横截面统计设计（cross-sectional mapping），不是关系型/网络型研究。若 Paper2 的 coding schema 需要样本间关系边，必须从其他论文引入，不能从此文导出。

---

### 6. 统计观察、候选 finding 与 final finding 边界

#### 6.1 原文中由字段/统计表支持的统计观察

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

#### 6.2 原文 discussion/recommendation 提出的候选 finding

以下来自 §4 Limitations 和 §5 Conclusion and Future work：

| 候选 finding | 类型 | 证据支持状态 |
|---|---|---|
| "both 'no data was used' and 'available upon request' are alarming for secondary studies" | 方法学批评（methodological critique） | moderate：基于观察事实（16 篇 "upon request"），但未量化 "no data was used" 的频次 |
| "journals should enforce the reporting practices of research artifacts" | 政策建议（policy recommendation） | weak：作者主张，非实验证据 |
| "identifying which research artifacts have sufficient quality is an important future study area" | 未来研究方向（future work direction） | weak：方向性建议 |
| "links to non-permanent repositories can become inaccessible"（2023 年仍有 2/19 dead） | 经验观察（empirical observation） | moderate：基于 2023 年 19 个链接中 2 个失效的观察，但样本量小 |

#### 6.3 对 Paper2 可迁移的方法学启发

| 启发 | 迁移方式 |
|---|---|
| 将"artifact availability"操作化为多值分类（Yes / No / By Request），而非简单二分 | Paper2 审计资产表的 `availability_status` 字段可参考 |
| 区分 permanent repository（带 DOI）与 non-permanent（personal/institutional page/GitHub 无 DOI），并记录 dead link | Paper2 资产表的 `storage_type` 和 `link_health` 字段 |
| 检查纳入论文是否包含 dedicated data availability section | Paper2 可作为 review 质量的一个代理指标 |
| logistic regression 作为跨论文趋势/venue 分析的方法 | Paper2 方法学参考 |
| 报告逐篇原始数据（Zenodo 工件）并声明 FAIR 数据原则 | Paper2 应遵循相同实践 |

#### 6.4 绝不能迁移的领域结论

本文是 **software engineering secondary studies** 的领域特定研究，以下内容绝不能直接迁移到 Paper2（LLM + 状态机形式化建模领域）：

- **任何具体百分比**（31.5%、62.0%、30.4%、38.5%、12.1% 等）——这些是 SE 领域的统计值
- **logistic regression 的具体系数和 odds ratio**
- **"SE community is improving" 的时间趋势陈述**
- **对特定 SE 期刊（IST、JSS、TSE 等）的 venue 级发现**
- **对 Scopus 检索和 ISSN 检索策略的方法学偏好**

可迁移的仅是**维度树结构**（三主干：上下文 / 可获得性 / 统计建模）、**字段定义模式**和**方法学设计**。

---

### 7. 对现有 `review.md` 的返修建议

#### 7.1 问题诊断

现有 `review.md` 的核心问题是**维度树被跨论文通用六叶投影覆盖，原文真实编码 schema 被架空**：

1. **"范围"叶**（A1DT-research-artifacts-secondary-studies-C01）：将原文的样本单位、纳排标准和检索策略提炼为"范围"是合理的，但把 15 个期刊、ISSN 检索、IC1–IC3 全部收入一个叶子过于宽泛。原文实际上有独立的 `[leaf-year]`、`[leaf-venue]` 和 `[leaf-availability]`（含纳排过滤），它们不是"范围"的子树，而是**编码维度本身**。

2. **"语料"叶**（A1DT-research-artifacts-secondary-studies-C02）：将 537 篇 secondary studies 作为"语料"描述主体，但原文不区分"语料"和"样本"——537 篇就是样本，没有外部语料概念。这是把 NLP/DL 论文的"语料"概念强行套用到 systematic mapping 上。

3. **"分类"叶**（A1DT-research-artifacts-secondary-studies-C03）：把 artifact availability 的 Yes/No/By Request 和 permanent repository 归为"分类"是合理的覆盖，但缺失了 dedicated section、link health 和 regression output。

4. **"方法"叶**（A1DT-research-artifacts-secondary-studies-C04）：原文的方法是 systematic mapping + logistic regression，但方法本身不是"维度树"的叶子——它是生产维度树的**过程**。在维度树中混入方法节点会混淆"样本被编码成什么"和"样本怎么被编码"。

5. **"证据"叶**（A1DT-research-artifacts-secondary-studies-C05）：原文的所有叶子字段都可支撑统计观察，不存在独立的"证据"叶子。

6. **"发现"叶**（A1DT-research-artifacts-secondary-studies-C07）：原文的讨论结论是"候选 finding"，不是维度树的编码维度。

7. **A.1–A.4 结构**：现有 A.1/A.2/A.3/A.4 使用了大量跨论文的抽象标识符（`A1DT-research-artifacts-secondary-studies-C01` 至 `C13`），这些标识符把原文事实封装在了跨论文投影的语言中，导致"样本编码 schema"不可直接阅读。

#### 7.2 按 C/I/M 分级的返修建议

##### C（Critical，阻塞级）

| # | 问题 | 建议 |
|---|---|---|
| C1 | 维度树仍然是六叶通用投影，不是原文真实编码 schema | 用本报告 §3 的三主干单树重写"维度树复原"章节。删除六叶通用接口节点。维度树应描述：root = Secondary Study (n=537) → 三主干（上下文 / 制品可获得性 / 统计建模）→ 每个主干的叶子字段。 |
| C2 | A.1--A.4 使用了跨论文抽象标识符，原文事实被封装在投影语言中 | A.1 维度树定义应从跨论文投影标识符（C01–C13）中解耦，用原文术语和原文表编号重构。A.2 证据账本应与 Table 1(a)/(b)/(c) 的行列锚点对齐。 |
| C3 | SUMMARY 表中"样本单位/样本数量/原生树类型/统计池资格"需要修正 | 样本单位 = 每篇 secondary study（非"研究工件"）；原生树类型 = 单树（非维度森林）；统计池资格 = 是（非局部可统计）。当前 review.md 中若已有 SUMMARY 表，需同步更新。 |

##### I（Important，重要级）

| # | 问题 | 建议 |
|---|---|---|
| I1 | review.md 未提及 Table 1(a) 中 Permanent repo 列的百分比计算基准差异 | 补充说明：Permanent repo 列以 `has_research_artifact = Yes`（169）为分母，不是以 Total（537）为分母。该差异影响 Paper2 字段的取值空间类型判定。 |
| I2 | review.md 未区分"原文统计观察"与"候选 finding" | 增加一节明确列出：哪些是直接来自 Table 1 的统计事实（strong evidence），哪些是 discussion/recommendation 的候选 finding（weak/moderate）。 |
| I3 | review.md 提到 "no data was used" 但未给出频次 | 原文本身也**未给出 "no data was used" 的频次**（仅提及为 qualitative observation）。review.md 应注明此为原文中的定性提及，非可统计字段。 |
| I4 | Zenodo 工件未检查 | A.4 应新增一项：check Zenodo artifact (`10.5281/zenodo.15488074`) 获取逐篇原始编码表，补充可能被正文省略的细粒度字段（repository provider 分类、paper title/DOI/author metadata 等）。标记为 A2a 精核任务。 |

##### M（Minor，建议级）

| # | 问题 | 建议 |
|---|---|---|
| M1 | review.md 中 "A1 角色" 一栏写的"审计制品链 / 可复现证据资产"偏笼统 | 精化为："A1 角色：为 Paper2 的 artifact availability schema 提供三字段锚点（has_artifact × permanent_repo × dedicated_section），尤其是条件字段设计（permanent_repo 仅在 has_artifact=Yes 时有效）和 link health 跟踪模式。" |
| M2 | review.md 引用 arXiv v3 / 2026-04-16 但出版日期为 2025-07-07 | 在版本号处加注：正式出版（IST vol 187 / 2025-11）与开放预印本（arXiv v3 / 2026-04-16）的版本差异，避免读者混淆 |
| M3 | 缺少明确的"非目标证据池"声明 | 已在 review.md 第 1 节注明"是否目标证据池 = 否"，但可加强为："本文是 SE 领域的方法学映射研究，所有统计数字不能迁移到 LLM+状态机领域，仅 schema 结构可迁移。" |

---

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

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

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-01 | 本文的维度树是单树、三主干结构（上下文 / 制品可获得性 / 统计建模） | 维度树分类 | [dim-root], [node-ctx], [node-artifact], [node-model] | EV-004, EV-005, EV-006, EV-007 | strong | 直接写入 review.md 的维度树复原 | 正文未呈现逐篇编码表的全部字段；Zenodo 工件可能补充额外叶子 |
| CLM-02 | 样本单位是每篇 secondary study (n=537)，不是 research artifact | 样本单位判定 | [dim-root] | EV-001, EV-002 | strong | SUMMARY 表"样本单位"字段修正 | 无 |
| CLM-03 | 原生维度树不是"六叶通用投影"，review.md 现有 C01–C13 结构需重写 | 审计返修判定 | 全部维度树节点 | EV-004, EV-005, EV-006, EV-007（对比现有 review.md 的 C01–C13） | strong | C 级返修建议 | 六叶投影在跨论文对齐场景中仍有投影价值，但不能替代本文自身的维度树 |
| CLM-04 | [leaf-availability] 的三个值（Yes/No/By Request）与 [leaf-permanent] 之间存在条件依赖：permanent 仅在 Yes 时适用 | 叶子间关系 | [leaf-availability] → [leaf-permanent] | EV-005（Table 1a 中 Permanent repo 列为 Yes 子集） | strong | Paper2 audit asset 表的条件字段设计 | 无 |
| CLM-05 | 2023 年 artifact availability 升至 62.0%，但这一数字不能迁移到 LLM+状态机领域 | 迁移边界 | [leaf-year] → [leaf-availability] | EV-006 | strong（原文）/ N/A（迁移） | 仅说明迁移边界规则 | SE 领域限定 |
| CLM-06 | 本文可迁移的是 schema 结构（三主干 + 叶子字段定义），不是任何具体百分比 | 迁移边界 | 全部维度树 | EV-005, EV-006, EV-007 | strong | Paper2 方法设计参考 | 所有数值不可迁移 |
| CLM-07 | Zenodo 工件（10.5281/zenodo.15488074）待 A2a 检查，可能补充细粒度叶子 | 证据缺口声明 | [dim-root] 的完整字段集 | EV-011 | moderate | A2a 精核任务入口 | 当前证据仅限于正文 Table 1 |
| CLM-08 | 原文未量化 "no data was used" 的频次，该发现不能作为可统计维度 | 证据强度降级 | [leaf-section] 的质量侧面 | EV-009 | weak | 标记为"原文定性提及，不可统计" | 频次未知 |

---

### 9. 技能使用与自我审查记录

#### 9.1 已读取的技能文件

| 文件 | 采用原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | "Every major claim must be backed by evidence. If evidence is missing, weaken the claim or mark the gap explicitly." 指导本报告所有降级决策。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | "A reviewer-quality objection should be specific enough that an author can act on it." 指导返修建议按 C/I/M 分级并给出具体重写方向。"Reproducibility: Can results be checked?" 驱动 Zenodo 工件待查标识。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | Claim Audit 规则："Strong claims need direct evidence." 指导将所有 statistical observation 与 candidate finding 分离。 |
| `research-planning/SKILL.md` | "Flag ambiguities explicitly rather than making assumptions." 指导在叶子维度表中区分"原文明确给出的字段"和"我们推断的字段"。 |
| `research-planning/references/planning-prompts.md` | 未直接使用；本文不建议实现，仅审计。 |
| `research-planning/references/output-schemas.md` | 未直接使用；schema 仅供参考。 |
| `autoresearch/SKILL.md` | "Completion is artifact-gated." 指导将 Zenodo 工件标注为 pending evidence。 |

#### 9.2 最高风险 3 点（主线程合并时需复核）

1. **风险 A — Zenodo 工件盲区**：本审计报告基于正文 Table 1 构建维度树。Zenodo 工件（`10.5281/zenodo.15488074`）可能包含更细粒度的编码字段（如 repository provider 具体分类：Zenodo/Figshare/GitHub/Mendeley/personal page 等、paper 级 DOI/标题/作者、额外抽取字段）。若这些字段与正文 Table 1 的聚合统计不同，维度树需调整。**合并复核**：下载 Zenodo 工件并做逐字段比对。

2. **风险 B — Table 1(a) Permanent repo 列分母歧义**：Table 1(a) 中 Permanent repo 列的百分比（如 IST "19 (39.6%)"）以 Yes 列（48）为分母而不是以 Total（194）为分母。这个判定来自数值推导（48 × 0.396 ≈ 19），但未在正文中显式声明。若推导错误，[leaf-permanent] 的取值空间定义需要修正。**合并复核**：PDF 视觉核验或 Zenodo 工件交叉验证。

3. **风险 C — "六叶投影"清理不彻底**：如果 reviewer 在主线程合并时仅简化为"用单树替换六叶"，但没有逐字段重写 A.1/A.2/A.3/A.4，新的维度树定义可能和旧的 A.2 证据账本标识符（C01–C13）形成事实冲突。**合并复核**：确保 A.2 证据账本、A.3 结论映射、A.1 维度树定义三个模块用同一套标识符体系，且全部对齐 Table 1 原文锚点。

#### 9.3 Blocked / Timeout / 文件缺失

- **未 blocked**：所有必需文件（bibtex、metadata、paper_content.txt、review.md、paper.pdf）均成功读取。
- **未 timeout**：所有命令均在合理时间内返回。
- **文件缺失项**：Zenodo 工件（`10.5281/zenodo.15488074`）未下载；这不属于本审计的文件缺失（任务仅要求读取指定本地文件），但属于**证据缺口**，已在 A.2（EV-011）和 §3（缺失部分说明）中标注。
- **技能文件**：全部 7 个技能文件成功读取。

---

**审计完成。** 本报告是自包含的完整审计输出，所有章节均已按 A1-DT v2 口径填充。