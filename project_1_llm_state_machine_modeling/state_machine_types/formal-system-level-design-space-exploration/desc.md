# 形式化系统级设计空间探索 / Formal System-level Design Space Exploration

## 基本信息

- 标题：Formal System-level Design Space Exploration
- 中文标题：形式化系统级设计空间探索
- 作者：Daniel Knorreck，Ludovic Apvrille，Renaud Pacalet
- 发表：*2010 10th Annual International Conference on New Technologies of Distributed Systems (NOTERE)*，pp. 1-8，2010
- DOI：`10.1109/NOTERE.2010.5536852`
- 链接：https://doi.org/10.1109/NOTERE.2010.5536852
- 形式主义：`DIPLODOCUS / TTool / LOTOS- and UPPAAL-backed SoC design-space exploration profile`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：面向 `SoC` 的 UML profile + formal back-end 设计空间探索路线
- 工具/实现获取方式：原文明确说明使用开源 `TTool` 作为 `DIPLODOCUS` 建模前端，并把形式分析接到 `CADP` 与 `UPPAAL`。
- 标准/格式获取方式：承载方式是 `DIPLODOCUS` 的 application / architecture / mapping UML 图，以及生成的 `LOTOS` 与 `UPPAAL` 规格；原文未给独立中立交换标准。

## 简报

这篇论文的关键价值，不是单纯说“`SoC` 可以用 UML 建模”，而是把 `application -> architecture -> mapping` 三段式设计空间探索真正压进 formal back-end。它把 `DIPLODOCUS` 中的 task、channel、event、request、CPU、bus、memory 和 deployment mapping 做成可以自动翻译到 `LOTOS`/`UPPAAL` 的抽象骨架，使设计者在很高抽象层上就能检查 safety、schedulability、bus load 和性能上界，而不是等到低层实现后才发现平台选型不合适。

- 形式主义定位：面向实时嵌入式 `SoC` 的 `UML` profile + formal-analysis 方法路线，不是通用状态机标准。
- 构造方式简述：先分别画应用任务图、硬件架构图和 mapping 图，再由 `Mapping-to-LOTOS`/`UPPAAL` 生成形式规格，最后借助 `CADP`、最长路径分析和模型检查评估设计是否满足约束。
- 基础设施与场景简述：依托 `DIPLODOCUS`、`TTool`、`LOTOS`、`CADP`、`UPPAAL` 与 `Y-chart` 式 application/architecture 分离，服务 `SoC` 平台选型、嵌入式任务映射与早期性能验证。

```text
application tasks + architecture nodes + mapping -> LOTOS/UPPAAL formal specification -> CADP/UPPAAL analysis -> safety / schedulability / bus-load / timing evidence
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `DIPLODOCUS` application modeling：任务、channel、event、request 与 activity-style behavior。
2. hardware architecture modeling：`CPU`、bus、bridge、memory、cache/miss-rate 等节点参数。
3. application-to-architecture mapping：任务上 CPU、channel 上 bus/memory path。
4. `Mapping-to-LOTOS` 形式化语义与 `UPPAAL` 对应语义。
5. 以 safety、schedulability、performance 为主的设计空间探索分析。

### 核心抽象

结合论文对 application / architecture / mapping 三层的组织方式，可以把 `DIPLODOCUS` 条目保守整理为：

$$
D = (\mathcal{A}, \mathcal{H}, \mathcal{M})
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}` 是应用层模型。
2. `\mathcal{H}` 是硬件架构层模型。
3. `\mathcal{M}` 是把应用映射到硬件上的 deployment / mapping 关系。
4. 这是根据论文的 `application diagrams + architecture diagrams + mapping diagrams` 结构做的保守归纳，不是作者逐字给出的单一元组。

应用层还可以进一步保守拆成：

$$
\mathcal{A} = (\mathcal{T}, \mathcal{C}, \mathcal{E}, \mathcal{R})
$$

上式中的符号逐项解释如下：

1. `\mathcal{T}` 是任务集合。
2. `\mathcal{C}` 是 channel 集合。
3. `\mathcal{E}` 是 event 集合。
4. `\mathcal{R}` 是 request 集合。
5. 这对应论文明确列出的三类通信机制以及任务行为骨架。

论文的核心语义变换可以写成：

$$
\mathrm{tf}(D) = L
$$

上式中的符号逐项解释如下：

1. `\mathrm{tf}` 是论文所说的 `Mapping-to-LOTOS` transformation。
2. `D` 是完整的 `DIPLODOCUS` 设计条目。
3. `L` 是生成后的 `LOTOS` 规格。
4. 论文说明这个变换显式编码了 scheduler、communication manager、task state machine 与 cycle-level tick。

结合论文对 `LOTOS` 主进程的描述，可把生成后的核心骨架保守整理为：

$$
L = \mathrm{Sched} \parallel \mathrm{Comm} \parallel \bigparallel_{t \in \mathcal{T}} \mathrm{Task}_t
$$

上式中的符号逐项解释如下：

1. `\mathrm{Sched}` 是每个 `CPU` 上的 scheduling manager。
2. `\mathrm{Comm}` 是跨 `CPU` 的 communication manager。
3. `\mathrm{Task}_t` 是任务 `t` 的 `LOTOS` 状态机过程。
4. `\parallel` 表示并行组合。
5. 这是根据论文对 `Scheduling manager / Communication manager / task state machine` 的文字说明做的保守抽象。

论文还把 mapping 后分析的目标关系收束为“mapping 不应引入新的不安全行为”，其目标可压成：

$$
\mathrm{Trace}_{map}(D) \subseteq \mathrm{Trace}_{app}(\mathcal{A})
$$

上式中的符号逐项解释如下：

1. `\mathrm{Trace}_{map}(D)` 是映射到具体平台后的形式轨迹集合。
2. `\mathrm{Trace}_{app}(\mathcal{A})` 是应用层抽象轨迹集合。
3. 论文把这一点作为 ongoing work 的正确性目标提出，而不是全文已完全证明的定理。

### 一个最小例子与通俗解释

论文里的 `MPEG2` 例子很适合直观说明这条路线：

1. 应用层有 `MPEG Decoder`、`VLC`、`Zigzag`、`IDCT`、`Motion Compensation` 等任务。
2. 这些任务通过 channel 交换 macroblock 样本，通过 event/request 做同步。
3. 设计者可以把全部任务都映射到单 `CPU`，也可以拆到两个 `CPU` 上，并通过 bus/memory 完成通信。
4. 形式后端再检查在给定主频和总线条件下，解码一帧图像需要多少 cycles，以及方案是否可调度。

通俗地说，`DIPLODOCUS` 像是把“系统做什么”和“硬件怎么承载它”先拆开画，再在第三步把两者接起来。它不是先写出最终代码，而是先问一句：如果这些任务这样分配到这些 `CPU` 和 bus 上，系统还能不能按时跑完、会不会卡住、总线会不会爆。

### 运行 / 接受 / 转移语义

论文的语义主线不是语言接受条件，而是 task-level 和 mapping-level 执行语义：

1. application level：任务通过 channel / event / request 交互。
2. mapping level：shared `CPU`、bus、memory 引入 contention、scheduling 和 latency。
3. formal level：`LOTOS` 进程网显式编码调度器、通信管理器和 cycle-based 执行。
4. analysis level：从 reachability graph、最长路径和可达状态推导 safety、schedulability、performance。

论文对三类 channel 明确区分：

1. `BR-BW`：blocking read / blocking write。
2. `BR-NBW`：blocking read / non-blocking write。
3. `NBR-NBW`：non-blocking read / non-blocking write。

这些通信原语之所以关键，是因为它们把任务级建模约束到很少数、但仍足够表达嵌入式控制交互的同步骨架上。

### 语义边界

边界同样很清楚：

1. 这不是低层 RTL 或真实代码语义，而是设计空间探索层的高抽象模型。
2. 数据被强抽象成 sample 数量，不携带具体值。
3. 连续动力学、概率语义和复杂 cache/memory 细节都不在主线内。
4. `UPPAAL` 语义在线里存在，但本文主体更集中于 `LOTOS`/`CADP` 路线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 三层对象骨架 | `$D = (\mathcal{A}, \mathcal{H}, \mathcal{M})$` | 应用、硬件和 mapping 是 `DIPLODOCUS` 的核心分层。 |
| 应用层骨架 | `$\mathcal{A} = (\mathcal{T}, \mathcal{C}, \mathcal{E}, \mathcal{R})$` | 任务、channel、event、request 是主通信对象。 |
| 形式变换 | `$\mathrm{tf}(D) = L$` | `DIPLODOCUS` 图可自动落成 `LOTOS` 规格。 |
| 生成后语义骨架 | `$L = \mathrm{Sched} \parallel \mathrm{Comm} \parallel \bigparallel_{t \in \mathcal{T}} \mathrm{Task}_t$` | 调度、通信和任务过程都进入正式语义。 |
| safety-preserving 目标 | `$\mathrm{Trace}_{map}(D) \subseteq \mathrm{Trace}_{app}(\mathcal{A})$` | mapping 后不应引入新的不安全行为。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 任务行为最后会变成 `LOTOS` 状态机，但前端更像 activity-style task model。 |
| 事件 / 触发 | 很强 | event、request、channel 都是一等通信原语。 |
| 守卫 / 数据 | 中等支持 | 控制结构支持较强，但数据被故意抽象成 sample 数量。 |
| 层次 | 弱支持 | 主线不是层次状态机，而是任务/架构/映射三层分离。 |
| 并发 / 同步 | 很强 | 多任务、多 `CPU`、bus contention 和同步通信是核心。 |
| 时间约束 | 很强 | cycles、主频、总线带宽、latency、schedulability 都是重点。 |
| 连续动态 / 随机性 | 不支持 | 不处理连续物理过程或概率执行。 |
| 可执行 / 可验证性 | 很强 | `TTool -> LOTOS/CADP` 与 `UPPAAL` 构成完整分析链。 |

### 形式化问题与性质

1. 论文真正补的是“高层 UML profile 怎样稳定进入 formal DSE”，而不是单纯提出一个任务图画法。
2. `Y-chart` 式 application / architecture 分离，是它适合做早期设计空间探索的核心原因。
3. 数据强抽象虽然牺牲了功能细节，但换来了 safety / timing / schedulability 分析的可扩展性。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 用 `DIPLODOCUS` application diagrams 描述任务和通信。
2. 用 architecture diagrams 描述 `CPU`、bus、memory、bridge 等平台。
3. 用 deployment/mapping 图把任务和 channel 映射到硬件节点与路径。
4. 自动生成 `LOTOS`/`UPPAAL` 形式规格并触发分析。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `DIPLODOCUS` UML profile 图。
2. `LOTOS` 进程网规格。
3. `CADP` reachability graph。
4. `UPPAAL` 模型与查询。

### 交换与互操作

这条路线的互操作重点不是开放标准文件，而是：

1. `DIPLODOCUS` 图到 `LOTOS`/`UPPAAL` 的自动转换。
2. `TTool` 对 formal back-end 的隐藏式封装。
3. 从 graph analysis 结果回写到 UML 设计空间探索流程。

## 配套基础设施

- 建模/编辑工具：`TTool`。
- 解析/交换/元模型支持：`DIPLODOCUS` profile、mapping-to-`LOTOS`/`UPPAAL` 转换。
- 仿真/执行支持：`TTool` 自带快速仿真能力。
- 验证/分析支持：`CADP` reachability graph、deadlock analysis、graph minimization、最长路径分析，以及 `UPPAAL`。
- 代码生成/转换支持：`LOTOS` 与 `UPPAAL` 形式规格生成；正文不主打部署代码生成。
- 标准化或社区生态：依托 `TTool / TURTLE / AVATAR / DIPLODOCUS` 研究生态，而非独立工业标准。

## 适用场景与需求前提

### 适用场景

适合 `SoC`、实时嵌入式软件/硬件协同设计、任务映射与平台选型，以及需要在实现前快速比较不同映射方案的场景。

### 需求前提

1. 应用可拆成有限任务、显式通信原语和较抽象的 control flow。
2. 平台资源可压成 `CPU/bus/memory` 等参数化节点。
3. 关注点主要是 safety、schedulability、bus load、timing 和性能，而不是位级功能细节。
4. 团队接受强数据抽象与 cycle-level cost model。

### 不适用或高成本场景

如果问题核心在复杂数据语义、连续控制闭环、概率/学习行为或真实缓存/存储层细节，这条路线会过于粗粒度。

## 与相邻形式主义的关系

相对 [avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md](../avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md)，它更强调 `SoC` 级 application / architecture / mapping 分离，而不是系统级安全/安全性共验证；相对 [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)，它更强调设计空间探索和平台映射；相对 [timed-automata-based-analysis-of-embedded-system-architectures/desc.md](../timed-automata-based-analysis-of-embedded-system-architectures/desc.md)，它提供了更完整的 UML 前端与自动翻译链，而不是直接从架构参数手写 timed models。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续要让 LLM 从需求生成“可验证且带平台意识”的状态机工件，那么 application behavior、platform architecture 和 mapping 不能只保留其中一层。

### 作为目标形式主义还是中间表示

更适合作为 architecture-aware 中间表示和 formal-analysis bridge，而不是最终交付给业务用户的通用状态机语言。

### 对需求到模型生成的启发

1. 需求抽取时不能只抓状态和事件，还要抓执行资源、通信介质和 timing cost。
2. 对通信进行“值抽象、保同步骨架”的做法，很适合在生成初期控制状态爆炸。
3. mapping 本身应被视为建模对象，而不是生成后的附加配置。

### 现实限制

它很适合早期架构探索，但不直接回答部署代码、真实数据语义和连续控制细节。

## 重要的相关工作

1. [avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md](../avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md)：同一 `TTool` 生态下更偏系统安全/安全性验证的 `SysML` 路线。
2. [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)：更偏实时 `UML` profile 与 formal validation toolkit。
3. [timed-automata-based-analysis-of-embedded-system-architectures/desc.md](../timed-automata-based-analysis-of-embedded-system-architectures/desc.md)：另一条面向嵌入式架构时序分析的 formal 路线。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 归类理由：论文主体在于把 `DIPLODOCUS` 这一 architecture-aware UML profile 接到 `LOTOS/UPPAAL` 上完成设计空间探索，因此更适合按 `🔣/🛠️` 归类，而不是单纯工具条目。
