# R5.7.4 静态裁决与指标 dry-run 报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与问题

R5.7.4 的任务是把 R5.7.1 评价逻辑链、R5.7.2 Better STM / repair target taxonomy、R5.7.3 objective metric framework 放到 4 个真实 `llms-emp` pair 上做 **静态 dry-run**：检查规则能否从 `NL + raw STM_0 + case matrix + loss / archive` 证据走到 taxonomy 裁决、metric permission 映射和 R6/R7 handoff [src-r571][src-r572-better][src-r572-tax][src-r573][clm-r574-boundary]。

本报告不是 repair 实验：本轮不运行 LLM、不读取 `.env`、不生成 `STM_k`、不产生 change ledger，因此不能报告 `valid_run`、`better`、Better STM 成功率或 repair effectiveness [clm-r574-boundary][clm-r574-no-better]。

## 2. 核心结论

| 主题 | R5.7.4 dry-run 结论 | 证据键 |
|---|---|---|
| 规则可执行性 | 四例均能从 committed `NL` / raw PlantUML / case matrix / archive 证据走到静态裁决；但正式 Better run 因无 `STM_k` 与 change ledger 一律不能判 `valid_run`。 | [clm-r574-preflight][clm-r574-no-better] |
| T0 condition-like | `0000` 的 `Front Distance > 10` 由 `NL` 与 raw `STM_0` 双重支持，可作为 T0 主线 `guard_condition` 的 `should_fix` dry-run finding；其他 hierarchy / source lifting 仍只是 monitor。 | [clm-r574-0000] |
| T0 low-noise control | `0001` 无 loss code、无 partial ledger 行，应作为 no-target / low-noise control；taxonomy 不应为它凭空制造缺陷。 | [clm-r574-0001] |
| T0.5 caveat | `0045` 的 timer / zero-time cue 与 normalization replay 只能作 T0.5 caveat / representation monitor；不得写 timed automata 或 repair gain。 | [clm-r574-0045] |
| T1 stress | `0018` 暴露 timing、fork/choice、cross-scope 与 condition-like stress，但 scope 是 `stress_t1`；不得进入 T0 Better 主比较。 | [clm-r574-0018] |
| 指标权限 | parse / inspect / evidence bundle 是 hard gate；loss code、conversion status、selected `.fcstm` hash 只能 report / trigger；guard/action fidelity、target closure 等必须等 R6/R7 有 `STM_k` 与 target-instance ledger 后才可作 supporting evidence。 | [clm-r574-metric] |
| `.fcstm` baseline 物化缺口 | 0001 / 0018 当前只有 seed-sweep hash 与 parse / inspect status，没有 standalone `.fcstm`；R6/R7 前必须物化 baseline evidence bundle。 | [clm-r574-fcstm-missing] |
| `.fcstm` hash 权威源 | 0000 / 0045 已有 selected smoke standalone `.fcstm`；selected hash 与 seed-sweep hash 不同属于不同转换运行的预期差异，不是缺失。R6/R7 需要明确 authoritative baseline hash，seed-sweep hash 作为 audit trail。 | [clm-r574-fcstm-authority] |

## 3. 四例总表

| pair | 角色 | scope | time / family | conversion / parse / inspect | loss codes | dry-run taxonomy finding | formal Better 状态 |
|---|---|---|---|---|---|---|---|
| `llms_emp_stm_results_0000` | HLDCS / GPT-4o / condition-like HSM | `main_t0` | T0 / HSM | partial / ok / ok | `condition_like_label_lowered_as_event` 等 3 类 | `guard_condition -> should_fix` for `Front Distance > 10`；hierarchy/source lifting monitor | outcome=`unknown`；reason=`not_evaluated_in_static_dry_run`；无 `STM_k` |
| `llms_emp_stm_results_0001` | HSTBS / GPT-4o / low-noise FSM | `main_t0` | T0 / FSM | converted / ok / ok | none | `not_repair_target` / no-target control | outcome=`unknown`；reason=`not_evaluated_in_static_dry_run`；无 `STM_k` |
| `llms_emp_stm_results_0045` | Microwave / DeepSeek / timer-like caveat | `caveat_t05` | T0.5 / UML-SysML statechart | partial / ok / ok | normalization replay + hierarchy/source lifting | `temporal_cue_tick_counter_caveat -> monitor`；conversion artifact monitor | outcome=`unknown`；reason=`not_evaluated_in_static_dry_run`；不进 T0 headline |
| `llms_emp_stm_results_0018` | Digital Camera / GPT-4 / T1 stress | `stress_t1` | T1 / UML-SysML statechart | partial / ok / ok | condition-like + cross-scope + normalization 等 | `out_of_scope_family -> out_of_scope`；condition-like only stress trigger | outcome=`unknown`；reason=`not_evaluated_in_static_dry_run`；不进 Better 主比较 |

以上 `conversion=partial/converted` 是 representation readiness 状态，不是 Better outcome；`partial` 不得被写成 repair failure，也不得被写成 repair success [src-r571][clm-r574-preflight]。

## 4. 代表性证据片段

### 4.1 `0000`：T0 HSM 的 guard candidate

`NL` 写明 “when front_distance > 10, auto transport to autonomous state”，raw PlantUML 对应迁移是：

```plantuml
InitialState --> Autonomous : Front Distance > 10
Autonomous --> HumanDriving : Human Steering Cmd or Brake Pressed
```

这使 `Front Distance > 10` 具备从 representation symptom 升级为 `guard_condition` / `should_fix` dry-run finding 的证据基础；但该结论仍不是正式 Better 裁决，因为没有 `STM_k` 证明 guard extraction 后无回归且语义更保真 [src-pairs][src-ledger][clm-r574-0000]。

### 4.2 `0001`：T0 FSM 的 no-target control

`0001` 的 raw PlantUML 只含 braking / operational / clamping / feedback 等普通事件迁移，case matrix 记录 `r5_loss_codes=[]`：

```plantuml
InitialState --> BrakingState : Brake Signal Received
InitialState --> OperationalState : Signal Transmission Fails
BrakingState --> ClampingState : Entering Clamping State
OperationalState --> InitialState : Signal Feedback Sent
```

因此 R5.7.4 应把它用作 taxonomy sanity check：没有 loss / ledger 证据时，规则不能为了“修复”而强行新增 target；若 R6 对该例产生改动，反而需要重点审查 over-repair [src-case][clm-r574-0001]。

### 4.3 `0045`：T0.5 timer-like caveat

`0045` 同时出现 zero-time cue、cooking time 与 timer expired：

```plantuml
DoorOpenWithItem --> DoorShutWithItem : Door Closed [zero time set]
ReadytoCookIdle --> Cooking : Start
CookingIdle --> DoorShutWithItem : Timer Expired
```

这些信息足以支持 T0.5 caveat / monitor，但不足以支持 timed automata、clock constraint 或 T0 headline success。`R5.LOSS.r3_1_normalization_replay_not_repair` 明确说明 normalization replay 是 conversion readiness，不是 repair gain [src-case][src-ledger][src-archive][clm-r574-0045]。

### 4.4 `0018`：T1 supplementary stress

`0018` 包含 seconds bound、probability-like cue、fork / choice / join 与 cross-scope 引用：

```plantuml
[*] --> TurnOn : 2 sec
AutoFocus -down-> choice1 : memFull=true
DetLight -down-> choice2 : <<GaStep>>{prob=0.4}
choice2 --> Join1 when : sunny=true
```

这类样例适合证明 R5.7 taxonomy 有 stress / out-of-scope 出口，而不是证明方法能处理 timed / probabilistic / arbitrary UML statechart。它可以进入 limitation / stress 表，但不能进入 T0 success denominator [src-case][src-archive][clm-r574-0018]。

## 5. R5.7.2 taxonomy 裁决结果

| pair | observed issue | semantic element | repair action | Better gate 影响 | 本轮结论 |
|---|---|---|---|---|---|
| `0000` | condition-like label + HSM lowering | `guard_condition` + `representation_artifact` | `should_fix` for guard；`monitor` for representation caveat | G0=main_t0；G1=cannot_evaluate；G2=pending 或 caveat；G3=待 no-regression run；G4=待 formal improvement；G5=待语义裁决；G6=pending 或 caveat reporting。 | 可形成 T0 target-instance seed，但需 R6/R7 正式 run 验证。 |
| `0001` | no recorded issue | none / no-target | `not_repair_target` | G0=main_t0；G1=cannot_evaluate；G2=not_applicable_until_change；G3=over-repair guard pending；G4=待 formal improvement check；G5=待语义裁决；G6=待 reporting bundle。 | 作为 no-target control；若后续改动需证明必要性。 |
| `0045` | timer cue + normalization replay | `temporal_cue` + `representation_artifact` | `monitor` | G0=caveat_t05；G1=cannot_evaluate；G2=caveat attribution；G3=不进 T0 headline；G4=不进 T0 headline；G5=仅 caveat-level；G6=caveat/reporting_only。 | T0.5 caveat，不进 T0 headline。 |
| `0018` | timing / fork-choice / cross-scope / condition-like | `out_of_scope_family` + stress triggers | `out_of_scope` / `monitor` | G0=stress_t1；G1=not_applicable_to_better_main_comparison；G2=not_applicable_to_better_main_comparison；G3=not_applicable_to_better_main_comparison；G4=not_applicable_to_better_main_comparison；G5=not_applicable_to_better_main_comparison；G6=stress/caveat reporting only。 | supplementary stress，不进 Better 主比较。 |

该表的 `repair action` 是 dry-run finding，不是 R6 已采取动作；正式 target closure 必须等 R6/R7 的 target-instance ledger 和 change ledger [src-r572-tax][clm-r574-no-better]。

## 6. R5.7.3 metric permission dry-run

| 证据 / 指标 | 本轮权限 | 四例落点 | 禁止外推 |
|---|---|---|---|
| `schema_validity_status`、`parse_validity_status`、`inspect_status` | `hard_gate` | 四例 parse / inspect 均 ok，可继续静态分析。 | 不证明语义更好。 |
| `evidence_bundle_completeness` | `hard_gate` for formal run | 静态输入证据足够；正式 Better run 缺 `STM_k` / change ledger。 | 不得写 formal `valid_run`。 |
| loss code / conversion status / loss count | `report_only` 或 `trigger_only` | 用于定位 representation caveat 和 stress risk。 | 不计 repair gain。 |
| `event_guard_action_folding_risk` | `trigger_only` | 0000 / 0018 触发；0000 有 NL/raw 支撑 guard candidate，0018 仅 stress。 | 不直接判 `better` / `not_better`。 |
| slot-level guard/action fidelity | `supporting_evidence` only after reference / target | 本轮只能说明未来需要 target-instance evidence。 | 无 reference 时不计算 F1。 |
| target closure | `supporting_evidence` after R6/R7 | 本轮没有 closure，因为没有 repair action taken。 | 不得报告 closure rate。 |
| T0.5/T1 统计 | `report_only` / caveat / stress | 0045、0018 分别进入 caveat / stress。 | 不混入 T0 headline。 |

## 7. R6/R7 handoff

### 7.1 给 R6 的提示

1. 对 `0000`，可把 `Front Distance > 10` 做成 guard-extraction feedback seed，但必须保留 raw label trace 与 no-regression 检查。
2. 对 `0001`，建议作为 no-op / low-noise control，验证 feedback loop 不会为了指标而过修。
3. 对 `0045`，若使用，只能要求离散 timeout event / counter abstraction，不得要求 clock constraint。
4. 对 `0018`，不要作为 T0 主线修复；如作为 stress，应显式记录 out-of-scope rationale。
5. 任何 R6 run 都必须保存 canonical baseline hash、candidate hash、change ledger、prompt、raw output、diagnostics、redaction 和 provider metadata；否则 R7 不得把它计入 Better 裁决 [src-r571][src-r572-better]。

### 7.2 给 R7 的提示

1. R7 eligibility 必须把 `scope_routing_status`、`run_validity_status`、`better_adjudication_outcome` 分层记录。
2. `T0=48 pairs` 仍只是 scope / pre-eligibility 上限，不是 success denominator。
3. target closure 必须按 `must_fix / should_fix / monitor / not_repair_target / out_of_scope` 分层，不允许单一总闭合率。
4. 正式 Better outcome 只能在 `STM_k`、change ledger、no-regression、semantic gate 和 reporting gate 全部闭合后产生。
5. R6/R7 前必须补齐或声明 `.fcstm` / canonical baseline evidence bundle：0001 / 0018 需要物化 standalone `.fcstm`；0000 / 0045 需要声明 selected smoke hash 是 authoritative baseline，seed-sweep hash 作为 audit trail，二者 hash 不同本身不是缺失 [clm-r574-fcstm-missing][clm-r574-fcstm-authority]。

## 8. 学术风险与禁止主张

1. 不把 R5.7.4 写成方法效果实验；它只验证评价协议与指标框架能否被真实样例消费 [clm-r574-boundary]。
2. 不把 representation symptom 直接写成 confirmed defect；0000 的 guard finding 也只是 dry-run target，不是正式 Better 结果 [clm-r574-0000]。
3. 不把 `0045` 升格为 timed automata 支持，不把 `0018` 混入 T0 headline [clm-r574-0045][clm-r574-0018]。
4. 不用 conversion、parse / inspect、loss count 或 `.fcstm` 成功证明 repair gain [clm-r574-no-repair-gain]。
5. 不隐藏 evidence bundle 风险：standalone `.fcstm` 缺口必须进入 R6/R7 handoff；selected-vs-seed hash 差异必须声明权威 baseline 与 audit trail，而不是误写成同类缺口 [clm-r574-fcstm-missing][clm-r574-fcstm-authority]。

## 9. 后续入口

| 后续阶段 | 应读取 | 继承内容 |
|---|---|---|
| R5.7.5 | 本报告与 [../experiment_design/repair_target_adjudication/](../experiment_design/repair_target_adjudication/) 四个样例文件 | 把 taxonomy、metric permission、evidence gap 合成 R6/R7 handoff。 |
| R6 | `0000` / `0001` / `0045` / `0018` 各自裁决文件 | 生成 feedback prompt / replay / fake run skeleton 时的 target 与 scope 约束。 |
| R7 | 本报告 §6--§7 | eligibility、metric column、target-instance ledger 与 denominator discipline。 |
| R8 | 本报告 §8 | limitation / stress / failure ledger 写法。 |

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告 | 当前 PR 提交 | `2026-07-03 23:44:12` | 首次冻结 R5.7.4 四例静态裁决、metric permission dry-run、R6/R7 handoff 和 `.fcstm` evidence gap。 | 后续链接、排版和入口同步不改变本报告 freeze time。 | [src-pairs]、[src-case]、[src-ledger]、[src-archive]。 |
| [../experiment_design/repair_target_adjudication/](../experiment_design/repair_target_adjudication/) 四例文件 | 当前 PR 提交 | `2026-07-03 23:44:12` | 为每个 pair 记录样例级 taxonomy、metric permission 与 claim-evidence map。 | 后续若替换样例或补正式 run，应新增文件或明确 supersede。 | 同上。 |
| [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md) | `feb0deef` | R5.7.1 freeze | 冻结 claim boundary、分母、A 层、归因边界。 | R5.7.4 只消费，不重写。 | Markdown 合同 + pipeline JSONL。 |
| [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) / [repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md) | R5.7.2 PR | R5.7.2 freeze | 冻结 G0--G6、三层输出、taxonomy、candidate-only 纪律。 | R5.7.4 只消费，不重写。 | Markdown 合同。 |
| [../experiment_design/metrics/objective_metric_framework.md](../experiment_design/metrics/objective_metric_framework.md) | R5.7.3 PR | R5.7.3 freeze | 冻结 metric permission、schema、anti-gaming、baseline migration。 | R5.7.4 只消费，不重写。 | Markdown 合同。 |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-r571] | `r571_evaluation_logic` | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md) | md | 评价逻辑链、claim boundary、分母、A 层、归因边界。 | §1--§10。 |
| [src-r572-better] | `r572_better_stm` | [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) | md | G0--G6、三层输出、semantic gate。 | §3--§13。 |
| [src-r572-tax] | `r572_repair_target_taxonomy` | [../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md) | md | repair target taxonomy、五级 `repair_action_allowed`。 | §1--§7。 |
| [src-r573] | `r573_metric_framework` | [../experiment_design/metrics/objective_metric_framework.md](../experiment_design/metrics/objective_metric_framework.md) | md | 五级 `metric_permission`、entry schema、anti-gaming。 | §2、§5、§8、§11。 |
| [src-pairs] | `llms_emp_pairs` | [../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl](../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl) | jsonl | 4 个样例的 `NL` 与 raw `STM_0`。 | row filters: `pair_id in {0000,0001,0045,0018}`；fields `nl_text`、`stm0_text`。 |
| [src-case] | `llms_emp_case_matrix` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | time level、structure family、conversion、parse / inspect、loss code、hash；60 pair denominator。 | row filters: `raw_pair_id in {0000,0001,0045,0018}`；global count `len=60`。 |
| [src-ledger] | `partial_attribution_ledger` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | jsonl | partial attribution、candidate-only、pipeline artifact。 | row filters: `raw_pair_id in {0000,0045,0018}`；0001 has no row。 |
| [src-archive] | `llms_emp_record_archive` | [../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip](../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip) | zip | record 级 status、loss count、canonical states/transitions、irrecoverable fields、hash。 | members `llms-emp-stm-subset__llms_emp_stm_results_*.json` for four ids。 |
| [src-selected] | `selected_seed_examples` | [../selected_seed_examples/README.md](../selected_seed_examples/README.md) | md / fcstm | selected smoke standalone `.fcstm` availability and authoritative-baseline caveat。 | dirs `llms-emp-gpt4o-hldcs`、`llms-emp-deepseek-microwave`；their `fcstm_meta.json` records `selected_fcstm_sha256` and `synchronized_from_fcstm_sha256`；no dirs for 0001/0018。 |
| [src-adjudication] | `r574_adjudication_docs` | [../experiment_design/repair_target_adjudication/README.md](../experiment_design/repair_target_adjudication/README.md) | md | 四例样例级静态裁决入口。 | 四个秒级样例文件。 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-r574-boundary] | `R574-C1` | R5.7.4 是静态裁决 / metric dry-run，不运行 LLM、不生成 `STM_k`、不报告 repair effectiveness。 | scope / prohibition | [src-r571] §1/§9；[src-r572-better] §13；[src-r573] §1/§5。 | [cmd-r574-doc-links] | high | 后续 R6/R7 才可能产生正式 run。 |
| [clm-r574-preflight] | `R574-C2` | 四例均有 committed `NL`、raw `STM_0`、case matrix 与 archive 证据，足够做 static dry-run。 | trace | [src-pairs] row filters；[src-case] row filters；[src-archive] four members。 | [cmd-r574-four-case-preflight] | high | preflight pass 不等于 formal valid run。 |
| [clm-r574-no-better] | `R574-C3` | 四例本轮 `run_validity_status` 均为 canonical `protocol_or_provenance_invalid`，`better_adjudication_outcome` 均为 canonical `unknown`，原因是 `not_evaluated_in_static_dry_run`。 | prohibition | [src-r572-better] G1/G2/G6；本报告 §3。 | [cmd-r574-four-case-preflight] | high | 静态 taxonomy finding 可保留。 |
| [clm-r574-0000] | `R574-C4` | 0000 可形成 T0 `guard_condition -> should_fix` dry-run finding；representation lowering 仍 monitor。 | decision | [src-pairs] row `0000` NL/raw；[src-case] `r5_loss_codes`；[src-ledger] `r5_7_candidate_only=true`。 | [cmd-r574-four-case-preflight] | medium | 没有 `STM_k`，不能判 Better。 |
| [clm-r574-0001] | `R574-C5` | 0001 是 no-target / low-noise control；不应凭空制造 repair target。 | decision | [src-case] row `0001` `r5_loss_codes=[]`；[src-ledger] no row；[src-pairs] raw FSM。 | [cmd-r574-four-case-preflight] | high | 未来 R6 若产生改动，需要另行审计 over-repair。 |
| [clm-r574-0045] | `R574-C6` | 0045 是 T0.5 timer-like caveat；normalization replay 不计 repair gain。 | scope / decision | [src-pairs] row `0045` timer cues；[src-case] T0.5 / partial；[src-ledger] `pipeline_artifact`；[src-archive] `loss_count=7`。 | [cmd-r574-four-case-preflight] | high | 只支持 discrete event / counter caveat，不支持 timed automata。 |
| [clm-r574-0018] | `R574-C7` | 0018 是 T1 stress / out-of-headline；不得进入 T0 Better 主比较。 | scope / decision | [src-pairs] row `0018`; [src-case] T1; [src-archive] `blocked_transitions_count=1` / irrecoverable field。 | [cmd-r574-four-case-preflight] | high | 可用于 limitation / stress 表。 |
| [clm-r574-metric] | `R574-C8` | R5.7.3 指标在四例中只能按 hard_gate / supporting / trigger / report-only / forbidden 权限使用，不能 metric-only 判 Better。 | protocol | [src-r573] §2--§11；本报告 §6。 | [cmd-r574-doc-links] | high | R7 才冻结 final metrics / thresholds。 |
| [clm-r574-fcstm-missing] | `R574-C9a` | 0001 / 0018 缺 standalone `.fcstm`；R6/R7 前需物化 baseline evidence bundle。 | risk / handoff | [src-selected]；[src-case] `fcstm_sha256`。 | [cmd-r574-fcstm-gap] | high | 不阻塞本轮静态 dry-run。 |
| [clm-r574-fcstm-authority] | `R574-C9b` | 0000 / 0045 selected snapshot hash 与 seed-sweep hash 不同是预期差异；R6/R7 前需声明 authoritative baseline hash，seed-sweep hash 作 audit trail。 | risk / handoff | [src-selected] `selected_fcstm_sha256` / `synchronized_from_fcstm_sha256`；[src-case] seed-sweep `fcstm_sha256`。 | [cmd-r574-fcstm-gap] | high | 不应把该差异误写成缺失或修复问题。 |
| [clm-r574-no-repair-gain] | `R574-C10` | conversion / normalization / `.fcstm` parse inspect 只能支撑 readiness，不计 repair gain。 | prohibition | [src-r571] §6；[src-case] `repair_contribution_allowed=false`；[src-archive] `conversion_attribution` / `representation_attribution`。 | [cmd-r574-four-case-preflight] | high | 仍可作为 R6/R7 实验介质准备证据。 |

### A.4 复验命令

```bash
# [cmd-r574-doc-links]
python - <<'PY'
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair')
for rel in [
    'experiment_design/evaluation_logic.md',
    'experiment_design/quality_model/better_stm_definition.md',
    'experiment_design/quality_model/repair_target_taxonomy.md',
    'experiment_design/metrics/objective_metric_framework.md',
    'experiment_design/repair_target_adjudication/README.md',
    'reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md',
]:
    p = base / rel
    print(rel, p.exists(), p.stat().st_size if p.exists() else 'missing')
PY
```

```bash
# [cmd-r574-four-case-preflight]
python - <<'PY'
import json, pathlib, collections, zipfile
base = pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
ids = ['llms_emp_stm_results_0000','llms_emp_stm_results_0001','llms_emp_stm_results_0045','llms_emp_stm_results_0018']
case = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
pairs = [json.loads(l) for l in (base/'corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl').read_text().splitlines() if l.strip()]
ledger = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl').read_text().splitlines() if l.strip()]
print('all_pairs', len(case), collections.Counter(r['time_level'] for r in case), collections.Counter(r['conversion_status'] for r in case))
for rid in ids:
    c = next(r for r in case if r['raw_pair_id'] == rid)
    p = next(r for r in pairs if r['pair_id'] == rid)
    rows = [r for r in ledger if r['raw_pair_id'] == rid]
    print(rid, c['time_level'], c['structure_family'], c['conversion_status'], c['parse_status'], c['inspect_status'], c['r5_loss_codes'], bool(p['nl_text']), bool(p['stm0_text']), 'ledger_rows', len(rows))
zip_path = base/'pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip'
with zipfile.ZipFile(zip_path) as z:
    for rid in ids:
        member = f'llms-emp-stm-subset_records/llms-emp-stm-subset__{rid}.json'
        rec = json.loads(z.read(member).decode())
        print('archive', rid, rec['status'], rec['loss_count'], rec['canonical_states_count'], rec['canonical_transitions_count'], rec['fcstm_sha256'])
PY
```

```bash
# [cmd-r574-fcstm-gap]
python - <<'PY'
from pathlib import Path
import json
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair')
case = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
selected_map = {
    'llms_emp_stm_results_0000': 'selected_seed_examples/llms-emp-gpt4o-hldcs/fcstm_meta.json',
    'llms_emp_stm_results_0045': 'selected_seed_examples/llms-emp-deepseek-microwave/fcstm_meta.json',
}
for rid, rel in selected_map.items():
    data = json.loads((base/rel).read_text())
    seed = next(r for r in case if r['raw_pair_id'] == rid)['fcstm_sha256']
    print(rid, 'selected', data['selected_fcstm_sha256'], 'synchronized_from', data['synchronized_from_fcstm_sha256'], 'seed_sweep', seed, 'same_as_seed', data['selected_fcstm_sha256'] == seed)
for rid, rel in [
    ('llms_emp_stm_results_0000', 'selected_seed_examples/llms-emp-gpt4o-hldcs/model.fcstm'),
    ('llms_emp_stm_results_0045', 'selected_seed_examples/llms-emp-deepseek-microwave/model.fcstm'),
    ('llms_emp_stm_results_0001', 'selected_seed_examples/llms-emp-gpt4o-hstbs/model.fcstm'),
    ('llms_emp_stm_results_0018', 'selected_seed_examples/llms-emp-gpt4-digital-camera/model.fcstm'),
]:
    print(rid, rel, (base/rel).exists())
PY
```
