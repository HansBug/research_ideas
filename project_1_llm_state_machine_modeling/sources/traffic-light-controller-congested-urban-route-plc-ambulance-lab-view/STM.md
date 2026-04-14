# Traffic Light Controller for the Congested Urban Route using PLC and Ambulance Detection using RF Transmitter and Receiver with Lab VIEW - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口交通灯的密度感知延时和救护车 RF 抢占放到了同一条控制链里，明确给出了 `SL1.0-SL4.3` 传感器集和 `5/10/15/20 s` 绿灯延长规则，足以形成交通信号方向的双 A 条目。

## 条目 1: Density-and-Ambulance Priority Traffic Light Controller

- 控制对象：道路交通信号控制领域的密度自适应与救护车优先交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个四路口交通灯控制器，用 `PLC` 读取每条车道的四级传感器密度信号来延长绿灯时长，并在检测到救护车 `RF` 编码后沿其行进路径强制给绿灯优先。
- 判断：算。对象是实际路口信号控制系统，而不是只讲监测平台或通讯方案；原文明确写出车道传感器组、时间延长规则、救护车检测条件和抢占后输出变化，可以稳定整理成 EFSM。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract 与 Introduction，`paper_content.txt` 第 22-43、104-121 行
> In this paper an intelligent traffic control system using PLC is proposed. System measures the traffic density on each road by counting the number of vehicles and then takes the decision. Programming is done using ladder diagram ... this paper presents a simple ambulance controlled traffic system ... allowing an ambulance to arrive at a particular location without it having to stop anywhere until the destination is reached.
>
> There are 2 methods in controlling the traffic light system ... sequencing method ... and the demand based controller which response to the preprogrammed timer based on real time sensor detection ... Based on this detection, the programmable logic controller will trigger the traffic light indicators according to real demand.

#### 摘录 B

- 出处：第 3 页，`V. Proposed Methodology`，`paper_content.txt` 第 234-253 行
> The self-algorithm traffic light system is made up by combination of the sequencing programming method and the sensor based programming method in the PLC as the main controller.
>
> In each and every lane fours sensors are placed to detect the no of vehicles named as
> SENSOR SET 1: SL1.0, SL1.1, SL1.2 & SL1.3
> SENSOR SET 2: SL2.0, SL2.1, SL2.2 & SL2.3
> SENSOR SET 3: SL3.0, SL3.1, SL3.2 & SL3.3
> SENSOR SET 4: SL4.0, SL4.1, SL4.2 & SL4.3

#### 摘录 C

- 出处：第 4 页，密度控制测试条件，`paper_content.txt` 第 258-277 行
> The first condition is similar to conventional traffic light system which is when the SL1.0 is activated; the timing for the green color traffic light indicator in certain junction will turn on for a period of approximately 5 seconds.
>
> The second condition is when both SL1.0 and SL1.1 is activated ... green color traffic light indicator will be extended ... for approximately 10 seconds.
>
> The third condition is when both SL1.0, SL1.1 & SL1.2 is activated ... will be extended ... for approximately 15 seconds.
>
> Similarly the fourth condition is when SL1.0, SL1.1, SL1.2 & SL1.3 is activated ... will be extended ... for approximately 20 seconds.

#### 摘录 D

- 出处：第 3-6 页，救护车检测与仿真说明，`paper_content.txt` 第 214-231、278-300、333-336 行
> An RF Transmitter & Receiver module reads the respective decoder number from the corresponding ambulance RF transmitter encoder ... If the obtained Signals get matched with any of the Signal's, then a green indication is given along the path of the ambulance or else no change in the signal takes place.
>
> Firstly, whenever the ambulance arrives at particular junction, the ambulance driver has to show his corresponding lane ... This controller is capable of communicating with input and output modules ... If the obtained Signals get matched ... then a green indication is given along the path of the ambulance or else no change in the signal takes place.
>
> This system performs as a normal traffic system in the absence of ambulance. The operation gets altered whenever the ambulance arrives at a particular junction.

### 2. 基于原文整理后的自然语言描述

The proposed controller combines a preprogrammed traffic-light sequence with a PLC-based demand controller, so its behavior depends both on the current signal phase and on four-sensor traffic-density measurements collected from each lane set `SL1.0-SL1.3`, `SL2.0-SL2.3`, `SL3.0-SL3.3`, and `SL4.0-SL4.3`. For a congested lane, the controller increases the green interval stepwise: one active sensor yields about `5 s`, two active sensors yield about `10 s`, three active sensors yield about `15 s`, and four active sensors yield about `20 s` of green for that junction movement. In parallel, the ambulance-priority subsystem reads an RF code from the ambulance-side transmitter/encoder pair, compares it with the stored lane identifiers, and if the code matches it forces a green indication along the ambulance path instead of leaving the normal cycle unchanged. When no ambulance is detected, the installation behaves as the normal density-sensitive traffic controller and only the real-time sensor counts affect the signal timing.

### 3. 逐句溯源

1. 句子 1：The proposed controller combines a preprogrammed traffic-light sequence with a PLC-based demand controller, so its behavior depends both on the current signal phase and on four-sensor traffic-density measurements collected from each lane set `SL1.0-SL1.3`, `SL2.0-SL2.3`, `SL3.0-SL3.3`, and `SL4.0-SL4.3`.
   对应摘录：A, B
2. 句子 2：For a congested lane, the controller increases the green interval stepwise: one active sensor yields about `5 s`, two active sensors yield about `10 s`, three active sensors yield about `15 s`, and four active sensors yield about `20 s` of green for that junction movement.
   对应摘录：C
3. 句子 3：In parallel, the ambulance-priority subsystem reads an RF code from the ambulance-side transmitter/encoder pair, compares it with the stored lane identifiers, and if the code matches it forces a green indication along the ambulance path instead of leaving the normal cycle unchanged.
   对应摘录：D
4. 句子 4：When no ambulance is detected, the installation behaves as the normal density-sensitive traffic controller and only the real-time sensor counts affect the signal timing.
   对应摘录：A, D
