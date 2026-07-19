# Pair `0055`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0054`](../0054/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0056`](../0056/README.md)

- LLM：`Claude`
- 模型/场景：Microwave Oven Control with entry and <br> exit actions
- NL SHA-256：`934e19bd4ae2a793c334fdcf486092d3aa20858f09ae892753ef87698feb061f`
- PlantUML SHA-256：`322a51f31a2fe5f946fa71caf2f1e44a4d2c7ffe089b2ca987de2ae7d009abe6`
- FCSTM SHA-256：`750004071ba8ecb96a3d6e1d090214979e072afc8e96d88f9bf53139418945e6`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Microwave 16 edge 逐条一致；`[time = 0]` 保持 opaque。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0055.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0055.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0055.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. The microwave starts in the DoorShut state. From this state, the system can either remain in DoorShut if a Cancel action is performed or transition to the DoorOpen state when the door is opened.
2. When the Door Opened action occurs in the DoorShut state, the system transitions to the DoorOpen state. The door can be closed to return to the DoorShut state.
3. In the DoorOpen state, placing an item inside the microwave transitions the system to DoorOpenWithItem. If the item is removed, the system returns to DoorOpen.
4. From DoorOpenWithItem, the system can transition to DoorShutWithItem if the door is closed with zero time set or to ReadytoCook if cooking time is entered.
5. In the DoorShutWithItem state, opening the door transitions the system back to DoorOpenWithItem, while entering cooking time takes the system to ReadytoCook, where the cooking time is displayed and updated.
6. In the ReadytoCook state, if the Cancel action is performed, the system returns to DoorShutWithItem, canceling or updating the cooking time. If the door is opened, the system transitions to DoorOpenWithItem.
7. When the Start action is performed in ReadytoCook, the system transitions to the Cooking state, where the timer starts.
8. In the Cooking state, opening the door stops the timer and the system transitions to DoorOpenWithItem, while if the timer expires, the system moves to DoorShutWithItem. A Cancel action transitions the system back to ReadytoCook.
```

## 原装 PlantUML STM0

```plantuml
@startuml

[*] --> DoorShut

DoorShut --> DoorShut : Cancel
DoorShut --> DoorOpen : Door Opened

DoorOpen --> DoorShut : Door Closed
DoorOpen --> DoorOpenWithItem : Place Item

DoorOpenWithItem --> DoorOpen : Remove Item
DoorOpenWithItem --> DoorShutWithItem : Door Closed [time = 0]
DoorOpenWithItem --> ReadytoCook : Enter Cooking Time

DoorShutWithItem --> DoorOpenWithItem : Door Opened
DoorShutWithItem --> ReadytoCook : Enter Cooking Time

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
state llms_emp_stm_results_0055 named "llms_emp_stm_results_0055" {
    event Cancel named "Cancel";
    event Door_Opened named "Door Opened";
    event Door_Closed named "Door Closed";
    event Place_Item named "Place Item";
    event Remove_Item named "Remove Item";
    event Door_Closed_time_0 named "Door Closed [time = 0]";
    event Enter_Cooking_Time named "Enter Cooking Time";
    event Start named "Start";
    event Timer_Expired named "Timer Expired";
    state DoorShut named "DoorShut";
    state DoorOpen named "DoorOpen";
    state DoorOpenWithItem named "DoorOpenWithItem";
    state DoorShutWithItem named "DoorShutWithItem";
    state ReadytoCook named "ReadytoCook";
    state Cooking named "Cooking";
    [*] -> DoorShut;
    DoorShut -> DoorShut : /Cancel;
    DoorShut -> DoorOpen : /Door_Opened;
    DoorOpen -> DoorShut : /Door_Closed;
    DoorOpen -> DoorOpenWithItem : /Place_Item;
    DoorOpenWithItem -> DoorOpen : /Remove_Item;
    DoorOpenWithItem -> DoorShutWithItem : /Door_Closed_time_0;
    DoorOpenWithItem -> ReadytoCook : /Enter_Cooking_Time;
    DoorShutWithItem -> DoorOpenWithItem : /Door_Opened;
    DoorShutWithItem -> ReadytoCook : /Enter_Cooking_Time;
    ReadytoCook -> DoorShutWithItem : /Cancel;
    ReadytoCook -> DoorOpenWithItem : /Door_Opened;
    ReadytoCook -> Cooking : /Start;
    Cooking -> DoorOpenWithItem : /Door_Opened;
    Cooking -> DoorShutWithItem : /Timer_Expired;
    Cooking -> ReadytoCook : /Cancel;
}
```

[上一组 `0054`](../0054/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0056`](../0056/README.md)
