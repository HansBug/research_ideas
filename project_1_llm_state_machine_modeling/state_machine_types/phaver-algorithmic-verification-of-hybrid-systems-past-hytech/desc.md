# PHAVer：超越 HyTech 的混成系统算法验证器 / PHAVer: algorithmic verification of hybrid systems past HyTech

## 基本信息

- 标题：PHAVer: algorithmic verification of hybrid systems past HyTech
- 中文标题：PHAVer：超越 HyTech 的混成系统算法验证器
- 作者：Goran Frehse
- 发表：*International Journal on Software Tools for Technology Transfer*，10(3):263-279，2008
- DOI：`10.1007/S10009-007-0062-X`
- 链接：https://www-verimag.imag.fr/~frehse/frehse_sttt2008.pdf
- 形式主义：`Piecewise-Constant-Derivative / Affine Hybrid Automata / PHAVer`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：exact-safety verifier / reachability algorithm
- 工具/实现获取方式：原文明确给出 `PHAVer` 的 Verimag 主页与发行入口，工具作为 `HyTech` 之后的新一代 hybrid verifier 发布。
- 标准/格式获取方式：承载方式是 `PHAVer` 的文本式 hybrid automata 输入与约束脚本；原文没有给独立于工具的中立交换格式。

## 简报

这篇论文的核心价值，不是再讲一遍 `Hybrid Automata` 理论，而是把 `HyTech` 之后长期受限的精确可达性验证重新做成可用工具。`PHAVer` 直接瞄准“带分段常值导数界的混成系统安全验证”，同时对更一般的 affine dynamics 采用 on-the-fly over-approximation、location splitting 和 exact arithmetic，把很多原本算不动的 benchmark 真正推进到可验证范围。

- 形式主义定位：面向 `Piecewise-Constant-Derivative` 与 affine hybrid systems 的精确/保守可达性验证路线，而不是新的混成自动机本体。
- 构造方式简述：输入 hybrid automata、线性/仿射 flow predicates、jump relations 与 invariants，再围绕 reachability fixed point、polyhedral operations 和 splitting heuristics 做验证。
- 基础设施与场景简述：依托 `PHAVer` 命令行工具、Verimag 发布页、exact arithmetic polyhedra 与 compositional reachability，服务导航 benchmark、互斥协议、tunnel diode 等 hybrid safety 场景。

```text
hybrid model -> linear/affine predicates + invariants -> reachability fixed point + polyhedral splitting -> safe / unsafe / conservative over-approximation
```

## 形式主义定义与核心对象

### 定义对象

论文直接把 `PHAVer` 所处理的输入对象写成一类 hybrid automata：

1. 连续变量 `X`，并区分 controlled / input / output variables。
2. locations 与 location invariants。
3. 同步标签与带 jump relation 的 discrete transitions。
4. `Flow` 谓词，用于给每个 location 指派导数约束。
5. 初始状态集合 `Init`。

### 核心抽象

原文给出的混成自动机骨架为：

$$
H = (Loc, (X, O, C), Lab, Edg, Flow, Inv, Init)
$$

上式中的符号逐项解释如下：

1. `Loc` 是 locations 集合。
2. `X` 是连续变量集合。
3. `C` 是 controlled variables，`O` 是其中被指定为 outputs 的子集。
4. `Lab` 是同步标签集合，包含 stutter label `\tau`。
5. `Edg` 是离散转移集合，每条边都带 jump relation。
6. `Flow` 为每个 location 指派流动谓词。
7. `Inv` 是所有行为必须始终满足的 invariant 集合。
8. `Init` 是初始状态集合。

论文随后把 `PHAVer` 的可处理约束写成线性形式：

$$
\sum_i \alpha_i x_i + \beta \triangleleft 0
$$

上式中的符号逐项解释如下：

1. `x_i` 是变量。
2. `\alpha_i` 与 `\beta` 是整数常数。
3. `\triangleleft` 表示 `<` 或 `\le`。
4. 这些线性约束共同构成 invariants、初始条件、jump relations 与部分 flow predicates 的基础。

工具算法最核心的对象不是单条 run，而是 symbolic states 与 fixed-point reachability：

$$
R_{k+1} := R_k \cup post_c(post_d(R_k))
$$

上式中的符号逐项解释如下：

1. `R_k` 是第 `k` 轮 reachability 迭代得到的 symbolic-state 集合。
2. `post_d` 是 discrete post-operator。
3. `post_c` 是 continuous post-operator。
4. 不动点近似的质量，直接决定 `PHAVer` 能否精确或保守地回答安全问题。

### 一个最小例子与通俗解释

论文中既有 timing-based mutual exclusion，也有导航 benchmark。用最小直觉来讲，可以把它想成这样：

1. 一个 location `Cruise` 里，位置 `x` 的导数不是固定值，而是落在一个线性可描述的区间或多面体里。
2. 只要 `x` 还在 invariant 给定的安全区间内，系统就可以连续演化。
3. 当 guard 满足时，系统通过 jump relation 切到另一个 location，并可能重置一部分变量。
4. `PHAVer` 不去采样几条轨迹，而是用 polyhedra 计算“整块可达状态”，再判断这整块是否会触碰 bad set。

通俗地说，`PHAVer` 像“会做精确多面体几何的混成状态机验证器”。你给它 modes、线性约束、仿射流动和离散跳转，它回给你的是可达区域，而不是几条偶然仿真曲线。

### 运行 / 接受 / 转移语义

论文把状态写成 `(l,v)`，其中 `l` 是 location，`v` 是变量 valuation。连续演化来自 `Flow`，离散跳转来自 `(l,a,\mu,l')` 形式的边，而可达性则通过 symbolic-state fixed point 计算：

$$
R_0 = post_c(Init), \quad R_{k+1} := R_k \cup post_c(post_d(R_k))
$$

上式中的符号逐项解释如下：

1. `Init` 是初始状态集合。
2. `post_c(Init)` 先把初始位置在连续时间上展开。
3. `post_d(R_k)` 计算一次离散跳转后继。
4. `post_c(post_d(R_k))` 再把这些后继做时间流逝扩张。
5. 整个迭代持续到达到不动点或用户接受的保守近似为止。

对 compositional modeling，原文还给出并行组合：

$$
H = H_1 \parallel H_2
$$

其核心含义是：兼容的子 automata 可以同步组合，而非可达性结论可以模块化地向整体系统传播。

### 语义边界

这篇论文的边界说得很清楚：

1. `PHAVer` 最擅长的是 piecewise-constant-derivative 或 affine hybrid systems。
2. 对 affine dynamics，它依赖 on-the-fly over-approximation 与 state-space splitting。
3. invariants 默认需要在每个 location 上是 convex。
4. 若连续动力学太非线性，或者必须依赖数值仿真而非 polyhedral over-approximation，`PHAVer` 就不再是最自然的入口。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| hybrid automaton 骨架 | `$H = (Loc, (X, O, C), Lab, Edg, Flow, Inv, Init)$` | 固定 `PHAVer` 的输入对象。 |
| 线性约束 | `$\sum_i \alpha_i x_i + \beta \triangleleft 0$` | invariants、guards 与 jump predicates 的基础表示。 |
| reachability fixed point | `$R_{k+1} := R_k \cup post_c(post_d(R_k))$` | 工具求解安全问题的核心框架。 |
| 并行组合 | `$H = H_1 \parallel H_2$` | 支撑 compositional reachability。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | locations 是离散骨架。 |
| 事件 / 触发 | 强支持 | 同步标签和 jump relations 明确存在。 |
| 守卫 / 数据 | 很强 | 线性 guards、jump predicates、invariants 都是第一等对象。 |
| 层次 | 弱支持 | 主体不是层次状态机，而是 flat hybrid automata 的组合。 |
| 并发 / 同步 | 部分支持 | 通过 parallel composition 处理兼容 automata。 |
| 时间约束 | 很强 | 连续时间直接进入 flow predicates。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 适合 piecewise-constant-derivative 与 affine flow，不涉及概率。 |
| 可执行 / 可验证性 | 很强 | exact arithmetic、reachability、splitting、approximation 都具备。 |

### 形式化问题与性质

1. `PHAVer` 的重点是“symbolic reachability 能否真正落地”，而不是单纯重述 hybrid automata 理论。
2. piecewise-constant derivative bounds 解释了它为什么比 `HyTech` 更能处理复杂但仍可线性约束的系统。
3. 对 affine dynamics 的 on-the-fly over-approximation，是它从“理论可判定”走向“工程可算”的关键桥梁。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 写 hybrid automata 的 textual model。
2. 用线性谓词表达 invariants、initial states 与 jump relations。
3. 对 affine dynamics 明确给出 `X \cup \dot X` 上的线性约束。
4. 由工具执行 reachability、splitting 与 over-approximation。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PHAVer` 自身的文本式 hybrid automata 输入。
2. 线性/仿射谓词与 jump relations。
3. exact arithmetic polyhedra。
4. 用户给定的 splitting constraints 与分析参数。

### 交换与互操作

这篇论文的互操作重点不在开放标准，而在与既有 hybrid verification 生态的承接：

1. 输入风格延续并超出 `HyTech` 可处理的线性混成建模方式。
2. compositional reachability 允许分模块分析。
3. affine systems 可通过 conservatively splitting 的方式被拉回可分析子类。

## 配套基础设施

- 建模/编辑工具：以 `PHAVer` 文本输入与命令行为主，原文明确给出工具主页。
- 解析/交换/元模型支持：支持 hybrid automata 的 textual predicates；无中立交换标准。
- 仿真/执行支持：主体是 symbolic reachability，不强调高保真仿真器。
- 验证/分析支持：exact arithmetic、discrete/continuous post、splitting、conservative over-approximation、safety verification。
- 代码生成/转换支持：原文不强调代码生成；重点是模型收束与验证。
- 标准化或社区生态：Verimag 发布页、benchmark 与 `HyTech` 后继关系构成其主要生态。

## 适用场景与需求前提

### 适用场景

适合需要验证混成安全性的场景，尤其是 continuous dynamics 还能被 piecewise-constant 或 affine constraints 收束的控制与嵌入式系统。

### 需求前提

1. 连续动力学应能写成线性或仿射 predicate，或至少能被保守分割近似到这一类。
2. invariants 最好是 convex。
3. 目标问题主要是 safety / reachability，而不是概率、学习或纯数值性能。
4. 建模者能够接受 polyhedral 级别的符号化输入，而不是只提供仿真模型。

### 不适用或高成本场景

若系统核心是强非线性 ODE、复杂数值积分或黑盒仿真，`PHAVer` 的多面体路线会很快吃力。

## 与相邻形式主义的关系

相对 [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)，`PHAVer` 明确是在“HyTech 之后”扩可处理规模与精度；相对 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)，它仍更偏 exact / polyhedral symbolic verification；相对 [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)，它不走 Taylor-model flowpipe，而是坚持在线性/仿射约束空间里求 reachability。

## 与本研究的关系

### 对 Project 1 的价值

它证明了当 `project_1` 生成的状态机需要进入 hybrid verification 后端时，“把需求收束成可判定混成子类”是一条非常现实的落地路线。

### 作为目标形式主义还是中间表示

更适合作为验证后端的专用落点，而不是仓库里的通用交付格式。

### 对需求到模型生成的启发

1. 若要把自然语言需求送进 `PHAVer`，必须显式产出 locations、flow predicates、jump relations 与 invariants。
2. 连续动力学是否可被线性/仿射约束化，直接决定验证闭环能否走通。
3. “生成 - 验证 - 修复” 中的修复，不只是改 guards，也可能是把模型收束到更可分析的子类。

### 现实限制

`PHAVer` 能力很强，但前提也很硬：它要的是结构化、可多面体化的 hybrid model，而不是黑盒仿真器。

## 重要的相关工作

- [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：`PHAVer` 明确要超越的上一代 hybrid verifier。
- [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)：后续更强调 scalability 的 hybrid verification platform。
- [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)：更偏 non-linear flowpipe 的后续路线。
- [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)：混成自动机模型本体母线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Piecewise-Constant-Derivative / Affine Hybrid Automata / PHAVer`
- 论文角色：exact-safety verifier / reachability algorithm
