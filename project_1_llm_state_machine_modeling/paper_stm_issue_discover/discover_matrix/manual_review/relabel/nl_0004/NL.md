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
| `NL-L001` | 1. The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal. | 1. 系统起始于关门中状态（DoorsClosing state），并在门关闭时迁移至行驶中状态（InMotion），由关闭/发出离站信号（"Closed/SendDeparted"）触发。 |
| `NL-L002` | 2. In the InMotion state, the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected. | 2. 在行驶中状态中，系统可以要么在它到达时迁移至停车状态（Stopping），由到达/停车、发出到达信号（"Arrived/Stop, Send Arrived"）指示，要么如果检测到障碍物，迁移至紧急停车状态（EmergencyStopping）。 |
| `NL-L003` | 3. When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal. | 3. 当检测到障碍物时，系统进入紧急停车状态，该状态包含动作紧急停车（"Emergency Stop"）并发送检测到障碍信号（"Obstacle Detected"）。〔原文如此：actions 为复数，但仅列出一个动作〕〔译者存疑：and sends 的主语可读作 which（即 EmergencyStopping 状态），也可读作 the system，原文无法判定；译文按 which 读法承接〕 |
| `NL-L004` | 4. Within the InMotion state, the system operates in three substates: Accelerating, Cruising, and Approaching, which represent different phases of the train's motion. | 4. 在行驶中状态内部，系统以三个子状态（substates）运行：加速（Accelerating）、巡航（Cruising）和接近（Approaching），它们表示列车运动的不同阶段。 |
| `NL-L005` | 5. The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal. | 5. 系统起始于加速子状态，一旦巡航速度达到，移动至巡航子状态，由达到巡航/巡航信号（"Reached Cruising/Cruise"）指示。 |
| `NL-L006` | 6. If the system is in the Accelerating substate and approaches its destination, it transitions to the Approaching substate upon receiving the "Approached/Decelerate" signal. | 6. 如果系统处于加速子状态并接近其目的地，它在接收到接近/减速信号（"Approached/Decelerate"）时迁移至接近子状态。 |
| `NL-L007` | 7. The system in the Cruising substate transitions to the Approaching substate when it approaches the destination, triggered by the "Approached/Decelerate" signal. | 7. 处于巡航子状态的系统在接近目的地时迁移至接近子状态，由接近/减速信号触发。 |
| `NL-L008` | 8. The system enters the Accelerating substate when motion begins, marked by the "Entry/Accelerate" action. | 8. 系统在运动开始时进入加速子状态，由进入/加速动作（"Entry/Accelerate"）标记。〔原文如此："Entry/Accelerate" 中的 Entry 首字母大写，与 UML 生命周期关键字 entry 的小写写法不一致〕 |
| `NL-L009` | 9. In the Approaching substate, the system sends the "Send" signal and continues to approach the destination. | 9. 在接近子状态中，系统发出发送信号（"Send"）并继续接近目的地。 |
| `NL-L010` | 10. The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate. | 10. 系统在接近目的地期间保持处于接近子状态，直到它准备好停车或减速。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该句提出：初始状态为 DoorsClosing；迁移 DoorsClosing → InMotion，触发条件为门已关闭，触发信号为 "Closed/SendDeparted"。歧义点：原文同时给出条件（门已关闭）与信号（"Closed/SendDeparted"），未说明二者是否指向同一事件。
- `NL-L002`：该句提出：由 InMotion 出发的两条迁移——InMotion → Stopping（条件：到达；指示信号 "Arrived/Stop, Send Arrived"）与 InMotion → EmergencyStopping（条件：检测到障碍物）。歧义点：① 原文用 either … or … 只列出两条迁出，未说明除此之外 InMotion 是否还有其他迁出；② "indicated by" 未明说该信号是触发迁移的事件还是仅标记到达条件。
- `NL-L003`：该句提出：进入 EmergencyStopping 状态的条件（检测到障碍物），该状态包含的动作 "Emergency Stop" 与所发送的信号 "Obstacle Detected"。歧义点：第 2 句给出 InMotion → EmergencyStopping 的迁移，其条件同样为检测到障碍物；本句的「进入」与第 2 句的「迁移」是否指同一要求，原文未点明。
- `NL-L004`：该句提出层次要求：InMotion 状态包含三个子状态 Accelerating、Cruising、Approaching，表示列车运动的不同阶段；本句未给出这些子状态之间的迁移关系。
- `NL-L005`：该句提出：初始点要求（起始于 Accelerating 子状态）；迁移 Accelerating → Cruising，条件为达到巡航速度，由信号 "Reached Cruising/Cruise" 指示。歧义点：① "begins in" 未明确是仅首次运行还是每次进入 InMotion 时都从 Accelerating 开始；② "as indicated by" 未明说该信号是触发迁移的事件还是仅标记条件成立。
- `NL-L006`：该句提出：迁移 Accelerating → Approaching，条件为接近目的地，触发事件为收到信号 "Approached/Decelerate"。歧义点：本句与第 5 句给出两条均从 Accelerating 出发的迁移（分别至 Approaching 与 Cruising），原文未说明两条件同时成立时如何取舍。
- `NL-L007`：该句提出：迁移 Cruising → Approaching，条件为接近目的地，触发信号 "Approached/Decelerate"。歧义点：本句与第 6 句给出目标均为 Approaching 的两条迁移（分别自 Accelerating 与 Cruising 出发），条件与触发信号的表述相同，原文未说明二者有无区别。
- `NL-L008`：该句提出：进入 Accelerating 子状态的条件（运动开始）及关联动作 "Entry/Accelerate"。歧义点：① 原文未给出该进入的出发状态；② 本句的进入条件与第 5 句「起始于 Accelerating 子状态」的关系原文未说明；③ "marked by" 未明说该动作的执行时点。
- `NL-L009`：该句提出：系统处于 Approaching 子状态时发送信号 "Send" 并继续接近目的地。歧义点：① 原文未给出发送该信号的触发条件或时机；② 本句未给出从 Approaching 出发的迁移，仅描述该子状态内的持续行为。
- `NL-L010`：该句提出：系统在接近目的地期间保持在 Approaching 子状态，直到准备好停车或减速。歧义点：① 原文未说明「准备好停车或减速」之后的去向；② 此处的「停车」「减速」与第 2 句的 Stopping 状态及信号 "Approached/Decelerate" 是否对应，原文未点明。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英文原文 → 选定中文译名）：

状态：DoorsClosing state → 关门中状态；InMotion state → 行驶中状态；Stopping state → 停车状态；EmergencyStopping state → 紧急停车状态。

子状态：Accelerating substate → 加速子状态；Cruising substate → 巡航子状态；Approaching substate → 接近子状态；substates → 子状态。

信号："Closed/SendDeparted" → 关闭/发出离站；"Arrived/Stop, Send Arrived" → 到达/停车、发出到达；"Obstacle Detected" → 检测到障碍；"Reached Cruising/Cruise" → 达到巡航/巡航；"Approached/Decelerate" → 接近/减速；"Send" → 发送。

动作："Emergency Stop" → 紧急停车；"Entry/Accelerate" → 进入/加速。

普通名词：doors → 门；obstacle → 障碍物；destination → 目的地；cruising speed → 巡航速度；motion → 运动。

反复出现的歧义：第 1、2、5、7 句均以「由……信号指示/触发」的写法把信号与迁移关联，但原文未明确该信号与迁移条件（门关闭、到达、达到巡航速度、接近目的地）之间的关系，即信号是否即触发事件、条件与信号是否须同时成立；「目的地」在全篇未给出定义；第 5 句「起始于 Accelerating 子状态」与第 8 句「运动开始时进入 Accelerating 子状态」的关系原文未说明；全篇仅第 2 句出现情态动词 "can"。

原文质量问题：第 3 句 actions 为复数但仅列出一个动作（"Emergency Stop"）；第 6、7 句分别给出自 Accelerating、Cruising 至 Approaching 的迁移，条件与触发信号的表述相同。整份观察：段 8 的 "Entry/Accelerate" 里 Entry 首字母大写，而 UML 关键字 entry 为小写 —— 该写法不一致已在段 8 就地标注。

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
