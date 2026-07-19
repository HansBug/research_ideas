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
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：该行无作者 checking regeneration，按合同回退 Phase-I；InMotion 三子态、DoorsClosing/Stopping/EmergencyStopping 共 7 状态、8 边及 Accelerating/Approaching/EmergencyStopping 的 4 个 lifecycle action 全保留。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0054.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0054.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0054.json) | [人工总账](../../MANUAL_REVIEW.md)

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
