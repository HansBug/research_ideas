# Research on Longitudinal Active Collision Avoidance of Autonomous Emergency Braking Pedestrian System (AEB-P) - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：AEB-P 的预警、自动制动接管和分层控制模块较清楚。

## 条目 1: Warning and braking handoff in the AEB-P system
- 控制对象：行人自动紧急制动系统（AEB-P）

### 0. 条目识别与判定

- 一句话说明：这是汽车主动安全控制领域的 AEB-P system，用于依据碰撞时间和制动安全距离先发出预警，再在必要时接管制动。
- 判断：算，但属于功能链路型样本。对象是实际 AEB 控制系统，原文给出了 warning model、automatic braking intervention 以及上下层控制模块之间的职责分配。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section 2，对 warning model 的说明，行 174-176
> system were explained. Based on the research of collision time (TTC), the braking safety distance,
> and other related theoretical systems, the AEB-P system early warning model was established,
> which deﬁnes the driving safety level and the working area of the AEB-P warning system.

#### 摘录 B
- 出处：第 4 页，Section 2，对 pre-braking warning function 的要求，行 214-215
> 6. The AEB-P system should have a collision avoidance warning function. Before the automatic
> intervention of emergency braking, it should be led by a driver to remind him of a potential

#### 摘录 C
- 出处：第 5 页，System architecture，对 five modules 的说明，行 222-222
> This system consisted of ﬁve modules, namely, sensing system, early warning system, self-learning

### 2. 基于原文整理后的自然语言描述

The AEB-P system establishes an early-warning model from collision time and braking safety distance and uses it to define the driving safety level and working area of the warning system. Before automatic emergency braking intervenes, the system provides a collision-avoidance warning to the driver. The system is organized into sensing, early warning, self-learning, upper-control and lower-control modules so that the desired deceleration can be translated into throttle and brake commands.

### 3. 逐句溯源

1. 句子 1：The AEB-P system establishes an early-warning model from collision time and braking safety distance and uses it to define the driving safety level and working area of the warning system.
   对应摘录：A
2. 句子 2：Before automatic emergency braking intervenes, the system provides a collision-avoidance warning to the driver.
   对应摘录：B
3. 句子 3：The system is organized into sensing, early warning, self-learning, upper-control and lower-control modules so that the desired deceleration can be translated into throttle and brake commands.
   对应摘录：C
