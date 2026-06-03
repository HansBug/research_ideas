# PR-E2 e2e ref-model skill 使用指南

本文件用于 PR-E2：让 Codex / Claude Code 类 agent 在**不调用顶层 agent-loop runtime** 的前提下，基于 repo-local skill / toolbox 自主完成“NL + 论文子路径 -> FCSTM/pyfcstm ref model 候选”的 e2e 建模、验证、修复和留痕。

## 1. 硬性边界

1. **禁止调用顶层 agent-loop runtime**：不得调用 `method.loop.run_agent_loop(...)`、PR-D representative runner 或任何一键 full staged runner。
2. **允许调用底层工具箱**：可以调用 `SD-*` deterministic tools、`SL-*` prompt generators、pyfcstm parse/build/inspect/sim utilities，以及仓库内只读论文材料。
3. **修改范围**：若需要改 skill，本 PR 默认只允许改 `project_1_llm_state_machine_modeling/method/agent_loop_skill/` 及其子路径。若发现来自上游语法 prompt / grammar digest 的硬伤会直接误导 skill 使用者（例如实际 parser 不支持却在 grammar 中要求的语法），可作为特例修改 `project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md`；此类改动必须先核对相邻 PR（尤其 PR-E1）已有 diff，尽量采用相同修正以避免 merge 后冲突。
4. **质量优先**：允许 Codex / Claude Code 长时间运行。时间限制只用于防止死锁或 CLI 挂死，不应用来牺牲论文阅读、验证或 repair 质量。
5. **证据留痕**：每个样本的输入、读取路径、候选模型、检查反馈、修复轨迹和最终判断都必须能写入 PR comment。
6. **NFRR 必填**：每个样本必须按 [nfrr_evaluation_guide.md](./nfrr_evaluation_guide.md) 给出 NFRR claim、八维 vector、tier、cap reasons、allowed_use 与 `calibration_status=uncalibrated_candidate_gate`。
7. **最低准出**：若样本未达到 `final_tier >= T2`、`SD-2/SD-3 pass`、无 unwaived `SD-4` blocking、至少一个 `counted_for_main_BVS=true` 的 obligation-anchored `SD-6` scenario pass、无 critical contradiction / reachable test-harness pollution，只能称为 diagnostic evidence，不能称为 ref-model candidate。hot-start/debug scenario 不能用于满足最低准出。
8. **Ground-Truth candidate 目标**：若声称“Ground Truth 级别 ref model 蓝本”，应达到 `final_tier >= T3`、`FE=3`、`REC=3`、`BVS=3`、`evidence_mode in {NL+paper, authoritative_NL}`、`obligation_independence in {independent_adjudicated, model_blind_independent}`；未人工签核前必须写 `signed_reference=false`。

## 2. 推荐输入格式

每个 e2e 样本至少提供：

```text
Path 类别: Path-1 或 Path-2
样本编号: P1-01 / P1-02 / P2-01 / P2-02 ...
NL 片段: 可来自 eval/data/sources/<case>/nl.md 或 sources/<case>/STM.md / DESC.md 中整理出的需求片段
论文子路径: project_1_llm_state_machine_modeling/sources/<case>/
目标: 产出 FCSTM/pyfcstm ref model 候选，并记录验证/修复轨迹
禁止: 不得调用 method.loop.run_agent_loop 或一键 runner
```

论文子路径通常应包含：

```text
paper.pdf
paper_content.txt
bibtex.bib
DESC.md
STM.md
```

优先阅读顺序：

```text
bibtex.bib -> STM.md / DESC.md -> paper_content.txt -> paper.pdf（必要时核对）
```

`STM.md` / `DESC.md` 可以作为人工整理过的索引，但不能替代论文证据。每个正式样本默认应至少抽读 `paper_content.txt` 中与状态机、状态表、流程图、控制算法、结果解释直接相关的章节；如果没有回看 `paper_content.txt`，必须在 PR comment 中明确说明原因，并把该样本标为 grounding 风险，reviewer 可按影响评为 I。

## 3. 推荐 e2e 流程

### E0. Skill discovery

读取：

```text
project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/nfrr_evaluation_guide.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/stages/
```

输出记录：列出实际读取的 skill 文件。`SKILL.md` / `CLAUDE.md` 当前是指向 `AGENT_LOOP_SKILL.md` 的软链接；如果 agent 环境无法跟随 symlink，应直接读取 `AGENT_LOOP_SKILL.md`，并在 PR comment 中说明这是入口解析差异而不是 skill 缺失。

### E1. Evidence grounding

从 NL 与论文材料抽取：

- 控制对象与边界；
- 状态 / 阶段 / 模式；
- 输入事件或传感信号；
- 输出动作；
- guard / 阈值 / 定时；
- 异常、复位、回退或非法状态；
- 原文证据位置或整理文件位置；
- 合成变量 / 合成状态 / 离散化抽象：例如把“门关闭后运行”抽象成 `door_closed`，或把连续控制量离散成 `0/1/2/3` 档位。

输出记录：一张简短 grounding 表，说明每个状态/转移来自哪里；凡不是论文直接命名、而是为了可观测性或仿真引入的变量/状态，都必须标为 `synthetic abstraction`，并说明它不应被下游误当成 paper-defined ground truth。

### E2. Initial candidate modeling

可以使用 `SL-1` prompt generator 作为提示蓝本，也可以由 agent 自行建模，但必须遵守 pyfcstm/FCSTM 语法，并输出候选 DSL。

禁止把论文无关背景、连续控制公式或硬件清单机械塞进状态机；优先保留可验证的离散控制骨架。

### E3. Deterministic checks

正式样本必须至少尝试 `SD-2 -> SD-3 -> SD-4 -> SD-6`。`SD-6` 不是可随意省略的 optional polish：P1/P2 ref model 候选只有在行为 scenario 上跑过仿真，才有足够证据交给下游。若场景尚未充分，只能标记为 `部分可用 / oracle weak`，不能声称 ready。

若某个工具入口不可用，应记录命令、错误摘要和影响分类，不要静默跳过。

当前 pyfcstm parser 注意事项：

- 变量类型以实际 parser 为准；当前已验证支持 `def int` / `def float`，不支持 `def bool`、`true`、`false`。布尔量请用 `int` flag（如 `0/1`）表达，并在注释中说明语义。
- `// @external` / `// @input` 注释可作为人工/下游静态验证的语义标记，但当前 `run_sd4_design(..., policy_profile="generated_candidate")` 不消费该注释；因此它不能自动消除 `W_UNWRITTEN_READ_VAR` / `W_GUARD_VARS_NEVER_CHANGE`。
- 外部传感输入优先用显式事件更新、环境采样 aspect、或 `int/float` 变量 + 清晰 PR comment 说明来建模；不要用无意义 self-assignment 只为消警。

```python
from method.schema import StageContext, TestScenario, ScenarioSet
from method.stages.sd_tools import (
    freeze_scenario_set,
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,
)

context = StageContext(nl=nl, current_dsl=current_dsl)
parse_feedback, parse_meta = run_sd2_parse(current_dsl, context)
if parse_feedback.ok:
    semantic_feedback, semantic_meta, build = run_sd3_semantic(current_dsl, context)
if semantic_feedback.ok:
    design_feedback, design_meta = run_sd4_design(context, policy_profile="generated_candidate")
```

如需构造最小 scenario，可使用：

```python
import hashlib

scenario = TestScenario(
    name="diagnostic_hot_start_sanity",
    description="diagnostic_hot_start sanity; do not count this as main BVS evidence",
    initial_vars={"some_flag": 0},  # hot-start 时显式给出所需变量初值；不要依赖隐式环境
    steps=[],
)
coverage, coverage_meta = run_sd5a_scenario_coverage(current_dsl, [scenario])
scenario_set, freeze_meta = freeze_scenario_set(
    [scenario],
    source_dsl_hash="sha256:" + hashlib.sha256(current_dsl.encode("utf-8")).hexdigest(),
    source_inspect_hash="sha256:" + hashlib.sha256(repr(context.inspect_json or {}).encode("utf-8")).hexdigest(),
    source_grounding_hash="sha256:" + hashlib.sha256(repr(context.grounding_map).encode("utf-8")).hexdigest(),
    coverage_report=coverage,
)
sim_feedback, sim_meta = run_sd6_sim(current_dsl, scenario_set, context)
```

上述示例只展示 SD-6 API 的最小调用方式。它是 `diagnostic_hot_start`，只能用于 debug / sanity，不得计入 NFRR 的主 BVS 证据。若要计入主 BVS，scenario 必须在 NFRR ledger 中标为以下三类之一：

1. `default_prefix`：从默认初态出发；
2. `reachable_prefix`：从默认初态显式执行事件 / guard 前缀到达目标状态，并在 comment 中列出前缀；若当前 SD-6 runtime 只能用 `initial_state` 近似执行，需要额外写 `runtime_execution_mode=runtime_hotstart_surrogate` 与状态快照理由；
3. `external_input_initial_vars`：只注入论文 / NL 明确给出的外部输入变量，并配套 external-input ledger。

不要把 synthetic observability variables、output-only variables 或为了 scenario 方便而写的 test profile 标成 `external_input_initial_vars`。

### E4. Repair loop

若 parse / semantic / design / sim / review 任一失败：

1. 选择最早 blocking feedback；
2. 用 `SD-8 FixPlan` 产出结构化修复计划；
3. 使用 `SL-9` prompt generator 或 agent 自行修复；
4. 用 `SD-10 RepairReview` 或等价本地检查确认未引入漂移；
5. 回到 E3 重新从 parse 开始检查。

注意：`suggested_fix` 只是规则诊断的参考 hint，不是必须照抄的编辑命令。agent 可以基于 NL 与全局约束提出更合理的修复方案。

`SD-10 RepairReview` 的结果必须分级处理：

- `regression_detected=true` 或 candidate parse/semantic fail：必须继续修复，不能 waiver。
- 新增 blocking design diagnostic：必须修复，除非能明确证明是工具 policy 与论文外部输入之间的已知不匹配，并在 comment 中给出 external-input waiver。
- `count_drift` / `forced_transition_count_drift` / `missing_required_grounding`：不能简单忽略。若它来自必要的结构性修复（例如为 nested region 增加 root-level release state，或 `GroundingMap` 使用聚合 ref 而当前 SD-10 只支持精确元素 ref），必须给出逐项 waiver：旧模型缺陷、修复为何必要、论文证据、frozen scenario regression 结果，以及为什么不会改变 NL 语义。
- 如果只需要最终 acceptance gate，可对最终 DSL 做一次 no-op `SD-10`（`old_dsl == candidate_dsl`）作为“残余回归检查”，但这不能替代对真实 repair delta 的 waiver / 解释。

因此，PR comment 中应区分：`SD-10 pass`、`SD-10 conservative fail + explicit waiver`、`SD-10 fail unresolved`。只有前两者可以作为 ref-model 候选交接；第三种应标为 not ready。

### E5. Optional lightweight review

可以使用 `SL-7` / `SL-10B` prompt generator 组织外部 LLM 评审，但必须记录：

- 输入摘要；
- provider / CLI；
- 输出 decision / findings；
- 是否 blocking；
- 对模型质量的影响。

### E6. NFRR evaluation and exit gate

完成最终候选模型后，必须读取 [nfrr_evaluation_guide.md](./nfrr_evaluation_guide.md)，基于 `NL + final FCSTM model`（可选 `paper_dir`）生成 NFRR report。NFRR report 不得只写“高/中/低质量”，必须包含：

- `claim`：`evidence_mode`、`scope_type`、`obligation_independence`、`allowed_use_rule_id`、`allowed_use`、`signed_reference`、`calibration_status`；
- NL coverage ledger 与 obligation ledger；
- obligation-to-model alignment；
- `SD-2/SD-3/SD-4` 检查摘要；
- obligation-anchored scenario 与 `SD-6` 结果；
- mutation / DMR 证据或 explicit limitation；
- waiver ledger；
- `FE/NGF/REC/GAS/SCB/AAT/BVS/DMR` 八维分数；
- `tier_before_cap`、`cap_reasons`、`final_tier`。

#### Scenario provenance integrity audit

在给出 `BVS` 分数前，必须先做 scenario provenance 真实性自检。每条 scenario 至少记录：

| 字段 | 含义 |
|---|---|
| `scenario_id` | 场景编号 |
| `covered_obligation_ids` | 覆盖的 obligation |
| `oracle_source` | NL span / paper span / human assumption；不得来自当前模型运行结果 |
| `provenance` | `default_prefix` / `reachable_prefix` / `external_input_initial_vars` / `diagnostic_hot_start` / `model_derived_oracle` |
| `prefix_generation` | `default` / `manual_from_NL` / `bfs_depth_K` / `heuristic` / `none` |
| `reachable_prefix_witness` | 若 `initial_state` 非空且要计入主 BVS，必须列出从默认初态到该状态的事件/guard 前缀 |
| `runtime_execution_mode` | `executed_prefix` / `runtime_hotstart_surrogate` / `default_runtime`；若是 surrogate 必须说明 runtime 限制 |
| `state_snapshot_justification` | surrogate 初始化内部/output-only 变量时，说明这些值来自 state entry/invariant 或 prefix actions，不是外部输入 |
| `initial_state` | 若非空，说明为什么不是 diagnostic hot-start |
| `external_input_ledger_ref` | 仅 `external_input_initial_vars` 必填 |
| `counted_for_main_BVS` | 是否计入主 BVS |
| `sd6_result` | pass / fail / not_run |

反例与处理：

1. **synthetic observability var 错标 external input**：如 `current_floor`、`direction`、`hbrg` 这类由模型输出或仅为观测引入的变量，不能作为 `external_input_initial_vars` 的依据。若从中间楼层 hot-start，只能标 `diagnostic_hot_start`，除非给出从默认初态到该楼层的 reachable prefix。
2. **中间状态 hot-start 覆盖主链**：直接 `initial_state=SomeMiddleState` 且无前缀，只能 debug；不能把它算进 BVS 主证据。若因 SD-6 缺少 step-level 变量刷新 / timer fast-forward 而必须 surrogate 执行，需要列出 reachable prefix、外部输入 ledger 和 state snapshot justification。
3. **model-derived oracle**：若 expected state / vars 是跑当前模型后反推出来的，不得计入主 BVS。
4. **scope retro-shrink**：不能先看模型覆盖了什么，再把难覆盖的 NL span 标为 out-of-scope；所有 NL spans 必须先分类。
5. **hot-start dominance**：若 critical/major scenario obligations 的主证据主要依赖 `diagnostic_hot_start`，应降低 BVS 与 final tier，而不是用 scenario pass-rate 刷分。

PR-E2 最低准出：`final_tier >= T2`，且不得存在 critical contradiction、reachable test-harness pollution、unwaived `SD-4` blocking、缺失 NL/obligation/scenario provenance ledger、或 `SD-6` 全失败。最低准出所依赖的 scenario 必须 `counted_for_main_BVS=true`；`diagnostic_hot_start` / `model_derived_oracle` 不能满足最低准出。若目标是“Ground Truth 级别 ref model 蓝本”，应达到 `final_tier >= T3`，但没有人工/专家签核时仍必须写 `signed_reference=false`。

### E7. Final evidence package

每次 skill 修改并 push 后，必须重新跑一轮 4 个样本（Path-1 至少 2 个、Path-2 至少 2 个），并把每个样本作为独立 PR comment 留痕。PR-E2 不要求完全复制 PR-E1 的 run-record 格式，但每个样本 comment 至少应接近 PR-E1 报告的信息密度，包含：

- 样本编号、Path 类别、NL 来源、论文路径；
- 使用的 agent / CLI / skill 入口；
- 实际读取文件；
- 禁止调用项检查结论；
- 输入 NL 原文；
- 输入 NL 中文翻译 / 中文释义；
- 最终 FCSTM/pyfcstm 候选模型全文；
- 全流程真实摘要表：stage、是否 LLM、轮次、结果、获取的信息/反馈、本阶段做了什么、DSL 修改、artifact/命令；
- deterministic checks / review checks 结果；
- repair 轨迹与每次修复依据；
- NFRR 评价：claim、NL coverage ledger、obligation ledger、scenario provenance ledger、八维 vector、tier、cap reasons、allowed_use、准出结论；
- 作为 ref model 的学术质量评审：覆盖、抽象、未覆盖语义、是否达到 NFRR 最低准出 / Ground-Truth candidate 目标、仍需人工签核的问题；
- 合成变量 / 合成状态 / 离散化抽象声明：列出所有非论文直接定义的变量、状态或事件，并说明其存在理由；
- advisory / warning waiver：尤其是 external input、output-only variable、SD-10 conservative fail 的逐项处理；
- skill 改进建议。

若本轮 skill 修改后 4 个样本没有重跑，不能声称“本轮已 ready”；只能标为局部修复或文档修正。

## 4. 建模习语与边界模板

### 4.1 外部输入变量

控制系统论文常把传感器、环境量或连续控制器输出作为状态机 guard 输入。PR-E2 推荐按以下优先级建模：

1. **事件更新模式**：用事件表达外部输入变化，例如 `BPUpdated`、`RefreshSensors`，并在转移或 aspect 中更新变量。
2. **环境采样 aspect 模式**：对每个控制周期都会刷新的输入，用 root-level aspect 表达采样意图；不要用无意义 self-assignment 伪造内部写入。
3. **人工标记模式**：可在变量声明后写 `// @external` 或 `// @input` 辅助人工审计，但必须说明当前 SD-4 不消费该注释，不能把它当作自动通过依据。

若 SD-4 因外部输入给出 blocking warning，producer 必须在 PR comment 中解释：这是模型错误、工具策略不匹配、还是需要补事件/aspect 的真实问题。

**大表驱动 / 外部连续输入的边界**：能源管理、医疗设备等论文常用状态表或阈值表描述“任意外部输入 -> 状态/动作”。这类 ref model 的最终语义应优先保留真实外部输入变量，例如 `PL`、`Ppv`、`Pw`、`SoC`，由 scenario `initial_vars` 或外部环境层提供取值；不要把 12 个测试 scenario 写成 `sample_case == 1..12` 并在模型本体里硬编码输入 profile。

允许使用 `RefreshInputs` / `SampleInputs` 事件表达“环境刷新已发生”，也允许在 scenario 中用 hot-start / initial_vars 直接设置外部输入；但如果引入 `sample_case`，它必须被明确标为 **test harness / scenario driver**，不得冒充论文定义的控制变量，也不得作为最终 ref model 的主语义。若为了通过当前 `generated_candidate` SD-4 policy 而不得不使用 external-input waiver，应记录：

- 哪些变量是外部输入；
- 为什么没有内部 transition 写入它们；
- `SD-4` 的 `W_UNWRITTEN_READ_VAR` / `W_GUARD_VARS_NEVER_CHANGE` 是否属于工具 policy 与外部输入语义不匹配；
- `SD-6` 是否用多个 `initial_vars` scenario 覆盖关键 nominal / abnormal / edge 分支。

**输出变量 advisory**：执行器输出、报警 flag、日志计数、显示码等变量经常只在 effects/enter 中写入、由 scenario 观测，而不参与 guard。这类 `W_UNREFERENCED_VAR` / `W_WRITE_ONLY_VAR` 通常是可接受 advisory；不要为了消警把 output-only 变量伪造进 guard。

### 4.2 事件作用域与初始 cycle

复杂/层次模型中，局部事件、forced transition 与初始 transition 很容易造成“看起来能 parse，但 scenario 不触发”的假阳性。PR-E2 producer 必须遵守：

- 在 scenario 中注入事件时，说明它是 root event 还是 nested/local event；必要时参考 `stages/SD-6.md` 和 pyfcstm 文档确认事件路径。
- 对 composite state 的初始 transition，至少设置一个 hot-start sanity scenario，并在 comment 中说明初始 cycle 后实际落到哪个 leaf state。
- 若模型使用 forced transition 或 local event，必须至少有一个 scenario 覆盖该边；否则标记为 `oracle weak`。
- 若 scenario 需要 hot-start 到某个 nested state，必须显式提供 `initial_state` 与所需 `initial_vars`，不要依赖隐式变量默认值。

#### 4.2.1 事件作用域最小示例

`:: Event` 会创建/引用 source state namespace 下的 local event；`: /Event` 引用 root-level 绝对事件。若 scenario 注入的是 `events=["/Start"]`，transition 也应写 root-absolute event，而不是 local event。

```fcstm
state Root {
    event Start;
    [*] -> A;
    state A;
    state B;
    A -> B :: Start;
    A -> B : /Start;
}
```

上例第一条 transition 使用 local event `Root.A.Start`；第二条使用 root event `Root.Start`。正式输出模型中不要保留解释性注释。

```python
TestScenario(
    name="trigger_root_start",
    initial_state="Root.A",
    initial_vars={...},
    steps=[ScenarioStep(name="start", events=["/Start"], expected_state="Root.B")],
)
```

如果同名事件在多个 nested state 中出现，producer 必须在 comment 中说明它是 local event、parent-relative event 还是 root-absolute event，并用至少一个 scenario 覆盖真实注入路径。

#### 4.2.2 浮点阈值与整数化

若论文阈值很小或容易触发浮点比较噪声，可以把连续量做可解释的整数化，例如把 slip `0.01` 表达为 `slp_x100 >= 1`，并在 PR comment 中说明比例尺、单位和未覆盖的连续动力学。整数化只能用于降低 DSL/sim 噪声，不能改变阈值方向或扩大/缩小安全边界。

### 4.3 Path-2 candidate 边界

PR-E2 产物默认是 `ref model 候选`，不是 signed reference model。尤其是 Path-2 能源管理、医疗设备这类复杂论文，若只覆盖主链、抽象时间、或把连续时间条件事件化，必须写明：

- 覆盖了哪些状态/转移/输出；
- 没覆盖哪些子链、优先级、异常或连续控制语义；
- 是否 `main_result_eligible` 只作为候选观察而非正式主结果；
- 后续人工签核前需要补哪些证据。

### 4.4 不可达/非法状态

论文中的 illegal / invalid / fallback 状态可能被设计为“理论上不应进入，但必须有恢复边”。这类状态不应简单删除。推荐在 PR comment 中说明：

- 它是 paper-defined abnormal state 还是模型误造的 dead state；
- 是否有显式恢复边；
- 若 SD-4 报 `W_UNREACHABLE_STATE`，该 warning 是合理提示还是需要 policy waiver / scenario 覆盖。

## 5. 每轮修改后的四例闭环协议

PR-E2 的验收对象不是“skill 文档看起来合理”，而是“skill 能驱动 Codex/Claude 类 agent 产出足以作为 Path1/Path2 ref-model 蓝本的模型”。因此每轮迭代必须按以下顺序闭环：

```text
修改 skill / 上游 grammar prompt 硬伤
-> push
-> 4 个样本重新由 Codex 调用 skill 生成真实 ref-model 候选
-> 每个样本各自 new PR comment 留痕
-> 3 reviewer 同时 review 当前 skill + 4 个生成结果
-> reviewer 可对 skill 与模型质量提出 C/I/M
-> 修复 C/I，尽量吸收不拖进度的 M
-> 再次 4 样本真实生成
```

reviewer 的 review 范畴包括：

| 范畴 | 需要判断的问题 | 可给 C/I 的情形 |
|---|---|---|
| skill 全流程可用性 | agent 能否独立发现输入、工具、prompt、stage、repair、report 规则 | skill 会系统性误导 agent 或证据无法复现 |
| 语法/工具一致性 | grammar digest、SD tools、pyfcstm runtime 是否一致 | 文档要求的 DSL 会被实际 parser/semantic 拒绝 |
| ref model 学术质量 | 状态/变量/guard/action 是否忠实覆盖 NL/论文证据 | 模型缺失核心状态链、关键 guard/action，或抽象导致 Path1/Path2 结论不可靠 |
| scenario / sim oracle | 是否至少覆盖关键 nominal/abnormal/edge 转移 | 未仿真关键行为却声称 ready |
| fake/real 边界 | 是否绕过 skill、调用顶层 runtime、或把 hot-start/replay 冒充主结果 | 证据污染 PR-E2 主结论 |

只有当三路 reviewer 均确认 `C: 无 / I: 无`，且最新一轮 4 个样本的 ref-model 候选达到“可作为后续 Path1/Path2 ref model 蓝本”的质量，PR-E2 才能进入 ready-to-merge。

## 6. PR comment 记录模板

建议每个样本按下列结构写 PR comment；若模型过长，仍应保留最终候选模型全文或可审查摘录，并给出最小复现命令。

````markdown
## PR-E2 样本实测：<样本编号> <case_id>

- 身份：<codex/claude/...> skill-driven e2e producer
- Path 类别：Path-1 / Path-2
- 论文子路径：`project_1_llm_state_machine_modeling/sources/<case>/`
- NL 来源：`...`
- skill 入口：`agent_loop_skill/SKILL.md` 或 `agent_loop_skill/CLAUDE.md`
- 禁止调用检查：未调用 `method.loop.run_agent_loop(...)` / 未调用一键 runner

### 读取材料

| 类型 | 路径 | 用途 |
|---|---|---|
| skill | `...` | ... |
| paper | `...` | ... |

### 输入 NL 原文

```text
...
```

### 输入 NL 中文翻译 / 中文释义

```text
...
```

### Grounding 摘要

| 元素 | 证据 | 说明 |
|---|---|---|
| state/action/guard | `...` | ... |

### 最终候选模型

```fcstm
...
```

### 全流程真实摘要表

| Stage | 是否 LLM | 轮次 | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/命令 |
|---|---:|---:|---|---|---|---|---|
| E0/Skill discovery | 否 | - | ✅/❌ | ... | ... | 无 | `...` |
| E1/Grounding | 是/否 | 0 | ✅/❌ | ... | ... | 无/有 | `...` |
| E2/Modeling | 是 | 0 | ✅/❌ | ... | 生成 initial DSL | 生成 DSL | `...` |
| SD-2/3/4/6 | 否 | 0 | ✅/❌ | ... | 本地检查 | 无 | `...` |
| Repair/Review | 是/否 | 1 | ✅/❌ | ... | 修复/评审 | ... | `...` |

### 检查与修复轨迹

| 轮次 | 动作 | 反馈 | 修复 |
|---|---|---|---|
| 0 | initial candidate | ... | ... |

### ref model 学术评审

| 维度 | 结论 | 问题/证据 |
|---|---|---|
| NL fidelity | ... | ... |
| 状态/变量/guard/action 覆盖 | ... | ... |
| scenario/sim 覆盖 | ... | ... |
| main_result_eligible | true/false | ... |
| 合成变量/离散化抽象 | ... | 标明 synthetic / paper-defined / scenario-only |
| warning / SD-10 waiver | ... | pass / conservative fail + waiver / unresolved fail |
| 人工签核前待补 | ... | ... |

### 最终判断

- 状态：可用 / 部分可用 / 不可用
- 主要质量问题：...
- skill 改进建议：...
````

## 7. 常见误用与分级

| 误用 | 影响 | review 等级 |
|---|---|---|
| 调用 `method.loop.run_agent_loop(...)` 产出模型 | 不是 PR-E2 skill evidence | C |
| 未读取 skill，只凭 issue comment 工作 | 无法证明 repo-local skill 可用 | I |
| 未读取论文路径或 NL 来源不清 | ref-model grounding 不可信 | I |
| 不运行任何 parse/semantic/design/sim/review 检查 | 质量证据不足 | I |
| 只给摘要不给候选模型 | 无法审计 | I |
| comment 缺少局部命令或关键输出 | 可复现性弱 | I/M，视影响而定 |
| 文案不够美观但证据完整 | 不影响学术目标 | M |
```
