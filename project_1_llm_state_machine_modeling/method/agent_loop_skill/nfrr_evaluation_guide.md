# NFRR：NL + FCSTM 无参考模型质量评价体系

本文件是 PR-E2 skill 路径内的 **NFRR v3 完整自包含版**。它用于评价一个由 LLM / agent 生成的 FCSTM / pyfcstm 状态机模型在没有 existing reference model 时，是否足以作为 ref-model candidate 进入后续人工审阅、Path1/Path2 实验或论文证据链。

## 0. 方法定位

### 0.1 名称

**NFRR：NL-grounded FCSTM Reference Readiness**  
中文：**基于自然语言证据的 FCSTM 参考模型就绪度评价**。

### 0.2 一句话定义

给定一段自然语言需求 `NL` 和一个生成得到的 FCSTM / pyfcstm 模型 `model`，NFRR 通过 **NL 义务抽取、模型结构对齐、形式检查、行为场景仿真、变异诊断、scope/abstraction/waiver 审计**，判断这个模型是否只是一个诊断样本、是否可作为 within-NL candidate、是否可进入 paper-grounded reviewer queue，或是否已经达到 signed reference 的证据强度。

### 0.3 重要边界

NFRR 是 **formative readiness profile**，不是一个可以把维度加总/平均的 latent quality score。

也就是说：

- 不报告“总分”；
- 不把 8 个维度平均成一个数字；
- 不声称自动评价能证明模型绝对正确；
- 不把 `NFRR-T2/T3` 等同于 signed reference；
- 在未完成 calibration 之前，NFRR 只能称为 `uncalibrated_candidate_gate`，不能称为 validated metric。

NFRR 的学术定位是：

> 在没有 existing reference model 的条件下，把 generated FCSTM model 是否可作为 reference-model candidate 的证据链结构化、可复核、可审计地表达出来。

## 1. 输入与输出

### 1.1 输入

```text
required:
  NL: 自然语言需求片段 / 论文整理需求 / benchmark requirement fragment
  model: generated FCSTM / pyfcstm DSL

optional:
  paper_dir: 单论文目录，例如 paper_content.txt / bibtex.bib / DESC.md / STM.md
  declared_scope: producer 或任务方预先声明的覆盖边界
  run_context: provider、prompt hash、生成轨迹、repair history、review history 等
```

### 1.2 输出

```text
NFRR vector:
  FE / NGF / REC / GAS / SCB / AAT / BVS / DMR 八个维度，每维 0/1/2/3 分

NFRR tier:
  T0 / T1 / T2 / T3 / T4

claim:
  evidence_mode
  scope_type
  obligation_independence
  allowed_use_rule_id
  allowed_use
  signed_reference
  calibration_status

ledgers:
  NL coverage ledger
  obligation ledger
  model inventory
  alignment ledger
  scenario ledger
  mutation ledger
  waiver ledger
  cap reason ledger
```

### 1.3 三种 evidence mode

| evidence_mode | 输入 | 适用场景 | 结论边界 |
|---|---|---|---|
| `NL-only` | 只有 `NL + model` | 模拟真实运行时只给需求片段和模型的评价场景 | 只评价模型是否忠实于给定 NL，不能声称覆盖论文全文 |
| `NL+paper` | `NL + model + paper_dir` | 内部构造高质量 ref model，需要最大化 grounding | 可检查 NL 是否遗漏 paper 中与 scope 相关的关键状态/表格/异常链 |
| `authoritative_NL` | `NL + model`，但 NL 本身是权威需求规格 | 官方 benchmark requirement / signed industrial requirement | 可以把 NL 视为评价权威来源，但必须提供 provenance |

`authoritative_NL` 不能随便填，必须提供：

```json
{
  "authority_provenance": {
    "source_type": "official_requirement|benchmark_spec|industrial_requirement|human_signed_requirement",
    "source_ref": "repo path / URL / document id",
    "is_human_summarized": false,
    "signoff": "author / maintainer / dataset owner / human reviewer",
    "signer_role": "dataset_owner|benchmark_maintainer|domain_expert|independent_reviewer|producer_self",
    "scope_statement": "why this NL is the full authority for this evaluation"
  }
}
```

若缺少 `authority_provenance`，必须自动回落为 `NL-only`。

## 2. 核心概念

### 2.1 Obligation（需求义务）

Obligation 是从 NL 中抽取出的、模型应该表达的可评价语义单元。常见类型：

| 类型 | 例子 |
|---|---|
| `state` | `Waiting`、`Extending`、`Retracting`、`Faulted` |
| `event` | `BeginExtend`、`Extended`、`ResetFault` |
| `transition` | `Waiting + BeginExtend -> Extending` |
| `guard` | `temperature <= limit`、`battery_level < reserve_threshold` |
| `action/output` | `valve_open=1`、`alarm=1`、`drive_cmd=up` |
| `hierarchy` | `MotionControl` 包含 `Extending` 与 `Retracting` 子状态 |
| `reset/fault` | `FaultDetected` 强制进入 `Faulted`，`ResetFault` 返回 `Waiting` |
| `external_input` | `load_demand / renewable_power / battery_level` 来自环境或传感器 |
| `temporal/order` | 初始化后自动进入某状态；请求后到达传感器触发停止 |

### 2.2 Claim（评价结论声明）

每个 NFRR report 必须输出 claim，禁止只写 tier。

| 字段 | 允许值 | 说明 |
|---|---|---|
| `evidence_mode` | `NL-only` / `NL+paper` / `authoritative_NL` | 证据来源 |
| `scope_type` | `full_NL_fragment` / `subsystem_main_chain` / `component` / `local_fragment` | 模型覆盖范围 |
| `obligation_independence` | `single_self_assessment` / `two_pass_self_check` / `independent_adjudicated` / `model_blind_independent` / `human_signed` | obligation / alignment / waiver 是否独立复核 |
| `allowed_use_rule_id` | `AU-0..AU-6` | allowed_use 的派生规则 |
| `allowed_use` | `diagnostic_only` / `within_NL_candidate` / `reviewer_queue` / `paper_grounded_candidate` / `signed_reference` | 下游允许用途 |
| `signed_reference` | `true/false` | 是否已经人工/专家/独立 gold 签核 |
| `calibration_status` | `uncalibrated_candidate_gate` / `pilot_only` / `validated_metric` / `exploratory_profile_only` | 该评价体系是否已完成经验校准 |

## 3. 完整执行流程

### S0. 输入锁定与元信息记录

记录：

```json
{
  "nl_hash": "...",
  "model_hash": "...",
  "paper_dir": "optional path",
  "declared_scope": "optional",
  "evaluator": "name / model / reviewer identity",
  "timestamp": "...",
  "run_context_ref": "optional",
  "nfrr_version": "3.0"
}
```

若没有 `declared_scope`，默认 scope 是：**覆盖整个输入 NL fragment**。评价器不能事后把 NL 中难建模的义务排除。

### S1. Model-blind NL coverage ledger

这一步必须尽量在读取 model inventory 之前完成，以防止“只抽模型已经覆盖的义务”刷分。

#### S1.1 NL 切分规则

将 NL 切成 `NL-1...NL-n`：

1. 原始 bullet / 段落句号 / 分号级子句作为最小 span；
2. 不任意细切成词级义务；
3. 每个 span 必须分类，不能留空；PR-E2 样本 comment 若没有给出可复核的 NL coverage ledger，不允许声明 REC=3 / NGF=3，也不得进入 ready evidence。

#### S1.2 每个 NL span 的分类

| 分类 | 含义 | 是否进入 REC 分母 |
|---|---|---|
| `required_obligation` | 状态、事件、转移、guard、action、异常、时序等模型应表达语义 | 是 |
| `required_soft` | 建议性但影响质量的语义 | 默认不进硬 cap，可影响 NGF |
| `optional_obligation` | `may/can/optional` 之类可选行为 | 否 |
| `out_of_scope` | 任务或 declared_scope 预先排除，且有理由 | 否，但限制 allowed_use |
| `non_modelable_context` | 背景、动机、硬件清单、连续动力学细节等 | 否 |
| `ambiguous` | 需要人工裁决 | 否；过多会提升 uncertainty |

#### S1.3 模态词默认映射

| NL 表达 | 默认分类 |
|---|---|
| `shall` / `must` / `has to` / `is required to` / `always` / `reset forces` | `required_obligation` |
| `will` / `does` / `when...then` / `if...then` / `enters` / `transitions to` | `required_obligation` |
| `should` / `recommended` | `required_soft` |
| `may` / `can` / `optional` | `optional_obligation` |
| 背景描述但无离散控制义务 | `non_modelable_context` |

注意：`will/when...then/if...then` 若出现在论文背景或示例段落中，可以降为 `non_modelable_context`，但必须写 rationale。

#### S1.4 防刷分硬规则

- 每个 NL span 都必须被分类；未分类 span 最高 `T1`。如果 report/comment 完全缺少 NL coverage ledger，则视为 `NL_SPAN_UNCLASSIFIED`，最高 `T1`。
- 含有状态/事件/guard/action/reset/fault/temporal 语义的 span 若被标为 out-of-scope，必须引用 declared_scope 或 paper/任务边界；否则最高 `T1`。
- 若 evaluator 已经看过 model，只能标 `two_pass_self_check` 或 `single_self_assessment`，不能假装 model-blind。

### S2. Obligation ledger

每条 required obligation 必须结构化。

```json
{
  "obligation_id": "O-001",
  "nl_span_id": "NL-3",
  "type": "transition|state|event|guard|action|hierarchy|reset|fault|external_input|temporal",
  "requiredness": "required|required_soft|optional",
  "criticality": "critical|major|minor",
  "source_state": "optional",
  "target_state": "optional",
  "trigger_event": "optional",
  "guard": {
    "expr": "optional",
    "var": "optional",
    "op": "optional",
    "threshold": "optional"
  },
  "action_or_output": "optional",
  "external_inputs": ["optional"],
  "evidence_text": "short NL span",
  "scope_status": "in_scope|out_of_scope|non_modelable|ambiguous",
  "rationale": "short"
}
```

#### Criticality 默认规则

| 义务类型 | 默认 criticality |
|---|---|
| safety / fault / reset / alarm / stop / emergency / global invariant | `critical` |
| 主链状态、主链转移、阈值方向、动作输出 | `major` |
| 展示、日志、辅助输出、非主链 helper | `minor` |

### S3. Reliability / independence protocol

正式实验建议至少两路抽取：

1. `ledger_A`：model-blind 抽取；
2. `ledger_B`：换 prompt / provider / reviewer 的 model-blind 抽取；
3. 仲裁：required / optional / out-of-scope / criticality 分歧进入 `adjudication_log`。

最小一致性指标：

```text
span_classification_agreement = same_classified_spans / total_spans
required_obligation_iou = |required_A ∩ required_B| / |required_A ∪ required_B|
critical_label_agreement = agreement on critical/major/minor
```

建议阈值：`required_obligation_iou >= 0.6`。

#### Independence cap

| obligation_independence | 定义 | 最高 tier | 可进入 paper_grounded_candidate 吗 |
|---|---|---:|---|
| `single_self_assessment` | 同一 producer/evaluator 生成模型并给 NFRR，未独立复核 | T2 | 否 |
| `two_pass_self_check` | 同一 agent/团队两次自查，但无独立 reviewer/human adjudication | T2 | 否 |
| `independent_adjudicated` | 独立 reviewer/human 对 obligation、criticality、alignment、waiver、scenario oracle 做复核并记录 adjudication | T3 | 可以，若满足其他条件 |
| `model_blind_independent` | obligation ledger 在看 model inventory 前由独立 evaluator 冻结 | T3 | 可以，若满足其他条件 |
| `human_signed` | T3 证据包 + 人工/专家/独立 gold signoff | T4 | 是 |

#### 最小 adjudication_log

```json
{
  "adjudication_log": {
    "reviewer_identity": "github user / human / independent agent name",
    "reviewer_blind_to_model_generation": true,
    "reviewed_items": ["nl_span_classification", "requiredness", "criticality", "alignment", "waivers", "scenario_oracles"],
    "disagreements": [
      {"item": "O-003", "producer_label": "optional", "reviewer_label": "required", "resolution": "required"}
    ],
    "comment_or_artifact_ref": "PR comment URL / file path",
    "accepted": true
  }
}
```

同一 agent session、同一 prompt chain、同一 producer 调参后的二次 review 不算 independent。

### S4. Model inventory 与形式检查

对 FCSTM 执行：

1. `SD-2 parse`；
2. `SD-3 semantic/build`；
3. `SD-4 inspect/design`；
4. 输出 model inventory。

Inventory 至少包含：

```text
states
events
variables
transitions
guards
actions/effects
hierarchy
forced transitions
initial/final states
comments/annotations
```

工具输出引用：

```json
{
  "tool": "SD-2|SD-3|SD-4",
  "ok": true,
  "tool_output_ref": "path or PR comment section",
  "diagnostics": [
    {"id": "W_UNWRITTEN_READ_VAR", "element": "Root.x", "severity": "warning"}
  ]
}
```

#### SD-4 / design warning waiver ledger

任何 blocking / warning 若被 waive，必须写：

```json
{
  "warning_id": "W_GUARD_VARS_NEVER_CHANGE:...",
  "model_element_path": "Root.SomeTransition",
  "waiver_type": "external_input|output_only|known_tool_policy_gap|accepted_abstraction",
  "nl_or_paper_evidence": "NL-5 / paper page/table",
  "risk": "what could go wrong",
  "reviewer": "self|independent|human",
  "accepted": true
}
```

硬规则：

- 无证据 waiver 不得提升 FE/AAT；
- 涉及 critical/major required obligation 的无证据 waiver 最高 T1；
- critical/major waiver 只有 self reviewer 且无直接 NL/paper 证据，最高 T2；若影响 critical required behavior，则最高 T1。

### S5. Obligation-to-model alignment

将每条 in-scope required obligation 对齐到 model inventory。

| label | 判定标准 |
|---|---|
| `matched_exact` | 关键字段在模型中同名/同义存在，方向、阈值、动作一致 |
| `matched_abstract` | 模型用离散化/helper/routing/pseudo-state 表达同一语义，且 abstraction ledger 完整 |
| `partially_matched` | 存在对应元素，但缺少非关键字段或只覆盖部分分支 |
| `missing` | required obligation 无对应表达 |
| `contradicted` | 模型与 NL 相反或不兼容，如阈值方向、目标状态、动作值错误 |
| `extra_unjustified` | 模型元素无法映射到 obligation，也不是合理 helper/external/synthetic |

#### Field score

```text
field_score = matched_required_fields / total_required_fields
```

规则：

- `matched_exact`：`field_score=1.0`；
- `matched_abstract`：只有完整保留 critical/major fields 且 abstraction ledger 完整时 `field_score=1.0`；否则退回 partial 公式；
- `partially_matched`：按字段比例；
- `missing`：0；
- `contradicted`：0，并增加 contradiction count。

#### 默认 required fields

| obligation 类型 | 默认 required fields |
|---|---|
| `state` | state identity；若 NL 提到 hierarchy，则包含 parent/hierarchy；若提到 entry/exit effect，也包含 effect |
| `transition` | source、target、trigger/guard；若 NL 提到 effect/action，也包含 effect/action |
| `guard` | variable、operator direction、threshold、target behavior |
| `action/output` | output variable、assigned value/effect、触发位置 |
| `reset/fault` | trigger、source scope、target state、是否 forced/global、相关 action |
| `temporal` | order relation、前置状态/事件、后继状态/动作 |
| `external_input` | variable identity、environment/sensor evidence、供值方式 |
| `hierarchy` | parent、child、初始子状态或 containment relation |

#### Critical contradiction

以下与 NL 相反时，视为 critical/major contradiction：

- safety/fault/reset/alarm/stop；
- 阈值方向；
- 目标状态；
- 动作值；
- 模式互斥；
- forced transition；
- global invariant。

critical contradiction 最高 T1；若与全局语义相反且核心结构不可保留，T0/T1。

### S6. Scenario probes：obligation-anchored oracle

Scenario 用于验证模型行为，但必须避免“模型自证”。

#### S6.1 Oracle-first 原则

Scenario 的 expected outcome 必须来自 obligation ledger，而不是从当前 model inventory 或当前模型运行结果反推。

每个 scenario 必须记录：

```json
{
  "scenario_id": "S-001",
  "covered_obligation_ids": ["O-003", "O-004"],
  "oracle_source": "NL_span|paper_span|human_assumption",
  "expected_state": "from obligation, not model-derived",
  "expected_vars": {"from obligation": "..."},
  "provenance": "default_prefix|reachable_prefix|external_input_initial_vars|diagnostic_hot_start",
  "prefix_generation": "bfs_depth_K|manual_from_NL|heuristic|none",
  "reachable_prefix_witness": "event/guard prefix from default state, required when initial_state is non-empty and provenance=reachable_prefix",
  "runtime_execution_mode": "executed_prefix|runtime_hotstart_surrogate|default_runtime",
  "state_snapshot_justification": "required when runtime_hotstart_surrogate initializes internal/output vars",
  "external_input_ledger_ref": "required when provenance=external_input_initial_vars or reachable prefix relies on refreshed external inputs",
  "counted_for_main_BVS": true,
  "sd6_result": "pass|fail|not_run"
}
```

若 expected outcome 来自 model inventory，只能标：

```text
model_derived_oracle=true
```

并且不得计入主 BVS。

#### S6.2 Scenario provenance

| provenance | 是否计入 BVS 主证据 | 说明 |
|---|---|---|
| `default_prefix` | 是 | 从默认初态出发 |
| `reachable_prefix` | 是 | 从默认初态显式走到中间状态；若 SD-6 因当前 runtime 限制用 `initial_state` 近似执行，必须给出 `reachable_prefix_witness` 与 `runtime_execution_mode=runtime_hotstart_surrogate` |
| `external_input_initial_vars` | 是 | 从默认初态出发并只用 `initial_vars` 注入外部输入值，必须有 external-input ledger；若同时指定 `initial_state`，还必须满足 `reachable_prefix` 规则 |
| `diagnostic_hot_start` | 否 | 只能 debug，不能作为主证据 |
| `model_derived_oracle` | 否 | 只能 debug，不能作为主证据 |

#### S6.2.1 Scenario provenance hard rules

1. `initial_state` 非空不自动等于 `reachable_prefix`。只有同时给出从默认初态到该状态的事件 / guard 前缀，且该前缀来自 NL/paper obligation、paper 状态表或可复核搜索，才可标为 `reachable_prefix`。该前缀必须写入 `reachable_prefix_witness`；若只是“这个状态看起来可达”的口头判断，仍按 `diagnostic_hot_start` 处理。
2. 当前 `SD-6` `ScenarioStep` 不支持 step-level 变量刷新 / timer fast-forward；因此允许有限的 `runtime_hotstart_surrogate`：用 `initial_state` 执行目标 source-state 场景，但只有同时满足以下条件才可计入主 BVS：a) `reachable_prefix_witness` 说明该 source state 从默认初态可达；b) 所有内部 / output-only `initial_vars` 都等于该 source state 的 entry/during invariant 或已在前缀中由动作产生；c) 外部输入刷新变量有 external-input ledger；d) expected outcome 仍来自 NL/paper obligation 而不是当前模型运行结果；e) report 明确写 `runtime_execution_mode=runtime_hotstart_surrogate`。
3. `external_input_initial_vars` 只能注入传感器、环境量、连续控制器输出、状态表输入等 NL/paper 明确给出的外部输入。synthetic observability variables、output-only variables、test profile variables、为了断言方便添加的 helper variables 不得作为 external input。
4. 每个 `external_input_initial_vars` scenario 必须引用 external-input ledger，列出变量、证据、为什么不由模型内部写入，以及对应的 NL/paper source。若 scenario 同时使用 `initial_state`，则还必须引用 reachable-prefix witness；否则即使变量是外部输入，也只能算 `diagnostic_hot_start`。
5. 若 expected state / expected vars 来自当前 model inventory、当前模型运行结果或手工观察当前 DSL 后反推，必须标为 `model_derived_oracle=true`，不得计入主 BVS。
6. NFRR report 必须统计：

```text
main_scenario_count
counted_main_bvs_count
diagnostic_hot_start_count
model_derived_oracle_count
external_input_initial_vars_count
reachable_or_default_prefix_count
hot_start_main_obligation_ratio
```

其中：

```text
hot_start_main_obligation_ratio = critical+major obligations whose only scenario evidence is diagnostic_hot_start / all critical+major scenario-obligations
```

若 `hot_start_main_obligation_ratio >= 0.5`，则 `BVS` 最高为 `1`，并触发 final tier 最高 `T1` 的 hard cap。若比例在 `[0.25, 0.5)`，则 `BVS` 最高为 `2`，且必须在 `cap_reasons` 中记录 `HOT_START_PARTIAL_DEPENDENCE`。若 scenario provenance ledger 缺失或没有 `counted_for_main_BVS` 字段，则 BVS 最高为 `1`，并触发 `SCENARIO_PROVENANCE_MISSING`。

#### S6.3 Reachable prefix 生成算法

`reachable_prefix` 的操作定义：

1. 在 SD-3 build 后得到 transition graph；
2. 对目标/source state 做 BFS/DFS，默认最大深度 `K=20`；
3. 先按 state graph 找候选 transition 序列；
4. 再根据 transition guard/action 生成 `initial_vars` 或 step inputs；
5. 对每条 guard，尝试最小 satisfying assignment；
6. 找不到可执行 prefix 时，标 `prefix_unreachable`，不得伪造 prefix。

若 evaluator 只能靠 LLM 猜 prefix：

```text
prefix_synthesis = heuristic
BVS 最高 1
若主 scenario 全靠 heuristic/hot-start，则 final 最高 T1
```

#### S6.4 Boundary probe 规则

对 guard `x op c`：

| 变量/阈值类型 | probe 值 |
|---|---|
| int / enum-like | `c-1`, `c`, `c+1`，按 operator 选择正反两侧 |
| float | `eps = 10^(-p)`，`p` 为阈值小数位数 + 1；如 `0.01` 则 eps=`0.001` |
| boolean encoded int | `0/1`，不得使用 parser 不支持的 bool literal |
| 多变量表达式 | 固定非目标变量为 NL/paper nominal 值，只移动目标变量；无法确定则标 `boundary_uncertain` |

若变量声明为 `int`，eps 必须退化为 1；只有 `float` 才按小数位数选 eps。

### S7. Mutation / diagnostic robustness

DMR 衡量的是 scenario suite 对典型缺陷的敏感性，不单独证明模型正确。

一个 mutant 被 caught 的必要条件：

```text
original model passes obligation-anchored scenario
mutated model fails the same scenario
```

#### 最小 mutator 集

| mutant | source | 判定 |
|---|---|---|
| wrong transition target | required transition obligation | target 改为 sibling/other state，scenario 应 fail |
| missing reset/fault/forced transition | critical reset/fault obligation | 删除 forced/global transition，scenario 应 fail |
| guard direction / boundary flip | guard obligation | `<`/`<=`/`>`/`>=` 方向或 threshold perturb，boundary probe 应 fail |
| missing effect | action/output obligation | 删除 effect/enter action，expected_vars 应 fail |
| wrong effect value | action/output obligation | 输出值改为相反/邻近值，expected_vars 应 fail |

#### Mutation confusion matrix

| obligation | mutant | original pass | mutated fail | caught | survivor reason |
|---|---|---:|---:|---:|---|

#### 每条 obligation 的最小 mutant 数

| criticality | 最小 targeted mutant |
|---|---:|
| critical | 至少 2 个，覆盖不同错误类型；若只有一种可变异字段，必须在 ledger 写 `mutable_field_count=1` 并解释 |
| major | 至少 1 个 |
| minor | 可选 |

## 4. 八维评分体系

### 4.1 公式

```text
weighted_recall = sum(field_score(required obligation) * criticality_weight) / sum(criticality_weight)
criticality_weight:
  critical = 3
  major = 2
  minor = 1

scenario_generation_coverage = obligations_with_runnable_or_executed_main_scenario / all critical+major scenario-obligations
scenario_pass_rate = passed counted main scenarios / runnable counted main scenarios

mutation_generation_coverage = obligations_with_generated_targeted_mutant / all critical+major mutable-obligations
mutation_caught_rate = caught targeted mutants / runnable targeted mutants
```

`scenario-obligation` / `mutable-obligation` 分母只统计 S1 中判定为 required 且 critical/major 的 obligation，不包含 `non_modelable_context`、`optional_obligation` 或无关背景。`diagnostic_hot_start` 与 `model_derived_oracle` 不进入 runnable counted main scenario 分子；若把它们计入 pass-rate，应视为评分错误。

若 strict waiver 将某项移出分母，必须记录：

```text
all critical+major obligations
scenario-obligations
mutable-obligations
strict waiver 移除数
not-covered 数
```

### 4.2 八个维度

| 维度 | 中文名 | 0 分 | 1 分 | 2 分 | 3 分 |
|---|---|---|---|---|---|
| **FE** | 形式可执行性 | SD-2/3 fail | parse/semantic 勉强可用但有 blocking 或不可解释 design issue | SD-2/3 pass，SD-4 无 unwaived blocking，warning 部分有 waiver | SD-2/3/4 clean，或所有 warning/blocking 均有严格 waiver ledger |
| **NGF** | NL 语义忠实度 | critical contradiction >0 或 major contradiction 多发 | 主状态名存在但 transition/guard/action 大量 missing | 无 critical contradiction，major required 大体 matched，少量 partial/missing | required obligations 基本 exact/abstract matched，无 critical/major contradiction |
| **REC** | 需求覆盖率 | weighted_recall < 0.4 | 0.4–0.7 | 0.7–0.9 且无 critical missing | >=0.9 且无 critical/major missing |
| **GAS** | guard/action 一致性 | guard/action critical contradiction | guard/action 覆盖 <0.4 或无 boundary probe | guard/action 覆盖 >=0.7，关键 boundary 部分 pass | guard/action 覆盖 >=0.9，critical boundary/action probes pass |
| **SCB** | scope 边界清晰度 | scope 缺失且事后排除 NL 义务 | scope 模糊或 out-of-scope 理由弱 | scope 清楚，NL spans 全分类，out-of-scope 有理由 | producer/task-declared scope 与 evaluator 验证一致，claim/allowed_use 清楚 |
| **AAT** | 抽象与假设透明度 | helper/synthetic/external/waiver 污染无说明 | 有说明但缺 evidence 或混入本体 | 主要 synthetic/external/waiver 有 ledger | 所有 abstraction/external/input/output-only/waiver 均有 evidence+rationale+risk |
| **BVS** | 行为验证强度 | 无 scenario、SD-6 fail、或主证据是 model-derived oracle | 只有 sanity/hot-start/heuristic prefix，缺少 scenario provenance ledger，或 counted scenario_generation_coverage <0.4 | counted scenario_generation_coverage >=0.6 且 counted pass_rate >=0.7，覆盖至少一条主链，oracle_weak=false，hot-start 依赖未支配 critical/major 义务 | counted scenario_generation_coverage >=0.8，critical scenario obligations 全覆盖，counted pass_rate >=0.9，覆盖主链+边界+异常，oracle 全部 obligation-anchored，且 provenance/前缀/external-input ledger 完整 |
| **DMR** | 诊断/变异敏感性 | 无 mutation，或 original model 未通过对应 scenario | mutation_generation_coverage <0.4 或 caught_rate <0.5 | mutation_generation_coverage >=0.6 且 caught_rate >=0.6，覆盖至少两类 mutant | mutation_generation_coverage >=0.8 且 caught_rate >=0.8；critical guard/action/reset/target mutants 无 survivor |

若 NL 中没有 guard/action obligation，GAS 标 `N/A`，tier 判定时视为满足最低门槛，但必须说明“NL 中无 guard/action 义务”。

## 5. Tier 判定与 hard caps

### 5.1 Tier 必要条件

| Tier | 名称 | 必要条件 |
|---|---|---|
| **T0** | 不可用 | SD-2/3 fail；或模型完全无法对应 NL；或 critical contradiction 导致全局行为相反且核心结构不可保留 |
| **T1** | 诊断样本 | FE>=1，但存在 critical missing/contradiction、unwaived blocking、SD-6 fail、oracle_weak、hot-start-only、NL span 未分类等 |
| **T2** | within-scope candidate | FE>=2, NGF>=2, REC>=2, GAS>=2/N/A, SCB>=2, AAT>=2, BVS>=2, DMR>=1；无 critical contradiction |
| **T3** | strong candidate within declared scope | FE=3, NGF>=2, REC=3, GAS>=2/N/A, SCB>=3, AAT>=2, BVS=3, DMR>=2；需要 `independent_adjudicated` 或 `model_blind_independent` |
| **T4** | signed reference | T3 + `signed_reference=true` + human/expert/gold signoff |

### 5.2 Hard cap table

| 条件 | 最高 tier |
|---|---:|
| SD-2/3 fail | T0 |
| critical contradiction | T1 |
| critical required obligation missing | T1 |
| 未分类 NL span 且可能含模型义务 | T1 |
| 缺少可审计 NL coverage ledger / obligation ledger | T1 |
| out-of-scope 无 declared_scope / evidence 支撑 | T1 |
| unwaived SD-4 blocking | T1 |
| reachable test harness pollution | T1 |
| main scenario 全部 diagnostic_hot_start 或 model-derived oracle | T1 |
| 缺少 scenario provenance ledger 或缺少 `counted_for_main_BVS` 字段 | T1 |
| `hot_start_main_obligation_ratio >= 0.5` | T1 |
| SD-6 fail / oracle_weak=true | T1 |
| required weighted_recall <0.7 | T1 |
| no scenario matrix | T1 |
| single_self_assessment | T2 |
| two_pass_self_check without independent adjudication | T2 |
| required_obligation_iou <0.6 且无 adjudication | T2 |
| DMR=0 | T2 |
| critical required obligation 缺 runnable obligation-anchored scenario 且无 strict waiver | T2 |
| critical required obligation 缺 targeted mutant 且无 independent/tool waiver | T2 |
| NL-only 且非 authoritative_NL，用于 Path1/Path2 paper-grounded ref construction | T2 |
| 无 human/expert signoff | T3 |

最终 tier 计算：

```text
final_tier = min(tier_before_cap, all hard caps)
```

所有触发 cap 都必须写入 `cap_reasons`。

## 6. Test harness / sample-case 污染规则

若最终 DSL 本体中出现只服务于 scenario/test 的 reachable 元素，例如：

```text
sample_case
probe
oracle
expected
scenario
test_case
__probe_*
__expected_*
```

且无法映射到 NL/paper obligation 或合理 abstraction，则为 **test harness pollution**。

Hard cap：

| 情况 | 最高 tier |
|---|---:|
| reachable test harness pollution | T1 |
| unreachable 注释/死代码式 helper，且进入 AAT ledger | T2 |
| scenario profile 通过 DSL 本体变量硬编码，而非 scenario initial_vars / external input | T1 |

## 7. Allowed use 派生规则

`allowed_use` 不能手填，必须由 `final_tier + evidence_mode + scope_type + independence + signed_reference + cap_reasons + calibration_status` 派生。若手填值与派生值冲突，以派生值为准。

| rule_id | 条件 | allowed_use |
|---|---|---|
| **AU-0** | `final_tier <= T1` | `diagnostic_only` |
| **AU-1** | `final_tier = T2` 且 `evidence_mode=NL-only` | `within_NL_candidate` |
| **AU-2** | `final_tier = T2` 且 `evidence_mode=authoritative_NL` | `reviewer_queue` |
| **AU-3** | `final_tier = T2` 且 `evidence_mode=NL+paper` | `reviewer_queue` |
| **AU-4** | `final_tier = T3` 且 `independence in {independent_adjudicated, model_blind_independent}` 且 `evidence_mode in {NL+paper, authoritative_NL}` | `paper_grounded_candidate` |
| **AU-5** | `final_tier = T3` 但 `scope_type in {component, local_fragment}` | `reviewer_queue`，只能用于 component/fragment-level |
| **AU-6** | `final_tier = T4` 且 `signed_reference=true` | `signed_reference` |

若多条 AU 同时命中，取更严格的 allowed_use。严格度：

```text
diagnostic_only < within_NL_candidate < reviewer_queue < paper_grounded_candidate < signed_reference
```

AU-5 优先于 AU-4：`component/local_fragment` 即便证据强，也不能进入 full-system reference 统计。

禁止组合：

- `NL-only + paper_grounded_candidate`；
- `signed_reference=false + allowed_use=signed_reference`；
- `scope_type=local_fragment + full-system reference 统计`；
- `single_self_assessment/two_pass_self_check + paper_grounded_candidate`。

若 `calibration_status=exploratory_profile_only`，allowed_use 不得超过 `reviewer_queue`。

## 8. Calibration protocol

NFRR v3 可以作为 PR-E2 的 **candidate gate / structured review rubric** 使用。若要在论文中声称它是 validated metric，需要执行 calibration protocol。

未校准时必须写：

```text
calibration_status = uncalibrated_candidate_gate
```

### 8.1 校准样本

| 集合 | 最小数量 | 来源 |
|---|---:|---|
| Path1 gold/reference subset | >=10 | 有 signed/ref behavior 或人工 reference 的样本 |
| Path2 paper-grounded subset | >=10 | 有 paper_dir、状态表/流程图/专家可审证据的样本 |
| known-bad mutants | 每个好模型 >=5 | threshold direction / missing reset / wrong effect / wrong target / harness pollution |

若样本不足：

```text
calibration_status = pilot_only
```

不得声称 validated metric。

### 8.2 统计与阈值

| validity / reliability | 指标 | 建议阈值 |
|---|---|---|
| convergent validity | NFRR tier 与 expert ordinal score / component-level F-score 的 Spearman ρ 或 Kendall τ | ρ >= 0.5 或 τ >= 0.35 |
| discriminant validity | FE 单独预测 high tier 的能力 | FE pass 不应单独把低 fidelity 模型推到 T2/T3 |
| known-groups validity | known-bad mutants 被降级到 T1/T2 的比例 | >=90%；critical contradiction 应 100% 不进 T3 |
| inter-rater reliability | required/optional/out-of-scope Cohen κ 或 IoU | κ >=0.6 或 required IoU >=0.6 |
| alignment reliability | matched/exact/partial/contradicted label agreement | κ >=0.6 |

若校准未达阈值：

```text
calibration_status = exploratory_profile_only
allowed_use 不得超过 reviewer_queue
论文中不得把 NFRR 作为主评价指标，只能作为诊断性 profile
```

当 `calibration_status=validated_metric` 时，必须附 calibration artifact ref：

```json
{
  "calibration_artifact_ref": "run path / report path / PR comment URL"
}
```

## 9. 最小 report schema

```json
{
  "nfrr_version": "3.0",
  "claim": {
    "evidence_mode": "NL-only|NL+paper|authoritative_NL",
    "authority_provenance": null,
    "scope_type": "full_NL_fragment|subsystem_main_chain|component|local_fragment",
    "obligation_independence": "single_self_assessment|two_pass_self_check|independent_adjudicated|model_blind_independent|human_signed",
    "allowed_use_rule_id": "AU-0..AU-6",
    "allowed_use": "diagnostic_only|within_NL_candidate|reviewer_queue|paper_grounded_candidate|signed_reference",
    "signed_reference": false,
    "calibration_status": "uncalibrated_candidate_gate|pilot_only|validated_metric|exploratory_profile_only",
    "calibration_artifact_ref": null
  },
  "nl_spans": [
    {"id": "NL-1", "text": "...", "class": "required_obligation", "rationale": "..."}
  ],
  "obligations": [
    {"obligation_id": "O-001", "nl_span_id": "NL-1", "type": "transition", "criticality": "major"}
  ],
  "model_inventory_ref": {
    "sd2": "...",
    "sd3": "...",
    "sd4": "..."
  },
  "alignments": [
    {"obligation_id": "O-001", "label": "matched_exact", "field_score": 1.0, "model_element_path": "Root.A->B"}
  ],
  "scenarios": [
    {
      "scenario_id": "S-001",
      "covered_obligation_ids": ["O-001"],
      "oracle_source": "NL-1",
      "expected_state": "Root.Target",
      "expected_vars": {"x": 1},
      "provenance": "reachable_prefix",
      "prefix_generation": "manual_from_NL",
      "reachable_prefix_witness": "default -> A via Start",
      "runtime_execution_mode": "executed_prefix",
      "state_snapshot_justification": null,
      "initial_state": null,
      "external_input_ledger_ref": null,
      "counted_for_main_BVS": true,
      "sd6_result": "pass"
    }
  ],
  "mutations": [
    {"mutation_id": "M-001", "obligation_id": "O-001", "mutant": "wrong_transition_target", "original_pass": true, "mutated_fail": true, "caught": true}
  ],
  "waivers": [
    {"warning_id": "...", "accepted": true, "evidence": "NL-4", "risk": "..."}
  ],
  "coverage": {
    "weighted_recall": 0.0,
    "scenario_generation_coverage": 0.0,
    "scenario_pass_rate": 0.0,
    "mutation_generation_coverage": 0.0,
    "mutation_caught_rate": 0.0,
    "main_scenario_count": 0,
    "counted_main_bvs_count": 0,
    "diagnostic_hot_start_count": 0,
    "model_derived_oracle_count": 0,
    "external_input_initial_vars_count": 0,
    "reachable_or_default_prefix_count": 0,
    "hot_start_main_obligation_ratio": 0.0
  },
  "scores": {
    "FE": 0,
    "NGF": 0,
    "REC": 0,
    "GAS": 0,
    "SCB": 0,
    "AAT": 0,
    "BVS": 0,
    "DMR": 0
  },
  "tier_before_cap": "T0|T1|T2|T3|T4",
  "cap_reasons": [],
  "final_tier": "T0|T1|T2|T3|T4"
}
```

### 建议 cap reason 枚举

```text
SD2_FAIL
SD3_FAIL
CRITICAL_CONTRADICTION
CRITICAL_REQUIRED_MISSING
NL_SPAN_UNCLASSIFIED
OUT_OF_SCOPE_UNSUPPORTED
UNWAIVED_SD4_BLOCKING
TEST_HARNESS_POLLUTION
MODEL_DERIVED_ORACLE
SCENARIO_PROVENANCE_MISSING
HOT_START_DOMINANCE
HOT_START_PARTIAL_DEPENDENCE
SD6_FAIL
ORACLE_WEAK
LOW_REQUIRED_RECALL
NO_SCENARIO_MATRIX
IND_SINGLE_SELF_ASSESSMENT
IND_TWO_PASS_SELF_CHECK
LOW_OBLIGATION_IOU
DMR_ZERO
CRITICAL_NO_SCENARIO
CRITICAL_NO_MUTANT
NL_ONLY_PAPER_GROUNDED_TASK
NO_HUMAN_SIGNOFF
CALIBRATION_EXPLORATORY
SCOPE_LOCAL_FRAGMENT
```

## 10. Markdown 输出模板

```markdown
## NFRR report: <artifact_id>

### 0. Claim

| 字段 | 值 |
|---|---|
| evidence_mode | ... |
| scope_type | ... |
| obligation_independence | ... |
| allowed_use_rule_id | ... |
| allowed_use | ... |
| signed_reference | false |
| calibration_status | uncalibrated_candidate_gate |

### 1. NL coverage ledger

| NL span | class | rationale |
|---|---|---|
| NL-1 | required_obligation | ... |

### 2. Obligation ledger

| id | type | criticality | NL span | required fields |
|---|---|---|---|---|
| O-001 | transition | major | NL-1 | source/target/event/guard |

### 3. Model checks

| check | result | diagnostics | ref |
|---|---|---|---|
| SD-2 | pass/fail | ... | ... |
| SD-3 | pass/fail | ... | ... |
| SD-4 | pass/fail | ... | ... |

### 4. Alignment

| obligation | label | field_score | model element | risk |
|---|---:|---:|---|---|
| O-001 | matched_exact | 1.0 | Root.A->B | none |

### 5. Scenario evidence

| scenario | obligations | provenance | oracle_source | SD-6 |
|---|---|---|---|---|
| S-001 | O-001 | reachable_prefix | NL-1 | pass |

### 6. Mutation evidence

| mutation | obligation | original pass | mutated fail | caught |
|---|---|---:|---:|---:|
| M-001 | O-001 | true | true | true |

### 7. Scores

| Dimension | Score | Evidence | Risk | Improvement |
|---|---:|---|---|---|
| FE |  |  |  |  |
| NGF |  |  |  |  |
| REC |  |  |  |  |
| GAS |  |  |  |  |
| SCB |  |  |  |  |
| AAT |  |  |  |  |
| BVS |  |  |  |  |
| DMR |  |  |  |  |

### 8. Tier

- tier_before_cap: ...
- cap_reasons: ...
- final_tier: ...
- allowed_use: ...
```

## 11. Worked example

### 11.1 输入 NL

```text
When pressure > 10, the pump shall stop and alarm shall sound until Ack. Reset returns the controller to Manual.
```

### 11.2 NL coverage ledger

| span | class | obligation |
|---|---|---|
| NL-1 `pressure > 10` 时 pump stop | required_obligation | O1 guard/action：`pressure > 10 -> Stopped`, `pump_output=0` |
| NL-2 alarm sound until Ack | required_obligation | O2 action/event：`alarm=1` until `Ack` clears |
| NL-3 Reset returns Manual | required_obligation | O3 critical reset：any -> Manual |

### 11.3 若模型只覆盖 O1

模型只有 `pressure > 10 -> Stopped`，但没有 alarm/Ack/reset：

- REC 不能得 1.0，因为 O2/O3 必须进入分母；
- O3 是 critical missing，final 最高 T1；
- 若 scenario 只从模型推导 `pressure=11 -> Stopped`，BVS 最多 1；
- 若新增 `sample_case=1` 使 scenario 通过，属于 test harness pollution，最高 T1；
- 即使 FE=3，也不能进入 T2/T3。

## 12. PR-E2 准出标准

### 12.1 单个 ref-model sample 的最低准出

PR-E2 中每个 skill-generated sample 至少必须达到：

```text
final_tier >= T2
allowed_use in {within_NL_candidate, reviewer_queue, paper_grounded_candidate}
calibration_status = uncalibrated_candidate_gate
SD-2/SD-3 pass
SD-4 无 unwaived blocking
至少一个 `counted_for_main_BVS=true` 的 obligation-anchored scenario 通过 SD-6
无 reachable test harness pollution
无 critical contradiction
```

若达不到上述要求，该 sample 只能作为 diagnostic evidence，不能称为 ref-model candidate。

### 12.2 Ground-Truth 级 ref-model candidate 的目标准出

若 PR-E2 希望产出“可作为 Ground Truth 级别 ref model 蓝本”的候选，目标应为：

```text
final_tier >= T3
obligation_independence in {independent_adjudicated, model_blind_independent}
evidence_mode in {NL+paper, authoritative_NL}
allowed_use in {paper_grounded_candidate, reviewer_queue}
BVS = 3
REC = 3
FE = 3
无 critical/major contradiction
无 unwaived critical/major warning
所有 critical scenario obligations 有 runnable obligation-anchored scenario
所有 critical mutable obligations 有 targeted mutant 或 strict waiver
signed_reference = false  # 除非已有人工/专家签核；否则仍不得称 signed reference
```

在未完成人工/专家签核前，即使达到 T3，也只能称为：

```text
strong paper-grounded ref-model candidate / Ground Truth candidate blueprint
```

不能称为 signed reference / final ground truth。

### 12.3 PR-E2 comment 必须包含

每个样本 comment 至少包含：

1. 输入 NL；
2. 可选 paper_dir；
3. generated FCSTM model 全文；
4. NFRR claim；
5. NL coverage ledger；
6. obligation-to-model alignment；
7. SD-2/3/4 检查；
8. scenario + SD-6；
9. mutation / DMR；
10. waiver ledger；
11. 8 维 scores；
12. final tier + cap reasons + allowed_use。

对于 PR-E2 当前用途，若没有完成 calibration，应统一写：

```text
calibration_status = uncalibrated_candidate_gate
```
