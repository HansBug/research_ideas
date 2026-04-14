# A Sliding Mode Control Architecture for Autonomous Driving in Highway Scenarios Based on Quadratic Artificial Potential Fields - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高速公路自动驾驶的 lane keeping / lane change / ACC / velocity tracking 机动选择写成单一 FSM，并给出 `d0 + t_H v_x` 与固定 `t_LC` 机动时间等工程 guard。

## 条目 1: Highway maneuver FSM for overtaking, ACC, and lane keeping

- 控制对象：汽车与道路车辆控制领域的高速公路自动驾驶机动选择控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 SAE L3 高速公路场景的机动选择 FSM，用当前车道索引、前车速度、目标车道安全距离和固定机动时间来协调保持车道、左右换道、目标速度跟踪和 ACC。
- 判断：算。对象是实际自动驾驶行为逻辑，不是纯 SMC 理论；原文明确列出可选 driving tasks、lane-change guard、`d0 + t_H v_x` 安全距离、固定 `t_LC` 机动时间和状态切换实例。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`B. Behavioral Logic`，`paper_content.txt` 第 210-225 行
> A ﬁnite state machine (FSM) chooses the driving task based on the detected surrounding environment. In the highway scenario, the possible tasks are left or right lane change, lane keeping, target velocity tracking, and adapting cruise control (ACC). The outputs of the FSM are the target position (Xtarget,Ytarget) ... and the target velocity for the longitudinal controller.
>
> ... the FSM checks the presence of a slower vehicle ahead on the same lane. If a slower vehicle is present ... then the FSM evaluates if the left LC maneuver is suitable ... Otherwise ... a right LC maneuver is considered ... The LC maneuver can be performed if the target distance dtar = d0 + tHvx is kept from any vehicle on the target lane ... If no LC maneuver is planned, the FSM activates the LK.

#### 摘录 B

- 出处：第 4 页，lane-change generation，`paper_content.txt` 第 231-258 行
> the LC begins at tini. We freeze the current value l to design a smooth trajectory connecting the lane centers from l to ltar in a ﬁxed maneuver time tLC. Thus, for each sampling time tini ≤ t ≤ tini + tLC, the FSM computes dlane = ... where α = 1 or α = −1 if moving to the lane at the left or the right, respectively ...
>
> Together with the APF target position, the reference velocity vref is computed given the current lane l. The FSM considers three factors to compute vref: the user-selected velocity vmax, the comfort in terms of maximum lateral acceleration ay,max, and the ACC maneuver.

#### 摘录 C

- 出处：第 5-6 页，Simulation scenario and results，`paper_content.txt` 第 398-410 行
> The simulation is divided into three sequential sections to evaluate the considered maneuvers ... the ego vehicle encounters three slower vehicles ahead ... the ego can begin the overtaking maneuver by moving to the left lane. Ahead on the second lane, the ego vehicle ﬁnds a car traveling at 110 km/h ... Thus, the ego vehicle must activate the adaptive cruise control system till the car ahead ends the overtaking. ...
>
> At t = 18 s, the behavioral logic transitioned to state 1 (moving left), initiating the overtaking maneuver ... adaptive cruise control maneuver was completed at t = 29 s, maintaining a consistent safety distance of 57 meters ... The vehicle successfully completed the overtaking maneuver at t = 73 s when the safety conditions for rejoining the rightmost lane were met.

### 2. 基于原文整理后的自然语言描述

The autonomous-highway behavior supervisor is a single FSM that selects among lane keeping, left/right lane change, target-velocity tracking, and adaptive cruise control according to the current lane and the surrounding traffic. Its decision logic first evaluates the lane index, then checks whether a slower vehicle blocks the current lane, and only authorizes a lane change if the target lane preserves the safety condition `d_tar = d_0 + t_H v_x` with respect to surrounding vehicles. Once a lane-change maneuver is started at `t_ini`, the FSM freezes the current lane index and generates a smooth transition to the target-lane center over a fixed maneuver time `t_LC`; the same supervisor simultaneously computes the longitudinal reference velocity from `v_max`, comfort constraints on lateral acceleration, and the ACC requirement. The simulation narrative shows that this is not just a conceptual logic sketch: the controller enters `state 1 (moving left)` at `18 s`, completes the ACC phase at `29 s` while keeping a `57 m` safety distance, and returns to the rightmost lane after the overtaking sequence is safely completed at `73 s`. The discrete maneuver FSM is therefore tightly coupled to continuous APF-based path tracking and longitudinal control, but its state choice logic remains explicit enough to extract as a highway-driving STM sample.

### 3. 逐句溯源

1. 句子 1：The autonomous-highway behavior supervisor is a single FSM that selects among lane keeping, left/right lane change, target-velocity tracking, and adaptive cruise control according to the current lane and the surrounding traffic.
   对应摘录：A
2. 句子 2：Its decision logic first evaluates the lane index, then checks whether a slower vehicle blocks the current lane, and only authorizes a lane change if the target lane preserves the safety condition `d_tar = d_0 + t_H v_x` with respect to surrounding vehicles.
   对应摘录：A
3. 句子 3：Once a lane-change maneuver is started at `t_ini`, the FSM freezes the current lane index and generates a smooth transition to the target-lane center over a fixed maneuver time `t_LC`; the same supervisor simultaneously computes the longitudinal reference velocity from `v_max`, comfort constraints on lateral acceleration, and the ACC requirement.
   对应摘录：B
4. 句子 4：The simulation narrative shows that this is not just a conceptual logic sketch: the controller enters `state 1 (moving left)` at `18 s`, completes the ACC phase at `29 s` while keeping a `57 m` safety distance, and returns to the rightmost lane after the overtaking sequence is safely completed at `73 s`.
   对应摘录：C
5. 句子 5：The discrete maneuver FSM is therefore tightly coupled to continuous APF-based path tracking and longitudinal control, but its state choice logic remains explicit enough to extract as a highway-driving STM sample.
   对应摘录：A, B, C
