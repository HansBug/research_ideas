# Pair `0035`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0034`](../0034/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0036`](../0036/README.md)

- LLM：`Kimi`
- 模型/场景：Microwave Oven Control with entry and <br> exit actions
- NL SHA-256：`934e19bd4ae2a793c334fdcf486092d3aa20858f09ae892753ef87698feb061f`
- PlantUML SHA-256：`84d17e092a8e8b903382f3a07c115bb1511466a24ce5d36dee4c24d90b990a76`
- FCSTM SHA-256：`93c79f69bad2f07cc28aa18d85a2713fef4c586024be480b9154928af2c19de8`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Microwave 16 edge 与六个 body 逐条一致。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0035.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0035.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0035.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm MicrowaveStateMachine
[*] --> DoorShut

DoorShut : DoorShut
DoorShut --> DoorShut : Cancel
DoorShut --> DoorOpen : Door Opened

DoorOpen : DoorOpen
DoorOpen --> DoorShut : Door Closed
DoorOpen --> DoorOpenWithItem : Item Placed

DoorOpenWithItem : DoorOpenWithItem
DoorOpenWithItem --> DoorOpen : Item Removed
DoorOpenWithItem --> DoorShutWithItem : Door Closed
DoorOpenWithItem --> ReadytoCook : Cooking Time Entered

DoorShutWithItem : DoorShutWithItem
DoorShutWithItem --> DoorOpenWithItem : Door Opened
DoorShutWithItem --> ReadytoCook : Cooking Time Entered

ReadytoCook : ReadytoCook
ReadytoCook --> DoorShutWithItem : Cancel
ReadytoCook --> DoorOpenWithItem : Door Opened
ReadytoCook --> Cooking : Start

Cooking : Cooking
Cooking --> DoorOpenWithItem : Door Opened
Cooking --> DoorShutWithItem : Timer Expired
Cooking --> ReadytoCook : Cancel

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0035 named "MicrowaveStateMachine" {
    event Cancel named "Cancel";
    event Door_Opened named "Door Opened";
    event Door_Closed named "Door Closed";
    event Item_Placed named "Item Placed";
    event Item_Removed named "Item Removed";
    event Cooking_Time_Entered named "Cooking Time Entered";
    event Start named "Start";
    event Timer_Expired named "Timer Expired";
    state DoorShut named "DoorShut\n[PlantUML body] DoorShut";
    state DoorOpen named "DoorOpen\n[PlantUML body] DoorOpen";
    state DoorOpenWithItem named "DoorOpenWithItem\n[PlantUML body] DoorOpenWithItem";
    state DoorShutWithItem named "DoorShutWithItem\n[PlantUML body] DoorShutWithItem";
    state ReadytoCook named "ReadytoCook\n[PlantUML body] ReadytoCook";
    state Cooking named "Cooking\n[PlantUML body] Cooking";
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

[上一组 `0034`](../0034/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0036`](../0036/README.md)
