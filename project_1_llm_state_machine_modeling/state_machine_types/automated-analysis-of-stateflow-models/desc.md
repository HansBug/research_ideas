# Stateflow 模型的自动化分析 / Automated Analysis of Stateflow Models

## 基本信息

- 标题：Automated Analysis of Stateflow Models
- 中文标题：Stateflow 模型的自动化分析
- 作者：Hamza Bourbouh, Pierre-Loic Garoche, Christophe Garion, Arie Gurfinkel, Temesghen Kahsai, Xavier Thirioux
- 发表：*EPiC Series in Computing*, 46:144-161, 2017
- DOI：`10.29007/b8gq`
- 链接：https://doi.org/10.29007/b8gq
- 形式主义：`Stateflow / CPS denotational semantics / CoCoSim Lustre translation`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`Stateflow` 自动语义编译、安全验证与代码生成路线
- 工具/实现获取方式：原文说明实现包括 `OCaml` 解释器与代码生成器，并把 `Stateflow -> Lustre automaton` 代码生成器集成进开源 `CoCoSim` 分析框架；文中给出 CoCoSim 相关代码与 regression-test 入口。
- 标准/格式获取方式：输入承载是 `MathWorks Simulink/Stateflow` chart；中间承载是 CPS 化 denotational semantics、hierarchical state machine 与 `Lustre automaton`；验证侧进一步生成 `Horn clauses`，不是独立行业交换标准。

## 简报

这篇论文的价值在于把 `Stateflow` 从“工业工具里的图形控制语言”推到“可编译、可验证、可复用后端的语义路线”。作者不满足于把 chart 简单拍平成普通转移系统，而是从 Hamon 的 `Stateflow` 语义出发，用 continuation-passing style (`CPS`) 重写 denotational semantics，再实例化成解释器、命令式代码生成器和 `Lustre automaton` 代码生成器，最终接入 `CoCoSim` 做 safety property 验证。

- 形式主义定位：`Stateflow` 的自动分析与编译路线，而不是新的状态机本体。
- 构造方式简述：`Stateflow chart -> CPS denotational semantics -> hierarchical state machine / Lustre automaton -> CoCoSim safety verification`。
- 基础设施与场景简述：依托 `Simulink/Stateflow`、`OCaml` 语义实现、`Lustre` 与 `CoCoSim`，适合嵌入式和 CPS 控制逻辑的自动安全验证与代码生成。

```text
Stateflow chart -> CPS semantics -> interpreter / Lustre automaton -> Horn clauses / CoCoSim verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Stateflow` chart、层次状态、junction、内部/外部 transition、事件、守卫和动作。
2. Hamon 风格 denotational semantics 及其 CPS 化。
3. 由语义函数实例化出的解释器、命令式代码生成器和 `Lustre automaton` 代码生成器。
4. `CoCoSim` 侧的 safety property modeling、代码生成、验证和失败性质图形调试。

### 核心抽象

论文的核心编译对象可保守整理为：

$$
\mathcal{C}_{sf} : SF \to LA
$$

上式中的符号逐项解释如下：

1. `$SF$` 是输入的 `Stateflow` chart 集合。
2. `$LA$` 是输出的 `Lustre automaton` 表示。
3. `$\mathcal{C}_{sf}$` 表示论文中基于 CPS denotational semantics 的编译过程。
4. 这个函数不是手写模板映射，而是由语义函数实例化得到的代码生成路线。

论文借用 CPS 的基本思想，把“后续怎么执行”显式作为参数传递。代表性规则可写成：

$$
\llbracket e_0 e_1 \rrbracket \kappa = \llbracket e_0 \rrbracket(\lambda v_0.\llbracket e_1 \rrbracket(\lambda v_1.v_0 v_1 \kappa))
$$

上式中的符号逐项解释如下：

1. `$e_0 e_1$` 是函数应用形式的表达式。
2. `$\llbracket \cdot \rrbracket$` 是语义解释函数。
3. `$\kappa$` 是 continuation，表示当前表达式求值完成后应继续执行的后续计算。
4. `$v_0$` 和 `$v_1$` 是分别由 `$e_0$` 和 `$e_1$` 求得的中间值。

对 `Stateflow` transition，论文中的结构可保守写成：

$$
t = (e_t, c, (a_c, a_t), d)
$$

上式中的符号逐项解释如下：

1. `$e_t$` 是触发事件。
2. `$c$` 是 guard 条件。
3. `$a_c$` 是 condition action，即守卫成立后立即执行的动作。
4. `$a_t$` 是 transition action，即真正完成转移后执行的动作。
5. `$d$` 是目标，可以是状态，也可以是 junction。

CPS 化 transition 语义的直觉可压成：

$$
\llbracket t \rrbracket(\theta,w,s,f,g) = \mathrm{Ite}(\mathrm{event}(e_t)\land c,\ a_c;\llbracket d \rrbracket_{\theta}(w,s\circ a_t,f,g),\ f)
$$

上式中的符号逐项解释如下：

1. `$\theta$` 是 junction 或 transition-list 的语义环境。
2. `$w$` 是 wrapper continuation，用于进入或包裹目标结构。
3. `$s$` 是 success continuation。
4. `$f$` 和 `$g$` 分别表示局部失败与全局失败 continuation。
5. `$\mathrm{Ite}$` 表示条件分支。
6. `$s\circ a_t$` 表示成功 continuation 前还要执行 transition action。

### 一个最小例子与通俗解释

论文继续使用 `Stateflow` 秒表例子：

1. 顶层有 `Run` 和 `Stop` 两个模式。
2. 内部包含 `Reset`、`Lap_stop`、`Running`、`Lap` 等子状态。
3. `START` 和 `LAP` 是用户事件，`TIC` 驱动计时变量 `cent/sec/min` 更新。
4. 若事件和守卫匹配，transition 会执行 condition action、junction 选择和 transition action，并最终进入目标状态。

通俗地说，这条路线像给 `Stateflow` chart 装了一个“语义编译器”。它不只是把图画成另一张图，而是把每个事件、守卫、junction 和层次状态都解释成可组合的 continuation，再把这些 continuation 实例化成可执行代码或可验证模型。

### 运行 / 接受 / 转移语义

论文的自动分析链可写成：

$$
SF \xrightarrow{\mathrm{CPS}} HSM \xrightarrow{\mathrm{codegen}} LA \xrightarrow{\mathrm{CoCoSim}} \mathrm{Safe?}
$$

上式中的符号逐项解释如下：

1. `$SF$` 是 `Stateflow` 输入模型。
2. `$HSM$` 是保留结构和 modal behavior 的 hierarchical state machine 语义层。
3. `$LA$` 是 `Lustre automaton`。
4. `$\mathrm{Safe?}$` 表示 `CoCoSim` 对 safety property 的验证结果。

论文强调该编译保持 `Stateflow` 的层次结构和 modal behavior，因此验证对象不只是拍平后的普通图，而是由语义驱动生成的中间表示。

### 语义边界

1. 论文服务的是 `Stateflow` 自动安全验证，不是完整 `Simulink` 连续模型语义。
2. 它依赖 Hamon 的 `Stateflow` 语义基础，仍需面对 MathWorks 工具行为没有官方完整形式语义的问题。
3. `Lustre` 与 `Horn clauses` 后端很适合 safety verification，但不等于覆盖所有 `Stateflow` 特性。
4. 文中实验基于 `CoCoSim v0.1`、`Matlab 2016a` 与 `Stateflow 8.7`，工具版本边界需要保留。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 编译目标 | `$\mathcal{C}_{sf}: SF \to LA$` | 从 `Stateflow` chart 生成 `Lustre automaton`。 |
| CPS 语义 | `$\llbracket e_0 e_1 \rrbracket \kappa$` | 把控制流、求值顺序和代码生成后续显式参数化。 |
| 转移对象 | `$t=(e_t,c,(a_c,a_t),d)$` | 事件、守卫、动作和目标共同决定一次 `Stateflow` 转移。 |
| 验证链 | `$SF \to HSM \to LA \to \mathrm{Safe?}$` | 语义编译后接 `CoCoSim` safety verification。 |
| 实验边界 | `77` 个 `Stateflow` 模型 | 论文用工业规模 benchmark 验证编译和验证路线的可行性。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 论文保留 `Stateflow` 的层次状态和 modal behavior。 |
| 事件 / 触发 | 很强 | `START/LAP/TIC` 这类事件直接进入 transition semantics。 |
| 守卫 / 数据 | 很强 | condition action、transition action 和计时变量更新都是核心对象。 |
| 层次 | 很强 | 论文明确把结构保持作为贡献之一。 |
| 并发 / 同步 | 部分支持 | `Stateflow` 的 parallel arrangement 属于语义对象，但本文主线更偏编译与安全验证。 |
| 时间约束 | 间接支持 | `TIC` 等事件可表达离散时间推进；显式 clock automata 不是本文本体。 |
| 连续动态 / 随机性 | 不支持随机性，连续动态依赖外部 `Simulink` | 本文处理 `Stateflow` 控制逻辑，不处理连续 ODE 语义。 |
| 可执行 / 可验证性 | 很强 | `OCaml` 实现、`Lustre` 生成、`CoCoSim` 验证和 Horn clause 后端构成完整路线。 |

### 形式化问题与性质

1. 这篇论文真正补的是“从 `Stateflow` 到可验证后端”的语义编译方法。
2. `CPS` 的作用是把 `Stateflow` 中复杂的控制后续、junction 和动作顺序变成统一代码生成接口。
3. 对 `project_1` 来说，它说明 LLM 生成 `Stateflow` 不能只生成图形节点，还要生成适合后端验证的事件、守卫和动作结构。

## 构造方式与承载格式

### 建模入口

建模入口是 `MathWorks Simulink/Stateflow` 中的 chart，包含层次状态、junction、事件、guard、动作和输入输出信号。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Stateflow` chart。
2. `OCaml` 中实现的 CPS denotational semantics。
3. 解释器或命令式代码生成器。
4. `Lustre automaton`。
5. `CoCoSim` 侧的 Horn clause 验证工件。

### 交换与互操作

论文的互操作重点在于把 `Stateflow` 接入 `CoCoSim / Lustre / Horn clauses`。它没有提出开放交换标准，而是把工业图形载体和形式验证后端桥接起来。

## 配套基础设施

- 建模/编辑工具：`Matlab/Simulink/Stateflow`。
- 解析/交换/元模型支持：论文侧重点是语义编译与代码生成，未提出独立 `XML/JSON` 交换格式。
- 仿真/执行支持：`OCaml` 解释器和 `Stateflow` 原始仿真环境。
- 验证/分析支持：`CoCoSim`、`Lustre automaton`、Horn clauses 与 safety property checking。
- 代码生成/转换支持：`Stateflow -> imperative code` 和 `Stateflow -> Lustre automaton`。
- 标准化或社区生态：依附 `Simulink/Stateflow` 工业生态与开源 `CoCoSim` 分析框架。

## 适用场景与需求前提

### 适用场景

适合已经使用 `Stateflow` 建模嵌入式控制器、汽车/航电/CPS 控制逻辑，并希望自动做 safety verification 或生成验证后端模型的场景。

### 需求前提

1. 需求已经可以落成 `Stateflow` 的状态、事件、guard 和动作。
2. 控制逻辑需处在论文支持的 `Stateflow` 子集或 `CoCoSim` 可处理范围内。
3. 验证目标主要是 safety properties。
4. 团队接受 `Lustre / Horn clauses` 作为验证中间层。

### 不适用或高成本场景

如果需求核心是连续动力学、概率行为、开放式分布式协议，或强依赖完整 `Stateflow` 工具私有语义，本文路线需要额外抽象和核对。

## 与相邻形式主义的关系

相对 [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)，那篇重点是澄清 `Stateflow` 操作语义，本文把语义进一步变成自动编译与验证路线；相对 [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)，`C2E2` 更偏 `Stateflow` hybrid verification 工具，本文更偏 `CPS semantics -> Lustre / CoCoSim`；相对 [an-educational-toolbox-on-supervisory-control-theory-using-matlab-simulink-stateflow/desc.md](../an-educational-toolbox-on-supervisory-control-theory-using-matlab-simulink-stateflow/desc.md)，后者把 `Stateflow` 当 supervisory-control 教学/工程入口，本文把它当自动安全验证前端。

## 与本研究的关系

### 对 Project 1 的价值

1. 它给 `Stateflow` 这条工业状态机载体补了“生成后怎么验证”的工程链路。
2. `CPS` 化语义对 LLM 生成尤其有启发，因为它要求显式化后续、动作顺序和目标结构。
3. `Stateflow -> Lustre -> Horn clauses` 是一个可复用的“需求到可验证模型”候选中间路线。

### 作为目标形式主义还是中间表示

它更适合作为 `Stateflow` 目标形式主义的验证后端路线，而不是新的最终建模语言。

### 对需求到模型生成的启发

1. 生成 `Stateflow` 模型时，必须让事件、guard、junction 和动作顺序可被语义编译器消化。
2. 如果验证后端是 `CoCoSim`，需求里的 safety property 应该同步结构化，而不能只生成 chart。
3. 对复杂层次控制，保留 hierarchy 可能比直接 flatten 更利于解释和修复。

### 现实限制

它的可靠性依赖 `Stateflow` 子集、`CoCoSim` 工具链版本和后端性质表达能力；对完整 `Stateflow` 生态仍不能视作一次性解决。

## 重要的相关工作

### 奠基或前身工作

- [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)：`Stateflow` 形式语义母线。
- `Lustre`：本文生成的同步语言后端。

### 同类型或同家族工作

- [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)：`Stateflow` 到混成验证工具路线。
- [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)：`UPPAAL -> Stateflow` 反向实现桥。

### 标准 / 格式 / 工具链工作

- `Matlab/Simulink/Stateflow` 工业建模环境。
- `CoCoSim` 与 `Horn clauses` 验证后端。

### 与本研究关系最紧的工作

- 从自然语言需求生成 `Stateflow` 时，本文提供了检验模型是否能继续进入自动验证链的关键约束。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Stateflow / CPS denotational semantics / CoCoSim Lustre translation`
- 论文角色：`Stateflow` 自动语义编译、安全验证与代码生成路线
- 核心功能：把 `Stateflow` chart 通过 CPS denotational semantics 编译为可验证的 `Lustre automaton` 并接入 `CoCoSim` safety checking。
- 关键特性：`CPS` 语义、层次结构保持、junction / transition action、`OCaml` 解释器、`Lustre` 生成、Horn clause 后端。
- 构造方式：`Stateflow chart -> CPS semantic functions -> interpreter / code generator -> Lustre automaton -> CoCoSim verification`。
- 基础设施：`Simulink/Stateflow`、`OCaml`、`CoCoSim`、`Lustre`、Horn clauses。
- 适用场景：嵌入式与 CPS 控制逻辑的 `Stateflow` 自动安全验证和代码生成。
- 需求前提：需求需能落成支持子集内的 `Stateflow` 事件、guard、动作和 safety property。
- 状态：🟢 直接可用
