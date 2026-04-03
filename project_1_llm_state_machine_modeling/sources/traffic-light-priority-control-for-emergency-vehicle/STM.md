# Traffic Light Priority Control For Emergency Vehicle - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了紧急车辆发送优先请求、控制器切换绿灯/红灯、车辆通过后恢复默认时序的控制链。

## 条目 1: Green-Corridor Priority Request
- 控制对象：道路交通信号领域的应急车辆优先信号控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G2 应急车辆交通灯优先）

### 0. 条目识别与判定
- 一句话说明：这是交叉口交通灯优先控制器，用于在救护车、消防车等紧急车辆接近时接收优先请求并为其创建绿波通行通道。
- 判断：算。对象是实际交通灯控制系统，原文包含触发条件、灯态调整和恢复正常序列的完整链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 20-31
> The system combines advanced communication and sensing technologies including GPS, RFID, and wireless data transmission with adaptive signal control mechanisms. As an emergency vehicle nears an intersection, it sends a priority request signal containing details such as its real-time location, travel direction, and estimated arrival time to the nearest traffic controller. The controller analyzes this data and immediately adjusts the signal cycle, providing a green light for the emergency vehicle while holding cross-traffic signals on red. Once the vehicle passes safely, the controller automatically restores the standard traffic sequence.

#### 摘录 B
- 出处：第 1-2 页，system objectives, 行 96-110
> When an emergency vehicle approaches an intersection, it transmits a signal or identification code that is received by the traffic control unit. The control unit processes this data to determine the vehicle’s direction, distance, and estimated time of arrival. Based on this information, the system dynamically changes the traffic light sequence to provide a green signal for the emergency vehicle’s direction and red signals for other lanes until the vehicle passes safely through the junction.

#### 摘录 C
- 出处：第 2-4 页，`III. EXISTING SYSTEM / IV. METHODOLOGY`，行 159-179, 249-269
> The priority control system detects the approach of an emergency vehicle and automatically adjusts the traffic light sequence to provide a clear passage.
> ...
> Each emergency vehicle ... is equipped with an RFID tag that emits a unique identification signal. When the
> vehicle approaches an intersection, the RFID reader installed at the traffic junction detects this tag and sends the
> corresponding data to the Arduino. Upon receiving the signal, the Arduino processes it and identifies the vehicle as an
> emergency vehicle that requires priority passage.
> ...
> The controller logic ensures that the lane in which the emergency vehicle is approaching turns green, while all other intersecting directions turn red ...
> ...
> The system uses RF modules (RF Transmitter and RF Receiver) for communication between the emergency vehicle
> and the traffic control unit ... the microcontroller executes a predefined algorithm that prioritizes the signal accordingly.
> ... Once the vehicle crosses the junction, the system reverts to the normal signal sequence.

### 2. 基于原文整理后的自然语言描述

When an emergency vehicle approaches an intersection, it sends a priority request or identification signal carrying its location, direction, distance, and estimated arrival time to the traffic controller. The implemented architecture can realize this detection through RFID or RF communication, where a transmitter on the emergency vehicle is received at the junction and the controller identifies the approaching vehicle as a priority vehicle. Once priority is confirmed, the controller executes the signal-selection algorithm so that the emergency vehicle’s approach turns green while all conflicting lanes remain red, thereby creating a clear path or green corridor through the intersection. After the emergency vehicle clears the junction, the system restores the standard traffic sequence.

### 3. 逐句溯源

1. 句子 1：When an emergency vehicle approaches an intersection, it sends a priority request or identification signal carrying its location, direction, distance, and estimated arrival time to the traffic controller.
   对应摘录：A, B
2. 句子 2：The implemented architecture can realize this detection through RFID or RF communication, where a transmitter on the emergency vehicle is received at the junction and the controller identifies the approaching vehicle as a priority vehicle.
   对应摘录：C
3. 句子 3：Once priority is confirmed, the controller executes the signal-selection algorithm so that the emergency vehicle’s approach turns green while all conflicting lanes remain red, thereby creating a clear path or green corridor through the intersection.
   对应摘录：A, B, C
4. 句子 4：After the emergency vehicle clears the junction, the system restores the standard traffic sequence.
   对应摘录：A, C
