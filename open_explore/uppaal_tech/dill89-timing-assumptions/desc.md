# Timing Assumptions and Verification of Finite-State Concurrent Systems

- 问题一句话：dense-time 并发验证缺少可操作约束表示。
- 方法一句话：用 timers、timed traces 与 timer-region automaton 编码事件间延迟假设。
- 解决点一句话：把 timing assumptions 变成可自动验证的差分约束对象，为后来的 region/DBM 路线奠基。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🧱 核心算法/数据结构` 条目，但更准确地说，它是 `UPPAAL` 之前那条 **continuous-time verification 前史** 上非常关键的一环。它既不像 [ad90-timed-automata](../ad90-timed-automata/) 那样直接给出 timed automata 的统一语义骨架，也不像 [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/) 那样已经进入 `UPPAAL` 式 symbolic model checking；它做的是更早、也更底层的一步：先回答“**带上下界延迟假设的并发有限状态系统，能不能仍然做自动验证**”。

放在当前文库的时间线上看，这篇工作和 `ad90` 一起构成了 `1990` 年前后 dense-time 形式化的两块早期地基，但它们的重心并不一样：

1. `ad90` 更偏一般 timed language / timed automata 的语义与可判定性边界。
2. `dill89` 更偏“如何把事件间延迟假设接进 finite-state verification”的工程可操作框架。

从后见之明看，这篇论文最重要的价值，不是它已经长成后来的 `UPPAAL`，而是它先把三个后来反复出现的关键元素提前摆出来了：

1. **用实数时间而不是离散 tick 建模。**
2. **用 convex region 表示一批可能的时间赋值。**
3. **用差分约束矩阵和最短路闭包把 region 规范化。**

后两点尤其值得重视，因为这已经非常接近后来 `DBM / canonical closure / Floyd-Warshall` 的核心味道。

## 立足问题

这篇论文真正面对的问题，不是泛泛的“实时系统需要验证”，而是一个当时非常具体的张力：传统 speed-independent verification 假设系统必须在**任意相对速度**下都满足规格，但工程上很多系统其实知道一部分真实延迟信息。如果这些 timing assumptions 可以被形式化利用，系统就可以既更高效地设计，也更精确地验证；如果做不到，验证就只能停留在过强、过保守的 speed-independent 模型里。

作者在引言里把当时常见的时间建模路线分成了三类，并明确指出前两类都不够好：

1. **离散时间模型**
   - 需要先选一个时间量子，再把系统行为映射成整数步。
   - 问题在于这个量子必须预先承诺；选粗了会漏掉细粒度 bug，选细了又会把状态空间直接炸大。
2. **全局 tick / 全局时钟模型**
   - 连续时间表面上存在，但实际约束是靠和固定频率时钟比较来表达。
   - 这样无法精确表达“事件 `b` 在事件 `a` 之后最多两秒发生”这类要求，因为 tick 只能给出量化近似。
3. **整数有界的连续时间模型**
   - 这是作者要推进的方向，即直接在实数时间上处理延迟上下界。

所以，这篇论文立足的问题可以压成三个层次：

1. **如何在 continuous time 上表达事件之间的上下界延迟。**
2. **如何让这种表达仍然能接入 automata-based verification。**
3. **如何避免模型退化成“只有数学定义、没有自动验证流程”的理论壳子。**

作者并没有直接去发明完整 timed automata，而是从 speed-independent trace verification 出发，一步步把 timing assumptions 嵌进去。这一点很关键，因为它决定了整篇论文的方法不是“先定义最一般的时间自动机再回头找用途”，而是“从现有 finite-state verification 工作流出发，最小改造到足以支持实数时间延迟假设”。

## 核心方法

这篇论文的方法主线非常清楚，可以拆成五步：**trace framework -> timers -> timing automaton -> difference constraints / canonical form -> finiteness proof**。它不是单个算法，而是一整套把 timing assumptions 变成自动验证对象的构造。

### 1. 先从 speed-independent trace verification 出发

论文先回顾 speed-independent 场景下的 trace-based verification。一个过程被表示成 trace structure `(E, X)`：

$$
(E, X)
$$

其中 $E$ 是事件集合，$X$ 是无限 trace 集合。系统满足规格，本质上还是语言包含：

$$
X \subseteq X'.
$$

这里的意义在于，作者没有抛弃既有 finite-state verification 框架，而是明确要把 timing assumptions 嵌进同一个包含判定路线里。换句话说，验证主问题仍然是“实现 trace 集是否包含于规格 trace 集”，只是 trace 本身不再只记录事件顺序，还要附带时间信息。

### 2. 引入 timers，把延迟约束挂到事件上

作者的第一个关键设计，是不用全局时钟来表达时间，而是引入一组**虚构的 timers**。timer 不是系统组件本身，而是形式化分析中的“闹钟对象”：

1. 某个事件发生时可以 `set(i)` 一个 timer。
2. 在给定上下界区间内，timer 会在未来某个时间 `expire(i)`。
3. timer 的具体设定值不是系统精确控制的，而只保证落在给定上下界内。

timer system 被定义为：

$$
(T, l, u, A_0),
$$

其中：

1. $T$ 是 timer 集合。
2. $l(i)$、$u(i)$ 分别给出 timer $i$ 的 lower / upper bound。
3. $A_0$ 是初始激活的 timer 集。

这一步很有方法论意味。作者不是说“每个事件都带一个时间戳”，而是把“事件触发后若干时间内应发生另一事件”编码成：

1. 第一个事件与 `set(i)` 同步发生。
2. 第二个事件与 `expire(i)` 同步发生。

这样就把“事件间延迟”转成了“timer set/expire 序列是否满足约束”。这使 timing assumptions 被改写成一种**可与原 trace 同步组合的事件语言**。

### 3. 定义 timing-consistent traces，并构造 timing automaton

在这套 timer 机制上，作者定义了 timed trace 和 timing consistency。若 `set(i)` 在位置 $\ell$ 发生、`expire(i)` 在其后第一次于位置 $m$ 发生，则必须满足：

$$
l(i) \le \tau(m) - \tau(\ell) \le u(i).
$$

这里的 $\tau$ 是实数时间序列。换句话说，作者把 timing assumptions 变成了 timed trace 合法性的判定条件。

为了自动验证这些条件，作者进一步构造了一个 **timing automaton**。它不是后来的 timed automaton，而是一个专门接受 timing-consistent traces 的 Büchi automaton，且由两部分合取得到：

1. **well-formedness automaton**
   - 检查 timer 的 set / expire 是否语法上合理。
   - 例如 timer 不能在未激活时过期，激活 timer 不能凭空重复设置，等等。
2. **timer region automaton**
   - 检查不同 timer 的相对到期顺序是否可能由某组实数延迟产生。

这第二部分是整篇论文最关键的构造。作者的直觉是：每当 timer 事件发生时，可以记录一个“当前所有激活 timers 还剩多久到期”的 valuation；一组 valuation 形成一个 convex linear region；这些 regions 就构成自动机的状态空间。

所以，作者的核心对象已经不是普通 finite-state node，而是：

1. 一个 trace 上的 timer activation pattern。
2. 一个对应的 timer valuation region。
3. 它们在事件发生时如何推进到下一个 region。

这已经非常接近后来“符号状态 = 离散位置 + 时间约束区”的基本思想。

### 4. 用 difference constraints 和 DB matrix 表示 timer regions

timer region 仅靠“每个 timer 的上下界”并不够，因为不同 timers 之间的**相对差值**也会持续携带信息。作者在例子里专门强调：如果只保留单个 timer 的区间而不记录 timer 之间的差分关系，就会丢失精度。

因此，region 必须表示两类约束：

1. 单个 timer 的上下界。
2. 任意两个 timers 之间的差分约束。

作者把这类对象表示成 difference-bounds matrix：

$$
D : A^2 \to B,
$$

矩阵项 $D(i, j)$ 给出：

$$
v(i) - v(j) \le D(i, j).
$$

为了把单变量上下界统一进同一表示里，还引入一个 fictitious timer `0`，使得：

$$
v(i) = v(i) - v(0).
$$

这一步极其重要，因为它让“timer region”从几何对象变成了**算法对象**。更关键的是，作者已经注意到同一个 region 可能有很多不同矩阵表示，因此必须做 canonicalization。其做法是：

1. 把 DB matrix 看成带权有向图。
2. 用 all-pairs shortest path 求最紧闭包。
3. 用闭包后的 canonical matrix 作为 region 的唯一表示。

换句话说，后来的 `DBM canonical closure` 基本味道已经在这里出现了。作者甚至明确指出：empty region 的判定等价于 shortest-path 过程中发现 negative cycle。

### 5. 证明 reachable timer regions 有限，从而得到自动验证

如果 region space 仍然无限，这一切都还只是一个半成品。于是论文最后必须证明：从初始 region 出发可达的 timer regions 只有有限多个。

这一步的逻辑是：

1. 先证明 timing automaton 精确接受 timing-consistent traces。
2. 再证明 timer region 的可达集合是有限的。
3. 于是 timing automaton 变成一个真正可执行的 finite automaton verification object。

从验证流程上看，整套方法最终变成：

1. 先从实现中提取 speed-independent automaton。
2. 把相关事件改写成和 `set/expire` 同步的事件。
3. 与 timing automaton 做 conjunction。
4. 再用 Büchi automata 的 usual inclusion / emptiness 机制检查是否满足规格。

也就是说，这篇论文真正打通的是：

$$
\text{timing assumptions} \to \text{timer events} \to \text{region automaton} \to \text{language-based verification}.
$$

## 解决了什么问题

这篇论文真正解决的，不是“所有实时系统都能高效验证”这种夸张命题，而是三件更基础、更关键的事。

### 1. 它把 timing assumptions 变成了自动验证对象

在此之前，工程里知道一些事件间延迟信息，不等于这些信息就能进入 formal verification。作者把“事件间延迟上下界”编进 timer system、timed trace 和 timing automaton 之后，timing assumptions 不再只是自然语言假设，而是能够直接参与自动机运算的正式对象。

### 2. 它说明了 continuous time 不必然破坏 finite-state verification 路线

论文证明：即使时间是实数，只要约束形式受控，仍然可以通过 convex region 与 difference constraints 把问题拉回有限自动机世界。这对后来的实时模型检查路线意义极大，因为它说明 dense time 并不必然意味着“只能做无限状态数学分析”。

### 3. 它提前给出了 `DBM` 路线的核心骨架

虽然文中还没有后来 `UPPAAL/UDBM` 那样成熟的术语和工程库，但以下几个关键构件已经具备：

1. pairwise difference constraints；
2. 矩阵化表示；
3. canonical closure；
4. negative cycle 判空；
5. 可达 region 有限性。

这说明它不是一篇“只有历史意义”的背景文献，而是后续 `DBM / zone` 技术线的直接前史。

当然，这篇论文也有明确边界：

1. 它处理的是 finite-state concurrent systems。
2. timing assumptions 需要用户先给定上下界。
3. 它验证的是“在这些假设下实现是否满足 speed-independent specification”，而不是完整的一般 timed specification theory。
4. 结论部分也承认，下一步应当是**证明 timing properties 本身**，而不仅是把 timing assumptions 当作前提。

## 与 UPPAAL 技术线的关系

如果只看表面标题，这篇论文不像 `UPPAAL` 论文；但如果看方法血缘，它和 `UPPAAL` 的关系其实很直接。

### 它接在谁之后

它接在更早的 speed-independent trace verification 和 Büchi-automata verification 路线上，把 timing assumptions 接进去。与 [ad90-timed-automata](../ad90-timed-automata/) 相比，它不追求统一 timed automata 语言理论，而是更偏向把 timing constraints 嵌回既有验证工作流。

### 它往后影响了谁

在当前文库里，它往后最直接影响的是：

1. [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/)
   - 开始把实时验证正式推进到 `UPPAAL` 式 symbolic model checking。
2. [llpy97-compact-data-structure](../llpy97-compact-data-structure/)
   - 把 difference-constraint 表示进一步压缩成更适合实际工具的 compact 数据结构。
3. [bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/)
   - 对 `DBM` 的语义、操作和 canonicalization 做 thesis 级系统整理。

### 它更靠近哪条主线

它最靠近的其实是：

1. `DBM / difference constraints`
2. `region / symbolic state representation`
3. `timing assumptions -> constraint automaton`

而不是 `Tiga / SMC / ECDAR` 这些更晚的分支。

## 实现与材料

1. **内容详细程度**
   - 我认为这篇条目大致在 `🟨 中等` 到 `🟩 较完整` 之间，当前总账记为 `🟨 中等` 是保守但合理的。
   - 原因是它把 timer system、timing-consistent trace、timer region automaton、difference-bounds matrix 和 canonicalization 主线都写得比较明确，但很多实现层面还停留在构造与证明，不是后来的工程化算法说明书。
2. **实现可获取程度**
   - 当前仍应保持 `🟥 暂未获取实现源码`。
   - 这篇论文是前史奠基工作，并没有给出现代意义上的公开实现仓库。
3. **材料质量判断**
   - `paper_content.txt` 足够支撑问题、方法和主要证明思路的重建。
   - 但若后续要继续深挖某个 formal proof 细节，仍应回到原 PDF 图式和公式排版核对。

## 对本研究的启发

这篇论文对当前博士研究最直接的启发，不在于“复刻一套 timer automaton”，而在于它展示了一个非常值得学习的方法模式：

1. 先把工程里真实存在、但常被自然语言化处理的 timing assumptions 抽出来。
2. 再把这些 assumptions 变成结构化对象，而不是备注。
3. 然后把它们和验证主流程做形式化耦合，而不是并列存在。

对本仓库的研究主题来说，这意味着：

1. 从需求到状态机建模时，时间前提不能只作为描述性文本保留。
2. 若要让 LLM 参与形式化建模，输出里必须有能继续进入验证流程的约束对象。
3. 在“生成-验证-修复”闭环里，时间假设应像 guard、invariant 一样成为一等对象，而不是后处理补丁。
