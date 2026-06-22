# pairs_preview

## 示例 pair: unified_uml_state_train_0000

- 源文件：`assets/raw/umlcode_state_diagram_train.parquet`
- 源定位：`row=0; columns=input,uml_code,reasoning`
- 源 SHA-256：`02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d`
- eligibility：`conditional_final_pool`
- NL：

```text
Imagine you're at a restaurant and you're trying to order a meal. You want to order a burger, but you also want to order a side dish, a salad, and a drink. You want to pay for everything separately, but you don't want to have to navigate through multiple menus or tabs to order each item. You want to be able to order everything at once, so that you can see all the options and their prices in one place.

To achieve this, I want the software to allow me to create a single "menu" for all the items I want to order, and then I can select each item individually. The software should also allow me to view the menu and the prices of each item, and to pay for everything in one step. The menu should also be able to update itself automatically when I make changes to the menu items.

This feature would be particularly useful for people who like to eat out or who have trouble navigating multiple menus or tabs. It would also be useful for people who want to order food online or through a mobile app.
```

- STM_0：

```plantuml
@startuml
[*] --> "Menu Created"
"Menu Created" --> "Adding Items"
"Adding Items" --> "Viewing Menu"
"Viewing Menu" --> "Editing Menu"
"Viewing Menu" --> "Payment"
"Editing Menu" --> "Viewing Menu"
"Payment" --> [*]
@enduml
```
