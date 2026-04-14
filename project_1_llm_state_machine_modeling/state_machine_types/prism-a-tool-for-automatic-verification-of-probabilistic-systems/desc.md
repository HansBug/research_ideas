# PRISM：概率系统自动验证工具 / PRISM: A Tool for Automatic Verification of Probabilistic Systems

## 基本信息

- 标题：PRISM: A Tool for Automatic Verification of Probabilistic Systems
- 中文标题：PRISM：概率系统自动验证工具
- 作者：Andrew Hinton，Marta Z. Kwiatkowska，Gethin Norman，David Parker
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 441-444，2006
- DOI：`10.1007/11691372_29`
- 链接：https://doi.org/10.1007/11691372_29
- 形式主义：`DTMC / MDP / CTMC / PRISM`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：probabilistic model-checking platform / guarded-command based quantitative verification environment
- 工具/实现获取方式：论文直接给出伯明翰主页 `www.cs.bham.ac.uk/~dxp/prism` 作为入口；当前官方站点已演化为 `https://www.prismmodelchecker.org/`，源码、手册与示例仍可获取。
- 标准/格式获取方式：原文明确说明承载方式是 `PRISM` 建模语言与性质语言，核心对象是 modules、guarded commands、rewards，以及针对 `Matlab / ETMCC / MRMC` 的导出格式；无中立交换标准。

## 简报

这篇论文的价值，在于把概率模型检查从零散算法集合收束成一套可持续维护的平台。`PRISM` 用一个基于 `Reactive Modules` 的文本语言，把 `DTMC / MDP / CTMC`、概率时序性质、奖励结构、图形界面、命令行、数值求解与 Monte-Carlo 仿真整合到统一环境中。

- 形式主义定位：概率状态模型的验证基础设施，而不是新的状态机族本体。
- 构造方式简述：用 modules + finite-range variables + probabilistic guarded commands 写模型，再用 `PCTL/CSL` 风格性质与 `R` 奖励查询驱动求解。
- 基础设施与场景简述：依托统一建模语言、GUI/CLI、符号求解、显式求解和仿真引擎，服务通信协议、随机化算法、能耗分析与一般定量系统验证。

```text
probabilistic reactive model -> PRISM language -> symbolic/numeric/simulation engines -> probability / steady-state / reward results
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `PRISM`：

1. `DTMC`。
2. `MDP`。
3. `CTMC`。
4. rewards / costs。
5. `PCTL / CSL` 风格性质。
6. `PRISM` 建模语言与多种分析引擎。

### 核心抽象

论文明确说明 `PRISM` 直接支持三类概率模型。可把其支持集合压成：

$$
\mathcal{M} = \{ DTMC, MDP, CTMC \}
$$

上式中的符号逐项解释如下：

1. `DTMC` 是离散时间 Markov 链。
2. `MDP` 是带非确定性与概率选择的 Markov 决策过程。
3. `CTMC` 是连续时间 Markov 链。
4. 这三类对象构成了 2006 版 `PRISM` 的核心覆盖面。

论文同时说明模型语言基于 `Reactive Modules`。可把一份 `PRISM` 模型保守整理为：

$$
\mathcal{P} = (M_1, \ldots, M_k, V, Syn, R)
$$

上式中的符号逐项解释如下：

1. `M_i` 是第 `i` 个 module。
2. `V` 是全局与局部 finite-range variables 集合。
3. `Syn` 是模块间同步动作集合。
4. `R` 是 states/transitions 上的 reward structure。
5. 这是根据论文对 modules、variables、synchronisation 与 rewards 的描述做的保守归纳。

性质语言方面，论文明确强调三个主操作符：

$$
P[\psi], \qquad S[\phi], \qquad R[\rho]
$$

上式中的符号逐项解释如下：

1. `P` 用于事件发生概率。
2. `S` 用于 long-run / steady-state 概率。
3. `R` 用于 expected cost / reward。
4. 论文给出的示例查询都围绕这三类结果展开。

### 一个最小例子与通俗解释

论文没有展开长案例，但给了典型的性质样式。一个最小直觉例子可以理解为：

1. 先写一个有 `ok` 和 `error` 两个吸收状态的 `DTMC`。
2. 再给“执行一步耗能多少”写一个 reward。
3. 问题一是“最终出错的概率是多少”。
4. 问题二是“在到达 `ok` 之前的期望能耗是多少”。

通俗地说，`PRISM` 就是“把普通模型检查中的真/假问题，扩成概率、长期频率和期望代价这三类数量问题”的平台。

### 运行 / 接受 / 转移语义

论文列出的代表性查询可以压成：

$$
P_{\ge p}[\ \phi_1\ U^{\le T}\ \phi_2\ ]
$$

$$
S_{=?}[\phi]
$$

$$
R_{=?}[F\ target]
$$

上式中的符号逐项解释如下：

1. 第一式表示时间有界直到性质的概率查询。
2. `S_{=?}[\phi]` 表示满足 `\phi` 的长期稳态概率。
3. `R_{=?}[F\ target]` 表示到达目标前累计 reward 的期望值。
4. 论文中 `P / S / R` 三类查询共同构成 `PRISM` 的用户语义入口。

从求解流程角度，可把 `PRISM` 的主线保守写成：

$$
\text{model text} \to \text{finite-state probabilistic model} \to \text{numerical / symbolic / simulation analysis}
$$

这里各符号含义如下：

1. 首先由高层文本模型构造有限状态概率模型。
2. 再由图算法、数值迭代、BDD/MTBDD 风格符号方法或 Monte-Carlo 仿真给出结果。
3. 论文特别强调近似仿真分析已成为与数值求解并列的重要路径。

### 语义边界

这篇论文的边界主要有：

1. 2006 版 `PRISM` 主要覆盖 `DTMC / MDP / CTMC`，而不是更晚才加入的概率实时变体全集。
2. 它是平台型工具论文，不负责奠定这些模型族的理论定义。
3. 尽管支持导出到多个外部工具格式，但它本身不是中立交换标准。
4. 复杂连续动力学或 rich hybrid semantics 不在其主线之内。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 支持模型族 | `$\mathcal{M} = \{ DTMC, MDP, CTMC \}$` | 论文明确给出的核心模型覆盖面。 |
| 平台骨架 | `$\mathcal{P} = (M_1, \ldots, M_k, V, Syn, R)$` | modules、variables、synchronisation 和 rewards 是建模语言主骨架。 |
| 概率查询 | `$P_{\ge p}[\phi_1\ U^{\le T}\ \phi_2]$` | 概率时序性质的典型写法。 |
| 稳态查询 | `$S_{=?}[\phi]$` | long-run probability 查询。 |
| 代价查询 | `$R_{=?}[F\ target]$` | reward/cost 驱动的定量分析入口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕有限状态概率模型工作。 |
| 事件 / 触发 | 中等支持 | 主要通过 guarded commands 与同步动作表达。 |
| 守卫 / 数据 | 强支持 | finite-range variables、global variables 与 probabilistic updates 都很核心。 |
| 层次 | 不支持 | 主线是平铺 modules，而不是层次状态机。 |
| 并发 / 同步 | 强支持 | Reactive Modules 式并行组合是平台基础。 |
| 时间约束 | 条件支持 | `CTMC` 提供连续时间率语义，但此文主线还不是 timed automata。 |
| 连续动态 / 随机性 | 随机性很强，连续动态不支持 | 概率/随机性是核心；连续 ODE 不在范围内。 |
| 可执行 / 可验证性 | 很强 | GUI、CLI、符号/数值/仿真三类分析路径都已具备。 |

### 形式化问题与性质

1. `PRISM` 真正补上的不是单个算法，而是“统一模型语言 + 统一性质语言 + 多后端分析”的平台骨架。
2. 它把 rewards/costs 提升为一等对象，这对后续控制系统的能耗、失败前期望步数等分析很重要。
3. 对本文库而言，它是后来 `PRISM 4.0`、`PRISM-games`、`JANI` 与 `Storm` 这条 quantitative 工具生态的早期锚点。

## 构造方式与承载格式

### 建模入口

典型建模入口是：

1. 以 modules + guarded commands 描述系统。
2. 用有限范围变量承载离散状态。
3. 用同步动作和并行组合描述并发交互。
4. 用 rewards 描述能耗、消息丢失或时间消耗等数量指标。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PRISM` 文本建模语言。
2. `PCTL/CSL` 风格性质文本。
3. 导出的 transition matrix 与 state space。
4. 面向 `Matlab / ETMCC / MRMC` 的若干外部格式。

### 交换与互操作

论文强调了两种互操作方式：

1. 模型可导出为矩阵和状态空间文本，供外部工具复用。
2. 其他形式主义也可翻译导入到 `PRISM`。

## 配套基础设施

- 建模/编辑工具：GUI 与命令行双入口。
- 解析/交换/元模型支持：统一模型/性质语言与多种导入导出格式。
- 仿真/执行支持：支持 manual exploration 与 Monte-Carlo discrete-event simulation。
- 验证/分析支持：graph-based reachability、数值求解、BDD/MTBDD 式符号求解与 distributed simulation。
- 代码生成/转换支持：主线不是代码生成，而是模型导入导出与分析流程复用。
- 标准化或社区生态：开源发布、跨平台支持、案例仓库和文档共同构成长期概率验证生态。

## 适用场景与需求前提

### 适用场景

适合随机化协议、分布式算法、可靠性分析、功耗管理以及任何需要问“概率是多少”“长期频率是多少”“期望代价是多少”的离散概率系统。

### 需求前提

1. 系统可落成有限状态概率模型。
2. 数据域可有限化到建模语言允许的范围。
3. 需求关心概率、稳态或期望代价，而非仅仅布尔可达性。
4. 若做大规模分析，团队需要接受符号/数值求解器的建模约束。

### 不适用或高成本场景

如果系统主体是连续物理动力学、重度层次状态语义或无穷数据域，直接使用这条早期 `PRISM` 路线会很吃力。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，这篇 2006 论文是 `PRISM` 的平台母线，而后者是其概率实时扩展节点；相对 [iscas-mc-a-web-based-probabilistic-model-checker/desc.md](../iscas-mc-a-web-based-probabilistic-model-checker/desc.md)，`ISCAS MC` 复用了 `PRISM` 风格输入，但更偏 Web 服务；相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)，`Storm` 更现代更模块化，而这里是更早的统一平台奠基条目。

## 与本研究的关系

### 对 Project 1 的价值

1. 它表明状态机文库不应只围绕 deterministic verification，也要保留 probability/reward 这类后端接口。
2. 若需求侧出现可靠性、能耗、失败前期望耗时等非布尔目标，`PRISM` 路线提供了成熟的分析后端。
3. 它也是后续 `JANI` 等 interchange layer 的重要前史。

### 作为目标形式主义还是中间表示

对大多数控制需求，它更像概率验证后端；对本身就是概率系统的对象，也可以是直接建模目标。

## 重要的相关工作

- [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：`PRISM` 向概率实时方向的扩展。
- [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：新一代概率模型检查平台。
- [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：后续 quantitative 互操作层。
- [vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md](../vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md)：与 `PRISM` 的精确数值路线形成统计模型检查对照。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`DTMC / MDP / CTMC / PRISM`
- 论文角色：probabilistic model-checking platform / guarded-command based quantitative verification environment
- 核心功能：统一概率模型建模、`P/S/R` 性质分析与数值/符号/仿真求解
- 关键特性：modules、guarded commands、rewards、GUI/CLI、Monte-Carlo simulation
- 构造方式：`Reactive Modules` 风格文本模型 + `PCTL/CSL` 性质 + 多引擎分析
- 基础设施：GUI、CLI、symbolic engines、numeric solvers、simulation manager、导入导出格式
- 适用场景：随机化协议、可靠性与能耗分析、一般离散概率系统验证
- 需求前提：系统需有限状态化并需要概率/稳态/期望代价结果
- 状态：🟢
