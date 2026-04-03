# 使用 UPPAAL-TRON 测试实时嵌入式软件：一个工业案例研究 / Testing Real-Time Embedded Software Using UPPAAL-TRON: An Industrial Case Study

## 基本信息

- 标题：Testing Real-Time Embedded Software Using UPPAAL-TRON: An Industrial Case Study
- 中文标题：使用 UPPAAL-TRON 测试实时嵌入式软件：一个工业案例研究
- 作者：Kim G. Larsen，Marius Mikucionis，Brian Nielsen，Arne Skou
- 发表：*Proceedings of the 5th ACM International Conference on Embedded Software (EMSOFT 2005)*，pp. 299-306，2005
- DOI：`10.1145/1086228.1086283`
- 链接：https://doi.org/10.1145/1086228.1086283
- 形式主义：`Timed Automata / UPPAAL-TRON Online Testing Model`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：在线黑盒一致性测试 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL-TRON`、`UPPAAL` 引擎和 Danfoss `EKC` 控制器适配器；论文称 `TRON` 可在线获取用于评估/研究，但未给出现代公开仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、adapter API、timed trace、`rtioco/irtioco` 一致性关系；无独立交换标准。

## 简报

这篇论文很典型地展示了 `Timed Automata` 不只是拿来做离线模型检查，还可以直接拿来驱动在线测试。作者把测试规格拆成 environment model 和 IUT model 两部分，`UPPAAL-TRON` 在运行时维护“当前可能状态集合”，一边给实现送输入，一边检查输出和延时是否仍满足模型。其 Danfoss `EKC 201/301` 工业恒温控制器案例说明：只要输入输出能离散成 actions，timed automata 就能直接接进 HIL/SIL 测试回路。

- 形式主义定位：这是经典 `Timed Automata` 主干上的在线测试应用条目，重点是“environment assumptions + relativized conformance + online symbolic execution”。
- 构造方式简述：把测试规范写成 environment automata 与 IUT automata 的网络，再让 `TRON` 维护符号状态集 `Z`，随机执行输入、等待输出或延时，并实时判定是否 conformance。
- 基础设施与场景简述：依托 `UPPAAL`、`UPPAAL-TRON`、adapter API 和工业控制器测试台，服务实时嵌入式设备的模型驱动在线测试。

```text
environment assumptions + IUT timed automata -> symbolic state set -> online stimulation / monitoring -> pass / fail verdict
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 由 environment 和 IUT 组成的 timed automata network。
2. relativized timed input/output conformance。
3. `after` 和 `out` 运算定义的在线监控语义。
4. 运行时维护的 reachable symbolic state set `Z`。
5. 连接抽象动作和真实设备的 adapter。

### 核心抽象

原文明确指出测试规格是一个 network of timed automata，可保守整理为：

$$
\mathcal{N}_{test} = A_{env} \parallel A_{iut}
$$

上式中的符号逐项解释如下：

1. `A_{env}` 是环境模型，负责生成相关输入和限制允许的 delay。
2. `A_{iut}` 是系统规格模型，用来定义允许的输出和时序容忍度。
3. `\parallel` 表示两部分联合构成完整测试规格。

论文最关键的正式定义是 relativized timed input/output conformance：

$$
irtioco\ e s = \forall \sigma \in TTr(s,e).\ \mathrm{out}((i,e)\ \mathrm{after}\ \sigma) \subseteq \mathrm{out}((s,e)\ \mathrm{after}\ \sigma)
$$

上式中的符号逐项解释如下：

1. `s` 是系统规格。
2. `e` 是环境规格。
3. `i` 是待测实现。
4. `\sigma` 是一条 timed input/output trace。
5. `TTr(s,e)` 是规格与环境组合下可发生的所有 timed traces。
6. `\mathrm{after}` 表示执行 trace 后系统可能处于的状态集合。
7. `\mathrm{out}` 表示从该状态集合还能合法产生的输出与 delay 集合。

### 一个最小例子与通俗解释

论文里先用一个简单 cooling controller 解释 environment assumptions 的作用，再把方法落到 Danfoss `EKC` 控制器：

1. 环境 automaton 描述温度变化、用户操作和 defrost 触发。
2. IUT automaton 描述压缩机、报警和 defrost 的允许行为。
3. `TRON` 运行时可能选择发一个输入，也可能让时间流逝并等待输出。
4. 如果观察到的输出或等待时间超出了模型许可，测试立即判为 fail。

通俗地说，这相当于“让状态机一边扮演环境，一边扮演裁判”，测试脚本不再是手写的固定序列，而是运行时从模型里现取。

### 运行 / 接受 / 转移语义

论文给出的核心在线算法维护：

$$
Z \subseteq S \times E
$$

其中 `S` 是系统规格状态空间，`E` 是环境状态空间，`Z` 是在当前 timed trace 之后可能到达的符号状态集合。

在线执行可保守整理为：

$$
Z \xrightarrow{i?} Z\ \mathrm{after}\ i \qquad Z \xrightarrow{d} Z\ \mathrm{after}\ d \qquad Z \xrightarrow{o!} Z\ \mathrm{after}\ o
$$

上式中的符号逐项解释如下：

1. `i?` 表示 tester 向 IUT 发送输入。
2. `d` 表示等待一段合法 delay。
3. `o!` 表示 tester 观察到 IUT 输出。
4. 每一步都通过 `after` 运算更新符号状态集合 `Z`。

论文还明确区分：

1. `EnvOutput(Z)`：当前环境允许 tester 主动发出的输入集合。
2. `ImpOutput(Z)`：当前 IUT 合法输出集合。
3. `Delays(Z)`：在不违反 invariants 的前提下，当前允许等待的 delay 集合。

### 语义边界

这篇论文的边界主要有：

1. 只处理离散或已离散化的输入输出 actions。
2. 测试价值高度依赖环境模型质量。
3. 主要关注 mode switches、deadline 和允许的时序窗口，不处理连续微分方程主导的行为。
4. 实际精度还会受 adapter latency 和观测接口限制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 测试规格网络 | `$\mathcal{N}_{test} = A_{env} \parallel A_{iut}$` | 把环境与系统规格一起写成 timed automata network。 |
| 一致性关系 | `$irtioco\ e s = \forall \sigma \in TTr(s,e).\ \mathrm{out}((i,e)\ \mathrm{after}\ \sigma) \subseteq \mathrm{out}((s,e)\ \mathrm{after}\ \sigma)$` | 定义实现相对环境的 timed conformance。 |
| 运行时状态集 | `$Z \subseteq S \times E$` | 在线测试维护的符号状态集合。 |
| 在线更新 | `$Z \xrightarrow{i?/d/o!} Z\ \mathrm{after}\ (\cdot)$` | 每个输入、输出或 delay 都用 `after` 更新状态集。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | environment 与 IUT 都由显式 automata 位置表示。 |
| 事件 / 触发 | 很强 | 输入、输出和 delay 都是一等测试对象。 |
| 守卫 / 数据 | 中等支持 | 依赖 clocks、整数和 channel；不追求复杂数据语义。 |
| 层次 | 不支持 | 主体是平铺 automata network。 |
| 并发 / 同步 | 强支持 | `UPPAAL` 网络、共享变量和同步动作是工具基础。 |
| 时间约束 | 很强 | deadline、容忍窗口和延时一致性是主轴。 |
| 连续动态 / 随机性 | 不支持 | 连续过程需要先离散化后才能接入。 |
| 可执行 / 可验证性 | 很强 | 模型可直接驱动在线测试与 fail verdict。 |

### 形式化问题与性质

1. 论文把 timed automata 从“离线验模工具”推进到了“在线测试执行器”。
2. environment assumptions 不是附属物，而是 conformance 关系的组成部分。
3. 对本文库最关键的价值，是它补强了 `Timed Automata` 在工业测试链路中的代表应用簇。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 为环境和 IUT 分别建立 timed automata。
2. 显式建模 adapter 和观测误差容忍区间。
3. 在 `UPPAAL` 中组合并检查基本一致性。
4. 由 `TRON` 在线维护 `Z` 并实时生成刺激 / 监控输出。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata network。
2. `after` / `out` 运算支持的符号状态集。
3. test log 中的 timed trace。
4. adapter API 与物理接口。

### 交换与互操作

论文的互操作重点在：

1. `UPPAAL` 模型到 `TRON` 引擎的直接复用；
2. adapter 把抽象动作映射到真实 IUT 接口；
3. 测试日志再回流到 `UPPAAL` 做离线诊断。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：`TRON` 直接消费 `UPPAAL` 模型；无独立交换标准。
- 仿真/执行支持：`UPPAAL-TRON` 在线执行测试，支持 timed trace 记录。
- 验证/分析支持：符号 reachability、`after` 运算、coverage features 与 fail diagnosis。
- 代码生成/转换支持：不是代码生成，而是 model-to-test-execution。
- 标准化或社区生态：依托 `UPPAAL` 工具线和实时嵌入式测试生态。

## 适用场景与需求前提

### 适用场景

适合工业控制器、实时嵌入式设备和 HIL/SIL 测试，只要系统交互能抽象为离散 actions 且关键 correctness 体现在时间约束与模式切换上。

### 需求前提

1. 输入输出需可离散化成 actions。
2. 环境假设必须能显式建模。
3. IUT 需提供足够好的 adapter 接口。
4. 关注点是 conformance / deadline / timing tolerance，而非复杂连续动力学。

### 不适用或高成本场景

如果系统主要行为来自高维连续控制回路，或环境模型根本无法稳定抽象，直接用这里的在线 timed-automata testing 会非常吃力。

## 与相邻形式主义的关系

相对 [testing-automotive-reactive-systems-using-timed-automata/desc.md](../testing-automotive-reactive-systems-using-timed-automata/desc.md)，本文更强调正式的一致性关系和在线算法；相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，它把 timed automata 从 verification 推进到 testing；相对 [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)，这里不做 plan repair，而是实时判定实现是否仍落在规格允许集合内。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果 Project 1 最终想形成“生成-验证-修复”闭环，生成的状态机不该只适合 model checking，也应尽可能兼容 testing。

### 作为目标形式主义还是中间表示

对在线测试工作流，它可以直接作为目标形式主义；对需求到模型自动化，它也是非常有价值的验证/测试共用中间表示。

### 对需求到模型生成的启发

1. 环境模型必须和系统模型一起生成，而不是事后补。
2. 若未来要接 testing，模型里应保留输入输出动作和 timing tolerance。
3. adapter 限制本身也是需求约束的一部分，不应完全留给实现阶段兜底。

### 现实限制

在线测试的真正瓶颈通常不是 timed automata 语义，而是 IUT 可观测性和 adapter 时延；如果这部分不稳，模型再好也难落地。

## 重要的相关工作

- [testing-automotive-reactive-systems-using-timed-automata/desc.md](../testing-automotive-reactive-systems-using-timed-automata/desc.md)：另一篇把 timed automata 接入 HIL testing 的代表应用。
- [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：同样围绕真实运行系统，但目标是验证而不是在线测试。
- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：同属实时嵌入式领域的 `TA` 应用条目，但对象是总线协议而非测试执行链。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：`Timed Automata / UPPAAL-TRON Online Testing Model`
- 论文角色：在线黑盒一致性测试 / 定时自动机应用建模
- 核心功能：基于 environment assumptions 做实时 conformance testing
- 关键特性：`rtioco/irtioco`、`after/out`、在线符号状态集、adapter、timed traces
- 构造方式：environment `TA` + IUT `TA` + `TRON` 在线算法
- 基础设施：`UPPAAL` + `UPPAAL-TRON` + adapter API
- 适用场景：工业控制器和实时嵌入式系统在线测试
- 需求前提：输入输出需可离散化，环境假设需显式建模
- 状态：🟢
