# 分段复合板装配 pause-resume 监督器 / Sensor-Guided Assembly of Segmented Structures with Industrial Robots

## 论文在讲什么

这篇论文讨论的是用工业机器人完成大型分段复合结构装配的问题。具体场景是将较大的复合板从 pick-up 区域搬运到 assembly nest，并在视觉和力传感的帮助下完成精确对位与柔顺放置。作者关心的不只是单一步骤的视觉伺服或力控制，而是如何把 `pick-up`、`transport`、`placement` 这三个环节组织成一条可以长期重复执行、又能随时人工介入的完整制造流程。

系统实现层面也比较具体。原文同时使用 overhead camera、机器人腕部相机、力/力矩传感器、外部运动接口和 ROS 过程控制器，把大型柔性面板从任意放置姿态抓取出来，再运输到目标工位并完成亚毫米级对齐。对 `sources/` 最关键的是，作者明确说整条流程由一台 finite state machine 负责 govern process flow and user interface，因此这里保留下来的不是单纯的 robot skill，而是一套制造流程监督控制语义。

## 控制系统在文中的位置

这里的控制系统描述属于论文主体，而不是附带实现。虽然文章也详细讨论了 QP 运动控制、视觉伺服、轨迹规划和力控制，但这些算法最终都是挂在整体 assembly process 的状态机之下。论文在问题定义部分就把三大步骤写成 process states，并明确指出 solution implementation 的第一步就是构建 state machine，负责步骤之间的切换、操作员交互和异常条件处理。

这篇论文值得注意的地方在于，它没有把流程状态机写成一个单向脚本。正文进一步说明同一套状态转移既可以在 autonomous mode 下运行，也可以在 safe teleoperation 下被人工接管；系统支持 pause、manual take-over、playback、resume、replan，以及向前或向后切换步骤。这使得状态机真正承担了监督控制职责，而不是只在 GUI 上表示“当前做到哪一步”。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补进的是 `🏭` 方向一种比较有区分度的装配流程监督样本。很多制造论文会详细讲末端执行器、视觉算法或路径规划，但不把整条流程的离散控制链说清楚；这篇则把核心 process states、异常中断、人工辅助和恢复策略写得比较完整，因此很适合作为 `FSM + T0` 的 end-to-end 制造监督器样本。

它还有助于补齐“人工接管与恢复”这类对自动建模很重要、但在现有工业样本中并不总是充分表达的控制语义。原文不仅保留了 nominal `pick-up -> transport -> placement` 主链，还明确说明出现异常或需要 secondary operation 时如何返回已知状态、如何暂停、如何回放和恢复。这种 pause-resume-manual transition 语义对后续建模异常恢复链或 supervisory workflow 很有价值。

## 如果需要人工细读，建议怎么读

人工回原文时，建议先看第一页摘要和第二到四页的问题描述，把三步 assembly process、重复运行条件和人工中断需求先建立起来。随后直接读第四页末到第五页初围绕 `Construct a state machine` 的段落，再跳到第七到第八页 `Software Architecture` 和 Figure 4 附近，把状态机如何管理 autonomous / safe teleoperation、pause / playback / resume / replan 这些监督语义读清楚。

QP 运动控制、视觉伺服、力控制和硬件参数部分可以放到第二轮再看。它们对于理解为什么系统能稳定执行有帮助，但第一次如果目标是重建 `STM.md`，最值得优先抓的仍然是三大流程状态、操作员交互边界、异常中断与恢复分支，以及 process controller 如何调用这些状态转移。
