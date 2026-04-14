# Modeling and Synthesis of the Lane Change Function of an Autonomous Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动驾驶换道功能中的 `Lateral State Manager` 写成带 request、direction 和 timer 约束的 EFSM，并进一步给出可修复危险行为的 `outputupdate` 修正链，原文与可描述性都达到双 A。

## 条目 1: Request-Consistent Lateral State Manager for Lane Change

- 控制对象：汽车与道路车辆控制领域的自动驾驶车辆换道横向状态管理器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车辆换道模块中的 `Lateral State Manager (LSM)`，负责在每个 planner 更新周期内保持换道进度、检查左右变道请求，并在需要时修正 `direction` 与 `request` 的不一致。
- 判断：算。对象是实际道路车辆换道控制链的核心状态管理器，原文不仅明确给出请求信号、周期性 update 节拍、内部状态更新与 enter 动作，还给出 timer 与危险 mismatch 约束以及修复后的可控输出更新链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，`3. System Description and Modeling`，`paper_content.txt` 第 353-415 行
> This paper focuses on a part of the lane change module called the lateral state manager (LSM). ... Planner has the responsibility to decide in which lane to drive, and when. ... These are three valued signals that can take the values NoRequest, ChangeLeft, and ChangeRight.
>
> The LSM receives the lane change request signal and issues commands to the Path Planner to safely change lanes ... thus it is implemented as a state machine.
>
> The LSM code is called once every execution cycle, and it goes through three different stages during each call ... all of the inputs are updated ... code snippet associated to the current state is executed ... if a transition occurs, then the third stage executes specific code connected to entering a certain state.
>
> Modeling LSM's 223 lines of MATLAB-code in Supremica ... resulted in a single EFSM with 75 locations, 86 events, 123 transitions, and 17 variables.

#### 摘录 B

- 出处：第 5 页，`4. Specification`，`paper_content.txt` 第 433-454 行
> The property states that the LSM internal variable direction and the incoming request from Planner may not differ during more than one update event; when a lane change is performed, it needs to accord with the currently active request.
>
> If two consecutive updates occur where direction and request differs ... verification showed that this blocking state is indeed reachable from the initial state ... this faulty behavior was also present in the actual code and could lead to collision.

#### 摘录 C

- 出处：第 6-7 页，`5. Synthesis`，`paper_content.txt` 第 508-573 行
> The BDD-based synthesis ... produces a list of guards ... all concern the request input signal from the Planner and the internal variable direction.
>
> It is possible to add the plant shown in Fig. 4 to the model. Now, a supervisor has access to a controllable event, outputupdate, between e4 or e5 and update, where the supervisor has the possibility to choose the value of the variable direction.
>
> By changing the guards for the e4 and e5 events ... to request /= direction and request = direction, respectively, we can verify that the plant ... complies with the specification.

### 2. 基于原文整理后的自然语言描述

The lane-change function is centered on a cyclically updated `Lateral State Manager (LSM)` that receives `NoRequest`, `ChangeLeft`, or `ChangeRight` commands from `Planner` and keeps the vehicle's lane-change progress across update cycles. Each execution cycle first refreshes inputs, then runs the current state's internal update code, and finally executes one-shot entry code if a transition occurs, so the controller is explicitly organized as an update-driven EFSM rather than a loose maneuver description. In the published model, this behavior is compiled into a single EFSM with `75` locations, `123` transitions, and `17` variables, including the current location and the request/direction-related memory needed to track the maneuver. The safety requirement is that the internal `direction` variable may differ from the incoming `request` for at most one update, because otherwise the controller can continue a lane change on the wrong side and produce a collision-relevant mismatch. To repair that behavior, the model introduces a controllable `outputupdate` step between internal transitions and the next `update`, allowing the supervisor to rewrite `direction` or choose the correct guarded branch so the executed lane change remains consistent with the current request.

### 3. 逐句溯源

1. 句子 1：The lane-change function is centered on a cyclically updated `Lateral State Manager (LSM)` that receives `NoRequest`, `ChangeLeft`, or `ChangeRight` commands from `Planner` and keeps the vehicle's lane-change progress across update cycles.
   对应摘录：A
2. 句子 2：Each execution cycle first refreshes inputs, then runs the current state's internal update code, and finally executes one-shot entry code if a transition occurs, so the controller is explicitly organized as an update-driven EFSM rather than a loose maneuver description.
   对应摘录：A
3. 句子 3：In the published model, this behavior is compiled into a single EFSM with `75` locations, `123` transitions, and `17` variables, including the current location and the request/direction-related memory needed to track the maneuver.
   对应摘录：A
4. 句子 4：The safety requirement is that the internal `direction` variable may differ from the incoming `request` for at most one update, because otherwise the controller can continue a lane change on the wrong side and produce a collision-relevant mismatch.
   对应摘录：B
5. 句子 5：To repair that behavior, the model introduces a controllable `outputupdate` step between internal transitions and the next `update`, allowing the supervisor to rewrite `direction` or choose the correct guarded branch so the executed lane change remains consistent with the current request.
   对应摘录：C
