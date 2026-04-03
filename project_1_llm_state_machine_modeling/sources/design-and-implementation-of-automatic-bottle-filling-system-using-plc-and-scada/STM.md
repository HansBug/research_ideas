# Design and Implementation of Automatic Bottle Filling System Using PLC and SCADA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出了停带灌装短流程，还明确补足了顶置储液罐的液位维持逻辑和实现阶段的定时替代方案。

## 条目 1: Photoelectric Detection and Valve-Controlled Filling Cycle
- 控制对象：瓶装液体灌装站的 PLC 与 SCADA 控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G8 瓶装灌装短流程）

### 0. 条目识别与判定
- 一句话说明：这是工业灌装领域的瓶装灌装控制器，用于检测瓶子到达灌装工位、停止输送带、打开电磁阀灌装并在达到目标后恢复输送。
- 判断：算。对象是实际灌装控制系统，原文给出了 photoelectric sensor、conveyor stop/run、electrovalve open/close 和 filling completion 的明确顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 31 页，Bottle Detection Mechanism / Liquid Flow Control Mechanism，行 743-755
> The task of bottle detection is performed using a photoelectric sensor. A photoelectric sensor is placed on the side of the conveyor belt at the filling station to detect the presence of a bottle. ... when a bottle is brought in front of the sensor by the conveyor belt ... the PLC will give command to the conveyor motor to run or to stop. When the bottle is detected by the photoelectric sensor, the task of filling the bottle with liquid starts. An electro valve is used to control the flow of liquid from overhead tank to the bottle. The electrovalve is positioned at the filling station. When a bottle stops underneath the valve, it gets a command from the PLC to open the valve and liquid flows from the overhead tank to the bottle up to a particular level.

#### 摘录 B
- 出处：第 66-68 页，Flow Chart for Bottle Sensing and Filling System / Liquid level control，行 1821-1857
> Figure 4.11 shows the flow chart of the bottle sensing and filling system. When the system is powered on, the conveyor belt starts running. The conveyor belt keeps running if the photoelectric sensor does not detect the presence of any bottle in front of it. If the sensor detects any bottle then the conveyor belt stops, Electro valve opens and bottle filling starts, the amount of liquid filling is controlled using a weighting sensor. ... The Electro valve then closes and after some time delay conveyor belt starts again with the filled bottle and carries the bottle to the other end where the bottle is collected. ... When the liquid goes below low level, the DC motor starts pumping liquid from the main reservoir to the overhead tank. When the liquid touches upper level, DC motor pump stops to prevent overflow of liquid at the overhead tank.

#### 摘录 C
- 出处：第 70-71 页，Conclusion，行 1987-1999
> Since weighting sensor was not available to control the amount of liquid to be filled while implementing the system. The amount is controlled using a timer instead, which results in different amount of liquid for different bottles.

### 2. 基于原文整理后的自然语言描述

When the bottle-filling system is powered on, the conveyor keeps running until the photoelectric sensor detects a bottle at the filling station. Once a bottle is detected, the PLC stops the conveyor, opens the electrovalve, and starts filling the bottle from the overhead tank. In the control design the filling amount is decided from the target quantity, and in the implemented prototype this quantity is approximated by a timer because the weighting sensor was unavailable. After the target amount is reached, the valve is closed, the conveyor restarts after a short delay, and the filled bottle is carried to the collection end; in parallel, low- and high-level sensing keeps the overhead tank supplied by starting the pump below the low level and stopping it again at the upper level.

### 3. 逐句溯源

1. 句子 1：When the bottle-filling system is powered on, the conveyor keeps running until the photoelectric sensor detects a bottle at the filling station.
   对应摘录：A, B
2. 句子 2：Once a bottle is detected, the PLC stops the conveyor, opens the electrovalve, and starts filling the bottle from the overhead tank.
   对应摘录：A, B
3. 句子 3：In the control design the filling amount is decided from the target quantity, and in the implemented prototype this quantity is approximated by a timer because the weighting sensor was unavailable.
   对应摘录：B, C
4. 句子 4：After the target amount is reached, the valve is closed, the conveyor restarts after a short delay, and the filled bottle is carried to the collection end; in parallel, low- and high-level sensing keeps the overhead tank supplied by starting the pump below the low level and stopping it again at the upper level.
   对应摘录：B
