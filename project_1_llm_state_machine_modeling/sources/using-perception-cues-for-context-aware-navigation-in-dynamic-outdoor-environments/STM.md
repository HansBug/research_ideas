# Using perception cues for context-aware navigation in dynamic outdoor environments - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 UGV 的高层 behavior executor 写成显式五态机，`NORMAL / PEDESTRIAN / THREAT` 之间的切换完全由感知 cue 驱动，状态、优先级、切换动作和取消/重发目标命令都写得很清楚，是 `⚙️` 方向很有代表性的监督控制样本。

## 条目 1: Context-aware behavior executor for dynamic UGV navigation

- 控制对象：通用控制领域的小型 UGV 上下文感知导航监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据 pedestrian 和 weapon cue 在 terrain-aware、socially compliant 与 covert 三类导航行为之间切换的 UGV 高层监督控制器。
- 判断：算。对象是实际地面无人车的导航监督器，而不是泛泛的智能架构图；原文明确给出行为执行状态机、五个离散状态、优先级规则、触发信号和进入各状态时取消/配置/下发新目标的动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> We discuss our approach to the integration of several context-aware navigation behaviors on a small unmanned ground vehicle (UGV) and a perception stack that provides cues used to transition between these different learned behaviors. Specifically, we integrate socially compliant, terrain-aware, and covert behaviors in an outdoor navigation scenario where the UGV encounters moving pedestrians, different terrains, and weapon threats.

#### 摘录 B

- 出处：第 6-7 页，`System integration for context-aware navigation`
> The supporting software components of our robotic system constitute the autonomy architecture. ... This context is used as input to the navigation behaviors and also to the behavior executor to determine when to transition between these navigation modules.

#### 摘录 C

- 出处：第 12-13 页，`3.3 Navigation`
> The behavior executor implements the state machine shown in Figure 9. ... The state machine proceeds through five states, IDLE, NORMAL, PEDESTRIAN, THREAT, and DONE. ... The THREAT condition has the highest priority ... Likewise, in the absence of the threat mode, the socially compliant navigation controller will be used if pedestrians are detected ... and the normal-mode controller will be used in the absence of either of these conditions.

#### 摘录 D

- 出处：第 13 页，`3.3 Navigation`
> In a mission where the robot must first move through an empty section of road and then encounters a group of pedestrians, it would transition from the NORMAL state to the PEDESTRIAN state. ... It then sends a new goal to the socially compliant navigation controller to continue the operation. When the robot encounters a threat ... it cancels either the terrain-aware or socially compliant navigation controller ... reconfigures the IOC controller for covert operation, and sends a new goal to the IOC controller. ... There are no transitions back from threat mode; the robot will continue the use of covert navigation until the goal is reached.

### 2. 基于原文整理后的自然语言描述

The UGV uses a five-state behavior executor that starts from `IDLE`, enters `NORMAL` terrain-aware navigation after receiving a goal, and then preempts that nominal behavior whenever perception reports pedestrians or threats in the surrounding scene. The first priority rule is explicit: weapon detection sends the controller into `THREAT`, while pedestrian detection only triggers `PEDESTRIAN` when no threat is active, and otherwise the system stays in `NORMAL`. A transition is not just a label change, because the executor cancels the currently running navigation module, reconfigures the IOC controller when covert traversal is needed, and then issues a new goal to the selected behavior. When the robot sees pedestrians, it hands off from terrain-aware IOC to socially compliant NaviGAN, whereas a threat cue forces either normal or pedestrian mode to be preempted by covert navigation. The machine only leaves this high-priority covert branch once the destination is reached, so context recognition directly governs the supervisory mission flow rather than only tuning low-level control gains.

### 3. 逐句溯源

1. 句子 1：The UGV uses a five-state behavior executor that starts from `IDLE`, enters `NORMAL` terrain-aware navigation after receiving a goal, and then preempts that nominal behavior whenever perception reports pedestrians or threats in the surrounding scene.
   对应摘录：A, B, C
2. 句子 2：The first priority rule is explicit: weapon detection sends the controller into `THREAT`, while pedestrian detection only triggers `PEDESTRIAN` when no threat is active, and otherwise the system stays in `NORMAL`.
   对应摘录：C
3. 句子 3：A transition is not just a label change, because the executor cancels the currently running navigation module, reconfigures the IOC controller when covert traversal is needed, and then issues a new goal to the selected behavior.
   对应摘录：D
4. 句子 4：When the robot sees pedestrians, it hands off from terrain-aware IOC to socially compliant NaviGAN, whereas a threat cue forces either normal or pedestrian mode to be preempted by covert navigation.
   对应摘录：C, D
5. 句子 5：The machine only leaves this high-priority covert branch once the destination is reached, so context recognition directly governs the supervisory mission flow rather than only tuning low-level control gains.
   对应摘录：D
