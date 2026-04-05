# Research on driving behavior decision making system of autonomous driving vehicle based on benefit evaluation model - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动驾驶车辆的五种驾驶行为模式、输入事件集合、初始/终止状态与状态转移函数写成了完整的高层行为决策 FSM。

## 条目 1: Five-mode benefit-evaluated driving supervisor
- 控制对象：自动驾驶车辆的高层驾驶行为决策系统
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆控制领域的自动驾驶行为决策 supervisor，用有限状态机在自由行驶、跟车、换道、紧急制动和故障停车之间切换。
- 判断：算。对象是实际自动驾驶车辆的高层决策控制器，原文明确给出状态集合、输入事件、转移函数、初始状态、终止状态和各模式触发语义。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 23-30
> To design a decision making system for autonomous driving vehicles, firstly, based on the decomposition of human driver operation process, five basic driving behavior modes are constructed, a driving behavior decision making framework for autonomous driving vehicle based on finite state machine is proposed. Then, to achieve lane change decision making for autonomous driving vehicle, lane change behavior characteristics of human driver lane change maneuver are analyzed and extracted.

#### 摘录 B
- 出处：第 4-5 页，Section 2，对五种驾驶行为模式的定义，行 282-305
> five basic driving behavior modes are constructed for the automatic driving system mentioned in this paper.
> ...
> Free driving mode: The current lane conforms driving rules and no obstacles in the lane.
> Automatic car following mode: Autonomous driving vehicle follows front vehicle in current lane.
> Lane changing mode: In case of obstacles in current lane, low driving efficiency in current lane or the current lane does not conform to traffic rules, ego vehicle needs to change lane from current lane to adjacent lane.
> Automatic emergency braking mode: For emergency scenario in which lane changing obstacle avoidance could not be completed, autonomous vehicle enter automatic emergency braking mode.
> Failure parking mode: When automatic driving system encounters failure fault, autonomous driving vehicle pulled into the rightmost lane and stopped immediately.

#### 摘录 C
- 出处：第 6 页，Section 4，对 FSM 形式化定义的说明，行 433-455
> Driving behavior decision making model of autonomous driving vehicle could be expressed as:
>
> F=(Q,E,δ,q0,F)
>
> Where Q represents the set of all driving behaviors, E represents the set of all input events, δ represents state transition function, q0 represents the initial state, F represents the set of termination state.
> ...
> The initial state of the vehicle entering automatic driving mode is free driving. In termination state, the vehicle enters failure parking mode or exits automatic driving mode. State transition function represents the transfer rules between driving behaviors.

#### 摘录 D
- 出处：第 5-6 页，Section 3，对决策输入信息的说明，行 386-410
> Comprehensive scenario information is the basis for lane change decision making. The input information for lane change decision making consists traffic information, environment information and vehicular state information. All the processed information is input into lane change decision making module.
> ...
> Traffic information reflects the traffic rules and road information; environment information extracts real time location, velocity and other state information of obstacles; vehicular state information reflects the running state information of ego vehicle.

### 2. 基于原文整理后的自然语言描述

The autonomous-driving decision system is organized as a finite-state supervisor with five driving modes: free driving, automatic car following, lane changing, automatic emergency braking, and failure parking. It evaluates traffic information, environment information, and vehicular state information to determine which driving behavior should be active in the current scenario. The paper formalizes the controller as `F = (Q, E, δ, q0, F)`, where `Q` is the behavior set, `E` is the external input-event set, `δ` is the state transition function, the initial state `q0` is free driving, and termination occurs when the vehicle exits automatic driving or enters failure parking. Free driving is used when the lane is rule-conforming and obstacle-free, car following maintains safe headway to a front vehicle, lane changing is entered when the current lane is blocked, inefficient, or rule-incompatible, emergency braking handles cases where obstacle avoidance by lane change cannot be completed, and failure parking moves the vehicle to the rightmost lane and stops it immediately.

### 3. 逐句溯源

1. 句子 1：The autonomous-driving decision system is organized as a finite-state supervisor with five driving modes: free driving, automatic car following, lane changing, automatic emergency braking, and failure parking.
   对应摘录：A, B
2. 句子 2：It evaluates traffic information, environment information, and vehicular state information to determine which driving behavior should be active in the current scenario.
   对应摘录：D
3. 句子 3：The paper formalizes the controller as `F = (Q, E, δ, q0, F)`, where `Q` is the behavior set, `E` is the external input-event set, `δ` is the state transition function, the initial state `q0` is free driving, and termination occurs when the vehicle exits automatic driving or enters failure parking.
   对应摘录：C
4. 句子 4：Free driving is used when the lane is rule-conforming and obstacle-free, car following maintains safe headway to a front vehicle, lane changing is entered when the current lane is blocked, inefficient, or rule-incompatible, emergency braking handles cases where obstacle avoidance by lane change cannot be completed, and failure parking moves the vehicle to the rightmost lane and stops it immediately.
   对应摘录：B
