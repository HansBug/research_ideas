# Control and Plant Modeling for Manufacturing Systems using Statecharts - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 并行, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 tagged machine 的送料、压标、取件过程写成 `Statecharts + guard + timerT1 + tm(2s)` 控制链，既有对象边界，也有具体 `psOn / s1On / s2On / s3On / fsOn` 触发顺序和阀门动作，属于高质量制造控制样本。

## 条目 1: Tagged-Machine Statecharts Control with a Two-Second Pressing Timer

- 控制对象：工业自动化与离散制造领域的 tagged machine 送料、压标与取件顺序控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 并行, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个典型制造单元的顺序控制系统，由 piece-loader、piece-sensor、三个单作用气缸、阀门和 photoelectric sensor 组成，并用 Statecharts 把送料、压标、取件与两秒定时压紧流程串起来。
- 判断：算。对象是实际 manufacturing machine controller，不是单纯建模方法流程；原文把组件、初始配置、运行场景、guards、阀门命令和 `timerT1 / tm(2s)` 都明确写出。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Section `IV.A Definition`，`paper_content.txt` 第 305-325 行
> The tagged machine is composed of seven components: (a piece-loader, a piece-sensor - PS, a feeding cylinder - C1, a pressing cylinder - C2, an extraction cylinder - C3, an air-compressed valve - V4, and a photoelectric sensor - FS). ... In its initial configuration the system needs to have all cylinder arms, valves and sensors set to "RETURNED", "OFF" and "FALSE", respectively. The system starts its operation when the "Start" button is pushed. The running scenario is described as follows: "The feeding cylinder pushes one workpiece to the mold. Then the pressing cylinder pushes the tag over the workpiece for about two seconds. As the last step, the extraction cylinder joins valve4 to remove the piece, pushing it to the deposit."

#### 摘录 B

- 出处：第 5-6 页，Section `IV.B The Model`，`paper_content.txt` 第 431-462 行
> For example, psOn[c1]=v1On means that: when the event "psOn" occurs, the command-event "v1On" is triggered ... s1On[c2]=v1Off&v2On means that: when the event "s1On" occurs, if [c2] is true then the command-events "v1Off" and "v2On" are triggered ... s2On[c3]=timerT1 means that: when the event "s2On" occurs, if [c3] is true then the event "timerT1" is triggered ... tm(2s)[c4]/v2Off&v3On

#### 摘录 C

- 出处：第 5-6 页，Fig. 10 `Tagged machine: control model` 及其说明，`paper_content.txt` 第 486-507 行
> TimerT1 Off On* timerT1 [c3] tm(2s)
>
> ... the asterisk in state "On" of TimerT1 indicates the start of timer and after two seconds (tm(2s)) the variable "T1" should be changed to "true".

#### 摘录 D

- 出处：第 5-6 页，Fig. 9 `Tagged machine: sequence of events` 及说明，`paper_content.txt` 第 452-469 行
> psOn [c1]/v1On
> s1On [c2]/v1Off&v2On
> s2On [c3]/timerT1
> tm(2s) [c4]/v2Off&v3On
> s3On [c5]/v4On
> fsOn [c6]/v3Off&v4Off

### 2. 基于原文整理后的自然语言描述

The paper models a concrete tagged manufacturing machine rather than a generic workflow: a piece is loaded, pushed into the mold, pressed for about two seconds, and then extracted to the deposit. The controller starts from an initial configuration where all cylinder arms are returned, all valves are off, and all sensors are false, and it begins execution when the `Start` button is pressed. In the event chain, `psOn[c1]` opens valve `v1`, `s1On[c2]` closes `v1` and opens `v2`, and `s2On[c3]` triggers the internal timer `timerT1` instead of immediately advancing the extraction sequence. Once the timer reaches `tm(2s)` under guard `c4`, the controller closes `v2` and opens `v3`, then `s3On[c5]` opens `v4`, and finally `fsOn[c6]` closes `v3` and `v4` after the manufactured piece has been removed. Because the model is expressed in Statecharts with explicit guards, a dedicated timer component, and parallel actuator state machines, it is a strong `HSM + T1` manufacturing control sample rather than a loose scenario sketch.

### 3. 逐句溯源

1. 句子 1：The paper models a concrete tagged manufacturing machine rather than a generic workflow: a piece is loaded, pushed into the mold, pressed for about two seconds, and then extracted to the deposit.
   对应摘录：A
2. 句子 2：The controller starts from an initial configuration where all cylinder arms are returned, all valves are off, and all sensors are false, and it begins execution when the `Start` button is pressed.
   对应摘录：A
3. 句子 3：In the event chain, `psOn[c1]` opens valve `v1`, `s1On[c2]` closes `v1` and opens `v2`, and `s2On[c3]` triggers the internal timer `timerT1` instead of immediately advancing the extraction sequence.
   对应摘录：B, D
4. 句子 4：Once the timer reaches `tm(2s)` under guard `c4`, the controller closes `v2` and opens `v3`, then `s3On[c5]` opens `v4`, and finally `fsOn[c6]` closes `v3` and `v4` after the manufactured piece has been removed.
   对应摘录：B, C, D
5. 句子 5：Because the model is expressed in Statecharts with explicit guards, a dedicated timer component, and parallel actuator state machines, it is a strong `HSM + T1` manufacturing control sample rather than a loose scenario sketch.
   对应摘录：B, C
