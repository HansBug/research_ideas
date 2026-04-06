# Rabinizer 4：从 LTL 到你偏好的确定型自动机 / Rabinizer 4: From LTL to Your Favourite Deterministic Automaton

## 基本信息

- 标题：Rabinizer 4: From LTL to Your Favourite Deterministic Automaton
- 中文标题：Rabinizer 4：从 LTL 到你偏好的确定型自动机
- 作者：Jan Křetínský，Tobias Meggendorfer，Salomon Sickert，Christopher Ziegler
- 发表：*Computer Aided Verification*，`LNCS 10981`，pp. 567-577，2018
- DOI：`10.1007/978-3-319-96145-3_30`
- 链接：https://doi.org/10.1007/978-3-319-96145-3_30
- 形式主义：`LTL / deterministic omega-automata / Rabinizer 4`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：deterministic-automata translation suite / `PRISM` and parity-game bridge for `LTL`
- 工具/实现获取方式：原文明确给出 `http://rabinizer.model.in.tum.de` 作为 `Rabinizer 4` 下载、在线 demo、可视化和使用说明入口；同时给出与 `PRISM` 和 `PG Solver` 对接的实现说明。
- 标准/格式获取方式：原文明确说明输入是 `LTL` 公式，输出是标准 `HOA` 格式自动机；额外还支持把 `DPA` 序列化成 `PG Solver` 所用 parity-game 格式。

## 简报

这篇论文的核心贡献，不是提出新的 `omega` 自动机母型，而是把“从 `LTL` 到哪一类确定型自动机最合适”真正做成一个可选、可比较、可接验证与综合后端的工具套件。`Rabinizer 4` 不再只停在 `LTL -> DGRA/DRA`，而是把 `LTL -> LDGBA / LDBA / DPA / DGRMA` 也纳入统一入口，并同时把结果接到 `PRISM` 概率模型检查和 parity-game 合成链上。

- 形式主义定位：`LTL -> deterministic omega-automata` 的翻译与互操作基础设施，而不是新的自动机理论本体。
- 构造方式简述：以一组命令行工具实现多条 `LTL` 翻译链，并输出 `HOA` 自动机，再把结果送入 `PRISM` 或 parity-game solver。
- 基础设施与场景简述：依托 `HOA`、`PRISM` distribution、`PG Solver` serialization、BDD-based symbolic representation 与多种 translation heuristics，服务概率模型检查与 `LTL` synthesis。

```text
LTL formula -> Rabinizer 4 translator suite -> deterministic omega-automaton in HOA -> PRISM model checking / parity-game synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTL` 公式；
2. deterministic `omega` automata family；
3. `HOA` 交换格式；
4. `PRISM` 概率模型检查桥接；
5. parity-game synthesis bridge。

### 核心抽象

论文可以保守整理成一组统一翻译接口：

$$
\tau : \mathrm{LTL} \to \{\mathrm{DGRA}, \mathrm{DRA}, \mathrm{LDGBA}, \mathrm{LDBA}, \mathrm{DPA}, \mathrm{DGRMA}\}
$$

上式中的符号逐项解释如下：

1. `$\mathrm{LTL}$` 是线性时序逻辑公式集合。
2. 输出族覆盖 generalized Rabin、Rabin、limit-deterministic Büchi、parity 与 frequency-LTL 相关自动机。
3. `Rabinizer 4` 的价值就在于把这些输出类型收进一套统一工具入口。

原文明确给出了对应的命令行工具：

$$
\{\texttt{ltl2dgra}, \texttt{ltl2dra}, \texttt{ltl2ldgba}, \texttt{ltl2ldba}, \texttt{ltl2dpa}, \texttt{fltl2dgrma}\}
$$

上式中的符号逐项解释如下：

1. `ltl2dgra / ltl2dra` 延续早期 `Rabinizer 3` 的核心功能。
2. `ltl2ldgba / ltl2ldba` 提供 limit-deterministic 路线。
3. `ltl2dpa` 支持 `LDBA -> DPA` 或 `DRA -> DPA` 两种模式。
4. `fltl2dgrma` 则把 frequency extension of `LTL` 翻到 `DGRMA`。

对频率扩展，论文使用的核心算子是：

$$
G_{\sim \rho}\varphi
$$

上式中的符号逐项解释如下：

1. `$\sim \in \{\ge, >, \le, <\}$`。
2. `$\rho \in [0,1]$`。
3. 它表示满足 `$\varphi$` 的位置比例满足阈值关系 `$\sim \rho$`。
4. `Rabinizer 4` 给出了该扩展的首个实现级翻译与模型检查入口。

从 automata-theoretic verification 视角，可保守写成：

$$
\mathcal{K} \models \varphi \iff L(\mathcal{K}) \cap L(\tau(\neg \varphi)) = \emptyset
$$

上式中的符号逐项解释如下：

1. `$\mathcal{K}$` 是被验证系统。
2. `$\varphi$` 是目标 `LTL` 公式。
3. `$\tau(\neg\varphi)$` 是对否定公式构造出的确定型自动机。
4. 论文真正补的是如何为不同后端提供“更合适的确定型自动机”，而不是只给一类输出。

### 一个最小例子与通俗解释

可以把 `Rabinizer 4` 的使用方式理解成：

1. 输入一条 `LTL` 公式。
2. 如果目标是概率模型检查，就优先选 `DGRA / DRA / LDBA / DGRMA`。
3. 如果目标是 `LTL` synthesis，就更希望拿到 `DPA` 并转成 parity game。
4. 工具再把结果统一写成 `HOA` 或 parity-game serialization。

通俗地说，`Rabinizer 4` 像“确定型 `omega` 自动机的多路变速箱”。同一条 `LTL` 性质，不同后端真正想吃的自动机并不一样；这篇论文把这种差异正式做成了工具级选择，而不是让用户手工拼接多套 translator。

### 运行 / 接受 / 转移语义

论文的重点不是某一种 automaton 的单独运行语义，而是多条翻译链和它们的后端用途：

1. `DGRA / DRA` 主要服务传统概率模型检查流程。
2. `LDGBA / LDBA` 为更轻量的确定化与概率检查场景提供替代。
3. `DPA` 主要服务 parity-game based synthesis。
4. `DGRMA` 则承接 frequency `LTL` 的 mean-payoff 风格验证。

工程优化方面，论文明确提到：

1. `ltl2dgra / ltl2dra` 采用 master/slave 构造，并对 `G\psi` 子公式做简化、suspension 与按 `SCC` 分离 acceptance。
2. `ltl2ldba` 对 safety / co-safety 子公式做 breakpoint elimination，并允许 non-deterministic initial component。
3. `ltl2dpa` 同时尝试输入公式和其否定的翻译，返回较小者。
4. 实现层面把 transition function 也做成 symbolic 表示，并配合 caching、parallel batch inputs 与局部 acceptance 标注提速。

### 语义边界

这篇论文的边界同样明确：

1. 它是 deterministic `omega`-automata 翻译与后端桥接工具，不是一般控制状态机 DSL。
2. 它面向 `LTL` 及其频率扩展，不处理 timed / hybrid / dataful guards 本体。
3. 它服务 verification / synthesis back-end，而不是需求建模前端。
4. 不同输出 automata family 的优劣仍依赖后端任务，不存在单一绝对最佳类型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 统一翻译接口 | `$\tau : \mathrm{LTL} \to \{\mathrm{DGRA}, \mathrm{DRA}, \mathrm{LDGBA}, \mathrm{LDBA}, \mathrm{DPA}, \mathrm{DGRMA}\}$` | 说明 `Rabinizer 4` 支持多类确定型输出。 |
| 工具族 | `$\{\texttt{ltl2dgra}, \texttt{ltl2dra}, \texttt{ltl2ldgba}, \texttt{ltl2ldba}, \texttt{ltl2dpa}, \texttt{fltl2dgrma}\}$` | 用户面对的是统一工具套件而不是单条翻译。 |
| 频率扩展 | `$G_{\sim \rho}\varphi$` | 论文包含 frequency `LTL` 的首个实现级翻译与验证入口。 |
| 验证规约 | `$\mathcal{K} \models \varphi \iff L(\mathcal{K}) \cap L(\tau(\neg \varphi)) = \emptyset$` | 解释这些 deterministic automata 如何进入模型检查流程。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 deterministic `omega` automata 工作。 |
| 事件 / 触发 | 中等支持 | 核心对象是命题公式与无限词，不是控制事件语言。 |
| 守卫 / 数据 | 弱支持 | 不处理 rich data guards。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 间接支持 | 通过后端模型检查或 synthesis 消费结果，而非直接提供并发建模语言。 |
| 时间约束 | 不支持 | 非 timed family。 |
| 连续动态 / 随机性 | 间接支持 | 通过 `PRISM` distribution 服务概率系统，但不是混成/随机本体建模器。 |
| 可执行 / 可验证性 | 很强 | `HOA` 输出、`PRISM` bridge、parity-game serialization 与在线 demo 都已到位。 |

### 形式化问题与性质

1. `Rabinizer 4` 的关键不是“多一个 translator”，而是把多类确定型自动机收进同一工作流。
2. 它让“给不同后端挑合适 automaton family”从人工拼工具变成统一基础设施问题。
3. 频率 `LTL`、`PRISM` bridge 和 parity-game export 三条链一起出现，使它明显超出单纯论文原型的范围。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `LTL` 文本公式；
2. 命令行翻译器族；
3. `PRISM` distribution；
4. parity-game serialization。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `HOA` 自动机；
2. symbolic transition representation；
3. `PRISM` 模型检查接口；
4. `PG Solver` 所需 parity-game 格式。

### 交换与互操作

互操作是这篇论文的主轴之一：

1. `HOA` 统一了 deterministic automata 的输出交换层。
2. 自带的 `PRISM` 发行版把 `LDBA / DGRMA` 这类结果真正接进概率验证流程。
3. `DPA -> parity games` 的导出则把翻译链延伸到 synthesis。

## 配套基础设施

- 建模/编辑工具：主线是命令行 translator suite、在线 demo 与 automata visualization。
- 解析/交换/元模型支持：`LTL` 输入、`HOA` 输出、`PG Solver` parity-game serialization。
- 仿真/执行支持：不做控制系统仿真，但支持 automata visualization 与 batch translation workflow。
- 验证/分析支持：`PRISM` distribution、frequency `LTL` model checking、parity-game based synthesis bridge。
- 代码生成/转换支持：核心是 `LTL -> deterministic automata` 与 `DPA -> parity games` 转换，而不是嵌入式代码生成。
- 标准化或社区生态：`HOA`、`PRISM`、`PG Solver`、在线 demo 与 `Rabinizer` 系列工具线。

## 适用场景与需求前提

### 适用场景

适合 `LTL` 性质验证、概率模型检查、需要 deterministic `omega` automata 的研究原型，以及基于 parity games 的 `LTL` synthesis 场景。

### 需求前提

1. 需求或性质必须能落成 `LTL` 或其频率扩展。
2. 后端明确需要确定型 `omega` 自动机，而不是一般 `NBA` 即可。
3. 团队需要在不同 automaton family 间做任务导向选择。
4. 若要接概率验证或综合，需要额外接受 `PRISM` 或 parity-game solver 的工作流。

### 不适用或高成本场景

如果问题核心是 timed / hybrid / hierarchical controller modeling，或者性质不是 `LTL` 家族，`Rabinizer 4` 只能充当局部后端而不是主战场。

## 与相邻形式主义的关系

相对 [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md)，`Owl` 更像统一算法底盘，而 `Rabinizer 4` 是构建在类似底盘之上的具体 deterministic-translation 套件；相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，`HOA` 是交换格式本体，而本文是围绕该格式组织的翻译与后端桥接；相对 [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)，`Spot` 更偏通用 `LTL/omega` 操作框架，本文则专注 deterministic outputs 与 `PRISM/synthesis` 连接。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明验证闭环里“把性质翻成哪类自动机”本身就是关键基础设施问题。
2. 若后续要把控制需求里的时序性质落到 automata-theoretic verification，`Rabinizer 4` 这类 translator suite 是直接可复用的后端资产。
3. 它也提醒我们：格式、translator 与后端 model checker / game solver 的衔接程度，决定了形式主义生态的真实成熟度。

### 作为目标形式主义还是中间表示

更适合作为性质验证与综合的后端中间表示工具链，而不是控制系统建模前端。

### 对需求到模型生成的启发

1. 若生成的控制模型最终要接受 `LTL` 性质验证，最好尽早考虑能否接上 `HOA` / deterministic-automata toolchain。
2. “一个 translator 对多个后端”的架构，比为每个验证任务单独造一条临时转换链更稳。
3. 不同后端偏好的 automaton family 不同，这种差异应在工具架构层显式建模。

## 重要的相关工作

1. [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md)：`LTL/omega` 算法与 API 底盘。
2. [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：`Rabinizer 4` 默认输出并交换的 `HOA` 格式。
3. [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)：更通用的 `LTL/omega` 操作工具链。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`LTL / deterministic omega-automata / Rabinizer 4`
- 论文角色：deterministic-automata translation suite / `PRISM` and parity-game bridge for `LTL`
- 归类理由：论文主体是多类确定型 `omega` 自动机的翻译、输出格式与后端桥接基础设施，典型属于工具链与互操作层条目。
