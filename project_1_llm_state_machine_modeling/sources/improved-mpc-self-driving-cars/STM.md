# Improved MPC for trajectory planning of self-driving cars - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 lane-change / brake 决策层明确写成 FSM，状态节点、距离 guard 与 `δk / γk` 激活输出都能直接回溯到正文与 flowchart，可作为车辆监督控制的 `EFSM + T0` 样本。

## 条目 1: Brake-then-lane-change overtaking supervisor

- 控制对象：汽车与道路车辆控制领域的障碍避让与超车监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个位于 IMPC 上层的车辆决策监督器，它根据前车距离、左侧车道占用和前后安全距离，在正常行驶、制动跟随、执行换道和继续行驶之间切换，并输出 `δk` / `γk` 激活信号给 MPC。
- 判断：算。对象是实际自动驾驶决策层而不是单纯轨迹优化公式；原文明确写出 FSM 决策逻辑、场景条件和输出激活函数，且 Fig. 4 直接给出流程图。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 39-52 行
> To tackle the challenges associated with lane changes in diverse driving environments, this study introduces an Improved Model Predictive Control (IMPC) approach ... Subsequently, a Sigmoid function is utilized to restrict vehicle movements, while Finite State Machine (FSM) decision-making selects appropriate maneuvers in real time according to changing driving conditions. ... ensuring rapid acquisition of longitudinal and lateral accelerations for lane changes, braking, and overtaking maneuvers.

#### 摘录 B

- 出处：第 7-8 页，`Obstacle avoidance trajectory planning` 与 `FSM-based decision-making`，`paper_content.txt` 第 410-442 行
> The architecture comprises two layers: the decision-making and trajectory-planning layers. The decision layer determines lane changes or braking and formulates these tasks as MPC constraints. A Finite State Machine (FSM) triggers specific activation functions based on constraints to execute various driving maneuvers.
>
> ... once the vehicle reaches a safe distance from the preceding vehicle, it evaluates the availability of the left lane. If clear, the vehicle changes lanes; otherwise, it remains in its current lane. In case the front vehicle decelerates beyond a safe braking distance, the vehicle initiates braking until the left lane clears, then changes lanes, returning to its original lane after overtaking ...
>
> The FSM ( Fig 4 ) algorithm determines braking or overtaking actions based on surrounding information ... Depending on the scenario, it generates an appropriate activation function sent to the MPC ...
>
> Where δk represents the lane change activation function; the vehicle initiates a lane change when δk = 1. γk denotes the braking activation function; braking occurs when γk = 1.

#### 摘录 C

- 出处：第 9 页，Fig. 4 caption，`paper_content.txt` 第 473-477 行
> Fig4. FSM flowchart. Blue denotes the vehicle’s operational processes, while green represents the decision parameters.

### 2. 基于原文整理后的自然语言描述

The retained control object is the FSM-based decision layer that sits above the IMPC trajectory planner and decides when the ego vehicle should keep normal operation, brake behind a slower vehicle, execute a lane change, or continue driving after the maneuver. Its guards are extended state conditions rather than bare events: the controller checks whether the following distance to the preceding vehicle is insufficient, whether the adjacent lane is empty, and whether safe distances from the front and rear vehicles have been restored before permitting the next transition. When the left lane is clear, the supervisor raises the lane-change activation `δk = 1`; when the front vehicle decelerates too strongly and a safe braking distance is violated, it instead raises the braking activation `γk = 1` and keeps braking until the overtaking path becomes admissible. After overtaking, the controller does not terminate immediately but waits until the rear-side safety condition is satisfied before returning the vehicle to its original lane. The resulting state machine is discrete at the decision level but continuously coupled to the MPC layer, because its output activations directly reshape the longitudinal and lateral constraints used for motion generation.

### 3. 逐句溯源

1. 句子 1：The retained control object is the FSM-based decision layer that sits above the IMPC trajectory planner and decides when the ego vehicle should keep normal operation, brake behind a slower vehicle, execute a lane change, or continue driving after the maneuver.
   对应摘录：A, B, C
2. 句子 2：Its guards are extended state conditions rather than bare events: the controller checks whether the following distance to the preceding vehicle is insufficient, whether the adjacent lane is empty, and whether safe distances from the front and rear vehicles have been restored before permitting the next transition.
   对应摘录：B, C
3. 句子 3：When the left lane is clear, the supervisor raises the lane-change activation `δk = 1`; when the front vehicle decelerates too strongly and a safe braking distance is violated, it instead raises the braking activation `γk = 1` and keeps braking until the overtaking path becomes admissible.
   对应摘录：B
4. 句子 4：After overtaking, the controller does not terminate immediately but waits until the rear-side safety condition is satisfied before returning the vehicle to its original lane.
   对应摘录：B, C
5. 句子 5：The resulting state machine is discrete at the decision level but continuously coupled to the MPC layer, because its output activations directly reshape the longitudinal and lateral constraints used for motion generation.
   对应摘录：A, B
