# 分布式事件时钟自动机 / Distributed Event Clock Automata

## 基本信息

- 标题：Distributed Event Clock Automata
- 中文标题：分布式事件时钟自动机
- 作者：James Ortiz、Axel Legay、Pierre-Yves Schobbens
- 发表：*Implementation and Application of Automata* (CIAA 2011), pp. 250-263, 2011
- DOI：`10.1007/978-3-642-22256-6_23`
- 链接：https://staff.info.unamur.be/jor/DecaReport/DECAVersionExt.pdf
- 形式主义：`Distributed Recursive Event Clock Automata (DECA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程工具；机器可处理入口是 `RECA + process map` 结构、multi-timed semantics、determinization 与 region-based emptiness / inclusion checks。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `RECA` 自动机骨架、局部进程时钟、`ISS` 语义与 process-indexed event clocks。

## 简报

这篇论文要解决的问题很明确：经典 `Timed Automata` 和 `Event-Clock Automata` 都默认“所有时钟完美同步”，但真正的 distributed real-time system 往往只有各进程自己的本地时间。`DECA` 的做法不是回到自由 reset 的一般时钟，而是把 `Recursive Event Clock` 这条 determinizable 规格线改写成“每个 clock 绑定某个 process 的局部时间”，从而在保住布尔闭包和 language inclusion decidability 的前提下，把 event-clock family 推进到 distributed setting。

- 形式主义定位：`Timed Automata` 主干下 `Event-Clock / Recursive Event-Clock` 方向的分布式独立时钟扩展。
- 构造方式简述：先取一个 `RECA`，再给每个 event clock 指定所属进程；语义中每个进程按自己的 local rate 演化。
- 基础设施与场景简述：核心基础设施是 determinization、complementation、`tau`-wise / existential / universal timed languages，以及到 `DECTL` 的逻辑翻译。

```text
event-clock family -> recursive event clocks -> process-indexed independent clocks -> DECA -> decidable inclusion / refinement
```

## 形式主义定义与核心对象

### 定义对象

原文要建模的是“多个进程各自按本地时钟推进，而时间约束仍由可观测事件决定”的 timed languages。相比普通 `TA`，这里最关键的新增结构不是 guard 语言，而是：

1. clock 不再引用全局统一时间；
2. event 的“发生时间”必须按所属 process 的 local time 来解释；
3. 同一个 word 可以在不同 rate assignment 下诱导出不同的 multi-timed semantics。

### 核心抽象

原文 Definition 9 把 `DECA` 写成：

$$
(A,\pi)
$$

上式中的符号逐项解释如下：

1. `A` 是一个 `Recursive Event Clock Automaton (RECA)`。
2. `\pi : C \to Proc` 把每个 event clock 绑定到某个 process。
3. `C` 是 clocks 集合，`Proc` 是进程集合。

也就是说，`DECA` 不是重新发明一套 transition graph，而是在 `RECA` 的 clock 语义外面再包上一层“这个 clock 用谁的 local time 来测量”。

### 一个最小例子与通俗解释

可以把它想成两个进程 `p` 和 `q` 共同观察同一个低层 automaton `B`：

1. `x_B^p` 表示“按进程 `p` 的本地时间看，距离上一次 `B` 接受某监控状态过去了多久”。
2. `x_B^q` 表示同样的事，但计时单位换成进程 `q` 的本地时间。
3. 如果 `q` 的钟走得更快，那么即使两边看到的是同一串离散事件，`x_B^q` 也会更早超出上界。

通俗地说，`DECA` 像“给 event-clock automata 装上多块彼此不同步的本地表”。约束仍然由事件决定，但“距上次事件过了多久”不再是一个全局公共值，而是每个进程各算各的。

### 运行 / 接受 / 转移语义

原文 Definition 10 中，`DECA` 的 run 由状态序列和区间序列组成，并通过 process-local rates `\tau` 来解释 clock valuation。对 recorder clock，原文给出：

$$
\nu(\rho,t,\tau,x_B^q)=
\begin{cases}
\tau_q(t)-\tau_q(r), & r=\max\{s<t \mid (s,\rho)\in L^+(B,\tau)\} \\
(\tau_q(t)-\tau_q(r))^+, & r=\sup\{s<t \mid (s,\rho)\in L^+(B,\tau)\} \\
?, & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `\rho` 是当前运行对应的 `ISS`。
2. `t` 是当前参考时间。
3. `\tau_q` 是进程 `q` 的 local time evolution。
4. `x_B^q` 是“由低层 automaton `B` 决定、并用进程 `q` 局部时间测量”的过去型 event clock。
5. `L^+(B,\tau)` 是 `B` 在 rate assignment `\tau` 下接受的事件时刻集合。

直观上，`DECA` 的 clock 值不是由 automaton 执行时 reset 出来的，而是由“某个低层事件何时发生”以及“某个进程的本地时间如何流逝”共同决定。

### 语义边界

相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，`DECA` 更强，因为它允许 recursive event definitions 和 independent clocks；相对一般 independent-clock timed automata (`icTA`)，它又更受限，因为 clock 仍必须由 event semantics 决定，而不是自由 reset。

### 关键性质与判定边界

原文的核心正结果是：

$$
\text{DECA is determinizable and closed under } \cup,\ \cap,\ \complement
$$

并且关键判定问题保持可解：

$$
\text{tau-wise emptiness and language inclusion for DECA are PSPACE-complete}
$$

相比之下，作者先证明 `icTA` 的 universal timed language 很快退化为困难甚至空集，这正是为何要回到 event-clock / recursive-event 这条 fully decidable 规格线。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 继承 `RECA` 的有限状态骨架。 |
| 事件 / 触发 | 强支持 | clocks 由被监控 automaton / formula 的事件触发。 |
| 守卫 / 数据 | 强支持时钟守卫 | 约束基于 process-indexed event clocks，不依赖自由 reset。 |
| 层次 | 部分支持 | “recursive event” 通过低层 automaton / formula 形成语义层次。 |
| 并发 / 同步 | 强支持分布式本地时间 | 多进程共享事件字，但 local clocks 独立推进。 |
| 时间约束 | 强支持 | 支持 recorder / predictor event clocks 与多种 timed languages。 |
| 连续动态 / 随机性 | 不支持 | 没有连续物理动力学。 |
| 可执行 / 可验证性 | 强理论支持 | determinization、complementation、emptiness / inclusion 都有明确复杂度。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$(A,\pi)$` | 在 `RECA` 外显式加上 process binding。 |
| process 映射 | `$\pi:C\to Proc$` | 每个 clock 的时间参考系由所属进程决定。 |
| 语义接口 | `$\nu(\rho,t,\tau,x_B^q)$` | clock 值依赖低层事件与局部时钟演化。 |
| 闭包性质 | `$\cup,\cap,\complement$` | 支撑 refinement / inclusion workflow。 |
| 复杂度 | `PSPACE-complete` | tau-wise emptiness / inclusion 仍可判。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. 哪些 event 应由哪个低层 automaton / formula 来识别；
2. 每个 event clock 应绑定哪个 process；
3. 关注的是 `tau`-wise、existential 还是 universal timed language。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. `RECA` 状态机骨架；
2. process-indexed clock map `\pi`；
3. `ISS` 表示；
4. region-style determinization / emptiness construction。

### 交换与互操作

它与以下 family 直接相连：

1. [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)
2. `Recursive Event Clock / SCL / EventClockTL`
3. independent-clock timed automata (`icTA`)

其中第三类给了 distributed clock setting，前两类给了 decidable clock discipline；`DECA` 正是把两者拼接起来。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `DECA` determinization、region automaton 与 `DECTL` 翻译。
- 仿真/执行支持：可以按 `ISS + rate assignment` 解释多时钟语义。
- 验证/分析支持：emptiness、inclusion、universality、布尔闭包和逻辑到自动机翻译。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 event-clock / recursive event timed specification 族的理论分支。

## 适用场景与需求前提

### 适用场景

适合那些必须同时表达：

1. 分布式进程各有本地时间；
2. 时间约束仍应由可观测事件稳定决定；
3. 需要 refinement / language inclusion 等 fully decidable analysis。

### 需求前提

1. 需求主要是 timed specification，而不是工程执行器建模。
2. clock 应可解释为某种“上次 / 下次由低层事件定义的观察值”。
3. 不希望重新落回自由 reset clocks 带来的 inclusion undecidability。

### 不适用或高成本场景

若系统需要大量本地可编程 reset、复杂数据更新或连续物理动力学，`DECA` 就不是合适目标；它更像 distributed timed specification family，而不是 CPS 执行模型。

## 与相邻形式主义的关系

相对 `ECA`，它把 event clock family 推向 recursive event 和 distributed local-time setting；相对 `icTA`，它牺牲了自由 reset 换来布尔闭包和 inclusion decidability；相对 `SCL / EventClockTL`，它提供了对应的 automata-side承载体。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Timed Automata` 主干从“单全局时钟语义”推进到“分布式局部时间 + 可确定化规格”这一条此前文库还没明确挂树的分支。

### 作为目标形式主义还是中间表示

更适合作为高层规格或逻辑到自动机的中间表示，而不是最终面向工业控制工程师的交付模型。

### 对需求到模型生成的启发

如果需求本身就带“各子系统时间不同步，但仍要基于事件时距写规格”的语义，LLM 不应直接把它硬压成普通 `TA`；先生成 `DECA` 或其逻辑同构物更稳。

## 重要的相关工作

### 奠基或前身工作

- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)
- `State Clock Logic / EventClockTL`

### 同类型或同家族工作

- `Recursive Event Clock Automata`
- `Independent-Clock Timed Automata`

### 标准 / 格式 / 工具链工作

- 原文没有工程标准；最重要的基础设施是 determinization、region automaton 和 `DECTL -> DECA` 翻译。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Timed Automata -> Input-Determined / Event-Clock 方向 -> Distributed Event Clock Automata / DECA`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
