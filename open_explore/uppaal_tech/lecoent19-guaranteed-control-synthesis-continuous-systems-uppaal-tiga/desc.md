# Guaranteed Control Synthesis for Continuous Systems in Uppaal Tiga

- 问题一句话：`Uppaal Tiga` 擅长整数化 timed game，但直接把连续系统离散化会丢掉两次采样之间的安全保证。
- 方法一句话：论文把 sampled switched system 的连续动力学用 set-based Euler tube 包进整数上下界函数，再让 `Tiga` 在这些安全包络上做策略合成。
- 解决点一句话：它把 `Uppaal Tiga` 从离散近似控制推进到对连续系统有 guaranteed safety 的控制合成，并给出 monotone refinement 与 `Stratego` 后优化路径。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，而且是 `Uppaal Tiga` 技术线上非常关键的一步。早期 `Tiga` 已经能做 timed games 和 controller synthesis，但主要假设模型本身已经是适合符号求解的离散/整数化 timed system。本文则把目标推进到了**连续时间 sampled switched systems**，并且关注的是安全关键控制，而不是纯离散近似下的名义策略。

它在文库里的位置大致是：

1. 承接 [cassez05-analysis-of-timed-games](./../cassez05-analysis-of-timed-games/) 与 [behrmann07-uppaal-tiga](./../behrmann07-uppaal-tiga/) 这条 timed-game/controller synthesis 主线；
2. 与 [david14-verification-performance-evaluation-timed-game-strategies](./../david14-verification-performance-evaluation-timed-game-strategies/) 一样，都是在把 `Tiga` 策略推向更可信、更工程化的使用方式；
3. 再往后又和 `Stratego` 的优化/学习路径形成连接，因为论文最后显式用 `Uppaal Stratego` 做 safe strategy 上的性能优化。

所以它不是单纯的连续控制论文，而是**`UPPAAL` 本体控制合成能力向 continuous dynamics 延展**的节点。

## 立足问题

论文立足的问题非常明确：如果把连续系统直接离散化成整数状态，再把它丢给 `Uppaal Tiga`，通常只能保证采样时刻上的安全，而无法保证两次采样之间的真实连续轨迹也安全。

作者用 adaptive cruise control 案例说明这一点。系统动力学可以写成 sampled switched system：

$$ \dot{x} = f_j(x). $$

这里：

1. $x$ 是连续状态；
2. $j \in U$ 是当前 mode；
3. controller 只在采样时刻切换 mode。

问题在于，若只在采样点上看离散近似状态，可能会得到“表面上安全”的策略，但真实连续轨迹在两个采样点之间已经越界。论文给出的车距例子中，离散变量 `distance` 还大于安全阈值，而真实连续车距 `rDistance` 已经更小，甚至可能碰撞。

因此本文真正瞄准的缺口是：

1. `Tiga` 需要整数状态与可判定的 timed game 结构；
2. 连续系统安全又要求对整个采样区间上的轨迹给出保证；
3. 如何在不破坏 `Tiga` 可判定性的前提下，把连续轨迹的安全包络塞进整数化模型。

这不是普通“数值离散化误差”问题，而是 `Uppaal Tiga` 语义边界本身与 continuous safety 之间的缝隙。

## 核心方法

整篇论文的方法主线很清晰：先把连续系统写成 sampled switched system，再用 guaranteed Euler method 计算 reachability tube，最后把 tube 的整数上下界编码进 `Uppaal Tiga` 可处理的 timed game。

### 1. 先把连续控制问题写成 sampled switched game

作者考虑的系统是：

$$ \dot{x} = f_j(x), \qquad j \in U. $$

控制器在固定采样周期 $\tau$ 上选 mode，所以系统在每个区间 $[k\tau, (k+1)\tau]$ 上都是一个固定 vector field 的连续演化。  
对 ACC 案例，状态包括两车速度和车距，连续动力学写成：

$$ \dot{v}_f = a_f, \qquad \dot{v}_e = a_e, \qquad \dot{d} = v_f - v_e. $$

这样建模后，`Ego` 与 `Front` 自然对应 timed game 的 controllable / uncontrollable players，而采样周期则由一个每单位时间触发一次的 system component 强制。

### 2. 解释为什么直接整数离散化不够

若只按传统方式把连续状态离散成整数，得到类似：

$$ x(t + \tau) = F_j(x(t)). $$

那么 `Tiga` 当然可以在整数 guards 上工作，但这里只保证采样点状态，而不保证中间连续轨迹。论文用图示明确指出：离散近似轨迹可能仍高于安全线，但真实连续轨迹已经跌破。

也就是说，本文方法并不是“更精确地离散化”而已，而是要引入一个**在整个采样区间内都成立的包络**。

### 3. 用 set-based Euler approximation 计算 reachability tube

作者采用 guaranteed Euler method。对某个 mode $j$ 和初始点 $\tilde{x}_0$，先写出 Euler 线性近似：

$$ \tilde{\varphi}_j(t,\tilde{x}_0) = \tilde{x}_0 + t f_j(\tilde{x}_0). $$

然后不是只拿这个中心轨迹，而是结合 Lipschitz / one-sided Lipschitz 常数，构造半径函数 $\delta_j(\rho,t)$，使得真实轨迹始终落在一个 ball/tube 内：

$$ \varphi_j(t, x_0) \in B(\tilde{\varphi}_j(t,\tilde{x}_0), \delta_j(\rho,t)). $$

这里：

1. $\rho$ 是初始不确定半径；
2. $\delta_j$ 是随时间增长的误差上界；
3. 如果整个 tube 都在安全集 $S$ 内，则连续系统在该采样区间上真正安全。

这一步是整篇方法的理论核心。它把 continuous safety 问题从“精确跟踪每一条轨迹”转成“证明一个可计算 tube 始终包含所有可能轨迹，且 tube 自身没越界”。

### 4. 把 tube 变成 `Tiga` 可接受的整数上下界函数

仅有 Euler tube 还不够，因为 `Tiga` 不能直接对实值非时钟变量做 synthesis。作者于是定义离散步长 $h=\tau/k$，沿 Euler 子步递推：

$$ x^j_{i+1} = x^j_i + h f_j(x^j_i), \qquad \rho^j_{i+1} = \delta_j(\rho^j_i, h). $$

然后从这些子步点和半径构造整数下界、整数上界函数：

$$ H^k_j(x_0,\rho_0), \qquad G^k_j(x_0,\rho_0). $$

它们分别是整个采样区间上连续状态的安全 under-approximation / over-approximation。论文再进一步定义末端 successor bounds：

$$ h^k_j(x_0,\rho_0), \qquad g^k_j(x_0,\rho_0). $$

关键点在于：这些函数内部虽然用 doubles 计算，但**返回结果是整数**。于是 `Uppaal Tiga` 看到的 state space 仍然只包含整数变量，可判定性不被破坏。

### 5. 在 `Tiga` 中合成“保持 tube 安全”的策略

接下来作者并不是要求 `Tiga` 直接保证真实连续状态安全，而是要求它选择动作，使得每一步的整数包络都不越过安全集：

1. 当前整数上下界给出一个 tube；
2. 若某个候选 controllable action 导致 `H` 或 `G` 已经离开安全集 `S`，就把这条边判成 unsafe；
3. `Tiga` 再在这些约束下做标准安全策略合成。

这一步将 continuous safety 转译为 discrete game 的 guard elimination。论文核心定理表明：只要每一步通过 `H/G` 判定都安全，则真实连续系统在整个演化过程中都安全。

换句话说，这篇论文的方法真正打通了下面这条链：

1. continuous ODE
2. guaranteed reachability tube
3. integer bounds
4. `Tiga`-compatible timed game
5. safe controller synthesis

### 6. 对 monotone systems 再做 refinement，避免 tube 太保守

set-based method 的常见问题是 tube 会越滚越大，导致策略过分保守。为此论文额外利用 monotonicity，给出更紧的 discrete-time 包围序列：

1. 直接分别推进下界点 `y_i^{min}` 和上界点 `y_i^{max}`；
2. 用 monotone property 证明真实轨迹始终夹在两者之间；
3. 再用更小半径的 `H/G` 函数检查区间安全。

这样可以显著压缩保守性。作者在 ACC 上展示出 refined guaranteed strategy 和原来 non-guaranteed discrete strategy 非常接近，只是略微更保守。

### 7. 在 safe strategy 基础上再用 `Stratego` 做优化

论文最后一步很有 `UPPAAL` 风格：先用 `Tiga` 得到 guaranteed safe strategy，再把该策略当作安全约束，交给 `Uppaal Stratego` 用强化学习/优化算法寻找更优的安全子策略。

也就是说，本文不是停在“能保证安全”，而是说明：

1. guaranteed synthesis 先给出不可越界的动作集；
2. `Stratego` 再在这个安全动作集上优化 accumulated distance 等指标。

这让本文直接把 `Tiga` 与 `Stratego` 两条 `UPPAAL` 线串到了一起。

## 解决了什么问题

这篇论文解决的最关键问题，是让 `Uppaal Tiga` 对连续系统的控制合成不再只是“离散采样点上看起来安全”。

第一，它填上了离散 `Tiga` 模型和 continuous safety guarantee 之间的缝：策略判定依据不再是单点近似状态，而是整个采样区间的 Euler reachability tube。

第二，它把这件事做成了**整数接口**，没有破坏 `Tiga` 的可判定性前提。对 `UPPAAL` 技术线来说，这一点比任何单独的控制案例都重要。

第三，它给出了 monotone refinement，证明 guaranteed method 不一定必然过分保守，实际可以逼近原先的最优离散策略。

第四，它展示了 guaranteed safety 与后续 optimization 并不冲突：安全先由 `Tiga` 保证，性能再由 `Stratego` 继续压榨。

## 与 `UPPAAL` 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系非常直接。

1. 它是 `Tiga` 路线的重要延伸：从 timed games 走向 sampled continuous systems。
2. 它同时连接 `Stratego` 路线：安全动作集的外层由 `Tiga` 给，内层优化由 `Stratego` 做。
3. 它也体现了 `UPPAAL` 团队在 `2010s` 后期并没有停在老的 timed-game 框架，而是在把形式方法往混成控制与 guaranteed numerical methods 方向继续推进。

如果按文库中的主线看，它非常适合放在：

1. `UPPAAL-Tiga` 的早期博弈/控制论文之后；
2. `Stratego` 优化与 compact strategy 工作之前；
3. 作为“从离散 timed games 过渡到 continuous/hybrid control synthesis”的节点。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。它给出了：

1. sampled switched system 问题定义；
2. Euler tube 与误差界；
3. `H/G/h/g` 等整数化函数；
4. 在 `Uppaal` 中的建模方式；
5. ACC 案例与后续优化。

虽然仍需要读附录/实现代码来完全复刻具体函数，但主线已经相当扎实。

从实现可获取程度看，更适合标 `🟧 仅可执行/可使用版本可得`：

1. 论文明确基于 `Uppaal Tiga` 与 `Uppaal Stratego` 实现；
2. 但当前没有看到与本文一一对应的公开源码仓库或 artifact；
3. 因此能追到的是工具线和论文中的函数定义，不是现成源码快照。

## 对本研究的启发

对当前博士研究，这篇论文非常有启发。

第一，它展示了**先做保守包络，再做离散验证/合成**的思路。若你的研究后面要处理“从非形式化描述生成模型，但模型细节不完全确定”的情况，这种先求安全包络再交给 verifier 的路线很有借鉴价值。

第二，作者严格区分了“看起来能离散化”与“真正保证连续行为安全”两回事。这对状态机建模研究尤其重要：模型若只在采样点正确，往往还不够。

第三，它说明 `UPPAAL` 技术线里的工程/理论融合非常深：数值分析、timed games、策略验证和优化都能串成一个闭环。这和你要做的“生成-验证-修复”闭环在方法论上是高度相通的。
