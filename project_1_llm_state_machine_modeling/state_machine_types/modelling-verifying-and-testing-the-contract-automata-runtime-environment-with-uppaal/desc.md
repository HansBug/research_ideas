# 使用 Uppaal 对 Contract Automata 运行时环境进行建模、验证与测试 / Modelling, Verifying and Testing the Contract Automata Runtime Environment with Uppaal

## 基本信息

- 标题：Modelling, Verifying and Testing the Contract Automata Runtime Environment with Uppaal
- 中文标题：使用 Uppaal 对 Contract Automata 运行时环境进行建模、验证与测试
- 作者：Davide Basile
- 发表：*Coordination Models and Languages*, pp. 93-110, 2024
- DOI：`10.1007/978-3-031-62697-5_6`
- 链接：https://doi.org/10.1007/978-3-031-62697-5_6
- 形式主义：`Contract Automata / CARE / Uppaal Stochastic Timed Automata Model`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：运行时形式分析 / contract automata middleware verification
- 工具/实现获取方式：原文明确给出 `CARE` 运行时、`RunnableOrchestration` / `RunnableOrchestratedContract` 两个核心 Java 抽象类，以及公开的 `Uppaal` 模型、日志与测试产物仓库。
- 标准/格式获取方式：承载方式是 `CARE` 的 Java/TCP 实现与 `Uppaal` 的 stochastic timed automata network；原文未提供独立行业交换标准。

## 简报

这篇论文不是再定义一种新的契约自动机，而是把已有的 `CARE` 中间件真正压成可验证的运行时通信模型。它把 orchestrator、service、buffer、socket timeout 和 centralised/distributed action 的低层交互全部显式化，然后用 `Uppaal` 的穷举与统计模型检查，检查 deadlock、orphan message、termination 和 configuration consistency 等性质。

- 形式主义定位：面向接口/契约模型运行时落地的形式分析条目，而不是新的组合语义本体。
- 构造方式简述：从 `CARE` 的 Java middleware 出发，抽成 orchestrator template、service template、timeout automata 和 FIFO buffers，再对 choice/action 配置做验证。
- 基础设施与场景简述：依托 `CARE`、`CATLib/CATApp`、`Uppaal`、model-based testing 与 Java sockets，服务 contract-based applications 与 service orchestration runtime。

```text
contract automata orchestration -> CARE Java runtime -> stochastic timed automata network -> Uppaal exhaustive/SMC verification -> deadlock/orphan-message/runtime-consistency evidence
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. `CARE` 中的 orchestrator 与多个 orchestrated services。
2. centralised / distributed 两类 action 执行方式。
3. dictatorial / majoritarian 两类 choice 策略。
4. 用数组实现的 FIFO communication buffers。
5. 用指数分布抽象的 send/read 延迟与 socket timeout 机制。

### 核心抽象

结合原文对全局 declarations、templates 与 timeout automata 的描述，可把验证模型保守整理为：

$$
\mathcal{N}_{CARE} = (\mathcal{O}, \{\mathcal{S}_i\}_{i=1}^{N}, \{\mathcal{T}_i\}_{i=0}^{N}, B, \delta, \lambda)
$$

上式中的符号逐项解释如下：

1. `\mathcal{O}` 是 orchestrator 的 `Uppaal` automaton。
2. `\mathcal{S}_i` 是第 `i` 个 service 的 template instance。
3. `\mathcal{T}_i` 是 orchestrator 与 services 对应的 socket-timeout automata。
4. `B` 是 `CARE` 读写双方共享的 FIFO buffers。
5. `\delta` 是 action/choice 配置，如 `centralised/distributed` 与 `dictatorial/majoritarian`。
6. `\lambda` 是发送与接收的指数分布速率参数。

论文对统计模型检查还显式使用 Chernoff-Hoeffding 型仿真次数界：

$$
N = \left\lceil \frac{\ln(2)-\ln(\alpha)}{2\varepsilon^2} \right\rceil
$$

上式中的符号逐项解释如下：

1. `N` 是为某个概率性质采样的仿真条数。
2. `\alpha` 是置信度误差参数。
3. `\varepsilon` 是估计精度。
4. 这个公式说明统计验证的样本数主要由置信区间决定，而不是模型状态空间大小决定。

### 一个最小例子与通俗解释

最小例子可以理解成“一个 orchestrator 协调两个服务完成一次 request/offer 匹配”：

1. orchestrator 先发送 `ORCCHECK`，确认 service 与全局 configuration 一致。
2. 若当前 orchestration 要执行一次 match，orchestrator 会给 requester 和 offerer 分配角色。
3. 在 `centralised` 配置里，payload 经由 orchestrator 转发；在 `distributed` 配置里，orchestrator 只分发地址与端口，两个 service 自行直连交换消息。
4. 若某个 service 收到不符合其 contract 的动作，运行时会抛出 `ContractViolationException`。

通俗地说，这篇论文做的事情，相当于把“契约自动机上允许的下一步动作”翻译成“socket 层消息什么时候发、谁先等、谁先回、buffer 会不会堵死”的可验证状态机网络。

### 运行 / 接受 / 转移语义

运行时全局状态可保守整理为：

$$
s = (\vec{\ell}, \nu, b, \delta)
$$

上式中的符号逐项解释如下：

1. `\vec{\ell}` 是 orchestrator、services 与 timeout automata 当前所在的位置向量。
2. `\nu` 是 stochastic timed automata 中的时钟与延迟相关状态。
3. `b` 是当前全部 communication buffers 的内容。
4. `\delta` 是当前 action/choice 配置。

论文用于证明“不会因协议错误而永久卡死”的代表性性质，可保守压缩为：

$$
A[](\neg deadlock \lor Timeout \lor Terminated)
$$

上式中的符号逐项解释如下：

1. `deadlock` 是 `Uppaal` 的特殊谓词。
2. `Timeout` 表示某个 socket timeout automaton 已进入超时位置。
3. `Terminated` 表示 orchestrator 与所有 services 已一致结束。
4. 该式表达的是：任意执行中，系统不会落入无法解释的死锁，要么发生显式超时，要么完成正常终止。

### 语义边界

这篇论文的边界非常明确：

1. 它验证的是 `CARE` runtime 自身，而不是任意上层 service composition 的业务正确性。
2. 真实 payload 被抽象成有限消息常量，如 `ACTION/REQUEST/OFFER/ACK`。
3. 时间语义主要用于读写延迟和 timeout，不是对业务合同本身做实时时序建模。
4. choice/action 的配置空间有限，目标是运行时协议正确性而不是复杂最优调度。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 运行时网络骨架 | `$\mathcal{N}_{CARE} = (\mathcal{O}, \{\mathcal{S}_i\}, \{\mathcal{T}_i\}, B, \delta, \lambda)$` | 把 orchestrator、services、timeout 与 buffers 统一到同一个 `Uppaal` 网络里。 |
| 统计采样规模 | `$N = \lceil (\ln(2)-\ln(\alpha))/(2\varepsilon^2) \rceil$` | 说明 statistical model checking 的仿真条数由精度与置信度控制。 |
| 全局运行状态 | `$s = (\vec{\ell}, \nu, b, \delta)$` | 同时跟踪控制位置、时间状态、buffer 内容与配置。 |
| 死锁安全 | `$A[](\neg deadlock \lor Timeout \lor Terminated)$` | 任意执行中不会出现无解释的协议性卡死。 |
| 运行时一致性 | `configuration(service_i) = configuration(orchestrator)` | orchestration 开始前必须通过 compatibility check。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | orchestrator、service、timeout 都是显式 automata。 |
| 事件 / 触发 | 强支持 | `ORCCHECK`、`ORCCHOICE`、`ACTION`、`REQUEST`、`OFFER`、`ACK` 等消息是一等对象。 |
| 守卫 / 数据 | 部分支持 | 重点在 buffer 可用性、configuration 与消息类型，不在复杂业务数据。 |
| 层次 | 部分支持 | 有 runtime/object 层次，但核心仍是平面 automata network。 |
| 并发 / 同步 | 强支持 | 多 services 并发、buffer 同步和 centralised/distributed 协作是主体。 |
| 时间约束 | 强支持 | 写/读延迟与 socket timeout 被显式建模为 stochastic timed behavior。 |
| 连续动态 / 随机性 | 支持随机、无连续 | 使用指数分布延迟；没有连续动力学。 |
| 可执行 / 可验证性 | 强执行、强验证 | 既有真实中间件实现，也有 `Uppaal` exhaustive/SMC 与 model-based testing。 |

### 形式化问题与性质

1. 论文最关键的补充是“contract automata 运行时到底如何通信、阻塞和恢复”。
2. `centralised` 与 `distributed` 两种 action 模式在同一验证框架里得到统一比较。
3. `orphan message`、buffer overflow、configuration mismatch 这类纯实现级问题被正式纳入模型。
4. 对接口/组合主干来说，它比已有 `CARE` 运行时论文更强调“怎么用 timed/stochastic model 把 runtime proof 补完整”。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 从 `RunnableOrchestration` 与 `RunnableOrchestratedContract` 抽出控制逻辑。
2. 把 Java TCP/IP sockets 抽成异步 FIFO buffers。
3. 用 exponential-delay transitions 模拟 send/read 的随机耗时。
4. 把 choice 与 action configuration 作为全局离散参数放进 `Uppaal` 模型。

### 机器可处理承载方式

原文使用的机器可处理承载方式包括：

1. `Uppaal` template automata。
2. global declarations 中的 buffer arrays、configuration 变量与 timeout threshold。
3. 由 traceability comments 标注到源码位置的模型转移。
4. 基于模型自动生成的测试产物与日志。

### 交换与互操作

互操作重点不在开放交换标准，而在 runtime 适配：

1. orchestrator 与 services 通过统一消息常量交互。
2. service action 与 Java method 绑定。
3. `centralised/distributed` 配置允许同一 contract 应用切换两种执行路线。

## 配套基础设施

- 建模/编辑工具：`Uppaal`。
- 解析/交换/元模型支持：原文提供 traceability-enhanced model 和 buffer-based runtime abstraction，未定义通用元模型。
- 仿真/执行支持：`CARE` Java middleware 可直接执行 contract-based applications。
- 验证/分析支持：`Uppaal` exhaustive model checking、statistical model checking 与 model-based testing。
- 代码生成/转换支持：原文不做代码生成，但给出模型到测试的半自动链路。
- 标准化或社区生态：依托 `Contract Automata` 与 `Uppaal` 两条成熟研究线，开放标准化仍偏弱。

## 适用场景与需求前提

### 适用场景

适合 contract-based service orchestration、需要显式协调者的分布式中间件，以及想把接口契约真正落到运行时验证闭环的系统。

### 需求前提

1. 服务接口可以先写成有限的 request/offer 契约动作。
2. orchestration 由有限状态结构驱动，而不是完全动态发现。
3. 运行时允许引入 orchestrator、wrapper 或 port/address 协商机制。
4. 系统核心风险集中在 buffer、timeout、message ordering 与 role assignment。

### 不适用或高成本场景

如果系统核心在海量动态发现、开放世界参与方或复杂 payload 数据语义，这种 finite-state runtime abstraction 的成本会迅速升高。

## 与相邻形式主义的关系

相对 [Contract Automata](../contract-automata/desc.md)，本文不再扩展匹配语义，而是补 runtime protocol correctness；相对 [A Runtime Environment for Contract Automata](../a-runtime-environment-for-contract-automata/desc.md)，本文把 `CARE` 从“可执行运行时”进一步推进到“可验证的 stochastic timed runtime”；相对 [The Theory of Timed I/O Automata](../the-theory-of-timed-input-output-automata/desc.md)，它不追求接口精化的一般理论，而是围绕一个具体中间件实现做可执行验证。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提供了非常直接的证据：接口/契约模型不仅能做静态组合分析，也能继续走到“运行时行为是否遵守模型”的闭环。

### 作为目标形式主义还是中间表示

对 service orchestration 这类场景，它更像“接口/契约目标模型 + 运行时验证中间表示”的组合体。

### 对需求到模型生成的启发

1. 如果未来要做生成-验证-修复闭环，不能只生成静态 contract automata，还要显式抽取 runtime configuration、timeout 和 message protocol。
2. buffer、ack、role assignment 这类实现细节值得在模型层保留，因为它们经常决定系统是否真的可用。
3. 异常如 `ContractViolationException`、timeout 与 orphan messages 都可以作为后续自动修复的反馈信号。

### 现实限制

它主要验证 `CARE` 这一条具体 runtime 线，离“任意接口契约系统都能统一落地验证”还差一层通用化工作。

## 重要的相关工作

- [Contract Automata](../contract-automata/desc.md)：给出静态契约组合与 agreement 主体。
- [A Runtime Environment for Contract Automata](../a-runtime-environment-for-contract-automata/desc.md)：给出 `CARE` 的执行语义与 Java runtime 骨架。
- [Controller Synthesis of Service Contracts with Variability](../controller-synthesis-of-service-contracts-with-variability/desc.md)：展示 `Contract Automata` 在可变性与控制综合方向的延展。

## 文献分类总结

- 这是一篇 `🔌` 类高价值应用条目，核心贡献是把 `Contract Automata / CARE` 的运行时协议压成可验证的 stochastic timed automata network。
- 其描述客体是服务接口与交互契约，因此记为 `🤝`；论文语境面向服务编排与分布式 middleware，因此记为 `🌐`。
- 对 `project_1` 来说，它补出了“接口/契约模型如何继续进入运行时验证”这一条非常关键的落地证据链。
