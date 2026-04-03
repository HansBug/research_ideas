# 基于时序逻辑规格的多机器人任务协调 Petri 网 / Petri Net Based Multi-Robot Task Coordination from Temporal Logic Specifications

## 基本信息

- 标题：Petri Net Based Multi-Robot Task Coordination from Temporal Logic Specifications
- 中文标题：基于时序逻辑规格的多机器人任务协调 Petri 网
- 作者：Bruno Lacerda, Pedro U. Lima
- 发表：*Robotics and Autonomous Systems*, 122:103289, 2019
- DOI：`10.1016/j.robot.2019.103289`
- 链接：https://doi.org/10.1016/j.robot.2019.103289
- 形式主义：`Petri Net + Safe LTL + Supervisory Control`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：多机器人协调 / Petri 网监督控制
- 工具/实现获取方式：原文给出 `PN + DFA + safe LTL + supervisory control` 的完整算法，但未提供单独公开软件包。
- 标准/格式获取方式：承载方式是 labelled `PN`、safe `LTL`、`DFA` 与 admissibility procedure；原文未给独立交换格式。

## 简报

这篇论文的核心贡献，是把多机器人团队协调规则写成 safe `LTL`，再通过 `DFA + PN` 组合得到 supervisor candidate，而不是只把 Petri 网当作并发可视化工具。作者特别强调了 admissibility：合成出来的 supervisor 不能去禁止那些它根本控制不了的事件。

- 形式主义定位：面向 multi-robot coordination 的 `Petri Net` 监督控制框架，不是单纯任务流程图。
- 构造方式简述：先用 labelled `PN` 建 uncontrolled team model，再把 safe `LTL` 翻译成 `DFA`，随后组合并检查 admissibility。
- 基础设施与场景简述：依托 `safe LTL`、`DFA`、`PN` 结构分析与 supervisory control，服务物流、监测、维修与 task-assignment 类多机器人系统。

```text
multi-robot team model -> labelled Petri net -> safe LTL coordination rules -> DFA composition -> admissible PN supervisor -> coordinated execution
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. uncontrolled multi-robot team。
2. labelled Petri net model。
3. safe `LTL` coordination specifications。
4. `DFA` 形式的 specification automaton。
5. admissible supervisor。

### 核心抽象

原文直接定义了带事件标签的 Petri 网：

$$
G = \langle P, T, W^+, W^-, M_0, E, l \rangle
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合。
2. `T` 是 transition 集合。
3. `W^-` 是从 place 到 transition 的输入权矩阵。
4. `W^+` 是从 transition 到 place 的输出权矩阵。
5. `M_0` 是初始 marking。
6. `E` 是事件集合。
7. `l : T \to E` 是 transition 的事件标签函数。

输入/输出权向量写成：

$$
{}^\bullet t = W^-(\cdot, t), \qquad t^\bullet = W^+(\cdot, t)
$$

使能与 firing 语义分别是：

$$
t \text{ is enabled in } M \iff {}^\bullet t \le M
$$

以及

$$
M \xrightarrow{t} M' \iff M' = M - {}^\bullet t + t^\bullet
$$

上式中的符号逐项解释如下：

1. `M` 与 `M'` 是 firing 前后的 marking。
2. `${}^\bullet t` 是 firing 消耗的 token 向量。
3. `t^\bullet` 是 firing 产生的 token 向量。

论文还显式给出了行为语言：

$$
L_E^{fin}(G) = \{l(t_1)\cdots l(t_n) \mid M_0 \xrightarrow{t_1} M_1 \xrightarrow{t_2} \cdots \xrightarrow{t_n} M_n\}
$$

以及用于状态/事件联合推理的无限语言：

$$
L(G) \subseteq (E \times R(G))^\omega
$$

这使 safe `LTL` 可以同时对事件和 marking 约束进行推理。

### 一个最小例子与通俗解释

论文里的代表例子是“机器人执行任务并处理维修”的团队协调：

1. `idle_robots` 中有可用机器人 token。
2. 某个任务 `j_i` 进入系统后，transition 触发分配，token 从 idle 流向 working。
3. 若机器人执行中损坏，token 转到 `broken_robots` 和 incomplete-task queue。
4. 其他机器人可以尝试 repair，但 repair 结果可能成功、失败或发现不可修复。

通俗地说，这个模型像“多机器人协作流水线图”：token 同时代表机器人资源和任务占用状态，而 `LTL` 则像给这张并发网附上“哪些坏事永远不能发生”的规则。

### 运行 / 接受 / 转移语义

论文的一个关键点，是把 `LTL` 公式写到 `(event, marking)` 序列上，而不仅仅是事件 trace 上。可保守写成：

$$
\sigma = (e_0, M_0)(e_1, M_1)\cdots \in L(G)
$$

上式中的符号逐项解释如下：

1. `e_k` 是第 `k` 次 firing 对应的事件标签。
2. `M_k` 是对应时刻的 reachable marking。
3. 这样一来，公式既能约束“发生了什么”，也能约束“此时系统里还有多少 robot/job token”。

论文给出的典型 safe `LTL` 约束之一可压缩写成：

$$
\varphi = G\big((n_R - M(\mathrm{broken\_robots}) - M(\mathrm{dead\_robots}) \ge \sum_{j_i \in J} M(j_i\_\mathrm{in\_system})) \rightarrow X \neg \mathrm{replace\_robot}\big)
$$

上式中的符号逐项解释如下：

1. `n_R` 是系统中的机器人总数。
2. `M(\mathrm{broken\_robots})` 与 `M(\mathrm{dead\_robots})` 是当前不可用机器人数量。
3. `M(j_i\_\mathrm{in\_system})` 是任务 `j_i` 当前在系统中的数量。
4. 该式表示：如果当前剩余可用机器人还足够处理系统中的任务，就不应在下一步执行 `replace_robot`。

### 语义边界

这篇论文的边界也很清楚：

1. 它主要处理离散团队协调与并发资源约束，不直接建模连续轨迹控制。
2. 重点是 admissible supervisor synthesis，不是高精度运动规划。
3. `LTL` 公式必须落在 safe fragment 上，才适合这里的 `DFA` 翻译与监督控制流程。
4. 论文强调的是 team-level coordination，而不是每个单机器人内部控制器。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 标签化 Petri 网 | `$G = \langle P, T, W^+, W^-, M_0, E, l \rangle$` | 用并发网表示机器人资源、任务和故障。 |
| 使能条件 | `${}^\bullet t \le M$` | 所有资源前提到位后 transition 才能触发。 |
| firing 语义 | `$M' = M - {}^\bullet t + t^\bullet$` | token 直接编码团队状态更新。 |
| 可达 marking | `$R(G)$` | supervisor 与 `LTL` 都基于 reachable markings。 |
| 事件语言 | `$L_E^{fin}(G)$` | 监督回路中观察到的有限事件序列。 |
| 状态/事件语言 | `$L(G) \subseteq (E \times R(G))^\omega$` | 支持同时对事件与 marking 写公式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 部分支持 | 系统状态由 marking 分布表示，不是单控制状态机。 |
| 事件 / 触发 | 强支持 | transition 事件和 supervisor 控制是主体。 |
| 守卫 / 数据 | 支持 | 通过 marking 线性约束表达资源/数量条件。 |
| 层次 | 部分支持 | 论文主体不是层次网，但 supervisor 组合有结构化分层。 |
| 并发 / 同步 | 强支持 | Petri 网最核心的优势就在这里。 |
| 时间约束 | 不支持 | 这里不建显式时钟；时序由事件序控制。 |
| 连续动态 / 随机性 | 不支持 | 纯离散协调层。 |
| 可执行 / 可验证性 | 强分析 | 支持 `LTL` 规格、`DFA` 组合与 admissibility 检查。 |

### 形式化问题与性质

1. 这篇论文最重要的点，是把多机器人 coordination 从“写一个 plan”升级成“合成一个可证明 admissible 的 supervisor”。
2. `LTL` 不是只看事件，还能对 marking 线性约束建模，这一点很关键。
3. 与许多仅做 PN 建模的工作相比，它把 specification language 和 supervisor synthesis 接进来了。
4. 这使它成为 Petri 并发主干里非常典型的“规则驱动团队协调”应用条目。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下步骤：

1. 为多机器人系统建立 labelled `PN`。
2. 把 coordination rules 写成 safe `LTL`。
3. 将公式翻译成 `DFA`。
4. 将 `DFA` 与 `PN` 组合并验证 admissibility。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. labelled `PN`。
2. safe `LTL` formulas。
3. `DFA` specification automata。
4. admissibility verification procedure。

### 交换与互操作

互操作重点在：

1. 从 Petri 网行为语言到 `LTL/DFA` 规格层。
2. 从 `DFA` 再回到 supervisor `PN`。
3. 通过可控/不可控事件划分，把高层规则接到实际执行回路。

## 配套基础设施

- 建模/编辑工具：原文未绑定单一 `PN` 编辑器。
- 解析/交换/元模型支持：有 labelled `PN` 与 `DFA` 结构，但无统一交换标准。
- 仿真/执行支持：重点在 supervisor synthesis 与执行约束，而非仿真器细节。
- 验证/分析支持：safe `LTL`、`DFA` translation、admissibility checking。
- 代码生成/转换支持：论文强调 supervisor synthesis，但未提供公开代码生成器。
- 标准化或社区生态：依托 Petri nets、temporal logic 与 supervisory control 研究生态。

## 适用场景与需求前提

### 适用场景

适合物流、监测、任务分派、维修协作等多机器人团队协调问题，尤其适合高并发、资源共享和规则型安全约束明显的系统。

### 需求前提

1. 机器人/任务/资源状态能写成有限 marking。
2. 需要显式区分 controllable 和 uncontrollable events。
3. 协调要求可写成 safe `LTL` 或 marking 线性约束。
4. 关注点是团队级规则，而非底层连续控制器。

### 不适用或高成本场景

若主要困难是连续轨迹优化、感知不确定性或高维几何避障，仅靠此类离散 `PN + LTL` supervisor 不足，需要与 motion/hybrid 模型结合。

## 与相邻形式主义的关系

相对 [modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，本文更强调 specification-to-supervisor synthesis；相对 [long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md](../long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md)，它不追求长期收益优化，而是规则约束；相对 [a-petri-net-model-for-an-open-path-multi-agv-system/desc.md](../a-petri-net-model-for-an-open-path-multi-agv-system/desc.md)，它更偏 team-level temporal specification 与 controllability。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文直接表明：当需求里“永远不能发生什么”主导系统行为，而且对象是并发团队时，Petri 网比普通状态机更自然。

### 作为目标形式主义还是中间表示

对多机器人协调系统，它可以直接作为目标形式主义；对一般控制系统，它也适合作为并发/资源子系统的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把 event vocabulary、resource places 和 safety rules 一起抽出。
2. LLM 若生成的是 Petri 网，还应同步生成 controllable/uncontrollable 划分。
3. 当需求包含明确“坏事永不发生”口径时，safe `LTL` 是很自然的规格层。

## 重要的相关工作

- [modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)：更偏任务网与性能分析。
- [long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md](../long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md)：随机 Petri / reward 方向的多机器人扩展。
- [a-petri-net-model-for-an-open-path-multi-agv-system/desc.md](../a-petri-net-model-for-an-open-path-multi-agv-system/desc.md)：AGV 路径和资源占用建模。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心贡献是把多机器人协调规则写成 safe `LTL` 并合成 admissible `PN` supervisor。
- 其描述客体是并发团队资源与任务流，因此记为 `🏭`；论文语境是多机器人系统，因此记为 `🌡️`。
- 对 `project_1` 来说，它补的是“并发团队需求如何从自然语言规则走到可执行网模型”的关键链路。
