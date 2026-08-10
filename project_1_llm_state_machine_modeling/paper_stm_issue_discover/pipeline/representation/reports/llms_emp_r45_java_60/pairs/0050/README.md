# Pair `0050`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0049`](../0049/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0051`](../0051/README.md)

- LLM：`Claude`
- 模型/场景：high-level driving module
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE52`；Excel row：`52`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`false`
- Phase-I PlantUML SHA-256：`317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4`
- NL SHA-256：`f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`
- PlantUML SHA-256：`317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4`
- FCSTM SHA-256：`e1ff73267c5acdc5aa29721d4ad1c0e13a3ca756cbbc5b5af819627bf3fc3767`
- review subject SHA-256：`cc0a71d371522f98574f065c66fd03b4c9e52b331d31ad04d21076754db99023`
- working contract SHA-256：`c9a9f791897cdfaac696f9e6d65d05be0cb7313feb6d9415b614e99d5d8ff61e`
- 结构裁决：`structure_preserved`
- source states / transitions：`5` / `9`
- mapped / blocked / silent drop：`9` / `0` / `0`
- final / lifecycle / body coverage：`3/3` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`5` / `9`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`14` / `24` / `0`
- source macro / positive identity trace / conversion boundary trace：`9` / `14` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0050 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0050.puml:line:5\|state HumanDrivingMode {, source-ref:llms_emp_feedback_final_0050.puml:line:3\|[*] --> HumanDrivingMode : Power On`；FCSTM anchors：`element-ref:source:state:HumanDrivingMode@line:7\|state HumanDrivingMode named "HumanDrivingMode";, element-ref:compiler:transition_segment:tr_0001:segment:1@line:28\|[*] -> HumanDrivingMode : /Power_On;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0050.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0050.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0050.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0050.json) | [source trace](../../source_traces/llms_emp_feedback_final_0050.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 The human driving mode is represented by a simple state. | source-ref:llms_emp_feedback_final_0050.puml:line:5\|state HumanDrivingMode { | element-ref:source:state:HumanDrivingMode@line:7\|state HumanDrivingMode named "HumanDrivingMode"; | source:state:HumanDrivingMode | - | Case 0050 binds source:state:HumanDrivingMode to authored PlantUML occurrence 'state HumanDrivingMode {' and current FCSTM occurrence 'state HumanDrivingMode named "HumanDrivingMode";'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | power on | source-ref:llms_emp_feedback_final_0050.puml:line:3\|[*] --> HumanDrivingMode : Power On | element-ref:compiler:transition_segment:tr_0001:segment:1@line:28\|[*] -> HumanDrivingMode : /Power_On; | source:transition:tr_0001 | compiler:transition_segment:tr_0001:segment:1 | Case 0050 binds source:transition:tr_0001 to authored PlantUML occurrence '[*] --> HumanDrivingMode : Power On' and current FCSTM occurrence '[*] -> HumanDrivingMode : /Power_On;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0005` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0050.puml:line:12\|SubState3 --> [*] | element-ref:compiler:state:llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005@line:12\|state FinalWaittr_0005 named "Completed final boundary: AutonomousMode.SubState3";, element-ref:compiler:transition_segment:tr_0005:segment:1@line:16\|SubState3 -> FinalWaittr_0005; | compiler:state:llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005, compiler:transition_segment:tr_0005:segment:1, source:transition:tr_0005 | Case 0050 final_boundary occurrence review:final_boundary:0001:tr_0005 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005, compiler:transition_segment:tr_0005:segment:1, source:transition:tr_0005. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:multi_segment_macro:0002:tr_0007` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0050.puml:line:17\|AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final), source-ref:llms_emp_feedback_final_0050.puml:line:20\|AutonomousMode --> [*] : Power Off | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:17\|SubState1 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:2@line:18\|SubState2 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:3@line:19\|SubState3 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:4@line:26\|AutonomousMode -> HumanDrivingMode : if [R45RouteToken == 7] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0007:segment:5@line:23\|FinalWaittr_0005 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, compiler:transition_segment:tr_0007:segment:5, source:transition:tr_0007 | Case 0050 multi_segment_macro occurrence review:multi_segment_macro:0002:tr_0007 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, compiler:transition_segment:tr_0007:segment:5, source:transition:tr_0007. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0003:tr_0007` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0050.puml:line:17\|AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final), source-ref:llms_emp_feedback_final_0050.puml:line:20\|AutonomousMode --> [*] : Power Off | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:17\|SubState1 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:2@line:18\|SubState2 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:3@line:19\|SubState3 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:4@line:26\|AutonomousMode -> HumanDrivingMode : if [R45RouteToken == 7] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0007:segment:5@line:23\|FinalWaittr_0005 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, compiler:transition_segment:tr_0007:segment:5, source:transition:tr_0007 | Case 0050 route_controller occurrence review:route_controller:0003:tr_0007 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, compiler:transition_segment:tr_0007:segment:3, compiler:transition_segment:tr_0007:segment:4, compiler:transition_segment:tr_0007:segment:5, source:transition:tr_0007. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:final_boundary:0004:tr_0008` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0050.puml:line:19\|HumanDrivingMode --> [*] : Power Off | element-ref:compiler:transition_segment:tr_0008:segment:1@line:30\|HumanDrivingMode -> [*] : /Power_Off; | compiler:transition_segment:tr_0008:segment:1, source:transition:tr_0008 | Case 0050 final_boundary occurrence review:final_boundary:0004:tr_0008 binds exact source refs to working-contract elements compiler:transition_segment:tr_0008:segment:1, source:transition:tr_0008. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:multi_segment_macro:0005:tr_0009` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0050.puml:line:17\|AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final), source-ref:llms_emp_feedback_final_0050.puml:line:20\|AutonomousMode --> [*] : Power Off | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0009:segment:1@line:20\|SubState1 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:2@line:21\|SubState2 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:3@line:22\|SubState3 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:4@line:27\|AutonomousMode -> [*] : if [R45RouteToken == 9] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0009:segment:5@line:24\|FinalWaittr_0005 -> [*] : /Power_Off effect { R45RouteToken = 9; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, source:transition:tr_0009 | Case 0050 multi_segment_macro occurrence review:multi_segment_macro:0005:tr_0009 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, source:transition:tr_0009. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0006:tr_0009` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0050.puml:line:17\|AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final), source-ref:llms_emp_feedback_final_0050.puml:line:20\|AutonomousMode --> [*] : Power Off | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0009:segment:1@line:20\|SubState1 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:2@line:21\|SubState2 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:3@line:22\|SubState3 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:4@line:27\|AutonomousMode -> [*] : if [R45RouteToken == 9] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0009:segment:5@line:24\|FinalWaittr_0005 -> [*] : /Power_Off effect { R45RouteToken = 9; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, source:transition:tr_0009 | Case 0050 route_controller occurrence review:route_controller:0006:tr_0009 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, source:transition:tr_0009. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:final_boundary:0007:tr_0009` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0050.puml:line:17\|AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final), source-ref:llms_emp_feedback_final_0050.puml:line:20\|AutonomousMode --> [*] : Power Off | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0009:segment:1@line:20\|SubState1 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:2@line:21\|SubState2 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:3@line:22\|SubState3 -> [*] : /Power_Off effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:4@line:27\|AutonomousMode -> [*] : if [R45RouteToken == 9] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0009:segment:5@line:24\|FinalWaittr_0005 -> [*] : /Power_Off effect { R45RouteToken = 9; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, source:transition:tr_0009 | Case 0050 final_boundary occurrence review:final_boundary:0007:tr_0009 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, source:transition:tr_0009. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:synthetic_state:0008:001-FinalWaittr_0005` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0050.puml:line:12\|SubState3 --> [*] | element-ref:compiler:state:llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005@line:12\|state FinalWaittr_0005 named "Completed final boundary: AutonomousMode.SubState3"; | compiler:state:llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005, source:transition:tr_0005 | Case 0050 synthetic_state occurrence review:synthetic_state:0008:001-FinalWaittr_0005 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005, source:transition:tr_0005. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I52` | `true` | `317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4` | - | - |
| `phase_ii_format` | `U52` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z52` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE52` | `true` | `317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`5` / `5`
- aligned transition endpoints：`9`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.composite_source_activation_dispatch` | 2 |
| `R45.DEBT.opaque_transition_label_semantics` | 5 |

## NL

```text
1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml

[*] --> HumanDrivingMode : Power On

state HumanDrivingMode {
}

state AutonomousMode {
[*] --> SubState1
SubState1 --> SubState2
SubState2 --> SubState3
SubState3 --> [*]
}

HumanDrivingMode --> AutonomousMode : [front_distance > 10]

AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final)

HumanDrivingMode --> [*] : Power Off
AutonomousMode --> [*] : Power Off

@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0050 named "llms_emp_feedback_final_0050" {
    event Power_On named "Power On";
    event _front_distance_10 named "[front_distance > 10]";
    event human_steering_cmd_nor_brake_pressed_nor_in_auto_final named "human steering cmd\\nor brake pressed\\nor in (auto final)";
    event Power_Off named "Power Off";
    state HumanDrivingMode named "HumanDrivingMode";
    state AutonomousMode named "AutonomousMode" {
        state SubState1 named "SubState1";
        state SubState2 named "SubState2";
        state SubState3 named "SubState3";
        state FinalWaittr_0005 named "Completed final boundary: AutonomousMode.SubState3";
        [*] -> SubState1;
        SubState1 -> SubState2;
        SubState2 -> SubState3;
        SubState3 -> FinalWaittr_0005;
        SubState1 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };
        SubState2 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };
        SubState3 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };
        SubState1 -> [*] : /Power_Off effect { R45RouteToken = 9; };
        SubState2 -> [*] : /Power_Off effect { R45RouteToken = 9; };
        SubState3 -> [*] : /Power_Off effect { R45RouteToken = 9; };
        FinalWaittr_0005 -> [*] : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final effect { R45RouteToken = 7; };
        FinalWaittr_0005 -> [*] : /Power_Off effect { R45RouteToken = 9; };
    }
    AutonomousMode -> HumanDrivingMode : if [R45RouteToken == 7] effect { R45RouteToken = 0; };
    AutonomousMode -> [*] : if [R45RouteToken == 9] effect { R45RouteToken = 0; };
    [*] -> HumanDrivingMode : /Power_On;
    HumanDrivingMode -> AutonomousMode : /_front_distance_10;
    HumanDrivingMode -> [*] : /Power_Off;
}
```

[上一组 `0049`](../0049/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0051`](../0051/README.md)
