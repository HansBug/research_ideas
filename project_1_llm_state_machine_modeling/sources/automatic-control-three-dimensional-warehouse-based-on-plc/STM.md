# Automatic Control Three-Dimensional Warehouse based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三维自动仓库的“选位-检测工件-X/Z/Y 轴运动-送到 AGV 点-回原位”顺序和限位/原点/报警 I/O 写得完整，适合作为仓储控制 `EFSM + T0` 样本。

## 条目 1: Three-Axis Warehouse Store-and-Retrieve Controller
- 控制对象：工业自动化与离散制造领域的三维自动仓库存取控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个利用 PLC、三轴电机、抓取托盘和多组限位/原点/料位传感器完成自动入库搬运的立体仓库控制器。
- 判断：算。对象是明确的自动仓库存取系统，原文既给出 X/Y/Z 运动顺序，也给出 emergency stop、origin、limit、alarm 和库位检测 I/O，足以整理成可追溯的 `EFSM + T0` 条目。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract / C. DC motor
> This paper is based upon use of PLC (Programmable Logic Controllers), 3-ph motor and sensors for the purpose of automatic goods handling inside the warehouse and the logistics industries.
>
> The main objective of the project controls the three-dimensional warehouse in goods handling with help of PLCs. The whole process is done automatically based on input signals from the PLC to the respective devices.
>
> It is use to operate the directions of the stacker crane and the gripper. The motor operation is performed using PLC and relays. Triaxial operation is performed here that is, X axis, Y axis and Z axis. Hence three motors are used to perform this operation and one for the gripper movement.

#### 摘录 B
- 出处：第 2 页，Methodology Working
> - Select the location where the material is to be stored
> - Press start button followed by the store button.
> - If store button is pressed, sensor will sense the presence of material.
> - If material is display, motor ‘X’ will start rotating in forward direction till the selected location and will stop.
> - After that the motor ‘Z’ move up to material selected point,
> - Once the object reaches the selected position, motor ‘Y’ (in/out) tray(gripper) will move to take the material
> - If tray (gripper) selected object, the motor ‘Z’ and motor ‘X’ will move to AGV point.
> - After arriving object position, the motor ‘Z’ and motor ‘X’ will rotate in reverse direction to handling next object position

#### 摘录 C
- 出处：第 2-3 页，Display configuration position devices of PLC program
> I0.0 CEMG Emergency stop ... I0.3 3ELP 3-axis positive limit ... I0.4 3ORG1 3 axis origin 1 ... I0.7 3EL- 3 axis negative limit ... I2.4 U1ALM One-axis inverter alarm ... I2.6 U3ALM Three-axis inverter alarm ...
>
> I3.0 SQ1 Raw material warehouse position 1. Workpiece detection switch ... I6.3 SQ28 Raw material warehouse position 28. Workpiece detection switch.
>
> Q0.3 START Start relay ... Q0.4 STOP Stop relay ... Q0.5 DIS_LIM Over limit contact relay ... Q0.6 ALMHL Alarm indicator ... Q1.0 STOP_U Inverter stop.

### 2. 基于原文整理后的自然语言描述

The three-dimensional warehouse controller begins by receiving a target storage location and a start/store command, then checks through the input sensor chain that a workpiece is present. Once storage is confirmed, the PLC drives the `X` axis forward to the selected slot, raises the `Z` axis to the target level, and actuates the `Y` tray or gripper to take the material. After the object is secured, the controller commands the `Z` and `X` axes to move toward the AGV handoff point and then returns them in reverse to prepare for the next cycle. The sequence is guarded by emergency-stop, positive/negative limit, origin, inverter-alarm, and slot-detection signals, while the outputs include dedicated start, stop, over-limit, alarm, and inverter-stop relays. This gives a clear event-and-sensor-driven warehouse store-and-retrieve EFSM instead of a loose warehouse automation overview.

### 3. 逐句溯源

1. 句子 1：The three-dimensional warehouse controller begins by receiving a target storage location and a start/store command, then checks through the input sensor chain that a workpiece is present.
   对应摘录：A, B
2. 句子 2：Once storage is confirmed, the PLC drives the `X` axis forward to the selected slot, raises the `Z` axis to the target level, and actuates the `Y` tray or gripper to take the material.
   对应摘录：A, B
3. 句子 3：After the object is secured, the controller commands the `Z` and `X` axes to move toward the AGV handoff point and then returns them in reverse to prepare for the next cycle.
   对应摘录：B
4. 句子 4：The sequence is guarded by emergency-stop, positive/negative limit, origin, inverter-alarm, and slot-detection signals, while the outputs include dedicated start, stop, over-limit, alarm, and inverter-stop relays.
   对应摘录：C
5. 句子 5：This gives a clear event-and-sensor-driven warehouse store-and-retrieve EFSM instead of a loose warehouse automation overview.
   对应摘录：A, B, C
