# Battery management system enhancement for lithium-ions battery cells using switched shunt resistor approach based on finite state machine control algorithm - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把锂电 BMS 的 `ISO / CHG` 两套故障恢复逻辑明确写成 FSM，并给出 fault boolean、cool-down 计数、safety test 和 shunt 配合充电的完整闭环，可直接作为高质量过程控制样本。

## 条目 1: ISO-CHG Fault-Recovery Battery BMS Supervisor

- 控制对象：过程与环境控制领域的锂离子电池组 BMS 充放隔离与故障恢复监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向多节锂电池组的 BMS supervisor，用 `ISO` 与 `CHG` 两个 MOSFET 状态机管理充放电隔离、故障锁断、冷却计数和重新接入。
- 判断：算。对象是真实电池管理控制器，不是纯电路说明；原文明确给出两套 FSM、故障条件组合、`n=100` cool-down 计数、safety test 与过压场景下的 repeated disconnect/reconnect 行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Introduction
> In detail, an algorithm for controlling the shunt resistors is proposed by the present paper which is based on the use of finite state machines (FSM). This algorithm is applicable to the enhancement of the battery management system of lithium-ion battery cells, which are equipped with shunt resistors.

#### 摘录 B

- 出处：第 8-9 页，Figure `7` / Section `3`
> FIGURE 7 (A). Isolation (ISO) control finite state machine, (B). Charging (CHG) control finite state machine.
>
> Cell voltage, current and temperature are identified as critical parameters for safety. This is implemented in the BMS with five fault conditions checked by the MCU, if any of the conditions occur, either ISO or CHG will be switched off according to the finite state machine models illustrated in Figure 7A, B. The Boolean fault conditions are: over voltage, under voltage, over charge current, over discharge current, and over temperature. These are combined into the values CHGFAULT = Over Voltage | Over Charge Current | Over Temperature and ISOFAULT = Under Voltage | Over Discharge Current | Over Temperature.

#### 摘录 C

- 出处：第 9-10 页，Section `3`
> The finite state machines (FSMs) in Figures 8A, B determine how the BMS handles various combinations of fault conditions. ... The variables ISOcount and CHGcount provide a cool-down period after a fault before the checks if the fault has been resolved. This system allows the BMS to protect itself from harm, while still recovering from temporary faults. When a new fault occurs, ISOcount and CHGcount are set to their maximum value, n (100). After which, the variables count down until the safety test is performed. If a fault occurs when the count has not yet been cleared, the countdown is reset to n−1.

#### 摘录 D

- 出处：第 12 页，Section `4 Results and discussions`
> 4200 mV and 4150 mV represent the maximum safe voltage and the minimum charged threshold respectively. ... when cell B4 reaches the maximum voltage before the battery is fully charged, a fault condition is activated and the charger is disconnected for the cool down period. This fault condition is triggered four times. ... during the cool down period it applied the shunt resistors to cell B4 to discharge it before charging recommenced.

### 2. 基于原文整理后的自然语言描述

The battery-management supervisor is implemented as two coupled finite-state machines, one controlling the isolation path (`ISO`) and the other controlling the charging path (`CHG`), so the pack can be actively disconnected, tested, and reconnected after temporary faults. Both machines monitor cell voltage, current, and temperature and derive the composite guard variables `ISOFAULT` and `CHGFAULT` from under-voltage, over-voltage, over-current, and over-temperature conditions. When a fault is detected, the corresponding path is switched off, `ISOcount` or `CHGcount` is loaded with the cool-down horizon `n = 100`, and the controller moves through countdown and safety-test states before attempting reconnection; if another fault arrives before the countdown clears, the counter is reset to `n-1`. In the charging machine, the enabled branch is further guarded by charging thresholds such as `V < V_TH` and `0 < I < I_TH`, so charging is only resumed when both the fault flag and terminal conditions are safe. The result traces show the intended behavior in operation: repeated over-voltage on cell `B4` disconnects charging, activates the cool-down phase, applies shunt discharge to the critical cell, and only then recommences charging.

### 3. 逐句溯源

1. 句子 1：The battery-management supervisor is implemented as two coupled finite-state machines, one controlling the isolation path (`ISO`) and the other controlling the charging path (`CHG`), so the pack can be actively disconnected, tested, and reconnected after temporary faults.
   对应摘录：A, B
2. 句子 2：Both machines monitor cell voltage, current, and temperature and derive the composite guard variables `ISOFAULT` and `CHGFAULT` from under-voltage, over-voltage, over-current, and over-temperature conditions.
   对应摘录：B
3. 句子 3：When a fault is detected, the corresponding path is switched off, `ISOcount` or `CHGcount` is loaded with the cool-down horizon `n = 100`, and the controller moves through countdown and safety-test states before attempting reconnection; if another fault arrives before the countdown clears, the counter is reset to `n-1`.
   对应摘录：C
4. 句子 4：In the charging machine, the enabled branch is further guarded by charging thresholds such as `V < V_TH` and `0 < I < I_TH`, so charging is only resumed when both the fault flag and terminal conditions are safe.
   对应摘录：B, C
5. 句子 5：The result traces show the intended behavior in operation: repeated over-voltage on cell `B4` disconnects charging, activates the cool-down phase, applies shunt discharge to the critical cell, and only then recommences charging.
   对应摘录：D
