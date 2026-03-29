# Automata for Modeling Real-Time Systems

- 问题一句话：实时系统缺少统一时钟自动机模型。
- 方法一句话：定义 clocks/guards/resets 的 timed automata 语义。
- 解决点一句话：奠定 `UPPAAL` 全部时钟自动机底座。

## 论文定位

这篇论文在 `uppaal_tech/` 里属于 `🧱 核心算法/数据结构` 条目，但它更准确地说是 `UPPAAL` 的**理论前史奠基论文**，还不是 `UPPAAL` 工具本身的实现论文。它位于当前总账“理论前史与引擎奠基（1990-1997）”的起点位置，前面更接近 [dill89-timing-assumptions](./../dill89-timing-assumptions/) 这类 dense-time 约束建模前驱，后面则直接通向 [lpw95-real-time-model-checking](./../lpw95-real-time-model-checking/)、[llpy97-compact-data-structure](./../llpy97-compact-data-structure/) 和 [lpy97-uppaal-nutshell](./../lpy97-uppaal-nutshell/) 这些真正把 timed automata 做成 `UPPAAL` 验证引擎和工具链的工作。

它的核心价值不在于给出某个工程实现，而在于把“实时时序行为应该如何被自动机化、哪些操作仍然可判定、哪些边界已经不可判定”这一整套问题先讲清楚。后续 `UPPAAL` 的 clocks、guards、resets、region-based reasoning 以及“实现模型 / 规格模型”分层思路，基本都能在这里找到语义源头。

## 立足问题

这篇论文面对的核心问题，是当时的并发系统验证主流形式化模型大多只能处理**事件顺序**，却不能精确处理**事件发生的真实时间**。标准的 `ω`-automata、时序逻辑和 trace semantics 擅长表达“先后关系”，但面对“某响应必须在 2 秒内发生”这类硬实时约束时，原模型不够用。

原文明确指出，当时常见的两类建模办法都存在明显缺陷：

1. **离散时间模型**
   - 需要先选定一个固定时间粒度，再把连续时间逼近成整数步。
   - 这样会直接限制模型精度，很多真实的 delay 约束只能近似表达。
2. **`tick` 伪时钟模型**
   - 把时间编码成全局 `tick` 事件或全局自然数变量。
   - 这种做法虽然容易嫁接到现有自动机或时序逻辑上，但很难精确表达“两个事件恰好相差 2 秒”这类约束。

因此，论文真正立足的不是“再发明一种带时间的自动机”这么宽泛，而是要解决三个更具体的技术瓶颈：

1. 如何在**dense time** 上给并发实时系统一个足够精确的 trace 语义。
2. 如何把这种语义装进**有限状态**的自动机框架里，而不是退化成无限状态的语义对象。
3. 在引入连续时间以后，哪些经典自动机操作和验证问题还能保住，哪些会失效。

这第三点尤其关键。作者并不满足于只定义一个“能写时间约束”的模型，而是进一步追问：它对交、投影、补、包含这些语言论操作还剩下多少好性质；如果这些性质崩了，那么自动验证还能怎样做。这种“先给模型，再把可判定性边界画出来”的思路，正是后续 `UPPAAL` 技术线能够持续演进的基础。

## 核心方法

这篇论文的方法不是单一算法，而是一套从**语义建模**到**可判定性分析**再到**可补子类设计**的完整框架。

### 1. 先定义 timed traces，把时间显式放进 trace semantics

作者先从 untimed trace semantics 出发，把一个 trace 扩展成 `(\rho, \tau)` 这样的 timed trace：

1. `\rho` 负责记录事件序列。
2. `\tau` 负责记录对应事件发生的实数时间。
3. 时间序列满足从 `0` 开始、严格递增、并且无界推进。

这一步的关键不只是“给每个事件附上时间戳”，而是明确选择了**非负实数上的 dense-time 语义**。这样一来，模型允许在两个事件之间出现任意细粒度的时间差，也允许异步系统在连续时间上表达精确 delay，而不是被离散步长绑死。

如果再往机制层看，这里的 timed trace 其实先固定了后面所有 timed automata 运行都要遵守的三条底层规则：

1. **Initiality**
   - 第一件事默认发生在时间 `0`。
   - 这样可以把“绝对时间”转成“相对 delay”来讨论。
2. **Monotonicity**
   - 事件时间必须严格递增。
   - 这样能排除同一条 trace 上的时间倒流和零时长重复触发。
3. **Progress**
   - 任意有界时间区间里只能出现有限多个事件。
   - 这一步很关键，它把后续自动机运行限制在一个对验证仍可控的语义框架里。

作者还把 parallel composition、hiding、renaming 这些 untimed process 上的操作原样推广到了 timed traces 上。也就是说，方法第一步不是直接谈验证算法，而是先把“实时系统也能像普通 process algebra 一样组合”这件事的语义底座搭起来。

### 2. 用 clocks + guards + resets 定义 timed automata

在 timed trace 语义之上，作者把 `ω`-automata 扩展成 timed automata。其核心机制就是后来 `UPPAAL` 最基本的那套骨架：

1. 自动机仍有有限个离散状态。
2. 另外携带有限个实值 clocks。
3. 每条迁移可以：
   - 读取一个输入符号；
   - 重置一组 clocks；
   - 带一个 guard，比较 clock 值与常数。

也就是说，方法上并不是把“时间”当作全局单变量来统一推进，而是把时间差分散到多个 clocks 上，让每个 clock 记录“自上次某事件/某迁移以来过了多久”。这样就能直接表达“从某次 `a` 之后到下一次 `b` 的 delay 不超过 2”这类局部约束，而不需要把整个系统改写成离散化倒计时模型。

在 acceptance 上，作者同时讨论了 timed Buchi automata (`TBA`) 和 timed Muller automata (`TMA`)。这说明他们不是只关心 reachability，而是从一开始就把 infinite behavior、liveness 和长期实时性质一起纳入了模型。

如果按更细的“对象 / 规则 / 过程”来看，这里的方法骨架其实已经非常完整：

1. **对象层**
   - 自动机状态 `S`
   - 时钟集合 `C`
   - 迁移边 `(s, s', \sigma, \lambda, \delta)`
2. **规则层**
   - 时间流逝时，所有 clocks 同步增长。
   - 只有当前 valuation 满足 guard `\delta` 时，对应迁移才可执行。
   - 迁移执行后，`λ` 中的 clocks 被 reset 为 `0`。
3. **过程层**
   - 给定 timed trace `(\rho, \tau)`，自动机在“离散状态 + 当前 valuation + 当前时间”三元组上运行。
   - 每一步先让 clocks 随 `t_{i+1} - t_i` 增长，再检查 guard，最后对指定 clocks reset。

换句话说，论文真正提供的是一个**带显式 valuation 演化规则的运行语义**，而不只是“状态机上可以写时间约束”这种口头描述。后来的 `UPPAAL` 虽然在实现层已经完全不同，但它的语义核心仍然是这一层机制。

### 3. 用语言论视角分析这个模型到底还能做什么

论文没有停在定义层，而是系统分析 timed automata 接上哪些语言论操作后仍可工作。核心结论是：

1. `TBA` 对 union、intersection 和 projection 闭合。
2. 因而 parallel composition、hiding、renaming 这类系统构造操作也还能保住。

这一步很重要，因为它说明 timed automata 不是一个“只能写例子”的模型，而是可以像传统自动机那样做组合式系统建模。后续 `UPPAAL` 工具里把多个 template 组合起来，本质上就沿着这条语言论路线在工程化。

这里的方法并不神秘，但非常扎实：

1. **union**
   - 直接走 automata 的 disjoint union。
2. **intersection**
   - 走 product construction。
   - 两边 automata 的 clocks 集合先视为互不相交，再把 joint transition 的 reset 集合并起来、guard 做合取。
3. **projection**
   - 本质上是对边标签做相应变化。

也就是说，作者不是简单宣称“这些操作大概还成立”，而是把 timed automata 真正纳入了 automata-theoretic constructions 的工作流。这一点对后来 `UPPAAL` 这种组合式建模工具非常关键，因为它保证“多组件系统 = 单组件模型的运算结果”这条路线在理论上站得住。

### 4. 用 region equivalence 把无限时钟赋值压成有限状态

这是论文里最关键的方法性贡献之一。timed automata 的直接运行状态包含实值 clock valuation，显然是无限的。作者没有试图精确枚举所有时钟值，而是构造了一个**region equivalence**：

1. 对每个 clock，只保留它相对最大比较常数的“有效整数部分信息”。
2. 对多个 clock，再保留它们 fractional parts 的相对次序。
3. 超过最大比较常数之后，具体值被视为等价。

这相当于说，作者识别出决定未来可执行行为的，不是每个 clock 的精确实数值，而是：

1. 它是否已经跨过关键常数界限。
2. 它当前落在哪个整数区间。
3. 多个 clock 之间谁先到下一个整数边界。

基于这种等价关系，作者把无限 valuation 空间压缩成有限多个 regions，再定义 `succ` 关系表示纯时间流逝导致的 region 跳转，并把 timed automaton 转成一个普通 Buchi automaton 来接受 `Untime[L(M)]`。这一步直接给出了 emptiness decision procedure。

如果把这一步写得再具体一些，论文的方法是：

1. 先为每个 clock 找到它在 guards 里出现的最大常数 `c_x`。
2. 再定义 valuation 等价：
   - 若 clock 还没超过 `c_x`，则保留它的整数部分；
   - 若已经超过 `c_x`，则只记“已超过”，不再区分具体多大；
   - 对仍在有效范围内的多个 clocks，再保留 fractional parts 的相对顺序。
3. 把 `(state, valuation)` 压缩成 `(state, region)`。
4. 再定义 `succ(region)`，表示“仅因时间流逝而首先到达的下一个 region”。
5. 用这套 region graph 构造一个普通 `ω`-automaton：
   - 一类边表示纯时间流逝；
   - 一类边表示原 timed automaton 的实际迁移。

更关键的是，作者没有只证明“region 有限”，而是继续把 acceptance 也搬过去：除了要求访问原 automaton 的 accepting states，还要求 clocks 在运行中满足对应的无界推进/重复 reset 条件。于是最终可以把 `TBA` 的 timed-language emptiness 化成普通 Buchi automaton 的 emptiness。

所以这里的方法贡献其实包含两层：

1. **有限抽象层**：把无限 valuation 压成有限个 regions。
2. **判定过程层**：把 timed-language 问题翻译成 ordinary Buchi automaton 的 emptiness。

从后见之明看，这里虽然还不是后来 `UPPAAL` 工程里更高效的 `zone/DBM` 路线，但已经把“**用有限抽象表示连续时间状态空间**”这一主问题完整立起来了。后续 `region -> zone -> DBM` 的演进，正是在这条方法轴上继续向可实现、可扩展推进。

### 5. 用 deterministic timed Muller automata 划出可补、可规约的规格子类

论文后半段没有试图“强行修复”一般 `TBA` 的不可判定性，而是改走另一条路：定义 deterministic timed automata，进一步引入 `DTMA` 作为可补的规格形式。

这里的方法重点是：

1. 把 determinism 定义为同一状态、同一输入下可用迁移的 guards 互斥。
2. 再要求 complete，使任意 timed trace 都有唯一运行。
3. 一旦运行唯一，补语言就可通过补 acceptance family 实现。

这里的关键不只是“加个 deterministic 限制”，而是把**可补性**真正做成一条执行路径：

1. 先要求唯一初始状态。
2. 再要求同一状态、同一输入下所有可能触发的 guards 两两互斥。
3. 再把 automaton 补成 complete，使任意 timed trace 都恰好对应一条运行。
4. 一旦运行唯一，complement 就不再需要对时钟行为做额外猜测，而只需把 Muller acceptance family 取补。

因此，作者不是证明“一般 timed automata 其实也能高效验证”，而是明确提出：

1. 实现模型可以继续用更一般的 `TBA`。
2. 规格模型则应放进 `DTMA` 这样的可补子类。

这实际上是一个非常重要的建模分工思想，后续很多形式化工具都会反复用到。

### 6. 用 `2`-counter machine 编码证明 inclusion 不可判定

这篇论文的方法里还有一块很重要，但经常在二手概述里被说得太轻，就是它对**边界**的处理并不是一句“不可判定”带过，而是给出了明确的归约思路。

作者把非确定 `2`-counter machine 的 recurring computation 问题编码进 timed traces：

1. 一个配置被编码成某个单位时间区间里的事件串。
2. 两个计数器的值，被编码成区间里 `a_1`、`a_2` 出现的次数。
3. successive configurations 的关系，则通过“相隔 `1` 个时间单位的 matching events”来表达。

这件事的技术味道非常重，因为它说明 dense time 的表达能力已经足够强，强到可以把 counter machine 行为塞进 trace 里。于是 inclusion 的不可判定就不是外部传闻，而是这个模型自身表达能力过强所导致的直接后果。

这部分方法很值得在 `desc.md` 里保留，因为它提醒我们：这篇论文不只是“提出了 timed automata”，还同时证明了**为什么后续工具设计不能无限制地沿一般语言包含去做**。

## 解决了什么问题

这篇论文真正解决的，不是“把实时系统完全验证好了”，而是更基础也更关键的三件事。

### 1. 给实时系统建模提供了统一而精确的自动机语义

它把 dense-time、事件时间戳、clocks、guards、resets、Buchi/Muller acceptance 放进一个统一框架里，使实时系统终于可以像经典 `ω`-automata 那样，被表示成可组合的语言对象。这直接解决了“连续时间系统缺少统一自动机模型”的问题。

### 2. 说明了哪些验证能力还能保住

论文证明了：

1. `TBA` 对 union / intersection / projection 闭合。
2. emptiness 仍可判定。
3. 因而可以把 timed traces 与 qualitative verification 重新接上。

这说明 continuous time 的引入虽然让问题变难，但并没有把自动机路线整体炸掉。至少在构造系统模型、做组合和判空这一层，技术路线仍然成立。

### 3. 更重要地画清了边界：一般 inclusion 不可判定

论文同样明确证明了：

1. 一般 `TBA` 的 language inclusion 是不可判定的。
2. 因而 `TBA` 也不对 complement 闭合。

这其实是非常重要的“负结果”。它告诉后续研究者：不能天真地指望“把 Buchi automata 那一套直接搬到 dense-time 上，所有验证问题还照常可做”。如果不承认这个边界，后面的 `UPPAAL` 设计就会失焦。

### 4. 给出了一条可继续前进的替代方案

论文没有止于“不可判定”，而是进一步提出 `DTMA` 这条 complementable 子类路线。这样一来，自动验证并没有被完全堵死，而是被重写成：

1. 用一般 timed automata 描述实现行为。
2. 用 deterministic timed Muller automata 描述规格。
3. 通过可补性把验证问题重新带回自动机运算框架。

这件事的意义在于：它把“实时自动机能做什么”和“不能做什么”同时定了下来，给后来 `UPPAAL` 一系工作提供了非常清楚的研究边界。

## 与 `UPPAAL` 技术线的关系

如果从当前文库的技术线看，这篇论文离后来的 `UPPAAL` 还有一段距离，但它定义了几乎所有最核心的语义零件。

### 它接在谁之后

它直接承接的是 dense-time verification 的前驱工作，尤其是当前文库中的 [dill89-timing-assumptions](./../dill89-timing-assumptions/) 这类“把 timing assumptions 放进有限状态模型”的路线。相比前驱工作，它把问题从“带时间假设的验证”进一步推进成“带时间 trace language 的自动机理论”。

### 它往后影响了谁

在当前文库里，它往后最直接影响的是：

1. [lpw95-real-time-model-checking](./../lpw95-real-time-model-checking/)
   - 把 timed automata 真正接到 symbolic model checking。
2. [llpy97-compact-data-structure](./../llpy97-compact-data-structure/)
   - 沿着“连续时间状态空间需要有限符号表示”这条路继续推进到更可实现的数据结构。
3. [lpy97-uppaal-nutshell](./../lpy97-uppaal-nutshell/)
   - 把这套理论骨架组织成早期 `UPPAAL` 工具语言和工作流说明。

如果再从更长的谱系看，后来的 `DBM / zone / federation` 都是在回答这里留下的同一个主问题：怎样高效表示与操作连续时间约束状态空间。

### 它更靠近哪条主线

它最靠近的是：

1. `timed automata semantics`
2. `symbolic state-space abstraction`
3. `verification decidability boundary`

而不直接属于后来的：

1. `DBM / zone` 工程数据结构实现线
2. `Tiga / SMC / ECDAR / Stratego / Coshy` 这些专门扩展线

换句话说，这篇论文的角色不是某个后期分支的节点，而是整棵技术树的根部定义。

## 实现与材料

按当前文库口径，我认为这篇论文的材料状态判断是合理的：

1. **内容详细程度：`🟩 较完整`**
   - 原文对 timed traces、timed automata、region equivalence、emptiness construction、deterministic subclass 都给出了正式定义和关键证明思路。
   - 但它还不是后来的实现论文，没有把具体数据结构、复杂度优化和工程组织写到足够接近复现工具实现的程度。
2. **实现可获取程度：`🟥 暂未获取实现源码`**
   - 这篇论文本身是理论奠基工作，当前没有对应的源码仓库或可直接获取的实现入口。
   - 后续 `UPPAAL`、`UDBM` 等源码线能体现它的后继实现影响，但不能倒推说这篇论文“实现源码可得”。

原文还需要特别注意一点：它的方法里已经出现了 region-based finite abstraction，但这不等于后来 `UPPAAL` 实际采用的 `DBM/zone` 工程实现。写相关工作时，不能把这两层混成同一件事。

## 对本研究的启发

对当前博士研究，这篇论文至少有三点直接启发。

### 1. 状态机建模不能把时间语义后置成附属标签

如果目标模型最终要进入 `UPPAAL` 一类验证路线，那么时间约束最好从一开始就进入状态机语义，而不是事后再把“2 秒内”“最迟多久”贴成自然语言备注。否则后续验证时会不断遇到语义错位。

### 2. 生成式建模与验证式建模需要区分“表达能力”和“可判定边界”

这篇论文最有价值的一点，是它没有因为模型表达能力增强就默认验证问题仍然可做。对 LLM 辅助建模也一样：

1. 一个模型能把需求表达出来，不代表对应验证任务仍然可判定。
2. 在设计验证剖面、性质模板和自动修复流程时，必须显式关心“落到哪个可处理子类里”。

### 3. 规格侧与实现侧可以采用不同约束强度

论文把一般 `TBA` 和可补的 `DTMA` 分开，这对当前研究很有借鉴意义。后续如果做“LLM 先生成候选模型，再自动验证并修复”的闭环，很可能也需要：

1. 在实现/候选模型侧保留更强表达能力。
2. 在规格/性质侧压到一个更稳定、更可自动处理的片段。

这种分层比“所有东西统一塞进一个最强模型”更现实，也更有利于做自动化。
