# 火星样本返回捕获-封装-返回系统机器人控制软件的初步设计 / A Preliminary Design of the Robotic Control Software for Mars Sample Return - Capture, Containment, and Return System

## 论文在讲什么
这篇论文解决的是火星样本返回任务中，机器人传送装置如何通过 flight software 安全执行抓取/传送动作的问题。输入是 motion primitive 命令、`RSCE` telemetry、Worker Task 检查结果和 stop/fault 事件，方法是设计一个显式主 FSM 管理配置、预检查、运动执行和后检查，输出是 `RSW` 的机器人控制软件结构。
从论文的展开方式看，输入侧主要落在 motion primitive commands、`RSCE` telemetry、Worker Task result、stop command、fault condition，核心做法是 `Step / StateExit / StateEntry / StateRun` 调度的机器人控制 FSM，最终形成的则是 机器人运动原语执行控制链、异常处理逻辑和 `RSW` 软件架构。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是 `Mars Sample Return` 任务 `CCRS` 中的 `Robot Software (RSW)`。它负责 command and monitor 控制机器人机构的 avionics，使系统能够执行 sterilize、install、pick-and-place 等与样本转运相关的动作。
`RSW` 主状态机明确包括 `UNKNOWN`、`INITIALIZED`、`RSCE_ON`。 论文把 nominal path 写得非常明确，例如 启动后从 `UNKNOWN` 进入 `INITIALIZED`、等待 telemetry 后进入 `RSCE_ON`、完成初始配置后进入 `READY_ON`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文是真实航天任务软件中的离散控制链，不是泛化的机器人方法描述。 它能提供“命令-配置-预检-执行-后检-异常回退”这种非常规整的工程控制模板。 论文正文足以支撑 `STM.md` 达到 `🟢 A`，适合直接进入主数据集候选池。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `current/requested state` 这种工程化状态管理写法、`StateExit / StateEntry / StateRun` 的控制器文本组织结构、stop/fault 作为统一回退接口的建模方式 这些最容易直接转成状态机自然语言描述的部分。 论文是 preliminary design，某些底层 motion primitive 细节还没完全展开。 低层机器人运动学和硬件细节较多，不应全部混入高层状态机文本。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。
