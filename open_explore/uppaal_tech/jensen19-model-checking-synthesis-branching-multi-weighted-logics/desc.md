# Model Checking and Synthesis for Branching Multi-Weighted Logics

- 问题一句话：`UPPAAL` 相关优化/博弈模型常常同时涉及时间、代价、能量等多资源，但传统逻辑很难同时表达 branching-time 结构和多资源硬约束。
- 方法一句话：论文定义带多非负权重的 Kripke/game 结构与扩展 `CTL`，先用 `cut` 和常数边界获得可判定模型检查，再把 reachability synthesis 编码成 dependency graph 的最小不动点问题。
- 解决点一句话：它把多资源 branching-time 逻辑从“表达上可写”推进到有明确 undecidability/PSPACE/EXPTIME 边界和 on-the-fly synthesis 算法的状态。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，而且在 `UPPAAL` 技术线上更偏**逻辑与算法理论扩张**而不是工具工程。它没有直接讨论 timed automata 的 clock 数据结构，也不是某个具体 `UPPAAL` 产品分支的用户手册，而是在回答：若我们想在 `UPPAAL` 风格 open system / game setting 中同时追踪多个 quantitative resource，该用什么逻辑表达、哪些问题还可判定、合成又该怎么做。

因此它和早期 `timed games / priced timed automata / Stratego` 的关系不是替代，而是补充：

1. 早期工作更多是在模型层面加入 price、time、energy 之类单一或少量资源；
2. 本文则是在逻辑层把这些资源统一提升成多维非负权重，并明确引入 branching-time specification；
3. 它为后续更强的 timed ATL / quantitative synthesis 条线准备了语义和复杂度边界。

在当前文库时间线上，它可以看作 `timed games / compact strategies / TATL` 之间的一块中间理论台阶。

## 立足问题

论文立足的问题，是 open-system synthesis 已经不只需要回答“能不能达到某状态”，还常常需要回答：

1. 是否存在一种控制程序，使得所有运行都满足某些资源上界；
2. 同时又存在一些环境分支，能在另一组资源条件下到达目标；
3. 而这些条件涉及不止一个维度，例如时间、收益、能量、成本。

传统线性时序逻辑只能表达路径上的单一视角；普通 `CTL` 虽然有 branching quantifier，但不擅长把多资源累积约束写进语义里。作者因此提出多权重扩展：在状态转移系统上给每条边贴多维非负权重向量，并让逻辑直接能引用这些累积资源。

从技术上看，困难不止一个：

1. 多资源意味着状态语义不再只依赖当前节点，还依赖沿路径累积到的向量成本；
2. branching-time 逻辑要求同时表达“必须如此”和“可能如此”；
3. 一旦允许逻辑里自由比较不同资源维度或做减法，极容易触发不可判定性。

所以这篇论文的真正目标，不只是“发明一套多资源逻辑”，而是：

1. 明确 full logic 到底何时不可判定；
2. 找到一个足够有用但仍可判定的 fragment；
3. 在 synthesis 侧给出真正能跑的 on-the-fly 解法。

## 核心方法

论文的方法分成三步：先扩模型与逻辑，再做 decidability/complexity 切分，最后为 reachability synthesis 建 dependency-graph 算法。

### 1. 定义 n-weighted Kripke structure 与 weighted CTL

作者首先给出 `n-Weighted Kripke Structure`：

$$ K = (S, s_0, AP, L, T). $$

这里的转移关系不再只是 `S \times S`，而是带一个 $n$ 维非负权重向量。对于一条运行 $r$，在位置 $i$ 的累积成本记作 `cost_r(i)`。

逻辑层则把 `CTL` 扩展为可读写这些累积资源的 `WCTL`。其核心不是直接给每个时序算子绑一个固定时间上界，而是允许在公式里写资源表达式，例如：

1. `#i`
   - 第 `i` 维资源当前累积值；
2. `reset #i in φ`
   - 在子公式 `φ` 的求值上下文里把某些资源清零；
3. `e ./ c`
   - 比较资源表达式与常数。

于是逻辑既能表达安全/可达这样的 branching-time 结构，也能表达多资源约束。

### 2. 先证明 full logic 不可判定，再切出常数边界 fragment

论文第一大结果很直接：full `WCTL` 在有限 3-weighted Kripke structure 上就已经 undecidable。作者通过把两计数器 Minsky machine 编码进三维权重，证明只要逻辑里能自由比较维度、做减法或模拟计数器平衡，就能恢复经典不可判定性。

这一步很关键，因为它说明作者不是盲目扩张表达力，而是先把边界画出来。

随后论文对逻辑做约束，得到 `cb-WCTL`：所有 bounds 只能和常数比较。此时作者引入 boundary vector 与截断函数 `cut`，把无限增大的代价向量压成有限抽象：

$$ \mathrm{cut}(w)[i] = \min(w[i], b[i] + 1). $$

这里 $b$ 来自公式中出现的最大常数边界。这个构造的思想很朴素但非常有效：一旦某个资源分量已经超过“所有公式还能关心的最大界限”，继续增大也不会改变公式真假，于是可以统一折叠成 `b[i] + 1`。

基于这个 `cut`，论文把 `cb-WCTL` 的 model checking 重新压回有限展开，并证明复杂度是 `PSPACE-complete`。  
这一步的方法价值在于：它没有试图保留 full exact cost，而是抓住“公式实际还能分辨到哪”为止。

### 3. 再把模型扩成 multi-weighted game structure，定义 synthesis

在 synthesis 侧，作者把结构提升成带 controllable / uncontrollable 转移的 `n-WG`。这里的 open-system 视角和 `UPPAAL Tiga/Stratego` 一脉相承：控制器选择可控转移，环境解析不可控分支，最终得到 strategy-restricted graph。

论文关心的问题是：是否存在策略 `s`，使得受该策略限制后的系统满足某个 `WCTL` 公式。

对于一般 `cb-WCTL`，策略记忆需求会很高，甚至需要记住 run 上哪些 uncontrollable branch 被走过。这一点论文通过例子强调：不是只看当前 state 就能定义 winning strategy。

### 4. 对 upper-bounded fragment 给出一般 decidability 结果

论文随后考虑 `ub-WCTL`，即 temporal operators 本身带 upper-bounds，并فرض模型满足 cost-convergence：任何 cycle 在被公式关心的维度上都必须继续增长。

这样一来，只要 run 足够长，所有上界都会被冲掉，对应公式真假会变得稳定。作者因此证明：在 cost-convergent model 上，`ub-WCTL` synthesis 是 decidable 的。

这个结果本质上是说：若资源沿循环必然前进，而且逻辑只看有限 horizon 内的上界性质，那么策略搜索空间虽然大，但终究可截断。

### 5. 为 reachability fragment 设计 dependency graph 编码

真正最有算法味的部分在第 5 节。作者把 `WReach` 这一 reachability fragment 的 synthesis 问题编码到 dependency graph。  
每个节点形如：

$$ \langle (s, w), AF\, y \rangle $$

或对应的中间决策节点，表示“在状态 `s`、累积资源 `w` 下，是否存在策略保证最终满足目标原子公式 `y`”。  
依赖边的生成规则分三类：

1. 若当前已满足目标，就直接指向真；
2. 若当前有 controllable transitions，则枚举策略选择；
3. 再把环境的 uncontrollable 后继全部展开成依赖目标。

这里再次用到 `cut(w)`，保证即使资源理论上可以无限增长，dependency graph 仍是有限的。

### 6. 用最小不动点赋值求解 winning strategy

对 dependency graph，作者考虑布尔赋值 `A : V \to \{0,1\}`，并定义单调算子 `F(A)`。由于赋值空间形成完备格，最小不动点 `A_G^{min}` 存在。  
论文证明：

1. 若根节点在 `A_G^{min}` 中取值为 `1`，则存在 winning strategy；
2. 反之，若有 winning strategy，则根节点必被最小不动点标成 `1`。

也就是说，reachability synthesis 被规约成了 dependency graph 的最小不动点赋值问题，而后者可以 on-the-fly 线性求解。

这一步是整篇论文最像 `UPPAAL` 团队算法风格的地方：不是先铺满整个 game graph 再离线做解，而是尽量把问题压成局部展开、局部传播的依赖图。

### 7. 给出复杂度边界：`EXPTIME-complete`

在 reachability fragment 上，论文进一步证明 synthesis 问题是 `EXPTIME-complete`。hardness 来自 countdown games 规约；membership 则由：

1. `cut` 后 dependency graph 的有限性；
2. 最小不动点算法的线性时间；
3. 以及图大小对维度数的指数依赖；

共同得出。

因此本文最终不是只给了一个“能做”的算法，而是把从 undecidability、到 `PSPACE` model checking、到 `EXPTIME` reachability synthesis 的整条复杂度地图都补上了。

## 解决了什么问题

这篇论文解决了三个层面的关键问题。

第一，它明确说明 full multi-weighted branching-time logic 很快就不可判定，从而避免后续工作在错误的表达力预期上空转。

第二，它给出了一个足够有用的 `cb-WCTL`/`ub-WCTL` 可判定子集，并用 `cut` 机制把无限累积资源重新压成有限分析对象。

第三，它在 reachability fragment 上给出真正的 on-the-fly synthesis 算法，把 winning strategy 问题转成 dependency graph 最小不动点计算。这一点让逻辑不再只是“有语义”，而是真的进入了算法层。

## 与 `UPPAAL` 技术线的关系

这篇论文与 `UPPAAL` 技术线的关系主要体现在三方面。

1. 它延续了 `UPPAAL` 团队长期关注的 open-system / game-theoretic 视角，与 `Tiga`、`Stratego` 的问题设置高度同构。
2. 它把“多资源”从 priced timed automata 或单一 cost objective 提升到了 logic 层和 synthesis 层，因此比早期 price/game 工作更抽象、更 general。
3. 它又为后续更强的逻辑工作铺路，例如 timed ATL / coalition reasoning / 更复杂的 symbolic dependency-graph 算法。

如果放在当前文库时间线里看，它很适合作为：

1. 早期 `priced/timed games` 线的逻辑提升；
2. `compact strategies / stochastic hybrid games` 之前的多资源语义补完；
3. 后续 `TATL` 线的一块前置逻辑基础。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。原因是：

1. 模型与逻辑定义完整；
2. 不可判定性、可判定 fragment、dependency graph 编码、复杂度证明主线都写清楚了；
3. reachability synthesis 的算法结构已经足够让人复现主要思想。

从实现可获取程度看，更适合标 `🟥 暂未获取实现源码`：

1. 论文主要是逻辑与算法结果；
2. 没有看到稳定公开的代码仓库直接提供这篇论文的 model checker / synthesizer；
3. 因此目前能获取的是理论方法，而非论文级源码实现。

## 对本研究的启发

对当前博士研究，这篇论文有两个很强的启发。

第一，它说明一旦把“成本/资源/时间”提升成逻辑对象，必须非常小心 decidability 边界。对你后续如果要让 LLM 自动生成性质或验证场景，这种边界意识很重要。

第二，`cut` 与 dependency graph 的设计展示了一种很典型的 `UPPAAL` 式思路：与其死保留所有精细数值，不如抓住“公式还能分辨什么”和“局部子问题如何依赖”这两个本质维度。对自动验证与模型修复流程里的状态压缩、任务分解，都很有借鉴意义。
