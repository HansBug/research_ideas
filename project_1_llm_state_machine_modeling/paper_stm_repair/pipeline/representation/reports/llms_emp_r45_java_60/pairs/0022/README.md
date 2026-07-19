# Pair `0022`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0021`](../0021/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0023`](../0023/README.md)

- LLM：`Llama`
- 模型/场景：Hybrid Sport Utility Vehicle, HSUV
- NL SHA-256：`9fe426ba761d5a52c3b670f35410502a5289bdd9489c4a9bfa983e34d565040c`
- PlantUML SHA-256：`8ea7e01c4cf73f562b0c55fed76f8f318797aa06f9ee043170e79385f326f7c5`
- FCSTM SHA-256：`57d64c17528e6ecf28c079cdb1390c8a2368094a8107d617f8445ec04b568380`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：9 条 edge 齐；`PoweredOn -> [*] / keyOff` 为真实 root final，不再生成普通 end leaf。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0022.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0022.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0022.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states.
2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal.
3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm DeviceController
[*] --> PoweredOn
PoweredOn --> Operate: start
Operate --> Idle: user idle
Operate --> AcceleratingCruising: user accelerate or cruise
Operate --> Braking: user brake
Idle --> Operate: user action
AcceleratingCruising --> Operate: user action
Braking --> Operate: user action
PoweredOn --> [*]: keyOff
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0022 named "DeviceController" {
    event start named "start";
    event user_idle named "user idle";
    event user_accelerate_or_cruise named "user accelerate or cruise";
    event user_brake named "user brake";
    event user_action named "user action";
    event keyOff named "keyOff";
    state PoweredOn named "PoweredOn";
    state Operate named "Operate";
    state Idle named "Idle";
    state AcceleratingCruising named "AcceleratingCruising";
    state Braking named "Braking";
    [*] -> PoweredOn;
    PoweredOn -> Operate : /start;
    Operate -> Idle : /user_idle;
    Operate -> AcceleratingCruising : /user_accelerate_or_cruise;
    Operate -> Braking : /user_brake;
    Idle -> Operate : /user_action;
    AcceleratingCruising -> Operate : /user_action;
    Braking -> Operate : /user_action;
    PoweredOn -> [*] : /keyOff;
}
```

[上一组 `0021`](../0021/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0023`](../0023/README.md)
