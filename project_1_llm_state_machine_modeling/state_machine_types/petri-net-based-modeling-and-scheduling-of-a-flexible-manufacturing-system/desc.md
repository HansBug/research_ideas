# 基于 Petri 网的柔性制造系统建模与调度 / Petri-Net Based Modeling and Scheduling of a Flexible Manufacturing System

## 基本信息

- 标题：Petri-Net Based Modeling and Scheduling of a Flexible Manufacturing System
- 中文标题：基于 Petri 网的柔性制造系统建模与调度
- 作者：C. W. Cheng, T. H. Sun, L. C. Fu
- 发表：*Proceedings of the 1994 IEEE International Conference on Robotics and Automation*, pp. 513-518, 1994
- DOI：`10.1109/ROBOT.1994.351246`
- 链接：https://doi.org/10.1109/ROBOT.1994.351246
- 形式主义：`Timed Place Petri Net (TPPN) for FMS Scheduling`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：柔性制造系统调度 / 定时位置 Petri 网应用建模
- 工具/实现获取方式：原文给出完整 FMS 原型、`TPPN` 建模规则、`Limited-Expansion A` 启发式搜索算法和台大自动化实验室 prototype FMS 验证，但未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `TPPN` 网结构、marking 序列和搜索算法；原文未使用 `PNML` 等交换标准。

## 简报

这篇论文把 FMS 里的机器、有限缓冲区、机器人和 `AGV` 都压进一个 `Timed Place Petri Net (TPPN)`，再把“从初始 marking 到最终 marking 的 firing sequence”直接解释成一条生产调度。为了避免完整 `A*` 搜索太吃内存，作者又提出 `Limited-Expansion A`，只保留 `OPEN` 中代价最小的前 `b` 个 marking，从而在可接受内存下找近优 schedule。

- 形式主义定位：属于 `Petri Nets / Timed Petri Nets` 在柔性制造调度上的应用条目，核心对象是资源 token 流、并发工序和带时长的 operation places。
- 构造方式简述：把 FMS 拆成 `Transportation Model` 与 `Process-Flow Model` 两个 `TPPN` 子网，place 分成 resource / operation / intermediate / control 四类，再用 firing sequence 搜索 schedule。
- 基础设施与场景简述：算法层是 `Limited-Expansion A`，工程场景是含机器、robot、buffer 和 `AGV` 的 prototype FMS。

```text
machines + buffers + robots + AGVs -> TPPN transportation/process-flow submodels -> marking search / firing sequence -> near-optimal FMS schedule
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. `Transportation Model`，描述 `AGV` 在各 stop 之间的移动和路权控制。
2. `Process-Flow Model`，描述零件工艺路线、机器占用和资源分配。
3. 四类 places：resource、operation、intermediate、control。
4. 从初始 marking 到最终 marking 的 firing sequence。
5. 基于 marking 搜索的 `Limited-Expansion A` 调度算法。

### 核心抽象

原文没有把 `TPPN` 写成单一标准元组，但根据其对 places、transitions、marking 和 place time 的描述，可保守整理为：

$$
N_{TPPN} = (P, T, F, M_0, \tau_P)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合。
2. `$T$` 是 transition 集合，原文中 transition 被视为瞬时 firing。
3. `$F \subseteq (P \times T) \cup (T \times P)$` 是流关系。
4. `$M_0$` 是初始 marking。
5. `$\tau_P : P_{op} \to \mathbb{R}_{\ge 0}$` 给 operation places 赋持续时间，其中 `$P_{op} \subseteq P$`。
6. 这个元组是根据原文“time is associated only with places and all transitions are instantaneous”做的保守整理。

place 语义在文中分为四类：

1. `Resource Places`：有 token 表示对应机器、机器人、`AGV` 或 stop control right 当前空闲可用。
2. `Operation Places`：token 表示某个加工/搬运动作正在执行，并携带持续时间。
3. `Intermediate Places`：token 表示前一操作已完成、等待下一操作。
4. `Control Places`：连接 `Transportation Model` 和 `Process-Flow Model`，传递跨子网事件/条件。

### 一个最小例子与通俗解释

可以把论文模型理解成一个最小 FMS 片段：

1. 一个零件 token 在输入 buffer 对应的 intermediate place 中等待。
2. 一个 robot/AGV 对应的 resource place 上有 token，表示搬运资源空闲。
3. 某个 transition firing 后，资源 token 被拿走，零件 token 进入 operation place，表示“正在搬运/加工”。
4. 经过 `\tau_P` 指定的持续时间后，token 流向下一 intermediate place，同时资源 place 重新得到 token。
5. 这一连串 firing 的顺序就是一条 schedule。

通俗地说，这个模型像“给每台机器、每辆 AGV 和每个缓冲区都发 token 的生产线网”。token 在哪里，系统状态就在哪里；token 按什么顺序走完从 `M_0` 到 `M_f`，那条路径就是调度方案。

### 运行 / 接受 / 转移语义

论文明确把 firing sequence 看成 schedule。可保守写成：

$$
M_0 \xRightarrow{\sigma} M_f,\qquad \sigma = t_1 t_2 \cdots t_n
$$

上式中的符号逐项解释如下：

1. `$M_0$` 是所有机器、robot、`AGV` 和 buffer 初始化后的初始 marking。
2. `$M_f$` 是所有目标零件加工/搬运完成后的最终 marking。
3. `$\sigma$` 是 firing sequence。
4. `$t_1,\dots,t_n \in T$` 是依次 firing 的 transitions。

搜索算法在每个 successor marking 上计算代价：

$$
M = \arg\min_{M' \in OPEN} f(M')
$$

并在 `OPEN` 超过容量 `b` 时，只保留代价较小的前 `b` 个 marking。原文给出的最坏复杂度可写成：

$$
O(bn)
$$

上式中的符号逐项解释如下：

1. `$b$` 是 `OPEN` list 的最大容量。
2. `$n$` 是问题中的 operation 总数。
3. 这一复杂度分析把 node cost evaluation 视为主要开销来源。

### 语义边界

这篇论文的边界主要有：

1. `TPPN` 假设 transition 瞬时发生、时间只挂在 places 上。
2. `Limited-Expansion A` 牺牲全局最优保证来换内存与时间可控。
3. 模型重点是 FMS routing / resource contention / scheduling，不讨论复杂连续运动控制。
4. 适合工艺路径和运输拓扑已知的制造系统，不适合高度不确定的在线感知规划。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TPPN` 骨架 | `$N_{TPPN} = (P, T, F, M_0, \tau_P)$` | 把资源、工序和时间统一进 timed place Petri net。 |
| 调度即 firing 序列 | `$M_0 \xRightarrow{\sigma} M_f$` | 从初始到最终 marking 的路径就是一条 schedule。 |
| 最佳下一步选择 | `$M = \arg\min_{M' \in OPEN} f(M')$` | 启发式搜索按估价函数扩展更优 marking。 |
| `OPEN` 剪枝 | `|OPEN| \le b` | 只保留有限个候选 marking 以控内存。 |
| 最坏复杂度 | `$O(bn)$` | 用近优性换取低于完整 `A*` 的内存和计算压力。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 直接表示资源占用和工序状态。 |
| 事件 / 触发 | 强支持 | 加工、搬运、路权释放等都由 transition firing 表示。 |
| 守卫 / 数据 | 部分支持 | 控制 places 可传事件条件，但复杂数据不是主线。 |
| 层次 | 部分支持 | transportation/process-flow 是结构化分解，但不是深层层次网语义。 |
| 并发 / 同步 | 强支持 | 资源竞争、并发工序和跨子网同步是核心。 |
| 时间约束 | 强支持 | operation places 显式带持续时间。 |
| 连续动态 / 随机性 | 不支持 | 不建模连续 ODE 或概率 firing。 |
| 可执行 / 可验证性 | 强分析、可调度实现 | marking 搜索直接产出可执行 schedule。 |

### 形式化问题与性质

1. 论文最有价值的点是把“FMS 调度问题”直接变成“在 timed Petri net 状态空间中找一条 marking 路径”。
2. `control places` 把运输子网和工艺子网连接起来，使跨资源协调仍保持网模型语义。
3. `Limited-Expansion A` 说明 Petri 网状态空间搜索可以和工程可用的启发式剪枝结合。
4. 对 `Petri` 主干来说，这篇论文是很早的制造系统应用侧证。

## 构造方式与承载格式

### 建模入口

建模过程可概括为：

1. 先列出机器、robot、`AGV`、buffer 和 stop control resources。
2. 为 transport 与 process flow 分别建立 `TPPN` 子网。
3. 用 control places 连接两个子网。
4. 指定初始/最终 marking 和 operation place 时间。
5. 在可达 marking 图上运行 `Limited-Expansion A` 搜索 schedule。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `TPPN` 网图。
2. marking / firing sequence。
3. `OPEN/CLOSE` 搜索表。
4. prototype FMS 的工艺时间与运输时间参数表。

### 交换与互操作

互操作重点在两个子网之间的控制 place 接口：

1. `Process-Flow Model` 发出 `AGV-call` 一类请求。
2. `Transportation Model` 根据路权和 push-AGV 规则移动载具。
3. 完成运输后再通过 control places 把状态返回工艺子网。

## 配套基础设施

- 建模/编辑工具：原文未指定 Petri 网专用建模器。
- 解析/交换/元模型支持：未使用 `PNML` 或独立元模型。
- 仿真/执行支持：在台大 Automation Lab prototype FMS 上做实现验证。
- 验证/分析支持：reachable marking search、`Limited-Expansion A`、adaptive scheduling。
- 代码生成/转换支持：原文未提供自动代码生成，但 firing sequence 可直接解释为生产调度。
- 标准化或社区生态：建立在 Petri nets / FMS scheduling 传统线上，而非标准交换生态。

## 适用场景与需求前提

### 适用场景

适合含机器、机器人、`AGV`、有限缓冲区和共享路权的柔性制造系统调度，尤其适合“要同时看并发资源占用和工序时间”的 FMS。

### 需求前提

1. 工艺路线、机器集合、buffer 结构和运输拓扑要能明确列出。
2. 各 operation 的持续时间要可参数化。
3. 关键资源竞争关系适合用 token 表示。
4. 调度目标能转成 marking 路径代价函数。

### 不适用或高成本场景

如果主要问题是高维连续轨迹控制、视觉感知不确定性或高度动态重构拓扑，单靠这种 `TPPN + heuristic search` 不够直接。

## 与相邻形式主义的关系

相对 [application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md](../application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md)，本文更强调完整 FMS 子网分解和 `A*` 风格 marking 搜索，而不是用 invariants 直接推 cycle time；相对 [time-petri-nets/desc.md](../time-petri-nets/desc.md)，本文是具体制造应用上的 `TPPN` 工程化条目；相对 [a-petri-net-model-for-an-open-path-multi-agv-system/desc.md](../a-petri-net-model-for-an-open-path-multi-agv-system/desc.md)，本文更早且更偏 FMS 工艺+运输联合调度。

## 与本研究的关系

### 对 Project 1 的价值

它说明：当需求里出现“共享机器/机器人/AGV 资源、有限 buffer、工艺顺序、运输路权、近优调度”时，`Petri` 网比普通 FSM 更自然，因为 marking 本身就能表达资源并发状态。

### 作为目标形式主义还是中间表示

对制造调度问题，`TPPN` 可以直接作为目标形式主义；对一般控制系统，它也可以作为并发资源层的中间模型。

### 对需求到模型生成的启发

1. 需求抽取应显式区分 resource / operation / intermediate / control 四类 place 语义。
2. “从初始状态到目标状态的一条可行调度”可以直接对齐到 firing sequence。
3. 若后续还要自动优化，状态机生成时最好把代价函数和剪枝参数也留下接口。

### 现实限制

论文算法不保证最优解，且 `TPPN` 建模仍要求工艺和运输结构先被高质量离散化。

## 重要的相关工作

### 奠基或前身工作

1. 原文直接把 Petri nets 用作 FMS 并发行为建模基础。
2. `A*` 与 beam/staged search 是 `Limited-Expansion A` 的算法背景。

### 同类型或同家族工作

1. [application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md](../application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md) 是另一篇制造调度 timed Petri 应用条目。
2. [a-petri-net-model-for-an-open-path-multi-agv-system/desc.md](../a-petri-net-model-for-an-open-path-multi-agv-system/desc.md) 和 [petri-net-approach-of-collision-prevention-supervisor-design-in-port-transport-system/desc.md](../petri-net-approach-of-collision-prevention-supervisor-design-in-port-transport-system/desc.md) 分别把 `Petri` 应用拓展到多 `AGV` 通行安全和港口运输监督控制。

### 标准 / 格式 / 工具链工作

1. 原文未使用 `PNML` 等标准格式。
2. 其重点是网模型 + 搜索算法 + 原型系统验证。

### 与本研究关系最紧的工作

1. 它为“从制造资源需求到 Petri 网并发模型”提供了很直接的 place 类型划分模板。
2. 对 `project_1` 来说，这种模板可以帮助 LLM 在资源调度类需求上少走 `FSM` 硬编码路线。

## 文献分类总结

- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 形式主义：`Timed Place Petri Net (TPPN) for FMS Scheduling`
- 论文角色：柔性制造系统调度 / 定时位置 Petri 网应用建模
- 核心功能：用 `TPPN` 表达 FMS 并发资源流，并把 firing sequence 解释成 near-optimal schedule
- 关键特性：resource/operation/intermediate/control places、AGV routing、control-place coupling、`Limited-Expansion A`
- 构造方式：`Transportation Model + Process-Flow Model` 双子网 + marking 搜索
- 基础设施：prototype FMS、heuristic marking search、adaptive scheduling
- 适用场景：机器/机器人/`AGV`/buffer 共享下的柔性制造调度
- 需求前提：工艺路线、运输拓扑和操作时长需可离散化
- 状态：🟢
