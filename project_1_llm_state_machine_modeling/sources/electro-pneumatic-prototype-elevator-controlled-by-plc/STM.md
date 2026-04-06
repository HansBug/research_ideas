# Implementation of an Electro-Pneumatic Prototype Elevator Controlled by PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文文本足以支撑三层电-气动电梯的呼梯、内呼优先、上下行 relay、门开闭 relay、楼层传感与压力故障制动控制链，虽然流程图 OCR 不完整，但正文仍可达到双 A。

## 条目 1: Three-Stop Electro-Pneumatic Elevator Call-and-Door Controller

- 控制对象：楼宇机电与电梯控制领域的三层电-气动 PLC 电梯呼梯、行驶与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个三层电-气动电梯原型的 PLC 控制器，用内外呼梯按钮、proximity switch、relay、solenoid 和门控信号完成呼梯、上下行、开关门和应急制动。
- 判断：算。论文主体是实际 prototype elevator 的搭建与 PLC ladder 控制，正文明确给出输入按钮、楼层传感、relay 命名、门控与制动保护。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Introduction / current work
> The current work, focuses on using pneumatic components and electrical components to build prototype model of an Electro-pneumatic elevator consisting of three stops (floors) ... controlled by using PLC.
>
> The PLC ... is (LS\GLOFA-G7M-DR20A) series with (8) input and (12) output. It is programmed with a Ladder language.

#### 摘录 B

- 出处：第 5-6 页，Procedure of Elevator Model Implementation
> The proximate switches were used to identify these stories limits for the cabin.
>
> Every button in charge of calling the cabin to the floor by the passengers ... These buttons work like that ones' outside the cabin in calling the cabin by the passengers.
>
> The priority in following command is for the buttons inside the cabin ...

#### 摘录 C

- 出处：第 7 页，The Solenoids / Relays
> The first relay is (relay up) named as (rlyup) in the PLC program. This relay is responsible for the cabin ascending ...
>
> The second relay is (relay down) named as (rlydown) in the PLC program. This relay is responsible for cabin descending ...
>
> The last relay ... responsible for opening and closing the cabins' door, which is named as (d-o and d-c) in the PLC program.

#### 摘录 D

- 出处：第 9-10 页，Brake / Software Process
> If any defect in the pressure of the air cylinder happens ... the solenoid arm comes inside the solenoids' body ... as a result, the brakes contained cabin in same height.
>
> The software process first check the status of the floors the up and down movement, the opening and shutting of the door, by using sensors, and then the Ladder program is implemented in the system to control all the movements in time.

### 2. 基于原文整理后的自然语言描述

The electro-pneumatic elevator controller supervises a three-stop prototype using discrete PLC inputs and relay-driven pneumatic outputs. Floor call buttons outside the cabin and smaller inside-cabin buttons generate requests, with the paper explicitly giving priority to the inside-cabin commands. Proximity switches mark the three floor limits so the PLC can decide when the cabin has reached a requested stop. For motion, the PLC energizes `rlyup` to drive the solenoids that move the cabin upward or `rlydown` to drive the solenoids that move the cabin downward. When the cabin reaches the requested floor, the door relay pair `d-o / d-c` controls door opening and closing. The software process checks floor status, up/down movement, and door opening/shutting through sensors before executing the ladder program, and a pressure-switch/brake path holds the cabin if an air-pressure defect is detected.

### 3. 逐句溯源

1. 句子 1：The electro-pneumatic elevator controller supervises a three-stop prototype using discrete PLC inputs and relay-driven pneumatic outputs.
   对应摘录：A, C
2. 句子 2：Floor call buttons outside the cabin and smaller inside-cabin buttons generate requests, with the paper explicitly giving priority to the inside-cabin commands.
   对应摘录：B
3. 句子 3：Proximity switches mark the three floor limits so the PLC can decide when the cabin has reached a requested stop.
   对应摘录：B, D
4. 句子 4：For motion, the PLC energizes `rlyup` to drive the solenoids that move the cabin upward or `rlydown` to drive the solenoids that move the cabin downward.
   对应摘录：C
5. 句子 5：When the cabin reaches the requested floor, the door relay pair `d-o / d-c` controls door opening and closing.
   对应摘录：C, D
6. 句子 6：The software process checks floor status, up/down movement, and door opening/shutting through sensors before executing the ladder program, and a pressure-switch/brake path holds the cabin if an air-pressure defect is detected.
   对应摘录：D
