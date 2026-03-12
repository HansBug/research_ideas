# DESIGNING OF RAILWAY SIGNALLING, INTERLOCKING SYSTEM AND CONTROLLING USING PLC WITH SCADA - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对道口触发和联锁原则有清楚文字说明，但大量实现细节依赖示意图与一般性介绍。

## 条目 1: Level-Crossing Actuation with Route Interlocking Constraints
- 控制对象：铁路信号与联锁控制系统

### 0. 条目识别与判定

- 一句话说明：这是轨道交通控制领域的 PLC/SCADA 联锁控制系统，用于管理道口障碍物动作并防止冲突进路同时放行。
- 判断：算。对象是实际铁路信号与联锁系统，原文明确给出了道口动作顺序和联锁约束条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Proposed System，`paper_content.txt` 第 23-29, 55-64 行
> The main task of interlocking is to provide a route request at suitable managing points and signals, which will not cause any collision. The proposed work is dependent on PLC, which are capable of performing signaling and interlocking process automatically which can even be changed, corrected and observed by using SCADA system.
>
> By employing the PLC for automatic control of railway trains would decrease the railway traffic and also automating railway gate control at the level crossings. ... Design of an automated railway signalling and interlocking system using Programic logic controller(PLC) will do all the operations that are performed manually.

#### 摘录 B
- 出处：第 2 页，Level Crossing / Interlocking，`paper_content.txt` 第 79-83, 95-100 行
> When activated, the lights flash, the bells ring and the barriers lower, as the crossing is usually automatic. ... when the barriers begin to go up, the square light stops flashing.
>
> Some of the fundamental principal of interlocking include: Signals may not be operated to permit conflicting train movements to take place at the same time on set route. Switches and other appliances in the route must be properly 'set' before a signal may allow train movements to enter that route.

### 2. 基于原文整理后的自然语言描述

The PLC/SCADA railway controller automatically handles signalling and interlocking tasks that were previously performed manually. At a level crossing, activation makes the warning lights flash, rings the bells, and lowers the barriers, and the indication changes again when the barriers rise. The interlocking logic prevents conflicting train movements from being permitted at the same time and requires switches and other route appliances to be correctly set before any signal authorizes entry into the route.

### 3. 逐句溯源

1. 句子 1：The PLC/SCADA railway controller automatically handles signalling and interlocking tasks that were previously performed manually.
   对应摘录：A
2. 句子 2：At a level crossing, activation makes the warning lights flash, rings the bells, and lowers the barriers, and the indication changes again when the barriers rise.
   对应摘录：B
3. 句子 3：The interlocking logic prevents conflicting train movements from being permitted at the same time and requires switches and other route appliances to be correctly set before any signal authorizes entry into the route.
   对应摘录：A, B
