# Design, Specification, and Synthesis of Aircraft Electric Power Systems Control Logic - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把飞机电气分配系统的 bus/contactor/generator 重构控制写成带时钟变量和接触器延迟约束的合成自动机，细节足够支撑一个高质量 EPS 重配置 EFSM 条目。

## 条目 1: Timed Reconfiguration Controller for Aircraft Electric Power Distribution

- 控制对象：飞机电气分配系统的接触器重配置与关键母线供电保护控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是飞机电气分配系统的离散重配置控制器，用来根据发电机健康状态、接触器状态和母线供电状态选择正确的 contactor configuration，并满足 50 ms 级别的关键母线约束。
- 判断：算。对象是实际 aircraft electric power system 的控制逻辑，不是单纯形式化方法演示；原文给出了环境变量、受控变量、母线时钟、接触器延迟和中央控制仿真结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 10 页，Figure 2.3 discussion
> "automaton moves to state 2 or state 3"

#### 摘录 B

- 出处：第 28 页，Section 3.3
> "never be unpowered for more than 50 msec"

#### 摘录 C

- 出处：第 36-37 页，Sections 3.3-3.4
> "10 msec"

### 2. 基于原文整理后的自然语言描述

The aircraft electric-power controller is synthesized as a finite automaton whose states encode current valuations of generators, contactors, and buses, and the controller chooses the next contactor configuration based on the observed environment state sequence. In the simplified case study, four generators feed four buses through seven contactors: generator health is treated as environment input, contactor commands and directions are controlled variables, and bus power statuses are dependent variables derived from neighboring generators and contactors. The controller must keep safety-critical buses powered, and the thesis states that such loads must never be unpowered for more than 50 ms while the system is being reconfigured through contactor state changes. To express that timing, each essential bus is assigned a clock variable whose tick is 10 ms, so the bus clock increments whenever the bus is unpowered and resets to zero once power is restored; the safety rule then bounds the allowable outage window to five ticks. The controller also models non-ideal actuation by introducing contactor intent variables and separate contactor clocks, which capture open and close delays between commands and physical state changes. As a result, the final control object is not a static table but a timed reconfiguration EFSM that jointly reasons about generator faults, resource non-paralleling, bus power status, and delayed contactor execution.

### 3. 逐句溯源

1. 句子 1：The aircraft electric-power controller is synthesized as a finite automaton whose states encode current valuations of generators, contactors, and buses, and the controller chooses the next contactor configuration based on the observed environment state sequence.
   对应摘录：A；`paper_content.txt` 第 606-612 行。
2. 句子 2：In the simplified case study, four generators feed four buses through seven contactors: generator health is treated as environment input, contactor commands and directions are controlled variables, and bus power statuses are dependent variables derived from neighboring generators and contactors.
   对应摘录：A；`paper_content.txt` 第 1136-1153 行。
3. 句子 3：The controller must keep safety-critical buses powered, and the thesis states that such loads must never be unpowered for more than 50 ms while the system is being reconfigured through contactor state changes.
   对应摘录：B；`paper_content.txt` 第 809-813 行。
4. 句子 4：To express that timing, each essential bus is assigned a clock variable whose tick is 10 ms, so the bus clock increments whenever the bus is unpowered and resets to zero once power is restored; the safety rule then bounds the allowable outage window to five ticks.
   对应摘录：B, C；`paper_content.txt` 第 1074-1089 行，1212-1218 行。
5. 句子 5：The controller also models non-ideal actuation by introducing contactor intent variables and separate contactor clocks, which capture open and close delays between commands and physical state changes.
   对应摘录：C；`paper_content.txt` 第 1100-1114 行。
6. 句子 6：As a result, the final control object is not a static table but a timed reconfiguration EFSM that jointly reasons about generator faults, resource non-paralleling, bus power status, and delayed contactor execution.
   对应摘录：A, B, C；`paper_content.txt` 第 809-813 行，1074-1114 行，1263-1280 行。
