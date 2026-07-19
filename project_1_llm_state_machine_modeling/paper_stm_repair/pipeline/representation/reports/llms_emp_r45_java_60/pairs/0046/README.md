# Pair `0046`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0045`](../0045/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0047`](../0047/README.md)

- LLM：`DeepSeek`
- 模型/场景：UAV swarm state machine diagram
- NL SHA-256：`a01c022f5380700b6c13800497291640b4d64abbadce1d8984be0c14880ebeb3`
- PlantUML SHA-256：`709704f395b88943b357c62d4b4c1f93cb2b1e09ef0f72f8f26648de311b99fc`
- FCSTM SHA-256：`3dfdf5bb32d903419953857ce9b3da4a9b4770ee9a34e12c728f8385f6f946d7`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：UAV 4 state、6 edge 与 body/slash label 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0046.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0046.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0046.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1 This state machine model describes the state transitions of a UAV swarm.
2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas.
3 When the UAV swarm is intercepted, it transitions to the formation adjustment state.
4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm UAVSwarmStateMachine [UAV Swarm State Machine]

[*] --> Idle
Idle : Initial State

Idle --> Searching : Start Mission
Searching : Target Search State
Searching --> FormationAdjustment : Intercepted
Searching --> Attacking : Task Assignment Received

FormationAdjustment : Formation Adjustment State
FormationAdjustment --> Searching : Formation Adjusted

Attacking : Attack State
Attacking --> Searching : Attack Completed / UAV Count Decreased

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0046 named "UAVSwarmStateMachine [UAV Swarm State Machine]" {
    event Start_Mission named "Start Mission";
    event Intercepted named "Intercepted";
    event Task_Assignment_Received named "Task Assignment Received";
    event Formation_Adjusted named "Formation Adjusted";
    event Attack_Completed_UAV_Count_Decreased named "Attack Completed / UAV Count Decreased";
    state Idle named "Idle\n[PlantUML body] Initial State";
    state Searching named "Searching\n[PlantUML body] Target Search State";
    state FormationAdjustment named "FormationAdjustment\n[PlantUML body] Formation Adjustment State";
    state Attacking named "Attacking\n[PlantUML body] Attack State";
    [*] -> Idle;
    Idle -> Searching : /Start_Mission;
    Searching -> FormationAdjustment : /Intercepted;
    Searching -> Attacking : /Task_Assignment_Received;
    FormationAdjustment -> Searching : /Formation_Adjusted;
    Attacking -> Searching : /Attack_Completed_UAV_Count_Decreased;
}
```

[上一组 `0045`](../0045/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0047`](../0047/README.md)
