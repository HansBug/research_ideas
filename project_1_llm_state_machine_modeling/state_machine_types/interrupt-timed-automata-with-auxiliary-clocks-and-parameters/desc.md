# 带辅助时钟与参数的中断时间自动机 / Interrupt Timed Automata with Auxiliary Clocks and Parameters

## 基本信息

- 标题：Interrupt Timed Automata with Auxiliary Clocks and Parameters
- 中文标题：带辅助时钟与参数的中断时间自动机
- 作者：Beatrice Berard、Serge Haddad、Aleksandra Jovanovic、Didier Lime
- 发表：*Fundamenta Informaticae*, 143(3-4):235-259, 2016
- DOI：`10.3233/FI-2016-1313`
- 链接：https://arxiv.org/pdf/1409.2408.pdf
- 形式主义：`Interrupt Timed Automata with Auxiliary Clocks / Parametric Interrupt Timed Automata (PITA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是按 level 分层的 main / auxiliary clocks、`act(q)` 语义、参数前缀编码到 `ITA` 的归约，以及参数空间分区后的 class graph。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是带辅助 clocks 的 `ITA` 元组、`PITA` 参数化表达式和 reachability reduction / partition procedure。

## 简报

这篇论文不是只做一个小补丁，而是同时沿 `ITA` 主线开出两条后继：一条是**辅助时钟**，让同一 level 不再只能靠一只 main clock 说话；另一条是**参数化**，让 guards / updates 里的常数变成参数多项式。难点在于，这两种扩展都很容易把 timed model 推向不可判；而论文给出的结果是，在 `ITA` 的分层 discipline 下，它们仍能保住 reachability 的可判定性，甚至还能讨论 scoped / universal / robust reachability。

- 形式主义定位：`Interrupt Timed Automata` 的辅助时钟扩展，以及其参数化版本 `PITA`。
- 构造方式简述：每个 level 的 clock 集从单一 `x_i` 扩成 `X_i = \{x_i\} \uplus Y_i`，并允许 guards / updates 中出现参数化系数。
- 基础设施与场景简述：核心基础设施是 class graph、把 additive parameters 编码成前缀 clocks 的 reduction、以及 multiplicative case 的 parameter-space partition。

```text
ITA -> auxiliary clocks per level -> parametric guards / updates -> additive reduction to ITA -> parameter-space partition -> existential / universal / robust reachability
```

## 形式主义定义与核心对象

### 定义对象

论文首先扩展 `ITA` 的时钟结构：在每个 level，除了 main clock 之外，还允许若干 auxiliary clocks。直观上，main clock 负责该层最核心的执行时间，而 auxiliary clocks 用来记录同层内更细的局部时间痕迹，但又不能破坏 `ITA` 原有的层级可判定结构。

### 核心抽象

带辅助时钟的 `ITA` 写成：

$$
A = \langle \Sigma, n, Q, q_0, Q_f, \lambda, X, act, \Delta \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是动作字母表。
2. `n` 是 levels 数。
3. `Q` 是状态集，`q_0` 是初始状态，`Q_f` 是接受状态集。
4. `\lambda:Q \to \{1,\ldots,n\}` 给每个状态分配 level。
5. `X = \biguplus_{i=1}^n X_i` 是全体 clocks，并满足

$$
X_i = \{x_i\} \uplus Y_i
$$

其中 `x_i` 是第 `i` 层的 main clock，`Y_i` 是该层的 auxiliary clocks。

6. `act:Q \to X` 给每个状态指定 active clock。
7. `\Delta` 是迁移集合；guards 只允许引用当前层 clocks 和更低层的 main clocks，updates 也必须遵守“不让低层辅助时钟间接影响高层行为”的 discipline。

参数化版本进一步写成：

$$
A = \langle P, \Sigma, n, Q, q_0, Q_f, \lambda, X, act, \Delta \rangle
$$

其中 `P` 是参数集，guards / updates 中的系数属于 `Pol(P,\mathbb Q)`。

### 一个最小例子与通俗解释

一个直觉例子是两层中断系统：

1. level 1 的 `x_1` 记录主任务已执行多久。
2. level 2 的 `x_2` 记录中断处理总时长。
3. 同时再给 level 2 放一只 auxiliary clock `y_2`，专门记录“进入某个中断子阶段后已经过了多久”。

这样：

1. `x_2` 负责说“整次中断执行了多久”。
2. `y_2` 负责说“当前中断内部的某段等待是否超界”。

通俗地说，这个 family 像“给 `ITA` 每层增加一些辅助秒表，并允许某些时间常数变成待综合参数”，但又必须非常克制地限制这些新自由度的流向。

### 运行 / 接受 / 转移语义

其语义配置写成：

$$
(q,v)
$$

对时间步，只有 `act(q)` 指定的 active clock 演化：

$$
v'(act(q)) = v(act(q)) + d
$$

并且：

$$
v'(x) = v(x) \quad \text{for any other clock } x
$$

离散步由

$$
q \xrightarrow{\varphi,a,u} q'
$$

触发，并要求：

$$
v \models \varphi,\qquad v' = v[u]
$$

对于参数化版本，再引入参数 valuation `\pi`，判断条件变成：

$$
\pi, v \models C \bowtie 0
$$

即先用 `\pi` 解释参数，再看当前 clock valuation 是否满足比较式。

### 语义边界

论文为辅助时钟扩展增加的真正硬约束是：低层 auxiliary clocks 不能通过 guards / updates 直接或间接污染更高层行为。也正是这一点，保证了“多一些 clocks”不等于“退化回一般不可判的 hybrid/timed update system”。

### 关键性质与判定边界

对带辅助 clocks 的 `ITA`，论文证明：

$$
\text{Reachability} \in 2\mathrm{EXPTIME}
$$

并且当 level 数固定时：

$$
\text{Reachability is PSPACE-complete}
$$

对 additive `PITA`，论文给出一个很关键的 reduction：

$$
\exists \pi:\ q \text{ reachable in } A(\pi) \iff q \text{ reachable in a non-parametric ITA } A'
$$

对一般 multiplicative `PITA`，则证明：

$$
\text{scoped existential / universal / robust reachability are decidable}
$$

而且通过参数空间有限分区和每个分区上的有限 automaton，获得统一分析框架。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 延续 `ITA` 的 level-based states。 |
| 事件 / 触发 | 强支持 | 离散边仍承担中断切换和层级变化。 |
| 守卫 / 数据 | 强支持时间守卫 | guards / updates 现在可带 auxiliary clocks 和 parameters。 |
| 层次 | 强支持 | levels 仍是模型主骨架。 |
| 并发 / 同步 | 不支持 | 仍主要面向单中断控制流。 |
| 时间约束 | 强支持 | main / auxiliary clocks 共同表达细粒度中断时序。 |
| 连续动态 / 随机性 | 不支持一般连续流 | 变量仍是 clocks。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、scoped reachability、robust reachability 都有明确结果。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 扩展时钟分层 | `$X_i=\{x_i\}\uplus Y_i$` | 每层从单 main clock 扩成 main + auxiliary clocks。 |
| 顶层模型 | `$A=\langle \Sigma,n,Q,q_0,Q_f,\lambda,X,act,\Delta\rangle$` | 带辅助 clocks 的 `ITA` 骨架。 |
| 参数化模型 | `$A=\langle P,\Sigma,n,Q,q_0,Q_f,\lambda,X,act,\Delta\rangle$` | 在 `ITA` 上再叠一层参数。 |
| additive reduction | `$\exists \pi\ \text{reachable in } A(\pi) \iff \text{reachable in } A'$` | 把参数综合问题降回普通 `ITA`。 |
| robustness | `$\exists \pi,\varepsilon>0:\ \forall \pi',\|\pi-\pi'\|_\infty<\varepsilon$` reachable | 让参数鲁棒性进入 `ITA` 分支。 |

## 构造方式与承载格式

### 建模入口

建模时需要先决定：

1. 哪些 level 只需要 main clock，哪些需要 auxiliary clocks。
2. 参数是只加在常数项上，还是会乘到 clocks 上。
3. 哪些参数分析目标是 existential，哪些需要 universal 或 robust 语义。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. 带 `X_i = \{x_i\}\uplus Y_i` 的分层时钟结构。
2. additive case 到 `ITA` 的前缀编码构造。
3. multiplicative case 的参数空间分区与 class graph。

### 交换与互操作

它与 [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md) 的母线直接相连，也与 [polynomial-interrupt-timed-automata/desc.md](../polynomial-interrupt-timed-automata/desc.md) 的代数化扩展形成互补：本篇偏 auxiliary / parameter 维度，后者偏 polynomial guard / update 维度。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 class graph、parameter partition 和 additive reduction。
- 仿真/执行支持：可按 active-clock 语义直接执行。
- 验证/分析支持：auxiliary-clock reachability、existential / universal / robust parametric reachability。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `ITA` 分支上的经典理论扩展节点。

## 适用场景与需求前提

### 适用场景

适合那些 `ITA` 已能表达主干中断逻辑，但还需要：

1. 在同一 level 内记住额外的局部时间痕迹；或
2. 把某些 deadlines、drifts、timeouts 抽成参数做综合 / 鲁棒分析。

### 需求前提

1. 系统仍必须保有清晰的 interrupt-level discipline。
2. 辅助 clocks 的作用应局限在当前层或通过 main clocks 受控传播。
3. 参数化目标必须能接受理论层面的 reachability / robustness 分析，而不是立即需要工程执行器。

### 不适用或高成本场景

若辅助 clocks 与参数会导致跨层任意耦合，或需要更一般的非线性连续行为，则这条 family 的可判定性假设就很难保住。

## 与相邻形式主义的关系

相对 [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md)，它更强但仍遵守中断层级 discipline；相对 [polynomial-interrupt-timed-automata/desc.md](../polynomial-interrupt-timed-automata/desc.md)，这里的“强”主要来自 auxiliary clocks 和 parameters，而不是把 guards / updates 提升到纯 polynomial 代数层面。

## 与本研究的关系

### 对 Project 1 的价值

它把 `ITA` 主线从“一个经典节点”推进成“可以继续长后继的 branch”，尤其适合支撑演化树里关于 parameter / robustness / auxiliary-memory 的后续扩展。

### 作为目标形式主义还是中间表示

更适合作为理论选型节点或参数化中断控制流的中间表示，而不是直接工程部署格式。

### 对需求到模型生成的启发

如果需求里既有中断层级，又有“某层内部还要额外记住阶段内等待时间”或“时限值还需要综合”的表述，那么 LLM 生成 `PITA` 比停留在基础 `ITA` 更贴合。

### 现实限制

它主要服务 reachability / robustness 这类理论问题；工程工具链和标准载体仍然缺失。

## 重要的相关工作

### 奠基或前身工作

- [interrupt-timed-automata/desc.md](../interrupt-timed-automata/desc.md)

### 同类型或同家族工作

- [polynomial-interrupt-timed-automata/desc.md](../polynomial-interrupt-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的“基础设施”是 additive reduction、parameter partition 和 class-graph reasoning。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Interrupt Timed Automata -> Interrupt Timed Automata with Auxiliary Clocks and Parameters`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Interrupt Timed Automata with Auxiliary Clocks / Parametric Interrupt Timed Automata (PITA)`
- 论文角色：模型扩展
- 核心功能：给 `ITA` 增加辅助时钟与参数化 guards / updates，同时保住 reachability 与 robustness 的可判定性。
- 关键特性：main / auxiliary clocks、additive reduction、multiplicative parameter partition、scoped / universal / robust reachability。
- 构造方式：`A=\langle \Sigma,n,Q,q_0,Q_f,\lambda,X,act,\Delta\rangle` 与 `A=\langle P,\Sigma,n,Q,q_0,Q_f,\lambda,X,act,\Delta\rangle`。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：参数化中断控制流、level 内细粒度时序、鲁棒 deadline 分析。
- 需求前提：系统具备清晰 interrupt levels，且辅助 clocks / 参数不会打破层级 discipline。
- 状态：🟢
