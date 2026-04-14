# Control and Monitor of Product Filling Automation System in PLC-Based Packaging Using HMI Omron NB7W-TW00B - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把“传送到位、落料计数、达到 HMI 设定值后放行下一包”的控制链写成了完整 PLC+HMI 灌装逻辑，并给出 I/O 地址、传感器行为和计数规则。

## 条目 1: HMI-configurable count-based product filling controller

- 控制对象：工业自动化与离散制造领域的可配置计数式产品灌装/包装控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个通过 HMI 设定目标计数、利用光电与电感传感器驱动输送带和落料电机的 PLC 包装灌装控制器。
- 判断：算。对象是实际产品灌装装置，原文按输入按钮、容器检测、钢球计数、输出电机和 HMI 计数设定给出了完整的离散动作链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 16-22 行
> This study aims to design and create an automation system for filling products into packaging. PLC CP1E-N30DR-A system can be controlled and monitored via Omron NB7W-TW00B HMI.
>
> The number of steel balls is set via HMI. The HMI screen display consists of inputs: Push Button Start, Push Button Stop, input the number of products in the packaging, packaging sensor, and steel ball sensor; outputs: conveyor and counter display.

#### 摘录 B

- 出处：第 1-2 页，`2. Device Design / 2.1 Work Description`，`paper_content.txt` 第 57-67、77-91 行
> Device controller using PLC Omron CP1E-N30DR-A. The input consists of a Push Button Start, a Push Button Stop, a photoelectric sensor to detect the presence of a container, and an inductive proximity sensor to see a steel ball. The system’s output consists of a conveyor motor and a steel ball reservoir motor.
>
> When the Push Button Start is pressed for a moment, the conveyor will run carrying the container/package. The conveyor will stop when the container/package is detected by a photoelectric sensor. The steel ball reservoir motor will rotate, dropping the steel balls into the box.
>
> When the inductive proximity has seen several steel balls according to the setting value counter entered in the HMI, the motor for the steel ball reservoir will stop. The container/package conveyor will run again, so the process repeats for the next container/package, and the process will stop when the stop button is pressed.

#### 摘录 C

- 出处：第 2 页，`2.2 PLC I/O addressing / 2.3 Time Chart / 2.4 Ladder Diagram`，`paper_content.txt` 第 98-140 行
> This system uses a programmable memory for internal storage of instructions that implement specific functions such as logic, sequencing, timing, counting.
>
> Input Address: `00.00` Push Button Start, `00.01` Push Button Stop, `00.02` Photoelectric sensor, `00.03` Proximity Inductive Sensor.
>
> Output Address: `100.00` Conveyor Motor, `100.01` Steel Ball reservoir Motor.
>
> Figure 4 shows a time sequence diagram of the system's work. Figure 5 shows the program control ladder diagram of the device.

#### 摘录 D

- 出处：第 3-5 页，传感器与 HMI 说明，`paper_content.txt` 第 160-200、289-327 行
> When the Photoelectric sensor detects the presence of packaging on the conveyor, input `00.02` PLC `1` is used to stop the conveyor.
>
> The Inductive Proximity Sensor detects steel balls that fall into the packaging. The change of the `00.03` PLC input from `0` to `1` is used as the pulse input, which is calculated by the counter.
>
> The HMI screen display consists of inputs: Push Button Start, Push Button Stop, input setting value counter/number of products loaded into the package, container/packaging sensors, and steel ball sensors; output in the form of a conveyor, a steel ball reservoir motor and a present value counter.
>
> Setting Value Counter is done before the system starts ... Enter the desired value counter setting, then press ENTER. After that, run the system by pressing the Push Button Start button.

### 2. 基于原文整理后的自然语言描述

The controller uses the Omron PLC and HMI together as an EFSM whose main data variable is the operator-configurable target count for the number of products to be loaded into each package. After the operator sets the desired counter value on the HMI and presses `Start`, the conveyor motor runs until the photoelectric sensor detects that a container is positioned under the steel-ball reservoir. At that point the conveyor stops, the reservoir motor turns on, and every steel ball detected by the inductive proximity sensor generates a pulse on input `00.03` that is accumulated by the counter. Once the accumulated count reaches the HMI setpoint, the reservoir motor stops and the conveyor resumes so the next package can enter the filling position. The interface is fully explicit in the paper because the authors provide the input and output addresses, the time chart, the ladder diagram, the sensor-trigger semantics, and the HMI rule for editing the counter before the cycle starts.

### 3. 逐句溯源

1. 句子 1：The controller uses the Omron PLC and HMI together as an EFSM whose main data variable is the operator-configurable target count for the number of products to be loaded into each package.
   对应摘录：A, D
2. 句子 2：After the operator sets the desired counter value on the HMI and presses `Start`, the conveyor motor runs until the photoelectric sensor detects that a container is positioned under the steel-ball reservoir.
   对应摘录：B, D
3. 句子 3：At that point the conveyor stops, the reservoir motor turns on, and every steel ball detected by the inductive proximity sensor generates a pulse on input `00.03` that is accumulated by the counter.
   对应摘录：B, D
4. 句子 4：Once the accumulated count reaches the HMI setpoint, the reservoir motor stops and the conveyor resumes so the next package can enter the filling position.
   对应摘录：B, D
5. 句子 5：The interface is fully explicit in the paper because the authors provide the input and output addresses, the time chart, the ladder diagram, the sensor-trigger semantics, and the HMI rule for editing the counter before the cycle starts.
   对应摘录：C, D
