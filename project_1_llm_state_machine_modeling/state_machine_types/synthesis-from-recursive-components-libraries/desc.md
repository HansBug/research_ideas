# 从递归组件库合成系统 / Synthesis from Recursive-Components Libraries

## 基本信息

- 标题：Synthesis from Recursive-Components Libraries
- 中文标题：从递归组件库合成系统
- 作者：Yoad Lustig、Moshe Vardi
- 发表：*Electronic Proceedings in Theoretical Computer Science*, 54:1-16, 2011
- DOI：`10.4204/EPTCS.54.1`
- 链接：https://doi.org/10.4204/EPTCS.54.1
- 形式主义：`Recursive Library Components (RLC) / Recursive-Component Libraries`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / call-return component-library branch
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `RLC` tuple、interface function、composition tree、nested-word Buchi automata 与树自动机化简。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 recursive library component tuple、call / return / re-entry interfaces 与 composition tree。

## 简报

这篇论文正是把上一条 `component libraries` 从 flat control-flow 推到 call-return 版本的那一步。作者明确说研究对象是“带 call and return 控制结构的 component library”，并直接把新组件命名为 `Recursive Library Component (RLC)`。对当前演化树来说，这篇文献的重要性不在 NWTL synthesis 算法，而在它终于给“递归组件库”这个 family 写出了清楚的 tuple、call state、return state、re-entry state 与 composition-tree semantics。

- 形式主义定位：`Component Libraries` 的递归化 / call-return 化扩展。
- 构造方式简述：每个 component 是带初始、call、return、re-entry 四类接口状态的 transducer；组合时通过接口函数把 call states 接到被调组件，把 return states 接回调用者的 re-entry states。
- 基础设施与场景简述：纯理论条目，但它把 recursive-component composition 变成了树结构对象，直接连到 nested words / `NWBA`。

```text
control-flow component library -> call / return / re-entry interfaces -> recursive library component -> composition tree -> nested-word specification
```

## 形式主义定义与核心对象

### 定义对象

相对上一代 flat component-library model，这里新增的核心是：

1. call states；
2. return states；
3. re-entry states；
4. 由此诱导出的 call stack / composition tree。

因此它不再只是“final-state 交接控制权”，而是真正开始接近 `RSM` 风格的 call-return interface。

### 核心抽象

原文把单个递归组件写成：

$$
M=\langle \Sigma_I,\Sigma_O,S,s_0,s_e^R,S_C,S_R,\delta,L \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma_I,\Sigma_O` 是输入和输出字母表。
2. `S` 是状态集合。
3. `s_0` 是被调用时进入的初始状态。
4. `s_e^R` 是 re-entry states 集合，表示子调用返回后从哪里继续。
5. `S_C` 是 call states 集合。
6. `S_R` 是 return states 集合。
7. `\delta:S\times\Sigma_I\to S` 是内部转移函数。
8. `L:S\to\Sigma_O` 是输出标签。

组合对象写成有限元组：

$$
\langle (1,C_1,f_1),\ldots,(k,C_k,f_k)\rangle
$$

其中 `f_i:S_C\to [k]` 指定某个 component 的每个 call state 应该调用哪一个 composition element。

### 一个最小例子与通俗解释

可以把它想成“一个在线商店组件调用支付组件，再返回商店组件”的状态机化版本：

1. 商店组件在某个 call state 进入支付组件。
2. 支付组件运行一段时间后到达某个 return state。
3. 返回值编号决定调用者从哪个 re-entry state 继续。

通俗地说，`RLC` 就像“每个库组件都长出一组 call/return 插槽的状态机函数块”。这已经非常接近程序里的过程调用，也比上一代 final-state hand-off 模型更像 `RSM`。

### 运行 / 接受 / 转移语义

原文把整个组合诱导成一个可能无限的 transducer `M`。其状态形状为：

$$
\langle i_1,\ldots,i_m,s\rangle
$$

上式中的符号逐项解释如下：

1. `i_1,\ldots,i_m` 是当前调用栈上的 composition-element 索引。
2. `s` 是当前最内层 component 的局部状态。

三类转移语义分别是：

1. internal transition：留在当前 component 内部；
2. call transition：把被调 element 压入上下文并跳到其 `s_0`；
3. return transition：弹出一层上下文并跳到调用者对应的 re-entry state。

若当前在第 `j` 个 call state，则调用步可以写成：

$$
\langle i_1,\ldots,i_m,s\rangle \to \langle i_1,\ldots,i_m,f_{i_m}(j),s_0[f_{i_m}(j)]\rangle
$$

若当前在第 `j` 个 return state，则返回步为：

$$
\langle i_1,\ldots,i_m,s\rangle \to \langle i_1,\ldots,i_{m-1},s_e^j[i_{m-1}]\rangle
$$

这就是 `RLC` family 的本体语义。

### 语义边界

这篇文献的 family boundary 很清楚：

1. 它仍是 transducer component family，不是一般 pushdown 程序语言。
2. 相对 `Component Libraries`，新增的是 call-return stack，而不是并发或数据流。
3. 规格语言从 `LTL` 升到 `NWTL`，原因正是对象本身已经带 nested-word 结构。

### 关键性质与判定边界

对当前文库最关键的结论不是复杂度数值，而是它把对象和规格一起稳定化了：

$$
\text{recursive component library} + \text{NWTL} \Rightarrow 2\mathrm{EXPTIME}\text{-complete}
$$

更重要的是，它引入了 composition tree 这一持久可挂树对象，使 recursive-component family 有了稳定命名，而不再只是“带调用的组件 synthesis”。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 组件仍是 transducer 状态机。 |
| 事件 / 触发 | 支持 | 输入字母驱动局部迁移。 |
| 守卫 / 数据 | 不支持 | 无额外变量。 |
| 层次 | 强支持 | 调用栈与 composition tree 形成递归层次。 |
| 并发 / 同步 | 不支持 | 单控制流。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 组合诱导 transducer、nested-word 规格与 tree-automata reduction 完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单组件 | `$M=\langle \Sigma_I,\Sigma_O,S,s_0,s_e^R,S_C,S_R,\delta,L \rangle$` | `RLC` 的 canonical tuple。 |
| 组合对象 | `$\langle (1,C_1,f_1),\ldots,(k,C_k,f_k)\rangle$` | recursive-component library composition。 |
| 全局状态 | `$\langle i_1,\ldots,i_m,s\rangle$` | 调用栈 + 局部状态。 |
| call step | `$\langle i_1,\ldots,i_m,s\rangle \to \langle i_1,\ldots,i_m,f_{i_m}(j),s_0[f_{i_m}(j)]\rangle$` | 调用被调组件。 |
| return step | `$\langle i_1,\ldots,i_m,s\rangle \to \langle i_1,\ldots,i_{m-1},s_e^j[i_{m-1}]\rangle$` | 按返回编号接回调用者。 |

## 构造方式与承载格式

### 建模入口

1. 先定义若干 `RLC` 组件。
2. 为每个组件固定 call / return / re-entry 接口。
3. 用接口函数把每个 call state 连到某个 composition element。
4. 再把整个组合表示成 composition tree。

### 机器可处理承载方式

机器可处理承载方式主要是：

1. `RLC` tuple；
2. composition element tuple；
3. global transducer semantics；
4. composition tree；
5. `NWBA` / tree automata constructions。

### 交换与互操作

它与当前文库中的关系如下：

1. 直接承接 [synthesis-from-component-libraries/desc.md](../synthesis-from-component-libraries/desc.md) 的 control-flow component-library branch。
2. 在 call-return 结构上与 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 和 [model-checking-of-unrestricted-hierarchical-state-machines/desc.md](../model-checking-of-unrestricted-hierarchical-state-machines/desc.md) 同宗。
3. 规格侧又和 [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md) 的 nested-word family 正面接上。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `RLC` tuple 与 composition tree。
- 仿真/执行支持：组合诱导出的 `M` 给出可执行 transducer semantics。
- 验证/分析支持：`NWBA`、composition tree、tree automata emptiness。
- 代码生成/转换支持：原文未给工程生成流程。
- 标准化或社区生态：研究型 family，主要价值在把 recursive component libraries 稳定成可引用的 formalism。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要从可复用组件库中合成带过程调用结构的系统时。
2. 关心 call-return computation 的 local / nested specifications 时。
3. 需要把 library synthesis 接到 `RSM` 支线上时。

### 需求前提

1. 控制流是单线程式、过程调用式的。
2. 调用与返回接口可用有限个 call / return / re-entry slots 表达。
3. 组件库规模有限，但组合深度可无界。

### 不适用或高成本场景

如果系统本质是 bounded hierarchy 而非无界 call-return，更适合转向 hierarchical systems from a library；如果需要开放环境 pruning 语义，则应转向 open modules / module checking 支线。

## 与相邻形式主义的关系

相对 `Component Libraries`，它把 final-state hand-off 推成了真正的 call-return；相对 `RSM`，它的组件更像 transducer library element 而不是程序分析中的 procedure module；相对 hierarchical systems from a library，它允许无界递归，而后者强调 bounded hierarchy。

## 与本研究的关系

对 `project_1` 来说，这篇论文很重要，因为它说明“自底向上拼接可复用组件”完全可以落成一个严肃的 call-return 状态机 family，而不是只停留在 synthesis 方法词汇。若后续希望让 LLM 生成的中间表示具备“组件可复用 + 调用可追踪”的性质，这条线很值得保留。

## 重要的相关工作

1. [synthesis-from-component-libraries/desc.md](../synthesis-from-component-libraries/desc.md)：flat control-flow precursor。
2. [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：程序分析视角下的 `RSM` 母线。
3. [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)：规格与语义对象侧的 nested-word family。

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为核心对象是递归组件状态机。
- 这是一篇 `🧱 模型本体` 文献，因为可入库的是 `RLC` family 本身，而不是 NWTL synthesis 算法。
- 它主要描述 `🤝 接口 / 交互契约`，因为 call / return / re-entry interface 是本体核心。
- 它属于 `🧮 形式语言与自动机理论`，因为全文都在 automata / tree-automata / nested-word 框架里定义和分析 family。
