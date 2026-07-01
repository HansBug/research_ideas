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

对 Paper2 来说，这篇论文是“先构造领域地图，再决定是否需要深度证据合成”的方法学母文。它直接支持导师讨论中的判断：SLR / SMS 不是机械整理，真正关键是由研究者设定 scope 与维度，再用论文阅读持续修正维度模式。

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
| A1-M5 统计分析就绪 | 类别频数、交叉覆盖、趋势和 bubble plot 可直接支持描述性统计。 | 可迁移为 coverage matrix、cross-tab、分母固定和 missing-value 语义。 | 不支持 effect-size meta-analysis。 |
| A1-M6 research finding 形成与裁决 | 从覆盖缺口形成 future review / guideline 建议，强调 map 与 review 互补。 | 可迁移为候选 finding ledger 的“覆盖缺口 / 后续深读”启发式。 | 最终领域发现仍需研究者裁决和反证检查。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> [!WARNING] v1-deprecated: 本节为 A1-DT v1 历史草稿 / 迁移来源，只能作为返修来源和历史证据，不是 A1-DT v2 当前事实口径。v2 事实以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
说明：本旧版迁移草稿已中文化；英文 / 缩写保留为原文术语或后续字段标识。
系统映射研究模式（mapping_study_pattern）
├── 研究范围
│   ├── 概览目标
│   ├── 时间趋势目标
│   ├── 发表论坛目标
│   └── 缺口识别目标
├── 检索与选择
│   ├── 数据库检索
│   ├── 手工论坛检索
│   ├── RQ 驱动检索词
│   ├── 纳入标准
│   └── 排除标准
├── 分类方案
│   ├── 主题切面
│   ├── 贡献切面
│   ├── 研究类型切面
│   ├── keywording 来源
│   └── 类别演化 / 合并 / 拆分记录
├── 抽取证据
│   ├── 论文到类别的映射表
│   ├── 简短理由
│   ├── 类别频次
│   └── 交叉切面频次
├── 可视化
│   ├── 频次表
│   ├── 汇总统计
│   └── 气泡图
└── 发现边界
    ├── 覆盖缺口
    ├── 发表论坛缺口
    ├── map vs review 边界
    └── 下一轮综述建议
```

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
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__codex.md](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__codex.md)、[../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__claude.md](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__claude.md)、[../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__deepseek.md](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md](../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

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
| 总体判定 | v2 已返修完成：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

---

### 1. 原文证据阅读说明

#### 1.1 实际读取范围

- 完整阅读 `paper_content.txt`（537 行 / 10 页）：Abstract、§1 Introduction、§2.1–§2.5 SMS 流程、§3.1–§3.2 比较与讨论、§4 指南、§5 Conclusion、References。
- 完整阅读 `bibtex.bib`：DOI = 10.14236/ewic/EASE2008.8，作者 4 人，venue = EASE 2008 / BCS。
- 完整阅读 `metadata.json`：确认 `eligible_for_statistical_synthesis = false`、`evidence_role = "mapping_guideline_pattern"`、`systematic_evidence_status = "systematic_mapping"`。
- 完整阅读旧版 `review.md`（332 行）：确认其已包含历史 A1-DT v1 19×3 审计后返修块，但仍以六个通用接口叶为主叙述。

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
   - Tree B 的字段：RQ、Search Strings、数据库（databases）/Forums、Inclusion/Exclusion 直接复用 Kitchenham&Charters 2007 SLR 协议字段。
   - 处方 Tree C 的字段：Wieringa 2006（研究类型（Research-Type） 6 类）+ 作者新增 Contribution 类（流程/方法/模型/工具/指标）+ 领域相关 Topic facet。
   - 流程 Tree D：作者自创 5 步 流程管线（Figure 1）。

4. **RQ 与样本单位的关系？**
   - 本文没有用 RQ1/RQ2/... 形式声明本文自己的研究问题；§Objective 用自然语言陈述："describe how to conduct SMS"、"compare SMS with SLR"、"provide 指南"。
   - 因此 RQ 在本文中不是树根，而是"目标声明"；Table 1 的 RQ 列是被对比的两个示例研究的 RQ，是 Tree B 的一个字段。

5. **若无系统样本库，如何降级？**
   - 不需要降级。本文同时具备方法论叙述（模式种子）+ 真实样本表（n=10 编码 + n=2 对比），可同时作为：(i) Tree A 的小型描述性统计 seed（不进领域统计池）；(ii) Tree C 的处方 模式种子；(iii) Tree D 的 流程 流程管线 seed。

#### 2.2 与旧版 review.md 的差异判定

旧版 review.md 在"原文模式主树（19×3 审计后返修）"已经触及上述 Tree A 关键字段（研究目标（Research Goals）、Means of Analysis、Wieringa、Contribution、Map vs Review），但**仍未明确区分"本文编码的真实样本表"（n=10 SLR、n=2 mapping 示例）与"本文向未来 SMS 推荐使用的处方 模式"（3-facet）**。这是本轮 needs-repair 的核心。

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

旧版 review.md 的 `[dim-...-b1] mapping planning` / `[...b2] keywording` / `[...b3] 分类 scheme` / `[...b4] map visualization` / `[...b5] research gap identification` 五个主干分支实际上**全部来自 Tree D（流程节点）**，没有给 Tree A 的真实 n=10 样本编码表留位置。这是当前 review.md 最需要返修之处。

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
- 多目标布尔多值列（研究目标（Research Goals）、Means of Analysis 一行多 x）的字段化方式历史草稿曾提出迁移建议；当前禁止直接采信到 Paper2 的"论文承担的角色 / 方法类型 / 评价方式"等字段。

#### 6.4 绝不能迁移的领域结论

- 任何关于 OO 设计、Software Product Line Variability 子领域的具体频数与缺口（如 Mujtaba SPL 中 Verification & Validation × 验证型研究（验证型研究） = 11 篇）；
- Bailey 2007 与 Mujtaba 2008 这两个示例的具体 RQ 与检索串；
- Table 5 中 10 篇具体 SLR 的领域结论（成本估算、需求获取等）。

---

### 7. 对旧版 `review.md` 的返修来源（C / I / M）

#### C 级（必须返修，影响学术结论）

- **C1 — 维度树根结构错误：未区分"被编码样本"与"处方 模式"。** 现 `维度树结构` 节将五个流程步骤当作主干 b1–b5，把 Tree A 的 n=10 真实样本字段（研究目标（Research Goals） / Inclusion / Counts / Means of Analysis）压入 `[leaf-...-分类法]` 等通用接口叶，丢失了"本文最重要的样本编码就是 Table 5"这一事实。
  - **返修动作**：把"原生维度树/森林"改写为本审计第 3 节四棵子树并列；现"维度树结构" code block 应拆分为 Tree A / B / C / D 四块，并明确标注每棵树的样本性与 n。
- **C2 — Table 5 行×列矩阵缺失。** 现 review.md 没有把 Table 5 的二维结构作为关系边明确表化，导致后续无法做"行汇总（每篇 SLR 的目标向量）"与"列汇总（每个目标维度的频数）"的统计观察。
  - **返修动作**：补本审计 §5 关系边表，特别是 R-A.row×col。

#### I 级（重要，应在本轮或下一轮处理）

- **I1 — Wieringa 6 类与 Means-of-Analysis 4 类作为封闭枚举未在叶子层完整列出。** 现 `审计返修` 表只写"验证、评价、解决方案提案、philosophical、opinion、experience"一行，没有把 6 类分成 6 个叶子并标注取值空间为封闭互斥枚举。
  - **返修动作**：把本审计 §4 表中 L-C.3.1 ~ L-C.3.6 与 L-A.5.1 ~ L-A.5.4 抬升为正式叶子。
- **I2 — Bailey 2007 与 Mujtaba 2008 两个示例研究的 n=2 对比样本未被列为独立子树。** 现 review.md 完全忽略 Tree B；但 Tables 1、2 与 Figure 3 都是围绕这 2 个示例展开的字段化。
  - **返修动作**：新增 Tree B 章节，并明确 n=2 不可统计、仅作"成对对比叙述"。
- **I3 — 统计观察未明确分母 (10 vs 2 vs 21)。** 现 review.md 在 `统计与候选发现链路` 节把分母写成"当前 19 篇 survey-of-surveys 样本"，这是 SUMMARY 级分母，与本文内 n=10 / n=2 的内嵌统计混淆。
  - **返修动作**：分母按本文内嵌（n=10 SLR、n=2 mapping 示例）和文库外部（19 篇）两层分开标注。

#### M 级（建议性）

- **M1 — `历史草稿` 中保留的 v1 树（`mapping_study_pattern`）已被标注"不作事实真源"，建议进一步压缩或删除以减少阅读噪声。**
- **M2 — SUMMARY 表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"建议改为：样本单位 = `SE SLR (n=10) + mapping 示例 (n=2)`；样本数量 = `10 / 2`；原生树类型 = `维度森林（Tree A + B + 处方 C + 流程 D）`；统计池资格 = `否；仅方法学描述性 seed`。**
- **M3 — `原文模式候选叶子映射（A1 种子）` 表中 5 个候选叶子（mapping-planning / keywording / 分类-scheme / map-visualization / 缺口（gap）-identification）实际上都是 Tree D 流程节点，建议改名为 `Tree D process-节点 seed`，并新增 `Tree A sample-field` 与 `Tree C prescriptive-facet` 两类候选叶子。**
- **M4 — `审计返修口径` 提到三路审计（codex/claude/deepseek）共同结论，建议在本次 A1-DT v2 审计后更新该口径，标注 v2 已对 v1 通用六叶接口降级为投影。**

---

### 8. 历史审计草案归档（禁止消费为事实真源）

> [!WARNING] 历史草案归档，禁止消费为事实真源：本节仅保留 A1-DT v2 形成过程中的审计草稿，不得作为当前证据强度、SUMMARY 统计池、正式维度树或正式结论-证据映射使用。若本节与文末正式 `### A.1`--`### A.4` 审计附录冲突，一律以文末正式审计附录为准。

#### 历史 A.2 维度树证据账本草案（禁止消费）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-v2-001 | paper_content.txt | §Abstract; §2 Figure 1 | p.1 line 12–17; p.2 Figure 1 | "build a 分类方案 … analysis of results focuses on 频次"；SMS 5 步流程图 | scope_anchor | 历史草稿旧强度（当前禁止采信） | Tree D 全部节点、根节点 | false（Figure 1 节点名文本可读） | 仅限本文内部方法学叙述 |
| EV-v2-002 | paper_content.txt | §2.1 Table 1; §2.3 Table 2 | p.2; p.3 | 两个示例研究的 RQ 与 inclusion/exclusion 字段化对比 | sample_table | 历史草稿旧强度（当前禁止采信） | Tree B 全部叶子；L-B.1–L-B.5 | true（建议视觉核对 Table 1/2 列对齐） | n=2，仅作示例性对比，不可外推 |
| EV-v2-003 | paper_content.txt | §2.4 + Table 3 | p.4 | "three main 切面（facets） … topic … contribution … research"；Wieringa 6 类完整定义 | prescriptive_schema | 历史草稿旧强度（当前禁止采信） | Tree C 全部；L-C.1, L-C.2, L-C.3.1–L-C.3.6 | true（Table 3 文本完整，建议版面核对） | 处方层；2008 年版本，未含 智能体/LLM 类，需现代扩展 |
| EV-v2-004 | paper_content.txt | §2.5 + Figure 3 | p.5 | "Excel table … each category … short rationale"；bubble plot 数字 50/56/0/8/128 等 | sample_visualization | medium | L-B.6, L-B.7；R-C.facet3 | true（Figure 3 必须 PDF 视觉核对，文本提取已乱序） | Mujtaba SPL 领域结论不可迁移 |
| EV-v2-005 | paper_content.txt | §3 line 269–275 | p.6 | "21 papers … eight systematic reviews being included … two further … included" | sampling_chain | 历史草稿旧强度（当前禁止采信） | A.1.1 Reference ID 分母 = 10；候选 = 21 | false | 揭示 n=10 由 21→8+2 而来 |
| EV-v2-006 | paper_content.txt | §3.1 Table 5 | p.7 | 10 篇 SLR × (研究目标（Research Goals） 4 + Inclusion 2 + Counts 2 + Means of Analysis 4) 主表 | sample_encoding_matrix | 历史草稿旧强度（当前禁止采信） | Tree A 全部叶子；R-A.row×col | true（Table 5 视觉核对优先；尤其常量列如 A.5.4 全 x、A.3.1 全 x） | n=10 频数仅作方法学 seed，不进领域统计池 |
| EV-v2-007 | paper_content.txt | §3.2 + §4 | p.7–9 | mapping vs review 在 goal/流程/breadth/depth 上的差异；4 条 指南 扩展 | author_claim | medium | 候选发现 与处方 发现（§6.2） | false | 处方建议，不是样本统计推论 |
| EV-v2-008 | paper_content.txt | §4 "Adaptive Reading Depth"; §3.2 "Validity Consideration" | p.8 | 摘要不足 / 术语混乱 / 73% 论文 designation 错误 / 分类误判风险 | limitation | medium | 迁移边界；外推限制 | false | 限制本身可作 Paper2 字段误差源种子 |

#### 历史 A.3 结论-证据映射草案（禁止消费）

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-v2-T01 | 本文原生树类型为**维度森林**：Tree A (n=10 SLR 编码) + Tree B (n=2 mapping 对比) + Tree C (处方 3-facet) + Tree D (5 步流程)；不是单树 | 树类型（tree_type） | 根节点 | EV-v2-001, EV-v2-002, EV-v2-003, EV-v2-006 | 历史草稿旧强度（当前禁止采信） | 模式种子（schema_seed）；改写 review.md 维度树结构节 | Tree C/D 是处方层，不能写成"被编码的样本字段" |
| CLM-v2-A01 | Table 5 是本文唯一的样本编码主表，n=10 SLR × 12 字段；行=Reference ID，列=4 字段组下细分布尔/数值 | 样本单位（sample_unit） | Tree A 全部 | EV-v2-005, EV-v2-006 | 历史草稿旧强度（当前禁止采信） | 可作方法学描述性统计 seed；可生成行汇总（每 SLR 目标向量）与列汇总（每字段频数） | 不进入领域统计池；分母与检索策略强耦合 |
| CLM-v2-A02 | Means of Analysis 列 Narrative Summary 全 10 篇置 x，说明叙述总结是 SE SLR 默认输出形态；Meta Study 仅 2/10，揭示 SE SLR 量化合成不普及 | descriptive_stat | L-A.5.1, L-A.5.4 | EV-v2-006 | 历史草稿旧强度（当前禁止采信） | 可迁移为"SE SLR 方法学成熟度"指标 seed | 仅 n=10；可在更大 SLR 池中验证 |
| CLM-v2-A03 | Inclusion 需求 "研究（Research） is Within Focus Area" 全 10 篇都置 x，是常量列，无判别力 | descriptive_stat | L-A.3.1 | EV-v2-006 | 历史草稿旧强度（当前禁止采信） | 揭示该字段是 SLR 通用 baseline gate，不应进入分类用途 | n=10；可在更大池中验证 |
| CLM-v2-B01 | Bailey 2007 与 Mujtaba 2008 是本文的 mapping 示例样本（n=2），不是被独立纳排的样本 | 样本单位（sample_unit） | Tree B 全部 | EV-v2-002, EV-v2-004 | 历史草稿旧强度（当前禁止采信） | 用于对比 SMS 实施差异；仅成对叙述 | n=2 不可外推；Mujtaba 2008 当时为 in-submission |
| CLM-v2-C01 | Wieringa 6 类研究类型是封闭互斥枚举（Validation / Evaluation / 解决方案提案 / Philosophical / Opinion / Experience），构成处方 模式 的关键叶子层 | 叶子_definition | L-C.3.1 ~ L-C.3.6 | EV-v2-003 | 历史草稿旧强度（当前禁止采信） | 可迁移为 Paper2 论文研究类型字段种子 | 2008 年版本，需为 LLM/智能体 工作类型扩展 |
| CLM-v2-D01 | Figure 1 五步流程是处方 流程 模式；不能与 Tree A 样本字段混淆 | process_模式 | Tree D | EV-v2-001 | 历史草稿旧强度（当前禁止采信） | 可迁移为 Paper2 流程章节 | 不是样本字段，不能进入字段表 |
| CLM-v2-F01 | 本文给出的统计观察均为类别频数与交叉覆盖；§4 的 指南 扩展（互补使用 / Adaptive Reading Depth / Wieringa 推荐 / 可视化）是处方建议，不是样本统计推论 | 候选发现边界（candidate_finding_boundary） | L-A.2~A.5, §4 | EV-v2-006, EV-v2-007 | 历史草稿旧强度（当前禁止采信） | 仅作 候选发现；不可升级为 最终发现 | 最终发现 必须经跨论文证据与研究者裁决 |
| CLM-v2-R01 | 本文 §4 "Validity Consideration" 报告"73% 论文 designation 错误"是质量风险证据，可作 Paper2 字段误差源种子 | risk_anchor | Tree A 所有叶子 + Tree C | EV-v2-008 | medium | 可迁移为字段分类置信度种子 | 该数字来自 Mendes 2005 子集，不是本文 n=10 池 |

---

### 9. 技能使用与自我审查记录

#### 9.1 技能文件使用与采用原则

| 技能文件 | 读取状态 | 采用的关键原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 已读首 80 行 | "claim-证据-engineering workflow"、Evidence gate（仓库文件优先于记忆）、Task-state gate、Citation gate（不臆造引用） |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 已读首 80 行 | 5 维 reviewer 维度（Originality/Quality/Clarity/Significance/Reproducibility/Ethics）；C/I/M 应"足够具体到作者可操作" |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 已读首 60 行 | "不要默默修复"，要把无法在本轮验证的风险显式列出；reviewer simulation 中 Weaknesses 必须引用具体节/表/证据 |
| `research-planning/SKILL.md` | 已读首 60 行 | 4 阶段计划：Overall Plan → Architecture 设计 → Logic 设计 → Configuration；本审计在第 3 节用"样本单位 → 字段结构 → 关系边 → 统计/发现 边界"对应该 4 阶段 |
| `research-planning/references/planning-prompts.md` | 未直接读取（time-budget） | 间接应用（按 SMS 流程对照） |
| `research-planning/references/output-schemas.md` | 未直接读取 | 间接应用（JSON 结构化字段表） |
| `autoresearch/SKILL.md`（oh-my-codex 插件缓存） | 未读取 | `部分-blocked`；按本任务规范 §0(6) 记录 |

#### 9.2 Reviewer 视角—本输出最高风险 3 点

1. **Figure 3 bubble plot 数字未做 PDF 视觉核对**：本审计 §6.1 列出的 SPL Variability 频数（50/56/0/8/128 等）来自 `paper_content.txt` 字符流，未做形位还原；主线程合并前必须用 PDF 视觉核对一次，避免误把 OCR 串扰当作真实分布。
2. **n=10 与 n=19 两层分母容易在 SUMMARY 合并时混淆**：本文内嵌 Tree A 的 n=10 SLR 是"本文自己编码的样本"，与文库 SUMMARY 中的"19 篇 survey-of-surveys 样本"不是一个分母；如果不在 review.md 中显式分层，下游主线程做 SUMMARY 统计时可能把本文 n=10 的频数误当作 19 池贡献。
3. **Tree C（处方）与 Tree A（样本）的混淆延续**：若返修时仅替换通用六叶接口而不把"处方 模式种子"与"样本编码字段"分层，下一轮审计仍可能把 Wieringa 6 类当作"本文已统计样本的字段"，从而把处方建议误升级为统计观察。reviewer 应在合并时核查 review.md 是否明确写出"Tree C 是处方层，不是 n=10 编码字段"。

#### 9.3 blocked / timeout / 文件缺失

- `autoresearch/SKILL.md`: 未读取 — `部分-blocked`（time budget；按任务规范 §0(6) 记为风险，但不阻塞审计）。
- `paper.pdf` 视觉核对: 未做 — 已在多处显式标注 `needs_manual_check`。
- 其他指定技能/指南文件: 全部可读，无 file_missing 报错。

---

**审计结论一句话**：旧版 `review.md` 已经迈出 v1→v2 返修第一步（"原文模式主树"节），但仍把 Tree D 流程节点当成主干 b1–b5、把 n=10 真实样本表压成通用接口叶；本轮 A1-DT v2 审计的核心增量是确认本文为**维度森林**（n=10 SLR 表 + n=2 mapping 对比 + 3-facet 处方 + 5 步过程），并把 Table 5 的 12 个具体字段、Wieringa 6 类封闭枚举、Means of Analysis 4 类多值布尔列作为正式叶子升级到原文模式主树。判定：**需要返修**（C1+C2 必须本轮返修；I1–I3 应在下一轮处理；M1–M4 为建议）。

> [!NOTE]
> v2 返修后记：以上“对旧版 `review.md` 的返修来源”和审计草案是 A1-DT v2 返修前的独立审计输入；当前文件已经在[维度树复原](#维度树复原)与文末 A.1--A.4 中完成主线程裁决和返修。本审计报告保留为历史归档，不再作为当前状态判定依据。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md](../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-petersen-2008-systematic-mapping-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-petersen-2008-systematic-mapping-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-petersen-2008-systematic-mapping-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-petersen-2008-systematic-mapping-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-petersen-2008-systematic-mapping-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-petersen-2008-systematic-mapping-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/petersen-2008-systematic-mapping__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-petersen-2008-systematic-mapping-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/petersen-2008-systematic-mapping.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见上文“维度树复原”的叶子维度表、关系边表和审计草案。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-petersen-2008-systematic-mapping-type | clm-petersen-2008-systematic-mapping-type | src-petersen-2008-systematic-mapping-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：方法学论文（SMS guideline / methodology paper），内嵌一个 n=10 SLR 特征化样本表 与 n=2 mapping 示例对比 | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-petersen-2008-systematic-mapping-unit | clm-petersen-2008-systematic-mapping-unit | src-petersen-2008-systematic-mapping-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：主样本：10 篇 SE systematic reviews（Table 4–5）；辅助样本：2 个 mapping 示例研究（Bailey 2007 OO Design；Mujtaba 2008 SPL Variability，Tables 1–2 + Figure 3）；另含处方型 schema（3-facet + Wieringa）面向未来 SMS 使用，但不是本文自己的样本编码 | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-petersen-2008-systematic-mapping-denom | clm-petersen-2008-systematic-mapping-denom | src-petersen-2008-systematic-mapping-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：Table 5 主样本 n=10（从 21 篇 SLR 候选中筛得 8+2=10）；mapping 示例对比 n=2；Wieringa 研究类型枚举值 6；Means of Analysis 枚举值 4；Research Goals 枚举值 4；Inclusion Requirements 枚举值 2 | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-petersen-2008-systematic-mapping-tree | clm-petersen-2008-systematic-mapping-tree | src-petersen-2008-systematic-mapping-text; src-petersen-2008-systematic-mapping-codex; src-petersen-2008-systematic-mapping-claude; src-petersen-2008-systematic-mapping-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林**（4 棵子树）：A=SLR 特征化表（n=10 真实样本）、B=mapping 示例对比表（n=2 真实样本）、C=处方 3-facet 分类（模式种子）、D=SMS 流程 pipeline（process schema） | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-petersen-2008-systematic-mapping-pool | clm-petersen-2008-systematic-mapping-pool | src-petersen-2008-systematic-mapping-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：否；方法论文 / guideline-like seed。仅 Tree A 内部 n=10 频数和 Tree B 的 n=2 对比可作方法学描述性统计 seed，不进入领域统计合成池；Tree C/D 仅为 模式种子（schema_seed） | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-petersen-2008-systematic-mapping-type | A1DT-petersen-2008-systematic-mapping-C01 | 本文原文类型为：方法学论文（SMS guideline / methodology paper），内嵌一个 n=10 SLR 特征化样本表 与 n=2 mapping 示例对比 | paper_type | type | ev-petersen-2008-systematic-mapping-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-petersen-2008-systematic-mapping-unit | A1DT-petersen-2008-systematic-mapping-C02 | 本文被编码样本单位为：主样本：10 篇 SE systematic reviews（Table 4–5）；辅助样本：2 个 mapping 示例研究（Bailey 2007 OO Design；Mujtaba 2008 SPL Variability，Tables 1–2 + Figure 3）；另含处方型 schema（3-facet + Wieringa）面向未来 SMS 使用，但不是本文自己的样本编码 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-petersen-2008-systematic-mapping-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-petersen-2008-systematic-mapping-tree | A1DT-petersen-2008-systematic-mapping-C03 | 本文原生维度树 / 维度森林为：**维度森林**（4 棵子树）：A=SLR 特征化表（n=10 真实样本）、B=mapping 示例对比表（n=2 真实样本）、C=处方 3-facet 分类（模式种子）、D=SMS 流程 pipeline（process schema） | 树类型（tree_type） | native_tree | ev-petersen-2008-systematic-mapping-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-petersen-2008-systematic-mapping-pool | A1DT-petersen-2008-systematic-mapping-C04 | 本文统计池资格为：否；方法论文 / guideline-like seed。仅 Tree A 内部 n=10 频数和 Tree B 的 n=2 对比可作方法学描述性统计 seed，不进入领域统计合成池；Tree C/D 仅为 模式种子（schema_seed） | eligibility | 统计池（statistical_pool） | ev-petersen-2008-systematic-mapping-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-petersen-2008-systematic-mapping-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-petersen-2008-systematic-mapping-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-petersen-2008-systematic-mapping-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
