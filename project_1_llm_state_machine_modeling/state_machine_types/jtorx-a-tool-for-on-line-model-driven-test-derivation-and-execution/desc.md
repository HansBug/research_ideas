# JTorX：在线模型驱动测试推导与执行工具 / JTorX: A Tool for On-Line Model-Driven Test Derivation and Execution

## 基本信息

- 标题：JTorX: A Tool for On-Line Model-Driven Test Derivation and Execution
- 中文标题：JTorX：在线模型驱动测试推导与执行工具
- 作者：Axel Belinfante
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 266-270，2010
- DOI：`10.1007/978-3-642-12002-2_21`
- 链接：https://doi.org/10.1007/978-3-642-12002-2_21
- 形式主义：`IOLTS / ioco / uioco / JTorX`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：on-line model-based testing / `(u)ioco` checking workbench
- 工具/实现获取方式：论文明确给出原始入口 `http://fmt.cs.utwente.nl/tools/jtorx/`，并说明 `JTorX` 以 `BSD` 风格许可证免费发布；当前仍可通过 University of Twente 研究页面与历史镜像追溯。
- 标准/格式获取方式：原文明确列出 `graphml`、Aldebaran `.aut`、`Jararaca` traces、`TorX Explorer protocol`、`TorX Adapter protocol`、标准输入输出与单 TCP 连接等承载/接口方式。

## 简报

这篇论文的重点，不是提出新的测试理论，而是把 `ioco/uioco` 一套“在线推导、在线执行、在线判定”的模型驱动测试工作流做成易部署、易教学、也足够开放的工具链。`JTorX` 通过 `Explorer/Primer/Driver/Adapter` 这组模块，把模型、测试目的、悬挂自动机、被测系统和日志/消息序列图统一到一个在线测试框架里。

- 形式主义定位：基于 `ioco/uioco` 的在线模型驱动测试路线，而不是新的状态机家族。
- 构造方式简述：先以 `graphml/.aut` 或 `TorX Explorer` 暴露模型，再由 `Primer` 构造 suspension automaton，`Driver` 在线决定刺激/观测，`Adapter` 把动作落到真实 SUT。
- 基础设施与场景简述：依托 `ioco/uioco` 理论、`Explorer` 接口、日志/MSC 视图、interactive/guided simulation 与 `(u)ioco` checkers，服务协议、组件与交互系统的模型驱动测试教学和快速验证。

```text
IOLTS-like model -> Explorer -> Primer / suspension automaton -> Driver + Adapter -> on-line test derivation / execution -> verdict + log + MSC
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `JTorX`：

1. 基于 `ioco/uioco` 的模型驱动测试理论。
2. 作为状态空间统一入口的 `Explorer`。
3. 负责 determinization 与 quiescence 标记的 `Primer`。
4. 负责在线测试控制的 `Driver`。
5. 负责连接真实 SUT 的 `Adapter` 与可选 `Combinator/Test Purpose`。

### 核心抽象

结合论文“labelled transition system state space”“suspension automaton”“(u)ioco-related”这些表述，可把其所依赖的模型骨架保守整理为：

$$
M = (S, s_0, L_I, L_O, \to)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `s_0` 是初始状态。
3. `L_I` 是输入动作集合。
4. `L_O` 是输出动作集合。
5. `\to` 是带标签迁移关系。
6. 这是依据论文所述 `ioco`/LTS 背景做的保守标准化整理，不是本文显式给出的统一元组。

论文直接给出了工具核心组件图，可保守压成：

$$
\mathrm{JTorX} = (\mathrm{Explorer}, \mathrm{Primer}, \mathrm{Driver}, \mathrm{Adapter}, \mathrm{Combinator})
$$

上式中的符号逐项解释如下：

1. `Explorer` 提供对模型或测试目的状态空间的统一访问。
2. `Primer` 在需要时构造 suspension automaton。
3. `Driver` 控制一次测试运行，决定是施加刺激、检查观测还是停止。
4. `Adapter` 连接真实或模拟的 SUT。
5. `Combinator` 在 guided test run 中把模型与 test purpose 组合。
6. 这与论文图 1 的组件分解一致。

由于论文明确说明 `Primer` 会把 quiescent states 标上 `\delta` 自循环，可把它的核心行为保守写成：

$$
\mathrm{SA}(M) = \mathrm{det}(M) \cup \{(s,\delta,s) \mid s \text{ is quiescent}\}
$$

上式中的符号逐项解释如下：

1. `\mathrm{det}(M)` 表示对模型的确定化结果。
2. `\delta` 是 quiescence 标签。
3. 若状态 `s` 是 quiescent，则在 suspension automaton 中为其加上 `\delta` 自循环。
4. 这是对论文“determinizes and marks quiescent states with δ-labelled selfloops”的直接整理。

基于论文所依赖的 `ioco` 理论，可把工具的判定目标保守写成：

$$
I \mathrel{\mathrm{ioco}} S \iff \forall \sigma \in \mathrm{Straces}(S): out(I \after \sigma) \subseteq out(S \after \sigma)
$$

上式中的符号逐项解释如下：

1. `I` 是实现或被测系统的行为模型。
2. `S` 是规范模型。
3. `\sigma` 是规范允许的 suspension traces。
4. `out(X \after \sigma)` 表示系统 `X` 在执行 `\sigma` 后可能产生的输出/静默集合。
5. 这条公式不是本文新定义，而是论文明确声称其工具所依据的 `ioco` 核心判定思想。

### 一个最小例子与通俗解释

论文没有展开完整 toy protocol，但它给出的最小工作链很清楚：

1. 先把模型以 `graphml`、`.aut` 或 `TorX Explorer` 暴露给 `Explorer`。
2. `Primer` 在需要时按需构造 suspension automaton。
3. `Driver` 在线决定接下来是发一个刺激、接收一个观测还是结束测试。
4. `Adapter` 把动作落到真实程序的标准输入输出或 TCP 连接上。
5. 测试过程实时产生日志和动态消息序列图。

通俗地说，`JTorX` 像一个“边测边想”的模型驱动测试器：它不是先把整份测试脚本离线生成好，而是在测试进行过程中，持续根据模型和 SUT 的反馈决定下一步做什么。

### 运行 / 接受 / 转移语义

从论文的工具架构看，一次在线测试的运行逻辑可保守整理为：

$$
(\mathit{model}, \mathit{sut}, q) \xrightarrow{\mathrm{Driver}} (\mathit{stimulus} \mid \mathit{observe} \mid \mathit{stop})
$$

上式中的符号逐项解释如下：

1. `model` 是由 `Explorer/Primer` 暴露给测试器的当前模型状态。
2. `sut` 是 `Adapter` 所连接的被测系统当前可交互接口。
3. `q` 是 `Driver` 当前掌握的测试运行上下文。
4. `stimulus`、`observe`、`stop` 对应论文对 `Driver` 职责的原文描述。

同时，guided test run 时还会引入 test purpose：

$$
\mathrm{Run}_{guided} = \mathrm{Combinator}(M, TP)
$$

其中：

1. `M` 是模型。
2. `TP` 是 test purpose。
3. `Combinator` 让 `Driver` 在模型与目标轨迹共同约束下选择动作。

### 语义边界

论文也清楚给出边界：

1. `JTorX` 强依赖 `ioco/uioco` 与 suspension automata 视角。
2. 参数化动作标签和更复杂的实时扩展在文末仍被列为未来工作。
3. 工具强调在线推导、在线执行与教育友好，而不是单纯高性能离线测试生成。
4. 其开放性来自接口协议与模型格式支持，而不是通用交换标准本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$M = (S, s_0, L_I, L_O, \to)$` | 对应论文背后的 `ioco` / LTS 建模对象。 |
| 工具组件 | `$\mathrm{JTorX} = (\mathrm{Explorer}, \mathrm{Primer}, \mathrm{Driver}, \mathrm{Adapter}, \mathrm{Combinator})$` | 论文图 1 给出的核心架构。 |
| suspension automaton | `$\mathrm{SA}(M) = \mathrm{det}(M) \cup \{(s,\delta,s) \mid s \text{ is quiescent}\}$` | 对应 `Primer` 的 determinize + quiescence marking 行为。 |
| `ioco` 判定目标 | `$I \mathrel{\mathrm{ioco}} S \iff \forall \sigma \in \mathrm{Straces}(S): out(I \after \sigma) \subseteq out(S \after \sigma)$` | 对应论文所依赖的核心测试一致性关系。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 基础对象就是 LTS / suspension automaton 状态空间。 |
| 事件 / 触发 | 很强 | 输入、输出、静默与 test purpose 路径共同驱动测试。 |
| 守卫 / 数据 | 弱支持 | 主线是基于标签与 traces 的行为测试，而不是复杂数据守卫。 |
| 层次 | 不适用 | 论文主体不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 通过外部建模环境和 Explorer 接口接入，不在工具本体内部重定义。 |
| 时间约束 | 有扩展潜力 | 论文提到可与 timed testing 方向衔接，但主体不是 timed JTorX。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 在线推导、执行、模拟、`(u)ioco` checking 与日志可视化都已打通。 |

### 形式化问题与性质

1. `JTorX` 的关键价值，在于把 `TorX` 的开放架构保留下来，同时显著降低部署与教学使用门槛。
2. `uioco`、underspecified trace checking 和 `(u)ioco` model-to-model checking，让它不只是“跑测试”的工具，也能先审模型。
3. 动态 `MSC`、interactive/guided simulation 和内建 `graphml/.aut` 支持，使它特别适合解释测试过程。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. 使用 `graphml` 绘制 automata，或导入 Aldebaran `.aut`。
2. 通过 `TorX Explorer protocol` 连接 `mCRL2`、`LTSmin`、`CADP` 等外部环境。
3. 使用 `Jararaca` 文件表达正则式风格 traces / test guidance。
4. 通过 `Adapter` 把模型测试动作接到真实程序、模拟模型或 TCP 服务。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `graphml`。
2. Aldebaran `.aut` 文件。
3. `Jararaca` traces。
4. `TorX Explorer protocol` 与 `TorX Adapter protocol`。
5. 标准输入输出或单 TCP 连接。

### 交换与互操作

这条路线的互操作重点非常明确：

1. `Explorer` 把外部建模环境统一抽象成状态空间访问接口。
2. `Adapter` 把真实 SUT 与测试器解耦。
3. `graphml`、`.aut`、`Jararaca` 让模型、轨迹和 test purpose 都有可导入入口。

## 配套基础设施

- 建模/编辑工具：`yEd` + `graphml`、外部 LTS 环境、交互式 GUI。
- 解析/交换/元模型支持：`.aut`、`graphml`、`Jararaca`、`TorX Explorer` 协议。
- 仿真/执行支持：manual exploration、guided simulation、在线测试执行。
- 验证/分析支持：underspecified trace checker、`(u)ioco` checker、动态 `MSC`、日志。
- 代码生成/转换支持：不以代码生成/部署为主，重点是在线测试派生。
- 标准化或社区生态：依托 `ioco` 理论、University of Twente 工具线以及 `mCRL2/LTSmin/CADP` 等生态桥接。

## 适用场景与需求前提

### 适用场景

适合协议、组件、交互系统和课程实验中的模型驱动测试，尤其适合需要边执行边派生测试、并希望把测试过程可视化解释出来的场景。

### 需求前提

1. 模型能够以 LTS / IOLTS 风格暴露。
2. 关注的是输入输出一致性、静默、未指定 traces 等交互行为问题。
3. 团队接受在线测试而不是只做离线测试脚本生成。
4. SUT 能通过标准输入输出、TCP 或适配器协议接入。

### 不适用或高成本场景

如果系统强依赖复杂数据、连续动力学或高密度时间约束，而又没有合适的外部 Explorer/Adapter 支撑，`JTorX` 的收益会明显下降。

## 与相邻形式主义的关系

相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)，`UPPAAL TRON` 更偏 timed automata 的实时测试，而 `JTorX` 更偏一般 `ioco/uioco` 在线测试骨架；相对 [modelling-verifying-and-testing-the-contract-automata-runtime-environment-with-uppaal/desc.md](../modelling-verifying-and-testing-the-contract-automata-runtime-environment-with-uppaal/desc.md)，后者是在已有 runtime 之上做定时分析，而 `JTorX` 直接把模型测试执行做成前台工具；相对 [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)，`libFAUDES` 更像算法库，`JTorX` 更像测试执行工作台。

## 与本研究的关系

### 对 Project 1 的价值

它补了一条非常重要的“生成后如何测”的路线：如果 `project_1` 将来让 LLM 生成某种交互式状态机，`JTorX` 说明可以先把模型暴露成统一状态空间，再在线派生测试，而不必先把全部测试用例离线枚举出来。

### 作为目标形式主义还是中间表示

更像测试与分析基础设施，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. 若生成的状态机能明确区分输入、输出和静默，后续测试链会清晰很多。
2. 状态机工具链的关键不只在格式，还在 `Explorer/Adapter` 这类桥接接口。
3. 在线测试特别适合在模型尚不稳定、需要快速试探边界时使用。

### 现实限制

这条路线默认问题能被收束成 `ioco/uioco` 风格的交互一致性判断；对更复杂的时空语义仍需外部补强。

## 重要的相关工作

1. [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：实时测试工具线。
2. [modelling-verifying-and-testing-the-contract-automata-runtime-environment-with-uppaal/desc.md](../modelling-verifying-and-testing-the-contract-automata-runtime-environment-with-uppaal/desc.md)：runtime verification + testing 工具桥。
3. [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)：离散事件系统算法库型基础设施。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`IOLTS / ioco / uioco / JTorX`
- 论文角色：on-line model-based testing / `(u)ioco` checking workbench
- 归类理由：论文主体是基于 `ioco/uioco` 的在线测试推导与执行路线，并通过 `JTorX` 将其做成可操作工具链。
