# Power dispatching techniques as a finite state machine for a standalone photovoltaic system with a hybrid energy storage - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把独立光伏混合储能系统的功率调度明确拆成 `WMC -> PFC -> SWC` 层次链，并在 `Hybrid / Battery only / Disconnected` 及其子状态上给出基于 `SOC`、负载与功率上限的状态转移逻辑。

## 条目 1: Hybrid-Battery-Disconnected Dispatching Supervisor

- 控制对象：独立光伏混合储能系统的分层功率调度控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个为独立光伏系统中电池与超级电容混合储能单元分配功率份额的层次式 supervisor，上层决定工作模式，下层再细分可完全供电、受限供电或断开。
- 判断：算。对象是真实能量管理控制器，而不是纯性能优化公式；原文给出了 `Hybrid / Battery only / Disconnected` 及其子状态、转移条件和功率引用更新规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 22-28 行
> This paper presents innovative power management and control strategies for a HES connected in DC coupled architecture. ... Power management strategies are developed in a hierarchical architecture as an event driven finite state machine. Primary control is implemented using current mode control and voltage mode control adapted at the bi-directional DC-DC converters and the voltage source inverter connected to the HES, respectively.

#### 摘录 B

- 出处：第 6-7 页，`2.4 Control system overview` 与 `3.1. Working mode control (WMC)`，`paper_content.txt` 第 206-211 行与第 238-260 行
> The power dispatching strategies are designed in hierarchical fashion as an event driven system with PID and state-flow control. ... the control system includes four stages each having their own control task depend on the hierarchical position ... At this stage, the availability and the accessibility of each ES element for power dispatching are determined based on their SOC. ... h: Hybrid mode. b: Battery only mode d: Disconnected mode ... T11 SOCbat(t)>SOCbat,min && SOCsc(t)<SOCsc,min ... T12 SOCbat(t)>SOCbat,min && SOCsc(t)>SOCsc,min ... T13 ... T14 ...

#### 摘录 C

- 出处：第 7-9 页，`3.2. Power Flow Control (PFC) of the HES`，`paper_content.txt` 第 263-304 行
> Power will be delivered to the load only in the ‘Hybrid’ and ‘Battery only’ modes. ... The ‘Hybrid’ mode ... consists of three states: ‘Fully dispatchable’, ‘Limited’ and ‘Disconnected’. ... When the calculated battery power share ... is higher than the maximum allowable capacity of the battery, the system transits to the limited state ... There are two states in the PFC of the ‘Battery only’ mode: ‘Connected’ and ‘Disconnected’ where only the battery array takes care of the load demand ... otherwise the system transits to disconnected.

### 2. 基于原文整理后的自然语言描述

The hybrid energy-storage controller is organized as a hierarchical finite-state machine in which the top `Working Mode Control` layer first selects whether the standalone PV system operates in `Hybrid`, `Battery only`, or `Disconnected` mode based on the current state of charge of the battery and supercapacitor. When both storage elements are available, the system enters `Hybrid`; if only the battery remains dispatchable it falls back to `Battery only`; and if the availability constraints are violated it moves to `Disconnected`. Inside `Hybrid`, the `Power Flow Control` layer refines the mode into `Fully dispatchable`, `Limited`, or `Disconnected` according to whether the combined storage power can meet the load and whether the calculated battery or supercapacitor shares exceed their maximum ratings. In `Limited`, the battery reference is clipped to a predetermined fraction and the supercapacitor supplies the remainder, while in `Battery only` the substate collapses to `Connected` or `Disconnected` depending on whether battery capacity still covers the load. The lowest switching layer then turns those references into PWM commands for the bidirectional converters and inverter, so the discrete supervisor is tightly coupled to continuous power variables such as `SOC`, load demand, and converter limits.

### 3. 逐句溯源

1. 句子 1：The hybrid energy-storage controller is organized as a hierarchical finite-state machine in which the top `Working Mode Control` layer first selects whether the standalone PV system operates in `Hybrid`, `Battery only`, or `Disconnected` mode based on the current state of charge of the battery and supercapacitor.
   对应摘录：A, B
2. 句子 2：When both storage elements are available, the system enters `Hybrid`; if only the battery remains dispatchable it falls back to `Battery only`; and if the availability constraints are violated it moves to `Disconnected`.
   对应摘录：B
3. 句子 3：Inside `Hybrid`, the `Power Flow Control` layer refines the mode into `Fully dispatchable`, `Limited`, or `Disconnected` according to whether the combined storage power can meet the load and whether the calculated battery or supercapacitor shares exceed their maximum ratings.
   对应摘录：C
4. 句子 4：In `Limited`, the battery reference is clipped to a predetermined fraction and the supercapacitor supplies the remainder, while in `Battery only` the substate collapses to `Connected` or `Disconnected` depending on whether battery capacity still covers the load.
   对应摘录：C
5. 句子 5：The lowest switching layer then turns those references into PWM commands for the bidirectional converters and inverter, so the discrete supervisor is tightly coupled to continuous power variables such as `SOC`, load demand, and converter limits.
   对应摘录：A, B, C
