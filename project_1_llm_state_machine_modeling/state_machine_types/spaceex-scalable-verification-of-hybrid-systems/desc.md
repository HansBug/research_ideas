# SpaceEx：可扩展混成系统验证平台 / SpaceEx: Scalable Verification of Hybrid Systems

## 基本信息

- 标题：SpaceEx: Scalable Verification of Hybrid Systems
- 中文标题：SpaceEx：可扩展混成系统验证平台
- 作者：Goran Frehse，Colas Le Guernic，Alexandre Donze，Scott Cotton，Rajarshi Ray，Olivier Lebeltel，Rodolfo Ripado，Antoine Girard，Thao Dang，Oded Maler
- 发表：*Computer Aided Verification*，pp. 379-395，2011
- DOI：`10.1007/978-3-642-22110-1_30`
- 链接：https://www-verimag.imag.fr/~tdang/Papers/CAV2011.pdf
- 形式主义：`Affine / Piecewise-Affine Hybrid Systems / SpaceEx`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：hybrid reachability platform / scalable verifier
- 工具/实现获取方式：原文明确给出 `http://spaceex.imag.fr`，并说明 examples 与 tool 都可从该平台获取。
- 标准/格式获取方式：原文强调 `model file + configuration file + output files` 的平台化工作流，并配有 web UI 与 model editor；未给独立于 `SpaceEx` 的中立交换标准。

## 简报

这篇论文的重点，是把 hybrid verification 从“能算一些小例子”推进到真正可扩展的平台。`SpaceEx` 一边保留 hybrid automata 的经典语义骨架，一边把分析核心、web interface 和 model editor 组织成完整平台，并用 support functions、template polyhedra、variable time steps 和 clustering 把高维 reachability 做到更可用的规模。

- 形式主义定位：面向 affine / piecewise-affine hybrid systems 的 reachability platform，而不是新的混成自动机理论。
- 构造方式简述：输入 model file 与 configuration file，平台内部围绕 support functions、template hulls 和 variable-step flowpipe algorithm 做 over-approximate reachability。
- 基础设施与场景简述：依托 command-line analysis core、web interface、graphical model editor 与 benchmark bundle，服务高维混成系统验证与可视化分析。

```text
hybrid model -> model/config files -> support-function reachability + variable-step flowpipe -> graphical visualization / safety result
```

## 形式主义定义与核心对象

### 定义对象

论文明确把 `SpaceEx` 的输入对象固定为 hybrid automaton：

1. 连续变量 `Var`。
2. locations 与 invariants。
3. 带 labels 的 transitions、guards 与 assignments。
4. 初始状态集合 `Init`。
5. 每个 location 上的连续动力学 `Flow`。

### 核心抽象

原文直接给出混成自动机骨架：

$$
H = (Loc, Var, Lab, Inv, Flow, Trans, Init)
$$

上式中的符号逐项解释如下：

1. `Loc` 是 locations 集合。
2. `Var` 是连续变量集合。
3. `Lab` 是 transition labels 集合。
4. `Inv` 为每个 location 指派 invariant。
5. `Flow` 为每个 location 指派连续动力学。
6. `Trans` 是离散转移集合。
7. `Init` 是初始状态集合。

对论文关注的连续动力学，原文写成：

$$
\dot{x}(t) = Ax(t) + u(t), \quad u(t) \in U
$$

上式中的符号逐项解释如下：

1. `x(t)` 是时间 `t` 下的连续状态向量。
2. `A` 是线性系统矩阵。
3. `u(t)` 是非确定输入。
4. `U` 是闭且有界的凸输入集合。

离散赋值则写成：

$$
x' = Rx + w, \quad w \in W
$$

上式中的符号逐项解释如下：

1. `R` 是线性重置矩阵。
2. `x'` 是离散跳转后的状态。
3. `w` 是非确定赋值输入。
4. `W` 是闭且有界的凸集合。

算法层的骨架是 reachability fixed point：

$$
R_0 = post_c(Init), \quad R_{k+1} := R_k \cup post_c(post_d(R_k))
$$

上式中的符号逐项解释如下：

1. `post_d` 是 discrete post-operator。
2. `post_c` 是 continuous post-operator。
3. `R_k` 是第 `k` 轮 symbolic-state 集合。
4. 这个 fixed point 决定了平台最终的 reachable states。

### 一个最小例子与通俗解释

论文中的 benchmark 包含 filtered oscillator 和高维控制系统。把最小直觉压缩一下，就是：

1. 在某个 location 里，系统按线性微分方程连续演化。
2. 只要状态还在 invariant 里，就继续沿着 flow 前进。
3. 一旦 guard 成立，就触发离散跳转，并按 `x' = Rx + w` 更新变量。
4. `SpaceEx` 不会只取几个时间步采样，而是算一串 over-approximate flowpipe，把整片可达区域包出来。

通俗地说，`SpaceEx` 像“专门给高维 hybrid system 画安全边界的 reachability 平台”。你关心的不是单条轨迹，而是“这一大团状态未来会扩成什么样”。

### 运行 / 接受 / 转移语义

论文把每个具体状态写成 `(l,x)`，其中 `l` 是 location，`x` 是连续变量值。对于连续部分，`SpaceEx` 定义：

$$
Reach_{t_1,t_2}(X)
$$

上式中的符号逐项解释如下：

1. `X` 是某一时刻的初始连续状态集合。
2. `Reach_{t_1,t_2}(X)` 表示从 `X` 出发，在 `[t_1,t_2]` 时间段内所有可达状态。
3. 该算子是 flowpipe construction 的核心目标。

variable time-step flowpipe 算法则写成：

$$
\Psi_{k+1} = \Psi_k \oplus e^{At_k}\Psi_{\delta_k}(U), \qquad
\Omega_k = e^{At_k}\Omega_{[0,\delta_k]}(X_0,U) \oplus \Psi_k
$$

以及：

$$
Reach_{0,T}(X_0) \subseteq \bigcup_{k=0}^{N-1} \Omega_k
$$

上式中的符号逐项解释如下：

1. `\delta_k` 是第 `k` 段时间步长。
2. `t_k` 是前 `k` 段累积时间。
3. `\Psi_k` 近似输入 `U` 累积造成的可达偏移。
4. `\Omega_k` 是第 `k` 段 flowpipe over-approximation。
5. 整个 flowpipe 并集覆盖 `[0,T]` 内所有可达状态。

### 语义边界

这篇论文的边界也很清楚：

1. `SpaceEx` 主打的是 affine / piecewise-affine hybrid systems。
2. 可达集是 over-approximation，不承诺对一般 hybrid systems 的 exact verification。
3. invariants、intersections 和 assignments 的处理高度依赖 support-function 与 template-polyhedra 近似。
4. 若系统主要是强非线性 ODE，则需要转向 `Flow*` 一类工具。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| hybrid automaton 骨架 | `$H = (Loc, Var, Lab, Inv, Flow, Trans, Init)$` | 固定 `SpaceEx` 的输入对象。 |
| 连续动力学 | `$\dot{x}(t) = Ax(t) + u(t),\ u(t)\in U$` | 工具主打的 affine dynamics。 |
| 离散赋值 | `$x' = Rx + w,\ w\in W$` | reset/assignment 的平台化表示。 |
| reachability fixed point | `$R_{k+1} := R_k \cup post_c(post_d(R_k))$` | 高层算法骨架。 |
| flowpipe 覆盖 | `$Reach_{0,T}(X_0) \subseteq \bigcup_k \Omega_k$` | 平台返回的是可达集 over-approximation。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | locations 是离散骨架。 |
| 事件 / 触发 | 强支持 | labeled transitions、guards 与 assignments 明确存在。 |
| 守卫 / 数据 | 很强 | guards、assignments、template intersections 都是核心。 |
| 层次 | 部分支持 | model editor 支持 nested components。 |
| 并发 / 同步 | 部分支持 | 通过组件组合处理复杂系统，但重心不在协议层。 |
| 时间约束 | 很强 | 连续时间直接体现在 flowpipe computation 中。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 适合 affine / piecewise-affine dynamics。 |
| 可执行 / 可验证性 | 很强 | analysis core、web UI、model editor 三件套齐全。 |

### 形式化问题与性质

1. `SpaceEx` 的标志性点不是单一算法，而是“reachability algorithm + platform engineering”的合体。
2. support functions 与 template polyhedra 的混合表示，是它兼顾效率与交集/包含判断的关键。
3. variable time steps 与 clustering 是它从 `PHAVer` 一代走向 scalability 的主要工程改进。

## 构造方式与承载格式

### 建模入口

原文给出的典型入口是：

1. 写 model file。
2. 再写 configuration file，指定 initial states、scenario 与分析参数。
3. 用 web interface 启动分析，或直接调用 analysis core。
4. 必要时在 model editor 中图形化构造 nested hybrid components。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `SpaceEx` model file。
2. configuration file。
3. analysis core 输出的一系列 result files。
4. web interface / model editor 对这些文件的可视化封装。

### 交换与互操作

这篇论文的互操作重点是平台内部接口，而不是开放中立标准：

1. analysis core、web interface 与 model editor 三层分离。
2. 同一模型可通过命令行或 web UI 使用。
3. nested-component editor 负责把复杂 hybrid system 组织成可分析结构。

## 配套基础设施

- 建模/编辑工具：graphical model editor，支持 nested components。
- 解析/交换/元模型支持：model/configuration files 与 analysis core 工作流；无中立交换标准。
- 仿真/执行支持：主体是 symbolic / set-based analysis，不是仿真器。
- 验证/分析支持：support functions、template polyhedra、variable time steps、clustering、fixed-point reachability。
- 代码生成/转换支持：原文不强调代码生成；核心是 analysis platform。
- 标准化或社区生态：`spaceex.imag.fr`、web UI、examples 与 benchmark 共同构成稳定工具生态。

## 适用场景与需求前提

### 适用场景

适合高维混成系统、线性控制系统、oscillator、LTI plant 与其他能被 affine hybrid model 收束的安全验证问题。

### 需求前提

1. 连续动力学最好能写成 affine 或 piecewise-affine 形式。
2. guards、assignments 与 invariants 需要显式结构化。
3. 目标问题主要是 reachability / safety，而不是概率或学习。
4. 团队愿意接受 set-based over-approximation，而不是只看单条仿真轨迹。

### 不适用或高成本场景

若系统关键复杂度来自强非线性 ODE 或高阶非多面体约束，则 `SpaceEx` 不是最自然的第一选择。

## 与相邻形式主义的关系

相对 [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)，`SpaceEx` 更强调 scalability 与平台化；相对 [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)，它仍主要停留在 affine hybrid line；相对 [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)，它代表的是更成熟的第二/第三代 hybrid verification platform。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 未来要把生成的控制模型接到成熟验证后端，那么“平台级 hybrid verifier”已经足够成熟，可以作为目标落点来反推建模约束。

### 作为目标形式主义还是中间表示

更像验证后端与工具平台，而不是中立建模语言。

### 对需求到模型生成的启发

1. 需求生成 hybrid model 时，必须把 dynamics、invariants、assignments 与 initial states 清晰分栏。
2. 若目标是高维系统，建模阶段就要考虑支持函数/模板多面体一类的可分析承载。
3. 平台化工具通常同时要求“模型结构”和“分析配置”两部分输入，生成端也应考虑把 scenario/configuration 一并结构化。

### 现实限制

`SpaceEx` 很强，但其强项明确落在 affine reachability；如果需求超出这一建模前提，就要考虑其他 hybrid verifier。

## 重要的相关工作

- [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：早期 hybrid verification 工具母线。
- [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)：`SpaceEx` 直接承接的 polyhedral verification 路线。
- [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)：非线性 hybrid flowpipe 分析路线。
- [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)：工业 `Stateflow` 接 hybrid verification 的另一条工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Affine / Piecewise-Affine Hybrid Systems / SpaceEx`
- 论文角色：hybrid reachability platform / scalable verifier
