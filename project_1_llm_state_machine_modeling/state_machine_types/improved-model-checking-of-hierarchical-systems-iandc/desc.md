# 分层系统的改进模型检验（I&C 全文版） / Improved model checking of hierarchical systems

## 基本信息

- 标题：Improved model checking of hierarchical systems
- 中文标题：分层系统的改进模型检验（I&C 全文版）
- 作者：Benjamin Aminof, Orna Kupferman, Aniello Murano
- 发表：*Information and Computation*, 210:68-86, 2012
- DOI：`10.1016/j.ic.2011.10.008`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/Hierarchial-extended.pdf
- 形式主义：`Hierarchical Systems / Hierarchical Structures`，并在同文中系统引入 `Hierarchical Modal Transition Systems (HMTS)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / finite hierarchy + HMTS abstraction
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 hierarchical arena / structure tuple、hierarchical games、flat expansion、hierarchical parity games 与 `HMTS` abstraction-refinement。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 sub-structures、boxes、exit summaries、must/may transitions、`HMTS` 与 hierarchy-preserving abstraction。

## 简报

这篇 `I&C 2012` 全文版把 `VMCAI 2010` 的 `hierarchical systems / HMTS` 条目真正做实了：它不再只是“模型检验还能更快”，而是把 finite hierarchy 重新确立为值得独立维护的 formalism，同时把 hierarchical games、hierarchical parity games 和 `HMTS` abstraction-refinement 统一纳入同一条语义链。对当前演化树来说，这使 `HSM -> Hierarchical Systems / HMTS` 不再只有 conference 起点，而有了更完整的 journal-level family 依据。

- 形式主义定位：`HSM` 之后对 finite hierarchy 的稳定再命名，也是 `HMTS` 进入层次状态机支线的正式全文版入口。
- 构造方式简述：系统由一组有限深度的 sub-structures 组成，boxes 只允许指向更深层结构；在 abstraction 侧，又引入 `must/may` transition 与 `?` 标记，构成 hierarchy-preserving `HMTS`。
- 基础设施与场景简述：全文版最重要的新增，是 unified game-based approach、hierarchical parity games 以及 hierarchy-preserving abstraction-refinement，而不是单一逻辑的小修补。

```text
finite reused sub-systems -> hierarchical structures -> hierarchical games / parity games -> HMTS abstraction -> hierarchy-preserving model checking
```

## 形式主义定义与核心对象

### 定义对象

论文坚持把“有限层次复用”与“无界递归”区分开来。也就是说，它研究的不是 `uHSM / RSM` 那种 unbounded stack，而是 repeated sub-systems 的有限深度 hierarchy。

### 核心抽象

原文先把一个 hierarchical arena 写成：

$$
V = \langle V_1,\ldots,V_n \rangle
$$

其中每个 sub-arena 为：

$$
V_i = \langle W_i^0, W_i^1, B_i, in_i, exit_i, \tau_i, R_i \rangle
$$

上式中的符号逐项解释如下：

1. `W_i^0` 与 `W_i^1` 分别是 player 0 / player 1 的状态集合。
2. `B_i` 是 boxes 集合。
3. `in_i` 是初始状态，`exit_i` 是出口状态集合。
4. `\tau_i : B_i \to \{i+1,\ldots,n\}` 规定每个 box 指向哪个更深层 sub-arena。
5. `R_i` 是局部边关系。

对应的单玩家 hierarchical structure 写成：

$$
K = \langle K_1,\ldots,K_n \rangle,\qquad
K_i = \langle AP, V_i, \sigma_i \rangle
$$

journal full version 进一步把 hierarchy-preserving abstraction 写成：

$$
M = \langle M_1^A,\ldots,M_n^A \rangle
$$

其中每个 `M_i^A` 都带有 `R_i^{must} \subseteq R_i^{may}` 与三值标签 `\sigma_i^A : W_i^A \times AP \to \{tt, ff, ?\}`，这就是 `HMTS` 的核心骨架。

### 一个最小例子与通俗解释

可以把它理解成“有限层次任务控制器”：

1. 顶层任务里有一个 box 代表“停靠流程”。
2. 这个流程子结构只定义一次，但可在多个上层位置复用。
3. 复用深度有限，因此不会产生无界调用栈。
4. 若还想做抽象，可把若干状态和若干 concrete boxes 合并成 abstract state / abstract box，得到 `HMTS`。

通俗地说，它是“明确不让 hierarchy 退化成 recursion 的层次状态机 family”，而 journal full version 的新增则是：即便做抽象，也不必先 flatten。

### 运行 / 接受 / 转移语义

hierarchical system 的 flat state 形如：

$$
(b_0,\ldots,b_k,w)
$$

上式中的符号逐项解释如下：

1. `b_0,\ldots,b_k` 是沿 hierarchy 进入当前状态的 box 上下文。
2. `w` 是最内层 sub-structure 里的真实状态。

整套系统的平展语义记作：

$$
K^f
$$

于是公式满足关系由：

$$
K \models \varphi \iff K^f \models \varphi
$$

给出。全文版进一步把 model checking 统一规约到 hierarchical game，再规约到 hierarchical parity game，因此得到：

$$
\text{solve } G_{K,A_\varphi}
$$

这条统一语义链。

### 语义边界

这个 family 的边界如下：

1. boxes 只能指向更深层编号结构，因此 hierarchy depth 有限。
2. 它不是 recursive family，没有无界 stack。
3. `HMTS` 不是另起一条 DSL 线，而是同一 family 上的 hierarchy-preserving abstraction 载体。
4. 其优势不只在 succinctness，还在“不 flatten 也能做 branching-time reasoning”。

### 关键性质与判定边界

全文版最关键的复杂度结论之一是：

$$
\mathrm{MC}(Hierarchical\ Systems, \mu\text{-calculus}) \text{ is } \mathrm{PSPACE}\text{-complete}
$$

并且原文强调，时间复杂度只在 hierarchy depth 上多项式增长。与此同时，hierarchical parity games 的求解又构成了各类 branching-time logics 的统一后端，而 `HMTS` 则提供了：

$$
R_i^{must} \subseteq R_i^{may}, \qquad \sigma_i^A(\cdot,\cdot) \in \{tt,ff,?\}
$$

这一套 hierarchy-preserving abstraction 语义。这使全文版既稳定了 `Hierarchical Systems` 节点，也稳定了 `HMTS` 这条 side branch。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | sub-structures、boxes、entry/exit、reused components。 |
| 事件 / 触发 | 弱支持 | 核心在结构层次与博弈/抽象语义，不在动作标签。 |
| 守卫 / 数据 | 不支持 | 原文重点不在变量。 |
| 层次 | 强支持 | 有限深度 hierarchy 是定义核心。 |
| 并发 / 同步 | 不支持 | 这里仍是 sequential finite hierarchy。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | hierarchical games、parity games、`$\mu$-calculus` 与 `HMTS` abstraction。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| hierarchical arena | `$V = \langle V_1,\ldots,V_n \rangle$` | 有限层次骨架。 |
| sub-arena | `$V_i = \langle W_i^0, W_i^1, B_i, in_i, exit_i, \tau_i, R_i \rangle$` | 单层 hierarchy 单元。 |
| hierarchical structure | `$K = \langle K_1,\ldots,K_n \rangle$` | 单玩家 finite hierarchy 系统。 |
| `HMTS` 抽象 | `$R_i^{must} \subseteq R_i^{may}$`, `$\sigma_i^A \in \{tt,ff,?\}$` | hierarchy-preserving abstraction 的核心对象。 |
| 判定边界 | `$\mathrm{MC}(Hierarchical\ Systems,\mu\text{-calculus})$ is `PSPACE`-complete` | journal full version 稳定下来的主口径。 |

## 构造方式与承载格式

### 建模入口

1. 先把系统拆成若干可复用的 finite sub-structures。
2. 用 boxes 引用更深层 sub-structures，保证 hierarchy 有限。
3. 若要做 branching-time verification，则把结构乘上对应 automaton，转成 hierarchical games。
4. 若要做抽象，则直接在 hierarchy 上构造 `HMTS`，而不是先 flatten。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. hierarchical arena / structure tuples；
2. flat expansion `K^f`；
3. hierarchical games / hierarchical parity games；
4. `HMTS` must/may abstraction；
5. abstraction-refinement loop。

### 交换与互操作

它与当前文库中的关系如下：

1. 会议起点是 [improved-model-checking-of-hierarchical-systems/desc.md](../improved-model-checking-of-hierarchical-systems/desc.md)。
2. 向上承接 [model-checking-of-hierarchical-state-machines-toplas/desc.md](../model-checking-of-hierarchical-state-machines-toplas/desc.md) 与 [formal-analysis-of-hierarchical-state-machines/desc.md](../formal-analysis-of-hierarchical-state-machines/desc.md) 的 `HSM` 母线。
3. 向旁对照 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 与 [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)，强调“finite hierarchy 不应被递归线完全吞掉”。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 hierarchical tuples、hierarchical games 与 `HMTS`。
- 仿真/执行支持：可通过 flat expansion 或 hierarchy-preserving game semantics 解释。
- 验证/分析支持：hierarchical parity games、`$\mu$-calculus` model checking、`HMTS` abstraction-refinement。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要价值在有限 hierarchy 本体与 hierarchy-preserving abstraction。

## 适用场景与需求前提

### 适用场景

适合：

1. 有大量 repeated sub-systems、但 nesting depth 有限的层次控制逻辑。
2. 不希望为了验证先把 hierarchy 完全 flatten 掉的系统。
3. 需要 hierarchy-preserving abstraction / refinement 的层次状态机分析。

### 需求前提

1. 复用关系必须是有限层次，而不是无界递归。
2. 系统压缩收益主要来自 repeated sub-systems。
3. 关注的是 branching-time / parity / abstraction 问题，而不是工程 DSL 外观。

### 不适用或高成本场景

如果系统有真正的无界递归，应转向 `uHSM / RSM`；如果还要开放环境分区，应转向 open hierarchy / open pushdown；如果只是工程执行语言，则无需挂到这条理论枝上。

## 与相邻形式主义的关系

相对 conference 版，这篇全文版把 unified game-based approach、hierarchical parity games 与 `HMTS` abstraction 全部固定下来；相对 `HSM`，它更明确地把 bounded hierarchy 稳定成独立 family；相对 `uHSM / RSM`，它坚持 hierarchy 是 finite reuse，而不是 recursion。

## 与本研究的关系

### 对 Project 1 的价值

它提醒我们：层次状态机支线不应只沿递归方向膨胀。对很多需求到模型任务，finite hierarchy 本身就是更自然、更可控的目标 family。

### 作为目标形式主义还是中间表示

可以同时作为目标形式主义候选与验证导向中间表示候选，尤其适合“重复子流程复用但不需要无界调用栈”的需求。

### 对需求到模型生成的启发

如果需求里主要信号是“重复子任务复用”“有限层次嵌套”“不希望平铺成大图”，那么自动建模时应优先考虑 `Hierarchical Systems / HMTS` 一线，而不是默认抬升到 recursion。

### 现实限制

它仍是理论条目，没有工程语言与工业工具生态。

## 重要的相关工作

### 奠基或前身工作

- [improved-model-checking-of-hierarchical-systems/desc.md](../improved-model-checking-of-hierarchical-systems/desc.md)
- [model-checking-of-hierarchical-state-machines-toplas/desc.md](../model-checking-of-hierarchical-state-machines-toplas/desc.md)

### 同类型或同家族工作

- [formal-analysis-of-hierarchical-state-machines/desc.md](../formal-analysis-of-hierarchical-state-machines/desc.md)
- `HMTS` / hierarchical abstraction line
- [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)：作为 finite hierarchy 的 open recursive 对照线。

## 文献分类总结

- 这篇全文版把 `Hierarchical Systems / HMTS` 从 2010 conference 节点稳定成了 journal-level family。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、应用或纯算法优化条目。
- 在当前演化树里，它最适合继续挂在 `Statecharts -> HSM -> Hierarchical Systems / HMTS`，并作为该节点的 2012 full-version 锚点。
