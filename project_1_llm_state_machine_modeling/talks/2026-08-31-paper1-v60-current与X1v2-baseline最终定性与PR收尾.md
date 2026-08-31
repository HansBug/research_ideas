# Paper1：v60/current 与 X1v2 baseline v3 的最终定性与 PR 收尾

> 这是 Paper1 的实验结论和交班材料，不是导师原话，也不替代 [v4 中文正式报告](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。当前结果只来自 [final-results v4 归档](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md) 及其 canonical JSON/TSV；历史 v46、v27、v2、旧人工裁定记录和旧 witness audit 不属于当前 headline。

## A. 一页结论

current v4 在共同的 `145 expected issues x 3 rounds = 435 expected-round units` 上有更高的 FULL discovery coverage，也有更高的 L2 coverage；代价是 report-based precision 比 baseline v3 低 `4.34 pp`。因此不能写成 ours 在所有指标上都更好。

| 指标 | v60/current v4 | X1v2 baseline v3 | 口径 |
| --- | ---: | ---: | --- |
| method cells / reports | 162 / 1271 | 162 / 512 | 每侧 54 pair x 3 rounds；report 是原始 finding report |
| K / N / I reports | 749 / 231 / 291 | 312 / 105 / 95 | K/N/I report-level disposition |
| D2 / D1 / D0 / A0 reports | 721 / 259 / 120 / 171 | 342 / 75 / 85 / 10 | D/A report-level disposition |
| report precision | 980/1271 = 77.10% | 417/512 = 81.45% | `(K reports + N reports) / all reports` |
| FULL hit@1 | 310/435 = 71.26% | 227/435 = 52.18% | expected-round FULL units |
| FULL hit@3 | 119/145 = 82.07% | 106/145 = 73.10% | unique expected IDs hit in any round |
| FULL hit@all | 86/145 = 59.31% | 46/145 = 31.72% | unique expected IDs in all 3 rounds |
| supported coverage @1 / @3 | 337/435 = 77.47% / 128/145 = 88.28% | 264/435 = 60.69% / 119/145 = 82.07% | FULL 或 PARTIAL；不是主 FULL hit |
| L2 FULL hit@1 / @3 / @all | 105/117 = 89.74% / 37/39 = 94.87% / 33/39 = 84.62% | 50/117 = 42.74% / 26/39 = 66.67% / 8/39 = 20.51% | L2 分母分别为 39 x 3、39、39 |
| FULL-hit max W2 / W1 / W0 | 197/310 / 113/310 / 0/310 | 0/227 / 227/227 / 0/227 | 只在本侧 FULL hits 内按最高 W 统计 |
| K hits / N groups / I clusters | 119 / 121 / 189 | 106 / 98 / 95 | 三种单位不同；I cluster 不是 defect entity |
| predicate terminal usage | 12/19 | N/A | baseline 没有同构 predicate receipt schema |

表中数字由 [fair comparison v4 的 combined summary](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json)、[current v4 summary](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit/summary_v4.json) 和 [baseline v3 summary](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/summary_v3.json) 复算。`W2/W1/W0` 的分母是 FULL-hit units，不是全部 finding；baseline predicate usage 的 `N/A` 表示不适用，不是零。

## B. 问题定义和范围

Paper1 处理的输入是一条自然语言需求和一份作者 PlantUML 状态机。目标是发现需求、模型结构或可执行状态机语义之间的不一致，并保留 source-level、可追溯、可复核的 issue evidence。主线是 issue discovery；repair 不是本篇实验目标，只是后续方向。

当前模型对象可写为 `M = (S, E, V, Tr, A)`，覆盖离散 FSM、层次状态机和带变量/guard/action 的 EFSM 子集。本文明确不外推到 clocks、invariants、orthogonal/concurrent regions、hybrid/unbounded temporal properties 或其他执行模型，也不把 145-item ledger 之外的缺陷宇宙当成已覆盖。完整边界见 [model_scope.md](../paper_stm_issue_discover/story/model_scope.md)。

台账是研究者依据自然语言、作者模型和来源证据维护的 source-backed expected inventory，是命中率的分母，不宣称穷尽所有领域缺陷。`D1` 存在多种完整读法时，最终读法必须保留 ambiguity 和敏感性；不能用参考模型、method finding 或旧 expected mapping 反向补全原文没有的信息。

## C. 方法设计

### C.1 数据和执行顺序

当前方法的证据链按以下顺序组织：

```text
NL + 作者 PlantUML
  -> canonical source IR / source trace
  -> FCSTM working representation
  -> pyfcstm native / inspection facts
  -> predicate routing and typed execution
  -> method evidence and receipts
  -> 人工 validity/relation 裁定
```

`method/` 保存冻结的证据发现方法和 19-predicate runtime；`judge/` 保存 issue #195 下人工完成的 report validity/relation 裁定入口；`evaluation/` 负责 provider-free 的机械汇总、归并、指标、manifest 和审计。Paper1 中所有 validity、relation、D/A、K/N/I 与成分分析判断均由人工完成，机器只读取人工裁定制品并按既定闭合规则做一致性校验和算术复算。`pyfcstm/FCSTM` 是获得可执行检查能力的中间介质，不单独构成 Paper1 的 novelty。PlantUML 到 FCSTM 是内部 projection；projection、compiler-owned element 或未闭合 runtime evidence 必须回到作者 source 后才能归因于作者模型。

本文的责任主体口径固定为：凡涉及的 judge、validity、relation、D/A、K/N/I 和成分分析，均由人工完成，并以带有 reason、basis、source refs 和审计记录的人工裁定为准。程序只负责读取已完成的人工记录、确定性闭合、hash/link/schema 检查和算术复算，不承担新的裁定；内部 reviewer/subagent 记录也只是质量审阅证据，不被表述为独立的人类 inter-rater 研究。

19 个谓词来自状态机、形式化验证和执行语义相关调研，分为 Structure（6）、Topology（4）、Trajectory simulation（4）和 Bounded verification（5）四族。current v4 中有 12/19 个 distinct predicate IDs 产生过 terminal receipt，8/19 个 distinct IDs 出现在至少一条 report-bound finding 中；这两个数分别是 ID 级执行和 ID 级绑定指标，不是 defect coverage、W2、hit 或 predicate contribution。baseline 没有同构 schema，故为 N/A。旧 registry 中的 `118/145` 只能叫冻结设计期 planned snapshot，不能叫已验证的逐项 gold coverage；谓词后端审计的 evaluation-only 入口是 [predicate gold README](../paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/README.md)。

### C.2 证据强度

W0/W1/W2 是独立证据轴。W2 要求准确制品上的合法 executable object、typed input、精确 artifact hash、backend terminal true/false 和完整 receipt；W1 有具体模型元素或路径但没有完整 terminal receipt；W0 只有散文主张。W 不决定 D/A 或 K/N/I。建立一个缺陷存在通常只需要 source-backed 的 sound violation 或具体反例；静态证据已经闭合时，不为形式完整性强行升级到仿真或 BMC。

`report-bound binding rows` 与 distinct predicate IDs 也不能混用。current 的 `825/1271 = 64.91%` 是逐 report 的 binding-row 诊断，`303/825 = 36.73%` 是这些行中遗留 `coverage_class` marker 的比例；它们都不能替代 12/19、8/19、W2 数或 hit 数。

## D. issue #189 / #195 的学术定义和裁定闭合

本节把两个 issue 的关键约束写在 talk 内，详细讨论分别见 [issue #189](https://github.com/HansBug/research_ideas/issues/189) 和 [issue #195](https://github.com/HansBug/research_ideas/issues/195)。它们不是新的数据源，而是 current v4 与 baseline v3 共同依赖的评测边界。

### D.1 issue #189：source-first 的发现与证据定义

issue #189 解决的是“报告说模型有问题”之前，什么才算一个可审计的 defect claim。判断顺序固定为：

1. 先读完整的作者 NL 与作者 PlantUML，确认作者 source fact、source locus、主体和实际语义；
2. 再判该 fact 是否违反作者需求中的 obligation，并区分需求没有成立、模型没有违反义务、事实本身不成立和归因落在方法内部表示等情况；
3. 只有 source fact、义务、归因和证据链闭合，才把 finding 作为 source-level issue 进入后续 relation/KNI 评测。

因此，FCSTM、compiler/lowering 或 runtime trace 只能提供执行证据和定位线索，不能单独定义作者模型缺陷。投影后的 element 若不能经 source trace 回到作者制品，不能进入 current K/N；它可以作为方法 invalid-output 的诊断，计入 report precision 分母。`D2/D1/D0/A0` 是对“事实与被违反义务”的裁定轴，不是 W 或 predicate 的同义词：D2 表示 source fact 成立且有明确被违反义务；D1 表示 source fact 成立，但至少两种完整且与 source 相容的读法仍会改变义务或归因判断；D0 表示 source fact 成立但没有 surviving violated obligation；A0 表示报告事实或归因在完整作者制品上不成立。D0、A0 都必须进入 I，不能因为模型事实存在就把它们当作 K。

### D.2 issue #195：独立 validity 与 relation

issue #195 要求把报告“是否成立”和“它对应哪个 expected issue”分开。所有 validity、relation、D/A、K/N/I 和成分判断均由人工完成：人工先在完整 source-first validity certificate 下判报告是否成立，再判合法报告与外部 expected ledger 的 relation；评测程序只按这些人工记录和冻结规则确定性生成最终字段与指标，不承担新的语义判断。方法不能读取 expected ledger、人工裁定输出或历史结果来改变自己的 finding。relation 只允许以下三个值：

| relation | 学术含义 | 指标去向 |
| --- | --- | --- |
| `FULL` / `FULL_MATCH` | 与 expected 的 source/context 相容，并满足至少一项：同一缺陷实例、同一根因、同一被违反义务，或同一根因的直接可归因表现 | 贡献主 hit |
| `PARTIAL` / `PARTIAL_MATCH` | 报告支持较宽义务或同一问题家族，但没有证明是该 expected 实例 | 进入 supported coverage，不贡献 FULL hit，不是 FP |
| `NO` / `NO_MATCH` | 没有可接受的 expected relation | D2/D1 全 NO 时为 N；I 仍为 invalid |

`K/N/I` 的闭合顺序因此是 `作者 source fact -> D/A -> 全部 expected relation -> K/N/I`：D2/D1 加至少一个可接受 positive relation 进入 K；D2/D1 对全部 expected 都是 NO 进入 N；D0/A0 直接进入 I。N 不是“未命中就算一个新缺陷”，而是有效但未能认领现有 expected 的报告；I 也不是 291 个独立缺陷。

expected ledger 是 source-backed expert-annotated inventory，不是穷尽整个 defect universe。K 按 expected ledger ID 去重；N 只有在同一 side、同一 pair 内，同时共享 substantive obligation、source locus/root cause、property 和最小修复意图时才归并，不能跨 pair/side、按文本相似度、状态名或 expected ID 自动合并。I 不建立 substantive defect group，I cluster 只是 invalid diagnostic。这样既保留 raw report 的审计粒度，也避免把 raw report、expected ID、N group 和诊断 cluster 误称为同一实体。

### D.3 公平比较和证据轴

current 使用 `issue-189-195-manual-evidence-v2`；baseline 非 K 重审使用 `issue-189-195-baseline-ni-v3`。两者都遵守上述语义边界，但 baseline v3 的原有 279 个 K 是冻结快照，不能把 baseline v3 叙述成与 current 同深度的新一轮全盲人工实验。W0/W1/W2 独立于 D/A、relation、K/N/I：它只描述可重放证据强度；`FULL` 是主 hit，`PARTIAL` 是 supported coverage，`NO` 不是 hit。主 precision 只按 report 计算，任何 ledger/group ratio 都必须单独叫 diagnostic composition。完整 protocol、字段定义、版本和 hash 入口见 [final-results SCHEMA](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md)。

## E. 实验设计和评测协议

冻结实验是 `54 pair x 3 rounds`，每侧 `162 cells`，expected inventory 有 `145` 条，hit@1 的分母为 `435`。current v4 是既有 pane5 source-first 结果的 raw/source/hash/relation 再验证，不宣称新一轮 1271 条独立 inter-rater 人工实验；baseline v3 是原非 K 的 233 条逐条重审加原有 279 条 K 的冻结快照，也不是新的 provider 实验。

两侧先读作者 source 和原始 report，再判 D/A 和 relation，最后机械闭合 K/N/I，并只对 N 做 substantive grouping：

| 层 | 规则 |
| --- | --- |
| relation | `FULL` 与 expected 的 source/context 相容，并满足至少一项：同一缺陷实例、同一根因、同一被违反义务，或同一根因的直接可归因表现；`PARTIAL` 是支持同一较宽义务/家族但不足以确认上述对应关系；`NO` 是没有可接受关系。PARTIAL 可以进入 supported coverage，不进入主 FULL hit；NO 不是 hit。 |
| D/A | D2/D1 表示 source fact 成立且存在对应 violated obligation；D0 表示 source fact 成立但没有 surviving violated obligation；A0 表示报告事实或归因在完整作者制品上不成立。D0/A0 都进入 I。 |
| K/N/I | D2/D1 加 positive relation 进入 K；D2/D1 且对全部 expected relation 为 NO 进入 N；D0/A0 进入 I。 |
| K unit | 按 expected ledger ID 去重；重复命中同一 expected ID 不增加 K hit。 |
| N unit | 只在同一 side、同一 pair 内，依据共同义务、source locus/root cause、property 和最小 repair intent 归并；不跨 side/pair，不按文本相似度、状态名或 expected ID 自动合并。singleton 只表示没有证据支持合并，不是已证明的独立缺陷。 |
| I unit | I 是 report-level invalid disposition；I cluster 只描述重复形态，不是实质缺陷实体，不进入 substantive grouped precision。 |
| precision | 主 precision 是 report-based：`(K reports + N reports) / all reports`。任何 ledger/group ratio 都单独称为 diagnostic composition，不叫主 precision。 |

W-on-hits 的统计使用每个 FULL hit unit 内最高 W 等级。hit@1 是 expected-round units；hit@3 是三轮任一 FULL 的 expected IDs；hit@all 要求三轮均 FULL。L2 只把 39 条 L2 expected issues 放入对应分母。D/A、K/N/I、W 和 predicate usage 属于不同轴，不能互相替代。

## F. 完整结果和成分分析

### F.1 报告、D/A、K/N/I

| 项目 | current v4 | baseline v3 | 说明 |
| --- | ---: | ---: | --- |
| reports | 1271 | 512 | raw report 分母 |
| K / N / I reports | 749 / 231 / 291 | 312 / 105 / 95 | K/N/I report units |
| D2 / D1 / D0 / A0 | 721 / 259 / 120 / 171 | 342 / 75 / 85 / 10 | D/A report units |
| N D2 / D1 reports | 38 / 193 | 50 / 55 | N 内的 D tier |
| substantive N groups | 121 | 98 | N grouping unit |
| diagnostic I clusters | 189 | 95 | invalid diagnostic，不是 defect 数 |

current 的 N 组大小为 `1:52, 2:31, 3:36, 4:1, 5:1`；baseline v3 为 `1:92, 2:5, 3:1`。这两行是同侧的 grouping composition，不是 raw report 数，也不是跨臂因果解释。

### F.2 I 组成和 NADC overlay

| I 成分 | current v4 | baseline v3 |
| --- | ---: | ---: |
| D0 | 120 | 85 |
| ordinary A0 / `FALSE_POSITIVE` | 53 | 10 |
| current-only A0 / `NOT_A_DEFECT_CLAIM` (NADC) | 118 | N/A，baseline v3 无同构分类 |
| I reports | 291 | 95 |

current I 的 `291 = 120 + 53 + 118`。NADC overlay 只作用于 current-side invalid reports，把 118 条分为 compiler-owned `38`、projection/trace `24`、runtime/evidence closure `48`、indeterminate `8`；前 110 条是确认的 method-owned mechanisms，strict lowering-only confirmed 为 `0`。来源是 [conversion attribution v1 overlay](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/README.md) 和其 [summary JSON](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/i_attribution_summary_v1.json)。

这不能被写成“全部差异由 lowering/compiler 造成”：baseline v3 没有同构 NADC subtype，不能把 baseline 缺失机械写成 0，也不能据此证明 baseline 没有 representation/evidence cost。NADC 也不等于所有 I，更不等于 conversion debt。

### F.3 Precision 差距

主 precision 为 current `980/1271 = 77.10%`、baseline `417/512 = 81.45%`，差异 `-4.34 pp`。互补的 I rate 为 current `291/1271 = 22.90%`、baseline `95/512 = 18.55%`，差异 `+4.34 pp`。按各自 report 分母做描述性分解：D0 率差为 `120/1271 - 85/512 = -7.16 pp`，ordinary FP 率差为 `53/1271 - 10/512 = +2.22 pp`；NADC 只报告 current-side `118/1271 = 9.28%`，因为 baseline 不可比。把缺失 baseline cell 当作机械 0 的 `+9.28 pp` 只是 bookkeeping residual，不是 causal estimate。

### F.4 Predicate 和 W

current terminal receipt 的 12/19 distinct IDs 是 `G1, G2, G4, R1, R2, R4, S1, S2, S3, S4, S5, V4`；report-bound 的 8/19 是 `G1, G2, R2, S2, S3, S4, S5, V4`。baseline 为 N/A。current report-bound rows 为 `825/1271 = 64.91%`，其中 legacy `coverage_class` markers 为 `303/825 = 36.73%`，两者仅作行级诊断。

FULL-hit max W 的 current 为 W2/W1/W0 `197/310, 113/310, 0/310`；baseline 为 `0/227, 227/227, 0/227`。这些分母分别是本侧 FULL hit 数 `310` 和 `227`。不能拿全部 finding 的 W 分布替代这张表。

### F.5 NO_RERUN

本轮结论是 `NO_RERUN`。审计没有发现 FCSTM-only 或 compiler-owned 现象进入 current K/N；已有 invalid 成本已进入 report precision，归因可以放在 evaluation-only overlay 中完成。因此没有重新运行 method、provider、15x1、54x3 或 162-cell 实验，也没有重新进行人工裁定或改变 hit、W、D/A、K/N/I 或 canonical relation。

## G. 学术口径、可写 claim 和限制

### G.1 文献依据和项目 operationalization

issue #189/#195 的“学术定义”不是把某个后验分数直接当作真值，而是把来源、义务、观察和裁定顺序写清楚。本文采用的底层依据如下；每条只承担表中注明的边界，项目自己的状态、分组和仲裁规则仍标为 operationalization。

- Dwyer, Avrunin & Corbett, *Patterns in Property Specifications for Finite-State Verification*, ICSE 1999, DOI [10.1145/302405.302672](https://doi.org/10.1145/302405.302672)，publisher abstract：支持将有限状态性质按可复用 pattern 组织；不逐字规定本项目的 issue 义务或 K/N/I。
- Giannakopoulou et al., *Formal Requirements Elicitation with FRET*, CEUR-WS 2584, 2020, [PDF pp. 1-5, §§1-3](https://ceur-ws.org/Vol-2584/PT-paper4.pdf)（NASA [NTRS 20200001989](https://ntrs.nasa.gov/citations/20200001989)）：支持把 component、scope、condition、timing、response 分开形式化，并用 trace/语义检查 formalization；不证明作者未写出的意图或本项目的人工裁定结果。
- Barr et al., *The Oracle Problem in Software Testing: A Survey*, IEEE TSE 2015, DOI [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785)，§2.3、Definitions 2.6-2.8，printed p. 510：支持区分完整 oracle 与 partial/sound oracle；不把一次执行结果自动升级为义务等价。
- Beer et al., *Efficient Detection of Vacuity in Temporal Model Checking*, Formal Methods in System Design 2001, DOI [10.1023/A:1008779610539](https://doi.org/10.1023/A:1008779610539)，作者机构 abstract：说明蕴含前件不可满足时性质可能平凡成立，因此执行结果要检查 vacuity；不为本项目任意非时序组合性质提供通用判据。
- Tretmans, *Model Based Testing with Labelled Transition Systems*, 2008, DOI [10.1007/978-3-540-78917-8_1](https://doi.org/10.1007/978-3-540-78917-8_1)，abstract 与 §1，pp. 1-2：支持把实现相对 required-behavior model 的 conformance 与可观察执行分开，并承认测试不能一般性证明没有错误。
- OMG, *OMG Unified Modeling Language (OMG UML), Version 2.5.1*, formal/2017-12-05, [official PDF](https://www.omg.org/spec/UML/2.5.1/PDF)，pp. 307、312-317、346、350，Clauses 14.2.3.2、14.2.3.6、14.2.3.7、14.2.3.9.1、14.5.2.1、14.5.2.5、14.5.6.7：支持 initial pseudostate、completion、run-to-completion 和 terminate 的 UML 语义边界；本文不把 FinalState、leaf state、无出边状态和全局 termination 混为一谈。
- Abadi & Lamport, *The Existence of Refinement Mappings*, Theoretical Computer Science 1991, DOI [10.1016/0304-3975(91)90224-P](https://doi.org/10.1016/0304-3975(91)90224-P)，author-hosted report §2.4, printed p. 11：支持用行为包含/映射明确 implication 方向；单向 implication 不能被写成 equivalence。
- Harel & Naamad, *The STATEMATE Semantics of Statecharts*, TOSEM 1996, DOI [10.1145/235321.235322](https://doi.org/10.1145/235321.235322)，§2, pp. 298-299：支持把状态机行为写成由 stimuli、statuses 和 steps 构成的 runs；不把 STATEMATE 的并发或时间语义直接转移给 UML/PlantUML/pyfcstm。
- Biere et al., *Symbolic Model Checking without BDDs*, TACAS 1999, DOI [10.1007/3-540-49059-0_14](https://doi.org/10.1007/3-540-49059-0_14)，§§1、6, pp. 194、205：支持把 bounded counterexample 与无界证明区分；没有 completeness bound 时，有限范围内未找到反例不是无界性质证明。Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15)，§1, pp. 154-155：支持把抽象反例回放到 concrete model，排除 spurious witness。

- IEEE Std 1044-2009, *IEEE Standard Classification for Software Anomalies*, DOI [10.1109/IEEESTD.2010.5399061](https://doi.org/10.1109/IEEESTD.2010.5399061)：支撑 anomaly classification/disposition 和 intended-behavior 相关术语，不逐字规定本项目的 K/N/I。
- Porter, Votta & Basili, *Comparing Detection Methods for Software Requirements Inspections: A Replication Using Professional Subjects*, IEEE TSE 1995, DOI [10.1109/32.391380](https://doi.org/10.1109/32.391380)：支撑 true fault、false positive 和已知问题区分；不提供本项目的 report precision 公式。
- Klees et al., *Evaluating Fuzz Testing*, CCS 2018, DOI [10.1145/3243734.3243804](https://doi.org/10.1145/3243734.3243804)：支持 distinct bugs 与 raw reports 需要区分；不直接定义本项目 N grouping。
- Okun, Delaitre & Black, *Report on the NIST Static Analysis Tool Exposition (SATE) IV*, NIST SP 500-297, DOI [10.6028/NIST.SP.500-297](https://doi.org/10.6028/NIST.SP.500-297)：支持按 directly/indirectly/unrelated relatedness 讨论报告关联；不直接给出本文的 pair-local root-cause rule。
- Ahmed et al., *MCeT: A Model Checking and Testing Framework for Behavioral Models*, MODELS 2025, DOI [10.1109/MODELS67397.2025.00014](https://doi.org/10.1109/MODELS67397.2025.00014)：支持 equivalent issue 与人工确认 new true issue 的区分；本文不把内部 reviewer QA 写成正式 inter-rater study。
- Pearson et al., *A Large-Scale Study of the Impact of Report Granularity on Fault Localization*, ICSE 2017, DOI [10.1109/ICSE.2017.62](https://doi.org/10.1109/ICSE.2017.62)：说明 report granularity 会影响 fault decomposition；不证明本项目的 121/98 group count 是唯一分解。
- Martinez et al., *Astor: Exploring the Design Space of Generate-and-Validate Program Repair beyond GenProg*, EMSE 2017, DOI [10.1007/s10664-016-9470-4](https://doi.org/10.1007/s10664-016-9470-4)：用于说明 semantic/repair equivalence 不等于 patch 文本相同；本文不声称 repair 已完成。

这些来源分别支撑 anomaly disposition、false-positive/true-fault 区分、distinct bug、relatedness、报告粒度和等价性边界。“同 side + 同 pair + 共同义务 + source/root cause + 最小修复意图”是基于这些概念形成的 Paper1 operationalization，不是某一篇文献逐字给出的完整标准。本文也没有找到“most precise predicate”统一的学界层级定义；predicate 的使用和证据强度必须逐条看 scope、量词、timing、观察粒度和 source attribution。

### G.2 可以写的 claim

1. 在冻结输入和协议下，ours 的 overall FULL/L2 discovery coverage 高于 baseline v3。
2. ours 以 `4.34 pp` 的 report-level precision 差异换取更高 discovery coverage，这是当前 operating-point trade-off。
3. current FULL hits 中 `197/310` 的最高 W 是 W2。
4. 19-predicate registry 有外部学术来源；current 12 个 distinct IDs 产生 terminal receipt，8 个 distinct IDs 进入 report-bound finding。
5. source-first、manual-supervised evaluation 保存 reason/basis、source refs、hash 和审计链。

### G.3 不可以写的 claim

- ours 在 precision、coverage、成本和所有维度都更好；
- NADC 的全部差异由 lowering/compiler 造成；
- baseline 没有 representation/evidence cost；
- 12/19 或 8/19 等于 defect coverage、W2 或 hit 数；
- I cluster 是独立缺陷数，或 145 条台账是绝对真值；
- reviewer/subagent PASS 是新的人工 inter-rater study；
- 当前结果证明不存在问题、repair 已完成，或结果可以外推到未声明的模型语义。

### G.4 限制

主要敏感性包括：current 继承既有 source-first review chain；baseline v3 与 current 的人工复核深度并不完全对称；N grouping 有 conservative boundary；I cluster 是 invalid diagnostic；baseline 没有 current predicate/NADC 同构 schema；模型范围不含时钟、不变式、正交并发、hybrid 和无界性质；台账不是完整 defect universe。结论只外推到声明的 ledger、模型范围、冻结 method 和相应 FCSTM soundness fragment。

## H. 复现、发布面和 PR 收尾

### H.1 当前唯一入口

```text
project_1_llm_state_machine_modeling/talks/README.md
  -> 本 talk
  -> final_results/.../report/v60_current_vs_x1v2_baseline_v4_cn.md
  -> final_results/.../README.md
  -> current v4 / baseline v3 / fair v4 canonical JSON/TSV and manifests
```

发布面只包含 current v4、baseline v3、fair v4、conversion attribution v1 的必要 schema/summary/manifest/review 和正式报告。raw、reference、旧 v2、旧人工裁定记录、旧 witness audit 继续由 archive/provenance 入口绑定，不能被默认导航当作 current fact source。逐条 evaluation gold 的入口是 [predicate_gold_v1](../paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/README.md)，它不进入 method prompt、routing、registry runtime、测试输入或 discovery context。

### H.2 Provider-free 命令

以下命令只读冻结制品或生成 evaluation-only 派生验证：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_current_reaudit_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_baseline_v3.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_fair_comparison_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only

venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_conversion_attribution_v1.py --repo-root .
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src venv/bin/python -m paper_stm_evaluation.final_results_archive validate --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --repository-root .
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/validate_release_structure.py
```

### H.3 交班状态

- branch：`paper1/m-witness-discovery`；开始本次 closeout 时 HEAD 为 `9b512558123f305971e16746b9b48560c832cd6f`，远端同 hash。最终提交和 push hash 以 sessionlog 与 PR comment 的最后复核为准。
- 本次修改范围：talks 入口/状态导航、历史 banner、本最终 talk、release documentation audit 的 HEAD-specific review、受控 documentation exception 和由 authoritative finalizer 更新的 publication/archive manifest；未修改 raw、reference、canonical decision/relation、registry、method 实现或实验输入。
- 执行纪律：`provider_calls=0`、`billable_calls=0`、`method_reruns=0`、`judge_reruns=0`，并且没有运行 15x1、54x3、162-cell 或 replay。
- PR #193 的目标是从旧 v25 Draft 叙事收敛到 v4 release/documentation closeout；是否 Ready、required checks 和 mergeability 以 push 后 GitHub 只读复核为准。

最终交班应同时提供：三轨 numeric/provenance、semantic/fairness、documentation/navigation/academic review；`shuorenhua` 的 protected-span 清单、保真回读和最小润色记录；current/baseline/fair/conversion/archive/release validator 输出；protected-file 对拍；最后 commit、remote hash 和 PR mergeability。无论文风如何调整，数字、单位、路径、协议、限定词、责任主体和“不重新运行”的边界都必须保持不变。
