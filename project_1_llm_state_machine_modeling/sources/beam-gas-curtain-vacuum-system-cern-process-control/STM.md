# Automated Process Control for the Beam Gas Curtain Vacuum System at CERN - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 CERN 束气幕真空系统的自动注气过程明确定义成 PLC 上的注入 FSM，并给出状态功能、`10 min`/`20 h` 定时、压力/执行器故障触发的恢复与 `Safe` 链。

## 条目 1: Beam-Gas Curtain Injection State Supervisor

- 控制对象：CERN BGC 真空系统的自动气体注入控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个在 CERN 真空控制框架中运行的 PLC 注气过程监督器，用状态机驱动阀门、抽气、注气、恢复和安全锁定链条。
- 判断：算。对象是真实大型科研装置的工艺控制器，原文不仅说“用了 PLC/FSM”，还逐状态解释 `Stand-by / Preparing / Prepared / Injection / Stopping Injection / Recovery / Safe / Service` 的职责与转移条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 9-19 行
> This paper presents the design and implementation of an automated gas injection control system, fully integrated within the LHC Vacuum Control System SCADA and using Vacuum Framework. The solution includes a finite state machine (FSM) deployed on a programmable logic controller (PLC), a new state-aware SCADA interface, and a comprehensive interlock strategy combining device-level and process-level safety. ... requiring only two user actions to initiate an injection.

#### 摘录 B

- 出处：第 5 页，`3.1 Automatic Injection Process`，`paper_content.txt` 第 283-318 行
> The FSM states correspond to the stages of the injection cycle ... Stand-by: Default operational state ... Preparing: Injection line is evacuated with PPINJ, gate valves are opened ... Prepared: System is ready for injection. If “Start Injection” command is not issued within 10 minutes, returns to Stand-by automatically through Recovery. Injection: VVA2 opens to inject the gas curtain. Stops on user command or automatically after 20 hours ... Stopping Injection ... Recovery ... Safe ... Service.

#### 摘录 C

- 出处：第 6 页，`3.2 Process Interlocks and State-Based Safety` 与 `3.3 New User Interface`，`paper_content.txt` 第 325-379 行
> Process interlocks are conditions applied to the states of the process. If the conditions are not met, the process will either not be able to start or will move from the current state to the Safe state in a controlled manner. ... Start Process Interlocks ... do not allow the process to move to the preparing state. ... Prepare Process Interlocks ... move the process to the Recovery state and then to the Safe state. ... Injection Process Interlocks ... move the process to the Stopping Injection state and then to the Safe state. ... only two button presses needed to start a gas injection.

### 2. 基于原文整理后的自然语言描述

The BGC automatic injection controller is implemented as a PLC-resident finite-state machine that coordinates vacuum preparation, gas injection, shutdown, recovery, and safe fallback for the CERN beam-gas curtain instrument. In the normal chain, the process starts from `Stand-by`, moves into `Preparing` to evacuate the injection line and open the necessary valves, reaches `Prepared`, and then enters `Injection` when the operator issues the start command. The controller carries explicit engineering timers: if the system remains in `Prepared` for more than `10 min` without a start command it returns toward `Stand-by` through `Recovery`, and if injection continues for `20 h` it is stopped automatically. During operation, pressure and device-status interlocks are evaluated per state, so violations during `Preparing` or `Prepared` force `Recovery` and then `Safe`, while violations during `Injection` first pass through `Stopping Injection` before ending in `Safe`. Experts may still switch to `Service` for manual maintenance, but normal user operation is reduced to two UI actions because the state-aware SCADA panel exposes the FSM, alarms, and interlock blockers directly.

### 3. 逐句溯源

1. 句子 1：The BGC automatic injection controller is implemented as a PLC-resident finite-state machine that coordinates vacuum preparation, gas injection, shutdown, recovery, and safe fallback for the CERN beam-gas curtain instrument.
   对应摘录：A, B
2. 句子 2：In the normal chain, the process starts from `Stand-by`, moves into `Preparing` to evacuate the injection line and open the necessary valves, reaches `Prepared`, and then enters `Injection` when the operator issues the start command.
   对应摘录：B
3. 句子 3：The controller carries explicit engineering timers: if the system remains in `Prepared` for more than `10 min` without a start command it returns toward `Stand-by` through `Recovery`, and if injection continues for `20 h` it is stopped automatically.
   对应摘录：B
4. 句子 4：During operation, pressure and device-status interlocks are evaluated per state, so violations during `Preparing` or `Prepared` force `Recovery` and then `Safe`, while violations during `Injection` first pass through `Stopping Injection` before ending in `Safe`.
   对应摘录：C
5. 句子 5：Experts may still switch to `Service` for manual maintenance, but normal user operation is reduced to two UI actions because the state-aware SCADA panel exposes the FSM, alarms, and interlock blockers directly.
   对应摘录：A, B, C
