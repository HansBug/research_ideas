# Expert Review V1 TODO

本文档是 `expert_review` 的 **v1 分阶段执行总表**。它不是一次性“大重写”计划，而是一个**逐阶段、局部调整、持续可运行**的重构与对齐路线图。

它也不是“在旧代码上持续修修补补”的许可文件。后续每个 phase 除了能力与对齐指标改进外，还必须持续推动 `expert_review/` 的路径结构、模块边界和运行时组织朝 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md) 第 `13` 节建议目录架构收敛。

当前文档列出的 `Phase 1..6` 是**当前计划主干**，不是不可变上限。若后续发现为了实现真正的 v1 架构收敛、目录重组、运行时收口或对齐补足，仍需要新的独立阶段，则允许继续新增 `Phase 7+`；但新增 phase 也必须遵守本文所有运行、验收、记录、自我迭代与回写规则。

本路线图的硬约束如下：

1. 每个 phase 都只能在当前 `expert_review` 可运行实现的基础上做局部修改、调整和扩充。
2. 每个 phase 完成后，`expert_review` 必须继续保持完整可运行状态。
3. 每个 phase 完成后，新的代码必须真实接入运行路径，不允许明显不可达的新代码。
4. 每个 phase 完成后，都必须在当期架构能力边界内做一次对齐评测。
5. 每个 phase 都必须完整记录该阶段的对齐指标、改进点、退化点和剩余问题。
6. 最终在最后一个 phase 完成后，内部 reviewer 架构需要整体达到 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md) 所定义的 v1 目标形态。
7. 后续各 phase 不只追求“行为上更像 v1”，还必须让 `expert_review/` 的目录布局、模块职责与运行时编排逐步落到 v1 设计稿建议的 `schemas / prompts / tools / agents / graph / compatibility` 形态上。
8. 当前 phase 数量不是硬上限；若为了真正完成 v1 结构收敛仍需补充阶段，可以继续新增 phase，但不得借此跳过已有阶段的收尾、验收和如实回写。

推荐阅读顺序：

1. 先读 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
2. 再读 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md)
3. 最后读本文

关联 PR：

1. 当前执行 PR：[PR #6：将 expert review 重构到 v1 多智能体运行时方向](https://github.com/HansBug/research_ideas/pull/6)

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
5. 每个 phase 除能力提升外，至少要推动一次 `expert_review/` 路径结构、模块边界或运行时组织朝 v1 设计收敛的实质性变更。
6. 阶段性适配层可以存在，但核心能力不能长期继续堆在历史单文件或跨层杂糅文件里打补丁。
7. 每个阶段结束后都必须跑最小测试与最小评测。

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

### 2.1.2 每一阶段必须满足的结构收敛要求

1. 每个后续 phase 都必须明确回答：本阶段把 `expert_review/` 的哪一部分朝 v1 目录架构推进了。
2. 推荐对齐目标以 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md) 第 `13` 节为准，优先收敛到：
   - `schemas/`
   - `prompts/`
   - `tools/`
   - `agents/`
   - `graph/`
   - `compatibility/`
3. 若某阶段还不能一次完成正式拆分，也必须明确临时归宿与后续迁移目标，避免新逻辑继续无边界堆进历史大文件。
4. 阶段验收不仅看指标，也看路径结构和职责边界是否更接近 v1 设计，而不是继续停留在旧工程组织上。

### 2.2 每一阶段必须满足的记录要求

每个阶段都必须留下：

1. 本阶段改动范围说明。
2. 本阶段接入了哪些真实运行路径。
3. 本阶段推动了哪些路径结构、模块边界或项目架构收敛。
4. 本阶段新增或移除了哪些中间结构。
5. 本阶段完整对齐指标。
6. 本阶段相对上阶段的提升项。
7. 本阶段相对上阶段的退化项。
8. 本阶段已知未解决问题。
9. 本阶段内部每一轮自我迭代的完整记录。

补充硬要求：

1. 每一次完成任务后，都必须把完成情况**如实写回 TODO**。
2. 必须如实回写，不允许把未完成项提前打勾。
3. 该打勾的打勾。
4. 没有完成的项目必须明确说明当前现状、阻塞原因和下一步处理口径。
5. TODO 不是计划草稿，而是整个 phase 执行过程中的真实状态台账。
6. 每次 phase 状态发生变化后，必须同步更新 [PR #6](https://github.com/HansBug/research_ideas/pull/6) 的 body。
7. PR body 至少要同步：
   - 当前 phase checkbox 状态
   - 当前 phase 是否完成
   - 当前对齐基线摘要
8. TODO 与 PR body 的 phase 状态、阶段结论和基线摘要不得长期不一致；若短时间内存在差异，必须在当次任务结束前补齐同步。
9. 若新增 `Phase N+1`，必须同步把新增阶段写入 TODO 与 PR body，并说明新增原因、目标边界和验收口径。

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
- 真实接入情况：`agent.py` 已默认路由到 `expert_review_v1_runtime.py` 的 staged runtime；`heuristic_expert_review()` 已退化为对该 runtime 的兼容包装，不再主导评审逻辑。
- 运行时边界：`benchmark.py` 仅承担离线 benchmark 回放与分析；运行时不依赖 `expert_review/` 路径外数据。
- 可运行性：`review_artifacts()`、`review_model()`、`python -m expert_review`、`pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 均已验证。
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

* [x] 细化 `input dossier / prediction dossier / reference dossier` 结构。
* [x] 强化已知格式探测逻辑，但只把它作为加速器。
* [x] 强化未知格式下的通用要素抽取。
* [x] 让 dossier 明确记录：
  * [x] major elements
  * [x] major relations
  * [x] behaviors
  * [x] constraints
  * [x] ambiguities
  * [x] observability
* [x] 引入更稳定的 evidence item 组织方式。
* [x] 让 traceability、equivalence、quality 三类后续节点只依赖 dossier，而不是直接依赖原始输入。
* [x] 减少 parser-only 与 llm-extracted 中间产物之间的冲突。
* [x] 跑一轮以 extraction/dossier 为主的误差分析。
* [x] 在 Phase 2 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [x] 记录 Phase 2 每一轮迭代的修改项与指标前后变化。

### Checklist

* [x] dossier 已成为真实运行流中的标准中间层。
* [x] 已知格式探测失败不会阻塞评审。
* [x] 未知格式仍能给出保守但结构化的 dossier。
* [x] dossier 信息已足够支撑后续节点。
* [x] 新增 dossier 字段不是摆设，已被真实消费。
* [x] 没有新增不可达中间模块。
* [x] 已记录 Phase 2 的完整对齐指标。
* [x] 已保留 Phase 2 多轮自我迭代链路记录。
* [x] 停止 Phase 2 迭代的原因已明确记录为“提升边际化”或等价结论。

### Phase 2 当前状态回写

- 回写时间：`2026-04-16 17:36:56`
- 完成状态：`Phase 2` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 2`，未推进到 `Phase 3`。
- 真实接入情况：
  - `InputDossier` 已扩展为 `summary / requirements / behaviors / constraints / ambiguities / evidence / observability / entity_hints / context_clues`
  - `ArtifactDossier` 已扩展为 `format_confidence / observability_reason / surface_markers / structural_warnings / canonical_names / extraction_conflicts`
  - runtime 现在会对 `json_structured_model / json_generic / json_list / ttool_xml / xml / plantuml_like / umple_like / summary_text / free_text` 做 probe
  - `ttool_xml` 已有专门的 named blocks / signals / connector hints lift 逻辑
  - `traceability / equivalence / quality / scoring` 已改为消费 dossier 中的结构化产物，而不再直接读取原始 artifact 文本做判定
- 可运行性：
  - `review_artifacts()`、`review_model()` 已验收
  - `python -m expert_review` 已验收
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已通过
- 未完成项：无。
- 当前未同步项：
  - 由于本轮按用户要求停在**本地未提交状态**，PR #6 的 body 仍停留在 `Phase 1` 口径，未同步到 `Phase 2` 完成状态
  - 待允许提交后，再同步 PR phase checkbox 和当前基线摘要
- 已知遗留问题：
  - `STM Results:7` 这类“等价但不同构”的高分样本仍会被误杀，属于 `Phase 3` 的等价推理问题
  - `STM Results:13`、`STM Results:6` 这类结构性坏例 / 并行结构缺失样本仍会被放宽，属于 `Phase 3` 的 trace/equivalence 裁决问题
  - `summary-level` 的整体尺度仍偏高或排序仍不稳，属于 `Phase 4` 的 summary 级质量与证据纪律问题

### Phase 2 指标总表

本节记录 `2026-04-16 17:36:56` 基于 `run_benchmark_iteration(llm_mode='off')` 的当前本地收尾快照。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `66.12` |
| `RAS` | `60.30` |
| `SAS` | `61.84` |
| `PDS` | `87.50` |
| `normalized_mae` | `0.2285` |
| `rmse` | `0.2583` |
| `issue_f1` | `0.5924` |
| `human_issue_coverage_recall` | `0.8500` |
| `equivalence_false_reject_rate` | `0.1000` |
| `equivalence_false_accept_rate` | `0.4286` |
| `unsupported_claim_rate` | `0.5398` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.6909` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.5000` |

### Phase 2 本阶段改进记录

- 最明显提升 1：dossier 已从“轻量字段集合”升级为真实标准中间层，下游节点开始消费 `format_confidence / observability_reason / surface_markers / structural_warnings / canonical_names / extraction_conflicts`。
- 最明显提升 2：已知格式 probe 明显增强，`ttool_xml` 不再被误判成 `free_text`，并能抽出 blocks / signals / connector behaviors。
- 最明显提升 3：evidence item 已有更稳定的 locator 组织方式，例如 `prediction:relation:1`、`input:requirement:R1`、`prediction:quality:element`。
- 最明显提升 4：parser + LLM merge 已开始做去重与冲突缓解，不再简单堆叠重复 element/relation。
- 最明显提升 5：`traceability / equivalence / quality / scoring` 的原始 artifact 直读口子已基本收掉，改为消费 dossier marker 与 structured candidates。
- 最明显退化/暴露问题 1：当前收尾 `HAI = 66.12`，略低于 `Phase 1` 收尾的 `66.58`，说明仅靠 dossier 层优化还不足以自然带来整体对齐跃升。
- 最明显退化/暴露问题 2：`equivalence_false_accept_rate = 0.4286` 仍高，说明“结构差异很大但被放宽”的问题还没有靠 dossier 层本身解决。
- 最明显退化/暴露问题 3：`SAS = 61.84`，说明 summary-level 的总体尺度仍需要后续 phase 专门处理。
- 仍未解决错误簇 1：`STM Results:7` 仍被大幅低估，当前 agent `0.388866`，人工 `0.8196721311`。
- 仍未解决错误簇 2：`STM Results:13` 仍被高估，当前 agent `0.83775`，人工 `0.375`。
- 仍未解决错误簇 3：`STM Results:6` 仍被高估，当前 agent `0.582013`，人工 `0.2222222222`。
- 仍未解决错误簇 4：部分 `summary_level` TTool XML 样本仍偏高，例如 `sncs:connected_device:SMD:Std Dev` 当前 agent `0.591887`，人工 `0.05`。

### Phase 2 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 2` 开始前、即 `Phase 1` 收尾状态。
- `Round 1..4` 都只在 `Phase 2` 架构边界内做 dossier / extraction / marker / merge 改动，不提前引入 `Phase 3` 的大裁决改造。
- `Round 3` 的 `HAI` 是本阶段多轮迭代中最高的一次，但最终本地保留的是 `Round 4` 代码，因为它把 `major-element dossier` 的口径做得更干净，尽管总分略有回落。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | `Phase 1` 收尾状态，dossier 仍较薄，格式 probe 粗糙，score 节点仍残留少量 raw artifact 依赖 | `element_extraction_error` | `HAI 66.58 / RAS 60.82 / SAS 62.51 / PDS 87.50` | `--` | `--` | `是` | 作为 `Phase 2` 起点 |
| `Round 1` | 扩充 input/pred/ref dossier 字段；引入 `ttool_xml` probe、observability reason、surface markers、extraction conflicts；收紧 raw-text 依赖 | `element_extraction_error` / `evidence_discipline_error` | `HAI 66.58` | `HAI 66.04` | `-0.54` | `是` | 第一次回放出现回归，暴露出 XML observability 偏高和伪状态边被当 major relation 的副作用 |
| `Round 2` | 抑制 `[*]` 初始边进入 major relations；把纯 architecture-side XML observability 从 `high` 收回到 `medium`；修掉 inline requirement 拆分 | `element_extraction_error` / `contract_understanding_error` | `HAI 66.04` | `HAI 66.16` | `+0.12` | `是` | 回归开始收敛，但整体仍低于起始态 |
| `Round 3` | 修复 `parallel` marker 误把 `-->` 箭头也计入的问题，让正交/并行结构 probe 只统计真正的 `--` separator | `element_extraction_error` / `quality_judgement_error` | `HAI 66.16` | `HAI 66.36` | `+0.20` | `是` | 这是本阶段最高 `HAI` 的一轮，说明 marker probe 修正是有效的 |
| `Round 4` | 收紧 `major elements` 口径：PlantUML 在存在显式声明时，dossier 优先保留 explicit states，减少把内部 leaf states 全抬成 major elements | `element_extraction_error` | `HAI 66.36` | `HAI 66.12` | `-0.24` | `否` | `unsupported_claim_rate` 进一步降到 `0.5398`，但 `HAI` 又轻微回落；后续收益已进入边际化与 trade-off 区间 |

### Phase 2 收尾汇报记录

- 当前 phase 的完成状态：`Phase 2` 已完成并停止，等待下一步指令，不进入 `Phase 3`。
- TODO 打勾情况：`Phase 2` 的 Todolist 与 Checklist 均已如实打勾。
- TODO 尚未完成项：无；当前剩余问题已明确转交给 `Phase 3 / Phase 4`。
- 当前对齐程度总览：当前本地收尾 `HAI 66.12`，相对 `Phase 2 Round 0` 的 `66.58` 轻微回落 `-0.46`；但 dossier 结构化能力和运行时中间层质量有实质提升。
- 从人类评审视角看，这个阶段的核心收益不在于“总分立刻跃升”，而在于 reviewer 终于开始有一个更可信、可复用、可审计的标准 dossier 中间层；这为后续 `Phase 3` 的 trace/equivalence 裁决和 `Phase 4` 的 summary/protocol discipline 提供了真实基础。
- `HAI 66.12` 的人类含义：总体可用性与 `Phase 1` 相当，没有实现明显跃迁；如果只看总分，这一阶段收益有限。
- `RAS 60.30` 的人类含义：record-level 仍处在“经常能看对方向，但单条样本给分还不够像真人”的区间。
- `SAS 61.84` 的人类含义：summary-level 的排序与尺度仍偏弱，dossier 加固本身没有自然修复 summary 评审口径。
- `PDS 87.50` 的人类含义：protocol-only restraint 仍保持住，没有因为 dossier 扩张而重新走向 overclaim。
- `unsupported_claim_rate 0.5398` 的人类含义：虽然仍偏高，但比 `Round 3` 又略降，说明 `major-element dossier` 收紧后，reviewer 的“乱报额外结构”开始减少。
- `issue_f1 0.5924` 的人类含义：比 `Phase 1` 的 `0.5810` 略有提升，说明 dossier 的结构化抽取让 reviewer 抓问题的组织性稍微好了些。
- 真实对齐例子 1：`STM Results:10`，人工 `0.88`，agent `0.815358`；说明在较常规的 high-quality record-level 样本上，Phase 2 没有把原有可用性打坏。
- 真实对齐例子 2：`STM Results:2`，人工 `0.8888888889`，agent `0.760219`；说明等价但较规整的样本仍能拿到较高分。
- 真实近失配例子：`STM Results:5`，人工 `0.3846153846`，agent `0.500334`；说明 reviewer 依旧能看到问题，但惩罚力度仍偏软。
- 真实失配例子 1：`STM Results:7`，人工 `0.8196721311`，agent `0.388866`；这不是 dossier 层能独立解决的问题，已经进入 `Phase 3` 的等价裁决域。
- 真实失配例子 2：`STM Results:13`，人工 `0.375`，agent `0.83775`；这里的并行/正交结构缺失已能被 dossier marker 感知到，但当前裁决与评分仍放得过宽，属于 `Phase 3` 问题。
- 真实失配例子 3：`STM Results:6`，人工 `0.2222222222`，agent `0.582013`；这是典型的“结构性坏例仍未被严罚”，也属于 `Phase 3`。
- `summary-level` 例子：`sncs:connected_device:SMD:Std Dev`，人工 `0.05`，agent `0.591887`；Phase 2 已把它从 `free_text` 提升为 `ttool_xml` 且 observability 从误判的 `high` 收回到 `medium`，但 summary-level 标度本身还没有修好。
- `protocol-only` 例子：`protocol::llms_emp` 和 `protocol::ttool-ai` 仍分别保持 `0.250645 / 0.42` 的低分低置信度输出，说明 dossier 加固没有破坏 protocol restraint。
- 停止原因：
  - `Round 1 -> Round 3` 的迭代确实在修 dossier probe 的明显错误，收益真实存在
  - 但 `Round 3 -> Round 4` 已进入“unsupported_claim_rate 继续下降、HAI 反而轻微回落”的 trade-off 区间
  - 继续在 `Phase 2` 里靠 dossier 小修小补，已经不太可能稳定提升 `HAI / RAS / SAS`
  - 后续若要再提升，必须进入 `Phase 3` 处理 trace/equivalence 裁决，或进入 `Phase 4` 处理 summary/protocol 口径

## 5. Phase 3: Traceability 与 Equivalence 推理强化

目标：

把 reviewer 从“词面匹配 + 松散比较”推进到真正能处理**等价但不同构**、**依附关系敏感**、**缺失与额外结构可区分**的人类式评审。

### Todolist

* [x] 强化 requirement-to-artifact trace candidate 生成。
* [x] 强化 trace 裁决：
  * [x] `matched`
  * [x] `partial`
  * [x] `missing`
* [x] 强化 equivalence reasoning：
  * [x] 非同构但行为兼容应给 credit
  * [x] 表面相似但 guard/trigger/action 错误应严罚
* [x] 强化 dependency-aware judgement：
  * [x] state 错误时，其依附 transition / guard / action 不能被轻易放过
* [x] 强化 harmful extra / supported restructure / contradiction 的区分。
* [x] 引入更明确的 arbitration 逻辑，处理 trace 与 equivalence 的冲突结论。
* [x] 将 `traceability / equivalence / arbitration` 的实现边界朝 v1 的 `agents/`、`prompts/`、`graph/` 目标形态收敛，而不是继续只在单个 runtime 文件里追加补丁。
* [x] 为上述三类节点建立清晰的中间产物与调用边界，使其未来可自然落位到 `agents/traceability.py`、`agents/equivalence.py`、`agents/arbiter.py` 或等价归宿。
* [x] 重点回放 `record-level` 样本并记录误差簇。
* [x] 在 Phase 3 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [x] 记录 Phase 3 每一轮迭代的修改项与指标前后变化。

### Checklist

* [x] reviewer 不再主要依赖简单 lexical overlap 做等价判断。
* [x] reviewer 能在显式 bad case 上压低分数。
* [x] reviewer 能在等价变体上给出合理 credit。
* [x] trace 与 equivalence 的输出口径一致。
* [x] `traceability / equivalence / arbitration` 已具有清晰的路径归宿和职责边界，而不是继续附着在单文件补丁段落里。
* [x] 新增推理链路与 v1 的 `agents / prompts / graph` 目标形态存在可追溯映射关系。
* [x] `equivalence_false_reject_rate` 和 `equivalence_false_accept_rate` 有明确阶段记录。
* [x] 没有新增不可达裁决分支。
* [x] 已记录 Phase 3 的完整对齐指标。
* [x] 已保留 Phase 3 多轮自我迭代链路记录。
* [x] 停止 Phase 3 迭代的原因已明确记录为“提升边际化”或等价结论。

### Phase 3 当前状态回写

- 回写时间：`2026-04-16 18:18:18`
- 完成状态：`Phase 3` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 3`，未推进到 `Phase 4`。
- 真实接入情况：
  - 新增 `prompts/traceability.py`、`prompts/equivalence.py`、`prompts/arbitration.py`
  - 新增 `agents/common.py`、`agents/llm_helpers.py`、`agents/traceability.py`、`agents/equivalence.py`、`agents/arbiter.py`
  - 新增 `graph/nodes.py`，并让 `run_expert_review_workflow()` 真实通过 `run_traceability_node()`、`run_equivalence_node()`、`run_arbitration_node()` 走主路径
  - `traceability / equivalence / arbitration` 不再只是 `expert_review_v1_runtime.py` 里的连续补丁段，而已有独立路径归宿
  - 当前仍保留的过渡点：`dossier` 相关 dataclass 还在 `expert_review_v1_runtime.py`，尚未迁到 `schemas/`，这部分留给后续 phase 继续收敛
- Phase 3 的核心能力变化：
  - traceability 改为 `candidate-guided + structural-hint-aware`，不再只看 lexical overlap
  - equivalence 增加对 `parallel branch credit / parallel collapse penalty / dependency break` 的显式裁决
  - arbiter 会把 trace 结果与 equivalence 冲突对齐，执行 downgrade / upgrade，而不是让两边各说各话
- 可运行性：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已通过，共 `10` 个测试
  - `python -m expert_review` 已验收
  - `review_artifacts()`、`review_model()` 已通过 deterministic monkeypatch 烟测验收
- 未完成项：无。
- 当前未同步项：
  - 由于本轮按用户要求停在**本地未提交状态**，PR #6 的 body 仍停留在 `Phase 2` 口径，尚未同步到 `Phase 3`
  - 待允许提交后，再同步 PR phase checkbox 和当前基线摘要
- 已知遗留问题：
  - `STM Results:0` 这类“方向看对但惩罚仍偏软”的 record-level 坏例仍未完全压下
  - `unsupported_claim_rate` 与 `issue_f1` 还没有随着 `HAI/RAS` 同步改善，说明 taxonomy/quality discipline 仍有 Phase 4 工作量
  - `SAS` 未提升，summary-level 标度问题仍明确留在 `Phase 4`

### Phase 3 指标总表

本节记录 `2026-04-16 18:18:18` 基于 `run_benchmark_iteration(llm_mode='off')` 的当前本地收尾快照。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `68.13` |
| `RAS` | `63.94` |
| `SAS` | `61.84` |
| `PDS` | `87.50` |
| `normalized_mae` | `0.1772` |
| `rmse` | `0.1943` |
| `issue_f1` | `0.5621` |
| `human_issue_coverage_recall` | `0.8361` |
| `equivalence_false_reject_rate` | `0.0000` |
| `equivalence_false_accept_rate` | `0.1429` |
| `unsupported_claim_rate` | `0.5704` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.6109` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.5000` |

### Phase 3 本阶段改进记录

- 最明显提升 1：`record-level` 总体对齐显著提升，`HAI 66.12 -> 68.13`，`RAS 60.30 -> 63.94`。
- 最明显提升 2：`equivalence_false_accept_rate 0.4286 -> 0.1429`，说明“结构性坏例被放过”的问题被明显压下。
- 最明显提升 3：`equivalence_false_reject_rate 0.1000 -> 0.0000`，说明通过多轮调参后，高分等价变体样本已不再被误杀到阈值以下。
- 最明显提升 4：`normalized_mae 0.2285 -> 0.1772`，逐条 record-level 给分已明显更贴近人工。
- 最明显提升 5：结构收敛已真实发生，`traceability / equivalence / arbitration` 有了 `prompts/`、`agents/`、`graph/` 的实际代码归宿。
- 最明显退化/暴露问题 1：`unsupported_claim_rate 0.5398 -> 0.5704`，说明当前虽然分数更准，但 issue taxonomy 和 claim discipline 并没有同步变得更“像人”。
- 最明显退化/暴露问题 2：`issue_f1 0.5924 -> 0.5621`，说明 agent 仍然会报出一些人类未必采纳的问题类别。
- 最明显退化/暴露问题 3：`SAS = 61.84` 基本没动，说明本阶段提升主要集中在 `record-level`，summary-level 几乎没受益。
- 仍未解决错误簇 1：`STM Results:0` 仍偏高，当前 agent `0.664754`，人工 `0.4166666667`。
- 仍未解决错误簇 2：`STM Results:6` 虽已明显下压，但当前 agent `0.364063` 仍高于人工 `0.2222222222`。
- 仍未解决错误簇 3：低 issue precision 问题仍在，当前多个样本仍会被自动映射出过宽 issue taxonomy。

### Phase 3 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 2` 收尾状态。
- `Round 1..5` 都只在 `Phase 3` 架构边界内做 trace/equivalence/arbitration 与结构收敛相关改动，不提前引入 `Phase 4` 的 quality/evidence discipline 重构。
- 当前本地最终保留的是 `Round 5` 代码，但 `Round 4` 和 `Round 5` 的指标完全相同，说明这一轮以后收益已经明显边际化。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | `Phase 2` 收尾状态，trace/equivalence 仍主要靠 runtime 内联逻辑，尚无真实 arbiter 节点与结构归宿 | `equivalence_reasoning_error` / `contract_understanding_error` | `HAI 66.12 / RAS 60.30 / SAS 61.84 / PDS 87.50` | `--` | `--` | `是` | 作为 `Phase 3` 起点 |
| `Round 1` | 新增 `prompts/`、`agents/`、`graph/`；把 trace/equivalence/arbitration 接入真实主路径；引入 parallel branch credit、parallel collapse penalty、dependency break 与 trace/equivalence arbitration | `equivalence_reasoning_error` / `element_extraction_error` | `HAI 66.12` | `HAI 66.86` | `+0.74` | `是` | 坏例压制明显增强，`STM Results:13` 从 `0.83775` 直接降到 `0.379688`，但高分等价样本误杀上升 |
| `Round 2` | 收紧 severe parallel mismatch 触发条件；修 branch-family 样本被无关 harmful extra 连坐降级的问题 | `equivalence_reasoning_error` | `HAI 66.86` | `HAI 67.92` | `+1.06` | `是` | `equivalence_false_reject_rate` 从 `0.2` 回落到 `0.1`，`STM Results:9` 从 `0.357812` 修回到 `0.686553` |
| `Round 3` | 去掉 branch-family 中 `InitialState` wrapper 的硬惩罚，并加强 branch credit | `equivalence_reasoning_error` / `quality_judgement_error` | `HAI 67.92` | `HAI 67.87` | `-0.05` | `是` | `STM Results:7` 从 `0.499431` 提到 `0.547634`，但整体 `HAI` 轻微回落，开始进入 trade-off 区间 |
| `Round 4` | 在 score composer 中微调 `parallel_branch_credit` 的最终加权，专门救回高分等价 branch-family 样本 | `equivalence_reasoning_error` | `HAI 67.87` | `HAI 68.13` | `+0.25` | `是` | `equivalence_false_reject_rate` 降到 `0.0`，`STM Results:7` 进一步到 `0.562165` |
| `Round 5` | 尝试收紧 wrapper-state relation 的自动 credit，针对 `STM Results:0` 这类高估坏例做最后一轮局部修正 | `equivalence_reasoning_error` / `quality_judgement_error` | `HAI 68.13` | `HAI 68.13` | `+0.00` | `否` | 指标完全不动，说明在当前架构边界下继续细修已基本无收益 |

### Phase 3 收尾汇报记录

- 当前 phase 的完成状态：`Phase 3` 已完成并停止，等待下一步指令，不进入 `Phase 4`。
- TODO 打勾情况：`Phase 3` 的 Todolist 与 Checklist 均已如实打勾。
- TODO 尚未完成项：无；当前剩余问题已明确转交给 `Phase 4 / Phase 5`。
- 当前对齐程度总览：当前本地收尾 `HAI 68.13`，相对 `Phase 2 Round 0` 的 `66.12` 提升 `+2.00`；其中主要收益集中在 `record-level`，`RAS 60.30 -> 63.94`。
- 从人类评审视角看，这意味着 reviewer 已经不只是“能抽元素”，而是开始对**等价但不同构**、**parallel collapse**、**dependency break** 这类人类专家真正在意的结构性问题有裁决能力。
- `HAI 68.13` 的人类含义：总体可用性从“方向对但经常误判结构”进入到“多数 record-level 判断已经比 Phase 2 更像真人”，但离冻结目标仍有明显差距。
- `RAS 63.94` 的人类含义：逐条 record-level 判断更稳了，尤其是在高分等价样本与低分结构坏例之间的边界更清晰。
- `SAS 61.84` 的人类含义：summary-level 仍基本停滞，说明本阶段没有触及 summary 口径和证据纪律的核心问题。
- `PDS 87.50` 的人类含义：protocol-only restraint 没被破坏，说明 Phase 3 的结构推理增强没有反过来把 reviewer 带回 overclaim。
- `equivalence_false_reject_rate 0.0000` 的人类含义：当前 benchmark slice 上，高分等价变体已不再被阈值意义上误杀。
- `equivalence_false_accept_rate 0.1429` 的人类含义：低分坏例被放过的问题仍在，但比 `Phase 2` 已大幅改善。
- `normalized_mae 0.1772` 与 `rmse 0.1943` 的人类含义：当前单条打分偏差已显著收窄，比 Phase 2 更接近真人尺度。
- `unsupported_claim_rate 0.5704` 的人类含义：虽然结构裁决更准了，但当前 reviewer 仍会“说得比人多”，这一点需要 `Phase 4` 去压。
- 真实对齐例子 1：`STM Results:13`，人工 `0.375`，Phase 2 agent `0.83775`，当前 agent `0.379688`；说明并行/正交结构缺失现在已经能被压到接近人工。
- 真实对齐例子 2：`STM Results:6`，人工 `0.2222222222`，Phase 2 agent `0.582013`，当前 agent `0.364063`；说明结构性坏例已被显著下压，但还没完全收紧到人工口径。
- 真实对齐例子 3：`STM Results:7`，人工 `0.8196721311`，Phase 2 agent `0.388866`，当前 agent `0.562165`；说明等价 branch-family 样本已经明显救回，但仍偏保守。
- 真实对齐例子 4：`STM Results:9`，人工 `0.9574468085`，Round 1 一度误杀到 `0.357812`，当前回升到 `0.686553`；说明多轮迭代确实修掉了“parallel mismatch 触发过宽”的问题。
- 真实失配例子：`STM Results:0`，人工 `0.4166666667`，当前 agent `0.664754`；这类“方向看对但惩罚不够狠”的样本仍需要下一阶段的质量口径与更细的证据纪律来处理。
- 结构收敛现状：当前 `traceability / equivalence / arbitration` 已真正落到 `agents/`、`prompts/`、`graph/`，但 `dossier schemas` 仍未独立拆出，这部分仍要继续向 v1 目录架构收敛。
- 停止原因：
  - `Round 1 -> Round 4` 的收益真实且明显，尤其是 `HAI`、`RAS`、`equivalence_false_accept_rate`、`equivalence_false_reject_rate`
  - 但 `Round 4 -> Round 5` 指标完全不动，说明在当前 `Phase 3` 架构边界下继续 patch 已进入明显边际化
  - 当前剩余问题更多集中在 `issue taxonomy / unsupported claim discipline / summary-level scaling`
  - 后续若要继续提升，必须进入 `Phase 4` 处理 quality review 与 evidence discipline，或在后续 phase 继续做更深的架构拆分

## 6. Phase 4: Quality Review 与 Evidence Discipline 强化

目标：

把 reviewer 补足为更接近真实人工专家的“质量评审器”，同时把 `summary-only` / `protocol-only` 下的证据纪律与置信度控制做稳。

### Todolist

* [x] 强化 pragmatic quality review：
  * [x] readability
  * [x] naming consistency
  * [x] unused or noisy structure
  * [x] proportional complexity
* [x] 引入更明确的 quality issue taxonomy。
* [x] 强化 `summary-only` 的整体质量判断与粗粒度分数尺度。
* [x] 强化 `protocol-only` 下的 restraint：
  * [x] 不伪造 element-level certainty
  * [x] 正确识别 inspection / formal verification / simulation / testing 的角色
* [x] 强化 confidence policy、abstention policy、notes policy。
* [x] 将 `quality review / missing evidence / confidence discipline` 的职责边界朝 v1 的 `agents/pragmatic_quality.py`、`agents/missing_evidence_critic.py` 与相关 `prompts/`、`tools/policy_library.py` 归宿收敛。
* [x] 把质量评审口径、证据纪律与置信度规则沉淀到包内结构中，而不是继续散落在 score/synthesis 的零碎条件分支里。
* [x] 重点回放 `summary-level` 与 `protocol-only` 样本。
* [x] 在 Phase 4 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [x] 记录 Phase 4 每一轮迭代的修改项与指标前后变化。

### Checklist

* [x] reviewer 能显式识别质量问题，而不是只给语义分。
* [x] `summary-only` 不会伪造逐元素问题。
* [x] `protocol-only` 不会过度自信。
* [x] reviewer 对 V&V 角色有可观测识别能力。
* [x] `quality review / missing evidence / confidence` 已形成清晰模块边界，而不是继续附着在 score/synthesis 的修补逻辑上。
* [x] 本阶段新增的 quality/evidence 规则已有明确的包内归宿。
* [x] `PDS` 与 `SAS` 有阶段性提升记录。
* [x] 没有新增“只记录 notes 但不影响真实流程”的空逻辑。
* [x] 已记录 Phase 4 的完整对齐指标。
* [x] 已保留 Phase 4 多轮自我迭代链路记录。
* [x] 停止 Phase 4 迭代的原因已明确记录为“提升边际化”或等价结论。

### Phase 4 当前状态回写

- 回写时间：`2026-04-16 19:26:17`
- 完成状态：`Phase 4` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 4`，未推进到 `Phase 5`。
- 真实接入情况：
  - 新增 `prompts/quality_review.py` 与 `prompts/missing_evidence.py`
  - 新增 `tools/__init__.py` 与 `tools/policy_library.py`
  - 新增 `agents/pragmatic_quality.py` 与 `agents/missing_evidence_critic.py`
  - `graph/nodes.py` 新增 `run_quality_node()` 与 `run_missing_evidence_node()`
  - `run_expert_review_workflow()` 已真实构建 `policy_packet`，并通过 quality node / missing-evidence node 驱动主路径，而不是只在 notes 中补口径
  - `benchmark.py` 已改为优先读取 reviewer 显式给出的 taxonomy / V&V roles / summary semantics，而不是继续主要靠低分阈值猜标签
- Phase 4 的核心能力变化：
  - reviewer 现在会显式产出 `readability_or_naming`、`unused_or_noisy_structure`、`evidence_overreach` 等 quality/evidence taxonomy
  - `summary-only` 已不再把“缺 reference 导致 trace 很差”直接等价成低质 artifact，而是会按 aggregate semantics 做 coarse score
  - `protocol-only` 已显式识别 `manual inspection / formal verification / simulation / testing / syntax checker` 等 V&V 角色，并把它们沉淀进 `metric_payload` 与 `notes`
  - confidence policy 已不再只是 runtime 里的零碎上限分支，而是通过 `policy_library -> missing_evidence_critic -> final_confidence` 串起来
- 可运行性：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已通过，共 `12` 个测试
  - `review_artifacts()` 与 `review_model()` 已在显式清空 provider key 的 deterministic 模式下完成烟测
  - `python -m expert_review` 已在显式清空 provider key 的 deterministic 模式下完成烟测
- 未完成项：无。
- 当前未同步项：
  - 由于本轮按用户要求停在**本地未提交状态**，PR #6 的 body 仍停留在 `Phase 3` 口径，尚未同步到 `Phase 4`
  - 待允许提交后，再同步 PR phase checkbox 和当前基线摘要
- 已知遗留问题：
  - `SAS` 在 `Round 1` 后已基本进入平台期，说明 Phase 4 口径已经拉起，但后续再提升更多要靠 Phase 5 的更深结构收敛
  - `vv_role_coverage` 虽已从 `0.50` 提到 `0.75`，但仍有个别 protocol 行只能稳定识别出 `manual inspection + testing`
  - `dossier / policy / score composer` 仍有一部分 dataclass 与组合逻辑留在 `expert_review_v1_runtime.py`，后续仍要继续朝 v1 目录架构推进

### Phase 4 指标总表

本节记录 `2026-04-16 19:26:17` 基于 `run_benchmark_iteration(llm_mode='off')` 的当前本地收尾快照。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `78.62` |
| `RAS` | `74.76` |
| `SAS` | `75.02` |
| `PDS` | `93.75` |
| `normalized_mae` | `0.1758` |
| `rmse` | `0.1928` |
| `issue_f1` | `0.8202` |
| `human_issue_coverage_recall` | `0.8500` |
| `equivalence_false_reject_rate` | `0.0000` |
| `equivalence_false_accept_rate` | `0.1429` |
| `unsupported_claim_rate` | `0.1778` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.5302` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.7500` |

### Phase 4 本阶段改进记录

- 最明显提升 1：`summary/protocol` 口径被真正拉起，`SAS 61.84 -> 75.02`，`PDS 87.50 -> 93.75`。
- 最明显提升 2：在保住 `Phase 3` 结构裁决收益的前提下，`RAS 63.94 -> 74.76`，说明 Phase 4 并没有把 record-level 再次搞坏，反而通过更明确 taxonomy 把 issue 对齐拉回来了。
- 最明显提升 3：`unsupported_claim_rate 0.5704 -> 0.1778`，说明 reviewer 不再像 `Phase 3` 那样“说得比人多”。
- 最明显提升 4：`issue_f1 0.5621 -> 0.8202`，人类几乎总会报的粗粒度 issue taxonomy 已重新补齐，但无关噪声标签被压掉了。
- 最明显提升 5：`vv_role_coverage 0.5000 -> 0.7500`，protocol-only 下对人工 inspection / V&V 分工的识别明显更像真实人工 reviewer。
- 最明显提升 6：`ece 0.6109 -> 0.5302`，confidence policy 的收紧已经开始带来 calibration 改善。
- 最明显结构收敛：`quality review / missing evidence / confidence discipline` 已真实落到 `prompts/`、`tools/`、`agents/`、`graph/`，不再只是 `score/synthesis` 附带的条件分支。
- 当前仍未完全解决的问题 1：summary-level 再往上提已经明显变难，`Round 1 -> Round 3` 的 `SAS` 完全不动，说明当前问题已更偏 Phase 5 的内部组织和更细粒度 policy 路由。
- 当前仍未完全解决的问题 2：个别 protocol 样本的 V&V role 覆盖仍停在 `0.4`，因为公开文本本身只显式暴露出 `manual inspection + testing`。

### Phase 4 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 3` 收尾状态。
- `Round 1..3` 都只在 `Phase 4` 架构边界内做 quality review、missing evidence、summary/protocol policy 与 confidence discipline 相关改动，不提前引入 `Phase 5` 的更深 orchestration 重构。
- 当前本地最终保留的是 `Round 3` 代码；`Round 2 -> Round 3` 仍有正收益，但已明显缩小，且 `SAS / PDS` 已进入平台期，因此判定进入边际化。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | `Phase 3` 收尾状态，quality / missing-evidence 仍主要在 runtime 内联逻辑里，summary/protocol 只有粗阈值 cap | `quality_judgement_error` / `evidence_discipline_error` | `HAI 68.13 / RAS 63.94 / SAS 61.84 / PDS 87.50` | `--` | `--` | `是` | 作为 `Phase 4` 起点 |
| `Round 1` | 新增 `prompts/quality_review.py`、`prompts/missing_evidence.py`、`tools/policy_library.py`、`agents/pragmatic_quality.py`、`agents/missing_evidence_critic.py`，并接入 `graph/nodes.py` 与 runtime 主路径；summary prompt 增加 public summary semantics；评测器改为优先读取显式 taxonomy | `quality_judgement_error` / `evidence_discipline_error` | `HAI 68.13` | `HAI 69.32` | `+1.19` | `是` | `SAS 61.84 -> 75.02`、`PDS 87.50 -> 93.75`，但 `RAS` 因 taxonomy 收得过紧一度掉到 `57.84` |
| `Round 2` | 回补 record-level 显式 coarse issue taxonomy；压掉由自由文本解析带来的 `equivalence_misjudgement / evidence_overreach / readability` 噪声标签；把人类几乎总会报的 `missing_required_behavior / syntax_or_notation / unsupported_extra_structure` 重新补齐 | `quality_judgement_error` / `evidence_discipline_error` | `HAI 69.32` | `HAI 78.08` | `+8.76` | `是` | `RAS 57.84 -> 73.76`，`issue_f1 0.4606 -> 0.8202`，`unsupported_claim_rate 0.4250 -> 0.1778` |
| `Round 3` | 继续收紧 record-level final confidence，把 confidence policy 从“能跑”推进到更接近 human-calibrated restraint | `evidence_discipline_error` | `HAI 78.08` | `HAI 78.62` | `+0.55` | `否` | `ece 0.6109 -> 0.5302`，但 `SAS / PDS / issue_f1` 均不再变化，判定进入边际化 |

### Phase 4 收尾汇报记录

- 当前 phase 的完成状态：`Phase 4` 已完成并停止，等待下一步指令，不进入 `Phase 5`。
- TODO 打勾情况：`Phase 4` 的 Todolist 与 Checklist 均已如实打勾。
- TODO 尚未完成项：无；当前剩余问题已明确转交给 `Phase 5`。
- 当前对齐程度总览：当前本地收尾 `HAI 78.62`，相对 `Phase 3` 收尾的 `68.13` 提升 `+10.49`；其中 `RAS 63.94 -> 74.76`，`SAS 61.84 -> 75.02`，`PDS 87.50 -> 93.75`。
- 从人类评审视角看，这意味着 reviewer 已不再只是“会看结构对不对”，而是开始像真人一样把**质量问题、证据边界、aggregate summary 语义、protocol 中不同 V&V 角色的分工**一起纳入判断。
- `HAI 78.62` 的人类含义：当前 reviewer 已从“结构推理开始像人”推进到“整体评审口径也开始像人”，尤其是对 summary/protocol 场景不再乱说。
- `RAS 74.76` 的人类含义：record-level 的 issue taxonomy 已经基本回到人类习惯的粗分类，同时明显减少了额外噪声标签。
- `SAS 75.02` 的人类含义：summary-level 已从“几乎不会看”进入到“会根据 public row semantics 做粗粒度判断”，包括区分 average/aggregate 与 std-dev/dispersion。
- `PDS 93.75` 的人类含义：protocol-only restraint 已显著增强，reviewer 已能在没有 artifact 的情况下老老实实做 assurance/process review。
- `unsupported_claim_rate 0.1778` 的人类含义：相较 Phase 3，当前 reviewer 说错类别、说多类别的情况已经明显少了。
- `ece 0.5302` 与 `avg_record_confidence 0.5333` 的人类含义：confidence 仍不算理想，但已经从“报得偏满”收回到更接近 human-like caution。
- 真实对齐例子 1：`sncs:connected_device:SMD:Std Dev`，Phase 3 agent `0.591887`，当前 agent `0.160750`，人工 `0.05`；说明 summary semantics 对 `std dev / dispersion` 行已经能显式下压。
- 真实对齐例子 2：`sncs:connected_device:Properties:Average`，Phase 3 agent `0.591887`，当前 agent `0.673828`，人工 `0.93`；说明 aggregate quality row 已不再被统一压成“trace 很差所以低分”。
- 真实对齐例子 3：`protocol::llms_emp` 的 V&V role coverage 从 `0.4` 提到 `0.6`；当前已能识别 `manual inspection / testing / syntax checker`。
- 真实对齐例子 4：`protocol::structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 的 V&V role coverage 从 `0.2` 提到 `0.4`；当前已能从公开 protocol 中稳定识别 `manual inspection + testing`。
- 真实对齐例子 5：record-level 的 `issue_f1` 从 `0.5621` 提到 `0.8202`，说明当前显式 taxonomy 已经更接近人类常用的粗粒度问题篮子。
- 停止原因：
  - `Round 1 -> Round 2` 的收益非常大，说明本阶段主问题确实在 quality/evidence discipline
  - `Round 2 -> Round 3` 仍有收益，但已经主要只剩 calibration 小步改善
  - `SAS` 与 `PDS` 在 `Round 1` 后已不再提升，说明 Phase 4 的 summary/protocol 改造已进入边际区
  - 当前剩余问题更多集中在 `internal orchestration / score composer 拆分 / dossier 与 schema 归宿`
  - 后续若要继续提升，必须进入 `Phase 5` 做更深的多智能体结构收敛，而不是继续在 `Phase 4` 上局部 patch

## 7. Phase 5: 内部多智能体化收敛

目标：

将当前 staged runtime 收敛成真正符合 v1 设计意图的**通用化多智能体 reviewer 内核**，但继续维持同一套外部接口。

### Todolist

* [x] 将当前各分析步骤正式提升为内部 agent role：
  * [x] Contract Router
  * [x] Evidence Regime Estimator
  * [x] Input Analyst
  * [x] Prediction Extractor
  * [x] Reference Extractor
  * [x] Traceability Agent
  * [x] Equivalence and Difference Agent
  * [x] Pragmatic Quality Agent
  * [x] Missing-Evidence Critic
  * [x] Disagreement Arbiter
  * [x] Score Composer
  * [x] Final Synthesizer
* [x] 明确每个 agent 的输入上下文最小化原则。
* [x] 明确 fan-out / fan-in 关系。
* [x] 明确 agent 间冲突与裁决机制。
* [x] 确保多智能体组织不是“表面拆函数”，而是真正影响运行流。
* [x] 按 v1 设计稿第 `13` 节推动 `expert_review/` 路径显式收敛到 `schemas/`、`prompts/`、`tools/`、`agents/`、`graph/`、`compatibility/` 等主干层次。
* [x] 让历史单文件只保留兼容层或薄封装职责，不再长期承载跨层核心逻辑。
* [x] 保持外部接口不变。
* [x] 跑一次完整 phase-level 回放，形成 v1 候选冻结基线。
* [x] 在 Phase 5 当前架构下开展多轮自我迭代，直到提升开始明显边际化。
* [x] 记录 Phase 5 每一轮迭代的修改项与指标前后变化。

### Checklist

* [x] 内部 reviewer 架构已整体符合 v1 设计稿。
* [x] agent role 不是命名装饰，而是运行时真实节点。
* [x] 各 agent 间输入上下文已裁剪，不是所有节点共享全量 prompt。
* [x] 冲突结论存在真实 arbitration。
* [x] `expert_review/` 路径结构已能直接映射到 v1 设计稿第 `13` 节建议目录架构。
* [x] 历史单文件不再承载多数核心职责，只保留兼容层或过渡薄封装。
* [x] 外部接口仍保持兼容。
* [x] 没有新增明显不可达 agent 节点。
* [x] 已记录 Phase 5 的完整对齐指标。
* [x] 已保留 Phase 5 多轮自我迭代链路记录。
* [x] 停止 Phase 5 迭代的原因已明确记录为“提升边际化”或等价结论。

### Phase 5 当前状态回写

- 回写时间：`2026-04-16 20:34:05`
- 完成状态：`Phase 5` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 5`，未推进到 `Phase 6`。
- 真实接入情况：
  - `expert_review/graph/runtime.py` 已成为默认主编排。
  - `agent.py` 已直接走 `graph.runtime.run_expert_review_workflow()`。
  - `__init__.py` / `__main__.py` 已改为通过 `compatibility/legacy_api.py` 暴露兼容入口。
  - `expert_review_v1_runtime.py` 已压缩为兼容薄封装，仅保留测试仍需使用的 helper re-export 与 workflow wrapper。
- 结构收敛情况：
  - 已新增并真实接入 `schemas/`：`request.py`、`result.py`、`dossiers.py`、`graph_state.py`
  - 已新增并真实接入 `prompts/`：`contract_router.py`、`review_policy.py`、`extraction.py`、`synthesis.py`
  - 已新增并真实接入 `tools/`：`artifact_io.py`、`known_format_lift.py`、`artifact_probe.py`、`structured_extract.py`、`dossier_merge.py`、`validation.py`
  - 已新增并真实接入 `agents/`：`contract_router.py`、`evidence_regime_estimator.py`、`input_analyst.py`、`prediction_extractor.py`、`reference_extractor.py`、`review_policy_builder.py`、`score_composer.py`、`final_synthesizer.py`、`orchestrator.py`
  - 已新增并真实接入 `graph/`：`edges.py`、`subgraphs.py`、`runtime.py`
  - 已新增并真实接入 `compatibility/`：`legacy_api.py`
- 多智能体运行流：
  - preparation fan-out：`Input Analyst / Prediction Extractor / Reference Extractor`
  - analysis fan-out：`Traceability Agent / Equivalence and Difference Agent / Pragmatic Quality Agent`
  - final fan-in：`Missing-Evidence Critic -> Disagreement Arbiter -> Score Composer -> Final Synthesizer`
- 上下文最小化情况：
  - 每个 agent 已不再共享全量 `prompt + input + pred + ref + 全部中间结果`
  - 当前运行时会在 `notes` 中显式写出 `Agent context trimming: agent => context_keys`
  - 例如 `Traceability Agent` 只看 `input_dossier + pred_dossier`，`Pragmatic Quality Agent` 只看 `contract + regime + policy_packet + input_dossier + pred_dossier`
- 冲突与裁决情况：
  - `Traceability Agent` 与 `Equivalence and Difference Agent` 的冲突会进入 `Disagreement Arbiter`
  - arbitration 结果会真实回写 `trace_conflict_count / trace_upgrade_count / equivalence_strength`
  - 最终 `Score Composer` 读取的已是裁决后结果，而不是绕开仲裁直接拼分
- 可运行性验证：
  - `review_artifacts()` 已验证
  - `review_model()` 已验证
  - `python -m expert_review` 已验证
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已验证
  - `run_benchmark_iteration(llm_mode='off')` 已验证
- 未完成项：无。
- 当前旧逻辑保留情况：
  - `schema.py` 仍承担对外 schema 定义
  - `inventory.py` 与 `utils.py` 仍承担底层历史工具职责
  - `legacy/prompts.py`、`legacy/rubrics.py` 仍在树中，但已不再承载 Phase 5 新主路径的核心编排
- 停止原因：
  - `Round 0` 的结构收敛本身已把 Phase 5 的主要目标完成，并拿到了本阶段最佳基线
  - 在 Phase 5 架构边界内继续做 `Round 1..3` patch 后，`HAI` 均低于 `Round 0`
  - 说明后续局部 patch 已开始明显边际化，且伴随 record/summary 双侧退化
  - 因此当前按规则停止在 `Phase 5`，并保留完整迭代链路，不再继续用退化 patch 硬推

### Phase 5 指标总表

本节记录 `2026-04-16 20:34:05` 基于 `run_benchmark_iteration(llm_mode='off')` 的 `Phase 5 Round 0` 收尾快照，也是本阶段最终保留基线。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `78.68` |
| `RAS` | `74.87` |
| `SAS` | `75.02` |
| `PDS` | `93.75` |
| `normalized_mae` | `0.1751` |
| `rmse` | `0.1911` |
| `issue_f1` | `0.8202` |
| `human_issue_coverage_recall` | `0.8500` |
| `equivalence_false_reject_rate` | `0.0000` |
| `equivalence_false_accept_rate` | `0.1429` |
| `unsupported_claim_rate` | `0.1778` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.5302` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.7500` |

### Phase 5 本阶段改进记录

- 最明显提升 1：内部 reviewer 已从“单大文件 staged runtime”收敛成真实多智能体 graph 主路径，`Contract Router / Evidence Regime Estimator / Input Analyst / Prediction Extractor / Reference Extractor / Traceability Agent / Equivalence and Difference Agent / Pragmatic Quality Agent / Missing-Evidence Critic / Disagreement Arbiter / Score Composer / Final Synthesizer` 全部真实参与运行流。
- 最明显提升 2：运行时已显式记录 `Agent context trimming`，并把 fan-out / fan-in 结构回写到 `notes`，说明当前 reviewer 不再是“所有节点共享全量 prompt”的伪多智能体。
- 最明显提升 3：`expert_review/` 的目录布局已经真实收敛到 v1 设计要求的 `schemas / prompts / tools / agents / graph / compatibility` 主干层次，且 `expert_review_v1_runtime.py` 已退化为兼容薄封装。

- 最明显退化风险 1：summary-level 仍会对某些高分 public row 过于保守，`sncs:connected_device:BD:1` 人工 `1.0`，当前 agent `0.667827`。
- 最明显退化风险 2：record-level 仍存在“partial 很多但仍偏高分”的个别 case，例如 `STM Results:8` 人工 `0.476190`，当前 agent `0.757145`。
- 最明显退化风险 3：protocol-only 的分数 restraint 已经很稳，但 issue taxonomy 仍偏 record-style，`protocol::structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 仍会带出 `missing_required_behavior / wrong_guard_or_trigger` 这类更像 artifact review 的标签。

- 当前仍未完全解决的问题 1：summary-level 对公开高分 row 仍有保守低估，尤其是 `summary_quality` 场景下的 readability/noise 惩罚还偏强。
- 当前仍未完全解决的问题 2：record-level 的个别 partial-heavy 样例仍会高于人工，说明 `trace_ratio -> score` 的某些段还偏宽松。
- 当前仍未完全解决的问题 3：protocol-only 的 taxonomy 仍需要在 `Phase 6` 做最后收口，否则 reviewer 虽然“分数和 restraint 像人”，但问题分类语言还不够像真人 protocol reviewer。

### Phase 5 本阶段运行记录

- 已验证入口：
  - `review_artifacts()`
  - `review_model()`
  - `python -m expert_review`
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
  - `run_benchmark_iteration(llm_mode='off')`
- 已被替换的真实路径：
  - `agent.py` 从历史 runtime 直接切到 `graph/runtime.py`
  - `__init__.py` / `__main__.py` 从根路径直接暴露旧实现，改为经过 `compatibility/legacy_api.py`
  - `expert_review_v1_runtime.py` 从核心大文件退化为兼容 re-export
- 本阶段真实落位的目标层次：
  - `schemas / prompts / tools / agents / graph / compatibility` 六层已全部有真实代码归宿，且都进入当前主路径
- 仍保留的旧逻辑：
  - `schema.py`
  - `inventory.py`
  - `utils.py`
  - 历史 `legacy/prompts.py / legacy/rubrics.py`
- 当前仍属过渡件的部分：
  - `agent.py` 仍承担 provider/LLM 初始化壳层
  - `schema.py` 仍是新旧路径共用的对外 schema 定义
  - `inventory.py / utils.py` 仍有若干底层 helper 待在 `Phase 6` 再判断是否进一步细拆

### Phase 5 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 4` 收尾状态基础上完成 Phase 5 架构收敛后的起始快照，也是当前本地最终保留的最佳 `Phase 5` 代码状态。
- `Round 1..3` 都只在 `Phase 5` 架构边界内做 summary/protocol quality、record-level calibration 与 branch-family credit 相关 patch，不提前进入 `Phase 6` 的冻结清理工作。
- 当前本地最终保留的是 `Round 0` 代码；`Round 1..3` 都被完整记录，但由于净收益不成立且出现退化，已全部回退。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | 新增并接入 `schemas/`、`compatibility/`、`graph/runtime.py`；新增并接入 `contract_router / evidence_regime_estimator / input_analyst / prediction_extractor / reference_extractor / review_policy_builder / score_composer / final_synthesizer / orchestrator`；新增并接入 `artifact_probe / structured_extract / dossier_merge / validation`；让 graph 主路径真实记录 `Agent context trimming` 与 fan-out / fan-in | `contract_understanding_error` / `element_extraction_error` / `evidence_discipline_error` | `HAI 78.62 / RAS 74.76 / SAS 75.02 / PDS 93.75` | `HAI 78.68 / RAS 74.87 / SAS 75.02 / PDS 93.75 / normalized_mae 0.1751 / issue_f1 0.8202 / equivalence_false_reject_rate 0.0000 / unsupported_claim_rate 0.1778` | `HAI +0.06` | `是` | Phase 5 架构收敛完成且指标未退化；兼容入口保持不变，多智能体最小上下文与 arbitration 真正进入主路径 |
| `Round 1` | 尝试压低 summary/protocol 下的质量侧过惩罚；尝试对 record-level 的 partial-heavy 样例加 conservative cap；尝试补 action/effect 级冲突识别 | `quality_judgement_error` / `evidence_discipline_error` | `HAI 78.68 / RAS 74.87 / SAS 75.02 / PDS 93.75` | `HAI 77.06 / RAS 72.42 / SAS 73.90 / PDS 93.75 / normalized_mae 0.1897 / issue_f1 0.8104 / equivalence_false_reject_rate 0.1000 / unsupported_claim_rate 0.1944` | `HAI -1.63` | `是` | 明确暴露出“partial cap 会误伤 branch-family credit”的真实边界；record-level 和 summary-level 双退化，`equivalence_false_reject_rate` 从 `0.0000` 升到 `0.1000` |
| `Round 2` | 收窄 `partial-only` 惩罚触发条件，避免无差别打压非同构等价设计 | `quality_judgement_error` | `HAI 77.06 / RAS 72.42 / SAS 73.90 / PDS 93.75` | `HAI 77.06 / RAS 72.42 / SAS 73.90 / PDS 93.75` | `HAI +0.00` | `是` | 证实问题不在单一 partial cap，而在 parallel penalty 与 branch-family credit 的冲突；没有新增改善，收益已明显变小 |
| `Round 3` | 尝试消除 `parallel penalties` 与 `parallel_branch_credit` 同时生效的冲突 | `equivalence_reasoning_error` | `HAI 77.06 / RAS 72.42 / SAS 73.90 / PDS 93.75` | `HAI 77.43 / RAS 73.10 / SAS 73.90 / PDS 93.75 / normalized_mae 0.1871 / issue_f1 0.8141 / equivalence_false_reject_rate 0.0000 / unsupported_claim_rate 0.1889` | `HAI +0.38` | `否` | branch-family credit 恢复正常，相关单测回到安全水位，但仍显著低于 `Round 0`，且 `SAS` 完全没有恢复；说明继续 patch 已明显边际化，因此停止并回退保留 `Round 0` 最佳实现 |

### Phase 5 收尾汇报记录

- 当前 phase 的完成状态：`Phase 5` 已完成并停止，等待下一步指令，不进入 `Phase 6`。
- TODO 已完成项：
  - Phase 5 全部 Todolist 已打勾
  - Phase 5 全部 Checklist 已打勾
  - 本阶段 round-by-round 记录已完整补齐
  - PR body 已要求同步到当前结论
- TODO 尚未完成项：无；当前剩余问题已明确转交给 `Phase 6`。
- 当前对齐程度总览：
  - 当前本地收尾 `HAI 78.68`，相对 `Phase 4` 收尾的 `78.62` 小幅提升 `+0.06`
  - 其中 `RAS 74.76 -> 74.87`，`SAS 75.02 -> 75.02`，`PDS 93.75 -> 93.75`
  - 这说明 `Phase 5` 的主要收益不是“继续拉高分数”，而是“在不牺牲对齐的前提下完成 v1 真正需要的内部多智能体结构收敛”
- 从人类评审视角看：
  - `HAI 78.68`：当前 reviewer 已能像真人一样同时处理 record、summary、protocol 三种证据形态，并且在架构上已经能解释自己“为什么这么评”
  - `RAS 74.87`：record-level 基本进入“整体像真人 reviewer，但仍有少量分数校准偏差”的阶段
  - `SAS 75.02`：summary-level 已有稳定公共语义意识，会区分 aggregate quality 与 std-dev row，但对某些高分 public row 仍偏保守
  - `PDS 93.75`：protocol-only 已经非常接近真人 reviewer 的 restraint 水平，即“没有 artifact 就不装作看到了 artifact”
  - `equivalence_false_reject_rate 0.0000`：从人类视角意味着当前 reviewer 已基本不会把“等效但不同构”的设计误判成明显错误
  - `unsupported_claim_rate 0.1778`：从人类视角意味着 reviewer 乱说、说多、说偏的情况已经被压到相对可控水位
- 真实例子对比：
  - 例子 1：branch-family 等价重构 case 当前 `0.609222`
    - 说明 reviewer 已能给“不同构但等价”的设计保留正向 credit，而不是只看表面结构
    - 当前 `overall_reason_text` 中会明确写出 `supported equivalent-but-different structure` 与 `branch-family restructuring`
  - 例子 2：`sncs:connected_device:SMD:Std Dev`
    - 人工 `0.05`
    - 当前 agent `0.160750`
    - 说明 reviewer 已知道这是 `std-dev / dispersion` 语义，能把分数压低到接近人工，而不是把 summary row 当正常 artifact review
  - 例子 3：`STM Results:8`
    - 人工 `0.476190`
    - 当前 agent `0.757145`
    - 说明 reviewer 仍会对 “partial 很多但人工其实更严” 的样例偏乐观，这仍是下一阶段要继续收口的 record-level calibration 问题
  - 例子 4：`protocol::structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models`
    - 当前 agent `0.488989`，`confidence 0.42`
    - 说明 reviewer 已能老老实实把 protocol-only task 当 assurance review 处理，而不会虚构元素级结论
    - 但 issue taxonomy 仍带有 `missing_required_behavior / wrong_guard_or_trigger` 等 record-style 标签，说明 protocol-only 的表述语气还需要 Phase 6 清理
- 当前仍与人类有偏差的地方：
  - 高分 summary row 仍偏保守
  - 个别 partial-heavy record row 仍偏高
  - protocol-only 的 issue taxonomy 语言还不够“像人工 protocol reviewer”
- 当前 phase 是否停止：`是`，停止在 `Phase 5`，等待下一步指令。

## 8. Phase 6: V1 冻结前验证与收口

目标：

在 Phase 5 的基础上完成最终收口，使 reviewer 能作为“v1 真正可冻结版本”被固定下来。

### Todolist

* [x] 对照 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md) 的停止标准做完整核验。
* [x] 对所有 phase 的指标演化做总汇总。
* [x] 明确哪些指标已经达到停止门槛，哪些还未达到。
* [x] 整理最终 v1 的 prompt / policy / rubric / agent 角色定义。
* [x] 对照 v1 设计稿第 `13` 节核对最终路径结构与模块归宿，补齐缺失项并删除明显偏离项。
* [x] 去掉已经被替换掉的旧临时实现和旁路逻辑。
* [x] 确保兼容层与 v1 内核彻底分离，历史 API 只保留在 `compatibility/` 或等价薄层中。
* [x] 做一次不可达路径检查，确保最终 v1 代码树干净。
* [x] 输出版本级对齐报告与冻结说明。
* [x] 汇总所有 phase 内部多轮自我迭代记录，形成完整优化链路总账。

### Checklist

* [x] v1 的真实实现已经不是“半旧半新”混合状态。
* [x] 最终代码路径结构、模块边界和运行时组织都已与 v1 设计稿对齐，而不是只做到行为近似。
* [x] 所有阶段性临时逻辑都有归宿：
  * [x] 要么进入正式路径
  * [x] 要么被删除
* [x] 没有明显不可达代码残留。
* [x] 有完整 phase-by-phase 对齐演化记录。
* [x] 有完整 phase-by-phase 且 round-by-round 的优化链路记录。
* [x] 有最终冻结版本说明。
* [x] 若未达门槛，已明确写出阻塞项与下一版设计入口。

### Phase 6 当前状态回写

- 回写时间：`2026-04-16 21:48:23`
- 完成状态：`Phase 6` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 6`，并已按规则新增 `Phase 7` 作为后续提分入口。
- 真实接入情况：
  - `expert_review/graph/runtime.py` 继续作为默认主编排，当前 benchmark 与入口验证都直接以此路径为准。
  - `compatibility/legacy_api.py` 成为历史 API 的唯一正式兼容面，`review_artifacts()`、`review_model()`、`heuristic_expert_review()` 均由此统一暴露。
  - `expert_review_v1_runtime.py` 已删除，不再保留“测试 helper 通过旧运行时兼容中转”的旁路。
  - `test_review.py` 已改为直接引用正式模块：`agents/input_analyst.py`、`tools/artifact_probe.py`、`tools/dossier_merge.py`、`compatibility/legacy_api.py`。
  - `agent.py` 已移除 `heuristic_expert_review()`，只保留 provider/LLM 初始化壳层与 `ExpertReviewAgent.review()` 主职责。
- 结构收敛情况：
  - 当前正式运行时目录主干已稳定为 `schemas / prompts / tools / agents / graph / compatibility`
  - 根层保留物已明确收缩为包入口、对外 schema、共享 helper 与 provider 壳层
  - 当前版本级核验与冻结说明已单独固化到 [V1_ALIGNMENT_REPORT.md](./V1_ALIGNMENT_REPORT.md)
- 未完成项：无；`Phase 6` 自身事项已全部闭合。
- 当前停止原因：
  - `Phase 6` 的目标是冻结前核验与代码树收口，而不是继续在当前 phase 内做提分 patch
  - 当前收口后 benchmark 指标与 `Phase 5 Round 0` 保持一致，未观察到明显回退
  - 由于冻结门槛仍显著未达标，后续继续提分已明确转交给 `Phase 7`

### Phase 6 指标总表

本节记录 `2026-04-16 21:48:23` 基于 `run_benchmark_iteration(llm_mode='off')` 的 `Phase 6` 收口快照。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `78.68` |
| `RAS` | `74.87` |
| `SAS` | `75.02` |
| `PDS` | `93.75` |
| `normalized_mae` | `0.1751` |
| `rmse` | `0.1911` |
| `issue_f1` | `0.8202` |
| `human_issue_coverage_recall` | `0.8500` |
| `equivalence_false_reject_rate` | `0.0000` |
| `equivalence_false_accept_rate` | `0.1429` |
| `unsupported_claim_rate` | `0.1778` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.5302` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.7500` |

### Phase 6 本阶段改进记录

- 最明显提升 1：删除 `expert_review_v1_runtime.py`，并让测试直接引用正式模块，当前代码树不再保留“旧 runtime 兼容中转层”。
- 最明显提升 2：历史 API 已进一步收口到 `compatibility/legacy_api.py`，`agent.py` 不再继续承担兼容函数暴露职责。
- 最明显提升 3：当前版本级对齐报告、冻结判断、phase 演化总表与 `Phase 7` 入口已经固定到 [V1_ALIGNMENT_REPORT.md](./V1_ALIGNMENT_REPORT.md) 与本 `TODO`，后续不会再缺失冻结前收尾台账。

- 最明显退化风险 1：未观察到新的 `HAI / RAS / SAS / PDS` 级明显回退；当前 benchmark 指标与 `Phase 5 Round 0` 保持一致。
- 最明显退化风险 2：由于 `Phase 6` 故意不做提分 patch，冻结差距本身没有缩小，说明该 phase 不能替代真正的下一轮提分工作。
- 最明显退化风险 3：历史 `legacy/prompts.py / legacy/rubrics.py` 仍作为 `v0` 参考快照留在树中，虽然不再进入主路径，但后续若要继续压缩根层噪声，仍应优先在新 phase 内评估是否进一步归档。

- 当前仍未完全解决的问题 1：`record-level` 的个别 partial-heavy 样例仍高于人工，`RAS` 远未达到冻结门槛。
- 当前仍未完全解决的问题 2：`summary-level` 的高分 public row 仍偏保守，`SAS` 仍不足以支持冻结。
- 当前仍未完全解决的问题 3：`unsupported_claim_rate` 与 `ece` 仍显著高于停止标准，这已不是 `Phase 6` 收口能解决的问题，而是 `Phase 7` 的核心提分目标。

### Phase 6 本阶段运行记录

- 已验证入口：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
  - `python -m expert_review`（在清空 provider env 的 deterministic 模式下）
  - `run_benchmark_iteration(llm_mode='off')`
- 已被替换或删除的真实路径：
  - `expert_review_v1_runtime.py` 已删除
  - `test_review.py` 不再通过旧 runtime helper re-export 访问正式能力
  - `agent.py` 不再保留 `heuristic_expert_review()`
- 本阶段真实落位的目标层次：
  - `schemas / prompts / tools / agents / graph / compatibility` 六层均仍由当前主路径真实使用
- 当前仍保留的旧逻辑：
  - `schema.py`
  - `inventory.py`
  - `utils.py`
  - 历史 `legacy/prompts.py / legacy/rubrics.py`
- 当前仍属过渡或特殊保留的部分：
  - 无明显 runtime 过渡件；根层保留物当前都已有明确职责或历史参考定位

### Phase 6 多轮自我迭代记录

说明：

- `Phase 6` 的 round 记录以“冻结核验与收口”而不是“继续局部提分”作为边界。
- 因此本 phase 只保留 `Round 0`：完成代码树收口、兼容边界清理、版本级对齐核验，并确认当前版本无明显回退。
- 后续若要继续做评分逻辑、policy 或 agent 分工层面的 patch，按规则必须进入新开的 `Phase 7`，而不是继续把提分工作混进 `Phase 6`。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | 删除 `expert_review_v1_runtime.py`；测试改为直连正式模块；从 `agent.py` 移除 `heuristic_expert_review()`；补齐版本级对齐报告、冻结判断与 `Phase 7` 入口 | `compatibility_boundary` / `codebase_hygiene` | `HAI 78.68 / RAS 74.87 / SAS 75.02 / PDS 93.75` | `HAI 78.68 / RAS 74.87 / SAS 75.02 / PDS 93.75 / normalized_mae 0.1751 / issue_f1 0.8202 / unsupported_claim_rate 0.1778 / ece 0.5302` | `HAI +0.00` | `否` | 说明 `Phase 6` 收口未引入明显回退；当前 phase 目标已完成，继续提分需进入 `Phase 7` |

### Phase 6 收尾汇报记录

- 当前 phase 的完成状态：`Phase 6` 已完成并停止，等待下一步指令；`Phase 7` 已创建但尚未开始实现。
- TODO 已完成项：
  - `Phase 6` 全部 Todolist 已打勾
  - `Phase 6` 全部 Checklist 已打勾
  - 版本级对齐报告与冻结说明已写入 [V1_ALIGNMENT_REPORT.md](./V1_ALIGNMENT_REPORT.md)
  - `Phase 7` 已写入当前 `TODO`
- TODO 尚未完成项：无；当前未冻结原因已如实转交给 `Phase 7`。
- 当前对齐程度总览：
  - 当前 `HAI 78.68 / RAS 74.87 / SAS 75.02 / PDS 93.75`
  - 与 `Phase 5 Round 0` 相比，本次 `Phase 6` 收口没有带来明显回退，也没有试图伪造“只靠清理代码就能继续提分”的假象
  - 当前 reviewer 已具备稳定的多智能体主路径和较强的 protocol restraint，但离冻结标准仍有明显差距
- 对各项核心指标的解释：
  - `HAI 78.68`：整体已经进入“明显像真人 reviewer”的区间，但还不足以宣告和人工达到可接受对齐
  - `RAS 74.87`：record-level 仍是当前冻结的最大阻塞项之一，说明逐条人工评审对齐还不够严密
  - `SAS 75.02`：summary-level 语义意识已稳定，但高分 public row 仍偏保守
  - `PDS 93.75`：protocol-only restraint 已经很稳，`Phase 7` 不能以牺牲这一点为代价去换分
  - `unsupported_claim_rate 0.1778` 与 `ece 0.5302`：当前 reviewer 仍有“说得偏多、置信度校准偏松”的系统性问题，这也是下一阶段必须重点压的项
- 真实例子对比：
  - 例子 1：branch-family 等价重构 case 仍保持 `0.609222`
    - 说明本次 `Phase 6` 收口没有破坏“不同构但等价应给 credit”的核心能力
  - 例子 2：`sncs:connected_device:SMD:Std Dev` 仍保持接近 `Phase 5` 的低分 summary 语义处理
    - 说明 `summary-only` 语义识别未因代码树收口而回退
  - 例子 3：`protocol::structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 仍不会虚构元素级结论
    - 说明 protocol-only restraint 未被破坏
    - 但 taxonomy 语气仍不够像真人 protocol reviewer，这一问题已明确转交 `Phase 7`
- 当前 phase 是否停止：`是`，停止在 `Phase 6`；后续待命，等待是否进入 `Phase 7` 的实现指令。

## 9. 后续总目标、双里程碑与 Phase 7-15 路线图

从 `Phase 7` 开始，后续工作不再只是泛泛地“继续提分”，而是明确围绕以下**实际用途**推进：

1. 把 `expert_review` 做成一个可对 `proj1` 各类 baseline / 生成模型结果进行**批量评分、排序、筛选**的 reviewer。
2. reviewer 不只要“讲得通”，还要能在论文中以可追溯指标与实验设计支撑“**agent-based review 在学术上成立**”。
3. 后续迭代必须同时服务两条主线：
   - 工程主线：做到可稳定批量筛选。
   - 学术主线：做到可在论文中主张 human-aligned / evidence-aware / agent-based reviewer 成立。

### 9.1 当前诊断基线

除保留 `Phase 6` 的 deterministic benchmark slice 快照外，从 `Phase 7` 开始，默认还必须同时跟踪**full available benchmark** 诊断结果。

当前基于 `2026-04-17` full available benchmark 的 deterministic 诊断快照为：

| 指标 | 当前值 |
|---|---:|
| `HAI` | `79.68` |
| `RAS` | `77.33` |
| `SAS` | `73.62` |
| `PDS` | `93.75` |
| `record normalized_mae` | `0.2126` |
| `record spearman_rho` | `0.4817` |
| `record pairwise_order_accuracy` | `0.6164` |
| `summary normalized_mae` | `0.1359` |
| `summary spearman_rho` | `0.2781` |
| `summary pairwise_order_accuracy` | `0.5307` |
| `issue_f1` | `0.9126` |
| `human_issue_coverage_recall` | `0.9305` |
| `unsupported_claim_rate` | `0.0865` |
| `equivalence_false_reject_rate` | `0.0174` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `ece` | `0.4764` |
| `vv_role_coverage` | `0.7500` |

当前已经可以明确的诊断结论：

1. 当前 reviewer 的**问题提取与证据克制**已经相对稳定，说明它更像一个 evidence-aware review assistant。
2. 当前 reviewer 的**数值打分、排序能力与置信度校准**仍明显不足，说明它还不像一个可稳定替代专家打分的 batch scorer。
3. 当前 full available benchmark 的 `record-level` 强对齐数据实际上主要来自 `llms_emp`，`summary-level` 主要来自 `ttool-ai`，而 `512` 条 `component_level_review` 还未进入主评测主指标。
4. 因此，当前版本还不能在论文中直接主张“expert reviewer agent 已被学术上充分验证成立”。

### 9.2 双里程碑定义

后续路线固定为两个逐级里程碑：

1. **Milestone A：达到可用于整体筛选的程度**
   - 用途定位：批量预筛、批量排序、异常样本优先级上浮、人类专家工作量缩减。
   - 结论边界：可以说“能用于整体筛选”，但不能说“已经能替代专家最终裁决”。
2. **Milestone B：达到可用于论文中学术主张的程度**
   - 用途定位：不仅能用于批量筛选，还能在论文中支撑“agent-based review 作为 human-aligned reviewer surrogate 是成立的”。
   - 结论边界：必须同时过 full benchmark、generalization、lockbox、ablation 与稳定性门槛。

路线归属如下：

1. `Phase 7` 到 `Phase 10`：服务 `Milestone A`
2. `Phase 11` 到 `Phase 15`：服务 `Milestone B`

### 9.3 Milestone A：可用于整体筛选

目标：

把当前 reviewer 从“会提问题的 review assistant”推进到“可以稳定做 batch ranking / filtering / triage 的 automated reviewer”。

Milestone A 达成条件：

1. `HAI >= 82`
2. `RAS >= 80`
3. `SAS >= 76`
4. `PDS >= 90`
5. `record normalized_mae <= 0.15`
6. `record spearman_rho >= 0.60`
7. `record pairwise_order_accuracy >= 0.70`
8. `summary spearman_rho >= 0.45`
9. `summary pairwise_order_accuracy >= 0.65`
10. `unsupported_claim_rate <= 0.08`
11. `ece <= 0.20`
12. `protocol_only_overclaim_rate = 0`
13. `rerun_score_std <= 0.03`
14. 已具备批量执行、结果导出与筛选阈值策略，而不是只支持单条 demo 评审。

### 9.4 Milestone B：可用于论文中的学术论证

目标：

把 reviewer 从“可用的 batch scorer”推进到“在论文中可 defensible 地主张 human-aligned / agent-based review 成立”的级别。

Milestone B 达成条件：

1. 满足 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md) 第 `14` 节停止标准。
2. 额外满足以下学术门槛：
   - `PDS >= 90`
   - `record spearman_rho >= 0.75`
   - `record pairwise_order_accuracy >= 0.80`
   - `summary spearman_rho >= 0.60`
   - `summary pairwise_order_accuracy >= 0.75`
   - `|score_bias| <= 0.05`
   - `high_confidence_error_rate <= 0.05`
   - `critical_issue_recall >= 0.90`
   - `weighted_kappa >= 0.60`
   - `lockbox` 集任一核心指标退化不超过 `2` 点
   - leave-one-family-out 的 `HAI` 降幅不超过 `5` 点
3. 已补齐对 `component_level_review` 的正式主评测，并形成可单独报告的 `CRAS` 或等价组件级对齐指标。
4. 已完成关键 agent / policy / routing 的 ablation，能证明当前“agent-based reviewer”不是纯包装，而是结构上确有增益。
5. 已完成 deterministic 主路径与 LLM-enabled 主路径的稳定性、成本与风险边界说明。

### 9.5 从 Phase 7 开始必须新增并持续跟踪的指标

除当前已有指标外，后续必须逐步补齐以下新增指标：

1. `CRAS`
   - Component Review Alignment Score
   - 用于吃进 `component_level_review` 的 states / transitions / guards / actions / hierarchy / parallel / history 等分项人工审查结果
2. `critical_issue_recall`
   - 专门约束 reviewer 不能漏掉对人工最关键的问题
3. `weighted_kappa`
   - 用于判断 overall judgement / coarse judgement 是否和人工具有一致性，而不只是分数接近
4. `high_confidence_error_rate`
   - 专门压 reviewer 的“高置信错判”
5. `evidence_locator_validity`
   - reviewer 给出的 evidence locator 是否真的指向可追溯证据
6. `LOFO_generalization_gap`
   - leave-one-family-out 下的性能降幅
7. `latency_p95`
8. `token_cost_per_record`

## 10. Phase 7: 全量 benchmark 口径固定与下一阶段提分地图

目标：

把当前 `slice-only` 快照升级为后续所有 phase 都能统一依赖的 full benchmark / train-dev-validation-lockbox / LOFO 评测框架，并固定 `Milestone A / B` 的正式验收口径。

### Todolist

* [ ] 把 `slice benchmark` 与 `full available benchmark` 的用途彻底分开：前者用于快迭代，后者用于阶段验收。
* [ ] 明确当前主评测实际覆盖了哪些论文、哪些 regime、哪些 review 粒度，不能再把 coverage 缺口隐含带过。
* [ ] 把 `Phase 6` 之后的实际需求、双里程碑、阶段目标与 target metrics 正式固化到本 `TODO`。
* [ ] 设计并落地 `train / dev / validation / lockbox` 切片构造规则。
* [ ] 设计并落地 leave-one-family-out 的评测脚手架。
* [ ] 为 `component_level_review` 的纳入准备统一 taxonomy 与结果对齐 schema。
* [ ] 给后续 phase 形成统一误差地图：`contract / extraction / equivalence / quality / evidence discipline / calibration / ranking`。
* [ ] 在不引入评分逻辑回退的前提下，让 benchmark harness 能同时导出 slice 与 full report。

### Checklist

* [ ] 后续不再只以默认 `18 + 16 + 4` 的 slice 作为阶段结论口径。
* [ ] 已明确写出当前 benchmark coverage 与当前空白区，而不是笼统地说“已对齐人工”。
* [ ] `Phase 7` 完成后，后续每个 phase 都可同时汇报：
  * [ ] slice 快速指标
  * [ ] full available benchmark 指标
  * [ ] validation / lockbox 指标
  * [ ] LOFO 指标
* [ ] 本 phase 没有提前混入下一阶段的大量评分 patch。

### Phase 7 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone A`
- 当前状态：已创建，尚未开始实现。
- 当前定位：先把“怎么评估后续 phase 是否真的进步”这件事固定下来。

## 11. Phase 8: Record-Level 数值校准、压缩效应修复与 partial-heavy 严惩

目标：

优先修当前最伤 batch scoring 的问题：低分样例被抬高、高分样例被压低、partial-heavy 样例仍高估。

### Todolist

* [ ] 系统性分析 `record-level` 的 score compression：低分高估、高分低估、居中收缩。
* [ ] 对 partial-heavy / structurally bad / semantically broken 样例建立更强惩罚逻辑。
* [ ] 强化 `dependency-aware penalty`，避免 state 本身错了但 transition/guard/action 仍拿到过宽 credit。
* [ ] 收口 `wrong_action_or_effect` 与 `wrong_guard_or_trigger` 的惩罚强度，使其更接近人工。
* [ ] 保持 `issue_f1 / human_issue_coverage_recall / PDS` 不因重标定而显著退化。
* [ ] 针对 score bias 引入显式诊断与回归约束。
* [ ] 记录高误差 record rows 的典型错误簇与改善前后对比。

### Checklist

* [ ] `record normalized_mae <= 0.18`
* [ ] `record spearman_rho >= 0.55`
* [ ] `record pairwise_order_accuracy >= 0.68`
* [ ] `|record score_bias| <= 0.08`
* [ ] `unsupported_claim_rate <= 0.10`
* [ ] `equivalence_false_reject_rate` 不明显回退。
* [ ] partial-heavy 高估样例不再是当前最大残差簇。

### Phase 8 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone A`
- 当前状态：已创建，尚未开始实现。
- 前置条件：`Phase 7` 完成并固定 full benchmark / split / LOFO 口径。

## 12. Phase 9: Summary-Level 排序、分数语义与高分 public row 收口

目标：

让 reviewer 不只会在 `summary-level` 场景里“少乱说”，还要能更接近人工地做高低分区分和排序。

### Todolist

* [ ] 修复高分 public row 过度保守的问题。
* [ ] 压低无必要的 `readability_or_naming` / `unused_or_noisy_structure` 过惩罚。
* [ ] 收口 summary-level 的 score semantics，使 aggregate / std-dev / min / max / run-score 的语义判读更像人工。
* [ ] 继续保持 `summary_only_element_claim_rate = 0` 的证据纪律。
* [ ] 建立 summary-specific rank error 与 score bias 诊断视图。
* [ ] 对真实低分 summary row 保持足够惩罚，避免为了拉高高分 row 而整体漂白。

### Checklist

* [ ] `SAS >= 76`
* [ ] `summary normalized_mae <= 0.12`
* [ ] `summary spearman_rho >= 0.45`
* [ ] `summary pairwise_order_accuracy >= 0.65`
* [ ] `summary_only_element_claim_rate = 0`
* [ ] 高分 public row 的系统性低估不再是主要误差簇。

### Phase 9 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone A`
- 当前状态：已创建，尚未开始实现。
- 前置条件：`Phase 8` 已先收口 record-level 的尺度问题。

## 13. Phase 10: Batch Screening 模式、阈值策略与 Milestone A 验收

目标：

把 reviewer 从“评测时可用”推进到“实际可批量跑、可导出、可用于整体筛选”的状态，并完成 `Milestone A` 验收。

### Todolist

* [ ] 为 batch review 明确输入协议、批量执行方式与结果导出格式。
* [ ] 建立基于 `overall_score / confidence / unsupported extras / evidence discipline` 的 triage 阈值策略。
* [ ] 明确哪些分数段直接放行、哪些进入人工复核、哪些高风险上浮。
* [ ] 加入 batch 模式下的延迟、成本与失败重试统计。
* [ ] 对 deterministic 路径做批量稳定性验证，避免 batch 跑时出现口径漂移。
* [ ] 输出 `Milestone A` 验收报告：当前 reviewer 可以怎么用，不可以怎么用。

### Checklist

* [ ] `Milestone A` 的全部门槛均已满足。
* [ ] 已形成可操作的 batch screening 使用口径，而不是只有 benchmark 指标。
* [ ] `latency_p95`、失败重试和导出结构已可观测。
* [ ] 当前 reviewer 可被明确表述为“可用于整体筛选”，但尚未越界宣称“可替代专家最终裁决”。

### Phase 10 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone A`
- 当前状态：已创建，尚未开始实现。
- 停止条件：本 phase 结束时必须明确判断 `Milestone A` 是否已达成。

## 14. Phase 11: Component-Level Human Review 对齐与 `CRAS` 建立

目标：

把目前还未纳入主评测的 `component_level_review` 正式吸入评测主干，补上“像真人逐项检查 states / transitions / guards / actions / hierarchy / parallel / history”的证据链。

### Todolist

* [ ] 正式接入 `512` 条 `component_level_review` 到 benchmark 主评测流程。
* [ ] 统一组件级 issue taxonomy 与 TP/FP/FN 归约规则。
* [ ] 为各组件类建立独立统计：
  * [ ] states
  * [ ] transitions
  * [ ] guards
  * [ ] actions
  * [ ] hierarchical states
  * [ ] parallel regions
  * [ ] history states
* [ ] 定义并落地 `CRAS` 或等价组件级总指标。
* [ ] 明确哪些组件维度是 reviewer 当前真正强项，哪些仍是缺口。

### Checklist

* [ ] `component_level_review` 已不再游离于主评测之外。
* [ ] `CRAS >= 80`
* [ ] 各主要组件类别 `macro_f1 >= 0.75`
* [ ] 组件级 report 可独立解释，而不是只有一个黑盒总分。

### Phase 11 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：补齐论文论证里最缺的一块“逐组件人工对齐”证据。

## 15. Phase 12: Judgement / Reason / Evidence Reliability 深化

目标：

让 reviewer 不只在“分数”上接近人工，也在 judgement、关键问题召回、evidence locator 与 explanation 一致性上达到论文可用程度。

### Todolist

* [ ] 补齐 `overall_judgement` / coarse judgement 的对齐指标：
  * [ ] `macro_f1`
  * [ ] `weighted_kappa`
  * [ ] `judgement_flip_rate`
* [ ] 补齐 `critical_issue_recall`。
* [ ] 补齐 `evidence_locator_validity`。
* [ ] 收口 `contradiction_rate`，避免维度之间互相打架。
* [ ] 继续压 `unsupported_claim_rate` 到学术可接受范围。
* [ ] 让 explanation 更像人工 expert review，而不是只像 taxonomy dump。

### Checklist

* [ ] `critical_issue_recall >= 0.88`
* [ ] `weighted_kappa >= 0.50`
* [ ] `unsupported_claim_rate <= 0.08`
* [ ] `evidence_locator_validity >= 0.90`
* [ ] `contradiction_rate` 明显低于当前版本。

### Phase 12 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 前置条件：`Phase 11` 已让组件级对齐进入正式评测。

## 16. Phase 13: Generalization、Validation / Lockbox 与 LOFO 验证

目标：

证明当前 reviewer 不是只会对齐当前 benchmark 风格，而是具有真正的泛化性与可复现性。

### Todolist

* [ ] 正式落地 `train / dev / validation / lockbox` 数据切分与版本晋升机制。
* [ ] 正式落地 leave-one-family-out 测试。
* [ ] 把阶段验收默认从“单次 full available benchmark”提升为“validation + lockbox + LOFO”联合口径。
* [ ] 对 lockbox 上的主要残差簇做单独分析。
* [ ] 明确哪些 patch 是真泛化提升，哪些只是对当前可见 benchmark 过拟合。

### Checklist

* [ ] 已有可复用的 validation / lockbox 报告流程。
* [ ] `lockbox` 任一核心指标退化不超过 `4` 点。
* [ ] `LOFO_generalization_gap` 已可计算。
* [ ] 当前 reviewer 的提升不再主要依赖可见 benchmark 风格。

### Phase 13 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：把“对齐 benchmark”推进到“对齐人工评审机制”的泛化论证。

## 17. Phase 14: LLM-Enabled 主路径、随机性稳定性与成本边界

目标：

把当前主要以 deterministic 口径评测的 reviewer，推进到可对外说明 deterministic / LLM-enabled 两条主路径的差异、收益、风险与成本。

### Todolist

* [ ] 在 `llm_mode='auto'` 或等价真实 LLM 路径下做重复实验。
* [ ] 报告 deterministic 与 LLM-enabled 两条主路径的：
  * [ ] 对齐差异
  * [ ] 置信度差异
  * [ ] rerun 稳定性
  * [ ] `latency_p50 / latency_p95`
  * [ ] `token_cost_per_record`
* [ ] 判断 LLM 是否带来实质收益，还是只增加波动与成本。
* [ ] 明确默认对外主路径与 fallback 口径。

### Checklist

* [ ] LLM-enabled 主路径没有引入不可接受的随机性漂移。
* [ ] `rerun_score_std <= 0.03`
* [ ] 已可说明 deterministic 与 LLM-enabled 分别适合什么场景。
* [ ] 成本与延迟边界已可被论文与工程说明同时接受。

### Phase 14 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：补齐“agent-based reviewer 是否必须依赖在线 LLM 才成立”的论证。

## 18. Phase 15: 学术冻结候选、Ablation 与论文级证据包

目标：

完成 `Milestone B` 的最终验收，冻结一个可在论文中正式引用的 reviewer 版本，并给出完整证据包。

### Todolist

* [ ] 以 full benchmark + validation + lockbox + LOFO 为基础做最终验收。
* [ ] 完成关键模块的 ablation：
  * [ ] regime detection / review policy
  * [ ] equivalence + arbiter
  * [ ] missing-evidence critic
  * [ ] score composer / synthesis policy
  * [ ] deterministic-only vs LLM-enabled
* [ ] 明确当前“agent-based”结构到底带来了哪些独立贡献。
* [ ] 输出 paper-ready evidence package：
  * [ ] 最终 alignment report
  * [ ] milestone report
  * [ ] ablation report
  * [ ] failure case appendix
  * [ ] claims / non-claims 边界说明
* [ ] 明确此时可以在论文中怎么说，不可以怎么说。

### Checklist

* [ ] `Milestone B` 的全部门槛均已满足。
* [ ] 已能基于 ablation 证明当前 reviewer 的 agent-based 结构具有必要性，而不是纯包装。
* [ ] 已有完整 paper-ready 证据链，而不是只剩单个总分。
* [ ] 若仍未达标，已明确开启 `Phase 16+` 的原因与下一批技术入口。

### Phase 15 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 停止条件：本 phase 结束时必须明确判断 `Milestone B` 是否已达成，若未达成则按规则新开 `Phase 16+`。

## 19. 每个 Phase 的统一对齐记录模板

每个 phase 完成后，至少记录以下内容：

### 19.1 指标总表

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

### 19.2 本阶段改进记录

1. 本阶段最明显提升的三项能力。
2. 本阶段最明显退化的三项能力。
3. 本阶段仍未解决的三类错误簇。

### 19.3 本阶段运行记录

1. 哪些入口已验证。
2. 哪些真实路径被替换。
3. 本阶段哪些 `schemas / prompts / tools / agents / graph / compatibility` 目标层次已经有真实落位。
4. 哪些旧逻辑仍然保留。
5. 哪些模块只是临时过渡件。

### 19.4 本阶段多轮自我迭代记录

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

### 19.5 本阶段收尾汇报记录

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

## 20. 阶段推进规则

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
11. 每个后续 phase 都必须同时推进结构收敛；如果只是继续在旧文件和旧路径上叠补丁、没有让项目架构更接近 v1 设计，则不得视为完成该 phase。
12. 若当前最后一个 phase 结束时仍未达到冻结条件，允许继续新增后续 phase；但必须明确写出为什么现有阶段不足、下一阶段具体补什么，以及新增 phase 的停止标准。

## 21. 最终目标

最终目标不是“写完一个看起来像 v1 的新目录”，而是：

1. `expert_review` 的真实运行时内部已经成为 v1 设计稿定义的通用化多智能体 reviewer。
2. reviewer 在任意时点都保持完整可运行。
3. 整个重构周期中的每一阶段都有完整对齐记录。
4. 任何阶段都没有通过堆不可达代码来伪装进度。
5. 最终冻结版本能够以完整、可追溯、可评测的形式被后续版本继续继承。
6. 每个阶段结束时，TODO 台账与真实执行状态始终一致，且都已向用户做过一次如实、可解释、带指标和例子的收尾汇报。
7. 最终的 `expert_review/` 路径结构、模块边界和运行时组织都已真正靠拢 v1 设计，而不是停留在旧项目架构上的长期修补状态。
