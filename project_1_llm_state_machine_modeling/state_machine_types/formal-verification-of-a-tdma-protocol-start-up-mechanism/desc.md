# TDMA 协议启动机制的形式化验证 / Formal Verification of a TDMA Protocol Start-Up Mechanism

## 基本信息

- 标题：Formal Verification of a TDMA Protocol Start-Up Mechanism
- 中文标题：TDMA 协议启动机制的形式化验证
- 作者：Henrik Lonn, Paul Pettersson
- 发表：*1997 IEEE Pacific Rim International Symposium on Fault-Tolerant Systems*, pp. 235-242, 1997
- DOI：`10.1109/PRFTS.1997.640153`
- 链接：https://doi.org/10.1109/PRFTS.1997.640153
- 形式主义：`Timed Automata / DACAPO TDMA Start-Up Network`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：⏱️
- 论文角色：TDMA 启动同步验证 / 定时自动机应用建模
- 工具/实现获取方式：原文把 bus automaton、4 个 station automata 和 1 个 test automaton 建成 `UPPAAL` 网络，并在 guard 上自动注入 `±10^{-3}` clock drift；论文未给公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、bus channels、test automaton 和 invariant formulas；不是独立交换标准。

## 简报

这篇论文研究的不是 TDMA 正常运行时的吞吐，而是“系统刚启动、各节点时钟还没对齐时，能不能在有漂移的情况下自己同步起来”。作者把 `DACAPO` 协议的 bus 与 station 行为压成 timed automata network，并验证 4 个站点从任意初始状态出发都能在有界时间内进入正常模式。

- 形式主义定位：这是 `Timed Automata` 在实时总线启动同步问题上的应用条目，重点是 bus ownership、clock drift 和 recovery-mode 协调。
- 构造方式简述：用 1 个 bus automaton、4 个 station automata 和 1 个 test automaton，通过 `FTOBUS/SOF/JAM` 等信道连接，显式建模 `Bit Clock`、`Node ID Count`、`Error Count` 和 `Mode`。
- 基础设施与场景简述：依托 `UPPAAL` 的 invariant / bounded-liveness 验证，服务安全关键分布式嵌入式系统的 TDMA 启动协议分析。

```text
TDMA slot/rendezvous rules + clock drift -> bus/station/test timed automata -> UPPAAL invariants -> startup convergence / normal-mode correctness
```

## 形式主义定义与核心对象

### 定义对象

论文里的关键对象包括：

1. `DACAPO` 协议中的单总线 TDMA 启动机制。
2. bus automaton，用于表达 `SOF`、冲突和 corrupted frame 生命周期。
3. station automaton，用于表达 `Normal / Resynchronization / Recover` 三种模式。
4. test automaton，用于表达“到 deadline 时全部进入 normal mode”以及“normal mode 下发送顺序正确”。
5. 显式 clock drift，大小对应 `\pm 10^{-3}`。

### 核心抽象

论文对单个站点最有辨识度的形式化抽象是它的局部状态向量：

$$
\{Bitclock\ count,\ Node\ ID\ count,\ Frame\ Error\ count,\ Mode\}
$$

上式中的符号逐项解释如下：

1. `Bitclock count` 表示本地 bit clock 在当前 TDMA slot 内的位置。
2. `Node ID count` 表示当前站点认为“这个 slot 属于谁”。
3. `Frame Error count` 统计空槽或错误帧。
4. `Mode` 取 `Normal`、`Resynchronization` 或 `Recover`。

系统级网络可以保守整理为：

$$
\mathcal{N}_{tdma} = Bus \parallel St_0 \parallel St_1 \parallel St_2 \parallel St_3 \parallel Test
$$

上式中的符号逐项解释如下：

1. `$Bus$` 是共享广播总线 automaton。
2. `$St_i$` 是第 `$i$` 个站点 automaton。
3. `$Test$` 是辅助验证用 automaton。
4. `$\parallel$` 表示由握手通道组成的 timed automata network。

论文还明确给出了 bus 与 station 之间的关键信道集合，可压成：

$$
\Sigma_{bus} = \{FTOBUS, FFROMBUS, SOF, JAMTOBUS, JAMFROMBUS, JAM\}
$$

上式中的符号逐项解释如下：

1. `FTOBUS` 表示发送节点开始向总线广播一帧。
2. `FFROMBUS` 表示正常帧从总线移除。
3. `SOF` 表示接收方观察到 start-of-frame。
4. `JAMTOBUS` 和 `JAMFROMBUS` 分别表示冲突帧进入和离开总线。
5. `JAM` 用于通知接收方 bus activity 是损坏帧而不是有效帧。

### 一个最小例子与通俗解释

最小例子可以把场景想成 4 个站点冷启动：

1. 每个站点一开始的 `bitclock` 和 `idcount` 都可能不同。
2. 某站点如果认为轮到自己，就尝试在自己的 TDMA slot 上发 recovery frame。
3. bus automaton 会把首个发送解释为 `SOF`，后续重叠发送解释为 `JAM`。
4. 站点收到 `SOF` 后把本地 `idcount` 对齐到发送方；收到 `JAM` 或空槽则递增错误计数并继续前进。

通俗地说，这像“几块彼此走得快慢不同的手表，靠总线上谁先说话来慢慢把节拍对齐”。普通 `FSM` 只能表达模式切换，而 timed automata 还能表达“多少时间算一个 slot”“多快多慢的 drift 仍然能收敛”“何时必须从 silence 进入 recover mode”。

### 运行 / 接受 / 转移语义

论文把 timed automata network 的基本验证目标写成 invariant / bounded-liveness 公式。第一条核心性质是：

$$
Inv((not\ test.start) \rightarrow (n == 4))
$$

上式中的符号逐项解释如下：

1. `test.start` 是 test automaton 的初始位置。
2. `not test.start` 表示已经到达 deadline 之后。
3. `$n$` 是当前处于 `Normal` mode 的 station 数量。
4. `n == 4` 表示 4 个站点都已经进入正常模式。

第二条核心性质是：

$$
Inv(not\ test.error)
$$

上式中的符号逐项解释如下：

1. `test.error` 是 test automaton 中表示发送顺序或节拍错误的状态。
2. `Inv(not test.error)` 表示系统永远不应进入该错误状态。
3. 这保证了启动完成后 bus 上确实按 `0,1,2,3,0,1,2,3,\ldots` 的顺序运行。

论文最终还从模型中求出了启动时延上界：

$$
T_{startup}^{max} \approx 21\ \text{TDMA slots}
$$

上式中的符号逐项解释如下：

1. `$T_{startup}^{max}$` 是从任意初始状态到全体进入 `Normal` mode 的最坏时间。
2. `21 TDMA slots` 是 4 节点、含 `\pm 10^{-3}` drift 和首次 collision 场景下的结果。

### 语义边界

这篇论文的边界主要有：

1. 只验证 4 个站点，5 个站点在当时已超出现实可验证资源。
2. 假定 bus 无传播延迟，因为协议可在设计时预补偿。
3. 不考虑新的 transient/permanent communication fault，只考虑初始失步与 collision。
4. recovery set 是预先指定的，不允许所有节点都在 recovery mode 中任意广播。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 站点局部状态 | `$\{Bitclock\ count,\ Node\ ID\ count,\ Frame\ Error\ count,\ Mode\}$` | 把启动同步问题压到 4 个离散/时间核心量上。 |
| 系统组合 | `$\mathcal{N}_{tdma} = Bus \parallel St_0 \parallel St_1 \parallel St_2 \parallel St_3 \parallel Test$` | 用 bus、station 和 test automata 组成完整验证网络。 |
| 总线接口集合 | `$\Sigma_{bus} = \{FTOBUS, FFROMBUS, SOF, JAMTOBUS, JAMFROMBUS, JAM\}$` | 精确刻画正常广播、起始接收和冲突传播语义。 |
| 启动收敛性质 | `$Inv((not\ test.start) \rightarrow (n == 4))$` | 到 deadline 时全部 4 个站点都必须进入 normal mode。 |
| 正常运行性质 | `$Inv(not\ test.error)$` | 收敛后 bus 发送顺序和节拍不得出错。 |
| 最坏启动时间 | `$T_{startup}^{max} \approx 21\ \text{TDMA slots}$` | 量化了 protocol start-up 的最坏恢复代价。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Normal`、`Resynchronization`、`Recover` 是问题核心。 |
| 事件 / 触发 | 强支持 | `SOF`、`JAM`、slot-end、silence count 和 own-slot transmit 都驱动转移。 |
| 守卫 / 数据 | 强支持 | `idcount`、`errcount`、`silence` 和 drift-aware clock guards 决定行为。 |
| 层次 | 弱支持 | 非层次状态机，但 bus/station/test 三层职责分明。 |
| 并发 / 同步 | 强支持 | 4 个站点共享总线并通过同步信道交互。 |
| 时间约束 | 强支持 | 每个 slot、frame、half-window 和 drift 窗口都被显式编码。 |
| 连续动态 / 随机性 | 不支持 | 只有实数时钟和离散模式，不包含连续物理动力学。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 直接给出 invariants 与 startup bound。 |

### 形式化问题与性质

1. 论文真正解决的是“多主节点、无主时钟、带漂移启动”这一类高风险初始化问题。
2. test automaton 的加入很关键，因为它把 bounded-liveness 变成了 invariant 形式。
3. recovery set 的限制说明，有些协议设计约束不是实现细节，而是收敛性成立的必要前提。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先把 TDMA slot、frame 和 reception window 固定成离散时间结构。
2. 再分别建 bus automaton 和 station automaton。
3. 用 `SOF/JAM` 区分成功接收与损坏帧。
4. 用 test automaton 表达收敛和正常运行性质。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata 模板。
2. 全局整数变量，如 `busid`、`idcount_i`、`errcount_i`、`silence_i`、`n`。
3. 显式 bus 通道集合。
4. invariant 公式和 test automaton。

### 交换与互操作

互操作重点在：

1. station 通过 `FTOBUS/SOF/JAM` 与 bus 同步。
2. test automaton 只观察系统状态，不直接参与协议功能。
3. drift 通过对 guard 做区间变换自动注入到 `UPPAAL` 模型里。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：无独立交换标准；模型直接由 `UPPAAL` automata 承载。
- 仿真/执行支持：可在 `UPPAAL` 中重放 startup/collision 场景。
- 验证/分析支持：支持 invariant、bounded-liveness 风格性质和 deadlock 检查。
- 代码生成/转换支持：原文未提供代码生成。
- 标准化或社区生态：依托 `UPPAAL` 与 TDMA safety-critical protocol 分析路线。

## 适用场景与需求前提

### 适用场景

适合安全关键分布式嵌入式系统中的 TDMA 总线启动、重同步和 bus ownership 协议验证。

### 需求前提

1. 系统拓扑规模较小且节点数可固定。
2. slot 长度、reception window 和 drift 上界必须明确。
3. 协议逻辑主要是同步、恢复和时序保证，而不是复杂负载内容。

### 不适用或高成本场景

如果系统包含长总线传播延迟、动态节点加入退出、概率通信故障或大规模节点集，仅靠这里的模型会明显过于理想化或状态爆炸。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是典型的 timed automata 协议落地案例；相对 [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)，它关心启动同步而不是 steady-state bus arbitration；相对 [verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md](../verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md)，它更基础，关注的是 TDMA startup convergence。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里出现“若系统整体失步，必须在多少时隙内恢复一致节拍”这类描述时，timed automata 比普通状态机更合适，因为它能同时表达模式、时间窗和同步语义。

### 作为目标形式主义还是中间表示

对实时通信协议验证，它完全可以作为目标形式主义；对更大的车载/工业系统，它也可作为通信启动子系统的中间验证模型。

### 对需求到模型生成的启发

1. 需要把局部时间表示拆成显式计数器和模式变量。
2. 启动/恢复协议往往需要单独的 test/observer automaton 来表达 deadline 性质。
3. 时钟漂移上界应尽早从自然语言需求中抽取出来，而不是留到实现后期。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文所依赖的 timed automata 理论基础。
- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：同样面向嵌入式总线，但关注运行期仲裁。
- [verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md](../verification-of-a-fieldbus-scheduling-protocol-using-timed-automata/desc.md)：同样是 timed automata 总线协议条目，但焦点是调度合法性和拓扑恢复。

## 文献分类总结

- 形式主义：`Timed Automata / DACAPO TDMA Start-Up Network`
- 成熟度：`UPPAAL` 建模、drift 注入和 test-based invariant 验证链都比较清晰。
- 条目价值：这是一篇 `⏱️` 类实时协议应用条目，核心价值在于展示 timed automata 如何精确承接 TDMA 启动收敛问题。
