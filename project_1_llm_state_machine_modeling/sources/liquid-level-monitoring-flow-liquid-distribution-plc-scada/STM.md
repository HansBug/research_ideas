# Liquid Level Monitoring and Flow based Liquid Distribution System using PLC and SCADA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把选定目标、开阀启泵、按流量累积完成、以及多种中途故障触发自动暂停再重启的控制链写得很明确，足以形成高质量液体转运样本。

## 条目 1: Flow-Interlocked Liquid Transfer and Pause-Recovery Supervisor

- 控制对象：液位/流量联锁的液体转运阀泵监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的液体分配控制器，根据目标容器、设定转运量、液位/流量联锁和阀门反馈来控制开阀、启泵、暂停、恢复和完成。
- 判断：算。对象是真实工艺转运控制器，原文明确给出 auto 模式下的按钮序列、阀泵动作、暂停触发条件、恢复方式和流量累计完成条件，不是单纯传感器展示稿。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`Algorithm`，`paper_content.txt` 第 218-245 行
> Click on Auto button from SCADA screen to keep the system in Auto mode.
>
> Then select the Transferring button ... Select the destination ... Enter the set quantity ...
>
> If all the interlocks satisfied then operations will confirmed otherwise doesn’t confirmed.
>
> If operation confirmed then click on Start button.
>
> Observe destination, dispensing, suction solenoid valves are opened followed by pump starts running to transfer the liquid/solvent from source tank to destination.
>
> After transferring ... the given set quantity then operation completed automatically and opened valves are closed and pump stops.

#### 摘录 B

- 出处：第 3 页，`Algorithm`，`paper_content.txt` 第 235-245 行
> If Level in source tank decreases and flow sensor in line senses the liquid/solvent flow then operation remains continues otherwise operation will be paused automatically. That means all the opened valves are closed and pump stops.
>
> While liquid/solvent pumping, when flow sensor totalizes the flow rate equivalent to the given set quantity then operation completed automatically and opened valves are closed and pump stops.

#### 摘录 C

- 出处：第 7-8 页，`Interlock enabled then pause screen`，`paper_content.txt` 第 446-468 行
> If any one of the following deviation occurs in the middle of the process then the process will be paused.
> • If there is no change in the storage tank level and if there is no change in the line flow.
> • If pump dry run or tripped or failed.
> • If any one of the dispensing valves open feedback is not received to PLC or valve fails.
> • During dispensing ... any one of other valve is opened manually from field (override).
> • If liquid level/Level switch in the storage tank goes low.
>
> The enabled interlock displayed on SCADA operating screen. It must be corrected ... Then user comes back and process start again by click on start button.

### 2. 基于原文整理后的自然语言描述

The liquid-distribution supervisor begins in auto mode after the operator chooses a transfer destination and enters the requested quantity on the SCADA screen. If all pre-check interlocks are satisfied, the controller opens the suction, dispensing, and destination valves and then starts the pump to move liquid from the source tank to the selected receiver. The transfer is allowed to continue only while source level is decreasing and the line flow sensor confirms that liquid is moving; otherwise the controller pauses automatically by closing the opened valves and stopping the pump. Additional pause triggers include pump trip or dry run, missing valve-open feedback, manual override of other valves, and low source-tank level, after which the user must correct the interlock and restart the process. When the flow totalizer reaches the requested transfer quantity, the supervisor turns the pump off, closes the valves, and ends the operation as a completed transfer.

### 3. 逐句溯源

1. 句子 1：The liquid-distribution supervisor begins in auto mode after the operator chooses a transfer destination and enters the requested quantity on the SCADA screen.
   对应摘录：A
2. 句子 2：If all pre-check interlocks are satisfied, the controller opens the suction, dispensing, and destination valves and then starts the pump to move liquid from the source tank to the selected receiver.
   对应摘录：A
3. 句子 3：The transfer is allowed to continue only while source level is decreasing and the line flow sensor confirms that liquid is moving; otherwise the controller pauses automatically by closing the opened valves and stopping the pump.
   对应摘录：B
4. 句子 4：Additional pause triggers include pump trip or dry run, missing valve-open feedback, manual override of other valves, and low source-tank level, after which the user must correct the interlock and restart the process.
   对应摘录：C
5. 句子 5：When the flow totalizer reaches the requested transfer quantity, the supervisor turns the pump off, closes the valves, and ends the operation as a completed transfer.
   对应摘录：A, B, C
