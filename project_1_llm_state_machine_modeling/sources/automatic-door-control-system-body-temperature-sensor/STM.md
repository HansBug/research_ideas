# Automatic Door Control System With Body Temperature Sensor - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把红外感知、体温判别、正常开门、异常告警和反转关门链写得很直接，能够稳定形成楼宇自动门方向的双 A `EFSM + T1` 样本。

## 条目 1: Temperature-Qualified Automatic Door Access Controller

- 控制对象：楼宇机电与门控领域的体温筛查自动门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向楼宇入口的自动门控制器，用红外传感器触发体温检测，再根据温度是否正常决定开门还是蜂鸣告警。
- 判断：算。对象是真实门控系统，原文明确给出了输入触发、阈值判别、开门输出、异常输出和几秒后反向关门的顺序链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`3.1 Prototype Overview`，`paper_content.txt` 第 137-148 行
> In use, when the Infrared Sensor detects an object such as a human hand, it will activate the MLX90614 Temperature Sensor. After that, the MLX90614 Temperature Sensor will read how high the temperature of the object is so that the results of these readings will be displayed on a 16x2 LCD screen. When the temperature read is a normal temperature between 36 – 37 °C it will activate the DC Motor which has been fitted with gear to rotate so that the door can open automatically and the LED will light up for a few seconds as a sign of safety. When the recorded temperature is not normal, the DC Motor will not be activated but the Buzzer and LED will sound and flash several times within a few seconds as a warning signal.

#### 摘录 B

- 出处：第 2 页，`3.2 Functions and How it Works`，`paper_content.txt` 第 166-182 行
> 1. Infrared sensor will detect objects (human hands). When the sensor reads an object, the infrared sensor will activate the MLX 90614 Temperature Sensor.
>
> 2. The MLX 90614 Temperature Sensor reads the object temperature and the temperature reading results will be displayed on a 16 x 2 LCD.
>
> 3. When the temperature is 37°C, the DC Motor is not active which causes the door to not open and the Buzzer will sound as a notification if the temperature exceeds the normal limit and the LED will flash in a few seconds.
>
> 4. When the temperature is normal, the LED will light up continuously for a few seconds. Not only that, the DC Motor will rotate so that the door will open within a few seconds after opening, the DC Motor will rotate in the opposite direction so that the door will close again.

### 2. 基于原文整理后的自然语言描述

The controller waits for the infrared sensor to detect a hand or other approaching object and uses that event to activate the `MLX90614` temperature sensor. It then reads and displays the measured temperature on the `16 x 2` LCD before choosing between two guarded branches. If the measured temperature is within the normal `36-37 °C` range, the PLC-side logic turns on the LED, drives the DC motor so the door opens automatically, and then reverses the motor after a few seconds so the door closes again. If the temperature is above the normal limit, the motor branch is blocked and the system instead keeps the door closed while the buzzer and LED flash as a warning for staff intervention.

### 3. 逐句溯源

1. 句子 1：The controller waits for the infrared sensor to detect a hand or other approaching object and uses that event to activate the `MLX90614` temperature sensor.
   对应摘录：A, B
2. 句子 2：It then reads and displays the measured temperature on the `16 x 2` LCD before choosing between two guarded branches.
   对应摘录：A, B
3. 句子 3：If the measured temperature is within the normal `36-37 °C` range, the PLC-side logic turns on the LED, drives the DC motor so the door opens automatically, and then reverses the motor after a few seconds so the door closes again.
   对应摘录：A, B
4. 句子 4：If the temperature is above the normal limit, the motor branch is blocked and the system instead keeps the door closed while the buzzer and LED flash as a warning for staff intervention.
   对应摘录：A, B
