# Pair `0014`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0013`](../0013/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0015`](../0015/README.md)

- LLM：`GPT-4`
- 模型/场景：state machine for Train Control
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`711124b29144fbb337739a5e7d8d97d8b7cdacd5828e71a036f0bbbae40364fc`
- FCSTM SHA-256：`890606eaa259bb7115dc6be50b169bb41989c04d1c618636e9c8315f62d068fa`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：root/Approaching/EmergencyStopping 缺 initial 均 fail-closed；10 条 macro 和 generic body 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0014.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0014.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0014.json) | [人工总账](../../MANUAL_REVIEW.md)

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

## 原装 PlantUML STM0

```plantuml
@startuml

DoorsClosing --> InMotion: Closed/SendDeparted

state InMotion {
[*] --> Accelerating : Entry/Accelerate
Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate
Cruising --> Approaching : Approached/Decelerate

state Accelerating
state Cruising
state Approaching {
DuringApproaching: Nearing Destination
DuringApproaching --> Approaching: Send
}
}

InMotion --> Stopping: Arrived/Stop, SendArrived
InMotion --> EmergencyStopping: Obstacle Detected

state Stopping
state EmergencyStopping {
Entry: Emergency Stop
DuringEmergencyStopping: Obstacle Detected
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0014 named "llms_emp_stm_results_0014" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Entry_Accelerate named "Entry/Accelerate";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Send named "Send";
    event Arrived_Stop_SendArrived named "Arrived/Stop, SendArrived";
    event Obstacle_Detected named "Obstacle Detected";
    state UnspecifiedInitial named "Unspecified initial";
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating";
        state Cruising named "Cruising";
        state Approaching named "Approaching" {
            state UnspecifiedInitial named "Unspecified initial";
            state DuringApproaching named "DuringApproaching\n[PlantUML body] Nearing Destination";
            DuringApproaching -> [*] : /Send;
            [*] -> UnspecifiedInitial;
        }
        state InitialWaittr_0002 named "Awaiting initial event: Entry/Accelerate";
        [*] -> InitialWaittr_0002;
        InitialWaittr_0002 -> Accelerating : /Entry_Accelerate;
        Accelerating -> Cruising : /Reached_Cruising_Cruise;
        Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
        Approaching -> Approaching : /Send;
    }
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping" {
        state UnspecifiedInitial named "Unspecified initial";
        state Entry named "Entry\n[PlantUML body] Emergency Stop";
        state DuringEmergencyStopping named "DuringEmergencyStopping\n[PlantUML body] Obstacle Detected";
        [*] -> UnspecifiedInitial;
    }
    state DoorsClosing named "DoorsClosing";
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    !InMotion -> Stopping : /Arrived_Stop_SendArrived;
    !InMotion -> EmergencyStopping : /Obstacle_Detected;
    [*] -> UnspecifiedInitial;
}
```

[上一组 `0013`](../0013/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0015`](../0015/README.md)
