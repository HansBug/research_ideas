# Typed obligation surface 的领域来源与证据矩阵

状态：本文是 typed obligation surface 的来源真源。它回答“为什么需要这些义务、每个 operator 来自哪里、哪些是基础义务、哪些只是组合宏或后端关系”。它不从 54 pair、145 条台账、X1v2 漏报或任何调试运行推导方法成员。

## 1. 取证协议

本轮先复用 [PR #183](https://github.com/HansBug/research_ideas/pull/183) 已完成检索、逐字核验和对抗裁定的文献池，再只对新 surface 的空白做定向补检。复用的是来源与经裁定事实，不复用旧 19 谓词的分类、闭合词表或 transductive 构建故事；新 surface 必须重新完成“领域任务/真实缺陷 → typed family/operator → 必要字段 → lowering → executor”的映射。

证据分为三种：`P` 表示 PR #183 已有来源可直接复用，`N` 表示本轮因新 operator 或旧证据不充分而新增的一手来源，`Ø` 表示仍无直接领域依据。证据等级分为：①真实控制系统、工业模型、实际工具检查或带自然分母的经验材料；②OMG UML、语言规范或公认形式语义给出的定义性依据；③仅有本文需求或当前实现动机，不能宣称领域普遍性。

所有数量必须注明单位。`系统数`、`领域数`、`publication/source 数`、`property 数`、`check 数`和`tool report 数`互不替代；同一系统可支撑多个义务，各 operator 的系统数不得求和。PR #183 的 313 条界内案例和 310 篇论文是按相关性筛入的来源框，不是缺陷发生率分母；其最终 361 个 predicate-source 单元是存在性库存，也不是总体 prevalence 分母。

## 2. 冻结后的分层

论文只保留五类 semantic obligation：`ElementObligation`、`AttachmentObligation`、`GuardSetObligation`、`GraphObligation`、`TemporalObligation`。`UnsupportedObligation` 已删除，因为“当前后端是否支持”不是领域义务；编译器对每个候选产生独立 `SupportDisposition`，取值为 `executable/W2 ceiling`、`located_only/W1 ceiling` 或 `prose_only/W0 ceiling`。

每个 operator 另有一个方法角色：`core` 是有直接领域任务或标准语义的基础义务；`derived_macro` 是若干 core operator 的固定组合；`backend_comparison` 是 SMT、AST 或 type checker 的内部关系，不作为论文级领域性质；`under_supported_extension` 是有现实需求形状但领域基数薄弱、只能收窄陈述的扩展。该角色不决定某条 finding 的 D；D 仍由独立 LLM 裁决具体 NL 是否建立了被违反义务。

## 3. 结构义务矩阵

| 领域任务/缺陷 | 论文表示 | 角色 | 来源 | 现实基数与限制 | lowering / executor |
|---|---|---|---|---|---|
| 需求点名的 state/event/variable/action/effect/transition 是否存在 | `Element.exists(kind, ref)` | `core` | ②/P | PR #183 的保守真实系统下界分别为 12/1/6/9/9/18；这些集合重叠，不可求和 | `*_exists`，source/artifact AST 与 inventory |
| 某元素不得存在 | `not Element.exists(...)` | `derived_macro` | P | 与 existence 共用现实需求依据，不另造一类领域传统 | `exists(expected=false)`；当前 transition 有专门 `transition_absent` |
| 元素 kind 是否匹配 | type binding/check | `backend_comparison` | ②/P | UML 给出元类型与 association，但不证明 NL 到元素的绑定正确 | type/AST checker；不作为独立领域 operator |
| NL 明示的成员集合或数量是否完整 | `Element.cardinality`，优先 named-set equality | `under_supported_extension` | ①/P+N | PR #183 仅有 2 个实例和 1 个设备类标准；精确 N 必须来自 NL，不得从元模型阈值借用 | `child_count` 仅覆盖 direct、authored、non-pseudostate child；其他形状降级 |
| 子状态是否属于 NL 指定父状态 | `Attachment.containment(child,parent)` | `under_supported_extension` | ③/P+N | PR #183 真实系统下界为 0；UML Chapter 14 的 47 条 constraint 中没有“正确父状态”规则 | exact source containment + mapping projection；只能称 requirement-relative 检查 |
| 默认入口是否进入 NL 指定状态 | `Attachment.initial_target` | `core` | ①/P+N、②/N | 真实系统下界 5；target identity 由需求给出。UML 只直接支持 region 至多一个 initial、initial outgoing 至多一条且不得有 trigger/guard，是否必须有 initial 是 profile-specific semantic variation point | identity、existence、uniqueness、shape 应拆为四个 assertion，不再混成一个布尔结论 |
| transition source/target 引用是否完整 | `Attachment.transition_endpoints` | `core` | ②/P+N | `edge_declared` 的真实系统下界 18，至少 6 个领域；UML source/target 均为 `[1..1]` 且属于同一 StateMachine | exact AST endpoint assertion |
| transition 是否指向需求指定 target | `Attachment.transition_target_consistency` | `core` | ①/N | Lackner & Schmidt 2015 将 change transition target 列为 mutation target；没有合法系统分母，只能称 requirement/reference-relative | observed/reference transition 双边 endpoint assertion |
| NL 指定 trigger/guard/effect/action phase 是否挂在正确 slot | `Attachment.trigger/guard/effect/action_phase` | `core` | ①/P+N、②/P | effect/action 的真实系统下界均为 9；trigger/guard wrong-owner 与 action phase defect 没有独立系统分母。UML 中这些 slot 多数可选，只有 NL 明示时才形成义务 | exact slot/owner assertion；opaque expression 只定位，不做词面比较 |
| 同一 decision point 的 guard 是否可满足 | `GuardSet.satisfiable` | `core` | ①/P+N | 作为 dead transition、overlap 和 completeness 的基础查询；没有独立 prevalence | guard AST + SMT model/unsat receipt |
| 同一 `(source,event)` 的 alternatives 是否互斥 | `GuardSet.disjoint` | `core` | ①/P+N | 至少 A-7E、TCAS II、Ford powertrain 三个独立真实系统，覆盖航空与汽车；A-7E 报告 57 个实例但少数可能是假警报 | 对显式 `transition_refs` 按 `(source,event)` 分组，执行 pairwise SAT |
| 同一 `(source,event)` 的 alternatives 是否覆盖全部情况 | `GuardSet.complete` | `core` | ①/N | 至少上述三个真实系统；Ford 在一个 powertrain 模型上执行 65 个 missing-case checks | 检查 `valid(or(guards))`，保存 uncovered assignment；当前后端尚待补齐 |
| 两公式是否等价或蕴含 | formula `equivalent/implies` | `backend_comparison` | ② | 是 SMT 可定义关系，不是独立领域缺陷类型 | `p↔q` 双向 implication 或 `not sat(p and not q)` |

结构义务的主要一手来源是 [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF)、[Lackner & Schmidt 2015](https://doi.org/10.4204/EPTCS.180.4)、[Heitmeyer et al. 1996](https://doi.org/10.1145/234426.234431)、[Heimdahl & Leveson 1996](https://doi.org/10.1109/32.508311) 与 [Sims et al. 2001](https://doi.org/10.1109/ASE.2001.989794)。PR #183 的裁定后逐项数字见 [predicate_provenance.md](../../related_work/provenance/predicate_provenance.md) 和 [evidence_distribution.md](../../related_work/provenance/evidence_distribution.md)。

## 4. 图与时序义务矩阵

| 领域任务/性质 | 论文表示 | 角色 | 来源 | 现实基数与限制 | lowering / executor |
|---|---|---|---|---|---|
| 某状态/配置能否从指定起点到达 | `Graph.reachable(source,target)` | `core` | ①/P+N、②/N | PR #183 真实系统下界 8；B&O power controller 的 15 项工业性质中 3 项为 reachability/possibility | source-target BFS/topology；有 bound 时必须使用 bounded trace，不能静默复用无界图结论 |
| 全部可达非终态是否无 deadlock | `Graph.deadlock_free(scope)` | `core` | ①/N、②/N | RoboChart 有 3 个机器人案例系统；Ford、A-7E 等材料说明该检查真实存在，但没有跨系统 prevalence | 枚举 reachable configurations，并明确时间推进、final 豁免与并发语义；当前正式 lowering 仍缺 |
| 禁止路径或禁止到达作用域 | `Graph.path_absent(source,target/scope)` | `core` | ①/N、②/N | B&O power controller 15 项性质中 2 项属于路径排除；1 个真实系统、1 个领域 | reachability 的对偶、cut/path witness；不能退化成单边不存在 |
| 从每个 reachable state 可到 marked/final | `Graph.coaccessible_to(marked)` | `derived_macro` | ①/N、②/N | nonblocking 研究表含 19 个模型变体、7 个 model families、11/19 blocking；真实部署系统数未知 | `reachable(s) -> EF marked`；当前 `escapable = reachable and not_dead_end` 语义不足，冻结前只给 W1 |
| 从 target 必然到 root termination | `Graph.inevitable_root_termination_from(target)` | `derived_macro` | ②/N | UML 区分 FinalState 与 TerminatePseudostate，没有 `stable_termination` 标准 operator，也没有可靠现实分母 | `reachable(target) and AF(root_exit)`，并记录 cycle/dead-end counterexample；旧名仅作 legacy alias |
| 事件后到目标 | `Temporal.response(trigger,response,scope,bound?)` | `core`；event-target relation 是 macro | ①/P+N、②/P | PR #183 broad response 真实系统下界 17，但大部分是无界 eventually，不能当严格步数界；B&O 有 5/15 bounded response | unbounded 与 bounded response 分型；无 bound 不得默认 8 |
| P 之前必须已有 S | `Temporal.precedence` | `core` | ①/P+N、②/P | Dwyer 原始调查和 VTT 工业库均有该形状；B&O 有 3/15 ordering checks | scope-aware temporal lowering；当前后端尚缺 |
| 指定 scope 内至少出现一次 | `Temporal.existence` | `core` | ①/P+N、②/P | Dwyer 555-property survey 中 Existence 26；VTT 另有 recurrent reachability，但不是同一量词 | 必须显式区分 existential path 与 all-trace eventuality |
| 指定 scope 内不得出现 | `Temporal.absence` | `core` | ①/P+N、②/P | Dwyer survey 中 Absence 85；VTT 库有 124 条 `never {SERE}`，覆盖 5 个项目和 20 个系统 | scope-aware invariant/counterexample trace |
| 指定 scope 内始终成立 | `Temporal.universality` | `core` | ①/P+N、②/P | PR #183 invariant 真实系统下界 46；VTT 库有 2033 条 `G(p)`，覆盖 5 个项目和 26 个系统 | invariant/BMC 或无界模型检查；必须标注 bound 与证明范围 |
| 最终终止 | `existence(final)`、`response(start,final)` 或 `A<> final` | `derived_macro` | ②/N | termination 与 deadlock freedom 不等价；PR #183 旧 termination 真实系统下界 4，但只硬证了一半 | 组合 core patterns，不再作为独立基础 pattern |
| 持续到 release | `universality` + `after_until` scope | `derived_macro` | ①/P、②/P | PR #183 `persists_until` 真实系统下界 25；它不是 Manna-Pnueli 的 persistence `FG p` | `holds_until_release` 宏；若研究 `FG p` 应另立无界 operator |
| event consumer 是否可达 | executor precondition/receipt | `backend_comparison` | Ø | 没找到独立 verification pattern 或现实基数 | 仅作为 response/event-consumption assertion 的前置条件，不放入领域 surface |

图与时序的主要来源是 [Dwyer, Avrunin & Corbett 1999](https://doi.org/10.1145/302405.302672)、[UPPAAL query semantics](https://docs.uppaal.org/language-reference/query-semantics/symb_queries/)、[Mohajerani et al. 2016](https://doi.org/10.1007/s10626-015-0217-y)、[B&O power controller](https://doi.org/10.7146/brics.v6i8.20065)、[B&O A/V protocol](https://doi.org/10.7146/brics.v4i31.18957) 与 [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF)。

## 5. 合法自然分母

本轮新增的最强工业自然分母是 [VTT industrial property dataset](https://zenodo.org/records/7759742) 及其 [JSS 2024 论文](https://doi.org/10.1016/j.jss.2024.112153)：3923 条实际验证性质，来自 5 个客户项目、26 个匿名核电/铁路系统。样本内有 2033 条 `G(p)` 覆盖 26 个系统、445 条 `G(p -> X q)` 覆盖 22 个系统、415 条 sequence response 覆盖 22 个系统、373 条 `AG EF p` 覆盖 10 个系统、124 条 absence 覆盖 20 个系统、105 条 past precedence 覆盖 18 个系统、31 条 eventual response 覆盖 4 个系统。这些比例只能描述该性质库，不能外推控制系统总体，也不能声称每种公式都跨两个行业。

[Dwyer et al. 1999](https://doi.org/10.1145/302405.302672) 提供性质样本分母：555 条性质、至少 35 个来源，其中 511/555 匹配 patterns；Response 245、Universality 119、Absence 85、Existence 26、Precedence 26。它证明五类 pattern 对现实 property specification 的覆盖力，但不是系统数或控制领域发生率。

[Sims et al. 2001](https://doi.org/10.1109/ASE.2001.989794) 的 Ford powertrain 模型提供工具检查分母：536 个 nondeterminism checks 中 12 个失败、65 个 missing-case checks 中 0 个失败、426 个 dead-code checks 中 6 个失败。它只能说明这些义务在一个真实汽车控制模型上被批量执行，不能把 12/536 当作跨系统缺陷率。[Heitmeyer et al. 1996](https://doi.org/10.1145/234426.234431) 在一个 A-7E OFP 上报告 57 个 Disjointness tool reports，作者同时说明少数可能不是错误，因此不能写成 57 个确认缺陷。

## 6. 从来源到可执行方法

来源不是 prompt 中的一张“缺陷答案表”。冻结过程先把现实检查任务归纳为五类义务和最小 core operator，再由 method-owned registry 固定派生宏、字段角色、允许的 lowering、soundness fragment 与 executor。LLM 只做 NL 义务、scope、coreference 和 exact element binding；确定性 compiler 只检查 typed operator 与 `EvidenceGoal` relation 的预注册兼容关系，并执行 AST、图、SMT 或 trace 程序。

每条候选必须经历 `typed obligation → operator-level lowering validation → SupportDisposition → compiled Evidence Program → real execution → receipt → source attribution → independent D adjudication`。没有 sound lowering 时，候选不会被删除：有 exact location 则 W1，没有 location 则 W0；只有真实执行得到 terminal counterexample 且证据链闭合时才是 W2。

54 pair 只用于冻结方法后的统一 benchmark evaluation。逐条 feasibility audit 可以揭示哪些条目在当前 surface 中 expressible、partial 或 unsupported，并形成 limitation，但不得反向添加 operator、修改 prompt 语义或把 X1v2 miss 变成方法规则。工程调试只允许修复 schema、hash chain、exception handling、lowering 实现和证据闭包对既定合同的偏离。

## 7. 三段式论文 story

第一段：真实控制系统、工业属性库、状态机质量检查、UML/形式语义和 property-pattern 传统已经反复提出 element/attachment、guard consistency/completeness、reachability/deadlock/path exclusion 与五类 temporal pattern；本文通过复用 PR #183 的裁定后来源池并补齐其空白，构建五类 typed obligation surface，同时明确宏、后端关系与证据不足扩展。

第二段：方法将 NL、作者源 PlantUML、带语义映射注释的 FCSTM 和 inspect 事实送入 LLM 语义节点，得到 typed obligation 与 exact binding；固定 compiler 将其 lower 为可执行 Evidence Program，在 pyfcstm/source AST/graph/SMT/trace 后端真实运行，并为每条 finding 产出 W、L、source attribution、执行 receipt 与独立 D。

第三段：冻结同一方法后，在完整 54 pair、145 条台账上与同模型 X1v2 横向比较 overall 与各 D×L 分层 hit、precision/false positive、W2/W1/W0、source-attributable W2 和美元成本倍率。论文的效果结论来自该统一评测，不来自 operator 的构建过程。
