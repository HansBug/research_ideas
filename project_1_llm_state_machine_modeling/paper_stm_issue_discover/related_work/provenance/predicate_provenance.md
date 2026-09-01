# 当前 19 条谓词的来源、执行与发表审计

这是 `four-family-19-core.v1` 的唯一人读审计入口。它不修改冻结 registry、54 个 PlantUML pair、145 条台账、人工裁定或 v60/current 结果。`current_source_catalog.json` 只保存 source-ID mapping 和本审计的结构化状态；完整书目、逐字引文、crosswalk、论证和论文边界均以本文件为准。检索截止日为 2026-09-02。历史的 313/310/454/361 是来源库存或筛选规模，不是谓词 prevalence 分母。

## 三类责任与 W2

每条谓词的**学术资格**说明 requirement-relative 检查为何在控制系统、状态机或形式方法中成立；**方法执行语义**说明 FCSTM token、AST、`macrostep`、`called()`、冷启动、horizon 和 replay；**实例授权**说明具体 trigger、guard、domain、scope、bound 或 expected value 由哪句 NL/source artifact 绑定。三类证据互不替代。外部论文不定义本项目 API；代码和方法说明也不为业务义务背书。

`W2` 还必须有精确 binding、受支持 fragment、终止 Boolean receipt 和 hash-bound replay。`true` 表示通过该 fragment，`false` 是该 fragment 内的反例；均不替代人工 D/A、有效性、relation 或 K/N/I。`unknown`、`failure` 一律不可作为机械证实。方法语义的版本化依据是 `pipeline/evidence_discovery/METHOD_PRINCIPLES.md` §§2--3、`method/src/paper_stm_method/compiler/soundness.py`、`backends/{topology,bounded_verification}.py` 与 `method/tests/test_provider_free_fixture.py`。

## 双向 legacy/current crosswalk

| legacy ID | current ID(s) | relation | 命题承接与边界 | source-unit IDs 与 commit/path evidence |
| --- | --- | --- | --- | --- |
| `event_declared`、`variable_declared`、`state_declared` | S1 | `merge_derived` | 三条具名元素义务合为 kind-parametric closed inventory；当前不处理未绑定业务元素。 | `ST1,ST2,ST4`; `3e4e003e1` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `edge_declared` | S2 | `direct_reuse` | 承接精确 transition source--target 存在。 | `ST1,ST2,ST4`; `3e4e003e1` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `initial_target` | S2 | `split` | 只承接入口 target identity；initial 唯一性和迁移形状不被 S2 假装执行。 | `ST1,ST2,ST4`; `d1b4d71c7` 与 `related_work/provenance/current_source_catalog.json`。 |
| -- | S3 | `newly_added` | 旧 19 没有精确 trigger-set equality；当前从已映射的 UML trigger source pool 新增该 requirement-relative 比较。 | `ST1,ST2,ST5`; `d1b4d71c7` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `action_declared` | S4、R3 | `split` | 当前把静态 lifecycle slot 固定为 S4，把 trace 内行为发生固定为 R3。 | `ST1,ST3,ST7,ST8,TR1,TR2`; `3e4e003e1` 与 `pipeline/archive/witness_search_prototype_legacy_20260821/TYPED_OBLIGATION_PROVENANCE.md`。 |
| `effect_declared` | S6 | `direct_reuse` | 承接 transition effect member。 | `ST1,ST2,ST9`; `3e4e003e1` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `guard_distinguishable` | S5、V1、V2 | `split` | AST equality、有限域互斥和有限域覆盖分开；UML 不把互斥列为默认义务。 | `ST1,ST2,ST3,BV4,BV5,BV6`; `d1b4d71c7` 与 `related_work/provenance/current_source_catalog.json`。 |
| `reaches` | G1、G2 | `split` | existential finite path 与 universal eventuality 不可互推。 | `TP1,TP2,TP3,TP4`; `3e4e003e1` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| -- | G3 | `newly_added` | 旧 19 没有 source--target avoidance 命题；当前将来源池中的路径约束单独固定为 node-only 可执行片段。 | `TP3,TP3B,TP3C`; `d1b4d71c7` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `terminates` | G2、G4、V4 | `split` | 旧 termination 混合必达、coaccessibility 和 progress；当前显式分开。 | `TP2,TP3,TP4,TP6,G4-RP1,G4-RP2,BV7,BV8,BV9`; `056997691` 与 `method/src/paper_stm_method/compiler/soundness.py`。 |
| `event_consumed` | R1 | `direct_reuse` | 事件响应义务承接；`macrostep` 是方法语义。 | `TR1,TR2,ST8`; `3e4e003e1` 与 `pipeline/evidence_discovery/METHOD_PRINCIPLES.md`。 |
| `occupancy_after` | R2 | `direct_reuse` | 当前承接刺激后目标 active 的轨迹义务。 | `TR1,TR2,ST3`; `3e4e003e1` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `stays_in` | R4 | `direct_reuse` | 当前承接有限 interval 的 active 保持。 | `TP1,TR4,TR5,TR6`; `3e4e003e1` 与 `method/src/paper_stm_method/resources/predicate_registry.json`。 |
| `persists_until`、`invariant` | V5 | `merge_derived` | 承接 occupancy safety 核心；当前 true 只表示有限通过。 | `TP3,TP3B,TP3C`; `056997691` 与 `method/src/paper_stm_method/compiler/soundness.py`。 |
| `response_within` | V3 | `direct_reuse` | 承接有界响应；不把无界 response 文献转成步数界。 | `TP1,BV7,TR1`; `d1b4d71c7` 与 `method/src/paper_stm_method/compiler/soundness.py`。 |
| `containment` | -- | `retired` | 父状态“正确性”需要外部需求参照；UML containment 规则不能导出它。 | `ST1`; `d1b4d71c7` 与 `related_work/provenance/archive/legacy_20260821/predicate_provenance.md`。 |
| `cardinality` | -- | `not_carried` | NL 指定任意 N 与 UML 固定 multiplicity 不同。 | `ST1`; `d1b4d71c7` 与 `related_work/provenance/archive/legacy_20260821/predicate_provenance.md`。 |
| `variable_delta_after` | -- | `not_carried` | 后值义务未进入冻结四族最小 surface。 | `TR1,TR2`; `d1b4d71c7` 与 `related_work/provenance/archive/legacy_20260821/predicate_provenance.md`。 |

上表覆盖 legacy 的 19 个唯一 key，current keyset 精确为 `S1--S6,G1--G4,R1--R4,V1--V5`。来源池重映射见 `3e4e003e1`，四族注册冻结见 `d1b4d71c7`，native execution 统一见 `056997691`，历史裁定见 `692783fe1`/`08a034ba8`。旧路线没有证据证明设计者从未接触 54-pair 台账，故本文只使用 **literature-informed, retrospectively consolidated evidence layer**，不用 preregistered 或 evaluation-independent taxonomy。

## 书目与逐字引文

[^uml251]: Object Management Group. *Unified Modeling Language (UML), Version 2.5.1*. 2017, §14.5.11.8, p. 362; §14.5.8.6, p. 354. https://www.omg.org/spec/UML/2.5.1/PDF (accessed 2026-09-02). “The source and target Vertices of a Transition must be contained in the same StateMachine as the Transition.”
[^heimdahl1996]: Mats P. E. Heimdahl and Nancy G. Leveson. “Completeness and Consistency in Hierarchical State-Based Requirements.” *IEEE TSE*, 22(6), 1996. https://doi.org/10.1109/32.508311. The recovered author PDF, p. 4: “The logical OR of the conditions on every transition out of any state must form a tautology.”
[^heitmeyer1996]: Constance Heitmeyer, Robert Jeffords, and Bruce Labaw. “Automated Consistency Checking of Requirements Specifications.” *ACM TOSEM*, 5(3), 1996, pp. 231--261. https://doi.org/10.1145/234426.234431. The recovered NRL version, p. 18, reports the A-7E disjointness analysis and cautions that “a few probably are not” errors.
[^sims2001]: Steve Sims, Rance Cleaveland, Ken Butts, and Scott Ranville. “Automated Validation of Software Models.” *ASE 2001*. https://doi.org/10.1109/ASE.2001.989794. p. 4: in the overlapping-condition example the successor “could be either B or C”; pp. 7--8 report Ford powertrain checks.
[^dwyer1999]: Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. “Patterns in Property Specifications for Finite-State Verification.” *Proceedings of ICSE 1999*, pp. 411--420. https://doi.org/10.1145/302405.302672. p. 413 defines a between scope as “any part of the execution from one given state/event to another”; p. 414 defines Absence as “A given state/event does not occur within a scope.”
[^mirabadi2009]: Ahmad Mirabadi and Mohammad B. Yazdi. “Automatic Generation and Verification of Railway Interlocking Control Tables Using FSM and NuSMV.” *Transport Problems*, 4(1), 2009, pp. 103--110. http://transportproblems.polsl.pl/pl/Archiwum/2009/zeszyt1/2009t4z1_11.pdf (accessed 2026-09-02). p. 2: “the route should be isolated from all potential conflicting movements”; p. 6: “no two conflicting routes can be set at the same time.”
[^mohajerani2016]: Sahar Mohajerani, Robi Malik, and Martin Fabian. “A Framework for Compositional Nonblocking Verification of Extended Finite-State Machines.” *Discrete Event Dynamic Systems*, 26(1), 2016, pp. 33--84. https://doi.org/10.1007/s10626-015-0217-y. The definition requires every reachable state to reach a marked state.
[^andrec2023]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification – A Survey.” *ACM Computing Surveys*, 55(13s), 2023, pp. 1--47. https://doi.org/10.1145/3579821.

## 逐条审计

每条的“状态”均按 `academic_qualification_status; method_semantics_status; instance_authority_status` 列出；证据 refs 分别见 source IDs、上述书目和方法路径。所有状态的 rationale 是：外部 source 只承担该条的领域/形式义务，方法路径只承担执行语义，typed binding/receipt 只承担当前实例。

### S1 `element_exists`

**现行精确命题。** “A named element of the specified kind belongs to the closed declaration inventory.” NL 明示 state/event/variable/action/effect 时才产生存在义务；UML 元模型给出 element/reference 位置。[`ST1,ST2,ST4`; ^uml251]

**义务与出处。** legacy 的 `event_declared`、`variable_declared`、`state_declared` 在 S1 合并为 kind-parametric inventory；没有把未绑定的业务元素纳入。`ST1,ST2,ST4` 是冻结 source-unit mapping，外部 formal 依据为 UML 元模型。全文逐字引文与页码见 [^uml251]；它只支撑元模型位置，具体存在义务来自当前 pair 的 NL binding。chronology/leakage：来源池由 `3e4e003e1` 重映射、registry 由 `d1b4d71c7` 冻结，故只能称 literature-informed、retrospectively consolidated。

**方法、实例与 W2。** registry 的 kind-parametric inventory 是义务层；native source-static backend 仅执行 `state`、`event`、`transition`/`edge` 的 `closed_fcstm` membership。variable、action、effect、composite 或 owner-local scope 不在 S1 的可执行片段，必须保持 W1/W0 或由其他谓词处理。实例的 kind、名称和 scope 仍须来自精确 NL/source binding。W2 还要求合法 typed inputs、终止 Boolean receipt 和 hash-bound replay，缺任一项不把运行结论升格为论文主张。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，仅 `scope=closed_fcstm` 的 state/event/transition/edge membership。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。该 fragment 的 `true`、`false`均 `W2/ELIGIBLE`；`unknown`、`failure`均 `W1/INELIGIBLE`。`0000:r3:i4:receipt`（composite，W1）和 `0034:r3:i2:receipt`（composite，W0）本已不是 W2，故只收窄发表解释，不改变 W2、headline 或重跑资格。

### S2 `transition_exists`

**现行精确命题。** “A transition exists between the specified source and target.” source--target requirement 由 NL 授权，Transition endpoint 由 UML §14.5.11.8 支撑。[`ST1,ST2,ST4`; ^uml251]

**义务与出处。** `edge_declared` 直接承接为 S2，`initial_target` 仅承接入口 target identity，未把 initial 唯一性或无 trigger/guard 的良构性偷换为本谓词。`ST1,ST2,ST4` 的 external formal anchor 是 UML；全文逐字引文为 “The source and target Vertices of a Transition must be contained in the same StateMachine as the Transition.”（[^uml251]，§14.5.11.8, p. 362），它支撑 endpoint 的语义位置，不替 NL 规定 endpoint。chronology/leakage 见 `3e4e003e1`、`d1b4d71c7`。

**方法、实例与 W2。** exact owner-local state path、initial pseudostate 和 source--target carrier 的解释是 method-owned；某一 endpoint pair 是否应存在必须由 pair 的 NL/source binding 授权。W2 要求这类绑定、native identity、完整 receipt 和 replay 同时成立。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，仅 exact native state paths 和 `closed_fcstm`/exact owner scope。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。该 fragment 的 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 enabledness、trigger、effect 或跨层级模糊引用。影响 0。

### S3 `trigger_set_equals`

**现行精确命题。** “The parsed trigger set of a transition equals the required trigger set.” trigger 属于 transition；未触发迁移是可能的 requirements 缺口。[`ST1,ST2,ST5`; ^uml251,^heimdahl1996]

**义务与出处。** S3 是 `newly_added`：旧 19 没有同形 trigger-set equality，但其来源池已有 UML trigger slot 与层次状态需求一致性资料 `ST1,ST2,ST5`。全文逐字引文与页码分别见 [^uml251]、[^heimdahl1996]；它们说明 transition/condition 的语义位置和一致性检查形状，required trigger set 本身只来自 NL。chronology/leakage：`d1b4d71c7` 在四族 surface 冻结此比较，未声明其与 54 pair 独立。

**方法、实例与 W2。** FCSTM tokenization、无序集合和 AST/canonical equality 是 method-owned，不能冒充 external semantic definition；transition carrier 与 required trigger list 则由 source/NL binding 授权。W2 要求 exact carrier、合法 list、terminal receipt 和 replay；没有 carrier 时保留 W1/W0，不从 parser 能力反推义务。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，精确 carrier 的无序 parsed token set。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。token equality 不推出 event path identity 或消费。影响 0。

### S4 `state_action_attached`

**现行精确命题。** “The specified action is attached to the specified lifecycle phase of the specified state.” lifecycle slots和控制恢复动作支撑静态 requirement-relative 检查。[`ST1,ST3,ST7`; ^uml251]

**义务与出处。** legacy `action_declared` 在当前 surface 被 split：S4 只检查静态 lifecycle slot，R3 才检查 trace 内行为发生。`ST1,ST3,ST7` 映射到 UML action/lifecycle position 和控制恢复资料；全文逐字引文和页码见 [^uml251]。这不把外部元模型的 optional slot 误写为必须存在的领域规则，只有 NL 明示才成立。chronology/leakage 由 `3e4e003e1` 的 typed-surface remapping 和 `d1b4d71c7` 的 registry freeze 记录。

**方法、实例与 W2。** `entry|do|exit` 的 closed enumeration、action representation 和 source carrier 是方法语义；state、phase、action 的 expected value 是实例绑定。W2 必须同时有 exact state、phase/action binding、合法 typed plan、terminal receipt 和 replay；它不会把静态挂接误写成动作已实际执行。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，exact state 与 `entry|do|exit`。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。静态挂接不推出动作实际发生。影响 0。

### S5 `transition_guard_equals`

**现行精确命题。** “The parsed guard of a transition equals the required guard.” external source 只定位 guard 的 transition role；NL 才建立 equality obligation。[`ST1,ST2,ST3`; ^uml251]

**义务与出处。** legacy `guard_distinguishable` 被拆为 S5 的 carrier-local equality、V1 的互斥和 V2 的覆盖。`ST1,ST2,ST3` 只提供 guard 的元模型/控制模型位置；全文逐字引文与页码见 [^uml251]。guard exactness 的 requirement-relative 方向来自 NL，而不是从 UML 的 optional guard slot 推导。chronology/leakage：`d1b4d71c7` 冻结拆分；未证明 freeze 前未接触 evaluation ledger。

**方法、实例与 W2。** FCSTM guard AST 的 structural equality、空 guard 的表示和 parser failure 由方法规格定义；目标 transition 与 required guard 由 source/NL binding 定义。W2 仅适用于 exact carrier 与 AST fragment 的 complete receipt/replay；逻辑等价、SAT 和业务等价排除在外。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，exact carrier 的 FCSTM guard AST structural equality。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出逻辑 SAT、等价或业务等价。影响 0。

### S6 `transition_effect_attached`

**现行精确命题。** “The specified effect belongs to the effect set of the specified transition.” effect 是 transition 的正式 slot，控制迁移可以附执行动作。[`ST1,ST2,ST9`; ^uml251]

**义务与出处。** `effect_declared` 直接承接为 S6。`ST1,ST2,ST9` 将 external UML effect slot 与控制迁移动作材料映射到当前义务；全文逐字引文和页码见 [^uml251]。这只说明 effect 的语义位置，所需 effect member 是 source/NL 实例授权。chronology/leakage：来源池重映射在 `3e4e003e1`，四族命题在 `d1b4d71c7` 冻结。

**方法、实例与 W2。** exact transition carrier、effect list membership 和 token representation 属于方法执行语义；transition/effect expectation 来自 binding。W2 需要 exact carrier、完整 typed inputs、terminal Boolean receipt 与 hash-bound replay；不把 effect membership 推成实际执行、输出或变量后值。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，一个 exact transition 的 effect member。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出执行、输出或变量变化。影响 0。

### G1 `may_reach`

**现行精确命题。** “A finite graph path exists from the source set to the target set.” 有限可达性是经典 verification property。[`TP1,TP2,ST3`; ^dwyer1999]

**义务与出处。** legacy `reaches` 在当前拆为 G1 的 existential finite path 与 G2 的 universal eventuality；两者不互推。`TP1,TP2,ST3` 映射到 property-pattern 与控制模型来源。全文逐字引文和调查范围见 [^dwyer1999]，其 511/555 pattern 统计支持性质形状的使用，而不是当前实例。chronology/leakage：`3e4e003e1` 的 operator remapping 先于 `d1b4d71c7` 的 registry freeze，但没有事前独立于 evaluation 的主张。

**方法、实例与 W2。** leaf graph、source/target set normalization 与图搜索是 method-owned；两个 endpoint set 是否必须存在来自 NL/source binding。W2 要求 closed native graph、exact binding、terminal receipt 和 replay；守卫、数据、优先级和 scheduler 不在这一图 fragment 内。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，closed native leaf graph。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 guard/data/priority/scheduling 下可执行。影响 0。

### G2 `must_reach`

**现行精确命题。** “Under the declared graph completion, every path from the source eventually visits the target.” universal eventuality 不等于 G1 reachability。[`TP2,TP3,TP4`; ^dwyer1999]

**义务与出处。** `reaches` 的全称分支和 `terminates` 的必达成分在 G2 汇合，外部 property-pattern/路径语义 source units 为 `TP2,TP3,TP4`。全文逐字引文、页码和 555-property 调查定位见 [^dwyer1999]；它支持 eventuality 的逻辑形式，不给本项目设置 horizon。chronology/leakage：当前命题由 `d1b4d71c7` 冻结，native receipt 由 `056997691` 统一，均不能倒写为 preregistration。

**方法、实例与 W2。** `H=declared-state count`、`.fbmcq` query 和 receipt decoding 是方法语义；起点、目标和 graph completion 是实例 binding。由于没有 lasso/completeness 论证，W2 不能承载 registry 的无界全称命题，故 publication exclusion 是语义裁定，不是新实验问题。

**执行、极性与发表。** `RESOLVED_CLAIM_EXCLUSION`。backend 检查 `must_reach <= H`，`H=declared-state count`，没有 lasso 或 completeness 论证。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。`true`、`false`均 `NOT_APPLICABLE/INELIGIBLE`，claim scope 是“历史 runtime receipt，不是无界 G2”；`unknown`、`failure`同样 INELIGIBLE。影响：排除 `0020:r3:i1:receipt`、`0020:r3:i5:receipt` 共 2 条 W2 的论文级解释，原 W2 和 headline 不变。

### G3 `route_avoids`

**现行精确命题。** “Every path from the source to the target avoids the forbidden node or edge set.” source--target scope 内的 absence 是形式性质形状；禁止冲突进路是铁路安全约束形状。[`TP1,TP3,TP3B,TP3C`; ^dwyer1999,^mirabadi2009]

**义务与出处。** G3 是新增的 source--target avoidance 命题，未把旧 `reaches` 或 `terminates` 伪装成禁止路径。全文逐字引文与页码：Dwyer 等将“between”限定为两个状态/事件之间的执行片段，并将 absence 定义为该 scope 内不发生给定状态/事件（[^dwyer1999]，pp. 413--414）；这给出全称路径约束的形式形状。Mirabadi 与 Yazdi 的铁路联锁全文则把冲突 movement 的 route isolation 和“no two conflicting routes”列为安全要求（[^mirabadi2009]，pp. 2、6）。`TP3,TP3B,TP3C` 只记录这些外部来源到冻结 source pool 的映射，不替代一手引用。chronology/leakage：`d1b4d71c7` 新增 registry row，`056997691` 固化 native execution。

**方法、实例与 W2。** native route enumeration 与 forbidden carrier normalization 是方法语义；source、target、forbidden set 必须逐项受 NL/source binding 授权。W2 只涵盖 exact leaf-node fragment 与 complete receipt/replay。没有 source-target path 的 `true` 是空真，不能改写为存在一条安全路线。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，只支持 exact leaf-state forbidden node，不支持 edge/composite。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`，但无 source-target path 时 `true` 空真，不能解释为存在安全路径；`unknown`、`failure`为 `W1/INELIGIBLE`。影响 0。

### G4 `coaccessible_to`

**现行精确命题。** “Every root-reachable node can reach a marked node along a finite path.” nonblocking/coaccessibility不同于 termination。[`TP6,G4-RP1,G4-RP2`; ^mohajerani2016]

**义务与出处。** legacy `terminates` 的 coaccessibility 成分拆为 G4，和 G2 的必达、V4 的 progress 保持不同。`TP6,G4-RP1,G4-RP2` 映射到 nonblocking/reachability sources；Mohajerani 等的全文逐字定义是 every reachable state reaches a marked state，书目信息与定位见 [^mohajerani2016]。它支撑 formal obligation，不把任何 marked state 的选择说成外部事实。chronology/leakage：`3e4e003e1` 记录 typed obligation remapping，`d1b4d71c7` 冻结当前 operator。

**方法、实例与 W2。** root/marked set、native topology projection 与 finite-path executor 是方法语义；roots 和 marked states 来自 source/NL binding。W2 仅在完整 native topology fragment、终止 Boolean receipt 和 replay 内可用；不推出 all-path termination、公平性或 concurrent configuration-space。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，仅 native topology projection。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 all-path termination、公平性或并发 configuration-space。影响 0。

### R1 `event_consumed`

**现行精确命题。** “The exact event occurs and is consumed in the declared macrostep.” 未触发迁移的事件是 requirements consistency concern。[`TR1,TR2,ST8`; ^heimdahl1996]

**义务与出处。** legacy `event_consumed` 直接承接为 R1。`TR1,TR2,ST8` 映射控制场景、协议状态机执行和技术边界；Heimdahl--Leveson 的全文逐字引文和页码见 [^heimdahl1996]，它支撑 requirement consistency 检查而不定义本项目消费 API。chronology/leakage：`3e4e003e1` 留下来源池复用记录，`056997691` 才统一 native witness execution。

**方法、实例与 W2。** `macrostep`、cold schedule、consumer identification 和 `called()` 是方法自有语义；event、schedule、step 和期望消费由精确 NL/source binding 授权。W2 需 native trace、terminal Boolean receipt 和 hash-bound replay；它不推广为所有 event 或 scheduler 的结论。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，一个 closed cold schedule。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。`macrostep` 与 consumer 是方法语义，不推出所有事件或调度。影响 0。

### R2 `state_reached_after`

**现行精确命题。** “The target state is active in the trailing portion of the declared trace window.” 控制刺激后的 occupancy 是轨迹 requirement 形状。[`TR1,TR2,ST3`; ^dwyer1999]

**义务与出处。** `occupancy_after` 直接承接为 R2。`TR1,TR2,ST3` 连接控制刺激与轨迹来源；Dwyer 等对 response/existence pattern 的全文逐字引文、页码与调查边界见 [^dwyer1999]。该来源只说明 post-stimulus occupancy 是可形式化性质形状，target、stimulus 和窗口由实例 binding 决定。chronology/leakage：重映射 `3e4e003e1`，冻结 `d1b4d71c7`。

**方法、实例与 W2。** cold scenario、trailing window 和 active-state observation 是方法语义；stimulus、state 和 window 是 NL/source authority。W2 需要 exact trace, complete terminal receipt 和 replay；不能从单一 schedule 推出因果、所有调度或全局可达性。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，固定 cold scenario/trailing window。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出因果或所有调度可达。影响 0。

### R3 `behavior_occurs`

**现行精确命题。** “The specified behavior occurs at the specified owner and slot within the trace.” lifecycle behaviour/trace obligation来自状态机执行实践。[`TR1,TR2,ST8`; ^andrec2023]

**义务与出处。** legacy `action_declared` 的运行时分支由 R3 承接，S4 只保留静态 slot。`TR1,TR2,ST8` 与 UML-state-machine execution sources 对应；André 等对不同状态机语义和验证转换的全文逐字引文、版本与页码见 [^andrec2023]。这不把 `called()` 或当前 replay fidelity 洗成外部语义。chronology/leakage：typed remapping 为 `3e4e003e1`，native execution 为 `056997691`。

**方法、实例与 W2。** lifecycle carrier resolution、`called()`、trace window 与 replay fidelity 是方法定义；owner、slot、behavior 和 window 由 source/NL binding 授权。W2 仅在该具名 abstract carrier、合法 scenario 和完整 receipt/replay 条件下成立；不推出具体 I/O 或业务效果。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，具名 abstract lifecycle carrier 和固定 window。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。`called()` 和 replay fidelity 是方法定义，不推出具体 I/O 或业务效果。影响 0。

### R4 `state_retained`

**现行精确命题。** “The target state remains active at every recorded point in the closed interval.” 这是有限 trace 内保持，而非无限 persistence。[`TP1,TR4,TR5,TR6`; ^dwyer1999]

**义务与出处。** `stays_in` 直接承接为 R4；它保留有限 interval 内 active 的要求，不把 legacy 名称偷换成无限 persistence。`TP1` 提供 universality/persistence 的外部形式义务；`TR4,TR5,TR6` 只与 trace/counterexample evidence 的技术形态对应。Dwyer 等的 universality/persistence 边界和全文逐字引文定位见 [^dwyer1999]。实例 interval 而非外部文献给出具体时长。chronology/leakage：`3e4e003e1` remapping，`d1b4d71c7` registry freeze。

**方法、实例与 W2。** recorded points、closed interval 和 SimulationRuntime trace 是方法语义；state/interval 是精确 NL/source binding。W2 需要完整 trace、terminal receipt 和 replay，任何 unknown/failure 仅保留 W1；不推出连续时间、open until 或 global invariant。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，closed interval 的 recorded points。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出连续时间、开放 until 或全局 invariant。影响 0。

### V1 `guards_disjoint`

**现行精确命题。** “No two guards in the same choice group are simultaneously satisfiable within the declared domain.” A-7E/Ford 的 overlap/nondeterminism 检查说明义务形状；UML 不默认要求互斥。[`BV4,BV5,BV6`; ^heitmeyer1996,^sims2001]

**义务与出处。** legacy `guard_distinguishable` 在当前被分解为 S5 equality、V1 disjointness 与 V2 completeness。`BV4,BV5,BV6` 对应 A-7E/Ford guard analyses；Heitmeyer 等的 A-7E disjointness report 和 Sims 等的 overlapping-condition example 均有全文逐字引文、页码和书目信息 [^heitmeyer1996][^sims2001]。这些来源说明检查义务，不把 UML 写成默认互斥规则。chronology/leakage：分解冻结于 `d1b4d71c7`，未声称事前隔离 evaluation。

**方法、实例与 W2。** choice-group collection、solver encoding、finite-domain enumeration 与 assignment witness 是方法语义；source/event、guard list 和 finite domain 只能由 NL/source binding 给予。W2 还需完整 group、合法 domain、terminal receipt 与 replay。有限域 true 不可以推出全输入域互斥。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，完整 same-source/same-event group 与明确 finite domain。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。domain必须来自 NL binding，有限 true 不推出全输入互斥。影响 0。

### V2 `guards_complete`

**现行精确命题。** “The disjunction of guards in the same choice group covers the declared input domain.” guard coverage是 requirements completeness 的经典检查。[`BV4,BV5,BV6`; ^heimdahl1996,^sims2001]

**义务与出处。** V2 是 `guard_distinguishable` 拆分后的 coverage 分支，非 S5 equality 的同义复述。`BV4,BV5,BV6` 关联 guard coverage sources；Heimdahl--Leveson 的全文逐字要求是 “The logical OR of the conditions on every transition out of any state must form a tautology.”（[^heimdahl1996]，p. 4），Sims 等的 Ford missing-case checks 提供工业检查背景 [^sims2001]。域的边界仍须由当前 NL 给出。chronology/leakage：`d1b4d71c7` 冻结 current predicate；不写 preregistered taxonomy。

**方法、实例与 W2。** exact choice group、finite-domain solver program、uncovered assignment 和 receipt are method-owned；source/trigger/domain binding 是实例 authority。W2 只在完整 group 与 declared finite domain、terminal receipt 和 replay 同时具备时可写；不推出 global coverage 或 deadlock freedom。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，exact choice group与 finite declared domain。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。fragment 内 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。不推出 global coverage或deadlock freedom。影响 0。

### V3 `response_within`

**现行精确命题。** “After every supported occurrence of p, q occurs within the declared bound and unit.” response是外部 property pattern；步数界是更窄的当前义务。[`TP1,BV7,TR1`; ^dwyer1999]

**义务与出处。** legacy `response_within` 直接承接为 V3。`TP1,BV7,TR1` 连接 response pattern、bounded-response audit 与 scenario source；Dwyer 等的全文逐字引文、页码和 sample boundary 见 [^dwyer1999]。外部 literature 可支撑 response pattern，不能把无界 eventually 直接变成 milliseconds 或 steps bound。chronology/leakage：四族 row 由 `d1b4d71c7` 冻结，当前 V3 gate 的修复发生在本 R1，且不改任何 frozen receipt。

**方法、实例与 W2。** `.fbmcq` 编译的 discrete step bound、scope 和 replay 是方法语义；p/q、bound、unit 和 scope 由 current NL/source binding 授权。W2 仅在 `unit=steps` 的受支持 fragment、terminal receipt 和 replay 中成立；milliseconds 是明确的 W1/INELIGIBLE exclusion，不是 experiment TODO。

**执行、极性与发表。** `IMPLEMENTATION_SUBSET`，只接受正整数 `unit=steps`。本轮将 soundness validator 从错误接受 `milliseconds` 收紧到与 backend 一致，回归覆盖见 `method/tests/test_provider_free_fixture.py`。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。steps fragment的 `true`、`false`为 `W2/ELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`；milliseconds为 W1/INELIGIBLE。影响 0。

### V4 `deadlock_free`

**现行精确命题。** “Every reachable, stable, nonterminal configuration admits model progress.” deadlock freedom与 termination不同。[`TP4,BV8,BV7,BV9`; ^andrec2023]

**义务与出处。** `terminates` 的 progress 成分在 V4 单列，不与 G2/G4 混用。`TP4` 提供对所有路径或所有可达配置量化的外部形式依据；`BV8,BV7,BV9` 仅映射并发状态空间、deadlock audit 与 TLA+ 的技术术语和边界。André 等对 UML state-machine semantics/model-checking translation 的全文逐字引文、版本和页码见 [^andrec2023]。这支撑 configuration-level formal obligation，不把 local leaf probe 写成外部 theorem。chronology/leakage：native receipt unified 于 `056997691`，R1 仅收窄其发表解释。

**方法、实例与 W2。** topology-reachable leaves、hot start、one-step probe、state-preserving effects 与 valuation coverage 的实现差异由 method audit 定义；initial scope 必须来自 source/NL binding。既有 probe 没有枚举 all reachable configurations，故所有极性均无 publication W2，82 个 exact terminal-false receipt IDs 被列入 impact exclusion，而非重新运行或修改 canonical data。

**执行、极性与发表。** `RESOLVED_CLAIM_EXCLUSION`。backend 在 topology-reachable stable leaves 做 one-step probe，未枚举 all reachable configurations，且 hot start、state-preserving effect与 valuation覆盖未闭合。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。`true`、`false`均 `NOT_APPLICABLE/INELIGIBLE`，`unknown`、`failure`同样 INELIGIBLE。影响：排除 `current_source_catalog.json` 中精确列出的 82 个 terminal-false V4 receipts 的全称论文级 W2 解释，保留历史 receipt、W 和 headline。

### V5 `state_invariant`

**现行精确命题。** “Every reachable configuration satisfies the expected occupancy value of the specified state.” safety invariant和互斥 occupancy有外部状态空间依据。[`TP3,TP3B,TP3C`; ^dwyer1999]

**义务与出处。** legacy `persists_until`、`invariant` 合并为 V5 的 occupancy safety core；当前 true 的有限通过不再继承 legacy 的强名称。`TP3,TP3B,TP3C` 连接 safety/path sources，Dwyer 等的 universality property pattern 全文逐字引文、页码和样本边界见 [^dwyer1999]。它只支撑无界 invariant 的规范形状，expected occupancy 是 source/NL binding。chronology/leakage：`3e4e003e1` 重映射，`056997691` 固化 runtime path，均非 evaluation-independent registration。

**方法、实例与 W2。** finite horizon、initial scope、solver program 和 replay are method-owned；state/expected occupancy/initial scope 是实例 authority。bounded `false` 加上 exact binding 和 complete replay 是对无界 invariant 的单向反例，bounded `true` 不是证明。因此 `false` 可 W2，其他极性维持 W1/INELIGIBLE。

**执行、极性与发表。** `SOUND_FALSE_PROXY`。有限 horizon 内的 `false` 是无界 invariant 的有效反例，bounded `true` 不证明无界性质。状态：`QUALIFIED_EXTERNAL; SPECIFIED_AND_TESTED; SOURCE_BOUND`。`false`为 `W2/ELIGIBLE`，scope 是完整 binding/replayed counterexample；`true`为 `W1/INELIGIBLE`；`unknown`、`failure`为 `W1/INELIGIBLE`。影响 0。

## 发表面结论

19/19 均为 `QUALIFIED_EXTERNAL`、`SPECIFIED_AND_TESTED`、`SOURCE_BOUND`；没有把 private FCSTM semantics 洗成外部传统。G2 的 2 条和 V4 的 82 条历史 W2 保留为冻结 runtime evidence，但不再作为全称论文级 W2 证明。V3 的 milliseconds 合同已修复。其余 W2 只能按上文 fragment 和 polarity 书写。19 条不是完备 defect taxonomy，也不是 evaluation-independent preregistration。
