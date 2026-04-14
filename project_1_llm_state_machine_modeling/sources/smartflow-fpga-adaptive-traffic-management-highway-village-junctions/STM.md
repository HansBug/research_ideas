# SmartFlow: FPGA-Based Adaptive Traffic Management for Enhanced Pedestrian Safety at Highway-Village Junctions - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 zebra-crossing 交通灯写成了“相位 FSM + 距离阈值违规检测 + 蜂鸣告警”的完整控制链，时间参数和阈值都足够明确，可直接入账为双 A 样本。

## 条目 1: Pedestrian-Zebra Violation-Aware Traffic Signal Controller
- 控制对象：面向 highway-village junction 与 zebra crossing 的 FPGA 自适应交通灯与违规告警控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 `FPGA + HC-SR04 + buzzer` 实现的交通灯控制器，在固定相位轮转上叠加红灯期近距离车辆入侵检测和蜂鸣告警，以保护 zebra crossing 行人安全。
- 判断：算。对象是明确的 traffic-management controller，不是单纯传感器实验；原文同时给出四个相位状态、`15/3/10/3 s` 配时、`20 cm` 违规阈值、`60 ms` 测距周期和 `1 kHz` 告警输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 11-22 行
> The system integrates ultrasonic sensors (HC-SR04), a Field-Programmable Gate Array (FPGA) programmed in Verilog HDL, and a buzzer to detect and deter traffic signal violations in real time. Ultrasonic sensors monitor vehicle proximity within 20 cm of zebra crossings during red light phases, transmitting data to the FPGA via GPIO pins. The FPGA processes these inputs using a finite state machine, controlling LED-based traffic signals (green: 15s, yellow: 3s, red: 10s) and triggering a 1 kHz buzzer alert upon detecting violations.

#### 摘录 B
- 出处：第 4-6 页，`Software Design / System Operation / Software Development`，`paper_content.txt` 第 167-183、239-254 行
> The system is implemented in Verilog HDL, comprising four key modules:
>
> tf3 Module: Implements a finite state machine (FSM) with four states (main green/cross red, main yellow/cross red, main red/cross green, main red/cross yellow), controlling signal timing (31 s cycle).
>
> sensor_controller Module: Manages ultrasonic sensors, triggering measurements every 60 ms ...
>
> The operational flow ensures real-time violation detection: Initialization ... Sensor Monitoring ... Violation Detection ... Alerting ... Continuous Operation ...
>
> The software was developed in Verilog HDL ... The tf3 Module uses a 50 MHz clock, divided to 1 Hz for timing ... The ultrasonic_sensor Module ... includes states for idle, trigger, echo measurement, and timeout (3 ms) ... sensor_controller ... comparing distances against a 20 cm threshold ... alarm Module ... activating the buzzer when the distance is below 20 cm during a red signal phase.

#### 摘录 C
- 出处：第 8-9 页，`Results / Conclusion`，`paper_content.txt` 第 307-318、369-376 行
> Detection Accuracy: The system achieved 98% accuracy, correctly identifying 49 out of 50 red signal violations.
>
> Response Time: The average response time was 12 ms from violation detection to buzzer activation ...
>
> False Positive Rate ... mitigated by adding a 10 ms debounce filter.
>
> The finite state machine-based control ensures precise signal timing (green: 15 s, yellow: 3 s, red: 10 s), while the buzzer’s 1 kHz alerts effectively notify pedestrians and drivers of violations.

### 2. 基于原文整理后的自然语言描述

The SmartFlow controller combines a four-phase traffic-signal FSM with a red-phase vehicle-intrusion detection branch for zebra-crossing protection. Its `tf3` phase machine rotates through `main green/cross red`, `main yellow/cross red`, `main red/cross green`, and `main red/cross yellow`, using a `31 s` overall cycle built from `15 s`, `3 s`, `10 s`, and `3 s` signal durations. In parallel, the sensor-control path triggers ultrasonic measurements every `60 ms`, computes vehicle distance, and treats any object within `20 cm` of the crossing during a red phase as a violation. When that guard is satisfied, the alarm branch raises a `1 kHz` buzzer alert while keeping the stop indication active; the reported implementation further adds a `10 ms` debounce filter to suppress spurious alerts and reaches `98%` violation-detection accuracy with `12 ms` response time. This makes the sample a strong `EFSM + T1` traffic controller because the nominal signal sequence and the safety override are both explicit in the paper.

### 3. 逐句溯源

1. 句子 1：The SmartFlow controller combines a four-phase traffic-signal FSM with a red-phase vehicle-intrusion detection branch for zebra-crossing protection.
   对应摘录：A, B
2. 句子 2：Its `tf3` phase machine rotates through `main green/cross red`, `main yellow/cross red`, `main red/cross green`, and `main red/cross yellow`, using a `31 s` overall cycle built from `15 s`, `3 s`, `10 s`, and `3 s` signal durations.
   对应摘录：B, C
3. 句子 3：In parallel, the sensor-control path triggers ultrasonic measurements every `60 ms`, computes vehicle distance, and treats any object within `20 cm` of the crossing during a red phase as a violation.
   对应摘录：A, B
4. 句子 4：When that guard is satisfied, the alarm branch raises a `1 kHz` buzzer alert while keeping the stop indication active; the reported implementation further adds a `10 ms` debounce filter to suppress spurious alerts and reaches `98%` violation-detection accuracy with `12 ms` response time.
   对应摘录：A, C
5. 句子 5：This makes the sample a strong `EFSM + T1` traffic controller because the nominal signal sequence and the safety override are both explicit in the paper.
   对应摘录：A, B, C
