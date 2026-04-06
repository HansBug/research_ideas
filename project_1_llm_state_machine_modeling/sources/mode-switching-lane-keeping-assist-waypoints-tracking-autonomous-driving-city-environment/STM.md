# Mode Switching Control Using Lane Keeping Assist and Waypoints Tracking for Autonomous Driving in a City Environment - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市自动驾驶控制写成显式的 supervisory mode switching 链，清楚区分 `ASASC` 与 `MS-ABS`、LKA/waypoint 两个转向子模式、多级制动阶段以及 `trestart`/`0.1 s` 等工程时间条件，满足双 A。

## 条目 1: City-Driving Mode-Switching and Restart Supervisor
- 控制对象：汽车与道路车辆控制领域的城市自动驾驶模式切换与制动恢复监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个面向城市道路、路口与行人的自动驾驶高层监督器，用上层模式切换决定 `ASASC` 与 `MS-ABS`，并在下层用 LKA/waypoint 与多阶段制动/重启逻辑执行具体控制。
- 判断：算。对象是实际自动驾驶车辆的运行控制器，不是单纯算法流程；原文明确写出了模式、切换阈值、状态标志、时间门槛和仿真中的停止/恢复行为。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7 页，supervisory decision layer，`paper_content.txt` 第 255-291 行
> ... ASASC ... to drive on roads with junctions and only use LKA when it is safe ... brake using the Multi-Stage Autonomous Braking System (MS-ABS) ... restart when the traffic light is green or when the way is clear again ... thresholds specifying forward crossing/collision warning time ... the time gap ... and lane keeping thresholds ... if (Green light) ... call ... ASASC ... else if (amber or red traffic light) or (road user detected) call ... MS-ABS ... A finite state machine enables the car to start again when the light turns back to green ...

#### 摘录 B
- 出处：第 10-12 页，`MS-ABS`，`paper_content.txt` 第 500-595 行
> The traffic light signals are programmed as a periodic finite state machine sequence. ... Autonomous braking is implemented using a finite state machine to select realistic progressive deceleration stages in the range from 0 to 1g ... n=3 ... Each deceleration stage has an associated braking time ... There is an additional 0.1s detection time delay ... FCW status =1 or FSLCW=1 ... while i ≤ n ... Braking status = 1 ... if traffic light is green or ORU out of collision area for duration trestart ... Braking status = 0 ...

#### 摘录 C
- 出处：第 19-20 页，traffic-light simulation，`paper_content.txt` 第 818-837 行
> Initially, the traffic light is green ... The traffic light then switches to amber, then red. ... The traffic light is amber for 3 s before switching to red for 13 s, then amber and red for 2 s before turning back to green for 15 s ... Figure 11 shows that the vehicle stops at the correct ... position when the traffic light switches to red, then starts successfully again when the light switches back to green ... The vehicle automatically restarts when the pedestrian is no longer on a collision course.

### 2. 基于原文整理后的自然语言描述

The controller is organized as a supervisory mode-switching hierarchy that decides when the vehicle should run the steering-and-acceleration supervisor `ASASC` and when it should hand control to the multi-stage braking system `MS-ABS`. Inside `ASASC`, the steering logic itself has two submodes: lane-keeping MPC on main roads where LKA sensing is safe, and waypoint-tracking pure pursuit at junctions where lane-keeping sensors are considered risky. The switch to braking is driven by explicit status and threshold variables, including `FCW`, `FSLCW`, collision/stop-line warning times, headway thresholds, and lane-keeping thresholds; when braking is activated, the throttle controller is disabled and the vehicle enters a stop-start FSM. That braking FSM is not abstract: it uses a periodic traffic-light sequence, three deceleration stages, a `0.1 s` sensing delay, and a restart guard requiring either a green light or an ORU to stay outside the collision area for `trestart`. The simulation section then validates the control chain with an explicit `green -> amber (3 s) -> red (13 s) -> amber/red (2 s) -> green` sequence, showing that the vehicle stops at the signal line, restarts on green, stops again for a pedestrian, and restarts once the collision risk disappears.

### 3. 逐句溯源

1. 句子 1：The controller is organized as a supervisory mode-switching hierarchy that decides when the vehicle should run the steering-and-acceleration supervisor `ASASC` and when it should hand control to the multi-stage braking system `MS-ABS`.
   对应摘录：A
2. 句子 2：Inside `ASASC`, the steering logic itself has two submodes: lane-keeping MPC on main roads where LKA sensing is safe, and waypoint-tracking pure pursuit at junctions where lane-keeping sensors are considered risky.
   对应摘录：A
3. 句子 3：The switch to braking is driven by explicit status and threshold variables, including `FCW`, `FSLCW`, collision/stop-line warning times, headway thresholds, and lane-keeping thresholds; when braking is activated, the throttle controller is disabled and the vehicle enters a stop-start FSM.
   对应摘录：A, B
4. 句子 4：That braking FSM is not abstract: it uses a periodic traffic-light sequence, three deceleration stages, a `0.1 s` sensing delay, and a restart guard requiring either a green light or an ORU to stay outside the collision area for `trestart`.
   对应摘录：B
5. 句子 5：The simulation section then validates the control chain with an explicit `green -> amber (3 s) -> red (13 s) -> amber/red (2 s) -> green` sequence, showing that the vehicle stops at the signal line, restarts on green, stops again for a pedestrian, and restarts once the collision risk disappears.
   对应摘录：C
