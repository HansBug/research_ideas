# Pair `0053`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0052`](../0052/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0054`](../0054/README.md)

- LLM：`Claude`
- 模型/场景：Pump Control state machine
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE55`；Excel row：`55`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`ce9980726ff386e89f12448d5c9cfd123590e6b3e804649ff6c3928054a1edc3`
- NL SHA-256：`a391765dba935d89e6d2467c97b218c0136d106ea9c00bac91e6525e28ac04f1`
- PlantUML SHA-256：`b153279f857c7cd61ea92a60e3970d39454d2199a56f999942f4647031b81211`
- FCSTM SHA-256：`1b5b33eae1325d5a5b9b28fef84be55c8b4f4a294b69db95f38af2e48a8edf1b`
- review subject SHA-256：`143d4a8c97e2b70eb2f89547d49e40492bf59882ceff3af2718225bd1ca28879`
- working contract SHA-256：`daedf6474f76665026eb5892c6ae12b53a1f600923777aadfc93ab6129c2afdf`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `4`
- mapped / blocked / silent drop：`4` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `3/3`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `4`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`14` / `7` / `0`
- source macro / positive identity trace / conversion boundary trace：`7` / `14` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0053 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0053.puml:line:5\|state PumpControl {, source-ref:llms_emp_feedback_final_0053.puml:line:3\|[*] --> PumpControl`；FCSTM anchors：`element-ref:source:state:PumpControl@line:2\|state PumpControl named "PumpControl" {, element-ref:compiler:transition_segment:tr_0001:segment:1@line:18\|[*] -> PumpControl;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0053.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0053.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0053.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0053.json) | [source trace](../../source_traces/llms_emp_feedback_final_0053.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | PumpControl | source-ref:llms_emp_feedback_final_0053.puml:line:5\|state PumpControl { | element-ref:source:state:PumpControl@line:2\|state PumpControl named "PumpControl" { | source:state:PumpControl | - | Case 0053 binds source:state:PumpControl to authored PlantUML occurrence 'state PumpControl {' and current FCSTM occurrence 'state PumpControl named "PumpControl" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | PumpControl | source-ref:llms_emp_feedback_final_0053.puml:line:3\|[*] --> PumpControl | element-ref:compiler:transition_segment:tr_0001:segment:1@line:18\|[*] -> PumpControl; | source:transition:tr_0001 | compiler:transition_segment:tr_0001:segment:1 | Case 0053 binds source:transition:tr_0001 to authored PlantUML occurrence '[*] --> PumpControl' and current FCSTM occurrence '[*] -> PumpControl;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:synthetic_state:0001:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0053.puml:line:5\|state PumpControl { | element-ref:compiler:state:llms_emp_feedback_final_0053.PumpControl.UnspecifiedInitial@line:15\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:PumpControl@line:2\|state PumpControl named "PumpControl" { | compiler:state:llms_emp_feedback_final_0053.PumpControl.UnspecifiedInitial, source:state:PumpControl | Case 0053 synthetic_state occurrence review:synthetic_state:0001:001-UnspecifiedInitial binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0053.PumpControl.UnspecifiedInitial, source:state:PumpControl. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I55` | `true` | `ce9980726ff386e89f12448d5c9cfd123590e6b3e804649ff6c3928054a1edc3` | - | - |
| `phase_ii_format` | `U55` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z55` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE55` | `true` | `b153279f857c7cd61ea92a60e3970d39454d2199a56f999942f4647031b81211` | 1. missing regions | 1.0 |

## Official identity ledger

- status：`aligned`
- canonical / official states：`7` / `7`
- aligned transition endpoints：`4`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.missing_explicit_initial` | 1 |
| `R45.DEBT.opaque_state_body_semantics` | 3 |

## NL

```text
1. The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions.
2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState.
3. The system first transitions to the PumpState substate, where the pump is activated or controlled.
4. The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow.
5. Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml

[*] --> PumpControl

state PumpControl {
state PumpRegion {
[*] --> PumpState
PumpState : Pump activated or controlled
}

state WaterRegion {
[*] --> WaterState
WaterState : Water flow control/monitoring
}

state MethaneRegion {
[*] --> MethaneState
MethaneState : Methane flow control/monitoring
}
}

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0053 named "llms_emp_feedback_final_0053" {
    state PumpControl named "PumpControl" {
        state PumpRegion named "PumpRegion" {
            state PumpState named "PumpState\n[PlantUML body] Pump activated or controlled";
            [*] -> PumpState;
        }
        state WaterRegion named "WaterRegion" {
            state WaterState named "WaterState\n[PlantUML body] Water flow control/monitoring";
            [*] -> WaterState;
        }
        state MethaneRegion named "MethaneRegion" {
            state MethaneState named "MethaneState\n[PlantUML body] Methane flow control/monitoring";
            [*] -> MethaneState;
        }
        state UnspecifiedInitial named "Unspecified initial";
        [*] -> UnspecifiedInitial;
    }
    [*] -> PumpControl;
}
```

[上一组 `0052`](../0052/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0054`](../0054/README.md)
