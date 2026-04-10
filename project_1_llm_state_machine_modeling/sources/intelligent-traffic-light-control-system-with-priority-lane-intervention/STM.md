# Intelligent Traffic Light Control System with Priority Lane Intervention - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟 / 协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口默认循环、`NS/FS` 密度延时和蓝牙人工接管统一写到同一个控制器里，正文足以支撑双 A 交通灯样本。

## 条目 1: Density-adaptive traffic phase controller with Bluetooth priority override

- 控制对象：道路交通信号控制领域的 `NS/FS` 密度感知与蓝牙优先接管交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `Arduino Mega + HC-05 Bluetooth + 8 个 IR 传感器 + ABC 手机应用` 的四车道路口交通灯控制器，用默认相位循环、密度延时和人工优先接管共同决定哪一车道获得绿灯。
- 判断：算。对象是实际交通灯控制系统，原文不但说明了传感器和蓝牙接管接口，还明确给出了 `NS/FS` 加时逻辑、人工按钮映射和系统在默认/干预两种模式间的切换条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 17-31 行
> This study aims to build an intelligent traffic light with a vehicle density sensor device and a smartphone application to increase the accuracy of light timing and parse traffic density. Furthermore, in an emergency, they can still overcome and accelerate the speed of passing vehicles by manually intervening with the traffic light through a smartphone application connected wirelessly to the traffic light. ... When NS detects a vehicle with a green light, it increases Y seconds from the default X seconds. If FS detects a vehicle with a green light, it increases by Z seconds. Settings with the ABC application can randomly turn on the green light in four lanes according to the will of the smartphone operator.

#### 摘录 B

- 出处：第 2 页，`Introduction`，`paper_content.txt` 第 150-176 行
> This paper presents the design and implementation of intelligent traffic light control that can reduce traffic jams by adjusting the length of time the traffic lights are on. The length of time the red and green lights is based on the level of traffic of passing vehicles. Furthermore, traffic control officers can adjust the traffic light manually if vehicles need to be prioritized to pass. ... the algorithm implemented in the Arduino IDE was developed to set the time interval for the traffic light based on the status of the IR sensor.

#### 摘录 C

- 出处：第 4-6 页，`Proposed Intelligent Traffic Light Control / Bluetooth Module / Arduino Bluetooth Control / System implementation`，`paper_content.txt` 第 423-444、589-612、616-631 行
> Figure 2 shows an intelligent traffic light model system using IR sensors to detect vehicles. Each lane is equipped with two IR sensors. Each of these IR sensors is defined as a near sensor (NS) and far sensor (FS) according to the sensor distance to the traffic light. ... The proposed system aims to optimize traffic light time intervals based on traffic flow density detected using IR sensors.
>
> The Bluetooth Module HC-05 ... functions to receive command signals from smartphones through the Arduino Bluetooth Control (ABC) application ... Using the features available in ABC, the smartphone will then send specific command signals to determine/control the lighting ...
>
> The system starts by initializing all the conditions of the sensors and LEDs. Next, the traffic light is given a default interval time to run the traffic light cycle. After the system runs with the default interval time, the system will read the condition whether there is intervention from the mobile device ... If there is intervention, the traffic light will work based on the instructions given by the mobile device. If there is no intervention, the system will read the condition of the density of vehicles ... If there is traffic congestion ... the system will give additional time on the path with the GREEN light signal ... The system will provide a default interval time if no traffic density is detected.

#### 摘录 D

- 出处：第 7-8 页，`ABC test / Traffic light test / Conclusion`，`paper_content.txt` 第 675-694、740-768、779-800 行
> Button A to turn on the green light in lane 1, button B to turn on the green light in lane 2, button C to turn on the green light in lane 3, and button D to turn on the green light in lane 4.
>
> if it detects a vehicle, the green light, which defaults to lit for X seconds, will be added for Y seconds so that the light turns on for XY seconds. Likewise, for FS, if it detects a vehicle, the green light that defaults to lit for X seconds will be added for Z seconds to turn the light to XZ seconds.
>
> The results showed that the green light setting, which rotates clockwise with each green light on each lane for X seconds, can work well. ... When the NS detects a vehicle, the green light will increase Y seconds from the default X seconds. Likewise, if the FS detects a vehicle, the green light will increase by Z seconds from the default X seconds. Likewise, the ABC application software settings can randomly turn on the green light in the four existing lanes.

### 2. 基于原文整理后的自然语言描述

The intersection controller starts with a default clockwise cycle that serves the four lanes in order, while continuously monitoring both the eight `IR` sensors and the smartphone-linked `ABC` control channel. Each lane has a near sensor `NS` and a far sensor `FS`, and when the currently green lane still contains traffic, the controller extends that green phase by `Y` seconds for `NS` detection or by `Z` seconds for `FS` detection beyond the default `X` seconds. If no operator intervention is present, the controller keeps using that density-adaptive rule to decide whether it should stay with the current green phase or return to the normal default interval. When an officer intervenes through the `HC-05` Bluetooth link, the smartphone sends a direct lane-selection command, and button `A/B/C/D` immediately forces the green light to lane `1/2/3/4` while the other lanes stay red. After the manual priority action or the density-based extension finishes, the system continues its ordinary traffic-light cycle and keeps re-evaluating sensors and mobile commands.

### 3. 逐句溯源

1. 句子 1：The intersection controller starts with a default clockwise cycle that serves the four lanes in order, while continuously monitoring both the eight `IR` sensors and the smartphone-linked `ABC` control channel.
   对应摘录：B, C, D
2. 句子 2：Each lane has a near sensor `NS` and a far sensor `FS`, and when the currently green lane still contains traffic, the controller extends that green phase by `Y` seconds for `NS` detection or by `Z` seconds for `FS` detection beyond the default `X` seconds.
   对应摘录：A, C, D
3. 句子 3：If no operator intervention is present, the controller keeps using that density-adaptive rule to decide whether it should stay with the current green phase or return to the normal default interval.
   对应摘录：B, C, D
4. 句子 4：When an officer intervenes through the `HC-05` Bluetooth link, the smartphone sends a direct lane-selection command, and button `A/B/C/D` immediately forces the green light to lane `1/2/3/4` while the other lanes stay red.
   对应摘录：A, C, D
5. 句子 5：After the manual priority action or the density-based extension finishes, the system continues its ordinary traffic-light cycle and keeps re-evaluating sensors and mobile commands.
   对应摘录：C, D
