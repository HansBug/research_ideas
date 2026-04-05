# 从组件库合成系统 / Synthesis from Component Libraries

## 基本信息

- 标题：Synthesis from Component Libraries
- 中文标题：从组件库合成系统
- 作者：Yoad Lustig、Moshe Y. Vardi
- 发表：*Foundations of Software Science and Computational Structures*, pp. 395-409, 2009
- DOI：`10.1007/978-3-642-00596-1_28`
- 链接：https://doi.org/10.1007/978-3-642-00596-1_28
- 形式主义：`Control-Flow Component Libraries / Component-Library Transducers`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / component-library control-flow branch
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 control-flow component transducer、interface function、composition transducer、composition tree 与 parity tree automata reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 transducer component tuple、control-flow composition `C=\langle [n_F],L,[m],i_0,\rho,\emptyset,L_C\rangle` 与 connectivity / composition tree。

## 简报

这篇论文表面上谈的是 synthesis，但能进演化树的原因并不是算法，而是它把“由可复用组件组成系统”正式压成了一个 control-flow component family。作者明确区分了 data-flow composition 与 control-flow composition，并指出只有后者适合组件像函数一样交接控制权。对当前文库来说，这正好提供了一个位于 `HSM/RSM` 旁边、但更偏 library-composition 的 precursor：后面的 recursive-component libraries 和 hierarchical systems from a library 都是从这里长出来的。

- 形式主义定位：component-library line 的起点，特别是其中的 control-flow composition branch。
- 构造方式简述：每个 component 是有 final states 的 transducer；系统组合由一个更高层的 composition transducer 决定“某个 final state 之后把控制权交给谁”。
- 基础设施与场景简述：纯理论条目，但提出了 regular composition tree 这一机器可处理承载方式，是后续 recursive / hierarchical library synthesis 的直接前件。

```text
component transducer -> final-state interface -> control hand-off function -> composition transducer -> regular composition tree
```

## 形式主义定义与核心对象

### 定义对象

原文先把“组件库合成”拆成两类：

1. data-flow composition；
2. control-flow composition。

真正属于当前层次状态机支线的是第二类，因为它把系统看成“某一时刻只有一个 component 在控制”，而不是同时连线传数据。

### 核心抽象

单个 control-flow component 被写成普通 transducer：

$$
M=\langle \Sigma_I,\Sigma_O,Q,q_0,\delta,F,L \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma_I,\Sigma_O` 是输入和输出字母表。
2. `Q` 是状态集合。
3. `q_0` 是初始状态。
4. `\delta` 是转移函数。
5. `F` 是 final states，表示该 component relinquish control 的出口。
6. `L` 是输出标注函数。

真正的新 family 在于组合对象：

$$
C=\langle [n_F],L,[m],i_0,\rho,\emptyset,L_C \rangle
$$

上式中的符号逐项解释如下：

1. `[n_F]` 是 final-state index alphabet。
2. `L` 是底层 component library。
3. `[m]` 是“interfaced components”的索引集。
4. `i_0` 是起始被激活的 interfaced component。
5. `\rho:[m]\times[n_F]\to[m]` 决定某个组件从某个 final state 退出后，控制权交给谁。
6. `L_C:[m]\to L` 指出每个 interfaced component 实际实例化的是库中的哪个 component。

### 一个最小例子与通俗解释

把它想成“一个由现成函数块拼起来的调度机”：

1. 当前控制块 `C_a` 持有控制权并持续和环境交互。
2. 一旦它进入第 `j` 个 final state，组合器 `\rho(i,j)` 决定切到哪个下一个组件实例。
3. 新组件总是从自己的初始状态开始。

通俗地说，这个 formalism 像“把函数库当状态机模块库，然后再用一张上层切换图来决定退出后接谁”。它还没有 call-return 栈，但已经有清晰的组件接口与控制交接语义。

### 运行 / 接受 / 转移语义

原文把组合后的系统仍看成一个 transducer：

$$
C_L=\langle \Sigma_I,\Sigma_O,Q_{CL},q_0^{CL},\delta_{CL},\emptyset,L_{CL} \rangle
$$

其中状态空间来自 component 状态与 interfaced-component 索引的笛卡尔积：

$$
Q_{CL}=\bigcup_{i\in[m]} Q(i)\times\{i\}
$$

若当前组件 `i` 内部还没到 final state，则系统在本组件内推进；若到达第 `j` 个 final state，则切换规则为：

$$
\delta_{CL}(\langle q,i\rangle,\sigma)=\langle q_0(\rho(i,j)),\rho(i,j)\rangle
$$

这条式子表达的正是 control-flow component libraries 的本体语义：组件不是并行拼接，而是按 final-state interface 一段段移交控制权。

### 语义边界

这篇论文自己就把边界说得很清楚：

1. data-flow composition 会导致 synthesis 不可判定。
2. control-flow composition 才是当前可判定、可树化处理的分支。
3. 作者还明确写到 “call and return” 的 richer control-flow model 属于未来工作，这正是后续 recursive-component libraries 的入口。

### 关键性质与判定边界

对当前文库最重要的不是复杂度数字本身，而是这条 family boundary：

$$
\text{data-flow composition} \Rightarrow \text{undecidable}
$$

而

$$
\text{control-flow composition} \Rightarrow 2\mathrm{EXPTIME}\text{-complete}
$$

这说明“组件库”不是一个泛概念，只有控制交接式 composition 才能稳定成长为后续的 recursive / hierarchical 支线。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 组件本体就是 transducer。 |
| 事件 / 触发 | 支持 | 通过输入字母驱动组件内部迁移。 |
| 守卫 / 数据 | 不支持 | 论文不引入额外变量。 |
| 层次 | 弱支持 | 尚未有 call-return hierarchy，但已有 component-level composition。 |
| 并发 / 同步 | 不支持 | 每个时刻只有一个 component 在控制。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | regular composition tree 与 automata-theoretic synthesis pipeline 完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单组件 | `$M=\langle \Sigma_I,\Sigma_O,Q,q_0,\delta,F,L \rangle$` | control-flow component transducer。 |
| 组合器 | `$C=\langle [n_F],L,[m],i_0,\rho,\emptyset,L_C \rangle$` | component-library composition 的正式骨架。 |
| 组合系统状态 | `$Q_{CL}=\bigcup_{i\in[m]}Q(i)\times\{i\}$` | 当前组件内部状态加实例索引。 |
| 控制交接 | `$\delta_{CL}(\langle q,i\rangle,\sigma)=\langle q_0(\rho(i,j)),\rho(i,j)\rangle$` | final-state 驱动的 hand-off。 |
| family 边界 | `data-flow undecidable`, `control-flow 2EXPTIME-complete` | 为后续 recursive branch 划出可入树入口。 |

## 构造方式与承载格式

### 建模入口

1. 先把底层可复用模块建成 transducer components。
2. 为每个 component 固定 final states 作为交接接口。
3. 再用 composition transducer 指定 final-state 到下一个 component 的映射。
4. 最后把整个组合转写成 regular composition tree 供 automata 处理。

### 机器可处理承载方式

原文核心机器承载方式有：

1. component transducer tuple；
2. control-flow composition transducer；
3. composition tree；
4. parity tree automata over composition trees。

### 交换与互操作

它与当前文库中的关系如下：

1. 是 [synthesis-from-recursive-components-libraries/desc.md](../synthesis-from-recursive-components-libraries/desc.md) 的直接前身。
2. 也为 [synthesis-of-hierarchical-systems/desc.md](../synthesis-of-hierarchical-systems/desc.md) 的 hierarchical-component-library branch 提供 flat precursor。
3. 与 [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md) 一样，都在把“开放组合”压回 formal model，而不是只谈应用。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 transducer component 和 composition tree。
- 仿真/执行支持：组合后的 `C_L` 自身就是可执行 transducer。
- 验证/分析支持：可转成 regular tree / parity automata synthesis 问题。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：研究型 family，主要价值在提供 component-library control-flow 的正式蓝本。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要从有限状态组件库合成更大控制器，但还没进入递归调用层时。
2. 关心组件的 final-state interface，而不是数据流 wiring 时。
3. 作为 recursive / hierarchical library synthesis 的 flat 先导模型。

### 需求前提

1. 系统任一时刻只有一个组件处于 control。
2. 组件的控制交接可以抽成有限 final-state 接口。
3. 问题重点在 control-flow composition，而不是 data-flow。

### 不适用或高成本场景

如果系统本质上需要 call-return 栈、re-entry semantics 或 bounded hierarchy 重用，这个模型就偏弱，应转向 recursive components 或 hierarchical systems from a library。

## 与相邻形式主义的关系

相对普通 transducer synthesis，它把“从零构造”改成“从组件库组合”；相对 recursive-component libraries，它还没有 call / return / re-entry 语义；相对 hierarchical systems from a library，它还停留在 flat components，而非 boxes / hierarchical sub-transducers。

## 与本研究的关系

对 `project_1` 来说，这篇文献的重要性在于它把“组件库 + 控制交接”稳定成了一个可挂树的 family。后续若要研究“需求先映成可复用片段，再自底向上组出层次模型”，这条线比 generic synthesis 论文更接近目标形式主义建设。

## 重要的相关工作

1. [synthesis-from-recursive-components-libraries/desc.md](../synthesis-from-recursive-components-libraries/desc.md)：在本条 flat control-flow branch 上继续加上 call-return 结构。
2. [synthesis-of-hierarchical-systems/desc.md](../synthesis-of-hierarchical-systems/desc.md)：把组件库推进到 hierarchy-preserving transducer family。
3. [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md)：open hierarchical side 的另一条 formal branch。

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为主体是 component transducer 及其组合模型。
- 这是一篇 `🧱 模型本体` 文献，因为真正可入库的是 control-flow component-library formalism，而不是 synthesis procedure 本身。
- 它主要描述 `🤝 接口 / 交互契约`，因为 final-state interface 与 control hand-off 是核心对象。
- 它属于 `🧮 形式语言与自动机理论`，因为整篇都在 automata/tree-automata 层面定义对象与证明边界，而非实现框架或 DSL。
