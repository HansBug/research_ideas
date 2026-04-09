# RATSY：带综合能力的需求分析工具 / RATSY - A New Requirements Analysis Tool with Synthesis

## 基本信息

- 标题：RATSY - A New Requirements Analysis Tool with Synthesis
- 中文标题：RATSY：带综合能力的需求分析工具
- 作者：Roderick Bloem，Alessandro Cimatti，Karin Greimel，Georg Hofferek，Robert Könighofer，Marco Roveri，Viktor Schuppan，Richard Seeber
- 发表：*Computer Aided Verification*，Lecture Notes in Computer Science 6174，pp. 425-429，2010
- DOI：`10.1007/978-3-642-14295-6_37`
- 链接：https://doi.org/10.1007/978-3-642-14295-6_37
- 形式主义：`Buchi automata / PSL / GR(1) reactive synthesis / RATSY`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：property-based design workbench with automaton editor, game-based debugging, realizability checking, and synthesis backends
- 工具/实现获取方式：原文明确给出 `RATSY` 站点 `http://rat.fbk.eu/ratsy/`，并说明工具主体以 `Python` 实现，符号算法通过 `SWIG` 调用 `CUDD` 与 `NuSMV`。
- 标准/格式获取方式：核心承载是 deterministic complete `Buchi` automata、自动生成的 `PSL` 公式、`GR(1)` 规格转换，以及 `BLIF / Verilog` 输出；不是中立行业交换标准。

## 简报

`RATSY` 的价值不在于提出一种新的状态机母型，而在于把“形式化需求如何写、如何调、如何判定可实现、如何一键综合”这些环节收进同一条 property-based design 工作流。相对早期 `RAT` 只做 `PSL` 级分析，`RATSY` 新增了图形化 `Buchi` 自动机编辑、基于博弈的不可实现调试、以及面向 `GR(1)` 的 correct-by-construction synthesis。

- 形式主义定位：面向反应式需求工程的分析与综合工作台，而不是新的 DSL 母语言。
- 构造方式简述：图形 `Buchi` 属性或 `PSL` 规格先进入分析链，再做 realizability / debugging / synthesis，最后可输出 `BLIF` 与 `Verilog`。
- 基础设施与场景简述：依托 `Python + CUDD + NuSMV + Wring + Anzu`，服务数字系统与反应式控制逻辑的 property-based design。

```text
informal design intent -> Buchi automata / PSL specification -> realizability + diagnostic game -> GR(1) synthesis -> BLIF / Verilog implementation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 图形化 `Buchi` 自动机属性编辑器。
2. `PSL` 级形式化需求分析。
3. 基于 counterstrategy / countertrace 的 diagnostic game。
4. `GR(1)`-oriented synthesis backend。
5. `BLIF / Verilog` 硬件实现输出。

### 核心抽象

论文最直接的形式化输入对象是用来表达单个属性的 deterministic complete `Buchi` word automaton，可保守整理为：

$$
A = (\Sigma, Q, q_0, \delta, F)
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是信号字母表，由输入/输出布尔信号赋值组成。
2. `$Q$` 是自动机状态集合。
3. `$q_0 \in Q$` 是初始状态。
4. `$\delta : Q \times \Sigma \rightarrow Q$` 是确定性转移函数。
5. `$F \subseteq Q$` 是接受状态集合，用于表达 `Buchi` 接受条件。

原文明确指出编辑器要求自动机保持 deterministic 和 complete，这一点可整理为：

$$
\forall q \in Q,\ \forall \sigma \in \Sigma,\ \exists ! q' \in Q:\ \delta(q,\sigma) = q'
$$

上式中的符号逐项解释如下：

1. `$\exists !$` 表示“存在且仅存在一个”。
2. 该条件同时编码了完备性与确定性。
3. 工具通过隐式 dead state 与自动更新 guard 条件来维持这一约束。

对其 synthesis backend，正文说明它复用了 `Anzu` 风格的 `GR(1)` 路线。根据原文“支持 `GR(1)` 规格并执行若干语法转换”的描述，可把其核心可综合输入保守整理为：

$$
(\varphi_i^a \land \varphi_s^a \land \varphi_l^a) \Rightarrow (\varphi_i^g \land \varphi_s^g \land \varphi_l^g)
$$

上式中的符号逐项解释如下：

1. `$\varphi_i^a$` 是环境初始假设。
2. `$\varphi_s^a$` 是环境安全假设。
3. `$\varphi_l^a$` 是环境活性假设。
4. `$\varphi_i^g$`、`$\varphi_s^g$`、`$\varphi_l^g$` 分别是系统的初始、安全、活性保证。
5. 这不是论文正文逐字写出的公式，而是依据其 `GR(1)` synthesis backend 描述做的保守归纳。

### 一个最小例子与通俗解释

可以用一个“请求-应答”需求来理解 `RATSY` 的工作方式：

1. 环境信号 `req` 表示外部发出请求。
2. 系统信号 `ack` 表示系统给出应答。
3. 用户在图形编辑器里画一个简单 `Buchi` 自动机，要求“只要 `req` 出现，之后最终要进入 `ack` 为真的接受状态”。
4. 如果规格与其他安全约束冲突，工具会给出 counterstrategy，并让用户在 diagnostic game 里扮演系统玩家，直观看到“哪里根本走不通”。

通俗地说，`RATSY` 像是“把形式化需求变成可画、可玩、可综合”的工作台。你不是只写一堆时序逻辑公式，而是先画属性自动机、再看调试博弈、最后直接点到综合输出。

### 运行 / 接受 / 转移语义

单个属性自动机的接受语义仍然是标准 `Buchi`：

$$
\mathrm{Run}(w) = q_0 q_1 q_2 \cdots,\quad q_{k+1} = \delta(q_k, w_k)
$$

$$
w \in L(A) \iff \mathrm{Inf}(\mathrm{Run}(w)) \cap F \neq \emptyset
$$

上式中的符号逐项解释如下：

1. `$w = w_0 w_1 w_2 \cdots$` 是信号赋值序列。
2. `$\mathrm{Run}(w)$` 是该序列在自动机上的运行。
3. `$\mathrm{Inf}(\mathrm{Run}(w))$` 是运行中无限次出现的状态集合。
4. 若这些无限访问状态与接受集 `$F$` 有交集，则该运行被接受。

论文对调试的核心解释是“用户作为系统玩家，对抗由 unrealizable core 导出的 counterstrategy / countertrace”。这可以保守整理成一个诊断博弈：

$$
G = (V_e, V_s, E, v_0, Win)
$$

上式中的符号逐项解释如下：

1. `$V_e$` 是环境步位置集合。
2. `$V_s$` 是系统步位置集合。
3. `$E$` 是环境动作与系统动作的交替边。
4. `$v_0$` 是调试起点。
5. `$Win$` 表示与原规格一致的系统目标条件。

### 语义边界

1. `RATSY` 不是一般 `LTL` synthesis 平台；正文强调 synthesis 与 debugging 主线主要围绕 `GR(1)`。
2. 它的图形前端聚焦 `Buchi` 属性自动机，而不是层次状态机或时钟自动机。
3. 它更适合作为反应式数字系统的 property-based design 工具，而不是连续控制器运行时。
4. 对 full `LTL`，正文提到的是 preliminary realizability route，而非完整 debugging / synthesis 全能力支持。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 属性自动机骨架 | `$A = (\Sigma, Q, q_0, \delta, F)$` | 图形编辑器的核心建模对象。 |
| 确定完备约束 | `$\forall q,\forall \sigma,\exists !q':\delta(q,\sigma)=q'$` | 工具以隐式 dead state 和自动更新条件保证 determinism / completeness。 |
| `Buchi` 接受 | `$w \in L(A) \iff \mathrm{Inf}(\mathrm{Run}(w)) \cap F \neq \emptyset$` | 图形属性最终仍落到标准 `Buchi` 语义。 |
| `GR(1)` 可综合骨架 | `$(\varphi_i^a \land \varphi_s^a \land \varphi_l^a) \Rightarrow (\varphi_i^g \land \varphi_s^g \land \varphi_l^g)$` | `RATSY` synthesis backend 的核心可解片段。 |
| 调试博弈 | `$G = (V_e, V_s, E, v_0, Win)$` | 不可实现规格通过 diagnostic game 暴露冲突点。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 输入是属性自动机与反应式实现，不是显式业务状态机 DSL。 |
| 事件 / 触发 | 很强 | 信号条件、自动机转移与反应式环境/系统交互是核心。 |
| 守卫 / 数据 | 中等支持 | 主要处理布尔与有限域信号；多值变量由 `NuSMV` 自动编码为布尔量。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 中等支持 | 以同步信号步进和博弈式环境/系统回合为主。 |
| 时间约束 | 不支持 | 不涉及 dense time 或 clocks。 |
| 连续动态 / 随机性 | 不支持 | 面向离散反应式数字系统。 |
| 可执行 / 可验证性 | 很强 | realizability、simulation、diagnostic game、synthesis、`BLIF/Verilog` 输出一体化。 |

### 形式化问题与性质

1. 论文的创新重点是把“写规格、测规格、调规格、综合实现”打通，而不是单点优化某个求解算法。
2. 图形化 `Buchi` 编辑器降低了需求编写门槛，但底层仍然回到 `PSL / GR(1)` 语义。
3. 调试阶段采用对抗博弈，把 unrealizability 变成可交互的故障定位过程，这比只给一个“不可实现”结论更适合需求修复。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 图形 `Buchi` automaton editor。
2. 直接输入 `PSL` 规格。
3. 参数化 automata instantiation。
4. realizability / synthesis 命令式工作流。

### 机器可处理承载方式

机器可处理承载方式包括：

1. deterministic complete `Buchi` automata。
2. 自动生成的 `PSL` 公式。
3. 语法变换后的 `GR(1)` 或 `LTL` 规格。
4. 综合得到的 `BLIF` 与 `Verilog` 电路表示。

### 交换与互操作

1. 图形 automata 与 `PSL` 双入口互相连通。
2. 后端依赖 `NuSMV` parser 进行语法转换与布尔编码。
3. full `LTL` 路线借助 `Wring` 与 Lily 相关转换组件。
4. 综合实现可导出 `BLIF / Verilog`，便于接后续硬件或验证链。

## 配套基础设施

- 建模/编辑工具：图形 `Buchi` automaton editor，可自动维护 determinism 与 completeness。
- 解析/交换/元模型支持：`PSL` parser、`NuSMV` parser、`SWIG` bridge、multi-valued-to-Boolean encoding。
- 仿真/执行支持：对 realizable 规格先综合实现，再由用户在 GUI 中做 simulation。
- 验证/分析支持：trace-level analysis、realizability checking、unrealizable core、counterstrategy / countertrace diagnostic game。
- 代码生成/转换支持：`GR(1)` synthesis backend，输出 `BLIF` 与 `Verilog`。
- 标准化或社区生态：依托 `Python + CUDD + NuSMV + Wring + Anzu` 的组合式研究生态；原文未给行业标准化承载。

## 适用场景与需求前提

### 适用场景

适合反应式数字系统、接口协议、控制逻辑和 property-based design 流程中“需求先行、实现后到”的场景，尤其适合需要先判定规格是否 realizable、再做 correct-by-construction synthesis 的项目。

### 需求前提

1. 需求需能落成 `PSL` 或 deterministic complete `Buchi` 属性自动机。
2. 系统/环境交互应主要表现为有限信号步进，而不是连续动态。
3. 若希望进入 synthesis 路线，规格最好能转换到 `GR(1)` 片段。
4. 团队愿意把 debugging 前移到规格阶段，而不是等实现后再排查。

### 不适用或高成本场景

1. 复杂连续控制、概率行为或 dense-time 约束不适合直接用 `RATSY`。
2. 若需求本身无法结构化为环境假设与系统保证，综合链会很难稳定工作。
3. 若只需要一个轻量时序逻辑检查器，不一定需要整套图形编辑与 diagnostic game 基础设施。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 更偏可插拔 `GR(1)` synthesis backend，而 `RATSY` 更强调需求录入、图形 `Buchi` 编辑与 diagnostic game；相对 [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md)，`Spectra` 是更系统的文本 DSL 前端，而 `RATSY` 仍以图形 automata / `PSL` 为主；相对 [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)，`Acacia` 更聚焦 `LTL` synthesis 本身，而 `RATSY` 把“需求分析 + debugging + synthesis”集成为一条设计链。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“结构化需求 -> 形式化规格 -> 调试 -> 综合”可以是一个连续闭环，而不是彼此割裂的环节。
2. 图形 `Buchi` 属性编辑器对“LLM 先抽需求模式、再落属性自动机”的中间表示设计很有启发。
3. diagnostic game 提供了非常适合作为修复反馈的交互式解释对象。

### 作为目标形式主义还是中间表示

更适合作为需求分析与 synthesis 前端工作台，而不是最终系统长期维护的主状态机表示。

### 对需求到模型生成的启发

1. 不必一开始就让模型生成直接落到底层实现，可以先落到可检查的属性层。
2. “自动机 + 时序公式”双表示并存，比单一文本公式更利于需求确认与修复。
3. 如果未来要做“生成-验证-修复”闭环，counterstrategy 与 unrealizable core 是高价值反馈信号。

### 现实限制

其综合能力依赖底层 `GR(1)` / restricted `LTL` 片段；超出该边界后，`RATSY` 更像分析器而不是一站式综合平台。

## 重要的相关工作

1. `RAT`：`RATSY` 的直接前身，负责 `PSL` 级形式化需求分析。
2. `Anzu`：正文明确说明 synthesis 功能基于 Python 重写的 `Anzu` 路线。
3. `NuSMV 2` 与 `CUDD`：分别提供解析/布尔编码和符号算法底座。
4. Lily / Wring / bounded synthesis / antichain realizability：构成正文所列的 full `LTL` 和相邻综合路线参考。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Buchi automata / PSL / GR(1) reactive synthesis / RATSY`
- 论文角色：property-based design workbench with automaton editor, game-based debugging, and synthesis
- 核心功能：把反应式需求的编辑、分析、diagnostic game 调试与实现综合收进同一工作台
- 关键特性：graphical `Buchi` editor、`PSL` generation、realizability、counterstrategy debugging、`GR(1)` synthesis、`BLIF/Verilog`
