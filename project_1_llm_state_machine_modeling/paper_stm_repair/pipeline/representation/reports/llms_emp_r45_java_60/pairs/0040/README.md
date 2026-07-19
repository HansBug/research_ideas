# Pair `0040`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0039`](../0039/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0041`](../0041/README.md)

- LLM：`DeepSeek`
- 模型/场景：high-level driving module
- NL SHA-256：`f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`
- PlantUML SHA-256：`42acdd25b7fad2ff8a9502db8169a3ff849a3ba164e3381d70467c97e615cf7e`
- FCSTM SHA-256：`e3817e84b86d17c816c9b7f640bde28e265e9173bb6546277bc6577e6725e544`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：双 event initial wait、Autonomous children、forced return 与 root final 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0040.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0040.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0040.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm DrivingSystem [Driving System State Machine]

[*] --> HumanDriving : Power On
HumanDriving : Human Driving Mode

HumanDriving --> Autonomous : front_distance > 10
Autonomous : Autonomous Mode
state Autonomous {
[*] --> AutoInitial : Enter Autonomous Mode
AutoInitial --> AutoFinal : Auto Process Complete
AutoFinal : Auto Final State
}

Autonomous --> HumanDriving : human_steering_cmd || brake_pressed || in (AutoFinal)
HumanDriving --> [*] : Power Off
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0040 named "DrivingSystem [Driving System State Machine]" {
    event Power_On named "Power On";
    event front_distance_10 named "front_distance > 10";
    event Enter_Autonomous_Mode named "Enter Autonomous Mode";
    event Auto_Process_Complete named "Auto Process Complete";
    event human_steering_cmd_brake_pressed_in_AutoFinal named "human_steering_cmd || brake_pressed || in (AutoFinal)";
    event Power_Off named "Power Off";
    state InitialWaittr_0001 named "Awaiting initial event: Power On";
    state Autonomous named "Autonomous\n[PlantUML body] Autonomous Mode" {
        state AutoFinal named "AutoFinal\n[PlantUML body] Auto Final State";
        state AutoInitial named "AutoInitial";
        state InitialWaittr_0003 named "Awaiting initial event: Enter Autonomous Mode";
        [*] -> InitialWaittr_0003;
        InitialWaittr_0003 -> AutoInitial : /Enter_Autonomous_Mode;
        AutoInitial -> AutoFinal : /Auto_Process_Complete;
    }
    state HumanDriving named "HumanDriving\n[PlantUML body] Human Driving Mode";
    [*] -> InitialWaittr_0001;
    InitialWaittr_0001 -> HumanDriving : /Power_On;
    HumanDriving -> Autonomous : /front_distance_10;
    !Autonomous -> HumanDriving : /human_steering_cmd_brake_pressed_in_AutoFinal;
    HumanDriving -> [*] : /Power_Off;
}
```

[上一组 `0039`](../0039/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0041`](../0041/README.md)
