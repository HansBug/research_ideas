# SCOTS：符号控制器综合工具 / SCOTS: A Tool for the Synthesis of Symbolic Controllers

## 基本信息

- 标题：SCOTS: A Tool for the Synthesis of Symbolic Controllers
- 中文标题：SCOTS：符号控制器综合工具
- 作者：Matthias Rungger，Majid Zamani
- 发表：*Proceedings of the 19th International Conference on Hybrid Systems: Computation and Control*，pp. 99-104，2016
- DOI：`10.1145/2883817.2883834`
- 链接：https://doi.org/10.1145/2883817.2883834
- 形式主义：`symbolic control / discrete abstractions / feedback refinement relation / SCOTS`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：nonlinear-control symbolic-abstraction toolbox for reachability/invariance synthesis
- 工具/实现获取方式：原文明确说明工具与实验可从作者团队页面获取；当前公开入口可通过归档页面 `https://webarchiv.typo3.tum.de/EI/hcs/software/scots/` 访问。
- 标准/格式获取方式：主体承载是 `C++` library、uniform-grid symbolic model、polytopes/ellipsoids、Matlab interface 与 controller files；不是中立行业交换标准。

## 简报

`SCOTS` 补的是控制系统文献里非常重要的一类基础设施：给定非线性控制系统的微分方程、采样时间和离散化参数，自动构造 symbolic model，再用固定点算法为 reachability / invariance 规格综合静态控制器。相比把 `Timed Automata` 或 `LTL` 直接当控制模型，`SCOTS` 更贴近连续控制对象本身，它从 plant dynamics 出发，靠 feedback refinement relation 把抽象控制器安全地下放回原系统。

- 形式主义定位：面向非线性控制系统 symbolic abstraction 与 controller synthesis 的工具基础设施。
- 构造方式简述：连续 plant -> sampled system -> uniform-grid symbolic model -> fixed-point synthesis -> abstract controller -> refinement back to plant。
- 基础设施与场景简述：依托 `C++` core、Matlab interface、growth bounds、uniform grids、polytopes/ellipsoids 和 feedback refinement relation，服务非线性系统的 reachability / invariance 控制。

```text
differential-equation plant -> sampled system -> symbolic model on uniform grid -> fixed-point synthesis -> refined static controller
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. perturbed nonlinear sampled systems；
2. symbolic models / discrete abstractions；
3. feedback refinement relation (`FRR`)；
4. reachability 与 invariance 规格；
5. `SCOTS` 的 `C++/Matlab` 工具链。

### 核心抽象

论文把 plant 与 symbolic model 都统一成 simple system：

$$
S_1 = (X_1, U_1, F_1), \qquad S_2 = (X_2, U_2, F_2)
$$

上式中的符号逐项解释如下：

1. `$S_1$` 是原始 plant。
2. `$X_1$` 是 plant 状态空间，`$U_1$` 是输入集合。
3. `$F_1$` 给出在输入下的后继状态集合。
4. `$S_2$` 是由离散化得到的 symbolic model。
5. `$X_2$` 通常是 uniform-grid cells，`$U_2$` 是有限输入子集。

`SCOTS` 的核心正确性基础是 feedback refinement relation：

$$
Q \subseteq X_1 \times X_2
$$

上式中的符号逐项解释如下：

1. `$Q$` 把连续 plant 状态映到抽象 cell。
2. 若 `$(x_1, x_2) \in Q$`，说明抽象状态 `$x_2$` 可安全代表 plant 状态 `$x_1$`。
3. 论文给出两条关键条件保证抽象控制器可下放回原系统。

这两条条件可直接写成：

$$
U_{S_2}(x_2) \subseteq U_{S_1}(x_1)
$$

$$
u \in U_{S_2}(x_2) \Rightarrow Q(F_1(x_1, u)) \subseteq F_2(x_2, u)
$$

上式中的符号逐项解释如下：

1. 第一式说明抽象模型允许的输入不能超出 plant 真正可接受的输入。
2. 第二式说明：若在抽象模型中选择了输入 `$u$`，则 plant 的所有真实后继经量化后都必须落在抽象后继中。
3. 这就是 refinement 正确性的根本来源。

论文的连续系统骨架为：

$$
\dot{\xi}(t) \in f(\xi(t), u) + [-w, w]
$$

上式中的符号逐项解释如下：

1. `$\xi(t)$` 是连续状态。
2. `$u$` 是控制输入。
3. `$f$` 是系统动力学右端项。
4. `$w$` 是扰动边界，表示系统存在有界不确定性。

### 一个最小例子与通俗解释

一个最小直觉例子可以这样理解：

1. 你有一个连续状态空间里的非线性装置，例如某个电力电子或机动系统。
2. 你把状态空间切成一个个小网格格子，把可选控制输入也离散化。
3. 对每个格子和输入，`SCOTS` 计算“系统下一步可能跑到哪些格子”。
4. 然后它在这个有限图上做 reachability 或 safety 的 fixed-point computation，再把得到的控制策略映回真实系统。

通俗地说，`SCOTS` 就像“先把连续世界刻成有保证的离散地图，再在地图上综合控制器”。

### 运行 / 接受 / 转移语义

论文给出 sampled system 的定义：若在输入 `$u$` 下从 `$x$` 出发，经采样时间 `$\tau$` 后到达 `$x'$`，则 `$x' \in F_1(x,u)$`。为合成控制器，论文定义 predecessor：

$$
\mathrm{pre}(Y_2) = \{x_2 \in X_2 \mid \exists u \in U_{S_2}(x_2),\ F_2(x_2, u) \subseteq Y_2\}
$$

上式中的符号逐项解释如下：

1. `$Y_2$` 是抽象状态集合。
2. `$\mathrm{pre}(Y_2)$` 表示存在某个输入，使得所有抽象后继都留在 `$Y_2$` 中的状态。
3. 这就是抽象控制综合里“系统能确保下一步进入安全区域”的核心算子。

在此基础上，论文定义了两个固定点骨架：

$$
\kappa_G(Y) = \mathrm{pre}(Y) \cup Z_2, \qquad \hat{G}(Y) = \mathrm{pre}(Y) \cap Z_2
$$

上式中的符号逐项解释如下：

1. `$Z_2$` 是目标集或安全集的抽象表示。
2. `$\kappa_G$` 用于 reachability synthesis 的最小固定点。
3. `$\hat{G}$` 用于 invariance synthesis 的最大固定点。
4. `SCOTS` 直接在工具中提供这两类固定点计算。

### 语义边界

1. `SCOTS` 关注 sampled nonlinear control systems，不是通用 timed-automata verifier。
2. 原论文原生支持 reachability 与 invariance，两者都对应 memoryless/static controllers。
3. 它依赖 growth bounds、uniform grids 和有限输入抽样，因此会受到离散化维度爆炸影响。
4. 论文重点是 symbolic abstraction 与 controller refinement，不是 richer temporal logic synthesis。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| system 骨架 | `$S_1 = (X_1, U_1, F_1),\ S_2 = (X_2, U_2, F_2)$` | 统一表示连续 plant 与抽象模型。 |
| `FRR` | `$Q \subseteq X_1 \times X_2$` | 保证抽象控制器可安全下放。 |
| 输入保守性 | `$U_{S_2}(x_2) \subseteq U_{S_1}(x_1)$` | 抽象层不能虚构 plant 没有的控制能力。 |
| 后继覆盖 | `$Q(F_1(x_1,u)) \subseteq F_2(x_2,u)$` | 抽象转移必须覆盖真实演化。 |
| predecessor | `$\mathrm{pre}(Y_2) = \{x_2 \mid \exists u,\ F_2(x_2,u)\subseteq Y_2\}$` | fixed-point synthesis 的核心算子。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 连续 plant 被离散成 uniform-grid symbolic states。 |
| 事件 / 触发 | 中等支持 | 更像采样控制输入，而不是事件驱动协议。 |
| 守卫 / 数据 | 中等支持 | 核心是连续状态区间和几何集合，不是程序变量守卫。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 弱支持 | 原文主要面向单 plant 抽象，而非组件并发。 |
| 时间约束 | 中等支持 | 有采样时间 `\tau`，但不是 timed-automata clocks。 |
| 连续动态 / 随机性 | 很强 | 非线性微分方程与扰动边界是主对象。 |
| 可执行 / 可验证性 | 很强 | symbolic model construction、fixed-point synthesis、Matlab simulation 都已工程化。 |

### 形式化问题与性质

1. `SCOTS` 的根本价值在于把“抽象建模 + controller synthesis + refinement”做成一条可重复工作流。
2. `FRR` 是它区别于纯启发式离散化的关键，因为它提供了严格可下放保证。
3. 对文库而言，它是 symbolic-control 工具母线，而不是新的主树节点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 连续动力学 `f(x,u)`；
2. 扰动与测量误差边界；
3. 采样时间 `\tau`；
4. uniform-grid 参数；
5. 目标/安全集的 polytope 或 ellipsoid 定义。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `C++` classes：`SymbolicSet`、`SymbolicModel`、`FixedPoint`；
2. grid cells 与 overflow symbols；
3. reachability / invariance fixed-point computations；
4. Matlab interface for simulation and visualization。

### 交换与互操作

1. `SCOTS` 不是通用交换标准，更像 `C++/Matlab` toolbox。
2. 规格中的目标集和安全集以 polytopes/ellipsoids 给出。
3. 后续网络化扩展 `SENSE` 直接复用 `SCOTS` 产生的 plant symbolic model。

## 配套基础设施

- 建模/编辑工具：主要是 `C++` toolbox 与 Matlab front-end。
- 解析/交换/元模型支持：uniform-grid cells、polytopes、ellipsoids、controller data structures；原文未提供中立 exchange standard。
- 仿真/执行支持：Matlab interface 支持 closed-loop simulation 和抽象状态空间可视化。
- 验证/分析支持：symbolic model construction、reachability/invariance synthesis、fixed-point routines。
- 代码生成/转换支持：论文重点在 controller synthesis 与 refinement，不在嵌入式代码生成。
- 标准化或社区生态：官方工具页、`C++` 实现、Matlab interface，以及同系列 symbolic-control 理论共同构成生态。

## 适用场景与需求前提

### 适用场景

适合非线性控制系统、带扰动的 sampled-data plants、需要严格 reachability / safety 保证的符号控制问题。

### 需求前提

1. 系统需能写成连续动力学并在固定采样周期下观察。
2. 输入集合需要可有限离散化。
3. 目标/安全集需可表示为 polytopes 或 ellipsoids。
4. 需要接受状态空间离散化带来的维度代价。

### 不适用或高成本场景

若需求主体是一般 `LTL`、复杂并发协议或超高维连续系统，`SCOTS` 的网格离散化会变得昂贵或不自然。

## 与相邻形式主义的关系

相对 [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md) 与 [dryvr-data-driven-verification-and-compositional-reasoning-for-automotive-systems/desc.md](../dryvr-data-driven-verification-and-compositional-reasoning-for-automotive-systems/desc.md)，`SCOTS` 更强调可综合控制器而不仅是 reachability/verification；相对 [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)，`Synthia` 是 timed-automata/game route，`SCOTS` 则直接从连续 plant 动力学做 symbolic abstraction；相对 [sense-abstraction-based-synthesis-of-networked-control-systems/desc.md](../sense-abstraction-based-synthesis-of-networked-control-systems/desc.md)，`SENSE` 是在 `SCOTS` plant symbolic model 之上继续把网络非理想因素纳入控制综合。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明控制系统状态机/抽象模型不一定要从离散逻辑出发，也可以从连续 plant 严格抽象得到。
2. 如果未来研究要把需求生成的控制结构接到物理系统验证/综合后端，`SCOTS` 提供了很强的下游基础设施。
3. `FRR` 思路对“生成模型后如何保证可部署”尤其重要。

### 作为目标形式主义还是中间表示

更像面向物理控制问题的抽象后端与合成基础设施，不是需求侧直接交付给用户的前端建模语言。

### 对需求到模型生成的启发

1. 面向 CPS 时，离散状态机生成后还需要接连续 plant abstraction 才能落地。
2. “抽象模型正确但能否下放回 plant”应成为研究中的单独问题。
3. 可把 `FRR` 看作需求模型与部署模型之间的一种可信映射约束。

### 现实限制

网格化与状态空间爆炸仍是主要工程瓶颈；对高维系统，`SCOTS` 更适合作为方法锚点和中等规模 backend。

## 重要的相关工作

### 奠基或前身工作

1. symbolic models / discrete abstractions for nonlinear control。
2. feedback refinement relations：论文的理论骨架。

### 同类型或同家族工作

1. `Pessoa`、`CoSyMA`：论文在引言中直接比较的同类符号控制工具线。
2. [sense-abstraction-based-synthesis-of-networked-control-systems/desc.md](../sense-abstraction-based-synthesis-of-networked-control-systems/desc.md)：网络化控制系统扩展。

### 标准 / 格式 / 工具链工作

1. Matlab interface：原文强调的 simulation/visualization bridge。
2. polytope/ellipsoid set representation：目标/安全集输入主承载。

### 与本研究关系最紧的工作

1. [sense-abstraction-based-synthesis-of-networked-control-systems/desc.md](../sense-abstraction-based-synthesis-of-networked-control-systems/desc.md)
2. [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`symbolic control / discrete abstractions / feedback refinement relation / SCOTS`
- 论文角色：nonlinear-control symbolic-abstraction toolbox for reachability/invariance synthesis
- 核心功能：从连续 plant 自动构造 symbolic model，并为 reachability / invariance 规格综合可下放控制器
- 关键特性：`FRR`、uniform grids、growth bounds、fixed-point synthesis、Matlab simulation
- 构造方式：continuous plant -> sampled system -> symbolic model -> fixed-point controller -> refinement
- 基础设施：`C++` toolbox + Matlab interface + geometric set representations
- 适用场景：非线性 sampled-data control、symbolic controller synthesis、带扰动物理系统
- 归类理由：论文主体是工具箱、抽象构造和控制器下放机制，明显属于 symbolic-control 基础设施条目。
