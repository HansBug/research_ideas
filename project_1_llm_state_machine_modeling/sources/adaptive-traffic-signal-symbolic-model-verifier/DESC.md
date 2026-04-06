# 自适应交通灯状态机 / Modeling and Verification of Agent based Adaptive Traffic Signal using Symbolic Model Verifier

## 论文在讲什么

这篇论文研究的是一个两条道路交叉口上的 adaptive traffic signal system。作者的目标不是做传统固定配时，而是让信号灯根据当前车道排队长度动态调整绿灯持续时间，并把这一套设计转写为 FSM，再用 NuSMV 检查 CTL 性质。论文篇幅不长，但问题定义、控制变量和状态转换图都比较集中，所以很适合做 `sources/` 里的交通信号强样本。

更具体地说，作者把四种可能的绿灯组合当成四个离散状态，让系统按 `NORTH -> WEST -> SOUTH -> EAST` 的 weighted round-robin 顺序轮转。绿灯时长不是预设常数，而是由入口/出口监测代理统计的当前排队长度决定，并受 `Tthr` 上限约束。这样，论文保留下来的不是“交通流优化思想”，而是一个真正可以直接读成状态机的控制器。

## 控制系统在文中的位置

这里的控制系统描述是论文的核心对象。NuSMV 和 CTL 只是后续验证工具，前提是作者先把交通信号系统设计成一个带状态、变量和计数器的离散控制模型。如果没有前面那套 phase order、queue-length counting、`CV=min(Tcal,Tthr)` 和 `wait time counter`，后面的验证根本无从谈起。

这也意味着它和很多只把交通灯当成验证示例的论文不一样。文中既没有把状态机缩成一句话，也没有只给一个抽象框图，而是把 `Turn` 的语义、四个方向相位、主代理如何汇总入口/出口计数、何时切换下一相位都说明白了。对 `sources/` 来说，这正是最需要的那种“验证论文里仍然保住了完整控制链”的样本。

## 对我们为什么有用

它对当前文库最直接的价值，是补了 `🚦` 方向里一个非常干净的 `EFSM + T1` 样本。交通灯方向虽然样本不少，但很多稿子偏 `PLC prototype`、图像感知、或只是固定周期灯控；这篇的优势在于它把“相位 + 计数器 + 阈值 + 等待时间”四件事合成了一套明确的扩展状态机，因此既保留了传统 signal phase，又保留了动态变量驱动。

这篇论文也有很好的检索启发价值。它说明 traffic 方向真正高命中的不是宽泛的 `smart traffic`，而是 `adaptive traffic signal + weighted round-robin + Tthr + counter + wait time` 这种词簇。后续若要继续补更强的交通样本，应优先找这种“相位轮转和定时/计数变量都写得很实”的文章，而不是只讲优化算法或感知系统的稿件。

## 如果需要人工细读，建议怎么读

人工重读时，先看第 `1` 页摘要和引言末尾，确认作者确实是把场景转成 FSM，而不是只做策略比较。然后直接跳到第 `2-3` 页的设计部分，把 `Tthr`、`tv`、Entry/Exit agents、Master agent、queue length 和 `weight` 的关系先抽出来；这是理解控制逻辑的关键。接着再看第 `4` 页 `State Transition Diagram`，把 `Turn=0..3` 的相位映射、`CV=min(Tcal,Tthr)`、counter 递减和 `wait time counter` 一并核对，基本就能重建 `STM.md`。

CTL 公式和模型检查结果可以第二轮再读。它们对理解论文为什么正确很重要，但对第一轮抽状态机并不是最优先。第一次阅读只要把 phase order、动态权重分配和等待时间测量读清楚，就足以把这篇论文当作一个结构完整的 traffic-signal EFSM 样本重新写出来。
