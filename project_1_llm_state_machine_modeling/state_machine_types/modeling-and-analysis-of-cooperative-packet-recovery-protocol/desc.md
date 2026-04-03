# 协作式分组恢复协议的建模与分析 / Modeling and Analysis of Cooperative Packet Recovery Protocol

## 基本信息

- 标题：Modeling and Analysis of Cooperative Packet Recovery Protocol
- 中文标题：协作式分组恢复协议的建模与分析
- 作者：Muhammad Naeem，Muhammad Atif，Arshad Ali，Maryam Gulzar，Imran Riaz Hasrat
- 发表：*IEEE Access*，Volume 12，pp. 56334-56343，2024
- DOI：`10.1109/ACCESS.2024.3389738`
- 链接：https://doi.org/10.1109/ACCESS.2024.3389738
- 形式主义：`Timed Automata / Cooperative Packet Recovery Protocol Model`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：协议缺陷分析 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL` 建模和 verifier，对两种 server-client 架构做形式验证；未提供独立公开模型仓库。
- 标准/格式获取方式：承载方式是 source/server/client/receiver 的 `UPPAAL` timed automata、buffer arrays、broadcast/unicast channels 和 requirement queries；无统一交换标准。

## 简报

这篇论文研究的是 multicast video/audio 里一个很具体的 QoS 问题：client 漏包以后，server 靠 NACK 请求回传 repair packet，机制是否真能稳定恢复所有丢失分组。作者把 source、server、client 和 receivers 都写成 timed automata，再把 buffer、NACK queue 和 inter-packet delay 作为离散参数接进模型，最后用 `UPPAAL` 检查 deadlock、repair completeness 和 recovered packet delivery 等性质。结果显示：协议并不像原始方案声称的那样总能恢复丢包。

- 形式主义定位：这是经典 `Timed Automata` 主干上的协议分析条目，重点是“buffer-aware protocol model + formal requirements + counterexample-based defect finding”。
- 构造方式简述：把 source/server/client/receiver 分别建模，client 和 server 维护 circular buffer、NACK buffer、retry counter 等状态，再用 `A[]` 查询验证协议功能需求。
- 基础设施与场景简述：依托 `UPPAAL`、broadcast/unicast channels、buffer 函数和 requirement formulas，服务 multicast packet recovery 协议分析与 QoS 条件调参。

```text
协议规则 + buffer / NACK 机制 + IPD -> source/server/client/receiver timed automata -> requirement queries -> counterexamples / 参数调整
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. source、server、client、receiver 四类协议进程。
2. playback buffer、repair buffer 和 NACK buffer。
3. `SendPkt`、`SendNack`、`SendRepairPkt` 等通信动作。
4. `R1-R4` 四个 formal requirements。
5. 用于估计 active part of buffer (`APB`) 的解析公式。

### 核心抽象

结合原文结构，可保守整理出协议模型骨架：

$$
\mathcal{N}_{cprp} = A_{src} \parallel A_{srv} \parallel \Big(\bigparallel_i A_{cli,i}\Big) \parallel \Big(\bigparallel_j A_{rcv,j}\Big)
$$

上式中的符号逐项解释如下：

1. `A_{src}` 是 source automaton。
2. `A_{srv}` 是 retransmit server automaton。
3. `A_{cli,i}` 是第 `i` 个 client automaton。
4. `A_{rcv,j}` 是第 `j` 个 receiver automaton。
5. `\parallel` 表示所有进程通过 channels 并行同步。

对 client 侧，最关键的不是位置数本身，而是 buffer 和 sequence-number 变量。可保守整理为：

$$
Client_i = (L_i, l_i^0, C_i, Buf_i, Nack_i, E_i, Inv_i)
$$

上式中的符号逐项解释如下：

1. `L_i` 是 client 的位置集合。
2. `l_i^0` 是初始位置。
3. `C_i` 是与 delay、send/receive 动作相关的 clocks。
4. `Buf_i` 是 playback buffer 及其 `front/rear` 指针。
5. `Nack_i` 是待恢复丢包相关状态，如 `packet2Recover`、`retry_count`。
6. `E_i` 是带 guards、sync 和 updates 的边集合。
7. `Inv_i` 是位置不变式。

### 一个最小例子与通俗解释

最小例子就是一个 client 丢了某个 packet：

1. source 连续广播 packet。
2. client 收到一个更大的 sequence number，于是发现中间有丢包。
3. client 把丢失包号写进 buffer，并通过 `SendNack` 向 server 申请 repair packet。
4. 如果 server 的 repair buffer 还没把这个 packet 覆盖掉，就会回传；否则 recovery 失败。

通俗地说，这篇论文做的就是“把网络协议里的缓冲区和补包队列也都状态机化”，于是很多原来靠直觉觉得“应该能补回来”的路径，都会被 model checker 直接打出反例。

### 运行 / 接受 / 转移语义

论文给出的第一个需求是 deadlock 条件：

$$
A[]\ deadlock\ \text{imply}\ Source.Packet == totalPackets
$$

上式中的符号逐项解释如下：

1. `A[]` 表示所有路径上的所有状态。
2. `deadlock` 表示模型不能继续推进。
3. `Source.Packet` 是 source 已发送的 packet 计数。
4. `totalPackets` 是总包数。
5. 该式表示：只有当 source 已经发完全部 packet 时，协议才允许 deadlock。

关于 repair 完整性，论文给出：

$$
A[]\ deadlock\ \text{imply}\ all\_avaliable\_packets\_RecoeverOrNot()
$$

其含义是：只要 deadlock 发生，所有 server buffer 中本来可恢复的 packet 都应已经被回复。

论文还给出了 active part of buffer 的解析公式之一：

$$
APB = \sum_{Pkt=1}^{\infty} BS - \frac{DR \times IPD}{8 \times Pkt}
$$

上式中的符号逐项解释如下：

1. `APB` 是 active part of buffer。
2. `BS` 是 buffer size。
3. `DR` 是 data rate。
4. `IPD` 是 inter-packet delay。
5. `Pkt` 是 packet sequence number。
6. 该式用于解释为什么 source/client 速率差和 `IPD` 会持续侵蚀有效缓冲空间。

### 语义边界

这篇论文的边界主要有：

1. buffer size、packet count、client/receiver 数量都被有限化，以避免 state explosion。
2. 协议行为主要围绕 sequence、buffer 和 delay，不建模真实底层网络的全部细节。
3. 重点是功能性 protocol requirements，不是链路层概率丢包模型。
4. 原文结论依赖离散化的参数设置和有限客户端规模。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 协议网络 | `$\mathcal{N}_{cprp} = A_{src} \parallel A_{srv} \parallel (\bigparallel_i A_{cli,i}) \parallel (\bigparallel_j A_{rcv,j})$` | source / server / client / receiver 统一建模。 |
| deadlock 约束 | `$A[]\ deadlock\ \text{imply}\ Source.Packet == totalPackets$` | 只有 source 发完包后才允许停机。 |
| repair 完整性 | `$A[]\ deadlock\ \text{imply}\ all\_avaliable\_packets\_RecoeverOrNot()$` | server 中可恢复的包不应遗留未回复。 |
| client 丢包处理 | `$A[]\ Client.Packet2send == Client.lastReceivedPkt\ \text{imply}\ allmisspacketsOrNacked()$` | client 在发送最后观测包时，不应还留有未 NACK 的丢包。 |
| recovered packet 完整性 | `$A[]\ forall(i:id_t)\ Client(i).Recovered\_pkt\_lost < 1$` | 恢复包不能落到“收到但发不出去”的状态。 |
| 缓冲区分析 | `$APB = \sum_{Pkt=1}^{\infty} BS - \frac{DR \times IPD}{8 \times Pkt}$` | 解释 `IPD` 和速率差对有效缓冲区的侵蚀。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | source/server/client/receiver 都有显式协议状态。 |
| 事件 / 触发 | 很强 | `SendPkt`、`SendNack`、`SendRepairPkt` 等事件是主体。 |
| 守卫 / 数据 | 强支持 | buffer 数组、sequence number、retry count 和 guards 都进入模型。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 很强 | 多 client、多 receiver 与 server/source 并发通信是核心。 |
| 时间约束 | 强支持 | packet send/repair delay 与 `IPD` 都进入时序分析。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散协议与缓冲区行为。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 可直接给出 requirement violation trace。 |

### 形式化问题与性质

1. 论文真正有价值的不是“又一个协议用了 `UPPAAL`”，而是它把 buffer overwrite、repair race 和 sequence-ordering 缺陷都显式结构化了。
2. 这类条目很适合作为 `Timed Automata` 在协议 / 分布式系统侧的应用代表。
3. 它也说明：协议的 QoS claim 不能只凭仿真或经验，状态机化后很多边界条件会直接暴露。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 拆出 source、server、client、receiver 四类进程。
2. 把 playback / repair / NACK buffer、front/rear 指针和 sequence number 建成离散变量。
3. 用 broadcast / unicast channel 连接协议动作。
4. 把需求整理成 `R1-R4` 四类查询。
5. 再用 `APB` 公式分析 `DR` 与 `IPD` 的参数影响。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata templates。
2. buffer arrays 与辅助函数。
3. broadcast / unicast channels。
4. `A[]` 形式的 safety queries。

### 交换与互操作

论文的互操作重点在：

1. 协议结构到 timed automata network 的映射；
2. protocol requirements 到 `UPPAAL` query 的映射；
3. verification trace 再回流解释为 buffer malfunction scenarios。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：无独立交换标准；直接在 `UPPAAL` 模型中承载。
- 仿真/执行支持：支持行为仿真和 diagnostic trace。
- 验证/分析支持：`UPPAAL` verifier + requirements + counterexample generation。
- 代码生成/转换支持：原文未提供协议实现代码生成链。
- 标准化或社区生态：属于 `Timed Automata` 在通信协议 / QoS 分析上的典型应用路线。

## 适用场景与需求前提

### 适用场景

适合 multicast / video-distribution 一类带 repair server、NACK queue 和有限缓冲区的实时协议分析，尤其适合查找顺序恢复与 buffer overwrite 缺陷。

### 需求前提

1. 协议动作和 packet sequence 必须可有限化。
2. buffer 结构、queue 规则和 retry policy 必须可显式建模。
3. 关键 correctness 目标应能压成 safety / deadlock / ordering requirements。

### 不适用或高成本场景

如果协议依赖大规模开放网络、复杂概率丢包模型或难以有限化的拓扑变化，仅靠这里的离散 `TA` 网络会失真或爆炸。

## 与相邻形式主义的关系

相对 [verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md](../verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md)，本文焦点是 buffer / NACK / repair 顺序，而不是 token-based scheduling；相对 [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)，这里的对象是 multicast packet recovery 协议，而不是总线仲裁；相对 [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，这篇更突出对“协议原 claim 是否成立”的反例式审计。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提醒我们：当需求里出现缓存、重试、补偿和丢失恢复时，状态机建模不能只画高层交互，还要把 buffer semantics 变成一等对象。

### 作为目标形式主义还是中间表示

对协议验证，它可以直接作为目标形式主义；对更大的系统设计流程，它也适合作为通信子系统的时序中间表示。

### 对需求到模型生成的启发

1. `NACK`、repair、buffer overwrite 这类机制要显式提取成状态与变量。
2. 协议 claim 很适合整理成 `A[]` 风格 requirement queries。
3. 若需求还涉及 QoS 参数调优，模型里应保留 `IPD`、`DR` 和 buffer size 等参数入口。

### 现实限制

这类协议模型最容易遇到 state explosion，因此需求抽取时要谨慎控制 client 数、buffer 大小和 packet 数的有限化口径。

## 重要的相关工作

- [verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md](../verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md)：同样是协议级 `TA` 应用，但对象是工业 fieldbus 调度。
- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：另一篇总线/协议验证条目，可对照其更接近嵌入式网络仲裁的问题结构。
- [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：更早的工业协议调试案例，展示了 `TA` 在真实协议缺陷定位上的另一条落地路线。

## 文献分类总结

- 主类：⏱️
- 描述客体：🤝
- 所属领域：🌐
- 形式主义：`Timed Automata / Cooperative Packet Recovery Protocol Model`
- 论文角色：协议缺陷分析 / 定时自动机应用建模
- 核心功能：用 `UPPAAL` 找出 packet recovery、buffer overwrite 和顺序恢复缺陷
- 关键特性：NACK、repair buffer、sequence numbers、`IPD`、formal requirements
- 构造方式：source/server/client/receiver `TA` + buffers + requirement queries
- 基础设施：`UPPAAL`
- 适用场景：multicast packet recovery、QoS-oriented protocol analysis
- 需求前提：buffer、包序号和时延规则需可有限化
- 状态：🟢
