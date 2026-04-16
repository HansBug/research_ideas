# Expert Review V1 TODO

本文档是 `expert_review` 的 **v1 分阶段执行总表**。它不是一次性“大重写”计划，而是一个**逐阶段、局部调整、持续可运行**的重构与对齐路线图。

本路线图的硬约束如下：

1. 每个 phase 都只能在当前 `expert_review` 可运行实现的基础上做局部修改、调整和扩充。
2. 每个 phase 完成后，`expert_review` 必须继续保持完整可运行状态。
3. 每个 phase 完成后，新的代码必须真实接入运行路径，不允许明显不可达的新代码。
4. 每个 phase 完成后，都必须在当期架构能力边界内做一次对齐评测。
5. 每个 phase 都必须完整记录该阶段的对齐指标、改进点、退化点和剩余问题。
6. 最终在最后一个 phase 完成后，内部 reviewer 架构需要整体达到 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md) 所定义的 v1 目标形态。

推荐阅读顺序：

1. 先读 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
2. 再读 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md)
3. 最后读本文

## 1. 当前基线

当前基线版本：`dev/reviewer` 分支上 PR #6 创建时的实现

当前代码状态：

1. 已保留外部接口兼容：
   - `ExpertReviewRequest`
   - `ExpertReviewResult`
   - `review_artifacts()`
   - `review_model()`
   - `python -m expert_review`
2. 已完成初版 v1 风格运行时骨架：
   - contract router
   - evidence regime estimator
   - artifact dossier
   - traceability analysis
   - equivalence and difference analysis
   - pragmatic quality analysis
   - missing-evidence critic
   - score composer / final synthesizer
3. 已新增离线自我迭代 harness，但 benchmark 仅用于外环评测，不进入 reviewer 运行时依赖。

当前基线对齐指标：

| 指标 | 当前值 |
|---|---:|
| `HAI` | `66.16` |
| `RAS` | `59.91` |
| `SAS` | `62.85` |
| `PDS` | `87.50` |
| `normalized_mae` | `0.2119` |
| `equivalence_false_reject_rate` | `0.1250` |
| `unsupported_claim_rate` | `0.5508` |
| `summary_only_element_claim_rate` | `0.0000` |
| `protocol_only_overclaim_rate` | `0.0000` |

当前主要问题：

1. `record-level` 分数校准仍然偏弱。
2. 等价但不同构设计的给分策略仍不稳定。
3. 对某些明显结构性/语义性坏例的惩罚仍不够稳定。
4. `summary-level` 的排序与整体尺度仍然不够贴近人工。
5. `protocol-only` 的证据纪律已经较稳，但 V&V 角色覆盖还不够满。

## 2. 全周期执行原则

### 2.1 每一阶段必须满足的运行要求

1. 真实入口必须可运行：
   - `review_artifacts()`
   - `review_model()`
   - `python -m expert_review`
2. 本阶段新增逻辑必须接入真实运行流。
3. 不允许“先堆模块，后续再接”的明显不可达实现。
4. 不允许把阶段性重构做成旁路 demo，而主路径继续停留在旧逻辑。
5. 每个阶段结束后都必须跑最小测试与最小评测。

### 2.2 每一阶段必须满足的记录要求

每个阶段都必须留下：

1. 本阶段改动范围说明。
2. 本阶段接入了哪些真实运行路径。
3. 本阶段新增或移除了哪些中间结构。
4. 本阶段完整对齐指标。
5. 本阶段相对上阶段的提升项。
6. 本阶段相对上阶段的退化项。
7. 本阶段已知未解决问题。

### 2.3 每一阶段必须满足的对齐要求

每个阶段都不是“等最后再对齐”，而是：

1. 在该阶段完成后，基于该阶段架构能力做一次真实回放。
2. 用当期 reviewer 实现直接跑 benchmark slice。
3. 记录该阶段的：
   - `HAI`
   - `RAS`
   - `SAS`
   - `PDS`
   - `normalized_mae`
   - `issue_f1`
   - `human_issue_coverage_recall`
   - `equivalence_false_reject_rate`
   - `unsupported_claim_rate`
   - `protocol_only_overclaim_rate`
   - `ece`
   - `rerun_score_std`
4. 若某阶段对齐退化，必须记录原因，不得只保留“最好的一轮”。

## 3. Phase 1: 运行时骨架替换

目标：

把旧的 heuristic-heavy 单路径 reviewer 替换成一个**保持接口兼容**的 v1 风格 staged runtime，并确保 reviewer 在重构开始时就已经进入真实的新架构主路径。

### Todolist

* [ ] 保持现有外部接口不变。
* [ ] 将旧 reviewer 的主入口切换到新的 staged runtime。
* [ ] 引入 `contract -> regime -> dossier -> trace/equivalence/quality -> score/synthesis` 主流程。
* [ ] 明确区分运行时逻辑与离线 benchmark 逻辑。
* [ ] 确保未知格式输入不会阻塞评审。
* [ ] 确保 reviewer 没有回退到路径外数据依赖。
* [ ] 建立该阶段的基线测试。
* [ ] 建立该阶段的基线对齐快照。

### Checklist

* [ ] `review_artifacts()` 能跑通。
* [ ] `review_model()` 能跑通。
* [ ] `python -m expert_review` 能跑通。
* [ ] 旧主路径不再主导评审逻辑。
* [ ] 新运行时已经是默认主路径。
* [ ] 没有新增明显不可达代码。
* [ ] 已记录 Phase 1 的完整对齐基线。

## 4. Phase 2: 抽取器与 Dossier 加固

目标：

把当前初版 dossier 流程强化成 reviewer 的稳定中间层，使后续多智能体分析不再直接依赖原始 artifact 字符串做模糊推理。

### Todolist

* [ ] 细化 `input dossier / prediction dossier / reference dossier` 结构。
* [ ] 强化已知格式探测逻辑，但只把它作为加速器。
* [ ] 强化未知格式下的通用要素抽取。
* [ ] 让 dossier 明确记录：
  * [ ] major elements
  * [ ] major relations
  * [ ] behaviors
  * [ ] constraints
  * [ ] ambiguities
  * [ ] observability
* [ ] 引入更稳定的 evidence item 组织方式。
* [ ] 让 traceability、equivalence、quality 三类后续节点只依赖 dossier，而不是直接依赖原始输入。
* [ ] 减少 parser-only 与 llm-extracted 中间产物之间的冲突。
* [ ] 跑一轮以 extraction/dossier 为主的误差分析。

### Checklist

* [ ] dossier 已成为真实运行流中的标准中间层。
* [ ] 已知格式探测失败不会阻塞评审。
* [ ] 未知格式仍能给出保守但结构化的 dossier。
* [ ] dossier 信息已足够支撑后续节点。
* [ ] 新增 dossier 字段不是摆设，已被真实消费。
* [ ] 没有新增不可达中间模块。
* [ ] 已记录 Phase 2 的完整对齐指标。

## 5. Phase 3: Traceability 与 Equivalence 推理强化

目标：

把 reviewer 从“词面匹配 + 松散比较”推进到真正能处理**等价但不同构**、**依附关系敏感**、**缺失与额外结构可区分**的人类式评审。

### Todolist

* [ ] 强化 requirement-to-artifact trace candidate 生成。
* [ ] 强化 trace 裁决：
  * [ ] `matched`
  * [ ] `partial`
  * [ ] `missing`
* [ ] 强化 equivalence reasoning：
  * [ ] 非同构但行为兼容应给 credit
  * [ ] 表面相似但 guard/trigger/action 错误应严罚
* [ ] 强化 dependency-aware judgement：
  * [ ] state 错误时，其依附 transition / guard / action 不能被轻易放过
* [ ] 强化 harmful extra / supported restructure / contradiction 的区分。
* [ ] 引入更明确的 arbitration 逻辑，处理 trace 与 equivalence 的冲突结论。
* [ ] 重点回放 `record-level` 样本并记录误差簇。

### Checklist

* [ ] reviewer 不再主要依赖简单 lexical overlap 做等价判断。
* [ ] reviewer 能在显式 bad case 上压低分数。
* [ ] reviewer 能在等价变体上给出合理 credit。
* [ ] trace 与 equivalence 的输出口径一致。
* [ ] `equivalence_false_reject_rate` 和 `equivalence_false_accept_rate` 有明确阶段记录。
* [ ] 没有新增不可达裁决分支。
* [ ] 已记录 Phase 3 的完整对齐指标。

## 6. Phase 4: Quality Review 与 Evidence Discipline 强化

目标：

把 reviewer 补足为更接近真实人工专家的“质量评审器”，同时把 `summary-only` / `protocol-only` 下的证据纪律与置信度控制做稳。

### Todolist

* [ ] 强化 pragmatic quality review：
  * [ ] readability
  * [ ] naming consistency
  * [ ] unused or noisy structure
  * [ ] proportional complexity
* [ ] 引入更明确的 quality issue taxonomy。
* [ ] 强化 `summary-only` 的整体质量判断与粗粒度分数尺度。
* [ ] 强化 `protocol-only` 下的 restraint：
  * [ ] 不伪造 element-level certainty
  * [ ] 正确识别 inspection / formal verification / simulation / testing 的角色
* [ ] 强化 confidence policy、abstention policy、notes policy。
* [ ] 重点回放 `summary-level` 与 `protocol-only` 样本。

### Checklist

* [ ] reviewer 能显式识别质量问题，而不是只给语义分。
* [ ] `summary-only` 不会伪造逐元素问题。
* [ ] `protocol-only` 不会过度自信。
* [ ] reviewer 对 V&V 角色有可观测识别能力。
* [ ] `PDS` 与 `SAS` 有阶段性提升记录。
* [ ] 没有新增“只记录 notes 但不影响真实流程”的空逻辑。
* [ ] 已记录 Phase 4 的完整对齐指标。

## 7. Phase 5: 内部多智能体化收敛

目标：

将当前 staged runtime 收敛成真正符合 v1 设计意图的**通用化多智能体 reviewer 内核**，但继续维持同一套外部接口。

### Todolist

* [ ] 将当前各分析步骤正式提升为内部 agent role：
  * [ ] Contract Router
  * [ ] Evidence Regime Estimator
  * [ ] Input Analyst
  * [ ] Prediction Extractor
  * [ ] Reference Extractor
  * [ ] Traceability Agent
  * [ ] Equivalence and Difference Agent
  * [ ] Pragmatic Quality Agent
  * [ ] Missing-Evidence Critic
  * [ ] Disagreement Arbiter
  * [ ] Score Composer
  * [ ] Final Synthesizer
* [ ] 明确每个 agent 的输入上下文最小化原则。
* [ ] 明确 fan-out / fan-in 关系。
* [ ] 明确 agent 间冲突与裁决机制。
* [ ] 确保多智能体组织不是“表面拆函数”，而是真正影响运行流。
* [ ] 保持外部接口不变。
* [ ] 跑一次完整 phase-level 回放，形成 v1 候选冻结基线。

### Checklist

* [ ] 内部 reviewer 架构已整体符合 v1 设计稿。
* [ ] agent role 不是命名装饰，而是运行时真实节点。
* [ ] 各 agent 间输入上下文已裁剪，不是所有节点共享全量 prompt。
* [ ] 冲突结论存在真实 arbitration。
* [ ] 外部接口仍保持兼容。
* [ ] 没有新增明显不可达 agent 节点。
* [ ] 已记录 Phase 5 的完整对齐指标。

## 8. Phase 6: V1 冻结前验证与收口

目标：

在 Phase 5 的基础上完成最终收口，使 reviewer 能作为“v1 真正可冻结版本”被固定下来。

### Todolist

* [ ] 对照 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md) 的停止标准做完整核验。
* [ ] 对所有 phase 的指标演化做总汇总。
* [ ] 明确哪些指标已经达到停止门槛，哪些还未达到。
* [ ] 整理最终 v1 的 prompt / policy / rubric / agent 角色定义。
* [ ] 去掉已经被替换掉的旧临时实现和旁路逻辑。
* [ ] 做一次不可达路径检查，确保最终 v1 代码树干净。
* [ ] 输出版本级对齐报告与冻结说明。

### Checklist

* [ ] v1 的真实实现已经不是“半旧半新”混合状态。
* [ ] 所有阶段性临时逻辑都有归宿：
  * [ ] 要么进入正式路径
  * [ ] 要么被删除
* [ ] 没有明显不可达代码残留。
* [ ] 有完整 phase-by-phase 对齐演化记录。
* [ ] 有最终冻结版本说明。
* [ ] 若未达门槛，已明确写出阻塞项与下一版设计入口。

## 9. 每个 Phase 的统一对齐记录模板

每个 phase 完成后，至少记录以下内容：

### 9.1 指标总表

1. `HAI`
2. `RAS`
3. `SAS`
4. `PDS`
5. `normalized_mae`
6. `rmse`
7. `issue_f1`
8. `human_issue_coverage_recall`
9. `equivalence_false_reject_rate`
10. `equivalence_false_accept_rate`
11. `unsupported_claim_rate`
12. `protocol_only_overclaim_rate`
13. `ece`
14. `rerun_score_std`

### 9.2 本阶段改进记录

1. 本阶段最明显提升的三项能力。
2. 本阶段最明显退化的三项能力。
3. 本阶段仍未解决的三类错误簇。

### 9.3 本阶段运行记录

1. 哪些入口已验证。
2. 哪些真实路径被替换。
3. 哪些旧逻辑仍然保留。
4. 哪些模块只是临时过渡件。

## 10. 阶段推进规则

1. 除非当前阶段的真实运行已经稳定，否则不推进到下一阶段。
2. 除非当前阶段已留下完整指标记录，否则不算完成。
3. 若某阶段为追某一指标导致另一关键指标明显退化，必须如实记录，不得跳过。
4. 若某阶段发现当前设计本身无法继续局部演进，应在进入下一阶段前先更新设计文档。
5. 若最终需要新增 `v2` 设计目录，必须以“当前 TODO 的 phase 记录完结”为前提。

## 11. 最终目标

最终目标不是“写完一个看起来像 v1 的新目录”，而是：

1. `expert_review` 的真实运行时内部已经成为 v1 设计稿定义的通用化多智能体 reviewer。
2. reviewer 在任意时点都保持完整可运行。
3. 整个重构周期中的每一阶段都有完整对齐记录。
4. 任何阶段都没有通过堆不可达代码来伪装进度。
5. 最终冻结版本能够以完整、可追溯、可评测的形式被后续版本继续继承。
