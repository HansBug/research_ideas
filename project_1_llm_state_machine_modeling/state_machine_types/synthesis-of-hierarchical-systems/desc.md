# 层次系统的合成 / Synthesis of Hierarchical Systems

## 基本信息

- 标题：Synthesis of Hierarchical Systems
- 中文标题：层次系统的合成
- 作者：Benjamin Aminof、Fabio Mogavero、Aniello Murano
- 发表：*Formal Aspects of Component Software*, pp. 42-60, 2012
- DOI：`10.1007/978-3-642-35743-5_4`
- 链接：https://doi.org/10.1007/978-3-642-35743-5_4
- 形式主义：`Hierarchical Systems from a Library / Hierarchical-Component Libraries`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / hierarchical-component-library branch
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 hierarchical transducer tuple、library of hierarchical components、connectivity tree 与 parity tree automata。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 hierarchical transducer `K=\langle \Sigma_I,\Sigma_O,\langle K_1,\ldots,K_n\rangle\rangle`、box / exit interfaces、library `L_0` 与 connectivity tree。

## 简报

这篇论文把“从组件库合成系统”这条线真正拉回层次状态机谱系。作者不再满足于 flat transducer library，而是明确要求库元素本身就是 hierarchical transducer，并且允许多轮 bottom-up synthesis。对当前演化树来说，它补出的不是一个算法优化节点，而是一条很清楚的 family：系统可以不是从零平铺出来，而是从层次组件库中逐层组装出来。

- 形式主义定位：component-library line 上的 bounded-hierarchy 扩展，也就是“从层次组件库合成层次系统”。
- 构造方式简述：每个库元素都是带 boxes 的 hierarchical transducer；合成结果通过 connectivity tree 指定每个 exit 后应该接哪一个库中层次组件。
- 基础设施与场景简述：论文没有工程工具，但 connectivity tree、hierarchical transducer、regular witness 与 modularity criteria 已足够把它稳定成可挂树的 family。

```text
hierarchical transducer library -> boxes / exits -> connectivity tree -> synthesized hierarchical transducer -> bottom-up module growth
```

## 形式主义定义与核心对象

### 定义对象

原文的核心对象不是单个 flat transducer，而是“层次 transducer 的库”。每个组件本身就可以嵌套子组件，且合成结果仍保持 hierarchy，而不是 flatten 后再重组。

### 核心抽象

原文把 hierarchical transducer 写成：

$$
K=\langle \Sigma_I,\Sigma_O,\langle K_1,\ldots,K_n\rangle\rangle
$$

其中每个 sub-transducer 满足：

$$
K_i=\langle W_i,B_i,in_i,Exit_i,\tau_i,\delta_i,\Phi_i\rangle
$$

上式中的符号逐项解释如下：

1. `W_i` 是局部状态集合。
2. `B_i` 是 boxes 集合。
3. `in_i` 是 entry state。
4. `Exit_i` 是 exits 集合。
5. `\tau_i` 把每个 box 映到更低层 sub-transducer。
6. `\delta_i` 是在内部状态或 box-exit 上读输入后的迁移函数。
7. `\Phi_i` 是输出标签函数。

flat expansion 则把 hierarchy 展开成普通 Moore machine：

$$
K^f
$$

它说明这个 family 并没有脱离经典有限状态骨架，只是通过 boxes 把重复子结构压缩了。

### 一个最小例子与通俗解释

原文的 chronograph 例子很适合作为直觉模型：

1. 秒计数器是一个低层 transducer。
2. 分钟计数器通过若干 boxes 反复调用秒计数器。
3. 如果把合成好的 60 分钟计时器放回库中，还能继续被小时计数器复用。

通俗地说，这个 formalism 像“把层次状态机真的当作可复用的积木块”。与普通 synthesis 不同，目标不是找一张巨大的 flat 状态图，而是找一棵能复用已有层次部件的 connectivity tree。

### 运行 / 接受 / 转移语义

hierarchical transducer 的一步迁移由局部状态或 box exit 与输入字母共同决定：

$$
\delta_i:(\bigcup_{b\in B_i}\{b\}\times Exit_{\tau_i(b)} \cup (W_i\setminus Exit_i)) \times \Sigma_I \to W_i \cup B_i
$$

上式中的符号逐项解释如下：

1. 当前控制点可以是内部状态，也可以是某个 box 的某个 exit。
2. 读入一个输入字母后，控制点要么去本层另一个状态，要么进入另一个 box。
3. 进入 box 时，语义上隐式跳到被调 sub-transducer 的 `in_j`。

库级别的组合不直接写成“大图拼接”，而是写成 connectivity tree。每个节点选择一个库组件，子节点对应其各个 exits 后面接上的下游组件。这一承载方式是本 family 真正的结构化语义核心。

### 语义边界

这条支线与 recursive-component libraries 的边界很清楚：

1. 这里强调的是 bounded hierarchy，而不是无界调用栈。
2. 组件复用通过 box nesting 实现，而不是 pushdown-like recursive call stack。
3. 因此它更接近 `HSM/HMTS` 一侧，而不是 `RSM` 的无界递归侧。

### 关键性质与判定边界

原文把 family 的复杂度边界写得很稳定：

$$
\mu\text{-calculus synthesis from a hierarchical library is EXPTIME-complete}
$$

以及

$$
LTL\text{ synthesis from a hierarchical library is }2\mathrm{EXPTIME}\text{-complete}
$$

更关键的是，作者强调 synthesized hierarchical system 可能比 flat system 指数级更小，但复杂度并没有因此上升到更高量级。这正说明它是一条值得单独维护的 hierarchy-preserving family。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 由 hierarchical transducer 状态和 boxes 组成。 |
| 事件 / 触发 | 支持 | 输入字母驱动局部迁移。 |
| 守卫 / 数据 | 不支持 | 重点不在变量。 |
| 层次 | 强支持 | boxes / sub-transducers 是本体。 |
| 并发 / 同步 | 不支持 | 主线是 sequential hierarchy。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | flat expansion、connectivity tree、tree automata 都完整给出。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总体定义 | `$K=\langle \Sigma_I,\Sigma_O,\langle K_1,\ldots,K_n\rangle\rangle$` | hierarchical transducer 总骨架。 |
| sub-transducer | `$K_i=\langle W_i,B_i,in_i,Exit_i,\tau_i,\delta_i,\Phi_i\rangle$` | 单个层次组件的正式 tuple。 |
| flat expansion | `$K^f$` | hierarchy 与普通 transducer 的桥。 |
| 迁移函数 | `$\delta_i:(\cdots)\times\Sigma_I \to W_i \cup B_i$` | box-exit 与内部状态统一进同一语义。 |
| library synthesis 边界 | `$\mu$-calculus: EXPTIME`, `$LTL: 2EXPTIME$` | hierarchy-preserving family 的稳定复杂度。 |

## 构造方式与承载格式

### 建模入口

1. 先定义一批 hierarchical transducer components。
2. 为每个组件固定 boxes、exits 与 box-to-subtransducer 映射。
3. 再用 connectivity tree 指出各个 exits 后面接哪一个库组件。
4. 如需多轮设计，则把新合成出的模块回灌进库 `L_0`。

### 机器可处理承载方式

机器可处理承载方式主要有：

1. hierarchical transducer tuple；
2. flat expansion；
3. library `L_0`；
4. connectivity tree；
5. parity tree automata。

### 交换与互操作

它与当前文库中的关系如下：

1. 承接 [synthesis-from-component-libraries/desc.md](../synthesis-from-component-libraries/desc.md) 的 flat control-flow component-library branch。
2. 与 [improved-model-checking-of-hierarchical-systems/desc.md](../improved-model-checking-of-hierarchical-systems/desc.md) 一样，都强调 finite hierarchy 的独立价值。
3. 相对 [synthesis-from-recursive-components-libraries/desc.md](../synthesis-from-recursive-components-libraries/desc.md)，它选择 bounded hierarchy 而非无界 recursive call stack。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 hierarchical transducer、flat expansion 与 connectivity tree。
- 仿真/执行支持：flat expansion 提供直接执行语义。
- 验证/分析支持：基于 tree automata 的 realizability / synthesis。
- 代码生成/转换支持：原文未给工程代码生成流程。
- 标准化或社区生态：研究型 family，主要价值在把 library-based hierarchy synthesis 固定成 formal node。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要自底向上复用层次组件构造更大控制器的场景。
2. 希望把 synthesized result 保持成 hierarchy，而不是平铺成 flat transducer 的场景。
3. 需要给“可复用层次状态机库”找 formal-language / automata-theory 蓝本时。

### 需求前提

1. 系统的复用关系是有限层次的。
2. 组件接口可抽成 boxes 与 exits。
3. 目标系统可以接受 library-based bottom-up growth，而不是无界过程递归。

### 不适用或高成本场景

如果问题真正依赖无界 call-return recursion，这条线就不如 recursive-component libraries 或 `RSM` 合适；如果问题只需 open/closed semantics 而不涉及库复用，则 `HSM/HMTS` 足够。

## 与相邻形式主义的关系

相对 flat component libraries，它把组件本体提升成 hierarchy；相对 `HSM/HMTS`，它更强调“来自库的组合与复用”；相对 recursive-component libraries，它保留有限层次、避免掉入无界 pushdown semantics。

## 与本研究的关系

对 `project_1` 而言，这篇论文特别有价值，因为它把“先产出可复用模块，再不断拼成更大模型”正式写成了 hierarchy-preserving formalism。若未来希望 LLM 先生成局部模式块、再在验证闭环里逐层装配，这篇文献比传统 monolithic synthesis 更贴近研究目标。

## 重要的相关工作

1. [synthesis-from-component-libraries/desc.md](../synthesis-from-component-libraries/desc.md)：flat component-library precursor。
2. [synthesis-of-hierarchical-systems-scp/desc.md](../synthesis-of-hierarchical-systems-scp/desc.md)：同一家族的 journal full version。
3. [improved-model-checking-of-hierarchical-systems/desc.md](../improved-model-checking-of-hierarchical-systems/desc.md)：hierarchy-preserving abstraction / game side 的 bounded-hierarchy sibling。

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为核心对象是层次 transducer family。
- 这是一篇 `🧱 模型本体` 文献，因为真正可挂树的是 hierarchical-component-library formalism，而不是 synthesis algorithm 的技巧。
- 它主要描述 `🎛️ 控制 / 反应式逻辑`，因为对象是输入驱动的层次控制器 / Moore machine。
- 它属于 `🧮 形式语言与自动机理论`，因为全文通过 automata、tree automata 与 complexity 方式刻画 hierarchy-preserving family。
