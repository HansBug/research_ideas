# Flight Demonstrations of Unmanned Aerial Vehicle Swarming Concepts - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双 UAV 协同搜索/确认任务写成 mission-controller FSA，明确给出了车辆间请求、确认、返航与载荷动作分支，并用仿真、HIL 和飞行试验证明整套离散任务链可执行。

## 条目 1: Two-UAV cooperative mission controller

- 控制对象：双无人机协同搜索与目标确认任务的高层任务控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是无人机集群领域的双机协同任务控制器，用有限状态自动机驱动搜索、互相请求复核、确认目标、盘旋成像和返航链条。
- 判断：算。对象是真实飞行试验中的无人机任务控制软件，原文明确给出任务步骤、控制器职责、触发事件和验证过程，不是泛泛的 swarm 概念说明。

### 1. 原文摘录

#### 摘录 A

- 出处：Simple Teaming Approach，`paper_content.txt` 第 98-125 行
> a simple reference mission was developed: a team of two autonomous UAVs tasked to cooperate to search for, locate, and positively identify a target ... 1. Following launch and flyout, the vehicles begin a search ... 2. When one vehicle detects a tone, it localizes and records the location ... 3. The identifying UAV then requests the second UAV to break from its search pattern ... 4. if the second UAV indicates that the beacon is a decoy ... both UAVs return to their search patterns. 5. if the second UAV indicates that the beacon is the target ... one UAV loiters and captures images ... then both vehicles return home.

#### 摘录 B

- 出处：Mission Control Software，`paper_content.txt` 第 240-289 行
> The mission control software was responsible for five primary functions: (1) receiving mission definitions ... (2) receiving processed information from the sensors ... (3) exchanging messages with other vehicles and the ground station, (4) determining the necessary changes in the state of the vehicle, and (5) sending appropriate commands to the sensors and autopilot. ... mission specifications ... were represented as finite state automata (FSA). ... transitions are expressed in terms of events ... such as receiving communications from another team member, reaching a predetermined spatial location, detecting a vehicle health problem, sensing some phenomenon in the environment, or receiving a change of mission.

#### 摘录 C

- 出处：Reference Mission Demonstration Results，`paper_content.txt` 第 340-360 行
> Testing of the teaming concept consisted of software simulation, hardware-in-the-loop tests, and ultimately flight tests. ... These tests were accomplished to validate the FSAs and their implementation. ... With one airborne vehicle and one vehicle emulated on the ground, the teaming behaviors were demonstrated, and the reference mission was successfully accomplished. This included the correct identification of decoy beacons and cooperation of the two UAVs to identify the target beacon.

### 2. 基于原文整理后的自然语言描述

The reference swarm mission is encoded as a mission-controller FSA in which two autonomous UAVs start by searching a prescribed area and then reconfigure their behavior when one vehicle detects a candidate RF beacon. The first UAV localizes the beacon and requests the second UAV to leave its search pattern and fly to that location, after which the pair either resumes search if the second tone is absent or confirms the target, loiters for imagery, and returns home if both tones are present. At software level, the controller receives mission definitions, sensor products, vehicle and ground messages, and platform health data, and uses state transitions triggered by communications, waypoint arrival, environmental conditions, or vehicle parameters to issue commands to sensors and autopilot. The FSA was validated first in software simulation and HIL tests and then in a flight demonstration where one airborne UAV cooperated with a ground-emulated teammate to correctly reject decoys and identify the target beacon.

### 3. 逐句溯源

1. 句子 1：The reference swarm mission is encoded as a mission-controller FSA in which two autonomous UAVs start by searching a prescribed area and then reconfigure their behavior when one vehicle detects a candidate RF beacon.
   对应摘录：A, B
2. 句子 2：The first UAV localizes the beacon and requests the second UAV to leave its search pattern and fly to that location, after which the pair either resumes search if the second tone is absent or confirms the target, loiters for imagery, and returns home if both tones are present.
   对应摘录：A
3. 句子 3：At software level, the controller receives mission definitions, sensor products, vehicle and ground messages, and platform health data, and uses state transitions triggered by communications, waypoint arrival, environmental conditions, or vehicle parameters to issue commands to sensors and autopilot.
   对应摘录：B
4. 句子 4：The FSA was validated first in software simulation and HIL tests and then in a flight demonstration where one airborne UAV cooperated with a ground-emulated teammate to correctly reject decoys and identify the target beacon.
   对应摘录：C
