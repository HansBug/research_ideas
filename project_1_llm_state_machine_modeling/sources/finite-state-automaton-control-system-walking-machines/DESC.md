# 通用控制与形式化工具 / Finite state automaton based control system for walking machines

## 论文在讲什么

这篇论文关注的是 walking machine 的控制系统设计，作者用一个 hexapod 机器人来验证方案。文章的重点不是机械结构本身，而是如何把行走机器人复杂的导航、动作和步态选择过程拆成一组层次化、可复用的有限状态自动机。作者明确说控制结构采用了 hierarchical top-down decomposition：高层发任务给中层，中层再向下层发需求，每个过程都被视作一个单独的 finite state automaton。

这使它天然不同于很多只讲步态规划或逆运动学的机器人论文。作者不是在连续控制层面谈腿轨迹生成，而是把系统控制骨架拆成 global navigation FSM、local navigation FSM 和 gait sub-behaviour FSM，并继续说明不同状态各自读写哪些 repository、在什么条件下跳转。因此这篇文献对 `sources/` 的价值，不是“机器人领域又多一篇”，而是它提供了一条很清晰的层次状态机控制链。

## 控制系统在文中的位置

控制系统结构就是本文主角。论文第 3-6 页连续几节都在解释控制系统如何分层、global navigation 负责什么、local navigation 负责什么、为何还要在 motion behaviour 下面再挂一层 gait FSM。也就是说，我们关心的状态机描述不是附带案例，而是作者提出的整套 walking-machine control architecture 的核心表达方式。

从 `sources/` 的角度看，这篇文献也不只是“画了几个状态图”的软样本。作者不仅列出状态名，还交代了 obstacle、heading error、out-of-corridor、fault 等 guard 如何通过 whiteboard repository 触发状态迁移。因此它适合作为机器人/通用控制方向里那类“层次化导航监督器”的高质量样本，而不是只能保留抽象框架印象的背景文献。

## 对我们为什么有用

当前 `⚙️` 方向已经有一些机器人监督器和 mission FSM，但很多样本更偏单层任务流，或者主要关注某个具体应用场景。这篇 walking-machine 论文补的是另一类非常有价值的结构：高层负责任务和全局导航，中层负责本地运动和避障，底层再决定 tripod / wave 等具体 gait。这种“三层职责分解 + 自顶向下请求链”的写法，对后续训练模型理解层次状态机特别有帮助。

它还有一个附加优势，就是 guard 信息写得比较实。论文没有把状态迁移说成模糊的“根据环境切换”，而是给出 `ffault`、`fleftobs`、`foutofcorridor` 这类具体条件，让我们能把状态机自然语言描述写得更靠近工程事实。这种既有层次、又有 guard 的样本，在通用机器人控制里并不算常见，因此值得作为 `💎` 核心样本保留。

## 如果需要人工细读，建议怎么读

人工细读时，建议先读 `Control system structure`，确认层次划分、process 之间的任务传递方向，以及“each process is treated as a separate finite state automaton”这条总原则。之后立即跳到 `Global navigation FSM` 和 `Local navigation FSM` 两节，先把 global 层和 local 层分别有哪些状态、每层解决什么问题、两层如何衔接读清楚。

第二轮再看 gait sub-behaviour 和 OnEntry / OnExit 条件说明，重点核对 `Stripod / Swave` 的选择条件，以及 `ffault`、`fleftobs`、`foutofcorridor` 这些 guard 如何驱动状态跳转。至于逆运动学、底层动作实现和更一般的多足机器人背景，可以暂时放在后面，因为它们对理解整篇论文当然重要，但对重建层次 FSM 主链的优先级低于状态集合、层次边界和迁移条件。
