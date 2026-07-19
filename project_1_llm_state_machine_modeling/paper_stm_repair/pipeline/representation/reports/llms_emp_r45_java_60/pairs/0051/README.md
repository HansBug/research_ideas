# Pair `0051`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0050`](../0050/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0052`](../0052/README.md)

- LLM：`Claude`
- 模型/场景：State machine diagram of the base brake subsystem
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE53`；Excel row：`53`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`4f821f97dcb4ba5854519a1255f41ee39f44b23e13b77663db966d82f8d23a25`
- NL SHA-256：`abb20a2187c100d7c75a3038df101c91b369df70a07dfafd6eafc72da859fc99`
- PlantUML SHA-256：`2e9acbd193d890e5d0f600256e74d7d5bed336fdf9360e3a30f6d7f0dc06ef3f`
- FCSTM SHA-256：`ffe0a959d6617f73ffb0ff2438f325139483f5875d63dea9f8b75d9d8439780e`
- 结构裁决：`structure_preserved`
- source states / transitions：`4` / `7`
- mapped / blocked / silent drop：`7` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `2/2`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`4` / `7`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：基础制动 4 状态、7 边与两个 body 完整对应，Braking/Operational 同标签反馈返回及 Clamping 的 Braking Complete 返回均保持独立。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0051.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0051.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0051.json) | [人工总账](../../MANUAL_REVIEW.md)

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I53` | `true` | `4f821f97dcb4ba5854519a1255f41ee39f44b23e13b77663db966d82f8d23a25` | - | - |
| `phase_ii_format` | `U53` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z53` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE53` | `true` | `2e9acbd193d890e5d0f600256e74d7d5bed336fdf9360e3a30f6d7f0dc06ef3f` | 1. missing transition and state | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`4` / `4`
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
| `R45.DEBT.opaque_state_body_semantics` | 2 |
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

ClampingState --> InitialState : Braking Complete

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0051 named "llms_emp_feedback_final_0051" {
    event Brake_Signal_Received named "Brake Signal Received";
    event Signal_Transmission_Fails named "Signal Transmission Fails";
    event Entering_Clamping_State named "Entering Clamping State";
    event Signal_Feedback_Sent named "Signal Feedback Sent";
    event Braking_Complete named "Braking Complete";
    state InitialState named "InitialState\n[PlantUML body] Initial State";
    state BrakingState named "BrakingState";
    state OperationalState named "OperationalState";
    state ClampingState named "ClampingState\n[PlantUML body] Brake Caliper Clamping State";
    [*] -> InitialState;
    InitialState -> BrakingState : /Brake_Signal_Received;
    InitialState -> OperationalState : /Signal_Transmission_Fails;
    BrakingState -> ClampingState : /Entering_Clamping_State;
    OperationalState -> InitialState : /Signal_Feedback_Sent;
    BrakingState -> InitialState : /Signal_Feedback_Sent;
    ClampingState -> InitialState : /Braking_Complete;
}
```

[上一组 `0050`](../0050/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0052`](../0052/README.md)
