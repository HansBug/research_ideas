# Turning Base Transceiver Stations into Scalable and Controllable DC Microgrids Based on a Smart Sensing Strategy - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把基站直流微电网 EMS 写成 `6` 状态有限状态机，包含 tariff 切换、SOC/PV 阈值、`30 s` 过渡态和 `15 min` 平均光伏功率判断，细节足以形成双 A 的过程控制样本。

## 条目 1: Tariff-and-PV-Aware BTS Microgrid EMS
- 控制对象：过程与环境控制领域的基站直流微电网能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个协调电网、光伏、BESS 与非关键负载的基站直流微电网 EMS，用 tariff、SOC、PV 阈值和停电影响来切换供能状态。
- 判断：算。对象是真实电信基站能量管理控制器；原文直接给出状态集合、优先级规则、正常运行转移表和带 `30 s / 15 min` 的时间性 guard，不是只有 mode 名称的粗粒度框图。

### 1. 原文摘录

#### 摘录 A
- 出处：第 14 页，Section `3.4.2. Energy Management System`
> The following states provide an optimal solution for the operation of the BTS while at the same time making an efficient use of the BESS:
> State 0 or Back-up State ...
> State 1 or Transition State (Peak Tariff) or Battery Charging State (Off-Peak Tariff): this state is used as a transition state in the case of working in the Peak tariff period. The BTS remains in this state for a maximum of 30 s. During the Off-peak tariff period, this state is used to charge the battery.
> State 2 or No Battery State ...
> State 3 or Battery Discharging State ...
> State 4 or Island State ...
> State 5 or Cloud State ...

#### 摘录 B
- 出处：第 14-15 页，Section `3.4.2. Energy Management System` 与 `Table 1`
> Three levels of priority are established, in the state transition:
> (1) Very High Priority: In the event of a grid outage, the state is immediately changed from any state to State 0 or Back-up State. When the outage is over, the FSM enters State 1 or Transition State.
> (2) High Priority: If there is a change from the off-peak tariff period to the peak tariff period or vice versa, there is a transition from any state to State 1 or Transition State.
> (3) Normal Priority: Common EMS operation with grid available and operating within one of the working periods.
>
> State 1 ... PT&&SOC<SOC min || OT&&SOC>SOC max -> 2
> PT&&PV<THPV&&SOC>SOC min -> 3
> PT&&PV>=THPV&&SOC>SOC min -> 4

#### 摘录 C
- 出处：第 15-16 页，`Table 1` 与随后的解释段落
> PV, average PV over the last 15 min: this is used to determine the continuity of the PV drop.
>
> It is important to note that all state transitions in this mode of operation are made by applying hysteresis to the PV thresholds of state switching to ensure as few transitions as possible, thus avoiding high-frequency state changes. Following this approach, the Cloud State is implemented to prevent that if a drop in PV production is produced by an occasional cloud, no reconnection to the grid takes place.

### 2. 基于原文整理后的自然语言描述

The BTS microgrid controller is organized as a six-state EMS with `Back-up`, `Transition/Battery Charging`, `No Battery`, `Battery Discharging`, `Island`, and `Cloud` states that coordinate grid supply, PV generation, battery usage, and non-critical-load shedding. Its transition logic is priority-ordered: any grid outage immediately forces the system from any current state into `State 0`, any PT/OT tariff change forces a jump into `State 1`, and only when those two higher-priority events are absent does the controller evaluate the normal-priority switching table. Under normal priority, `State 1` acts as the gateway state and uses tariff, SOC, and PV thresholds to decide whether the system should disconnect the battery (`State 2`), discharge it to support loads (`State 3`), or move into islanded PV-plus-BESS operation (`State 4`). The timing semantics are explicit rather than implicit: the peak-period transition state lasts at most `30 s`, and the cloud-protection logic checks the average PV power over the last `15 min` instead of reacting to instantaneous fluctuations. Hysteresis around the PV thresholds and the dedicated `Cloud State` prevent rapid state oscillation and unnecessary reconnection to the grid when PV briefly dips because of passing clouds.

### 3. 逐句溯源

1. 句子 1：The BTS microgrid controller is organized as a six-state EMS with `Back-up`, `Transition/Battery Charging`, `No Battery`, `Battery Discharging`, `Island`, and `Cloud` states that coordinate grid supply, PV generation, battery usage, and non-critical-load shedding.
   对应摘录：A
2. 句子 2：Its transition logic is priority-ordered: any grid outage immediately forces the system from any current state into `State 0`, any PT/OT tariff change forces a jump into `State 1`, and only when those two higher-priority events are absent does the controller evaluate the normal-priority switching table.
   对应摘录：B
3. 句子 3：Under normal priority, `State 1` acts as the gateway state and uses tariff, SOC, and PV thresholds to decide whether the system should disconnect the battery (`State 2`), discharge it to support loads (`State 3`), or move into islanded PV-plus-BESS operation (`State 4`).
   对应摘录：B
4. 句子 4：The timing semantics are explicit rather than implicit: the peak-period transition state lasts at most `30 s`, and the cloud-protection logic checks the average PV power over the last `15 min` instead of reacting to instantaneous fluctuations.
   对应摘录：A, C
5. 句子 5：Hysteresis around the PV thresholds and the dedicated `Cloud State` prevent rapid state oscillation and unnecessary reconnection to the grid when PV briefly dips because of passing clouds.
   对应摘录：A, C
