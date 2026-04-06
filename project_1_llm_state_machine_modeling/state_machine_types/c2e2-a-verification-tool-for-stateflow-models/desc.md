# C2E2：Stateflow 模型验证工具 / C2E2: A Verification Tool for Stateflow Models

## 基本信息

- 标题：C2E2: A Verification Tool for Stateflow Models
- 中文标题：C2E2：Stateflow 模型验证工具
- 作者：Parasara Sridhar Duggirala，Sayan Mitra，Mahesh Viswanathan，Matthew Potok
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 68-82，2015
- DOI：`10.1007/978-3-662-46681-0_5`
- 链接：https://doi.org/10.1007/978-3-662-46681-0_5
- 形式主义：`Stateflow / C2E2 hybrid verification flow`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：Stateflow 仿真驱动验证方法 / tool paper
- 工具/实现获取方式：原文给出 `https://publish.illinois.edu/c2e2-tool/`，并说明前端基于 Python、验证算法基于 C++，并连接 `CAPD`、`GLPK`、`PPL`、`matplotlib` 等库。
- 标准/格式获取方式：承载方式是带注释的 `Stateflow` `.mdl` / `.hyxml` 模型、bounded-time safety properties 和 discrepancy annotations；原文未给中立交换标准。

## 简报

这篇论文的关键价值，是把工业界常见的 `Stateflow` 模型接上一个“仿真驱动、但有形式保证”的验证流程。`C2E2` 不靠暴力 state-space symbolic explosion，而是把 `Stateflow` 解释成 hybrid automata，再用 validated simulations、discrepancy annotations 和 reachtube over-approximation 去证明或反驳 bounded-time safety。

- 形式主义定位：`Stateflow` 模型的 simulation-driven hybrid verification 路线，而不是新的状态机语言。
- 构造方式简述：输入带注释的 `Stateflow` 模型，前端解析成 hybrid automata，生成 simulation code，再由验证算法做 reachtube over-approximation。
- 基础设施与场景简述：依托 Python front end、C++ verifier、`CAPD` validated simulation、`GLPK`、`PPL` 和可视化器，服务带非线性 ODE、guards、resets 的 `Stateflow` CPS 模型。

```text
annotated Stateflow model -> hybrid-automata interpretation -> validated simulation + discrepancy annotation -> reachtube checking -> safe / unsafe
```

## 形式主义定义与核心对象

### 定义对象

论文将输入对象固定为：

1. 带连续变量与离散 locations 的 `Stateflow` 模型。
2. 由 differential equations 定义的 trajectories。
3. 由 guards / resets 定义的 discrete transitions。
4. bounded-time safety properties。
5. 用户提供的 discrepancy annotations `⟨K,\gamma⟩`。

### 核心抽象

原文直接把解释后的混成自动机写成：

$$
A = \langle V, Loc, A, D, T \rangle
$$

上式中的符号逐项解释如下：

1. `V` 是变量集合，其中包含特殊离散变量 `loc` 和连续变量集 `X`。
2. `Loc` 是 locations 集合，即 `loc` 的取值域。
3. `A` 是 actions / transition labels 集合。
4. `D \subseteq val(V) \times A \times val(V)` 是 discrete transitions 集合。
5. `T` 是 trajectories 集合，并按 location 的 ODE 与 invariant 分组。

该论文最重要的工具假设不是单纯的 HA tuple，而是 discrepancy annotation：

$$
\|\tau_1(t)-\tau_2(t)\| \le K \|\tau_1(0)-\tau_2(0)\| e^{\gamma t}
$$

上式中的符号逐项解释如下：

1. `\tau_1`、`\tau_2` 是同一 location dynamics 下的两条 trajectories。
2. `K` 是 multiplicity factor。
3. `\gamma` 是 exponential factor。
4. 该不等式用于把单条 validated simulation 膨胀成一段可证明 sound 的 reachtube。

### 一个最小例子与通俗解释

论文最直观的例子是 cardiac cell + pacemaker：

1. `stimOn` 和 `stimOff` 两个离散 modes 由 `Stateflow` 状态表示。
2. 连续变量 `u`、`v` 表示心肌细胞某些电性质，时钟 `t` 用来控制刺激切换。
3. 当 `t >= 5` 时，从 `stimOn` 切回 `stimOff`，并重置 `t = 0`。
4. `C2E2` 不是枚举全部轨迹，而是对代表性仿真轨迹做“带证明的膨胀”，判断是否可能碰到 unsafe set。

通俗地说，`C2E2` 像“会给仿真加安全边界的 Stateflow 验证器”。它不是只给你一条 sample trace，而是告诉你“这条轨迹附近整片行为都安全 / 都不安全 / 还需要细分”。

### 运行 / 接受 / 转移语义

论文对 bounded-time safety 的判定写成：

$$
exec(A,\Sigma,T,N)
$$

其中可以保守理解为从初始集 `\Sigma` 出发、时间界 `T`、离散切换界 `N` 下的执行集合。安全性判定写成：

$$
\exists \tau_0 a_1 \cdots \tau_k \in exec(A,\Sigma,T,N),\ \tau_k(t)\in U \Rightarrow unsafe
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是初始状态集。
2. `U` 是 unsafe set。
3. `\tau_i` 是 trajectory 段。
4. `a_i` 是离散动作。
5. 若某条 bounded execution 最终进入 `U`，则系统 unsafe；否则 safe。

工具算法的关键中间产物是 reachtube：

$$
\mathcal{R} = (R_0,\ldots,R_k)
$$

上式中的符号逐项解释如下：

1. `R_i` 是第 `i` 个时间片上的 reachable region over-approximation。
2. 它由 validated simulation 与 discrepancy annotation 共同生成。
3. `tagRegion`、`invariantPrefix` 与 `checkSafety` 决定该 reachtube 对安全性的结论。

### 语义边界

这篇论文非常坦率地给出了边界：

1. 它只做 bounded-time safety，不做无界时域全性质。
2. 依赖用户提供每个 ODE 的 discrepancy annotation。
3. `Stateflow` 在工具中按 urgent、deterministic 语义解释。
4. 为了保证终止，对这种 urgent semantics 的 guard 还要求是 hyperplanes，并实际验证一个 `\epsilon`-perturbed model。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| HA 骨架 | `$A = \langle V, Loc, A, D, T \rangle$` | `Stateflow` 被解释成 hybrid automata。 |
| discrepancy annotation | `$\|\tau_1(t)-\tau_2(t)\| \le K \|\tau_1(0)-\tau_2(0)\| e^{\gamma t}$` | 用来把单条仿真膨胀成安全边界。 |
| bounded-time unsafety | `$\exists \text{ execution } \in exec(A,\Sigma,T,N): \tau_k(t)\in U$` | 判定是否存在进入 unsafe set 的 bounded execution。 |
| reachtube | `$\mathcal{R} = (R_0,\ldots,R_k)$` | 算法的核心 over-approximation 对象。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Stateflow` locations 是离散骨架。 |
| 事件 / 触发 | 强支持 | guards / urgent transitions 直接驱动切换。 |
| 守卫 / 数据 | 很强 | guards、resets、ODEs、unsafe polyhedra 全显式进入验证。 |
| 层次 | 部分支持 | 输入是 `Stateflow`，但工具核心关注其 hybrid interpretation。 |
| 并发 / 同步 | 弱到中 | 论文主线不是并发协议，而是 CPS hybrid safety。 |
| 时间约束 | 很强 | bounded time horizon 是核心。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 支持 nonlinear ODE，不涉及概率。 |
| 可执行 / 可验证性 | 很强 | front end、property editor、plotter 与 verifier 是一体化工具。 |

### 形式化问题与性质

1. `C2E2` 的关键创新是“仿真 + 形式保证”而不是纯 symbolic 或纯 testing。
2. discrepancy annotations 是它能在非线性系统上保持 soundness 的核心。
3. relative completeness 明确限制在 robustly safe / robustly unsafe 场景，这比泛泛说“能验证 Stateflow”严谨得多。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 在 `Stateflow` 里建模，并添加 ODE / guard / reset / annotation。
2. 前端读取 `.mdl` 或 `.hyxml`。
3. 通过 GUI 输入或编辑 bounded-time safety property。
4. 运行 verifier 并查看 reachable-set plot。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 带注释的 `Stateflow` `.mdl` 模型。
2. `.hyxml` 中间格式。
3. 编译出的 simulation code。
4. reachtube 数据与 property specification。

### 交换与互操作

这篇论文的互操作重点不是开放标准，而是模块化架构：

1. front end 与 verification engine 分离。
2. simulation engine 可替换成 `CAPD`、`VNODE-LP`、`Boost` 等。
3. checker 可以与 `GLPK`、潜在的 `Z3` 等后端组合。

## 配套基础设施

- 建模/编辑工具：`Stateflow` + `C2E2` front end。
- 解析/交换/元模型支持：前端扩展 `Hylink` parser，把 `.mdl/.hyxml` 转成中间格式。
- 仿真/执行支持：`CAPD` 和 `VNODE-LP` 等 validated simulation engines。
- 验证/分析支持：C++ verifier、reachtube construction、bounded-time safety checking。
- 代码生成/转换支持：前端会生成 simulation code，并可扩展到其他模型类型或后端。
- 标准化或社区生态：academic 免费发布，另有 `PPL` / `matplotlib` 可视化与属性编辑支持。

## 适用场景与需求前提

### 适用场景

适合 `Stateflow` 主导的汽车、航电、医疗设备和一般 CPS 控制器，只要重点是 bounded-time safety 而且模型含 ODE + guards + resets。

### 需求前提

1. 模型能解释成 deterministic / urgent hybrid automata。
2. guards 与 resets 最好是 polynomial / hyperplane-friendly。
3. 用户能为每个 ODE 提供 discrepancy annotation。
4. 目标性质可以写成 bounded-time safety，而不是更复杂的时序逻辑全集。

### 不适用或高成本场景

如果没有可用 annotation，或者要做的是无界 liveness、随机语义或开放并发协议，`C2E2` 就不是理想路线。

## 与相邻形式主义的关系

相对 [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)，本文讲的是验证工具而不是工业语义澄清；相对 [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md) 与 `Flow* / Ariadne` 这类 hybrid verifiers，它更贴近 `Stateflow` 建模入口；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，它并不把问题收束成纯 clocks 模型，而是保留非线性 ODE。

## 与本研究的关系

### 对 Project 1 的价值

它证明了工业 `Stateflow` 目标并不意味着只能仿真，仍然可以接一个带形式保证的验证后端。

### 作为目标形式主义还是中间表示

更像连接 `Stateflow` 生态与 hybrid verification 的方法路线，而不是中立交换格式。

### 对需求到模型生成的启发

1. 若未来 LLM 生成 `Stateflow`，最好同时生成 guards、resets、ODE annotations 和 safety property skeleton。
2. “生成之后怎么验证” 不一定只能靠符号模型检查，也可以走 simulation-driven proof 路线。
3. 工具能否成功，很大程度取决于生成模型是否满足 deterministic / urgent / annotated 的收束条件。

### 现实限制

`C2E2` 很适合 bounded-time safety，但对更宽的验证目标和无注释模型并不宽容。

## 重要的相关工作

- [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)：`Stateflow` 工业语义母线。
- [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：混成自动机 symbolic verification 工具母线。
- [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：更偏 clocks 的 timed-automata 工具路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Stateflow / C2E2 hybrid verification flow`
- 论文角色：Stateflow 仿真驱动验证方法 / tool paper

