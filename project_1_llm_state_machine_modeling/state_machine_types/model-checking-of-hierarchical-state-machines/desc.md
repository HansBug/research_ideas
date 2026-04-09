# 层次状态机的模型检验 / Model Checking of Hierarchical State Machines

## 基本信息

- 标题：Model Checking of Hierarchical State Machines
- 中文标题：层次状态机的模型检验
- 作者：Rajeev Alur, Mihalis Yannakakis
- 发表：*Proceedings of the 6th ACM SIGSOFT International Symposium on Foundations of Software Engineering*, pp. 175-188, 1998
- DOI：`10.1145/288195.288305`
- 链接：https://www.cis.upenn.edu/~alur/Fse98.pdf
- 形式主义：`Hierarchical State Machines (HSM) / Hierarchical Kripke Structures`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 保层次判定边界奠基
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 hierarchical Kripke structure 元组、box-expansion 语义、trace language 与 reachability / `LTL` / `CTL` 判定问题。
- 标准/格式获取方式：原文没有 DSL、XML 或交换标准，核心承载方式是 `K = \langle K_1,\ldots,K_n \rangle` 的层次结构定义与其 flat expansion 语义。

## 简报

这篇论文把 `Statecharts` 一类“状态可以展开成另一个状态机”的直觉，收束成了可严格分析的 `Hierarchical Kripke Structure`。它的关键不是又做一个图形语言，而是把“盒子 + 共享子机 + 显式 entry/exit”整理成标准元组，并证明很多分析任务不必先完全 flatten。对当前文库的层次状态机支线来说，它正是 `Statecharts` 之后第一篇足够经典、又足够 formal-language / automata-theory 风格的模型本体节点。

- 形式主义定位：`Statecharts` 的一个语义收束版母节点，用层次 Kripke 结构表达 sequential hierarchical behavior。
- 构造方式简述：系统由若干组件 `K_i` 组成；组件内有普通节点 `N_i`、盒子 `B_i`、唯一入口 `in_i`、若干出口 `O_i`，盒子通过映射 `Y_i` 指向更低层组件。
- 基础设施与场景简述：原文是纯理论工作，但直接建立了 reachability、automata-emptiness、`LTL` 与 `CTL` 模型检验路线，并把“避免 flatten”的层次分析问题固定成稳定母线。

```text
层次反应式需求 -> boxes + entry/exit + shared submachine -> flat expansion / trace semantics -> reachability / temporal-logic checking
```

## 形式主义定义与核心对象

### 定义对象

原文关注的是 sequential hierarchical state machines，也就是“状态本身还能展开成另一个状态机”的有限控制系统，但暂时不引入并发与共享变量。作者用 Kripke structure 作为统一记法，因此模型天然适合接 `LTL/CTL` 语义。

### 核心抽象

普通 flat Kripke structure 写成：

$$
M = (W, in, R, L)
$$

上式中的符号逐项解释如下：

1. `W` 是状态集合。
2. `in \in W` 是初始状态。
3. `R \subseteq W \times W` 是迁移关系。
4. `L : W \to 2^P` 给每个状态打上原子命题标签。

层次版本则写成：

$$
K = \langle K_1,\ldots,K_n \rangle
$$

其中每个组件

$$
K_i = (N_i, B_i, in_i, O_i, X_i, Y_i, E_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 box / supernode 集合。
3. `in_i \in N_i` 是该组件唯一入口。
4. `O_i \subseteq N_i` 是出口节点集合。
5. `X_i : N_i \to 2^P` 是普通节点的命题标注函数。
6. `Y_i : B_i \to \{i+1,\ldots,n\}` 把每个盒子映射到一个更低层组件。
7. `E_i` 是边关系；边可以连普通节点，也可以从“盒子 + 被调组件的某个出口”返回。

### 一个最小例子与通俗解释

论文正文里的经典例子是 digital clock。顶层组件只有 `24` 个小时盒子，每个小时盒子都复用同一个“分钟循环”子机；分钟子机又复用同一个“秒循环”子机。这样：

1. 顶层只关心“当前小时是哪一个大模式”。
2. 小时内部不必重新复制 `60` 分钟结构。
3. 共享子机定义后，可以在多个上下文中复用。

通俗地说，`HSM` 就是“允许把一个状态折叠成一本子流程手册的状态机”。普通 `FSM` 只能把所有状态平铺在一个大图上；`HSM` 则允许说“进入这个大状态后，再按另一台状态机继续跑”，因此既保留了有限状态骨架，又能压缩结构。

### 运行 / 接受 / 转移语义

每个层次组件都可以展开成 ordinary flat structure。若 `K_i` 的 flat expansion 记为 `K_i^F`，则其状态集合递归地由“普通节点 + 盒子上下文中的下层状态”组成。直观写法可压成：

$$
W_i = N_i \cup \{ (b,v) \mid b \in B_i,\ Y_i(b)=j,\ v \in W_j \}
$$

上式中的符号逐项解释如下：

1. `W_i` 是展开后 `K_i^F` 的状态集合。
2. `b` 是当前所处的上层盒子。
3. `v` 是盒子内部被展开组件 `K_j^F` 的一个状态。

因此，flat state 本质上是“若干上下文盒子 + 当前最内层普通节点”的向量。论文明确指出，像 `send` 这样的内层节点可以在不同上下文里出现成不同 flat state，例如 `(try_1, send)` 与 `(try_2, send)`。

对 trace 语义，原文把 flat execution 投影到命题标签后得到：

$$
L(K) = \mathrm{Traces}(K_1^F)
$$

如果再给定 Büchi automaton `A`，则 automata-emptiness 问题就是判定：

$$
L(A) \cap L(K) \neq \varnothing
$$

### 语义边界

这个模型刻意收紧了 `Statecharts` 的一些自由度：

1. 它是 sequential 的，不含并发区。
2. 它没有 shared variables，也没有复杂数据更新。
3. hierarchy 的核心含义是“组件复用 + box expansion”，不是广播事件或跨层任意跳转。
4. 它适合做 trace-based temporal verification，而不是直接做工程 DSL 执行语义。

### 关键性质与判定边界

原文最重要的不是某个单独算法，而是说明“hierarchy 带来指数级 succinctness，但不必一律付出 flatten 的指数成本”。文中给出的代表性结论包括：

$$
\mathrm{Reachability}(K) \in P
$$

且 reachability 对 hierarchical machines 是 `P`-complete。

对线性时序性质，若把规格给成 Büchi automaton `A`，论文给出：

$$
\mathrm{Emptiness}(K,A) \text{ can be solved in time polynomial in } |K| \text{ and } |A|
$$

对 `LTL`，文中进一步写成：

$$
\mathrm{MC}_{LTL}(K,\varphi) = O(|K| \cdot 8^{|\varphi|})
$$

而 `CTL` 的复杂度则与出口数强相关；single-exit 情况仍可做保层次分析，但 multiple-exit 会显著增大难度。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 普通节点 + box / supernode 是核心。 |
| 事件 / 触发 | 弱支持 | 原文主记法是 Kripke transition，不强调显式事件标签。 |
| 守卫 / 数据 | 不支持 | 没有共享变量与复杂数据守卫。 |
| 层次 | 强支持 | hierarchy / reuse / context 是模型本体。 |
| 并发 / 同步 | 不支持 | 明确只研究 sequential hierarchical machines。 |
| 时间约束 | 不支持 | 无 clocks / deadlines。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 直接面向 reachability、`LTL`、`CTL`。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| flat Kripke 结构 | `$M=(W,in,R,L)$` | ordinary baseline。 |
| 层次组件 | `$K_i=(N_i,B_i,in_i,O_i,X_i,Y_i,E_i)$` | HSM 的 canonical component tuple。 |
| flat expansion | `$W_i = N_i \cup \{(b,v)\}$` | box 展开后的上下文状态。 |
| trace language | `$L(K)=\mathrm{Traces}(K_1^F)$` | 层次结构的外显行为。 |
| automata-emptiness | `$L(A)\cap L(K)\neq\varnothing$` | linear-time verification 入口。 |

## 构造方式与承载格式

### 建模入口

1. 先定义顶层组件与初始节点。
2. 再识别哪些状态适合折叠成可复用子机。
3. 为每个子机固定唯一入口和若干出口。
4. 用 `Y_i` 明确 box 指向哪一个下层组件。

### 机器可处理承载方式

机器可处理承载方式不是 XML/DSL，而是：

1. hierarchical component tuple；
2. flat expansion 规则；
3. trace language；
4. temporal-logic / Büchi product construction。

### 交换与互操作

原文没有工程交换格式，但谱系互操作非常强：

1. 往上可接 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md) 作为语义收束版。
2. 往下可自然长出 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md) 与 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)。

## 配套基础设施

- 建模/编辑工具：原文未提供公开工具。
- 解析/交换/元模型支持：核心是 hierarchical tuple 与 flat expansion。
- 仿真/执行支持：可按 expanded Kripke structure 直接执行。
- 验证/分析支持：reachability、automata-emptiness、`LTL`、`CTL` 是主线。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：为后续 `CHSM`、`HRM`、`RSM`、context-dependent family 提供了统一父节点。

## 适用场景与需求前提

### 适用场景

适合：

1. 主要难点在模式层次与复用，而不在并发或数据。
2. 需要对层次结构本身做保层次分析。
3. 希望把 `Statecharts` 风格对象收束成更简单、可判定的理论模型。

### 需求前提

1. 系统核心是有限离散控制。
2. hierarchy 主要表现为“子模式复用”。
3. 可以接受唯一入口、显式出口和无共享变量的骨架。

### 不适用或高成本场景

若需求强依赖并发同步、变量作用域、history、preemption 或递归调用，单纯 `HSM` 就不够，需要转向 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)、[efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md) 或 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)。

## 与相邻形式主义的关系

相对 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)，`HSM` 去掉了大量语义歧义，保留 hierarchy / reuse 骨架；相对普通 `FSM`，它把“状态里再嵌一台状态机”正式化；相对 `CHSM`，它还没有并发 product；相对 `RSM`，它没有 recursion。

## 与本研究的关系

### 对 Project 1 的价值

它把“层次状态机”从图形直觉压成了标准可比较的理论节点，是当前演化树里把 `Statecharts` 接到 automata-theory 支线的最关键桥梁之一。

### 作为目标形式主义还是中间表示

更适合作为谱系母节点和中间表示，而不是工程交付语言。

### 对需求到模型生成的启发

当需求主要呈现“主模式 / 子模式 / 共享子流程复用”特征时，LLM 不应只生成 flat `FSM`，而应优先判断是否该生成 `HSM` 风格骨架。

### 现实限制

它为了保判定性而去掉了很多工程语言常见特性，因此在真实软件工程中通常还要向更丰富但更重的分支扩展。

## 重要的相关工作

### 奠基或前身工作

- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)：层次状态机的图形化源头。

### 同类型或同家族工作

- [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)：在 `HSM` 上加入并发。
- [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)：把 hierarchy 推到 mode / variable / history 语义。
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：把 hierarchy 推到 recursion / call-return。
- [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)：把 proposition labeling 推到 supernodes / contexts。

## 文献分类总结

- 这篇论文属于 `Statecharts -> HSM` 的经典理论收束节点。
- 它不是 DSL、工具或应用案例，而是严格的 `🧩 + 🧱 + 🧮` 模型本体条目。
- 对当前文库最重要的价值，是为 `CHSM / HRM / RSM / context-dependent H/RSM` 提供了稳定父边。
