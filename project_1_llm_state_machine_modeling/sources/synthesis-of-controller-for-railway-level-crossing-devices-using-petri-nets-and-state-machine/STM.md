# Synthesis of Controller for Railway-Level Crossing Devices Using Petri Nets and State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路道口控制器同时写成 simple time Petri net 与 LabVIEW statechart，明确给出 closing/opening 子过程、8 秒与 6 秒时序及四态控制图，属于高价值道口时序控制样本。

## 条目 1: Timed Railway Level-Crossing Warning and Barrier Statechart

- 控制对象：自动铁路道口警示与栏杆开闭控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是轨道交通领域的道口控制器，利用传感轨段触发红灯、警笛、栏杆闭合与重新开启，并把这套行为实现为带时间约束的 Petri net 与四态 statechart。
- 判断：算。对象是实际铁路道口设备控制器，不是纯形式化方法演示；正文明确给出了报警/闭合/开启链路、8 秒与 6 秒约束、预警时间范围，以及状态机中的 waiting/closing/maintenance/opening 四态。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，Section 3.1，`paper_content.txt` 第 163-183 行
> rail vehicle approaching the crossing ... launch controller of MCD system, resulting in the inclusion of red light on the road signals and turning on sirens sound signal, after 8 seconds' delay, electric drives that leave the bars dams are activated ... after max. 6 seconds from the exit of the rail vehicle from the sensor track of the crossing danger zone, lights on the road signalling are switched off and lifting of bars dams begins.

#### 摘录 B

- 出处：第 6-7 页，Section 3.1，`paper_content.txt` 第 184-201 行
> closing the crossing must be performed with the appropriate lead time ... it is assumed that the pre-warning time t0 is: t0 = tn + tzp + t0p ... the delay time to be paid by the MCD controller ... shall be 1 sec ... the time should be included in the range: 30 s < t0 < 90 s.

#### 摘录 C

- 出处：第 8-10 页，Section 5-6，`paper_content.txt` 第 223-249 行，第 253-274 行
> a simple time net for these devices is developed ... Macrotransition TM12 is responsible for closing the passage sub-process and macrotransition TM14 for sub-process of opening run ... The state diagram ... takes the following four states: waiting, closing, maintenance, opening ... The features of this module include ... states and transitions, events, hierarchy, and substates.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller begins its warning sequence when a train is detected on the approach section, at which point the road red lights and siren are activated immediately. After an 8-second engineered delay, the barrier drives are commanded to close, the barrier lamps are turned on as the barriers deviate from the vertical position, and the closure process may continue even if a second train is detected during warning. Once the train leaves the danger zone, the opening sequence begins within at most 6 seconds, the road lights are switched off, the barriers are lifted, and the lamp and signalling states are updated again when the vertical position is restored. The timing envelope is not informal: the paper defines a pre-warning formula `t0 = tn + tzp + t0p`, with controller delay and inventory constants, and constrains the usable lead time to the range from 30 to 90 seconds. This behavior is first modeled as a simple time Petri net with macrotransitions for detection, closing and opening, and then implemented as a LabVIEW statechart with the four controller states `waiting`, `closing`, `maintenance`, and `opening`, including hierarchy and substates.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller begins its warning sequence when a train is detected on the approach section, at which point the road red lights and siren are activated immediately.
   对应摘录：A；`paper_content.txt` 第 163-168 行。
2. 句子 2：After an 8-second engineered delay, the barrier drives are commanded to close, the barrier lamps are turned on as the barriers deviate from the vertical position, and the closure process may continue even if a second train is detected during warning.
   对应摘录：A；`paper_content.txt` 第 169-175 行。
3. 句子 3：Once the train leaves the danger zone, the opening sequence begins within at most 6 seconds, the road lights are switched off, the barriers are lifted, and the lamp and signalling states are updated again when the vertical position is restored.
   对应摘录：A；`paper_content.txt` 第 177-183 行。
4. 句子 4：The timing envelope is not informal: the paper defines a pre-warning formula `t0 = tn + tzp + t0p`, with controller delay and inventory constants, and constrains the usable lead time to the range from 30 to 90 seconds.
   对应摘录：B；`paper_content.txt` 第 184-201 行。
5. 句子 5：This behavior is first modeled as a simple time Petri net with macrotransitions for detection, closing and opening, and then implemented as a LabVIEW statechart with the four controller states `waiting`, `closing`, `maintenance`, and `opening`, including hierarchy and substates.
   对应摘录：C；`paper_content.txt` 第 223-249 行，253-274 行。
