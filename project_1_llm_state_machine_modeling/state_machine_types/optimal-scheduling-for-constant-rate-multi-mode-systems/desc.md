# 常速率多模态系统最优调度 / Optimal Scheduling for Constant-Rate Multi-Mode Systems

## 基本信息

- 标题：Optimal Scheduling for Constant-Rate Multi-Mode Systems
- 中文标题：常速率多模态系统最优调度
- 作者：Rajeev Alur、Ashutosh Trivedi、Dominik Wojtczak
- 发表：*Proceedings of the 15th ACM International Conference on Hybrid Systems: Computation and Control*, pp. 75-84, 2012
- DOI：`10.1145/2185632.2185647`
- 链接：https://www.cis.upenn.edu/~alur/Hscc12.pdf
- 形式主义：`Constant-Rate Multi-Mode Systems (CMS)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立工具；机器可处理入口是 `H=(M,n,R)` 元组、schedule semantics、线性规划式安全判定和 priced extension。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 finite modes、constant rate vectors、convex safe set 和 periodic schedule constructions。

## 简报

这篇论文把一类非常干净的混成系统固定成了一个稳定 family：系统只有有限个 mode，每个 mode 里所有连续变量都按常向量速率线性漂移，而 scheduler 可以在不触发局部 guard / invariant 的前提下自由切换 mode。这个极简假设让 `CMS` 同时具备两点：一方面足够像 hybrid system，可以建模 HVAC、能耗和安全边界；另一方面又足够受限，使 safe schedulability、safe reachability 和若干 optimality 问题都能落到多项式时间。

- 形式主义定位：`Hybrid Automata` 下 free-switching、constant-rate 的可判定 multi-mode 子类。
- 构造方式简述：给定有限 modes、每个 mode 的 rate vector、一个 convex safe set，再寻找 non-Zeno mode schedule。
- 基础设施与场景简述：核心基础设施是 LP characterization、periodic schedule synthesis 与 average / reachability cost optimization。

```text
hybrid mode family -> constant rate vector in each mode -> free switching under global safety -> CMS -> polynomial schedulability / reachability
```

## 形式主义定义与核心对象

### 定义对象

`CMS` 关注的是“局部动力学极简单，但全局要靠 mode switching 才能维持安全”的 hybrid scheduling 问题。和一般 `HA` 不同，它没有 transition guard、没有 reset、也没有复杂 flow ODE；唯一的动态来源就是“在当前 mode 里按固定速率前进多久，然后切到哪个 mode”。

### 核心抽象

原文 Definition 1 给出的母模型是：

$$
H = (M,n,R)
$$

上式中的符号逐项解释如下：

1. `M` 是有限非空的 mode 集合。
2. `n` 是连续变量个数。
3. `R : M \to \mathbb R^n` 给每个 mode 指定一个 rate vector。

一条 schedule 是 timed actions 序列：

$$
\sigma = \langle (m_1,t_1),(m_2,t_2),\ldots \rangle
$$

其中 `m_i` 是第 `i` 段采用的 mode，`t_i` 是在该 mode 中停留的时间。

### 一个最小例子与通俗解释

最典型的直觉例子就是两个房间的 HVAC：

1. 开启制冷时，房间温度按负常速率下降；
2. 关闭制冷时，房间温度按正常速率回升；
3. 若永远停在某个固定 mode，温度最终会越界；
4. 只有不断在几个 mode 之间切换，才可能一直把状态压在 comfort region 内。

通俗地说，`CMS` 像“只有几个固定推力方向的连续系统”，而 scheduler 的任务就是决定“每个方向推多久”，让轨迹永远不撞出安全多面体。

### 运行 / 接受 / 转移语义

给定起始状态 `x_0`，有限 run 写成：

$$
r=\langle x_0,(m_1,t_1),x_1,\ldots,(m_k,t_k),x_k\rangle
$$

并满足状态更新公式：

$$
x_i = x_{i-1} + t_i \cdot R(m_i)
$$

上式中的符号逐项解释如下：

1. `x_i \in \mathbb R^n` 是第 `i` 次切换后的连续状态。
2. `R(m_i)` 是 mode `m_i` 对应的常速率向量。
3. `t_i` 是该向量生效的持续时间。

若安全集 `S` 是 convex，则只要每一段 run 的端点都在 `S` 中，该段线性插值轨迹就也在 `S` 中。

### 语义边界

`CMS` 的 tractability 正是建立在“自由切换 + 常速率 + 只有全局安全目标”这三个条件上。原文明确指出：

1. 一旦给 mode 附局部 invariant 或给切换附 guard，问题会回到 undecidable；
2. 若要求 scheduler 只能在固定 sampling rate 上做决定，则 safe schedulability 变成 `PSPACE`-complete。

### 关键性质与判定边界

原文对核心决策问题给出的形式化问题是：

$$
\text{Given } H,S,x,\ \text{decide whether } \exists \sigma \text{ non-Zeno s.t. } Run(x,\sigma)\subseteq S
$$

其代表性正结果是：

$$
\text{Safe schedulability and safe reachability for CMS are decidable in polynomial time}
$$

并且如果存在安全策略，原文还构造出周期性的安全 schedule，这使 `CMS` 成为非常稳定的 hybrid control skeleton。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 modes 是模型骨架。 |
| 事件 / 触发 | 弱支持 | 切换由 scheduler 选择，不依赖离散输入事件。 |
| 守卫 / 数据 | 不支持局部 guard | 原始 tractable family 故意不引入复杂 guard / invariant。 |
| 层次 | 不支持 | 原始模型是平坦的 mode 集合。 |
| 并发 / 同步 | 不支持显式并发 | 多变量通过同一全局 mode 一起演化。 |
| 时间约束 | 强支持 | 连续时间停留与 non-Zeno schedule 是核心。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 每个 mode 内是常向量线性流。 |
| 可执行 / 可验证性 | 强理论支持 | schedulability、reachability 和多种 optimality 都可算法化。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$H=(M,n,R)$` | 纯净的 constant-rate multi-mode 骨架。 |
| schedule | `$\sigma=\langle(m_i,t_i)\rangle$` | scheduler 只需要决定 mode 和 dwell time。 |
| 状态更新 | `$x_i=x_{i-1}+t_iR(m_i)$` | 每个 mode 内的动力学是线性平移。 |
| 安全问题 | `$\exists$ non-Zeno safe schedule` | 核心判定问题。 |
| 复杂度 | `polynomial-time` | 这条 branch 的主要价值正是 tractability。 |

## 构造方式与承载格式

### 建模入口

建模时通常要先决定：

1. 系统有哪些可切换的 operating modes；
2. 每个 mode 下连续变量的 constant rate 是多少；
3. 安全集 `S` 是否可以稳定压成一个 bounded convex polytope。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. `H=(M,n,R)` 元组；
2. schedule / run 表示；
3. convex safe set；
4. LP-based optimization 和 periodic schedule synthesis。

### 交换与互操作

它与以下方向直接相关：

1. `HVAC / green scheduling` 应用；
2. `Hybrid Automata` 中的可判定子类；
3. [safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md](../safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md) 的不确定速率推广；
4. [linear-rate-multi-mode-systems/desc.md](../linear-rate-multi-mode-systems/desc.md) 的线性速率 sibling。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 LP constraints、periodic schedule representation 和 priced extension。
- 仿真/执行支持：按 piecewise-linear mode schedule 直接执行即可。
- 验证/分析支持：safe schedulability、safe reachability、reachability cost、average cost、clocked control 变体。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 hybrid scheduling / energy management / multi-mode control 的理论母型。

## 适用场景与需求前提

### 适用场景

适合那些：

1. 每个 mode 内连续变量近似常速率漂移；
2. 安全约束主要体现在全局 polytope，而不是局部 transition logic；
3. 控制目标本质上是“怎么切换 mode”。

### 需求前提

1. 动力学需能压缩成 constant rate vectors。
2. 安全集最好是 bounded convex。
3. 系统允许 scheduler 自由切换，而不依赖复杂触发 guard。

### 不适用或高成本场景

若系统必须依赖 mode-local guards、reset、复杂 ODE 或不确定扰动，`CMS` 很快就不够；这正是后续 `BMS`、`LRMMS` 或一般 `HA` 要接手的地方。

## 与相邻形式主义的关系

相对一般 `Hybrid Automata`，`CMS` 更弱但更可判；相对 `BMS`，它没有环境选择的不确定 rate set；相对 `LRMMS`，它的连续流只是平移，不是向 mode-specific equilibrium 指数收敛。

## 与本研究的关系

### 对 Project 1 的价值

它为 `Hybrid Automata` 主干补出了一条非常稳定的 `multi-mode / scheduling` 分支，使混成树不再只围绕 rectangular / o-minimal / stopwatch 这类经典边界。

### 作为目标形式主义还是中间表示

对能耗调度、资源切换、模式控制类需求，它既可以做理论目标形式主义，也可以做从自然语言到更复杂混成模型之间的中间抽象。

### 对需求到模型生成的启发

如果需求表达的是“几种离散模式下连续量分别按固定趋势变化，并且目标是一直不越界”，那就不该一上来生成一般 `HA`；先压成 `CMS` 往往更利于后续验证和修复。

## 重要的相关工作

### 奠基或前身工作

- 一般 `Hybrid Automata` 母线。

### 同类型或同家族工作

- [safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md](../safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md)
- [linear-rate-multi-mode-systems/desc.md](../linear-rate-multi-mode-systems/desc.md)
- [weak-singular-hybrid-automata/desc.md](../weak-singular-hybrid-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或文件格式；最重要的基础设施是 LP characterization 和 periodic schedule construction。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Hybrid Automata -> Singular / Constant-Rate Hybrid 支线 -> Constant-Rate Multi-Mode Systems`。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
