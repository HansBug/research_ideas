# Development of a network level crossing system - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把网络化道口控制器的双计数器、四种工作模式、启动自检链和网络/本地故障退化逻辑写得足够完整，可直接作为铁路道口 `EFSM + T0` 样本。

## 条目 1: Four-mode network-degraded railway crossing controller

- 控制对象：轨道交通与铁路控制领域的网络化道口四模式监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于相邻道口协同退化控制的网络化 level crossing controller，在正常、自身故障、网络故障和双故障条件下切换不同控制模式，并利用 conventional counter 与 approaching train number counter 管理列车位置。
- 判断：算。对象是实际铁路道口控制器，不是单纯 ICT 架构介绍；原文明确给出了四种控制模式、双计数器更新逻辑、模式进入条件以及开机后从自检到联网运行的切换链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 20-31 行
> Recent ICT (information communication technology) progress has been applied to solve our issues. We have developed a network level crossing system. More than three level crossing controllers are connected through the Ethernet LAN connection to exchange their operational data. At normal state, they are operating as stand-alone machines, once one controller detects a problem, it operates not by means of its own data but by another controller’s data. As a result, by a degraded level crossing function, passers by need not undergo unnecessary extensive warning.

#### 摘录 B

- 出处：第 4-5 页，`3.1 Managing the train location`，`paper_content.txt` 第 151-167 行
> A conventional level crossing checks train locations using a train number counter that indicates the number of trains in the control area of the level crossing.
>
> In order to overcome this problem, we have developed a new level crossing controller which has two train counters. One is the same counter as a current level crossing controller and the other is a new counter named approaching train number counter which can manage the number of trains running in the area between adjacent level crossings on both sides.
>
> Moreover, when a level crossing detects that it has failed, the system changes into a degraded mode using the approaching train counter.

#### 摘录 C

- 出处：第 5-6 页，`3.2 Four status of a network level crossing system`，`paper_content.txt` 第 213-218、268-291 行
> The level crossing controller has four modes in accordance with status of itself and the network (the controller is normal/abnormal state and normal/abnormal obtaining of data of adjacent level crossings via the network).
>
> (a) Network Mode (Level crossing controller is normal and Network is normal) ... the level crossing controller is operating as a stand-alone device, and constantly obtains information of the adjacent level crossings to operate the degraded logics in the background to assure safety even while the system is operating normally.
>
> (b) Degraded Mode (Level crossing controller is abnormal and Network is normal) ... using the approaching train number counter ... the system assures safe control by performing train location management the same as with conventional control.
>
> (c) Local Mode (Level crossing controller is normal and Network is abnormal) ... our system not to perform incorrect mode transition that may result in a dangerous situation.
>
> (d) Failure Mode (Level crossing controller is abnormal and Network is abnormal) ... it makes/keeps warning to prevent dangerous results.

#### 摘录 D

- 出处：第 6 页，mode transition chart 说明，`paper_content.txt` 第 292-300 行
> We defined four control modes to secure safety and investigated individual transition conditions. Figure 4 shows the mode transition chart. The startup process firstly runs when the power switch is turned on and self-diagnosis runs simultaneously. Secondly, with good results of the startup process, the system shifts to Local Mode. Thirdly, after a health check of the network, it shifts to Network Mode that is expected as the usual status of the system and the level crossings. In the case of trouble or failure around the level crossing or the network, the system detects a failure part and changes its mode to the corresponding one.

### 2. 基于原文整理后的自然语言描述

The retained control object is a networked railway level-crossing controller that normally behaves as a stand-alone crossing but can fall back to adjacent crossings when its own detector or controller becomes unreliable. Its internal logic is extended with two counters: the conventional train-number counter for the local control area and an `approaching train number counter` that is maintained from neighboring crossings so the degraded controller can still infer train presence between adjacent sites. The controller explicitly operates in four modes: `Network Mode`, where the crossing works locally while continuously receiving adjacent data in the background; `Degraded Mode`, where a failed local controller switches to the approaching-train counter and keeps the same safety objective as conventional control; `Local Mode`, where the local controller is healthy but network information is abnormal and unsafe mode transitions are blocked; and `Failure Mode`, where both local and network information are unreliable so the system keeps warning continuously. Startup is also part of the control chain: power-on self-diagnosis first leads to `Local Mode`, then a successful network health check promotes the system to `Network Mode`, and later controller-side or network-side faults drive the machine into the corresponding fallback mode. Taken together, the paper exposes a concrete railway-crossing EFSM in which counter values and network health determine the admissible control mode and the warning policy.

### 3. 逐句溯源

1. 句子 1：The retained control object is a networked railway level-crossing controller that normally behaves as a stand-alone crossing but can fall back to adjacent crossings when its own detector or controller becomes unreliable.
   对应摘录：A, C
2. 句子 2：Its internal logic is extended with two counters: the conventional train-number counter for the local control area and an `approaching train number counter` that is maintained from neighboring crossings so the degraded controller can still infer train presence between adjacent sites.
   对应摘录：B
3. 句子 3：The controller explicitly operates in four modes: `Network Mode`, where the crossing works locally while continuously receiving adjacent data in the background; `Degraded Mode`, where a failed local controller switches to the approaching-train counter and keeps the same safety objective as conventional control; `Local Mode`, where the local controller is healthy but network information is abnormal and unsafe mode transitions are blocked; and `Failure Mode`, where both local and network information are unreliable so the system keeps warning continuously.
   对应摘录：C
4. 句子 4：Startup is also part of the control chain: power-on self-diagnosis first leads to `Local Mode`, then a successful network health check promotes the system to `Network Mode`, and later controller-side or network-side faults drive the machine into the corresponding fallback mode.
   对应摘录：D
5. 句子 5：Taken together, the paper exposes a concrete railway-crossing EFSM in which counter values and network health determine the admissible control mode and the warning policy.
   对应摘录：A, B, C, D
