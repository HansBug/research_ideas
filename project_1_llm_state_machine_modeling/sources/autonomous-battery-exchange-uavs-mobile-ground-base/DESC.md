# 移动地面基站上的无人机换电任务执行树 / Autonomous Battery Exchange of UAVs with a Mobile Ground Base

## 论文在讲什么

这篇论文研究的是怎样让一个移动地面基站在无人参与的情况下为小型无人机自动换电。系统本身不是单一机器人，而是由地面 `rover`、机械臂、服务站 `SBox` 和待服务的 `UAV` 共同组成。作者既讨论了机械结构、换电机构和定位方案，也讨论了用什么软件框架把这些异构组件组织成一个能真正执行任务的协同系统。

对 `sources/` 来说，最重要的不是换电机构本身，而是文中把整个任务写成了一个层次执行树，并明确说明机械臂高层规划器使用 `HFSM`。这意味着论文不只提供“一个机器人做了什么”，而是提供了“任务怎样被分解、怎样在不同 agent 之间委派、怎样形成嵌套执行链”，非常适合作为航空方向的 mission-level 状态机样本。

## 控制系统在文中的位置

这里的控制系统描述是论文的核心实现载体之一。作者并没有把协同控制框架只当作背景设施，而是把自动换电是否能成功，直接建立在这套 delegation framework 与 executor tree 是否能正确组织多个 agent 之上。从 `change_batt` 顶层执行器到 `dock_wasp` 子执行器，再到更底层的 `move_to / pick / dock`，原文都给出了较清楚的状态式任务分解。

这篇还值得保留的一个原因是，它不是那种泛泛而谈的“multi-agent architecture”。文中真正公开了 `find_wasp`、`disarm_wasp`、`lock_wasp`、`switch_batt`、`release_wasp`、`deploy_wasp` 等可命名、可排序、可分派的任务节点，因此我们保留的是一套真实的 UAV 服务任务监督器，而不是系统架构图的文字说明。

## 对我们为什么有用

在现有文库里，航空航天方向很多样本会漂向飞行模式管理、接近交会、安全模式或任务管理；这篇补进的是另一个很实用的子方向：地面支持系统与 UAV 协同的任务执行监督器。它不仅有清晰的任务链，而且天然带有多代理委派、服务协议和嵌套子任务这几类结构特征，对后续做更复杂状态机自动生成很有帮助。

它还补充了一种很有价值的控制叙述方式。很多论文只给最终状态图，不解释任务如何从高层目标递归展开；而这篇明确写了 `change_batt` 如何下钻为 `dock_wasp`，又如何继续分解成 `move_to / pick / dock`。如果后续需要研究“给定高层任务描述，如何生成多层状态机”或“如何从文本里同时提取层次和协同关系”，这篇会比普通单机飞行模式论文更有信息量。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `1-2` 页摘要和 `Collaborative Mission Framework` 的导入文字，先确认系统包含哪些 agent，以及作者为什么需要 distributed communication and control architecture。然后直接跳到第 `4` 页附近机械臂高层规划器与 `SBox` 的说明，抓住 `HFSM`、delegation module、communication hub 和 “service two wasps simultaneously” 这些关键词，先建立系统边界。

随后重点读第 `6` 页 `Battery Exchange Operation` 与 Figure `10` 周边文字，把 `change_batt` 顶层执行器和 `dock_wasp` 子执行器完整抄出来，再核对每个任务节点分别委派给哪个 agent。第一次人工复核时，不需要先深挖全部机械设计、视觉定位或轨迹规划细节；只要把 executor tree 的层次和委派链读稳，就足够重新构建这篇的核心状态机样本。
