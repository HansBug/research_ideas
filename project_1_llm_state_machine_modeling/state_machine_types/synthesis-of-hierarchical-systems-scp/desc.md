# 层次系统的合成（SCP 全文版） / Synthesis of hierarchical systems

## 基本信息

- 标题：Synthesis of hierarchical systems
- 中文标题：层次系统的合成（SCP 全文版）
- 作者：Benjamin Aminof、Fabio Mogavero、Aniello Murano
- 发表：*Science of Computer Programming*, 83:56-79, 2014
- DOI：`10.1016/j.scico.2013.07.001`
- 链接：https://doi.org/10.1016/j.scico.2013.07.001
- 形式主义：`Hierarchical Systems from a Library / Hierarchical-Component Libraries`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / hierarchical-component-library family 稳定
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 hierarchical structure / transducer tuple、connectivity tree、single-round / multi-round synthesis 与 modularity-criteria automata。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 hierarchical transducer、library `L_0`、connectivity tree 与 regular witness。

## 简报

这篇 journal 版的价值，不是简单把 conference 稿拉长，而是把 `hierarchical systems from a library` 这条线真正稳定成了一个可长期引用的 family。它补齐了 hierarchical structures 与 hierarchical transducers 的正式定义，给出更完整的 chronograph 例子，并把“多轮 bottom-up synthesis + modularity criteria”写成了可重复引用的口径。对当前演化树来说，这篇全文版意味着这条 library-hierarchy 支线不再只有一个 short conference 起点。

- 形式主义定位：hierarchical-component-library branch 的 journal-level family anchor。
- 构造方式简述：库元素是 hierarchical transducers，合成结果通过 connectivity tree 选择库组件并连接其 exits，同时可在多轮中持续回灌新模块。
- 基础设施与场景简述：虽然仍是纯理论条目，但它把 connectivity-tree witness、hierarchical parity-game summaries 与 modularity criteria 一起整理进一个更完整的 family 定义里。

```text
hierarchical transducer library -> connectivity tree -> hierarchy-preserving synthesis -> modularity criteria -> multi-round bottom-up design
```

## 形式主义定义与核心对象

### 定义对象

相对 conference 版，journal 版把对象固定成两层：

1. hierarchical structures / hierarchical transducers 的正式母定义；
2. 从 library 合成 hierarchy 的 connectivity-tree 语义。

因此它不仅是算法长文版，也是 family 边界的稳定整理版。

### 核心抽象

journal 版首先把 hierarchical structure 与 hierarchical transducer 分开讲。对当前文库最关键的是 transducer 版本：

$$
K=\langle \Sigma_I,\Sigma_O,\langle K_1,\ldots,K_n\rangle\rangle
$$

其中每个 sub-transducer 仍写成：

$$
K_i=\langle W_i,B_i,in_i,Exit_i,\tau_i,\delta_i,\Phi_i\rangle
$$

上式中的符号逐项解释如下：

1. `W_i` 是局部状态。
2. `B_i` 是 boxes 或 superstates。
3. `in_i` 是入口。
4. `Exit_i` 是出口集合。
5. `\tau_i` 指出每个 box 引用哪个下层 sub-transducer。
6. `\delta_i` 是 deterministic transition function。
7. `\Phi_i` 给状态打输出标签。

原文还明确写出 flat expansion `K^f`，并强调 hierarchical systems 可以看作 bounded recursive systems 的特例。

### 一个最小例子与通俗解释

journal 版详写的 chronograph 例子很好地说明了这条 family：

1. 先有一个 seconds-counter transducer。
2. 再通过 boxes 复用它构造 minutes-counter。
3. 合成出的 60 分钟计时器还能继续放回库里，被更高层组件拿去复用。

通俗地说，这条线是在回答：“如果我手里已经有若干层次状态机模块，能不能继续用它们长出新的层次状态机，而不是每次都平铺重写一遍？” 论文给出的回答是肯定的，而且 formalism 足够稳定。

### 运行 / 接受 / 转移语义

单个 hierarchical transducer 的运行仍通过 flat expansion 来解释；但真正的新语义对象是 connectivity tree。每个树节点标记某个库 transducer，孩子节点对应当前 transducer 的不同 exits 之后连接的下游组件。

因此，一个 synthesized hierarchical system 可以被 connectivity tree 编码，而 regular connectivity tree 则对应一个有限可表示的 witness。虽然原文的 automata construction 很复杂，但对 family 本体而言，关键只是：

$$
\text{library composition} \Longleftrightarrow \text{connectivity tree}
$$

这让“从库合成层次系统”不再是口头说法，而是一个稳定的树对象。

### 语义边界

journal 版进一步把边界讲清楚：

1. 这条线强调 finite hierarchy 的复用，不走无界 recursion。
2. 逻辑虽可用 `LTL` 或 `\mu`-calculus，但逻辑不是 family 本体。
3. modularity criteria 也只是约束 synthesized hierarchy 的额外条件，不改变底层对象仍是 hierarchical transducer library。

### 关键性质与判定边界

journal 版保留并系统化了 conference 版的复杂度边界：

$$
\mu\text{-calculus}: \mathrm{EXPTIME}\text{-complete}
$$

以及

$$
LTL: 2\mathrm{EXPTIME}\text{-complete}
$$

同时强调 synthesized hierarchical system 可能指数级小于 flat counterpart，却不导致更差的基本复杂度量级。对演化树而言，这说明该 family 不是“工程压缩技巧”，而是一条正式模型分支。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | hierarchical transducer 是核心对象。 |
| 事件 / 触发 | 支持 | 输入驱动 deterministic transitions。 |
| 守卫 / 数据 | 不支持 | 不依赖额外变量。 |
| 层次 | 强支持 | boxes / exits / sub-transducers 构成主体。 |
| 并发 / 同步 | 不支持 | 主线仍是 sequential hierarchy。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | connectivity tree、regular witness、tree automata 和 modularity criteria 一体化。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| hierarchical transducer | `$K=\langle \Sigma_I,\Sigma_O,\langle K_1,\ldots,K_n\rangle\rangle$` | family 母定义。 |
| sub-transducer | `$K_i=\langle W_i,B_i,in_i,Exit_i,\tau_i,\delta_i,\Phi_i\rangle$` | 层次组件骨架。 |
| flat expansion | `$K^f$` | hierarchy 到 flat semantics 的桥。 |
| witness object | `connectivity tree` | library-based synthesis 的正式承载。 |
| 判定边界 | `$\mu$: EXPTIME`, `$LTL: 2EXPTIME$` | family 的稳定复杂度。 |

## 构造方式与承载格式

### 建模入口

1. 先准备初始库 `L_0`。
2. 库中每个元素都是 hierarchical transducer。
3. 单轮合成通过 connectivity tree 连接这些组件。
4. 多轮合成则把新模块继续回写到库中。

### 机器可处理承载方式

journal 版更完整地固定了以下机器承载方式：

1. hierarchical structure / transducer tuple；
2. flat expansion；
3. connectivity tree；
4. regular connectivity witness；
5. modularity-criteria tree automata。

### 交换与互操作

它与当前文库中的关系如下：

1. 是 [synthesis-of-hierarchical-systems/desc.md](../synthesis-of-hierarchical-systems/desc.md) 的 journal full version。
2. 与 [improved-model-checking-of-hierarchical-systems-iandc/desc.md](../improved-model-checking-of-hierarchical-systems-iandc/desc.md) 一起，分别从 synthesis 和 model-checking 两侧稳定 bounded hierarchy。
3. 与 [synthesis-from-recursive-components-libraries/desc.md](../synthesis-from-recursive-components-libraries/desc.md) 构成 bounded hierarchy 与 unbounded recursive library 的分叉。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 hierarchical transducer、connectivity tree 与 modularity criteria automata。
- 仿真/执行支持：flat expansion 提供执行语义。
- 验证/分析支持：`LTL / \mu`-calculus synthesis、regular witness、tree automata。
- 代码生成/转换支持：原文未给出工程代码生成。
- 标准化或社区生态：研究型 family，但作为 journal full version，足以稳定此支线的命名与口径。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要正式表达“从层次组件库多轮长出新模块”的场景。
2. 希望 synthesized result 天然保持 hierarchy，而非事后压缩的场景。
3. 需要为 hierarchy-preserving bottom-up design 找到 formal anchor 的场景。

### 需求前提

1. 系统复用关系应是有限层次的。
2. 组件接口可抽成 boxes 与 exits。
3. 设计过程允许以模块为粒度逐轮推进。

### 不适用或高成本场景

若目标需要无界调用栈或更强的 pushdown-like recursion，这条线就不如 recursive-component libraries / `RSM`；若只关心 closed/open hierarchy 的 verification 而不关心 library growth，则 `HSM/HMTS/open modules` 更直接。

## 与相邻形式主义的关系

相对 conference 版，它把 family 边界写得更完整；相对 flat component libraries，它强调 hierarchy-preserving reuse；相对 recursive-component libraries，它代表 bounded hierarchy 一侧，而不是无界 call-return 栈。

## 与本研究的关系

这篇全文版对 `project_1` 很重要，因为它把“生成局部层次模块，再逐轮回灌、复用、扩张”为一种 formalism 而不是 workflow slogan。对 LLM 驱动的“生成-验证-修复”闭环来说，这种多轮模块成长视角很有启发价值。

## 重要的相关工作

1. [synthesis-of-hierarchical-systems/desc.md](../synthesis-of-hierarchical-systems/desc.md)：conference 起点。
2. [synthesis-from-component-libraries/desc.md](../synthesis-from-component-libraries/desc.md)：flat component-library precursor。
3. [improved-model-checking-of-hierarchical-systems-iandc/desc.md](../improved-model-checking-of-hierarchical-systems-iandc/desc.md)：bounded hierarchy 的 verification/full-version sibling。

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为主体是 hierarchical transducer family。
- 这是一篇 `🧱 模型本体` 文献，因为全文版真正稳定的是 hierarchical-component-library formalism，而不是单次合成技巧。
- 它主要描述 `🎛️ 控制 / 反应式逻辑`，因为对象仍是输入驱动的层次控制器。
- 它属于 `🧮 形式语言与自动机理论`，因为核心工作是形式定义、tree-automata construction 与 family complexity 边界。
