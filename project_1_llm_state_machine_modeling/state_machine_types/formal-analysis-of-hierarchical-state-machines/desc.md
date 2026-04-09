# 层次状态机的形式化分析 / Formal Analysis of Hierarchical State Machines

## 基本信息

- 标题：Formal Analysis of Hierarchical State Machines
- 中文标题：层次状态机的形式化分析
- 作者：Rajeev Alur
- 发表：*Verification: Theory and Practice*, pp. 42-66, 2003
- DOI：`10.1007/978-3-540-39910-0_3`
- 链接：https://doi.org/10.1007/978-3-540-39910-0_3
- 形式主义：`Hierarchical State Machines (HSM) / Hierarchical Kripke Structures`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论综述 / 分支梳理
- 工具/实现获取方式：原文未提供公开工具；机器可处理入口是 `K=(K_1,\ldots,K_n)` 层次模块元组、expansion `K_i^F`、reachability / cycle detection、hierarchical automata、hierarchical Kripke structures 与 `LTL/CTL` model checking 任务。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是模块化 `HSM` / Kripke 结构定义、box-expansion 语义与 automata-theoretic / symbolic analysis 框架。

## 简报

这篇 chapter 的价值，不是提出一个全新节点，而是把 `HSM` 这条支线内部已经出现的几个关键方向一次性整理成了统一视角：先从 module-based `HSM` / hierarchical Kripke structure 出发，再讨论 reachability、cycle detection、language-theoretic 复杂度、`LTL/CTL` 验证，最后把带变量的 symbolic route、`HRM` 风格 richer hierarchy 以及 `RSM` 这条递归外延都纳入同一叙事框架。对当前文库来说，它非常适合用来校准“层次状态机族演化树”里父子关系的文字说明。

- 形式主义定位：`HSM` 主枝的 formal-analysis 总览条目，用来系统说明 sequential hierarchy 的定义、分析边界与后续外延。
- 构造方式简述：以 `K=(K_1,\ldots,K_n)` 的模块集合为核心；模块里有 nodes、boxes、entry/exit、indexing function 与 edge relation；通过 expansion 得到 flat state machine。
- 基础设施与场景简述：纯理论条目，但直接串起 `HSM`、hierarchical automata、hierarchical Kripke structures、`RSM` 与 symbolic hierarchy 这些分支。

```text
hierarchical module family -> expansion / flat semantics -> reachability / cycle / LTL / CTL -> variables / HRM / RSM 外延
```

## 形式主义定义与核心对象

### 定义对象

原文把 `HSM` 固定成一个由多个 module 组成的层次系统。每个 module 有显式 entry / exit 接口，box 通过索引函数指向更低层 module；这使得 hierarchy 不再只是图形直觉，而是可直接接分析算法的正式对象。

### 核心抽象

原文给出的总元组是：

$$
K = (K_1,\ldots,K_n)
$$

其中每个 module

$$
K_i = (N_i,B_i,I_i,O_i,Y_i,E_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集合。
2. `B_i` 是 boxes 集合。
3. `I_i \subseteq N_i` 是 entry nodes。
4. `O_i \subseteq N_i` 是 exit nodes。
5. `Y_i : B_i \to \{i+1,\ldots,n\}` 指定每个 box 引用哪个更低层 module。
6. `E_i` 是边关系，边可以从普通节点或 return 指向普通节点或 call。

若把 hierarchy 展开，原文将第 `i` 个 module 的 expansion 写作 `K_i^F`。其状态集保守压成：

$$
W_i \subseteq \Bigl(\bigcup_{j>i} B_j\Bigr)^* \Bigl(\bigcup_{j\ge i} N_j\Bigr)
$$

上式中的符号逐项解释如下：

1. `W_i` 是 `K_i^F` 的 flat states 集合。
2. 前面的 `B^*` 部分是上下文链，也就是从外层传下来的若干 boxes。
3. 最后一个节点成分表示当前所处的最内层普通节点。

### 一个最小例子与通俗解释

原文继续使用 digital clock 作为最自然的解释：

1. 顶层 module 用 `24` 个 hour-box 表示“当前小时”。
2. 每个 hour-box 指向同一个 minute module。
3. minute module 中每个 minute-box 又指向同一个 second module。

通俗地说，这就是“把一张巨大的平铺状态图折成三层抽屉柜”：第一层抽屉装小时，第二层装分钟，第三层装秒；真正运行时的 flat state 不是一个单节点，而是“当前在哪个抽屉里 + 抽屉内部的哪个节点”。

### 运行 / 接受 / 转移语义

原文把每个 module 的 flat expansion 递归定义出来。若 `b` 是某个引用 `K_j` 的 box，则 `K_j^F` 的状态会在外层上下文 `b` 中出现。因此可以把 flat state 理解成：

$$
b \cdot v
$$

这里的符号逐项解释如下：

1. `b` 是当前外层 box 上下文。
2. `v` 是被调下层 module 展开后的一个状态。
3. 连接记号 `\cdot` 表示“在 box `b` 的上下文里看到状态 `v`”。

对 top-level module，整个层次结构的平铺语义就是：

$$
K^F = K_n^F
$$

若把 hierarchy 看成 Kripke 结构，则 trace language 写成：

$$
L(K) = \mathrm{Traces}(K^F)
$$

### 语义边界

原文同时强调了几个边界：

1. 当前章节主线是 non-recursive hierarchy；如果去掉调用依赖的 acyclic 限制，就会得到 `RSM`。
2. `HSM` 可以看成“栈深预先有界的 pushdown system”。
3. hierarchy 自身并不引入变量；但 variables 一旦加入，就会进入 symbolic hierarchy / `HRM` 风格外延。
4. 这里主要研究 sequential hierarchy，不处理 `CHSM` 的并发 product。

### 关键性质与判定边界

原文把若干重要分析结果集中整理为：

$$
\mathrm{Reachability}(K,T) \text{ is PTIME-complete}
$$

并给出多入口情况下的时间界：

$$
O(|K| \cdot k^2)
$$

这里的 `k` 是每个 module 的 entry / exit 接口规模上界。

对 cycle detection，原文给出与 reachability 同级别的复杂度量级；对 `LTL`：

$$
\mathrm{MC}_{LTL}(K,\varphi) = O(k^2 \cdot |K| \cdot 8^{|\varphi|})
$$

对 `CTL`：

$$
\mathrm{MC}_{CTL}(K,\varphi) = O(k^2 \cdot |K| \cdot 2^{4|\varphi|})
$$

而在 single-exit 情况下，原文进一步指出 `CTL` 的结构复杂度是 `PSPACE`-complete，这正是层次状态机主枝和后续 `RSM` / pushdown 线衔接前的一个关键边界。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | nodes + boxes + entry/exit 是核心。 |
| 事件 / 触发 | 支持 | 通过 edge relation 与 Kripke transitions 表达。 |
| 守卫 / 数据 | 部分支持 | 当前主体先不加变量，但专门讨论了变量扩展方向。 |
| 层次 | 强支持 | 整篇围绕 hierarchy 本身展开。 |
| 并发 / 同步 | 不支持 | 本文主线不讨论 `CHSM` 并发积。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、cycle、emptiness、`LTL/CTL` 都有系统整理。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$K=(K_1,\ldots,K_n)$` | 层次系统由若干 module 组成。 |
| 模块元组 | `$K_i=(N_i,B_i,I_i,O_i,Y_i,E_i)$` | `HSM` 的 canonical module definition。 |
| flat state | `$W_i \subseteq B^*N$` | expansion 后的状态由上下文链和当前节点组成。 |
| reachability | `$\mathrm{Reachability}(K,T)$` | hierarchy-preserving 基本分析问题。 |
| `HSM` 与 pushdown 关系 | `$\text{HSM} \subset$ bounded-stack pushdown-style systems` | 指出 `RSM` 将是自然外延。 |

## 构造方式与承载格式

### 建模入口

1. 先把系统划成若干 modules。
2. 为每个 module 固定 entry / exit 接口。
3. 再用 boxes 指向更低层 modules。
4. 最后通过 expansion 得到统一 flat semantics。

### 机器可处理承载方式

文中默认的机器可处理载体是：

1. module tuple；
2. call / return 风格 box 接口；
3. flat expansion `K_i^F`；
4. temporal-logic 与 Büchi-product 分析。

### 交换与互操作

原文没有独立交换格式，但对谱系整理非常有用：

1. 往前承接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)。
2. 往后解释 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 为什么会自然出现。
3. 还专门把 [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md) 这类带变量 / richer hierarchy 的路线纳入讨论。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 module tuple 与 expansion semantics。
- 仿真/执行支持：可通过 flat expansion 解释。
- 验证/分析支持：reachability、cycle detection、language problems、`LTL/CTL`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于理论总览条目，主要作用是给家族边界定口径。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要系统理解 `HSM` 家族有哪些稳定分支与分析任务。
2. 需要在演化树中澄清 `HSM -> RSM / HRM` 这些后继的来路。
3. 需要一个比较权威的层次状态机 formal-analysis 总览条目。

### 需求前提

1. 研究重点是 hierarchy，而不是 DSL 外观。
2. 系统控制骨架可用 module + box + entry/exit 表达。
3. 关心的问题是可达性、时序逻辑与判定边界。

### 不适用或高成本场景

如果需求已经转向工程语言标准、交换格式或应用案例，这篇文献就不够直接；它更适合作为演化树说明性文献，而不是工程落地文献。

## 与相邻形式主义的关系

相对 [hierarchical-state-machines/desc.md](../hierarchical-state-machines/desc.md)，这篇更偏 formal-analysis 综述而不是表达力总览；相对 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)，它把 non-recursive hierarchy 明确界定为 bounded-stack 版本；相对 `HRM`，它说明 richer hierarchy 往变量 / symbolic 路线扩展后会发生什么。

## 与本研究的关系

### 对 Project 1 的价值

它能显著提升当前“状态机族演化树”的可解释性，因为它把 `HSM` 主枝上的 formal-analysis 母线、`RSM` 递归外延以及 variables / `HRM` 方向全放进一个统一语境。

### 作为目标形式主义还是中间表示

更适合作为谱系校准和理论说明，而不是单独的目标形式主义。

### 对需求到模型生成的启发

当 LLM 需要判断“某段需求应该落到普通层次状态机，还是已经需要 richer hierarchy / recursion”时，这篇文献提供了非常清楚的分界线。

### 现实限制

它本身并不提供公开工具，也不是新模型提出条目；主要价值在于梳理和校准。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [hierarchical-state-machines/desc.md](../hierarchical-state-machines/desc.md)

### 同类型或同家族工作

- [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)
- [model-checking-of-unrestricted-hierarchical-state-machines/desc.md](../model-checking-of-unrestricted-hierarchical-state-machines/desc.md)

## 文献分类总结

- 这篇文献是 `HSM` 主枝的 formal-analysis 汇总条目，虽然偏综述，但仍然围绕单一层次状态机家族本体展开。
- 它对当前文库最大的价值不是“新增一个树节点”，而是把既有 `HSM` 支线的挂接依据和分叉逻辑说得更稳。
- 因此它适合作为 `🧱` 模型本体条目正式入账，并在演化树说明里充当 `HSM` 主枝的理论整理代表。
