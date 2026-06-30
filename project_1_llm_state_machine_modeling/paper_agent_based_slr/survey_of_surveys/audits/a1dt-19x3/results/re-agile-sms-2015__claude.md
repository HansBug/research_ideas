# re-agile-sms-2015 · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：是。已读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` 与 `references/paper-story.md`、`reviewer-guidelines.md`、`reviewer-self-review.md`（依据 PR 任务要求声明遵循其口径；下文 C/I/M 与对学术目标的影响判断基于上述 reviewer 规则）。
- 是否读取 `$research-planning`：是。已读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`。
- 是否读取 `$oh-my-codex:autoresearch`：是。已读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。
- 是否完整阅读 `paper_content.txt`：是。逐页阅读了全部 9 页 / 954 行（Abstract、I Introduction、II Background、III Methodology、IV Results A–D、V Discussion A–D、VI Conclusion、References、Primary Sources [S1]–[S28]），覆盖摘要、3 个 RQ、检索 / 纳排、抽取与编码、Tables I–V、B1–B6、P1–P6、提出的 agile RE 定义、Limitations、Conclusion 与全部 Primary Sources 清单。
- 是否核对 `paper.pdf`：未做视觉级核对，因为 reviewer 任务限定为文本级审计，并且 `paper_content.txt` 已经稳定还原了 Tables I–V 的代码、文章 ID 和章节结构；版面 / 图形细节未影响本次维度树审计判断。复杂版式或表格的视觉级核对应在 A2a 阶段补做。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文第 1 页明确给出 3 个 overall research questions（不是隐含 RQ）：

1. **RQ1**：What has been researched regarding requirements engineering in an agile context?（研究分布 / 主题 mapping，对应 §IV.A、§IV.B 与 Tables I / II / III）。
2. **RQ2**：What are the reported key benefits of agile requirements engineering?（对应 §IV.C 与 Table IV 的 B1–B6）。
3. **RQ3**：What are the reported problems and corresponding solutions related to agile requirements engineering?（对应 §IV.D 与 Table V 的 P1–P6 以及每个 problem 下的 solution 段落）。

贡献声明（§I, §V.B, §VI）包含三个明确部分：(a) 28 篇 mapping；(b) 提出 agile RE 的综合定义（§V.B 单独段落，是一个**显式 synthesis 产出**，不是路线图愿景）；(c) 指出 P3 / P4 / P6 无解决方案、P1 / P2 解决方案多源自传统 RE 等 gap 与 future work。

### 2.2 原文方法流程 / 抽取 / 编码 / 统计 / finding 形成方式

§III Methodology 明确：

- **检索**：Elsevier Scopus，2014 年 9 月执行，唯一显式检索式：`TITLE-ABS-KEY(("requirements analysis" OR "requirements engineering") AND (agile OR scrum)) AND NOT KEY("agile manufacturing")`，初始 241 条。
- **纳排链条**（数值齐全）：241 → 移除 46 条非 journal / conference → 移除 8 条非英文 → 187 条进入 title / abstract 筛选 → 排除 123 条 → 65 条全文 → 排除 37 条 → **28 条纳入**。Title / abstract 阶段 5 条 exclusion criteria + 全文阶段 3 条 exclusion criteria 均显式列出。
- **抽取字段（显式列出）**：metadata、context、methods、results。
- **编码 / 分类 schema（显式列出）**：将 result 抽取归到 4 个 subject areas — (i) Definition of RE in agile context；(ii) Benefits identified in agile RE；(iii) Problems identified in agile RE；(iv) Solutions proposed for the problems。其中 benefits / problems / solutions 再被 collate / analyse / categorize 到 thematic areas。
- **统计**：venue 分布（Table I）、agile method context 分布（Table II，20 / 7 / 1）、article type 分布（Table III，6 / 5 / 3 / 1 / 2 / 8 / 3）、B1–B6 与 article 映射（Table IV）、P1–P6 与 article 映射（Table V）。所有分母均为 N=28。
- **Finding 形成方式**：从 Tables IV/V 的 problem / benefit / solution 频次 + thematic coding → §V Discussion 中讨论；再从 “P3 / P4 / P6 无 proposed solution”这一显式空白 → §V.C 与 §VI 形成研究 gap 与 future work 建议。

### 2.3 原文显式 extraction form / classification schema / taxonomy / coding scheme / 图表 / roadmap / quality rubric

- **显式 taxonomy**（必须在维度树里出现）：
  - Venue type ∈ {Conference proceedings, Journal, Magazine}（Table I）。
  - Agile method context ∈ {Unspecified agile, Scrum, FDD}（Table II，N=20/7/1）。
  - Article type ∈ {Multiple case study, Single case study, Experience report, Tool evaluation, Method evaluation, Method proposal, Position paper}（Table III）。
  - Benefit codes B1–B6，闭枚举（Table IV）。
  - Problem themes P1–P6，闭枚举（Table V）。
  - Solution per problem：以 P1–P6 为锚点的开放清单（§IV.D 段落级，含 “No solutions to P3 / P4 / P6 were proposed”）。
  - 4 个 result subject areas（Definition / Benefits / Problems / Solutions）。
- **没有**显式 quality rubric / quality assessment table。文中只对 article type 评论（method proposal 缺 empirical evaluation 等），属于 discussion 而非 quality scoring。
- **没有** roadmap figure / proposed framework figure。只有 Tables I–V 共 5 张表，无 figure。
- 不是 guideline / roadmap / proposal paper，而是 “系统检索 + 显式纳排 + 编码 + thematic synthesis” 的标准 SMS。

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

- 从 Table III + §V.A 文章类型分布 → finding：“60% 经验性、29% 无 empirical evaluation 的 method proposal、11% position paper → 需要更多 empirical evaluation”。
- 从 Table II → finding：“71% 未指明 agile 方法上下文，影响泛化性”。
- 从 Table I → finding：“RE 在 ASD 没有稳定 publication venue”，但 IEEE Software 5 篇说明业界关注。
- 从 §IV.D + Table V 中 P3 / P4 / P6 没有 solution → finding 与 future work：“需要更多关于 prioritization、technical debt、tacit knowledge、effort estimation 的研究”。
- §V.B 综合提出 agile RE 的定义，是一个**显式 synthesis 产物**。
- §V.D Limitations：只有 2 条显式（Scopus 单库；关键词集小），未做 quality assessment 也未单独 threats-to-validity 章节。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确 | 根节点表述为 “A Mapping Study on Requirements Engineering in Agile Software Development 的研究目标 / RQ / 贡献声明”，符合原文范围；但未在根节点信息内显式挂 3 个 RQ。 | M |
| 主干分支是否覆盖原文 schema | **覆盖不足** | 当前 5 个主干 b1–b5 是 “综述范围 / 语料 / 主题分类 / 方法 / 评价统计 ” 的通用脚手架（来自 `patterns/pattern-field-schema.md` 的 M0–M6），并非原文 schema 的主干。原文真正的主干至少应包含：**RQ1 研究分布（venue / method-context / article-type 三轴统计）**、**RQ2 Benefit 编码（B1–B6 闭枚举）**、**RQ3 Problem 编码（P1–P6 闭枚举）**、**Problem→Solution 映射（含 “no solution proposed”）**、**Agile RE 定义 synthesis 产物**。当前树把这五块全部塞进 `taxonomy / method / evidence / finding` 四个通用叶子，丢失了原文的最稳定结构。 | **C** |
| 叶子维度是否足够具体 | **过于通用** | 6 个 `leaf-*` 是跨论文通用接口（scope / corpus / taxonomy / method / evidence / finding），不是该原文实际叶子。文中 `“A1-DT 叶子层口径校准”` 自己也承认“跨论文通用接口层…不是对原文全部抽取字段、分类项或报告叶子的完成复原”。后接的 5 条候选叶子（agile-re-topic / problem / benefit / solution / evidence-gap）虽方向正确，但 (a) 没有把 B1–B6 与 P1–P6 这两组**闭枚举编码**列为可观测叶子；(b) 没有把 venue-type / agile-method-context / article-type 这三组 RQ1 用到的具体维度列出来；(c) 把 “evidence-gap” 写成单叶，掩盖了原文显式的 “problem code → solution 缺失” 这种结构性 finding 入口；(d) 没有 “proposed definition of agile RE” 这一显式 synthesis 叶子。 | **C** |
| 取值空间是否可执行 | **不可执行** | 通用叶子表里的取值空间写成 “自由文本”“枚举”“层级枚举” 等类型占位，但**未列原文实际取值**。例如 `leaf-method` 没有写出 {Multiple case study, Single case study, Experience report, Tool evaluation, Method evaluation, Method proposal, Position paper}；`leaf-taxonomy` 没有写出 B1–B6 / P1–P6；`leaf-orig-problem`、`leaf-orig-benefit` 的取值描述是英文长句，但没列具体 code。A2a 拿到这棵树将无法直接对原文进行字段 / 取值核验。 | **C** |
| 关系边是否缺失 | **缺关键关系** | 原文最关键的一条结构关系是 “Problem theme P1–P6 与 Solution 段落的一对多映射，且 P3 / P4 / P6 显式 = 0 solution” —— 这是 §V.C 与 §VI 形成 future work 与 gap 的核心证据链。当前树没有任何节点 / 边表达 problem→solution 映射或 “no solution proposed” 这一观测，全部模糊地塞进 `leaf-finding` 一个叶子。 | **C** |
| 统计用途 / 分母是否正确 | **过度降级** | 所有叶子统计用途字段统一写 “可进入描述统计 / 交叉统计，前提是分母和样本单位明确”，但没有明确 N=28（included articles）、N=187 / 65（纳排链条节点）这两类不同分母。链路表里又把 “是否进入主统计池” 全部标 `否`，与 SUMMARY 中将本篇当成 mapping study 样本贡献编码结构的事实并不矛盾，但**口径未区分 “A1-DT schema seed 不入主统计池” 与 “原文字段本身就具备分母”** 两件事。会让后续 reviewer 误读为本篇无可统计字段。 | I |
| 候选 finding 路径是否完整 | **路径缺失** | 原文至少有 4 条显式 finding 路径：(F1) article-type 分布 → “需更多 empirical evaluation”；(F2) method-context 分布 → “71% unspecified 影响泛化”；(F3) venue 分布 → “RE in ASD 无 home venue”；(F4) **P3 / P4 / P6 无 solution → 显式 future work**。当前 `leaf-finding` 只用一句 “candidate finding / risk_only” 占位，未把这 4 条路径作为可识别的候选 finding 列出，也没区分 “mapping 分布型 finding” 与 “缺失型 finding（gap）”。 | I |
| A.1–A.4 证据链是否足够 | **过度降级 + 锚点不足** | A.2 的 4 条证据 EV-001–004 全部标 `not_verified` 并写 “待 A2a 精确页码复核”。但 `paper_content.txt` 已稳定还原 Tables I–V、3 个 RQ、纳排数值链条、B/P 编码与 Limitations。证据等级至少应区分：(i) 文本级 verified（Tables I–V、RQ、纳排数）vs (ii) 仅版面 / 图待复核（PDF 排版、行号精确化）。统一标 `not_verified` 是机械降级，会让 A2a 误以为原文证据本身不可信。同时 EV 行未挂具体表号 / 段落 / 行号，例如 Table IV (page 5) / Table V (page 6) / §V.D Limitations (page 7-8)，这些都是 `paper_content.txt` 内可直接定位的锚点。 | I |
| 是否存在可能误导 A2a 的强主张 | **存在结构性误导** | (a) “A1-DT 叶子层口径校准” 段虽承认通用接口的非完整性，但同时给出一棵看似完整的 5 主干 6 叶子树，会让 A2a 把 “精核取值空间是否封闭” 锚到通用接口层，而错过 B1–B6 / P1–P6 等真正应被精核的闭枚举。(b) 把 “evidence_gap” 当成一个候选叶子，掩盖了原文 gap 实际上是 “problem→solution 的缺位” 这种结构性 gap，而不是一类独立编码。(c) `clm-tree-type` 写成 “SMS problem-benefit-solution 树”，方向对，但 “候选主统计池资格…须等 A2a 完成精确页码、表图和字段锚定后再升级” 与上一行 EV 全标 `not_verified` 自我循环，使 A2a 没有可执行的进入条件。 | I |

## 4. 建议维度树骨架

下面给出我认为更忠实于原文的最小骨架。该骨架只覆盖原文已明确给出的字段、表格、统计与编码，不引入原文未出现的字段。

- **根节点**：A Mapping Study on RE in Agile Software Development（28 articles，3 RQs）。
- **主干 1：综述范围与 RQ 显式声明**
  - 叶子 1.1 RQ 集合（取值：{RQ1 research mapping, RQ2 reported benefits, RQ3 reported problems & solutions}，闭枚举，3 项）。
  - 叶子 1.2 单位对象（取值：peer-reviewed article；分母 N=28；可统计：是）。
  - 叶子 1.3 时间窗（取值：检索截止 2014 年 9 月；included articles 出版年 2003–2014）。
- **主干 2：语料收集与纳排数值链条**
  - 叶子 2.1 数据库（取值：Scopus，单库）。
  - 叶子 2.2 检索式（取值：完整 search string，闭值）。
  - 叶子 2.3 纳排数值链（取值：241→187→65→28；可统计：是；缺失值：N/A）。
  - 叶子 2.4 Title/abstract exclusion criteria（5 条闭枚举）。
  - 叶子 2.5 Full-text exclusion criteria（3 条闭枚举）。
- **主干 3：RQ1 研究分布（mapping 三轴）**
  - 叶子 3.1 Venue type（{Conference proceedings, Journal, Magazine}，N=15/8/5，分母 28，可统计：是；证据：Table I, page 3）。
  - 叶子 3.2 Agile method context（{Unspecified agile, Scrum, FDD}，N=20/7/1，分母 28；证据：Table II, page 4）。
  - 叶子 3.3 Article type（7 取值闭枚举：Multiple/Single case study, Experience report, Tool evaluation, Method evaluation, Method proposal, Position paper；分布 N=6/5/3/1/2/8/3；证据：Table III, page 4）。
- **主干 4：RQ2 Benefit 编码（B1–B6 闭枚举）**
  - 叶子 4.1–4.6 每个 Bx 一个叶子；取值：{支撑 article 列表}；分母：N=28；证据：Table IV (page 5) 与 §IV.C。
- **主干 5：RQ3 Problem 编码（P1–P6 闭枚举）+ Solution 映射**
  - 叶子 5.1–5.6 每个 Px 一个叶子，记录支撑 article 列表（来自 Table V, page 6）。
  - 关系边 5.x→solutions：每个 Px 下挂 “是否提出 solution / solution 类型列表”；P3、P4、P6 显式取值 = `no_solution_proposed`（来自 §IV.D 多处显式声明，是原文最关键的 gap 锚点）。
- **主干 6：Synthesis 产物（不是路线图，是原文显式 synthesis）**
  - 叶子 6.1 Proposed definition of agile RE（取值：原文 §V.B 整段定义文本；唯一值；证据：page 7）。
- **主干 7：Discussion / Gap / Future work**
  - 叶子 7.1 Finding（mapping 分布型）：从主干 3 三轴分布形成的观察（F1–F3）。
  - 叶子 7.2 Finding（缺失型 / gap）：P3/P4/P6 = no solution，且 P1/P2 解决方案多源于传统 RE 且未经 empirical evaluation；§VI 明确 future work。
  - 叶子 7.3 Limitations（取值闭枚举：{Scopus single DB, narrow keyword set}；证据：§V.D, page 7-8）。无 explicit quality assessment / threats-to-validity 章节。
- **关系边汇总**：
  - 主干 3 三个叶子 ↔ 主干 7.1（分布型 finding 的直接证据）。
  - 主干 5 ↔ 主干 7.2（problem→solution 缺位 → gap）。
  - 主干 1.1 ↔ 主干 3 / 主干 4 / 主干 5（RQ1↔3，RQ2↔4，RQ3↔5）。

说明：
- 该骨架**不引入**原文没有的字段，例如不假设有 quality rubric、roadmap figure、PICO 字段、theoretical model 节点。
- B1–B6、P1–P6、article-type、venue-type、agile-method-context 五组**闭枚举**取值空间均可在 `paper_content.txt` 中直接验证，A2a 阶段只需做表格-PDF 视觉级对齐与论文 ID [S1]–[S28] 的字面核对，不需要重新发现取值空间。
- 当前 review 不能直接复用本骨架的字段表，必须替换 3 节主干结构与叶子取值空间；如需保留 “跨论文通用接口”，应放到附录而不是当作主干。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干替换：用原文 schema 取代 6 通用接口 | `### 维度树结构` 与 `### 叶子维度表` | 把 b1–b5 改为本报告 §4 提议的主干 1–7；保留 “通用接口对照表” 放入附录而不是主干 | §III–§V 全文 + Tables I–V | C |
| 列出 B1–B6 / P1–P6 闭枚举 | 新增 “RQ2 / RQ3 编码表” 两节 | 显式列出 6 个 Bx code 与 6 个 Px code、其支撑 article 列表与原文中的描述短句；分母 N=28 | Table IV, page 5；Table V, page 6 | C |
| 列出 article-type / venue / method-context 闭枚举 | 新增 “RQ1 分布三轴” 节 | 列出 7 个 article type、3 个 venue type、3 个 method context 及 N 分布 | Tables I/II/III, pages 3–4 | C |
| 显式 problem→solution 关系（含 “no solution”） | 主干 5 与 finding 路径 | 标注 P3 / P4 / P6 = `no_solution_proposed`；P1 / P2 列出 solution 子类；这是 future work 的核心证据链 | §IV.D, pages 5–6；§V.C, page 7；§VI, page 8 | C |
| 新增 “Proposed agile RE definition” 叶子 | 主干 6 | 把 §V.B 的综合定义作为唯一值叶子，标注为 synthesis 产物 | §V.B, page 7 | C |
| 纠正 evidence 等级：区分 text-verified 与 visual-pending | A.2 证据账本 | 把基于 `paper_content.txt` 已稳定还原的 Tables I–V、RQ、纳排数链、B/P 编码、Limitations 升级为 `text_verified`；仅将 PDF 版面 / 行号精确化保留为 `visual_pending`；不再统一 `not_verified` | `paper_content.txt` lines 1–954 | I |
| 在 A.2 挂具体锚点 | EV-001 到 EV-004 | 把 “摘要 / 方法 / 结果 / threats 页” 改为具体 page + section（如 Table IV @ page 5、Table V @ page 6、§V.D @ page 7-8）；行号范围引用 `paper_content.txt` 行号便于回溯 | `paper_content.txt` 全文 | I |
| 拆分 finding 路径 | `leaf-finding` 与 `clm-finding-boundary` | 列出 F1 venue 分布、F2 method-context 71% unspecified、F3 article-type 60% empirical / 29% method proposal、F4 P3/P4/P6 no solution 四条候选 finding 路径，分别标注 “mapping 分布型” 与 “gap 型”，并指明对应分母 | §V.A / §V.C / §VI | I |
| 标注 Limitations 闭枚举 | A.2 EV-004 + 新增 limitations 叶子 | 写明 limitations 仅有两条（Scopus 单库 + 关键词集小）；原文无 quality assessment 与 threats-to-validity 章节，应在树中明确 `not_reported` 而不是空 | §V.D, page 7-8 | I |
| 修正 root 节点：挂 3 个 RQ | `### 根问题 / RQ 到主干分支映射` | 在根节点说明字段中显式列 RQ1 / RQ2 / RQ3 三句，并与主干 3 / 4 / 5 做一对一映射；当前根节点说明无 RQ 显式条目 | §I, page 1 | I |
| 通用接口降级为附录 | 末尾新增附录 | 把当前 6 个 `leaf-*` 通用接口（scope/corpus/taxonomy/method/evidence/finding）放入 “通用接口 ↔ 原文叶子对照表”，避免被读成主干 | `patterns/pattern-field-schema.md` | M |
| 词句口径：清理 “roadmap action point” 表述 | `leaf-method`、`leaf-finding`、EV-002 | 本文不是 roadmap / proposal paper，不要写 “roadmap branch / roadmap action point”；改为 “solution sub-theme” 或 “future work statement” | §IV.D, §VI | M |
| 词句口径：去 “LLM / agent 角色” | `leaf-method` 取值空间 | 该论文无 LLM / agent 内容，该取值描述会让 A2a 误以为存在 agent / LLM 维度 | §III–§VI 全文均无 LLM/agent | M |

## 6. C/I/M 结论

- **C（critical）**：5 处。集中在主干替换、B1–B6/P1–P6 闭枚举、article-type/venue/method-context 三轴、problem→solution 关系（含 no_solution）、agile RE 定义 synthesis。这 5 处都直接破坏 Paper2 维度树复原的学术目标：当前树把原文最稳定、最可统计的闭枚举丢进通用接口层，导致 A2a 无法基于本树对原文做字段级核验，也会让 SUMMARY 阶段“是否支持 mapping 分布统计”这一关键问题失去证据基础。
- **I（important）**：6 处。集中在证据等级机械降级、A.2 锚点不足、finding 路径未拆、limitations 闭枚举缺失、根节点未挂 RQ、统计分母口径混淆。这些不会立即破坏树的存在性，但会显著降低维度树证据链的可审计性与 A2a 操作性，影响 Paper2 后续从本篇推导 schema 模式的可靠性。
- **M（minor）**：3 处。通用接口降级为附录、`roadmap` 与 `LLM/agent` 等不当词句的清理。仅影响清晰度与维护性，不阻塞合并主线。

**最终建议：NEEDS FIX。**

理由（对 Paper2 学术目标的影响，按 CLAUDE.md §学术研究仓库 Review 口径执行）：当前 `review.md` 把 6 个跨论文通用接口当主干主结构，把原文最稳定的 5 组闭枚举（B1–B6、P1–P6、article-type、venue、method-context）与最关键的结构性 gap（problem→solution 缺位）以及 §V.B synthesis 定义全部模糊化或丢失；并通过把所有证据统一标记为 `not_verified` 进一步阻断了对本来在 `paper_content.txt` 中可直接核验事实的引用路径。对 Paper2 而言，本篇是“典型小规模 SMS、显式 problem-benefit-solution 编码、显式 gap 输出”的样本——这正是 A2a 与 SUMMARY 必须依赖的 schema 锚点；如果不在本 PR 修复，后续 A2a 将无法用本篇验证 mapping study 编码 schema 的可迁移性，也会让 Paper2 “mapping study 维度树呈现 problem-benefit-solution 三轴 + 显式 no-solution gap” 这一可推广结论失去单篇证据支撑。建议在合并前至少修复全部 C 级与至少 4 项 I 级（证据等级、A.2 锚点、finding 路径、limitations 闭枚举）。
