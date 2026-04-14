# 可靠无人机架构中的航路点避碰状态机 / Designing a Reliable UAV Architecture Operating in a Real Environment

## 论文在讲什么

这篇论文整体上讲的是一个面向真实运行环境的 reliable UAV architecture 设计过程。作者从 FHA、FTA、MBSE、UML、SIL 等角度讨论如何把无人机系统从 use case、state machine 一路推到最终算法和测试方案，因此它并不是一篇只盯着单个控制器的小论文，而是一篇带有系统工程气质的 UAV 架构设计论文。

不过，对 `sources/` 来说，它真正值得保留的核心不是那些规范和架构流程，而是文中 `WAYPOINT` flight mode 下的 collision-avoidance state machine。作者把“正常按航路点飞行”和“检测并处理空中冲突/地形障碍”组织成一套明确的 mission-level state machine，而且还区分了单线程和双线程实现方式，这使得它超出了泛泛架构论文的层次，形成了可以直接抽样的飞行控制样本。

## 控制系统在文中的位置

这里的控制系统描述虽然不是论文唯一主题，但它是作者把架构落到具体飞行任务上的主要载体。文章先给出 `WAYPOINT` 模式的 use case，再映射到 Figure 2 / Figure 3 的 state machine，然后进一步说明 `testCollision()` 与 `findWPT()` 在状态内承担什么处理。也就是说，state machine 不是用来装饰 UML 方法论的示意图，而是支撑 collision-avoidance scenario 的核心行为模型。

这篇论文需要如实把边界说清楚：它整体确实偏 architecture / certification / test-plan 叙述，而不是纯控制算法论文。但这并不妨碍其中的 `FWM1/FWM2/FWM3/FWM4/SUP/ExS1/ExS2` 构成一个足够具体的离散控制对象。对文库而言，保留的是这套 mission supervisor，而不是整篇论文的系统工程讨论。

## 对我们为什么有用

它对当前文库最大的价值，是补了 `✈️` 方向里一种很实的 mission-level `HSM + T0` 样本。航空航天方向很多论文都会漂向连续飞控、轨迹优化、估计与避障算法；而这篇提供的是更适合状态机建模的数据形态：航路点选择、飞往目标点、配置识别传感器、supervisor 检查、进入避碰流程、再回到主航线。这样的状态链对后续自动建模任务非常友好。

它也给检索策略带来很明确的提醒。单看题名里的 `architecture` 很容易误判成低命中方法稿，但如果正文里明确出现 `Use Cases -> State Machine diagrams -> final algorithms`，并且 `WAYPOINT + collision avoidance + supervisor + exceptional situation` 这些词真正落到图和正文链路上，那么这类论文就值得保留。也就是说，航空方向不能简单把 `architecture` 全部降权，关键要看它有没有把 mission logic 写实。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `1` 页摘要和第 `8-10` 页的 Section `3 Modeling of UAV Architecture`，快速确认作者讨论的是 `WAYPOINT` mode 下的 collision-avoidance scenario，而不是宽泛的 UAV 架构。然后重点读第 `9-10` 页的 Figure 1、Figure 2、Figure 3 及其配套文字，先把 `FWM1/FWM2/FWM3/FWM4/SUP/ExS1/ExS2` 这些状态的职责抽出来，再核对 nominal path 和 emergency path 的执行顺序。

如果只是为了重建 `STM.md`，前面的 FHA/FTA 规范背景、后面的数值方程、SIL 测试架构和开放式硬件架构讨论都可以第二轮再看。它们说明这套系统为什么可靠，但不是第一轮抽状态机的关键。第一次阅读只要抓住 `WAYPOINT` 主链、异常链、并行线程和 `testCollision/findWPT` 两个状态内动作，就足够把这篇论文作为 flight-mission HSM 样本稳定重建出来。
