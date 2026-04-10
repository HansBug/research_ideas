# VLSI-Enabled Intelligent Parking Management System using Edge Artix-7 FPGA for Real-Time Automation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文围绕停车入口测距、车位占用、伺服道闸、LED 满位告警和超声测距 FSM 展开，原文可追溯细节足以形成双 A 停车控制子系统样本。

## 条目 1: Ultrasonic-Gated Slot-Monitoring Parking Controller

- 控制对象：智慧停车与车位管理领域的入口测距、道闸伺服与车位占用监测控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 Artix-7 FPGA 停车场控制器，用 HC-SR04 超声传感器检测入口车辆，用 IR 传感器监测车位，并用 PWM 驱动 SG90 伺服道闸和 LED 状态输出。
- 判断：算。虽然显式 FSM 主要写在超声测距子模块，但该子模块直接服务于入口道闸控制，且原文还给出车位、伺服、显示、满位、时序和测试链路，属于真实控制子系统。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 8-25 行
> This paper presents a VLSI-based Smart Car Parking System implemented on the Edge Artix-7 FPGA board, leveraging hardware parallelism for low-latency, energy-efficient automation. The system integrates ultrasonic (HC-SR04) and infrared sensors for vehicle detection and slot occupancy monitoring, respectively. Upon vehicle approach, the ultrasonic sensor triggers a servo motor (SG90) via pulse-width modulation (PWM) to control gate access, while IR sensors update slot status in real time, displayed via LED indicators. ... Hardware implementation demonstrates a gate response time of 0.5 seconds and 100% slot detection accuracy. ... validated through a four-slot prototype.

#### 摘录 B

- 出处：第 4 页，`3.2 Sensor Integration / 3.3 FPGA Control Logic / 3.4 Output Mechanisms`，`paper_content.txt` 第 138-155 行
> The system employs HC-SR04 ultrasonic sensors for vehicle detection at the entrance and IR sensors for slot occupancy monitoring. The ultrasonic sensor triggers a digital signal when a vehicle is within 30 cm, processed by the FPGA with a latency of 10 us. IR sensors detect vehicle presence with 98% accuracy.
>
> The control logic, implemented in Verilog HDL, manages sensor interfacing, PWM signal generation for servo motors, and LED updates.
>
> The SG90 servo motor, controlled via PWM, opens the gate within 0.5 seconds upon vehicle detection. LEDs indicate slot status (ON for occupied, OFF for available), with a "Parking Full" alert triggered when all slots are occupied.

#### 摘录 C

- 出处：第 4 页，`4.1 Design Flow / 4.2 Simulation and Verification`，`paper_content.txt` 第 163-178 行
> The system was divided into key modules: ultrasonic sensor controller, servo motor driver, IR sensor processor, and main integrator. Each module was coded to handle specific functions - e.g., the ultrasonic module uses a finite state machine (FSM) with states for triggering, echo measurement, and distance calculation, operating at a 50 MHz clock frequency to achieve precise timing. The servo module generates PWM signals with pulse widths of 50 us (0 degrees) and 75 us (90 degrees) for gate control, ensuring smooth operation. Integration was performed in the main module, where inputs from sensors (CLOCK_50, ECHO1/2, i1/2) are processed to drive outputs (TRIG1/2, servo_out1/2, led1/2).
>
> Waveforms were analyzed to confirm correct behavior, e.g., trigger pulses of 600 cycles and echo measurements up to 150,000 cycles to handle timeouts. ... This step ensured 100% coverage of edge cases, including full parking conditions and sensor failures.

#### 摘录 D

- 出处：第 6 页，`5.1 Testing Methodology / 5.2 Experimental Results`，`paper_content.txt` 第 216-229 行
> Functional testing involved scripted scenarios in ModelSim, such as vehicle entry (ultrasonic trigger), slot occupancy (IR activation), and full parking (LED alerts). Hardware testing used a four-slot prototype with physical vehicles (scaled models) to simulate urban parking environments.
>
> The system achieved a gate opening latency of 0.5 s, with ultrasonic detection accurate to within 5 cm at distances up to 4 m. IR sensors provided 100% occupancy detection accuracy in control LEDs lighting, with LEDs updating in under 10 ms. ... Simulation waveforms confirmed correct PWM and echo processing.

### 2. 基于原文整理后的自然语言描述

The FPGA parking controller watches the entrance with an HC-SR04 ultrasonic sensor and monitors slot occupancy with IR sensors, while driving an SG90 servo gate and LED slot indicators through Verilog logic on an Edge Artix-7 board. When a vehicle is detected within 30 cm at the entrance, the FPGA processes the digital detection with microsecond latency, drives PWM to open the servo gate within 0.5 s, and continues to update slot LEDs so that occupied slots are ON, available slots are OFF, and a parking-full alert is raised when every slot is occupied. Its ultrasonic controller is implemented as a timed FSM over trigger, echo-measurement, and distance-calculation states, running from a 50 MHz clock, producing trigger pulses of 600 cycles, handling echo measurements up to 150,000 cycles for timeout behavior, and exposing `TRIG`, `servo_out`, and LED outputs through the integrated module. The reported simulations and four-slot hardware tests cover vehicle entry, slot occupancy, full-parking conditions, sensor failures, and rapid inputs, confirming correct PWM/echo processing, 0.5 s gate response, sub-10 ms LED updates, and 100% slot detection in the prototype.

### 3. 逐句溯源

1. 句子 1：The FPGA parking controller watches the entrance with an HC-SR04 ultrasonic sensor and monitors slot occupancy with IR sensors, while driving an SG90 servo gate and LED slot indicators through Verilog logic on an Edge Artix-7 board.
   对应摘录：A, B
2. 句子 2：When a vehicle is detected within 30 cm at the entrance, the FPGA processes the digital detection with microsecond latency, drives PWM to open the servo gate within 0.5 s, and continues to update slot LEDs so that occupied slots are ON, available slots are OFF, and a parking-full alert is raised when every slot is occupied.
   对应摘录：B
3. 句子 3：Its ultrasonic controller is implemented as a timed FSM over trigger, echo-measurement, and distance-calculation states, running from a 50 MHz clock, producing trigger pulses of 600 cycles, handling echo measurements up to 150,000 cycles for timeout behavior, and exposing `TRIG`, `servo_out`, and LED outputs through the integrated module.
   对应摘录：C
4. 句子 4：The reported simulations and four-slot hardware tests cover vehicle entry, slot occupancy, full-parking conditions, sensor failures, and rapid inputs, confirming correct PWM/echo processing, 0.5 s gate response, sub-10 ms LED updates, and 100% slot detection in the prototype.
   对应摘录：C, D
