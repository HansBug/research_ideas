# Pair `0046`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0045`](../0045/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0047`](../0047/README.md)

- LLM：`DeepSeek`
- 模型/场景：UAV swarm state machine diagram
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE48`；Excel row：`48`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`709704f395b88943b357c62d4b4c1f93cb2b1e09ef0f72f8f26648de311b99fc`
- NL SHA-256：`a01c022f5380700b6c13800497291640b4d64abbadce1d8984be0c14880ebeb3`
- PlantUML SHA-256：`de64704c2571b8915067365e1dfe1b336b93228e5776eeca7fcf92a9a29d9ddc`
- FCSTM SHA-256：`01ea38a2c439aea4a06d866dee2ca8fd52cee5c1120de6d88b3db1da8d8492a5`
- review subject SHA-256：`4b6ad1c16fe3f9af1fcef278c2d4dfbb5ae45d31fbde325be2459e74a8384a7a`
- working contract SHA-256：`cf32dc7dcb75a451ecde7e98613137323d5cd31b84f3c8d42acf28911160af85`
- 结构裁决：`structure_preserved`
- source states / transitions：`9` / `10`
- mapped / blocked / silent drop：`10` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `6/6`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`9` / `10`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`25` / `21` / `0`
- source macro / positive identity trace / conversion boundary trace：`16` / `25` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0046 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0046.puml:line:2\|state UAVSwarmStateMachine {, source-ref:llms_emp_feedback_final_0046.puml:line:9\|Searching --> FormationAdjustment : Intercepted`；FCSTM anchors：`element-ref:source:state:UAVSwarmStateMachine@line:9\|state UAVSwarmStateMachine named "UAVSwarmStateMachine" {, element-ref:compiler:transition_segment:tr_0003:segment:1@line:18\|Searching -> FormationAdjustment : /Intercepted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0046.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0046.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0046.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0046.json) | [source trace](../../source_traces/llms_emp_feedback_final_0046.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 This state machine model describes the state transitions of a UAV swarm. | source-ref:llms_emp_feedback_final_0046.puml:line:2\|state UAVSwarmStateMachine { | element-ref:source:state:UAVSwarmStateMachine@line:9\|state UAVSwarmStateMachine named "UAVSwarmStateMachine" { | source:state:UAVSwarmStateMachine | - | Case 0046 binds source:state:UAVSwarmStateMachine to the exact authored occurrence 'state UAVSwarmStateMachine {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | intercepted | source-ref:llms_emp_feedback_final_0046.puml:line:9\|Searching --> FormationAdjustment : Intercepted | element-ref:compiler:transition_segment:tr_0003:segment:1@line:18\|Searching -> FormationAdjustment : /Intercepted; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0046 binds source:transition:tr_0003 to the exact authored occurrence 'Searching --> FormationAdjustment : Intercepted'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:synthetic_state:0001:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0046.puml:line:2\|state UAVSwarmStateMachine { | element-ref:compiler:state:llms_emp_feedback_final_0046.UnspecifiedInitial@line:8\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:UAVSwarmStateMachine@line:9\|state UAVSwarmStateMachine named "UAVSwarmStateMachine" { | compiler:state:llms_emp_feedback_final_0046.UnspecifiedInitial, source:state:UAVSwarmStateMachine | Case 0046 risk synthetic_state occurrence review:synthetic_state:0001:001-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0002:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0046.puml:line:2\|state UAVSwarmStateMachine { | element-ref:compiler:state:llms_emp_feedback_final_0046.UAVSwarmStateMachine.UnspecifiedInitial@line:10\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:UAVSwarmStateMachine@line:9\|state UAVSwarmStateMachine named "UAVSwarmStateMachine" { | compiler:state:llms_emp_feedback_final_0046.UAVSwarmStateMachine.UnspecifiedInitial, source:state:UAVSwarmStateMachine | Case 0046 risk synthetic_state occurrence review:synthetic_state:0002:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I48` | `true` | `709704f395b88943b357c62d4b4c1f93cb2b1e09ef0f72f8f26648de311b99fc` | - | - |
| `phase_ii_format` | `U48` | `true` | `b3023ff8047c0dfd30780c30a8e285c085a73de7857077baa08c47655bfa297c` | syntax error: stm UAVSwarmStateMachine [UAV Swarm State Machine] | YES |
| `phase_ii_grammar` | `Z48` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE48` | `true` | `de64704c2571b8915067365e1dfe1b336b93228e5776eeca7fcf92a9a29d9ddc` | 1. missing regions | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`9` / `9`
- aligned transition endpoints：`10`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.missing_explicit_initial` | 2 |
| `R45.DEBT.opaque_state_body_semantics` | 6 |
| `R45.DEBT.opaque_transition_label_semantics` | 8 |

## NL

```text
1 This state machine model describes the state transitions of a UAV swarm.
2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas.
3 When the UAV swarm is intercepted, it transitions to the formation adjustment state.
4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
state UAVSwarmStateMachine {
state SearchRegion {
[*] --> Idle
Idle : Initial State

Idle --> Searching : Start Mission
Searching : Target Search State
Searching --> FormationAdjustment : Intercepted
Searching --> Attacking : Task Assignment Received

FormationAdjustment : Formation Adjustment State
FormationAdjustment --> Searching : Formation Adjusted

Attacking : Attack State
Attacking --> Searching : Attack Completed / UAV Count Decreased
}

state MissionRegion {
[*] --> MissionActive
MissionActive : Mission Active State
MissionActive --> MissionComplete : Mission Completed
MissionComplete : Mission Complete State
}
}

SearchRegion --> MissionRegion : Mission Completed
MissionRegion --> SearchRegion : Start Mission

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0046 named "llms_emp_feedback_final_0046" {
    event Start_Mission named "Start Mission";
    event Intercepted named "Intercepted";
    event Task_Assignment_Received named "Task Assignment Received";
    event Formation_Adjusted named "Formation Adjusted";
    event Attack_Completed_UAV_Count_Decreased named "Attack Completed / UAV Count Decreased";
    event Mission_Completed named "Mission Completed";
    state UnspecifiedInitial named "Unspecified initial";
    state UAVSwarmStateMachine named "UAVSwarmStateMachine" {
        state UnspecifiedInitial named "Unspecified initial";
        state SearchRegion named "SearchRegion" {
            state Idle named "Idle\n[PlantUML body] Initial State";
            state Searching named "Searching\n[PlantUML body] Target Search State";
            state FormationAdjustment named "FormationAdjustment\n[PlantUML body] Formation Adjustment State";
            state Attacking named "Attacking\n[PlantUML body] Attack State";
            [*] -> Idle;
            Idle -> Searching : /Start_Mission;
            Searching -> FormationAdjustment : /Intercepted;
            Searching -> Attacking : /Task_Assignment_Received;
            FormationAdjustment -> Searching : /Formation_Adjusted;
            Attacking -> Searching : /Attack_Completed_UAV_Count_Decreased;
        }
        state MissionRegion named "MissionRegion" {
            state MissionActive named "MissionActive\n[PlantUML body] Mission Active State";
            state MissionComplete named "MissionComplete\n[PlantUML body] Mission Complete State";
            [*] -> MissionActive;
            MissionActive -> MissionComplete : /Mission_Completed;
        }
        !SearchRegion -> MissionRegion : /Mission_Completed;
        !MissionRegion -> SearchRegion : /Start_Mission;
        [*] -> UnspecifiedInitial;
    }
    [*] -> UnspecifiedInitial;
}
```

[上一组 `0045`](../0045/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0047`](../0047/README.md)
