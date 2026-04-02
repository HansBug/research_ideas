# 商业现场总线协议的建模与分析 / Modelling and Analysis of a Commercial Field Bus Protocol

## 基本信息

- 标题：Modelling and Analysis of a Commercial Field Bus Protocol
- 中文标题：商业现场总线协议的建模与分析
- 作者：Alexandre David, Wang Yi
- 发表：*Proceedings of the 12th Euromicro Conference on Real-Time Systems (ECRTS 2000)*, pp. 165-172, 2000
- DOI：`10.1109/EMRTS.2000.854004`
- 链接：https://doi.org/10.1109/EMRTS.2000.854004
- 形式主义：`Timed Automata / UPPAAL Network`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：⏱️
- 论文角色：工业协议验证 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL`，并说明从 `AF100` 协议源码与抽象 `C-like` 代码双线构造模型；公开工具入口可直接使用 `UPPAAL` 官网发布版本。
- 标准/格式获取方式：承载方式是 `UPPAAL` 的 timed automata network、clock/integer variables、`urgent/committed` 状态与 `A[]`、`E<>` 查询；原文未提供独立交换标准。

## 简报

这篇论文的关键价值，不是单纯“拿 timed automata 验一个协议”，而是展示了怎样把一个已经在线上跑了多年、代码量和文档复杂度都很高的工业现场总线协议，分层压成可调试的 `UPPAAL` 网络模型。作者不是试图一次性证明 `AF100` “完全正确”，而是用逐层抽象、错误边界、`urgent/committed` 语义和诊断 trace，把问题定位回协议逻辑与实现细节，尤其是 race condition、timeout 与 semaphore 误用。

- 形式主义定位：面向工业实时通信协议调试与局部验证的 `Timed Automata` 网络，而不是纯理论的单自动机模型。
- 构造方式简述：从协议源码和抽象 `C-like` 代码出发，建立 `16` 个 automata、`4` 个 clocks、`32` 个整数变量的 `UPPAAL` 模型，再逐层抽成多个 bus coupler 抽象版本。
- 基础设施与场景简述：依托 `UPPAAL` 的 `urgent/committed` 状态、clock invariants、reachability/invariant queries 和 diagnostic trace，服务工业现场总线、实时协议和数据链路层调试。

```text
协议源码 / 规范 -> UPPAAL timed automata network -> 抽象模型族 + A[]/E<> 性质 -> 诊断 trace -> 协议逻辑与实现缺陷定位
```

## 形式主义定义与核心对象

### 定义对象

原文的直接对象不是抽象教材里的“一个 timed automaton”，而是一个工业协议子系统的 `UPPAAL` 网络模型，尤其是：

1. `AF100` 的 bus coupler、`VFI` master/slave、queue 和 physical bus。
2. 由源码直接映射得到的多个并发 automata。
3. 表示 timeout、等待、race condition 的 clocks 与 integer variables。
4. `committed/urgent` 状态、`urgent transitions` 与 invariants。
5. 用于 partial verification 与 debugging 的多层抽象模型。

### 核心抽象

论文没有把模型重新写成单一标准元组，而是直接按 `UPPAAL` 网络来建模。基于原文对“`16` 个 automata、`4` 个 clocks、`32` 个 integer variables”的描述，可将其保守整理为：

$$
\mathcal{N} = (\{A_i\}_{i=1}^{16}, C, V, \mathit{Sync}, \mathit{Inv})
$$

上式中的符号逐项解释如下：

1. `A_i` 是第 `i` 个 timed automaton，对应发送进程、接收进程、semaphore 或辅助函数行为。
2. `C` 是时钟集合，原文实例里共有 `4` 个时钟。
3. `V` 是离散变量集合，原文实例里共有 `32` 个整数变量。
4. `\mathit{Sync}` 是 automata 之间通过 channel/事件进行的同步关系。
5. `\mathit{Inv}` 是 location invariants，用来表达 timeout 与驻留时间限制。

若把单个组件 automaton 再细化，可保守写成：

$$
A_i = (L_i, \ell_i^0, C_i, V_i, E_i, \mathrm{Inv}_i, \tau_i)
$$

上式中的符号逐项解释如下：

1. `L_i` 是位置集合。
2. `\ell_i^0` 是初始位置。
3. `C_i \subseteq C` 是该 automaton 使用的时钟。
4. `V_i \subseteq V` 是该 automaton 观察或更新的离散变量。
5. `E_i` 是带 guard、reset、synchronisation 的转移集合。
6. `\mathrm{Inv}_i` 给每个位置附加时间不变式。
7. `\tau_i` 表示位置/转移的 `urgent`、`committed` 等语义标注。

### 一个最小例子与通俗解释

原文最核心的最小片段是 master 侧 `VFI -> Bus Coupler -> Bus -> slave` 这条握手路径。直观上可以理解成：

1. `VFI` 把一包数据写给 bus coupler。
2. bus coupler 等待 mailbox 或 semaphore 条件满足后，把包送进 bus。
3. 对端 coupler 收到包，再把 acknowledgement 往回送。
4. 若这期间 timeout、bit read 或 semaphore 次序发生 race，某一侧就会“以为”对方已经写好 / 读走，从而进入 de-synchronization。

通俗地说，这里的 timed automata 像一套“会计时的协议流程显微镜”：不仅看系统到了哪个离散状态，还会看“这一步是不是等太久了”“两个线程是不是抢先了”“某个信号是不是在不该丢的时候丢了”。

### 运行 / 接受 / 转移语义

论文直接依赖 `UPPAAL` 的 timed automata network 语义。对全局状态可保守写成：

$$
s = (\vec{\ell}, \nu, \sigma)
$$

上式中的符号逐项解释如下：

1. `\vec{\ell}` 是所有 automata 当前 location 的向量。
2. `\nu` 是当前时钟赋值。
3. `\sigma` 是当前整数变量赋值。

全局一步转移可保守写成：

$$
(\vec{\ell}, \nu, \sigma) \xrightarrow{e} (\vec{\ell}\,', \nu', \sigma')
$$

当且仅当某个同步事件 `e` 的 guard 成立、相应 clock reset/变量更新执行完毕，且源/目标位置都满足 invariants。

论文中真正被反复检查的是 `UPPAAL` 查询，例如：

$$
A[]\,\varphi
$$

以及

$$
E\langle\rangle\,\psi
$$

上式中的符号逐项解释如下：

1. `A[]\,\varphi` 表示在所有可达执行上不变式 `\varphi` 恒成立。
2. `E\langle\rangle\,\psi` 表示存在一条执行能到达满足 `\psi` 的状态。
3. 论文用这两类查询分别检查 precedence / correctness / semaphore 异常与可达错误边界。

### 语义边界

这篇论文里的 timed automata 语义边界很明确：

1. 目标是 industrial debugging，不是对整个 `AF100` 做完备正确性证明。
2. 模型大量使用抽象和 pruning，因此很多性质是“在已排除错误边界条件下的部分验证”。
3. 数据包内容被故意抽象掉，只保留 transparent bit 和少量关键变量。
4. 重点在 protocol logic、synchronisation 和 timeout，而不是业务层语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 网络模型骨架 | `$\mathcal{N} = (\{A_i\}_{i=1}^{16}, C, V, \mathit{Sync}, \mathit{Inv})$` | `AF100` 被实现为多 automata 并发网络，而不是单一协议图。 |
| 全局执行状态 | `$s=(\vec{\ell}, \nu, \sigma)$` | 可同时观察离散位置、clock 值和离散变量。 |
| 不变式检查 | `$A[]\,\varphi$` | 用于表达 transparent bit、precedence、semaphore 等“永远不应违反”的性质。 |
| 可达性检查 | `$E\langle\rangle\,\psi$` | 用于找 error border、live-loop 和具体 counterexample。 |
| 正确性示例 | `$A[]\,(VFIToCoupler\_1P1.written \Rightarrow vfiTrans1 \neq -1)$` | 写数据前 transparent bit 不能是无效值。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 协议进程、bus coupler、queue、VFI 都用 location 建模。 |
| 事件 / 触发 | 强支持 | packet write、ack、timeout、bit read/write 都是核心触发。 |
| 守卫 / 数据 | 强支持 | guard、bit 条件、counter 与透明位共同决定转移。 |
| 层次 | 弱支持 | 原文主要是并发网络与多层抽象，不是层次状态机。 |
| 并发 / 同步 | 强支持 | 多 automata 并发、同步信号、queue 和 semaphore 是主体。 |
| 时间约束 | 强支持 | timeout、delay、urgent/committed、location invariant 都是分析核心。 |
| 连续动态 / 随机性 | 不支持 | 纯离散实时协议。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 可直接做 reachability / invariant 检查与 diagnostic trace。 |

### 形式化问题与性质

1. 论文最重要的不是“timed automata 能建模现场总线”，而是证明了 `urgent/committed` 这些语义旋钮足以把 race condition 与 delay 效应拆出来分析。
2. 它明确区分 faithful source-level model 与 abstract debugging model，这对工业协议尤其关键。
3. `A[]` 与 `E<>` 查询在这里承担的是“缺陷定位器”而不是“完备证明器”。
4. 抽象模型 1-5 的关系说明 timed automata 网络不仅能验性质，还能承载 abstraction ladder。

## 构造方式与承载格式

### 建模入口

建模入口非常工程化：

1. 先从 `AF100` 文档、源码结构和 bus coupler 实现出发。
2. 将发送/接收、queue、semaphore、函数逻辑分别映射成 `UPPAAL` automata。
3. 用 transparent bit、ack、mailbox、counter 等变量保留最关键的协议状态。
4. 再逐层抽掉实现细节，得到用于 debugging 的抽象模型族。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` timed automata network。
2. location 上的 `urgent/committed` 标注。
3. clocks、invariants 与 integer variables。
4. `A[]` / `E<>` 查询与 diagnostic trace。
5. 与模型同步维护的抽象 `C-like` 代码。

### 交换与互操作

互操作重点不在开放标准，而在“源代码 - 抽象模型 - 调试 trace”的闭环：

1. faithful model 直接贴近源码结构，便于把 counterexample 回映到实现。
2. abstract model 便于减少状态空间、局部定位 race condition。
3. `UPPAAL` 查询结果与 trace 可以直接服务工业伙伴的调试流程。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：原文围绕 `UPPAAL` 模型与抽象 `C-like` 源同步维护，未提供开放元模型。
- 仿真/执行支持：重点不在运行时执行，而在 symbolic state-space exploration。
- 验证/分析支持：`A[]`、`E<>`、deadlock detection、diagnostic traces。
- 代码生成/转换支持：原文没有自动代码生成；反而是从源码反向抽象到 automata。
- 标准化或社区生态：依托 timed automata / `UPPAAL` 成熟研究生态，但 `AF100` 本身是商业协议。

## 适用场景与需求前提

### 适用场景

适合实时通信协议、工业现场总线、嵌入式 data-link / transport 子层这类“有离散握手、有 timeout、有 race 风险”的系统调试与验证。

### 需求前提

1. 协议行为能拆成有限个离散状态与事件。
2. 时间行为可以表达成 timeout、等待窗口或不允许延迟的 urgent step。
3. 系统关键错误主要来自顺序、同步与时间，而非复杂数据算法。
4. 工程团队接受“抽象验证 + 反向定位源码”的工作流。

### 不适用或高成本场景

如果系统核心难点在大规模数据语义、复杂连续控制律或海量节点的真实网络时延统计，这种以 timed automata 为主的调试建模会很快碰到抽象成本和状态空间压力。

## 与相邻形式主义的关系

相对 [Timed I/O Automata](../the-theory-of-timed-input-output-automata/desc.md)，本文更偏 `UPPAAL` 工程实践与工业调试；相对 [Reactive Modules](../reactive-modules/desc.md)，它不强调 assume-guarantee 组合与变量模块化，而更强调 timeout、race 与 trace 回放；相对一般协议 `FSM`，它把时间语义、urgency 与 invariants 作为一等对象。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文证明：对于工业控制通信协议，`Timed Automata` 不只是“理论上可验证”，而是能作为源码级抽象与缺陷定位的中间表示。

### 作为目标形式主义还是中间表示

它更适合作为验证导向的中间表示，而不是最终交付给工程人员的首选建模语言；但在协议和实时接口子系统上，也可以直接作为分析工件。

### 对需求到模型生成的启发

1. 从非形式化协议说明到可验证模型时，最先保留的应是 timeout、同步点和错误边界，而不是所有数据细节。
2. “faithful model -> abstract model family” 这条梯度非常适合做 LLM 辅助建模与修复。
3. 若目标是帮助工程调试，则生成模型必须能回映到源码结构，而不是只给一个好看的高层图。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：给出本条应用路线的理论母体。
- [The Theory of Timed I/O Automata](../the-theory-of-timed-input-output-automata/desc.md)：更强调实时接口组合与实现关系。
- `UPPAAL` 早期音频协议、调度与实时控制案例：共同构成“timed automata 走向工业案例”的背景链条。

## 文献分类总结

- 这是一篇 `⏱️` 类高价值应用条目，核心不是提出新自动机，而是展示 `Timed Automata + UPPAAL` 如何进入工业协议调试闭环。
- 其描述客体是协议/交互关系，因此记为 `🤝`；论文语境是实时协议与嵌入式通信，因此记为 `⏱️`。
- 对 `project_1` 来说，它提供了“实时接口行为 -> 可验证状态机网络 -> trace 驱动修复”的完整范式样板。
