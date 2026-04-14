# Batch Process Control using AB1400 Programmable Logic Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把工业混料槽的液位阈值、阀门顺序、`3 mins` 混合定时和排放复位链写成了一条完整 batch cycle，可直接作为工业批处理双 A 样本。

## 条目 1: Timed Water-Acid Mixing and Drain Batch Controller
- 控制对象：工业混料槽的批处理顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是工业自动化与离散制造领域的混料批处理控制器，用 `L1/L2/L3` 液位、三只电磁阀和 `3 mins` 定时链组织“放空-进水-进酸-混合-排放-重启”循环。
- 判断：算。对象是实际工业 mixer 的批处理控制程序，原文直接给出了输入液位、阀门动作、混合时间、排放顺序和循环复位逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`II. OBJECTIVE`，`paper_content.txt` 第 60-72 行
> This work try a simple blending of two colour fluids in a container where we only have three level sensors (L1,L2, and L3) and two liquids flowing in through two solenoid valves, solenoid a (water control) and solenoid b (acid control) and draining out through solenoid c (blend outflow).
>
> The batch is to be controlled by timer. After required level of blend is sensed (by L3) the mixer runs for 3 mins. ... The process initiates with the drain valve open, water and acid valves closed, mixer motor is off, and the tank is empty.

#### 摘录 B
- 出处：第 2 页，`III. OBSERVATION`，`paper_content.txt` 第 74-89 行
> When start button is pressed water is filled upto L2 and it ends as L2 is closed. First of all as start is pressed output O:0/15 turns ON and remains ON until tank is emptied. Rung 2 closes normally open drain valve, before timer T:4 activates. Rung 3 energises solenoid 1 until L2 doesn’t signal, once it signals solenoid 1 gets de-energised. Then motor is turned ON and mix it for 3 mins.
>
> Similarly acid is filled upto L3 by solenoid 2 as level gets detected by L3 solenoid b de-energises. And then mixer gets started and it runs for 3 minutes. After time delay of 3 mins solenoid 3 opens and the blend gets drained out. Once the blend gets out completely, the process cycle restarts.

### 2. 基于原文整理后的自然语言描述

The batch-process controller is a timed PLC EFSM for an industrial mixer with three level sensors `L1/L2/L3`, two inlet solenoid valves for water and acid, one outlet solenoid valve for draining, and a mixer motor. Its initial condition is an empty tank with the drain valve open, both inlet valves closed, and the mixer motor off. After the start button is pressed, the controller first closes the drain path, fills water through solenoid `a` until level `L2` is reached, and then turns the mixer on for a `3 mins` interval. It then fills acid through solenoid `b` until level `L3` is detected, runs the mixer again for `3 minutes`, and finally opens solenoid `c` to drain the blended liquid after the timed mixing delay expires. Once the tank is empty, the controller restarts the whole process cycle, so the overall logic is a drain-reset, staged filling, timed mixing, draining, and automatic repeat sequence.

### 3. 逐句溯源

1. 句子 1：The batch-process controller is a timed PLC EFSM for an industrial mixer with three level sensors `L1/L2/L3`, two inlet solenoid valves for water and acid, one outlet solenoid valve for draining, and a mixer motor.
   对应摘录：A
2. 句子 2：Its initial condition is an empty tank with the drain valve open, both inlet valves closed, and the mixer motor off.
   对应摘录：A
3. 句子 3：After the start button is pressed, the controller first closes the drain path, fills water through solenoid `a` until level `L2` is reached, and then turns the mixer on for a `3 mins` interval.
   对应摘录：B
4. 句子 4：It then fills acid through solenoid `b` until level `L3` is detected, runs the mixer again for `3 minutes`, and finally opens solenoid `c` to drain the blended liquid after the timed mixing delay expires.
   对应摘录：A, B
5. 句子 5：Once the tank is empty, the controller restarts the whole process cycle, so the overall logic is a drain-reset, staged filling, timed mixing, draining, and automatic repeat sequence.
   对应摘录：B
