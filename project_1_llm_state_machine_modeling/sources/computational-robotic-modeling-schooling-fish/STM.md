# Computational and robotic modeling reveal parsimonious combinations of interactions between individuals in schooling fish - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：虽然论文主问题是鱼群行为建模，但文中对机器人平台实现给出了完整的两态 FSM、双时间尺度控制、避障超时和无效目标回退流程，足以作为双 A 的机器人控制样本。

## 备注

- 当前目录中的 `paper.pdf` 使用 PMC 可打印页面导出的 PDF 版本；原始站点的部分直链 PDF 文本提取明显失真，因此这里保留的是更稳定、可直接回溯状态机段落的版本。

## 条目 1: COMPUTE-MOVE schooling-robot navigation controller

- 控制对象：通用控制与群体机器人领域的单机器人目标选择与运动执行控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是机器人鱼群平台中单个机器人执行局部决策的控制器，用 `COMPUTE` 和 `MOVE` 两个主状态组织邻居选择、目标生成、运动执行和避障恢复。
- 判断：算。对象是实际机器人平台上的控制软件而不是单纯生物学模型，原文明确给出了状态机结构、`20 ms` 控制周期、约 `1.3 s` 决策尺度、`3 s` 超时和 `80 mm` 回退规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 40-45 页，机器人控制时间尺度与状态机实现，行 931-940 与 1034-1049
> The clock cycle of the imaging process module is 300 ms ... location data to the right robots on a shorter time scale (every 20 ms). These data are used in real time ... simulating the computational model, which is about 1.3 s. ... The time interval of the Real Time Control module is 20 ms for each robot ... We design a state machine control structure to implement the HIL simulation control for each robot.

#### 摘录 B

- 出处：第 45 页，机器人状态机总体说明，行 1059-1070
> The state machine control structure for an individual robot includes two main states: COMPUTE state and MOVE state ... When a robot is in the COMPUTE state ... the computational model determines a new decision ... After that, the robot switches to the MOVE state and adjusts its wheels to move towards the decision place ... To prevent collisions between robots, we designed and implemented an obstacle avoidance protocol. When no valid targets can be generated during the COMPUTE state ... the robot generates a valid target place by means of a scanning method and, alternatively, just moves back over a short distance.

#### 摘录 C

- 出处：第 48-49 页，状态与附加过程细节，行 1085-1144
> At any time a robot can be in one of the two following states: (1) the COMPUTE state for choosing a new target place, and (2) the MOVE state to reach the target place. ... If the scanning method cannot find a valid target, the robot moves back over a distance of 80 mm and starts again the COMPUTE state. ... MOVE State: ... the robot first rotates towards the target and then moves straight until it reaches the target ... If the focal robot cannot go back into the MOVE state within 3 seconds, it toggles to the COMPUTE state to determine a new target. ... If, after scanning, no free space is available for moving, the robot moves back over a predefined distance of 80 mm ... and then toggles to the COMPUTE state.

#### 摘录 D

- 出处：补充图 S8，行 1516-1524
> S8 Fig. Finite state machine diagram of one robot. ... In the COMPUTE state, the model determines a new target to reach by integrating the local information about the neighbors and the environment. ... If the scanning fails, the robot moves back 80 mm and starts again for model computing. If the decision target is valid, the robot switches into MOVE state, which includes three sub-states: Rotate, Move straight, and Avoid obstacle.

### 2. 基于原文整理后的自然语言描述

The robotic schooling platform implements each robot controller as a two-state finite-state machine with a slow decision layer and a fast execution layer: the behavioral decision process runs on a scale of about `1.3 s`, while real-time motion control is updated every `20 ms`. In the `COMPUTE` state, the robot selects influential neighbors, computes the heading variation and kick length prescribed by the model, and validates the resulting target position against walls and nearby robots. When a valid target exists, the controller switches to `MOVE`, where the robot rotates toward the target and moves straight to it while running an obstacle-avoidance procedure. Recovery logic is explicit: if the robot cannot resume `MOVE` within `3 s`, or if no valid target can be generated within `3 s`, it falls back to re-computation, potentially after a predefined `80 mm` backward motion; the supplementary state-machine diagram also refines `MOVE` into `Rotate`, `Move straight`, and `Avoid obstacle`.

### 3. 逐句溯源

1. 句子 1：The robotic schooling platform implements each robot controller as a two-state finite-state machine with a slow decision layer and a fast execution layer: the behavioral decision process runs on a scale of about `1.3 s`, while real-time motion control is updated every `20 ms`.
   对应摘录：A
2. 句子 2：In the `COMPUTE` state, the robot selects influential neighbors, computes the heading variation and kick length prescribed by the model, and validates the resulting target position against walls and nearby robots.
   对应摘录：B, C
3. 句子 3：When a valid target exists, the controller switches to `MOVE`, where the robot rotates toward the target and moves straight to it while running an obstacle-avoidance procedure.
   对应摘录：B, C, D
4. 句子 4：Recovery logic is explicit: if the robot cannot resume `MOVE` within `3 s`, or if no valid target can be generated within `3 s`, it falls back to re-computation, potentially after a predefined `80 mm` backward motion; the supplementary state-machine diagram also refines `MOVE` into `Rotate`, `Move straight`, and `Avoid obstacle`.
   对应摘录：C, D
