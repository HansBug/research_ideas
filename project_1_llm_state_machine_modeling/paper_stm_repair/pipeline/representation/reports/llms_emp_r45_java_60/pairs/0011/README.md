# Pair `0011`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0010`](../0010/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0012`](../0012/README.md)

- LLM：`GPT-4`
- 模型/场景：State machine diagram of the base brake subsystem
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE13`；Excel row：`13`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`3d75fa9170ba4fdf5b0e8061e2dc1bba709824fbffb6768713232f262bb6ce28`
- NL SHA-256：`abb20a2187c100d7c75a3038df101c91b369df70a07dfafd6eafc72da859fc99`
- PlantUML SHA-256：`a609a81454607877775487b2b020a85ab1e4ad859a7dc98f20e2df0a93104c12`
- FCSTM SHA-256：`80bc87148fdeef46a1b69f22f9cb71c060030bf763cdbf90614579b051f8a078`
- 结构裁决：`structure_preserved`
- source states / transitions：`5` / `7`
- mapped / blocked / silent drop：`7` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `3/3`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`5` / `7`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：与 0001 同源但独立 GPT-4 行的 5 状态、7 边和三个 body 均以本行 hash 冻结，两个不同来源的 Signal Feedback 边都存在。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0011.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0011.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0011.json) | [人工总账](../../MANUAL_REVIEW.md)

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I13` | `true` | `3d75fa9170ba4fdf5b0e8061e2dc1bba709824fbffb6768713232f262bb6ce28` | - | - |
| `phase_ii_format` | `U13` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z13` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE13` | `true` | `a609a81454607877775487b2b020a85ab1e4ad859a7dc98f20e2df0a93104c12` | 1. missing state and transition | 1.0 |

## Official identity ledger

- status：`aligned`
- canonical / official states：`5` / `5`
- aligned transition endpoints：`7`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.opaque_state_body_semantics` | 3 |
| `R45.DEBT.opaque_transition_label_semantics` | 6 |

## NL

```text
1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations.
2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state.
3 After entering the braking state, the system transitions to the brake caliper clamping state.
```

## 作者 Phase-II 最终 PlantUML STM0

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

OperationalState --> ClampingLoseState : Transition to Clamping Lose State
ClampingLoseState : Clamping Lose State
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0011 named "llms_emp_feedback_final_0011" {
    event Brake_Signal_Received named "Brake Signal Received";
    event Signal_Transmission_Fails named "Signal Transmission Fails";
    event Entering_Clamping_State named "Entering Clamping State";
    event Signal_Feedback_Sent named "Signal Feedback Sent";
    event Transition_to_Clamping_Lose_State named "Transition to Clamping Lose State";
    state InitialState named "InitialState\n[PlantUML body] Initial State";
    state BrakingState named "BrakingState";
    state OperationalState named "OperationalState";
    state ClampingState named "ClampingState\n[PlantUML body] Brake Caliper Clamping State";
    state ClampingLoseState named "ClampingLoseState\n[PlantUML body] Clamping Lose State";
    [*] -> InitialState;
    InitialState -> BrakingState : /Brake_Signal_Received;
    InitialState -> OperationalState : /Signal_Transmission_Fails;
    BrakingState -> ClampingState : /Entering_Clamping_State;
    OperationalState -> InitialState : /Signal_Feedback_Sent;
    BrakingState -> InitialState : /Signal_Feedback_Sent;
    OperationalState -> ClampingLoseState : /Transition_to_Clamping_Lose_State;
}
```

[上一组 `0010`](../0010/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0012`](../0012/README.md)
