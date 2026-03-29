# Uppaal Coshy: Automatic Synthesis of Compact Shields for Hybrid Systems

- 问题一句话：对带连续状态和复杂混成动力学的系统，单纯“求一个安全策略”还不够，真正落地时还要能自动生成 shield、处理不可判定的 reachability 近似、并把结果压成足够小的表示。
- 方法一句话：基于分区网格与两人 safety game 合成混成系统 shield，再用系统采样近似 reachability，最后用 `Caap` 把网格型 shield 压成等价 decision tree。
- 解决点一句话：把 `UPPAAL` 的策略/紧凑表示路线推进到“hybrid shield synthesis + compact representation + 与 Stratego 联动学习”的新阶段。

## 论文定位

这篇论文是当前文库里离 `2025` 最近的 `UPPAAL` 技术条目之一，也是 `safe/optimal/compact` 路线在 hybrid shield 方向上的最新落地成果。

它承接的不是普通 timed verification，而是更长的一条策略线：

1. `Tiga` 负责 timed game 下的安全控制合成；
2. `Stratego` 负责安全壳内的统计优化；
3. [ashok19-sos-safe-optimal-small-strategies-hybrid-markov-decision-processes](../ashok19-sos-safe-optimal-small-strategies-hybrid-markov-decision-processes/) 负责把安全/最优策略压成 decision tree；
4. 本文则把这些思想推进到**混成系统的 shield synthesis**，而且明确集成进 `Uppaal`。

所以它不只是“又一个 hybrid 工具”，而是 `UPPAAL` 后期策略研究逐渐走向连续状态空间、屏蔽器、紧凑表示和学习联动的集中体现。

## 立足问题

文章面对的问题有三层。

### 1. 混成系统上的 shield synthesis 很难做成全自动

在离散系统里，shield synthesis 通常归结为有限状态博弈；但在 hybrid / stochastic hybrid 场景里：

1. 状态空间连续；
2. 动力学可能复杂；
3. reachability 自身就可能很难甚至不可判定；

这让“先精确算完 transition relation，再求 shield”的路线很不现实。

### 2. 即使算出 shield，显式网格表示也可能巨大

本文采用的是 partition-based shield synthesis，天然会得到“每个 cell 对应一组允许动作”的表格式表示。网格越细，shield 越精，但存储量也越大。对部署到实际控制器而言，这个体量本身就是问题。

### 3. 现代工作流不只要安全 shield，还要继续在 shield 下学效率策略

文章特别强调 `UPPAAL Coshy` 不只是合成一个 safety shield，而是把它和 `Uppaal Stratego` 连起来：先有 shield 保安全，再在 shield 约束下做 reinforcement learning 求高效策略。这说明本文不是孤立的安全工具，而是更大策略工作流的一部分。

## 核心方法

本文的方法可以拆成两大块：

1. **分区式混成 shield synthesis**
2. **`Caap` 压缩成紧凑 decision tree**

### 1. 用 `EMDP` 形式化连续状态上的控制问题

文章先把目标系统写成 `k` 维 `Euclidean Markov Decision Process`：

$$
M = (S, A, T)
$$

其中：

1. `S \subseteq \mathbb{R}^k`
   - 有界连续状态空间；
2. `A`
   - 有限动作集；
3. `T(s,a)`
   - 给出在状态 `s` 下执行动作 `a` 后，后继连续状态的概率密度。

这里的 shield 是 memoryless nondeterministic strategy：

$$
\sigma : S \to 2^A
$$

要求它的所有 outcome 都保持在安全集合 `\varphi \subseteq S` 内。

这一定义和 earlier Stratego/SOS 路线一脉相承：允许 nondeterministic safe strategy 作为最外层安全壳，然后再在壳内做别的事情。

### 2. 用规则矩形网格把连续状态离散化

由于 `S` 连续，作者引入规则矩形 grid。网格由：

1. granularity vector `\gamma`
2. offset vector `\omega`

决定，把状态空间切成很多 cell。每个 cell 是半开矩形区间的笛卡尔积。

这一步的关键作用是把无限状态问题转成有限 cell 问题。之后再定义一个有限 transition system `T_{M,\gamma,\omega}`：

$$
C \xrightarrow{a} C' \iff \exists s \in C.\ \exists s' \in C'.\ T(s,a)(s') > 0
$$

于是 shield synthesis 就变成了 cell 图上的安全博弈问题。

### 3. 用最大不动点定义安全 cell 集合

对安全性质 `\varphi`，论文先定义立即安全的 cells：

$$
C_\varphi^0 = \{ C \in P^\omega_\gamma \mid C \subseteq \varphi \}
$$

然后定义真正的安全 cells 为满足下式的最大集合：

$$
C_\varphi = C_\varphi^0 \cap \{ C \mid \exists a \in A.\ \forall C'.\ C \xrightarrow{a} C' \Rightarrow C' \in C_\varphi \}
$$

这实际上就是经典 safety game 的 greatest fixed point 版本：

1. 只有当存在某动作，使得所有后继 cell 都仍在安全集中时，该 cell 才安全。

最后得到最宽松的 shield：

$$
\nu_\varphi(C) = \{ a \in A \mid \forall C'.\ C \xrightarrow{a} C' \Rightarrow C' \in C_\varphi \}
$$

再把它提升回连续状态空间：

$$
\sigma(s) = \nu_\varphi([s]_{P^\omega_\gamma})
$$

因此，shield synthesis 的理论骨架非常清晰：网格抽象 + safety fixed point + 提升回原空间。

### 4. 现实实现里，初始安全 cell 通过 systematic sampling 近似

上面定义虽然优雅，但实现有两个困难。第一个是：安全性质 `\varphi` 在 `Uppaal` 里通常是用户给的查询式，而不是能轻易做符号包含判断的几何区域。

于是工具的做法是：

1. 对每个 cell 按规则采样。
2. 检查采样点是否违反 safety query。
3. 只有所有样本都安全，才把该 cell 放进 `C_\varphi^0`。

这不是精确判定，而是系统采样式近似。它体现了本文的一贯哲学：对混成系统里本就难算的东西，优先采用自动、实用、可统计验证的近似方法。

### 5. transition relation 也通过模拟近似，而不是精确 reachability

第二个困难是 `C \xrightarrow{a} C'` 本身的判断。对复杂 hybrid dynamics 来说，精确 reachability 很难算。

`Uppaal Coshy` 的做法是：

1. 从每个 cell 里抽若干样本状态；
2. 对每个动作 `a`，从这些状态出发运行 `Uppaal` 模拟器；
3. 直到再次轮到 controller 做选择；
4. 看模拟落入哪个后继 cell；
5. 把这些 cell 加入抽象 transition relation。

这实际上是 simulation-based abstraction。也就是说，构造安全博弈所需的抽象边，作者不要求精确算出，而是用系统模拟近似得到。

### 6. 用 `m` 次重采样处理随机性

如果系统本身带随机分布，仅靠一次模拟显然不够。于是工具允许用户指定 `m`：

1. 对同一个 sampled state 和 action，重复模拟 `m` 次；
2. 收集多个可能后继；
3. 用这些后继近似抽象转移。

这样虽然仍是 under-approximate / sample-based，但能更稳地覆盖 stochastic outcome。

### 7. 处理无界状态空间与无关变量

实现中还有两个很实际的问题。

#### 7.1 无界空间

很多混成系统没有天然紧边界，比如 bouncing ball 的位置和速度就未必容易先验界定。作者因此引入一个 dummy `C_out`：

1. 样本跑出用户指定边界时，转到 `C_out`；
2. 用户可指定 `C_out` 一律安全、一律不安全，或进一步采样决定。

这让工具对“状态边界不易严格给出”的系统更好用。

#### 7.2 忽略与安全无关的变量

若某些变量只记录 cost 或其他与 safety 无关的信息，可以不放进 grid。这样会大幅减少 cell 数量。论文对 bouncing ball 的示例就指出：

1. 某些 location/cost/clock 变量完全可省。

这实际上是在告诉用户：shield synthesis 的状态抽象，不必机械照抄原模型全部变量。

### 8. 用 `Caap` 把 cell-based shield 压成等价 decision tree

本文第二大贡献是 `Caap`。与 earlier `SOS` 不同，这里不是从 tabular strategy 学一个近似树，而是从 axis-aligned partition 出发，求一个**功能等价但更紧凑**的 decision tree 表示。

其思路是：

1. 原始 shield 其实就是很多 cell，每个 cell 对应一个动作集合。
2. 如果相邻 cell 的动作集合相同，就希望把它们并成更大的矩形区域。
3. 区域继续由 decision tree 里的轴对齐谓词表示。

### 9. `Caap` 的核心：扩张 region，同时满足三条规则

为了合法合并，扩张出的候选 region `R'` 必须满足三条 expansion rules：

1. `R'` 内所有 cell 的动作集合相同。
2. `R'` 不与当前已固定区域重叠。
3. `R'` 不能把原 partition 里的某个 region 切成两个不相连残片。

第三条最关键，因为它保证整体 partition 仍可由矩形区域组成。

`Caap` 算法就从最细 partition 出发，贪心地扩张区域，直到不能再扩，再把结果转回 decision tree。

### 10. 与 `Stratego` 联动：先 shield，再学高效策略

论文展示了完整工作流：

1. 先用 `acontrol` 查询合成 shield。
2. 保存 shield。
3. 用 `Caap` 压成紧凑 representation。
4. 再把 compact shield 读回 `Uppaal`。
5. 在 `under compact_shield` 约束下，用 `Stratego` 学习一个高效但仍安全的策略。

bouncing ball 示例非常清楚地展示了三种对象的区别：

1. 完全不考虑安全的效率策略，会让球掉地上。
2. 仅有 shield 时，安全但随机动作太频繁，不够高效。
3. shielded + efficient strategy，则既安全又不乱打球。

这一步表明 `Coshy` 不是孤立的 shield 工具，而是策略工作流中的安全前端。

## 解决了什么问题

这篇论文主要解决了三个问题。

### 1. 它把 hybrid shield synthesis 做成了 `Uppaal` 中的自动流程

此前同类思想更多停在研究算法层；本文则明确集成进 `Uppaal`，而且支持其较丰富的建模语言。

### 2. 它用 simulation-based approximation 绕开了最难的 reachability 障碍

面对混成系统里 notoriously hard 的 reachability，作者没有试图强行精确求解，而是选择：

1. 抽样安全判断；
2. 抽样后继可达；
3. 再用统计验证查询去补信心。

这是一条很 pragmatical 但非常工程化的路线。

### 3. 它把 shield 的“体积问题”正面解决了

通过 `Caap`，论文把大网格 shield 压成非常小的 decision tree。文中案例显示：

1. bouncing ball 从 `1,430,000` 个 cell 压到 `2,972` 个 region；
2. 其他模型也有很显著压缩。

这使得 shield 真正有机会被导出到嵌入式环境中使用。

## 与 UPPAAL 技术线的关系

这篇论文在时间线上非常像一个“后期汇合点”：

1. 它延续了 `Stratego/SOS` 那条“安全 + 紧凑表示 + 学习”的思想。
2. 它把问题域推进到 hybrid systems。
3. 它引入 shield 这一比一般策略更偏安全运行时保护的对象。

所以它标志着 `UPPAAL` 已不再只是一个做 timed verification 的工具，而是继续向：

1. hybrid control
2. runtime shielding
3. compact deployable policy representation

这三个方向生长。

## 实现与材料

- 内容详细程度：`🟩 较完整`。这是 tool paper，但 workflow、query、抽象构造、压缩算法和案例都写得很实。
- 实现可获取程度：`🟧 仅可执行/可使用版本可得`。论文明确说已集成到 `Uppaal`，也给出 feature/documentation 线索，但目前未见完整公开源码仓库。
- 关键材料线索：
  - `Uppaal` 官方 features / query syntax 文档
  - 论文中的完整查询例子
  - 与 `Stratego`、earlier shield synthesis 论文联读
- 复现注意点：
  - 若要复现实验，必须注意 `n`、`m`、grid granularity、是否把 `C_out` 视为安全等参数。
  - `Caap` 追求的是功能等价压缩，不是近似分类器意义下的泛化。

## 对本研究的启发

这篇论文对当前博士研究的启发主要有四点。

1. **面对连续状态系统，可以优先接受“抽样近似 + 安全统计验证”的路线**
   - 并不是所有 formal 环节都必须精确求解后才能落地。
2. **安全壳与高效策略应分层**
   - 先求 shield 保安全，再在 `under shield` 下学效率策略，这个工作流非常值得迁移。
3. **紧凑表示不应只在离散策略上做**
   - 混成系统的网格化 shield 同样需要压缩，否则根本没法部署。
4. **查询语言层要能直接串起合成、压缩、再学习**
   - 本文最强的地方之一，就是整个流程已进入 `Uppaal` 查询与文件工件链条。

总的来说，这篇论文是 `UPPAAL` 走向 hybrid shielding 与可部署安全控制器的重要节点，也是当前文库里最能体现“形式化方法 + 近似计算 + 工程部署”三者汇合的一篇。
