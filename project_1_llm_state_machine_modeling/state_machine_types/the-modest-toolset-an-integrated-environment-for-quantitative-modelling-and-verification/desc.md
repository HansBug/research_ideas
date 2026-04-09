# Modest 工具集：定量建模与验证的一体化环境 / The Modest Toolset: An Integrated Environment for Quantitative Modelling and Verification

## 基本信息

- 标题：The Modest Toolset: An Integrated Environment for Quantitative Modelling and Verification
- 中文标题：Modest 工具集：定量建模与验证的一体化环境
- 作者：Arnd Hartmanns，Holger Hermanns
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 593-598，2014
- DOI：`10.1007/978-3-642-54862-8_51`
- 链接：https://doi.org/10.1007/978-3-642-54862-8_51
- 形式主义：`Modest / networks of stochastic hybrid automata`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：quantitative modelling language + multi-backend analysis environment
- 工具/实现获取方式：原文明确给出 `www.modestchecker.net` 作为下载、文档、案例与相关论文入口。
- 标准/格式获取方式：核心承载方式是 `Modest` 文本语言、probabilistic guarded commands、`Uppaal TA` import/export 与统一的 `SHA` 中间语义；无单独中立交换标准。

## 简报

这篇论文的重要性不在于再提出一个单点求解器，而在于给“概率 + 实时 + 连续动力学”这类定量模型做出一个统一工作台。`Modest Toolset` 用 `networks of stochastic hybrid automata (SHA)` 做共同语义底盘，再把 `Modest`、guarded commands 和 `Uppaal TA` 这些不同建模入口，以及 `prohver`、`mcpta`、`mctau`、`modes` 这些分析后端串成一体。

- 形式主义定位：跨多类定量自动机的统一建模与分析基础设施。
- 构造方式简述：不同输入语言先归一到 `SHA`，再按模型子类选不同分析后端。
- 基础设施与场景简述：依托 `Modest`、`SHA` 语义、`mime` 图形界面与多后端分析器，服务 real-time、stochastic、hybrid 系统的定量验证。

```text
Modest / guarded commands / Uppaal TA -> networks of SHA -> backend-specific restriction -> quantitative verification or simulation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 统一语义底盘 `networks of stochastic hybrid automata`。
2. 三个输入入口：`Modest`、probabilistic guarded commands、`Uppaal TA`。
3. 四个分析后端：`prohver`、`mcpta`、`mctau`、`modes`。
4. `mime` 图形界面与统一命令行接口。

### 核心抽象

论文直接给出了 `SHA` 对各子模型的包含关系，可压成：

$$
\mathrm{DTMC} \subseteq \mathrm{MDP} \subseteq \mathrm{PTA} \subseteq \mathrm{STA} \subseteq \mathrm{SHA}
$$

$$
\mathrm{LTS} \subseteq \mathrm{TA} \subseteq \mathrm{HA} \subseteq \mathrm{PHA} \subseteq \mathrm{SHA}
$$

上式中的符号逐项解释如下：

1. `DTMC` 是离散时间马尔可夫链。
2. `MDP` 是马尔可夫决策过程。
3. `PTA` 是概率定时自动机。
4. `STA` 是随机定时自动机。
5. `LTS`、`TA`、`HA`、`PHA` 分别是标号迁移系统、定时自动机、混成自动机、概率混成自动机。
6. `SHA` 是论文作为统一语义基础的 stochastic hybrid automata。

结合论文“sets of automata that run asynchronously and can communicate via shared actions and global variables”的表述，可把一个 `SHA` 网络保守写成：

$$
\mathcal{N} = (\mathcal{A}_1,\ldots,\mathcal{A}_n, V, Act)
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}_1,\ldots,\mathcal{A}_n` 是并行运行的自动机组件。
2. `V` 是全局变量集合。
3. `Act` 是共享动作集合。
4. 这组记号是根据论文文字描述对 `SHA` 网络骨架做的保守归纳。

### 一个最小例子与通俗解释

论文给了一个很好的最小例子：有损信道。

1. `snd` 发送后，有 `0.99` 概率进入等待接收状态。
2. 也有 `0.01` 概率消息直接丢失。
3. 若进入等待状态，则延迟 `2` 个时间单位后触发 `rcv`。

这件事在论文里分别用 `Modest`、guarded commands 和 `Uppaal TA` 三种语言表示。通俗地说，`Modest Toolset` 的价值就是“同一个定量行为，可以从不同语法入口写进来，再交给统一后端去算”。

### 运行 / 接受 / 转移语义

论文把 `SHA` 的三种关键语义因素说得很清楚，可压成：

$$
\text{quantitative model} = \text{continuous dynamics} + \text{nondeterminism} + \text{probability}
$$

上式中的符号逐项解释如下：

1. `continuous dynamics` 对应微分方程和一般连续变量演化。
2. `nondeterminism` 用于并发、抽象或环境不确定性。
3. `probability` 用于已知分布的随机选择与随机延迟。

不同分析后端只覆盖 `SHA` 的不同子类。可保守写成：

$$
\mathcal{N} \xrightarrow{\mathrm{restrict}} \mathcal{N}' \xrightarrow{\mathrm{backend}} result
$$

其中：

1. `\mathcal{N}` 是统一的 `SHA` 网络。
2. `\mathcal{N}'` 是满足某个后端前提的受限子模型。
3. `backend` 可能是 `prohver`、`mcpta`、`mctau` 或 `modes`。

### 语义边界

论文明确承认：

1. `SHA` 是统一语义底盘，但不同后端并不都能吃下全部 `SHA`。
2. 工具集主打的是复用现有建模语言与分析器，不是“从零实现所有求解器”。
3. 因此它的强项是统一入口和统一工作流，而不是单一算法极限。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `SHA` 覆盖关系 1 | `$\mathrm{DTMC} \subseteq \mathrm{MDP} \subseteq \mathrm{PTA} \subseteq \mathrm{STA} \subseteq \mathrm{SHA}$` | 概率/实时子类都被统一到底盘中。 |
| `SHA` 覆盖关系 2 | `$\mathrm{LTS} \subseteq \mathrm{TA} \subseteq \mathrm{HA} \subseteq \mathrm{PHA} \subseteq \mathrm{SHA}$` | 离散、定时、混成与概率混成都可纳入。 |
| 网络骨架 | `$\mathcal{N} = (\mathcal{A}_1,\ldots,\mathcal{A}_n, V, Act)$` | 统一的 automata-network 视角。 |
| 分析链 | `$\mathcal{N} \xrightarrow{\mathrm{restrict}} \mathcal{N}' \xrightarrow{\mathrm{backend}} result$` | 先统一，再按后端可处理子类求解。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 自动机网络是核心。 |
| 事件 / 触发 | 强支持 | 共享动作、guards 与同步是常规能力。 |
| 守卫 / 数据 | 强支持 | 输入语言和后端都支持丰富表达。 |
| 层次 | 中等支持 | 不是层次状态机工具，但支持组合式建模。 |
| 并发 / 同步 | 很强 | 多自动机异步运行并通过共享动作通信。 |
| 时间约束 | 很强 | 定时与随机延迟是核心。 |
| 连续动态 / 随机性 | 很强 | 统一处理连续动力学与概率/随机性。 |
| 可执行 / 可验证性 | 很强 | 有多后端验证与仿真链。 |

### 形式化问题与性质

1. 这篇论文主打的是“统一工作台”，不是单点模型本体。
2. `SHA` 作为共同语义，使已有模型和已有后端都能被复用。
3. 这类平台型论文对文库的价值，在于把原本分裂的 `PTA/STA/HA/PHA` 支线拉到同一基础设施视角下。

## 构造方式与承载格式

### 建模入口

原文给出的建模入口有三条：

1. `Modest` 高层组合式文本语言。
2. probabilistic guarded commands。
3. `Uppaal TA` 的图形/文本模型导入导出。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Modest` 源文件。
2. guarded-command 文本模型。
3. `Uppaal TA` 模型。
4. 统一的 `SHA` 中间语义。

### 交换与互操作

这篇论文的互操作重点在于：

1. 三种输入语言可互转并统一到底层 `SHA`。
2. 后端求解器可按子类分工复用。
3. 图形界面 `mime` 与命令行共享同一工具基础设施。

## 配套基础设施

- 建模/编辑工具：`mime` 图形界面与命令行。
- 解析/交换/元模型支持：`Modest`、guarded commands、`Uppaal TA` import/export。
- 仿真/执行支持：`modes` 支持 simulation 和 statistical model checking。
- 验证/分析支持：`prohver`、`mcpta`、`mctau`、`modes`。
- 代码生成/转换支持：重点是模型转换与后端桥接，不是部署代码生成。
- 标准化或社区生态：`Modest` 网站、案例、文档与多后端研究生态。

## 适用场景与需求前提

### 适用场景

适合需要同时表达概率、时间和一定连续动力学，并希望在一个平台里切换输入语言与分析后端的 CPS / safety-critical 定量分析场景。

### 需求前提

1. 目标模型能落到 `SHA` 或其典型子类。
2. 团队确实关心 dependability、performance、expected reward 之类定量性质。
3. 能接受“统一平台 + 多后端分工”的工作方式。

### 不适用或高成本场景

如果问题只是简单离散状态机，或者只需要某一个专用求解器，`Modest Toolset` 的统一性优势就不那么关键。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM` 更像单一平台，而 `Modest Toolset` 更强调多输入语言和多后端统一；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 只是一条输入/后端支线；相对 [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)，`PHAVer` 是单点分析器，而这里是把这类工具装进统一环境。

## 与本研究的关系

### 对 Project 1 的价值

它提醒我们：在给状态机族选型时，不能只看模型本体，也要看有没有把不同语言、求解器和案例串起来的“平台型基础设施”。

### 作为目标形式主义还是中间表示

更像平台与中间承载层，而不是最终输出形式主义。

### 对需求到模型生成的启发

1. 若未来需求里混有概率、时间和连续约束，最好提前考虑统一中间语义，而不是等后面再临时拼接多个后端。
2. “多前端 + 统一中间表示 + 多后端”是一条值得借鉴的架构模式。
3. 这类平台允许后续闭环研究把“生成”和“验证”分别挂在不同入口与后端上。

### 现实限制

统一平台不意味着所有子类都被同一算法完整处理；后端能力仍有边界。

## 重要的相关工作

1. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：概率实时平台。
2. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：经典 timed automata 工具链。
3. [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)：混成自动机 reachability 工具锚点。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：主贡献是以 `SHA` 为共同底盘组织多语言、多后端的统一分析环境。
