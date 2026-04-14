# System Modeling in the COSMA Environment - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文主体是 COSMA 建模环境，但其中的 distributed brake controller 案例对制动力状态、邻车消息传播和距离触发升级链都写得很具体。

## 条目 1: Distributed railway brake-force propagation controller
- 控制对象：轨道交通领域的分布式列车制动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个列车各车厢独立 brake controller 组成的分布式制动系统，每个控制器依据速度、距离激活器、紧急制动杆和邻车消息选择本车制动力等级。
- 判断：算。对象是实际铁路制动控制子系统，原文给出了制动力主状态、邻车消息交互、距离触发和从 `break1` 到 `break2` 的升级路径。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，`3. Model of a distributed brake control system`，行 253-268
> Our case study is a simplified, distributed brake control system for railway transport.
> ...
> Every car of a train has one controller, which activates brakes of the car and selects a brake force.
> ...
> The controller obtains signals from: velocity meter, coils detecting distance from a station, emergency brake levers.
> ...
> It obtains also messages from one or two controllers, which are situated in the next and previous car of the train.
> ...
> While an indication of higher brake force arrives than actually selected, in that case the higher force is applied for local brakes.

#### 摘录 B
- 出处：第 4 页，主状态与信号定义，行 308-348
> We distinguish principal states of the controller, which are related to the applied break force.
> ...
> break0 - break force is 0,
> break1 - middle force,
> break2 - big force.
> ...
> Figure 3 depicts a part of this automaton. It shows two principal states (i.e., b2_break1, b2_break2) and eight transitional states, which control signal exchange.
> ...
> b2_commCord Emergency brake lever pulled
> ...
> b2_leftRecBreak2 Message "force 2" from the left controller
> ...
> b2_distSens1 Car passes the 1st distance activator
> b2_distSens2 Car passes the 2nd distance activator
> b2_distSens3 Car passes the 3rd distance activator
> speed0 Current car speed is low
> speed1 Current car speed is medium
> speed2 Current car speed is high

#### 摘录 C
- 出处：第 4-5 页，对升级链的说明，行 344-394
> B2_commCord reception (emergency brake) causes the transition form b2_break1 to b2_break2 through the states: b2_leftBreak2a and b2_rightBreak2. At these states, messages to the neighbor controllers are generated and acknowledges are awaited.
> ...
> B2_leftRecBreak2 reception from the left neighbor (his brake force is 2) causes the transition form b2_break1 to b2_break2 through the states: b2_leftBreak2Ack and b2_rightBreak2
> ...
> Distance detector generates three signals: b2_distSens1, b2_distSens2, b2_distSens3.
> ...
> The following transition depends on the actual train speed and can conduct to the states:
> b2_break1 - no change of brake force,
> b2_break2 - through the states b2_leftBreak2a and b2_rightBreak2, where respective messages to the neighbors are generated.

### 2. 基于原文整理后的自然语言描述

Each car in the distributed railway brake system owns a local brake controller that selects the car’s brake force while exchanging messages with the neighboring controllers. The principal controller modes are `break0`, `break1`, and `break2`, and the automaton augments these force levels with transitional communication states that send force-upgrade messages and wait for acknowledgements. When an emergency brake command is received, or when a neighbor reports force level `2`, the local controller escalates from `break1` to `break2` through intermediate message-exchange states such as `b2_leftBreak2a`, `b2_rightBreak2`, or the corresponding acknowledgement states. Distance-activator events `b2_distSens1/2/3` are also interpreted together with the current train speed, so the controller either keeps `break1` or upgrades to `break2` and propagates the stronger braking request to adjacent cars.

### 3. 逐句溯源

1. 句子 1：Each car in the distributed railway brake system owns a local brake controller that selects the car’s brake force while exchanging messages with the neighboring controllers.
   对应摘录：A
2. 句子 2：The principal controller modes are `break0`, `break1`, and `break2`, and the automaton augments these force levels with transitional communication states that send force-upgrade messages and wait for acknowledgements.
   对应摘录：B, C
3. 句子 3：When an emergency brake command is received, or when a neighbor reports force level `2`, the local controller escalates from `break1` to `break2` through intermediate message-exchange states such as `b2_leftBreak2a`, `b2_rightBreak2`, or the corresponding acknowledgement states.
   对应摘录：B, C
4. 句子 4：Distance-activator events `b2_distSens1/2/3` are also interpreted together with the current train speed, so the controller either keeps `break1` or upgrades to `break2` and propagates the stronger braking request to adjacent cars.
   对应摘录：B, C
