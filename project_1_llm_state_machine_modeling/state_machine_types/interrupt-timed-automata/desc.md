# 中断时间自动机 / Interrupt Timed Automata

## 基本信息

- 标题：Interrupt Timed Automata: Verification and Expressiveness
- 中文标题：中断时间自动机：验证与表达能力
- 作者：Beatrice Berard、Serge Haddad、Mathieu Sassolas
- 发表：*Formal Methods in System Design*, 40(1):41-87, 2012
- DOI：`10.1007/s10703-011-0140-2`
- 链接：https://arxiv.org/pdf/1203.6453.pdf
- 形式主义：`Interrupt Timed Automata (ITA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 level-based interrupt clocks、state timing policy、class graph 与 `ITA^-` 化简。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `(\Sigma,AP,Q,q_0,F,pol,X,\lambda,lab,\Delta)` 结构、active-clock 语义与 class-graph abstraction。

## 简报

这篇论文提出了一条和普通 `Timed Automata` 明显不同的 timed family：系统按 interrupt levels 组织，在任意时刻**只有当前 level 的 clock 在走**，低层 clocks 被冻结，高层 clocks 还未激活。这让它非常适合表达单处理器上的任务打断、抢占和恢复。论文最重要的价值不是“能模拟暂停时钟”本身，而是证明了这条 family 的 untimed language 仍 regular，reachability 可判，而且它与 classical `TA` / `CRTA` 在表达力上不可比。

- 形式主义定位：面向 preemption / interruption 的 level-based timed automata family。
- 构造方式简述：状态带 level 和 `Lazy/Urgent/Delayed` policy；每个 level 一只 interrupt clock，时间推进时只有 active clock 演化。
- 基础设施与场景简述：核心基础设施是 class graph、`ITA^-`、reachability / model checking complexity 和 expressiveness comparison，而不是工程运行库。

```text
interrupt levels -> one active clock per level -> lower clocks frozen -> class graph abstraction -> decidable reachability for timed interruption models
```

## 形式主义定义与核心对象

### 定义对象

`ITA` 的目标对象是“带抢占和中断的实时控制流”。普通 `TA` 默认所有 clocks 一起流逝；`ITA` 则明确表达“当前正在执行哪一层任务”，并用层级切换来冻结或恢复 clocks。

### 核心抽象

原文的正式定义是：

$$
A = \langle \Sigma, AP, Q, q_0, F, pol, X, \lambda, lab, \Delta \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是动作字母表，`AP` 是原子命题集。
2. `Q` 是有限状态集，`q_0` 是初始状态，`F` 是接受状态集。
3. `pol:Q \to \{Lazy, Urgent, Delayed\}` 给每个状态分配时间策略。
4. `X = \{x_1,\ldots,x_n\}` 是 interrupt clocks。
5. `\lambda:Q \to \{1,\ldots,n\}` 给每个状态分配 level，`x_{\lambda(q)}` 是该状态的 active clock。
6. `lab` 给状态打原子命题标签。
7. `\Delta` 是迁移集合，guards 只允许引用当前及更低 level 的 clocks，updates 受 level discipline 限制。

### 一个最小例子与通俗解释

最小直觉例子是一个两层任务系统：

1. `q_0` 处于 level 1，主任务运行，只有 `x_1` 递增。
2. 一旦高优先级中断到来，系统跳到 level 2 的 `q_1`，此时 `x_1` 冻结，开始让 `x_2` 计时。
3. 中断处理结束后回到低层，继续使用冻结前的 `x_1`。

通俗地说，`ITA` 像“带硬件暂停键的时间自动机”。普通 `TA` 里所有 clocks 都是一起走的挂钟；`ITA` 里的 clocks 更像分层任务的 CPU 执行计时器，谁在跑，谁的时间才往前走。

### 运行 / 接受 / 转移语义

原文的语义配置写成：

$$
(q,v,\beta)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `v` 是各 interrupt clocks 的赋值。
3. `\beta` 记录自上次离散迁移后是否已经有时间流逝，用于处理 `Delayed` policy。

若在状态 `q` 中时间流逝 `d`，则只有 active clock 增长：

$$
v'(x_{\lambda(q)}) = v(x_{\lambda(q)}) + d
$$

并且：

$$
v'(x) = v(x) \quad \text{for all other clocks } x
$$

离散迁移则要求存在

$$
q \xrightarrow{\varphi,a,u} q'
$$

满足：

$$
v \models \varphi,\qquad v' = v[u]
$$

此外：

$$
pol(q)=Urgent \Rightarrow d=0
$$

以及：

$$
pol(q)=Delayed \land \beta=\bot \Rightarrow \text{discrete step forbidden}
$$

### 语义边界

论文明确指出：`ITA` 是 hybrid-automata 背景下的受限 timed model，但它和 classical `TA` / `CRTA` 在 timed-language 角度**不可比**。因此它不是普通 `TA` 的简单子类，也不是一般 `HA` 的工程化近似，而是一条独立、稳定的中断时间分支。

### 关键性质与判定边界

论文首先证明：

$$
\text{the untimed language of an ITA is regular}
$$

并给出 reachability 的复杂度边界：

$$
\text{Reachability(ITA)} \in \mathrm{NEXPTIME}
$$

当 clocks 数固定时还有：

$$
\text{Reachability(ITA)} \in \mathrm{PTIME}
$$

此外，论文还证明：

$$
\text{the timed-language families of ITA and TA are incomparable}
$$

以及与 `CRTA` 也不可比；同时 `SCL` 这类 timed linear logic 的 model checking 不可判，但若干 branching-time fragments 仍可判。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 状态带显式 level 和 timing policy。 |
| 事件 / 触发 | 强支持 | 离散迁移表达任务切换、中断进入和退出。 |
| 守卫 / 数据 | 强支持时间守卫 | guards / updates 受 level discipline 限制。 |
| 层次 | 强支持 | interrupt levels 是模型骨架，而不是附属注释。 |
| 并发 / 同步 | 不支持 | 原始模型主要面向单处理器抢占控制流。 |
| 时间约束 | 强支持 | active/frozen clock 语义是模型核心。 |
| 连续动态 / 随机性 | 不支持一般连续流 | 变量仍是 clocks，不是一般 ODE。 |
| 可执行 / 可验证性 | 强理论支持 | class graph、reachability、若干 model-checking fragment 都清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=\langle \Sigma,AP,Q,q_0,F,pol,X,\lambda,lab,\Delta\rangle$` | 给 interrupt family 一个标准骨架。 |
| 配置 | `$(q,v,\beta)$` | 语义中必须保留状态、clock valuation 与 delayed-policy 标志。 |
| 时间推进 | `$v'(x_{\lambda(q)})=v(x_{\lambda(q)})+d$` | 任一时刻只有 active clock 真正流逝。 |
| 可判定性 | `untimed language regular` | 可用有限 abstraction 组织分析。 |
| 表达边界 | `ITA \nsubseteq TA` 且 `TA \nsubseteq ITA` | 说明它值得作为独立树节点。 |

## 构造方式与承载格式

### 建模入口

建模时首先要决定：

1. 系统应分成多少个 interrupt levels。
2. 每个 level 的 clock 应计哪类执行时间。
3. 哪些状态必须 `Urgent`、哪些允许 `Delayed`。
4. 哪些 level 切换会冻结或重置已有 clocks。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. level-annotated states。
2. interrupt-clock guards / updates。
3. class graph 与 `ITA^-` 化简。

### 交换与互操作

它与 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 classical `TA` 主线、[the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md) 的 stopwatch 语义分支，以及后续的参数 / 多项式扩展都有直接关系，但其表达力边界足以单独形成 timed-interruption 主线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 class graph、`ITA^-` 和 level-disciplined clock expressions。
- 仿真/执行支持：可直接按 timed transition system 运行。
- 验证/分析支持：regular untimed language、reachability、CTL-style fragments、expressiveness comparison。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 timed / hybrid boundary 上的经典理论 family。

## 适用场景与需求前提

### 适用场景

适合单处理器抢占式任务系统、带 interrupt levels 的实时调度语义、以及需要显式保留“暂停/恢复执行时间”结构的理论建模。

### 需求前提

1. 系统必须能自然写成若干 priority levels。
2. 时间应主要理解为不同层级任务的执行时间，而不是全局 wall-clock。
3. 中断进入和退出的结构必须稳定且有限。

### 不适用或高成本场景

若系统本质上是一般 dense-time 并发网络，或需要所有 clocks 一起演化，普通 `TA` 更自然；若还需一般连续流，则更靠近 `HA`。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，`ITA` 最大差别是 active/frozen clock 语义；相对 [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)，它不是任意 stopwatch 组合，而是受 interrupt levels 约束的可判定子类；相对一般 `HA`，它仍然只操作 clocks，而不进入通用连续动力学。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了一条此前缺失的“timed interruption / preemption”主线，不必再把所有暂停时钟语义都硬塞到 `Stopwatch Automata` 或一般 `Hybrid Automata` 下面。

### 作为目标形式主义还是中间表示

对带明确抢占语义的实时控制软件，它可以直接作为目标形式主义；对一般控制逻辑，则更像一个理论参照节点。

### 对需求到模型生成的启发

如果需求里明确区分“主任务执行”“高优中断打断”“中断结束恢复”，那么 LLM 直接生成 `ITA` 通常比把这些语义绕成普通 `TA` 的 reset 方案更自然。

### 现实限制

它的工程工具生态明显弱于 `UPPAAL` 主线，而且一旦放宽为更一般的 hybrid/stopwatch 形式，可判定性很快消失。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)
- [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)

### 同类型或同家族工作

- [polynomial-interrupt-timed-automata/desc.md](../polynomial-interrupt-timed-automata/desc.md)
- [interrupt-timed-automata-with-auxiliary-clocks-and-parameters/desc.md](../interrupt-timed-automata-with-auxiliary-clocks-and-parameters/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的“基础设施”是 class-graph abstraction 和 complexity results。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `时间 / 连续主干 -> Interrupt Timed Automata` 的独立中断时间分支。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Interrupt Timed Automata (ITA)`
- 论文角色：模型提出
- 核心功能：用 level-based active/frozen clock 语义精确表达带中断和抢占的实时控制流。
- 关键特性：interrupt levels、`Lazy/Urgent/Delayed` policy、class graph、reachability decidability、与 `TA/CRTA` 不可比。
- 构造方式：`A=\langle \Sigma,AP,Q,q_0,F,pol,X,\lambda,lab,\Delta\rangle`。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：抢占式任务系统、实时中断控制流、level-based execution-time modeling。
- 需求前提：需求能稳定分成 interrupt levels，并显式关心暂停/恢复执行时间。
- 状态：🟢
