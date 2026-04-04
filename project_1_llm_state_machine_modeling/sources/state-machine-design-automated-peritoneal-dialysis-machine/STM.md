# State Machine Design for an Automated Peritoneal Dialysis Machine - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了自动腹膜透析机的 5-bit FSM、I/O 表、驻留计时、浊度终止和 `11111` 错误态，能够直接形成高质量医疗设备过程控制描述。

## 条目 1: APD process supervisor with turbidity-triggered termination and error alarm
- 控制对象：自动腹膜透析机的过程监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个为自动腹膜透析机调度准备液体、注液、驻留、排液、冲洗与错误告警的设备过程状态机，核心 guard 来自流量、压力、液位、浊度、故障和定时变量。
- 判断：算。对象是真实医疗设备控制器，不是界面流程；原文给出了状态编码、I/O、转移逻辑、dwell timer 与 error state，完全符合本研究关注的状态机属性控制系统。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> This work aims to implement a finite state machine design to modify the process of an automated, economical PD system.
>
> Furthermore, a turbidity sensor is added to measure the efficiency of the dialysis process and reduce the current dialysis time, which can reach eight hours.

#### 摘录 B
- 出处：第 7 页，Section 3.3 `Interface design`
> During the dwelling phase, the duration is defined, and a timer is included.
>
> The turbidity check is integrated ... blue to indicate low turbidity during the drainage stage.
>
> Any fault activates an error state in the FSM (state 11111), which immediately halts the system and alerts the user both visually and audibly.

#### 摘录 C
- 出处：第 8 页，Section 4.1 `Finite state machine (FSM)`
> Thus, they are employed to model the process of the designed PD machine.
>
> future development will include serum creatinine monitoring ... to enable adaptive FSM transitions based on clearance efficiency rather than preset time-based states.

#### 摘录 D
- 出处：第 10 页，Section 4.2-4.3 / Table 2 / Figure 13
> The I/O table, Table 2, shows that there are 16 inputs and 18 outputs representing the proposed design.
>
> The state diagram presented in Figure 13 illustrates all possible states for the proposed PD process, where the standby state is assigned as 00000 and the error alarm as 11111.

### 2. 基于原文整理后的自然语言描述

The automated peritoneal dialysis machine is modeled as a finite state process controller whose state space covers standby, instruction handling, solution preparation, filling, dwelling, draining, looping, flushing, and a dedicated error alarm state. After the user completes the startup and safety-confirmation sequence, the controller prepares the dialysis solution, enters the filling phase, and then switches into a dwelling phase in which a timer explicitly governs the residence period of the solution. During drainage, the machine evaluates turbidity so that clear effluent can terminate the session earlier instead of forcing a fixed maximum-duration cycle, while the remaining sensor inputs continue to supervise flow, pressure, and liquid level conditions. The state diagram is coupled with a 16-input/18-output table, so the machine’s transitions are guarded by concrete process signals rather than by a purely narrative workflow. Any detected fault or dangerous condition forces the controller into the `11111` error-alarm state, where the process is halted immediately and the user is alerted visually and audibly.

### 3. 逐句溯源

1. 句子 1：The automated peritoneal dialysis machine is modeled as a finite state process controller whose state space covers standby, instruction handling, solution preparation, filling, dwelling, draining, looping, flushing, and a dedicated error alarm state.
   对应摘录：C, D
2. 句子 2：After the user completes the startup and safety-confirmation sequence, the controller prepares the dialysis solution, enters the filling phase, and then switches into a dwelling phase in which a timer explicitly governs the residence period of the solution.
   对应摘录：B, D
3. 句子 3：During drainage, the machine evaluates turbidity so that clear effluent can terminate the session earlier instead of forcing a fixed maximum-duration cycle, while the remaining sensor inputs continue to supervise flow, pressure, and liquid level conditions.
   对应摘录：A, B, D
4. 句子 4：The state diagram is coupled with a 16-input/18-output table, so the machine’s transitions are guarded by concrete process signals rather than by a purely narrative workflow.
   对应摘录：D
5. 句子 5：Any detected fault or dangerous condition forces the controller into the `11111` error-alarm state, where the process is halted immediately and the user is alerted visually and audibly.
   对应摘录：B, D
