# Pair `0024`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0023`](../0023/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0025`](../0025/README.md)

- LLM：`Llama`
- 模型/场景：state machine for Train Control
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`0a9b42eaa34ae47557ece09f79e387a69a29da2e13d4f833a4edaaf9a42d2598`
- FCSTM SHA-256：`50e573527c805910b55976c526855b814b9a475d0241a4a9a300d87356c065c8`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：InMotion-owned entry/exit hook 与 root ownerless exit 分开；ancestor reentry/普通返回共10条 macro齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0024.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0024.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0024.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm TrainSystem
[*] --> DoorsClosing
DoorsClosing: Doors are closing
DoorsClosing --> InMotion: Closed/SendDeparted
state InMotion {
[*] --> Accelerating
Accelerating: Accelerating
Accelerating --> Cruising: Reached Cruising/Cruise
Accelerating --> Approaching: Approached/Decelerate
entry/Entry/Accelerate
Cruising: Cruising
Cruising --> Approaching: Approached/Decelerate
Approaching: Approaching
Approaching --> InMotion:
exit/Send
}
InMotion --> Stopping: Arrived/Stop, Send Arrived
InMotion --> EmergencyStopping: Obstacle Detected
EmergencyStopping: Emergency Stop
EmergencyStopping --> InMotion:
exit/Send Obstacle Detected
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0024 named "TrainSystem\n[Unowned PlantUML exit] Send Obstacle Detected" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Arrived_Stop_Send_Arrived named "Arrived/Stop, Send Arrived";
    event Obstacle_Detected named "Obstacle Detected";
    state InMotion named "InMotion" {
        enter abstract EntryAccelerate;
        exit abstract Send;
        state Accelerating named "Accelerating\n[PlantUML body] Accelerating";
        state Cruising named "Cruising\n[PlantUML body] Cruising";
        state Approaching named "Approaching\n[PlantUML body] Approaching";
        [*] -> Accelerating;
        Accelerating -> Cruising : /Reached_Cruising_Cruise;
        Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
        Approaching -> [*];
    }
    state DoorsClosing named "DoorsClosing\n[PlantUML body] Doors are closing";
    state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Emergency Stop";
    state Stopping named "Stopping";
    [*] -> DoorsClosing;
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    InMotion -> InMotion;
    !InMotion -> Stopping : /Arrived_Stop_Send_Arrived;
    !InMotion -> EmergencyStopping : /Obstacle_Detected;
    EmergencyStopping -> InMotion;
}
```

[上一组 `0023`](../0023/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0025`](../0025/README.md)
