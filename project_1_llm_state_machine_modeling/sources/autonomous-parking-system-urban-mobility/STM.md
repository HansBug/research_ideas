# Transport Automation in Urban Mobility: A Case Study of an Autonomous Parking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 APS 从 `drop-off` 到 `pick-up` 的自动泊车生命周期拆成五个可执行功能场景，并补出接管条件、泊车/离位动作包与失联制动规则，足以形成系统级停车 supervisor 样本。

## 条目 1: Drop-off-to-pick-up autonomous parking supervisor

- 控制对象：智慧停车与车位管理领域的自动驾驶泊车全流程监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个真实车端 APS supervisor，用移动端和车端通信把 `drop-off -> autonomous drive -> parking -> exit -> pick-up handover` 串成一条完整的自动泊车控制链。
- 判断：算。对象是明确的自动泊车控制系统而不是单纯 HMI 或轨迹规划算法；原文给出了五个主功能阶段、各阶段的进入条件、完成条件、驾驶/离位动作以及失联/不安全条件下的中止规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This paper is dedicated to the development of an autonomous parking system for on-street parking in urban areas. The system is capable of fully automated parking manoeuvres from drop-off to pick-up zones, thus removing human drivers from the vehicle control loop. The system autonomously navigates to the parking space and parks the vehicle without human intervention.

#### 摘录 B

- 出处：第 13 页，Section `4.5 Methodology`
> The overall APS is split into five major functional scenarios:
> 1. The APS starts from the drop-off zone;
> 2. Automated driving to a point of interest;
> 3. Automated manoeuvring into a parking slot;
> 4. Automated exiting of the parking slot;
> 5. Vehicle handover to the driver at the pick-up zone.
>
> The APS procedure starts with pulling up to the drop-off zone ... The vehicle checks whether all occupants have left the vehicle and all the doors are closed. When all the requirements are met, the APS vehicle assumes control of the vehicle. The parking slot is reserved.

#### 摘录 C

- 出处：第 13-16 页，Section `4.5 Methodology` 与 `5.2 Test Description`
> Automated driving to a point of interest. The vehicle navigates to a point of interest ... Several manoeuvres are performed, following a straight or curved lane, turning left/right, etc.
>
> Automated exiting of the parking slot ... The manoeuvres “accelerate/decelerate”, “manoeuvre out of the parking slot”, and “reverse driving” are required ... The APS vehicle autonomously drives to the pick-up zone to complete this step.
>
> In the event of functionality failure and the loss of connectivity, the AV immediately terminates the manoeuvre and applies the brakes.

### 2. 基于原文整理后的自然语言描述

The APS is organized as a top-level parking supervisor that starts from a driver-operated drop-off zone and hands vehicle control to the automation only after occupants have exited, doors are closed, and the parking slot has been reserved. Its nominal control chain contains five major scenarios: `drop-off initialization`, `drive to point of interest`, `parking-slot manoeuvre`, `slot exit`, and `driver handover at the pick-up zone`. The travel phases are themselves maneuver packages rather than single moves, because the controller may follow straight or curved lanes, turn left or right, accelerate or decelerate, reverse out of the slot, and then continue toward the designated pick-up point. Completion conditions are also explicit: parking ends only when the vehicle is collision-free, fits the assigned slot, and enters standby with the parking brake activated, while the final handover releases the slot after the driver re-enters the car. Safety supervision is part of the same lifecycle, since unsafe conditions, user abort, or communication loss force an immediate stop and brake application, making the APS a layered parking-control HSM rather than a mere trajectory-planning module.

### 3. 逐句溯源

1. 句子 1：The APS is organized as a top-level parking supervisor that starts from a driver-operated drop-off zone and hands vehicle control to the automation only after occupants have exited, doors are closed, and the parking slot has been reserved.
   对应摘录：A, B
2. 句子 2：Its nominal control chain contains five major scenarios: `drop-off initialization`, `drive to point of interest`, `parking-slot manoeuvre`, `slot exit`, and `driver handover at the pick-up zone`.
   对应摘录：B
3. 句子 3：The travel phases are themselves maneuver packages rather than single moves, because the controller may follow straight or curved lanes, turn left or right, accelerate or decelerate, reverse out of the slot, and then continue toward the designated pick-up point.
   对应摘录：C
4. 句子 4：Completion conditions are also explicit: parking ends only when the vehicle is collision-free, fits the assigned slot, and enters standby with the parking brake activated, while the final handover releases the slot after the driver re-enters the car.
   对应摘录：B, C
5. 句子 5：Safety supervision is part of the same lifecycle, since unsafe conditions, user abort, or communication loss force an immediate stop and brake application, making the APS a layered parking-control HSM rather than a mere trajectory-planning module.
   对应摘录：B, C
