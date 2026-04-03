# DESIGNING OF RAILWAY SIGNALLING, INTERLOCKING SYSTEM AND CONTROLLING USING PLC WITH SCADA - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：💎 含核心样本
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对道口警示链、route/point 冲突约束以及同平台冲突时的 free-platform 分流都有明确文字，但大量实现细节仍依赖示意图与一般性介绍。

## 条目 1: Level-Crossing Actuation with Route Interlocking Constraints
- 控制对象：铁路信号与联锁控制系统
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是轨道交通控制领域的 PLC/SCADA 联锁控制系统，用于管理道口障碍物动作并防止冲突进路同时放行。
- 判断：算。对象是实际铁路信号与联锁系统，原文明确给出了道口动作顺序和联锁约束条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Proposed System，`paper_content.txt` 第 23-29, 55-65 行
> The main task of interlocking is to provide a route request at suitable managing points and signals, which will not cause any collision. The proposed work is dependent on PLC, which are capable of performing signaling and interlocking process automatically which can even be changed, corrected and observed by using SCADA system.
>
> By employing the PLC for automatic control of railway trains would decrease the railway traffic and also automating railway gate control at the level crossings. ... Design of an automated railway signalling and interlocking system using Programic logic controller(PLC) will do all the operations that are performed manually.

#### 摘录 B
- 出处：第 2-3 页，Level Crossing / Interlocking / SCADA Board，`paper_content.txt` 第 79-106, 149-155 行
> When activated, the lights flash, the bells ring and the barriers lower, as the crossing is usually automatic. More rarely, once the barriers fully lowered, the sound changes. For some level crossings, when the barriers begin to go up, the square light stops flashing.
>
> Some of the fundamental principal of interlocking include: Signals may not be operated to permit conflicting train movements to take place at the same time on set route. Switches and other appliances in the route must be properly 'set' before a signal may allow train movements to enter that route. In order to ensure that the signalling system never provides conflicting signals and the points are not set for more than one train that might end up proceeding on to the same section of track and hence suffering a collision, various schemes have been developed to coordinate the settings of the points and the signals within the region controlled by a signalbox or signal cabin.
>
> Sometimes it is possible of arriving two trains on same platform. In that cases one train should wait outside the platform. This problem can overcome by using Interlocking System. PLC automatically navigates the train to on a free platform.

### 2. 基于原文整理后的自然语言描述

The PLC/SCADA railway controller converts previously manual signalling and interlocking work into automatic route management and level-crossing control. At a level crossing, activation makes the warning lights flash, rings the bells, and lowers the barriers; once the barriers are fully down the sound may change, and when the barriers begin to rise the square light stops flashing. Interlocking is enforced at the resource level: a route request may be granted only at suitable managing points and signals, conflicting train movements may not be authorized on the same set route, and switches or other appliances must already be correctly set before any signal allows entry into the route. The same coordination logic keeps points and signals from being set for more than one train on the same section and, when two trains arrive for the same platform, one train waits outside while the PLC navigates the other to a free platform.

### 3. 逐句溯源

1. 句子 1：The PLC/SCADA railway controller converts previously manual signalling and interlocking work into automatic route management and level-crossing control.
   对应摘录：A
2. 句子 2：At a level crossing, activation makes the warning lights flash, rings the bells, and lowers the barriers; once the barriers are fully down the sound may change, and when the barriers begin to rise the square light stops flashing.
   对应摘录：B
3. 句子 3：Interlocking is enforced at the resource level: a route request may be granted only at suitable managing points and signals, conflicting train movements may not be authorized on the same set route, and switches or other appliances must already be correctly set before any signal allows entry into the route.
   对应摘录：A, B
4. 句子 4：The same coordination logic keeps points and signals from being set for more than one train on the same section and, when two trains arrive for the same platform, one train waits outside while the PLC navigates the other to a free platform.
   对应摘录：B
