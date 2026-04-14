# Visual Language State Machine Robot - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把基于视觉语言模型的移动机器人行为组织成 `Navigation / Follow / Notification + Remote control` 三模主状态机，并明确给出 `2 s / 10 s / 30 s / 1 s` 的局部时间约束。

## 条目 1: VLM-guided navigation-follow-remote supervisor

- 控制对象：通用控制与移动机器人领域的基于视觉语言模型的导航、跟随与远程接管监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把 VLM 感知结果变成 `Navigation`、`Follow` 和 `Notification + Remote control` 三种机器人工作模式的主状态机，且每个模式都绑定了明确的速度、定时和人工接管规则。
- 判断：算。对象是真实移动机器人行为控制器，原文既给出主状态图，也给出规则化决策算法、跟随子程序中的 `30 s` 计时器与 `tracking lost > 1 s` 退出条件，以及危险物触发的远程接管链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 27-36 行
> Our system leverages the VLM to interpret scenes, gestures, and hazards, dynamically adjusting behavior without per-task training. For navigation, the robot adapts its algorithm parameters based on scene understanding; for Human Robot Interaction (HRI), it interprets gestures to trigger behaviors like following; for safety, it recognizes hazards and either navigates more cautiously or hands control to a human operator. These behaviors are synchronized by a state-based controller informed by the VLM output.

#### 摘录 B

- 出处：第 3 页，Figure 3 / Section `3.1-3.2`，`paper_content.txt` 第 153-223 行
> Figure 3: State diagram. ... VLM perception within a hierarchical state machine for dynamic parameter adaptation based on real-time environmental context. ... In this state, the state machine sets maximum speed and inflation radius while the robot autonomously follows goals. In Follow and Remote states, the state machine directly controls velocity. ... if person close ∧ raising hand then state←FOLLOW ... if object ∈ Oh then state←REMOTE ... else state←NAVIGATION ... This ensures outputs are selected no more frequently than every 2 seconds and no less than every 10 seconds.

#### 摘录 C

- 出处：第 6 页，Algorithm 2，`paper_content.txt` 第 333-360 行
> if tracking activated then start timer T←30 s ... if tracking lost >1s or T expired then exit tracking ... if too close then stop robot ... else compute and send velocity commands

#### 摘录 D

- 出处：第 4-6 页，Section `3.5-3.6` 与 Experiments，`paper_content.txt` 第 259-278、392-398 行
> VLM-detected objects are validated by the state machine against a predefined list of hazards ... on a match, the Message module is invoked. ... The robot then halts and waits for the first user to establish a connection. ... The user then remotely controls the robot to move it away from the dangerous object. ... detecting a wet floor sign and switching to Remote mode.

### 2. 基于原文整理后的自然语言描述

The robot is governed by a hierarchical state machine whose master modes are `Navigation`, `Follow`, and `Notification + Remote control`, and a VLM-based decision layer maps parsed scene JSON into one of these modes. In `Navigation`, the controller adjusts maximum speed and inflation radius and lets the rover follow goals autonomously, while the `Follow` and `Remote` branches directly command robot velocity. The decision layer is temporally stabilized by a history buffer and majority voting so that state outputs are produced no more often than every `2 s` and no less often than every `10 s`. The `Follow` subroutine starts a `30 s` timer and exits if tracking is lost for more than `1 s` or the timer expires, while also stopping the robot if the person becomes too close. When a hazardous object such as a wet-floor sign or glass door is recognized, the supervisor triggers the notification module, halts the robot, and keeps it on the remote-assistance path until a user connects and manually guides the robot away from danger.

### 3. 逐句溯源

1. 句子 1：The robot is governed by a hierarchical state machine whose master modes are `Navigation`, `Follow`, and `Notification + Remote control`, and a VLM-based decision layer maps parsed scene JSON into one of these modes.
   对应摘录：A, B
2. 句子 2：In `Navigation`, the controller adjusts maximum speed and inflation radius and lets the rover follow goals autonomously, while the `Follow` and `Remote` branches directly command robot velocity.
   对应摘录：B
3. 句子 3：The decision layer is temporally stabilized by a history buffer and majority voting so that state outputs are produced no more often than every `2 s` and no less often than every `10 s`.
   对应摘录：B
4. 句子 4：The `Follow` subroutine starts a `30 s` timer and exits if tracking is lost for more than `1 s` or the timer expires, while also stopping the robot if the person becomes too close.
   对应摘录：C
5. 句子 5：When a hazardous object such as a wet-floor sign or glass door is recognized, the supervisor triggers the notification module, halts the robot, and keeps it on the remote-assistance path until a user connects and manually guides the robot away from danger.
   对应摘录：A, D
