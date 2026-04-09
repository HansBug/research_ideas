# 有界重传协议的建模与验证 / Modeling and Verifying a Bounded Retransmission Protocol

## 基本信息

- 标题：Modeling and Verifying a Bounded Retransmission Protocol
- 中文标题：有界重传协议的建模与验证
- 作者：Pedro R. d'Argenio, Joost-Pieter Katoen, Jan Tretmans, Theo C. Ruys
- 发表：*Proceedings of COST 247 Workshop on Applied Formal Methods in System Design*, pp. 114-127, 1996
- DOI：原文未提供
- 链接：https://research.utwente.nl/en/publications/modeling-and-verifying-a-bounded-retransmission-protocol
- 形式主义：`Timed Automata / Bounded Retransmission Protocol Network`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：文件传输协议验证 / 定时自动机应用建模
- 工具/实现获取方式：原文把 sender、receiver 和两条 lossy channel 写成 `UPPAAL` 网络，并与 `Spin` 的 untimed 版本做对照；论文未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、服务逻辑公式和 handshake channel；不是独立交换标准。

## 简报

这篇论文研究的是一个“不是一定能成功”的文件传输协议。它基于 alternating bit protocol，但每个 chunk 只能重传有限次，所以协议可能在超时后放弃整次传输。作者把 sender、receiver 以及两条 lossy channel 压成 timed automata network，用它分析哪些正确性 actually 依赖实时间语义。

- 形式主义定位：这是 `Timed Automata` 主干上的经典协议应用条目，重点是“bounded retransmission + timeout + lossy channel”如何被精确地压成 clocks/guards。
- 构造方式简述：用 `S || R || K || L` 组成网络，其中 `S/R` 各自带 timer，`K/L` 建模 one-message-capacity 的 lossy channel。
- 基础设施与场景简述：依托 `UPPAAL` 做 timed verification，并把服务要求写成逻辑公式，用于判断协议是否符合 file-transfer service。

```text
file-transfer service + lossy channels + timeout assumptions -> sender/receiver/channel timed automata -> UPPAAL properties -> conformance / timing necessity analysis
```

## 形式主义定义与核心对象

### 定义对象

论文里的关键对象包括：

1. file-transfer service 的逻辑规格。
2. sender `S`，带 timer `T1` 和 retry counter。
3. receiver `R`，带 timer `T2` 和 alternating-bit expectation。
4. 两条 lossy channel：数据通道 `K` 与确认通道 `L`。
5. 五个关键 clocks：`u`、`v`、`w`、`x`、`z`。

### 核心抽象

论文的 timed automaton 骨架可整理为：

$$
A = \langle L, l_0, C, A_c, E, I \rangle
$$

上式中的符号逐项解释如下：

1. `$L$` 是位置集合。
2. `$l_0$` 是初始位置。
3. `$C$` 是 clocks 集合。
4. `$A_c$` 是动作和同步标签集合。
5. `$E$` 是带 guard 和 reset 的边集合。
6. `$I$` 是位置不变式。

协议网络则可以保守压成：

$$
\mathcal{N}_{brp} = S \parallel R \parallel K \parallel L
$$

上式中的符号逐项解释如下：

1. `$S$` 是 sender automaton。
2. `$R$` 是 receiver automaton。
3. `$K$` 是数据通道 automaton。
4. `$L$` 是确认通道 automaton。
5. `$\parallel$` 表示通过 handshake channel 组合出的 timed automata network。

文中还显式给出了接口签名：

$$
F,G : (b,b',ab,d_i), \qquad A,B : ack
$$

上式中的符号逐项解释如下：

1. `$F,G$` 是 sender 与 receiver 之间的数据帧接口。
2. `$b$` 和 `$b'$` 表示 first/last bit。
3. `$ab$` 是 alternating bit。
4. `$d_i$` 是第 `$i$` 个 chunk。
5. `$A,B$` 是确认消息通道。

### 一个最小例子与通俗解释

最小例子可以看成只传一个 chunk：

1. sender 读取文件后进入 `next_frame`，通过 `F!` 发出首个 frame，并把 `x` 设为 `0`。
2. 如果在 `x < T1` 时收到 `B?ack`，sender 就认为该 chunk 传输成功。
3. 如果 `x == T1` 仍未收到 ack，就重传并让 `rc := rc + 1`。
4. 当 `rc == MAX` 仍失败时，sender 输出 `I_DK` 或 `I_NOK`，结束本次传输。

通俗地说，这像“发一个数据块，等一会儿，没回就再发，但最多只试固定次数”。普通 `FSM` 只能说“超时了就重发”，而 timed automata 还能说“多久以内收到 ack 才算这次尝试成功”“多久以后必须 declare failure”“sync delay 需要多大才不会误触发超时”。

### 运行 / 接受 / 转移语义

论文最关键的 timed 假设之一是“不会发生 premature timeout”，它被写成：

$$
T_1 > 2 \cdot TD + \delta
$$

上式中的符号逐项解释如下：

1. `$T_1$` 是 sender timeout 上界。
2. `$TD$` 是单次通道传输延迟上界。
3. `$\delta$` 是 receiver 处理时间。
4. 该式确保确认不会在 sender 已经判超时之后才迟到。

为了满足 abort 后 receiver 先完成清理再开始下一次文件传输，论文还显式加入同步等待：

$$
SYNC > TR
$$

上式中的符号逐项解释如下：

1. `$SYNC$` 是 sender 在失败后额外等待的同步时长。
2. `$TR$` 是 receiver 用于确认 transmission-abort 的等待窗。
3. 这条关系把原本不现实的外部假设改成了协议内部性质。

在服务层面，论文还给出典型一致性性质，例如：

$$
is = I\_OK \rightarrow i_k = I\_OK
$$

上式中的符号逐项解释如下：

1. `$is$` 是 sender 侧最终收到的服务指示。
2. `$I\_OK$` 表示整次传输成功。
3. `$i_k$` 是 receiver 侧最后一个 chunk 的指示。
4. 该式表示 sender 若被告知成功，则 receiver 末项也必须是成功指示。

### 语义边界

这篇论文的边界主要有：

1. 数据内容被高度抽象，重点只在 control data 与 timing。
2. `K/L` 两条通道都只有一个 message capacity。
3. `UPPAAL` 模型最终对文件长度和数据域做了固定化裁剪，以避免 region explosion。
4. 关注的是 stop-and-wait 风格 bounded retransmission，不是大窗口滑动协议。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 骨架 | `$A = \langle L, l_0, C, A_c, E, I \rangle$` | 协议组件都按标准 timed automata 编码。 |
| 协议组合 | `$\mathcal{N}_{brp} = S \parallel R \parallel K \parallel L$` | sender、receiver 和双通道组成完整网络。 |
| 通道签名 | `$F,G : (b,b',ab,d_i), \ A,B : ack$` | 把首尾标志、alternating bit 和确认接口显式结构化。 |
| 无 premature timeout | `$T_1 > 2 \cdot TD + \delta$` | sender 的 timeout 必须晚于最坏消息往返和接收处理。 |
| abort 后同步等待 | `$SYNC > TR$` | 失败后新一轮传输不能早于 receiver 清理完成。 |
| 服务一致性 | `$is = I\_OK \rightarrow i_k = I\_OK$` | sender 若收到成功，则 receiver 末项也必须成功。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | sender/receiver/channel 都有显式 phase。 |
| 事件 / 触发 | 强支持 | `F/G/A/B` 上的握手动作是模型骨架。 |
| 守卫 / 数据 | 强支持 | first/last bit、alternating bit、retry counter 和 service indication 都进入 guard/update。 |
| 层次 | 不支持 | 纯平铺 automata network。 |
| 并发 / 同步 | 强支持 | `S/R/K/L` 通过 handshake 同步构成协议语义。 |
| 时间约束 | 强支持 | `T1/T2/TD/TR/SYNC/MAX` 直接决定正确性。 |
| 连续动态 / 随机性 | 不支持 | 只有离散协议状态和 clocks。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 与 `Spin` 的对照突出 timing 在正确性中的必要性。 |

### 形式化问题与性质

1. 这篇论文的重点不只是“协议可验证”，而是“bounded retransmission 的正确性确实依赖时间建模”。
2. `SYNC` 这类额外等待的引入很有价值，因为它把不现实的环境假设变成了协议可设计要素。
3. 服务逻辑与 timed automata 网络并行存在，说明需求侧和实现侧需要双层形式化。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先把 file-transfer service 写成输入/输出关系。
2. 再把 sender、receiver 与 lossy channels 建模成 timed automata。
3. 用 `T1/T2` 与 `MAX` 表达 bounded retransmission。
4. 最后在 `UPPAAL` 中检查 conformance 所需的关键性质。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` automata 图。
2. `F/G/A/B` 同步通道。
3. clocks 与 retry/data-control 变量。
4. 与服务规格对应的逻辑性质。

### 交换与互操作

互操作重点在：

1. sender 与 receiver 通过通道 `K/L` 间接交换 frame 和 ack。
2. service specification 与 protocol model 通过性质检查对齐。
3. `Spin` 用 untimed 版本复查，强调 timing abstraction 的影响。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`，并辅以 `Spin` 对 untimed 假设做比较。
- 解析/交换/元模型支持：无独立交换标准；模型直接承载在 `UPPAAL/Promela` 描述中。
- 仿真/执行支持：可在 `UPPAAL` 中分析 timeout / retransmission traces。
- 验证/分析支持：支持服务一致性、timeout 假设与 conformance 相关性质。
- 代码生成/转换支持：原文未提供。
- 标准化或社区生态：依托 alternating-bit / communication protocol verification 社区语境。

## 适用场景与需求前提

### 适用场景

适合 bounded retry、lossy channel、硬 timeout 主导的通信协议和嵌入式文件传输服务。

### 需求前提

1. 业务逻辑能抽成 chunk 级 stop-and-wait 交互。
2. timeout、最大通道时延和重试上限明确。
3. 正确性主要落在服务一致性与时限，而不是复杂 payload 数据语义。

### 不适用或高成本场景

如果协议依赖大窗口流控、概率丢包模型或复杂队列化数据结构，这里的抽象会太弱。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是 timed automata 在早期协议验证上的代表案例；相对 [formal-verification-of-a-tdma-protocol-start-up-mechanism/desc.md](../formal-verification-of-a-tdma-protocol-start-up-mechanism/desc.md)，它关注 point-to-point 文件传输而非总线同步；相对 [verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md](../verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md)，它更基础，强调 retransmission / timeout。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：协议需求里的“成功、失败、未知、最大重试次数、超时窗口”都可以直接转成 timed automata 中的状态、clock 和 service property。

### 作为目标形式主义还是中间表示

对实时协议验证，它可以直接作为目标形式主义；对控制系统中的通信子系统，它也适合作为中间验证层。

### 对需求到模型生成的启发

1. 要把服务语义和实现语义分别建模。
2. timeout 假设不应藏在自然语言注释里，必须显式成为公式。
3. `unknown/don't know` 这类灰色结果同样应该保留为模型中的正式输出。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文所依赖的 timed automata 理论底座。
- [formal-verification-of-a-tdma-protocol-start-up-mechanism/desc.md](../formal-verification-of-a-tdma-protocol-start-up-mechanism/desc.md)：同样是协议型 timed automata 条目，但焦点在 TDMA 启动同步。
- [verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md](../verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md)：同属实时总线/协议线条，但对象是调度协议。

## 文献分类总结

- 形式主义：`Timed Automata / Bounded Retransmission Protocol Network`
- 成熟度：协议结构、服务逻辑和 `UPPAAL` 验证链都很清晰，是早期高质量 timed-protocol 案例。
- 条目价值：这是一篇 `⏱️` 类协议应用条目，核心价值在于把 bounded retransmission 的时间假设显式化并验证其必要性。
