# 卡片 · Sultan, Apvrille & Coudert, SoSyM 2026 —— 依赖图 + LLM 的 SysML 多视图一致性检测与纠正

⭐ **全文已取到并通读**（⛔ 不是仅据摘要）。⭐ 论文是 **CC-BY 4.0 开放获取**，⛔ 但 `link.springer.com` 对 CLI 一律返回 `Client Challenge`（Fastly/HUMAN WAF，需 JS）——⭐ 最终经渲染代理取到全文正文（184 KB markdown）＋ Table 1–8 的独立表页 ＋ 原始 HTML（680 KB，含 Data availability / Ethics / Appendix A）。⭐ **另外把实现仓库里的真实 prompt 源码也取到了**（见 B3、D），⛔ 所以本卡的 prompt 断言不是从论文正文推的，是逐字从 `.java` 读的。

⚠️ **本卡开头先回答任务书最要紧的两问，⛔ 因为它们决定这篇对我们是「强背书」还是「不同问题」。**

---

## ⭐⭐ 先答第 1 问：「规则法抓不到深层语义问题」这句话原文是什么、有没有实验

### 逐字原文（⭐ 共四处，⛔ 全部核对过）

**① 摘要（M，逐字，已在 `id="Abs1"` 与 Crossref JATS 双源核对）：**

> "Traditional approaches to consistency rely on formal rule-based methods, sometimes complemented by ontologies. **Yet, these techniques often fall short when dealing with deeper semantic issues that cannot be explicitly expressed as rules.**"

**② §1 Introduction（M，逐字）：**

> "However, **even ontology-based approaches struggle to bridge more complex semantic gaps, due to their dependence on explicit rules.** Recent advances in Large Language Models (LLMs) offer a promising direction for addressing these more intricate semantic inconsistencies [4, 5, 6]."

**③ §2.1 Enforcing UML/SysML models consistency（M，逐字 —— ⭐ 这是最完整的一处）：**

> "While these rule-based strategies, especially those employing formal reasoning on such rules, including ontology-based approaches, are highly effective and relevant, **they inherently only address inconsistencies explicitly defined by rule constraints. As a consequence, some classes of semantic inconsistencies may remain unaddressed.**"

**④ §2.1 后段（M，逐字 —— ⭐ 给出了具体的「哪一类」）：**

> "Furthermore, **some semantic inconsistencies may be difficult to address by rules that can be checked algorithmically** (e.g., **if two synonymous names are used in different diagrams to designate the same modeled object**—as Sect. 4 illustrates), therefore calling for complementary approaches."

### ⛔⛔ 它给了什么证据 —— **答案：断言 ＋ 一个 worked example ＋ 一条文献计量旁证，⛔ 没有对照实验**

| 它拿出来的东西 | 是什么级别的证据 | 逐字 |
| :-- | :-- | :-- |
| ⛔ **文献计量旁证** | ⚠️ **证的是「我们的规则是新的」，⛔ 不是「规则法不够」** | "As evidence of this, to the best of our knowledge, some of the rules we first proposed in [6], and that we extend in this paper, especially those focusing on cross-view consistency between SysML UCDs and BDs (see Sect. 3), **have not been reported in existing literature reviews.**" |
| ⭐ **一个构造出来的例子**（Fig. 4，DPS 的 `Wind_Sensor` 块 vs `Propeller_Anemometer` actor 指同一实体） | ⭐ 说明性例子，⛔ 非实验 | "In a purely rule-based consistency detection approach, and **unless supported by extensive synonym dictionaries or ontologies, it is difficult to algorithmically determine that the actor and the block indeed refer to the same entity.**" |
| ⭐ **一次真实命中**（walkthrough 里 LLM 抓到 `Propeller_Ane`**r**`ometer` 拼错，并在纠正阶段改对） | ⭐ **单例 anecdote**，⛔ 不是分类统计 | §6.2 逐字："The walkthrough illustrates that the LLM+rule-based inconsistency detection and correction approach successfully identified and resolved a naming mismatch, in which two different terms (one being misspelled) actually referred to the same concept. **This type of inconsistency is typically difficult to capture through formal rules alone**, illustrating the added value that LLM-based complementary approaches can bring." |
| ⭐ **另一次真实命中**（识别出两个不同块其实是同一实体、应合并） | ⭐ 单例 anecdote | §6.1.1 逐字："Another example included in our results is the identification of two distinct blocks that in fact represent the same entity and should therefore be merged: […] **These inconsistencies, which are relevant, were obviously not captured by our rules.**" |
| ⛔ **与纯规则法的定量对照** | ⛔ **不存在** | ⭐ Table 7 只有 LLM+rule 一条臂；⛔ 没有 rules-only 臂，⛔ 没有 rules-only 的漏检数 |
| ⛔ **假阴性（漏检）测量** | ⛔ **明确没做** | §6.3 Construct validity 逐字："**our measurements currently account for true positives and false positives, but not false negatives.**" |

### ⛔⛔ 结论 —— ⚠️ **这篇是「窄口径的强背书 ＋ 宽口径的反向证据」，⛔ 不能当成「LLM 是深层语义的答案」来引**

1. ⭐ **窄口径成立**：对 **命名/同义词/术语失配** 这一类，它有两个真实命中，且明说规则抓不到。⭐ 这一类可以当背书引。
2. ⛔⛔ **宽口径反向**：⭐ 这篇论文自己的实验证明，在**逻辑依赖语义**上，**确定性图算法完胜 LLM**。⭐ §6.1.1 逐字："the step-by-step illustration provided in Sect. 5 shows that **even the most advanced LLMs available at the time of evaluation were unable to identify logical dependencies along simple paths involving only two consecutive edges.** This observation strongly supports the need to combine the LLM-based detection approach with complementary techniques, such as the graph-based approach proposed in this paper."
3. ⚠️ ⭐ **而且那个「最先进模型」是 GPT-5.1**（M，§5.2.2 逐字："Applying this approach to **[M-Incomplete]** with GPT−5.1 as the underlying LLM yields the following list of inconsistencies […] **Three false positives are also reported.**"）。⭐ 逐条对照：图法 **9 检出 / 0 误报 / 0 漏检**；GPT-5.1 **3 个误报**，⛔ 且其中一个误报恰恰是**看不见一条两跳路径**（它说 UCD 里 `regulatePositionAndHeading` 没到 `computeActuatorsSetpoint`，⛔ 而 `regulatePositionAndHeading → sendActuatorsSetpoint → computeActuatorsSetpoint` 就在图里）。
4. ⭐⭐ **所以「那个位置」的准确状态是：⭐ 命名/同义类那一格被这篇占了（有例子、无统计）；⛔ 而「深层语义」这个大口径下的其它格子它自己都判给了确定性方法。** ⛔ 用它当「规则法不够、所以要 LLM」的引用是可以的，⛔ **但必须限定到命名/术语类，⛔ 否则会被审稿人用这篇自己的 Table 8 反驳。**

---

## ⭐⭐ 再答第 2 问：它检的是「多视图之间」还是「模型 vs 需求」

⚠️ **任务书猜对了大半，⛔ 但有一个非平凡的例外，⭐ 必须说清。**

### ⭐ 判定的**对象与分类学**：⛔ 纯粹是多视图之间（＋单视图内部）

⭐ §6.1.1 逐字（M）：

> "We differentiate between **internal inconsistencies (within a single diagram)** and **cross-view inconsistencies, i.e., between a block diagram (and the related state machine diagrams) and a use case diagram.**"

⭐ Table 7 的列就只有这两类 ＋ `Errors`。⛔ **没有「模型 vs 需求」这一类，⛔ 也没有以 NL 规约为分母的任何统计。** ⭐ 全部 38 条形式化规则（B5）也全是 diagram-内部 或 diagram-对-diagram：`RU*`（UCD 内）· `RB*`（BD 内）· `RS*`（SMD 内）· `RUB*`（UCD↔BD）· `RSU*`（UCD↔AVATAR 模型）· `RSB*`（SMD↔BD）。⛔ **一条都不涉及 NL。**

### ⚠️⚠️ **但 NL 规约确实进了 prompt** —— ⭐ 这是那个非平凡例外

⭐ §5.1.3 逐字（M）：

> "Finally, **the request sent to the AI engine contains above-mentioned constraints, the question/query, the system specification, and the UCD and BD in textual format.**"

⭐ 实现侧逐字印证（M，从 `AIDiagramCoherency.java` 源码读的，⛔ 不是从论文推的）：

```java
private String[] QUESTION_IDENTIFY_INCOHERENCIES = {
  "From the provided specification and from the two SysML diagrams given in textual format,"
  + "identify the incoherencies between the two diagrams. ..."};
...
chatData.aiinterface.addKnowledge("The system specification is: " + _spec, "ok");
```

⭐ 于是**它实际产出的东西里混着 model-vs-NL 判定**。⭐ 配套仓库 README 里作者自己贴的真实输出就有（M，逐字）：

> "There is **no actor or use case for ErrorCorrectionCode, which is a significant part of the system as per the specification.**"

⛔ 这条显然是「模型 vs 规约」，⛔ 不是「视图 vs 视图」。⛔ **但它在 Table 7 里会被记成 `internal`（因为它只涉及 Diagram1）**，⛔ 论文从不承认这一类的存在。

### ⭐⭐ 第 2 问的裁定

| 维度 | 它 | ⭐ 我们（v46） |
| :-- | :-- | :-- |
| ⭐ **问题定义** | ⛔ **多视图一致性**（UCD ↔ BD ↔ SMD） | ⭐ **模型 vs 自然语言需求** |
| ⭐ 判定分母 | ⛔ 视图对（12 个 BD×UCD 组合） | ⭐ NL 需求条目（台账 98 条） |
| ⭐ 参考物（reference） | ⛔ **另一个模型**（UCD 当 reference） | ⭐ **NL 文本** |
| ⚠️ NL 在不在 context 里 | ⭐ **在**（system specification 随 prompt 一起给） | ⭐ 在（就是被比的对象） |
| ⛔ NL 算不算判定依据 | ⛔ **不算 —— 无 NL 分母、无 NL 类别、无 NL ground truth** | ⭐ **就是全部依据** |

⛔⛔ **所以：⭐ 与我们不是同一个问题。** ⚠️ 术语陷阱确认成立 —— ⭐ 它的 `consistency checking` 与 CSUR 综述口径一致，指**多视图模型之间**。⛔ **不得把它当作 model-vs-NL 的先例或可比数字。** ⭐ 但它是我们**最近的邻居**：⭐ 同为 UML/SysML 状态机 · 同为「检出 ＋ 纠正」· 同为 LLM+规则混合 · 顶刊。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `sosym2026-state-machine-consistency` |
| `title` | ⭐ **On the consistency of state machines, use cases and block diagrams using dependency graphs and Large Language Models**（M，Crossref ＋ 落地页 `<title>` 双源一致） |
| 作者 | ⭐ **Bastien Sultan · Ludovic Apvrille · Sophie Coudert**（M，Crossref author 字段；⭐ 三人同属 LTCI, Télécom Paris, Institut Polytechnique de Paris） |
| `year` | ⭐ **2026**（M，Crossref `published: 2026-07-06`；⛔ 无 early-access 年歧义；⚠️ 尚未编卷期 —— Crossref `volume/issue/page` 全为 `None`，属 Online First） |
| `venue` | ⭐ **Software and Systems Modeling (SoSyM)**, Springer（M）。⭐ Communicated by **Marsha Chechik and Benoit Combemale**（M，`id="ethics"` 段逐字） |
| `ccf` | ⭐ **B** —— ⭐ 本仓库 [ccf_venues/SUMMARY.md](../../../../../ccf_venues/SUMMARY.md) 有 [`journal-b-sosym`](../../../../../ccf_venues/journal-b-sosym/README.md) 建档，标记 `🥈` = CCF B（M） |
| `doi` | ⭐ [`10.1007/s10270-026-01388-4`](https://doi.org/10.1007/s10270-026-01388-4) —— ⭐ **已实际访问核验**：Crossref API `/works/` 返回完整题录（title / 3 authors / container / published / license / reference-count **51**）；`doi.org` 解析 302 → `link.springer.com`。⭐ Unpaywall `is_oa: true`, `oa_status: hybrid`, `license: cc-by`, `version: publishedVersion` |
| `arxiv` | ⛔ **无**（⭐ 已试 arXiv 检索与 ar5iv；⛔ 无对应条目） |
| `url`（全文） | [link.springer.com/article/10.1007/s10270-026-01388-4](https://link.springer.com/article/10.1007/s10270-026-01388-4) —— ⚠️ 直接 `curl` 得 `Client Challenge`（3038 B HTML，WAF），⭐ 经渲染代理取到完整正文 |
| `url`（HAL 题录） | [telecom-paris.hal.science/hal-05682394v1](https://telecom-paris.hal.science/hal-05682394v1) —— ⚠️ **题录在、全文不在**（HAL API `fileMain_s: None`，OpenAlex 也报该 location `is_oa: false`） |
| `artifact_type` | ⭐ **SysML/UML 三类图**：Use Case Diagram (UCD) · Block Definition Diagram (BD) · **State Machine Diagram (SMD)**；⭐ 均为 TTool 的 **AVATAR** SysML profile 实例。⭐ 另有一个中间表示：**AVATAR dependency graph** |
| `task` | ⭐ **一致性检查（＝缺陷检测）＋ 纠正**，⛔ 附带 **生成**（BD/UCD/SMD 从 NL 规约生成，⭐ 复用其 TTool-AI 前作） |
| `boundary` | ⚠️ **`邻域`**（⛔ 不是纯界内 —— 见下方说明） |

### ⚠️ `boundary` 为什么判 `邻域` 而不是 `界内`

⭐ 主体确实是 EFSM 形态：⭐ Definition 4 的 SMD = `(S, T)`，⭐ Definition 3 的 transition description = `⟨after, guard, actions⟩`，⭐ actions 含赋值 / 随机赋值 / `send`/`receive` 同步 / 方法调用 —— ⭐ 即 $M=(S,E,V,Tr,A)$。⛔ **但有两项界外成分（M，逐字）：**

1. ⛔ **时间约束**：Definition 3 逐字 "$after \in \mathbb{N}$ **constrains the delay before firing** _t_"；⭐ §3.2.1 引言句也逐字说 transition description 含 "**a temporal constraint**"。⭐ 规则 `RS3` 专管它。⚠️ 这不是时钟变量＋不变式，⛔ 但也不是无时间。
2. ⛔ **并发**：AVATAR 模型 = BD ＋ **每个 block 一台状态机**，⭐ 块间经 `send→receive` 同步（⭐ §3.5 逐字提到 "transition synchronizations via $send\rightarrow receive$, and $receive\rightarrow send$ when the underlying connection is synchronous"）。⛔ 不是单状态机内的正交区，⛔ 但是真并发合成，⭐ 且 TTool 底层就是做时间模型检查的。

⭐ 按 [README.md](../README.md) §2.1 的三档，⭐ L3 不设边界门只要求标注 —— ⭐ 本卡标 `邻域` 并把两项成分写明。⛔⛔ **提醒：若后续要把这篇搬进 L1/L2（那两轨过边界门），⛔ 必须先在这两点上重走一遍门。**

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐ 论文有**两条并列的检测链**（Ct3 与 Ct4），⭐ 共用一条纠正链。⭐ 按论文自己的任务编号画（`D1.1–D1.5` / `C1–C3` 出自 Fig. 5，⭐ 图法三段出自 Fig. 6/7）：

```
┌── Ct3：LLM+规则链（每张图一条，两张图并行跑 D1.* 与 D2.*）─────────────────────┐
│  [人] 给 NL 系统规约                                                        │
│   → [确定性] D1.1 组 prompt ＝ 用户输入 ＋ 语法约束 ＋ 该图型的内部一致性规则（RAG 式注入）│
│   → [LLM]   D1.2 生成图（JSON 数组回传）                                     │
│   → [确定性] D1.3 语法 ＋ 规则检查 ── 不过则回 D1.1（⭐ 上限 20 轮）             │
│   → [人]    D1.4 人工看图：接受 / 要求改 / 重生成                             │
│   → [确定性] D1.5 从 JSON 画图，⭐ 建构时**强制**一批规则（correct-by-construction）│
├── 跨图检测 ────────────────────────────────────────────────────────────┤
│   → [确定性] C1 把两张图导成精简文本 ＋ 输出格式约束 ＋（可选）跨图规则           │
│   → [LLM]   C2 产出不一致清单（⛔ 自由文本 description）                       │
│   → [人]    C3 人挑哪些条目要修 → 回灌 D1.1 / D2.1（＝纠正）                  │
├── Ct4：依赖图链（⛔ 全程无 LLM）───────────────────────────────────────────┤
│   [人]    G1 给 BD/SMD 的 block、state、transition 打 tag（＝手工建跨视图链接）  │
│   → [确定性] G2 `model2graph`：AVATAR 模型 → 依赖图（⭐ 有双射性证明）           │
│   → [确定性] G3 Algorithm 1 图遍历比对 → 不一致清单                            │
└──────────────────────────────────────────────────────────────────────┘
```

⭐⭐ **合起来 11 段 · 其中 LLM 只有 2 段**（`D1.2` 生成/纠正 · `C2` 检测）· **人 3 段**（`D1.4` 接受门 · `C3` 挑条目 · `G1` 打 tag）· **确定性 6 段**。

⚠️ ⭐ **Ct4 整条链一个 LLM 都没有** —— ⛔ 这一点很重要：⭐ 论文最漂亮的那组数（Table 8，0 误报 0 漏检）**完全来自确定性链**。

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| `D1.2` 初次生成 | ⭐ **生成器**（NL 规约 → UCD/BD/SMD） |
| `D1.2` 纠正复用 | ⭐ **修复者**（⭐ 输入 ＝ 规约 ＋ 待修图的文本 ＋ 不一致清单；⛔ **同一个生成器换 prompt，⛔ 不是独立修复器**） |
| `C2` 跨图检测 | ⭐ **评审者 / 检测器**（⛔ 自由文本输出） |
| ⛔ 裁决者 | ⛔ **LLM 从不担任** —— ⭐ 见 B4 |
| ⛔ 打 tag | ⛔ **人做**（⚠️ 论文说这本可以交给 LLM，⭐ 但没做：逐字 "an alternative approach could rely on the TTool-AI interaction mechanism with the LLM to provide an automated tagging"） |

### B3 · prompt 策略

| 策略 | 有无 | 证据 |
| :-- | :-: | :-- |
| ⭐ **规则以自然语言注入 prompt**（作者自称 RAG） | ⭐ **有** | ⭐ §2.2 逐字："**The RAG-based formal rule injection we perform in the context of the current paper follows this latter approach.**" ⭐ 实现里就是拼字符串：`AIDiagramCoherencyWithFormalRules.java` 逐字含 `"#Respect: In a block diagram, the blocks representing actors as defined in the use-case diagram must bear identical names to their corresponding use cases.\n"` 等三条 ＋ 一条 `"#Respect: Give any incoherency you can identify concerning the two provided diagrams"` |
| ⭐ **结构化输出约束**（JSON schema，⛔ prompt 里说明，⛔ 非受限解码） | ⭐ **有** | ⭐ 逐字（源码）：`"When you are asked to identify all the relevant incoherencies between two diagrams, return them as a JSON specification formatted as follows:{incoherencies: [{ \"diagram\" : \"diagram1 or diagram2\", \"description\": \"description of the incoherency\"}...]}"` |
| ⭐ **解析/校验失败回灌**（迭代反馈） | ⭐ **有** | ⭐ `D1.3` 失败 → "a new request is forged from the results of the syntax analysis" → 回 `D1.1` |
| ⛔ few-shot / CoT / self-consistency 投票 / 多智能体辩论 / tool calling | ⛔ **无** | ⭐ 正文与源码都无（S） |
| ⛔ 模型自反思（self-reflection） | ⛔ **无** | ⭐ §2.2 把 Yang et al. 的 self-reflection 列为**别人的**做法（"Relatedly, Yang et al. propose a self-reflection mechanism […] In this case, responses are not checked against an external set of formal rules"），⛔ 明确把自己划到「查外部形式化规则」那一侧 |

⭐ **prompt 全部公开在源码里**（→ D 节），⭐ 且 Data availability 段逐字点名："The source code of our implementation, **including the full prompts used for the automated interactions with the LLMs**, is hosted in TTool's Git repository".

### ⚠️⚠️ B3 附一条**对我们直接有用的负面发现**

⭐ §4.2.2 Implementation details 逐字（M）：

> "we have decided, in our implementation of the process, **to make optional the injection of rules introduced in Table 4. Indeed, when these rules are incorporated into the consistency request (C1), the LLM tends to exclusively focus on these rules, thus ignoring other consistency aspects.**"

⭐ §6.2 再说一遍并给出对策（M）：

> "injecting formal rules into the LLM-based cross-view inconsistency detection process tends to make the LLM focus primarily on these rules. As a result, our answer to **RQ2** is positive in the context of model generation and correction tasks, **but more nuanced for LLM-based cross-view inconsistency detection.** In this latter case, **it is beneficial to run the detection process twice, once with formal rules embedded and once without**, to take advantage of a broader detection basis."

⭐⭐ **这就是「把闭合词表塞进检测 prompt 会造成隧道视野」的一个独立外部观察。** ⚠️ 我们 v46 的 `occupancy_after` 的 `nl_cue` 把模型从 `edge_declared` 上引开（324 格里 `edge_declared` 被问 **0.0%**）是同一种病；⛔ 他们的对策是**跑两遍取并集**，⭐ 而不是修词表。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

⭐⭐ **这篇有三个循环，⭐ 三个裁决者，⛔ 而 LLM 一个都不是。**

| 循环 | 裁决者 | ⭐ 类型 | 终止条件 | 最大轮数 |
| :-- | :-- | :-- | :-- | :-- |
| `D1.1 → D1.2 → D1.3 → D1.1`（生成/纠正内环） | `D1.3` 的语法分析 ＋ 形式化规则检查 | ⭐ **`parser / 编译器` ＋ `确定性规则`** | ⭐ 收敛（规则全过）/ ⛔ 撞上限 | ⭐ **20**（M，逐字："our implementation of the process **caps the maximum number of iterations at 20**"） |
| `D1.4` 接受门 | ⛔ **人** | ⭐ 人叫停 | ⛔ 无 |
| `C1 → C2 → C3 → D1.1`（检测-纠正外环） | ⛔ **人**（挑哪些不一致要修） | ⭐ 人叫停 | ⛔ **无上限、无自动重启** |

⭐ **裁决者类型逐条对照词表**：⛔ `LLM 自评` = **无**；⭐ `parser / 编译器` = **有**；⭐ `确定性规则` = **有**；⭐ `人` = **有（两处）**；⛔ `sound oracle`（模型检查器 / SMT）= **不在这条链上**（⚠️ TTool 有模型检查器，⛔ 但本文没把它接进一致性循环）；⛔ `测试执行` = 无。

#### ⛔ 有无报告循环的边际收益 —— ⛔ **没有，⭐ 但有一条更强的话**

⛔ **逐轮数字：原文未提供。** ⛔ 论文既没给「第 N 轮修好几条」的表，也没给 token/成本曲线。

⭐ 但它给了一个**上限从未被触及**的事实（M，逐字）：

> "If this limit is reached, the correctness-by-construction guarantees described in Dx.5 […] no longer entirely hold, and the user is notified via the GUI that the iteration limit has been exceeded. **In practice, however, this threshold was never reached in the evaluations reported below.**"

⭐ 加上 walkthrough 里唯一被记录的一次循环：⭐ 初版 UCD 违反 `RU8`（每个 actor 至少连一个 use case），⭐ 两条内部不一致，⭐ 一次反馈就修好（M，逐字："These two internal inconsistencies were then addressed through the automated feedback mechanism. As a result, **the final version of the UCD adheres fully to the guidelines listed in Table 1.**"）。

⭐⭐ **S 级推论（⛔ 论文没这么写，⭐ 但从上面两条可直接推出）：⭐ 当裁决者是确定性规则时，收敛发生在很少的轮数内（远小于 20），⛔ 因此他们根本不需要报边际收益曲线。** ⚠️ 这与我们 v46 的实测互补：⭐ 我们「第 3–5 轮零收益」的那 79% token 全花在**两个 LLM 自评 reviewer** 上，⛔ 而**确定性那条（`convert ⇄ precheck_and_seal`）在我们这里同样是 0 token 且性价比最高**。⭐ **两边独立得到同一个形状。**

#### ⛔ 外环的收益也没报，⛔ 且它明确留了一次没做的迭代

⭐ §5.1.4 逐字：⭐ 纠正后 "**not all inconsistencies were corrected.** For example, the DPS block is still unrelated to other blocks. […] **Another iteration on inconsistency detection (stages C1 to C3) could resolve these remaining issues.**" ⛔ **那一轮他们没跑，⛔ 所以外环的第 2 轮收益是空白。**

### B5 · ⭐ 中间表示

⚠️⚠️ **这篇有两套中间表示，⭐ 一套闭合一套开放，⛔ 绝不能混谈。**

| | ⭐ ① 形式化规则目录 | ⭐ ② 依赖图 | ⛔ ③ LLM 检测输出 |
| :-- | :-- | :-- | :-- |
| 有无 | ⭐ 有 | ⭐ 有 | ⭐ 有（⛔ 但无结构） |
| 形态 | ⭐ **缺陷类型学 / 规则目录**（38 条编号规则，每条带形式化表达式） | ⭐ **中间 IR**（有向图 ＋ 顶点 tag 集合） | ⛔ **自由文本 JSON**：`{"diagram": ..., "description": <自由文本>}` |
| ⭐ **是否闭合** | ⭐⭐ **闭合** —— ⛔ 从固定 38 条里选 | ⭐ 闭合（⭐ 结构由 `model2graph` 唯一决定，⭐ 有双射证明） | ⛔⛔ **完全开放** —— ⛔ 无类别字段、⛔ 无枚举、⛔ 描述随便写 |
| ⭐ **谁定的 / 谁选** | ⭐ **作者预编目录**；⛔⛔ **按阶段硬编码挑选，⛔ 不是 LLM 选** | ⭐ 作者定义（⭐ 前作 [9,10] 的 IR，⭐ 本文首次形式化） | ⛔ LLM 自由生成 |

#### ⭐ 38 条规则全表（⛔ 逐条抄下，⭐ 这是与我们 19 条谓词最直接的对照物）

⭐ **Table 1 · UCD 内部（10 条）**

| ID | 规则 | ⭐ 论文给的出处/理由 |
| :-- | :-- | :-- |
| RU1 | There is at least one actor and one use case in the diagram | ⭐ 实用性：The UCD shall not be empty |
| RU2 | Any link shall involve two actors/use cases existing in the diagram | ⭐ 实用性：The UCD shall be a (well-defined) graph |
| RU3 | Each actor/use case shall have a name | ⭐ **UML 2.5.1 标准 [47]** |
| RU4 | Actor names shall start with a noun | ⭐ **文献 [48,49,50,51]** |
| RU5 | Use case names shall start with a verb | ⭐ **Derives from [2] 与 [48,49,50,51]** |
| RU6 | Any link between an actor and a use case shall be an association link | ⭐ **文献 [48]** |
| RU7 | No link shall exist between two actors | ⭐ **UML 标准 [47]** |
| RU8 | Each actor shall be linked to at least one use case | ⭐ **Derives from [50]** |
| RU9 | At most one link shall exist between two given elements | ⭐ **文献 [50]** |
| RU10 | Any link between two use cases shall be either a specialization, inclusion or extension link | ⭐ **Derives from [48]** |

⭐ **Table 2 · BD 内部（12 条）**：`RB1` 至少一个 block（非空）· `RB2` block 名唯一 · `RB3` 属性名唯一 · `RB4` 方法名唯一 · `RB5` 信号名唯一 · `RB6` 属性类型限 bool/int · `RB7` 方法签名参数类型限 bool/int · `RB8` 信号签名参数类型限 bool/int · `RB9` 信号必须是 input 或 output · `RB10` link 两端端口须属图中存在的 block · `RB11` link 必须有合法通信语义 · `RB12` connection 必须涉及所属 block 中真实存在的两个信号。⭐ 出处：`RB2`–`RB5` 记 "Ensure distinguishability between elements from an implementation point of view"（⭐ 实用性）；`RB6`–`RB9` 记 "**These rules are necessary to comply with Definitions 1, 7 and 8**"（⭐ **元模型定义性**）；`RB10` 记 TTool-AI 实现 [7]。

⭐ **Table 3 · SMD 内部（5 条）**：`RS1` 恰好一个 start state（⭐ 理由：确保唯一初始状态）· `RS2` guard 必须是正确的布尔表达式（⭐ 出处 Definition 3）· `RS3` `after` 只能是正确的算术表达式（⭐ 出处 Definition 3）· `RS4` 两个不同状态不能同名（⭐ 实用性）· `RS5` transition 的起止状态必须在 SMD 中存在（⭐ 出处 Definition 4）。

⭐ **Table 4 · UCD↔BD 跨视图（2 条）**：`RUB1` 任何 environment block 至少与一个 system block 有 link · `RUB2` 任何 environment block 必须对应 UCD 中定义的一个 actor。⭐ 出处：⛔ **纯方法学理由**（"environment blocks are justified in a model only if they contribute to the modeling of the system's interfaces" / "External entities interacting with the system modeled shall be represented as actors in the UCD"）。⚠️ **这两条正是他们声称文献综述里没有的那两条。**

⭐ **Table 5 · UCD↔AVATAR 模型跨视图（5 条，⭐ 图法用的就是这组）**：`RSU1` UCD 每个顶点（use case 或 actor）在依赖图里都得有一个被同名 tag 标注的顶点 · `RSU2` UCD 里每条 `include` 路径，在依赖图里得有一条**反向**的对应路径 · `RSU3` `extend` 路径同理 · `RSU4` 每条 actor↔use case 的 `associate` 关系，依赖图里得有**双向**两条路径 · `RSU4w` `RSU4` 的**弱化版**（只要一条方向）。⭐ 出处：⛔ **方法学假设，⛔ 且论文自己声明比 UML 更强**（逐字："**These rules are not universal.** Rather, they illustrate the kind of methodological rules that can be defined and checked through simple graph traversals using our formalization. They should therefore be understood as **methodological consistency rules rather than as an encoding of UML/SysML semantics (they are actually stronger than the constraints defined in UML)**"）。

⭐ **Table 6 · SMD↔BD 跨视图（4 条）**：`RSB1` action 不得引用该 block 未定义的信号 · `RSB2` action 不得引用未定义属性 · `RSB3` guard 不得引用未定义属性 · `RSB4` `send`/`receive` 必须符合目标信号的 profile。⭐ 出处：⭐ **全部记 Definition 7/8（元模型定义性）**。

⭐ **合计 10+12+5+2+5+4 = 38 条**（⭐ 若把 `RSU4`/`RSU4w` 算一条则 37）。

#### ⭐⭐ 与我们 19 条谓词的对照（⛔ 这一格最有价值）

| 维度 | ⭐ 它（38 条规则） | ⭐ 我们（19 条谓词） |
| :-- | :-- | :-- |
| 闭合性 | ⭐ 闭合 | ⭐ 闭合 |
| ⛔ **谁选** | ⛔⛔ **按阶段硬编码**：⭐ `D1.1` 注入 `RU4,RU5,RU7,RU8,RU10⁺`；⭐ `D1.3` 检查 `RU1,RU2,RU3,RU8,RU9`；⭐ `D1.5` 建构时强制 `RU1,RU2,RU3,RU6,RU7,RU10⁺` —— ⛔ **三份固定名单，⛔ 与被检对象无关** | ⭐⭐ **LLM 在每条需求上自动选** |
| ⭐ **出处分级** | ⭐⭐ **有！** ⭐ Table 1–6 每条都有 `Reference (when applicable) or justification` 列，⭐ 分三类：**① 有文献/标准依据**（`RU3,RU4,RU5,RU6,RU7,RU8,RU9,RU10` ＝ 8 条）· **② 元模型定义性**（`RB6–RB9,RS2,RS3,RS5,RSB1–RSB4` ＝ 11 条）· **③ 只有实用性/方法学理由**（`RU1,RU2,RB1–RB5,RS1,RS4,RUB1,RUB2,RSU1–RSU4w` ＝ 19 条） | ⭐ **① 12 · ② 6 · ③ 1**（见 [../../provenance/](../../provenance/)） |
| ⭐ 输出粒度 | ⛔ 规则是**判据**，⛔ 但 LLM 侧输出**不挂规则 ID**（⛔ 只有自由文本 description） | ⭐ 断言脚本挂谓词 |
| ⭐ 覆盖率自陈 | ⭐ **明说不完备**（逐字："These rules **do not exhaustively cover** all the constraints specified in the formal definitions […] rather, they constitute a **pragmatic subset**"） | ⚠️ 我们实测只用到 15/19 |

⭐⭐ **两条可直接搬的做法**：

1. ⭐⭐ **它的 `justification` 列就是我们 provenance 三类分级的一个已发表先例**，⭐ 且是在 **CCF-B 顶刊**上过审的。⭐ 它的 ③ 类占 19/38（**50%**），⛔ 而我们 ③ 类只有 1/19（**5.3%**）。⭐ **也就是说：我们的出处纪律比一篇 SoSyM 论文严得多。⭐ 这本身是可写的。**
2. ⭐ **它明说规则集是 pragmatic subset 而非穷尽** —— ⭐ 这给我们「19 条不穷尽」提供了口径先例。

### B6 · 模型

| 用途 | 模型 | 证据 |
| :-- | :-- | :-- |
| ⭐ 生成（automotive braking ＋ space-based system 的全部图） | ⛔ **GPT-3.5** | ⭐ M，§6.1 逐字："All diagrams of the automotive system and of the space-based system were generated using **GPT 3.5**, and the diagrams of DPS were generated with **GPT 4**." |
| ⭐ 生成（DPS 的图） | ⛔ **GPT-4** | ⭐ 同上 |
| ⭐ 检测（`C1–C3`，⭐ Table 7 全部数字） | ⛔ **GPT-4** | ⭐ M，§6.1 逐字："**GPT 4** was used to identify inconsistencies." |
| ⭐ 纠正 | ⛔ **GPT-4** | ⭐ M："**GPT 4** was used to perform diagram updates." |
| ⭐⭐ **§5.2.2 那次 UCD vs 完整 AVATAR 模型的补充对照** | ⭐⭐ **GPT-5.1** | ⭐ M，逐字："Applying this approach to **[M-Incomplete]** with **GPT−5.1** as the underlying LLM yields the following list of inconsistencies." |
| ⭐ 有无多模型对照 | ⛔ **实质上没有** —— ⛔ 没有同一任务的跨模型对比表 | ⚠️ §7 逐字把它列为 future work："the evaluation presented in Sect. 6 relied on OpenAI's GPT. **It would be worthwhile to explore the complementary use of different LLMs** within this workflow" |
| ⭐ 实现支持的 provider | ⭐ OpenAI / MistralAI / 本地自托管 | ⭐ M，配套仓库 README 逐字："You will need either an **OpenAI** or **MistralAI** API key, or a locally hosted LLM." |
| ⭐ 工具版本 | ⭐ TTool **3.0 beta, build 14731**（LLM 部分）· **build 14863**（图法部分） | ⭐ M，§6.1 |

⚠️⚠️ **X1 的模型代际折扣在这篇上要**分段**打**：⛔ Table 7 的全部 69 条数据来自 **GPT-3.5/GPT-4**（⭐ 即 2023–2024 代），⛔ 参考价值需打折。⭐⭐ **但**「LLM 看不见两跳路径」那个致命发现来自 **GPT-5.1**，⭐ 即 2025 年末代 —— ⛔ **那条不能打折**，⭐ 它恰恰说明这个缺陷不是模型代际能解决的。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | ⭐ 在哪一段 |
| :-- | :-- | :-- |
| ⭐ 语法分析器 | ⭐ TTool 的 syntax checker ＋ JSON 解析 | `D1.3` |
| ⭐ **形式化规则检查器** | ⭐ 对生成结果算法化验 38 条规则的一个子集 | `D1.3` |
| ⭐⭐ **建构时强制**（correct-by-construction） | ⭐ 从 LLM 输出画图时**直接把一批规则做成不可违反**（⭐ 例：属性类型未定义则默认建为 integer） | `D1.5` |
| ⭐ 图导文本 | ⭐ TTool 自研精简文本格式（⛔ 不用 SysML v2 文本，⭐ 因为太啰嗦） | `C1` |
| ⭐⭐ **`model2graph` 模型变换** | ⭐ AVATAR 模型 → 依赖图，⭐⭐ **本文证明它与原模型双射**（Theorem 3/6, Corollary 4/7） | `G2` |
| ⭐⭐ **Algorithm 1 图遍历比对** | ⭐ 查两件事：① reference 图里的每个 label 在另一图里存不存在；② reference 图里任两个 label 间若有有向路径，另一图里对应 label 间是否也有 | `G3` |
| ⛔ 模型检查器 / 求解器 | ⛔ **没接进一致性循环** | ⚠️ TTool 有 direct model-checking of SysML [43]，⛔ 但本文只在 related work 提，⛔ 不参与 |

⭐⭐ **这一格的核心发现**：⭐⭐ **它的「可信底座」是一个带正确性证明的图变换 ＋ 图遍历，⭐ 而这个底座直接当检测器用（Ct4），⛔ 不是当求值器给 LLM 打分。** ⭐ 结果就是 **Table 8：3 个模型，0 误报 0 漏检。**

⚠️ ⭐ 对照我们：⭐ 我们有 pyfcstm 这个 sound oracle，⛔ 但它在**求值端**；⭐ 而这篇把确定性检查**做成一条独立的、与 LLM 并列的检测臂**。⭐⭐ **这是 M1 第二条设计原则的一个已发表先例，⛔ 但形态与我们设想的不同 —— ⛔ 它不是「把裁决者换成 sound oracle」，⛔ 而是「再加一条不含 LLM 的检测臂，两臂取并集」。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⛔⛔ **无。** ⛔ 没有 rules-only 臂、⛔ 没有 human 臂、⛔ 没有其它 LLM 方法臂。⚠️ **唯一的「对照」是两条自家臂互比**（Ct3 LLM 臂 vs Ct4 图臂），⭐ 且论文把它写成互补而非竞争 |
| `dataset` | ⭐ **LLM 臂：3 个系统 × (2 BD × 2 UCD) = 12 个图对**。⭐ 系统来源：automotive braking system（**FP7 EVITA** 项目）· space-based system（**H2020 SPARTA** 项目）· dynamic positioning system（DPS，⛔ 作者自撰规约）。⭐ **图法臂：1 个系统（DPS）× 1 个 reference UCD × 3 个 AVATAR 模型** |
| ⭐ **分母怎么定的** | ⚠️⚠️ **分母是「检出的条数」而不是「应检出的条数」** —— ⛔ 即 **precision 分母，⛔ 无 recall 分母**。⭐ Table 7 的 `Total = 69` 是**真不一致的检出数**，`Errors = 6` 单列且从总数中剔除。⭐ 逐字："Inconsistencies incorrectly identified are cataloged in the 'Error' column; **they are excluded from the total inconsistency count and are not addressed during the correction phase.**" |
| ⭐ 缺陷从哪来 | ⭐⭐ **LLM 臂：天然存在** —— ⛔ 被检的 BD/UCD 本身就是 LLM（GPT-3.5/4）生成的，⭐ 不一致是生成的副产物，⛔ **没有人工播种**。⚠️ **图法臂：人工播种** —— ⭐ 逐字："**These three models, we have designed**"：`[M-complete]`（应一致）· `[M-incomplete]`（拆掉 anemometer ＋ 调节算法不用传感器信息）· `[M-faulty]`（DPS block 的 SMD 里去掉指向执行器的输出信号同步） |
| `metrics` | ⭐ Table 7：`Inconsistencies detected`（internal / cross-view / Errors / Total）＋ `Inconsistencies corrected`（internal / cross-view / Total 分数式）。⭐ Table 8：`Detected / Errors / Missing`。⛔⛔ **无任何 `@k` 口径** —— ⛔ 每格只跑一次 |
| ⭐ `judged_by` | ⛔⛔ **作者自己，⭐ 主观，⛔ 无第三方、⛔ 无标注者间一致性、⛔ 无 $\kappa$、⛔ 无一致率。** ⭐ 作者自己写在 Threats 里（逐字）："**There is also inherent subjectivity in the classification of detected inconsistencies**, in particular when determining their relevance to specific diagrams and identifying them as errors." ⭐ 图法臂更直白："since we were also responsible for designing both the AVATAR models and the verification algorithms, **there is a potential for confirmation bias**" |
| `human_baseline` | ⛔ **本文无。** ⭐ 只引前作 [7,11]（对 Master 级工程学生的生成质量对比），⭐ 逐字："for Master-level engineering students, the generation process produces diagrams that are on average equivalent in quality to those created by students, while requiring substantially less time" —— ⚠️ ⛔ 那是**生成**质量，⛔ 不是一致性检测 |
| `runs` | ⛔⛔ **每格一次，⛔ 报单次，⛔ 无方差、⛔ 无重复采样。** ⛔ 论文全文未提 temperature、seed 或重复运行 |
| ⭐ `adverse_results` | ⭐⭐ **处理得相当坦白** —— 见下方专节 |

### ⭐ Table 7 逐格数字（⛔ 全表抄下，⭐ 已复算自洽）

| System | Test | Diagram | Internal | Cross-view | Errors | Total | Corr. Int. | Corr. Cross | Corr. Total |
| :-- | :-- | :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Automated braking | BD1 vs UCD1 | BD1 | 1 | 2 | 0 | 3 | 1 | 2 | 3/3 |
| | | UCD1 | 0 | 0 | 0 | 0 | 0 | 0 | – |
| | BD1 vs UCD2 | BD1 | 0 | 1 | 0 | 1 | 0 | 1 | 1/1 |
| | | UCD2 | 0 | 3 | 0 | 3 | 0 | 2 | 2/3 |
| | BD2 vs UCD1 | BD2 | 5 | 1 | 1 | 6 | 4 | 1 | 5/6 |
| | | UCD1 | 0 | 1 | 1 | 1 | 0 | 1 | 1/1 |
| | BD2 vs UCD2 | BD2 | 4 | 2 | 0 | 6 | 3 | 1 | 4/6 |
| | | UCD2 | 2 | 2 | 0 | 4 | 2 | 2 | 4/4 |
| Space-based system | BD1 vs UCD1 | BD1 | 3 | 6 | 0 | 9 | 3 | 5 | 8/9 |
| | | UCD1 | 0 | 0 | 0 | 0 | 0 | 0 | – |
| | BD1 vs UCD2 | BD1 | 4 | 1 | 0 | 5 | 3.5 | 1 | 4.5/5 |
| | | UCD2 | 3 | 1 | 0 | 4 | 2.5 | 1 | 3.5/4 |
| | BD2 vs UCD1 | BD2 | 2 | 2 | 0 | 4 | 1 | 2 | 3/4 |
| | | UCD1 | 1 | 1 | 1 | 2 | 1 | 1 | 2/2 |
| | BD2 vs UCD2 | BD2 | 1 | 4 | 0 | 5 | 1 | 4 | 5/5 |
| | | UCD2 | 0 | 2 | 0 | 2 | 0 | 2 | 2/2 |
| Dynamic positioning | BD1 vs UCD1 | BD1 | 1 | 1 | 0 | 2 | 1 | 0 | 1/2 |
| | | UCD1 | 0 | 0 | 1 | 0 | 0 | 0 | – |
| | BD1 vs UCD2 | BD1 | 2 | 2 | 0 | 4 | 1.5 | 1.5 | 3/4 |
| | | UCD2 | 2 | 0 | 0 | 2 | 0 | 2 | 2/2 |
| | BD2 vs UCD1 | BD2 | 1 | 0 | 0 | 1 | 0.5 | 0 | 0.5/1 |
| | | UCD1 | 1 | 1 | 0 | 2 | 1 | 1 | 2/2 |
| | BD2 vs UCD2 | BD2 | 3 | 0 | 1 | 3 | 2.5 | 0 | 2.5/3 |
| | | UCD2 | 0 | 0 | 1 | 0 | 0 | 0 | – |
| ⭐ **Total** | | | **36** | **33** | **6** | **69** | **28.5** | **30.5** | **59/69** |

⭐ **我方复算（⛔ 论文没列这些中间量）**：⭐ BD 侧检出合计 **49**，`49/12 = 4.08` ↔ 论文说 "averaging **4** inconsistencies for BDs"，✅ 对上；⭐ UCD 侧 **20**，`20/12 = 1.67` ↔ 论文说 "**1.7** for UCDs"，✅ 对上；⭐ `36+33 = 69` ✅；⭐ `28.5+30.5 = 59` ✅；⭐ `59/69 = 85.5%` ↔ 论文 "an automatic resolution of **85.5%** of the inconsistencies on average" ✅；⭐ `6/(69+6) = 8%` ↔ 论文 "this represents **8%** of the detected inconsistencies, meaning that **92%** of detected inconsistencies were relevant" ✅。

⚠️⚠️ **但 §6.3 的 `87%` 复算不出来（⛔ 我方实测，⭐ 见 F §3）**：⭐ §6.1.1 报 **85.5%**（micro，`59/69` ✅ 对上）；⛔ §6.3 报 **87%**（逐字 "which currently ranges from **50% to 100%** per diagram, with an average of **87%**"）。⭐ 我方按三种自然聚合逐一复算：**逐图宏平均（20 张）= 85.82%** · **逐图对宏平均（12 对）= 83.49%** · **逐系统宏平均（3 个）= 84.08%**。⛔⛔ **一个都不是 87%。** ⭐ 其中「逐图宏平均」这一档的 **区间恰好是 `50%`–`100%`**（✅ 与论文逐字一致），⭐ 所以论文指的应当就是这一档 —— ⛔ **但那一档算出来是 85.8%，不是 87%。**

### ⭐ Table 8 逐格（⛔ 图法臂）

| AVATAR model | Detected | Errors | Missing |
| :-- | :-: | :-: | :-: |
| **[M-complete]** | 0 | 0 | 0 |
| **[M-incomplete]** | 9 | 0 | 0 |
| **[M-faulty]** | 14 | 0 | 0 |

⚠️⚠️ ⭐ **注意这是 `n = 3` 的完美分**，⛔ 且 ground truth 由**同一批人**设计的模型定义。⭐ 作者自己承认（逐字）："We believe that all relevant logical dependency inconsistencies (and only those) introduced in the models were identified. **Nonetheless, since we were also responsible for designing both the AVATAR models and the verification algorithms, there is a potential for confirmation bias.** Therefore, it would be valuable to conduct further evaluations using additional, **pre-existing** AVATAR models".

### ⭐⭐ `adverse_results` 专节 —— ⭐ 这篇怎么写不利结果（⛔ 我们的 −15.82pp 可直接借鉴）

⭐ **它把不利结果写在四个地方，⛔ 一个都没藏：**

1. ⭐⭐ **摘要里就写了**（M，逐字）：⭐ "Overall, the practical illustration shows that the approach is effective for identifying and correcting inconsistencies, **although the LLM-based component produces both false positives and false negatives.**" ⭐⭐ **它把自家核心组件的 FP＋FN 写进了摘要最后一句。**
2. ⭐ **正文明说需要人在环内**（M，逐字）：⭐ "However, it also produces false positives; **therefore, user involvement in the loop is essential.**"
3. ⭐ **明说自家指标不完备**（M，逐字）：⭐ "our measurements currently account for true positives and false positives, **but not false negatives. However, we observed the presence of false negatives**, as the graph-based approach detected inconsistencies that were missed by the LLM-based approach. **Additional analyses and metrics incorporating false negatives would provide a more accurate and balanced evaluation of the LLM-based approach.**"
4. ⭐⭐ **主动把自家漂亮结果的适用范围钉死**（M，逐字）：⭐ 图法臂 "this performance holds **only** because the analysis was performed using the UCD as the reference model. **If the analysis were carried out in the opposite direction** […] **several false positives would appear** due to the way UCDs and design models are constructed […] **That should be kept in mind when using the approach.**"

⭐ **另外还有两条自我归因的方法论反省**（⚠️ ⭐ 这两条对我们尤其有用）：

- ⭐ **主动指出自家实验低估了自己**（M，逐字）：⭐ "In our experiments, we incorporated the entire list of detected inconsistencies […] into a single prompt […] **Handling each inconsistency individually might improve the correction rate** […] Consequently, **the performance of the LLM-based correction approach may be underestimated in our current evaluation.**"
- ⭐ **主动指出对照对自家 LLM 臂不公平**（M，逐字）：⭐ "as mentioned earlier, **the tags are not exported to the textual format provided to the LLM** in the LLM-based approach. **Exporting these tags might have improved its comparative performance** with respect to the graph-based approach in detecting the same inconsistencies."

⭐⭐ **形态总结**：⭐⭐ **不利结果 → 写进摘要 ＋ 正文 ＋ 独立 Threats 三节（Internal / Construct / External）＋ 明确写出「这个不利可能是我们实验设计造成的、真实性能可能更好」。⛔ 不隐藏、⛔ 不粉饰、⛔ 也不过度自我批评。** ⭐ 这正好是我们 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9「方向性松紧要一致」要求的那个形状，⭐ 而且是在 CCF-B 顶刊上过审的形状。

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| ⭐ 论文全文 | ⭐ **🟢** | [`10.1007/s10270-026-01388-4`](https://doi.org/10.1007/s10270-026-01388-4) | ⭐ **CC-BY 4.0 开放获取**（Crossref `license: creativecommons.org/licenses/by/4.0` ×2；Unpaywall `is_oa: true / oa_status: hybrid / license: cc-by / version: publishedVersion`）。⚠️ ⛔ **直连被 WAF 拦**：`curl` PDF 得 `HTTP 200` 但 body 是 3038 B 的 `<title>Client Challenge</title>`；`WebFetch` 得 `303 → idp.springer.com/authorize`。⭐ 经渲染代理取到正文 184 KB ＋ 原始 HTML 680 KB ＋ Table 1–8 独立表页 8/8 |
| ⭐ **实验代码（框架）** | ⭐ **🟢** | [gitlab.telecom-paris.fr/mbe-tools/TTool](https://gitlab.telecom-paris.fr/mbe-tools/TTool) | ⭐ 工具核验：`HTTP 200 · text/html`。⭐ 我方补充实取：GitLab API project `id=225`，默认分支 `master`，**HEAD `f9ff1501e9`**（`2026-07-27T15:32:33Z`, "Merge branch 'avatar-2-proverif-bug'"），license **`Other`**（⭐ 源码头逐字为 **CeCILL**：`"http://www.cecill.info"`），star 8。⭐ 论文点名的两个目录都实取到：`src/main/java/ai/` **38 个文件**、`src/main/java/avatartranslator/consistencyverification/` **1 个文件**（`ConsistencyVerification.java`） |
| ⭐ **数据集 / 复现包** | ⭐ **🟢** | [github.com/ZebreDeSoixanteQuatorzeCanons/SoSyM_Consistency](https://github.com/ZebreDeSoixanteQuatorzeCanons/SoSyM_Consistency) | ⭐ **工具输出逐字**：`HEAD 43155a71fd · 文件 13（非文档 9）· release 0 · license 无`。⭐ 我方补充实取完整清单：`LLMApproach/{specification_automatedbraking.md, specification_dps.md, specification_spacebasedsystem.md}`（3 份 NL 规约，2764 / 1247 / 1997 B）＋ `LLMApproach/{automatedbraking, dps, spacebasedsystem, dps_forStepByStepIllustration}.xml`（TTool 模型，175 KB–1.33 MB）＋ `DependencyGraphApproach/SoSyM_graphEval.xml`（561 KB）＋ `README.md`（7372 B，含逐步复现指令）。⚠️ ⛔ **其中 4 个是 `.xml~` 编辑器备份文件** —— ⛔ 有效文件实为 9 个。⛔ **无 license 文件** |
| ⭐ ground truth / 逐条判定 | ⚠️ **🟠** | ⭐ 同上仓库 | ⚠️ **没有独立的 ground-truth 台账。** ⭐ 逐字（§6.1）："The model file presents diagrams **and detected inconsistencies** generated from the following stages" —— ⛔ 即判定结果**内嵌在 TTool 的 `.xml` 模型文件里**，⛔ 需装 TTool 才能读。⛔ **无 CSV / JSON 逐条结果，⛔ 无 `Errors` 那 6 条的清单，⛔ 无 Table 7 的可下载原始表** |
| ⭐ 实验结果细则 | ⚠️ **🟠** | ⭐ 论文 Table 7 / 8 ＋ Appendix B | ⛔ **只有论文内表格。** ⛔ Table 7 只到 diagram 粒度（24 行），⛔ 不到「哪一条不一致」粒度。⚠️ ⛔ **Appendix B（GPT-5.1 的完整检出清单）是一张图片**（`10270_2026_1388_Figl_HTML.png` 一族），⛔ 文本不可提取；⛔ §5.1.3/§5.2.2 里所有 LLM 输出示例同样是图片 |
| ⭐⭐ **prompt 是否公开** | ⭐⭐ **🟢** | ⭐ TTool 仓库 `src/main/java/ai/` | ⭐⭐ **公开，⭐ 且我方逐字实取了**。⭐ Data availability 逐字承诺："The source code of our implementation, **including the full prompts used for the automated interactions with the LLMs**, is hosted in TTool's Git repository"。⭐ 实取 5 个关键文件全部 `HTTP 200`：`AIUseCaseDiagram.java` (12343 B) · `AIBlockConnAttribWithSlicing.java` (12520 B) · `AIStateMachinesAndAttributes.java` (11231 B) · `AIDiagramCoherency.java` (4673 B) · `AIDiagramCoherencyWithFormalRules.java` (5353 B)。⭐ prompt 就是 Java 字符串常量，⭐ 可直接读（B3 已抄若干逐字） |
| ⭐ Artifact DOI（Zenodo/OSF/4open） | ⛔ **⚪** | — | ⛔ **不存在。** ⭐ 已检 Crossref `link` 字段（只有 Springer 自家两条）· Unpaywall `oa_locations`（只有 publisher 一条）· OpenAlex `locations`（Springer ＋ HAL）· Zenodo 检索。⛔ **无归档 DOI，⛔ 无版本快照 —— ⛔ 两个 git 仓库都可能漂移** |
| ⭐ 前作配套仓库（⭐ 顺手核） | ⭐ **🟢** | [github.com/zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) | ⭐ 工具输出逐字：`HEAD f2c52282cb · 文件 54（非文档 33）· release 0 · license 无`。⭐ 新仓 README 逐字承认血统："Most of its content comes from our the repository where we stored the companion data for our first works on the topic: https://github.com/zebradile/ttool-ai" |

### ⭐ 资产终裁（⛔ 机械判据之外的人工判断）

⭐⭐ **总体 🟢，⭐ 这是本轮资产最完整的一篇之一**：⭐ prompt 真的能读到逐字、⭐ NL 规约真的在、⭐ 工具真的开源（CeCILL）、⭐ 复现指令真的写了。⛔ **但两处扣分**：

1. ⛔ **逐条判定结果被锁在 TTool `.xml` 里** —— ⛔ 不装工具无法核 Table 7 的任何一行。⭐ 这就是「report reproducibility support ≠ 我们能取到东西」那条差（见 [verification_log.md](../verification_log.md) §6.4）的一个具体样本：⭐ 论文自陈完全可复现，⛔ 但**外部审查者拿不到可机读的逐条判定**。
2. ⛔ **无归档 DOI** —— ⭐ TTool HEAD 已经从论文里写的 build 14731/14863 走到了 `f9ff1501e9`（2026-07-27），⛔ **论文用的那两个 build 在 GitLab 上没有 tag/release 定位**（`release 0`）。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

| # | 可搬的设计决定 | ⭐ 证据强度 |
| :-: | :-- | :-- |
| **①** | ⭐⭐ **「再加一条不含 LLM 的确定性检测臂，两臂取并集」比「把 LLM 的裁决者换成 oracle」更好落地。** ⭐ 它的 Ct4 是 `[人] 打 tag → [确定性] 模型变换 → [确定性] 图遍历`，⛔ 零 LLM，⭐ 而拿到 Table 8 的 `0 误报 0 漏检`。⭐ **我们有 pyfcstm，完全可以照这个形状开第二臂** —— ⭐ 不改现有 discover 链，⛔ 只加一条并列的确定性谓词全扫臂，⭐ 结果取并集 | ⭐ **M**（形态明写、数字明写） |
| **②** | ⭐⭐ **确定性裁决者的循环收敛得非常快，快到不必报边际收益** —— ⭐ 上限 20 轮「never reached」，⭐ walkthrough 里一次反馈就修好 `RU8`。⭐ **这是我们「确定性那条 0 token 性价比最高、LLM 自评那两条零收益」的独立外部印证** | ⭐ **S**（从「never reached」＋单例推出；⛔ 无逐轮曲线） |
| **③** | ⭐⭐ **规则目录逐条挂 `justification` 列**，⭐ 分「文献/标准 · 元模型定义性 · 纯方法学」三类 —— ⭐⭐ **这与我们 provenance 三类分级同构，⭐ 且已在 CCF-B 顶刊过审。** ⭐ 更有用的是它的比例：⛔ **③ 类（无外部依据）占 19/38 = 50%**，⭐ 而我们只有 1/19 = 5.3%。⭐ **「我们的出处纪律比一篇 SoSyM 论文严一个数量级」是可写的** | ⭐ **M**（Table 1–6 的第三列逐条可数） |
| **④** | ⭐ **规则集自称 `pragmatic subset` 而非穷尽** —— ⭐ 逐字 "These rules **do not exhaustively cover** all the constraints […] they constitute a **pragmatic subset**"。⭐ 我们「19 条不穷尽、v46 只用到 15」可以照这个口径写，⛔ 不必当成缺陷 | ⭐ **M** |
| **⑤** | ⭐ **不利结果的写法**（→ C 节专节）：⭐⭐ **FP＋FN 写进摘要最后一句** ＋ 三节 Threats ＋ 主动说「我们的实验设计可能低估了自己」。⭐ 我们的 −15.82pp 可以照抄这个结构 | ⭐ **M** |
| **⑥** | ⭐ **prompt 直接以源码常量公开** —— ⛔ 不做附录截图、⛔ 不做「available upon request」。⭐ 我们本来就在源码里，⭐ 这条只是印证做法可行 | ⭐ **M** |

### 2. ⛔ 不可取 / 陷阱

| # | 陷阱 | ⚠️ 它踩没踩我们踩过的坑 |
| :-: | :-- | :-- |
| **①** | ⛔⛔ **`Errors` 被从分母里剔除，⛔ 且没有 recall 分母** —— ⭐ 逐字 "they are **excluded from the total inconsistency count**"。⛔ 于是 `92% relevant` 这个数**不是 precision 的常规算法**（⭐ 它其实是 `69/(69+6)`，⛔ 而 `85.5%` 的分母又是剔除后的 69）。⛔ **两个分母在同一小节里换了口径而没标注** | ⛔ **这正是本仓库 §3.5 第 4 条「评测口径迁就结果」的形态**。⭐ 我们的 98 条能力分母 ＋ `hit@1/@3/@all` 三口径同报，⭐ 比它严格得多 |
| **②** | ⛔⛔ **判定全由作者自己做，⛔ 无第三方、⛔ 无 $\kappa$、⛔ 无一致率** —— ⭐ 且作者自认 "potential for **confirmation bias**"、"inherent **subjectivity**"。⛔ 图法臂尤其：**同一批人设计缺陷模型、同一批人写检测算法、同一批人判对错，⛔ 然后拿到满分** | ⛔ **这是「自证式验证」（§3.5 第 5 条）**。⭐ 我们 574 位逐位 ＋ 288 簇五类的人工判定虽然也是自判，⛔ 但至少判据先落盘、⭐ 且逐位可复算 |
| **③** | ⛔⛔ **`n` 极小且无重复采样** —— ⭐ LLM 臂 12 个图对，⭐ 图法臂 **3 个模型**；⛔ 每格跑一次，⛔ 无 temperature/seed 记录，⛔ 无方差。⛔ **`0 误报 0 漏检` 建立在 `n=3` 上** | ⛔ 我们 324 格 × 3 轮 ＋ `@k` 三口径，⭐ 这一点上我们强得多。⛔ **不要被它 Table 8 的满分吓到 —— ⛔ 那不是可比数字** |
| **④** | ⛔ **`0.5` 的半分从哪来，⛔ 论文一个字都没解释** —— ⭐ Table 7 里出现 `3.5` `2.5` `1.5` `0.5`（⭐ 共 6 处），⛔ 全文 grep 无 `partial` / `half` / 打分细则。⛔ **半分直接进了 `59/69 = 85.5%` 这个主结果** | ⛔ **判定规则未落盘的典型** |
| **⑤** | ⚠️ **纠正阶段「哪些条目要修」由人挑** —— ⭐ 逐字 "the list of inconsistencies is **(partially or totally) incorporated by the user**"，⛔ 且 `Errors` 那 6 条被人**先剔掉**才进纠正。⛔ **所以 85.5% 的纠正率是「人已经把错的滤掉之后」的纠正率**，⛔ 不是端到端自动率 | ⛔ 若我们要报修复率，⭐ **必须区分「端到端」与「人已过滤」两个口径** |
| **⑥** | ⚠️ **外环第 2 轮没跑** —— ⭐ 逐字 "**Another iteration** on inconsistency detection (stages C1 to C3) **could resolve** these remaining issues"。⛔ **「could」是猜的，⛔ 没有数据** | ⚠️ ⭐ 我们有那条数据（第 3–5 轮零收益），⛔ 而且方向相反。⭐ **别把它的「再跑一轮应该能好」当成先例信** |
| **⑦** | ⛔⛔ **把规则注进检测 prompt 会造成隧道视野** —— ⭐ 逐字 "the LLM tends to **exclusively focus on these rules, thus ignoring other consistency aspects**"。⛔ 他们的对策是**跑两遍取并集**（⭐ 一遍带规则一遍不带），⛔ **而不是修规则的措辞** | ⭐⭐ **这是我们已经踩过的坑的外部独立复现**：⭐ `occupancy_after` 的 `nl_cue` 把模型从 `edge_declared` 引开，⛔ 324 格里 `edge_declared` 被问 **0.0%**。⛔ **注意他们的对策（跑两遍）对我们不适用 —— ⭐ 我们成本已经 212.6×，⛔ 翻倍不可接受；⭐ 我们的解是修 `nl_cue`（实测 0 → 4/6）** |
| **⑧** | ⛔ **Ct4 的跨视图链接由人手工打 tag** —— ⭐ 这是整个漂亮结果的前提，⛔ 而作者承认 "the overall validity of the method **heavily depends on the quality and accuracy of the model annotations provided by the engineer**"，⛔ 且**没测打 tag 花了多少时间**（Construct validity 逐字："do not account for the time spent by users either in tagging the models or in analyzing the identified inconsistencies"） | ⛔ **它把最贵的一步移出了度量范围**。⚠️ ⭐ 我们若要开确定性第二臂，⛔ **必须先回答「跨视图链接谁建」—— ⛔ 若答案是人，那条臂的成本就不是零** |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| # | 差别 | ⛔ 为什么阻断照搬 |
| :-: | :-- | :-- |
| **①** | ⛔⛔ **问题不同：⭐ 它是多视图模型互比，⭐ 我们是模型 vs NL** | ⛔ 它的 reference 是**另一个形式化制品**（UCD 图），⭐ 所以可以做**图对图的确定性遍历**。⛔⛔ **我们的 reference 是自然语言，⛔ 无法变换成图 —— ⛔ Ct4 那条确定性臂在我们这里根本无法原样存在。** ⭐ 我们能搬的只有「确定性臂与 LLM 臂并列」这个**架构形状**，⛔ 不是它的算法 |
| **②** | ⛔ **它的确定性臂依赖人工 tag 建链接** | ⭐ 它自己说得很清楚（§2.1 逐字）："The LLM-based method, **Ct3, requires no prior linking** […] Conversely, the graph-based method, **Ct4, depends on establishing pseudo-links**, for example, by annotating model elements with the system function(s) they represent." ⛔⛔ **我们的 54 pair 没有这种 tag，⛔ 建它就是一次全量人工标注 —— ⛔ 成本量级与 G1 重标相当** |
| **③** | ⛔ **中间表示的「谁选类」完全相反** | ⭐ 它：**三份硬编码名单**（`D1.1` 注哪几条、`D1.3` 查哪几条、`D1.5` 强制哪几条），⛔ 与被检对象无关。⭐ 我们：**LLM 逐需求自动选**。⛔⛔ **所以它对「闭合词表 ＋ LLM 自动选」这个组合给不出任何先例** —— ⚠️ ⭐ 本轨要数的那个组合，⛔ **这篇不算一票** |
| **④** | ⛔ **它的 LLM 输出无结构** | ⛔ `{"diagram": ..., "description": <自由文本>}`，⛔ 无类别、⛔ 无谓词、⛔ 无可机械求值的断言。⛔⛔ **所以它的「检出」永远需要人读，⛔ 而我们的断言脚本可以机械求值。⭐ 这是我们相对它的结构性优势，⛔ 也意味着它的 92%/85.5% 与我们的任何数字都不可比** |
| **⑤** | ⛔ **模型代际混杂** | ⭐ Table 7 全部来自 GPT-3.5/GPT-4；⭐ 只有 §5.2.2 那一次用 GPT-5.1。⛔⛔ **引用它的定量数字时必须标模型代次**，⛔ 否则会被质疑。⭐ **反过来，「GPT-5.1 仍看不见两跳路径」那条不受代际折扣影响，⭐ 是这篇最耐久的发现** |

---

## F. 存疑与未核项

1. ⚠️ **Appendix B 的 GPT-5.1 完整检出清单读不到** —— ⭐ 已试渲染代理取正文（拿到 Appendix A 的 glossary 全文）、⭐ 取原始 HTML 680 KB 定位 `id="Sec44"`；⛔ 结果：**Appendix B 正文是图片**（`10270_2026_1388_Figl_HTML.png` 一族，`media.springernature.com`），⛔ HTML 里只有 `<div class="c-article-section__figure-content">`。⛔ **所以「3 个误报」的具体内容我只拿到 §5.2.2 引述的那 1 条**，⛔ 另 2 条未知。⚠️ ⭐ 同理，§5.1.3/§5.1.4/§5.2.2 的全部 prompt/输出示例（figure e–m，共 9 张）都是图片，⛔ 未 OCR。
2. ⚠️ **Table 7 那 6 条 `Errors` 的具体内容只知道两条** —— ⭐ 论文举了「说两个已连接的块应该连起来」（§6.1.1 逐字 "such as the erroneous assertion that two already connected blocks should be connected"）与 §5.1.3 那条 Controller/User 的；⛔ 其余 4 条未列。⛔ **仓库里也没有可机读的 Errors 清单**（判定内嵌在 `.xml`）。
3. ⛔⛔ **§6.3 的 `87%` 复算不出来（⭐ 我方实测，⛔ 这是一条真实的数字缺陷，⛔ 不是我没找到口径）** —— ⭐ 我把 Table 7 的 24 行全部录入并按三种自然聚合复算：**逐图宏平均（20 张有分母的图）= 85.82%** · **逐图对宏平均（12 对）= 83.49%** · **逐系统宏平均（3 个系统）= 84.08%** · **micro（`59/69`）= 85.51%**。⛔ **四个数里没有 87%。** ⭐ 论文逐字给的区间 "ranges from **50% to 100%** per diagram" 唯一匹配「逐图宏平均」那一档（⭐ 我方复算 min = 50%、max = 100%，✅ 逐字对上），⛔ **而那一档是 85.8%。** ⚠️ ⭐ 最可能是 `85.8 → 87` 的抄写或四舍五入错误，⛔ **但我不为它编一个能凑出 87% 的口径 —— ⛔ 标为「复算不出」。** ⭐ 复算脚本已就地跑过，⛔ 未落盘。
4. ⚠️ **`0.5` 半分的判定规则未知** —— ⛔ 已 grep 全文 `partial` / `half` / `0.5` / `counted as`，⛔ 无任何打分细则。⛔ **6 处半分直接进了主结果 `59/69`。**
5. ⭐ **Table 7 的内部自洽性我方已机械复核，✅ 全部通过（⛔ 此项不是存疑，⭐ 保留以说明核过）** —— ⭐ 24 行逐行验 `Internal + Cross-view = Total`（`Errors` **不**计入 `Total`，⭐ 论文明写）：**24/24 通过**；⭐ 逐行验 `Corr.Int + Corr.Cross = Corr.Total 的分子` 且 `分母 = Total`：**20/20 通过**（⭐ 4 行 `Total = 0` 的分母栏为 `–`）。⭐ 合计栏亦全部对上：`36 / 33 / 6 / 69 / 28.5 / 30.5 / 59`。⭐ 另复算出论文正文那两个未列中间量：**BD 侧 49 条、`49/12 = 4.08`**（↔ 论文 "averaging 4"）· **UCD 侧 20 条、`20/12 = 1.67`**（↔ 论文 "1.7"）。
6. ⚠️ **无法核 Table 7/8 的任何一行** —— ⛔ 逐条判定内嵌在 TTool `.xml`（175 KB–1.33 MB），⛔ 需装 TTool 3.0 beta 才能打开。⛔ **本卡未装 TTool，⛔ 所以 Table 7/8 的数字只做了内部自洽复算（✅ 全对），⛔ 未做与原始制品的对拍。**
7. ⚠️ **论文用的 TTool build 14731 / 14863 定位不到** —— ⭐ 已查 GitLab project 225：`release 0`，⛔ 无 tag。⛔ 当前 HEAD `f9ff1501e9`（2026-07-27）已远离评测时的 build。⛔ **无法取到评测时的确切代码版本。**
8. ⚠️ **HAL 上没有全文** —— ⭐ 已查 HAL API（`fileMain_s: None`）与落地页 [hal-05682394v1](https://telecom-paris.hal.science/hal-05682394v1)（`HTTP 200`，⛔ 页面无 document/file 链接）；⭐ OpenAlex 也标该 location `is_oa: false`。⛔ **CC-BY 的论文只在 Springer 一处，⛔ 而 Springer 有 WAF。**
9. ⚠️ **作者主页有 `.bib` 但无作者版 PDF** —— ⭐ 已取 [perso.telecom-paristech.fr/apvrille/research_publications.html](https://perso.telecom-paristech.fr/apvrille/research_publications.html)（`HTTP 200`, 123635 B），⭐ 该条目逐字只挂 `online paper (open access)` ＋ `./docs/sosym_sultan_july2026.bib`，⛔ **没有 author-version PDF 链接**（⭐ 对比：同页 MODELSWARD'2026 与 SysCon'2026 条目都有 `paper (author version)`）。
10. ⚠️ **前作 MODELS'24 未读** —— ⭐ 本篇是它的期刊扩展版，⭐ Ct2/Ct3 大部分来自那篇（⭐ 且拿了 **DISTINGUISHED PAPER AWARD**，见作者主页文件名 `models2024_sultan_distinguishedpaperaward.pdf`）。⭐ 全文可取（[perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf](https://perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf)），⛔ **但本卡未读它**。⚠️ ⭐ 若要追「Ct3 的原始实验数据」（本篇 Table 7 是不是就是那篇的表），⭐ 必须读那篇。
11. ⚠️ **同组还有两篇 2026 年的强相关工作未读** —— ⭐ 从作者主页实取到条目：⭐ **B. Sultan, L. Apvrille, "Towards Safe LLM-Based Model Driven Engineering: when Syntax Checking and Safety Formal Verification Join the Loop", ERTS 2026**（[hal.science/hal-05513959](https://hal.science/hal-05513959)）—— ⚠️⚠️ **标题里 "Safety Formal Verification Join the Loop" 直指我们「把裁决者换成 sound oracle」那条设计原则**，⛔ **本卡未读，⭐ 强烈建议单独抽一张卡**；⭐ 以及 **L. Apvrille, B. Sultan, "Continuous AI Assistance for Model-Driven Engineering", MODELSWARD 2026**（[docs/apvrille_modelsward2026.pdf](https://perso.telecom-paristech.fr/apvrille/docs/apvrille_modelsward2026.pdf)）。
12. ⚠️ **`boundary` 判 `邻域` 是我方裁定，⛔ 不是论文明说** —— ⭐ 依据是 Definition 3 的 `after ∈ ℕ`（M，逐字 "constrains the delay before firing"）与块间 `send→receive` 并发同步（M）。⛔ **若后续要把这篇搬进 L1/L2，⛔ 必须在这两点上重走边界门。**
13. ⚠️ **未核「同义词/命名类不一致」在 69 条里占多少** —— ⭐ 这是它唯一真正支撑「规则法不够」的那一类，⛔ 但 Table 7 只分 internal/cross-view，⛔ 不分类别。⛔ **所以「LLM 相对规则法的净增益有多大」这个数，⛔ 这篇没有。** ⭐ 论文自己也把它列为 future work（逐字："Ideally, we should also develop a **taxonomy of common inconsistency types** and assess the extent to which the approach addresses each category"）。
