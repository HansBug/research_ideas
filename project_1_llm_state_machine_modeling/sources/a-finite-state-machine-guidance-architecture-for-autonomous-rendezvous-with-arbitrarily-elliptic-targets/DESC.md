# 面向任意椭圆目标轨道的自主交会有限状态机引导架构 / A Finite State Machine Guidance Architecture for Autonomous Rendezvous with Arbitrarily Elliptic Targets

## 论文在讲什么
这篇论文解决的是航天器在任意椭圆目标轨道附近的自主交会引导问题。输入是相对漂移、hold point、relative orbit 状态和任务时间线，方法是构造 `WSE / SSE` 双主状态的分层 FSM，并在下层挂接 drift、safe sizing 和 station keeping 等控制模块，输出是可安全执行的交会 guidance logic。
从论文的展开方式看，输入侧主要落在 relative drift、hold point、keep-out-zone margin、mission timeline、relative orbital elements，核心做法是 layered FSM + truth tables + maneuver library，最终形成的则是 自主交会 guidance layer 与仿真验证结果。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文把 guidance layer 明确组织为两大主状态，例如 `WSE`：Walking Safe Ellipse、`SSE`：Stationary Safe Ellipse。
这篇论文不是单纯 `T0` 的模式管理，因为它给了，例如 hold duration、drifting period、`TTL` 触发的重新计算。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文补充了当前 `sources` 中较少见的交会/近距离操作方向 HSM 样本。 它的状态名字、判定条件和时间阈值非常适合直接转写成状态机自然语言描述。 与一般只讲轨道控制方程的论文不同，它把高层 mission guidance 的状态骨架讲清楚了。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `main state + manager truth table + control submodule` 的层次化写法、`hold point / TTL / drift threshold` 这套时间和空间条件表达、在一个状态机中融合 `move/stop + sizing + waiting + correction` 的复合控制叙事 这些最容易直接转成状态机自然语言描述的部分。 低层机动求解仍然带有较多轨道动力学公式，不适合全部直接当作状态机文本。 结构图重要性很高，抽取时必须结合 Figure 4/5 与 Table 9。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。
