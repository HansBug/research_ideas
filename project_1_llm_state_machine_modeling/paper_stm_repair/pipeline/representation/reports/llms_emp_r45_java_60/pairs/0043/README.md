# Pair `0043`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0042`](../0042/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0044`](../0044/README.md)

- LLM：`DeepSeek`
- 模型/场景：Pump Control state machine
- NL SHA-256：`a391765dba935d89e6d2467c97b218c0136d106ea9c00bac91e6525e28ac04f1`
- PlantUML SHA-256：`aebd7f70f2529017cb257c1b3001e18cadc8222c085b3cf7a33aada16cfb3bd1`
- FCSTM SHA-256：`d0852ce9ec23cd9f5c0e7bdad6e42e6aec6d9fb6426e488be3df2e331237931e`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：bracket labels 原字符串进入 named opaque event；四条边齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0043.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0043.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0043.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm PumpControlSystem [Pump Control State Machine]

[*] --> PumpControl

state PumpControl {
[*] --> PumpState
PumpState --> WaterState : [Water Flow Detected]
PumpState --> MethaneState : [Methane Flow Detected]
WaterState --> PumpState : [Water Flow Completed]
MethaneState --> PumpState : [Methane Flow Completed]
}

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0043 named "PumpControlSystem [Pump Control State Machine]" {
    event _Water_Flow_Detected named "[Water Flow Detected]";
    event _Methane_Flow_Detected named "[Methane Flow Detected]";
    event _Water_Flow_Completed named "[Water Flow Completed]";
    event _Methane_Flow_Completed named "[Methane Flow Completed]";
    state PumpControl named "PumpControl" {
        state PumpState named "PumpState";
        state WaterState named "WaterState";
        state MethaneState named "MethaneState";
        [*] -> PumpState;
        PumpState -> WaterState : /_Water_Flow_Detected;
        PumpState -> MethaneState : /_Methane_Flow_Detected;
        WaterState -> PumpState : /_Water_Flow_Completed;
        MethaneState -> PumpState : /_Methane_Flow_Completed;
    }
    [*] -> PumpControl;
}
```

[上一组 `0042`](../0042/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0044`](../0044/README.md)
