# 卡片 · **Process Fragment Recommendation in Process Modeling: Are LLMs the Answer?**（TSE 2026）

⭐ 本轮**唯一顶刊级（CCF A / TSE）**条目。

---

## ⛔⛔ 版本声明（⭐ 读这张卡前必须先读这一节）

⚠️ **正式发表版（IEEE TSE 2026）全文不可得**（IEEE Xplore 付费墙，Unpaywall / OpenAlex 均判 `closed`，WUR 机构库记录挂了 accepted version 却**不提供 PDF**）。

⭐ **本卡的 B / C 两节内容取自同一工作的开放获取前置版本**：作者博士论文 [Supporting business process management: clone detection and recommendation techniques](https://pure.tue.nl/ws/files/369623105/20251113_Saeedi_Nikoo_hf.pdf)（TU/e，2025-11-13 答辩，199 页，⭐ 本轮实测 HTTP 200 / 24,185,921 bytes）的 **Chapter 5**（pp. 126–162）。

⭐ **两版是同一工作，有三条独立交叉证据**：

| # | 证据 | 内容 |
| :-: | :-- | :-- |
| 1 | 论文自陈（thesis §1.3 逐字） | "Subprocess Recommendation in Process Modeling: Are Large Language Models the Answer? **Under review at Transactions on Software Engineering (TSE) journal**." |
| 2 | ⭐ Zenodo 记录已回填终版信息 | 复现包 [10.5281/zenodo.15110021](https://doi.org/10.5281/zenodo.15110021) 的标题用的是**终版标题** `Process Fragment Recommendation...`，描述里逐字写着 `doi: 10.1109/TSE.2026.3690186, May 2026` |
| 3 | ⭐ 终版摘要与 thesis 摘要在核心数字上一致 | 「LLMs might not be the answer always」「maximum of 6 nodes」「three times more meaningful」「≈60% of the complete process」四处措辞在 WUR 记录的终版摘要中原样出现 |

⛔ **但仍有版本风险，必须记住两条**：

1. ⚠️ **标题在评审中改过**：`Subprocess Recommendation` → `Process Fragment Recommendation`；`Large Language Models` → `LLMs`。⭐ 说明评审期确实做过修订。
2. ⛔ **终版 pp. 1–21，thesis 章节约 37 页**——⛔ 篇幅口径不同，**细节数字可能在修订中变动过**。

⭐ **因此本卡的证据级别按两档记**：

- **M(thesis)** = thesis Chapter 5 原文明写（附逐字英文）
- **M(pub)** = ⭐ **同时**在终版摘要里得到确认（⭐ 这一档最硬）
- **S / I** = 照 schema 通用口径

---

## A. 元信息

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `id` | `tse2026-process-fragment-recommendation` | — |
| `title` | Process Fragment Recommendation in Process Modeling: Are LLMs the Answer? | M(pub) |
| `year` | ⭐ **2026**（⚠️ e-pub ahead of print **2026-05-14**；⛔ 无 volume / issue，pp. 1–21） | M(pub) |
| `venue` | ⭐ **IEEE Transactions on Software Engineering (TSE)** | M(pub) |
| `ccf` | ⭐⭐ **A**（[ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 第 53 行：`journal-a-tse \| TSE \| 期刊 \| 🏆 \| 软工综合顶刊，四个 project 都可对齐`） | M |
| `doi` | ⭐ [10.1109/TSE.2026.3690186](https://doi.org/10.1109/TSE.2026.3690186) —— ⭐ **本轮实际经 Crossref API 核验过**（返回 title / authors / pages 1-21 / container-title 全部匹配） | M |
| `arxiv` | ⛔ **无**（arXiv API 按标题与按作者两路检索均 0 命中） | M |
| `url` | 开放前置版：[TU/e Pure 论文 PDF](https://pure.tue.nl/ws/files/369623105/20251113_Saeedi_Nikoo_hf.pdf) · 终版记录：[WUR](https://research.wur.nl/en/publications/process-fragment-recommendation-in-process-modeling-are-llms-the-) | M |
| 作者 | Mahdi Saeedi Nikoo · Sangeeth Kochanthara · Önder Babur · Mark van den Brand（TU Eindhoven；⭐ Babur 现 Wageningen） | M |
| `artifact_type` | ⭐ **BPMN 2.0 过程模型**，具体到 `subprocess`（子过程）元素 | M(thesis) |
| `task` | ⭐ **补全 / 推荐**（给一个残缺子过程，推荐它的完整形态）——⛔ **不是**缺陷检测、⛔ 不是一致性检查 | M(thesis) |
| `boundary` | ⭐ **邻域**（BPMN 与工作流，见 [README.md](../README.md) §2.1 三档表） | M |

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐⭐ **本文有两条平行流水线**（⛔ 这是全文结构的关键：LLM 那条是**被对照的一方**，不是唯一一方）。

**A 路 · 相似度检索式推荐（⛔ 零 LLM）**

```
[确定性] Camunda BPMN Model API 解析 BPMN
   → [确定性] 纳入/排除四道过滤（节点数 / 语言 / 标签长度 / 去重）
   → [确定性] 深度优先切片，生成 30/50/70/90% 残缺子过程
   → [确定性] SAMOS（VSM + bigram）或 Apromore（GED + 串编辑 + WordNet）全库检索
   → [确定性] 取 top-n 作为推荐
```

**B 路 · LLM 生成式推荐**

```
[确定性] 同上，切片得到残缺子过程
   → [确定性] 编码成「简化 bigram」文本
   → [LLM] zero-shot 单次调用，补全子过程
   → [确定性] bigram 解析器（⛔ 解析失败即整例丢弃，⛔ 不回灌不重试）
   → [确定性] bigram → 图 → BPMN 可视化
   → [确定性] SAMOS 与 Apromore 双份相似度打分 + 阈值规则判「是否 meaningful」
```

⭐ **阶段计数：B 路 7 个阶段，其中 LLM 阶段 1 个（1/7）。A 路 5 个阶段，LLM 阶段 0 个。**

⚠️ **对照我们的 10 节点 / 5 LLM**：⛔ 这套流水线的 LLM 占比低得多，⭐ 而且 **LLM 只在一个点上出现、只被调用一次**。

- 级别 **M(thesis)**：§5.3 逐字 —— "In the second approach, the subprocess under development is presented to an LLM. We ask the LLM to complete the subprocess. We then transform the LLM-generated completion into a corresponding visual representation in BPMN"

### B2 · 每次 LLM 调用的角色

| 调用 | 角色 | 级别 |
| :-- | :-- | :-: |
| 唯一一次调用 | ⭐ **生成器**（补全残缺子过程）——⭐ 兼 **翻译器**（须以受约束的 bigram 文本格式输出） | M(thesis) |

⛔⛔ **没有评审者 · 没有修复者 · 没有裁决者 · 没有规划者 · 没有分类器。** ⭐ 这是本卡与我们最大的形态差异。

### B3 · prompt 策略

| 策略 | 有无 | 细节 | 级别 |
| :-- | :-: | :-- | :-: |
| `zero-shot` | ⭐ **有** | 逐字："we applied **zero-shot learning**" | M(thesis) |
| `few-shot` | ⛔ **无** | ⭐ 明确列为 out of scope（§5.7） | M(thesis) |
| `CoT` | ⛔ **无** | ⭐ 明确拒绝并给了理由（见下） | M(thesis) |
| `self-consistency` 投票 | ⛔ **无** | 原文未提及 | S |
| `RAG` | ⛔ **无** | ⭐ 只作为 future work 建议（§5.7） | M(thesis) |
| 工具调用 / function calling | ⛔ **无** | 原文未提及 | S |
| ⭐ `结构化输出约束` | ⚠️ **只有文字描述，⛔ 无 schema / 无受限解码** | ⭐ 靠 prompt 里一段自然语言定义格式；⛔ 校验只在事后由解析器做 | M(thesis) |
| `角色扮演` | ⭐ **有** | Persona pattern："You are an expert in business process modeling." | M(thesis) |
| 多智能体辩论 | ⛔ **无** | — | S |

⭐ **prompt 三段式来自 White et al. 的 prompt pattern catalog，三个 pattern 各管一段**（§5.3.2）：

1. **Meta Language Creation pattern** —— 定义输入输出格式
2. **Persona pattern** —— 定角色
3. **Template pattern** —— 描述任务

⭐⭐ **prompt 全文公开在 Figure 5.3，逐字抄录如下**（⭐ 这是本卡最可直接复用的一块）：

> **(part 1: Meta Language Creation)** "A bigram represents a segment of a business process model in the format "type:t1,name:n1 → type:t2,name:n2", where "type" indicates the node type, "name" indicates the node label, and "→" signifies the directed edge between two nodes."
>
> **(part 2: Persona)** "You are an expert in business process modeling."
>
> **(part 3: Template)** "I need your help to complete the following subprocess by adding the missing steps. Please ensure that the completion is as comprehensive as possible. The output must include both the provided incomplete part and your completion. Provide the output exclusively in bigram format, with no additional explanations or comments."
>
> `<incomplete subprocess>`

⭐⭐ **他们拒绝 CoT 的理由值得记**（⛔ 与我们的直觉相反）：

> "Chain-of-thought prompting [295], while effective for reasoning tasks, **would add unnecessary verbosity that could complicate the interpretation of the model's output**." —— §5.7，级别 **M(thesis)**

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| **有无循环** | ⛔⛔ **无** —— ⭐ 单次 zero-shot 调用，⛔ 无修订、无重试、无反馈回灌 | M(thesis) |
| **裁决者是谁** | ⭐ **确定性规则 + 相似度阈值**（⛔ 但它只在**事后评测**里当裁决者，⛔ **不参与运行时**——因为没有循环给它裁） | M(thesis) |
| **终止条件** | ⭐ 单次即止（⛔ 不适用） | M(thesis) |
| **最大轮数** | ⭐ **1** | M(thesis) |
| **有无报逐轮边际收益** | ⛔⛔ **无，因为没有轮** | M(thesis) |

⭐⭐ **这一格最重要的发现不是「没循环」，而是「⛔ 它撞上了一个必须靠循环解决的问题，然后选择了丢弃而不是修复」。**

⭐ 逐字（§5.5，RQ2 段）：

> "**not all outputs from LLMs conformed to our predefined bigram formatting.** The most frequent reasons for not conforming include adding extra, undefined key-value pairs (e.g., `condition:no`) or inserting redundant separator characters within bigrams, **rendering these outputs unprocessable by similarity-based tools.** This issue is potentially attributable to hallucinations in LLM outputs [29]. See the replication package [241] for the list of these non-conforming LLM completions. **Out of 3,361 slice completions from LLMs only 2,769 slices (GitHub: 1,352; SAP-SAM: 1,417) are parsable by both SAMOS and Apromore.**"

⭐ **算一下这个损耗**：$3{,}361 - 2{,}769 = 592$，即 ⭐ **17.6% 的 LLM 产出因为格式不合规被整例丢弃**（级别 **S**，由 M(thesis) 的两个数字直接相减）。

⛔⛔ **他们的处置是「丢弃」，⛔ 不是「原地重试 + 定向反馈」。** ⭐ 而他们自己在 §5.7 里明写了正确做法应该是什么：

> "While LLMs exhibit advanced coding capabilities, they do not always generate error-free outputs [156]. Our findings revealed instances of syntactic inconsistencies—such as incorrect formatting and extraneous key-value pairs—affecting the usability of LLM-generated completions. **This underscores the necessity of automated validation mechanisms to detect and correct such errors** before incorporating these recommendations into production BPMN models [156]."

⭐⭐ **对我们的直接意义**：⭐ 这正是本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §10 第 1 层（「节点内原地重试，把解析错误回灌」）在外部文献里的**空缺证据**——⭐ **一篇 TSE 论文因为没做这一层，白扔了 17.6% 的样本**，⛔ 并且在 Implications 里把它写成 future work。⭐ 我们的 `convert` 内部契约重试**净 +1118 条断言**那个数字，在这条对照下价值明确。

⚠️ **一个必须区分的点**：⭐ 原文确实有一处「迭代」，⛔ 但那是**设计期人工迭代 prompt**，⛔ 不是运行时循环：

> "**The prompt evolved iteratively as we experimented with different versions** to optimize the accuracy of the LLM's completion. For instance, in our initial attempts, the LLM produced irrelevant explanations alongside the intended completion. We refined the prompt to explicitly instruct the LLM to avoid such redundancy." —— §5.3.2，级别 **M(thesis)**

⭐ 即：**裁决者是人，循环发生在论文写作期，不在系统里。**

### B5 · ⭐ 中间表示

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| **有无** | ⭐ **有** —— ⭐ 「**简化 bigram 编码**」 | M(thesis) |
| **形态** | ⭐ 文本化图序列化格式：`type:t1,name:n1 → type:t2,name:n2` —— ⛔ **不是** DSL、⛔ 不是缺陷类型学、⛔ 不是谓词族、⛔ 不是 JSON schema | M(thesis) |
| ⭐ **是否闭合** | ⚠️ **混合，必须分开说**：⭐ **格式闭合**（一个固定的 pre-authored 模板）+ ⭐ **节点 type 词表闭合**（来自 BPMN 元模型：task / event / gateway）+ ⛔ **节点 name 完全开放**（自由生成） | S |
| ⭐ **谁定的** | ⭐ **预编**（人在设计期定），⛔ **不是 LLM 生成、⛔ 不是从目录里挑、⛔ 不是从语料归纳**。⭐ 来源有二：① SAMOS 自己的 n-gram 格式的简化版；② 受 Chaaben et al. 把活动图文本化的做法启发 | M(thesis) |
| ⭐ **谁选类** | ⛔⛔ **不适用——没有类可选。** ⭐ 这个 IR 是**序列化格式**，⛔ 不是**选择词表**；⭐ LLM 不做任何「从 N 个里挑一个」的动作 | S |

⭐⭐ **他们为什么不用 BPMN 官方 XML，⭐ 这段对我们选 DSL 直接相关，逐字抄下**：

> "Note that, our choice of a simplified bigram encoding for BPMN subprocesses in the prompt **instead of Object Management Group standard for BPMN serialization in XML format [203] is motivated by the poor performance of LLMs [193] when using the XML format. We iteratively identified that a simpler bigram format gives better results**, which is in line with evidence from literature [193]. **We hypothesize that the metadata in standard BPMN XML format, including custom tags, parameters, and formatting structures adds complexity and noise, which leads to poorer results from LLMs.** Validating the hypothesis and diving deeper into the reasons behind this phenomena is beyond the scope of this study." —— §5.3.2，级别 **M(thesis)**

⭐ 注意末句：⭐ **这是一条被明确标为「未验证的假设」的设计决定**，⛔ 不是被证明的结论。

⚠️ **对照我们「闭合 19 条 + LLM 自动选」**：⛔ **这篇给不出先例**——⭐ 它的 IR 里根本没有「选类」这个动作。⭐ 本卡在 B5 这一格对 M1 的贡献是**反面的**：⭐ 它说明「把 IR 做成序列化格式」和「把 IR 做成选择词表」是两种完全不同的东西，⛔ 而前者在 BPMN 圈子里更常见。

### B6 · 模型

| 模型 | 版本字符串（⭐ 原文逐字） | 级别 |
| :-- | :-- | :-: |
| OpenAI ChatGPT | ⭐ `GPT-4o` | M(thesis) |
| Google Gemini | ⭐ `gemini-1.5-pro-latest` | M(thesis) |

⭐ **有多模型对照：2 个 LLM。**

⚠️⚠️ **这一条按 schema 的口径必须打折**：⭐ 两个模型都是 **2024 年代**（`gemini-1.5-pro-latest` 尤其），⛔ 而论文 **2026-05 才正式发表**。⭐ 作者自己把这一点写进了 internal validity 威胁：

> "A threat to internal validity concerns the reproducibility of our experiment **due to the rapid advancements in LLMs**. The results in this study were obtained using a specific version and configuration of the LLMs. However, **as LLMs continue to evolve, conducting the same experiment with newer versions might yield different results.**" —— §5.8，级别 **M(thesis)**

⭐ 他们还明写没有领域专用模型：

> "To our knowledge, **there are no LLMs specifically specialized in the domain of process modeling**, and we did not conduct an analysis of other similar LLMs." —— §5.7，级别 **M(thesis)**

⛔ **原文未提供**：temperature / top-p / seed / 采样次数 / 是否多次重跑取均值。（⭐ 详见 C 节 `runs` 与 G 节。）

### B7 · ⭐ 确定性成分（⭐ 这套流水线的确定性含量很高）

| 环节 | 是什么 | 级别 |
| :-- | :-- | :-: |
| BPMN 解析 / 切片生成 | ⭐ **Camunda BPMN Model API**（开源 Java 库，⭐ 解析 / 创建 / 修改 BPMN 2.0 XML） | M(thesis) |
| 语言过滤 | ⭐ **Lingua** 开源语言检测库（⭐ 逐个 activity label 检测） | M(thesis) |
| 去重 | ⭐ **SAMOS 距离为 0**（⛔ 刻意不用哈希，⭐ 理由：哈希抓不到空白/大小写/格式差异） | M(thesis) |
| 相似度检索器 1 | ⭐ **SAMOS**：VSM + bigram（⭐ n=2 设定）+ 词频 + stemming / 同义词 | M(thesis) |
| 相似度检索器 2 | ⭐ **Apromore**：graph-edit distance + string-edit distance + **WordNet** 语言相似度 + connector 的 context similarity | M(thesis) |
| ⭐ 自建 parser | ⭐ **他们给 Apromore 加了一个 BPMN parser**（⛔ Apromore 原生只吃 EPC），⭐ 把 BPMN 的 task/event/gateway/sequence flow 映到 EPC 的 function/event/connector/arrow | M(thesis) |
| bigram → 图 | ⭐ 转换器（⭐ 见 Figure 5.6） | M(thesis) |
| ⭐ 判 meaningful | ⭐ **确定性阈值规则**（SAMOS 0.7 / Apromore GED 0.6 / 或「超过 per-case baseline」） | M(thesis) |
| 统计检验 | ⭐ **Spearman 相关系数** | M(thesis) |

⭐⭐ **但有一条必须点明，⛔ 否则会读错这张卡**：⭐ **上面全部确定性成分里，没有一个是 sound oracle。**

⭐ SAMOS 与 Apromore 是**相似度度量**，⛔ 不是正确性判定器：⭐ 它们回答「这两个子过程有多像」，⛔ **不回答「这个子过程对不对」**。⭐ Camunda API 只做**语法级** parse。⛔ **全流水线没有任何一处检查 LLM 产出的 BPMN 在语义上是否 well-formed**（⛔ 比如网关是否配平、是否可达、是否死锁）。

⭐ 作者自陈了这个缺口：

> "In this research, **we focused on the syntactic similarity** of recommendations to the ground truth. However, two subprocesses can be syntactically different yet semantically similar—meaning they may implement similar functionalities despite variations in elements, labeling, or structure. **Identifying semantic similarities in process models remains a challenging task [123]**, requiring further research in this area." —— §5.7，级别 **M(thesis)**

---

## C. 实验

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⭐⭐ **有，而且方向与我们相反**：⭐ **非 LLM 的传统相似度工具（SAMOS + Apromore）是 baseline，LLM 是被检验的新方法**。⛔ 无「LLM 朴素基线」 | M(thesis) |
| `dataset` | ⭐ **两个开源库**：① GitHub BPMN 数据集（⭐ 来自作者自己的 EMSE 2025 研究）；② **SAP-SAM**（SAP Signavio Academic Models，⭐ ≈1M 模型 / 103 CSV / 2011–2024，⭐ 其中 ≈634k 是 BPMN） | M(thesis) |
| `metrics` | ⭐ `Recall@1` · `Recall@10` · `MRR`（RQ1）；⭐ SAMOS 相似度分 + Apromore 相似度分 + 「meaningful」二值判定（RQ2） | M(thesis) |
| ⭐ `judged_by` | ⭐⭐ **全自动确定性脚本**（⛔ 无人工标注 · ⛔ 无 LLM-as-judge · ⛔ 无标注者间一致性 $\kappa$）——⚠️ **见下方 C2 的自证式验证隐患** | M(thesis) |
| `human_baseline` | ⛔⛔ **无**，⭐ 且作者把它列为**首要 construct validity 威胁** | M(thesis) |
| `runs` | ⚠️⚠️ **原文未提供** —— ⛔ 全文未出现跑几次、是否重复采样、方差、temperature、seed。⭐ 从「3,361 slices → 2,769 parsable」这一组固定数字看，**像是单次运行**（级别 **I**，⛔ 不得写成事实句） | I |
| ⭐ `adverse_results` | ⭐⭐ **见 C1，⭐ 这是本卡对我们最值钱的一节** | — |

### ⭐ C1 · ⭐⭐ 「Are LLMs the Answer?」——⭐ 答案是什么，⭐ 以及他们怎么写这个不利结果

⭐⭐ **答案：部分否定。** ⭐ 而且他们**没有把否定藏起来，⛔ 而是把它做成了标题、摘要首句和 contribution**。

⭐ **以下四段逐字抄录**（⭐ 全部同时出现在 thesis 与终版摘要，故级别 **M(pub)**，⭐ 是本卡最硬的一档）：

**① 摘要（⭐ 直接给否定，⛔ 但立刻加限定条件）**

> "Our results indicate that **LLMs might not be the answer always**, with process model similarity measuring tools **outperforming LLMs** in process recommendations for processes **with a maximum of 6 nodes**, with **three times more meaningful recommendation cases**. Our results also reveal that both LLMs and similarity tools perform most reliably when **≈60% of the complete process is given as input**. This study highlights the importance of **aligning recommendation techniques with available context, process size, and dataset characteristics**."

**② Introduction（⭐⭐ 这一段是全卡最值得学的写法：⭐ 先承认对方赢在哪一个指标上，⛔ 再说那个指标不等于结论）**

> "**LLMs generated recommendations that are more similar to the expected outputs than traditional similarity-based methods in at least 65% of recommendation cases. However, this does not always lead to more meaningful recommendations by LLMs than similarity tools.** Cumulatively, similarity-based tools provided meaningful recommendations **at least three times more often** than LLMs for subprocesses with up to six nodes. In contrast, **for larger subprocesses, LLMs generated nearly twice as many meaningful recommendations** as similarity-based tools. Both approaches show their most reliable performance on subprocesses with around 6 to 12 nodes."

**③ Introduction 末段（⭐ 把不利结果重构成「对实践者的选型指南」）**

> "Our study highlights the importance of selecting recommendation approaches based on the available context and process size and **could be a precursor to practitioners on when to choose what kind of recommenders and cautioning that LLMs are not always the best answer.** This study forms a starting step on avenues that require further research such as impact of effective prompting and data quality on building recommenders and **reiterates the need for validation mechanisms**"

**④ RQ2 答案框（⭐ 用同一组数据同时给出「谁赢」和「在哪赢」，⛔ 不给单一总分）**

> "Traditional similarity tools are better when subprocesses contain up to 6 nodes, while LLMs are more effective for larger ones. This is evidenced by **242 meaningful recommendations by SAMOS compared to 77 by ChatGPT, out of 924 cases in ≤Q1 dataset partitions**, and **679 meaningful recommendations by ChatGPT, as compared to 401 by SAMOS, out of 1,845 within IQR and >Q3 dataset partitions**, when the highest number of meaningful recommendations by a similarity measure is considered."

⭐⭐ **⭐ 拆解他们的四个修辞动作**（⭐ 这四条我们写 −15.82pp 可以逐条对表）：

| # | 动作 | 具体怎么做的 | ⭐ 我们能不能照搬 |
| :-: | :-- | :-- | :-- |
| **1** | ⭐ **把否定写进标题，做成问句** | `Are LLMs the Answer?` —— ⭐ 标题先立问，⛔ 答案「不总是」就不再是打脸，⭐ 而是**论文回答了自己提的问题** | ⭐ **能，且成本极低**。⭐ 我们的 −15.82pp 若配一个「Does a Multi-Stage Assertion Pipeline Beat a Single Prompt?」式标题，⛔ 不利结果立刻从「失败」变成「结论」 |
| **2** | ⭐⭐ **切分维度，让否定变成条件式** | ⛔ 不报「LLM 输了」，⭐ 而报「**≤6 节点输 3.1×，>6 节点赢 1.7×**」——⭐ 用 quartile 分区把单一胜负拆成 regime | ⭐ **能，而且这是最该学的一条**。⭐ 我们已有 pair 维度、模型维度、`hit@1/@3/@all` 三口径；⛔ **缺的是一条「在哪一类样本上我方反超」的切分** |
| **3** | ⭐ **承认对方赢的那个指标，然后区分「相似」与「有用」** | ⭐ 「LLM 在 ≥65% 的例子里更像 ground truth，**但更像不等于更 meaningful**」——⭐ 靠一个**独立定义的 meaningful 判据**把两件事分开 | ⭐ **能**。⭐ 对我们即：⛔ 承认朴素基线 `hit@1` 更高，⭐ 同时给出一个朴素基线做不到的维度（可机械求值 / 可归因 / 可复算） |
| **4** | ⭐ **把不利结果转成选型建议与 future work** | ⭐ "could be a precursor to practitioners on when to choose what kind of recommenders" + ⭐ 提出 RAG 混合是「arguably one of the most promising directions」 | ⭐ **能，但要小心**。⚠️ 照本仓库 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9 的方向性松紧纪律，⛔ 不能只在「唯一能止损那处」写满前景 |

⭐⭐ **⭐ 还有第五个动作，⚠️ 这个是我们应当警惕而非照搬的**：

⭐ 他们对 90% 切片时 LLM 性能下降这个不利现象，给了一段**可能替 LLM 开脱的替代解释**：

> "**It's also possible that the decline in performance might not be entirely due to an inherent limitation of LLMs. A prompt that invokes domain knowledge could enhance the LLM's ability to generate the correct completion.**" —— §5.6，级别 **M(thesis)**

⚠️ ⭐ 这句在学术上是诚实的（⭐ 它标了 "possible"、⭐ 并说 "this hypothesis needs further investigation to validate"），⛔ **但它没有任何数据支持**。⭐ 我们写 −15.82pp 时若写「换个 prompt 也许就好了」，⛔ **必须配一次实测**，⛔ 否则那是自我开脱而非限定。

### ⭐ C2 · ⭐ 分母怎么定的（⭐ 六段漏斗，⭐ 每一步都有数字——⭐ 这一节的做法直接可搬）

⭐⭐ **他们把样本损耗写成一条完整的、每步带数字的漏斗，⛔ 一步都没有藏。** ⭐ 级别全部 **M(thesis)**。

| 步骤 | GitHub | SAP-SAM | 合计 | 剔除理由（⭐ 原文明写） |
| :-- | --: | --: | --: | :-- |
| 起始模型数 | 7,331 | 16,593 | — | ⭐ GitHub 全量；⭐ SAP-SAM 按 CSV 分层抽样 ≈10%（⭐ 从 165,929 个含 `subprocess` 的模型中） |
| 原始子过程 | 8,392 | 2,421 | 10,813 | — |
| ⛔ 剔 < 3 flow node | 7,052 | 2,172 | — | ⭐ "we expect minimal context"，⭐ < 2 非起止节点即视为 trivial |
| ⛔ 剔非英文 | 5,063 | 1,656 | — | ⭐ Lingua 逐 label 检测；⭐ 剔掉 1,989 / 516 条 |
| ⛔ 剔全标签 < 3 字符 | 4,194 | 1,603 | — | ⭐ "meaningful activity labels cannot consist of only two letters"；⭐ 剔 869 / 53 |
| ⛔ 剔重复 | **967** | **1,490** | **2,457** | ⭐ SAMOS 距离 = 0；⛔ 刻意不用哈希 |
| ⚠️ **BPMN Model API 支持** | 782 | 725 | **1,507** | ⚠️ **只有 1,507/2,457（61.3%）能被切片工具处理** |
| 切片产出 | — | — | **5,383** | ⭐ 30%: 888 · 50%: 1,481 · 70%: 1,507 · 90%: 1,507 |
| ⚠️ **两个相似度工具都能解析** | 1,617 | 1,744 | **3,361** | ⚠️ **5,383 → 3,361，损耗 37.6%** |
| ⛔ **LLM 产出可解析** | 1,352 | 1,417 | **2,769** | ⛔ **17.6% 格式不合规被丢**（见 B4） |

⭐⭐ **⭐ 分区口径**：⭐ 按子过程节点数的**四分位数**切三档 `≤Q1` / `IQR` / `>Q3`。⭐ 实测阈值（⭐ Figure 5.5，⭐ 本卡从 PDF 的 glyph 编码逐字解出并与正文「median 7 和 8」交叉验证过）：

| 数据集 | Q1 | median | Q3 |
| :-- | --: | --: | --: |
| GitHub | 5 | **7** | 10 |
| SAP-SAM | 6 | **8** | 12 |

⭐ 所以摘要里的「maximum of 6 nodes」= 两个数据集 Q1 的较大者；⭐ 「around 6 to 12 nodes」= IQR 跨两库的并集。⭐ **口径自洽。**

⭐ 他们给了选四分位数的理由：

> "We chose quartile-based splitting because **it adapts to the dataset's distribution**, enabling a more systematic evaluation of recommender performance across subprocess sizes while capturing differences in complexity." —— §5.5，级别 **M(thesis)**

⭐ **切片档位 30 / 50 / 70 / 90%，也给了理由**：

> "The choice of starting at 30% and 20% increments are **motivated by having at least two nodes in the input subprocess** and to have a common, yet quantized and incremental input size (of at least one node) across the dataset for a uniform comparison. **Both of these values are derived based on the median size of subprocesses, 7 and 8**" —— §5.5，级别 **M(thesis)**

### ⭐ C3 · ⭐⭐ 「meaningful」的判据（⭐ 有一条我们该直接偷的设计）

⭐ 三层判据，级别全部 **M(thesis)**：

**第一层 · 定义**

> "we consider a recommendation to be **meaningful** if the recommended subprocess **resembles the ground truth, allowing for structural differences**, e.g., additions or deletions of elements, or variations in labeling and layout. This is commonly referred to as **approximate clones [74]**."

**第二层 · 阈值（⭐ 外部出处，⛔ 不是自定）**

> "Although there is **no universally accepted threshold** in the literature for defining approximate clones, studies using each tool typically adopt specific similarity thresholds. **For SAMOS, a threshold of 0.7** is commonly used in related studies [22,237]. For studies employing the GED technique [86,160]—the same technique used by the Apromore similarity tool—**a similarity threshold of 0.6** is a common one."

**第三层 · ⭐⭐ per-case baseline（⭐⭐ 这一条是本卡最该搬的单点设计）**

> "However, **we apply this quality measure only to slice sizes where the baseline similarity falls below the threshold** for an approximate clone. **We define the baseline as the similarity between the given slice and the ground truth subprocess.** In cases where the baseline exceeds this threshold, we define a recommendation as meaningful **if the similarity between the recommended subprocess and the ground truth surpasses the baseline.** For instance, if the baseline similarity score produced by SAMOS for a slice is 0.75 (the approximate clone threshold for SAMOS is 0.7), a completion is considered "meaningful" only if the similarity score produced by SAMOS for the completion is **more than 0.75**."

⭐⭐ **⭐ 翻译成一句话：⭐ 每一例的达标线不是固定阈值，⭐ 而是「⭐ 输入本身已经达到的水平」。** ⛔ 推荐必须**比你手里已经有的东西更好**才算数。

⚠️ **为什么这条对我们重要**：⭐ 我们的 `hit@k` 分母是台账条目数，⛔ 但**没有一条 per-case 的「不做也能拿到多少」的地板**。⭐ 一个模型缺陷若极其显然（⛔ 朴素读一遍就能看出），⭐ 我方发现它与朴素基线发现它**在当前口径下同权**。⭐ 引入 per-case 地板会让「⭐ 只有我方能发现的那些条目」单独显形——⭐ 而那恰好是 −15.82pp 之下我们唯一可能反超的地方。

⭐ **另有一条严格性口径值得记**（RQ1 侧）：

> "**We count a recommendation as correct only if it exactly matches the ground truth.**" / "**We take a conservative approach and do not consider partially correct recommendations as valid**, but rather consider only the predictions of the entire ground truth for the calculation of the metrics."

### ⭐ C4 · ⚠️⚠️ 自证式验证隐患，⭐ 以及他们的缓解办法（⭐ 这条按本仓库 §3.5 第 5 项该查，⭐ 结论是**他们做了缓解**）

⚠️ **隐患**：⭐ SAMOS 与 Apromore ⭐ **既是被评测的推荐器（RQ1/RQ2 的一方），⛔ 又是给 LLM 产出打分的裁判**。⛔ 裁判和选手是同一个人。

⭐ **他们的缓解，逐字**：

> "For the same set of data items, we run the recommendation pipeline (see Figure 5.6) using both LLMs and traditional similarity tools. We then compare the completions provided by the LLMs and similarity tools. **To minimize bias, we use both SAMOS and Apromore similarity measures to compare the completions by the LLMs to the ground truth data.**" —— §5.5，级别 **M(thesis)**

⭐ **并且在结果里贯彻到底**：⭐ 全文**每一个 LLM 数字都同时给两份**（⭐ 「at least … (Apromore score) and at most … (SAMOS score)」），⛔ **从不合并成单一数字**。⭐ 例：

> "ChatGPT provided **at least 601** meaningful recommendations (Apromore score - GitHub: 267, SAP-SAM: 334) and **at most 751** (SAMOS score - GitHub: 299, SAP-SAM: 452) out of 2,769 recommendation cases"

⭐⭐ **⭐ 这是一个可直接复用的纪律**：⭐ **当你的裁判同时是你的竞争对手时，⭐ 报双裁判、⛔ 永不合并成单一数字，⭐ 并把结论写成区间（at least / at most）。**

### ⭐ C5 · 统计检验

⭐ **有，但只有一处，⛔ 且不是用来比较两种方法的。**

⭐ **Spearman 秩相关系数**，检验「上下文量 ↔ ground truth 排到前面的可能性」（级别 **M(thesis)**）：

| 数据集 | Apromore | SAMOS |
| :-- | --: | --: |
| GitHub | ≈0.79 | ≈0.89 |
| SAP-SAM | ≈0.84 | ≈0.87 |

⛔⛔ **原文未提供**：⛔ LLM vs 相似度工具的差异**没有做显著性检验**（⛔ 无 $p$ 值、⛔ 无 Wilcoxon / Mann-Whitney、⛔ 无效应量、⛔ 无置信区间）。⭐ 「3×」与「≈2×」都是**原始计数比**。

⚠️ ⭐ 方法论层面他们自称做的是 design science 的 "**statistical difference-making experiment**"（Wieringa 口径），⛔ 但落地只到了描述统计 + 一个相关系数。⭐ 这是一篇 TSE 论文的实际严谨度上限，⭐ **对我们是个有用的校准点**：⛔ 我们不必为 −15.82pp 补一套显著性检验才敢投——⭐ 但反过来，⭐ 补了就是加分项。

### ⭐ C6 · 主要结果表（RQ1，⭐ Table 5.2 逐字）

| tool | dataset | count | recall@1 | recall@10 | MRR |
| :-- | :-- | --: | --: | --: | --: |
| SAMOS | GitHub | 1,617 | **0.76** | **0.95** | **0.83** |
| SAMOS | SAP-SAM | 1,744 | 0.71 | 0.88 | 0.77 |
| Apromore | GitHub | 1,617 | 0.45 | 0.67 | 0.52 |
| Apromore | SAP-SAM | 1,744 | 0.54 | 0.81 | 0.63 |

⭐ **RQ2 汇总（2,769 例分母）**：

| 推荐器 | meaningful 数 | 口径 |
| :-- | :-- | :-- |
| Apromore | 377 | 单一（自己的分） |
| SAMOS | 643 | 单一（自己的分） |
| ⭐ ChatGPT (GPT-4o) | ⭐ **601 – 751** | ⭐ 双裁判区间 |
| Gemini 1.5 Pro | 455 – 531 | ⭐ 双裁判区间 |

⭐ **两个工具的一致率**（⭐ 顺带就是一条「无人工标注时怎么报可靠性」的做法）：⭐ GitHub recall@1 ≈65%（1,048/1,617）· recall@10 ≈71%；⭐ SAP-SAM recall@1 ≈72% · recall@10 ≈83%。

⭐ **exact match（⭐ LLM 偶尔真能命中）**：⭐ GitHub 上 ChatGPT 18/1,352 被两个工具都判为完全一致，⭐ 其中 **16 例出现在 90% 切片**；⭐ SAP-SAM 上 Gemini 11 例，⭐ **全部**在 90% 切片且全在 IQR 分区。

---

## D. ⭐ 资产（⛔ 全部本轮实际取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据（⭐ 逐字贴机械输出） |
| :-- | :-: | :-- | :-- |
| 论文全文（**终版**） | ⛔ **🔒** | [10.1109/TSE.2026.3690186](https://doi.org/10.1109/TSE.2026.3690186) | ⭐ Unpaywall：`is_oa: True` ⛔ 但 `best_oa_location` 指向 WUR **landing page**，`url_for_pdf: None`，`evidence: deprecated`。⭐ 实取 WUR 页：⛔ **无任何 PDF 文件，只有 DOI 链接**。⭐ IEEE Xplore 返回 HTTP 202 + JS 壳 |
| ⭐ 论文全文（**开放前置版**） | ⭐ **🟢** | [TU/e Pure 论文 PDF](https://pure.tue.nl/ws/files/369623105/20251113_Saeedi_Nikoo_hf.pdf) | ⭐ `HTTP=200 SIZE=24185921 TYPE=application/pdf` · ⭐ 199 页 · ⭐ Chapter 5 = 本文（pp. 126–162）· ⚠️ **`research.tue.nl` 同一文件返回 403（Cloudflare「Just a moment」），⛔ 必须用 `pure.tue.nl` 域** |
| ⭐ **实验代码 + 数据（复现包）** | ⭐ **🟢** | [10.5281/zenodo.15110021](https://doi.org/10.5281/zenodo.15110021) | ⭐ Zenodo API：⭐ 1 个文件 `replication package.zip` · ⭐ **1,803,858,439 bytes（1.80 GB）** · ⭐ `md5:ef71378bb0a161c4d425877306e335d1` · ⭐ **license `cc-by-4.0`** · ⭐ date 2025-03-30 · ⭐ 描述中逐字写有终版 `doi: 10.1109/TSE.2026.3690186, May 2026`。⭐ 文件端点 HEAD = `HTTP 200`、`content-length: 1803858439`（⭐ 与元数据一致）。⚠️ **Range 请求被 Zenodo 限流拦（403「unusual traffic from your network」），⛔ 故未能列出 zip 内部条目** |
| ⭐ **数据集 / Benchmark** | ⭐ **🟢** | ① [10.5281/zenodo.13955920](https://doi.org/10.5281/zenodo.13955920)（GitHub BPMN 库）② SAP-SAM（第三方公开） | ⭐ ①：Zenodo API 实取，1 文件 zip **395,658,045 bytes**，`cc-by-4.0`，2024-10-19。⭐ ②：原文引 [257]，⛔ 本轮未单独核 SAP-SAM 入口。⭐ **ground truth 有**：ground truth = 完整子过程本身（⭐ 由切片构造，⛔ 无需人工标注） |
| 实验结果细则 | ⭐ **🟡** | 复现包内 | ⭐ 论文内有 Table 5.2 / 5.4 汇总 + 8 张分布图；⭐ 原文明写不合规 LLM 产出清单在包里（"See the replication package [241] for the list of these non-conforming LLM completions"）。⚠️ ⛔ **但逐条结果是否在包里，本轮因限流未能确认** → ⛔ 故不判 🟢 |
| Artifact / 复现包 DOI | ⭐ **🟢** | ⭐ Zenodo DOI，⭐ CC-BY-4.0 | ⭐ 同上 |
| ⭐ **prompt 是否公开** | ⭐⭐ **🟢** | ⭐ **论文正文 Figure 5.3，全文逐字** | ⭐ 本卡 B3 已完整抄录三段。⭐ ⛔ **这是本轮少见的「prompt 完整可见」条目** |

### ⭐ 终裁说明

⭐ **代码 / 数据 / prompt 三项全 🟢，⭐ 这在本轨里属于上游水平。** ⛔ **唯一取不到的是终版论文本身**——⭐ 而这一项被开放前置版基本补齐（⚠️ 代价是版本风险，见开头版本声明）。

⚠️ ⭐ 关于复现包判 🟢ⓘ 的理由说明：⭐ 按简报里 FlowFSM 那条教训，「仓库存在 ≠ 🟢」。⭐ 本项判 🟢 的依据**不是链接存在**，⭐ 而是：⭐ ① 元数据给出 **1.80 GB** 的实体大小与 md5；⭐ ② 文件端点 HEAD 实返 200 且 content-length 与元数据**逐字节一致**；⭐ ③ CC-BY-4.0 明确可用。⛔ **空壳不可能有 1.8 GB。** ⚠️ 但**「取到的够不够复现」本轮无法判定**，⛔ 因为限流挡住了内容列举。

---

## E. ⭐ 对 M1 的意义

### 1. ⭐ 可取之处（⭐ 具体到能搬的设计决定）

| # | 能搬的东西 | ⭐ 怎么搬 |
| :-: | :-- | :-- |
| **1** | ⭐⭐ **per-case baseline 判据**（C3 第三层） | ⭐ **本卡最高价值的单点。** ⭐ 给每一条台账条目定一条「不用我们这套流水线、朴素读一遍能不能拿到」的地板，⭐ 只把**超过地板**的算作我方增益。⭐ 这会让 −15.82pp 之下「只有我方能发现」的那部分单独显形 |
| **2** | ⭐⭐ **双裁判 + 区间报数**（C4） | ⭐ 当裁判与选手身份重叠时，⭐ **报两份分、写成 at least / at most、⛔ 永不合并**。⭐ 我们的 `adjudicate_results` 是 LLM 自评，⛔ 而被判的对象也是 LLM 产出——⭐ 同构隐患，⭐ 这条纪律直接适用 |
| **3** | ⭐⭐ **切分维度让否定变条件式**（C1 动作 2） | ⭐ 我们目前只有 pair / 模型 / `@k` 三个维度，⛔ **缺一条按「样本难度」的切分**。⭐ 他们用节点数四分位数；⭐ 我们可用（模型规模 / 缺陷显著度 / 需求 kind）——⭐ 目标是找到「我方反超」的那个 regime |
| **4** | ⭐ **六段漏斗式分母披露**（C2） | ⭐ 每一步剔除都给数字 + 理由 + 剩余量。⭐ 我们已有 `00x8` 排除与 98 条能力分母的裁定，⭐ 但**没有做成一张连续漏斗表**。⭐ 做一张，成本低、防守力强 |
| **5** | ⭐ **格式选择的诚实处理** | ⭐ 他们选简化 bigram 而非 BPMN XML，⭐ 并把理由标为**未验证的假设**（B5 末句）。⭐ 我们选 pyfcstm DSL 的理由也应这样标 |
| **6** | ⭐ **阈值一律引外部出处** | ⭐ SAMOS 0.7 / GED 0.6 都挂了既有文献，⭐ 并明说「no universally accepted threshold」。⭐ 与我们 [provenance/](../../provenance/) 的三类分级同一路数 |

### 2. ⛔ 不可取 / 陷阱（⭐ 它踩了我们已经踩过或正要踩的哪些坑）

| # | 坑 | ⭐ 对照我们 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **schema 不合规就整例丢弃，⛔ 不重试不反馈** —— ⭐ 白扔 **17.6%（592/3,361）** 的 LLM 产出，⭐ 然后把「automated validation mechanisms」写进 future work | ⭐⭐ **这正是本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §10 第 1 层的外部空缺证据。** ⭐ 我们的 `convert` 内部契约重试净 +1118 条断言，⭐ 在这条对照下**价值可量化陈述**。⛔ 而且注意：⭐ 被丢掉的那 592 例极可能不是随机分布的（⭐ 越复杂的子过程越容易产出 `condition:no` 这类多余键值），⛔ **这构成一个未被讨论的选择偏差** |
| **2** | ⛔ **全流水线没有 sound oracle**（B7 末） | ⭐ 相似度度量 ≠ 正确性判定器。⛔ 他们的 BPMN 产出**从未被检查是否 well-formed**（⛔ 网关配平 / 可达性 / 死锁一概不查）。⭐ **我们有 pyfcstm，这是我方真实优势**；⛔ 但 M1 第二条原则要动的是「把它从求值端搬到裁决端」——⭐ 本篇给不出这方面的先例，⭐ 只给出「不做会怎样」 |
| **3** | ⛔ **无人工基线、⛔ 无人工判定、⛔ 无 $\kappa$** | ⭐ 判定 100% 自动。⭐ 好处是可复算，⛔ 代价是「meaningful」是否真的对建模者有用**完全没有验证**——⭐ 作者自己列为首要 construct validity 威胁。⚠️ ⭐ **反向提醒我们**：⭐ 我们 574 位人工逐位判定是**成本极高但对方普遍没有**的东西，⭐ 应当在论文里当作方法论强项写，⛔ 而不是只当成开销 |
| **4** | ⚠️ **单次运行（推测）、⛔ 无方差、⛔ 无 temperature/seed** | ⭐ 级别 **I**。⛔ 若确为单次，则 LLM 那一侧的所有数字**没有稳定性估计**。⭐ 我们的 `hit@1/@3/@all` 三口径在这一点上**严格更强**，⭐ 这是可以明说的差异 |
| **5** | ⚠️ **模型代次落后两年** | ⭐ GPT-4o + gemini-1.5-pro 做实验，⭐ 2026-05 发表。⭐ 按 X1 的实测（⭐ SOTA 与上一代不是一个量级），⛔ 其「LLM 在小子过程上输 3×」这个结论**对当代模型的适用性未知**。⛔ **我们引用它时必须带上这个限定**，⛔ 不能拿它当「LLM 就是不行」的证据 |
| **6** | ⚠️ **无显著性检验** | ⭐ 「3×」「≈2×」都是原始计数比。⛔ 一篇 TSE 论文尚且如此——⭐ 这是有用的**期望值校准**，⛔ 但不构成我们也可以不做的许可 |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么它的做法不能直接照搬）

| 维度 | ⭐ 他们 | ⭐ 我们 | ⛔ 为什么不能直接搬 |
| :-- | :-- | :-- | :-- |
| **任务** | ⭐ **补全 / 推荐**（⭐ 生成缺失部分） | ⭐ **缺陷检测**（⭐ 判断已有模型对不对） | ⛔⛔ **根本差别。** ⭐ 补全任务有一个**天然的 ground truth**（⭐ 被切掉的那部分），⭐ 所以判定可以纯自动、可以用相似度当代理。⭐ 缺陷检测**没有这种结构**——⛔ 「这个模型有什么问题」的 ground truth 必须人工建。⭐ **这解释了为什么我们必须付 574 位人工判定，⛔ 而他们不用** |
| **判定装置** | ⭐ 相似度 + 阈值（⭐ 确定性但**近似**） | ⭐ 人工逐位 + pyfcstm 求值（⭐ 确定性且**精确**） | ⭐ 他们的自动判定**不可迁移**到我们的任务；⛔ 反之我们的人工判定他们不需要 |
| **粒度单位** | ⭐ **`subprocess`**（⭐ BPMN 记法自带的元素） | ⭐ **「一条需求 × 这份模型」** | ⭐ 详见 F1：⛔ 他们的粒度是**记法白送的**，⭐ 我们的粒度是**自己构造的**。⭐ 这意味着我们**必须论证**粒度选择，⛔ 而他们可以不论证 |
| **LLM 占比** | ⭐ 1/7 阶段 | ⭐ 5/10 节点 | ⭐ 他们的流水线**确定性含量高得多**。⛔ 若 M1 要减少 LLM 阶段，⭐ 本篇是一个「LLM 只用一次也能出 TSE」的存在性证明 |
| **循环** | ⛔ **无** | ⭐ 有（⛔ 且实测两个 LLM 自评 reviewer 零收益） | ⭐ 本篇**给不出「循环该怎么做」的正面先例**；⭐ 它只提供「不做循环的代价 = 17.6% 样本损耗」这个数字 |
| **不利结果的位置** | ⭐ **标题 + 摘要首句 + contribution** | ⛔ 目前是主结果的负号 | ⭐⭐ **这是可以立刻照搬的**（⭐ C1 四个动作） |

---

## F. ⛔ 用户必答问题的逐条回答

### ⭐ F1 · ⭐⭐ 「片段」是怎么定义与切分的？粒度怎么定的？⭐ 为什么选这个粒度（⭐ 有没有给理由）？

⭐⭐ **定义：⭐ 「片段」= BPMN 标准里的 `subprocess` 元素，⛔ 不是任意子图。** ⭐ 级别 **M(thesis)**，⭐ 脚注 6 逐字：

> "**A type of activity that represents a set of related activities within a larger business process [203]**."（⭐ [203] = OMG BPMN 标准）

⭐ **切分怎么做的（⛔ 注意：这里有两个不同的「切」，⛔ 不要混）**：

| 「切」 | 做什么 | 怎么做 |
| :-- | :-- | :-- |
| **① 取片段** | ⭐ 从完整 BPMN 模型里**取出**子过程 | ⛔ **不切**——⭐ 直接在模型文件里搜关键词 `subprocess`，⭐ 因为「BPMN standard notation uses the term for annotating subprocess element」。⭐ **粒度是记法白送的** |
| **② 造残缺输入** | ⭐ 把完整子过程**削成**残缺形态 | ⭐ **深度优先遍历**：先沿一条从 start 到 end 的路径加节点，⭐ 再补其它路径，⭐ 直到覆盖全部节点。⭐ 取 30/50/70/90% 四个快照。⭐ 工具 = Camunda BPMN Model API |

⭐ ② 的逐字（§5.5）：

> "In our simulation of the step-wise subprocess development, **we adopt a depth-first traversal approach.** Initially, nodes along a single path, starting from a start node and progressing until an end node is reached, are incorporated into the process. Subsequently, additional nodes are appended to complete other paths within the subprocess, until all nodes from the ground truth subprocess are covered."

⭐⭐ **⭐ 为什么选这个粒度 —— ⭐ 给了理由，⭐ 而且是三条，⛔ 都在 §5.1**（级别 **M(thesis)**）：

**理由 1 · ⭐ 建模者自己更想要片段（⭐ 引了实证文献）**

> "**a majority of business process modelers prefer the recommendation of a complete fragment of a process over individual activity [94].**"

**理由 2 · ⭐⭐ 单节点粒度在结构上不够用（⭐ 这条最硬）**

> "Recommender systems for business process modeling predominantly focus on **activity recommendation**, which aims to propose a label for an atomic task activity. **They do not cover other crucial elements in a business process model such as events and gateways, which are required for modeling most of the real-world processes.** … **The lack of support for the three kinds of flow objects (events, activities, gateways) by recommenders, makes them unsuitable for recommendation of process fragments.**"

⭐ 并且他们**预先反驳了「单节点重复 N 次不就等于片段吗」**（§5.9.1）：

> "One may argue that if we repeat running single node recommenders for enough number of steps, we could produce the desired subprocesses. However, note that such approaches **mostly recommend task or event nodes** in business process models, **while missing other nodes such as gateways**. Also, when multiple nodes are involved in a subprocess, **receiving a recommendation as a complete subprocess is more desirable than building it step-by-step.** Additionally, since the next node recommendation depends on the existing context of the incomplete subprocess and the modeler's choices, **it is likely that the final result will be a subprocess that combines nodes from various similar subprocesses, rather than the intended ground truth subprocess.**"

**理由 3 · ⭐ 类比代码片段推荐**

> "The parallel problem in the programming languages domain is **code snippet recommendation**, which has been widely explored. Similar to code snippet recommendation, we focus on recommending parts of a process that are **coherent and logically grouped together**, known as a subprocess."

⚠️⚠️ **⭐ 但这里有一条对我们极重要的自陈：⭐ 他们承认这个粒度是「⛔ 记法给的，⭐ 不是最优的」，⭐ 并把更灵活的粒度列为 future work**（§5.10，级别 **M(thesis)**）：

> "First, we plan to extend the existing recommenders or develop recommenders that **extend the scope of model fragmentation to include techniques such as SESE decomposition, which may provide more flexible and effective fragment recommendations.**"

⭐ **SESE = single-entry-single-exit**，⭐ 即图论意义上的结构化区域分解。

⭐⭐ **⭐ 对我们的意义（⭐ 这是 F1 的落点）**：

⭐ 两者都在做「⭐ 比整模型细、⛔ 比单元素粗」的粒度选择，⛔ **但正当性来源完全不同**：

| | ⭐ 他们（`subprocess`） | ⭐ 我们（「一条需求 × 这份模型」） |
| :-- | :-- | :-- |
| ⭐ 粒度从哪来 | ⭐ **BPMN 标准自带的元素** —— ⭐ 有 OMG 标准背书，⛔ 不需要论证「为什么按这个切」 | ⭐ **我们自己构造的判定单位** —— ⛔ **没有任何标准背书** |
| ⭐ 论证负担 | ⭐ 轻：⛔ 只需论证「为什么不用更细的单节点」 | ⭐⭐ **重：⛔ 必须论证「为什么按需求条切、⛔ 而不是按状态/迁移/元素切」** |
| ⭐ ground truth 从哪来 | ⭐ **切片自动构造**（⭐ 削掉的部分就是答案） | ⭐ **人工建台账** |
| ⭐ 自陈局限 | ⭐ **明说记法粒度不够灵活，⭐ 指向 SESE** | ⭐ 待定 |

⭐⭐ **可直接借用的一条论证结构**：⭐ 他们论证粒度的方式**不是**说「我们的粒度好」，⛔ 而是**说「更细的那个粒度在结构上漏东西」**（⭐ 漏 gateway 与 event）。⭐ 我们论证「一条需求 × 这份模型」时可以照这个形状走：⛔ **更细的粒度（单元素/单迁移）漏掉的是「跨元素的需求语义」**——⭐ 一条需求往往同时约束多个元素，⛔ 按元素切会把它撕碎。⭐ 这个论证在我们这边同样成立，⭐ 而且比「我们的粒度更自然」有力得多。

### ⭐ F2 · ⭐⭐ 实验设计与指标口径（⭐ TSE 级别的严谨度）

⭐ **逐条对表**（⭐ 详细展开见 C1–C6）：

| 问题 | 答案 | 级别 |
| :-- | :-- | :-: |
| **baseline 是什么** | ⭐⭐ **传统相似度工具 SAMOS + Apromore（⛔ 非 LLM）当 baseline，⭐ LLM 是被检验方**。⛔ **方向与我们相反**（⭐ 我们是 LLM 流水线 vs LLM 朴素基线） | M(thesis) |
| **分母怎么定的** | ⭐⭐ **六段漏斗，每步带数字**：10,813 → 2,457 → 1,507 → 5,383 slices → 3,361 → **2,769**。⭐ 主结果分母 = **2,769**（RQ2）/ **3,361**（RQ1，分 1,617 + 1,744 两库独立） | M(thesis) |
| **有没有多轮 / `@k` 口径** | ⚠️⚠️ **有 `@k`，⛔ 但它不是我们那个 `@k`！** ⭐ 他们的 `Recall@1` / `Recall@10` 是**同一次运行内排序列表的前 k 名**；⛔ 我们的 `hit@3` / `hit@all` 是**重复采样 3 轮的跨轮聚合**。⛔ **两者回答完全不同的问题**：⭐ 他们的 @k 测「排序质量」，⭐ 我们的 @k 测「稳定性」。⛔ **本文没有任何跨轮口径** | M(thesis) + S |
| **判定谁做的** | ⭐ **全自动确定性脚本**（⭐ SAMOS + Apromore 相似度 + 三层阈值规则）。⛔ **无人工标注 · ⛔ 无 LLM-as-judge** | M(thesis) |
| **有无标注者间一致性** | ⛔ **无 $\kappa$**（⛔ 没有人类标注者，⭐ 故不适用）。⭐ **但有一个等价物**：⭐ 两个相似度工具的**一致率**（⭐ GitHub recall@1 ≈65%、recall@10 ≈71%；⭐ SAP-SAM ≈72% / ≈83%）—— ⭐ 这可以看成「两个自动裁判之间的一致性」 | M(thesis) |
| **有没有人类基线** | ⛔⛔ **无。** ⭐ 且作者把它列为**首要 construct validity 威胁**，⭐ 逐字："The primary threat to construct validity stems from the use of a **simulated setting** to evaluate our approach, **rather than conducting a user study with real participants**." | M(thesis) |
| **有没有统计显著性检验** | ⚠️ **只有 Spearman 相关（0.79–0.89），⛔ 用来验「上下文量 ↔ 命中」这一条假设。** ⛔⛔ **LLM vs 相似度工具的比较没有做任何显著性检验**：⛔ 无 $p$ 值、⛔ 无非参检验、⛔ 无效应量、⛔ 无置信区间。⭐ 「3×」「≈2×」是原始计数比 | M(thesis) |
| **跑几次 / 有无方差** | ⚠️ **原文未提供**（⛔ 无 runs / temperature / seed / 重复采样）。⭐ 从固定计数看**像单次**（级别 **I**） | I |

⭐⭐ **⭐ 一条对我们特别有利的观察**：⭐ 一篇 TSE 论文在「多轮稳定性」这一格上是**空的**——⛔ 没有重复采样、没有方差、没有跨轮口径。⭐ 而我们的 `hit@1 / hit@3 / hit@all` 三口径同时报是**严格更强的做法**。⭐ 这可以在论文里当作方法论贡献明说，⛔ 而不只是内部纪律。

### ⭐ F3 · ⭐⭐ 「Are LLMs the Answer?」——⭐ 答案是什么？⭐ 不利结果怎么写的？

⭐⭐ **答案：⭐ 「不总是」——⭐ 一个按规模切分的条件式答案。**

⭐ **一句话版本**：⭐ ≤6 节点的子过程上，⭐ **传统非 LLM 工具赢 3.1×**（⭐ SAMOS 242 vs ChatGPT 77，⭐ 分母 924）；⭐ >6 节点上，⭐ **LLM 赢 1.69×**（⭐ ChatGPT 679 vs SAMOS 401，⭐ 分母 1,845）。

⭐ **全部相关段落已在 C1 逐字抄录**（⭐ 四段引文 + 第五段「替 LLM 开脱」的段落）。⭐ 这里只补一条 C1 没放的、⭐ 关于 90% 切片性能下降的完整段落（⭐ 因为它是本文对**自己不利现象**处理得最细的一处，级别 **M(thesis)**）：

> "**The decline in meaningful recommendations at larger contexts (90%) for both LLMs suggests that either they failed to introduce significant new information or their generated completions deviated from the ground truth.** We believe that the drop in performance could be attributed to the removal of the ground truth. With the ground truth missing, the subprocess becomes so specific that similarity-based tools struggle to find a fitting "puzzle piece" to complete the task. **Additionally, we hypothesize that LLM-based tools may lack the necessary background knowledge to accurately fill in the gaps. However, this hypothesis needs further investigation to validate. It's also possible that the decline in performance might not be entirely due to an inherent limitation of LLMs. A prompt that invokes domain knowledge could enhance the LLM's ability to generate the correct completion.**"

⭐⭐ **⭐ 这段的结构值得拆开看，⭐ 它是「一个不利现象 → 四个候选解释」的模板**：

1. ⭐ 现象陈述（⛔ 不修饰）：⭐ 90% 上下文时 meaningful 反而下降
2. ⭐ 解释 A（⭐ 归因于实验设计）：⭐ ground truth 被移除导致库里找不到合适拼图
3. ⭐ 解释 B（⭐ 归因于 LLM 能力）：⭐ 缺领域背景知识 —— ⭐ **标注为 hypothesis，⛔ 需进一步验证**
4. ⭐ 解释 C（⭐ 归因于自己的 prompt）：⭐ 也许换个调用领域知识的 prompt 就好了

⭐ **可取**：⭐ 三个解释都明确标了不确定性（"We believe" / "we hypothesize" / "It's also possible"），⛔ 没有一个写成事实句。⭐ 这与本仓库 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9 「⭐ 每个数字标证据级别、⛔ 标 I 的不得写成事实句」同一路数。

⚠️ **不可取**：⭐ 解释 C **没有任何实测支撑**，⛔ 而它恰好是唯一能替自己方案开脱的那一个。⛔ **我们写 −15.82pp 时若要用这一招，必须先跑那次实测。**

---

## G. ⛔ 存疑与未核项

1. ⛔⛔ **⭐ 终版 TSE 全文未取到，⭐ B/C 两节据 OA 前置版（thesis Chapter 5）** —— ⭐ 已试过：⭐ IEEE Xplore 文档页（⛔ HTTP 202 + JS 壳）· ⭐ Crossref 给的 `xplorestaging` PDF 直链（⛔ 返回 IEEE 登录 HTML）· ⭐ Unpaywall（⛔ `url_for_pdf: None`，⭐ 仅指向 WUR landing page）· ⭐ WUR 机构库页（⛔ 无 PDF，⭐ 只有 DOI 链接）· ⭐ OpenAlex（⛔ `is_oa: false`）· ⭐ arXiv API 按标题与按作者两路（⛔ 0 命中）。⚠️ **⭐ 后果：⭐ 本卡所有具体数字都可能在评审修订中变动过。⭐ 已用「终版摘要四处措辞一致」做交叉验证，⛔ 但那只覆盖了摘要级结论，⛔ 覆盖不到 Table 5.2 / 5.4 的逐格数字。**
2. ⚠️ **⭐ 摘要说「≈60% of the complete process」，⛔ 但正文结果的 meaningful 峰值在 70% 切片** —— ⭐ RQ1 的 recall 随切片单调上升，⭐ RQ2 的 meaningful 率在 70% 达峰后 90% 回落。⛔ **「≈60%」这个数字在正文里找不到直接对应的表格行**，⭐ 推测是对「50–70% 区间」的概括（级别 **I**）。⛔ 未能确认它在终版里是否改过。
3. ⚠️⚠️ **⭐ 是否单次运行 —— ⛔ 全文查不到。** ⭐ 已在 thesis Chapter 5 全文（4366–5872 行）检索 runs / temperature / seed / repetition / variance，⛔ 无命中。⭐ 级别 **I**，⛔ 本卡未写成事实句。⚠️ **⭐ 这一项若能确认为单次，⭐ 则本文 LLM 侧所有数字都缺稳定性估计**，⛔ 是引用时必须带的限定。
4. ⚠️ **⭐ 复现包（1.8 GB）内部条目未能列举** —— ⭐ 已试：⭐ Zenodo 网页文件直链（⛔ 403）· ⭐ API `files/.../content` 端点 + Range 请求取尾部中央目录（⛔ 403「unusual traffic from your network」，⭐ 即限流而非缺文件）。⭐ 无 Range 的 HEAD 请求返 200 + `content-length: 1803858439`，⭐ **故文件确实存在且非空壳**；⛔ 但「⭐ 逐条结果 / ⭐ 不合规 LLM 产出清单 / ⭐ prompt 变体历史是否在内」⛔ 未能验证 → ⭐ 实验结果细则一项因此判 🟡 而非 🟢。
5. ⚠️ **⭐ SAP-SAM 数据集入口本轮未单独核验** —— ⭐ 只核了作者自己那份 GitHub BPMN 库的 Zenodo（⭐ 395 MB，⭐ 实取元数据）。⭐ SAP-SAM 是第三方公开数据集（⭐ 原文引 [257]），⛔ 未去 signavio 侧确认当前可获取性。
6. ⚠️ **⭐ 本条与 L3 硬门 1 的关系需主 session 裁定** —— ⭐ [README.md](../README.md) §2 硬门 1 写「⛔ 只把 LLM 当被评测对象…的不算」。⭐ 本文的定位**恰好在这条线上**：⭐ 一方面 LLM 是**被评测对象**（⭐ 与传统工具做对照），⛔ 另一方面他们确实**构建了**一条 LLM 推荐流水线（⭐ prompt 设计 + bigram 编码 + 产出转 BPMN 可视化 + 解析器）。⭐ 我判**过门**（⭐ 有可抽取的流水线形态，⭐ B1–B7 各格都填得出内容），⛔ **但这是判断而非事实，⭐ 记在这里以便复核。**
7. ⚠️ **⭐ thesis 章节与终版的篇幅差（⭐ 约 37 页 vs pp. 1–21）未能解释** —— ⛔ 可能是排版口径不同（⭐ 论文单栏大开本 vs TSE 双栏），⛔ 也可能确有内容删减。⛔ 无法区分。
8. ⚠️ **⭐ MDE / OCL 类语义约束是否存在：⛔ 确认为无，⭐ 但这是「查遍全文未见」而非「原文明说没有」** —— ⭐ 已检索 Chapter 5 全文，⛔ 无 OCL / metamodel constraint / well-formedness / validation rule 类机制（⭐ 只有 Camunda API 的语法 parse）。⭐ 级别 **S**。
