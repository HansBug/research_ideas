# 嵌入式系统开发中的整体化方法 / A Holistic Approach in Embedded System Development

## 基本信息

- 标题：A Holistic Approach in Embedded System Development
- 中文标题：嵌入式系统开发中的整体化方法
- 作者：Bojan Nokovic，Emil Sekerinski
- 发表：*Electronic Proceedings in Theoretical Computer Science*，Vol. 187，pp. 72-85，2015
- DOI：`10.4204/EPTCS.187.6`
- 链接：https://doi.org/10.4204/EPTCS.187.6
- 形式主义：`pCharts / pState / probabilistic timed hierarchical state machines`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`pCharts` 建模、分析、文档和代码生成一体化 workflow
- 工具/实现获取方式：原文明确给出 `pState` 下载入口 `http://pstate.mcmaster.ca`，并说明它可把 `pCharts` 翻译到 `PRISM` 模型并生成 `C` 代码。
- 标准/格式获取方式：承载方式是 `pCharts` 图形层次状态机、附着在状态上的 queries / invariants / rewards、翻译出的 probabilistic guarded commands 与 `PRISM` `MDP` 模型；不是独立行业标准。

## 简报

这篇论文的核心不是单纯“又一个 statechart 变体”，而是强调在嵌入式系统开发里，用同一套形式主义贯通建模、性质说明、定量分析、文档和代码生成。`pCharts` 把层次状态机扩展到 probabilistic transitions、timed transitions、stochastic timing 和 cost/reward；`pState` 再把这些模型编译成 `PRISM` 可检查的 guarded commands，并可回到可执行代码。

- 形式主义定位：面向嵌入式系统的概率/时间扩展层次状态机 DSL 与工具链。
- 构造方式简述：用 `pCharts` 画 state hierarchy、并发区、事件和带概率/时间/奖励的 transitions，再把 properties 直接附在状态上，由 `pState` 生成 `PRISM` 模型或 `C` 代码。
- 基础设施与场景简述：依托 `pState`、`PRISM`、probabilistic guarded commands、内嵌文档和 query boxes，服务 resource-aware embedded systems、sensor networks 和概率实时控制分析。

```text
嵌入式需求 -> pCharts 层次状态机 + queries/rewards -> pState -> PRISM / C code -> 定量分析与实现
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. `pCharts`；
2. 层次状态与并发 `AND/XOR` 结构；
3. probabilistic / timed / stochastic transitions；
4. invariants；
5. cost/reward annotations；
6. `PCTL`-style queries；
7. `pState` 到 `PRISM` / `C` 的翻译。

### 核心抽象

论文没有给出单一元组定义，但根据其语言说明可保守整理为：

$$
P = (C, E, T, I, \mathcal R)
$$

上式中的符号逐项解释如下：

1. `$C$` 是层次状态配置结构，含 `AND/XOR` states。
2. `$E$` 是广播事件集合。
3. `$T$` 是转移集合，允许普通、概率、定时和随机时间扩展。
4. `$I$` 是状态不变式集合。
5. `$\mathcal R$` 是状态和 transition 上的 reward/cost 标注。
6. 该式是对论文 `pCharts` 特性的保守整理，不是原文逐字定义。

论文最关键的语义桥接是 probabilistic guarded commands normal form：

$$
b_1 ! S_1 [] \cdots [] b_m ! S_m
$$

其中每个分支内部又是概率选择：

$$
S_i = p_1 : A_1 \oplus \cdots \oplus p_k : A_k
$$

上式中的符号逐项解释如下：

1. `$b_i$` 是布尔 guard。
2. `$S_i$` 是被该 guard 启用的 guarded command。
3. `$p_j$` 是概率，满足同一组概率分支总和为 `1`。
4. `$A_j$` 是相应的赋值语句或更新动作。
5. `[]` 表示 guarded-command 之间的非确定选择。

### 一个最小例子与通俗解释

论文给出的 sender-receiver 例子很适合作为最小说明：

1. `Sender` 初始在 `Sleeping`，`Receiver` 初始在 `Listening`。
2. wake-up 后，sender 以 `0.4` 概率去 `Sending`，以 `0.6` 概率回到 `Sleeping`。
3. `send` 之后，消息以 `0.9` 概率到达 receiver，使其进入 `Off`，以 `0.1` 概率丢失。
4. 在状态和 transition 上还可以挂 `energy`、`tran` 这类 reward。

通俗地说，`pCharts` 像“把普通层次状态图升级成一个能顺手表达概率、时间和代价的嵌入式系统建模板”。你不只是在画模式切换图，还在同一张图上说明“到达这个状态的概率是多少”“多久后触发”“耗了多少能量”“我们要查什么性质”。

### 运行 / 接受 / 转移语义

论文给出的典型 `PRISM` 概率查询是：

$$
P_{\min=?}[F(receiver = Off)]
$$

上式中的符号逐项解释如下：

1. `$P_{\min=?}$` 表示求最小可达概率。
2. `$F$` 是 eventually operator。
3. `$receiver = Off$` 是目标状态谓词。
4. 该公式表示“接收者最终关闭的最小概率是多少”。

reward 查询则写成：

$$
R^{tran}_{\max=?}[F(receiver = Off)]
$$

上式中的符号逐项解释如下：

1. `$R^{tran}_{\max=?}$` 表示对 reward structure `tran` 求最大期望值。
2. `$F(receiver = Off)$` 表示直到 receiver 进入 `Off` 为止的 reachability reward。
3. 该式对应“在 receiver 关闭前，最多期望发送多少次”。

论文还展示了 invariant 会被翻译成 always-condition，例如：

$$
P_{\ge 1}[G((sender = Sleeping) \Rightarrow \neg(receiver = Off))]
$$

上式中的符号逐项解释如下：

1. `$P_{\ge 1}$` 表示概率 `1` 必须满足。
2. `$G$` 是 globally operator。
3. 后面的蕴含式表示 “若 sender 仍在 sleeping，则 receiver 不应处于 off”。

### 语义边界

1. `pCharts` 强调 event-centric semantics 和 broadcast events，不等同于 `UML` 的单接收者事件语义。
2. 其核心验证后端是 `PRISM` 风格的 probabilistic model checking，不是任意 theorem proving。
3. 语言很强调嵌入式系统属性与 rewards，但不是连续混成动力学模型。
4. 代码生成是重要配套，但论文主线仍是统一形式主义和分析工作流。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 语言骨架 | `$P = (C, E, T, I, \mathcal R)$` | `pCharts` 把层次状态、事件、转移、不变式和 reward 统一到同一模型。 |
| guarded commands | `$b_1 ! S_1 [] \cdots [] b_m ! S_m$` | `pState` 用 guarded-command normal form 定义和翻译 `pCharts`。 |
| 概率分支 | `$S_i = p_1 : A_1 \oplus \cdots \oplus p_k : A_k$` | 单个转移内部可带概率更新。 |
| 概率查询 | `$P_{\min=?}[F(receiver = Off)]$` | 典型 reachability probability query。 |
| reward 查询 | `$R^{tran}_{\max=?}[F(receiver = Off)]$` | 典型 expected reward query。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 层次 `AND/XOR` 状态是主骨架。 |
| 事件 / 触发 | 很强 | event-centric semantics，事件可广播到并发状态。 |
| 守卫 / 数据 | 强 | guards、变量 valuation 和 invariants 都是一等对象。 |
| 层次 | 很强 | 继承自 hierarchical state machines。 |
| 并发 / 同步 | 强 | `AND` states 支持并发结构。 |
| 时间约束 | 强 | 有 timed transitions 和 stochastic timing。 |
| 连续动态 / 随机性 | 强 | 支持 probabilistic transitions 与 cost/reward。 |
| 可执行 / 可验证性 | 很强 | `pState` 既能翻译到 `PRISM`，也能生成 `C` 代码。 |

### 形式化问题与性质

1. `pCharts` 把 model design 和 property specification 合在同一层次结构中。
2. event-centric semantics 让它比很多 `UML` 扩展更适合直接翻成 probabilistic guarded commands。
3. reward/invariant/query 都直接挂在状态图上，特别适合嵌入式系统的 tradeoff analysis。

## 构造方式与承载格式

### 建模入口

1. 先建立层次状态图与并发结构。
2. 再标注事件、guards、概率分支和 timed transitions。
3. 如有需要，附加 invariants、query boxes 和 reward annotations。
4. 最后由 `pState` 生成 `PRISM` 模型或 `C` 代码。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `pCharts` 图形模型；
2. 附着在状态上的 queries / invariants / rewards；
3. probabilistic guarded commands；
4. `PRISM` `MDP` 模型与生成的 `C` 代码。

### 交换与互操作

`pCharts` 的互操作路线很清楚：

1. 图形 `pCharts` -> guarded commands；
2. guarded commands -> `PRISM` `MDP`；
3. 没有概率分支的子图可走更高效的 nested control-structure / `C` code generation 路线。

## 配套基础设施

- 建模/编辑工具：`pState`。
- 解析/交换/元模型支持：`pState` 负责把 `pCharts` 翻译到 `PRISM` 所需的 guarded-command / `MDP` 表达。
- 仿真/执行支持：支持从中间控制结构生成 `C` 代码。
- 验证/分析支持：`PRISM` 提供概率和 reward 性质检查。
- 代码生成/转换支持：论文明确说明支持 `C` code generation。
- 标准化或社区生态：研究型工具链，和 `PRISM` 生态紧密耦合，但不是标准组织主导的 interchange format。

## 适用场景与需求前提

### 适用场景

适合概率/时间/资源代价都重要的嵌入式系统、传感器网络、RFID 场景和 resource-aware reactive controllers。

### 需求前提

1. 系统行为可写成层次离散模式切换。
2. 不确定性主要表现为概率或随机时间，而不是连续微分方程。
3. 性质能写成 reachability probability、reward 或 invariant 一类查询。
4. 团队接受图形模型和 `PRISM` 后端分析工作流。

### 不适用或高成本场景

如果系统的核心是连续物理动力学、复杂对象交互语义或大规模通用软件架构，`pCharts` 就不是最自然的第一载体。

## 与相邻形式主义的关系

相对 `UML` statecharts 扩展，`pCharts` 更强调 event-centric semantics 和 direct probabilistic/reward annotations；相对纯 `PRISM` 输入语言，它提供了更高层次、层次化的图形前端；相对 `Probabilistic Timed Automata`，它更像一个可落地的 statechart DSL，而不是扁平 timed automata 母型。

## 与本研究的关系

### 对 Project 1 的价值

1. 它非常适合补“层次状态机 + 时间/概率扩展 + 验证后端”这条宽度。
2. 同一模型中同时容纳结构、性质、reward 和文档的做法，对 LLM 生成高可信模型很有参考意义。
3. 这条路线也与后续 verification profile、property generation 和 iterative repair 都有天然接口。

### 作为目标形式主义还是中间表示

既可作为某些嵌入式概率/时间系统的目标形式主义，也可作为更底层 `PRISM/PTA` 前的高层中间表示。

### 对闭环生成-验证-修复的启发

如果未来要让 LLM 生成“能直接验证和再生成代码”的模型，`pCharts + pState` 这种一体化链路比只输出普通层次状态图更接近工程闭环。

## 重要的相关工作

- `PRISM`
- `Probabilistic Timed Automata`
- `UML Statecharts`
- `pState`

## 文献分类总结

- 形式主义：`pCharts / pState / probabilistic timed hierarchical state machines`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 关键词：`pCharts`、`pState`、概率状态图、reward、`PRISM`
