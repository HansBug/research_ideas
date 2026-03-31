问题一句话：本文验证的是开源中间件 `CARE` 的低层运行时交互逻辑，核心问题是在 Java `TCP/IP` socket 通信、缓冲与超时机制存在时，服务与 orchestrator 的实现是否仍满足 contract automata 语义承诺。
方法一句话：作者将 `CARE` 抽象为 stochastic timed automata 网络，用 `Uppaal` 同时做穷举验证、统计模型检查和 model-based testing，并把抽象测试自动具体化成 `JUnit` 用例直接回测真实实现。
验证收获一句话：论文验证了 deadlock freedom、无 orphan messages、配置兼容性等关键性质，还借由模型检查发现并修复了非阻塞 socket 假设导致的死锁问题，形成了“模型-验证-测试-源码”直连闭环。

## 基本信息

- 标题：Formal Analysis of the Contract Automata Runtime Environment with Uppaal: Modelling, Verification and Testing
- 中文标题：使用 `Uppaal` 对合同自动机运行时环境进行形式化分析：建模、验证与测试
- 作者：Davide Basile
- 单位：ISTI-CNR, Formal Methods and Tools Lab
- 发表：Logical Methods in Computer Science，2026
- DOI：`10.46298/lmcs-22(1:8)2026`
- 链接：[DOI](https://doi.org/10.46298/lmcs-22(1:8)2026)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：`Contract Automata Runtime Environment (CARE)` 分布式中间件及其 orchestrator / services 通信运行时
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文明确给出 `CARE` 开源发布、补充材料 `Zenodo` 和测试/模型链接。
- 案例/数据获取方式：案例来自 `CARE` 中间件源码、合同自动机规约和由 `Uppaal` 生成的抽象测试；无独立数据集但工件公开。

## 简报

这篇论文的价值在于它不只“证明一个模型正确”，而是把一个真实开源中间件从抽象模型一路连到源码测试。对象是 `CARE`，即一个根据 contract automata 协调服务执行的分布式运行时。论文验证的不是合同自动机理论本身，而是 orchestrator 与多个 services 通过 `TCP/IP` socket 实现这些合同语义时，会不会因为缓冲、阻塞、消息乱序、配置不一致等低层问题破坏运行时正确性。

- 系统：基于 contract automata 的分布式中间件 `CARE`。
- 特点：open-source、分布式、消息缓冲、超时、支持不同 orchestration 配置。
- 规模：论文模型覆盖 orchestrator、多个 services、socket timeout automata 和不同 buffer 参数设置；源码约 `770` 行与模型逐步对照。
- 模型：`Uppaal` stochastic timed automata 网络，带多版本模型和测试装饰代码。
- 性质：termination、absence of deadlocks、absence of orphan messages、no interference、compatibility check。
- 方法：穷举验证 + 统计模型检查 + `Yggdrasil` 抽象测试生成 + `JUnit` 具体测试。
- 结果：验证了多项关键性质，并发现了旧版非阻塞 socket 假设下的真实死锁问题。

`CARE 源码/合同规约 -> Uppaal 抽象模型 -> exhaustive + statistical checking -> 生成抽象测试 -> concretise 成 JUnit -> 反向验证抽象层合理性`

## 论文定位

这是一篇典型的软件服务运行时验证论文，验证对象明确是 middleware 行为与服务编排运行时，因此归入 `🧩 + 🌐`。它尤其值得注意，因为它把 `UPPAAL` 从“只做模型验证”推进到了“模型驱动测试 + 源码 traceability”的闭环。

## 验证对象与问题背景

### 系统与场景

`CARE` 是一个分布式 middleware，用来执行 contract automata 规约的服务组合。每一步 orchestration 都会被落实为 orchestrator 与 services 之间一系列低层 socket 交互。

### 系统组成与运行机制

论文中的关键对象包括：

1. `RunnableOrchestration`；
2. `RunnableOrchestratedContract` 服务实例；
3. `SocketTimeout` automata；
4. contract automata library (`CATLib`) 支撑的上层规约语义；
5. Java `TCP/IP` socket 通信与缓冲。

### 验证边界

作者明确说明：论文聚焦的是 `CARE` 运行时层面的低层交互实现，而不是证明合同自动机理论本身，也不是验证具体应用领域业务逻辑。

### 核心问题

论文关心的主要问题是：

1. 中间件是否会 deadlock；
2. 终止时是否仍残留未消费消息；
3. 无关服务会不会错误干涉某次 distributed match；
4. 若 orchestrator 与 service 配置不兼容，系统能否阻止 orchestration 启动；
5. 抽象模型是否足够接近真实源码实现。

## 模型与形式化建模

### 抽象对象

模型把 `CARE` 抽成：

1. orchestrator 模板；
2. service 模板；
3. timeout 模板；
4. buffer / socket 相关共享结构。

### 抽象边界

论文显式抽象掉：

1. 具体 payload 细节；
2. 上层业务 application 逻辑；
3. 合同内容的具体语义细节；
4. 某些与验证目标无关的 Java 实现细节。

保留的则是：

1. 缓冲区容量；
2. 发送/接收次序；
3. blocking / non-blocking 语义；
4. timeout；
5. 配置兼容性；
6. orchestrator 与 service 的状态推进。

### traceability 与测试装饰

一个很特别的点是：模型中每个关键 transition 都可追踪回源码，且模型里插入了 test code，用于从 `Uppaal` 生成 abstract tests，再 concretise 成 `JUnit`。

## 验证目标与性质

### 待验证问题

论文系统验证了五类性质：

1. 终止性；
2. 无死锁；
3. 无 orphan messages；
4. distributed match 时无额外服务干涉；
5. 配置不兼容时 orchestration 不会启动。

### 性质类型

它们覆盖：

1. 活性；
2. 安全；
3. 终止后一致性；
4. reachability；
5. testing-oriented reachability。

### 查询表达

文中的代表性查询包括：

1. 终止相关：
   `ror.Stop --> ((ror.Terminated && (forall(i:id_t) ROC(i).Terminated)) || (exists(i:id_t) SocketTimeout(i).Timeout))`
2. 无死锁：
   `A[](not deadlock || (exists(i:id_t) SocketTimeout(i).Timeout) || (ror.Terminated && (forall(i:id_t) ROC(i).Terminated)))`
3. 无 orphan messages：
   `A[]((ror.Terminated && (forall(i:id_t) ROC(i).Terminated)) imply allEmpty())`
4. 配置不兼容不启动：
   `A<>((ror.Error && carl.Error) || ror.Timeout)`
   `A[](!ror.Start)`
5. 测试生成使用 reachability 查询：
   `E<>(alice.steps[0] == ORC_CHECK && ...)`

## 核心方法与验证流程

1. 先根据 `CARE` 源码和运行时结构建立抽象 `Uppaal` 模型。
2. 用穷举和统计模型检查验证 termination、deadlock、message consumption 等性质。
3. 通过 counterexample 分析模型与实现中的设计问题。
4. 为模型添加 testing hooks 和 traceability 信息。
5. 由 `Yggdrasil` 生成抽象测试，再补全参数，转成 `JUnit` 测试真实源码。
6. 用测试结果反向校验抽象层级是否合理。

## 案例与结果

### deadlock 与建模缺陷定位

论文最有代表性的发现之一是：

1. 旧版模型错误地把 socket 发送端假设为 non-blocking；
2. 在 majoritarian/dictatorial choice 下，orchestrator 可不断向某个永不消费消息的服务压入 `ORCCHOICE/SKIP`；
3. 这会把对方缓冲区填满并导致死锁；
4. `Uppaal` 的 counterexample trace 揭示了这一数百步长问题；
5. 修复方式是把 socket 语义改为默认 blocking mode。

### 关键性质验证

论文报告：

1. 终止相关性质在两组参数设置 `c1/c2` 下都成立；
2. 无死锁性质同样成立，但第二组参数设置需要更高内存和更多状态；
3. 终止时所有 buffers 为空；
4. distributed match 不会被无关服务干涉；
5. 配置不兼容时 orchestrator 的 `Start` 永远不会被到达。

### 模型驱动测试

论文没有停在模型层，而是：

1. 使用 `Uppaal` 生成 abstract test cases；
2. 将其具体化为 `JUnit`；
3. 直接对 `CARE` 源码执行；
4. 由此建立模型和实现的一一映射关系。

这使得“抽象过头”不再只是口头风险，而能通过 concrete tests 进行检验。

## 与本研究的关系

### 相关性分析

它和博士研究高度相关，因为它展示了从 formal model 到 implementation testing 的完整闭环，而且对象本身就是典型的状态机式运行时系统。

### 可借鉴之处

1. 通过 traceability 把模型 transition 和源码行关联起来。
2. 利用 model-based testing 反向验证抽象层级是否合适。
3. 把统计验证、穷举验证与测试统一放在同一工作流里。

### 存在的不足与改进空间

1. 抽象层仍然忽略了应用层 payload 和部分 Java 细节。
2. 更大参数规模需要更强计算资源或更多依赖统计检查。
3. 每次 `CARE` 版本升级后，模型、traceability 和测试都需要同步维护。

### 对本研究的启发

它说明“形式化模型是否足够接近实现”并不是无法回答的问题，只要建立 traceability 和 model-based testing，就可以把这一问题变成工程上可验证的闭环。

## 重要的相关工作

### 1. `UPPAAL` 的 model-based testing 线

- 本文系统使用了 `Yggdrasil` 风格的离线测试生成，且对象是公开源码，这一点在 `UPPAAL` 应用文献中非常少见。

### 2. contract automata 到运行时落地

- 它把 contract automata 这种高层行为规约真正连到了中间件实现层，是“规约 -> 运行时 -> 验证 -> 测试”链条的典型案例。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：`CARE` 开源发布、论文补充材料和模型/测试工件均公开可访问。
- 获取方式/链接：[DOI](https://doi.org/10.46298/lmcs-22(1:8)2026)；[CARE Release](https://github.com/contractautomataproject/CARE/releases/tag/v1.0.1)；[补充材料](https://doi.org/10.5281/zenodo.14671729)
- 对后续复用的现实影响：这是非常高公开度的软件运行时案例，既可复用 `Uppaal` 模型，也可直接观察 abstract test 到 `JUnit` 的具体化过程。
