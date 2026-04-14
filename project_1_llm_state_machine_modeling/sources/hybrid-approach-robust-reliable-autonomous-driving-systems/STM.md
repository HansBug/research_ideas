# Integrating Modular Pipelines with End-to-End Learning: A Hybrid Approach for Robust and Reliable Autonomous Driving Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动驾驶决策模块明确写成同步 `Moore` FSM，给出四个 driving states、二进制输入编码、`10 Hz` 运行频率以及输出到 `PID` 纵向控制器的速度参考，是一条完整的 `FSM + T1` 城市场景决策链。

## 条目 1: Four-State Urban Decision-Making Moore FSM
- 控制对象：汽车与道路车辆控制领域的城市场景驾驶决策 FSM
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个位于自动驾驶 modular pipeline 中的同步 `Moore` 决策状态机，用来在通行、跟车、红灯停车和停车牌停车之间切换目标速度控制策略。
- 判断：算。对象是论文主系统里的 decision-making module 而非附属示意；原文给出状态集合、输入编码、状态职责、`TTC` 制动逻辑、运行频率以及与 `PID` 纵向控制层的接口。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，Section `3.4. Decision Making`，行 387-418
> The decision-making module utilizes a synchronous Moore finite state machine (FSM) to orchestrate actions based on inputs from the collision risk assessment (CRA) module. ... The finite state machine (FSM) consists of four key states. ... Drive State (S1): No obstacles impede the vehicle's progress. ... Follow the Leader State (S2): The CRA reports an obstacle ... triggering dynamic speed adjustments. ... Red Light State (S3) and Stop Sign State (S4): These states mirror the "Follow the Leader" logic, utilizing TTC to achieve controlled stops ... The decision-making module employs a straightforward yet effective FSM structure for robust decision making. ... The FSM operates synchronously at 10 Hz, aligning with sensory data capture rates. ... The TTC formula is: TTC = Distance / Relative Velocity.

#### 摘录 B
- 出处：第 9 页，Section `3.5. Control`，行 420-428
> The control layer generates steering, throttle, and brake commands ... For longitudinal control, the decision-making module (FSM) calculates the desired agent's velocity, which is used to compute the final velocity. A proportional-integral-derivative (PID) controller then ensures the agent follows this desired reference.

#### 摘录 C
- 出处：第 27 页，Table `2. Finite state machine (FSM) inputs`，行 1330-1338
> Input Description
> 00 No obstacles detected, indicating a clear path ahead.
> 01 An obstacle is being tracked, requiring speed adjustments to maintain safe following distances.
> 10 A red traffic light is ahead, necessitating a controlled stop.
> 11 A stop sign is detected, also demanding a full stop.

### 2. 基于原文整理后的自然语言描述

The urban-driving decision module is a synchronous Moore FSM that maps the collision-risk-assessment output to four driving states: `Drive`, `Follow the Leader`, `Red Light`, and `Stop Sign`. Its input alphabet is explicitly encoded as `00` for clear path, `01` for tracked obstacle, `10` for red light, and `11` for stop sign, and the next state depends on the current input rather than on state history. Each state defines a concrete longitudinal behavior: `Drive` commands a nominal target speed, while the other three states use distance and time-to-collision information to reduce speed or achieve a controlled stop. The FSM runs synchronously at `10 Hz`, which gives the controller an explicit engineering-rate timing semantics rather than a purely untimed mode list. Its output is the desired vehicle velocity, which is then followed by a downstream PID longitudinal controller that converts the state-machine decision into throttle and brake actions.

### 3. 逐句溯源

1. 句子 1：The urban-driving decision module is a synchronous Moore FSM that maps the collision-risk-assessment output to four driving states: `Drive`, `Follow the Leader`, `Red Light`, and `Stop Sign`.
   对应摘录：A
2. 句子 2：Its input alphabet is explicitly encoded as `00` for clear path, `01` for tracked obstacle, `10` for red light, and `11` for stop sign, and the next state depends on the current input rather than on state history.
   对应摘录：A, C
3. 句子 3：Each state defines a concrete longitudinal behavior: `Drive` commands a nominal target speed, while the other three states use distance and time-to-collision information to reduce speed or achieve a controlled stop.
   对应摘录：A
4. 句子 4：The FSM runs synchronously at `10 Hz`, which gives the controller an explicit engineering-rate timing semantics rather than a purely untimed mode list.
   对应摘录：A
5. 句子 5：Its output is the desired vehicle velocity, which is then followed by a downstream PID longitudinal controller that converts the state-machine decision into throttle and brake actions.
   对应摘录：A, B
