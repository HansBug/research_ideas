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

当前基线对齐指标（`2026-04-16 16:46:49` 的 deterministic 收尾快照）：

| 指标 | 当前值 |
|---|---:|
| `HAI` | `66.58` |
| `RAS` | `60.82` |
| `SAS` | `62.51` |
| `PDS` | `87.50` |
| `normalized_mae` | `0.2177` |
| `issue_f1` | `0.5810` |
| `human_issue_coverage_recall` | `0.8500` |
| `equivalence_false_reject_rate` | `0.1000` |
| `unsupported_claim_rate` | `0.5547` |
| `summary_only_element_claim_rate` | `0.0000` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `vv_role_coverage` | `0.5000` |

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

### 2.1.1 每一阶段后的自我迭代硬要求

每个 phase 完成后的工作**不止是跑一轮评测**，而是必须进入该阶段架构边界内的多轮自我迭代优化。

硬要求如下：

1. 每个 phase 完成后，必须基于**当前这个架构与现状**进入多轮自我迭代。
2. 自我迭代不能只跑一轮；必须连续做多轮 patch -> replay -> analysis -> patch。
3. 只有当进一步提升已经明显开始边际化时，才允许停止该 phase 的自我迭代并推进到下一阶段。
4. 如果关键指标仍然还能明显提升，就不能提前停止。
5. 每一轮都只能在该阶段允许的局部调整范围内继续优化，不能偷偷跨 phase 提前引入下一阶段的大结构改动。
6. 每一轮迭代后 reviewer 仍必须保持完整可运行。
7. 每一轮迭代都必须留下完整记录，形成从 phase 开始到 phase 收敛的连续优化链路。

### 2.2 每一阶段必须满足的记录要求

每个阶段都必须留下：

1. 本阶段改动范围说明。
2. 本阶段接入了哪些真实运行路径。
3. 本阶段新增或移除了哪些中间结构。
4. 本阶段完整对齐指标。
5. 本阶段相对上阶段的提升项。
6. 本阶段相对上阶段的退化项。
7. 本阶段已知未解决问题。
8. 本阶段内部每一轮自我迭代的完整记录。

补充硬要求：

1. 每一次完成任务后，都必须把完成情况**如实写回 TODO**。
2. 必须如实回写，不允许把未完成项提前打勾。
3. 该打勾的打勾。
4. 没有完成的项目必须明确说明当前现状、阻塞原因和下一步处理口径。
5. TODO 不是计划草稿，而是整个 phase 执行过程中的真实状态台账。

### 2.2.1 每一轮自我迭代必须记录的内容

每个 phase 内部的每一轮迭代，至少要记录：

1. `round_id`
2. 本轮修改了什么
3. 本轮修改属于哪类问题修复：
   - `contract_understanding_error`
   - `element_extraction_error`
   - `equivalence_reasoning_error`
   - `quality_judgement_error`
   - `evidence_discipline_error`
4. 本轮修改前指标
5. 本轮修改后指标
6. 本轮指标 delta
7. 本轮提升最明显的点
8. 本轮新增或暴露出的退化点
9. 本轮结束后是否继续迭代
10. 若停止，停止原因是否为“收益明显边际化”

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
5. 某阶段内的每一轮自我迭代都必须有前后指标对比，不能只记录 phase 结束时的最终一组数。
6. phase 结束时除了阶段终态指标，还必须保留“本阶段多轮优化链路”的完整记录。

## 3. Phase 1: 运行时骨架替换

目标：

把旧的 heuristic-heavy 单路径 reviewer 替换成一个**保持接口兼容**的 v1 风格 staged runtime，并确保 reviewer 在重构开始时就已经进入真实的新架构主路径。

### Todolist

* [x] 保持现有外部接口不变。
* [x] 将旧 reviewer 的主入口切换到新的 staged runtime。
* [x] 引入 `contract -> regime -> dossier -> trace/equivalence/quality -> score/synthesis` 主流程。
* [x] 明确区分运行时逻辑与离线 benchmark 逻辑。
* [x] 确保未知格式输入不会阻塞评审。
* [x] 确保 reviewer 没有回退到路径外数据依赖。
* [x] 建立该阶段的基线测试。
* [x] 建立该阶段的基线对齐快照。
* [x] 在 Phase 1 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [x] 记录 Phase 1 每一轮迭代的修改项与指标前后变化。

### Checklist

* [x] `review_artifacts()` 能跑通。
* [x] `review_model()` 能跑通。
* [x] `python -m expert_review` 能跑通。
* [x] 旧主路径不再主导评审逻辑。
* [x] 新运行时已经是默认主路径。
* [x] 没有新增明显不可达代码。
* [x] 已记录 Phase 1 的完整对齐基线。
* [x] 已保留 Phase 1 多轮自我迭代链路记录。
* [x] 停止 Phase 1 迭代的原因已明确记录为“提升边际化”或等价结论。

### Phase 1 当前状态回写

- 回写时间：`2026-04-16 16:46:49`
- 完成状态：`Phase 1` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 1`，未推进到 `Phase 2`。
- 真实接入情况：`expert_review_agent.py` 已默认路由到 `expert_review_v1_runtime.py` 的 staged runtime；`heuristic_expert_review()` 已退化为对该 runtime 的兼容包装，不再主导评审逻辑。
- 运行时边界：`expert_review_self_iteration.py` 仅承担离线 benchmark 回放与分析；运行时不依赖 `expert_review/` 路径外数据。
- 可运行性：`review_artifacts()`、`review_model()`、`python -m expert_review`、`pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_expert_review.py` 均已验证。
- 未完成项：无。
- 已知遗留问题：`record-level` 分数校准仍偏弱；等价但不同构设计的裁决仍不稳定；`protocol-only` 的 V&V 角色覆盖只达到部分覆盖。

### Phase 1 指标总表

本节记录 `2026-04-16 16:46:49` 基于 `run_benchmark_iteration(llm_mode='off')` 的收尾快照。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `66.58` |
| `RAS` | `60.82` |
| `SAS` | `62.51` |
| `PDS` | `87.50` |
| `normalized_mae` | `0.2177` |
| `rmse` | `0.2513` |
| `issue_f1` | `0.5810` |
| `human_issue_coverage_recall` | `0.8500` |
| `equivalence_false_reject_rate` | `0.1000` |
| `equivalence_false_accept_rate` | `0.2857` |
| `unsupported_claim_rate` | `0.5547` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.6857` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.5000` |

### Phase 1 本阶段改进记录

- 最明显提升 1：真实默认主路径已切到 v1 staged runtime，外部接口保持兼容，且未知格式自由文本输入不会阻塞评审。
- 最明显提升 2：`summary-only` 与 `protocol-only` 的证据纪律已经被压稳，`summary_only_element_claim_rate = 0.0000`，`protocol_only_overclaim_rate = 0.0000`。
- 最明显提升 3：`protocol-only` 下开始显式识别 V&V 分工并控制置信度，`PDS = 87.50`，`confidence_discipline = 1.0000`。
- 最明显退化/暴露问题 1：`record-level` 校准仍弱，`normalized_mae = 0.2177`，说明对单条样本的给分偏差仍然较大。
- 最明显退化/暴露问题 2：`unsupported_claim_rate = 0.5547` 仍高，说明 agent 还存在“问题抓得太多、证据不够硬”的倾向。
- 最明显退化/暴露问题 3：`ece = 0.6857`，说明当前置信度与真实正确性仍不够一致。
- 仍未解决错误簇 1：高人工分的等价变体仍会被误杀，例如 `STM Results:7`、`STM Results:9`。
- 仍未解决错误簇 2：低人工分的坏例仍有被打高分的情况，例如 `STM Results:6`、`STM Results:0`、`STM Results:8`。
- 仍未解决错误簇 3：`protocol-only` 下的 V&V 角色覆盖仍只有 `0.5000`，说明 reviewer 知道要克制，但还没有把角色理解补满。

### Phase 1 多轮自我迭代记录

说明：

- `Round 0` 是运行时骨架替换刚完成后的起始快照。
- `Round 1..4` 是 Phase 1 架构边界内的局部优化轮次。
- 历史中间轮次保留了 `HAI` 主指标快照；完整子指标只对起始态与收尾态做了保留。这里不补造不存在的中间明细。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | 完成主路径切换，建立 `contract -> regime -> dossier -> trace/equivalence/quality -> score/synthesis` 骨架 | `contract_understanding_error` / `element_extraction_error` | 无 | `HAI 56.90 / RAS 54.09 / SAS 48.61 / PDS 75.00` | `--` | `是` | 起始基线，说明骨架替换后 reviewer 已进入真实新路径，但对齐仍明显不够 |
| `Round 1` | 清理 slice/regime 路由与运行时边界，修正 benchmark 只在外环使用，收紧未知格式降级路径 | `contract_understanding_error` / `evidence_discipline_error` | `HAI 56.90` | `HAI 60.45` | `+3.55` | `是` | 先把运行边界与 regime 识别做稳，避免旧路径语义泄漏 |
| `Round 2` | 强化 `summary-only` 证据纪律与 notes policy，压制无依据的元素级断言 | `quality_judgement_error` / `evidence_discipline_error` | `HAI 60.45` | `HAI 63.13` | `+2.68` | `是` | 这一轮主要修复“只看 summary 却假装看到元素细节”的问题 |
| `Round 3` | 强化 `protocol-only` 的 V&V 角色识别、mixed-evidence 提示与保守置信度策略 | `evidence_discipline_error` / `quality_judgement_error` | `HAI 63.13` | `HAI 66.59` | `+3.46` | `是` | `PDS` 明显抬升，reviewer 已基本学会“什么时候不能装懂” |
| `Round 4` | 调整结构性惩罚与等价裁决权重，尝试同时压低坏例分数并保留合理等价 credit | `equivalence_reasoning_error` / `quality_judgement_error` | `HAI 66.59` | `历史快照 HAI 66.16` | `-0.43` | `否` | 当前树收尾重跑为 `HAI 66.58`，说明这轮之后提升已进入边际化区间，没有形成稳定的新增收益 |

### Phase 1 收尾汇报记录

- 当前 phase 的完成状态：`Phase 1` 已完成并停止，等待下一步指令，不进入 `Phase 2`。
- TODO 打勾情况：`Phase 1` 的 Todolist 与 Checklist 均已如实打勾。
- TODO 尚未完成项：无；现存问题已转化为下一阶段 backlog，而不是本阶段未完成项。
- 当前对齐程度总览：`HAI 66.58`，相对起始基线 `56.90` 提升 `+9.68`；说明 reviewer 已从“新骨架刚接上但与人工还有明显距离”提升到“方向上可用、局部已接近人工，但还远未到冻结水位”。
- `HAI 66.58` 的人类含义：整体对齐已脱离不可用区，很多判断方向已对，但离 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md) 中建议的冻结目标 `HAI >= 85` 仍有明显差距。
- `RAS 60.82` 的人类含义：逐条记录级判断已经从低 50 分段抬到低 60 分段，代表 reviewer 常能抓到问题方向，但单条样本上的打分幅度和误差控制仍不够像真人。
- `SAS 62.51` 的人类含义：summary 级整体分数与证据纪律明显比旧实现稳，但 `RankAlign = 32.50` 仍低，说明“哪一组整体更好”的排序还不够像人工。
- `PDS 87.50` 的人类含义：`protocol-only` 场景下，reviewer 基本已经学会克制，不会在没有逐元素证据时伪造细节，这一点已比较接近真人的保守习惯。
- `normalized_mae 0.2177` 与 `rmse 0.2513` 的人类含义：在 `0..1` 分数尺度上，当前平均误差仍在约 `0.22` 左右，说明“能看出好坏方向”和“给出接近真人的准分”仍是两回事。
- `issue_f1 0.5810` 与 `human_issue_coverage_recall 0.8500` 的人类含义：大多数真人会指出的问题 reviewer 已经能覆盖到，但它又额外说了太多真人并不会采纳的问题。
- `unsupported_claim_rate 0.5547` 的人类含义：当前 reviewer 仍偏“爱挑问题”，超过一半的问题主张在人工口径下证据不够硬，这会直接拉低可用性。
- `equivalence_false_reject_rate 0.1000` 的人类含义：每十个合理变体里，大约还有一个会被误拒；对真正要冻结的 expert reviewer 来说，这仍偏高。
- `vv_role_coverage 0.5000` 的人类含义：reviewer 已知道 inspection / verification / simulation / testing 不是一回事，但只覆盖到一半左右的应识别角色，还不够像真人专家。
- 真实对齐例子 1：`STM Results:10`，人工 `0.88`，agent `0.813744`；这说明 reviewer 已经能对“整体正确、但仍有局部问题”的样本给出接近人工的高分判断。
- 真实对齐例子 2：`STM Results:2`，人工 `0.8888888889`，agent `0.790336`；说明 reviewer 在一部分高质量样本上已经能保持“高分但不满分”的真人风格。
- 真实近失配例子：`STM Results:5`，人工 `0.3846153846`，agent `0.483567`；说明 reviewer 已看到有问题，但惩罚力度仍偏软。
- 真实失配例子 1：`STM Results:7`，人工 `0.8196721311`，agent `0.314871`；这是典型的“等价但不同构设计被误杀”，说明等价推理还没有稳住。
- 真实失配例子 2：`STM Results:6`，人工 `0.2222222222`，agent `0.604218`；这是典型的“明显坏例却给高分”，说明结构性坏例惩罚仍不稳定。
- 真实失配例子 3：`STM Results:0`，人工 `0.4166666667`，agent `0.686849`；说明 reviewer 仍会对部分中低质量样本过宽。
- `protocol-only` 例子 1：`protocol::llms_emp` 的 agent 分数为 `0.250645`，置信度 `0.42`，`vv_role_coverage = 0.4`；说明 reviewer 已会低分、低置信度保守输出，但角色理解还不完整。
- `protocol-only` 例子 2：`protocol::ttool-ai` 的 agent 分数同样为 `0.250645`，置信度 `0.42`，`vv_role_coverage = 0.8`；说明同样的克制策略已经成立，但不同协议样本间的角色覆盖仍不均衡。
- 停止原因：在 `Phase 1` 允许的局部调整内，多轮迭代已经把主路径切换、未知格式兜底和证据纪律做到基本稳定；继续靠本阶段的小修小补已无法稳定提升 `HAI/RAS/SAS`，收益开始明显边际化，因此按规则停止并待命。

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
* [ ] 在 Phase 2 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [ ] 记录 Phase 2 每一轮迭代的修改项与指标前后变化。

### Checklist

* [ ] dossier 已成为真实运行流中的标准中间层。
* [ ] 已知格式探测失败不会阻塞评审。
* [ ] 未知格式仍能给出保守但结构化的 dossier。
* [ ] dossier 信息已足够支撑后续节点。
* [ ] 新增 dossier 字段不是摆设，已被真实消费。
* [ ] 没有新增不可达中间模块。
* [ ] 已记录 Phase 2 的完整对齐指标。
* [ ] 已保留 Phase 2 多轮自我迭代链路记录。
* [ ] 停止 Phase 2 迭代的原因已明确记录为“提升边际化”或等价结论。

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
* [ ] 在 Phase 3 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [ ] 记录 Phase 3 每一轮迭代的修改项与指标前后变化。

### Checklist

* [ ] reviewer 不再主要依赖简单 lexical overlap 做等价判断。
* [ ] reviewer 能在显式 bad case 上压低分数。
* [ ] reviewer 能在等价变体上给出合理 credit。
* [ ] trace 与 equivalence 的输出口径一致。
* [ ] `equivalence_false_reject_rate` 和 `equivalence_false_accept_rate` 有明确阶段记录。
* [ ] 没有新增不可达裁决分支。
* [ ] 已记录 Phase 3 的完整对齐指标。
* [ ] 已保留 Phase 3 多轮自我迭代链路记录。
* [ ] 停止 Phase 3 迭代的原因已明确记录为“提升边际化”或等价结论。

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
* [ ] 在 Phase 4 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [ ] 记录 Phase 4 每一轮迭代的修改项与指标前后变化。

### Checklist

* [ ] reviewer 能显式识别质量问题，而不是只给语义分。
* [ ] `summary-only` 不会伪造逐元素问题。
* [ ] `protocol-only` 不会过度自信。
* [ ] reviewer 对 V&V 角色有可观测识别能力。
* [ ] `PDS` 与 `SAS` 有阶段性提升记录。
* [ ] 没有新增“只记录 notes 但不影响真实流程”的空逻辑。
* [ ] 已记录 Phase 4 的完整对齐指标。
* [ ] 已保留 Phase 4 多轮自我迭代链路记录。
* [ ] 停止 Phase 4 迭代的原因已明确记录为“提升边际化”或等价结论。

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
* [ ] 在 Phase 5 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [ ] 记录 Phase 5 每一轮迭代的修改项与指标前后变化。

### Checklist

* [ ] 内部 reviewer 架构已整体符合 v1 设计稿。
* [ ] agent role 不是命名装饰，而是运行时真实节点。
* [ ] 各 agent 间输入上下文已裁剪，不是所有节点共享全量 prompt。
* [ ] 冲突结论存在真实 arbitration。
* [ ] 外部接口仍保持兼容。
* [ ] 没有新增明显不可达 agent 节点。
* [ ] 已记录 Phase 5 的完整对齐指标。
* [ ] 已保留 Phase 5 多轮自我迭代链路记录。
* [ ] 停止 Phase 5 迭代的原因已明确记录为“提升边际化”或等价结论。

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
* [ ] 汇总所有 phase 内部多轮自我迭代记录，形成完整优化链路总账。

### Checklist

* [ ] v1 的真实实现已经不是“半旧半新”混合状态。
* [ ] 所有阶段性临时逻辑都有归宿：
  * [ ] 要么进入正式路径
  * [ ] 要么被删除
* [ ] 没有明显不可达代码残留。
* [ ] 有完整 phase-by-phase 对齐演化记录。
* [ ] 有完整 phase-by-phase 且 round-by-round 的优化链路记录。
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

### 9.4 本阶段多轮自我迭代记录

每个 phase 内部，应追加一个 round-by-round 记录区，至少包含：

1. `Round 0`：该 phase 刚完成结构改造时的起始基线
2. `Round 1..N`：该 phase 内每一轮继续优化
3. 每一轮的：
   - 修改内容
   - 修改目的
   - 修改前指标
   - 修改后指标
   - 指标 delta
   - 是否继续迭代
4. 最终停止条件：
   - 指标已经达到目标
   - 或进一步提升已明显边际化

### 9.5 本阶段收尾汇报记录

每个 phase 在所有当期要求的事项都处理完之后，必须追加一段“阶段收尾汇报记录”，至少包含：

1. 当前 phase 的完成状态
2. TODO 中哪些项已完成并已打勾
3. TODO 中哪些项尚未完成，以及当前现状
4. 当前对齐程度总览
5. 对各项核心指标的解释：
   - 当前数值到了什么程度
   - 从人类评审视角意味着什么
6. 至少给出若干真实例子对比，说明：
   - reviewer 当前和人类对齐在哪里
   - reviewer 当前和人类还偏差在哪里
7. 明确说明是否停止在当前 phase，等待下一步指令

## 10. 阶段推进规则

1. 除非当前阶段的真实运行已经稳定，否则不推进到下一阶段。
2. 除非当前阶段已留下完整指标记录，否则不算完成。
3. 若某阶段为追某一指标导致另一关键指标明显退化，必须如实记录，不得跳过。
4. 若某阶段发现当前设计本身无法继续局部演进，应在进入下一阶段前先更新设计文档。
5. 若最终需要新增 `v2` 设计目录，必须以“当前 TODO 的 phase 记录完结”为前提。
6. 除非当前 phase 在其自身架构边界内已经做过多轮自我迭代并出现明显边际收益衰减，否则不得推进到下一 phase。
7. 每个 phase 结束时必须同时具备：
   - phase 级最终指标
   - round-by-round 优化链路记录
   - 停止继续迭代的明确理由
8. 每个 phase 在所有当期事项都处理完后，必须先把 TODO 如实回写，再停下来向用户汇报当前状况，而不是直接进入下一 phase。
9. 该次汇报必须包含：
   - 当前完成状态
   - 当前对齐程度
   - 各项核心指标的含义及其人类视角解释
   - 真实例子对比
10. 在完成上述回写与汇报前，不得视为该 phase 真正收尾。

## 11. 最终目标

最终目标不是“写完一个看起来像 v1 的新目录”，而是：

1. `expert_review` 的真实运行时内部已经成为 v1 设计稿定义的通用化多智能体 reviewer。
2. reviewer 在任意时点都保持完整可运行。
3. 整个重构周期中的每一阶段都有完整对齐记录。
4. 任何阶段都没有通过堆不可达代码来伪装进度。
5. 最终冻结版本能够以完整、可追溯、可评测的形式被后续版本继续继承。
6. 每个阶段结束时，TODO 台账与真实执行状态始终一致，且都已向用户做过一次如实、可解释、带指标和例子的收尾汇报。
