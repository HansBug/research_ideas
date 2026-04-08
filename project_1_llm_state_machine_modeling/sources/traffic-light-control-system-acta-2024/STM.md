# Traffic Light Control System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向车流感知、跳过空方向、定时相位衔接和行人请求放行逻辑都写到了 PLC 程序层，可直接整理为双 A 的交通灯控制样本。

## 条目 1: Sensor-Gated Four-Way Traffic and Pedestrian Cycle

- 控制对象：道路交通信号领域的 PLC 四向路口交通灯与行人过街控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个两向交叉口的交通灯控制器，用车辆检测传感器、多个定时器和行人请求计数来组织 `north → south → east → west` 的跳相放行与行人过街。
- 判断：算。对象是实际路口信号控制系统，原文直接给出各方向绿灯的启停条件、定时器依赖、空方向跳过逻辑和行人请求分支，不是泛化的优化框架说明。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Introduction`，`paper_content.txt` 第 13-17 行、第 36-45 行
> sensors are used to detect the presence of vehicle at every route, if the presence of vehicle is not detected then the route is omitted form the operation of that cycle. The program also guides a safe context for the pedestrian crossing.
>
> The green light activates only in one path at a time and after a certain interval it should get deactivated, and the green light of the next path should be turned on. ... So, the pedestrian can only use the cross walk when every of the traffic signal for the vehicles is turned to red and only when two of the four pedestrian request switches are pressed.

#### 摘录 B

- 出处：第 3-4 页，`North green`，`paper_content.txt` 第 199-232 行
> North green ... it’s a mandatory condition that operator should be enabled and there should be sensed input from the north vehicle sensor for the activation of north green. The activation of north green is skipped only if there is no detection of vehicle by north vehicle sensor in that path.
>
> The above condition not only activates the north green but also energises timer T1 ... The output of the timer T1 is used ... to activate the successor of north green, which can be either one of south green, east green or west green.
>
> north green should be deactivated by the timer T1 ... Or when, there is output signal form the counter (Q2.3), the output form counter is obtained only if two of the four pedestrian request switches are pressed.

#### 摘录 C

- 出处：第 4-6 页，`South green / East green / West green`，`paper_content.txt` 第 240-271 行、第 293-320 行、第 339-371 行
> South green is activated only when the flip-flop (Q0.1) is set ... detection of vehicle by the south vehicle sensor, the pedestrian crossing green should be disabled, and should achieve one of the following conditions: 1. When there is no vehicle sensed by north vehicle sensor ... 2. When the timer T1 energises.
>
> East green is activated when the flip-flop (Q0.2) archives the set condition ... 1. The set on-delay time of timer T2 ... 2. For the scenario where the activation of south green is omitted ... timer T1 ... 3. Or in the case where both north vehicle sensor and south vehicle sensor doesn’t detect vehicle.
>
> West green is activated ... when the flip-flop (Q0.3) is set ... detection of vehicle by the west vehicle sensor, operator to be enabled, the pedestrian crossing green to be disabled and when it meets one of the following conditions: 1. When the timer T3 is energised ... 2. When there is no presence of vehicle of detected by east vehicle sensor ... 3. When there is no presence of vehicles detected by both south vehicle sensor and east vehicle sensor ... 4. Or, when there is no presence of vehicle detected by north vehicle senor, south vehicle sensor and east vehicle.

#### 摘录 D

- 出处：第 6-7 页，`Pedestrian operator / Simulation Results and Discussion`，`paper_content.txt` 第 376-395 行、第 445-467 行
> the counter (C1) which plays key role to activate the green light for the pedestrian crossing green and it also energises the timer T9. The on-delay of the timer T9 is used to turn of the signal (Q1.7).
>
> The operator is reset ... after the on-delay from the timer T5 which energises when the green light for pedestrian crossing is activated. This ensures that programme doesn’t get the request signal the pedestrian more than once until the activation of green light for pedestrians to cross.
>
> When the programme is enabled and if there is no presence of vehicle in the traffic, then the pedestrian green at every four corners is enabled ... After a certain interval the green light is deactivated and activates the green for its successor ... The activation of green is skipped in the direction where no vehicles are present. When two of the four pedestrian crossing switches are pressed this turns on the pedestrian green after the end of the cycle.

### 2. 基于原文整理后的自然语言描述

The controller is a sensor-gated EFSM that sequences the four vehicle directions in the order `north → south → east → west`, but only activates a direction when the operator latch is enabled, the corresponding vehicle sensor detects presence, and the pedestrian-crossing green is inactive. `North green` starts the cycle, energizes `T1`, and hands control to `south`, `east`, or `west` depending on which downstream directions still have vehicles, while `south`, `east`, and `west` each use their own timer-driven successor logic so that empty directions are skipped rather than being served by a fixed full cycle. The same timer chain is also used for resets, so each phase can terminate either because its successor fires, because the operator is disabled, or because the current direction becomes the last active service in the cycle. In parallel, pedestrian requests are accumulated through the request switches and counter logic, and once two requests are present the controller completes the current vehicle phase, forces all vehicle directions to red, enables pedestrian green, and uses `T5` and `T9` to prevent repeated requests until the pedestrian crossing interval finishes. This yields a timed vehicle-phase controller with an explicit pedestrian branch, empty-approach skipping, and phase-to-phase handoff through named PLC timers.

### 3. 逐句溯源

1. 句子 1：The controller is a sensor-gated EFSM that sequences the four vehicle directions in the order `north → south → east → west`, but only activates a direction when the operator latch is enabled, the corresponding vehicle sensor detects presence, and the pedestrian-crossing green is inactive.
   对应摘录：A, B, C
2. 句子 2：`North green` starts the cycle, energizes `T1`, and hands control to `south`, `east`, or `west` depending on which downstream directions still have vehicles, while `south`, `east`, and `west` each use their own timer-driven successor logic so that empty directions are skipped rather than being served by a fixed full cycle.
   对应摘录：A, B, C
3. 句子 3：The same timer chain is also used for resets, so each phase can terminate either because its successor fires, because the operator is disabled, or because the current direction becomes the last active service in the cycle.
   对应摘录：B, C
4. 句子 4：In parallel, pedestrian requests are accumulated through the request switches and counter logic, and once two requests are present the controller completes the current vehicle phase, forces all vehicle directions to red, enables pedestrian green, and uses `T5` and `T9` to prevent repeated requests until the pedestrian crossing interval finishes.
   对应摘录：A, B, D
5. 句子 5：This yields a timed vehicle-phase controller with an explicit pedestrian branch, empty-approach skipping, and phase-to-phase handoff through named PLC timers.
   对应摘录：A, B, C, D
