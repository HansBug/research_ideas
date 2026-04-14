# 地下矿井多机器人协同部署与钻孔 HFSM / Underground Multi-robot Systems at Work: a revolution in mining

## 论文在讲什么

这篇论文讨论的是一个面向地下矿井作业的 heterogeneous multi-robot system。作者不是只做地图构建或巡检，而是希望让不同角色的机器人分工完成更接近真实矿业流程的任务，包括勘探、部署钻具、锚定和钻孔。文中聚焦的是 drilling phase，也就是 `Deployer` 和 `Stinger` 到达目标区域之后，怎样完成地形分析、钻具放置、锚定和钻孔这一串任务。

论文篇幅不长，但目标很明确：用多机器人、各自本机的 HFSM 行为和跨机器人触发消息，把原本需要中心持续联机调度的流程改成一个更模块化、更容错的顺序协同系统。因此它不是泛泛的机器人平台描述，而是一个很明确的任务级行为控制设计。

## 控制系统在文中的位置

控制系统描述在文中就是主角。作者明确说高层 autonomous drilling mission 必须被拆成 discrete software modules，对应不同 robot behavior，而整套部署依赖的是 HFSMs。`Deployer` 和 `Stinger` 不是简单顺序执行动作脚本，而是分别运行自己的 HFSM，再通过 ROS2 trigger message 把控制权顺次交给下一段行为。

这一点让它对 `sources/` 很有价值。很多多机器人论文会停留在体系结构、通信栈或模块接口层，但这篇把 mission modules 和 handoff 点写得足够明确，甚至还能从 `Figure 2-4` 读到 `Move To DeployPose`、`Centering` 这类关键状态名和 Deployer/Stinger 的具体衔接方式。

## 对我们为什么有用

它补的是 `⚙️` 方向里相对少见的多机器人任务监督样本，而且同时带 `层次 + 协议交互` 两种结构信号。相比常见的单机器人 navigation FSM，这篇的样本价值在于：控制对象是协同系统，状态推进依赖角色切换和跨机器人触发，而不是单一机器人内部的顺序动作。

这对后续数据集很重要，因为它能帮助模型接触“一个状态机如何通过消息触发另一个状态机”的写法，也能补充 mission-module 级的行为抽象，而不仅是传统设备控制或单车/单机 task planner。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看摘要和 `Concept of Operation`，先把 `Deployer`、`Stinger` 两个主要角色在 drilling phase 里分别负责什么读清。然后直接看 `Software Architecture and Mission Modules` 与 Figure `2`，确认顶层任务链 `3D Environment Mapping -> ... -> Mission Completed` 怎样被拆成顺序模块，以及为什么作者把它视为 collaborative multi-robot operation。

之后再看 Figure `3-4` 和相邻文字，把 `Move To DeployPose`、`Centering`、trigger message、`move motor` action server 这些关键衔接位置读细。底层硬件、CANopen、lattepanda、UR10 集成细节可以第二轮再看，因为对状态机抽取来说，第一轮最关键的是顶层模块链和 Deployer/Stinger 之间的控制权交接。
