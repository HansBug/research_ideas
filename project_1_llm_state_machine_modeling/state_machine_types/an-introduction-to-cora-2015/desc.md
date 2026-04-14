# CORA 2015 导论 / An Introduction to CORA 2015

## 基本信息

- 标题：An Introduction to CORA 2015
- 中文标题：CORA 2015 导论
- 作者：Matthias Althoff
- 发表：*EPiC Series in Computing*，Vol. 34，pp. 120-151，2015
- DOI：`10.29007/zbkv`
- 链接：https://doi.org/10.29007/zbkv
- 形式主义：`CORA / continuous and hybrid reachability toolbox`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：continuous/hybrid reachability toolbox and set-representation infrastructure
- 工具/实现获取方式：原文明确说明 `CORA` 是 `MATLAB` toolbox，并给出各 set classes、continuous-dynamics classes 和 hybrid-automaton classes。
- 标准/格式获取方式：承载方式是 `MATLAB` 类库、zonotope family、matrix-set classes 和 `hybridAutomaton/location` objects；原文未给中立交换标准。

## 简报

这篇论文的关键价值，不是只介绍一种 reachability 算法，而是把连续与混成系统分析真正做成一个“可插拔 set representation + dynamics class”的工具平台。`CORA` 把 zonotope、polynomial zonotope、probabilistic zonotope、matrix zonotope、polytope 等集合表示，与 linear / nonlinear / DAE / hybrid dynamics 的 reachability 算法放到同一 `MATLAB` 框架里，使研究者可以在不重写整套分析器的前提下替换集合表示或系统类。

- 形式主义定位：面向连续/混成系统 reachability 的分析平台，而不是新的混成自动机本体。
- 构造方式简述：用不同 set classes 表示初始集、guard、invariant 与可达集，再调用对应 continuous/hybrid dynamics class 做 reachability、simulation 和 plot。
- 基础设施与场景简述：依托 `MATLAB`、zonotope family、matrix-set operations、continuous-dynamics classes 与 `hybridAutomaton/location` classes，服务 linear/nonlinear/hybrid system safety verification。

```text
initial set + set representation classes + dynamics class -> reachable-set computation -> guard/invariant intersection -> hybrid safety evidence
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. set representations：zonotope、zonotope bundle、polynomial zonotope、probabilistic zonotope、polytope 等。
2. continuous dynamics：linear、parameter-varying、nonlinear、DAE。
3. hybrid dynamics：location、guard、jump、invariant。
4. `MATLAB` object-oriented toolbox architecture。
5. reachable set、simulation、plot 和 conversion pipeline。

### 核心抽象

论文直接给出 zonotope 定义：

$$
Z = (c, g^{(1)}, \ldots, g^{(p)})
$$

上式中的符号逐项解释如下：

1. `c \in \mathbb{R}^n` 是 zonotope 的中心。
2. `g^{(i)} \in \mathbb{R}^n` 是第 `i` 个 generator。
3. `p` 是 generator 个数。
4. 这是 `CORA` 中最基础、也最常用的集合表示之一。

论文还把 zonotope 解释成 Minkowski 和的形式，可保守写成：

$$
Z = c \oplus l^{(1)} \oplus \cdots \oplus l^{(p)}
$$

上式中的符号逐项解释如下：

1. `l^{(i)}` 是由 generator `g^{(i)}` 诱导的线段。
2. `\oplus` 是 Minkowski addition。
3. 这说明 zonotope 本质上是若干线段平移叠加后的集合。

对 hybrid dynamics，论文直接定义：

$$
HA = (V, v_0, X, X_0, U, P, inv, T, g, h, f)
$$

上式中的符号逐项解释如下：

1. `V` 是 location 集合。
2. `v_0` 是初始 location。
3. `X` 是连续状态空间。
4. `X_0` 是初始连续状态集合。
5. `U` 是输入空间。
6. `P` 是参数空间。
7. `inv` 为每个 location 指派 invariant。
8. `T` 是离散转移集合。
9. `g` 是 guard function。
10. `h` 是 jump function。
11. `f` 是连续流函数。

其跳转语义被限制为线性形式：

$$
x' = K(v_i, v_j)x + l(v_i, v_j)
$$

上式中的符号逐项解释如下：

1. `x` 是跳转前连续状态。
2. `x'` 是跳转后连续状态。
3. `K(v_i, v_j)` 是从 location `v_i` 到 `v_j` 的线性变换矩阵。
4. `l(v_i, v_j)` 是对应的偏移项。
5. 这说明 `CORA` 中 hybrid jump 的主承载是 affine map。

连续线性系统的骨架也被论文直接写成：

$$
\dot{x}(t) = Ax(t) + Bu(t), \quad x(0) \in X_0, \quad u(t) \in U
$$

上式中的符号逐项解释如下：

1. `x(t)` 是连续状态向量。
2. `A` 是系统矩阵。
3. `B` 是输入矩阵。
4. `u(t)` 是输入信号。
5. `X_0` 是初始集合。
6. `U` 是输入集合。

### 一个最小例子与通俗解释

论文里的 bouncing-ball 例子很适合说明 `CORA` 的工作方式：

1. location 中连续状态按重力方程演化。
2. 初始状态不是单点，而是一个 zonotope。
3. 当球碰到地面 guard 时，触发 jump，把速度按恢复系数瞬时反向缩放。
4. `CORA` 输出的不是单条仿真轨迹，而是一整片随时间推进的 reachable set。

通俗地说，`CORA` 像一个“集合演算版仿真器”。普通仿真器一次只追一条轨迹，`CORA` 追的是一团初始不确定性会扩张成什么形状，并且把这团形状在连续演化、guard 触发和 jump 之后如何变化都保留下来。

### 运行 / 接受 / 转移语义

`CORA` 的核心运行语义是 reachable-set based：

1. 先选定一种 set representation。
2. 对连续 dynamics 执行线性变换、Minkowski 加法、reduce、intersection 等操作。
3. 对 hybrid system 再叠加 guard intersection、jump map 和 invariant clipping。
4. 最终得到 over-approximated reachable set，并用它判断 unsafe set 是否可达。

### 语义边界

边界同样很清楚：

1. 论文主线是 toolbox 架构与 set representations，不是某一种单独最优算法。
2. 它广泛覆盖 linear/nonlinear/hybrid classes，但精度与效率仍依赖所选 set class。
3. 主要工作在 `MATLAB` 生态中完成。
4. 工具很强，但不是开放交换格式或中立运行时标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| zonotope | `$Z = (c, g^{(1)}, \ldots, g^{(p)})$` | `CORA` 最基础的集合表示。 |
| zonotope 组合语义 | `$Z = c \oplus l^{(1)} \oplus \cdots \oplus l^{(p)}$` | 说明它是若干线段的 Minkowski 和。 |
| hybrid automaton | `$HA = (V, v_0, X, X_0, U, P, inv, T, g, h, f)$` | `CORA` 对 hybrid system 的直接骨架定义。 |
| jump map | `$x' = K(v_i, v_j)x + l(v_i, v_j)$` | hybrid jumps 采用 affine update。 |
| continuous dynamics | `$\dot{x}(t) = Ax(t) + Bu(t)$` | linear reachability 的典型入口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 对 hybrid automaton location 和连续状态都支持良好。 |
| 事件 / 触发 | 中等支持 | guard 和 discrete transitions 负责模式切换。 |
| 守卫 / 数据 | 很强 | guard、invariant、input set、parameter set 都是核心。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 弱支持 | 主体是单体或组合连续/混成系统 reachability。 |
| 时间约束 | 很强 | reachable set 本质上是时间推进的。 |
| 连续动态 / 随机性 | 很强连续 / 中等随机 | 连续系统覆盖极广，并支持 probabilistic zonotope 这类随机扩展。 |
| 可执行 / 可验证性 | 很强 | 可做 simulation、reachability、plot 和 hybrid safety analysis。 |

### 形式化问题与性质

1. 论文真正补的是“reachability 工具箱平台化”，而不是单一 reachability trick。
2. set representation 与 dynamics class 的分离，是 `CORA` 可扩展性的关键。
3. `hybridAutomaton/location` 类和 zonotope family 共同构成了它最稳定的基础设施骨架。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 选择 set representation，例如 zonotope。
2. 选择 dynamics class，例如 linear / nonlinear / hybrid。
3. 指定初始集、输入集、guard 与 invariant。
4. 调用 `reach`、`simulate`、`plot` 等方法。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `MATLAB` classes。
2. set objects，如 zonotope、polytope、interval hull。
3. continuous-dynamics classes。
4. `hybridAutomaton` 与 `location` objects。

### 交换与互操作

互操作重点在于：

1. 不同 set representations 之间的 exact / over-approx conversion。
2. continuous dynamics 与 hybrid dynamics 共享同一集合基础设施。
3. 使用统一接口调用不同 reachability 算法。

## 配套基础设施

- 建模/编辑工具：`MATLAB` 中的 `CORA` toolbox。
- 解析/交换/元模型支持：set conversions、matrix-set classes、hybrid automaton classes。
- 仿真/执行支持：`simulate`、`plot` 和连续/混成轨迹计算。
- 验证/分析支持：continuous reachability、hybrid reachability、guard intersection、unsafe analysis。
- 代码生成/转换支持：主线是分析而非部署代码生成。
- 标准化或社区生态：依托混成系统 reachability 研究生态；不是中立交换标准。

## 适用场景与需求前提

### 适用场景

适合线性/非线性/混成系统的安全验证、可达性分析、控制器验证和不确定初始集分析。

### 需求前提

1. 系统能写成 `CORA` 支持的 continuous / hybrid dynamics class。
2. 初始集、guard、invariant 最好能落到现有 set representations。
3. 团队能接受 over-approximation 的 reachable set 视角。
4. 使用 `MATLAB` 生态是默认前提。

### 不适用或高成本场景

如果需求主要是开放交换、部署执行、图形化工业标准或纯离散接口/协议验证，`CORA` 就不是最自然的载体。

## 与相邻形式主义的关系

相对 [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md)，它覆盖的系统类更广、set representations 更多，但不主打 simulation-equivalent 语义；相对 [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)，它更像现代 toolbox 平台，而不是单一路径的 symbolic model checker；相对 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md) 与 [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)，它的特色在于把多种 set representation 和 dynamics class 统一到同一 `MATLAB` 架构中。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续要把 LLM 生成的状态机接到混成验证后端，后端不只关心 automaton 结构，还关心 reachable-set representation 是否合适。

### 作为目标形式主义还是中间表示

更适合作为混成/连续验证的分析后端与执行载体，而不是直接给用户的目标建模语言。

### 对需求到模型生成的启发

1. 对连续系统，需求抽取时必须把初始不确定性、guard、invariant 和 jump map 分开。
2. 选择哪种 set representation 会直接影响后续分析的可扩展性。
3. 如果目标是接多个 verifier，最好在生成阶段就把 continuous/hybrid semantics 与 set assumptions 显式化。

### 现实限制

它对混成 reachability 很强，但对纯离散状态机、开放交换标准和工业图形建模不是直接答案。

## 重要的相关工作

1. [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md)：affine-hybrid 可达性工具线。
2. [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：更早的 hybrid model checker 主线。
3. [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)：可扩展混成验证代表工具。
4. [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)：非线性混成分析路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文主体是 reachability toolbox 的集合表示、类架构和 hybrid-analysis 基础设施，而不是新的混成自动机本体，因此更适合归到 `📦/🏗️`。
