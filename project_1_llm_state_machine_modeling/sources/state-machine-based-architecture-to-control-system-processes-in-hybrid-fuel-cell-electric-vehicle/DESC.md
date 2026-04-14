# 混合燃料电池汽车的分层监督状态机 / State machine-based architecture to control system processes in a hybrid fuel cell electric vehicle

## 论文在讲什么

这篇论文讨论的是混合燃料电池汽车里的 fuel cell system supervisory controller。作者不是只做某个连续控制律，而是围绕燃料电池系统运行过程本身，设计一个中央状态机来协调阴极、热管理、阳极和 DC/DC 等多个子系统，并把启动、运行、最小功率和停机过程组织起来。

论文把这个 supervisory controller 分成三部分：State Machine、Optimal Setpoint Generator 和 Power Limit Calculator。其中对 `sources/` 最有价值的，是作为核心骨架的状态机部分。它明确列出顶层状态，又进一步把 start-up 和 shutdown 展开为更细的子状态链，所以不是简单的 mode list，而是典型的层次 supervisor。

## 控制系统在文中的位置

控制系统描述在文中占据绝对主体位置。第 3 节先介绍 SM 架构，再给 protocol/status number 表，再给 overall scheme，随后专门用两个小节解释 start-up 和 shutdown sub-state machine，最后还用实车曲线把 `t = 14 s`、`t = 23 s`、`t > 540 s` 等关键过程和局部变量变化对应起来。

这意味着我们关心的离散控制链，在这篇论文里不是附带说明，而是作者组织整个 fuel-cell process control 的主表达方式。它也和纯能源管理策略论文不同，这里真正控制的是“系统过程如何安全推进”，而不只是功率分配结果。

## 对我们为什么有用

这篇论文对 `🚗` 方向很有价值，因为它补的是车载动力系统里的 `HSM + T1` supervisor 样本。库里车辆方向很多条目都更偏行为决策或道路场景，而这篇补的是 powertrain/fuel-cell 过程管理，结构差异明显。

它还补了两个很重要的可抽取位点：一是 protocol/status number 这种带反馈确认的模式切换机制，二是“超时即 Failsafe”的硬安全分支。这两类信息对后续自动生成验证性质、恢复故障链和层次状态机都很关键。

## 如果需要人工细读，建议怎么读

人工细读时，建议先看第 3.1.1 的 protocol/status number 表，再看第 3.1.2 的 overall scheme，最后重点读 3.1.3 和 3.1.4。优先抓顶层状态、启动链、停机链、`Min Power -> Run / Normal Shutdown` 的分叉、以及 timeout 触发 `Failsafe` 的规则。读顺这些以后，再回头看 setpoint generator 和 power limit calculator 就会容易很多。
