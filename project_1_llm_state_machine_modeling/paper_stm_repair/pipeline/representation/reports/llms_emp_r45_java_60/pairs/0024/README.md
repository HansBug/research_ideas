# Pair `0024`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0023`](../0023/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0025`](../0025/README.md)

- LLM：`Llama`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE26`；Excel row：`26`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`0a9b42eaa34ae47557ece09f79e387a69a29da2e13d4f833a4edaaf9a42d2598`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`5900a03e9a58e6079bacd2857c82133e549809bb532a33c62ecbbe3077cb5745`
- FCSTM SHA-256：`2ac55a187d25d8d141b62d0a8bd639a248aeb7d5b681313417d9c074dbb4ab17`
- review subject SHA-256：`b70c2aa8cba5d64797dc8f2dafa2d43ffd7c974ab960be19bf39d0497f21d9ee`
- working contract SHA-256：`716ef19af2d57b347421c09299fcaaecdf49ab76ebbb2ccab601cc4c9a86b45b`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `10`
- mapped / blocked / silent drop：`10` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `5/5`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `10`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`22` / `19` / `0`
- source macro / positive identity trace / conversion boundary trace：`15` / `22` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0024 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences. Fresh v6 main-session review re-read NL, PlantUML, FCSTM, working contract, and source trace after the portable Java identity change; source/FCSTM/trace bytes are unchanged and verification remains fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0024.puml:line:5\|state InMotion {, source-ref:llms_emp_feedback_final_0024.puml:line:4\|DoorsClosing --> InMotion: Closed/SendDeparted`；FCSTM anchors：`element-ref:source:state:InMotion@line:9\|state InMotion named "InMotion" {, element-ref:compiler:transition_segment:tr_0002:segment:1@line:23\|DoorsClosing -> InMotion : /Closed_SendDeparted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0024.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0024.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0024.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0024.json) | [source trace](../../source_traces/llms_emp_feedback_final_0024.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | InMotion | source-ref:llms_emp_feedback_final_0024.puml:line:5\|state InMotion { | element-ref:source:state:InMotion@line:9\|state InMotion named "InMotion" { | source:state:InMotion | - | Case 0024 binds source:state:InMotion to the exact authored occurrence 'state InMotion {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | Closed/SendDeparted | source-ref:llms_emp_feedback_final_0024.puml:line:4\|DoorsClosing --> InMotion: Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0002:segment:1@line:23\|DoorsClosing -> InMotion : /Closed_SendDeparted; | source:transition:tr_0002 | compiler:transition_segment:tr_0002:segment:1 | Case 0024 binds source:transition:tr_0002 to the exact authored occurrence 'DoorsClosing --> InMotion: Closed/SendDeparted'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0007` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0024.puml:line:14\|Approaching --> InMotion:exit/Send | element-ref:compiler:transition_segment:tr_0007:segment:1@line:17\|Approaching -> [*] : /exit_Send;, element-ref:compiler:transition_segment:tr_0007:segment:2@line:24\|InMotion -> InMotion : /exit_Send; | compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, source:transition:tr_0007 | Case 0024 risk multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0007: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I26` | `true` | `0a9b42eaa34ae47557ece09f79e387a69a29da2e13d4f833a4edaaf9a42d2598` | - | - |
| `phase_ii_format` | `U26` | `true` | `c23a45feac8a5c988a860287f8c6a9282a9c6c01116aecff1b2ca8caba300b4e` | syntax error: stm TrainSystem | YES |
| `phase_ii_grammar` | `Z26` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE26` | `true` | `5900a03e9a58e6079bacd2857c82133e549809bb532a33c62ecbbe3077cb5745` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`7` / `7`
- aligned transition endpoints：`10`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.opaque_state_body_semantics` | 5 |
| `R45.DEBT.opaque_transition_label_semantics` | 8 |

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
DoorsClosing: Doors are closing
DoorsClosing --> InMotion: Closed/SendDeparted
state InMotion {
[*] --> Accelerating
Accelerating: Accelerating
Accelerating --> Cruising: Reached Cruising/Cruise
Accelerating --> Approaching: Approached/Decelerate

Cruising: Cruising
Cruising --> Approaching: Approached/Decelerate
Approaching: Approaching
Approaching --> InMotion:exit/Send
}
InMotion --> Stopping: Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping: Obstacle Detected
EmergencyStopping: Emergency Stop
EmergencyStopping --> InMotion:exit/Send Obstacle Detected
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0024 named "llms_emp_feedback_final_0024" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event exit_Send named "exit/Send";
    event Arrived_Stop_Send_Arrived named "Arrived/Stop, Send Arrived";
    event Obstacle_Detected named "Obstacle Detected";
    event exit_Send_Obstacle_Detected named "exit/Send Obstacle Detected";
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating\n[PlantUML body] Accelerating";
        state Cruising named "Cruising\n[PlantUML body] Cruising";
        state Approaching named "Approaching\n[PlantUML body] Approaching";
        [*] -> Accelerating;
        Accelerating -> Cruising : /Reached_Cruising_Cruise;
        Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
        Approaching -> [*] : /exit_Send;
    }
    state DoorsClosing named "DoorsClosing\n[PlantUML body] Doors are closing";
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Emergency Stop";
    [*] -> DoorsClosing;
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    InMotion -> InMotion : /exit_Send;
    !InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    !InMotion -> EmergencyStopping : /Obstacle_Detected;
    EmergencyStopping -> InMotion : /exit_Send_Obstacle_Detected;
}
```

[上一组 `0023`](../0023/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0025`](../0025/README.md)
