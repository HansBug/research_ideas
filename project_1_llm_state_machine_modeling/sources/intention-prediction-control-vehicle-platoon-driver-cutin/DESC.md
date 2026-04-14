# 基于意图预测的车辆编队 cut-in 应对控制 / Intention Prediction-Based Control for Vehicle Platoon to Handle Driver Cut-In

## 论文在讲什么

这篇论文讨论的是混合交通里一个很现实的问题：当人驾车辆试图插入自动化车队时，车队到底应该收紧队形阻止 cut-in，还是主动让出安全距离。作者提出的方案把整个问题拆成两层：前面是一套意图与轨迹预测模块，判断人驾车是否要 cut-in、是强制还是自由 cut-in、以及它处在可防止还是不可防止区间；后面则是一个高层 FSM 加低层预测控制器，把这些判断转换成实际的车队纵向控制策略。

论文并不是泛泛地谈“预测 + 控制”，而是把高层模式机写得很清楚。`CF`、`cut-in prevention` 和 `cut-in yielding` 三个状态分别对应正常跟驰、缩短车距防插入和主动让行，低层 MPC 再去执行各状态下的纵向控制策略。随后作者通过 driver-in-the-loop 实验，分别验证无 cut-in、mandatory cut-in 和多种 discretionary cut-in 场景下 FSM 是怎样切换的。

## 控制系统在文中的位置

我们关心的控制系统描述在文中属于核心方法，而不是某个局部模块。整篇 Section IV 都围绕高层 FSM 和低层 predictive control 展开，高层模式选择器是把“预测结果”落到“控制行为”的关键接口。如果没有这个 FSM，前面的意图预测只会停留在识别层，无法真正说明车队该怎么做。

更重要的是，这个高层控制器同时保住了正常链和让行/防插入分支。论文并不是只说“检测到 cut-in 就让一下”，而是把 mandatory 与 discretionary 区分开，又把 preventable 与 unpreventable 区分开，再据此决定进入 `cut-in prevention` 还是 `cut-in yielding`。这让它非常适合做混合交通协同控制的状态机样本。

## 对我们为什么有用

对 `sources/` 来说，这篇文章能补足汽车与道路车辆方向里“编队控制 + 人驾车交互”的样本，而不仅是单车换道或单车行为规划。当前文库里虽然已有 lane change、overtake、urban behavior planner 一类控制器，但涉及“自动化车队与外部人驾车辆冲突协商”的状态机样本并不算多，这篇恰好把这种交互写成了很清楚的三态 supervisor。

它对后续自动建模也很有价值，因为状态名字、模式含义、转移 guard 和实验观测都比较集中。后续如果需要把自然语言恢复成高层状态机，或者想在验证失败后回原文补 guard，这篇论文里的 `mandatory/discretionary`、`preventable/unpreventable`、`reach the target lane` 等条件都很适合作为明确的建模锚点。

## 如果需要人工细读，建议怎么读

如果要人工复核 `STM.md`，建议先看第 1-2 页摘要和引言，确认控制目标到底是“保持 platoon 完整性”和“保证道路安全”之间的折中，而不是普通单车跟驰。随后直接跳到第 5 页的 `IV-A High-Level FSM`，把三个状态、四类核心 guard（是否有 cut-in 意图、mandatory/discretionary、preventable/unpreventable、是否到达目标车道）逐个标出来。再接着看第 9-10 页 mandatory / discretionary cut-in 实验里的状态轨迹图，核对这些 guard 在真实试验里是怎么触发模式切换的。

至于前面的意图预测算法细节、后面的 MPC 数学模型和参数推导，可以放到第二轮再看。它们当然影响控制性能，但如果当前目标是提取状态机样本，第一轮更值得先固定的是模式集合、状态转移边界和“为什么从 `CF` 去 `prevention` 或 `yielding`”这条高层控制链。
