# Pair `0033`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0032`](../0032/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0034`](../0034/README.md)

- LLM：`Kimi`
- 模型/场景：Pump Control state machine
- NL SHA-256：`a391765dba935d89e6d2467c97b218c0136d106ea9c00bac91e6525e28ac04f1`
- PlantUML SHA-256：`a885b2b07e8c8761bd81c54e9e326daf3a2ce3138e4cae0c305ee6c9fe8145db`
- FCSTM SHA-256：`2037af251445e2af5c1cf45ea2a6091558a89058b329cbf86263a2b772adbb8b`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：`stm PumpControlSystem {}` 作为 model container，四状态七边与 body 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0033.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0033.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0033.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm PumpControlSystem {
[*] --> PumpControl
PumpControl : PumpControl state
PumpControl --> PumpState : Activate Pump
PumpControl --> WaterState : Monitor Water Flow
PumpControl --> MethaneState : Monitor Methane Flow

PumpState : PumpState
PumpState --> PumpControl : Pump Deactivated

WaterState : WaterState
WaterState --> PumpControl : Water Flow Stabilized

MethaneState : MethaneState
MethaneState --> PumpControl : Methane Flow Stabilized
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0033 named "PumpControlSystem" {
    event Activate_Pump named "Activate Pump";
    event Monitor_Water_Flow named "Monitor Water Flow";
    event Monitor_Methane_Flow named "Monitor Methane Flow";
    event Pump_Deactivated named "Pump Deactivated";
    event Water_Flow_Stabilized named "Water Flow Stabilized";
    event Methane_Flow_Stabilized named "Methane Flow Stabilized";
    state PumpControl named "PumpControl\n[PlantUML body] PumpControl state";
    state PumpState named "PumpState\n[PlantUML body] PumpState";
    state WaterState named "WaterState\n[PlantUML body] WaterState";
    state MethaneState named "MethaneState\n[PlantUML body] MethaneState";
    [*] -> PumpControl;
    PumpControl -> PumpState : /Activate_Pump;
    PumpControl -> WaterState : /Monitor_Water_Flow;
    PumpControl -> MethaneState : /Monitor_Methane_Flow;
    PumpState -> PumpControl : /Pump_Deactivated;
    WaterState -> PumpControl : /Water_Flow_Stabilized;
    MethaneState -> PumpControl : /Methane_Flow_Stabilized;
}
```

[上一组 `0032`](../0032/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0034`](../0034/README.md)
