# Pair `0029`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0028`](../0028/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0030`](../0030/README.md)

- LLM：`Llama`
- 模型/场景：autonomous mode
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE31`；Excel row：`31`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`0e203bbdf499156e24ca9a904b56de5c0c2fe2564291b451cadb185885975fdd`
- NL SHA-256：`b7425c44960b36c3534f118279e347786d4074191efea7bf9a7c5ba032c9e82c`
- PlantUML SHA-256：`2edfafb6df737f010d3b53ca3bffca7bd52cd3ea9bd00629283443edd094f4ea`
- FCSTM SHA-256：`78376582a2c53dc3ef5042e180083fb450826cfc2be5f02ecdb7a2c1ba6845ad`
- review subject SHA-256：`05bd2d27f0c11f09cd285b54011d6ae59f1f1b716cb6fbe55622f3dcf351026b`
- working contract SHA-256：`b0c10e15f1a3af9e28961698c6996406d9d6b6e9b0fe8cd0d4fa4d79875da2be`
- 结构裁决：`structure_preserved`
- source states / transitions：`17` / `27`
- mapped / blocked / silent drop：`27` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `3/3`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`17` / `27`
- official identity remaps：state `1` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`47` / `48` / `0`
- source macro / positive identity trace / conversion boundary trace：`30` / `47` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0029 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0029.puml:line:10\|state HighwayMode {, source-ref:llms_emp_feedback_final_0029.puml:line:4\|AutonomousMode --> InitialState : initial`；FCSTM anchors：`element-ref:source:state:HighwayMode@line:16\|state HighwayMode named "HighwayMode" {, element-ref:compiler:transition_segment:tr_0002:segment:1@line:62\|AutonomousMode -> InitialState : /initial;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0029.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0029.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0029.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0029.json) | [source trace](../../source_traces/llms_emp_feedback_final_0029.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | HighwayMode | source-ref:llms_emp_feedback_final_0029.puml:line:10\|state HighwayMode { | element-ref:source:state:HighwayMode@line:16\|state HighwayMode named "HighwayMode" { | source:state:HighwayMode | - | Case 0029 binds source:state:HighwayMode to the exact authored occurrence 'state HighwayMode {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | AutonomousMode | source-ref:llms_emp_feedback_final_0029.puml:line:4\|AutonomousMode --> InitialState : initial | element-ref:compiler:transition_segment:tr_0002:segment:1@line:62\|AutonomousMode -> InitialState : /initial; | source:transition:tr_0002 | compiler:transition_segment:tr_0002:segment:1 | Case 0029 binds source:transition:tr_0002 to the exact authored occurrence 'AutonomousMode --> InitialState : initial'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:official_identity_remap:0001:state-001` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0029.puml:line:41\|FinishState: Finish State | element-ref:source:state:HighwayMode.FinishState@line:21\|state FinishState named "FinishState\n[PlantUML body] Finish State"; | source:state:HighwayMode.FinishState | Case 0029 risk official_identity_remap occurrence review:official_identity_remap:0001:state-001: The occurrence follows the pinned PlantUML qualified Entity/Link identity result, including the recorded remap, instead of substituting a lexical guess. |
| `review:multi_segment_macro:0002:tr_0025` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0029.puml:line:40\|AutonomousMode --> FinishState : auto_finished=true | element-ref:compiler:transition_segment:tr_0025:segment:1@line:67\|AutonomousMode -> HighwayMode : /auto_finished_true;, element-ref:compiler:transition_segment:tr_0025:segment:2@line:23\|[*] -> FinishState : /auto_finished_true; | compiler:transition_segment:tr_0025:segment:1, compiler:transition_segment:tr_0025:segment:2, source:transition:tr_0025 | Case 0029 risk multi_segment_macro occurrence review:multi_segment_macro:0002:tr_0025: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0003:tr_0026` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0029.puml:line:43\|UrbanMode --> FinishState : auto_finished=true | element-ref:compiler:transition_segment:tr_0026:segment:1@line:68\|!UrbanMode -> HighwayMode : /auto_finished_true;, element-ref:compiler:transition_segment:tr_0026:segment:2@line:24\|[*] -> FinishState : /auto_finished_true; | compiler:transition_segment:tr_0026:segment:1, compiler:transition_segment:tr_0026:segment:2, source:transition:tr_0026 | Case 0029 risk multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0026: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:synthetic_state:0004:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0029.puml:line:10\|state HighwayMode { | element-ref:compiler:state:llms_emp_feedback_final_0029.HighwayMode.UnspecifiedInitial@line:17\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:HighwayMode@line:16\|state HighwayMode named "HighwayMode" { | compiler:state:llms_emp_feedback_final_0029.HighwayMode.UnspecifiedInitial, source:state:HighwayMode | Case 0029 risk synthetic_state occurrence review:synthetic_state:0004:001-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0005:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0029.puml:line:20\|state UrbanMode { | element-ref:compiler:state:llms_emp_feedback_final_0029.UrbanMode.UnspecifiedInitial@line:36\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:UrbanMode@line:35\|state UrbanMode named "UrbanMode" { | compiler:state:llms_emp_feedback_final_0029.UrbanMode.UnspecifiedInitial, source:state:UrbanMode | Case 0029 risk synthetic_state occurrence review:synthetic_state:0005:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I31` | `true` | `0e203bbdf499156e24ca9a904b56de5c0c2fe2564291b451cadb185885975fdd` | - | - |
| `phase_ii_format` | `U31` | `true` | `2edfafb6df737f010d3b53ca3bffca7bd52cd3ea9bd00629283443edd094f4ea` | syntax error: stm AutonomousDriving | YES |
| `phase_ii_grammar` | `Z31` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE31` | `true` | `2edfafb6df737f010d3b53ca3bffca7bd52cd3ea9bd00629283443edd094f4ea` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`17` / `17`
- aligned transition endpoints：`27`

| source-parser identity | pinned PlantUML identity | raw ref | reason |
|---|---|---|---|
| `FinishState` | `HighwayMode.FinishState` | `llms_emp_feedback_final_0029.puml:line:41` | `unique_official_entity_identity` |

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.missing_explicit_initial` | 2 |
| `R45.DEBT.opaque_state_body_semantics` | 3 |
| `R45.DEBT.opaque_transition_label_semantics` | 25 |

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
AutonomousMode: Autonomous Mode
AutonomousMode --> InitialState : initial
InitialState: Initial State

InitialState --> HighwayMode : high_way=true
InitialState --> UrbanMode : urban_way=true

state HighwayMode {
HighwayMode --> enter_hwy : enter
enter_hwy --> cruise : dist_to_front<25 & extra_lane=true
enter_hwy --> lane_change : dist_to_front<25 & extra_lane=true
cruise --> lane_change : dist_to_front<25 & extra_lane=true
cruise --> FinishState : dist_to_exit<2
lane_change --> cruise : lane_change_completed
lane_change --> exit_hwy : dist_to_exit<2
}

state UrbanMode {
UrbanMode --> enter_urban : enter
enter_urban --> lane_change_urban : dist_to_front<15 & extra_lane=true
enter_urban --> straight : road_clear
enter_urban --> intersection : intersection=true
lane_change_urban --> straight : lane_change_completed
lane_change_urban --> exit_urban : dist_to_exit<0.7
straight --> intersection : intersection=true
straight --> lane_change_urban : dist_to_front<15 & extra_lane=true
}

state CollisionAvoidance {
[*] --> collision_avoidance_deactive
collision_avoidance_deactive --> collision_avoidance_active : pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode
collision_avoidance_active --> collision_avoidance_deactive : front_inactive & rear_inactive & pedestrian_inactive
}

HighwayMode --> UrbanMode : urban_way=true
UrbanMode --> HighwayMode : high_way=true

AutonomousMode --> FinishState : auto_finished=true
FinishState: Finish State

UrbanMode --> FinishState : auto_finished=true
HighwayMode --> FinishState : auto_finished=true
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0029 named "llms_emp_feedback_final_0029" {
    event initial named "initial";
    event high_way_true named "high_way=true";
    event urban_way_true named "urban_way=true";
    event enter_ named "enter";
    event dist_to_front_25_extra_lane_true named "dist_to_front<25 & extra_lane=true";
    event dist_to_exit_2 named "dist_to_exit<2";
    event lane_change_completed named "lane_change_completed";
    event dist_to_front_15_extra_lane_true named "dist_to_front<15 & extra_lane=true";
    event road_clear named "road_clear";
    event intersection_true named "intersection=true";
    event dist_to_exit_0_7 named "dist_to_exit<0.7";
    event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_highway_mode_dist_to_front_10_urban_mode named "pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode";
    event front_inactive_rear_inactive_pedestrian_inactive named "front_inactive & rear_inactive & pedestrian_inactive";
    event auto_finished_true named "auto_finished=true";
    state HighwayMode named "HighwayMode" {
        state UnspecifiedInitial named "Unspecified initial";
        state enter_hwy named "enter_hwy";
        state cruise named "cruise";
        state lane_change named "lane_change";
        state FinishState named "FinishState\n[PlantUML body] Finish State";
        state exit_hwy named "exit_hwy";
        [*] -> FinishState : /auto_finished_true;
        [*] -> FinishState : /auto_finished_true;
        ! * -> enter_hwy : /enter_;
        enter_hwy -> cruise : /dist_to_front_25_extra_lane_true;
        enter_hwy -> lane_change : /dist_to_front_25_extra_lane_true;
        cruise -> lane_change : /dist_to_front_25_extra_lane_true;
        cruise -> FinishState : /dist_to_exit_2;
        lane_change -> cruise : /lane_change_completed;
        lane_change -> exit_hwy : /dist_to_exit_2;
        ! * -> FinishState : /auto_finished_true;
        [*] -> UnspecifiedInitial;
    }
    state UrbanMode named "UrbanMode" {
        state UnspecifiedInitial named "Unspecified initial";
        state enter_urban named "enter_urban";
        state lane_change_urban named "lane_change_urban";
        state straight named "straight";
        state intersection named "intersection";
        state exit_urban named "exit_urban";
        ! * -> enter_urban : /enter_;
        enter_urban -> lane_change_urban : /dist_to_front_15_extra_lane_true;
        enter_urban -> straight : /road_clear;
        enter_urban -> intersection : /intersection_true;
        lane_change_urban -> straight : /lane_change_completed;
        lane_change_urban -> exit_urban : /dist_to_exit_0_7;
        straight -> intersection : /intersection_true;
        straight -> lane_change_urban : /dist_to_front_15_extra_lane_true;
        [*] -> UnspecifiedInitial;
    }
    state CollisionAvoidance named "CollisionAvoidance" {
        state collision_avoidance_deactive named "collision_avoidance_deactive";
        state collision_avoidance_active named "collision_avoidance_active";
        [*] -> collision_avoidance_deactive;
        collision_avoidance_deactive -> collision_avoidance_active : /pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_highway_mode_dist_to_front_10_urban_mode;
        collision_avoidance_active -> collision_avoidance_deactive : /front_inactive_rear_inactive_pedestrian_inactive;
    }
    state AutonomousMode named "AutonomousMode\n[PlantUML body] Autonomous Mode";
    state InitialState named "InitialState\n[PlantUML body] Initial State";
    [*] -> AutonomousMode;
    AutonomousMode -> InitialState : /initial;
    InitialState -> HighwayMode : /high_way_true;
    InitialState -> UrbanMode : /urban_way_true;
    !HighwayMode -> UrbanMode : /urban_way_true;
    !UrbanMode -> HighwayMode : /high_way_true;
    AutonomousMode -> HighwayMode : /auto_finished_true;
    !UrbanMode -> HighwayMode : /auto_finished_true;
}
```

[上一组 `0028`](../0028/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0030`](../0030/README.md)
