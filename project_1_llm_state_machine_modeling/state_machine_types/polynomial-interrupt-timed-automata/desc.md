# 多项式中断时间自动机 / Polynomial Interrupt Timed Automata

## 基本信息

- 标题：Polynomial Interrupt Timed Automata
- 中文标题：多项式中断时间自动机
- 作者：Beatrice Berard、Serge Haddad、Claudine Picaronny、Mohab Safey El Din、Mathieu Sassolas
- 发表：*Reachability Problems*, pp. 20-32, 2015
- DOI：`10.1007/978-3-319-24537-9_3`
- 链接：https://arxiv.org/pdf/1504.04541.pdf
- 形式主义：`Polynomial Interrupt Timed Automata (PolITA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 polynomial guards / updates、`TCTL_int` 语义和基于 cylindrical decomposition 的有限 abstraction。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `PolITA` 元组、polynomial constraints / updates，以及 CAD-based symbolic partition。

## 简报

这篇论文沿 `ITA` 主线走的是另一条后继路线：不是去加参数或辅助 clocks，而是把线性的 guards / updates 直接放宽到**多项式**。也就是说，高层 active clock 不再只跟低层时钟做线性比较，而是可以落到代数曲线和多项式更新上。按常识这一步几乎必然会把验证推向不可控，但论文用 cylindrical decomposition 把这条分支重新拉回了可判定范围，并把 reachability 放进更一般的 `TCTL_int` model checking 框架中。

- 形式主义定位：`Interrupt Timed Automata` 的 polynomial guard / update 扩展。
- 构造方式简述：保持 `ITA` 的 level discipline，但把当前层 guard / update 中允许出现的表达式从线性推广到多项式。
- 基础设施与场景简述：核心基础设施是 first-order theory of reals 上的 cylindrical decomposition、有限 bisimulation abstraction 和 on-the-fly verification construction。

```text
ITA -> polynomial guards / updates -> cylindrical decomposition -> finite abstraction -> TCTL_int model checking / reachability
```

## 形式主义定义与核心对象

### 定义对象

`PolITA` 仍然研究带 interrupt levels 的 timed control flow，但允许当前层的时间约束和更新关系呈现代数曲线，而不再局限于线性不等式。它要表达的是“分层中断控制流 + 更强的代数时序约束”。

### 核心抽象

原文的正式定义是：

$$
A = \langle \Sigma, Q, q_0, F, X, \lambda, \Delta \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是动作字母表。
2. `Q` 是有限状态集，`q_0` 是初始状态，`F` 是接受状态集。
3. `X = \{x_1,\ldots,x_n\}` 是 interrupt clocks。
4. `\lambda:Q \to \{1,\ldots,n\}` 给每个状态分配 level，并指定 active clock `x_{\lambda(q)}`。
5. `\Delta` 是迁移集合。

当 `q` 处于 level `k`，迁移上的 guard 允许写成：

$$
P \bowtie 0,\qquad P \in \mathbb Q[x_1,\ldots,x_k]
$$

即 guard 可以是当前层及更低层 clocks 上的多项式约束。

更新仍保持层级 discipline。若 `k \le k'`，则当前层 active clock 可以被更新为：

$$
x_k := P,\qquad P \in \mathbb Q[x_1,\ldots,x_{k-1}]
$$

更高层 clocks 在进入前保持 `0`，更低层 clocks 按 `ITA` 的限制保持不变。

### 一个最小例子与通俗解释

论文中的示例就是：在 level 2 中，不再写线性约束 `x_2 \le c`，而是直接写：

$$
x_2^2 > x_1 + 1
$$

或

$$
(2x_1-1)x_2^2 > 1
$$

通俗地说，`PolITA` 像“保留了 `ITA` 的中断层级骨架，但把直线边界换成了代数曲线”。它不是一般 hybrid ODE 模型，因为变量仍是 clocks；但它也不再是线性时钟系统。

### 运行 / 接受 / 转移语义

其语义配置写成：

$$
(q,v)
$$

时间步和基础 `ITA` 一样，只有 active clock 增长：

$$
v' = v +_{\lambda(q)} d
$$

这里 `+_{\lambda(q)}` 表示只对当前层 active clock 加上 `d`，其他 clocks 保持不变。

离散步满足：

$$
(q,v) \xrightarrow{a} (q',v')
$$

当且仅当存在

$$
q \xrightarrow{\varphi,a,u} q' \in \Delta
$$

使得：

$$
v \models \varphi,\qquad v' = v[u]
$$

### 语义边界

相对 [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md)，`PolITA` 更强，因为 guards / updates 不再局限于线性；但它仍然保留“每层只有一只 active clock、只依赖低层 clocks”的核心 discipline。正是这点，使它没有直接退化成一般 hybrid automata。

### 关键性质与判定边界

论文给出的主结论是：

$$
\text{ModelChecking}_{TCTL_{int}}(\text{PolITA}) \text{ is decidable}
$$

并给出复杂度上界：

$$
\text{time} \le (|A| \cdot |\varphi| \cdot d)^{2^{O(n)}}
$$

其中 `n` 是 clocks 数，`d` 是出现多项式的最大次数。

reachability 作为 `TCTL_int` 的特例自然也可判。此外，原文还证明：

$$
\text{PolITA and Stopwatch Automata are incomparable in expressive power}
$$

这说明 `PolITA` 不是单纯“更强的 stopwatch model”，而是一条独立、代数化的中断时间分支。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保留 `ITA` 的 level-based states。 |
| 事件 / 触发 | 强支持 | 仍由离散动作和层级切换驱动。 |
| 守卫 / 数据 | 强支持时间守卫 | guards / updates 升级为多项式表达式。 |
| 层次 | 强支持 | interrupt levels 仍是主骨架。 |
| 并发 / 同步 | 不支持 | 原始模型不是并发网络。 |
| 时间约束 | 强支持 | clocks 仍是模型主体，只是约束更代数化。 |
| 连续动态 / 随机性 | 不支持一般连续流 | 没有 ODE，只是 polynomial comparisons / updates。 |
| 可执行 / 可验证性 | 强理论支持 | `TCTL_int`、reachability 和 finite abstraction 都明确可做。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=\langle \Sigma,Q,q_0,F,X,\lambda,\Delta\rangle$` | `PolITA` 的标准骨架。 |
| polynomial guard | `$P \bowtie 0,\ P \in \mathbb Q[x_1,\ldots,x_k]$` | 当前层可用代数曲线切分状态空间。 |
| time step | `$v' = v +_{\lambda(q)} d$` | 即使升到 polynomial，时间推进仍只作用于 active clock。 |
| 验证主结论 | `$\text{ModelChecking}_{TCTL_{int}}(\text{PolITA})$ decidable` | reachability 被纳入更一般的逻辑框架。 |
| 表达边界 | `PolITA \nsubseteq SWA` 且 `SWA \nsubseteq PolITA` | 值得单独挂成树节点。 |

## 构造方式与承载格式

### 建模入口

建模时首先要决定：

1. 哪些时序约束必须提升到 polynomial 级别。
2. 这些多项式是否只需要出现在当前层 active clock 上。
3. 是否真的需要代数边界，而不是线性 `ITA` 已足够。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. polynomial guards / updates。
2. `TCTL_int` 公式。
3. cylindrical decomposition 与由其诱导的有限 abstraction。

### 交换与互操作

它与 [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md) 的基础分支直接相连，也与 [interrupt-timed-automata-with-auxiliary-clocks-and-parameters/desc.md](../interrupt-timed-automata-with-auxiliary-clocks-and-parameters/desc.md) 的 parameter / auxiliary 路线互补：前者扩 memory / uncertainty，这里扩 algebraic expressiveness。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 polynomial elimination、cylindrical decomposition 和 finite bisimulation abstraction。
- 仿真/执行支持：可按 active-clock timed transition semantics 直接运行。
- 验证/分析支持：`TCTL_int` model checking、reachability、on-the-fly abstraction construction。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `ITA` 理论分支上的代数化扩展节点。

## 适用场景与需求前提

### 适用场景

适合那些中断层级明确，但线性 guards / updates 不足以表达关键边界的 timed models，例如需要代数曲线式时间判据的理论建模问题。

### 需求前提

1. 系统仍应满足 `ITA` 的 level discipline。
2. 非线性主要应体现在 polynomial guards / updates，而不是一般连续动力学。
3. 目标以理论分析和验证边界为主，而不是成熟工程工具链。

### 不适用或高成本场景

若只是普通线性中断约束，基础 `ITA` 更简单；若需要一般连续流 / 任意 nonlinear dynamics，则应转向更一般的 `HA`。

## 与相邻形式主义的关系

相对 [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md)，它是 algebraic strengthening；相对 [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)，它与 `SWA` 表达力不可比；相对一般 `HA`，它仍然依赖 clocks + levels，而不是任意微分系统。

## 与本研究的关系

### 对 Project 1 的价值

它把 `ITA` 主线补成一条很鲜明的“polynomial / algebraic guard-update”后继分支，使这棵树不再只有参数和辅助时钟方向的扩展。

### 作为目标形式主义还是中间表示

更适合作为理论分支节点或高阶时序约束的中间表示，而不是工程落地格式。

### 对需求到模型生成的启发

如果需求已经出现“某层的允许时序边界是代数曲线而不是线性窗口”这类结构，LLM 生成 `PolITA` 会比把模型硬压成线性 `ITA` 更保真。

### 现实限制

它的强项是理论 decidability 和表达边界；工程工具和标准载体仍然几乎为空。

## 重要的相关工作

### 奠基或前身工作

- [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md)

### 同类型或同家族工作

- [interrupt-timed-automata-with-auxiliary-clocks-and-parameters/desc.md](../interrupt-timed-automata-with-auxiliary-clocks-and-parameters/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的“基础设施”是 cylindrical decomposition 和 finite abstraction。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Interrupt Timed Automata -> Polynomial Interrupt Timed Automata`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Polynomial Interrupt Timed Automata (PolITA)`
- 论文角色：模型扩展
- 核心功能：把 `ITA` 的线性 guards / updates 提升到多项式层面，并用 cylindrical decomposition 保住可验证性。
- 关键特性：polynomial constraints、`TCTL_int`、finite abstraction、与 `SWA` 不可比。
- 构造方式：`A=\langle \Sigma,Q,q_0,F,X,\lambda,\Delta\rangle` + polynomial guards / updates。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：中断层级清晰但线性边界不足的 timed models。
- 需求前提：非线性主要体现在 polynomial clocks 关系，而不是一般连续动力学。
- 状态：🟢
