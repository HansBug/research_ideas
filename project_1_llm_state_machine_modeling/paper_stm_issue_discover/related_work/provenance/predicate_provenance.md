# 当前 12 条谓词的来源、执行与发表边界

本文记录 `four-family-12-core.v1` 的 12 条谓词，族内编号为 `S1–S5 / G1–G3 / R1–R3 / V1`。我们依据相关文献与标准，面向工作流的证据需求选择这些谓词，用于类型化绑定、执行适用检查和生成可追溯回执。选择范围由工作流的证据需求界定，不主张完备缺陷分类或最优子集。

本文件维护完整书目、一手引文定位、用途和执行边界；结构化对应关系见 [current_source_catalog.json](./current_source_catalog.json)。来源检索截止日仍为 2026-09-02，本次版本与编号整理日期为 2026-09-05。完整前版审计、旧编号及其历史结果说明见 [pre-P1 归档](./archive/pre_p1_20260905/README.md)。

## 用途与来源

| ID | 可执行证据形式 | source IDs |
| --- | --- | --- |
| S1 | 元素存在 | ST1、ST2、ST4 |
| S2 | 迁移存在 | ST1、ST2、ST4 |
| S3 | 触发集精确相等 | ST1、ST2、ST5 |
| S4 | 生命周期动作挂接 | ST1、ST3、ST7 |
| S5 | 守卫精确相等 | ST1、ST2、ST3 |
| G1 | 有限路径存在 | TP1、TP2、ST3 |
| G2 | 声明边界内必达 | TP2、TP3、TP4 |
| G3 | 根可达节点到标记节点的共可达性 | TP6、G3-RP1、G3-RP2 |
| R1 | 声明宏步内事件被消费 | TR1、TR2、ST8 |
| R2 | 刺激后的目标状态激活 | TR1、TR2、ST3 |
| R3 | 闭区间内状态保持 | TP1、TR4、TR5、TR6 |
| V1 | 有界死锁／进展探测 | TP4、BV8、BV7、BV9 |

## 三类责任与 W2

外部文献与标准说明检查义务的学术依据；方法规范、代码和测试说明 FCSTM 的 token、AST、宏步、图投影、冷启动、horizon 与回放语义；当前自然语言描述和源制品的精确绑定说明实例中的名称、scope、界限与期望值。三类证据各自承担对应责任。

W2 要求受支持片段、精确实例绑定、完整身份链、可核验的描述／来源／绑定引用，以及终止 Boolean receipt。极性资格限定可写的最强命题，不能把有界查询或叶状态探测扩写为无界全称定理。完成的合格执行不替代人工 D/A、有效性、对应关系或 K/N/I 裁定；`unknown` 与未完成求值不能形成 W2。版本化执行依据见 `method/src/paper_stm_method/compiler/soundness.py`、四族 backend 和方法测试。

## 书目与逐字引文

[^uml251]: Object Management Group. *Unified Modeling Language (UML), Version 2.5.1*. 2017, §14.5.11.8, p. 362; §14.5.8.6, p. 354. https://www.omg.org/spec/UML/2.5.1/PDF (accessed 2026-09-02). “The source and target Vertices of a Transition must be contained in the same StateMachine as the Transition.”
[^heimdahl1996]: Mats P. E. Heimdahl and Nancy G. Leveson. “Completeness and Consistency in Hierarchical State-Based Requirements.” *IEEE TSE*, 22(6), 1996. https://doi.org/10.1109/32.508311. The recovered author PDF, p. 4: “The logical OR of the conditions on every transition out of any state must form a tautology.”
[^dwyer1999]: Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. “Patterns in Property Specifications for Finite-State Verification.” *Proceedings of ICSE 1999*, pp. 411--420. https://doi.org/10.1145/302405.302672. p. 413 defines a between scope as “any part of the execution from one given state/event to another”; p. 414 defines Absence as “A given state/event does not occur within a scope.”
[^mohajerani2016]: Sahar Mohajerani, Robi Malik, and Martin Fabian. “A Framework for Compositional Nonblocking Verification of Extended Finite-State Machines.” *Discrete Event Dynamic Systems*, 26(1), 2016, pp. 33--84. https://doi.org/10.1007/s10626-015-0217-y. The definition requires every reachable state to reach a marked state.
[^andrec2023]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification – A Survey.” *ACM Computing Surveys*, 55(13s), 2023, pp. 1--47. https://doi.org/10.1145/3579821.
[^biere2006]: Armin Biere, Keijo Heljanko, Tommi Junttila, Timo Latvala, and Viktor Schuppan. “Linear Encodings of Bounded LTL Model Checking.” *Logical Methods in Computer Science*, 2(5), 2006. https://doi.org/10.2168/LMCS-2(5:5)2006.
[^uppaal]: UPPAAL. “Symbolic Query Semantics.” Documentation, accessed 2026-09-02. https://docs.uppaal.org/language-reference/query-semantics/symb_queries/.
[^fabian1998]: Martin Fabian. *On Object Oriented Nondeterministic Supervisory Control*. PhD thesis, Chalmers University of Technology, 1998, pp. 28, 40, 91. https://research.chalmers.se/publication/1126/file/1126_Fulltext.pdf (accessed 2026-09-02).

## 一手全文引文定位表

本表是逐条审计引用的唯一 quote register。每个锚点保留原文、版本与页码/章节；“支撑范围”只说明它可以承担的外部领域或形式命题，实例的具体名称、域、界和 scope 仍须由 `Source-bound instance authority` 合同承担，不能由下列文字反推。

<a id="quote-uml-transition"></a>
**Q-UML-transition。** UML 2.5.1 §14.5.11.1, printed p. 359: “A Transition represents an arc between exactly one source Vertex and exactly one Target vertex.” §14.5.11.6, printed p. 360: “Designates the originating Vertex (State or Pseudostate) of the Transition” and “Designates the target Vertex that is reached when the Transition is taken.” 支撑 S1/S2 的元模型位置与端点角色，不规定任意业务迁移必须存在。[^uml251]

<a id="quote-uml-trigger"></a>
**Q-UML-trigger。** UML 2.5.1 §13.3.3.1, printed p. 291: “A Trigger specifies a specific point in the definition of a Behavior at which an Event occurrence may have such an effect.” §14.5.11.6, printed p. 360: “trigger : Trigger [0..*]”. 支撑 S3 的 trigger 位置，不定义 FCSTM token-set equality。[^uml251]

<a id="quote-uml-lifecycle"></a>
**Q-UML-lifecycle。** UML 2.5.1 §14.2.3.4.3, printed p. 308: “A State may have an associated entry Behavior”; “a State may also have an associated exit Behavior”; and “A State may also have an associated doActivity Behavior.” 支撑 S4 的 lifecycle 行为位置，不把 optional slot 改写为无条件业务义务。[^uml251]

<a id="quote-uml-guard-effect"></a>
**Q-UML-guard-effect。** UML 2.5.1 §14.5.11.6, printed p. 360: “effect : Behavior [0..1] ... Specifies an optional behavior to be performed when the Transition fires.” 同节还规定：“A guard is a Constraint that provides a fine-grained control over the firing of the Transition.” 支撑 S5 的 guard carrier 角色；guard 的所需值来自 NL binding。[^uml251]

<a id="quote-uml-run-to-completion"></a>
**Q-UML-run-to-completion。** UML 2.5.1 §14.2.3.9.1, printed p. 316: “Event occurrences are detected, dispatched, and processed by the StateMachine execution, one at a time.” 同节还规定：“When all orthogonal Regions have finished executing the Transition, the current Event occurrence is fully consumed.” 支撑 R1 的 event-processing obligation；本文的 `macrostep`、scheduler 和 consumer API 另由方法规范定义。[^uml251]

<a id="quote-uml-active-configuration"></a>
**Q-UML-active-configuration。** UML 2.5.1 §14.2.3.4.2, printed p. 308: “A State is said to be active if it is part of the active state configuration.” 同节规定稳定 configuration 没有 further enabled transitions，且已完成 entry behaviors。支撑 R2/R3/V1 的 configuration-level 术语，不替本文的 cold trace 或有限 horizon 背书。[^uml251]

<a id="quote-dwyer-existence-response"></a>
**Q-Dwyer-existence-response。** Dwyer, Avrunin and Corbett, ICSE 1999, p. 412: “A given state/event occurs within a scope” (Existence); p. 413: “A response property says that when S occurs then an occurrence of P must follow.” 支撑 G1、R2 的性质形状，不能把其无界模式自动改成当前的有限 step bound。[^dwyer1999]

<a id="quote-dwyer-absence-universality"></a>
**Q-Dwyer-absence-universality。** Dwyer, Avrunin and Corbett, ICSE 1999, pp. 413--414: a between scope is “any part of the execution from one given state/event to another”, and Absence is “A given state/event does not occur within a scope.” 该全文的 Universality pattern定义为 “A given state/event occurs throughout a scope.” 支撑 R3 在声明区间内的保持形状，而非当前后端的完整性。[^dwyer1999]

<a id="quote-fabian-coaccessibility"></a>
**Q-Fabian-coaccessibility。** Fabian, 1998, p. 40: “when some marked state is reachable from any state it is said to be coaccessible.” p. 91 adds that “every string of L(P) can be continued to reach a marked state” for nonblocking language. 支撑 G3 的 coaccessibility/nonblocking 形式形状，不将其替换为 all-path termination。[^fabian1998]

<a id="quote-biere-completeness"></a>
**Q-Biere-completeness。** Biere et al., LMCS 2006, p. 43: “Section 7 shows how BMC can be made complete. Specifically we show how our encodings can be extended with a termination check to achieve completeness.” 支撑 G2 对 bounded result 的完整性限制：没有相应 completion/lasso 论证时，有限检查不能承担无界证明。[^biere2006]

<a id="quote-uppaal-state-space"></a>
**Q-UPPAAL-state-space。** UPPAAL symbolic query semantics defines `A[] p` as “p holds in all reachable states”, `A<> p` as “p eventually holds in all paths”, and `p --> q` as `A[] (p imply A<> q)`; it defines `deadlock` as a state where no transition can be taken. 支撑 G2 的全路径量化术语与 V1 的 deadlock 边界，不替代 FCSTM runtime semantics。[^uppaal]

## 逐条审计

各条分别说明检查义务的形式形状、方法执行语义和实例授权；实际可执行范围以各条的“执行、极性与发表”为准，状态字段沿用结构化来源目录。

### S1 `element_exists`

**一手全文定位。** [Q-UML-transition](#quote-uml-transition)；它只定位可声明元素与 transition endpoint 的元模型角色。

**检查义务。** “A named element of the specified kind belongs to the closed declaration inventory.” NL 明示 state/event/variable/action/effect 时才产生存在义务；外部 UML 文本只为已使用的 state-machine carrier 提供元模型位置，不声称用一条 transition 引文覆盖所有类别。`ST1,ST2,ST4`。[^uml251]

**义务与出处。** S1 依据 UML 的元素及迁移端点角色，检查描述所要求的具名元素是否存在。`ST1,ST2,ST4` 对应这些元模型与控制模型来源；一手引文见 [Q-UML-transition](#quote-uml-transition)。所需元素的种类、名称与范围由当前描述和源制品绑定给出。

**方法、实例与 W2。** registry 的 kind-parametric inventory 是义务层；native source-static backend 仅执行 `state`、`event`、`transition`/`edge` 的 `closed_fcstm` membership。variable、action、effect、composite 或 owner-local scope 不在 S1 的可执行片段，必须保持 W1/W0 或由其他谓词处理。实例的 kind、名称和 scope 仍须来自精确 NL/source binding。W2 还要求合法 typed inputs、终止 Boolean receipt 和 hash-bound replay，缺任一项不把运行结论升格为论文主张。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，仅 `scope=closed_fcstm` 的 state/event/transition/edge membership。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。该 fragment 的 `true`、`false`均 `W2/ELIGIBLE`；`unknown`、`failure`均 `W1/INELIGIBLE`。

### S2 `transition_exists`

**一手全文定位。** [Q-UML-transition](#quote-uml-transition)。

**检查义务。** “A transition exists between the specified source and target.” source--target requirement 由 NL 授权，Transition endpoint 由 UML §14.5.11.8 支撑。`ST1,ST2,ST4`。[^uml251]

**义务与出处。** S2 依据 UML 的 source/target endpoint 定义检查一条要求存在的迁移。`ST1,ST2,ST4` 的外部形式依据见 [Q-UML-transition](#quote-uml-transition) 和 [^uml251] §14.5.11.8, p. 362。入口 target identity 可由该检查表达；initial 唯一性和无 trigger/guard 的良构性不属于它。

**方法、实例与 W2。** exact owner-local state path、initial pseudostate 和 source--target carrier 的解释是 method-owned；某一 endpoint pair 是否应存在必须由 pair 的 NL/source binding 授权。W2 要求这类绑定、native identity、完整 receipt 和 replay 同时成立。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，仅 exact native state paths 和 `closed_fcstm`/exact owner scope。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。该 fragment 的 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 enabledness、trigger、effect 或跨层级模糊引用。

### S3 `trigger_set_equals`

**一手全文定位。** [Q-UML-trigger](#quote-uml-trigger)。

**检查义务。** “The parsed trigger set of a transition equals the required trigger set.” trigger 属于 transition；未触发迁移是可能的 requirements 缺口。`ST1,ST2,ST5`。[^uml251][^heimdahl1996]

**义务与出处。** `ST1,ST2,ST5` 提供 UML trigger 槽位与层次状态需求一致性资料。逐字引文见 [Q-UML-trigger](#quote-uml-trigger) 和 [^heimdahl1996]。它们说明 transition/condition 的语义位置与一致性检查动机；期望触发集来自当前描述，token-set equality 由方法定义。

**方法、实例与 W2。** FCSTM tokenization、无序集合和 AST/canonical equality 是 method-owned，不能冒充 external semantic definition；transition carrier 与 required trigger list 则由 source/NL binding 授权。W2 要求 exact carrier、合法 list、terminal receipt 和 replay；没有 carrier 时保留 W1/W0，不从 parser 能力反推义务。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，精确 carrier 的无序 parsed token set。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。token equality 不推出 event path identity 或消费。

### S4 `state_action_attached`

**一手全文定位。** [Q-UML-lifecycle](#quote-uml-lifecycle)。

**检查义务。** “The specified action is attached to the specified lifecycle phase of the specified state.” lifecycle slots 和控制恢复动作支撑静态 requirement-relative 检查。`ST1,ST3,ST7`。[^uml251]

**义务与出处。** `ST1,ST3,ST7` 提供 UML lifecycle 槽位与控制恢复动作的背景，一手引文见 [Q-UML-lifecycle](#quote-uml-lifecycle)。S4 检查静态挂接；optional slot 是否应存在由描述授权，静态挂接不能证明动作实际执行。

**方法、实例与 W2。** `entry|do|exit` 的 closed enumeration、action representation 和 source carrier 是方法语义；state、phase、action 的 expected value 是实例绑定。W2 必须同时有 exact state、phase/action binding、合法 typed plan、terminal receipt 和 replay；它不会把静态挂接误写成动作已实际执行。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，exact state 与 `entry|do|exit`。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。静态挂接不推出动作实际发生。

### S5 `transition_guard_equals`

**一手全文定位。** [Q-UML-guard-effect](#quote-uml-guard-effect)。

**检查义务。** “The parsed guard of a transition equals the required guard.” external source 只定位 guard 的 transition role；NL 才建立 equality obligation。`ST1,ST2,ST3`。[^uml251]

**义务与出处。** `ST1,ST2,ST3` 定位 guard 的迁移角色，一手引文见 [Q-UML-guard-effect](#quote-uml-guard-effect)。S5 的期望守卫来自当前描述；UML 的 optional guard 槽位不自动建立该等式义务。

**方法、实例与 W2。** FCSTM guard AST 的 structural equality、空 guard 的表示和 parser failure 由方法规格定义；目标 transition 与 required guard 由 source/NL binding 定义。W2 仅适用于 exact carrier 与 AST fragment 的 complete receipt/replay；逻辑等价、SAT 和业务等价排除在外。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，exact carrier 的 FCSTM guard AST structural equality。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出逻辑 SAT、等价或业务等价。

### G1 `may_reach`

**一手全文定位。** [Q-Dwyer-existence-response](#quote-dwyer-existence-response)。

**检查义务。** “A finite graph path exists from the source set to the target set.” 有限可达性是经典 verification property。`TP1,TP2,ST3`。[^dwyer1999]

**义务与出处。** `TP1,TP2,ST3` 提供性质模式和控制模型中的可达性依据。Dwyer 等的 Existence 定义见 [Q-Dwyer-existence-response](#quote-dwyer-existence-response)。本方法将其操作化为有限图路径检查；起点和目标仍须由实例绑定给出。

**方法、实例与 W2。** leaf graph、source/target set normalization 与图搜索是 method-owned；两个 endpoint set 是否必须存在来自 NL/source binding。W2 要求 closed native graph、exact binding、terminal receipt 和 replay；守卫、数据、优先级和 scheduler 不在这一图 fragment 内。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，closed native leaf graph。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 guard/data/priority/scheduling 下可执行。

### G2 `must_reach`

**一手全文定位。** [Q-UPPAAL-state-space](#quote-uppaal-state-space) 的 `A<>` 全路径 eventuality 与 [Q-Biere-completeness](#quote-biere-completeness) 的 bounded-completeness 边界。

**检查义务。** “Under the declared graph completion, every path from the source eventually visits the target.” universal eventuality 不等于 G1 reachability。`TP2,TP3,TP4`。[^dwyer1999]

**义务与出处。** `TP2,TP3,TP4` 对应路径和必达性质。UPPAAL 的 `A<> p` 定义见 [Q-UPPAAL-state-space](#quote-uppaal-state-space)，支撑全路径 eventuality；Biere 等见 [Q-Biere-completeness](#quote-biere-completeness)，说明有界编码的完整性条件。外部来源不为当前实例设置 horizon。

**方法、实例与 W2。** `H=declared-state count`、`.fbmcq` query 和 receipt decoding 是方法语义；起点、目标和 graph completion 是实例 binding。完成的 Boolean 执行在受支持的有界片段上可形成 W2；没有 lasso/completeness 论证只限制其可写成的语义范围，不能把该执行改写为 W1，也不能将其表述为 registry 的无界全称命题。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`。backend 检查 `must_reach <= H`，`H=declared-state count`，没有 lasso 或 completeness 论证。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。在绑定、身份链和终止回执闭合时，`true`、`false`均为 `W2/ELIGIBLE`，其 claim scope 是声明界限内的 G2 查询结果；`unknown`、`failure`为非 W2。不得扩写成无界全路径最终可达性证明。

### G3 `coaccessible_to`

**一手全文定位。** [Q-Fabian-coaccessibility](#quote-fabian-coaccessibility)。

**检查义务。** “Every root-reachable node can reach a marked node along a finite path.” nonblocking/coaccessibility 不同于 termination。`TP6,G3-RP1,G3-RP2`。[^mohajerani2016]

**义务与出处。** `TP6,G3-RP1,G3-RP2` 对应共可达与非阻塞来源。Fabian 的逐字定义见 [Q-Fabian-coaccessibility](#quote-fabian-coaccessibility)；Mohajerani 等的定义要求每个可达状态能到达标记状态 [^mohajerani2016]。标记集合由当前描述和源制品绑定选择，共可达性不等于全路径终止。

**方法、实例与 W2。** root/marked set、native topology projection 与 finite-path executor 是方法语义；roots 和 marked states 来自 source/NL binding。W2 仅在完整 native topology fragment、终止 Boolean receipt 和 replay 内可用；不推出 all-path termination、公平性或 concurrent configuration-space。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，仅 native topology projection。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 all-path termination、公平性或并发 configuration-space。

### R1 `event_consumed`

**一手全文定位。** [Q-UML-run-to-completion](#quote-uml-run-to-completion)。

**检查义务。** “The exact event occurs and is consumed in the declared macrostep.” 未触发迁移的事件是 requirements consistency concern。`TR1,TR2,ST8`。[^heimdahl1996]

**义务与出处。** `TR1,TR2,ST8` 对应控制场景、事件处理与轨迹技术资料。UML 的逐字事件处理和消费语义见 [Q-UML-run-to-completion](#quote-uml-run-to-completion)。它支撑事件消费检查；本项目的 `macrostep` 和消费 API 由方法定义。

**方法、实例与 W2。** `macrostep`、cold schedule、consumer identification 和 `called()` 是方法自有语义；event、schedule、step 和期望消费由精确 NL/source binding 授权。W2 需 native trace、terminal Boolean receipt 和 hash-bound replay；它不推广为所有 event 或 scheduler 的结论。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，一个 closed cold schedule。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。`macrostep` 与 consumer 是方法语义，不推出所有事件或调度。

### R2 `state_reached_after`

**一手全文定位。** [Q-UML-active-configuration](#quote-uml-active-configuration) 与 [Q-Dwyer-existence-response](#quote-dwyer-existence-response)。

**检查义务。** “The target state is active in the trailing portion of the declared trace window.” 控制刺激后的 occupancy 是轨迹 requirement 形状。`TR1,TR2,ST3`。[^dwyer1999]

**义务与出处。** `TR1,TR2,ST3` 对应刺激与轨迹来源。UML 的 active configuration 定义和 Dwyer 的 Existence/Response 形状见上述一手引文。目标状态、刺激和观察窗口由当前实例绑定给出。

**方法、实例与 W2。** cold scenario、trailing window 和 active-state observation 是方法语义；stimulus、state 和 window 是 NL/source authority。W2 需要 exact trace, complete terminal receipt 和 replay；不能从单一 schedule 推出因果、所有调度或全局可达性。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，固定 cold scenario/trailing window。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出因果或所有调度可达。

### R3 `state_retained`

**一手全文定位。** [Q-UML-active-configuration](#quote-uml-active-configuration) 与 [Q-Dwyer-absence-universality](#quote-dwyer-absence-universality)。

**检查义务。** “The target state remains active at every recorded point in the closed interval.” 这是有限 trace 内保持，而非无限 persistence。`TP1,TR4,TR5,TR6`。[^dwyer1999]

**义务与出处。** `TP1` 提供 Universality 的形式依据，逐字引文见 [Q-Dwyer-absence-universality](#quote-dwyer-absence-universality)；`TR4,TR5,TR6` 对应轨迹和反例证据的技术形态。检查范围是实例指定的闭区间，不由文献推导时长。

**方法、实例与 W2。** recorded points、closed interval 和 SimulationRuntime trace 是方法语义；state/interval 是精确 NL/source binding。W2 需要完整 trace、terminal receipt 和 replay，任何 unknown/failure 仅保留 W1；不推出连续时间、open until 或 global invariant。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，closed interval 的 recorded points。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出连续时间、开放 until 或全局 invariant。

### V1 `deadlock_free`

**一手全文定位。** [Q-UML-active-configuration](#quote-uml-active-configuration) 与 [Q-UPPAAL-state-space](#quote-uppaal-state-space)。

**检查义务。** “Every reachable, stable, nonterminal configuration admits model progress.” deadlock freedom 与 termination不同。`TP4,BV8,BV7,BV9`。[^andrec2023]

**义务与出处。** `TP4` 提供可达配置量化的形式依据，UPPAAL 的 `deadlock` 定义见 [Q-UPPAAL-state-space](#quote-uppaal-state-space)；`BV8,BV7,BV9` 对应状态空间、死锁检查与 TLA+ 的技术术语和边界。André 等提供 UML 执行与验证转换的背景 [^andrec2023]。这些来源支持检查义务，当前叶状态探测的执行范围由方法另行定义。

**方法、实例与 W2。** topology-reachable leaves、hot start、one-step probe、state-preserving effects 与 valuation coverage 的实现差异由 method audit 定义；initial scope 必须来自 source/NL binding。既有 probe 的完成 Boolean 执行可在其声明的叶状态探测片段上形成 W2；它没有枚举所有可达稳定配置，因此不能作为全局无死锁结论。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`。backend 在 topology-reachable stable leaves 做 one-step probe，未枚举 all reachable configurations，且 hot start、state-preserving effect 与 valuation 覆盖有明确边界。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。在绑定、身份链和终止回执闭合时，`true`、`false`均为 `W2/ELIGIBLE`，其 claim scope 限于该叶状态探测；`unknown`、`failure`为非 W2。不得扩写为全局无死锁证明。
