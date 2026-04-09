# 工业过程控制实体分层状态机行为模型 / A New State Machine Behaviour Model for Procedural Control Entities in Industrial Process Control Systems

## 论文在讲什么

这篇论文表面上是在提出一种新的 state machine behaviour model，但它不是只停在形式化层面，而是把这一模型落到一个真实工业项目里的气力输送控制案例上。作者关心的是慢响应连续/批处理过程里，很多动作并不是瞬时完成的，传统状态机只让 `do/loop` 序列有持续时间，会让工程实现显得别扭，因此他们重新设计了 procedural control entity 的状态机语义。

为了证明这种新语义有意义，论文选了一个 ground ore pneumatic transport 场景，把矿粉从储料仓送往 dosing silo 的过程写成有顶层运行态、有嵌套子状态、而且每段 filling/emptying sequence 都带持续时间的分层状态机。对我们来说，真正有价值的就是这部分工业控制案例。

## 控制系统在文中的位置

这里的控制系统既是方法验证载体，也是论文里最具体、最可落地的行为对象。作者虽然用了不少篇幅解释为什么现有状态机在慢过程上不够自然，但最终所有论点都落到 Figure `8/9` 的 pneumatic transport 状态机上，通过它来展示新模型和传统模型在复杂度与可表达性上的差异。

因此，这篇论文不能简单归成“纯方法论文”。它的方法性确实很强，但气力输送 controller 的顶层状态、`Running` 超状态、`Emptying` 的嵌套结构以及 filling 持续序列都写得很清楚，足以独立抽成一条高质量 `STM`。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补进的是 `🏭` 方向里很有代表性的一类样本：不是一般的 `PLC` 启停逻辑，而是“慢工业过程 + 层次状态机 + 持续序列”的 supervisor。它能帮助我们把样本库从单纯的 flat `FSM/EFSM` 再往真正的 `HSM + T1` 过程控制语义扩一点。

另外，它也很适合研究 LLM 在面对“状态内还带 durative sub-sequence”的文本时，能否正确恢复层次边界。很多论文只写 `start/run/stop`，而这里把 `Filling` 和 `Emptying` 都拆成更细粒度的 durative 片段，这种写法对自动建模很有训练价值。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `1` 页摘要，把论文到底想解决什么问题先弄清楚：不是所有 action 都该被当成瞬时 transition。随后直接跳到第 `8-10` 页的 `4.2` 到 `4.4`，先把 Figure `8` 里的顶层与嵌套状态完整读出来，再看 `Filling` 和 `Emptying` 为什么要被拆成带持续时间的子段。

如果后面还需要补更细的背景，再回到前面的 state-machine 语义讨论部分。第一次复核不需要先把整篇建模论证都吃透，重点是先锁定这个工业气力输送案例本身的状态骨架，以及“durability of action sequences”如何具体作用在 `Filling` 和 `Emptying` 上。
