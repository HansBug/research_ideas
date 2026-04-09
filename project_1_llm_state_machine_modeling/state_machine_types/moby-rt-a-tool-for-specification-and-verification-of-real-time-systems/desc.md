# Moby/RT：面向实时系统规约与验证的工具链 / Invited Tool Demonstration Moby/RT: A Tool for Specification and Verification of Real-Time Systems

## 基本信息

- 标题：Invited Tool Demonstration Moby/RT: A Tool for Specification and Verification of Real-Time Systems
- 中文标题：Moby/RT：面向实时系统规约与验证的工具链
- 作者：Henning Dierks
- 发表：*Electronic Notes in Theoretical Computer Science*，82(2):346，2004
- DOI：`10.1016/S1571-0661(05)82595-2`
- 链接：https://doi.org/10.1016/S1571-0661(05)82595-2
- 形式主义：`Moby/RT / Constraint Diagrams / PLC-Automata / Structured Text / Timed Automata`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：`PLC` 实时控制需求、设计、代码生成与验证一体化工具链
- 工具/实现获取方式：原文直接把 `Moby/RT` 描述为集成工具，含 `Constraint Diagram` 与 `PLC-Automata` 图形编辑器、仿真器、`Structured Text` 编译器、从需求综合 `PLC-Automata` 的算法以及接入 `UPPAAL` 的自动验证链；正文未给稳定公开仓库。
- 标准/格式获取方式：承载工件主要是 `Constraint Diagrams`、`PLC-Automata`、生成的 `Structured Text` 以及面向 `UPPAAL` 的 `Timed Automata`；不是行业中立交换标准。

## 简报

这篇论文的价值，不在于再发明一种新的时间状态机母型，而在于把工业 `PLC` 控制逻辑的几个断裂层真正接起来了：需求层用 `Duration Calculus` 和 `Constraint Diagrams`，设计层用 `PLC-Automata`，实现层落到 `Structured Text`，验证层再翻到 `Timed Automata` 和 `UPPAAL`。对 `project_1` 来说，这正是“需求表述 -> 形式模型 -> 实现载体 -> 自动验证”闭环的早期工程化样板。

- 形式主义定位：围绕 `PLC-Automata` 的 requirements-to-design-to-code-to-verification 基础设施，而不是新的理论母型。
- 构造方式简述：先把连续时间需求写成 `DC/CD`，再综合或手工构造 `PLC-Automata`，随后编译到 `Structured Text`，并把语义映射到 `Timed Automata` 做自动验证。
- 基础设施与场景简述：依托 `DC`、`Constraint Diagrams`、`PLC-Automata`、`ST`、`UPPAAL` 与若干图形编辑/仿真组件，服务 `PLC` 型实时工业控制系统。

```text
需求约束 -> DC / Constraint Diagrams -> PLC-Automata -> Structured Text / Timed Automata -> PLC 实现 / UPPAAL 验证
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Duration Calculus (DC)` 需求公式；
2. `Constraint Diagrams (CD)` 图形化需求承载；
3. `PLC-Automata` 设计规约；
4. `Structured Text (ST)` 实现载体；
5. `Timed Automata (TA)` 验证语义与 `UPPAAL` 后端。

### 核心抽象

论文直接给出 `PLC-Automaton` 的形式化元组：

$$
A = (Q,\Sigma,\delta,q_0,\varepsilon,S_t,S_e,\Omega,\omega)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是有限状态集合。
2. `$\Sigma$` 是输入集合。
3. `$\delta : Q \times \Sigma \to Q$` 是迁移函数。
4. `$q_0$` 是初始状态。
5. `$\varepsilon$` 是一次 `PLC` 轮询周期的上界。
6. `$S_t : Q \to \mathbb{R}_{\ge 0}$` 给每个状态附加延迟时间。
7. `$S_e : Q \to \mathcal P(\Sigma)$` 给每个状态附加“哪些输入会触发延迟”的输入集合。
8. `$\Omega$` 是输出集合。
9. `$\omega : Q \to \Omega$` 是输出函数。

需求与设计之间的正确性关系首先在 `DC` 层表达为：

$$
DC(spec) \Rightarrow DC(req)
$$

上式中的符号逐项解释如下：

1. `$DC(spec)$` 是设计规约的 `DC` 语义。
2. `$DC(req)$` 是需求规约的 `DC` 语义。
3. 当设计和需求使用不同抽象变量集时，论文还允许加入 link 公式再判定蕴含。

工具链的最关键语义桥接是：

$$
TA(A) \approx DC_{strong}(A), \qquad DC_{strong}(A) \Rightarrow DC(A)
$$

上式中的符号逐项解释如下：

1. `$TA(A)$` 是从 `PLC-Automaton` 构造出的 `Timed Automaton` 语义。
2. `$DC_{strong}(A)$` 是加强版 `DC` 语义。
3. `$\approx$` 表示论文建立的运行等价关系。
4. 这说明把 `PLC-Automata` 送到 `UPPAAL` 做验证，不是拍脑袋近似，而是有明确语义连接。

自动验证条件则被压成：

$$
DC(A) \Rightarrow DC(C) \iff TA(A)\parallel TA(C)\not\models E<> \ bad
$$

上式中的符号逐项解释如下：

1. `$C$` 是某个 `Constraint Diagram`。
2. `$TA(C)$` 是从该需求图生成的 timed test automaton。
3. `$bad$` 是需求违例位置。
4. 右侧含义是：只要并行组合后无法到达 `bad`，就说明设计满足需求。

### 一个最小例子与通俗解释

论文中的 watchdog 例子很适合说明这条路线：

1. 状态 `q0` 输出 `OK`，表示持续收到正常信号。
2. 首次读到 `n` 时转到 `q1`，输出 `Test`，并开始计时。
3. 若 `n` 连续保持超过约 `9` 秒，则转到 `q2`，输出 `Alarm`。
4. 若中途又读到 `s`，则回到 `q0`。

通俗地说，`PLC-Automata` 不是普通状态机上“顺手加个计时器”，而是把 `PLC` 扫描周期、稳定输入持续时间和状态输出都当成一等语义对象。`Moby/RT` 做的就是把这种工业控制思路从需求图一路护送到可执行代码和模型检查。

### 运行 / 接受 / 转移语义

论文对 `PLC-Automata` 的 `DC` 语义写成若干合取公式：

$$
DC(A) = \bigwedge_{j=1}^{11} DC_j
$$

上式中的符号逐项解释如下：

1. 每个 `$DC_j$` 描述一个局部语义约束，例如初始状态、输入采样、输出关联或扫描周期约束。
2. 论文示例中 `$DC_1$` 用来固定初始状态为 `$q_0$`。
3. 这种写法说明 `PLC` 的循环执行语义被直接压进区间时序逻辑。

对反应时间上界，论文给出：

$$
\lceil state_A \in Q_0 \land input_A \in \Sigma_0 \rceil \xrightarrow{c_n} \lceil state_A \in \delta^n(Q_0,\Sigma_0) \rceil
$$

其中：

$$
s(q,\Sigma_0)=
\begin{cases}
S_t(q)+2\varepsilon, & S_t(q)>0 \land \Sigma_0 \cap S_e(q)\neq\emptyset \\
\varepsilon, & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$\delta^n(Q_0,\Sigma_0)$` 表示从状态集合 `$Q_0$` 出发，在输入集合 `$\Sigma_0$` 下经过 `$n$` 步可达的状态集合。
2. `$c_n$` 是论文给出的最坏反应时间上界。
3. `$s(q,\Sigma_0)$` 体现了状态延迟注解和 `PLC` 轮询周期共同造成的额外代价。
4. 这不是简单的“边权求和”，而是专门针对 `PLC` scan-cycle 语义校正后的时间分析。

### 语义边界

1. 主体面向 `PLC` 周期执行、离散输入轮询和有限控制逻辑。
2. 连续时间需求主要在 `DC/CD` 层表达，设计与实现仍回落到可实现的 `PLC-Automata` 与 `ST`。
3. 论文依赖 `UPPAAL` 做自动验证，因此验证对象最终必须能翻到相应 `Timed Automata`。
4. 这不是一般混成控制器综合框架，也不处理富连续动力学本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PLC-Automaton` 元组 | `$A = (Q,\Sigma,\delta,q_0,\varepsilon,S_t,S_e,\Omega,\omega)$` | 固定设计层状态机与 `PLC` 周期语义骨架。 |
| 需求满足 | `$DC(spec) \Rightarrow DC(req)$` | 需求与设计在 `DC` 层的核心判定关系。 |
| `TA` 语义桥接 | `$TA(A) \approx DC_{strong}(A)$` | 说明 timed-backend 验证是有语义根据的。 |
| 自动验证条件 | `$TA(A)\parallel TA(C)\not\models E<> \ bad$` | `UPPAAL` 可直接消费的最终判定形式。 |
| 反应时间上界 | `$\xrightarrow{c_n}$` 与 `$s(q,\Sigma_0)$` | 把 `PLC` 扫描周期和状态延迟一起纳入上界分析。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `PLC-Automata` 本身就是显式状态与输出函数。 |
| 事件 / 触发 | 很强 | 输入轮询、延迟输入集合和状态切换都是一等对象。 |
| 守卫 / 数据 | 中等支持 | 主体是离散输入与延迟注解，不是富数据运算。 |
| 层次 | 弱支持 | 正文最后提到可层次化组织，但本文主体仍是基础 `PLC-Automata`。 |
| 并发 / 同步 | 条件支持 | 工具支持网络化 `PLC-Automata`，但语义主线仍以单机为核心解释。 |
| 时间约束 | 很强 | `DC`、状态延迟、扫描周期上界和 `TA` 验证都是中心内容。 |
| 连续动态 / 随机性 | 不支持 | 连续时间只以逻辑约束方式出现，不进入连续状态演化。 |
| 可执行 / 可验证性 | 很强 | 有编辑、仿真、综合、`ST` 代码生成与 `UPPAAL` 验证链。 |

### 形式化问题与性质

1. `Moby/RT` 的代表性在于把“需求、设计、实现、验证”四层工件钉成一条可机械转换的链。
2. 它不是只会做模型检查，而是也考虑从 `DC` implementables 综合 `PLC-Automata`。
3. `PLC` 扫描周期 `\varepsilon` 被作为硬语义对象保留下来，这对工业控制建模尤其关键。

## 构造方式与承载格式

### 建模入口

论文中的典型入口包括：

1. 用 `Constraint Diagrams` 表达需求模式；
2. 用 `PLC-Automata` 描述可实现控制逻辑；
3. 用 `Structured Text` 作为 `PLC` 部署代码；
4. 用 `Timed Automata` 作为自动验证中间表示。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 图形化 `CD`；
2. 图形化 `PLC-Automata`；
3. 自动生成的 `ST` 程序；
4. 自动生成的 `TA(A)` 与 `TA(C)`。

### 交换与互操作

1. `DC/CD -> PLC-Automata` 提供需求到设计的链接。
2. `PLC-Automata -> ST` 提供实现落地路径。
3. `PLC-Automata / CD -> Timed Automata` 提供与 `UPPAAL` 的互操作。

## 配套基础设施

- 建模/编辑工具：`Constraint Diagram` 与 `PLC-Automata` 图形编辑器。
- 解析/交换/元模型支持：`CD`、`PLC-Automata`、`ST`、`TA` 几类工件之间存在明确转换关系。
- 仿真/执行支持：支持网络化 `PLC-Automata` 的仿真，以及记录与回放。
- 验证/分析支持：`DC` 需求检查、反应时间上界分析、`UPPAAL` reachability 验证。
- 代码生成/转换支持：`PLC-Automata` 到 `Structured Text` 编译，以及需求到 `PLC-Automata` 的综合。
- 标准化或社区生态：建立在 `PLC` 工业编程实践、`Structured Text` 和 `UPPAAL` 既有生态之上。

## 适用场景与需求前提

### 适用场景

适合那些已经有相对清晰的工业控制需求模式，希望进一步形成 `PLC` 设计、部署代码和自动验证闭环的场景，尤其是带定时告警、轮询执行和输入稳定时间判断的控制器。

### 需求前提

1. 需求需要能压成 `DC` 或 `Constraint Diagram` 风格的时序约束。
2. 实现对象更接近周期扫描式 `PLC` 控制，而不是连续控制器。
3. 关键时间性质需要显式考虑 `PLC` 周期上界和状态延迟注解。
4. 团队接受多层工件并存，而不是只保留单一代码视图。

### 不适用或高成本场景

若系统核心是高维连续动力学、概率行为或复杂数据处理，`Moby/RT` 这类 `PLC`-中心路线会比较吃力；若需求本身无法结构化成 `CD/DC` 约束，也难以发挥工具链优势。

## 与相邻形式主义的关系

相对 [a-unifying-semantics-for-sequential-function-charts/desc.md](../a-unifying-semantics-for-sequential-function-charts/desc.md)，`SFC` 更像 `IEC 61131-3` 里的工业步骤控制语义本体，而 `Moby/RT` 是围绕 `PLC-Automata` 的需求-实现-验证工具链；相对 [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)，`CIF 3` 偏监督控制工程平台，`Moby/RT` 更强调 `PLC` scan-cycle 与 `DC` 需求桥接；相对 [uppaal-in-a-nutshell/desc.md](../uppaal-in-a-nutshell/desc.md)，`UPPAAL` 是 timed-backend，本条目说明工业 `PLC` 设计怎样被系统地送进这个后端。

## 与本研究的关系

### 对 Project 1 的价值

1. 这篇论文非常接近 `project_1` 想解决的主问题：如何把非形式化或半形式化需求，逐层变成高可信状态机模型。
2. 它证明“一个中间表示不够”，需求图、设计状态机、实现代码和验证模型可以各有其职，但又通过明确转换连接。
3. 对后续 `project_3/project_4` 而言，它还提供了“验证失败后能回指到哪一层工件”的现实模板。

### 作为目标形式主义还是中间表示

更像围绕 `PLC-Automata` 的工程基础设施与多工件桥梁，而不是单纯前端建模语言。

### 对需求到模型生成的启发

1. 需求到模型自动化不必一步到位；中间可以有 `CD -> PLC-Automata -> TA` 这样的分层过渡。
2. 若目标系统是工业控制器，周期执行语义必须在建模时就被显式保留。
3. 代码生成和验证最好共享同一设计层语义，而不是各自发明一套近似模型。

## 重要的相关工作

1. [a-unifying-semantics-for-sequential-function-charts/desc.md](../a-unifying-semantics-for-sequential-function-charts/desc.md)：工业 `PLC` 语义主线对照。
2. [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)：另一条工业控制工具链路线。
3. [uppaal-in-a-nutshell/desc.md](../uppaal-in-a-nutshell/desc.md)：`Moby/RT` 验证后端所依赖的 timed platform。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
