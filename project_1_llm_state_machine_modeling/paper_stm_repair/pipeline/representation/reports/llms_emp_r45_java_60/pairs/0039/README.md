# Pair `0039`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0038`](../0038/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0040`](../0040/README.md)

- LLM：`Kimi`
- 模型/场景：autonomous mode
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE41`；Excel row：`41`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`false`
- Phase-I PlantUML SHA-256：`187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391`
- NL SHA-256：`b7425c44960b36c3534f118279e347786d4074191efea7bf9a7c5ba032c9e82c`
- PlantUML SHA-256：`187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391`
- FCSTM SHA-256：`b08cb9457a167036b218c27aff0df2c4570e4b419f61ce4030603894e90ce540`
- review subject SHA-256：`2eeb169de2d28a284680426da60451a5430d45d27810a3411857f4c253fa5998`
- working contract SHA-256：`f0fc1f8cf7f3bcc1f88ab3957e9a25e3197a53a70e4fae705e63edc215e6ef5e`
- 结构裁决：`structure_preserved`
- source states / transitions：`15` / `26`
- mapped / blocked / silent drop：`26` / `0` / `0`
- final / lifecycle / body coverage：`2/2` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`15` / `26`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`41` / `42` / `0`
- source macro / positive identity trace / conversion boundary trace：`26` / `41` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0039 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences. Fresh v6 main-session review re-read NL, PlantUML, FCSTM, working contract, and source trace after the portable Java identity change; source/FCSTM/trace bytes are unchanged and verification remains fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0039.puml:line:4\|state AutonomousMode {, source-ref:llms_emp_feedback_final_0039.puml:line:7\|InitialState --> HighwayMode : high_way=true`；FCSTM anchors：`element-ref:source:state:AutonomousMode@line:15\|state AutonomousMode named "AutonomousMode" {, element-ref:compiler:transition_segment:tr_0003:segment:1@line:48\|InitialState -> HighwayMode : /high_way_true;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0039.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0039.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0039.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0039.json) | [source trace](../../source_traces/llms_emp_feedback_final_0039.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | AutonomousMode | source-ref:llms_emp_feedback_final_0039.puml:line:4\|state AutonomousMode { | element-ref:source:state:AutonomousMode@line:15\|state AutonomousMode named "AutonomousMode" { | source:state:AutonomousMode | - | Case 0039 binds source:state:AutonomousMode to the exact authored occurrence 'state AutonomousMode {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | high_way=true | source-ref:llms_emp_feedback_final_0039.puml:line:7\|InitialState --> HighwayMode : high_way=true | element-ref:compiler:transition_segment:tr_0003:segment:1@line:48\|InitialState -> HighwayMode : /high_way_true; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0039 binds source:transition:tr_0003 to the exact authored occurrence 'InitialState --> HighwayMode : high_way=true'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0009` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0039.puml:line:16\|lane_change --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009@line:20\|state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change";, element-ref:compiler:transition_segment:tr_0009:segment:1@line:26\|lane_change -> FinalWaittr_0009 : /dist_to_exit_2; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009, compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009 | Case 0039 risk final_boundary occurrence review:final_boundary:0001:tr_0009: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:final_boundary:0002:tr_0010` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0039.puml:line:18\|cruise --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010@line:21\|state FinalWaittr_0010 named "Completed final boundary: AutonomousMode.HighwayMode.cruise";, element-ref:compiler:transition_segment:tr_0010:segment:1@line:27\|cruise -> FinalWaittr_0010 : /dist_to_exit_2; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010, compiler:transition_segment:tr_0010:segment:1, source:transition:tr_0010 | Case 0039 risk final_boundary occurrence review:final_boundary:0002:tr_0010: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:synthetic_state:0003:001-FinalWaittr_0009` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:16\|lane_change --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009@line:20\|state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change"; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009, source:transition:tr_0009 | Case 0039 risk synthetic_state occurrence review:synthetic_state:0003:001-FinalWaittr_0009: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0004:002-FinalWaittr_0010` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:18\|cruise --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010@line:21\|state FinalWaittr_0010 named "Completed final boundary: AutonomousMode.HighwayMode.cruise"; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010, source:transition:tr_0010 | Case 0039 risk synthetic_state occurrence review:synthetic_state:0004:002-FinalWaittr_0010: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:explicit_concurrency:0005:001-multiple_initial_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:2\|[*] --> AutonomousMode, source-ref:llms_emp_feedback_final_0039.puml:line:44\|[*] --> collision_avoidance_deactive | element-ref:compiler:transition_segment:tr_0001:segment:1@line:57\|[*] -> AutonomousMode;, element-ref:compiler:transition_segment:tr_0024:segment:1@line:58\|[*] -> collision_avoidance_deactive; | source:transition:tr_0001, source:transition:tr_0024 | Case 0039 risk explicit_concurrency occurrence review:explicit_concurrency:0005:001-multiple_initial_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I41` | `true` | `187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391` | - | - |
| `phase_ii_format` | `U41` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z41` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE41` | `true` | `187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`15` / `15`
- aligned transition endpoints：`26`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.multiple_initial_fanout` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 20 |

## NL

```text
1. The system begins in the AutonomousMode state, which transitions into the InitialState substate, marking the starting point of the autonomous driving mode.
2. From the InitialState, the system can transition to either HighwayMode or UrbanMode based on conditions: `high_way=true` for HighwayMode or `urban_way=true` for UrbanMode.
3. In the HighwayMode state, the system begins in the enter_hwy substate, and can transition to cruise or lane_change based on the distance to the front vehicle (`dist_to_front<25`) and the availability of an extra lane (`extra_lane=true`).
4. If the system is in lane_change, it can return to cruise once the lane change is completed or exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`).
5. In the cruise substate, if the distance to the front vehicle becomes less than 25 meters (`dist_to_front<25`) and there is an extra lane available, the system transitions to lane_change. The system can also exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`).
6. The HighwayMode ends when the system transitions to FinishState, triggered by the `auto_finished=true` condition.
7. In UrbanMode, the system begins in the enter_urban substate. From here, it can transition to lane_change_urban if the distance to the front vehicle is less than 15 meters (`dist_to_front<15`) and an extra lane is available, or straight if the road ahead is clear, or intersection if it detects an intersection (`intersection=true`).
8. In the lane_change_urban substate, the system transitions to straight if the lane change is complete or to exit_urban if the distance to the urban exit is less than 0.7 kilometers (`dist_to_exit<0.7`).
9. In the straight substate, if the system detects an intersection, it transitions to the intersection substate. If the distance to the front vehicle becomes less than 15 meters (`dist_to_front<15`) and an extra lane is available, it transitions to lane_change_urban.
10. The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied.
11. The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively, facilitating seamless mode shifts during the drive.
12. The collision avoidance system is initially in the collision_avoidance_deactive state. It transitions to collision_avoidance_active when certain conditions are met, such as detecting pedestrians (`pedestrian_detected`), the rear distance being less than 5 meters with a velocity over 30 km/h (`dist_to_rear<5 & vel>30`), or the front distance being less than 15 meters in highway mode or 10 meters in urban mode.
13. Once in the collision_avoidance_active state, the collision avoidance system returns to the collision_avoidance_deactive state when there is no active danger, as indicated by the conditions `front_inactive`, `rear_inactive`, and `pedestrian_inactive`.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
[*] --> AutonomousMode

state AutonomousMode {
[*] --> InitialState

InitialState --> HighwayMode : high_way=true
InitialState --> UrbanMode : urban_way=true

state HighwayMode {
[*] --> enter_hwy

enter_hwy --> cruise
cruise --> lane_change : dist_to_front<25 && extra_lane=true
lane_change --> cruise : lane change completed
lane_change --> [*] : dist_to_exit<2

cruise --> [*] : dist_to_exit<2
cruise --> lane_change : dist_to_front<25 && extra_lane=true
}

HighwayMode --> FinishState : auto_finished=true

state UrbanMode {
[*] --> enter_urban

enter_urban --> lane_change_urban : dist_to_front<15 && extra_lane=true
enter_urban --> straight : road ahead is clear
enter_urban --> intersection : intersection=true

lane_change_urban --> straight : lane change complete
lane_change_urban --> exit_urban : dist_to_exit<0.7

straight --> intersection : intersection=true
straight --> lane_change_urban : dist_to_front<15 && extra_lane=true
}

UrbanMode --> FinishState : auto_finished=true
}

AutonomousMode --> HighwayMode : high_way=true
AutonomousMode --> UrbanMode : urban_way=true

[*] --> collision_avoidance_deactive

collision_avoidance_deactive --> collision_avoidance_active : pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 in HighwayMode || dist_to_front<10 in UrbanMode)

collision_avoidance_active --> collision_avoidance_deactive : front_inactive && rear_inactive && pedestrian_inactive

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0039 named "llms_emp_feedback_final_0039" {
    event high_way_true named "high_way=true";
    event urban_way_true named "urban_way=true";
    event dist_to_front_25_extra_lane_true named "dist_to_front<25 && extra_lane=true";
    event lane_change_completed named "lane change completed";
    event dist_to_exit_2 named "dist_to_exit<2";
    event auto_finished_true named "auto_finished=true";
    event dist_to_front_15_extra_lane_true named "dist_to_front<15 && extra_lane=true";
    event road_ahead_is_clear named "road ahead is clear";
    event intersection_true named "intersection=true";
    event lane_change_complete named "lane change complete";
    event dist_to_exit_0_7 named "dist_to_exit<0.7";
    event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode named "pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 in HighwayMode || dist_to_front<10 in UrbanMode)";
    event front_inactive_rear_inactive_pedestrian_inactive named "front_inactive && rear_inactive && pedestrian_inactive";
    state AutonomousMode named "AutonomousMode" {
        state HighwayMode named "HighwayMode" {
            state enter_hwy named "enter_hwy";
            state cruise named "cruise";
            state lane_change named "lane_change";
            state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change";
            state FinalWaittr_0010 named "Completed final boundary: AutonomousMode.HighwayMode.cruise";
            [*] -> enter_hwy;
            enter_hwy -> cruise;
            cruise -> lane_change : /dist_to_front_25_extra_lane_true;
            lane_change -> cruise : /lane_change_completed;
            lane_change -> FinalWaittr_0009 : /dist_to_exit_2;
            cruise -> FinalWaittr_0010 : /dist_to_exit_2;
            cruise -> lane_change : /dist_to_front_25_extra_lane_true;
        }
        state UrbanMode named "UrbanMode" {
            state enter_urban named "enter_urban";
            state lane_change_urban named "lane_change_urban";
            state straight named "straight";
            state intersection named "intersection";
            state exit_urban named "exit_urban";
            [*] -> enter_urban;
            enter_urban -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            enter_urban -> straight : /road_ahead_is_clear;
            enter_urban -> intersection : /intersection_true;
            lane_change_urban -> straight : /lane_change_complete;
            lane_change_urban -> exit_urban : /dist_to_exit_0_7;
            straight -> intersection : /intersection_true;
            straight -> lane_change_urban : /dist_to_front_15_extra_lane_true;
        }
        state InitialState named "InitialState";
        state FinishState named "FinishState";
        [*] -> InitialState;
        InitialState -> HighwayMode : /high_way_true;
        InitialState -> UrbanMode : /urban_way_true;
        !HighwayMode -> FinishState : /auto_finished_true;
        !UrbanMode -> FinishState : /auto_finished_true;
        ! * -> HighwayMode : /high_way_true;
        ! * -> UrbanMode : /urban_way_true;
    }
    state collision_avoidance_deactive named "collision_avoidance_deactive";
    state collision_avoidance_active named "collision_avoidance_active";
    [*] -> AutonomousMode;
    [*] -> collision_avoidance_deactive;
    collision_avoidance_deactive -> collision_avoidance_active : /pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode;
    collision_avoidance_active -> collision_avoidance_deactive : /front_inactive_rear_inactive_pedestrian_inactive;
}
```

[上一组 `0038`](../0038/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0040`](../0040/README.md)
