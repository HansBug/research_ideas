# Automatic Beverage Making Process - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把饮料批处理产线写成了从配方选择、阀门加料、计时搅拌、传感器定位灌装到包装与 `CIP` 清洗的完整 PLC 顺序控制链，细节足以支撑双 A 的 `🏭` 样本。

## 条目 1: Flavor-Mixing Bottle-Filling Batch Controller

- 控制对象：工业自动化与离散制造领域的饮料制备、灌装与包装批处理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 PLC 与 SCADA 实现的饮料批处理控制器，负责配方选择、原液和水的计时投料、搅拌、瓶位检测灌装、封盖包装以及批次结束后的 `CIP` 清洗。
- 判断：算。对象是真实制造控制过程，原文明确写出了输入触发、阀门和泵动作、计时混合、传感器定位、输送带启停和包装执行顺序，属于典型可抽取的顺序控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 40-59 行
> ... this project provides a method of manufacturing beverage drinks in an approach by implementation of automation using PLC & SCADA enabling beverage preparation, filling and packaging ... complete process offers execution of beverage manufacturing using the principle of batch process ...

#### 摘录 B

- 出处：第 1 页，Introduction，`paper_content.txt` 第 68-88 行
> ... the prototype depicts a commercial beverage preparation and filling unit which is controlled using programmable logic controller (PLC) and the whole process is monitored using SCADA ... the process begins with an user input for selection of flavour (Lime or Orange) ... the liquid concentrate of chosen flavour is mixed with the solution in the mixing tank ... filling the containers with the beverage drink it further moves to the packaging unit by a conveyor ...

#### 摘录 C

- 出处：第 2 页，`Demonstration`，`paper_content.txt` 第 125-145 行
> 1. The process starts with the input from the operator ... by choice of the flavor of beverage (Lime or Orange).
>
> 2. After selecting flavor, the valve of the reservoir tank opens and fills the solution into the mixing tank.
>
> 3. The valve of the chosen flavor tank opens and the flavor solution is added into the mixing tank.
>
> 4. On basis of timer instructions, the stirrer in the mixing tank rotates and mixes the solution with the flavor.
>
> 5. As the process of filling starts, the container placed on the conveyor is detected ... by a capacitive proximity sensor.
>
> 6. Once the bottle is detected, the conveyor stops and the filling pump starts to fill the bottle based on timer instructions ...
>
> 8. At packaging station, the preheated lids are placed on the bottle through a double acting cylinder.
>
> 9. At the end of each batch, cleaning is done by CIP method ...

#### 摘录 D

- 出处：第 3 页，`Demonstration using SCADA`，`paper_content.txt` 第 206-236 行
> ... when we switch ON (START) then the liquid concentrate starts to fill its respective tank. The pumps helps to fill water tank from the reservoir. By automatic opening of water valve, the water pass to the two mixing tank for a given time ... The valve of beverage tank opens ... Timer is set to the programmed for the valves opening and closing as per the tanks volume. A stirrer motor is fitted to mix the liquids ... Then in the next process the conveyor motor starts ... the container is detected at the exact point by a Proximity sensor at that time conveyor motor stops and filling process starts for a given amount of time ... Then the containers go to the packaging unit ... This process continues till mixing tank is empty until the batch is complete to undergo CIP. Then the whole process starts again.

### 2. 基于原文整理后的自然语言描述

The beverage controller is organized as a PLC-driven batch process that starts from an operator flavor selection and then executes a fixed sequence of filling, mixing, bottle handling, packaging, and end-of-batch cleaning actions. After the selected recipe is chosen, the controller opens the reservoir valve and the corresponding flavor-tank valve to charge the mixing tank, and it uses timer instructions to decide how long the stirrer should run and how long each liquid valve should stay open. When the batch reaches the filling stage, the conveyor advances bottles until a capacitive proximity sensor detects a container at the filling point, at which time the conveyor stops and the filling pump runs for a programmed interval. Once filling is complete, the bottle is transferred to the packaging station, where preheated lids are applied through a double-acting cylinder. The same batch supervisor keeps repeating the cycle until the mixing tank is empty, after which the process enters a `CIP` cleaning phase and then restarts the next batch.

### 3. 逐句溯源

1. 句子 1：The beverage controller is organized as a PLC-driven batch process that starts from an operator flavor selection and then executes a fixed sequence of filling, mixing, bottle handling, packaging, and end-of-batch cleaning actions.
   对应摘录：A, B, C
2. 句子 2：After the selected recipe is chosen, the controller opens the reservoir valve and the corresponding flavor-tank valve to charge the mixing tank, and it uses timer instructions to decide how long the stirrer should run and how long each liquid valve should stay open.
   对应摘录：C, D
3. 句子 3：When the batch reaches the filling stage, the conveyor advances bottles until a capacitive proximity sensor detects a container at the filling point, at which time the conveyor stops and the filling pump runs for a programmed interval.
   对应摘录：C, D
4. 句子 4：Once filling is complete, the bottle is transferred to the packaging station, where preheated lids are applied through a double-acting cylinder.
   对应摘录：C
5. 句子 5：The same batch supervisor keeps repeating the cycle until the mixing tank is empty, after which the process enters a `CIP` cleaning phase and then restarts the next batch.
   对应摘录：C, D
