# CubeSat Flight Software: Insights and a Case Study - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文在 PHI-Demo case study 中给出了脚本引擎的显式状态机，并把 LEOP 自动脚本、时延命令链和在轨脚本排程写得很完整，可直接形成 CubeSat 任务脚本监督样本。

## 条目 1: PHI-Demo Script Engine with LEOP and Chained Orbit Scripts
- 控制对象：PHI-Demo CubeSat app-based flight software 的脚本执行引擎
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 CubeSat 机载软件中的脚本引擎，用于在失联或长间隔接触期间按时间顺序执行 CLI 命令脚本，并在 LEOP、载荷操作和后续多轨任务之间做自动衔接。
- 判断：算。对象是实际 12U CubeSat flight software 的任务执行子系统，原文给出了脚本文件触发条件、`Idle / Armed / Running / Finished / Aborted` 状态机、LEOP 启动脚本和脚本链式执行机制。

### 1. 原文摘录

#### 摘录 A
- 出处：第 29 页，`Script Engine`
> A script file is simply a sequence of CLI commands optionally separated by time delays and stored in a text file. When a script file is triggered, commands are released and executed in a timely fashion while orbiting, whether the satellite is still in contact or not.
>
> The script engine works by first setting the engine itself to armed. A script file must also be marked as armed.
>
> Next, the script engine reads the armed file and starts executing the CLI commands stored in the script file line-by-line.

#### 摘录 B
- 出处：第 29 页，`Script Engine`
> Upon execution, an output file is created and filled with reply lines corresponding to each CLI command executed.
>
> At the end of each script file, another script file can also be armed.
>
> Upon finishing the execution of the first one, the following script file is executed. This allows the ground team to queue or chain many script files covering satellite operations for many orbits spanning many upcoming days or weeks.

#### 摘录 C
- 出处：第 30 页，`Fig. 10 State Machine Diagram for the Script Engine`
> Idle
>
> Armed Script Engine Armed by command
>
> Running Script File Armed by command
>
> Finished Aborted

#### 摘录 D
- 出处：第 30 页，`Fig. 10` 下方正文
> when the FSW is initialized and run for the first time (upon separation), a script dedicated for Launch and Early Orbit Phase (LEOP) operations is run immediately.
>
> The LEOP script conducts operation such as solar panel and antenna deployment.
>
> Then, the script engine enters an idle mode waiting to be armed.

### 2. 基于原文整理后的自然语言描述

The PHI-Demo flight software includes a script engine that executes onboard operations as a timed sequence of CLI commands stored in text scripts, so satellite tasks can continue while the spacecraft is out of contact with the ground. The controller first requires both the engine and a script file to be marked as armed, then enters a `Running` state where it reads the armed file line by line, releases commands with any scripted delays, and records each reply into an output file for later downlink inspection. Its explicit state machine contains `Idle`, `Armed`, `Running`, `Finished`, and `Aborted`, and script completion may directly arm the next script so that many operations can be chained across multiple orbits, days, or weeks. On first startup after separation, a dedicated `LEOP` script is launched immediately to handle actions such as solar-panel and antenna deployment, and only after that sequence finishes does the engine return to `Idle` waiting for future arming. As a result, the script engine behaves as a mission-task FSM that combines explicit run states, delayed command execution, startup automation, and multi-script queueing into one reusable orbit-operations controller.

### 3. 逐句溯源

1. 句子 1：The PHI-Demo flight software includes a script engine that executes onboard operations as a timed sequence of CLI commands stored in text scripts, so satellite tasks can continue while the spacecraft is out of contact with the ground.
   对应摘录：A
2. 句子 2：The controller first requires both the engine and a script file to be marked as armed, then enters a `Running` state where it reads the armed file line by line, releases commands with any scripted delays, and records each reply into an output file for later downlink inspection.
   对应摘录：A, B
3. 句子 3：Its explicit state machine contains `Idle`, `Armed`, `Running`, `Finished`, and `Aborted`, and script completion may directly arm the next script so that many operations can be chained across multiple orbits, days, or weeks.
   对应摘录：B, C
4. 句子 4：On first startup after separation, a dedicated `LEOP` script is launched immediately to handle actions such as solar-panel and antenna deployment, and only after that sequence finishes does the engine return to `Idle` waiting for future arming.
   对应摘录：D
5. 句子 5：As a result, the script engine behaves as a mission-task FSM that combines explicit run states, delayed command execution, startup automation, and multi-script queueing into one reusable orbit-operations controller.
   对应摘录：A, B, C, D
