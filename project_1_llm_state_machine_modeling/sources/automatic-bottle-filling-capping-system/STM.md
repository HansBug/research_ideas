# Automatic Bottle Filling And Capping System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多规格瓶体选择、旋转盘停位灌装、按时间截止灌装、停位封盖以及四路分拣出料写成一条完整控制链，足以构成双 A 制造样本。

## 条目 1: User-selected multi-bottle fill-cap-dispense cycle

- 控制对象：工业自动化与离散制造领域的多规格双液体瓶装灌装、封盖与分拣控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `250 ml / 500 ml`、`water / juice` 组合任务的瓶装生产控制器，用键盘输入、推瓶机构、旋转盘、灌装 IR、封盖 IR 和输送带把选型、灌装、封盖和分拣串成自动流程。
- 判断：算。对象是论文主控制系统，原文明确给出用户输入、瓶型选择、定时灌装、封盖触发和四路出料逻辑，不是单纯机构展示。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 11-17 行
> The main aim of the proposed system is to fill the bottles of varying volumes with two different liquids according to user input and automatically cap the filled bottles of different volumes on a single assembly and dispense it. ... The bottles are filled through a solenoid valve using a water pump. For the capping of bottles of different volumes two DC motors are used and capping is done by linear mechanism. Finally, the bottles are dispensed using a conveyor belt driven by a motor.

#### 摘录 B

- 出处：第 2-3 页，`3.2 Bottle Selection / 3.3 Bottle Placement / 3.4 Filling Process`，`paper_content.txt` 第 152-195 行
> The user will be prompted at the beginning to indicate how many 250 ml and 500 ml bottles should be filled with water and how many should be filled with juice ...
>
> After taking input from the user the system gets started and there are two pushing mechanisms ... one for 250ml bottles and one for 500ml bottles. The pushing mechanism pushes the bottle onto the rotating mechanism.
>
> After bottles are pushed onto the rotating mechanism the rotating mechanism starts rotating, IR sensor placed near the filling poles senses the bottle and stops the rotating mechanism. ... The filling of the bottle is done based on time, after a certain time when the bottle is filled the solenoid valve cuts off the water supply. ... the system will fill the 250ml bottle with water first and then the 250ml bottle with juice and then the 500ml bottle with water and at last the 500ml bottle with juice.

#### 摘录 C

- 出处：第 3-4 页，`3.5 Capping Process / 3.6 Dispensing Mechanism / Block Diagram`，`paper_content.txt` 第 197-216、230-273 行
> After the bottles are filled ... an IR sensor placed at the capping mechanism senses the bottle and stops the rotating mechanism, then the bottles are capped by using a linear mechanism in which two DC motors are used. One DC motor is used to move another DC motor UP and down, the other DC motor holds the cap of the bottle and tightens it.
>
> Once the bottles are capped then the rotating mechanism starts again ... the bottles are placed on the conveyor belt ... The dispensing is done at four different places, 250ml bottle with water at one place and 250ml bottle with juice at another place and so on.
>
> ... Upon sensing a bottle, a pump is activated to pump the liquid into the bottle through the solenoid valve ... Once the bottle is filled, the solenoid valve cuts off the liquid flow ... another IR sensor located near the capping mechanism senses the presence of the bottle, causing the rotating mechanism to stop.

### 2. 基于原文整理后的自然语言描述

The bottle-filling controller begins with a user-selection stage in which the operator specifies how many `250 ml` and `500 ml` bottles should be filled with `water` or `juice`, and this input determines the production sequence for the machine. After the appropriate push mechanism loads a bottle onto the rotating platform, the filling IR sensor stops the rotation at the fill pole and the corresponding pump-solenoid branch fills the bottle for a time-based interval until the valve cuts the flow. The paper makes the production order explicit for mixed jobs, such as `250 ml water -> 250 ml juice -> 500 ml water -> 500 ml juice`, so the controller is not just reactive at one station but also schedules a whole batch cycle. Once the bottle reaches the capping station, a second IR sensor stops the rotating mechanism again and a two-motor linear mechanism lowers and tightens the cap. After capping, the platform restarts, the conveyor carries the bottle out, and the machine routes finished products to four output positions according to bottle size and liquid type.

### 3. 逐句溯源

1. 句子 1：The bottle-filling controller begins with a user-selection stage in which the operator specifies how many `250 ml` and `500 ml` bottles should be filled with `water` or `juice`, and this input determines the production sequence for the machine.
   对应摘录：B
2. 句子 2：After the appropriate push mechanism loads a bottle onto the rotating platform, the filling IR sensor stops the rotation at the fill pole and the corresponding pump-solenoid branch fills the bottle for a time-based interval until the valve cuts the flow.
   对应摘录：A, B, C
3. 句子 3：The paper makes the production order explicit for mixed jobs, such as `250 ml water -> 250 ml juice -> 500 ml water -> 500 ml juice`, so the controller is not just reactive at one station but also schedules a whole batch cycle.
   对应摘录：B
4. 句子 4：Once the bottle reaches the capping station, a second IR sensor stops the rotating mechanism again and a two-motor linear mechanism lowers and tightens the cap.
   对应摘录：A, C
5. 句子 5：After capping, the platform restarts, the conveyor carries the bottle out, and the machine routes finished products to four output positions according to bottle size and liquid type.
   对应摘录：A, C
