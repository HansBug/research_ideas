# petersen-2015-mapping-guidelines-update · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：否。`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` 等 codex skills 路径在当前 claude 会话不可读取（这些是 codex 侧 skill，不在 claude Skill 工具的 available-skills 列表中）；本审计按 paper-story.md / reviewer-guidelines.md / reviewer-self-review.md 的精神（reviewer 必须先复原原文真实结构再判断现状）执行，但未直接 Read 这三份文件。
- 是否读取 `$research-planning`：否，同上原因。
- 是否读取 `$oh-my-codex:autoresearch`：否，同上原因。
- 是否完整阅读 `paper_content.txt`：是。文件共 1974 行，分两段读取覆盖 §1 引言、§2 Background、§3 方法（含 §3.6 validity 框架与 Table 3 data extraction form）、§4 Results（含 Fig 5–15 频次分布、Fig 12 topic-independent classification facets、Fig 13 topic-related classification、Fig 14 visualizations）、§5 Guideline updates（含 §5.1 planning、§5.1.2 study identification、§5.1.3 extraction/classification、§5.1.4 visualization、§5.1.5 validity、§5.2 conducting、§5.3 reporting、§5.4 evaluate the mapping process 含 Tables 8–13 rubric、§5.5 dissemination）、§6 Conclusions、Appendix A 包含 / 排除清单、Appendix B Tables B.15–B.27（13 个映射表）以及全部参考文献。
- 是否核对 `paper.pdf`：否。本审计为文本级与 review.md 已存事实的一致性审计；版面图表精核为 A2a 任务（与 review.md A.4 `cmd-…-visual-check` 状态 `needs_manual_check` 一致）。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

原文目标为更新 2008 年 Petersen et al. SMS guideline，方法为对 2004–2012 年 SE mapping studies 做 systematic mapping。四个 RQ：

- RQ1：哪些 guidelines 被用于 SE SMS。
- RQ2：被覆盖的 SE topics。
- RQ3：发表 venue 与时间。
- RQ4：systematic mapping process 如何被执行（含 study identification、classification、visualization）。

三项贡献声明：评估 SMS 当前做法、与 Kitchenham & Brereton 2013 best practices 比较、合并为更新版 guideline。

### 2.2 方法流程与 finding 形成方式

- 数据库：IEEE Xplore、ACM、Scopus、Inspec/Compendex。
- 流程（Fig 1）：7752 → 5082（删 2004 前）→ 60（题摘）→ 43（全文）→ 54（snowball）→ 44（QA）→ 52 + 8 + 11（reviewer 复查 + snowball 增补）= 52 主要研究。
- QA 三问：动机清晰、mapping process 清晰、是否有 empirical evidence / results。
- finding 形成：先对 52 篇做频次统计（Fig 2–15、Table 4、Appendix B 13 张映射表），与 Table 5 中 10 份既有 guideline 做活动比较，再合并出更新 guideline（§5）并构造 evaluation rubric（Tables 8–13）。

### 2.3 显式抽取字段、taxonomy、coding scheme、rubric、图表

原文真正显式定义的 schema 元素：

1. **Data extraction form (Table 3, p.4)** — 11 字段：Study ID、Article Title、Author Name、Year of Publication、Area in SE (SWEBOK)、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type。
2. **Validity taxonomy (§3.6, §5.1.5)** — 5 类：descriptive、theoretical、generalizability（external / internal）、interpretive、repeatability。
3. **Search strategy facets (Fig 6)** — 3 类：database、manual、snowballing。
4. **Developing search (Fig 7, Table B.19)** — 5 strategies：PICO(C)、consult experts/librarians、iteratively improve、keywords from known papers、standards/encyclopedias/thesaurus。
5. **Evaluating search (Fig 8, Table B.20)** — 4 strategies：paper test-set、expert evaluation、authors' web pages、test–retest。
6. **Inclusion/exclusion (Fig 9, Table B.21)** — 3 strategies：identify objective criteria、resolve disagreements with additional reviewers、decision rules（Ali & Petersen Table 6 六格 A–F）。
7. **Data extraction process (Fig 11, Table B.23)** — 4 strategies：identify objective criteria、obscuring information、additional reviewer + 协商、test–retest。
8. **Topic-independent classification facets (Fig 12, Table B.24)** — 5 facets：venue、research type、research method、study focus、contribution type。
9. **Research type taxonomy (Wieringa, Table 7)** — 6 类决策表：evaluation research、solution proposal、validation research、philosophical paper、opinion paper、experience paper。
10. **Research method classification (Fig 19)** — controlled experiment、case study、action research、survey、ethnography、simulation、prototyping、mathematical analysis、lab experiment 等，并按 validation / evaluation research 归类。
11. **Publication venue classification (Fig 18, Finland Ministry of Education)** — peer-reviewed / non-refereed / professional / general public / artistic / thesis / patents / audiovisual 等多级层。
12. **Topic-specific classification (Fig 13, Table B.25)** — 2 类：emerging classification（keywording → open coding）、existing scheme（IEEE / ISO / SWEBOK）。
13. **Visualization taxonomy (Fig 14, Table B.26)** — 6 类：line diagram、pie diagram、bar plot、bubble plot、Venn diagram、heatmap。
14. **Guideline comparison matrix (Table 5)** — 10 列 guideline × 多行 activities，构成 mapping process 整体活动空间。
15. **Updated mapping process (§5)** — 三阶段：planning（need identification & scoping → study identification → data extraction & classification → visualization → validity threats → evaluate the mapping）、conducting、reporting。
16. **Reporting structure (§5.3)** — Introduction / Related Work / Research Method（含 RQ、search、study selection、data extraction、QA、analysis & classification、validity）/ Results / Discussion-Conclusions / Appendix。
17. **Evaluation rubric (Tables 8–14)** — 26 个 actions（Table 8）+ 5 张 rubric 表（need、search strategy、search evaluation、extraction/classification、validity）+ Table 14 现有研究在 rubric 上的频数。
18. **Appendix B（Tables B.15–B.27）** — 13 张映射表：studies per topic、venues、guidelines、search strategies、developing search、evaluating search、inclusion/exclusion、QA、data extraction process、topic-independent classification、topic-related classification、visualizations、validity threats。

### 2.4 finding / gap / recommendation 链路

- 频次统计（Fig 5–15、Appendix B）→ 与 Table 5 既有 guideline 对照 → 暴露 guideline 覆盖空缺 → 在 §5 各小节给出 recommendation（PICO 用 P+I、Finland venue 分类、Wieringa 研究类型决策表 Table 7、研究方法–研究类型映射 Fig 19）→ §5.4 构造 rubric → 把 52 篇 rubric 评分（Table 14、Fig 20–21）写为 evidence-based reflection。
- §6 给出 RQ1–RQ4 的 finding（最常用 guideline 是 Kitchenham 2007 与 Petersen 2008、SWEBOK 覆盖良好、testing 最热、conf/journal 各占约半、需要 trade-off effort vs reliability）。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本通过 | 根节点写"Guidelines for conducting systematic mapping studies …"，与论文标题、RQ、贡献声明一致。 | 通过 |
| 主干分支是否覆盖原文 schema | 不通过 | 当前主干为 `b1 planning / b2 conducting / b3 reporting / b4 quality rubric / b5 topic-independent dimensions`。原文 §5 明确只有三个阶段（planning / conducting / reporting）；`quality rubric` 是 §5.4 "evaluate the mapping process"，属 planning 阶段子节点；`topic-independent dimensions` 是 §4.4.4 / §5.1.3 data extraction & classification 下的 facets，属 conducting 阶段子节点。把它们升格为主干使得真正的 conducting 子结构（search strategies、inclusion/exclusion、extraction、classification、visualization）被压缩成一个空节点。 | I |
| 叶子维度是否足够具体 | 不通过 | 当前 6 个 leaf（scope / corpus / taxonomy / method / evidence / finding）是 A1-M0–M6 的通用接口，review.md 第 193 行已自承"不是对原文全部抽取字段、分类项或报告叶子的完成复原"。原文显式列出的 11 个 data extraction 字段、5 类 validity、6 类 visualization、5 类 topic-independent facets、6 类 research type、3 类 search strategy、5 类 developing-search 策略、4 类 evaluating-search 策略、3 类 inclusion/exclusion、6 段 reporting 结构、26 个 rubric actions、13 张 Appendix B 表均未在维度树或候选叶子中以具体节点出现，仅以 `orig-*` 五个顶层标题集中存在。 | I |
| 取值空间是否可执行 | 不通过 | 6 个通用 leaf 的"取值空间"列基本为"自由文本"或"完整枚举 / 层级枚举 / 自由文本"等元描述，没有给出原文真实可枚举值（例如 visualization 的 6 类、validity 的 5 类、research type 的 6 类、search strategy 的 3 类）。在原文已经把这些取值闭合给出的前提下，依然写成开放自由文本，会让 A2a 无法直接进入字段闭合状态。 | I |
| 关系边是否缺失 | 不通过 | 原文存在明显的横向关系：research method ↔ research type（Fig 19 把方法映射到 validation/evaluation research）、guideline ↔ activity（Table 5）、rubric action ↔ rubric score（Tables 8–13）、Appendix B 表 ↔ Fig 5–15。当前 review.md 8.3 节关系边合同存在但**没有任何关系边实例**，导致这些显著的二维 / 跨表关系在维度树中丢失。 | I |
| 统计用途 / 分母是否正确 | 通过（条件性） | A.2 全部证据打 `not_verified`、A.3 全部 `weak/schema_seed`、统计池资格写"否（A1-DT 阶段仅作 schema seed）"。这与 §8.6 临时降级规则一致，没有把弱证据升级为统计结论。原文实际具备非常明确的分母（52 mapping studies、各 Appendix B 表的 studies 列），但当前 review 选择不写入是合理的保守做法；A2a 必须补回分母。 | 通过 |
| 候选 finding 路径是否完整 | 不通过 | 候选发现表只挂在 leaf-finding 一行，写为"统计观察 / discussion → 候选发现 → 研究者裁决"，没有把原文 §6 已给出的 RQ1–RQ4 finding（"individual guidelines not sufficient"、"testing 最热"、"journals/conferences 各半"、"need trade-off effort vs reliability"）作为 candidate finding 实例落地，也没有把 rubric ratio 31%、median 33%、25% > 40% 等量化观察列为候选。即使作为 schema_seed，也应至少给出 1–2 个原文实例作为锚点。 | I |
| A.1–A.4 证据链是否足够 | 部分通过 | A.1 三个来源（pdf/text/bib）齐全且 local_verified；A.2 四条证据皆 `not_verified`，页码全部写"待 A2a 精确页码复核"；A.3 九条结论全部 weak / schema_seed；A.4 两条检查，结构检查 passed、视觉检查 needs_manual_check。结构完备但实际证据强度极弱，未利用全文文本级阅读已能锁定的页码（如 Table 3 在 p.4、Fig 12 在 p.7、Fig 14 在 p.8、Table 5 在 p.9、Tables 8–13 在 p.14、Appendix B 在 p.16–17）。在 review.md 自称"已读全文文本"的前提下，至少应将 EV-…-002 / EV-…-003 升级为 medium 并写明具体表 / 图编号。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过 | 维度树多次显式声明 `schema_seed`、`not_verified`、`A1-DT 阶段仅作 schema seed`，没有把 roadmap / 作者愿景写成完成型统计 finding；快速结论卡片对"图表 / 附录矩阵待 A2a 人工核对"诚实标注。无误导性强主张。 | 通过 |

## 4. 建议维度树骨架

下面给出更忠实于原文的最小修复骨架。它把 `planning / conducting / reporting` 还原为唯一三主干，把 `quality rubric` 和 `topic-independent dimensions` 还原为子节点，并把原文显式枚举的取值空间挂到对应叶子。所有节点初始仍可标 `not_verified` / `schema_seed`，但取值空间不再写"自由文本"占位。

```text
[dim-…-root] Guidelines for conducting systematic mapping studies (RQ1–RQ4)
├── [dim-…-planning] Planning the mapping (§5.1)
│   ├── [leaf-…-need-scoping] Need identification & scoping (§5.1.1)
│   │     取值空间：{examine extent/range, determine value of SLR, summarize findings, identify gaps}（Arksey/O'Malley 4 类目标）+ 高层 RQ + 下层 RQ
│   ├── [leaf-…-study-id-plan] Study identification plan (§5.1.2)
│   │     取值空间：{database, manual, snowballing}×{PICO(C), experts, iterative, keywords-from-known, standards/encyclopedias}×{test-set, expert-eval, authors' web pages, test–retest}×{objective criteria, additional reviewer + 协商, decision rules A–F}
│   ├── [leaf-…-extraction-classification-plan] Extraction & classification plan (§5.1.3)
│   │     取值空间：Table 3 11 字段 + Fig 11 4 策略 + Fig 12 5 facets {venue, research type, research method, study focus, contribution type} + Fig 13 {emerging, existing scheme}
│   ├── [leaf-…-visualization-plan] Visualization plan (§5.1.4)
│   │     取值空间：{line diagram, pie diagram, bar plot, bubble plot, Venn diagram, heatmap}
│   ├── [leaf-…-validity-plan] Validity plan (§5.1.5, §3.6)
│   │     取值空间：{descriptive, theoretical, generalizability(internal/external), interpretive, repeatability}
│   └── [leaf-…-evaluate-mapping-rubric] Evaluate the mapping process / quality rubric (§5.4)
│         取值空间：Table 8 26 actions × Tables 9–13 rubric scores {0,1,2,3} × Table 14 频数 × ratio %
├── [dim-…-conducting] Conducting the mapping (§5.2)
│   └── [leaf-…-conducting-execution] 执行 planning 决策，记录每阶段证据（spreadsheets, reference manager），允许迭代回修。
└── [dim-…-reporting] Reporting the mapping (§5.3)
    ├── [leaf-…-report-structure] Reporting structure
    │     取值空间：{Introduction, Related Work, Research Method(RQ/search/study-selection/extraction/QA/analysis-classification/validity), Results, Discussion/Conclusions, Appendix(included+borderline excluded)}
    └── [leaf-…-dissemination] Dissemination (§5.5)
          取值空间：Fig 18 Finland venue 分类树 × journals/conferences/workshops rubric 分布（Fig 21）

[edge-…-method-to-type] research method ↔ research type（Fig 19）
[edge-…-guideline-to-activity] guideline ↔ activity（Table 5：10 guidelines × activities）
[edge-…-rubric-to-action] rubric category ↔ Table 8 actions
[edge-…-appendixB-to-fig] Appendix B table ↔ Fig 5–15 频次图
```

候选 finding 路径（schema_seed 级，仍需 A2a 精核分母）应至少包含：
- RQ1 finding：Kitchenham 2007 与 Petersen 2008 最常用；24 / 52 篇组合多份 guideline → "individual guideline 不充分"。
- RQ2 finding：testing 最热，education / configuration management 最弱（Fig 3 / Table B.15）。
- RQ3 finding：journals 与 conferences 比例约半（Fig 4），IST 14 篇最多（Table 4）。
- RQ4 finding：rubric ratio 中位 33%，25% > 40%（Fig 20）；search-strategy 与 search-evaluation 多数在 No description / Minimal evaluation（Table 14）。

当前 review.md 已显式声明"叶子层口径校准"作为护栏，但护栏不能替代真实结构 — 建议至少把上述骨架落实为候选叶子（即使全部打 `not_verified`），以避免 A2a 误把通用接口当成原文 schema 全集。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支错位：`b4 quality rubric` / `b5 topic-independent dimensions` 不是原文主干 | "维度树结构" 与"根问题 / RQ 到主干分支映射"表 | 将主干压缩为 planning / conducting / reporting 三个；把 quality rubric 下挂为 planning.evaluate-mapping-rubric；把 topic-independent dimensions 下挂为 planning.extraction-classification-plan 的子节点。 | paper_content.txt §5、§5.1–§5.4 | I |
| 6 个通用 leaf 与原文 schema 不对齐 | "维度树结构"、"叶子维度表" | 用 §4 建议骨架替换或并行新增原文级叶子（need-scoping / study-id-plan / extraction-classification-plan / visualization-plan / validity-plan / evaluate-mapping-rubric / conducting-execution / report-structure / dissemination）。原 6 个通用 leaf 可保留为跨论文接口层，但需明确标注"通用接口（A1-M 映射），不是原文叶子"。 | paper_content.txt §5.1.1–§5.5 | I |
| 取值空间未利用原文已闭合枚举 | "叶子维度表"取值空间列 | 将"自由文本"替换为原文枚举：visualization=6 类、validity=5 类、search strategy=3 类、developing search=5 类、evaluating search=4 类、inclusion/exclusion=3 类 + decision rules A–F、topic-independent facets=5 类、research type=6 类（Wieringa）、reporting structure=6 段、rubric action=26 项。 | paper_content.txt §3.6 / §4.4 / §5.1–§5.4 / Table 3 / Table 5 / Tables 8–13 / Appendix B | I |
| 关系边为空 | §8.3 关系边表 | 至少补 4 条：(1) research method ↔ research type；(2) guideline ↔ activity（Table 5）；(3) rubric category ↔ Table 8 actions；(4) Appendix B 表 ↔ Fig 5–15 频次图。 | paper_content.txt Fig 19 / Table 5 / Tables 8–14 / Appendix B | I |
| `orig-topic-independent-dimension` 挂在 `b3 reporting` 是错的 | "原文模式候选叶子映射"表 | 将其父节点改为 `b2 conducting`（具体落到 extraction-classification-plan）；同时 `orig-quality-rubric` 父节点改为 planning.evaluate-mapping-rubric。 | paper_content.txt §4.4.4 / §5.1.3 / §5.4 | I |
| 候选 finding 没有任何原文实例 | "统计与候选发现链路"、A.3 | 至少在 leaf-finding 下挂 4 个 schema_seed 候选 finding（RQ1–RQ4 §6 结论 + rubric 量化观察），保持 `weak/schema_seed/not_verified` 状态，但用具体原文短语锚定。 | paper_content.txt §6, Fig 20–21, Table 14 | I |
| A.2 证据页码不应全为待复核 | A.2 证据账本 | 在"已读全文文本级"前提下，至少把 EV-…-002 / 003 的"原文页码"从"待 A2a 精确页码复核"升级为具体页：Table 3 → p.4；Fig 12 → p.7；Fig 14 → p.8；Table 5 → p.9；Fig 19 → p.13；Tables 8–13 → p.14；Appendix B → p.16–17。证据强度可保持 `weak`（图表需版面核验），但页码不应空白。 | paper_content.txt 全文已含页眉行 `K. Petersen et al. / Information and Software Technology 64 (2015) 1–18`、`--- Page N ---` | I |
| 快速结论卡片"未做图表视觉级人工核对"与 A.4 状态一致但未给出最小核验清单 | A.4 / §7 待复核 | 把"§7 待复核"7 条与 A.4 visual-check 合并为统一最小核验清单（Table 5 / Fig 12 / Fig 14 / Table 7 / Fig 19 / Tables 8–14 / Appendix B 13 张表），并把每项写明"用于支撑哪个叶子 / 取值空间 / 候选 finding"，避免 A2a 重新猜测。 | review.md §7、A.4 | M |
| `orig-*` 候选叶子取值空间过粗 | "原文模式候选叶子映射"取值空间列 | 把"目标、RQ、protocol、scope、数据库和检索策略"等口语化串展开为原文层级清单。例如 planning 写：{need identification & scoping(Arksey/O'Malley 4 类目标), study identification, extraction & classification, visualization, validity, evaluate-mapping-rubric}。 | paper_content.txt §5.1 | M |

## 6. C/I/M 结论

- C：无。当前 review.md 没有把弱证据升级为统计结论、没有把通用接口冒充原文 schema 全集（已有"叶子层口径校准"声明）、没有把 roadmap / 愿景写成完成型 finding，未直接破坏 Paper2 A1-DT 学术目标或证据链。
- I：8 条。维度树主干结构错位、叶子未对齐原文 schema、取值空间未闭合、关系边为空、`orig-topic-independent-dimension` 错挂、候选 finding 无原文实例、A.2 页码全空、`orig-quality-rubric` 错挂 — 这些会实质影响 A2a 复原原文 schema 与候选发现的可审计性，且当前 PR 仍可在不改变 A1-DT 范围内修复。
- M：2 条。最小核验清单与 §7 合并、`orig-*` 取值空间展开。
- 最终建议：**NEEDS FIX**。当前维度树以通用接口 + 顶层标题候选叶子的方式承载 schema，虽诚实但密度不足以指导 A2a 精核；建议按 §4 建议骨架补足原文叶子、取值空间与关系边，证据强度可保持 `weak/schema_seed`，但结构必须先到位。
