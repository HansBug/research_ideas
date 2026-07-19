# Pair `0020`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0019`](../0019/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0021`](../0021/README.md)

- LLM：`Llama`
- 模型/场景：high-level driving module
- NL SHA-256：`f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`
- PlantUML SHA-256：`478b8db78f5465f4ced13d2ed7f455bc12bbb5c77b5d1d0b475cdc97d905b8c6`
- FCSTM SHA-256：`f36df10020b8fabe70b41f35fa10511873d7470e64a4b7101f4c62227fbd1b2e`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：`stm` name、Autonomous children、两条 child-to-Human occurrence 与两个 root final 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0020.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0020.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0020.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm DrivingMode
[*] -> HumanDrivingMode
HumanDrivingMode: Human Driving Mode
HumanDrivingMode -> AutonomousMode: front_distance > 10
AutonomousMode: Autonomous Mode
state AutonomousMode {
[*] -> AutoInitialState
AutoInitialState: Initial State
AutoInitialState -> AutoOperationalState: Signal Transmission Succeeds
AutoOperationalState: Operational State
AutoOperationalState -> AutoFinalState: Mission Completed
AutoFinalState: Final State
AutoOperationalState -> HumanDrivingMode: human steering cmd, brake pressed
AutoFinalState -> HumanDrivingMode: human steering cmd, brake pressed
}
HumanDrivingMode -> [*]: Power Off
AutonomousMode -> [*]: Power Off
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0020 named "DrivingMode" {
    event front_distance_10 named "front_distance > 10";
    event Signal_Transmission_Succeeds named "Signal Transmission Succeeds";
    event Mission_Completed named "Mission Completed";
    event human_steering_cmd_brake_pressed named "human steering cmd, brake pressed";
    event Power_Off named "Power Off";
    state AutonomousMode named "AutonomousMode\n[PlantUML body] Autonomous Mode" {
        state AutoInitialState named "AutoInitialState\n[PlantUML body] Initial State";
        state AutoOperationalState named "AutoOperationalState\n[PlantUML body] Operational State";
        state AutoFinalState named "AutoFinalState\n[PlantUML body] Final State";
        [*] -> AutoInitialState;
        AutoInitialState -> AutoOperationalState : /Signal_Transmission_Succeeds;
        AutoOperationalState -> AutoFinalState : /Mission_Completed;
        AutoOperationalState -> [*] : /human_steering_cmd_brake_pressed;
        AutoFinalState -> [*] : /human_steering_cmd_brake_pressed;
    }
    state HumanDrivingMode named "HumanDrivingMode\n[PlantUML body] Human Driving Mode";
    [*] -> HumanDrivingMode;
    HumanDrivingMode -> AutonomousMode : /front_distance_10;
    AutonomousMode -> HumanDrivingMode : /human_steering_cmd_brake_pressed;
    AutonomousMode -> HumanDrivingMode : /human_steering_cmd_brake_pressed;
    HumanDrivingMode -> [*] : /Power_Off;
    !AutonomousMode -> [*] : /Power_Off;
}
```

[上一组 `0019`](../0019/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0021`](../0021/README.md)
