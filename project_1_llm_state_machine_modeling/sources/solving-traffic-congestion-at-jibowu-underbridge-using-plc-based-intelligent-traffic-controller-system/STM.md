# Solving Traffic Congestion at Jibowu Underbridge, Lagos Using PLC-Based Intelligent Traffic Controller System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对相对车道成对轮转、按传感器触发数调整绿灯时长、拥堵覆盖例外和应急车辆优先模式都有明确文字，可直接整理为交通灯控制样本。

## 条目 1: Timed Operation with Congestion and Emergency Override
- 控制对象：城市路口 PLC 智能交通灯控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的智能路口控制器，用于在正常定时控制、拥堵优先和应急车辆优先之间切换。
- 判断：算。对象是实际交通灯控制系统，原文明确给出了定时模式、传感器覆盖条件和应急车辆处理方式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 24-30 行
> The sensor is attached to monitor the congestion level in each lane, quickly assessing the number of vehicles in less than 2 seconds. Based on this information, a signal is sent to activate the Green light for the lane with the highest vehicle count, while signaling Red for the other lanes.
>
> This system effectively manages the presence of emergency vehicles by turning all signals red, except for one, when an emergency vehicle approaches.

#### 摘录 B
- 出处：第 7-8 页，Implementation / Result and Discussion，`paper_content.txt` 第 312-326, 329-380 行
> For each lane, two inductive sensors are installed, and the program will assess the sensor conditions to determine if they have been triggered or not. The ladder logic program utilizes the total number of triggered sensors to determine the appropriate timing for triggering ON the green LED. Once the green LED timing is completed, the yellow LED will then illuminate for 5 seconds, followed by the red LED. The traffic signal will then either wait or yield to vehicles on the other lanes based on the sensor conditions in those respective lanes. In the event that none of the lanes experience significant traffic congestion, the system will operate according to the predefined timer that has been programmed into the PLC.
>
> The traffic signal operation initiates with the red LEDs triggered ON for 1 minute on lane 1 and lane 3, while the green LED is triggered ON on lane 2 and lane 4. After 45 seconds from the start of the operation, the yellow indicator LED on lane 2 and lane 4 starts blinking. Subsequently, the operation proceeds with the red LEDs being triggered ON for 1 minute on lane 2 and lane 4, and the green LED is ON on Lane 1 and lane 3. Again, after 45 seconds from the start of the operation, the yellow indicator LEDs on lane 1 and lane 3 starts blinking. This sequence continues in a repeated manner unless any of the roads' sensors are overrides the timing sequence as a result of congestion.
>
> It should be noted that green LED on any congested lane will be triggered ON except if any of the following situations occur; i. All the lanes are congested. ii. Lane 1 and lane 2 or lane 4 are congested iii. Lane 3 and lane 2 or lane 4 are congested. In the event that the above cases occur, then the timing sequence will prevail over the sensor readings.
>
> If no vehicles are present on any of the lanes, the LEDs will transition from green to yellow within 2 seconds, and from yellow to red in an additional 2 seconds. This cycle continues sequentially, starting from lane 1, followed by lane 2, lane 3, and finally lane 4. If there are two vehicles on lane 1, the time taken for the green LED to change to yellow is 16 seconds, and the same principle applies to the other lanes.

### 2. 基于原文整理后的自然语言描述

Under normal operation, the controller alternates the two opposite-lane pairs: lane 2 and lane 4 are green while lane 1 and lane 3 stay red for one minute, and after 45 seconds the currently open pair starts yellow blinking before the opposite pair is released. Each lane has two inductive sensors, and the PLC uses the total number of triggered sensors to determine the green duration; after green expires, yellow stays on for 5 seconds before red, and if no lane is significantly congested the predefined timer sequence continues. When congestion is detected, the sensors can override the normal timing to clear the congested lane or lane pair, but the timer still prevails when all lanes are congested or when the congested combinations are `lane 1 + lane 2/4` or `lane 3 + lane 2/4`. In the no-vehicle case, the LEDs step from green to yellow in 2 seconds and from yellow to red in another 2 seconds sequentially from lane 1 to lane 4, while a lane with two detected vehicles gets a 16-second green-to-yellow interval on the same principle. The same controller also supports an emergency mode in which all signals turn red except the lane reserved for the approaching emergency vehicle.

### 3. 逐句溯源

1. 句子 1：Under normal operation, the controller alternates the two opposite-lane pairs: lane 2 and lane 4 are green while lane 1 and lane 3 stay red for one minute, and after 45 seconds the currently open pair starts yellow blinking before the opposite pair is released.
   对应摘录：B
2. 句子 2：Each lane has two inductive sensors, and the PLC uses the total number of triggered sensors to determine the green duration; after green expires, yellow stays on for 5 seconds before red, and if no lane is significantly congested the predefined timer sequence continues.
   对应摘录：A, B
3. 句子 3：When congestion is detected, the sensors can override the normal timing to clear the congested lane or lane pair, but the timer still prevails when all lanes are congested or when the congested combinations are `lane 1 + lane 2/4` or `lane 3 + lane 2/4`.
   对应摘录：B
4. 句子 4：In the no-vehicle case, the LEDs step from green to yellow in 2 seconds and from yellow to red in another 2 seconds sequentially from lane 1 to lane 4, while a lane with two detected vehicles gets a 16-second green-to-yellow interval on the same principle.
   对应摘录：B
5. 句子 5：The same controller also supports an emergency mode in which all signals turn red except the lane reserved for the approaching emergency vehicle.
   对应摘录：A
