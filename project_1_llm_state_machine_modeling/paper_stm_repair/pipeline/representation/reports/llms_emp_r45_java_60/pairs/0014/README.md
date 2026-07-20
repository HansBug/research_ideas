# Pair `0014`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0013`](../0013/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0015`](../0015/README.md)

- LLM：`GPT-4`
- 模型/场景：state machine for Train Control
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE16`；Excel row：`16`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`711124b29144fbb337739a5e7d8d97d8b7cdacd5828e71a036f0bbbae40364fc`
- NL SHA-256：`3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce`
- PlantUML SHA-256：`36f37fba4bcf46ac2f33879309c90543d30aef033d1e692c83272858bbf45876`
- FCSTM SHA-256：`11c39b60937cace57632d6cb9ac9d6aef1c439b7fbee8ce0c1b9e11af832115d`
- review subject SHA-256：`531a165c061ac679c4fa399b1f3c3dd4a6be0c6118ea16fd42a6e35b7a1c6ca7`
- working contract SHA-256：`c30306adc0948e55fce48ee85e818037d103618e76616b72a57ec8d69e89704e`
- 结构裁决：`structure_preserved`
- source states / transitions：`8` / `7`
- mapped / blocked / silent drop：`7` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `4/4`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`8` / `7`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`19` / `22` / `0`
- source macro / positive identity trace / conversion boundary trace：`11` / `19` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0014 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0014.puml:line:2\|state DoorsClosing, source-ref:llms_emp_feedback_final_0014.puml:line:4\|DoorsClosing --> InMotion: Closed/SendDeparted`；FCSTM anchors：`element-ref:source:state:DoorsClosing@line:9\|state DoorsClosing named "DoorsClosing";, element-ref:compiler:transition_segment:tr_0001:segment:1@line:30\|DoorsClosing -> InMotion : /Closed_SendDeparted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0014.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0014.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0014.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0014.json) | [source trace](../../source_traces/llms_emp_feedback_final_0014.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | DoorsClosing | source-ref:llms_emp_feedback_final_0014.puml:line:2\|state DoorsClosing | element-ref:source:state:DoorsClosing@line:9\|state DoorsClosing named "DoorsClosing"; | source:state:DoorsClosing | - | Case 0014 binds source:state:DoorsClosing to the exact authored occurrence 'state DoorsClosing'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | Closed/SendDeparted | source-ref:llms_emp_feedback_final_0014.puml:line:4\|DoorsClosing --> InMotion: Closed/SendDeparted | element-ref:compiler:transition_segment:tr_0001:segment:1@line:30\|DoorsClosing -> InMotion : /Closed_SendDeparted; | source:transition:tr_0001 | compiler:transition_segment:tr_0001:segment:1 | Case 0014 binds source:transition:tr_0001 to the exact authored occurrence 'DoorsClosing --> InMotion: Closed/SendDeparted'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0002` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:7\|[*] --> Accelerating : Entry/Accelerate | element-ref:compiler:state:llms_emp_feedback_final_0014.InMotion.InitialWaittr_0002@line:17\|state InitialWaittr_0002 named "Awaiting initial event: Entry/Accelerate";, element-ref:compiler:transition_segment:tr_0002:segment:1@line:18\|[*] -> InitialWaittr_0002;, element-ref:compiler:transition_segment:tr_0002:segment:2@line:19\|InitialWaittr_0002 -> Accelerating : /Entry_Accelerate; | compiler:state:llms_emp_feedback_final_0014.InMotion.InitialWaittr_0002, compiler:transition_segment:tr_0002:segment:1, compiler:transition_segment:tr_0002:segment:2, source:transition:tr_0002 | Case 0014 risk multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0002: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:synthetic_state:0002:001-InitialWaittr_0002` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:7\|[*] --> Accelerating : Entry/Accelerate | element-ref:compiler:state:llms_emp_feedback_final_0014.InMotion.InitialWaittr_0002@line:17\|state InitialWaittr_0002 named "Awaiting initial event: Entry/Accelerate"; | compiler:state:llms_emp_feedback_final_0014.InMotion.InitialWaittr_0002, source:transition:tr_0002 | Case 0014 risk synthetic_state occurrence review:synthetic_state:0002:001-InitialWaittr_0002: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0003:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:2\|state DoorsClosing, source-ref:llms_emp_feedback_final_0014.puml:line:23\|state Stopping, source-ref:llms_emp_feedback_final_0014.puml:line:24\|state EmergencyStopping {, source-ref:llms_emp_feedback_final_0014.puml:line:6\|state InMotion { | element-ref:compiler:state:llms_emp_feedback_final_0014.UnspecifiedInitial@line:8\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:DoorsClosing@line:9\|state DoorsClosing named "DoorsClosing";, element-ref:source:state:EmergencyStopping@line:25\|state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Obstacle Detected" {, element-ref:source:state:InMotion@line:10\|state InMotion named "InMotion" {, element-ref:source:state:Stopping@line:24\|state Stopping named "Stopping"; | compiler:state:llms_emp_feedback_final_0014.UnspecifiedInitial, source:state:DoorsClosing, source:state:EmergencyStopping, source:state:InMotion, source:state:Stopping | Case 0014 risk synthetic_state occurrence review:synthetic_state:0003:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0004:003-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:14\|state Approaching { | element-ref:compiler:state:llms_emp_feedback_final_0014.InMotion.Approaching.UnspecifiedInitial@line:14\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:InMotion.Approaching@line:13\|state Approaching named "Approaching\n[PlantUML body] Nearing Destination\n[PlantUML body] Ready to Stop/Decelerate" { | compiler:state:llms_emp_feedback_final_0014.InMotion.Approaching.UnspecifiedInitial, source:state:InMotion.Approaching | Case 0014 risk synthetic_state occurrence review:synthetic_state:0004:003-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0005:004-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0014.puml:line:24\|state EmergencyStopping { | element-ref:compiler:state:llms_emp_feedback_final_0014.EmergencyStopping.UnspecifiedInitial@line:26\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:EmergencyStopping@line:25\|state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Obstacle Detected" { | compiler:state:llms_emp_feedback_final_0014.EmergencyStopping.UnspecifiedInitial, source:state:EmergencyStopping | Case 0014 risk synthetic_state occurrence review:synthetic_state:0005:004-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I16` | `true` | `711124b29144fbb337739a5e7d8d97d8b7cdacd5828e71a036f0bbbae40364fc` | - | - |
| `phase_ii_format` | `U16` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z16` | `true` | `36f37fba4bcf46ac2f33879309c90543d30aef033d1e692c83272858bbf45876` | cannot connect internal state to the composite state itself. | YES |
| `phase_ii_semantic` | `AE16` | `true` | `36f37fba4bcf46ac2f33879309c90543d30aef033d1e692c83272858bbf45876` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`8` / `8`
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
| `R45.DEBT.missing_explicit_initial` | 3 |
| `R45.DEBT.opaque_state_body_semantics` | 4 |
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

## NL

```text
1. The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal.
2. In the InMotion state, the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected.
3. When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal.
4. Within the InMotion state, the system operates in three substates: Accelerating, Cruising, and Approaching, which represent different phases of the train's motion.
5. The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal.
6. If the system is in the Accelerating substate and approaches its destination, it transitions to the Approaching substate upon receiving the "Approached/Decelerate" signal.
7. The system in the Cruising substate transitions to the Approaching substate when it approaches the destination, triggered by the "Approached/Decelerate" signal.
8. The system enters the Accelerating substate when motion begins, marked by the "Entry/Accelerate" action.
9. In the Approaching substate, the system sends the "Send" signal and continues to approach the destination.
10. The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
state DoorsClosing

DoorsClosing --> InMotion: Closed/SendDeparted

state InMotion {
[*] --> Accelerating : Entry/Accelerate
Accelerating --> Cruising : Reached Cruising/Cruise
Accelerating --> Approaching : Approached/Decelerate
Cruising --> Approaching : Approached/Decelerate

state Accelerating
state Cruising
state Approaching {
Approaching: Nearing Destination
Approaching: Ready to Stop/Decelerate
}
}

InMotion --> Stopping: Arrived/Stop, SendArrived
InMotion --> EmergencyStopping: Obstacle Detected

state Stopping
state EmergencyStopping {
Entry: Emergency Stop
EmergencyStopping: Obstacle Detected
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0014 named "llms_emp_feedback_final_0014" {
    event Closed_SendDeparted named "Closed/SendDeparted";
    event Entry_Accelerate named "Entry/Accelerate";
    event Reached_Cruising_Cruise named "Reached Cruising/Cruise";
    event Approached_Decelerate named "Approached/Decelerate";
    event Arrived_Stop_SendArrived named "Arrived/Stop, SendArrived";
    event Obstacle_Detected named "Obstacle Detected";
    state UnspecifiedInitial named "Unspecified initial";
    state DoorsClosing named "DoorsClosing";
    state InMotion named "InMotion" {
        state Accelerating named "Accelerating";
        state Cruising named "Cruising";
        state Approaching named "Approaching\n[PlantUML body] Nearing Destination\n[PlantUML body] Ready to Stop/Decelerate" {
            state UnspecifiedInitial named "Unspecified initial";
            [*] -> UnspecifiedInitial;
        }
        state InitialWaittr_0002 named "Awaiting initial event: Entry/Accelerate";
        [*] -> InitialWaittr_0002;
        InitialWaittr_0002 -> Accelerating : /Entry_Accelerate;
        Accelerating -> Cruising : /Reached_Cruising_Cruise;
        Accelerating -> Approaching : /Approached_Decelerate;
        Cruising -> Approaching : /Approached_Decelerate;
    }
    state Stopping named "Stopping";
    state EmergencyStopping named "EmergencyStopping\n[PlantUML body] Obstacle Detected" {
        state UnspecifiedInitial named "Unspecified initial";
        state Entry named "Entry\n[PlantUML body] Emergency Stop";
        [*] -> UnspecifiedInitial;
    }
    DoorsClosing -> InMotion : /Closed_SendDeparted;
    !InMotion -> Stopping : /Arrived_Stop_SendArrived;
    !InMotion -> EmergencyStopping : /Obstacle_Detected;
    [*] -> UnspecifiedInitial;
}
```

[上一组 `0013`](../0013/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0015`](../0015/README.md)
