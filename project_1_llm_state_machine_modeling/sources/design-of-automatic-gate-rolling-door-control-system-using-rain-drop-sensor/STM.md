# Design of Automatic Gate Rolling Door Control System Using Rain Drop Sensor - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出了滚动门在雨天、晴天、障碍物干预下的输入-输出逻辑，并给出了开门、关门与报警的工程延迟数据。

## 条目 1: Weather-and-obstacle rolling-door supervisor
- 控制对象：楼宇机电领域的自动 rolling door 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个仓库 rolling door 的自动控制器，使用雨滴传感器判断天气、红外传感器判断门下障碍，并驱动直流电机执行开门、关门或停门报警。
- 判断：算。对象是实际门控控制系统，原文明确给出了输入传感器、输出执行器、障碍停门规则以及开关门的工程延迟。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Figure 6 后的系统算法说明，行 222-254
> Based on Figure 6, a series of block diagrams consisting of input, process, and output is designed.
> ...
> Rain sensors and infrared sensors are used as a system input.
> ...
> Arduino controls the DC motor as a gate drive that automatically opens or closes according to sensor readings.
> ...
> When the rain sensor is active, when the weather is rainy, when the infrared sensor is not active, or when there are no obstacles, the DC motor is active to close the gate, along with the red LED that lights up and the I2C LCD.
> ...
> If the weather is bright or the rain sensor is dry again, then the DC motor is active to open the gate, the green LED lights up, and the information is displayed on the I2C LCD.
> ...
> if the two sensors are active simultaneously, namely the rain sensor and the infrared sensor (there is an obstacle), the DC motor stops or does not move. The alarm will sound until the infrared sensor does not detect any obstacles. The system returns to reading the condition of the rain sensor.

#### 摘录 B
- 出处：第 5-6 页，`Testing Delay Time on DC Motors / Infrared Sensor Accuracy Testing / Testing the Delay Time on the Buzzer Sounding`，行 367-479
> This test is carried out to determine the function of the DC motor and to determine the delay time of the DC motor rotating or moving.
> ...
> Table 3 calculates the delay time ... = 13.48/10 = 1.34 seconds.
> ...
> Table 4 ... = 9.86/10 = 0.98 seconds
> ...
> The sensor will activate and signal the system when an obstacle is in front of the infrared sensor at a predetermined distance.
> ...
> Test results in Table 5 ... = 8.66/10 = 0.86 seconds
> ...
> the delay time buzzer sounds as a warning sign of an alarm if someone crosses while the system operates with an average of 0.86 seconds.

#### 摘录 C
- 出处：第 6-7 页，`Overall System Testing`，行 490-540
> Table 6. Overall System Testing
> ...
> ON (Rain) / OFF -> ON (Down) / OFF / close / OK
> ON (sunny / dry) / OFF -> ON (Up) / OFF / open / OK
> ON (Rain) / ON -> OFF / ON Alarm / stop / OK
> ON (sunny / dry) / ON -> ON (Up) / OFF / open / OK
> OFF / OFF -> OFF / OFF / stop / OK
> ...
> The system works when the weather outside is rainy. Then the rain sensor or raindrop sensor detects rain and sends a signal to the system to be forwarded to the DC motor as the driving force to close the gate rolling door
> ...
> When the rain is over and the weather is sunny again ... it sends a signal to the system to be forwarded to the DC motor as the driving force to open the rolling door gate again
> ...
> if it is raining and the active infrared sensor detects an obstacle and the DC motor is not active or silent, the alarm will sound until the infrared sensor is free.

### 2. 基于原文整理后的自然语言描述

The rolling-door controller reads a raindrop sensor as its primary weather input and an infrared sensor as its obstacle guard, then drives a DC motor, LEDs, buzzer, and LCD according to the combined sensor condition. In rainy weather with no obstacle, it enters the closing branch and drives the motor downward so that the gate closes, whereas when the sensor becomes dry again it enters the opening branch and drives the motor upward so that the gate reopens. If rain and obstacle are detected at the same time, the controller inhibits motor movement, keeps the gate stopped, and sounds an alarm until the infrared sensor clears, after which it returns to the rain-sensing loop. The implementation is backed by measured engineering delays: the average rain-detection response is about `1.19 s`, the dry-detection response is about `0.92 s`, the closing motor delay is about `1.34 s`, the reopening delay is about `0.98 s`, and the buzzer warning delay is about `0.86 s`.

### 3. 逐句溯源

1. 句子 1：The rolling-door controller reads a raindrop sensor as its primary weather input and an infrared sensor as its obstacle guard, then drives a DC motor, LEDs, buzzer, and LCD according to the combined sensor condition.
   对应摘录：A, B
2. 句子 2：In rainy weather with no obstacle, it enters the closing branch and drives the motor downward so that the gate closes, whereas when the sensor becomes dry again it enters the opening branch and drives the motor upward so that the gate reopens.
   对应摘录：A, C
3. 句子 3：If rain and obstacle are detected at the same time, the controller inhibits motor movement, keeps the gate stopped, and sounds an alarm until the infrared sensor clears, after which it returns to the rain-sensing loop.
   对应摘录：A, C
4. 句子 4：The implementation is backed by measured engineering delays: the average rain-detection response is about `1.19 s`, the dry-detection response is about `0.92 s`, the closing motor delay is about `1.34 s`, the reopening delay is about `0.98 s`, and the buzzer warning delay is about `0.86 s`.
   对应摘录：B
