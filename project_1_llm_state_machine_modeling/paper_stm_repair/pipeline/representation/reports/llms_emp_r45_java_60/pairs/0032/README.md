# Pair `0032`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0031`](../0031/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0033`](../0033/README.md)

- LLM：`Kimi`
- 模型/场景：Hybrid Sport Utility Vehicle, HSUV
- NL SHA-256：`9fe426ba761d5a52c3b670f35410502a5289bdd9489c4a9bfa983e34d565040c`
- PlantUML SHA-256：`95515e5e0af74e499fafe8da9fd82fb1a94f745f719b94288e6ece5872545451`
- FCSTM SHA-256：`622170b81a91fa7bc32cb240c4adb5662c017c064054059c98e13bda161e775a`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Device 6 state、13 edge 与六条 body 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0032.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0032.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0032.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states.
2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal.
3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm [stateMachine] Device Operation [Device Operation State Machine]

[*] --> OffState
OffState : Off
OffState --> OperateState : start
OperateState : Operate
OperateState --> IdleState : No Action
OperateState --> AcceleratingState : Accelerate
OperateState --> CruisingState : Cruise
OperateState --> BrakingState : Brake
IdleState : Idle
AcceleratingState : Accelerating
CruisingState : Cruising
BrakingState : Braking
IdleState --> AcceleratingState : Accelerate
IdleState --> BrakingState : Brake
AcceleratingState --> CruisingState : Reach Speed
AcceleratingState --> BrakingState : Brake
CruisingState --> BrakingState : Brake
BrakingState --> IdleState : Stop
OperateState --> OffState : keyOff

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0032 named "[stateMachine] Device Operation [Device Operation State Machine]" {
    event start named "start";
    event No_Action named "No Action";
    event Accelerate named "Accelerate";
    event Cruise named "Cruise";
    event Brake named "Brake";
    event Reach_Speed named "Reach Speed";
    event Stop named "Stop";
    event keyOff named "keyOff";
    state OffState named "OffState\n[PlantUML body] Off";
    state OperateState named "OperateState\n[PlantUML body] Operate";
    state IdleState named "IdleState\n[PlantUML body] Idle";
    state AcceleratingState named "AcceleratingState\n[PlantUML body] Accelerating";
    state CruisingState named "CruisingState\n[PlantUML body] Cruising";
    state BrakingState named "BrakingState\n[PlantUML body] Braking";
    [*] -> OffState;
    OffState -> OperateState : /start;
    OperateState -> IdleState : /No_Action;
    OperateState -> AcceleratingState : /Accelerate;
    OperateState -> CruisingState : /Cruise;
    OperateState -> BrakingState : /Brake;
    IdleState -> AcceleratingState : /Accelerate;
    IdleState -> BrakingState : /Brake;
    AcceleratingState -> CruisingState : /Reach_Speed;
    AcceleratingState -> BrakingState : /Brake;
    CruisingState -> BrakingState : /Brake;
    BrakingState -> IdleState : /Stop;
    OperateState -> OffState : /keyOff;
}
```

[上一组 `0031`](../0031/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0033`](../0033/README.md)
