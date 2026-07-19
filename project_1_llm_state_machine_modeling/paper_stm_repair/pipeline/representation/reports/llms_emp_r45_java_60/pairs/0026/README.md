# Pair `0026`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0025`](../0025/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0027`](../0027/README.md)

- LLM：`Llama`
- 模型/场景：UAV swarm state machine diagram
- NL SHA-256：`a01c022f5380700b6c13800497291640b4d64abbadce1d8984be0c14880ebeb3`
- PlantUML SHA-256：`894d0cfae3a1dc6b26026f6c4eb1e342402deab997113ffc849c636aa68a4aba`
- FCSTM SHA-256：`49aece10a82ff093b2df3bf4722e480b88da5333fa3c9b1bccbe3c1a7ff05bb8`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：UAV 4 state、4 transition、root final 与 body 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0026.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0026.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0026.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm UAV Swarm State Machine
[*] --> SearchingState
SearchingState: Target Search State

SearchingState --> FormationAdjustmentState : Intercepted
FormationAdjustmentState: Formation Adjustment State

SearchingState --> AttackState : Task Assignment Received
AttackState: Attack State

AttackState --> SearchingState : Attack Completed
SearchingState --> [*] : Mission Completed
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0026 named "UAV Swarm State Machine" {
    event Intercepted named "Intercepted";
    event Task_Assignment_Received named "Task Assignment Received";
    event Attack_Completed named "Attack Completed";
    event Mission_Completed named "Mission Completed";
    state SearchingState named "SearchingState\n[PlantUML body] Target Search State";
    state FormationAdjustmentState named "FormationAdjustmentState\n[PlantUML body] Formation Adjustment State";
    state AttackState named "AttackState\n[PlantUML body] Attack State";
    [*] -> SearchingState;
    SearchingState -> FormationAdjustmentState : /Intercepted;
    SearchingState -> AttackState : /Task_Assignment_Received;
    AttackState -> SearchingState : /Attack_Completed;
    SearchingState -> [*] : /Mission_Completed;
}
```

[上一组 `0025`](../0025/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0027`](../0027/README.md)
