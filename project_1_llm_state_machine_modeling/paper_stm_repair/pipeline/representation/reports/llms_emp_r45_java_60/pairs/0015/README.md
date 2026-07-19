# Pair `0015`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0014`](../0014/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0016`](../0016/README.md)

- LLM：`GPT-4`
- 模型/场景：Microwave Oven Control with entry and <br> exit actions
- NL SHA-256：`934e19bd4ae2a793c334fdcf486092d3aa20858f09ae892753ef87698feb061f`
- PlantUML SHA-256：`beba54d00f7620bcc9b14a882183354a7d49a56468c27fda7a0d2fd4c11b1c6b`
- FCSTM SHA-256：`6b03cc6b56e8df69b56cf442783adbc1886be3422ca9f63550ccfcd97173199d`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：六个 scoped `State1` 独立；22 条跨层 macro 齐；`Remove Item` deep entry 优先于默认 initial。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0015.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0015.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0015.json) | [人工总账](../../MANUAL_REVIEW.md)

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

[*] -> DoorShut

state DoorShut {
[*] -> State1
State1 -down-> State2 : Open Door
State1 --> State1 : Cancel
State2 -> DoorOpen: Close Door
}

state DoorOpen {
[*] -> State1
State1 -> DoorOpenWithItem : Place Item
DoorOpenWithItem --> State1 : Remove Item
}

state DoorOpenWithItem {
[*] -> State1
State1 --> DoorShutWithItem : Close Door/Zero Time
State1 --> ReadytoCook : Enter Time
}

state DoorShutWithItem {
[*] -> State1
State1 --> DoorOpenWithItem : Open Door
State1 --> ReadytoCook : Enter Time
}

state ReadytoCook {
[*] -> State1
State1 --> Cooking : Start
State1 --> DoorOpenWithItem : Open Door
State1 --> DoorShutWithItem : Cancel/Update Time
}

state Cooking {
[*] -> State1
State1 --> DoorOpenWithItem : Open Door/Stop Timer
State1 --> DoorShutWithItem : Timer Expired
State1 -> ReadytoCook : Cancel
}

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0015 named "llms_emp_stm_results_0015" {
    event Open_Door named "Open Door";
    event Cancel named "Cancel";
    event Close_Door named "Close Door";
    event Place_Item named "Place Item";
    event Remove_Item named "Remove Item";
    event Close_Door_Zero_Time named "Close Door/Zero Time";
    event Enter_Time named "Enter Time";
    event Start named "Start";
    event Cancel_Update_Time named "Cancel/Update Time";
    event Open_Door_Stop_Timer named "Open Door/Stop Timer";
    event Timer_Expired named "Timer Expired";
    state DoorShut named "DoorShut" {
        state State1 named "State1";
        state State2 named "State2";
        [*] -> State1;
        State1 -> State2 : /Open_Door;
        State1 -> State1 : /Cancel;
        State2 -> [*] : /Close_Door;
    }
    state DoorOpen named "DoorOpen" {
        state State1 named "State1";
        [*] -> State1 : /Remove_Item;
        [*] -> State1;
        State1 -> [*] : /Place_Item;
    }
    state DoorOpenWithItem named "DoorOpenWithItem" {
        state State1 named "State1";
        [*] -> State1;
        State1 -> [*] : /Close_Door_Zero_Time;
        State1 -> [*] : /Enter_Time;
    }
    state DoorShutWithItem named "DoorShutWithItem" {
        state State1 named "State1";
        [*] -> State1;
        State1 -> [*] : /Open_Door;
        State1 -> [*] : /Enter_Time;
    }
    state ReadytoCook named "ReadytoCook" {
        state State1 named "State1";
        [*] -> State1;
        State1 -> [*] : /Start;
        State1 -> [*] : /Open_Door;
        State1 -> [*] : /Cancel_Update_Time;
    }
    state Cooking named "Cooking" {
        state State1 named "State1";
        [*] -> State1;
        State1 -> [*] : /Open_Door_Stop_Timer;
        State1 -> [*] : /Timer_Expired;
        State1 -> [*] : /Cancel;
    }
    [*] -> DoorShut;
    DoorShut -> DoorOpen : /Close_Door;
    DoorOpen -> DoorOpenWithItem : /Place_Item;
    !DoorOpenWithItem -> DoorOpen : /Remove_Item;
    DoorOpenWithItem -> DoorShutWithItem : /Close_Door_Zero_Time;
    DoorOpenWithItem -> ReadytoCook : /Enter_Time;
    DoorShutWithItem -> DoorOpenWithItem : /Open_Door;
    DoorShutWithItem -> ReadytoCook : /Enter_Time;
    ReadytoCook -> Cooking : /Start;
    ReadytoCook -> DoorOpenWithItem : /Open_Door;
    ReadytoCook -> DoorShutWithItem : /Cancel_Update_Time;
    Cooking -> DoorOpenWithItem : /Open_Door_Stop_Timer;
    Cooking -> DoorShutWithItem : /Timer_Expired;
    Cooking -> ReadytoCook : /Cancel;
}
```

[上一组 `0014`](../0014/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0016`](../0016/README.md)
