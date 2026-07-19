# Pair `0025`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0024`](../0024/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0026`](../0026/README.md)

- LLM：`Llama`
- 模型/场景：Microwave Oven Control with entry and <br> exit actions
- NL SHA-256：`934e19bd4ae2a793c334fdcf486092d3aa20858f09ae892753ef87698feb061f`
- PlantUML SHA-256：`a4422437b46a20b3d0a4e9745b990a2bdc24ffc315d709f3450762fd7b514254`
- FCSTM SHA-256：`700ec6957e95a00d382b9b1eecac59013875789aa2cf08cce941dfb7d9c015e5`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Microwave 六状态与16条平面边逐条一致。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0025.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0025.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0025.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm Microwave
[*] --> DoorShut
DoorShut --> DoorShut: Cancel
DoorShut --> DoorOpen: Door Opened
DoorOpen --> DoorShut: Door Closed
DoorOpen --> DoorOpenWithItem: Item Placed
DoorOpenWithItem --> DoorOpen: Item Removed
DoorOpenWithItem --> DoorShutWithItem: Door Closed
DoorOpenWithItem --> ReadytoCook: Cooking Time Entered
DoorShutWithItem --> DoorOpenWithItem: Door Opened
DoorShutWithItem --> ReadytoCook: Cooking Time Entered
ReadytoCook --> DoorShutWithItem: Cancel
ReadytoCook --> DoorOpenWithItem: Door Opened
ReadytoCook --> Cooking: Start
Cooking --> DoorOpenWithItem: Door Opened
Cooking --> DoorShutWithItem: Timer Expired
Cooking --> ReadytoCook: Cancel
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0025 named "Microwave" {
    event Cancel named "Cancel";
    event Door_Opened named "Door Opened";
    event Door_Closed named "Door Closed";
    event Item_Placed named "Item Placed";
    event Item_Removed named "Item Removed";
    event Cooking_Time_Entered named "Cooking Time Entered";
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

[上一组 `0024`](../0024/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0026`](../0026/README.md)
