# 基于度量区间时序逻辑的运动规划定时自动机方法 / Timed Automata Approach for Motion Planning Using Metric Interval Temporal Logic

## 基本信息

- 标题：Timed Automata Approach for Motion Planning Using Metric Interval Temporal Logic
- 中文标题：基于度量区间时序逻辑的运动规划定时自动机方法
- 作者：Yuchen Zhou, Dipankar Maity, John S. Baras
- 发表：arXiv preprint arXiv:1603.08246, 2016
- DOI：原文未提供
- 链接：https://arxiv.org/abs/1603.08246
- 形式主义：`Timed Automata / MITL Input-Output Timed Automaton`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：机器人运动规划 / `MITL` 驱动的定时自动机应用建模
- 工具/实现获取方式：原文明确给出 `MITL2Timed` 工具、`PyUPPAAL` 自动建模脚本与 GitHub 仓库入口。
- 标准/格式获取方式：承载方式是 `MITL` 公式、`IOTA`、地图抽象定时自动机 `T_map` 与 `UPPAAL` 模型；原文未给独立交换标准。

## 简报

这篇论文的重点，不是单纯把机器人路径规划写成 reachability，而是把“带明确时间窗口的高层任务”先写成 `MITL`，再系统地翻译成定时自动机并交给 `UPPAAL` 求一条满足约束的有限时间轨迹。作者的路线非常直接：地图先做 cell decomposition，运动时间由动力学估计；任务约束先变成 `MITL`；然后 `MITL -> IOTA -> product TA -> UPPAAL query`。

- 形式主义定位：面向机器人高层时序任务规划的 `Timed Automata` 应用框架，不是新的时钟自动机本体。
- 构造方式简述：先把地图抽象成 `T_map`，再把 `MITL` 公式编译成 `Input Output Timed Automaton (IOTA)`，最后做 product 并求 `E<> final`。
- 基础设施与场景简述：依托 `MITL2Timed`、`PyUPPAAL`、`UPPAAL` 与 cell decomposition，服务带 deadline / 周期 survey / 顺序访问约束的机器人规划问题。

```text
高层时间任务 -> MITL 公式 -> IOTA -> 与地图 TA 做乘积 -> UPPAAL 查询 -> 满足时序约束的有限轨迹
```

## 形式主义定义与核心对象

### 定义对象

论文处理的核心对象包括：

1. 原子命题与 `MITL` 任务公式。
2. `MITL` 到 `IOTA` 的转换结果。
3. 由 cell decomposition 得到的地图定时自动机 `T_map`。
4. `IOTA \times T_map` 的 product automaton。
5. `UPPAAL` 中的终态可达性查询。

### 核心抽象

论文首先给出 `MITL` 语法：

$$
\varphi ::= \top \mid \pi \mid \neg \varphi \mid \varphi \lor \varphi \mid \varphi\ U_I\ \varphi
$$

上式中的符号逐项解释如下：

1. `\pi` 是原子命题。
2. `U_I` 是带时间区间 `I` 的 timed until。
3. 其他布尔与时序算子如 `\Diamond_I`、`\Box_I` 都可由此派生。

其关键语义是：

$$
(\xi,t) \models \varphi_1 U_I \varphi_2
\iff
\exists s \in I,\ (\xi,t+s)\models \varphi_2 \land \forall s' \le s,\ (\xi,t+s')\models \varphi_1
$$

其中：

1. `\xi` 是布尔轨迹。
2. `t` 是当前时间点。
3. `s` 是满足 `\varphi_2` 的未来时间偏移。
4. 在 `s` 到来之前，`\varphi_1` 必须持续成立。

为了进入自动机求解，论文定义了输入输出定时自动机：

$$
A = (\Sigma, Q, \Gamma, C, \lambda, \gamma, I, \Delta, q_0, F)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入字母表。
2. `Q` 是离散状态集合。
3. `\Gamma` 是输出字母表。
4. `C` 是时钟变量集合。
5. `\lambda: Q \to \Sigma` 给状态赋输入标记。
6. `\gamma: Q \to \Gamma` 给状态赋输出标记。
7. `I` 是状态不变式。
8. `\Delta` 是带 guard 与 reset 的转移关系。
9. `q_0` 是初始状态。
10. `F` 是需反复访问的 `Buchi` 接受状态集合。

### 一个最小例子与通俗解释

论文给了一个非常直观的例子：机器人需要先访问区域 `A`，再在区间 `[l,r]` 内访问区域 `B`。该约束写成：

$$
\varphi = (\neg B\ U\ A) \land (\Diamond_{[l,r]} B)
$$

通俗地说，这相当于告诉系统：

1. 在看到 `A` 之前，不允许先碰到 `B`。
2. 但 `B` 又不能无限晚，必须在规定时间窗里出现。
3. 地图自动机负责“哪些位置可走、走一格要多久”。
4. `IOTA` 负责“这些位置序列是否满足时序公式”。

因此，这种方法像“给地图再叠一层会计时的逻辑监工”。

### 运行 / 接受 / 转移语义

论文的整体求解骨架可以压缩为：

$$
\mathcal{T}_{plan} = T_{map} \times A_{\varphi}
$$

其中：

1. `T_{map}` 是由地图与机器人动力学估计得到的 timed automaton。
2. `A_{\varphi}` 是由 `MITL` 公式翻译得到的 `IOTA`。
3. 乘积后的状态同时编码“机器人在哪”和“公式满足到哪一步”。

论文对 timed eventually 的处理，是把一个算子拆成 generator 与 checker 两个自动机，并共享时钟变量。典型移动或逻辑转移都带 guard 与 reset，例如：

$$
z > 0 \mid z := 0
$$

上式中的符号逐项解释如下：

1. `z` 是对应逻辑子式的时钟。
2. `z > 0` 是 guard。
3. `z := 0` 表示该逻辑阶段重新计时。

最终满足性检查被转成 `UPPAAL` 查询：

$$
E\langle\rangle\ final
$$

这里的 `final` 是作者额外加的终态，用来接住所有满足有限接受条件的路径。也就是说，只要 product automaton 中存在一条能到 `final` 的有限运行，这条路径就可作为满足 `MITL` 约束的规划解。

### 语义边界

这篇论文的边界主要是：

1. 地图必须先被离散成 cells，底层连续控制被抽象掉。
2. 单步移动时间需要能由动力学保守估计。
3. 重点是有限时间轨迹满足，不处理一般无限运行控制综合。
4. 任务公式主要围绕 `MITL` 的 bounded-time 约束，而不是概率或博弈语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `MITL` 语法 | `$\varphi ::= \top \mid \pi \mid \neg \varphi \mid \varphi \lor \varphi \mid \varphi U_I \varphi$` | 用显式时间区间表达任务。 |
| `MITL` 语义 | `$(\xi,t)\models \varphi_1 U_I \varphi_2$` | 明确“何时必须满足、此前必须维持什么”。 |
| `IOTA` 元组 | `$A = (\Sigma, Q, \Gamma, C, \lambda, \gamma, I, \Delta, q_0, F)$` | 逻辑约束被编译成带时钟的自动机。 |
| 乘积规划模型 | `$\mathcal{T}_{plan} = T_{map} \times A_{\varphi}$` | 把地图约束与逻辑约束合并。 |
| 时钟迁移 | `$z > 0 \mid z := 0$` | 逻辑阶段推进依赖显式时钟守卫与复位。 |
| 满足性查询 | `$E\langle\rangle final$` | 直接用 `UPPAAL` 找到满足 `MITL` 的有限路径。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 地图位置与逻辑进度都被离散状态化。 |
| 事件 / 触发 | 强支持 | 区域命题变化与逻辑算子推进是核心。 |
| 守卫 / 数据 | 强支持 | 时钟 guard、命题标签与地图邻接共同决定转移。 |
| 层次 | 弱支持 | 主要是 product automaton，不走层次状态机路线。 |
| 并发 / 同步 | 部分支持 | generator/checker 通过共享时钟和同步信号协作。 |
| 时间约束 | 强支持 | 整个方法就是围绕 bounded temporal constraints 展开。 |
| 连续动态 / 随机性 | 弱连续、无随机 | 连续运动只被估时抽象，不显式建模随机性。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 直接给可行路径和最短时间解。 |

### 形式化问题与性质

1. 论文真正补的是“如何把 `MITL` 任务落成一个可求解的 timed automata product”，而不只是展示某个时钟模型。
2. 其关键工程点在于 generator / checker 分解与 `PyUPPAAL` 自动建模。
3. 这一框架适合时间窗口型任务，而不是几何最优控制。
4. 因而它是 `Timed Automata` 主干上一条很典型的高层任务规划应用线。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 对地图做 cell decomposition。
2. 估计相邻 cells 之间的移动时间并构造 `T_map`。
3. 把 `MITL` 公式转换成 `IOTA`。
4. 对两者做乘积并生成 `UPPAAL` 模型。

### 机器可处理承载方式

原文直接给出的机器可处理承载方式包括：

1. `MITL` 公式。
2. `IOTA` 定义与其 generator/checker 自动机。
3. 地图定时自动机 `T_map`。
4. `UPPAAL` XML 模型与 `E<> final` 查询。

### 交换与互操作

互操作重点在：

1. 逻辑层的 `MITL` 如何编译成 `IOTA`。
2. 运动层的地图抽象如何赋命题标签。
3. `PyUPPAAL` 如何把 product automaton 直接落到验证器输入。

## 配套基础设施

- 建模/编辑工具：`MITL2Timed`、`PyUPPAAL`。
- 解析/交换/元模型支持：以 `MITL`、`IOTA` 和 `UPPAAL` 模型为主，无独立交换标准。
- 仿真/执行支持：重点是 `UPPAAL` symbolic search，而不是运行时控制器执行。
- 验证/分析支持：`UPPAAL` 可做 reachability、最短时间路径与 diagnostic trace。
- 代码生成/转换支持：论文实现了从逻辑公式到 `UPPAAL` 模型的自动生成。
- 标准化或社区生态：依托 `MITL`、timed automata 和 `UPPAAL` 生态。

## 适用场景与需求前提

### 适用场景

适合机器人周期巡检、带访问顺序的区域到访、时间窗口任务和其他“高层时序要求强于连续轨迹细节”的规划问题。

### 需求前提

1. 环境可离散为有限 cells。
2. 单步移动时间可保守估计成区间或常值。
3. 高层任务能写成 `MITL` 公式。
4. 低层控制器能可靠执行高层给出的 cell-to-cell 移动。

### 不适用或高成本场景

如果环境极度连续、命题标签难以稳定定义、或底层执行时间强不确定，这套 `MITL + TA` 管线的建模成本会显著上升。

## 与相邻形式主义的关系

相对 [Multi-Robot Planning: A Timed Automata Approach](../multi-robot-planning-a-timed-automata-approach/desc.md)，本文把任务入口从 reachability/`CTL` 推到了 `MITL`；相对 [Transforming Robotic Plans with Timed Automata to Solve Temporal Platform Constraints](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)，本文更强调“从公式直接合成路径”，后者更强调“从既有计划修正到平台可执行轨迹”；相对纯 `MITL` satisfiability 工作，它给出了明确机器人规划落地链路。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求中直接出现“先后访问 + 时间窗口 + 周期约束”时，`Timed Automata` 可以把自然语言时序要求较直接地吸纳进形式模型。

### 作为目标形式主义还是中间表示

对带显式时序约束的任务规划，它可以直接作为目标形式主义；对更复杂控制系统，也很适合作为“时间约束层”的中间表示。

### 对需求到模型生成的启发

1. 高层需求中的时序词应尽量被抽成 `MITL` 而非仅停留在自然语言。
2. 地图和任务可分两层建模，再通过 product 合并。
3. 若后续要接验证器，自动生成 `UPPAAL` 模型的链路值得优先保留。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文所有建模仍建立在经典定时自动机主干之上。
- [Multi-Robot Planning: A Timed Automata Approach](../multi-robot-planning-a-timed-automata-approach/desc.md)：同样是机器人规划，但任务入口更偏 reachability。
- [Transforming Robotic Plans with Timed Automata to Solve Temporal Platform Constraints](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)：同样把 `TA` 用于机器人计划时序修正。

## 文献分类总结

- 这是一篇 `⏱️` 类高价值应用条目，核心贡献是把 `MITL` 任务公式系统地编译到可求解的 timed automata product。
- 它的描述客体是机器人高层行为与任务逻辑，因此记为 `🎛️`；论文语境面向机器人/CPS 规划，因此记为 `🌡️`。
- 对 `project_1` 来说，它提供了“需求中的时间约束如何进入状态机建模与验证链”的非常直接的样板。
