# 实时系统在线即时测试 / Online On-the-Fly Testing of Real-time Systems

## 基本信息

- 标题：Online On-the-Fly Testing of Real-time Systems
- 中文标题：实时系统在线即时测试
- 作者：Marius Mikucionis，Kim G. Larsen，Brian Nielsen
- 发表：*BRICS Report Series*，10(49)，2003
- DOI：`10.7146/brics.v10i49.21821`
- 链接：https://doi.org/10.7146/brics.v10i49.21821
- 形式主义：`timed automata / online on-the-fly testing / T-UPPAAL precursor`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：基于 `UPPAAL` 符号状态集的在线实时一致性测试先驱路线
- 工具/实现获取方式：原文明确说明算法已实现为 `UPPAAL` 的扩展，即后来的 `T-UPPAAL` 早期原型；正文未给稳定公开仓库。
- 标准/格式获取方式：输入是由 `IUT` 模型和环境模型组成的 closed network of timed automata，输出是 `pass/fail/inconclusive` verdict 与可选 execution trace；不是中立交换标准。

## 简报

这篇论文的重要性在于，它把“实时模型驱动测试”从离线生成测试用例，推进到边执行边推导的 on-the-fly 模式。核心思想是维护一个当前可达符号状态集 `$Z$`，每观察到一次输入、输出或时间流逝，就立即用 `UPPAAL` 风格的符号操作更新 `$Z$`，并据此决定下一步该发什么输入、等多久、以及当前实现是否已经违反规格。

- 形式主义定位：围绕 timed automata 的在线一致性测试方法路线，而不是新的 timed automata 本体。
- 构造方式简述：将测试规格建成 `IUT` 模型与环境模型的并行 timed automata 网络，测试器在运行中交替选择输入或延时，并通过 `After`/`Closure` 算法维护当前符号状态集。
- 基础设施与场景简述：依托 `UPPAAL` 语言、符号 clock-constraint 运算、adapter 和 timed trace inclusion，一边驱动真实实现，一边实时给出 verdict。

```text
IUT model + environment model -> timed-automata test specification -> symbolic state-set update -> online input/wait choice -> pass / fail / inconclusive
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata 与 timed-automata networks；
2. test specification；
3. timed trace inclusion conformance relation；
4. 当前可达符号状态集 `$Z$`；
5. `After`、`Closure_\tau`、`Closure^\delta_\tau` 算法。

### 核心抽象

论文直接使用标准 timed automaton 元组：

$$
A = (L,\ell_0,I,E)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 location 集合。
2. `$\ell_0$` 是初始 location。
3. `$I:L\to G(X)$` 为各 location 指定 invariant。
4. `$E\subseteq L\times G(X)\times Act\times U(X)\times L$` 是带 guard、动作和 update 的边集合。

测试规格被定义成一个 closed network of timed automata，可分成两部分：

$$
TS = IUT \parallel ENV
$$

上式中的符号逐项解释如下：

1. `$IUT$` 是实现模型。
2. `$ENV$` 是环境模型。
3. 测试器以 adapter 的身份代替环境与真实实现交互。

论文的核心运行时对象是当前可达状态集：

$$
Z \subseteq \{ \langle \bar{\ell},z\rangle \}
$$

上式中的符号逐项解释如下：

1. `$\bar{\ell}$` 是网络中各 automata 的 location 向量。
2. `$z$` 是 clock-constraint system，也就是一个 symbolic zone。
3. `$Z$` 表示“观察到当前 timed trace 后，规格可能处于哪些符号状态”。

在 action 级别，论文给出三类可选集合：

$$
EnvInput(Z)=\{a\in A_{out}\mid \langle \bar{\ell},z\rangle \in Z,\ \langle \bar{\ell},z\rangle \xrightarrow{a?}\}
$$

$$
EnvOutput(Z)=\{a\in A_{in}\mid \langle \bar{\ell},z\rangle \in Z,\ \langle \bar{\ell},z\rangle \xrightarrow{a!}\}
$$

$$
ImpOutput(Z)=\{a\in A_{out}\mid \langle \bar{\ell},z\rangle \in Z,\ \langle \bar{\ell},z\rangle \xrightarrow{a!}\}
$$

上式中的符号逐项解释如下：

1. `EnvInput(Z)` 是环境可以对实现施加的输入动作。
2. `EnvOutput(Z)` 是环境模型自身可产生的输出。
3. `ImpOutput(Z)` 是实现模型当前允许产生的输出。
4. 测试器正是靠这些集合判断“该发什么”“看到什么才算合法”。

### 一个最小例子与通俗解释

论文中的 coffee machine 很适合作为最小例子：

1. 环境模型是一个 scientist，会投币并请求咖啡。
2. `IUT` 模型是咖啡机，会在不同时间窗口返回 `weakCoffee!` 或 `strongCoffee!`。
3. 测试器并不会先把整条测试序列算完，而是看当前 `$Z$`，决定“现在该投币还是再等一会”。
4. 如果机器在当前时间点输出了规格不允许的咖啡，或者安静太久导致 `After(Z,\delta)=\emptyset`，就立刻判 `fail`。

通俗地说，这条方法像“带时钟的在线裁判”。它不是拿着一张固定脚本去跑，而是一边看比赛一边根据当前合法状态空间调整下一步动作。

### 运行 / 接受 / 转移语义

论文把 on-the-fly testing 的关键算子写成：

$$
After(Z,a)=Closure_\tau(\{\langle \bar{\ell}',z'\rangle \mid \langle \bar{\ell},z\rangle \in Closure_\tau(Z),\ \langle \bar{\ell},z\rangle \xrightarrow{a} \langle \bar{\ell}',z'\rangle\})
$$

以及

$$
After(Z,\delta)=\{ \langle \bar{\ell},z'\rangle \mid \langle \bar{\ell},z\rangle \in Closure^\delta_\tau(Z,\delta),\ z'=(z\land (t==\delta))\big|_{t:=0}\}
$$

上式中的符号逐项解释如下：

1. `$Closure_\tau$` 计算零时延下所有内部动作闭包。
2. `$Closure^\delta_\tau(Z,\delta)$` 计算在不超过 `$\delta$` 时间内，经内部动作可到达的符号状态集。
3. 辅助时钟 `$t$` 用来限制从最近一次可观测动作开始经过了多久。
4. 这两条公式就是在线算法的心脏。

判定逻辑则围绕 `$Z$` 是否为空、输出是否在 `ImpOutput(Z)` 内、以及是否落入环境未预期的输出来给出：

1. `fail`：实现输出或等待超出规格允许范围；
2. `inconclusive`：环境假设被破坏，测试目标无法继续；
3. `pass`：在当前观测下实现始终保持 timed trace inclusion。

### 语义边界

1. 论文默认 `IUT` 及其模型是 input-enabled。
2. 测试规格是 closed network，环境被显式建模，而不是留空。
3. 方法主体面向 dense-time timed automata，不处理连续动力学。
4. 算法的实用性依赖符号状态集规模保持可控。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 元组 | `$A=(L,\ell_0,I,E)$` | 测试规格的基础建模单位。 |
| test specification | `$TS=IUT\parallel ENV$` | 测试不是只看实现，还显式看环境。 |
| 当前状态估计 | `$Z \subseteq \{\langle \bar{\ell},z\rangle\}$` | 在线 testing 的核心运行时抽象。 |
| 动作后继 | `$After(Z,a)$` | 观察到动作后的符号更新。 |
| 延时后继 | `$After(Z,\delta)$` | 观察到时间流逝后的符号更新。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接建立在 timed automata network 与符号状态集之上。 |
| 事件 / 触发 | 很强 | 输入/输出动作是测试驱动核心。 |
| 守卫 / 数据 | 中等支持 | 支持 `UPPAAL` 风格 clocks/guards，但主体不是富数据建模。 |
| 层次 | 不支持 | 不讨论层次状态机。 |
| 并发 / 同步 | 很强 | 网络并发和同步动作是基本前提。 |
| 时间约束 | 很强 | dense-time、delay、quiescence、timed traces 都在中心位置。 |
| 连续动态 / 随机性 | 不支持 | 不涉及 hybrid / stochastic 行为。 |
| 可执行 / 可验证性 | 很强 | 算法直接驱动真实 `IUT` 并在线产出 verdict。 |

### 形式化问题与性质

1. 这篇论文把 timed testing 从离线 test-suite 生成推进到了在线交互式验证。
2. 它是后续 `T-UPPAAL`、`UPPAAL-TRON` 和 2008 年 timed testing 总结条目的直接前驱。
3. 用 `$Z$` 维护可能状态而不是猜单一状态，是 timed、nondeterministic black-box testing 能成立的关键。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `IUT` 的 timed automata 模型；
2. 环境 `ENV` 模型；
3. adapter；
4. execution strategy，如随机选择输入或等待时间。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` 风格 timed automata 网络；
2. symbolic states `\langle \bar{\ell},z\rangle`；
3. execution scenarios 形成的 timed traces；
4. `pass/fail/inconclusive` verdict。

### 交换与互操作

1. 测试器通过 adapter 把抽象动作映射到真实系统输入输出。
2. 算法直接复用 `UPPAAL` 的符号约束求解与可达性风格操作。
3. 整条路线后来演化成 `T-UPPAAL` 与 `UPPAAL-TRON` 工具链。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` timed automata 语言。
- 解析/交换/元模型支持：symbolic clock-constraint systems、location vectors、adapter 接口。
- 仿真/执行支持：测试器直接在线等待输出、发送输入并推进真实系统。
- 验证/分析支持：timed trace inclusion、state-set update、online verdicting。
- 代码生成/转换支持：不主打部署代码生成，而是测试执行驱动。
- 标准化或社区生态：作为 `T-UPPAAL / UPPAAL-TRON` 母线中的早期基础论文。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式控制器、协议实现和其他可抽象成 timed automata 的黑盒系统在线一致性测试。

### 需求前提

1. 系统和环境都能形式化成 timed automata。
2. 观测接口能区分输入动作、输出动作和时间流逝。
3. 实现可通过 adapter 被测试器驱动。
4. 测试目标以实时行为一致性为主，而不是富数据业务逻辑。

### 不适用或高成本场景

若环境假设无法明确建模、输出时间戳难以准确采集，或符号状态集爆炸过快，则这条在线路线的收益会下降。

## 与相邻形式主义的关系

相对 [t-uppaal-online-model-based-testing-of-real-time-systems/desc.md](../t-uppaal-online-model-based-testing-of-real-time-systems/desc.md)，本文是更早期的 on-the-fly 母线条目；相对 [testing-real-time-systems-using-uppaal/desc.md](../testing-real-time-systems-using-uppaal/desc.md)，2008 年那篇是更系统的综整版，补了 `TIOTS/rtioco_e/observer` 框架；相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)，后者是更接近工业案例的 `UPPAAL-TRON` 应用化落地。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明生成出来的 timed model 不一定只拿去 model checking，也可以直接驱动在线测试。
2. 对“生成-验证-修复”闭环而言，在线测试能提供另一类反例来源。
3. 如果 LLM 生成的状态机要面向真实系统验证，这类 adapter + symbolic-state-set 路线很值得保留。

### 作为目标形式主义还是中间表示

更像围绕 timed automata 的验证方法路线，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 生成 timed model 时最好同步保留环境模型，而不是只生 IUT 本体。
2. 若后续要接在线测试，输入输出方向和可观测时间行为必须在建模阶段就明确。
3. 能否维护紧凑的符号状态集，会直接影响模型的实际可验证性。

## 重要的相关工作

1. [t-uppaal-online-model-based-testing-of-real-time-systems/desc.md](../t-uppaal-online-model-based-testing-of-real-time-systems/desc.md)：更接近正式工具发布的后续条目。
2. [testing-real-time-systems-using-uppaal/desc.md](../testing-real-time-systems-using-uppaal/desc.md)：timed-testing 路线的后续系统总结。
3. [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：`UPPAAL-TRON` 工业化实例。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
