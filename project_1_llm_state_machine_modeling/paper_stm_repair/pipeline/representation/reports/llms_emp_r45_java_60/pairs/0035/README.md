# Pair `0035`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0034`](../0034/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0036`](../0036/README.md)

- LLM：`Kimi`
- 模型/场景：Microwave Oven Control with entry and <br> exit actions
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE37`；Excel row：`37`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`84d17e092a8e8b903382f3a07c115bb1511466a24ce5d36dee4c24d90b990a76`
- NL SHA-256：`934e19bd4ae2a793c334fdcf486092d3aa20858f09ae892753ef87698feb061f`
- PlantUML SHA-256：`c16d76cb6627900d53a4d241695d00ef9d0986e7374bf9c1786279032db51594`
- FCSTM SHA-256：`b24ae4c657aad172783fdbacc31d613c5f2a6b481489b1ccdd0e5424dc8378a8`
- 结构裁决：`structure_preserved`
- source states / transitions：`6` / `15`
- mapped / blocked / silent drop：`15` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `1/1`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`6` / `15`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：微波炉 6 状态、15 条作者实际边全对应，包括 DoorOpen 的 Item Removed 自环；非标准 `state DoorShut as ... <<initial>>` 保留为 body，root 无真实 initial 因而使用 UnspecifiedInitial。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0035.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0035.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0035.json) | [人工总账](../../MANUAL_REVIEW.md)

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I37` | `true` | `84d17e092a8e8b903382f3a07c115bb1511466a24ce5d36dee4c24d90b990a76` | - | - |
| `phase_ii_format` | `U37` | `true` | `ec92e0afb25b2b6b75c37d2145018b50e626eb58e456dd8dc0b20aaad13c2ea9` | syntax error: stm MicrowaveStateMachine | YES |
| `phase_ii_grammar` | `Z37` | `true` | `ec92e0afb25b2b6b75c37d2145018b50e626eb58e456dd8dc0b20aaad13c2ea9` | Define composite state DoorShut {}, but there are no real child states in it | NO |
| `phase_ii_semantic` | `AE37` | `true` | `c16d76cb6627900d53a4d241695d00ef9d0986e7374bf9c1786279032db51594` | 1. interaction error | 1.0 |

## Official identity ledger

- status：`aligned`
- canonical / official states：`6` / `6`
- aligned transition endpoints：`15`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.missing_explicit_initial` | 1 |
| `R45.DEBT.opaque_state_body_semantics` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 15 |

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

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
state DoorShut as "Door Shut" <<initial>>
DoorShut --> DoorShut : Cancel
DoorShut --> DoorOpen : Door Opened
DoorOpen --> DoorOpen : Item Removed
DoorOpen --> DoorOpenWithItem : Item Placed
DoorOpenWithItem --> DoorOpen : Item Removed
DoorOpenWithItem --> DoorShutWithItem : Door Closed
DoorOpenWithItem --> ReadytoCook : Cooking Time Entered
DoorShutWithItem --> DoorOpenWithItem : Door Opened
DoorShutWithItem --> ReadytoCook : Cooking Time Entered
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
state llms_emp_feedback_final_0035 named "llms_emp_feedback_final_0035" {
    event Cancel named "Cancel";
    event Door_Opened named "Door Opened";
    event Item_Removed named "Item Removed";
    event Item_Placed named "Item Placed";
    event Door_Closed named "Door Closed";
    event Cooking_Time_Entered named "Cooking Time Entered";
    event Start named "Start";
    event Timer_Expired named "Timer Expired";
    state UnspecifiedInitial named "Unspecified initial";
    state DoorShut named "DoorShut\n[PlantUML body] as \"Door Shut\" <<initial>>";
    state DoorOpen named "DoorOpen";
    state DoorOpenWithItem named "DoorOpenWithItem";
    state DoorShutWithItem named "DoorShutWithItem";
    state ReadytoCook named "ReadytoCook";
    state Cooking named "Cooking";
    DoorShut -> DoorShut : /Cancel;
    DoorShut -> DoorOpen : /Door_Opened;
    DoorOpen -> DoorOpen : /Item_Removed;
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
    [*] -> UnspecifiedInitial;
}
```

[上一组 `0034`](../0034/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0036`](../0036/README.md)
