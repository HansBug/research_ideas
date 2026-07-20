# Pair `0044`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0043`](../0043/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0045`](../0045/README.md)

- LLM：`DeepSeek`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE46`；Excel row：`46`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`7f5397c95cef79f21a7d18892486a912a7cdeaa1d9d9465bac47df872e0c9b6a`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`38ba184ccbb3ed5d77a9cf48493190fd87c83374219d033194248984f2410fe3`
- FCSTM SHA-256：`fee93bc0feff0dca7e8cf38872fe6c5c70a1045c81db1c7f7ca5d4e9871044cb`
- review subject SHA-256：`88a1e1dee7901eeb358f35765f526401d82ada4ec044df3f0c84649367f4db1d`
- working contract SHA-256：`18f58b1d3274deadcf06beb977983d54654676473eed026479cadf308f73f7ae`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `9`
- mapped / blocked / silent drop：`9` / `0` / `0`
- final / lifecycle / body coverage：`2/2` / `3/3` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `9`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`19` / `26` / `0`
- source macro / positive identity trace / conversion boundary trace：`12` / `19` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0044 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0044.puml:line:4\|state DoorsClosing, source-ref:llms_emp_feedback_final_0044.puml:line:5\|DoorsClosing --> InMotion : Closed/SendDeparted`；FCSTM anchors：`element-ref:source:state:DoorsClosing@line:7\|state DoorsClosing named "DoorsClosing";, element-ref:compiler:transition_segment:tr_0002:segment:1@line:33\|DoorsClosing -> InMotion : /Closed_SendDeparted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0044.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0044.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0044.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0044.json) | [source trace](../../source_traces/llms_emp_feedback_final_0044.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | DoorsClosing | source-ref:llms_emp_feedback_final_0044.puml:line:4\|state DoorsClosing | element-ref:source:state:DoorsClosing@line:7\|state DoorsClosing named "DoorsClosing"; | source:state:DoorsClosing | - | Case 0044 binds source:state:DoorsClosing to the exact authored occurrence 'state DoorsClosing'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | Closed/SendDeparted | source-ref:llms_emp_feedback_final_0044.puml:line:5\|DoorsClosing --> InMotion : Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0002:segment:1@line:33\|DoorsClosing -> InMotion : /Closed_SendDeparted; | source:transition:tr_0002 | compiler:transition_segment:tr_0002:segment:1 | Case 0044 binds source:transition:tr_0002 to the exact authored occurrence 'DoorsClosing --> InMotion : Closed/SendDeparted'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0008` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0044.puml:line:22\|Stopping --> [*] | element-ref:compiler:transition_segment:tr_0008:segment:1@line:36\|Stopping -> [*]; | compiler:transition_segment:tr_0008:segment:1, source:transition:tr_0008 | Case 0044 risk final_boundary occurrence review:final_boundary:0001:tr_0008: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:final_boundary:0002:tr_0009` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0044.puml:line:23\|EmergencyStopping --> [*] | element-ref:compiler:transition_segment:tr_0009:segment:1@line:37\|!EmergencyStopping -> [*]; | compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009 | Case 0044 risk final_boundary occurrence review:final_boundary:0002:tr_0009: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:synthetic_state:0003:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:7\|state InMotion { | element-ref:compiler:state:llms_emp_feedback_final_0044.InMotion.UnspecifiedInitial@line:9\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:InMotion@line:8\|state InMotion named "InMotion" { | compiler:state:llms_emp_feedback_final_0044.InMotion.UnspecifiedInitial, source:state:InMotion | Case 0044 risk synthetic_state occurrence review:synthetic_state:0003:001-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0004:002-LifecycleActive` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:8\|state Accelerating : entry/Accelerate | element-ref:compiler:state:llms_emp_feedback_final_0044.InMotion.Accelerating.LifecycleActive@line:12\|state LifecycleActive named "Active body of Accelerating";, element-ref:source:state:InMotion.Accelerating@line:10\|state Accelerating named "Accelerating" { | compiler:state:llms_emp_feedback_final_0044.InMotion.Accelerating.LifecycleActive, source:state:InMotion.Accelerating | Case 0044 risk synthetic_state occurrence review:synthetic_state:0004:002-LifecycleActive: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0005:003-LifecycleActive` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:10\|state Approaching : do/Send | element-ref:compiler:state:llms_emp_feedback_final_0044.InMotion.Approaching.LifecycleActive@line:18\|state LifecycleActive named "Active body of Approaching";, element-ref:source:state:InMotion.Approaching@line:16\|state Approaching named "Approaching" { | compiler:state:llms_emp_feedback_final_0044.InMotion.Approaching.LifecycleActive, source:state:InMotion.Approaching | Case 0044 risk synthetic_state occurrence review:synthetic_state:0005:003-LifecycleActive: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0006:004-LifecycleActive` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:20\|state EmergencyStopping : do/Emergency Stop, send "Obstacle Detected" | element-ref:compiler:state:llms_emp_feedback_final_0044.EmergencyStopping.LifecycleActive@line:28\|state LifecycleActive named "Active body of EmergencyStopping";, element-ref:source:state:EmergencyStopping@line:26\|state EmergencyStopping named "EmergencyStopping" { | compiler:state:llms_emp_feedback_final_0044.EmergencyStopping.LifecycleActive, source:state:EmergencyStopping | Case 0044 risk synthetic_state occurrence review:synthetic_state:0006:004-LifecycleActive: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:lifecycle:0007:001-InMotion.Accelerating` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:8\|state Accelerating : entry/Accelerate | element-ref:compiler:lifecycle_action:InMotion.Accelerating:1:Accelerate@line:11\|enter abstract Accelerate; | compiler:lifecycle_action:InMotion.Accelerating:1:Accelerate, source:lifecycle:InMotion.Accelerating:1 | Case 0044 risk lifecycle occurrence review:lifecycle:0007:001-InMotion.Accelerating: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0008:002-InMotion.Approaching` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:10\|state Approaching : do/Send | element-ref:compiler:lifecycle_action:InMotion.Approaching:2:Send@line:17\|>> during before abstract Send; | compiler:lifecycle_action:InMotion.Approaching:2:Send, source:lifecycle:InMotion.Approaching:2 | Case 0044 risk lifecycle occurrence review:lifecycle:0008:002-InMotion.Approaching: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0009:003-EmergencyStopping` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0044.puml:line:20\|state EmergencyStopping : do/Emergency Stop, send "Obstacle Detected" | element-ref:compiler:lifecycle_action:EmergencyStopping:3:EmergencyStopSendObstacleDetected@line:27\|>> during before abstract EmergencyStopSendObstacleDetected; | compiler:lifecycle_action:EmergencyStopping:3:EmergencyStopSendObstacleDetected, source:lifecycle:EmergencyStopping:3 | Case 0044 risk lifecycle occurrence review:lifecycle:0009:003-EmergencyStopping: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I46` | `true` | `7f5397c95cef79f21a7d18892486a912a7cdeaa1d9d9465bac47df872e0c9b6a` | - | - |
| `phase_ii_format` | `U46` | `true` | `38ba184ccbb3ed5d77a9cf48493190fd87c83374219d033194248984f2410fe3` | syntax error: stm TrainSystem | YES |
| `phase_ii_grammar` | `Z46` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE46` | `true` | `38ba184ccbb3ed5d77a9cf48493190fd87c83374219d033194248984f2410fe3` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`7` / `7`
- aligned transition endpoints：`9`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.missing_explicit_initial` | 1 |
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

state DoorsClosing
DoorsClosing --> InMotion : Closed/SendDeparted

state InMotion {
state Accelerating : entry/Accelerate
state Cruising
state Approaching : do/Send

Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate
Cruising --> Approaching : Approached/Decelerate
}

InMotion --> Stopping : Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping : Obstacle Detected

state EmergencyStopping : do/Emergency Stop, send "Obstacle Detected"

Stopping --> [*]
EmergencyStopping --> [*]

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0044 named "llms_emp_feedback_final_0044" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Arrived_Stop_Send_Arrived named "Arrived/Stop, Send Arrived";
    event Obstacle_Detected named "Obstacle Detected";
    state DoorsClosing named "DoorsClosing";
    state InMotion named "InMotion" {
        state UnspecifiedInitial named "Unspecified initial";
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
        !Accelerating -> Cruising : /Reached_Cruising_Cruise;
        !Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
        [*] -> UnspecifiedInitial;
    }
    state EmergencyStopping named "EmergencyStopping" {
        >> during before abstract EmergencyStopSendObstacleDetected;
        state LifecycleActive named "Active body of EmergencyStopping";
        [*] -> LifecycleActive;
    }
    state Stopping named "Stopping";
    [*] -> DoorsClosing;
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    !InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    !InMotion -> EmergencyStopping : /Obstacle_Detected;
    Stopping -> [*];
    !EmergencyStopping -> [*];
}
```

[上一组 `0043`](../0043/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0045`](../0045/README.md)
