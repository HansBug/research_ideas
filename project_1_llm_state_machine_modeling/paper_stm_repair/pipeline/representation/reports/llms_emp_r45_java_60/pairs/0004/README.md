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
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：InMotion 三子态、Stopping/EmergencyStopping 与 3 个 lifecycle hook 全保留；DoorsClosing 自指 initial 被显式降为 InvalidInitial surrogate，未悄悄改成正常 child initial。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0004.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0004.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0004.json) | [人工总账](../../MANUAL_REVIEW.md)

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
