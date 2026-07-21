# Paper1 Discover Agent

本目录实现 paper1 的 `B-discover`：给定 A 阶段已经准备并冻结的
`<NL, raw/source STM_0, fcstm STM_0>`，在 FCSTM 中间语义层上完整探索行为义务，
发现 source-level 行为问题，并把问题、通过项、执行证据和覆盖审查写入不可变运行记录。

Discover 只读，不修改 `STM_0`，不执行 Repair、Confirm，也不在运行中回到 PlantUML
或其他 source 表示层。raw/source 与 source trace 仅用于 grounding 和归因。paper1 的
核心贡献仍是 feedback-driven loop 以及 simulation / bounded formal verification 的
可执行反馈集成；FCSTM、Controller、records 和审查工具是方法基础设施，不单独作为
headline contribution。

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

`review_discovery_coverage` 是 Discover Agent 可调用的同级业务工具，不是第二个顶层
orchestrator。该工具内部运行两个无工具、无 gold、无模型修改权限的独立 LLM reviewer。
它们只审查当前冻结输入和完整台账，并把结构化意见返回主 Agent。任一 reviewer 未通过，
主 Agent 都必须在同一个 Discover run 内继续工作。

## 2. Controller 与 Agent 边界

Controller 只建立 issue-agnostic 的确定性骨架：

1. 校验 fresh run、输入角色、hash、pyfcstm 版本和 submodule commit。
2. 使用 pyfcstm public API 完成 parse、semantic、inspect 和基础运行能力检查。
3. 机械切分 NL 为稳定 `InputSegment`。
4. 为每个非 meta clause 建立基础 behavior row，并为实际出现的结构、数量、条件、
   effect、顺序、持续性、完成、时序等 cue 建立 `CoverageRequirement`。
5. 从 structured inspect 和 source trace 生成完整 `SourceFact` inventory。
6. 装配只绑定当前冻结任务的工具和 append-only records。
7. 对 plan、断言执行、归因、审查指纹和最终提交做失败关闭式校验。

Controller 不做以下工作：

- 不预设 D01-D12 或其他问题 taxonomy。
- 不预测哪个位置存在问题。
- 不生成 gold issue、gold assertion 或 expected verdict。
- 不把 conversion/lowering 差异自动判为 source-level issue。
- 不用正集 inventory 冒充“缺失元素已经被发现”。

Discover Agent 负责解释 NL 语义、识别独立可修复义务、选择证据路线并形成正向命题。
`True` 始终表示模型满足该 Root，`False` 表示模型与该 Root 矛盾。禁止通过双重否定、
expected-failure 元数据或常量表达式把期望答案写入断言。

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

断言可以修订，但 Unit、Root、basis、required 状态和 evidence scope 不得被弱化。每次
修订创建新版本，旧版本和旧执行记录保留。所有 latest required assertions 都必须得到
有模型证据的 terminal bool；异常、unsupported、non-bool、超时或证据族不满足均为
`inconclusive`，不能自动当作问题。

注册失败不仅返回 error code，还返回 `required_actions`。对未直接验证的 SourceFact，
反馈包含完整事实快照、兼容 evidence family、可接受谓词示例、推荐工具、具体动作和通过
判据。这样严格门禁不会退化为要求 Agent 猜测内部 AST 规则。

## 4. 十项 Agent 工具

| 工具 | 状态 | 作用 |
|---|---|---|
| `read_fcstm_guide` | 必用 | 第一次业务调用；读取 `pyfcstm.llm` FCSTM guide、版本与 SHA。 |
| `read_task` | 必用 | guide 后读取完整冻结任务；重复调用只返回稳定身份信息。 |
| `read_fbmcq_guide` | 条件必用 | 首次撰写或注册 `fbmcq(...)` 前读取官方指南。 |
| `query_model` | 可用 | 对 states/events/variables/transitions 等 structured inspect 做精确查询。 |
| `observe_trace` | 可用 | 按 FCSTM cycle 语义探索一条明确有限轨迹，不单独形成 Root verdict。 |
| `lookup_source_trace` | 可用 | 查询 source/FCSTM 映射，只支持归因，不决定 NL 是否满足。 |
| `register_coverage_plan` | 必用 | 原子化注册 Units、Roots、bases 和所有 initial assertions。 |
| `eval_assert` | 必用 | 每次只执行一条已注册 latest assertion，并记录真实调用与结果。 |
| `revise_assertion` | 条件使用 | 对 inconclusive 或被审查证明为弱/错向的断言追加新版本。 |
| `review_discovery_coverage` | 必用 | 对当前完整台账执行双独立审查；通过前禁止提交。 |

所有工具都不接受任意文件路径、URL、shell、外部 Python、alternate case、reference/gold、
Repair 或模型修改参数。每个 Agent-facing tool 的注册 docstring 必须自包含说明 Purpose、
When to use、When not to use、Parameters、Returns、Execution、Failure semantics、
Evidence limitations、Permissions 和 Example，并由合同测试读取真实注册 description。

`eval_assert` 的受限环境额外提供开放式 `effect_deltas(source=..., event=...,
target=...)`。它返回当前匹配迁移上全部可解析的 `(variable, delta)`，无变量或无 effect 时
返回空 tuple。对于“某动作使某个计数减少”但当前模型根本没有对应变量的 NL 义务，Agent
可写 `any(delta < 0 for _, delta in effect_deltas(...))`，从而让缺失行为稳定得到 `False`，
而不需要虚构 `dummy`、`sentinel` 或不存在的变量名。已知且可追溯的真实变量仍可使用
`effect_delta(..., variable=...)`。

注册门禁同时拒绝两类已经在真实运行中观察到的 coverage gaming：

- 用不存在的哨兵变量调用 `effect_delta`，再把 `None` 当作“已检查完整 effect”的证据；
- 先按三个已知名称过滤状态，再用 `len(...) == 3` 冒充对“包含三个区域”的完整基数检查。

基数断言必须比较一个完整、稳定、由模型定义的范围，例如
`len(states(parent='Root.Searching', recursive=False)) == 3`；不能用候选名枚举、成员过滤或
字面量列表把结果凑成目标数，也不能通过 `or` 附加一个会独立返回 `True` 的旁路。数量对象
必须与 NL 一致：areas/modes/regions 计 `states`，events 计 `events`，variables/counters
计 `variables`，明确的 transitions 才计 `transitions`；不能用 plan-derived
`bound_model_refs` 或无关 inventory 代替。areas/modes/regions 等层级数量还要求
`states(parent=..., recursive=False)` 的 parent 与同一 Root 的 `state:<parent>` model ref
精确一致；共享前缀的嵌套无关容器不能通过。

方向 effect 断言同样必须直接决定顶层布尔值。`effect_delta.variable` 只能是冻结模型中真实
存在的单一字符串字面量，不能在表达式中拼接或动态选择；开放式 `effect_deltas` 只能使用
无过滤 generator，并必须用 literal source、event（或显式 `None`）和 target 绑定一条确定
迁移，不能先挑中一个有利变量或搜索全模型无关 effect，再声称已经检查当前义务。

## 5. 独立覆盖审查

`review_discovery_coverage` 只允许在完整 plan 已注册，且所有 latest required assertions
均为 terminal 后调用。工具向两个隔离 reviewer 提供：

- 完整 NL、FCSTM、raw source、source trace 和 normalized inspect；
- 全部 Segment、Requirement 和 behavior SourceFact；
- Units、Roots、latest assertions、真实执行记录；
- 审查前 Controller projection；
- 当前台账 fingerprint 与必须逐项审查的 ID 集合。

两个 reviewer 分工：

1. `semantic_coverage`：逐条核对 NL 对象、触发、源/目标、数量、方向、顺序、持续性、
   完成范围和时限是否被同强度正向命题覆盖。
2. `adversarial_falsification`：主动构造可能让当前断言错误通过的路径、guard、effect、
   hierarchy、initialization、timing、issue projection 等反例。

每个 reviewer 必须显式枚举全部 required Segment、Requirement、Root，以及当前计划选作
断言证据的 SourceFact ID；完整 SourceFact inventory 仍提供给 reviewer 用于攻击会推翻主要
结论的明显漏项，但不机械要求逐事实断言。Controller 对 required ID 集合做精确相等校验。
failed finding 还必须至少关联一个当前真实台账 ID；
虚构 ID、泛泛评论或无关联建议均失败关闭。

每条失败意见同时包含：

```text
problem
missed_behavior_risk
related_*_ids
coverage_dimensions
recommended_tools
recommended_steps
recommended_action
pass_criteria
```

因此 review 不是只给裁决。它必须告诉主 Agent 漏掉了什么、为什么影响召回或误报、应调用
哪些现有工具、如何补强断言，以及什么条件下才可复审通过。程序化 ID mismatch 和过早调用
review 也会生成确定性 `required_actions`。

`coverage_dimensions` 明确指出建议将增加或重查哪一类覆盖，例如 `nl_semantics`、
`model_behavior`、`source_trace_grounding`、`assertion_strength`、
`issue_projection_evidence` 或 `anti_gaming`。`recommended_action` 不能只写“继续检查”或
“提高覆盖率”，必须说明要检查的具体行为、路径、条件或 evidence dimension；
`pass_criteria` 必须给出下一次 review 可观察、可判定的闭合条件。建议只能使用当前 Discover
已有工具，不能要求 Agent 直接改 Controller projection，也不能用 FBMCQ 解释 NL，或把 NL
加强成原文没有的 `only`、every-state、future-model 义务。为避免“建议继续检查”这类无法
执行的口号，`recommended_action` 必须逐字点名至少一个 `recommended_tools` 中的工具，
以及至少一个 `related_*_ids` 中的当前台账 ID，
`recommended_steps` 必须为每个推荐工具分别写出关联 ID、检查目标、参数/模型范围和预期证据，
其中 `suggested_arguments` 按工具合同至少给出 `query_kind`、`cycles`、`element_refs`、
`assertion_chain_id/assert` 或完整 `plan` 等相应键，并复用真实工具 Pydantic 输入合同校验
enum、列表层级、必填字段和额外字段；
`pass_criteria` 必须点明 terminal bool、具体 state/transition/effect/trace/ID 闭合等可观察
结果。全称量词是否越界由持有冻结 NL 的 gate 判断；原文明确写了 `all states` 时不会被关键词
门禁误拒。

审查通过绑定 `reviewed_state_fingerprint`。任何后续 `eval_assert` 或 assertion revision
都会改变 fingerprint，使旧 pass 立即失效；必须重新执行双审查。

如果 reviewer provider、stream 或结构化输出链路临时失败，工具返回
`execution_status=retryable_reviewer_failure` 和 `passed=false`，保留当前台账并写入
append-only record。主 Agent 必须在不改动当前 fingerprint 的情况下重试；基础设施失败
既不能被视为覆盖通过，也不能被伪装成某个 source-level issue。

只有 provider/transport 类临时故障允许上述重试；schema-invalid verdict、错误 review kind
等确定性合同故障返回 `execution_status=reviewer_contract_failure`，保留同轮已完成 reviewer
verdict 和失败审计，并终止当前 Discover attempt。它们不能通过反复调用同一工具被掩盖。

## 6. Issue 投影与归因

全部 latest assertions 执行且双审查通过后，Controller 投影：

- `issue_root_projection`：正向 Root 被证据反驳，且 source attribution 足以支撑问题归因。
- `regression_guard_projection`：正向 Root 已满足，后续 Repair 必须保持。
- `incomplete_root_projection`：仍有非 terminal 断言；此时禁止成功提交。

非 identity 输入只有在冻结 source trace 提供精确一对一映射时，contradiction 才能发布为
`confirmed` 并进入 Repair。ambiguous/untraceable conversion attribution 必须保持
`candidate_only` 和 `downstream_repair_allowed=false`。raw/source 与 FCSTM 文本完全相同
且 `relation_policy=exact_identity` 时，Controller 使用同一结构事实建立可审计 identity
归因；这只消除 conversion 歧义，不提供 gold verdict。

## 7. 一次运行的强制顺序

System prompt 要求同一个 Discover run 完成：

1. `read_fcstm_guide -> read_task`。
2. 对每个主要 NL clause/cue 找到模型实现，并使用完整 SourceFact inventory 探索会实质影响这些义务的模型交互；不机械地为每个事实单独建断言。
3. 必要时调用 query/trace/source-trace；涉及 FBMCQ 时先读 guide。
4. 注册完整计划；被拒后必须按 `required_actions` 修正完整计划，不能删除困难义务。
5. 对每条 latest required assertion 分别调用 `eval_assert`。
6. 对 inconclusive 或审查指出的弱命题调用 `revise_assertion`，再执行新版本。
7. 调用 `review_discovery_coverage`；一次 failed review 返回多条行动时，先完成该轮全部
   `required_actions/recommended_steps` 及其 pass criteria，再重复审查，直至当前 fingerprint pass。
8. 核对 attribution 和最终 projection。
9. 仅提交一次与 Controller projection 一致的 `submit_discovery`。

业务工具的拒绝与失败由本次 Agent 自行消化，不再由外部 controller 猜测下一项语义动作。
每个非完成返回都必须提供错误对象、`required_actions`、建议工具、具体修正动作和可观察的
pass criteria；system prompt 要求 Agent 先产生真实的 payload、证据或台账变化，再重试原 gate。
只有 reviewer 明确标记为基础设施瞬态失败时，才允许对未变 fingerprint 做一次原样重试。
外部运行监控只负责在 provider/contract 已不可恢复时保留失败证据，不参与问题发现或命题修订。

成功没有 partial 分支。`issues_found` 与 `reviewer_accepted_zero_issue` 都必须同时满足：

- Controller 生成的主要行为 Segment/Requirement worklist 闭合，并报告 `covered / total / ratio`；
- 所有被选作 assertion evidence 的 SourceFact 被直接审计，完整 inventory 中没有明显遗漏会推翻主要结论；
- 所有 latest required assertions terminal；
- 无 incomplete Root；
- 两个 reviewer 均审查合同要求的完整 ID 集，且没有影响主要结论的阻塞 finding；
- 当前 fingerprint 的 `review_discovery_coverage.passed=true`。

这里的 worklist ratio 只描述本次运行内部的过程覆盖。论文实验中的问题发现覆盖率/召回率必须在运行后使用不暴露给 Agent 的人工标注或 reference issue 集计算，并与误报一同报告；不得把 worklist 的 `100%` 写成全语义、全性质或全路径覆盖。

## 8. 真实运行

真实 LLM 前先加载环境变量：

```bash
source .env
source venv/bin/activate
make discover-demo
```

Demo 只有真实 provider 模式，并使用与 `utils.agent.demo` 相同的 Rich 交互输出。直接运行：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src:project_1_llm_state_machine_modeling:$PWD \
python -m paper_stm_repair_loop.discover \
  --pair-id llms_emp_stm_results_0000_manual_identity \
  --profile gpt-5.5 \
  --coverage-review-profile claude-opus-4-7 \
  --falsification-review-profile deepseek-v4-pro \
  --content-language zh-CN \
  --renderer rich \
  --output-dir runs/paper1/discover/manual-0000
```

自定义 identity 输入：

```bash
make discover-custom \
  DISCOVER_CASE=custom-case \
  DISCOVER_NL=/path/to/nl.txt \
  DISCOVER_FCSTM=/path/to/model.fcstm \
  DISCOVER_OUT=runs/paper1/discover/custom-case
```

若 raw/source 与 FCSTM 不同，必须同时提供 `DISCOVER_RAW_SOURCE` 和
`DISCOVER_SOURCE_TRACE`，不能猜测映射。

默认不设置主 Agent 或 reviewer 预算。受限 smoke 可通过 CLI 传入：

```text
--max-model-calls
--max-tool-calls
--max-turns
--max-seconds
--review-max-model-calls
--review-max-turns
--review-max-seconds
```

所有显式限制必须为正数，秒数必须有限。主 Agent、两个 reviewer 的精确 profile 和预算
写入 manifest；不允许把临时 smoke 限额静默当成正式实验条件。

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

`records/` 是方法事实源，每笔记录按 sequence 和 hash chain 追加，写后不改。Agent audit
保留主 Agent 和内部 reviewer 各自的逐 turn/model/structured-output 证据；内部 reviewer
使用隔离 callback context，不得污染主 Agent 的 turn、tool lifecycle 或 model-call 计数。
`loops/discover.md`
由确定性 Python renderer 从 records 生成，支持 `zh-CN/en-US`，LLM 不直接写报告结构。

失败 run 可以保留用于审计，但不得进入正式结果。正式实验必须使用 clean tracked commit，
记录 pyfcstm gitlink、模型精确 ID、provider、调用日期、prompt、raw output、usage/缺失说明、
错误、重试、redaction 与 eligibility。

## 10. 验证

```bash
make discover-test

source venv/bin/activate
ruff check \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src/paper_stm_repair_loop \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/tests
```

Development fixtures 和 evaluator gold 只用于测试/验收，不进入 Agent 或 reviewer context。
它们证明已声明能力上的回归，不允许被写进 prompt、coverage rows、plan gate 或运行结果。
