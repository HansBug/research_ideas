# Smart Traffic Light Control System using Ultrasonic Sensors and FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出超声测距 FSM 的状态、触发脉冲、Echo 等待、60 ms 周期、距离阈值和双车道绿/红灯分配，能够形成双 A 的自适应交通信号控制样本。

## 条目 1: Ultrasonic Density-Based Traffic Signal Controller

- 控制对象：道路交通信号控制领域的双车道超声密度感知 FPGA 交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 HC-SR04 超声传感器和 Edge Artix-7 FPGA 动态比较车道密度并切换绿/红灯输出的交通灯控制系统。
- 判断：算。原文给出了超声传感器 FSM、周期触发、Echo 超时、距离阈值、密度比较、灯色输出和测试结果，满足 `EFSM + T1` 的可追溯控制样本要求。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 15-27 行
> This paper unveils a Smart Traffic Light Control System that synergizes ultrasonic sensors with a field-programmable gate array (FPGA) platform, specifically the EDGE Artix-7, to orchestrate dynamic signal modulation predicated on real-time traffic density. Leveraging ultrasonic sensors' acoustic precision, the system quantifies vehicular proximity ... prioritizing green phases for high-density corridors. ... Experimental validation ... with sensors achieving a +/-3 mm precision within a 2-400 cm range and signal adjustments executed in under 60 ms, yielding a 30% reduction in simulated waiting times compared to legacy systems.

#### 摘录 B

- 出处：第 5 页，`3.5 Finite State Machine (FSM) / 3.6 Flowchart`，`paper_content.txt` 第 165-174 行
> The FSM for the ultrasonic sensor module (Figure 3) comprises five states:
>
> IDLE: Initializes trigger and counter to zero, waiting for a start signal.
>
> SEND_TRIGGER: Sends a 10 us trigger pulse (600 clock cycles at 50 MHz).
>
> MEASURE ECHO: Counts clock cycles until Echo goes low, calculating distance.
>
> DONE: Signals measurement completion and returns to IDLE.
>
> The system's operation is depicted in Figure 4. The process begins with initializing the FPGA and sensors, followed by periodic trigger pulses every 60 ms. Distance is calculated, compared across lanes, and used to control LED outputs for traffic signals. WAIT_ECO_START: Waits for the Echo pin to go high, with a 3 ms timeout.

#### 摘录 C

- 出处：第 7 页，`4.1 Verilog Modules / 4.2 Simulation`，`paper_content.txt` 第 194-207 行
> The ultrasonic sensor module generates a 10 us trigger pulse and measures echo duration to calculate distance, using a 50 MHz clock. The FSM transitions through IDLE, SEND TRIGGER, WAIT ECHO START, MEASURE ECHO, and DONE states, with a 3 ms timeout for robustness. The sensor controller module interfaces with a single HC-SR04 sensor, generating start pulses every 60 ms and driving four LEDs based on distance thresholds (10 cm, 15 cm, 20 cm, 30 cm). The dual ultrasonic module integrates two sensor controllers, comparing their LED outputs to determine lane density and control green/red LEDs accordingly.
>
> The dual ultrasonic module was simulated with varying lane density scenarios, ensuring correct green/red LED assignments. Simulation waveforms showed a 60 ms cycle time and <1 us latency in signal updates.

#### 摘录 D

- 出处：第 8 页，`5 TESTING AND RESULTS`，`paper_content.txt` 第 230-251 行
> Two HC-SR04 sensors were positioned to detect objects (representing vehicles) at varying distances, with the FPGA controlling LED outputs to simulate traffic signals.
>
> Traffic Flow Simulation: A two-lane setup was simulated, with objects moved to mimic different traffic densities scenarios. Waiting times were compared to a fixed-timer system (30 s green/red cycle).
>
> Response Time: The system processed sensor data and updated LEDs within 60 ms for dual-sensor inputs, ensuring real-time operation. Single-sensor tests showed a 20 us latency from echo detection to LED activation.
>
> Traffic Flow: In scenarios with unequal lane densities (e.g., five objects in Lane 1 vs. one in Lane 2), the system assigned green to Lane 1 and red to Lane 2 ... Equal density scenarios defaulted to a balanced 15 s cycle.

### 2. 基于原文整理后的自然语言描述

The traffic-light controller uses two HC-SR04 ultrasonic sensor channels on an Edge Artix-7 FPGA to measure lane proximity, estimate relative lane density, and drive traffic-signal LEDs. Each sensor channel runs a timed FSM with `IDLE`, `SEND_TRIGGER`, `WAIT_ECHO_START`, `MEASURE_ECHO`, and `DONE` states: it initializes the trigger and counter, sends a 10 us trigger pulse of 600 cycles at 50 MHz, waits up to 3 ms for Echo to begin, measures the echo duration to calculate distance, and returns to `IDLE` after signaling completion. A sensor controller repeats this measurement every 60 ms, maps distances to four proximity LEDs using 10 cm, 15 cm, 20 cm, and 30 cm thresholds, and the dual ultrasonic controller compares the two lanes' LED/density results to select which lane receives green and which receives red. In tests with unequal density, such as five objects on Lane 1 and one on Lane 2, the controller assigns green to the denser lane and red to the other lane; with equal density it falls back to a balanced 15 s cycle, while measured dual-sensor LED updates stay within 60 ms and single-sensor echo-to-LED latency is about 20 us.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller uses two HC-SR04 ultrasonic sensor channels on an Edge Artix-7 FPGA to measure lane proximity, estimate relative lane density, and drive traffic-signal LEDs.
   对应摘录：A, D
2. 句子 2：Each sensor channel runs a timed FSM with `IDLE`, `SEND_TRIGGER`, `WAIT_ECHO_START`, `MEASURE_ECHO`, and `DONE` states: it initializes the trigger and counter, sends a 10 us trigger pulse of 600 cycles at 50 MHz, waits up to 3 ms for Echo to begin, measures the echo duration to calculate distance, and returns to `IDLE` after signaling completion.
   对应摘录：B, C
3. 句子 3：A sensor controller repeats this measurement every 60 ms, maps distances to four proximity LEDs using 10 cm, 15 cm, 20 cm, and 30 cm thresholds, and the dual ultrasonic controller compares the two lanes' LED/density results to select which lane receives green and which receives red.
   对应摘录：B, C
4. 句子 4：In tests with unequal density, such as five objects on Lane 1 and one on Lane 2, the controller assigns green to the denser lane and red to the other lane; with equal density it falls back to a balanced 15 s cycle, while measured dual-sensor LED updates stay within 60 ms and single-sensor echo-to-LED latency is about 20 us.
   对应摘录：D
