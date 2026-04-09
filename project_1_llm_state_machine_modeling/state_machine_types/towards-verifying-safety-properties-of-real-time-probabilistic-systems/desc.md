# 面向实时概率系统安全性质验证 / Towards Verifying Safety Properties of Real-Time Probabilistic Systems

## 基本信息

- 标题：Towards Verifying Safety Properties of Real-Time Probabilistic Systems
- 中文标题：面向实时概率系统安全性质验证
- 作者：Fenglin Han，Jan Olaf Blech，Peter Herrmann，Heinz Schmidt
- 发表：*Electronic Proceedings in Theoretical Computer Science*，147，pp. 1-15，2014
- DOI：`10.4204/EPTCS.147.1`
- 链接：https://doi.org/10.4204/EPTCS.147.1
- 形式主义：`Reactive Blocks / PRTESM / PTA / PRISM / BeSpaceD`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：probabilistic real-time safety verification route for Reactive Blocks
- 工具/实现获取方式：论文明确基于 `SPACE / Reactive Blocks` 工具集扩展，并集成 `PRISM` 与 `BeSpaceD`；其中 `Reactive Blocks` 负责建模与代码生成，`PRISM` 负责概率实时模型检查，`BeSpaceD` 负责空间性质验证。
- 标准/格式获取方式：核心承载方式是 `Reactive Blocks` building blocks、`PRTESM`、导出的 `PRISM PTA` / `PCTL` 语句，以及为 `BeSpaceD` 生成的时空 trace 记录。

## 简报

这篇论文的关键点，不是又讲一遍 `PRISM` 或 timed automata，而是把 `Reactive Blocks` 这种可复用组件式建模环境扩展成“能表达概率实时行为、能做概率时序证明、还能追踪空间安全影响”的一条完整方法路线。它把 building blocks 的外部状态机进一步扩展成 `PRTESM`，再自动翻译到 `PRISM` 和 `BeSpaceD`，从而让“反应时间概率分布会不会导致空间碰撞”这种问题在开发期就能被检查。

- 形式主义定位：`Reactive Blocks` 概率实时安全验证方法，而不是新的状态机族母线。
- 构造方式简述：先在 `Reactive Blocks` 中建模 building blocks 与环境模拟器，再用 `PRTESM` 描述概率实时接口行为，随后翻译到 `PTA/PCTL` 给 `PRISM`，并把时空 traces 送入 `BeSpaceD`。
- 基础设施与场景简述：依托 `Reactive Blocks`、`PRTESM`、`PRISM`、`BeSpaceD` 与自动代码生成/仿真，服务机器人、嵌入式控制和 CPS 中带概率反应时间与空间安全要求的系统。

```text
Reactive Blocks model + environment simulator -> PRTESM -> PTA + PCTL -> PRISM probability result -> spatiotemporal traces -> BeSpaceD collision / safety analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Reactive Blocks` building blocks、UML activities 与 `ESM/RTESM`。
2. 概率实时时间扩展 `PRTESM`。
3. 基础验证后端 `PTA` 与 `PCTL/PTCTL`。
4. `PRISM` 概率模型检查。
5. `BeSpaceD` 的时空占用与碰撞分析。

### 核心抽象

论文明确说明其概率实时形式主义建立在 `PTA` 之上。结合其叙述，可把 underlying model 写成：

$$
A = (L, l_0, X, \Sigma, inv, prob)
$$

上式中的符号逐项解释如下：

1. `L` 是 locations 集合。
2. `l_0` 是初始 location。
3. `X` 是时钟集合。
4. `\Sigma` 是动作/同步标签集合。
5. `inv` 是 location invariants。
6. `prob` 是带概率的跳转关系。
7. 这是论文明确采用的 `PTA` 背景形式化对象的保守整理。

论文本身引入了 `PRTESM` 作为 `ESM/RTESM` 的扩展，可把其接口行为骨架保守写成：

$$
M_{PRT} = (S, s_0, \Sigma, C, \Pi, \to)
$$

上式中的符号逐项解释如下：

1. `S` 是 `PRTESM` 状态集合。
2. `s_0` 是初始状态。
3. `\Sigma` 是通信与同步动作集合。
4. `C` 是实时时钟/截止约束集合。
5. `\Pi` 是离散概率分布参数集合。
6. `\to` 是带 guard、clock 与 probability 的迁移。
7. 这是对论文“PRTESM 允许描述概率实时时间行为并可直接翻译到 PTA”的保守归纳。

论文直接给出了其 `PRISM` 查询模板：

$$
P=?[F_{\leq T}\ \texttt{"target"}]
$$

上式中的符号逐项解释如下：

1. `P=?` 表示查询数值概率。
2. `F_{\leq T}` 表示“在不超过 `T` 的时间内最终达到”。
3. `\texttt{"target"}` 是模型中标记目标动作或目标状态发生的标签。
4. 论文用它来验证整体反应时间分布。

在具体机器人场景里，论文给出的实例是：

$$
P=?[F_{\leq 4600}\ \texttt{"target"}]
$$

上式中的符号逐项解释如下：

1. 时间单位采用论文所述的 100 微秒粒度。
2. `4600` 对应 `0.46s`。
3. 该公式用于评估系统是否能在 `0.46s` 内完成关键反应链。

论文还给出了空间占用的规范化模式：

$$
time = t \;\to\; occupied(area_1, p_1) \land \cdots \land occupied(area_n, p_n)
$$

上式中的符号逐项解释如下：

1. `t` 是某个离散时间点。
2. `area_i` 是某个空间区域。
3. `p_i` 是系统在该时间点占用该区域的概率。
4. 这是论文对 `BeSpaceD` 输入风格的直接概括。

### 一个最小例子与通俗解释

论文用 factory hall 中的 moving robot 场景做说明：

1. 机器人沿直线在厂房中央移动，最大速度 `10m/s`。
2. 安全控制器每隔 `10ms` 轮询人和机器人位置。
3. 根据人与机器人的距离，切换 `Normal / Yellow / Red` 三种运行模式。
4. 传感、处理、通信与执行四类任务都带有离散概率的时延分布。
5. `PRISM` 计算整体反应时间概率，`BeSpaceD` 再判断这些反应时延是否会导致空间碰撞。

通俗地说，这条路线不是只问“控制器最终会不会停下”，而是问“它在多大概率上能在足够短的时间内停下，从而把空间碰撞风险压到可接受范围”。

### 运行 / 接受 / 转移语义

论文的关键运行流程可以保守整理为：

$$
\tau_{PTA} : M_{PRT} \to A
$$

和

$$
\tau_{Space} : Trace(M_{PRT}) \to Spec_{BeSpaceD}
$$

上式中的符号逐项解释如下：

1. `\tau_{PTA}` 表示把 `PRTESM` 翻译成 `PRISM` 可处理的 `PTA`。
2. `Trace(M_{PRT})` 表示从仿真中抽取的时空 traces。
3. `\tau_{Space}` 表示把 traces 转成 `BeSpaceD` 的空间规范输入。
4. 这两步正是论文五步工程流程中的核心自动化桥。

论文给出的 `PRISM` 模块代码还说明，一条概率迁移会被展开为多段概率分支，例如：

$$
s=2 \to r_1:(s'=5) + (r_2-r_1):(s'=6) + \cdots + (r_5-r_4):(s'=9)
$$

上式中的符号逐项解释如下：

1. `s` 是当前离散控制状态。
2. `r_i` 是累积概率界。
3. 每个目标状态代表不同的时延区间。
4. 这是论文图 7 中 `PRISM` 代码片段的直接数学化整理。

### 语义边界

论文也明确指出了若干限制：

1. 某些 intra/inter-component communications 如果不是以 `ESM` 风格建模，就无法被该路线直接捕捉。
2. 方法的适用性依赖建模抽象层次。
3. 论文主要处理离散概率分布，而不是连续概率分布。
4. 空间分析目前基于仿真抽取 traces，而不是全量符号空间推理。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 底层 `PTA` 骨架 | `$A = (L, l_0, X, \Sigma, inv, prob)$` | 论文明确采用 `PTA` 作为概率实时验证后端。 |
| `PRTESM` 骨架 | `$M_{PRT} = (S, s_0, \Sigma, C, \Pi, \to)$` | 概括了 `ESM/RTESM` 到概率实时接口模型的扩展。 |
| 概率实时性质 | `$P=?[F_{\leq T}\ \texttt{"target"}]$` | 论文用于验证整体反应时间概率的查询模板。 |
| 空间占用规范 | `$time=t \to occupied(area_1,p_1)\land\cdots\land occupied(area_n,p_n)$` | 表示在某时间点系统占据不同空间区域的概率。 |
| 概率分支 | `$s=2 \to r_1:(s'=5)+(r_2-r_1):(s'=6)+\cdots$` | 对应论文图 7 中的 `PRISM` 命令。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `ESM/RTESM/PRTESM` 与控制模式切换是核心。 |
| 事件 / 触发 | 很强 | building blocks 间通信动作直接进入 `PRTESM`/`PTA`。 |
| 守卫 / 数据 | 中等支持 | 距离与模式选择逻辑明确，但本文重点在时钟与概率。 |
| 层次 | 中等支持 | 依托 `Reactive Blocks` building blocks 组合。 |
| 并发 / 同步 | 强支持 | `PRISM` 同步标签与分布式 building blocks 组合是主线。 |
| 时间约束 | 很强 | 实时时钟、截止约束与反应时间概率是核心。 |
| 连续动态 / 随机性 | 随机性强，连续动态间接支持 | 连续运动用模拟器近似，概率时延分布直接建模。 |
| 可执行 / 可验证性 | 很强 | 建模、仿真、`PRISM` 查询、`BeSpaceD` 空间分析与代码生成都已连通。 |

### 形式化问题与性质

1. 论文的关键创新是把概率实时行为拉进 `Reactive Blocks` 这种组件化开发环境，而不是只在独立 model checker 里建模。
2. 它强调“概率时延会引起空间安全后果”这一跨层联系，这比单纯验证时序公式更贴近 CPS 真实风险。
3. `PRTESM -> PTA -> PRISM` 与 `trace -> BeSpaceD` 两条翻译链共同构成了该方法的核心。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. 用 `Reactive Blocks` 建立 building blocks、UML activities 与环境模拟器。
2. 用 `PRTESM` 注释概率实时接口行为。
3. 自动翻译为 `PRISM` 的 `PTA` 模块与 `PCTL/PTCTL` 查询。
4. 仿真时抽取时空 traces，转给 `BeSpaceD`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Reactive Blocks` building blocks 与 `ESM/PRTESM`。
2. `PRISM` module code。
3. `PCTL/PTCTL` probability queries。
4. `BeSpaceD` 的时空 occupancy traces。
5. 由 `Reactive Blocks` 生成的可执行 Java 模拟器/核心代码。

### 交换与互操作

这条路线的互操作重点非常明确：

1. `Reactive Blocks` 到 `PRISM` 的模型翻译。
2. `Reactive Blocks` 仿真 traces 到 `BeSpaceD` 的空间验证翻译。
3. 同一模型在功能验证、概率时序验证和空间安全验证之间共享结构化 building blocks。

## 配套基础设施

- 建模/编辑工具：`Reactive Blocks`、building blocks、UML activities、`ESM/PRTESM`。
- 解析/交换/元模型支持：自动生成 `PRISM` 模块、性质语句与 `BeSpaceD` traces。
- 仿真/执行支持：`Reactive Blocks` 生成 Java 模拟器并执行场景。
- 验证/分析支持：内建功能检查、`PRISM` 概率模型检查、`BeSpaceD` 空间碰撞分析。
- 代码生成/转换支持：通过 `Reactive Blocks` 自动生成 Java 代码；另有模型到 `PRISM/BeSpaceD` 的翻译。
- 标准化或社区生态：依托 `Reactive Blocks`、`PRISM` 与 `BeSpaceD` 三类工具生态。

## 适用场景与需求前提

### 适用场景

适合机器人、嵌入式控制、CPS 安全控制和其他需要同时考虑概率时延、实时反应与空间安全的系统。

### 需求前提

1. 系统能被拆成 `Reactive Blocks` 风格的 reusable building blocks。
2. 关键风险能被表达成离散概率时延分布。
3. 空间后果可由仿真 traces 近似抽取。
4. 团队接受 `Reactive Blocks + PRISM + BeSpaceD` 的多工具协同流程。

### 不适用或高成本场景

如果系统通信行为难以投射到 `ESM/PRTESM`，或者概率与空间模型必须完全符号化而非仿真抽取，这条路线会比较吃力。

## 与相邻形式主义的关系

相对 [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)，本文不是单纯把高层模型翻到 `PRISM`，而是把概率实时验证与空间安全后果结合起来；相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM 4.0` 是基础后端平台，而这里是面向 `Reactive Blocks` 的开发流程扩展；相对 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)，`SpaceEx` 偏混成可达性，而本文偏离散概率时延与空间占用风险。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文直接说明：如果未来 `project_1` 的生成目标包含安全关键 CPS，状态机模型不应只停在功能正确性，还应考虑“时间概率分布会不会通过空间后果放大风险”。这非常贴近“生成-验证-修复”闭环里后两步的实际需求。

### 作为目标形式主义还是中间表示

更像验证桥与分析流程，而不是最终目标形式主义；其中 `PRTESM` 与 `PTA` 更像高价值中间表示。

### 对需求到模型生成的启发

1. 若需求中已包含反应时延与风险概率，生成的状态机最好原生保留这些参数。
2. 组件式状态机若能自动投射到概率验证与空间分析后端，会极大增强闭环修复能力。
3. 安全性质不一定只写成布尔“会/不会”，也可以是概率阈值约束。

### 现实限制

这条路线对建模抽象和工具桥接要求较高，不适合把所有 CPS 都一股脑套进去。

## 重要的相关工作

1. [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)：`PTA -> PRISM` 的另一条工具桥。
2. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：概率实时模型检查基础平台。
3. [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：更现代的概率模型检查后端平台。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Reactive Blocks / PRTESM / PTA / PRISM / BeSpaceD`
- 论文角色：probabilistic real-time safety verification route for Reactive Blocks
- 归类理由：论文主体是把 `Reactive Blocks` 接到概率实时与空间安全验证后端的方法路线，而不是单独提出新的母线形式主义。
