# Pair `0054`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0053`](../0053/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0055`](../0055/README.md)

- LLM：`Claude`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Generation PlantUML`
- 作者输出单元格：`I56`；Excel row：`56`
- Phase-I fallback：`true`
- 相对 Phase-I 是否变化：`false`
- Phase-I PlantUML SHA-256：`096e925ebe77027797d115e656538bc942eb62e77b1e3dc426f51ae457533d14`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`096e925ebe77027797d115e656538bc942eb62e77b1e3dc426f51ae457533d14`
- FCSTM SHA-256：`9aab3f42e6d79cf52fa3ce5e13a973bc378a839d1c9a6bf2cef357db3c13d83a`
- review subject SHA-256：`5e5ac531b1f680243539ffd3d6e532e77b2fc9646f05ff7ec952a21b9b6195bd`
- working contract SHA-256：`b57812811fb8951b6c8422d0d6b3673d7d2822b53938df5c5cf59ad1a324ab91`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `8`
- mapped / blocked / silent drop：`8` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `4/4` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `8`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`19` / `24` / `0`
- source macro / positive identity trace / conversion boundary trace：`12` / `19` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0054 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. All four authored lifecycle declarations retain owner/kind/action identity, while LifecycleActive and abstract hooks remain compiler-owned/runtime-excluded.
- source anchors：`source-ref:llms_emp_feedback_final_0054.puml:line:4\|state InMotion {, source-ref:llms_emp_feedback_final_0054.puml:line:7\|Accelerating --> Cruising : Reached Cruising/Cruise`；FCSTM anchors：`element-ref:source:state:InMotion@line:7\|state InMotion named "InMotion" {, element-ref:compiler:transition_segment:tr_0003:segment:1@line:20\|!Accelerating -> Cruising : /Reached_Cruising_Cruise;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0054.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0054.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0054.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0054.json) | [source trace](../../source_traces/llms_emp_feedback_final_0054.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | InMotion | source-ref:llms_emp_feedback_final_0054.puml:line:4\|state InMotion { | element-ref:source:state:InMotion@line:7\|state InMotion named "InMotion" { | source:state:InMotion | - | Case 0054 binds source:state:InMotion to the exact authored occurrence 'state InMotion {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | Reached Cruising/Cruise | source-ref:llms_emp_feedback_final_0054.puml:line:7\|Accelerating --> Cruising : Reached Cruising/Cruise | element-ref:compiler:transition_segment:tr_0003:segment:1@line:20\|!Accelerating -> Cruising : /Reached_Cruising_Cruise; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0054 binds source:transition:tr_0003 to the exact authored occurrence 'Accelerating --> Cruising : Reached Cruising/Cruise'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:synthetic_state:0001:001-LifecycleActive` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:5\|[*] --> Accelerating | element-ref:compiler:state:llms_emp_feedback_final_0054.InMotion.Accelerating.LifecycleActive@line:10\|state LifecycleActive named "Active body of Accelerating";, element-ref:source:state:InMotion.Accelerating@line:8\|state Accelerating named "Accelerating" { | compiler:state:llms_emp_feedback_final_0054.InMotion.Accelerating.LifecycleActive, source:state:InMotion.Accelerating | Case 0054 risk synthetic_state occurrence review:synthetic_state:0001:001-LifecycleActive: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0002:002-LifecycleActive` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:8\|Accelerating --> Approaching : Approached/Decelerate | element-ref:compiler:state:llms_emp_feedback_final_0054.InMotion.Approaching.LifecycleActive@line:16\|state LifecycleActive named "Active body of Approaching";, element-ref:source:state:InMotion.Approaching@line:14\|state Approaching named "Approaching" { | compiler:state:llms_emp_feedback_final_0054.InMotion.Approaching.LifecycleActive, source:state:InMotion.Approaching | Case 0054 risk synthetic_state occurrence review:synthetic_state:0002:002-LifecycleActive: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0003:003-LifecycleActive` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:15\|InMotion --> EmergencyStopping : [obstacle detected] | element-ref:compiler:state:llms_emp_feedback_final_0054.EmergencyStopping.LifecycleActive@line:29\|state LifecycleActive named "Active body of EmergencyStopping";, element-ref:source:state:EmergencyStopping@line:26\|state EmergencyStopping named "EmergencyStopping" { | compiler:state:llms_emp_feedback_final_0054.EmergencyStopping.LifecycleActive, source:state:EmergencyStopping | Case 0054 risk synthetic_state occurrence review:synthetic_state:0003:003-LifecycleActive: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:lifecycle:0004:001-InMotion.Accelerating` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:6\|Accelerating : entry/Accelerate | element-ref:compiler:lifecycle_action:InMotion.Accelerating:1:Accelerate@line:9\|enter abstract Accelerate; | compiler:lifecycle_action:InMotion.Accelerating:1:Accelerate, source:lifecycle:InMotion.Accelerating:1 | Case 0054 risk lifecycle occurrence review:lifecycle:0004:001-InMotion.Accelerating: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0005:002-InMotion.Approaching` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:10\|Approaching : do/Send | element-ref:compiler:lifecycle_action:InMotion.Approaching:2:Send@line:15\|>> during before abstract Send; | compiler:lifecycle_action:InMotion.Approaching:2:Send, source:lifecycle:InMotion.Approaching:2 | Case 0054 risk lifecycle occurrence review:lifecycle:0005:002-InMotion.Approaching: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0006:003-EmergencyStopping` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:17\|EmergencyStopping : do/Emergency Stop | element-ref:compiler:lifecycle_action:EmergencyStopping:3:EmergencyStop@line:27\|>> during before abstract EmergencyStop; | compiler:lifecycle_action:EmergencyStopping:3:EmergencyStop, source:lifecycle:EmergencyStopping:3 | Case 0054 risk lifecycle occurrence review:lifecycle:0006:003-EmergencyStopping: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0007:004-EmergencyStopping` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0054.puml:line:18\|EmergencyStopping : do/Send Obstacle Detected | element-ref:compiler:lifecycle_action:EmergencyStopping:4:SendObstacleDetected@line:28\|>> during before abstract SendObstacleDetected; | compiler:lifecycle_action:EmergencyStopping:4:SendObstacleDetected, source:lifecycle:EmergencyStopping:4 | Case 0054 risk lifecycle occurrence review:lifecycle:0007:004-EmergencyStopping: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I56` | `true` | `096e925ebe77027797d115e656538bc942eb62e77b1e3dc426f51ae457533d14` | - | - |
| `phase_ii_format` | `U56` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z56` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE56` | `false` | `-` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`7` / `7`
- aligned transition endpoints：`8`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.opaque_transition_label_semantics` | 6 |

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
[*] --> DoorsClosing

state InMotion {
[*] --> Accelerating
Accelerating : entry/Accelerate
Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate
Cruising --> Approaching : Approached/Decelerate
Approaching : do/Send
}

DoorsClosing --> InMotion : Closed/SendDeparted
InMotion --> Stopping : Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping : [obstacle detected]

EmergencyStopping : do/Emergency Stop
EmergencyStopping : do/Send Obstacle Detected
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0054 named "llms_emp_feedback_final_0054" {
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Arrived_Stop_Send_Arrived named "Arrived/Stop, Send Arrived";
    event _obstacle_detected named "[obstacle detected]";
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating" {
            enter abstract Accelerate;
            state LifecycleActive named "Active body of Accelerating";
            [*] -> LifecycleActive;
        }
        state Cruising named "Cruising";
        state Approaching named "Approaching" {
            >> during before abstract Send;
            state LifecycleActive named "Active body of Approaching";
            [*] -> LifecycleActive;
        }
        [*] -> Accelerating;
        !Accelerating -> Cruising : /Reached_Cruising_Cruise;
        !Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
    }
    state DoorsClosing named "DoorsClosing";
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping" {
        >> during before abstract EmergencyStop;
        >> during before abstract SendObstacleDetected;
        state LifecycleActive named "Active body of EmergencyStopping";
        [*] -> LifecycleActive;
    }
    [*] -> DoorsClosing;
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    !InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    !InMotion -> EmergencyStopping : /_obstacle_detected;
}
```

[上一组 `0053`](../0053/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0055`](../0055/README.md)
