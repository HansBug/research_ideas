# 工业 AGV 三模式监督控制 / Safe Performance of an Industrial Autonomous Ground Vehicle in the Supervisory Control Framework

## 论文在讲什么

这篇论文研究的是一个工业 Autonomous Guided Vehicle (AGV) 在 supervisory control framework 下的安全控制问题。作者把整台 AGV 拆成多个 discrete event subsystems，再用 Ramadge–Wonham 框架和 Supervisory Control Theory 去建模、证明 controllability，并验证受控系统的 nonblocking 性质。

与很多只讲“AGV 调度”或“AGV 路径规划”的文章不同，这篇论文真正关心的是 AGV 各子系统本身的离散控制结构。文中不仅讲总体框架，还把 operation modes、drive motor、steer motor、传感器和按钮等子系统分别写成自动机，再通过同步积形成整机控制模型。

## 控制系统在文中的位置

我们关注的控制系统描述在文中是主体，不是案例外壳。作者的主要贡献就是把 AGV 的控制对象逐个翻译成 DES automata，再配上 supervisory automata 去实现安全性能。因此，像 `emergency / reset / active` 这样的 operation subsystem，并不是附图，而是整篇文章最基础的控制单元之一。

这也意味着这篇论文非常适合做“形式化控制样本”的来源。原文不只说“AGV 有几个模式”，而是把状态集、事件集、初始状态、允许事件、转移函数和可控/不可控事件分区都列了出来。对于 `STM.md` 来说，这种正文密度通常比只给一个流程图更容易稳定落到双 A。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补的是工业 AGV 方向里一个偏正式、偏 supervisory 的离散控制样本。库里虽然已有不少 PLC 和制造单元控制器，但这种“从 operation subsystem 开始就直接给出 DES 六元组”的 AGV 监督控制论文并不多，尤其适合后续做“从自然语言恢复显式自动机元素”的抽取任务。

它的另一个价值在于控制语义很干净。以 operation subsystem 为例，`emergency / reset / active` 这三个模式以及 `switch to reset / active / emergency` 三类命令就已经构成了一个结构完整的监督 FSM；如果后续需要更复杂的多自动机组合，还可以继续回原文扩展到 drive motor 或 steer motor 子系统。

## 如果需要人工细读，建议怎么读

人工回原文时，建议先读摘要与 `2.2 Operation Subsystem`，优先把 AGV 被拆成哪些子系统、operation subsystem 在其中承担什么角色看清楚。然后把 `GMM` 的状态集、事件集、active-event set、transition function 和 controllability 一口气读完，因为这是最直接的 `STM` 主链。

如果后续需要补更复杂的控制层次，再继续读 `2.3 Drive Motor Subsystem`、后面的 steer motor 与 supervisory automata 部分，确认 operation subsystem 如何和执行部件自动机同步。仿真和 formal proof 段落可以第二轮再看，因为第一轮做样本抽取时，`GMM` 已经足够独立成型。
