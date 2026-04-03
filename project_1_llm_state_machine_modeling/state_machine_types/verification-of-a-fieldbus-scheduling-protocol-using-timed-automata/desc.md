# 基于定时自动机的 Fieldbus 调度协议验证 / Verification of a Fieldbus Scheduling Protocol Using Timed Automata

## 基本信息

- 标题：Verification of a Fieldbus Scheduling Protocol Using Timed Automata
- 中文标题：基于定时自动机的 Fieldbus 调度协议验证
- 作者：Nicholaos Petalidis
- 发表：*Computing and Informatics*, Vol. 28, pp. 655-672, 2009
- DOI：原文未提供
- 链接：https://www.cai.sk/ojs/index.php/cai/article/view/54
- 形式主义：`Timed Automata / Scheduling-Layer Fieldbus Network`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`Fieldbus` 调度协议验证 / 定时自动机应用建模
- 工具/实现获取方式：原文直接使用 `UPPAAL` 建立 scheduling layer、medium layer、data-link entity 和 network management 的 timed automata，并通过查询验证 token circulation、link inactivity、LAS transfer 等性质；论文未给公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、共享消息结构和查询公式；不是独立行业交换标准。

## 简报

这篇论文关心的不是普通的消息收发，而是 `Fieldbus` 里“谁什么时候有资格发 token、多久必须恢复调度、调度器上线下线后网络还能不能继续工作”这一层。作者把传统上常被塞进 data-link layer 内部细节的 scheduler 单独提升成一个 `scheduling layer`，再把 medium layer、DLE 和 network management 一起拼成 timed automata network，用 `UPPAAL` 去检查 changing-topology 下的 safety / liveness 性质。

- 形式主义定位：这是 `Timed Automata` 主干上的工业协议应用条目，重点不在提出新时钟自动机家族，而在展示“调度层 + 介质层 + 数据链路层”如何稳地落成可检网络。
- 构造方式简述：把 scheduler、medium、data-link entity 和 network management 分别建成 timed automata，用 `Tirrd`、`Ttdp` 等 clocks 追踪 link inactivity、token transfer 和 time distribution。
- 基础设施与场景简述：依托 `UPPAAL` 的 reachability / safety / liveness 查询，服务有 token circulation、scheduler takeover 和 changing topology 约束的实时工业现场总线。

```text
fieldbus timing parameters + scheduler rules -> scheduling / medium / DLE timed automata -> UPPAAL queries -> token circulation / safety / liveness verification
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 作为独立层建模的 `scheduling layer`。
2. 承接物理链路和低层转发语义的 `medium layer`。
3. 与具体节点行为对应的 `DLE` automata。
4. 控制节点上下线的 `network management layer`。
5. 表示 link inactivity、token recovery 和 time distribution 的 clocks，如 `Tirrd`、`Ttdp`。
6. `PT / TL / SR / TD / RT / RI` 等协议消息，以及 `UPPAAL` 查询公式。

### 核心抽象

论文直接给出了 timed automaton 的标准定义：

$$
T = \langle L, l_0, C, A, E, I \rangle
$$

上式中的符号逐项解释如下：

1. `$L$` 是位置集合，对应离线、仲裁、持有 token、监控 `PT` 等协议状态。
2. `$l_0 \in L$` 是初始位置。
3. `$C$` 是时钟集合，用来记录 inactivity、token transfer、delay 等时间量。
4. `$A$` 是动作、共动作和内部动作集合。
5. `$E \subseteq L \times A \times B(C) \times 2^C \times L$` 是边集合，其中 `$B(C)$` 是时钟守卫，`$2^C$` 是复位时钟集合。
6. `$I : L \to B(C)$` 把不变式绑定到位置。

论文还给出了 network of timed automata 的组合定义，可保守整理为：

$$
\mathcal{N}_{fb} = A_{SL} \parallel A_{ML} \parallel A_{DLE,1} \parallel \cdots \parallel A_{DLE,n} \parallel A_{NM}
$$

上式中的符号逐项解释如下：

1. `$A_{SL}$` 是 scheduling layer automaton。
2. `$A_{ML}$` 是 medium layer automaton。
3. `$A_{DLE,i}$` 是第 `$i$` 个 data-link entity automaton。
4. `$A_{NM}$` 是 network management automaton。
5. `$\parallel$` 表示按同步动作和共享变量组合的 timed automata network。

这篇论文最关键的抽象不是某个单机 automaton，而是“把 scheduler 单独提升成一层”。作者将其语义压成：

$$
\Sigma_{SL} = \{ON, OFF, CL, TL_i, TD_j, PT_j, RT_i, RI_i, START_i, DATA_i, END_i\}
$$

上式中的符号逐项解释如下：

1. `$\Sigma_{SL}$` 是 scheduling layer 可收发的协议消息集合。
2. `$TL/PT/TD$` 分别对应 transfer LAS、pass token、time distribution 等关键调度消息。
3. `$START_i/DATA_i/END_i$` 是介质层向上暴露的分段活动。
4. 这一定义说明调度语义并非抽象附属物，而是可独立枚举的接口集合。

### 一个最小例子与通俗解释

最小例子可以理解成两个 scheduler 和一个普通节点共享一条总线：

1. 某 scheduler 处于 `hasSchedulerToken`，此时它可以发 `PT` 或 `TD`。
2. 如果链路长时间无活动，`Tirrd` 超过阈值，就必须触发 `CL` 或重新进入 token acquisition。
3. 如果当前 LAS 被关闭，另一个在线 scheduler 需要通过 `TL / SR / PT` 等消息重新接管调度权。
4. `UPPAAL` 随后检查：系统会不会死锁？离线/上线切换后是否仍然存在某个 scheduler 最终拿到 token？

通俗地说，这像“把现场总线调度器本身当成一个需要被验证的实时控制器”。普通 `FSM` 只能表达“收到了什么包”，而 timed automata 还能表达“多久没包就算调度失效”“接管 token 前允许等待多久”“哪类恢复动作必须在时限内发生”。

### 运行 / 接受 / 转移语义

论文强调两类语义：

1. 单 automaton 的 clocks / guards / invariants 语义。
2. 多 automata 之间通过 shared message 和同步动作耦合出的全网语义。

其基本安全查询可整理为：

$$
A[]\ \neg deadlock
$$

上式中的符号逐项解释如下：

1. `$A[]$` 表示“所有路径上的所有状态都满足”。
2. `$\neg deadlock$` 表示系统不能进入无延时、无动作可走的状态。
3. 这是 timed protocol network 的最低正确性要求。

论文表 3 中给出的调度层性质里，最典型的一条是：

$$
A[]\big((msg.pType = PT \land msg.sender = 0 \land Medium.Receiving) \Rightarrow (SL1.transmittedPT \land SL1.Tirrd \le Ptrd)\big)
$$

上式中的符号逐项解释如下：

1. `msg.pType = PT` 表示当前介质上观察到 `PT` packet。
2. `msg.sender = 0` 表示发送者是指定 scheduler。
3. `Medium.Receiving` 表示 medium layer 正在接收该消息。
4. `SL1.transmittedPT` 表示 scheduler `SL1` 的确处于发出 `PT` 的合法状态。
5. `SL1.Tirrd \le Ptrd` 则把 `PT` 发送与 token recovery delay 约束绑定起来。

文中还给出一条关键 liveness 风格性质：

$$
E\Diamond SL1.hasSchedulerToken
$$

上式中的符号逐项解释如下：

1. `$E\Diamond$` 表示“存在一条路径最终到达某状态”。
2. `SL1.hasSchedulerToken` 表示 scheduler `SL1` 最终拿到了 token。
3. 这类性质用于确认 changing-topology 下调度恢复并非永远失败。

### 语义边界

这篇论文的边界主要有：

1. 它重点在 token-bus style 调度与恢复逻辑，不讨论高层复杂应用数据语义。
2. 物理链路被抽象成 medium layer，而不是逐位电气仿真。
3. 论文明确指出 `UPPAAL` 对 variable-rate clock / large drift 的处理能力有限。
4. 更适合有限节点、明确 timing parameters 的工业协议，而不是开放互联网协议。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单 automaton 骨架 | `$T = \langle L, l_0, C, A, E, I \rangle$` | 用时钟守卫和不变式描述 scheduler / medium / DLE。 |
| 全网组合 | `$\mathcal{N}_{fb} = A_{SL} \parallel A_{ML} \parallel A_{DLE,1} \parallel \cdots \parallel A_{NM}$` | 把调度、介质、数据链路和管理层接成同一网络。 |
| 调度层消息集 | `$\Sigma_{SL} = \{ON, OFF, CL, TL_i, TD_j, PT_j, RT_i, RI_i, START_i, DATA_i, END_i\}$` | 明确 scheduling layer 的接口与可观测语义。 |
| 死锁自由 | `$A[]\ \neg deadlock$` | 系统不能卡死。 |
| `PT` 合法发送 | `$A[]((msg.pType = PT \land Medium.Receiving) \Rightarrow (SL1.transmittedPT \land SL1.Tirrd \le Ptrd))$` | `PT` packet 必须发生在合法时序窗口。 |
| token 可恢复性 | `$E\Diamond SL1.hasSchedulerToken$` | 存在执行使 scheduler 拿到 token。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `off-line`、`LM1/LM2`、`hasSchedulerToken` 等显式状态是主体。 |
| 事件 / 触发 | 强支持 | `PT / TL / SR / TD / RT / RI` 等协议消息直接驱动转移。 |
| 守卫 / 数据 | 强支持 | 时钟守卫、共享消息字段、地址与时间参数都进入 guard。 |
| 层次 | 弱支持 | 不是层次状态机，但通过 `scheduling / medium / DLE / NM` 分层组织语义。 |
| 并发 / 同步 | 强支持 | 多 scheduler、多 DLE 与 medium 并行同步是模型主体。 |
| 时间约束 | 强支持 | `Tirrd`、`Ttdp`、`Ptrd`、`Virrd` 等参数直接决定协议合法性。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散实时协议模型。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 可直接检查 reachability、safety 与 liveness。 |

### 形式化问题与性质

1. 论文真正补出的不是“一般现场总线能验证”，而是“调度层本身可以作为独立对象建模并验证”。
2. changing topology 是这篇论文的重要应用侧增量，因为它要求验证上线/下线下的 token recovery。
3. 这条路线比只做 response-time analysis 更强，因为它显式检查协议合法性与恢复过程。

## 构造方式与承载格式

### 建模入口

建模入口可概括为：

1. 枚举 protocol timing parameters 与 packet types。
2. 将 scheduler、medium、DLE、network management 分别建成 timed automata。
3. 用 shared message 变量和同步 channel 连接各层。
4. 用 `UPPAAL` 查询表达 packet legality、token recovery、deadlock freedom。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata templates。
2. 共享 `msg` 结构和 clocks。
3. `UPPAAL` safety / liveness 查询。

### 交换与互操作

互操作重点在：

1. scheduling layer 和 medium layer 如何共享 packet 语义。
2. network management 如何通过 `ON/OFF` 改写 scheduler 行为。
3. DLE 如何通过 medium 感知 token 与 activity。

## 配套基础设施

- 建模/编辑工具：原文直接使用 `UPPAAL` 建模和查询。
- 解析/交换/元模型支持：无独立交换格式；模型主体是 `UPPAAL` 网络与共享消息结构。
- 仿真/执行支持：可在 `UPPAAL` 中仿真不同 packet / topology 场景。
- 验证/分析支持：支持 reachability、safety、liveness 和 diagnostic reasoning。
- 代码生成/转换支持：原文未提供自动代码生成链。
- 标准化或社区生态：依托 `Fieldbus` 协议背景与 `UPPAAL` 研究生态。

## 适用场景与需求前提

### 适用场景

适合 Foundation Fieldbus 一类带 token circulation、scheduler takeover 和严格 timing parameters 的工业总线协议。

### 需求前提

1. 协议消息类型和 timing constants 可显式枚举。
2. 节点数、scheduler 数与 topology 变化范围可有限化。
3. 关键正确性问题在调度合法性、恢复性和时序窗口，而不是大规模数据语义。

### 不适用或高成本场景

如果系统核心难点在复杂负载数据、概率时延分布或连续物理链路细节，仅靠这里的 timed automata 分层抽象会过于粗粒度。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是典型工业协议落地；相对 [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，本文更突出 `scheduling layer` 的独立建模与 changing-topology 语义；相对 [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)，它不是固定优先级广播总线，而是带显式 scheduler token 的 fieldbus 调度协议。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里出现“谁拥有调度权、多久必须恢复、上下线如何影响通信合法性”时，生成的状态机不能只建业务流程，还要显式抽出调度层时钟语义。

### 作为目标形式主义还是中间表示

对工业协议验证，它可以直接作为目标形式主义；对更大控制系统，也适合作为通信子系统的时序中间表示。

### 对需求到模型生成的启发

1. 协议规范中的 packet set 和 timing constants 可以直接转成 timed automata guard / invariant。
2. 有些“看似实现细节”的 scheduler 逻辑，实际上值得在模型层独立成一层。
3. changing-topology 这类运维条件也应进入状态机生成，而不是留给后验口头假设。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文所依赖的经典定时自动机理论底座。
- [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：同样面向工业现场总线，但焦点是 bus coupler 抽象与缺陷定位。
- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：同样是协议/总线应用条目，但总线仲裁机制不同。

## 文献分类总结

- 形式主义：`Timed Automata / Scheduling-Layer Fieldbus Network`
- 成熟度：`UPPAAL` 查询链路明确，属于可直接复用的工业协议建模样板。
- 条目价值：这是一篇 `⏱️` 类高价值应用条目，核心贡献是把 `Fieldbus` 调度层作为独立 timed automata 层来验证。
