# Urgent Partial Order Reduction for Extended Timed Automata

- 问题一句话：timed automata 长期难以套用经典 POR，因为时间流逝会给原本独立的动作重新引入依赖。
- 方法一句话：只在 `UPPAAL` 风格 `XTA` 的 zero-time urgent 区域里做 stubborn-set reduction，并结合 zone、变量读写分析、broadcast 近似与静态 reachable-action 预计算。
- 解决点一句话：把 partial-order reduction 真正做进现代 `Uppaal` 扩展语言里，在紧迫并发行为丰富的模型上显著压缩 reachable states。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，是 `UPPAAL` 近年“利用结构信息压缩状态空间”主线上的一个非常重要条目。它和早期 untimed 系统上的 stubborn sets/persistent sets 是同一思想谱系，但它的关键难点在于：**时间本身会制造依赖，因此 timed automata 不能直接照搬 untimed POR**。

它在时间线上大致接在：

1. 早期 partial order reduction for timed systems 的若干失败或近似尝试之后；
2. 本文作者自己更早的“disjoint activity / periodic systems”工作之后；
3. 并指向后续更现代的 `Uppaal` 引擎优化与 static analysis。

它的独特价值是：对象不再是经典 TA，而是更接近真实 `Uppaal` 输入语言的 `extended timed automata (XTA)`，包括：

1. handshake / broadcast communication
2. shared variables
3. C-like discrete data manipulation

这使它比很多 earlier timed POR 论文更贴近实际工具内核。

## 立足问题

untimed POR 的核心前提是：若两个动作彼此独立，就不必探索它们的全部交错顺序，只保留代表性 interleaving 即可。

但 timed automata 里这个前提很容易失效。原因在于，哪怕两个离散动作在变量读写上互不干扰，时间推进也可能改变它们的可执行性。换句话说：

1. 在 untimed 系统里独立的动作；
2. 到了 timed 系统里，可能因 guard、invariant、delay 竞争而互相 enable/disable。

这正是 timed POR 多年难以真正落地的根源。

作者的关键观察是：并不是所有状态都同样难。若系统进入 **urgent behavior**，也就是当前是 zero-time state，时间已经不能继续流逝，那么上述“时间引入依赖”的问题会显著弱化。此时系统只剩一串必须立刻发生的离散动作，而这些动作之间就有可能重新出现类似 untimed 系统里的独立性。

因此，本文真正盯住的是：

1. 如何在 zero-time urgent states 上定义 sound 的 independence；
2. 如何让该 independence 同时覆盖 clocks、整数变量、通信动作；
3. 如何把这套东西做进 `Uppaal` 的真实 `XTA` 输入语言与 reachability engine 中。

## 核心方法

这篇论文的方法分成四层：urgent-state 观察、操作级依赖分析、conditional stubborn set 算法、`Uppaal` 工程化实现。

### 1. 只在 zero-time states 上做 reduction

作者首先区分了普通状态与 zero-time states。若当前状态允许时间推进，那么 delay 本身就可能与后续动作形成复杂依赖，此时论文直接不做 aggressive reduction，而返回全部 enabled actions。

真正的 reduction 只发生在：

1. 某个组件位于 urgent/committed location；
2. 或者 invariant 已使时间无法继续流逝；
3. 因而整个网络停在 zero-time state。

在这种状态下，系统接下来只能通过离散动作离开当前局面。这就把 timed POR 问题局部还原成了一个“接近 untimed”的 stubborn-set 问题。

### 2. 在 `XTA` 上定义动作独立性，不只看语法，还看 zone 形状

论文最技术性的部分，在于它没有偷懒地把 independence 定义成“不同组件、不同变量就独立”。作者先把一个 action 拆成一组 operations：

1. guard 里读取哪些 clocks / variables；
2. update 写哪些 discrete variables；
3. reset 哪些 clocks；
4. 是否有 increment / decrement；
5. 对 zone 施加的 clock constraints 会不会改变其他动作的可行性。

然后在 operation 层定义 read/write/inc/dec 的冲突规则，再把它提升到 action independence 上。

这里最关键的一点，是作者还显式使用当前状态里的 zone `Z`。因为两个 clock constraints 即使语法上看着无关，也可能因当前 zone 形状而彼此影响。论文给出的 Independence of Operations 里有一条专门的 zone-shape 条件，目的就是避免“看似无关、实际因当前 zone 而互相 disable”的情况。

这意味着本文的 independence 不是纯静态标签，而是：

1. 一部分来自静态读写分析；
2. 一部分来自当前 symbolic state 的几何形状。

### 3. 用 time-enabling actions 与 property-relevant actions 种子化 stubborn set

为了保证 reduction 不丢目标状态，作者在构造 stubborn set 时，不是从空集慢慢猜，而是先把两类关键动作纳入：

1. **time-enabling actions**
   - 这些动作一旦发生，可能让系统重新回到可延时状态。
   - 若丢掉它们，就可能破坏“哪些状态能重新让时间流动”的可达性。
2. **property-relevant actions**
   - 与当前 reachability formula 有关，可能直接决定目标状态能否出现。

这两类动作是构造条件 stubborn set 的种子。随后算法再递归地补入：

1. 能够 enable 当前未启用动作的其他动作；
2. 与已选动作不独立的动作；
3. 对 property / delay preservation 必不可少的动作。

### 4. 用 Algorithm 1 计算 conditional stubborn sets

论文给出的 Algorithm 1 是整篇方法的核心。其流程大意是：

1. 若状态不是 zero-time，则返回所有 enabled actions。
2. 否则先计算 `A_s^\ ]` 这一组当前语义可达的候选动作。
3. 再根据公式 `\varphi` 计算 property-interesting actions。
4. 若它们中都不是 time-enabling，就额外强制挑一个 time-enabling action 加入。
5. 接着进入 while-loop：
   - 若某动作还没 enabled，就把能 enable 它的动作补进来；
   - 若某动作已 enabled，就把所有与之 dependent 的动作补进来。

最终得到的 `St_s^\ ]` 是一个满足 reachability-preserving 条件的动作子集，只有这些动作生成 successor。其本质上就是把 untimed stubborn sets 移植到了 urgent timed fragment 中。

### 5. 为 `Uppaal` 做三类关键工程优化

为了让这套方法真能在 `Uppaal` 中跑，论文做了三类很务实的工程处理。

#### 5.1 Reachable actions 预计算

作者并不在每个状态从所有语法动作全集里算依赖，而是做静态分析，预先算出从当前 urgent state 语义上“可能相关”的动作超集 `A_s^\ ]`。这样能减少每次 stubborn-set 构造的工作量。

#### 5.2 Broadcast channels 的 super-action 近似

`Uppaal` 的 broadcast 同步若完全展开，接收者组合数可能指数爆炸。论文因此把一个 broadcast sender 和所有潜在 receiver 组合成一个保守的 super-action。虽然更保守，但避免了在 reduction 自己这里又产生一次组合爆炸。

#### 5.3 预计算依赖矩阵与辅助数据结构

包括：

1. 哪些 edge 能到达某位置；
2. 哪些变量集与哪些动作相关；
3. 哪些动作之间潜在依赖。

这样在线验证时，action dependence 检查尽量退化成常数时间查表，而不是每次重做语义分析。

## 解决了什么问题

这篇论文解决的，是 `Uppaal` 风格现代 `XTA` 上 partial-order reduction 长期难以实用的问题。

第一，它没有试图在所有 timed states 上强做 POR，而是识别出 urgent zero-time fragment 这一真正适合 reduction 的局部区域。这是它能 sound 且有效的关键。

第二，它把 independence 做到了 `XTA` 现实语言层，包括：

1. clocks
2. discrete variables
3. increments/decrements
4. handshake / broadcast
5. shared-memory 风格依赖

第三，它把这套理论真正嵌入 `Uppaal` 实现，并在多个工业模型上得到明显收益。论文实验显示，对有大量 urgent concurrent behavior 的模型，reachable states 与时间都能得到数量级压缩；而对不适合 reduction 的模型，额外开销虽存在但仍可接受。

第四，它给出了 reproducibility package，这一点对后续继续做引擎优化与横向对比很重要。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系非常紧密：

1. 它直接作用于 `Uppaal` 内核的 state-space exploration；
2. 它和 `DBM / zone / extrapolation` 一样，属于验证引擎底层性能主线；
3. 它又比早期理论工作更贴近现代 `Uppaal` 输入语言和工业模型。

它最适合与以下条目连成一条线看：

1. 早期 disjoint activity / sequential composition：利用结构顺序性减枝；
2. 本文：利用 urgency 局部恢复 POR；
3. dynamic extrapolation：继续从 symbolic abstraction 角度压缩状态空间。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。它把：

1. zero-time urgent state 的观察；
2. operation/action independence 定义；
3. conditional stubborn set 算法；
4. `Uppaal` 工程细节；
5. 实验结果；

都讲得比较扎实。

从实现可获取程度看，更适合标 `🟨 部分实现源码可得`。原因是：

1. 论文说方法已实现进 `Uppaal`；
2. 还给了 reproducibility package `DEIS-Tools/upor`；
3. 但 `Uppaal` 主工具里对应 feature 的完整内核源码快照并不是直接公开可得。

因此，最实际的实现线索是：

1. reproducibility package；
2. `Uppaal` 主工具可运行版本；
3. 论文中的 static analysis / broadcast approximation 描述。

## 对本研究的启发

对当前博士研究，这篇论文的启发很强：

1. **不要试图在所有状态统一做重优化**
   - 本文的成功恰恰来自只抓“urgent zero-time”这块特别适合 reduction 的区域。
2. **语义上真正相关的局部结构值得专门利用**
   - 你的验证闭环也可以考虑只在特定 profile 或特定局部结构上启用更强分析，而不是全局一刀切。
3. **现代状态机语言的优化必须同时处理 clocks 与 discrete data**
   - 如果未来 LLM 生成的模型含变量、数组和复杂 guard，那么后端优化不能只盯 clock semantics。
