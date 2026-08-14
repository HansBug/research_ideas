# 卡片 · **RFSeek**（RFC 散文 → 带 provenance 的协议状态/事件可视摘要）

⭐ **全文可得**：本地 [`baselines/rfseek-and-ye-shall-find/`](../../../../baselines/rfseek-and-ye-shall-find/) 有 `paper.pdf` + `paper_content.txt`（7 页全文，含 References）。⭐⭐ **另外自取了一份论文之外的官方材料**：⭐ 作者 2026-03-19 在 **IETF 125 RASPRG** 的讲稿（16 页 PDF，14.8 MB，⭐ 本卡实际下载并提取过）—— ⭐ 它给出了论文里没有的**外部验证结论**与**工具获取方式**。

⛔⛔ **一句话定位（⭐ 与本簇另两篇的关系）**：⭐ 本簇被派任务时的设想是「三篇都把 LLM 与 sound oracle 接起来」；⛔ **RFSeek 不是** —— ⛔ **它整条流水线里没有任何 oracle、没有任何循环、没有任何机械裁决**。⭐ 它进本簇的价值在**另一维**：⭐⭐ **它是三篇里唯一把「可追溯」当第一等目标的，⭐ 且它的 prompt 敏感性观察是三篇里对我们最直接有用的一组实测。**

---

## A. 元信息

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `id` | `rfseek` | — |
| `title` | RFSeek and Ye Shall Find: A tool for summary visualization and analysis of RFCs | M |
| `year` | ⭐ **2025**（arXiv 首发 2025-09-12） | M |
| `venue` | ⛔⛔ **无正式 venue** —— ⭐ **arXiv preprint**（`cs.NI`，另挂 `cs.HC` / `cs.LG`）。⭐ 已核：Crossref 用完整标题检索**无任何匹配记录**（⭐ 返回的三条是无关文献）。⭐⭐ **但已在 IETF 125 RASPRG（Research and Analysis of Standard-Setting Processes RG）presented**，⭐ 讲稿标题 `Beyond ASCII Art: Making RFC Protocol Logic Auditable with RFSeek`，⭐ session `2026-03-19 06:00`，⭐ 文档状态 `Active`，last updated `2026-03-15` | M |
| `ccf` | ⛔ **未收录**（⭐ arXiv preprint + IETF RG 讲稿，⛔ 均不在 [ccf_venues/](../../../../../ccf_venues/) 范围内） | S |
| `doi` | ⭐ `10.48550/arXiv.2509.10216`（⭐ arXiv DOI）。⛔ **无出版方 DOI**（⭐ 因为无 venue） | M |
| `arxiv` | [2509.10216](https://arxiv.org/abs/2509.10216) —— ⭐ **已核**：arXiv API 返回 `title = RFSeek and Ye Shall Find`（⚠️ **API 只返回主标题，⛔ 不含副标题**），`published 2025-09-12T13:08:50Z`，⛔ 无 `arxiv:doi`、⛔ 无 `journal_ref` | M |
| `artifact_type` | ⭐ **协议状态机的「summary visualization」** —— ⭐ 作者自创的表示，⭐ 比 FSM 更富：⛔ 不只状态与边，⭐ 还含触发事件 + 条件 + 动作细节 + **文本出处** + 分组信息 | M |
| `task` | ⭐⭐ **抽取 + 追溯 + 缺陷检测（针对规范文档本身）** —— ⭐ 注意它检测的**不是模型的缺陷，而是官方 ASCII 图相对 RFC 正文的缺漏**。⛔ 无生成形式模型、⛔ 无修复、⛔ 无验证 | M |
| `boundary` | ⭐ **邻域** —— ⭐ 协议状态机明列在 L3 硬门 2 与 `邻域` 档 | M |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **5 段 · 其中 LLM 3 段 · ⛔ 无循环**）

```
[人] 提供一份 RFC（纯文本，含 ASCII 图）
  → [确定性] 预处理：whitespace normalization + ASCII table condensation
  → [确定性] 按结构切块：section / subsection / 更小 fragment（按大小定）
  → [确定性] 算每块的 dense embedding，检索文档别处语义相关片段作补充上下文
  → [LLM ①] Structural Summarization：逐块产「面向 FSM 抽取」的定向摘要
  → [LLM ②] Visualization Extraction：从**全部摘要**（⭐ 此时能塞进单个 prompt）产图；
              ⭐ 每条边必须**引用**它所依据的摘要片段
  → [LLM ③] Semantic Grounding：为每条边**回取** RFC 原文段落作为依据
  → [确定性] 载入 UI（hover 看摘要、Show in RFC 跳原文并高亮、蓝/绿区分来源、light bulb 只看新边）
  → [人] 审计、验证、改标签、重排版；⭐ 必要时给 RFC 作者写反馈
```

⭐ **阶段名逐字**（§2.2 与讲稿 p.8 一致）：`Structural Summarization` · `Visualization Extraction` · `Semantic Grounding`。⭐ 讲稿的 pipeline 图逐字：`RFC → LLM → Summaries → LLM → Diagram`。〔M〕

⭐ **为什么要先摘要再抽图（逐字）**：`RFC documents are typically too large to be processed by LLMs in a single pass due to input length restrictions.` · `Using summary-based input enables us to include the full RFC context within a single prompt.` ⭐⭐ **即摘要层的作用是「把长文压到能一次看全」，⭐ 从而保住跨章节的长程一致性。**〔M〕

### B2 · 每次 LLM 调用的角色

| 调用 | 角色 |
| :-- | :-- |
| ① Structural Summarization | ⭐ **抽取器 / 摘要者**（⛔ 「摘要者」不在词表里，⭐ 本卡新增：⭐ 它产的是中间自然语言摘要，不是结构化元素） |
| ② Visualization Extraction | ⭐ **生成器**（产节点与边）+ ⭐ **翻译器**（散文 → 图结构） |
| ③ Semantic Grounding | ⭐⭐ **检索改写器 / 溯源器** —— ⛔ 「溯源器」本卡新增：⭐ 它的产物既不是新内容也不是判定，⭐ 而是**每条边到 RFC 原文段落的指针** |

⛔⛔ **没有评审者、没有裁决者、没有修复者。**〔S〕

### B3 · prompt 策略

`RAG`（⭐ embedding 检索文档内语义相关片段作补充上下文 —— 逐字 `we compute dense vector representations (embeddings) and use these to retrieve semantically relevant excerpts from elsewhere in the document to supplement the main content during summarization`）· `分块 + 分阶段任务拆解`（逐字 `partitioned into specific tasks that LLMs excel at, such as summarization and semantic grounding`）· ⭐ **定向摘要（targeted summaries）而非通用摘要** · ⭐ **强制引用约束**（逐字 `we required that every extracted transition be explained by its originating text`）。⛔ **无 few-shot 明述 · ⛔ 无结构化输出 schema 明述 · ⛔ 无 CoT · ⛔ 无 self-consistency · ⛔ 无 function calling · ⛔ 无循环。**〔M〕

⛔ **prompt 原文未公开**（→ D 节）。

### B4 · ⭐⭐ 循环与裁决者

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无循环 | ⛔⛔ **无。** ⭐ 三个 LLM 阶段是**一条直线**，⛔ 没有任何回灌 | M |
| ⭐ **裁决者是谁** | ⛔⛔ **`人`（且只在事后）。** ⭐ 流水线本身**不做任何裁决**；⭐ 唯一的验证装置是 UI：⭐ 人 hover 看依据、点 `Show in RFC` 跳原文、自己判断这条边对不对。⛔ **无 sound oracle、⛔ 无 parser、⛔ 无测试执行、⛔ 无 LLM 自评、⛔ 无确定性规则** | M |
| 终止条件 | ⛔ **不适用**（无循环） | M |
| 最大轮数 | ⛔ **不适用** | M |
| ⭐ 有无报告循环边际收益 | ⛔ **不适用**。⭐⭐ **但它报了一个相邻且极有价值的东西：prompt 变更的边际效应** —— ⭐ 见 B4a | M |

#### B4a · ⭐⭐⭐ 没有循环，但有一组「prompt 改一句话，产出怎么变」的实测（§2.3）

⭐⭐ **这一节（论文的 §2.3 Prompting Strategy）是 RFSeek 对 M1 最有价值的部分**，⛔ 比它的方法本身有价值。⭐ 四条实测，⭐ **全部逐字**：

| # | 改了什么 | ⭐ 结果（逐字） | ⭐ 我方读法 |
| :-: | :-- | :-- | :-- |
| 1 | ⭐ 只喂「最相关」的章节（选择性输入） | `While this sanity check performed reasonably well, it reproduced the transitions already depicted in the diagrams and did not yield any new or implicit protocol behaviors.` | ⛔⛔ **精准检索会把「新发现」检索掉** —— ⭐ 只喂最相关的段落，模型就只会复述已知的东西 |
| 2 | ⭐ 从输入里**去掉** RFC 自带的 ASCII 图（对 RFC9293） | `When the diagram was absent, certain transitions were missing from the summaries, as they were not directly mentioned elsewhere in the document. While we did not systematically assess this across all protocols, this suggests that transitions described exclusively in diagrams may be overlooked by LLM-based extraction methods focused on text.` | ⭐ 图里有正文没有的信息；⛔ 纯文本路线会漏 |
| 3 | ⭐⭐ 把 prompt 改成要求抽「**精确且准确的** FSM」 | ⭐⭐⭐ `Notably, when we prompted the LLM to extract a "precise and accurate FSM" it completely omitted some edges it had previously identified, such as the one shown in Figure 2b.` | ⛔⛔⛔ **要求「精确」直接删掉了召回** —— ⭐ 而被删掉的正是**全文的核心发现那条边**（⭐ Figure 2b = 后来促成 RFC 9293 errata 的那条 `SYN-RECEIVED → LISTEN`） |
| 4 | ⭐⭐ 加一句「把摘要里提到的**所有**迁移都抽出来」 | ⭐⭐⭐ `Interestingly, this did not increase the total number of transitions identified; rather, the set of extracted transitions shifted. With the revised prompt, only transitions explicitly mentioned in the summaries were extracted, while transitions previously inferred implicitly by the LLM from the text were now omitted. This warrants further investigation.` | ⛔⛔⛔ **产出总数守恒，⛔ 集合发生位移** —— ⭐ 加一条要求换来的不是「多抽几条」，⭐ 而是「换成抽另一批」 |

⭐⭐⭐ **第 3、4 条与我们 v46 的 `occupancy_after` 事故是同一个现象。** ⭐ 我们那次是：⭐ 一条 `nl_cue` 的措辞在**逐字教模型别用 `edge_declared`**，⛔ 结果 324 格里 `edge_declared` 被问 **0.0%**；⭐ 改掉措辞后 0 → 4/6。⭐⭐ **RFSeek 独立在另一个任务、另一个模型（GPT-4.1）、另一个团队上撞到了同一件事**，⛔ 而且他们把它写进了论文。⭐ **这构成一条可引的外部证据：prompt 措辞会重新分配召回，而不是增加召回。**〔M（四条逐字）+ S（与我方事故的同构性）〕

### B5 · ⭐ 中间表示

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无 | ⭐ **有，两层** | M |
| 形态①：⭐ **结构化摘要**（section-level summaries）| ⭐ 自然语言、⛔ 非结构化 schema，⭐ 但**定向**（针对 FSM 抽取而非通用摘要）。⭐ 逐字 `We also compared general-purpose summaries to targeted summaries focused on FSM extraction ... Using shorter, targeted summaries did not reduce precision, so we adopted them as our default input.` | M |
| 形态②：⭐⭐ **自创 summary representation**（§2.1）| ⭐ **每条迁移的字段表是闭合的四项**，⭐ 逐字：`(i) the triggering event, and any relevant conditions; (ii) the action that should be taken, if any, in detail - including the construction / destruction of data structures, error codes, and any other pertinent information; (iii) the originating text (see §2.2), and (iv) in case of a grouped transition: which states are included.` | M |
| ⭐ **是否闭合** | ⭐ **字段 schema 闭合，⛔ 内容完全开放**。⭐ 闭合的部分：迁移必须有上述四项；⭐ 另有两类**新引入的元素类型** —— ⭐ **grouped / `any` 节点**（逐字 `when multiple states share the same event and handle it identically, we introduce a representative grouped node to avoid overcrowding the presentation`；⭐ 讲稿与 Fig 2a 里是灰色椭圆）与 ⭐⭐ **inferred transitions**（逐字 `we include transitions that are recommended but are not mandatory, and transitions that are inferred from the text. In the case of inferred transitions, our summary always includes the reasoning for their creation. To the best of our knowledge, this is the first time such edges have been introduced.`）。⛔ 开放的部分：状态名、事件名、条件、动作全自由生成 | M |
| ⭐ **谁定的** | ⭐ **作者预定义表示，⭐ LLM 自由填** —— ⛔ **没有任何「从固定集合里选」的环节**。⛔ 无预编目录、⛔ 无规则匹配、⛔ 人不挑 | S |

⭐⭐ **对我们的可比性**：⭐ 我们是「**闭合 19 条谓词 + LLM 自动选**」；⛔ 它是「**闭合的字段表 + 完全开放的内容**」。⭐⭐ **所以它在 B5 这一维上是我们的反面**：⛔ 它靠「不限制内容」换来了新发现（⭐ RFC 9293 那条边），⛔ 代价是**没有任何机械手段判断一条边是不是编的**（→ C 节）。

### B6 · 模型

⛔⛔ **单一模型，⛔ 无对照，⛔ 无版本日期**：⭐ 逐字 `All experiments used the OpenAI GPT-4.1 model via the OpenAI API.`

⚠️ **两个问题**：① ⛔ **只给 `GPT-4.1` 一个名字，⛔ 无 snapshot 日期**（⭐ 对照 PAT-Agent 给了 `o3-mini-2025-01-31`、Event-B Agent 给了 `GPT-5 (2025-08-07 version)`）—— ⛔ **不可精确复现**；② ⛔ **无第二个模型对照**，⭐ 故 §2.3 那四条 prompt 敏感性观察**无法排除「这是 GPT-4.1 一个模型的特性」**。⚠️ 按 X1 的结论，GPT-4.1 与当前 SOTA 有代际差，⛔ **绝对数字（Table 1 的 missing edges）参考价值要打折**；⭐ 但 §2.3 的**方向性**观察与我们在 SOTA 上的独立观察一致，⭐ 故那部分的参考价值反而更高。〔M（模型名）+ I（打折与"更高"两句是我方判断）〕

### B7 · ⭐ 确定性成分（⛔ 本簇最薄的一层）

| 环节 | 是什么 | 级别 |
| :-- | :-- | :-: |
| 预处理 | ⭐ whitespace normalization + ASCII table condensation | M |
| ⭐ 结构切块 | ⭐ 按 section / subsection / fragment 切，⭐ 按大小定粒度 | M |
| ⭐ embedding + 检索 | ⭐ dense vector 检索文档内语义相关片段 | M |
| ⭐ UI | ⭐ hover / `Show in RFC` / `Recenter` / 蓝绿着色 / light bulb 切换 / `5/6` 计数与前后翻 / 可保存复用的用户定制 | M |
| ⛔⛔ **oracle** | ⛔⛔ **无。** ⛔ 无模型检查器、⛔ 无 parser、⛔ 无编译器、⛔ 无求解器、⛔ 无一致性检查器、⛔ 无字符串校验 | M（全文与讲稿均无任何验证组件） |

⭐⭐⭐ **对 M1 的一条硬结论**：⭐ **RFSeek 证明了「不接 oracle 也能做出对领域专家有用的东西」**（⭐ 它促成了一条 RFC errata），⛔ **但代价是它的正确性主张完全无法被机械检验**（→ C 节）。⭐ **这正是我们的处境的一个镜像**：⭐ 我们有 pyfcstm 可用，⛔ 只是放在了求值端 —— ⭐ **RFSeek 是「连求值端都没有」的那一档，⭐ 看清它付出的代价，就知道我们那个 oracle 值多少。**

---

## C. 实验

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⭐ **有，一个外部方法：`PROSPER`**（Sharma & Yegneswaran，HotNets 2023，⭐ 同为 LLM 抽 RFC FSM 且同以「供人理解」为目标）。⛔ **无消融、⛔ 无自建 LLM 直出 baseline、⛔ 无多模型对照** | M |
| `dataset` | ⛔⛔ **4 份 RFC**：`PPTP (RFC2637)` · `DCCP (RFC4341)` · `QUIC (RFC9000)` · `TCP (RFC9293)`。⛔ **分母极小，⛔ 且分母定义有断口** —— 见 C.1 | M |
| `metrics` | ⛔⛔ **只有两个，且只测一侧**：`Missing Nodes` · `Missing Edges`（⭐ 逐字表注 `lower is better`）。⛔⛔ **无 precision、⛔ 无 false-positive、⛔ 无多报计数、⛔ 无 `@k`、⛔ 无任何多轮口径** | M |
| ⭐ `judged_by` | ⛔⛔ **作者自己，人工比对，⛔ 无标注者间一致性**。⭐ 判据是「RFSeek 的图 vs RFC 里已发表的 ASCII 图」：逐字 `For each, we measured how faithfully RFSeek recovered FSM edges and nodes depicted in the published diagrams`。⛔ **无第三方、⛔ 无 $\kappa$、⛔ 无一致率、⛔ 无 LLM-as-judge**（⭐ 后者在这里反而是优点） | M |
| `human_baseline` | ⛔ **无**（⛔ 无 user study —— ⭐ 讲稿 p.15 说**正在招**：逐字 `We are looking for protocol practitioners to help shape the project ‣Participate in short usability sessions ‣Join us at the IETF 126 Hackathon`） | M |
| `runs` | ⛔⛔ **未报运行次数、⛔ 未报方差、⛔ 未报 temperature / seed**。⭐ 已 grep 全文确认 | M |
| ⭐ `adverse_results` | ⭐ 见 C.1 / C.2 / C.3 | — |

### C.1 ⛔⛔ 它的评测只测召回、⛔ 不测精度 —— ⭐ 而它的核心主张恰恰是精度

⭐ **它宣称的目标是 soundness**，逐字（§5）：`although our summaries are LLM-extracted, we prioritize soundness with respect to the RFC: approximate FSMs may suffice for automation, but for understanding and auditability, correctness is essential.` ⭐ 又（§4）：`While we do not claim completeness, we focus on correctness: our extracted summary diagrams are grounded in and traceable to the RFC source.`

⛔⛔⛔ **但 Table 1 的两个指标（Missing Nodes / Missing Edges）量的全是「漏了多少」，⛔ 一个都不量「多出了多少」。** ⛔ **即：它把主张放在 correctness 上，却只测了 completeness 的那一侧。** ⭐ 那些「RFC 图里没有、RFSeek 新加的边」有多少是真的、多少是编的，⛔ **论文里没有任何数字**。⭐ 唯一的正面证据是**逐个案例的定性核对**（⭐ 四个 case study 各举 1–2 条新边并回原文说明）。

⭐ Table 1 逐字（⭐ 含两条脚注，⭐ 脚注本身是诚实的）：

| RFC | PROSPER Missing Nodes | PROSPER Missing Edges | RFSeek Missing Nodes | RFSeek Missing Edges |
| :-- | :-: | :-: | :-: | :-: |
| PPTP (RFC2637) | 0 | 19 | 0 | **6** |
| DCCP (RFC4341) | 1 | 7 | 0 | **1** |
| QUIC (RFC9000) | — | — | 0 | **2** |
| TCP (RFC9293) | — | — | 0 | **1** |

⭐ 脚注 1 逐字：`The RFC only shows two diagrams, others are described, making it a poor candidate for PROSPER.` ⭐ 脚注 2 逐字：`PROSPER use RFC 793 for TCP, making a direct comparison unfair.`

⭐⭐ **值得肯定的一点**：⛔ 4 行里**有 2 行 baseline 是空的**，⭐ 而作者**在表内脚注里明写为什么不可比**（⛔ 而不是留空不解释、⛔ 也不是硬凑一个数）。⭐ **这个处理方式可以直接借鉴** —— ⭐ 我们 L1 实测「外部可比数字 0 条」时的写法与此同构。

### C.2 ⭐⭐⭐ 一条**真正的外部验证**：RFC 9293 的 editorial errata 被接受了

⛔ **论文里只写到「可以给作者写反馈」这一步**（§1 逐字 `they send a note to the RFC authors. At the very least, they suggest adding a reference to the omission in Section 3.3.2.`）。

⭐⭐ **但讲稿（IETF 125 RASPRG，2026-03-19）给出了后续结果**，⭐ 逐字片段（⚠️ **PDF 提取时两句被挤在一行**，⭐ 原文是两张幻灯片元素）：
- `Example: the TCP state machine from RFC9293` + `Result: an editorial errata was submitted and accepted`
- 结果页逐字：`TCP 1 missing edge Led to editorial errata for RFC 9293`

⭐⭐⭐ **这是本簇三篇里唯一一条「第三方权威接受了方法的产出」的证据。** ⭐ 另有一条独立交叉验证在论文里：逐字 `a review of the Linux kernel's TCP implementation reveals that this transition is, in fact, present there.` ⭐ **即那条边有两重外部确认：Linux 内核实现 + IETF 接受的 errata。**

⭐⭐ **对我们的意义（⛔ 这是策略性的，不是方法性的）**：⭐ **一个只有 4 个样本、只测单侧指标、无 baseline 消融、无方差的工作，靠「一条被标准组织接受的发现」建立了可信度。** ⭐ 我们手上有 **574 位人工逐位判定 + 324 格 + 三口径**，⛔ 但**没有任何一条「被外部接受」的发现**。⚠️ **这个不对称值得记：证据的『量』与证据的『分量』不是一回事。**〔M（讲稿与论文逐字）+ I（策略读法是我方判断）〕

### C.3 ⭐ 它怎么处理不利结果

1. ⭐ **PPTP 上漏了 6 条边，⛔ 照实报**（⭐ Table 1 里 RFSeek 自己那一列并非全 0）。⭐ 正文逐字 `RFSeek recovered all but six diagrammed transitions`。
2. ⭐ **主动限定主张**：逐字 `While we do not claim completeness`。
3. ⭐⭐ **把自己的 prompt 探索过程里的失败全写出来**（B4a 四条）—— ⛔ 包括「加了一条要求反而把 inferred 边弄丢了」这种**对自己不利**的结果，⭐ 并诚实地写 `This warrants further investigation.` ⭐⭐ **在一篇 7 页短文里花整整一节写「我们试过什么、什么没成」，⭐ 这个取舍值得学。**
4. ⭐ **对 QUIC 这一行只有 RFSeek 有数字**，⛔ 但**在脚注里说明是 PROSPER 不适用而非我方挑软柿子**。

### C.4 ⛔ 断言 / 性质从哪来

⛔⛔ **不适用 —— 它没有断言、没有性质、没有验证。** ⭐ 它的「判据」是**官方 ASCII 图**（⭐ 作为召回的分母），⛔ 而那个分母本身是不完整的（⭐ 论文全文的出发点就是这一点：逐字 `these depictions of Finite State Machines (FSMs) are typically abstract, and often incomplete`）。⭐⭐ **所以它处在一个循环里**：⛔ 用不完整的图当分母去量一个声称要超越那张图的方法。⭐ 作者对此是清楚的（⭐ 才有 case study 那些定性核对），⛔ 但**没有构造出第二个分母**。〔S〕

---

## D. ⭐ 资产（⛔ 逐条实际取过）—— ⛔ **本簇最差的一家**

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | 🟢 | [arXiv:2509.10216](https://arxiv.org/abs/2509.10216) · 本地 `paper.pdf` | ⭐ arXiv API title 一致、`published 2025-09-12T13:08:50Z` · 本地 7 页全文已通读 |
| ⭐ **官方讲稿（论文之外的材料）** | 🟢 | [IETF 125 RASPRG 讲稿](https://datatracker.ietf.org/doc/slides-125-rasprg-beyond-ascii-art-making-rfc-protocol-logic-auditable-with-rfseek/) | ⭐⭐ **本卡实际下载并提取过**：`HTTP 200 · application/pdf · 14,755,240 B · PDF 1.3 · 16 页`，⭐ 用 `tools.pdf_extractor` 提出 16 页文本。⭐ Datatracker 元数据：`slides-125-rasprg-...-00` · `Meeting Slides` · session `2026-03-19 06:00` · state `Active` · last updated `2026-03-15`。⚠️ ⛔ **Datatracker 页面本身不列作者名** |
| ⛔⛔ **实验代码** | ⚪ → 🟡 | ⛔ 无 | ⛔⛔ **论文全文无任何 availability statement** —— ⭐ 已 grep `available\|github\|artifact\|open.?source\|zenodo\|release\|our (tool\|code\|repo)`，⛔ **11 处命中全部是参考文献 URL 或在讲 PROSPER 的 Artifact Miner**，⛔ **零处是自己的代码**。⭐ 已试过 WebSearch（⛔ 未找到仓库或 demo）。⭐⭐ **讲稿 p.15 只给一个邮箱**：逐字 `Email: RFSeek.info@gmail.com` + `https://arxiv.org/pdf/2509.10216`。⭐ **故按简报口径判 🟡（需联系申请）而非 ⚪** —— ⭐ 讲稿邀请 practitioner 参加 usability session 与 IETF 126 Hackathon，⭐ 说明**存在一个可用实例**，⛔ 只是不公开 |
| 数据集 / Benchmark | 🟢（输入）/ ⚪（打包） | RFC2637 / RFC4341 / RFC9000 / RFC9293 | ⭐ 输入是公开 RFC，⭐ 任何人都能自取（⭐ IETF 官方 DOI 如 [RFC 9293](https://doi.org/10.17487/RFC9293)）。⛔⛔ **但没有打包的评测集** —— ⛔ 无 ground-truth 边表、⛔ 无「官方图里有哪些边」的机读清单、⛔ 无 RFSeek 输出的图文件。⛔ **即 Table 1 那 4 行数字无法被独立复算** |
| ⭐ 实验结果细则 | ⚪ | — | ⛔ **只有论文里的 Table 1（4 行 × 4 列）**。⛔ 无逐边清单、⛔ 无「哪 6 条 PPTP 边漏了」的枚举、⛔ 无新增边的完整列表。⭐ 讲稿 p.11 给了同一份数字的另一种排版，⛔ 未增加信息 |
| Artifact / 复现包 DOI | ⚪ | — | ⛔ 无 Zenodo / 4open / OSF |
| ⛔⛔ **prompt 是否公开** | ⚪ | — | ⛔⛔ **未公开。** ⭐ §2.3 用散文描述了四种 prompt 策略与它们的效果，⛔ **但没有给出任何 prompt 原文**。⛔ **这使 B4a 那四条极有价值的观察无法被复现** |
| license | ⚪ | — | ⛔ 无代码故无 license；⭐ arXiv 页的许可未核 |

⭐⭐ **总评**：⛔⛔ **本簇资产最差的一家，⭐ 且缺口正好落在最有价值的地方** —— ⭐ 它最值得复用的东西是 §2.3 那四条 prompt 敏感性观察，⛔ 而 **prompt 原文恰恰没公开**。⚠️ **这不是空壳仓库问题（⭐ 它根本没仓库），⛔ 是「有一手观察但拿不到可复现载体」。**

---

## E. ⭐ 对 M1 的意义

### 1. ⭐⭐ 可取之处

1. ⭐⭐⭐ **§2.3 那四条 prompt 敏感性实测**（B4a）—— ⭐ 尤其第 3、4 条。⭐⭐ **可直接当作我方 `occupancy_after` / `nl_cue` 事故的外部同构证据**：⛔ 「要求更精确」会删召回；⛔ 「多加一条要求」不增总量只换集合。⭐ **对 M1 的操作含义**：⛔ **每次改 prompt 措辞后，不能只看目标指标涨没涨，必须看「被换走了什么」** —— ⭐ 我们的五类多报分类正好可以承担这个观测，⛔ 但目前没有一个「集合位移量」的指标（⭐ 例如两代次命中集合的对称差）。
2. ⭐⭐ **provenance 做成一等公民，⭐ 且在产物 schema 里强制**（B5 形态②的字段 iii）。⭐ **对我们 C-③「可追溯」那一维的直接对照**：⭐ 我们的证据绑定（`bind_attribution`）是**流水线的一个阶段**，⛔ 而它是**产物的一个必填字段**。⭐⭐ **后者更硬**：⛔ 字段缺失就是产物不合格，⛔ 而阶段可以产出空绑定。
3. ⭐⭐ **`inferred` 与 `derived-from-diagram` 分开着色 + 可切换只看新的**（⭐ 蓝 = 来自 FSM 章节、绿 = 来自正文别处、light bulb 切换）。⭐⭐ **这是一个把「证据强度」做进 UI 的做法**。⭐ 对我们：⛔ 我们的台账目前把「有领域证据 / 元模型定义性 / 无外部依据」三类分级**记在文档里**，⛔ **没有做进任何产物或界面** —— ⭐ 而分级的价值恰恰在于**每次读到一条结论时都能看见它的强度**。
4. ⭐⭐ **inferred 边必须附推理理由**（逐字 `In the case of inferred transitions, our summary always includes the reasoning for their creation.`）。⭐ 即**推断出来的东西必须自带「为什么」**，⛔ 而不是与直接证据混在一起。
5. ⭐ **不可比的 baseline 单元格留空 + 表内脚注说明原因**（C.1）—— ⭐ 我们 L1 的「外部可比数字 0 条」可以照这个格式写。
6. ⭐ **在 7 页里花一节写失败探索**（C.3 ③）—— ⭐ 值得学的取舍。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔⛔ **它宣称 soundness，却只测了 completeness 的反面（missing），⛔ 从不测多报。**（C.1）⭐⭐ **这条对我们是一面镜子**：⛔ 若我们只报 `hit@k` 而不报多报，⛔ 就是同一个毛病。⭐ **我们已经报五类多报 —— ⛔ 不要因为任何理由把它去掉。**
2. ⛔⛔⛔ **provenance 是 LLM 断言的，⛔ 不是机械核验的。**（→ E.3 与 F.1）⭐ 整条溯源链是「LLM 引用摘要片段 → LLM 回取 RFC 段落」，⛔ **没有任何一步验证「被引用的那段文字真的存在于 RFC 里」**，⛔ 也没有验证「那段文字真的支持这条边」。⭐⭐ **可追溯 ≠ 已核验** —— ⭐ 它做到的是「**让人能审**」，⛔ 不是「**机器已审**」。⛔ **若我们照搬，会得到一个看起来有证据链、实则每一环都是生成物的产物。**
3. ⛔⛔ **无 oracle、无循环、无任何机械裁决**（B7）—— ⭐ 故它对「裁决者该换成什么」这一问**给不出正面答案**，⛔ 只给出反面参照（⭐ 不接 oracle 的代价见 C.1 / C.4）。⛔ **不要引 RFSeek 支持任何关于循环或裁决者的主张。**
4. ⛔⛔ **分母是一个自己承认不完整的东西**（C.4）—— ⛔ 用不完整的官方 ASCII 图当召回分母，去量一个声称要超越它的方法。⭐ **对我们**：⚠️ 我们的台账 98 条能力分母正在 G1 全量重标，⛔ **这条提醒我们分母的构造方式本身要能被质询**。
5. ⛔ **4 个样本、⛔ 单模型、⛔ 无版本日期、⛔ 未报运行次数、⛔ 无方差、⛔ prompt 未公开** —— ⭐ 六项里我们全部做得更好，⛔ 不要退。
6. ⛔ **靠 `grouped / any 节点` 压缩展示，⛔ 但没有量化压缩造成的信息损失。** ⭐ 逐字理由是 `to avoid overcrowding the presentation` —— ⭐ 一个**呈现层**的理由改变了**产物的语义**（⛔ 多个状态被折成一个代表节点）。⛔ 论文未讨论这是否让某些迁移变得无法区分。

### 3. ⚠️ 与我们的关键差别（⛔ 说明为什么不能直接照搬）

1. ⛔⛔⛔ **它检测的对象根本不同。** ⭐ 我们检测「**模型相对 NL 需求的缺陷**」；⭐ 它检测「**官方图相对 RFC 正文的缺漏**」。⭐⭐ **关键后果**：⛔ 它的「被检对象」是一张**图**、「参照物」是**同一份文档的正文**，⭐ 所以两侧同源、同一份文本；⛔ **我们的两侧是异源的**（⭐ 一个是 DSL 模型，一个是自然语言）。⛔ **所以它的溯源做法（回指同一文档的段落）在我们这里要跨表示对齐，⛔ 难度不是一个量级。**
2. ⛔⛔ **它的产物是给人看的，⛔ 不是给机器求值的。** ⭐ 逐字 `the FSMs produced by prior work are machine-readable representations intended for trace synthesis, whereas RFSeek provides users with human-interpretable summary diagrams for interactive exploration.` ⭐⭐ **这解释了它为什么可以不接 oracle** —— ⛔ **人在回路里做最终裁决**。⛔ 我们的目标是自动化闭环，⛔ 不能靠这一条。
3. ⭐ **制品邻域**（协议状态机）—— ⭐ 按 L3 规定不设边界门，⛔ 但进论文必须回 L1 重走。
4. ⚠️ **无 venue、无 CCF** —— ⭐ arXiv preprint + IETF RG 讲稿。⛔ **若要在论文里引它，必须清楚它没有经过同行评审**；⭐ 但它引出的 RFC 9293 errata 是**可查的第三方事实**，⛔ 那部分不受 venue 影响。

---

## F. ⛔ 存疑与未核项

1. ⚠️⚠️⚠️ **provenance 到底锚在什么粒度上，⛔ 论文没说清 —— ⭐ 这是本卡最重要的未核项，⭐ 也正好是主 session 第 4 问要的那格。** ⭐ 能确认的：
   - ⭐ **粒度 = 文本段落 / passage**（⛔ **不是字符级偏移、⛔ 不是段落 id、⛔ 也不只是散文引用**）。逐字：`we prompt the LLM to retrieve the corresponding RFC text passages that justify each edge`。
   - ⭐ **是可枚举、可计数的**：UI 里显示 `5/6` 并可前后翻。逐字 `If an edge is justified by multiple text passages, the summary tooltip displays progress (e.g., "5/6") and arrow buttons enable navigation between all supporting RFC snippets.`
   - ⭐ **是两跳链，不是一跳**：边 → 摘要片段（逐字 `we instruct the LLM to identify and cite the specific summary segment(s) that serve as the basis for that transition`）→ RFC 原文段落（上一条）。
   - ⛔⛔ **不能确认①：那些 passage 是怎么在 RFC 正文里被定位并高亮的。** ⭐ 论文只说 `automatically scrolls the RFC side panel to the first relevant passage and highlights all supporting locations`，⛔ **完全没说锚定机制**（⛔ 是字符串精确匹配？⛔ 模糊匹配？⛔ LLM 直接给行号？⛔ 未提及任何一种）。
   - ⛔⛔ **不能确认②：有没有任何一步验证「LLM 回取的那段文字真的存在于 RFC 里」。** ⛔ 全文与讲稿都没有提到任何校验。⭐ 已试过：通读全文 §2.1 / §2.2 / §3 与讲稿 16 页全文，⛔ 均无。
   - ⛔⛔ **因此定稿口径**：⭐ 必须写成「**provenance 是 LLM 断言的，可被人审计，但未被机器核验**」，⛔ **不得写成「每个节点/边都能指回 RFC 的具体文本」这种事实句。**
2. ⚠️ **工具是否真的存在可用实例** —— ⭐ 讲稿邀请 practitioner 参加 usability session 与 IETF 126 Hackathon，⭐ **强烈暗示存在**；⛔ 但**本轮未取到任何可访问的实例**。⭐ 已试过：① grep 论文全文找 availability（⛔ 零命中）；② WebSearch（⛔ 未找到仓库/demo）；③ 读 Datatracker 元数据页（⛔ 无链接）；④ 提取 16 页讲稿并 grep `github|http|demo|try it`（⭐ **只命中一个 gmail 与 arXiv PDF 链接**）。
3. ⚠️ **`GPT-4.1` 无 snapshot 日期** —— ⛔ 原文未提供，⛔ 不可精确复现。
4. ⚠️ **Table 1 的 4 行数字无法独立复算** —— ⛔ 无 ground-truth 边表、⛔ 无 RFSeek 输出的图文件。⭐ 已试过在论文与讲稿里找逐边清单，⛔ 均无。
5. ⚠️ **QUIC 那行「2 missing edges」的分母是什么，⛔ 不清楚** —— ⭐ 论文自己说 QUIC 的 RFC `provides partial and inconsistent state machine figures for select procedures`，⛔ 那么「漏了 2 条」是相对哪张图算的、总共几条，⛔ 原文未提供。
6. ⚠️ **讲稿里 `an editorial errata was submitted and accepted` 未在 IETF errata 系统里独立核到** —— ⭐ 已试过：读 Datatracker 讲稿元数据页（⛔ 无 errata 记录）+ 提取讲稿全文（⭐ 有这句）。⛔ **本轮未去 RFC Editor 的 errata 数据库查 RFC 9293 的 errata 条目**，⛔ 故这条只有作者自陈（⭐ 但是在 IETF 官方场合的自陈）。
7. ⚠️ **`grouped / any 节点` 的合并规则是否确定性** —— ⭐ 判据逐字是 `when multiple states share the same event and handle it identically`，⛔ 但「handle it identically」谁判、⛔ 是 LLM 判还是规则判，⛔ 原文未提供。
8. ⚠️ **PDF 提取时讲稿多处文字被挤在一行**（⭐ 幻灯片元素本无阅读顺序）—— ⭐ 本卡引用讲稿时已逐处标明是片段；⛔ **不排除某些并列文字实际属于不同幻灯片**。⭐ 已用 `-m text` 模式，⛔ 未回 PDF 逐页目视核对版面。
