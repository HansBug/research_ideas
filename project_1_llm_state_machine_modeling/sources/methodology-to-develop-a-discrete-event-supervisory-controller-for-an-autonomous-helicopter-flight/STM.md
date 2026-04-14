# Methodology To Develop A Discrete-Event Supervisory Controller For An Autonomous Helicopter Flight - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚描述了 Bell 412 自主任务从起飞到着陆的监督控制分解，并明确了不安全状态与接管条件。

## 条目 1: Takeoff-on-route-landing supervisory flow for Bell 412 autonomy
- 控制对象：Bell 412 直升机自主飞行监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空自主飞行控制领域的 supervisory controller for an autonomous helicopter，用于在任务规划、航路飞行和着陆阶段之间切换，并在找不到可接受落点时决定交还飞行员。
- 判断：算。对象是实际 rotorcraft autonomy supervisor，原文明确给出了起飞、航路、着陆三阶段分解，以及避免进入不安全状态的监督逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，对 CVLAD autonomy system 的说明，行 71-82
> The Mission Planning Software serves as the launchpad for setting up autonomous helicopter missions. It allows users to specify the take-off location, create flight plans, and define desired speeds and altitudes.
>
> The Autonomy Core encompasses a Flight Control Computer (FCC), a Mission Manager, and the Supervisory Controller. The FCC ... manages automatic take-offs, waypoint navigation, and other essential functions. ... Once the helicopter reaches the landing leg, the Landing Zone Evaluation module selects the safest landing location. Upon determining the most suitable spot, the Autonomy Core executes an autonomous landing.

#### 摘录 B
- 出处：第 4 页，对 DES supervisory control 的说明，行 128-145
> A discrete-event system (DES) is a discrete-state, event-driven system ...
>
> the control mechanism intends to prevent the system from entering an “unacceptable” state ... An example of an “unacceptable” state in the context of autonomous flight could be landing on an obstacle if a suitable landing location is not found, or running out of fuel while conducting an autonomous mission.
>
> when the system is complex ... we need a high-level controller to monitor the inner states of each component, derive its own state, and make decisions accordingly. Such a controller can be essentially represented using a state machine that depicts the desired system’s state-flow

#### 摘录 C
- 出处：第 10 页，Supervisor DEVS Model Development，对 full mission supervisor 的说明，行 362-390
> We developed a supervisory controller for the entire autonomous mission, from take-off to landing.
>
> Once the aircraft approaches the PLP, the LIDAR-based landing zone evaluation system will identify Landing Points (LPs) ... for how long LPs are sought after and which LPs are “accepted” will be the responsibility of the Supervisor. The Supervisor will also receive inputs from the FCC, mission manager, pilot, and aircraft, and will determine whether the FCC should be ordered to land the helicopter at the received LP location, or to hand control over to the pilot, if no suitable landing point is found.
>
> the Supervisor coupled model was decomposed into 3 sub-components Takeoff, On Route, and Landing.

#### 摘录 D
- 出处：第 11-12 页，Landing Point Manager Atomic Model，对 landing 子状态与两条 trajectory 的说明，行 443-493
> The atomic model uses thirteen states to represent this behavior: (1) IDLE, (2) WAIT_FOR_LANDING_PHASE, (3) REQUEST_STATE_PLP, (4) GET_STATE_PLP, (5) START_LZE_SCAN, (6) LZE_SCAN, (7) HANDOVER_CONTROL, (8) PILOT_CONTROL, (9) REQUEST_STATE_LP, (10) GET_STATE_LP, (11) NOTIFY_LP, (12) LP_APPROACH, (13) LP_ACCEPT_EXP.
>
> The first trajectory occurs when the PLP is achieved ... before an LP is received. After the PLP is achieved the Landing Point Manager will request the aircraft state ... request for the helicopter to be stabilized ... If an LP is not received during the scan of the landing zone, the model will hand over control of the aircraft to the pilot
>
> The second trajectory occurs when an LP is received ... before the PLP is achieved or if the landing zone evaluation successfully identifies an LP ... the model then requests the aircraft state and starts the LP_APPROACH timer ... If the received LP is valid ... the model sends a new LP output ... Once the LP_APPROACH timer expires, the system will transition to an end state ... and will not allow any further updates to the LP
>
> pilot can take control of the helicopter at any state

### 2. 基于原文整理后的自然语言描述

The Bell 412 supervisor is a discrete-event, state-based controller that monitors the FCC, mission manager, pilot, aircraft, and landing-zone-evaluation outputs so the mission does not enter unacceptable states such as attempting to land without a suitable landing point. At the top level it is decomposed into `Takeoff`, `On Route`, and `Landing`: `Takeoff` initializes the mission and checks autonomy readiness, `On Route` forwards mission items as waypoints are reached, and `Landing` handles the final phase from the planned landing point to either touchdown or pilot handover. Inside landing, the landing-point manager cycles through `IDLE`, `WAIT_FOR_LANDING_PHASE`, `REQUEST_STATE_PLP`, `GET_STATE_PLP`, `START_LZE_SCAN`, `LZE_SCAN`, `REQUEST_STATE_LP`, `GET_STATE_LP`, `NOTIFY_LP`, `LP_APPROACH`, `LP_ACCEPT_EXP`, `HANDOVER_CONTROL`, and `PILOT_CONTROL` depending on whether a valid landing point is found and whether the pilot takes over. If the aircraft reaches the PLP before any landing point is available, the supervisor requests aircraft state, asks for stabilization, starts the landing-zone scan, and hands control to the pilot if no suitable landing point is received. If a landing point is received before or during the scan, the supervisor requests aircraft state, starts an LP-acceptance timer, publishes each new valid landing point that is sufficiently separated from the previous one, and once the timer expires it stops accepting further LP updates. Pilot takeover is allowed from any state, and the supervisor arbitrates whether the FCC retains control to land or control is yielded back to the pilot.

### 3. 逐句溯源

1. 句子 1：The Bell 412 supervisor is a discrete-event, state-based controller that monitors the FCC, mission manager, pilot, aircraft, and landing-zone-evaluation outputs so the mission does not enter unacceptable states such as attempting to land without a suitable landing point.
   对应摘录：B, C
2. 句子 2：At the top level it is decomposed into `Takeoff`, `On Route`, and `Landing`: `Takeoff` initializes the mission and checks autonomy readiness, `On Route` forwards mission items as waypoints are reached, and `Landing` handles the final phase from the planned landing point to either touchdown or pilot handover.
   对应摘录：C
3. 句子 3：Inside landing, the landing-point manager cycles through `IDLE`, `WAIT_FOR_LANDING_PHASE`, `REQUEST_STATE_PLP`, `GET_STATE_PLP`, `START_LZE_SCAN`, `LZE_SCAN`, `REQUEST_STATE_LP`, `GET_STATE_LP`, `NOTIFY_LP`, `LP_APPROACH`, `LP_ACCEPT_EXP`, `HANDOVER_CONTROL`, and `PILOT_CONTROL` depending on whether a valid landing point is found and whether the pilot takes over.
   对应摘录：D
4. 句子 4：If the aircraft reaches the PLP before any landing point is available, the supervisor requests aircraft state, asks for stabilization, starts the landing-zone scan, and hands control to the pilot if no suitable landing point is received.
   对应摘录：C, D
5. 句子 5：If a landing point is received before or during the scan, the supervisor requests aircraft state, starts an LP-acceptance timer, publishes each new valid landing point that is sufficiently separated from the previous one, and once the timer expires it stops accepting further LP updates.
   对应摘录：D
6. 句子 6：Pilot takeover is allowed from any state, and the supervisor arbitrates whether the FCC retains control to land or control is yielded back to the pilot.
   对应摘录：A, C, D
