# PLC based Multilevel Automatic Car Parking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文正文虽然不长，但把 parking-in 主链中的按钮触发、旋转止挡、升降到位、开 ramp、下降投放和回原点顺序写得集中而完整，可稳定提取一条停车执行控制链。

## 备注

- 当前条目只采纳正文 `WORKING` 小节中明确展开的 `parking-in` 主链，不把 `scope` 小节对 retrieval 的愿景性描述扩写成未被正文逐步证明的控制细节。

## 条目 1: Rotate-lift-drop multilevel parking controller

- 控制对象：多层自动停车装置的旋转、升降与投放顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车位管理领域的 multilevel parking controller，用于在车辆驶上平台后按按钮指令驱动旋转、升降、开 ramp、下放车辆和回零复位。
- 判断：算。对象是实际立体停车机构的执行控制链，正文明确写出了按钮、limit switch、各层 proximity sensor、顶层到位、ramp 打开、下降投放和回到初始位这些顺序步骤；虽然 retrieval 只在 `scope` 中被概述，但 parking-in 主链本身已经足够完整。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 17-25 行
> A elevator is used to lift the car and park it at respective free slot. A PLC is used for checking vacancies and the control of the elevator. The proximity sensors installed in the system give PLC information regarding the free space as well as when the elevator has to stop depending on where the car is to be parked.

#### 摘录 B

- 出处：第 2-3 页，`WORKING`，`paper_content.txt` 第 160-180 行
> As the car comes on platform we have to press a button ... Then the rotation of the structure starts ... After rotating to a particular extent, it trips the limiting switch and then rotation of structure will stop.
>
> Then dc motor which is there for lifting the ramp will start ... at each level of the parking area we have proximity sensors ... When lift reaches to the top most sensor ... the ramp will open ... the platform lift starts but this time in anticlockwise direction ... it drops the car in the space ... Afterwards ramp will be closed again and lift goes down to its initial position.

#### 摘录 C

- 出处：第 3 页，`SCOPE OF THE PROJECT`，`paper_content.txt` 第 208-220 行
> The scope of this project is to design and develop a prototype of a PLC based Multilevel Automatic Car Parking System which parks and retrieves cars by an elevator ... All mechanisms needed to transport a car from the parking platform to the parking chambers ... are driven and controlled by Programmable Logic Controller (PLC) and the identification between cars and its owners are done by Human Machine Interface (HMI).

### 2. 基于原文整理后的自然语言描述

The parking controller begins when a car arrives on the platform and the operator presses the parking button, which starts rotation of the structure through the low-speed DC motor. When the rotating platform reaches the required angular position, a limit switch trips and stops the rotation stage. The lift motor then raises the ramp while per-level proximity sensors report the car position; once the top sensor is reached, the lift stops, the ramp opens through the forward gear motion, and the mechanism reverses direction to descend. During the downward motion the system drops the car into the designated parking space, then closes the ramp and returns the lift to its initial position for the next vehicle. The paper also states that the same PLC/HMI system is intended to support elevator-based parking and retrieval, but the fully detailed control chain given in the body is the parking-in sequence described above.

### 3. 逐句溯源

1. 句子 1：The parking controller begins when a car arrives on the platform and the operator presses the parking button, which starts rotation of the structure through the low-speed DC motor.
   对应摘录：B
2. 句子 2：When the rotating platform reaches the required angular position, a limit switch trips and stops the rotation stage.
   对应摘录：B
3. 句子 3：The lift motor then raises the ramp while per-level proximity sensors report the car position; once the top sensor is reached, the lift stops, the ramp opens through the forward gear motion, and the mechanism reverses direction to descend.
   对应摘录：A, B
4. 句子 4：During the downward motion the system drops the car into the designated parking space, then closes the ramp and returns the lift to its initial position for the next vehicle.
   对应摘录：B
5. 句子 5：The paper also states that the same PLC/HMI system is intended to support elevator-based parking and retrieval, but the fully detailed control chain given in the body is the parking-in sequence described above.
   对应摘录：C
