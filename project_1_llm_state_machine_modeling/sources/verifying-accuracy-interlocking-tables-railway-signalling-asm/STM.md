# Verifying the accuracy of interlocking tables for railway signalling systems using abstract state machines - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把联锁表里的进路请求、道岔位置、信号机显示、反向进路锁闭和列车移动条件连成了一条完整控制链，可直接作为 `🚆` 方向的双 A 监督控制样本。

## 条目 1: Route request, point locking, and train movement controller from interlocking tables

- 控制对象：轨道交通与铁路控制领域的车站联锁进路请求、道岔布置与列车移动监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是以车站联锁表为基础的进路监督控制器，用进路占用、反向进路锁闭、道岔位置和信号显示共同决定是否锁闭进路、何时允许列车继续前进。
- 判断：算。对象是实际铁路信号系统里的联锁控制逻辑，原文明确给出了初始状态、联锁表字段、进路开放条件、道岔与信号联动，以及列车移动时的 guard 条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Table 1 前后的 transition-rule 描述
> Route column includes the route number ... Blocks indicate which blocks are included in that route. Point and signal columns define the proper situation of the points and the signals for that specific route. ... the counter routes column is to point out the routes which of them should be locked, while the route which is taken into account is assigned. Signals are redefined as R (red), G (green) and Y (yellow).
>
> Routes and points are not locked at the initial stage. All the signals are defined as vertical line (red), not allowing any passage.

#### 摘录 B

- 出处：第 4 页，联锁表驱动的进路建立与列车移动规则
> if a train requires the route R1 and if the requirements for the opening of the route have been fulfilled, (which means the rail blocks are available and no counter route is locked), then that particular route is locked. After having the route locked, points are arranged and locked. Afterwards, the signal state changes according to the interlocking table. Also, the motion of the train is determined based on the signal and point states and the moving direction.
>
> if TrainFrontSituationID(Train1) = TC21 ... if (SigColour(Signal21) = Green or SigColour(Signal21) = Yellow) ... if (PointPosition(P2) = Normal and PointPosition(P21) = Normal) then TrainFrontSituationID(Train1) := TC2

#### 摘录 C

- 出处：第 5-6 页，Table 1 与 failure injection 分析
> Route Blocks Points Signals Counter routes
>
> R6: TC21 ? TC2 ... P21: Normal ... S21: G All/{R6,R1,R3}
>
> Collision of trains simply means that two trains are on the same rail block at the same time. ... although Route1 and Route9 are counter routes ... it has been able to lock Route9, while Route1 is already locked.
>
> If a route is opened for one of the trains but point positions are not correctly arranged, then a possible derailment can happen.

### 2. 基于原文整理后的自然语言描述

The interlocking controller starts from an all-red, all-unlocked configuration and reads each route request against the interlocking table, whose rows explicitly bind together route identity, occupied blocks, required point positions, signal aspects, and counter-route exclusions. When a requested route is admissible, the supervisor first locks the route, then arranges and locks the relevant points, and only afterwards changes the signal aspect, so route establishment is gated by both resource availability and mutual exclusion with counter routes. Train movement is also guard-driven rather than implicit: for example, a right-moving train at `TC21` may advance to `TC2` only when `Signal21` is `Green` or `Yellow` and both `P2` and `P21` are in the `Normal` position. Specific table rows such as `R6` encode which counter routes must stay locked while the current route remains active, so route allocation and release are coupled to a resource-exclusion structure rather than a simple linear sequence. The injected-fault analysis shows why these guards matter: if a counter route is incorrectly allowed or a point is misaligned, the same model reaches collision or derailment conditions, making the controller a concrete EFSM-style railway supervision sample rather than a purely formal-methods artifact.

### 3. 逐句溯源

1. 句子 1：The interlocking controller starts from an all-red, all-unlocked configuration and reads each route request against the interlocking table, whose rows explicitly bind together route identity, occupied blocks, required point positions, signal aspects, and counter-route exclusions.
   对应摘录：A
2. 句子 2：When a requested route is admissible, the supervisor first locks the route, then arranges and locks the relevant points, and only afterwards changes the signal aspect, so route establishment is gated by both resource availability and mutual exclusion with counter routes.
   对应摘录：B
3. 句子 3：Train movement is also guard-driven rather than implicit: for example, a right-moving train at `TC21` may advance to `TC2` only when `Signal21` is `Green` or `Yellow` and both `P2` and `P21` are in the `Normal` position.
   对应摘录：B
4. 句子 4：Specific table rows such as `R6` encode which counter routes must stay locked while the current route remains active, so route allocation and release are coupled to a resource-exclusion structure rather than a simple linear sequence.
   对应摘录：C
5. 句子 5：The injected-fault analysis shows why these guards matter: if a counter route is incorrectly allowed or a point is misaligned, the same model reaches collision or derailment conditions, making the controller a concrete EFSM-style railway supervision sample rather than a purely formal-methods artifact.
   对应摘录：C
