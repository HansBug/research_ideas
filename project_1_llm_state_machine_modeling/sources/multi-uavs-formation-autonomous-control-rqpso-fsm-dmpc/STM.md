# Multi-UAVs Formation Autonomous Control Method Based on RQPSO-FSM-DMPC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多无人机编队的五种 formation mode、九个 trigger event 以及雷达 / no-fly threat 下的重构职责写得很集中，是很清楚的 formation manager 样本。

## 条目 1: Five-mode UAV formation manager

- 控制对象：多无人机编队重构任务中的 formation management unit
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据威胁信息、任务命令和编队约束在 `S1-S5` 五种 formation mode 之间切换，并把下一个 mode 交给 DMPC 控制器的多无人机编队管理器。
- 判断：算。对象是真实编队控制中的离散 mode manager，不是单纯优化器；原文给出了状态集合、触发事件集合、状态图和典型 threat-driven transition 语义。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要，`paper_content.txt` 第 11-16 行
> For various threats in the enemy defense area ... the unmanned aerial vehicles formation needs to be reconfigured ... By establishing the virtual-leader formation model, this paper puts forward distributed model predictive control and finite state machine formation manager ... Simulation result shows that this algorithm can control multiple UAVs formation autonomous reconfiguration effectively and achieve covert penetration safely.

#### 摘录 B

- 出处：第 6-7 页，Section `5.2 Design of Formation Control Manager Based on FSM`，`paper_content.txt` 第 393-437 行
> FSM formation management unit will make the formation mode of the next step and transfer it to DMPC formation controller ...
>
> we can determine five models of UAV formation as follows: free formation flight S1; forming the initial formation S2; keeping the formation S3; formation reconfiguration S4; formation avoidance control S5.
>
> the switching condition (trigger event) ... I1 ... I2 ... I3 ... I4 ... I5 ... I6 ... I7 ... I8 ... I9.

#### 摘录 C

- 出处：第 7 页，Figure 7 与同节说明，`paper_content.txt` 第 428-445 行
> Figure 7: FSM state transition diagram.
>
> When UAVs formation arrives in the target zone and finds the early warning radar threat or air defense radar threat ... the overall formation transforms the formation based on this UAV and reference trajectory point ...
>
> Assuming that the initial state of formation is S3, when a certain UAV ... detects the early warning radar or air defense radar, the formation goes into S4 ... the other UAVs in the formation will also carry on real-time resolving to obtain the desired formation parameters.

### 2. 基于原文整理后的自然语言描述

The formation management unit receives neighbouring-UAV states, environmental threat information, mission commands, and reference-trajectory coordinates, and it chooses the next formation mode before the DMPC controller produces the concrete control signals. The machine defines five explicit states: `S1` free formation flight, `S2` forming the initial formation, `S3` keeping the formation, `S4` formation reconfiguration, and `S5` formation avoidance control. Its trigger alphabet covers formation command `I1`, constraint satisfaction `I2`, fixed obstacle or no-fly detection `I3`, obstacle cleared `I4`, join and leave events `I5/I6`, cooperative-task start and end `I7/I8`, and the formation-dissolution command `I9`, with Figure `7` giving the transition graph among these modes. When the formation encounters early-warning or air-defense radar, the manager moves from the normal keeping mode into `S4`, selects the UAV nearest to the radar to perform interference, and reconfigures the rest of the team around that UAV and the reference trajectory. When the team detects a no-fly zone or obstacle, the controller switches into the avoidance mode and reorganizes the formation around the threat geometry, so the paper exposes a full five-mode formation-reconfiguration FSM rather than only an optimization cost function.

### 3. 逐句溯源

1. 句子 1：The formation management unit receives neighbouring-UAV states, environmental threat information, mission commands, and reference-trajectory coordinates, and it chooses the next formation mode before the DMPC controller produces the concrete control signals.
   对应摘录：B
2. 句子 2：The machine defines five explicit states: `S1` free formation flight, `S2` forming the initial formation, `S3` keeping the formation, `S4` formation reconfiguration, and `S5` formation avoidance control.
   对应摘录：B
3. 句子 3：Its trigger alphabet covers formation command `I1`, constraint satisfaction `I2`, fixed obstacle or no-fly detection `I3`, obstacle cleared `I4`, join and leave events `I5/I6`, cooperative-task start and end `I7/I8`, and the formation-dissolution command `I9`, with Figure `7` giving the transition graph among these modes.
   对应摘录：B, C
4. 句子 4：When the formation encounters early-warning or air-defense radar, the manager moves from the normal keeping mode into `S4`, selects the UAV nearest to the radar to perform interference, and reconfigures the rest of the team around that UAV and the reference trajectory.
   对应摘录：A, C
5. 句子 5：When the team detects a no-fly zone or obstacle, the controller switches into the avoidance mode and reorganizes the formation around the threat geometry, so the paper exposes a full five-mode formation-reconfiguration FSM rather than only an optimization cost function.
   对应摘录：A, B, C
