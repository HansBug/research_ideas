# 使用局部时间语义检查定时 Büchi 自动机空性 / Checking Timed Büchi Automata Emptiness Using the Local-Time Semantics

## 基本信息

- 标题：Checking Timed Büchi Automata Emptiness Using the Local-Time Semantics
- 中文标题：使用局部时间语义检查定时 Büchi 自动机空性
- 作者：Frédéric Herbreteau，B. Srivathsan，Igor Walukiewicz
- 发表：*33rd International Conference on Concurrency Theory (CONCUR 2022) / LIPIcs 243*，Article 12，2022
- DOI：`10.4230/LIPIcs.CONCUR.2022.12`
- 链接：https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CONCUR.2022.12
- 形式主义：`Timed Büchi Automata Networks / local-time semantics / local-zone graph / bounded-spread regions`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：local-time Büchi-emptiness verification route for timed automata networks
- 工具/实现获取方式：论文给出完整算法路线和与 local-time abstraction 相衔接的理论基础，但明确把 POR 看成 oracle，而不是发布单一独立工具。
- 标准/格式获取方式：对象仍是标准 timed automata network；新增的是面向 Büchi non-emptiness 的 local-zone / region / abstraction 语义层。

## 简报

这篇论文的关键贡献不是重新发明 `Büchi automata`，而是把 local-time semantics 这条本来主要用于 reachability 的 timed backend 路线，真正推进到 `Büchi non-emptiness`。它解决了三件事：local-time 语义对无限 Büchi runs 是否仍 sound、local-zone graph 对无限 runs 是否仍可用、以及怎样在 bounded-spread 前提下把 local zones、regions、abstraction 和 POR 重新拼成一个可终止的 Büchi 检查流程。

- 形式主义定位：timed automata networks 的 Büchi 空性验证方法路线，而不是新的 timed family。
- 构造方式简述：标准 timed network 先切到 local-time semantics，再构造 local-zone graph，随后在 bounded-spread 前提下建立 region equivalence，并结合 `a^D_{\preccurlyeq LU}` 与 trace-faithful source function 做 Büchi emptiness。
- 基础设施与场景简述：依托 local zones、bounded-spread regions、`LU` abstraction 和 POR oracle，服务并发实时系统的 `LTL` / Büchi 类活性检查。

```text
timed network -> local-time semantics -> local-zone graph -> bounded-spread region theory -> a^D_{≼LU} + source function -> Büchi non-emptiness result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. networks of timed automata；
2. local-time semantics；
3. Büchi non-emptiness problem；
4. local-zone graph；
5. bounded-spread region graph 与 `a^D_{\preccurlyeq LU}` 抽象。

### 核心抽象

论文给出的 network 骨架是：

$$
\mathcal N = \langle A_1,A_2,\ldots,A_k\rangle, \qquad A_i = (Q_i,q^{init}_i,\Sigma_i,X_i,\Delta_i)
$$

上式中的符号逐项解释如下：

1. `\mathcal N` 是 `k` 个 timed automata 的网络。
2. `Q_i` 是第 `i` 个 automaton 的离散状态集合。
3. `q^{init}_i` 是其初始状态。
4. `\Sigma_i` 是动作字母表。
5. `X_i` 是 clocks。
6. `\Delta_i` 是带 guard / reset 的迁移集合。

延续 local-time 路线，论文继续使用带 reference clocks 的 local valuation：

$$
v : (X \cup X_t) \to \mathbb{R} \qquad \text{with } v(t_p) \ge v(x)\ \text{for } x \in X_p
$$

上式中的符号逐项解释如下：

1. `X_t = \{t_p \mid p \in Proc\}` 是每个进程的 reference clocks。
2. `v(t_p)-v(x)` 才表示进程 `p` 中时钟 `x` 已走过的时间。
3. 共享动作仍要求相应 reference clocks 对齐。

论文把 Büchi non-emptiness 问题直接表述为：给定动作集合 `F`，是否存在无限 run 使 `F` 中动作被无限次访问。可保守整理为：

$$
\exists \rho = (q_0,v_0)\xrightarrow{\Delta_0}(q_0,v'_0)\xrightarrow{b_1}(q_1,v_1)\xrightarrow{\Delta_1}\cdots \quad \text{s.t.}\quad |\{i \mid b_i \in F\}| = \infty
$$

上式中的符号逐项解释如下：

1. `\rho` 是 local-time 或 global-time 下的无限 run。
2. `b_i` 是第 `i` 个离散动作。
3. `F` 是被要求 infinitely often 访问的动作集合。
4. 这正对应论文 Definition 1 的问题设定。

为让 infinite-run reasoning 能在 local-time 下终止，论文继续使用 bounded-spread 和 region machinery。其关键抽象写成：

$$
\mathfrak a^D_{\preccurlyeq LU}(W) = \mathfrak a^\star_{\preccurlyeq LU}(spread_D(W))
$$

上式中的符号逐项解释如下：

1. `spread_D(W)` 先把 valuation 集限制到 `D`-spread 部分。
2. `\mathfrak a^\star_{\preccurlyeq LU}` 是 local-time `LU` 模拟抽象。
3. 这一步是把 reachability abstraction 真正带进 Büchi setting 的关键。

### 一个最小例子与通俗解释

论文开头举的直观场景是：两个进程各自沿本地时间移动，只有做共享动作时才同步时间轴。

1. 如果只用 global-time semantics，独立动作的不同 interleavings 往往会被“全局时间先后顺序”强行区分开。
2. local-time semantics 则允许进程保持各自时间线，只在共享动作时强制对齐。
3. 这样，许多本来会让 Büchi zone graph 爆炸的 interleavings，又重新表现出 diamond 结构。

通俗地说，这篇论文是在回答：“reachability 时 local-time 很有用，那如果我要检查一个系统是否可能一直活着、一直循环执行某类动作，local-time 还能不能撑住？” 它的回答是能，但要补上 bounded-spread regions、合适的 abstraction，以及对 POR 使用条件的更细约束。

### 运行 / 接受 / 转移语义

论文定义 local-zone graph：

$$
LZG(\mathcal N) = \{(q,Z) \mid q \in Q,\ Z \text{ is a local zone}\}
$$

上式中的符号逐项解释如下：

1. `q` 是全局离散状态元组。
2. `Z` 是 local valuations 的 zone。
3. 节点表示某控制状态下的一整片 local valuation 集。

local-zone graph 的动作后继可写为：

$$
(q,Z)\xRightarrow{b}(q',Z')
$$

上式中的符号逐项解释如下：

1. `b` 是局部动作或同步动作。
2. `Z'` 是在 guard、reset 和 local elapse 之后得到的后继 local zone。
3. 论文证明 finite prefixes 上，这个图对 local-time runs sound / complete。

真正面向无限 runs 的关键，是 `(M,D)`-region graph。其作用可以整理为：

$$
(q,[v]^D_M)\xrightarrow{u}(q',[v']^D_M)
$$

上式中的符号逐项解释如下：

1. `[v]^D_M` 表示带最大常数 `M` 和 spread bound `D` 的 region class。
2. 这个 region graph 在 bounded-spread 前提下是有限的。
3. 论文用它把 infinite local runs、finite abstraction 和 Büchi reasoning 接了起来。

### 语义边界

1. 论文主线是 Büchi emptiness，不是一般 branching-time / synthesis / probabilistic timed。
2. 结果依赖 bounded-spread network 这一关键限制。
3. 当把 POR、abstraction 和 Büchi 组合在一起时，论文要求 network deterministic；作者也说明通常可通过 action renaming 达成。
4. 论文明确指出，如果状态里允许 invariants，则某些 soundness 结论会失效。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| network 骨架 | `$\mathcal N=\langle A_1,\ldots,A_k\rangle,\ A_i=(Q_i,q_i^{init},\Sigma_i,X_i,\Delta_i)$` | 标准 timed network 输入模型。 |
| local valuation | `$v:(X\cup X_t)\to\mathbb R,\ v(t_p)\ge v(x)$` | local-time semantics 的基本 valuation 形式。 |
| Büchi 问题 | `$|\{i \mid b_i \in F\}|=\infty$` | 需要某组动作在无限 run 中被无限次触发。 |
| local-zone successor | `$(q,Z)\xRightarrow{b}(q',Z')$` | 用 local zones 而不是 monolithic global zones 做 symbolic exploration。 |
| bounded-spread abstraction | `$\mathfrak a^D_{\preccurlyeq LU}(W)=\mathfrak a^\star_{\preccurlyeq LU}(spread_D(W))$` | 让 Büchi 检查在 bounded-spread 前提下保持 finiteness。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 对象仍是标准 timed automata network。 |
| 事件 / 触发 | 很强 | 论文的 Büchi 接受条件直接建在动作集合上。 |
| 守卫 / 数据 | 中等支持 | 以 clocks / guards 为主，不处理富数据。 |
| 层次 | 不适用 | 不是层次状态机。 |
| 并发 / 同步 | 很强 | local-time 和 POR 的整条路线都围绕并发独立性。 |
| 时间约束 | 很强 | clocks、reference clocks、bounded spread、regions 都是核心。 |
| 连续动态 / 随机性 | 不支持 | 不在本文范围。 |
| 可执行 / 可验证性 | 很强 | 从 local zones 到 bounded-spread regions 再到 Büchi emptiness 的算法链条完整。 |

### 形式化问题与性质

1. 论文给出 local-time semantics 对 Büchi runs 的 soundness，这一步是 reachability 到 liveness 的关键跨越。
2. `(M,D)`-region graph 提供了 infinite-run 需要的有限 region machinery。
3. 在 deterministic bounded-spread networks 上，论文最终把 abstraction、POR 和 Büchi emptiness 拼成了一个完整可终止的 local-time route。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 标准 timed network；
2. local-time semantics；
3. local-zone graph；
4. bounded-spread region graph；
5. trace-faithful source function。

### 机器可处理承载方式

机器可处理承载方式包括：

1. local valuations；
2. local zones；
3. `(M,D)`-regions；
4. `a^D_{\preccurlyeq LU}` abstraction；
5. source-function restricted abstract local-zone graph。

### 交换与互操作

1. 前端仍是标准 timed automata network。
2. 后端则从 global zone route 切到 local-zone / region / POR 组合路线。
3. 论文不发布独立文件标准，但为后续 timed backend 实现提供了清晰理论接口。

## 配套基础设施

- 建模/编辑工具：沿用普通 timed automata network 前端。
- 解析/交换/元模型支持：核心是 local zones、bounded-spread regions 和 abstraction，不是新文件格式。
- 仿真/执行支持：主线不是 simulation，而是 symbolic Büchi analysis。
- 验证/分析支持：Büchi emptiness、local-zone graph、region graph、`LU` abstraction、POR oracle 接口。
- 代码生成/转换支持：不涉及代码生成；关键“转换”是从原 network 到 bounded-spread reasoning artifact。
- 标准化或社区生态：偏理论 timed backend 论文，适合作为 `TChecker` / future tool routes 的理论锚点。

## 适用场景与需求前提

### 适用场景

适合需要检查活性、循环执行或 `LTL` 类性质的并发实时系统，尤其是那些 interleaving 爆炸明显的 timed networks。

### 需求前提

1. 系统已能建成 timed network。
2. 活性问题最终能规约到 Büchi non-emptiness。
3. 若要直接用论文主算法，系统需满足 bounded-spread，且最好能整理成 deterministic network。

### 不适用或高成本场景

1. 若系统核心问题只是 safety reachability，这篇会比 reachability-only 论文更重。
2. 若 network 中同步极少又不满足 bounded-spread，region machinery 的使用会受限。
3. 若问题涉及 richer timed-data / pushdown / probabilistic extensions，还需要其他后端路线补齐。

## 与相邻形式主义的关系

1. 相对 [abstractions-for-the-local-time-semantics-of-timed-automata/desc.md](../abstractions-for-the-local-time-semantics-of-timed-automata/desc.md)，本文是它的 Büchi extension。
2. 相对 [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md)，那篇解决 reachability 和 local sync graph，这篇推进到 infinite-run / Büchi。
3. 相对 [zone-based-verification-of-timed-automata-extrapolations-simulations-and-what-next/desc.md](../zone-based-verification-of-timed-automata-extrapolations-simulations-and-what-next/desc.md)，本文是 survey 中 “local-time / partial-order / liveness backend” 那条支线的具体锚点之一。

## 与本研究的关系

### 对 Project 1 的价值

它对 `project_1` 的意义在于：如果未来 LLM 生成的 timed models 不只是要证明“坏事不会发生”，还要证明“某类响应最终会无限次出现”或 `LTL`-style liveness，这篇正好说明 local-time route 不是只能做 reachability，而是可以进一步覆盖 Büchi emptiness。

### 作为目标形式主义还是中间表示

它是 timed verification backend 方法路线，不是新的目标形式主义。

### 对需求到模型生成的启发

1. 生成 timed network 时应尽量保留动作归属进程的信息。
2. 若未来关心 liveness，模型设计时就要注意哪些动作应构成 accepting set。
3. 并发结构和频繁同步模式会直接影响 Büchi 检查是否能受益于 local-time / POR。

### 现实限制

1. 论文对 deterministic 和 bounded-spread 的依赖较强。
2. 贡献集中在 backend 理论，不在前端建模生态。
3. 真正的工程收益还需要具体 tool implementation 才能完全体现。

## 重要的相关工作

### 奠基或前身工作

1. [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md)：reachability 版 local-time 路线。
2. [abstractions-for-the-local-time-semantics-of-timed-automata/desc.md](../abstractions-for-the-local-time-semantics-of-timed-automata/desc.md)：bounded-spread abstraction foundation。

### 同类型或同家族工作

1. classic `LU` / zone abstractions 仍是 global-time 对照基线。
2. [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md) 和 [using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md](../using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md) 是 global-time backend 的邻近路线。

### 与本研究关系最紧的工作

1. 对本仓库来说，这篇和上面的 abstraction paper 一起，把 “local-time timed verification” 从 reachability 补到了 liveness。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Büchi Automata Networks / local-time semantics / local-zone graph / bounded-spread regions`
- 论文角色：local-time Büchi-emptiness verification route for timed automata networks
- 核心功能：把 local-time semantics 从 reachability 推进到 Büchi non-emptiness
- 关键特性：accepting-action Büchi setting、bounded-spread regions、`a^D_{≼LU}`、trace-faithful source function、deterministic-network requirement
- 构造方式：timed network -> local-time semantics -> local zones -> bounded-spread region abstraction -> Büchi emptiness
- 基础设施：local-zone / region reasoning、POR oracle 接口、LIPIcs 理论算法链
- 适用场景：并发实时系统的活性与 `LTL`-style timed verification
- 需求前提：系统可建成 timed network，并最好满足 bounded-spread / determinism 前提
- 状态：🟢 直接可用
