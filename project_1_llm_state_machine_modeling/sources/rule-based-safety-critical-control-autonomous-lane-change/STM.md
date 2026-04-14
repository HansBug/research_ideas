# Rule-Based Safety-Critical Control Design using Control Barrier Functions with Application to Autonomous Lane Change - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把换道控制器写成显式 FSM，并把每个状态绑定到相应的 CLF-CBF-QP 安全控制律，同时给出了 `1.5 s` 完成判据和回退逻辑。

## 条目 1: Safety-Critical Lane-Change FSM with Return-to-Lane Recovery

- 控制对象：汽车与道路车辆领域的安全关键自动换道监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个自主车辆换道控制器，用高层命令、横向位置和交通安全判据驱动 `ACC / L or R / BL or BR` 四类状态，并在每个状态内选择不同的安全控制优化问题。
- 判断：算。对象是实际道路车辆换道监督器，原文明确给出了状态集合、输入信号、完成时长判据、威胁回退链以及状态与连续安全控制之间的对应关系。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Figure 2 / Section III-A Finite State Machine，行 272-298
> Fig. 2: Finite state machine of lane change controller. The command from behaviour planner ( c), current traffic environment ( e) and the ego vehicle’s positional information ( p) work as the input signals to this finite state machine and its output is the controller’s state.
>
> ... The proposed controller is a finite state machine (FSM), where rule-based CLF-CBF-QP formulations are used to calculate the system’s optimal input.
>
> Fig. 2 shows the proposed FSM. The FSM’s output is a state representing one of the following:
> Adaptive Cruise Control State -ACC: The ego vehicle maintains a desired speed and follows a leading vehicle in its current lane at a safe distance.
> Left or Right Lane Change State -L or R: The ego vehicle is expected to do a collision-free lane change maneuver to the left or right adjacent lane, respectively.
> Back to Current Lane From Left or Right State -BL or BR: The ego vehicle drives back to its current lane to avoid a potential crash if a threat arises during a lane change maneuver.

#### 摘录 B

- 出处：第 3-4 页，Section III-A Finite State Machine，行 302-342
> Command from High-Level Behaviour Planner ( c): This indicates the high-level planner’s expected maneuver for the ego vehicle. Value 0 will set the controller in ACC state; value 1 or -1 will make the controller work in L or R state, respectively.
>
> Positional Information - ( p): This represents the ego vehicle’s relative lateral position. Value 0 means the ego vehicle is in its current lane; if it moves across the edge between current and target lanes, p will change to 0.5; finally, when the ego vehicle is totally in its target lane for more than some duration of time, e.g. 1.5 s, p will become 1, which represents the success of a lane change maneuver and will bring the controller back to ACC state.
>
> Traffic Environment Information - ( e): This shows whether the ego vehicle can do a lane change maneuver under safety-critical constraints. When the CLF-CBF-QP formulation is in the L or R state and is numerically unsolvable due to a potential future collision, e will change from 1 to 0. When c is not 0 but e is 0, then if the FSM is in ACC state, it will continue working in this state; otherwise, as shown in Fig. 2, the FSM will go back to ACC state via BL or BR state.
>
> When c’s value is -1 or 1 but the ego vehicle is in ACC state, a predictive calculation ... will be made to determine if the ego vehicle can get enough space for a lane change maneuver after accelerating to the speed limit. When the result shows this is possible, the speed limit will be the desired speed for ACC state and the ego vehicle will re-enter L or R state once the lane change CLF-CBF-QP is solvable.
>
> These switches between different states implement the function of a planner in our proposed strategy. According to the input signals, the FSM will decide when is the best opportunity to do the lane change maneuver. Additionally, if this maneuver is interrupted, the FSM will drive the ego vehicle to change to its target lane again once it is safe.

### 2. 基于原文整理后的自然语言描述

The autonomous lane-change controller is an FSM whose states select different rule-based CLF-CBF-QP safety-control formulations according to the behaviour-planner command `c`, the lateral-position signal `p`, and the traffic-safety signal `e`. Its main states are `ACC`, which keeps the ego vehicle at a desired speed and safe following distance in the current lane, `L` or `R`, which execute a collision-free lane change to the adjacent lane, and `BL` or `BR`, which return the vehicle to the current lane when a threat appears during the maneuver. The command signal sets `ACC` when `c = 0` and requests left or right lane change when `c = 1` or `-1`, while the positional signal uses `p = 0` for the current lane, `p = 0.5` while crossing the lane boundary, and `p = 1` only after the vehicle has remained fully in the target lane for more than about `1.5 s`, at which point the controller returns to `ACC`. If the lane-change CLF-CBF-QP becomes unsolvable because of a potential future collision, `e` drops to `0`, an ongoing lane change is forced back through `BL` or `BR` to `ACC`, and the controller will attempt the commanded lane change again only after the predictive safety calculation shows that enough space is available.

### 3. 逐句溯源

1. 句子 1：The autonomous lane-change controller is an FSM whose states select different rule-based CLF-CBF-QP safety-control formulations according to the behaviour-planner command `c`, the lateral-position signal `p`, and the traffic-safety signal `e`.
   对应摘录：A, B
2. 句子 2：Its main states are `ACC`, which keeps the ego vehicle at a desired speed and safe following distance in the current lane, `L` or `R`, which execute a collision-free lane change to the adjacent lane, and `BL` or `BR`, which return the vehicle to the current lane when a threat appears during the maneuver.
   对应摘录：A
3. 句子 3：The command signal sets `ACC` when `c = 0` and requests left or right lane change when `c = 1` or `-1`, while the positional signal uses `p = 0` for the current lane, `p = 0.5` while crossing the lane boundary, and `p = 1` only after the vehicle has remained fully in the target lane for more than about `1.5 s`, at which point the controller returns to `ACC`.
   对应摘录：B
4. 句子 4：If the lane-change CLF-CBF-QP becomes unsolvable because of a potential future collision, `e` drops to `0`, an ongoing lane change is forced back through `BL` or `BR` to `ACC`, and the controller will attempt the commanded lane change again only after the predictive safety calculation shows that enough space is available.
   对应摘录：B
