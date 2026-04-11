# Automated Driving Control in Highway Scenarios Through a Two-Level Hierarchical Architecture - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高速公路自动驾驶机动选择写成“高层路径规划 FSM + 低层鲁棒运动控制”的两层结构，并给出速度/距离跟踪切换的显式 hysteresis guard。

## 条目 1: Hierarchical highway maneuver-selection supervisor

- 控制对象：汽车与道路车辆控制领域的高速公路自动驾驶机动选择与轨迹规划监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用于高速公路自动驾驶的两层控制架构，高层 FSM 决定保持车道、跟车/控距、换道与超车类机动，低层控制器负责跟踪所生成的速度和轨迹。
- 判断：算。对象是实际自动驾驶控制系统而不是纯规划框架；原文明确写出层次结构、FSM 角色、可切换的 driving tasks，以及 `Speed Tracking <-> Distance Tracking` 的 guard 与 hysteresis。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 28-35 行
> We introduce an approach for automated driving in highway scenarios based on a two-level hierarchical architecture. The high-level consists of a path planner ... maneuvers of highway driving, such as lane keeping, lane change, velocity, and distance tracking ... A switching logic described by a finite state machine, based on acquired sensor data, selects the most appropriate maneuver to realize in the present driving scenario.

#### 摘录 B

- 出处：第 4 页，Section `III`，`paper_content.txt` 第 180-205 行
> The low-level controller computes the steering and acceleration actions needed to track the path computed at the higher level. A finite state machine (FSM) manages the switching among the considered maneuvers. ... The actual traffic conditions are considered by an FSM, which selects the most suitable maneuver to perform.

#### 摘录 C

- 出处：第 9 页，Section `D. Behavioral Logic`，`paper_content.txt` 第 710-733 行
> To manage the transition among the different driving functions, we introduce the finite-state machine (FSM) reported in Fig. 5. ... Supposing that the Lane Keeping function is always active, the transition Speed Tracking (ST)→Distance Tracking (DT) is governed by the hysteresis mechanism based on the relative distance dO between HV and OV ... `ST→DT if dO<dtar−dm1`; `DT→ST if dO>dtar+dm2` ... hysteresis thresholds introduced to avoid chattering during the switching ST↔DT.

### 2. 基于原文整理后的自然语言描述

The automated highway controller is organized as a two-level hierarchical architecture in which a high-level path-planner finite-state machine selects the maneuver objective and a lower-layer robust controller tracks the resulting path and speed references. The high-level supervisor explicitly covers lane keeping, lane change, speed tracking, and distance tracking, and it switches task according to traffic conditions observed by the onboard sensors rather than by swapping the whole control architecture. One documented mode change is the `Speed Tracking -> Distance Tracking` switch, which occurs when the relative distance `d_O` to the preceding vehicle drops below `d_tar - d_m1`, and the return switch to `Speed Tracking` is released only when `d_O` rises above `d_tar + d_m2`, creating hysteresis against chattering. After the maneuver is chosen, the corresponding MPC path-planning objective and the interpolated reference trajectory are handed to the low-level steering and acceleration controller, so the discrete supervisor stays tightly coupled to continuous motion control.

### 3. 逐句溯源

1. 句子 1：The automated highway controller is organized as a two-level hierarchical architecture in which a high-level path-planner finite-state machine selects the maneuver objective and a lower-layer robust controller tracks the resulting path and speed references.
   对应摘录：A, B
2. 句子 2：The high-level supervisor explicitly covers lane keeping, lane change, speed tracking, and distance tracking, and it switches task according to traffic conditions observed by the onboard sensors rather than by swapping the whole control architecture.
   对应摘录：A, B
3. 句子 3：One documented mode change is the `Speed Tracking -> Distance Tracking` switch, which occurs when the relative distance `d_O` to the preceding vehicle drops below `d_tar - d_m1`, and the return switch to `Speed Tracking` is released only when `d_O` rises above `d_tar + d_m2`, creating hysteresis against chattering.
   对应摘录：C
4. 句子 4：After the maneuver is chosen, the corresponding MPC path-planning objective and the interpolated reference trajectory are handed to the low-level steering and acceleration controller, so the discrete supervisor stays tightly coupled to continuous motion control.
   对应摘录：A, B, C
