# 多 FSM 机器人系统通信与乒乓球收集案例 / Communication Within Multi-FSM Based Robotic Systems

## 论文在讲什么

这篇论文的主标题确实偏方法，核心想讲的是一种基于 embodied agent、whiteboard 和 `LLFSM` 的机器人系统设计与实现方式。但作者没有只停在方法论，而是用一个具体的 `table-tennis ball-collecting robot` 贯穿整篇说明。这个机器人有 camera、sonar、body、vacuum 等子系统，上层控制器在搜索、收集和避障之间切换，下层子系统负责把高层命令落实到视觉检测、障碍检测、底盘运动和吸附动作。

因此，这篇论文对 `sources/` 的价值不在“通信框架”本身，而在它把一个具体移动机器人控制问题写成了清晰的层次状态机。相比很多只说框架、不给具体控制对象的 robotics middleware 论文，这里至少留下了一个边界清晰、输入输出明确、可追溯到条目级 evidence 的控制案例。

## 控制系统在文中的位置

控制系统描述在文中既是方法载体，也是实际案例。前半部分先铺垫 embodied agent、LLFSM、whiteboard 这些概念，但到了第 7 节，作者切换成对 ball-collecting robot 的具体说明：哪些是实传感器，哪些是虚拟子系统，控制子系统 `cbc` 怎么根据球和障碍检测信息给 body/vacuum 发命令，上层 `cFbc` 状态机又如何在 `search / collect / avoid` 之间切换。

也就是说，这不是那种“有一个案例名字，但正文里几乎没有控制细节”的方法论文。相反，作者把输入缓冲、输出缓冲、transition function、terminal condition 乃至 collect 行为如何根据 ball radius 和 image offset 生成速度/偏移命令都写出来了，所以状态机样本是足够实的。

## 对我们为什么有用

当前 `⚙️` 方向里，很多样本要么是平面的任务 FSM，要么是更偏行为规划而不强调层次关系。这篇论文补进来以后，可以明显增强 `HSM + T0` 这一侧的监督控制样本，因为它不仅有顶层三态任务流，还显式说明每个行为本身是 subFSM，并通过 camera/sonar/body/vacuum 子系统把任务层和执行层连起来。

它还有一个额外好处：这里的 case 并不依赖工业 PLC 词汇，也不依赖很强的时间语义，而是强调 perception cue 如何驱动高层任务切换。对后续做自然语言到状态机建模时，这类“感知驱动的层次任务控制”样本和传统顺序控制样本是互补的。

## 如果需要人工细读，建议怎么读

人工细读时，建议先跳到第 7 节，先看 `Structure` 和 `Activities` 两段，把 ball-collecting robot 的子系统边界和 `search / collect / avoid` 三个主状态记住。然后继续读 collect 行为的 transition function、terminal condition 和后面关于 search/avoid 的说明，把“何时搜索、何时转入收集、何时被障碍打断、何时调用 bug avoidance”这条主逻辑读顺。

至于前面大量关于通信分类、whiteboard 抽象、LLFSM 实现模型和与其他框架对比的内容，可以放在第二轮。那些部分对理解论文方法当然重要，但如果目标是抽取状态机样本，优先级明显低于第 7 节里关于具体机器人控制对象的结构和活动描述。
