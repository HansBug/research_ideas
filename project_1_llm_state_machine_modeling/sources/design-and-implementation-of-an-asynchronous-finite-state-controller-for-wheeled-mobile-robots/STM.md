# Design and Implementation of an Asynchronous Finite State Controller for Wheeled Mobile Robots - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展有限状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 WMR 的异步有限状态控制器写成了明确的车道跟随/检测/变道链，状态名、guard 条件、障碍阈值和输出接口都能直接落成自然语言状态机描述。

## 条目 1: Three-lane obstacle-avoidance lane-change controller for a WMR
- 控制对象：轮式移动机器人在三车道环境中的避障换道控制器
- 状态机类型：EFSM（扩展有限状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个小型 WMR 在三车道道路上执行 lane following 和 obstacle-driven lane change 的控制器。
- 判断：算。对象是实际移动机器人控制器，而不是纯路径规划方法；原文明确给出了异步 FSM、状态流图、障碍距离阈值、orientation guard 和输出 PWM 接口。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页 Abstract
> In the proposed scenarios, the WMR drives along a path until an obstacle is detected at less than 50 cm, causing the WMR to check whether the first lane is free to go and move on.

#### 摘录 B
- 出处：第 5 页，Section 2.2 `Software Design`
> These values are then processed and provided as input to the finite state machine controller.
>
> Each state has code to either keep the current lane or to turn in order to change lane, depending on the distance measured by the nearest obstacle ahead.
>
> The transition between states happens because of guard conditions on the measured distance and on the orientation of the vehicle with respect to the direction of the road.

#### 摘录 C
- 出处：第 6 页，Figure 5 `Scheme of robot's evolution overtime`
> Follow right lane
>
> Check middle lane
>
> Follow middle lane
>
> Check left lane
>
> Follow left lane
>
> STOP

#### 摘录 D
- 出处：第 8-9 页，Section 3 `Case Study / Flowchart Design`
> Within the flowchart, there are states that require the robot to perform certain actions, such as following the road, while continuously monitoring the environment to detect the presence of in-front obstacles.
>
> The inputs of the flowchart were measurements retrieved from sensors described in Section 2.3, while the outputs were the pulse width modulation to supply to the motors ... together with the heading of the servomotor linked to the ultrasonic sensor.
>
> The critical distance required to detect an obstacle was set at 0.5 m.

### 2. 基于原文整理后的自然语言描述

The wheeled mobile robot is controlled by an asynchronous finite-state machine that combines line following with obstacle-triggered lane changing in a three-lane road scenario. It starts in the rightmost-lane following state and continuously monitors ultrasonic distance, line-tracking feedback, and wheel-based orientation estimates while remaining on the current lane. When an obstacle is detected within `0.5 m`, the controller leaves the current `Follow` state and enters a lane-check state, where the next transition depends on guard conditions defined over the measured front distance and the robot orientation relative to the road. If an adjacent lane is free, the controller activates the lane-change action, rotates the robot with a bounded proportional controller, and then settles back into the corresponding `Follow middle lane` or `Follow left lane` state. The state machine outputs motor PWM commands and ultrasonic-sensor servo headings throughout this process, and if no admissible lane remains the execution reaches `STOP` instead of continuing blind motion.

### 3. 逐句溯源

1. 句子 1：The wheeled mobile robot is controlled by an asynchronous finite-state machine that combines line following with obstacle-triggered lane changing in a three-lane road scenario.
   对应摘录：A, B
2. 句子 2：It starts in the rightmost-lane following state and continuously monitors ultrasonic distance, line-tracking feedback, and wheel-based orientation estimates while remaining on the current lane.
   对应摘录：B, C, D
3. 句子 3：When an obstacle is detected within `0.5 m`, the controller leaves the current `Follow` state and enters a lane-check state, where the next transition depends on guard conditions defined over the measured front distance and the robot orientation relative to the road.
   对应摘录：A, B, D
4. 句子 4：If an adjacent lane is free, the controller activates the lane-change action, rotates the robot with a bounded proportional controller, and then settles back into the corresponding `Follow middle lane` or `Follow left lane` state.
   对应摘录：B, C, D
5. 句子 5：The state machine outputs motor PWM commands and ultrasonic-sensor servo headings throughout this process, and if no admissible lane remains the execution reaches `STOP` instead of continuing blind motion.
   对应摘录：C, D
