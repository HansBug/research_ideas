# app-reviews-slr-se · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude（作为 PR #135 的 `claude` 学术 reviewer 进行只读审计，不修改任何仓库文件）。
- 是否读取 `$ai-research-writing-skill`：否。`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` 以及其 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` 路径在本沙箱中不存在（codex skills 目录未被挂载到当前 Claude Code 会话）。本次审计改用以下等价口径替代：仓库 [CLAUDE.md](../../../../../CLAUDE.md) §“学术研究仓库 Review 口径规范”、`survey_of_surveys/GUIDE.md` 和 `patterns/pattern-field-schema.md`，以及导师 talks（`project_1/talks/SUMMARY.md`）中关于“维度树须忠实复原原文 schema，不得用通用接口冒充原文叶子”的硬约束。
- 是否读取 `$research-planning`：否。同上，`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md` 在本沙箱不可达；以 `survey_of_surveys/README.md` 与 `paper2 story/paper_story.md` 的检索/抽取/分类/统计/finding 形成路径作为替代规划口径。
- 是否读取 `$oh-my-codex:autoresearch`：否。`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/...` 同样不可达；以 `survey_of_surveys/GUIDE.md` 的 A1→A2a 升级纪律作为替代。
- 是否完整阅读 `paper_content.txt`：是（2661 行全文）。覆盖 RQ 段（pp.3-4 §2.1）、检索/筛选/PRISMA（pp.4-6 §2.2）、Table 1 纳排（p.6）、Table 2 venue（p.6）、F1-F18 抽取表（pp.6-7 §2.3 Table 3）、Inter/Intra-rater coding（pp.7-9 §2.4 Table 4）、分类 schema 构造（§2.4，9+4+14 类）、Demographics（pp.9-12 Table 5/6）、RQ1 分析类型 Table 7（p.11，9 类频次）、Table 8 数据组合（p.12）、Table 9 mining technique（p.16）、Table 10-12 技术×分析交叉表（pp.16-22）、Table 13 SE activity（pp.22-23，14 类）、Table 14-15 activity×analysis 交叉表（pp.25-26）、Table 16-17 dataset/tool（pp.33-37）、Table 18 five-number summary（p.37）、Table 19-22 user-study & effectiveness（pp.37-44）、Table 23 与既有 survey 对比（p.50）、§4.1-4.10 共 10 个 discussion finding（pp.45-49）、§5 Threats（p.49）、§6 Related work、§7 Conclusion。
- 是否核对 `paper.pdf`：否。本轮以文本核对为主；当前 review.md A.4 已将“PRISMA 图、Table 5-23 视觉核验”列为 `needs_manual_check`，本审计沿用该标记不重复 PDF 视觉核验，但已在文本上锁定页码与表号。

## 2. 原文真实结构复原

### 2.1 RQ / 研究目标 / 贡献声明

- 总目标（p.3 §2.1）：理解 app review analysis 如何支持 SE。
- 五个 RQ（p.3 §2.1）：
  - RQ1 app review analysis 的类型；
  - RQ2 实现这些分析的技术；
  - RQ3 被声称受支持的 SE 活动；
  - RQ4 评价方法；
  - RQ5 评价结果（“how well do existing app review analysis approaches support software engineers”）。
- 贡献（§7 Conclusion，p.51）：182 篇 primary studies；9 类 review analysis；4 类 mining technique；14 类 SE activity；effectiveness 与 user-perceived quality 两条评价线；以及 10 项研究 implications/future work（§4.1-4.10）。

### 2.2 方法流程

- 协议遵循 Kitchenham 2004 SLR（§2，p.3）。
- 检索（§2.2，pp.4-5）：六大数字库（ACM DL、IEEE Xplore、SpringerLink、Wiley、Elsevier ScienceDirect；文本提取只清晰显示五个，第六个待 PDF 核验）；时间窗 2010-01—2020-12；两条 query：specific + generic。
- PRISMA 数量链（§2.2，p.4 Figure 1）：1656 → 去重 303 → 筛 1353 → 排 1225 → +14（手工 venue）→ +40（snowballing 含 backward 全部 / forward 仅 10 篇 top-cited）→ 182。
- 纳排（Table 1，p.6）：3 条 inclusion + 3 条 exclusion；inter-rater κ=0.9，20 篇 pilot。
- 数据抽取（Table 3，p.7）：F1-F18 抽取表，每条字段都明确指向 RQ（F1-F5 documentation，F6→RQ1，F7→RQ2，F8-F9→RQ3，F10-F12/F14-F17→RQ4，F13→RQ5，F18→RQ4），且部分字段有显式子字段（F6.1/F6.2/F6.3，F7.1/F7.2，F10.1/F10.2，F14.1/F14.2）。
- 抽取可靠性（§2.3，p.7）：intra-rater 93%（20% 样本），inter-rater 90%（10% 样本）。
- 分类 schema 三套（§2.4，pp.7-9）：
  - App Review Analysis：5（Martin 2017）+ 7（Cannataro & Comito 2003 mining）+ 7（Miner 2012 text analytics）→ 合并去重 → 8 → +Recommendation → 最终 9 类（Table 7）。
  - Mining Technique：4（Tavakoli 2018）+ 1（statistical analysis from Miner 2012）→ 排除 feature extraction → 最终 4 类（Table 9，Manual / NLP / ML / Statistical）。
  - SE Activity：258 SWEBOK 候选词 → 58 候选 → 排除 44 不匹配 → 最终 14 类（Table 13）。
- 分类可靠性（Table 4，p.9）：Review Analysis intra/inter = 93%/87%；SE Task = 100%/87%；Mining Technique = 90%/80%。
- 合成（§2.4）：spreadsheet → descriptive statistics + 交叉表；明确声明因 heterogeneity 不做 meta-analysis（§3 后续与 §4 多处）。

### 2.3 原文显式 schema / 字段 / 表 / 图（必须在维度树中能找到锚点）

| 原文对象 | 位置 | 内容 |
|---|---|---|
| F1-F18 + 子字段 F6.1-F6.3 / F7.1-F7.2 / F10.1-F10.2 / F14.1-F14.2 | Table 3, pp.6-7 | 抽取表，绑定 RQ |
| 9 类 App Review Analysis | Table 7, p.11 | Information Extraction 56(31%)、Classification 105(58%)、Clustering 44(24%)、Search/IR 24(13%)、Sentiment 40(22%)、Content Analysis 54(30%)、Recommendation 30(16%)、Summarization 25(14%)、Visualization（第 9 类，频次低） |
| Data combined with reviews | Table 8, p.12 | 与 review 联合使用的数据类型清单 |
| 4 类 Mining Technique | Table 9, p.16 | Manual / NLP / ML / Statistical |
| Mining technique × analysis 交叉表 | Table 10, p.16 | RQ1×RQ2 矩阵 |
| Mining technique 组合 × analysis | Table 11, p.18 | MA/NLP/ML/SA 组合用法 |
| ML 子技术分布 | Table 12, p.22 | 监督/非监督等子分类 |
| 14 类 SE Activity | Table 13, pp.22-23 | requirements / design / construction / testing / maintenance 等子领域，含未指定 activity |
| Analysis × SE activity | Table 14, p.25 | RQ1×RQ3 矩阵 |
| Analysis 组合 × SE activity | Table 15, p.26 | 同上组合表 |
| Public datasets | Table 16, pp.33-36 | 公开 annotated dataset 清单 |
| Public tools | Table 17, pp.36-37 | 公开 review-mining 工具清单 |
| Five-number summary of dataset size | Table 18, p.37 | min/Q1/median/Q3/max |
| User-study evaluation criteria | Table 19, p.38 | user study 评估准则映射 |
| User-study participants | Table 20, p.39 | 参与者类型 |
| Effectiveness controlled experiments | Table 21, pp.40-43 | 控制实验结果合成 |
| User-study qualitative synthesis | Table 22, pp.43-44 | qualitative 评估合成 |
| 与既有 survey 对比 | Table 23, p.50 | 7 个 dimension × 5 个 survey 的覆盖对比 |
| 10 个 discussion finding | §4.1-4.10, pp.45-49 | growing interest / SE goals & use cases / reference model / dataset size / replication package / practice impact / practitioner requirements / industrial needs / efficiency & scalability / ML training |
| 4 类 Threats | §5, p.49 | incompleteness / publication bias / subjectivity / taxonomy reliability |

### 2.4 Finding 形成路径

§4 每一个小节明确遵循“RQx 统计观察 → 量化片段（Table N、X%、N studies）→ 解释 → 缺口 / future work”范式；例如 §4.4 引用 Table 16/17、给出“平均 2,800 reviews”、对比真实 app 体量；§4.5 引用 Table 16/17 缺乏 replication package；§4.10 引用 RQ2 ML 频次得出训练成本/漂移问题。这是 paper2 story 中“候选 finding 必须带统计来源”的范式样本。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过（标题口径）但缺贡献声明 | `[dim-app-reviews-slr-se-root]` 文字尚可，但没有把 5 个 RQ 显式挂到根。 | M |
| 主干分支是否覆盖原文 schema | **不通过** | 当前 5 个 b1-b5 试图对应 RQ1-RQ5 + discussion，但 b4 把 RQ4 与 RQ5 合并为“评价与复现资产”，b5 退化为“discussion gap”，导致 RQ5（“how well … support”）这条贡献声明被吞掉；同时缺失“report structure / threats / related work comparison（Table 23）/ artifact spreadsheet”几个原文必备分支。 | I |
| 叶子维度是否足够具体 | **严重不通过** | 6 个 `leaf-*` 全是“scope / corpus / taxonomy / method / evidence / finding”这类**跨论文通用接口词**；原文真正可写成叶子的对象（F1-F18 抽取字段、9 类 analysis、4 类 mining technique、14 类 SE activity、Table 8 / 10-12 / 14-15 / 16-23 字段、§4.1-4.10 ten findings、§5 four threats）几乎没有一个被独立挂在树上，仅在“原文模式候选叶子映射”表中以 5 行 `not_verified` schema_seed 占位。这与 PR body 中“严防把通用 6 leaf 接口当成原文 schema”的红线直接相撞。 | **C** |
| 取值空间是否可执行 | 不通过 | 6 个通用 leaf 的取值空间写法（“自由文本”“层级枚举”“布尔/数值/链接状态”）是 schema seed 字段；但原文已经给出**封闭枚举**：9 类 analysis、4 类 technique、14 类 SE activity 都可以直接固化，缺失值语义（“paper 未明确 SE activity”）也已经在 Table 13 注脚中显式存在。当前树没有把这些封闭枚举钉死，A2a 看不到从哪里升级。 | I |
| 关系边是否缺失 | 不通过 | 关系边只画了 method↔evidence 与 taxonomy↔finding 两条；原文的关键关系边（analysis × technique = Table 10/11；analysis × SE activity = Table 14/15；technique × ML 子类 = Table 12；analysis ↔ dataset/tool = Table 16/17；analysis ↔ effectiveness/user-study = Table 19-22；分类 schema ↔ inter/intra-rater = Table 4）几乎没有进入关系边表。 | I |
| 统计用途 / 分母是否正确 | 通过（保守口径） | 统计与候选发现链路明确写明“A1-DT 阶段仅作 schema seed，不进入主统计池”，分母分别给出“19 篇文库”“182 篇分类表”“统计结果+discussion”，口径与 Paper2 story 一致。 | 通过 |
| 候选 finding 路径是否完整 | 不通过 | §4.1-4.10 共 10 个 discussion finding 与 §5 的 4 类 threat 都没有进入候选 finding 台账；当前只有抽象的“可生成与 ‘统计观察与候选发现’ 相关的候选发现”一句模板话。 | I |
| A.1-A.4 证据链是否足够 | 不通过 | A.2 五条 EV-001~005 的“原文页码”全部写成“摘要/方法/结果页；待 A2a 精确页码复核”；但 paper_content.txt 已经能精确到 Table 3=p.7、Table 7=p.11、Table 4=p.9、Table 13=pp.22-23、§4.4=p.46、§5=p.49、Table 23=p.50 等；当前 review 用“全文 not_verified”兜底，与“尽可能完整阅读 paper_content.txt”的根级规定（CLAUDE.md §3.2/§5.2）和 paper2 story 中“证据强度优先升级”的纪律不一致。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过 | 整体保持 `weak`/`schema_seed`/`candidate_finding`，未把 Roadmap 写成完成型统计 finding；没有把 not_verified 升级成可统计结论。 | 通过 |

## 4. 建议维度树骨架

下面给出更忠实于原文的最小修复方案。沿用 `[dim-]/[branch-]/[leaf-]` ID 风格，可以与现有 review.md 中已有节点对齐；建议直接替换“维度树结构”与“叶子维度表”两节。

```text
[dim-app-reviews-slr-se-root] Dąbrowski 2022 SLR on App Reviews for SE
├── [b1] RQ1 App Review Analysis 类型（F6 / Table 7）
│   ├── [leaf-rq1-analysis-type] 9 类封闭枚举：Information Extraction / Classification / Clustering /
│   │     Search & IR / Sentiment / Content Analysis / Recommendation / Summarization / Visualization
│   ├── [leaf-rq1-mined-info]   F6.2 mined information 子字段（feature / problem report / request / opinion / …）
│   └── [leaf-rq1-data-combo]   Table 8 与 review 联合使用的数据类型
├── [b2] RQ2 Mining Technique（F7 / Table 9-12）
│   ├── [leaf-rq2-technique-class] 4 类封闭枚举：Manual / NLP / ML / Statistical
│   ├── [leaf-rq2-technique-name]  F7.2 具体技术名（Naive Bayes、SVM、LDA、…）
│   ├── [leaf-rq2-ml-subtype]      Table 12 ML 子分类（监督/非监督/半监督/active learning）
│   └── [edge-analysis×technique]  Table 10/11 RQ1×RQ2 交叉
├── [b3] RQ3 SE Activity（F8-F9 / Table 13-15）
│   ├── [leaf-rq3-activity]   14 类 SE activity（含 “unspecified”缺失值语义）
│   ├── [leaf-rq3-justification] F9 justification 文本字段（可为空）
│   └── [edge-analysis×activity] Table 14/15 RQ1×RQ3 交叉
├── [b4] RQ4 Empirical Evaluation（F10-F12, F14-F17 / Table 16-20）
│   ├── [leaf-rq4-eval-objective]  F10.1（effectiveness / user-perceived quality）+ F10.2
│   ├── [leaf-rq4-eval-procedure]  F11 controlled experiment / user study / case study
│   ├── [leaf-rq4-metrics]         F12 precision/recall/usability/…
│   ├── [leaf-rq4-dataset]         F14 + Table 16 公开数据集 + Table 18 five-number summary
│   ├── [leaf-rq4-annotation]      F15 / F16 / F17 标注任务、人数、质量度量
│   └── [leaf-rq4-tool]            Table 17 公开工具清单
├── [b5] RQ5 Empirical Result（F13 / Table 21-22）
│   ├── [leaf-rq5-effectiveness] Table 21 controlled experiment 结果（range/median per metric）
│   ├── [leaf-rq5-user-study]    Table 22 perceived quality 合成
│   └── [leaf-rq5-participants]  Table 20 参与者类型
├── [b6] Reliability & Methodological Quality（§2.3 / §2.4 / Table 4）
│   ├── [leaf-coding-intra]  F1-F18 intra-rater 93%、各分类 schema intra（93/100/90）
│   ├── [leaf-coding-inter]  F1-F18 inter-rater 90%、各分类 schema inter（87/87/80）
│   └── [leaf-replication]   F18 + §2.4 supplementary spreadsheet
├── [b7] Discussion Finding（§4.1-4.10）
│   ├── [leaf-finding-list]  10 个 finding 各自的“统计来源 → 解释 → 缺口”三元组（必须显式枚举）
│   └── [leaf-finding-link]  每个 finding 与 b1-b6 的统计锚点（如 §4.4 ↔ Table 16/Table 18）
├── [b8] Threats to Validity（§5）
│   └── [leaf-threats]  4 类 threat + 4 类 mitigation
└── [b9] Comparison with Related Surveys（§6 / Table 23）
    └── [leaf-related-coverage]  Martin 2017 / Genc-Nayebi 2017 / Tavakoli 2018 / Noei 2019 的 7 维度覆盖矩阵
```

关键差异：

1. 主干 b1-b5 直接=RQ1-RQ5，与 Table 3 的 F-字段→RQ 绑定一一对应；不再把 RQ4+RQ5 合并；
2. 新增 b6/b7/b8/b9 四个**原文显式存在但当前树缺失**的分支；
3. 每个叶子的取值空间都直接锁定到原文表/图/章节，可在 A2a 阶段直接升级为可统计字段；
4. 关系边显式覆盖 Table 10/11/14/15 这四张原文核心交叉表；
5. 原 review.md 中的 6 个 `leaf-*-{scope,corpus,taxonomy,method,evidence,finding}` 通用接口可降级为 audits/patterns 层的“跨论文接口映射”，不要继续放在本文维度树主干。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支与 RQ 不对齐 | review.md §维度树结构 + “根问题 / RQ 到主干分支映射” | 把 b1-b5 改为 RQ1-RQ5；新增 b6(reliability)/b7(discussion)/b8(threats)/b9(related survey)。 | paper_content.txt L109-115（5 RQ）；§4.1-4.10；§5；§6 Table 23 | **C** |
| 叶子层是通用接口而非原文 schema | review.md §叶子维度表 | 用 §4 列出的 18+ 个原文叶子替换当前 6 个通用 leaf；将 9/4/14 三套枚举钉死为封闭取值空间。 | Table 3 (pp.6-7)；Table 7 (p.11)；Table 9 (p.16)；Table 13 (pp.22-23) | **C** |
| F1-F18 全部塞进单行候选叶子 | review.md §原文模式候选叶子映射 | 把 F1-F18 拆为 18 个候选叶子（或至少按 F6/F7/F8-F9/F10-F12/F13/F14-F17/F18 七组拆开），并标出对应 RQ。 | paper_content.txt L228-269 | I |
| 三套分类 schema 的可靠性证据缺失 | A.2 证据账本 | 新增一条 EV 行专门承载 Table 4（intra/inter 93/87, 100/87, 90/80）；当前 EV-002 含义过宽。 | paper_content.txt L321-339 | I |
| Table 10/11/14/15 交叉表关系边缺失 | review.md §关系边表 | 新增 `[edge-analysis×technique]`、`[edge-analysis×activity]`、`[edge-ml-subtype]`、`[edge-analysis×dataset]` 四条关系边并指明分母（182 篇）。 | paper_content.txt L705-826, L1019-1100 | I |
| §4.1-4.10 十条 finding 未落账 | review.md §统计与候选发现链路 / §A.3 结论-证据映射 | 增加一张 “candidate finding ledger”，逐条枚举 10 个 finding 的“统计观察 → discussion → future work”，并保留 `candidate_finding` 强度。 | paper_content.txt L1695-1849 | I |
| §5 四类 threats 未进维度树 | review.md §维度树结构 / §A.3 | 增加 `[b8] threats` 叶子（incompleteness / publication bias / subjectivity / taxonomy reliability）+ 4 个 mitigation。 | paper_content.txt L1849-1885 | I |
| Table 23 与既有 survey 对比未落账 | review.md §维度树结构 / §A.2 | 增加 `[b9] related-survey-comparison` 叶子，承载 Martin/Genc-Nayebi/Tavakoli/Noei 在 7 维度上的覆盖差异。 | paper_content.txt L1923-1933 | M |
| 证据账本统一 `not_verified` 过度保守 | A.2 EV-001~005 | 把已经在 paper_content.txt 中明确锁定页码/表号的事实升级为 `text_verified`（仍区别于 PDF 视觉核验），并补 `表格或图编号` 字段：Table 3 p.7、Table 4 p.9、Table 7 p.11、Table 13 pp.22-23、Table 23 p.50、§4.1-4.10 pp.45-49、§5 p.49。 | paper_content.txt 全文 | I |
| 根节点定义缺贡献声明 | review.md §根问题映射 | 在 `[dim-root]` 释义中加入 “182 primary studies；9+4+14 三套封闭枚举；effectiveness + user-perceived quality 双线 evaluation；10 个 future-work direction” 这一贡献声明。 | §7 Conclusion (p.51) | M |
| 历史草稿章节标号 `## 历史草稿` 跳过了 §3 / §5 | review.md 节标号 | 把“历史草稿（已迁移）”改为 `## 5.` 或挂为附录，避免目录里 §3 之后直接跳到“历史草稿（已迁移）”。 | review.md 当前结构 | M |

## 6. C/I/M 结论

- **C（critical）**：
  - **C1** 当前维度树以 6 个跨论文通用接口（scope/corpus/taxonomy/method/evidence/finding）作为唯一叶子层，未复原原文显式 schema（F1-F18 + 9/4/14 三套封闭枚举 + Table 10/11/14/15 交叉关系 + §4 十项 finding + §5 四类 threats + Table 23 related-survey 对比）；这直接构成 PR body 红线“把通用 6 leaf 接口误当成原文 schema”，并使 A2a 在维度树上无法落锚，会破坏 Paper2 A2a/A2b 阶段“按原文 schema 抽字段/做交叉统计/做候选 finding”的整条证据链。
  - **C2** 主干 b1-b5 把 RQ4+RQ5 合并、把 §4 discussion 单独算一个 b5，导致 RQ5（“现有方法对工程师的实际支持”）这一贡献声明无叶子承载，会让后续读 A1 维度树的人误以为本文没有专门的“empirical result”分支。
- **I（important）**：
  - I1 Table 4 reliability / Table 10-15 交叉表 / Table 16-22 evaluation 与 user-study / Table 23 related-survey 比较 / §4.1-4.10 ten findings / §5 four threats，均缺独立叶子或独立 EV 行，影响维度树作为 schema seed 的可用性与可审计性。
  - I2 A.2 五条 EV 统一 `not_verified`，但相应事实在 paper_content.txt 已经能锁定具体页码/表号；这种过度兜底会让 audits 主 session 误以为本文证据等级低于实际，从而错配统计池资格。
  - I3 F1-F18 被压缩成单行候选叶子，缺少 F6.x/F7.x/F10.x/F14.x 子字段拆分，A2a 无法继承。
- **M（minor）**：
  - M1 根节点描述缺“182 / 9+4+14 / 10 findings” 贡献声明。
  - M2 节标号在“## 历史草稿”处断层。
  - M3 当前 review.md 未显式把“six major digital libraries 但抽取文本只见五个”这条已经待复核的事实从“§7 待复核”移到 A.4 检查清单中（目前已在 §7 列出，仅为对齐建议）。

- **最终建议：NEEDS FIX**。
  - 触发理由：C1（通用接口冒充原文 schema）与 C2（RQ5 贡献声明无叶子）必须在 A1-DT 合流到 main 之前修复，否则会污染 A2a 的字段枚举与交叉统计入口。M 级问题可作为后续 hardening backlog 不阻塞合并。
