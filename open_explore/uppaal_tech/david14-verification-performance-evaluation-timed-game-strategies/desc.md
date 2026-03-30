# Verification and Performance Evaluation of Timed Game Strategies

- 问题一句话：`UPPAAL-TIGA` 已经能合成 timed game 策略，但合成完以后，如何继续验证这条策略的附加正确性与性能后果仍然缺少统一方法。
- 方法一句话：论文一条路把 `UPPAAL-TIGA` 产生的 zone-based strategy 翻译成 controller timed automaton，另一条路把策略直接保存在内存里接入扩展后的 `MC/SMC` 语义，从而在闭环系统上继续做验证与统计评价。
- 解决点一句话：它把 synthesis、verification、performance evaluation 串成了一条完整链路，并形成了 `Control-SMC` 这条策略感知的 `Uppaal` 分支。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `⚡ 改进与扩展`。它关注的不是“能不能合成策略”，而是策略合成之后还能做什么。也就是说，它试图弥补 `UPPAAL-TIGA` 与 `UPPAAL-SMC` 之间长期存在的一条裂缝：

1. `TIGA` 负责 synthesize；
2. `SMC` 负责 evaluate stochastic / performance behavior；
3. 但如果 evaluation 的对象是“已经合成出来的控制策略”，这两者此前并没有真正接上。

因此，这篇文章更像“后合成分析”的正式开端。

## 立足问题

controller synthesis 在 timed games 里通常回答的是一个很干净的问题：给定控制目标 `\varphi`，是否存在策略使系统无论环境如何动作都满足它。

但实际工程里，这只解决了第一层问题。拿到一条 winning strategy 后，人们还会继续追问：

1. 它除了保证原目标外，还是否满足额外的 correctness property；
2. 它平均会消耗多少时间、能量、代价；
3. 它在随机环境下的表现如何；
4. 两条都能赢的策略，哪条更合适。

而传统 `UPPAAL-TIGA` 在这方面并不够：

1. 它给你一个策略；
2. 但这个策略更像 synthesis artifact；
3. 要继续做 closed-loop verification / performance evaluation，并没有统一工作流。

所以本文真正面对的是一个很实际的缺口：**如何把“已经合成好的策略”重新放回 `UPPAAL` 分析框架里，继续对其后果做 model checking 和 statistical model checking。**

## 核心方法

论文的核心方法是“双通路策略接入”：

1. 一条路把策略翻译成 controller timed automaton；
2. 另一条路直接在引擎里把策略当作内存中的控制组件使用。

### 1. 把 `UPPAAL-TIGA` 的策略看成 location 上的 zone-action 表

作者首先回顾 `UPPAAL-TIGA` 输出策略的形式。它本质上是每个 location 上的一组 `(zone, action)` 对：

$$ \hat{s}(\ell) = \{ (Z_1, a_1), \ldots, (Z_n, a_n) \} $$

给定具体状态 `q = (\ell, v)`，只要找到 `v \in Z_i` 的那一项，就知道当前应执行哪个 controllable action，或者应继续等待 `\lambda`。

这一步非常关键，因为它把策略从“抽象求解结果”转成了一个可再处理的数据结构。

### 2. 第一条路：把策略翻译成 controller timed automaton

论文在第 4 节系统说明，如何把上述 zone-based strategy 翻译成 controller TA `C`。

翻译思路是：

1. 对每个离散 location `\ell` 建一个 basic controller fragment；
2. 从 `Init` 先切到一个 switch state `SW`；
3. 再按策略中的各个 zone `Z_i` 分别进入 choice state；
4. 然后根据动作类型分三类处理：
   - 若 `a_i` 是 controllable action，则立即同步执行；
   - 若 `a_i = \lambda` 且允许无界等待，则 controller 保持空等环境动作；
   - 若是 bounded delay，则在 controller 中用 invariant / guards 限定最多能等多久，再在上界处重新决策。

这一步的核心价值是：策略被 materialize 成一个普通 timed automaton 组件。于是后续标准 `UPPAAL` model checking 就可以把它与被控 plant 组合成闭环系统：

$$ C(G) $$

然后继续问新的性质。

### 3. 为了让 controller 观察和控制 plant，需要显式同步与状态可见化

翻译不是简单照抄 zone。论文还说明，为了让 controller 真能驱动原 timed game `G`，需要做若干工程处理：

1. 给原模型 location 分配全局 ID；
2. 用全局 flags 追踪各组件当前离散位置；
3. 把原本 local clocks 改成 controller 可见的 global clocks；
4. 对 uncontrollable actions 用专门同步通道让 controller 观察环境行为；
5. 对 controllable actions 用对应通道让 controller 发出控制动作。

也就是说，翻译策略并不是“只做静态代码生成”，而是认真把原博弈模型重构成一个可执行闭环组合系统。

### 4. 第二条路：不翻译成 TA，而是把策略直接接入 `MC/SMC` 语义

如果每次都先翻译 controller TA，再组合、再分析，工作流依然偏重。于是论文进一步提出 `Control-SMC`：

1. `Uppaal-tiga` 先 synthesize strategy；
2. 引擎把该策略保存在内存里；
3. 随后的 `MC` 与 `SMC` 直接在“受策略约束的系统”上运行。

形式上，若系统全局状态空间为 `St`，则策略可以看成：

$$ s : St \to (\mathbb{R} \times \Sigma_c) \cup \{ \lambda \} $$

含义是：

1. `s(q) = (d, a)` 表示在状态 `q` 下策略要求等待 `d` 再执行 controllable action `a`；
2. `s(q) = \lambda` 表示无限等待环境动作。

这就使策略成了一个“一状态组件” `A_s`。在 stochastic semantics 里，它自己的 delay distribution 是集中在 `d` 上的 Dirac delta：

$$ \mu_q^s = \delta_d $$

这样一来，策略就能和其他随机组件一起参加 race，只不过它的选择不再随机，而是被合成结果固定。

### 5. 扩展后的 `MC/SMC` 只允许策略允许的 controllable transitions

无论走 controller TA 还是内存策略，最关键的变化都一样：后续探索里，环境方的 uncontrollable transitions 仍按原语义发生，但 controllable transitions 必须被策略过滤。

也就是说：

1. `MC` 时，对手分支仍全部展开；
2. `SMC` 时，对手按 stochastic semantics 采样；
3. 但控制方只允许策略授权的动作与延迟。

因此后续查询问的，其实不再是原始 timed game，而是“在既定策略监督下的闭环系统”。

### 6. 为了做性能评价，可以在原 timed game 上再加 costs / hybrid clocks

论文还特别强调：策略合成只关心原控制目标，但策略评价阶段可以再往模型里加 cost / stochastic info。比如：

1. 计步数的变量；
2. 能耗 clock；
3. hybrid clocks；
4. delay density function。

于是可以问：

1. 某策略在 30 时间单位内到达目标的概率多大；
2. 平均要多少步；
3. 平均能耗多少。

这就把 synthesis 与 performance evaluation 真正打通了。

## 解决了什么问题

这篇论文解决的是策略合成后的“后处理断层”问题。

第一，它让 synthesized strategy 不再只是终点结果，而是能被继续验证和统计评估的对象。

第二，它把两条本来分离的能力线接起来了：

1. `UPPAAL-TIGA` 的 controller synthesis；
2. `UPPAAL-SMC` 的 stochastic / performance analysis。

第三，它给出两种接法：

1. 显式翻译成 controller TA；
2. 直接在引擎内存里接入策略。

这样既有可解释的 automaton-level artifact，也有更轻量的一体化工作流。

第四，它形成了 `Control-SMC` 这条非常有代表性的中间层技术：策略不是黑箱输出，而是后续分析的一等输入。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/)
2. [david11-statistical-model-checking-real-time](../david11-statistical-model-checking-real-time/)
3. [bulychev12-uppaal-smc-priced-timed-automata](../bulychev12-uppaal-smc-priced-timed-automata/)

前者解决“如何 synthesize”，后者解决“如何 statistically evaluate”；本文解决的是“怎样评估已经 synthesize 出来的策略”。

### 它往后影响了谁

它往后明显影响：

1. [david15-uppaal-stratego](../david15-uppaal-stratego/)
2. 更广义的 strategy optimization / strategy comparison
3. 后续 `UPPAAL` 中把 synthesis 与 evaluation 更紧地串在一起的工作

### 它更靠近哪条主线

它最靠近：

1. timed game strategies
2. controller synthesis after-analysis
3. `SMC`-based performance evaluation

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 策略翻译方法、扩展 stochastic semantics 与 `Control-SMC` 工作流都讲得很清楚，已经能让读者理解整个机制是如何运转的。
2. **实现可获取程度**
   - 更适合评为 `🟧 仅可执行/可使用版本可得`。
   - 论文明确表明实现基于 `Uppaal` / `Control-SMC` 分支，但当前没有找到和文章严格对应的公开源码仓库或可复现代码快照。
3. **材料价值**
   - 它非常适合作为“策略合成之后还能做什么”的入口材料，尤其适合理解 closed-loop evaluation 这条路线。

## 对本研究的启发

这篇论文对当前博士研究的启发非常强。

第一，**生成结果不该在生成那一刻就寿终正寝**。本文把 strategy 当成后续验证与评估对象；对你的状态机建模与修复链来说，生成出来的候选模型、修复策略、验证剖面也都应继续进入下一轮分析。

第二，它给出了一种很好的“结果物双表示”思路：

1. 一种是翻译成显式 automaton，便于解释与复核；
2. 另一种是保存在引擎内部，便于高效继续分析。

第三，它提醒我们：修复或控制建议除了“是否可行”，还应继续问“代价 / 风险 / 性能如何”。如果后续你的研究要比较不同修复候选，这篇文章的工作流会非常有参考价值。
