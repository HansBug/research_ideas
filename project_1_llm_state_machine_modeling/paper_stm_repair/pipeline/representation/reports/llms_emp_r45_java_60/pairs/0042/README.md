# Pair `0042`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0041`](../0041/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0043`](../0043/README.md)

- LLM：`DeepSeek`
- 模型/场景：Hybrid Sport Utility Vehicle, HSUV
- NL SHA-256：`9fe426ba761d5a52c3b670f35410502a5289bdd9489c4a9bfa983e34d565040c`
- PlantUML SHA-256：`29fbe0d61ae3a876eff04656b538e326ef8e93b3df83da0bda9be7bcfb07eb97`
- FCSTM SHA-256：`e07a8489a28f68e3e5463d647d25d873755c9689ba1c7986519db96741f8c4e7`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：keyOff event initial wait、Operate 三状态与7条边齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0042.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0042.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0042.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states.
2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal.
3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm DeviceStateMachine

[*] --> Off : keyOff
Off --> Operate : start
Operate --> Off : keyOff

state Operate {
[*] --> Idle
Idle --> AcceleratingOrCruising : accelerate
AcceleratingOrCruising --> Idle : stop
AcceleratingOrCruising --> Braking : brake
Braking --> Idle : stop
Braking --> AcceleratingOrCruising : accelerate
}

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0042 named "DeviceStateMachine" {
    event keyOff named "keyOff";
    event start named "start";
    event accelerate named "accelerate";
    event stop named "stop";
    event brake named "brake";
    state InitialWaittr_0001 named "Awaiting initial event: keyOff";
    state Operate named "Operate" {
        state Idle named "Idle";
        state AcceleratingOrCruising named "AcceleratingOrCruising";
        state Braking named "Braking";
        [*] -> Idle;
        Idle -> AcceleratingOrCruising : /accelerate;
        AcceleratingOrCruising -> Idle : /stop;
        AcceleratingOrCruising -> Braking : /brake;
        Braking -> Idle : /stop;
        Braking -> AcceleratingOrCruising : /accelerate;
    }
    state Off named "Off";
    [*] -> InitialWaittr_0001;
    InitialWaittr_0001 -> Off : /keyOff;
    Off -> Operate : /start;
    !Operate -> Off : /keyOff;
}
```

[上一组 `0041`](../0041/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0043`](../0043/README.md)
