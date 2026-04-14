# 感知 cue 驱动的 UGV 上下文切换导航 / Using perception cues for context-aware navigation in dynamic outdoor environments

## 论文在讲什么

这篇论文讨论的是一个在动态户外环境中运行的小型 `UGV`，它不是只会做普通避障，而是会根据感知到的上下文在不同导航行为之间切换。作者把 terrain-aware、socially compliant 和 covert 三种 learned behavior 放进一套统一系统里，再让 perception stack 通过 pedestrian 和 weapon cue 去驱动高层 behavior executor 的状态切换。

因此，这篇论文关注的不只是“某个导航算法好不好”，而是一个真实机器人如何在任务环境变化时改变自己的行为模式。它既有感知模块，也有学习到的 traversal behavior，但真正让它适合作为 `sources/` 样本的是那条显式的高层状态机：状态、优先级和切换动作都被正文写出来了。

## 控制系统在文中的位置

控制系统描述在文中是主线的一部分，而不是附带示意。作者先解释 autonomy architecture，再明确说 behavior executor 会根据 perception 输出在不同 navigation module 之间切换，随后在第 12-13 页把 Figure 9 的 state machine 展开，直接说明有 `IDLE / NORMAL / PEDESTRIAN / THREAT / DONE` 五个状态，以及何时从 normal 切到 pedestrian、何时被 threat 抢占。

这让它和一般“感知 + 规划 + 控制”流水线论文不一样。这里不是简单地把不同模块串起来，而是让一个显式 supervisor 去决定当前该激活哪个行为模块、何时取消旧模块、何时重发目标、何时保持 covert 模式直到任务结束。对状态机数据集来说，这是非常直接的监督控制样本。

## 对我们为什么有用

当前 `⚙️` 方向里，真正把 perception cue 写成高层 guard 的样本并不多。这篇论文补进来后，可以显著增强“感知驱动行为切换”的监督控制案例，与传统 PLC 顺序控制、工业机器人装配链、固定 mission FSM 形成明显差异。它不是单纯地列几个 mode name，而是把 `P` 和 `T` 两类 cue 与优先级、取消动作和后续控制器激活一并写清楚。

它也补了一个对后续自动建模很重要的模式：这里的控制对象不是低层速度闭环，而是一个 mission-level behavior executor。对 `project_1` 来说，这种样本有助于模型学习“感知条件如何驱动行为模式切换”，而不是只会还原简单工序顺序。

## 如果需要人工细读，建议怎么读

人工细读时，建议先读摘要和第 6-7 页 architecture 总览，只要确认这篇论文到底有哪些 navigation behaviors，以及 perception 在系统里扮演什么角色。然后直接跳到第 12-13 页 `3.3 Navigation`，重点看 behavior executor 的 Figure 9 和与之配套的文字，把五个状态、`P`/`T` 触发、优先级、cancel 当前模块以及 send new goal 这些动作先读完整。

之后再回头看 perception 和 learned behavior 细节，例如 pedestrian tracking、weapon detection、IOC 正常模式和 covert 模式的训练过程。这些内容有助于理解为什么切换有效，但如果目标是恢复状态机主链，它们的优先级低于 behavior executor 那几段直接控制描述。
