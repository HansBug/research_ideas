# 综合卡 · 行为模型缺陷类型学 × 反馈信号取自哪里

⚠️ **这不是一张逐篇卡。** ⭐ 它回答两个横向问题，⛔ 因此不按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 的 A–F 逐篇展开，⭐ 但**证据级别纪律照旧**：每条断言标 **M / S / I**，⭐ M 必附逐字英文片段并注明出自哪一节。

⭐ **覆盖的五份工作**（⭐ 全部实际访问过；⛔ 一份全文不可得，已在 §F 列出试过的入口）：

| 代号 | 标题 | 年 | Venue | CCF | 入口 | 全文 |
| :-- | :-- | :-: | :-- | :-: | :-- | :-: |
| **T-A** | Accurate and Consistent Graph Model Generation from Text with Large Language Models（**AbsCon**） | 2025 | MODELS 2025 | B | [arXiv:2508.00255](https://arxiv.org/abs/2508.00255) | ⭐ 🟢 [HTML v1](https://arxiv.org/html/2508.00255v1) |
| **T-B** | Assessing the Business Process Modeling Competences of Large Language Models（**BEF4LLM**） | 2026 | Information Systems, Vol. 142, Art. 102761 | ⚠️ 未收录于本仓库 [ccf_venues/](../../../../../ccf_venues/) | [arXiv:2601.21787](https://arxiv.org/abs/2601.21787) · [DOI 10.1016/j.is.2026.102761](https://doi.org/10.1016/j.is.2026.102761) | ⭐ 🟢 [HTML v2](https://arxiv.org/html/2601.21787v2) |
| **T-C** | Improving LLM-Generated Process Model Quality Through Reinforcement Learning: The Role of Reward Function Design | 2026 | ⚠️ **仅 arXiv 预印本**，未列 venue | 无 | [arXiv:2607.06175](https://arxiv.org/abs/2607.06175) | ⭐ 🟢 [HTML v1](https://arxiv.org/html/2607.06175v1) |
| **F-A** | A Formalism-Aware Reward Loop for Handwritten UML-to-PlantUML Generation | 2026 | ⭐ **MODELS 2026 · NIER track** | B | [arXiv:2607.28987](https://arxiv.org/abs/2607.28987) | ⭐ 🟢 [HTML v1](https://arxiv.org/html/2607.28987v1) |
| **F-B** | ITG: Trace Generation via Iterative Interaction between LLM Query and Trace Checking | 2024 | ICSE-NIER 2024, pp. 11–15 | A | [DOI 10.1145/3639476.3639779](https://doi.org/10.1145/3639476.3639779) | ⛔ **不可得** |

⭐ **T-B / T-C 的 CCF 与 venue 备注**：Elsevier *Information Systems* 在本仓库 [ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 里**没有条目**（⭐ 那里的 `journal-b-ist` 是 *Information and Software Technology*，⛔ 不是同一刊）—— ⛔ 不要把它当成已核 CCF 等级。⚠️ T-C 的 arXiv abs 页**不列任何 venue**，⛔ 因此在对照表里只能当预印本用。

---

## ⛔⛔ 先说一条会改变结论的发现：**「三份分类学」实际只有两份**

⭐⭐ **T-C 的「38 项指标」就是 T-B 的 BEF4LLM 框架，⛔ 不是第三套独立分类学。**

⭐ **证据（M · T-C §1 Introduction 逐字）**：

> "the BEF4LLM evaluation framework [26] provides **38 automated metrics** across three established quality dimensions (syntactic, pragmatic, and semantic quality) that can serve directly as reward signals"

⭐ **再一处（M · T-C §2.2 逐字）**：

> "26 introduce BEF4LLM, a framework comprising **38 metrics** across syntactic, pragmatic, and semantic quality dimensions, and benchmark **17 open-source LLMs** on BPMN generation"

⭐ **算术对得上（M）**：T-B §4 逐字 —— "In total, the BEF4LLM framework comprises **39 individual metrics: One for validity, 16 for syntactic quality, 15 for pragmatic quality, and seven for semantic quality**." ⭐ T-C 只把 **validity** 拿出来当罚项（`p ∈ {−1, 0}`），⛔ 不进奖励的质量项，⭐ 于是 `16 + 15 + 7 = 38`。

⭐ **作者集合也重合（M）**：T-B 作者 Chantale **Lauer**, Peter Pfeiffer, Alexander **Rombach**, Nijat **Mehdiyev**；T-C 作者 Alexander **Rombach**, Chantale **Lauer**, Nijat **Mehdiyev**。⛔ 同一组人、同一框架、⭐ T-C 只是把它当 RL 奖励源。

⛔⛔ **后果**：⭐ 初筛记的「三份现成分类学」应改成 **两份**（T-A 三分法 · T-B/T-C 四视角 39 项）⭐ 外加**第三份此前没登记的**——⭐ **F-A §4.3 归纳出的 8 类错误分类学**（见下 §1.4），⭐ 而那一份恰恰是三者里**唯一同时带方向轴与深度轴**的。

---

# ⭐⭐ 问题一 · 现成的行为模型缺陷类型学

## 1.1 · T-A（AbsCon）三分法

⭐ **制品**：labeled graph $G = (\mathcal{N}, \mathcal{E}, \mathtt{L})$，⭐ 实测落在 **Mermaid** 文本上（flowchart / taxonomy / program graph 三类）。⚠️ **明确忽略节点属性**（M · §II-A 逐字："**this paper ignores node attributes** and defines a labeled graph"）—— ⛔ 这一句对我们的变量维空缺很关键，见 §2.3。

⭐ **三类逐字抄下（M · Abstract + §I Problem statement，两处措辞略有差异，⭐ 两份都抄）**：

| # | Abstract 里的名字（逐字） | Abstract 里的定义（逐字） | §I 里的名字（逐字） |
| :-: | :-- | :-- | :-- |
| 1 | **"syntax violations"** | "the generated model may not adhere to the syntax defined by its metamodel" | **"syntax"** |
| 2 | **"constraint inconsistencies"** | "the structure of the model might not conform to some domain-specific constraints" | **"consistency"** |
| 3 | **"inaccuracy"** | "due to the inherent uncertainty in LLMs, the models can include inaccurate, hallucinated elements" | **"quality"** |

⚠️ **两处命名不一致本身是个信号（S）**：⭐ Abstract 用缺陷名（violations / inconsistencies / inaccuracy），§I 用维度名（syntax / consistency / quality）。⭐ 我们 G1 定 `statement` 字段时会遇到同一个岔路口：**是写「缺陷是什么」还是写「哪个维度不合格」**。⛔ T-A 自己没统一。

### ⭐ 判据是什么 —— 谁来判、能不能机械判

| 类 | 判据 | 谁判 | ⭐ 能否机械判 |
| :-: | :-- | :-- | :-- |
| 1 · syntax | ⭐ **能不能被解析成图** | ⭐ Mermaid parser | ⭐⭐ **完全机械** |
| 2 · consistency | ⭐ **一组显式写出的 well-formedness 约束**（⭐ 论文给的 flowchart 例子是 **5 条**） | ⭐ 约束求解器（**CBC** solver） | ⭐⭐ **完全机械** |
| 3 · inaccuracy | ⛔ **对着 ground-truth 模型算 soft precision / recall / F1**（⛔ 不是对着 NL 描述） | ⭐ 自动脚本 | ⚠️ **机械但换了对象** |

⭐⭐ **第 3 类的判据是本卡最重要的一处细节（M · §V-B Metrics 逐字）**：

> "Since **automated comparison of a graph model with the natural language description may be unreliable**, we evaluate model quality using either downstream task performance or **ground truth comparison**"

⛔⛔ **也就是说：T-A 定义第 3 类时说的是「相对描述不准确」，⭐ 但测的时候换成了「相对参考模型不像」。** ⭐ 这个替换他们自己写明了理由，⛔ 但它意味着 **T-A 的第 3 类不可直接给我们用** —— 我们的 discover 任务**只有 NL，没有参考模型**。

⭐ 那 5 条 flowchart 约束逐字（M · §III-A）：

> "a valid instance flowchart must: (1) have a **single starting node**; (2) allow **reaching every other node from the starting node**; (3) require **decision nodes to have at least two targets**; (4) ensure that each **outgoing relation from a decision node has a non-empty condition**; and (5) contain **no self-cycles**."

### ⭐ 有没有实测各类占比

| 类 | ⭐ 实测数字 |
| :-: | :-- |
| 1 · syntax | ⛔ **没给占比。** ⭐ 只有定性句（M · §III-C 逐字）："we observe that **LLMs rarely produce syntax errors** when using the Mermaid diagramming language" —— ⭐ 且他们**直接把语法错的样本过滤掉**（"filter out any generated models with syntax errors"） |
| 2 · consistency | ⭐⭐ **有。** ⭐ `Con` 列 = 满足全部约束的模型百分比。⭐ **Direct 基线**：PAGED **93.25 / 94.48 / 95.40 / 96.63**（Llama3.1-70b / 8b / GPT-4o-mini / GPT-4o）→ ⭐ **只有 3.4%–6.8% 违反约束**；⭐ WordNet **65.00 / 78.00 / 83.00 / 95.00** → ⛔ **最差 35% 违反** |
| 3 · inaccuracy | ⚠️ **只有聚合 F1，⛔ 没有按缺陷子类拆。** ⭐ Direct 基线 F1：PAGED **75.19–79.54**，WordNet **59.20–71.14** |

## 1.2 · T-B（BEF4LLM）四视角 · 39 项指标

⭐ **制品**：**BPMN 2.0 XML**（⭐ 不是状态机）。⭐ **它建在 SIQ 框架之上**（M · §1 逐字："building on the **SIQ** framework [47], which comprises 39 metrics ... across **four quality dimensions**"）。

⭐ **四视角逐字（M · Abstract）**："**syntactic quality, pragmatic quality, semantic quality, and validity**"

### ⭐ 39 项逐条抄下

**① Validity（1 项）** —— ⭐ 判据逐字（M · §4.4）："checks whether the **BPMN XML file is parsable**" · "We check the validity $Q_{\text{val}}$ of the BPMN XML **based on the XSD schema**"

⭐⭐ **它被刻意从 syntactic 里拆出来，理由逐字（M · §4.4）**：

> "**validity serves as a gatekeeping criterion** as the remaining metrics can only be computed if a valid BPMN XML file is available. Moreover, **validity and syntactic quality operate at different layers**. While syntactic quality captures conformance to **BPMN modeling rules**, validity captures conformance to the **BPMN XML schema**."

**② Syntactic quality（16 项，Table 2 逐条）**：

| # | 逐字 | # | 逐字 |
| :-: | :-- | :-: | :-- |
| 1 | Existence of a start event | 9 | Split gateway has matching join gateway |
| 2 | Existence of an end event | 10 | Exactly one process per pool |
| 3 | One start event per process | 11 | Each observable task has a label |
| 4 | One end event per process | 12 | Task: $in=1$, $out=1$ |
| 5 | Sequence-flow connection rules | 13 | Non-exception intermediate event: $in=1$, $out=1$ |
| 6 | Message-flow connection rules | 14 | Exception event: $in=0$, $out=1$ |
| 7 | Start event: $in=0$, $out=1$ | 15 | Split gateway: $in=1$, $out>1$ |
| 8 | End event: $in=1$, $out=0$ | 16 | Join gateway: $in>1$, $out=1$ |

**③ Pragmatic quality（15 项，Table 3 逐条，⭐ 分六类但只用了五类）**：

| 类 | 指标（逐字） |
| :-- | :-- |
| Size | 1 TNN (total number of nodes) · 2 TNG (total number of gateways) · 3 TNSF (total number of sequence flows) · 4 TNMF (total number of message flows) · 5 Diameter |
| Density | 6 Density · 7 AGD (average gateway degree) · 8 CNC (connectivity coefficient) |
| Connector interplay | 9 GH (gateway heterogeneity) · 10 CFC (control-flow complexity) · 11 CC (cross-connectivity) |
| Partitionability | 12 Sequentiality · 13 Separability · 14 Depth |
| Concurrency | 15 TS (token split) |
| ⛔ **Cyclicity** | ⛔ **列在分类里但被删掉了** |

⭐ Cyclicity 被删的理由逐字（M · §4.2）："**Cyclicity ... is not included** in the BEF4LLM framework because existing research **does not provide multiple thresholds** for cyclicity metrics" —— ⚠️ ⭐ **一条纯粹因为「没有可用阈值」而被砍掉的维度**；⛔ 不是因为它不重要。

**④ Semantic quality（7 项，Table 4 逐条）**：

| 组 | 指标（逐字） |
| :-- | :-- |
| Natural-language similarity | 1 Syntactic label similarity · 2 Semantic label similarity · 3 Context similarity |
| Graph-structure similarity | 4 Graph-edit distance · 5 Common nodes and edges |
| Behavioural similarity | 6 Causal-footprint overlap · 7 Dependency-graph overlap |

### ⭐ 判据是什么 —— 谁来判、能不能机械判

⭐⭐ **全部机械，⛔ 而且「能否机械判」是入选的硬门（M · §4 逐字）**：

> "each selected metric **must be computable fully automatically** from a generated BPMN-XML file and a corresponding ground-truth process model (for semantic quality). This implies that **metrics that require manual human judgment are excluded from the framework**"

⭐ 三类归一化方式各不相同（M）：

- **Syntactic**：布尔（0/1）**或** 比例（"dividing the number of elements **not following the rule** by the total number of elements covered by this rule"）
- **Pragmatic**：⭐ **四个经验阈值切成五组**（`norm_desc` / `norm_asc`），⭐ 阈值取自既有文献。⭐ 举例逐字："a BPMN model with 45 nodes ... $t_1=29.9$, $t_2=43.7$, $t_3=58.1$, $t_4=81.1$ ... the score $0.5$ is assigned"
- **Semantic**：⛔ **必须有 ground-truth 模型**（M · §4.3 逐字："Directly verifying these properties against the real world is **impractical**, so we **compare a candidate process model** $M_c$ **with a ground-truth process model** $M_g$")

⚠️ **T-B 自陈的 semantic 局限逐字（M · §4.3 结尾）** —— ⭐ 这一段值得整段搬进我们的 Limitations：

> "Semantic quality is assessed via similarity to a ground-truth model, which **constrains the evaluation to what is expressed in that reference**. Label-based similarity metrics further restrict the assessment by approximating equivalence through one-to-one matching, even when employing synonym handling and related techniques, and **may therefore penalize valid alternative phrasings or differences in granularity**."

### ⭐ 有没有实测各类占比

⭐⭐ **有，而且是本卡里最扎实的一组（M · §6）**：⭐ 17 个开源 LLM × 105 个 text-BPMN pair × 5 次 = **8,925 次运行**，⭐ 耗时约 5 天。

| 维度 | ⭐ 实测 |
| :-- | :-- |
| Validity | ⛔ **最差的一维**：`$Q_{val}$` 从 **0.3067**（falcon3:10b）到 **0.9733**（llama3.3:70b）。⭐ 逐字："**Only llama3.3:70b-instruct reached a validity correctness of above 90%**" —— ⛔ 且这是**已经允许一轮 refinement 之后**的数字 |
| Syntactic | ⭐ 全部 > **0.75**（最高 falcon3:10b **0.9082**） |
| Pragmatic | ⭐ 全部 > **0.8**（最高 qwen2.5:14b **0.8907**）—— ⭐ 逐字："The pragmatic quality has therefore reached a **practical ceiling**" |
| Semantic | ⛔⛔ **系统性落后**：最高 qwen2.5:32b **0.5768**；⭐ 逐字："**semantic quality consistently lagged behind**" |
| ⭐ 人类专家对照 | ⭐⭐ **有**（⛔ 另建德语小数据集）：⭐ 专家 semantic **0.5152** 是全场最高；⛔ 但 syntactic / pragmatic **多个 LLM 反超人类**。⭐ 逐字："**LLMs make fewer syntactic errors, while humans reflect more on the textual descriptions and the overall semantic quality**" |

⭐ **另一处极其可用的实测（M · T-C §5.1.1 逐字）** —— ⭐ 把 syntactic 分数换算成**违规条数**：

> "the syntactic gain corresponds to approximately 1.5 additional BPMN rules satisfied per model (out of 16), **reducing average rule violations from 2.8 to 1.2**"

⭐ 即 SFT-only 的 Llama 平均违反 **2.8/16 = 17.5%** 的 BPMN 语法规则。

## 1.3 · T-C 的分类学 = T-B 的分类学

⛔ **不重复抄。** ⭐ T-C 对分类学**没有任何新增或改动**，⭐ 它的贡献在奖励函数组合（见 §2.2）。⭐ 唯一新增的是三类各自的**类别小结**（M · §3.3）：syntactic 的 16 项"span **three categories** of modeling rules"、pragmatic 的 15 项"organized into **five categories**" —— ⚠️ ⭐ 注意 pragmatic 在 T-B 里写的是**六类删一类剩五类**，⭐ T-C 直接写五类，⛔ **两处对不上口径但不矛盾**。

## 1.4 · ⭐⭐ 第三份分类学（此前未登记）：F-A §4.3 的 8 类

⭐ **这一份初筛没记，⭐ 但它是三份里唯一带方向轴的。**

⭐ **逐字（M · F-A §4.3）**：

> "grouping recurring mistakes with an **inductively derived taxonomy** covering failures of **extraction, compilation, recognition, typing, structure, hallucination, omission, and cosmetic fidelity**."

⭐ **8 类**：`extraction` · `compilation` · `recognition` · `typing` · `structure` · `hallucination` · `omission` · `cosmetic fidelity`

### ⭐ 判据 · 占比 —— ⛔ 它自己主动否认可测量性

⭐⭐ **逐字（M · §4.3，紧接上句）**：

> "The taxonomy is **an organising scheme rather than a measurement instrument**: given the **interpretive nature of the labelling** and the modest sample, we characterise dominant patterns rather than **report per-category frequencies**."

⛔ **所以：判据是人工解释性标注（作者自己，120 个输出 = 4 模型 × 30 图），⛔ 无占比、⛔ 无标注者间一致性。**

⭐⭐ **但它给出了一条我们能直接用的二分（M · §4.3 逐字）** —— ⭐ 这可能是本卡对 G1 最有用的一句：

> "the distinction between **meaning-preserving deviations and meaning-altering errors**. The former changes the representation while keeping the intended interpretation ... **Representation-based rewards penalise both** whenever they differ from the target representation, **whereas human raters need not**"

⭐ 具体反例逐字（M · §4.3 + Fig. 2）："the model renders the sketch's decision as a **switch-branch** where the reference uses an **if-branch**. **Both produce structurally identical diagrams and preserve the decision logic**, yet the control-flow-graph reward scores the switch as a deviation."

---

## ⭐⭐ 1.5 · 对照表：三份分类学 × 我们的 19 条谓词族

⭐ 我们的 19 条（出处见 [../../provenance/predicate_provenance.md](../../provenance/predicate_provenance.md)）：

- **结构 S · 10 条**：`state_declared` `event_declared` `variable_declared` `action_declared` `effect_declared` `edge_declared` `initial_target` `containment` `cardinality` `guard_distinguishable`
- **仿真 B · 6 条**：`reaches` `occupancy_after` `event_consumed` `terminates` `stays_in` `variable_delta_after`
- **BMC P · 3 条**：`invariant` `response_within` `persists_until`

### 表 1 · T-A 三类 → 我们

| T-A 类 | ⭐ 我们哪里接得住 | 覆盖 |
| :-- | :-- | :-: |
| 1 · syntax violations | ⛔ **不是谓词接的** —— ⭐ 由 `precheck_and_seal` 里的 **pyfcstm parse / semantic facade** 接。⚠️ 且我们的被测制品**进来就已经可解析**，⭐ 与 T-A「先 filter 掉语法错样本」是同一个处置 | ⚠️ **口径外** |
| 2 · constraint inconsistencies | ⭐⭐ **正对我们的结构族 10 条。** ⭐ 它那 5 条 flowchart 约束逐条落点：(1) single starting node → `initial_target` + `cardinality`；(2) reaching every other node → `reaches`；(3) decision ≥ 2 targets → `cardinality`；(4) non-empty condition → `guard_distinguishable`；⛔ (5) **no self-cycles → 我们没有对应谓词** | ⭐ **4/5** |
| 3 · inaccuracy / hallucinated elements | ⚠️ **半接。** ⭐ `*_declared` 家族抓「模型里用了但没声明」；⛔ 但 T-A 这一类**同时含「模型里多出来的元素」**，⭐ 而我们 19 条里**只有 `state_declared` 明写「缺失或多余」**（⛔ `variable_declared` 没写，⭐ 已在 provenance 表记为待 R1 裁的形状问题） | ⚠️ **方向轴残缺** |

### 表 2 · T-B / T-C 四视角 39 项 → 我们

| T-B 视角 | 项数 | ⭐ 我们哪里接得住 | 覆盖 |
| :-- | :-: | :-- | :-: |
| **Validity**（XSD 可解析） | 1 | ⭐ pyfcstm parse gate（⛔ 确定性层，⛔ 不是谓词） | ⚠️ 口径外 |
| **Syntactic**（BPMN 建模规则） | 16 | ⭐ #1–4（start/end 存在性 + 唯一性）→ `initial_target` + `cardinality`；⭐ #5–6（flow 连接规则）→ `edge_declared`；⭐ #7–8 #12–16（**度数规则** $in/out$）→ `cardinality` + `edge_declared`；⭐ #11（task 有 label）→ `action_declared` / `effect_declared`；⛔ **#9（split 有匹配 join）· #10（每 pool 一个 process）无对应** —— ⭐ 且 #9 本就在我们的**并发界外** | ⭐ **约 14/16** |
| **Pragmatic**（size / density / connector interplay / partitionability / concurrency） | 15 | ⛔⛔ **零。** ⛔ 我们 19 条里**没有任何一条**度量模型的规模、密度、可理解性或复杂度 | ⛔⛔ **0/15** |
| **Semantic**（label / graph / behavioural similarity） | 7 | ⛔ **结构性不适用** —— ⭐ 全部 7 项都要 **ground-truth 模型**做参照，⭐ 而我们的 discover 任务**只有 NL、没有参考模型**。⚠️ 最近的类比是 #6–7（causal-footprint / dependency-graph overlap）↔ 我们的仿真族 6 条，⛔ 但**方向相反**：他们量「与参考像不像」，我们量「对着 NL 成不成立」 | ⛔ **0/7 可直接用** |

### ⭐ 表 3 · F-A 8 类 → 我们（⭐ 这张才是给 G1 的 issue 字段用的）

| F-A 类 | ⭐ 对 G1 哪个字段说话 | 我们现状 |
| :-- | :-- | :-- |
| `extraction` / `recognition` | ⚠️ **F-A 专属** —— 它的输入是**手写草图图像**，这两类是视觉识别错。⛔ 我们输入是 NL 文本，无对应 | ⛔ 不适用 |
| `compilation` | ⭐ `depth` 的最浅一档 | ⭐ pyfcstm parse gate |
| `typing` | ⭐ `depth` 的第二档 | ⭐ 结构族 `*_declared` |
| `structure` | ⭐ `depth` 的第三档 | ⭐ 结构族 + `containment` |
| ⭐⭐ `hallucination` vs `omission` | ⭐⭐ **`direction` 字段的直接先例** —— ⭐ 两者被列为**并列的两类**，⛔ 不是一类的两个符号 | ⚠️ 我们只有 `state_declared` 明写双向 |
| `cosmetic fidelity` | ⚠️ 可对应 G1 的「不算缺陷」档 | ⛔ 我们台账没有这一档 |

---

## ⭐⭐ 1.6 · 对照表的结论：⛔ 我们覆盖不到哪些类

### ⛔ 结论 1 · 变量维空缺，**⛔ 分类学层面根本没得抄**

⭐ 我们的实测事实（M · 本仓库 [../../../discover_matrix/docs/findings/v46_weakness_anatomy.md](../../../discover_matrix/docs/findings/v46_weakness_anatomy.md) §）：`variable_declared` / `variable_delta_after` / `response_within` / `invariant` **四条从未作为 primary 出现**。

⭐⭐ **三份分类学里也全是空的，⭐ 而且两份是明确声明排除的：**

1. ⭐ **T-A（M · §II-A 逐字）**："**this paper ignores node attributes**"
2. ⭐ **T-B（M · §4 结尾逐字）**："we **exclude artifacts** ... (e.g., groups, **data objects**, and text annotations). So are **data objects omitted, as the data perspective is not assessed** within the chosen metrics and therefore **outside the scope of our framework**."
3. ⭐ **F-A**：class diagram 的 reward 确实覆盖 attributes（0–5 分），⛔ 但那是**静态结构**里的属性声明，⛔ 不是变量赋值 / 增量语义

⭐⭐ **裁定（S）**：我们的变量维空缺 **不能**归因为「词表漏了一类」——⭐ 邻域三份分类学一份都没有变量语义这一维。⛔ 所以这是**开放机会**，⛔ 不是**可抄的欠账**。⚠️ 但它同时意味着**没有外部依据可挂**，⭐ 与 provenance 表里 `variable_delta_after` 的「界内语料侧为 0，全部来自文献」是**同一件事的两面**。

### ⛔ 结论 2 · 时序性质空缺，**⛔ 同样没有先例**

⭐ 三份分类学**没有任何一项是时序逻辑性质**（no invariant / no bounded response / no until）。⭐ 最接近的是 T-B semantic 的 **causal-footprint overlap** 与 **dependency-graph overlap**（M · Table 4），⛔ 但那是**行为相似度**，⛔ 不是**行为性质**——⭐ 它问「两个模型的因果足迹重合多少」，⛔ 不问「这个模型是否始终满足 $\varphi$」。

⭐⭐ **裁定（S）**：`invariant` / `response_within` 为空，**⛔ 分类学层面也没有对手能对照**。⚠️ ⭐ 结合 provenance 表已记的 `response_within` 系统性缺口（"文献里的 Response 模式几乎一律是**无界** eventually"），⭐ **这一族的外部支撑本来就最薄**，⛔ 台账为空与它是一致的，⛔ 不是两个独立问题。

### ⛔ 结论 3 · **我们完全没有 pragmatic 维（15/15 不覆盖）**

⭐⭐ **这是反方向的空缺，⛔ 而且是三份分类学里指标数最多的单一维度。** ⭐ T-B 的 15 项 pragmatic 全部落在「人读不读得懂」上：size / density / connector interplay / partitionability / concurrency。⛔ 我们 19 条**一条都不碰**。

⚠️ **这未必是缺陷（I）**：看起来 pragmatic 与我们的任务定义正交 —— ⭐ 我们做的是**「模型 vs NL 需求」的缺陷检测**，⛔ 而 pragmatic 说的是「这个模型好不好读」，⛔ 一个又丑又对的模型在我们口径下没有缺陷。⭐ 但 T-B 自己警告过这条正交性不彻底（M · §4.2 逐字："pragmatic quality **should therefore be interpreted in conjunction with the other BEF4LLM dimensions—especially semantic quality**—rather than in isolation"）。⚠️ ⭐ 若 G1 要给 `depth` 定档，**「过于庞杂以致不可判读」这一档要不要设**，是个待裁项。

### ⛔ 结论 4 · **`nl_evidence` 字段没有任何先例可抄**

⭐⭐ **三份分类学没有一份把判据锚在 NL 文本上。**

| 分类学 | ⭐ 判据锚在哪 |
| :-- | :-- |
| T-A 类 1–2 | ⭐ 元模型 + 显式约束集（⛔ 与 NL 无关） |
| T-A 类 3 | ⛔ **定义时说 NL，测的时候换成 ground-truth 模型**（逐字见 §1.1） |
| T-B validity / syntactic / pragmatic | ⭐ XSD schema · BPMN 规则 · 经验阈值（⛔ 全与 NL 无关） |
| T-B semantic | ⛔ **ground-truth 模型**（M · §4.3 逐字："Directly verifying these properties against the real world is impractical") |
| F-A 全部 8 类 | ⛔ **参考 XMI / 参考 CFG** |

⭐⭐ **裁定（S）**：⛔ **整个邻域都在拿「参考模型」当真值，⛔ 没有人拿「NL 原文的哪一句」当真值。** ⭐ 这既说明我们的 `nl_evidence` 字段是**真正的新东西**（⭐ 论文里可以这么讲），⛔ 也说明**没有现成的字段口径可抄**，⭐ G1 得自己定。⚠️ ⭐ 另外这条同时解释了为什么 §1.1 那句 "automated comparison of a graph model with the natural language description **may be unreliable**" 会被 T-A 写进 Metrics 一节——⛔ 那正是我们要硬做的事，⭐ 而领域里一篇 MODELS 论文明写它不可靠。⭐⭐ **这句要么被我们引来当动机，要么会被审稿人引来打我们，⛔ 二选一，最好我们先引。**

### ⭐ 结论 5 · 覆盖得到的部分（⛔ 别在论文里当创新写）

⭐ **T-A 类 2 我们接住 4/5，T-B syntactic 我们接住约 14/16。** ⛔ 这意味着**结构族 10 条基本是领域共识**，⛔ 不是新东西 —— ⭐ 与 provenance 表把 6 条判为「② 元模型定义性」是一致的。⚠️ ⭐ 唯一确实没有对应的两项（T-A 的 no-self-cycles、T-B #9 split/join 匹配）⛔ 一个属并发界外、⭐ 一个是可考虑补的（自环）。

---

# ⭐⭐ 问题二 · 反馈信号该取自哪里

## 2.1 · F-A（MODELS 2026 NIER）· formalism-aware rewards

⭐ **核心句逐字（M · Abstract）**："We investigate **formalism-aware rewards: feedback signals derived from analysable model representations rather than surface text**."

### ⭐⭐ 问 1 · 「可分析的模型表示」具体是什么？怎么得到？得不到时怎么办？

| 制品 | ⭐ 可分析表示 | ⭐ 怎么得到 |
| :-- | :-- | :-- |
| Class diagram | ⭐ **XMI** | ⭐ 逐字（M · §3 Class-diagram reward）："generated PlantUML is **compiled to XMI through the PlantUML server**" |
| Activity diagram | ⭐ **control-flow graph（CFG）** | ⭐ 逐字（M · §3 Infrastructure）："**a custom ANTLR4 grammar and CFG builder, which we developed for PlantUML activity diagrams**, produce the activity-diagram CFG" |

⭐ **为什么 activity 不能也用 XMI（M · §3 Reward instantiation 逐字）**：

> "Activity diagrams have **no comparable export**, and **textual comparison misleads because one control flow admits many syntactic forms**."

⭐⭐ **得不到时怎么办 —— ⛔ 直接判 0，⭐ 且是刻意设计的（M，两处）**：

> §3 Class-diagram reward: "if compilation fails or yields **no parseable XMI**, **all content rewards are zero**"
>
> §3 Infrastructure: "a **patched PlantUML processing loop turns malformed generations into deterministic zero rewards rather than crashes**"

⭐⭐ **这一句对我们是纪律层的直接印证**：⭐ 它与本仓库 CLAUDE.md §10「除此之外一律降级，不许抛」是**同一条工程判断**——⛔ 解析失败**不许把整格搞崩**，⭐ 而是**变成一个确定性的 0 分并继续往下走**。⭐ F-A 为此专门 patch 了 PlantUML 的处理循环。

⭐ **另一条基础设施细节（M · §3 Infrastructure）**："a **persistent conversion server** keeps repeated PlantUML-to-XMI conversion **off the training critical path**" —— ⚠️ ⭐ 即「求解器在环」的**代价是真的**，⭐ 他们靠常驻服务摊掉。

### ⭐⭐ 问 2 · 奖励怎么算？标量还是结构化差异报告？⭐ 回灌给模型的是什么形态？

⭐⭐ **答案分两层，⛔ 而这两层的区别是本卡最关键的一处：**

**① 计算层：结构化的、逐分量的差异比对。**

⭐ **逐字（M · §3 Reward instantiation）**：

> "Each diagram type's reward **sums to 20**. A **shared format reward (0–1)** applies to both. The class-diagram reward adds a **compilation reward (0–1)** and structural rewards over **classes (0–3), relationships (0–5), methods (0–5), and attributes (0–5)**; the activity-diagram reward adds a **compilation reward (0–1)**, a **control-flow-graph structural reward (0–9)**, and a **label reward (0–9)**."

⭐ 各分量的比对方式（M · §3）：

- **classes**：按 name + type 比
- **attributes / methods**：⭐ **逐类贪心匹配**，"greedily matching generated members to target members on **case-insensitive name**, with **partial credit** for matching signatures and modifiers"
- **relationships**：⭐ **六种关系类型**（"association, aggregation, composition, generalisation, realisation, dependency"），⭐ "matching a generated relationship to a target **only when both its kind and its connected classes agree**, with partial credit for multiplicities and role names"
- **CFG structural**：⭐ 两个子分数取平均 —— "a **weighted Jaccard similarity over node-kind multisets**, penalising missing or spurious constructs, and an **assignment-based topology score inspired by graph edit distance**"，⭐ 后者用 **Hungarian algorithm** 做最小代价二分匹配，⭐ 代价函数区分同类/异类匹配、含 **swimlane-aware penalty**、并比较匹配节点的出边种类
- **label**：⭐ **TF-IDF cosine**，⛔ 不是精确串匹配（"so that distinctive domain terms count more than common function words"）

**② 回灌层：⛔⛔ 压成一个标量，⛔ 而且根本不回到模型的上下文里。**

⭐⭐ **逐字（M · §3 Two-stage adaptation）**：

> "For each input, the model generates a **group of candidate PlantUML outputs**. Each candidate is converted into an analysable representation and scored by the formalism-aware rewards, **giving every candidate a scalar reward**. **GRPO** then compares the candidates within the group: those **scoring above the group average are reinforced** and those below it are discouraged, so the model **gradually shifts probability** toward generations whose underlying model structure matches the reference."

⛔⛔ **所以：回灌形态是「⭐ 标量奖励 → ⛔ 梯度」，⛔ 不是「定位」、⛔ 不是「反例」、⛔ 也不是把差异报告塞回 prompt。** ⭐ 模型在**推理时看不到任何反馈**；⭐ 它在**训练时通过参数变化**吸收反馈。

⭐⭐ **这一点必须写进我们的对照表，⛔ 否则会误读 F-A**：

| | ⭐ 我们（v46） | ⭐ F-A |
| :-- | :-- | :-- |
| 反馈计算 | ⭐ pyfcstm 求值 + 契约门 → ⭐ **结构化诊断** | ⭐ XMI / CFG 比对 → ⭐ **逐分量分数** |
| ⭐ **反馈回灌形态** | ⛔ **文本**（报错文案进上下文） | ⛔ **标量 → 梯度**（⛔ 不进上下文） |
| ⭐ **循环单位** | ⭐ **同一格内的修订轮** | ⭐ **训练步 × 候选组** |
| 推理时是否有反馈 | ⭐ **有** | ⛔ **无** |

⚠️ ⭐ **F-A 的「reward loop」不是我们意义上的修订循环。** ⭐ 它是 GRPO 的采样-打分-更新循环。⛔ **不要把它当作「别人也在把 oracle 放在裁决端」的证据** —— ⭐ 它把 oracle 放在**奖励端**，⭐ 那是第三个位置。

### ⭐ 问 3 · 与「拿字符串相似度当反馈」相比提升多少？有没有消融？

⭐⭐ **有消融，⛔ 而结论对 F-A 自己不利，⭐ 且他们如实公布了。**

⭐ **消融逐字（M · §4.1 Ablation）**：

> "the full **SFT-plus-GRPO pipeline is statistically indistinguishable from supervised fine-tuning alone** on both class diagrams ($p=0.94$) and activity diagrams ($p=0.64$), using **paired Wilcoxon tests**."

⭐ **注意 SFT 就是「表面文本对齐」那一档**（M · §3 Two-stage adaptation 逐字）："it optimises only for **surface agreement with the reference text**, not for the structure of the resulting model"。⭐ **所以这个消融回答的正是问 3**：⛔ **在 F-A 的 held-out 集上，「结构化奖励」相对「表面文本对齐」的增量 = 统计上测不出来。**

⭐ **逐分量表（Table 2）里 SFT-only 甚至更高**：

| 分量 | Ours（SFT+GRPO） | ⭐ SFT（no RL） |
| :-- | --: | --: |
| Class · Compilation | 100.0 | 100.0 |
| Class · Class-level | 98.3 | 98.3 |
| Class · Relationship | **84.2** | 83.6 |
| Class · Attribute | 98.0 | 98.0 |
| Class · Method | 90.9 | **91.2** |
| Activity · Compilation | 86.7 | ⛔ **100.0** |
| Activity · Structural | 73.4 | ⛔ **86.0** |
| Activity · Label | 69.2 | ⛔ **78.6** |

⭐ 作者对此的处理逐字（M · §4.1）："The higher SFT figures on the activity components **should therefore not be read as a systematic regression**: on this small held-out set the reward-guided stage **demonstrates feasibility but not yet a statistically detectable gain**."

⭐⭐ **`adverse_results` 处置方式可直接借鉴（M · Abstract）**："**The added benefit of the reward-guided stage remains open on the current held-out set.**" —— ⭐ **写进摘要**，⛔ 不藏在 Limitations。⭐ 这与我们要处理 **−15.82pp** 的方式是同一策略。

⭐ **另有一处正向对照（M · §4.1）**：⛔ 整条适配管线（SFT + GRPO 合起来）相对 untuned base 确实有效 —— activity 编译率 **20.0% → 86.7%**，content score **2.81 → 13.71**；class content **11.27 → 17.60**。⛔ **但那是 SFT 的功劳，⛔ 不是 formalism-aware reward 的功劳** —— ⭐ 消融正是把这两者分开的那一步。

### ⭐ 问 4 · 循环几轮？有没有逐轮收益？

⛔⛔ **原文未提供任何逐轮 / 逐步的边际收益数字。**

⭐ 能确认的（M / S）：

- ⭐ **循环单位是 GRPO 的候选组**，⛔ 论文**没给组大小 $K$、没给训练步数、没给早停策略**
- ⚠️ ⭐ 他们把「逐轮/逐分量收益」列为 **future work**（M · §5 Richer reward optimisation 逐字）："**group-relative optimisation that normalises the aggregate can let strong components mask weak ones, weakening the training signal for weaker subscores. Decoupling the normalisation per component**, as in group reward-decoupled policy optimisation (GDPO), may provide a more targeted signal"
- ⭐⭐ **这条 future work 对我们有直接价值（S）**：⭐ 「聚合归一化会让强分量掩盖弱分量」⛔ 与我们「修订机器吃 79% token 而覆盖净变化 ≈ 0」是**同一类病**——⭐ **总分在动，弱项没动。** ⚠️ ⭐ 我们的契约门若只报「过/不过」而不分解到具体义务，会踩同一个坑。

### ⭐ F-A 的其它必记项

| 字段 | 值 |
| :-- | :-- |
| ⭐ 模型 | ⭐ **Qwen3.5-4B**（小开源 VLM）+ 两个专有基线 **Gemini 3 Flash** / **GPT-4.1 Mini**；⛔ 无更多模型对照 |
| 数据 | ⭐ ~500 手写 UML 图（class + activity）配人写 PlantUML；⚠️ **held-out 只有每类 15 张 = 30** |
| ⭐ `judged_by` | ⭐⭐ **两套并行**：① 自动（= reward 函数复用为 metric）② **人工排序研究，26 人**，⭐ 经 UML 知识测筛选，⭐ **Borda count** 聚合，⭐ **Kendall's $W$ 在 0.80–0.91**（⭐ 报了标注者间一致性） |
| ⭐ 自动 vs 人工一致性 | ⭐ **Spearman $\rho = 0.565$, $p < 0.001$, $n = 120$**（class 0.607 / activity 0.636）；⭐ 作者自评逐字："The association is significant but **only moderate**" |
| ⚠️ 基线公平性 | ⭐ 他们**主动说明对自己不利**（M · §4 逐字）："This gives the proprietary baselines a **more explicit instruction prompt**, making the comparison **conservative with respect to the fine-tuned model**" |
| ⭐ 确定性成分 | ⭐ PlantUML 编译器 / XMI 导出 · ⭐ **自研 ANTLR4 grammar + CFG builder** · ⭐ Hungarian algorithm · TF-IDF · 常驻转换服务 |

## 2.2 · ⭐ 顺带：T-C 是「另一条把结构化度量当奖励」的路线

⭐ **T-C 与 F-A 是同一范式的两个实例**（⛔ 两篇互不引用，S）：⭐ 都是 **SFT → 群体相对策略优化**，⭐ 奖励都来自**确定性结构度量**，⛔ 回灌都是**标量 → 梯度**。⭐ 差别在 T-C 把 38 项指标**显式压成三个维度分再加权求和**：

⭐ 逐字（M · T-C §3.4）：权重向量 $\mathbf{w} = (w_{\text{syn}}, w_{\text{pra}}, w_{\text{sem}})$ 满足 $\sum w_i = 1$，⭐ 罚项 $p \in \{-1, 0\}$，⭐ 有效输出奖励落在 $[0,1]$、含罚项全域 $[-1,1]$。

⭐⭐ **T-C 的三条结论对我们全都可用（M · Abstract + §5）**：

1. ⭐ **RL 提升 pragmatic / syntactic，semantic 基本不动。** Llama：syn $0.824 \to 0.926$（$\Delta = +0.092$）· prag $0.794 \to 0.934$（$\Delta = +0.139$）· sem $0.561 \to 0.594$（$\Delta = +0.030$, $p_{adj} = 0.018$）。Qwen：prag $\Delta = +0.116$ · syn $\Delta = +0.032$ · ⛔ **sem $\Delta = -0.018$ 且不显著（$p_{adj} = 0.35$）**。⭐ 作者自陈逐字："**semantic quality is the dimension least amenable to reward-based optimization**"
2. ⭐⭐ **等权重打败定向加权**（逐字）："emphasizing a specific dimension **fails to improve it and can collapse the model into a low-quality mode**" —— ⭐ 举例：$R_2$（无罚项）拿到 pragmatic **0.964** 但 semantic **掉到 0.547**
3. ⭐ **最稳定的效果是方差收缩**：pragmatic 标准差 $0.085 \to 0.013$，⭐ 约 **6.5 倍**

⚠️ **一处必须记的口径缺陷（M · T-C §5.1.1 逐字）**：

> "Because the **SFT-only baseline produces only 36 valid outputs (out of 105)**, while $R_1$ produces 102, the paired statistical comparison is conducted on a **restricted subset of samples**."

⛔⛔ **即：那些 $\Delta$ 是在「两边都有效输出」的子集上算的，⛔ 而两边的有效率是 36 vs 102。** ⭐ 作者自己提醒了（"should therefore be interpreted in conjunction with its substantially lower validity rate"），⛔ 但**分母不同的对照仍然是分母不同的对照**。⭐ 这正是我们 §3.5 「评测口径」那条要防的形态，⭐ 可以当反面教材引。

## 2.3 · ⭐ T-B 里其实藏着一个**确定性裁决者的修订循环**

⭐⭐ **这一条初筛没记，⛔ 但它是本卡里唯一「与我们形态最接近」的循环。**

⭐ **逐字（M · T-B §5）**：

> "If the BPMN XML file returned by the LLM is **invalid**, a **refinement loop** is started. Here, a **refinement prompt** is sent, **stating which errors the BPMN XML file contains** and that it should be fixed. Note that **only one refinement per description is done**."

⭐ **反馈内容逐字（M · T-B §5，另一处）**：

> "To guide the LLM, a **list of the most common mistakes**, along with the **actual mistakes found by the XML validator**, is added to the prompt."

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有** |
| ⭐ **裁决者是谁** | ⭐⭐ **确定性规则 / parser** —— **XSD schema validator**（⛔ 不是 LLM 自评） |
| 终止条件 | ⭐ **最大轮数 = 1** |
| ⭐ 回灌形态 | ⭐⭐ **文本**：⭐ validator 的**实际报错** + ⭐ **一份常见错误清单**（⛔ 后者是静态的，与本次错误无关） |
| ⭐ 逐轮边际收益 | ⛔⛔ **未单独报告。** ⭐ 只能间接看到：⛔ **允许一轮修订之后，17 个 LLM 里仍只有 1 个 validity > 90%**，⛔ 最差的 0.3067 |

⭐⭐ **这个间接数字很有分量（S）**：⭐ **一轮确定性裁决者的修订，仍然救不回大部分格。** ⭐ 与我们「确定性裁决者 0 token 性价比最高」并不矛盾——⭐ 便宜不等于足够。⚠️ ⭐ 但它同时说明：⛔ **T-B 也没有报逐轮收益**，⭐ 所以「第 3–5 轮零收益」这条实测**在邻域里没有可比数字**（⭐ 与 [_ours-v46.md](./_ours-v46.md) §F 的判断一致）。

⚠️ ⭐ 另注意 T-B 那份 "**list of the most common mistakes**" —— ⭐ 它是**与本次错误无关的静态清单**。⛔ 按我们 §3.5 的口径，⛔ **这种东西要查是否构成引导性泄漏**（⛔ 若清单里的条目恰是评测要考的那些规则）。⭐ T-B 是纯评测框架、被测对象就是那些规则，⛔ 所以它自己不构成问题，⛔ 但**这个形态我们不能照搬**。

## 2.4 · F-B（ITG, ICSE-NIER 2024）· ⛔ 全文不可得

⛔⛔ **全文不可得。** ⭐ DOI 本身**已核验为真**（M · Crossref API 返回 200：title `ITG: Trace Generation via Iterative Interaction between LLM Query and Trace Checking`、container `Proceedings of the 2024 ACM/IEEE 44th International Conference on Software Engineering: New Ideas and Emerging Results`、publisher ACM、page `11-15`、date `2024-04-14`）。

⚠️ ⭐ **Crossref 的 container title 写的是「44th」，⛔ 而 ICSE 2024 是第 46 届** —— ⛔ 这是 ACM 那条 proceedings 记录自身的错，⛔ 不是我方笔误。⭐ 引用时以 **ICSE-NIER 2024, pp. 11–15** 为准。

### ⛔ 试过的入口

| 入口 | 结果 |
| :-- | :-- |
| `https://dl.acm.org/doi/10.1145/3639476.3639779` | ⛔ **HTTP 403** |
| `https://dl.acm.org/doi/pdf/10.1145/3639476.3639779`（curl + 浏览器 UA） | ⛔ **HTTP 403**（⛔ 返回的 5707 字节是反爬页，⛔ 不是 PDF） |
| `https://ieeexplore.ieee.org/document/10726939/` | ⛔ **HTTP 202，0 字节** |
| `https://openreview.net/forum?id=qgGGcFsqjE` | ⛔ **bot 验证 interstitial**，⛔ 无任何论文内容 |
| `https://api.openreview.net/notes?forum=...` / `api2.openreview.net` | ⛔ **HTTP 403** |
| Unpaywall `api.unpaywall.org/v2/10.1145/...` | ⛔ **`is_oa = None`，无 OA location** |
| Semantic Scholar Graph API | ⚠️ ⭐ **只拿到 abstract**；⛔ `openAccessPdf` 指回同一个 403 的 ACM 链接（⭐ 标 `GOLD`，⛔ 实际取不到） |
| arXiv / ar5iv | ⛔ **该论文无 arXiv 版本** |

### ⭐ 仅据 abstract 能回答的

⭐ **abstract 逐字（M · via Semantic Scholar Graph API，⭐ 与 ACM 落地页摘要一致）**：

> "we propose an **iterative interaction framework** for applying LLMs, exemplified by **ChatGPT**, to generate a trace satisfying a given LTL formula. The key insight behind it is to **transfer the powerful reasoning capabilities of LLM to LTL trace generation via iterative interaction between LLM reasoning and logical reasoning**. Preliminary results show that compared with the state-of-the-art approach, **the accuracy is relatively improved by 9.7%-23.4%**."

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有**（⭐ "iterative interaction"，M） |
| ⭐ **裁决者是谁** | ⭐⭐ **sound oracle · trace checking**（⭐ 标题即 "**Trace Checking**"；⭐ LTL trace checking 是判定过程，M/S） |
| ⭐ 两个环节 | ⭐ **LLM query** + **trace checking**，⭐ 循环调用直到生成满足公式的 trace（S · 从标题与 abstract 的 "iterative interaction between LLM reasoning and logical reasoning" 推出） |
| 最大轮数 | ⛔ **原文未提供**（⛔ abstract 不含） |
| 逐轮边际收益 | ⛔ **原文未提供**（⛔ abstract 不含） |
| ⭐ 提升幅度 | ⭐ 相对 SOTA **9.7%–23.4%**（M）；⛔ **但那是对比另一套方法，⛔ 不是循环的边际收益** |

### ⛔⛔ 你问的那一问：checker 的输出怎么回到 LLM 的？⭐ 原始反例还是被翻译过？

⛔⛔ **我无法凭已核材料回答这一问。**

⚠️ ⭐ **必须说清楚一件事**：⭐ 本轮检索过程中，网页搜索的**摘要器**给出了看起来很具体的说法（⭐ 大意是「用 satisfiability proof 构造 prompt」、「repair prompt 做 error feedback」、「few-shot 约束输出格式」、「query history 计入 token 上限因而限制了最大迭代数」）。⛔⛔ **我没有拿到任何一份可核的原文来证实这些句子**——⛔ 它们既可能来自 PDF、也可能是摘要器的转述或推测。⛔ **按本卡纪律，它们既不能标 M，也不能标 S。**

⭐⭐ **所以这一问的答案是：⛔ 待核。** ⭐ 唯一能说的是（⭐ 基于标题与 abstract，**S**）：⛔ **反馈不可能只是「过/不过」一个比特** —— ⭐ 因为 abstract 明写要把 LLM 推理与**逻辑推理**交互起来，⭐ 而单个比特谈不上「逻辑推理的交互」。⛔ **但「是原始反例还是被翻译过」这一具体形态，⛔ 拿不到全文就不能定。**

⭐ ⚠️ **后续取全文的建议入口**（⛔ 本轮都没走通或未尝试）：⭐ 机构 ACM DL 订阅（⭐ 最可能成功）· ⭐ 联系通信作者 Hai Wan（SYSU）· ⭐ 同组 ISSTA 2024 姊妹论文 *Learning to Check LTL Satisfiability and to Generate Traces via Differentiable Trace Checking*（[DOI 10.1145/3650212.3680337](https://doi.org/10.1145/3650212.3680337)，⭐ 据 Unpaywall 页面存在，⚠️ **本轮未取**）。

---

# D. ⭐ 资产（⛔ 全部实际去取过）

| 工作 | 资源 | 状态 | URL | ⭐ 核验证据 |
| :-- | :-- | :-: | :-- | :-- |
| **T-A** | 全文 | ⭐ 🟢 | [arxiv.org/html/2508.00255v1](https://arxiv.org/html/2508.00255v1) | ⭐ 244,302 字节，CC BY 4.0 |
| **T-A** | ⭐ 代码 + prompt + 逐次结果 | ⭐ 🟢 | [github.com/20001LastOrder/LLM-AbsCon](https://github.com/20001LastOrder/LLM-AbsCon) | ⭐ `verify_assets` 逐字：**HEAD `908e49f2ae` · 文件 1461（非文档 1456 · 源码 44） · release 0 · license 无**。⭐ 人工复核树：⭐ **`activity/prompts.py`（prompt 公开）· `activity/data/paged.json`（数据）· `activity/results/<model>/paged/results_1..N.csv`（⭐ 逐次运行结果，⛔ 不只是论文表格）** |
| **T-A** | ⛔ license | ⚪ | — | ⛔ **无 license 文件** |
| **T-B** | 全文 | ⭐ 🟢 | [arxiv.org/html/2601.21787v2](https://arxiv.org/html/2601.21787v2) | ⭐ 1,157,992 字节 |
| **T-B** | ⭐ 框架实现 + 数据 | ⭐ 🟢 | [gitlab-iwi.dfki.de/lauer/bef4llm](https://gitlab-iwi.dfki.de/lauer/bef4llm) | ⭐ GitLab API 逐字：**HEAD `ac29bf0743` · `2026-05-28T08:50:53+00:00` · title `Edit reward_fuctions`**；⭐ 树顶层：**`src/` `test/` `data_human_comparison/` `requirements.txt` `setup.py` `README.md`**；⭐ 18 commits · 1 branch · 0 tags。⛔ **不是空壳** |
| **T-C** | 全文 | ⭐ 🟢 | [arxiv.org/html/2607.06175v1](https://arxiv.org/html/2607.06175v1) | ⭐ 449,090 字节，CC BY 4.0 |
| **T-C** | 代码 | ⚠️ 🟠 | [github.com/chlauer99/RL_for_process_modeling](https://github.com/chlauer99/RL_for_process_modeling) | ⭐ `verify_assets` 逐字：**HEAD `be1d2b7369` · 文件 11（非文档 9 · 源码 7） · release 0 · license 无**。⛔⛔ **判 🟠 而非 🟢**：⭐ 机械判据说「不是空壳」，⛔ 但 **11 个文件 / 7 个源码文件**撑不起「48 个配置 × 2 个模型家族的 GSPO 训练 + 38 项指标评测」——⚠️ ⭐ 按 schema §D 的口径，**「取到的够不够复现」是人裁**，⛔ 我判**不够** |
| **F-A** | 全文 | ⭐ 🟢 | [arxiv.org/html/2607.28987v1](https://arxiv.org/html/2607.28987v1) | ⭐ 132,809 字节；⭐ accepted author manuscript |
| **F-A** | ⭐ 代码 + prompt + **reward 定义** | ⛔ 🟠 | `anonymous.4open.science/r/uml-to-plantuml-F938` | ⛔⛔ **入口已死**：⭐ 页面 **HTTP 401**；⭐ API 返回 **HTTP 410 + `{"error":"repository_expired"}`**。⚠️ ⭐ 而论文正文明写"**The artifact provides exact weights, edit costs, and class-diagram sub-scores**"——⛔ **那些权重与编辑代价现在拿不到** |
| **F-A** | 数据集（~500 手写图） | ⛔ 🟠 | — | ⛔ 引文逐字："**Dataset paper accepted but not yet publicly available.** Note: Full citation withheld for double-anonymous review" |
| **F-B** | 全文 | ⛔ ⚪→🔒 | [DOI 10.1145/3639476.3639779](https://doi.org/10.1145/3639476.3639779) | ⛔ **8 个入口全败**（逐条见 §2.4）。⭐ DOI 本身经 Crossref 核实存在 |
| **F-B** | 代码 / 数据 / prompt | ⛔ 未知 | — | ⛔ **无法判定** —— ⛔ 全文不可得，⛔ abstract 不提资产 |

---

# E. ⭐ 对 M1 的意义

## 1 · ⭐ 可取之处

1. ⭐⭐ **T-B 的「validity 从 syntactic 里拆出来当 gatekeeper」这个分层，直接可搬到 G1 的 `depth` 字段。** ⭐ 它给的理由是硬的（逐字："validity and syntactic quality **operate at different layers**"，⭐ 一个是文件 schema、一个是建模规则），⛔ 而且它是**可执行的**：⭐ 不过 gate 的样本**不算质量分只算 validity 分**，⛔ 不静默丢格。
2. ⭐⭐ **F-A 的「解析失败 → 确定性 0 分，⛔ 不崩」是我们 §10 纪律的外部印证。** ⭐ 逐字："turns malformed generations into **deterministic zero rewards rather than crashes**"。⭐ 论文里可以引它来支撑「降级而非抛出」这条工程选择。
3. ⭐⭐ **F-A §4.3 的 `meaning-preserving deviation` vs `meaning-altering error` 二分，是 G1 最该抄的一条。** ⭐ 我们判「多报」时同样面对这个问题：⛔ 模型给的断言与台账写法不同、但说的是同一件事，⛔ 算不算多报？⭐ F-A 给了名字、给了反例（if-branch vs switch-branch）、⭐ 并量化了它造成的代价（⭐ 自动分与人工排序只有 $\rho = 0.565$ 的中等相关）。
4. ⭐ **T-C 的「等权重打败定向加权」可以省我们一次实验。** ⭐ 若日后要给 19 条谓词或多道门加权，⛔ **先别做定向加权** —— ⭐ 它的实测是定向加权「fails to improve it and can **collapse the model into a low-quality mode**」。
5. ⭐⭐ **`adverse_results` 的写法：F-A 把「消融测不出增益」写进了 Abstract。** ⭐ 逐字："The added benefit of the reward-guided stage **remains open** on the current held-out set." ⭐ 这是处理我们 **−15.82pp** 的一个现成模板——⛔ 不藏、⭐ 不硬拗、⭐ 说清「未建立」而不是「不成立」。
6. ⭐ **F-A 的人工判定装置可以照抄形制**：⭐ 26 人 · ⭐ 知识测筛选 · ⭐ 分块设计（3 块 × 10 图，每块 5 class + 5 activity）· ⭐ Borda count 聚合 · ⭐ **报 Kendall's $W$**（0.80–0.91）· ⭐ 自动分与人工排序做 Spearman。⭐ 我们目前 `judged_by` 是人工逐位判定但**没有标注者间一致性**（[_ours-v46.md](./_ours-v46.md) §C）——⭐ 这是可补的一格。

## 2 · ⛔ 不可取 / 陷阱

1. ⛔⛔ **⛔ 不要把 F-A 当作「别人把 sound oracle 放在裁决端」的先例。** ⭐ 它放在**奖励端**：⭐ 反馈压成标量、⛔ 走梯度、⛔ **不进模型上下文、⛔ 推理时模型看不到任何反馈**。⭐ 我们的 v46 是**上下文内的文本反馈**。⛔ 这是两种不同的机制，⛔ 混谈会让 [pipeline_forms.md](../pipeline_forms.md) 的对照表失真。⚠️ ⭐ 邻域里**唯一与我们同形态**的（确定性裁决者 + 文本回灌 + 上下文内修订）是 **T-B §5 那个一轮 refinement loop**，⛔ 而它只允许 1 轮、⛔ 且不报逐轮收益。
2. ⛔⛔ **T-C 的分母陷阱不能踩**：⭐ SFT-only **36/105** 有效 vs $R_1$ **102/105** 有效，⛔ 而 $\Delta$ 是在**两边都有效的子集**上算的。⭐ 作者提醒了，⛔ 但那仍是分母不同的对照。⭐ 我们报主臂 vs X1 时**必须双分母同时给**。
3. ⛔ **T-A 第 3 类的定义-测量错位不能学**：⭐ 定义写「相对 NL 描述不准确」，⛔ 测的时候换成「相对 ground-truth 模型不像」。⭐ 我们的 `nl_evidence` 字段**存在的意义正是不做这个替换**，⛔ 所以更不能在实现里偷偷退回参考模型比对。
4. ⛔ **⛔ 不要把 T-B 的 "list of the most common mistakes" 那个形态搬进我们的修订反馈。** ⭐ 那是一份**与本次错误无关的静态清单**；⛔ 在我们的场景里，⛔ 静态清单若与被考的规则重合，⛔ 就是 §3.5 意义上的引导性泄漏。⭐ 我们的反馈必须**只含本次实际触发的诊断**。
5. ⛔ **F-A 的 future work 提前警告了我们一个坑（S）**：⭐ 「聚合归一化会让强分量掩盖弱分量，削弱弱分量的训练信号」。⭐ 映射到我们：⛔ **若契约门只报「过/不过」而不分解到具体未满足义务，修订轮就学不到弱项** —— ⚠️ ⭐ 这与我们实测的「79% token、覆盖净变化 ≈ 0」高度同形，⭐ 是一条值得单独查的机制假说。

## 3 · ⚠️ 与我们的关键差别

1. ⚠️ ⭐ **制品不是状态机。** ⭐ T-A 是 labeled graph / Mermaid，T-B/T-C 是 BPMN 2.0 XML，F-A 是 PlantUML class/activity diagram。⛔ **没有一份做 FSM / HSM / EFSM**。⭐ 所以它们的分类项**不能逐条平移**，⛔ 只能取轴（层次 / 方向 / 深度）。
2. ⚠️⚠️ ⭐ **三份分类学都以「有参考模型」为前提，⛔ 我们没有。** ⭐ T-B semantic 7 项全要 $M_g$；F-A 全部 reward 都要参考 XMI / 参考 CFG；T-A 第 3 类实测要 ground truth。⭐ 我们只有 **NL + 模型**。⛔ **这既是我们的新意，⛔ 也是我们没有现成判据可抄的根本原因。**
3. ⚠️ ⭐ **任务方向相反**：⭐ 它们全是**生成质量评估 / 生成改进**，⭐ 我们是**缺陷检测**。⭐ 一个「分数低」的模型在它们的口径下是差模型；⛔ 在我们口径下，「哪一条 NL 需求被违反了、证据在哪」才是产出。⛔ **分数不是发现。**
4. ⚠️ ⭐ **界内边界差异**：⭐ T-B syntactic #9（split gateway 有匹配 join）与整个 concurrency 组、⭐ T-A 的 fork/parallel flow —— ⛔ **全部落在我们的并发界外**。⭐ 对照表算覆盖率时**必须先扣掉这些**，⛔ 否则会把「不在断言对象内」误记成「方法未能检出」（⛔ CLAUDE.md 明令禁止）。

---

# F. ⛔ 存疑与未核项

1. ⛔⛔ ⚠️ **F-B（ITG）checker 输出的回灌形态（原始反例 vs 被翻译）—— 未确认。** ⭐ 已试过 8 个入口（ACM landing 403 · ACM PDF 403 · IEEE 202/0 字节 · OpenReview 网页 bot 墙 · OpenReview API 403 × 2 · Unpaywall 无 OA · S2 只给 abstract · arXiv 无此文）。⛔ 网页搜索摘要器给出的具体说法**无原文可核，故不入账**。
2. ⚠️ **F-B 的最大轮数与逐轮收益 —— 原文未提供**（⛔ abstract 不含；⛔ 全文不可得）。
3. ⚠️ **F-A 的 reward 精确权重与 edit cost —— 拿不到。** ⭐ 论文说在 artifact 里，⛔ 而 `anonymous.4open.science/r/uml-to-plantuml-F938` 返回 **410 `repository_expired`**。⭐ 后续入口：⭐ 等 camera-ready 换成正式仓库，⭐ 或联系作者 Mersedeh Sadeghi（U Cologne）。
4. ⚠️ **F-A 的 GRPO 组大小 $K$、训练步数、早停 —— 原文未提供。** ⛔ 因此「循环几轮」这一问对 F-A 也答不上。
5. ⚠️ **F-A 数据集不可得**：⛔ 引文逐字「Dataset paper accepted but not yet publicly available」，⛔ 且因双盲隐去了完整引用。
6. ⚠️ **T-C 代码是否足以复现 —— 我判 🟠，⛔ 但这是人裁不是机械判。** ⭐ 11 文件 / 7 源码 撑 48 配置 × 2 模型家族看起来不够，⛔ 但我没有逐文件读过内容。⭐ 复核方式：clone 后看有没有训练入口与 38 项指标实现（⛔ 或它是否 import 了 T-B 的 `bef4llm` 包 —— ⭐ 若是，则实际可复现性要连着 T-B 仓库一起判）。
7. ⚠️ **Elsevier *Information Systems* 的 CCF 等级未核。** ⛔ 本仓库 [ccf_venues/](../../../../../ccf_venues/) 无该 venue 条目（⭐ `journal-b-ist` 是另一刊）。⛔ 我没有查 CCF 目录原件，⛔ 故留空而非填一个值。
8. ⚠️ **T-C 的 venue 未定**：⭐ arXiv abs 页不列任何 venue，⛔ 只有 "21 pages, 5 figures"。⛔ 引用时只能按预印本引，⛔ 不得写成会议/期刊论文。
9. ⚠️ **「我们只用到 15/19」中那 4 条的口径需与 G1 对齐。** ⭐ 本卡按 [../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/README.md](../../../discover_matrix/ledger_v2/provenance/relabel/README.md) 取「**从未作为 primary**」：`variable_declared` / `variable_delta_after` / `response_within` / `invariant`。⚠️ ⭐ 而 [predicate_provenance.md](../../provenance/predicate_provenance.md) 的「台账断言」列里**只有 `invariant` 是 0**（⭐ 其余三条有 1–2 条非 primary 断言）。⛔ **「15/19」说的是 primary 口径，⛔ 不是「出现过」口径** —— ⛔ 两个数不能互换引用。
10. ⚠️ **T-A / T-B 都没有按缺陷子类拆的占比。** ⭐ T-A 只给聚合 `Con` 与 F1；⭐ T-B 给到维度级均值（⛔ 逐 metric 的分布在附录 Table 15–18，⛔ 本轮未逐表核）。⛔ **所以「哪一类缺陷最常见」这个问题，⛔ 邻域没有可直接引的答案。**
11. ⚠️ **T-B 的 pragmatic 分组数在两篇里不一致**：⭐ T-B 写「六类删 cyclicity 剩五类」，⭐ T-C §3.3 直接写「five categories」。⛔ 不矛盾，⛔ 但引用时要注意别写成「T-B 有六类 pragmatic 指标」。

---

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 | ⭐ 建立。⭐ 覆盖 T-A / T-B / T-C / F-A 四份全文（⭐ 均实取 arXiv HTML）+ F-B（⛔ 全文不可得，8 入口失败）。⭐⭐ **主要更正：初筛记的「三份分类学」实为两份** —— T-C 的 38 项指标就是 T-B 的 BEF4LLM 去掉 validity；⭐ 同时**新登记第三份**（F-A §4.3 的 8 类）。 |
