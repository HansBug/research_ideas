# Prototype Design and Application of a Semi-Circular Automatic Parking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把车库控制明确拆成 `vehicle acceptance` / `vehicle delivery` 两个顶层模式，并把 `OPLS` 选位和 `POC` 执行子流程、`5.2 sec / 2.75 sec` 运动时间和 `SW1 / SW2` 传感触发都写了出来，可直接作为停车控制样本。

## 条目 1: Acceptance-Delivery Parking Supervisor with OPLS and POC

- 控制对象：半圆形自动停车系统的车位分配、搬运与取车监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个真实半圆形多层停车原型的任务监督控制器，顶层在 `vehicle acceptance mode` 和 `vehicle delivery mode` 之间切换，下层再调用最优车位选择和搬运执行子过程完成停车与取车。
- 判断：算。对象是实际停车控制系统，不是单纯机械结构展示；正文给出了模式名、进入条件、选位规则、执行子程序和局部时间参数。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，系统工作流程，`paper_content.txt` 第 109-132 行
> The operation of the system can be explained with two operating mode: vehicle acceptance mode and vehicle delivery mode.
>
> After detecting the parking lot closest to the starting position within the empty parking lots as the lot to be parked, the control unit ... allows that the vehicle carrying unit gets the vehicle ... and then parks it in the detected parking lot.

#### 摘录 B

- 出处：第 6-7 页，控制程序与 OPLS，`paper_content.txt` 第 542-604 行
> The relevant procedure completes the parking process by executing the subroutines including the “Optimal Parking Lot Selection” (OPLS) and “Position Control” (POC) algorithms.
>
> The parking lot which has the shortest parking time ... is considered as the optimal parking lot.
>
> The Vehicle carrying unit covers the distance between two floors in vertical movement in 5.2 sec ... and the distance between two parking lot in horizontal motion in 2.75 sec.

#### 摘录 C

- 出处：第 7 页，`POC` 算法，`paper_content.txt` 第 650-694 行
> The POC algorithm ... is used to implement the parking entrance and exit processes.
>
> This algorithm generates the control signals needed by the stepper motors ... by executing 3 subroutines: back-and-forth movement subroutine, vertical movement subroutine and horizontal movement subroutine.
>
> The back-and-forth movement subroutine generates the control signals ... according to the switch position information of the reed relays ... until the SW2 switch is on ... or ... until the SW1 switch is on.

### 2. 基于原文整理后的自然语言描述

The semi-circular parking system is organized as a hierarchical supervisor with two top-level operating modes: `vehicle acceptance mode` for incoming cars and `vehicle delivery mode` for retrieval. In the acceptance branch, after plate recognition and operator confirmation, the controller runs `OPLS` to evaluate all free slots and select the one with the minimum transfer time from lot `14`, using a simple travel-time model built from `5.2 sec` per floor in vertical motion and `2.75 sec` per parking-lot step in horizontal motion. Once the target slot is chosen, the controller enters `POC`, which coordinates three execution subroutines for back-and-forth pallet motion, vertical positioning, and horizontal positioning to move the vehicle from the acceptance/delivery lot into the selected slot. In the delivery branch, the registered plate information is used to recover the stored parking location, and the same `POC` execution chain is reused in reverse to bring the vehicle back to the pickup lot. At the actuator level, the back-and-forth subroutine is sensor gated: the carrying arm advances until `SW2` becomes active and retracts until `SW1` becomes active, which gives the sample an explicit local timing and event-triggered execution structure.

### 3. 逐句溯源

1. 句子 1：The semi-circular parking system is organized as a hierarchical supervisor with two top-level operating modes: `vehicle acceptance mode` for incoming cars and `vehicle delivery mode` for retrieval.
   对应摘录：A
2. 句子 2：In the acceptance branch, after plate recognition and operator confirmation, the controller runs `OPLS` to evaluate all free slots and select the one with the minimum transfer time from lot `14`, using a simple travel-time model built from `5.2 sec` per floor in vertical motion and `2.75 sec` per parking-lot step in horizontal motion.
   对应摘录：A, B
3. 句子 3：Once the target slot is chosen, the controller enters `POC`, which coordinates three execution subroutines for back-and-forth pallet motion, vertical positioning, and horizontal positioning to move the vehicle from the acceptance/delivery lot into the selected slot.
   对应摘录：B, C
4. 句子 4：In the delivery branch, the registered plate information is used to recover the stored parking location, and the same `POC` execution chain is reused in reverse to bring the vehicle back to the pickup lot.
   对应摘录：A, B, C
5. 句子 5：At the actuator level, the back-and-forth subroutine is sensor gated: the carrying arm advances until `SW2` becomes active and retracts until `SW1` becomes active, which gives the sample an explicit local timing and event-triggered execution structure.
   对应摘录：C
