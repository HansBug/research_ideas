# Controlling and Monitoring of Traffic Light Control Using Schneider PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对两路口交通灯的 north/east 双向相位循环、计时表、内存位和 ladder 映射讲得完整，可直接形成双 A 交通信号样本。

## 条目 1: North-east timed signal cycle with latch-and-timer memory bits

- 控制对象：基于 Schneider PLC 的双方向交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个双向路口交通灯控制器，用启动/停止主锁存、`M2-M6` 内存位、计时器和计数器驱动 north/east 两路红黄绿灯循环。
- 判断：算。对象是实际交通灯控制系统，原文给出了 north/east 相位次序、每个阶段的持续时间，以及 `M2-M6 -> Q1-Q6` 的输出对应关系。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-33 行
> In this system the PLC is operated through a start and off switch and the traffic lights are given different priorities with the help of timers. The system controls a two-way traffic signal ... The work that has been implemented a master circuit using the start and the stop pb with memory latching has been used. That memory latch has been used as the input along with timers to create the different light signals at the required interval of time.

#### 摘录 B

- 出处：第 6 页，`9.2 PROCESS DIAGRAM`，`paper_content.txt` 第 505-520 行
> The north side road has signals R1, G1, Y1 and the east direction road are R2, G2, Y2. At the first instant the red signal on the north side road glows for five minutes and the red signal on the east side road glows for five minutes. After that, the red signal on the north side road continues to glow whereas the east side signal turns to yellow. Next, the red signal on the north side continue to glow but the east side road changes its signal to green ... at last, north side signal becomes green whereas, the east side continue to be red ... After completing this cycle the entire process repeats itself.

#### 摘录 C

- 出处：第 6-7 页，`10. RESULTS AND DISCUSSION / 10.2 COUNTER`，`paper_content.txt` 第 540-558 行、第 590-616 行
> The topmost circuit acts as the master circuit ... The memory bit that is latched in the first circuit acts as the input in the second circuit. The timer t5 (NC) is fed parallel and t1 (NC) is used in the input with the memory bit M2 ... In the memory bit M2, M3, M4 R1 is common ... connected to the output Q1 ... M6 is connected to Q5(Y1) ... M5 is connected to Q3(G1) ... M4 is connected to Q6(Y2) ... M3 is connected to Q4(G2).
>
> The north road begins with a red light and remains that way while the east road alternates between red, yellow, and green ... Utilizing counters and timers, the timers regulate how long each light (Red, Yellow, Green) remains on ... The memory bits M2, M3, etc. function in tandem with timers to guarantee proper signal switching by storing the current states of each signal.

### 2. 基于原文整理后的自然语言描述

The Schneider PLC controller uses a start-stop master circuit with memory latching to initialize and sustain a timed traffic-light sequence for the north and east roads. The phase cycle is organized around the two directions `R1/G1/Y1` and `R2/G2/Y2`: both roads begin in red, the east side then passes through yellow and green while the north side stays red, and later the east side returns to red while the north side goes through yellow and green before the whole cycle repeats. The paper maps this sequence to ladder-level memory bits and outputs, using timer contacts together with `M2-M6` to drive `Q1-Q6` for the corresponding lamps. The result is a repeatable timed two-road signal controller in which counters and timers maintain phase duration and guarantee that the light changes occur in the intended order.

### 3. 逐句溯源

1. 句子 1：The Schneider PLC controller uses a start-stop master circuit with memory latching to initialize and sustain a timed traffic-light sequence for the north and east roads.
   对应摘录：A, C
2. 句子 2：The phase cycle is organized around the two directions `R1/G1/Y1` and `R2/G2/Y2`: both roads begin in red, the east side then passes through yellow and green while the north side stays red, and later the east side returns to red while the north side goes through yellow and green before the whole cycle repeats.
   对应摘录：B, C
3. 句子 3：The paper maps this sequence to ladder-level memory bits and outputs, using timer contacts together with `M2-M6` to drive `Q1-Q6` for the corresponding lamps.
   对应摘录：C
4. 句子 4：The result is a repeatable timed two-road signal controller in which counters and timers maintain phase duration and guarantee that the light changes occur in the intended order.
   对应摘录：A, C
