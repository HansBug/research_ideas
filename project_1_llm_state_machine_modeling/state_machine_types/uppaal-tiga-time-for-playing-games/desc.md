# UPPAAL-Tiga：与时间博弈对弈 / UPPAAL-Tiga: Time for Playing Games!

## 基本信息

- 标题：UPPAAL-Tiga: Time for Playing Games!
- 中文标题：UPPAAL-Tiga：与时间博弈对弈
- 作者：Gerd Behrmann，Agnès Cougnard，Alexandre David，Emmanuel Fleury，Kim G. Larsen，Didier Lime
- 发表：*Computer Aided Verification*，`LNCS 4590`，pp. 121-125，2007
- DOI：`10.1007/978-3-540-73368-3_14`
- 链接：https://doi.org/10.1007/978-3-540-73368-3_14
- 形式主义：`Timed Game Automata / NTGA / UPPAAL-Tiga`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-game controller-synthesis workbench / strategy generation and simulation tool
- 工具/实现获取方式：原文明确给出 `UPPAAL-Tiga` 作为集成进 `UPPAAL` 生态的新一代 timed-game 工具，支持命令行与图形模拟器输出策略，并提到与 `Simulink/Real-Time Workshop` 的完整合成-仿真-代码生成链路。
- 标准/格式获取方式：承载方式沿用 `UPPAAL 4.0` 的扩展输入语言、template/network 建模和查询语法；控制目标用 `control:P` 表示，策略可导出为 decision graphs（`BDD/CDD` 混合表示）。

## 简报

这篇论文的核心贡献，不是重新提出 timed game automata，而是把它做成第一套真正高效、可交互、可输出 controller strategy 的成熟工具。`UPPAAL-Tiga` 把 controllable/uncontrollable action 分区、实时博弈求解、策略导出和 GUI 对战模拟放到同一个环境里，使“实时控制综合”从理论算法变成可操作的工具链。

- 形式主义定位：基于 `Timed Game Automata` 的控制综合与博弈分析工具，而不是新的状态机族母型。
- 构造方式简述：以 network of timed game automata 为建模对象，在 `UPPAAL 4.0` 前端上输入模型，再通过 `control:P` 查询求 winning strategy。
- 基础设施与场景简述：依托 `UPPAAL 4.0` 输入语言、DBM/BDD/CDD 后端、GUI/CLI 和策略图导出，服务 safety / reachability controller synthesis 与实时系统博弈验证。

```text
timed game automata network -> control:P query -> symbolic game solving -> winning strategy / counter-strategy -> simulation and controller synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed game automata；
2. network of timed game automata (`NTGA`)；
3. controllable / uncontrollable actions；
4. safety / reachability control objectives；
5. strategy generation、decision graphs 与 simulator。

### 核心抽象

对单个 timed game automaton，论文的核心差异在动作分区：

$$
\Sigma = \Sigma_c \uplus \Sigma_u
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是动作集合。
2. `$\Sigma_c$` 是 controllable actions，由 controller 触发。
3. `$\Sigma_u$` 是 uncontrollable actions，由 environment/opponent 触发。
4. `$\uplus$` 表示二者不交且共同构成全部动作。

网络模型可保守整理为：

$$
G = A_1 \parallel A_2 \parallel \cdots \parallel A_n
$$

上式中的符号逐项解释如下：

1. `$A_i$` 是单个 timed game automaton。
2. `$\parallel$` 表示网络化组合。
3. `$G$` 是整个待综合控制对象。

论文对控制目标直接采用查询形式：

$$
\texttt{control: } P
$$

其中

$$
P \in \{A[]\varphi,\ A[\varphi_1 W \varphi_2],\ A<>\varphi,\ A[\varphi_1 U \varphi_2]\}
$$

上式中的符号逐项解释如下：

1. `$\varphi,\varphi_1,\varphi_2$` 是状态谓词。
2. `$A[]\varphi$` 表示总是满足安全性质。
3. `$A<>\varphi$` 表示最终到达目标状态。
4. `$W$` 与 `$U$` 分别是 weak until 与 until。
5. `control:P` 表示要综合一个策略，使系统在所有环境动作下满足 `$P$`。

winning strategy 也可保守整理为：

$$
\sigma : State \to (\Sigma_c \cup \{\mathrm{delay}\})
$$

上式中的符号逐项解释如下：

1. `$\sigma$` 是 controller strategy。
2. `State` 是当前符号状态。
3. 输出要么是执行某个 controllable action，要么是选择 delay。
4. 这与论文原文“perform a controllable action or delay”的描述一致。

### 一个最小例子与通俗解释

论文给了一个最小示例：

1. 模型只有一个 clock `$x$`。
2. 既有 controllable edges `c_i`，也有 uncontrollable edges `u_i`。
3. 目标是达到 `Goal`。
4. 查询写成 `control: A<> A.Goal`。

通俗地说，`UPPAAL-Tiga` 不是只问“这个系统会不会到 Goal”，而是在问：“我能不能在环境乱动的情况下，仍然总能把系统带到 Goal？” 这就是实时控制综合，而不只是普通模型检查。

### 运行 / 接受 / 转移语义

其核心语义差别是 environment priority。可保守写成：

$$
\mathrm{Pre}_{ctrl}(S) = \{\, s \mid \exists \sigma(s)\ \forall \text{ opponent moves},\ \mathrm{Next}(s,\sigma)\subseteq S \,\}
$$

上式中的符号逐项解释如下：

1. `$S$` 是当前安全或可赢状态集。
2. `$\sigma(s)$` 是 controller 在状态 `$s$` 的选择。
3. `$\mathrm{Next}(s,\sigma)$` 表示在该选择及环境响应下的后继。
4. 这体现了“对所有 uncontrollable moves 都必须可赢”的博弈语义。

对 reachability 控制目标，则对应：

$$
\exists \sigma\ \forall \pi_{env}\ .\ \pi_{\sigma,\pi_{env}} \models A<>\varphi
$$

上式中的符号逐项解释如下：

1. `$\sigma$` 是 controller strategy。
2. `$\pi_{env}$` 是环境策略或环境动作序列。
3. `$\pi_{\sigma,\pi_{env}}$` 是二者共同诱导出的运行。
4. 该式表达“存在控制器，使所有环境对抗下最终到达目标”。

### 语义边界

论文同时明确了边界：

1. 主线是 perfect-observation timed games。
2. 部分可观测综合是后续方向，不是当前成熟功能。
3. zeno-avoiding strategy 在当时还是 future work。
4. 它服务 timed games，不是概率游戏或混成博弈通用平台。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 动作分区 | `$\Sigma = \Sigma_c \uplus \Sigma_u$` | controller 与 environment 的基本分工。 |
| 网络模型 | `$G = A_1 \parallel \cdots \parallel A_n$` | 工具处理的是 timed game automata 网络。 |
| 控制查询 | `$\texttt{control: }P$` | 用户与求解器的直接接口。 |
| 策略接口 | `$\sigma : State \to (\Sigma_c \cup \{\mathrm{delay}\})$` | 输出是控制动作或延时。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心对象是 timed game automata network。 |
| 事件 / 触发 | 很强 | 通过 controllable / uncontrollable actions 建模博弈。 |
| 守卫 / 数据 | 中等支持 | 继承 `UPPAAL` 风格 guards、clocks 与扩展输入语言。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 很强 | 网络组合与同步是基础能力。 |
| 时间约束 | 很强 | 这是 timed-game synthesis 工具。 |
| 连续动态 / 随机性 | 不支持 | 不面向 hybrid / stochastic games。 |
| 可执行 / 可验证性 | 很强 | 支持策略生成、counter-strategy、GUI/CLI 对战和 decision-graph 输出。 |

### 形式化问题与性质

1. 这篇论文补的是“实时博弈求解可工程化”。
2. 它把 timed-game synthesis 直接放进 `UPPAAL` 的输入和交互范式里，降低了 adoption 成本。
3. 决策图和 simulator 让 strategy 不只停留在 yes/no 判定上。

## 构造方式与承载格式

### 建模入口

建模入口沿用 `UPPAAL 4.0`：

1. template / network 建模；
2. extended input language；
3. `control:P` 查询；
4. GUI/CLI 启动策略求解。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `NTGA` symbolic states；
2. `UPPAAL` 风格 clocks、guards、actions；
3. `TCTL`-style control queries；
4. decision graphs（离散部分 `BDD`、符号部分 `CDD`）。

### 交换与互操作

互操作重点体现在：

1. 与 `UPPAAL 4.0` 前端完全整合。
2. 可导出 strategy / counter-strategy。
3. 可与 `Simulink`、`Real-Time Workshop` 组合成 synthesis-to-code chain。

## 配套基础设施

- 建模/编辑工具：直接继承 `UPPAAL 4.0` GUI 与扩展输入语言。
- 解析/交换/元模型支持：支持 `UPPAAL` 模板化输入、`control:P` 查询与 decision-graph 输出。
- 仿真/执行支持：GUI/CLI 都可让用户与策略对战；也支持策略导出。
- 验证/分析支持：reachability / safety control objectives、controller synthesis、counter-strategy generation。
- 代码生成/转换支持：论文明确提到和 `Simulink/Real-Time Workshop` 结合的完整链路。
- 标准化或社区生态：依附 `UPPAAL` 生态，是 timed-game synthesis 的专门扩展。

## 适用场景与需求前提

### 适用场景

适合实时控制综合、资源/调度控制、工业实时系统博弈验证，以及需要把 environment uncertainty 显式建成对手的场景。

### 需求前提

1. 系统能抽成 timed game automata。
2. 动作必须能明确分成 controllable 与 uncontrollable。
3. 性质应主要落成安全或可达类控制目标。

### 不适用或高成本场景

若系统更像概率平台、部分可观测博弈、连续动力学或 rich dataful protocol game，仅靠 `UPPAAL-Tiga` 不够。

## 与相邻形式主义的关系

相对 [timed-controller-synthesis-an-industrial-case-study/desc.md](../timed-controller-synthesis-an-industrial-case-study/desc.md)，那篇展示 timed-game synthesis 的工业应用，而本文是其工具底座；相对 [ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md](../ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md)，两者都依赖 `UPPAAL` 生态，但 `ECDAR` 偏 timed interface theory，`UPPAAL-Tiga` 偏 controller synthesis；相对 [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)，`UPPAAL-SMC` 偏统计验证，`UPPAAL-Tiga` 偏博弈求解与策略综合。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提供了“带环境对抗的实时状态机”后端，不再只是普通定时自动机验证。
2. 若后续需求里存在 controller / environment 明确分责，`Timed Game Automata` 会比普通 `TA` 更合适。
3. 它也说明工具链成熟度会直接影响形式主义选型。

### 作为目标形式主义还是中间表示

更适合作为高价值后端形式主义或验证/综合后端，而不是大多数需求建模任务的默认前端表示。

### 对需求到模型生成的启发

1. 需求分析阶段应尽早识别哪些事件是 controllable、哪些是 environment-driven。
2. 若目标是策略综合，就必须在生成模型时保留对手动作边界。
3. 查询语言 `control:P` 的存在说明“模型生成”和“控制问题表达”需要一起设计。

## 重要的相关工作

1. [timed-controller-synthesis-an-industrial-case-study/desc.md](../timed-controller-synthesis-an-industrial-case-study/desc.md)：`UPPAAL-Tiga` 在工业油泵案例中的应用。
2. [ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md](../ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md)：timed interface 环境。
3. [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)：`UPPAAL` 生态中的统计验证扩展。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Game Automata / NTGA / UPPAAL-Tiga`
- 论文角色：timed-game controller-synthesis workbench / strategy generation and simulation tool
- 归类理由：论文主体是 timed game automata 的工程化求解平台、策略输出与工具集成，而不是新的 timed-state-machine 本体。
