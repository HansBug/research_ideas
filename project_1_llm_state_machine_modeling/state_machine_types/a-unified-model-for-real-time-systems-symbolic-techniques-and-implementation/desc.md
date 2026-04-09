# 面向实时系统的统一模型：符号技术与实现 / A Unified Model for Real-Time Systems: Symbolic Techniques and Implementation

## 基本信息

- 标题：A Unified Model for Real-Time Systems: Symbolic Techniques and Implementation
- 中文标题：面向实时系统的统一模型：符号技术与实现
- 作者：S. Akshay，Paul Gastin，R. Govind，Aniruddha R. Joshi，B. Srivathsan
- 发表：*Computer Aided Verification*，pp. 266-288，2023
- DOI：`10.1007/978-3-031-37706-8_14`
- 链接：https://doi.org/10.1007/978-3-031-37706-8_14
- 形式主义：`generalized timed automata / history clocks / future clocks / GTA`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：unified timed-model and symbolic-reachability route with prototype implementation
- 工具/实现获取方式：原文明确说明把算法做成了 `Tchecker` 上的 prototype implementation，并扩展了 open-source `Tchecker`；当前提取文本未保留独立仓库 URL。
- 标准/格式获取方式：核心承载是 GTA 语法、history / future clocks、instantaneous timed programs 与 `Tchecker` 上的扩展输入；它不是通用交换标准。

## 简报

这篇论文补的是 timed-verification 里很少见的一条“统一建模母线”。经典 timed automata、event-clock automata 和 automata with timers 往往各有各的语义与算法，工具支持也不均衡。本文提出 generalized timed automata (`GTA`)，把普通 clocks、event-recording clocks、prophecy clocks 和 timers 都统一到 history clocks / future clocks 两类变量里，再给出带 simulation 的 zone-based reachability algorithm，并做了 `Tchecker` 原型实现。

- 形式主义定位：面向多类 real-time models 的统一 timed-automata 变体与 reachability 方法，而不是单纯工具包装。
- 构造方式简述：先把模型写成 history / future clocks 上的 `GTA`，再用 zones、distance graphs 与 simulation 做 symbolic enumeration，并在 safe subclass 上保证终止。
- 基础设施与场景简述：依托 `GTA` 统一语法、safe-GTA 限制、zone graph、simulation preorder 与 `Tchecker` prototype，服务 `TA`、`ECA`、timers 和 event-clock specifications 的统一分析。

```text
timed model with clocks / event-clocks / timers -> GTA -> zone graph + simulation -> finite symbolic reachability on safe subclass
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. history clocks 与 future clocks；
2. 带 diagonal constraints 的 clock constraints；
3. instantaneous timed programs；
4. generalized timed automata (`GTA`)；
5. `XD`-safe GTA 与 zone-based reachability algorithm。

### 核心抽象

论文首先把时钟集合分为两类：

$$
X = X_H \cup X_F
$$

上式中的符号逐项解释如下：

1. `X_H` 是 history clocks，取值非负并随时间增加。
2. `X_F` 是 future clocks，取值非正并只能增加到 `0`。
3. history clocks 可统一普通 clocks 与 event-recording clocks。
4. future clocks 可统一 timers 与 event-predicting clocks。

约束语法写成：

$$
\varphi ::= x - y \triangleleft c \mid \varphi \land \varphi
$$

上式中的符号逐项解释如下：

1. `x,y \in X \cup \{0\}`，其中 `0` 是常量时钟。
2. `\triangleleft` 取自 `\le,<`。
3. `c` 是整数权值。
4. 当 `x,y \neq 0` 时，这就是 diagonal constraint。

论文直接给出 valuation 定义：

$$
v : X \cup \{0\} \to \overline{\mathbb{R}}
$$

上式中的符号逐项解释如下：

1. `v(0)=0`。
2. history clocks 映到 `\mathbb{R}_{\ge 0} \cup \{+\infty\}`。
3. future clocks 映到 `\mathbb{R}_{\le 0} \cup \{-\infty\}`。
4. `+\infty / -\infty` 还承担“未定义 / inactive”标记作用。

最核心的模型元组是：

$$
A = (Q, \Sigma, X, \Delta, (q_0,g_0), (Q_f,g_f))
$$

上式中的符号逐项解释如下：

1. `Q` 是离散控制位置集合。
2. `\Sigma` 是动作字母表。
3. `X = X_H \cup X_F` 是时钟集合。
4. `\Delta \subseteq Q \times \Sigma \times Programs \times Q` 是带 instantaneous timed programs 的离散转移。
5. `(q_0,g_0)` 给出初始位置与初始 guard。
6. `(Q_f,g_f)` 给出接受位置集合与终止 guard。

### 一个最小例子与通俗解释

论文第一页的图给了一个很直观的对照：

1. 左边普通 timed automaton 用普通 clock `x` 表示“距离上一次动作已经过了多久”。
2. 右边 timer automaton 用 timer `t_x` 表示“距离 timeout 还有多久”。
3. 两者都能表达“相邻动作间隔恰好为 `1`”。
4. `GTA` 的统一视角是：前者属于 history-clock 建模，后者属于 future-clock 建模。

通俗地说，`GTA` 把“向前记过去多久”和“向后记还剩多久”放进了同一个时钟语义里。这样同一套 zone machinery 就有机会同时服务 timed automata、event-clock automata 和 timers。

### 运行 / 接受 / 转移语义

论文先定义 instantaneous timed programs：

$$
prog ::= guard \mid change \mid prog ; prog
$$

上式中的符号逐项解释如下：

1. `guard` 是一条时钟约束 `g \in \Phi(X)`。
2. `change = [R]` 表示对 `R \subseteq X` 中的时钟做 reset 或 release。
3. `prog ; prog` 表示原子 guard 与 change 的顺序组合。
4. 这比普通 `TA` 的“单 guard + 单 reset”更一般。

程序语义被统一成 valuation 关系：

$$
v \xrightarrow{prog} v'
$$

上式中的符号逐项解释如下：

1. 若 `prog` 是 guard，则要求 `v \models g` 且 `v'=v`。
2. 若 `prog` 是 `[R]`，则对 history clocks 做 reset、对 future clocks 做 release。
3. 若 `prog = prog_1 ; prog_2`，则中间存在某个 `v''` 使两段语义顺序成立。
4. 这使 guard 与 release/reset 可以被统一推理。

`GTA` 的 transition-system semantics 也由论文直接给出：

$$
(q,v) \xrightarrow{\delta} (q, v+\delta), \quad (q,v) \xrightarrow{t} (q',v')
$$

上式中的符号逐项解释如下：

1. 第一种是 delay transition，要求 future clocks 在时间流逝后仍不超过 `0`。
2. 第二种是 discrete transition，其中 `t=(q,a,prog,q') \in \Delta` 且 `v \xrightarrow{prog} v'`。
3. run 从满足 `g_0` 的初始配置出发。
4. 最后配置满足 `q \in Q_f` 且 `v \models g_f` 时接受。

### 语义边界

1. 论文明确证明 unrestricted `GTA` reachability 不可判定。
2. 真正可算法化的是 `XD`-safe `GTA` 子类。
3. 其可判定性关键在于限制“参与 diagonal constraints 的 future clocks”与“arbitrary release”之间的组合。
4. 这条边界比普通 `TA` 更宽，但也不是无条件任意扩展。

`XD`-safe 的关键条件可直接整理为：

$$
x-y \triangleleft c \text{ with } x,y \in X_F \Rightarrow x,y \in X_D
$$

以及

$$
x \in X_D \cap R_i \Rightarrow (x = 0) \lor (x = -\infty) \text{ occurs in } g_i
$$

上式中的符号逐项解释如下：

1. `X_D \subseteq X_F` 是允许参与 future-future diagonal constraints 的 future clocks 子集。
2. 若某个 `X_D` 中的时钟要被 release，则 release 前必须先被检查为 `0` 或 `-\infty`。
3. 这是 safe subclass 的核心限制。
4. 论文据此得到 `XD`-safe GTA 的 decidable reachability。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 时钟分区 | `$X = X_H \cup X_F$` | 统一普通 clocks、recording clocks、timers 和 prophecy clocks。 |
| 约束语法 | `$\varphi ::= x-y \triangleleft c \mid \varphi \land \varphi$` | 直接容纳 diagonal constraints。 |
| 模型元组 | `$A = (Q,\Sigma,X,\Delta,(q_0,g_0),(Q_f,g_f))$` | `GTA` 的正式定义。 |
| 程序语义 | `$v \xrightarrow{prog} v'$` | guard、reset、release 统一进同一关系。 |
| safe 条件 | `$x \in X_D \cap R_i \Rightarrow (x=0)\lor(x=-\infty)$` | 防止 future diagonal + arbitrary release 造成不可判定。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍保留 automata 风格位置与离散转移。 |
| 事件 / 触发 | 很强 | 离散动作字母表 `\Sigma` 是显式对象。 |
| 守卫 / 数据 | 很强 | 支持一般 clock constraints 与 diagonal constraints。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 弱支持 | 主体是单 automaton 语义与 symbolic reachability。 |
| 时间约束 | 很强 | 统一 clocks、timers、event-clocks 与 diagonal constraints。 |
| 连续动态 / 随机性 | 不支持 | 这是纯实时时钟模型，不是 hybrid / stochastic extension。 |
| 可执行 / 可验证性 | 很强 | 给出了 terminating symbolic algorithm 与 `Tchecker` prototype。 |

### 形式化问题与性质

1. 论文的关键贡献不只是统一建模，还包括在这个统一模型上保留有效的 zone-based algorithm。
2. 它第一次把 event-clock diagonals 和 timers 直接放进同一有效实现路线里。
3. 对 `project_1` 而言，这类 unified timed backend 很适合接住未来 richer timed state-machine 变体。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. history / future clocks 的声明；
2. initial / final guards；
3. instantaneous timed programs；
4. `Tchecker` 扩展输入。

### 机器可处理承载方式

机器可处理承载方式包括：

1. GTA zones；
2. distance graphs；
3. simulation preorder；
4. `Tchecker` 扩展前端；
5. safe-subclass reachability search。

### 交换与互操作

这篇论文的互操作重点在：

1. 把 `TA`、`ECA` 和 timers 统一降到 `GTA`；
2. 算法与实现都落在 `Tchecker` 生态上；
3. event-clock specifications over timed automata 也可借由统一模型进入同一 reachability pipeline。

## 配套基础设施

- 建模/编辑工具：核心是 `Tchecker` 上的扩展输入，不主打独立 GUI。
- 解析/交换/元模型支持：支持 GTA、zones、distance graphs 与 simulation-based symbolic search。
- 仿真/执行支持：重点是 reachability checking，不是执行仿真环境。
- 验证/分析支持：zone graph、simulation、distance-graph operations、safe-GTA decidability。
- 代码生成/转换支持：没有部署代码生成；重点是 symbolic backend。
- 标准化或社区生态：与 `Tchecker`、timed-automata symbolic verification 社区和 `ECA` / timers 理论线直接衔接。

## 适用场景与需求前提

### 适用场景

适合需要在同一模型与算法框架下同时处理普通 clocks、event-clocks、timers 和 diagonal constraints 的实时验证任务。

### 需求前提

1. 系统核心仍应是 finite-state + real-time clocks 的组合。
2. 若要保证终止，模型应落在 `XD`-safe subclass 或其邻近可约简片段。
3. 用户愿意接受 symbolic reachability 而不是只依赖 translation 到普通 `TA`。
4. 如果模型需要 event-clock specification over timed models，这条统一路线尤其有价值。

### 不适用或高成本场景

若系统包含无界数据、复杂博弈或连续动力学主导，`GTA` 不是直接目标；若大量使用 unrestricted future-diagonals 与 arbitrary release，则会触碰不可判定边界。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文不是替代 `TA`，而是向上统一 `TA`、`ECA` 与 timers；相对 [reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md](../reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md)、[configurable-verification-of-timed-automata-with-discrete-variables/desc.md](../configurable-verification-of-timed-automata-with-discrete-variables/desc.md) 和 [fast-zone-based-algorithms-for-reachability-in-pushdown-timed-automata/desc.md](../fast-zone-based-algorithms-for-reachability-in-pushdown-timed-automata/desc.md)，这些条目补的是特定 timed backend 变体，本文补的是统一 timed mother model；相对 [survey-of-timed-automata-for-real-time-systems/survey.md](../survey-of-timed-automata-for-real-time-systems/survey.md)，survey 盘点变体，本文给出了一条实际统一实现路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“时间状态机”不一定要分裂成一堆互不兼容的小家族，后端完全可以寻求统一建模与统一验证。
2. 对后续 timed-profile verification，这种 unified backend 很有参考价值。
3. 若 `project_1` 以后需要承载 timeout、预测时钟和 richer temporal constructs，这篇文章提供了结构化落点。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像 richer timed verification backend，同时也可以看作 timed state-machine family 的扩展目标形式主义。

### 对需求到模型生成的启发

1. 需求建模阶段可以区分“记录已经过了多久”和“离下一次事件还剩多久”两类时间信息。
2. 统一后端比为每类 timed variant 各写一套验证桥接更稳。
3. safe-subclass 的思想也提醒前端建模要主动规避不可判定组合。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：经典 timed automata 母线。
- [reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md](../reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md)：`TChecker` 近邻 timed backend 路线。
- [configurable-verification-of-timed-automata-with-discrete-variables/desc.md](../configurable-verification-of-timed-automata-with-discrete-variables/desc.md)：更现代的 timed abstraction framework。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇很强的 unified timed-backend 条目，适合作为 history / future clocks、safe-GTA 边界与统一 zone-based reachability 实现路线的正式证据入账。
