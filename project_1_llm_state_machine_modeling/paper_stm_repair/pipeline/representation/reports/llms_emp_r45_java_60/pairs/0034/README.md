# Pair `0034`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0033`](../0033/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0035`](../0035/README.md)

- LLM：`Kimi`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE36`；Excel row：`36`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`47368dce1df97e572f9709094956208acb6532b92405a125582d2b538b3fe283`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`7b8702713b8df8f9d419d808632d39871052f2f9d179f3fbfd01f3d133856d11`
- FCSTM SHA-256：`e8119a95379e5089085a8d5127cb6036c06664d71a16ee5b17d327fd43b09a0c`
- review subject SHA-256：`849dcf7644754b0cefc9c9360679f855819b0a93d9b544d5f530ebe6940a8de3`
- working contract SHA-256：`b0b922f200582715f04caeb7d1430b4deeb15e033e53e4ea335802c20eac0b15`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `13`
- mapped / blocked / silent drop：`13` / `0` / `0`
- final / lifecycle / body coverage：`2/2` / `5/5` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `13`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`25` / `27` / `0`
- source macro / positive identity trace / conversion boundary trace：`18` / `25` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0034 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0034.puml:line:2\|[*] --> DoorsClosing, source-ref:llms_emp_feedback_final_0034.puml:line:5\|DoorsClosing --> InMotion : Closed/SendDeparted`；FCSTM anchors：`element-ref:source:state:DoorsClosing@line:10\|state DoorsClosing named "DoorsClosing" {, element-ref:compiler:transition_segment:tr_0002:segment:1@line:28\|DoorsClosing -> InMotion : /Closed_SendDeparted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0034.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0034.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0034.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0034.json) | [source trace](../../source_traces/llms_emp_feedback_final_0034.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | DoorsClosing | source-ref:llms_emp_feedback_final_0034.puml:line:2\|[*] --> DoorsClosing | element-ref:source:state:DoorsClosing@line:10\|state DoorsClosing named "DoorsClosing" { | source:state:DoorsClosing | - | Case 0034 binds source:state:DoorsClosing to authored PlantUML occurrence '[*] --> DoorsClosing' and current FCSTM occurrence 'state DoorsClosing named "DoorsClosing" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | Closed/SendDeparted | source-ref:llms_emp_feedback_final_0034.puml:line:5\|DoorsClosing --> InMotion : Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0002:segment:1@line:28\|DoorsClosing -> InMotion : /Closed_SendDeparted; | source:transition:tr_0002 | compiler:transition_segment:tr_0002:segment:1 | Case 0034 binds source:transition:tr_0002 to authored PlantUML occurrence 'DoorsClosing --> InMotion : Closed/SendDeparted' and current FCSTM occurrence 'DoorsClosing -> InMotion : /Closed_SendDeparted;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0005` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0034.puml:line:11\|EmergencyStopping --> [*] : Obstacle Cleared | element-ref:compiler:transition_segment:tr_0005:segment:1@line:31\|EmergencyStopping -> [*] : /Obstacle_Cleared; | compiler:transition_segment:tr_0005:segment:1, source:transition:tr_0005 | Case 0034 final_boundary occurrence review:final_boundary:0001:tr_0005 binds exact source refs to working-contract elements compiler:transition_segment:tr_0005:segment:1, source:transition:tr_0005. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:final_boundary:0002:tr_0013` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0034.puml:line:25\|Approaching --> [*] : Destination Missed | element-ref:compiler:transition_segment:tr_0013:segment:1@line:39\|Approaching -> [*] : /Destination_Missed; | compiler:transition_segment:tr_0013:segment:1, source:transition:tr_0013 | Case 0034 final_boundary occurrence review:final_boundary:0002:tr_0013 binds exact source refs to working-contract elements compiler:transition_segment:tr_0013:segment:1, source:transition:tr_0013. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:lifecycle:0003:001-DoorsClosing` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0034.puml:line:4\|DoorsClosing : entry/Accelerate | element-ref:compiler:lifecycle_action:DoorsClosing:1:Accelerate@line:11\|enter abstract Accelerate; | compiler:lifecycle_action:DoorsClosing:1:Accelerate, source:lifecycle:DoorsClosing:1 | Case 0034 lifecycle occurrence review:lifecycle:0003:001-DoorsClosing binds exact source refs to working-contract elements compiler:lifecycle_action:DoorsClosing:1:Accelerate, source:lifecycle:DoorsClosing:1. The lifecycle owner, kind, and action text remain source-visible through an abstract hook, while executable action behavior stays capability_excluded. |
| `review:lifecycle:0004:002-EmergencyStopping` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0034.puml:line:10\|EmergencyStopping : entry/Emergency Stop | element-ref:compiler:lifecycle_action:EmergencyStopping:2:EmergencyStop@line:16\|enter abstract EmergencyStop; | compiler:lifecycle_action:EmergencyStopping:2:EmergencyStop, source:lifecycle:EmergencyStopping:2 | Case 0034 lifecycle occurrence review:lifecycle:0004:002-EmergencyStopping binds exact source refs to working-contract elements compiler:lifecycle_action:EmergencyStopping:2:EmergencyStop, source:lifecycle:EmergencyStopping:2. The lifecycle owner, kind, and action text remain source-visible through an abstract hook, while executable action behavior stays capability_excluded. |
| `review:lifecycle:0005:003-Accelerating` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0034.puml:line:14\|Accelerating : entry/Accelerate | element-ref:compiler:lifecycle_action:Accelerating:3:Accelerate@line:19\|enter abstract Accelerate; | compiler:lifecycle_action:Accelerating:3:Accelerate, source:lifecycle:Accelerating:3 | Case 0034 lifecycle occurrence review:lifecycle:0005:003-Accelerating binds exact source refs to working-contract elements compiler:lifecycle_action:Accelerating:3:Accelerate, source:lifecycle:Accelerating:3. The lifecycle owner, kind, and action text remain source-visible through an abstract hook, while executable action behavior stays capability_excluded. |
| `review:lifecycle:0006:004-Cruising` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0034.puml:line:19\|Cruising : entry/Cruise | element-ref:compiler:lifecycle_action:Cruising:4:Cruise@line:22\|enter abstract Cruise; | compiler:lifecycle_action:Cruising:4:Cruise, source:lifecycle:Cruising:4 | Case 0034 lifecycle occurrence review:lifecycle:0006:004-Cruising binds exact source refs to working-contract elements compiler:lifecycle_action:Cruising:4:Cruise, source:lifecycle:Cruising:4. The lifecycle owner, kind, and action text remain source-visible through an abstract hook, while executable action behavior stays capability_excluded. |
| `review:lifecycle:0007:005-Approaching` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0034.puml:line:23\|Approaching : entry/Decelerate | element-ref:compiler:lifecycle_action:Approaching:5:Decelerate@line:25\|enter abstract Decelerate; | compiler:lifecycle_action:Approaching:5:Decelerate, source:lifecycle:Approaching:5 | Case 0034 lifecycle occurrence review:lifecycle:0007:005-Approaching binds exact source refs to working-contract elements compiler:lifecycle_action:Approaching:5:Decelerate, source:lifecycle:Approaching:5. The lifecycle owner, kind, and action text remain source-visible through an abstract hook, while executable action behavior stays capability_excluded. |
| `review:explicit_concurrency:0008:001-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0034.puml:line:13\|InMotion --> Accelerating, source-ref:llms_emp_feedback_final_0034.puml:line:18\|InMotion --> Cruising, source-ref:llms_emp_feedback_final_0034.puml:line:22\|InMotion --> Approaching, source-ref:llms_emp_feedback_final_0034.puml:line:5\|DoorsClosing --> InMotion : Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0006:segment:1@line:32\|InMotion -> Accelerating;, element-ref:compiler:transition_segment:tr_0009:segment:1@line:35\|InMotion -> Cruising;, element-ref:compiler:transition_segment:tr_0011:segment:1@line:37\|InMotion -> Approaching;, element-ref:source:state:InMotion@line:13\|state InMotion named "InMotion"; | source:state:InMotion, source:transition:tr_0006, source:transition:tr_0009, source:transition:tr_0011 | Case 0034 explicit_concurrency occurrence review:explicit_concurrency:0008:001-ambiguous_unlabeled_fanout binds exact source refs to working-contract elements source:state:InMotion, source:transition:tr_0006, source:transition:tr_0009, source:transition:tr_0011. The authored fork, join, or fan-out occurrence remains source-visible, while unsupported concurrent execution is capability_excluded rather than guessed. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I36` | `true` | `47368dce1df97e572f9709094956208acb6532b92405a125582d2b538b3fe283` | - | - |
| `phase_ii_format` | `U36` | `true` | `697e6a22abedd11fce067c44f4fec67b6ffe1c37a833cb1acef019c33d22acd6` | 1. syntax error: stm TrainStateMachine { | YES |
| `phase_ii_grammar` | `Z36` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE36` | `true` | `7b8702713b8df8f9d419d808632d39871052f2f9d179f3fbfd01f3d133856d11` | 1. missing composite state | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`7` / `7`
- aligned transition endpoints：`13`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.ambiguous_unlabeled_fanout` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 9 |

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

DoorsClosing : entry/Accelerate
DoorsClosing --> InMotion : Closed/SendDeparted

InMotion --> Stopping : Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping : Obstacle Detected

EmergencyStopping : entry/Emergency Stop
EmergencyStopping --> [*] : Obstacle Cleared

InMotion --> Accelerating 
Accelerating : entry/Accelerate
Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate

InMotion --> Cruising 
Cruising : entry/Cruise
Cruising --> Approaching : Approached/Decelerate

InMotion --> Approaching 
Approaching : entry/Decelerate
Approaching --> Stopping : Ready to Stop
Approaching --> [*] : Destination Missed
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0034 named "llms_emp_feedback_final_0034" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Arrived_Stop_Send_Arrived named "Arrived/Stop, Send Arrived";
    event Obstacle_Detected named "Obstacle Detected";
    event Obstacle_Cleared named "Obstacle Cleared";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Ready_to_Stop named "Ready to Stop";
    event Destination_Missed named "Destination Missed";
    state DoorsClosing named "DoorsClosing" {
        enter abstract Accelerate;
    }
    state InMotion named "InMotion";
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping" {
        enter abstract EmergencyStop;
    }
    state Accelerating named "Accelerating" {
        enter abstract Accelerate;
    }
    state Cruising named "Cruising" {
        enter abstract Cruise;
    }
    state Approaching named "Approaching" {
        enter abstract Decelerate;
    }
    [*] -> DoorsClosing;
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    InMotion -> EmergencyStopping : /Obstacle_Detected;
    EmergencyStopping -> [*] : /Obstacle_Cleared;
    InMotion -> Accelerating;
    Accelerating -> Cruising : /Reached_Cruising_Cruise;
    Accelerating -> Approaching : /Approached_Decelerate;
    InMotion -> Cruising;
    Cruising -> Approaching : /Approached_Decelerate;
    InMotion -> Approaching;
    Approaching -> Stopping : /Ready_to_Stop;
    Approaching -> [*] : /Destination_Missed;
}
```

[上一组 `0033`](../0033/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0035`](../0035/README.md)
