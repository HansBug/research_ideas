# Pair `0028`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0027`](../0027/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0029`](../0029/README.md)

- LLM：`Llama`
- 模型/场景： Digital camera state machine diagrams
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE30`；Excel row：`30`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`ef9eb75e567c05b8516af0e319003e7de3b473791a3b76727595941bb1716d36`
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`57c45db265e62b495d63f22e70b0b2bdaa25a85983874937be0384262621833a`
- FCSTM SHA-256：`fd1af48c412cdbc3c80d16f00125876c1af10a762b6f97bc19a0f91611c7cbc5`
- review subject SHA-256：`58200944c29e61904b08aeb3b2b4271936e90eda9aa13844fe14012ccd0b3df4`
- working contract SHA-256：`ec8bc7697ad89b1753ea7fd4f2f3f5ac980a639a0f4e7be6f1a28f4e8293ee23`
- 结构裁决：`structure_preserved`
- source states / transitions：`6` / `15`
- mapped / blocked / silent drop：`15` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `6/6`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`6` / `15`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`27` / `26` / `0`
- source macro / positive identity trace / conversion boundary trace：`21` / `27` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0028 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0028.puml:line:2\|state DoorShut as "Door Shut" <<initial>>, source-ref:llms_emp_feedback_final_0028.puml:line:20\|ReadytoCook --> Cooking : Start`；FCSTM anchors：`element-ref:source:state:DoorShut@line:11\|state DoorShut named "DoorShut\n[PlantUML body] as \"Door Shut\" <<initial>>";, element-ref:compiler:transition_segment:tr_0012:segment:1@line:29\|ReadytoCook -> Cooking : /Start;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0028.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0028.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0028.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0028.json) | [source trace](../../source_traces/llms_emp_feedback_final_0028.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | The system begins in the TurnOn state, which has two possible execution times, with a maximum of 2 seconds and a | source-ref:llms_emp_feedback_final_0028.puml:line:2\|state DoorShut as "Door Shut" <<initial>> | element-ref:source:state:DoorShut@line:11\|state DoorShut named "DoorShut\n[PlantUML body] as \"Door Shut\" <<initial>>"; | source:state:DoorShut | - | Case 0028 binds source:state:DoorShut to authored PlantUML occurrence 'state DoorShut as "Door Shut" <<initial>>' and current FCSTM occurrence 'state DoorShut named "DoorShut\n[PlantUML body] as \"Door Shut\" <<initial>>";'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | start | source-ref:llms_emp_feedback_final_0028.puml:line:20\|ReadytoCook --> Cooking : Start | element-ref:compiler:transition_segment:tr_0012:segment:1@line:29\|ReadytoCook -> Cooking : /Start; | source:transition:tr_0012 | compiler:transition_segment:tr_0012:segment:1 | Case 0028 binds source:transition:tr_0012 to authored PlantUML occurrence 'ReadytoCook --> Cooking : Start' and current FCSTM occurrence 'ReadytoCook -> Cooking : /Start;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:synthetic_state:0001:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0028.puml:line:2\|state DoorShut as "Door Shut" <<initial>>, source-ref:llms_emp_feedback_final_0028.puml:line:3\|state DoorOpen as "Door Open", source-ref:llms_emp_feedback_final_0028.puml:line:4\|state DoorOpenWithItem as "Door Open with Item", source-ref:llms_emp_feedback_final_0028.puml:line:5\|state DoorShutWithItem as "Door Shut with Item", source-ref:llms_emp_feedback_final_0028.puml:line:6\|state ReadytoCook as "Ready to Cook", source-ref:llms_emp_feedback_final_0028.puml:line:7\|state Cooking as "Cooking" | element-ref:compiler:state:llms_emp_feedback_final_0028.UnspecifiedInitial@line:10\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:Cooking@line:16\|state Cooking named "Cooking\n[PlantUML body] as \"Cooking\"";, element-ref:source:state:DoorOpen@line:12\|state DoorOpen named "DoorOpen\n[PlantUML body] as \"Door Open\"";, element-ref:source:state:DoorOpenWithItem@line:13\|state DoorOpenWithItem named "DoorOpenWithItem\n[PlantUML body] as \"Door Open with Item\"";, element-ref:source:state:DoorShut@line:11\|state DoorShut named "DoorShut\n[PlantUML body] as \"Door Shut\" <<initial>>";, element-ref:source:state:DoorShutWithItem@line:14\|state DoorShutWithItem named "DoorShutWithItem\n[PlantUML body] as \"Door Shut with Item\"";, element-ref:source:state:ReadytoCook@line:15\|state ReadytoCook named "ReadytoCook\n[PlantUML body] as \"Ready to Cook\""; | compiler:state:llms_emp_feedback_final_0028.UnspecifiedInitial, source:state:Cooking, source:state:DoorOpen, source:state:DoorOpenWithItem, source:state:DoorShut, source:state:DoorShutWithItem, source:state:ReadytoCook | Case 0028 synthetic_state occurrence review:synthetic_state:0001:001-UnspecifiedInitial binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0028.UnspecifiedInitial, source:state:Cooking, source:state:DoorOpen, source:state:DoorOpenWithItem, source:state:DoorShut, source:state:DoorShutWithItem, source:state:ReadytoCook. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I30` | `true` | `ef9eb75e567c05b8516af0e319003e7de3b473791a3b76727595941bb1716d36` | - | - |
| `phase_ii_format` | `U30` | `true` | `f67f5822ca1241f6e95e9d90361f2610ba8fb61662c13c4245d1c8d358560cc2` | 1.syntax error: stm CameraSystem<br>2. syntax error: TurnOff --> [*] | YES |
| `phase_ii_grammar` | `Z30` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE30` | `true` | `57c45db265e62b495d63f22e70b0b2bdaa25a85983874937be0384262621833a` | 1. missing transitions<br>2. interaction error | 1.0 |

## Official identity ledger

- status：`aligned`
- canonical / official states：`6` / `6`
- aligned transition endpoints：`15`

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
| `R45.DEBT.opaque_state_body_semantics` | 6 |
| `R45.DEBT.opaque_transition_label_semantics` | 15 |

## NL

```text
1. The system begins in the TurnOn state, which has two possible execution times, with a maximum of 2 seconds and a minimum of 2 seconds, before transitioning to the fork1 state.
2. The TurnOn state transitions into a fork1 state, which contains parallel paths leading to AutoFocus and DetLight.
3. The AutoFocus state has execution times of 2 seconds maximum and 1 second minimum before proceeding to the choice1 state, which is triggered when the condition memFull=true is true.
4. The DetLight state has execution times of 1 second maximum and 0 seconds minimum, transitioning to the choice2 state when the condition <>{prob=0.4} is met.
5. If the fork1 state transitions to choice3, it proceeds to the ChargedFlash state, which has execution times of 4 seconds maximum and 2 seconds minimum.
6. The ChargedFlash state can lead to Junction3, where the system starts and proceeds to the Join2 state. The transition occurs when Charged=true.
7. The choice3 state also transitions to Junction3, and once the system reaches Junction3, it joins the Join2 state.
8. The choice2 state transitions to Join2, and if the condition sunny=true is met, it further joins the Join1 state, which leads to Junction2.
9. In the Junction2 state, the system proceeds to TakePicture, followed by WriteMemory, with execution times of 3 seconds maximum and 2 seconds minimum.
10. After WriteMemory completes, the system enters Junction1 before proceeding to TurnOff, which ends the process and transitions back to the initial state, represented by [*].
11. In the Fork2 state, which is part of the Join2 substate, the system can either proceed to Junction2 or Flash. If the Flash state is activated, it transitions to Terminate, ending the sequence.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
state DoorShut as "Door Shut" <<initial>>
state DoorOpen as "Door Open"
state DoorOpenWithItem as "Door Open with Item"
state DoorShutWithItem as "Door Shut with Item"
state ReadytoCook as "Ready to Cook"
state Cooking as "Cooking"

DoorShut --> DoorOpen : Door Opened
DoorShut --> DoorShut : Cancel
DoorOpen --> DoorShut : Door Closed
DoorOpen --> DoorOpenWithItem : Item Placed
DoorOpenWithItem --> DoorOpen : Item Removed
DoorOpenWithItem --> DoorShutWithItem : Door Closed
DoorOpenWithItem --> ReadytoCook : Cooking Time Entered
DoorShutWithItem --> DoorOpenWithItem : Door Opened
DoorShutWithItem --> ReadytoCook : Cooking Time Entered
ReadytoCook --> DoorShutWithItem : Cancel
ReadytoCook --> DoorOpenWithItem : Door Opened
ReadytoCook --> Cooking : Start
Cooking --> DoorOpenWithItem : Door Opened
Cooking --> DoorShutWithItem : Timer Expired
Cooking --> ReadytoCook : Cancel
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0028 named "llms_emp_feedback_final_0028" {
    event Door_Opened named "Door Opened";
    event Cancel named "Cancel";
    event Door_Closed named "Door Closed";
    event Item_Placed named "Item Placed";
    event Item_Removed named "Item Removed";
    event Cooking_Time_Entered named "Cooking Time Entered";
    event Start named "Start";
    event Timer_Expired named "Timer Expired";
    state UnspecifiedInitial named "Unspecified initial";
    state DoorShut named "DoorShut\n[PlantUML body] as \"Door Shut\" <<initial>>";
    state DoorOpen named "DoorOpen\n[PlantUML body] as \"Door Open\"";
    state DoorOpenWithItem named "DoorOpenWithItem\n[PlantUML body] as \"Door Open with Item\"";
    state DoorShutWithItem named "DoorShutWithItem\n[PlantUML body] as \"Door Shut with Item\"";
    state ReadytoCook named "ReadytoCook\n[PlantUML body] as \"Ready to Cook\"";
    state Cooking named "Cooking\n[PlantUML body] as \"Cooking\"";
    [*] -> UnspecifiedInitial;
    DoorShut -> DoorOpen : /Door_Opened;
    DoorShut -> DoorShut : /Cancel;
    DoorOpen -> DoorShut : /Door_Closed;
    DoorOpen -> DoorOpenWithItem : /Item_Placed;
    DoorOpenWithItem -> DoorOpen : /Item_Removed;
    DoorOpenWithItem -> DoorShutWithItem : /Door_Closed;
    DoorOpenWithItem -> ReadytoCook : /Cooking_Time_Entered;
    DoorShutWithItem -> DoorOpenWithItem : /Door_Opened;
    DoorShutWithItem -> ReadytoCook : /Cooking_Time_Entered;
    ReadytoCook -> DoorShutWithItem : /Cancel;
    ReadytoCook -> DoorOpenWithItem : /Door_Opened;
    ReadytoCook -> Cooking : /Start;
    Cooking -> DoorOpenWithItem : /Door_Opened;
    Cooking -> DoorShutWithItem : /Timer_Expired;
    Cooking -> ReadytoCook : /Cancel;
}
```

[上一组 `0027`](../0027/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0029`](../0029/README.md)
