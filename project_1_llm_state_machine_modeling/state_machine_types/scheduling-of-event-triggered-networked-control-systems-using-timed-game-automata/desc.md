# 用时间博弈自动机调度事件触发网络控制系统 / Scheduling of Event-Triggered Networked Control Systems using Timed Game Automata

## 基本信息

- 标题：Scheduling of Event-Triggered Networked Control Systems using Timed Game Automata
- 中文标题：用时间博弈自动机调度事件触发网络控制系统
- 作者：Dieky Adzkiya，Manuel Mazo Jr
- 发表：arXiv 预印本，2016
- DOI：原文未给 DOI；当前目录保存的是 `arXiv:1610.03729` 公开 PDF
- 链接：https://arxiv.org/abs/1610.03729
- 形式主义：`Timed Game Automata / Event-Triggered NCS Scheduler`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：共享网络调度 / `Timed Game Automata` 应用条目
- 工具/实现获取方式：原文明确使用 `UPPAAL-Tiga` 生成 winning strategy；未提供独立代码仓库。
- 标准/格式获取方式：承载方式是 `TA`、`TGA`、`NTGA` 数学定义和 `UPPAAL-Tiga` 游戏模型；无统一交换标准。

## 简报

这篇论文的核心不是单纯验证一个已有控制器，而是把“多个事件触发控制回路争用一条共享网络”这个调度问题直接写成了 `Timed Game Automata` 的安全博弈问题。网络是否空闲、控制回路何时请求更新、调度器是否提前强制更新，全部被放进同一个 `NTGA` 里。随后，调度器的目标被写成“永远别让系统进入冲突状态”，也就是合成一个保证无冲突的 strategy。

- 形式主义定位：这是 `Timed Automata -> Timed Game Automata` 的典型应用条目，重点是“controller/environment role split + safety objective + strategy synthesis”。
- 构造方式简述：先给共享网络一个 `TGAnet`，再为每个 event-triggered control loop 构造 `TGAcl`，最后并行组合成 `NTGA` 并对 bad states 做安全博弈求解。
- 基础设施与场景简述：依托 `UPPAAL-Tiga`、event-triggered abstraction 和 network occupancy model，服务共享通信网络上的多控制回路调度。

```text
事件触发控制回路 + 共享网络占用约束 -> network / loop TGA -> NTGA -> safety strategy -> 无冲突 scheduler
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 标准 `TA` 作为基础语义对象。
2. `TGA`，即区分 controllable / uncontrollable actions 的时间博弈自动机。
3. `NTGA`，即多个 `TGA` 的并行组合。
4. 共享网络 automaton `TGAnet`。
5. bad-state safety objective 与 strategy synthesis。

### 核心抽象

原文给出的 `Timed Game Automaton` 定义是：

$$
TGA = (L, \ell_0, Act_c, Act_u, C, E, Inv)
$$

上式中的符号逐项解释如下：

1. `L` 是有限位置集合。
2. `\ell_0` 是初始位置。
3. `Act_c` 是 controllable actions，由调度器/控制器触发。
4. `Act_u` 是 uncontrollable actions，由环境触发。
5. `C` 是时钟集合。
6. `E` 是带 guard、action 和 reset 的边集合。
7. `Inv` 是位置不变式。

论文对多个博弈自动机的并行组合写成：

$$
TGANCSs := TGAnet \mid TGAcl_1 \mid \cdots \mid TGAcl_N
$$

上式中的符号逐项解释如下：

1. `TGAnet` 是共享通信网络的博弈自动机。
2. `TGAcl_i` 是第 `i` 个控制回路对应的博弈自动机。
3. 组合后的全局状态同时跟踪网络位置、各控制回路位置和所有时钟赋值。

### 一个最小例子与通俗解释

一个最小直觉例子是：两条控制回路共享一条网络链路，每次发送更新都要占用网络 `\Delta` 时间。

1. 当网络在 `Idle` 时，某条回路可以请求更新并把网络切到 `InUse`。
2. 若另一条回路在 `InUse` 期间也请求更新，就会转到 `Bad`，表示通信冲突。
3. 调度器可以做两件事：提前强制某条回路更新，或者选择它当前采用哪个 triggering coefficient。
4. 博弈求解的目标就是：无论环境何时触发 uncontrollable request，调度器都能保证永远不进 `Bad`。

通俗地说，这不是“时钟到了就发消息”的被动验证，而是“面对会主动捣乱的环境，调度器该如何先手布局”的时间博弈。

### 运行 / 接受 / 转移语义

原文首先给出 `TA` 的标准操作语义，再把其提升到 `TGA`。其中 delay / discrete transitions 的基础语义为：

$$
(\ell, u) \xrightarrow{d}_{TS} (\ell, u + d)
$$

$$
(\ell, u) \xrightarrow{a}_{TS} (\ell', u')
$$

上式中的符号逐项解释如下：

1. 第一式表示在满足 `Inv(\ell)` 的前提下延时 `d`。
2. 第二式表示当边 `\ell \xrightarrow{g, a, r} \ell'` 的 guard 成立时，执行 action `a` 并复位 `r` 中的时钟。
3. `u` 与 `u'` 分别是跳转前后的时钟赋值。

论文对 safety objective 的 bad states 直接给出集合表达：

$$
A = \{(\ell_{net}, \ell_1, \ldots, \ell_N, u_{net}, u_1, \ldots, u_N) \mid \ell_{net} = Bad\}
$$

上式中的符号逐项解释如下：

1. `\ell_{net}` 是共享网络 automaton 的当前位置。
2. `\ell_1, \ldots, \ell_N` 是各控制回路 automata 的当前位置。
3. `u_{net}, u_1, \ldots, u_N` 是对应时钟赋值。
4. 若网络位置进入 `Bad`，就表示有控制回路在网络忙碌时仍发起更新请求，发生通信冲突。

### 语义边界

这篇论文的边界相当清楚：

1. 调度器是集中式的，需要看到抽象后的全局状态。
2. 网络模型默认所有控制回路占用同一固定上界 `\Delta`。
3. 目标是 safety，重点在 conflict avoidance，而不是 cost-optimal control。
4. 文中也明确指出，若要表达更细的优化目标，可能需要 `priced timed game automata`，而本文并未进入那条路线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TGA` 元组 | `$TGA = (L, \ell_0, Act_c, Act_u, C, E, Inv)$` | 把 action 明确分成 controller 和 environment 两类。 |
| 并行组合 | `$TGANCSs := TGAnet \mid TGAcl_1 \mid \cdots \mid TGAcl_N$` | 调度问题落到网络化的时间博弈自动机。 |
| bad states | `$A = \{(\ell_{net}, \ell_1, \ldots, \ell_N, u_{net}, u_1, \ldots, u_N) \mid \ell_{net} = Bad\}$` | 把通信冲突写成显式安全禁区。 |
| 求解目标 | `winning strategy for safety objective` | 合成能永久避开冲突状态的 scheduler。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 网络和每个控制回路都有显式位置模式。 |
| 事件 / 触发 | 强支持 | request、update、earlier update、triggering choice 都是核心事件。 |
| 守卫 / 数据 | 强支持 | guards 和 clock regions 决定调度器可行动作。 |
| 层次 | 不支持 | 模型主体是平面 `TGA/NTGA` 组合。 |
| 并发 / 同步 | 强支持 | 网络与多个控制回路通过同步动作共同演化。 |
| 时间约束 | 强支持 | channel occupancy、inter-sample times 和 region bounds 是主体。 |
| 连续动态 / 随机性 | 部分支持 | 控制对象本身来自连续系统抽象，但调度模型是离散时间博弈。 |
| 可执行 / 可验证性 | 强综合 | `UPPAAL-Tiga` 可直接求 winning strategy。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先为共享网络构造 `TGAnet`，刻画 `Idle / InUse / Bad`。
2. 再把每个 event-triggered control loop 抽象成一个 `TGAcl`。
3. 在 `TGAcl` 中加入 controllable 的 coefficient choice / earlier update 和 uncontrollable 的 update request。
4. 最后把 bad states 写成安全目标，并交给 `UPPAAL-Tiga` 合成策略。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `TGA` / `NTGA` 数学定义。
2. 共享网络与控制回路的模板化 automata。
3. `UPPAAL-Tiga` 游戏模型。
4. 基于 strategy 的 centralized scheduler。

### 交换与互操作

这篇论文没有统一交换格式；它的价值主要在：

1. 把 event-triggered scheduling 统一写成 `NTGA`；
2. 从 game model 直接导出 winning strategy；
3. 为后续实现提供 scheduler decision logic。

## 配套基础设施

- 建模/编辑工具：`UPPAAL-Tiga`。
- 解析/交换/元模型支持：原文未提供通用交换格式。
- 仿真/执行支持：以策略导出的 centralized scheduler 为主，正文展示了 `UPPAAL-Tiga` 生成的策略片段。
- 验证/分析支持：safety game solving、winning states 计算。
- 代码生成/转换支持：原文展示了如何从抽象 event-triggered timing model 和 network model 构造 `NTGA`，但未给自动代码生成器。
- 标准化或社区生态：属于 `UPPAAL-Tiga` / timed game synthesis 工具线。

## 适用场景与需求前提

### 适用场景

适合多条控制回路共享通信网络、并且调度器需要在冲突避免和控制性能之间做离散决策的网络化控制系统。

### 需求前提

1. 控制回路必须能抽象成 event-triggered timing model。
2. 环境动作和调度器动作必须明确区分成 uncontrollable / controllable。
3. 网络占用上界和更新请求模式必须可显式写成 clocks 与 guards。
4. 目标主要是 safety，而不是复杂的长期收益最优。

### 不适用或高成本场景

若系统需要部分可观测策略、异构占用时间、复杂优化目标或分布式 scheduler，这篇论文的 centralized `NTGA` 框架就会偏弱。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文在 `TA` 上新增了 controllable / uncontrollable action 的角色划分，因此稳定落到 `Timed Game Automata` 分支；相对 [Timed Controller Synthesis: An Industrial Case Study](../timed-controller-synthesis-an-industrial-case-study/desc.md)，两者同属 `TGA` 主干，但那篇聚焦油泵控制器综合，本文聚焦共享网络下的 event-triggered scheduler；相对 [Adaptive Scheduling of Data Paths using Uppaal Tiga](../adaptive-scheduling-of-data-paths-using-uppaal-tiga/desc.md)，两者都用 `UPPAAL-Tiga`，但本文更强调 bad-state safety objective 与 centralized network scheduler。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，当需求文本里已经隐含“环境动作”和“控制动作”两个参与方时，直接把目标形式主义提到 `TGA` 会比死守经典 `TA` 更自然。

### 作为目标形式主义还是中间表示

对需要 controller synthesis 的调度问题，它可以直接作为目标形式主义；对一般需求到状态机建模，它也很适合作为 synthesis-oriented 中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要显式区分 scheduler 可以决定什么、环境会决定什么。
2. “冲突不可达”这类要求非常适合直接翻译成 bad states。
3. 若文本里出现“提前更新”“切换阈值”“共享信道占用”等词，往往已经指向了 `TGA` 建模入口。

### 现实限制

自动化生成最难的不是写出 `TGA` 语法，而是找到既保真又足够小的抽象，否则 strategy synthesis 很快就会爆炸。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文的 `TGA` 仍建立在经典 `TA` 的 clocks/guards 之上。
- [Timed Controller Synthesis: An Industrial Case Study](../timed-controller-synthesis-an-industrial-case-study/desc.md)：同属 `Timed Game Automata` 主干的工业综合路线。
- [Adaptive Scheduling of Data Paths using Uppaal Tiga](../adaptive-scheduling-of-data-paths-using-uppaal-tiga/desc.md)：同样使用 `UPPAAL-Tiga`，但对象是工业流水线而非共享网络控制回路。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Timed Game Automata / Event-Triggered NCS Scheduler`
- 论文角色：共享网络调度 / `Timed Game Automata` 应用条目
- 核心功能：把 event-triggered NCS 的共享网络调度写成 safety game 并综合无冲突策略
- 关键特性：controllable / uncontrollable actions、`NTGA`、bad states、centralized scheduler
- 构造方式：`TGAnet` + `TGAcl_i` -> `NTGA` -> safety strategy
- 基础设施：`UPPAAL-Tiga`
- 适用场景：共享通信网络上的多控制回路调度与冲突规避
- 需求前提：环境动作、调度器动作和网络占用约束需可显式抽象
- 状态：🟢
