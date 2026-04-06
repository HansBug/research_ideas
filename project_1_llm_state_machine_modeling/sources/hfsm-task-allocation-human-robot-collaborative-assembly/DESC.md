# 人机协作装配任务分配 HFSM / A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks

## 论文在讲什么

这篇论文研究的是 human-robot collaborative assembly 中的任务分配问题。作者关注的不只是“人和机器人怎么分工”，而是如何把一个完整装配任务拆成可管理的子任务，再依据能力、工作负荷和执行性能，把这些子任务分配给 human 或 robot agent。论文最终在一个 smoothie machine 的 crusher unit 装配场景上做验证，用 Franka Emika Panda 与人工操作员共同完成装配。

从表达形式上看，它并不是把任务分配写成单次优化求解，而是用 hierarchical finite-state machine 去承载整个控制逻辑。也就是说，论文保留下来的核心不是某个数学目标函数，而是“任务如何被选中、如何被分配、分给人后如何发指令、分给机器人后如何执行、完成后又如何回到下一个任务”的离散控制过程。

## 控制系统在文中的位置

这里的控制系统描述是论文的主角。HFSM 并不是后处理表示，而是作者定义 task allocation framework 的基本组织方式。顶层的 `task selector / task allocator / communication instructor / task executor` 决定控制循环怎么流动；下层的 sub-task state machines 则决定一个 assembly task 如何再被拆成可执行动作。人机协作是通过这两层状态机合起来实现的。

这篇论文也不是停留在“有个框架图”的抽象层。作者明确说明了 `start`、`newtask`、`task finished`、`nomore task` 这些信号如何驱动顶层状态流，同时又给出 crusher-unit assembly 的 28 个任务和并行执行逻辑，说明 HFSM 真正落在一个具体工业对象上，而不是只停留在分工理念层面。

## 对我们为什么有用

它对 `sources/` 的直接价值，是补了 `🏭` 方向里相对少见的 `HSM + T0` 协作装配样本。工业自动化条目里传统 PLC 顺序控制很多，但“任务分解 + 角色分配 + 并行执行”的 HFSM 样本并不多，尤其是像这篇这样既有顶层 supervisor，又有真实装配任务序列和 parallel branch 的文章更少。

它还提供了一类很重要的样本差异：这里的状态机不以定时器和简单 I/O 切换为主，而是以任务阶段、角色分配和并行子流程为主。对于后续做自然语言到状态机建模的数据集，这能帮助模型学到“industrial control”并不只等于 PLC ladder logic，也可能是 HRC 中更高层的协作监督控制。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `1` 页摘要，把 crusher unit、human/robot allocation 和 HFSM 这三件事先钉住。然后直接跳到第 `2-3` 页的 Figure 1 和 Figure 2 相关文字，先抽顶层四个状态、`start/newtask/task finished/nomore task` 信号，以及“子任务状态可串行也可并行”的规则。接着再看第 `6-7` 页的 crusher-unit case，把 28 个任务、task selector structure 和 parallel tasks 的说明拿来核对这套控制链确实落在真实装配上。

工作负荷模型、人体弹簧模型和性能估计公式可以放到第二轮再读。它们对于理解分配依据很重要，但对第一轮重建 `STM.md` 并不是最优先。第一次阅读只要把顶层控制循环、子任务状态机层和真实装配实例之间的对应关系读稳，就足够把这篇论文作为 HRC task-allocation HFSM 样本重新抽出来。
