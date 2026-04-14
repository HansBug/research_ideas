# Proactive Robot Control for Collaborative Manipulation Using Human Intent - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把协作搬运中的角色协商控制器写成多层架构上的一组高层状态机，并给出计时阈值、冲突检测、`abort` 回退与软硬目标分支，是非常完整的人机共操监督样本。

## 条目 1: Goal-negotiation high-level controller

- 控制对象：协作搬运任务中基于人类意图识别的机器人高层角色协商控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是协作搬运人机交互中的高层监督器，用不同状态机来决定机器人是跟随、坚持自身目标、尝试让步，还是因冲突过强而中止。
- 判断：算。对象是实际机器人控制架构中的高层离散决策层，原文明确给出了多种状态机、定时阈值、冲突条件和异常回退，而不是只有模糊的 shared-control 描述。

### 1. 原文摘录

#### 摘录 A

- 出处：Architecture，`paper_content.txt` 第 155-166 行
> The proposed robot control architecture ... comprises three distinct layers ... The lower layer employs a Cartesian twist controller operating at a frequency of 500Hz. ... The HLC is a set of state machines responsible for imitating human behavior ... Each state machine is triggered according to a predefined robot goal and responds to human intent feedback.

#### 摘录 B

- 出处：High-Level Reasoning / KCG and Follower，`paper_content.txt` 第 209-234 行
> The high-level control module consists of three state machines ... Each state machine runs at 50Hz. ... KCG ... simply generates a static Fref towards gi and stops when the target is achieved ... it may terminate in two possible states: Nominal Termination and Forced Termination. ... The human intent perception block accumulates the output of the intent recognizer, and when the timer threshold is met it switches to KCG by selecting the most likely goal.

#### 摘录 C

- 出处：High-Level Reasoning / Hard Goal and Soft Goal，`paper_content.txt` 第 238-275 行
> In the hard goal mode, the robot prioritizes its own goal even though this creates a conflict. ... If a conflict is perceived ... the magnitude of Fref increases, otherwise decreases. ... If a human applies an excessive amount of force and overpowers the robot, the state machine transitions to the abort state ... The soft goal has an additional subtask Attempt Human Goal (AHG) ... if the robot misinterprets the human goal and spends too much time in the disagreement state, the robot switches to the Follower mode.

#### 摘录 D

- 出处：Results / Switching Frequency，`paper_content.txt` 第 478-495 行
> In the hard goal controller ... the average duration spent in agreement and disagreement states were 1.37s and 1.44s ... The average number of switches was 0.8. ... in the soft goal controller ... the average duration ... were 1.6s and 0.9s ... The average switching rate was 0.7 ... These results demonstrate the robustness of the proposed controller scheme against false transitions ... accurate tuning of timer thresholds ...

### 2. 基于原文整理后的自然语言描述

The controller uses a three-layer architecture in which a `500 Hz` Cartesian twist controller and an admittance layer are topped by a `50 Hz` high-level controller implemented as a family of state machines. The base `Known Common Goal` machine drives toward a shared goal and terminates either nominally or in a forced stop, while the `Follower` machine waits until an intent-recognition timer threshold is met and then switches into that known-goal routine. The `Hard Goal` machine instead increases or decreases reference force according to agreement or conflict with the human, and it transitions to an `abort` state if stretch force shows that the human has overpowered the robot. The `Soft Goal` machine adds an `Attempt Human Goal` branch that temporarily defers to the perceived human goal but falls back to `Follower` if disagreement lasts too long, and the reported `0.7-0.8` average switching counts show that the timer-guarded logic is stable rather than chattering.

### 3. 逐句溯源

1. 句子 1：The controller uses a three-layer architecture in which a `500 Hz` Cartesian twist controller and an admittance layer are topped by a `50 Hz` high-level controller implemented as a family of state machines.
   对应摘录：A, B
2. 句子 2：The base `Known Common Goal` machine drives toward a shared goal and terminates either nominally or in a forced stop, while the `Follower` machine waits until an intent-recognition timer threshold is met and then switches into that known-goal routine.
   对应摘录：B
3. 句子 3：The `Hard Goal` machine instead increases or decreases reference force according to agreement or conflict with the human, and it transitions to an `abort` state if stretch force shows that the human has overpowered the robot.
   对应摘录：C
4. 句子 4：The `Soft Goal` machine adds an `Attempt Human Goal` branch that temporarily defers to the perceived human goal but falls back to `Follower` if disagreement lasts too long, and the reported `0.7-0.8` average switching counts show that the timer-guarded logic is stable rather than chattering.
   对应摘录：C, D
