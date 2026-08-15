<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0005 -->
# NL 规约材料 · `nl_0005`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0005`](./0005.md)、[`0015`](./0015.md)、[`0025`](./0025.md)、[`0035`](./0035.md)、[`0045`](./0045.md)、[`0055`](./0055.md)。它们由**同一份 NL 规约**（sha8 `934e19bd`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **8** 段（`NL-L001` … `NL-L008`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0005.json](../translations/nl_0005.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1. The microwave starts in the DoorShut state. From this state, the system can either remain in DoorShut if a Cancel action is performed or transition to the DoorOpen state when the door is opened. | 1. 微波炉起始于门关状态（DoorShut）。自该状态起，系统可以要么保持在门关，如果取消动作（Cancel）被执行，要么迁移到门开状态（DoorOpen），当门被打开时。 |
| `NL-L002` | 2. When the Door Opened action occurs in the DoorShut state, the system transitions to the DoorOpen state. The door can be closed to return to the DoorShut state. | 2. 当开门动作（Door Opened）在门关状态中发生时，系统迁移到门开状态〔译者存疑：动作名 Door Opened 中间有空格，与本份其余名称（如 DoorShut）的连写方式不一致〕。门可以被关闭以返回到门关状态。 |
| `NL-L003` | 3. In the DoorOpen state, placing an item inside the microwave transitions the system to DoorOpenWithItem. If the item is removed, the system returns to DoorOpen. | 3. 在门开状态中，将物品放入微波炉内使系统迁移到门开含物（DoorOpenWithItem）。如果物品被取出，系统返回到门开。 |
| `NL-L004` | 4. From DoorOpenWithItem, the system can transition to DoorShutWithItem if the door is closed with zero time set or to ReadytoCook if cooking time is entered. | 4. 自门开含物起，系统可以迁移到门关含物（DoorShutWithItem），如果门在时间设置为零的情况下被关闭，或者到待烹饪（ReadytoCook），如果烹饪时间被输入。〔译者存疑：with zero time set 的挂靠不定——既可读作「关门」这一动作附带的独立条件（守卫），也可读作「零时间关门」整体是一个动作/触发；译文用「在……的情况下」保留两解，未替原文消歧〕 |
| `NL-L005` | 5. In the DoorShutWithItem state, opening the door transitions the system back to DoorOpenWithItem, while entering cooking time takes the system to ReadytoCook, where the cooking time is displayed and updated. | 5. 在门关含物状态中，打开门把系统迁移回门开含物，而输入烹饪时间把系统带到待烹饪，在那里烹饪时间被显示并更新。〔译者存疑：while 既可作对比连词（「而」），也可作时间连词（「与此同时」）；译文取对比义，因为时间义会蕴含两条迁移同时发生的并发语义，而并发超出本项目建模对象边界〕 |
| `NL-L006` | 6. In the ReadytoCook state, if the Cancel action is performed, the system returns to DoorShutWithItem, canceling or updating the cooking time. If the door is opened, the system transitions to DoorOpenWithItem. | 6. 在待烹饪状态中，如果取消动作被执行，系统返回到门关含物，取消或更新烹饪时间。如果门被打开，系统迁移到门开含物。 |
| `NL-L007` | 7. When the Start action is performed in ReadytoCook, the system transitions to the Cooking state, where the timer starts. | 7. 当启动动作（Start）在待烹饪中被执行时，系统迁移到烹饪状态（Cooking），在那里计时器启动。 |
| `NL-L008` | 8. In the Cooking state, opening the door stops the timer and the system transitions to DoorOpenWithItem, while if the timer expires, the system moves to DoorShutWithItem. A Cancel action transitions the system back to ReadytoCook. | 8. 在烹饪状态中，打开门停止计时器并且系统迁移到门开含物，而如果计时器到期，系统移到门关含物。取消动作把系统迁移回待烹饪。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该段规定初始点：微波炉起始于门关状态；并规定两条迁移：执行取消动作后保持在门关状态（去向与源状态相同），门被打开时迁移到门开状态。歧义：原文以 either…or… 列举这两种去向，未说明该列举是否穷尽。
- `NL-L002`：该段规定两条迁移：开门动作在门关状态发生时迁移到门开状态（与第 1 段的迁移重复），门被关闭时返回到门关状态。歧义：本段第 2 句未点名该返回迁移的源状态，仅由上下文推知为门开状态。
- `NL-L003`：该段规定两条迁移：门开状态下将物品放入微波炉内→门开含物；物品被取出→返回门开。歧义：本段第 2 句未点名该返回迁移的源状态，仅由上下文推知为门开含物；原文也未说明取出物品时门处于何种状态。
- `NL-L004`：该段规定门开含物状态的两条出迁移：门在时间设置为零的情况下被关闭→门关含物；烹饪时间被输入→待烹饪。歧义：原文的 zero time 未指明是何种时间（本段未出现 cooking 一词），由上下文看疑为烹饪时间设为零；原文也未说明这两条去向是否穷尽、两条触发条件是否互斥。
- `NL-L005`：该段规定门关含物状态的两条出迁移：打开门→返回门开含物；输入烹饪时间→带到待烹饪；并规定在待烹饪中烹饪时间被显示并更新（属对变量的要求）。歧义：原文未说明烹饪时间在何种情况下被更新。
- `NL-L006`：该段规定待烹饪状态的两条出迁移：执行取消动作→返回门关含物，同时取消或更新烹饪时间；门被打开→门开含物。歧义：原文未说明取消与更新如何取舍，也未说明返回门关含物后物品是否仍在微波炉内。
- `NL-L007`：该段规定一条迁移：待烹饪中执行启动动作→烹饪状态；并规定在烹饪状态中计时器启动。计时器启动涉及时间机制，属本项目建模对象（状态/事件/变量/迁移/动作）边界之外。歧义：原文未说明烹饪时间为零时启动动作是否仍可执行。
- `NL-L008`：该段规定烹饪状态的三条出迁移：打开门（计时器停止）→门开含物；计时器到期→门关含物；取消动作→返回待烹饪。其中计时器到期为时间类触发条件，原文未给出任何时长值，属本项目建模对象边界之外。歧义：原文未说明从烹饪状态返回待烹饪后烹饪时间的处置。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名中文译名对照表（英文原文→中文，正文严格按此表）：DoorShut→门关；DoorOpen→门开；DoorOpenWithItem→门开含物；DoorShutWithItem→门关含物；ReadytoCook→待烹饪；Cooking→烹饪；Cancel→取消动作；Start→启动动作；Door Opened→开门动作；microwave→微波炉；door→门；item→物品；cooking time→烹饪时间；timer→计时器；zero time→时间设置为零。其他观察：原文区分 cooking time 与 timer 两个词，但未明说二者关系；全篇未给出任何计时数值与单位；第 1 段与第 2 段对门关状态—开门→门开状态的迁移重复表述，且第 2 段的动作名 Door Opened 中间带空格，与本份其余名称的连写方式不一致；除 Cancel、Start、Door Opened 外，其余事件均以散文短语表述（如 opening the door、entering cooking time），未给出动作名；各段列举出迁移时均未声明是否穷尽。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. The microwave starts in the DoorShut state. From this state, the system can either remain in DoorShut if a Cancel action is performed or transition to the DoorOpen state when the door is opened. 
  2 | 2. When the Door Opened action occurs in the DoorShut state, the system transitions to the DoorOpen state. The door can be closed to return to the DoorShut state. 
  3 | 3. In the DoorOpen state, placing an item inside the microwave transitions the system to DoorOpenWithItem. If the item is removed, the system returns to DoorOpen. 
  4 | 4. From DoorOpenWithItem, the system can transition to DoorShutWithItem if the door is closed with zero time set or to ReadytoCook if cooking time is entered. 
  5 | 5. In the DoorShutWithItem state, opening the door transitions the system back to DoorOpenWithItem, while entering cooking time takes the system to ReadytoCook, where the cooking time is displayed and updated. 
  6 | 6. In the ReadytoCook state, if the Cancel action is performed, the system returns to DoorShutWithItem, canceling or updating the cooking time. If the door is opened, the system transitions to DoorOpenWithItem. 
  7 | 7. When the Start action is performed in ReadytoCook, the system transitions to the Cooking state, where the timer starts. 
  8 | 8. In the Cooking state, opening the door stops the timer and the system transitions to DoorOpenWithItem, while if the timer expires, the system moves to DoorShutWithItem. A Cancel action transitions the system back to ReadytoCook.
```
