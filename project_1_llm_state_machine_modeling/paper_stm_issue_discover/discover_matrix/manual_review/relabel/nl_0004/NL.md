<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0004 -->
# NL 规约材料 · `nl_0004`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0004`](./0004.md)、[`0014`](./0014.md)、[`0024`](./0024.md)、[`0034`](./0034.md)、[`0044`](./0044.md)、[`0054`](./0054.md)。它们由**同一份 NL 规约**（sha8 `3110cbcf`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **10** 段（`NL-L001` … `NL-L010`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0004.json](../translations/nl_0004.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1. The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal. | 1. 系统起始于 DoorsClosing 状态，并在车门关闭时迁移到 InMotion，由 "Closed/SendDeparted" 信号触发。 |
| `NL-L002` | 2. In the InMotion state, the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected. | 2. 在 InMotion 状态中，系统可以要么在其到达时迁移到 Stopping 状态，由 "Arrived/Stop, Send Arrived" 信号指示，要么迁移到 EmergencyStopping 状态，如果检测到障碍物。 |
| `NL-L003` | 3. When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal. | 3. 当检测到障碍物时，系统进入 EmergencyStopping 状态，其包含动作 "Emergency Stop" 并发送 "Obstacle Detected" 信号。〔原文如此：actions 用了复数，但其后只给出 "Emergency Stop" 一项动作〕〔译者存疑：and sends 的主语可读作 which（即 EmergencyStopping 状态），也可读作 the system；译文用「其」保留该歧义〕 |
| `NL-L004` | 4. Within the InMotion state, the system operates in three substates: Accelerating, Cruising, and Approaching, which represent different phases of the train's motion. | 4. 在 InMotion 状态内部，系统在三个 substates（子状态）中运行：Accelerating、Cruising 和 Approaching，它们代表列车运动的不同阶段。 |
| `NL-L005` | 5. The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal. | 5. 系统起始于 Accelerating substate（子状态），一旦达到巡航速度就移动到 Cruising substate（子状态），如 "Reached Cruising/Cruise" 信号所指示。 |
| `NL-L006` | 6. If the system is in the Accelerating substate and approaches its destination, it transitions to the Approaching substate upon receiving the "Approached/Decelerate" signal. | 6. 如果系统处于 Accelerating substate（子状态）并接近其目的地，它就在收到 "Approached/Decelerate" 信号时迁移到 Approaching substate（子状态）。 |
| `NL-L007` | 7. The system in the Cruising substate transitions to the Approaching substate when it approaches the destination, triggered by the "Approached/Decelerate" signal. | 7. 处于 Cruising substate（子状态）的系统在其接近目的地时迁移到 Approaching substate（子状态），由 "Approached/Decelerate" 信号触发。 |
| `NL-L008` | 8. The system enters the Accelerating substate when motion begins, marked by the "Entry/Accelerate" action. | 8. 系统在运动开始时进入 Accelerating substate（子状态），以 "Entry/Accelerate" 动作标记。〔原文如此：Entry 首字母大写，而 UML 的生命周期关键字 entry 为小写〕 |
| `NL-L009` | 9. In the Approaching substate, the system sends the "Send" signal and continues to approach the destination. | 9. 在 Approaching substate（子状态）中，系统发送 "Send" 信号并继续接近目的地。 |
| `NL-L010` | 10. The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate. | 10. 系统在接近目的地期间保持在 Approaching substate（子状态）中，直到它准备好停止或减速。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：约束元素：顶层 initial pseudostate（初始伪状态）指向 DoorsClosing；迁移 DoorsClosing → InMotion，触发标签为复合标签 "Closed/SendDeparted"（UML 中 `X/Y` 即 trigger（触发）/ action（动作），原文整体称之为 signal（信号），二者不对应）。歧义一（涉及初始点，判读时须格外注意）：本句只说系统起始于 DoorsClosing，**未说明 DoorsClosing 是否为 composite state（复合状态）**，也未说明其内部是否存在 initial pseudostate（初始伪状态）以及该初始点应指向何处；因此本句对「DoorsClosing 内部初始点」既不构成授权也不构成禁止。歧义二："when the doors are closed" 既可读作事件（车门关闭这一动作发生时），也可读作状态条件（车门处于关闭状态时）；译文「当车门关闭时」同样保留该歧义。歧义三："starts in" 未说明是首次上电还是任意时刻的启动。
- `NL-L002`：约束元素：两条以 InMotion 为源的迁移——InMotion → Stopping（标签 "Arrived/Stop, Send Arrived"）与 InMotion → EmergencyStopping（条件为检测到障碍物）。歧义一："it arrives" 的 it 指代不明（系统 / 列车）。歧义二：未说明这两条迁移的源端是 InMotion 整体（即从复合状态边界出发）还是其某个 substate（子状态）。歧义三：EmergencyStopping 那一支只给出条件 "if an obstacle is detected"，未给出显式 trigger（触发）名，无法判定它是事件名还是 guard（守卫）。歧义四："can either ... or" 中的 can 未说明这两条迁移是否穷尽了 InMotion 的全部出边。
- `NL-L003`：约束元素：EmergencyStopping 状态的动作集合——"Emergency Stop" 与发送 "Obstacle Detected"。歧义一：原文未区分这两个动作分别属于 entry（进入）、do（持续）还是 exit（退出）生命周期。歧义二："sends the \"Obstacle Detected\" signal" 中被发送的对象名与前一句用作迁移条件的 obstacle detected 措辞相同，原文未区分「发送的信号」与「触发迁移的事件」。歧义三：本句前半段与第 2 句后半段重复描述同一条 InMotion → EmergencyStopping 迁移，二者是否为同一约束，原文未言明。
- `NL-L004`：约束元素：层次结构——InMotion 为 composite state（复合状态），其内部恰含三个 substates（子状态）：Accelerating、Cruising、Approaching。「three」是确切数量，可用于判读子状态缺失 / 多余。本句只声明子状态的存在与数量，未声明其中哪一个是内部初始点（该约束由第 5 句给出）。
- `NL-L005`：约束元素：InMotion 内部的 initial pseudostate（初始伪状态）指向 Accelerating；迁移 Accelerating → Cruising，标签为复合标签 "Reached Cruising/Cruise"。歧义（涉及初始点，判读时须格外注意）："The system begins in the Accelerating substate" 中的 begins 未显式说明作用域——它既可读作「InMotion 这一 composite state（复合状态）内部的初始点」，也可读作「系统整体的启动点」；只有结合第 1 句（系统整体起始于 DoorsClosing）才能排除后者，原文本身并未明说。另："once cruising speed is reached" 是自然语言条件，与标签中的 Reached Cruising 是否为同一 trigger（触发），原文未言明。
- `NL-L006`：约束元素：迁移 Accelerating → Approaching，标签为复合标签 "Approached/Decelerate"。歧义一：条件 "is in the Accelerating substate and approaches its destination" 中，前半是源状态、后半究竟是 guard（守卫）还是 trigger（触发）的自然语言复述，原文未区分；且它与 "upon receiving the \"Approached/Decelerate\" signal" 是合取关系还是同一件事的两种说法，也未言明。
- `NL-L007`：约束元素：迁移 Cruising → Approaching，标签为复合标签 "Approached/Decelerate"，与第 6 句所用标签同名。歧义：同一 trigger（触发）名 "Approached/Decelerate" 被两条不同源端的迁移共用，原文未说明二者是同一事件的两条迁移还是重名。
- `NL-L008`：约束元素：Accelerating 的 entry（进入）动作 Accelerate。歧义（涉及初始点 / 进入点，判读时须格外注意）：本句既可读作对第 5 句「InMotion 内部初始点指向 Accelerating」的重复陈述，也可读作另立一条以 "when motion begins" 为条件的进入路径；"motion begins" 未映射到任何具名 trigger（触发），原文未区分这两种读法。另："marked by the \"Entry/Accelerate\" action" 把 entry 生命周期关键字与动作名一并写在引号内，作为「动作」而非「触发/动作」对，与第 1、5、6、7 句中 `X/Y` 的用法不一致。
- `NL-L009`：约束元素：Approaching 中的一个发送动作 Send；⛔ 原文未说明它属于 entry（进入）、do（持续）还是 exit（退出）生命周期（同第 3 句）。歧义："the system sends the \"Send\" signal" 把 Send 同时当作动作名与被发送的信号名，无法从本句判定被发送对象究竟是什么；原文共有三处引号内不含斜杠的标签（"Emergency Stop" / "Obstacle Detected" / "Send"），本处是其中唯一一处与同句动词同形的（sends the "Send" signal）。另："continues to approach the destination" 是持续性行为描述，未映射到任何 state（状态）、transition（迁移）或 variable（变量）。
- `NL-L010`：约束元素：Approaching 的驻留条件，未新增任何 state（状态）或 transition（迁移）。歧义一："until it is ready to stop or decelerate" 未给出对应的 trigger（触发）、guard（守卫）或目标状态，无法映射到任何具体迁移；判读「缺失迁移」时本句不构成明确约束。歧义二：decelerate 一词在第 6、7 句中已作为进入 Approaching 的动作出现，此处却作为离开 Approaching 的条件之一，原文未说明二者关系。歧义三："ready to stop" 与第 2 句的 Stopping 是否指同一件事，原文未言明。边界说明：本句的 while / until 只是自然语言的持续与终止表述，未引入任何时钟变量或秒级时间约束，仍在 $M = (S, E, V, Tr, A)$ 边界之内。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

【术语表 · 标识符原样保留】状态名（7 个）：DoorsClosing、InMotion、Stopping、EmergencyStopping、Accelerating、Cruising、Approaching。本份 NL 中不出现任何 variable（变量）名或 guard（守卫）表达式。

【复合标签 · 全部连引号带内容原样保留，不翻译、不拆开】共 9 处引号标签，其中 6 处为 UML `X/Y`（trigger（触发）/ action（动作））斜杠形式："Closed/SendDeparted"（第 1 句）、"Arrived/Stop, Send Arrived"（第 2 句）、"Reached Cruising/Cruise"（第 5 句）、"Approached/Decelerate"（第 6、7 句，共 2 处）、"Entry/Accelerate"（第 8 句）；另 3 处为不含斜杠的纯动作 / 信号名："Emergency Stop"、"Obstacle Detected"（第 3 句）、"Send"（第 9 句）。注意 "Arrived/Stop, Send Arrived" 内部含一个逗号，斜杠后是两个动作，整体仍是一个标签，不得按逗号断句。

【译法一致性】transition(s) to → 迁移到；moving to（第 5 句）→ 移动到（原文此处换用 moving，译文相应区分，未统一为「迁移」）；enters → 进入；starts in / begins in → 起始于；remains in → 保持在；substate(s) → 按 SPEC 第 4 条保留英文并加中文括注，第 4 句原文为复数故写作 substates（子状态），其余各句为单数写作 substate（子状态）；signal → 信号（原文把整条迁移标签也称作 signal，译文照译，不改称「事件」或「触发」）。

【反复出现的歧义（跨句）】一、原文通篇把 `X/Y` 复合迁移标签统称为 signal（信号），未区分 trigger（触发）与 action（动作）；凡涉及「某标签究竟是事件名还是动作名」的判读，本份 NL 均不提供依据。二、原文反复用自然语言条件（when it arrives / once cruising speed is reached / approaches its destination / when motion begins）与引号标签并列陈述，二者是合取关系还是同一件事的两种说法，全篇未加区分。三、涉及初始 / 起始作用域的语义共三处（第 1 句的 starts in、第 5 句的 begins in、第 8 句的 enters ... when motion begins），三处均未显式声明作用域（顶层 / composite state（复合状态）内部），译文均按字面直译，未替其消歧；⭐ 第 3 句也用了 enters，但那只是一条普通迁移的目标，不涉初始点。四、第 1 句只约束顶层初始点指向 DoorsClosing，全篇未有任何一句提及 DoorsClosing 内部是否存在 substate（子状态）或 initial pseudostate（初始伪状态）。

【原文质量问题】共 2 处已用〔原文如此〕标注：第 3 句 actions 用复数但只列一项动作；第 8 句 Entry 首字母大写而 UML 关键字 entry 为小写。另有 1 处〔译者存疑〕：第 3 句 and sends 的主语可读作 which 或 the system。其余未标注但值得注意的措辞问题：第 2 句 either ... or 的并列项不严格对称（either transition to X ... or to Y）；第 3 句与第 2 句后半段重复描述同一条迁移；第 8 句与第 5 句重复描述 Accelerating 的进入；第 9 句把 Send 同时当作动作名与信号名。

【建模对象边界】全篇未出现 clock（时钟）、时间约束、orthogonal region（正交区）或 concurrent activation（并发激活）等越界构造；第 9、10 句的 continues / while / until 均为自然语言持续性表述，不引入时钟语义，仍在 $M = (S, E, V, Tr, A)$ 边界之内。

【格式说明】原文第 1–9 行行尾各有一个尾随空格，第 10 行无尾随空格且无行尾换行；en 与 zh 均已照抄该尾随空格。第 4 句原文用冒号引出三项并列（逗号 + and），译文对应写作冒号 + 顿号 + 「和」，标点为一一对应映射。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal. 
  2 | 2. In the InMotion state, the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected. 
  3 | 3. When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal. 
  4 | 4. Within the InMotion state, the system operates in three substates: Accelerating, Cruising, and Approaching, which represent different phases of the train's motion. 
  5 | 5. The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal. 
  6 | 6. If the system is in the Accelerating substate and approaches its destination, it transitions to the Approaching substate upon receiving the "Approached/Decelerate" signal. 
  7 | 7. The system in the Cruising substate transitions to the Approaching substate when it approaches the destination, triggered by the "Approached/Decelerate" signal. 
  8 | 8. The system enters the Accelerating substate when motion begins, marked by the "Entry/Accelerate" action. 
  9 | 9. In the Approaching substate, the system sends the "Send" signal and continues to approach the destination. 
 10 | 10. The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate.
```
