# Formal Specification and Verification of a Coordination Protocol for an Automated Air Traffic Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Protocol（协议/交互状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：AAC 中 AutoResolver、TSAFE、TCAS 与 controller/pilot 之间的控制权交接与返还条件足够明确。

## 条目 1: Layered control handoff in the Automated Airspace Concept
- 控制对象：自动空中交通控制系统中的冲突协调协议
- 状态机类型：Protocol（协议/交互状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：协议交互、显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空交通控制领域的 AAC coordination protocol，用于在不同冲突时间窗下在 controller、AutoResolver、TSAFE 和 TCAS 之间分配与回收控制责任。
- 判断：算。对象是实际空中交通控制系统中的协调控制协议，原文清楚给出了冲突时间窗、审批、自动接管、最后保护层和控制返还逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Section 3，对 AAC layered design 与责任分层的说明，行 176-232
> The strategic separation layer, referred to as the AutoResolver , addresses conﬂicts from three
> to 20 minutes in the future.
> ...
> The tactical separation layer, known as the Tactical Separation Assured Flight Environment
> (TSAFE),addressesconﬂictsprojectedtooccurlessthan3minutesinthefuture.
> ...
> Finally, the Trafﬁc Alert and Collision Avoidance System (TCAS) , is required by the Federal
> AviationAdministrationmandatetoaddresspossiblecollisionslessthan30secon dsinthefuture.
> ...
> The AutoResolver detects long-term conﬂicts, up to 20 min utes in the future,
> corresponding to time slot (1) ... If approved by the controller, the resolutions from the AutoResolver will be transmitted to the affected aircraft.
> TSAFE detects conﬂicts up to 3 minutes in the future. If the time to LOS is
> between 1 and 3 minutes ... TSAFE will ﬁrst alert the controller and wait for approval.
> In this circumstance, the controller has three choices: approve
> the resolution from TSAFE and give control responsibility for the involved aircraft to TSAFE,
> resolve the conﬂict manually, or wait without resolving the conﬂict.
> ...
> if the time to LOS falls below the TSAFEthreshold
> of 1 minute ... TSAFE will take control ... without having to wait for controller approval
> ...
> After the conﬂict is
> resolved, TSAFE will return control of the aircraft involved to the controller.

#### 摘录 B
- 出处：第 8 页，Figure 4，对 `TSAFE_Alert` 变量取值的说明，行 315-320
> there are three possible values for the variable TSAFE Alert: Non, AT and BT, corre-
> sponding to no LOS detected, LOS detected with time to LOS above and below the threshold.
> Since TSAFE and the AutoResolver construct pairwise conﬂict lists, there is such a variable for
> each pair of aircraft with different sufﬁxes.

### 2. 基于原文整理后的自然语言描述

The Automated Airspace Concept distributes conflict handling across layered components: AutoResolver addresses conflicts from `3` to `20` minutes ahead, TSAFE handles tactical conflicts up to `3` minutes ahead, and TCAS provides the last collision-avoidance layer for projected collisions under `30` seconds. If the time to loss of separation is between `1` and `3` minutes, TSAFE alerts the controller and waits for approval, after which the controller may transfer responsibility to TSAFE, resolve the conflict manually, or wait while keeping control. Once the controller has transferred control to TSAFE, the controller should not issue further resolutions for the involved aircraft until the conflict has been resolved. If the time to loss of separation drops below `1` minute, TSAFE takes control automatically without waiting for approval and later returns control to the controller after the conflict is resolved. The environment records this tactical situation through `TSAFE_Alert` values `Non`, `AT`, and `BT`, which distinguish no LOS, LOS above the threshold, and LOS below the threshold for each aircraft pair.

### 3. 逐句溯源

1. 句子 1：The Automated Airspace Concept distributes conflict handling across layered components: AutoResolver addresses conflicts from `3` to `20` minutes ahead, TSAFE handles tactical conflicts up to `3` minutes ahead, and TCAS provides the last collision-avoidance layer for projected collisions under `30` seconds.
   对应摘录：A
2. 句子 2：If the time to loss of separation is between `1` and `3` minutes, TSAFE alerts the controller and waits for approval, after which the controller may transfer responsibility to TSAFE, resolve the conflict manually, or wait while keeping control.
   对应摘录：A
3. 句子 3：Once the controller has transferred control to TSAFE, the controller should not issue further resolutions for the involved aircraft until the conflict has been resolved.
   对应摘录：A
4. 句子 4：If the time to loss of separation drops below `1` minute, TSAFE takes control automatically without waiting for approval and later returns control to the controller after the conflict is resolved.
   对应摘录：A
5. 句子 5：The environment records this tactical situation through `TSAFE_Alert` values `Non`, `AT`, and `BT`, which distinguish no LOS, LOS above the threshold, and LOS below the threshold for each aircraft pair.
   对应摘录：B
