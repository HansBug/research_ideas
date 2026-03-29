# Adding Symmetry Reduction to Uppaal

- 问题一句话：大量对称进程的 timed model 在 `UPPAAL` 里会因重复对称状态而迅速爆炸。
- 方法一句话：给建模语言加入 `scalarset`，静态提取 process/data symmetry，定义 state swap 与 canonical representative，把对称类压成单个符号状态代表。
- 解决点一句话：把经典 finite-state symmetry reduction 真正搬进 `UPPAAL` 的 zone/DBM 语义里，并在多个对称协议上得到指数级时间与内存缩减。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，但它和一般“搜索剪枝小优化”不一样，它瞄准的是 `UPPAAL` 早期最核心的工程痛点之一：**面对成批同构进程时，symbolic state space 里会反复探索本质等价的状态**。它大致位于当前文库“架构重构与数据结构专题化”之后、`UPPAAL 4.0` 之前的阶段，和 [behrmann02-uppaal-implementation-secrets](./../behrmann02-uppaal-implementation-secrets/) 关注内部效率、[david03-unification-sharing-timed-automata-verification](./../david03-unification-sharing-timed-automata-verification/) 关注共享压缩的方向很接近，但这里解决的是另一类冗余：**不是相同约束被重复存储，而是对称进程排列顺序导致的等价状态被重复搜索**。

这篇工作的重要性在于，它不是简单把 `Murphi` 的对称削减搬过来，而是正面处理 `UPPAAL` 的 timed symbolic state 表示。对 `UPPAAL` 来说，状态已经不是纯离散配置，而是：

$$
s = (l, v, Z)
$$

其中 `l` 是 location vector，`v` 是整数变量赋值，`Z` 是用 `DBM` 表示的 zone。也就是说，若要做 canonical symmetry reduction，不能只交换离散进程索引，还必须让 clock valuation 的符号表示也跟着正确交换。这正是本文的方法难点。

## 立足问题

论文立足的问题很直接：很多经典 timed protocol 明明在结构上高度对称，例如 Fischer mutual exclusion、CSMA/CD、音视频协议、分布式算法等，但普通 `UPPAAL` 还是会把“进程 1 在这里、进程 2 在那里”和“进程 2 在这里、进程 1 在那里”当成两套不同状态来探索。随着进程数增大，这类重复会迅速放大成状态爆炸。

作者不是在抽象层泛泛而谈“对称性有帮助”，而是明确指出要把 symmetry reduction 真正用于 `UPPAAL`，至少有两个技术关卡：

1. 必须从 `UPPAAL` 的建模语言里**静态识别**哪些对象是对称的。
2. 必须构造一个代表函数 `\theta`，把同一对称类里的状态都压到一个 canonical representative 上，而且这个代表必须和 `UPPAAL` 的 symbolic timed state 相容。

从 transition-system 角度，作者把目标表述成：若一组 automorphism 诱导的等价关系 `\approx` 是 bisimulation，并保持待检查性质 `\varphi`，那么搜索时就不必保留整个对称类，只保留代表即可。对应的代表函数需要满足：

$$
\forall q \in Q,\ q \approx \theta(q)
$$

问题看似标准，但 `UPPAAL` 这里有两个额外难点。

第一，`UPPAAL` 的建模语言和 `Murphi` 不同。你不能简单沿用 `Murphi` 里那套“见到某种对称类型就自动交换”的论证，因为 `UPPAAL` 模板、参数化实例、数组、整数变量、同步、clock reset 都会影响对称性是否仍然成立。

第二，`UPPAAL` 的 symbolic state 用 zone/DBM 表示一整片 clock valuation。即便离散部分容易交换，怎样在 `DBM` 层上高效算出“交换后再取 canonical 代表”的结果，才是实做中的真正难点。作者明确说，这一步的 soundness 证明和 canonical representative 算法都是本文的主要理论贡献。

## 核心方法

这篇论文的方法可以拆成四层：语言层显式标注对称性、语义层提取 automorphism、算法层计算 canonical representative、搜索层把 reachability 改成只探索代表。

### 1. 在建模语言里引入 `scalarset`

作者先把 `Murphi` 中的 `scalarset` 思想移植到 `UPPAAL`。核心做法是允许用户显式声明一个对称数据类型，例如把进程编号建成一个大小为 `n` 的 `scalarset`，再把模板实例、变量、数组索引等绑定到这个集合上。

这一步的作用不是“为了写法好看”，而是为了给静态分析提供一个明确的、可执行的 symmetry source。作者从模型里提取出：

1. 标成对称的 scalarset 类型集合 `\Omega`。
2. 每个 scalarset 类型对应的变量集合 `V_\alpha`。
3. 以该 scalarset 为索引的数组维度集合 `D_\alpha`。
4. 进程实例和 scalarset 元素之间的实例化映射 `\gamma`。

也就是说，论文不是靠事后猜“这些进程大概长得一样”，而是要求用户在语言层显式给出“这里有一组可交换对象”，然后工具再对这些对象做静态合法性检查。

### 2. 定义 state swap，把对称性交给 automorphism/bisimulation 论证

有了 `scalarset` 之后，作者为每个 `\alpha` 上的元素对 `(i, j)` 构造 `swap^\alpha_{i,j}`。这个 state swap 分成两部分：

1. **process swap**
   - 若两个进程来自同一模板，且仅在某个 scalarset 参数上分别实例化为 `i` 与 `j`，则交换它们在状态里的局部贡献。
   - 具体会交换 active location、局部变量、局部 clocks。
2. **data swap**
   - 对所有以该 scalarset 为索引的数组维度，把索引 `i` 和 `j` 的数据交换。
   - 对所有该 scalarset 类型的变量，把值 `i` 和 `j` 对调。

于是，Fischer 协议中“交换进程 0 和 2”的动作，不只是把模板实例名对换，还会一起交换：

1. 两个进程当前所处 location；
2. 两个进程局部 clock 的值；
3. 全局对称变量里出现的进程编号；
4. 以进程编号为索引的数组条目。

作者再通过一组语法约束保证这种交换不会被模型自己破坏，例如不允许把 `scalarset` 元素拿去做加减法一类会打破置换对称的操作。最终证明：

1. 每个 state swap 都是 automorphism；
2. 这些 automorphism 生成的群 `G(H)` 诱导出 bisimulation；
3. 因而 reachability 搜索可以在对称类代表上进行。

其对称等价关系写成：

$$
q \approx q' \iff \exists h \in G(H),\ h(q) = q'
$$

### 3. 关键难点：为 symbolic timed states 计算 canonical representative

如果状态只是纯离散结构，canonical representative 常见做法是把所有可交换排列里字典序最小的那个拿来当代表。本文也沿用“最小代表”思路，但 `UPPAAL` 的状态还带 zone，因此不能只对离散部分排序。

作者的关键贡献，是给出一个对 `UPPAAL` symbolic state 可执行的 canonicalization 算法。直观上，它不是随便挑某个 swap 后的状态，而是对整个对称类求一个**规范最小**的代表，使得同一对称类里的任意状态最终都会映到同一结果。这保证了搜索时真正实现“一个 orbit 只存一个状态”。

这一步特别难，是因为 zone 是一组 clock valuation 的凸集合，而不是单点赋值。交换两个对称进程时，需要让 zone 中对应 clocks 的角色一起被置换，并在 `DBM` 级别保持语义正确。作者明确强调，这正是本文的主要理论与实现难点，且 full version 里单独给了较长证明。

### 4. 把代表函数接到 reachability 算法上

一旦有了代表函数 `\theta`，reachability 搜索的改动就很简单：

1. 初始 waiting set 不再存所有初始状态，而是存它们的代表。
2. 每次扩 successor，也先把 successor 映到代表再入队。

于是搜索规模不再取决于原状态数，而更接近于“对称类的数量”。若某个 scalarset 大小是 `n`，理论上一个 full symmetry 可对应约 `n!` 的压缩潜力。作者也强调，这正是许多协议中能带来数量级收益的原因。

## 解决了什么问题

这篇论文解决的不是“symmetry reduction 在 timed system 里有没有用”这种概念问题，而是把它**真正落到 `UPPAAL` 的模型语言、symbolic state 和验证流程里**。

第一，它让用户能够在 `UPPAAL` 语言里显式声明对称对象，并通过静态检查保证这种声明是 sound 的。这样 symmetry 不再依赖人工口头说明，而变成工具可消费的信息。

第二，它把 automorphism/bisimulation 层面的理论，成功接到了 `UPPAAL` 的 zone/DBM 状态表示上。也就是说，本文真正打通了“timed symbolic state 也能做 canonical symmetry reduction”这件事。

第三，它在实验里证明，对典型对称协议，这种方法能显著减少时间与内存开销，而且收益会随 `scalarset` 大小增长而呈指数级放大。论文里直接指出，在 Fischer、CSMA/CD 和工业 agreement protocol 上，都得到了非常明显的压缩；例如普通 `UPPAAL` 很快到极限时，symmetry prototype 还能继续推到大得多的实例。

第四，它给后续 `UPPAAL` 技术线留下了一个重要范式：**不仅可以从数据结构层压缩状态，也可以从模型本体的对称结构里压缩状态**。这和之后的 partial order reduction、dynamic extrapolation 一样，都属于“用模型结构信息改进引擎效率”的主线。

## 与 UPPAAL 技术线的关系

这篇工作和 `UPPAAL` 技术线的关系很清楚：

1. 向前，它建立在 `UPPAAL` 已经具备的 symbolic reachability 与 `DBM` 状态表示上。
2. 同时期，它和 [david03-unification-sharing-timed-automata-verification](./../david03-unification-sharing-timed-automata-verification/) 一样，都在做“怎么让 `UPPAAL` 别浪费内存和搜索步数”。
3. 向后，它预示了后来一整条“利用额外结构信息缩减状态空间”的分支，包括 partial order reduction、local time semantics、dynamic extrapolation 等。

如果从文库分类看，它最接近“状态空间削减”这一细分支线：不是改 timed automata 语义本身，而是在保持正确性的前提下减少必须显式探索的 symbolic states。

## 实现与材料

从内容详细程度看，这篇论文达到 `🟩 较完整`。它把：

1. 为什么 timed symmetry 不同于普通 finite-state symmetry；
2. `scalarset` 语言扩展怎么工作；
3. state swap 与 canonical representative 的基本思路；
4. prototype 的实验收益；

都讲得比较清楚。真正最重的 soundness 证明和 canonical representative 细节在 full version 中更完整，因此如果要精确复现算法实现，最好结合扩展版论文一起看。

从实现可获取程度看，更适合标成 `🟨 部分实现源码可得`。原因是：

1. 论文明确说做了 `UPPAAL` prototype extension；
2. 但当前没有看到该 symmetry prototype 的独立公开源码仓库；
3. 能追到的是 `UPPAAL` 主工具线、`UDBM` 等相关底层源码，而不是本文 feature 的完整实现快照。

因此，这篇条目的“实现线索”更像是：

1. `UPPAAL` 主工具历史；
2. `UDBM` / `utap` 等底层库；
3. 论文与 full version 的算法描述。

## 对本研究的启发

对当前博士研究，这篇论文最有价值的启发是：**当模型中存在天然可交换的结构时，不应该让验证引擎把这些结构当成完全不同的搜索分支**。

这对你的研究至少有三点可迁移意义：

1. 若 LLM 生成的状态机里存在成批同构子模块，后续验证与修复阶段可以主动识别“结构对称”而非盲目逐个展开。
2. 语言层显式标注很重要。`scalarset` 的经验说明，很多高级优化需要用户或上游建模阶段把结构信息显式暴露出来。
3. “规范代表”思想值得迁移到模型修复与结果归并里。很多候选修复本质上只差对称置换，若不做 canonicalization，也会造成搜索重复。
