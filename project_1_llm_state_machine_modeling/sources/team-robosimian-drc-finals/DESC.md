# RoboSimian 接触触发行为控制 / Team RoboSimian: Semi-autonomous Mobile Manipulation at the 2015 DARPA Robotics Challenge Finals

## 论文在讲什么

这篇论文是 JPL 团队总结 RoboSimian 在 2015 DARPA Robotics Challenge Finals 中整机设计、控制、感知和任务执行经验的系统论文。它不是只讲某个局部抓取算法，而是把机器人如何在弱通信条件下完成驾驶、下车、开门、拧阀、抓钻切墙和复杂地形移动这些任务整体串起来。论文把系统定位成“高层可重复、低层可适应”的半自主架构，高层依赖对象/任务框架里的可复用脚本和导航位姿，低层则通过接触行为和力传感去应对现场误差。

对 `sources/` 来说，最关键的是作者没有把 behavior 只停留在抽象概念上，而是明确说它们是异步、接触触发的层次状态机，并展示了 `Door Open`、`Valve Turn`、`Drill Grab`、`Drive to Contact` 等行为图。再加上原文又解释了行为如何先规划到对象相对起始位姿、再依据力/距离阈值和 timeout 执行局部闭环动作，所以它不是泛架构论文，而是很具体的机器人任务控制样本。

## 控制系统在文中的位置

这里的控制系统描述是论文主体之一。虽然文中也有大量机械设计、通信、定位和 motion primitive 的内容，但真正把“机器人接下来如何执行任务”落地的，是 Section 5 和 Section 8 中的 behavior layer。作者把 limb server、control module 和 behavior request 串成一条执行链，再把 door、valve、wall 等操作任务拆成若干可复用的接触行为，因此这一层不是附属实现，而是整台机器人半自主执行能力的核心。

更重要的是，这些 behavior 不是只有状态名。论文解释了每个状态都可以带 force-control setpoint、open-loop Cartesian move、motion complete / time reached / force-torque threshold 这些结束条件，并在 Figure 7 里给出 success/failure 分支。也就是说，我们关心的状态机描述在文中承担的是“把复杂操作任务组织成可重复、可恢复、可参数化局部控制链”的角色。

## 对我们为什么有用

这篇论文补的是 `⚙️` 方向比较少见、而且质量很高的 `HSM + T1` 机器人任务监督样本。库里虽然已经有轮式足球机器人、叉车导航或小型巡检机器人等条目，但 RoboSimian 这篇提供的是另一种更强的表达面向：不是单一平面移动任务，而是围绕真实灾害响应操作任务的可复用 contact behavior library。它把对象相对起始位姿、局部力觉适应、层次子状态和失败恢复全部放进同一套 supervisor 里，这对后续让模型恢复复杂 manipulation state machine 很有价值。

它还有一个很重要的样本意义：很多大型机器人系统论文会把状态机埋在图里或者退化成“software architecture”泛介绍，而这篇既给出总体架构，也给出行为图和任务级组合关系，所以可以直接作为“复杂机器人系统论文中什么才算真正可抽的控制对象”这一判断基线。尤其 `door / valve / wall` 任务链，对于异常分支、局部接触条件和层次化行为复用都提供了很好的语言素材。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `11-12` 页左右的 Section `5.1 Behaviors` 和 Figure `7`。这一段能最快锁定 behavior 的基本建模单位：它们是怎样与控制环对接的、每个状态有什么参数化动作、什么样的 end condition 会触发 success/failure，以及为什么这是层次状态机。接着直接跳到第 `21-22` 页的 manipulation tasks 讨论，看作者如何把开门、拧阀、抓钻和接触推进任务映射到具体 behaviors；这里最适合补齐“对象相对起始位姿”和“多段子行为组合”的语义。

至于 motion primitives、网络通信和硬件设计这些章节，可以第二轮再看。它们帮助理解整机为什么能在 DRC 里工作，但对重建 `STM.md` 里的核心状态机不是第一优先级。第一次细读时应优先把 behavior 的状态、guard、timeout、success/failure 分支和任务组合读稳，再去回看其他模块如何支撑这层 supervisor。
