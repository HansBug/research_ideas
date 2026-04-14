# CARMA II: A ground vehicle for autonomous surveying of alpha, beta and gamma radiation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `waitingforcall / movingtocurrentwaypoint / reversing` 三态、低电量回家、不可达 waypoint 跳过和污染阈值触发倒车重规划写得很完整，是很强的移动机器人任务 supervisor 样本。

## 条目 1: Radiation-aware waypoint survey supervisor

- 控制对象：CARMA II 地面辐射巡检机器人的高层 survey supervisor
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把 coverage waypoint 列表、低电量回家、污染阈值倒车、不可达 waypoint 跳过和 home return 统一组织起来的辐射巡检机器人监督控制器。
- 判断：算。对象是真实核设施巡检机器人而不是单独的 costmap 算法；原文明确给出状态名、进入条件、事件集合、倒车距离规则和恢复路径。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要，`paper_content.txt` 第 59-75 行
> This paper presents an autonomous ground vehicle that can survey nuclear facilities for alpha, beta and gamma radiation and generate radiation heatmaps. New methods for preventing the robot from spreading radioactive contamination using a state-machine and radiation costmaps are introduced. This is the first robot that can detect alpha and beta contamination and autonomously re-plan around the contamination without the wheels passing over the contaminated area.

#### 摘录 B

- 出处：第 7-8 页，Section `4.3.2 State machine`，`paper_content.txt` 第 485-515 行
> When CARMA II is started up it enters the waitingforcall state ... a ROS service call is used to trigger the servicecall event ... and then transitions to the movingtocurrentwaypoint state.
>
> While in this state, CARMA II continuously monitors for the events: Waypoint unreachable, low battery, waypoint reached, alpha or beta radiation above threshold ... If battery drops below a preset threshold, or the user triggers the gohomecall event the robot ... changes the current waypoint to the home location ... If the waypoint that has been met is the home waypoint, CARMA II transitions to the waitingforcall state.

#### 摘录 C

- 出处：第 8 页，Section `4.3.2 State machine`，`paper_content.txt` 第 516-540 行
> When the RadEye SX reports levels of alpha or beta radiation that is above a given threshold, the ... robot transitions to the reversing state. In this state, CARMA II will reverse a fixed distance and the radiation costmap will be automatically updated.
>
> ... the refresh interval of the sensor (ts): v < d/t m/s ... For a RadEye SX with an update rate of 1 Hz and forward velocity of 0.2 m/s, the robot should reverse at least ... 0.4 m ... this minimum distance is increased to 1.0 m in this study.
>
> When the reversing motion is completed CARMA II exits the reversing state and transitions to the moving to waypoint state ... If the current waypoint has become blocked by radiation, the waypoint unreachable event will be triggered as soon as the robot re-enters the moving to waypoint state.

### 2. 基于原文整理后的自然语言描述

The CARMA II survey robot begins in `waitingforcall`, where it stays still while the operator defines the coverage region and then triggers a ROS `servicecall` that publishes the waypoint list and selects the first waypoint as the active goal. In `movingtocurrentwaypoint`, the robot drives with global and local planners over obstacle and radiation costmaps while continuously monitoring the events `Waypoint unreachable`, `low battery`, `waypoint reached`, and `alpha or beta radiation above threshold`. If a waypoint becomes unreachable, the supervisor skips to the next goal; if battery falls below the preset threshold or the operator issues `gohomecall`, the controller replaces the current goal with the home location, and reaching home returns the machine to `waitingforcall`. When alpha or beta readings exceed the configured threshold, the machine enters `reversing`, backs up by a distance computed from forward speed and sensor refresh interval, updates the radiation costmap, and then resumes motion toward the same waypoint or later forces a skip if the waypoint is now blocked. This yields a complete radiation-aware EFSM whose main control variables are the current waypoint, home flag, battery condition, and radiation-trigger outcome, while its local timing semantics come from the `1 Hz` sensor update rate and the minimum `1.0 m` reverse manoeuvre.

### 3. 逐句溯源

1. 句子 1：The CARMA II survey robot begins in `waitingforcall`, where it stays still while the operator defines the coverage region and then triggers a ROS `servicecall` that publishes the waypoint list and selects the first waypoint as the active goal.
   对应摘录：B
2. 句子 2：In `movingtocurrentwaypoint`, the robot drives with global and local planners over obstacle and radiation costmaps while continuously monitoring the events `Waypoint unreachable`, `low battery`, `waypoint reached`, and `alpha or beta radiation above threshold`.
   对应摘录：A, B
3. 句子 3：If a waypoint becomes unreachable, the supervisor skips to the next goal; if battery falls below the preset threshold or the operator issues `gohomecall`, the controller replaces the current goal with the home location, and reaching home returns the machine to `waitingforcall`.
   对应摘录：B
4. 句子 4：When alpha or beta readings exceed the configured threshold, the machine enters `reversing`, backs up by a distance computed from forward speed and sensor refresh interval, updates the radiation costmap, and then resumes motion toward the same waypoint or later forces a skip if the waypoint is now blocked.
   对应摘录：A, C
5. 句子 5：This yields a complete radiation-aware EFSM whose main control variables are the current waypoint, home flag, battery condition, and radiation-trigger outcome, while its local timing semantics come from the `1 Hz` sensor update rate and the minimum `1.0 m` reverse manoeuvre.
   对应摘录：A, B, C
