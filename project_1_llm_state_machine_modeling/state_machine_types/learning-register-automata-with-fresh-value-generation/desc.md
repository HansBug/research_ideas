# 学习可生成新鲜值的寄存器自动机 / Learning Register Automata with Fresh Value Generation

## 基本信息

- 标题：Learning Register Automata with Fresh Value Generation
- 中文标题：学习可生成新鲜值的寄存器自动机
- 作者：Fides Aarts，Paul Fiterau-Brostean，Harco Kuppens，Frits Vaandrager
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 9035`，pp. 165-183，2015
- DOI：`10.1007/978-3-319-25150-9_11`
- 链接：https://doi.org/10.1007/978-3-319-25150-9_11
- 形式主义：`register automata learning / Tomte / fresh outputs`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：fresh-output register-automata learning method and `Tomte` tool route
- 工具/实现获取方式：原文明确给出 `Tomte` 入口 `http://tomte.cs.ru.nl/`，并说明实现可接 `LearnLib` 的 `Mealy` learner；实验部分系统对比 `RALib`。
- 标准/格式获取方式：主承载是 data words、`RA` 元组、mapper、`MQ/EQ` 查询和抽象反例；不是中立交换标准。

## 简报

这篇论文补的是 `register automata` 学习里非常关键的一步：让学习算法不仅能处理 equality-based 数据守卫，还能处理“系统返回一个此前从未出现过的新值”这种真实系统里常见但更难的行为。作者用 counterexample-guided abstraction refinement 自动构造 mapper，把巨大数据动作空间压成有限抽象动作，再交给 `Mealy` learner，从而让 `Tomte` 可以学习带 fresh outputs 的 `RA`。

- 形式主义定位：围绕 `register automata` 的主动学习方法路线，而不是新的 `RA` 母型。
- 构造方式简述：`SUL` 与 learner 之间放置 history-dependent mapper；反例出现后再自动细化 mapper 和抽象字母表。
- 基础设施与场景简述：依托 `Tomte`、`LearnLib`、`TTT` / Observation Pack、`MQ/EQ` 查询和 benchmark，对接带 fresh passwords / identifiers / sequence numbers 的系统。

```text
SUL with data + fresh outputs -> history-dependent mapper -> abstract Mealy learning -> counterexample-guided refinement -> register automaton hypothesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. register automata (`RA`)；
2. `RA` 的 `Mealy`-style operational semantics；
3. mapper-based abstraction；
4. fresh outputs；
5. `Tomte` 的 `CEGAR` learning loop。

### 核心抽象

论文直接给出寄存器自动机的定义：

$$
R = \langle I, O, L, l_0, V, \to \rangle
$$

上式中的符号逐项解释如下：

1. `$I$` 和 `$O$` 分别是有限的输入符号集与输出符号集。
2. `$L$` 是 location 集合，`$l_0 \in L$` 是初始 location。
3. `$V$` 为每个 location 指派一组 registers。
4. `$\to$` 是带输入、守卫、更新和输出的迁移关系。

论文把 `RA` 的操作语义定义成一个无限状态 `Mealy` 机：

$$
[[R]] = \langle I \times \mathbb{Z}, O \times \mathbb{Z}, Q, q_0, \Rightarrow \rangle
$$

上式中的符号逐项解释如下：

1. `$I \times \mathbb{Z}$` 与 `$O \times \mathbb{Z}$` 表示“动作标签 + 数据值”的输入输出动作。
2. `$Q$` 是由 location 与寄存器赋值组成的状态集合。
3. `$q_0$` 是初始语义状态。
4. `$\Rightarrow$` 是由 `RA` 迁移和寄存器更新诱导出的 `Mealy` 迁移关系。

论文给出的单步语义可保守整理为：

$$
(l,\xi) \xrightarrow{i(d)/o(e)} (l', \xi')
\quad \text{if} \quad
l \xrightarrow{i, g, \rho, o} l',\ \xi[in \mapsto d, out \mapsto e] \models g,\ \xi' = (\xi[in \mapsto d, out \mapsto e]) \circ \rho
$$

上式中的符号逐项解释如下：

1. `$\xi$` 是当前寄存器赋值。
2. `$i(d)$` 是带数据值 `$d$` 的输入动作。
3. `$o(e)$` 是带数据值 `$e$` 的输出动作。
4. `$g$` 是当前迁移守卫。
5. `$\rho$` 是更新函数，它把新 location 的寄存器绑定到旧寄存器或当前输入/输出变量上。
6. `$\xi'$` 是执行更新后的新寄存器赋值。

### 一个最小例子与通俗解释

论文里很适合做最小例子的，是带“注册-登录”的 fresh-password 系统：

1. 用户发出 `Register`。
2. 系统返回 `OK(password)`，其中 `password` 是一个新鲜值。
3. 之后只有输入 `Login(password)` 才能成功。
4. 若输入旧密码、陌生密码或与历史值冲突的值，则转到失败输出。

通俗地说，这类系统难点不在“状态多”，而在“系统会临时创造新数据值”。`Tomte` 的 mapper 正是在做这件事：把无限多真实值归纳成“是旧值 / 新值 / 与哪个寄存器相等”之类有限抽象，再在这个抽象空间里学习。

### 运行 / 接受 / 转移语义

论文把学习问题拆成“有限抽象 `Mealy` 学习 + 抽象细化”两层。其核心接口可压成：

$$
\mathrm{MQ}(w), \qquad \mathrm{EQ}(H)
$$

上式中的符号逐项解释如下：

1. `$\mathrm{MQ}(w)$` 询问抽象字 `$w$` 是否被当前系统行为允许。
2. `$\mathrm{EQ}(H)$` 询问当前假设机 `$H$` 是否已与目标系统等价。
3. 由于真实系统带数据值，`Tomte` 先通过 mapper 把 concrete trace 映到 abstract trace，再把查询交给 `Mealy` learner。

mapper 的本质可保守写成：

$$
\alpha_h : \Sigma_{\mathrm{concrete}}^{*} \to \Sigma_{\mathrm{abstract}}^{*}
$$

上式中的符号逐项解释如下：

1. `$\alpha_h$` 是历史相关的抽象映射。
2. `$\Sigma_{\mathrm{concrete}}$` 是真实系统的数据动作字母表。
3. `$\Sigma_{\mathrm{abstract}}$` 是有限抽象动作字母表。
4. fresh output 的处理正是通过不断细化 `$\alpha_h$` 来完成的。

### 语义边界

1. 论文核心是 learning route，不是新的 `RA` 理论边界论文。
2. 重点数据理论仍然接近 equality / freshness，而不是复杂算术约束。
3. 需要可查询、可复位的 `SUL`，并不适合完全被动日志学习。
4. fresh outputs 是亮点，但也引入了 mapper refinement 成本。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RA` 元组 | `$R = \langle I, O, L, l_0, V, \to \rangle$` | 论文采用的目标模型。 |
| 操作语义 | `$[[R]] = \langle I \times \mathbb{Z}, O \times \mathbb{Z}, Q, q_0, \Rightarrow \rangle$` | 把 `RA` 看成带数据的 `Mealy` 机。 |
| 单步语义 | `$(l,\xi) \xrightarrow{i(d)/o(e)} (l', \xi')$` | 守卫与更新如何作用到寄存器。 |
| 学习接口 | `$\mathrm{MQ}(w), \mathrm{EQ}(H)$` | `Tomte` 与 `Mealy` learner 的基本交互。 |
| 抽象映射 | `$\alpha_h : \Sigma_{\mathrm{concrete}}^{*} \to \Sigma_{\mathrm{abstract}}^{*}$` | 无限数据动作被压缩到有限抽象动作空间。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 学习目标就是带 location 和寄存器的 `RA`。 |
| 事件 / 触发 | 很强 | 输入输出动作都带参数。 |
| 守卫 / 数据 | 很强 | equality guard、fresh outputs、寄存器更新是全文主轴。 |
| 层次 | 不支持 | 不面向层次状态机。 |
| 并发 / 同步 | 弱支持 | 主要讨论单 `SUL` 的交互学习。 |
| 时间约束 | 不支持 | 不是 timed-learning 路线。 |
| 连续动态 / 随机性 | 不支持 | 纯离散数据语言学习。 |
| 可执行 / 可验证性 | 很强 | 已在 `Tomte` 工具中实现，并与 `RALib` 做系统对比。 |

### 形式化问题与性质

1. 论文真正解决的是“如何在主动学习中处理 fresh outputs”，而不是仅仅再换一个 query 策略。
2. mapper 是核心，因为真实数据动作空间无限，而 `Mealy` learner 只能处理有限字母表。
3. `TTT` 的引入进一步减少了查询数，使 `Tomte` 对复杂 benchmark 更稳。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 可执行 `MQ/EQ` 风格查询的 `SUL`；
2. data words；
3. history-dependent mapper；
4. `Mealy` learner 与反例分析器。

### 机器可处理承载方式

机器可处理承载方式包括：

1. concrete data traces；
2. abstract action traces；
3. `RA` 元组与寄存器赋值；
4. mapper refinement data structures。

### 交换与互操作

1. `Tomte` 通过 mapper 在真实系统与 `LearnLib` 的有限字母表学习器之间搭桥。
2. 反例分析会决定是补新抽象还是扩现有抽象类别。
3. 论文主要强调学习流程接口，而不是独立文件标准。

## 配套基础设施

- 建模/编辑工具：不是图形建模器，核心是 `Tomte` 学习工具。
- 解析/交换/元模型支持：data traces、abstract traces、mapper 与 `RA` hypothesis。
- 仿真/执行支持：通过 `MQ/EQ` 驱动 `SUL`，并借助 `Mealy` learner 进行交互。
- 验证/分析支持：counterexample analysis、abstraction refinement、benchmark comparison with `RALib`。
- 代码生成/转换支持：不主打部署代码生成，重点是恢复可分析的 `RA` 模型。
- 标准化或社区生态：`Tomte` 与 `LearnLib / RALib` 生态紧密相关，是 dataful automata learning 工具线的重要一环。

## 适用场景与需求前提

### 适用场景

适合登录协议、认证接口、会话管理、分配新标识符的服务、以及其他需要显式建模 freshness 的 `API / protocol` 行为恢复场景。

### 需求前提

1. 系统必须可重置并可执行主动查询。
2. 关键行为需能压成 data words。
3. 数据关系最好主要落在 equality / freshness 范围内。
4. 团队接受 learning + refinement loop 的额外查询成本。

### 不适用或高成本场景

若系统是纯被动日志、无法查询，或者数据语义依赖复杂算术与跨对象约束，`Tomte` 这条路会明显变难。

## 与相邻形式主义的关系

相对 [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md)，本文重点不是演示 `LearnLib` 工作流，而是解决 fresh outputs；相对 [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)，后者强调 white-box information 融合，这篇更强调 mapper-based abstraction refinement；相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 是通用基础设施，而 `Tomte` 是针对 `RA` 尤其 fresh-output `RA` 的专门学习路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明对带变量、带新值生成的控制逻辑，纯静态建模之外还可以用主动学习回收结构证据。
2. fresh outputs 对需求建模特别有启发，因为很多真实控制/协议系统都会分配新标识符或临时句柄。
3. mapper + refinement 的分层设计，非常适合迁移到“生成 - 验证 - 修复”闭环里。

### 作为目标形式主义还是中间表示

更适合作为行为恢复、对照验证和修复反馈的中间表示，而不是最终面向工程师的前端建模语言。

### 对需求到模型生成的启发

1. 如果目标系统存在 freshness 语义，LLM 生成模型时不能只写 equality guards。
2. 反例不应只被记录为失败样本，还应该触发抽象层级本身的修正。
3. 把 concrete trace 与 abstract trace 显式分层，会显著改善后续修复与解释性。

## 重要的相关工作

1. [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md)：较早的 `RA` 学习 workflow 演示。
2. [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)：将 white-box 结构信息并入 `RA` 学习的路线。
3. [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：更广义的主动自动机学习基础设施。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`register automata learning / Tomte / fresh outputs`
- 论文角色：fresh-output register-automata learning method and `Tomte` tool route
- 归类理由：论文主体是带 fresh outputs 的 `RA` 学习方法与 `Tomte` 实现，核心贡献落在 mapper refinement 和主动学习流程，而不是新的工具标准或新的 automata 本体。
