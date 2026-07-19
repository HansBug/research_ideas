# Pair `0034`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0033`](../0033/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0035`](../0035/README.md)

- LLM：`Kimi`
- 模型/场景：state machine for Train Control
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`47368dce1df97e572f9709094956208acb6532b92405a125582d2b538b3fe283`
- FCSTM SHA-256：`034508c247959283b176072ac0363a4ce3ffe5ab719f1f5bc6a40fa7775f7d75`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：directional arrow 未伪造层级；13 edge、两个 root final、五个 lifecycle hook 与三路 fan-out 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0034.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0034.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0034.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm TrainStateMachine {
[*] --> DoorsClosing
DoorsClosing : entry/Accelerate
DoorsClosing --> InMotion : Closed/SendDeparted

InMotion --> Stopping : Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping : Obstacle Detected

EmergencyStopping : entry/Emergency Stop
EmergencyStopping --> [*] : Obstacle Cleared

InMotion -down-> Accelerating
InMotion -right-> Cruising
InMotion -up-> Approaching

Accelerating : entry/Accelerate
Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate

Cruising : entry/Cruise
Cruising --> Approaching : Approached/Decelerate

Approaching : entry/Decelerate
Approaching --> Stopping : Ready to Stop
Approaching --> [*] : Destination Missed
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0034 named "TrainStateMachine" {
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
    state InMotion named "InMotion";
    state Stopping named "Stopping";
    [*] -> DoorsClosing;
    !DoorsClosing -> InMotion : /Closed_SendDeparted;
    InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    InMotion -> EmergencyStopping : /Obstacle_Detected;
    !EmergencyStopping -> [*] : /Obstacle_Cleared;
    InMotion -> Accelerating;
    InMotion -> Cruising;
    InMotion -> Approaching;
    !Accelerating -> Cruising : /Reached_Cruising_Cruise;
    !Accelerating -> Approaching : /Approached_Decelerate;
    !Cruising -> Approaching : /Approached_Decelerate;
    !Approaching -> Stopping : /Ready_to_Stop;
    !Approaching -> [*] : /Destination_Missed;
}
```

[上一组 `0033`](../0033/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0035`](../0035/README.md)
