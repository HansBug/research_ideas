# 基于状态机输出的监督控制实现 / Modelling and Implementation of Supervisory Control Systems Using State Machines with Outputs

## 论文在讲什么

这篇文献讨论的是如何把监督控制理论合成出来的 supervisor 转换成更适合控制器实现的 `Mealy state machine with outputs`，并最终落到 PLC Ladder 代码上。它本身明显是一篇方法型章节，但作者没有只谈算法，而是用一个制造系统案例完整展示 plant、specification、supervisor、state-machine simplification 直到 implementation 的全过程。

对样本库最重要的部分就是这个 manufacturing example。它由三台 apparatus 和两个容量为 `1` 的 intermediary buffers 组成，控制目标是避免设备完成任务时下游缓存已满，或设备启动时上游没有工件。也就是说，虽然整章在讲 formal methodology，但中间这套设备-缓存协调逻辑本身就是一个清晰的离散事件控制对象。

## 控制系统在文中的位置

控制系统在文中既是方法的输入输出，也是具体案例载体。前几节在介绍 SCT、monolithic supervisor 和 Mealy machine 语义时，都是为了让后面这个制造系统的 supervisor 能够被转换、约简并实现。作者不是临时拿一个小例子点缀，而是让整个方法链围绕这套系统展开。

更具体地说，文中最可复用的是两层描述。第一层是 physical meaning：`A1-A3` 是三台设备，`B1-B2` 是两个缓冲区，`ax` 是启动操作，`bx` 是操作完成。第二层是控制语义：哪些 `b` 事件会让哪些 `a` 动作可用、哪些事件只是被记录、哪些组合事件会在同一扫描周期里触发多个输出动作。这对我们提取状态机自然语言样本非常关键，因为很多监督控制论文只给抽象 automata，而这篇还能把控制意图说回具体设备链。

## 对我们为什么有用

它对 `sources/` 的价值首先在于补了一个很干净的 `FSM + T0` Mealy 监督控制样本。相比很多更偏 verification 或 synthesis 的 DES 论文，这篇在状态、事件和动作之间的映射关系上更直接，特别适合后续拿来做“事件触发 + 输出动作 + buffer 约束”型自然语言建模样本。

其次，这个案例还能补一种很重要的表达形态：有些控制器的核心不是显式时间和复杂 mode names，而是“哪些事件组合成立时允许哪些动作”的协调关系。对于后续研究 LLM 从非形式化文本中恢复 EFSM/FSM 时，这类事件-动作监督链与传统 PLC 顺序控制链是不同的样本类型，值得保留。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `4` 节 motivation example，把 system composition、`ax / bx` 的物理含义，以及 overflow/underflow 这两个规范目标先捋清楚。只有把三设备双缓存的约束关系看明白，后面看到 `b1-a2`、`b2-a3` 和组合事件时才不会把它误读成纯形式符号游戏。

接着直接跳到第 `9-12` 页，读 `8-state Mealy machine` 和 `reduced 4-state machine` 两部分，重点关注 state naming、slash 后面的 output actions、dashed self-loop 的含义，以及 `b1 & b2` 这类组合事件如何触发 `a1 / a2 / a3`。至于前面的 supervisor synthesis 背景、Grail、PLC 同步控制器实现问题，可以放到第二轮再看；如果当前任务是重做 `STM.md`，优先级最高的仍是 manufacturing example 本身。
