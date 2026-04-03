# 使用 UPPAAL 验证 LEGO Mindstorms 实时控制程序 / Model-Checking Real-Time Control Programs: Verifying LEGO Mindstorms Systems Using UPPAAL

## 基本信息

- 标题：Model-Checking Real-Time Control Programs. Verifying LEGO Mindstorms Systems Using UPPAAL
- 中文标题：使用 UPPAAL 验证 LEGO Mindstorms 实时控制程序
- 作者：Torsten K. Iversen，Kåre J. Kristoffersen，Kim G. Larsen，Morten Laursen，Rune G. Madsen，Steffen K. Mortensen，Paul Pettersson，Chris B. Thomasen
- 发表：*BRICS Report Series*，Vol. 6, No. 53，1999
- DOI：`10.7146/BRICS.V6I53.20123`
- 链接：https://doi.org/10.7146/BRICS.V6I53.20123
- 形式主义：`Timed Automata / RCX Control-Program Verification Model`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：控制程序验证 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `NQC` compiler、内部 `rcx2uppaal` 翻译器和 `UPPAAL`；论文未提供现代公开仓库。
- 标准/格式获取方式：承载方式是 `NQC -> RCX bytecode -> UPPAAL` 的 timed automata 网络、scheduler model 与 environment automata；无统一交换标准。

## 简报

这篇论文非常早就把“真实控制程序 -> timed automata -> model checking”这条链路跑通了。作者处理的是 LEGO `RCX` brick 上运行的并发实时控制程序：先把 `NQC` 程序编译成 `RCX` bytecode，再由 `rcx2uppaal` 自动翻译成 task automata；`RCX` 的 round-robin scheduler 也被单独建模；最后用户再提供 environment timed automata，就能对完整控制闭环做验证。LEGO 砖块分拣机案例表明，工具不只是能证明系统在合理环境下工作，还能指出环境假设不满足时会出现什么错误。

- 形式主义定位：这是经典 `Timed Automata` 主干上的控制程序验证条目，重点是“program translation + scheduler model + environment model”。
- 构造方式简述：`NQC` 程序先编译为 `RCX` bytecode，再把每条指令翻成 timed automata 片段，同时把 round-robin scheduler 和传感器/执行器接口也建模，最终在 `UPPAAL` 中联合验证。
- 基础设施与场景简述：依托 `NQC` compiler、`rcx2uppaal`、`UPPAAL` 和 environment automata，服务小型嵌入式控制程序的 scheduler-aware verification。

```text
NQC control program -> RCX bytecode -> task automata + scheduler automaton + environment automata -> UPPAAL verification
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 由多个任务组成的 `RCX` 控制程序。
2. round-robin scheduler automaton。
3. 由 `RCX_active`、`RCX_currentTask`、`RCX_timer` 等变量刻画的任务调度状态。
4. 传感器和执行器接口变量。
5. 用户提供的 environment timed automata。

### 核心抽象

结合原文第 3 节的翻译流程，可保守整理出系统模型：

$$
\mathcal{M}_{rcx} = A_{sched} \parallel A_{task,0} \parallel \cdots \parallel A_{task,n} \parallel E_1 \parallel \cdots \parallel E_m
$$

上式中的符号逐项解释如下：

1. `A_{sched}` 是 `RCX` 调度器 automaton。
2. `A_{task,k}` 是第 `k` 个任务翻译得到的 timed automaton。
3. `E_j` 是第 `j` 个 environment automaton。
4. `\parallel` 表示所有 automata 在 `UPPAAL` 中并行同步。

论文还给出了 scheduler 的关键状态变量：

$$
State_{sched} = (RCX\_active, RCX\_currentTask, RCX\_timer)
$$

上式中的符号逐项解释如下：

1. `RCX_active` 是 bit array，记录哪些任务处于 active 状态。
2. `RCX_currentTask` 表示当前执行或下一个将执行的任务编号。
3. `RCX_timer` 是 scheduler 的全局时钟，用来度量调度开销和指令执行时间。

### 一个最小例子与通俗解释

论文在前几页先给了一个最小程序：不断 `PlaySound` 再 `Delay(100)`。

1. `PlaySound` 会被翻译成一段带执行时长的 automaton 片段。
2. `Delay(100)` 会先把当前任务标记为 inactive，再等待 `100` 时间单位后重新激活。
3. scheduler 以 round-robin 顺序轮询活跃任务。
4. environment automata 负责提供传感器变化和外部物理对象。

通俗地说，这篇论文把“嵌入式任务程序”当成了“由很多小状态机片段拼成的大状态机”，而且连调度器本身也不再是黑盒。

### 运行 / 接受 / 转移语义

论文直接使用 `UPPAAL` 查询语言。对黑色 LEGO 砖块，关键性质之一是：

$$
E\Diamond (BlackBrick.Kicked\_off)
$$

$$
A[]\ \neg(BlackBrick.Passed)
$$

上式中的符号逐项解释如下：

1. `E\Diamond` 表示存在一条执行路径最终达到给定状态。
2. `BlackBrick.Kicked_off` 表示黑砖最终被踢出传送带。
3. `A[]` 表示所有路径上的全局不变式。
4. `BlackBrick.Passed` 表示黑砖错误地直接通过末端而没有被踢走。
5. 两个查询联合表达了黑砖必须被正确分拣。

对红色 LEGO 砖块，性质则是：

$$
E\Diamond (RedBrick.Passed)
$$

$$
A[]\ \neg(RedBrick.Kicked\_off)
$$

这说明红砖应当顺利通过，而不是被误踢。

### 语义边界

这篇论文的边界主要有：

1. 模型依赖用户显式给出 environment timed automata。
2. 硬件级电机、传感器和物理过程都被离散化成有限时序对象。
3. 适合小型控制程序，不适合复杂操作系统级运行时。
4. 调度模型是明确写死的 round-robin，而不是任意可配置 RTOS。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统模型 | `$\mathcal{M}_{rcx} = A_{sched} \parallel A_{task,0} \parallel \cdots \parallel E_1 \parallel \cdots \parallel E_m$` | 任务、调度器和环境联合建模。 |
| 调度状态 | `$State_{sched} = (RCX\_active, RCX\_currentTask, RCX\_timer)$` | round-robin scheduler 的核心离散/时间状态。 |
| 黑砖正确性 | `$E\Diamond (BlackBrick.Kicked\_off)$` | 黑砖最终可以被踢出。 |
| 黑砖不漏检 | `$A[]\ \neg(BlackBrick.Passed)$` | 黑砖不能直接通过末端。 |
| 红砖正确性 | `$E\Diamond (RedBrick.Passed)$` | 红砖应通过传送带。 |
| 红砖不误踢 | `$A[]\ \neg(RedBrick.Kicked\_off)$` | 红砖不能被误踢。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个任务、scheduler、brick 和 actuator 都有显式位置。 |
| 事件 / 触发 | 很强 | 任务调度、传感器变化、kick 动作都是核心事件。 |
| 守卫 / 数据 | 中等支持 | 使用 bounded integers、端口变量和 clocks。 |
| 层次 | 不支持 | 模型由多个平铺 automata 组成。 |
| 并发 / 同步 | 很强 | 多任务与 scheduler 并发执行是主体。 |
| 时间约束 | 很强 | 指令耗时、delay 指令、砖块到达和执行器动作都显式计时。 |
| 连续动态 / 随机性 | 不支持 | 物理行为被有限离散化。 |
| 可执行 / 可验证性 | 很强 | 可直接在 `UPPAAL` 中检查 reachability / invariance。 |

### 形式化问题与性质

1. 论文展示了“程序级自动翻译到 `TA`”的很早期完整链路。
2. 调度器单独建模这一点尤其关键，它让验证对象不只是业务逻辑，还包括 runtime overhead。
3. 对本文库而言，它补强了 `Timed Automata` 主干在“控制程序验证”上的早期代表应用。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 把 `NQC` 程序编译成 `RCX` bytecode。
2. 用 `rcx2uppaal` 把每条指令翻译成 timed automata 片段。
3. 构造 scheduler automaton。
4. 引入 environment automata 和 sensor/actuator 接口变量。
5. 在 `UPPAAL` 中验证目标性质。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `NQC` 程序。
2. `RCX` bytecode。
3. `UPPAAL` timed automata 网络。
4. scheduler / task / environment 三类 automata。

### 交换与互操作

论文的互操作重点在：

1. `NQC -> RCX bytecode -> UPPAAL` 的翻译链；
2. environment automata 与程序模型的传感器/执行器接口耦合；
3. query 结果再回流解释为真实 LEGO 砖块分拣行为。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：`NQC` compiler + `rcx2uppaal` 翻译器；无统一交换标准。
- 仿真/执行支持：通过 LEGO `RCX` brick 与实验装置验证模型假设。
- 验证/分析支持：`UPPAAL` reachability / invariance。
- 代码生成/转换支持：支持从控制程序自动转换为 timed automata，而非反向代码生成。
- 标准化或社区生态：属于 `UPPAAL` 早期嵌入式控制程序验证路线。

## 适用场景与需求前提

### 适用场景

适合小型实时控制程序、教育/原型机器人和可显式建模 scheduler 开销的嵌入式任务系统。

### 需求前提

1. 控制程序需能编译成有限 bytecode / instruction set。
2. 任务调度策略必须明确。
3. 传感器、执行器和环境交互可抽成有限 timed automata。

### 不适用或高成本场景

如果系统依赖复杂 RTOS、动态内存、不可控外设驱动栈或难以离散化的连续环境，这套翻译和验证会迅速失真。

## 与相邻形式主义的关系

相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)，本文是离线验证而不是在线测试；相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，这里验证对象是更底层的任务程序和 scheduler；相对 [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)，这篇做的是控制程序与环境联验，而不是高层计划落地。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常贴近 Project 1 的“需求到状态机自动建模”主线，因为它直接说明了程序结构、调度器和环境都可以统一压进 `Timed Automata`。

### 作为目标形式主义还是中间表示

对小型实时控制程序，它完全可以作为目标形式主义；对更大控制系统，它也是很强的验证中间表示。

### 对需求到模型生成的启发

1. 调度策略不能被当作外部背景，应该进模型。
2. 程序指令时序、传感器接口和环境假设要一起生成。
3. 如果将来要从代码反推模型，这篇论文给出了很早的程序到 automata 翻译样板。

### 现实限制

真正困难的地方不在 `UPPAAL` 本身，而在于把环境抽象到既能保真、又不致爆炸的粒度。

## 重要的相关工作

- [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：同样面向真实嵌入式控制器，但走向在线测试。
- [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：展示了 `TA` 在现代机器人软件栈中的另一种落地方式。
- [timed-automata-based-analysis-of-embedded-system-architectures/desc.md](../timed-automata-based-analysis-of-embedded-system-architectures/desc.md)：同样面向嵌入式系统，但对象是部署架构资源层而不是程序翻译层。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：`Timed Automata / RCX Control-Program Verification Model`
- 论文角色：控制程序验证 / 定时自动机应用建模
- 核心功能：把并发控制程序、scheduler 和环境联合翻译为可验证 `TA` 网络
- 关键特性：`NQC/RCX` 翻译、scheduler automaton、task automata、sensor/actuator interface
- 构造方式：`NQC -> RCX bytecode -> rcx2uppaal -> UPPAAL`
- 基础设施：`NQC` compiler + `rcx2uppaal` + `UPPAAL`
- 适用场景：小型实时控制程序和 scheduler-aware embedded verification
- 需求前提：任务集、调度开销和环境接口需可显式结构化
- 状态：🟢
