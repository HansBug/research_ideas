# 递归混成自动机的一人与两人可达性问题 / On the Reachability Problem for Recursive Hybrid Automata with One and Two Players

## 基本信息

- 标题：On the Reachability Problem for Recursive Hybrid Automata with One and Two Players
- 中文标题：递归混成自动机的一人与两人可达性问题
- 作者：Shankara Narayanan Krishna、Lakshmi Manasa、Ashutosh Trivedi
- 发表：arXiv preprint arXiv:1406.7289, 2014
- DOI：原文未提供；相关后续会议版本为 `Reachability Games on Recursive Hybrid Automata`, TIME 2015, DOI `10.1109/TIME.2015.27`
- 链接：https://arxiv.org/abs/1406.7289
- 形式主义：`Recursive Hybrid Automata (RHA)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型定义与判定边界系统化分析
- 工具/实现获取方式：原文未提供工程工具；机器可处理入口是 `RHA` tuple、configuration semantics、pass-by-value / pass-by-reference 机制、glitch-free / bounded-context 子类与 time-bounded contraction reasoning。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 recursive components、boxes、stopwatch / clock 变量、上下文栈语义和 reachability-game framing。

## 简报

虽然这篇论文的标题强调的是 reachability，但对当前文库更重要的是：它给出了 `Recursive Hybrid Automata` 这条 family 的完整语法、语义、子类划分和可判定边界。换句话说，它不是单纯拿 `HA` 做一个算法题，而是把“带递归调用的 singular / stopwatch hybrid automata”正式固定成了一个稳定模型点。

- 形式主义定位：`Recursive Timed Automata` 向连续变量 / stopwatch 语义扩出来的混成递归分支。
- 构造方式简述：把 `RSM` 的 box / call-return 骨架、`HA` 的 continuous variables、以及 by-value / by-reference 参数传递机制合并到一起。
- 基础设施与场景简述：核心基础设施是 configuration LTS、glitch-free restriction、bounded-context contraction 与 one-player / two-player reachability games。

```text
recursive state machines + hybrid variables + pass-by-value/reference -> RHA -> recursive hybrid control / verification
```

## 形式主义定义与核心对象

### 定义对象

`RHA` 要建模的是“可递归调用的 hybrid control flow”。相比普通 `Hybrid Automata`，新增的是组件调用栈和变量传参；相比 [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)，新增的是 clocks 之外更一般的连续变量、stopwatch 和 singular-rate dynamics。

### 核心抽象

原文 Definition 1 把递归混成自动机写成：

$$
H=(X,(H_1,H_2,\ldots,H_k))
$$

上式中的符号逐项解释如下：

1. `X` 是全局连续变量集合。
2. `H_1,\ldots,H_k` 是组件集合。

每个组件 `H_i` 的骨架为：

$$
H_i=(N_i,EN_i,EX_i,B_i,Y_i,A_i,X_i,P_i,Inv_i,E_i,J_i,F_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集，`EN_i` / `EX_i` 分别是入口和出口节点。
2. `B_i` 是 boxes，也就是调用别的组件的位置。
3. `Y_i` 指定每个 box 映射到哪个组件。
4. `A_i` 是动作集，`X_i` 是离散转移函数。
5. `P_i : B_i \to 2^X` 给每个 box 指定哪些变量按值传递，其余变量按引用传递。
6. `Inv_i` 是 invariant，`E_i` 是 action enabledness。
7. `J_i` 是 reset 集，`F_i` 是 flow function。

### 一个最小例子与通俗解释

最直观的例子是一个主控制过程 `Main` 调用一个子过程 `Check`：

1. `Main` 里某个 stopwatch `x` 记录已经等待了多久；
2. 进入 box 调用 `Check` 时，可以规定 `x` 按值传递，也可以规定按引用传递；
3. 若按值传递，返回时 `Main` 看到的是调用前的 `x`；若按引用传递，返回时保留 `Check` 内部经过时间流逝后的 `x`。

通俗地说，`RHA` 就像“给 hybrid automata 加上函数调用和参数传递”。它不再只是一张扁平状态图，而是一个带连续变量栈语义的递归程序模型。

### 运行 / 接受 / 转移语义

原文 Definition 2 中，一个 configuration 写成：

$$
(\langle \kappa \rangle,q,\nu)
$$

上式中的符号逐项解释如下：

1. `\langle \kappa \rangle \in (B\times \mathbb R^{|X|})^*` 是未返回调用的上下文栈。
2. `q` 是当前 location。
3. `\nu` 是当前变量 valuation，且必须满足 `Inv(q)`。

若当前位置不是 call/return 特殊点，则时间流逝和离散动作满足：

$$
\nu + F(q)\cdot t' \in Inv(q)\ \text{for all } t' \in [0,t]
$$

并在动作 `a` 可使能时：

$$
\nu' = (\nu + F(q)\cdot t)[J(a):=0]
$$

若当前位置是 call port，则把当前 box 和 valuation 压栈；若是 exit node，则按照 `P(b)` 的 by-value / by-reference 规则恢复或保留变量。

### 语义边界

原文额外定义了几个直接决定可判定性的子类：

1. `glitch-free`：每个 box 要么所有变量都按值传递，要么全部按引用传递。
2. `hierarchical`：高层组件不能调用同阶或更高阶组件。
3. `bounded-context`：递归上下文深度被限制。

这些不是实现细节，而是 `RHA` 家族内部的重要分支节点。

### 关键性质与判定边界

原文给出一组很清晰的边界：

$$
\text{Reachability is undecidable for unrestricted RHA with } \ge 2 \text{ stopwatches}
$$

同时也给出正结果：

$$
\text{Time-bounded reachability is decidable for bounded-context RHA using only pass-by-reference}
$$

以及：

$$
\text{Reachability for glitch-free RHA with 2 stopwatches is decidable}
$$

因此，`RHA` 不是一个单一复杂度点，而是一整条“递归 + hybrid variables + parameter passing”分层 family。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有 locations、components、boxes 与显式 call/return。 |
| 事件 / 触发 | 强支持 | 离散动作和递归调用都可触发结构变化。 |
| 守卫 / 数据 | 强支持 | invariants、guards、resets 与 by-value/by-reference 都是核心。 |
| 层次 | 强支持 | 组件层次和递归上下文是模型骨架。 |
| 并发 / 同步 | 不支持 | 原始 family 关注递归控制流，不是并发组合。 |
| 时间约束 | 强支持 | 时间流逝、clocks、stopwatches 与 time-bounded reachability 都明确。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 论文聚焦 singular / stopwatch hybrid dynamics。 |
| 可执行 / 可验证性 | 强理论支持 | 一般情形不可判，bounded-context / glitch-free 子类可判。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 顶层模型 | `$H=(X,(H_1,\ldots,H_k))$` | 把 hybrid variables 嵌入递归组件系统。 |
| 组件骨架 | `$H_i=(N_i,EN_i,EX_i,B_i,Y_i,A_i,X_i,P_i,Inv_i,E_i,J_i,F_i)$` | call/return、变量传参和 hybrid 语义都在这里。 |
| configuration | `$(\langle\kappa\rangle,q,\nu)$` | 语义必须同时记住调用栈和连续变量值。 |
| glitch-free | `$P(b)=X$ or $P(b)=\varnothing$` | 可判定性的重要分界。 |
| 复杂度边界 | undecidable / decidable split | 形成完整的 recursive-hybrid family 地图。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. 哪些控制逻辑适合拆成独立组件；
2. 哪些连续变量需要按值传递，哪些应按引用传递；
3. 动力学是否能约束到 singular / stopwatch 级别；
4. 是否需要 bounded-context 或 glitch-free 来换取可判定性。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. component / box / call-return 骨架；
2. continuous valuations 与 context stack；
3. glitch-free / bounded-context 限制；
4. one-player / two-player reachability-game framing。

### 交换与互操作

它和以下 family 的关系最直接：

1. [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)
2. 一般 `Hybrid Automata`
3. `Recursive Stopwatch Automata`

可以把它理解成“把 `RTA` 的递归骨架换成了更一般的 singular hybrid dynamics”。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 component syntax、configuration semantics 和 region / contraction style abstractions。
- 仿真/执行支持：可按 configuration LTS 和 flow function 解释。
- 验证/分析支持：reachability、termination、games、time-bounded variants、glitch-free / bounded-context decidability。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于递归程序验证与 hybrid automata 理论交叉地带的 family 节点。

## 适用场景与需求前提

### 适用场景

适合那些：

1. 控制逻辑本身具有递归调用结构；
2. 组件内部既有连续时间演化，又要保留调用栈语义；
3. 目标是研究可达性、博弈或 time-bounded verification。

### 需求前提

1. 连续动力学最好能约束到 singular / stopwatch 语义。
2. 需要显式区分 by-value 和 by-reference 变量传递。
3. 若想获得正结果，通常还要接受 glitch-free 或 bounded-context 之类的结构限制。

### 不适用或高成本场景

若系统没有递归调用，普通 `HA` 或 `RTA` 更简单；若连续动力学很复杂、非线性且必须并发组合，`RHA` 的理论框架也会迅速变重。

## 与相邻形式主义的关系

相对 [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)，`RHA` 把“递归 + 时钟”推广到更一般的 hybrid variables；相对一般 `Hybrid Automata`，它增加了 call/return / context stack；相对 `Recursive Stopwatch Automata`，它又是更大的母类。

## 与本研究的关系

### 对 Project 1 的价值

它为 `Hybrid Automata` 主干补出了此前还空着的 `recursive hybrid` 节点，使 timed recursion 和 hybrid recursion 两条线在演化树里都闭合起来。

### 作为目标形式主义还是中间表示

更适合作为高表达力理论目标或语义上界，而不是直接面向工程应用的首选模型。

### 对需求到模型生成的启发

当需求天然带有层次化子过程调用，而且每个子过程内部还有连续演化时，LLM 不应强行平铺成普通 `HA`；先抽成 `RHA` 更能保留控制流结构。

## 重要的相关工作

### 奠基或前身工作

- [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)
- 一般 `Hybrid Automata`

### 同类型或同家族工作

- `Recursive Stopwatch Automata`
- `glitch-free RHA`
- `bounded-context RHA`

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的基础设施是 context semantics、glitch-free discipline 和 time-bounded contraction。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Hybrid Automata -> Recursive Hybrid Automata`，并在说明里标出它与 `Recursive Timed Automata` 的邻接关系。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
