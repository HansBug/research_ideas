# Pair `0049`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0048`](../0048/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0050`](../0050/README.md)

- LLM：`DeepSeek`
- 模型/场景：autonomous mode
- NL SHA-256：`b7425c44960b36c3534f118279e347786d4074191efea7bf9a7c5ba032c9e82c`
- PlantUML SHA-256：`85f000271f03ab4d83260494bfe73b053111cfaf660a9f3d79c7ea912063ded6`
- FCSTM SHA-256：`a8b75ab36f78ccc2f9597bf74f25bb495abd9c29ade977670c2bba78a6833776`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Highway/Urban/root 三个 `FinishState` 不合并；29 edge 与 CollisionAvoidance hierarchy 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0049.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0049.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0049.json) | [人工总账](../../MANUAL_REVIEW.md)

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

## 原装 PlantUML STM0

```plantuml
@startuml
[*] --> AutonomousMode
state AutonomousMode {
[*] --> InitialState
InitialState --> HighwayMode : high_way=true
InitialState --> UrbanMode : urban_way=true

state HighwayMode {
[*] --> enter_hwy
enter_hwy --> cruise : dist_to_front>=25
enter_hwy --> lane_change : dist_to_front<25 && extra_lane=true
lane_change --> cruise : lane_change_complete
lane_change --> FinishState : dist_to_exit<2
cruise --> lane_change : dist_to_front<25 && extra_lane=true
cruise --> FinishState : dist_to_exit<2
cruise --> FinishState : auto_finished=true
}

state UrbanMode {
[*] --> enter_urban
enter_urban --> lane_change_urban : dist_to_front<15 && extra_lane=true
enter_urban --> straight : road_clear
enter_urban --> intersection : intersection=true
lane_change_urban --> straight : lane_change_complete
lane_change_urban --> exit_urban : dist_to_exit<0.7
straight --> intersection : intersection=true
straight --> lane_change_urban : dist_to_front<15 && extra_lane=true
straight --> FinishState : auto_finished=true
intersection --> straight : road_clear
intersection --> FinishState : auto_finished=true
}

HighwayMode --> UrbanMode : urban_way=true
UrbanMode --> HighwayMode : high_way=true
}

state CollisionAvoidance {
[*] --> collision_avoidance_deactive
collision_avoidance_deactive --> collision_avoidance_active : pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 && in(HighwayMode)) || (dist_to_front<10 && in(UrbanMode))
collision_avoidance_active --> collision_avoidance_deactive : front_inactive && rear_inactive && pedestrian_inactive
}

AutonomousMode --> FinishState : auto_finished=true
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0049 named "llms_emp_stm_results_0049" {
    event high_way_true named "high_way=true";
    event urban_way_true named "urban_way=true";
    event dist_to_front_25 named "dist_to_front>=25";
    event dist_to_front_25_extra_lane_true named "dist_to_front<25 && extra_lane=true";
    event lane_change_complete named "lane_change_complete";
    event dist_to_exit_2 named "dist_to_exit<2";
    event auto_finished_true named "auto_finished=true";
    event dist_to_front_15_extra_lane_true named "dist_to_front<15 && extra_lane=true";
    event road_clear named "road_clear";
    event intersection_true named "intersection=true";
    event dist_to_exit_0_7 named "dist_to_exit<0.7";
    event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode named "pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 && in(HighwayMode)) || (dist_to_front<10 && in(UrbanMode))";
    event front_inactive_rear_inactive_pedestrian_inactive named "front_inactive && rear_inactive && pedestrian_inactive";
    state AutonomousMode named "AutonomousMode" {
        state HighwayMode named "HighwayMode" {
            state enter_hwy named "enter_hwy";
            state cruise named "cruise";
            state lane_change named "lane_change";
            state FinishState named "FinishState";
            [*] -> enter_hwy;
            enter_hwy -> cruise : /dist_to_front_25;
            enter_hwy -> lane_change : /dist_to_front_25_extra_lane_true;
            lane_change -> cruise : /lane_change_complete;
            lane_change -> FinishState : /dist_to_exit_2;
            cruise -> lane_change : /dist_to_front_25_extra_lane_true;
            cruise -> FinishState : /dist_to_exit_2;
            cruise -> FinishState : /auto_finished_true;
        }
        state UrbanMode named "UrbanMode" {
            state enter_urban named "enter_urban";
            state lane_change_urban named "lane_change_urban";
            state straight named "straight";
            state intersection named "intersection";
            state exit_urban named "exit_urban";
            state FinishState named "FinishState";
            [*] -> enter_urban;
            enter_urban -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            enter_urban -> straight : /road_clear;
            enter_urban -> intersection : /intersection_true;
            lane_change_urban -> straight : /lane_change_complete;
            lane_change_urban -> exit_urban : /dist_to_exit_0_7;
            straight -> intersection : /intersection_true;
            straight -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            straight -> FinishState : /auto_finished_true;
            intersection -> straight : /road_clear;
            intersection -> FinishState : /auto_finished_true;
        }
        state InitialState named "InitialState";
        [*] -> InitialState;
        InitialState -> HighwayMode : /high_way_true;
        InitialState -> UrbanMode : /urban_way_true;
        !HighwayMode -> UrbanMode : /urban_way_true;
        !UrbanMode -> HighwayMode : /high_way_true;
    }
    state CollisionAvoidance named "CollisionAvoidance" {
        state collision_avoidance_deactive named "collision_avoidance_deactive";
        state collision_avoidance_active named "collision_avoidance_active";
        [*] -> collision_avoidance_deactive;
        collision_avoidance_deactive -> collision_avoidance_active : /pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode;
        collision_avoidance_active -> collision_avoidance_deactive : /front_inactive_rear_inactive_pedestrian_inactive;
    }
    state FinishState named "FinishState";
    [*] -> AutonomousMode;
    !AutonomousMode -> FinishState : /auto_finished_true;
}
```

[上一组 `0048`](../0048/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0050`](../0050/README.md)
