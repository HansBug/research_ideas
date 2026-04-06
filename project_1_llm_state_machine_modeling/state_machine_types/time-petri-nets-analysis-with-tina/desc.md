# TINA：时间 Petri 网分析工具 / Time Petri Nets Analysis with TINA

## 基本信息

- 标题：Time Petri Nets Analysis with TINA
- 中文标题：TINA：时间 Petri 网分析工具
- 作者：Bernard Berthomieu，Francois Vernadat
- 发表：*Third International Conference on the Quantitative Evaluation of Systems (QEST 2006)*，pp. 123-124，2006
- DOI：`10.1109/QEST.2006.56`
- 链接：https://projects.laas.fr/tina/papers/qest06.pdf
- 形式主义：`Time Petri Nets / TINA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：time-Petri-net analysis environment
- 工具/实现获取方式：原文明确给出 `Tina (TIme Petri Net Analyzer, http://www.laas.fr/tina)` 作为软件环境入口。
- 标准/格式获取方式：原文明确说明 `Tina` 接受 graphical / textual 输入，并支持 `PNML`；输出可导出为多种 textual / binary formats 供外部 checker 使用。

## 简报

这篇短文的价值，在于把 `Time Petri Nets` 的分析母线真正落实成完整工具箱。`TINA` 不只是画网和跑仿真，而是同时覆盖 reachability / coverability / invariants、persistent sets / covering steps、state class graph、observer-based realtime checking、外部 checker backend 与 `PNML` 输入承载，基本把 `Time Petri Net` 的工程工具链骨架一次性说清了。

- 形式主义定位：面向 `Petri Net / Time Petri Net` 的分析环境与工具箱，而不是新的时间网语义。
- 构造方式简述：输入可以是图形或文本 `PN/TPN` 模型，内部先转成 abstract timed transition systems，再按要保留的性质选择 state-space construction。
- 基础设施与场景简述：依托 front-end、exploration engine、API、back-end printers 与外部 checker 接口，服务实时嵌入式系统、`TOPCASED/OpenEmbeDD/SPICES` 等工程项目。

```text
PN / TPN model -> Tina front-end / PNML -> abstract timed transition system -> state-space abstraction / model checking / path analysis -> checker output
```

## 形式主义定义与核心对象

### 定义对象

这篇论文的主体虽然是工具，但其工作对象始终是 `Time Petri Nets`：

1. 库所 `P` 与变迁 `T`。
2. 基础 `Pre/Post` 流网络。
3. 与变迁绑定的 firing delay intervals。
4. 由 marking 与时间约束组成的 state classes。
5. observer、path analysis 与外部 model checking 所依赖的抽象状态空间。

### 核心抽象

结合本文与本库已有 `Time Petri Nets` 条目，可把 `TINA` 直接处理的模型骨架写成：

$$
N = (P, T, Pre, Post, m_0, I_s)
$$

上式中的符号逐项解释如下：

1. `P` 是库所集合。
2. `T` 是变迁集合。
3. `Pre` 与 `Post` 分别给出输入/输出弧权重。
4. `m_0` 是初始 marking。
5. `I_s` 是把每个变迁映到静态 firing interval 的函数。

论文进一步说明，`Time Petri Nets` 的无限状态空间会被压成 state classes：

$$
C = (m, D)
$$

上式中的符号逐项解释如下：

1. `m` 是当前 marking。
2. `D` 是记录时间信息的 polyhedral domain。
3. `TINA` 的 `state class graph` 系列工具，正是围绕这样的抽象节点组织。

### 一个最小例子与通俗解释

最小直觉可以这样理解：

1. 一个 token 进入某个 place 以后，对应变迁 `t` 被使能。
2. `t` 不能立刻 firing，而是必须在自己的时间窗口内触发。
3. 如果系统并发很强，直接枚举每条 interleaving 会爆炸，于是 `TINA` 用 persistent sets、covering steps 和 state classes 做压缩。
4. 对使用者来说，`TINA` 不只是“看这张网能不能跑”，而是“在保留关键性质的前提下，把巨大的 timed state space 压到还能分析的规模”。

通俗地说，`TINA` 像“时间 Petri 网的工具总线”。它把建模、抽象、导出和检查串成了一条完整分析链。

### 运行 / 接受 / 转移语义

对 `Time Petri Nets`，运行状态可写成 `(m,\nu)`，其中 `m` 是 marking，`\nu` 记录使能变迁的计时；而 `TINA` 重点关心把这类无限状态压成 state classes：

$$
C = (m, D)
$$

这里 `D` 是 firing-delay 信息形成的约束域。论文明确提到三类 state-class constructions：

$$
\mathrm{SCG}_{std}, \qquad \mathrm{SCG}_{strong}, \qquad \mathrm{SCG}_{atomic}
$$

上式中的符号逐项解释如下：

1. `\mathrm{SCG}_{std}` 是经典 state class graph，保留 markings 与线性时序性质。
2. `\mathrm{SCG}_{strong}` 保留 states 与 `LTL` 相关性质。
3. `\mathrm{SCG}_{atomic}` 进一步保留 states 与 bisimilarity。

对实时性质，论文明确给出两条主路线：

$$
\text{TCTL via observers}, \qquad \text{schedule analysis via plan}
$$

上式中的符号逐项解释如下：

1. `TCTL via observers` 表示通过 observers 把大量 realtime requirements 编译进网结构再检查。
2. `plan` 是 `TINA` 中专门做 firing schedules 路径分析的工具。

### 语义边界

这篇论文的边界也很清楚：

1. 主体仍是 `Petri Net / Time Petri Net` 路线，不是一般 hybrid dynamics。
2. 抽象的保留性质取决于具体 construction，不同 state-class graph 的语义强弱不同。
3. 它强调的是分析环境，不是统一的跨工具标准语义本体。
4. 如果需求更像层次状态机或 interface contract，`TINA` 就不是自然入口。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 时间网骨架 | `$N = (P, T, Pre, Post, m_0, I_s)$` | 固定 `TINA` 处理的核心对象。 |
| 状态类节点 | `$C = (m, D)$` | 用有限抽象表示无限 timed state space。 |
| state-class family | `$\mathrm{SCG}_{std}, \mathrm{SCG}_{strong}, \mathrm{SCG}_{atomic}$` | 不同抽象保留不同性质。 |
| realtime analysis 路线 | `$\text{TCTL via observers}, \text{schedule analysis via plan}$` | `TINA` 不只做 reachability，还覆盖 realtime checking 与 path analysis。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 是离散骨架。 |
| 事件 / 触发 | 强支持 | 变迁 firing 是核心事件。 |
| 守卫 / 数据 | 部分支持 | 核心是时间窗口与结构约束，不是复杂数据。 |
| 层次 | 弱支持 | 主体不是层次状态机。 |
| 并发 / 同步 | 很强 | `Petri Net` 并发语义是母线。 |
| 时间约束 | 很强 | `Time Petri Net` 和 state-class abstractions 是主体。 |
| 连续动态 / 随机性 | 不支持 | 没有一般连续 ODE。 |
| 可执行 / 可验证性 | 很强 | 编辑、仿真、抽象、导出、检查一体化。 |

### 形式化问题与性质

1. `TINA` 的核心不是“又一个 Petri net editor”，而是围绕 preservation class 来选 state-space construction。
2. `persistent sets + covering steps` 体现了它对 untimed combinatorial explosion 的处理。
3. `state classes + observers + plan` 则体现了它对 realtime analysis 的处理。

## 构造方式与承载格式

### 建模入口

论文明确给出：

1. graphical input；
2. textual input；
3. `PNML` 输入；
4. 用户自定义 front-end 也可通过 API 接入。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `TINA / PNML` 输入。
2. abstract timed transition systems 内部表示。
3. abstract Kripke transition systems。
4. textual / binary backend outputs。

### 交换与互操作

这篇论文的互操作是它的强项之一：

1. 前端可把多种输入编译到统一 internal representation。
2. 后端可导出给 `MEC`、`CADP` 等外部 checker。
3. API 允许用户为自己特定模型族开发 front-end。

## 配套基础设施

- 建模/编辑工具：graphic editor + textual input。
- 解析/交换/元模型支持：支持 `PNML` 与自定义 front-end API。
- 仿真/执行支持：usual editing / simulation facilities。
- 验证/分析支持：reachability、coverability、invariants、persistent sets、covering steps、state class graphs、observer-based realtime checking、`plan` path analysis、`selt` model checker。
- 代码生成/转换支持：重点是导出到外部 checker 的 textual / binary backends，而不是代码生成。
- 标准化或社区生态：`TINA` 已进入 `TOPCASED`、`OpenEmbeDD`、`SPICES` 等工程项目。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式系统、并发资源流、工业调度与其他天然适合 `Petri Net / Time Petri Net` 建模的系统。

### 需求前提

1. 需求本体更像 token/resource flow，而不是单控制器状态切换。
2. 关键时序能落到变迁 firing 时间窗口。
3. 需要保留的性质能对应到某类 state-space abstraction。
4. 若要外接 checker，团队需接受 `TINA` 的导出工作流。

### 不适用或高成本场景

若系统主要是层次 statechart、interface protocol 或一般连续动力学，直接走 `TINA` 并不自然。

## 与相邻形式主义的关系

相对 [time-petri-nets/desc.md](../time-petri-nets/desc.md)，本文代表的是 `TPN` 的工程分析环境；相对 [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)，`TINA` 更贴近经典 `Time Petri Net` 与 state-class abstractions；相对 [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)，它直接把 `PNML` 用作输入承载而非只讨论标准本身。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果未来 `project_1` 生成的模型更像并发资源流系统，而不是纯状态机，那么 `Time Petri Net` 路线已经有成熟分析环境可接。

### 作为目标形式主义还是中间表示

对实时并发资源流系统，它可以是直接目标形式主义；对一般控制状态机，更像专门化验证后端。

### 对需求到模型生成的启发

1. 若要接 `TINA`，需求到模型的生成阶段就要显式区分 places、transitions、markings 与 firing intervals。
2. 若需要外部 checker，生成阶段还应考虑 `PNML` 或 `TINA` textual carrier。
3. “同一网导出到不同 checker” 的思路，对后续 `project_1` 的多后端验证设计很有参考价值。

### 现实限制

`TINA` 很成熟，但它解决的是时间网与并发抽象问题，不是通用状态机交换格式。

## 重要的相关工作

- [time-petri-nets/desc.md](../time-petri-nets/desc.md)：`Time Petri Net` 的模型本体与 state-class 方法母线。
- [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)：更偏 `Timed-Arc Petri Net` 的 IDE/verification 路线。
- [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)：`PNML` 承载标准路线。
- [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md)：高层 `Petri Net` 工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Time Petri Nets / TINA`
- 论文角色：time-Petri-net analysis environment
