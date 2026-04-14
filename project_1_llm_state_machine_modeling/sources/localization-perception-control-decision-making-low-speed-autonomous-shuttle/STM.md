# Localization and Perception for Control and Decision Making of a Low Speed Autonomous Shuttle in a Campus Pilot Deployment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把低速 autonomous shuttle 的跟驰与信号处理决策直接写成 `CC / ACC / CACC / Stop` 控制链，并用仿真曲线验证状态切换。

## 条目 1: Three-State Low-Speed Shuttle Decision Supervisor

- 控制对象：汽车与道路车辆控制领域的低速 autonomous shuttle 决策与跟驰/信号处理监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个低速校园 shuttle 的决策监督器，用 GPS/Leddar/DSRC 输入在巡航、跟驰、协同跟驰和红灯停车之间切换。
- 判断：算。对象是实际自治车辆高层决策控制链，正文明确点名三类主状态并交代进入条件、保持条件和场景验证。

### 1. 原文摘录

#### 摘录 A

- 出处：第 10 页，`Test Scenario`，`paper_content.txt` 第 700-710 行
> The path to be followed is generated from the GPS points on the road and vehicle is set to autonomously drive on this path ... DSRC radio is mainly used for determination of the traffic light state in the intersection. Leddar sensor is utilized for detection of the distance between ego vehicle and preceding vehicle.

#### 摘录 B

- 出处：第 10-11 页，Section `A. Decision Making`，`paper_content.txt` 第 716-749 行
> a simple decision-making strategy is created with three main states.
> ...
> The developed decision making strategy consists of three main states. In Cruise Control (CC) state, the vehicle is given a velocity profile to follow as a longitudinal control strategy.
> ...
> In case there is any traffic light nearby on path, according to the state of the light it can go to stop state or continue.
> ...
> according to the distance, it goes to Adaptive Cruise Control (ACC) state or Cooperative Adaptive Cruise Control (CACC) state in the case of a communicating preceding vehicle for car following.
> In this state, the vehicle keeps a safe time gap with the preceding vehicle.

#### 摘录 C

- 出处：第 11-12 页，`HiL Simulation Results`，`paper_content.txt` 第 768-790 行
> in case of any other vehicle coming in front, vehicle goes to ACC mode to adapt the speed of preceding vehicle and keep the distance, disregarding the velocity profile.
> ...
> recorded vehicle velocity, vehicle decision state (Stop/ACC/CC) and traffic light state (green/red) was plotted
> ...
> starting around 90th second ... it comes across a non-communicating preceding vehicle ... autonomous vehicle goes to ACC mode and slows down to adapt to the speed and keep the distance
> ...
> Around 125th second, it comes close to the intersection where there is a traffic light which is at red signal state and it stops. It waits until the light is green and then continues its way.

### 2. 基于原文整理后的自然语言描述

The shuttle supervisor follows a planned campus route using GPS, Leddar, and DSRC inputs and organizes driving behavior into Cruise Control, ACC, and CACC, with stop behavior when the signal state requires it. In `CC`, the shuttle tracks a velocity profile derived from the current map segment so it can slow for curves, intersections, and traffic lights while continuously monitoring DSRC traffic-light messages. When a preceding vehicle is detected by the Leddar sensor, the controller switches to `ACC`, or to `CACC` when the preceding vehicle is communicating, and in these car-following modes it maintains a safe time gap instead of blindly following the nominal profile. When the traffic-light state is red, the decision logic enters stop behavior and waits until green before returning to route following. The simulation evidence reported in the paper shows the vehicle switching from `CC` to `ACC` around the 90th second and then stopping for a red light around the 125th second before resuming motion.

### 3. 逐句溯源

1. 句子 1：The shuttle supervisor follows a planned campus route using GPS, Leddar, and DSRC inputs and organizes driving behavior into Cruise Control, ACC, and CACC, with stop behavior when the signal state requires it.
   对应摘录：A, B
2. 句子 2：In `CC`, the shuttle tracks a velocity profile derived from the current map segment so it can slow for curves, intersections, and traffic lights while continuously monitoring DSRC traffic-light messages.
   对应摘录：A, B
3. 句子 3：When a preceding vehicle is detected by the Leddar sensor, the controller switches to `ACC`, or to `CACC` when the preceding vehicle is communicating, and in these car-following modes it maintains a safe time gap instead of blindly following the nominal profile.
   对应摘录：A, B, C
4. 句子 4：When the traffic-light state is red, the decision logic enters stop behavior and waits until green before returning to route following.
   对应摘录：B, C
5. 句子 5：The simulation evidence reported in the paper shows the vehicle switching from `CC` to `ACC` around the 90th second and then stopping for a red light around the 125th second before resuming motion.
   对应摘录：C
