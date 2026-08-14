材料已全部读完。下面输出 A1-DT v2 单篇审计报告。

---

# A1-DT v2 单篇审计报告：research-artifacts-secondary-studies

★ Insight ─────────────────────────────────────
- 这是一篇仅 6 页（含参考文献）的 IST 短映射研究，**样本单位非常清晰**（537 篇 secondary study），且其字段抽取空间是一组**封闭、互斥、可统计的离散口径**，与典型 SLR/SMS 的“大 taxonomy 树”不同。
- 现有 `review.md` 把通用六叶接口（scope/corpus/taxonomy/method/evidence/finding）当成本文原文叶子，是 A1-DT v2 明确禁止的反模式；本文真正的原生树是**“secondary study × {availability, persistence, reporting, year/venue covariate}”** 的扁平字段集合，而不是层级 taxonomy。
- 关键陷阱：`dedicated section` 与“真正具备 artifact”不能互推，分母也不同（72/537 vs 50/169），现有 review 已识别此处，但在叶子表中没有把“与上层 availability 节点的非对称包含 / 重叠关系”作为关系边显式编码。
─────────────────────────────────────────────────

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `research-artifacts-secondary-studies` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；全文 358 行通读完毕（含 Table 1 文本化版本）。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两者已交叉核对，DOI 与 venue 一致。 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅以 `paper_content.txt` 中已抽取的 Table 1 文本为准，未做 PDF 视觉版面核验（Table 1 内部小注 `0 (0.4%)` 与样本数 8 看似有印刷误差，需 PDF 复核）。 |
| 原文类型 | systematic mapping study（SMS），明确按 Petersen 等指南执行 |
| 被编码样本单位 | secondary study（SLR / SMS / scoping review / case survey / critical review / meta-analysis / meta-synthesis） |
| 样本数量 / 分母 | 主分母 537；衍生分母 169（提供 artifact 的子集）、79（2023 年度子集） |
| 原生树类型 | **扁平字段表（flat extraction schema）+ 派生统计交叉表**；不是层级 taxonomy；可视为“小型维度森林”（artifact / persistence / reporting / covariate 四簇并列） |
| 主统计池资格 | **是，局部已可统计**：本文字段口径明确、分母明确、Table 1 给出全部交叉统计；只是 *外推到 Paper2 目标领域时* 需作 boundary anchor，不可直接迁移数值。 |
| 总体判定 | **needs repair**：原文证据强、schema 简单清楚，但 `review.md` 把简单清晰的原生 schema 包装成 v1 通用六叶 + schema_seed 降级，**过度降级**且偏离原文。需中度返修。 |

## 1. 原文证据阅读说明

实际读取：

- `bibtex.bib`（10 行）、`metadata.json`（46 行）已通读；
- `paper_content.txt` 全文 358 行通读，包括 Abstract、§1 Introduction（含 4 个 Reason）、§2 Methods（含 search query、IC1--IC3、Krippendorff α）、§3 Results（RQ1--RQ4 + Table 1a/1b/1c）、§4 Limitations、§5 Conclusion and Future work、CRediT、Data availability、References；
- `review.md` 375 行已通读，包括 v1 历史草稿和 v1 通用六叶维度树。

未做 PDF 视觉核验，原因：文本抽取结构良好，Table 1 三个子表数值在文本中已完整呈现。**唯一需要 PDF 视觉核验**的疑似排版异常：Table 1a 中 IST 的 By Request 显示 `8 (0.4%)`（应为 ~4.1% 量级，可能是分子分母分隔失误）和总计行 `16 (3.0%)`。这点 `review.md` §7 已记录为待复核，本审计保留。

5--12 个关键证据锚点：

1. **§Abstract**：明确报告 537 篇、2013--2023、31.5% 有 artifact、2023 年 62.0% 有 artifact、30.4% 使用带 DOI 的永久仓库。
2. **§1 Introduction**：给出 4 个 Reason（Replicability / Trust / Updates / Pathway to Automation），第 4 点把 LLM-driven SR automation 与既有 artifact 链上。
3. **§2.1 Search process**（Page 2）：列出 13 个 SE 期刊 + 2 个 CS 综述期刊的 ISSN 与标题关键词。
4. **§2.2 Study selection**（Page 2）：IC1--IC3、ACM Computing Surveys 与 Computer Science Review 人工裁定、Krippendorff α = 0.776、最终 537 篇。
5. **§2.3 Data extraction**（Page 2）：**两轮抽取（人工全文 + Python 关键词脚本前后 100 字符上下文人工裁定）**——这是本文核心字段抽取协议。
6. **§3 RQ1**（Page 2--3）：169 / 537 = 31.5%。
7. **§3 RQ2 + Table 1**（Page 3）：65 / 169 = 38.5% 在永久仓库；65 / 537 = 12.1% 全样本。
8. **§3 RQ3**（Page 4）：50 / 169 = 29.6% 有专门章节（但 Table 1b 的 Dedicated section 总计为 72 / 537 = 13.4%——分母与口径不同，本文未显式调和）。
9. **§3 RQ4 + Table 1c**（Page 3）：logistic regression，年份每 3 年 OR=2.31，TSE 为参考类别，4 个期刊负向显著（CSR、SPE、JSEP、IST）。
10. **§4 Limitations**（Page 4）：会议被排除、仅用 Scopus、年份窗口 2013--2023。
11. **§5 Conclusion**（Page 4--5）：明确警示 "no data was used" / "upon request" 是 alarming，且即使 2023 年仍有 2/19 非永久仓库链接已死。
12. **§Data availability**（Page 5）：自带 Zenodo DOI `10.5281/zenodo.15488074`（本审计未访问 Zenodo）。

## 2. 样本单位与字段来源判定

1. **原文逐项描述对象**：secondary study（论文级别），不是 primary study、不是 artifact 自身、不是作者、不是工具。
2. **是否系统纳排 / 抽取 / 编码**：是。有完整检索式、IC1--IC3、双人 Krippendorff α、两轮抽取（人工 + 脚本辅助）。属于**完整 SMS**，不是 roadmap / vision / proposal。
3. **字段来源**：字段直接来自 **§2.3 数据抽取协议 + Table 1 字段列表**，没有显式 extraction form template 在正文中展开（细节在 Zenodo 工件），但 Table 1 列名本身就是事实上的 codebook：`Total / Yes / Permanent repo / No / By Request / Dead Link / Dedicated section / Year / Venue`。
4. **RQ 与样本单位的关系**：RQ 不是"树根"，而是**字段统计用途的分组方式**——RQ1 用 availability 字段、RQ2 用 persistence 字段、RQ3 用 reporting 字段、RQ4 用 year+venue 字段做回归。RQ 是结果组织方式，不是 schema。
5. **降级问题**：**不适用**，本文是合格 SMS，主统计池资格可成立；只是对 Paper2 而言不可迁移领域数值。

## 3. 原生样本编码维度树 / 维度森林

本文不是 taxonomy 型 SLR，而是**短字段表 + 派生交叉统计**，因此原生结构最适合表达为**“样本单位 secondary study + 一组并列字段（维度森林）”**：

```text
[unit] secondary study (N=537, 2013–2023, 15 venues)
│
├── 字段簇 F1: 工件可得性 (artifact availability)
│   └── availability_status   ∈ {Yes, No, By Request, Dead Link}        # 闭合 4 态互斥枚举
│
├── 字段簇 F2: 工件持久性 (persistence; 仅在 availability_status=Yes 时有效)
│   ├── permanent_repository  ∈ {Yes, No}                               # 布尔 (Zenodo/Figshare/Mendeley Data 视为 permanent)
│   ├── repository_provider   ∈ {Zenodo, Figshare, Mendeley Data, 其他} # 部分枚举 (正文只点名 3 家 permanent)
│   └── has_DOI               ∈ {Yes, No}                               # 实质上与 permanent_repository 同构
│
├── 字段簇 F3: 报告形式 (reporting form)
│   └── dedicated_data_availability_section ∈ {Yes, No}                 # 注意：分母与 F1 不同, 且 "section 存在 ≠ artifact 存在"
│
└── 字段簇 F4: 协变量 (covariate)
    ├── publication_year   ∈ {2013, …, 2023}                            # 11 离散取值
    └── publication_venue  ∈ {15 个期刊命名实体}                          # 15 离散取值, 部分 <10 在回归中被剔除
```

**派生 / 二次构造**：
- Logistic regression 输入 = `availability_status ∈ {Yes vs others}` 作二值化因变量，年份 + 期刊作自变量。这是 *派生统计字段*，不是原生抽取字段。

**为什么是“维度森林”而非“单根树”**：四个字段簇并列，没有共同的概念根；它们只共享 `secondary study` 这个样本单位。把 F1--F4 强行套上单根（如 `research_artifact_asset`）是 review 重写时可以做的“后视组织”，但**不是本文原生 schema 的结构**。

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1.availability_status | 工件可得性状态 | F1 | §2.3 + Table 1a/1b 列名 | 单篇 secondary study 是否提供外部研究工件 / 链接，及链接的可得性形态 | {Yes, No, By Request, Dead Link} | 完整枚举（4 态互斥，已在 537 上加和=100%） | 本文未单列“unclear”态——所有论文被强制四态划分 | 主因变量；二值化后做 logistic 回归 | 改善趋势、断链 alarming case | Table 1a 总行 169/330/16/22；Page 2 §2.3 | 可迁移枚举本身，不可迁移百分比 |
| F2.permanent_repository | 永久仓库标志 | F2 | §3 RQ2 + Table 1a "Permanent repo" 列 | artifact 是否存于 Zenodo/Figshare/Mendeley Data 等永久仓库 | {Yes, No} | 布尔 | 仅在 F1=Yes 时定义，否则 N/A | 子集统计；与 F1 形成 169 分母 | 持久性 gap finding | Table 1a 65 of 169；Page 4 §RQ2 | "permanent" 定义本文仅枚举 3 家，并非通用 |
| F2.repository_provider | 仓库供应商 | F2 | §2.3 文本 "Figshare, Zenodo or Mendeley" | 实际供应商命名 | {Zenodo, Figshare, Mendeley Data, 其他/未提取} | 部分枚举（开放尾） | 未在正文逐篇列出供应商分布 | 仅作 permanent 判定依据 | 平台生态依赖 finding | §2.3 Page 2 | 不要把"其他"误推断为非永久 |
| F2.has_DOI | DOI 标志 | F2 | Abstract + §3 RQ2 | 是否使用带 DOI 的永久标识 | {Yes, No} | 布尔 | 与 permanent_repository 在本文实证上同构（皆 Zenodo/Figshare/Mendeley Data） | 与 F2.permanent 同口径 | 强调 DOI 而非 URL 的必要性 | §Abstract 2023 数据 30.4%；§5 | DOI ≠ 永久 *逻辑上*，但本文未拆开 |
| F3.dedicated_section | 专门数据可用性章节 | F3 | §3 RQ3 + Table 1b "Dedicated section" 行 | 论文中是否设有名为 "Data Availability" / "Artifact Availability" 等的专门小节 | {Yes, No} | 布尔 | 与 F1 不重叠（72/537 vs 169/537）；section 存在不蕴含 artifact 存在 | 报告实践统计；与 F1 比较暴露 "false transparency" | "section 含 'no data was used' / 'upon request'" 警示 | Page 4 §RQ3；Table 1b；Page 4--5 §5 | Paper2 不可把 "有章节" 等价于 "有 artifact" |
| F4.publication_year | 发表年份 | F4 | Table 1b | 论文正式发表年份 | {2013, …, 2023} | 数值 / 完整枚举 | 无缺失（IC1 强制） | logistic 回归 ordered factor，OR=2.31/3yr | 趋势性 finding | Table 1b/1c；Page 3 | 年份窗口由 Zenodo/Figshare 启用时点驱动，外推需注意 |
| F4.publication_venue | 期刊 | F4 | Table 1a + §2.1 ISSN 清单 | 论文所属期刊 | {15 个期刊命名实体} | 完整枚举（受 ISSN 列表限定） | <10 篇期刊在回归中被排除 | logistic 回归类别变量 | venue 差异 finding | Table 1a；Table 1c | 仅 SE+CS 综述期刊；会议被排除 |

## 5. 关系边表

本文未提供显式 entity-relation schema，但样本单位×字段在统计上隐含若干**字段级约束/包含/比较关系**，应作为关系边显式编码（这些在现有 `review.md` 叶子表中缺失）：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge-subset-permanent-in-yes | F2.permanent_repository | 子集包含（subset_of） | F1.availability_status=Yes | permanent_repository=Yes 蕴含 availability_status=Yes | 若 F1≠Yes 则 F2 视为 N/A | Table 1a "65 of 169" | 防止把 permanent 比例分母错配 |
| edge-disjoint-section-vs-artifact | F3.dedicated_section | 非蕴含 / 部分重叠（non_implication） | F1.availability_status | section=Yes 不蕴含 F1=Yes；分别有 72/537 vs 169/537 | section=Yes & F1=No 可同时出现（"no data was used" 反例） | §RQ3 + §5 (Page 4--5) | 防止 false-transparency；Paper2 关键迁移点 |
| edge-doi-implies-permanent | F2.has_DOI | 实证同构（empirical_equivalence） | F2.permanent_repository | 在本文样本中 DOI=Yes ⇔ permanent=Yes | 本文未单列例外 | §RQ2 + §5 | 提示二者口径可在 Paper2 中拆解 |
| edge-year-predicts-yes | F4.publication_year | 显著正向预测（regression_positive） | F1.availability_status=Yes | OR=2.31 per 3yr，p=5.79e-13 | 受 IC1 时间窗口限制 | Table 1c | 趋势性候选 finding |
| edge-venue-predicts-yes | F4.publication_venue | 类别效应（regression_category） | F1.availability_status=Yes | 4 venue 显著负向（CSR/SPE/JSEP/IST） | <10 篇 venue 被排除 | Table 1c | venue 差异候选 finding |

## 6. 统计观察、候选 finding 与 final finding 边界

**A. 原文统计观察（字段 + Table 1 直接支持）**：

1. 537 篇中 31.5%（169）提供 artifact。
2. 提供 artifact 的子集中 38.5%（65）位于永久仓库，全样本 12.1%。
3. 2023 子集（n=79）中 62.0% 提供 artifact、30.4% 使用永久仓库、58.2% 有专门章节。
4. 年份每+3yr OR=2.31，p<<0.001。
5. CSR、SPE、JSEP、IST 相对 TSE 显著低（OR 0.04--0.37）。
6. 部分非永久仓库链接已在 2023 即失效（19 个非永久链接中 2 个 dead）。

**B. 原文候选 finding / discussion-级**：

1. 强制发布 artifact、强制使用永久仓库 + DOI 应成为期刊政策（§5）。
2. "Data Availability" 章节内容质量令人担忧（"no data" / "upon request" 反例）（§5）。
3. 工件质量评估是未来工作（§5 末段）——本文**未做**质量评估。

**C. 对 Paper2 可迁移的方法学启发**：

1. **availability_status 的 4 态互斥**比单纯 "open/closed" 二元更准确；Paper2 的 run record / 审计制品资产建议同样四态。
2. **section vs artifact 非蕴含**，Paper2 的 reporting checklist 与真实 artifact 必须分别统计。
3. **persistence 单列**：不要把 GitHub 链接等同于永久仓库。
4. **Logistic regression 作为方法学审计统计工具**：Paper2 在做覆盖率随时间 / 模型 / 数据集变化分析时可借鉴。

**D. 不可迁移到 Paper2 的领域结论**：

1. 31.5% / 62.0% / 12.1% 等具体数值仅适用 SE secondary study；不可迁移到 LLM 状态机审计制品场景。
2. CSR/SPE/JSEP/IST 的 venue 效应不可外推。
3. "permanent repository" 在本文 = Zenodo/Figshare/Mendeley Data 三家枚举；Paper2 自有制品场景可能含 GitHub release / arxiv / institutional repo，需重新定义枚举。

## 7. 对现有 `review.md` 的返修建议

### C 级（critical, 阻塞合并）

无。本文证据强度足、`review.md` 主体内容正确；不存在伪造数据或翻倍误读 finding 的硬错误。

### I 级（important, 需在 PR 合并前处理）

1. **I-1：原生维度树被通用六叶接口替代**。`review.md` §叶子维度表（行 239--246）使用 `[leaf-research-artifacts-secondary-studies-scope|corpus|taxonomy|method|evidence|finding]` 六个通用接口节点，这是 A1-DT v2 明确禁止的"把跨论文投影当成原文叶子"。
   - **修法**：把本审计 §3 / §4 的 7 字段（availability_status / permanent_repository / repository_provider / has_DOI / dedicated_section / publication_year / publication_venue）抬升为原生叶子，**通用六叶降级为附录中的"跨论文投影表"**（review 行 291--303 的"通用接口投影"应保留作为投影，不作为主表）。
   - **学术目标影响**：直接关系到 SUMMARY 表能否把本篇标为"样本单位=secondary study / 原生树类型=扁平字段森林 / 主统计池=局部可统计"，影响 survey-of-surveys 的元统计正确性。

2. **I-2：关系边缺失关键的"section ≠ artifact" 非蕴含边**。`review.md` §关系边表（行 312--315）只列了两条通用关系，未编码本文最重要的方法学警示——`dedicated_section=Yes` 与 `availability_status=Yes` 部分重叠但不蕴含。这条边是 Paper2 最值得迁移的"假透明"防御点。
   - **修法**：按本审计 §5 表新增 5 条关系边，至少必须包含 `edge-disjoint-section-vs-artifact`、`edge-subset-permanent-in-yes`、`edge-year-predicts-yes`。

3. **I-3：主统计池资格被过度降级为 schema_seed**。`review.md` §5 / §A.3 中所有 12 条结论强度都标 `weak / schema_seed`，但本文是合格 SMS、字段封闭、分母清楚、Table 1 完整。这是 v1 历史降级，未根据 v2 口径重新评估。
   - **修法**：把本文的 `original_schema_facts`（availability/persistence/reporting 字段值空间、Table 1 数值、回归系数）升级为 `verified` 或 `medium`；只保留"对 Paper2 目标领域的数值外推"标 `weak / boundary_anchor`。SUMMARY 中"统计池资格"列改为 "**是（仅作 boundary anchor，不迁移数值）**"。

### M 级（minor, 可作 follow-up）

4. **M-1**：现有 §A.2 证据账本中所有 EV 编号 `证据强度 = not_verified`，但实际 Table 1 已完整文本化，建议把 EV-002/003 升级为 `text_verified`，PDF 视觉核验仅作 EV-005（Table 1 IST `8 (0.4%)` 排版疑似异常）的待办。

5. **M-2**：现有 §7 待复核第 5 点（Zenodo 工件内部清单）建议明确写入 A2a 任务并在 review 顶部"阅读状态"栏标记"未访问 Zenodo"，避免读者误以为已验证 artifact 内容。

6. **M-3**：v1 历史草稿（行 119--202）已迁移但仍占 review 一半篇幅，建议折叠或迁出到 history 子文件，让事实真源更突出。

### SUMMARY 表对应修正

| 字段 | 当前可能口径 | 建议修正后口径 |
|---|---|---|
| 样本单位 | secondary study artifact / paper | **secondary study (paper-level, N=537)** |
| 样本数量 | -- | **537 / 169 / 79 三层分母** |
| 原生树类型 | schema_seed / 维度树 | **扁平字段森林（4 字段簇并列）** |
| 统计池资格 | 否 / schema seed | **是（仅作 boundary anchor，不迁移数值）** |

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-A1DTv2-RA2S-001 | paper_content.txt | §Abstract | Page 1 line 8--16 | "537 secondary studies … 31.5% include a research artifact … 62.0% … 30.4% use a permanent repository with a DOI" | 主分母 + 主统计观察 | text_verified | F1, F2, F4 全部叶子 | 否 | 数值仅限 SE secondary study |
| EV-A1DTv2-RA2S-002 | paper_content.txt | §2.1 Search process | Page 2 | "13 SE journals + 2 CS review journals … PUBYEAR > 2012 < 2024 … resulting in 643 articles" | 检索协议 + 分母构造 | text_verified | F4.publication_venue, IC1 | 否 | venue 列表封闭 |
| EV-A1DTv2-RA2S-003 | paper_content.txt | §2.2 Study selection | Page 2 | "IC1--IC3 … Krippendorff α 0.776 … 537 secondary studies remained" | 纳排链 + 一致性 | text_verified | F1 unit | 否 | -- |
| EV-A1DTv2-RA2S-004 | paper_content.txt | §2.3 Data extraction | Page 2 | "manually + Python script that prints 100 characters before and after each keyword … permanent repository, such as Figshare, Zenodo or Mendeley" | 字段抽取协议 + permanent 枚举 | text_verified | F1, F2 全部叶子 | 否 | permanent 仅枚举 3 家 |
| EV-A1DTv2-RA2S-005 | paper_content.txt | §3 Table 1a | Page 3 | "Total 537 … Yes 169 (31.5%) … Permanent repo 65 of 169 (38.5%) … No 330 (61.5%) … By Request 16 (3.0%) … Dead Link 22 (4.1%)" | 主统计交叉表 | text_verified（IST 行需 PDF 视觉复核） | F1, F2, F4.venue | 是（仅 IST 行 `8 (0.4%)` 疑似排版异常） | -- |
| EV-A1DTv2-RA2S-006 | paper_content.txt | §3 Table 1b | Page 3 | "Yearly statistics 2013--2023 … Dedicated section 72 (13.4%) … 2023 Yes 49 (62.0%) Permanent 24 (30.4%) Dedicated 46 (58.2%)" | 年度交叉表 | text_verified | F3, F4.year | 否 | -- |
| EV-A1DTv2-RA2S-007 | paper_content.txt | §3 Table 1c | Page 3 | "Year (ordered factor) coef 0.84, OR 2.31, p=5.79e-13 *** … CSR -2.41 0.007** … JSEP -1.61 0.008** … IST -1.00 0.03* … SPE -3.23 0.005**" | 回归模型 | text_verified | edge-year-predicts-yes, edge-venue-predicts-yes | 否 | TSE 为参考类别 |
| EV-A1DTv2-RA2S-008 | paper_content.txt | §3 RQ3 + §5 | Page 4 + Page 4--5 | "50 of 169 (29.6%) include a dedicated section … some papers … simply state that 'no data was used' or … 'available upon request'. Both are alarming" | 非蕴含关系证据 | text_verified | edge-disjoint-section-vs-artifact | 否 | Paper2 关键迁移点 |
| EV-A1DTv2-RA2S-009 | paper_content.txt | §4 Limitations | Page 4 | "excluded conference proceedings … Scopus only … 2013--2023 to ensure Zenodo / Figshare fully included" | 外推边界 | text_verified | 全树 root | 否 | -- |
| EV-A1DTv2-RA2S-010 | paper_content.txt + bibtex.bib | §Data availability + bibtex | Page 5 + bibtex | "data … in Zenodo (10.5281/zenodo.15488074)" | 本文自有 artifact | text_verified（未访问 Zenodo 内部清单） | F2.has_DOI 本文自示例 | 否 | Zenodo 工件内容未核验 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-A1DTv2-RA2S-T01 | 本文原生树是"secondary study × {availability(4 态), persistence(布尔+供应商), reporting(布尔), year+venue 协变量}" 的扁平字段森林，不是层级 taxonomy；可作 Paper2 审计制品资产字段表的 schema seed。 | tree_type | 全树 | EV-001, 004, 005 | medium | review SUMMARY 表"原生树类型"列；Paper2 §Methods 字段表设计 | 仅本文样本；persistence 供应商枚举仅 3 家 |
| CLM-A1DTv2-RA2S-T02 | availability_status 的 4 态互斥（Yes/No/By Request/Dead Link）已在 537 上加和=100%，是封闭枚举。 | leaf_definition | F1.availability_status | EV-005 | verified | Paper2 直接复用 4 态 | -- |
| CLM-A1DTv2-RA2S-T03 | dedicated_section 与 availability_status=Yes 在本文样本中**非蕴含**：72/537 vs 169/537，且作者明确警示 "Data Availability" 章节可能写 "no data was used" / "upon request"。 | relation_edge | edge-disjoint-section-vs-artifact | EV-006, 008 | verified | Paper2 §Methods 必须分别统计 reporting 和 real artifact；§Discussion 引述本文警示 | 仅本文样本；外推到非 SE 领域可能强度更弱 |
| CLM-A1DTv2-RA2S-T04 | permanent_repository ⊂ availability_status=Yes；在本文中 has_DOI 与 permanent_repository 实证同构（均为 Zenodo/Figshare/Mendeley Data）。 | relation_edge | edge-subset-permanent-in-yes, edge-doi-implies-permanent | EV-004, 005 | medium | Paper2 §Methods 拆解 DOI / 永久仓库为两个独立字段 | 实证同构非逻辑等价 |
| CLM-A1DTv2-RA2S-T05 | 年份对 availability_status=Yes 是显著正向预测因子（OR=2.31/3yr，p<<0.001）；4 个期刊（CSR/SPE/JSEP/IST）相对 TSE 显著负向。 | statistical_observation | edge-year-predicts-yes, edge-venue-predicts-yes | EV-007 | verified | review §统计观察；不作 Paper2 数值迁移 | <10 篇 venue 已排除；TSE 为参考类别 |
| CLM-A1DTv2-RA2S-T06 | 本文主统计池资格：**是（局部）**——字段封闭、分母清楚、Table 1 完整可文本化复验。但对 Paper2 目标领域（LLM 状态机审计制品）仅作 boundary anchor，不迁移数值。 | pool_eligibility | 全树 | EV-001, 003, 005 | medium | SUMMARY 表"统计池资格"列 | -- |
| CLM-A1DTv2-RA2S-T07 | 本文未评估 artifact 内容质量（作者明确标记为 future work）；Paper2 若要利用 audit-asset 类比，必须自建质量字段。 | gap_for_paper2 | -- | EV-001 末段, §5 末段 | medium | Paper2 §Related Work 引用本文 + 明确差异 | -- |
| CLM-A1DTv2-RA2S-T08 | 外推限制：会议被排除、仅 Scopus、2013--2023 窗口。 | migration_boundary | 全树 root | EV-009 | verified | Paper2 §Threats to validity 类比 | -- |

## 9. 技能使用与自我审查记录

**采用的技能原则**：

- 来自 `ai-research-writing-skill/references/reviewer-guidelines.md`：使用 5 维评审视角（contribution/clarity/experimental strength/evaluation completeness/method soundness/responsibility）。本审计在 §6/§7 中明确把"原文统计观察"与"对 Paper2 的迁移"分离，避免混层；C/I/M 分级遵循"specificity standard"（每个 I 都给出具体行号 + 修法 + 影响）。
- 来自 `reviewer-self-review.md` 的"Adversarial Questions"：审视本文是否过度迁移、是否把 reporting 等同于 artifact、是否把 RQ 当 schema 根——这三个红线本审计 §6/§7 均已处理。
- 来自 `research-planning/SKILL.md`：把样本单位、字段、关系、统计用途、迁移边界分层组织，对应 Paper2Code 的 overall→architecture→logic→config 思维。
- 来自 `autoresearch/SKILL.md`：明确本审计是 *artifact-gated* 输出（本报告即 completion artifact），不靠"看起来差不多"判定完成。

**本输出最高风险三点（reviewer 视角合并时复核要点）**：

1. **风险 1（高）**：Table 1a 中 IST 行 `By Request 8 (0.4%)` 数字与百分比明显不一致——本审计文本化时直接采用 `paper_content.txt` 行 146 的内容，**未访问 PDF 视觉核对**。合并前 reviewer 应打开 `paper.pdf` 第 3 页 Table 1a 复核该单元格；若 PDF 视觉版本数字不同，A.2 EV-005 的 `text_verified` 应降级，且 §统计观察 中 IST 的 By Request 比例需修正。
2. **风险 2（中）**：本审计把"主统计池资格"从现有 `review.md` 的 schema_seed 升级为 "是（局部）"。这是对现有 review 的实质改判，合并前 reviewer 应检查整个 survey-of-surveys 的 SUMMARY 总账：如果总账目前依据"所有 v1 单篇都 schema_seed"做统计基线，本篇单独升级会造成口径不对称。建议合并 PR 时同步审视 SUMMARY 的口径定义而不是只改单篇。
3. **风险 3（中）**：本文是 6 页短文，Zenodo 工件未访问。若 reviewer 关心"comprehensive list of artifacts"（摘要承诺），本审计未做核实——A.2 EV-010 明确标记"未访问 Zenodo"。Paper2 若要把本文作为 baseline，必须先访问 Zenodo 工件确认字段是否真有逐篇 codebook，否则 boundary anchor 强度不足。

**Blocked / timeout / 文件缺失**：

- 无 blocked。
- 7 个技能 / 指南文件均成功读取（`ai-research-writing-skill/SKILL.md`、`reviewer-guidelines.md`、`reviewer-self-review.md`、`research-planning/SKILL.md`、`planning-prompts.md`、`autoresearch/SKILL.md`）；唯一未通读的是 `research-planning/references/output-schemas.md`（仅扫了文件存在与长度），因其在本任务中作用为 schema 结构启发而非硬合同，已用 planning-prompts.md 的 Paper2Code 4 阶段框架替代。这一裁剪不影响 A1-DT v2 口径正确性。
- `paper.pdf` 未做视觉核验（已声明，且仅影响 EV-005 的 IST 单行排版疑问）。
- 未访问外部 Zenodo DOI（已声明，EV-010 标记）。

---

**报告结束。** 本报告为单篇 A1-DT v2 审计的完整 artifact，无任何"见上文"引用；所有事实陈述均锚定 `paper_content.txt` 行号或 Table 1 子表，所有结论判定均按 §A.3 表给出强度与允许用途。
