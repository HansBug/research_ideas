# Pair `0012`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0011`](../0011/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0013`](../0013/README.md)

- LLM：`GPT-4`
- 模型/场景：Hybrid Sport Utility Vehicle, HSUV
- NL SHA-256：`9fe426ba761d5a52c3b670f35410502a5289bdd9489c4a9bfa983e34d565040c`
- PlantUML SHA-256：`0314bb466726c4ba81177282e717511244fc77bf24682ba951f4103fd32b169a`
- FCSTM SHA-256：`5c2717310c343f9d3166add39113b65b2cbb0793c5f0df8146e5becc5018d9b9`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Off/Operate hierarchy、五条事件边与 composite forced exit 对齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0012.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0012.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0012.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states.
2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal.
3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping.
```

## 原装 PlantUML STM0

```plantuml
@startuml
[*] --> Off
Off --> Operate : start
state Operate {
[*] --> Idle
Idle --> AcceleratingOrCruising : accelerate
AcceleratingOrCruising --> Braking : brake
Braking --> Idle : stop
}
Operate --> Off : keyOff
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0012 named "llms_emp_stm_results_0012" {
    event start named "start";
    event accelerate named "accelerate";
    event brake named "brake";
    event stop named "stop";
    event keyOff named "keyOff";
    state Operate named "Operate" {
        state Idle named "Idle";
        state AcceleratingOrCruising named "AcceleratingOrCruising";
        state Braking named "Braking";
        [*] -> Idle;
        Idle -> AcceleratingOrCruising : /accelerate;
        AcceleratingOrCruising -> Braking : /brake;
        Braking -> Idle : /stop;
    }
    state Off named "Off";
    [*] -> Off;
    Off -> Operate : /start;
    !Operate -> Off : /keyOff;
}
```

[上一组 `0011`](../0011/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0013`](../0013/README.md)
