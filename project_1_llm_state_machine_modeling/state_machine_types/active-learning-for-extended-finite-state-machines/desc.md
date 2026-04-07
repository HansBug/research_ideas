# 扩展有限状态机的主动学习 / Active Learning for Extended Finite State Machines

## 基本信息

- 标题：Active Learning for Extended Finite State Machines
- 中文标题：扩展有限状态机的主动学习
- 作者：Sofia Cassel，Falk Howar，Bengt Jonsson，Bernhard Steffen
- 发表：*Formal Aspects of Computing*，28(2):233-263，2016
- DOI：`10.1007/s00165-016-0355-5`
- 链接：https://doi.org/10.1007/s00165-016-0355-5
- 形式主义：`Register Automata / EFSM learning / symbolic decision trees / tree oracles`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal-level `RA/EFSM` active-learning route with symbolic decision trees and canonical tree oracles
- 工具/实现获取方式：原文主体是学习算法、tree queries 与 benchmark 评估，没有给出独立公开工具入口；它更像后续 `LearnLib / RALib / Tomte` 这条数据化自动机学习工具线的理论与方法锚点。
- 标准/格式获取方式：承载方式是 data words、register automata、symbolic decision trees、tree oracles、symbolic suffixes 与 hypothesis automata；不是独立交换标准。

## 简报

这篇论文是 `Learning Extended Finite State Machines` 的 journal 级扩展版，重点不在重新定义一种新的 `EFSM`，而在于给 `RA/EFSM` 找到一条真正可扩展的主动学习路线。作者把经典 `L*` 对普通字母表的 prefix/suffix 思想推广到带数据参数的交互系统，用 symbolic decision trees (`SDT`) 和 tree queries 去代替简单 membership queries，从而避免直接枚举无限或巨大数据域。

- 形式主义定位：`RA/EFSM` 学习方法路线，而不是新的离散状态机母型。
- 构造方式简述：`SUL -> tree queries / symbolic suffixes -> SDT -> symbolic Nerode equivalence -> canonical RA hypothesis`。
- 基础设施与场景简述：依托 data words、parameterized symbols、guards、assignments、tree oracle 与 black-box testing，服务带数据参数的协议、API 和交互式软件组件模型恢复。

```text
dataful black-box system -> tree queries -> SDT / prefix classes -> register automaton hypothesis -> equivalence-style refinement
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. data words 与 data languages；
2. register automata (`RA`)；
3. symbolic decision trees (`SDT`)；
4. canonical tree oracles；
5. symbolic Nerode equivalence 与 `SL*` learning loop。

### 核心抽象

论文直接把 `RA` 定义成：

$$
A = (L, l_0, X, \Gamma, \lambda)
$$

上式中的符号逐项解释如下：

1. `$L$` 是有限 location 集合。
2. `$l_0$` 是初始 location。
3. `$X$` 为每个 location 指定可见 registers 集合。
4. `$\Gamma$` 是有限迁移集合。
5. `$\lambda : L \to \{+,-\}$` 给出接受/拒绝标记。

单条迁移写成：

$$
\langle l,\ \alpha(p),\ g,\ \pi,\ l' \rangle
$$

上式中的符号逐项解释如下：

1. `$l$` 与 `$l'$` 是源和目标 location。
2. `$\alpha(p)$` 是带形式参数 `$p$` 的动作符号。
3. `$g$` 是关于 `$p$` 与 registers 的 guard。
4. `$\pi$` 是寄存器并行赋值。
5. 这正是原文 `RA` 的核心结构。

论文把 tree query 的返回对象压成：

$$
O_L(u, V) = T
$$

上式中的符号逐项解释如下：

1. `$L$` 是待学习的 data language。
2. `$u$` 是当前前缀 data word。
3. `$V$` 是 symbolic suffix 集合。
4. `$T$` 是返回的 `(u,V)`-tree，也就是一个 `SDT`。
5. `SDT` 用来总结“在前缀 `$u$` 之后，哪些数据关系会改变接受性”。

符号化 Nerode 等价可写成：

$$
u \equiv_{O_L} u' \iff O_L(u,V) \simeq_\gamma O_L(u',V)
$$

上式中的符号逐项解释如下：

1. `$u$` 与 `$u'$` 是两个前缀 data words。
2. `$O_L(u,V)$` 与 `$O_L(u',V)$` 是对应的 `SDT`。
3. `$\simeq_\gamma$` 表示在寄存器重命名 `$\gamma$` 下树同构。
4. 这就是 `SL*` 收敛与 canonical automata construction 的基础。

### 一个最小例子与通俗解释

论文中的水泵例子很适合说明这类模型：

1. 输入动作是 `level(p)`，参数 `$p$` 表示液位值。
2. 状态机在一个 location 中记录上一次液位值到寄存器 `$x_1$`。
3. 如果当前 `$p < x_1$`，就走“液位下降”分支；如果 `$x_1 \le p$`，就走“液位上升或不降”分支。
4. 学习器不会关心这次输入是 `2`、`4` 还是 `17` 本身，而是关心“它和寄存器中的旧值是什么关系”。

通俗地说，这篇论文学到的不是“一个输入字母序列”，而是“一个输入值相对于历史值满足什么关系时该怎么走”。这正是 `EFSM/RA` 相比普通 `FSM` 多出来的关键表达力。

### 运行 / 接受 / 转移语义

论文给出的 `RA` 步进语义可以直接写成：

$$
\langle l,\nu \rangle \xrightarrow{\alpha(d)} \langle l',\nu' \rangle
$$

上式中的符号逐项解释如下：

1. `$\nu$` 与 `$\nu'$` 是 registers 的 valuation。
2. 输入符号是带具体数据值 `$d$` 的 `$\alpha(d)$`。
3. 只有当 `$d$` 在 valuation `$\nu$` 下满足 guard `$g$` 时，迁移才可触发。
4. 触发后按赋值 `$\pi$` 更新 registers，得到新 valuation `$\nu'$`。

论文把语言接受性写成：

$$
L(A) = \{ w \mid A \text{ accepts } w \}
$$

其中：

1. `$A$` 是 simple register automaton。
2. `$w$` 是 data word。
3. 接受与拒绝由 run 结束时 location 的 `$\lambda$` 标记决定。

### 语义边界

1. 论文学的是 `RA` 风格的 dataful state machine，不是工业 `EFSM` 所有变体。
2. 关键关系主要是 theory `$R$` 中允许的关系，而不是任意算术程序语义。
3. 它依赖可查询的 black-box system，不适合纯文档驱动建模。
4. 主体不讨论时间、层次与并发控制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RA` 骨架 | `$A = (L, l_0, X, \Gamma, \lambda)$` | 给 `EFSM/RA` 学习提供正式目标对象。 |
| 单条迁移 | `$\langle l,\alpha(p),g,\pi,l' \rangle$` | guard 与 assignment 是数据化状态机的核心。 |
| 步进语义 | `$\langle l,\nu \rangle \xrightarrow{\alpha(d)} \langle l',\nu' \rangle$` | 数据值如何触发 guard 并更新寄存器。 |
| tree query | `$O_L(u, V) = T$` | 用 `SDT` 汇总前缀后的数据区分结构。 |
| symbolic Nerode | `$u \equiv_{O_L} u' \iff O_L(u,V) \simeq_\gamma O_L(u',V)$` | 这是 canonical `RA` construction 的基础。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | location / transition 仍是离散自动机骨架。 |
| 事件 / 触发 | 很强 | parameterized actions 是直接输入单位。 |
| 守卫 / 数据 | 很强 | registers、guards、assignments 是全文主线。 |
| 层次 | 不支持 | 主体不是层次状态机学习。 |
| 并发 / 同步 | 不支持 | 目标是单个 data language / protocol 行为。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 dataful learning。 |
| 可执行 / 可验证性 | 中等支持 | 有完整学习算法与 benchmark，但原文不提供成熟独立工具包。 |

### 形式化问题与性质

1. 论文真正补出的，是 `RA/EFSM` 这类带数据守卫的状态机“如何被主动学出来”。
2. `SDT + tree oracle` 是区别于普通 observation table 学习的核心。
3. 这条线直接通向后来的 `RALib`、tree-based `RA` learning 与 grey-box dataful learning。

## 构造方式与承载格式

### 建模入口

原文中的典型入口包括：

1. data words 与 parameterized symbols；
2. guards、assignments 与 registers；
3. symbolic suffix 集合；
4. tree queries 与 equivalence-style refinement。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `RA` transitions；
2. `SDT` trees；
3. canonical tree-oracle answers；
4. prefix classes 与 hypothesis automata。

### 交换与互操作

这篇论文的互操作重点不在文件标准，而在学习流程分层：

1. membership-like information 被压成 `SDT`。
2. prefix classes 通过 tree isomorphism 合并或拆分。
3. 最终再回落成 `RA/EFSM` 风格 hypothesis。

## 配套基础设施

- 建模/编辑工具：原文不提供图形建模器；主体是学习算法与 benchmark 工作流。
- 解析/交换/元模型支持：data words、register automata、symbolic decision trees、tree-oracle interface。
- 仿真/执行支持：需要可查询的 black-box system 作为被学习对象。
- 验证/分析支持：核心是 tree queries、equivalence-style refinement、canonical automata construction 与 benchmark evaluation。
- 代码生成/转换支持：原文不涉及代码生成。
- 标准化或社区生态：更适合作为后续 `LearnLib / RALib / Tomte` 工具线的理论与方法锚点。

## 适用场景与需求前提

### 适用场景

适合带数据参数的协议、服务 API、网络交互组件，以及任何核心行为依赖“当前输入值与历史值关系”的黑盒系统模型恢复。

### 需求前提

1. 系统必须可通过 queries 交互。
2. 数据关系应主要落在有限 theory 可表达的 guards 上。
3. 目标模型比普通 `FSM` 更强，但又不至于需要完整程序语义。
4. 若要有效学习，系统通常还需要可重置、可重复试验。

### 不适用或高成本场景

若系统大量依赖复杂数值计算、dense time、并发共享状态或不可重置执行环境，这条 `RA/EFSM` 学习路线会迅速变贵。

## 与相邻形式主义的关系

相对 [learning-extended-finite-state-machines/desc.md](../learning-extended-finite-state-machines/desc.md)，这篇论文是更完整的 journal 版，明确补出了 canonical tree oracle、symbolic Nerode equivalence 与收敛证明；相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 更像通用基础设施，而本文专门推进 dataful `RA/EFSM` 学习；相对 [scalable-tree-based-register-automata-learning/desc.md](../scalable-tree-based-register-automata-learning/desc.md)，后者是在这条 `SDT` 主线上继续做 classification-tree 化和可扩展性优化。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机自动建模”并不只有从需求正向生成一条路，也可以从已有实现反推，尤其是带 guards 与 assignments 的 `EFSM`。
2. 对控制软件需求来说，很多行为约束本身就是“当前值是否等于上次值”“参数是否满足某种关系”，普通 `FSM` 不够，而 `RA/EFSM` 很相关。
3. 如果后续要做“生成模型 vs 真实系统”的闭环比对，这类 dataful learning 是重要旁证。

### 局限

1. 主线离时间、层次和并发控制都比较远。
2. 它依赖可执行查询，不适合只靠需求文档直接补模。

## 重要的相关工作

1. [learning-extended-finite-state-machines/desc.md](../learning-extended-finite-state-machines/desc.md)：同一路线的 conference 版本。
2. [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：更通用的主动自动机学习基础设施。
3. [scalable-tree-based-register-automata-learning/desc.md](../scalable-tree-based-register-automata-learning/desc.md)：这条 `RA` 学习路线的后续 tree-based 扩展。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Register Automata / EFSM learning / symbolic decision trees / tree oracles`
- 论文角色：journal-level `RA/EFSM` active-learning route with symbolic decision trees and canonical tree oracles
- 归类理由：论文主体是在 `RA/EFSM` 目标上建立主动学习方法、`SDT` 数据结构和 canonical tree-oracle 语义，典型属于数据化状态机学习方法路线条目。
