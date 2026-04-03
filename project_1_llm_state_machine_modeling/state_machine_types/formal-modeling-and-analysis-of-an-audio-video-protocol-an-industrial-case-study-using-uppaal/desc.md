# 音视频协议的形式化建模与分析：一个使用 UPPAAL 的工业案例 / Formal Modeling and Analysis of an Audio/Video Protocol: An Industrial Case Study Using UPPAAL

## 基本信息

- 标题：Formal Modeling and Analysis of an Audio/Video Protocol: An Industrial Case Study Using UPPAAL
- 中文标题：音视频协议的形式化建模与分析：一个使用 UPPAAL 的工业案例
- 作者：Klaus Havelund, Arne Skou, Kim G. Larsen, Kristian Lund
- 发表：*BRICS Report Series*, Vol. 4, No. 31, November 1997
- DOI：`10.7146/brics.v4i31.18957`
- 链接：https://doi.org/10.7146/brics.v4i31.18957
- 形式主义：`Timed Automata / Audio-Video Bus Protocol Model`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：⏱️
- 论文角色：工业音视频总线协议验证 / 定时自动机应用建模
- 工具/实现获取方式：原文把 B&O 协议压成 `9` 个 `UPPAAL` timed automata，并利用最短 diagnostic trace 找到真实实现 bug；论文未给公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata、共享 bus 变量、observer 和查询公式；不是独立交换标准。

## 简报

这篇论文是 `UPPAAL` 工业案例里的经典条目之一。作者面对的是 B&O 一套已运行多年的音视频总线协议，原实现是 `2800` 行汇编加少量流程图，已知“偶尔丢消息”但找不到根因。论文把协议发送端、碰撞检测器、frame generator、observer 和共享 bus 压成 `9` 个 timed automata，最终自动得到一条错误 trace 并定位出 collision-detection 的时间漏洞。

- 形式主义定位：这是 `Timed Automata` 主干上的工业通信协议应用条目，重点是共享 bus、collision detection 和诊断 trace。
- 构造方式简述：用 `Bus + SenderSystem A + SenderSystem B` 组成网络，每个 sender system 再拆成 `Sender`、`Detector`、`FrameGenerator`、`Observer`。
- 基础设施与场景简述：依托 `UPPAAL` 的仿真、最短错误轨迹和 committed nodes，服务嵌入式共享总线协议的建模、调试和修复。

```text
低层汇编/流程图协议 -> bus/sender/detector/frame-generator timed automata -> UPPAAL trace analysis -> collision bug 定位与修复验证
```

## 形式主义定义与核心对象

### 定义对象

论文里的关键对象包括：

1. 音视频组件共享的一条 broadcast bus。
2. 两个对称的 sender system：`A` 和 `B`。
3. 每个 sender system 内的 `Sender`、`Detector`、`FrameGenerator`、`Observer`。
4. `T5/T1/T2/T3/T4` 消息序列和 jamming signal。
5. collision detection 所依赖的 `S1/S2/W` 采样点和 timing parameters。

### 核心抽象

协议帧语法可直接压成：

$$
frame ::= T5 \cdot \alpha \cdot T4, \qquad \alpha \in \{T1,T2,T3\}^{\ge 15}
$$

上式中的符号逐项解释如下：

1. `$T5$` 是 frame 开始和 bus reservation 标记。
2. `$\alpha$` 是至少 `15` 个数据符号组成的主体。
3. `$T4$` 是 frame 结束和 bus release 标记。
4. `$\{T1,T2,T3\}^{\ge 15}$` 表示主体由 `T1/T2/T3` 构成，长度至少为 `15`。

协议网络可整理为：

$$
\mathcal{N}_{av} = Bus \parallel A_{sender} \parallel A_{detector} \parallel A_{fg} \parallel A_{obs} \parallel B_{sender} \parallel B_{detector} \parallel B_{fg} \parallel B_{obs}
$$

上式中的符号逐项解释如下：

1. `$Bus$` 是共享总线 automaton。
2. `$A_{sender}, B_{sender}$` 是两个发送控制 automata。
3. `$A_{detector}, B_{detector}$` 负责碰撞检测。
4. `$A_{fg}, B_{fg}$` 负责 frame-generator 细节。
5. `$A_{obs}, B_{obs}$` 用于观察 frame 是否在未检测碰撞时被破坏。

bus 的合成规则在论文中极其关键，可以压成：

$$
bus = APn \land BPn
$$

上式中的符号逐项解释如下：

1. `$APn$` 和 `$BPn$` 分别是两个 sender 当前输出到 bus 的寄存器值。
2. `$\land$` 表示由于 `0V` 优先，bus 行为等价于逻辑与。
3. 这条简单规则正是 collision 何时被观察到的物理抽象。

### 一个最小例子与通俗解释

最小例子可以看成 A 和 B 试图几乎同时占用总线：

1. A 在初始化阶段检测到 bus 空闲，于是准备发 `T5`。
2. B 也做了同样判断，并在很接近的时刻开始发送。
3. `Detector` 在每个 `S2` 点比较采样值 `s1/s2` 与本地输出 `pf/pn` 是否一致。
4. 一旦不一致，协议要求进入 collision handling，并可能发 jamming signal。

通俗地说，这像“两个人同时抢着说话，但协议要求双方都得意识到自己撞车了”。timed automata 的价值在于，它不仅能表达“撞了”，还能表达“在第几个采样点才看出来”“如果检测太早停止，谁会误以为自己其实没撞”。

### 运行 / 接受 / 转移语义

论文最重要的正确性性质是 observer 公式：

$$
A[]\ (A\_eof = 1 \rightarrow (A\_diff = 0 \land B\_res = 0))
$$

上式中的符号逐项解释如下：

1. `$A[]$` 表示对所有路径上的所有状态都成立。
2. `$A\_eof = 1$` 表示 sender `A` 已完成一帧发送。
3. `$A\_diff = 0$` 表示 `A` 发出的 frame 未被破坏。
4. `$B\_res = 0$` 表示 `B` 没有在这次发送中检测到碰撞。
5. 该式要求：若 `A` 认为自己已成功发完一帧，则不能出现“实际 frame 被破坏但只有 B 发现冲突”的情况。

论文还给出了 protocol correctness 的自然语言核心，可保守压成：

$$
destroyed(X) \rightarrow detect(X), \qquad detect(X) \rightarrow detect(Y)
$$

上式中的符号逐项解释如下：

1. `$destroyed(X)$` 表示 sender `$X$` 的 frame 被另一个 sender 破坏。
2. `$detect(X)$` 表示 sender `$X$` 检测到了 collision。
3. 第二个蕴含表示：如果一个发送方看到了 collision，另一个同时发送的发送方也应该看到。

### 语义边界

这篇论文的边界主要有：

1. 只建 sender-side behavior，不建完整 receiver 语义。
2. 有效模型是经过抽象和削减的，不是 `2800` 行汇编逐语句仿真。
3. 重点在 collision detection，而不是完整业务 payload 内容。
4. 真实物理层只保留到 `0V/5V` 和采样时序这一层。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 帧语法 | `$frame ::= T5 \cdot \alpha \cdot T4,\ \alpha \in \{T1,T2,T3\}^{\ge 15}$` | 明确 reservation、payload 和 release 结构。 |
| 系统组合 | `$\mathcal{N}_{av} = Bus \parallel A_{sender} \parallel \cdots \parallel B_{obs}$` | `9` 个 timed automata 组成最终 validated model。 |
| 总线抽象 | `$bus = APn \land BPn$` | 把 `0V` 优先的物理规则压成可验证布尔语义。 |
| observer 正确性 | `$A[]\ (A\_eof = 1 \rightarrow (A\_diff = 0 \land B\_res = 0))$` | `A` 成功发送时不能暗中发生 frame destruction。 |
| collision correctness | `$destroyed(X) \rightarrow detect(X),\ detect(X) \rightarrow detect(Y)$` | frame 一旦被撞坏，相关发送者都应意识到 collision。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | initialization、transmission、collision handling 等 phase 很清晰。 |
| 事件 / 触发 | 强支持 | `T5/T1/T2/T3/T4`、jamming、`zero/one`、`Aframe/A_new_Pn` 等事件是核心。 |
| 守卫 / 数据 | 强支持 | `A_stop`、`A_eof`、bus samples 和 delay guards 决定协议行为。 |
| 层次 | 弱支持 | 不是层次状态机，但 sender system 内部做了模块分解。 |
| 并发 / 同步 | 强支持 | 两个 sender system 竞争共享 bus，本质就是并发同步问题。 |
| 时间约束 | 强支持 | reaction delay、output delay、frame gap、collision-detection point 都是显式时间条件。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散总线时序模型。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 仿真和 shortest diagnostic trace 直接定位实现 bug。 |

### 形式化问题与性质

1. 论文的最大价值在于证明：老问题“偶发丢消息”可以通过 timed automata 自动定位，而不是只能靠长期测试碰运气。
2. `DetectionStopRule` 过早停止碰撞检测，是一个极其典型的“只有时序模型才能看见”的 bug。
3. committed nodes 的大量使用说明，这类协议往往需要原子化小段动作，否则模型会引入伪行为。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先把汇编和流程图中的协议规则提炼成 bus reservation、frame gap、collision detection 等规则。
2. 再把 bus、sender、detector、frame generator、observer 分别建模。
3. 用共享变量记录 bus 输出和 frame 完成状态。
4. 通过 observer 公式和 diagnostic trace 验证/调试实现。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` 图形 timed automata。
2. 共享变量，如 `APn/BPn`、`A_eof`、`A_stop`、`A_diff`。
3. 同步通道，如 `zero/one`、`Aframe`、`A_new_Pn`。
4. `UPPAAL` 查询和 shortest diagnostic trace。

### 交换与互操作

互操作重点在：

1. sender 与 detector 通过同步点和共享 bus 变量耦合。
2. frame generator 为 sender 提供可执行的 bit-level frame 展开。
3. observer 只读协议状态，不改变原协议控制流。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 与 `Autograph` 风格的图形建模。
- 解析/交换/元模型支持：无独立标准格式；模型直接承载在 `UPPAAL` 描述中。
- 仿真/执行支持：`UPPAAL` simulator 用于快速发现早期建模错误。
- 验证/分析支持：支持 shortest diagnostic trace、observer property 和 deadlock 检查。
- 代码生成/转换支持：原文未提供代码生成链。
- 标准化或社区生态：依托 `UPPAAL` 工具链和工业协议调试流程。

## 适用场景与需求前提

### 适用场景

适合共享总线、显式采样点、collision detection 和严格发送时序主导的嵌入式通信协议。

### 需求前提

1. 关键协议规则可以离散化成有限 phase 和时序窗口。
2. bug 主要发生在 timing / sampling / collision 逻辑，而不是复杂数据内容。
3. 共享 bus 的物理层能被保守抽象为有限值和固定 delay。

### 不适用或高成本场景

如果协议核心问题在概率噪声、复杂模拟电气特性或大规模多节点数据路由，只用这里的抽象会过于粗粒度。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是工业 bus protocol 的经典落地；相对 [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，它更强调 collision detection bug 而非 broader field-bus 结构；相对 [formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md](../formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md)，两者都属于 B&O 场景，但一个是 bus 协议，一个是 power controller。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：从低层实现材料里抽状态机并不一定要先有漂亮设计文档，很多时候汇编、流程图和采样规则就足够生成 timed automata 骨架。

### 作为目标形式主义还是中间表示

对总线协议验证，它可以直接作为目标形式主义；对更大的控制系统，也适合作为通信子系统的验证中间表示。

### 对需求到模型生成的启发

1. 需要显式抽取 sampling points 和 timing constants。
2. observer automata 很适合承接“实现不该偷偷出错”的需求。
3. 真实 bug 往往埋在“最后一次检测何时停止”这类时序边界条件里。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文依赖的 timed automata 理论基础。
- [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：同样是工业总线协议 `UPPAAL` 案例。
- [formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md](../formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md)：同样是 B&O 语境下的 `UPPAAL` 工业案例。

## 文献分类总结

- 形式主义：`Timed Automata / Audio-Video Bus Protocol Model`
- 成熟度：`UPPAAL` 工具链、observer 技法和 diagnostic debugging 路线都非常成熟。
- 条目价值：这是一篇 `⏱️` 类工业协议应用条目，核心价值在于用 timed automata 真正找出并修复了长期存在的 bus-collision bug。
