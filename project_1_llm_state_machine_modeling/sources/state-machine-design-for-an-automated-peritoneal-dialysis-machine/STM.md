# State machine design for an automated peritoneal dialysis machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接以 FSM 为主题，给出 `S0-S17`、16 个输入、18 个输出、状态图、状态转移表、故障报警状态 `11111` 和基于传感器的排液/冲洗/复位条件，是非常稳的医疗设备控制双 A 样本。

## 条目 1: Peritoneal-Dialysis Flush-Fill-Dwell-Drain Supervisor

- 控制对象：医疗设备领域的自动腹膜透析机流程监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用有限状态机管理腹膜透析准备、加热、灌注、排液、冲洗、浊度判定和故障报警的医疗设备控制器。
- 判断：算。原文不仅声明采用 FSM，还给出状态图、I/O 表、状态转移表和故障/危险值分支，证据完整。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The proposed optimized process includes a flush stage, a turbidity sensor, and a LabVIEW finite state machine interface to track progress.

#### 摘录 B

- 出处：第 8-10 页，`State diagram / Input-output table`
> The state diagram covers all possible states; standby is `00000`, error alarm is `11111`, with 16 inputs and 18 outputs representing the design.

#### 摘录 C

- 出处：第 10-12 页，`State transition table`
> From standby, `S=1, DM=1, FM=0` goes to written instructions; `S=1, DM=0, FM=1` goes to flush; `F=1` goes to alarm; filling, draining, flush and turbidity branches are represented as state transitions.

### 2. 基于原文整理后的自然语言描述

The automated peritoneal-dialysis controller starts in standby state `00000` and branches according to the user's selected mode. If the start button is active and dialysis mode is selected, the FSM moves through written instructions, optional audible instructions, heater-on/heater-off preparation, and then the filling state once temperature and start-dialysis conditions are satisfied. During filling, flow, level, and pressure inputs determine whether the machine stays in filling or moves to filling end, downward movement, draining start, draining end, loop, and valve-control states. A separate flush mode can be selected from standby and is also reached after dialysis valve-control steps, allowing the tubing to be rinsed as part of the optimized process. The turbidity sensor controls the final branch: high turbidity loops the machine back to heater-on for another dialysis cycle, while low turbidity returns the system to standby; any danger value or fault drives the system to the error alarm state `11111`, which halts the system and alerts the user.

### 3. 逐句溯源

1. 句子 1：The automated peritoneal-dialysis controller starts in standby state `00000` and branches according to the user's selected mode.
   对应摘录：B, C
2. 句子 2：If the start button is active and dialysis mode is selected, the FSM moves through written instructions, optional audible instructions, heater-on/heater-off preparation, and then the filling state once temperature and start-dialysis conditions are satisfied.
   对应摘录：B, C
3. 句子 3：During filling, flow, level, and pressure inputs determine whether the machine stays in filling or moves to filling end, downward movement, draining start, draining end, loop, and valve-control states.
   对应摘录：B, C
4. 句子 4：A separate flush mode can be selected from standby and is also reached after dialysis valve-control steps, allowing the tubing to be rinsed as part of the optimized process.
   对应摘录：A, C
5. 句子 5：The turbidity sensor controls the final branch: high turbidity loops the machine back to heater-on for another dialysis cycle, while low turbidity returns the system to standby; any danger value or fault drives the system to the error alarm state `11111`, which halts the system and alerts the user.
   对应摘录：B, C
