# agent_loop/ — 上一版单 Agent discover 实现（已退出运行路径）

> 🔴 **本目录不在当前运行路径上。代码完整保留，但论文的任何数字都不来自这里。**
>
> | 问题 | 答案 |
> | :-- | :-- |
> | 当前活的实现在哪 | [../../../pipeline/feedback_loop/](../../../pipeline/feedback_loop/)，包 `paper_stm_feedback_loop` |
> | 本目录的包名 | `paper_stm_repair_loop`（旧名，见 [../../../pipeline/README.md](../../../pipeline/README.md) §4） |
> | 入口还能跑吗 | 能，但**前缀已改**：`make legacy-discover-*`，不是 `make discover-*` |
> | 为什么保留 | 一次性代码搬运与 golden fixture 来源；作为架构对照的历史记录 |
> | 测试规模 | 266 个（`make legacy-discover-test`） |
>
> ⚠️ **`make discover-demo` / `make discover-test` 现在转发到 [../../../pipeline/feedback_loop/](../../../pipeline/feedback_loop/)。** 本文件下文 §8、§10 里写的这两条命令**已经不指向本目录**——正确的 legacy 入口见 §8.0。
>
> ⚠️ **本目录没有自己的 `Makefile`。** 所有 `make` 目标都定义在**仓库根 `Makefile`** 里。
>
> ⛔ 运行时禁止 import `paper_stm_repair_loop`，也不得把 `agent_loop/src` 加入活路径的 `PYTHONPATH`。

## 0. 与当前实现的架构差异（这是本目录唯一的现存价值）

| 维度 | 本目录（旧） | [../../../pipeline/feedback_loop/](../../../pipeline/feedback_loop/)（当前） |
| :-- | :-- | :-- |
| 编排 | 一个顶层 Discover Agent + 11 个工具，Agent 自行决定调用顺序 | 确定性 LangGraph StateGraph，阶段固定 |
| 审查 | Agent 主动调 `review_discovery_coverage`，内含两个隔离 reviewer | 每个生产阶段配一个审查者，路由强制打回 |
| 断言来源 | Agent 自由撰写表达式，由注册门禁事后拒绝 | 先验闭合的 19 谓词词表 |
| 输入根 | [../../../selected_seed_examples/](../../../selected_seed_examples/)（`load_pair()`） | `../representation/reports/llms_emp_r45_java_60/` |
| 失败语义 | 门禁拒绝可导致整次 attempt 终止 | 降级落盘，带结构化诊断 |

下文是这一版的完整设计记录，**按历史材料阅读**，其中「paper1 核心贡献是 feedback-driven loop」「Repair / Confirm 后续阶段」等表述均已被 2026-08 的收窄定调作废：paper1 只做 issue discover，贡献口径以 [../../../README.md](../../../README.md) §2 为准。

---

## 历史设计记录（以下内容保留原样）

本目录实现 paper1 早期版本的 `B-discover`：给定 A 阶段已经准备并冻结的 `<NL, raw/source STM_0, fcstm STM_0>`，在 FCSTM 中间语义层上完整探索行为义务，发现 source-level 行为问题，并把问题、通过项、执行证据和覆盖审查写入不可变运行记录。

Discover 只读，不修改 `STM_0`，不执行 Repair、Confirm，也不在运行中回到 PlantUML 或其他 source 表示层。raw/source 与 source trace 仅用于 grounding 和归因。FCSTM、Controller、records 和审查工具是方法基础设施，不单独作为 headline contribution。

## 1. 当前方法结构

一次 Discover attempt 只有一个顶层 Discover Agent `AgentApp.run`：

```text
冻结 NL / raw source / FCSTM / source trace
  -> Controller 机械分段、生成 coverage rows 和 SourceFact inventory
  -> 同一次 Discover Agent run
       -> 读取 FCSTM guide 和冻结任务
       -> 双向探索 NL -> model 与 model -> NL/source
       -> 注册完整 CoverageUnit / Root / assertion 计划
       -> 逐条 eval_assert
       -> 调用 review_discovery_coverage
            -> 隔离的 semantic coverage reviewer
            -> 隔离的 adversarial falsification reviewer
       -> 按审查建议补查、修订、重跑并再次审查
       -> 当前台账审查通过后提交一次结构化结果
  -> Controller 复验并发布 discover_completed
  -> 确定性生成 loops/discover.md
```

`review_discovery_coverage` 是 Discover Agent 可调用的同级业务工具，不是第二个顶层 orchestrator。该工具内部运行两个无工具、无 gold、无模型修改权限的独立 LLM reviewer。它们只审查当前冻结输入和完整台账，并把结构化意见返回主 Agent。任一 reviewer 未通过，主 Agent 都必须在同一个 Discover run 内继续工作。

## 2. Controller 与 Agent 边界

Controller 只建立 issue-agnostic 的确定性骨架：

1. 校验 fresh run、输入角色、hash、pyfcstm 版本和 submodule commit。
2. 使用 pyfcstm public API 完成 parse、semantic、inspect 和基础运行能力检查。
3. 机械切分 NL 为稳定 `InputSegment`。
4. 为每个非 meta clause 建立基础 behavior row，并为实际出现的结构、数量、条件、effect、顺序、持续性、完成、时序等 cue 建立 `CoverageRequirement`。
5. 从 structured inspect 和 source trace 生成完整 `SourceFact` inventory。
6. 装配只绑定当前冻结任务的工具和 append-only records。
7. 对 plan、断言执行、归因、审查指纹和最终提交做失败关闭式校验。

Controller 不做以下工作：

- 不预设 D01-D12 或其他问题 taxonomy。
- 不预测哪个位置存在问题。
- 不生成 gold issue、gold assertion 或 expected verdict。
- 不把 conversion/lowering 差异自动判为 source-level issue。
- 不用正集 inventory 冒充“缺失元素已经被发现”。

Discover Agent 负责解释 NL 语义、识别独立可修复义务、选择证据路线并形成正向命题。`True` 始终表示模型满足该 Root，`False` 表示模型与该 Root 矛盾。禁止通过双重否定、expected-failure 元数据或常量表达式把期望答案写入断言。

## 3. 覆盖台账

Controller 冻结三类基础对象：

| 对象 | 含义 | 完整性作用 |
|---|---|---|
| `InputSegment` | NL 的机械片段 | 任何片段必须进入 Unit 或得到非行为 disposition。 |
| `CoverageRequirement` | clause 基础行为义务和实际 cue 行 | 每个 ID 必须进入同 clause Unit，并由同强度 required assertion 直接引用。 |
| `SourceFact` | state/event/variable/transition/guard/effect/initial/hierarchy/region 等结构化事实 | 完整 inventory 用于双向探索；被选作 assertion evidence 的事实必须进入 Unit，并由兼容的事实特定谓词直接检查。 |

Agent 注册：

```text
CoverageUnit
  -> exactly one PropositionRootNode
       -> one or more required LogicalAssertion chains
            -> append-only versions
                 -> per-version eval_assert records
```

断言可以修订，但 Unit、Root、basis、required 状态和 evidence scope 不得被弱化。每次修订创建新版本，旧版本和旧执行记录保留。所有 latest required assertions 都必须得到有模型证据的 terminal bool；异常、unsupported、non-bool、超时或证据族不满足均为 `inconclusive`，不能自动当作问题。

注册失败不仅返回 error code，还返回 `required_actions`。对未直接验证的 SourceFact，反馈包含完整事实快照、兼容 evidence family、可接受谓词示例、推荐工具、具体动作和通过判据。这样严格门禁不会退化为要求 Agent 猜测内部 AST 规则。

## 4. 十一项 Agent 工具

| 工具 | 状态 | 作用 |
|---|---|---|
| `read_fcstm_guide` | 必用 | 第一次业务调用；读取 `pyfcstm.llm` FCSTM guide、版本与 SHA。 |
| `read_task` | 必用 | guide 后读取完整冻结任务；重复调用只返回稳定身份信息。 |
| `read_fbmcq_guide` | full formal profile 必用 | `read_task` 后固定读取一次官方指南，只表示能力已知，不强制调用 FBMCQ；non-formal ablation 不暴露该工具。 |
| `inspect_model` | 可用 | 读取 Controller 冻结的 parse/semantic/inspect/diagnostics/metrics，只生成弱线索，不直接产生 issue verdict。 |
| `query_model` | 可用 | 以 strict `entities/topology/path` operation 查询结构与 guard-agnostic 拓扑事实；正向路径不等于 runtime 可执行。 |
| `observe_trace` | 可用 | 按 FCSTM cycle 语义探索一条明确有限轨迹；支持 cold 或 exact-state + complete-vars hot start，不单独支撑普遍性结论。 |
| `lookup_source_trace` | 可用 | 查询 source/FCSTM 映射，只支持归因，不决定 NL 是否满足。 |
| `register_coverage_plan` | 必用 | 原子化注册 Units、Roots、bases 和所有 initial assertions。 |
| `eval_assert` | 必用 | 每次只执行一条已注册 latest assertion，并记录真实调用与结果。 |
| `revise_assertion` | 条件使用 | 对 inconclusive 或被审查证明为弱/错向的断言追加新版本。 |
| `review_discovery_coverage` | 必用 | 对当前完整台账执行双独立审查；通过前禁止提交。 |

所有工具都不接受任意文件路径、URL、shell、外部 Python、alternate case、reference/gold、Repair 或模型修改参数。每个 Agent-facing tool 的注册 docstring 必须自包含说明 Purpose、When to use、When not to use、Parameters、Returns、Execution、Failure semantics、Evidence limitations、Permissions 和 Example，并由合同测试读取真实注册 description。

`eval_assert` 的受限环境把 structure/relation/effect、simulation 和 bounded formal verification 作为同等地位的证据能力，由 Agent 根据命题量化范围选择，不按固定阶梯调用。其中：

- `simulate(cycles, initial_state=None, initial_vars=None)` 支持 cold/hot start；cold start 可用 partial `initial_vars` 覆盖部分声明变量，其余使用 declaration initializer，仍需显式前置 `[]`；hot start 的第一个 cycle 直接从冻结初始状态执行，不要求前置 `[]`，但不能证明 cold reachability 或被跳过的 entry action；
- `topology()` / `path()` 回答 guard-agnostic 结构可达与路径问题；正向结果只是 runtime 可行性的 over-approximation；
- `fbmcq(...)` 可用 NL 明示的 `requirement_bound`，也可以使用诚实记录有限 horizon 的 `analysis_bound`；bounded result 不得写成无界证明。

环境另提供开放式 `effect_deltas(source=..., event=..., target=...)`。它返回当前匹配迁移上全部可解析的 `(variable, delta)`，无变量或无 effect 时返回空 tuple。对于“某动作使某个计数减少”但当前模型根本没有对应变量的 NL 义务，Agent 可写 `any(delta < 0 for _, delta in effect_deltas(...))`，从而让缺失行为稳定得到 `False`，而不需要虚构 `dummy`、`sentinel` 或不存在的变量名。已知且可追溯的真实变量仍可使用 `effect_delta(..., variable=...)`。

注册门禁同时拒绝两类已经在真实运行中观察到的 coverage gaming：

- 用不存在的哨兵变量调用 `effect_delta`，再把 `None` 当作“已检查完整 effect”的证据；
- 先按三个已知名称过滤状态，再用 `len(...) == 3` 冒充对“包含三个区域”的完整基数检查。

基数断言必须比较一个完整、稳定、由模型定义的范围，例如 `len(states(parent='Root.Searching', recursive=False)) == 3`；不能用候选名枚举、成员过滤或字面量列表把结果凑成目标数，也不能通过 `or` 附加一个会独立返回 `True` 的旁路。数量对象必须与 NL 一致：areas/modes/regions 计 `states`，events 计 `events`，variables/counters 计 `variables`，明确的 transitions 才计 `transitions`；不能用 plan-derived `bound_model_refs` 或无关 inventory 代替。areas/modes/regions 等层级数量还要求 `states(parent=..., recursive=False)` 的 parent 与同一 Root 的 `state:<parent>` model ref 精确一致；共享前缀的嵌套无关容器不能通过。

方向 effect 断言同样必须直接决定顶层布尔值。`effect_delta.variable` 只能是冻结模型中真实存在的单一字符串字面量，不能在表达式中拼接或动态选择；开放式 `effect_deltas` 只能使用无过滤 generator，并必须用 literal source、event（或显式 `None`）和 target 绑定一条确定迁移，不能先挑中一个有利变量或搜索全模型无关 effect，再声称已经检查当前义务。

## 5. 独立覆盖审查

`review_discovery_coverage` 只允许在完整 plan 已注册，且所有 latest required assertions 均为 terminal 后调用。工具向两个隔离 reviewer 提供：

- 完整 NL、FCSTM、raw source、source trace 和 normalized inspect；
- 全部 Segment、Requirement 和 behavior SourceFact；
- Units、Roots、latest assertions、真实执行记录；
- 审查前 Controller projection；
- 当前台账 fingerprint 与必须逐项审查的 ID 集合。

两个 reviewer 分工：

1. `semantic_coverage`：逐条核对 NL 对象、触发、源/目标、数量、方向、顺序、持续性、完成范围和时限是否被同强度正向命题覆盖。
2. `adversarial_falsification`：主动构造可能让当前断言错误通过的路径、guard、effect、hierarchy、initialization、timing、issue projection 等反例。

每个 reviewer 必须显式枚举全部 required Segment、Requirement、Root，以及当前计划选作断言证据的 SourceFact ID；完整 SourceFact inventory 仍提供给 reviewer 用于攻击会推翻主要结论的明显漏项，但不机械要求逐事实断言。Controller 对 required ID 集合做精确相等校验。failed finding 还必须至少关联一个当前真实台账 ID；虚构 ID、泛泛评论或无关联建议均失败关闭。

每条失败意见同时包含：

```text
problem
required_scope
observed_scope
scope_gap
risk
related_*_ids
coverage_dimensions
routes
recommended_tools        # 可选；只有语义不可替代时才 mandatory
recommended_steps        # 可选恢复路线，不是工具配额
recommended_action
pass_criterion
```

因此 review 不是只给裁决。它必须先说清命题要求什么范围、当前证据真正覆盖了什么、两者的语义缺口及风险，再给出一条或多条等强恢复路线和可观察通过条件。`required_function_families` 只证明某证据 family 真实调用，不证明证据范围已足够；reviewer 也不能因未调用某工具就机械拒绝。程序化 ID mismatch 和过早调用 review 仍会生成确定性 `required_actions`。

`coverage_dimensions` 明确指出建议将增加或重查哪一类覆盖，例如 `nl_semantics`、`model_behavior`、`source_trace_grounding`、`assertion_strength`、`issue_projection_evidence` 或 `anti_gaming`。`recommended_action` 不能只写“继续检查”或“提高覆盖率”，必须说明要检查的具体行为、路径、条件或 evidence dimension；`pass_criterion` / 兼容字段 `pass_criteria` 必须给出下一次 review 可观察、可判定的闭合条件。建议只能使用当前 Discover 已暴露的能力，不能要求 Agent 直接改 Controller projection，也不能用 FBMCQ 解释 NL，或把 NL 加强成原文没有的 `only`、every-state、future-model 义务。`recommended_action` 必须点名至少一个 `related_*_ids` 中的当前台账 ID 和具体检查对象；只有 `recommended_tools` 非空、表示某工具语义不可替代时，action 才必须点名相应工具。`recommended_steps` 若存在，其工具必须属于 `recommended_tools`，related IDs 必须属于当前 finding，`suggested_arguments` 继续复用真实工具 Pydantic 输入合同校验。全称量词是否越界由持有冻结 NL 的 gate 判断；原文明确写了 `all states` 时不会被关键词门禁误拒。

审查通过绑定 `reviewed_state_fingerprint`。任何后续 `eval_assert` 或 assertion revision 都会改变 fingerprint，使旧 pass 立即失效；必须重新执行双审查。

如果 reviewer provider、stream 或结构化输出链路临时失败，工具返回 `execution_status=retryable_reviewer_failure` 和 `passed=false`，保留当前台账并写入 append-only record。主 Agent 必须在不改动当前 fingerprint 的情况下重试；基础设施失败既不能被视为覆盖通过，也不能被伪装成某个 source-level issue。

只有 provider/transport 类临时故障允许上述重试；schema-invalid verdict、错误 review kind 等确定性合同故障返回 `execution_status=reviewer_contract_failure`，保留同轮已完成 reviewer verdict 和失败审计，并终止当前 Discover attempt。它们不能通过反复调用同一工具被掩盖。

## 6. Issue 投影与归因

全部 latest assertions 执行且双审查通过后，Controller 投影：

- `issue_root_projection`：正向 Root 被证据反驳，且 source attribution 足以支撑问题归因。
- `regression_guard_projection`：正向 Root 已满足，后续 Repair 必须保持。
- `incomplete_root_projection`：仍有非 terminal 断言；此时禁止成功提交。

非 identity 输入只有在冻结 source trace 提供精确一对一映射时，contradiction 才能发布为 `confirmed` 并进入 Repair。ambiguous/untraceable conversion attribution 必须保持 `candidate_only` 和 `downstream_repair_allowed=false`。raw/source 与 FCSTM 文本完全相同且 `relation_policy=exact_identity` 时，Controller 使用同一结构事实建立可审计 identity 归因；这只消除 conversion 歧义，不提供 gold verdict。

## 7. 一次运行的强制顺序

System prompt 要求同一个 Discover run 完成：

1. full formal profile 固定执行 `read_fcstm_guide -> read_task -> read_fbmcq_guide`；non-formal ablation 只执行前两步且不暴露 formal 工具。读 guide 只表示能力已知，不强制对所有 Root 使用 FBMCQ。
2. 对每个主要 NL clause/cue 找到模型实现，并使用完整 SourceFact inventory 探索会实质影响这些义务的模型交互；不机械地为每个事实单独建断言。
3. 根据命题是结构事实、单个具体工况还是多 execution/valuation/path 性质，选择 structure/effect、simulation 或 FBMCQ；可选 `inspect_model` 只用于找线索。注册前只允许一次绑定明确 proposition 的定向 query/trace，source trace 仍只在真实矛盾后用于归因。
4. 注册完整计划；被拒后必须按 `required_actions` 修正完整计划，不能删除困难义务。
5. 对每条 latest required assertion 分别调用 `eval_assert`。
6. 对 inconclusive 或审查指出的弱命题调用 `revise_assertion`，再执行新版本。
7. 调用 `review_discovery_coverage`；一次 failed review 返回多条行动时，先完成该轮全部 `required_actions/recommended_steps` 及其 pass criteria，再重复审查，直至当前 fingerprint pass。
8. 核对 attribution 和最终 projection。
9. 仅提交一次与 Controller projection 一致的 `submit_discovery`。

业务工具的拒绝与失败由本次 Agent 自行消化，不再由外部 controller 猜测下一项语义动作。每个非完成返回都必须提供错误对象、`required_actions`、建议工具、具体修正动作和可观察的 pass criteria；system prompt 要求 Agent 先产生真实的 payload、证据或台账变化，再重试原 gate。只有 reviewer 明确标记为基础设施瞬态失败时，才允许对未变 fingerprint 做一次原样重试。外部运行监控只负责在 provider/contract 已不可恢复时保留失败证据，不参与问题发现或命题修订。

成功没有 partial 分支。`issues_found` 与 `reviewer_accepted_zero_issue` 都必须同时满足：

- Controller 生成的主要行为 Segment/Requirement worklist 闭合，并报告 `covered / total / ratio`；
- 所有被选作 assertion evidence 的 SourceFact 被直接审计，完整 inventory 中没有明显遗漏会推翻主要结论；
- 所有 latest required assertions terminal；
- 无 incomplete Root；
- 两个 reviewer 均审查合同要求的完整 ID 集，且没有影响主要结论的阻塞 finding；
- 当前 fingerprint 的 `review_discovery_coverage.passed=true`。

这里的 worklist ratio 只描述本次运行内部的过程覆盖。论文实验中的问题发现覆盖率/召回率必须在运行后使用不暴露给 Agent 的人工标注或 reference issue 集计算，并与误报一同报告；不得把 worklist 的 `100%` 写成全语义、全性质或全路径覆盖。

## 8. 真实运行

### 8.0 当前正确的 legacy 入口（本节为更名后补正）

根 `Makefile` 已把无前缀的 `discover*` 目标让给 [../../../pipeline/feedback_loop/](../../../pipeline/feedback_loop/)。要跑**本目录**必须用 `legacy-` 前缀：

```bash
source .env
source venv/bin/activate

make legacy-discover-demo                                        # = legacy-discover-custom，走 identity fixture
make legacy-discover-pair DISCOVER_PAIR=llms_emp_feedback_final_0029
make legacy-discover-test                                        # 266 个测试
make legacy-discover DISCOVER_ARGS="--help"                      # 裸转发
```

`legacy-discover-demo` 的输入变量也带前缀：`LEGACY_DISCOVER_CASE`、`LEGACY_DISCOVER_NL`、`LEGACY_DISCOVER_FCSTM`、`LEGACY_DISCOVER_RAW_SOURCE`、`LEGACY_DISCOVER_SOURCE_TRACE`，默认指向 [`fixtures/discover_integrated/0000_hldcs_manual_identity/`](./fixtures/discover_integrated/0000_hldcs_manual_identity/)。`DISCOVER_PROFILE`、`DISCOVER_LANGUAGE`、`DISCOVER_RENDERER`、`DISCOVER_OUT`、`DISCOVER_ARGS` 两侧共用。等价直调：

```bash
PYTHONPATH=.../pipeline/agent_loop/src:project_1_llm_state_machine_modeling:$PWD \
python -m paper_stm_repair_loop.discover --help
```

### 8.1 原文（命令前缀已过期，语义仍有效）

真实 LLM 前先加载环境变量：

```bash
source .env
source venv/bin/activate
make legacy-discover-demo
```

Demo 只有真实 provider 模式，并使用与 `utils.agent.demo` 相同的 Rich 交互输出。直接运行：

```bash
make legacy-discover-demo \
  DISCOVER_PROFILE=gpt-5.5 \
  DISCOVER_OUT=runs/paper1/discover/manual-0000
```

`legacy-discover-demo` 使用隔离在 `fixtures/discover_integrated/0000_hldcs_manual_identity/` 下的人工 FCSTM identity 工程样例，不占用正式 60 例 [../../../selected_seed_examples/](../../../selected_seed_examples/)。需要运行正式 pair 时使用 `make legacy-discover-pair DISCOVER_PAIR=llms_emp_feedback_final_NNNN`。

`--profile` 是本次运行唯一的模型选择入口。Discover 主 Agent、语义覆盖 reviewer 和对抗性漏报 reviewer 必须使用同一个 profile；两个 reviewer 只分离角色、system prompt、上下文和审计目录，不允许切换到其他模型。

自定义 identity 输入：

```bash
make legacy-discover-custom \
  LEGACY_DISCOVER_CASE=custom-case \
  LEGACY_DISCOVER_NL=/path/to/nl.txt \
  LEGACY_DISCOVER_FCSTM=/path/to/model.fcstm \
  DISCOVER_OUT=runs/paper1/discover/custom-case
```

若 raw/source 与 FCSTM 不同，必须同时提供 `LEGACY_DISCOVER_RAW_SOURCE` 和 `LEGACY_DISCOVER_SOURCE_TRACE`，不能猜测映射。

默认不设置主 Agent 或 reviewer 预算。受限 smoke 可通过 CLI 传入：

```text
--max-model-calls
--max-tool-calls
--max-turns
--max-seconds
--review-max-model-calls
--review-max-turns
--review-max-seconds
--fbmcq-process-wall-seconds
--fbmcq-solver-timeout-ms
--fbmcq-max-bound
```

所有显式限制必须为正数，秒数必须有限。主 Agent、两个 reviewer 的精确 profile 和预算写入 manifest；FBMCQ 的 process wall time、solver timeout 与 max bound 也只在 CLI 显式给出时生效并记录。默认正式运行不设隐藏资源限制，不允许把临时 smoke 限额静默当成正式实验条件。

## 9. 输出与证据链

```text
outdir/
├── manifest.json
├── capability_manifest.json
├── inputs/
├── contexts/discover-attempt-001/
├── agent_audit/discover/
│   ├── audit.jsonl
│   ├── result.json
│   └── coverage_reviews/
│       ├── review-001-semantic_coverage/
│       └── review-002-adversarial_falsification/
├── records/L000-<sequence>-<record-type>/record.json
└── loops/discover.md
```

`records/` 是方法事实源，每笔记录按 sequence 和 hash chain 追加，写后不改。Agent audit 保留主 Agent 和内部 reviewer 各自的逐 turn/model/structured-output 证据；内部 reviewer 使用隔离 callback context，不得污染主 Agent 的 turn、tool lifecycle 或 model-call 计数。`loops/discover.md` 由确定性 Python renderer 从 records 生成，支持 `zh-CN/en-US`，LLM 不直接写报告结构。

失败 run 可以保留用于审计，但不得进入正式结果。正式实验必须使用 clean tracked commit，记录 pyfcstm gitlink、模型精确 ID、provider、调用日期、prompt、raw output、usage/缺失说明、错误、重试、redaction 与 eligibility。

## 10. 验证

```bash
make legacy-discover-test        # 266 个测试；`make discover-test` 现在跑的是 feedback_loop

source venv/bin/activate
ruff check \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/src/paper_stm_repair_loop \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/tests
```

Development fixtures 和 evaluator gold 只用于测试/验收，不进入 Agent 或 reviewer context。它们证明已声明能力上的回归，不允许被写进 prompt、coverage rows、plan gate 或运行结果。

真实 provider 的 S1-S4 证据选择 smoke 是显式 opt-in，不进入默认 pytest：

```bash
source .env
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/tests/helpers/probe_discover_evidence_choice.py \
  --run-real \
  --profile gpt-5.5 \
  --profile claude-opus-4-7 \
  --out runs/paper1/discover/evidence-choice-<git-head>.jsonl
```

该 helper 为 S1-S4 分别启动独立 `AgentApp.run`，输出精确 profile/model/adapter、prompt hash、实际工具调用、structured decision、usage/cache、限制、rubric 结果，并区分 provider/transport 基础设施失败和语义选择失败。默认 smoke 限制固定为 Issue #165 的 `4 model calls / 3 tool calls / 4 turns / 180s`，只约束该小型 smoke，不改变正式 Discover 默认无隐藏资源限制的合同。

PR #162 的 60 例 FCSTM 资产可用以下 helper 做显式 opt-in FBMCQ 性能探测；`--limit` 存在时只是小型 smoke，省略时才执行严格的 60/60 ID 集合 preflight 和全量 probe：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/src:project_1_llm_state_machine_modeling:$PWD \
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/tests/helpers/probe_discover_fbmcq.py \
  --fcstm-dir project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60/fcstm \
  --bounds 5,20,50 \
  --output runs/paper1/discover/fbmcq-probe-<git-head>.jsonl
```

正式全量模式还会 fail closed 检查：输入必须是唯一的 `feedback_final_pairs.jsonl` 与 `llms_emp_r45_java_60/fcstm/`；PR #162 资产提交 `ef73e4bf` 和 report `manifest.json.research_commit` 都必须是当前 HEAD 的祖先。路径、lineage、数量、ID 集合或 provenance 任一不符均返回 `input_asset_preflight_failed`，不会搜索或降级到其他旧资产。

两类 helper 都使用排他创建，拒绝覆盖已有输出；`runs/` 只保留本地审计证据，不提交。
