# An Autonomous Control Framework of Unmanned Helicopter Operations for Low-Altitude Flight in Mountainous Terrains - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把无人直升机低空飞行中的 `long-range penetration / fast approach / fast avoidance / circuitous flight` 四类任务写成统一 FSM，并明确给出基于目标检测、威胁等级和可见性变化的切换逻辑。

## 条目 1: Low-altitude mission-task FSM for target approach and threat avoidance
- 控制对象：无人直升机低空飞行任务的高层决策控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个无人直升机在山地低空任务中根据目标、威胁和可见性状态切换穿透、接近、快速规避和迂回飞行的任务状态机。
- 判断：算。对象是真实飞行平台的高层任务决策器，不是单纯视觉或避障算法流程；原文给出了 flight task、优先级、guard 条件和恢复逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 17 页，Section 4.2 `Finite State Machine`
> On this basis, a finite state machine was established to combine the decision-making and control methods, thus forming the overall framework for unmanned helicopter operations in low-altitude flight.
>
> The finite state machine established a continuous operation process without human interference and covered most scenes in the low-altitude flight.

#### 摘录 B
- 出处：第 18 页，Section 4.2 `Finite State Machine`
> In low-altitude flight, a helicopter is given a distant destination and required to approach the destination at low altitude.
>
> Once the target is detected, the helicopter immediately heads to the target through visual servo control and revises the target's position.
>
> In case the target is lost, the helicopter continues flying to the defined target points to approach the target and returns to visual servo control when the target is rediscovered.

#### 摘录 C
- 出处：第 18-19 页，Section 4.2 `Finite State Machine`
> We defined a threat threshold ET, whereby a threat degree that higher than ET is considered as a serious threat.
>
> In this situation, the helicopter executes fast avoidance flight to escape the sight range of the threat as soon as possible, seeking terrains as cover to change its visibility.
>
> The helicopter executes fast avoidance upon detecting a serious threat, regardless of whether a target is detected in the view.

#### 摘录 D
- 出处：第 19-20 页，Section 4.2 `Finite State Machine`
> If the threat degree is lower than ET, the detected threat is considered a small threat, and the helicopter executes circuitous flight.
>
> The finite state machine presents a detailed decision-making framework through the state transitions of different flight tasks, such as long-range penetration, fast approach, fast avoidance, and circuitous flight.
>
> For the long-range penetration task, the helicopter approaches the destination and avoids terrain obstacles according to the VFH method.

### 2. 基于原文整理后的自然语言描述

The unmanned helicopter controller is organized as a mission-task FSM whose baseline state is `long-range penetration`, in which the aircraft follows VFH-generated commands to approach a distant destination at low altitude while avoiding terrain obstacles. When a target is detected, the supervisor switches to `fast approach`, locks the yaw channel to the target with visual servoing, and keeps placing target points ahead so that the helicopter can continue approaching even if the target is briefly lost and later reacquired. In parallel with target handling, the controller also evaluates every detected threat and compares its threat degree `E` with the threshold `ET`. If `E > ET`, the FSM enters `fast avoidance`, forces the helicopter to head toward the threat for visibility judgement, and commands lateral cover-seeking maneuvers until the threat is lost from view and invisibility is restored behind terrain. If `E <= ET`, the controller instead chooses `circuitous flight`, places VFH target points on the side of the helicopter, bypasses the threat while preserving concealment, and then resumes the original destination-approach chain once the threat disappears.

### 3. 逐句溯源

1. 句子 1：The unmanned helicopter controller is organized as a mission-task FSM whose baseline state is `long-range penetration`, in which the aircraft follows VFH-generated commands to approach a distant destination at low altitude while avoiding terrain obstacles.
   对应摘录：A, D
2. 句子 2：When a target is detected, the supervisor switches to `fast approach`, locks the yaw channel to the target with visual servoing, and keeps placing target points ahead so that the helicopter can continue approaching even if the target is briefly lost and later reacquired.
   对应摘录：B
3. 句子 3：In parallel with target handling, the controller also evaluates every detected threat and compares its threat degree `E` with the threshold `ET`.
   对应摘录：C
4. 句子 4：If `E > ET`, the FSM enters `fast avoidance`, forces the helicopter to head toward the threat for visibility judgement, and commands lateral cover-seeking maneuvers until the threat is lost from view and invisibility is restored behind terrain.
   对应摘录：C
5. 句子 5：If `E <= ET`, the controller instead chooses `circuitous flight`, places VFH target points on the side of the helicopter, bypasses the threat while preserving concealment, and then resumes the original destination-approach chain once the threat disappears.
   对应摘录：D
