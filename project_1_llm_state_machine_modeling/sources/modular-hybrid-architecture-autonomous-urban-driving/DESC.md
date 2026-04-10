# 模块化城市自动驾驶混合系统架构 / A Modular, Hybrid System Architecture for Autonomous, Urban Driving

## 论文在讲什么

这篇论文介绍的是 Georgia Tech `Sting Racing` 参加 DARPA Urban Challenge 时使用的一套模块化城市自动驾驶架构。作者的基本判断是，城市驾驶里的不同场景需要完全不同的感知重点、控制策略和仲裁逻辑，因此不能只靠一条统一的 sense-plan-act 主线去覆盖所有情况。于是他们把整车运行拆成若干“modes of operation”，再用嵌套混合自动机把这些模式组织起来。

整篇论文围绕这个架构如何支撑城市驾驶任务展开。顶层有 `Follow Lanes`、`Handle Intersection`、`Park`、`Unpark`、`U-Turn` 等模式，往下又继续细分为车道跟随、绕障、交叉口排队与通行等子机。它不是单独介绍某个局部感知算法，而是在讲一辆真实比赛自动驾驶车怎样通过层次模式管理把复杂任务压缩成可调试、可扩展的控制系统。

## 控制系统在文中的位置

控制系统描述在本文里是绝对核心，而不是某个实验附录。论文从一开始就强调城市驾驶需要切换 sensing priorities 和 control regimes，然后用 Figure 3 给出高层模式集合，用第 `4` 节给出 `Nested Hybrid Automata` 的形式化定义，再把若干子机写成更深层的 automata。这种写法使它不只是“有一个状态机图”，而是真正以层次自动机为主线展开系统说明。

同时，这套状态机并不悬空存在。论文明确说 situational awareness block 选择出的 action 会送往 behavior arbitration，仲裁器再把离散模式转成曲率和速度指令交给 vehicle control block。因此这里的 HSM 直接参与实际车辆控制，而不是只做任务调度示意。这一点对我们筛样很关键，因为它说明这些状态是真正的控制模式。

## 对我们为什么有用

这篇论文对 `sources/` 的意义，在于它提供了一个非常典型、而且证据很完整的 `HSM + 连续耦合` 自动驾驶样本。很多自动驾驶论文只给顶层行为图，缺少子机和 guard；这篇却把顶层模式、`Follow Lanes` 内部子状态、`Handle Intersection` 的多阶段链，以及更深层 `traverse-intersection` 子机都写出来了，还明确说明 `Blocked` 有基于时间的跳转。

它还补充了“层次结构为什么要这样设计”的工程语境。作者把模块化、可测试、可增量扩展当作架构原则，这让它非常适合后续用来研究 LLM 如何从分层自然语言需求恢复层次状态机结构，而不是只恢复一张平面行为图。对于项目一的数据集建设，这是难得的高质量层次样本。

## 如果需要人工细读，建议怎么读

人工细读时，建议先看第 3-5 页 `Coverage of the Required Capabilities`，把六个顶层模式、`Follow Lanes` 子机和 `Handle Intersection` 子机的职责边界读清楚。这部分最能帮助你快速建立“哪些是高层模式、哪些是更细一层的动作状态”的直觉。

第二轮再看第 7-10 页的 `Nested Hybrid Automata` 形式化定义和层次展开，重点确认每一层 automaton 的离散状态集合、上下层如何嵌套，以及 action 怎样映射到仲裁器。若只是为重做 `STM.md`，测试章节和大量系统组件介绍可以延后；先把分层状态结构和 guard 读透，回报最高。
