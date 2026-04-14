# Smart Railway Gate Level Crossing System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路平交口的来车检测、告警、关闸、离车开闸和信号恢复链写成了对称的传感器驱动流程，虽然篇幅短，但控制主链完整，足以作为铁路道口方向的双 A `EFSM + T0` 样本入账。

## 条目 1: Train-Arrival Gate Closure and Road-Signal Recovery Cycle

- 控制对象：轨道交通与铁路控制领域的列车到达关闸与道路信号恢复控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用成对 `IR sensors`、`servo motors`、`LED signals` 和 `buzzer` 管理平交道口闭合与重新开放的铁路道口控制器。
- 判断：算。对象是实际铁路道口安全子系统，原文明确给出了 arrival / departure 两条检测链、告警动作、关闸动作、开闸动作以及道路信号的输出切换。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`III. PROPOSED SYSTEM`，`paper_content.txt` 第 54-59 行
> We use infrared sensors in our system; one pair of these sensors is used to detect train arrival in both directions, while the other pair detects train departure in both directions.

#### 摘录 B

- 出处：第 3 页，`system overview`，`paper_content.txt` 第 70-75 行
> IR sensors, motors, LED signals, a buzzer, and an Arduino Uno make up the system. ... The railway gates are opened and closed by servo motors. At railroad crossings, LED lights serve as traffic signals, and buzzers alert passing cars to the approaching train.
>
> The arrival sensor sends a signal to the microcontroller, which then proceeds to perform the following operations sequentially. A buzzer alerts passengers at the level crossing.

#### 摘录 C

- 出处：第 3-4 页，`Case 1 When train arrival is detected`，`paper_content.txt` 第 88-95 行
> Ir sensor detected the train and it sends message to ESP 32 to close the gates. The yellow led is enabled indicating the closing of gates flowed by the red led light and the gates are closed. The buzzer is also enabled indicating the closing of gates.

#### 摘录 D

- 出处：第 4-5 页，`Case 2 When the Train Departure is Detected / Conclusion`，`paper_content.txt` 第 115-123 行、第 140-145 行
> The IR Sensor at the other side of the level crossing detects the departure of the train and it sends message to ESP 32 to open the gates. The green led light is enabled indicating the opening of gates and the gates are opened.
>
> corresponding actions are taken by motor to open or close the gateway ... warning time for arrival of train or its departure is enough to take the corresponding decision and also in that much time the closing/opening of gateway through use of servo motor is done accordingly.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller uses separate arrival and departure `IR` sensors to decide when the road gate must leave its open state and enter a protected train-passage sequence. Once an arrival sensor detects a train, the controller enables the buzzer, turns on a yellow warning light, then switches to red and commands the servo-driven gates to close. The protected state is held until the departure-side sensor detects that the train has cleared the crossing, at which point the controller enables the green road light and reopens the gates. Because the same arrival-close and departure-open logic is described for both travel directions, the paper provides a clean bidirectional railway-crossing control cycle rather than only a single demo snapshot.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller uses separate arrival and departure `IR` sensors to decide when the road gate must leave its open state and enter a protected train-passage sequence.
   对应摘录：A, B
2. 句子 2：Once an arrival sensor detects a train, the controller enables the buzzer, turns on a yellow warning light, then switches to red and commands the servo-driven gates to close.
   对应摘录：B, C
3. 句子 3：The protected state is held until the departure-side sensor detects that the train has cleared the crossing, at which point the controller enables the green road light and reopens the gates.
   对应摘录：D
4. 句子 4：Because the same arrival-close and departure-open logic is described for both travel directions, the paper provides a clean bidirectional railway-crossing control cycle rather than only a single demo snapshot.
   对应摘录：A, D
