`★ Insight ─────────────────────────────────────`
- Petersen 2008 这篇论文实际上承担两种角色：它既是 SMS 方法论文（处方式），又内嵌一个 n=10 的小型 systematic-review 特征化样本表 (Table 5)；前者给出"未来 SMS 应使用的 facet 三维分类"（处方 schema），后者才是"被本文实际编码的样本表"（描述 schema）。已有 review.md 把两者混压进六个通用接口叶，未把 Table 5 的 n=10 字段化样本与 Tables 1+2 的 n=2 对比样本作为原文真实样本单位区分开。
- 关键澄清：本文同时存在"维度森林"——(A) 10 篇 SLR 的特征化 schema [n=10]、(B) 2 个 mapping 示例研究的对比 schema [n=2]、(C) 未来 SMS 推荐采用的 3-facet 分类（Topic × Contribution × Wieringa Research-Type）、(D) SMS 流程 5 步 pipeline。其中只有 (A) 与 (B) 是被本文实际编码的样本单位，(C)(D) 是处方 schema，不能写成"被编码字段"。
`─────────────────────────────────────────────────`

下面给出完整中文审计报告。

---

# A1-DT v2 单篇审计报告 — `petersen-2008-systematic-mapping`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2008-systematic-mapping` |
| agent | `claude`（claude-opus-4-7[1m]，主进程，无 subagent） |
| 是否已读 `paper_content.txt` | 是 — 全文 537 行（10 页 OCR/text 提取版本）逐页通读，含 Tables 1–5、Figures 1–3 文本提取部分 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是 — 均已读 |
| 是否打开或核对 `paper.pdf` | 否（本轮未做版面级视觉核对）；表/图编号、页码以 `paper_content.txt` 的 `--- Page N ---` 分隔为准；Figure 3 bubble plot 数字布局只做了文本级辨认，未核对图形细节 |
| 原文类型 | 方法学论文（SMS guideline / methodology paper），内嵌一个 n=10 SLR 特征化样本表 与 n=2 mapping 示例对比 |
| 被编码样本单位 | 主样本：10 篇 SE systematic reviews（Table 4–5）；辅助样本：2 个 mapping 示例研究（Bailey 2007 OO Design；Mujtaba 2008 SPL Variability，Tables 1–2 + Figure 3）；另含处方型 schema（3-facet + Wieringa）面向未来 SMS 使用，但不是本文自己的样本编码 |
| 样本数量 / 分母 | Table 5 主样本 n=10（从 21 篇 SLR 候选中筛得 8+2=10）；mapping 示例对比 n=2；Wieringa 研究类型枚举值 6；Means of Analysis 枚举值 4；Research Goals 枚举值 4；Inclusion Requirements 枚举值 2 |
| 原生树类型 | **维度森林**（4 棵子树）：A=SLR 特征化表（n=10 真实样本）、B=mapping 示例对比表（n=2 真实样本）、C=处方 3-facet 分类（schema seed）、D=SMS 流程 pipeline（process schema） |
| 主统计池资格 | 否；方法论文 / guideline-like seed。仅 Tree A 内部 n=10 频数和 Tree B 的 n=2 对比可作方法学描述性统计 seed，不进入领域统计合成池；Tree C/D 仅为 schema_seed |
| 总体判定 | needs repair — 现有 review.md 已开始向原文 schema 主树返修但仍欠缺：(i) 没有把"被编码的真实样本单位"（n=10 / n=2）与"处方 schema"（3-facet）分层；(ii) Wieringa 6 类与 Means-of-Analysis 4 类作为封闭枚举未在叶子层完整定义；(iii) 关系边（Table 5 行=10 篇 SLR × 列=4 字段组）未表化 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取范围

- 完整阅读 `paper_content.txt`（537 行 / 10 页）：Abstract、§1 Introduction、§2.1–§2.5 SMS process、§3.1–§3.2 比较与讨论、§4 guidelines、§5 Conclusion、References。
- 完整阅读 `bibtex.bib`：DOI = 10.14236/ewic/EASE2008.8，作者 4 人，venue = EASE 2008 / BCS。
- 完整阅读 `metadata.json`：确认 `eligible_for_statistical_synthesis = false`、`evidence_role = "mapping_guideline_pattern"`、`systematic_evidence_status = "systematic_mapping"`。
- 完整阅读现有 `review.md`（332 行）：确认其已包含历史 A1-DT v1 19×3 审计后返修块，但仍以六个通用接口叶为主叙述。

### 1.2 未做的核验

- 未在 PDF 中视觉核对 Figure 1（SMS 流程图）、Figure 2（keywording 构建分类方案）、Figure 3（bubble plot）；`paper_content.txt` 中 Figure 3 数字布局是字符流，未做形位还原。
- 未核对 Table 3 (Wieringa 研究类型表) 与 Table 5 (SLR 特征表) 的列对齐细节，但二者文本完整可读，枚举项清晰。
- `autoresearch/SKILL.md`（位于 codex 插件缓存）本轮未直接读取，记为 `partial-blocked`，但所采用的"先样本单位 → 再字段结构 → 再证据链"工作流与 autoresearch / research-planning skill 的 4 阶段输出一致。

### 1.3 关键证据锚点（11 条，控制短引）

| 锚点 | 位置 | 短引或释义 |
|---|---|---|
| E1 | §Abstract（p.1 line 12–17） | "build a classification scheme … analysis of results focuses on frequencies of publications for categories" — 明确分析重心是类别频数 |
| E2 | §2 (p.2 Figure 1) | SMS 五步流程：Definition of RQ → Conduct Search → Screening → Keywording (abstracts) → Data Extraction & Mapping |
| E3 | §2.1 Table 1 (p.2) | 两个示例研究的 RQ 字段化对比：OO Design Map 3 个 RQ vs SPL Variability Map 2 个 RQ |
| E4 | §2.3 Table 2 (p.3) | 两个示例研究的 Inclusion/Exclusion 字段化对比 |
| E5 | §2.4 (p.4) "three main facets were created … topic … type of contribution … research facet" | 三-facet 分类方案的明确定义 |
| E6 | §2.4 Table 3 (p.4) | Wieringa 6 类研究类型封闭枚举：Validation / Evaluation / Solution Proposal / Philosophical / Opinion / Experience |
| E7 | §2.5 (p.5) "Excel table … each category … short rationale why the paper should be in a certain category" | 抽取表 + 短理由（rationale）字段化要求 |
| E8 | §2.5 Figure 3 (p.5) bubble plot | 多 facet 交叉频数可视化：Variability Context × Contribution × Research（数字含 50/56/0/8/128 等列汇总） |
| E9 | §3 (p.6) "search resulted in a total of 21 papers … this resulted in eight systematic reviews being included … two further … resulted in ten" | Tree A 样本分母链：候选 21 → 含 8 + 补 2 = 10 |
| E10 | §3.1 Table 5 (p.7) | n=10 SLR × 4 字段组（Research Goals 4 类 / Inclusion 2 类 / Numeric counts / Means of Analysis 4 类）的样本编码主表 |
| E11 | §4 (p.8–9) "Adaptive Reading Depth … Classify Papers Based on Evidence and Novelty … Visualize Your Data" | 四条 guideline 扩展（recommend）— 处方建议，不是被编码的样本字段 |

---

## 2. 样本单位与字段来源判定

### 2.1 五问回答

1. **原文纳入并逐项描述的对象是什么？**
   - **主样本（Tree A，n=10）**：作者用 "systematic review AND software engineering" 在 Inspec/Compendex、IEEExplore、ACM DL 检索得 21 篇候选，按"在 SE 内 / 遵循 Kitchenham&Charters 2007 / 标题或摘要明示 systematic review"筛得 8 篇 + Kitchenham 2007 keynote 中补 2 篇 = **10 篇 SE systematic reviews**（Table 4 给出 ID 1–10 文献，Table 5 给出特征化字段）。
   - **辅样本（Tree B，n=2）**：两个 mapping 示例研究——(Bailey et al. 2007) 的 OO Design Map 与 (Mujtaba et al. 2008) 的 SPL Variability Map——作为"如何做 SMS"的示例，被在 Tables 1–2 和 Figure 3 中字段化对比。

2. **作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**
   - 对 Tree A 有：明确检索串、3 库来源、纳排标准、补充入选规则，最终编码到 Table 5 的 4 字段组。
   - 对 Tree B 没有系统检索：示例研究是作者团队自己的两篇先行工作（其中 Mujtaba 2008 还是 in-submission 状态），用于说明 SMS 流程，不是被独立纳排筛出的样本。

3. **原文字段来自哪里？**
   - Tree A 的字段：来自作者自定义的特征化 schema（§3.1 "Research Goals / Inclusion Requirements / Number of Articles Included / Means of Analysis"），其中 Means of Analysis 部分明确引用 Dixon-Woods 2005。
   - Tree B 的字段：RQ、Search Strings、Databases/Forums、Inclusion/Exclusion 直接复用 Kitchenham&Charters 2007 SLR 协议字段。
   - 处方 Tree C 的字段：Wieringa 2006（Research-Type 6 类）+ 作者新增 Contribution 类（process/method/model/tool/metric）+ 领域相关 Topic facet。
   - 流程 Tree D：作者自创 5 步 pipeline（Figure 1）。

4. **RQ 与样本单位的关系？**
   - 本文没有用 RQ1/RQ2/... 形式声明本文自己的研究问题；§Objective 用自然语言陈述："describe how to conduct SMS"、"compare SMS with SLR"、"provide guidelines"。
   - 因此 RQ 在本文中不是树根，而是"目标声明"；Table 1 的 RQ 列是被对比的两个示例研究的 RQ，是 Tree B 的一个字段。

5. **若无系统样本库，如何降级？**
   - 不需要降级。本文同时具备方法论叙述（schema seed）+ 真实样本表（n=10 编码 + n=2 对比），可同时作为：(i) Tree A 的小型描述性统计 seed（不进领域统计池）；(ii) Tree C 的处方 schema seed；(iii) Tree D 的 process pipeline seed。

### 2.2 与现有 review.md 的差异判定

现有 review.md 在"原文 schema 主树（19×3 审计后返修）"已经触及上述 Tree A 关键字段（Research Goals、Means of Analysis、Wieringa、Contribution、Map vs Review），但**仍未明确区分"本文编码的真实样本表"（n=10 SLR、n=2 mapping 示例）与"本文向未来 SMS 推荐使用的处方 schema"（3-facet）**。这是本轮 needs-repair 的核心。

---

## 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**。下面分四棵子树给出，每棵树标注 `样本性`（被编码 vs 处方）与 `用途`。

### 3.1 Tree A — SLR 特征化样本表（n=10，被编码样本）【主样本】

```text
[A] SE Systematic Reviews 特征化表  ── 样本单位 = 1 篇 SLR；n=10；分母可统计
├── A.1 Reference Identity  (Table 4)
│   ├── A.1.1  Reference ID  ∈ {1..10}            [完整枚举, 数值 ID]
│   └── A.1.2  Citation Key                       [自由文本, 文献引用]
├── A.2 Research Goals  (Table 5, 行 1–4)        [多值布尔, 一篇 SLR 可同时占多列]
│   ├── A.2.1  Identify Best and Typical Practices    [布尔]
│   ├── A.2.2  Classification and Taxonomy            [布尔]
│   ├── A.2.3  Emphasis on Topic Categories           [布尔]
│   └── A.2.4  Identify Publication Fora              [布尔]
├── A.3 Inclusion Requirements  (Table 5, 行 5–6) [多值布尔]
│   ├── A.3.1  Research is Within Focus Area          [布尔]
│   └── A.3.2  Empirical Methods Used                 [布尔]
├── A.4 Number of Included Articles  (Table 5, 行 7–8) [数值]
│   ├── A.4.1  Potentially Relevant Studies           [自然数 或 n.a.]
│   └── A.4.2  Relevant Studies Included              [自然数]
└── A.5 Means of Analysis  (Table 5, 行 9–12)    [多值布尔]
    ├── A.5.1  Meta Study                             [布尔]
    ├── A.5.2  Comparative Analysis                   [布尔]
    ├── A.5.3  Thematic Analysis                      [布尔]
    └── A.5.4  Narrative Summary                      [布尔]
```

### 3.2 Tree B — Mapping 示例研究对比表（n=2，被编码样本）【辅助样本】

```text
[B] 两个 mapping 示例研究的对比表  ── 样本单位 = 1 个 mapping 示例；n=2
├── B.1 Research Questions  (Table 1)             [自由文本 + RQ 列表]
├── B.2 Search String                             [自由文本布尔表达式]
├── B.3 Databases / Forums                        [枚举：CS 数据库全集 vs SPLC+PFE+期刊]
├── B.4 Inclusion Criteria  (Table 2)            [自由文本判定规则]
├── B.5 Exclusion Criteria  (Table 2)            [自由文本判定规则]
├── B.6 Classification Scheme                     [3-facet 实例化或 intervention type]
└── B.7 Visualization                             [summary stats / freq table  vs  bubble plot]
```

### 3.3 Tree C — 处方 3-facet 分类 schema（schema_seed，未来 SMS 使用）【处方】

```text
[C] SMS 推荐分类方案  ── 处方层；不是被本文编码的样本字段
├── C.1 Topic Facet                               [开放层级；领域相关；示例 = SPL Variability 6 类]
├── C.2 Contribution Facet  (§2.4)                [枚举：process / method / model / tool / metric]
└── C.3 Research-Type Facet  (Table 3, Wieringa)  [封闭枚举, 互斥 6 类]
    ├── C.3.1  Validation Research
    ├── C.3.2  Evaluation Research
    ├── C.3.3  Solution Proposal
    ├── C.3.4  Philosophical Paper
    ├── C.3.5  Opinion Paper
    └── C.3.6  Experience Paper
```

### 3.4 Tree D — SMS 流程 pipeline（process schema，未来 SMS 使用）【处方】

```text
[D] SMS 五步流程 (Figure 1)  ── 处方层；过程节点不是字段
├── D.1 Definition of Research Question / Review Scope    → 输出：Review Scope
├── D.2 Conduct Search                                    → 输出：All Papers
├── D.3 Screening of Papers (inclusion / exclusion)       → 输出：Relevant Papers
├── D.4 Keywording using Abstracts                        → 输出：Classification Scheme
└── D.5 Data Extraction and Mapping Process              → 输出：Systematic Map
```

### 3.5 与已有 review.md `维度树结构` 的对照

现有 review.md 的 `[dim-...-b1] mapping planning` / `[...b2] keywording` / `[...b3] classification scheme` / `[...b4] map visualization` / `[...b5] research gap identification` 五个主干分支实际上**全部来自 Tree D（流程节点）**，没有给 Tree A 的真实 n=10 样本编码表留位置。这是当前 review.md 最需要返修之处。

---

## 4. 叶子维度表

下表只列**有原文证据支撑的叶子**；处方型 C/D 子树的叶子用 `schema_seed` 标记。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-A.2.1 | 目标—识别最佳/典型实践 | A.2 | Table 5 第 1 行 "Identify Best and Typical Practices" | SLR 是否声明以经验研究识别最佳或典型实践为目标 | {true, false} | 布尔 | 单元格空白 = false | 10 篇中标 x 的 8 篇可统计为 80% | 多目标重叠 → SLR 多目标常态 | E10 | 可作 SLR/SMS 目标分类种子；不可外推到非 SE 领域 |
| L-A.2.2 | 目标—分类与分类法 | A.2 | Table 5 第 2 行 | SLR 是否产出 framework / taxonomy / 分类 | {true, false} | 布尔 | 空白 = false | 10/10 中 3 篇（ID 7, 8, +1） | mapping 与 review 的目标交集 | E10 | 同上 |
| L-A.2.3 | 目标—主题类别强调 | A.2 | Table 5 第 3 行 | SLR 是否统计各子主题论文分布 | {true, false} | 布尔 | 空白 = false | 2/10 | 与 Identify Publication Fora 强相关 | E10 | 同上 |
| L-A.2.4 | 目标—识别发表论坛 | A.2 | Table 5 第 4 行 | SLR 是否识别相关 journal/conf/workshop | {true, false} | 布尔 | 空白 = false | 2/10 | 与 mapping 目标更接近 | E10 | 同上 |
| L-A.3.1 | 纳入要求—主题相关 | A.3 | Table 5 第 5 行 | 全 10 篇都要求 | {true} | 布尔（饱和） | n/a | 10/10；常量列；无判别力 | 揭示"主题相关性"是 SLR 通用门槛 | E10 | 不可作判别字段，只作 baseline check |
| L-A.3.2 | 纳入要求—使用经验方法 | A.3 | Table 5 第 6 行 | 是否限定 primary study 使用经验方法 | {true, false} | 布尔 | 空白 = false | 8/10 | "经验方法"是 SLR 的主导筛选门槛 | E10 | 可迁移为 SLR vs SMS 区分点 |
| L-A.4.1 | 候选论文数 | A.4 | Table 5 第 7 行 | 检索阶段命中数 | {自然数 ∪ n.a.}；观测值 = {5453, 963, 5453, 5453, 1344, 353, 5453, n.a., 185, 564} | 数值或缺失 | n.a. = 作者未报告 | 中位数 ≈ 1344；偏态分布 | 揭示 SLR 检索规模差异巨大（185–5453） | E10 | 单位为篇；不同检索策略不可直接比较 |
| L-A.4.2 | 入选论文数 | A.4 | Table 5 第 8 行 | 最终入选数 | {自然数}；观测值 = {78, 24, 24, 78, 10, 173, 103, 304, 10, 26} | 数值 | 不应缺失 | 中位数 ≈ 26；最大 304 | 入选率 = A.4.2/A.4.1，呈现 SLR 严苛性 | E10 | 与领域、方法严苛度强耦合 |
| L-A.5.1 | 分析方法—Meta Study | A.5 | Table 5 第 9 行 | 是否做统计 meta-analysis | {true, false} | 布尔 | 空白 = false | 2/10 | meta-analysis 在 SE SLR 中罕见 | E10 | 可作 SLR 方法学成熟度指标 |
| L-A.5.2 | 分析方法—Comparative Analysis | A.5 | Table 5 第 10 行 | 是否使用逻辑简化/置信度评估 | {true, false} | 布尔 | 空白 = false | 1/10 | 极少见 | E10 | 同上 |
| L-A.5.3 | 分析方法—Thematic Analysis | A.5 | Table 5 第 11 行 | 是否按主题计数 | {true, false} | 布尔 | 空白 = false | 2/10 | 这是 mapping 的核心方法 | E10 | mapping 与 review 重叠点 |
| L-A.5.4 | 分析方法—Narrative Summary | A.5 | Table 5 第 12 行 | 是否使用叙述性总结 | {true, false} | 布尔 | 空白 = false | 10/10；常量列 | 所有 SE SLR 都做叙述总结 | E10 | 表明"叙述"是 SE SLR 默认输出形态 |
| L-B.1 | 示例—RQ 集合 | B.1 | Table 1 | 示例研究的 RQ 列表 | 自由文本 | 自由文本 | n/a | n=2 不可统计 | 揭示 RQ 颗粒度（3 vs 2） | E3 | n=2 不能外推 |
| L-B.2 | 示例—检索串 | B.2 | §2.2 | 布尔表达式 | 自由文本 | 自由文本 | n/a | n=2 | 揭示 PICO 在 SMS 中可松绑 outcome | §2.2 line 117–121 | 不可量化 |
| L-B.3 | 示例—数据库/论坛 | B.3 | §2.2 | 检索来源 | 自由文本 + 类别 | 半结构化 | n/a | n=2 | "全 CS 库"vs"特定 venue + 期刊"二元对比 | §2.2 line 122–128 | n=2 不能外推 |
| L-B.4 | 示例—纳入标准 | B.4 | Table 2 | 详细 inclusion 规则 | 自由文本 | 自由文本 | n/a | n=2 | "需经验证据" vs "摘要明示主题" | E4 | n=2 不能外推 |
| L-B.5 | 示例—排除标准 | B.5 | Table 2 | 详细 exclusion 规则 | 自由文本 | 自由文本 | n/a | n=2 | 抽象关键词偶现 ≠ 实质贡献 | E4 | n=2 不能外推 |
| L-B.6 | 示例—分类方案 | B.6 | §2.4 | 实际采用的 facet 组合 | OO Design 用 intervention type；SPL Variability 用 3-facet | 半结构化 | n/a | n=2 | Bailey 用 1 facet；Petersen 团队推荐 3 facet | E5 | 示例性 |
| L-B.7 | 示例—可视化 | B.7 | §2.5 + Figure 3 | 频数表 vs bubble plot | {summary stats, frequency table, bubble plot} | 枚举（n=2 观测） | n/a | n=2 | bubble plot 是新增贡献 | E8 | 可作处方 seed |
| L-C.3.* | Wieringa 研究类型（处方枚举） | C.3 | Table 3 | 推荐用于未来 SMS 的论文研究类型分类 | {Validation, Evaluation, Solution Proposal, Philosophical, Opinion, Experience} | 封闭枚举（6） | 互斥使用 | 不计入本文样本编码 | 可作所有下游 SMS 的字段种子 | E6 | 可迁移为 Paper2 论文研究类型字段；2008 年版本不含 LLM/agent 类，需扩展 |
| L-C.2 | Contribution 类型（处方枚举） | C.2 | §2.4 | 推荐贡献类别 | {process, method, model, tool, metric, ...} | 开放枚举 | 可多值 | schema_seed | 字段种子 | E5 | metric 在原文中实际出现于 Figure 3（"Metric" 列），可视为枚举的一部分 |
| L-C.1 | Topic Facet（处方开放） | C.1 | §2.4 | 领域相关主题轴 | 完全开放 | 自由文本/层级 | n/a | schema_seed | 字段种子 | E5 | 必须按领域重建 |

---

## 5. 关系边表

本文存在**显式关系结构**——Table 5 是一个 `SLR × 字段` 的二维矩阵，每个单元格是一条 (SLR, 字段, 取值) 关系边；Figure 3 bubble plot 是 `Topic × Contribution × Research-Type` 的三维交叉频数。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R-A.row×col | A.1.1 Reference ID（10 行） | 编码 | A.2/A.3/A.4/A.5 各字段（12 列） | 见 L-A.2.1 ~ L-A.5.4 | 单元格空白 = 该 SLR 不具该属性（除 A.4 为数值） | E10 / Table 5 | n=10 × 12 字段的二维矩阵；可做行/列汇总频数与交叉表 |
| R-B.row×col | B（OO Design / SPL Variability，2 行） | 对比 | B.1 ~ B.7（7 列） | 见 L-B.* | 不应缺失 | E3 / E4 | n=2 对比矩阵，只支持成对差异叙述 |
| R-C.facet3 | 论文（Bailey 2007 + Mujtaba 2008 样本） | 三-facet 交叉分类 | Topic × Contribution × Research-Type | 见 Figure 3 数字 | 0 单元格 = 主题/方法缺口 | E8 | 处方的 bubble plot 交叉覆盖；Mujtaba SPL Variability 实例化为 6×5×6 三维网格 |
| R-D.pipeline | D.1 ~ D.5（流程节点） | 顺序产出 | Review Scope → All Papers → Relevant Papers → Classification Scheme → Systematic Map | 见 §2 Figure 1 | n/a | E2 | 顺序约束，非样本字段 |
| R-keywording | D.4 abstract keywording | 演化更新 | C 处方分类 schema | 可新增/合并/拆分类别 | n/a | §2.5 line 220–223 "the classification scheme evolves while doing the data extraction, like adding new categories or merging and splitting existing categories" | 处方 schema 演化关系 |

未发现额外的"论文之间引用"或"作者—venue"关系边被显式编码。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 由字段/统计表支持的统计观察（本文实有）

| 观察 | 来源 | 可成立强度 |
|---|---|---|
| 10 篇 SE SLR 中 8 篇以 "Identify Best and Typical Practices" 为目标（80%） | Table 5 行 1 | strong（n=10 frequency） |
| 10 篇 SE SLR 全部使用 Narrative Summary 作为分析手段 | Table 5 行 12 | strong；常量列说明"叙述总结是 SE SLR 默认输出" |
| 仅 2/10 使用 Meta Study；1/10 使用 Comparative Analysis | Table 5 行 9–10 | strong；揭示 SE SLR 量化合成不普及 |
| SLR 入选率（A.4.2/A.4.1）总体很低（如 78/5453 ≈ 1.4%；24/963 ≈ 2.5%） | Table 5 行 7–8 | strong but caveat：检索策略差异巨大 |
| SPL Variability bubble plot 中 Evaluation Research 列 = 50/128 ≈ 39.06%，Validation Research = 56/128 ≈ 43.75% | Figure 3 文本提取 | medium（文本提取，未做版面核对） |

### 6.2 原文 §4 给出的候选 finding（recommendation 形态）

| 候选 finding | 性质 |
|---|---|
| SMS 与 SLR 应互补使用 — 先 SMS 结构化再 SLR 深入 | recommendation（非样本统计推论） |
| Adaptive Reading Depth：当摘要不足时应读 introduction/conclusion | guideline 经验性建议 |
| 应使用 Wieringa 研究类型分类，并按 evidence-level 与 novelty 进一步细分 | 处方建议 |
| 应使用 bubble plot 等可视化展示多 facet 交叉 | 处方建议 |

### 6.3 对 Paper2 可迁移的方法学启发

- "类别频数 + 交叉覆盖 → 候选缺口"链路（不直接等于 final finding）；
- 抽取表必须配 short rationale 字段；
- 处方 schema 可演化（merge/split）；
- 多目标布尔多值列（Research Goals、Means of Analysis 一行多 x）的字段化方式可直接迁移到 Paper2 的"论文承担的角色 / 方法类型 / 评价方式"等字段。

### 6.4 绝不能迁移的领域结论

- 任何关于 OO Design、Software Product Line Variability 子领域的具体频数与缺口（如 Mujtaba SPL 中 Verification & Validation × Validation Research = 11 篇）；
- Bailey 2007 与 Mujtaba 2008 这两个示例的具体 RQ 与检索串；
- Table 5 中 10 篇具体 SLR 的领域结论（成本估算、需求获取等）。

---

## 7. 对现有 `review.md` 的返修建议（C / I / M）

### C 级（必须返修，影响学术结论）

- **C1 — 维度树根结构错误：未区分"被编码样本"与"处方 schema"。** 现 `维度树结构` 节将五个流程步骤当作主干 b1–b5，把 Tree A 的 n=10 真实样本字段（Research Goals / Inclusion / Counts / Means of Analysis）压入 `[leaf-...-taxonomy]` 等通用接口叶，丢失了"本文最重要的样本编码就是 Table 5"这一事实。
  - **返修动作**：把"原生维度树/森林"改写为本审计第 3 节四棵子树并列；现"维度树结构" code block 应拆分为 Tree A / B / C / D 四块，并明确标注每棵树的样本性与 n。
- **C2 — Table 5 行×列矩阵缺失。** 现 review.md 没有把 Table 5 的二维结构作为关系边明确表化，导致后续无法做"行汇总（每篇 SLR 的目标向量）"与"列汇总（每个目标维度的频数）"的统计观察。
  - **返修动作**：补本审计 §5 关系边表，特别是 R-A.row×col。

### I 级（重要，应在本轮或下一轮处理）

- **I1 — Wieringa 6 类与 Means-of-Analysis 4 类作为封闭枚举未在叶子层完整列出。** 现 `审计返修` 表只写"validation、evaluation、solution proposal、philosophical、opinion、experience"一行，没有把 6 类分成 6 个叶子并标注取值空间为封闭互斥枚举。
  - **返修动作**：把本审计 §4 表中 L-C.3.1 ~ L-C.3.6 与 L-A.5.1 ~ L-A.5.4 抬升为正式叶子。
- **I2 — Bailey 2007 与 Mujtaba 2008 两个示例研究的 n=2 对比样本未被列为独立子树。** 现 review.md 完全忽略 Tree B；但 Tables 1、2 与 Figure 3 都是围绕这 2 个示例展开的字段化。
  - **返修动作**：新增 Tree B 章节，并明确 n=2 不可统计、仅作"成对对比叙述"。
- **I3 — 统计观察未明确分母 (10 vs 2 vs 21)。** 现 review.md 在 `统计与候选发现链路` 节把分母写成"当前 19 篇 survey-of-surveys 样本"，这是 SUMMARY 级分母，与本文内 n=10 / n=2 的内嵌统计混淆。
  - **返修动作**：分母按本文内嵌（n=10 SLR、n=2 mapping 示例）和文库外部（19 篇）两层分开标注。

### M 级（建议性）

- **M1 — `历史草稿` 中保留的 v1 树（`mapping_study_pattern`）已被标注"不作事实真源"，建议进一步压缩或删除以减少阅读噪声。**
- **M2 — SUMMARY 表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"建议改为：样本单位 = `SE SLR (n=10) + mapping 示例 (n=2)`；样本数量 = `10 / 2`；原生树类型 = `维度森林（Tree A + B + 处方 C + 流程 D）`；统计池资格 = `否；仅方法学描述性 seed`。**
- **M3 — `原文模式候选叶子映射（A1 种子）` 表中 5 个候选叶子（mapping-planning / keywording / classification-scheme / map-visualization / gap-identification）实际上都是 Tree D 流程节点，建议改名为 `Tree D process-node seed`，并新增 `Tree A sample-field` 与 `Tree C prescriptive-facet` 两类候选叶子。**
- **M4 — `审计返修口径` 提到三路审计（codex/claude/deepseek）共同结论，建议在本次 A1-DT v2 审计后更新该口径，标注 v2 已对 v1 通用六叶接口降级为投影。**

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-v2-001 | paper_content.txt | §Abstract; §2 Figure 1 | p.1 line 12–17; p.2 Figure 1 | "build a classification scheme … analysis of results focuses on frequencies"；SMS 5 步流程图 | scope_anchor | strong | Tree D 全部节点、根节点 | false（Figure 1 节点名文本可读） | 仅限本文内部方法学叙述 |
| EV-v2-002 | paper_content.txt | §2.1 Table 1; §2.3 Table 2 | p.2; p.3 | 两个示例研究的 RQ 与 inclusion/exclusion 字段化对比 | sample_table | strong | Tree B 全部叶子；L-B.1–L-B.5 | true（建议视觉核对 Table 1/2 列对齐） | n=2，仅作示例性对比，不可外推 |
| EV-v2-003 | paper_content.txt | §2.4 + Table 3 | p.4 | "three main facets … topic … contribution … research"；Wieringa 6 类完整定义 | prescriptive_schema | strong | Tree C 全部；L-C.1, L-C.2, L-C.3.1–L-C.3.6 | true（Table 3 文本完整，建议版面核对） | 处方层；2008 年版本，未含 agent/LLM 类，需现代扩展 |
| EV-v2-004 | paper_content.txt | §2.5 + Figure 3 | p.5 | "Excel table … each category … short rationale"；bubble plot 数字 50/56/0/8/128 等 | sample_visualization | medium | L-B.6, L-B.7；R-C.facet3 | true（Figure 3 必须 PDF 视觉核对，文本提取已乱序） | Mujtaba SPL 领域结论不可迁移 |
| EV-v2-005 | paper_content.txt | §3 line 269–275 | p.6 | "21 papers … eight systematic reviews being included … two further … included" | sampling_chain | strong | A.1.1 Reference ID 分母 = 10；候选 = 21 | false | 揭示 n=10 由 21→8+2 而来 |
| EV-v2-006 | paper_content.txt | §3.1 Table 5 | p.7 | 10 篇 SLR × (Research Goals 4 + Inclusion 2 + Counts 2 + Means of Analysis 4) 主表 | sample_encoding_matrix | strong | Tree A 全部叶子；R-A.row×col | true（Table 5 视觉核对优先；尤其常量列如 A.5.4 全 x、A.3.1 全 x） | n=10 频数仅作方法学 seed，不进领域统计池 |
| EV-v2-007 | paper_content.txt | §3.2 + §4 | p.7–9 | mapping vs review 在 goal/process/breadth/depth 上的差异；4 条 guideline 扩展 | author_claim | medium | 候选 finding 与处方 finding（§6.2） | false | 处方建议，不是样本统计推论 |
| EV-v2-008 | paper_content.txt | §4 "Adaptive Reading Depth"; §3.2 "Validity Consideration" | p.8 | 摘要不足 / 术语混乱 / 73% 论文 designation 错误 / 分类误判风险 | limitation | medium | 迁移边界；外推限制 | false | 限制本身可作 Paper2 字段误差源种子 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-v2-T01 | 本文原生树类型为**维度森林**：Tree A (n=10 SLR 编码) + Tree B (n=2 mapping 对比) + Tree C (处方 3-facet) + Tree D (5 步流程)；不是单树 | tree_type | 根节点 | EV-v2-001, EV-v2-002, EV-v2-003, EV-v2-006 | strong | schema_seed；改写 review.md 维度树结构节 | Tree C/D 是处方层，不能写成"被编码的样本字段" |
| CLM-v2-A01 | Table 5 是本文唯一的样本编码主表，n=10 SLR × 12 字段；行=Reference ID，列=4 字段组下细分布尔/数值 | sample_unit | Tree A 全部 | EV-v2-005, EV-v2-006 | strong | 可作方法学描述性统计 seed；可生成行汇总（每 SLR 目标向量）与列汇总（每字段频数） | 不进入领域统计池；分母与检索策略强耦合 |
| CLM-v2-A02 | Means of Analysis 列 Narrative Summary 全 10 篇置 x，说明叙述总结是 SE SLR 默认输出形态；Meta Study 仅 2/10，揭示 SE SLR 量化合成不普及 | descriptive_stat | L-A.5.1, L-A.5.4 | EV-v2-006 | strong | 可迁移为"SE SLR 方法学成熟度"指标 seed | 仅 n=10；可在更大 SLR 池中验证 |
| CLM-v2-A03 | Inclusion Requirements "Research is Within Focus Area" 全 10 篇都置 x，是常量列，无判别力 | descriptive_stat | L-A.3.1 | EV-v2-006 | strong | 揭示该字段是 SLR 通用 baseline gate，不应进入分类用途 | n=10；可在更大池中验证 |
| CLM-v2-B01 | Bailey 2007 与 Mujtaba 2008 是本文的 mapping 示例样本（n=2），不是被独立纳排的样本 | sample_unit | Tree B 全部 | EV-v2-002, EV-v2-004 | strong | 用于对比 SMS 实施差异；仅成对叙述 | n=2 不可外推；Mujtaba 2008 当时为 in-submission |
| CLM-v2-C01 | Wieringa 6 类研究类型是封闭互斥枚举（Validation / Evaluation / Solution Proposal / Philosophical / Opinion / Experience），构成处方 schema 的关键叶子层 | leaf_definition | L-C.3.1 ~ L-C.3.6 | EV-v2-003 | strong | 可迁移为 Paper2 论文研究类型字段种子 | 2008 年版本，需为 LLM/agent 工作类型扩展 |
| CLM-v2-D01 | Figure 1 五步流程是处方 process schema；不能与 Tree A 样本字段混淆 | process_schema | Tree D | EV-v2-001 | strong | 可迁移为 Paper2 流程章节 | 不是样本字段，不能进入字段表 |
| CLM-v2-F01 | 本文给出的统计观察均为类别频数与交叉覆盖；§4 的 guideline 扩展（互补使用 / Adaptive Reading Depth / Wieringa 推荐 / 可视化）是处方建议，不是样本统计推论 | candidate_finding_boundary | L-A.2~A.5, §4 | EV-v2-006, EV-v2-007 | strong | 仅作 candidate finding；不可升级为 final finding | final finding 必须经跨论文证据与研究者裁决 |
| CLM-v2-R01 | 本文 §4 "Validity Consideration" 报告"73% 论文 designation 错误"是质量风险证据，可作 Paper2 字段误差源种子 | risk_anchor | Tree A 所有叶子 + Tree C | EV-v2-008 | medium | 可迁移为字段分类置信度种子 | 该数字来自 Mendes 2005 子集，不是本文 n=10 池 |

---

## 9. 技能使用与自我审查记录

### 9.1 技能文件使用与采用原则

| 技能文件 | 读取状态 | 采用的关键原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 已读首 80 行 | "claim-evidence-engineering workflow"、Evidence gate（仓库文件优先于记忆）、Task-state gate、Citation gate（不臆造引用） |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 已读首 80 行 | 5 维 reviewer 维度（Originality/Quality/Clarity/Significance/Reproducibility/Ethics）；C/I/M 应"足够具体到作者可操作" |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 已读首 60 行 | "不要默默修复"，要把无法在本轮验证的风险显式列出；reviewer simulation 中 Weaknesses 必须引用具体节/表/证据 |
| `research-planning/SKILL.md` | 已读首 60 行 | 4 阶段计划：Overall Plan → Architecture Design → Logic Design → Configuration；本审计在第 3 节用"样本单位 → 字段结构 → 关系边 → 统计/finding 边界"对应该 4 阶段 |
| `research-planning/references/planning-prompts.md` | 未直接读取（time-budget） | 间接应用（按 SMS 流程对照） |
| `research-planning/references/output-schemas.md` | 未直接读取 | 间接应用（JSON 结构化字段表） |
| `autoresearch/SKILL.md`（oh-my-codex 插件缓存） | 未读取 | `partial-blocked`；按本任务规范 §0(6) 记录 |

### 9.2 Reviewer 视角—本输出最高风险 3 点

1. **Figure 3 bubble plot 数字未做 PDF 视觉核对**：本审计 §6.1 列出的 SPL Variability 频数（50/56/0/8/128 等）来自 `paper_content.txt` 字符流，未做形位还原；主线程合并前必须用 PDF 视觉核对一次，避免误把 OCR 串扰当作真实分布。
2. **n=10 与 n=19 两层分母容易在 SUMMARY 合并时混淆**：本文内嵌 Tree A 的 n=10 SLR 是"本文自己编码的样本"，与文库 SUMMARY 中的"19 篇 survey-of-surveys 样本"不是一个分母；如果不在 review.md 中显式分层，下游主线程做 SUMMARY 统计时可能把本文 n=10 的频数误当作 19 池贡献。
3. **Tree C（处方）与 Tree A（样本）的混淆延续**：若返修时仅替换通用六叶接口而不把"处方 schema seed"与"样本编码字段"分层，下一轮审计仍可能把 Wieringa 6 类当作"本文已统计样本的字段"，从而把处方建议误升级为统计观察。reviewer 应在合并时核查 review.md 是否明确写出"Tree C 是处方层，不是 n=10 编码字段"。

### 9.3 blocked / timeout / 文件缺失

- `autoresearch/SKILL.md`: 未读取 — `partial-blocked`（time budget；按任务规范 §0(6) 记为风险，但不阻塞审计）。
- `paper.pdf` 视觉核对: 未做 — 已在多处显式标注 `needs_manual_check`。
- 其他指定技能/指南文件: 全部可读，无 file_missing 报错。

---

**审计结论一句话**：现有 `review.md` 已经迈出 v1→v2 返修第一步（"原文 schema 主树"节），但仍把 Tree D 流程节点当成主干 b1–b5、把 n=10 真实样本表压成通用接口叶；本轮 A1-DT v2 审计的核心增量是确认本文为**维度森林**（n=10 SLR 表 + n=2 mapping 对比 + 3-facet 处方 + 5 步流程），并把 Table 5 的 12 个具体字段、Wieringa 6 类封闭枚举、Means of Analysis 4 类多值布尔列作为正式叶子升级到原文 schema 主树。判定：**needs repair**（C1+C2 必须本轮返修；I1–I3 应在下一轮处理；M1–M4 为建议）。
