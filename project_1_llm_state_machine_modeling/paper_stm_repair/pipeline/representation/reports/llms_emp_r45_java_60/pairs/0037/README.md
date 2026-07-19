# Pair `0037`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0036`](../0036/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0038`](../0038/README.md)

- LLM：`Kimi`
- 模型/场景：Collision avoidance sub-machine state diagram
- NL SHA-256：`49854d044ad99f16a710021500f5e972da93b27635a41144d9b91d32444c0f63`
- PlantUML SHA-256：`98186aedfa61de1b81699fd4bd301bc000ab9f0bb900f68ff062a90c6a9e3d23`
- FCSTM SHA-256：`20805a85b4b85a4cea891d191e430fa30c862e99e2f0df493a5101205be63494`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：bracket endpoint 还原为六个 state；三条 root final 与全部 signal edge 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0037.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0037.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0037.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. There are three region in this diagram
2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.
3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm CollisionAvoidanceSystem
[*] --> InitialState
InitialState: Initial State

InitialState --> FrontendCollision : Frontend Collision Detected
InitialState --> RearEndCollision : Rear-End Collision Detected
InitialState --> PedestrianCollision : Pedestrian Collision Detected

[FrontendCollision] -down-> [BrakingControl] : Brake Signal Received
[RearEndCollision] -down-> [SteeringControl] : Steering Signal Received
[PedestrianCollision] -down-> [EmergencyStop] : Emergency Stop Signal Received

[BrakingControl] --> [*] : Collision Avoided
[SteeringControl] --> [*] : Collision Avoided
[EmergencyStop] --> [*] : Collision Avoided

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0037 named "CollisionAvoidanceSystem" {
    event Frontend_Collision_Detected named "Frontend Collision Detected";
    event Rear_End_Collision_Detected named "Rear-End Collision Detected";
    event Pedestrian_Collision_Detected named "Pedestrian Collision Detected";
    event Brake_Signal_Received named "Brake Signal Received";
    event Steering_Signal_Received named "Steering Signal Received";
    event Emergency_Stop_Signal_Received named "Emergency Stop Signal Received";
    event Collision_Avoided named "Collision Avoided";
    state InitialState named "InitialState\n[PlantUML body] Initial State";
    state FrontendCollision named "FrontendCollision";
    state RearEndCollision named "RearEndCollision";
    state PedestrianCollision named "PedestrianCollision";
    state BrakingControl named "BrakingControl";
    state SteeringControl named "SteeringControl";
    state EmergencyStop named "EmergencyStop";
    [*] -> InitialState;
    InitialState -> FrontendCollision : /Frontend_Collision_Detected;
    InitialState -> RearEndCollision : /Rear_End_Collision_Detected;
    InitialState -> PedestrianCollision : /Pedestrian_Collision_Detected;
    FrontendCollision -> BrakingControl : /Brake_Signal_Received;
    RearEndCollision -> SteeringControl : /Steering_Signal_Received;
    PedestrianCollision -> EmergencyStop : /Emergency_Stop_Signal_Received;
    BrakingControl -> [*] : /Collision_Avoided;
    SteeringControl -> [*] : /Collision_Avoided;
    EmergencyStop -> [*] : /Collision_Avoided;
}
```

[上一组 `0036`](../0036/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0038`](../0038/README.md)
