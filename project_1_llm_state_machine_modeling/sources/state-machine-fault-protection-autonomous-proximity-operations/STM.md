# STATE MACHINE FAULT PROTECTION FOR AUTONOMOUS PROXIMITY OPERATIONS - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把火星样本回收近距离接近与捕获的 fault-protection 行为写成显式 mission-phase state machine，既有 nominal/abort 链，又有 `30-45 min / 5 min / 2 min` 的风险分区时间窗口。

## 条目 1: Rendezvous-and-capture fault-protection supervisor

- 控制对象：航空航天与飞行/空管控制领域的自主近距离接近与捕获 fault-protection 监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于 Mars Sample Return 近距离接近与样本捕获任务的 fault-protection mission supervisor，按风险区间切换 standby、abort、capture 和 locate-object 行为。
- 判断：算。对象是实际航天器 `GN&C` 近距操作中的 fault-protection system，而不是一般架构综述；原文明确给出 mission zones、状态集合、进入条件、abort 返回链和 capture 失败后的 `Locate OS` 恢复逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 9 页，zones of criticality，`paper_content.txt` 第 467-483 行
> The first zone is called the “passive miss region”. During this zone the SRO must constantly thrust to remain on an intercept course with the OS.
>
> Zone 1 should last about 30-45 minutes and the distance to the target will close from 50 m to about 20 m.
>
> The second zone is called the “active abort region” ... Zone 2 should last around 5 minutes, and the distance from the target will close from 20 m to about 5 m.
>
> The third zone is called the “unavoidable intercept region” ... Zone 3 should last around 2 minutes and the distance from the target will close from 5 m to zero.

#### 摘录 B

- 出处：第 9 页，state-machine introduction，`paper_content.txt` 第 484-491 行
> The rendezvous process was developed into a state machine that will be used by the fault protection system to determine how to respond to various faults as they are detected.
>
> Fault responses will be calibrated based on the relative risk to the mission in each zone.
>
> The state machine ... represents both nominal and off-nominal processes. The system begins in Passive Standby ...

#### 摘录 C

- 出处：第 10 页，nominal and abort transitions，`paper_content.txt` 第 503-527 行
> This is a passively stable trajectory that will not impact the OS even if it drifts.
>
> When proper lighting and communication conditions are achieved and the OS has been acquired by all rendezvous sensors, the “closed-loop” approach will begin. The system then enters the “Passive Miss Region”.
>
> If at any point in this region something goes wrong, the system simply stops maneuvers and enters Passive Abort ... it would return to the Passive Standby state ...
>
> If no problems occur, the system will enter the “Active Abort Region” ... If at any point something goes wrong, an abort can be commanded to return to Passive Standby via the Active Abort mode. Finally, just before intercept the system enters the “Unavoidable Intercept Region”.

#### 摘录 D

- 出处：第 10 页，capture-failure recovery，`paper_content.txt` 第 528-539 行
> If capture is unsuccessful and the OS does not enter the capture volume, the system enters the “Locate OS” state.
>
> It will attempt to determine where the OS is located before performing any slew or thrust maneuvers.
>
> Once the OS is found, an abort maneuver is commanded.
>
> If the OS cannot be confirmed inside the capture volume after the door has closed, the system also enters the LocateOS state and will abort unless the OS is found inside the capture volume.

### 2. 基于原文整理后的自然语言描述

The proximity-operations fault-protection logic is organized as a mission-phase state machine rather than as a flat threshold alarm system. It starts from `Passive Standby`, can optionally execute a `Final Hop`, and then enters the closed-loop rendezvous process through the `Passive Miss Region` once lighting, communication, and sensor-acquisition conditions are satisfied. Fault handling is phase-sensitive: in the `Passive Miss Region` a fault causes `Passive Abort` and return to standby, in the `Active Abort Region` an explicit abort maneuver can still avoid intercept, and in the `Unavoidable Intercept Region` the vehicle must either capture the sample or collide. These regions are separated by concrete mission windows of roughly `30-45 min` from `50 m` to `20 m`, `5 min` from `20 m` to `5 m`, and `2 min` from `5 m` to `0 m`. If capture fails or the object is not confirmed inside the capture volume after door closure, the machine transitions to `Locate OS`, searches before any slew or thrust maneuver, and commands an abort unless the object is found inside the capture volume.

### 3. 逐句溯源

1. 句子 1：The proximity-operations fault-protection logic is organized as a mission-phase state machine rather than as a flat threshold alarm system.
   对应摘录：B
2. 句子 2：It starts from `Passive Standby`, can optionally execute a `Final Hop`, and then enters the closed-loop rendezvous process through the `Passive Miss Region` once lighting, communication, and sensor-acquisition conditions are satisfied.
   对应摘录：B, C
3. 句子 3：Fault handling is phase-sensitive: in the `Passive Miss Region` a fault causes `Passive Abort` and return to standby, in the `Active Abort Region` an explicit abort maneuver can still avoid intercept, and in the `Unavoidable Intercept Region` the vehicle must either capture the sample or collide.
   对应摘录：A, C
4. 句子 4：These regions are separated by concrete mission windows of roughly `30-45 min` from `50 m` to `20 m`, `5 min` from `20 m` to `5 m`, and `2 min` from `5 m` to `0 m`.
   对应摘录：A
5. 句子 5：If capture fails or the object is not confirmed inside the capture volume after door closure, the machine transitions to `Locate OS`, searches before any slew or thrust maneuver, and commands an abort unless the object is found inside the capture volume.
   对应摘录：D
