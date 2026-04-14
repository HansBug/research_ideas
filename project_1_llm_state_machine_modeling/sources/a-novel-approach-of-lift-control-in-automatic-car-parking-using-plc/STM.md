# A Novel Approach of Lift Control in Automatic Car Parking Using PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动立体车库升降机的 `manual / auto` 顶层模式、按楼层差决定上下行、慢速传感减速、到位停机和报警联锁写成了完整控制链。

## 条目 1: Auto-Manual Lift Controller for Multilevel Parking
- 控制对象：智慧停车领域的立体车库升降机控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是自动立体车库中的 PLC 升降机控制模块，用传感器、VFD 和 auto/manual 两级控制逻辑把车辆升降到目标楼层并在异常时进入报警/急停分支。
- 判断：算。对象是实际停车设备的升降机控制器，原文不仅给出楼层选择和上下行逻辑，还明确写出了 manual mode、auto mode、slow sensor、stop sensor、alarm acknowledgment 等控制条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction
> In this paper a novel approach for lift control is proposed in fully automatic Level Car Parking System which used to take cars in/out of system & park the cars. Entire system is controlled using a Programmable Logic Controller (PLC). As speed control is required for multiple speed setting & proper stopping accuracy, the lift will be driven by the VFD ... The pallet position on lift, accurate positioning between lift-level & safety interlocks are sensed from dedicated sensor.

#### 摘录 B
- 出处：第 3 页，Operational Sequence
> 1) Manual Mode: a) The lift manual mode operation is inching. b) The lift inched with spring action button in up or down direction for maintenance work. c) Facility to change the speed will not be given. d) The speed in the manual/maintenance mode is slow speed.
>
> 2) Auto Mode: a) lift is always waiting for command in auto mode b) The command given to the lift is in terms of direction and number of levels to move. c) depending upon the command direction lift starts to move respective direction d) Once slow sensor (fork sensor) is sensed the speed of the VFD is made slow. e) As soon as the stop sensor (fork sensor) is sensed the lift stops. f) The level position sensors are checked to ensure that the lift is stopped correctly.

#### 摘录 C
- 出处：第 4-5 页，Results / Conclusion
> The current position of the lift is sensed by pallet position sensors denoted as `P` & two fork sensors denoted as `F1` & `F2`. Fork sensors are used as slow speed & stop speed indication. Lift is kept in manual mode ... As soon as main lift down button is released, lift stop instantly at that time. Main lift always moves in slow speed when it is operating in manual mode.
>
> Whenever an alarm occurs whole lift goes into emergency case where the operator needs to acknowledge alarm to avoid major accidents at parking.

### 2. 基于原文整理后的自然语言描述

The multilevel parking lift is organized around two top-level modes: a manual inching mode for maintenance and an auto mode that waits for movement commands expressed as direction plus number of levels. In auto mode, the controller computes whether the lift should move upward or downward from the difference between source and destination levels, starts the VFD-driven lift in that direction, and then uses fork sensors to switch from normal motion to slow motion before issuing the stop at the target level. Separate pallet-position and level-confirmation sensors are used to verify that the lift is aligned with the requested level and that pallet transfer is safe. In manual mode, the lift moves only while the spring-action up or down button is pressed and always remains at slow speed. If an alarm or emergency case occurs, the lift enters a protected branch that requires operator acknowledgment before normal parking operation can resume.

### 3. 逐句溯源

1. 句子 1：The multilevel parking lift is organized around two top-level modes: a manual inching mode for maintenance and an auto mode that waits for movement commands expressed as direction plus number of levels.
   对应摘录：B
2. 句子 2：In auto mode, the controller computes whether the lift should move upward or downward from the difference between source and destination levels, starts the VFD-driven lift in that direction, and then uses fork sensors to switch from normal motion to slow motion before issuing the stop at the target level.
   对应摘录：A, B
3. 句子 3：Separate pallet-position and level-confirmation sensors are used to verify that the lift is aligned with the requested level and that pallet transfer is safe.
   对应摘录：A, B, C
4. 句子 4：In manual mode, the lift moves only while the spring-action up or down button is pressed and always remains at slow speed.
   对应摘录：B, C
5. 句子 5：If an alarm or emergency case occurs, the lift enters a protected branch that requires operator acknowledgment before normal parking operation can resume.
   对应摘录：C
