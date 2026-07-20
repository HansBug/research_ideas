# Pair `0004`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0003`](../0003/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0005`](../0005/README.md)

- LLM：`GPT-4o`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE6`；Excel row：`6`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`6313557b3733707618bb785619f2b87e2f93ed3373c038222112f8cff3d2694c`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`188bebba5631b87c315e966d8cd0f993630182d74f9b9bd677e1452198e458cb`
- FCSTM SHA-256：`5247f3fbb6272d8bc99d80d20ce9a22d587511cd01737de2bf4129aa025d34b9`
- review subject SHA-256：`f8a60e145bb15ad83720de6349669e10f08239f84bf12f39523713ad9054fc61`
- working contract SHA-256：`93bb221344cbb90c35846da281f4aa369a0ae01f0a7fe6ac121af970406b266e`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `9`
- mapped / blocked / silent drop：`9` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `4/4` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `9`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`20` / `26` / `0`
- source macro / positive identity trace / conversion boundary trace：`13` / `20` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0004 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences. Fresh v6 main-session review re-read NL, PlantUML, FCSTM, working contract, and source trace after the portable Java identity change; source/FCSTM/trace bytes are unchanged and verification remains fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0004.puml:line:4\|state DoorsClosing {, source-ref:llms_emp_feedback_final_0004.puml:line:8\|DoorsClosing --> InMotion : Closed/SendDeparted`；FCSTM anchors：`element-ref:source:state:DoorsClosing@line:7\|state DoorsClosing named "DoorsClosing" {, element-ref:compiler:transition_segment:tr_0003:segment:1@line:36\|!DoorsClosing -> InMotion : /Closed_SendDeparted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0004.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0004.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0004.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0004.json) | [source trace](../../source_traces/llms_emp_feedback_final_0004.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | DoorsClosing | source-ref:llms_emp_feedback_final_0004.puml:line:4\|state DoorsClosing { | element-ref:source:state:DoorsClosing@line:7\|state DoorsClosing named "DoorsClosing" { | source:state:DoorsClosing | - | Case 0004 binds source:state:DoorsClosing to the exact authored occurrence 'state DoorsClosing {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | Closed/SendDeparted | source-ref:llms_emp_feedback_final_0004.puml:line:8\|DoorsClosing --> InMotion : Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0003:segment:1@line:36\|!DoorsClosing -> InMotion : /Closed_SendDeparted; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0004 binds source:transition:tr_0003 to the exact authored occurrence 'DoorsClosing --> InMotion : Closed/SendDeparted'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:synthetic_state:0001:001-InvalidInitialtr_0002` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:5\|[*] --> DoorsClosing | element-ref:compiler:state:llms_emp_feedback_final_0004.DoorsClosing.InvalidInitialtr_0002@line:8\|state InvalidInitialtr_0002 named "PlantUML initial target outside child scope: DoorsClosing"; | compiler:state:llms_emp_feedback_final_0004.DoorsClosing.InvalidInitialtr_0002, source:transition:tr_0002 | Case 0004 risk synthetic_state occurrence review:synthetic_state:0001:001-InvalidInitialtr_0002: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0002:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:13\|state Accelerating { | element-ref:compiler:state:llms_emp_feedback_final_0004.InMotion.Accelerating.UnspecifiedInitial@line:14\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:InMotion.Accelerating@line:12\|state Accelerating named "Accelerating" { | compiler:state:llms_emp_feedback_final_0004.InMotion.Accelerating.UnspecifiedInitial, source:state:InMotion.Accelerating | Case 0004 risk synthetic_state occurrence review:synthetic_state:0002:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0003:003-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:24\|state Approaching { | element-ref:compiler:state:llms_emp_feedback_final_0004.InMotion.Approaching.UnspecifiedInitial@line:20\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:InMotion.Approaching@line:18\|state Approaching named "Approaching" { | compiler:state:llms_emp_feedback_final_0004.InMotion.Approaching.UnspecifiedInitial, source:state:InMotion.Approaching | Case 0004 risk synthetic_state occurrence review:synthetic_state:0003:003-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0004:004-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:32\|state EmergencyStopping { | element-ref:compiler:state:llms_emp_feedback_final_0004.EmergencyStopping.UnspecifiedInitial@line:31\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:EmergencyStopping@line:28\|state EmergencyStopping named "EmergencyStopping" { | compiler:state:llms_emp_feedback_final_0004.EmergencyStopping.UnspecifiedInitial, source:state:EmergencyStopping | Case 0004 risk synthetic_state occurrence review:synthetic_state:0004:004-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:lifecycle:0005:001-InMotion.Accelerating` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:14\|Accelerating: entry/Accelerate | element-ref:compiler:lifecycle_action:InMotion.Accelerating:1:Accelerate@line:13\|enter abstract Accelerate; | compiler:lifecycle_action:InMotion.Accelerating:1:Accelerate, source:lifecycle:InMotion.Accelerating:1 | Case 0004 risk lifecycle occurrence review:lifecycle:0005:001-InMotion.Accelerating: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0006:002-InMotion.Approaching` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:25\|Approaching: do/Send | element-ref:compiler:lifecycle_action:InMotion.Approaching:2:Send@line:19\|>> during before abstract Send; | compiler:lifecycle_action:InMotion.Approaching:2:Send, source:lifecycle:InMotion.Approaching:2 | Case 0004 risk lifecycle occurrence review:lifecycle:0006:002-InMotion.Approaching: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0007:003-EmergencyStopping` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:33\|EmergencyStopping: entry/Emergency Stop | element-ref:compiler:lifecycle_action:EmergencyStopping:3:EmergencyStop@line:29\|enter abstract EmergencyStop; | compiler:lifecycle_action:EmergencyStopping:3:EmergencyStop, source:lifecycle:EmergencyStopping:3 | Case 0004 risk lifecycle occurrence review:lifecycle:0007:003-EmergencyStopping: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |
| `review:lifecycle:0008:004-EmergencyStopping` | `lifecycle` | `capability_excluded` | source-ref:llms_emp_feedback_final_0004.puml:line:34\|EmergencyStopping: do/Send Obstacle Detected | element-ref:compiler:lifecycle_action:EmergencyStopping:4:SendObstacleDetected@line:30\|>> during before abstract SendObstacleDetected; | compiler:lifecycle_action:EmergencyStopping:4:SendObstacleDetected, source:lifecycle:EmergencyStopping:4 | Case 0004 risk lifecycle occurrence review:lifecycle:0008:004-EmergencyStopping: The authored entry/do/exit occurrence retains its owner, lifecycle kind, action identity, and abstract FCSTM hook, without claiming runtime equivalence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I6` | `true` | `6313557b3733707618bb785619f2b87e2f93ed3373c038222112f8cff3d2694c` | - | - |
| `phase_ii_format` | `U6` | `true` | `ffbc4577a4244c407f754a67975472017d9b1aa0eb1bb23df025f891d434c81a` | syntax error (Assumed diagram type: state) entry/Accelerate | YES |
| `phase_ii_grammar` | `Z6` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE6` | `true` | `188bebba5631b87c315e966d8cd0f993630182d74f9b9bd677e1452198e458cb` | None | - |

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
| `R45.DEBT.invalid_source_initial_target` | 1 |
| `R45.DEBT.missing_explicit_initial` | 3 |
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

state DoorsClosing {
  [*] --> DoorsClosing
}

DoorsClosing --> InMotion : Closed/SendDeparted

state InMotion {
  [*] --> Accelerating

  state Accelerating {
    Accelerating: entry/Accelerate
  }

  Accelerating --> Cruising : Reached Cruising/Cruise
  Accelerating --> Approaching : Approached/Decelerate

  state Cruising

  Cruising --> Approaching : Approached/Decelerate

  state Approaching {
    Approaching: do/Send
  }
}

InMotion --> Stopping : Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping : Obstacle Detected

state EmergencyStopping {
  EmergencyStopping: entry/Emergency Stop
  EmergencyStopping: do/Send Obstacle Detected
}

state Stopping

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0004 named "llms_emp_feedback_final_0004" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Arrived_Stop_Send_Arrived named "Arrived/Stop, Send Arrived";
    event Obstacle_Detected named "Obstacle Detected";
    state DoorsClosing named "DoorsClosing" {
        state InvalidInitialtr_0002 named "PlantUML initial target outside child scope: DoorsClosing";
        [*] -> InvalidInitialtr_0002;
    }
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating" {
            enter abstract Accelerate;
            state UnspecifiedInitial named "Unspecified initial";
            [*] -> UnspecifiedInitial;
        }
        state Cruising named "Cruising";
        state Approaching named "Approaching" {
            >> during before abstract Send;
            state UnspecifiedInitial named "Unspecified initial";
            [*] -> UnspecifiedInitial;
        }
        [*] -> Accelerating;
        !Accelerating -> Cruising : /Reached_Cruising_Cruise;
        !Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
    }
    state EmergencyStopping named "EmergencyStopping" {
        enter abstract EmergencyStop;
        >> during before abstract SendObstacleDetected;
        state UnspecifiedInitial named "Unspecified initial";
        [*] -> UnspecifiedInitial;
    }
    state Stopping named "Stopping";
    [*] -> DoorsClosing;
    !DoorsClosing -> InMotion : /Closed_SendDeparted;
    !InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    !InMotion -> EmergencyStopping : /Obstacle_Detected;
}
```

[上一组 `0003`](../0003/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0005`](../0005/README.md)
