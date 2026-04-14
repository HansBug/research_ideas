# Automatic Bottle Filling System Using Plc Based Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了基于 IR 传感、TONR `7s` 灌装、TP `2s` 输送复位的 PLC 灌装逻辑，能直接形成高质量离散制造条目。

## 条目 1: TONR-Based Bottle Filling and Conveyor Handoff Controller

- 控制对象：自动灌装线的输送与定时灌装控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个瓶装灌装线控制器，用输送带、红外检测、泵/灌装阀、TONR 保持计时和 2 秒传送复位脉冲完成“到位-灌装-离位-下一瓶”循环。
- 判断：算。对象是实际离散制造控制器，原文给出 Ladder Network、7 秒灌装定时、故障恢复后剩余时间续算、2 秒输送衔接以及 IR 传感触发条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 16-24 行
> This paper presents a bottle filling machine that utilizes a PLC (programmable logic controller) in the automation business.
>
> The bottle is moved by means of a belt conveyor. Water flow is regulated by a DC pump that is set to tank. An infrared sensor uses the bottle's position to determine when to operate the pump. The pump is turned on and the bottle is filled with water when it is beneath the tank.

#### 摘录 B

- 出处：第 2-3 页，`III. PROPOSED WORK / Ladder Diagram`，`paper_content.txt` 第 157-173 行
> We have a start and stop pushbuttons for controlling the bottle filling process.
>
> Note: In this example, we are filling the bottles based on a timer (fixed time duration).
>
> According to the problem, we need a valve to be open for 7 seconds, and if there is a fault in between then when the fault is resolved the timer opens the valve for the remaining time so that the bottle gets completely filled, and does not get overflow.
>
> In order to do so, we have used a TONR that does not get reset completely even after power is cut.

#### 摘录 C

- 出处：第 3 页，`Network-2 / Network-3 / Network-4 / Working of System`，`paper_content.txt` 第 188-231 行
> Network-2: It contains a TONR whose state is controlled by the memory bit status from network 1. As the timer is turned on the memory bit M0.1 is activated after 7 seconds.
>
> Network-3: ... The fill valve will be in the open state until the timer TONR is not in the active state.
>
> Network-4: When the filling of the bottle is complete the conveyor motor should be turned on for 2 seconds. To turn on the motor for 2 seconds we can use TP, after which the timer TONR is made to reset ...
>
> The conveyor motor will stop moving and the DC pump will begin to feed liquid into the bottle when the infrared sensor identifies the bottle. ... If another bottle is detected, the same procedure will be carried out.

### 2. 基于原文整理后的自然语言描述

The bottle-filling controller is a PLC-based EFSM in which the conveyor first advances a bottle to the filling point and an infrared sensor then decides when the filling sequence should start. Once a bottle is detected under the tank, the conveyor stops, the DC pump or fill valve is enabled, and a `TONR` timer keeps that filling action active for `7` seconds so the bottle can be completed without overflow. Because the controller uses a retentive timer, an interruption does not force the fill cycle back to zero; instead, the valve reopens for the remaining time after the fault is cleared. After the fill phase completes, a `TP` pulse turns the conveyor motor on for `2` seconds, resets the `TONR`, and hands the system back to the transport stage so the next bottle can move into position. The overall loop is therefore a clean sequence of start/hold, timed filling, post-fill conveyor advance, and sensor-triggered restart.

### 3. 逐句溯源

1. 句子 1：The bottle-filling controller is a PLC-based EFSM in which the conveyor first advances a bottle to the filling point and an infrared sensor then decides when the filling sequence should start.
   对应摘录：A, C
2. 句子 2：Once a bottle is detected under the tank, the conveyor stops, the DC pump or fill valve is enabled, and a `TONR` timer keeps that filling action active for `7` seconds so the bottle can be completed without overflow.
   对应摘录：A, B, C
3. 句子 3：Because the controller uses a retentive timer, an interruption does not force the fill cycle back to zero; instead, the valve reopens for the remaining time after the fault is cleared.
   对应摘录：B
4. 句子 4：After the fill phase completes, a `TP` pulse turns the conveyor motor on for `2` seconds, resets the `TONR`, and hands the system back to the transport stage so the next bottle can move into position.
   对应摘录：C
5. 句子 5：The overall loop is therefore a clean sequence of start/hold, timed filling, post-fill conveyor advance, and sensor-triggered restart.
   对应摘录：A, C
