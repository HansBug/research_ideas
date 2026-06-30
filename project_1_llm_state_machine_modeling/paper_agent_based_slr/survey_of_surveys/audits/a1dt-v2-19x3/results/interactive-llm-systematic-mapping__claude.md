`★ Insight ─────────────────────────────────────`
- 这篇论文是 solution proposal，没有样本编码 schema，只有"流程阶段 × 人机角色 × agent 角色"的方法学骨架，因此原生维度树本质上是**方法流程森林**，而不是一棵 SLR 数据抽取树。
- 现有 `review.md` 已经在"原文 schema 主树（19×3 审计后返修）"中显式区分了六个通用接口叶子（跨论文投影）与原文主干（process/agent/loop/coding/trace/risk），方向正确，但叶子级别仍停留在 `schema_seed`，缺少 Fig.1 内"input ↔ refinement ↔ output"三元组的精确字段化。
- 关键风险：把"Relevant literature 段引用的 10 篇文献"误读为该文样本是错的——它们是叙事性引用，不是 coded sample；分母是 0。
`─────────────────────────────────────────────────`

下面是完整审计报告正文。

---

# A1-DT v2 单篇审计报告：`interactive-llm-systematic-mapping`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `interactive-llm-systematic-mapping` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；4 页全文 281 行均通读 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；二者交叉核对，年份字段已对齐：BibTeX `year=2025` ↔ `metadata.json publication_date=2024-11-01`，Page 1 脚注 "Available online 31 October 2024" 与之一致 |
| 是否打开或核对 `paper.pdf` | 否；本轮未用 Read 打开 PDF；Fig. 1 的文字描述只能依赖 `paper_content.txt` 第 79 行的 caption "The mapping process with LLM support."；列为待人工版面核验 |
| 原文类型 | solution proposal（作者自述："The research can be classified as a solution proposal"，Page 1 §Method）；既不是 SLR、也不是 SMS、tertiary、MLR；可被视为 vision / roadmap |
| 被编码样本单位 | **无系统样本库**。原文样本单位是"假想 LLM-supported mapping 工作流中的流程阶段 / agent 角色 / 人机交互节点"，不是 primary study |
| 样本数量 / 分母 | `not_applicable`。论文 References 仅 10 条，全部以叙事 "Relevant literature" 形式被引，不构成 coded sample；`Data availability: No data was used`（Page 3） |
| 原生树类型 | **维度森林（降级）**：①方法流程树（6 阶段） + ②agent/role 树（含 search 阶段 3 agent + 各阶段 LLM/人 双轨） + ③validity/risk 树（Reflections）。无样本编码 schema |
| 主统计池资格 | 否。理由：solution proposal；无系统检索、纳排、抽取；与 `metadata.json eligible_for_statistical_synthesis=false`、`evidence_role=solution_proposal_boundary_anchor` 一致。**局部仅可作 schema_seed / boundary_anchor / methodological seed** |
| 总体判定 | **needs repair**（minor + a few important）：方向正确，但叶子层仍是占位，建议按下文 §7 做 I 级返修；不阻塞合并 |

## 1. 原文证据阅读说明

**实际读取的本地文件**（按本次会话顺序）：

1. `bibtex.bib`（13 行，已读全文）
2. `metadata.json`（35 行，已读全文）
3. `review.md`（437 行，已读全文，作为返修基线）
4. `paper_content.txt`（281 行，已读全文，覆盖 Page 1 摘要+引言、Page 2 §2、Page 3 §2.4-§3 Reflections+Data availability、Page 4 References）

**未读但应核验**：`paper.pdf` 本轮未通过 Read 工具打开。Fig. 1 的视觉结构只通过文本提取中的 caption "The mapping process with LLM support." 推定；图中每个阶段下方的"researcher input + interactive refinement / LLM output"二/三栏布局，仅通过 §2 各小节自述行文重构，**未做版面核验**。这是本审计第一位的 blocked 风险，A2a 必须打开 PDF 核对。

**5–12 个最关键原文证据锚点**（行号引用 `paper_content.txt`）：

1. **Page 1 摘要 / Method 自述**：`"The research can be classified as a solution proposal. The solution was iteratively designed and discussed among the authors..."`（行 18–19）→ 决定了"非实证、无样本"。
2. **Page 1 Introduction §动机四点**：`"(1) An increased number of published papers... (2) Conducting mapping studies on a larger scope; (3) Getting additional research design ideas by interacting with the LLM; (4) Reduced effort allows updating mapping studies more regularly."`（行 35–39）。
3. **Page 1 human-in-the-loop 前提**：`"reviewers (a) are well educated in using the mapping study method, and (b) be experts in the topic they are reviewing."`（行 53–55）→ HITL 是硬约束。
4. **Page 2 Fig. 1 caption**：`"Fig. 1. The mapping process with LLM support."`（行 79）→ 图是流程图，不是分类表。
5. **Page 2 §2.2.1 三 agent 列举**：`"Keyword Identification Agent... Semantic Search Agent... Search Strategy Agent..."`（行 101–120）→ search 阶段的 3-agent 子树。
6. **Page 2 §2.2.1 Relevant literature - Wang et al. [5]**：`"GPT-generated queries result in less recall... (1) The use of PICO harms recall; (2) ... (3) requesting refinements reduces recall and improves precision."`（行 131–135）→ 这是被引文献的 finding，不是本文 finding。
7. **Page 3 §2.2.2 纳排 schema 雏形**：`"language models have to explain the reasons for inclusion and exclusion. Chain-of-thoughts prompting... citations are indispensable. They allow the verification of arguments and increase traceability."`（行 153–157）→ 纳排输出字段：decision + rationale + citation。
8. **Page 3 §2.3 编码二分**：`"1. Inductive coding... topic modeling... embeddings, reduce dimensions, cluster embeddings, and create topic representations... Bertopic ... 2. Deductive coding: Given is a data extraction scheme (e.g., SWE-BOK categories)... One-shot or Few-shot... RAG architecture..."`（行 177–191）→ extraction 子树二分。
9. **Page 3 §3 Reflections - validity 四点**：`"Publication bias and limited studies... The rapid evolution of LLMs... Many existing studies are from outside SE..."`（行 213–223）→ validity/risk 树叶子。
10. **Page 3 §3 two research directions**：`"Improving individual steps... Build a prototype representing the overall mapping process..."`（行 231–234）→ roadmap 两条。
11. **Page 3 Data availability**：`"No data was used for the research described in the article."`（行 246）→ 强证据：无样本分母。
12. **Page 4 References**：10 条参考文献（行 252–280）；其中 [4] = Petersen et al. 2015 SMS guidelines，是本文流程阶段的真正母本，等价于"借用现成 stage taxonomy"，不是本文新构建。

## 2. 样本单位与字段来源判定

**Q1: 原文纳入和逐项描述的对象是什么？**

原文不"纳入"任何 primary study。它"逐项描述"的对象是 **Petersen 等 2015 SMS guideline 提出的 5–6 个流程阶段**（need → search → inclusion/exclusion → data extraction & classification → visualization → reporting），在每个阶段下逐项描述：（a）人类研究者输入；（b）LLM 输出；（c）拟用的技术机制（RAG、BERTopic、CoT prompting 等）；（d）相关已有文献的旁证。这些"阶段"是单位对象，但它们不是 sample，而是 design slot。

**Q2: 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**

没有。`Data availability: No data was used`（行 246）。Method 自述为 "iteratively designed and discussed among the authors based on their experience"（行 18–19）。10 条参考文献以叙事方式被引，不是检索结果。

**Q3: 原文字段来自哪里？**

字段来源是 **作者基于 SMS guideline [4] 构造的 process model + 三 agent 架构 + HITL pattern + LLM 技术 menu**，不是 extraction form / classification schema / taxonomy / quality rubric / replication package。可视为 **conceptual blueprint**，对应 v2 口径下的 "methodological seed / boundary anchor"。

**Q4: RQ 与样本单位是什么关系？**

原文无显式 RQ 表。Objective 是 "discuss possibilities and next steps for using LLMs (e.g., GPT-4) in the mapping study process"（行 17）。它把"流程阶段"既当作 RQ 划分锚点（每个阶段一个 §），又当作贡献组织方式（每段都是一组 design claims + relevant literature）。即：**stage = RQ 容器 = 字段容器 = 贡献容器**，三位一体。

**Q5: 若无系统样本库，如何降级？**

按 v2 口径降级为：

- **不进入主统计池**（与 `metadata.json eligible_for_statistical_synthesis=false` 一致）
- **作 boundary anchor**：界定"interactive LLM-based SMS"的概念已在 2024/2025 被显式提出，Paper2 不能宣称首创
- **作 methodological seed**：为 Paper2 的 scaffold 提供候选 stage taxonomy 与 HITL/agent 字段模板
- **作 risk inventory seed**：Reflections 中的 publication bias / model drift / SE-specificity / 非 SE 证据外推 是 Paper2 风险章直接可用清单

## 3. 原生样本编码维度树 / 维度森林

**重要说明**：本树**不是样本编码 schema**，而是该论文用来组织"LLM-supported SMS 流程设计"的概念骨架。这是降级形态。

```text
[ROOT] interactive LLM-based SMS process model (Fig. 1 + §2)
│   tree_type: conceptual_blueprint / process_model
│   sample_unit: process_stage (NOT primary study)
│   sample_n: not_applicable
│
├── [B1] Process stage taxonomy（借自 SMS guideline [4]）
│   ├── [S1] Establishing a need for the map (§2.1)
│   ├── [S2] Study identification
│   │   ├── [S2a] Search (§2.2.1)
│   │   └── [S2b] Inclusion / exclusion (§2.2.2)
│   ├── [S3] Data extraction and classification (§2.3)
│   │   ├── [S3a] Inductive coding
│   │   └── [S3b] Deductive coding
│   ├── [S4] Visualization (§2.4)
│   └── [S5] Reporting (§2.5)
│
├── [B2] Per-stage triplet（Fig. 1 通用结构）
│   ├── [L-input] researcher_input（每阶段都有）
│   ├── [L-refine] interactive_refinement / human override
│   └── [L-output] LLM_output（每阶段都有）
│
├── [B3] Agent roles (S2a search 阶段专有 3-agent 架构)
│   ├── [A1] Keyword Identification Agent
│   ├── [A2] Semantic Search Agent (RAG + graph DB)
│   └── [A3] Search Strategy Agent
│
├── [B4] Technical mechanism menu（各阶段可调用的技术组件）
│   ├── topic_modeling / BERTopic (S3a)
│   ├── one_shot / few_shot / CoT prompting (S2b / S3b)
│   ├── RAG + document splitting (S3b)
│   ├── continual_learning / DSPy (S2b)
│   ├── tracing tools / LangSmith (§3)
│   ├── WebVoyager (grey literature, §3)
│   └── visualization tools / LIDA, ChatGPT code (S4)
│
├── [B5] Audit / traceability requirement set (§2.2.2 + §2.3)
│   ├── decision_label (include/exclude/uncertain)
│   ├── rationale / explanation
│   ├── cited_fragments / citations
│   └── source_location
│
├── [B6] Validity / threat（§3 Reflections）
│   ├── publication_bias
│   ├── limited_studies_on_LLM_reliability
│   ├── rapid_model_evolution / provider_drift (Claude.ai, GPT-o1)
│   ├── non_SE_evidence_transfer_risk
│   └── SE_specific_evaluation_needed
│
└── [B7] Research roadmap (§3 末尾)
    ├── [R1] Improve & evaluate individual steps
    └── [R2] Build end-to-end prototype
```

**取值空间类型说明**：

- B1 stage taxonomy：**层级枚举**（5 大阶段 + 2 子阶段），但是借自 [4]，非本文饱和分类。
- B2 triplet：**关系值（field role）**，input/refine/output 是固定三槽。
- B3 agents：**有限枚举**（恰好 3），仅限 search 阶段。
- B4 mechanisms：**开放枚举**，作者只是示例性列举工具名，不是封闭集。
- B5 audit fields：**关系值集合**（decision + 4 个挂件字段），是 Paper2 最有迁移价值的部分。
- B6 threats：**开放枚举**，作者列了 4–5 项，是 risk inventory seed。
- B7 roadmap：**二值 / 有限枚举**（个体优化 vs 整体原型）。

**未完成 / 需 A2a 精核**：

- Fig. 1 实际包含多少 stage box、每个 box 的 input/output 文字是否与 §2 完全一致——必须开 PDF 核对。
- §2.4 / §2.5 较短，是否在 Fig. 1 中也有完整 triplet 槽，文本无法独自确认。
- Supplementary material（DOI 链接下）给出被下划线术语的定义——本轮未打开，叶子语义可能因此残缺。

## 4. 叶子维度表

下表只列**原文确实出现且可作为字段候选**的叶子，不混入跨论文通用接口。证据列直接给 `paper_content.txt` 行号。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| stage.need | 阶段：建立 map 需求 | B1 | §2.1 | 把研究目标 + 上下文输入给 LLM 得到候选 RQ，由人确认 | 1 个 stage | 单值标识 | 阶段缺失 = roadmap 不完整 | 仅 schema_seed | 阶段缺失为 gap | 行 81–84 | 可作 stage 模板，不能写成已验证流程 |
| stage.search | 阶段：检索 | B1 | §2.2.1 | 在保持可复现性前提下生成 Boolean 检索式 | 1 个 stage（内含 3 agent） | 单值 + 子树 | 同上 | 同上 | 同上 | 行 86–122 | 同上 |
| stage.inc_exc | 阶段：纳排 | B1 | §2.2.2 | LLM 给 include/exclude + rationale + citation | 1 个 stage | 单值 | 同上 | 同上 | 同上 | 行 136–170 | 同上 |
| stage.extract | 阶段：数据抽取与分类 | B1 | §2.3 | 二分为归纳/演绎编码 | 1 个 stage（内含 2 子模式） | 单值 + 子枚举 | 同上 | 同上 | 同上 | 行 171–199 | 同上 |
| stage.vis | 阶段：可视化 | B1 | §2.4 | LLM 生成绘图代码 / 拓扑可视化 | 1 个 stage | 单值 | 同上 | 同上 | 同上 | 行 200–206 | 同上 |
| stage.report | 阶段：报告 | B1 | §2.5 | LLM 在数据表/可视化基础上提示模式与 gap | 1 个 stage | 单值 | 同上 | 同上 | 同上 | 行 207–211 | 同上 |
| triplet.input | 字段角色：researcher input | B2 | Fig. 1 + §2 各小节首句 | 用户提供给 LLM 的对象（目标/abstracts/scheme/数据表/RQ） | 自由文本，每阶段类型不同 | 关系值（角色槽） | 缺失 = 自动化越界 | 用于 HITL gate 描述 | 可生成 "哪些阶段 input 最易自动化越界" 的候选发现 | 行 79–211 各 § 首句 | **该结构是本文最强迁移点** |
| triplet.refine | 字段角色：interactive refinement | B2 | Fig. 1 + §2 各小节"We edit ... as input for the next stage"等表述 | 用户对 LLM 输出的编辑、覆盖、追问、确认 | 自由文本 | 关系值 | 缺失 = 退化为全自动 | 同上 | 同上 | 行 83–84 等 | 同上 |
| triplet.output | 字段角色：LLM output | B2 | Fig. 1 + §2 各小节"the LLM proposes/suggests/generates ..." | LLM 在该阶段的产物（RQ 候选、agent 建议、include/exclude、topic 表、图、报告 highlights） | 自由文本，每阶段类型不同 | 关系值 | 缺失 = LLM 未介入该阶段 | 同上 | 同上 | 行 82–211 | 同上 |
| agent.keyword | Search-Agent：关键词识别 | B3 | §2.2.1 item 1 | 识别相关术语、同义词、历史术语、概念层级 | 1 个有限 agent slot | 单值 | -- | 同上 | -- | 行 101–110 | 仅限 search 阶段 |
| agent.semantic | Search-Agent：语义检索 | B3 | §2.2.1 item 2 | RAG + 可选 graph DB；调整检索策略，不直接选文献 | 1 slot | 单值 | -- | 同上 | -- | 行 111–118 | 同上 |
| agent.strategy | Search-Agent：检索策略 | B3 | §2.2.1 item 3 | 输出最终可执行 Boolean / DB-specific 查询 | 1 slot | 单值 | -- | 同上 | -- | 行 119–120 | 同上 |
| mech.bertopic | 技术机制：topic modeling | B4 | §2.3 item 1, §2.4 | embeddings → 降维 → 聚类 → topic 表示 | 工具列：BERTopic | 开放枚举 | -- | -- | -- | 行 178–184, 205–206 | 工具名易过时 |
| mech.prompt_style | 技术机制：prompt 形式 | B4 | §2.2.2 + §2.3 item 2 | zero/one/few-shot / CoT / DSPy 优化 | 开放枚举 | 开放枚举 | -- | -- | -- | 行 154, 158–166, 187–188 | 不要绑定具体 prompt 写法 |
| mech.rag | 技术机制：RAG + 文档切分 | B4 | §2.2.1 + §2.3 item 2 | 先 RAG 定位再 prompt LLM | bool / 配置 | 布尔 + 配置自由文本 | -- | -- | -- | 行 111–117, 188–191 | 同上 |
| mech.continual | 技术机制：持续学习 / DSPy | B4 | §2.2.2 | 从 inc/exc 偏好迭代学习 | bool + 工具名 | 布尔 + 工具引用 | -- | -- | -- | 行 144–149 | 工具名易过时 |
| mech.trace_tool | 技术机制：tracing 工具 | B4 | §3 Complementary Tools | LangSmith 类工具 | 工具列 | 开放枚举 | -- | -- | -- | 行 224–226 | 同上 |
| mech.web | 技术机制：web agent | B4 | §3 | WebVoyager 用于灰文献 | 工具列 | 开放枚举 | -- | -- | -- | 行 226–229 | 工具名易过时 |
| audit.decision | 审计字段：决策标签 | B5 | §2.2.2 | include / exclude / borderline | 三值枚举 | 有限枚举 | 缺失即不可审 | 用于 trace 覆盖率 seed | 可作 gap：哪个阶段 trace 最缺 | 行 150–157 | **强迁移点** |
| audit.rationale | 审计字段：理由 | B5 | §2.2.2 | LLM 给出的解释 / CoT | 自由文本 | 自由文本 | 同上 | 同上 | 同上 | 行 153–155 | CoT 不等于必须暴露推理链，应解读为可审计 rationale |
| audit.citation | 审计字段：引用 | B5 | §2.2.2 | 文本证据片段 + 原文位置 | 关系值（fragment + locator） | 关系值 | 同上 | 同上 | 同上 | 行 155–157 | 强迁移点 |
| audit.source_loc | 审计字段：来源位置 | B5 | §2.2.2 隐含 | 引用所指原文 page / paragraph / line | 关系值 | 关系值 | 同上 | 同上 | 同上 | 行 156–157 | 同上 |
| threat.pub_bias | 风险：publication bias | B6 | §3 | 现有 LLM-for-review 研究有限且可能有发表偏差 | 风险条目 | 布尔 + 描述 | -- | 用于 risk inventory | risk 候选 | 行 213–217 | 直接迁移 |
| threat.model_drift | 风险：模型快速演化 | B6 | §3 | Claude.ai、GPT-o1 等会让评估过时 | 风险条目 | 同上 | -- | 同上 | 同上 | 行 215–217 | 等价 Paper2 provider drift |
| threat.non_se | 风险：证据外 SE 化 | B6 | §3 | 很多证据来自 SE 之外 | 风险条目 | 同上 | -- | 同上 | 同上 | 行 218–221 | 直接迁移 |
| threat.se_specific | 风险：缺 SE-specific evaluation | B6 | §3 | 需要 SE-specific solution & evaluation | 风险条目 | 同上 | -- | 同上 | 同上 | 行 219–222 | 直接迁移 |
| roadmap.steps | 路线图条 R1：单步评估 | B7 | §3 末尾 | 分别评估每个 stage 的策略 | 1 path | 二值 | -- | 候选 next-step | candidate roadmap | 行 231–232 | 直接迁移 |
| roadmap.proto | 路线图条 R2：端到端 prototype | B7 | §3 末尾 | 构建覆盖全流程 prototype 收集反馈 | 1 path | 二值 | -- | 同上 | 同上 | 行 232–234 | 直接迁移 |

## 5. 关系边表

原文虽然不是 ER schema，但 Fig. 1 + §2 + §2.2.1 / §2.3 存在若干 **显式关系边**，列举如下：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel.stage_to_triplet | stage.* | each-has-a | triplet.{input, refine, output} | 角色槽固定 3 个 | 槽缺失 = 该阶段未被建模 | Fig. 1 全图；行 79；行 81–211 各阶段首句 | Paper2 scaffold 字段模板 |
| rel.stage_seq | stage.need | feeds_into | stage.search → stage.inc_exc → stage.extract → stage.vis → stage.report | 有序链 | 顺序断裂 = 流程不完整 | 行 64–71 §2 开篇；§2.1 末尾 "as input for the next stage" 行 83 | scaffold stage order |
| rel.search_to_agent | stage.search | composed_of | agent.{keyword, semantic, strategy} | 3 agent | agent 缺失 = 搜索代理化不完整 | 行 99–122 | 唯一显式 3-agent 子树 |
| rel.agent_pipe_kw_to_sem | agent.keyword | provides_terms_to | agent.semantic | 关系值 | -- | 行 117–118 "Relevant search terms are then extracted again from the selected documents" | citation pearl growing pipeline |
| rel.agent_pair_pearl | agent.{keyword, semantic} | jointly_support | citation_pearl_growing 策略 | 关系值 | -- | 行 121–122 | 把 pearl growing 作为复合产出 |
| rel.extract_branch | stage.extract | branches_into | {inductive_coding, deductive_coding} | 二分 | -- | 行 177–191 | extraction 子模式 |
| rel.inc_exc_to_audit | triplet.output (at stage.inc_exc) | must_carry | audit.{decision, rationale, citation, source_loc} | 关系值集合 | 缺失 = 不可审 | 行 150–157 | **trace 强约束**，是 Paper2 最可执行的 schema |
| rel.fulltext_unlock | automation_level | unlocks | fulltext_as_extract_input | 布尔 | -- | 行 173–176 "go beyond adaptive reading depth ... consider the complete papers as input" | 解读为"自动化越高，输入可越深" |
| rel.threat_to_evaluation | threat.{model_drift, non_se, se_specific} | motivates | roadmap.steps & roadmap.proto | 关系值 | -- | 行 213–234 | 风险驱动 roadmap |

**总结**：原文存在 **流程顺序、agent 内部 pipeline、纳排→审计字段挂件、风险→roadmap** 四类显式关系边。它不是 ER schema，但已经足够支撑 Paper2 scaffold 的字段映射，**比"无显式关系边"要强**。

## 6. 统计观察、候选 finding 与 final finding 边界

| 类别 | 内容 | 证据 |
|---|---|---|
| **原文自身统计观察** | 无。论文没有任何数字、表格、图表数据点。Fig. 1 是流程图。 | 行 246 Data availability |
| **被引文献统计观察（不是本文 finding）** | (a) Wang et al. [5]：GPT 生成的 Boolean query 召回更低；PICO 损害召回；refinement 降召回升精度（行 130–135）；(b) Huotala et al. [6]：one-shot / few-shot / few-shot CoT 与人类性能接近；zero-shot 较差；GPT-4 优于 GPT-3.5（行 159–166）；(c) Guo et al. [7]：GPT 善于排除无关，但召回不高（行 167–170）；(d) Petersen [9]：GPT-4 判断 case study 时优于作者（行 197–199） | 行 123–135、158–170、192–199 |
| **原文 discussion / roadmap 候选 finding** | (i) HITL 是 LLM-supported SMS 必要前提；(ii) 可复现性需要保留 Boolean search；(iii) inc/exc 必须挂 rationale + citation；(iv) 自动化提升后可用完整 PDF 做 deductive coding；(v) 模型快速演化导致评估易过时；(vi) 需要 SE-specific evaluation；(vii) roadmap 双轨：先单步评估再端到端 prototype | 全文综合，主要行 52–55、92–96、150–157、173–176、213–234 |
| **对 Paper2 可迁移的方法学启发** | （a）stage × triplet × audit 三层 schema 模板；（b）三 agent search 是可重用模式；（c）provider drift / non-SE transfer / SE-specific evaluation 作为 risk inventory；（d）roadmap 双轨叙事可借用 | 行 79, 99–122, 213–234 |
| **绝不能迁移的领域结论** | 1. 不可写"已被验证的 LLM-supported SMS 解决方案"；2. 不可写"GPT 在文献综述中可靠"；3. 不可写"首创 interactive LLM-based SMS"（本文 2024/2025 已显式提出该方向）；4. 不可把被引文献 [5–9] 的数字当作本文 finding；5. 不可写本文符合 PRISMA / 提供 replication package | 行 18–19、行 213–234、行 246 |

## 7. 对现有 `review.md` 的返修建议

总体方向：**现有 review.md 在结构上已经识别出"通用六叶 = 投影"vs"原文 schema 主树 = 事实源"，但叶子还停留在占位描述，应该把上面 §3–5 的具体字段、关系边、取值空间种子写进去。**

**Critical (C)**：无 C 级问题。该 review.md 没有把六叶通用接口冒充原文叶子全集（在 line 283 已显式说明），也没有把被引文献数字当作本文 finding，也没有违反主统计池排除规则。

**Important (I)**：

- **I-1**：line 297–306 的"维度树结构"过于压缩，把"研究范围 / 语料链条 / 主题分类 / 方法分类 / 评价 / 候选发现"这 6 个通用接口直接挂在 5 个原文主干下，看起来仍像把通用接口当主结构。**建议把这 6 个 leaf 整体折叠到一个单独的"通用接口投影"小节（事实上 line 360–371 已经有这个表），同时在主"维度树结构"代码块里改用本审计 §3 给出的 B1–B7 + 子节点。**
- **I-2**：line 338–346 的"原文 schema 主树（19×3 审计后返修）"只给了 6 行主干名，没有给"叶子 / 取值空间种子"具体词。**建议把本审计 §4 表（28 行）中至少 stage.*、triplet.*、agent.* 与 audit.* 四类合并进该表，作为 A2a 精核入口的具体清单。**
- **I-3**：line 411 EV-004 缺少"被引文献 ≠ 本文样本"的显式分隔。**建议在 A.2 增加一条 EV-005：来源 = `paper_content.txt` 行 123–199 + 行 246，证据角色 = `cited_literature_anecdote`，证据强度 = `weak`，迁移边界 = "不得把 [5]–[9] 的数字写成本文 finding"。** 这是本论文最易被误用的位置。
- **I-4**：关系边维度（本审计 §5）在现行 review.md 里**完全缺失**——line 298–306 的 b1–b5 主干没有任何"input→output→audit"或"keyword→semantic→strategy"的关系边描述。建议新增一节"原文显式关系边"，用本审计 §5 表的 9 条边作为种子。

**Minor (M)**：

- M-1：line 16 "已读全文文本-paper_content核验" 写法略生硬，可改为"全文文本核验"。
- M-2：line 41 "Fig. 1 已回原文核对" 与本轮审计冲突（本审计未开 PDF）；如果原 review 写作时确实开过 PDF，则保留并加上日期戳；否则建议改为 "Fig. 1 caption 已通过 paper_content.txt 第 79 行核验；版面待 A2a 复核"。
- M-3：line 271 CCF 复核状态 "WAF" 与 line 13 完全重复，可只在卡片保留一处。
- M-4：line 156 dimension pattern 行写得很好（"流程树、search 3 agent、extraction 二分"），可以直接抽出来作为 §3 主结构的镜像描述，避免上下两段冗余。

**对 SUMMARY 总账的修正建议**：

- "样本单位 / 样本数量 / 原生树类型 / 统计池资格"四列应分别为：`process_stage / not_applicable / forest (process + agent + risk) / NOT_in_main_pool, boundary_anchor only`。如果 SUMMARY 当前写的是"single tree / 6 leaves / yes-partial"则需要纠正。

## 8. 审计附录草案：证据账本与结论映射

可直接迁回 `review.md` A.2 / A.3。

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-iLLM-SMS-001 | paper_content.txt | Page 1 Abstract Method | 行 18–19 | "research can be classified as a solution proposal ... iteratively designed and discussed among the authors" | tree_type / non-empirical 自述 | strong (作者自述) | ROOT, B1–B7, 主统计池排除 | 否 | 仅支撑"非实证 + 无样本"判定 |
| EV-iLLM-SMS-002 | paper_content.txt | Page 1 Intro 末段 | 行 52–55 | "reviewers (a) well educated in mapping study method, (b) experts in topic" | HITL 必要条件 | strong | B2 triplet.refine, B5 audit.* | 否 | HITL 是硬约束，不可省 |
| EV-iLLM-SMS-003 | paper_content.txt | Page 2 §2 + Fig. 1 caption | 行 64–79 | "presents each step of the review process and briefly outlines the input and actions done by the user and the output of the LLM" | stage × triplet 结构 | medium (文本+图未版面核验) | B1, B2, rel.stage_to_triplet | **是**（必须打开 PDF 核 Fig. 1） | Fig. 1 内部细节待版面确认 |
| EV-iLLM-SMS-004 | paper_content.txt | Page 2 §2.2.1 | 行 99–122 | "three agents: Keyword Identification Agent, Semantic Search Agent, Search Strategy Agent ... support a citation pearl growing strategy" | search 3-agent 子树 + agent 间 pipeline | strong | B3, rel.search_to_agent, rel.agent_pipe_kw_to_sem, rel.agent_pair_pearl | 否 | 仅限 search 阶段；不要扩到其他阶段 |
| EV-iLLM-SMS-005 | paper_content.txt | Page 3 §2.2.2 | 行 150–157 | "language models have to explain the reasons ... Chain-of-thoughts prompting ... citations are indispensable ... increase traceability" | 纳排 audit 字段强约束 | strong | B5 audit.*, rel.inc_exc_to_audit | 否 | CoT 不等于必须暴露推理链；解读为可审计 rationale |
| EV-iLLM-SMS-006 | paper_content.txt | Page 3 §2.3 | 行 177–191 | "Inductive coding ... topic modeling ... Bertopic. Deductive coding: Given is a data extraction scheme (e.g., SWE-BOK) ... One-shot or Few-shot ... RAG architecture" | extraction 二分 + 机制菜单 | strong | stage.extract, mech.bertopic, mech.prompt_style, mech.rag | 否 | SWE-BOK 仅作为示例，不要写成 scheme 本身 |
| EV-iLLM-SMS-007 | paper_content.txt | Page 3 §3 Reflections | 行 213–223 | "Publication bias and limited studies ... rapid evolution of LLMs ... Many existing studies are from outside SE" | validity / threat 树 | strong | B6 threat.*, threat→roadmap 关系 | 否 | 等价 Paper2 provider drift / 非 SE 证据外推 |
| EV-iLLM-SMS-008 | paper_content.txt | Page 3 §3 末尾 | 行 231–234 | "Improving individual steps ... Build a prototype representing the overall mapping process" | roadmap 双轨 | strong | B7 roadmap.* | 否 | 直接迁移 |
| EV-iLLM-SMS-009 | paper_content.txt | Page 3 Data availability | 行 246 | "No data was used for the research described in the article." | 强证据：无样本分母 | strong | 主统计池排除 | 否 | 决定性 |
| EV-iLLM-SMS-010 | paper_content.txt | Page 2–3 各 "Relevant literature" 段 | 行 123–135, 158–170, 192–199 | Wang [5], Huotala [6], Guo [7], Petersen [9] 的数字与陈述 | **被引文献的 finding**（不是本文 finding） | weak（叙事性引用） | 风险注脚 | 否 | **关键迁移红线**：不得写成本文结论 |
| EV-iLLM-SMS-011 | paper.pdf | Page 2 Fig. 1 版面 | -- | -- | 图内 box / 箭头 / 标签精确文字 | not_verified | rel.stage_to_triplet, B2 三槽是否每阶段都齐 | **是** | A2a 必须打开 PDF |
| EV-iLLM-SMS-012 | Supplementary material (online) | Appendix A | -- | 被下划线术语定义 | not_verified | mech.* 工具语义 | **是** | 本轮未打开 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-iLLM-SMS-T01 | 本文树型 = process model + agent role tree + risk inventory 组成的森林；样本单位 = process_stage；样本数 = not_applicable；不进入主统计池，仅作 boundary anchor / methodological seed | tree_type | ROOT | EV-001, EV-009 | strong | boundary_anchor, schema_seed | 仅限本文；不能外推到所有 LLM-for-SMS 研究 |
| C-iLLM-SMS-T02 | 流程阶段链 need→search→inc/exc→extract→vis→report 借自 [4] 2015 SMS guideline，本文未饱和验证 | stage_taxonomy | B1 | EV-003 | medium | scaffold candidate | 借用结构，不是本文贡献新 taxonomy |
| C-iLLM-SMS-T03 | Fig. 1 的 "researcher input × interactive refinement × LLM output" 三槽是本文对 Paper2 最强迁移点 | structural_pattern | B2, rel.stage_to_triplet | EV-003 | medium (待版面核) | scaffold 字段模板 | Fig. 1 版面待 A2a 核 |
| C-iLLM-SMS-T04 | Search 阶段三 agent 是唯一显式 agent 子树；不要把它推广到其他阶段 | sub_schema | B3 | EV-004 | strong | agent role 模板 | 仅限 search |
| C-iLLM-SMS-T05 | 纳排阶段 LLM 输出必须挂 decision + rationale + citation + source_location 四件套，否则不可审计 | audit_constraint | B5, rel.inc_exc_to_audit | EV-005 | strong | Paper2 trace schema 直接落点 | CoT 不等于暴露推理链 |
| C-iLLM-SMS-T06 | 风险清单 {pub_bias, model_drift, non_se_transfer, se_specific_eval_needed} 可直接作为 Paper2 risk inventory seed | risk_inventory | B6 | EV-007 | strong | Paper2 §限制 / §风险章 | 原文未量化任何风险 |
| C-iLLM-SMS-T07 | Roadmap 双轨（单步评估 / 端到端 prototype）可作为 Paper2 方法学叙事模板 | roadmap_pattern | B7 | EV-008 | medium | story / method 叙事 | 仅作叙事模板，非已验证路径 |
| C-iLLM-SMS-T08 | §2 各 "Relevant literature" 段引用的数字与陈述属于 [5]–[9] 等文献，不属于本文 finding；引用本文时不得把这些数字写成本文结论 | citation_boundary | B6, EV-010 | EV-010 | strong | 引用红线 | 强制约束 |
| C-iLLM-SMS-T09 | "interactive LLM-based SMS" 这一方向已在 2024/2025 由本文显式提出；Paper2 不得宣称首创，但可补全 evaluation / prototype | priority_boundary | ROOT | EV-001, EV-008 | strong | Paper2 §related work 必须 cite | -- |

## 9. 技能使用与自我审查记录

**已读取并采用的技能 / 指南文件**：

1. `~/.codex/skills/ai-research-writing-skill/SKILL.md` — 采用其"claim-evidence-engineering workflow"原则、"Evidence gate"、"Citation gate"。本审计每条结论都挂证据锚点（EV-001 至 EV-012），符合 evidence gate。
2. `~/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` — 采用其"Originality / Soundness / Clarity / Significance / Reproducibility / Ethics"六维度；本审计对原 review.md 的 I 级建议（I-1 至 I-4）以"是否可被作者直接行动"为标准（constructive specificity standard）。
3. `~/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` — 采用其"Reviewer-Review Simulation"模板和"Adversarial Questions"；§7 的 C/I/M 分级即来自该模板。
4. `~/.codex/skills/research-planning/SKILL.md` — 用作背景：因本任务是审计而非论文规划，未启动 4-turn planning 流程。
5. `~/.codex/skills/research-planning/references/planning-prompts.md` — 用作背景，确认本任务输出不应转写为 plan_dataset / plan_training schema（不适用）。
6. `~/.codex/skills/research-planning/references/output-schemas.md` — 同上，仅作背景对照。
7. `~/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` — 采用其"completion is artifact-gated"原则：本审计在 §0 卡片显式给出"判定 = needs repair"作为可被验证的 artifact 状态，而不是仅以"已完成阅读"作为完成判据。

**本输出最高风险 3 点（reviewer 视角）**：

1. **Fig. 1 未版面核验**：本审计对 B2 triplet 是否在每一阶段都齐全的判断，建立在 §2 各小节首句的文本重构上。如果 Fig. 1 实际 box 排列与 §2 节次不一一对应（例如 visualization / reporting 在图中可能只是单槽而非三槽），则本审计对 rel.stage_to_triplet 的"每阶段都有三槽"叙述需要降级。**主线程合并时必须打开 `paper.pdf` 核 Fig. 1**。
2. **Supplementary material 未打开**：行 107 脚注 "Underlined words are defined in the supplementary material" 表明文中下划线词（如 RAG、Bertopic、embeddings、feature words 等）有作者给出的定义。本审计未读 supplementary，所以 mech.bertopic / mech.rag 等叶子的取值空间口径只能算 `not_verified`。
3. **被引文献与本文 finding 边界**：§2 各 "Relevant literature" 段引用的 Wang/Huotala/Guo/Petersen 的具体数字（recall 下降、GPT-4 优于 GPT-3.5、case study 判断 GPT-4 优于作者等）极易被下游误读为"本文 finding"。本审计已在 EV-010 + C-iLLM-SMS-T08 显式划界；但 review.md 当前对此分隔不够强，需通过 §7-I-3 建议补一条 EV-005。

**blocked / timeout / 文件缺失状态**：

- 无 blocked：所有指定本地文件 `bibtex.bib` / `metadata.json` / `paper_content.txt` / `review.md` 均成功读取。
- 1 项 deferred：`paper.pdf` 本轮未通过 Read 打开（任务时间窗内未做版面核验）；列为 A2a 必做项，不阻塞本审计输出。
- 1 项 deferred：supplementary material 在线 DOI 下，本轮未打开；同样列为 A2a 必做项。
- 无 timeout。

**最终自我陈述**（reviewer-self-review.md §"Final Self-Review Statement" 模板）：

```text
本审计目前最强的地方在于：清晰区分了"该文无样本编码 schema"vs"该文确有 process/agent/audit/risk 概念骨架"，并把 B1–B7 主干、关系边和审计字段拆出可直接迁回 review.md 的 28 行叶子表 + 9 行关系边表 + 9 行结论表。
当前最大的剩余 reviewer 风险是：Fig. 1 未版面核验，supplementary 未打开；少数叶子（mech.* 工具语义、B2 在 visualization/reporting 阶段是否真有三槽）仍是文本重构判断。
支持中心结论 "tree_type = forest, NOT_in_main_pool" 的主要证据是 EV-001 (作者自述 solution proposal) + EV-009 (Data availability: No data was used)。
本轮主动弱化的主张：不写 Fig. 1 版面已核验；不写 supplementary 已读；不把被引文献数字写成本文 finding；不写"已成熟 evaluation"。
提交阻塞项：无（不阻塞合并）；A2a 必做项 2 项（PDF 版面、supplementary）。
```

---

**报告完。** 总结一行：现有 `review.md` 方向正确（已显式标注"通用六叶 = 投影，原文主树 = 事实源"），但叶子级别仍是占位；建议按本审计 §7 I-1 至 I-4 做 important 级返修——主要工作是把 §3 B1–B7 + §4 叶子表 + §5 关系边表 + §8 A.2/A.3 草案替换/合并进 review.md 现有节，不需要重写。判定 = **needs repair (I 级)，不阻塞合并**。
