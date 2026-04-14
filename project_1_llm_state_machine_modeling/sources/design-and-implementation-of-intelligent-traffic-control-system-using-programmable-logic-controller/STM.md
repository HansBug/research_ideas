# Design and Implementation of Intelligent Traffic Control System using Programmable Logic Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对 primary/open-loop 与 secondary/closed-loop 的切换、50m 上游传感器反馈、一次输出周期的覆盖规则和对向车道分组关系都有明确描述，适合直接入账。

## 条目 1: Primary Timing with One-Cycle Sensor Override
- 控制对象：四向环岛交通灯 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的四向路口控制器，用于在正常定时控制和基于拥堵反馈的优先控制之间切换。
- 判断：算。对象是实际交通灯控制系统，原文明确写出 primary/secondary control、传感器反馈和覆盖规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-5 页，Section 2.3.1 / 2.3.2，`paper_content.txt` 第 341-355 行
> The model developed for the road access is based on two control measures – open-loop control is under a normal condition where the lights are triggered to allow or stop access using a preset time while the closed-loop control energizes the system based on a monitored condition.
>
> An ultrasonic sensor has been utilized to give feedback to the input section of the PLC at the instance when vehicular density is increased or vehicular flow is lengthy and stalled. The ultrasonic sensor is placed by the side of the median strip 50m far from the roundabout. This is to enable effective monitoring and give sufficient dead time.

#### 摘录 B
- 出处：第 5 页，Section 2.5 Principles，`paper_content.txt` 第 390-400 行
> The conventional road traffic light system works relative to the principle of an open-loop system. The open-loop system which is also the primary control operates to time and is not capable of self-control which means it can’t derive the desired output relative to a feedback function. The secondary control parameter has been designed to run on the primary control so depending on the signal from the feedback system, it overrides the open-loop control and has the closed-loop control actuated for only one cycle of output. This will continue while allowing other tracks to continue in their normal states.

#### 摘录 C
- 出处：第 5-6 页，Section 2.6 / 3 Results and Discussion，`paper_content.txt` 第 404-421, 493-521 行
> The signal going through the output ports with the following addresses O:0/0, O:0/1, O:0/2 and O:0/3 controls the road traffic light indicator on each road track. While some of the input ports as well are terminated with the ultrasonic infrared sensor on each road track with port addresses I:0/0, I:0/1, I:0/2 and I:0/3 respectively. Output ports O:0/0 and O:0/1 will be controlled by the input port I:0/1 and the output ports O:0/2 and O:0/3 will be controlled by the input port O:0/2. The control program will be highly influenced with the aid of timer bits. ... For tracks A and B, their sensor switches are aligned with the I:0/1 address and tracks C and D are aligned with the I:0/2 address.
>
> When the device is energized from the start, the states of the sensors and the input ports where they are terminated are used to update the output ports on the PLC as it relates to the downloaded logic program stored in the memory section of the microprocessor. Then the system commences its default traffic operation by taking turns based on a preset time. This will continue until the level of any sensor switches to a high state and at once the road traffic lights on the road track with its sensor having a high state turns green and stays so until its preset duration has elapsed while the other road tracks stay low and eventually returns to normal state.
>
> Once there is a deviation from the setpoint i.e., the input sensor has now detected traffic congestion, the PLC processes the new input signal in its microprocessor and turns the colour of the congested lanes to green while the other less congested lanes will keep the red lights on until a set time has elapsed. This process has been programmed to continue as long as the lane remains congested.

### 2. 基于原文整理后的自然语言描述

At startup the PLC scans the ultrasonic sensor inputs, updates the corresponding output ports, and drives the four-road roundabout in a primary open-loop mode in which access is granted or stopped by preset timing. An ultrasonic sensor mounted about 50 m before the roundabout feeds the input section when density is increased or flow is stalled, and the secondary closed-loop controller is designed to run on top of the primary controller rather than replace it. When feedback becomes active, the secondary control overrides the open-loop program for one output cycle, turns the congested road track green for its preset duration, keeps the less congested tracks red or low, and then returns the system to the normal timed sequence. The implementation groups opposite tracks on shared sensor and output paths and uses timer bits to influence the control program.

### 3. 逐句溯源

1. 句子 1：At startup the PLC scans the ultrasonic sensor inputs, updates the corresponding output ports, and drives the four-road roundabout in a primary open-loop mode in which access is granted or stopped by preset timing.
   对应摘录：A, C
2. 句子 2：An ultrasonic sensor mounted about 50 m before the roundabout feeds the input section when density is increased or flow is stalled, and the secondary closed-loop controller is designed to run on top of the primary controller rather than replace it.
   对应摘录：A, B
3. 句子 3：When feedback becomes active, the secondary control overrides the open-loop program for one output cycle, turns the congested road track green for its preset duration, keeps the less congested tracks red or low, and then returns the system to the normal timed sequence.
   对应摘录：B, C
4. 句子 4：The implementation groups opposite tracks on shared sensor and output paths and uses timer bits to influence the control program.
   对应摘录：C
