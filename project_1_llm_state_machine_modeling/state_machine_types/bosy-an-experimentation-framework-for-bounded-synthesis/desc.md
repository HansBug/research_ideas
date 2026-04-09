# BoSy：有界综合实验框架 / BoSy: An Experimentation Framework for Bounded Synthesis

## 基本信息

- 标题：BoSy: An Experimentation Framework for Bounded Synthesis
- 中文标题：BoSy：有界综合实验框架
- 作者：Peter Faymonville，Bernd Finkbeiner，Leander Tentrup
- 发表：*Computer Aided Verification*，pp. 325-332，2017
- DOI：`10.1007/978-3-319-63390-9_17`
- 链接：https://doi.org/10.1007/978-3-319-63390-9_17
- 形式主义：`bounded synthesis / LTL reactive synthesis / BoSy`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：multi-backend bounded-synthesis framework spanning SAT/QBF/DQBF/EPR/SMT encodings
- 工具/实现获取方式：原文脚注明确给出 `BoSy` 入口 `https://react.uni-saarland.de/tools/bosy/`。
- 标准/格式获取方式：输入采用 JSON-based problem description，包含 `LTL` 公式、输入输出原子命题划分和 `Mealy/Moore` 目标语义；输出支持 `AIGER`、`SMV`、`DOT`。

## 简报

`BoSy` 补的是 reactive synthesis 里非常工程化的一条线：不是重新发明一套自动机理论，而是把 bounded synthesis 做成一个“可试不同编码、不同 solver、不同搜索策略”的实验框架。它把同一个 `LTL` 综合问题分别编码到 `SAT / QBF / DQBF / EPR / SMT`，再比较不同逻辑层与 solver 层的表现，因此既是综合器，也是一个 encodings-vs-solvers 的评测平台。

- 形式主义定位：围绕 `LTL` bounded synthesis 的方法路线与实验框架，而不是新的状态机本体。
- 构造方式简述：`LTL + I/O partition + Mealy/Moore semantics -> universal co-Büchi automaton -> bound-k constraint encoding -> SAT/QBF/DQBF/EPR/SMT solver -> implementation extraction`
- 基础设施与场景简述：依托 JSON 输入、`ltl3ba/spot`、多类 solver、bound search 与多格式输出，服务 reactive controller synthesis、solver comparison 与 `SYNTCOMP` 风格竞赛/benchmark。

```text
LTL specification -> universal co-Buchi automaton -> bound-k encoding -> solver witness -> Mealy/Moore implementation -> AIGER/SMV/DOT
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTL` reactive synthesis；
2. bounded synthesis；
3. universal co-Büchi automaton preprocessing；
4. 多种逻辑编码后端；
5. `Mealy/Moore` 实现抽取与多格式输出。

### 核心抽象

对 `BoSy` 而言，综合目标仍然是一个有限状态控制器。可保守整理为：

$$
M = (S, s_0, \Sigma_I, \Sigma_O, \delta, \lambda)
$$

上式中的符号逐项解释如下：

1. `$S$` 是控制器状态集合。
2. `$s_0$` 是初始状态。
3. `$\Sigma_I$` 和 `$\Sigma_O$` 分别是环境输入与系统输出字母表。
4. `$\delta$` 是状态更新函数。
5. `$\lambda$` 是输出函数；在 `Mealy` 与 `Moore` 语义下其绑定位置不同。

bounded synthesis 的核心问题可压成：

$$
\exists M,\ |S| \le k,\ M \models \varphi
$$

上式中的符号逐项解释如下：

1. `$\varphi$` 是输入的 `LTL` 规格。
2. `$k$` 是当前轮次假设的状态上界。
3. 若存在不超过 `$k$` 个状态的实现 `$M$` 满足规格，则当前 bound 可行。
4. 若不可行，框架就提高 `$k$` 后重新编码。

论文实际流程还要先把公式下沉为 automaton，再转成约束：

$$
\varphi \Rightarrow A^{ucb}_\varphi \Rightarrow C_k(\varphi) \Rightarrow \text{solver witness} \Rightarrow M
$$

上式中的符号逐项解释如下：

1. `$A^{ucb}_\varphi$` 是与规格等价的 universal co-Büchi automaton。
2. `$C_k(\varphi)$` 是在给定状态界 `$k$` 下得到的约束系统。
3. `solver witness` 是 SAT/QBF 等求解器返回的 satisfying assignment 或 certificate。
4. 最终再从 witness 中抽取实现。

### 一个最小例子与通俗解释

一个最小例子可以是请求-授权控制器：

1. 输入命题 `req` 表示环境提出请求。
2. 输出命题 `grant` 表示系统发出授权。
3. 规格要求“请求若反复出现，则授权必须反复响应，且授权行为满足额外安全约束”。
4. `BoSy` 会先尝试找 1-state controller；若无解，就试 2-state、3-state，直到某个 `k` 出现可行解。

通俗地说，`BoSy` 像一个“带尺子的综合器”。它不是一上来就找任意大控制器，而是不断问：`1` 个状态够不够？`2` 个够不够？同时还允许你比较“这道题让 SAT 解更划算，还是让 QBF 解更划算”。

### 运行 / 接受 / 转移语义

论文明确把 `BoSy` 的求解链拆成 preprocessing、encoding、solver、postprocessing 四步。对输入自动机的使用可以保守理解为：

$$
L(M) \subseteq L(\varphi)
$$

上式中的符号逐项解释如下：

1. `$L(M)$` 表示控制器在所有环境输入下诱导出的行为集合。
2. `$L(\varphi)$` 表示满足规格的行为集合。
3. bounded synthesis 用约束方式保证控制器所有可能行为都不违反 `LTL` 规格。

对 `QBF` 路线，论文还强调其 witness-extraction 分两步完成：先解带顶层存在量词的查询，再调用 certifying solver 产生 Boolean functions 形式的见证。也就是说，`BoSy` 的“运行语义”不仅是有无解判断，还包括把解重新编码成 transition/output circuits 的过程。

### 语义边界

1. `BoSy` 解决的是有限离散 `LTL` reactive synthesis，不处理连续动力学与显式时钟。
2. bounded synthesis 追求的是“小状态数实现”的增量构造，不是 richer payoff game 的最优控制。
3. 工具高度依赖 automata translation 和 solver 生态；编码优劣会显著影响效果。
4. 论文提供的是实验框架和方法路线，不是前端建模 DSL。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 实现骨架 | `$M = (S, s_0, \Sigma_I, \Sigma_O, \delta, \lambda)$` | `BoSy` 最终要抽取的控制器对象。 |
| bounded synthesis 查询 | `$\exists M,\ |S| \le k,\ M \models \varphi$` | 逐步增大 bound 的核心。 |
| automaton-to-constraint 链 | `$\varphi \Rightarrow A^{ucb}_\varphi \Rightarrow C_k(\varphi)$` | 说明为什么它能统一比较多类 solver 编码。 |
| 语言满足关系 | `$L(M) \subseteq L(\varphi)$` | bounded synthesis 保证实现不违反 `LTL` 规格的语义直觉。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 输出就是有限状态 `Mealy/Moore` 控制器。 |
| 事件 / 触发 | 很强 | 输入/输出原子命题分区是问题定义核心。 |
| 守卫 / 数据 | 弱支持 | 主体是 Boolean reactive synthesis，不是 rich data guards。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 通过环境/系统轮换交互建模，但不是组件代数。 |
| 时间约束 | 不支持 | 不属于 timed synthesis。 |
| 连续动态 / 随机性 | 不支持 | 不处理 hybrid / stochastic plant。 |
| 可执行 / 可验证性 | 很强 | 输出可为 circuits、`SMV` 或 `DOT`，且可再接 standard hardware model checkers。 |

### 形式化问题与性质

1. `BoSy` 的代表性在于把不同逻辑层编码统一到一个 bounded-synthesis 框架里。
2. 论文清楚展示了“编码更紧凑”与“solver 实际更强”并不总是同一回事。
3. 因此，它既是综合器，也是 reactive synthesis 实验方法学基础设施。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. JSON-based problem description；
2. `LTL` 规格；
3. 输入/输出原子命题划分；
4. `Mealy` 或 `Moore` 目标语义；
5. bound search strategy。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `ltl3ba/spot` 输出的 automaton；
2. SAT/QBF/DQBF/EPR/SMT constraint systems；
3. assignment / certificate-based implementation representation；
4. `AIGER / SMV / DOT` 输出。

### 交换与互操作

1. 输入层支持 `LTL` 与分区签名；预处理层兼容 `ltl3ba`、`spot`、`SPIN never-claims`、`HOA`。
2. 输出层支持 `AIGER`、`SMV`、`DOT`，可继续接验证器或可视化工具。
3. 求解层通过统一框架接入多类 solver，便于实验比较。

## 配套基础设施

- 建模/编辑工具：主体是命令行实验框架与 JSON 输入，不是图形前端。
- 解析/交换/元模型支持：automata preprocessing、JSON input、`HOA/SPIN never-claims` compatibility、multi-format outputs。
- 仿真/执行支持：不主打交互仿真，但输出实现可进入标准硬件 model checkers。
- 验证/分析支持：bound search、encoding comparison、solver benchmarking、realizability / synthesis。
- 代码生成/转换支持：从 solver witness 生成 circuit-like implementation，并导出 `AIGER`/`SMV`/`DOT`。
- 标准化或社区生态：`BoSy` website、`ltl3ba`、`spot`、PicoSAT、CryptoMiniSat、RAReQS、CAQE、DepQBF、QuAbs、CADET、Z3、CVC4 等共同构成生态。

## 适用场景与需求前提

### 适用场景

适合从 `LTL` 规格综合有限状态控制器、比较不同 solver/encoding 路线，以及为 `SYNTCOMP` 类 benchmark 搭建统一实验底座。

### 需求前提

1. 需求必须可写成 `LTL`。
2. 输入/输出原子命题分区需要清楚给出。
3. 目标实现应是有限状态 `Mealy/Moore` 控制器。
4. 使用者接受“逐步增加状态界”的 bounded search 工作流。

### 不适用或高成本场景

若系统带 dense time、连续动力学、复杂数据域或定量 payoff，`BoSy` 不是自然入口；若规格远超有限布尔接口，也难直接受益。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 更专注 `GR(1)` 片段和插件式综合，而 `BoSy` 面向一般 `LTL` 的 bounded-synthesis 编码比较；相对 [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)，`Acacia+` 走的是 `UCB/K-coBuchi + safety game + antichain` 路线，`BoSy` 则把 automaton 进一步编成逻辑约束交给多种 solver；相对 [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md) 与 [dissecting-ltlsynt/desc.md](../dissecting-ltlsynt/desc.md)，后两者更强调 `DPA/parity-game` 显式求解，`BoSy` 更强调 symbolic/logical encodings 的多后端实验性。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明了从结构化时序需求直接下沉到可执行控制器，在工具上已经有成熟求解后端。
2. 对“生成-验证-修复”闭环而言，`bound`、unsat 结果和 solver witness 都能成为很好的反馈信号。
3. 多编码后端也提示我们：研究中不应把一种 solver 路线误当成唯一真理。

### 作为目标形式主义还是中间表示

更像综合后端与实验框架，不是前端目标语言。

### 对需求到模型生成的启发

1. 若需求已经可稳定转为 `LTL`，可以直接把“状态机建模”推进到“控制器综合”。
2. `Mealy/Moore` 语义区分值得在前端显式保留。
3. solver witness 与多格式导出说明：中间表示、部署表示和验证表示最好分层处理。

### 现实限制

bounded synthesis 虽然工程上实用，但仍受状态界增长和 solver 能力影响；对大型规格，它更像实验平台而不是银弹。

## 重要的相关工作

### 奠基或前身工作

1. bounded synthesis：论文的直接方法学母线。
2. `LTL` reactive synthesis：问题本身可追溯到 Church synthesis。

### 同类型或同家族工作

1. [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)：antichain-based `LTL` synthesis。
2. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：`GR(1)` synthesis framework。
3. [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)：on-the-fly `DPA/parity` synthesis。
4. [dissecting-ltlsynt/desc.md](../dissecting-ltlsynt/desc.md)：基于 `Spot` 的 textbook automata-theoretic synthesis pipeline。

### 标准 / 格式 / 工具链工作

1. `ltl3ba` 与 `spot`：公式到 automaton 的 preprocessing 基础设施。
2. `AIGER`、`SMV`、`DOT`：输出实现和分析结果的主要承载格式。

### 与本研究关系最紧的工作

1. [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)：展示另一条 `LTL` 综合工具主线。
2. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：展示 `GR(1)` 子片段与一般 `LTL` 后端之间的差别。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`bounded synthesis / LTL reactive synthesis / BoSy`
- 论文角色：multi-backend bounded-synthesis framework spanning SAT/QBF/DQBF/EPR/SMT encodings
- 核心功能：在统一框架下比较并运行多种 bounded-synthesis 逻辑编码与 solver 路线
- 关键特性：universal co-Büchi preprocessing、bound search、SAT/QBF/DQBF/EPR/SMT backends、witness extraction、多格式输出
- 构造方式：`LTL + I/O partition -> automaton -> bound-k encoding -> solver witness -> implementation`
- 基础设施：JSON input、`ltl3ba/spot`、多类 solver、`AIGER/SMV/DOT`
- 适用场景：`LTL` 控制器综合、solver benchmarking、bounded-synthesis experiments
- 归类理由：论文主体不是语言本体，而是“如何把 bounded synthesis 工程化为多编码、多 solver、可抽取实现的统一方法路线”。
