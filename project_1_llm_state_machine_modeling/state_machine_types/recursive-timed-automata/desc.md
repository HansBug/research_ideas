# 递归时间自动机 / Recursive Timed Automata

## 基本信息

- 标题：Recursive Timed Automata
- 中文标题：递归时间自动机
- 作者：Ashutosh Trivedi、Dominik Wojtczak
- 发表：*Automated Technology for Verification and Analysis* (ATVA 2010), pp. 306-324, 2010
- DOI：`10.1007/978-3-642-15643-4_23`
- 链接：https://qav.cs.ox.ac.uk/papers/atva10.pdf
- 形式主义：`Recursive Timed Automata (RTA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 timed automata components、boxes、entry/exit nodes、clock pass-by-value / pass-by-reference 机制与 region abstraction。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 recursive timed automaton tuple、configuration semantics、glitch-free restriction 与 reachability / termination games。

## 简报

这篇论文把普通 `Timed Automata` 的“平面状态图”提升成“可递归调用的组件集合”。也就是说，状态里不再只有 location，还允许通过 box 调用另一个 timed component，并显式区分 clock 是按值传递还是按引用传递。对当前文库来说，这正好把 `Timed Automata` 主干向“call/return / recursive control flow”方向补出一个经典理论节点。

- 形式主义定位：`Timed Automata` 主干上的递归 / call-return 结构扩展。
- 构造方式简述：把 timed automata 包装成多个带 entry / exit 的组件，并通过 box 调用彼此；调用时 clocks 可按值或按引用传递。
- 基础设施与场景简述：原文是纯理论工作，但 reachability、termination、games、glitch-free fragment 与 region abstraction 都给得很完整。

```text
timed automaton component -> box call / return -> clock pass-by-value or pass-by-reference -> recursive timed control flow
```

## 形式主义定义与核心对象

### 定义对象

论文从 recursive state machines 出发，把 timed automata 的 clock、guard、invariant 和 reset 机制嫁接到“组件 + 调用栈”骨架上。其目标对象，是带递归调用的 timed control flow，而不是普通扁平 timed transition system。

### 核心抽象

递归时间自动机的语法在原文 Definition 4 中写成：

$$
T = (C, (T_1, T_2, \ldots, T_k))
$$

上式中的符号逐项解释如下：

1. `C` 是全局时钟集合。
2. `T_1,\ldots,T_k` 是各个组件。

每个组件 `T_i` 则写成：

$$
T_i = (N_i, En_i, Ex_i, B_i, Y_i, A_i, X_i, P_i, Inv_i, E_i, \rho_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集，`En_i` / `Ex_i` 分别是入口和出口节点。
2. `B_i` 是 boxes，也就是“调用别的组件”的位置。
3. `Y_i : B_i \to \{1,\ldots,k\}` 指明每个 box 调到哪个组件。
4. `A_i` 是动作集。
5. `X_i` 是离散转移函数。
6. `P_i : B_i \to 2^C` 指明 box 调用时哪些时钟按值传递；剩余时钟按引用传递。
7. `Inv_i` 是位置不变式。
8. `E_i` 是动作可使能条件。
9. `\rho_i` 是时钟 reset 函数。

### 一个最小例子与通俗解释

最小直觉例子是一个主组件 `Main` 调用子组件 `Check`：

1. `Main` 在本地 clock `x` 达到某个阈值后进入 box。
2. `Check` 内部可以继续等待并重置某些 clock。
3. 若 `x` 是按值传递，则返回 `Main` 后 `x` 恢复成调用前的值；若按引用传递，则返回后看到的是子组件执行后的当前值。

通俗地说，`RTA` 就像“给 timed automata 加上函数调用”。普通 `TA` 只能在一张平面图里来回走；`RTA` 则允许带时钟语义的子程序调用，而且时钟还能像程序变量一样区分 by-value 和 by-reference。

### 运行 / 接受 / 转移语义

论文的配置写成：

$$
(\langle \kappa \rangle, q, \nu)
$$

上式中的符号逐项解释如下：

1. `\langle \kappa \rangle \in (B \times V)^*` 是调用上下文，也就是尚未返回的 box 栈和保存的 clock valuations。
2. `q` 是当前顶层组件中的顶点。
3. `\nu` 是当前 clock valuation。

语义上，若 `q` 是普通顶点，则和普通 `TA` 一样先让时间流逝、再做离散动作；若 `q` 是 call port，则把当前 box 与 valuation 压栈并跳到被调用组件的入口；若 `q` 是 exit node`，则按 box 的传参机制恢复或保留 clocks 后返回。

### 语义边界

论文定义了一个关键可判定性边界：glitch-free。

$$
\text{glitch-free} \iff \forall b \in B,\ P(b)=C \text{ or } P(b)=\varnothing
$$

也就是说，对每个 box，要么所有 clocks 都按值传递，要么所有 clocks 都按引用传递，不能混搭。原文证明，这个限制正是从不可判到可判的关键分界。

### 关键性质与判定边界

最重要的负结果是：

$$
\text{Termination problem is undecidable for recursive timed automata with at least 3 clocks}
$$

而游戏版本更强：

$$
\text{Termination game problem is undecidable for recursive timed automata with at least 2 clocks}
$$

另一方面，对 glitch-free `RTA`，原文通过 region abstraction 把问题降到 recursive-state-machine 风格的有限抽象上，因此 reachability / termination 恢复可判。论文给出的复杂度结论之一可压成：

$$
\text{Reachability for 1-player glitch-free RTA with at least 2 clocks is EXPTIME-complete}
$$

并且两人博弈版本达到：

$$
\text{Reachability games on glitch-free RTA are in } 2\mathrm{EXPTIME}
$$

因此这条 family 的真正形状是：一般模型很快不可判，但 glitch-free 子类形成稳定、可分析的 timed-recursive branch。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 除普通 locations 外，还显式支持 box / call / return 结构。 |
| 事件 / 触发 | 强支持 | 既有 timed action，也有递归调用和返回。 |
| 守卫 / 数据 | 支持时钟守卫 | guard / invariant / reset 与普通 `TA` 同源，外加 clock 传参机制。 |
| 层次 | 部分支持 | 不是 Harel 式层次状态图，但有更强的递归组件层次。 |
| 并发 / 同步 | 不支持 | 论文关注单递归控制流，不是 network composition。 |
| 时间约束 | 强支持 | 继承 `TA` 的 dense-time clocks。 |
| 连续动态 / 随机性 | 不支持 | 没有 ODE 或概率。 |
| 可执行 / 可验证性 | 强理论支持 | 一般情形不可判，glitch-free fragment 通过 region abstraction 可分析。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 顶层模型 | `$T=(C,(T_1,\ldots,T_k))$` | 把 timed automata 组织成可递归调用的组件集合。 |
| 组件骨架 | `$T_i=(N_i,En_i,Ex_i,B_i,Y_i,A_i,X_i,P_i,Inv_i,E_i,\rho_i)$` | 显式加入 box、entry/exit 和 by-value/by-reference clock passing。 |
| 配置 | `$(\langle \kappa \rangle,q,\nu)$` | 语义中必须同时保留调用栈和当前时钟值。 |
| glitch-free 条件 | `$\forall b,\ P(b)=C \text{ or } P(b)=\varnothing$` | 一般不可判与可判 fragment 的关键边界。 |
| 负结果 | `3` clocks undecidable / `2`-player `2` clocks undecidable | 说明混合 clock-passing 机制的表达力很强。 |

## 构造方式与承载格式

### 建模入口

建模时需要先决定：

1. 哪些 timed behavior 应拆成独立组件。
2. 调用点是否需要保留 caller 时钟值。
3. 哪些 clocks 适合视为 local，哪些更像 global。
4. 是否能接受 glitch-free 限制，以换取可判定性。

### 机器可处理承载方式

原文的承载方式是组件图、boxes、entry/exit、时钟不变式与 pass-by-value / pass-by-reference 映射，不涉及工程 DSL。

### 交换与互操作

它与以下理论对象最紧密：

1. 普通 `Timed Automata` 母线。
2. recursive state machines / recursive game graphs。
3. timed pushdown / timed software verification 方向的可判定性边界研究。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 component/box/call-return 结构、clock valuations 与 region abstraction。
- 仿真/执行支持：可按 configuration LTS 执行。
- 验证/分析支持：reachability、termination、games、region abstraction、复杂度分类。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 timed automata 理论里与 recursive state machines 交叉的经典模型分支。

## 适用场景与需求前提

### 适用场景

适合那些本质上带有函数调用、子程序复用或递归控制流的 real-time software / timed controller 理论建模问题。

### 需求前提

1. 系统必须既有 dense-time clocks，又有显式 call/return 结构。
2. 需求可以接受组件级划分和调用栈语义。
3. 若想保住可判定性，最好能进一步满足 glitch-free。

### 不适用或高成本场景

若系统只有平面控制流，普通 `Timed Automata` 更简单；若需求含连续动力学，`Hybrid Automata` 更自然；若混合 by-value / by-reference clock passing 不可避免，可判定性会迅速恶化。

## 与相邻形式主义的关系

相对普通 `Timed Automata`，`RTA` 的新增点是递归组件和 clock-passing 机制；相对 pushdown timed system，它更像“在 timed automaton 语法内显式加入 box / entry / exit 的 recursive-state-machine 化”；相对未来可能补入的 `Recursive Hybrid Automata`，它仍然停留在纯 clock-based timed 层面。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Timed Automata` 主干扩展到一个非常稳定的“递归调用 / real-time software”分支，不再只有 event-clock、parametric、priced、game 这类守卫语义子枝。

### 作为目标形式主义还是中间表示

对面向递归控制软件或硬实时子程序验证的需求，它可以直接成为目标形式主义；对一般工业控制流程，则更多是理论参照。

### 对需求到模型生成的启发

如果需求天然描述成“主控制器调用若干带 timeout 的子过程”，那么 LLM 生成 `RTA` 往往比强行把所有控制流摊平成单张 `TA` 更自然。

## 重要的相关工作

1. `Timed Automata` 母线：为其提供 clocks、guard 和 invariant 语义。
2. recursive state machines：为其提供 box / entry / exit / context 语义骨架。
3. pushdown timed systems：共同构成 timed recursion 的可判定性边界背景。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它正式定义并分析了 `Recursive Timed Automata` family，而不是只给某个程序验证案例。
- 它应挂在 `Timed Automata` 主干下，作为递归 / call-return 方向的独立子节点。
- 它不是 DSL、工具或应用论文；核心价值在模型本体、语义和 decidability boundary。
