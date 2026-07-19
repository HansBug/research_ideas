# Pair `0023`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0022`](../0022/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0024`](../0024/README.md)

- LLM：`Llama`
- 模型/场景：Pump Control state machine
- NL SHA-256：`a391765dba935d89e6d2467c97b218c0136d106ea9c00bac91e6525e28ac04f1`
- PlantUML SHA-256：`3237c282856c15de2d2cc794e37cf945b24316694858ba99b94ec69521cc5e2a`
- FCSTM SHA-256：`78894c5e565298f23d94365d53ffe7494467606865ff1dd3861e605fca0eee64`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：PumpControl flat graph、三条 edge 与四条 body 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0023.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0023.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0023.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions.
2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState.
3. The system first transitions to the PumpState substate, where the pump is activated or controlled.
4. The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow.
5. Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm PumpControlSystem
[*] --> PumpControl
PumpControl: Pump Control
PumpControl --> PumpState: Start Pump
PumpState: Pump Activated
PumpControl --> WaterState: Monitor Water Flow
WaterState: Water Flow Monitored
PumpControl --> MethaneState: Monitor Methane Flow
MethaneState: Methane Flow Monitored
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0023 named "PumpControlSystem" {
    event Start_Pump named "Start Pump";
    event Monitor_Water_Flow named "Monitor Water Flow";
    event Monitor_Methane_Flow named "Monitor Methane Flow";
    state PumpControl named "PumpControl\n[PlantUML body] Pump Control";
    state PumpState named "PumpState\n[PlantUML body] Pump Activated";
    state WaterState named "WaterState\n[PlantUML body] Water Flow Monitored";
    state MethaneState named "MethaneState\n[PlantUML body] Methane Flow Monitored";
    [*] -> PumpControl;
    PumpControl -> PumpState : /Start_Pump;
    PumpControl -> WaterState : /Monitor_Water_Flow;
    PumpControl -> MethaneState : /Monitor_Methane_Flow;
}
```

[上一组 `0022`](../0022/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0024`](../0024/README.md)
