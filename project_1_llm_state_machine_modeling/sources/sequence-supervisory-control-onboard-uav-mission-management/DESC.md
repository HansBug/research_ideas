# 无人直升机任务序列监督控制 / A Sequence and Supervisory Control System for Onboard Mission Management of an Unmanned Helicopter

## 论文在讲什么

这篇论文讨论的是无人直升机的 onboard mission management 问题。作者不是只给一个飞行动作模块，而是试图在行为式控制和三层体系结构之间做折中，让同一套系统既能执行预设 mission，又能接受地面操作员或机载组件发来的直接命令，并在人工/自动切换时保持安全。

对 `sources/` 来说，最有价值的部分是文中的 `Sequence Control System` 顶层 state chart。作者把 `Mission Mode`、`Command Mode`、`Stand By`、`Slow Down` 以及命令合法性检查都写到了状态机语义里，所以这篇不是泛泛的 UAV 架构论文，而是一篇确实落到了任务监督器上的控制样本。

## 控制系统在文中的位置

这里的控制系统描述处于论文核心位置。文章先讨论为什么 UAV 需要多层 autonomy 和事件驱动决策，然后直接用 state chart 给出 `Sequence Control System` 的顶层行为，再补上 truth table 和 EBNF grammar 去约束外部命令与 mission 序列。这说明状态机不是被动配图，而是这套 mission manager 的主要执行语义。

它与很多只讲 `behavior tree`、`planner` 或 `architecture` 的 UAV 论文不同。这里保留下来的不是抽象软件分层，而是明确的控制对象：什么情况下进入 `Mission Mode`，什么情况下进入 `Command Mode`，如何回到 `Stand By`，以及 mission command sequence 什么时候算合法。

## 对我们为什么有用

这篇论文对文库的直接意义，是补了一条很典型的航空航天 `HSM + T0` 样本。很多 UAV 文献都会漂向路径规划、避障算法、连续飞控或视觉估计；而这篇提供的是更贴近离散建模的数据形态：任务模式、命令模式、安全回退、命令过滤和 mission grammar。

它也告诉后续检索不要简单把 `mission management / architecture` 题名都降权。如果正文里真的出现 `Mission Mode / Command Mode / Stand By / Slow Down / truth table / grammar` 这些词，并且它们构成可执行的状态机主链，那么这类论文反而很适合 `sources/`。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `1` 页的 overview 和第 `4-5` 页关于 `Event-based Model` 的部分，先确认对象是 `Sequence Control System` 顶层 supervisor，而不是泛泛的 UAV 软件分层。随后重点读 Figure 3 附近文字，把 `Mission Mode`、`Command Mode`、`Stand By`、`Slow Down` 和 `Parse Command` 之间的关系整理出来。

如果目标是重做 `STM.md`，第二轮再回看 truth table 和 EBNF grammar 的细节即可。第一次阅读只要抓住顶层状态切换、安全 fallback、以及 `<mission>` 必须 `take-off -> ... -> land` 的约束，就足以把这篇论文恢复成一条稳定的任务监督器样本。
