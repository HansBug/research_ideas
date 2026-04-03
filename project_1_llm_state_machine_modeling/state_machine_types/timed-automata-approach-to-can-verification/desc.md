# 用于 CAN 验证的定时自动机方法 / Timed Automata Approach to CAN Verification

## 基本信息

- 标题：Timed Automata Approach to CAN Verification
- 中文标题：用于 CAN 验证的定时自动机方法
- 作者：Jan Krakora, Zdenek Hanzalek
- 发表：*IFAC Proceedings Volumes*, 37(4):147-152, 2004
- DOI：`10.1016/S1474-6670(17)36111-6`
- 链接：https://doi.org/10.1016/S1474-6670(17)36111-6
- 形式主义：`Timed Automata / UPPAAL Network for CAN Verification`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`CAN` 总线实时验证 / 定时自动机应用建模
- 工具/实现获取方式：原文明确基于 `UPPAAL` 建立 `CAN` 仲裁、收发器、总线与应用进程模型，并用模型检查查询验证死锁、仲裁失败与截止期性质；论文未给独立代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` 风格的 timed automata network、时钟约束、同步动作和查询公式；原文未给独立交换标准。

## 简报

这篇论文处理的是一个很典型的实时嵌入式问题：多个处理器通过 `CAN` 总线广播发送消息时，光有最坏响应时间公式还不够，系统还需要知道会不会死锁、两个处理器会不会“同时成功发送”、最高优先级消息是否可能意外输掉仲裁，以及实际 deadline 是否满足。作者的做法是把 `CAN` 仲裁、收发器、总线和应用进程都压成定时自动机，并把这些自动机交给 `UPPAAL` 做组合验证。

- 形式主义定位：这是 `Timed Automata` 主干上的应用型条目，核心价值是把 `CAN` 总线时序与仲裁逻辑落成可模型检查的时钟自动机网络。
- 构造方式简述：把 arbitration、transceiver、bus、application process 分别建模成 timed automata，再通过同步动作和时钟约束表达总线占用、优先级比较、消息传输时长与 deadline。
- 基础设施与场景简述：依托 `UPPAAL` 查询语言与 `CAN` 协议结构，服务汽车电子、分布式控制器、实时广播总线与 `OSEK` 一类实时操作系统场景。

```text
message period / priority / transmission time -> arbitration + transceiver + bus timed automata -> UPPAAL queries -> deadlock / arbitration / deadline / response-time verification
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `CAN` 总线上的 application processes 与其周期/截止期参数。
2. 表达仲裁逻辑的 arbitration automaton。
3. 每个处理器对应的 transceiver automaton。
4. 表达总线占用与比特发送时长的 bus automaton。
5. 记录 deadline 与 response time 的 clocks / timers。
6. 用 `UPPAAL` 查询语言写成的时序与可达性性质。

### 核心抽象

原文以 `UPPAAL` 图模型给出 `CAN` 各部件的 timed automata。结合文中的建模说明，可把单个 timed automaton 保守整理为：

$$
A = \langle L, l_0, C, \Sigma, E, Inv \rangle
$$

上式中的符号逐项解释如下：

1. `L` 是位置集合，对应仲裁、请求、发送、等待等离散阶段。
2. `l_0 \in L` 是初始位置。
3. `C` 是时钟集合，用来记录发送持续时间、等待时间和响应时间。
4. `\Sigma` 是同步动作集合，例如请求、成功发送、发送被拒绝等事件。
5. `E \subseteq L \times \Sigma \times \Phi(C) \times 2^C \times L` 是迁移集合，其中 `\Phi(C)` 表示时钟守卫，`2^C` 表示时钟复位集合。
6. `Inv : L \to \Phi(C)` 为位置不变式，约束系统在某位置可停留的最长时间。
7. 这一定义是基于论文中的 `UPPAAL` 建模结构做的保守符号化整理；论文正文主要以图示 automata 给出细节。

整网模型可保守记成：

$$
\mathcal{N}_{CAN} = A_{arb} \parallel A_{bus} \parallel (A_{tr,1} \parallel A_{proc,1}) \parallel \cdots \parallel (A_{tr,n} \parallel A_{proc,n})
$$

上式中的符号逐项解释如下：

1. `A_{arb}` 是仲裁自动机。
2. `A_{bus}` 是总线自动机。
3. `A_{tr,i}` 是第 `i` 个节点的收发器自动机。
4. `A_{proc,i}` 是第 `i` 个应用进程自动机。
5. `\parallel` 表示按同步动作组合的 timed automata network。
6. 该网络的目标是共同表达固定优先级广播、总线共享与进程级 deadline 约束。

论文中的响应时间分析目标可整理为：

$$
R_m = C_m + J_m + w_m
$$

上式中的符号逐项解释如下：

1. `R_m` 是标识符为 `m` 的消息最坏响应时间。
2. `C_m` 是消息自身传输时间。
3. `J_m` 是进程释放抖动或操作系统延迟。
4. `w_m` 是因总线忙碌和更高优先级消息竞争引入的等待时间。
5. 论文把这一响应时间目标与 `UPPAAL` 查询结合，用来检查给定 `Deadline` 是否可满足。

### 一个最小例子与通俗解释

最直观的例子就是两个处理器同时争夺 `CAN` 总线：

1. `Processor 1` 与 `Processor 2` 几乎同时发起发送请求。
2. 两个 transceiver 都进入请求状态，并把各自 message identifier 交给仲裁逻辑。
3. 由于 `CAN` 是固定优先级仲裁，标识符更高优先级的一方保留发送权，另一方被拒绝并等待下一轮。
4. `UPPAAL` 可以继续检查：这种竞争是否会导致死锁？最高优先级消息会不会反常失败？最后是否还能赶上 deadline？

通俗地说，这个模型像“把总线争用现场拆成几台带秒表的状态机”。普通 `FSM` 只能说“先请求再发送”，而 timed automata 还能说“必须在多久内发送完”“等待多久后算违约”“同一时刻是谁赢仲裁”。

### 运行 / 接受 / 转移语义

论文中的运行语义重点有四层：

1. application process 按周期释放消息并启动本地 response-time 计时。
2. transceiver 将本地请求送入 arbitration automaton，等待 `request_success` 或 `request_denied`。
3. arbitration automaton 依据 fixed priority 选择当前可占用总线的请求。
4. bus automaton 用时钟表达帧传输持续时间，并在发送结束后释放总线。

原文给出的核心 `UPPAAL` 性质，按标准记号可整理为：

$$
A[]\ \neg deadlock
$$

以及

$$
E\Diamond (Transceiver_1.request\_success \land Transceiver_2.request\_success)
$$

上式中的符号逐项解释如下：

1. `A[]` 表示“对所有执行路径上的所有时刻都成立”。
2. `\neg deadlock` 表示系统不能进入无后继动作的死锁状态。
3. `E\Diamond` 表示“存在一条执行路径最终到达某状态”。
4. 第二条性质检查两个 transceiver 是否都可能成功完成请求。
5. 论文还给出了 `E\Diamond(Transceiver_1.request_denied)` 来检查仲裁失败是否可能发生。

针对 deadline 与最坏响应时间，论文又检查：

$$
A[](Process_m.trans\_finished \Rightarrow Process_m.t\_{response\_time} < Deadline)
$$

以及

$$
A[](Process_m.trans\_finished \Rightarrow Process_m.t\_{response\_time} < R_m)
$$

上式中的符号逐项解释如下：

1. `Process_m.trans_finished` 表示消息 `m` 已完成发送。
2. `Process_m.t_{response_time}` 是进程 `m` 的响应时间时钟或统计量。
3. `Deadline` 是给定的时限阈值。
4. `R_m` 是通过迭代验证得到的最坏响应时间上界。
5. 这两条性质分别回答“给定 deadline 是否满足”与“最坏响应时间上界是多少”。

### 语义边界

这篇论文的边界主要在于：

1. 主体关注 `CAN` 仲裁与消息时序，而不是上层复杂应用逻辑。
2. 模型假定系统可以离散成固定优先级消息、传输时长和有限个节点。
3. `UPPAAL` 模型对协议关键路径做了抽象，不等价于逐位仿真真实硬件。
4. 文中主要讨论离散时间约束与消息级性质，不涉及连续动力学。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单个 automaton 骨架 | `$A = \langle L, l_0, C, \Sigma, E, Inv \rangle$` | 用 clocks、guards 和 invariants 表达总线部件的时序行为。 |
| `CAN` 网络组合 | `$\mathcal{N}_{CAN} = A_{arb} \parallel A_{bus} \parallel (A_{tr,1} \parallel A_{proc,1}) \parallel \cdots \parallel (A_{tr,n} \parallel A_{proc,n})$` | 把仲裁、总线、收发器和进程连成一个可检网络。 |
| 死锁自由 | `$A[]\ \neg deadlock$` | 检查系统是否可能卡死。 |
| 仲裁可达性 | `$E\Diamond(Transceiver_1.request\_success \land Transceiver_2.request\_success)$` | 检查两个处理器是否都可能成功发送。 |
| 优先级失败可达性 | `$E\Diamond(Transceiver_1.request\_denied)$` | 检查某个请求是否会输掉仲裁。 |
| 响应时间目标 | `$R_m = C_m + J_m + w_m$` | 把传输、抖动和等待统一成最坏响应时间目标。 |
| deadline 检查 | `$A[](Process_m.trans\_finished \Rightarrow Process_m.t_{response\_time} < Deadline)$` | 判断消息是否能在时限内完成。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仲裁、请求、发送、等待等阶段都是显式位置。 |
| 事件 / 触发 | 强支持 | request success / denied、process release、send finished 是主体。 |
| 守卫 / 数据 | 部分支持 | 重点是 identifier、deadline、timer，而不是复杂数据流。 |
| 层次 | 不支持 | 原文使用平铺的 network，而非层次状态机。 |
| 并发 / 同步 | 强支持 | 多节点并行、同步动作和共享总线竞争是主体。 |
| 时间约束 | 强支持 | clocks、invariants、deadline、response time 是核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散实时时序模型。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 可直接检查死锁、仲裁与 deadline 性质。 |

### 形式化问题与性质

1. 论文把“总线竞争是否满足实时性”从解析公式推广到“协议 + 应用 + 仲裁”联合模型检查。
2. 除了 deadline，它还显式检查 deadlock 与 arbitration anomaly，这比只算响应时间更完整。
3. 由于模型是 modular 的，作者还指出后续可扩展到 `TT-CAN`。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 枚举每个 processor 的周期消息与优先级。
2. 为 arbitration、bus、transceiver、process 分别构建 timed automata。
3. 用 clocks 表达 transmission time、response time 与 deadline。
4. 用同步动作表达请求、仲裁成功/失败与发送完成。
5. 写出 `UPPAAL` 查询以检查死锁、可达性与实时性。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` 风格 timed automata 图模型。
2. message timing 参数与 process 参数表。
3. `UPPAAL` 查询公式。

### 交换与互操作

互操作重点在：

1. 应用进程参数如何映射为 process automata。
2. 总线仲裁结果如何同步到 transceiver 状态。
3. response-time 统计如何通过 clocks 回传给性质查询。

## 配套基础设施

- 建模/编辑工具：原文直接使用 `UPPAAL` 风格 timed automata 建模。
- 解析/交换/元模型支持：有 `UPPAAL` 查询与模型结构，但无独立交换标准。
- 仿真/执行支持：论文主体不强调部署执行，重点在模型检查。
- 验证/分析支持：支持死锁分析、仲裁可达性、deadline 检查和最坏响应时间迭代求解。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 `CAN` 协议、实时系统分析和 `UPPAAL` 社区生态。

## 适用场景与需求前提

### 适用场景

适合汽车电子、分布式嵌入式控制器、工业总线消息调度以及一切“固定优先级广播 + 明确 deadline”的 `CAN` 类系统。

### 需求前提

1. 系统通信可抽成有限个周期/偶发消息。
2. 优先级、传输时长和 deadline 可显式给出。
3. 关注点在仲裁、等待与截止期，而不是复杂数据路径。
4. 节点数和关键交互规模可被模型检查工具接受。

### 不适用或高成本场景

如果系统主要问题在大规模数据载荷、复杂应用协议栈或连续控制闭环，仅靠这里的 message-level timed automata 抽象会过于粗粒度。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文不是奠基定义，而是把 clocks 和 deadline 落到了 `CAN` 总线验证上；相对 [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，这里更聚焦固定优先级广播与响应时间，而不是工业现场总线的实现缺陷诊断；相对 [Automatic Verification of Component-Based Real-Time CORBA Applications](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)，本文对象更靠近底层总线协议而不是组件化中间件。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求中明确出现“优先级、总线共享、deadline、最坏响应时间”时，生成的状态机不该只是普通消息流程，而应显式保留时钟、等待与仲裁语义。

### 作为目标形式主义还是中间表示

对实时通信验证，它可以直接作为目标形式主义；对更大的控制系统需求链路，它也适合作为通信子系统的中间时序表示。

### 对需求到模型生成的启发

1. 需求里的“谁先占总线、等待多久算超时、谁可能被拒绝”都应转成 timed transitions 和 queries。
2. message identifier、周期和 deadline 是非常稳定的结构化输入，可直接抽进模型。
3. 性质生成不能只产出 safety / liveness，还要自动补 `response time` 与 `deadline` 查询。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：提供本文所依赖的 timed automata 理论底座。
- [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：同样面向总线/协议的定时自动机应用，但更偏实现缺陷调试。
- [Automatic Verification of Component-Based Real-Time CORBA Applications](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)：同样用 `UPPAAL` 验证实时组件交互，但应用层级更高。
- [Formal Verification of ROS-Based Robotic Applications Using Timed-Automata](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：展示 timed automata 如何继续推广到机器人中间件通信。

## 文献分类总结

- 这是一篇 `⏱️` 类应用型条目，核心价值是把 `CAN` 总线仲裁、消息发送和 deadline 检查落实为 `UPPAAL` 可验证的 timed automata network。
- 它描述的是总线上的节点交互和通信协议行为，因此记为 `🤝`；论文主要语境是实时嵌入式通信系统，因此记为 `⏱️`。
- 对 `project_1` 来说，它提示我们后续在做实时控制需求建模时，要把“仲裁、等待、最坏响应时间”当成一等建模对象，而不是事后附注。
