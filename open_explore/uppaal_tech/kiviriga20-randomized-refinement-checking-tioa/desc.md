# Randomized Refinement Checking of Timed I/O Automata

- 问题一句话：`TIOA` refinement 理论虽然成熟，但用符号博弈和 zone 结构做完整检查时，面对大系统和“先找错再说”的开发需求往往太重。
- 方法一句话：基于 concrete-state random walk 做 under-approximate falsification，用 `RET` 和 `RCF` 两种启发式快速寻找 refinement counterexample。
- 解决点一句话：把 `TIOA` refinement 从“只能等完整验证结束”推进成“先用随机化方法极速找反例，再做最终完整证明”的双阶段流程。

## 论文定位

这篇论文在 `UPPAAL/ECDAR` 技术线里的价值很明确：它不是重写 timed I/O specification theory，也不是提出新 refinement 定义，而是专门解决 refinement checking 的**工程可扩展性**问题。

它依赖的理论背景已经相当成熟：

1. `TIOA / TIOTS / refinement` 语义来自 `ECDAR` 系列工作。
2. 传统 `Ecdar` 工具通过 timed game + zone/DBM 的符号法做完整 refinement 检查。

但这篇论文指出，在真实开发中并不总是需要马上做完全验证。很多时候更高价值的问题是：

1. 当前模型有没有明显违反 refinement 的地方。
2. 是否能在几秒或几分钟内先抓到一个反例。
3. 随着系统规模增长，能否避免一上来就承担完整符号探索的指数爆炸成本。

所以，这篇文章在技术线上扮演的是“随机化 falsification 支线起点”的角色。它后面直接接上了 [kiviriga21-randomized-reachability-analysis-uppaal](../kiviriga21-randomized-reachability-analysis-uppaal/) 那篇把同类思想推广到一般 reachability 的工作。

## 立足问题

论文立足的问题可以分成三个层面。

### 1. 符号 refinement 检查太贵

文章开头回顾了经典 state-space explosion 问题，并指出即便有各种 symbolic/reduction 技术，完整 refinement verification 仍然很贵。对 `TIOA` 来说，`Ecdar` 要检查的是一对规格之间的 alternating simulation / refinement game，这意味着：

1. 状态里要同时携带 reﬁnement 左右两边的信息。
2. 带时钟的状态仍要经由 zone/DBM 结构表示。
3. waiting/passed 之类的全局搜索数据结构会随着系统快速膨胀。

因此，当目标仅仅是“找一个 counterexample”时，完整方法常常有些大材小用。

### 2. 现有随机化方法并不直接适配这类问题

论文也观察到，直接把 `SMC` 风格的 stochastic semantics 搬过来并不合适。原因很简单：用于统计估计的随机语义会对 delay 做均匀采样，这对 falsification 来说可能非常糟糕。

文中给了一个典型难例：如果某条通向错误的边只在一个极窄的 guard 窗口内可走，那么 `SMC` 会因为“几乎永远采不到那个精确 delay”而极难发现反例。

也就是说，针对 falsification，我们需要的不是“符合物理概率分布的运行”，而是“更偏向边界/角落/极限时刻的高效探索”。

### 3. refinement falsification 特别适合做成开发早期的轻量步骤

论文明确提出一种两阶段开发流程：

1. 先跑多个便宜的近似/随机化 counterexample detection 方法，尽快发现错误。
2. 只有在这些方法都没找到错时，再做昂贵的完整符号 refinement verification。

这一点非常重要。它说明论文的目标并不是“替代完整验证”，而是把 refinement 工作流重新分层。

## 核心方法

这篇论文的核心是基于 concrete semantics 的 memory-less random walks，并围绕“如何选 transition、如何选 delay、如何控制 walk”做出专门为 refinement falsification 设计的启发式。

### 1. 用 concrete state 而不是 symbolic zone 做探索

论文最先做出的关键决策是：随机化检查在 concrete states 上运行，而不是沿用 zone/DBM 的符号状态。

这样做有两个直接后果：

1. **好处**
   - 避开昂贵的 symbolic abstraction 计算。
   - 每一步只处理一个具体时钟赋值与位置组合。
   - 非常节省内存，因为 random walk 不保存全局 explored set。
2. **代价**
   - 失去完整性。
   - 找不到反例并不代表 refinement 成立。

因此它天生就是 under-approximate falsification，而不是 verification。

### 2. 把 refinement rule 检查嵌进 walk 过程中

论文仍然以标准 refinement 语义为方向感，只是把“全图验证”改成“沿某条具体路径不断尝试违反 refinement rule”。

具体来说：

1. **delay rule**
   - 对当前 reﬁnement state pair，比较左右两边能延迟的最大时间。
   - 如果左边还能延迟而右边不能，就得到 violation。
2. **output rule**
   - 如果左边走出某个输出，而右边无法匹配，也得到 violation。
3. **input rule**
   - 由于 specification 输入使能，某些输入动作本身不会直接导致 violation，但可以把状态带到新的、更危险的位置。

也就是说，random walk 并不是瞎走，而是在 concrete path 上逐步寻找能打破 refinement obligation 的点。

### 3. `RET`：先算所有 eventually enabled transitions，再均匀挑一个

第一种主力启发式是 `RET`，即 `Random Enabled Transition`。

其关键思想是：不要先随机 delay，再看有什么 transition；而是反过来，先看当前 concrete state 下**哪些 transition 现在或将来会变 enabled**，再从中均匀挑一个目标 transition。

这一步非常重要，因为它显式消除了一个常见偏差：如果先选 delay，那么 guard 宽的边更容易被走到，guard 窄的边更容易被忽略。`RET` 通过“先选边、后配 delay”的方式，让每条 eventually enabled edge 都有近似相同的机会被探索。

### 4. `RCF`：先挑 channel，再只算该 channel 的 transition

第二种启发式是 `RCF`，即 `Random Channel First`。

它的出发点是：`RET` 的最贵步骤在于计算“所有 eventually enabled transitions”，尤其在并行组合系统里，要枚举和检查大量边。于是 `RCF` 先随机选一个 channel，只为这个 channel 计算可能可用的 transition；若没有结果，再换另一个 channel。

这相当于以更少的计算换取更快的每步推进。

但论文也很诚实地说明，`RCF` 不是总比 `RET` 好。它在某些模型里会因为 channel 级别的随机化引入新的概率偏置，甚至错过更有价值的边。因此 `RET` 与 `RCF` 的优劣，本身就是实验要回答的问题之一。

### 5. 选 delay 时强烈偏向 lower/upper bounds

transition 选出来之后，还需要一个具体 delay 让目标 transition 变成 enabled。论文不采用简单均匀采样，而是强调：

1. 很多 timed bug 就藏在边界。
2. deadline violation、最小等待要求、极限约束等，天然都和上下界有关。

因此，论文设计了偏向 `LB` 和 `UB` 的 delay 选择机制。最朴素版本中，delay 更可能取 guard 可用区间的 lower bound 或 upper bound，而不是中间某个普通值。

这个策略的直觉非常好理解：

1. “早了一点/晚了一点”常常决定是否出错。
2. timed counterexample 往往正是 corner case。

所以 falsification 用的 delay policy，应该天然比 SMC 更“尖锐”。

### 6. 让 delay probability 在多轮 random walk 间循环变化

如果一直固定某种边界偏置，仍可能只对一类模型有效。因此论文进一步提出了**自适应/循环式 delay 分布**：

1. 第一轮可能偏 `50% LB / 50% UB`
2. 后面逐渐改成更偏 `UB`
3. 再“翻转”成更偏 `LB`

通过不断变换 delay choice distribution，让随机搜索不会长期卡死在某一种时序偏好上。

这一步的核心意义是：作者没有试图设计一个“永远最优”的 delay heuristic，而是承认不同模型需要不同偏好，于是让工具在不同偏好之间自动轮换。

### 7. walk 完全无记忆，但要靠 step bound 终止

因为 random walk 不存 explored states，它天然有机会反复经过同一状态。这在 falsification 里未必是坏事，因为重复经过某状态时，可能会因为随机选择不同而走出不同路径。

但这样也带来一个问题：循环系统里 walk 可能永远不结束。论文因此设置了静态 step bound，用最大步数截断一次 walk。

这说明论文选择的是“极简内存占用 + 多次独立试探”的路线，而不是引入更复杂的覆盖/记忆结构。

### 8. 通过实验比较不同 delay policy 与启发式的真实效果

论文没有停在启发式定义，而是系统地比较了：

1. 均匀 delay 版本。
2. 固定偏边界的版本。
3. 动态变化概率的版本。
4. `RET` 与 `RCF` 的差异。

实验对象包括：

1. Milner’s scheduler
2. Leader Election protocol
3. mutation testing 设置

结果非常明确：

1. 均匀 delay 的版本和 `SMC` 一样，对“窄 violation”非常弱。
2. 偏向边界与动态概率变化显著提升了 falsification 效率。
3. 在大模型上，启发式方法比 `Ecdar` 的完整符号 refinement 检查快很多，甚至可达数百倍。

尤其在很大的系统里，当 `Ecdar` 超时或内存吃紧时，随机化方法仍可能快速给出反例。

## 解决了什么问题

这篇论文主要解决了三个问题。

### 1. 它把 refinement checking 拆成“先否证、后证明”的双阶段流程

之前的工作流更像“一上来就做完整证明”；这篇论文说明，对大型系统，更合理的是：

1. 先用随机化 falsification 尽快抓错。
2. 只在没有发现错误时，再做完整验证。

这大幅改善了 refinement 检查在实际开发中的交互速度。

### 2. 它找到了 timed falsification 比 `SMC` 更合适的启发式设计

SMC 的概率语义适合统计估计，但不适合专门抓 counterexample。论文通过“先选 transition、再配边界 delay”的思路，明确区分了 falsification 与 statistical estimation 的目标。

### 3. 它为 `TIOA` 线引入了现代 under-approximate analysis 视角

这篇论文最重要的路线意义在于：`ECDAR/TIOA` 支线不再只依赖完整 symbolic game solving，也开始吸收 randomized under-approximate search 这类现代思路。

## 与 UPPAAL 技术线的关系

从大时间线看，这篇论文连接了两条原本较远的路线：

1. 一边是 `ECDAR` 那条偏 specification theory / refinement 的线。
2. 另一边是 `UPPAAL` 内部越来越重视 randomized / statistical / lightweight analysis 的线。

它说明即便在最“语义严肃”的 refinement 问题里，`UPPAAL` 生态也开始接受一个很实用的观点：

1. 完整性很重要。
2. 但快速找错同样重要，而且应当由不同算法层承担。

后续 [kiviriga21-randomized-reachability-analysis-uppaal](../kiviriga21-randomized-reachability-analysis-uppaal/) 就把这一思路从 `TIOA refinement` 推广到了更一般的 reachability 分析。

## 实现与材料

- 内容详细程度：`🟩 较完整`。论文已经把 heuristic、probability intuition、实验对象和结果写得较细，足够把方法主线复现出来。
- 实现可获取程度：`🟢 论文对应实现源码直达`。论文末尾明确给出了 Java prototype 与实验模型下载地址，这对复现实验非常有帮助。
- 相关实现线索：
  - `Ecdar`：完整 refinement 检查对照组。
  - Java prototype：本文随机化 falsification 原型。
- 复现注意点：
  - 论文原型是 Java，不是后来直接嵌进 `UPPAAL` 主工具的版本。
  - `RET` 与 `RCF` 的效果高度依赖 delay policy 设置和步数上限。

## 对本研究的启发

这篇论文对当前博士研究最直接的启发，是“验证闭环要区分找错阶段和证明阶段”。

1. **面对 LLM 生成模型，先快找错通常更值**
   - 一开始就追求最完整验证，往往反馈慢、成本高。
   - 更实用的做法是先跑 cheap falsification，把大错先打掉。
2. **时间系统的 bug 很多就藏在边界**
   - 论文对 `LB/UB` 的偏置选择特别值得借鉴。
   - 对状态机模型修复而言，也可以把边界条件当成优先测试对象。
3. **under-approximation 完全可以是正式流程的一部分**
   - 只要明确它的角色是“找反例，不给证明”，它就不是不严谨，而是分工清晰。

总之，这篇论文把 refinement checking 从“只能用重量级完整方法”推进到了“可以先用轻量随机化方法极速找错”，这是一个很重要的工作流转变。
