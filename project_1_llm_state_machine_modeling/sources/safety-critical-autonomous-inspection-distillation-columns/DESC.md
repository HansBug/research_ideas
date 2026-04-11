# 蒸馏塔托盘巡检七任务监督器 / Safety-critical Autonomous Inspection of Distillation Columns using Quadrupedal Robots Equipped with Roller Arms

## 论文在讲什么

这篇论文面向化工蒸馏塔托盘这种狭窄、湿滑且多层的工业环境，讨论一台带滚轮臂的四足机器人如何完成自主巡检。作者把 locomotion、层间 transition、perception 和 safety filter 这些部件整合到一个统一框架里，目标是在工业级托盘环境中减少人工介入。

对 `sources/` 来说，最有价值的不是底层控制 barrier function，而是作者明确给出了一个任务级状态机，把 manway 搜索、单层巡检、移向过渡点、层间上/下行、后处理和安全撤离组织成可执行的监督链。这让论文不止是“安全控制方法”，而是具备完整任务状态语义的案例论文。

## 控制系统在文中的位置

状态机在文中承担的是总任务协调器角色。论文的底层还有 locomotion stack、transition stack 和 perception package，但这些模块如何串联、何时进入下一阶段、何时停止、何时重复巡检，全部由这个上层状态机决定。它是整套 autonomous inspection system 的离散骨架。

这意味着我们关心的状态机描述并不是附带插图，而是整篇论文把系统拼成一个能自主工作的 industrial inspection robot 的关键环节。正文也明确把它描述为“enhance the autonomy”的核心机制。

## 对我们为什么有用

这篇论文补入的是一个较少见的工业巡检状态机样本。相比更常见的移动机器人导航或四足步态控制论文，它把“任务目标变化”“搜索与过渡”“失败停机”和“安全撤离”放在同一条监督链里，适合拿来训练模型识别较长的任务级状态序列。

此外，它还能补足仓库中“危险工业环境中的机器人自主任务管理”表达方式。后续如果要对比 mission supervisor、inspection workflow 和 transition controller 之间的文字差异，这篇论文会很有参考价值。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 1 页摘要和引言，把系统对象、危险环境假设以及“all system components into a state machine”这个总纲读清楚；然后直接跳到第 5-6 页的 `E. State Machine` 和 `Figure 6-7`，这里已经列出了七个任务、状态推进顺序、重复条件和失败处理，是重做 `STM.md` 的核心区域。

像中间关于 reduced-order model、CBF safety filter 和 transition trajectory generation 的内容，可以放在第二轮阅读来补连续控制背景。若要快速恢复离散控制主链，优先保住的仍然是七个任务状态、goal added/modified 的重复条件，以及 failed transition 的停机语义。
