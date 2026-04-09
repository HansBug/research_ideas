# 使用 CodeSurfer/x86 与 WPDS++ 对 x86 可执行文件做模型检查 / Model Checking x86 Executables with CodeSurfer/x86 and WPDS++

## 基本信息

- 标题：Model Checking x86 Executables with CodeSurfer/x86 and WPDS++
- 中文标题：使用 CodeSurfer/x86 与 WPDS++ 对 x86 可执行文件做模型检查
- 作者：G. Balakrishnan，T. Reps，N. Kidd，A. Lal，J. Lim，D. Melski，R. Gruian，S. Yong，C.-H. Chen，T. Teitelbaum
- 发表：*Computer Aided Verification*，pp. 158-163，2005
- DOI：`10.1007/11513988_17`
- 链接：https://doi.org/10.1007/11513988_17
- 形式主义：`Weighted Pushdown Systems / CodeSurfer/x86 / WPDS++ / PathInspector`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：从真实 `x86` 可执行文件恢复 `WPDS` 并自动回答安全查询的程序分析工具链
- 工具/实现获取方式：原文明确给出三件工具构成 `CodeSurfer/x86 + WPDS++ + PathInspector`；其中 `CodeSurfer` 与 `IDA Pro` 是前端恢复基础设施，`WPDS++` 是加权下推求解库，`PathInspector` 是用户侧安全查询器。
- 标准/格式获取方式：核心承载不是中立交换标准，而是由 `CodeSurfer/x86` 恢复出的 `IR`、`WPDS` 规则、query automaton 与 regular-stack query。

## 简报

这篇论文补的是“真实二进制程序如何被收束成可验证的下推后端”这条基础设施路线。它不是再介绍一次 `WPDS` 理论，而是把 `IDA Pro` 反汇编、`CodeSurfer/x86` 的 `IR/VSA` 恢复、`WPDS++` 的 generalized reachability，以及 `PathInspector` 的 automaton-style safety query 串成了一条从可执行文件直达模型检查的工具链。

- 形式主义定位：围绕 `x86 executable -> weighted pushdown system -> safety query` 的程序验证基础设施，而不是新的自动机母型。
- 构造方式简述：`executable -> disassembly / VSA / IR recovery -> PDS/WPDS -> query automaton cross-product -> reachability / witness`。
- 基础设施与场景简述：依托 whole-program IR recovery、call-stack sensitive `WPDS` 求解和可视化 counterexample，服务可执行文件级静态验证、栈安全分析和控制流安全查询。

```text
x86 可执行文件 -> CodeSurfer/x86 IR -> PDS / WPDS -> query automaton -> reachable error? -> witness path
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `CodeSurfer/x86` 恢复的控制流图、调用图与系统依赖图。
2. `Pushdown System (PDS)`，用于编码过程间控制流。
3. `Weighted Pushdown System (WPDS)`，用于支持数据流和 stack-qualified 查询。
4. `PathInspector` 的 query automaton。
5. witness path 与 stack-aware dataflow queries。

### 核心抽象

控制流后端首先被压成标准下推系统：

$$
\mathcal{P} = (P, \Gamma, \Delta)
$$

上式中的符号逐项解释如下：

1. `$P$` 是控制位置集合；原文这里通常只需要单一 `PDS` 控制状态。
2. `$\Gamma$` 是栈字母表，在该编码里对应程序位置与返回点。
3. `$\Delta$` 是下推规则集合，负责编码过程内边、调用边与返回边。

在此基础上再加上权值域，可得：

$$
\mathcal{W} = (\mathcal{P}, S, f)
$$

上式中的符号逐项解释如下：

1. `$\mathcal{P}$` 是上面的底层 `PDS`。
2. `$S$` 是用户定义的 semiring 或权值域。
3. `$f$` 把每条下推规则映成某个抽象变换或代价。

论文对过程间控制流给出的三类规则可保守整理为：

$$
\langle p,\ell \rangle \to \langle p,\ell' \rangle, \qquad \langle p,\ell_{call} \rangle \to \langle p,\ell_{entry}\,\ell_{ret} \rangle, \qquad \langle p,\ell_{exit} \rangle \to \langle p,\epsilon \rangle
$$

上式中的符号逐项解释如下：

1. 第一类规则表示过程内 `CFG` 边。
2. 第二类规则表示调用，把被调入口与返回点压入栈形态。
3. 第三类规则表示过程返回，弹出一层调用上下文。
4. `$\ell$`、`$\ell'$`、`$\ell_{call}$`、`$\ell_{entry}$`、`$\ell_{ret}$`、`$\ell_{exit}$` 都是程序位置。

对安全查询，`PathInspector` 把禁止模式写成有限自动机，再与程序模型做积。可保守写成：

$$
ErrReachable \iff Reach\big((\mathcal{W} \otimes A_q), C_{err}\big) \neq \emptyset
$$

上式中的符号逐项解释如下：

1. `$A_q$` 是 query automaton，用来编码禁止位置序列。
2. `$\mathcal{W} \otimes A_q$` 是程序 `WPDS` 与查询自动机的乘积。
3. `$C_{err}$` 是错误配置集合。
4. 若可达，则工具能返回 witness path。

### 一个最小例子与通俗解释

一个最小直觉例子可以是：

1. 当前执行到函数 `main` 中的位置 `\ell_1`。
2. 在 `\ell_1` 调用 `foo`，于是栈里压入返回点 `\ell_{ret}`。
3. `foo` 内部若到达某个危险位置 `\ell_{bug}`，而 query automaton 正在追踪“某前序条件已经发生”，就会进入错误状态。
4. `WPDS++` 回答的不是“某一层函数里有没有 bug”，而是“带调用栈上下文时，这个错误配置是否可达”。

通俗地说，这套工具链像“把真实二进制的调用栈语义装进模型检查器里”。它不是只看源码表面结构，而是直接对最终可执行文件的控制流和栈行为做形式化分析。

### 运行 / 接受 / 转移语义

对 `PathInspector` 这类安全查询，核心语义是错误配置可达性。可保守写成：

$$
Post^\ast(C_0) \cap C_{err} \neq \emptyset
$$

上式中的符号逐项解释如下：

1. `$C_0$` 是初始配置集。
2. `$Post^\ast$` 表示下推系统在任意有限步后的后继闭包。
3. `$C_{err}$` 是 query automaton 已到错误状态的乘积配置集合。
4. 非空就表示存在反例执行。

若使用权值，则序列规则上的 `extend` 给出路径级抽象变换，不同路径再用 `combine` 汇总；因此这条工具链既能做只关心控制配置的 safety query，也能支持带上下文的数据流问题。

### 语义边界

1. `PathInspector` 当时主打的是 possible control configurations，而不是完整数据状态验证。
2. 数据流分析虽可借 `WPDS++` 扩展，但若权值抽象过粗，返回的 counterexample 可能不可执行。
3. 前端依赖“标准编译模型”假设；若可执行文件破坏常规栈 discipline，恢复出的 `IR` 可能不可靠。
4. 这是程序二进制验证路线，不是高层状态图 DSL。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PDS` 骨架 | `$\mathcal{P}=(P,\Gamma,\Delta)$` | 用调用栈精确表示过程间控制流。 |
| `WPDS` 骨架 | `$\mathcal{W}=(\mathcal{P},S,f)$` | 在 `PDS` 上加权以支持数据流与更丰富查询。 |
| 调用编码 | `$\langle p,\ell_{call}\rangle \to \langle p,\ell_{entry}\,\ell_{ret}\rangle$` | 调用点与返回点被显式写入栈语义。 |
| 安全查询乘积 | `$\mathcal{W}\otimes A_q$` | forbidden-pattern 自动机与程序控制流联立。 |
| 错误可达性 | `$Post^\ast(C_0)\cap C_{err}\neq\emptyset$` | witness path 与反例显示的直接依据。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 控制位置与调用栈共同定义程序状态。 |
| 事件 / 触发 | 中等支持 | 主对象是程序位置序列，不是外部反应式事件接口。 |
| 守卫 / 数据 | 中等支持 | `WPDS++` 可承载数据流权值，但 PathInspector 主线仍偏控制配置。 |
| 层次 | 很强 | 过程调用天然形成栈式层次。 |
| 并发 / 同步 | 不支持 | 面向顺序过程间控制流。 |
| 时间约束 | 不支持 | 不涉及 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 纯离散程序分析。 |
| 可执行 / 可验证性 | 很强 | 可从真实可执行文件直接恢复模型并产生 witness。 |

### 形式化问题与性质

1. 这篇论文真正补出的，不是新的下推理论，而是“从机器级程序到 `WPDS` 后端”的工程桥梁。
2. whole-program analysis 和无调试信息恢复是其工程价值的重要部分，因为它避免了只看源码 `IR` 的失真。
3. query automaton 的使用说明这条路线天然适合把模式化安全需求编成自动机监视器。

## 构造方式与承载格式

### 建模入口

主要入口包括：

1. `x86` 可执行文件本身。
2. `IDA Pro` 反汇编结果。
3. `CodeSurfer/x86` 恢复出的 `CFG/call graph/SDG`。
4. 用户定义的 query automaton 或 stack-qualified dataflow query。

### 机器可处理承载方式

机器可处理承载方式包括：

1. recovered `IRs`。
2. `PDS/WPDS` 规则集。
3. regular-language 风格的调用字符串或配置集合。
4. query automaton 与 witness path。

### 交换与互操作

1. 它不是 XML/JSON 一类交换标准，而是把低层程序恢复到统一 `WPDS` 后端。
2. 上游可接不同可执行文件，前提是前端恢复器可工作。
3. 下游可接 generalized reachability、安全查询与更丰富的数据流求值。

## 配套基础设施

- 建模/编辑工具：`IDA Pro` 提供反汇编与初始结构恢复，`CodeSurfer/x86` 进一步重建 `IR`。
- 解析/交换/元模型支持：`CFG`、call graph、system dependence graph、a-locs 与 `VSA` 恢复。
- 仿真/执行支持：主线不在执行器，而在静态模型恢复与 reachability 求解。
- 验证/分析支持：`WPDS++` generalized reachability、illegal stack manipulation check、stack-qualified dataflow query、PathInspector safety queries。
- 代码生成/转换支持：可执行文件到 `IR/PDS/WPDS` 的自动转换是核心。
- 标准化或社区生态：原文未给中立标准；其生态价值主要来自 `WPDS` 程序分析与 `CodeSurfer` 工具族。

## 适用场景与需求前提

### 适用场景

适合二进制静态验证、过程间控制流安全查询、调用栈敏感程序分析，以及必须直接分析最终可执行文件而不是源码中间表示的场景。

### 需求前提

1. 可执行文件需要基本符合常规编译模型与栈 discipline。
2. 目标需求最好能写成 forbidden control pattern、可达性或可组合的数据流权值问题。
3. 调用栈语义是关键，否则用 `WPDS` 建模收益会下降。
4. 团队能接受保守近似与潜在不可执行反例的后处理。

### 不适用或高成本场景

1. 对高度自修改代码、强混淆样本或非标准运行时，前端恢复可能不稳。
2. 若需求核心是 rich numeric semantics 或并发共享内存语义，这篇论文的主工具链并不直接覆盖。
3. 若只需源码级局部检查，引入完整 `CodeSurfer/x86 + WPDS++` 代价可能偏高。

## 与相邻形式主义的关系

相对 [weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md](../weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md)，这篇论文不是抽象的 `WPDS` 方法母线，而是把它落到真实 `x86` 可执行文件验证；相对 [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)，`PDAAAL` 更像通用 reachability library，而这里更强调 executable recovery 与安全查询工作流；相对 [pumoc-a-ctl-model-checker-for-sequential-programs/desc.md](../pumoc-a-ctl-model-checker-for-sequential-programs/desc.md)，`PuMoC` 走的是 `CTL` 程序模型检查，而这里更偏 automaton-style safety query 与数据流扩展。

## 与本研究的关系

### 对 Project 1 的价值

它对 `project_1` 的直接启发是：即便目标系统不是先天以状态机形式给出，也可以通过自动恢复把真实软件行为压成可验证的栈式状态模型。这有三点价值：

1. 为 LLM 生成后的软件控制逻辑提供“可回落到何种后端验证模型”的参考。
2. 说明控制状态与调用栈可以组成一种比普通 `FSM` 更忠实的软件行为模型。
3. 说明 query automaton 这类外部性质监视器很适合与结构化模型自动配对。

### 可借鉴点

1. 把非形式化或源码级描述先转成结构化 `IR`，再转成状态机后端，这是一条可复用的两阶段建模路线。
2. `forbidden pattern -> query automaton` 的思路，适合后续性质生成与验证场景自动化。
3. 对控制逻辑而言，“程序位置 + 调用栈”本身就是一种状态机抽象，而不必强行压回扁平 `FSM`。

### 局限与注意事项

1. 该路线偏程序分析，不直接服务工业控制 DSL 或图形状态图。
2. 数据面并非 PathInspector 当前主轴，若研究对象强调变量精确语义，还需更强权值与约束系统。
3. 对 LLM 驱动建模而言，它更适合作为后端落脚点，而不是前端交互式建模语法。

## 重要的相关工作

1. [weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md](../weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md)：给出 `WPDS` 在过程间分析中的方法母线。
2. [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)：补 weighted pushdown library 侧的后续工程基础设施。
3. [pumoc-a-ctl-model-checker-for-sequential-programs/desc.md](../pumoc-a-ctl-model-checker-for-sequential-programs/desc.md)：展示顺序程序模型检查的另一条 pushdown 验证分支。

## 文献分类总结

- 这是一篇 `📦 标准、交换格式、元模型与执行载体` 条目，因为它补的是从真实程序到下推后端的可复用工具链。
- 这是一篇 `🏗️ 标准/基础设施` 条目，而不是单纯 `🛠️ 方法路线`，因为重点在 `CodeSurfer/x86 + WPDS++ + PathInspector` 三件套的长期基础设施拼装。
- 它描述的核心对象是 `🎛️ 控制 / 反应式逻辑`，因为被分析对象是程序可能到达的控制配置及其调用栈上下文。
- 它应挂在 `weighted-pushdown verification backends` 的静态基础设施口径下，并补强 `CodeSurfer/x86 / WPDS++ / PathInspector` 这一支 executable-level 工程入口。
