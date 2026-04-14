# 定时自动机局部时间语义的抽象：偏序方法的基础 / Abstractions for the local-time semantics of timed automata: a foundation for partial-order methods

## 基本信息

- 标题：Abstractions for the local-time semantics of timed automata: a foundation for partial-order methods
- 中文标题：定时自动机局部时间语义的抽象：偏序方法的基础
- 作者：R. Govind，Frédéric Herbreteau，B. Srivathsan，Igor Walukiewicz
- 发表：*Proceedings of the 37th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS 2022)*，pp. 1-14，2022
- DOI：`10.1145/3531130.3533343`
- 链接：https://doi.org/10.1145/3531130.3533343
- 形式主义：`Timed Networks / local-time semantics / bounded-spread abstraction / partial-order reduction`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：local-time reachability abstraction route for timed networks with partial-order reduction
- 工具/实现获取方式：论文给出 prototype / algorithmic route，核心面向可接入 timed-verification backend 的局部时间抽象与 subsumption；当前 `paper.pdf` 是作者公开的 author version。
- 标准/格式获取方式：对象仍是标准 networked timed automata；新增的是 local-time valuations、bounded-spread 条件、`a^D_{\preccurlyeq LU}` 抽象与 source-function 驱动的偏序方法接口。

## 简报

这篇论文的关键点，不是再讲一遍 `Timed Automata`，而是回答一个更底层的问题：如果我们想把 untimed 世界里效果很好的 partial-order reduction 真正搬到 timed networks 里，local-time semantics 到底需要什么样的抽象后端才能既保 diamond、又能用 subsumption、还不至于无限膨胀。论文的回答分两步：先证明对任意 timed network 不可能同时满足所有理想性质；再通过 bounded-spread network 这一限制，构造出既 finite 又能和 POR 配合的 `a^D_{\preccurlyeq LU}` 路线。

- 形式主义定位：面向 timed-network reachability 的 local-time abstraction / POR 方法路线。
- 构造方式简述：标准 timed network 先切到 local-time semantics，再用 bounded-spread 约束和 `a^D_{\preccurlyeq LU}` 抽象维持 finiteness，并通过 trace-faithful source function 接入偏序约减。
- 基础设施与场景简述：依托 local zones、`LU`-style abstractions、subsumption、source functions 和 bounded-spread conversion，服务并发交错很多的实时系统 reachability。

```text
timed network -> local-time semantics -> local zones -> bounded-spread restriction -> a^D_{≼LU} abstraction + source function -> reachability with subsumption and POR
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. networked timed automata；
2. local-time valuations 与 reference clocks；
3. local-zone graph；
4. source function 驱动的 partial-order reduction；
5. bounded-spread networks 与 `a^D_{\preccurlyeq LU}` 抽象。

### 核心抽象

论文直接把 timed network 定义为：

$$
N = (A_1,\ldots,A_k), \qquad A_p = (Q_p,\Sigma_p,X_p,q^{init}_p,T_p)
$$

上式中的符号逐项解释如下：

1. `N` 是由 `k` 个进程组成的 timed network。
2. `Q_p` 是进程 `p` 的离散状态集合。
3. `\Sigma_p` 是进程 `p` 的动作字母表。
4. `X_p` 是进程 `p` 的局部 clocks。
5. `q^{init}_p` 是初始状态。
6. `T_p \subseteq Q_p \times \Sigma_p \times \varphi(X_p) \times 2^{X_p} \times Q_p` 是带 guard 和 reset 的迁移。

local-time semantics 的核心是给每个进程引入 reference clock `t_p`。论文直接把 local valuation 写成：

$$
v : (X \cup X_t) \to \mathbb{R} \qquad \text{with } v(t_p) \ge v(x) \text{ for } x \in X_p
$$

上式中的符号逐项解释如下：

1. `X = \bigcup_p X_p` 是所有普通 clocks。
2. `X_t = \{t_p \mid p \in Proc\}` 是每个进程的 reference clocks。
3. `v(t_p)-v(x)` 才是时钟 `x` 的真实“已过去时间”。
4. 这种 offset-style 解释是论文为保证 local zones 封闭性而采用的关键设计。

共享动作 `b` 的执行要求相关进程本地时间对齐：

$$
v(t_{p_1}) = v(t_{p_2}) \qquad \forall p_1,p_2 \in dom(b)
$$

上式中的符号逐项解释如下：

1. `dom(b)` 是执行动作 `b` 的进程集合。
2. 只有这些进程的 reference clocks 相等时，共享动作才能触发。
3. 局部动作则不需要这种跨进程同步。

论文引入 bounded-spread 概念来绕开一般情形下的不可能性。spread 定义可整理为：

$$
spread(v) = \max_{p,q \in Proc} |v(t_p - t_q)|
$$

上式中的符号逐项解释如下：

1. `v(t_p-t_q)` 是两个进程 reference clocks 的差。
2. `spread(v)` 衡量不同进程局部时间漂移的最大幅度。
3. 若 `spread(v) \le D`，则 `v` 是 `D`-spread valuation。

最终论文给出的核心抽象是：

$$
\mathfrak{a}^D_{\preccurlyeq LU}(W) = \mathfrak{a}^{\star}_{\preccurlyeq LU}(spread_D(W))
$$

上式中的符号逐项解释如下：

1. `W` 是 valuation 集或 zone。
2. `spread_D(W)` 先把集合限制到 `D`-spread valuations。
3. `\mathfrak{a}^{\star}_{\preccurlyeq LU}` 是基于 local-time `LU` 模拟的抽象。
4. `\mathfrak{a}^D_{\preccurlyeq LU}` 是 bounded-spread 场景下真正可用的 finite quasi-abstraction。

### 一个最小例子与通俗解释

论文开头的双进程例子最直观。一个进程做本地动作 `b`，另一个进程做本地动作 `c`，然后它们在 `$` 上同步：

1. 在 global-time semantics 下，先做 `c` 需要等待 2 个时间单位，于是会错过 `b` 的上界，diamond 被打破。
2. 在 local-time semantics 下，进程 `P_2` 可以先把自己的本地时间推进到 2 去执行 `c`，而 `P_1` 先不动。
3. 随后 `P_1` 执行 `b`，再把自己的 reference clock 追上去，就还能做同步 `$`。

通俗地说，论文做的是“把原来被全局时间硬绑在一起的几个并发进程解耦成各走各的表，只有真同步时再对表”。这样，许多只因 interleaving 顺序不同而裂开的 timed diamonds 才能重新被 POR 利用。

### 运行 / 接受 / 转移语义

论文的 local run 写成：

$$
(q_0,v_0)\xrightarrow{\Delta_0}(q_0,v'_0)\xrightarrow{b_1}(q_1,v_1)\xrightarrow{\Delta_1}\cdots\xrightarrow{b_n}(q_n,v_n)\xrightarrow{\Delta_n}(q_n,v'_n)
$$

上式中的符号逐项解释如下：

1. `q_i` 是全局离散控制状态元组。
2. `v_i,v'_i` 是 local valuations。
3. `\Delta_i` 是逐进程的局部延迟向量。
4. `b_i` 是同步或局部动作。

偏序方法通过 source function 接入。论文把它整理为：

$$
src : Q \times 2^{\Sigma} \to 2^{\Sigma}
$$

上式中的符号逐项解释如下：

1. `Q` 是控制状态空间。
2. `2^{\Sigma}` 是当前 enabled actions 的子集。
3. `src` 选择需要展开的动作子集。
4. 论文要求它 trace-faithful，这样才不会破坏 reachability completeness。

### 语义边界

1. 论文聚焦 reachability，不是一般 liveness、timed games 或 synthesis。
2. 结论并非对任意 timed network 一刀切成立；bounded-spread 是关键限制。
3. 文章明确证明：对一般网络，不存在同时满足若干理想性质的 simulation-based abstraction。
4. 这条线是 backend algorithm，不是新的前端建模标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| network 骨架 | `$N=(A_1,\ldots,A_k),\ A_p=(Q_p,\Sigma_p,X_p,q^{init}_p,T_p)$` | 标准 timed network 输入对象。 |
| local valuation | `$v:(X\cup X_t)\to\mathbb R,\ v(t_p)\ge v(x)$` | 每个进程带 reference clock 的局部时间解释。 |
| 同步条件 | `$v(t_{p_1})=v(t_{p_2}) \ \forall p_1,p_2\in dom(b)$` | 共享动作前相关进程局部时间必须对齐。 |
| spread | `$spread(v)=\max_{p,q}|v(t_p-t_q)|$` | bounded-spread 网络的核心参数。 |
| 有界抽象 | `$\mathfrak a^D_{\preccurlyeq LU}(W)=\mathfrak a^\star_{\preccurlyeq LU}(spread_D(W))$` | 有限化 local-time abstraction 的关键构造。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 对象始终是标准 networked timed automata。 |
| 事件 / 触发 | 很强 | 通过动作域 `dom(b)` 和 source function 直接组织。 |
| 守卫 / 数据 | 中等支持 | 重点是时钟 guards，不强调富数据。 |
| 层次 | 不适用 | 不是层次状态机路线。 |
| 并发 / 同步 | 很强 | 论文核心就在并发动作的 independence 与同步恢复。 |
| 时间约束 | 很强 | local-time semantics、reference clocks 和 spread 都是时间构件。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 给出 abstraction、subsumption、POR 组合与复杂度分析。 |

### 形式化问题与性质

1. 论文先证明一般 timed networks 上“理想 local-time abstraction”的不可能性，再给出 bounded-spread 这一可操作解法。
2. `a^D_{\preccurlyeq LU}` 的 inclusion test 可在 `O(|X \cup X_t|^2)` 内完成，这是其真正工程可用的关键。
3. 该路线把 “POR + subsumption” 这两个经常互相牵制的优化，重新放进同一条 timed backend 流程里。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 标准 timed network；
2. local-time semantics；
3. local-zone graph；
4. source-function based POR；
5. bounded-spread abstraction。

### 机器可处理承载方式

机器可处理承载方式包括：

1. local valuations；
2. local zones；
3. source functions；
4. `LU`-style abstraction；
5. bounded-spread restricted zones。

### 交换与互操作

1. 本文不发明新前端格式，继续沿用 timed automata networks。
2. 主要互操作价值在 backend：它让 local-time route 能与现有 POR 思想结合。
3. 和传统 zone tools 的接口体现在抽象和 subsumption 层，而不是语言层。

## 配套基础设施

- 建模/编辑工具：沿用标准 timed automata network 前端。
- 解析/交换/元模型支持：核心是 local valuations、zones、source function 和 abstraction，而不是新交换格式。
- 仿真/执行支持：非重点；主线是 symbolic reachability。
- 验证/分析支持：local-zone graph、bounded-spread restriction、subsumption、partial-order reduction。
- 代码生成/转换支持：不涉及代码生成；重要“转换”是把一般 network 变成 `N_D` 这一 bounded-spread 版本。
- 标准化或社区生态：偏研究型 timed backend 路线，面向可嵌入后续工具实现。

## 适用场景与需求前提

### 适用场景

适合并发成分多、局部动作丰富、interleaving 爆炸明显的实时系统 reachability。

### 需求前提

1. 系统已能落成标准 timed network。
2. 主要难点来自并发交错，而不是复杂数据或连续动力学。
3. 若要直接套用论文主结果，系统需要能满足 bounded-spread 条件，或接受通过 `N_D` 转换换取额外同步。

### 不适用或高成本场景

1. 若系统几乎没有并发独立动作，local-time + POR 收益会很有限。
2. 若必须保留原始并发度而不接受额外同步，`N_D` 转换可能代价较高。
3. 若问题是 liveness、probabilistic timed 或 pushdown timed，本篇不足以单独覆盖。

## 与相邻形式主义的关系

1. 相对 [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md)，那篇重在 local-zone reachability 与 synchronized-zone subsumption，这篇继续把 local-time 路线推进到“可与 POR 共存的抽象基础”。
2. 相对 [checking-timed-buchi-automata-emptiness-using-the-local-time-semantics/desc.md](../checking-timed-buchi-automata-emptiness-using-the-local-time-semantics/desc.md)，本文是 reachability / abstraction foundation，后者把同一路线扩到 Büchi emptiness。
3. 相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)，`a4LU` 仍站在 global-time zone route，这篇转向 local-time + POR。

## 与本研究的关系

### 对 Project 1 的价值

它对 `project_1` 的意义非常直接：如果未来 LLM 生成的 timed models 往往是并发网络，而不是单体 automaton，那么验证闭环能否跑起来，往往取决于 backend 是否能控制 interleaving explosion。这篇正是关于 այդ个问题的基础证据。

### 作为目标形式主义还是中间表示

它不是目标形式主义，而是 timed-network 验证后端的方法路线。

### 对需求到模型生成的启发

1. 生成模型时要尽量保留局部动作与共享动作的区分。
2. 组件之间若存在天然频繁同步，可为 bounded-spread 性质提供结构性条件。
3. “模型表达力”与“模型可高效验证”不是同一个问题，LLM 输出如果忽略并发结构，会直接压垮后端。

### 现实限制

1. 论文偏理论和 backend，不解决前端建模易用性。
2. bounded-spread 是强条件，通用性依赖结构特征。
3. 实际性能还取决于未来具体 POR oracle 的质量。

## 重要的相关工作

### 奠基或前身工作

1. `Bengtsson` 等人的 local-time semantics 是整条路线的前身。
2. [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md) 是直接前序节点。

### 同类型或同家族工作

1. [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)：global-time `LU` 抽象主线。
2. [using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md](../using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md)：另一条 timed backend 抽象线。

### 与本研究关系最紧的工作

1. [checking-timed-buchi-automata-emptiness-using-the-local-time-semantics/desc.md](../checking-timed-buchi-automata-emptiness-using-the-local-time-semantics/desc.md)：把本篇 reachability foundation 推到 Büchi 空性。
2. [zone-based-verification-of-timed-automata-extrapolations-simulations-and-what-next/desc.md](../zone-based-verification-of-timed-automata-extrapolations-simulations-and-what-next/desc.md)：从更高层总结这类 timed backend 的外推/模拟版图。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Networks / local-time semantics / bounded-spread abstraction / partial-order reduction`
- 论文角色：local-time reachability abstraction route for timed networks with partial-order reduction
- 核心功能：为 local-time semantics 提供能与 subsumption 和 POR 同时兼容的 bounded-spread 抽象基础
- 关键特性：reference clocks、source function、bounded spread、`a^D_{≼LU}`、`O(|X \cup X_t|^2)` inclusion test
- 构造方式：timed network -> local-time semantics -> local zones -> bounded-spread abstraction + POR
- 基础设施：prototype-level timed backend route、local-zone abstractions、trace-faithful source-function interface
- 适用场景：并发 timed networks 的 reachability verification
- 需求前提：系统可建成 timed network，且 interleaving explosion 是主要瓶颈
- 状态：🟢 直接可用
