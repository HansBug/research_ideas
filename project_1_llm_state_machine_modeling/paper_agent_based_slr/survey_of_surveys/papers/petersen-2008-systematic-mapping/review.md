# Systematic Mapping Studies in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic Mapping Studies in Software Engineering |
| 作者 | Kai Petersen; Robert Feldt; Shahid Mujtaba; Michael Mattsson |
| 年份 | 2008 |
| 类型 | SMS 方法论文；包含 系统映射 process、分类维度构造、map/review 对照和 guideline 扩展建议。 |
| 出版形态 | 会议 |
| 期刊/会议/预印本 | [EASE](https://conf.researchr.org/series/ease) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | C |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | EASE 2008 / BCS Electronic Workshops in Computing；DOI 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 10 页；未做图表视觉级人工核对。 |
| 证据等级 | 全文文本级；图表 / 表格布局待 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.14236/ewic/EASE2008.8> |
| 综述类型 | SMS 方法论文 / 系统映射 方法学 seed。 |
| SE 子领域 | 软件工程 系统映射 方法学。 |
| A1 角色 | 从失败路径升级为全文级方法学种子：提供 SMS 流程、keywording、三维分类 facet、频数 / bubble plot 呈现、map 与 review 的互补边界。 |
| 是否目标证据池 | 否；只作为 `survey_of_surveys/` 的方法学 模式种子，不作为某个 SE 主题领域事实。 |
| 是否统计池 | 不进入普通 SLR/SMS 领域统计池；其内部频数和 map/review 对照只可作为方法学描述性统计 seed。 |
| 一句话结论 | 这篇论文最适合支撑 Paper2 的“维度模式会随阅读演化、字段值要有 rationale、统计观察主要来自类别频数和交叉覆盖”的方法故事。 |

## 2. 论文内容详读

### 2.1 论文定位与目标

本文的目标不是回答某个具体技术是否有效，而是把 系统映射 引入软件工程，说明其流程、产物和与 systematic review 的区别。作者在摘要和 §2.1 中把 mapping 的主要目标定义为：为研究领域提供概览、识别研究数量与类型、观察时间趋势、识别发表论坛，并用这些信息暴露研究空白。

对 Paper2 来说，这篇论文是“先构造领域地图，再决定是否需要深度证据合成”的方法学母文。它支持导师讨论中的判断：SLR / SMS 不是机械整理，真正关键是由研究者设定 scope 与维度，再用论文阅读持续修正维度模式。

### 2.2 系统映射 流程

作者给出五步流程：

1. 定义研究问题 / 研究范围。
2. 检索 原始研究。
3. 按纳排标准筛选相关论文。
4. 对摘要做 keywording，形成分类方案。
5. 抽取数据并映射成 systematic map。

其中对 A1 最关键的是 §2.4--§2.5：分类方案不是预先一次性冻结，而是在读摘要、聚类关键词、排序论文时形成；如果摘要质量不足，可继续看引言或结论；在数据抽取过程中还可以新增、合并或拆分类别。作者还要求在抽取表中记录每篇论文为什么被放入某个类别的短理由，这与 Paper2 的字段级证据链高度一致。

### 2.3 搜索与纳排

本文对搜索与纳排的启发主要是“广覆盖优先于过早深挖”。作者指出，如果目标是 mapping，则搜索串不宜被特定实验设计或特定 outcome 过度限制，否则容易导致地图不完整。纳排标准要由 RQ 驱动，例如排除只在摘要开头泛泛提到关键词、但正文贡献并不相关的论文。

这对 A1/A2a 的含义是：构建综述之综述文库时，不能只收高等级、方法最完整的 SLR；还要保留 SMS、guideline、roadmap、失败路径和边界样本，用来校准字段取值空间和降级规则。

### 2.4 分类维度与字段模式

本文最可迁移的是三类 facet：

1. **主题 facet**：按领域对象划分，例如 variability 的不同子主题。
2. **贡献 facet**：按论文贡献形态划分，例如 process、method、model、tool。
3. **研究类型 facet**：采用 Wieringa 等提出的研究类型，如 validation research、evaluation research、solution proposal、philosophical paper、opinion paper、experience paper。

这说明 Paper2 后续的维度模式应是树状 / 分层的，而不是只列一张扁平字段表。一个目标主题可以有 topic axis、artifact axis、method axis、research-type axis、evaluation axis；其中部分轴来自领域，部分轴来自通用 SE research methodology。

### 2.5 证据呈现与统计分析

本文强调 systematic map 的分析重心是类别频数和类别交叉。作者使用 summary statistics、frequency table 和 bubble plot 展示论文在不同 facet 组合下的分布。bubble plot 的价值在于同时展示多个 facet 的交叉覆盖，让研究空白以“某类主题 / 研究类型组合论文很少”的方式显现。

这对 Paper2 的启发是：统计分析不等于最终 research finding。统计分析先产生 coverage / density / gap / imbalance 这类观察；随后才由研究者判断这些观察是否构成可写入论文的发现、是否需要反证、是否只适用于某一 scope。

### 2.6 map 与 review 的互补边界

作者比较 systematic maps 和 systematic reviews 后指出，二者目标不同：mapping 更关注分类、主题覆盖和发表论坛；review 更关注证据状态、方法效果和更深入的叙述解释。两者都可以识别研究空白，但空白类型不同：map 看到的是类别覆盖不足，review 看到的是证据不足或报告不足。

这给 A1/A2a 一个重要边界：`survey_of_surveys/` 中的 SMS / guideline 可以为维度模式、统计观察和可视化方式提供先验，但不能替代针对目标主题的深度证据审查。

### 2.7 效度与限制

本文没有独立的传统 threats 章节，但在比较和 guideline 讨论中反复提到：摘要可能不足以支持分类；术语使用不稳定；过窄纳排会损害 breadth；过细分类会放大判断错误；mapping 通常不做与 systematic review 同等深度的质量评价。作者提出的缓解方式包括自适应阅读深度、使用较高层级分类、保留 rationale、必要时查看引言或结论。

这些都适合转化为 Paper2 的证据等级规则：题摘级只能候选；全文文本级才可采纳字段；图表级数值要回原文核对；每个字段都要有 source anchor 和裁决记录。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 主要面向 overview、topic coverage、publication trend、venue/forum、research type，而非 effect size。 | `paper_content.txt` §2.1、Table 1。 | 可迁移为 A2a 的 mapping 型 RQ 模板。 | 不适合直接回答技术有效性或 causal outcome。 |
| dimension pattern | 三个核心 facet：topic、contribution、research type；分类方案通过 keywording 从论文中演化。 | §2.4、Figure 2、Table 3。 | 可作为 researcher-defined meta-model 字段树候选。 | 具体 topic facet 来自 product-line variability 示例，不得迁移到 LLM4STM。 |
| finding pattern | 通过类别频数和交叉覆盖识别研究空白，并提出 map 与 review 互补使用的建议。 | §2.5、§3.2、§4、§5。 | 可迁移为“统计观察 → 缺口解释 → 后续 review 决策”的 finding heuristic。 | finding 属方法学层，不是目标领域事实。 |
| evidence presentation pattern | extraction table + short rationale + category frequency + bubble plot / table。 | §2.5、Figure 3、Table 5。 | 可迁移为字段级证据表和 coverage dashboard。 | 图表布局和气泡位置需 PDF 视觉核对。 |
| validity / threat pattern | 主要威胁是摘要信息不足、术语混乱、搜索/纳排过窄、分类误判、depth/breadth trade-off。 | §3.2、§4。 | 可迁移为 A2a 的分类效度与证据等级说明。 | 本文没有完整独立 threats checklist。 |
| report structure pattern | 结构为背景 / 方法流程 / 比较分析 / guideline / 结论，适合作为方法学综述写作模板。 | 章节 §1--§5。 | 可迁移到 survey-of-surveys 方法章节和 pattern library 文档。 | 后续 Paper2 还需加入人机协同、审计制品链和研究者裁决。 |

## 4. A1-M0--M6 元维度贡献

| A1-M 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 研究意图与综述元模型 | 定义 systematic map 的目标、范围、产物和与 systematic review 的差异。 | 先由研究者设定主题范围与 mapping / review 类型。 | 不把 map 的 breadth 误写成 review 的 evidence strength。 |
| A1-M1 语料收集与纳排 | 搜索串、数据库 / 手工论坛、纳排标准都由 RQ 驱动；过窄 outcome 会破坏地图完整性。 | 检索计划应记录 scope、forum、数据库、排除理由和失败路径。 | 搜索范围和纳排宽度需与目标论文贡献一致。 |
| A1-M2 研究对象与主题语义 | topic facet 展示如何把领域对象组织为主题轴。 | 可迁移为 LLM4STM / LLM4modeling 的对象、工件、任务、输出谱系等字段树。 | 示例 topic 不能跨领域照搬。 |
| A1-M3 方法 / 技术 / 干预 | contribution facet 与 research type facet 展示论文方法形态分类。 | 可迁移为方法类型、工具、agent 角色、human-in-the-loop、研究类型字段。 | Wieringa 分类需结合现代 LLM/agent 研究扩展。 |
| A1-M4 评价、证据与复现资产 | extraction table、short rationale、frequency table、bubble plot 都是字段证据资产。 | Paper2 字段值必须带 rationale / source anchor / schema version。 | 本文不要求公开复制包，不能直接支撑 artifact completeness。 |
| A1-M5 统计分析就绪 | 类别频数、交叉覆盖、趋势和 bubble plot 可作为候选支撑描述性统计。 | 可迁移为 coverage matrix、cross-tab、分母固定和 missing-value 语义。 | 不支持 effect-size meta-analysis。 |
| A1-M6 research finding 形成与裁决 | 从覆盖缺口形成 future review / guideline 建议，强调 map 与 review 互补。 | 可迁移为候选 finding ledger 的“覆盖缺口 / 后续深读”启发式。 | 最终领域发现仍需研究者裁决和反证检查。 |

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **维度模式必须允许演化**：keywording 和后续分类更新说明字段不是一次写死的，而是要有版本、合并、拆分和回填。
2. **字段值要有短理由**：作者要求每篇论文归类时给 rationale；Paper2 应把这个升级为 source span + rationale + confidence。
3. **统计分析适合先做 coverage**：map 的核心是频数和交叉覆盖，适合让研究者快速看出哪里值得深读。
4. **map 与 review 应分工**：A1/A2b 的 survey-of-surveys 可以先提供模式地图，A4/A5 目标主题试运行再做深度证据和 finding 裁决。
5. **分类效度是核心风险**：LLM/agent 自动抽字段时，最危险的不是少写摘要，而是把论文放错类别且没有证据链。

### 6.2 风险

1. 该文的图表信息较多，`paper_content.txt` 难以还原 Figure 1--3 的布局；正式引用图形模式前需视觉核对。
2. 该文的统计主要是描述性覆盖，不应被写成效果评估或因果证据。
3. 2008 年的研究类型分类需要用现代 LLM/agent 论文重新扩展，否则可能低估工具 / 系统 / agentic workflow 的类别。
4. 该文没有把开放制品作为强制字段；Paper2 不能因此放松 run record、原文 span、schema revision log 等审计要求。

## 7. 待复核

1. A2a 若要精确引用 mapping process 图，需视觉核对 Figure 1（p.2）。
2. A2a 若要复用 keywording 流程，需视觉核对 Figure 2（p.4）。
3. A2a 若要复用 bubble plot 模式，需视觉核对 Figure 3（p.5）。
4. Table 3 的 Wieringa research type 与 Table 5 的 review characteristics 若用于正式字段定义，需核对跨列表格排版。
5. `file` 与 `pdfinfo` 页数显示不一致；当前以 `pdfinfo` 和 `paper_content.txt` 的 10 页为准。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__codex.md](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__codex.md)、[../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__claude.md](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__claude.md)、[../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__deepseek.md](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md](../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `petersen-2008-systematic-mapping` |
| 审计代理 | `claude`（claude-opus-4-7[1m]，主进程，无 subagent） |
| 是否已读 `paper_content.txt` | 是 — 全文 537 行（10 页 OCR/text 提取版本）逐页通读，含 Tables 1–5、Figures 1–3 文本提取部分 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是 — 均已读 |
| 是否打开或核对 `paper.pdf` | 否（本轮未做版面级视觉核对）；表/图编号、页码以 `paper_content.txt` 的 `--- Page N ---` 分隔为准；Figure 3 bubble plot 数字布局只做了文本级辨认，未核对图形细节 |
| 原文类型 | 方法学论文（SMS 指南 / methodology paper），内嵌一个 n=10 SLR 特征化样本表 与 n=2 mapping 示例对比 |
| 被编码样本单位 | 主样本：10 篇 SE systematic reviews（Table 4–5）；辅助样本：2 个 mapping 示例研究（Bailey 2007 OO 设计；Mujtaba 2008 SPL Variability，Tables 1–2 + Figure 3）；另含处方型 模式（3-facet + Wieringa）面向未来 SMS 使用，但不是本文自己的样本编码 |
| 样本数量 / 分母 | Table 5 主样本 n=10（从 21 篇 SLR 候选中筛得 8+2=10）；mapping 示例对比 n=2；Wieringa 研究类型枚举值 6；Means of Analysis 枚举值 4；研究目标（Research Goals） 枚举值 4；Inclusion 需求 枚举值 2 |
| 原生树类型 | **维度森林**（4 棵子树）：A=SLR 特征化表（n=10 真实样本）、B=mapping 示例对比表（n=2 真实样本）、C=处方 3-facet 分类（模式种子）、D=SMS 流程 流程管线（流程 模式） |
| 主统计池资格 | 否；不进入后续主统计池。A1-DT v2 仅允许其作为方法学种子、模式种子或边界锚点；若原文内部存在 convenience sample / guideline 示例统计，也不得混入 Paper2 主统计池。 |
| 总体判定 | v2 已返修完成：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

---

### 1. 原文证据阅读说明

#### 1.1 实际读取范围

- 完整阅读 `paper_content.txt`（537 行 / 10 页）：Abstract、§1 Introduction、§2.1–§2.5 SMS 流程、§3.1–§3.2 比较与讨论、§4 指南、§5 Conclusion、References。
- 完整阅读 `bibtex.bib`：DOI = 10.14236/ewic/EASE2008.8，作者 4 人，venue = EASE 2008 / BCS。
- 完整阅读 `metadata.json`：确认 `eligible_for_statistical_synthesis = false`、`evidence_role = "mapping_guideline_pattern"`、`systematic_evidence_status = "systematic_mapping"`。
- 完整阅读当前 `review.md`：确认需把真实样本表与处方型 SMS 流程分层复原。

#### 1.2 未做的核验

- 未在 PDF 中视觉核对 Figure 1（SMS 流程图）、Figure 2（keywording 构建分类方案）、Figure 3（bubble plot）；`paper_content.txt` 中 Figure 3 数字布局是字符流，未做形位还原。
- 未核对 Table 3 (Wieringa 研究类型表) 与 Table 5 (SLR 特征表) 的列对齐细节，但二者文本完整可读，枚举项清晰。
- `autoresearch/SKILL.md`（位于 codex 插件缓存）本轮未直接读取，记为 `部分-blocked`，但所采用的"先样本单位 → 再字段结构 → 再证据链"工作流与 autoresearch / research-planning skill 的 4 阶段输出一致。

#### 1.3 关键证据锚点（11 条，控制短引）

| 锚点 | 位置 | 短引或释义 |
|---|---|---|
| E1 | §Abstract（p.1 line 12–17） | "build a 分类方案 … analysis of results focuses on 频次 of publications for 类别" — 明确分析重心是类别频数 |
| E2 | §2 (p.2 Figure 1) | SMS 五步流程：Definition of RQ → Conduct Search → Screening → Keywording (abstracts) → 数据抽取（数据抽取） & Mapping |
| E3 | §2.1 Table 1 (p.2) | 两个示例研究的 RQ 字段化对比：OO 设计 Map 3 个 RQ vs SPL Variability Map 2 个 RQ |
| E4 | §2.3 Table 2 (p.3) | 两个示例研究的 Inclusion/Exclusion 字段化对比 |
| E5 | §2.4 (p.4) "three main 切面（facets） were created … topic … type of contribution … research facet" | 三-facet 分类方案的明确定义 |
| E6 | §2.4 Table 3 (p.4) | Wieringa 6 类研究类型封闭枚举：Validation / Evaluation / 解决方案提案 / Philosophical / Opinion / Experience |
| E7 | §2.5 (p.5) "Excel table … each category … short rationale why the paper should be in a certain category" | 抽取表 + 短理由（rationale）字段化要求 |
| E8 | §2.5 Figure 3 (p.5) bubble plot | 多 facet 交叉频数可视化：Variability Context × Contribution × 研究（Research）（数字含 50/56/0/8/128 等列汇总） |
| E9 | §3 (p.6) "search resulted in a total of 21 papers … this resulted in eight systematic reviews being included … two further … resulted in ten" | Tree A 样本分母链：候选 21 → 含 8 + 补 2 = 10 |
| E10 | §3.1 Table 5 (p.7) | n=10 SLR × 4 字段组（研究目标（Research Goals） 4 类 / Inclusion 2 类 / Numeric 计数 / Means of Analysis 4 类）的样本编码主表 |
| E11 | §4 (p.8–9) "Adaptive Reading Depth … Classify Papers Based on Evidence and Novelty … Visualize Your Data" | 四条 指南 扩展（recommend）— 处方建议，不是被编码的样本字段 |

---

### 2. 样本单位与字段来源判定

#### 2.1 五问回答

1. **原文纳入并逐项描述的对象是什么？**
   - **主样本（Tree A，n=10）**：作者用 "系统综述 AND software engineering" 在 Inspec/Compendex、IEEExplore、ACM DL 检索得 21 篇候选，按"在 SE 内 / 遵循 Kitchenham&Charters 2007 / 标题或摘要明示 系统综述"筛得 8 篇 + Kitchenham 2007 keynote 中补 2 篇 = **10 篇 SE systematic reviews**（Table 4 给出 ID 1–10 文献，Table 5 给出特征化字段）。
   - **辅样本（Tree B，n=2）**：两个 mapping 示例研究——(Bailey et al. 2007) 的 OO 设计 Map 与 (Mujtaba et al. 2008) 的 SPL Variability Map——作为"如何做 SMS"的示例，被在 Tables 1–2 和 Figure 3 中字段化对比。

2. **作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**
   - 对 Tree A 有：明确检索串、3 库来源、纳排标准、补充入选规则，最终编码到 Table 5 的 4 字段组。
   - 对 Tree B 没有系统检索：示例研究是作者团队自己的两篇先行工作（其中 Mujtaba 2008 还是 in-submission 状态），用于说明 SMS 流程，不是被独立纳排筛出的样本。

3. **原文字段来自哪里？**
   - Tree A 的字段：来自作者自定义的特征化 模式（§3.1 "研究目标（Research Goals） / Inclusion 需求 / Number of Articles Included / Means of Analysis"），其中 Means of Analysis 部分明确引用 Dixon-Woods 2005。
   - Tree B 的字段：RQ、Search Strings、数据库（databases）/Forums、Inclusion/Exclusion 沿用 Kitchenham&Charters 2007 SLR 协议字段。
   - 处方 Tree C 的字段：Wieringa 2006（研究类型（Research-Type） 6 类）+ 作者新增 Contribution 类（流程/方法/模型/工具/指标）+ 领域相关 Topic facet。
   - 流程 Tree D：作者自创 5 步 流程管线（Figure 1）。

4. **RQ 与样本单位的关系？**
   - 本文没有用 RQ1/RQ2/... 形式声明本文自己的研究问题；§Objective 用自然语言陈述："describe how to conduct SMS"、"compare SMS with SLR"、"provide 指南"。
   - 因此 RQ 在本文中不是树根，而是"目标声明"；Table 1 的 RQ 列是被对比的两个示例研究的 RQ，是 Tree B 的一个字段。

5. **若无系统样本库，如何降级？**
   - 不需要降级。本文同时具备方法论叙述（模式种子）+ 真实样本表（n=10 编码 + n=2 对比），可同时作为：(i) Tree A 的小型描述性统计 seed（不进领域统计池）；(ii) Tree C 的处方 模式种子；(iii) Tree D 的 流程 流程管线 seed。

#### 2.2 当前复原重点

当前复原的重点是明确区分“本文编码的真实样本表”（n=10 SLR、n=2 mapping 示例）与“本文向未来 SMS 推荐使用的处方模式”（3-facet），避免把示例性样本编码和方法学建议混成同一层。

---

### 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**。下面分四棵子树给出，每棵树标注 `样本性`（被编码 vs 处方）与 `用途`。

#### 3.1 Tree A — SLR 特征化样本表（n=10，被编码样本）【主样本】

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[A] SE 系统综述特征化表  ── 样本单位 = 1 篇 SLR；n=10；分母可统计
├── A.1 引用身份  (Table 4)
│   ├── A.1.1  引用编号  取值 ∈ {1..10}            [完整枚举, 数值 ID]
│   └── A.1.2  引用键                       [自由文本, 文献引用]
├── A.2 研究目标  (Table 5, 行 1–4)        [多值布尔, 一篇 SLR 可同时占多列]
│   ├── A.2.1  识别最佳与典型实践（识别最佳与典型实践）    [布尔]
│   ├── A.2.2  分类与分类法（分类 and 分类法；下文简称“分类目标”）            [布尔]
│   ├── A.2.3  强调主题类别（强调主题类别）           [布尔]
│   └── A.2.4  识别发表场所（识别发表场所；下文简称“发表源识别”）              [布尔]
├── A.3 纳入要求  (Table 5, 行 5–6) [多值布尔]
│   ├── A.3.1  研究位于关注范围内（研究位于关注范围内）          [布尔]
│   └── A.3.2  使用经验方法（使用经验方法）                 [布尔]
├── A.4 纳入文章数量  (Table 5, 行 7–8) [数值]
│   ├── A.4.1  潜在相关研究（潜在相关研究）           [自然数 或 不适用]
│   └── A.4.2  纳入的相关研究（纳入的相关研究）              [自然数]
└── A.5 分析方式  (Table 5, 行 9–12)    [多值布尔]
    ├── A.5.1  元研究（Meta 研究）                             [布尔]
    ├── A.5.2  比较分析（比较分析）                   [布尔]
    ├── A.5.3  主题分析（主题分析）                      [布尔]
    └── A.5.4  叙事总结（叙事总结）                      [布尔]
```

#### 3.2 树 B：系统映射示例研究对比表（n=2，被编码样本）【辅助样本】

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[B] 两个 mapping 示例研究的对比表  ── 样本单位 = 1 个 mapping 示例；n=2
├── B.1 研究问题  (Table 1)             [自由文本 + RQ 列表]
├── B.2 检索式                             [自由文本布尔表达式]
├── B.3 数据库 / 论坛                        [枚举：CS 数据库全集 vs SPLC+PFE+期刊]
├── B.4 纳入标准  (Table 2)            [自由文本判定规则]
├── B.5 排除标准  (Table 2)            [自由文本判定规则]
├── B.6 分类方案                     [三切面实例化或干预类型（intervention type）]
└── B.7 可视化                             [汇总统计（summary stats）/ 频数表（freq table） vs 气泡图（bubble plot）]
```

#### 3.3 树 C：处方型三切面分类模式（作为模式种子，供未来 SMS 使用）【处方】

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[C] SMS 推荐分类方案  ── 处方层；不是被本文编码的样本字段
├── C.1 主题切面                               [开放层级；领域相关；示例 = 软件产品线可变性（SPL Variability）6 类]
├── C.2 贡献类型切面  (§2.4)                [枚举：过程（process）/ 方法/ 模型/ 工具/ 指标]
└── C.3 研究类型切面  (Table 3, Wieringa)  [封闭枚举, 互斥 6 类]
    ├── C.3.1  验证型研究（验证型研究）
    ├── C.3.2  评价型研究（评价型研究）
    ├── C.3.3  方案提出型论文（解决方案提案）
    ├── C.3.4  哲学型论文（哲学型论文）
    ├── C.3.5  观点型论文（观点型论文）
    └── C.3.6  经验型论文（经验型论文）
```

#### 3.4 树 D：SMS 流程管线（过程模式，未来 SMS 使用）【处方】

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[D] SMS 五步流程（Figure 1）  ── 处方层；过程节点不是字段
├── D.1 定义研究问题 / 综述范围（Definition of 研究问题 / 综述范围）    → 输出：综述范围
├── D.2 执行检索（执行检索）                                    → 输出：全部论文（全部论文）
├── D.3 论文筛选（论文筛选；纳入 / 排除）       → 输出：相关论文
├── D.4 基于摘要关键词化（基于摘要关键词化）                        → 输出：分类方案
└── D.5 数据抽取与映射过程（数据抽取 and Mapping 过程）              → 输出：系统映射图
```

#### 3.5 与已有 review.md `维度树结构` 的对照

当前复原必须把 Tree D（流程节点：mapping planning / keywording / classification / visualization / gap identification）与 Tree A（真实 n=10 样本编码表）分开，避免流程树挤占样本编码树的位置。

---

### 4. 叶子维度表

下表只列**有原文证据支撑的叶子**；处方型 C/D 子树的叶子用 `模式种子（schema_seed）` 标记。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-A.2.1 | 目标—识别最佳/典型实践 | A.2 | Table 5 第 1 行 "识别最佳与典型实践" | SLR 是否声明以经验研究识别最佳或典型实践为目标 | {true, false} | 布尔 | 单元格空白 = false | 10 篇中标 x 的 8 篇可统计为 80% | 多目标重叠 → SLR 多目标常态 | E10 | 可作 SLR/SMS 目标分类种子；不可外推到非 SE 领域 |
| L-A.2.2 | 目标—分类与分类法 | A.2 | Table 5 第 2 行 | SLR 是否产出 框架 / 分类法 / 分类 | {true, false} | 布尔 | 空白 = false | 10/10 中 3 篇（ID 7, 8, +1） | mapping 与 review 的目标交集 | E10 | 同上 |
| L-A.2.3 | 目标—主题类别强调 | A.2 | Table 5 第 3 行 | SLR 是否统计各子主题论文分布 | {true, false} | 布尔 | 空白 = false | 2/10 | 与 Identify Publication Fora 强相关 | E10 | 同上 |
| L-A.2.4 | 目标—识别发表论坛 | A.2 | Table 5 第 4 行 | SLR 是否识别相关 journal/conf/workshop | {true, false} | 布尔 | 空白 = false | 2/10 | 与 mapping 目标更接近 | E10 | 同上 |
| L-A.3.1 | 纳入要求—主题相关 | A.3 | Table 5 第 5 行 | 全 10 篇都要求 | {true} | 布尔（饱和） | n/a | 10/10；常量列；无判别力 | 揭示"主题相关性"是 SLR 通用门槛 | E10 | 不可作判别字段，只作 baseline check |
| L-A.3.2 | 纳入要求—使用经验方法 | A.3 | Table 5 第 6 行 | 是否限定 原始研究 使用经验方法 | {true, false} | 布尔 | 空白 = false | 8/10 | "经验方法"是 SLR 的主导筛选门槛 | E10 | 可迁移为 SLR vs SMS 区分点 |
| L-A.4.1 | 候选论文数 | A.4 | Table 5 第 7 行 | 检索阶段命中数 | {自然数 ∪ 不适用}；观测值 = {5453, 963, 5453, 5453, 1344, 353, 5453, 不适用, 185, 564} | 数值或缺失 | 不适用 = 作者未报告 | 中位数 ≈ 1344；偏态分布 | 揭示 SLR 检索规模差异巨大（185–5453） | E10 | 单位为篇；不同检索策略不可直接比较 |
| L-A.4.2 | 入选论文数 | A.4 | Table 5 第 8 行 | 最终入选数 | {自然数}；观测值 = {78, 24, 24, 78, 10, 173, 103, 304, 10, 26} | 数值 | 不应缺失 | 中位数 ≈ 26；最大 304 | 入选率 = A.4.2/A.4.1，呈现 SLR 严苛性 | E10 | 与领域、方法严苛度强耦合 |
| L-A.5.1 | 分析方法—Meta Study | A.5 | Table 5 第 9 行 | 是否做统计 元分析（meta-analysis） | {true, false} | 布尔 | 空白 = false | 2/10 | 元分析（meta-analysis） 在 SE SLR 中罕见 | E10 | 可作 SLR 方法学成熟度指标 |
| L-A.5.2 | 分析方法—Comparative Analysis | A.5 | Table 5 第 10 行 | 是否使用逻辑简化/置信度评估 | {true, false} | 布尔 | 空白 = false | 1/10 | 极少见 | E10 | 同上 |
| L-A.5.3 | 分析方法—Thematic Analysis | A.5 | Table 5 第 11 行 | 是否按主题计数 | {true, false} | 布尔 | 空白 = false | 2/10 | 这是 mapping 的核心方法 | E10 | mapping 与 review 重叠点 |
| L-A.5.4 | 分析方法—Narrative Summary | A.5 | Table 5 第 12 行 | 是否使用叙述性总结 | {true, false} | 布尔 | 空白 = false | 10/10；常量列 | 所有 SE SLR 都做叙述总结 | E10 | 表明"叙述"是 SE SLR 默认输出形态 |
| L-B.1 | 示例—RQ 集合 | B.1 | Table 1 | 示例研究的 RQ 列表 | 自由文本 | 自由文本 | n/a | n=2 不可统计 | 揭示 RQ 颗粒度（3 vs 2） | E3 | n=2 不能外推 |
| L-B.2 | 示例—检索串 | B.2 | §2.2 | 布尔表达式 | 自由文本 | 自由文本 | n/a | n=2 | 揭示 PICO 在 SMS 中可松绑 outcome | §2.2 line 117–121 | 不可量化 |
| L-B.3 | 示例—数据库/论坛 | B.3 | §2.2 | 检索来源 | 自由文本 + 类别 | 半结构化 | n/a | n=2 | "全 CS 库"vs"特定 venue + 期刊"二元对比 | §2.2 line 122–128 | n=2 不能外推 |
| L-B.4 | 示例—纳入标准 | B.4 | Table 2 | 详细 inclusion 规则 | 自由文本 | 自由文本 | n/a | n=2 | "需经验证据" vs "摘要明示主题" | E4 | n=2 不能外推 |
| L-B.5 | 示例—排除标准 | B.5 | Table 2 | 详细 exclusion 规则 | 自由文本 | 自由文本 | n/a | n=2 | 抽象关键词偶现 ≠ 实质贡献 | E4 | n=2 不能外推 |
| L-B.6 | 示例—分类方案 | B.6 | §2.4 | 实际采用的 facet 组合 | OO 设计 用 intervention type；SPL Variability 用 3-facet | 半结构化 | n/a | n=2 | Bailey 用 1 facet；Petersen 团队推荐 3 facet | E5 | 示例性 |
| L-B.7 | 示例—可视化 | B.7 | §2.5 + Figure 3 | 频数表 vs bubble plot | {汇总统计（summary stats）, 频数表（频次 table）, 气泡图（bubble plot）} | 枚举（n=2 观测） | n/a | n=2 | bubble plot 是新增贡献 | E8 | 可作处方 seed |
| L-C.3.* | Wieringa 研究类型（处方枚举） | C.3 | Table 3 | 推荐用于未来 SMS 的论文研究类型分类 | {验证型研究（验证型研究）, 评价型研究（评价型研究）, 方案提出型论文（解决方案提案）, 哲学型论文（哲学型论文）, 观点型论文（观点型论文）, 经验型论文（经验型论文）} | 封闭枚举（6） | 互斥使用 | 不计入本文样本编码 | 可作所有下游 SMS 的字段种子 | E6 | 可迁移为 Paper2 论文研究类型字段；2008 年版本不含 LLM/智能体 类，需扩展 |
| L-C.2 | Contribution 类型（处方枚举） | C.2 | §2.4 | 推荐贡献类别 | {流程, 方法, 模型, 工具, 指标, ...} | 开放枚举 | 可多值 | 模式种子（schema_seed） | 字段种子 | E5 | 指标 在原文中实际出现于 Figure 3（"Metric" 列），可视为枚举的一部分 |
| L-C.1 | Topic Facet（处方开放） | C.1 | §2.4 | 领域相关主题轴 | 完全开放 | 自由文本/层级 | n/a | 模式种子（schema_seed） | 字段种子 | E5 | 必须按领域重建 |

---

### 5. 关系边表

本文存在**显式关系结构**——Table 5 是一个 `SLR × 字段` 的二维矩阵，每个单元格是一条 (SLR, 字段, 取值) 关系边；Figure 3 bubble plot 是 `Topic × Contribution × 研究类型（Research-Type）` 的三维交叉频数。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R-A.row×col | A.1.1 Reference ID（10 行） | 编码 | A.2/A.3/A.4/A.5 各字段（12 列） | 见 L-A.2.1 ~ L-A.5.4 | 单元格空白 = 该 SLR 不具该属性（除 A.4 为数值） | E10 / Table 5 | n=10 × 12 字段的二维矩阵；可做行/列汇总频数与交叉表 |
| R-B.row×col | B（OO 设计 / SPL Variability，2 行） | 对比 | B.1 ~ B.7（7 列） | 见 L-B.* | 不应缺失 | E3 / E4 | n=2 对比矩阵，只支持成对差异叙述 |
| R-C.facet3 | 论文（Bailey 2007 + Mujtaba 2008 样本） | 三-facet 交叉分类 | Topic × Contribution × 研究类型（Research-Type） | 见 Figure 3 数字 | 0 单元格 = 主题/方法缺口 | E8 | 处方的 bubble plot 交叉覆盖；Mujtaba SPL Variability 实例化为 6×5×6 三维网格 |
| R-D.流程管线 | D.1 ~ D.5（流程节点） | 顺序产出 | 综述范围（Review Scope） → 全部论文 → 相关论文（Relevant Papers） → 分类 Scheme → 系统映射图（Systematic Map） | 见 §2 Figure 1 | n/a | E2 | 顺序约束，非样本字段 |
| R-keywording | D.4 abstract keywording | 演化更新 | C 处方分类模式 | 可新增/合并/拆分类别 | n/a | §2.5 line 220–223 "the 分类方案 evolves while doing the 数据抽取, like adding new 类别 or merging and splitting existing 类别" | 处方 模式 演化关系 |

未发现额外的"论文之间引用"或"作者—venue"关系边被显式编码。

---

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段/统计表支持的统计观察（本文实有）

| 观察 | 来源 | 可成立强度 |
|---|---|---|
| 10 篇 SE SLR 中 8 篇以 "识别最佳与典型实践" 为目标（80%） | Table 5 行 1 | strong（n=10 频次） |
| 10 篇 SE SLR 全部使用 Narrative Summary 作为分析手段 | Table 5 行 12 | strong；常量列说明"叙述总结是 SE SLR 默认输出" |
| 仅 2/10 使用 Meta Study；1/10 使用 Comparative Analysis | Table 5 行 9–10 | strong；揭示 SE SLR 量化合成不普及 |
| SLR 入选率（A.4.2/A.4.1）总体很低（如 78/5453 ≈ 1.4%；24/963 ≈ 2.5%） | Table 5 行 7–8 | strong but caveat：检索策略差异巨大 |
| SPL Variability bubble plot 中 评价型研究（评价型研究） 列 = 50/128 ≈ 39.06%，验证型研究（验证型研究） = 56/128 ≈ 43.75% | Figure 3 文本提取 | medium（文本提取，未做版面核对） |

#### 6.2 原文 §4 给出的候选发现（推荐 形态）

| 候选发现 | 性质 |
|---|---|
| SMS 与 SLR 应互补使用 — 先 SMS 结构化再 SLR 深入 | 推荐（非样本统计推论） |
| Adaptive Reading Depth：当摘要不足时应读 introduction/conclusion | 指南 经验性建议 |
| 应使用 Wieringa 研究类型分类，并按 证据-level 与 novelty 进一步细分 | 处方建议 |
| 应使用 bubble plot 等可视化展示多 facet 交叉 | 处方建议 |

#### 6.3 对 Paper2 可迁移的方法学启发

- "类别频数 + 交叉覆盖 → 候选缺口"链路（不直接等于 最终发现）；
- 抽取表必须配 short rationale 字段；
- 处方 模式 可演化（merge/split）；
- 多目标布尔多值列（研究目标（Research Goals）、Means of Analysis 一行多 x）的字段化方式可作为候选迁移启发；后续必须经 A2a 证据核验和研究者裁决后采纳到 Paper2 的"论文承担的角色 / 方法类型 / 评价方式"等字段。

#### 6.4 绝不能迁移的领域结论

- 任何关于 OO 设计、Software Product Line Variability 子领域的具体频数与缺口（如 Mujtaba SPL 中 Verification & Validation × 验证型研究（验证型研究） = 11 篇）；
- Bailey 2007 与 Mujtaba 2008 这两个示例的具体 RQ 与检索串；
- Table 5 中 10 篇具体 SLR 的领域结论（成本估算、需求获取等）。

---

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
