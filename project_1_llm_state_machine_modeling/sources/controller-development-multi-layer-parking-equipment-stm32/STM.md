# The Controller Development of Multi-layer Parking Equipment Based on STM32 - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层六车位立体停车设备的自动/手动/故障模式和完整 parking process 写成了明确的传感器限位驱动链，正文强度足以形成双 A 样本。

## 条目 1: Automatic Parking Sequence with Manual/Fault Fallback
- 控制对象：三层六车位立体停车设备控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是面向三层六车位机械式停车设备的嵌入式控制器，用自动/手动模式、限位传感器和多个电机协调停车、取车、故障报警和人工调整。
- 判断：算。对象是实际停车设备控制器，原文不仅给出自动/手动/故障入口，还给出 parking process 中逐步受限位条件驱动的执行顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，`3. Software Architecture Design and Application Verification / Figure 8`，`paper_content.txt` 第 222-249 行
> Based on the control need of the three layers and six place parking equipment, design the software control flow. Control mode is divided into automatic and manual operation, and manual operation is apply to manual adjustment when the system can not run automatically due to equipment malfunctions or other problems. The automatic mode is the normal way of the multi-layer parking equipment, and can automatically park and withdraw the vehicle according to the customer demand, Figure 8 shows the main program flow chart of the parking system with three layers and six parking equipment. The controller makes a judgment of parking or taking the car according to user input, then enter the corresponding subroutine.
>
> Start -> Device initialization -> Meet the operational requirements -> Acquisition vehicle access information -> Emergency braking / Fault detect / Voice alarm / Manual adjustment / Parking / Withdraw -> Parking process / Withdraw process -> Vehicle finish -> End

#### 摘录 B
- 出处：第 6 页，`Figure 9 Parking Process Diagram`，`paper_content.txt` 第 258-305 行
> The parking process is basically the same as pick up. Here only introduce the parking process, the control system based on the information of user input to determine the parking, then find free place, according to predetermined algorithm processes to finish the parking process, the parking process diagram as shown in Figure 9.
>
> Start -> Gain parking information -> Free parking Spaces -> M3 start -> Mount limit reached -> Tray up -> M3 stop -> M1 start -> Rotate limit reached -> Mounter rotate -> M1 stop -> M2 start -> Uprights back -> Back to slow down limit reached -> M2 slow down -> Back to stop limit reached -> M2 stop -> M3 start -> Tray down -> Tray limit reached -> M3 stop -> M2 start -> Uprights forward -> Forward to stop limit reached -> M2 stop -> M3 start -> Mounter down -> Mounter limit reached -> M3 stop -> End
>
> YM2 slow down Forward to slow down limit reached

### 2. 基于原文整理后的自然语言描述

The multi-layer parking controller initializes the device, checks whether operational requirements are met, acquires vehicle access information, and then branches into automatic parking or withdrawing, manual adjustment, emergency braking, or fault detection with voice alarm. In normal operation it uses automatic mode to judge whether the user requests parking or taking the car and then enters the corresponding subroutine, while manual mode is reserved for adjustment when automatic running is blocked by equipment malfunctions or other problems. For parking, the controller gains parking information, confirms that a free parking space exists, raises the tray with `M3` until the mount limit is reached, rotates the mounter with `M1` until the rotate limit is reached, and drives the uprights backward with `M2`, including back slow-down and back stop limits. It then lowers the tray until the tray limit is reached, drives the uprights forward with `M2` through forward slow-down and forward stop limits, lowers the mounter with `M3` until the mounter limit is reached, and ends the parking sequence.

### 3. 逐句溯源

1. 句子 1：The multi-layer parking controller initializes the device, checks whether operational requirements are met, acquires vehicle access information, and then branches into automatic parking or withdrawing, manual adjustment, emergency braking, or fault detection with voice alarm.
   对应摘录：A
2. 句子 2：In normal operation it uses automatic mode to judge whether the user requests parking or taking the car and then enters the corresponding subroutine, while manual mode is reserved for adjustment when automatic running is blocked by equipment malfunctions or other problems.
   对应摘录：A
3. 句子 3：For parking, the controller gains parking information, confirms that a free parking space exists, raises the tray with `M3` until the mount limit is reached, rotates the mounter with `M1` until the rotate limit is reached, and drives the uprights backward with `M2`, including back slow-down and back stop limits.
   对应摘录：B
4. 句子 4：It then lowers the tray until the tray limit is reached, drives the uprights forward with `M2` through forward slow-down and forward stop limits, lowers the mounter with `M3` until the mounter limit is reached, and ends the parking sequence.
   对应摘录：B
