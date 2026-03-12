# Methodology To Develop A Discrete-Event Supervisory Controller For An Autonomous Helicopter Flight - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚描述了 Bell 412 自主任务从起飞到着陆的监督控制分解，并明确了不安全状态与接管条件。

## 条目 1: Takeoff-on-route-landing supervisory flow for Bell 412 autonomy
- 控制对象：Bell 412 直升机自主飞行监督控制器

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
- 出处：第 10 页，Supervisor DEVS Model Development，行 362-390
> We developed a supervisory controller for the entire autonomous mission, from take-off to landing.
>
> Once the aircraft approaches the PLP, the LIDAR-based landing zone evaluation system will identify Landing Points (LPs) ... for how long LPs are sought after and which LPs are “accepted” will be the responsibility of the Supervisor. The Supervisor will also receive inputs from the FCC, mission manager, pilot, and aircraft, and will determine whether the FCC should be ordered to land the helicopter at the received LP location, or to hand control over to the pilot, if no suitable landing point is found.
>
> the Supervisor coupled model was decomposed into 3 sub-components Takeoff, On Route, and Landing.

### 2. 基于原文整理后的自然语言描述

The Bell 412 autonomous flight architecture uses mission planning to define the takeoff point, flight plan, speed, and altitude, and the Autonomy Core then carries out automatic takeoff, waypoint navigation, landing-zone evaluation, and autonomous landing. The supervisory controller is modeled as a discrete-event, state-based controller whose role is to keep the mission away from unacceptable states such as attempting to land without a suitable landing point. For the full mission, the supervisor is decomposed into Takeoff, On Route, and Landing components, and during the landing phase it decides whether to command landing at an accepted landing point or hand control back to the pilot.

### 3. 逐句溯源

1. 句子 1：The Bell 412 autonomous flight architecture uses mission planning to define the takeoff point, flight plan, speed, and altitude, and the Autonomy Core then carries out automatic takeoff, waypoint navigation, landing-zone evaluation, and autonomous landing.
   对应摘录：A
2. 句子 2：The supervisory controller is modeled as a discrete-event, state-based controller whose role is to keep the mission away from unacceptable states such as attempting to land without a suitable landing point.
   对应摘录：B
3. 句子 3：For the full mission, the supervisor is decomposed into Takeoff, On Route, and Landing components, and during the landing phase it decides whether to command landing at an accepted landing point or hand control back to the pilot.
   对应摘录：C
