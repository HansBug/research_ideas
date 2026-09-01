# Predicate-gold Academic Pilot Review

**Review verdict: FAIL**

本轮只审查 academic provenance 与协议证据，不做 145 条标注，不读取任何 v60 actual predicate/input 输出，也不运行 method、judge 或实验网格。完整机器可读矩阵见 [academic_claim_to_source_matrix.json](../academic_claim_to_source_matrix.json)。

## 判定

用户点名的 Dwyer ICSE 1999、FRET/FRETish、Barr oracle、Beer vacuity、Tretmans MBT、OMG UML 2.5.1，以及 refinement、trace semantics、bounded model checking、counterexample validity 均已找到正式来源并建立有限 claim。Dwyer、Barr、Beer 原有的 claim-level `NEEDS_SOURCE` 已用精确一手 PDF 页或精确 publisher/author-institution HTML section 关闭，因此 `named_source_coverage = PASS` 且 `needs_source_rows = []`；但 `protocol_evidence_closure = FAIL`：这些来源能支撑结构化 O、方向性 oracle/refinement、vacuity、模型有效性前提、RTC/initial 语义、bounded 结论和 counterexample concrete check，却不能直接证明本项目的三轨盲审、pane5 仲裁和正控构造本身有效。

本次 `FAIL` 是“在进入 145 条正式标注前，协议学术出处与验证尚未闭合”，不是任何 item-level gold verdict，也不是对 frozen 19 predicates 或 145 条台账的效果结论。

## 协议证据边界

| 协议动作 | 可用一手证据 | 允许的项目落法 | 不允许的外推 |
|---|---|---|---|
| 先规范化 O，再提议 P | Dwyer [1]；FRET [2] | 显式记录 component/scope/condition/timing/response 与 missing information | 不能把 pattern/FRETish 直接当作 145 条 gold 或声称词表完备 |
| 明确 O/P 方向 | Barr [3]；Abadi-Lamport [7] | `EQUIVALENT` 要求双向蕴含；`O_IMPLIES_P` 只可作 defective-side sound false proxy | 不能把相似、可执行或单向包含写成等价 |
| 检查 vacuity | Beer [4] | 检查 antecedent activation 与 observation-window reachability；量化谓词的 domain-nonempty guard 属项目扩展 | Beer 不证明本项目正控构造有效、domain 扩展充分或 contamination-free |
| 分离 source authority 与 execution receipt | Tretmans [5]；Barr [3] | 先由 author source 建 O，再在精确 artifact 上执行预冻结 P | receipt 不能修复错误 O、错误 mapping 或不完整 domain |
| 固定状态机语义剖面 | UML [6]；Harel-Naamad [8] | 区分 initial/RTC/dispatch/discard/consume/step/status，逐命题引用 | UML、STATEMATE、PlantUML、pyfcstm 不能整体系等同 |
| 限定 bounded 结论并核验反例 | Biere 等 [9]；Clarke 等 [10] | 记录 k/domain/model hash；反例须在 exact artifact 与同一 profile 上 replay | `no cex <= k` 不是无界证明；replay 也不自动证明 O/P 等价 |

## 高严重度缺口

### ACADEMIC-GAP-001：三轨盲审与 pane5 仲裁没有方法学出处或本地有效性证据

Barr [3] 给出了 ground-truth oracle、soundness 和 completeness 的定义，但没有证明“三个内部 reviewer + pane5”具有独立性，也没有证明这种仲裁优于单 reviewer、majority vote 或专家复核。若论文要把该结构表述成可信度方法，而非纯工程流程，必须补 primary methodology source，或做事前登记的 reviewer-agreement / adjudication validation；在此之前只能写成 project-engineered protocol。

### ACADEMIC-GAP-002：正控机制只得到 vacuity 动机，未得到构造有效性

Beer [4] 支持检查 antecedent failure 与 trivial pass，但不支持“minimal repair / repaired artifact 正控能发现错绑定”，更不支持 contamination check 的充分性。正式 Track C 不能把“正控返回 true”单独写成 gold 可信性证据；必须同时保留正控选择先验、语义等价理由、非空/可达检查和未观察 defective verdict 的证据，并补独立验证来源或实验。

### ACADEMIC-GAP-004：不同形式体系不能被拼成一个“共同状态机语义”

UML [6]、STATEMATE [8]、ioco/LTS [5] 与 SAT-BMC [9] 的 semantic object、step、observation 和 closure 条件不同。尤其 UML 明确允许“无 initial Pseudostate 时无统一处理”，并区分 dispatched-discarded 与 transitions-finished-consumed；因此 missing-initial 和 event-consumption gold 必须绑定明确 profile。任何把这些来源整体互换、或用一个 backend receipt 代替 source-to-semantics mapping 的做法都会破坏 item-level exactness。

## 已解决的来源缺口

`ACADEMIC-GAP-003` 已解决。Dwyer [1] 现定位到 IEEE Xplore `Abstract`，短引文只支撑 pattern-based codification/reuse；其正文 PDF 未读取，因此不据此声称 detailed pattern/scope taxonomy 完备。Barr [3] 现定位到开放许可 IEEE PDF 印刷页 510、Section 2.3、Definitions 2.6-2.8，PDF SHA-256 已记入矩阵。Beer [4] 已改为用户指定的 FMSD 2001 期刊版本，定位到 IBM Research 作者机构页 `Abstract`；该引文只直接支撑 antecedent failure 导致 trivial validity，不支撑本项目的正控或 contamination 机制。两项 HTML 证据均不推猜 PDF 页码。

## 进入正式标注前的门

1. 为三轨盲审/pane5 与正控构造补方法学 primary source 或事前登记的本地 validation protocol，并明确其只验证流程可靠性，不生成 item truth。
2. 冻结 proposition-specific semantic profile：UML/STATEMATE/FCSTM 每条只引用真正匹配的 clause，缺映射时返回 `UNSUPPORTED_EXACT` 或 `UNKNOWN`。
3. Track C 对 BMC/trace 继续执行 exact artifact hash、同 profile replay、bound/domain closure；这些是必要条件，不是 O/P 等价的替代品。

## References

[1] Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. 1999. “Patterns in Property Specifications for Finite-State Verification.” In *Proceedings of the 21st International Conference on Software Engineering (ICSE '99)*, 411-420. ACM. https://doi.org/10.1145/302405.302672

[2] Dimitra Giannakopoulou, Thomas Pressburger, Anastasia Mavridou, Julian Rhein, Johann Schumann, and Nija Shi. 2020. “Formal Requirements Elicitation with FRET.” In *Joint Proceedings of REFSQ-2020 Workshops, Doctoral Symposium, Live Studies Track, and Poster Track*, CEUR-WS Vol. 2584, PT-paper4. https://ceur-ws.org/Vol-2584/PT-paper4.pdf

[3] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. 2015. “The Oracle Problem in Software Testing: A Survey.” *IEEE Transactions on Software Engineering* 41(5): 507-525. https://doi.org/10.1109/TSE.2014.2372785

[4] Ilan Beer, Shoham Ben-David, Cindy Eisner, and Yoav Rodeh. 2001. “Efficient Detection of Vacuity in Temporal Model Checking.” *Formal Methods in System Design* 18(2): 141-163. https://doi.org/10.1023/A:1008779610539

[5] Jan Tretmans. 2008. “Model Based Testing with Labelled Transition Systems.” In *Formal Methods and Testing*, LNCS 4949, 1-38. Springer. https://doi.org/10.1007/978-3-540-78917-8_1

[6] Object Management Group. 2017. *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. Document formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/PDF

[7] Martín Abadi and Leslie Lamport. 1991. “The Existence of Refinement Mappings.” *Theoretical Computer Science* 82(2): 253-284. https://doi.org/10.1016/0304-3975(91)90224-P

[8] David Harel and Amnon Naamad. 1996. “The STATEMATE Semantics of Statecharts.” *ACM Transactions on Software Engineering and Methodology* 5(4): 293-333. https://doi.org/10.1145/235321.235322

[9] Armin Biere, Alessandro Cimatti, Edmund M. Clarke, and Yunshan Zhu. 1999. “Symbolic Model Checking without BDDs.” In *Tools and Algorithms for the Construction and Analysis of Systems (TACAS 1999)*, LNCS 1579, 193-207. Springer. https://doi.org/10.1007/3-540-49059-0_14

[10] Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2000. “Counterexample-Guided Abstraction Refinement.” In *Computer Aided Verification (CAV 2000)*, LNCS 1855, 154-169. Springer. https://doi.org/10.1007/10722167_15
