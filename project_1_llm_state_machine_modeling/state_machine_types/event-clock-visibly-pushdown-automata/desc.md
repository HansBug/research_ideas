# 事件时钟可见下推自动机 / Event-Clock Visibly Pushdown Automata

## 基本信息

- 标题：Event-Clock Visibly Pushdown Automata
- 中文标题：事件时钟可见下推自动机
- 作者：Nguyen Van Tang、Mizuhito Ogawa
- 发表：*SOFSEM 2009: Theory and Practice of Computer Science*, pp. 558-569, 2009
- DOI：`10.1007/978-3-540-95891-8_50`
- 链接：https://www.jaist.ac.jp/~mizuhito/papers/conference/SOFSEM09.pdf
- 形式主义：`Event-Clock Visibly Pushdown Automata (ECVPA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 pushdown alphabet 分区、event-clock constraint、`ECVPA` 元组以及到 untimed `VPA` 的互译。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `ECVPA` 的 location/stack/transition tuple 与 timed-word 语义。

## 简报

这篇论文把两条经典主线接到了一起：一条是 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md) 的 `Event-Clock Automata`，另一条是 [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md) 的 `Visibly Pushdown Automata`。结果得到的 `ECVPA` 既能表达带 call / return 的 timed structured words，又保住了 determinization 和布尔闭包，因此非常适合作为 `timed pushdown` 支线中的可分析 specification family。

- 形式主义定位：`Pushdown Timed Automata` 支线上的 event-clock / visible-stack 子类。
- 构造方式简述：先把输入字母分成 call / return / internal 三类，再让边上的时间约束只依赖 event clocks。
- 基础设施与场景简述：核心基础设施是 `ECVPA <-> untimed VPA` 互译、determinization、boolean closure 与 `TVPA ⊆ ECVPA` 方向的 inclusion 判定。

```text
timed structured word -> event clocks + visible stack discipline -> ECVPA -> untimed VPA translation -> boolean closure / inclusion
```

## 形式主义定义与核心对象

### 定义对象

`ECVPA` 面向的是带时间戳、且嵌套结构对输入符号可见的 timed words。也就是说：

1. call 符号必须触发 push。
2. return 符号必须触发 pop。
3. internal 符号不能改动栈。
4. 时间约束来自 event clocks，而不是自由 reset 的局部 clocks。

### 核心抽象

原文给出的 `ECVPA` 元组是：

$$
M = (Q,\Sigma,Q_0,\Gamma,\Delta,F)
$$

其中：

$$
\Delta = \Delta_c \cup \Delta_r \cup \Delta_i
$$

上式中的符号逐项解释如下：

1. `Q` 是有限位置集。
2. `\Sigma` 是 pushdown alphabet，并分成 `\Sigma_c,\Sigma_r,\Sigma_i`。
3. `Q_0\subseteq Q` 是初始位置集。
4. `\Gamma` 是栈字母表，包含栈底符号 `?`。
5. `\Delta_c,\Delta_r,\Delta_i` 分别是 push / pop / internal 转移关系。
6. `F\subseteq Q` 是接受状态集。

其中三类边分别形如：

$$
\Delta_c \subseteq Q\times \Sigma_c \times \Phi(C_\Sigma)\times Q\times(\Gamma\setminus\{?\})
$$

$$
\Delta_r \subseteq Q\times \Sigma_r \times \Phi(C_\Sigma)\times \Gamma\times Q
$$

$$
\Delta_i \subseteq Q\times \Sigma_i \times \Phi(C_\Sigma)\times Q
$$

这里的 `\Phi(C_\Sigma)` 表示 event-clock constraints。

### 一个最小例子与通俗解释

论文给出的典型直觉是：“若过程在某个 call 时被调用，则它必须在 `d` 个时间单位内返回，并且返回点满足某个性质 `q`。”用 `ECVPA` 来写时：

1. 读到 call 时按 visible discipline 把返回标记压栈。
2. 事件时钟记录“距离下一次 return 还有多久”或“距离上一次 call 过去多久”。
3. 当读到 return 时，既检查 event-clock constraint，又弹出栈顶标记。

通俗地说，`ECVPA` 像“给 `VPA` 装上了事件时钟”，这样它仍保留 call / return 的嵌套感知，但时间信息不再来自程序化 reset，而是来自输入本身。

### 运行 / 接受 / 转移语义

原文把配置写成：

$$
(q,\sigma)
$$

上式中的符号逐项解释如下：

1. `q` 是当前位置。
2. `\sigma` 是当前栈内容。

对 timed word `\bar w=(a_0,t_0)\cdots(a_n,t_n)`，一条 run 是配置序列：

$$
\rho=(q_0,\sigma_0)\cdots(q_{n+1},\sigma_{n+1})
$$

并要求：

$$
q_0\in Q_0,\qquad \sigma_0 = ?
$$

若 `a_i` 是 call、return 或 internal，则分别使用 `\Delta_c`、`\Delta_r`、`\Delta_i` 中满足当前 event-clock valuation 的边推进。接受条件是最后位置落在 `F` 中。

### 语义边界

相对普通 `VPA`，它新增 timed constraints；相对普通 `ECA`，它新增 visible stack discipline；相对一般 `TVPA`，它牺牲了一部分表达力，换回 determinization 和布尔闭包。

### 关键性质与判定边界

论文的关键观察是：

$$
\text{every ECVPA can be translated into an untimed VPA}
$$

因此很多性质都可以从 `VPA` 继承回来。可保守整理成：

$$
\text{ECVPA is determinizable and closed under Boolean operations}
$$

并且：

$$
L(A)\subseteq L(B)
$$

在 `A` 是 `TVPA`、`B` 是 `ECVPA` 时可判定。论文还指出 `Duration Automata` 是 `ECVPA` 的特例。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限位置 `Q` 作为控制骨架。 |
| 事件 / 触发 | 强支持 | 输入字母同时决定时间观察对象和栈操作种类。 |
| 守卫 / 数据 | 支持时间守卫 | 守卫来自 `event-clock` 约束。 |
| 层次 | 强支持 | call / return 通过 visible stack 形成嵌套层次。 |
| 并发 / 同步 | 不支持 | 原始模型面向单条 structured timed word。 |
| 时间约束 | 强支持 | 事件时钟是模型核心。 |
| 连续动态 / 随机性 | 不支持 | 无 ODE、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | 通过与 untimed `VPA` 互译恢复 determinization 与 closure。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$M=(Q,\Sigma,Q_0,\Gamma,\Delta,F)$` | 固定 timed visible-pushdown family 的标准骨架。 |
| 分解转移 | `$\Delta=\Delta_c\cup\Delta_r\cup\Delta_i$` | 把 push / pop / internal 三类行为分开。 |
| 配置 | `$(q,\sigma)$` | 有限状态加栈内容。 |
| 互译结论 | `$ECVPA \leftrightarrow$ untimed `VPA`` | closure / determinization 都可回收到 `VPA`。 |
| inclusion 结论 | `$L(TVPA)\subseteq L(ECVPA)$` decidable | 适合作为 timed pushdown 规格语言。 |

## 构造方式与承载格式

### 建模入口

建模时要先决定：

1. 哪些输入符号是 call、return、internal。
2. 哪些时间性质可以写成 event-clock constraints。
3. 是否真的需要一般 `TVPA` 的自由 clocks，还是 `ECVPA` 已够用。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. pushdown alphabet 分区。
2. `ECVPA` tuple。
3. 到 untimed `VPA` 的 timed / untimed translation。

### 交换与互操作

它和 [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md) 的 visible-stack 母线、[event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md) 的 event-clock timed 规格母线，以及本轮新增的 [pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md](../pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md) / [dense-timed-pushdown-automata/desc.md](../dense-timed-pushdown-automata/desc.md) 都直接相连。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 timed-to-untimed translation 和 symbolic timing constraints。
- 仿真/执行支持：可按 timed word 逐符号运行并同步维护栈。
- 验证/分析支持：determinization、boolean closure、inclusion with `TVPA`、`DA` special-case result。
- 代码生成/转换支持：支持转成 untimed `VPA` 分析，但不讨论工程代码生成。
- 标准化或社区生态：属于 timed structured-word verification 的经典理论 family。

## 适用场景与需求前提

### 适用场景

适合带 call / return 结构的 timed-word specification，例如递归程序、嵌套协议和结构化消息流的实时约束。

### 需求前提

1. 嵌套结构必须由输入字母类别显式可见。
2. 时间性质最好能写成事件时钟约束。
3. 更看重可判定 inclusion / complement，而不是最大表达力。

### 不适用或高成本场景

若栈操作不能由输入字母直接决定，则一般 `timed pushdown` 或 `RTA` 更合适；若完全不需要嵌套结构，则普通 `ECA` 已足够。

## 与相邻形式主义的关系

相对 [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)，`ECVPA` 增加了 event-clock timed constraints；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，它增加了 visible stack；相对一般 `timed visibly pushdown automata`，它是表达力更弱但分析性质更好的可确定化子类。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Timed Automata -> Pushdown Timed Automata` 这条新母线继续细化成“可确定化 structured timed-word specification”子枝，而不是只停在一般 timed-pushdown 大类上。

### 作为目标形式主义还是中间表示

很适合作为高层规格形式主义或 verification-oriented 中间表示，而不是直接作为控制器执行模型。

### 对需求到模型生成的启发

若需求文本里显式区分调用、返回和内部事件，并主要写“某类事件前后多久”的约束，LLM 很适合直接生成 `ECVPA`。

### 现实限制

它只能处理 visible stack discipline，无法覆盖所有一般 pushdown timed behavior。

## 重要的相关工作

### 奠基或前身工作

- [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)
- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)

### 同类型或同家族工作

- [pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md](../pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md)
- [dense-timed-pushdown-automata/desc.md](../dense-timed-pushdown-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或工具；最重要的基础设施是与 untimed `VPA` 的互译。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Timed Automata -> Pushdown Timed Automata -> Event-Clock Visibly Pushdown Automata`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
