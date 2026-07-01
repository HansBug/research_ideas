# Six years of systematic literature reviews in software engineering: An updated tertiary study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Six years of systematic literature reviews in software engineering: An updated tertiary study |
| 年份 | 2011 |
| 类型 | updated tertiary study |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 更新型三级研究；整合前两项 tertiary study 并扩展时间窗口。 |
| SE 子领域 | EBSE / SE 二级研究方法学 |
| A1 角色 | 提供“扩展旧 tertiary study + 自动/人工搜索 + 质量/覆盖/影响分析”的更新型模式。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 历史观察 | 暴露“更新型 tertiary study”需要记录与先前研究的合并/对比字段；已在 schema 中加入 `前序综述关系` 候选字段。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖新时间段数量、主题、活跃作者/机构、旧研究限制是否仍存在、质量是否提升。 | `paper_content.txt` Page 1 abstract；Page 2--3 Method / RQ。 | 可迁移为“增量更新型 survey-of-surveys”模式。 | 更新型 RQ 适合 longitudinal review，不适合所有单次 SLR。 |
| dimension pattern | 维度包括搜索策略、study selection、quality assessment、data extraction、研究主题、教育 / 实践影响。 | `paper_content.txt` Page 1 contents；Page 3--5 Method / Data extraction。 | 可迁移到 A2a 的字段树。 | 教育/实践影响字段有价值，但不能替代目标主题维度。 |
| finding pattern | 发现包括 SLR 数量增长、主题覆盖扩大、质量提升、但多数未评价 原始研究 质量且缺实践指南。 | `paper_content.txt` Page 1 abstract。 | 可迁移为“增长 + 质量 + 影响缺口”的 finding pattern。 | 具体增长和质量结论只属于当年 SE SLR 生态。 |
| evidence presentation pattern | 用 67 个新 SLR、24 个 SE topics、quality assessment、curriculum / practitioner relevance 支撑结论。 | `paper_content.txt` Page 1 abstract；Page 6--10 results/discussion。 | 可迁移为统计表 + 解释性结论。 | 分母与统计方式可迁移，具体数值不可迁移。 |
| validity / threat pattern | 关注搜索过程、前序研究合并、quality assessment 口径和对教育 / 实践影响的解释。 | `paper_content.txt` Page 3--5 Method。 | 可迁移到更新型 review 的 threat 模式。 | 更新型合并风险可参考，但需补现代检索库和开放科学风险。 |
| report structure pattern | Previous studies → Method → Data extraction results → Discussion of RQs → Conclusions。 | `paper_content.txt` Page 1 contents。 | 可迁移，尤其适合 A2b 对旧 / 新样本分层。 | 适合 update/integrate 型综述，非更新型主题需调整。 |

## 3. 对 PR-A1 schema 的启发

1. 新增 `前序综述关系` 字段：是否扩展、复现、整合或更新已有 tertiary study。
2. 新增 `实践 / 教育影响字段`：不能只统计主题，还要问研究发现是否转化为实践/教育建议。
3. 对 finding 必须保留“仍然不足”的负向发现模式，避免只总结增长。
4. 对更新型综述，需记录时间窗和与旧窗口的合并策略。

## 4. 待复核

- 正式引用质量/数量表前需 PDF 表格核对。
- 后续 A2a/A2b 需要补近十年 SE SLR/SMS/survey，以避免 A1 仅受早期 EBSE 文献影响。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | updated tertiary study 展示如何定义“更新 / 扩展 / 整合前序综述”。 | 可迁移 predecessor_relation 字段。 |
| A1-M1 语料收集与纳排 | 展示沿用和扩展前序检索边界的方式。 | 可迁移 update protocol 字段；具体语料年代需降级。 |
| A1-M2 研究对象与主题语义 | 继续组织 SE SLR topic、质量与报告维度。 | 可作为历史对比字段，不支撑现代结论。 |
| A1-M3 方法 / 技术 / 干预 | 主要贡献是二次研究更新方法，不是技术 taxonomy。 | 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 体现质量评价、报告质量和前序研究对齐。 | 可迁移到“复用前序证据时如何记录差异”。 |
| A1-M5 统计分析就绪 | 可形成跨年份 update / trend / quality 分布。 | 必须标注年份窗口。 |
| A1-M6 research finding 形成与裁决 | 从 update 对比中生成方法学 gap 和改进建议。 | 可迁移为“前序差异 -> 新 finding”的启发式。 |

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__codex.md](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__codex.md)、[../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__claude.md](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__claude.md)、[../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__deepseek.md](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md](../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `da-silva-2011-six-years-slr` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是；1625 行全文按页顺序通读（含 Table 2 完整 67 行明细、Table 3 完整 QA 分数明细、Table 4–13、Appendix A 全部 SE01–SE77 引用、References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；二者元数据互相一致 |
| 是否打开或核对 `paper.pdf` | 否；本轮全部以 `paper_content.txt` 文本为准；表格 / 图 (Fig.1 DCP、Fig.2 PRISMA 式流程) 已在文本中识别但未做版面级核验 |
| 原文类型 | SLR 的子型——**updated tertiary 研究**（temporal update + integration of two prior tertiary studies）；同时具备 系统映射研究 性质（本文自称"performed a mapping 研究 of SLRs"） |
| 被编码样本单位 | **已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 |
| 样本数量 / 分母 | SE=67；OS=20；FE=33；OS/FE=53；OS/FE+SE=120；QA assessment N=67（SE 自身）/ 120（整合） |
| 原生树类型 | **维度森林**：(1) 抽取表 模式树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (前序关系: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→发现 路径 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

实际读取的本地文件：
- `bibtex.bib`（11 行，确认 IST 53(9), 899–913, 2011, DOI 10.1016/j.infsof.2011.04.004）
- `metadata.json`（28 行，确认 CCF-B、updated tertiary 研究、`eligible_for_statistical_synthesis=true`）
- `review.md`（当前正文，含通用六叶投影与原生维度树复原；证据链已迁至 evidence_chain.md）
- `paper_content.txt`（1625 行）实际通读覆盖：
  - Page 1：Abstract、Contents、Introduction §1（EBSE 五步、conventional SLR / 系统映射研究 定义）
  - Page 2：§2 Previous studies（OS=20、FE=33、Da Silva 2010 critical appraisal）
  - Page 3：§3 Method（RQ1–RQ5 + 子问题、DCP 决策流程、检索过程 search string）
  - Page 4：§3.4 search engines (6 个)、Table 1 manual search 源、Fig.2 流程 1389→157→154→75→77→67
  - Page 5：§3.6 QA1–QA4 完整 rubric、§3.7 10 字段抽取表完整定义
  - Page 6–8：Table 2 完整 67 篇 SLR × 10 字段明细，含 EBSE/指南 cite 注脚 a–h
  - Page 9：Table 3 完整 67 篇 QA 分数 × QA1–QA4 + Final Score + Quartile
  - Page 10–11：Table 5 SLR↔SE Curriculum↔SWEBOK 映射明细
  - Page 11：Table 6 分布对比、Table 7 作者≥3 SLR、Table 8 国家分布、Table 9 SLR/MS 中位数
  - Page 12：Table 10 实践者指南、Table 11 QA of 原始研究、Table 12 指南 citation、Table 13 质量 trend
  - Page 13：§6 Limitations、§7 Conclusions（含"three complementary ways to update a SLR"——temporal update / search extension / both）
  - Page 14–15：References [1–28]、Appendix A 全部 SE01–SE77 文献条目
- 需要原文版面核验：Fig.1 DCP 图（文字提取较碎）、Fig.2 PRISMA 流程图（数字穿插难解析）、Table 6（SLRs/Subs 双列容易行错位）

5–12 个最关键的原文证据锚点（行号基于 `paper_content.txt`）：

1. **L11–25 Abstract**：原文自述"67 new SLRs addressing 24 software engineering topics" + "15 relevant to undergraduate curriculum, 40 of possible interest to 实践者" + "majority did not evaluate 质量 of 原始研究 and fail to provide 指南 for 实践者"。锚定样本单位为 SLR、分母 67/120 与 发现 边界。
2. **L222–248 §3.1 RQ1–RQ5**：完整列出五个 RQ + RQ1.1/RQ1.2 子问题，含明确时间窗 (2004-01-01 ↔ 2009-12-31)。
3. **L392–433 §3.6 QA1–QA4 rubric**：四题完整定义 + Y/P/N 评分 (Y=1, P=0.5, N=0) 是 质量 维度的封闭枚举取值空间。
4. **L451–468 §3.7 数据抽取（数据抽取）**：明确列出 10 个字段——Year / Quality Score / Review Type (SLR/MA/MS) / 综述范围（Review Scope） (RQ/SERT/RT) / 主题领域 / Cited EBSE / 是否引用指南 / # Primary studies / 实践者指南 / 来源类型 (J/C/WS/BS)。**这是本文原生模式的关键原文依据（A2a 前仍按候选证据管理）**。
5. **L575–771 Table 2**：67 行 × 10 字段的完整 抽取 form 实例化数据；含 EBSE/指南 cite 注脚 a/b/c (EBSE 论文 [14]/[8]/[24]) 与 d/e/f/g/h (指南 文件 [15]/[13]/[16]/[4]/[12])——揭示 "Cited EBSE" 与 "是否引用指南" 不是简单布尔，而是带子引用的关系列。
6. **L826–894 Table 3**：完整 67 篇 × QA1–QA4 × Final Score × Quartile 分布。
7. **L904–1136 Table 5**：每一篇 SLR 对应的 SE2004 Curriculum sub-section + SWEBOK Chapter/Section + "Useful for education" / "Useful for 实践者" (是/否/Possibly) + "Why?" 自由文本——这是显式的**关系边 模式**。
8. **L1162–1196 Table 6**：把 120 篇按 SE2004 Curriculum 10 大节 + SWEBOK 10 章重新交叉统计，并标"Software Configuration Management 与 Software Quality 在 120 篇 OS/FE+SE 中无任何 SLR"——这是典型的 缺口发现（缺口发现） 候选。
9. **L1227–1240 §5.4 RQ4 限制分析**：Quality 评价 21% (14/67) 仍是低 + 三个未做 QA 的原因（混淆 纳入标准、trustworthy source 借口、primary 太少）。
10. **L1342–1363 §7 Conclusions: three complementary ways to update a SLR**：原文显式定义 "temporal update" / "search extension" / "both" 三种 update 模式——这是本文 predecessor 关系类型的封闭枚举。
11. **L1226–1259 §6 Limitations**：QA2 的歧义需要返回原作者咨询、QA4 评分主观、protocol 描述不充分——是 威胁 / 效度 维度证据。
12. **L1472–1624 Appendix A (SE01–SE77)**：67 篇被编码 SLR 的完整书目数据——可作为样本池的版本锚。

### 2. 样本单位与字段来源判定

#### Q1：原文纳入和逐项描述的对象是什么？

**主样本单位：已发表的二级研究 (二次研究)，进一步细分为 conventional SLR / Mapping Study (MS) / Meta-Analysis (MA)。**整合层的样本是 OS/FE+SE = 120 个二级研究。

辅样本单位（衍生 / 关系侧）：
- 作者 (研究者) ——Table 7 列出 21 位 ≥3 SLR 的作者
- 机构 (organisation) ——总计 90 个 (OS/FE 43 + SE 55 - 重叠)
- 国家 / 地区 (country / region) ——SE 8 个新国家、OS/FE+SE 共 25 国
- 主题 (SE topic / Curriculum sub-section / SWEBOK chapter)
- 年份 (2004–2009) ——纵向统计单位

#### Q2：作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**有完整闭环**：
- 检索：6 个自动数据库 (ACM, IEEEXplore, ScienceDirect, CiteSeerX, ISI WoS, Scopus) + 13 本期刊 / 会议手工 (Table 1) + 回溯引用 (reference search)
- 检索式：完整列出 18 个同义短语布尔串 (L292–300)
- 验证：用 OS/FE 53 篇做回测，召回 50/51
- 纳排：1389 → 157（标题摘要初筛）→ 与手工 66 合并去重得 154 → 全文阅读得 75 → 加 [SE76]/[SE77] 反向搜索得 77 → 排除 10 篇得最终 67
- 决策一致性：DCP (Decision and Consensus Procedure)——双人独立打分 + ADT 协议/不一致表 + 第三人裁决 + 全员共识
- QA 校准：10 篇 blind reassessment 与 Kitchenham 2010 对照 (8/10 完全一致，剩余 2 篇各 1 项差异)

#### Q3：原文字段来自哪里？

**主要来自 §3.7 的显式 抽取 form（10 字段）+ §3.6 的 QA rubric（4 题 + Y/P/N 评分）**。实例化结果保存在 Table 2 (10 字段 × 67 行) 和 Table 3 (QA × 67 行)。关系边来自 Table 5 (SLR↔Curriculum↔SWEBOK) 和 Table 7/8 (作者 / 国家)。前序关系来自 §2、§3 文字描述与 §7 三种 update 类型定义。

#### Q4：RQ 与样本单位是什么关系？

RQ 是**统计聚合视角**，不是树根本身。每个 RQ 都对应抽取表中若干字段的聚合或交叉表：
- RQ1（数量增长） = 字段 Year × Cited EBSE/Guidelines 的频次（Table 4）
- RQ2（topic） = 字段 主题领域 × Curriculum × SWEBOK 的分布（Table 5, 6）
- RQ3（个人/组织） = 作者/机构/国家关系图（Table 7, 8）
- RQ4（限制是否仍存在） = QA3 + 实践者指南 + Quality 字段的纵向对比（Table 9–12）
- RQ5（质量提升） = QA1–QA4 final score 的年度均值 / quartile（Table 3, 13）

#### Q5：若无系统样本库，如何降级？

不适用——本文是 systematic 二次研究 with N=120 codable units，有完整模式 和封闭取值空间，**应当进入主统计池**，而不是停留在 `模式种子（schema_seed）`。

### 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**（多棵根并存），不是单树。森林由 6 棵互相挂接的子树构成：

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
森林根节点：软件工程二次研究（二次研究；首次术语；SLR/MS/MA；2004–2009；N=120）
│
├─ T1 [抽取表单] §3.7 抽取表（10 字段）
│  ├─ 年份                          取值 ∈ {2004, 2005, ..., 2009}                  数值/有限枚举
│  ├─ 质量评分                 ∈ [0, 4]，步长 0.5（即 QA1..QA4 之和；Y=1/P=0.5/N=0）  数值
│  ├─ 综述类型（Review Type）取值 ∈ {系统文献综述（SLR）, 元分析（MA）, 系统映射（MS）}                             封闭枚举
│  ├─ 综述范围（Review Scope）取值 ∈ {特定技术问题（RQ）, 软件工程研究趋势（SERT）, 研究方法（RT）}                            封闭枚举
│  │   └ 定义：RQ=特定技术问题（specific technical question）；SERT=软件工程主题趋势；RT=研究方法（research method）
│  ├─ 主题领域                    ∈ 24 个 SE 主题（开放但有 14 个 SE 新增；OS/FE+SE 合计若干）
│  ├─ 是否引用 EBSE 论文              取值 ∈ {N, Y[a], Y[b], Y[c]}                     带子引用的枚举
│  │   └ a=[14] Kitchenham 2004 ICSE, b=[8] Dybå 2005 IEEE SW, c=[24] Rainer&Beecham 2008
│  ├─ 是否引用指南              取值 ∈ {N, Y[d], Y[e], Y[f], Y[g], Y[h], 组合}    多值枚举
│  │   └ d=[15] Kitchenham 2004, e=[13] Kitchenham 2002 prelim, f=[16] K&Charters 2007,
│  │     g=[4] Biolchini 2005, h=[12] Khan 2003
│  ├─ 原始研究数量     ∈ ℕ⁺                                        数值
│  ├─ 是否给出实践者指南       取值 ∈ {Y, N}                                    布尔
│  └─ 来源类型取值 ∈ {J, C, WS, BS}; J=期刊（journal）, C=会议（conference）, WS=工作坊（workshop）, BS=丛书（book series）
│
├─ T2 [质量量规] §3.6 基于 DARE 的质量评估量规
│  ├─ QA1 纳排标准是否合适？    取值 ∈ {Y, P, N} (1 / 0.5 / 0)
│  ├─ QA2 检索是否可能覆盖所有相关研究？  取值 ∈ {Y, P, N}
│  ├─ QA3 评审者是否评估原始研究质量？     取值 ∈ {Y, P, N}
│  ├─ QA4 基础数据 / 研究是否充分描述？     取值 ∈ {Y, P, N}
│  ├─ 最终评分 = QA1+QA2+QA3+QA4 (0..4)
│  └─ 四分位 取值 ∈ {1st, 2nd, 3rd, 4th}
│
├─ T3 [主题分类法] §5.2/§5.4.1 主题分类（三层外部锚定）
│  ├─ 扁平 24 个软件工程主题（flat 24 SE topics；本地自由列表，含 需求 Eng / DSD / SPL / 测试 / ...）
│  ├─ SE 2004 课程映射（SE 2004 Curriculum mapping）
│  │   ├─ 10 大节 (计算基础（计算基础）/ 数学与工程基础（数学与工程基础）/ 专业实践（专业实践）/ 软件建模与分析（软件建模与分析）/
│  │   │           软件设计（SW 设计）/ 软件验证与确认（软件验证与确认）/ 软件演化（软件演化）/ 软件过程（软件过程）/ 软件质量（软件质量）/ 软件管理（软件管理）/
│  │   │           系统与应用专门领域（系统与应用专门领域）)
│  │   └─ 每节多个子小节 (e.g. MGT.pp.5 资源分配（资源分配）, DES.ar.5 领域特定架构（领域特定架构）)
│  └─ SWEBOK 映射（SWEBOK mapping）
│      └─ 10 章 (软件需求（SW 需求）/ 软件设计（SW 设计）/ 软件构造（软件构造）/ 软件测试（SW 测试）/ 软件维护（SW 维护）/
│                 软件配置管理（软件配置管理）/ 软件工程管理（软件工程管理）/ 软件工程过程（软件工程过程）/ 软件工程工具与方法（软件工程工具与方法）/ 软件质量（软件质量）)
│
├─ T4 [人员关系] §5.3 / Table 7-8 人员关系图
│  ├─ 研究者 --作者关系--> 系统综述（SLR）     (N=287 唯一研究者（unique 研究者） OS/FE+SE)
│  ├─ 研究者 --隶属关系--> 机构（organisation）  (90 orgs)
│  └─ 机构（organisation） --所在位置--> 国家   (25 countries) --聚合到--> 地区（region）
│
├─ T5 [前序关系] §7 更新类型（前序关系）
│  └─ 更新类型（更新类型）取值 ∈ {时间更新（时间更新）, 检索扩展（检索扩展）, 组合更新（组合更新）, 无更新（无更新）}
│      └─ 本文自身 = 对 FE 的时间更新（时间更新）；FE 是对 OS 的检索扩展（检索扩展）
│
└─ T6 [教育与实践相关性] Table 5 教育与实践相关性关系树（教育与实践相关性）
   ├─ 教育用途价值取值 ∈ {是（Yes）, 否（No）, 可能（Possibly）}
   ├─ 实践者用途价值取值 ∈ {是（Yes）, 否（No）, 可能（Possibly）}
   └─ 原因说明（why）                          ∈ 自由文本（含 9 种重复出现的模板理由）
```

子统计池可见的"发现 path"：
- T1.主题领域 + T3.Curriculum/SWEBOK → coverage 缺口（gap）（如 软件配置管理 / 软件质量 在 120 篇中为 0）
- T1.Review Type + T1.Number Primary Studies → Median per type per year (Table 9)
- T2.Final Score + T1.来源类型 / Scope / 实践者指南 → 回归 analysis (B 系数全列出)
- T1.Year + T2.Final Score → 质量 trend (Table 13)

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ds11.T1.year | 出版年份 | T1 抽取表 | §3.7 第一项 | 二级研究首次发表年 | 2004–2009 | 数值/有限枚举 | 未出现；预设全部填写 | 纵向 trend 分母 | 数量增长、质量趋势 | L451; Table 4 | 跨年统计可迁移；具体年份不可外推 |
| ds11.T1.qscore | 质量总分 | T1 抽取表 | §3.7 + §3.6 Final Score | ΣQA1..QA4 | [0, 4]，步长 0.5 | 数值 (有限格点) | 未见；零分需说明（[SE74]=0） | 均值 / quartile / 回归 因变量 | 质量提升 / SLR 类型差异 | L452, L826–894 | 评分规则可迁移；rubric 必须显式 |
| ds11.T1.rtype | 研究类型 | T1 抽取表 | §3.7 + Table 2 列 5 | conventional SLR vs MA vs MS | {SLR, MA, MS} | 完整枚举 | OS 不分 MS/SLR 时退化为 SLR；需明确 | 类型分布、主统计池分层 | mapping 比例上升的 发现 | L453–455 | 三分法可迁移；定义需附 PICOC vs exploratory |
| ds11.T1.rscope | 研究范围 | T1 抽取表 | §3.7 + Table 2 列 6 | technical Q vs SE topic trend vs 研究方法（research method） | {RQ, SERT, RT} | 完整枚举 | 无；强制三选一 | scope × score 回归 | "27% 仍是 RT" 是负向 发现 | L456–459 | 三分法可迁移 |
| ds11.T1.topic | 主题领域 | T1 抽取表 | §3.7 + Table 2 列 7 | 文章主题的自由标签 | 24 类 (SE) / OS/FE+SE 合并若干 | 部分封闭层级枚举 | 未见；强制分类 | topic 频次 / coverage 缺口（gap） | "软件质量 / 软件配置管理 = 0" | L460; Table 6 | 主题集合可迁移结构；具体标签不可外推 |
| ds11.T1.ebse_cite | EBSE 文献引用 | T1 抽取表 | §3.7 + 注脚 a–c | 是否引用 3 篇 EBSE 奠基论文 | {N, Y[a], Y[b], Y[c]} 可叠加 | 带子引用枚举 | N = 不引用；多个 Y 可共存 | EBSE positioning 率 | "80% SE positioned" | L461, Table 2 注脚 | 模式可迁移；具体引用列表需更新 |
| ds11.T1.guide_cite | 指南文献引用 | T1 抽取表 | §3.7 + 注脚 d–h | 是否引用 5 类 SLR 指南 | {N, Y[d..h]} 可叠加 | 带子引用枚举 | N = 不引用 | 指南 使用 × 质量 correlation | 回归 显著 (B=0.183) | L462, Table 12 | 模式可迁移；具体指南列表需更新 |
| ds11.T1.nprim | 主研究数量 | T1 抽取表 | §3.7 + Table 2 列 9 | 该 SLR 纳入的 原始研究 数量 | ℕ⁺，本文范围 2–691 | 数值 | 显式或表格隐含；少数需推断 | 与质量 Pearson r=-0.204 | "primary 多 → 质量低" | L463–464; Table 9 | 计数可迁移；阈值不可迁移 |
| ds11.T1.pract_guide | 实践指南 | T1 抽取表 | §3.7 + Table 2 列 10 | 是否显式给出 实践者指南 章节/表 | {Y, N} | 布尔 | 必须 Y/N | 指南 占比 (36%) | "指南 是 EBSE 缺失链路" | L465, Table 10 | 布尔可迁移；判定细则需复用 |
| ds11.T1.source_type | 发表载体 | T1 抽取表 | §3.7 + Table 2 列末 | 期刊/会议/工作坊/丛书 | {J, C, WS, BS} | 封闭枚举 | 强制四选一 | J vs C 质量差 (回归) | "J 比 C 高 0.117 分" | L466–468 | 四分类可迁移 |
| ds11.T2.qa1 | 纳排标准明确性 | T2 QA rubric | §3.6 QA1 | inclusion/exclusion 是否显式 | {Y(1), P(0.5), N(0)} | 完整枚举 | 强制三选一 | 各 quartile 分布 | 几乎全部满分 | L408–411 | rubric 可迁移；评分锚需附定义 |
| ds11.T2.qa2 | 文献搜索覆盖度 | T2 QA rubric | §3.6 QA2 (含 modifications) | 是否覆盖足够多数据库 | {Y, P, N} | 完整枚举 | 强制三选一 | 质量 趋势 | 评分歧义需向原作者咨询 (L1238) | L412–421 | 取值阈值随时代变化 |
| ds11.T2.qa3 | 主研究质量评价 | T2 QA rubric | §3.6 QA3 | 是否显式评价 primary 的 质量 | {Y, P, N} | 完整枚举 | 强制三选一 | "67% SE 做了 QA" | 仍是低指标 (21% 完整 QA) | L422–426 | 可迁移；P 含义需复用 |
| ds11.T2.qa4 | 数据描述充分性 | T2 QA rubric | §3.6 QA4 | 是否可追溯到 individual primary | {Y, P, N} | 完整枚举 | 强制三选一 | 1st quartile 多数失分 | 评分主观（L1238） | L427–433 | 可迁移；主观风险 |
| ds11.T2.quartile | 质量四分位 | T2 QA rubric | Table 3 列 6 | 按 final score 排序后的四分位 | {1st, 2nd, 3rd, 4th} | 完整枚举 | 自动生成 | 描述统计 | 1st 多 QA3/QA4 失分 | Table 3 | 四分位法可迁移 |
| ds11.T3.curri_sec | SE2004 Curriculum 节 | T3 分类法 | §5.2 Table 5/6 列 | 10 个 SE 课程领域 | 10 大节 + 子节 | 层级枚举 (外部锚) | "academic only" 时空缺 | coverage 缺口（gap） | "软件质量 = 0 SLR" | L1162–1196 | 可迁移结构；具体节随版本变 |
| ds11.T3.swebok_ch | SWEBOK 章 | T3 分类法 | §5.2 Table 5/6 列 | 10 章 SWEBOK | 10 章 + 节 | 层级枚举 (外部锚) | 同上 | coverage 缺口（gap） | "软件配置管理 = 0" | L1162–1196 | 同上 |
| ds11.T4.研究者 | 作者实体 | T4 关系图 | §5.3 / Table 7 | 单个作者 / 国家 / SLR 计数 | 自由文本 + 计数 | 实体 + 整数 | name 拼写差异需对齐 | top-N、Lorenz 曲线 | "10 个新作者进入≥3 SLR 群" | L701–712; Table 7 | 作者实体可迁移；具体人名不可 |
| ds11.T4.country | 国家 | T4 关系图 | Table 8 | 6 个地理区域 + 国家 | 6 region + 25 country | 完整枚举 (外部) | 0 = 该年/区无 SLR | 区域分布 | "USA<12%、Asia 从 0→15%" | L715–727; Table 8 | 区域结构可迁移 |
| ds11.T5.更新类型 | 前序更新关系 | T5 predecessor | §7 三种 update | 与前序 SLR 的关系 | {时间更新, 检索扩展, 组合类（组合类）, 无更新} | 完整枚举 | "无更新" 是默认 | 本文与 OS/FE 关系定位 | "120 篇中无内部 update" 是 缺口发现（缺口发现） | L1343–1363 | 三类划分可迁移到任何 update review |
| ds11.T6.edu | 对教育有用 | T6 relevance | Table 5 列 4 | 是否适合本科课程 | {是（Yes）, 否（No）, 可能（Possibly）} | 完整枚举 | 强制三选一 | 教育影响占比 (15/67) | "15 篇适合 curriculum" | Table 5 | 三态可迁移；判定靠人工 |
| ds11.T6.pract | 对实践有用 | T6 relevance | Table 5 列 5 | 是否适合实践者 | {是（Yes）, 否（No）, 可能（Possibly）} | 完整枚举 | 强制三选一 | 实践影响占比 (40/67) | "40 of possible interest" | Table 5 | 同上 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| ds11.E1 | SLR (sample) | covers_topic | 主题领域 | 24 SE topics | "general" 时归 SW Development | Table 2 | topic distribution |
| ds11.E2 | SLR | maps_to | SE2004 Curriculum sub-section | 10 大节×子节 | "academic only" 时不映射 | Table 5 | curriculum coverage |
| ds11.E3 | SLR | maps_to | SWEBOK Chapter/Section | 10 章×节 | "N/A" 显式标 | Table 5 | SWEBOK coverage |
| ds11.E4 | SLR | authored_by | 研究者 | 人名实体 | 必填 | App.A、Table 7 | author productivity |
| ds11.E5 | 研究者 | affiliated_with | Organisation | 90 个 | name normalisation 后聚合 | Table 7 | organisation analysis |
| ds11.E6 | Organisation | located_in | Country/Region | 25 国 / 6 区 | 必填 | Table 8 | regional spread |
| ds11.E7 | SLR | cites_ebse_paper | EBSE seminal paper | [14]/[8]/[24] | 多引用并存 | Table 2 注脚 a–c | EBSE positioning |
| ds11.E8 | SLR | cites_指南 | SLR 指南 | [15]/[13]/[16]/[4]/[12] | 多引用并存 | Table 2 注脚 d–h | 指南 use |
| ds11.E9 | SLR_new | updates / extends | SLR_prev | {时间更新, 检索扩展, 组合类（组合类）} | 0 例（发现 本身）| §7 | predecessor 模式 |
| ds11.E10 | SLR | analyses | primary_study_count | ℕ⁺ | 必填 | Table 2 | size × 质量 |
| ds11.E11 | SLR | published_in | Venue + 来源类型 | J/C/WS/BS + venue 名 | 必填 | Table 1, Table 2 | venue analysis |

本文具有显式关系型 模式（E2/E3/E4–E6/E7–E8 都是 many-to-many 外键关系），明显比一般 SLR 丰富。

### 6. 统计观察、候选发现 与 最终发现边界

#### A. 字段 / 统计表直接支撑的统计观察（high confidence，可入主统计池）

1. **OS/FE+SE 中 SE topics 数量分布**：24 个新主题 + 14 个 OS/FE 已有；6 个主题占 55% (经验研究方法（Empirical Research Methods） 16 / Cost 13 / RE 10 / DSD 9 / SW Dev 9 / 测试 9 / Maint 7)（L774–786）
2. **Quality trend**：2004 Mean=2.08 → 2009 Mean=2.61，6 年内 +12.5%（Table 13）
3. **Cited 指南 × 质量 回归**：B=0.183, p=0.000（L1212–1214）
4. **实践者指南 提升**：OS/FE 17% → SE 36% → 整合 28%（Table 10）
5. **QA of 原始研究 提升**：OS/FE 30% → SE 67% → 整合 51%（Table 11）
6. **Median 原始研究 per SLR/MS**：MS 显著高于 SLR（Table 9，例：2006 MS=403.5 vs SLR=7）
7. **Number primary × 质量 Pearson r=-0.204, p=0.05** (N=120)

#### B. 候选发现 / discussion 命题（needs cross-paper verification）

1. "SLR 数量增长但仍 majority 未做 质量评价" ——本文自陈但属于单篇 discussion
2. "USA 参与度<12% 表明 EBSE 集中在欧洲" ——单时点观察，需结合 2010 后数据
3. "MS 比例从 32% → 82%" ——部分由于本文采用 Da Silva 2010 的新分类法，**作者明确说重新用此法对 OS/FE 重算得 72% MS**，存在测量偏移
4. "EBSE 未被完全实现" ——§7 conclusion 命题，需 field survey 验证
5. "SW Configuration Management 与 软件质量 在 120 SLR 中是 0" ——这是**可统计的 缺口发现（缺口发现）**（不是仅 discussion），但仅锚定 2004–2009 窗口

#### C. 对 Paper2 可迁移的方法学启发

1. **10 字段抽取表 + QA1–QA4 rubric** 是 secondary 类研究的可复用 模式 骨架
2. **DCP (Decision and Consensus Procedure)** 提供了多人编码的可追溯流程
3. **Topic ↔ Curriculum/SWEBOK 双重外部锚定** 是把 local topic 分类法 与外部权威分类法绑定的高质量做法
4. **三种 update 类型** (temporal/search/组合类（组合类）) 是 update review 的可迁移分类
5. **回归 of 质量 因变量 × 多分类预测变量** 是统计 发现 的合规路径

#### D. 绝不能迁移的领域结论

1. 具体数字 (67、120、Quality Mean、Pearson r、回归 B) ——只属于 2004–2009 SE SLR 窗口
2. 具体 topic 标签（如 "DSD / SPL / 测试" 是 SE 2009 的领域结构，不可外推到 STM / LLM4SE）
3. 具体作者排行榜（Table 7）/ 国家排名（Table 8）——10 年后已大幅变化
4. EBSE / SWEBOK / SE2004 Curriculum 三个外部锚——版本已更新（SWEBOK 现为 v4 2024）
5. "QA3 21% 完整" 这类绝对水平——后续 SLR 实践已成熟，重测会显著不同

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
