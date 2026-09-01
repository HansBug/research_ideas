# Paper1 final talk：从自然语言与作者状态机发现可审计 issue

> 本文档是 Paper1 的最终定性说明，服务于论文写作与稳定交接；它不替代正式的 [v4 中文结果报告](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。所有当前数字只来自 [final-results v4 归档](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md) 及其 canonical JSON/TSV。历史 v46、v27、v2、旧裁定和旧 witness audit 仅由历史/provenance 入口保留，不属于当前 headline。

## 0. 开场路线图

Paper1 考察一条自然语言需求（NL）与同一任务的作者 PlantUML 状态机。在两份作者输入已经给定时，研究问题是能否发现可定位、可复核、带有理由和证据的不一致；它不涉及重新生成或自动修复模型。

冻结比较显示四点：current v4 的 overall FULL discovery coverage 高于 X1v2 baseline v3，优势在 L2 行为/全局性质上最明显；current 的 report-based precision 低 `4.34 pp`，应结合无效报告的组成解释；19-predicate backend 在适用时提供可执行证据，但不能表达所有问题，未执行的谓词或缺少 receipt 的问题不能据此视为不存在。

下文按论文顺序给出问题、已有工作、统一框架、方法、人工评测、结果和边界。结果数字及其机器可读指针集中在第 6 节，避免让结果表替代前面的定义。

## 1. 问题、动机和范围

控制系统需求通常以自然语言给出，而状态机用状态、事件、迁移、guard、trigger 和 action 表达行为。即使模型表面上可解析，LLM 生成的模型仍可能与需求不对齐，或在结构和可执行行为上留下不一致。文本对照、结构检查和运行验证各自能观察到不同的部分；任何一种都不能单独覆盖这个问题。

本文研究的是给定 NL 与作者状态机之后的 issue discovery。模型对象写作

`M = (S, E, V, Tr, A)`，

其中 `S` 为状态，`E` 为事件，`V` 为变量，`Tr` 为迁移，`A` 为 action。当前证据片段覆盖离散 FSM、层次状态机，以及带变量、guard 和 action 的 EFSM 子集。完整模型边界见 [model scope](../paper_stm_issue_discover/story/model_scope.md)。

结论不外推到 clocks、invariants、orthogonal/concurrent regions、hybrid semantics、无界 temporal properties 或未声明的其他执行模型。本文也不证明模型在所有行为上完全正确，不把 repair 写成当前实验目标。145 条 ledger issue 是研究者根据纳入的 NL、作者 PlantUML 与来源证据人工维护的 source-backed expected inventory；它提供固定的比较分母，不是整个 defect universe 的绝对真值。

## 2. 背景与相关工作

相关工作按照问题链而不是结果表组织。详细来源及其适用边界见 [related-work README](../paper_stm_issue_discover/related_work/README.md) 和 [predicate provenance](../paper_stm_issue_discover/related_work/provenance/predicate_provenance.md)。

### 2.1 Requirements-to-model consistency

需求到模型的一致性研究说明，模型的有效性和完整性必须相对需求、规格或可陈述的义务讨论，而不是只看图是否良构。IEEE Std 1044-2009 的 defect 定义、Krogstie 等的模型质量工作以及 FRET 的 requirements formalization 都提供了这一边界。它们不逐字定义本文的 D、L、W 或 145 条台账，而是说明为何 source fact、义务和证据必须分开记录。

### 2.2 状态机的结构与行为分析

UML、Statecharts 和 FSM 文献区分结构/局部状态问题与依赖路径、状态序列或执行集合的问题。Hilken 等讨论 structural 与 behavioral verification task；Baier 与 Katoen 区分 invariant 和依赖有限路径片段或执行集合的性质；Engels 等以及 Knapp 与 Mossakowski 说明部分一致性条件可静态检查，另一些需要考虑 dynamics。这些来源支撑“问题性质和所需信息范围”的概念边界，不强制任何 L2 问题必须使用 simulation、BMC 或 trajectory receipt。

### 2.3 Testing、simulation 与 model checking

model-based testing、simulation 与 model checking 为状态机行为提供不同形式的可观察执行、反例和验证边界。Barr 等关于 oracle problem 的整理、Tretmans 的 conformance/testing 讨论，以及 counterexample 文献都说明：一个 sound violation 或可复核反例足以建立某些问题存在，但一次通过或某个 predicate 为真不等于模型没有其他问题。本文因此把执行证据写成 W 的来源，而不把任何 backend 当成规范义务的唯一来源。

### 2.4 LLM 辅助建模与模型审查

现有研究分别覆盖需求形式化、模型验证、测试和 LLM 辅助建模。本文的关注点更窄：把 NL、作者状态机、source-level 定位、适用时的可执行证据，以及可复核的离线评测串成一条 issue-discovery 链路。本文不声称“首次”“唯一”，也不把相关工作的概念边界误写成项目规则。

### 2.5 Finding granularity、relatedness 与报告归并

报告行不是天然的 defect 单位。Porter、Votta 与 Basili 区分 true fault 和 false positive；Okun、Delaitre 与 Black 的 NIST SATE IV 报告区分 directly related、indirectly related 与 unrelated finding；Klees 等强调 fuzzing 的最终单位应是 distinct bug 而非 crash/input；Pearson 等说明 fault-level 评价受报告粒度影响；Martinez 等讨论 repair/semantic equivalence 的边界；Ahmed 等则把同根因、细节层级不同的 issue 作为 equivalent，并将人工确认的台账外真实问题单列。

这些来源支持 same-root-cause、relatedness、distinct issue 与报告粒度的概念。本文的 `FULL_MATCH/PARTIAL_MATCH/NO_MATCH`、K/N/I 和 N grouping 是基于这些概念形成的项目 operationalization，不是任一论文逐字给出的完整标准。

## 3. 统一问题框架：L、W 与 D

一个 finding 至少要回答三件互不替代的事：它是什么性质的问题、报告拿到了多强的证据、以及主张是否足以作为 defect claim。本文先定义 `L/W/D`，再在第 5 节用 relation 将报告与 expected ledger 建立比较关系，并派生 K/N/I。

```text
issue property (L) + report evidence (W) + defect qualification (D)
  -> relation to the expected ledger in the experiment
  -> K/N/I evaluation disposition
```

`L` 是 expected ledger 对问题性质的标注，`W` 是某条 report 的证据等级，`D` 是事实与被违反义务的裁定。L2 不自动要求 W2；W2 不自动使主张成为 defect；D2 也不说明问题属于哪个 L 层级。当前 L 的真源为 [l_tier.json](../paper_stm_issue_discover/discover_matrix/ledger_v2/l_tier.json)，其分布固定为 L0/L1/L2=`71/35/39`。

### 3.1 L：问题性质与所需信息范围

L 描述陈述一个 expected issue 需要理解到什么范围，不规定必须使用何种算法、predicate、backend 或 witness。

| 层级 | 项目 operationalization |
| --- | --- |
| L0 | pointwise/surface property。可由 NL 名称、属性或模型中单个元素及直接对应关系陈述，例如缺失或多余状态、事件、trigger，或局部标签不一致。 |
| L1 | structural/local-state property。涉及模型结构、单状态不变量或有限相邻元素关系；需要模型事实或局部结构，但问题本身不以多步执行、全局路径或执行集合量化，例如 guard 恒假、叶状态出度、局部层次或优先级。 |
| L2 | behavioral/global property。涉及状态和迁移间的路径、可达性、终止/非终止、死锁、事件响应、跨迁移约束或全局交互。它是问题性质，不表示必须生成轨迹或运行 BMC。 |

`defect_locus` 是 source anchor，不是 L 的替代字段。一条问题可锚定在单个 transition，却仍是 L2 的全局行为问题。L2 可由拓扑无路径、静态或符号充分条件、counterexample、trajectory、simulation 或 BMC 支持；没有 terminal execution receipt 时仍保留 L2，只把报告证据记为 W1。反过来，L1 也可以经合法 predicate execution 达到 W2。

在 `P => Q` 的用法中，`P` 是足以证明 defect `Q` 存在的 violation predicate。对 L2，若一个拓扑或结构性 `P` 被 soundly 证伪，就已足够建立 `Q`；不要求 `P <=> Q`，也不要求为形式完整性强行升级为更高级的行为轨迹。#189 的当前 L 定义、概念锚点与边界见 [issue #189](https://github.com/HansBug/research_ideas/issues/189)。

### 3.2 W：报告证据强度

| 层级 | 定义 |
| --- | --- |
| W0 | 只有散文主张。 |
| W1 | 有具体 source element、路径或结构定位，但没有完整 terminal receipt。 |
| W2 | 在准确制品上使用合法 executable object 和 typed input；artifact hash 一致；backend 返回明确 terminal `true/false`；receipt 保存输入、结果、版本和来源。 |

只要 predicate 在准确制品上合法完成，receipt 完整且 terminal result 明确，就按 W2 记录，不能因为旧 coverage marker 或保守标签降级。若当前 predicate registry、typed input 或 soundness fragment 无法表达某个问题，方法不把问题当作不存在，也不自动判成 false positive：有具体 source/structure evidence 时保留 W1；连具体定位也没有时才是 W0；fallback 原因必须写入审计字段。

### 3.3 D/A：什么主张足以称为 defect

D 是问题资格/规范性轴，回答 source fact 是否成立，以及是否存在可以陈述并守住的 violated obligation。它不由 W 或 predicate execution 自动决定。

| 裁定 | 定义 |
| --- | --- |
| D2 | source fact 成立，有明确 violated obligation，且没有存活的称职反读法。 |
| D1 | source fact 成立，但至少两种完整且与 source 相容的读法仍会改变义务或归因。 |
| D0 | source fact 成立，但没有 surviving violated obligation，或作者的设计解释成立。 |
| A0 | 报告事实或归因在完整作者制品上不成立。 |

D/A 是事实与义务的人工裁定轴。relation 与 K/N/I 是实验中报告和台账的比较及汇总，不能在此处互相替代。

## 4. 方法设计：从作者输入到可审计 evidence

方法不读取 expected ledger、人工裁定或历史 finding 来改变候选发现。冻结的流程把作者输入、工作表示、执行证据和人工评测职责分开：

```text
NL + 作者 PlantUML
  -> canonical source IR / source trace
  -> FCSTM working representation
  -> pyfcstm native / inspection facts
  -> candidate discovery and grounding
  -> predicate routing and typed execution
  -> evidence / receipt
  -> 人工 validity/relation/D-A adjudication
  -> deterministic evaluation summary
```

### 4.1 输入闭包和 provenance 固定

每个 cell 固定 pair identity、round、NL、作者 PlantUML、来源论文映射、artifact hash 和运行 manifest。方法只读取声明范围内的作者输入；expected ledger 与人工裁定物理上属于 evaluation 层，不能回流到方法候选。

### 4.2 NL contract extraction

从 NL 中抽取主体、状态、事件、条件、时序、响应、终止和其他可检查 obligation，并保留原文 source anchor。抽取结果用于提出候选和解释依据，不把候选自动升级为 defect 裁定。

### 4.3 作者模型解析和 source IR

作者 PlantUML 被解析为状态、迁移、trigger、guard、action、变量和 source location 的 canonical representation。source IR/source trace 的职责是保存作者文本与后续元素间的追溯关系；内部表示本身不是作者事实。

### 4.4 FCSTM projection 与 pyfcstm 原生事实

PlantUML 到 FCSTM 的 projection 提供统一、可执行的 working representation；pyfcstm/FCSTM 的原生 class、function 和 inspection facts 提供状态机事实、类型信息、迁移和执行语义。projection、compiler-owned element 或未闭合 runtime evidence 不能单独归因于作者模型。只有能经 source trace 回到作者制品的内容，才可成为 source-level finding。

### 4.5 候选发现和 grounding

discovery/grounding 把 NL obligation、作者模型事实和 source trace 汇合成候选 finding，并保存 source element、问题理由与证据基础。互补的 lens 只产生候选；它们在同一 finding schema 汇合后仍须经人工裁定，不能把散文主张直接写成已证实缺陷。

### 4.6 Predicate registry、routing 与 typed execution

谓词是可执行证据后端，不是方法主体外的临时脚本。冻结 registry `four-family-19-core.v1` 来自广泛、结构化的状态机、形式化验证、模型测试和执行语义领域调研，并经任务类型与常见性质的整体分析归纳为四族：Structure 6、Topology 4、Trajectory simulation 4、Bounded verification 5。provenance 为每个 ID 记录 domain/formal/technical 依据和能力边界；这是一套项目 predicate operationalization，不是已注册系统综述，也不声称单篇文献逐字规定 19 个具体 ID。

routing 根据候选 finding 的 obligation、元素类型、量词/时序需求和 backend capability 选择适用 predicate。binding 固定 typed input、source anchor、artifact hash 和 predicate ID；execution 才运行后端并保存 terminal result 与 receipt。仅有 predicate ID 或进入 routing 不等于已执行，更不等于 W2。

### 4.7 Evidence receipt、证据闭合与 W 分配

receipt 保存输入、输出、artifact hash、backend/version、source refs 和 terminal 状态。合法 execution 有 executable object、typed input、准确 artifact hash、明确 terminal `true/false` 与完整 receipt 时为 W2；只存在结构定位、路径或非终端线索时为 W1；只有散文主张时为 W0。W2 只提高可重放证据强度，不代替人工的 D/A、relation 或 K/N/I 裁定。

### 4.8 Predicate coverage 与 fallback

19 个谓词不保证覆盖所有可能的问题类型。当前 registry、typed input 或 soundness fragment 无法表达一个 source-grounded issue 时，方法保留 finding 和具体 source/structure evidence，记为 W1，并在 audit record 写明 predicate unsupported、typed input unavailable、capability boundary 或 receipt incomplete；没有具体定位时才记为 W0。谓词不是缺陷发现准入门，不能为了让每个 finding 都有 predicate 而伪造执行对象。

### 4.9 人工裁定和确定性评测

所有 validity、relation、D/A、K/N/I 与成分分析均由人工完成，并保留 reason、basis、source refs 与审计记录。人工以 [issue #189](https://github.com/HansBug/research_ideas/issues/189) 的 source-first/D-A 边界和 [issue #195](https://github.com/HansBug/research_ideas/issues/195) 的 relation/K-N-I 合同完成判读与仲裁。evaluator 只读取这些完成态人工记录，确定性地做闭合、去重、归并、指标计算、schema/hash/link 校验和算术复算。内部 reviewer 或 subagent 意见是质量审阅材料，不被表述为新的 inter-rater study。

## 5. 实验设计与人工评测协议

### 5.1 冻结矩阵与 expected inventory

冻结实验为 `54 pair x 3 rounds`，每侧 `162 cells`。54 个 pair 由来源论文纳入研究范围的 `6` 个 LLM 条件与 `9` 个 NL 案例构成，即 `6 x 9 = 54`。来源结果表的 `STM Results` 第 18 个数据行（Excel row 20）是 `llms_emp_feedback_final_0018`，即 Digital camera state machine diagrams；其作者 PlantUML 明确使用 fork/join 并描述 parallel paths，现有 working contract 将这类并发执行语义标为 capability-excluded。它整体超出本文离散/层次/EFSM fragment，因而在建立 Paper1 矩阵前排除；它不进入 54 pair、145 条台账或任何 hit/precision 分母。原始输入与来源定位见 [0018 source record](../paper_stm_issue_discover/selected_seed_examples/llms_emp_feedback_final_0018/source_meta.json) 和 [作者 PlantUML](../paper_stm_issue_discover/selected_seed_examples/llms_emp_feedback_final_0018/stm0.puml)。输入闭包和纳入映射由 [final-results archive](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md) 保存。

145 条台账由博士生研究者根据纳入 pair、对应 NL、作者状态机和来源证据逐条人工标注、整理与复核。台账保存 expected issue 内容、source locus、D/L、必要的性质/谓词预期及输入，但不是 method 运行后反向生成，也不是自动裁定产生。其形成、去重和边界见 [ledger README](../paper_stm_issue_discover/discover_matrix/ledger_v2/README.md)。

`hit@1` 的分母为 `145 x 3 = 435` expected-round units；L2 `hit@1` 的分母为 `39 x 3 = 117`。`hit@3` 和 `hit@all` 的分母为 145 unique expected IDs；L2 对应分母为 39。current v4 和 baseline v3 的人工审核构成并不完全对称：current 是既有 source-first 结果的逐条闭合，baseline v3 是非 K 逐条复核加原 K 冻结快照。因此它们是同一语义边界下的冻结比较，不是新的、完全对称的人类 inter-rater 研究。

### 5.2 Relation 与 K/N/I 的双维判读

issue #195 把“报告与 expected 的关系”和“报告自身是否成立及如何归属”分开。人工先确认报告核心技术主张是否成立；无效报告的 relations 强制闭合为全 `NO_MATCH`。有效报告再对同一 pair 的全部 expected 逐项判断 relation。

| relation | 含义 | 指标去向 |
| --- | --- | --- |
| `FULL_MATCH` | 与 expected 是同一缺陷实例、同一根因、同一 violated obligation，或同一根因的直接可归因表现。 | 贡献主 FULL hit。 |
| `PARTIAL_MATCH` | 有真实、可审计但不足以确认同一缺陷身份的局部或间接关系。 | 进入 supported coverage；不贡献主 FULL hit，也不是 false positive。 |
| `NO_MATCH` | 没有可接受的 expected relation，或是台账外问题。 | 在有效报告全 NO 时可进入 N。 |

relation 完成后，发布级 report disposition 为：

| 标签 | 概念定义 | 必要条件 | 评测角色 |
| --- | --- | --- | --- |
| `VALID_KNOWN`（K） | 报告核心主张成立，并可归属于至少一条冻结 expected。 | 有效，且至少一条 relation 为 FULL 或 PARTIAL。 | known report；只有 FULL 贡献主 hit，PARTIAL 只贡献 supported coverage。 |
| `VALID_NOVEL`（N） | 报告核心主张成立，但不是任何 frozen expected 的同一问题。 | 有独立制品证据、source anchor、reason/basis 和可行动主张；对该 pair 的全部 expected 为 NO。 | 有效但未认领台账的 report；不增加 expected hit，也不算 false positive。 |
| `INVALID`（I） | 核心主张不成立，或不能承担预先规定的最低举证责任。 | 作者制品、NL、执行/inspection evidence 或人工复核反驳主张，或无法给出可核验事实与归因。 | 无效 report；进入 report precision 分母和 invalid diagnostic，不是 defect entity。 |

固定顺序如下。`D/A` 是事实与 violated obligation 的裁定；K/N/I 是 relation 完成后的报告-台账闭合。D2/D1 报告仍必须经过有效性和 relation 审核，W 与 predicate 不参与这一闭合。

```text
source fact / technical claim
  -> D/A（事实与 violated obligation）
  -> 人工确认报告有效性；无效报告 relation 全为 NO_MATCH
  -> 枚举同一 pair 的全部 expected relation：FULL_MATCH / PARTIAL_MATCH / NO_MATCH
  -> K/N/I
  -> hit、supported coverage、precision、grouping 与诊断指标
```

在当前闭合中，D2/D1 加至少一个 FULL/PARTIAL 为 K；D2/D1 且同 pair 的全部 relations 为 NO 为 N；D0/A0 为 I。程序不会从模型自报标签、W、predicate ID、报告数量或台账缺席猜测 K/N/I。发布结果不保留 `OUT_OF_SCOPE`、最终 `UNKNOWN` 或“暂未审完”：争议在出数前经制品复核、独立复核和仲裁完成。

K 按 expected ledger ID 去重；同一 expected 的重复命中不增加 hit。N 只在同一 side、同一 pair 内，依据共同义务/property、相容 source locus/行为上下文、实质根因和最小 repair intent 做保守归并，允许跨 round；不能跨 side/pair，不能按文本相似度、状态名或 expected ID 自动合并。I 不建立 substantive defect group；I cluster 只描述无效报告的重复诊断形态。

### 5.3 指标与单位

指标按以下顺序报告：FULL `hit@1/@3/@all`、L2 FULL hit、report-based precision、W-on-hits、K/N/I、N substantive groups、I diagnostic clusters、predicate terminal usage 和 report-bound presence。

W-on-hits 对每一个 FULL hit unit 取该 hit 内最高 W，并以本侧 FULL hits 为分母。它不能由全部 finding 的 W 分布或全部 predicate execution 替代。主 precision 固定为 `(K reports + N reports) / all final reports`；任何 group/diagnostic 比率另行命名。

## 6. 冻结结果

本节的唯一数字源是 [fair comparison v4 combined summary](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json)、[current v4 summary](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit/summary_v4.json)、[baseline v3 summary](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json) 及正式 [v4 report](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。

### 6.1 Headline 与 coverage

| 指标 | current v4 | X1v2 baseline v3 | 单位/分母 |
| --- | ---: | ---: | --- |
| method cells / reports | 162 / 1271 | 162 / 512 | 每侧 54 pair x 3 rounds；report 是发布 finding 行。 |
| K / N / I reports | 749 / 231 / 291 | 312 / 105 / 95 | report-level disposition。 |
| D2 / D1 / D0 / A0 reports | 721 / 259 / 120 / 171 | 342 / 75 / 85 / 10 | report-level D/A。 |
| report precision | 980/1271 = 77.10% | 417/512 = 81.45% | `(K+N)/all reports`。 |
| FULL hit@1 | 310/435 = 71.26% | 227/435 = 52.18% | expected-round FULL units。 |
| FULL hit@3 | 119/145 = 82.07% | 106/145 = 73.10% | 任一 round FULL 的 unique expected IDs。 |
| FULL hit@all | 86/145 = 59.31% | 46/145 = 31.72% | 三轮均 FULL 的 unique expected IDs。 |
| L2 FULL hit@1 | 105/117 = 89.74% | 50/117 = 42.74% | 39 个 L2 expected x 3 rounds。 |
| L2 FULL hit@3 | 37/39 = 94.87% | 26/39 = 66.67% | unique L2 expected IDs。 |
| L2 FULL hit@all | 33/39 = 84.62% | 8/39 = 20.51% | 三轮均 FULL 的 L2 IDs。 |

### 6.2 W、predicate 与 report-bound presence

| 指标 | current v4 | X1v2 baseline v3 | 边界 |
| --- | ---: | ---: | --- |
| FULL-hit max W2 / W1 / W0 | 197/310 / 113/310 / 0/310 | 0/227 / 227/227 / 0/227 | 每侧以自己的 FULL-hit units 为分母。 |
| terminal-receipt distinct predicate IDs | 12/19 | N/A | current 的 distinct-ID execution 指标。 |
| report-bound distinct predicate IDs | 8/19 | N/A | current 的 distinct-ID binding 指标。 |
| report-bound binding rows / all reports | 825/1271 = 64.91% | N/A | 行级诊断，不是 distinct-ID 指标。 |
| legacy coverage-class marker / binding rows | 303/825 = 36.73% | N/A | 行级历史 marker，不替代 W、hit 或 coverage。 |

current 的 terminal IDs 是 `G1, G2, G4, R1, R2, R4, S1, S2, S3, S4, S5, V4`；report-bound IDs 是 `G1, G2, R2, S2, S3, S4, S5, V4`。`12/19` 与 `8/19` 都不是 defect coverage、FULL hit、W2 数或 predicate contribution。baseline 没有同构 predicate receipt/binding schema，因此写作 `N/A`，不是零。

### 6.3 I 的组成与 precision

| I 成分 | current v4 | baseline v3 |
| --- | ---: | ---: |
| D0 | 120 | 85 |
| ordinary A0 / `FALSE_POSITIVE` | 53 | 10 |
| current-only A0 / `NOT_A_DEFECT_CLAIM` (NADC) | 118 | N/A，baseline 无同构分类 |
| I reports | 291 | 95 |

current 侧 `291 = 120 + 53 + 118`。NADC 是 evaluation-only overlay：compiler-owned artifact `38`、projection/trace boundary `24`、runtime/evidence closure `48`、attribution-indeterminate `8`；其中 confirmed method-owned mechanisms 为 `110`，strict conversion-lowering confirmed 为 `0`。其来源为 [conversion attribution v1](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/README.md) 及 [summary JSON](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/i_attribution_summary_v1.json)。

precision 的差异为 `77.10% - 81.45% = -4.34 pp`；互补 I rate 为 current `291/1271 = 22.90%`、baseline `95/512 = 18.55%`，差异 `+4.34 pp`。描述性分解中，D0 rate 差为 `120/1271 - 85/512 = -7.16 pp`，ordinary A0 rate 差为 `53/1271 - 10/512 = +2.22 pp`；NADC 只能写 current-side `118/1271 = 9.28%`。baseline 没有同构 NADC 分类，不能把其缺失机械填为零，也不能用该 residual 做跨臂因果归因。

### 6.4 N：raw reports 与 substantive groups

N 的两个层次必须分开。raw N report 是人工裁定为 `VALID_NOVEL` 的发布报告行，用于审计和 report-based precision。N substantive group 是 same-side、same-pair、跨 round 可合并的实质性同质问题，用于描述已记录 novel root-cause 单元；它不是本体论意义上唯一的 defect 数。

| side | raw N reports | N substantive groups | report-level D2 / D1 | group-level D2 / D1 | raw-to-group | pair coverage |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| current v4 | 231 | 121 | 38/231 = 16.45% / 193/231 = 83.55% | 21/121 = 17.36% / 100/121 = 82.64% | 231/121 = 1.909 reports/group；`1 - 121/231 = 47.62%` 合并压缩 | 28/54 pair 有 N |
| baseline v3 | 105 | 98 | 50/105 = 47.62% / 55/105 = 52.38% | 48/98 = 48.98% / 50/98 = 51.02% | 105/98 = 1.071 reports/group；`1 - 98/105 = 6.67%` 合并压缩 | 34/54 pair 有 N |

`group-level D2/D1` 是对 canonical group JSON 每组 `d_tiers` 的确定性聚合，不是另一个改写过的 headline。两侧无 mixed-tier group；current 的 121 个 group 为 21 D2、100 D1，baseline 的 98 个 group 为 48 D2、50 D1。每个 N report 恰好有一个 group membership：current `231/231`，baseline `105/105`。baseline 的 group TSV 同时携带 95 个 I diagnostic clusters，不能误读为 193 个 N groups。

N group size 的组成进一步显示报告冗余形态不同：current 为 `1:52, 2:31, 3:36, 4:1, 5:1`，baseline 为 `1:92, 2:5, 3:1`。因此 current 的 N reports 更集中地重复落在少数 same-pair group 上，baseline 的 N groups 更常为保守 singleton。这个观察只描述报告-归并关系，不证明哪一侧发现了更多领域缺陷。

current 的代表组是 `v60_current:0006:0006:reachability:UAVSwarmStateMachine-root`：5 个成员 report，`d_tiers=[D2]`，其共同义务、source locus、根因和 repair intent 位于 [current N groups](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit/current_n_groups_v4.json) `#/groups/4`。baseline 的代表组是 `N-G-0022-01`：3 个 round 的同一 `PoweredOn` detour，`d_tiers=[D1]`，见 [baseline N groups](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json) `#/groups/n_groups/32`。这些审计记录保存共同义务、source locus、根因和 repair intent，而非仅保存文字相似度。

L 是 expected ledger 的属性，canonical N group schema 不给 N report 伪造 L0/L1/L2 分布。跨臂 N group 也没有 entity mapping：协议只允许 same-side、same-pair 归并，fair index 没有 cross-side `FULL_MATCH/PARTIAL_MATCH` 实体关系。因此跨臂“重合/独有 N group 数”是 `N/A`，不能从相似描述推断；这是一项可观察性边界，不是零值。

#### 54-pair N 分布

下表的格式为 `raw N reports / N substantive groups`，来自 [current report decisions](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json)、[baseline combined decisions](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_combined_512_v3.json) 和两侧 group JSON 的确定性重算。`0/0` 表示该 side/pair 没有 final N。

| pair | current N reports / groups | baseline N reports / groups |
| --- | ---: | ---: |
| `0000` | 0 / 0 | 1 / 1 |
| `0001` | 2 / 1 | 0 / 0 |
| `0002` | 0 / 0 | 0 / 0 |
| `0003` | 0 / 0 | 3 / 3 |
| `0004` | 0 / 0 | 6 / 5 |
| `0005` | 0 / 0 | 0 / 0 |
| `0006` | 14 / 7 | 4 / 4 |
| `0007` | 0 / 0 | 5 / 5 |
| `0009` | 33 / 14 | 2 / 1 |
| `0010` | 1 / 1 | 0 / 0 |
| `0011` | 3 / 2 | 1 / 1 |
| `0012` | 0 / 0 | 1 / 1 |
| `0013` | 4 / 3 | 0 / 0 |
| `0014` | 0 / 0 | 0 / 0 |
| `0015` | 5 / 4 | 0 / 0 |
| `0016` | 1 / 1 | 1 / 1 |
| `0017` | 4 / 2 | 2 / 2 |
| `0019` | 32 / 12 | 6 / 5 |
| `0020` | 1 / 1 | 2 / 2 |
| `0021` | 3 / 2 | 1 / 1 |
| `0022` | 0 / 0 | 4 / 2 |
| `0023` | 6 / 3 | 0 / 0 |
| `0024` | 0 / 0 | 0 / 0 |
| `0025` | 4 / 3 | 1 / 1 |
| `0026` | 0 / 0 | 0 / 0 |
| `0027` | 0 / 0 | 4 / 4 |
| `0029` | 26 / 13 | 2 / 2 |
| `0030` | 0 / 0 | 0 / 0 |
| `0031` | 2 / 1 | 0 / 0 |
| `0032` | 0 / 0 | 3 / 3 |
| `0033` | 1 / 1 | 2 / 2 |
| `0034` | 3 / 1 | 0 / 0 |
| `0035` | 0 / 0 | 2 / 2 |
| `0036` | 8 / 5 | 13 / 13 |
| `0037` | 0 / 0 | 4 / 4 |
| `0039` | 28 / 15 | 1 / 1 |
| `0040` | 1 / 1 | 3 / 3 |
| `0041` | 4 / 2 | 2 / 1 |
| `0042` | 0 / 0 | 1 / 1 |
| `0043` | 1 / 1 | 0 / 0 |
| `0044` | 0 / 0 | 0 / 0 |
| `0045` | 0 / 0 | 3 / 3 |
| `0046` | 1 / 1 | 4 / 4 |
| `0047` | 0 / 0 | 1 / 1 |
| `0049` | 35 / 20 | 6 / 6 |
| `0050` | 0 / 0 | 0 / 0 |
| `0051` | 2 / 1 | 0 / 0 |
| `0052` | 0 / 0 | 2 / 2 |
| `0053` | 0 / 0 | 0 / 0 |
| `0054` | 0 / 0 | 0 / 0 |
| `0055` | 0 / 0 | 2 / 2 |
| `0056` | 2 / 1 | 0 / 0 |
| `0057` | 4 / 2 | 2 / 1 |
| `0059` | 0 / 0 | 8 / 8 |

### 6.5 NO_RERUN 决策

当前冻结结论是 `NO_RERUN`。evaluation-only audit 没有发现 FCSTM-only 或 compiler-owned 现象进入 current K/N；已经识别的 invalid-output 成本留在 report precision 分母，归因只在 conversion-attribution overlay 中处理。因此没有重新运行 method、provider、15x1、54x3、162-cell 或 replay，也没有重新进行人工裁定或改变 hit、W、D/A、K/N/I 或 canonical relation。

## 7. 结果解释

### 7.1 Coverage 的差异

current 的 FULL hit@1 比 baseline 高 `19.08 pp`（`71.26%` 对 `52.18%`）。差异在 L2 更大：hit@1 高 `47.01 pp`，hit@all 高 `64.10 pp`。在冻结输入和协议下，这与 source closure、source trace、FCSTM/pyfcstm inspection 以及适用时的可执行 predicate evidence 共同出现；它们为行为/全局问题提供了更多可定位和可复核的证据路径。该结果是覆盖比较，不是“ours 在所有指标、成本或模型范围上更好”的结论。

### 7.2 Precision 的 trade-off

current 的 report precision 是 `77.10%`，baseline 是 `81.45%`，差异为 `-4.34 pp`。current I 包含 D0、ordinary A0/`FALSE_POSITIVE` 和 current-only NADC；NADC 只是 current-side evaluation overlay，baseline 没有同构分类。在冻结协议下，current 以适度的 invalid-output burden 换取更高的 FULL discovery coverage。不能把 NADC 全部归因于 lowering/compiler，也不能据此断言 baseline 没有 representation/evidence cost。

### 7.3 Predicate 的实际使用

19 是设计规模；`12/19` 是产生 terminal receipt 的 distinct predicate IDs；`8/19` 是进入最终 report-bound finding 的 distinct IDs。设计来源、实际执行、最终绑定和对某个 finding 的证据作用是四件不同的事。前两项都不是 defect coverage、FULL hit、W2 数或贡献数；`825/1271` 与 `303/825` 也只是行级诊断。baseline 的对应字段为 N/A，因为不存在同构 receipt/binding schema。

### 7.4 `P => Q` 与高级谓词较少的原因

令 `P` 为 violation predicate，`Q` 为某个 defect 存在。本文采用 `P => Q`：`P` 的 sound violation 足以支持 `Q`，但 `P` 为真并不证明 `Q` 不存在，更不等于 `P <=> Q`。因此，已有低层结构或拓扑事实能够 soundly 证伪问题时，方法不强行升级到 trajectory simulation 或 BMC。

高级谓词使用较少至少有三类原因：已有 sound violation 已闭合；当前用例没有对应义务；当前 capability、typed input 或 runtime observation 不支持该 execution。未使用或 unsupported predicate 不能被统一归因于 `P => Q`，也不表示问题不存在。对后者，正确行为是保留 source-grounded finding 并 fallback 到 W1，必要时 W0。

### 7.5 N 的两侧构成

N 的 raw-to-group 结果表明，current 的 231 条 N reports 被保守归并为 121 个 pair-local group，而 baseline 的 105 条 N reports 对应 98 个 group。current 的压缩率较高，说明相同 pair 中存在更多跨 round 重复地报告同一共同义务/根因的情况；baseline 的 92 个 singleton group 说明当前证据不足以把其报告合并。这个差异可能同时受到台账不完整、报告粒度、候选冗余、方法能力和人工审核构成的影响。

由于不存在 cross-side entity mapping，不能把一侧 N 的相似表述称为另一侧的相同 defect，也不能据此声称某侧“发现更多真实缺陷”。同样，N 的多少不能直接推导 coverage 高低：必须先看 K 漏归、I 误归和 group 规则是否一致。N group 只用于保守地说明已记录的 novel-report 构成；其审计入口在第 6.4 节给出。

## 8. 学术口径、可写 claim 与限制

### 8.1 引用如何支撑本文

| 来源 | 本文采用的概念边界 |
| --- | --- |
| [IEEE Std 1044-2009](https://doi.org/10.1109/IEEESTD.2010.5399061) | defect/anomaly 的规格相对性；不逐字定义项目 D 档。 |
| [Porter, Votta & Basili 1995](https://doi.org/10.1109/32.391380) | known fault、true fault 与 false positive 的报告级区分。 |
| [Klees et al. 2018](https://doi.org/10.1145/3243734.3243804) | distinct bug 而非 raw crash/input 的最终单位。 |
| [Okun, Delaitre & Black, NIST SP 500-297](https://doi.org/10.6028/NIST.SP.500-297) | relatedness 的 direct/indirect/unrelated 层次。 |
| [Ahmed et al., MODELS 2025](https://doi.org/10.1109/MODELS67397.2025.00014) | same-root-cause equivalence 与人工确认的新真实 issue 的概念。 |
| [Pearson et al., ICSE 2017](https://doi.org/10.1109/ICSE.2017.62) | fault-level evaluation 对报告粒度和定位粒度的依赖。 |
| [Martinez et al., EMSE 2017](https://doi.org/10.1007/s10664-016-9470-4) | repair/semantic equivalence 只能作为归并的辅助边界。 |

本文的 L/W/D、relation、K/N/I 和 N grouping 是以这些概念为依据的 operationalization。19 个谓词的来源由 [predicate provenance](../paper_stm_issue_discover/related_work/provenance/predicate_provenance.md) 逐项记录，但不把项目内部调研夸大为已注册系统综述，也不把文献当作每条 finding 的运行时裁定者。

### 8.2 可以写的 claim

- 在冻结输入和协议下，current 的 FULL 与 L2 discovery coverage 高于 baseline。
- current 以 `4.34 pp` 的 report-level precision 差异换取更高 discovery coverage。
- current 的 FULL hits 中，`197/310` 的最高 W 为 W2。
- current 的 19-predicate registry 中，12 个 distinct IDs 产生 terminal receipt，8 个进入 report-bound finding；这两个指标有明确边界。
- source-first、人工裁定的 evaluation 保存 reason/basis、source refs、hash 与审计链，并由程序做确定性闭合。

### 8.3 不能写的 claim

- ours 在 precision、coverage、成本和所有维度都更好；
- NADC 的全部差异由 lowering/compiler 造成；
- baseline 没有 representation/evidence cost；
- `12/19` 或 `8/19` 等于缺陷覆盖率、W2 数或 hit 数；
- I cluster 是独立缺陷数，或 145 条 ledger 是绝对真值；
- 内部 reviewer/subagent 审阅构成新的 inter-rater 研究；
- 当前结果证明不存在问题、repair 已完成，或可外推到未声明的模型语义。

### 8.4 限制

145 条台账不是完整 defect universe。current/baseline 的人工审核构成不完全对称；N grouping 是 pair-local、conservative operationalization；I cluster 不是 defect 数；baseline 没有 predicate/NADC 同构 schema；N 的跨臂 entity overlap 目前不可观察。结论只适用于声明的模型范围、ledger、冻结 method 和 FCSTM soundness fragment。历史 v46、v27 和旧 X1v2 只保留为 archive/provenance，不进入 current headline。

## 9. 结论

Paper1 研究的是在给定自然语言需求和作者状态机后，发现并审计不一致的问题。冻结评测显示，current v4 在共同的 435 个 expected-round units 上取得更高 FULL discovery coverage，尤其在 117 个 L2 expected-round units 上更高；代价是 report-level precision 低 `4.34 pp`。predicate backend 在适用时把 source-grounded finding 提升为 W2，但不是所有 issue 的准入门。

后续工作是扩展可执行片段、改善 typed input 和 runtime evidence closure、在不改变 source-first 归因边界的前提下减少 invalid-output burden，并对尚不可观察的跨臂 N entity 关系建立独立、人工可审计的比较材料。repair 仍是后续研究方向，不是本篇实验结论。

## Appendix A. 离线复算、发布面与交接入口

本 talk 的实验事实回链到 [final-results archive README](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md)。该归档入口链接 current v4、baseline v3、fair comparison v4、正式报告、canonical JSON/TSV、[archive manifest](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/archive_manifest.json) 和 [publication manifest](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/publication_manifest.json)。字段、hash、闭合规则和 provider-free 复算入口见 [SCHEMA](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md)。

本次文档重构没有运行 provider、method、人工裁定、15x1、54x3、162-cell 或 replay；冻结结论保持 `provider_calls=0`、`billable_calls=0`、`method_reruns=0`、`judge_reruns=0` 和 `NO_RERUN`。动态 PR、branch、commit、required check 与 mergeability 状态以 GitHub PR 为事实源，不把它们复制为本文档中的第二份流程台账。
