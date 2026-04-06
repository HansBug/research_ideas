# DryVR：面向汽车系统的数据驱动验证与组合推理 / DryVR: Data-Driven Verification and Compositional Reasoning for Automotive Systems

## 基本信息

- 标题：DryVR: Data-Driven Verification and Compositional Reasoning for Automotive Systems
- 中文标题：DryVR：面向汽车系统的数据驱动验证与组合推理
- 作者：Chuchu Fan，Bolun Qi，Sayan Mitra，Mahesh Viswanathan
- 发表：*Computer Aided Verification*，Lecture Notes in Computer Science 10426，pp. 441-461，2017
- DOI：`10.1007/978-3-319-63387-9_22`
- 链接：https://doi.org/10.1007/978-3-319-63387-9_22
- 形式主义：`DryVR / black-box simulator + transition graph hybrid verification`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：simulation-driven hybrid verification / discrepancy learning / graph reasoning framework
- 工具/实现获取方式：原文明确给出 `DryVR` 工具，并说明输入包括 black-box simulator、transition graph、initial set 与 unsafe set。
- 标准/格式获取方式：承载方式是 simulator traces、transition graph、initial/unsafe set 和 learned discrepancy；原文未给中立交换标准。

## 简报

这篇论文的关键价值，不是再写一个“只接受白盒微分方程”的 hybrid verifier，而是把现实系统里常见的 black-box simulator 直接纳入形式验证流程。`DryVR` 把系统抽成“continuous trajectories 由 simulator 给出，mode switches 由 white-box transition graph 给出”，再通过学习 discrepancy function、生成 reach tube，以及基于 graph simulation / sequential composition 的推理，把原本很难白盒建模的汽车控制系统也拉进 bounded verification。

- 形式主义定位：面向 black-box simulation 的 hybrid verification 方法路线，不是新的混成自动机理论母线。
- 构造方式简述：提供 initial set、unsafe set、transition graph 和 simulator，先从 simulation data 学 discrepancy，再做 graph-based reachability 和 safety checking，最后用 graph reasoning 扩展到更长 switching sequences。
- 基础设施与场景简述：依托 `DryVR`、transition graph、simulation traces、learned discrepancy、reachtube generation 与 graph simulation，服务 powertrain、AEB、lane merge、auto passing 等汽车系统验证。

```text
black-box simulator + transition graph + initial/unsafe sets -> discrepancy learning -> reach tubes per graph vertex -> bounded safety / graph-based compositional reasoning
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. transition graphs。
2. deterministic, prefix-closed labeled trajectories。
3. hybrid system `H = \langle L, \Theta, G, T_L \rangle`。
4. discrepancy learning。
5. GraphReach / VerifySafety / graph simulation / sequential composition。

### 核心抽象

论文首先定义 transition graph：

$$
G = \langle L, V, E, vlab, elab \rangle
$$

上式中的符号逐项解释如下：

1. `L` 是 mode labels 集合。
2. `V` 是 vertices 集合。
3. `E \subseteq V \times V` 是边集合。
4. `vlab : V \to L` 给每个 vertex 赋一个 mode。
5. `elab : E \to \mathbb{R}_{\ge 0} \times \mathbb{R}_{\ge 0}` 给每条边赋一个允许驻留时间区间。

在此基础上，论文直接定义 hybrid system：

$$
H = \langle L, \Theta, G, T_L \rangle
$$

上式中的符号逐项解释如下：

1. `L` 是 mode 集合。
2. `\Theta \subseteq \mathbb{R}^n` 是紧初始状态集。
3. `G` 是 transition graph。
4. `T_L` 是按 `L` 标记的 deterministic、prefix-closed trajectories 集合。
5. 与传统白盒 `ODE + guard + reset` 不同，这里连续部分主要通过 simulator 轨迹体现。

可达集与 reach tube 的定义在论文中写成：

$$
\mathrm{ReachTube}_H = \{\langle x, \ell, t \rangle \mid \text{for some } v,\ \langle x, \ell \rangle \text{ is reachable at time } t \text{ and vertex } v\}
$$

上式中的符号逐项解释如下：

1. `x` 是连续状态。
2. `\ell` 是当前 mode。
3. `t` 是全局时间。
4. `v` 是 transition graph 上的某个顶点。
5. 这说明 `DryVR` 输出的是按 graph vertex 分层的 reach tubes，而不是单一集合。

论文把 global exponential discrepancy 写成：

$$
\beta(x_1, x_2, t) = \lVert x_1 - x_2 \rVert K e^{\gamma t}
$$

上式中的符号逐项解释如下：

1. `x_1, x_2` 是两条轨迹的初始状态。
2. `t` 是时间。
3. `K` 和 `\gamma` 是从 simulation data 学出的常数。
4. `\beta` 用来上界相邻初始条件下轨迹之间的偏离。

论文还定义了 sequential composition：

$$
G_1 \circ G_2 = \langle L, V, E, vlab, elab \rangle
$$

上式中的符号逐项解释如下：

1. `G_1` 和 `G_2` 是两个 transition graph。
2. `\circ` 表示把 `G_1` 的 terminal vertex 与 `G_2` 的 initial vertex 对接。
3. 该构造用于把短 switching-sequence 的安全性推广到更长序列。

### 一个最小例子与通俗解释

论文里的 powertrain 例子很适合解释这条路线：

1. 系统有 `startup`、`normal`、`powerup`、`sensorfail` 等 modes。
2. 连续动力学不是手写给 `DryVR` 的闭式方程，而是由 `Simulink` simulator 提供轨迹。
3. 设计者额外给出 transition graph，规定 mode 之间允许怎样切换、每段可持续多久。
4. `DryVR` 再从初始集出发学习 discrepancy，膨胀仿真轨迹生成 reach tube，并检查 air-fuel ratio 等性质是否会进入 unsafe 区域。

通俗地说，`DryVR` 的思路是：既然很多工业控制器已经有 simulator 了，那就不要逼用户再重写一份完美的白盒模型。用户只要补一张“模式切换图”，工具就可以在 simulator 之上做近似但正式的安全分析。

### 运行 / 接受 / 转移语义

其运行语义主线是：

1. transition graph 控制 discrete switching skeleton。
2. simulator 提供每个 mode 下的 continuous trajectories。
3. discrepancy 把有限条仿真外推成 reach tube。
4. GraphReach 按 DAG 的 topological order 推进各 vertex 的可达集。
5. VerifySafety 对 unsafe set 做 refine-and-check。

### 语义边界

边界也很清楚：

1. 主线是 bounded verification，不是任意无限时域的完整判定。
2. 正确性依赖 learned discrepancy 足够可靠。
3. 连续部分默认来自 simulator，而不是完整白盒解析模型。
4. transition graph 是 DAG，且每段切换时间有界。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| transition graph | `$G = \langle L, V, E, vlab, elab \rangle$` | 模式切换骨架的正式定义。 |
| hybrid system | `$H = \langle L, \Theta, G, T_L \rangle$` | `DryVR` 的系统输入把 graph 与 trajectories 并列。 |
| reach tube | `$\mathrm{ReachTube}_H = \{\langle x, \ell, t \rangle \mid \cdots \}$` | 核心分析产物是按 mode/time 组织的 reach tubes。 |
| discrepancy | `$\beta(x_1, x_2, t) = \lVert x_1 - x_2 \rVert K e^{\gamma t}$` | 从 simulation data 学出的偏差上界。 |
| bounded safety | `$\mathrm{Reach}_H \cap U = \emptyset$` | 与 unsafe set 的交为空即安全。 |
| sequential composition | `$G_1 \circ G_2$` | 用短 graph 的结果推更长 switching sequence。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | transition graph 的 modes/vertices 是核心。 |
| 事件 / 触发 | 中等支持 | 切换通过 graph 边和驻留时间窗口给出。 |
| 守卫 / 数据 | 中等到强 | unsafe set、initial set 和 simulator state 都参与分析。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 弱支持 | 主体是单系统或组合系统的 mode switching 分析。 |
| 时间约束 | 很强 | edge labels 就是时间窗口，reach tube 也显式带时间。 |
| 连续动态 / 随机性 | 很强连续 / 不随机 | 连续动力学来自 simulator；概率仅在 discrepancy 学习正确性层面。 |
| 可执行 / 可验证性 | 很强 | 能输出 `SAFE/UNSAFE` 与 counterexample-style reachtube。 |

### 形式化问题与性质

1. 论文真正补的是“如何在 black-box simulator 之上做正式 reachability”，而不是再写一个纯白盒 hybrid verifier。
2. discrepancy learning 是它把仿真提升为可验证近似的关键。
3. graph simulation 与 sequential composition，使它能利用短 switching-sequence 的结果去推更长序列。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 准备 black-box simulator。
2. 指定 transition graph。
3. 指定 initial set 与 unsafe set。
4. 运行 discrepancy learning、GraphReach 和 VerifySafety。

### 机器可处理承载方式

机器可处理承载方式包括：

1. simulator traces。
2. graph text/configuration。
3. initial / unsafe sets。
4. learned discrepancy 与 reachtubes。

### 交换与互操作

这条路线的互操作重点在于：

1. 用 transition graph 作为对 simulator 的结构化补充。
2. 用 discrepancy 把仿真轨迹提升成 reach tube。
3. 用 graph reasoning 在不同 switching skeleton 之间复用验证结果。

## 配套基础设施

- 建模/编辑工具：`DryVR` 自身的 graph/input 配置与 simulator 接口。
- 解析/交换/元模型支持：transition graph、initial set、unsafe set 和 trajectory sample 输入。
- 仿真/执行支持：依赖外部 black-box simulator。
- 验证/分析支持：discrepancy learning、GraphReach、VerifySafety、graph simulation、sequential composition。
- 代码生成/转换支持：主线是验证与推理，不是部署代码生成。
- 标准化或社区生态：依托 hybrid verification 与 automotive benchmark 生态，而非中立标准。

## 适用场景与需求前提

### 适用场景

适合已有工业 simulator、但缺少完整白盒微分方程模型的汽车控制系统、ADAS、powertrain 和 hybrid controller 验证场景。

### 需求前提

1. 系统必须至少能提供稳定的 black-box simulator。
2. 模式切换骨架能整理成带时间区间的 DAG transition graph。
3. 初始集与 unsafe set 能结构化描述。
4. 团队接受 data-driven discrepancy 的近似边界。

### 不适用或高成本场景

如果系统没有可靠 simulator、切换结构不是有界 DAG、或者需要最强白盒可证明性，`DryVR` 就不是最直接的选择。

## 与相邻形式主义的关系

相对 [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md)，它更依赖 black-box simulator 与 learned discrepancy，而不是 affine system closed-form propagation；相对 [an-introduction-to-cora-2015/desc.md](../an-introduction-to-cora-2015/desc.md)，它不依赖统一 set-representation toolbox，而更强调 simulation-driven verification；相对 [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)，两者都面向仿真驱动验证，但 `DryVR` 用 transition graph + discrepancy learning 支撑更一般的 black-box hybrid setting。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续要把 LLM 生成的状态机落到 hybrid verifier，上游可以不必一次性生成完整白盒动力学，只要能稳定抽出 mode graph、切换时间窗口和 initial/unsafe sets，就能接上更现实的 data-driven 验证链。

### 作为目标形式主义还是中间表示

更适合作为验证后端和 reasoning bridge，而不是最终目标建模语言。

### 对需求到模型生成的启发

1. mode switching skeleton 本身就是非常重要的结构化工件。
2. 对连续部分可先允许 black-box，再逐步增强白盒精度。
3. 当系统存在明显重复的 switching pattern 时，graph composition / simulation reasoning 很有价值。

### 现实限制

它很适合 simulator-rich 的工业系统，但不适合没有结构化 transition graph 的纯黑箱系统。

## 重要的相关工作

1. [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md)：另一条 simulation-aware reachability 工具线。
2. [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)：面向 `Stateflow` 的仿真驱动验证工具。
3. [an-introduction-to-cora-2015/desc.md](../an-introduction-to-cora-2015/desc.md)：更通用的 continuous/hybrid reachability toolbox。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文主体是基于 simulator、transition graph 和 discrepancy learning 的验证路线，因此更适合按 `📦/🛠️` 归类，而不是按新的混成自动机本体处理。
