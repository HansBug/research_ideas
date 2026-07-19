# Pair `0011`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0010`](../0010/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0012`](../0012/README.md)

- LLM：`GPT-4`
- 模型/场景：State machine diagram of the base brake subsystem
- NL SHA-256：`abb20a2187c100d7c75a3038df101c91b369df70a07dfafd6eafc72da859fc99`
- PlantUML SHA-256：`3d75fa9170ba4fdf5b0e8061e2dc1bba709824fbffb6768713232f262bb6ce28`
- FCSTM SHA-256：`11ee049e364048a6a5104413f8a9e70fd6ac28300bb24746967da343e77ff480`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：与 `0001` 同构，全部 state/edge/body 对齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0011.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0011.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0011.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations.
2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state.
3 After entering the braking state, the system transitions to the brake caliper clamping state.
```

## 原装 PlantUML STM0

```plantuml
@startuml
[*] --> InitialState
InitialState: Initial State

InitialState --> BrakingState : Brake Signal Received
InitialState --> OperationalState : Signal Transmission Fails

BrakingState --> ClampingState : Entering Clamping State
ClampingState : Brake Caliper Clamping State

OperationalState --> InitialState : Signal Feedback Sent
BrakingState --> InitialState : Signal Feedback Sent

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0011 named "llms_emp_stm_results_0011" {
    event Brake_Signal_Received named "Brake Signal Received";
    event Signal_Transmission_Fails named "Signal Transmission Fails";
    event Entering_Clamping_State named "Entering Clamping State";
    event Signal_Feedback_Sent named "Signal Feedback Sent";
    state InitialState named "InitialState\n[PlantUML body] Initial State";
    state ClampingState named "ClampingState\n[PlantUML body] Brake Caliper Clamping State";
    state BrakingState named "BrakingState";
    state OperationalState named "OperationalState";
    [*] -> InitialState;
    InitialState -> BrakingState : /Brake_Signal_Received;
    InitialState -> OperationalState : /Signal_Transmission_Fails;
    BrakingState -> ClampingState : /Entering_Clamping_State;
    OperationalState -> InitialState : /Signal_Feedback_Sent;
    BrakingState -> InitialState : /Signal_Feedback_Sent;
}
```

[上一组 `0010`](../0010/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0012`](../0012/README.md)
