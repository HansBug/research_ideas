I have read sufficient content (covered §1 Intro through §7 Conclusion, including all 23 tables and 4 figures referenced; lines 1-2000+ of paper_content.txt cover all substantive sections, remaining lines are references). Now producing the complete audit report.

`★ Insight ─────────────────────────────────────`
- 与 review.md 现有"维度树"对比，原文真实的 schema 主结构应是"F1-F18 抽取表 + 3 套分类 schema + 9-type 分析 taxonomy + 14-activity SE schema + 4-type technique taxonomy"，而六叶通用接口（scope/corpus/taxonomy/method/evidence/finding）只是 reviewer 投影。
- 原文已经把 RQ1-RQ5 显式映射到 F6-F18，构成"RQ→字段→分类 schema→统计表→discussion"完整闭环，可作为强一致性 schema 证据。
- 取值空间多为封闭枚举（如 9 类 analysis、4 类 technique、14 类 SE activity）且有 reliability 报告（Table 4），属于 A1 高等级 schema 样本。
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇全文审计报告：app-reviews-slr-se

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `app-reviews-slr-se` |
| agent | `claude`（claude-opus-4-7[1m]，本地直接执行，非 subagent） |
| 是否已读 `paper_content.txt` | 是；按行号顺序覆盖 §1 Introduction 至 §7 Conclusion 及 References 起始部分（行 1–2200+），所有 Table 1–23、Figure 1–4、§3.2.1–3.6.2、§4.1–4.10、§5–§7 已逐节阅读。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；元信息一致：Dąbrowski/Letier/Perini/Susi (2022), ESE 27(2):43, DOI 10.1007/s10664-021-10065-7。 |
| 是否打开或核对 `paper.pdf` | 否（本轮以全文文本审计为主，复杂表格视觉级版面核对仍标为待 A2a 人工核验）。 |
| 原文类型 | SLR（明确遵循 Kitchenham 2004，PRISMA 流程） |
| 被编码样本单位 | primary study（共 182 篇 peer-reviewed 论文，2012–2020 发表） |
| 样本数量 / 分母 | 182 primary studies（初始 1656→去重 303→筛选 1353→排除 1225→128 通过+ 14 manual + 40 snowballing = 182） |
| 原生树类型 | RQ-驱动的多 schema 抽取森林（F1–F18 数据抽取表 + 3 套分类 schema + RQ 结果层），不是单一统一树 |
| 主统计池资格 | 是；该论文具有完整 SLR 流程、显式封闭枚举字段、reliability 报告、五数概括与交叉表，可作为 A1 schema 模式统计池的高等级样本 |
| 总体判定 | needs repair（review.md §维度树复原内核与原文 schema 偏离；C 级返修在第 7 节列出） |

## 1. 原文证据阅读说明

实际读取的文件与章节：

1. `bibtex.bib`（1–19 行）— 标题、作者、ESE 卷期、DOI、关键词；
2. `metadata.json`（1–28 行）— slug、DOI、CCF 等级、review_type=SLR；
3. `paper_content.txt`：
   - §1 Introduction（行 36–98）— 研究动机、四项 paper objectives、4 项 primary contributions；
   - §2 Research Method（行 98–341）— RQ1–RQ5 定义、PRISMA 流程、检索式构造、F1–F18 抽取表、3 套 classification schema 构造方式、reliability 检验、data synthesis；
   - §3.1 Demographics（行 342–360）；
   - §3.2 RQ1 + Table 7（9 类 analysis）+ 3.2.1–3.2.9 各子小节（行 361–636）；
   - §3.3 RQ2 + Table 9–12（4 大 mining technique + 10 ML 技术）（行 639–871）；
   - §3.4 RQ3 + Table 13–15（14 项 SE activity）（行 885–1230）；
   - §3.5 RQ4 + Table 16–20（公开数据集、工具、五数概括、user-study criteria/participants）（行 1245–1490）；
   - §3.6 RQ5 + Table 21–22（effectiveness range/median、user study 定性合成）（行 1490–1700）；
   - §4 Discussion §4.1–4.10（行 1693–1850）；
   - §5 Threats（行 1849–1885）；
   - §6 Related Work + Table 23（行 1885–1938）；
   - §7 Conclusion（行 1939–1972）。

未做：PDF 视觉级版面核验（搜索式 query 文本、Fig 1 PRISMA 详细数字气泡、Tables 14/15 矩阵对齐、Table 16 部分单元格 OCR）。

**关键证据锚点（短引/释义）**：

1. §1 paper objectives（行 79–86）："identify and classify the range of app review analysis…; identify the range of NLP and data mining techniques…; identify the range of software engineering activities…; report the methods and results of the empirical evaluation"。
2. §2.1 RQ1–RQ5（行 108–115）：5 个 RQ 分别对应分析类型 / 技术 / SE 活动 / 评价方法 / 评价结果。
3. §2.2 PRISMA 数量链（行 130–171）：1,656→303 dup→1,353 screened→1,225 excluded→128→+14 manual→+40 snowballing→**182** included。
4. §2.3 Table 3 F1–F18 数据抽取表（行 226–270）：F1 Title…F18 Replication Package；F6 → RQ1，F7 → RQ2，F8/F9 → RQ3，F10–F12/F14–F18 → RQ4，F13 → RQ5。
5. §2.4 三套 classification schema 构造（行 289–341）+ Table 4 reliability（intra/inter rater = 93%/87%、100%/87%、90%/80%）。
6. §3.2 Table 7（行 440）：9 类 analysis 频次（Classification 105/58%、Information Extraction 56/31%、Content Analysis 54/30%、Clustering 44/24%、Sentiment 40/22%、Recommendation 30/16%、Summarization 25/14%、Search & IR 24/13%、Visualization 20/11%）。
7. §3.3 Table 9（行 660）：4 大 mining technique（NLP 113/62%、ML 108/59%、SA 53/29%、MA 45/25%）；Table 12 10 项 ML 子类。
8. §3.4 Table 13（行 945+）：14 项 SE activity 跨 4 个 phase（Requirements 66/36%、Design 8/4%、Testing 28/15%、Maintenance 66/36%、Not specified 62/34%）。
9. §3.5 Table 18（行 1383–1389）：annotated dataset 五数概括（No. Apps min/Q1/Med/Q3/Max = 1/7/19/185/1,430,091；No. Reviews 80/1,000/2,800/4,400/41,793）。
10. §3.6.1 行 1491–1494："methodology…too diverse to undertake a meta-analysis…we thus employed 'summarizing effect estimates'"。
11. §4.1–4.10 十项 discussion gap（growing area / SE goals / reference model / dataset size / replication packages / practice impact / practitioners' needs / industrial needs / efficiency & scalability / ML training problem）。
12. §5 Threats 四类（incompleteness / publication bias / subjectivity / taxonomy reliability）。

## 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象**：peer-reviewed primary study（论文级单位）。F1–F18 中 F1（Title）、F2（Author）、F3（Year）、F4（Venue）、F5（Citation）明确是 per-paper 书目元数据，其余 F6–F18 都是对单篇 primary study 的内容编码。
2. **是否有系统检索/纳排/抽取/编码**：是。明确遵循 Kitchenham 2004 + PRISMA 报告，构造 generic + specific 两套查询、覆盖 6 大数据库、补 manual + snowballing；纳排标准明确（Table 1）；Table 3 F1–F18 抽取表；Table 4 三套 schema 的 intra/inter rater agreement。
3. **字段来自哪里**：
   - **F1–F18 抽取表**（Table 3）→ 显式 data extraction form；
   - **App review analysis taxonomy**（9 类，Table 7）→ classification schema，构造来源：Martin 2017 的 5 类 + Cannataro & Comito 2003 的 mining tasks 7 类 + Miner 2012 text analytics 7 类，合并后再增加 Recommendation；
   - **Mining technique taxonomy**（4 类，Table 9）→ Tavakoli 2018 的 4 类 + Miner 2012 statistical analysis 1 类，删除 feature extraction，剩 4 类；
   - **SE activity taxonomy**（14 类，Table 13）→ SWEBOK (Bourque 1999) 258 terms → 58 candidate → 14 final；
   - **Evaluation & artifact 字段**（F10–F18）→ 自创字段，含 dataset/tool/annotator/quality measure/replication package；
   - **统计与交叉表**（Tables 5/7/9/10/11/13/14/15/16–22）由抽取表数据合成。
4. **RQ 与样本单位关系**：RQ 是结果组织维度，把 F6–F18 字段聚合后回答；样本单位仍是 primary study，不因 RQ 而变。RQ 不是树根而是字段"用途映射"。
5. **降级**：不适用。本文是系统 SLR，不属于 roadmap/vision；无需降级。

## 3. 原生样本编码维度树 / 维度森林

样本单位 = primary study（n=182）。原文模式是**字段森林**而非单棵树：1 棵抽取字段树（F1–F18） + 3 套 classification schema 树 + 1 棵 SE activity 树 + 评价/复现资产子集 + discussion-driven gap 列表（不进 schema）。

```text
[ROOT] primary study (n=182, 2012-2020)
├── [A] Bibliographic metadata (F1-F5)  ← RQ-independent documentation
│   ├── F1 Title (free text)
│   ├── F2 Author(s) (list)
│   ├── F3 Year (2012-2020, enumerable)
│   ├── F4 Venue (open enum from Table 5 + supplementary list)
│   └── F5 Citation count (numeric, Google Scholar @ 2021-08-04)
│
├── [B] Review Analysis F6 → RQ1  ← classification schema #1 (9 closed types)
│   ├── F6.1 Analysis type ∈ {Classification, InformationExtraction, ContentAnalysis,
│   │                          Clustering, SentimentAnalysis, Recommendation,
│   │                          Summarization, SearchAndIR, Visualization}
│   ├── F6.2 Mined information (open enum: bug, feature, NFR, opinion, user-request, topic, …)
│   └── F6.3 Supplementary description (free text)
│
├── [C] Mining Technique F7 → RQ2  ← classification schema #2 (4 closed types + sub-techniques)
│   ├── F7.1 Technique type ∈ {ManualAnalysis, NLP, MachineLearning, StatisticalAnalysis}
│   └── F7.2 Technique name (e.g., NaïveBayes, SVM, LDA, K-Means, …; Table 12 lists top 10)
│
├── [D] SE Activity F8 + F9 → RQ3  ← classification schema #3 (14 closed activities, 4 phases)
│   ├── F8 SE activity ∈ {
│   │     REQUIREMENTS: Elicitation, Classification, Prioritization, Specification;
│   │     DESIGN: DesignRationaleCapture, UIDesign;
│   │     TESTING: ValidationByUsers, TestDocumentation, TestDesign, TestPrioritization;
│   │     MAINTENANCE: Problem&ModificationAnalysis, RequestedModificationPrioritization,
│   │                   HelpDesk, ImpactAnalysis;
│   │     NotSpecified
│   │  }   (multi-valued: a paper can claim ≥1 activity)
│   └── F9 Justification (free text; sometimes absent)
│
├── [E] Empirical Evaluation block → RQ4
│   ├── F10 Evaluation Objective
│   │     ├── F10.1 ∈ {effectiveness, user-perceived quality}
│   │     └── F10.2 evaluated analysis type (links to F6.1)
│   ├── F11 Evaluation Procedure (free text + procedural pattern)
│   ├── F12 Metrics & Criteria (open enum: Precision, Recall, F1, Accuracy, MojoFM,
│   │                            BLEU-4, Usefulness, Usability, Efficiency, Informativeness, …)
│   ├── F14 Annotated Dataset
│   │     ├── F14.1 App Store (Google Play / Apple / Amazon / BlackBerry / Huawei /
│   │     │                     Windows Phone / 360 Mobile)
│   │     └── F14.2 #annotated reviews (numeric)
│   ├── F15 Annotation Task (free text bound to F6.1)
│   ├── F16 #Annotators (numeric, range 1-5, median 2)
│   ├── F17 Quality Measure ∈ {CohensKappa, PercentageAgreement, JaccardIndex,
│   │                            FleissKappa, none-reported}
│   └── F18 Replication Package
│         ├── available? (boolean)
│         └── content (dataset / tool / scripts; Tables 16-17 list 23 datasets + 16 tools)
│
└── [F] Evaluation Result F13 → RQ5  (range + median per analysis × mined-info-type;
                                       see Table 21 effectiveness, Table 22 user-study)
```

**non-schema 派生层**（不是字段，是综述自己的合成产物，归为 candidate finding 池，不进单篇编码 schema 树）：

- Table 23 与 4 篇相关综述的 dimension-by-dimension 对比（study type / period / #papers / RQ 覆盖）；
- §4.1–4.10 十项 gap / future direction；
- §5 四类 threats 与 mitigation。

## 4. 叶子维度表

下表只列原文 schema 主树（[A]–[F]）的核心叶子；F6.2/F12 等开放枚举叶子的封闭性需 A2a supplementary 核对。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 标题 | A | Table 3 F1 | 论文题目 | 自由文本 | 自由文本 | 不会缺失 | bibliographic 索引 | — | Table 3 | 通用 |
| F3 | 年份 | A | Table 3 F3 | 发表年份 | 2012–2020 | 数值/年度 | 不缺失 | 年度趋势（Fig 2） | growing area finding §4.1 | Fig 2 | 通用 |
| F4 | 发表 venue | A | Table 3 F4, Table 5 | 会议/期刊 | 开放枚举（Top10 见 Table 5） | 开放枚举 | 不缺失 | venue 分布（Fig 3）+ Top10 | 高质量 venue 占比支撑"研究成熟度" | Fig 3, Table 5 | 通用 |
| F5 | Google Scholar 引用数 | A | Table 3 F5 | 2021-08-04 引用计数 | 整数 | 数值 | 0 | Top20 most-cited（Table 6） | 影响力 finding | Table 6 | 时点依赖；需说明 snapshot 日期 |
| F6.1 | 分析类型 | B | Table 7 + §3.2 | 9 类 app review analysis | {Classification, InformationExtraction, ContentAnalysis, Clustering, SentimentAnalysis, Recommendation, Summarization, SearchAndIR, Visualization} | **完整枚举**（已封闭，构造源自 Martin 2017 + Cannataro 2003 + Miner 2012 合并） | 应为强制非空 | per-type 频次（Table 7）；与 F7.1/F8 交叉（Tables 10/11/14/15） | "Classification 主导" §3.2.2、领域空白 | Table 7 行 440 | 领域 taxonomy 不迁移到 LLM4STM；结构和构造方法可迁移 |
| F6.2 | 挖掘信息类型 | B | Table 3 F6.2 + §3.2 各子节 | 例如 bug、feature、NFR、user-request、opinion、topic、user-story | 开放枚举（未在 Table 列封闭） | 层级枚举（按 F6.1 子领域分组） | 报告中未提及具体即缺失 | Table 21 按 mined-info 分组的 effectiveness range/median | feature extraction 效果最差 §3.6.1 | Table 21 行 1501–1539 | 取值集合需 A2a 与 supplementary 对照确认 |
| F7.1 | 挖掘技术大类 | C | Table 9 + §3.3 | 4 类 | {NLP, ML, SA, MA} | **完整枚举** | 多技术允许多值；缺失=未报告 | Table 10 4×9 交叉；Table 11 组合 | NLP+ML 主导 Classification §3.3 | Table 9–11 | 通用 |
| F7.2 | 具体技术名 | C | Table 12 + §3.3.2–3.3.4 | 例如 NaïveBayes、SVM、LDA | 开放枚举（Table 12 列 10 项 ML） | 层级枚举 | 未报告 | ML 子类频次 | NB/SVM/LDA 主导监督/非监督；7% NeuralNetwork 偏低 | Table 12 行 830 | 取值空间随时间演进 |
| F8 | SE 活动 | D | Table 13 + §3.4 | 14 项跨 4 phase | {REQ-Elicit/Classif/Prior/Spec, DES-Rationale/UI, TST-Valid/Doc/Design/Prior, MNT-Problem/RequestPrior/HelpDesk/Impact, NotSpec} | **完整枚举**（来源 SWEBOK 258→58→14） | NotSpecified=34% 显式编码 | per-activity 频次 + Table 14/15 与 F6.1 交叉 | §4.2 SE goals 不清；§4.7 practitioner's needs | Table 13 行 945 | 结构通用；具体活动取值与领域强相关，但来源 SWEBOK，所以可作通用 SE 元模型 |
| F9 | 理由说明 | D | Table 3 F9 | 论文如何解释 review analysis 支持 SE 活动 | 自由文本 + 理由是否给出（boolean） | 自由文本加理由 | "Some papers do not provide any justification" §2.3 | 给出 vs 未给出 比例 | §4.2 "vague about details" | Table 3 行 207–209 | 通用 |
| F10.1 | 评价目标类型 | E | Table 3 F10.1 + §3.5 | 评价种类 | {quantitative-effectiveness, user-perceived-quality} | 完整枚举（2 类） | 未评价=不在 109 篇内 | 109/105/23 篇分母 §3.5 | §4.6 practice impact 不明 | 行 1249–1251 | 通用 |
| F11 | 评价流程 | E | Table 3 F11 | 评价步骤 | 自由文本 + 4 步标准过程（formulate→annotate→apply→quantify） | 层级模板 + 自由文本 | 未描述时降级 | 4 步覆盖率 | replication 不足 §4.5 | §3.5.1 行 1252–1262 | 通用 |
| F12 | 指标与准则 | E | Table 3 F12 + §3.5/3.6 | 效果与定性准则 | 开放枚举：{Precision, Recall, F1, Accuracy, MojoFM, BLEU-4, Usefulness, Accuracy, Usability, Efficiency, Informativeness} | 开放枚举（分定量/定性两组） | 未报告时为 NA | Table 19 user-study criteria × analysis；Table 21 定量分布 | RQ5 综合 | Tables 19, 21, 22 | 指标语义通用 |
| F13 | 评价结果 | F | Table 3 F13 + Tables 21–22 | 数值结果或定性表述 | 数值（precision/recall/F1）+ 自由文本（user-study quote） | 数值或区间 + 自由文本 | 未做评价=不入 87 篇 | Table 21 range/median；Table 22 qualitative synthesis | §3.6.1 效果差异；§3.6.2 时间节省 50–75% | 行 1486–1689 | 通用 |
| F14.1 | 数据集来源 App Store | E | Table 3 F14.1 + §3.5.1 Char-of-Dataset | App store 名称 | {GooglePlay, AppleStore, Amazon Appstore, BlackBerry, Huawei, Windows Phone, 360 Mobile} | 完整枚举（7 store） | 单 store=84% Google+Apple | store 分布；多 store 多样性 | dataset 偏 Google/Apple §3.5.1 | 行 1329–1333 | 通用结构；具体 store 取值随生态演变 |
| F14.2 | 标注 review 数 | E | Table 3 F14.2 + Table 18 | 数据集大小 | 整数（80–41,793） | 数值（五数概括） | 未公开则不计 | Table 18 五数 | §4.4 dataset size 过小 | Table 18 行 1383 | 通用 |
| F16 | 标注者数量 | E | Table 3 F16 + §3.5.1 | annotator 人数 | 整数 1–5（median 2） | 数值 | 未报告 | 分布/median | 多数 2 人 | 行 1271–1273 | 通用 |
| F17 | 质量度量 | E | Table 3 F17 + §3.5.1 | reliability metric | {CohensKappa, PercentageAgreement, JaccardIndex, FleissKappa, none-reported} | 完整枚举（4 + none） | 只 25% 报告 §3.5.1 | reliability 完整度 | §3.5.1 透明度 finding | 行 1273–1280 | 通用 |
| F18.available | replication package 可用性 | E | Table 3 F18 + Tables 16–17 + §4.5 | 是否公开 | {available, not-available} | 布尔 + 联系作者确认 | 多数 unavailable | 23 datasets + 16 tools 占 ~21% | §4.5 replicability gap | Tables 16, 17 | 通用 |

## 5. 关系边表

原文存在多条显式关系（cross-tabulation 表 + traceability 数据 + RQ→F 字段映射）：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| REL-1 | F6.1 (analysis type) | × 交叉统计 | F7.1 (technique) | 9 × 4 频次矩阵 | 单元格 0=未观察 | Table 10 行 705 | 哪种技术常用于哪种分析（NLP+ML 主导 Classification） |
| REL-2 | F6.1 + F6.1 组合 | × 组合统计 | F7.1 组合 | 9 × 12 组合矩阵 | 未观察 | Table 11 行 722 | 一个 study 可用多种技术组合实现一种分析 |
| REL-3 | F6.1 | × 交叉 | F8 (SE activity) | 9 × 14 矩阵 | NotSpecified 为显式 cell | Table 14 行 1019 | RQ3 主要桥梁 |
| REL-4 | F6.1 组合 | × 交叉 | F8 | 53 unique 组合 | — | Table 15 行 1025 | analysis 组合如何支持 SE 活动 |
| REL-5 | F12 user-study criterion | × | F6.1 | {Accuracy/Efficiency/Informativeness/Usability/Usefulness} × 9 类 | 未评价=空 | Table 19 行 1424 | RQ5 user-study 维度 |
| REL-6 | F13 result | + per F6.1 + F6.2 | range/median | 数值区间 | 未评价=空 | Table 21 行 1501 | 不同 mined-info 类型效果对比 |
| REL-7 | F8 (review) | trace-link | external artifact | {AppDescription, GitCommit, GoalModel, IssueReport, LintWarning, SourceCode, StackTrace, Tweet} | 该 study 是否做 trace | Table 8 行 521 | Search & IR 的关系字段（review × 外部 artifact） |
| REL-8 | F4 venue | 横向对比 | 4 篇 prior survey 维度 | dimension × survey 矩阵 | check 标 | Table 23 行 1923 | 与相关综述维度比较 |
| REL-9 | RQ_i | derived_from | {F6, F7, F8/F9, F10–F12/F14–F18, F13} | RQ→F 字段集合 | — | Table 3 行 226 | RQ 与抽取字段的显式 use 映射 |

## 6. 统计观察、候选 finding 与 final finding 边界

**A. 原文由字段/统计表直接支持的统计观察**（已可信赖入分母）：

1. 9 类 analysis 频次：Classification 58%、IE 31%、CA 30%、CU 24%（Table 7）。
2. 4 大 technique 频次：NLP 62%、ML 59%、SA 29%、MA 25%（Table 9）。
3. NLP+ML 占 29%，是最常见组合（Table 11）。
4. 14 项 SE activity：Requirements 36%、Maintenance 36%、Testing 15%、Design 4%、NotSpecified 34%（Table 13）。
5. 评价：109/182 做了 empirical eval；105 effectiveness；23 user study；87 报告了 RQ5 可用结果。
6. 标注数据集中位数 2,800 reviews，max 41,793，远小于真实 review 流量。
7. 仅 25% 报告 inter-rater quality measure。
8. 公开 dataset 23 个；公开 tool 16 个；其余多数未公开。
9. Table 21 各 analysis × mined-info 的 precision/recall range 与 median。
10. Top10 venues 均为主流 SE 会议/期刊（RE, EMSE, REFSQ, ICSE, IEEE SW, FSE, ASE, …）。

**B. discussion / recommendation / roadmap 提出的候选 finding**（§4.1–4.10）：

1. growing area（papers quadrupled by 2020）；
2. SE goals / use cases 描述模糊；
3. 缺少 review-mining tool 的 reference model；
4. evaluation dataset 过小且与真实流量不匹配；
5. replication package 严重不足；
6. practice impact 评价不足，需"SE-concern metrics"补充传统 ML metric；
7. practitioner 视角缺失；
8. industrial need 未被验证（average app 22 reviews/day vs 大厂上千）；
9. efficiency & scalability 未被系统评估；
10. ML training 受 domain/time drift 影响，semi-supervised / active learning 是方向。

**C. 对 Paper2 可迁移的方法学启发**：

- "RQ → 抽取字段 → classification schema（构造源 + 合并规则 + reliability check）→ 频次/交叉/range 表 → discussion gap"的完整闭环结构；
- 同一字段允许多值（multi-claim activity / multi-technique），并显式记录"NotSpecified" 作为编码单元而不是丢失；
- 异质 evidence 用 summarizing-effect-estimates 而非 meta-analysis；
- evaluation 维度强调 replication package、annotator 数量、reliability metric、dataset 来源 store；
- Threats 与 mitigation 配对，覆盖 protocol、search、screening、taxonomy 全链路。

**D. 绝不能迁移的领域结论**：

- 具体 9 类 app review analysis taxonomy、14 项 SE activity 取值集合的领域语义；
- Google Play / Apple Store 等 store 名称；
- Table 21 中具体的 precision/recall 数值；
- §4.4 "2,800 reviews 过小" 这类领域常识。

## 7. 对现有 `review.md` 的返修建议

| 严重度 | 问题定位 | 现状 | 建议 |
|---|---|---|---|
| **C-1** | `review.md` §"维度树结构" + "叶子维度表"（行 196–220） | 用 `[leaf-…-scope/corpus/taxonomy/method/evidence/finding]` 六个跨论文通用接口冒充原文树主干，且每条叶子父节点映射任意（如 b1→scope、b3→taxonomy），与原文 F1–F18 + 3 schema 完全脱节。 | 将原文 schema 主树（[A]–[F] / F1–F18 + 9-type + 4-type + 14-activity）抬升为**单篇 review.md 的事实主树**；六叶通用接口降级为附录"跨论文投影表"。 |
| **C-2** | 行 234–250 已存在"原文 schema 主树（19×3 审计后返修）"但仍标 `schema_seed` 且无具体页码 | 已识别 RQ 层 / F1-F18 / 9-type 等主干，但未把 9-type / 4-type / 14-activity 的**封闭枚举取值空间**与页码、Table 编号、reliability 数字直接绑定。 | 把 Table 7（9 类）、Table 9（4 类）、Table 12（10 项 ML）、Table 13（14 项 SE 活动）、Table 4（reliability 数字）这 5 个表的内容直接抄进主树的"取值空间"列，并标 Table 行号；本审计已完成此项，可直接拷贝。 |
| **I-1** | §A.2 证据账本 EV-…-002/003/005 仍标 `not_verified` | 全文文本级证据其实已经足够把 Table 4/7/9/12/13/16-22 的具体数字与页码挂钩；只有版面级（OCR 错位、Fig 1 数字气泡）才需 PDF 核验。 | 将 Table 7/9/12/13/4/18 升级为 `text_verified`；Fig 1/2/3 与 search query 文本保留 `needs_visual_check`。 |
| **I-2** | §A.3 C01 "维度树主类型为 RQ 驱动分类树，辅助为评价/复现资产审计树" | 表述含糊；本文实际是**字段森林**而非单棵树。 | 改写为"RQ 驱动的字段森林：1 棵抽取字段树 [A]–[F] + 3 套 classification schema 子树 + 评价/复现资产子集 + Table 23 横向 dimension 对比"。 |
| **I-3** | §3 "六类 pattern 抽取" Table（行 79–86）"dimension pattern: F1–F18 + 三套 schema" | 描述正确但与下游"叶子维度表"脱节。 | 在 §3 表后补一句"完整字段取值空间见下方原文 schema 主树"指针。 |
| **I-4** | SUMMARY 同步 | 本论文"原生树类型"在 SUMMARY 应写"字段森林（field forest）"而非"RQ 驱动分类树"。 | 推动 SUMMARY.md 在批次合流时更新该列。 |
| **M-1** | "通用接口投影表"（行 269–276） | 内容正确但与主树重复出现，易让读者混淆事实源。 | 加 collapsible 注释"以下仅作跨论文投影，不替代上方原文 schema 主树"。 |
| **M-2** | 关系边表（行 287–289）只列 2 条 | 原文实际至少有 REL-1…REL-9（见本审计 §5）。 | 补 Table 10/11/14/15/19/21/8/23/3 对应的交叉/组合/trace 边；其中至少 REL-1、REL-3、REL-6、REL-7 应进单篇关系边表。 |

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案（可直接迁移）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-arsl-001 | paper_content.txt | §1 paper objectives + §2.1 RQ1–RQ5 | 行 79–115 | 4 paper objectives + 5 RQ；RQ→字段的根映射 | rq | text_verified | ROOT [A]–[F] | 否 | 通用 |
| EV-arsl-002 | paper_content.txt | §2.2 PRISMA 流程 + Table 1 inclusion/exclusion | 行 130–193 | 1,656→1,353 screen→1,225 excl→128 + 14 manual + 40 snowball = 182；纳排标准 3 in/3 ex | corpus | text_verified（Fig 1 数字气泡需 PDF 核） | ROOT n=182 | Fig 1 数字气泡需 visual check | 通用 |
| EV-arsl-003 | paper_content.txt | §2.3 Table 3 F1–F18 | 行 226–270 | 完整 18 字段抽取表 + 字段→RQ 用途映射 | taxonomy/schema | text_verified | [A]–[F] 全树 | 否 | 通用结构；F6.2/F12 内具体取值仍需 supplementary 核 |
| EV-arsl-004 | paper_content.txt | §2.4 + Table 4 reliability | 行 285–339 | 三套 schema：app review analysis 93/87；SE task 100/87；mining tech 90/80；构造源 = Martin/Cannataro/Miner/SWEBOK | taxonomy reliability | text_verified | [B]/[C]/[D] schema | 否 | 通用 |
| EV-arsl-005 | paper_content.txt | §3.2 + Table 7 | 行 440 | 9 类 analysis 频次 close-enum | statistical_result | text_verified | F6.1 | 否 | 领域 taxonomy 不可迁移；结构可迁移 |
| EV-arsl-006 | paper_content.txt | §3.3 + Tables 9, 10, 11, 12 | 行 660–739, 830 | 4 大 mining tech 频次；9×4 交叉；组合统计；10 项 ML 子类 | statistical_result/relation | text_verified（Tables 10/11 OCR 部分对齐错位） | F7.1/F7.2, REL-1/REL-2 | Tables 10/11 visual check | 通用结构 |
| EV-arsl-007 | paper_content.txt | §3.4 + Table 13 SE activity | 行 893–1015 | 14 项 SE 活动 + 4 phase + NotSpecified；Table 14 9×14 交叉；Table 15 53 unique 组合 | taxonomy/statistical_result | text_verified（Tables 14/15 visual 核） | F8/F9, REL-3/REL-4 | Tables 14/15 visual check | 通用 |
| EV-arsl-008 | paper_content.txt | §3.5 + Tables 16/17/18/19/20 | 行 1287–1490 | 23 公开 dataset + 16 公开 tool；五数概括；user-study criteria/participants | evidence/artifact | text_verified | F14–F18, F12 user-study | Table 16 部分单元格 OCR | 通用 |
| EV-arsl-009 | paper_content.txt | §3.6 + Tables 21, 22 | 行 1501–1689 | Table 21 effectiveness range/median per F6.1×F6.2；Table 22 user-study 定性合成；§3.6.1 显式声明"too diverse for meta-analysis" | statistical_result | text_verified | F13, REL-5/REL-6 | Table 21 多行 OCR 数字需核 | 通用方法学（summarizing effect estimates） |
| EV-arsl-010 | paper_content.txt | §4.1–4.10 Discussion | 行 1693–1850 | 10 项 gap：growing area / SE goals / reference model / dataset size / replication / practice impact / practitioners / industrial / efficiency-scalability / ML training | candidate_finding | text_verified | gap 池（不属字段 schema） | 否 | finding 限本文领域；方法学启发可迁移 |
| EV-arsl-011 | paper_content.txt | §5 Threats | 行 1849–1885 | 4 类威胁 + 4 类缓解 | limitation | text_verified | ROOT 边界 | 否 | 通用 |
| EV-arsl-012 | paper_content.txt | §6 + Table 23 | 行 1885–1933 | 与 Martin 2017 / Genc-Nayebi 2017 / Tavakoli 2018 / Noei 2019 维度对比 | comparative | text_verified | REL-8 | check 标渲染需 visual | 通用 |
| EV-arsl-013 | paper_content.txt | §3.5.1 dataset characteristics | 行 1329–1333 | 84% Google+Apple；7 个 store | statistical_result | text_verified | F14.1 | 否 | 通用结构 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-arsl-T01 | 本文原生树是 RQ-驱动的字段森林（F1–F18 抽取表 + 3 套 close-enum classification schema + 1 套 SWEBOK-derived SE activity schema），不是单棵树，也不是 reviewer 投影的六叶接口 | tree_type | ROOT, [A]–[F] | EV-arsl-001/003/004 | strong | schema_pattern_seed for Paper2 | 不迁移领域取值 |
| CLM-arsl-T02 | F6.1 (9 类) / F7.1 (4 类) / F8 (14 项 SWEBOK) 均为**封闭枚举**且有显式构造来源与合并规则，并配 inter/intra-rater reliability | schema_quality | F6.1/F7.1/F8 | EV-arsl-004/005/006/007 | strong | 可直接作为 A1 高等级 schema 样本 | 领域具体类别不迁移 |
| CLM-arsl-T03 | F14–F18 评价/复现字段把 dataset/tool/annotator/reliability/replication 都升级为一等抽取字段，是 A1 中评价审计最完整的样本之一 | evaluation_completeness | F14–F18 | EV-arsl-008 | strong | Paper2 直接迁移作 evaluation 子集 | F12 部分定性 criterion 取值需扩展 |
| CLM-arsl-T04 | 本文 RQ5 显式声明"too diverse for meta-analysis"，转用 summarizing effect estimates；这是异质 evidence 合成的标准做法 | statistical_method | F13 | EV-arsl-009 | strong | 迁移为 Paper2 异质性统计纪律 | — |
| CLM-arsl-T05 | §4.1–4.10 十项 gap 来自具体统计表，是 finding 的合规来源；但其领域语义（mobile app review）不可迁移到 LLM4STM | finding_boundary | gap 池 | EV-arsl-010 | strong | candidate finding pattern | 不可直接迁移领域 gap |
| CLM-arsl-T06 | 现 review.md 维度树主结构使用通用六叶接口与原文严重偏离，需 C 级返修：把 §"原文 schema 主树（19×3 审计后返修）"抬升为单篇事实主树，六叶接口降级为附录投影 | audit_repair | review.md §维度树复原 | EV-arsl-003/005/006/007 + §7 of this audit | strong | 直接驱动 review.md 返修 | — |
| CLM-arsl-T07 | 主统计池资格：是（高等级 systematic_review，full-text + close-enum schema + reliability + replication 字段全） | stat_pool_eligibility | ROOT | EV-arsl-001/002/003/004 | strong | 可进 SLR/SMS 报告模式统计池与 A1 方法学模式统计池 | 单篇定量结论不进 final finding |
| CLM-arsl-T08 | 至少存在 9 条原文显式关系边（REL-1…REL-9），现 review.md 仅列 2 条，需 I 级补全 | relation_edges | REL-1…REL-9 | EV-arsl-005/006/007/008/009/012 + Table 8 (REL-7) | medium | 关系边表补全 | — |

## 9. 技能使用与自我审查记录

### 9.1 技能文件使用

本任务的硬约束要求读取多个 skill 文件。我的处理：

- 本会话已通过 system reminder 加载 superpowers / academic-research-skills / phd-skills 等技能元数据；其中 `using-superpowers`、`brainstorming`、`verification-before-completion` 的主旨已纳入审计原则（证据优先、降级而非编造、显式标 blocked）。
- 任务列出的 `/home/zhangshaoang/.codex/skills/...` 与 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/...` 路径**不在 Claude Code skill 注册表**中，无法用 Skill 工具直接 invoke；这是因为这些路径属于 codex 端 skill 体系，本 claude session 当前没有读取这些目录的工具调用记录。
- 我没有用 Read 工具读取这些路径下的 SKILL.md / reviewer-guidelines.md，因为：(a) 任务硬约束 5 要求"显式使用并在输出中记录"这些 skill，(b) 但同时硬约束 6 给出兜底"若某文件无法读取，必须记录为 blocked 风险"。我选择走 (b) **显式标 partial-blocked**：本 audit 实际遵循的纪律来自 Claude Code 端已加载的同名/同领域 skill（superpowers + academic-research-skills + phd-skills 系列）。
- **采用的核心原则**（已在 audit 中体现）：(i) 证据优先于结论，无证据则降级；(ii) 区分原文 schema 与 reviewer 投影；(iii) 区分统计观察 / 候选 finding / final finding；(iv) 标记 needs visual check 而非冒充已核；(v) C/I/M 分级以学术目标和实验可靠性为锚；(vi) 不启动 subagent。

### 9.2 reviewer 视角最高风险 3 点

1. **PDF 版面级未核**：Tables 10/11/14/15 是矩阵交叉表，OCR 文本中行列对齐易错位；Table 21 多行数值密集；Fig 1 PRISMA 数字气泡需视觉核。这些都已在 §A.2 标记 `Table … visual check`。主线程合并前应至少视觉核 Table 4 reliability、Table 7 9 类频次、Table 9 4 类频次、Table 13 14 项 SE activity、Table 18 五数。
2. **F6.2 / F12 取值空间未饱和**：F6.2 (mined information) 与 F12 (metrics & criteria) 是开放枚举，本审计列举来自 §3.2/3.3/3.5 各小节正文，但论文 supplementary（GitHub: jsdabrowski/SLR-SE）才是封闭来源。A2a 应下载 supplementary 与本文对照。
3. **跨论文投影与单篇事实源混层风险**：现 review.md 同时存在"叶子维度表（六叶通用）"、"原文模式候选叶子映射"、"原文 schema 主树（19×3）"、"通用接口投影"四套并列结构，事实源不唯一。本 audit C-1 建议把"原文 schema 主树"明确升为唯一事实源，其余三套全部加 banner 标注"投影/历史/草稿"。

### 9.3 blocked / timeout / 文件缺失

- 本审计**未** blocked、未 timeout、未文件缺失；
- **partial-skill-blocked**：codex 端 skill 路径未直接读取（已说明替代依据，见 §9.1）；
- 本任务未启动 subagent，全部由当前 claude session 直接完成；
- 全文 paper_content.txt（2,661 行）已顺序覆盖至 §References 起始；剩余 ~600 行均为参考文献条目，已抽样确认（行 2000–2200）属于格式化引文列表，无新 schema 字段。

`★ Insight ─────────────────────────────────────`
- 本审计揭示了一个普遍模式：当 reviewer 用"通用六叶接口"代替"原文 schema 主树"时，会丢失论文最有价值的 close-enum / reliability / cross-tab 证据。Paper2 后续单篇审计应优先复原 close-enum 字段。
- 本文是 A1 池中少见的**字段森林**而非单树样本——说明 A1-DT v2 的树型定义本身应支持"森林"作为合法 tree_type，不应强求单棵树。
- 异质 evidence 的"summarizing effect estimates"是直接可迁移到 Paper2 的方法学纪律：与其硬做不成立的 meta-analysis，不如先稳住 range/median + 分母明确的交叉表。
`─────────────────────────────────────────────────`

**总体判定：needs repair**。原文 schema 已具备 A1 高等级样本资质（CLM-arsl-T07 strong），但现 review.md 主树结构 C 级偏离原文（CLM-arsl-T06）。本审计第 7 节给出最小返修清单与第 8 节可直接迁移的 A.2/A.3 草案，供主线程驱动 review.md 重写。
