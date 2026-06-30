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
| finding pattern | 发现包括 SLR 数量增长、主题覆盖扩大、质量提升、但多数未评价 primary study 质量且缺实践指南。 | `paper_content.txt` Page 1 abstract。 | 可迁移为“增长 + 质量 + 影响缺口”的 finding pattern。 | 具体增长和质量结论只属于当年 SE SLR 生态。 |
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
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 leaf / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生 schema。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__codex.md](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__codex.md)、[../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__claude.md](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__claude.md)、[../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__deepseek.md](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md](../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修 / needs repair”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 supplementary 精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `da-silva-2011-six-years-slr` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；1625 行全文按页顺序通读（含 Table 2 完整 67 行明细、Table 3 完整 QA 分数明细、Table 4–13、Appendix A 全部 SE01–SE77 引用、References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；二者元数据互相一致 |
| 是否打开或核对 `paper.pdf` | 否；本轮全部以 `paper_content.txt` 文本为准；表格 / 图 (Fig.1 DCP、Fig.2 PRISMA 式流程) 已在文本中识别但未做版面级核验 |
| 原文类型 | SLR 的子型——**updated tertiary study**（temporal update + integration of two prior tertiary studies）；同时具备 mapping study 性质（本文自称"performed a mapping study of SLRs"） |
| 被编码样本单位 | **已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 |
| 样本数量 / 分母 | SE=67；OS=20；FE=33；OS/FE=53；OS/FE+SE=120；QA assessment N=67（SE 自身）/ 120（整合） |
| 原生树类型 | **维度森林**：(1) 抽取表 schema 树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (predecessor relation: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→finding 路径 |
| 主统计池资格 | **是**——具备完整系统检索（自动+人工+回溯）、显式纳排、quality assessment、可分母统计字段；当前 `review.md` 把它标 `schema_seed` 是低估 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 needs repair；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、supplementary 风险进入 A2a。 |

### 1. 原文证据阅读说明

实际读取的本地文件：
- `bibtex.bib`（11 行，确认 IST 53(9), 899–913, 2011, DOI 10.1016/j.infsof.2011.04.004）
- `metadata.json`（28 行，确认 CCF-B、updated tertiary study、`eligible_for_statistical_synthesis=true`）
- `review.md`（221 行，含 v1 v2 历史返修标记 + 通用六叶 + "原文 schema 主树(19×3 审计后返修)"草案）
- `paper_content.txt`（1625 行）实际通读覆盖：
  - Page 1：Abstract、Contents、Introduction §1（EBSE 五步、conventional SLR / mapping study 定义）
  - Page 2：§2 Previous studies（OS=20、FE=33、Da Silva 2010 critical appraisal）
  - Page 3：§3 Method（RQ1–RQ5 + 子问题、DCP 决策流程、search process search string）
  - Page 4：§3.4 search engines (6 个)、Table 1 manual search 源、Fig.2 流程 1389→157→154→75→77→67
  - Page 5：§3.6 QA1–QA4 完整 rubric、§3.7 10 字段抽取表完整定义
  - Page 6–8：Table 2 完整 67 篇 SLR × 10 字段明细，含 EBSE/guideline cite 注脚 a–h
  - Page 9：Table 3 完整 67 篇 QA 分数 × QA1–QA4 + Final Score + Quartile
  - Page 10–11：Table 5 SLR↔SE Curriculum↔SWEBOK 映射明细
  - Page 11：Table 6 分布对比、Table 7 作者≥3 SLR、Table 8 国家分布、Table 9 SLR/MS 中位数
  - Page 12：Table 10 practitioner guidelines、Table 11 QA of primary studies、Table 12 guideline citation、Table 13 quality trend
  - Page 13：§6 Limitations、§7 Conclusions（含"three complementary ways to update a SLR"——temporal update / search extension / both）
  - Page 14–15：References [1–28]、Appendix A 全部 SE01–SE77 文献条目
- 需要 PDF 视觉核验：Fig.1 DCP 图（文字提取较碎）、Fig.2 PRISMA 流程图（数字穿插难解析）、Table 6（SLRs/Subs 双列容易行错位）

5–12 个最关键的原文证据锚点（行号基于 `paper_content.txt`）：

1. **L11–25 Abstract**：原文自述"67 new SLRs addressing 24 software engineering topics" + "15 relevant to undergraduate curriculum, 40 of possible interest to practitioners" + "majority did not evaluate quality of primary studies and fail to provide guidelines for practitioners"。锚定样本单位为 SLR、分母 67/120 与 finding 边界。
2. **L222–248 §3.1 RQ1–RQ5**：完整列出五个 RQ + RQ1.1/RQ1.2 子问题，含明确时间窗 (2004-01-01 ↔ 2009-12-31)。
3. **L392–433 §3.6 QA1–QA4 rubric**：四题完整定义 + Y/P/N 评分 (Y=1, P=0.5, N=0) 是 quality 维度的封闭枚举取值空间。
4. **L451–468 §3.7 Data extraction**：明确列出 10 个字段——Year / Quality Score / Review Type (SLR/MA/MS) / Review Scope (RQ/SERT/RT) / Topic Area / Cited EBSE / Cited Guidelines / # Primary studies / Practitioner Guidelines / Source Type (J/C/WS/BS)。**这是本文原生 schema 的最强证据**。
5. **L575–771 Table 2**：67 行 × 10 字段的完整 extraction form 实例化数据；含 EBSE/guideline cite 注脚 a/b/c (EBSE 论文 [14]/[8]/[24]) 与 d/e/f/g/h (guideline 文件 [15]/[13]/[16]/[4]/[12])——揭示 "Cited EBSE" 与 "Cited Guidelines" 不是简单布尔，而是带子引用的关系列。
6. **L826–894 Table 3**：完整 67 篇 × QA1–QA4 × Final Score × Quartile 分布。
7. **L904–1136 Table 5**：每一篇 SLR 对应的 SE2004 Curriculum sub-section + SWEBOK Chapter/Section + "Useful for education" / "Useful for practitioner" (Yes/No/Possibly) + "Why?" 自由文本——这是显式的**关系边 schema**。
8. **L1162–1196 Table 6**：把 120 篇按 SE2004 Curriculum 10 大节 + SWEBOK 10 章重新交叉统计，并标"Software Configuration Management 与 Software Quality 在 120 篇 OS/FE+SE 中无任何 SLR"——这是典型的 gap finding 候选。
9. **L1227–1240 §5.4 RQ4 限制分析**：Quality evaluation 21% (14/67) 仍是低 + 三个未做 QA 的原因（混淆 inclusion criteria、trustworthy source 借口、primary 太少）。
10. **L1342–1363 §7 Conclusions: three complementary ways to update a SLR**：原文显式定义 "temporal update" / "search extension" / "both" 三种 update 模式——这是本文 predecessor 关系类型的封闭枚举。
11. **L1226–1259 §6 Limitations**：QA2 的歧义需要返回原作者咨询、QA4 评分主观、protocol 描述不充分——是 threat / validity 维度证据。
12. **L1472–1624 Appendix A (SE01–SE77)**：67 篇被编码 SLR 的完整书目数据——可作为样本池的版本锚。

### 2. 样本单位与字段来源判定

#### Q1：原文纳入和逐项描述的对象是什么？

**主样本单位：已发表的二级研究 (secondary study)，进一步细分为 conventional SLR / Mapping Study (MS) / Meta-Analysis (MA)。**整合层的样本是 OS/FE+SE = 120 个二级研究。

辅样本单位（衍生 / 关系侧）：
- 作者 (researcher) ——Table 7 列出 21 位 ≥3 SLR 的作者
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

**主要来自 §3.7 的显式 extraction form（10 字段）+ §3.6 的 QA rubric（4 题 + Y/P/N 评分）**。实例化结果保存在 Table 2 (10 字段 × 67 行) 和 Table 3 (QA × 67 行)。关系边来自 Table 5 (SLR↔Curriculum↔SWEBOK) 和 Table 7/8 (作者 / 国家)。前序关系来自 §2、§3 文字描述与 §7 三种 update 类型定义。

#### Q4：RQ 与样本单位是什么关系？

RQ 是**统计聚合视角**，不是树根本身。每个 RQ 都对应抽取表中若干字段的聚合或交叉表：
- RQ1（数量增长） = 字段 Year × Cited EBSE/Guidelines 的频次（Table 4）
- RQ2（topic） = 字段 Topic Area × Curriculum × SWEBOK 的分布（Table 5, 6）
- RQ3（个人/组织） = 作者/机构/国家关系图（Table 7, 8）
- RQ4（限制是否仍存在） = QA3 + Practitioner Guidelines + Quality 字段的纵向对比（Table 9–12）
- RQ5（质量提升） = QA1–QA4 final score 的年度均值 / quartile（Table 3, 13）

#### Q5：若无系统样本库，如何降级？

不适用——本文是 systematic secondary study with N=120 codable units，有完整 schema 和封闭取值空间，**应当进入主统计池**，而不是停留在 `schema_seed`。

### 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**（多棵根并存），不是单树。森林由 6 棵互相挂接的子树构成：

```text
Forest root: secondary study (SLR/MS/MA) in software engineering, 2004–2009, N=120
│
├─ T1 [extraction-form] §3.7 抽取表 (10 字段)
│  ├─ Year                          ∈ {2004, 2005, ..., 2009}                  数值/有限枚举
│  ├─ Quality Score                 ∈ [0, 4] 步长 0.5 (= ΣQA1..QA4 with Y=1/P=0.5/N=0)  数值
│  ├─ Review Type                   ∈ {SLR, MA, MS}                             封闭枚举
│  ├─ Review Scope                  ∈ {RQ, SERT, RT}                            封闭枚举
│  │   └ 定义：RQ=specific technical Q；SERT=trends in a SE topic；RT=research methods
│  ├─ Topic Area                    ∈ 24 个 SE topics（开放但有 14 个 SE 新增；OS/FE+SE 合计若干）
│  ├─ Cited EBSE paper              ∈ {N, Y[a], Y[b], Y[c]}                     带子引用的枚举
│  │   └ a=[14] Kitchenham 2004 ICSE, b=[8] Dybå 2005 IEEE SW, c=[24] Rainer&Beecham 2008
│  ├─ Cited Guidelines              ∈ {N, Y[d], Y[e], Y[f], Y[g], Y[h], 组合}    多值枚举
│  │   └ d=[15] Kitchenham 2004, e=[13] Kitchenham 2002 prelim, f=[16] K&Charters 2007,
│  │     g=[4] Biolchini 2005, h=[12] Khan 2003
│  ├─ Number of Primary Studies     ∈ ℕ⁺                                        数值
│  ├─ Practitioner Guidelines       ∈ {Y, N}                                    布尔
│  └─ Source Type                   ∈ {J, C, WS, BS}; J=journal, C=conf, WS=workshop, BS=book series
│
├─ T2 [quality-rubric] §3.6 DARE-based QA rubric
│  ├─ QA1 inclusion/exclusion criteria appropriate?    ∈ {Y, P, N} (1 / 0.5 / 0)
│  ├─ QA2 search likely covered all relevant studies?  ∈ {Y, P, N}
│  ├─ QA3 reviewers assessed quality of primaries?     ∈ {Y, P, N}
│  ├─ QA4 basic data/studies adequately described?     ∈ {Y, P, N}
│  ├─ Final Score = QA1+QA2+QA3+QA4 (0..4)
│  └─ Quartile ∈ {1st, 2nd, 3rd, 4th}
│
├─ T3 [topic-taxonomy] §5.2/§5.4.1 主题分类（三层外部锚定）
│  ├─ flat 24 SE topics（local 自由列表，含 Requirements Eng / DSD / SPL / Testing / ...）
│  ├─ SE 2004 Curriculum mapping
│  │   ├─ 10 大节 (Computing Essentials / Math&Eng Fund / Prof Practice / SW Modelling&Analysis /
│  │   │           SW Design / SW V&V / SW Evolution / SW Process / SW Quality / SW Mgt /
│  │   │           Systems&App Specialties)
│  │   └─ 每节多个子小节 (e.g. MGT.pp.5 Resource allocation, DES.ar.5 Domain-specific architectures)
│  └─ SWEBOK mapping
│      └─ 10 章 (SW Requirements / SW Design / SW Construction / SW Testing / SW Maintenance /
│                 SW Config Mgt / SW Eng Mgt / SW Eng Process / SW Eng Tools&Methods / SW Quality)
│
├─ T4 [people-relation] §5.3 / Table 7-8 关系图
│  ├─ researcher  --authors-->  SLR     (N=287 unique researchers OS/FE+SE)
│  ├─ researcher  --affiliation-->  organisation  (90 orgs)
│  └─ organisation --located-->  country   (25 countries) --aggregated-into--> region
│
├─ T5 [predecessor-relation] §7 update 类型
│  └─ update_type ∈ {temporal_update, search_extension, combined, none}
│      └─ 本文自身=temporal_update of FE; FE was search_extension of OS
│
└─ T6 [education-practice-relevance] Table 5 关系树
   ├─ usefulness_for_education     ∈ {Yes, No, Possibly}
   ├─ usefulness_for_practitioner  ∈ {Yes, No, Possibly}
   └─ why?                          ∈ 自由文本（含 9 种重复出现的模板理由）
```

子统计池可见的"finding path"：
- T1.Topic Area + T3.Curriculum/SWEBOK → coverage gap（如 SW Config Mgt / SW Quality 在 120 篇中为 0）
- T1.Review Type + T1.Number Primary Studies → Median per type per year (Table 9)
- T2.Final Score + T1.Source Type / Scope / Practitioner Guidelines → regression analysis (B 系数全列出)
- T1.Year + T2.Final Score → quality trend (Table 13)

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ds11.T1.year | 出版年份 | T1 抽取表 | §3.7 第一项 | 二级研究首次发表年 | 2004–2009 | 数值/有限枚举 | 未出现；预设全部填写 | 纵向 trend 分母 | 数量增长、质量趋势 | L451; Table 4 | 跨年统计可迁移；具体年份不可外推 |
| ds11.T1.qscore | 质量总分 | T1 抽取表 | §3.7 + §3.6 Final Score | ΣQA1..QA4 | [0, 4]，步长 0.5 | 数值 (有限格点) | 未见；零分需说明（[SE74]=0） | 均值 / quartile / regression 因变量 | 质量提升 / SLR 类型差异 | L452, L826–894 | 评分规则可迁移；rubric 必须显式 |
| ds11.T1.rtype | 研究类型 | T1 抽取表 | §3.7 + Table 2 列 5 | conventional SLR vs MA vs MS | {SLR, MA, MS} | 完整枚举 | OS 不分 MS/SLR 时退化为 SLR；需明确 | 类型分布、主统计池分层 | mapping 比例上升的 finding | L453–455 | 三分法可迁移；定义需附 PICOC vs exploratory |
| ds11.T1.rscope | 研究范围 | T1 抽取表 | §3.7 + Table 2 列 6 | technical Q vs SE topic trend vs research methods | {RQ, SERT, RT} | 完整枚举 | 无；强制三选一 | scope × score regression | "27% 仍是 RT" 是负向 finding | L456–459 | 三分法可迁移 |
| ds11.T1.topic | 主题领域 | T1 抽取表 | §3.7 + Table 2 列 7 | 文章主题的自由标签 | 24 类 (SE) / OS/FE+SE 合并若干 | 部分封闭层级枚举 | 未见；强制分类 | topic frequency / coverage gap | "SW Quality / SW Config Mgt = 0" | L460; Table 6 | 主题集合可迁移结构；具体标签不可外推 |
| ds11.T1.ebse_cite | EBSE 文献引用 | T1 抽取表 | §3.7 + 注脚 a–c | 是否引用 3 篇 EBSE 奠基论文 | {N, Y[a], Y[b], Y[c]} 可叠加 | 带子引用枚举 | N = 不引用；多个 Y 可共存 | EBSE positioning 率 | "80% SE positioned" | L461, Table 2 注脚 | 模式可迁移；具体引用列表需更新 |
| ds11.T1.guide_cite | 指南文献引用 | T1 抽取表 | §3.7 + 注脚 d–h | 是否引用 5 类 SLR guideline | {N, Y[d..h]} 可叠加 | 带子引用枚举 | N = 不引用 | guideline 使用 × 质量 correlation | regression 显著 (B=0.183) | L462, Table 12 | 模式可迁移；具体指南列表需更新 |
| ds11.T1.nprim | 主研究数量 | T1 抽取表 | §3.7 + Table 2 列 9 | 该 SLR 纳入的 primary study 数量 | ℕ⁺，本文范围 2–691 | 数值 | 显式或表格隐含；少数需推断 | 与质量 Pearson r=-0.204 | "primary 多 → 质量低" | L463–464; Table 9 | 计数可迁移；阈值不可迁移 |
| ds11.T1.pract_guide | 实践指南 | T1 抽取表 | §3.7 + Table 2 列 10 | 是否显式给出 practitioner guideline 章节/表 | {Y, N} | 布尔 | 必须 Y/N | guideline 占比 (36%) | "guideline 是 EBSE 缺失链路" | L465, Table 10 | 布尔可迁移；判定细则需复用 |
| ds11.T1.source_type | 发表载体 | T1 抽取表 | §3.7 + Table 2 列末 | 期刊/会议/工作坊/丛书 | {J, C, WS, BS} | 封闭枚举 | 强制四选一 | J vs C 质量差 (regression) | "J 比 C 高 0.117 分" | L466–468 | 四分类可迁移 |
| ds11.T2.qa1 | 纳排标准明确性 | T2 QA rubric | §3.6 QA1 | inclusion/exclusion 是否显式 | {Y(1), P(0.5), N(0)} | 完整枚举 | 强制三选一 | 各 quartile 分布 | 几乎全部满分 | L408–411 | rubric 可迁移；评分锚需附定义 |
| ds11.T2.qa2 | 文献搜索覆盖度 | T2 QA rubric | §3.6 QA2 (含 modifications) | 是否覆盖足够多数据库 | {Y, P, N} | 完整枚举 | 强制三选一 | quality 趋势 | 评分歧义需向原作者咨询 (L1238) | L412–421 | 取值阈值随时代变化 |
| ds11.T2.qa3 | 主研究质量评价 | T2 QA rubric | §3.6 QA3 | 是否显式评价 primary 的 quality | {Y, P, N} | 完整枚举 | 强制三选一 | "67% SE 做了 QA" | 仍是低指标 (21% 完整 QA) | L422–426 | 可迁移；P 含义需复用 |
| ds11.T2.qa4 | 数据描述充分性 | T2 QA rubric | §3.6 QA4 | 是否可追溯到 individual primary | {Y, P, N} | 完整枚举 | 强制三选一 | 1st quartile 多数失分 | 评分主观（L1238） | L427–433 | 可迁移；主观风险 |
| ds11.T2.quartile | 质量四分位 | T2 QA rubric | Table 3 列 6 | 按 final score 排序后的四分位 | {1st, 2nd, 3rd, 4th} | 完整枚举 | 自动生成 | 描述统计 | 1st 多 QA3/QA4 失分 | Table 3 | 四分位法可迁移 |
| ds11.T3.curri_sec | SE2004 Curriculum 节 | T3 taxonomy | §5.2 Table 5/6 列 | 10 个 SE 课程领域 | 10 大节 + 子节 | 层级枚举 (外部锚) | "academic only" 时空缺 | coverage gap | "SW Quality = 0 SLR" | L1162–1196 | 可迁移结构；具体节随版本变 |
| ds11.T3.swebok_ch | SWEBOK 章 | T3 taxonomy | §5.2 Table 5/6 列 | 10 章 SWEBOK | 10 章 + 节 | 层级枚举 (外部锚) | 同上 | coverage gap | "SW Config Mgt = 0" | L1162–1196 | 同上 |
| ds11.T4.researcher | 作者实体 | T4 关系图 | §5.3 / Table 7 | 单个作者 / 国家 / SLR 计数 | 自由文本 + 计数 | 实体 + 整数 | name 拼写差异需对齐 | top-N、Lorenz 曲线 | "10 个新作者进入≥3 SLR 群" | L701–712; Table 7 | 作者实体可迁移；具体人名不可 |
| ds11.T4.country | 国家 | T4 关系图 | Table 8 | 6 个地理区域 + 国家 | 6 region + 25 country | 完整枚举 (外部) | 0 = 该年/区无 SLR | 区域分布 | "USA<12%、Asia 从 0→15%" | L715–727; Table 8 | 区域结构可迁移 |
| ds11.T5.update_type | 前序更新关系 | T5 predecessor | §7 三种 update | 与前序 SLR 的关系 | {temporal_update, search_extension, combined, none} | 完整枚举 | "none" 是默认 | 本文与 OS/FE 关系定位 | "120 篇中无内部 update" 是 gap finding | L1343–1363 | 三类划分可迁移到任何 update review |
| ds11.T6.edu | 对教育有用 | T6 relevance | Table 5 列 4 | 是否适合本科课程 | {Yes, No, Possibly} | 完整枚举 | 强制三选一 | 教育影响占比 (15/67) | "15 篇适合 curriculum" | Table 5 | 三态可迁移；判定靠人工 |
| ds11.T6.pract | 对实践有用 | T6 relevance | Table 5 列 5 | 是否适合实践者 | {Yes, No, Possibly} | 完整枚举 | 强制三选一 | 实践影响占比 (40/67) | "40 of possible interest" | Table 5 | 同上 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| ds11.E1 | SLR (sample) | covers_topic | Topic Area | 24 SE topics | "general" 时归 SW Development | Table 2 | topic distribution |
| ds11.E2 | SLR | maps_to | SE2004 Curriculum sub-section | 10 大节×子节 | "academic only" 时不映射 | Table 5 | curriculum coverage |
| ds11.E3 | SLR | maps_to | SWEBOK Chapter/Section | 10 章×节 | "N/A" 显式标 | Table 5 | SWEBOK coverage |
| ds11.E4 | SLR | authored_by | Researcher | 人名实体 | 必填 | App.A、Table 7 | author productivity |
| ds11.E5 | Researcher | affiliated_with | Organisation | 90 个 | name normalisation 后聚合 | Table 7 | organisation analysis |
| ds11.E6 | Organisation | located_in | Country/Region | 25 国 / 6 区 | 必填 | Table 8 | regional spread |
| ds11.E7 | SLR | cites_ebse_paper | EBSE seminal paper | [14]/[8]/[24] | 多引用并存 | Table 2 注脚 a–c | EBSE positioning |
| ds11.E8 | SLR | cites_guideline | SLR guideline | [15]/[13]/[16]/[4]/[12] | 多引用并存 | Table 2 注脚 d–h | guideline use |
| ds11.E9 | SLR_new | updates / extends | SLR_prev | {temporal_update, search_extension, combined} | 0 例（finding 本身）| §7 | predecessor pattern |
| ds11.E10 | SLR | analyses | primary_study_count | ℕ⁺ | 必填 | Table 2 | size × quality |
| ds11.E11 | SLR | published_in | Venue + Source Type | J/C/WS/BS + venue 名 | 必填 | Table 1, Table 2 | venue analysis |

本文具有显式关系型 schema（E2/E3/E4–E6/E7–E8 都是 many-to-many 外键关系），明显比一般 SLR 丰富。

### 6. 统计观察、候选 finding 与 final finding 边界

#### A. 字段 / 统计表直接支撑的统计观察（high confidence，可入主统计池）

1. **OS/FE+SE 中 SE topics 数量分布**：24 个新主题 + 14 个 OS/FE 已有；6 个主题占 55% (Empirical Research Methods 16 / Cost 13 / RE 10 / DSD 9 / SW Dev 9 / Testing 9 / Maint 7)（L774–786）
2. **Quality trend**：2004 Mean=2.08 → 2009 Mean=2.61，6 年内 +12.5%（Table 13）
3. **Cited guidelines × quality regression**：B=0.183, p=0.000（L1212–1214）
4. **Practitioner Guidelines 提升**：OS/FE 17% → SE 36% → 整合 28%（Table 10）
5. **QA of primary studies 提升**：OS/FE 30% → SE 67% → 整合 51%（Table 11）
6. **Median primary studies per SLR/MS**：MS 显著高于 SLR（Table 9，例：2006 MS=403.5 vs SLR=7）
7. **Number primary × quality Pearson r=-0.204, p=0.05** (N=120)

#### B. 候选 finding / discussion 命题（needs cross-paper verification）

1. "SLR 数量增长但仍 majority 未做 quality assessment" ——本文自陈但属于单篇 discussion
2. "USA 参与度<12% 表明 EBSE 集中在欧洲" ——单时点观察，需结合 2010 后数据
3. "MS 比例从 32% → 82%" ——部分由于本文采用 Da Silva 2010 的新分类法，**作者明确说重新用此法对 OS/FE 重算得 72% MS**，存在测量偏移
4. "EBSE 未被完全实现" ——§7 conclusion 命题，需 field survey 验证
5. "SW Configuration Management 与 SW Quality 在 120 SLR 中是 0" ——这是**可统计的 gap finding**（不是仅 discussion），但仅锚定 2004–2009 窗口

#### C. 对 Paper2 可迁移的方法学启发

1. **10 字段抽取表 + QA1–QA4 rubric** 是 secondary 类研究的可复用 schema 骨架
2. **DCP (Decision and Consensus Procedure)** 提供了多人编码的可追溯流程
3. **Topic ↔ Curriculum/SWEBOK 双重外部锚定** 是把 local topic taxonomy 与外部权威分类法绑定的高质量做法
4. **三种 update 类型** (temporal/search/combined) 是 update review 的可迁移分类
5. **regression of quality 因变量 × 多分类预测变量** 是统计 finding 的合规路径

#### D. 绝不能迁移的领域结论

1. 具体数字 (67、120、Quality Mean、Pearson r、regression B) ——只属于 2004–2009 SE SLR 窗口
2. 具体 topic 标签（如 "DSD / SPL / Testing" 是 SE 2009 的领域结构，不可外推到 STM / LLM4SE）
3. 具体作者排行榜（Table 7）/ 国家排名（Table 8）——10 年后已大幅变化
4. EBSE / SWEBOK / SE2004 Curriculum 三个外部锚——版本已更新（SWEBOK 现为 v4 2024）
5. "QA3 21% 完整" 这类绝对水平——后续 SLR 实践已成熟，重测会显著不同

### 7. 对旧版 `review.md` 的返修来源

#### Critical（C）— 影响 schema 学术真值，必修

**C1** ── `review.md` 当前 §"维度树结构" 把 [leaf-...-scope/corpus/taxonomy/method/evidence/finding] 六个**跨论文通用接口**当成本文原生叶子。这与原文 §3.7 给出的 10 字段 extraction form + §3.6 的 QA1–QA4 rubric 严重错位。必须把 **T1 抽取表 (10 字段)** 和 **T2 QA rubric (4 题 + Final + Quartile)** 提升为原文事实源，把六叶接口降级为 §"通用接口投影" 的下挂注。

**C2** ── 当前 §"原文 schema 主树（19×3 审计后返修）" 表只有 6 行 (rq-main / predecessor-update / extraction-form / quality-qa / topic-impact / limitation-finding)，且取值空间字段几乎全空。必须填充：(a) 10 字段 extraction form 的每一字段取值空间（已在本报告 §4 给出）；(b) QA1–QA4 的 Y/P/N 评分阈值；(c) update_type 的 {temporal/search/combined} 三值枚举。

**C3** ── `metadata.json` 已经标 `eligible_for_statistical_synthesis: true`，但 `review.md` "统计与候选发现链路" 表把所有节点写成 `否（A1-DT 阶段仅作 schema seed）`。这是不一致：本文的 67 / 120 篇 SLR + 完整字段表足以直接进入主统计池作为 *secondary study 元统计* 的可信样本。建议把统计池资格改为"是（限于 secondary study 元统计场景）"，并在 A.3 新增 `clm-...-pool-eligible` 结论。

#### Important（I）— 影响证据等级与可复用性

**I1** ── §"原文模式候选叶子映射（A1 种子）" 表只列 4 个候选叶子（secondary-study-profile / quality-assessment / topic-taxonomy / practice-impact），缺少：(a) Cited EBSE / Cited Guidelines 的带子引用枚举；(b) Number of Primary Studies 的数值字段；(c) Review Type / Review Scope 的封闭三分；(d) Source Type 的 J/C/WS/BS 四分；(e) 关系边（researcher/org/country）；(f) predecessor_relation 字段。应至少补齐到 §4 的 22 个 leaf + §5 的 11 条 edge。

**I2** ── 证据账本 A.2 仅有 4 条 (EV-001..004)，全部 `not_verified` 且页码空缺。应至少为 Table 2/3/5/6/13 各建一条已锚定证据（页码、表号、行号都明确），不再笼统写"摘要 / 引言页；待 A2a 精确页码复核"。基于本次通读，建议新增：
- EV-005 §3.6 QA rubric → L392–433 `paper_content.txt`
- EV-006 §3.7 10-field extraction form → L451–468
- EV-007 Table 2 (67×10 cells) → L575–771
- EV-008 Table 3 (67×6 cells) → L826–894
- EV-009 §7 update type triplet → L1343–1363

**I3** ── §"维度树复原" 的一句话结论说"维度树主类型为'tertiary 更新统计树'"语义不清。建议改为"**维度森林**：抽取表 schema 树 + QA rubric 树 + 双重外部主题分类 + 关系图 + predecessor 关系 + edu/practice 相关性"，并明确这是 6 棵子树并存。

#### Minor（M）— 工程性 / 可读性

**M1** ── `review.md` §2 表头是"六类 pattern 抽取"，但与 §"维度树复原" 重复且口径不一。建议合并：把"六类 pattern"作为跨论文外推视角的浓缩版，并在每行加一句"对应原文 schema 哪部分"。

**M2** ── A.4 cmd-...-visual-check 状态为 `needs_manual_check`。基于本次通读，Fig.1 (DCP)、Fig.2 (1389→67 流程) 与 Table 6 (双列 SLRs/Subs) 是 OCR 易错处，应明确列为 PDF 核验对象。

**M3** ── 时间窗口在不同位置写法不一（"2008-07–2009-12" / "2008.7-2009.12" / "July 2008–December 2009"），统一为 ISO `2008-07-01 ↔ 2009-12-31`。

#### 对 `SUMMARY.md` 的同步修正建议

1. "样本单位" 字段应从模糊的 "secondary study" 收紧为 **"secondary studies (SLR/MS/MA) in SE, with mapped author/org/country/topic relations; N_new=67 / N_total=120"**
2. "原生树类型" 字段应从单值改为 **"维度森林(6 子树)"**
3. "统计池资格" 字段应从 "schema_seed" 改为 **"局部可统计：可作为 secondary-study 元统计（即对 SLR 元数据做计量）的主统计池样本，但不作为目标领域 (e.g. STM/LLM4SE) 的统计池"**

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-ds11-005 | paper_content.txt | §3.6 QA rubric | L392–433 | QA1–QA4 完整定义 + Y=1 / P=0.5 / N=0 评分（QA2 已对 Kitchenham 2010 做歧义修正） | rubric | high | T2 全部叶子 (qa1–4, qscore, quartile) | 否 | 评分细则可复用，但 4 题集来自 DARE 2007 版；DARE 后已升级至 5 题 |
| EV-ds11-006 | paper_content.txt | §3.7 Data extraction | L451–468 | 显式列出 10 字段：Year / Quality Score / Review Type / Review Scope / Topic Area / Cited EBSE / Cited Guidelines / # Primary Studies / Practitioner Guidelines / Source Type | extraction_form | high | T1 全部叶子 | 否 | schema 结构可迁移；具体引用文献列表已陈旧 |
| EV-ds11-007 | paper_content.txt | Table 2 | L575–771 (67 行 × 10 字段) | 67 篇 SLR 完整字段实例化 | data_instance | high | T1 全部叶子取值空间饱和性 | 是（Table 行错位风险） | 数据点定型 schema；具体内容不外推 |
| EV-ds11-008 | paper_content.txt | Table 3 | L826–894 (67 行 × 6 列) | 67 篇 QA 分布；quartile 划分 | data_instance | high | T2 + Final + Quartile 实例化 | 是 | 同上 |
| EV-ds11-009 | paper_content.txt | Table 5 + Table 6 | L904–1136; L1162–1196 | SLR ↔ SE2004 Curriculum ↔ SWEBOK 完整映射；"SW Config Mgt / SW Quality 在 120 SLR 中=0" | relation + gap_finding | medium | E2, E3, T3 | 是（双列易错） | 外部分类法版本受限 |
| EV-ds11-010 | paper_content.txt | §7 Conclusions | L1343–1363 | "three complementary ways to update a SLR: temporal update / search extension / combined; 120 篇中无内部 update" | classification + finding | high | T5 update_type 三值枚举；E9 关系 | 否 | 三分法可迁移；finding 是 single-paper observation |
| EV-ds11-011 | paper_content.txt | §6 Limitations | L1226–1259 | QA2 评分需向原作者咨询；QA4 评分主观；很多 SLR protocol 描述不充分 | validity | medium | T2 整体可信度；E11 venue 报告质量 | 否 | rubric 主观性是共性，可外推 |
| EV-ds11-012 | paper_content.txt | Table 4 + §5.5 + Table 13 | L894–900; Table 13 | Quality Mean 2004=2.08 → 2009=2.61 (+12.5%)；EBSE-positioned 比例从 17% → 80% | statistical_result | high | trend findings | 否 | 数值不外推；趋势模式可迁移 |
| EV-ds11-013 | paper_content.txt | Table 2 注脚 a–h | L763–770 | a=[14], b=[8], c=[24] 是 EBSE 文献；d=[15], e=[13], f=[16], g=[4], h=[12] 是 SLR guidelines | enumeration | high | T1.ebse_cite 与 T1.guide_cite 的子引用枚举 | 否 | 引用集陈旧；模式可迁移 |
| EV-ds11-014 | paper_content.txt + Appendix A | App.A | L1472–1624 | SE01..SE77 全部 67 篇被编码 SLR 的书目数据 | sample_manifest | high | 样本池版本锚 | 否 | 列表是 frozen sample |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| clm-ds11-N01 | 本文样本单位是已发表的 SLR/MS/MA，N_new=67 / N_total=120 | sample_unit_definition | T1, T6 森林根 | EV-005, EV-006, EV-007, EV-014 | strong | 直接用于 review.md §0/§1 | 不外推到非 SE 二级研究 |
| clm-ds11-N02 | 本文具备 10 字段 extraction form + 4 题 QA rubric，构成完整 schema | schema_finalised | T1, T2 | EV-005, EV-006, EV-007, EV-008 | strong | 用于把"维度树主树"从 6 叶通用接口升级为原文 schema | rubric 是 DARE 2007 版，已升级 |
| clm-ds11-N03 | 本文的"原生树"是维度森林(6 棵)，不是单树 | tree_topology | T1..T6 | EV-005..EV-010 | strong | 用于校正 review.md "原生树类型" 字段 | — |
| clm-ds11-N04 | 本文具备主统计池资格（限于 secondary-study 元统计场景） | pool_eligibility | T1, T2, App.A | EV-007, EV-008, EV-014 | medium-strong | 改写 review.md §"统计与候选发现链路" 的池资格 | 不作为目标领域 (LLM4SE/STM) 的统计池 |
| clm-ds11-N05 | "SW Configuration Management 与 SW Quality 在 120 篇中=0 SLR" 是可统计 gap finding | gap_finding | T3 (Curriculum + SWEBOK) | EV-009 | strong (限 2004–2009 窗口) | 可作 candidate finding；不外推到 2024 | 时间窗口约束；SWEBOK 已升级 |
| clm-ds11-N06 | "MS 比例 32%→82%" 受测量法迁移 (Da Silva 2010 重分类) 干扰 | measurement_drift_warning | T1.rtype | L791–800 paper_content.txt | strong | 给跨论文统计加 caveat | 必须保留 |
| clm-ds11-N07 | 三种 update 类型 (temporal/search/combined) 可作 update-review 通用分类 | methodological_seed | T5 | EV-010 | strong | 直接迁移到 Paper2 的 predecessor schema | — |
| clm-ds11-N08 | 本文具有显式关系型 schema (SLR↔Curriculum/SWEBOK/researcher/org/country)，远比一般 SLR 丰富 | relation_richness | T3, T4 / E1–E11 | EV-007, EV-009 | strong | 可作 review.md §"关系边" 章节模板 | — |
| clm-ds11-N09 | DCP (Decision and Consensus Procedure) 是可迁移的多人编码流程 | methodological_seed | 全文 §3.3 | L257–280 | strong | Paper2 编码方法学借用 | — |
| clm-ds11-N10 | QA2 评分歧义需向原作者咨询，QA4 评分主观——rubric 本身有主观偏差 | validity_threat | T2 | EV-011 | medium | 提醒未来 schema 验证 | — |

### 9. 技能使用与自我审查记录

#### 采用的技能纪律（基于主 prompt 注入摘要 + 仓库 CLAUDE.md 内化规范）

- `ai-research-writing-skill` / `reviewer-guidelines`：reviewer 应基于证据分级（C/I/M），单论文 review 不外推；正式 finding 须有可追溯锚点。本报告所有结论均锚定 `paper_content.txt` 行号或表号。
- `ai-research-writing-skill` / `reviewer-self-review`：reviewer 输出后须自检"是否会被审稿人质疑证据强度"。本报告对每条 finding 标 strong/medium/weak。
- `research-planning` / `planning-prompts` + `output-schemas`：schema 字段需有取值空间、缺失值语义、统计用途。本报告 §4 叶子维度表严格 12 列。
- `oh-my-codex:autoresearch`：研究输出须把"已统计 vs. 候选 vs. 不可迁移"三层显式分开（§6 已分 A/B/C/D 四类）。
- 仓库 §A1-DT v2 协议：单论文 review 不能套用 A1-M0–M6 投影；不能把通用 6 叶接口当原文叶子全集（本报告对 review.md C1/C2 返修建议即基于此）。

#### Reviewer 视角：本输出的 3 个最高风险

1. **未做 PDF 版面级核验**：Table 2/3/5/6 在 `paper_content.txt` 中存在跨页换行、列错位风险（尤其 Table 6 的 SLRs/Subs 双列）。主线程合并前应至少抽样核对 5 行 Table 2 和 Table 3 的取值是否与 PDF 一致。
2. **"统计池资格升级"建议可能与 PR 整体 19 篇审计的 staging 策略冲突**：当前 PR 把所有 19 篇都暂保持 `schema_seed`，可能是 staging 一致性考虑而非单篇错判。主线程合并时应回看 PR body 是否明确允许逐篇升级，否则保留 schema_seed 但在 SUMMARY 增加"可统计候选"标签。
3. **关系边表 E9 (update_type) 的 `none` 取值是 finding 而非字段空缺**：原文说"120 篇中无内部 update"是 gap finding，但严格说也可解读为字段缺失。主线程合并时应明确这是 finding 还是 schema 空值，避免下游误读。

#### blocked / timeout / 文件缺失记录

- 未启动 subagent；本任务由当前 claude 直接完成。
- 未访问 `paper.pdf`（按指令"必要时核对"判断本轮文本足以支持 schema-level 审计；表格 / 图的版面核验列为 A2a 任务，已在 §7 M2 记录）。
- 未访问外部 skill 文件（CLAUDE 工作目录下 `~/.codex/skills/` 路径属于 codex 体系，本 claude 实例无文件读权限路径；按指令 §0.6 要求记录为 `blocked: 外部 skill 文件未直接读取，使用 prompt 中已注入的纪律摘要替代`）。
- 全部 1625 行 `paper_content.txt` 已按页顺序通读（Page 1–15 全覆盖），未跳页、未仅 grep 关键词。

---

报告结束。所有必填章节 §0–§9 均自包含给出，无对"上一条消息"或外部上下文的引用。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md](../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-da-silva-2011-six-years-slr-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-da-silva-2011-six-years-slr-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-da-silva-2011-six-years-slr-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-da-silva-2011-six-years-slr-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-da-silva-2011-six-years-slr-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-da-silva-2011-six-years-slr-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/da-silva-2011-six-years-slr__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-da-silva-2011-six-years-slr-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/da-silva-2011-six-years-slr.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-da-silva-2011-six-years-slr-type | clm-da-silva-2011-six-years-slr-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：SLR 的子型——**updated tertiary study**（temporal update + integration of two prior tertiary studies）；同时具备 mapping study 性质（本文自称"performed a mapping study of SLRs"） | paper_type | text_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-da-silva-2011-six-years-slr-unit | clm-da-silva-2011-six-years-slr-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：**已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 | sample_unit | text_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-da-silva-2011-six-years-slr-denom | clm-da-silva-2011-six-years-slr-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：SE=67；OS=20；FE=33；OS/FE=53；OS/FE+SE=120；QA assessment N=67（SE 自身）/ 120（整合） | denominator | text_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-da-silva-2011-six-years-slr-tree | clm-da-silva-2011-six-years-slr-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林**：(1) 抽取表 schema 树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (predecessor relation: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→finding 路径 | schema | text_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-da-silva-2011-six-years-slr-pool | clm-da-silva-2011-six-years-slr-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：**是**——具备完整系统检索（自动+人工+回溯）、显式纳排、quality assessment、可分母统计字段；当前 `review.md` 把它标 `schema_seed` 是低估 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 final finding |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-da-silva-2011-six-years-slr-type | A1DT-da-silva-2011-six-years-slr-C01 | 本文原文类型为：SLR 的子型——**updated tertiary study**（temporal update + integration of two prior tertiary studies）；同时具备 mapping study 性质（本文自称"performed a mapping study of SLRs"） | paper_type | type | ev-da-silva-2011-six-years-slr-type | 正式写作前需核对出版页和 PDF 版式 | text_verified | schema_seed / 背景方法样本描述 | 否 | -- |
| clm-da-silva-2011-six-years-slr-unit | A1DT-da-silva-2011-six-years-slr-C02 | 本文被编码样本单位为：**已发表的二级研究 (SLR / MS / MA)**——本研究 (SE) 新增 67 篇；整合前序 OS + FE 后总样本 N=120 | sample_unit | sample_unit | ev-da-silva-2011-six-years-slr-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | text_verified | schema_seed / A2a 抽取表设计 | 否 | -- |
| clm-da-silva-2011-six-years-slr-tree | A1DT-da-silva-2011-six-years-slr-C03 | 本文原生维度树 / 维度森林为：**维度森林**：(1) 抽取表 schema 树（10 字段），(2) QA rubric 树（4 题 + 评分 + quartile），(3) 主题分类树（24 SE topics × SE2004 Curriculum × SWEBOK），(4) 作者/机构/国家关系图，(5) 前序关系树 (predecessor relation: OS → FE → SE / temporal update / search extension)，外加 (6) limitation→finding 路径 | tree_type | native_tree | ev-da-silva-2011-six-years-slr-tree | 不代表跨论文通用模板 | text_verified | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-da-silva-2011-six-years-slr-pool | A1DT-da-silva-2011-six-years-slr-C04 | 本文统计池资格为：**是**——具备完整系统检索（自动+人工+回溯）、显式纳排、quality assessment、可分母统计字段；当前 `review.md` 把它标 `schema_seed` 是低估 | eligibility | statistical_pool | ev-da-silva-2011-six-years-slr-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-da-silva-2011-six-years-slr-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-da-silva-2011-six-years-slr-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-da-silva-2011-six-years-slr-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
