# 基于布尔规格的 Petri 网机器人规划 / Robot Planning Based on Boolean Specifications Using Petri Net Models

## 基本信息

- 标题：Robot Planning Based on Boolean Specifications Using Petri Net Models
- 中文标题：基于布尔规格的 Petri 网机器人规划
- 作者：Cristian Mahulea, Marius Kloetzer
- 发表：*IEEE Transactions on Automatic Control*, 63(7):2218-2225, 2018
- DOI：`10.1109/TAC.2017.2760249`
- 链接：https://doi.org/10.1109/TAC.2017.2760249
- 形式主义：`Petri Net with Outputs + Boolean ILP Planning`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：多机器人路径规划 / Petri 网应用与 ILP 规划
- 工具/实现获取方式：原文明确实现为 `Matlab` 上的 `RMTool` 扩展，并调用 `CPLEX`/LPP 求解器；文中称其为 freely-downloadable package。
- 标准/格式获取方式：承载方式是 `PN with outputs`、观测映射、Boolean 规格、`ILP` 约束和 firing-sequence reconstruction；无独立交换格式。

## 简报

这篇论文的价值，在于把“多机器人任务规格”从常见的 `LTL + product automaton` 路线换成了 `Petri Net + Boolean ILP` 路线。作者利用 `Petri Net` 对 identical robot team 的可扩展建模能力，把环境分区、机器人移动能力和 region-of-interest 观测统一成 `PN with outputs`，再把“访问/避免/最终驻留”这类布尔任务翻译成线性约束，最终用整数线性规划求得满足任务的机器人轨迹。

- 形式主义定位：面向 identical robot team 的 `Petri Net` 规划模型，不是一般 `LTL` 合成框架。
- 构造方式简述：先做 cell decomposition，再把相邻 cell 间移动建成 state-machine 型 `PN`，然后把布尔任务转成 `ILP`。
- 基础设施与场景简述：依托 `PN with outputs`、Boolean formula、`ILP`、`RMTool` 与 `CPLEX`，服务多机器人 region-based planning。

```text
environment partition -> PN with outputs -> Boolean region specification -> ILP -> firing sequence -> individual robot trajectories
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. ordinary `Petri Net` 的 places、transitions、flow matrix 和 marking。
2. 在 place 上附加观测映射得到的 `PN with outputs`。
3. 多机器人 team 的 token 化表示。
4. 区分“沿轨迹访问”和“最终停留”的 Boolean 规格变量。
5. 将 firing 序列翻译回 individual robot trajectories 的算法。

### 核心抽象

原文先把普通 `Petri Net` 定义为：

$$
N = (P, T, F)
$$

并给出 state equation：

$$
\tilde{m} = m + C \cdot \sigma
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合，对应环境分区单元。
2. `T` 是 transition 集合，对应相邻 cell 之间的移动能力。
3. `F` 是弧集合。
4. `C = Post - Pre` 是 token flow matrix。
5. `\sigma` 是 firing count vector。
6. `\tilde{m}` 是 firing 后得到的 marking。

作者随后定义 `PN with outputs`：

$$
Q = (N, m_0, \Pi, h)
$$

上式中的符号逐项解释如下：

1. `N` 是前述 `Petri Net`。
2. `m_0` 是初始 marking，token 个数对应机器人个数。
3. `\Pi` 是 region-of-interest 命题集合。
4. `h : P \to 2^\Pi` 是 observation map，指示某个 cell 满足哪些命题。

若 `v_{\Pi_i}` 是命题 `\Pi_i` 的特征向量，则命题激活条件写成：

$$
v_{\Pi_i} \cdot m > 0
$$

上式中的符号逐项解释如下：

1. `v_{\Pi_i}` 在所有满足区域 `\Pi_i` 的 places 上取 1。
2. `m` 是当前 marking。
3. 乘积大于 0 表示至少有一个机器人位于能满足 `\Pi_i` 的 cell 中。

### 一个最小例子与通俗解释

论文最直观的例子是多个 identical robots 在带若干兴趣区域的平面环境中完成布尔任务：

1. place 表示 cell，token 表示机器人。
2. 一个大写命题 `\Pi_i` 表示“某个机器人曾经访问过区域 `\Pi_i`”。
3. 一个小写命题 `\pi_i` 表示“最终有机器人停在区域 `\Pi_i`”。
4. 例如 `\neg \Pi_2 \land \Pi_1 \land \neg \pi_1 \land \pi_3 \land \pi_4 \land \pi_5` 表示：访问过区域 1、永远避开区域 2、最后不要停在区域 1、最终占据区域 3/4/5。

通俗地说，这个模型把“机器人是谁”弱化成“token 有几个”，把“去过哪、最后停哪”变成布尔命题，从而避免了多机器人 product automaton 的爆炸。

### 运行 / 接受 / 转移语义

论文对 Boolean 规格的语义区分得很清楚：

$$ \Pi_i \text{ is true on run } r \iff \exists j \in \{0,\ldots,|r|\},\ \Pi_i \in \|V \cdot m_j\| $$

$$ \pi_i \text{ is true on run } r \iff \Pi_i \in \|V \cdot m_{|r|}\| $$

上式中的符号逐项解释如下：

1. `r` 是一条由 firing 生成的 run。
2. `m_j` 是 run 中第 `j` 个 marking。
3. `V` 是由所有命题特征向量组成的矩阵。
4. 大写命题看“沿途是否访问”，小写命题只看“终点是否满足”。

针对最终状态约束，原文给出一个 `ILP`：

$$
\min \ \lambda w^T \sigma + \mu b
$$

$$
\text{s.t. } m = m_0 + C \sigma
$$

以及与布尔变量 `x_\gamma` 相关的一组线性约束。上式中的符号逐项解释如下：

1. `w` 是 transition 的平均移动代价。
2. `\sigma` 是 firing count vector。
3. `b` 用于上界化拥塞项 `\|Post \cdot \sigma\|_\infty`。
4. `\lambda,\mu` 分别权衡路径长度和潜在拥塞。

### 语义边界

这篇论文的边界很明确：

1. 机器人被假定为 identical tokens，不区分个体身份。
2. 规格只到 Boolean 级别，不表达一般时序顺序关系。
3. 环境是静态且已知的，并且可做 cell decomposition。
4. 重点是规划，不是在线反馈监督控制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PN` 基础骨架 | `$N = (P, T, F)$` | 描述环境分区和移动能力。 |
| state equation | `$\tilde{m} = m + C \sigma$` | 把机器人移动转成 marking 演化。 |
| `PN with outputs` | `$Q = (N, m_0, \Pi, h)$` | 把区域命题绑到网模型上。 |
| 命题激活 | `$v_{\Pi_i} \cdot m > 0$` | 判断某区域是否被至少一个机器人满足。 |
| 访问/终态语义 | `$\Pi_i$ vs $\pi_i$` | 区分沿途访问与最终停留。 |
| 规划目标 | `$\min \lambda w^T \sigma + \mu b$` | 在任务满足前提下优化距离和拥塞。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 直接表示 team 分布状态。 |
| 事件 / 触发 | 强支持 | transition firing 对应机器人在 cell 间移动。 |
| 守卫 / 数据 | 中等支持 | 主要通过 observation map 和线性约束表达。 |
| 层次 | 弱支持 | 重点不在层次控制。 |
| 并发 / 同步 | 强支持 | 多 token 自然表示多机器人并发。 |
| 时间约束 | 不支持 | 任务规格是 Boolean，不是 timed。 |
| 连续动态 / 随机性 | 弱支持 | 物理运动被离散成 cell 迁移。 |
| 可执行 / 可验证性 | 强规划 | 可求解 `ILP`，并把结果回译为机器人轨迹。 |

### 形式化问题与性质

1. 论文最关键的建模选择，是用 `Petri Net` 的 token 可扩展性替代多机器人 product automaton。
2. 布尔规格虽然表达力弱于 `LTL`，但换来了规模与求解上的可操作性。
3. `PN with outputs` 让 “region visit / final occupancy” 这类需求可以被线性编码。
4. 因而它是 `Petri Nets` 主干在多机器人布尔规划方向上的很强应用侧证。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 对环境做 cell decomposition。
2. 每个 cell 变成一个 place，相邻 cell 之间的移动变成 transition。
3. 根据区域覆盖关系建立 observation map `h`。
4. 把初始 robot deployment 转成初始 token distribution。
5. 将 Boolean 规格转成 `ILP` 约束并求解。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `PN with outputs`。
2. `Boolean` / `CNF` 规格。
3. `ILP` 变量与线性不等式。
4. firing sequence 到 robot strategies 的回译算法。

### 交换与互操作

互操作重点在：

1. 环境分区如何映射为 `PN` 结构。
2. 命题集合 `\Pi` 如何与 place 观测绑定。
3. `ILP` 求解结果如何转回 individual robot trajectories。

## 配套基础设施

- 建模/编辑工具：`Matlab` 上的 `RMTool` 扩展。
- 解析/交换/元模型支持：无独立 XML/JSON/元模型标准。
- 仿真/执行支持：原文给出仿真案例和轨迹重建方法。
- 验证/分析支持：`ILP` / `LPP` 求解、PN reachability reasoning。
- 代码生成/转换支持：支持从 `ILP` 解到 robot movement strategies 的算法化回译。
- 标准化或社区生态：依托 `Petri Net`、robot motion partition、`CPLEX` 和 `RMTool` 生态。

## 适用场景与需求前提

### 适用场景

适合 identical mobile robots 在静态已知环境中完成“访问哪些区域、避开什么区域、最后停在哪些区域”这类任务。

### 需求前提

1. 环境可稳定离散成有限 cell。
2. 机器人可被看作 identical tokens。
3. 任务可压成 Boolean region specifications。
4. 优化目标可接受用路径长度和拥塞上界近似。

### 不适用或高成本场景

如果任务需要显式顺序、时序逻辑、机器人个体身份约束或在线重规划，这种 `Boolean + PN + ILP` 方案的表达力会不够。

## 与相邻形式主义的关系

相对 [modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，本文更强调布尔任务满足而不是任务执行监控；相对 [petri-net-robotic-task-plan-representation-modelling-analysis-and-execution/desc.md](../petri-net-robotic-task-plan-representation-modelling-analysis-and-execution/desc.md)，它更偏规划求解而非 plan representation/execution；相对 [on-multi-robot-path-planning-based-on-petri-net-models-and-ltl-specifications/desc.md](../on-multi-robot-path-planning-based-on-petri-net-models-and-ltl-specifications/desc.md)，它牺牲时序表达力来换取更紧凑的 Boolean 编码。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求只是“访问/避免/终态占据”这类布尔区域约束时，并不一定要直接上 `LTL` 或更复杂协议模型，`Petri Net` 可以给出更紧凑的中间表示。

### 作为目标形式主义还是中间表示

对多机器人区域规划，它可以直接作为目标形式主义；对更复杂系统，它也可作为从自然语言区域任务到更高表达力时序模型之间的中间层。

### 对需求到模型生成的启发

1. 需求抽取时应区分“沿途访问”和“最终停留”。
2. 当机器人可交换且任务不区分个体身份时，用 token 比用独立 automata 更合适。
3. 若用户关心可解释的求解过程，把规格转成 `ILP` 约束往往比黑盒搜索更可维护。

## 重要的相关工作

- [modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)：更强调多机器人任务分析与执行。
- [petri-net-robotic-task-plan-representation-modelling-analysis-and-execution/desc.md](../petri-net-robotic-task-plan-representation-modelling-analysis-and-execution/desc.md)：Petri 网任务表示与执行路线。
- [on-multi-robot-path-planning-based-on-petri-net-models-and-ltl-specifications/desc.md](../on-multi-robot-path-planning-based-on-petri-net-models-and-ltl-specifications/desc.md)：结合 `LTL/Büchi` 的更强规格路线。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心贡献是把多机器人布尔区域规划压成 `PN with outputs + ILP` 求解链。
- 其描述客体是并发 robot team 的位置分布与资源流，因此记为 `🏭`；论文语境是 mobile robots / planning，因此记为 `🌡️`。
- 对 `project_1` 来说，它补足了“区域访问/避免 + identical team + 紧凑可解释规划”这一类需求的 `Petri Net` 证据。
