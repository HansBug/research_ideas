# llms-emp 0018 / Digital Camera / GPT-4：T1 supplementary stress 裁决 dry-run

> 证据引用说明：正文中的 `[src-*]`、`[clm-*]`、`[cmd-*]` 是文末审计附录稳定 key，不按数字重排。本文是 R5.7.4 静态 dry-run，不是正式 repair run。

## 1. 样例定位

| 字段 | 值 |
|---|---|
| pair id | `llms_emp_stm_results_0018` |
| cluster | `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr` |
| system / LLM | DCS / digital camera state machine / GPT-4 |
| scope routing | `stress_t1` |
| time level / structure | `T1` / `UML-SysML statechart` |
| conversion / canonical / parse / inspect | `partial` / `converted` / `ok` / `ok` |
| canonical states / transitions | 21 / 21 |
| static dry-run preflight | `pass`：`NL`、raw `STM_0`、case matrix、record archive 足够支撑静态裁决 [src-pairs][src-case][src-archive] |
| run_validity_status | `protocol_or_provenance_invalid` [clm-formal-invalid] |
| run_validity_reason | `static_dry_run_without_stmk_change_ledger_or_run_record`：本轮没有 `STM_k`、change ledger 或 run record。 |
| better_adjudication_outcome | `unknown` [clm-no-better] |
| better_outcome_reason | `not_evaluated_in_static_dry_run`；不得写 `better`。 |

## 2. 输入证据：NL / raw `STM_0` / canonical-loss-fcstm

### 2.1 `NL` 关键片段

包含 max/min seconds、fork / join / choice、`memFull=true`、`prob=0.4`、`sunny=true` 等 timing 与 UML control-flow stress 特征。 [src-pairs]

### 2.2 raw `STM_0` 关键片段

```plantuml
[*] --> TurnOn : 2 sec
AutoFocus -down-> choice1 : memFull=true
DetLight -down-> choice2 : <<GaStep>>{prob=0.4}
choice2 --> Join1 when : sunny=true
```

上述片段只用于说明 source evidence；R5.7.4 不把 raw -> canonical 的表示收益计入 repair gain [src-eval-logic][clm-no-repair-gain]。

### 2.3 case matrix 与 archive 证据

| 项 | 证据 |
|---|---|
| loss codes | `R45.LOSS.condition_like_label_lowered_as_event`、`R45.LOSS.cross_scope_transition_unrepresentable`、`R45.LOSS.initial_inferred_from_source_order_or_start_state`、`R45.LOSS.source_lifted_to_composite_boundary`、`R5.LOSS.r3_1_normalization_replay_not_repair`；archive 中 `loss_count=15`、`blocked_transitions_count=1`。 [src-case][src-archive] |
| attribution ledger | partial ledger 有 `primary_attribution=r5_7_candidate_only`，同时 `pipeline_artifact=true`；archive 记录 `irrecoverable_fields=[llms_emp_stm_results_0018.scxml:scxml/state[7]/state[2]/transition[1]]`。 [src-ledger] |
| seed-sweep `fcstm_sha256` | `6b57f2672a826f9ef533d39d76bb5cd3c5c15f643b98740159f045d1438a2963` [src-case][src-archive] |
| standalone `.fcstm` 状态 | 当前未找到 standalone `.fcstm` 文本；seed-sweep record 只有 `fcstm_sha256=6b57...`、parse ok、inspect ok、archive metadata 与 irrecoverable field。R6/R7 前必须物化 baseline evidence bundle。 [src-selected] |

## 3. R5.7.2 taxonomy 裁决

本节同时保留一行叙述性 summary 和实例级 target ledger。实例级 ledger 每行只表示一个 target instance，`repair_action_allowed` 必须是 R5.7.2 单值枚举。 [src-taxonomy]

**叙述性 summary**：`0018` 的 timing、fork/choice、cross-scope 与 condition-like labels 适合作为 T1 stress / limitation，不进入 T0 Better 主比较。 [clm-taxonomy]

| target_instance_id | target_id | semantic_element | scope_status | scope_routing_status | time_level | structure_family | nl_evidence_required | representation_evidence_required | repair_action_allowed | repair_action_override_reason | better_stm_condition_impact | conversion_artifact_risk | metric_permission | forbidden_extrapolation | r6_feedback | r7_implication | caveat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `r574-0018-out-of-scope-family` | `out_of_scope_family` | `out_of_scope_family` | `supplementary_stress` | `stress_t1` | `T1+` | `excluded family` | conditional：只需支撑 stress rationale。 | source artifact + scope rationale + archive blocked transition。 | `out_of_scope` | T1 stress retained for limitation/stress analysis，但不进入 main target。 | G0=stress_t1；G1=not_applicable_to_better_main_comparison；G2=not_applicable_to_better_main_comparison；G3=not_applicable_to_better_main_comparison；G4=not_applicable_to_better_main_comparison；G5=not_applicable_to_better_main_comparison；G6=not_applicable_to_better_main_comparison。 | high | `report_only`。 | 不得进入 main repair target、T0 denominator 或 method success。 | R6 不应作为 T0 主线修复。 | R7 只作为 stress / limitation 行。 | out-of-headline。 |
| `r574-0018-condition-like-stress-trigger` | `guard_condition` | `guard_condition` | `supplementary_stress` | `stress_t1` | `T1+` | `excluded family` | yes for stress trigger；不足以支持 T0 target。 | raw label + loss ledger + archive；无 formal change ledger。 | `monitor` | 类级 `guard_condition` 默认 `should_fix`，但该实例因 T1/stress scope 降级为 monitor。 | G0=stress_t1；G1=`cannot_evaluate`；G2=caveat attribution；G3=not_applicable_to_t0_headline；G4=not_applicable_to_t0_headline；G5=not_applicable_to_t0_headline；G6=caveat/reporting_only。 | high | `trigger_only` / `report_only`。 | 不得把 stress trigger 写成 T0 guard target success。 | 仅作为 R6 stress prompt 风险提示。 | R7 不计 target closure success。 | candidate-only in stress scope。 |
| `r574-0018-representation-artifact` | `representation_only_conversion_artifact` | `representation_artifact` | `supplementary_stress` | `stress_t1` | `T1+` | `excluded family` | no。 | conversion ledger + loss ledger + archive metadata。 | `monitor` | 与类级默认一致，但处于 stress scope。 | G0=stress_t1/not_positive_target；G1=`cannot_evaluate`；G2=caveat attribution；G3=not_applicable_without_repair_candidate；G4=not_applicable_to_positive_target；G5=not_applicable_to_positive_target；G6=caveat/reporting_only。 | high | `report_only`。 | 不得把 conversion/lowering 计为 repair gain。 | 只记录 evidence / representation risk。 | R7 作为 limitation evidence。 | readiness evidence only。 |

因此，本样例在 R5.7.4 中只输出 `dry_run_taxonomy_finding`，不输出正式 `better_adjudication_outcome=better` [clm-no-better]。

## 4. R5.7.3 metric permission dry-run

| 指标 / 证据 | 权限 | 用途 | 禁止外推 |
|---|---|---|---|
| schema / parse / inspect / evidence bundle | `hard_gate` | 判断是否可继续做静态或正式评价 | 不证明语义更好 |
| loss code / conversion status | `report_only` 或 `trigger_only` | 暴露 representation risk | 不计 repair gain |
| 本样例关键指标 | 见裁决说明 | parse / inspect 可作 hard gate；cross-scope 与 folding 风险为 `trigger_only`；T1 timing / probability / fork-join 相关统计只能 `report_only` / stress，不进入 Better quality comparison。 | 不能 metric-only 判 Better |
| change ledger presence | `hard_gate` for formal Better | 本轮缺失，阻断正式 Better run | 不得把静态 finding 当正式 run |

## 5. R6 feedback implication

R6 不应把此例作为 T0 主线修复目标；若用于 stress，应单独标记 out-of-scope rationale，并避免让反馈 prompt 要求 timed / probabilistic / arbitrary UML 支持。 [clm-r6]

## 6. R7 eligibility / metric implication

R7 可把此例用于 limitation / stress 表，记录 `blocked_transitions_count=1` 与 irrecoverable field；不得进入 T0 success denominator。 [clm-r7]

## 7. 未决项与禁止主张

1. 本轮未生成 `STM_k`，因此不能写正式 `valid_run`、`better` 或 repair effectiveness [clm-formal-invalid][clm-no-better]。
2. `.fcstm` / parse / inspect 只证明表示桥可审计；不能写成 repair gain [clm-no-repair-gain]。
3. 若后续 R6/R7 使用该例，必须重新物化或校验 baseline evidence bundle、candidate hash、change ledger、trace / scenario / semantic gate 证据 [clm-r7]。
4. 本样例的综合结论另见 R5.7.4 总报告 [2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](../../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md)。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件 | 当前 PR 提交 | `2026-07-03-23-44-12` | 首次为 `llms_emp_stm_results_0018` 写入 R5.7.4 静态裁决、metric permission dry-run 与 R6/R7 handoff。 | 后续链接 / 排版修正不改变 freeze time。 | [src-pairs]、[src-case]、[src-ledger]、[src-archive]。 |
| [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) | R5.7.2 PR | R5.7.2 freeze | 提供 G0--G6 gate、三层输出和 semantic gate。 | R5.7.4 只消费，不重写。 | Markdown 合同。 |
| [../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md) | R5.7.3 PR | R5.7.3 freeze | 提供五级 metric permission 与 anti-gaming 规则。 | R5.7.4 只消费，不重写。 | Markdown 合同。 |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-pairs] | `llms_emp_pairs` | [../../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl](../../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl) | jsonl | `NL` 与 raw `STM_0` 一手证据。 | row filter: `pair_id=llms_emp_stm_results_0018`；fields `nl_text`、`stm0_text`、`source_locator`。 |
| [src-case] | `llms_emp_case_matrix` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | time level、structure family、conversion / parse / inspect、loss codes、hash。 | row filter: `raw_pair_id=llms_emp_stm_results_0018`。 |
| [src-ledger] | `partial_attribution_ledger` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | jsonl | partial attribution、candidate-only、pipeline artifact。 | row filter: `raw_pair_id=llms_emp_stm_results_0018`。 |
| [src-archive] | `llms_emp_record_archive` | [../../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip](../../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip) | zip | record 级 status、loss count、canonical counts、hash、irrecoverable fields。 | member `llms-emp-stm-subset_records/llms-emp-stm-subset__llms_emp_stm_results_0018.json`。 |
| [src-selected] | `selected_seed_examples` | [../../selected_seed_examples/README.md](../../selected_seed_examples/README.md) | md / fcstm | standalone `.fcstm` snapshot availability caveat。 | selected directories for 0000 / 0045 only；0001 / 0018 only hash/status in archive。 |
| [src-eval-logic] | `r571_evaluation_logic` | [../evaluation_logic.md](../evaluation_logic.md) | md | claim boundary、分母、A gate、conversion 不计 repair gain。 | §1--§10。 |
| [src-better] | `r572_better_stm` | [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) | md | G0--G6、三层输出、semantic gate。 | §3--§5、§11--§13。 |
| [src-taxonomy] | `r572_repair_target_taxonomy` | [../quality_model/repair_target_taxonomy.md](../quality_model/repair_target_taxonomy.md) | md | 修复目标 taxonomy 与 `repair_action_allowed`。 | §1--§7。 |
| [src-metrics] | `r573_metric_framework` | [../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md) | md | 五级 `metric_permission` 与 anti-gaming。 | §2、§5、§8、§11。 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-formal-invalid] | `R574-0018-C1` | 本样例本轮不能写正式 `valid_run`，因为没有 `STM_k` / change ledger / run record。 | protocol | [src-better] G1/G2/G6；本文件 §1。 | [cmd-r574-0018] | high | static preflight pass 不等于 formal run valid。 |
| [clm-no-better] | `R574-0018-C2` | 本样例不能写 `better` 或 repair effectiveness；better_adjudication_outcome 是 canonical `unknown`，原因是 `not_evaluated_in_static_dry_run`。 | prohibition | [src-eval-logic]、[src-better]；本文件 §1、§7。 | [cmd-r574-0018] | high | R6/R7 真实 run 后可重新裁决。 |
| [clm-no-repair-gain] | `R574-0018-C3` | conversion / normalization / `.fcstm` / parse / inspect 只能支撑 readiness，不计 repair gain。 | prohibition | [src-eval-logic] §6；[src-case] / [src-archive] `repair_contribution_allowed=false`。 | [cmd-r574-0018] | high | 不否认它们对实验介质有用。 |
| [clm-taxonomy] | `R574-0018-C4` | 本样例的 static taxonomy finding 如 §3 所述。 | decision | [src-pairs]、[src-case]、[src-ledger]、[src-taxonomy]。 | [cmd-r574-0018] | medium | 没有 `STM_k`，所以只是 target / caveat finding，不是 Better 裁决。 |
| [clm-r6] | `R574-0018-C5` | 本样例的 R6 feedback implication 如 §5 所述。 | handoff | [src-taxonomy]、[src-metrics]、本文件 §5。 | 人工复验 | medium | R6 实现时需转成 prompt / run record 字段。 |
| [clm-r7] | `R574-0018-C6` | 本样例的 R7 eligibility / metric implication 如 §6 所述。 | handoff | [src-better]、[src-metrics]、本文件 §6。 | 人工复验 | medium | R7 才冻结最终 denominator / endpoint。 |

### A.4 复验命令

```bash
# [cmd-r574-0018]
python - <<'PY'
import json, pathlib, zipfile
base = pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
rid = 'llms_emp_stm_results_0018'
case = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
pairs = [json.loads(l) for l in (base/'corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl').read_text().splitlines() if l.strip()]
ledger = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl').read_text().splitlines() if l.strip()]
print('case', next(r for r in case if r['raw_pair_id'] == rid))
print('pair_nl_stm_present', bool(next(r for r in pairs if r['pair_id'] == rid)['nl_text']), bool(next(r for r in pairs if r['pair_id'] == rid)['stm0_text']))
print('ledger_rows', [r for r in ledger if r['raw_pair_id'] == rid])
zip_path = base/'pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip'
with zipfile.ZipFile(zip_path) as z:
    member = f'llms-emp-stm-subset_records/llms-emp-stm-subset__{rid}.json'
    rec = json.loads(z.read(member).decode())
    print('archive_status', rec['status'], rec['loss_reason_codes'], rec['fcstm_sha256'])
PY
```
