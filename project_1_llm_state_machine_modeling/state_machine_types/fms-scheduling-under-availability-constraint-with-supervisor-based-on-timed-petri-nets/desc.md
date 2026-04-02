# 可用性约束下基于时间 Petri 网监督器的 FMS 调度 / FMS Scheduling under Availability Constraint with Supervisor Based on Timed Petri Nets

## 基本信息

- 标题：FMS Scheduling under Availability Constraint with Supervisor Based on Timed Petri Nets
- 中文标题：可用性约束下基于时间 Petri 网监督器的 FMS 调度
- 作者：Mohamed Ali Kammoun、Wajih Ezzeddine、Nidhal Rezg、Zied Achour
- 发表：*Applied Sciences*, 7(4): 399, 2017
- DOI：`10.3390/app7040399`
- 链接：https://doi.org/10.3390/app7040399
- 形式主义：`Timed Petri Net + TMG Decomposition`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🏭
- 论文角色：FMS 调度 / availability-aware Timed Petri Net 监督控制
- 工具/实现获取方式：原文明确给出 `TPN` 建模、`TMG` 分解、`MILP` 求解和 `GA` 求解流程，并说明使用 `Xpress` 优化器。
- 标准/格式获取方式：承载方式是 `Timed Petri Net`、`Timed Marked Graph`、数学规划模型与 supervisor synthesis；原文未提供独立交换标准。

## 简报

这篇论文不是只用 `Petri Nets` 画一个调度流程，而是把柔性制造系统的作业顺序、资源容量和预防性维护窗口，一起压成可分解的 `Timed Petri Net`。作者先把原始 `TPN` 分解成一组 `TMG`，再从这些结构性质推导 `MILP`，求出最优 firing sequence，最后把这条 firing sequence 回写成 manufacturing supervisor。

- 形式主义定位：这是 `Timed Petri Net` 在制造调度与监督控制中的应用条目，重点是结构分解和 supervisor synthesis。
- 构造方式简述：先建立含 resource places 的原始 `TPN`，再分解成 `TMG` 集合，加入 timed direct arcs 与 extra time，最后用 `MILP/GA` 求调度并综合 supervisor。
- 基础设施与场景简述：依托 `TPN`、`TMG`、`Xpress` 和 genetic algorithm，适合制造系统 makespan 优化与维护约束下的调度。

```text
FMS jobs + machines + maintenance windows -> timed Petri net -> TMG decomposition + MILP / GA -> firing sequence -> supervisor synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. 初始 `Timed Petri Net` 的 places、transitions、arcs、weights 和 firing time。
2. 从 `TPN` 分解出来的 `Timed Marked Graphs`。
3. 作业顺序变量和维护前后位置变量。
4. 以 firing sequence 为中心的数学规划模型。
5. 最终回写到 decomposed `TPN` 上的 supervisor。

### 核心抽象

原文把 `TPN` 定义为：

$$
TPN = (P, T, O, W, h(T))
$$

上式中的符号逐项解释如下：

1. `$P$` 是 places 集合。
2. `$T$` 是 transitions 集合。
3. `$O$` 是 place-to-transition 与 transition-to-place 的直接弧集合。
4. `$W$` 是弧权函数。
5. `$h(T)$` 给每个 transition 赋予静态时间。

论文进一步关心 `TPN` 的 `TMG` 子类。可保守整理为：

$$
\forall p \in P,\ |\mathrm{In}(p)| = |\mathrm{Out}(p)| = 1,\quad W \in \{0,1\}
$$

上式中的符号逐项解释如下：

1. `$\mathrm{In}(p)$` 和 `$\mathrm{Out}(p)$` 分别表示 place 的输入与输出 transitions。
2. 该式表示每个 place 只连接一个前驱和一个后继。
3. 同时弧权被限制为 `0/1`，这正是 `Timed Marked Graph` 的结构特征。

对分解，论文给出：

$$
T = \bigcup_{i=1}^{n} T_i,\quad P = \left(\bigcup_{i=1}^{n} P_i\right) \cup P_R
$$

上式中的符号逐项解释如下：

1. `$T_i$` 是作业 `$i$` 的 transition 子集。
2. `$P_i$` 是作业 `$i$` 的内部 places。
3. `$P_R$` 是资源 places。
4. 分解后每个 `$TMG_i=(P_i,T_i,O_i,W_i,h(T_i))$` 表示单个作业的 free-dynamic。

### 一个最小例子与通俗解释

论文给出的最小例子是“两台机器、两类作业、两段维护窗口”的 FMS：

1. 先构造带资源 places 的原始 `TPN`。
2. 再去掉资源 places，把每个 job 拆成自己的 `TMG`。
3. 用 timed direct arcs 指定“谁先谁后”的可能顺序。
4. 若下一台机器正在维护，就给相应 transition 增加 extra time。

通俗地说，这个模型像“把每个作业自己的加工链先拆开，再用一层约束告诉它们什么时候能抢机器、什么时候必须等维护结束”。

### 运行 / 接受 / 转移语义

论文把优化目标写成：

$$
\min \max_{i=1,\ldots,n} H(t_{i,m})
$$

上式中的符号逐项解释如下：

1. `$H(t_{i,m})$` 是作业 `$i$` 在最后一台机器上的全局 firing 完成时刻。
2. 最大值对应整个生产计划的 makespan。
3. 最小化它，就是找最优调度序列。

约束中最核心的一条是单个作业的顺序加工：

$$
H(t_{i,j+1}) - H(t_{i,j}) \ge h(t_{i,j+1})
$$

上式中的符号逐项解释如下：

1. `$h(t_{i,j+1})$` 是作业 `$i$` 在机器 `$j+1$` 上的加工时间。
2. 该式保证作业必须按工艺顺序前进，且不能提前开始下一道工序。

论文还要求 supervisor 最终能够把解出的 firing sequence 回写到 decomposed `TPN` 中，因此调度结果不是停留在表格层，而是能重新变成带控制含义的网模型。

### 语义边界

这篇论文的边界包括：

1. 它主要面向离散制造作业与维护窗口，不涉及复杂连续控制动力学。
2. 求解效率建立在 `TPN -> TMG` 分解和特定结构假设上。
3. `GA` 提供近优解而非一般全局最优证明。
4. 重点是离线调度与 supervisor synthesis，不是在线重规划。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TPN` 元组 | `$TPN = (P, T, O, W, h(T))$` | 定义制造系统的时间网骨架。 |
| `TMG` 条件 | `$\forall p,\ |\mathrm{In}(p)| = |\mathrm{Out}(p)| = 1$` | 给出分解目标子网的结构特征。 |
| 分解框架 | `$T=\cup_i T_i,\ P=(\cup_i P_i)\cup P_R$` | 把整体 `TPN` 拆成作业级 `TMG` 与资源层。 |
| makespan 目标 | `$\min \max_i H(t_{i,m})$` | 以最后完成时间为优化目标。 |
| 顺序约束 | `$H(t_{i,j+1}) - H(t_{i,j}) \ge h(t_{i,j+1})$` | 保证作业工艺顺序与非抢占加工。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | places / transitions / markings 显式表示作业与资源状态。 |
| 事件 / 触发 | 强支持 | transition firing 就是调度事件。 |
| 守卫 / 数据 | 强支持 | 作业顺序变量、维护窗口和 extra time 都进入约束。 |
| 层次 | 强支持 | 原始 `TPN`、分解后的 `TMG`、求解模型和 supervisor 四层非常清楚。 |
| 并发 / 同步 | 强支持 | 多作业共享资源与互斥加工是主体。 |
| 时间约束 | 强支持 | firing time、makespan 和 maintenance window 都是核心。 |
| 连续动态 / 随机性 | 不适用 | 本文不讨论连续动力学和随机 firing。 |
| 可执行 / 可验证性 | 强分析、强综合 | 既能求最优序列，也能回写 supervisor。 |

### 形式化问题与性质

1. 论文最关键的贡献是把“求调度序列”和“综合 supervisor”连成同一条链。
2. `TMG` 分解让大规模 `TPN` 调度问题获得了更可控的结构。
3. 维护窗口通过二值变量进入 `MILP`，使 availability 不再是后验修补。
4. 对 `Timed Petri Net` 主干来说，这是制造系统调度与监督控制结合得很紧的一篇应用条目。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先按机器和作业建立原始 `TPN`。
2. 引入 resource places 表示容量约束。
3. 再分解为 job-level `TMG`。
4. 最后把顺序变量、维护变量和 supervisor 参数写入优化模型。

### 机器可处理承载方式

原文涉及的机器可处理承载方式包括：

1. `TPN` / `TMG` 图结构。
2. 决策变量 `$A(t_{i,j}, t_{i',j-1})$` 与 `$Z_{i,j+1}$`。
3. `MILP` 约束系统。
4. `GA` 染色体编码与 supervisor synthesis 步骤。

### 交换与互操作

互操作重点不在开放标准，而在“模型 -> 优化 -> 监督器”：

1. `TPN` 分解结果进入数学规划。
2. 最优 firing sequence 再回写到 decomposed `TPN`。
3. 得到的 supervisor 由 digital controllers 执行。

## 配套基础设施

- 建模/编辑工具：原文未指定专用网编辑器。
- 解析/交换/元模型支持：无独立交换格式。
- 仿真/执行支持：最终 supervisor 与数字控制器耦合执行。
- 验证/分析支持：`MILP`、`Xpress`、genetic algorithm。
- 代码生成/转换支持：给出从 firing sequence 到 supervisor 的系统化合成流程。
- 标准化或社区生态：建立在 `Petri Nets / Timed Petri Nets / scheduling optimization` 传统线上。

## 适用场景与需求前提

### 适用场景

适合柔性制造系统、受维护影响的加工车间、离散作业型生产系统，以及需要把调度结果重新落成 supervisor 的场景。

### 需求前提

1. 作业路线和加工时间可参数化。
2. 资源容量可离散成 places / tokens。
3. 维护窗口可写成显式时间区间。
4. 关注点是 makespan 与调度合法性，而不是复杂连续控制。

### 不适用或高成本场景

若系统有大规模在线扰动、复杂返工逻辑或强随机故障，仅靠本文的离线 `TPN + MILP/GA` 框架会不够灵活。

## 与相邻形式主义的关系

相对 [application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md](../application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md)，本文更强调 availability constraint 与 supervisor synthesis；相对 [time-petri-nets/desc.md](../time-petri-nets/desc.md)，它不讨论一般状态类方法，而是把时间网直接压到制造调度；相对 [task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md](../task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md)，它更侧重生产排序与维护约束而不是装配任务控制逻辑。

## 与本研究的关系

### 对 Project 1 的价值

它说明当需求包含“资源共享 + 时间代价 + 维护窗口 + 合法调度”时，`Petri Net` 比纯状态机更自然，因为 firing sequence、容量和约束可以一起进入模型。

### 作为目标形式主义还是中间表示

对制造调度问题，它完全可以是目标形式主义；对更一般控制问题，它也适合作为并发资源调度层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要显式记录机器、作业、容量和维护窗口。
2. 若目标是调度最优性，就应尽早把时间参数和资源约束放进模型，而不是后期再补。
3. supervisor synthesis 可以直接建立在优化结果之上，这对“生成-验证-修复”闭环很有启发。

### 现实限制

本文的解法对结构化制造系统很强，但对高度动态、在线重调度和非标准工艺流仍需额外机制。

## 重要的相关工作

- [application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md](../application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md)：制造单元定时 `Petri Net` 调度的早期代表。
- [time-petri-nets/desc.md](../time-petri-nets/desc.md)：时间 `Petri Net` 主线条目。
- [task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md](../task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md)：将 `Petri` 监督控制落到机器人装配控制。

## 文献分类总结

- 这是一篇 `🕸️` 类应用条目，核心贡献是用 `TPN` 分解、`MILP/GA` 求解和 supervisor synthesis 打通 FMS 调度闭环。
- 其描述客体是离散作业与资源流网络，因此记为 `🏭`；应用场景显然属于工业制造控制，因此领域记为 `🏭`。
- 对状态机族演化树而言，它补强的是 `Timed Petri Net` 主干在制造调度与维护约束上的应用证据，不单独生成新节点。
