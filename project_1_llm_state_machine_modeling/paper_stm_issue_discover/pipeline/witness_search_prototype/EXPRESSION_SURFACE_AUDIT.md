# EvidenceGoal 表达面审计与领域先行构建协议

状态：本文件是当前表达面审计的唯一事实源。它区分“已实现”“已粗审”“已知缺口”和“待领域取证候选”，不得用开发样例的命中结果替代逐条表达能力证明。

## 1. 当前结论

第二版台账唯一真源共有 145 条，其中 `L0/L1/L2=71/35/39`，`D2/D1=98/47`。本轮已经通览全部 145 条的 `id`、D、L、axes 和 summary，并对当前 25 个 `EvidenceGoal.relation`、13 个模板与 4 类执行后端做了粗粒度对照；这足以发现若干确定的表达缺口，但不等于已经完成逐条 feasibility proof。

当前仓库不存在完整的 `ledger item → normative property → EvidenceGoal → exact bindings → template/backend → W ceiling/unsupported reason` 矩阵。因此目前不能声称“145 条全部可表达”，也不能声称“大多数台账 issue 已经证明可覆盖”。0029 等 development pair 只能证明若干已实现关系能够端到端生成并真实执行 W2，不能证明完整表达面。

表达能力的正式完成判据是：每条台账 item 都有一行可复核映射；若可表达，必须给出不读取答案文本的 Goal 形状、形式绑定、后端、预期证书和最高 W；若不可表达，必须给出缺失的领域义务、元模型关系或执行语义。该矩阵只能用于覆盖审计，不得反向成为新增 Goal 家族的唯一动机。

## 2. 当前已实现的表达面

当前 25 个 relation 对 inventory/existence、initial、containment、direct transition、guard presence/overlap、reachability/dead-end、event consumption/response、wrong target/scope 和 stable termination 已有可执行路径。它们由 LLM 选择语义关系与 exact formal binding，再由固定 compiler 路由到 source/artifact AST、guard SMT、topology 或 pyfcstm trace/BMC；旧 19 个谓词只是部分 backend primitive，不是方法词表。

“存在 relation”不自动等于“完整表达该问题”。例如 `action_exists` 目前只检查某个 state/phase 是否存在任意 action，`transition_contract` 目前可以检查 edge 与 condition slot，却没有证明具体 guard 与规范 condition 等价。表达面审计必须核对被证明的精确命题，而不是只核对 relation 名字看起来相近。

## 3. 已确认的表达缺口

| 缺口族 | 代表台账项 | 当前为什么不足 | 需要的表达/后端能力 |
|---|---|---|---|
| UML region 与正交并发 | `EIS-0046-02`、`DIFF-0053-01` | `child_count` 只能数普通 direct substate，不能表达 region 数、orthogonality 或同时活跃；0046 已出现“真实 W2 但测错性质”的反例 | region metamodel IR、`region_count`、`orthogonal_region_exists`、`simultaneously_active`，以及 source region AST 与并发配置执行证书 |
| 具名 action/effect 身份 | `EIS-0014-04`、`EIS-0034-05`、`EIS-0024-02`、`EIS-0056-02` | `action_declared(state, phase)` 只证任意 action 存在，`effect_declared` 只证变量变化方向，不能证明 `Send`、`Emergency Stop` 或 `Decrease UAV Count` 的身份与槽位 | LLM 绑定规范 action/effect concept 与 exact source/FCSTM action ID；编译器检查 phase/slot/transition attachment；如比较 formal effect semantics，需声明可解析 fragment 与等价/蕴含后端 |
| 精确 condition 语义与 attachment | wrong-guard、condition scope/attachment 类 item | `transition_contract` 主要证明 relation 与 condition slot 存在，不能证明实际 guard 与规范 guard 同义、等价或挂在正确 relation 上 | LLM 给出规范 condition 与 exact relation binding；形式层对声明 grammar 内的 guard AST 做 equivalence/implication/attachment 检查，超出 fragment 降级 |
| state kind、composite 与 submachine | `EIS-0010-02` | `state_exists` 只证名字存在，不能证明 leaf/composite/submachine kind | `state_kind_is`、`is_composite`、`is_submachine` 与 source metamodel certificate |
| 层次迁移优先级、退出重入与历史保持 | `EIS-0039-02`、`EIS-0056-01` | same-source guard solver 和 bounded occupancy 不能表达祖先/后代 transition competition、层次优先级、退出重入导致的进度复位或 history preservation | hierarchical configuration semantics、enabled-transition priority、re-entry/history trace oracle，以及能同时指向竞争边和活动配置的 source certificate |
| 独立 trigger 集与复合 label 压缩 | `EIS-0000-02`、`EIS-0020-02`、`EIS-0030-03`、`EIS-0050-01` | 当前 event identity 常由一条 observed transition 绑定，缺少“NL 要求多个独立 trigger，而制品只有一个复合 event”的集合关系；missing event 也没有与 missing state 同等完整的规范不存在对象表示 | LLM 输出规范 trigger concept 集及各自适用 scope；形式层检查独立声明/消费关系与单事件 trace，不解析 label 词面来猜分解 |

另有一个明确的 schema/backend 不一致：`EvidenceGoal.sign` 允许 `changed`，而旧 `effect_declared` primitive 只接受 `positive/negative`。在冻结前必须选择删除该取值、补充严格定义的 `changed` 后端，或把它稳定降为 unsupported；不能让 schema 暗示并不存在的 W2 能力。

## 4. 领域先行的表达面构建

旧 19 谓词的来源调研已经暴露一项不可重复的错误：词表成员曾由本文评测 pair 上 750 条 splitter 输出的需求分布决定，属于 transductive 构建。它没有直接泄漏 ledger answer，但不能支持“方法由领域独立建立后再用于评测”的叙事。新 Goal 代数不得重复这一路径。

新表达面采用以下顺序构建并冻结：

1. 建立与 54 pair、145 条台账物理隔离的领域来源库，至少覆盖 UML/statechart 元模型与执行语义、状态机测试与 test-oracle/property-pattern 传统、model quality/model smell/UML defect taxonomy、控制与自动化系统需求、可执行 witness/counterexample/certificate 方法，以及 pyfcstm 当前可 sound 执行的形式片段。
2. 从来源中抽取“领域义务”，不是抽取本项目谓词名字。每条义务保存逐字引文、适用对象、量词/时序形状、最强反例、来源独立性、失败检索和限制，并按 ①领域证据、②元模型定义性、③暂缺外部依据分级。
3. 将来源独立的义务归纳成 obligation taxonomy，再设计最小且可组合的 Goal algebra。一个 Goal relation 只有在能够说明规范语义、binding 角色、正反例和预期执行证书时才可进入候选词表；不能因为某条 development ledger item 需要它就直接加入。
4. 为每个 Goal relation 建立 soundness table：允许的输入 fragment、AssertionIR 形状、backend、terminal verdict、source attribution 条件、W 上限、unsupported 出口和 mutation tests。没有 sound backend 的领域义务可以作为 W1/W0 发现面保留，但不能伪装成 W2 relation。
5. 用完全合成的 worked examples、metamorphic cases 和 mutation benchmark 检验 Goal、compiler 与证书，不把真实 pair ID、真实台账答案或 baseline miss 写入 runtime prompt。
6. 冻结来源库版本、taxonomy、Goal schema、compiler registry、prompt hash 和实现一致性审计后，才在 54 pair 上做 confirmatory evaluation。开发 pair 暴露的工程 bug 可以修；若由某条真实 item 导致新增语义 relation、规则或 prompt 义务，该 item 及同源近重复必须退出 confirmatory denominator 并登记 introduction motive。

这条路线支持的论文叙事是“基于领域与元模型证据建立可执行义务代数，然后在 54 pair 上评估发现、执行和归因效果”，而不是“观察 54 pair 的缺陷后把能命中的规则塞进词表”。[PR #183](https://github.com/HansBug/research_ideas/pull/183) 的旧 19 谓词 provenance 可以作为起始来源和反例材料，但不能直接平移成新 25 relation 已经获得充分出处。

## 5. 逐条 feasibility 矩阵合同

后续 145 条逐条审计至少包含以下字段：`ledger_id`、`D_ref`、`L_ref`、`normative_property`、`domain_obligation_id`、`goal_relation`、`goal_bindings_shape`、`binding_authority`、`template`、`backend`、`soundness_fragment`、`expected_certificate`、`w_ceiling`、`status`、`unsupported_reason`、`introduced_after_eval`。`status` 只能是 `expressible`、`partial`、`unsupported`、`not_a_method_obligation`。

逐条审计由 LLM 进行语义映射，不能用 ledger summary 关键词、axes 字符串或 defect kind 的确定性查表替代。确定性代码只可检查矩阵的 ID 完整性、枚举、引用闭包、145 条是否恰好覆盖和 relation/backend 是否存在。任何 `partial/unsupported` 都必须进入研究 backlog；任何在查看台账后新引入的 relation 必须标记 `introduced_after_eval=true`，并从 confirmatory claim 中隔离受影响条目。

## 6. 冻结前门

- 完成领域义务来源账和每个 Goal/template/backend 的 provenance；不能把“旧谓词有出处”外推为“新 relation 有出处”。
- 完成 145 条逐条 feasibility 矩阵，但只把它当覆盖审计与 limitation，不允许它静默改写已冻结的 confirmatory 方法。
- 关闭本文件列出的 region、named action/effect、condition、state kind、hierarchy/history、trigger-set 六类缺口，或明确其 W1/W0 上限和 headline 不覆盖范围。
- 对实现做语义边界一致性审计，尤其检查 unresolved 是否真正 veto、exact quote 是否被行号替代、是否存在唯一候选 namespace 补全、自由语义文本长度是否仍触发 schema failure，以及 receipt 是否绑定真实 LLM call/hash chain。
- 完成完全合成的正例、反例、非法 binding、unsupported fragment、backend exception 和 replay tests；同一 Goal 在修复 backend 后必须 replay 原 Goal，不能看到 truth 后改写。

## 7. 与实验结果的关系

0029 v36 的 `strict accepted 8/8` 是开发样例的 post-hoc 结果，说明当前表达子集可以自动发现并执行若干 L0/L1/L2 问题；它不证明 145 条表达完备，也不进入 overall 显著性或 precision 主张。正式结果必须另行报告 overall、L0/L1/L2、D×L、precision、W2 fraction、source-attribution fraction、degraded/unsupported grid 和同模型美元倍率。
