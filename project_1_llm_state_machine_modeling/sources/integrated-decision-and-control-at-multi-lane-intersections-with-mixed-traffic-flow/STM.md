# Integrated Decision and Control at Multi-Lane Intersections with Mixed Traffic Flow - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文在复杂路口混合交通场景下直接给出了黄灯/红灯/绿灯速度曲线切换 FSM，并把周边车辆、自行车、行人和停线约束并入状态设计，可作为车载决策控制双 A 样本。

## 条目 1: Traffic-Light-Aware Expected-Velocity Switching

- 控制对象：汽车与道路车辆领域的多车道路口信号感知式预期车速切换控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向多车道混合交通路口的自动驾驶决策控制器，用有限状态机在红、黄、绿灯之间切换期望通行/停车速度曲线，并把车辆、自行车、行人和停线约束一起纳入决策状态。
- 判断：算。对象是实际自动驾驶车辆的路口决策与控制子系统，原文明确给出交通灯 FSM、黄灯判断条件、状态输入组成以及红灯停线约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 40-45 行
> We first consider different velocity models for green and red lights in the training process and use a finite state machine to handle different modes of light transformation. Then we design different types of distance constraints for vehicles, traffic lights, pedestrians, bicycles respectively and formulize the constrained optimal control problems (OCPs) to be optimized.

#### 摘录 B

- 出处：第 2-3 页，`3.1 Static path planning`，`paper_content.txt` 第 215-235 行
> The traffic light system has three states, i.e., green, yellow and red lights ... the improved version of static path planning ... utilizes a finite state machine to deal with the different traffic signals.
>
> A represents current traffic light states, including green, yellow and red lights. Condition B indicates if A is the yellow light, whether the ego vehicle can stop in front of the stop line at the current position at a deceleration that does not affect the comfort.
>
> When the ego vehicle enters the intersection area, the expected velocity is selected according to the current signal light state. ... at the red light or green light, the ego vehicle just needs to select the corresponding speed curve ... As a warning signal, the yellow light allows the vehicle to choose to wait or drive according to the traffic in the intersection and vehicle states.

#### 摘录 C

- 出处：第 3 页，`3.2.1 Consideration of states`，`paper_content.txt` 第 266-283 行
> When the ego vehicle conducts different tasks, it needs to consider different surrounding traffic participants at the intersection ... vehicles, bicycles or pedestrians with potential conflicts according to different tasks.
>
> The state is designed to include information of the ego vehicle, surrounding traffic participants, static paths and traffic light state ... the traffic light state is also considered as the input, whose phases are represented by a number.

#### 摘录 D

- 出处：第 3 页，`3.2.2 Design of constraints`，`paper_content.txt` 第 298-307 行
> Instead of using virtual vehicles to simulate red light signals, we set constraints at the center of the stop line, which only works when the red light is on. ... we can define the safe distance ... to be kept from the surrounding traffic participants, road edge and stop line to ensure safety ...

### 2. 基于原文整理后的自然语言描述

The intersection controller is an EFSM that switches the ego vehicle between expected pass and expected stop velocity profiles according to the current traffic-light phase and the vehicle’s ability to stop safely. Its input state includes the ego vehicle, surrounding vehicles, bicycles, pedestrians, the candidate static paths, and the encoded traffic-light phase, so the signal state is not treated as an external annotation but as part of the decision state itself. Under green and red lights, the controller directly selects the corresponding pass or stop profile, while under yellow it evaluates whether the ego vehicle can still stop comfortably before the stop line and whether the intersection is crowded; this guard decides whether to continue through or fall back to the stopping curve. In addition, red-light handling is grounded by an explicit stop-line safety constraint rather than by a surrogate obstacle, and the same constrained decision layer also enforces distances to surrounding vehicles, bicycles, pedestrians, and road edges. The resulting control logic is a signal-aware velocity-switching machine embedded inside a larger mixed-traffic path-tracking controller.

### 3. 逐句溯源

1. 句子 1：The intersection controller is an EFSM that switches the ego vehicle between expected pass and expected stop velocity profiles according to the current traffic-light phase and the vehicle’s ability to stop safely.
   对应摘录：A, B
2. 句子 2：Its input state includes the ego vehicle, surrounding vehicles, bicycles, pedestrians, the candidate static paths, and the encoded traffic-light phase, so the signal state is not treated as an external annotation but as part of the decision state itself.
   对应摘录：C
3. 句子 3：Under green and red lights, the controller directly selects the corresponding pass or stop profile, while under yellow it evaluates whether the ego vehicle can still stop comfortably before the stop line and whether the intersection is crowded; this guard decides whether to continue through or fall back to the stopping curve.
   对应摘录：B
4. 句子 4：In addition, red-light handling is grounded by an explicit stop-line safety constraint rather than by a surrogate obstacle, and the same constrained decision layer also enforces distances to surrounding vehicles, bicycles, pedestrians, and road edges.
   对应摘录：A, C, D
5. 句子 5：The resulting control logic is a signal-aware velocity-switching machine embedded inside a larger mixed-traffic path-tracking controller.
   对应摘录：A, B, C, D
