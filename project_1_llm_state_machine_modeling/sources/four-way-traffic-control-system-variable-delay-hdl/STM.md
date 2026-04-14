# A Four-Way Autometic Traffic Control System with Variable Delay Using HDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向路口控制器写成 `SIM / SGM / DCM / SCU` 协作的 FSM，并明确给出 `S1-S4` 相位表和 `10/8/6/4/2/1` 秒延时映射，属于典型的双 A 定时交通灯样本。

## 条目 1: Variable-Delay Four-Way Traffic-Signal Cycle Controller

- 控制对象：道路交通信号控制领域的四向路口可变时延交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向四向路口的 `HDL/FPGA` 交通灯控制器，用车流输入总线决定相位驻留时间，并按 `S1-S4` 四步序列输出红黄绿灯与左转灯。
- 判断：算。对象是实际路口控制器本体，原文给出模块划分、控制总线、定时表和相位表，不是单纯实验平台或显示电路。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 20-29 行
> In this paper, a low cost, real-time ... automatic traffic control system has been proposed and implemented for four way traffic and the delay between two states can be changed manually, depending upon the density of the traffic ... The complete architecture ... has been designed using Finite State Machine (FSM) based approach and it contains three different modules ... SIM, SGM and DCM.

#### 摘录 B

- 出处：第 2-3 页，Section 2.2 `Architecture of the Proposed Traffic Controller`，`paper_content.txt` 第 120-145 行
> The workflow of the proposed traffic controller is based on the initialization of the system followed by the signal generation and delay calculation ... the proposed traffic controller is divided into four different modules ... System Initialization Module (SIM), Signal Generation Module (SGM) and Delay Control Module (DCM). A System Control Unit (SCU) is also there ... SCU operates based on the FSM depicted in Fig-3.

#### 摘录 C

- 出处：第 3 页，Section 2.3 `Operation of the Proposed Traffic Controller`，`paper_content.txt` 第 176-240 行
> The DCM ... receives the TIB signal ... calculate the delay ... There is a delay chart given in Table-1 ... 1 -> 10, 2 -> 8, 3 -> 6, 4 -> 4, 5 -> 2, Greater than 5 -> 1.  
> The signal generation process works in four steps ... S1, S2, S3 and S4. The first state S1 enables the red signal for lane 1 and 3 and green signal for lane 2 and 4 ... S2 makes the yellow signal enabled for lane 2 and 4 ... S3 turns G on for lane 1 and 3 and asserts R for lane 2 and 4 ... in S4, Y becomes asserted for lane 1 and 3 ...  
> The delay value is assigned in between two states ... End of this delay time denotes a change in states.

### 2. 基于原文整理后的自然语言描述

The proposed controller is a four-way traffic-signal EFSM implemented on FPGA, where a supervisory control unit coordinates initialization, signal generation and delay calculation rather than running a fixed cyclic lamp loop. Its architecture is explicitly partitioned into `SIM`, `SGM`, `DCM` and `SCU`, and the `DCM` reads the `TIB` traffic-input bus to convert the observed vehicle density into a state dwell time of `10/8/6/4/2/1` seconds. The `SGM` then executes a four-step signal sequence `S1 -> S2 -> S3 -> S4`, alternating which lane pair receives green, which receives yellow, and when the left-turn green signal is suppressed. Because the state transition timing is determined by external traffic-count inputs and an explicit delay table, the controller is better modeled as a timed engineering EFSM rather than a pure fixed-period FSM.

### 3. 逐句溯源

1. 句子 1：The proposed controller is a four-way traffic-signal EFSM implemented on FPGA, where a supervisory control unit coordinates initialization, signal generation and delay calculation rather than running a fixed cyclic lamp loop.
   对应摘录：A, B
2. 句子 2：Its architecture is explicitly partitioned into `SIM`, `SGM`, `DCM` and `SCU`, and the `DCM` reads the `TIB` traffic-input bus to convert the observed vehicle density into a state dwell time of `10/8/6/4/2/1` seconds.
   对应摘录：B, C
3. 句子 3：The `SGM` then executes a four-step signal sequence `S1 -> S2 -> S3 -> S4`, alternating which lane pair receives green, which receives yellow, and when the left-turn green signal is suppressed.
   对应摘录：C
4. 句子 4：Because the state transition timing is determined by external traffic-count inputs and an explicit delay table, the controller is better modeled as a timed engineering EFSM rather than a pure fixed-period FSM.
   对应摘录：A, C
