# modes：面向非确定性与罕见事件的统计模型检查器 / A Statistical Model Checker for Nondeterminism and Rare Events

## 基本信息

- 标题：A Statistical Model Checker for Nondeterminism and Rare Events
- 中文标题：modes：面向非确定性与罕见事件的统计模型检查器
- 作者：Carlos E. Budde，Pedro R. D’Argenio，Arnd Hartmanns，Sean Sedwards
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 340-358，2018
- DOI：`10.1007/978-3-319-89963-3_20`
- 链接：https://doi.org/10.1007/978-3-319-89963-3_20
- 形式主义：`statistical model checking / modes / Modest Toolset`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：结合 importance splitting 与 lightweight scheduler sampling 的 statistical model-checking 方法与工具平台
- 工具/实现获取方式：原文说明 `modes` 是 `Modest Toolset` 的一部分，可随该工具线获得；同时支持 `JANI` 交换格式与多核 / 分布式运行。
- 标准/格式获取方式：核心承载是 `Modest`、`xSADF`、`JANI`、内部统一 metamodel、simulation workers 与 `SMC` 查询配置；不是独立行业标准。

## 简报

这篇论文的重点不是“又一个 SMC 工具”，而是把两个长期难点同时工程化：一是 rare events 导致普通 Monte Carlo 采样极慢，二是 nondeterminism 使普通 simulation 不再有可靠语义。`modes` 通过 automated importance splitting 处理罕见事件，通过 lightweight scheduler sampling 近似最优调度器，从而把统计模型检查推进到 `MDP/MA/PTA/SHA` 这类更复杂的模型上。

- 形式主义定位：面向 nondeterministic stochastic models 的统计模型检查方法与工具路线。
- 构造方式简述：模型统一接入 `Modest Toolset` 内部元模型，再由 simulator、scheduler sampler、importance splitting 和 statistical evaluator 组合执行。
- 基础设施与场景简述：依托 `Modest Toolset`、`JANI`、multi-core / distributed simulation、importance splitting 与 `LSS`，服务 rare-event estimation、expected reward 与 nondeterministic quantitative analysis。

```text
stochastic / timed / hybrid model -> simulator + scheduler sampling + rare-event splitting -> statistical evaluation -> probability / reward estimate
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. statistical model checking (`SMC`)；
2. importance splitting 罕见事件估计；
3. lightweight scheduler sampling (`LSS`)；
4. 支持的模型族：`DTMC`、`CTMC`、`MDP`、`MA`、`PTA` 与受限 `SHA`；
5. `modes` 的 modular software architecture 与多核 / 分布式执行。

### 核心抽象

论文明确说明 `modes` 面向多种 stochastic model family，可压成：

$$
\mathcal M = \{\mathrm{DTMC},\mathrm{CTMC},\mathrm{MDP},\mathrm{MA},\mathrm{PTA},\mathrm{SHA}\}
$$

上式中的符号逐项解释如下：

1. `DTMC` 是离散时间马尔可夫链。
2. `CTMC` 是连续时间马尔可夫链。
3. `MDP` 是马尔可夫决策过程。
4. `MA` 是 Markov automata。
5. `PTA` 是 probabilistic timed automata。
6. `SHA` 指论文支持的那部分 stochastic hybrid automata 语义家族。

论文直接给出两类核心查询：

$$
P(\neg avoid\ U\ goal)
$$

$$
E(reward \mid goal)
$$

上式中的符号逐项解释如下：

1. `P(\neg avoid\ U\ goal)` 表示在不先进入 `avoid` 的前提下最终到达 `goal` 的概率。
2. `E(reward \mid goal)` 表示首次到达 `goal` 之前累积 reward 的期望值。
3. `avoid` 与 `goal` 都是对模型状态的谓词。
4. `reward` 可以是状态奖励和分支奖励共同定义的累积代价。

### 一个最小例子与通俗解释

一个最小直觉例子可以是无线协议或安全系统里的 rare-event reachability：

1. 系统大多数运行都会保持正常。
2. 只有极少数路径会到达 `failed`，这就是 rare event。
3. 若模型里还存在非确定分支，验证者关心的不是“某个随机 scheduler 下的失败概率”，而是最大或最小失败概率。
4. `modes` 先通过 importance splitting 提高 rare path 的采样效率，再通过 `LSS` 在多个 scheduler 之间搜索近优者。

通俗地说，`modes` 不只是“多跑几次仿真”，而是在统计采样里同时处理“稀有”和“有对手 / 有选择”这两件最棘手的事。

### 运行 / 接受 / 转移语义

论文把统计估计的结果写成样本均值，可压成：

$$
\hat v_n = \frac{1}{n}\sum_{i=1}^{n} v_i
$$

上式中的符号逐项解释如下：

1. `v_i` 是第 `i` 次 simulation run 对查询给出的单次取值。
2. `n` 是样本条数。
3. `\hat v_n` 是对真实概率或期望值的统计估计。

在有 non-determinism 的情况下，`modes` 关心的是对调度器空间做统计近似。可保守写成：

$$
\hat v^\star = \max_{\sigma \in \Sigma_{\mathrm{sched}}} \hat v_n(\sigma)
$$

上式中的符号逐项解释如下：

1. `\Sigma_{\mathrm{sched}}` 是候选 scheduler 集合。
2. `\hat v_n(\sigma)` 是在某个 scheduler `\sigma` 下的样本估计。
3. `\hat v^\star` 表示通过 `LSS` 近似搜索到的最优估计值。
4. 这是对论文“approximate optimal schedulers”思路的保守符号化整理。

### 语义边界

1. `modes` 不是 exhaustive probabilistic model checker，而是基于 simulation 的统计近似工具。
2. 其对 `SHA` 的支持只覆盖一个受限可模拟子集，而不是一般混成自动机。
3. 对 nondeterminism 的处理是统计近似最优 scheduler，不是完全精确求解。
4. rare-event 技术高度依赖 importance function 与 level construction 的自动化效果。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 支持模型族 | `$\mathcal M = \{\mathrm{DTMC},\mathrm{CTMC},\mathrm{MDP},\mathrm{MA},\mathrm{PTA},\mathrm{SHA}\}$` | `modes` 不是单一模型工具，而是覆盖多类 stochastic/timed/hybrid family。 |
| transient 查询 | `$P(\neg avoid\ U\ goal)$` | rare-event reachability 的核心查询骨架。 |
| reward 查询 | `$E(reward \mid goal)$` | 期望代价 / 奖励查询的核心骨架。 |
| 样本估计 | `$\hat v_n = \frac{1}{n}\sum_{i=1}^{n} v_i$` | `SMC` 的最基本统计输出。 |
| scheduler 近似优化 | `$\hat v^\star = \max_{\sigma \in \Sigma_{\mathrm{sched}}} \hat v_n(\sigma)$` | `LSS` 用于搜索近优 scheduler。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 支持多类 stochastic/timed/hybrid state models。 |
| 事件 / 触发 | 中等支持 | 依赖具体前端模型语义。 |
| 守卫 / 数据 | 中等支持 | `PTA`、`SHA` 与 `Modest/JANI` 前端都包含变量与条件。 |
| 层次 | 弱支持 | 不是层次状态机前端。 |
| 并发 / 同步 | 中等支持 | 由输入模型与 simulator 支持，而非工具专门语言特性。 |
| 时间约束 | 很强 | `CTMC`、`MA`、`PTA` 与受限 `SHA` 都涉及定量时间。 |
| 连续动态 / 随机性 | 很强 | rare events、概率、期望值和受限连续动力学是主体。 |
| 可执行 / 可验证性 | 很强 | 支持 multi-core、distributed、automated splitting 与 scheduler sampling。 |

### 形式化问题与性质

1. 这篇论文的主创新在方法路线：importance splitting 与 `LSS` 的可组合化。
2. 它让统计模型检查不再只适用于“纯随机、无 non-determinism”的简化模型。
3. 对文库而言，它既是 `Modest` 量化工具线的关键补充，也是 rare-event `SMC` 的工程锚点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Modest` 高层模型。
2. `xSADF` 模型。
3. `JANI` 交换格式。
4. `Modest Toolset` 共享基础设施中的内部统一 metamodel。

### 机器可处理承载方式

机器可处理承载方式包括：

1. simulator-specific internal metamodel。
2. transient / reward queries。
3. scheduler samples、importance levels 与 statistical evaluators。
4. multi-core / distributed worker execution。

### 交换与互操作

互操作重点在于：

1. `JANI` 使外部 quantitative tools 的模型可接入。
2. `modes` 作为 `Modest Toolset` 后端，与其他后端共享前端与基础设施。
3. modular architecture 允许 rare-event、scheduler sampling 与统计评估模块灵活组合。

## 配套基础设施

- 建模/编辑工具：依托 `Modest Toolset` 前端与相关输入语言，不主打独立图形编辑器。
- 解析/交换/元模型支持：`Modest`、`xSADF`、`JANI` 到内部 metamodel 的统一编译。
- 仿真/执行支持：多核、分布式 simulation，支持不同模型族的专用 simulator。
- 验证/分析支持：importance splitting、`LSS`、置信区间、假设检验、reward / reachability 分析。
- 代码生成/转换支持：重点是 simulation-based verification，不主打部署代码生成。
- 标准化或社区生态：依托 `Modest Toolset` 与 `JANI` 生态，在 quantitative verification 社区中互操作性较强。

## 适用场景与需求前提

### 适用场景

适合那些既有 stochastic / timed / hybrid 模型，又关心 rare-event probability、expected reward 或 non-deterministic optimal scheduler 近似的定量验证场景。

### 需求前提

1. 模型必须可有效模拟。
2. 需求更偏 reachability probability、expected reward 或相关 hypothesis testing，而不是严格的精确数值求解。
3. 若存在 non-determinism，团队接受统计近似最优 scheduler，而不是要求精确策略合成。

### 不适用或高成本场景

如果问题只适合精确符号模型检查，或者模型无法有效模拟、rare-event importance function 自动化效果很差，`modes` 的优势就会减弱。

## 与相邻形式主义的关系

相对 [ymer-a-statistical-model-checker/desc.md](../ymer-a-statistical-model-checker/desc.md)，`Ymer` 更早、也更偏传统 `SMC`，而本文把 rare events 和 nondeterminism 同时系统推进；相对 [plasma-lab-a-flexible-distributable-statistical-model-checking-library/desc.md](../plasma-lab-a-flexible-distributable-statistical-model-checking-library/desc.md)，`PLASMA-lab` 更强调 simulator interface 与多前端接入，本文更强调 rare-event + scheduler-sampling 组合；相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，那篇是平台总览，本文是其统计验证后端的细化实现。

## 与本研究的关系

### 对 Project 1 的价值

1. 它表明“生成状态机后如何做验证”未必只能走穷举模型检查，也可以走 simulation-based quantitative verification。
2. 对带随机性、罕见故障和复杂连续动力学近似的需求，`modes` 一类工具比传统显式穷举更现实。
3. 这也为后续 `project_2` / `project_3` 中的验证场景与 profile 设计提供了“概率 / reward / rare-event”方向的证据。

### 作为目标形式主义还是中间表示

更像验证方法与分析平台，而不是需求直接生成的最终形式主义。

### 对需求到模型生成的启发

1. 如果需求里出现“极小概率故障”“最坏 / 最优调度器”“期望代价”，生成阶段就要保留概率和 reward 语义。
2. 对这类模型，后续验证接口最好直接生成 `goal/avoid/reward` 形式的查询，而不是只生成布尔安全性质。
3. 生成结果若能对接 `JANI` 或 `Modest` 风格中间层，会更容易接入 quantitative ecosystem。

### 现实限制

统计近似方法终究要在精度、运行时间和置信度之间权衡，无法完全替代精确求解器。

## 重要的相关工作

1. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：`modes` 所属平台总览。
2. [plasma-lab-a-flexible-distributable-statistical-model-checking-library/desc.md](../plasma-lab-a-flexible-distributable-statistical-model-checking-library/desc.md)：分布式 `SMC` 基础设施对照线。
3. [ymer-a-statistical-model-checker/desc.md](../ymer-a-statistical-model-checker/desc.md)：更早的统计模型检查器锚点。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`statistical model checking / modes / Modest Toolset`
- 归类理由：论文主体贡献是 rare-event importance splitting 与 nondeterministic scheduler sampling 的统计验证方法路线，并以 `modes` 工具实现承载。
