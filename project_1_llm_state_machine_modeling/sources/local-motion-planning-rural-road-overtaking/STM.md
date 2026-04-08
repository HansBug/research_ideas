# Local Motion Planning for Overtaking Maneuvers in a Rural Road Environment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 rural-road overtaking 的行为层明确压成 `Free-Driving / Tracking / Overtaking` 三态 FSM，并把 ACC、IDM、comfort/sporty cost 设置和回退链一起写进正文。

## 条目 1: Three-State Rural-Road Overtaking Planner

- 控制对象：乡村道路环境中的自动驾驶超车行为与局部轨迹规划器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆控制领域的 rural-road overtaking behavior planner，用三态决策层在自由行驶、跟车和超车之间切换，再把状态结果交给 Frenet 轨迹生成、`ACC/IDM` 与 `MPC/PID` 控制链执行。
- 判断：算。对象是实际自动驾驶车辆的行为层控制器，原文给出了状态集合、切换条件、状态内动作、comfort/sporty 风格参数，以及完成超车后返回原状态的恢复规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6 页，`Figure 4` 附近，`paper_content.txt` 第 448-475 行
> Our simplified MOBIL model defines three states ...
>
> Free-Driving State ... no preceding vehicle ... trajectories crossing into the opposite lane are strictly prohibited ...
>
> Tracking State ... another vehicle is in front of the ego vehicle, preventing a safe overtake ... Adaptive Cruise Control (ACC) is realized ...
>
> Overtaking State ... triggered when the decision-making process deems overtaking feasible, and the driver approves it. The steps involved in this maneuver are swerving, overtaking, and returning to the original lane.

#### 摘录 B

- 出处：第 6 页，`6.1 Cost Function Based State Management`，`paper_content.txt` 第 477-497 行
> During the planning process, two distinct settings were identified beside the decision-based states: jerk minimization (comfort setting) and fastest trajectory execution (sporty setting). In the comfort setting, the cost function heavily weights the variation in lateral acceleration, whereas, in the sporty setting, the execution time is prioritized ...
>
> ... a sportier setting may lead to riskier decisions due to shorter trajectory execution times.

#### 摘录 C

- 出处：第 6 页，`6.2 Control Strategies`，`paper_content.txt` 第 512-526 行
> By default, the vehicle plans and proceeds free-driving along the trajectory in one of the operationally switchable driving styles (comfort or sporty). If a vehicle is detected ahead within a safe braking distance, the behavioral layer switches to the tracking state, and the vehicle adaptively matches its speed to the preceding vehicle and maintains a safe distance until the overtaking maneuver is triggered. Upon activation, the vehicle switches to the overtaking state, increases its speed, and selects trajectories that allow for a quick and safe overtaking. Once the maneuver is complete, the vehicle returns to the previous state and continues free-driving on its path.

### 2. 基于原文整理后的自然语言描述

The rural-road overtaking planner uses a three-state FSM composed of `Free-Driving`, `Tracking`, and `Overtaking`, and each state is tied to a different local-motion-planning policy rather than merely renaming the same controller. In free driving, opposite-lane trajectories are forbidden and the vehicle follows the reference path with the selected driving style; in tracking, the controller activates `ACC` with `IDM`-based longitudinal adaptation so the ego car keeps a safe distance behind the preceding vehicle. When overtaking is judged feasible and approved, the planner enters the overtaking state, increases speed, and executes a swerving-pass-return maneuver before falling back to the previous cruising behavior. The same behavior layer is parameterized by `comfort` and `sporty` cost settings, so the discrete state decisions remain coupled to continuous trajectory quality measures such as lateral acceleration variation and execution time.

### 3. 逐句溯源

1. 句子 1：The rural-road overtaking planner uses a three-state FSM composed of `Free-Driving`, `Tracking`, and `Overtaking`, and each state is tied to a different local-motion-planning policy rather than merely renaming the same controller.
   对应摘录：A
2. 句子 2：In free driving, opposite-lane trajectories are forbidden and the vehicle follows the reference path with the selected driving style; in tracking, the controller activates `ACC` with `IDM`-based longitudinal adaptation so the ego car keeps a safe distance behind the preceding vehicle.
   对应摘录：A, C
3. 句子 3：When overtaking is judged feasible and approved, the planner enters the overtaking state, increases speed, and executes a swerving-pass-return maneuver before falling back to the previous cruising behavior.
   对应摘录：A, C
4. 句子 4：The same behavior layer is parameterized by `comfort` and `sporty` cost settings, so the discrete state decisions remain coupled to continuous trajectory quality measures such as lateral acceleration variation and execution time.
   对应摘录：B, C
