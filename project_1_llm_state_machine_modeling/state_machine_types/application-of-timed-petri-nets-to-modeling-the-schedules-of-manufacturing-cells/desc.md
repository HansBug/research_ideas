# 使用定时 Petri 网对制造单元调度建模 / Application of Timed Petri Nets to Modeling the Schedules of Manufacturing Cells

## 基本信息

- 标题：Application of Timed Petri Nets to Modeling the Schedules of Manufacturing Cells
- 中文标题：使用定时 Petri 网对制造单元调度建模
- 作者：W. M. Zuberek
- 发表：*INRIA/IEEE Symposium on Emerging Technologies and Factory Automation (ETFA'95)*, Vol. 2, pp. 311-322, 1995
- DOI：`10.1109/ETFA.1995.496672`
- 链接：https://doi.org/10.1109/ETFA.1995.496672
- 形式主义：`Timed Petri Net Schedules for Manufacturing Cells`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：制造单元调度 / 定时 Petri 网应用建模
- 工具/实现获取方式：原文给出完整 timed Petri net 与 colored Petri net 构造；未给出单独代码，但公开提交版 PDF 可直接复现公式和建模规则。
- 标准/格式获取方式：承载方式是 timed Petri nets、colored Petri nets 和 invariant analysis；原文未给出独立交换格式。

## 简报

这篇论文做的不是一般“用 Petri 网画流程”，而是把制造单元里的机器人搬运调度写成可分析 cycle time 的 timed Petri nets。作者先从简单调度开始，把 `In -> M1 -> M2 -> M3 -> Out` 这样的机器人动作序列压成 timed net，再证明 composite schedules 可以由 simple schedules 交织得到，最后用 invariants 直接算出不同调度的吞吐率和最优 cycle time。

- 形式主义定位：属于 `Timed Petri Nets` 在制造/机器人单元调度中的应用条目，重点是并发资源流与周期性能分析。
- 构造方式简述：先把机器人搬运动作和机器加工动作变成 transition / place，再给 transition 赋 firing time，用 place invariants 推导周期。
- 基础设施与场景简述：依托 timed/colored `Petri Nets` 与 invariant analysis，面向 flexible manufacturing cells / robotic cells 的节拍优化。

```text
机器人搬运序列 + 机器加工时长 -> timed Petri net / colored Petri net -> invariant-based cycle-time analysis -> optimal schedule selection
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. simple schedules：每个周期恰有一个新零件进入、一个零件离开。
2. composite schedules：每个周期有多个零件进出。
3. timed Petri net 中的 places、transitions、marking 和 firing times。
4. 用于统一表示整个调度族的 colored Petri nets。
5. 由 place invariants 导出的 cycle time 和 throughput。

### 核心抽象

原文没有把 timed net 写成单一元组，但根据其对 places、transitions、marking 和 firing times 的定义，可保守整理为：

$$
N = (P, T, F, M_0, f)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合，表示条件，如“零件已装载”“机器加工结束”“机器人位于某处”。
2. `$T$` 是 transition 集合，表示机器加工或机器人搬运动作。
3. `$F$` 是流关系。
4. `$M_0$` 是初始 marking。
5. `$f : T \to \mathbb{R}_{\ge 0}$` 给每个 transition 赋 firing time。

论文明确采用 timed net 的三阶段 firing 语义：transition 开始时从输入 place 取走 token，经过 firing period 后再把 token 放到输出 place。可保守写成：

$$
M \xrightarrow{t,\ f(t)} M'
$$

上式中的符号逐项解释如下：

1. `$M$` 和 `$M'$` 分别是 firing 前后的 marking。
2. `$t$` 是正在执行的 transition。
3. `$f(t)$` 是该 transition 的持续时间。

对 simple schedules，作者直接枚举 3-machine cell 的六种调度，例如：

$$
A : (0,0,0) \to (1,0,0) \to (0,1,0) \to (0,0,1) \to (0,0,0)
$$

上式中的符号逐项解释如下：

1. 每个三元组表示 `M1/M2/M3` 是否装载工件。
2. `1` 表示该机器当前装有工件，`0` 表示空闲。
3. 调度 `$A$` 对应工件依次流经 `M1 -> M2 -> M3 -> Out`。

### 一个最小例子与通俗解释

论文最小例子就是 3-machine cell 的 schedule A：

1. 机器人从 `In` 取件并送到 `M1`。
2. `M1` 加工结束后，机器人卸下并送到 `M2`。
3. 再由 `M2` 送到 `M3`，最后送到 `Out`。
4. 机器人再空载回到 `In`，形成一个完整周期。

通俗地说，这个模型像一个“带工时的并发生产线网”。token 表示工件位置和资源占用状态，transition 表示机器加工或机器人搬运，一旦把时间赋给 transition，就能直接推导节拍。

### 运行 / 接受 / 转移语义

对 schedule A 的 timed net，机器加工 transition 与机器人动作 transition 共同构成一个周期。原文用 invariant analysis 直接给出其最小 cycle time：

$$
\tau_0 = \max(\tau_1, \tau_2, \tau_4)
$$

其中

$$
\tau_1 = o_1 + u + v + 2w + 4y
$$

$$
\tau_2 = o_2 + o_3 + 3v + 2w + x + 5y
$$

$$
\tau_4 = o_3 + u + 3v + 3w + x + 9y
$$

上式中的符号逐项解释如下：

1. `$o_1,o_2,o_3$` 是 `M1,M2,M3` 的加工时间。
2. `$u$` 是 pickup 时间。
3. `$v$` 是 unload 时间。
4. `$w$` 是 load 时间。
5. `$x$` 是 drop 时间。
6. `$y$` 是相邻机器之间的 travel 时间。

对 colored net 表达的整个 simple-schedule 家族，作者给出：

$$
\tau_{opt} = \min(\tau_A, \tau_B, \tau_C, \tau_D, \tau_E, \tau_F)
$$

上式中的符号逐项解释如下：

1. `$\tau_A \dots \tau_F$` 分别是六种简单调度的周期时间。
2. 最优调度就是 cycle time 最小的那一个。

### 语义边界

这篇论文的边界主要有：

1. 主要分析 steady-state throughput，不处理随机故障与实时重调度。
2. 假设零件类型、搬运路径和相邻 travel time 可以被简化。
3. 机器与机器人动作被抽成固定 duration transition。
4. 强项是结构分析和符号 cycle-time 公式，不是复杂可达性行为诊断。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed net 骨架 | `$N = (P, T, F, M_0, f)$` | 把调度写成带 firing time 的 Petri net。 |
| schedule A | `$A : (0,0,0) \to (1,0,0) \to (0,1,0) \to (0,0,1) \to (0,0,0)$` | 用 machine occupancy 序列定义 simple schedule。 |
| firing 语义 | `$M \xrightarrow{t,\ f(t)} M'$` | transition 持续一段真实时间后更新 marking。 |
| simple schedule 周期 | `$\tau_0 = \max(\tau_1,\tau_2,\tau_4)$` | cycle time 由最慢 invariant subnet 决定。 |
| 家族最优周期 | `$\tau_{opt} = \min(\tau_A,\tau_B,\tau_C,\tau_D,\tau_E,\tau_F)$` | 可在调度族内比较并选最优。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | place 直接编码工件位置、机器占用和机器人位置。 |
| 事件 / 触发 | 强支持 | 机器加工完成和机器人搬运动作都对应 transition。 |
| 守卫 / 数据 | 部分支持 | 重点是结构与时长，不在复杂数据变量。 |
| 层次 | 部分支持 | simple / composite / colored family 构成弱层次。 |
| 并发 / 同步 | 强支持 | 机器加工与机器人移动天然并发。 |
| 时间约束 | 强支持 | firing time 与 cycle time 分析是主体。 |
| 连续动态 / 随机性 | 无连续、弱随机 | 本文使用确定时长分析，不讨论连续动力学。 |
| 可执行 / 可验证性 | 强分析 | invariant analysis 直接导出吞吐率与节拍公式。 |

### 形式化问题与性质

1. 论文最有价值的部分是“从机器人动作序列机械地构造 timed net”。
2. 它把 schedule 族统一成 colored net，使“选哪条调度更优”变成同一模型上的比较问题。
3. 通过 invariants，它避免了完整 reachability 爆炸。
4. 对 `Timed Petri Nets` 主干来说，这是制造单元与机器人搬运应用的经典代表。

## 构造方式与承载格式

### 建模入口

建模过程可以概括为：

1. 先列出 cell configuration 序列。
2. 再把 configuration 差分转成机器人搬运动作序列。
3. 把机器加工与搬运动作映射成 timed net。
4. 用 invariants 推导周期与吞吐率。

### 机器可处理承载方式

原文使用的承载方式包括：

1. simple schedules 的配置序列。
2. timed Petri net 图结构与 transition firing time。
3. composite schedule 的交织构造。
4. colored Petri nets 对整个调度族的统一表示。

### 交换与互操作

互操作重点不在文件标准，而在“调度序列 -> timed net / colored net”：

1. 机器人动作序列可机械映射到 net 结构。
2. multiple schedules 可在 colored net 中共存。
3. 输出直接是符号化 cycle-time 公式，便于后续优化。

## 配套基础设施

- 建模/编辑工具：原文未指定专用编辑器。
- 解析/交换/元模型支持：未给出独立交换格式。
- 仿真/执行支持：重点不在在线执行，而在离线调度分析。
- 验证/分析支持：invariant analysis。
- 代码生成/转换支持：原文给出从 schedule 序列到 net 的系统化构造规则。
- 标准化或社区生态：建立在 `Petri Nets` / `Timed Petri Nets` / `Colored Petri Nets` 传统分析线上。

## 适用场景与需求前提

### 适用场景

适合 flexible manufacturing cells、robotic cells、机器加工与机器人搬运并发耦合的节拍优化问题。

### 需求前提

1. 调度能表示成有限 configuration 序列。
2. 机器加工和机器人搬运时间可以参数化。
3. 重点关心 throughput / cycle time，而不是复杂业务数据。
4. 系统并发结构适合用 token 流和资源占用表达。

### 不适用或高成本场景

当系统存在强非确定故障、复杂实时抢占、多种异构零件和高维控制逻辑时，仅靠这种结构化 timed net 会显得过简。

## 与相邻形式主义的关系

相对 [time-petri-nets/desc.md](../time-petri-nets/desc.md)，本文更偏制造调度应用与周期性能分析；相对 [coloured-petri-nets/desc.md](../coloured-petri-nets/desc.md)，它把 color 明确用来编码整个调度族；相对 [modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，本文更关注 steady-state manufacturing cell 的节拍与最优 schedule。

## 与本研究的关系

### 对 Project 1 的价值

它说明：如果需求中存在“并发加工 + 共享机器人搬运 + 周期性能指标”，Petri 网比普通状态机更自然，因为 token / invariant 能直接表达资源流和节拍。

### 作为目标形式主义还是中间表示

对制造单元调度问题，它可以直接作为目标形式主义；对一般控制逻辑问题，它也适合作为并发资源子系统的中间表示。

### 对需求到模型生成的启发

1. 需求抽取应包括资源位置、搬运动作、加工时长和路径结构。
2. 若最终目标是 throughput / cycle time，结构分析可能比纯 reachability 更高效。
3. 对一整族相似调度，color 是天然的压缩表示。

### 现实限制

建模前提较强，需要调度与时间参数先被结构化；它不直接覆盖复杂的异常恢复与在线重规划。

## 重要的相关工作

### 奠基或前身工作

1. 原文直接建立在 `Petri Nets`、timed nets 和 invariant analysis 的传统上。
2. 作者同时引用了 manufacturing cell scheduling 与 robot cell throughput 优化文献。

### 同类型或同家族工作

1. 本文把 simple / composite schedules 明确分开，为后续更复杂生产单元调度研究提供了模板。
2. colored nets 在文中承担了“统一表示调度族”的角色。

### 标准 / 格式 / 工具链工作

1. 论文没有绑定某个具体软件工具，重点是分析方法而不是工具产品。
2. 结构化 invariant analysis 是其最关键的基础设施。

### 与本研究关系最紧的工作

1. 对 `project_1` 而言，它是“并发/资源流型需求为什么要转 Petri 而非纯 FSM”的直接证据。
2. 它也提示后续验证场景生成时，可以把 throughput/cycle time 当成显式分析目标。

## 文献分类总结

- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 形式主义：`Timed Petri Net Schedules for Manufacturing Cells`
- 论文角色：制造单元调度 / 定时 Petri 网应用建模
- 核心功能：把制造单元 simple/composite schedules 统一建成 timed / colored Petri nets 并分析节拍
- 关键特性：并发资源流、firing time、invariant analysis、colored family representation
- 构造方式：configuration 序列 -> 机器人动作序列 -> timed net / colored net
- 基础设施：timed/colored Petri nets、invariant analysis
- 适用场景：flexible manufacturing cells、robotic cell scheduling、throughput 优化
- 需求前提：动作序列和时间参数可结构化枚举
- 状态：🟢
