# Pair `0027`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0026`](../0026/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0028`](../0028/README.md)

- LLM：`Llama`
- 模型/场景：Collision avoidance sub-machine state diagram
- NL SHA-256：`49854d044ad99f16a710021500f5e972da93b27635a41144d9b91d32444c0f63`
- PlantUML SHA-256：`9a0ab14a1252a2c11fb409f770f670f465e72b8fc542f5bb5e2019e476a778c6`
- FCSTM SHA-256：`d3b6b58b433f45f86dc36f2650bd5d31a2b96d25d29ec359191a35d6baffdc28`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：三条 ActiveState initial 全保留且顺序未变；multiple-initial debt 阻止宣称运行等价。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0027.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0027.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0027.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. There are three region in this diagram
2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.
3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm CollisionAvoidance
[*] --> DetectingState
DetectingState: Detecting Collision
DetectingState --> ActiveState : Frontend Collision or Rear-end Collision or Collision with Pedestrian detected
state ActiveState {
[*] --> BrakeControlState
[*] --> SteeringControlState
[*] --> SensorControlState
BrakeControlState --> InitialState : Signal Feedback Sent
SteeringControlState --> InitialState : Signal Feedback Sent
SensorControlState --> InitialState : Signal Feedback Sent
}
InitialState --> DetectingState : No Collision detected
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0027 named "CollisionAvoidance" {
    event Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected named "Frontend Collision or Rear-end Collision or Collision with Pedestrian detected";
    event Signal_Feedback_Sent named "Signal Feedback Sent";
    event No_Collision_detected named "No Collision detected";
    state ActiveState named "ActiveState" {
        state BrakeControlState named "BrakeControlState";
        state SteeringControlState named "SteeringControlState";
        state SensorControlState named "SensorControlState";
        state InitialState named "InitialState";
        [*] -> BrakeControlState;
        [*] -> SteeringControlState;
        [*] -> SensorControlState;
        BrakeControlState -> InitialState : /Signal_Feedback_Sent;
        SteeringControlState -> InitialState : /Signal_Feedback_Sent;
        SensorControlState -> InitialState : /Signal_Feedback_Sent;
    }
    state DetectingState named "DetectingState\n[PlantUML body] Detecting Collision";
    state InitialState named "InitialState";
    [*] -> DetectingState;
    DetectingState -> ActiveState : /Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected;
    InitialState -> DetectingState : /No_Collision_detected;
}
```

[上一组 `0026`](../0026/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0028`](../0028/README.md)
