# mctau：打通 Modest 与 UPPAAL 的桥接工具 / mctau: Bridging the Gap between Modest and UPPAAL

## 基本信息

- 标题：mctau: Bridging the Gap between Modest and UPPAAL
- 中文标题：mctau：打通 Modest 与 UPPAAL 的桥接工具
- 作者：Jonathan Bogdoll，Alexandre David，Arnd Hartmanns，Holger Hermanns
- 发表：*Model Checking Software*，pp. 227-233，2012
- DOI：`10.1007/978-3-642-31759-0_16`
- 链接：https://doi.org/10.1007/978-3-642-31759-0_16
- 形式主义：`Modest / timed automata / mctau / UPPAAL bridge`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`Modest -> UPPAAL` timed-automata translation、分析与可视化桥接工具
- 工具/实现获取方式：原文说明 `mctau` 隶属 `Modest Toolset`，并给出 `www.modestchecker.net`；`UPPAAL` 入口为 `www.uppaal.org`。
- 标准/格式获取方式：核心承载是 `Modest` 文本模型、`UPPAAL` 的 `.xml/.q` 输入、`verifyta` 自动分析链，以及 `mime` 集成界面；不是中立交换标准。

## 简报

这篇论文补的是定量 / 实时工具链里非常实用的一类“桥”：上游保持 `Modest` 的高层组合式建模，下游借用 `UPPAAL` 的定时自动机分析与可视化能力。`mctau` 的难点不只是文件转换，而是要把 `Modest` 与 `UPPAAL` 在时间约束、赋值语义和同步机制上的语义缝隙补平。

- 形式主义定位：`Modest` 到 `UPPAAL timed automata` 的翻译与分析基础设施。
- 构造方式简述：先把 `Modest` 进程网络识别为定时自动机子类，再做 deadline-to-invariant、assignment 与 synchronisation 语义对齐，最后输出 `UPPAAL XML` 或直接驱动 `verifyta`。
- 基础设施与场景简述：依托 `mctau`、`UPPAAL 4.1.5`、`mime`、图布局算法与 `verifyta`，服务 `Modest` 用户对 timed automata 模型的导出、可视化与自动分析。

```text
Modest model -> semantic-gap resolution -> UPPAAL XML / query file -> GUI analysis or verifyta batch checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Modest` 中以 `STA` 为共同语义的高层模型。
2. `UPPAAL` 支持的 network of timed automata。
3. 三类关键语义差距：deadlines vs. invariants、atomic assignments vs. sequential assignments、multi-way synchronisation vs. binary/broadcast synchronisation。
4. `mctau` 的导出与自动分析两种工作模式。
5. 对 `PTA` 的定性 over-approximation 处理。

### 核心抽象

结合论文语境，可把 `mctau` 处理的目标模型骨架保守写成：

$$
\mathcal N = (\mathcal A_1,\ldots,\mathcal A_n,\alpha,X)
$$

上式中的符号逐项解释如下：

1. `\mathcal A_1,\ldots,\mathcal A_n` 是并行运行的自动机组件。
2. `\alpha` 是各组件的动作字母表及其同步关系。
3. `X` 是时钟与变量集合。
4. 该元组不是论文直接给出的统一记法，而是对其“network of timed automata / Modest process network”描述的保守压缩。

桥接本身可以压成一个翻译函数：

$$
\tau_{\mathrm{mctau}} : M_{\mathrm{Modest}} \mapsto U_{\mathrm{UPPAAL}}
$$

上式中的符号逐项解释如下：

1. `M_{\mathrm{Modest}}` 是输入 `Modest` 模型。
2. `U_{\mathrm{UPPAAL}}` 是输出的 `UPPAAL` `.xml` 模型与 `.q` 查询文件。
3. `\tau_{\mathrm{mctau}}` 包含正文重点讨论的三类语义对齐步骤。

### 一个最小例子与通俗解释

论文给出的最小例子是一个通信信道：

1. 进程有动作 `put` 和 `get`，并带一个时钟 `c`。
2. 信道进入等待状态后把 `c` 置零。
3. 位置不变式要求 `c <= TD`，表示最多等待 `TD` 个时间单位。
4. 在等待期间可以发生 `get`，否则可走 `tau` 分支继续演化。

通俗地说，`mctau` 做的事不是“换个文件扩展名”，而是把 `Modest` 里更高层的 timed behaviour 翻成 `UPPAAL` 真正能按相同直觉去跑和分析的 timed automata 图。

### 运行 / 接受 / 转移语义

论文讨论的第一类关键语义映射是 deadline 与 invariant 的对应，可保守写成：

$$
\tau_{\mathrm{time}}(\mathrm{deadline}(c \ge d)) = \mathrm{Inv}(l): c \le d
$$

上式中的符号逐项解释如下：

1. `\mathrm{deadline}(c \ge d)` 表示 `Modest` 边上的紧迫约束。
2. `\mathrm{Inv}(l): c \le d` 表示 `UPPAAL` 位置 `l` 的不变式。
3. 该式表达论文中的核心例子：某些实用 deadline 可以转换成位置不变式。

论文对带概率分支模型的定性 over-approximation 给出了很清楚的查询替换策略：

$$
P_{\max}(\Diamond e) \leadsto (\forall \Box \neg e,\ \forall \Diamond e)
$$

上式中的符号逐项解释如下：

1. `P_{\max}(\Diamond e)` 是“最终到达 `e` 的最大概率”这类概率性质。
2. `\forall \Box \neg e` 检查是否所有路径都永远到不了 `e`，若成立则原概率为 `0`。
3. `\forall \Diamond e` 检查是否所有路径都最终到达 `e`，若成立则原概率为 `1`。
4. 若两者都不成立，则定性 over-approximation 只能说明原概率位于 `[0,1]`。

### 语义边界

1. `mctau` 只覆盖 `Modest` 中能稳定落到 timed-automata 路线的子集。
2. deadline 与 invariant 并非完全等价，论文明确指出某些 equality-style deadlines 不能直接映射。
3. 对 `PTA` 的支持本质上是“把概率分支改成非确定分支”的定性 over-approximation，不保留精确概率值。
4. 论文主打的是 bridge 和 workflow，不是重新定义 timed automata 本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 目标网络骨架 | `$\mathcal N = (\mathcal A_1,\ldots,\mathcal A_n,\alpha,X)$` | `mctau` 面向的是并行 timed-automata/networked process 模型。 |
| 桥接函数 | `$\tau_{\mathrm{mctau}} : M_{\mathrm{Modest}} \mapsto U_{\mathrm{UPPAAL}}$` | 从 `Modest` 到 `UPPAAL` 的翻译是工具主体。 |
| 时间语义映射 | `$\tau_{\mathrm{time}}(\mathrm{deadline}(c \ge d)) = \mathrm{Inv}(l): c \le d$` | deadline-to-invariant 是 bridge 的第一类核心修补。 |
| 概率性质定性替换 | `$P_{\max}(\Diamond e) \leadsto (\forall \Box \neg e,\ \forall \Diamond e)$` | `PTA` 被 over-approx 为 `TA` 后，只保留“概率是 0 / 1 / 不确定”的定性信息。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 目标就是 network of timed automata。 |
| 事件 / 触发 | 很强 | 动作同步、channel、queries 都是核心。 |
| 守卫 / 数据 | 中等支持 | 支持赋值、用户自定义函数和数据类型，但主体仍是 timed route。 |
| 层次 | 弱支持 | 论文不讨论层次状态机。 |
| 并发 / 同步 | 很强 | multi-way、binary、broadcast synchronisation 的语义对齐是核心难点。 |
| 时间约束 | 很强 | deadline、invariant、clock semantics 是本文主轴。 |
| 连续动态 / 随机性 | 弱到中等 | 概率只做定性 over-approximation，不做精确连续/随机分析。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` GUI、`verifyta`、`mime` 与自动导出全部打通。 |

### 形式化问题与性质

1. 这篇论文证明“工具桥接”的关键不是 I/O，而是对三类语义缝隙做精确修补。
2. `mctau` 的工程价值在于让 `Modest` 用户直接重用 `UPPAAL` 的验证与可视化生态。
3. 它也是把 `Modest Toolset` 从“多后端定量平台”细化到“具体 timed-automata backend”的重要证据条目。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Modest` 文本模型。
2. `mime` 中的集成编辑与分析入口。
3. 含概率分支的 `PTA` 风格模型的定性分析入口。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `.modest` 输入文件。
2. 导出的 `UPPAAL` `.xml` 自动机文件。
3. 导出的 `.q` 查询文件。
4. 直接调用 `verifyta` 的自动分析模式。

### 交换与互操作

互操作重点包括：

1. `Modest` 与 `UPPAAL` 之间的模型翻译。
2. `mime` 与 `mctau` 的无缝集成。
3. `UPPAAL` 图形界面与命令行两种分析链路。
4. 对 `PTA` 的 over-approximation 让同一 `Modest` 模型还能继续供 `mcpta` 与 `modes` 使用。

## 配套基础设施

- 建模/编辑工具：`mime` 图形界面与 `Modest` 文本模型。
- 解析/交换/元模型支持：`.modest -> .xml/.q` 翻译、数据类型和函数处理、图布局算法。
- 仿真/执行支持：可导入 `UPPAAL` 图形界面做模拟与可视化。
- 验证/分析支持：`verifyta` 自动分析、`UPPAAL` model checking、PTA 定性 over-approximation。
- 代码生成/转换支持：重点是模型转换与可视化输出，不主打部署代码生成。
- 标准化或社区生态：依托 `Modest Toolset`、`UPPAAL 4.1.5` 与二者各自的学术工具生态。

## 适用场景与需求前提

### 适用场景

适合已经用 `Modest` 建模、但希望借用 `UPPAAL` 生态做 timed verification、图形化检查、快速 sanity check 和批量 `verifyta` 分析的实时系统场景。

### 需求前提

1. 模型需属于 `Modest` 中能落到 timed automata 的那部分。
2. 关键时序行为最好能通过 deadlines、guards 与同步动作表达。
3. 团队愿意接受 `UPPAAL` 作为下游分析与展示载体。

### 不适用或高成本场景

如果需求必须保留精确概率值、复杂连续动力学或完整 `STA` 语义，仅靠 `mctau` 就不够，它更适合 timed-automata 主线而不是整个 `STA` 家族的全语义处理。

## 与相邻形式主义的关系

相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，本文是其 `UPPAAL` 后端细化条目；相对 [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)，`mcpta` 走的是 `Modest -> PTA -> PRISM` 路线，而本文走的是 `Modest -> TA -> UPPAAL` 路线；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，后者讲 timed automata 平台本体，本文讲的是如何把另一种高层语言稳定接进去。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机自动建模不一定直达最终验证器，中间可以保留高层语言，再通过桥接进入下游平台。
2. 对 `project_1` 很有启发的一点是：若后续需求生成阶段采用 richer DSL，可以单独建设“语义对齐层”而非直接放弃现成工具生态。
3. 它也补强了 timed automata 线在文库中的基础设施成熟度证据。

### 作为目标形式主义还是中间表示

更像“高层模型到下游 timed-automata verifier 的桥接层”，而不是最终交付给领域人员的目标形式主义。

### 对需求到模型生成的启发

1. 自动生成阶段可优先面向表达力更高、可读性更好的语言，然后再做到验证平台的保真投影。
2. 语义差距最危险的地方通常是时间、赋值和同步，后续闭环也应重点检查这三块。
3. 图形界面和批处理命令行并存，说明工具链设计应同时考虑“人读”和“机跑”。

### 现实限制

这条路线本质上仍依赖两端工具的具体语义约束，超出其共同交集的模型能力就会被削弱或丢失。

## 重要的相关工作

1. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：`Modest` 平台总览。
2. [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)：`Modest -> PRISM` 的 `PTA` 桥接路线。
3. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：`UPPAAL` timed automata 工具本体。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Modest / timed automata / mctau / UPPAAL bridge`
- 归类理由：主贡献是把 `Modest` 的 timed 子类稳定桥接到 `UPPAAL`，并提供导出、自动分析与可视化基础设施，而不是提出新的自动机母型。
