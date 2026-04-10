# Design of stereoscopic warehouse control system based on PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文既给出了 X/Y/Z 三轴驱动和限位联锁，也给出了完整 `delivery -> 定位 -> 送叉 -> 放货 -> 回零` 子流程，双 A 成立。

## 条目 1: Tri-axis storage-and-reset stacker controller

- 控制对象：工业物流领域的立体仓库堆垛机三轴存取控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 Mitsubishi PLC 控制的小型立体仓库堆垛机系统，通过 X/Y 轴步进电机和 Z 轴叉取电机完成入库、回零和故障保护。
- 判断：算。对象是实际仓储控制系统，原文给出输出端口、限位和传感器映射，并把入库流程一步一步写成了 delivery 子流程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-4 页，`main circuit / hardware structure design`，`paper_content.txt` 第 56-63、79-113 行
> DC contactor KM1, KM2 control the direct and reverse rotation of Z-axis DC motor M1 to complete operation of pick and place the cargo; DC contactor KM3 control X, Y axis two stepper motor M2, M3 power supply access, and emergency shutdown in case of failure ...
>
> Y0 and Y1 ... control stepper motor M2, M3 ... Y2 and Y3 ... control the stepping motor M2 and M3 in the direction of motion. Y4 and Y5 drive the Z shaft DC motor respectively to perform positive and reverse movement. The coil branches of the two contactors of KM1 and KM2 are designed as an interlock circuit to prevent erroneous operation. ... X16-X26 terminal of PLC connects the photoelectric sensors of 9 positions ... X27-X35 terminal connection 7 limit switch ... used for self-resetting of the system.

#### 摘录 B

- 出处：第 4 页，`system software design / Figure 5`，`paper_content.txt` 第 114-126、156-174 行
> The system software design includes delivery subsystem, pick up subsystem, reset subsystem and fault protection subsystem. ... When the delivery signal is detected at the input of the system, the delivery program begins. First of all, to detect the position of the information, to detect whether it is out of stock, if detected goods, the system display error, reset procedures, reset to the original 0 positions, the end of the operation. If no goods are detected, proceed to the next step, the horizontal X-axis stepper motor forward and position it at a horizontal position on the shelf, then the vertical Y-axis stepping motor forward and position it to a shelf Position, and then reach the designated position, Z-axis motor is running, fork into the goods. Then, the fork is lowered and the goods are placed on the shelves. Z-axis motor reversal, the fork will be recovered ... Perform a reset procedure, reset the stacker, etc. to the original 0 position, and end the program.

### 2. 基于原文整理后的自然语言描述

The warehouse stacker controller receives storage-position requests and first checks sensor information to determine whether the target location is already occupied. If the requested slot is not available, the system raises an operation-error indication and runs the reset procedure back to the origin. If the slot is available, the PLC drives the horizontal X-axis stepper motor to the correct column, then drives the vertical Y-axis stepper motor to the correct row, and finally actuates the Z-axis fork motor to insert the cargo. After the fork lowers and places the goods on the shelf, the Z-axis reverses to retract the fork, the mechanism rises back to a safe height, and the reset subsystem returns the whole stacker to the zero position. Interlock and limit-switch logic protect the direct and reverse drive paths and cut power when a fault or boundary condition is reached.

### 3. 逐句溯源

1. 句子 1：The warehouse stacker controller receives storage-position requests and first checks sensor information to determine whether the target location is already occupied.
   对应摘录：A, B
2. 句子 2：If the requested slot is not available, the system raises an operation-error indication and runs the reset procedure back to the origin.
   对应摘录：B
3. 句子 3：If the slot is available, the PLC drives the horizontal X-axis stepper motor to the correct column, then drives the vertical Y-axis stepper motor to the correct row, and finally actuates the Z-axis fork motor to insert the cargo.
   对应摘录：A, B
4. 句子 4：After the fork lowers and places the goods on the shelf, the Z-axis reverses to retract the fork, the mechanism rises back to a safe height, and the reset subsystem returns the whole stacker to the zero position.
   对应摘录：B
5. 句子 5：Interlock and limit-switch logic protect the direct and reverse drive paths and cut power when a fault or boundary condition is reached.
   对应摘录：A
