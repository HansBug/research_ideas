# A RULE-BASED CONTROLLER SIMULATION FOR AN AUTONOMOUS PARALLEL PARKING OF A CAR-LIKE ROBOT USING LASER SENSORS - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把并联停车辅助写成显式五步有限自动机，停车位搜索、对位、倒车入位、反打方向和居中对齐都以双激光、里程计和几何阈值触发，足以形成 `🅿️` 方向的双 A 样本。

## 条目 1: Five-step laser-guided parallel parking automaton

- 控制对象：智慧停车领域的并联停车辅助控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据前后两组激光测距、里程计和转向半径计算结果来完成并联停车的五步自动机控制器。
- 判断：算。对象是实际停车动作控制器，原文不仅给了 `Searching Space / Positioning Vehicle / Entering in the Space / Positioning in the Space / Aligning in the Space / Stopped` 这条有限自动机流程，还给了各步触发用到的 `SF1 / SR1 / SR3 / SF3` 传感条件、里程计计数与几何半径判断。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> Based on the data of the front and rear laser sensors, the automatic mode of the simulation environment controls the vehicle by generating acceleration and steering commands. ... the simulations results have shown that a finite state automaton is capable of parallel parking the car, based on two sensors data.

#### 摘录 B

- 出处：第 6-7 页，`4. Rule-Based Controller`
> Despite the difficulties of young drivers, this maneuver is well-defined in 5 steps as shown at Fig. 7. ... Figure 7. Finite Automaton for parallel parking maneuvers.

#### 摘录 C

- 出处：第 7 页，`4. Rule-Based Controller`
> The first step is the search for a space large enough so the car can park. In this phase, its actions are a forward controlled speed and the verification of the SF1 sensor values. ... When that space is found, the second step is triggered. It acts on the vehicle to keep a forward speed until the SR1 detects the obstacle ... When that happens, the vehicle stops. Now the vehicle is fully positioned.

#### 摘录 D

- 出处：第 7-8 页，`4. Rule-Based Controller / Eq. (5)`
> Based on this, the radius R can be estimated as follows ... if R is smaller than Rmin performed by the vehicle, so it can not park ... These analyses have to be carried out before the vehicle starts the maneuver, so it can decide if it is allowed to get in the parking space or if it will search for another place to park.
>
> When the vehicle is allowed to start the maneuver, the steering wheel has to be completely turned towards the curb ... then the vehicle begins to slowly move backwards. ... the finite automaton goes to the fourth step in which the steering wheel is turned completely to the other side and keep the vehicle moving backwards until SR3 read a distance value equal or smaller than a safety distance s. Next, the steering wheel is aligned and the vehicle move forward until it reaches the center of the parking space, verified by the difference between the SF3 and SR3 sensors.

### 2. 基于原文整理后的自然语言描述

The parking assistant is implemented as a five-step rule-based automaton that first searches for a valid parking slot, then positions the vehicle, backs into the slot, counter-steers for the second arc, and finally aligns the car at the center of the space. Its decisions are driven by two laser sensors mounted at the front and rear of the vehicle, together with odometry and compass information, so the controller does not simply replay a fixed path but reacts to measured slot length and current vehicle geometry. Before reversing, it computes a turning radius `R` and checks that the slot is large enough and collision-free relative to `Rmin`, which makes the entry decision depend on explicit parking constraints instead of on a single heuristic flag. During the maneuver, the automaton uses conditions such as `SF1` for slot discovery, `SR1` for final positioning before the first reverse arc, `SR3 <= s` for the second reverse arc termination, and `SF3 - SR3` balance for centering. This yields a compact but fully traceable `EFSM + T0` parking controller with both geometric guards and discrete phase progression.

### 3. 逐句溯源

1. 句子 1：The parking assistant is implemented as a five-step rule-based automaton that first searches for a valid parking slot, then positions the vehicle, backs into the slot, counter-steers for the second arc, and finally aligns the car at the center of the space.
   对应摘录：A, B, C, D
2. 句子 2：Its decisions are driven by two laser sensors mounted at the front and rear of the vehicle, together with odometry and compass information, so the controller does not simply replay a fixed path but reacts to measured slot length and current vehicle geometry.
   对应摘录：A, C, D
3. 句子 3：Before reversing, it computes a turning radius `R` and checks that the slot is large enough and collision-free relative to `Rmin`, which makes the entry decision depend on explicit parking constraints instead of on a single heuristic flag.
   对应摘录：D
4. 句子 4：During the maneuver, the automaton uses conditions such as `SF1` for slot discovery, `SR1` for final positioning before the first reverse arc, `SR3 <= s` for the second reverse arc termination, and `SF3 - SR3` balance for centering.
   对应摘录：C, D
5. 句子 5：This yields a compact but fully traceable `EFSM + T0` parking controller with both geometric guards and discrete phase progression.
   对应摘录：A, B, D
