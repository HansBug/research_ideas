# 层次模块检验中的程序复杂性 / Program Complexity in Hierarchical Module Checking

## 基本信息

- 标题：Program Complexity in Hierarchical Module Checking
- 中文标题：层次模块检验中的程序复杂性
- 作者：Aniello Murano, Margherita Napoli, Mimmo Parente
- 发表：*Logic for Programming, Artificial Intelligence, and Reasoning*, pp. 318-332, 2008
- DOI：`10.1007/978-3-540-89439-1_23`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/hier-module.pdf
- 形式主义：`Hierarchical Modules / Open Hierarchical State Machines`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / open hierarchical module
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 hierarchical module tuple、expanded flat module `M^f`、execution-tree set `exec(M)` 与 hierarchical Buchi tree automata `HNBT`。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 system / environment node partition、supernodes、open-module semantics 与 HNBT-based CTL checking。

## 简报

这篇论文表面上讲的是 `CTL` hierarchical module checking 的复杂度，但真正值得文库收的是它把 `HSM` 清楚推进成了 open-system 版本：节点不再只分层展开，还被划成 system nodes 和 environment nodes，supernode 也不再只是 closed hierarchy，而是“一个模块里还可以嵌另一个模块”的开放式层次机。对当前演化树来说，它补出的不是算法附庸，而是 `HSM` 支线向 open-system / module-checking 语义的一条稳定分支。

- 形式主义定位：`HSM` 的 open-system generalization，把 hierarchy 与 environment pruning semantics 合到同一模块模型里。
- 构造方式简述：每个 component 同时含 system nodes、environment nodes、boxes、exit nodes；box 指向更低层 component，并在展开后形成 open flat module。
- 基础设施与场景简述：纯理论条目，但给出 `hierarchical module`、expanded flat module `M^f`、`exec(M)`、`HNBT` 与 single-exit / multiple-exit program complexity。

```text
hierarchical module -> system/environment partition + supernodes -> open execution trees exec(M) -> HNBT -> CTL module checking
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 open systems 的层次版本。相比 closed `HSM`，新东西主要有两点：

1. 节点区分 system 与 environment。
2. boxes 指向的不是单纯 closed component，而是另一个 open hierarchical module。

因此，这篇论文实际上给出了“open hierarchical state machine / hierarchical module”的正式骨架。

### 核心抽象

原文把一个 hierarchical module 写成：

$$
M = (M_1,\ldots,M_n)
$$

其中每个 component 可整理为：

$$
M_i = (AP,S_i,E_i,R_i,Box_i,O_i,in_i,L_i,Y_i)
$$

上式中的符号逐项解释如下：

1. `AP` 是 atomic propositions 集合。
2. `S_i` 是 system nodes。
3. `E_i` 是 environment nodes。
4. `R_i` 是边关系。
5. `Box_i` 是 boxes / supernodes。
6. `O_i` 是 exit nodes。
7. `in_i` 是初始节点。
8. `L_i` 是命题标签函数。
9. `Y_i : Box_i \to \{i+1,\ldots,n\}` 把 box 映射到更低层 component。

### 一个最小例子与通俗解释

可以把它想成“一个分层饮料机，但用户选择仍来自环境”：

1. 顶层模块先由系统把水烧开。
2. 到 environment node 时，环境决定选咖啡还是茶。
3. 无论选哪一个，都可能通过 box 进入更细的糖分子模块。
4. module checking 问的是：无论环境怎么 pruning 掉某些分支，系统是否都满足 `CTL` 规范。

通俗地说，`hierarchical module` 像“会和环境持续交互的层次状态机”。它不只是 hierarchy，也不是一般 interface automata，而是把 open-system semantics 直接压进 `HSM` 骨架。

### 运行 / 接受 / 转移语义

原文把展开后的 flat module 记作：

$$
M^f
$$

其状态写成：

$$
\langle u_1,\ldots,u_h \rangle
$$

上式中的符号逐项解释如下：

1. `u_h` 是当前真正所在的 node。
2. `u_1,\ldots,u_{h-1}` 是沿层次展开路径上经过的 boxes。
3. 若 `u_h` 是 system node，则当前由系统选后继；若是 environment node，则由环境决定可用后继。

module checking 关心的不是单棵展开树，而是：

$$
exec(M)
$$

即环境可通过 pruning 产生的所有执行树集合。也正因为如此，open hierarchy 的难点不只是 flatten，而是“所有可能环境剪枝”与 hierarchy 的组合。

### 语义边界

这个 family 的边界很清楚：

1. 它仍是离散层次状态机 family，不引入时间、概率或连续动态。
2. 它不是一般 interface automata，而是 open `HSM`。
3. 当所有 `E_i` 为空时，就退化成 closed hierarchical model。
4. 难点在 open execution-tree semantics，而不是额外的 control feature。

### 关键性质与判定边界

论文的核心判定边界是：

$$
\text{single-exit hierarchical modules} \Rightarrow \mathrm{Ptime}
$$

以及

$$
\text{multiple-exit hierarchical modules} \Rightarrow \mathrm{Pspace}\text{-complete}
$$

这里说的是固定 `CTL` 公式下的 program complexity。也就是说，单出口 open hierarchy 仍能保持和普通 module checking 同级别的 tractability，而多出口 hierarchy 会把复杂度抬到 `Pspace`。

为了得到这个结果，作者引入了：

$$
\mathrm{HNBT}
$$

也就是 hierarchical nondeterministic Buchi tree automata，用来直接吃 `exec(M)`，避免先完全 flatten 再做经典 module checking。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | system nodes、environment nodes、boxes、exit nodes。 |
| 事件 / 触发 | 弱支持 | 重点是树化执行语义，不是动作标签。 |
| 守卫 / 数据 | 不支持 | 核心不在数据。 |
| 层次 | 强支持 | boxes / supernodes 构成 hierarchy。 |
| 并发 / 同步 | 不支持 | sequential open module。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | `exec(M)`、`HNBT`、`CTL` module checking。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$M=(M_1,\ldots,M_n)$` | hierarchical module 总体定义。 |
| 组件元组 | `$M_i=(AP,S_i,E_i,R_i,Box_i,O_i,in_i,L_i,Y_i)$` | open hierarchical component。 |
| flat state | `$\langle u_1,\ldots,u_h\rangle$` | 展开后的上下文状态。 |
| 执行树集合 | `$exec(M)$` | 所有环境 pruning 产生的 execution trees。 |
| 程序复杂度 | `single-exit: Ptime`, `multiple-exit: Pspace` | open hierarchy 的主边界。 |

## 构造方式与承载格式

### 建模入口

1. 先定义 open component：system nodes 与 environment nodes。
2. 再给 component 加上 boxes / exits，形成 hierarchy。
3. 用 `Y_i` 指定 supernode 展开到哪个下层 component。
4. 最后用 `exec(M)` 表达环境 pruning 语义。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. hierarchical module tuple；
2. expanded flat module `M^f`；
3. execution-tree set `exec(M)`；
4. `HNBT`。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 closed `HSM`。
2. 向旁边连接 module checking / open systems / interface reasoning。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 open hierarchical-module tuple 与 `exec(M)`。
- 仿真/执行支持：通过 expanded flat module 与 environment pruning 语义解释。
- 验证/分析支持：`CTL` hierarchical module checking、`HNBT` emptiness。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要价值在 open hierarchy 的 formal semantics。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要同时表达层次控制结构与环境干预的 open systems。
2. 需要比较 closed hierarchy 与 open hierarchy 在判定复杂度上的变化。
3. 想补齐 `HSM` 支线向 module checking / open-system 语义的分叉。

### 需求前提

1. 系统 / 环境责任边界可以抽成 state partition。
2. 环境影响可建模为 execution-tree pruning。
3. 关注的性质主要是 branching-time `CTL`。

### 不适用或高成本场景

如果系统完全 closed、没有环境选择，那么普通 `HSM` 足够；如果需要 richer contract / I-O action semantics，则更适合转向 `I/O Automata` 或 `Interface Automata` 家族。

## 与相邻形式主义的关系

相对 `HSM`，它把 hierarchy 推向 open-system semantics；相对 `RGG`，它不是双人 controller game，而是 environment pruning 的 module checking 语义；相对 `Interface Automata`，它仍保留 `HSM` 的 box-expansion hierarchy，而不是 action-interface composition。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机演化树里还有一条“开放环境 / 模块验证”分支，这对后续考虑需求中的 environment assumption、开放执行上下文与组合验证很重要。

### 作为目标形式主义还是中间表示

更适合作为验证导向中间表示，而不是最终建模语言。

### 对需求到模型生成的启发

如果需求里强依赖环境选择或外部禁用某些行为，单纯 closed `HSM` 不够，需要意识到 open hierarchical module 这种 family 的存在。

### 现实限制

它主要服务 formal verification，缺少工程生态，也不面向直接执行。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)

### 同类型或同家族工作

- [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md)
- `Pushdown module checking`：后续沿 pushdown / open-system 方向继续推进的工作。

## 文献分类总结

- 这篇论文补出了 `HSM` 的 open-system / module-checking 子线。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、工具或应用案例。
- 在当前演化树里，它最适合挂成 `HSM` 之下的“Open Hierarchical Modules”节点，用来和 `RGG`、`Interface Automata` 等开放交互线区分。
