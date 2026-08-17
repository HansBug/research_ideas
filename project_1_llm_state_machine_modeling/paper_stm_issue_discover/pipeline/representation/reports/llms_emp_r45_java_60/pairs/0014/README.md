# Pair `0014`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0013`](../0013/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0015`](../0015/README.md)

- LLM：`GPT-4`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE16`；Excel row：`16`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`711124b29144fbb337739a5e7d8d97d8b7cdacd5828e71a036f0bbbae40364fc`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`36f37fba4bcf46ac2f33879309c90543d30aef033d1e692c83272858bbf45876`
- FCSTM SHA-256：`5d1e81a3d641965bde0a1d147dcee27902162dbe283f46ac2824b11b0fe30733`
- review subject SHA-256：`4e01052b25eff964d18988c6d0631b939c2e2356e95efea68ab39f3d319c090e`
- working contract SHA-256：`3e580936e0365a9c3d3ce0504fb82332f3c01cfffd5574337169684a6e96ead9`
- 结构裁决：`structure_preserved`
- source states / transitions：`8` / `7`
- mapped / blocked / silent drop：`7` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `4/4`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`8` / `7`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`19` / `25` / `0`
- source macro / positive identity trace / conversion boundary trace：`11` / `19` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0014 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0014.puml:line:2\|state DoorsClosing, source-ref:llms_emp_feedback_final_0014.puml:line:4\|DoorsClosing --> InMotion: Closed/SendDeparted`；FCSTM anchors：`element-ref:source:state:DoorsClosing@line:10\|state DoorsClosing named "DoorsClosing";, element-ref:compiler:transition_segment:tr_0001:segment:1@line:35\|DoorsClosing -> InMotion : /Closed_SendDeparted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0014.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0014.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0014.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0014.json) | [source trace](../../source_traces/llms_emp_feedback_final_0014.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | DoorsClosing | source-ref:llms_emp_feedback_final_0014.puml:line:2\|state DoorsClosing | element-ref:source:state:DoorsClosing@line:10\|state DoorsClosing named "DoorsClosing"; | source:state:DoorsClosing | - | Case 0014 binds source:state:DoorsClosing to authored PlantUML occurrence 'state DoorsClosing' and current FCSTM occurrence 'state DoorsClosing named "DoorsClosing";'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | Closed/SendDeparted | source-ref:llms_emp_feedback_final_0014.puml:line:4\|DoorsClosing --> InMotion: Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0001:segment:1@line:35\|DoorsClosing -> InMotion : /Closed_SendDeparted; | source:transition:tr_0001 | compiler:transition_segment:tr_0001:segment:1 | Case 0014 binds source:transition:tr_0001 to authored PlantUML occurrence 'DoorsClosing --> InMotion: Closed/SendDeparted' and current FCSTM occurrence 'DoorsClosing -> InMotion : /Closed_SendDeparted;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0006` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:20\|InMotion --> Stopping: Arrived/Stop, SendArrived, source-ref:llms_emp_feedback_final_0014.puml:line:21\|InMotion --> EmergencyStopping: Obstacle Detected | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0006:segment:1@line:19\|Accelerating -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:2@line:20\|Cruising -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:3@line:21\|Approaching -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:4@line:32\|InMotion -> Stopping : if [R45RouteToken == 6] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, compiler:transition_segment:tr_0006:segment:3, compiler:transition_segment:tr_0006:segment:4, source:transition:tr_0006 | Case 0014 multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0006 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, compiler:transition_segment:tr_0006:segment:3, compiler:transition_segment:tr_0006:segment:4, source:transition:tr_0006. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0002:tr_0006` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:20\|InMotion --> Stopping: Arrived/Stop, SendArrived, source-ref:llms_emp_feedback_final_0014.puml:line:21\|InMotion --> EmergencyStopping: Obstacle Detected | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0006:segment:1@line:19\|Accelerating -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:2@line:20\|Cruising -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:3@line:21\|Approaching -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:4@line:32\|InMotion -> Stopping : if [R45RouteToken == 6] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, compiler:transition_segment:tr_0006:segment:3, compiler:transition_segment:tr_0006:segment:4, source:transition:tr_0006 | Case 0014 route_controller occurrence review:route_controller:0002:tr_0006 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, compiler:transition_segment:tr_0006:segment:3, compiler:transition_segment:tr_0006:segment:4, source:transition:tr_0006. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0003:tr_0007` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:20\|InMotion --> Stopping: Arrived/Stop, SendArrived, source-ref:llms_emp_feedback_final_0014.puml:line:21\|InMotion --> EmergencyStopping: Obstacle Detected | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:22\|Accelerating -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:2@line:23\|Cruising -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:3@line:24\|Approaching -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:4@line:33\|InMotion -> EmergencyStopping : if [R45RouteToken == 7] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, source:transition:tr_0007 | Case 0014 multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0007 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, source:transition:tr_0007. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0004:tr_0007` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:20\|InMotion --> Stopping: Arrived/Stop, SendArrived, source-ref:llms_emp_feedback_final_0014.puml:line:21\|InMotion --> EmergencyStopping: Obstacle Detected | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:22\|Accelerating -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:2@line:23\|Cruising -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:3@line:24\|Approaching -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:4@line:33\|InMotion -> EmergencyStopping : if [R45RouteToken == 7] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, source:transition:tr_0007 | Case 0014 route_controller occurrence review:route_controller:0004:tr_0007 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, source:transition:tr_0007. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:synthetic_state:0005:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:2\|state DoorsClosing, source-ref:llms_emp_feedback_final_0014.puml:line:23\|state Stopping, source-ref:llms_emp_feedback_final_0014.puml:line:24\|state EmergencyStopping {, source-ref:llms_emp_feedback_final_0014.puml:line:6\|state InMotion { | element-ref:compiler:state:llms_emp_feedback_final_0014.UnspecifiedInitial@line:9\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:DoorsClosing@line:10\|state DoorsClosing named "DoorsClosing";, element-ref:source:state:EmergencyStopping@line:27\|state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Obstacle Detected" {, element-ref:source:state:InMotion@line:11\|state InMotion named "InMotion" {, element-ref:source:state:Stopping@line:26\|state Stopping named "Stopping"; | compiler:state:llms_emp_feedback_final_0014.UnspecifiedInitial, source:state:DoorsClosing, source:state:EmergencyStopping, source:state:InMotion, source:state:Stopping | Case 0014 synthetic_state occurrence review:synthetic_state:0005:001-UnspecifiedInitial binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0014.UnspecifiedInitial, source:state:DoorsClosing, source:state:EmergencyStopping, source:state:InMotion, source:state:Stopping. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |
| `review:synthetic_state:0006:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:24\|state EmergencyStopping { | element-ref:compiler:state:llms_emp_feedback_final_0014.EmergencyStopping.UnspecifiedInitial@line:29\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:EmergencyStopping@line:27\|state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Obstacle Detected" { | compiler:state:llms_emp_feedback_final_0014.EmergencyStopping.UnspecifiedInitial, source:state:EmergencyStopping | Case 0014 synthetic_state occurrence review:synthetic_state:0006:002-UnspecifiedInitial binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0014.EmergencyStopping.UnspecifiedInitial, source:state:EmergencyStopping. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I16` | `true` | `711124b29144fbb337739a5e7d8d97d8b7cdacd5828e71a036f0bbbae40364fc` | - | - |
| `phase_ii_format` | `U16` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z16` | `true` | `36f37fba4bcf46ac2f33879309c90543d30aef033d1e692c83272858bbf45876` | cannot connect internal state to the composite state itself. | YES |
| `phase_ii_semantic` | `AE16` | `true` | `36f37fba4bcf46ac2f33879309c90543d30aef033d1e692c83272858bbf45876` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`8` / `8`
- aligned transition endpoints：`7`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.composite_source_activation_dispatch` | 2 |
| `R45.DEBT.missing_explicit_initial` | 2 |
| `R45.DEBT.opaque_state_body_semantics` | 4 |
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

## NL

```text
1. The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal.
2. In the InMotion state, the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected.
3. When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal.
4. Within the InMotion state, the system operates in three substates: Accelerating, Cruising, and Approaching, which represent different phases of the train's motion.
5. The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal.
6. If the system is in the Accelerating substate and approaches its destination, it transitions to the Approaching substate upon receiving the "Approached/Decelerate" signal.
7. The system in the Cruising substate transitions to the Approaching substate when it approaches the destination, triggered by the "Approached/Decelerate" signal.
8. The system enters the Accelerating substate when motion begins, marked by the "Entry/Accelerate" action.
9. In the Approaching substate, the system sends the "Send" signal and continues to approach the destination.
10. The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
state DoorsClosing

DoorsClosing --> InMotion: Closed/SendDeparted

state InMotion {
[*] --> Accelerating : Entry/Accelerate
Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate
Cruising --> Approaching : Approached/Decelerate

state Accelerating
state Cruising
state Approaching {
Approaching: Nearing Destination
Approaching: Ready to Stop/Decelerate
}
}

InMotion --> Stopping: Arrived/Stop, SendArrived
InMotion --> EmergencyStopping: Obstacle Detected

state Stopping
state EmergencyStopping {
Entry: Emergency Stop
EmergencyStopping: Obstacle Detected
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0014 named "llms_emp_feedback_final_0014" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Entry_Accelerate named "Entry/Accelerate";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Arrived_Stop_SendArrived named "Arrived/Stop, SendArrived";
    event Obstacle_Detected named "Obstacle Detected";
    state UnspecifiedInitial named "Unspecified initial";
    state DoorsClosing named "DoorsClosing";
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating";
        state Cruising named "Cruising";
        state Approaching named "Approaching\n[PlantUML body] Nearing Destination\n[PlantUML body] Ready to Stop/Decelerate";
        [*] -> Accelerating : /Entry_Accelerate;
        Accelerating -> Cruising : /Reached_Cruising_Cruise;
        Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
        Accelerating -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };
        Cruising -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };
        Approaching -> [*] : /Arrived_Stop_SendArrived effect { R45RouteToken = 6; };
        Accelerating -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };
        Cruising -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };
        Approaching -> [*] : /Obstacle_Detected effect { R45RouteToken = 7; };
    }
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Obstacle Detected" {
        state Entry named "Entry\n[PlantUML body] Emergency Stop";
        state UnspecifiedInitial named "Unspecified initial";
        [*] -> UnspecifiedInitial;
    }
    InMotion -> Stopping : if [R45RouteToken == 6] effect { R45RouteToken = 0; };
    InMotion -> EmergencyStopping : if [R45RouteToken == 7] effect { R45RouteToken = 0; };
    [*] -> UnspecifiedInitial;
    DoorsClosing -> InMotion : /Closed_SendDeparted;
}
```

[上一组 `0013`](../0013/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0015`](../0015/README.md)
