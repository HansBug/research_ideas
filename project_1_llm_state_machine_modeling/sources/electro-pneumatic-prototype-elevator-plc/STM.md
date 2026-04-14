# Implementation of an Electro-Pneumatic Prototype Elevator Controlled by PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层电气动电梯的呼梯、楼层检测、升降执行与门控执行都写进同一套 PLC 梯形图控制链，足以形成 `EFSM + T0` 双 A 样本。

## 条目 1: Three-Floor Electro-Pneumatic Elevator PLC Supervisor
- 控制对象：楼宇机电与电梯控制领域的三层电气动电梯呼梯、升降与门控监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个由 PLC 梯形图控制的三层电气动原型电梯，控制器根据内外呼梯按钮、楼层接近开关、上下行继电器和门开闭继电器来驱动轿厢升降与门控。
- 判断：算。对象是明确的 prototype elevator controller，不是单纯机构介绍；原文给出了三层结构、按钮信号、上下行/门控继电器分工，以及基于传感器状态的整体软件流程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1、3 页，Abstract / Introduction，`paper_content.txt` 第 8-15、126-130 行
> The current paper presents a new simple and clear implementation method for prototype Electro-pneumatic prototype elevator system. The controller used for the prototype was implemented in Ladder logic on a PLC. ... The current work focuses on using pneumatic components and electrical components to build prototype model of an Electro-pneumatic elevator consisting of three stops (floors) ... controlled by using PLC.

#### 摘录 B
- 出处：第 5 页，`Procedure of Elevator Model Implementation`，`paper_content.txt` 第 207-225 行
> The cylinder which is (126 cm) length was divided into three equal sections. Each section represents a (42 cm) story in the building model. The proximate switches were used to identify these stories limits for the cabin. ... The green buttons fitted with LED ... are similar to the real buttons of the elevators. Every button in charge of calling the cabin to the floor by the passengers ... there are another buttons ... inside the real elevator ... The priority in following command is for the buttons inside the cabin.

#### 摘录 C
- 出处：第 7、10 页，`Relays / Software Process of The Elevator System`，`paper_content.txt` 第 300-308、418-420 行
> Three relays were used in the elevator model ... The first relay is (relay up) named as (rlyup) in the PLC program ... responsible for cabin ascending ... The second relay is (relay down) named as (rlydown) ... responsible for cabin descending ... The last relay ... responsible for opening and closing the cabins' door, which is named as (d-o and d-c) in the PLC program. ... The software process first check the status of the floors the up and down movement, the opening and shutting of the door, by using sensors, and then the Ladder program is implemented in the system to control all the movements in time.

### 2. 基于原文整理后的自然语言描述

The prototype elevator controller models a three-floor electro-pneumatic lift as a PLC-driven supervisory sequence over floor requests, cabin motion, and door actuation. The plant is instrumented with outside and inside call buttons, floor-limit proximate switches, and cabin-door hardware, while the controller explicitly gives priority to the buttons associated with cabin commands. On the actuator side, the ladder program separates `rlyup`, `rlydown`, and `d-o/d-c` so that ascent, descent, and door opening or closing are commanded as distinct control actions. Because the software first checks floor position, up/down movement, and door status through sensors before issuing the ladder-logic outputs, the paper exposes a complete `EFSM + T0` elevator sample with concrete inputs, guards, and actuator effects.

### 3. 逐句溯源

1. 句子 1：The prototype elevator controller models a three-floor electro-pneumatic lift as a PLC-driven supervisory sequence over floor requests, cabin motion, and door actuation.
   对应摘录：A, C
2. 句子 2：The plant is instrumented with outside and inside call buttons, floor-limit proximate switches, and cabin-door hardware, while the controller explicitly gives priority to the buttons associated with cabin commands.
   对应摘录：B
3. 句子 3：On the actuator side, the ladder program separates `rlyup`, `rlydown`, and `d-o/d-c` so that ascent, descent, and door opening or closing are commanded as distinct control actions.
   对应摘录：C
4. 句子 4：Because the software first checks floor position, up/down movement, and door status through sensors before issuing the ladder-logic outputs, the paper exposes a complete `EFSM + T0` elevator sample with concrete inputs, guards, and actuator effects.
   对应摘录：B, C
