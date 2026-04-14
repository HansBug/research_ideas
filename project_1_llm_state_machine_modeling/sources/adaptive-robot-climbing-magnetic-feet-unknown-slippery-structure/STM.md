# Adaptive Robot Climbing with Magnetic Feet in Unknown Slippery Structure - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（任务级显式时序）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把磁足攀爬机器人的一步 climbing controller 明确写成四相 `full-support / pre-swing transition / swing / post-swing transition` 状态机，并进一步给出 slip 检测后在 `pre-swing` 或 `swing` 阶段触发 CoM 轨迹重规划的规则，能够稳定支撑双 A。

## 条目 1: Four-phase slip-aware magnetic-feet climbing supervisor
- 控制对象：通用控制与机器人任务领域的磁足攀爬机器人相位切换与滑移恢复控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（任务级显式时序）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向未知湿滑结构表面的磁足攀爬机器人控制器，用四相接触状态机组织一步攀爬，并在检测到滑移时按当前相位与估计摩擦条件重规划 CoM 轨迹和接触力分配。
- 判断：算。对象是真实机器人控制器而不是单纯轨迹优化方法；原文直接把 climbing control 写成四相 state machine，并给出 slip 检测相位、重规划入口和基于 slip velocity 的权重调节逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section `2.2.4 Phase-based state machine`
> Phase-based state machines are used together with WBLC to control a legged robot. We defined four state machines for one-step climbing control: full-support, pre-swing transition, swing, and post-swing transition. Each state machine represents a WBLC controller defined to consider different contact phases.

#### 摘录 B
- 出处：第 11 页，Section `4.2 CoM re-planning for slip reflex`
> If a slip is detected and the estimated friction coefficient and adhesion forces are significantly inferior, then we will need to re-plan the CoM trajectory for generating the desirable contact forces to keep rigid contact. The slip is supposed to be detected during the pre-swing or swing phase when the uncertainty for a contact is high.

#### 摘录 C
- 出处：第 15 页，Section `6.3 Slip-aware online weight adaption`
> Once the slip velocity exceeds the threshold, it starts to change the weights, and this can help a robot to slightly redistribute contact forces to stop sliding.

### 2. 基于原文整理后的自然语言描述

The climbing controller organizes each one-step motion of the magnetic-feet robot as a four-phase state machine consisting of `full-support`, `pre-swing transition`, `swing`, and `post-swing transition`, with each phase instantiating a different whole-body locomotion controller under different contact assumptions. This makes the state machine more than a gait labeler: it determines which contact dimensions, force constraints, and controller weights are active while the robot moves on steep structures. The model is extended by environment-dependent variables, because slip handling depends on estimated friction coefficients, magnetic adhesion forces, and the current phase time. When the controller detects slip during `pre-swing` or `swing`, it triggers CoM trajectory re-planning so that the remaining motion generates safer contact forces under the re-estimated surface condition. In parallel, once slip velocity exceeds a threshold, the controller adjusts optimization weights online to increase normal force and reduce tangential force, thereby redistributing contact forces to stabilize the robot before it loses contact.

### 3. 逐句溯源

1. 句子 1：The climbing controller organizes each one-step motion of the magnetic-feet robot as a four-phase state machine consisting of `full-support`, `pre-swing transition`, `swing`, and `post-swing transition`, with each phase instantiating a different whole-body locomotion controller under different contact assumptions.
   对应摘录：A
2. 句子 2：This makes the state machine more than a gait labeler: it determines which contact dimensions, force constraints, and controller weights are active while the robot moves on steep structures.
   对应摘录：A
3. 句子 3：The model is extended by environment-dependent variables, because slip handling depends on estimated friction coefficients, magnetic adhesion forces, and the current phase time.
   对应摘录：B
4. 句子 4：When the controller detects slip during `pre-swing` or `swing`, it triggers CoM trajectory re-planning so that the remaining motion generates safer contact forces under the re-estimated surface condition.
   对应摘录：B
5. 句子 5：In parallel, once slip velocity exceeds a threshold, the controller adjusts optimization weights online to increase normal force and reduce tangential force, thereby redistributing contact forces to stabilize the robot before it loses contact.
   对应摘录：C
