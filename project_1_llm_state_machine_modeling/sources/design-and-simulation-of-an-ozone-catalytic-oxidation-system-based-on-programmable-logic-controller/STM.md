# Design and Simulation of an Ozone Catalytic Oxidation System Based on Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文同时给出 `manual / automatic / secondary / stop` 运行分支、`15 min / 1 h / 30 min` 工程定时和围绕 `pH ≈ 9` 的 PID 闭环调节链，是过程控制方向结构差异比较明确的双 A 样本。

## 条目 1: Manual-auto OCO pH-treatment supervisor

- 控制对象：过程与环境控制领域的臭氧催化氧化废水处理 `PLC` 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个以 `Siemens S7-200 PLC` 为下位机、以 `Kingview` 为上位监控平台的臭氧催化氧化废水处理控制器，负责在手动、自动和二次运行条件下组织进液、加药、臭氧反应、循环泵和排液流程，并持续调节反应液 `pH`。
- 判断：算。对象是实际废水处理控制系统，原文不仅给出传感器到泵阀/臭氧发生器的控制链，还明确写出 `15 min / 1 h / 30 min` 的过程时序和 `manual / automatic / secondary / stop` 模式切换。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`3. System design` 与 `3.1 pH control`，`paper_content.txt` 第 121-137, 161-166 行
> As shown in Figure 1, the OCO system mainly consists of a physical sedimentation unit, an ozone generating unit, a reaction system, and an exhaust destruction system.
>
> During wastewater treatment, the pH needs to be stabilized at around 9... Here, the titration image is divided into three parts ... Then, three-stage nonlinear PID control was introduced to control the pH of the three parts.
>
> Because the reaction must be maintained in an alkaline state, hydrogen peroxide was directly applied to adjust the pH of the system. When the pH deviates from the equilibrium state, the amount of hydrogen entering the system was changed by adjusting the opening of the hydrogen peroxide pump until the system pH is as required.

#### 摘录 B

- 出处：第 3 页，`3.2 Signal transmission and processing of pH control system` 与 `3.3 Lower computer system`，`paper_content.txt` 第 171-224 行
> To control the pH through the reaction, a single closed loop control system was constructed to make a timely feedback upon detecting a signal. Then, the reaction system can adjust the pH based on the feedback.
>
> ... the probe of the sensor was directly contacted with the reaction liquid... The signal is transmitted via the wire to a pH meter, and converted into an electrical signal.
>
> ... the resulting digital signal will be transmitted to the single-chip microcomputer (SCM). Then, the digital signal sent out by the SCM will be converted into a 4-20mA current signal by a digital/analog (D/A) converter. Finally, the current signal will act on the hydrogen peroxide pump, directing it to change its opening.
>
> The main functions of the lower computer are to acquire the system states and feed back them to the upper computer, including pH, oxidation reduction potential (ORP), as well as the speed and on-off state of each pump... Finally, the PLC controller issues signals to control the pumps and ozone generator, referring to the received signals.

#### 摘录 C

- 出处：第 4 页，`3.6 Main program`，`paper_content.txt` 第 287-323 行
> (1) If the system is set to the manual mode, the green light will turn on at the first operation. At this time, the wastewater inlet pump pumps the wastewater into the settling tank, and the PLC timer starts counting for 15min... the ozone generator and the circulating pump will start to work, and the PLC timer will start counting for 1h... Finally, the outlet pump will be turned on to discharge the wastewater.
>
> (2) If the system is set to the automatic mode, the red light will turn on, and the timer will start counting for 30min. During this period, the manual mode was adopted to prevent the system from making large errors. After 30min, the PID program will be started to control the hydrogen peroxide pump, and monitor whether the pH of the reaction liquid reaches the set point.
>
> (3) If the system encounters a secondary operation... the timer will start to count for 15min to keep the operations of all devices in sync...
>
> (4) The stop button can send a signal to request the system to shut down.

#### 摘录 D

- 出处：第 4-5 页，`3.7 PID pH control system`，`paper_content.txt` 第 328-363 行
> ... if the signal is 1, the system will enter the manual mode, and the speed of the hydrogen peroxide pump will be controlled by the analog output; if the signal is 0, the system will enter the automatic mode, and the speed of the hydrogen peroxide pump will be adjusted automatically.
>
> ... I0.0 in the subprogram is the button to switch between the manual mode and automatic mode of the PID program. If I0.0 is ON, the system is in automatic mode; if it is OFF, the system is in manual mode.

### 2. 基于原文整理后的自然语言描述

The OCO controller supervises a wastewater-treatment plant composed of sedimentation, ozone generation, reaction, and exhaust-destruction units, and it keeps the reaction liquid near `pH = 9` through a three-stage nonlinear PID design. A closed-loop sensing chain sends the measured pH from the reaction liquid through the pH meter, A/D conversion, and PLC processing, and the PLC then adjusts the hydrogen-peroxide pump opening through a `4-20 mA` output signal. At the equipment level, the lower computer continuously acquires `pH`, `ORP`, and pump speed/on-off states, reports them to the upper computer, and issues commands to the pumps and ozone generator. In manual first-run mode, the controller fills the settling/OCO tanks, counts `15 min`, starts hydrogen peroxide dosing, then launches the ozone generator and circulating pump for `1 h` before discharging the wastewater. In automatic mode, the system first stays in a protected `30 min` stage, then enables PID pH regulation; if the plant is restarted after a stop, a secondary-operation branch shortens the pumping stage to `15 min`, and a stop request can shut the system down from any run.

### 3. 逐句溯源

1. 句子 1：The OCO controller supervises a wastewater-treatment plant composed of sedimentation, ozone generation, reaction, and exhaust-destruction units, and it keeps the reaction liquid near `pH = 9` through a three-stage nonlinear PID design.
   对应摘录：A
2. 句子 2：A closed-loop sensing chain sends the measured pH from the reaction liquid through the pH meter, A/D conversion, and PLC processing, and the PLC then adjusts the hydrogen-peroxide pump opening through a `4-20 mA` output signal.
   对应摘录：B
3. 句子 3：At the equipment level, the lower computer continuously acquires `pH`, `ORP`, and pump speed/on-off states, reports them to the upper computer, and issues commands to the pumps and ozone generator.
   对应摘录：B
4. 句子 4：In manual first-run mode, the controller fills the settling/OCO tanks, counts `15 min`, starts hydrogen peroxide dosing, then launches the ozone generator and circulating pump for `1 h` before discharging the wastewater.
   对应摘录：C
5. 句子 5：In automatic mode, the system first stays in a protected `30 min` stage, then enables PID pH regulation; if the plant is restarted after a stop, a secondary-operation branch shortens the pumping stage to `15 min`, and a stop request can shut the system down from any run.
   对应摘录：C, D
