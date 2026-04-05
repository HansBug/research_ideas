# Sistem Kontrol Robot Sepak Bola Beroda menggunakan Finite State Machine (FSM) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把轮式足球机器人从找球、对球、找门、对门到射门的任务链拆成明确状态，并给出了关键距离、角度和局部定时动作。

## 条目 1: Ball-Seek Straighten-Goal-Kick Soccer Robot FSM

- 控制对象：通用控制与机器人任务领域的轮式足球机器人任务控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 CMUCam5 视觉输入的轮式足球机器人任务 FSM，负责找球、校正姿态、找门、带球推进和射门。
- 判断：算。对象是真实机器人控制器，原文给出了显式状态名、距离/角度 guard、闭环 wander 机制和整套任务测试结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 23-31、39-45 行
> "wander"

- 证据说明：摘要直接把任务链概括为找球、对球、找门和射门，并给出相机检测范围 `20–60 cm` 与 `-40° 到 40°`。

#### 摘录 B

- 出处：第 6-7 页，`Gambar 6` 状态说明，`paper_content.txt` 第 220-264 行
> "jarak 10 cm"

- 证据说明：原文逐状态说明 `wander / scan ball / posisi bola / maju bola / luruskan bola / mencari gawang / maju ke gawang / posisi gawang / menendang` 及其切换条件，其中 ball distance、goal distance 与 robot angle 都被明确写出。

#### 摘录 C

- 出处：第 9-13 页，FSM tests，`paper_content.txt` 第 328-341、384-440、453-474 行
> "86%"

- 证据说明：测试部分说明 `wander 2 + wander 3` 构成闭环直到找到球，并报告五类任务场景的整体成功率与平均执行时间。

### 2. 基于原文整理后的自然语言描述

The wheeled soccer robot is controlled by a flat finite state machine that executes a fixed mission chain: scan or wander to find the ball, align the robot with the ball, search for the blue goal, align to the goal, move forward, and kick. Vision input from CMUCam5 is used within a calibrated operating envelope of `20–60 cm` distance and `-40°` to `40°` angle for ball detection. If the robot finishes a `360°` scan without finding the ball, it enters the wander logic, where `wander 2` and `wander 3` form a closed loop of rescanning, goal straightening, and short forward motion until the ball is found again. Once the ball is farther than `10 cm`, the robot stays in the move-to-ball branch; once the ball is within `10 cm`, it switches to goal-search, and when the goal distance reaches `20 cm` or less, the controller transitions to the kick state. The paper also states that the move-to-goal branch contains a forward action of about `1 second`, and the full mission controller reaches `86%` success with an average execution time of `29.24 seconds` over five scenario groups.

### 3. 逐句溯源

1. 句子 1：The wheeled soccer robot is controlled by a flat finite state machine that executes a fixed mission chain: scan or wander to find the ball, align the robot with the ball, search for the blue goal, align to the goal, move forward, and kick.
   对应摘录：A, B
2. 句子 2：Vision input from CMUCam5 is used within a calibrated operating envelope of `20–60 cm` distance and `-40°` to `40°` angle for ball detection.
   对应摘录：A
3. 句子 3：If the robot finishes a `360°` scan without finding the ball, it enters the wander logic, where `wander 2` and `wander 3` form a closed loop of rescanning, goal straightening, and short forward motion until the ball is found again.
   对应摘录：B, C
4. 句子 4：Once the ball is farther than `10 cm`, the robot stays in the move-to-ball branch; once the ball is within `10 cm`, it switches to goal-search, and when the goal distance reaches `20 cm` or less, the controller transitions to the kick state.
   对应摘录：B
5. 句子 5：The paper also states that the move-to-goal branch contains a forward action of about `1 second`, and the full mission controller reaches `86%` success with an average execution time of `29.24 seconds` over five scenario groups.
   对应摘录：B, C
