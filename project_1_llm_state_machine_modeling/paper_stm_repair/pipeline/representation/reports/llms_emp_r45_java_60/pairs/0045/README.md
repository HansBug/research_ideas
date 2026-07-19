# Pair `0045`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0044`](../0044/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0046`](../0046/README.md)

- LLM：`DeepSeek`
- 模型/场景：Microwave Oven Control with entry and <br> exit actions
- NL SHA-256：`934e19bd4ae2a793c334fdcf486092d3aa20858f09ae892753ef87698feb061f`
- PlantUML SHA-256：`bfe9731bf60d0dc17fd31b89dec3826f9c29be2eeebb752b48b5a1289440425e`
- FCSTM SHA-256：`91705ba9f200e1a55d78ae36bf9fcb5ee886536c012c5151e775b28ad9187ce7`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：各 composite 内同名 `DoorOpenWithItem` 按 lexical scope 独立；20 条跨层/内部 edge 齐。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0045.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0045.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0045.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm MicrowaveStateMachine [Microwave State Machine]

[*] --> DoorShut

state DoorShut {
[*] --> DoorShutIdle
DoorShutIdle --> DoorShutIdle : Cancel
DoorShutIdle --> DoorOpen : Door Opened
}

state DoorOpen {
[*] --> DoorOpenIdle
DoorOpenIdle --> DoorOpenWithItem : Item Placed
DoorOpenWithItem --> DoorOpenIdle : Item Removed
DoorOpenWithItem --> DoorShutWithItem : Door Closed [zero time set]
DoorOpenWithItem --> ReadytoCook : Cooking Time Entered
}

state DoorShutWithItem {
[*] --> DoorShutWithItemIdle
DoorShutWithItemIdle --> DoorOpenWithItem : Door Opened
DoorShutWithItemIdle --> ReadytoCook : Cooking Time Entered
}

state ReadytoCook {
[*] --> ReadytoCookIdle
ReadytoCookIdle --> DoorShutWithItem : Cancel
ReadytoCookIdle --> DoorOpenWithItem : Door Opened
ReadytoCookIdle --> Cooking : Start
}

state Cooking {
[*] --> CookingIdle
CookingIdle --> DoorOpenWithItem : Door Opened
CookingIdle --> DoorShutWithItem : Timer Expired
CookingIdle --> ReadytoCook : Cancel
}

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0045 named "MicrowaveStateMachine [Microwave State Machine]" {
    event Cancel named "Cancel";
    event Door_Opened named "Door Opened";
    event Item_Placed named "Item Placed";
    event Item_Removed named "Item Removed";
    event Door_Closed_zero_time_set named "Door Closed [zero time set]";
    event Cooking_Time_Entered named "Cooking Time Entered";
    event Start named "Start";
    event Timer_Expired named "Timer Expired";
    state DoorShut named "DoorShut" {
        state DoorShutIdle named "DoorShutIdle";
        [*] -> DoorShutIdle;
        DoorShutIdle -> DoorShutIdle : /Cancel;
        DoorShutIdle -> [*] : /Door_Opened;
    }
    state DoorOpen named "DoorOpen" {
        state DoorOpenIdle named "DoorOpenIdle";
        state DoorOpenWithItem named "DoorOpenWithItem";
        [*] -> DoorOpenIdle;
        DoorOpenIdle -> DoorOpenWithItem : /Item_Placed;
        DoorOpenWithItem -> DoorOpenIdle : /Item_Removed;
        DoorOpenWithItem -> [*] : /Door_Closed_zero_time_set;
        DoorOpenWithItem -> [*] : /Cooking_Time_Entered;
    }
    state DoorShutWithItem named "DoorShutWithItem" {
        state DoorShutWithItemIdle named "DoorShutWithItemIdle";
        state DoorOpenWithItem named "DoorOpenWithItem";
        [*] -> DoorShutWithItemIdle;
        DoorShutWithItemIdle -> DoorOpenWithItem : /Door_Opened;
        DoorShutWithItemIdle -> [*] : /Cooking_Time_Entered;
    }
    state ReadytoCook named "ReadytoCook" {
        state ReadytoCookIdle named "ReadytoCookIdle";
        state DoorOpenWithItem named "DoorOpenWithItem";
        [*] -> ReadytoCookIdle;
        ReadytoCookIdle -> [*] : /Cancel;
        ReadytoCookIdle -> DoorOpenWithItem : /Door_Opened;
        ReadytoCookIdle -> [*] : /Start;
    }
    state Cooking named "Cooking" {
        state CookingIdle named "CookingIdle";
        state DoorOpenWithItem named "DoorOpenWithItem";
        [*] -> CookingIdle;
        CookingIdle -> DoorOpenWithItem : /Door_Opened;
        CookingIdle -> [*] : /Timer_Expired;
        CookingIdle -> [*] : /Cancel;
    }
    [*] -> DoorShut;
    DoorShut -> DoorOpen : /Door_Opened;
    DoorOpen -> DoorShutWithItem : /Door_Closed_zero_time_set;
    DoorOpen -> ReadytoCook : /Cooking_Time_Entered;
    DoorShutWithItem -> ReadytoCook : /Cooking_Time_Entered;
    ReadytoCook -> DoorShutWithItem : /Cancel;
    ReadytoCook -> Cooking : /Start;
    Cooking -> DoorShutWithItem : /Timer_Expired;
    Cooking -> ReadytoCook : /Cancel;
}
```

[上一组 `0044`](../0044/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0046`](../0046/README.md)
