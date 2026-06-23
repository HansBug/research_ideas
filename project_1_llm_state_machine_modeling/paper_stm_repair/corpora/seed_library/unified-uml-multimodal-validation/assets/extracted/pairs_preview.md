# pairs_preview

- raw parquet 行数：999
- validator 可回溯行数：999
- 可计生成 STM_0 行数：989
- 生成失败 / 非 PlantUML 行数：10（索引：[60, 101, 162, 194, 309, 418, 607, 785, 838, 890]）

## 示例 0

```text
pair_id: unified_uml_state_train_0000
NL: Imagine you're at a restaurant and you're trying to order a meal. You want to order a burger, but you also want to order a side dish, a salad, and a drink. You want to pay for everything separately, but you don't want to have to navigate through multiple menus or tabs to order each item. You want to be able to order everything at once, so that you can see all the options and their prices in one place. |  | To achieve this, I want the software to allow me to create a single "menu" for all the items I
STM_0: @startuml | [*] --> "Menu Created" | "Menu Created" --> "Adding Items" | "Adding Items" --> "Viewing Menu" | "Viewing Menu" --> "Editing Menu" | "Viewing Menu" --> "Payment" | "Editing Menu" --> "Viewing Menu" | "Payment" --> [*] | @enduml
```

## 生成失败示例（不计 eligible）

```text
pair_id: unified_uml_state_train_0060
STM_0: No valid PlantUML code found.
```
