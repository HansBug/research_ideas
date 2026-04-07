# HASL：从概念到实验的性能评估与模型检查新方法 / HASL: A New Approach for Performance Evaluation and Model Checking from Concepts to Experimentation

## 基本信息

- 标题：HASL: A New Approach for Performance Evaluation and Model Checking from Concepts to Experimentation
- 中文标题：HASL：从概念到实验的性能评估与模型检查新方法
- 作者：Paolo Ballarini，Benoît Barbot，Marie Duflot，Serge Haddad，Nihal Pekergin
- 发表：*Performance Evaluation*，90，2015
- DOI：`10.1016/j.peva.2015.04.003`
- 链接：https://doi.org/10.1016/j.peva.2015.04.003
- 形式主义：`HASL / LHA / DESP / COSMOS`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：统计模型检查语言 + `LHA` 监视器 + `COSMOS` 工具链
- 工具/实现获取方式：原文明确给出 `COSMOS`，并说明其集成在 `CosyVerif` 平台中，支持命令行与图形界面；正文未给出稳定公开仓库 URL。
- 标准/格式获取方式：原文明确给出 `GrML` 作为 `GSPN` 与 `LHA` 的 XML 承载格式；它不是中立行业标准，而是 `COSMOS/CosyVerif` 工作流的机读入口。

## 简报

这篇论文的重要性不在于再发明一种普通 `CSL` 变体，而在于把“路径筛选 + 路径上奖励/统计量收集 + 统计估计”统一成一个可落地的框架。`HASL` 用一个与系统同步的 `LHA` 选择相关路径前缀，同时在线更新数据变量，再用表达式 `Z` 对这些变量的 moment 做统计估计；`COSMOS` 则把这套语言落到了 `GSPN -> C++ code generation -> Monte Carlo / confidence interval` 的执行链路上。

- 形式主义定位：面向 `DESP/GSPN` 的统计模型检查与性能评估方法，而不是新的 plant 状态机母型。
- 构造方式简述：`DESP/GSPN model + synchronised LHA + expression Z -> statistical estimation`。
- 基础设施与场景简述：依托 `COSMOS`、`CosyVerif`、`GrML`、`BOOST` 随机数生成与并行仿真，服务瞬态性能、复杂 reward、条件期望与随机离散事件系统分析。

```text
DESP / GSPN -> LHA monitor selects paths and accumulates variables -> HASL expression Z -> statistical estimation + confidence interval
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `DESP`，即离散事件随机过程；
2. `LHA`，即与 `DESP` 同步的线性混成自动机监视器；
3. `HASL` 公式 `(A, Z)`，其中 `A` 负责路径筛选和变量更新，`Z` 负责统计量定义；
4. `COSMOS`，即把 `GSPN + LHA + Z` 变成可执行统计验证流程的工具。

### 核心抽象

论文先把被分析系统写成：

$$
D = \langle S, \pi_0, E, Ind, enabled, delay, choice, target \rangle
$$

上式中的符号逐项解释如下：

1. `$S$` 是状态集合。
2. `$\pi_0$` 是初始状态分布。
3. `$E$` 是离散事件集合。
4. `$Ind$` 是从状态到实数的 indicator 函数集合。
5. `$enabled(s)$` 给出状态 `$s$` 下可触发的事件集合。
6. `$delay(s,e)$` 给出事件 `$e$` 在状态 `$s$` 下的延迟分布。
7. `$choice(s,E',d)$` 给出同最早延迟事件之间的随机冲突消解。
8. `$target(s,e,d)$` 给出等待 `$d$` 后触发 `$e$` 的目标状态。

监视器 `LHA` 写成：

$$
A = \langle E, L, \Lambda, Init, Final, X, flow, \to \rangle
$$

上式中的符号逐项解释如下：

1. `$E$` 是可与系统同步的事件字母表。
2. `$L$` 是位置集合。
3. `$\Lambda$` 为位置标签函数。
4. `$Init$` 与 `$Final$` 分别是初始和终止位置集合。
5. `$X = (x_1,\dots,x_n)$` 是实值数据变量。
6. `$flow$` 指定每个位置上各变量的线性演化速率。
7. `$\to$` 是带约束和更新的边关系，既允许与系统事件同步，也允许 `#` 自主边。

对变量随时间流逝的演化，论文给出：

$$
\mathrm{Elapse}(s,l,\nu,\delta)(x_k) = \nu(x_k) + flow_k(l)(s)\cdot \delta
$$

上式中的符号逐项解释如下：

1. `$s$` 是 `DESP` 当前状态。
2. `$l$` 是 `LHA` 当前 location。
3. `$\nu$` 是当前数据变量 valuation。
4. `$\delta$` 是流逝时间。
5. `$flow_k(l)(s)$` 是在状态 `$s$`、位置 `$l$` 下第 `$k$` 个变量的演化速率。

为处理自主边，论文还定义最早自主触发时刻：

$$
\mathrm{Autdel}(s,l,\nu) = \min \{\, \delta \mid \exists\, l \xrightarrow{\#, \gamma, U} l',\ s \models \Lambda(l') \land \mathrm{Elapse}(s,l,\nu,\delta) \models \gamma \,\}
$$

上式中的符号逐项解释如下：

1. `$\#$` 表示不依赖系统事件的自主边。
2. `$\gamma$` 是该自主边的左闭约束。
3. `$U$` 是边上的更新。
4. 该式返回第一条可执行自主边的最早触发时间。

### 一个最小例子与通俗解释

论文的共享资源例子很适合说明 `HASL` 的直觉：

1. `GSPN` 描述两类客户竞争同一个资源。
2. `LHA` 在看到某类客户开始服务、结束服务时，同步更新等待时间计数变量。
3. 当累计到 `k` 个样本后，`LHA` 到达 `Final`。
4. 表达式 `Z` 再对最后得到的变量值求均值、上下界或条件期望。

通俗地说，`HASL` 像“带记账能力的路径监视器”。它不是只问“某性质成不成立”，而是先挑出关心的路径，再在这些路径上边跑边记统计账，最后给出概率、均值或 reward 估计。

### 运行 / 接受 / 转移语义

论文把 `DESP` 的核心随机行为写成事件、状态和时间三族随机变量：

$$
\{s_n\}_{n \in \mathbb{N}},\quad \{e_n\}_{n \in \mathbb{N}^\ast},\quad \{\tau_n\}_{n \in \mathbb{N}}
$$

上式中的符号逐项解释如下：

1. `$s_n$` 是第 `$n$` 次事件后系统所处状态。
2. `$e_n$` 是第 `$n$` 次发生的事件。
3. `$\tau_n$` 是第 `$n$` 次事件的发生时间。

最早下一事件时刻由当前 schedule 决定：

$$
\tau_{n+1} = \min \{\, sched_n(e) \mid e \in E \,\}
$$

上式中的符号逐项解释如下：

1. `$sched_n(e)$` 是第 `$n$` 轮时事件 `$e$` 的当前调度时刻。
2. `$\tau_{n+1}$` 因而是所有已调度事件中的最早发生时刻。

同步乘积把系统和监视器压成一个新的 `DESP`：

$$
D' = \langle S', \pi_0', E', Ind', enabled', delay', choice', target' \rangle
$$

上式中的符号逐项解释如下：

1. `$S' = (S \times L \times Val) \cup \{\bot\}$`，即系统状态、监视器位置和变量估值的组合，再加一个失败吸收态。
2. `$E' = E \cup \{\#\}$`，同时包含系统事件和自主边伪事件。
3. `$target'$` 既处理与系统事件同步的迁移，也处理 `#` 自主迁移。

### 语义边界

1. 论文主线是统计模型检查和 reward 分析，不是数值精确求解器。
2. 其强项是复杂瞬态 measure、条件期望和多 reward 联合统计，而不是稳态分析。
3. `HASL` 依赖 `LHA` 对路径进行 almost-sure acceptance/rejection 的监视器式用法。
4. 工具实现以 `GSPN` 为高层输入主线，但语言本身面向更一般的 `DESP`。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `DESP` 骨架 | `$D = \langle S,\pi_0,E,Ind,enabled,delay,choice,target \rangle$` | 给出被分析随机离散事件系统的统一接口。 |
| `LHA` 骨架 | `$A = \langle E,L,\Lambda,Init,Final,X,flow,\to \rangle$` | 给出路径筛选与数据累计监视器。 |
| 时间流逝 | `$\mathrm{Elapse}(s,l,\nu,\delta)$` | 描述数据变量在线性流上的更新。 |
| 自主边触发 | `$\mathrm{Autdel}(s,l,\nu)$` | 定义自主边何时优先触发。 |
| 同步乘积 | `$D'$` | 把 `DESP` 与 `LHA` 组合成新的随机过程。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 通过 `DESP` 状态、`LHA` location 与 valuation 三层联合建模。 |
| 事件 / 触发 | 很强 | 同步事件与自主 `#` 事件并存。 |
| 守卫 / 数据 | 很强 | 线性约束、indicator、线性更新与多变量统计量是核心。 |
| 层次 | 弱支持 | 不是层次状态机语言，层次更多来自上层 `GSPN` 组织。 |
| 并发 / 同步 | 很强 | `GSPN` 天然支持并发与资源竞争，`LHA` 同步监视。 |
| 时间约束 | 很强 | 变量按 rate 演化，自主边按左闭约束最早触发。 |
| 连续动态 / 随机性 | 中到强 | 变量连续流逝是线性的，系统随机性来自 `DESP` 事件延迟与选择。 |
| 可执行 / 可验证性 | 很强 | `COSMOS` 直接支持代码生成、并行仿真和置信区间估计。 |

### 形式化问题与性质

1. `HASL` 把“路径是否被接受”和“路径上统计量如何累计”拆开，分别交给 `LHA` 与 `Z`。
2. `HASL` 明显比只支持成功概率的 `CSL` 类框架更适合 reward-rich performability measure。
3. `COSMOS` 选择 `GSPN` 作为高层输入，是为了兼顾随机离散事件系统建模灵活性与路径生成效率。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `GSPN` 模型；
2. 对应的同步 `LHA` 属性监视器；
3. `HASL` 表达式 `Z`；
4. 统计参数，如置信区间和样本控制。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `GrML` XML 表示的 `GSPN`；
2. `GrML` XML 表示的 `LHA`；
3. `COSMOS` 自动生成的 `C++` 仿真代码；
4. 结果文件中的均值、置信区间与轨迹统计输出。

### 交换与互操作

1. `COSMOS` 采用 `GrML` 作为模型与属性的共同承载格式。
2. `CosyVerif` 提供图形化集成入口。
3. 工具链更偏“平台内部互操作”，而非跨社区事实标准。

## 配套基础设施

- 建模/编辑工具：`COSMOS` 集成在 `CosyVerif` 中，支持命令行和图形界面。
- 解析/交换/元模型支持：`GrML` XML、`GSPN parser`、`LHA parser`。
- 仿真/执行支持：自动代码生成后的 `C++` 模拟器、并行运行多个副本。
- 验证/分析支持：统计模型检查、置信区间估计、复杂 reward / path measure 评估。
- 代码生成/转换支持：`GSPN + LHA -> C++` 的 model-driven code generation。
- 标准化或社区生态：`CosyVerif` 平台、`BOOST` 随机数库、与 `PRISM / UPPAAL / PLASMA / MARCIE` 等 SMC 工具有可比关系。

## 适用场景与需求前提

### 适用场景

适合需要同时表达“路径筛选条件”和“路径上复杂统计量”的随机离散事件系统分析，例如柔性制造系统、工作流/资源竞争系统、生物振荡过程和一般 `GSPN` 性能评估。

### 需求前提

1. 系统最好能压成 `DESP`，工程上通常进一步落到 `GSPN`。
2. 需求应能写成“某类路径被选中后，对路径变量做统计”的监视器式问题。
3. 使用者接受统计估计和置信区间，而不是纯数值精确解。
4. 属性最好偏瞬态、区间、奖励、条件期望，而不是只做简单布尔判定。

### 不适用或高成本场景

1. 若目标是经典稳态数值求解，`HASL` 不是最直接的入口。
2. 若性质无法被 `LHA` 监视器 almost-sure 地接受或拒绝，使用成本会显著上升。
3. 若模型不自然对应 `DESP/GSPN`，则要先做较重的前置建模转换。

## 与相邻形式主义的关系

相对只支持概率成功事件的 `CSL / CSLTA / CSRL` 线，`HASL` 更强调“监视器驱动的路径筛选 + reward 累计”；相对 `PRISM`、`UPPAAL-SMC`、`PLASMA-lab` 这类现成 SMC 平台，它更把 `LHA` 作为一等属性对象；相对文库中偏纯 `Petri Net` 工具条目，本文的重点不在网模型本体，而在如何用 `LHA` 把复杂性能/可依赖性问题编进一个统一统计检查框架。

## 与本研究的关系

### 对 Project 1 的价值

它提供了一个很强的启发：对控制系统状态机，不一定只把验证性质写成 `LTL/CTL` 公式，也可以把“路径筛选逻辑 + 在线累计变量”封装成监视器自动机。这对后续“验证场景生成”“性质模板表达”“带时间和 reward 的行为约束承载”都有直接参考价值。

### 可复用启发

1. 可以把 `LHA` 思路迁移成面向状态机验证的 observer / monitor 自动机模板。
2. `HASL` 的 `A + Z` 分层很适合把自然语言需求拆成“路径条件”和“统计目标”两块。
3. `GSPN/LHA -> code generation -> statistics` 的链路说明，生成式建模后端不必局限于单一模型检查器，也可以落到仿真+统计验证平台。

## 重要的相关工作

1. `CSLTA` 与多时钟扩展：代表 automaton-based stochastic logic 主线，是 `HASL` 的直接前史。
2. `CSRL`：代表 reward-enriched `CSL` 主线，`HASL` 明显向更复杂 reward/path measure 扩展。
3. `PRISM`、`UPPAAL-SMC`、`PLASMA-lab`、`MARCIE`：构成统计模型检查与随机系统分析的主要平台对照。
4. `COSMOS`：把 `HASL` 从逻辑/语言真正落成了可执行工具链。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 结论：这篇论文最适合作为“随机离散事件系统上的监视器式验证语言与统计分析方法”条目保留。它不提供新的控制状态机母型，但为后续把复杂时序/奖励需求落成可执行 observer 提供了非常强的模板。
