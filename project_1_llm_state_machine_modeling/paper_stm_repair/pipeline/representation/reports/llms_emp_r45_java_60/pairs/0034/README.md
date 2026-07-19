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
- FCSTM SHA-256：`603cbd9f06b3ce7e91bf30a9410cffde846e2dae0da2eda8c794844b7601105d`
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
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：DoorsClosing/InMotion/Stopping/EmergencyStopping/三运动态共 7 状态、13 边及五个 entry action 全保留；Obstacle Cleared 与 Destination Missed 两个 root final 保持终止，InMotion 无标签多出口明确留债。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0034.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0034.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0034.json) | [人工总账](../../MANUAL_REVIEW.md)

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
        state LifecycleActive named "Active body of DoorsClosing";
        [*] -> LifecycleActive;
    }
    state InMotion named "InMotion";
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping" {
        enter abstract EmergencyStop;
        state LifecycleActive named "Active body of EmergencyStopping";
        [*] -> LifecycleActive;
    }
    state Accelerating named "Accelerating" {
        enter abstract Accelerate;
        state LifecycleActive named "Active body of Accelerating";
        [*] -> LifecycleActive;
    }
    state Cruising named "Cruising" {
        enter abstract Cruise;
        state LifecycleActive named "Active body of Cruising";
        [*] -> LifecycleActive;
    }
    state Approaching named "Approaching" {
        enter abstract Decelerate;
        state LifecycleActive named "Active body of Approaching";
        [*] -> LifecycleActive;
    }
    [*] -> DoorsClosing;
    !DoorsClosing -> InMotion : /Closed_SendDeparted;
    InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    InMotion -> EmergencyStopping : /Obstacle_Detected;
    !EmergencyStopping -> [*] : /Obstacle_Cleared;
    InMotion -> Accelerating;
    !Accelerating -> Cruising : /Reached_Cruising_Cruise;
    !Accelerating -> Approaching : /Approached_Decelerate;
    InMotion -> Cruising;
    !Cruising -> Approaching : /Approached_Decelerate;
    InMotion -> Approaching;
    !Approaching -> Stopping : /Ready_to_Stop;
    !Approaching -> [*] : /Destination_Missed;
}
```

[上一组 `0033`](../0033/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0035`](../0035/README.md)
