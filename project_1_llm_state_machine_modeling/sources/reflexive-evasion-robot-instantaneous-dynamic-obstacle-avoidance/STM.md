# REBot: Reflexive Evasion Robot for Instantaneous Dynamic Obstacle Avoidance - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四足机器人瞬时避障系统明确写成 `Normal / Avoidance / Recovery` 三态 FSM，并给出由接近速度、姿态阈值、关节速度与底盘高度驱动的转移判据以及恢复策略效果。

## 条目 1: Normal-Avoidance-Recovery Reflexive Evasion FSM

- 控制对象：四足机器人面对高速动态障碍时的瞬时避障与恢复控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个部署在 Unitree Go2 四足机器人上的安全控制器，用正常、避障和恢复三个离散阶段衔接高速障碍规避与姿态稳定。
- 判断：算。对象是实际机器人安全监督器，原文明确给出三态 FSM、由障碍接近与姿态失稳阈值触发的转移条件、恢复阶段目标，以及对恢复阶段的消融验证。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，及第 3 页，Section IV-A，行 14-18, 64-78, 229-263
> REBot integrates an avoidance policy and a recovery policy within a finite-state machine. The REBot system is structured as a finite-state machine with three behavioral stages. During the normal stage, the robot performs its primary functional tasks. When an approaching obstacle is detected, REBot transitions to the avoidance stage, executing reflexive evasion maneuvers. After an evasive maneuver, the robot may become unstable. REBot then enters the recovery stage, during which a policy stabilizes the robot and restores normal function. When the obstacle is approaching the robot, i.e. `<v_O^t, p_R^t - p_O^t> > 0`, REBot switches to the avoidance stage. REBot judges the instability with three criteria: body orientation exceeds a safe range, joint velocity surpasses a stability limit, or base height drops below a threshold value.

#### 摘录 B

- 出处：第 4-7 页，Figure 3 / Section V-A / Section V-D，行 337-389, 435-440, 573-611
> Fig. 3 shows that a finite-state machine governs transitions between the `Normal`, `Avoidance`, and `Recovery` stages. The recovery policy ensures a smooth transition from the avoidance stage back to the normal stage, allowing the robot to regain balance. The reward function is designed corresponding to the instability criteria and includes orientation, stability, position, and additional penalties to reduce abrupt joint movements and encourage smoother transitions during recovery. The systems are evaluated with avoidance success rate and recovery stability rate, indicating the proportion of trials where the robot successfully stabilizes after avoidance. The recovery stage ensures a stable standing posture after rapid reflexive evasion. Removing the recovery stage leads to a drop of about 20% in the success rate within the reflex region.

### 2. 基于原文整理后的自然语言描述

REBot organizes quadrupedal dynamic-obstacle avoidance as a three-state FSM with `Normal`, `Avoidance`, and `Recovery`, so the robot can separate nominal standing or task execution, reflexive evasion, and post-evasion stabilization into explicit stages. The controller leaves `Normal` when the obstacle velocity and relative position indicate that the obstacle is approaching the robot, enters `Avoidance` to execute fast evasive maneuvers, and then switches to `Recovery` whenever the evasion leaves the robot unstable according to orientation, joint-velocity, or base-height thresholds. In `Recovery`, a dedicated policy drives the robot back toward its default posture and suppresses abrupt joint motions, allowing the controller to return safely to `Normal` instead of ending the behavior in a destabilized pose. The paper further validates that this recovery branch is functionally necessary by measuring both avoidance success rate and recovery stability rate and showing that removing the recovery stage reduces success by about 20% in the reflexive region.

### 3. 逐句溯源

1. 句子 1：REBot organizes quadrupedal dynamic-obstacle avoidance as a three-state FSM with `Normal`, `Avoidance`, and `Recovery`, so the robot can separate nominal standing or task execution, reflexive evasion, and post-evasion stabilization into explicit stages.
   对应摘录：A, B
2. 句子 2：The controller leaves `Normal` when the obstacle velocity and relative position indicate that the obstacle is approaching the robot, enters `Avoidance` to execute fast evasive maneuvers, and then switches to `Recovery` whenever the evasion leaves the robot unstable according to orientation, joint-velocity, or base-height thresholds.
   对应摘录：A
3. 句子 3：In `Recovery`, a dedicated policy drives the robot back toward its default posture and suppresses abrupt joint motions, allowing the controller to return safely to `Normal` instead of ending the behavior in a destabilized pose.
   对应摘录：B
4. 句子 4：The paper further validates that this recovery branch is functionally necessary by measuring both avoidance success rate and recovery stability rate and showing that removing the recovery stage reduces success by about 20% in the reflexive region.
   对应摘录：B
