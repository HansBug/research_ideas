# 层次状态机的模型检验（TOPLAS 全文版） / Model Checking of Hierarchical State Machines

## 基本信息

- 标题：Model Checking of Hierarchical State Machines
- 中文标题：层次状态机的模型检验（TOPLAS 全文版）
- 作者：Rajeev Alur, Mihalis Yannakakis
- 发表：*ACM Transactions on Programming Languages and Systems*, 23(3):273-303, 2001
- DOI：`10.1145/503502.503503`
- 链接：https://www.cis.upenn.edu/~alur/Fse98.pdf
- 形式主义：`Hierarchical State Machines (HSM) / Hierarchical Kripke Structures`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / `HSM` 语义与复杂度边界稳定条目
- 工具/实现获取方式：原文未提供公开工程实现；机器可处理入口是 hierarchical Kripke structure 元组、flat expansion 语义、trace language 与 `LTL/CTL` 判定问题。
- 标准/格式获取方式：原文没有 DSL、XML 或交换标准，核心承载方式是 `K=\langle K_1,\ldots,K_n\rangle` 的层次组件定义、box expansion 规则和时序逻辑检验问题。

## 简报

这篇 `TOPLAS` 全文版的价值，不是再提出一个新家族，而是把 1998 年 `FSE` 会议版的 `HSM` 母节点彻底稳定下来：它把 hierarchical Kripke structure 的定义、flat expansion、reachability、automata-emptiness、`LTL` 和 `CTL` 复杂度统一整理成 journal 级版本，成为后续 `CHSM / HRM / uHSM / RSM` 等层次状态机理论分支最稳的共同挂接依据之一。

- 形式主义定位：`Statecharts` 在 formal-language / automata-theory 语境下的一个精炼母节点，也是 `HSM` 支线最稳定的 journal 依据。
- 构造方式简述：系统由多层组件 `K_i` 组成，组件里有普通节点、boxes、唯一入口和若干出口；box 通过映射 `Y_i` 指向下层组件。
- 基础设施与场景简述：原文是纯理论工作，但直接固定了保层次 reachability、automata-theoretic `LTL` 与 branching-time `CTL` 分析路线，因此它比 conference 版更适合作为演化树中的长期锚点。

```text
hierarchical reactive requirement -> boxes + entry/exit + shared submachine -> flat Kripke expansion -> reachability / LTL / CTL checking
```

## 形式主义定义与核心对象

### 定义对象

原文研究的是 sequential hierarchical state machines，也就是允许“一个状态内部再展开成另一台有限状态机”的层次有限控制模型。它刻意不引入并发、共享变量和复杂数据操作，而是把层次复用本身压成一个可做模型检查的语义核心。

### 核心抽象

普通 Kripke 结构写成：

$$
M = (W, in, R, L)
$$

上式中的符号逐项解释如下：

1. `W` 是状态集合。
2. `in \in W` 是初始状态。
3. `R \subseteq W \times W` 是迁移关系。
4. `L:W \to 2^P` 给每个状态分配原子命题标签。

层次版本写成：

$$
K = \langle K_1,\ldots,K_n\rangle
$$

其中每个组件满足：

$$
K_i = (N_i,B_i,in_i,O_i,X_i,Y_i,E_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 boxes / supernodes 集合。
3. `in_i \in N_i` 是该组件唯一入口。
4. `O_i \subseteq N_i` 是出口节点集合。
5. `X_i:N_i\to 2^P` 是节点标签函数。
6. `Y_i:B_i\to \{i+1,\ldots,n\}` 指出每个 box 展开到哪个下层组件。
7. `E_i` 是局部边关系，既允许普通边，也允许从 box 返回的边。

### 一个最小例子与通俗解释

一个最小例子就是论文中反复使用的 digital clock 直觉：

1. 顶层是 `24` 个“小时”大状态。
2. 每个小时状态内部复用同一个“分钟循环”子机。
3. 分钟状态内部再复用同一个“秒循环”子机。

通俗地说，`HSM` 就像“状态里还能折叠一本子流程手册的状态机”。普通 `FSM` 只能把所有状态平铺出来；`HSM` 则允许把一部分状态压成一个可复用的子机器，因此结构会更紧凑，也更接近真实层次需求。

### 运行 / 接受 / 转移语义

原文把每个层次组件都展开成一个 flat Kripke 结构。若 `K_i` 的 flat expansion 记作 `K_i^F`，其状态集合递归地满足：

$$
W_i = N_i \cup \{(b,v)\mid b\in B_i,\ Y_i(b)=j,\ v\in W_j\}
$$

上式中的符号逐项解释如下：

1. `W_i` 是组件 `K_i` 展平后的状态集合。
2. `b` 表示当前所处的上层 box。
3. `v` 是被调下层组件展开后的一个状态。

因此 flat state 本质上是“上下文 boxes 序列 + 当前最内层节点”。原文进一步把系统行为写成 trace language：

$$
L(K) = \mathrm{Traces}(K_1^F)
$$

若给定一个 Büchi automaton `A`，则线性时序检验可以压成：

$$
L(A)\cap L(K)\neq \varnothing
$$

### 语义边界

这个 `HSM` 母模型的边界很明确：

1. 它是 sequential hierarchy，不含并发区。
2. 它没有共享变量，也没有复杂 guard/update。
3. 它的 hierarchy 主要表达“组件复用 + box expansion”，而不是工程 DSL 里那种带广播、history、优先级的大语义包。
4. 它适合做 trace-based 与 branching-time verification，不是工程交付语言。

### 关键性质与判定边界

原文最关键的结论，是 hierarchy 带来了指数级 succinctness，但很多问题不必先完全 flatten。可达性满足：

$$
\mathrm{Reachability}(K)\in P
$$

并且是 `P`-complete。对 `LTL`，原文给出可压成：

$$
\mathrm{MC}_{LTL}(K,\varphi)=O(|K|\cdot 8^{|\varphi|})
$$

而 `CTL` 的复杂度则显著依赖出口数；single-exit 情况仍可高效处理，multiple-exit 情形会明显变难。这正是后续 `uHSM / RSM / context-dependent hierarchy` 继续扩张时必须显式处理的接口宽度问题。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 普通节点与 box 是模型本体。 |
| 事件 / 触发 | 弱支持 | 原文主记法更接近 Kripke transition，而不是显式事件 DSL。 |
| 守卫 / 数据 | 不支持 | 不引入共享变量和复杂数据。 |
| 层次 | 强支持 | hierarchy / reuse / context 是整个模型的核心。 |
| 并发 / 同步 | 不支持 | 明确只研究 sequential hierarchical machines。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、`LTL`、`CTL` 直接建立在模型本体上。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| flat baseline | `$M=(W,in,R,L)$` | ordinary Kripke 结构基线。 |
| component tuple | `$K_i=(N_i,B_i,in_i,O_i,X_i,Y_i,E_i)$` | `HSM` 的 canonical 局部元组。 |
| flat expansion | `$W_i=N_i\cup\{(b,v)\}$` | box 展开后的上下文状态。 |
| trace language | `$L(K)=\mathrm{Traces}(K_1^F)$` | 层次结构的外显行为。 |
| automata-theoretic check | `$L(A)\cap L(K)\neq\varnothing$` | linear-time 检验入口。 |

## 构造方式与承载格式

### 建模入口

1. 先识别顶层主模式。
2. 再把可复用的子模式折叠成 boxes。
3. 给每个子模式固定唯一入口和有限出口。
4. 用 `Y_i` 把 box 映射到被复用的组件。

### 机器可处理承载方式

机器可处理承载方式不是 DSL 文件，而是：

1. component tuple；
2. flat expansion 规则；
3. trace language；
4. Büchi / temporal-logic product construction。

### 交换与互操作

它与当前文库里的互操作关系非常直接：

1. 向上承接 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md) 的图形直觉。
2. 向下稳定 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)、[hierarchical-state-machines/desc.md](../hierarchical-state-machines/desc.md)、[analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 等理论分支。

## 配套基础设施

- 建模/编辑工具：原文未提供公开工具。
- 解析/交换/元模型支持：核心是 hierarchical tuple 与 flat expansion 规则。
- 仿真/执行支持：可按 expanded Kripke structure 直接运行。
- 验证/分析支持：reachability、automata-emptiness、`LTL`、`CTL`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：作为 `HSM` 母节点，对后续层次状态机理论支线的生态意义很强，但并非工程标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 需求的主要复杂度来自层次分解和子机复用。
2. 希望对 hierarchy 本身做保层次分析，而不是盲目 flatten。
3. 需要给 `Statecharts` 找到一个更稳的理论落点。

### 需求前提

1. 系统本质仍是有限离散控制。
2. hierarchy 主要表现为模式复用与结构压缩。
3. 可以接受单入口、显式出口和无共享变量的骨架。

### 不适用或高成本场景

如果需求强依赖并发同步、history、作用域变量、开放环境接口或递归调用，那么单纯 `HSM` 不够，需要转向 `CHSM / HRM / uHSM / RSM` 等后继分支。

## 与相邻形式主义的关系

相对 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)，这篇 `TOPLAS` 版不新开节点，而是把 `HSM` 的定义、复杂度和挂接边界系统稳定下来；相对 `CHSM`，它没有并发 product；相对 `RSM`，它还没有 call-return recursion；相对 `HRM`，它也没有 variables、history 和 mode interface。

## 与本研究的关系

### 对 Project 1 的价值

它是当前文库里把 `Statecharts -> HSM` 这条 formal branch 稳定成 journal 级依据的关键条目，适合直接回写到状态机族演化树的主蓝本说明里。

### 作为目标形式主义还是中间表示

更适合作为层次状态机理论母节点与中间表示，而不是工业团队直接维护的交付语言。

### 对需求到模型生成的启发

当需求文本已经明显表现出“主模式 / 子模式 / 共享子流程”结构时，LLM 不应急于把它 flatten 成普通 `FSM`；先识别 `HSM` 骨架，往往更贴近真实结构。

## 重要的相关工作

### 奠基或直接相邻条目

1. [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)：1998 会议版 origin。
2. [hierarchical-state-machines/desc.md](../hierarchical-state-machines/desc.md)：`HSM` 家族综述型整理条目。
3. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：把 `HSM` 继续推进到递归支线。

### 同家族后继条目

1. [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)
2. [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)
3. [model-checking-of-unrestricted-hierarchical-state-machines/desc.md](../model-checking-of-unrestricted-hierarchical-state-machines/desc.md)

## 文献分类总结

- 这篇论文属于 `🧩 经典离散状态机`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🎛️ 控制 / 反应式逻辑`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它不建议在演化树里单独新开一个 `HSM` 子节点，而应作为 `Statecharts -> HSM` 这条主枝的 journal full-version 代表条目回写，把 `HSM` 节点的年份稳定成 `1998 / 2001`。
