# TuLiP：面向滚动时域时序逻辑规划的软件工具箱 / TuLiP: A Software Toolbox for Receding Horizon Temporal Logic Planning

## 基本信息

- 标题：TuLiP: A Software Toolbox for Receding Horizon Temporal Logic Planning
- 中文标题：TuLiP：面向滚动时域时序逻辑规划的软件工具箱
- 作者：Tichakorn Wongpiromsarn，Ufuk Topcu，Necmiye Ozay，Huan Xu，Richard M. Murray
- 发表：In *Proceedings of the 14th International Conference on Hybrid Systems: Computation and Control*，pp. 313-314，2011
- DOI：`10.1145/1967701.1967747`
- 链接：https://doi.org/10.1145/1967701.1967747
- 形式主义：`finite transition system abstraction / GR(1) synthesis / receding horizon temporal logic planning / TuLiP`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：embedded control synthesis toolbox integrating abstraction, GR(1) synthesis, and receding-horizon planning
- 工具/实现获取方式：原文明确给出 `TuLiP` 站点 `http://www.cds.caltech.edu/tulip`，并说明其为 Python-based toolbox。
- 标准/格式获取方式：核心承载是 continuous plant abstraction、`GR(1)` 规格、receding-horizon invariant 与 JTLV-based synthesis workflow；不是独立行业标准。

## 简报

`TuLiP` 解决的是“连续/混成控制对象如何接到反应式时序逻辑综合”这个非常工程化的问题。它不是单纯把 `LTL` 丢给求解器，而是把有限状态抽象、`GR(1)` 游戏综合和 receding-horizon planning 串成同一工具箱，使控制器在面对 adversarial environment 时仍能保持 correct-by-construction 保证。

- 形式主义定位：面向 embedded / cyber-physical control synthesis 的方法与工具箱，而不是新的自动机母型。
- 构造方式简述：continuous plant 先抽象成 finite transition system，再根据 `GR(1)` 规格综合策略，并通过 receding horizon 把大问题切成一组较小的子问题。
- 基础设施与场景简述：依托 Python toolchain、state-space abstraction、JTLV synthesis backend、counterexample reporting 与 invariant construction，服务自主驾驶、航电车辆管理和多目标跟踪。

```text
continuous plant + disturbances -> finite-state abstraction -> GR(1) game synthesis -> receding-horizon subproblems -> embedded controller
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 连续 plant 与 adversarial environment。
2. 从连续系统到 finite transition system 的 abstraction。
3. `GR(1)` 形式的任务规格。
4. receding-horizon partial-order structure 与 invariants。
5. Python-based synthesis toolbox 与 `JTLV` backend。

### 核心抽象

正文明确给出其当前支持的 plant dynamics：

$$
s[t+1] = As[t] + Bu[t] + Ed[t], \quad u[t] \in U,\ d[t] \in D,\ s[0] \in S
$$

上式中的符号逐项解释如下：

1. `$s[t]$` 是时刻 `$t$` 的连续状态。
2. `$u[t]$` 是控制输入。
3. `$d[t]$` 是外部扰动或环境输入。
4. `$A, B, E$` 是系统矩阵。
5. `$S, U, D$` 分别是状态空间、可行控制输入集和可行扰动集，论文假设它们为有界多面体。

论文还把任务规格收束到 `GR(1)` 形式，可整理为：

$$
\varphi = \left(\varphi_{init} \land \Box \varphi_e \land \bigwedge_{i \in I_f} \Box \Diamond \varphi_{f,i}\right)
\Rightarrow
\left(\Box \varphi_s \land \bigwedge_{i \in I_g} \Box \Diamond \varphi_{g,i}\right)
$$

上式中的符号逐项解释如下：

1. `$\varphi_{init}$` 描述初始条件。
2. `$\varphi_e$` 描述环境假设。
3. `$\varphi_{f,i}$` 是环境侧 fairness / liveness 条件。
4. `$\varphi_s$` 描述系统安全约束。
5. `$\varphi_{g,i}$` 是系统目标或 liveness guarantees。

receding-horizon 结构则通过对每个目标 `g_i` 建立偏序层次：

$$
P_i = (\{W_j^i\}, \preceq_{g_i})
$$

$$
\varphi_j^i =
\left((\nu \in W_j^i) \land \Box \varphi_e \land \bigwedge_{k \in I_f} \Box \Diamond \varphi_{f,k}\right)
\Rightarrow
\left(\Box \varphi_s \land \Box \Diamond (\nu \in F_i(W_j^i)) \land \Box \psi\right)
$$

上式中的符号逐项解释如下：

1. `$\{W_j^i\}$` 是围绕目标 `$g_i$` 划分出的状态层集合。
2. `$\preceq_{g_i}$` 是这些层之间的偏序。
3. `$\nu$` 表示当前离散抽象状态。
4. `$F_i(W_j^i)$` 是从层 `$W_j^i$` 出发的中间目标层。
5. `$\psi$` 是 receding-horizon invariant，用于保证局部规划拼接后仍保持全局正确性。

### 一个最小例子与通俗解释

可以把 `TuLiP` 想成“给有连续运动学的系统套上一层离散规划皮”。一个最小直觉例子是：

1. 小车在一组多边形区域之间移动，区域标签形成离散命题。
2. 环境可能关闭某些通道，或引入扰动。
3. 规格要求“小车最终到达目标区，并且始终避开禁区”。
4. `TuLiP` 先把连续动力学抽象成离散状态图，再综合满足规格的策略；若问题太大，则在 receding horizon 下分段规划。

通俗地说，`TuLiP` 像“把控制系统离散化后交给 reactive synthesis，再用滚动时域让求解别一下子爆掉”的工具箱。

### 运行 / 接受 / 转移语义

对连续 plant，运行语义由离散时间动力学给出；对离散抽象，执行语义可保守写成：

$$
T_{abs} \subseteq X_{abs} \times U_{abs} \times X_{abs}
$$

$$
(x,u,x') \in T_{abs} \iff \exists s \in \gamma(x),\ \exists d \in D,\ s' = As + Bu + Ed,\ s' \in \gamma(x')
$$

上式中的符号逐项解释如下：

1. `$X_{abs}$` 是抽象状态集合。
2. `$U_{abs}$` 是抽象控制动作集合。
3. `$\gamma(x)$` 表示抽象状态 `$x$` 对应的连续状态区域。
4. 若存在连续状态和扰动能把系统从 `$x$` 区域带到 `$x'$` 区域，则抽象转移存在。

对策略执行，论文强调 environment 被视为 adversary，因此控制器必须对所有 admissible 环境 profile 成立。这意味着其离散策略本质上是博弈策略，而不是单纯路径规划。

### 语义边界

1. 当前实现聚焦离散时间线性时不变系统与有界扰动，不是一般连续非线性系统的统一求解器。
2. 为了 tractability，论文强调采用 `GR(1)` 片段，而不是一般 `LTL`。
3. receding horizon 的正确性需要附加的 partial-order 与 invariant 条件，不是所有问题都能自动满足。
4. 工具的重点是 synthesis / planning toolchain，而不是最终部署时的运行时状态机框架。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 连续 plant 动力学 | `$s[t+1] = As[t] + Bu[t] + Ed[t]$` | `TuLiP` 当前支持的核心物理模型。 |
| `GR(1)` 规格骨架 | `$\varphi = (\varphi_{init} \land \Box \varphi_e \land \bigwedge \Box \Diamond \varphi_f) \Rightarrow (\Box \varphi_s \land \bigwedge \Box \Diamond \varphi_g)$` | synthesis 输入的主要逻辑片段。 |
| receding-horizon 分层 | `$P_i = (\{W_j^i\}, \preceq_{g_i})$` | 把大规划问题切成局部目标推进链。 |
| 局部子规格 | `$\varphi_j^i$` | 以 invariant 和 intermediate goal 拼接全局正确性。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 最终控制策略以 finite-state abstraction 与 automaton 形式表现。 |
| 事件 / 触发 | 中等支持 | 更多以环境 profile、离散区域与任务命题驱动，而非纯事件脚本。 |
| 守卫 / 数据 | 中等支持 | 连续状态通过抽象进入离散综合；正文主线不是复杂数据守卫 DSL。 |
| 层次 | 弱支持 | 非层次状态机工具。 |
| 并发 / 同步 | 中等支持 | 主要体现为 system vs environment 的博弈同步，而非并发组件代数。 |
| 时间约束 | 中等支持 | 使用离散时间步与 receding horizon，而不是 dense-time clocks。 |
| 连续动态 / 随机性 | 很强 | 连续 plant 与有界扰动是其核心切入点。 |
| 可执行 / 可验证性 | 很强 | abstraction、synthesis、counterexample、receding-horizon invariants 集成。 |

### 形式化问题与性质

1. `TuLiP` 的关键点不是“再做一个 `GR(1)` 求解器”，而是把 continuous plant abstraction 接到了 synthesis 入口。
2. receding horizon 不是启发式近似，而是通过足够条件与 invariant 来保留 correctness guarantee。
3. 工具明确把 environment 视为 adversary，因此比只考虑固定环境的 planning tool 更贴近 reactive synthesis。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 连续 plant 动力学矩阵与多面体约束。
2. 区域 / 命题标注形成的 proposition preserving partition。
3. `GR(1)` 规格。
4. partial-order 与 receding-horizon invariant 配置。

### 机器可处理承载方式

机器可处理承载方式包括：

1. finite state abstraction。
2. `GR(1)` synthesis problem。
3. 局部 horizon 规划子问题。
4. `JTLV` 可处理的离散综合输入与 counterexample 输出。

### 交换与互操作

1. 前端把连续 plant 离散化，再把离散问题交给 `JTLV`。
2. 结果既可用于离线规划，也可作为 receding-horizon 策略在线滚动执行。
3. 论文还计划接入 `Player/Stage` 与更一般的近似仿真 / 互模拟离散化工具。

## 配套基础设施

- 建模/编辑工具：Python-based toolbox，函数级 API 为主。
- 解析/交换/元模型支持：state-space partition、partial-order construction、counterexample handling。
- 仿真/执行支持：正文重点在 synthesis；后续计划与 `Player/Stage` 等仿真环境集成。
- 验证/分析支持：realizability 检查、counterexample 输出、receding-horizon sufficient-condition checking。
- 代码生成/转换支持：从 continuous plant 到 finite abstraction，再到 discrete strategy。
- 标准化或社区生态：依赖 `JTLV`，并与 `LTLMoP`、`Pessoa`、`LTLCon`、`conPAS2` 等同线工具形成对照生态。

## 适用场景与需求前提

### 适用场景

适合自主驾驶、航电管理、多目标跟踪等既包含连续 plant、又要求对抗式时序任务保证的 `CPS` 规划 / 控制综合场景。

### 需求前提

1. plant 需能抽象成有限状态模型，或至少能构造 proposition preserving partition。
2. 规格最好能落到 `GR(1)` 片段。
3. 环境行为需能描述为 admissible adversarial profiles。
4. 若采用 receding horizon，需要存在合适的 partial-order 与 invariant。

### 不适用或高成本场景

1. 若系统是高度非线性、强连续、且难以做有限抽象，建模成本会迅速上升。
2. 若需求远超 `GR(1)` 片段，后端 tractability 会受限。
3. 若问题根本不需要 adversarial environment，纯 planning tool 可能更轻。

## 与相邻形式主义的关系

相对 [ltlmop-experimenting-with-language-temporal-logic-and-robot-control/desc.md](../ltlmop-experimenting-with-language-temporal-logic-and-robot-control/desc.md)，`LTLMoP` 更偏 structured-English front-end 与 robot mission execution，而 `TuLiP` 更偏 continuous plant abstraction + `GR(1)` synthesis；相对 `Pessoa`，论文明确指出 `Pessoa` 支持 nonlinear / switched dynamics，但只支持更有限的 `LTL` 类；相对 `LTLCon / conPAS2`，`TuLiP` 的优势在于显式处理 adversarial environment 与 receding-horizon scaling。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 LLM 生成的状态机不必停在纯离散逻辑层，可以进一步接到 continuous plant abstraction。
2. `GR(1)` 规格与 receding-horizon invariant 为“生成-验证-修复”闭环提供了很清晰的中间接口。
3. 对抗式环境建模对控制系统需求尤其重要，能避免把环境默认成静态背景。

### 作为目标形式主义还是中间表示

更适合作为 high-value synthesis / planning 工具链和中间表示桥，而不是最终面向人工维护的主 DSL。

### 对需求到模型生成的启发

1. 若需求天然是“环境假设 + 控制目标”，可优先落到 `GR(1)` 骨架。
2. 对连续控制对象，状态机生成最好与抽象层联合设计，而不是完全脱离 plant。
3. invariant 与 counterexample 适合做自动修复反馈。

### 现实限制

它依赖离散抽象和 `GR(1)` tractability；对 richer continuous / temporal requirements 仍需更强后端或人工建模。

## 重要的相关工作

1. `JTLV`：正文明确给出作为底层 synthesis routine。
2. `LTLMoP`：与 `TuLiP` 同样考虑 adversarial environment，但更偏机器人任务。
3. `Pessoa / LTLCon / conPAS2`：作为 continuous abstraction + temporal planning 的直接对照工具。
4. receding-horizon temporal logic planning 主线：解释其为何能在 correctness 不丢失的前提下缩减求解规模。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`finite transition system abstraction / GR(1) synthesis / receding horizon temporal logic planning / TuLiP`
- 论文角色：embedded control synthesis toolbox with abstraction and receding-horizon planning
- 核心功能：把 continuous plant abstraction、`GR(1)` 综合和 receding-horizon planning 收进统一 Python 工具箱
- 关键特性：adversarial environment、finite abstraction、`JTLV` backend、partial-order layers、invariant checking、counterexamples
