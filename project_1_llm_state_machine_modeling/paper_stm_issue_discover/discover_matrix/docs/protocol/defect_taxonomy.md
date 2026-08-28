# 状态机缺陷类型学：从外部文献导出的三个可枚举维度

> **2026-08-29 现行口径**：本文中的“界外”只描述这份历史类型学和冻结 benchmark
> 当时没有提供的维度，不是现行缺陷分类出口。新报告不得判 `OUT_OF_SCOPE`：作者源承重
> 事实成立后必须裁 D2/D1/D0，当前谓词/backend 不支持只降低 W；D0 与 A0 都进入 I，
> 只有 D2/D1 能进入 K/N。历史表和数字不重写，以保留复现性。

> 本文件回答一个问题：**给人工判读者一套「选择题」式的缺陷类型，而这套类型必须来自外部文献，不得来自我们自己的谓词词表、`layer` 分层或现有台账条目。**
>
> 准入门槛有两条，缺一不可：**① 该划分在文献里有正式定义（可逐字引用）；② 每个取值配得出一条可操作的判定测试**——判读者指着制品就能判，不需要解释、不需要权衡。达不到第 ② 条的流派，即使很有名，本文件也只在 §2.7 记录并说明为什么不收。

## 1. 为什么类型学必须从外部来

### 1.1 循环论证会直接抵消本轮工作的目的

本轮重标注要回答的是：**现有缺陷台账是不是偏浅，有没有漏掉我们框架表达不了的缺陷。** 如果类型学的取值是从我们自己的 19 条谓词、四层 `layer` 或台账已有 126 条归纳出来的，那么判读者能选出来的类型，按构造就等于框架已经能说的东西——**问题本身被答案定义掉了**。

这不是假想风险。现工作单的 `direction` 字段（[relabel/HOWTO.md](../../ledger_v2/provenance/relabel/HOWTO.md) §D.1）明写取值就是「台账 98 条 `REPORTABLE` 实际用过的 8 类」。这个字段用来复核台账内部一致性没问题，用来发现台账的盲区则不可能——**没被用过的类不在选项里**。

### 1.2 这也是仓库既有纪律的要求

[CLAUDE.md](../../../../../CLAUDE.md) §3.5.-1 要求：每一条进入 prompt / schema / 门的规范性规则，必须能挂上一条可查证的外部依据；引入动机（某次运行暴露了什么）与领域出处（它凭什么成立）必须分开记录，不得互相冒充。缺陷类型学是判读者的判据来源，同样受这一条约束。

[rule_provenance.md](./rule_provenance.md) 更进一步：由于我们已经详细分析过「哪些缺陷没被发现」，此后写下的任何分类都落在动机审计的射程内。处置办法是**换掉主张的类型**——本文件因此只主张「这些划分在文献里存在且有正式定义」，不主张「因此我们的框架有依据」。

### 1.3 历史类型学的建模对象边界

按 [CLAUDE.md](../../../../../CLAUDE.md)「研究内容一的建模对象边界」，本类型学服务的对象是 $M = (S, E, V, Tr, A)$，即 FSM / HSM / EFSM。**时钟变量、状态不变式、正交区并发语义全部在建模对象之外。**

文献里确实存在这三类的缺陷类型（见 §2.6 与 §4.5），本文件把它们**列出并标为界外**。界外不等于不许记：正交区域一族已在 2026-08-13 获得一个**可记录、不计分**的取值 `defect_element = region`（`counts_as_defect = false`），时钟与不变式两族仍无取值、走自由描述。判据与撤销「不得取为维度取值」那句旧规则的理由见 §3.7。

## 2. 文献综述（按流派）

### 2.1 一致性测试的 FSM 故障模型

**Chow 1978（W-method）[1]** 是这一支的源头，也是本文件最重要的一条依据。它对故障类的定义方式本身就满足我们的准入门槛：**用「要把 $A$ 改成与 $A'$ 等价，只需改动哪一个函数」来定义故障类**。原文逐字（PDF 全文已取到并逐段核对）：

> "1) *Operation Errors* — A is said to have operation errors, if A is not equivalent to A' and A can be modified to be equivalent to A' by changing only the output function of A (without adding or deleting states in A)."
>
> "2) *Transfer Errors* — A is said to have transfer errors if A is not equivalent to A' and A can be modified to be equivalent to A' by changing only the next-state function of A (without adding or deleting states in A)."
>
> "3) *Extra States (missing states)* — A is said to have extra (missing) states if in order to make A equivalent to A' the number of states in A must be reduced (increased)."
>
> "We will refer to the above errors collectively as *sequencing errors*."

四点值得注意。第一，Chow 的三类同时切了两刀：**改哪个函数**（输出 / 次态）与**改多少个状态**（增 / 减）——这正是本文件维度 A 与维度 B 的雏形。第二，"without adding or deleting states" 这个限定语把「改」与「增删」显式分开了，判据是**声明数量变不变**。第三，Chow 的故障域以 $m \ge n$ 为界（$n$ 是被测机状态数，$m$ 是正确版本可能的最大状态数），`m-n` 出现在他的测试覆盖层级图里；这说明「多余状态」在该传统里是**有界的**，不是无限的。

第四，⚠️ **Chow 全篇用的词是 "errors"，从不写 "fault" 或 "fault model"**；「extra states / missing states」在他那里是**同一类**（第 3 类）而不是两类。后来通行的 "output fault" 是对 "operation error" 的**静默改名**，Chow 本人从未这样写。引用时不要把后世词汇塞回他嘴里。

**Fujiwara 等 1991（Wp-method）[2]** —— ⚠️ **它不是「沿用 Chow 的三类」，而是只承认两类。** 原文逐字（该 PDF 无文本层，为 CCITTFax 扫描件；下引句为渲染页面后**逐字读图**所得，p. 591）：

> "The discussion of the fault coverage of the test methods is therefore based on the fault model of FSM **"output" and "transfer" faults**."

紧邻的界定同样逐字：output error 指 "the implementation follows the FSM specification except for the output produced for certain state transitions"；transfer errors 指 "errors in the next state reached by a transition"。而**多余状态在这里根本不是故障类，是一条前提**——同段写作 "provided that the number of states of the implementation remains within a certain bound"。

⚠️ **由此得到本节最重要的一条分歧**：文献综述里常见的那句「经典 FSM 故障模型 = output + transfer + extra + missing states」是**把两篇论文合并出来的**，**从任何一篇都引不出来**。Chow 是三类且含状态数一类，Fujiwara 是两类且把状态数降为界。我们若要引「经典四类」，必须同时引两篇并说明这是合并口径。

**EFSM 扩展。** 把变量、守卫、赋值加进来之后，故障类扩展为四类。逐字（El-Fakih、Yevtushenko、Bozga、Bensalem [3]，开放获取，全文已取到并逐字核对）：

> "For instance, common types of EFSM faults (Bochmann & Petrenko 1994; El-Fakih et al. 2003) include **output, transfer, predicate, and assignment faults**."

三条限定必须一并记住。其一，该文用的词是 **predicate** 而非 guard。其二，这是一句**二手归属**——它把出处记给 Bochmann & Petrenko 1994 与 El-Fakih et al. 2003，而这两篇本轮**均未核**。其三，它是一句顺带的话，不是一节定义。

**反向证据同样存在**：Hierons 等的 ACM Computing Surveys 综述 [30] §5.2 只列两类——"detect **output faults**, i.e. transitions producing the wrong output, and **state transfer faults**, i.e. transitions going to incorrect states of the SUT I"，**没有数据层的两类**。也就是说 EFSM 四类并非领域共识。

更麻烦的一点：**"predicate fault" 这个名字之下没有稳定内容**。各家论文各自从布尔规约变异算子里另起一套（Variable Negation Fault / Associative Shift Fault / Operator Reference Fault 之类，源头是 NIST 的布尔故障类而非 FSM 测试）。因此本文件只把它当作**「缺陷落在守卫上」这一构件归属的依据**，不把它当作一个有内部结构的类。

⚠️ 最后一处对我们很关键：**EFSM 文献里没有「缺少一个变量声明」这一故障类**。原因是 EFSM 的上下文变量集合是机器定义的一部分，被假定给定；故障只发生在**引用**它们的守卫（predicate）与赋值（assignment）上。这直接决定了 §3.2 里 `variable` 取值的证据档位（见 §4.3）。

### 2.2 规约级变异算子：一套「按语法编辑操作」定义的缺陷类型学

变异算子集合本身就是一套故障模型——这句话是该领域自己说的，不是我们的推论。

**Fabbri 等** 先做 FSM [4] 再做 Statecharts [5]。Jia & Harman 的变异测试综述 [6]（IEEE TSE 2011，PDF 全文已取到）对前者的描述逐字为：

> "Fabbri et al. [88] applied Specification Mutation to validate specifications presented as FSMs. They proposed **9 mutation operators, representing faults related to the states, events and outputs of an FSM**."

以及对后者：

> "Statecharts can be considered as an extension of FSMs, so the first set of mutation operators for Statecharts was also proposed by Fabbri et al. [87], based on their previous work on FSM mutation operators."

**Fabbri 两篇原文均未取到全文**（IEEE Xplore 受限）。⚠️ 但**逐条算子表已从同组的技术报告取到**：ND-41（Fabbri、Maldonado、Sugeta、Masiero，USP-ICMC *Notas Didáticas* 41，1999 年 12 月，即 ISSRE 论文发表次月，同一四位作者）[36] 的 Tabela 4.1。该 PDF 是扫描件且 OCR 层系统性混淆 `l`/`I`，**下表为我把第 60 页渲染成图后逐行读图所得**，非文本抽取：

| 组 | 算子（逐字，含描述原文） |
| :-- | :-- |
| **FSM（8）** | `TraDefStaAlt` Altera estado *default* · `TraArcDel` Arco faltando · `TraEveDel` Evento faltando · `TraEveIns` Evento extra · `TraEveAlt` Evento trocado · `TraDesStaAlt` Destino trocado · `TraActDel` Ação faltando · `TraActAlt` Ação trocada |
| **EFSM（10）** | `TraExpDel` · `TraNegBoolExp` · `TraAssRelAlt` · `TraAritOperArit` · `TraRelOperRel` · `TraLogOperLog` · `TraNegLogExp` · `TraVarAltVar`（Troca variável por variável）· `TraConsAlt` · `TraConsAltVar` |
| **Statecharts 固有（17）** | `HistDelTra` · `HistTraAltTra` · `HistDelSta` · `HistHH*` · `HistH*H` · `HisInsHSta` · `HisInsH*Sta` · `TraCondInDel` · `TraCondInStaAlt` · `TraCondNYDel` · `TraCondNYEveAlt` · `TraEveExDel` · `TraEveExStaAlt` · `TraEveEnDel` · `TraEveEnStaAlt` · `TraBrOrigAlt` · `TraBrDestAlt` |

合计 **35** 条。这张表对本文件有三重价值。

其一，**FSM 那 8 条本身就是「构件 × 编辑操作」的叉积**，而且是用葡萄牙语独立写出来的：构件是 `Arco`（边）/ `Evento`（事件）/ `Ação`（动作）/ `estado default`（默认态），操作是 `faltando`（缺失）/ `extra`（多余）/ `trocado`（改换）。**这与 Lackner & Schmidt 的 deletion / insertion / property change 三分完全同构，而两者相隔 16 年、语言不同、互不引用**——这是维度 A × 维度 B 结构最有力的一条独立佐证。

其二，⚠️ **全表 35 条里没有任何一条状态级算子**——没有 `StaDel`、没有 `StaIns`。每一条都锚在**迁移**（`Tra*`）或**历史符号**（`Hist*` / `His*`）上。而 1994 年的 FSM 姊妹表据报是有 `StaDel` 的。也就是说，statechart 变异传统**把状态增删算子拿掉了**。这对维度 A 的 `state` 取值是一条需要记住的保留：它的支撑来自 Chow 而非变异算子传统。

其三，`TraVarAltVar`（变量换变量）是全表**唯一**的变量级算子，且是「换」不是「缺」——再次印证 §4.3：变量在这一传统里只作为被引用的操作数出现，从无「缺少变量声明」这一类。

ND-41 同页还给出一条对我们边界很有用的现成配置：三种抽象策略中的 **Estratégia Básica** 逐字为 "abstrai os componentes do tipo OR"，即**只抽取 OR 型构件、不涉正交**。若要采用这套算子而排除并发，可以直接引用作者自己命名的这一配置，不必自造限制。

**Lackner & Schmidt 2015 [7]**（EPTCS 开放获取，PDF 全文已取到）是本文件最直接的结构依据：它把「构件类型 × 编辑操作」这个二维结构**明写出来**，并说明应当取叉积。逐字：

> "From other mutation systems [4, 1, 12], we identified the following general categories for model-based mutation operators:
> 1. **Model element deletion**: a model designer forgets to add a model element, e.g. a feature, a mapping, or a transition
> 2. **Model element insertion**: a model designer inserts a superfluous model element, e.g. a feature, a mapping, or a transition
> 3. **Property change**: a model designer chooses a wrong value for a property of a model element, e.g. mandatory feature instead of optional, inverse value for a feature's status, or wrong transition target.
>
> For each model element-type, like mappings, transitions, guards, etc., one can check for applicable categories and implement mutation operators accordingly."

同一篇给出 UML 状态机侧的构件清单，逐字：

> "We identified five targets for mutation: (i) remove the entire transition, change its (ii) target state, as well as mutating its (iii) triggers, (iv) guard, and (v) effect. The latter three can be mutated according to the three defined categories delete, add and change."

它还显式声明了**一阶（single syntactic change）约束**，以及为什么「元素替换」不单列：

> "Only simple, first-order mutants should be generated. These mutants are produced by making exactly one syntactic change to the original specification."
>
> "we do not consider the exchange of an element by another, since this can easily be mimicked by removing and inserting the removed element at another point in the model."

这两句是 §3.3「一阶编辑约定」的直接来源。

对应的具体算子名（同篇）：`Delete Transition (DTR)` · `Change Transition Target (CTT)` · `Delete Effect (DEF)` · `Delete Trigger (DTI)` · `Insert Trigger (ITG)` · `Delete Guard (DGD)` · `Change Guard (CGD)`。注意 `CTT` 被归为 property change 而非 delete+insert——**这与 Chow 的 transfer error 是同一条**，两个相隔 37 年的传统在这一点上完全一致。

### 2.3 建模语言的良构性规则

**OMG UML 2.5.1（formal/2017-12-05）[8]。** 本仓库已对 Chapter 14 StateMachines 做过一次逐条开采，结果记在 [related_work/provenance/uml251_constraints.md](../../../related_work/provenance/uml251_constraints.md)：Chapter 14 内本地成文的 constraint 共 **47 条**，其中判定「状态层次归属正确性」的为 **0 条**，`Vertex` 元类根本没有 Constraints 小节（经 Eclipse UML2 的 `VertexOperations.java` 零个 `validate*` 交叉验证）。可直接用作判定测试的成文条款例如：

| 元类 | 条款名 | 逐字 |
| :-- | :-- | :-- |
| `Region` | `initial_vertex` | A Region can have at most one initial Vertex. |
| `Pseudostate` | `outgoing_from_initial` | The outgoing Transition from an initial vertex may have a behavior, but not a trigger or a guard. |
| `State` | `destinations_or_sources_of_transitions` | （跨命名空间的声明检查） |
| `Transition` | `transition_vertices` | The source and target Vertices of a Transition must be contained in the same StateMachine as the Transition. |

同一份开采也记录了两条**反向**结论，引用 UML 时必须一并带上：其一，UML **不要求**同一状态同一事件的多条迁移守卫互斥——规范正相反，明写 "It is possible for more than one Transition to be enabled within a StateMachine… such Transitions may be **in conflict**"，且优先级只给出 "a **partial ordering**"；其二，「Region 缺少 initial Pseudostate」被 UML 留作**未定**而非良构性违规，逐字为 "no specific approach is defined… One possible approach is to deem the model ill defined." ——即标准自己承认这只是一种可能选择。**但「语义变异点」这个词有版本悬崖，不要随口用**：它作为**成文的索引子条款类型**只存在到 UML 2.4.1（定义为 "explicitly identifies the areas where the semantics are intentionally under specified"）；在 2.5.1 里该短语几乎消失，实质内容仍在但**不再挂这个标签**。任何「UML 规范明确把 X 标为语义变异点」的说法必须锚到 2.4.1 及更早，否则对当前规范为假。该版本悬崖由协作核验者报出，**我只复核了 2.5.1 侧的实质文本（经本仓库既有开采），未独立复核 2.4.1 的条款类型定义**。

**工具规约层。** itemis CREATE / YAKINDU Statechart Tools 的校验器源码 [9] 给出一批可直接当判定测试用的成文检查，逐字（自 GitHub 源码读取，非二手转述）：`Node is not reachable.`（`vertex.MustBeReachable`）· `This region has no entry node.` / `There are multiple default entry nodes…`（`region.MustNotHaveMultipleDefaultEntries`）· `A final state should not have outgoing transitions.`（`finalstate.NoOutTransitions`）· `A state must have a name.`（`state.name.required`）· `Missing trigger. Transition is never taken.` · `Dead transition. This transition can not be taken due to previous transition with '%s' trigger.` · `A guard must not contain assignments.` · `Source and target of a transition must not be located in orthogonal regions!`（界外）。

MathWorks Stateflow 的 edit-time checks [10] 给出同族的三条：unreachable state、dangling transition（"every transition must have a valid destination"）、unreachable junction。

这一层的共同特征是**判据天然清晰**——它们本来就是要写成程序的。

**风格与完备性规则目录层。** 除了元模型良构性，还有一层成文规则专门管「合法但不该这么写」。这一层本轮**推翻了初稿的判断**：我起初把整个 model smell 传统按「判据是解释性的」排除，但**状态机子集恰恰不是这样**。

Arendt、Mantz 与 Taentzer 2009 的 SPES 交付件 [32] §3.4 "UML State Machine Smells" 给出**恰好 5 条**（PDF 全文已取到；该 PDF 丢失 `fi`/`fl` 连字，下引文按原样保留，"nal" 即 "final"）：

> 1. **State Machine: Initial And Final States** — There is no initial or nal state for the state machine. The top-level region of a state machine should have one initial state and at least one nal state so that the state machine has well-dened start and end points. — [46]
> 2. **State: Unnamed State** — While the UML allows for anonymous states, adding a descriptive name to the state increases the readability and understandability of the diagram. — [1]
> 3. **State: No Incoming** — The state has no incoming transitions. Without incoming transitions, the state can never be reached. — [1]
> 4. **State: No Outgoing** — The state has no outgoing transitions. Without outgoing transitions, the state can never be left. Check if this is merely an oversight or the actually intended behavior. — [1]
> 5. **Choice: Missing Guard** — If there are two or more transitions from a choice state, they all must have guards. A choice state realizes a dynamic conditional branch; the guards are required to evaluate the branch conditions. — [1]

两个源码键我已回该文件的 bibliography 逐条解出：`[1]` = Ambler, *The Elements of UML Style*, Cambridge University Press, 2002 [33]；`[46]` = Rupp, Queins, Zengler, *UML 2 glasklar*, Hanser, 2007 [34]。

商业工具 SDMetrics 的规则手册 [35] 给出同族规则，且额外提供一个**本文件很需要的三分**：每条规则标 `Correctness`（并注明 "This is a **WFR** of the UML"）/ `Completeness` / `Style`。逐字节选：

> C.18 `NoIncoming` · Category: **Completeness** — "State has no incoming transitions. Without incoming transitions, the state can never be reached. Add one or more transitions to the state. Suggested in [Amb03]."
>
> C.17 `InitialAndFinalStates` · Category: **Style** · Severity 2-med — "There is no initial or final state for the state machine. The top-level region of a state machine should have one initial state and at least one final state… Suggested in [JRH04]."
>
> C.17 `TooManyInitialStates` · Category: **Correctness** — "A region can have at most one initial state… This is a **WFR** of the UML."
>
> C.17 `DupName` · Category: **Correctness** — "The region has two or more states of the same name."
>
> C.18 `MissingGuard` · Category: **Correctness** — "If there are two or more transitions from a choice state, they all must have guards."

这个三分直接印证了 §2.3 前半段那条反向结论：**「缺初始 / 终态」被 SDMetrics 自己标为 `Style` 而非 `Correctness`，且不带 WFR 标记**——与 UML 2.5.1 把它留作语义变异点完全一致。而「一个 region 有两个初始态」则标 `Correctness` + WFR。**两者不是一回事，判读时不能混。**

⚠️ **这两份不是互相独立的证人。** 我逐字比对过：Arendt 第 3 条与 SDMetrics `NoIncoming` 的措辞近乎逐字相同，且两者都溯到 Ambler；Arendt 第 1 条溯到 `UML 2 glasklar`，SDMetrics `InitialAndFinalStates` 溯到 `[JRH04]`，仍是同一本书。**引用时必须说明这是同一谱系的两次转述，不得写成「两份独立目录一致」。** 整条状态机异味传统实际上收敛到 Ambler 2002 与 *UML 2 glasklar* 两本书加若干工具厂商。

### 2.4 通用缺陷分类里的「限定词」轴

**ODC（Orthogonal Defect Classification）[11]** 是软件工程里最标准的**多维**缺陷分类，也是本文件「多维而非扁平列表」这一形态的直接先例。它的 `Qualifier` 属性给出三值，官方 v5.2 规约 [12] 逐字：

> "Qualifier (applies to Defect Type): Qualifier captures the element of a nonexistent, wrong or irrelevant implementation."
> - **Missing** — the defect was due to an omission
> - **Incorrect** — the defect was due to a commission
> - **Extraneous** — the defect was due to something not relevant or pertinent to the document or code

出处口径需要限定：**`Missing / Incorrect / Extraneous` 的完整定义出现在 ODC v5.x 规约文档，而不必然出现在 1992 年 TSE 原文** [11] 里；1992 原文的重点是 defect type 分布与 trigger 分布。引用时应引 v5.2 规约，或注明这一点。

**检查阅读（inspection / perspective-based reading）传统**给出一套五类缺陷分类：**Omission · Incorrect Fact · Inconsistency · Ambiguity · Extraneous Information**。

⚠️ **这一支的出处初稿写错了，本轮已更正。** 正确的谱系是：

| 形态 | 出处 | 核实情况 |
| :-- | :-- | :-- |
| **六类**（Missing information · Ambiguous · Inconsistent · Incorrect fact · Extraneous information · **Miscellaneous**），对象是**需求文档** | Shull、Rus 与 Basili, IEEE Computer 2000 [13]（Table 1） | 可自由获取 |
| **五类**（去掉 Miscellaneous、前三项改名），对象是**设计模型** | **Travassos、Shull、Fredericks 与 Basili, OOPSLA 1999 [37]**（Table 1） | 全文已取到，Table 1 逐字核对 |
| 分类的来源 | **ANSI/IEEE Std 830-1984 的质量属性取反** | 二手（Shull 1998 学位论文 §2.1.3 自述），未回原文 |

⛔ **不要把五类记给 Basili & Weiss 1984**——那是二手文献里流传的一条误归属。Porter、Votta 与 Basili 1995 用的是另一套不兼容的 2×4 方案（omission / commission 各分四小类），Basili 等 1996 的 PBR 论文里根本没有这套分类。

本文件从这一支取两件事。第一，**它与 ODC 独立地给出了同一个 missing / incorrect / extraneous 三分**，且六类版自带 `Miscellaneous` 出口——这为 §3.3 的 `other` 出口提供了先例。第二，Travassos 版是**目前找到的唯一一份「以需求文档为参照物、且明确覆盖状态图」的成文缺陷分类**，见 §4.5。

`Ambiguity` 一类对形式化模型基本不适用（模型没有「多义」这回事，只有「不确定」），故不进维度表。

### 2.5 概念模型质量的语义学三层

**Lindland、Sindre 与 Sølvberg 1994（LSS 框架）[14]** 提出概念模型质量的三层：syntactic / semantic / pragmatic。它的价值在于**每层配一个不同的参照物**，因此「判定这条缺陷要拿什么去比」这个问题在这套框架里有正式答案。

**Reijers、Mendling 与 Recker 的 SIQ 框架 [15]** 把它落到过程模型上。可获取的技术报告 [16] 里对三层的说明逐字：

> "**Verification** addresses the need to establish a particular **syntactic** quality of a model in relation to various **formalized properties and rules**. **Validation** relates to the **semantic** quality of the model, i.e. whether a model makes truthful and accurate statements about **the domain it intends to capture**. Finally, **certification** focuses on the **pragmatic** quality of a model, to determine whether a model can actually be **understood by people**."

这条三分在 LLM 时代被原样继承：AbsCon（MODELS 2025）[17] 用 syntax / consistency / quality 三分；BEF4LLM [18] 明写 "building on the SIQ framework"，并在三层之外补了一个 **validity**（XML 是否可解析）作为守门项，理由是 LLM 会产出连 schema 都不合的输出。

对本文件而言，这三层只有**前两层**能进维度表。`pragmatic`（人读不读得懂）拿不出可操作判定测试——BEF4LLM 的 15 项 pragmatic 指标全部依赖**经验阈值**，而它自己就因为「没有多档阈值可用」砍掉了 cyclicity 这一维（逐字："Cyclicity … is not included in the BEF4LLM framework because existing research does not provide multiple thresholds for cyclicity metrics"）。我们没有这些阈值，因此 `pragmatic` 不设取值，落 `other`（详见 §2.7 与 §4.4）。

`validity` 同样不设取值：本语料的制品进入判读时**已经通过 parse gate**，不可解析的产出根本到不了判读者手上。

### 2.6 逻辑层：缺陷不落在任何单个元素上的那一支

⭐ **这一支是本文件第二轮新增的，也是整个座标系的另一半。** 前五节的传统有一个共同的出身局限：变异算子与 Chow 故障模型都来自**测试**领域，那里「缺陷」按定义就是**对规约做的一次语法编辑**。于是它们天生只能描述**能定位到单个元素**的东西。而下面这些缺陷，单看任何一个元素都完全合法。

#### 2.6.1 Heimdahl & Leveson 1996：不确定性与不完备性的形式定义与机械判据

**这是本节最重要的一条**，因为它同时给出了正式定义和**可以用手算的判据**。原文 [38]（IEEE TSE 22(6):363–377；全文 PDF 已取到，下引两段因双栏抽取错乱而由**渲染页面后读图**核对，p. 370 左栏）：

> "The guarding conditions on the transitions triggered by the same event are pairwise compared to see if they are mutually exclusive. **Two transitions with guarding conditions that are not mutually exclusive represent conflicting requirements.** In addition, **if the logical OR of the conditions on all transitions out of the state triggered by the same event does not form a tautology, then there are conditions for which no behavior is specified, i.e., the requirements are incomplete.**"

同页对同一件事的另一种表述：

> "Union composition requires that the domains of the functions describing the transitions involved in the composition are **disjoint**, i.e., no two transitions out of the same state can be satisfied at the same time. In addition, functions require that **the entire domain is covered**. Thus, there must be a satisfiable transition out of every state independent of what input arrives at the model boundary."

论文自己对这两个质量的命名逐字（Abstract / §1）：

> "1) **completeness** with respect to a set of criteria related to robustness (**a response is specified for every possible input and input sequence**) and 2) **consistency** (the specification is free from **conflicting requirements and undesired nondeterminism**)."

⭐ 两条判据可以直接改写成判读者的动作，**不需要模型检查器**：取某个状态在同一事件下的全部出边守卫 $g_1, \dots, g_n$，

- 存在一个变量赋值使某两条同时为真（$g_i \land g_j$ 可满足）→ **非确定性 / 冲突需求**
- 存在一个变量赋值使全部为假（$g_1 \lor \dots \lor g_n$ 不是永真式）→ **不完备（d-incomplete）**

论文用的术语是 **d-complete**（domain-complete），逐字："we use the term d-complete"。

⚠️ 两处限定必须记住。其一，这套定义是**为 RSML 写的**，其可判定性依赖 RSML 把行为强制成数学函数（"by forcing the behavior of an RSML specification to be a mathematical function, we can guarantee the d-completeness, consistency, and determinism"）；搬到别的记法上时，结论形式不变但需要重新论证。其二，论文自陈判据是**保守**的："the analysis is conservative and spurious error reports may be generated."

#### 2.6.2 Dwyer、Avrunin 与 Corbett 1999：性质规约模式——逻辑层的第二个轴

[39] 给出一套 **pattern × scope** 的二维分类，专门用来说「这个系统应当满足什么」。⭐ 对本文件有双重价值：它既能描述**跨制品的性质违反**，又能直接充当「修好之后怎样才算 ok」的表述语言。

**Pattern（8 条）**，取自作者维护的官方模式库 [40]（页面已取到并逐字核对）：

> Occurrence patterns「are used to express requirements related to the existence or lack of existence of certain states/events」——**Absence**（aka Never）· **Universality**（aka Globally, Henceforth）· **Existence**（aka Eventually, Future）· **Bounded Existence**
>
> Order patterns「are used to express requirements related to **pairs** of states/events」——**Precedence** · **Response**（aka Follows, Leads-To），以及两种链式变体 **Response Chains** · **Precedence Chains**

**Scope（5 条）**，逐字：

> "There are five basic kinds of scopes: **global** (the entire program execution), **before** (the execution up to a given state/event), **after** (the execution after a given state/event), **between** (any part of the execution from one given state/event to another given state/event) and **after-until** (like between but the designated part of the execution continues even if the second state/event does not occur)."

另有两条口径逐字，采用时必须一并带上：

> "a scope itself should be interpreted as **optional**; if the scope delimiters are not present in an execution then the specification will be true."
>
> "Before and after scopes for our patterns are interpreted relative to the **first** occurrence of the designated state/event."

⚠️ 本文件**不把 pattern × scope 设为必填维度**（40 个组合，判读负担过重），而是作为 §3.6 的**可选精化**。理由见那一节。

#### 2.6.3 模型检查的标准词汇

「不可达」「终止」「不终止」不是某个元素的属性，而是整张图或全部执行的属性。Baier & Katoen [41]（全书 PDF 已取到，下引均逐字核对）给出两条我们要用的定义：

> **Definition 2.10. Reachable States** —— "A state s is called reachable if there is some execution fragment that ends in s and that starts in some initial state."
>
> **Definition 2.4. Terminal State** —— "State s in transition system TS is called terminal if and only if $\mathrm{Post}(s) = \emptyset$."

⚠️⚠️ **这里有一处极易搞错、且直接影响判据的区分：「terminal state」不等于「deadlock」。** 同书 §3.1 逐字：

> "**A deadlock occurs if the complete system is in a terminal state, although at least one component is in a (local) nonterminal state.** The entire system has thus come to a halt, whereas at least one component has the possibility to continue to operate."

⛔ **也就是说 Baier & Katoen 意义上的 deadlock 是一个并发概念**——它要求存在一个「仍可继续」的分量。**在没有正交区的 $M$ 里这个条件无从成立**，因此本座标系**不使用 `deadlock` 这个名字**，改用 `unintended_terminal`，并直接锚在 Definition 2.4 的 terminal state 上。同书紧接着那句话恰好说明了为什么「是不是缺陷」必须另问：

> "For a transition system modeling a **sequential** computer program, terminal states occur as a natural phenomenon representing the **termination of the program**." 而对并行系统 "such terminal states are usually considered to be **undesired**."

⚠️ **`livelock` / `non-progress cycle` 在 Baier & Katoen 里没有定义。** 我 grep 过全书：`livelock` 只在 p. 3 的历史性引言里出现一次，`non-progress cycle` 一次都没有；该书把邻近概念形式化为 **starvation freedom**。有成文定义的是 SPIN [43]，逐字："A progress label states the requirement that the labeled global state must be visited infinitely often in any infinite system execution. **Any violation of this requirement can be reported by the verifier as a non-progress cycle.**" ⛔ 注意它**相对于用户手工标注的 progress label 定义**，因此没有「与标注无关」的活锁概念。这一条记在 §4.10。

工具侧另有成文条目可引，且已逐字核对：itemis CREATE 的 `vertex.MustBeReachable`「Node is not reachable.」[9]、SDMetrics 的 `NoIncoming` / `NoOutgoing`（Category: **Completeness**）[35]、Stateflow 的 unreachable state 与 dangling transition [10]。⭐ 注意这三处都只覆盖**静态图可达性**，不覆盖「守卫恒假导致的语义不可达」——后者要真跑求解器。

#### 2.6.4 层次语义：两处成文规定与一处跨家分歧

⭐ 这一小节的三条全部由我从 OMG UML 2.5.1 官方 PDF **自行下载并抽取核对**（`pdftotext -layout`，18,069,510 字节）。

**迁移优先级（§14.2.3.9.4 Firing priorities）逐字**：

> "In situations where there are conflicting Transitions, the selection of which Transitions will fire is based in part on an implicit priority. **These priorities resolve some but not all Transition conflicts, as they only define a partial ordering.** … By definition, **a Transition originating from a substate has higher priority than a conflicting Transition originating from any of its containing States.**"

⭐ **这条与经典 statechart 相反**——Harel & Naamad 的 STATEMATE 语义把优先权给**外层**。⚠️ 该逐字引文与其 Appendix C 声明的「未来版本将改为基于源态」这一保留，本轮**由协作核验者取得，我未独立复核**；可开放获取的第三方转述见 Crane & Dingel 的技术报告 [42]（同样未经我复核）。**引用这条分歧时必须带上 Appendix C 的保留**，否则会被熟悉该文的审稿人指为不严谨。

**默认进入会重跑内部初始（§14.2.3.4.5 Entering a State）逐字**：

> "**Default entry**: This situation occurs when the composite State is the direct target of a Transition … After executing the entry Behavior and forking a possible doActivity Behavior execution, **if an initial Pseudostate is defined, State entry continues from that Vertex via its outgoing Transition** (known as the default Transition of the State)."

⭐ 这正是「一条完全合法的迁移，因为指向复合态本身而把内部阶段重置」那类缺陷的规范依据；保留内部配置的**唯一**机制是 history 伪状态。**退出次序（§14.2.3.4.6）逐字**："When exiting from a composite State, **exit commences with the innermost State** in the active state configuration."

**无使能迁移的事件被静默丢弃（§14.2.3.9.1）逐字**：

> "**If no Transition is enabled and the corresponding Event type is not in any of the deferrableTriggers lists of the active state configuration, the dispatched Event occurrence is discarded** and the run-to-completion step is completed trivially."

⭐ 这条对判读很有用：它说明「某状态收到某事件后什么也不发生」在 UML 下是**合法且静默**的，因此这类缺陷只能靠 NL 判，不能靠语言规则判。

### 2.7 语义变异点：部分可判定，部分只能记为空白

**Harel 1987 [19]** 与 **Harel & Naamad 1996（STATEMATE 语义）[20]** 之后，statechart 的「同一张图不同读法」成为一个独立研究对象：**von der Beeck 1994 [21]** 系统比较 statechart 变体；**Crane & Dingel 2005 / 2007 [22]** 比较 UML 2、classical Harel 与 Rhapsody statechart；**Fecher 等 2005 [23]** 直接以「29 处新的不明确之处」为题。UML 2.5.1 自己也把若干点留作语义变异点（§2.3 引的 initial Pseudostate 缺席即其一）。

**这一支不进维度表**，原因是判定测试不成立：「这条缺陷是否存在」在这里取决于**判读者采用哪一套语义**，而不取决于制品。这不是判读者能靠看制品解决的，属于协议层要先裁定的事（本仓库的裁定见 [CLAUDE.md](../../../../../CLAUDE.md) 边界条款与 [fused_event_policy.md](./fused_event_policy.md)）。它在 §4.6 作为已知空白记录。

这一支里凡是关于**正交区并发**、**进入/退出动作在并发下的顺序**、**fork/join 语义**的变异点，一律界外。

### 2.8 调研到但不收进维度表的流派

| 流派 | 代表 | 不收的理由 | 状态 |
| :-- | :-- | :-- | :-: |
| model smells / bad smells in models | 「耦合过高」「结构不良」一族 | 判据是解释性的。判读者面对「这个模型结构不良吗」会卡住，选不下去，且两人选法不会一致 | ⛔ |
| UML 缺陷的实证研究 | Lange & Chaudron [24] | 其主结论是**检出率与误解率**，即缺陷的**影响 / 严重度**轴，不是缺陷**形态**轴。两种轴不得混进同一个维度。另：其缺陷形态表本轮**未取到全文**，不得据标题推测内容 | ⛔ |
| pragmatic quality 指标 | BEF4LLM 15 项 [18] | 判定依赖经验阈值，我们没有这些阈值；且它衡量的是「好不好读」，一个又丑又对的模型在本任务口径下不算缺陷 | ⛔ |
| UML 一致性规则目录 | Torre 等 [25]（119 条） | 判据清晰，但对象是**图与图之间**的一致性；本任务只有单一状态机视图，绝大多数规则不适用 | ⚠️ |
| 语义变异点 | von der Beeck [21] / Crane & Dingel [22] / Fecher [23] | 见 §2.7；剩余部分记为已知空白 | ⛔ |
| UML 设计故障分类 | Dinh-Trong 等 [26] | **全文未取到**（作者页 PDF 链接失效），不得据标题推测其类别；列为待补线索 | |

| 需求不一致的形式分类 | van Lamsweerde 等 [44]：conflict · divergence · competition · obstruction | **形式定义极完整，但判定测试立不住。** 四条互相独立的阻碍：① divergence 的判据是「**存在**一个 boundary condition $B$ 使诸断言矛盾」——判读者想不到那个 $B$ 就会判成「没问题」，这是搜索问题不是训练问题；② conflict 与 divergence 只差「$B = \mathrm{true}$ 够不够」，而这取决于你认为 `Dom` 里有什么，两个判读者会合理地不一致；③ 极小性条件要对**所有子集**验证；④ 全部定义都建立在**已形式化的目标断言**上，而形式化本身正是难的那一步。⭐ **但它的非形式那一层可用**：terminology clash（同概念两名）· designation clash（同名两概念）· structure clash（同概念两结构）——这三条判读者对着 NL 与模型就能判，值得作为命名类缺陷的候选精化 | ⚠️ |
| safety / liveness 二分 | Alpern & Schneider [45] | 形式定义清晰，但**只有两值、且不穷尽**——原文自陈 "Many properties are neither safety nor liveness"，判读者会被迫在混合型需求上误选。本座标系不单设此轴，因为维度 E（Dwyer pattern × scope）在同一位置提供了更细且更可操作的表述；safety / liveness 可由 pattern 反推（`Absence` / `Universality` 偏 safety，`Existence` / `Response` 偏 liveness） | 被 E 取代 |

状态列口径：⛔ 本轮不收 · ⚠️ 部分可用或待补。

## 3. 提出的座标系

### 3.0 结构：为什么需要一个先行的「定位范围」轴

初稿只有 A（构件）× B（限定词）× C（参照物）三个平行维度。**那套结构对逻辑层缺陷是失效的**，原因在出处：A 与 B 都源自变异算子与 Chow 故障模型，而那两支来自测试领域，**「缺陷」在那里按定义就是对规约做的一次语法编辑**。于是 A×B 只能描述「能归到某一个构件声明上」的东西。

一个非确定性缺陷没有「哪个元素错了」这回事——两条出边单看都合法，缺陷在**这一对**上；它也既不 missing、又不 extraneous、又不 incorrect。逼判读者为它选一个 `defect_element` 和一个 `defect_qualifier`，产出的不是数据，是噪声。

**因此本座标系改为条件式结构：先答「定位范围」，它决定后面问哪些轴。**

⭐ 这不是新发明的组织方式。ODC 自己就是这么组织的——它的 `Qualifier` 属性明写 "**applies to** Defect Type" [12]，即某个属性只在另一个属性取到特定值时才有意义。

**为什么不用「给 A 加一个『不定位于单个元素』取值」这个更省事的方案**：那样 B 仍然无处安放（三种编辑操作对全局性质都不成立），而且六类形态完全不同的逻辑层缺陷会被压进同一个桶——那恰恰是「描述能力浅」的病灶本身，不是它的解药。

#### 座标系全貌

| 轴 | 字段名 | 它问什么 | 取值数 | 何时必填 |
| :-- | :-- | :-- | :-: | :-- |
| **0 · 定位范围** | `defect_locus` | 要说清这条缺陷，最少得指出几处 | 4 | **总是** |
| A · 构件 | `defect_element` | 落在哪一类模型构件上 | 7 | `locus=element` 必填；其余可选 |
| B · 限定词 | `defect_qualifier` | 改对它要做哪一种编辑 | 4 | **仅** `locus=element` |
| **D · 逻辑类型** | `defect_logic_kind` | 是哪一种逻辑层缺陷 | 9 | **仅** `locus≠element` |
| C · 参照物 | `defect_reference` | 凭什么说它错 | 3 | **总是** |
| E · 性质模式 | `defect_property_pattern` | 修好之后怎样才算 ok | 8 × 5 | 可选精化 |

**必填轴合计 27 个取值，但任何一条记录只需回答 3 个问题。** 走 `element` 分支时是 locus → A → B → C 共四问，候选面 4+7+4+3 = 18；走逻辑分支时是 locus → D → C 共三问，候选面 4+9+3 = 16。⭐ **判读者面对的从来不是 27 个选项，而是一次 4 选 1 加上两三次 ≤9 选 1**，且每一步都有一句机械判据。这是我认为这个规模判读者能承受的理由。

维度 C 与工作单现有的 `basis` 字段高度重合（后者是「模型自身 / NL 显式义务 / NL 欠指定 / 参考模型」四选一）。若本轮保留 `basis`，维度 C 应当去掉。**两个不要同时上。**

判定测试全部落在**作者源 PlantUML 原文**上（工作单 §1.2 给的那份）。定义来自文献，判定测试是把定义落到判读者实际读的那份语法上——两者的分工在此说明，后文不再重复。

### 3.1 维度 0 · `defect_locus` 定位范围

**判定测试：要把这条缺陷说清楚，你最少得指出制品里的几处？**

| 取值 | 中文 | 判定测试 | 之后填什么 |
| :-- | :-- | :-- | :-- |
| `element` | 单元素 | **一处**就够：能指着一行说「就是它」 | A + B |
| `pair` | 元素间关系 | **两处或少数几处**，而且**单看每一处都合法**——缺陷在它们的关系里 | D（A 可选） |
| `global` | 全图性质 | 指不出具体处，必须说「整张图」或「所有执行」 | D（A 可选） |
| `other` | 其他 | 以上都不是 | D + 自由描述 |

**正式定义与出处：**

- `element` —— 这一档正是 Chow [1] 与变异算子传统 [7][36] 的定义域：故障即「只改动某一个函数 / 某一个模型元素」。Chow 的三类全部带 "without adding or deleting states" 这类**单点限定**，Lackner & Schmidt 的一阶约束 "exactly one syntactic change" 同理。
- `pair` —— Heimdahl & Leveson [38] 的两条判据都定义在**同一状态同一事件的一组出边**上（"pairwise compared"、"all transitions out of the state"），不定义在单条边上。Dwyer 的 Order patterns 也逐字说是 "related to **pairs** of states/events" [40]。
- `global` —— 可达性、终止性、死锁按定义是整个可达状态空间的性质。工具侧的对应条目是 itemis CREATE 的 `vertex.MustBeReachable` [9]。
- `other` —— 出口。

**与最易混取值的分界：**

| 容易混的一对 | 怎么分 |
| :-- | :-- |
| `element` vs `pair` | 问：**单看你点到的那一处，它自己有毛病吗**？有 → `element`；每一处单看都合法、毛病在它们凑一起 → `pair` |
| `pair` vs `global` | 问：**你能把涉及的处所列举出来吗**？能列举（这两条边、这条边和那个复合态）→ `pair`；只能说「从初始态出发走不到」「存在一条执行」→ `global` |
| 「跨制品矛盾」落哪 | **`locus` 里没有 `cross` 取值，这是有意的。** 「NL 要求恒真的性质、模型允许其反例」在**模型内**的定位就是 `global`（一条违反的执行路径），它的「跨制品」性由**维度 C = `requirement`** 承载。两者是不同的轴，合成一个会让「NL 点名的某个状态缺失」这种既跨制品又单元素的缺陷无处可去 |

### 3.2 一阶编辑约定（决定 §3.4 怎么用）

**本约定只在 `locus = element` 时生效。** 本轴只描述**一次编辑**，依据是 Lackner & Schmidt [7] 的一阶变异约束（"making exactly one syntactic change"）以及他们对「元素替换」的显式排除（"we do not consider the exchange of an element by another, since this can easily be mimicked by removing and inserting the removed element at another point"）。

因此：**若把这条缺陷改对需要两次及以上互不相同的编辑，维度 B 选 `other` 并在自由描述里写明需要哪几步。**

⛔ **但先回头看 §3.1。** 很多「一次编辑改不完」的情形根本不是 `element`，而是 `pair` 或 `global`，那时压根不该问 B。把逻辑层缺陷塞进 `element` + `other`，是本座标系最需要防的一种误填。

这不是兜底，是有信息量的判定。文献里的一阶变异算子按构造覆盖不到多阶缺陷；落进 `other` 的条目数本身就是「文献类型学覆盖不到我们语料」的度量（见 §4.7）。

### 3.3 维度 A · `defect_element` 构件

| 取值 | 中文 | 判定测试（指着作者源那一行问） |
| :-- | :-- | :-- |
| `state` | 状态 | 那一处是（或本应是）一个**状态节点**，包括它挂在哪个父态之下 |
| `transition` | 迁移 | 那一处是**一条边本身**：边在不在、从哪个源态出发、指向哪个目标态 |
| `trigger` | 触发事件 | 那一处是边标签上 `/` **之前、方括号之外**的**事件名** |
| `guard` | 守卫条件 | 那一处是边标签上**方括号 `[...]` 内**的布尔表达式 |
| `effect` | 效应与状态动作 | 那一处是边标签上 `/` **之后**的内容，或状态体内的 `entry` / `exit` / `do` 动作 |
| `variable` | 变量 | 守卫或效应**引用了**某个量，而该量在模型里没有独立声明 |
| `region` | 正交区域（**界外·记录用**） | 那一处是 PlantUML 的**正交区分隔符 `--`**，或它划出的一个并发区槽位（含「区应当有几个」这类数量断言）。只需数 `--` 的条数与它划出的区个数，**不需要判断并发语义本身** |
| `other` | 其他 | 以上都不是。**必须在自由描述里写清它是什么**；若一格装不下（涉及多个取值），同样落这里并写清是哪几个 |

⛔ **`region` 与其余六个取值不是同一种东西**：它 `counts_as_defect = false`，即**可记录、不计入缺陷统计**。理由与准入条件见 §3.7。

**正式定义与出处，逐取值：**

- `state` —— Chow [1] 的第三类以状态数定义："A is said to have extra (missing) states if in order to make A equivalent to A' the number of states in A must be reduced (increased)."；UML 2.5.1 [8] 元类 `State` / `Vertex`；Fabbri 的 FSM 算子组之一（"faults related to the **states**, events and outputs" [6]）。
- `transition` —— Chow [1] 第二类以次态函数定义："changing only the **next-state function** of A"；Lackner & Schmidt [7] 的 `Delete Transition (DTR)` 与 `Change Transition Target (CTT)`；UML 2.5.1 元类 `Transition` 及其 `source` / `target` 关联端。
- `trigger` —— Lackner & Schmidt [7] 的第 (iii) 个变异目标 "triggers"（算子 `DTI` / `ITG`）；UML 2.5.1 `Transition::trigger`；Fabbri 的 events 组 [6]。
- `guard` —— Lackner & Schmidt [7] 的第 (iv) 个变异目标 "guard"（算子 `DGD` / `CGD`）；EFSM 故障类里的 **predicate fault** [3]（该名下无稳定内部结构，见 §2.1）；UML 2.5.1 `Transition::guard`。
- `effect` —— Chow [1] 第一类以输出函数定义："changing only the **output function** of A"；Lackner & Schmidt [7] 的第 (v) 个变异目标 "effect"（算子 `DEF`，且明写 "We consider sending signals to the environment or other components to be part of a transition's effect"）；UML 2.5.1 `Transition::effect`、`State::entry` / `exit` / `doActivity`。
- `variable` —— ⚠️ **本取值的文献支撑最弱，判定测试却很清晰。** EFSM 传统有 **assignment fault**（对上下文变量的更新被破坏）与 **predicate fault** [3]，但**没有「缺少变量声明」这一故障类**——EFSM 的变量集合被假定给定。邻域的三份现成分类学则明确把数据维排除在外：AbsCon 逐字 "this paper **ignores node attributes**" [17]；BEF4LLM 逐字 "data objects **omitted**, as the data perspective is not assessed within the chosen metrics and therefore **outside the scope** of our framework" [18]；Lackner & Schmidt 逐字 "the classes are **merely containers for variables** and diagrams"，即不对其施加变异 [7]。详见 §4.3。
- `region` —— ⚠️ **本取值不承载任何缺陷类型学主张，它是一个记录槽位。** 文献侧确有正交区 / 并发的缺陷条目（见 §3.7 罗列的 UML 2.5.1 fork / join 8 条 constraint、itemis CREATE 的 `transition.SourceNotOrthogonalToTarget`、BEF4LLM 的 concurrency 组 [18]），但它们**全部落在 $M = (S, E, V, Tr, A)$ 之外**，故本取值 `counts_as_defect = false`。⛔ 不得据此把区域相关的发现计入缺陷统计，⛔ 也不得反过来据此声称语料里不存在区域相关问题 —— 两种读法都是错的，理由见 §3.7。
- `other` —— 出口。依据是检查阅读传统自带 `Others / Miscellaneous` 类 [13]，以及 F-A 的自陈："The taxonomy is **an organising scheme rather than a measurement instrument**" [27]。

**与最易混取值的分界：**

| 容易混的一对 | 怎么分 |
| :-- | :-- |
| `state` vs `transition` | 「X 进不去」：X 在作者源里**有没有一行声明**？没有 → `state`；有、只是没入边 → `transition` |
| `trigger` vs `guard` | 看它在标签的哪一侧：方括号**外**是 `trigger`，方括号**内**是 `guard` |
| `guard` vs `variable` | 缺的是**整个条件表达式**（该有 `[...]` 而没有）→ `guard`；条件在、但它引用的量没有声明 → `variable` |
| `effect` vs `state` | 「进入 X 时应发出信号」——发信号是动作，落 `effect`，不是 `state` |
| `transition` vs `state`（目标错） | 一条边接到了错的目标态：落 `transition` + `incorrect`（Chow 的 transfer error），**不落 `state`** |
| `state` 与层次归属 | 「Y 应当是 X 的子态而不是兄弟」：落 `state` + `incorrect`（父容器是状态的属性）。这类在 UML 2.5.1 的 47 条里**没有对应条款**，故维度 C 只能选 `requirement` 或 `other` |

### 3.4 维度 B · `defect_qualifier` 限定词

**判定测试（统一一句）：设想把这条缺陷改对，且只做一次编辑；改完之后，作者源里该类构件的声明条数是变多、不变，还是变少？**

| 取值 | 中文 | 判定测试 | 正式定义（逐字） |
| :-- | :-- | :-- | :-- |
| `missing` | 缺失 | 条数**变多**（新增一个构件，已有构件内容不变） | ODC [12]："the defect was due to an **omission**"；Lackner [7]："**Model element deletion**: a model designer forgets to add a model element" |
| `incorrect` | 错值 | 条数**不变**（只改动某个已有构件的一个属性值） | ODC [12]："the defect was due to a **commission**"；Lackner [7]："**Property change**: a model designer chooses a **wrong value for a property** of a model element … or **wrong transition target**" |
| `extraneous` | 多余 | 条数**变少**（删掉一个已有构件） | ODC [12]："the defect was due to something **not relevant or pertinent**"；Lackner [7]："**Model element insertion**: a model designer inserts a **superfluous** model element" |
| `other` | 其他 | 一次编辑改不完 | 见 §3.1；出口先例见 [13] 的 `Others` 类 |

**与最易混取值的分界：**

| 情形 | 落哪 | 为什么 |
| :-- | :-- | :-- |
| 事件名拼错 / 用了别的写法 | `incorrect` | 改一个属性值，条数不变。**不要**记成 `missing` + `extraneous` ——Lackner [7] 明确把「替换」排除在一阶算子之外 |
| 边接到了错的目标态 | `incorrect` | Chow 的 transfer error，定义就是「只改次态函数」，不增不删状态 |
| 子态挂错父态 | `incorrect` | 父容器是状态的一个属性；条数不变 |
| 整条边不存在 | `missing` | 条数变多 |
| 多出一个 NL 没要求、参考也没有的状态 | `extraneous` | 条数变少。「多余是不是缺陷」在文献里有分歧，见 §4.1 |
| 三个检测事件被塌缩成一个泛化事件 | `other` | 修复要删一条、加三条，是多阶。这类**恰恰是文献一阶算子覆盖不到的**，务必如实落 `other` |
| 一条边既缺守卫又指错目标 | `other`（或拆成两条记录） | 两次互不相同的编辑 |

### 3.5 维度 D · `defect_logic_kind` 逻辑层类型

⭐ **`locus ≠ element` 时填这一轴，`locus = element` 时不问。** 它承担 A×B 结构上表达不了的那一半。

| 取值 | 中文 | 判定测试（可手算，除非另注） |
| :-- | :-- | :-- |
| `nondeterminism` | 非确定性 | 取某状态在**同一事件**下的全部出边守卫，存在一个变量赋值使**其中两条同时为真** |
| `incompleteness` | 守卫不完备 | 同一组守卫，存在一个变量赋值使**全部为假**（即其析取不是永真式） |
| `unreachable` | 不可达 | 从初始态出发的图遍历到不了它 |
| `unintended_terminal` | 非预期终止 | 某状态**及其所有祖先**都没有可用出边（$\mathrm{Post}(s)=\emptyset$），而它不是有意的终态 |
| `nontermination` | 不终止 | NL 要求终会到达某终止条件，而模型存在一条永不到达它的执行。无「与标注无关」的形式定义，见 §4.10 |
| `property_violation` | 时序性质违反 | NL 要求一条时序性质，模型存在一条反例执行。一般需要模型检查器 |
| `priority_conflict` | 优先级冲突 | 存在一个状态配置与事件，使**内层与外层各有一条使能出边**，而哪条先发取决于语义约定 |
| `hierarchy_entry` | 层次进入语义 | 存在一条迁移，其目标是**复合态本身**而非其某个子态，且该复合态有默认入口（于是进入会重跑内部初始） |
| `other` | 其他 | 以上都不是。**必须自由描述** |

**正式定义与出处，逐取值：**

- `nondeterminism` —— Heimdahl & Leveson [38] 逐字："Two transitions with guarding conditions that are **not mutually exclusive** represent conflicting requirements."；同文把该质量命名为 consistency（"free from conflicting requirements and undesired nondeterminism"）。⚠️ UML 2.5.1 **不禁止**它（见 §2.3 与 §4.2），所以判成缺陷时维度 C 多半要选 `requirement`。
- `incompleteness` —— Heimdahl & Leveson [38] 逐字："if the **logical OR** of the conditions on all transitions out of the state triggered by the same event **does not form a tautology**, then there are conditions for which no behavior is specified, i.e., the requirements are **incomplete**."；论文术语为 **d-complete**。
- `unreachable` —— itemis CREATE [9] `vertex.MustBeReachable`："Node is not reachable."；SDMetrics [35] `NoIncoming`（Category: Completeness）："Without incoming transitions, the state can never be reached."；Arendt 等 [32] 异味 3。
- `unintended_terminal` —— Baier & Katoen [41] **Definition 2.4**："State s in transition system TS is called terminal if and only if $\mathrm{Post}(s) = \emptyset$."；SDMetrics [35] `NoOutgoing`："Without outgoing transitions, the state can never be left. **Check if this is merely an oversight or the actually intended behavior.**" ⭐ 后一句给出与「有意终态」的分界：判定「有意与否」要回 NL，所以本取值几乎总是配 `reference = requirement`。⛔ **不要叫它 deadlock**——Baier & Katoen 的 deadlock 要求「至少一个分量仍可继续」，那是并发概念，在无正交区的 $M$ 里不成立（§2.6.3）。⚠️ **判定测试必须把祖先的群迁移算进去**：一个叶状态画不出出边，若其外层复合态有出边，它就不是 terminal。这是本取值最常见的假阳性。⚠️⚠️ **但这一条只对作者源成立，2026-08-13 补注**：本类型学的判定测试按 §3.0 全部落在**作者源 PlantUML** 上，PlantUML 读作 UML，成组迁移语义成立，故上面这句对**判读作者源**是对的。⛔ **它不适用于 `model.fcstm`**——FCSTM 的父态出边**不下传**给活动子态（`pyfcstm/verify/topology.py` 里 `build_leaf_level_macro_graph()` 的函数 docstring 逐字：「Parent-level transitions **whose source is a composite state are therefore considered only after** a descendant leaf explicitly exits to that parent; they are not copied onto every active descendant leaf.」；⚠️ 本处初版误标为「模块注释」且引文为转述，已更正），子态须自己显式 `-> [*]` 才接得上。⭐ 于是同一个叶状态的 terminal 性在两种语义下**相反**：UML 下不是、FCSTM 下是。⛔ 因此**不得**用祖先论据去推翻来自 `pyfcstm inspect` 的 `W_DEADLOCK_LEAF`；该情形的正确归属是 `projection_artifact`（IR 上为真、作者源上为假）。证据与实测分布见 [inspect_capability_boundary.md](../findings/inspect_capability_boundary.md) §一。
- `nontermination` —— ⚠️ **没有与标注无关的形式定义**：Baier & Katoen 全书未定义 livelock / non-progress cycle，SPIN [43] 的 non-progress cycle 相对**用户手工标注的 progress label** 定义。因此本取值只能靠 NL 的终止义务立起来，可用 Dwyer 的 **Existence** 模式表述（「某终止事件必将发生」）。
- `property_violation` —— 用 Dwyer、Avrunin 与 Corbett 的 pattern × scope [39][40] 表述，见 §3.6.1。
- `priority_conflict` —— ⚠️ **这一取值的支撑是「各家语义不一致」这个事实本身**，而不是某一家的规则。UML 2.5.1 明写迁移可以冲突且优先级只是 "a **partial ordering**"（§2.3），而 Harel/STATEMATE 一系与 UML 在内层/外层谁优先上给出相反答案（§2.7）。因此**判定测试只判「存不存在这种局面」，不判「谁对」**——是否算缺陷交给 C 与 NL。
- `hierarchy_entry` —— 判定测试只看语法（目标是复合态本身 + 该复合态有默认入口），这一点可机械判；「重跑内部初始是否构成缺陷」同样交给 C 与 NL。⚠️ 该语义在 UML 与经典 statechart 之间也有分歧（§2.7）。
- `other` —— 出口。

**与最易混取值的分界：**

| 容易混的一对 | 怎么分 |
| :-- | :-- |
| `nondeterminism` vs `incompleteness` | 是同一组守卫的**两个相反方向**：存在赋值让**两条同时真** → 非确定；存在赋值让**全部假** → 不完备。一组守卫可以**同时**犯这两个错，那就拆成两条记录 |
| `unreachable` vs `unintended_terminal` | 进不去 → `unreachable`；进得去但出不来 → `unintended_terminal` |
| `unintended_terminal` vs 有意终态 | 看 NL 是否要求在此终止。SDMetrics 自己就把这条判断留给人。⛔ 先排除祖先群迁移 |
| `nontermination` vs `property_violation` | 违反的性质**只关乎「终止会发生」** → `nontermination`；是别的时序性质 → `property_violation` |
| `unintended_terminal` vs `nontermination` | 停住了不动 → `unintended_terminal`；一直在动但到不了终点 → `nontermination` |
| `priority_conflict` vs `nondeterminism` | 两条使能出边在**同一个状态**上 → `nondeterminism`；分处**内层与外层**、靠层次优先级消解 → `priority_conflict` |
| 任何一条 vs `element` 分支 | 若你能指着一行说「就是它错了」，那就该在 §3.1 选 `element`，根本不该来这一轴 |

### 3.6 维度 C · `defect_reference` 参照物

若工作单保留 `basis` 字段，本维度**不要**同时上（见 §3.0）。

**判定测试：判定这条缺陷成立，你需不需要引用 NL 的某一句？**

| 取值 | 中文 | 判定测试 | 正式定义（逐字） |
| :-- | :-- | :-- | :-- |
| `language` | 语言规则 | **不引用 NL 任何一句**就能判定；依据是建模语言 / 元模型的良构性规则 | SIQ [16]："Verification addresses the need to establish a particular **syntactic** quality of a model in relation to various **formalized properties and rules**" |
| `requirement` | 需求文本 | **必须引用 NL 的某一句**才能判定 | SIQ [16]："Validation relates to the **semantic** quality of the model, i.e. whether a model makes truthful and accurate statements about **the domain it intends to capture**" |
| `other` | 其他 | 两者都不是 | 出口。典型落点：只能靠参考模型对照；或依据是「人读不懂」（即 LSS 的 pragmatic 层，本文件不给它独立取值，理由见 §2.5 与 §4.4） |

**判 `language` 时可以直接引的成文条款**（避免判读者自己发明规则）：UML 2.5.1 [8] Chapter 14 的 47 条（例如 `Region::initial_vertex`、`Pseudostate::outgoing_from_initial`、`FinalState` 的 6 条、`Transition::transition_vertices`）；itemis CREATE 校验器 [9] 的 `vertex.MustBeReachable`、`region.MustNotHaveMultipleDefaultEntries`、`finalstate.NoOutTransitions`、`state.name.required`；Stateflow [10] 的 unreachable state / dangling transition / unreachable junction。

⚠️ **两处已知的陷阱**：其一，「多条出边守卫不互斥」**不能**判 `language`——UML 2.5.1 明写允许迁移冲突且只给出偏序（§2.3）；itemis CREATE 也靠优先级消解而不报错。其二，「复合态缺默认入口」**不能**判 `language`——UML 明确把它留作语义变异点。这两条要判成缺陷，必须走 `requirement` 并给出 NL 逐字依据。

#### 3.6.1 维度 E（可选）· `defect_property_pattern` 性质模式

**只在需要写清「修好之后怎样才算 ok」时填**，尤其是 `defect_logic_kind = property_violation` 那一档。取值是 Dwyer、Avrunin 与 Corbett [39][40] 的 **pattern × scope** 组合，两者各选一个：

| 轴 | 取值（逐字，见 §2.6.2） |
| :-- | :-- |
| pattern（8） | `Absence` 不出现 · `Universality` 恒成立 · `Existence` 必出现 · `Bounded Existence` 有界出现 · `Precedence` 先于 · `Response` 响应 · `Precedence Chain` 先于链 · `Response Chain` 响应链 |
| scope（5） | `Globally` 全程 · `Before` 直到某事件之前 · `After` 某事件之后 · `Between` 两事件之间 · `After-Until` 某事件后直到（第二事件可不出现） |

判定测试：把这条 NL 义务改写成一句「**在〈scope〉内，〈pattern〉〈对象〉**」；改写不出来就不填。

⚠️ **为什么设为可选而不是必填**：40 个组合、且需要判读者先把 NL 句子形式化，这不是「不查手册就能选对」的负担。⭐ 但它填得起来的时候价值很高——它同时给出了缺陷描述与验收判据，是三个字段里「修好算什么」那一项的现成语言。**建议先在少量样本上试填，测通过率再决定是否推广。**

采用时必须带上 §2.6.2 引的两条口径：scope 是**可选**的（分隔事件不出现则性质自动为真）；`Before` / `After` 相对**首次**出现解释。

### 3.7 界外内容：可记录、不计分

时钟约束、状态不变式、正交区并发语义落在 $M$ 之外。文献里对应的界外条目（列出以便审计）：UML 2.5.1 与 fork / join / 正交区绑定的 8 条 constraint 及散文条款 "A Transition from one Region to another in the same immediate enclosing composite State is not allowed."；itemis CREATE 的 `transition.SourceNotOrthogonalToTarget`；BEF4LLM syntactic 第 9 项 "Split gateway has matching join gateway" 与 pragmatic 的 concurrency 组 [18]；von der Beeck [21] 与 Crane & Dingel [22] 里关于并发与进入/退出顺序的比较维度；时间自动机变异算子（时钟一族）。

**2026-08-13 更正：本节此前写「不得取为维度取值」，那一条已撤销。** 撤销的理由不是放宽边界，而是原写法在两头都站不住：把界外对象**赶出座标系**，等于让它既不能被记录、也不能被统计，于是同一批材料在报表上呈现为「什么都没发生」。[CLAUDE.md](../../../../../CLAUDE.md) 的建模对象边界明写两条约束**同时**成立 —— 既不得把并发 / 时间类问题记为「方法未能检出」，**也不得反过来声称「这些模型没有并发 / 时间问题」**。给它一个可记录、但 `counts_as_defect = false` 的槽位，是唯一能同时满足这两条的做法。

现行口径：

| 界外族 | 有没有维度取值 | 怎么落 |
| :-- | :-- | :-- |
| 正交区域及其数量 | **有** —— `defect_element = region` | 照常登记，`counts_as_defect = false`，不进缺陷统计 |
| 时钟 / 计时 / 秒级约束 | 没有 | 写进自由描述，回收后人工分拣 |
| 状态不变式 | 没有 | 同上 |
| entry / exit 动作次序 | 没有（判定测试立不住，见 §3.8 第 6b 行与 §4.9） | `pair` + `logic_kind = other` + 自由描述 |

**为什么只给正交区域开了槽位、时钟与不变式没开**：判据是「有没有一条只看制品就能唯一判定的测试」。正交区在 PlantUML 里有**逐字的语法载体**（`--` 分隔符），数它有几条、划出几个区是纯词法操作，符合 §11 对确定性门的准入要求。时钟与不变式在本语料的作者源里没有对应语法载体（PlantUML 状态图不写时钟约束），判读者只能从散文语义推断，故不设取值。

⛔ **区域取值不是「边界被放宽了」。** 它记录的是「这里有一处与正交区有关的差异」，**不主张它是一个缺陷**。任何把 `region` 计入命中率、覆盖率或缺陷数的做法都是错的。

### 3.7.1 任一轴选 `other` 时必须附一句说明

**硬规则：五个轴中的任意一个取 `other`，都必须同时给出一句自然语言说明。** 说明只需回答两件事之一：

1. 它到底是什么（`other` 是出口，出口不写清等于没分类）；
2. 或者，为什么单值装不下 —— 即这一条**涉及多个取值**，写清是哪几个。

这条是**确定性判据**（「`other` 在不在、说明字段空不空」只看字段值即可唯一判定），故按 [CLAUDE.md](../../../../../CLAUDE.md) §11 允许做成校验器的 `E` 级门，见 [validate.py](../../ledger_v2/provenance/relabel/validate.py)。⛔ 与之相对，「这句说明写得对不对」是语义判断，**不做成门**。

### 3.8 验收：座标系对六类逻辑层缺陷的逐条表达检查

**这张表是本座标系的验收判据。** 若某一行填不出坐标，说明座标系还是浅的。

| # | 逻辑层缺陷 | `locus` | `logic_kind` | `reference` | 可选 E | 表达得了吗 |
| --: | :-- | :-- | :-- | :-- | :-- | :-: |
| 1 | 非确定性：同状态同触发，两条守卫重叠 | `pair` | `nondeterminism` | 多为 `requirement`（UML 不禁止） | —— | ✅ |
| 2 | 守卫不完备：某赋值下无迁移可用 | `pair` | `incompleteness` | `language` 或 `requirement` | —— | ✅ |
| 3a | 不可达 | `global` | `unreachable` | `language`（工具规约有成文条目） | —— | ✅ |
| 3b | 非预期终止（原表述「死锁」） | `global` | `unintended_terminal` | `requirement`（「是否有意终止」要问 NL） | —— | ✅ |
| 3c | 活锁 / 不终止 | `global` | `nontermination` | `requirement` | `Existence` × scope | ✅ |
| 4 | 层次语义交互：迁移指向复合态导致内部阶段重置 | `pair` | `hierarchy_entry` | `requirement` | —— | ✅ |
| 5 | 跨制品矛盾：NL 要求恒真的性质，模型允许反例 | `global` | `property_violation` | `requirement` | `Universality` × scope | ✅ |
| 6a | 迁移优先级：内层与外层同时使能 | `pair` | `priority_conflict` | `requirement` | —— | ✅ |
| 6b | entry / exit 动作次序 | `pair` | `other`（自由描述）| `requirement` | —— | 见下 |

**唯一一处表达不干净的是 6b（动作执行次序）。** 我没有为它单设取值，理由是判定测试立不住：UML 与经典 statechart 对跨层次迁移的 exit/entry 次序确有成文规定，但**判读者要判「次序错了」，必须先确定该模型遵循哪一套语义**——这正是 §2.7 说的、判定测试不成立的那一类。⛔ 硬设一个取值只会制造两人选法不一致的字段。**它落 `pair` + `other` 并自由描述，同时在 §4.9 记为已知空白。**

⭐ 另注意第 5 行：它证明了 §3.1 不设 `cross` 取值的决定是对的——「跨制品」由 `reference = requirement` 承载，`locus` 照常描述它在模型内的定位，两者不打架。

## 4. 分歧与空白

### 4.0 「经典 FSM 故障模型」这句话本身就是合并出来的

这是本轮核验中最值得单独记的一条，因为它会直接影响我们怎么在论文里引这一支。

| 出处 | 故障类数 | 多余状态怎么处理 | 用词 |
| :-- | :-: | :-- | :-- |
| Chow 1978 [1] | **3** | 是一个故障类（第 3 类，extra 与 missing 合为一类） | errors，全篇无 "fault" |
| Fujiwara 等 1991 [2] | **2** | 不是故障类，是一条前提（状态数上界 $m$） | 同一篇内 error / fault 混用 |
| Hierons 等 2009 [30] | **2** | 未列 | faults |
| El-Fakih 等 2016 [3]（EFSM） | **4** | 未列；另加 predicate / assignment 两类 | faults |

因此：**「经典 FSM 故障模型 = output + transfer + extra + missing states」从上面任何一篇都引不出来。** 要用这个四元组必须同时引 [1] 与 [2] 并注明是合并口径；且 "output fault" 是对 Chow "operation error" 的后世改名，不能当作 Chow 的原话。

对本类型学的影响是正面的：维度 A 与维度 B **不依赖**这四类里的任何一个具体命名，只依赖两篇共同的定义**形式**（「要改哪个函数 / 增删多少个元素」）。这个形式在两篇里完全一致。

### 4.1 「多余」是不是缺陷——文献不一致

Chow [1] 把 extra states 列为故障类，但故障域**有界**（`m-n`）。LSS [14] 的 semantic validity 要求模型中不含域外陈述，即多余是缺陷。ODC [12] 有 `Extraneous` 值。

但形式化一致性关系给的是**相反**答案：`ioco` [28] 只要求规约的 suspension trace 上输出集合被包含，规约未规定的输入是 **underspecified**，实现有自由度——**换言之，规约没说的地方多做了，不构成不符合**。UML 2.5.1 同样不禁止多余元素。

后果：判读者遇到「模型多了一个 NL 没要求的状态」时，落 `extraneous` 是形态判断（没问题），但**它算不算缺陷取决于我们采用哪种符合性口径**。这必须由工作单的另一个字段（`counts_as_defect` 或等价物）承担，不能塞进本类型学。

### 4.2 「不确定性」是不是缺陷——文献不一致，且我们必须自己裁

AbsCon [17] 的 5 条 flowchart 约束里有一条要求 "each outgoing relation from a decision node has a **non-empty condition**"；itemis CREATE 报 `Dead transition`；EFSM 的一致性要求逐字是「同源同输入的诸守卫互斥且析取为真」[3]。但 UML 2.5.1 明确**允许**冲突迁移（§2.3）。

本文件的处置是：`conflicting` **不设为维度 B 的第四个值**。理由是它在编辑口径下并无独立性——修复一处不确定性就是**改一个守卫**，条数不变，落 `incorrect`。这样既保住了「三值互斥且判定测试唯一」，又不丢信息（维度 A 会记下它落在 `guard` 上）。

### 4.3 变量维：文献里几乎是空的

`variable` 是本文件唯一一个**判定测试清晰、但文献支撑不足**的取值。三份邻域分类学各自显式排除数据维（逐字见 §3.2），EFSM 传统只在守卫与赋值里**引用**变量而不把变量声明本身当故障类。

这与我们台账的实测分布形成一个值得注意的对照：现台账 126 条里 `element_of_M` 为 `V` 的只有 **2 条**（`Tr` 60 / `S` 38 / `A` 18 / `E` 7 / 多个 1）。⚠️ **不要把这条对照读成「所以台账没问题」**——它同样可以读成「整个领域都没在看这一维」。两种读法本轮无法区分，这正是需要人工判读来定的事。

### 4.4 语用维：整支没有可操作判据

LSS / SIQ 的第三层（pragmatic，人读不读得懂）在文献里是正式的一层，BEF4LLM 甚至给了 15 项指标——但那 15 项全部依赖经验阈值，而它自己就砍掉过一个「没有阈值可用」的维度（§2.5）。本文件因此不给它取值。**代价是：若某条发现的实质是「这个模型对了但没法读」，它只能落 `defect_reference = other`。** 判读者遇到这种情形请在自由描述里写明，这是已知的类型学缺口而不是判读者的错。

### 4.5 「模型 vs 需求文本」这个参照物，被规则目录传统按构造排除

这是本轮最值得记的一条空白，且有**两份已发表工作的显式声明**（本仓库先前已逐字核验，见 [历史来源档案](../../../related_work/provenance/archive/legacy_20260821/evidence_distribution.md) §3.3b）：

- Lange 等 2003 [29]（**实质性理由**）："Hence we **exclude the relations with requirements** and implementation artefacts. The main reason for this is that automated checking the consistency and completeness of the relation between requirements and design … **require very different techniques or may even turn out to be infeasable without significant human contributions.**"
- Torre 等 [25]（**筛文准则**，排除条件之一）："EPs which discussed consistency rules between UML diagrams and other **non-UML sources of data, such as requirements** or source code."

同样的替换也发生在 LLM 时代：AbsCon 定义第三类时说的是「相对描述不准确」，实测时换成了对参考模型的比对，理由逐字为 "automated comparison of a graph model with the natural language description **may be unreliable**" [17]；BEF4LLM 的 semantic 七项全部要 ground-truth 模型 [18]。

⚠️ **两条边界不得逾越**：这些文献说的是「我们不做」，不是「没人做」；也不得据此主张「因此我们的做法有依据」——它只支撑一件事，即 `defect_reference = requirement` 这一格在**规则目录传统**里的缺席是**构造性的**。

⛔ **而且确实「有人做」——本轮找到了反例，必须一并写出，否则这一节会读成过度主张。** Travassos、Shull、Fredericks 与 Basili 1999 [37]（全文已取到，Table 1 与 §3 逐字核对）正是以需求文档为参照物的成文缺陷分类，且**明确覆盖状态图**（该文有一整节 "Reading Sequence x State diagrams"，实验材料含状态图）。其 Table 1 的「Applied to design」列逐字：

> **Omission** — "One or more design diagrams that should contain some concept from the general requirements or from the requirements document do not contain a representation for that concept."
>
> **Incorrect Fact** — "A design diagram contains a misrepresentation of a concept described in the general requirements or requirements document."
>
> **Extraneous Information** — "The design includes information that, while perhaps true, does not apply to this domain and should not be included in the design."

它还把这件事命名了，逐字："**Vertical reading** refers to reading techniques that are used to read documents built in different software lifecycle phases… **Traceability** between the phases is the most important feature here."

因此这一节的正确表述是：**缺席的是「模型-需求」这一参照物在规则目录 / 变异算子 / 模型质量度量三支里的构造性缺席，不是整个领域的缺席。** 检查阅读传统做了这件事，只是它靠人读而非靠可机械执行的规则。⭐ 这反而是对我们有利的定位：我们要做的是**把 Travassos 那一列从人工阅读推进到可断言的自动判定**，而不是「第一个把 NL 当真值的人」。⛔ 论文里不得写成后者。

### 4.6 语义依赖型缺陷：没有类型学槽位

一份制品可能在某套 statechart 语义下正确、在另一套下错误（von der Beeck [21] · Crane & Dingel [22] · Fecher 等 [23] 各自枚举了这类分歧点；UML 2.5.1 自己留了语义变异点）。这类「缺陷本身是语义依赖的」在本类型学里没有槽位，只能落 `other`。这不是疏漏，是有意的：判读者无法靠看制品判定它，需要协议层先裁定采用哪套语义。

### 4.7 一阶算子覆盖不到「融合 / 塌缩」类缺陷

「三个事件被写成一个泛化名」「析取守卫被压成一个标签」这类缺陷需要多阶编辑才能修好，因此按 §3.1 一律落维度 B 的 `other`。文献侧确认了这是个真空：Lackner & Schmidt [7] 明确只做一阶并显式排除「替换」；Fabbri 一系同样是逐算子的一阶变异。**`other` 的条目数与占比应当单独统计并进报告**——它直接度量「文献类型学在多大比例上说不出我们语料里的缺陷」。

### 4.8 状态机专属的实证缺陷分类学不存在

检索结果一致：严谨的实证缺陷分类学主要针对类图、活动图与 ER 模型；状态机侧最接近的是 statechart 特征与缺陷数的相关性研究，以及 Lange & Chaudron 一系（其轴是影响而非形态，§2.7）。**我们如果做出一份状态机的形态分类学并配上实测分布，这本身有新意**——但那是论文层面的判断，不是本文件的主张。

### 4.9 动作执行次序：有成文规定，但判定测试立不住

跨层次迁移的 exit / entry 动作次序在 UML 与经典 statechart 里都有成文规定，**但两家不完全一致**，且一份 PlantUML 制品并不声明它遵循哪一套。于是「次序错了」这个判断在判读者手上不可判定——它先要一个语义裁定。座标系为它保留 `pair` + `other`，并**不**假装能分类它。⚠️ 若后续协议层裁定了采用哪套语义，这一条就可以升格为正式取值。

### 4.10 「活锁」没有与标注无关的形式定义

`unreachable` 与 `unintended_terminal` 现已有教科书级定义（Baier & Katoen 的 Definition 2.10 与 2.4，§2.6.3）。⛔ **但 `nontermination` 没有。** 我已 grep 全书确认：`livelock` 只在 p. 3 的历史引言里出现一次、无定义，`non-progress cycle` 一次都没有；该书把邻近概念形式化为 **starvation freedom**。唯一有成文定义的是 SPIN [43]，而它**相对用户手工标注的 progress label** 定义——也就是说，「与标注无关的活锁」这个概念在标准文献里并不存在。

后果：`nontermination` 只能靠 **NL 的终止义务**立起来（配 `reference = requirement`），不能作为「模型自身即可判定」的缺陷主张。⛔ 论文里不得写「我们检测活锁」，只能写「我们检查 NL 要求的终止义务是否被满足」。

另一处仍未闭合：`unintended_terminal` 与「有意终态」的分界，任何工具规约都没有给出机械判据——SDMetrics 自己把这一判断留给人（"Check if this is merely an oversight or the actually intended behavior."）。

### 4.11 逻辑层的两条判据来自 RSML，可移植性需要论证

Heimdahl & Leveson 的两条判据（§2.6.1）之所以**可判定**，依赖 RSML 把行为强制成数学函数这一前提。搬到 PlantUML / FCSTM 上时，判据的**形式**不变（守卫两两可满足性、守卫析取的永真性），但「模型整体因此就 d-complete 且 consistent」这个**组合性结论**不能直接搬——那要重新论证。⛔ 论文里不得写成「我们的检查遵循 Heimdahl & Leveson 的方法，因此保证 d-completeness」。另外论文自陈判据**保守**，会产生虚报（"spurious error reports may be generated"）。

## 5. References

编号按首次引用顺序，唯 [30]–[37] 为初稿编号定下后补做的核验，附在各自最相关的分组末尾。

**取证档位说明**：本节区分三档——**全文/源码已取到并逐字核对**（最高）· **仅核书目**（Crossref / 出版页确认存在与卷期页，内容未读）· **他人核验、我未独立复核**（最低，逐条注明）。

**FSM / EFSM 故障模型**

[1] T. S. Chow. *Testing Software Design Modeled by Finite-State Machines*. IEEE Transactions on Software Engineering, SE-4(3):178–187, 1978. [DOI 10.1109/TSE.1978.231496](https://doi.org/10.1109/TSE.1978.231496) · [自由 PDF](https://archiv.infsec.ethz.ch/intranet_secured/r/1/chow-testingFSMs.pdf)。全文已取到并逐段核对；三类定义在 p. 182。

[2] S. Fujiwara, G. v. Bochmann, F. Khendek, M. Amalou, A. Ghedamsi. *Test Selection Based on Finite State Models*. IEEE Transactions on Software Engineering, 17(6):591–603, 1991. [DOI 10.1109/32.87284](https://doi.org/10.1109/32.87284) · [自由 PDF（uOttawa）](https://www.site.uottawa.ca/~bochmann/Curriculum/Pub/1991%20-%20Test%20selection%20based%20on%20finite%20state%20models.pdf)。该 PDF **无文本层**（CCITTFax 扫描件）；p. 591 的两句逐字引文系渲染成图后**读图核对**所得，非文本抽取。

[3] K. El-Fakih, N. Yevtushenko, M. Bozga, S. Bensalem. *Distinguishing Extended Finite State Machine Configurations Using Predicate Abstraction*. Journal of Software Engineering Research and Development, 4:1, 2016. [DOI 10.1186/s40411-016-0027-4](https://doi.org/10.1186/s40411-016-0027-4)。开放获取，全文已取到；EFSM 四类故障那一句已逐字核对。该句是**二手归属**（记给 Bochmann & Petrenko 1994 与 El-Fakih et al. 2003），**两个源头本轮均未核**。同组另有一篇实证评估可参：*An Assessment of Extended Finite State Machine Test Selection Criteria*, JSS 123:106–118, 2017, [DOI 10.1016/j.jss.2016.09.044](https://doi.org/10.1016/j.jss.2016.09.044)（仅核书目）。

[30] R. M. Hierons 等. *Using Formal Specifications to Support Testing*. ACM Computing Surveys, 41(2), 2009。§5.2 的两类故障（output faults / state transfer faults）逐字引文由协作核验者读原文取得，**本人未独立复核**；DOI 未独立确认。作为 §4.0 的反向证据使用。

[31] D. R. Kuhn. *Fault Classes and Error Detection Capability of Specification-Based Testing*. NIST NISTIR 6140。用于说明 "predicate fault" 的内部结构各家自定（Variable Negation Fault / Associative Shift Fault / Operator Reference Fault 出自布尔规约故障类）。**本人未独立复核**。

**规约级变异算子**

[4] S. C. P. F. Fabbri, M. E. Delamaro, J. C. Maldonado, P. C. Masiero. *Mutation Analysis Testing for Finite State Machines*. ISSRE 1994, pp. 220–229. [DOI 10.1109/ISSRE.1994.341378](https://doi.org/10.1109/ISSRE.1994.341378)。**全文未取到**，本文件只使用 [6] 的转述。

[5] S. C. P. F. Fabbri, J. C. Maldonado, T. Sugeta, P. C. Masiero. *Mutation Testing Applied to Validate Specifications Based on Statecharts*. ISSRE 1999, pp. 210–219. [DOI 10.1109/ISSRE.1999.809326](https://doi.org/10.1109/ISSRE.1999.809326)。**全文未取到**（IEEE Xplore 受限），逐条算子名未知。

[36] S. C. P. F. Fabbri, J. C. Maldonado, T. Sugeta, P. C. Masiero. *Teste de Especificações Baseadas em Statecharts*. USP-ICMC, Notas Didáticas 41, Dez./1999。[Wayback 存档 PDF](https://web.archive.org/web/2020id_/https://web.icmc.usp.br/SCATUSU/RT/Notas_Didaticas/ND_41.pdf)。全文已取到；Tabela 4.1（PDF 第 60 页）的 35 条算子由**渲染成图后逐行读图**核对——该 PDF 的 OCR 层系统性混淆 `l`/`I`，`pdftotext` 结果不可信，复核者请同样读图。它是 ISSRE'99 论文 [5] 的**同组同期技术报告**，不是那篇论文本身；两者算子集是否完全一致**未经证实**。

[6] Y. Jia, M. Harman. *An Analysis and Survey of the Development of Mutation Testing*. IEEE Transactions on Software Engineering, 37(5):649–678, 2011. [DOI 10.1109/TSE.2010.62](https://doi.org/10.1109/TSE.2010.62)。全文 PDF 已取到，§ Specification Mutation 逐字引用。

[7] H. Lackner, M. Schmidt. *Potential Errors and Test Assessment in Software Product Line Engineering*. MBT 2015, EPTCS 180:57–72. [DOI 10.4204/EPTCS.180.4](https://doi.org/10.4204/EPTCS.180.4)。开放获取，全文 PDF 已取到，§2.2 与 §4.2.2 逐字引用。

**逻辑层：完备性、一致性与性质规约**

[38] M. P. E. Heimdahl, N. G. Leveson. *Completeness and Consistency in Hierarchical State-Based Requirements*. IEEE Transactions on Software Engineering, 22(6):363–377, 1996. [DOI 10.1109/32.508311](https://doi.org/10.1109/32.508311) · [自由 PDF](http://dslab.konkuk.ac.kr/Class/2012/12SIonSE/Key%20Papers/Completeness%20and%20consistency%20in%20hierarchical%20state-based%20requirements.pdf)。全文已取到；p. 370 左栏的两条判据因双栏抽取错乱而由**渲染页面后读图**核对。会议版：*Completeness and Consistency Analysis of State-Based Requirements*, ICSE 1995, pp. 3–14, [DOI 10.1145/225014.225015](https://doi.org/10.1145/225014.225015)（未取）。

[39] M. B. Dwyer, G. S. Avrunin, J. C. Corbett. *Patterns in Property Specifications for Finite-State Verification*. ICSE 1999, pp. 411–420. [DOI 10.1145/302405.320258](https://doi.org/10.1145/302405.320258)。Crossref 给出两条并存记录：ACM 版 [DOI 10.1145/302405.302672](https://doi.org/10.1145/302405.302672)（pp. 411–420，1999）与 IEEE 版 [DOI 10.1109/icse.1999.841031](https://doi.org/10.1109/icse.1999.841031)。**论文原文本轮未取到**；本文件引用的 pattern 与 scope 定义全部来自作者维护的官方模式库 [40]，不来自论文。较早的工作坊版：*Property Specification Patterns for Finite-State Verification*, FMSP 1998, pp. 7–15, [DOI 10.1145/298595.298598](https://doi.org/10.1145/298595.298598)。

[40] M. B. Dwyer 等. *Temporal Specification Patterns*（作者维护的在线模式库）。[首页](https://matthewbdwyer.github.io/psp/) · [The Patterns](https://matthewbdwyer.github.io/psp/patterns.html) · [Occurrence](https://matthewbdwyer.github.io/psp/patterns/occurrence.html) · [Order](https://matthewbdwyer.github.io/psp/patterns/order.html) · [Scopes](https://matthewbdwyer.github.io/psp/patterns/scopes.html)。页面已取到并逐字核对；检索日期 2026-08-13。

[41] C. Baier, J.-P. Katoen. *Principles of Model Checking*. MIT Press, 2008。全书 PDF 已取到；Definition 2.4（Terminal State）· Definition 2.10（Reachable States）· §3.1 Deadlock 三处逐字核对，并已 grep 全书确认 `livelock` 仅在 p. 3 引言出现一次、`non-progress cycle` 零次。

[42] M. L. Crane, J. Dingel. *UML vs. Classical vs. Rhapsody Statecharts: Not All Models Are Created Equal*. Queen's University Technical Report 2005-501。[开放获取 PDF](https://research.cs.queensu.ca/TechReports/Reports/2005-501.pdf)。**本人未独立复核**；由协作核验者取得，用作 [22] 那篇付费 SoSyM 论文的开放替代。

[43] SPIN / Promela 手册，`progress` labels。[spinroot.com/spin/Man/progress.html](https://spinroot.com/spin/Man/progress.html)。**本人未独立复核**；由协作核验者逐字取得。用于说明 non-progress cycle 相对用户标注定义。

[44] A. van Lamsweerde, R. Darimont, E. Letier. *Managing Conflicts in Goal-Driven Requirements Engineering*. IEEE Transactions on Software Engineering, 24(11):908–926, 1998. [DOI 10.1109/32.730542](https://doi.org/10.1109/32.730542) · [作者预印本](http://www0.cs.ucl.ac.uk/staff/e.letier/publications/Conflicts-TSE.pdf)。**本人未独立复核**（协作核验者读全文并渲染 pp. 10–11 读图取得公式）。相关：van Lamsweerde & Letier, *Handling Obstacles in Goal-Oriented Requirements Engineering*, TSE 26(10):978–1005, 2000, [DOI 10.1109/32.879820](https://doi.org/10.1109/32.879820)。⛔ 「strong conflict」一词**不出自** 1998 年这篇，勿如此归属。

[45] B. Alpern, F. B. Schneider. *Defining Liveness*. Information Processing Letters, 21(4):181–185, 1985. [DOI 10.1016/0020-0190(85)90056-0](https://doi.org/10.1016/0020-0190%2885%2990056-0) · [作者 PDF](https://www.cs.cornell.edu/fbs/publications/DefLiveness.pdf)。**本人未独立复核**。术语源头：Lamport, *Proving the Correctness of Multiprocess Programs*, IEEE TSE SE-3(2):125–143, 1977, [DOI 10.1109/TSE.1977.229904](https://doi.org/10.1109/TSE.1977.229904)。

**建模语言与工具的良构性规则**

[8] Object Management Group. *OMG Unified Modeling Language (OMG UML), Version 2.5.1*, formal/2017-12-05, Clause 14 StateMachines. [omg.org/spec/UML/2.5.1](https://www.omg.org/spec/UML/2.5.1/)。本仓库已逐条开采，见 [uml251_constraints.md](../../../related_work/provenance/uml251_constraints.md)。

[9] itemis CREATE / YAKINDU Statechart Tools 校验器源码。[SGraph validators](https://github.com/itemisCREATE/statecharts/tree/master/plugins/org.yakindu.sct.model.sgraph/src/org/yakindu/sct/model/sgraph/validation) · [STextValidationMessages.java](https://github.com/itemisCREATE/statecharts/blob/master/plugins/org.yakindu.sct.model.stext/src/org/yakindu/sct/model/stext/validation/STextValidationMessages.java)。逐字消息串自源码读取。

[10] MathWorks. *Detect Modeling Errors During Edit Time*（Stateflow 文档）。[mathworks.com/help/stateflow/ug/stateflow-edit-time-checks.html](https://www.mathworks.com/help/stateflow/ug/stateflow-edit-time-checks.html)

[32] T. Arendt, F. Mantz, G. Taentzer. *UML Model Quality Assurance Techniques*. Philipps-Universität Marburg, Fachbereich Mathematik und Informatik, 2009-10-21（SPES 2020 AP4 交付件）。[Wayback 存档 PDF](https://web.archive.org/web/20170705091225/http://spes2020.informatik.tu-muenchen.de/results/AT-AP4-D-AT-4_1_g.pdf)。全文已取到；§3.4 的 5 条状态机异味与其 bibliography 键 `[1]` / `[46]` 均逐字核对。常被引的 2010 年 Arendt & Taentzer 技术报告本轮**未能取到**（无 PDF、无报告号、无 DOI）。

[33] S. W. Ambler. *The Elements of UML Style*. Cambridge University Press, 2002。[32] 的 `[1]`、SDMetrics 的 `[Amb03]` 均指向本书（或其后续版本）。未取到原书。

[34] C. Rupp, S. Queins, B. Zengler. *UML 2 glasklar*. Hanser Fachbuchverlag, 2007。[32] 的 `[46]`、SDMetrics 的 `[JRH04]` 均指向本书。未取到原书。

[35] SDMetrics User Manual, Appendix C: List of Design Rules。[C.17 Region Rules](https://www.sdmetrics.com/manual/Rules_region.html) · [C.18 State Rules](https://www.sdmetrics.com/manual/Rules_state.html) · [C.16 Statemachine Rules](https://www.sdmetrics.com/manual/Rules_statemachine.html)。页面已取到并逐字核对（含 `Correctness` / `Completeness` / `Style` 分类与 WFR 标记）；检索日期 2026-08-13。

[37] G. H. Travassos, F. Shull, M. Fredericks, V. R. Basili. *Detecting Defects in Object-Oriented Designs: Using Reading Techniques to Increase Software Quality*. OOPSLA 1999, pp. 47–56. [DOI 10.1145/320384.320389](https://doi.org/10.1145/320384.320389) · [自由 PDF](https://www.cs.umd.edu/~basili/publications/technical/T126.pdf)。全文已取到；Table 1 的五类定义（含「Applied to design」列）与 vertical/horizontal reading 定义逐字核对；该文含独立的 "Reading Sequence x State diagrams" 一节。

**通用缺陷分类**

[11] R. Chillarege, I. S. Bhandari, J. K. Chaar, M. J. Halliday, D. S. Moebus, B. K. Ray, M.-Y. Wong. *Orthogonal Defect Classification — A Concept for In-Process Measurements*. IEEE Transactions on Software Engineering, 18(11):943–956, 1992. [DOI 10.1109/32.177364](https://doi.org/10.1109/32.177364)。仅核书目，全文未取。

[12] IBM. *Orthogonal Defect Classification v5.2 for Software Design and Code*. [PDF](https://s3.us.cloud-object-storage.appdomain.cloud/res-files/70-ODC-5-2.pdf)。`Qualifier` 三值的完整定义出自此文档，**不必然出自 [11]**。

[13] F. Shull, I. Rus, V. Basili. *How Perspective-Based Reading Can Improve Requirements Inspections*. IEEE Computer, 33(7):73–79, 2000. [PDF](https://www.cs.umd.edu/~basili/publications/journals/J79.pdf)。五类缺陷（Omission / Incorrect Fact / Inconsistency / Ambiguity / Extraneous Information）的分类归属经二手核实，**未回原文逐字核对**；其更早源头通常追至 Basili & Weiss 对 A-7 需求文档的分析。

**概念模型质量框架**

[14] O. I. Lindland, G. Sindre, A. Sølvberg. *Understanding Quality in Conceptual Modeling*. IEEE Software, 11(2):42–49, 1994. [DOI 10.1109/52.268955](https://doi.org/10.1109/52.268955)。**全文未取到**（可获取副本失效）；书目经 Crossref 核实，三层划分经 [15][16] 二手确认。

[15] H. A. Reijers, J. Mendling, J. Recker. *Business Process Quality Management*. In: Handbook on Business Process Management 1, Springer, pp. 167–185, 2010. [DOI 10.1007/978-3-642-00416-2_8](https://doi.org/10.1007/978-3-642-00416-2_8)。仅核书目。

[16] H. A. Reijers 等. *Process Modelling Quality: A Framework and Research Agenda*（技术报告）。[PDF](https://hreijers.win.tue.nl/H.A.%20Reijers%20Bestanden/TechnicalReport.pdf)。全文已取到，SIQ 三层的 verification / validation / certification 逐字引自此文。

**LLM 时代的模型质量分类学（本仓库邻域卡片已核）**

[17] B. Chen 等. *Accurate and Consistent Graph Model Generation from Text with Large Language Models*（AbsCon）. MODELS 2025, pp. 130–141. [DOI 10.1109/MODELS67397.2025.00018](https://doi.org/10.1109/MODELS67397.2025.00018) · [arXiv:2508.00255](https://arxiv.org/abs/2508.00255)。卡片见 `paper_stm_issue_discover/related_work/neighborhood/cards/`——该目录目前**只在 PR #186 的分支 `paper1/l3-neighborhood-llm-survey` 上**，本分支尚无此路径，故此处不给相对链接。

[18] C. Lauer, P. Pfeiffer, A. Rombach, N. Mehdiyev. *Assessing the Business Process Modeling Competences of Large Language Models*（BEF4LLM）. Information Systems, 142:102761, 2026. [DOI 10.1016/j.is.2026.102761](https://doi.org/10.1016/j.is.2026.102761) · [arXiv:2601.21787](https://arxiv.org/abs/2601.21787)。

[27] *A Formalism-Aware Reward Loop for Handwritten UML-to-PlantUML Generation*. MODELS 2026 NIER. [arXiv:2607.28987](https://arxiv.org/abs/2607.28987)。其 §4.3 归纳的 8 类（extraction / compilation / recognition / typing / structure / hallucination / omission / cosmetic fidelity）自陈为 "an organising scheme rather than a measurement instrument"，因此本文件只取其 `hallucination` 与 `omission` 并列这一点作为维度 B 的旁证。

**语义变异点（记录为空白，不作维度）**

[19] D. Harel. *Statecharts: A Visual Formalism for Complex Systems*. Science of Computer Programming, 8(3):231–274, 1987. [DOI 10.1016/0167-6423(87)90035-9](https://doi.org/10.1016/0167-6423%2887%2990035-9)。仅核书目。

[20] D. Harel, A. Naamad. *The STATEMATE Semantics of Statecharts*. ACM TOSEM, 5(4):293–333, 1996. [DOI 10.1145/235321.235322](https://doi.org/10.1145/235321.235322)。仅核书目。

[21] M. von der Beeck. *A Comparison of Statecharts Variants*. FTRTFT 1994, LNCS 863, pp. 128–148. [DOI 10.1007/3-540-58468-4_163](https://doi.org/10.1007/3-540-58468-4_163)。仅核书目，逐条比较维度未取。

[22] M. L. Crane, J. Dingel. *UML vs. Classical vs. Rhapsody Statecharts: Not All Models Are Created Equal*. SoSyM 6(4):415–435, 2007（会议版 MoDELS 2005, LNCS, pp. 97–112）。[DOI 10.1007/s10270-006-0042-8](https://doi.org/10.1007/s10270-006-0042-8) · [会议版 DOI 10.1007/11557432_8](https://doi.org/10.1007/11557432_8)。仅核书目。

[23] H. Fecher, J. Schönborn, M. Kyas, W.-P. de Roever. *29 New Unclarities in the Semantics of UML 2.0 State Machines*. ICFEM 2005, LNCS, pp. 52–65. [DOI 10.1007/11576280_5](https://doi.org/10.1007/11576280_5)。仅核书目。

**调研到但不收（见 §2.7）**

[24] C. F. J. Lange, M. R. V. Chaudron. *Effects of Defects in UML Models — An Experimental Investigation*. ICSE 2006, pp. 401–411. [DOI 10.1145/1134285.1134341](https://doi.org/10.1145/1134285.1134341)。**全文未取到**（ACM DL 返回 403）；其缺陷形态表未知，不得据标题推测。

[25] D. Torre, Y. Labiche, M. Genero, M. Elaasar. *A Systematic Identification of Consistency Rules for UML Diagrams*. Journal of Systems and Software, 144:121–142, 2018. [DOI 10.1016/j.jss.2018.06.029](https://doi.org/10.1016/j.jss.2018.06.029)。排除准则的逐字引文经本仓库先前核验。

[26] T. Dinh-Trong, S. Ghosh, R. France, B. Baudry, F. Fleurey. *A Taxonomy of Faults for UML Designs*. MoDeVa Workshop @ MODELS 2005. [作者页](https://softwarediversity.eu/wp-publications/dinhtrong05a/index.html)。**全文未取到**（PDF 链接失效），列为待补线索。

**形式化符合性关系**

[28] J. Tretmans. *Model Based Testing with Labelled Transition Systems*. In: Formal Methods and Testing, LNCS 4949, 2008. [PDF](https://repository.ubn.ru.nl/bitstream/handle/2066/35653/1/35653.pdf)。本文件只用其 underspecification 的口径，未通读全文。

**仓库内已核验材料**

[29] C. Lange, M. R. V. Chaudron, J. Muskens, L. J. Somers, H. M. Dortmans. *An Empirical Investigation in Quantifying Inconsistency and Incompleteness of UML Designs*, 2003。逐字引文与出处见本仓库 [历史来源档案](../../../related_work/provenance/archive/legacy_20260821/evidence_distribution.md) §3.3b（该处已完成原文核验）。

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13（第四轮，同日） | **维度 A 新增取值 `region`（正交区域），并撤销 §3.7 里「界外条目不得取为维度取值」那句旧规则。** 起因是把台账 99 条 + 候选 141 条共 240 个对象逐一映射到本座标系之后，映射不上的对象里**只有一处**是座标系本身给不出取值，且它由三批互不通气的判定者（读 `statement` / 读 `ref+gen+reason` / 读未匹配 issue）独立撞到同一处：**正交区域及其数量**。旧规则要求把这类赶出座标系，后果是它既进不了记录、也进不了统计，同一批材料在报表上呈现成「什么都没发生」——而 [CLAUDE.md](../../../../../CLAUDE.md) 的建模对象边界明写两条约束同时成立（不得记为「方法未能检出」，**也不得**声称这些模型没有并发问题）。故改为给它一个可记录、`counts_as_defect = false` 的槽位。**同时新增 §3.7.1**：任一轴取 `other` 必须附一句自然语言说明（说清它是什么，或说清它涉及多个取值、单值装不下），该判据只看字段值即可唯一判定，故允许做成校验器 `E` 级门。**未改**：时钟与不变式两族仍无取值（PlantUML 状态图里没有对应语法载体，判定测试立不住），仍走自由描述。 |
| 2026-08-13（第三轮，同日） | **由三维扁平类型学改建为条件式座标系**，起因是初稿只覆盖「能定位到单个元素」的缺陷——那是 A/B 两轴出身于测试领域（缺陷即一次语法编辑）的结构性局限。新增**维度 0 `defect_locus`**（element / pair / global / other）作为先行轴，它决定后面问哪些轴；新增**维度 D `defect_logic_kind`**（9 值）承担逻辑层；新增**可选维度 E**（Dwyer pattern × scope）承担「修好算什么」。新增 §2.6 逻辑层文献（Heimdahl & Leveson 的两条机械判据 · Dwyer 模式库 · Baier & Katoen · UML 层次语义三条），新增 §3.8 对六类逻辑层缺陷的**逐条验收表**。**两处实质更正**：① `deadlock` 更名 `unintended_terminal` —— Baier & Katoen 的 deadlock 要求「至少一个分量仍可继续」，是并发概念，在无正交区的 $M$ 里不成立，正确的锚点是 Definition 2.4 terminal state，且判定必须把祖先群迁移算进去；② 「活锁」无与标注无关的形式定义（全书 grep 确认），`nontermination` 只能靠 NL 的终止义务立起来。**逐字核对由我本人完成的**：Heimdahl & Leveson p. 370（读图）· Dwyer 官方模式库四页 · Baier & Katoen 三处定义并 grep 全书 · UML 2.5.1 §14.2.3.9.4 / §14.2.3.4.5 / §14.2.3.4.6 / §14.2.3.9.1（自行下载 18 MB 官方 PDF 抽取）。**协作核验者取得而我未独立复核的**已在 §5 逐条标注（[42][43][44][45] 与 Harel Appendix C 保留）。 |
| 2026-08-13（第二轮，同日） | 迟到的三路文献核验带来四处实质更正与一处重要补全。**补全**：Fabbri statechart 变异算子表已从同组技术报告 ND-41 取到并读图核对（35 条），其 FSM 组的「构件 × faltando/extra/trocado」结构独立印证了维度 A × B 的叉积设计；同时确认**全表无状态级算子**、变量只有「换」无「缺」。**更正一**：model smell 传统不得整支排除——UML 状态机异味恰好有 5 条判据清晰的成文条目（Arendt 2009 §3.4 + SDMetrics），已收进 §2.3，并附「两份证人同谱系、非独立」的告诫。**更正二**：五类检查阅读分类的出处是 Travassos 等 1999，不是 Basili & Weiss 1984。**更正三**：§4.5 补入反例——Travassos 1999 正是以需求文档为参照物且覆盖状态图的成文分类，故「模型-需求参照物缺席」只对规则目录 / 变异算子 / 质量度量三支成立，不对整个领域成立。**更正四**：「语义变异点」作为成文条款类型只存在到 UML 2.4.1，2.5.1 已不挂该标签。 |
| 2026-08-13 | 建立。从六支外部文献流派导出三维 14 值的可枚举缺陷类型学；每个取值配正式定义（逐字 + 出处）、可操作判定测试与相邻取值分界；记录八条分歧与空白，其中 `variable` 维、语用维、模型-需求参照物三处为已知的文献真空。同轮补核推翻了初稿对 Fujiwara 1991 的描述（它只有两类故障，多余状态是前提不是故障类），并据此新增 §4.0：「经典 FSM 故障模型四元组」是两篇论文的合并口径，任何一篇都引不出来。Chow 1978（含 p. 591 读图核对的 Fujiwara 引文）、El-Fakih 等 2016、Jia & Harman 2011、Lackner & Schmidt 2015、Reijers 技术报告、itemis CREATE 校验器源码为全文/源码取到并逐字引用；其余条目的取证档位逐条标注在 §5。 |
