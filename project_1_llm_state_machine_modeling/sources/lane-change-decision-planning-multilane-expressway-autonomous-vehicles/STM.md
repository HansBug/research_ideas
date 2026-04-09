# Research on Lane-Change Decision and Planning in Multilane Expressway Scenarios for Autonomous Vehicles - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多车道高速场景的换道决策写成“模糊换道意愿 + 邻道安全等级 + 状态机驾驶逻辑”的完整控制链，既有离散状态也有安全等级和轨迹验证，原文与描述都足够双 A。

## 条目 1: Multilane lane-change decision FSM with fuzzy willingness and adjacent-lane safety rating

- 控制对象：汽车与道路车辆控制领域的多车道高速场景自动驾驶换道决策与轨迹规划控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于高速公路多车道场景的自动驾驶换道决策器，用模糊换道意愿和邻道安全等级驱动 lane-keeping / left-lane-change / right-lane-change 状态切换。
- 判断：算。对象是真实自动驾驶行为决策模块，不是单纯轨迹优化器；原文明确给出换道意愿三级决策、周边车辆三类横向行为、邻道安全等级、以及默认 lane keeping 的状态机驾驶逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，`Vehicle Lane-Change Decision Based on Fuzzy Inference System`，`paper_content.txt` 第 284-297 行
> After calculation by the fuzzy controller, the output initial lane-change willingness was calibrated to set the lane-change timing and a lane-change decision table was established.
> Lane-Changing Willingness Value ... no lane change / waiting for lane change / executing lane change.
> Firstly, the lateral movement state of vehicles around the self-driving car is classified into three behaviors: lane keeping, lane deviation, and lateral lane change.

#### 摘录 B

- 出处：第 8 页，`Adjacent Lane Safety Posture Determination`，`paper_content.txt` 第 531-548 行
> The safety posture of the target lane is classified according to the lateral movement of the vehicle ...
> If there is no space for a lane change in the adjacent lane on the left, the safety level of the target lane is recorded as 1.
> If there is space to change lanes ... and an associated vehicle is changing lanes into the target lane, the safety level ... is recorded as 2.
> If there is space ... and the associated vehicle is in a lane departure, the safety level ... is recorded as 3.
> If there is space ... and there is no associated vehicle in a lane departure, the safety level ... is recorded as 4.

#### 摘录 C

- 出处：第 10 页，`Vehicle driving logic and state machine`，`paper_content.txt` 第 672-697 行
> These two parts are combined to form a complete driving logic, as shown in Figure 4a. Based on this driving logic, a decision based on a finite state machine is designed, as shown in Figure 4b.
> In the figure, the values K, L, and R indicate lane keeping, lane changing to the left, and lane changing to the right, respectively.
> The lane-keeping state of the vehicle driving in the current lane is the default state, and the state transfer will be triggered when the condition is satisfied.

#### 摘录 D

- 出处：第 22-23 页，`Constant Speed Lane-Change Conditions`，`paper_content.txt` 第 1512-1528 行
> When the car is traveling for 4 s, the longitudinal relative distance ... is equal to the minimum safe distance Dsafe.
> As there is no space to change lanes on the right side of the car, the car can only change lanes to the left.
> After 7.5 s, the car has completed the lane change and enters lane 2.
> ... the safety level of the autonomous vehicle’s left and right adjacent lanes is 1 until 7.5 s ... after the lane change is completed ... the safety level to the left of the car becomes 4.

### 2. 基于原文整理后的自然语言描述

The controller first computes a fuzzy lane-change willingness and maps it into three discrete decision stages: `no lane change`, `waiting for lane change`, and `executing lane change`, while also classifying nearby vehicles as `lane keeping`, `lane deviation`, or `lateral lane change`. In parallel, it rates each adjacent lane with a four-level safety posture, where `1` means no lane-change space, `2` means the target lane is being entered by another vehicle, `3` means a nearby vehicle is departing, and `4` means the target lane is free for a safe maneuver. These signals are fused into a finite-state driving logic whose default state is `K` (lane keeping) and whose other two states are `L` and `R` for left and right lane-change execution. The simulation trace shows the state machine holding lane until the safety-distance threshold is met, selecting a left lane change when the right lane remains unavailable, completing the maneuver at `7.5 s`, and then updating the left-lane safety rating from `1` to `4` after the transition.

### 3. 逐句溯源

1. 句子 1：The controller first computes a fuzzy lane-change willingness and maps it into three discrete decision stages: `no lane change`, `waiting for lane change`, and `executing lane change`, while also classifying nearby vehicles as `lane keeping`, `lane deviation`, or `lateral lane change`.
   对应摘录：A
2. 句子 2：In parallel, it rates each adjacent lane with a four-level safety posture, where `1` means no lane-change space, `2` means the target lane is being entered by another vehicle, `3` means a nearby vehicle is departing, and `4` means the target lane is free for a safe maneuver.
   对应摘录：B
3. 句子 3：These signals are fused into a finite-state driving logic whose default state is `K` (lane keeping) and whose other two states are `L` and `R` for left and right lane-change execution.
   对应摘录：C
4. 句子 4：The simulation trace shows the state machine holding lane until the safety-distance threshold is met, selecting a left lane change when the right lane remains unavailable, completing the maneuver at `7.5 s`, and then updating the left-lane safety rating from `1` to `4` after the transition.
   对应摘录：D
