# Development of a Finite State Machine for a Small Unmanned Aircraft System Using Experimental Design - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 SUAS 跟踪地面车辆的自适应参数切换器明确写成 `36` 态 FSM，并给出状态生成规则与整张状态表，可直接作为“环境条件驱动参数切换”类航空航天样本。

## 条目 1: Wind-Maneuver Adaptive Tracking Parameter FSM

- 控制对象：航空航天与飞行控制领域的 SUAS 地面车辆跟踪参数切换控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 fixed-wing SUAS 跟踪地面车辆任务的条件自适应控制器，根据风向、风速和地面车辆机动类型切换 APM:Plane 的最优参数组合。
- 判断：算。对象是真实 SUAS autopilot 参数切换逻辑，而不是单纯实验设计方法；原文明确写出状态由哪些输入组合定义、状态数是多少、以及每个状态输出哪些控制参数设置。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6 页，Abstract，`paper_content.txt` 第 104-111 行
> Finite state machine (FSM) logic was developed to improve the APM:Plane software ... The FSM consists of 36 individual states defined by a combination of four wind directions, three wind speeds, and three ground maneuvers. Once the SUAS enters a particular state, the FSM modifies the default APM:Plane firmware parameter settings to optimal settings.

#### 摘录 B

- 出处：第 17 页，Section `1.6 Methodology Overview`，`paper_content.txt` 第 334-339 行
> Optimum autopilot parameter settings are estimated for each combination of wind speed, wind direction, and ground maneuver using statistical models. The estimated optimum parameters are organized into states. The states serve as the basis for a finite state machine (FSM) that is implemented using Python language scripts.

#### 摘录 C

- 出处：第 37 页，Section `3.8 Finite State Machine`，`paper_content.txt` 第 916-920 行
> With the models selected for each combination of the ground vehicle maneuver and wind direction, desirability functions ... find the settings that minimize the following distance variance for each combination of ground vehicle maneuver, wind direction, and wind speed. Each combination becomes a state in the FSM.

#### 摘录 D

- 出处：第 39 页，Table `13: States Table`，`paper_content.txt` 第 1155-1188 行
> Maneuver: Straight ... `3 knots / Headwind -> Max bank angle = 80`; `3 knots / Crosswind Right -> Waypoint radius = 40, Waypoint loiter radius = 30, Max bank angle = 70`. ... Maneuver: Turn ... `3 knots / Headwind -> Waypoint loiter radius = 70, Max bank angle = 65`; `7 knots / Tailwind -> Waypoint radius = 140, Waypoint loiter radius = 90, Max bank angle = 80`.

### 2. 基于原文整理后的自然语言描述

The controller models SUAS target tracking as a 36-state finite-state machine indexed by three input dimensions: ground maneuver, wind direction, and wind speed. For each combination, statistical experiments estimate an optimal set of APM:Plane parameters, and the FSM uses the current sensed conditions to switch the aircraft to the corresponding parameter state rather than keeping one fixed tuning for all situations. The state table shows that the outputs are not abstract labels only: each state writes concrete control settings such as `max bank angle`, `waypoint radius`, and `waypoint loiter radius`. For example, straight-flight headwind states keep `max bank angle = 80`, while straight crosswind states also set `waypoint radius = 40` and `waypoint loiter radius = 30`, with the bank angle reduced as wind speed increases. In turning states, the machine moves to wider loiter or waypoint radii, and the paper explicitly lists combinations such as `headwind turn -> loiter radius 70, max bank angle 65` and `7-knot tailwind turn -> waypoint radius 140, loiter radius 90, max bank angle 80`.

### 3. 逐句溯源

1. 句子 1：The controller models SUAS target tracking as a 36-state finite-state machine indexed by three input dimensions: ground maneuver, wind direction, and wind speed.
   对应摘录：A, C
2. 句子 2：For each combination, statistical experiments estimate an optimal set of APM:Plane parameters, and the FSM uses the current sensed conditions to switch the aircraft to the corresponding parameter state rather than keeping one fixed tuning for all situations.
   对应摘录：A, B, C
3. 句子 3：The state table shows that the outputs are not abstract labels only: each state writes concrete control settings such as `max bank angle`, `waypoint radius`, and `waypoint loiter radius`.
   对应摘录：D
4. 句子 4：For example, straight-flight headwind states keep `max bank angle = 80`, while straight crosswind states also set `waypoint radius = 40` and `waypoint loiter radius = 30`, with the bank angle reduced as wind speed increases.
   对应摘录：D
5. 句子 5：In turning states, the machine moves to wider loiter or waypoint radii, and the paper explicitly lists combinations such as `headwind turn -> loiter radius 70, max bank angle 65` and `7-knot tailwind turn -> waypoint radius 140, loiter radius 90, max bank angle 80`.
   对应摘录：D
