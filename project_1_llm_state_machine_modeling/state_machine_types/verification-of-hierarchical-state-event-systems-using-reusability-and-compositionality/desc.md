# 基于复用与组合性的层次 State/Event 系统验证 / Verification of Hierarchical State/Event Systems using Reusability and Compositionality

## 基本信息

- 标题：Verification of Hierarchical State/Event Systems using Reusability and Compositionality
- 中文标题：基于复用与组合性的层次 State/Event 系统验证
- 作者：Gerd Behrmann, Kim G. Larsen, Henrik Reif Andersen, Henrik Hulgaard, Jørn Lind-Nielsen
- 发表：*Formal Methods in System Design*, 21(2):225-244, 2002
- DOI：`10.1023/A:1016095519611`
- 链接：https://doi.org/10.1023/A:1016095519611
- 形式主义：`Hierarchical State/Event Machines / Systems (HSEM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / `SEM` hierarchy extension
- 工具/实现获取方式：原文直接面向 `visualSTATE` 层次扩展；机器可处理入口是 `HSEM` 七元组、serial / history / parallel state、flattening 与 hierarchy-aware reachability reuse。
- 标准/格式获取方式：原文没有独立 DSL 标准；核心承载方式是 `HSEM` 七元组、superstate 嵌套结构和由 flattening 派生的并发 `SEM` 语义。

## 简报

这篇论文真正补出来的，是 `State/Event` 这条线上的层次化版本，而不是又一篇“如何更快验证状态图”的方法文。它把 flat `SEM` 正式推进成 `HSEM`：状态不再只有 primitive state，还允许 serial、serial-history 和 parallel state；迁移也不再只在同一层里走，而是允许跨层、跨类型发生。对当前演化树而言，它让 `SEM` 这条母线长出了真正的 hierarchy 子枝，因此值得作为 `SEM -> HSEM` 的直接树节点，而不只是 `Statecharts` 的旁证。

- 形式主义定位：`SEM` 的层次扩展，把 `Statecharts` 风格的 nesting 收束到 `State/Event` family 中。
- 构造方式简述：模型由 primitive / serial / serial-history / parallel 四类状态和带事件、guard、输出多重集的迁移构成。
- 基础设施与场景简述：原文仍然依托 `visualSTATE`，但关键贡献是把 hierarchy 本身写成可形式化、可 flatten、可复用 reachability 结果的模型对象。

```text
并发 SEM -> superstate 嵌套 -> serial / history / parallel hierarchy -> flattening or hierarchy-aware verification
```

## 形式主义定义与核心对象

### 定义对象

`HSEM` 是一个层次自动机。和 flat `SEM` 相比，它最本质的变化不是“状态图更好看”，而是状态本身也分型了：有的状态是 primitive，有的状态是串行容器，有的状态带 history 语义，有的状态是并行容器。

### 核心抽象

论文直接给出 `HSEM` 七元组：

$$
M = \langle S, E, O, T, Sub, type, def \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `E` 是事件集合。
3. `O` 是输出集合。
4. `T` 是迁移集合。
5. `Sub : S \to P(S)` 给出每个状态的子状态集合。
6. `type : S \to \{pr,se,sh,pa\}` 指示状态类型，分别表示 primitive、serial、serial-history、parallel。
7. `def` 是对 serial 与 history 状态定义默认子状态的偏函数。

原文同时给出迁移类型：

$$
T \subseteq S \times E \times G \times M(O) \times S
$$

上式中的符号逐项解释如下：

1. 第一和最后一个 `S` 分别是源状态与目标状态。
2. `E` 是触发迁移的事件。
3. `G` 是 guard 集合。
4. `M(O)` 是输出动作的多重集。

### 一个最小例子与通俗解释

原文自己的 toy train 例子就很合适：

1. 顶层系统有 `Train` 与 `Crossing` 两个组件。
2. `Train` 内部的 `Move` 不是 primitive state，而是一个 superstate。
3. `Move` 再细分为 `Left` 与 `Right` 两个 primitive substates。
4. `Move` 还能被标成 history state，使再次激活时回到上次离开的子状态。

通俗地说，`HSEM` 像“把 `SEM` 放进能分层的盒子里”。普通 `SEM` 只会在同一平面上同步反应；`HSEM` 允许一个状态自己又是一台小系统，而且这个小系统还能带默认入口、history 和记忆。

### 运行 / 接受 / 转移语义

原文的关键语义桥梁是 flattening。也就是说，一个层次 `HSEM` 可以被递归展开成等价的 flat `SEM`。可保守整理成：

$$
\mathrm{flat}(M) = \text{an equivalent non-hierarchical } SEM
$$

并把某个子状态的 reachability 问题转写成 flattened system 上的 reachability：

$$
\mathrm{Reach}_M(s) \iff \mathrm{Reach}_{\mathrm{flat}(M)}(enc(s))
$$

这里的符号逐项解释如下：

1. `M` 是原始层次模型。
2. `\mathrm{flat}(M)` 是展开后的 flat `SEM`。
3. `enc(s)` 表示状态 `s` 在 flat system 中对应的编码位置。

这一定义抓住了论文的核心语义：`HSEM` 的层次结构并不改变它仍可落回 `SEM` 的事实，但保留 hierarchy 时可以复用 superstate 的 reachability 结果，避免每次都完全 flatten。

### 语义边界

`HSEM` 的边界如下：

1. 仍是纯离散、有限控制 family。
2. 新增的是 hierarchy 与 history，不是时钟或栈。
3. 迁移可跨任意层级与状态类型发生，这比普通 tree-shaped `FSM` 更灵活。
4. 其下层语义仍回到 `SEM`，不是另一套全新执行机理。

### 关键性质与判定边界

原文关心的核心问题仍是 reachability，但 hierarchy-aware reusability 是这篇条目的关键。可保守压成：

$$
\text{Given a target state } s,\ \text{decide whether } s \in \mathrm{Reach}(M)
$$

以及

$$
\mathrm{Reach}(superstate) \Rightarrow \text{candidate reuse for substates}
$$

也就是说，`HSEM` 的 hierarchy 不是只拿来画图，而是直接进入了验证语义与优化口径。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | primitive、serial、history、parallel 四类状态都是一等对象。 |
| 事件 / 触发 | 强支持 | 迁移由事件驱动。 |
| 守卫 / 数据 | 部分支持 | 有 guard，但主体仍是状态依赖，不是一般变量程序。 |
| 层次 | 强支持 | `Sub / type / def` 是模型核心。 |
| 并发 / 同步 | 强支持 | parallel state 直接属于语言本体。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | 可 flatten，也可做 hierarchy-aware reachability reuse。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `HSEM` 元组 | `$M=\langle S,E,O,T,Sub,type,def\rangle$` | 模型本体。 |
| 状态类型 | `$type:S \to \{pr,se,sh,pa\}$` | primitive / serial / history / parallel。 |
| 迁移关系 | `$T \subseteq S \times E \times G \times M(O) \times S$` | 事件、guard、输出一体化。 |
| flattening | `$\mathrm{flat}(M)$` | hierarchy 与 flat `SEM` 之间的语义桥梁。 |
| reachability bridge | `$\mathrm{Reach}_M(s) \iff \mathrm{Reach}_{\mathrm{flat}(M)}(enc(s))$` | hierarchy-preserving verification 的基础。 |

## 构造方式与承载格式

### 建模入口

1. 先定义顶层 `SEM` 组件与状态。
2. 再挑出需要细化的状态，给它们配置子状态集合 `Sub`。
3. 用 `type` 指明该状态是 serial、history 还是 parallel。
4. 若是 serial 或 history，再用 `def` 指定默认子状态。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `HSEM` 七元组。
2. superstate / substate 关系。
3. state type 与 default-substate 映射。
4. flattened `SEM` 表示与 hierarchy-aware reachability structures。

### 交换与互操作

这篇论文没有公共交换格式，但在谱系上承担三层桥接：

1. 向上承接 [verification-of-large-state-event-systems-using-compositionality-and-dependency-analysis/desc.md](../verification-of-large-state-event-systems-using-compositionality-and-dependency-analysis/desc.md) 的 `SEM` 母线。
2. 向旁对照 [model-checking-of-hierarchical-state-machines-toplas/desc.md](../model-checking-of-hierarchical-state-machines-toplas/desc.md) 的 `HSM`。
3. 向下说明 `State/Event` 家族也能长出自己的 hierarchy 分支，而不是只能依附 `Statecharts` 一条线。

## 配套基础设施

- 建模/编辑工具：原文明确依托 `visualSTATE` 及其层次扩展。
- 解析/交换/元模型支持：核心是 `HSEM` 七元组和 flattening 语义；无公开独立标准。
- 仿真/执行支持：可回落到 flat `SEM` 执行直觉。
- 验证/分析支持：hierarchy-aware reusability + compositional verification。
- 代码生成/转换支持：与 `visualSTATE` 工具链直接相关。
- 标准化或社区生态：研究与工业工具结合，但未形成广泛独立标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 控制逻辑天然带层次细化的嵌入式系统。
2. 同时需要并发组件与局部 history 记忆的状态机模型。
3. 希望保留 hierarchy 进行验证，而不是一开始就彻底 flatten 的场景。

### 需求前提

1. 控制复杂性主要来自层次细化，而不是递归调用。
2. 子状态切换关系可由有限事件和 guard 表达。
3. history 语义和 parallel region 是需求中的稳定概念，而非偶然图形整理。

### 不适用或高成本场景

如果需求核心是 entry/exit 接口、作用域变量和 black-box mode，更适合 [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)；如果核心是 recursion / call-return，则应转向 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)。

## 与相邻形式主义的关系

相对 `SEM`，`HSEM` 直接增加了 hierarchy 与 history；相对 `HSM`，它仍然保留 `State/Event` 风格的 event + guard + output 多重集骨架；相对 `HRM`，它还没有明确的 entry/exit interface、作用域变量和 mode reference 语义。

## 与本研究的关系

### 对 Project 1 的价值

`HSEM` 让 `State/Event` 这条线不再停在 flat 并发机，而是能真正进入层次状态机演化树，并与 `HSM/HRM` 形成可比较的 siblings。

### 作为目标形式主义还是中间表示

它既可以是目标形式主义，也可以是工程中间表示，尤其适合那些需求里已经显式出现“父状态/子状态/恢复上次子状态”的场景。

### 对需求到模型生成的启发

当需求文本里出现“某个模式内部还要继续细分”“退出后下次回到上次停的位置”“一个状态内部又含多个并行子流程”时，LLM 的目标就不该再是 flat `SEM`，而应升级到 `HSEM`。

### 现实限制

它仍然缺少真正的 call-return、time 和 richer data semantics；同时，公开标准化生态没有 `SCXML/UML` 那么强。

## 重要的相关工作

### 前后衔接

- [verification-of-large-state-event-systems-using-compositionality-and-dependency-analysis/desc.md](../verification-of-large-state-event-systems-using-compositionality-and-dependency-analysis/desc.md)
- [verification-of-state-event-systems-by-quotienting/desc.md](../verification-of-state-event-systems-by-quotienting/desc.md)
- [model-checking-of-hierarchical-state-machines-toplas/desc.md](../model-checking-of-hierarchical-state-machines-toplas/desc.md)

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为主体仍是离散层次控制，不涉及 clocks、continuous dynamics 或 probability。
- 这是一篇 `🧱 模型本体` 文献，因为原文直接提出并定义了 `HSEM` 七元组和状态类型体系。
- 这篇论文的描述客体是 `🎛️ 控制 / 反应式逻辑`，因为它面向嵌入式反应式控制器而非词、树或协议。
- 这篇论文属于 `🧮 形式语言与自动机理论`，因为它服务的是层次状态机 family 的正式定义、语义边界和谱系扩树。
