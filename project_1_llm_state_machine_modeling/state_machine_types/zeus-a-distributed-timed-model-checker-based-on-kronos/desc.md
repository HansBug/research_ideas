# Zeus：基于 KRONOS 的分布式定时模型检验器 / Zeus: A Distributed Timed Model-Checker Based on Kronos

## 基本信息

- 标题：Zeus: A Distributed Timed Model-Checker Based on Kronos
- 中文标题：Zeus：基于 KRONOS 的分布式定时模型检验器
- 作者：V. Braberman，A. Olivero，F. Schapachnik
- 发表：*Electronic Notes in Theoretical Computer Science*，Vol. 68 No. 4，pp. 503-522，2002
- DOI：`10.1016/S1571-0661(05)80389-5`
- 链接：https://doi.org/10.1016/S1571-0661(05)80389-5
- 形式主义：`Timed Automata / KRONOS / Zeus`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：distributed timed model-checking backend evolving from `KRONOS`
- 工具/实现获取方式：原文明确说明 `Zeus` 是从 `KRONOS` 演化出的 distributed timed model checker；正文未给稳定公开仓库或下载页。
- 标准/格式获取方式：主承载是 `Timed Automata`、`TCTL` reachability、zones / regions、`DBM` 与控制图划分结果；不是独立中立交换标准。

## 简报

这篇论文补的是 `KRONOS` 这条 timed-automata 工具线的分布式扩展母线。它不是重新定义 timed automata，而是试图回答一个更工程化的问题：既然 `KRONOS` 的瓶颈主要来自状态空间爆炸和内存耗尽，那么能否把后向 fixpoint 计算分散到多台机器上，同时尽量少通信、少上下文切换、少浪费空闲时间？`Zeus` 的回答是一套围绕控制图预分区、message piggybacking、delayed messaging 和 dead-time utilization 设计出来的分布式验证架构。

- 形式主义定位：`Timed Automata / KRONOS` 的分布式验证基础设施，而不是新的时间自动机子类。
- 构造方式简述：先沿用 `KRONOS` 的 timed-automata + region / zone symbolic semantics，再把控制图按分区映射到不同 capsule，由各自 fix-point engine、router、embassy 和 connector 协作。
- 基础设施与场景简述：依托 `KRONOS`、`DBM`、non-convex regions、`METIS` 图划分、piggybacking 与 delayed messaging，服务大规模 timed reachability / `TCTL` verification。

```text
timed-automata network -> backward fixpoint over zones/regions -> graph partition -> distributed region exchange -> global reachability answer
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `KRONOS` 风格 timed automata。
2. zones、regions 与 `DBM`。
3. backward `TCTL` reachability fixpoint。
4. a priori control-graph partitioning。
5. `Zeus` distributed architecture。

### 核心抽象

基础建模对象仍可保守写成：

$$
A = (L, \ell_0, C, E, Inv)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 locations 集合。
2. `$\ell_0$` 是初始 location。
3. `$C$` 是 clocks 集合。
4. `$E$` 是带 guards / resets 的迁移集合。
5. `$Inv$` 是不变式集合。

`KRONOS/Zeus` 的符号对象不是单个 valuation，而是非凸区域。可保守整理为：

$$
R = \bigcup_{i=1}^{m} Z_i
$$

上式中的符号逐项解释如下：

1. `$Z_i$` 是单个 convex zone。
2. 每个 `$Z_i$` 通常用 `DBM` 表示。
3. `$R$` 是论文中所说的 region，即 non-convex set。
4. 分布式传播的核心单位就是这些 region。

后向 reachability 的 fixpoint 可写成：

$$
R_0 = Goal,\qquad R_{k+1} = R_k \cup Pre(R_k)
$$

上式中的符号逐项解释如下：

1. `$Goal$` 是目标状态集合。
2. `$Pre(\cdot)$` 是前驱算子。
3. 迭代直到稳定得到最小不动点。
4. 初始状态是否落入该 fixpoint 就是 reachability 问题的答案。

### 一个最小例子与通俗解释

论文实验使用了 Train-Gate-Controller 一类 timed case study。可以把 `Zeus` 的工作方式理解成：

1. 整个 timed-automata 控制图被事先划分给多台机器。
2. 每台机器只负责自己那块 location partition 的 region 前驱计算。
3. 当某块 region 的前驱需要穿过分区边界时，再通过 embassy / connector 交换消息。
4. 若某台机器暂时空闲，它不会干等，而会压缩 region 表示，提前为后续计算减负。

通俗地说，`Zeus` 像是把 `KRONOS` 的后向搜索拆成多名协作者：每人盯着自己的一块图，只有真正需要跨区时才发消息，而且尽量顺手把下次会用到的信息一起捎上。

### 运行 / 接受 / 转移语义

timed automata 的基本语义步仍可保守写成：

$$
(\ell, \nu) \xrightarrow{d} (\ell, \nu + d)
$$

$$
(\ell, \nu) \xrightarrow{e} (\ell', \nu[X := 0])
$$

上式中的符号逐项解释如下：

1. `$\ell,\ell'$` 是离散位置。
2. `$\nu$` 是 clocks valuation。
3. `$d \ge 0$` 是延时。
4. `$e$` 是离散迁移事件。
5. `$X := 0$` 表示相应 clocks 被 reset。

`Zeus` 关注的是分布式 fixpoint，而不是重新定义局部语义。它的核心判定可保守写成：

$$
Init \subseteq R^\ast
$$

上式中的符号逐项解释如下：

1. `$Init$` 是初始状态集合。
2. `$R^\ast$` 是 fixpoint 稳定后的前驱闭包。
3. 若包含关系成立，则目标可达。
4. 这正对应论文所说“final answer is whether the initial states belong to the computed fix point”。

控制图分区可进一步抽成：

$$
\mathcal{P} : L \to \{1,\ldots,n\}
$$

上式中的符号逐项解释如下：

1. `$\mathcal{P}$` 把 location 映到处理节点编号。
2. `$n$` 是 processing nodes 数量。
3. 论文当前版本使用 `METIS` 对控制图做 a priori partitioning。

### 语义边界

1. `Zeus` 处理的是 `KRONOS` 风格 timed reachability / `TCTL` reachability，不是一般 hybrid systems。
2. 它的主贡献是 distributed backend architecture，而非 নতুন的 timed logic。
3. 论文强调异步并行版本很难获得理想 speedup，这本身就是其工程结论之一。
4. 当前版本优先验证后向 reachability，完整 `TCTL` 扩展被视为自然延伸而非已完全解决。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed-automata 骨架 | `$A = (L, \ell_0, C, E, Inv)$` | `Zeus` 继承的 `KRONOS` 建模对象。 |
| region 表示 | `$R = \bigcup_i Z_i$` | non-convex symbolic state。 |
| 后向 fixpoint | `$R_{k+1}=R_k \cup Pre(R_k)$` | reachability 核心算法。 |
| 判定条件 | `$Init \subseteq R^\ast$` | fixpoint 完成后的最终回答。 |
| 分区函数 | `$\mathcal{P}:L \to \{1,\ldots,n\}$` | distributed execution 的结构骨架。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心仍是 network of timed automata 的离散位置加 clocks。 |
| 事件 / 触发 | 很强 | 沿用 `KRONOS` 的 guards / resets / synchronization 语义。 |
| 守卫 / 数据 | 中等支持 | 重点在 clocks symbolic manipulation，不是 rich data 程序分析。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 很强 | 主要体现在 distributed backend 和 capsule coordination。 |
| 时间约束 | 很强 | `DBM`、zones、`TCTL` reachability 是主轴。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / probabilistic line。 |
| 可执行 / 可验证性 | 很强 | 已实现分布式 prototype，并报告速度与瓶颈分析。 |

### 形式化问题与性质

1. `Zeus` 的创新不在语义本体，而在 distributed symbolic backend 的架构组织。
2. `METIS` 预分区和 piggybacking 说明 timed verification 里通信模式非常关键。
3. 论文把“空闲时间用于 region compression”作为一等设计点，这很适合做工具谱系挂钩。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `KRONOS` 风格 timed automata 模型。
2. `TCTL` reachability 目标。
3. 控制图分区结果。
4. distributed capsules 间的 region 交换。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `DBM` 表示的 zones。
2. non-convex regions。
3. partitioned control graph。
4. network messages 中携带的 delta regions。

### 交换与互操作

互操作重点不在公开交换标准，而在 `KRONOS` 继承与分布式执行层：

1. `Zeus` 直接演化自 `KRONOS`。
2. `METIS` 被用于控制图划分。
3. distributed execution 通过 router / embassy / connector 协调局部与远端 region storage。

## 配套基础设施

- 建模/编辑工具：论文主体不强调新前端，默认继承 `KRONOS` 模型输入。
- 解析/交换/元模型支持：基于 timed-automata 控制图、zones / regions 和 partition 结果。
- 仿真/执行支持：重点不是 simulation，而是 distributed fixpoint execution。
- 验证/分析支持：backward `TCTL` reachability、symbolic propagation、distributed storage / messaging。
- 代码生成/转换支持：不主打代码生成；核心是 symbolic state 传播与压缩。
- 标准化或社区生态：依托 `KRONOS`、`DBM`、`METIS` 和 distributed model-checking 研究线。

## 适用场景与需求前提

### 适用场景

适合大状态空间 `Timed Automata` reachability / `TCTL` analysis，尤其适合内存压力大、单机 `KRONOS` 难以承载的实时系统验证。

### 需求前提

1. 系统需已落成 `Timed Automata`。
2. 关注点主要是 reachability 或可压成 fixpoint 风格的 `TCTL` 子问题。
3. 控制图分区确实能减少跨节点通信。
4. 分布式部署成本值得换取状态空间扩展能力。

### 不适用或高成本场景

如果问题规模并不大、模型无法有效分区，或主要瓶颈不在 symbolic state storage，分布式 `Zeus` 可能得不偿失。

## 与相邻形式主义的关系

相对 [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)，`KRONOS` 是单机 timed symbolic checking 母线，而 `Zeus` 是其 distributed backend 延长线；相对 [dtron-a-tool-for-distributed-model-based-testing-of-time-critical-applications/desc.md](../dtron-a-tool-for-distributed-model-based-testing-of-time-critical-applications/desc.md)，两者都强调分布式，但 `DTRON` 面向 timed testing runtime，`Zeus` 面向 timed model checking；相对 [obsslice-a-timed-automata-slicer-based-on-observers/desc.md](../obsslice-a-timed-automata-slicer-based-on-observers/desc.md)，`ObsSlice` 是送检前 slicing，`Zeus` 是实际 distributed checking backend。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明一旦目标形式主义落到 `Timed Automata`，验证基础设施的可扩展性会很快成为实际瓶颈。
2. 对“生成 - 验证 - 修复”闭环而言，后端是否支持大型模型决定了模型粒度上限。
3. 也提示我们：工具谱系里的 distributed / runtime / bridge 条目虽然不进主树节点，但对实际可用性很关键。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Timed Automata` 可能是目标形式主义，而 `Zeus` 明显是验证基础设施后端。

### 对需求到模型生成的启发

1. 若后续希望自动生成较大 timed models，必须同步考虑后端 partitionability。
2. clocks 与 location graph 结构会直接影响 distributed verification 成本。
3. “先补工具母线再补方法路线”在 timed 方向尤其重要。

## 重要的相关工作

1. [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)：`Zeus` 的直接母线。
2. [obsslice-a-timed-automata-slicer-based-on-observers/desc.md](../obsslice-a-timed-automata-slicer-based-on-observers/desc.md)：`KRONOS/OpenKronos` 周边 slicing 工具。
3. [dtron-a-tool-for-distributed-model-based-testing-of-time-critical-applications/desc.md](../dtron-a-tool-for-distributed-model-based-testing-of-time-critical-applications/desc.md)：另一条 distributed timed 基础设施路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / KRONOS / Zeus`
- 论文角色：distributed timed model-checking backend evolving from `KRONOS`
- 核心功能：把 `KRONOS` 的后向 timed reachability 扩展到 graph-partitioned distributed execution
- 关键特性：`DBM`、regions、`METIS` 预分区、piggybacking、delayed messaging、dead-time utilization
- 构造方式：`TA -> backward fixpoint over regions -> partitioned distributed propagation`
- 基础设施：`Zeus` architecture、`KRONOS`、`DBM`、router / embassy / connector / coordinator
- 适用场景：大规模实时系统 reachability、`TCTL` 子问题、单机内存吃紧的 timed verification
- 需求前提：系统需落成 `Timed Automata` 且控制图适合分区
- 状态：🟢
