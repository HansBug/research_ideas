# On Time with Minimal Expected Cost!

- 问题一句话：经典 timed game 合成只保证最坏情形时界，无法同时优化随机环境下的期望代价。
- 方法一句话：先用 `Uppaal-Tiga` 求最宽松的时间有界 winning strategy，再在其允许动作空间内用 `SMC + reinforcement learning` 学习近似最优调度。
- 解决点一句话：把 `UPPAAL` 从“只会 worst-case synthesis”推进到“兼顾 hard guarantee 与 expected-cost optimization”的策略合成。

## 论文定位

这篇论文在 `uppaal_tech/` 里应归入 `⚡ 改进与扩展`，而且是 `TIGA -> SMC -> Stratego` 这一小支线上的核心桥梁。它既不是传统 timed game 控制合成论文，也不是普通 `SMC` 概率估计论文，而是第一次较系统地把这两条线拼起来：先保证 worst-case time bound，再在这个安全可行域内继续优化 expected cost。

如果把它放在 `UPPAAL` 技术演进线中，它的地位很关键：

1. `Uppaal-Tiga` 擅长求可保证的策略。
2. `Uppaal SMC` 擅长估计随机环境下的期望/概率性能。
3. 本文把两者结合，解决“既要 hard guarantee，又要 good average behavior”的问题。

这实际上已经非常接近后面 `Uppaal Stratego` 的思想，因此它可视为 `Stratego` 正式工具化之前的理论与算法主文之一。

## 立足问题

这篇论文面对的问题，是经典 timed controller synthesis 和随机性能优化之间存在明显断层。

一方面，传统 timed games 把环境视为完全对抗者。这样做的结果是：

1. 能很好地保证 safety、time-bounded reachability 等最坏情形性质。
2. 但它只告诉你“不会太差”，不告诉你“平均有多好”。

另一方面，若把环境看作随机的，就更适合问期望代价、平均完成时间、平均能耗等问题；但纯粹做 expected cost minimization 又常常失去最坏情形保证。

于是就出现了一个非常实际的调度/控制问题：

1. 仅满足时界约束的策略可能平均代价很差。
2. 仅优化平均代价的策略可能在少数情况完全失控。
3. 实际工程往往恰恰需要两者兼顾。

作者因此把问题正式化为：在一个随机环境驱动的 `priced timed game` 中，如何合成一种策略，既保证某个 reachability 目标在 worst-case 时间界 `T` 内可达，又尽可能降低期望累积代价。

这就是一种很明确的 “beyond worst-case” 问题，只不过是在 timed / priced / stochastic setting 下提出。

## 核心方法

这篇论文的方法主线非常清晰，可以概括成“两阶段合成 + 学习优化”。

### 1. 对象层：把 timed game 放进 `PTMDP` 视角

作者先从 `Priced Timed Automata / Games` 出发。普通 `PTG` 中，环境是完全对抗性的；而在本文里，作者进一步假设环境延时与动作选择遵循随机分布，于是 timed game 被看作一种：

$$
\mathrm{PTMDP}
$$

也就是 `Priced Timed Markov Decision Process`。

这一步的意义是：

1. 保留 timed game 的控制结构。
2. 同时把环境不确定性解释为概率，而不再是纯粹对抗。

于是目标函数也自然从“是否存在 winning strategy”扩展为“在满足某个 winning constraint 的前提下，期望代价多小”。

### 2. 阶段一：先用 `Uppaal-Tiga` 计算满足时间上界的 most permissive strategy

论文并没有一上来就在整个策略空间里做 reinforcement learning。相反，它先做一件非常 `UPPAAL` 式的事情：利用既有 symbolic timed-game 算法，求出满足时间界 `T` 的**最宽松 winning strategy**：

$$
\sigma^p(G, T).
$$

这一步的作用非常关键：

1. 它确定了“哪些动作仍然允许，且不会破坏 worst-case time guarantee”。
2. 它把原始无限策略空间压缩到一个安全可行域。
3. 后续任何学习出的策略，都只在这个可行域里行动，因此天然继承 worst-case 保证。

换句话说，这篇论文最妙的地方之一，就是没有把学习算法和 hard guarantee 混在一起，而是让 `Tiga` 先负责画安全边界。

### 3. 阶段二：在最宽松策略内做随机化与强化学习

有了 `\sigma^p` 以后，作者将其 uniformize 成一个初始随机策略，也就是对允许动作先做均匀化。然后，通过 `SMC` 生成样本运行，迭代地调整各状态下动作分布，让期望代价下降。

核心思想是：

1. 从不会违反时界约束的动作集合开始。
2. 观察哪些控制选择在随机环境下更“划算”。
3. 强化这些选择，削弱差的选择。
4. 周期性评估并保留当前最好策略。

因此，本文的优化不是离线求解完整 Bellman 方程，而是一种 simulation-based policy improvement。

### 4. 评估与回填：用 `Uppaal SMC` 估计策略的 expected cost

作者在每一轮学习后，不是凭局部梯度就宣布改进成功，而是调用 `Uppaal SMC` 重新评估策略在随机环境中的 expected time / expected cost。于是整条方法链是：

$$
\mathrm{Tiga\ bound} \to \mathrm{uniformized\ strategy} \to \mathrm{sample\ runs} \to \mathrm{reinforcement} \to \mathrm{SMC\ evaluation}.
$$

这其实就是把 `UPPAAL-Tiga` 和 `Uppaal SMC` 两条原本平行的能力线合成了一条新的策略优化工作流。

### 5. 关键工程点：策略表示不能太笨

论文非常清楚地意识到，这种方法的瓶颈之一不只是“如何学习”，而是“如何表示学出来的策略”。如果策略表示太粗糙或太耗内存，那么再好的学习思想也难以落地。

作者因此探索了几类表示与学习机制：

1. **zone-based symbolic strategy**
   - 延续 `Uppaal-Tiga` 的符号表示。
2. **covariance-matrix 风格近似**
   - 用机器学习里熟悉的参数统计方式概括策略。
3. **logistic regression 表示**
   - 用参数化方式近似动作选择概率。
4. **splitting data structure**
   - 作者自己的分裂式树结构，逐步细化状态空间以表达策略差异。

这些表示的共同目标是：让策略既可学习、可评估，又不要在状态空间上失控。

### 6. 方法边界：近似最优而不是全局精确最优

作者非常务实地没有承诺“求全局最优”。他们追求的是：

1. 保证 given worst-case bound；
2. 在此约束下找到 near-optimal expected-cost strategy；
3. 相比已有 exact 方法，大幅降低计算代价。

这是本文方法能落地的关键。若一味追求完全精确的最优期望代价，复杂度很快会回到不可接受水平。

## 解决了什么问题

这篇论文解决的是 timed controller synthesis 一个长期存在的空档：**硬时界保证与平均性能优化如何结合。**

第一，它提出了一条切实可行的组合路线：`Tiga` 负责 worst-case safety/time guarantee，`SMC + learning` 负责随机环境下的期望代价优化。这样两种能力分工明确，也避免了互相拖垮。

第二，它把策略优化从“只看可达/不可达”推进到“在保证可达的前提下尽可能便宜”。这对于调度、资源分配、能耗控制等问题非常关键，因为很多工程系统不是只要“能按时完成”就够了，还要求平均代价低。

第三，它在 job-shop 类 `Duration Probabilistic Automata` 上展示了数量级的速度提升，相比此前 exact synthesis 方法更实用。

第四，它为后续 `Uppaal Stratego` 直接铺好了路。很多后文中“策略是第一类对象”“在已保证性质下探索策略空间”的思路，在这里已经成形。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系很紧密。

向前，它继承：

1. [behrmann07-uppaal-tiga](./../behrmann07-uppaal-tiga/) 的 timed game symbolic synthesis。
2. [david11-smc-priced-timed-automata](./../david11-smc-priced-timed-automata/) 和 `Uppaal SMC` 的统计估计能力。

向后，它直接影响：

1. [david15-uppaal-stratego](./../david15-uppaal-stratego/) 的工具化策略空间探索。
2. [jensen22-monte-carlo-tree-search-priced-timed-automata](./../jensen22-monte-carlo-tree-search-priced-timed-automata/) 这类继续在随机控制与优化上深化的工作。

若按支线分类，它最靠近：

1. `TIGA / timed games`
2. `SMC`
3. `strategy optimization / beyond worst-case`

## 实现与材料

这篇论文的材料质量很高，尤其适合做 `UPPAAL` 策略优化线的核心参考。

从内容详细程度看：

1. 它把 `PTMDP` 对象、目标函数和两阶段方法讲得很清楚。
2. 对 reinforcement learning 工作流和多种策略表示方式也给了实质内容。
3. 还有具体 motivating example 和 job-shop 风格实验。

这已经足够让读者重建方法轮廓，理解为什么它有效以及性能瓶颈在哪里。虽然不是完整代码手册，但算法与表示层都交代到了较深一层。

从实现可获取角度看，论文明确是新的 `Uppaal-Tiga` / `Uppaal SMC` 组合实现，并作为后续 `Stratego` 的技术基础。也就是说，工具实现明确存在；但完整源码级复现仍需对应工具版本代码。

## 对本研究的启发

对当前博士研究，这篇论文有三点非常直接的启发。

第一，它告诉我们：验证与优化不必分裂成两个世界。先用形式方法画出“绝对不能越界”的安全边界，再在边界内让学习算法去找更优解，是一种很稳健的研究路线。

第二，这种“两阶段”思想很适合 LLM 自动建模。我们完全可以先让形式验证器筛掉不满足关键硬约束的模型，再在合格模型空间里做性能导向的修复或优化。

第三，论文对策略表示的重视也很值得借鉴。未来若我们要让模型修复或验证反馈变得可学习、可优化，核心对象的表示方式往往和算法本身一样重要。
