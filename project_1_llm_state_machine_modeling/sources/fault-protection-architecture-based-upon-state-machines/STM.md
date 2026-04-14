# Development of a Fault Protection Architecture Based Upon State Machines - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把航天器故障保护写成 Stateflow 状态机，并给出 `Normal / PotentialFault / Fault` 的嵌套检测链、`FaultPersistence / ResolutionPersistence` 持续时间门槛以及飞行试验里的故障置位/恢复结果，满足双 A。

## 条目 1: Vibration Fault Detection and Recovery Stateflow Supervisor
- 控制对象：航空航天与飞行控制领域的 UAV/航天器故障保护体系中的振动故障检测与恢复监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个把机载振动监测结果送入 Stateflow 的故障检测与恢复监督器，用嵌套状态和持续时间门槛判定 `Normal`、`PotentialFault` 与 `Fault`，并把故障状态反馈回飞行系统。
- 判断：算。对象是实际航空器故障保护链的一部分，原文明确写出了状态、子状态、触发条件、持续时间 guard、输出标志和飞行试验中的恢复过程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 20-33 行
> This paper describes ... an architecture that utilizes state machines for Fault Detection, Isolation, and Recovery. Through the application of state machine logic, the architecture actively responds to hardware and software faults, allowing autonomous recovery to a safe state. ... The fault protection architecture is developed as a Stateflow block ... Based on that state, the fault protection algorithms determine if any faults are present ... and command actions to contain or prevent further faults.

#### 摘录 B
- 出处：第 8-9 页，`3.3 Vibration Detection Flight Test Results / Fig. 12`，`paper_content.txt` 第 497-523 行
> This FaultDetected flag is fed into the Stateflow diagram shown in Figure 12. ... The Stateflow diagram for vibration fault detection in Figure 12 begins with an initial state of “Normal” at the bottom right and an initial substate of “Standby”. If FaultDetected is set to 1, the substate within “Normal” transitions to “PotentialFault.” If the condition FaultDetected==1 persists for a length of time specified by FaultPersistence, then the state transitions from “Normal” to “Fault”. ... transitioning from “Fault” back to “Normal”: the condition FaultDetected==0 must persist for a length of time specified by ResolutionPersistence. The FaultStatus flag ... with 0 indicating “Normal” and 1 indicating “Fault”.

#### 摘录 C
- 出处：第 9-10 页，`3.3 Vibration Detection Flight Test Results / Fig. 14`，`paper_content.txt` 第 548-575 行
> ... The nervous system quickly detects the imbalance and outputs a FaultStatus of 1 at around 10 sec ... around 25 sec, the nervous system detects that balance has been restored and sets FaultStatus to 0. ... near 35 sec, a FaultStatus of 1 occurs ... The tape ... flies off at 40 sec. The copter transitions to balanced flight in segment G, which the nervous system detects around 45 sec, returning FaultStatus to 0. The delays in FaultStatus transitions are expected ...

### 2. 基于原文整理后的自然语言描述

The paper instantiates its fault-protection architecture as a Stateflow supervisor that receives state measurements, determines whether a fault is present, and issues containment or recovery commands back to the vehicle model. For the vibration case study, the controller consumes a `FaultDetected` flag derived from KNN classification of accelerometer data and feeds it into a nested Stateflow chart whose initial state is `Normal` and whose initial substate is `Standby`. If `FaultDetected` becomes `1`, the chart first moves into the `PotentialFault` substate, and only when that condition persists for the duration `FaultPersistence` does the parent state escalate from `Normal` to `Fault`. The return path is equally explicit: the chart stays in `Fault` until `FaultDetected==0` persists for `ResolutionPersistence`, after which the system returns to `Normal`, while the output `FaultStatus` exports `0` for normal flight and `1` for faulted flight. The flight-test trace shows that the supervisor raises `FaultStatus` shortly after an intentionally unbalanced propeller is flown, clears it after balance is restored, raises it again when imbalance is reintroduced, and finally returns it to `0` after the propeller re-balances, with the delays explained by the persistence guards.

### 3. 逐句溯源

1. 句子 1：The paper instantiates its fault-protection architecture as a Stateflow supervisor that receives state measurements, determines whether a fault is present, and issues containment or recovery commands back to the vehicle model.
   对应摘录：A
2. 句子 2：For the vibration case study, the controller consumes a `FaultDetected` flag derived from KNN classification of accelerometer data and feeds it into a nested Stateflow chart whose initial state is `Normal` and whose initial substate is `Standby`.
   对应摘录：B
3. 句子 3：If `FaultDetected` becomes `1`, the chart first moves into the `PotentialFault` substate, and only when that condition persists for the duration `FaultPersistence` does the parent state escalate from `Normal` to `Fault`.
   对应摘录：B
4. 句子 4：The return path is equally explicit: the chart stays in `Fault` until `FaultDetected==0` persists for `ResolutionPersistence`, after which the system returns to `Normal`, while the output `FaultStatus` exports `0` for normal flight and `1` for faulted flight.
   对应摘录：B
5. 句子 5：The flight-test trace shows that the supervisor raises `FaultStatus` shortly after an intentionally unbalanced propeller is flown, clears it after balance is restored, raises it again when imbalance is reintroduced, and finally returns it to `0` after the propeller re-balances, with the delays explained by the persistence guards.
   对应摘录：C
