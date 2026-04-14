# Petrify：并发规格操作与异步控制器综合工具 / Petrify: A Tool for Manipulating Concurrent Specifications and Synthesis of Asynchronous Controllers

## 基本信息

- 标题：Petrify: A Tool for Manipulating Concurrent Specifications and Synthesis of Asynchronous Controllers
- 中文标题：Petrify：并发规格操作与异步控制器综合工具
- 作者：Jordi Cortadella，Michael Kishinevsky，Alex Kondratyev，Luciano Lavagno，Alexandre Yakovlev
- 发表：*IEICE Transactions on Information and Systems*，Vol. E80-D, No. 3，pp. 315-325，1997
- DOI：原文与公开镜像未稳定给出可直接解析的 DOI
- 链接：https://www.cs.upc.edu/~jordicf/Research/gavina/BIB/files/petrify_ieice97.pdf
- 形式主义：`Petrify / Signal Transition Graphs / Petri Nets / Transition Systems`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`STG/PN/TS` 互转、region-based 规约与 speed-independent 异步控制器综合工具总览
- 工具/实现获取方式：原文明确把 `petrify` 作为已实现工具介绍，并系统说明其 `PN/STG/TS -> PN/STG/net-list` 能力；正文未给今天仍可直接访问的官方仓库地址。
- 标准/格式获取方式：核心承载不是独立行业交换标准，而是 `Petri Net`、`Signal Transition Graph`、`Transition System` 与基于 region 的综合约束。

## 简报

这篇论文补的是异步控制器工具链里非常关键的一层基础设施：如何把并发规格从 `TS`、`PN`、`STG` 之间来回变换，并最终落成保持输入输出行为的 speed-independent 控制器网表。它不是单纯介绍一个 GUI 工具，而是把 `region`、`excitation region`、`CSC` 状态编码、逻辑最小化和技术映射整成一条完整的工程流水线。

- 形式主义定位：围绕 `STG/PN/TS` 互转与异步控制器综合的基础设施条目，而不是新的状态机母型。
- 构造方式简述：`TS/PN/STG -> region analysis -> safe irredundant PN or STG -> CSC state assignment -> logic minimization -> speed-independent net-list`。
- 基础设施与场景简述：依托 `region` 理论、`excitation closure`、`CSC` 求解和 target library mapping，服务异步控制器综合、规约、重综合和并发规格调试。

```text
并发规格 -> TS / PN / STG -> regions / excitation regions -> 安全且无冗余的网模型 -> CSC 编码与技术映射 -> speed-independent 控制器
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Transition System (TS)`，用于承载扁平状态行为。
2. `Petri Net (PN)` 与 `Signal Transition Graph (STG)`，用于显式表达并发、因果和冲突。
3. `region / pre-region / post-region`，用于从状态图反推出 Petri 网 place。
4. `excitation region / generalized excitation region`，用于刻画某事件何时可触发。
5. `CSC` 状态编码、逻辑分解与 speed-independent 技术映射。

### 核心抽象

论文的状态规格起点可保守整理为：

$$
TS = (S, s_0, E, \to)
$$

上式中的符号逐项解释如下：

1. `$S$` 是状态集合。
2. `$s_0 \in S$` 是初始状态。
3. `$E$` 是事件集合。
4. `$\to \subseteq S \times E \times S$` 是带事件标签的转移关系。

对应的 Petri 网骨架可写成：

$$
N = (P, T, F, m_0)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合。
2. `$T$` 是 transition 集合，对应 `TS` 中的事件。
3. `$F$` 是流关系。
4. `$m_0$` 是初始 marking。

论文最关键的桥梁对象是 region。若 `$r \subseteq S$`，则它要满足：对任一同标签事件 `$e$` 的所有转移，进入、离开或不穿越 `$r$` 的关系必须一致。由此可把 minimal regions 转成 Petri 网 places。按文中的四条构造规则，可保守写成：

$$
P = R_{\min}, \quad F(r,e)=1 \iff r \in Pre(e), \quad F(e,r)=1 \iff r \in Post(e)
$$

上式中的符号逐项解释如下：

1. `$R_{\min}$` 是所有 minimal regions。
2. `$Pre(e)$` 是事件 `$e$` 的 pre-regions。
3. `$Post(e)$` 是事件 `$e$` 的 post-regions。
4. `$F(r,e)=1$` 表示 place `$r$` 指向 transition `$e$`。
5. `$F(e,r)=1$` 表示 transition `$e$` 指向 place `$r$`。

论文还要求 excitation closure 与 event effectiveness。其核心判据可压成：

$$
\bigcap Pre(e) = GER(e), \qquad Pre(e) \neq \emptyset
$$

上式中的符号逐项解释如下：

1. `$GER(e)$` 是事件 `$e$` 的 generalized excitation region。
2. 第一个式子要求所有 pre-regions 的交恰好刻画 `$e$` 被激发的最大状态集合。
3. 第二个式子要求每个事件至少有一个 pre-region，否则无法在网中为该事件提供可实现的因果前置。

### 一个最小例子与通俗解释

一个很直观的最小例子是请求-应答式异步握手：

1. 环境先发 `req+`。
2. 控制器收到请求后发 `ack+`。
3. 环境撤销请求 `req-`。
4. 控制器撤销应答 `ack-`。

若只用普通状态图，这四步只是线性状态序列；而在 `STG/PN` 里，可以显式表示“`ack+` 依赖 `req+` 已发生”“某些事件可并发”“冲突只由哪些 place 决定”。`petrify` 做的事情，可以理解成把扁平状态图里隐含的并发因果重新挖出来，再重新组装成适合综合的网结构和门级实现。

### 运行 / 接受 / 转移语义

论文的目标不是语言接受，而是行为保持。核心语义关系是：当 excitation closure 与 event effectiveness 成立时，综合得到的 `PN` 与原 `TS` 在可观察事件行为上双模拟。可保守写成：

$$
RG(N) \sim TS
$$

上式中的符号逐项解释如下：

1. `$RG(N)$` 是 Petri 网 `$N$` 的 reachability graph。
2. `$\sim$` 表示文中强调的 bisimilar 行为等价。
3. 这意味着外部观察者无法通过事件序列区分原规格与合成后的网模型。

进入电路综合阶段后，`CSC` 状态编码和单调 cover 条件保证最终网表 speed-independent，即在门延迟分布与多输入变化满足规格前提时保持 hazard-free。

### 语义边界

1. 论文主线针对并发离散规格，不涉及连续动力学或概率语义。
2. `petrify` 的强项是从 `TS/PN/STG` 恢复并发结构并综合异步控制器，不是通用高层 DSL。
3. speed-independent 保证建立在规格和技术映射条件满足的前提上，并非任意布尔电路都自动可得。
4. 对更大系统的组合与层次化管理，原文更多是工具与理论入口，不是完整工程平台说明书。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TS` 骨架 | `$TS=(S,s_0,E,\to)$` | 并发规格的状态级起点。 |
| `PN` 骨架 | `$N=(P,T,F,m_0)$` | 从 region 反推得到的事件级并发模型。 |
| region 到 place 的映射 | `$P=R_{\min}$` | `TS` 中的状态子集被物化为网中的 place。 |
| excitation closure | `$\bigcap Pre(e)=GER(e)$` | 保证从 `TS` 导出的网行为与激发条件一致。 |
| 行为保持 | `$RG(N)\sim TS$` | 综合出的 Petri 网与原状态规格双模拟。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 可从 `TS`、`PN`、`STG` 三种承载之间切换。 |
| 事件 / 触发 | 很强 | 事件标签是 `TS` 与 `STG` 的核心。 |
| 守卫 / 数据 | 弱支持 | 重点是事件因果与并发，不是富数据守卫。 |
| 层次 | 不支持 | 主体是扁平并发规格与网结构。 |
| 并发 / 同步 | 很强 | `PN/STG` 明确承载并发、冲突与因果。 |
| 时间约束 | 不支持 | 不是 timed net 或 timed automata 工具。 |
| 连续动态 / 随机性 | 不支持 | 纯离散异步控制路线。 |
| 可执行 / 可验证性 | 很强 | 能做规约、重综合与 speed-independent 电路实现。 |

### 形式化问题与性质

1. 这篇论文最重要的贡献不是单个算法，而是把 `region` 理论真正落成可操作的工具链。
2. 对 `TS -> PN/STG` 而言，`excitation closure` 与 `event effectiveness` 是行为保持的关键门槛。
3. 对异步电路实现而言，`CSC`、逻辑分解与 monotonic cover 条件共同决定是否能得到 speed-independent 网表。

## 构造方式与承载格式

### 建模入口

原文支持三类直接入口：

1. `Petri Net (PN)`。
2. `Signal Transition Graph (STG)`。
3. `Transition System (TS)`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 带事件标签的 `TS`。
2. `PN/STG` 的 place-transition 结构。
3. `CSC` 编码后的逻辑网络。
4. target gate library 上的异步控制器 net-list。

### 交换与互操作

1. 论文主线是 `TS/PN/STG` 之间的互转，而不是 XML 一类中立交换标准。
2. 回标注到规格层的能力是其工具价值的一部分，因为它让综合过程可被设计者追踪。
3. 它天然适合接在异步控制器规格与门级综合之间，形成“规格 -> 网 -> 实现”的闭环。

## 配套基础设施

- 建模/编辑工具：原文把 `petrify` 本身作为并发规格规约与异步控制器综合工具介绍。
- 解析/交换/元模型支持：`PN`、`STG`、`TS` 三类结构在工具内互转，核心中间对象是 `region` 与 `excitation region`。
- 仿真/执行支持：正文重点不在动态仿真器，而在行为保持的规约与综合。
- 验证/分析支持：token-flow analysis、region extraction、excitation closure 检查、`CSC` 状态编码。
- 代码生成/转换支持：可输出面向 target gate library 的 optimized net-list。
- 标准化或社区生态：原文未给独立标准；其生态价值更多体现在后续 `STG` 异步电路工具链的共同母线地位。

## 适用场景与需求前提

### 适用场景

适合异步控制器综合、并发控制逻辑规约、`STG` 规格重构，以及需要从状态图恢复并发因果结构的场景。

### 需求前提

1. 规格需能稳定表示为 `TS`、`PN` 或 `STG`。
2. 系统关键行为主要是离散事件因果与并发，而不是复杂数据变换。
3. 若目标是电路综合，则需要满足 `CSC` 与 speed-independent 映射前提。
4. 设计者愿意把规格整理成可进行 region 分析的形式。

### 不适用或高成本场景

1. 若系统本质上依赖 dense time、概率或连续动力学，`petrify` 不是自然入口。
2. 若需求主要是高层软件组件协议，不强调异步电路或并发因果，投入 `STG` 建模成本可能偏高。
3. 若系统包含大量富数据守卫和复杂算术，`region` 路线不一定是最合适的主干。

## 与相邻形式主义的关系

相对普通 `FSM`，`STG/PN` 更显式地表达并发、因果和冲突；相对 [design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md](../design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md)，`Workcraft` 更像后来的图形化工作台与组合流程，而 `petrify` 更接近这条 `STG` 综合母线上的核心引擎；相对 [snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md](../snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md)，`Snoopy` 更偏多类图式网建模工作台，而 `petrify` 更聚焦异步控制器综合与 `STG` 规约。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的价值不在“让 LLM 直接生成电路”，而在于补齐一条非常明确的形式化落地路线：

1. 非形式化控制需求若能先被整理成事件级 `TS/STG`，就可以借助 `region` 理论恢复并发结构。
2. 这为“需求到状态机自动建模”提供了一个清晰的目标中间层：不是只有 `FSM`，还可以是显式并发的 `STG/PN`。
3. 它也说明某些控制需求最终是以 speed-independent 约束落地的，这对后续验证与修复阶段很重要。

### 可借鉴点

1. 可把 `region / excitation region` 视为从文本需求抽取“事件依赖”和“可激发条件”的结构化模板。
2. `TS -> STG/PN` 的恢复思想，适合放进 LLM 闭环中的“生成后结构化规约”步骤。
3. `CSC` 与可实现性检查提醒我们：并非所有表面正确的状态机都适合直接实现，仍需可综合性约束。

### 局限与注意事项

1. 原文更关注异步电路与并发规格，不是通用软件状态机标准。
2. 若研究对象主要是带丰富数据与层次结构的控制软件，仍需与 `UML State Machine`、`SCXML`、`Statecharts` 等路线互补。
3. 其价值主要是提供并发控制逻辑的高可信中间模型，而不是覆盖所有需求表达形态。

## 重要的相关工作

1. [design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md](../design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md)：补的是后续 `STG` 异步电路工具工作台和 `petrify` 的集成型流程。
2. [snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md](../snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md)：补的是更宽泛的 graph-based Petri 工作台，不专注异步电路综合。
3. [renew-the-reference-net-workshop/desc.md](../renew-the-reference-net-workshop/desc.md)：补 reference net 与插件式 Petri IDE 生态，可作为 `PN` 侧长期工具背景。

## 文献分类总结

- 这是一篇 `📦 标准、交换格式、元模型与执行载体` 条目，因为核心贡献是把 `TS/PN/STG` 规约、综合和实现做成稳定工具链。
- 这是一篇 `🏗️ 标准/基础设施` 条目，而不是单纯 `🛠️ 方法路线`，因为它提供的是长期可复用的异步控制器综合基础设施。
- 它描述的核心对象是 `🎛️ 控制 / 反应式逻辑`，落点是异步控制器与事件驱动控制行为。
- 它最适合放在 `Petri Net / STG asynchronous-circuit tooling` 这条静态挂接口径下，作为后续 `Workcraft`、仲裁综合和更完整 `STG` 母线的重要前置证据。
