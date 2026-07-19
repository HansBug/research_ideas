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
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：DoorsClosing/InMotion 三子态/Stopping/EmergencyStopping 共 7 状态、9 边全在；Accelerating entry、Approaching do、EmergencyStopping do 三个 action 保留，Stopping 与 EmergencyStopping 两个 root final 正确终止。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0044.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0044.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0044.json) | [人工总账](../../MANUAL_REVIEW.md)

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
