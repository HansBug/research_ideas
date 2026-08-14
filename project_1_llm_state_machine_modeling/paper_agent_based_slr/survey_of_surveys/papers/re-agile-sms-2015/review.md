# A Mapping Study on Requirements Engineering in Agile Software Development

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | A Mapping Study on Requirements Engineering in Agile Software Development |
| 年份 | 2015 |
| 出版形态 | 会议 |
| 期刊/会议/预印本 | [SEAA](https://dsd-seaa.com/) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| CCF 复核状态 | 本轮未定位 CCF 目录条目 |
| 综述类型大类 | 🟦 SMS |
| 细分类型 / 原文自称 | SMS；Agile RE 原始研究 |
| 本文角色 | 🔵 类SLR |
| 统计池资格 | 🟢 入池 |
| 证据成熟度 | 🟡 全文 |
| 样本单位 / 分母链 | 📄 原研 / 28 |
| 原生维度树类型 | 🕸️ 关系树 |
| 来源等级 | Euromicro SEAA 2015；非 A / 一般国际会议；作者/机构镜像 PDF |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| SE 子领域 | Agile Requirements Engineering |
| A1 角色 | SMS 样本，用于验证 系统映射研究 与 tertiary study 的字段差异。 |
| 是否目标证据池 | 否。 |
| schema 历史观察 | 暴露 系统映射研究 更关注 taxonomy / benefit / problem / solution，而不一定有质量评价或 effect synthesis。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 目标是理解 agile RE 现象，识别定义、benefits、problems、solutions。 | `paper_content.txt` Page 1 摘要。 | 可迁移为 系统映射研究 的 broad exploratory RQ。 | SMS 探索性 RQ 不等同于效果评价型 SLR RQ。 |
| dimension pattern | 维度包括 benefits、problem areas、proposed solutions、user story、prioritization、technical debt、customer representatives 等。 | `paper_content.txt` Page 1 摘要。 | 可迁移为 taxonomy / issue / solution 字段。 | benefit/problem/solution 适合 agile RE，目标主题需重建分类轴。 |
| finding pattern | 发现包括 agile RE 定义模糊、benefits、problem areas 和 proposed solutions。 | `paper_content.txt` Page 1 摘要。 | 可迁移为“mapping 发现常是主题图谱 + 问题清单”。 | mapping finding 偏主题图谱，不能直接升级为因果或效果结论。 |
| evidence presentation pattern | 使用 28 articles 的研究分母和分类分析。 | `paper_content.txt` Page 1 摘要。 | 可迁移为小规模 SMS 表格。 | 28 篇短样本分母较小，不能支撑全域饱和判断。 |
| validity / threat pattern | 原文已定位 V.D Limitations；主要限制是仅使用 Scopus、检索词范围有限，额外数据库或关键词可能发现更多文章。 | `paper_content.txt` Page 1--9。 | 作为“不足 / 待核验”降级样例。 | 原文有 V.D Limitations，但未报告多研究者筛选/编码裁决、一致性或 QA 协议。 |
| report structure pattern | Introduction → Background / Method → Results → Discussion / Conclusion 的短会论文结构。 | `paper_content.txt` Page 1--9。 | 可迁移为 SMS 短文结构。 | 短会论文结构不能代表完整 SMS 报告标准。 |

## 3. 对 PR-A1 schema 的启发

1. SMS 类型应允许 exploratory RQ，不要求 PICO 或技术效果问题。
2. 需要 `taxonomy_axis` 与 `problem_solution_pattern` 等维度候选；benefit、problem、solution 先作为取值或子类，A2a 再决定是否拆为独立字段。
3. validity/threat 需区分：原文有 V.D Limitations，但只覆盖 Scopus 单库与检索词限制；不能脑补多研究者裁决或一致性机制。

## 4. 待复核

- PDF 来自作者/课程镜像，不是出版社直链；正式引用仍以 DOI 为准。
- 表格和分类轴需 PDF 核对后才能进入 A2a 统计。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 将 Agile Software Development 中的 Requirements Engineering 定义为系统映射主题。 | 可迁移子领域化 SMS scope 设定。 |
| A1-M1 语料收集与纳排 | 提供 SMS 检索、筛选和研究分类流程。 | 可迁移为 mapping-study 概览字段。 |
| A1-M2 研究对象与主题语义 | benefit / problem / solution taxonomy 是清晰的主题语义样本。 | 可迁移问题-方案字段模式，不迁移 Agile RE 结论。 |
| A1-M3 方法 / 技术 / 干预 | 方案分类可作为 intervention / practice taxonomy 样式。 | 需 A2a 用更多 SMS 样本验证。 |
| A1-M4 评价、证据与复现资产 | 用分类表和研究分布支撑结论。 | 表格数值正式引用前需核对。 |
| A1-M5 统计分析就绪 | 系统映射的分布统计适合生成 topic / solution coverage。 | 只能支撑候选观察。 |
| A1-M6 research finding 形成与裁决 | 从 benefit/problem/solution 分布形成研究空白。 | 可迁移 finding heuristic。 |

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__codex.md](../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__codex.md)、[../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__claude.md](../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__claude.md)、[../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__deepseek.md](../../audits/a1dt-v2-19x3/results/re-agile-sms-2015__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/re-agile-sms-2015.md](../../audits/a1dt-v2-19x3/adjudications/re-agile-sms-2015.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `re-agile-sms-2015` |
| 审计代理 | `claude` (Opus 4.7 / 1M) |
| 是否已读 `paper_content.txt` | 是。已完整阅读全文 954 行（Page 1–9）。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`metadata.json` 已确认 review_type=SMS, eligible_for_statistical_synthesis=true；`bibtex.bib` 提供 DOI 10.1109/SEAA.2015.70。 |
| 是否打开或核对 `paper.pdf` | 否。仅基于 `paper_content.txt` 完成文本级审计；表 I–V 的版面、对齐、上下角标和数字单元格需 A2a 在 PDF 上视觉核验。 |
| 原文类型 | 系统映射研究 (SMS)，作者明确依据 Kitchenham & Charters [18] 自我标定为 系统映射研究。 |
| 被编码样本单位 | 原始研究（28 篇敏捷 RE 原始研究，编号 S1–S28）。 |
| 样本数量 / 分母 | 241（搜索命中）→ 187（去除非 journal/conference 与非英文）→ 65（标题/摘要筛选后）→ **28**（全文筛选后的最终纳入数 = 主统计分母）。 |
| 原生树类型 | 维度森林 + 关系边：四个并列主干（venue/context/article-type/benefit/problem-solution），其中 problem→solution 为显式关系 模式。 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

实际读取文件与范围：
- `paper_content.txt`：Page 1–9 全文 954 行，含 Abstract / I. Introduction / II. Background (A/B/C) / III. Methodology / IV. Results (A/B/C/D) / V. Discussion (A/B/C/D) / VI. Conclusion / References [1]–[26] / Primary Sources [S1]–[S28]。
- `bibtex.bib`、`metadata.json`：用于元信息核验。
- `review.md`：当前 v1 审计后的产物，作为返修对象。
- 未开 `paper.pdf`：本轮所有"表 X 行/列"事实仅基于 text 提取；Table II/III/IV/V 的 `Articles` 单元格在 text 提取中已被原样保留，但**编号顺序、对齐、合并单元格、缺失逗号**等需 PDF 视觉核验后才能升级为 `pdf_verified`。

关键原文证据锚点（按章节序）：

1. **三个显式 RQ**：Page 1 I. Introduction 段 "The overall research questions ... 1) What has been researched ... 2) What are the reported key benefits ... 3) What are the reported problems and corresponding solutions ..."。
2. **检索分母链条**：Page 3 III. Methodology "Scopus ... September 2014 ... 241 results ... 46 ... 8 ... 187 ... 123 excluded ... 65 ... 37 excluded ... remaining 28 articles"，含完整 search string `TITLE-ABS-KEY(("requirements analysis" OR "requirements engineering") AND (agile OR scrum)) AND NOT KEY("agile manufacturing")`。
3. **抽取协议**：Page 3 末段 "article metadata, context, 方法 and results were extracted ... categorized under the following four subject areas: Definition of RE in the agile context, benefits ... problems ... solutions"。
4. **Table I venue 分布**：Page 3 "会议 proceedings N=15 ≈53%, 期刊 N=8 ≈29%, 杂志 N=5 ≈18%"，venue 名包含 AREW(2)/RE(3)/IEEE Software(5) 等。
5. **Table II agile-方法 context**：Page 4 "Unspecified agile N=20 (71%); Scrum N=7; FDD N=1"。
6. **Table III article-type**：Page 4 "Multiple case study 6 / Single case study 5 / Experience 报告 3 / Tool eval 1 / Method eval 2 / Method 提案 8 / Position paper 3"。
7. **Table IV B1–B6 封闭枚举**：Page 5 含完整六类 benefit 名称、对应 S 编号集合（如 B2 = [S2,S3,S4,S7,S18,S23]）。
8. **Table V P1–P6 封闭枚举**：Page 6 含完整六类 problem 与对应 S 编号集合（如 P1 = [S4,S7,S12,S18,S22,S23]）。
9. **problem→solution 本地复原关系模式**：Page 5–6 在 P1/P2/P5 后给出 solution 段，P3/P4/P6 后明确 "未提出解决方案 to PX were proposed in the articles"；这是本地从 prose 复原的关系边，不是原文 formal relation table。
10. **作者综合 发现 与定义**：Page 7 V.B "Towards a definition of agile RE" 给出作者自造定义；V.C/V.D 给出 缺口（gap） 与 limitation。

### 2. 样本单位与字段来源判定

1. **被编码对象**：28 篇原始研究（原始研究；首次术语, S1–S28），逐篇被作者抽取并归到 venue / context / article-type / definition / benefit set / problem set / solution set。
2. **是否系统**：是。Page 3 完整给出 Scopus 数据库、search string、时间窗（Sep 2014）、纳排标准（5 条 title/abstract + 3 条 完整-text）、分母链条 241/187/65/28，符合 Kitchenham-Charters [18] 系统映射研究 标准。
3. **字段来源**：
   - 抽取 form 在 III. Methodology 末段以散文形式给出（metadata + context + 方法 + results）；
   - 分类方案（classification scheme；首次术语） 由 Table I–V 显式承载；
   - B1–B6 与 P1–P6 为作者归纳所得的 thematic 分类法；原文报告主题归类结果，但未提供完整 open coding / codebook / 冲突裁决日志。
4. **RQ 与样本单位关系**：RQ 是字段用途（RQ1=研究分布, RQ2=benefit 抽取, RQ3=problem+solution 抽取）；样本单位是 原始研究；树根是"28 篇 RE-in-ASD 研究的 thematic mapping"。
5. **降级**：不按 roadmap/guideline 降级；本文是后续主统计池候选。但 A1 仅作 schema_seed，A2a 完成页码、表格和 prose 关系精核前，不进入最终定量统计；同时 N=28 较小，部分 cell (FDD=1, Tool eval=1) 单元过稀，统计结论需保留小样本警告。

### 3. 原生样本编码维度树

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] 敏捷软件开发（Agile Software Development）中的需求工程（Requirements Engineering）原始研究（28 篇）
├── [b-rq] 三个显式 RQ（字段用途锚）
│   ├── RQ1 研究分布：投影到发表源、敏捷上下文、文章类型
│   ├── RQ2 收益：投影到 B1–B6
│   └── RQ3 问题与解决方案：投影到 P1–P6 + solution 关系
│
├── [b-语料] 检索语料与纳排分母链
│   ├── 数据库：Scopus
│   ├── 原文检索式："(requirements analysis OR requirements engineering) AND (agile OR scrum) AND NOT (agile manufacturing)"
│   ├── 时间窗：until Sep 2014
│   ├── 初始结果：241
│   ├── 文档类型 / 语言过滤后：187
│   ├── 标题摘要过滤后：65；标题摘要排除 123
│   ├── 全文筛选后：28；全文排除 37
│   ├── 纳入年份跨度：2003–2014（正文 §VI 主要写 2004–2014，但 S20=2003）
│   └── 排除原因：无摘要访问（no abstract access）、非研究（non research）、非软件工程（non SE）、主题不符（off topic）、掠夺 / 虚荣出版（predatory vanity）、无全文访问（no fulltext access）、冗余扩展版（redundant extended）
│
├── [b-pub-venue] 发表源分类（Table I）
│   ├── 发表源类型：{会议（会议）, 期刊（期刊）, 杂志（杂志）}
│   ├── 会议：15（约 53%）
│   ├── 期刊：8（约 29%）
│   ├── 杂志：5（约 18%）
│   └── 发表源名称：开放枚举，见 Table I
│
├── [b-agile-context] 敏捷方法上下文（Table II）
│   ├── 未具体说明 agile 方法：20（71%）
│   ├── Scrum：7（25%）
│   └── FDD：1（4%）
│
├── [b-article-type] 研究类型（Table III）
│   ├── 多案例研究（multiple_case_study）：6
│   ├── 单案例研究（single_case_study）：5
│   ├── 经验报告（experience_report）：3
│   ├── 工具评价（tool_evaluation）：1
│   ├── 方法评价（method_evaluation）：2
│   ├── 方法提出（method_proposal）：8
│   └── 立场论文（position_paper）：3
│
├── [b-definition] Agile RE 定义维度（RQ1 子轴）
│   ├── 定义清晰度：模糊（vague）/ 无通用定义（no universal definition）
│   └── 作者提出的定义：§V.B 自由文本；属于 候选发现，不作为统计字段
│
├── [b-benefit] B1–B6 收益封闭枚举（Table IV）
│   ├── B1 降低过程开销：4 篇 {S2,S4,S20,S25}
│   ├── B2 改善需求理解：6 篇 {S2,S3,S4,S7,S18,S23}
│   ├── B3 减少过载 / 资源过分配：3 篇 {S2,S3,S7}
│   ├── B4 提升变化响应：5 篇 {S4,S7,S20,S23,S25}
│   ├── B5 快速交付与验证：3 篇 {S4,S20,S25}
│   └── B6 改善客户关系：2 篇 {S4,S7}
│
└── [b-problem-solution] P1–P6 问题 + 解决方案关系模式（Table V + §IV.D）
    ├── P1 客户 / 客户代表问题：6 篇；解决方案集合 = {S5,S10,S11,S12,S15,S17,S20,S26}
    ├── P2 用户故事格式不足：6 篇；解决方案集合 = {S1,S5,S8,S9,S24,S27}
    ├── P3 优先级排序困难：5 篇；解决方案集合 = ∅（无解决方案（无解决方案））
    ├── P4 技术债增长：2 篇；解决方案集合 = ∅（无解决方案（无解决方案））
    ├── P5 隐性需求知识：5 篇；解决方案集合 = {S20}
    └── P6 工作量估算不精确：2 篇；解决方案集合 = ∅（无解决方案（无解决方案））

关键迁移点：解决方案集合 = ∅ 是 一等信号；“未提出解决方案”不是缺失值，而是可统计 缺口（gap）。
```

`★ Insight ─────────────────────────────────────`
- `解决方案集合 = ∅` 是这份 模式 最值得迁移的设计选择：作者把"未提出解"作为 一等信号而不是缺失。Paper2 维度树的"缺口（gap） 字段"可以直接学这一招——空集是结论，不是 缺失数据。
- `多案例研究（multiple_case_study）=6 + 单案例研究（single_case_study）=5 + 经验报告（experience_report）=3 + tool/method eval=3 ≈ 17/28 = 61%` 与 §V.A 给出的"≈60%"自洽，可作为 A2a 一致性校验锚点之一。
`─────────────────────────────────────────────────`

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-rq-list | 三个显式 RQ | b-rq | §I Introduction RQ 段 | 作者声明的研究目标 | 三条自由文本 RQ | enum-3 | 不适用 | 字段用途 anchor | 不直接成 发现 | Page 1 RQ 段 | 仅本文 |
| L-语料-db | 检索数据库 | b-语料 | §III ¶2 | 检索源 | {Scopus} | 完整枚举（封闭） | 不适用 | 用于评估检索覆盖 | 单库覆盖局限 → candidate 威胁 | Page 3 §III | 可迁移结构 |
| L-语料-string | 检索式 | b-语料 | §III ¶2 | 完整 search string | 自由文本 + 关键词集合 | 文本+词袋 | 不适用 | 复现性证据 | 候选 keyword 聚类 | Page 3 §III | 可迁移结构 |
| L-语料-window | 时间窗 | b-语料 | §III ¶2 | 检索截止时间 | "Sep 2014" 单点 | 日期点 | 不适用 | 时效性评估 | 1 年截止可能漏 2014–2015 论文 | Page 3 §III | 可迁移结构 |
| L-语料-chain | 分母链 | b-语料 | §III ¶2-4 | 241/187/65/28 | 整数四元组 | 数值链 | 不适用 | 严格分母 | candidate selection 威胁 | Page 3 §III | 可迁移结构 |
| L-语料-excl | 纳排标准 | b-语料 | §III ¶3-5 | 5+3 条 exclusion | 封闭文本枚举 8 项 | enum-8 | 漏标=未应用 | 偏倚评估 | candidate 威胁 | Page 3 §III | 可迁移结构 |
| L-venue-type | venue 类型 | b-pub-venue | Table I | 出版形式 | {会议（会议）, 期刊（期刊）, 杂志（杂志）} | 三值枚举（封闭） | 不适用 | 频次表 | venue 分散 → "no primary venue" 发现 | Table I, §V.A | 可迁移结构 |
| L-venue-name | venue 名 | b-pub-venue | Table I | 具体 venue | 开放枚举（≥17 venue） | enum-open | 不适用 | venue 长尾 | candidate 缺口（gap） | Table I | 仅本文 |
| L-ctx-方法 | 敏捷方法上下文 | b-agile-context | Table II | 文章使用的敏捷方法 | {未说明（Unspecified）, Scrum, FDD} | 三值枚举（本样本封闭） | 不适用 | 频次 | "71% unspecified" 是显式 发现 | Table II, §V.A | 取值空间可能扩展 |
| L-art-type | 研究类型 | b-article-type | Table III | 文章类型 | {多案例研究（MultiCase）, 单案例研究（SingleCase）, 经验报告（ExpReport）, 工具评价（ToolEval）, 方法评价（MethodEval）, 方法提出（MethodProposal）, 立场论文（PositionPaper）} | 七值枚举（本样本封闭） | 不适用 | 频次 | "29% 方法 提案 w/o eval" → 发现 | Table III, §V.A | 可迁移分类轴 |
| L-def-clarity | 定义清晰度 | b-definition | §V.B | 作者对 agile RE 定义现状的判断 | {vague, contested, clear} | enum-3（本文取 vague） | 不适用 | 不入主统计 | 候选发现 "definition is vague" | §V.B | 仅本文判断 |
| L-def-author | 作者综合定义 | b-definition | §V.B blockquote | 作者自造定义文本 | 自由文本 | 自由文本 + 理由 | 不适用 | 不入主统计 | 候选发现 | §V.B | 不可直接采信 |
| L-benefit-code | benefit 类目 | b-benefit | Table IV | B1–B6 | {B1..B6} | enum-6 (closed) | 缺失=未观察到 | 频次 + 引用集合 | benefit landscape | Table IV | 可迁移轴 |
| L-benefit-studies | benefit→studies 关系 | b-benefit | Table IV | 每个 B 对应的 S 集合 | 关系（多对多） | 关系 set | ∅=未在样本中出现 | 频次/coverage | candidate "Bi 支撑薄" 判定 | Table IV | 可迁移结构 |
| L-problem-code | problem 类目 | b-problem-solution | Table V | P1–P6 | {P1..P6} | enum-6 (closed) | 缺失=未观察到 | 频次 | problem landscape | Table V | 可迁移轴 |
| L-problem-studies | problem→studies 关系 | b-problem-solution | Table V | 每个 P 对应的 S 集合 | 关系（多对多） | 关系 set | ∅=未在样本中出现 | 频次/coverage | candidate problem 强度 | Table V | 可迁移结构 |
| L-solution-rel | problem→solution 关系 | b-problem-solution | §IV.D 各小节 | 每个 P 对应的 S（solution 提议）集合 | 关系（多对多）+ NULL | 关系集合，且 ∅ 作为显式发现 | **∅ = "no solutions proposed"，是显式 发现** | 频次 + 缺口（gap） | 直接“研究空白（research gap）”信号 | Page 5–6 §IV.D | **强可迁移：空集做 first-class** |
| L-limit-search | 限制：单库 | b-语料 | §V.D | 仅用 Scopus | 布尔值 + rationale | 布尔值 | 不适用 | 威胁 assessment | candidate 威胁 | §V.D | 可迁移结构 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R-benefit-of | 研究（S1..S28） | reports_benefit | 收益代码（B1..B6） | {B1..B6} | 该 研究 未报告任何 benefit | Table IV | 频次/coverage |
| R-problem-of | 研究（S1..S28） | reports_problem | 问题代码（P1..P6） | {P1..P6} | 该 研究 未报告任何 problem | Table V | 频次/coverage |
| R-solution-of | 问题代码（P1..P6） | has_solution_in | 研究集合（研究 set）⊆ S1..S28 | 研究 set 或 ∅ | **∅ = 无解决方案（无解决方案_PROPOSED）（显式 发现）** | §IV.D 各小节末句 | 缺口（gap） 识别 |
| R-context-of | 研究（S1..S28） | uses_agile_method | agile 方法 | {未说明（Unspecified）, Scrum, FDD} | 不适用 | Table II | 上下文分层 |
| R-type-of | 研究（S1..S28） | has_article_type | 文章类型 | 七值枚举 | 不适用 | Table III | 类型分层 |
| R-venue-of | 研究（S1..S28） | published_in | 发表源名称 | 开放枚举 | 不适用 | Table I | venue 分布 |

`★ Insight ─────────────────────────────────────`
- 注意 `R-solution-of` 的源是 **problem code 而不是 研究**——这与 `R-benefit-of/R-problem-of` 的源不同。这是因为 §IV.D 是按 P1–P6 组织 solution，而不是按 研究 组织。这种"以问题为索引、以研究为证据"的结构是 SMS 中较少见的优雅设计。
- ∅ 作为显式 发现 的设计可作为候选抬升为 Paper2 维度树的通用约束：每个"建议/方法"叶子都应允许 `proposed = ∅` 并把它当作 一等结论。
`─────────────────────────────────────────────────`

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段/统计表直接支撑的统计观察（可作为 A2a 主统计候选）

| 观察 | 分母 | 数值 | 原文锚点 |
|---|---|---|---|
| 会议 占比 | 28 | 15/28 ≈ 53% | Table I |
| Unspecified agile context 占比 | 28 | 20/28 ≈ 71% | Table II, §V.A |
| 含实证成分文章占比 | 28 | 17/28 ≈ 60% (case+exp+evals) | §V.A |
| Method 提案 无评估占比 | 28 | 8/28 ≈ 29% | §V.A |
| Benefit 类目数（封闭） | 不适用 | 6 | Table IV |
| Problem 类目数（封闭） | 不适用 | 6 | Table V |
| Problem 无 solution 占比 | 6 | 3/6 (P3,P4,P6) | §IV.D 末句 |
| B2 支撑最强 | benefits | 6 studies | Table IV |
| P1, P2 支撑最强 | problems | 各 6 studies | Table V |

#### 6.2 作者提出的 候选发现（不可直接升级 final）

- "Agile RE 定义模糊"（§V.B）。
- "无主导 venue, RE in ASD 在出版形态上未'找到家'"（§V.A）。
- "大型/复杂系统中 user story 不够用"（§V.C 综合）。
- "P3/P4/P6 缺乏解 → 三个研究空白方向"（§V.C, §VI）。
- "方法提议未经实证评估 → 需更多实证研究"（§V.A, §VI）。

#### 6.3 可迁移到 Paper2 的方法学启发

- ∅-as-发现（空 solution set 作 一等结论）。
- "problem 索引 + 研究 证据"的关系型 模式（不要把 solution 压成 研究 的属性）。
- benefit/problem 双轴并列 + 共享 S-id 引用集，便于做 benefit-problem 对偶 mapping。
- 分母链严格保留（241→187→65→28）。

#### 6.4 不可迁移内容

- 任何 Agile RE 的领域结论（B1–B6, P1–P6 具体内容）不可迁移到 Paper2 的 STM / LLM-as-Judge / repair 主题。
- "Scrum/XP/FDD 三分"分类只对 agile RE 有效。
- N=28 + 单库（Scopus）+ 截至 2014.09 的样本属性。

## survey_of_surveys 自身 schema 抽取

本节把该论文投影到本目录自己的脚手架综述 schema（S1--S8）。判定等级只说明该维度在原文和本地证据链中的可用程度：`强` = 有明确原文结构和证据锚点；`中` = 有可复用结构但存在范围、裁决或精核限制；`弱` = 只作边界启发或风险提示；`不适用` = 原文类型不支持该维度进入统计池。

| 维度 | 判定等级 | 一句话抽取结果 | 证据位置 |
|---|---|---|---|
| S1 综述任务设定 | 强 | 本文是面向敏捷软件开发中需求工程的 SMS，显式提出 3 个 RQ：研究分布、收益、问题及对应解决方案。 | `review.md` 维度树复原 §1、§3；`evidence_chain.md` A.3 `clm-re-agile-sms-2015-type` |
| S2 语料收集与筛选 | 强 | 作者使用 Scopus、给出检索式和 2014-09 时间窗，并保留 241→187→65→28 的筛选分母链。 | `review.md` 维度树复原 §1--§3；`evidence_chain.md` A.2 `ev-re-agile-sms-2015-denom` |
| S3 原生维度树/样本编码对象 | 强 | 被编码对象是 28 篇原始研究 S1--S28，原生结构为 venue/context/article-type/benefit/problem 维度森林；作者按 P1--P6 组织 solution 讨论，problem→solution 关系边由本地审计复原，不是作者公开的 formal table。 | `review.md` 维度树复原 §2、§3、§5；`evidence_chain.md` A.3 `clm-re-agile-sms-2015-unit`、`clm-re-agile-sms-2015-tree`；`audits/a1-s1s8-19x1/adjudications/re-agile-sms-2015.md` |
| S4 字段级证据 | 中 | 叶子字段覆盖检索库、检索式、分母链、venue、agile context、article type、B1--B6、P1--P6 与 solution 关系；短文表格和页码待 A2a PDF 视觉核验。 | `review.md` 维度树复原 §4；`evidence_chain.md` A.2 `ev-re-agile-sms-2015-tree` |
| S5 维度模式演化 | 中 | 本文体现从 RQ 到分类表再到 finding 的模式演化：RQ1→分布字段，RQ2→benefit 枚举，RQ3→problem+solution 关系，并把空 solution set 作为缺口信号。 | `review.md` 维度树复原 §3、§5、§6.3 |
| S6 统计分析 | 强 | 原文给出会议 15/28、未说明 agile context 20/28、含实证成分约 17/28、method proposal 8/28、无 solution problem 3/6 等明确描述统计；这些只支持 mapping landscape，不支持因果或效果综合。 | `review.md` 维度树复原 §6.1；`audits/a1-s1s8-19x1/adjudications/re-agile-sms-2015.md` |
| S7 候选 finding | 强 | 候选 finding 包括 agile RE 定义模糊、缺少主导 venue、user story 在大型复杂系统中不足、P3/P4/P6 缺少解决方案、方法提议缺少实证评估。 | `review.md` 维度树复原 §6.2 |
| S8 研究者/作者质疑与裁决 | 弱 | 原文有 V.D Limitations，覆盖 Scopus 单库与关键词范围限制；未呈现多研究者筛选/编码冲突裁决、一致性或 QA 协议。 | `paper_content.txt` §V.D；`review.md` 维度树复原 §0、§6.2 |

### S1--S8 四分栏证据拆分

#### 总体统计池裁决

裁决：**主统计池候选，但仅限 A1 schema_seed / mapping 字段统计；A2a 精核前不得进入最终定量统计或研究发现池**。理由是原文确为 2015 年 SEAA 短会议论文形式的 systematic mapping study，给出 Scopus 检索式、时间窗、纳排标准与 241→187→65→28 的分母链，并对 28 篇原始研究 S1--S28 做 venue、context、article type、benefit、problem / solution 分类；但样本量较小、单库 Scopus、表 I--V 版面/页码尚未 PDF 视觉核验，且未报告多研究者筛选/编码裁决、一致性或 QA 协议。因此可作为 S1--S7 的可统计模式种子，S8 只能弱证据记录限制与缺失裁决机制。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文标题、摘要和引言明确为 “mapping study”；提出 3 个 RQ：研究了什么、报告了哪些 agile RE benefits、有哪些 problems 及 corresponding solutions。 | 根对象复原为“敏捷软件开发中的需求工程原始研究（28 篇）”，RQ1--RQ3 分别锚定分布、benefit、problem+solution 三类字段用途。 | **可入候选池**：SMS 任务设定清晰，可作为 exploratory mapping RQ 样本；不支持效果评价型结论。 | 核对 PDF 中 RQ 段页码与 wording；确认会议短文未在附录补充更细 protocol。 |
| S2 语料收集与筛选 | Methodology 给出 Scopus、2014-09 检索、完整检索式、排除非 journal/conference、非英文、题摘排除和全文排除标准；分母为 241→187→65→28。 | 复原出“语料/纳排分母链”分支：数据库、检索式、时间窗、初筛、题摘筛选、全文筛选、排除原因。 | **可入候选池**：分母链足以支撑 mapping-study 筛选字段；但单库检索限制需随字段一起保留。 | PDF 视觉核验检索式脚注、排除标准编号、分母数字；检查 2003/2004--2014 年份跨度表述差异。 |
| S3 原生维度树/样本编码对象 | 方法段说明抽取 metadata、context、methods、results，并归入 definition、benefits、problems、solutions；结果表使用 S1--S28 原始研究编号。 | 复原为维度森林：语料分支 + venue/context/article-type 三个分布分支 + definition + B1--B6 benefit + P1--P6 problem / solution 关系边。 | **可入候选池**：样本单位为原始研究，树/森林结构清楚；problem→solution 是本地从 §IV.D 复原的关系 schema，不应写成原文 formal table。 | 核验 Table I--V 中 S 编号、合并单元格、B/P 枚举是否与文本提取一致；确认 solution set 的边界。 |
| S4 字段级证据 | Table I--III 给 venue、agile method context、article type；Table IV--V 给 benefit/problem 类目及 S 编号集合；§IV.D 逐项讨论 solution 或 no solutions。 | 叶子字段包括 Scopus/search string/分母链、venue type/name、context、article type、definition clarity、B/P code、study set、solution relation、single-database limitation。 | **有条件可入候选池**：字段丰富且多为封闭枚举/关系集合；当前证据等级为全文文本级，表格数值仍不宜 final。 | 必须对表 I--V 做 PDF 表格级核验；特别核验会议/期刊/杂志计数、B1--B6/P1--P6 的 S 集合与空 solution 断言。 |
| S5 维度模式演化 | 原文从 RQ 到 Results 再到 Discussion：RQ1 形成分布表，RQ2 形成 benefit taxonomy，RQ3 形成 problem taxonomy 与 solution/gap 讨论。 | 复原出 RQ→字段→统计观察/候选 finding 的演化链；“solution 集合为空”被视为一等缺口信号。 | **中等候选资格**：可作为 mapping 维度如何生成 finding 的模式种子；但演化过程多由本地审计重构，不能当作作者显式方法论贡献。 | 核验 §IV.D/V.C/VI 中 no-solution 与 future-work 句子，避免把审计者归纳过度写成作者 schema。 |
| S6 统计分析 | 原文给出 28 篇样本的描述统计：conference 15/28、journal 8/28、magazine 5/28；unspecified agile 20/28、Scrum 7、FDD 1；method proposal 8/28；经验/评价类约 17/28 等。 | 统计分支可复原为分布统计 + coverage 统计 + problem 无 solution 比例（P3/P4/P6 = 3/6）。 | **可入候选池但小样本降权**：适合 landscape / coverage 统计，不适合因果、效果、饱和性或全域趋势判断。 | 核验所有百分比四舍五入和表格单元格；短会论文 N=28、单库 Scopus 和稀疏 cell（如 FDD=1、tool eval=1）必须保留警告。 |
| S7 候选 finding | 摘要、Discussion 和 Conclusion 给出 agile RE 定义模糊、无主导 venue、user story 在复杂大型系统中不足、P3/P4/P6 无解决方案、方法提议缺少实证评价等发现。 | finding 由字段统计和主题归纳支持：definition clarity、venue dispersion、article type distribution、problem-solution gap、empirical evaluation gap。 | **可入候选 finding 池**：仅作为本文内部 mapping finding 或 Paper2 方法启发；不得迁移 Agile RE 领域结论。 | A2a 需逐条映射 finding→表格/段落证据；区分作者明说、审计归纳与后续研究启发。 |
| S8 研究者/作者质疑与裁决 | §V.D Limitations 仅说明 Scopus 单库和检索词范围限制；未见多研究者筛选、编码冲突裁决、inter-rater agreement 或 QA checklist。 | 复原为“限制声明存在，但研究者裁决机制缺失”的弱分支；可记录 negative evidence。 | **弱资格/不入强统计**：可统计“是否报告 limitations=是、是否报告裁决/一致性=否/未报告”，但不支撑高可信 QA 模式。 | PDF 全文检索/视觉核验是否存在遗漏的裁决、双人筛选、编码一致性或 quality assessment 描述；若仍缺失，应保持弱或缺失编码。 |

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
