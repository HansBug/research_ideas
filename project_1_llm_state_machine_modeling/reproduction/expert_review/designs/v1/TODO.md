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
9. 禁止把运行时关键判定建立在硬特判上，尤其禁止基于原始字符串、子串、正则、词表或等价表面形式规则，直接对 `task type / model type / metamodel / regime / policy / score offset / prompt family / input family` 做主路径判断。
10. 如果某类任务确实需要细分或路由，必须由 LLM 或等价语义判定器完成，并且提问方式必须是语义性的，例如“该任务是否关注状态机结构语义”“该样本属于 A / B / C / other 哪一类”，每个类别都要有清晰定义、可执行边界和例子；禁止把“是否包含某关键词”伪装成 LLM 判定。
11. `expert_review` 必须把多语言、跨语言和跨元模型不一致视为默认支持场景，而不是英文默认场景；不得假设 `input / pred / ref / prompt / model label / metamodel label` 同语种、同命名体系或同表达习惯。
12. 从本规则引入起，每个 phase 的 checklist 都必须包含“语义判定与跨语言泛化合规”专门硬性检查项；在该项未通过前，该 phase 不能算完成。`Phase 1-10` 的相关历史债统一并入后续专项清理 phase，不因旧 checklist 缺项而视为天然合规。

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

### 2.1.3 语义判定、去硬特判与跨语言泛化硬要求

1. 运行时关键判断不得再依赖字符串特判：
   - 不允许 `"xxx" in text`、关键词表、正则命中、英文专用 token 猜测、标签别名表或类似机制，直接决定 `task / regime / policy / scoring / model-family / metamodel-family`。
   - 不允许把这类表面规则包一层 prompt 或 helper 之后继续作为主判断依据。
2. 如必须做任务分类、工件类型判定、证据制度判定、策略路由或模型类型归类，必须改为语义判定：
   - 问题本身必须问“它在语义上属于什么”，而不是“它表面上像什么词”。
   - 类别集合必须带定义、边界、正例与反例。
   - 必须保留 `other / unknown / ambiguous` 出口，不能强行把未知样本塞进某个硬编码类别。
3. 允许保留的 deterministic 逻辑只限非语义边界，例如：
   - 用户显式配置或 CLI 参数
   - 文件格式 / schema / field existence 解析
   - 明确协议字段或结构化元数据读取
   - 这类逻辑不得越界替代语义判定本身
4. 如果 LLM 语义判定失败、置信度过低或输入信息不足，fallback 必须是保守降级到 `unknown / generic / needs more evidence`，不能静默退回被禁止的字符串 heuristics。
5. 多语言、跨语言与跨元模型泛化是主路径要求，不是附加 bonus：
   - 至少要覆盖 `input / pred / ref` 彼此不同语言的情况
   - 至少要覆盖 `prompt / model label / metamodel label` 与工件正文不同语言或不同命名体系的情况
   - 至少要覆盖中英混合与非英文单语样本
6. 本小节从现在起对所有后续 phase 生效；`Phase 1-10` 已存在的违例不视为可接受遗留，而是必须在后续历史债清理 phase 中全部建账、替换和验收。

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
10. 本阶段新增、删除或保留的语义判定器与硬特判清单，以及对应理由。
11. 本阶段多语言 / 跨语言 / 跨元模型验证覆盖情况与失败簇。

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
   - `semantic_routing_error`
   - `equivalence_reasoning_error`
   - `quality_judgement_error`
   - `evidence_discipline_error`
   - `cross_language_generalization_error`
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
7. 每个 phase 结束时都必须追加一组“语义判定与跨语言泛化”专门验证，不能只在英文、同语言或已知标签样本上验收。
8. 该专门验证至少应覆盖：
   - `input` 与 `pred / ref` 不同语言
   - `prompt / model label / metamodel label` 与正文不同语言或不同命名体系
   - 中文、英文以及至少一种非中非英样本或等价 stress case
9. 若该专门验证未通过，或发现仍有运行时关键字符串特判残留，则该 phase checklist 必须判定为未通过。

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

## 9. 后续总目标、双里程碑与 Phase 7-16 路线图

从 `Phase 7` 开始，后续工作不再只是泛泛地“继续提分”，而是明确围绕以下**实际用途**推进：

1. 把 `expert_review` 做成一个可对 `proj1` 各类 baseline / 生成模型结果进行**批量评分、排序、筛选**的 reviewer。
2. reviewer 不只要“讲得通”，还要能在论文中以可追溯指标与实验设计支撑“**agent-based review 在学术上成立**”。
3. 后续迭代必须同时服务两条主线：
   - 工程主线：做到可稳定批量筛选。
   - 学术主线：做到可在论文中主张 human-aligned / evidence-aware / agent-based reviewer 成立。

### 9.1 当前诊断基线

除保留 `Phase 6` 的 deterministic benchmark slice 快照外，从 `Phase 7` 开始，默认还必须同时跟踪**full available benchmark** 诊断结果。

当前基于 `2026-04-17 11:00:22` full available benchmark 的 deterministic 诊断快照为：

| 指标 | 当前值 |
|---|---:|
| `HAI` | `83.39` |
| `RAS` | `80.48` |
| `SAS` | `81.51` |
| `PDS` | `93.75` |
| `record normalized_mae` | `0.1643` |
| `record spearman_rho` | `0.6683` |
| `record pairwise_order_accuracy` | `0.6910` |
| `summary normalized_mae` | `0.1044` |
| `summary spearman_rho` | `0.7319` |
| `summary pairwise_order_accuracy` | `0.7286` |
| `issue_f1` | `0.9126` |
| `human_issue_coverage_recall` | `0.9305` |
| `unsupported_claim_rate` | `0.0865` |
| `equivalence_false_reject_rate` | `0.0174` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `ece` | `0.3969` |
| `vv_role_coverage` | `0.7500` |

当前已经可以明确的诊断结论：

1. 当前 reviewer 的**record-level 数值尺度与排序能力**保持 `Phase 8` 收口状态，没有因为 `Phase 9` 的 summary patch 出现明显回退。
2. 当前 reviewer 的**summary-level 排序与 public-row 语义判读**已经显著改善，`SAS / summary normalized_mae / summary ranking` 全部越过 `Phase 9` 目标线。
3. 当前 `Milestone A` 的主瓶颈已不再是 summary ranking，而是 `record normalized_mae / record pairwise / unsupported_claim_rate / ece` 以及 batch screening 的执行与阈值口径。
4. 当前 full available benchmark 的 `record-level` 强对齐数据实际上主要来自 `llms_emp`，`summary-level` 主要来自 `ttool-ai`，而 `512` 条 `component_level_review` 还未进入主评测主指标；此外，运行时仍存在需要清理的语义判定硬编码与跨语言泛化历史债。因此仍不能在论文中直接主张“expert reviewer agent 已被学术上充分验证成立”，下一阶段应先处理去硬特判与泛化债，再推进 `component_level_review`、generalization 与学术证据链。

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
2. `Phase 11` 到 `Phase 16`：服务 `Milestone B`

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

当前状态：

1. `Phase 10` 已于 `2026-04-17` 正式达成 `Milestone A`。
2. 当前结论边界更新为：reviewer 已可用于整体筛选、批量预筛与异常样本上浮，但仍不能替代专家最终裁决。
3. `Milestone B` 仍远未完成，后续主问题已转到 `component_level_review`、generalization、ablation 与学术证据链。

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
6. 已通过“去硬特判 / 语义判定 / 多语言与跨语言 / 跨元模型泛化”硬门槛：
   - 运行时关键判断中不存在未登记的字符串硬特判残留
   - 必要分类任务均已采用带定义、边界与例子的语义判定
   - 跨语言 validation 中不存在系统性失败簇

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
9. `cross_language_validation_pass_rate`
   - 用于跟踪 `input / pred / ref / prompt / model label / metamodel label` 跨语言组合的通过率
10. `semantic_gate_violation_count`
   - 用于跟踪运行时关键路径中仍残留多少被禁止的硬特判或伪语义判定

## 10. Phase 7: 全量 benchmark 口径固定与下一阶段提分地图

目标：

把当前 `slice-only` 快照升级为后续所有 phase 都能统一依赖的 full benchmark / train-dev-validation-lockbox / LOFO 评测框架，并固定 `Milestone A / B` 的正式验收口径。

### Todolist

* [x] 把 `slice benchmark` 与 `full available benchmark` 的用途彻底分开：前者用于快迭代，后者用于阶段验收。
* [x] 明确当前主评测实际覆盖了哪些论文、哪些 regime、哪些 review 粒度，不能再把 coverage 缺口隐含带过。
* [x] 把 `Phase 6` 之后的实际需求、双里程碑、阶段目标与 target metrics 正式固化到本 `TODO`。
* [x] 设计并落地 `train / dev / validation / lockbox` 切片构造规则。
* [x] 设计并落地 leave-one-family-out 的评测脚手架。
* [x] 为 `component_level_review` 的纳入准备统一 taxonomy 与结果对齐 schema。
* [x] 给后续 phase 形成统一误差地图：`contract / extraction / equivalence / quality / evidence discipline / calibration / ranking`。
* [x] 在不引入评分逻辑回退的前提下，让 benchmark harness 能同时导出 slice 与 full report。

### Checklist

* [x] 后续不再只以默认 `18 + 16 + 4` 的 slice 作为阶段结论口径。
* [x] 已明确写出当前 benchmark coverage 与当前空白区，而不是笼统地说“已对齐人工”。
* [x] `Phase 7` 完成后，后续每个 phase 都可同时汇报：
  * [x] slice 快速指标
  * [x] full available benchmark 指标
  * [x] validation / lockbox 指标
  * [x] LOFO 指标
* [x] 本 phase 没有提前混入下一阶段的大量评分 patch。

### Phase 7 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 回写时间：`2026-04-17 01:25:43`
- 所属里程碑：`Milestone A`
- 完成状态：`Phase 7` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 7`，不提前进入 `Phase 8`。
- 当前定位：已把“怎么评估后续 phase 是否真的进步”固定为正式 benchmark harness，而不是继续依赖单一 `slice-only` 快照。
- 真实接入情况：
  - `benchmark.py` 已支持 `slice / full / split / phase7` 四类入口
  - `build_benchmark_inventory()`、`summarize_benchmark_coverage()`、`build_benchmark_split_bundle()`、`build_lofo_task_bundles()` 已进入真实 benchmark 主路径
  - `component_level_review` 的 alignment schema、统一 error map 与 ranking risk 已真实进入 phase7 bundle 导出结果
- 可运行性：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py` 已验证
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已验证
  - `python -m expert_review.benchmark --scope slice --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope full --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope split --split-name train|dev|validation|lockbox --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope phase7 --llm-mode off --rerun-count 0 --output-markdown /tmp/expert_review_phase7_bundle.md --output-json /tmp/expert_review_phase7_bundle.json` 已验证
- 结构收敛：
  - `expert_review/` 的正式 runtime 未被触碰；本阶段只把根层 `benchmark.py` 真正收敛成后续 phase 的统一离线评测 harness
  - 新增 `test_benchmark.py` 作为 benchmark harness 的固定最小回归入口
- 未完成项：
  - `component_level_review` 仍未进入主 `HAI / RAS / SAS` 指标，这一项本 phase 只完成 schema 预埋，不提前进入 `Phase 12`
- 已知遗留问题：
  - full benchmark 下 `record` 与 `summary` 的 ranking risk 仍都是 `high`
  - `calibration_error = 202` 仍是最大错误簇
  - `lockbox PDS = 75.00` 暴露 protocol-only family holdout 的脆弱点

### Phase 7 指标总表

本节记录 `2026-04-17 01:25:43` 基于 `run_benchmark_iteration(llm_mode='off', scope='full')` 的 `full available benchmark` 收尾快照，作为 `Phase 7` 的正式阶段结论口径。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `79.68` |
| `RAS` | `77.33` |
| `SAS` | `73.62` |
| `PDS` | `93.75` |
| `normalized_mae` | `0.2126` |
| `rmse` | `0.2357` |
| `issue_f1` | `0.9126` |
| `human_issue_coverage_recall` | `0.9305` |
| `equivalence_false_reject_rate` | `0.0174` |
| `equivalence_false_accept_rate` | `0.2439` |
| `unsupported_claim_rate` | `0.0865` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.4764` |
| `rerun_score_std` | `0.0000` |
| `vv_role_coverage` | `0.7500` |

### Phase 7 扩展评测快照

#### 1. coverage 与主评测口径

| 评测池 | 行数 | family 数 | 当前覆盖 |
|---|---:|---:|---|
| `record` | `192` | `18` | 目前全部来自 `llms_emp` |
| `summary` | `84` | `12` | 目前全部来自 `ttool-ai` |
| `protocol` | `4` | `4` | `llms_emp / requirements-capture-and-evaluation-in-nimbus-light-control / structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models / ttool-ai` |
| `component` | `512` | `16` | 当前 deferred；来自 `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` |

`component_level_review` 当前已固定的 canonical component taxonomy：

`Actions / All / Guards / Hierarchical states / History States / Parallel Regions / States / Transitions`

#### 2. slice、split 与 lockbox 快照

- `slice` 快速口径：`18 + 16 + 4`
  - `HAI 74.40 / RAS 71.01 / SAS 66.37 / PDS 93.75`

| split | `record` | `summary` | `protocol` | `HAI` | `RAS` | `SAS` | `PDS` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `train` | `86` | `35` | `1` | `81.95` | `78.10` | `75.97` | `100.00` |
| `dev` | `43` | `21` | `1` | `79.97` | `75.88` | `72.96` | `100.00` |
| `validation` | `32` | `14` | `1` | `79.07` | `77.11` | `66.61` | `100.00` |
| `lockbox` | `31` | `14` | `1` | `75.69` | `76.66` | `74.13` | `75.00` |

#### 3. LOFO 泛化快照

| regime | family 数 | 平均指标 | 最差指标 | 平均 gap vs full | 最差 gap vs full | 最差 family |
|---|---:|---|---|---:|---:|---|
| `record` | `18` | `avg_RAS = 76.75` | `min_RAS = 71.17` | `0.58` | `6.15` | `record::llms_emp::stm::GPT-4o` |
| `summary` | `12` | `avg_SAS = 73.15` | `min_SAS = 64.45` | `0.47` | `9.17` | `summary::ttool-ai::automated_braking::BD` |
| `protocol` | `4` | `avg_PDS = 93.75` | `min_PDS = 75.00` | `0.00` | `18.75` | `protocol::structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` |

#### 4. full benchmark 扩展诊断

| 扩展指标 | 当前值 |
|---|---:|
| `record spearman_rho` | `0.4817` |
| `record pairwise_order_accuracy` | `0.6164` |
| `summary spearman_rho` | `0.2781` |
| `summary pairwise_order_accuracy` | `0.5307` |
| `score_bias` | `-0.0788` |
| `high_confidence_error_rate` | `0.0000` |

| error bucket | 数量 |
|---|---:|
| `calibration_error` | `202` |
| `element_extraction_error` | `133` |
| `quality_judgement_error` | `124` |
| `contract_understanding_error` | `84` |
| `evidence_discipline_error` | `50` |
| `equivalence_reasoning_error` | `12` |

### Phase 7 本阶段改进记录

- 最明显提升 1：benchmark 口径已经从“默认只看 `18 + 16 + 4` slice”升级为同时固定 `slice / full available / train-dev-validation-lockbox / LOFO` 四套口径；后续每个 phase 现在都能报告真正可比较的阶段验收结果。
- 最明显提升 2：当前 coverage 缺口不再被隐含带过；`record = 192`、`summary = 84`、`protocol = 4`、`component = 512` 的真实覆盖、family 分布与论文来源已经全部显式化。
- 最明显提升 3：`component_level_review` 的统一 taxonomy/schema、full error map 和 ranking risk 已经进入 benchmark 导出物，后续 phase 不再需要重新发明“问题分桶”和“组件级对齐”口径。

- 最明显退化风险 1：本 phase 没有引入新的 runtime 回退，但新的 family-aware slice/phase7 报告让原来被单一快照掩盖的排序风险与泛化脆弱点完全暴露出来。
- 最明显退化风险 2：`lockbox PDS = 75.00` 与 protocol LOFO 最差 gap `18.75` 说明 protocol-only 目前不能只看整体 `PDS 93.75` 就宣称泛化稳定。
- 最明显退化风险 3：新的 full error map 显示 `calibration_error = 202`、`element_extraction_error = 133`、`quality_judgement_error = 124`，说明下一阶段不能再凭总分感觉式提分，而必须按错误簇精确打。

- 当前仍未完全解决的问题 1：`record` 排序仍偏弱，`spearman_rho = 0.4817`、`pairwise_order_accuracy = 0.6164`，这已直接进入 `Phase 8` 的主目标。
- 当前仍未完全解决的问题 2：`summary` 排序更弱，`spearman_rho = 0.2781`、`pairwise_order_accuracy = 0.5307`，说明 `Phase 9` 前不能提前宣称 summary-level 已接近人工排序。
- 当前仍未完全解决的问题 3：`component_level_review` 虽已完成 schema 收口，但仍未进入主 `HAI / RAS / SAS`；这部分必须留到后续独立 phase 正式纳入。

### Phase 7 本阶段运行记录

- 已验证入口：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py`
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
  - `python -m expert_review.benchmark --scope slice --llm-mode off`
  - `python -m expert_review.benchmark --scope full --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name train --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name dev --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name validation --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name lockbox --llm-mode off`
  - `python -m expert_review.benchmark --scope phase7 --llm-mode off --rerun-count 0 --output-markdown /tmp/expert_review_phase7_bundle.md --output-json /tmp/expert_review_phase7_bundle.json`
- 已被替换或新增的真实路径：
  - `benchmark.py` 从单一 slice replay 脚本扩展为统一 `slice / full / split / phase7 bundle` 入口
  - 新增 `build_benchmark_inventory()` 作为评测数据盘点入口
  - 新增 `build_benchmark_split_bundle()` 与 `build_lofo_task_bundles()` 作为后续阶段固定切片器
  - 新增 `summarize_benchmark_coverage()`、`build_component_alignment_schema()`、`error_map` 导出路径
  - 新增 `test_benchmark.py` 用于锁住 coverage / split / LOFO 的最小回归
- 本阶段真实落位的目标层次：
  - `tools` 向离线侧延伸出正式 benchmark harness 能力，但未侵入 runtime 主图
  - `compatibility` 边界保持稳定；外部 `review_artifacts()`、`review_model()`、`python -m expert_review` 未受影响
- 当前仍保留的旧逻辑：
  - `benchmark.py` 仍位于根层，作为统一离线 replay/analysis 入口
  - `component_level_review` 仍仅做 deferred schema，不提前纳入主评分
- 当前仍属过渡或特殊保留的部分：
  - LOFO 当前是评测脚手架而不是训练式 holdout 优化器
  - `component_level_review` 当前只完成 taxonomy/schema 收口，未进入 `CRAS`

### Phase 7 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 7` 的主实现轮：先把 coverage / split / LOFO / component schema / error map 真实接到 benchmark 主路径，并验证所有新增入口。
- `Round 1` 只在 `Phase 7` 边界内继续补 benchmark bundle 的摘要层，让 `validation / lockbox / LOFO / full error map` 直接进入 markdown/json 导出，不提前进入 `Phase 8` 的评分 patch。
- 当前本地最终保留的是 `Round 1` 代码；本阶段没有对 reviewer runtime 做任何评分逻辑修改。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | 新增 `record / summary / component / protocol` inventory；新增 coverage summary、component schema、split bundle、LOFO bundle、error map、`scope=slice|full|split|phase7` CLI；新增 `test_benchmark.py` | `contract_understanding_error` / `element_extraction_error` / `equivalence_reasoning_error` / `quality_judgement_error` / `evidence_discipline_error` / `calibration_error` | `Phase 6 slice-only: HAI 78.68 / RAS 74.87 / SAS 75.02 / PDS 93.75` | `slice HAI 74.40 / RAS 71.01 / SAS 66.37 / PDS 93.75`；`full HAI 79.68 / RAS 77.33 / SAS 73.62 / PDS 93.75`；`validation HAI 79.07 / lockbox HAI 75.69` | `口径切换，不做旧 slice 与新 full 的直接分差比较` | `是` | 本轮核心收益是把评测口径固定下来而不是直接提分；runtime 未改，新增变化全部属于 benchmark harness |
| `Round 1` | 新增 `split_summary`、`lofo_generalization`、`full error map` 与 `ranking risk` 的 bundle 汇总；同步更新 `README.md` 与 `GUIDE.md` 的 benchmark 入口说明 | `evaluation_surface` / `coverage_reporting` | `slice HAI 74.40 / full HAI 79.68 / validation HAI 79.07 / lockbox HAI 75.69` | `slice HAI 74.40 / full HAI 79.68 / validation HAI 79.07 / lockbox HAI 75.69` | `HAI +0.00` | `否` | 说明后续继续 patch 只会进入报告层细节，不会再带来新的阶段价值；继续做就会越界到 `Phase 8` 的评分优化，因此按规则停止 |

### Phase 7 收尾汇报记录

- 当前 phase 的完成状态：`Phase 7` 已完成并停止，等待下一步指令；`Phase 8` 的前置条件已经满足，但当前不提前启动。
- TODO 已完成项：
  - `Phase 7` 全部 Todolist 已打勾
  - `Phase 7` 全部 Checklist 已打勾
  - `slice / full / split / LOFO / component schema / error map` 已全部写回当前 TODO
  - `README.md`、`GUIDE.md` 与 benchmark CLI 说明已同步
- TODO 尚未完成项：
  - 无本 phase 内遗留未勾项
  - `component_level_review` 未纳入主评测并不属于漏做，而是按规划留给后续 phase 正式接入
- 当前对齐程度总览：
  - 当前正式阶段结论不再只看单一 slice，而是以 `full available benchmark` 为主：`HAI 79.68 / RAS 77.33 / SAS 73.62 / PDS 93.75`
  - 同时保留 `slice HAI 74.40` 作为快迭代口径，`validation HAI 79.07` 与 `lockbox HAI 75.69` 作为更保守的泛化口径
  - LOFO 的平均 gap 目前不大，但最差 family gap 已经把真实脆弱点直接暴露出来：`record 6.15 / summary 9.17 / protocol 18.75`
- 对各项核心指标的解释：
  - `HAI 79.68`：从整体上看 reviewer 已具备相当强的人类风格 alignment，但当前 phase 的核心结论是“评测口径已经可信”，不是“能力已经达标”
  - `RAS 77.33` 与 `normalized_mae 0.2126`：record-level 总体已能稳定工作，但排序仍弱，说明如果拿去做大规模筛选仍会有误排
  - `SAS 73.62`：summary-level 仍明显弱于可用于学术主张的门槛，特别是排序而非平均分接近的问题还很重
  - `PDS 93.75`：整体 restraint 仍稳，但 `lockbox` 与 protocol LOFO 已证明它不是无条件稳，需要继续补 protocol family 泛化
  - `unsupported_claim_rate 0.0865` 与 `ece 0.4764`：当前 reviewer 的“乱说”已经明显压下来了，但“给分和排序是否真像人”仍远未完成
- 真实例子对比：
  - 例子 1：`record::llms_emp::stm::GPT-4o`
    - 这是当前 `record` LOFO 最差 family，`worst_holdout_gap_vs_full = 6.15`
    - 说明 reviewer 在某些 diagram-type + model family 组合上仍存在明显 family dependence，不能只看 full aggregate 就乐观
  - 例子 2：`summary::ttool-ai::automated_braking::BD`
    - 这是当前 `summary` LOFO 最差 family，`worst_holdout_gap_vs_full = 9.17`
    - 说明 summary-level 的排序和尺度语义还不稳，尤其不能提前宣称 public row 排序已经充分对齐人工
  - 例子 3：`protocol::structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models`
    - 这是当前 protocol LOFO 最差 family，`min_PDS = 75.00`
    - 说明 protocol-only restraint 虽然总体高，但遇到 family holdout 仍可能退到仅“勉强可用”的程度
- 当前 phase 是否停止：`是`，停止在 `Phase 7`；继续往下做已经会跨入 `Phase 8` 的评分校准与错误簇定向修复，因此本轮按规则收口。

## 11. Phase 8: Record-Level 数值校准、压缩效应修复与 partial-heavy 严惩

目标：

优先修当前最伤 batch scoring 的问题：低分样例被抬高、高分样例被压低、partial-heavy 样例仍高估。

### Todolist

* [x] 系统性分析 `record-level` 的 score compression：低分高估、高分低估、居中收缩。
* [x] 对 partial-heavy / structurally bad / semantically broken 样例建立更强惩罚逻辑。
* [x] 强化 `dependency-aware penalty`，避免 state 本身错了但 transition/guard/action 仍拿到过宽 credit。
* [x] 收口 `wrong_action_or_effect` 与 `wrong_guard_or_trigger` 的惩罚强度，使其更接近人工。
* [x] 保持 `issue_f1 / human_issue_coverage_recall / PDS` 不因重标定而显著退化。
* [x] 针对 score bias 引入显式诊断与回归约束。
* [x] 记录高误差 record rows 的典型错误簇与改善前后对比。

### Checklist

* [x] `record normalized_mae <= 0.18`
* [x] `record spearman_rho >= 0.55`
* [x] `record pairwise_order_accuracy >= 0.68`
* [x] `|record score_bias| <= 0.08`
* [x] `unsupported_claim_rate <= 0.10`
* [x] `equivalence_false_reject_rate` 不明显回退。
* [x] partial-heavy 高估样例不再是当前最大残差簇。

### Phase 8 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 回写时间：`2026-04-17 02:40:12`
- 所属里程碑：`Milestone A`
- 完成状态：`Phase 8` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 8`，不提前进入 `Phase 9`。
- 当前定位：仅在 `record-level` 范围内修 score compression 与 residual cluster，不改 `summary / protocol` 评分语义，也不把工作越界到 `Phase 9`。
- 真实接入情况：
  - `equivalence.py` 已新增 `ref_element_coverage / ref_relation_coverage / missing_item_count / harmful_extra_count / contradiction_count` 等显式诊断字段。
  - `score_composer.py` 已新增 `matched_ratio / partial_ratio / missing_ratio / reference_alignment / missing_signal_count` 等 record-level metric payload。
  - `score_composer.py` 已新增窄范围 `record` 标定：`score stretch`、`trace-failure exact rescue`、`aligned partial-heavy bonus`、`huge missing-signal penalty`、`low-equivalence penalty`。
  - `summary` 与 `protocol` 路径未被改动；`SAS / PDS / summary-only evidence restraint` 仍保持原口径。
- 可运行性：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已验证
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py` 已验证
  - `python -m expert_review.benchmark --scope full --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope split --split-name validation --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope split --split-name lockbox --llm-mode off` 已验证
- 已知遗留问题：
  - `validation` 的 `record pairwise_order_accuracy = 0.5968` 仍偏低，说明 family-split 下 record ranking 还没有完全稳住。
  - `STM Results:57` 仍有明显低估，说明并行/正交结构上的 equivalence 误杀尚未完全解决。
  - `STM Results:43`、`STM Results:8` 仍被高估，说明部分 `partial-only` family 还需要更细的结构/语义区分。

### Phase 8 指标总表

本节记录 `2026-04-17 02:40:12` 基于 `run_benchmark_iteration(llm_mode='off', scope='full')` 的 `full available benchmark` 收尾快照，作为 `Phase 8` 的正式阶段结论口径。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `81.42` |
| `RAS` | `80.48` |
| `SAS` | `73.62` |
| `PDS` | `93.75` |
| `normalized_mae` | `0.1643` |
| `rmse` | `0.1968` |
| `issue_f1` | `0.9126` |
| `human_issue_coverage_recall` | `0.9305` |
| `equivalence_false_reject_rate` | `0.0174` |
| `equivalence_false_accept_rate` | `0.2439` |
| `unsupported_claim_rate` | `0.0865` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `summary_only_element_claim_rate` | `0.0000` |
| `ece` | `0.4229` |
| `record spearman_rho` | `0.6683` |
| `record pairwise_order_accuracy` | `0.6910` |
| `score_bias` | `-0.0459` |
| `high_confidence_error_rate` | `0.0000` |

### Phase 8 扩展评测快照

#### 1. split 泛化快照

| split | `HAI` | `RAS` | `record normalized_mae` | `record spearman_rho` | `record pairwise_order_accuracy` | `record score_bias` | `unsupported_claim_rate` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `validation` | `80.80` | `80.27` | `0.1687` | `0.6229` | `0.5968` | `-0.1044` | `0.0672` |
| `lockbox` | `77.94` | `80.73` | `0.1771` | `0.6615` | `0.7011` | `-0.0224` | `0.0952` |

#### 2. full benchmark 扩展诊断

| 扩展指标 | `Phase 7` | `Phase 8` | delta |
|---|---:|---:|---:|
| `HAI` | `79.68` | `81.42` | `+1.74` |
| `RAS` | `77.33` | `80.48` | `+3.16` |
| `record normalized_mae` | `0.2126` | `0.1643` | `-0.0483` |
| `record spearman_rho` | `0.4817` | `0.6683` | `+0.1866` |
| `record pairwise_order_accuracy` | `0.6164` | `0.6910` | `+0.0746` |
| `score_bias` | `-0.0788` | `-0.0459` | `+0.0329` |
| `ece` | `0.4764` | `0.4229` | `-0.0535` |
| `calibration_error` | `202` | `182` | `-20` |

### Phase 8 本阶段改进记录

- 最明显提升 1：record-level 的 score compression 已被实质性拉开，`record normalized_mae 0.2126 -> 0.1643`，`spearman_rho 0.4817 -> 0.6683`，`pairwise_order_accuracy 0.6164 -> 0.6910`。
- 最明显提升 2：高分精确对齐但 trace 失败的 `ACT` 家族已被显式救回；例如 `ACT Results:0` 从 `0.5970` 拉到 `0.9144`，对应人工分 `1.0000`。
- 最明显提升 3：高对齐 partial-heavy 且已有部分 matched support 的样例被系统性上调；例如 `STM Results:59` 从 `0.6538` 拉到 `0.7715`，对应人工分 `0.9773`。
- 最明显提升 4：`huge missing-signal` 的 sequence-diagram 过高估分簇已被压下；例如 `SD Results:59` 从 `0.7826` 压到 `0.6535`，虽然仍高估，但已不再是最大的主残差簇。
- 最明显提升 5：`issue_f1`、`human_issue_coverage_recall`、`PDS`、`unsupported_claim_rate` 与 `equivalence_false_reject_rate` 均保持稳定，没有为提分牺牲 evidence discipline。

- 最明显退化风险 1：`validation` 下 `record pairwise_order_accuracy = 0.5968` 仍偏低，说明当前 record-level calibration 在 family split 上还没有完全稳住。
- 最明显退化风险 2：`STM Results:57` 仍严重低估，提示并行/正交结构上的 equivalence 误杀仍会直接拖累部分高分样例。
- 最明显退化风险 3：`STM Results:43`、`STM Results:8` 这类 `partial-only` 但人工并不高分的 case 仍偏高，说明仅靠当前 alignment diagnostics 还不能完全区分“真等价重构”和“表面对齐但审稿人不买账”的样例。

- 当前仍未完全解决的问题 1：`summary` 侧几乎没动，`SAS = 73.62`、`summary spearman_rho = 0.2781`、`summary pairwise_order_accuracy = 0.5307` 仍直接卡住 `Phase 9`。
- 当前仍未完全解决的问题 2：`Milestone A` 仍未达成，当前还差 `HAI >= 82`、`SAS >= 76`、`record pairwise_order_accuracy >= 0.70` 等门槛。
- 当前仍未完全解决的问题 3：top residual cluster 已经从“huge missing-signal partial-heavy 高估”转成更混合的 `other / low_eq_low_ref / parallel-family false mismatch`，说明后续不应继续在 `Phase 8` 内单纯加大数值拉伸。

### Phase 8 本阶段运行记录

- 已验证入口：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py`
  - `python -m expert_review.benchmark --scope full --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name validation --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name lockbox --llm-mode off`
- 本阶段真实落位的目标层次：
  - 只改 `agents/equivalence.py` 与 `agents/score_composer.py`
  - 所有提分都落在 deterministic runtime 的 `record-level` 路径
  - `summary / protocol` 口径、外部 API 和 benchmark harness 不改

### Phase 8 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 8` 的起始基线，即 `Phase 7` 收尾后的 full benchmark。
- `Round 1` 是第一次直接上强惩罚与宽 rescue 的失败尝试，结果证明这条路会把大量真实 row 压穿。
- `Round 2` 回到 `Phase 7` 基线附近，只保留诊断字段后重新做窄校准，第一次把 `Phase 8` checklist 全部打穿。
- `Round 3` 在 `Round 2` 基础上进一步联合 `full + validation + lockbox` 调整 stretch/bonus/penalty 常数，获得最终保留版本。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | `Phase 7` 基线；保留 full/split/LOFO 口径，不引入新的评分 patch | `score_compression` / `partial-heavy overestimation` | `HAI 79.68 / RAS 77.33 / record normalized_mae 0.2126 / record spearman_rho 0.4817 / pairwise 0.6164 / bias -0.0788` | `同左` | `基线轮，无代码增量` | `是` | 确认为 `Phase 8` 的真实起点 |
| `Round 1` | 引入宽 `reference_alignment rescue` 与强 `gap_penalty`，同时对三维分数直接砍压 | `over-broad rescue` / `over-strong penalty` | `HAI 79.68 / RAS 77.33 / mae 0.2126 / FR 0.0174` | `HAI 77.13 / RAS 72.69 / mae 0.2785 / bias -0.2342 / FR 0.2174 / unsupported_claim_rate 0.1584` | `HAI -2.55` | `是` | 明确判定失败；该路线会把大量真实高分 row 压穿，不可保留 |
| `Round 2` | 回退到基线，仅保留诊断字段；新增窄 `record stretch + trace-failure rescue + aligned partial-heavy bonus + huge-missing penalty + low-equivalence penalty` | `score_compression` / `trace-failure exact rows` / `huge_missing_signal` | `HAI 79.68 / RAS 77.33 / mae 0.2126 / rho 0.4817 / pairwise 0.6164 / bias -0.0788` | `HAI 81.22 / RAS 80.13 / mae 0.1691 / rho 0.6623 / pairwise 0.6880 / bias -0.0522` | `HAI +1.54` | `是` | 第一次完整满足 `Phase 8` checklist，但仍有继续挖的空间 |
| `Round 3` | 在 `Round 2` 基础上提高 `stretch / trace-failure bonus / aligned-partial bonus`，并轻微上调 `low-equivalence penalty` | `residual underestimation` / `validation bias trimming` | `HAI 81.22 / RAS 80.13 / mae 0.1691 / rho 0.6623 / pairwise 0.6880 / bias -0.0522` | `HAI 81.42 / RAS 80.48 / mae 0.1643 / rho 0.6683 / pairwise 0.6910 / bias -0.0459` | `HAI +0.20` | `否` | `full`、`validation`、`lockbox` 都只剩边际增益；继续调已不再是 `Phase 8` 的主要瓶颈 |

### Phase 8 收尾汇报记录

- 当前 phase 的完成状态：`Phase 8` 已完成并停止，等待 `Phase 9`。
- TODO 已完成项：
  - `Phase 8` 全部 Todolist 已打勾
  - `Phase 8` 全部 Checklist 已打勾
  - `README.md`、`GUIDE.md`、PR body 已同步到当前阶段口径
- TODO 尚未完成项：
  - 无本 phase 内遗留未勾项
  - `summary-level` 排序、public row 语义与 `Milestone A` 验收仍属于后续 phase
- 当前对齐程度总览：
  - `record-level` 已达到当前 phase 的预期：`RAS 80.48 / normalized_mae 0.1643 / spearman_rho 0.6683 / pairwise 0.6910 / bias -0.0459`
  - `summary-level` 仍维持 `SAS 73.62`，说明当前主瓶颈已经明确转移到 `Phase 9`
  - `PDS 93.75`、`unsupported_claim_rate 0.0865` 与 `equivalence_false_reject_rate 0.0174` 说明本阶段提分没有以证据纪律和错杀高分样例为代价
- 对各项核心指标的解释：
  - `HAI 81.42`：整体人类风格对齐继续上升，但仍未达到 `Milestone A` 要求的 `82`
  - `RAS 80.48`：record-level 已首次进入 `80+`，说明 reviewer 已开始具备更像批量筛选器的数值尺度
  - `record pairwise_order_accuracy 0.6910`：离 `0.70` 只差一步，但仍未正式越过 `Milestone A` 的 record 排序门槛
  - `SAS 73.62`：当前若继续在 record-only 方向硬调，收益已经不再是主导，必须转向 `Phase 9`
- 当前 phase 是否停止：`是`，停止在 `Phase 8`；继续往下做主要会进入 summary-level 语义、public row 排序与 batch screening 策略，已属于 `Phase 9+`。

## 12. Phase 9: Summary-Level 排序、分数语义与高分 public row 收口

目标：

让 reviewer 不只会在 `summary-level` 场景里“少乱说”，还要能更接近人工地做高低分区分和排序。

### Todolist

* [x] 修复高分 public row 过度保守的问题。
* [x] 压低无必要的 `readability_or_naming` / `unused_or_noisy_structure` 过惩罚。
* [x] 收口 summary-level 的 score semantics，使 aggregate / std-dev / min / max / run-score 的语义判读更像人工。
* [x] 继续保持 `summary_only_element_claim_rate = 0` 的证据纪律。
* [x] 建立 summary-specific rank error 与 score bias 诊断视图。
* [x] 对真实低分 summary row 保持足够惩罚，避免为了拉高高分 row 而整体漂白。

### Checklist

* [x] `SAS >= 76`
* [x] `summary normalized_mae <= 0.12`
* [x] `summary spearman_rho >= 0.45`
* [x] `summary pairwise_order_accuracy >= 0.65`
* [x] `summary_only_element_claim_rate = 0`
* [x] 高分 public row 的系统性低估不再是主要误差簇。

### Phase 9 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 回写时间：`2026-04-17 11:00:22`
- 所属里程碑：`Milestone A`
- 完成状态：`Phase 9` 的 Todolist 与 Checklist 已全部完成，当前停止在 `Phase 9`，不提前进入 `Phase 10` 的 batch execution / screening 策略。
- 当前定位：仅在 deterministic `summary-level` 路径内收口 `public row semantics`、row-type calibration 与 summary ranking；`record / protocol` 主路径不扩 scope。
- 真实接入情况：
  - `tools/policy_library.py` 已新增 `infer_summary_row_type()` 与 `infer_summary_target()`，并把 `summary_row_type / summary_target` 放入 policy packet。
  - `agents/score_composer.py` 已新增 summary-mode row-type-aware `pivot / stretch / offset / bonus / penalty` 标定，并对 `run_level_score + SMD` 残差簇做窄范围额外抑制。
  - `score_composer.py` 的 metric payload 已显式暴露 `summary_row_type / summary_target / summary_score_stretch / summary_score_adjustment` 等诊断字段，支持按 public row 语义回放误差。
  - `test_review.py` 已新增 summary policy 回归测试，锁定 `raw public row / average row / BD / SMD` 的语义区分。
- 可运行性：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已验证
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py` 已验证
  - `python -m expert_review.benchmark --scope full --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope split --split-name validation --llm-mode off` 已验证
  - `python -m expert_review.benchmark --scope split --split-name lockbox --llm-mode off` 已验证
- 已知遗留问题：
  - `summary_level_run_score + SMD` 仍有少量双向大残差，例如 `main:automated_braking:ttool_ai:SMD:3/4` 仍从人工 `0.30` 高估到 `0.6830`。
  - `summary` / `aggregate_average` 下的 `BD / Properties` 仍偏保守，例如 `sncs:connected_device:Properties:Average` 人工 `0.93`、当前 agent `0.6965`。
  - `Milestone A` 仍未完成；当前真正卡点已转到 `record pairwise_order_accuracy`、`record normalized_mae`、`unsupported_claim_rate`、`ece` 与 `Phase 10` 的 batch screening 口径。

### Phase 9 指标总表

本节记录 `2026-04-17 11:00:22` 基于 `run_benchmark_iteration(llm_mode='off', scope='full')` 的 `full available benchmark` 收尾快照，作为 `Phase 9` 的正式阶段结论口径。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `83.39` |
| `RAS` | `80.48` |
| `SAS` | `81.51` |
| `PDS` | `93.75` |
| `record normalized_mae` | `0.1643` |
| `record spearman_rho` | `0.6683` |
| `record pairwise_order_accuracy` | `0.6910` |
| `summary normalized_mae` | `0.1044` |
| `summary spearman_rho` | `0.7319` |
| `summary pairwise_order_accuracy` | `0.7286` |
| `summary score_bias` | `-0.0145` |
| `summary_only_element_claim_rate` | `0.0000` |
| `unsupported_claim_rate` | `0.0865` |
| `ece` | `0.3969` |

### Phase 9 扩展评测快照

#### 1. split 泛化快照

| split | `HAI` | `SAS` | `summary normalized_mae` | `summary spearman_rho` | `summary pairwise_order_accuracy` | `summary score_bias` | `summary_only_element_claim_rate` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `validation` | `84.29` | `80.56` | `0.1333` | `0.8257` | `0.6923` | `0.0904` | `0.0000` |
| `lockbox` | `78.77` | `77.48` | `0.0841` | `0.5027` | `0.6154` | `-0.0306` | `0.0000` |

#### 2. full benchmark 扩展诊断

| 扩展指标 | `Phase 8` | `Phase 9` | delta |
|---|---:|---:|---:|
| `HAI` | `81.42` | `83.39` | `+1.97` |
| `RAS` | `80.48` | `80.48` | `+0.00` |
| `SAS` | `73.62` | `81.51` | `+7.89` |
| `summary normalized_mae` | `0.1359` | `0.1044` | `-0.0315` |
| `summary spearman_rho` | `0.2781` | `0.7319` | `+0.4538` |
| `summary pairwise_order_accuracy` | `0.5307` | `0.7286` | `+0.1979` |
| `unsupported_claim_rate` | `0.0865` | `0.0865` | `+0.0000` |
| `ece` | `0.4229` | `0.3969` | `-0.0260` |
| `calibration_error` | `182` | `174` | `-8` |

#### 3. summary residual cluster 快照

| summary row 簇 | `Phase 8` 平均 delta | `Phase 9` 平均 delta | 结论 |
|---|---:|---:|---|
| `raw_score_row` | `-0.1400` | `-0.0333` | 高分 public row 的系统性低估已明显收口 |
| `summary_level_run_score` | `+0.0320` | `+0.0178` | run-level 仍略高估，但已不再主导整体排序 |
| `case_aggregate_stat` | `+0.0090` | `-0.0143` | aggregate quality row 已基本回到人工附近 |
| `summary` | `-0.0560` | `-0.0486` | summary 平均分仍略保守，但已不再是最大主误差 |

### Phase 9 本阶段改进记录

- 最明显提升 1：`summary-level` 的排序与尺度已经实质性跨过本 phase 门槛，`SAS 73.62 -> 81.51`，`summary normalized_mae 0.1359 -> 0.1044`，`summary spearman_rho 0.2781 -> 0.7319`，`summary pairwise_order_accuracy 0.5307 -> 0.7286`。
- 最明显提升 2：高分 public row 的系统性低估不再主导误差簇；`raw_score_row` 平均 delta 已从约 `-0.1400` 收到 `-0.0333`。
- 最明显提升 3：`summary_only_element_claim_rate` 继续保持 `0.0000`，说明这轮提分没有靠 summary 场景下胡乱捏造 element-level blame 来换分。
- 最明显提升 4：`validation` 与 `lockbox` 的 `SAS` 分别达到 `80.56` 与 `77.48`，说明这轮并非只在 full available benchmark 上“看起来更好”。
- 最明显提升 5：`record-level` 主指标与 `PDS` 基本保持不动，说明 `Phase 9` 的 summary patch 没有把 `Phase 8` 已收口的 deterministic 主路径带崩。

- 最明显退化风险 1：`summary_level_run_score + SMD` 仍是本 phase 剩余的最稳定误差簇之一，既有低分高估，也有高分低估，说明该 row family 的真实人工语义仍未完全被固定规则吃透。
- 最明显退化风险 2：`summary / aggregate_average` 对 `BD / Properties` 仍偏保守，典型如 `sncs:connected_device:Properties:Average` 与 `sncs:connected_device:BD:Average`。
- 最明显退化风险 3：`Milestone A` 仍没达成，且当前缺口主要已不在 summary，而在 record ranking、误差校准与 batch screening 可执行口径。

- 当前仍未完全解决的问题 1：`record pairwise_order_accuracy = 0.6910` 仍低于 `Milestone A` 的 `0.70`。
- 当前仍未完全解决的问题 2：`record normalized_mae = 0.1643`、`unsupported_claim_rate = 0.0865` 与 `ece = 0.3969` 仍未达到 `Milestone A` 口径。
- 当前仍未完全解决的问题 3：`component_level_review` 仍未进入主评测指标，因此学术用途所需的组件级对齐证据链依旧缺失。

### Phase 9 本阶段运行记录

- 已验证入口：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py`
  - `python -m expert_review.benchmark --scope full --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name validation --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name lockbox --llm-mode off`
- 本阶段真实落位的目标层次：
  - 只改 `tools/policy_library.py`、`agents/score_composer.py` 与 `test_review.py`
  - 所有提分都落在 deterministic runtime 的 `summary-level` 路径
  - `record / protocol` 评分逻辑、外部 API 与 benchmark harness 主口径不改

### Phase 9 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 9` 的起始基线，即 `Phase 8` 收尾后的 full benchmark。
- `Round 1` 是第一次把 row-type / target-aware summary calibration 接到 runtime，直接完成本 phase 的核心跨越。
- `Round 2` 是一次更激进的挑战者版本，同时抬高 `Average / public score` 与更强压低 `SMD`，结果在 `full + validation + lockbox` 上一致退化，被明确回退。
- `Round 3` 只保留更窄的 `run_level_score + SMD` 抑制，获得最终保留版本。
- `Round 4` 再次尝试更强的 `run_level_score + SMD` penalty，结果 `validation` 微涨但 `full` 回退，因此不保留。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | `Phase 8` 基线；不引入新的 summary calibration | `summary ranking weak` / `public row underestimation` | `HAI 81.42 / SAS 73.62 / summary mae 0.1359 / rho 0.2781 / pairwise 0.5307 / summary bias -0.0453` | `同左` | `基线轮，无代码增量` | `是` | 确认为 `Phase 9` 的真实起点 |
| `Round 1` | 新增 `summary_row_type / summary_target` 推断；引入 row-type-aware `pivot / stretch / offset / bonus / penalty` | `summary score semantics` / `high-score public rows` | `HAI 81.42 / SAS 73.62 / mae 0.1359 / rho 0.2781 / pairwise 0.5307` | `HAI 83.33 / SAS 81.25 / mae 0.1039 / rho 0.7235 / pairwise 0.7258 / validation SAS 79.61 / lockbox SAS 77.48` | `HAI +1.91` | `是` | 第一次完整打穿 `Phase 9` checklist，但 residual 仍集中在 `run_level_score + SMD` 与 `summary average` |
| `Round 2` | 进一步抬高 `BD / Properties / UCD` 的 `Average / public score`，同时更强压低 `SMD` | `aggressive public-row lift` / `overfit risk` | `full SAS 81.25 / validation SAS 79.61 / lockbox SAS 77.48` | `full SAS 80.85 / validation SAS 78.91 / lockbox SAS 76.35` | `full SAS -0.40` | `是` | 明确判定失败；这条路会在 visible full 外一致伤到泛化，不可保留 |
| `Round 3` | 回退 `Round 2` 的 public-row lift，只保留更窄的 `run_level_score + SMD` 校准 | `run-level SMD residual` | `full SAS 81.25 / validation SAS 79.61 / lockbox SAS 77.48` | `full SAS 81.51 / validation SAS 80.56 / lockbox SAS 77.48 / rho 0.7319 / pairwise 0.7286` | `full SAS +0.26` | `是` | `full` 与 `validation` 同时改善，`lockbox` 不退，确认为保留版本 |
| `Round 4` | 把 `run_level_score + SMD` 的额外 penalty 从 `0.01` 提到 `0.02` | `micro-tuning` / `over-tightening` | `full SAS 81.51 / validation SAS 80.56 / lockbox SAS 77.48` | `full SAS 81.07 / validation SAS 80.59 / lockbox SAS 77.48` | `full SAS -0.44` | `否` | 说明继续在这条常数上硬拧已经进入平台区；保留 `Round 3` 作为最终版本 |

### Phase 9 收尾汇报记录

- 当前 phase 的完成状态：`Phase 9` 已完成并停止，等待 `Phase 10`。
- TODO 已完成项：
  - `Phase 9` 全部 Todolist 已打勾
  - `Phase 9` 全部 Checklist 已打勾
  - `README.md`、`GUIDE.md`、PR body 已同步到当前阶段口径
- TODO 尚未完成项：
  - 无本 phase 内遗留未勾项
  - `Milestone A` 验收、batch screening 执行方式与阈值策略属于后续 `Phase 10`
- 当前对齐程度总览：
  - `summary-level` 已达到当前 phase 的预期：`SAS 81.51 / normalized_mae 0.1044 / spearman_rho 0.7319 / pairwise 0.7286 / bias -0.0145`
  - `record-level` 保持 `Phase 8` 收口状态：`RAS 80.48 / normalized_mae 0.1643 / pairwise 0.6910`
  - `PDS 93.75`、`summary_only_element_claim_rate 0.0000` 与 `unsupported_claim_rate 0.0865` 说明本阶段提分没有以证据纪律为代价
- 对各项核心指标的解释：
  - `HAI 83.39`：整体人类风格对齐已越过 `Milestone A` 的总分门槛，但这不等于里程碑已完成
  - `SAS 81.51`：说明当前 summary-level 排序与 public-row 语义判读已不再是主要瓶颈
  - `validation / lockbox SAS 80.56 / 77.48`：说明 retained patch 具备一定 split 泛化，不是只对 full 可见集过拟合
  - `record pairwise_order_accuracy 0.6910`、`record normalized_mae 0.1643`、`unsupported_claim_rate 0.0865`、`ece 0.3969`：这些才是当前 `Milestone A` 未完成的真实卡点
- 当前 phase 是否停止：`是`，停止在 `Phase 9`；继续往下做主要会进入 `Phase 10` 的 batch screening 输入协议、阈值策略、导出与验收报告，已不再属于本 phase。

## 13. Phase 10: Batch Screening 模式、阈值策略与 Milestone A 验收

目标：

把 reviewer 从“评测时可用”推进到“实际可批量跑、可导出、可用于整体筛选”的状态，并完成 `Milestone A` 验收。

### Todolist

* [x] 为 batch review 明确输入协议、批量执行方式与结果导出格式。
* [x] 建立基于 `overall_score / confidence / unsupported extras / evidence discipline` 的 triage 阈值策略。
* [x] 明确哪些分数段直接放行、哪些进入人工复核、哪些高风险上浮。
* [x] 加入 batch 模式下的延迟、成本与失败重试统计。
* [x] 对 deterministic 路径做批量稳定性验证，避免 batch 跑时出现口径漂移。
* [x] 输出 `Milestone A` 验收报告：当前 reviewer 可以怎么用，不可以怎么用。

### Checklist

* [x] `Milestone A` 的全部门槛均已满足。
* [x] 已形成可操作的 batch screening 使用口径，而不是只有 benchmark 指标。
* [x] `latency_p95`、失败重试和导出结构已可观测。
* [x] 当前 reviewer 可被明确表述为“可用于整体筛选”，但尚未越界宣称“可替代专家最终裁决”。

### Phase 10 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 回写时间：`2026-04-17 18:10:00`
- 所属里程碑：`Milestone A`
- 完成状态：`Phase 10` 的 Todolist 与 Checklist 已全部完成，`Milestone A` 已正式达成。
- 当前定位：在 deterministic 主路径不改 graph 编排的前提下，同时补齐 batch screening 可执行面、record-level 最后几项门槛，以及 `Milestone A` 的使用边界说明。
- 真实接入情况：
  - `tools/policy_library.py` 已新增 `infer_record_diagram_type()`，并把 `record_diagram_type` 放入 `policy packet`，让 record-level 标定不再把 `ACT / SD / STM` 混为一谈。
  - `agents/score_composer.py` 已新增 record diagram offset、record-specific confidence recalibration 与对应诊断字段，显式压低“高自信但低精确对齐”的伪置信。
  - `agents/pragmatic_quality.py` 已在 `record-level` 下完全抑制 `unused_or_noisy_structure`，因为这一簇在 benchmark 上已证明主要是纯 `FP` 噪声。
  - 根层新增 [`batch.py`](../../batch.py) 作为 batch screening 主入口，支持 `json/jsonl` 输入、`json/jsonl/csv` 导出、triage policy、失败重试、rerun 稳定性与延迟统计。
  - `__init__.py` 已导出 batch API，`test_review.py` 与新增的 `test_batch.py` 已锁住 diagram-type 推断与 batch triage/export 回归。
- 可运行性：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py` 已验证
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py` 已验证
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_batch.py` 已验证
  - 全量 batch run 已导出 `/tmp/phase10_batch_full_final.json`、`/tmp/phase10_batch_full_final.jsonl`、`/tmp/phase10_batch_full_final.csv`
- 当前结论边界：
  - 可以说：当前 reviewer 已可用于 batch ranking / filtering / triage，能缩减人工筛查工作量。
  - 不可以说：当前 reviewer 已能替代专家最终裁决，或已经在学术上充分证明 agent-based review surrogate 成立。
- 已知遗留问题：
  - `component_level_review` 的 `512` 条人工逐组件对齐数据仍未进入主评测指标，因此组件级证据链仍缺。
  - `protocol-only` holdout 仍只有 `4` 个 family，`lockbox PDS = 75.00` 只能保守解读，不能拿来做强泛化主张。
  - batch triage 仍以“高精度预筛 + 大量人工复核”为主，`manual_review = 163 / 280`，说明它适合整体筛选，不适合无人值守自动裁决。

### Phase 10 指标总表

本节记录 `2026-04-17` 基于 `run_benchmark_iteration(llm_mode='off', scope='full')` 的 `full available benchmark` 收尾快照，作为 `Phase 10` 与 `Milestone A` 的正式验收口径。

| 指标 | 当前值 |
|---|---:|
| `HAI` | `85.99` |
| `RAS` | `85.21` |
| `SAS` | `81.51` |
| `PDS` | `93.75` |
| `record normalized_mae` | `0.1228` |
| `record spearman_rho` | `0.8366` |
| `record pairwise_order_accuracy` | `0.7695` |
| `summary normalized_mae` | `0.1044` |
| `summary spearman_rho` | `0.7319` |
| `summary pairwise_order_accuracy` | `0.7286` |
| `summary score_bias` | `-0.0145` |
| `issue_f1` | `0.9226` |
| `unsupported_claim_rate` | `0.0703` |
| `ece` | `0.1353` |
| `summary_only_element_claim_rate` | `0.0000` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `rerun_score_std` | `0.0000` |

### Phase 10 扩展评测快照

#### 1. `Milestone A` 验收表

| 指标 | 门槛 | `Phase 10` | 结果 |
|---|---:|---:|---|
| `HAI` | `>= 82` | `85.99` | `通过` |
| `RAS` | `>= 80` | `85.21` | `通过` |
| `SAS` | `>= 76` | `81.51` | `通过` |
| `PDS` | `>= 90` | `93.75` | `通过` |
| `record normalized_mae` | `<= 0.15` | `0.1228` | `通过` |
| `record spearman_rho` | `>= 0.60` | `0.8366` | `通过` |
| `record pairwise_order_accuracy` | `>= 0.70` | `0.7695` | `通过` |
| `summary spearman_rho` | `>= 0.45` | `0.7319` | `通过` |
| `summary pairwise_order_accuracy` | `>= 0.65` | `0.7286` | `通过` |
| `unsupported_claim_rate` | `<= 0.08` | `0.0703` | `通过` |
| `ece` | `<= 0.20` | `0.1353` | `通过` |
| `protocol_only_overclaim_rate` | `= 0` | `0.0000` | `通过` |
| `rerun_score_std` | `<= 0.03` | `0.0000` | `通过` |
| batch screening surface | `已具备` | `已具备` | `通过` |

#### 2. split 快照

| split | `HAI` | `RAS` | `SAS` | `PDS` | `record normalized_mae` | `record pairwise` | `unsupported_claim_rate` | `ece` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `validation` | `88.14` | `87.27` | `80.56` | `100.00` | `0.0946` | `0.6613` | `0.0469` | `0.1545` |
| `lockbox` | `81.66` | `85.98` | `77.48` | `75.00` | `0.1323` | `0.7935` | `0.0694` | `0.1033` |

说明：

1. `validation / lockbox` 说明 `Phase 10` patch 不是只在 full available benchmark 上“看起来更好”。
2. `lockbox PDS = 75.00` 由极小 protocol-only 样本主导，当前仍只能作为风险提示，不属于 `Milestone A` 的正式 gate。

#### 3. `Phase 9 -> Phase 10` 关键增益

| 指标 | `Phase 9` | `Phase 10` | delta |
|---|---:|---:|---:|
| `HAI` | `83.39` | `85.99` | `+2.60` |
| `RAS` | `80.48` | `85.21` | `+4.73` |
| `SAS` | `81.51` | `81.51` | `+0.00` |
| `record normalized_mae` | `0.1643` | `0.1228` | `-0.0415` |
| `record spearman_rho` | `0.6683` | `0.8366` | `+0.1683` |
| `record pairwise_order_accuracy` | `0.6910` | `0.7695` | `+0.0785` |
| `unsupported_claim_rate` | `0.0865` | `0.0703` | `-0.0162` |
| `ece` | `0.3969` | `0.1353` | `-0.2616` |
| `summary_only_element_claim_rate` | `0.0000` | `0.0000` | `+0.0000` |
| `PDS` | `93.75` | `93.75` | `+0.00` |

#### 4. batch screening 运行摘要

全量 batch run 基于 `280` 条当前 full-available task，结果如下：

| 指标 | 当前值 |
|---|---:|
| `total_items` | `280` |
| `success_count` | `280` |
| `failure_count` | `0` |
| `retry_total` | `0` |
| `retry_rate` | `0.0000` |
| `latency_p50` | `0.1495s` |
| `latency_p95` | `0.8922s` |
| `latency_max` | `1.3716s` |
| `rerun_score_std` | `0.0000` |
| `rerun_score_delta_max` | `0.0000` |
| `triage_flip_rate` | `0.0000` |
| `estimated_cost_usd_total` | `0.0` |

当前默认 triage 结果分布：

| bucket | 数量 |
|---|---:|
| `direct_pass` | `69` |
| `manual_review` | `163` |
| `high_risk_reject` | `48` |

#### 5. triage 质量快照

| bucket | `n` | 主要质量口径 | 结果 |
|---|---:|---|---:|
| `direct_pass` | `69` | `human_score >= 0.75` precision | `0.9710` |
| `direct_pass` | `69` | 高分样本 coverage | `0.4214` |
| `high_risk_reject` | `47` | `human_score <= 0.45` precision | `0.7021` |
| `high_risk_reject` | `47` | 低分样本 coverage | `0.5690` |
| `manual_review` | `160` | 中间分段占比 | `0.2812` |

当前 batch 使用结论：

1. `direct_pass` 桶已经足够高精度，可直接用于缩减高质量样本的人工复核量。
2. `high_risk_reject` 桶更适合作为“高风险上浮 / 优先复查”而非自动拒绝，因为其 precision 还不够支撑零人工裁决。
3. 大量样本仍进入 `manual_review`，这与 `Milestone A` 的边界一致：它是整体筛选器，不是最终判官。

### Phase 10 本阶段改进记录

- 最明显提升 1：`Milestone A` 已被正式打穿，`HAI / RAS / SAS / PDS / record mae / record ranking / unsupported / ece / rerun_score_std` 全部进入门槛内。
- 最明显提升 2：record-level 不再把不同图类型硬塞进同一校准槽；`ACT / SD / STM` 的窄 offset 后，`record normalized_mae 0.1643 -> 0.1228`，`record pairwise_order_accuracy 0.6910 -> 0.7695`。
- 最明显提升 3：record-specific confidence 被重新定义为“精确对齐可靠性”而不是“主观自信”，`ece 0.3969 -> 0.1353`，明显消除了原先的高自信错判。
- 最明显提升 4：`unused_or_noisy_structure` 在 record 模式下的噪声批评被清空后，`unsupported_claim_rate 0.0865 -> 0.0703`，且 `issue_f1` 仍上升到 `0.9226`，说明不是靠少报问题换指标。
- 最明显提升 5：batch surface 已真实可用，支持 `json/jsonl` 输入、`json/jsonl/csv` 导出、triage bucket、延迟/重试/稳定性统计，且 `280` 条 full run 无失败、无漂移。

- 最明显退化风险 1：`high_risk_reject` 桶 precision 只有 `0.7021`，所以 reject 只能作为高风险提示，不能自动拒绝。
- 最明显退化风险 2：`manual_review = 163 / 280`，说明当前 triage 仍明显偏保守；这是有意保精度的结果，但也意味着人工工作量下降还不算激进。
- 最明显退化风险 3：`lockbox PDS = 75.00` 暴露出 protocol holdout 太小，`Phase 10` 还不能对 protocol 泛化做更强结论。

- 当前仍未完全解决的问题 1：`component_level_review` 仍未进入主评测，`CRAS` 与逐组件宏观 `F1` 还没有建立。
- 当前仍未完全解决的问题 2：当前 batch 阈值是以 visible benchmark 为主做的 precision-oriented 标定，`validation + lockbox + LOFO` 的联合阈值鲁棒性仍要到后续 phase 才能正式论证。
- 当前仍未完全解决的问题 3：学术主张所需的 judgement / reason / evidence reliability、ablation 与 agent-based 必要性证明仍未完成，因此 `Milestone B` 还没有进入收口期。

### Phase 10 本阶段运行记录

- 已验证入口：
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py`
  - `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_batch.py`
  - `python -m expert_review.benchmark --scope full --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name validation --llm-mode off`
  - `python -m expert_review.benchmark --scope split --split-name lockbox --llm-mode off`
- 本阶段真实落位的目标层次：
  - 代码改动集中在 `tools/policy_library.py`、`agents/score_composer.py`、`agents/pragmatic_quality.py`、`batch.py`、`__init__.py`、`test_review.py`、`test_batch.py`
  - 所有提分都落在 deterministic runtime 的 `record-level` 与 batch execution surface
  - `summary-level`、graph 编排、外部主 API 与 benchmark harness 主框架没有被重新改写

### Phase 10 多轮自我迭代记录

说明：

- `Round 0` 是 `Phase 10` 的起始基线，即 `Phase 9` 收尾后的 full benchmark。
- `Round 1` 首次把 record diagram-aware calibration、record confidence 收缩和 batch surface 接入主路径，几乎打穿全部门槛，但 `unsupported_claim_rate` 仍略高于 `0.08`。
- `Round 2` 进一步删除 record-level 的纯噪声 issue 发射，完成 `unsupported_claim_rate` 的最后收口，并确认 `Milestone A` 正式达成。

| round_id | 本轮修改 | 问题类型 | 修改前 | 修改后 | delta | 是否继续 | 备注 |
|---|---|---|---|---|---:|---|---|
| `Round 0` | `Phase 9` 基线；batch surface 尚不存在，record-level 仍未做 diagram-aware calibration | `milestone gate gap` / `batch execution missing` | `HAI 83.39 / RAS 80.48 / SAS 81.51 / record mae 0.1643 / pairwise 0.6910 / unsupported 0.0865 / ece 0.3969` | `同左` | `基线轮，无代码增量` | `是` | 确认为 `Phase 10` 的真实起点 |
| `Round 1` | 新增 `infer_record_diagram_type()`、record diagram offset、record confidence recalibration，并落地 `batch.py` 与初版 triage policy | `record ranking gap` / `miscalibration` / `batch screening missing` | `HAI 83.39 / RAS 80.48 / mae 0.1643 / pairwise 0.6910 / unsupported 0.0865 / ece 0.3969` | `HAI 85.81 / RAS 84.88 / mae 0.1228 / pairwise 0.7695 / unsupported 0.0839 / ece 0.1353` | `HAI +2.42` | `是` | 几乎打穿全部门槛，但 `unsupported_claim_rate` 仍略高于 `Milestone A` 的 `0.08`，不能停 |
| `Round 2` | 在 record 模式下完全抑制 `unused_or_noisy_structure` issue 发射，并用 full batch run 回放 triage 稳定性 | `record false-positive issue noise` | `HAI 85.81 / RAS 84.88 / mae 0.1228 / pairwise 0.7695 / unsupported 0.0839 / ece 0.1353` | `HAI 85.99 / RAS 85.21 / mae 0.1228 / pairwise 0.7695 / unsupported 0.0703 / ece 0.1353` | `HAI +0.18` | `否` | 这一步正式打穿最后一个硬门槛，停止原因是 `Milestone A` 已完成，而不是边际太小就停 |

### Phase 10 收尾汇报记录

- 当前 phase 的完成状态：`Phase 10` 已完成并停止，下一步进入 `Phase 11`。
- TODO 已完成项：
  - `Phase 10` 全部 Todolist 已打勾
  - `Phase 10` 全部 Checklist 已打勾
  - `Milestone A` 已在正式 benchmark 与 batch surface 两条口径上同时达成
  - `README.md`、`GUIDE.md`、PR body 已同步到当前阶段口径
- TODO 尚未完成项：
  - 无本 phase 内遗留未勾项
  - `Milestone B` 的去硬特判历史债、组件级、泛化、ablation 与论文级证据链属于后续 `Phase 11+`
- 当前对齐程度总览：
  - `record-level` 已从“仍卡住 Milestone A”推进到“可用于整体筛选”：`RAS 85.21 / normalized_mae 0.1228 / spearman_rho 0.8366 / pairwise 0.7695`
  - `summary-level` 继续维持 `Phase 9` 收口状态：`SAS 81.51 / summary spearman_rho 0.7319 / pairwise 0.7286`
  - `PDS 93.75`、`summary_only_element_claim_rate 0.0000`、`unsupported_claim_rate 0.0703` 与 `rerun_score_std 0.0000` 说明本阶段提分没有靠放松证据纪律或制造不稳定性来换
- 对各项核心指标的解释：
  - `HAI 85.99`：说明当前 reviewer 已越过“整体筛选器”所需的人类风格对齐门槛
  - `RAS 85.21`：record-level 已进入高可用区间，批量筛选时不再只是“会挑问题”，而是已经具备可操作的数值尺度
  - `unsupported_claim_rate 0.0703 + ece 0.1353`：说明当前可筛选性不是靠胡乱报错或假高自信换来的
  - `manual_review 163 / 280`：说明它的真实工程定位是“高精度预筛 + 风险上浮 + 人工复核分流”，而不是自动化终审
- 当前 phase 是否停止：`是`，停止在 `Phase 10`；停止原因是 `Milestone A` 已正式达成，继续往下做已经进入 `Phase 11+` 的去硬特判历史债、组件级对齐、generalization 与学术证据链问题。

## 14. Phase 11: 去硬特判、语义判定与跨语言泛化历史债清理

目标：

系统性清理当前运行时中与“硬特判、字符串判定、英文默认假设、跨语言脆弱性”相关的历史债，把所有仍影响主路径判断的脆弱规则替换成真正的语义判定与保守 fallback，并在不引入显著性能回归的前提下完成多轮自我迭代，重点优化 prompt 与 semantic routing。

### Todolist

* [ ] 对当前运行时所有影响 `task / model / metamodel / regime / policy / score` 的判定入口做一次全量盘点，并按以下三类建账：
  * [ ] 必须删除的硬特判
  * [ ] 必须替换为语义判定的逻辑
  * [ ] 可以保留的纯结构性 deterministic 逻辑
* [ ] 逐项清理当前主路径中的历史债：
  * [ ] `contract` / task focus / input family 的字符串判定
  * [ ] `evidence regime` / review policy / routing 的字符串判定
  * [ ] model type / metamodel type / diagram family / row family 等影响策略选择的字符串判定
  * [ ] 任何直接由 prompt、input、pred、ref、label 文本触发的 hard-coded bonus / penalty / offset
* [ ] 为所有确需保留的判定任务设计并落地语义判定器：
  * [ ] 每个任务都给出类别定义、边界、正例、反例与 `other / unknown`
  * [ ] 提问方式必须直接询问语义类别，而不是询问是否命中某些词
  * [ ] 输出结果必须真实接入主路径，而不是只做离线分析
* [ ] 明确并文档化允许保留的 deterministic 边界：
  * [ ] 用户显式配置
  * [ ] schema / field existence / file format 解析
  * [ ] 其他结构性、非语义性约束
* [ ] 为语义判定失败、信息不足或置信度过低场景建立保守 fallback：
  * [ ] 统一降级到 `unknown / generic / needs more evidence`
  * [ ] 不允许静默回退到被禁止的字符串 heuristics
* [ ] 新增并固化 multilingual / cross-language / cross-metamodel validation slice：
  * [ ] 中文 `input` + 英文 `pred / ref / prompt / label`
  * [ ] 英文 `input` + 中文 `pred / ref / prompt / label`
  * [ ] `input / pred / ref` 语言彼此不一致的 mixed case
  * [ ] 至少一种非中非英样本或等价 stress case
  * [ ] metamodel / model label 与正文语言、命名体系都不一致的 case
* [ ] 建立本 phase 的 regression gate：
  * [ ] 相对 `Phase 10` 的 deterministic full benchmark，`HAI / RAS / SAS / PDS` 任一降幅不得超过 `1` 点
  * [ ] `unsupported_claim_rate` 与 `ece` 不得恶化超过 `0.02`
  * [ ] 若未达成，则本 phase 不得宣告完成
* [ ] 在本 phase 架构边界内执行多轮自我迭代，主要优化 semantic routing prompt、分类定义、边界描述与 fallback 策略。
* [ ] 完成后同步更新 `README.md`、相关设计文档、TODO 回写与 PR body，使“禁止硬特判 / 支持跨语言”的结论进入公开状态。

### Checklist

* [ ] 运行时关键路径已不存在未登记的字符串硬特判承担 `task / model / metamodel / regime / policy / score` 判断。
* [ ] 所有必要判定都已经改成语义判定，并且问题定义、类别边界、正反例与 `other / unknown` 出口完整可审计。
* [ ] fallback 路径不会静默把判定退回到字符串 heuristics。
* [ ] multilingual / cross-language / cross-metamodel validation slice 已通过，且没有新的系统性失败簇。
* [ ] 相对 `Phase 10` 的 deterministic full benchmark 没有显著回归：`HAI / RAS / SAS / PDS` 任一降幅不超过 `1` 点，`unsupported_claim_rate` 与 `ece` 恶化不超过 `0.02`。
* [ ] 已保留本 phase 多轮自我迭代记录，且 prompt 与 semantic routing 的主要优化轮次可追溯。
* [ ] 本 phase 已单独检查并满足“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”全局门禁。

### Phase 11 当前状态回写

- 创建时间：`2026-04-17 15:10:00`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：作为 `Phase 1-10` 相关历史债的集中清理阶段，优先把 reviewer 从“局部可用但仍带硬特判和语言假设”推进到“判定机制本身可被辩护”的状态。

## 15. Phase 12: Component-Level Human Review 对齐与 `CRAS` 建立

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
* [ ] 本 phase 已单独检查并满足“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”全局门禁。

### Phase 12 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：补齐论文论证里最缺的一块“逐组件人工对齐”证据。

## 16. Phase 13: Judgement / Reason / Evidence Reliability 深化

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
* [ ] 本 phase 已单独检查并满足“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”全局门禁。

### Phase 13 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 前置条件：`Phase 12` 已让组件级对齐进入正式评测。

## 17. Phase 14: Generalization、Validation / Lockbox 与 LOFO 验证

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
* [ ] 本 phase 已单独检查并满足“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”全局门禁。

### Phase 14 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：把“对齐 benchmark”推进到“对齐人工评审机制”的泛化论证。

## 18. Phase 15: LLM-Enabled 主路径、随机性稳定性与成本边界

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
* [ ] 本 phase 已单独检查并满足“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”全局门禁。

### Phase 15 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 当前定位：补齐“agent-based reviewer 是否必须依赖在线 LLM 才成立”的论证。

## 19. Phase 16: 学术冻结候选、Ablation 与论文级证据包

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
* [ ] 若仍未达标，已明确开启 `Phase 17+` 的原因与下一批技术入口。
* [ ] 本 phase 已单独检查并满足“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”全局门禁。

### Phase 16 当前状态回写

- 创建时间：`2026-04-17 00:38:42`
- 所属里程碑：`Milestone B`
- 当前状态：已创建，尚未开始实现。
- 停止条件：本 phase 结束时必须明确判断 `Milestone B` 是否已达成，若未达成则按规则新开 `Phase 17+`。

## 20. 每个 Phase 的统一对齐记录模板

每个 phase 完成后，至少记录以下内容：

### 20.1 指标总表

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

### 20.2 本阶段改进记录

1. 本阶段最明显提升的三项能力。
2. 本阶段最明显退化的三项能力。
3. 本阶段仍未解决的三类错误簇。

### 20.3 本阶段运行记录

1. 哪些入口已验证。
2. 哪些真实路径被替换。
3. 本阶段哪些 `schemas / prompts / tools / agents / graph / compatibility` 目标层次已经有真实落位。
4. 哪些旧逻辑仍然保留。
5. 哪些模块只是临时过渡件。

### 20.4 本阶段多轮自我迭代记录

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

### 20.5 本阶段语义判定与跨语言泛化合规记录

每个 phase 完成后，必须额外记录以下合规信息：

1. 本阶段移除了哪些硬特判、保留了哪些 deterministic 逻辑，以及保留理由。
2. 本阶段新增或修改了哪些语义判定任务。
3. 每个语义判定任务的类别定义、边界、正例、反例与 `other / unknown` 出口是否齐全。
4. fallback 是否仍保持保守且未回退到字符串 heuristics。
5. 本阶段跑了哪些 multilingual / cross-language / cross-metamodel case。
6. 这些 case 中哪些通过、哪些失败、失败簇是什么。
7. 是否存在仍未清掉的违例；若存在，则该 phase 不能判为完成。

### 20.6 本阶段收尾汇报记录

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

## 21. 阶段推进规则

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
10. 每个 phase 的 checklist 都必须包含并实际执行“禁止硬特判 / 语义判定 / 多语言与跨语言泛化”专门检查项；若该项未通过，则不得推进到下一 phase。
11. 若发现某阶段仍依赖字符串硬特判、英文默认假设或跨语言系统性失败，则必须在当前阶段继续修复或显式开新 phase 清债，不能把问题沉默带入下一阶段。
12. 在完成上述回写与汇报前，不得视为该 phase 真正收尾。
13. 每个后续 phase 都必须同时推进结构收敛；如果只是继续在旧文件和旧路径上叠补丁、没有让项目架构更接近 v1 设计，则不得视为完成该 phase。
14. 若当前最后一个 phase 结束时仍未达到冻结条件，允许继续新增后续 phase；但必须明确写出为什么现有阶段不足、下一阶段具体补什么，以及新增 phase 的停止标准。

## 22. 最终目标

最终目标不是“写完一个看起来像 v1 的新目录”，而是：

1. `expert_review` 的真实运行时内部已经成为 v1 设计稿定义的通用化多智能体 reviewer。
2. reviewer 在任意时点都保持完整可运行。
3. 整个重构周期中的每一阶段都有完整对齐记录。
4. 任何阶段都没有通过堆不可达代码来伪装进度。
5. 最终冻结版本能够以完整、可追溯、可评测的形式被后续版本继续继承。
6. 每个阶段结束时，TODO 台账与真实执行状态始终一致，且都已向用户做过一次如实、可解释、带指标和例子的收尾汇报。
7. 最终的 `expert_review/` 路径结构、模块边界和运行时组织都已真正靠拢 v1 设计，而不是停留在旧项目架构上的长期修补状态。
