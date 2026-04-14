# PLC Based Automatic Multistoried Car Parking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多层半圆形停车库的升降、旋转、楼层选择、气缸推送与回原点链路写成了完整 PLC 控制流程，足以稳定整理为高质量停车控制状态机样本。

## 条目 1: Semicircular Multistoried Parking Lift-Pallet Controller

- 控制对象：半圆形多层停车系统中的升降机与托盘联合控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是智慧停车领域的 PLC 停车控制器，负责在四栋三层半圆形车库之间完成空位检测、楼层/楼栋选择、升降、旋转、托盘推出和复位。
- 判断：算。对象是实际停车设备控制链，不是单纯 HMI 或装置展示；正文明确给出了传感器、限位开关、气缸、DCV、楼层优先级和停车完成后的回原点逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Section 2.3，`paper_content.txt` 第 156-173 行
> Entering of car inside the Escalator is ensured by the optical proximity sensor which is mounted on the escalator. Once car is entered in the escalator, other proximity sensors which are mounted on the each floor start sending their occupancy status to the PLC. Address of vacant floor is provided to the escalator by PLC. Escalator moves up ... Once car gets parked in the slot, escalator comes back to its original position.

#### 摘录 B

- 出处：第 3 页，Section 3.2，`paper_content.txt` 第 216-239 行
> This project requires three pneumatic cylinders ... These pneumatic cylinders are connected to 3/2 direction control valve (DCV). A direction control valve receives the signal from PLC and supplies proportionate air supply to cylinders. All cylinders get actuated at the same time and works on the same pressure ... Required pressure for actuation of cylinder is 3 psi.

#### 摘录 C

- 出处：第 4 页，Section 4.2，`paper_content.txt` 第 280-301 行
> PLC is used to control the movement of escalator and working of pneumatic mechanism ... Priorities for selection of building and floor are assigned to PLC using PLC programming ... PLC sends output signal to 3/2 Direction Control Valve which actuates three pneumatic cylinders. Pneumatic cylinder pushes the car inside the parking slot ... PLC gives the return command to Direction Control Valve and motor to move back to original position.

### 2. 基于原文整理后的自然语言描述

The parking controller starts when an optical proximity sensor confirms that a car has entered the lift pallet. The PLC then reads occupancy signals from the floor sensors, selects a vacant destination floor and building according to predefined priorities, and commands a bidirectional lift motor plus a rotary pallet drive so that the escalator reaches the assigned parking position. Limit switches stop the vertical and rotational motions precisely at the selected floor and building. Once the lift is aligned, the PLC actuates a 3/2 direction control valve that drives three synchronized pneumatic cylinders at 3 psi and pushes the palletized vehicle into the slot. After a completion signal is received from the parking-area sensor, the PLC issues a return command to the motor and pneumatic mechanism so the system goes back to its original ready position for the next car.

### 3. 逐句溯源

1. 句子 1：The parking controller starts when an optical proximity sensor confirms that a car has entered the lift pallet.
   对应摘录：A；`paper_content.txt` 第 157-159 行。
2. 句子 2：The PLC then reads occupancy signals from the floor sensors, selects a vacant destination floor and building according to predefined priorities, and commands a bidirectional lift motor plus a rotary pallet drive so that the escalator reaches the assigned parking position.
   对应摘录：A, C；`paper_content.txt` 第 160-170 行，280-291 行。
3. 句子 3：Limit switches stop the vertical and rotational motions precisely at the selected floor and building.
   对应摘录：A；`paper_content.txt` 第 169-170 行；以及同文前文第 138-153 行。
4. 句子 4：Once the lift is aligned, the PLC actuates a 3/2 direction control valve that drives three synchronized pneumatic cylinders at 3 psi and pushes the palletized vehicle into the slot.
   对应摘录：B, C；`paper_content.txt` 第 216-239 行，292-297 行。
5. 句子 5：After a completion signal is received from the parking-area sensor, the PLC issues a return command to the motor and pneumatic mechanism so the system goes back to its original ready position for the next car.
   对应摘录：A, C；`paper_content.txt` 第 172-173 行，297-301 行。
