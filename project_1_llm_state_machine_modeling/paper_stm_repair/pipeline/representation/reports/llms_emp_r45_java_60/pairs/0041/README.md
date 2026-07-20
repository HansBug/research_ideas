# Pair `0041`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0040`](../0040/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0042`](../0042/README.md)

- LLM：`DeepSeek`
- 模型/场景：State machine diagram of the base brake subsystem
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE43`；Excel row：`43`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`9dc040506c4abc2dc1dcee5536542e17a8b464277dc7f108c2a94941e969675e`
- NL SHA-256：`abb20a2187c100d7c75a3038df101c91b369df70a07dfafd6eafc72da859fc99`
- PlantUML SHA-256：`e574376ae58008bc3a246f72be7d4a125ae6846baa8d18045aeadf606839e1a4`
- FCSTM SHA-256：`9ca8bbb255d959d2b7d4142ed0d3d2fd48f0a12437ad6e68137142b5df5cd422`
- review subject SHA-256：`9bb4a90db43246fad84de236eb311ac72ae90b98040a3d966c521dfd3aeab2b2`
- working contract SHA-256：`a41d3c71b1dd78d3dd0e4e9f4a4cb276c1e9c9e70028477a22f364c5ea1763de`
- 结构裁决：`structure_preserved`
- source states / transitions：`4` / `8`
- mapped / blocked / silent drop：`8` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `2/2`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`4` / `8`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`14` / `15` / `0`
- source macro / positive identity trace / conversion boundary trace：`10` / `14` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0041 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0041.puml:line:2\|[*] --> InitialState, source-ref:llms_emp_feedback_final_0041.puml:line:6\|InitialState --> OperationalState : Signal Transmission Fails`；FCSTM anchors：`element-ref:source:state:InitialState@line:8\|state InitialState named "InitialState\n[PlantUML body] Initial State";, element-ref:compiler:transition_segment:tr_0003:segment:1@line:14\|InitialState -> OperationalState : /Signal_Transmission_Fails;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0041.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0041.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0041.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0041.json) | [source trace](../../source_traces/llms_emp_feedback_final_0041.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 This state machine model represents the train's basic braking device, which serves as the final execution unit for | source-ref:llms_emp_feedback_final_0041.puml:line:2\|[*] --> InitialState | element-ref:source:state:InitialState@line:8\|state InitialState named "InitialState\n[PlantUML body] Initial State"; | source:state:InitialState | - | Case 0041 binds source:state:InitialState to the exact authored occurrence '[*] --> InitialState'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | signal transmission fails | source-ref:llms_emp_feedback_final_0041.puml:line:6\|InitialState --> OperationalState : Signal Transmission Fails | element-ref:compiler:transition_segment:tr_0003:segment:1@line:14\|InitialState -> OperationalState : /Signal_Transmission_Fails; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0041 binds source:transition:tr_0003 to the exact authored occurrence 'InitialState --> OperationalState : Signal Transmission Fails'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

本组不要求 risk-tag 第二遍复核。

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I43` | `true` | `9dc040506c4abc2dc1dcee5536542e17a8b464277dc7f108c2a94941e969675e` | - | - |
| `phase_ii_format` | `U43` | `true` | `566d10146e2e3b6bc3d510cbe29ece0c2dfa104ea0f4230be1989f6fe3112b2e` | syntax error: stm BasicBrakingDevice [State Machine Diagram] | YES |
| `phase_ii_grammar` | `Z43` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE43` | `true` | `e574376ae58008bc3a246f72be7d4a125ae6846baa8d18045aeadf606839e1a4` | 1. missing transition and states | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`4` / `4`
- aligned transition endpoints：`8`

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
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

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

ClampingState --> BrakingState : Brake Signal Maintained
ClampingState --> InitialState : Brake Signal Released

OperationalState --> InitialState : Signal Feedback Sent
BrakingState --> InitialState : Signal Feedback Sent
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0041 named "llms_emp_feedback_final_0041" {
    event Brake_Signal_Received named "Brake Signal Received";
    event Signal_Transmission_Fails named "Signal Transmission Fails";
    event Entering_Clamping_State named "Entering Clamping State";
    event Brake_Signal_Maintained named "Brake Signal Maintained";
    event Brake_Signal_Released named "Brake Signal Released";
    event Signal_Feedback_Sent named "Signal Feedback Sent";
    state InitialState named "InitialState\n[PlantUML body] Initial State";
    state BrakingState named "BrakingState";
    state OperationalState named "OperationalState";
    state ClampingState named "ClampingState\n[PlantUML body] Brake Caliper Clamping State";
    [*] -> InitialState;
    InitialState -> BrakingState : /Brake_Signal_Received;
    InitialState -> OperationalState : /Signal_Transmission_Fails;
    BrakingState -> ClampingState : /Entering_Clamping_State;
    ClampingState -> BrakingState : /Brake_Signal_Maintained;
    ClampingState -> InitialState : /Brake_Signal_Released;
    OperationalState -> InitialState : /Signal_Feedback_Sent;
    BrakingState -> InitialState : /Signal_Feedback_Sent;
}
```

[上一组 `0040`](../0040/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0042`](../0042/README.md)
