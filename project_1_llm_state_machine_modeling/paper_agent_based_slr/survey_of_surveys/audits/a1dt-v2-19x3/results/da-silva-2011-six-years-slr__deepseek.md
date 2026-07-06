Now I have all the materials. Let me compose the full audit report.

---

# A1-DT v2 单篇全文审计报告：`da-silva-2011-six-years-slr`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `da-silva-2011-six-years-slr` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是；全文 1625 行，通读所有章节（§1--§7）、全部表格（Table 1--13）、附录 A 参考文献列表及 Fig. 1/Fig. 2 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；均已读取并核对 |
| 是否打开或核对 `paper.pdf` | 否；本审计基于 `paper_content.txt` 全文文本。Table 2 是跨页宽表，`paper_content.txt` 已捕获完整行列内容（含 [SE01]--[SE77] 及表头），但 PDF 版面核验（页码对应、跨页断裂、字号/格式异常）仍未执行。标记为 `needs_visual_verification` |
| 原文类型 | SLR（updated tertiary study — 更新型三级研究） |
| 被编码样本单位 | 个体 SLR（secondary study / systematic literature review），以 `[SE01]` 至 `[SE77]` 唯一标识，最终入选 67 篇 |
| 样本数量 / 分母 | SE 期：67 篇新 SLR；合并 OS/FE：120 篇（53+67） |
| 原生树类型 | **维度森林**（multi-table schema）：一个主编码表（Table 2）含 9 个数据抽取字段 + 3 个质量评估维度 + 教育/实践映射双外部分类体系（SE 2004 Curriculum + SWEBOK）+ 时间/作者/机构/国家/质量-年度趋势等跨维度分析 |
| 主统计池资格 | 是；具备系统检索/纳排/编码方案、清晰分母、可归档编码字段与统计表，可作为 Paper2 维度森林的核心 schema seed |
| 总体判定 | **pass**（原文已被充分阅读，维度森林已复原；现有 `review.md` 需返修以纠正"六叶通用接口"替代原生树的问题） |

---

## 1. 原文证据阅读说明

### 实际读取范围

| 读取对象 | 路径 / 来源 | 读取范围 |
|---|---|---|
| `bibtex.bib` | paper dir | 全文读取：作者、标题、IST 期刊、DOI、年份 |
| `metadata.json` | paper dir | 全文读取：所有 22 个字段 |
| `paper_content.txt` | paper dir | 全文 1625 行，覆盖 §1 Introduction -- §7 Conclusions、Table 1--13、Fig. 1--2、Appendix A 全部 SE01--SE77 引用 |
| `review.md` | paper dir | 全文 221 行，含快速结论卡片、六类 pattern 抽取、A1-M0--M6 脚手架、A.1--A.4 附录草案 |
| `paper.pdf` | paper dir | 未打开 |

### 是否仅基于 text

本审计主要基于 `paper_content.txt`。以下内容仍需 PDF 版面核验：
- Table 2 是 2 页以上的跨页宽表（16 列 × 67+ 行），`paper_content.txt` 已成功捕获，但可能存在列对齐偏移；
- Table 3 的质量分排序四等分表可能有删节；
- Table 5（教育/实践映射）、Table 11/12/13 的数值精度；
- Fig. 1（决策与共识流程 DCP）、Fig. 2（纳入流程图）为矢量图，无法从 text 复现其拓扑。

### 关键证据锚点（11 个）

1. **§1 Introduction** — "Two tertiary studies, published in 2009 and 2010, identified and analysed 54 SLRs... we extended and updated... 67 new SLRs addressing 24 software engineering topics"（摘要段，定义 tertiary study 继承关系与样本基数）
2. **§3.1 Research Questions** — RQ1--RQ5 完整列表，"equivalent to the research questions used in the FE"（定义 RQ 继承与前序对齐）
3. **§3.7 Data Extraction Process** — "We extracted the following data from the 77 studies" 下方给出 9 个字段全枚举（Year / Quality Score / Review Type / Review Scope / Topic Area / Cited EBSE / Cited Guidelines / Number of Primary Studies / Practitioners Guidelines / Source Type）
4. **§3.6 Quality Assessment** — QA1--QA4 四问完整定义，"Y=1, P=0.5, N=0" 评分细则
5. **§3.4 Search Process** — 自动搜索 query string 全文 + 手动搜索源列表（Table 1）+ 搜索策略（自动/手动/后向引用三级混合）
6. **Fig. 2 (Identification of Included SLRs)** — 1389 → 157 → 154 → 75 → 77 → 67 的漏斗纳排
7. **Table 2** — 67 行 × 16 列的完整主编码表，含 Study Ref、Year、Quality Score、Review Type、Review Focus、Review Topic、Cited EBSE、Cited Guidelines、Number Primary Studies、Practitioners Guidelines、Paper Type
8. **Table 5 + Table 6** — 教育课程（SE 2004 Curriculum）与实践知识体系（SWEBOK）双外部分类映射
9. **Table 7 + Table 8** — 作者频率表（≥3 篇）与国家分布表
10. **Table 11 + Table 12 + Table 13** — 质量评估演化、guideline 使用率、质量年度均值与标准差
11. **§7 Conclusions** — "three important changes"（覆盖扩大/研究者扩散/映射研究增多）与"three major limitations"（质量评估不足/合成方法弱/实践指南缺失）

---

## 2. 样本单位与字段来源判定

### 1. 纳入和逐项描述的对象

**个体 SLR（secondary study）**，即已发表的系统文献综述。每篇 SLR 以 `[SE01]` 至 `[SE77]`（含跳过编号）在 Table 2 和 Appendix A 中唯一标识。原文描述的对象是"这篇 SLR 的方法学质量、研究范围、主题归属、引用准则与实践转化"。

### 2. 系统检索 / 纳排 / 数据抽取 / 编码方案

**有完整的系统检索与纳排方案：**
- 自动搜索：6 个数字图书馆（ACM、IEEEXplore、Science Direct、CiteSeerX、ISI Web of Science、Scopus），统一 query string
- 手动搜索：15 个期刊和会议论文集（Table 1）
- 后向引用搜索：对 75 篇入选研究查全部参考文献，额外发现 2 篇
- 纳入/排除标准（§3.5）：需全文阅读后判断 SE 领域 SLR，排除非 SE、于 OS/FE 中已出现、时间窗口外、缩略版、质量 0 分
- 纳排漏斗（Fig. 2）：1389 → 157（第一滤） → 合并手动 66 → 去重 69 → 75 → 77 → 最终 67

**有系统数据抽取方案：**
- 9 字段编码方案在 §3.7 明确定义
- 双研究员独立抽取 + 决策与共识流程 DCP（Fig. 1）
- 质量评估用 DARE 四问，Y/P/N 三值评分，跨研究员盲评一致性验证（10 篇对比，8 完全一致）

### 3. 原文字段来源

字段来自以下原文层级：

| 层级 | 来源 |
|---|---|
| L0 样本单位标识 | Table 2 的 `Study Ref` 列 + Appendix A 的完整引用 |
| L1 抽取字段（9 字段） | §3.7 Data Extraction Process |
| L2 质量评估维度（QA1--QA4） | §3.6 Quality Assessment + DARE criteria |
| L3 外部分类体系映射 | §5.2：SE 2004 Curriculum Guidelines + SWEBOK（Table 5, Table 6） |
| L4 聚合统计维度 | RQ1（计数/年度增长）、RQ3（作者/机构/国家）、RQ5（质量年度趋势）、Table 7--Table 13 |
| L5 方法学局限性评估维度 | §5.4（RQ4：旧限制是否仍存在）+ §6 Limitations |

**无 replication package 或外部可下载编码表**。Table 2 是 paper 内嵌主编码表。

### 4. RQ 与样本单位的关系

RQ 不构成"树根"。关系如下：
- **RQ1**（数量）：聚合统计，使用样本单位计数
- **RQ2**（主题）：在 L1 字段 `Topic Area` + L3 映射（SE Curriculum / SWEBOK）上做分布统计
- **RQ3**（作者/机构/国家）：从样本单位的书目元数据中提取聚合
- **RQ4**（旧限制是否仍存在）：在 L2 质量维度 + L1 字段（QA3, Practitioner Guidelines）上做时间对比
- **RQ5**（质量是否提升）：在 L2 QA1--QA4 的年度均值上做趋势分析

**字段/维度是数据抽取的产物，RQ 是这些维度的统计使用方式。** 维度树应还原"从每篇 SLR 抽取了什么字段"，RQ 是字段的消费端。

### 5. 降级判断

**不适用**。本文有系统样本库（67 篇 SLR），有明确定义的编码方案，无需降级为 boundary anchor 或 methodological seed。

---

## 3. 原生样本编码维度树 / 维度森林

本文的原生编码体系是一个**维度森林**（multi-table dimensional forest），由以下互相关联但相对独立的编码子空间组成：

### 3.0 根对象

**`个体 SLR`（secondary study）**，以 `[SE01]`--`[SE77]` 为唯一标识符。

### 3.1 主干 1：抽取编码表（Table 2 的 9 + 1 字段）

```
[dim-da-silva-2011-root] 个体 SLR
├── [dim-da-silva-2011-l1-year] 发表年份
│   └── 取值空间：{2008, 2009}（完整枚举）
├── [dim-da-silva-2011-l1-quality-score] 质量评分
│   └── 取值空间：[0, 4]，步长 0.5（数值区间，来源：QA1+QA2+QA3+QA4 求和）
├── [dim-da-silva-2011-l1-review-type] 综述类型
│   └── 取值空间：{SLR (Conventional Systematic Literature Review), MA (Meta-Analysis), MS (Mapping Study)}（完整枚举）
├── [dim-da-silva-2011-l1-review-scope] 综述焦点
│   └── 取值空间：{RQ (detailed technical question), SERT (trends in SE topic area), RT (research methods)}（完整枚举）
├── [dim-da-silva-2011-l1-topic-area] SE 主题领域
│   └── 取值空间：自由文本（如 "Requirements Engineering" / "Distributed Software Development"），但 §5.2 汇总出 24 个离散主题（层级枚举的聚合层）
├── [dim-da-silva-2011-l1-cited-ebse] 引用 EBSE 论文
│   └── 取值空间：{Y (Yes), N (No)}（布尔）
├── [dim-da-silva-2011-l1-cited-guidelines] 引用 SLR 指南
│   └── 取值空间：{Y (Yes), N (No)}（布尔）
├── [dim-da-silva-2011-l1-num-primary-studies] 初级研究数量
│   └── 取值空间：正整数（数值/区间）
├── [dim-da-silva-2011-l1-practitioner-guidelines] 是否提供实践指南
│   └── 取值空间：{Y (Yes), N (No)}（布尔）
└── [dim-da-silva-2011-l1-source-type] 发表来源类型
    └── 取值空间：{J (Journal), C (Conference), WS (Workshop), BS (Book Series)}（完整枚举）
```

### 3.2 主干 2：质量评估维度（§3.6 QA1--QA4）

```
[dim-da-silva-2011-quality-root] 个体 SLR 的质量评估
├── [dim-da-silva-2011-qa1] 纳入/排除标准是否描述且适当
│   └── 取值空间：{Y=1, P=0.5, N=0}（层级枚举）
├── [dim-da-silva-2011-qa2] 文献搜索是否覆盖所有相关研究
│   └── 取值空间：{Y=1, P=0.5, N=0}（层级枚举）
├── [dim-da-silva-2011-qa3] 是否评估了初级研究的质量/有效性
│   └── 取值空间：{Y=1, P=0.5, N=0}（层级枚举）
└── [dim-da-silva-2011-qa4] 基础数据/研究是否充分描述
    └── 取值空间：{Y=1, P=0.5, N=0}（层级枚举）
```

注：QA1--QA4 的原始取值定义见 §3.6，Y/P/N 有详细释义（如 QA2 的 Y = "searched 4+ digital libraries and included additional search strategies"），不只是简写。| 取值空间类型：层级枚举（带释义条件）

### 3.3 主干 3：教育/实践双外部映射（§5.2, Table 5, Table 6）

```
[dim-da-silva-2011-edu-practice-root] 个体 SLR 的教育与实践关联
├── [dim-da-silva-2011-edu-curriculum] 对应 SE 2004 课程章节
│   └── 取值空间：外部分类法引用（SE 2004 Curriculum Guidelines 的 12 大类 × N 子节）
│   └── 取值空间类型：外部分类法引用
├── [dim-da-silva-2011-swbook] 对应 SWEBOK 知识域
│   └── 取值空间：外部分类法引用（SWEBOK 的 10 个知识域章节）
│   └── 取值空间类型：外部分类法引用
├── [dim-da-silva-2011-edu-relevance] 对本科教育的相关性
│   └── 取值空间：{Yes, Possibly, No}（层级枚举）
│   └── 证据锚点：Table 5 列 "Relevant to undergraduates?"
└── [dim-da-silva-2011-practice-relevance] 对实践的指导性
    └── 取值空间：{Yes, Possibly, No}（层级枚举）
    └── 证据锚点：Table 5 列 "Relevant to practitioners?"
```

### 3.4 主干 4：聚合分析维度（跨样本统计，不归入单篇字段）

```
[dim-da-silva-2011-aggregate-root] 聚合统计（来自 RQ1/3/5 讨论）
├── [dim-da-silva-2011-agg-authors] 作者/合著者（Table 7 的姓名/频率）
│   └── 取值空间类型：关系值（个体 SLR → 作者 → 机构 → 国家）
├── [dim-da-silva-2011-agg-organizations] 机构归属
├── [dim-da-silva-2011-agg-countries] 国家/地区（Table 8 的六大区域分类）
├── [dim-da-silva-2011-agg-quality-by-year] 质量 × 年份（Table 13）
├── [dim-da-silva-2011-agg-citation-vs-quality] 引用指南 × 质量（Table 12, §5.5 回归分析）
├── [dim-da-silva-2011-agg-num-primary-vs-quality] 初级研究数量 × 质量（Pearson r = −0.204）
└── [dim-da-silva-2011-agg-quality-evo] 初级研究质量评估演化（Table 11：N/Y/百分比）
```

### 3.5 维度森林结构说明

- 主干 1（L1 抽取字段）是**事实主源**，直接对应每篇个体 SLR；
- 主干 2（QA1--QA4）是 L1 字段 `Quality Score` 的**分解维度**；
- 主干 3（教育/实践映射）是**外部分类体系引用**，对 L1 的 `Topic Area` 做二次编码；
- 主干 4（聚合分析）是**跨样本统计维度**，不具有"每篇 SLR 取值"的单值语义。

以上主干 1 + 主干 2 + 主干 3 构成"可逐篇填充"的编码 schema；主干 4 构成统计消费层。

### 3.6 A2a 精核任务说明

以下字段需要 PDF 核对 + 原文确认：
- Table 2 的完整 16 列 header（`Review Focus` 列在 text 中似与 `Review Scope` 混淆，需原文确认是否同义；text 中 "Review Scope" 在 §3.7 定义为 RQ/SERT/RT，但 Table 2 header 写作 "Review focus"）
- QA3 的 P 取值条件（"the research question involves quality issues that are addressed by the study"）在 paper 中的实际应用边界
- Table 5 的教育/实践 relevance 判定标准的详细定义（`paper_content.txt` 未完整捕获）

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leaf-da-silva-2011-year` | 发表年份 | `dim-da-silva-2011-root` | §3.7 "The Year of publication" | 该 SLR 的出版年份 | {2008, 2009} | 完整枚举 | 无缺失（纳排条件之一） | RQ1 年度增长统计 | 年度趋势发现 | §3.7 para 1; Table 2 col "Year" | 可迁移为时间窗字段 |
| `leaf-da-silva-2011-quality-score` | 质量评分 | `dim-da-silva-2011-root` | §3.7 "The Quality Score of the study"; §3.6 QA1--QA4 评分细则 | 基于 DARE 四问的 0--4 加权和（每问 Y=1/P=0.5/N=0） | [0, 4]，步长 0.5 | 数值区间 | 排除质量分为 0 的 1 篇 | RQ5 质量趋势；与 guideline/期刊的回归 | 质量-实践关联发现 | Table 3, Table 13; §5.5 | 评分细则可迁移；具体 DARE 准则需适配目标领域 |
| `leaf-da-silva-2011-review-type` | 综述类型 | `dim-da-silva-2011-root` | §3.7 "The Review Type" | 该 SLR 的方法学类型 | SLR / MA / MS | 完整枚举 | "all 67 SLRs" 均有标注 | RQ4/5 按类型分层分析 | 映射研究比例上升趋势 | Table 2 col "Review type"; §5.5 按 RQ/SERT/RT 回归 | 枚举值可迁移到 Paper2 分类 |
| `leaf-da-silva-2011-review-scope` | 综述焦点 | `dim-da-silva-2011-root` | §3.7 "The Review Scope" | 该 SLR 的研究焦点类型 | RQ / SERT / RT | 完整枚举 | Table 2 中所有记录均有标注 | §5.5 回归：RQ 型质量更高 (p=0.025) | scope × quality 关联 | §3.7 para 1; Table 2 col "Review focus" | 可迁移为"焦点类型"字段 |
| `leaf-da-silva-2011-topic-area` | SE 主题领域 | `dim-da-silva-2011-root` | §3.7 "The software engineering Topic Area" | 该 SLR 涉及的 SE 主题 | 自由文本 → 聚合为 24 个主题（如 Requirements Engineering, Distributed Software Development, Software Product Line...） | 自由文本加理由（聚合层为层级枚举） | 无缺失 | RQ2 主题分布；教育/实践覆盖统计 | 主题覆盖扩大的发现 | Table 2 col "Review topic"; §5.2 | 自由文本需重新分类；不可直接迁移 SE 主题名 |
| `leaf-da-silva-2011-cited-ebse` | 引用 EBSE 论文 | `dim-da-silva-2011-root` | §3.7 "Whether the study explicitly Cited EBSE papers" | 是否引用 Kitchenham 2004/Dybå 2005/Jørgensen 2005 中至少一篇 | Y / N | 布尔 | 未标注即为 N | §5.4.4 指南使用分析 | 引文 × 质量关联 | Table 2 cols "Cited EBSE paper"+"Cited guidelines"; §5.4.4 | 可迁移为"方法论引用"字段 |
| `leaf-da-silva-2011-num-primary` | 初级研究数量 | `dim-da-silva-2011-root` | §3.7 "The Number of Primary studies" | 该 SLR 纳入的初级研究篇数 | 正整数（1--237） | 数值区间 | 所有入选研究均有明确或可推算数量 | §5.5 Pearson r = −0.204 vs 质量 | 大规模 SLR 质量下降的发现 | Table 2 col "Number primary studies"; §5.5 | 可迁移为通用"样本量"字段 |
| `leaf-da-silva-2011-pract-guidelines` | 实践指南提供 | `dim-da-silva-2011-root` | §3.7 "Whether the study Included Practitioners Guidelines" | 是否明确定义面向实践的指南章节/表格 | Y / N | 布尔 | 未标注即为 N | Table 10；§5.5 回归 B=0.183, p=0.000 | 实践指南不足的发现 | Table 2 col "Practitioners guidelines"; Table 10; §5.4.2 | 可迁移为"实践指导"字段 |
| `leaf-da-silva-2011-source-type` | 发表来源类型 | `dim-da-silva-2011-root` | §3.7 "The Source Type" | 该 SLR 首次发表的载体类型 | J / C / WS / BS | 完整枚举 | 所有记录均有标注 | §5.5 期刊 vs 会议质量对比 | 期刊 SLR 质量更高的发现 | Table 2 col "Paper type" | 可迁移为"载体类型"字段 |
| `leaf-da-silva-2011-qa1` | QA1 纳入/排除标准 | `dim-da-silva-2011-quality-root` | §3.6 QA1 | 纳入/排除标准是否明确定义且适当 | Y=1 / P=0.5 / N=0 | 层级枚举（带释义条件） | 所有入选研究均有评分 | 汇总为 quality score 的子项；非独立统计 | 多数研究在 QA1 上表现好 | §3.6 QA1 完整释义 | 可迁移为质量评估子维度 |
| `leaf-da-silva-2011-qa2` | QA2 搜索覆盖 | `dim-da-silva-2011-quality-root` | §3.6 QA2 | 文献搜索是否覆盖所有相关研究 | Y=1 / P=0.5 / N=0 | 层级枚举（带释义条件） | 同上 | 同上 | 多数研究在 QA2 上表现好 | §3.6 QA2 完整释义（含 bold face 修改部分） | 同上 |
| `leaf-da-silva-2011-qa3` | QA3 初级研究质量评估 | `dim-da-silva-2011-quality-root` | §3.6 QA3 | 是否评估了初级研究的质量/有效性 | Y=1 / P=0.5 / N=0 | 层级枚举（带释义条件） | 同上 | §5.4.3 关键分析；Q1 quartile 研究多在此失败 | 质量评估仍是主要短板的发现 | §3.6 QA3 + Table 11 | 同上 |
| `leaf-da-silva-2011-qa4` | QA4 数据/研究描述 | `dim-da-silva-2011-quality-root` | §3.6 QA4 | 基础数据/个体研究是否充分描述 | Y=1 / P=0.5 / N=0 | 层级枚举（带释义条件） | 同上 | Q1 quartile 研究多在此失败 | 评分主观性导致评分者间分歧多 | §3.6 QA4 + §6 Limitations | 同上 |
| `leaf-da-silva-2011-edu-relevance` | 本科教育相关性 | `dim-da-silva-2011-edu-practice-root` | §5.2; Table 5 | 该 SLR 对 SE 2004 本科课程的相关性 | Yes / Possibly / No | 层级枚举 | 仅"对学术界感兴趣"的不列入 Table 5 | Table 6 教育覆盖统计 | 15 篇 SLR 对本科教育相关 | Table 5, Table 6; §5.2 | 可迁移为"教育影响"字段，但教育体系需替换 |
| `leaf-da-silva-2011-practice-relevance` | 实践指导相关性 | `dim-da-silva-2011-edu-practice-root` | §5.2; Table 5 | 该 SLR 对从业者的潜在价值 | Yes / Possibly / No | 层级枚举 | 同上 | Table 6 实践覆盖统计 | 40 篇可能对实践者有用，但多数未提供明确指南 | Table 5, Table 6; §5.2 | 可迁移为"实践影响"字段 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel-da-silva-qual-to-qa` | `leaf-da-silva-2011-quality-score` | 组合（composition） | QA1, QA2, QA3, QA4 | Y/P/N → 数值 | 无，聚合即为得分 | §3.6: "The answers for the quality assessment questions... were then summed to yield the final quality score" | 确保质量分可分解为四维审计 |
| `rel-da-silva-topic-to-edu` | `leaf-da-silva-2011-topic-area` | 映射（mapping） | `leaf-da-silva-2011-edu-relevance` via SE 2004 Curriculum | 外部分类体系的章节 | 不纳入 Table 5 的不映射 | §5.2: "relating the topics covered with the SE 2004 Curriculum Guidelines... and SWEBOK" | 教育覆盖统计 |
| `rel-da-silva-topic-to-practice` | `leaf-da-silva-2011-topic-area` | 映射（mapping） | `leaf-da-silva-2011-practice-relevance` via SWEBOK | 外部分类体系的章节 | 同上 | 同上 | 实践覆盖统计 |
| `rel-da-silva-study-to-authors` | `dim-da-silva-2011-root` | 归属（belongs_to） | 作者集合 | 作者姓名字符串 | 所有 SLR 均有作者信息 | Table 7; §5.3 | 作者/机构/国家聚合统计 |
| `rel-da-silva-quality-trend` | `leaf-da-silva-2011-quality-score` | 时序（time_series） | `leaf-da-silva-2011-year` | 年度 → 均值/r | 无缺失年份 | Table 13; §5.5 | 质量年度趋势分析 |
| `rel-da-silva-quality-vs-guideline` | `leaf-da-silva-2011-quality-score` | 关联（correlation） | `leaf-da-silva-2011-pract-guidelines` | Y/N → 质量均值 | 所有研究均可分 | §5.5: "SLRs that explicitly provided guidelines... higher mean quality scores (Mean=2.85)" | 实践指南与质量的关联发现 |
| `rel-da-silva-quality-vs-source` | `leaf-da-silva-2011-quality-score` | 关联（correlation） | `leaf-da-silva-2011-source-type` | J/C/WS/BS → 质量均值 | 所有研究均可分 | §5.5: "SLRs published in Journals had higher quality scores (Mean=2.69) than... Conferences (Mean=2.44)" | 载体类型与质量关联 |
| `rel-da-silva-quality-vs-scope` | `leaf-da-silva-2011-quality-score` | 关联（correlation） | `leaf-da-silva-2011-review-scope` | RQ/SERT/RT → 质量均值 | 所有研究均可分 | §5.5: "SLRs with scope RQ performed better (Mean=2.88) than those with SERT (Mean=2.41)" | 焦点类型与质量关联 |
| `rel-da-silva-quality-vs-num-primary` | `leaf-da-silva-2011-quality-score` | 关联（correlation） | `leaf-da-silva-2011-num-primary` | Pearson r = −0.204, p=0.05 | 所有研究均可分 | §5.5: "SLRs addressing larger numbers of primary studies had lower quality scores" | 样本量与质量的反向关联 |
| `rel-da-silva-predecessor` | `dim-da-silva-2011-root`（本论文整体） | 继承/更新（updates） | OS [18] + FE [19] | — | — | §1; §3.1: "research questions... equivalent to the research questions used in the FE" | **对 Paper2 的关键字段：前序综述关系** |
| `rel-da-silva-old-vs-new-merge` | OS/FE 样本（53 SLR） | 合并（merges_with） | SE 样本（67 SLR） | — | — | §5: "compare them with the findings of OS/FE, and integrate the results (OS/FE + SE)" | 增量更新的合并策略 |

注：以上关系边中，`rel-da-silva-predecessor` 和 `rel-da-silva-old-vs-new-merge` 是"论文级"关系（不逐篇编码），但在维度森林设计中对应 A1 schema 的 `前序综述关系` 和 `合并策略` 字段。其余 8 条关系边均为"样本级"可编码关系，来自原文的关联分析。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文字段/统计表支持的统计观察

| 统计观察 | 支撑字段/表 | 证据强度 | 注意事项 |
|---|---|---|---|
| SE 期间 SLR 增长率（67 篇 in 1.5 年 vs 53 篇 in 4.5 年） | Table 4; RQ1 | strong | 时间窗口不对称，不能直接说"加速" |
| 24 个 SE 主题中 14 个在 OS/FE 中未出现 | Table 2 + Table 6 | strong | 依赖作者对主题的自由文本分类 |
| 质量分逐年提升（6 年提升 12.5%） | Table 13; RQ5 | strong | 2007 年下降例外，标准差仍较大 |
| 提供实践指南的 SLR 质量更高（M=2.85 vs M=2.38） | §5.5 回归 | strong | 相关性不等于因果 |
| 初级研究数量与质量分负相关（r=−0.204, p=0.05） | §5.5 Pearson | moderate | p=0.05 临界，效应量弱 |
| 仅 51% 的 SLR 评估了初级研究质量 | Table 11 | strong | — |
| 仅 28% 的 SLR 提供了实践指南 | Table 10 | strong | — |
| 仅 1 篇用 meta-analysis、2 篇用 meta-ethnography | §7 Conclusions | strong | 证据锚点明确 |
| 研究者数量增长 50%（103→159）、国家数 17→21 | §5.3 | strong | — |
| 亚洲在 OS/FE 中 0 篇、SE 中 10 篇（15%） | Table 8 | strong | 地理扩散显著 |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

| 候选 finding | 原文锚点 | 类型 | 可迁移性 |
|---|---|---|---|
| "SLR is being adopted consistently as a research method" | §7 Conclusions para 1 | 宏观趋势论断 | medium — 需更多时间窗口证据 |
| "EBSE is not being fully realised in practice"（因为缺少实践问题起源和指南） | §7 Conclusions para 4 | 领域诊断 | high — 可作为 Paper2 的对比基线 |
| "Mapping studies are increasing proportionally"（SLR 从"证据合成"转向"研究趋势映射"） | §7 Conclusions para 2 | 方法学趋势 | high — 可迁移为综述类型分布的 cross-check |
| "Updates and extensions of previous SLRs are essentially absent"（120 篇中 0 篇更新/扩展） | §7 Conclusions para 5 | 方法学缺口 | high — 直接支持"迭代修复"研究动机 |
| "Quality assessment of primary studies remains the major weakness" | §5.4.3; Table 11 | 方法学一致性发现 | high — 可与其他 tertiary study 交叉验证 |

### 6.3 对 Paper2 可迁移的方法学启发

1. **更新型 tertiary study 的合并策略**：本文明确示范了如何 inherit 前序研究的编码方案（QA1--QA4 沿用 DARE）、时间窗口、RQ 结构，并做可比性验证（blind assessment of 10 SLRs）。这直接对应 A1 schema 的 `前序综述关系` 和 `合并策略` 字段。
2. **维度森林设计模式**：本文证明 tertiary study 的编码 schema = 抽取字段（L1）+ 质量评估维度（L2）+ 外部分类体系映射（L3）+ 聚合统计（L4）。Paper2 可沿用此四层结构。
3. **纳排漏斗的完整文档化**：Fig. 2 的清晰度为 tertiary study 提供了可复现范本。
4. **多评估者共识流程 DCP**（Fig. 1）：可作为 Paper2 方法学声明中的参考。

### 6.4 绝不能迁移的领域结论

- 具体的 24 个 SE 主题及其频率分布（属于 2008--2009 年 SE SLR 生态）
- 具体作者/机构/国家排名（时效性极高）
- "Requirements Engineering 最多（8 篇）"等具体数字
- 教育课程映射的具体章节归属（SE 2004 Curriculum 已过时）
- SWEBOK 具体章节覆盖统计
- 质量年均值的具体数字（1.79--3.10 等）

---

## 7. 对现有 `review.md` 的返修建议

### C 级（Critical — 阻塞统计池资格）

| # | 问题 | 建议 |
|---|---|---|
| C1 | **"维度树"被通用六叶接口替代**。现有 `review.md` 的 A.1 表将 "scope / corpus / classification / method / evidence / finding" 六叶作为本文的原生维度树，这是跨论文投影模板，不是本文的编码 schema。本文的原生树是 §3.7 的 9 字段提取方案 + QA1--QA4 + SE Curriculum / SWEBOK 映射 + 聚合维度。 | 重写 §3 "维度树复原" 段，使用本文 §3.2--3.4 的原生编码结构替代六叶。六叶可保留在 A1-M0--M6 脚手架中作为跨论文投影，但不应标注为 "原文维度树"。 |
| C2 | **现有 A.1 DT 表中多个叶子是 schema_seed 占位符**，未填入本文实际字段名。例如 `leaf-da-silva-2011-six-years-slr-taxonomy` 等叶子使用了通用描述句 "来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构"，未指向实际字段。 | 替换为本文 §3.7 + §3.6 + §5.2 的实际字段标识（如 `leaf-da-silva-2011-review-type` 等）。 |
| C3 | **SUMMARY 表中样本单位/样本数量/原生树类型/统计池资格需要更新**。现有值可能是旧口径。 | 样本单位 = 个体 SLR；样本数量 = 67（SE 期间）/ 120（合并）；原生树类型 = 维度森林；统计池资格 = 是。 |

### I 级（Important — 影响维度树完整性）

| # | 问题 | 建议 |
|---|---|---|
| I1 | **缺失"教育/实践双外部映射"主干**（SE 2004 Curriculum + SWEBOK）。这是本文独创性的分类贡献，现有 review.md 未捕获。 | 新增 `dim-da-silva-2011-edu-practice-root` 主干和对应叶子（见 §4 叶子表）。 |
| I2 | **缺失"更新继承关系"的关系边**。本文与 OS/FE 的合并是核心方法学特征，现有 review.md 只有 `前序综述关系` 字段名，未展开关系边表。 | 添加 `rel-da-silva-predecessor` 和 `rel-da-silva-old-vs-new-merge`（见 §5 关系边表）。 |
| I3 | **A.2 证据账本缺少对 Table 2 列/Table 5/Table 6 的逐列证据映射**。现有 `EV-da-silva-2011-six-years-slr-002` 过于聚合。 | 补充按字段/表列的细化证据行。 |

### M 级（Minor — 建议优化）

| # | 问题 | 建议 |
|---|---|---|
| M1 | A.1 表使用 `schema_seed` 标签全覆盖，过度保守。经全文阅读后，至少 L1 的 9 字段可以升级为 `verified_by_text`。 | 将 L1 可核验字段（year, review type, review scope, source type 等）升级证据强度；仅对 QA 评分的精确值/Table 5 的个别行保留 `needs_visual_verification`。 |
| M2 | "六类 pattern 抽取"中的 dimension pattern 描述 "维度包括搜索策略、study selection、quality assessment、data extraction..." 这些都是方法学流程阶段，不是编码维度。 | 将此节中"方法流程"与"编码维度"区分，或者将该 pattern 重命名为 "methodology landmarks"。 |
| M3 | review.md 中部分表格引用 `paper_content.txt` 为 Page N，但未说明是否核实过原始 PDF 页码。 | 注明 "Page reference from paper_content.txt automatic extraction; needs PDF page number cross-check"。 |
| M4 | A.4 中 `needs_manual_check` 状态无具体检查清单。 | 补充具体检查项：Table 2 header 完整性、Table 5 判定标准、Fig. 1/Fig. 2 拓扑一致性。 |

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-v2-001 | paper_content.txt | §3.7 | "We extracted the following data from the 77 studies to answer the research questions:" 后跟 9 个 bullet items | "The Year of publication", "The Quality Score", "The Review Type", "The Review Scope", "The Topic Area", "Cited EBSE papers / Cited Guidelines", "Number of Primary studies", "Practitioners Guidelines", "Source Type" | 字段定义（primary schema） | **verified** | L1 全部 9 字段及其取值空间 | 否（text 级别已确认） | 字段语义需在 Paper2 中重新适配非 SE 领域 |
| EV-v2-002 | paper_content.txt | §3.6 | QA1--QA4 完整四问定义 + "Y = 1, P = 0.5, and N = 0" | "QA1: Are the review's inclusion and exclusion criteria described and appropriate? ... QA2: Is the literature search likely to have covered all relevant studies? ... QA3: Did the reviewers assess the quality/validity of the included studies? ... QA4: Were the basic data/studies adequately described?" | 字段定义（quality schema） | **verified** | QA1--QA4 四字段及其 Y/P/N 取值 | 否 | DARE 准则版本已变更（CRD 2010 有 5 问），本文仍用旧 4 问版 |
| EV-v2-003 | paper_content.txt | Table 2 | 67 行 × ≥12 列的完整编码表 | Study Ref, Year, Quality score, Review type, Review focus, Review topic, Cited EBSE, Cited guidelines, Number primary studies, Practitioners guidelines, Paper type | 实例层（instance data） | **verified** | 全部 L1 叶子字段的实例填充 | 是：header 对齐（"Review focus" vs "Review Scope"），跨页完整性 | 具体 SE 主题名不可迁移至非 SE 领域 |
| EV-v2-004 | paper_content.txt | §5.2; Table 5; Table 6 | "relating the topics covered with the Software Engineering 2004 Curriculum Guidelines... and the SWEBOK" | Table 5: 每篇 SLR → SE Curriculum section / SWEBOK chapter / Undergraduates relevance / Practitioners relevance | 字段定义 + 实例（edu/practice schema） | **verified** | 教育/实践双外部映射主干及 4 叶子 | 是：Table 5 的 relevance 判定标准全文需 PDF 确认 | 教育体系（SE 2004）和知识体系（SWEBOK 2004）均过时 |
| EV-v2-005 | paper_content.txt | §5.3; Table 7; Table 8 | "159 researchers... from 21 countries and 58 organisations" | Table 7 列出 ≥3 篇的作者姓名/国家/数量；Table 8 六大区域分布 | 聚合统计实例 | **verified** | 聚合维度中的作者/机构/国家分布 | 否 | 时间特定，不可外推 |
| EV-v2-006 | paper_content.txt | §5.5; Table 13 | "steady increase in the mean quality scores... except 2007" | Table 13: 2004--2009 分年/Cited Guidelines Yes/No 的均值与标准差 | 聚合统计 + 趋势发现 | **verified** | `leaf-da-silva-2011-quality-score` 的年度聚合使用 | 是：Table 13 的数值精度 | 趋势限于 2004--2009 SE SLR |
| EV-v2-007 | paper_content.txt | §5.5 | 质量分 × 实践指南 / 期刊 / RQ scope / 初级研究数的回归分析 | "Guidelines for Practitioners (B=0.183, std. error=0.038, p=0.000), Journal (B=0.117, p=0.005) and RQ (B=0.081, p=0.025)" | 关系边 + 统计发现 | **verified** | 4 条数值关联关系边 | 否 | 回归模型仅含三因子，可能有遗漏变量 |
| EV-v2-008 | paper_content.txt | §7 Conclusions | "only one ([SE37]) used a meta-analysis... two ([SE05, SE68]) used meta-ethnography" | "no other form of meta-synthesis was used" | 候选发现（方法学缺口） | **verified** | finding pattern "合成方法薄弱" | 否 | — |
| EV-v2-009 | paper_content.txt | §7 Conclusions para 5 | "We found neither an update nor an extension of a previous SLR among the 120 studies" | "producing updates and extensions... is an important research activity" | 候选发现（迭代缺口） + roadmap recommendation | **verified** | 对 Paper2 的关键动机支撑 | 否 | — |
| EV-v2-010 | paper_content.txt | §3.4; §3.5; Fig. 2 | 搜索 query string 全文 + 纳排漏斗 | "1389 documents → 157 → 154 → 75 → 77 → 67" | 纳排过程证据 | **verified** | 系统检索/纳排可信度支撑 | 否 | query string 语法为 2010 年特定搜索引擎 |
| EV-v2-011 | paper_content.txt | §6 Limitations | QA4 评分主观性、QA2 不一致性、SLR 报告不充分导致抽取困难 | "the scoring procedure to be too subjective for question QA4 and inconsistent for QA2" | 有效性威胁 | **verified** | method 强度上限 | 否 | — |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CONC-v2-001 | 原文以 9 字段抽取方案 + QA1--QA4 质量评估 + SE Curriculum / SWEBOK 双外部映射构成一个三层维度森林 | 维度树结构判定 | `dim-da-silva-2011-root`, L1, L2, L3 主干 | EV-v2-001, EV-v2-002, EV-v2-004 | **confirmed** | 直接用于重写 review.md §3 维度树复原 | L4（聚合统计层）属于字段消费层，不应混入编码 schema |
| CONC-v2-002 | 本文的维度森林是"多表 schema"而非"单树"，L1/L2/L3 构成可逐篇填充的三张关联表 | 维度树结构判定 | 全部关系边 | EV-v2-003, EV-v2-006, EV-v2-007 | **confirmed** | 指导 Paper2 的 schema 设计为多表结构 | 原文未显式使用 RDB 术语；这是审计复原 |
| CONC-v2-003 | 现有 review.md 以通用六叶替代原生树，需完全重写 | 返修判定（C 级） | review.md A.1 表 | 对比 EV-v2-001--004 与现有 review.md 的 A.1 | **confirmed** | review.md 重写的直接依据 | — |
| CONC-v2-004 | "更新型 tertiary study"模式提供前序关系、合并策略、质量对比三个可迁移字段 | 跨论文启发 | `rel-da-silva-predecessor`, `rel-da-silva-old-vs-new-merge` | EV-v2-001, EV-v2-009 | **confirmed** | 添加到 A1 schema candidate 中 | 合并策略的具体实现依赖继承旧编码方案 |
| CONC-v2-005 | "SLR 更新/扩展缺失"是可迁移的 roadmap 缺口，但不构成 Paper2 的统计证据 | 跨论文候选发现 | Paper2 研究动机 | EV-v2-009 | **confirmed** | 作为 Paper2 的 motivation 引用 | 这是 2011 年的发现，现代 SE SLR 生态可能已改变 |
| CONC-v2-006 | 实践指南不足（28%）和质量评估不足（49% 不做 QA3）是可迁移的方法学一致性观察 | 跨论文候选发现 | Paper2 假设 | EV-v2-007, EV-v2-008 | **confirmed** | 可与其他 tertiary study 交叉验证 | 需核对现代 SE SLR 生态中这两项是否改善 |

---

## 9. 技能使用与自我审查记录

### 已读取技能文件及采用原则

| 技能文件 | 采用的原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | "claim-evidence-engineering workflow" — 每项判定必须有证据锚点；"Evidence gate: repository files outrank memory" |
| `references/reviewer-guidelines.md` | 通用审查维度：originality/quality/clarity/significance；"constructive specificity standard" — 返修建议必须具体到节/表/叶子 |
| `references/reviewer-self-review.md` | "Five-Dimension Review" scoring (pass/needs revision/needs evidence)；"Claim Audit" — 对每个 claim 标记证据、风险、修订动作；"Adversarial Questions" — 从 skeptical reviewer 视角自问 |
| `research-planning/SKILL.md` | "Flag ambiguities explicitly rather than making assumptions" — 对不确定内容显式标注 |
| `references/planning-prompts.md` | "DO NOT FABRICATE DETAILS — only use what is provided" — 所有取值空间只来自原文 |
| `references/output-schemas.md` | 结构化输出模板 — 用于设计叶子维度表和关系边表的结构 |
| `autoresearch/SKILL.md` | "Completion is artifact-gated" — 审计完成的判定标准：所有章节均已填写、证据锚点可追溯 |

### Reviewer 视角最高风险 3 点

1. **risk-high-dimension-forest-structure**：本文的维度森林是一个"多表 schema"（L1 抽取表 + L2 质量表 + L3 教育/实践映射表），不是单棵树。如果主线程合并时强制要求单树结构，可能导致 schema 信息丢失或不当压平。**复核建议**：主线程应明确 Paper2 的目标 schema 是"单编码表"还是"多表维度森林"，并相应调整合并策略。

2. **risk-high-table2-misalignment**：`paper_content.txt` 中 Table 2 的 header 使用了 "Review focus" 列名，但 §3.7 明确定义为 "Review Scope"。这个别名差异在 text 提取中可能只是 OCR 或排版别名，但也可能反映了原文 Table 2 的一列承载了多于一个字段。**复核建议**：在 PDF 核验后确认列语义，并在 leaf 表标注澄清。

3. **risk-medium-pdf-unverified**：Table 2（67 行 × ≥12 列跨页宽表）、Table 5（教育/实践映射）和 Fig. 2（纳排漏斗）是整篇论文统计结论的核心锚点，但本审计未打开 PDF 做版面验证。`paper_content.txt` 的质量虽高（text 模式提取成功），但跨页宽表可能存在列偏移或数据行丢失。**复核建议**：在主线程合并前至少对 Table 2 的前 5 行和后 5 行做 PDF 抽样核对。

### 本轮状态

- **blocked**：否
- **timeout**：否
- **文件缺失**：否（所有指定文件均可读取）
- **PDF 版面核验**：未执行（标记为 `needs_visual_verification`）
- **审计完整性**：所有必填章节均已输出实质内容，无跳节或仅写"不适用"

---

*审计完成时间：2026-06-30 | agent: deepseek | 基于 paper_content.txt 全文 + bibtex.bib + metadata.json + review.md + 7 个技能/参考文件*