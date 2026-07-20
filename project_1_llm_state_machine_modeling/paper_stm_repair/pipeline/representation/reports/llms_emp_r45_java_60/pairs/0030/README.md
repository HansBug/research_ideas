# Pair `0030`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0029`](../0029/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0031`](../0031/README.md)

- LLM：`Kimi`
- 模型/场景：high-level driving module
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE32`；Excel row：`32`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`e1c89866e4ea2332ca45c2755508cf1c0742595876037ba3c3d0ae7f10feb9c9`
- NL SHA-256：`f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`
- PlantUML SHA-256：`3a57437b4affea98105ee794349865f92f42e01865786658aeeaf6529c76237a`
- FCSTM SHA-256：`b8c4c02d4b8e6d1ecc53e5d9bd442aba3a0dbc24eeeccf34a9362d66f1b7ea8a`
- review subject SHA-256：`28fbd0eb49957fd0bd7cd939eba45bc24b3aa3053513cb258620bade78bcd6ea`
- working contract SHA-256：`21a5dac1d5342985e099eb9f6be203d786788d65c461cefe4889d7d07258fac2`
- 结构裁决：`structure_preserved`
- source states / transitions：`4` / `7`
- mapped / blocked / silent drop：`7` / `0` / `0`
- final / lifecycle / body coverage：`1/1` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`4` / `7`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`11` / `18` / `0`
- source macro / positive identity trace / conversion boundary trace：`7` / `11` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0030 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences. Fresh v6 main-session review re-read NL, PlantUML, FCSTM, working contract, and source trace after the portable Java identity change; source/FCSTM/trace bytes are unchanged and verification remains fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0030.puml:line:4\|state HumanDriving {, source-ref:llms_emp_feedback_final_0030.puml:line:15\|HumanDriving --> Autonomous : front_distance > 10`；FCSTM anchors：`element-ref:source:state:HumanDriving@line:9\|state HumanDriving named "HumanDriving" {, element-ref:compiler:transition_segment:tr_0005:segment:1@line:22\|!HumanDriving -> Autonomous : /front_distance_10;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0030.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0030.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0030.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0030.json) | [source trace](../../source_traces/llms_emp_feedback_final_0030.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 The human driving mode is represented by a simple state. | source-ref:llms_emp_feedback_final_0030.puml:line:4\|state HumanDriving { | element-ref:source:state:HumanDriving@line:9\|state HumanDriving named "HumanDriving" { | source:state:HumanDriving | - | Case 0030 binds source:state:HumanDriving to the exact authored occurrence 'state HumanDriving {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | front_distance > 10 | source-ref:llms_emp_feedback_final_0030.puml:line:15\|HumanDriving --> Autonomous : front_distance > 10 | element-ref:compiler:transition_segment:tr_0005:segment:1@line:22\|!HumanDriving -> Autonomous : /front_distance_10; | source:transition:tr_0005 | compiler:transition_segment:tr_0005:segment:1 | Case 0030 binds source:transition:tr_0005 to the exact authored occurrence 'HumanDriving --> Autonomous : front_distance > 10'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0001` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0030.puml:line:2\|[*] --> HumanDriving : Power On | element-ref:compiler:state:llms_emp_feedback_final_0030.InitialWaittr_0001@line:8\|state InitialWaittr_0001 named "Awaiting initial event: Power On";, element-ref:compiler:transition_segment:tr_0001:segment:1@line:20\|[*] -> InitialWaittr_0001;, element-ref:compiler:transition_segment:tr_0001:segment:2@line:21\|InitialWaittr_0001 -> HumanDriving : /Power_On; | compiler:state:llms_emp_feedback_final_0030.InitialWaittr_0001, compiler:transition_segment:tr_0001:segment:1, compiler:transition_segment:tr_0001:segment:2, source:transition:tr_0001 | Case 0030 risk multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0001: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:final_boundary:0002:tr_0007` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0030.puml:line:18\|HumanDriving --> [*] : Power Off | element-ref:compiler:transition_segment:tr_0007:segment:1@line:24\|!HumanDriving -> [*] : /Power_Off; | compiler:transition_segment:tr_0007:segment:1, source:transition:tr_0007 | Case 0030 risk final_boundary occurrence review:final_boundary:0002:tr_0007: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:synthetic_state:0003:001-InitialWaittr_0001` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0030.puml:line:2\|[*] --> HumanDriving : Power On | element-ref:compiler:state:llms_emp_feedback_final_0030.InitialWaittr_0001@line:8\|state InitialWaittr_0001 named "Awaiting initial event: Power On"; | compiler:state:llms_emp_feedback_final_0030.InitialWaittr_0001, source:transition:tr_0001 | Case 0030 risk synthetic_state occurrence review:synthetic_state:0003:001-InitialWaittr_0001: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0004:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0030.puml:line:4\|state HumanDriving { | element-ref:compiler:state:llms_emp_feedback_final_0030.HumanDriving.UnspecifiedInitial@line:10\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:HumanDriving@line:9\|state HumanDriving named "HumanDriving" { | compiler:state:llms_emp_feedback_final_0030.HumanDriving.UnspecifiedInitial, source:state:HumanDriving | Case 0030 risk synthetic_state occurrence review:synthetic_state:0004:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I32` | `true` | `e1c89866e4ea2332ca45c2755508cf1c0742595876037ba3c3d0ae7f10feb9c9` | - | - |
| `phase_ii_format` | `U32` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z32` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE32` | `true` | `3a57437b4affea98105ee794349865f92f42e01865786658aeeaf6529c76237a` | 1. missing final state | 1.0 |

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
| `R45.DEBT.missing_explicit_initial` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 6 |

## NL

```text
1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
[*] --> HumanDriving : Power On

state HumanDriving {
}

state Autonomous {
state Navigating
state Parking
[*] --> Navigating
Navigating --> Parking : Park Request
Parking --> Navigating : Parking Complete
}

HumanDriving --> Autonomous : front_distance > 10
Autonomous --> HumanDriving : Human Steering Cmd / Brake Pressed / [*]

HumanDriving --> [*] : Power Off
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0030 named "llms_emp_feedback_final_0030" {
    event Power_On named "Power On";
    event Park_Request named "Park Request";
    event Parking_Complete named "Parking Complete";
    event front_distance_10 named "front_distance > 10";
    event Human_Steering_Cmd_Brake_Pressed named "Human Steering Cmd / Brake Pressed / [*]";
    event Power_Off named "Power Off";
    state InitialWaittr_0001 named "Awaiting initial event: Power On";
    state HumanDriving named "HumanDriving" {
        state UnspecifiedInitial named "Unspecified initial";
        [*] -> UnspecifiedInitial;
    }
    state Autonomous named "Autonomous" {
        state Navigating named "Navigating";
        state Parking named "Parking";
        [*] -> Navigating;
        Navigating -> Parking : /Park_Request;
        Parking -> Navigating : /Parking_Complete;
    }
    [*] -> InitialWaittr_0001;
    InitialWaittr_0001 -> HumanDriving : /Power_On;
    !HumanDriving -> Autonomous : /front_distance_10;
    !Autonomous -> HumanDriving : /Human_Steering_Cmd_Brake_Pressed;
    !HumanDriving -> [*] : /Power_Off;
}
```

[上一组 `0029`](../0029/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0031`](../0031/README.md)
