# R5.7.2 Better STM 判定与修复目标分类合同报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与问题

R5.7.2 解决的问题是：当后续 repair loop 真的产生候选 `STM_k` 时，什么样的证据足以说明它相对同一个 canonical `STM_0` 是 **Better STM**；什么情况即使 parse / inspect / scenario / 指标更好，也必须判为 `not_better`、`partial`、`unknown` 或协议无效 [clm-r572-no-effect]。

本报告不是 repair-loop 结果，不包含真实 `STM_k`，不报告成功率，也不把转换器、`.fcstm`、`pyfcstm` 或 taxonomy 本身写成论文贡献 [clm-r572-no-effect][clm-r572-medium-only]。长期规则真源已经落在 [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) 与 [../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md)，本报告只作为人类阅读 handoff [src-better][src-taxonomy]。

## 2. 核心结论

| 主题 | R5.7.2 冻结结论 | 证据键 |
|---|---|---|
| Better 比较对象 | raw `STM_0` 是 source evidence；直接比较对象是 canonical `STM_0` vs `STM_k`。 | [clm-r572-raw-role] |
| repair gain 起点 | raw -> canonical 只计 readiness / conversion bridge；repair gain 从 canonical `STM_0 -> STM_k` 开始。 | [clm-r572-raw-role] |
| gate 链 | Better STM 必须通过 G0 scope、G1 A gate、G2 attribution、G3 no-regression、G4 improvement、G5 semantic、G6 reporting。 | [clm-r572-gate-chain] |
| 输出模型 | 不用扁平 verdict；采用 `scope_routing_status`、`run_validity_status`、`better_adjudication_outcome` 三层输出。 | [clm-r572-outcome] |
| taxonomy | 冻结 11 类 target、11 字段合同、五级 `repair_action_allowed`。 | [clm-r572-taxonomy] |
| candidate-only | `condition_like_label_lowered_as_event` 等 representation symptom 不能直接升级为 confirmed defect。 | [clm-r572-candidate-only] |
| T0.5 / T1 | T0.5 tick/counter 可作 caveat 层讨论；T1 不进入 Better 主裁决。 | [clm-r572-t05] |
| 指标权限 | objective metrics 只作 supporting evidence，不能 metric-only verdict。 | [clm-r572-metrics] |
| 修订纪律 | 后续规则 / 指标修订必须由真实 dry-run findings 驱动；无 finding 的修订只能标 provisional。 | [clm-r572-revision] |

## 3. Better STM 判定链

R5.7.2 将旧版“Better STM 五条件”扩展为七道 gate [clm-r572-gate-chain]：

```text
NL + raw STM_0 + canonical STM_0 + STM_k + ledgers + diagnostics + scenarios + rubric
  -> G0 scope routing
  -> G1 A gate
  -> G2 attribution gate
  -> G3 no-regression gate
  -> G4 improvement gate
  -> G5 semantic gate
  -> G6 reporting gate
  -> scope_routing_status / run_validity_status / better_adjudication_outcome
```

这条链路的要点不是“多设几个表格字段”，而是堵住三类学术风险：

1. **归因洗白**：把 conversion / normalization / `.fcstm` parse success 写成 repair-loop gain [clm-r572-raw-role]。
2. **指标洗白**：把 diagnostics fewer、scenario pass、F1 更高写成 Better STM [clm-r572-metrics]。
3. **分母洗白**：把 failure / partial / unknown / protocol invalid 从主表中删掉，只报告成功样例 [clm-r572-outcome]。

## 4. 三层输出模型

R5.7.2 采用三层输出，而不是一个扁平状态字段 [clm-r572-outcome]。

| 层 | 字段 | 值 | 学术意义 |
|---|---|---|---|
| scope | `scope_routing_status` | `main_t0` / `caveat_t05` / `stress_t1` / `excluded_out_of_scope` | 决定样例是否可进入 T0 headline、caveat、stress 或 excluded。 |
| run validity | `run_validity_status` | `valid_run` / `stm0_readiness_failure` / `stmk_repair_failure` / `protocol_or_provenance_invalid` | 判断该 run 是否有资格进入 Better semantic adjudication。 |
| Better outcome | `better_adjudication_outcome` | `better` / `not_better` / `partial` / `unknown` | 只对有效 run 裁决相对改善。 |

关键调整是：不再把 `not_attributable` 当作常规 Better outcome。不可归因意味着协议或 provenance 失效，应进入 `protocol_or_provenance_invalid` 或 attribution ledger，而不是和 `not_better` / `unknown` 混在一起 [clm-r572-outcome]。

## 5. 修复目标 taxonomy v0

R5.7.2 冻结的 taxonomy 有 11 类一级目标 [clm-r572-taxonomy]：

| target_id | 核心对象 | 默认角色 |
|---|---|---|
| `state_structure` | 状态缺失、冗余、命名 / 边界错误。 | T0 main target。 |
| `transition_structure` | 迁移源、目标、连通性、删除 / 新增。 | T0 main target。 |
| `event_trigger` | 触发事件覆盖与一致性。 | T0 main target / monitor。 |
| `guard_condition` | 条件、布尔表达式、变量比较。 | T0 main candidate；需 NL 证据。 |
| `action_effect` | 输出、赋值、显示、计数器更新等效果。 | T0 main candidate；需 NL 证据。 |
| `hierarchy_pseudostate` | HSM 层级、choice/junction/initial/final、pseudo-state relay。 | T0 main target / monitor。 |
| `traceability_grounding` | 元素到 `NL` / raw label 的 trace。 | T0 main target。 |
| `scenario_behavioral_obligation` | 场景与行为义务。 | T0 main target。 |
| `temporal_cue_tick_counter_caveat` | timer-like cue / tick / discrete counter。 | T0.5 caveat。 |
| `representation_only_conversion_artifact` | conversion / lowering / loss ledger artifact。 | monitor / not repair target。 |
| `out_of_scope_family` | timed / hybrid / arbitrary UML / protocol FSM。 | out-of-scope。 |

每条 entry 必须带 11 个字段：`target_id`、`semantic_element`、`scope_status`、`time_level`、`structure_family`、`nl_evidence_required`、`representation_evidence_required`、`repair_action_allowed`、`better_stm_condition_impact`、`conversion_artifact_risk`、`forbidden_extrapolation` [clm-r572-taxonomy]。

## 6. 代表性例子

这些例子只用于解释规则，不是 R5.7.4 正式 dry-run，也不是 repair 效果证据 [clm-r572-no-effect]。

| 例子 | 初始判定 | 为什么不能直接定性 | R5.7.2 处理 |
|---|---|---|---|
| `Front Distance > 10` 被 lowering 为 event label | guard candidate | 需要看 `NL` 是否把它写成条件，raw `STM_0` 是否是条件式。 | confirmed 后才可 `should_fix` / `must_fix`；否则 monitor。 |
| `dist_to_front<25 && extra_lane=true` | strong guard candidate | 字符串像 guard，但仍需 NL 与 raw 证据。 | 可作为 R5.7.4 重点 dry-run；不能批量判 defect。 |
| `lane change completed` | 多数情况下是 trigger event | 完成事件也可能被误读为 action/effect。 | 默认保留 event，除非 NL 明确它是效果或目标状态。 |
| `show error` / `print bill` | action/effect cue | 可能是系统输出，也可能只是标签文本。 | 需 NL-grounded 裁决后再拆 action/effect。 |
| `Timer Expired` | timeout event 或 T0.5 cue | timeout event 与周期 tick / clock constraint 不同。 | 离散 event 可保留；tick/counter 进 T0.5 caveat；T1 out-of-scope。 |


## 7. 文档级 mini dry-run

以下 mini dry-run 只验证 R5.7.2 合同是否能指导判断，不是 R5.7.4 正式静态 dry-run，也不是 repair 效果证据 [clm-r572-no-effect]。

| 场景 | 输入现象 | 按 R5.7.2 应如何判 | 为什么 |
|---|---|---|---|
| guard/action/event 折叠 | `STM_k` parse ok，且 scenario 局部通过，但把 `dist_to_front<25 && extra_lane=true` 留在 event label。 | 不能直接判 Better；先进入 `guard_condition` candidate，若 NL/raw 证据确认应为 guard，则 G5 semantic gate 负向，输出 `not_better` 或 `partial`。 | parse / scenario 不能覆盖语义折叠；representation symptom 需要 NL + raw 证据裁决 [clm-r572-candidate-only][clm-r572-metrics]。 |
| 删除行为换取场景通过 | `STM_k` 删除一个 NL 明示的异常处理迁移，因此当前冻结场景 pass rate 提高。 | G3 no-regression 或 G5 semantic gate 失败；输出 `not_better` / `stmk_repair_failure`，不得计 Better。 | 场景通过率只是局部证据，不能通过删除需求行为刷指标 [clm-r572-gate-chain][clm-r572-metrics]。 |
| T0.5 tick/counter | microwave 类样例含“周期 tick / timeout / reset timer”线索，可降级为离散 counter。 | `scope_routing_status=caveat_t05`；可作 caveat 层 partial / monitor / should-fix 讨论，但不进入 T0 headline Better success。 | T0.5 与 T1 分开；T0.5 不是 timed automata claim [clm-r572-t05]。 |

## 8. 下游接口

| 阶段 | 必须继承什么 | 不能做什么 |
|---|---|---|
| R5.7.3 | 指标只能 supporting evidence；需定义指标族、偏序方向、适用边界、刷指标风险。 | 不能把 metric-only verdict 写成 Better。 |
| R5.7.4 | 用 3–5 个真实 / 准真实样例 dry-run gate 与 taxonomy，并记录 findings ledger。 | 不能把 dry-run 写成 repair effectiveness。 |
| R5.7.5 | 合成 R6/R7 handoff：gate、taxonomy、metrics、dry-run findings。 | 不能无证据修改 v0 合同。 |
| R6 | 实现 fake / replay repair loop skeleton 和 run record。 | 不能把 pre-repair normalization 当修复步骤。 |
| R7/R8 | 正式协议、真实 run、change ledger、semantic adjudication、failure ledger。 | 不能让失败、partial、unknown、protocol invalid 从分母消失。 |

## 9. 学术风险与禁止主张

1. 不写 R5.7.2 已证明 repair loop 有效 [clm-r572-no-effect]。
2. 不写 taxonomy target 已经是 confirmed defect 统计 [clm-r572-candidate-only]。
3. 不写 T0.5 支持 timed automata、clock constraints 或 real-time verification [clm-r572-t05]。
4. 不写 pyfcstm / fcstm 是本文贡献；它们只是实验介质 [clm-r572-medium-only]。
5. 不用 parse ok、inspect ok、scenario pass、diagnostics fewer、F1、文本相似度或 token cost 单独证明 Better STM [clm-r572-metrics]。
6. 不把 raw -> canonical 的 conversion recovery、normalization 或 lowering 写成 repair-loop gain [clm-r572-raw-role]。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md` | `df4af008` | `df4af008` | R5.7.2 首次落库 Better STM gate、taxonomy、Q1–Q12 决策 synthesis 与下游接口。 | 本次回填提交 | [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md)、[../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md) |

> 本节只说明 report 的迁移与冻结来源，不替代下面的 claim-evidence map。本 report 的首次内容提交为 `df4af008`；本次后续提交只回填来源 commit，不改变核心学术结论。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-eval-logic] | `r571_evaluation_logic` | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md) | md | R5.7.1 claim boundary、分母、A 层、归因、指标位置。 | §2–§10。 |
| [src-better] | `r572_better_stm_definition` | [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) | md | R5.7.2 Better STM gate、三层输出、硬拒绝、T0.5、semantic gate。 | §1–§12。 |
| [src-taxonomy] | `r572_repair_target_taxonomy` | [../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md) | md | 11 类 target、11 字段、五级 `repair_action_allowed`、candidate-only 纪律。 | §1–§7。 |
| [src-r56-handoff] | `r56_to_r57_handoff` | [../experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](../experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md) | md | taxonomy 最低字段、T0/T0.5/T1、candidate-only。 | §1–§5。 |
| [src-model-scope] | `r56_model_scope` | [../story/model_scope.md](../story/model_scope.md) | md | 状态机抽象、模型族、时间等级和 forbidden extrapolation。 | §2–§6。 |
| [src-case] | `llms_emp_case_matrix` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | 10×6 denominator、time level、conversion/readiness 当前事实。 | JSONL rows；`nl_cluster_id`、`time_level`、`conversion_status`。 |
| [src-q1] | `r572_q1` | [PR #140 Q1 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868188123) | github-comment | raw/canonical/STM_k 角色决策。 | comment 全文。 |
| [src-q2] | `r572_q2` | [PR #140 Q2 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868298209) | github-comment | G0–G6 gate 决策。 | comment 全文。 |
| [src-q4] | `r572_q4` | [PR #140 Q4 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868521779) | github-comment | 三层输出模型决策。 | comment 全文。 |
| [src-q5] | `r572_q5` | [PR #140 Q5 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868584922) | github-comment | taxonomy 11 类 / 11 字段 / 五级 action。 | comment 全文。 |
| [src-q6] | `r572_q6` | [PR #140 Q6 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868834329) | github-comment | guard/event/action folding 与 combo syntax。 | comment 全文。 |
| [src-q7] | `r572_q7` | [PR #140 Q7 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868890452) | github-comment | T0.5 tick/counter caveat 与 T1 out-of-scope。 | comment 全文。 |
| [src-q8] | `r572_q8` | [PR #140 Q8 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868946209) | github-comment | pair / cluster 报告。 | comment 全文。 |
| [src-q9] | `r572_q9` | [PR #140 Q9 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868983703) | github-comment | objective metrics 角色。 | comment 全文。 |
| [src-q10] | `r572_q10` | [PR #140 Q10 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4869021866) | github-comment | semantic adjudication / LLM-as-Judge / human role。 | comment 全文。 |
| [src-q12] | `r572_q12` | [PR #140 Q12 comment](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4869119301) | github-comment | 下游接口和 evidence-driven revision。 | comment 全文。 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-r572-no-effect] | `R572-C1` | R5.7.2 不运行 repair loop、不生成 `STM_k`、不报告 Better STM 成功率或 repair effectiveness。 | prohibition | [src-eval-logic] §1/§9；[src-better] 定位段。 | 人工复验 + [cmd-r572-doc-links] | high | 后续 R6/R7/R8 才能产生效果证据。 |
| [clm-r572-raw-role] | `R572-C2` | raw `STM_0` 是 source evidence；Better 直接比较对象是 canonical `STM_0` vs `STM_k`，repair gain 从 canonical 起算。 | decision | [src-q1]；[src-better] §2；[src-eval-logic] §6。 | 人工复验 | high | raw 仍必须用于语义裁决和转换归因。 |
| [clm-r572-gate-chain] | `R572-C3` | Better STM 判定采用 G0–G6 gate 链。 | decision | [src-q2]；[src-better] §3。 | 人工复验 | high | R5.7.4 可据 dry-run findings 提出 v1 修订。 |
| [clm-r572-outcome] | `R572-C4` | R5.7.2 采用三层输出模型，且不可归因属于 protocol/provenance invalid。 | decision | [src-q4]；[src-better] §4。 | 人工复验 | high | 最终 schema 由 R7/R8 冻结。 |
| [clm-r572-taxonomy] | `R572-C5` | repair target taxonomy v0 包含 11 类、11 字段与五级 `repair_action_allowed`。 | contract | [src-q5]；[src-taxonomy] §2–§3。 | [cmd-r572-taxonomy-fields] | high | 后续可新增子类，但不能删除最低字段。 |
| [clm-r572-candidate-only] | `R572-C6` | representation symptom 不能直接升级为 confirmed defect。 | prohibition | [src-r56-handoff] §2/§5；[src-taxonomy] §1/§4。 | 人工复验 | high | R5.7.4/R7 可逐例确认。 |
| [clm-r572-t05] | `R572-C7` | T0.5 tick/counter 只能 caveat 处理；T1 只作 stress / limitation。 | scope | [src-q7]；[src-model-scope]；[src-better] §7。 | 人工复验 | high | 不支持 timed automata claim。 |
| [clm-r572-metrics] | `R572-C8` | objective metrics 只能 supporting evidence，不能 metric-only verdict。 | prohibition | [src-q9]；[src-better] §9；[src-eval-logic] §7。 | 人工复验 | high | R5.7.3 仍需定义指标族和偏序。 |
| [clm-r572-revision] | `R572-C9` | 后续规则 / 指标修订必须由真实 dry-run findings 驱动。 | protocol | [src-q12]；[src-better] §9/§12。 | 人工复验 | high | 无 finding 的修订只能标 provisional。 |
| [clm-r572-medium-only] | `R572-C10` | `.fcstm` / `pyfcstm` / converter 是实验介质，不是论文核心贡献。 | prohibition | [src-model-scope]；[src-better] §2/§6。 | 人工复验 | high | 代码实现仍可依赖 pyfcstm，但写作要弱化。 |

### A.4 复验命令

```bash
# [cmd-r572-doc-links]
python - <<'PY'
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair')
for rel in [
    'experiment_design/quality_model/better_stm_definition.md',
    'experiment_design/quality_model/repair_target_taxonomy.md',
    'experiment_design/evaluation_logic.md',
    'experiment_design/SUMMARY.md',
    'reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md',
]:
    p = base / rel
    print(rel, p.exists(), p.stat().st_size if p.exists() else 'missing')
PY
```

```bash
# [cmd-r572-taxonomy-fields]
python - <<'PY'
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/quality_model/repair_target_taxonomy.md')
text = p.read_text()
required = [
    'target_id', 'semantic_element', 'scope_status', 'time_level',
    'structure_family', 'nl_evidence_required', 'representation_evidence_required',
    'repair_action_allowed', 'better_stm_condition_impact',
    'conversion_artifact_risk', 'forbidden_extrapolation',
    'must_fix', 'should_fix', 'monitor', 'not_repair_target', 'out_of_scope',
]
missing = [x for x in required if x not in text]
print('missing', missing)
raise SystemExit(1 if missing else 0)
PY
```
