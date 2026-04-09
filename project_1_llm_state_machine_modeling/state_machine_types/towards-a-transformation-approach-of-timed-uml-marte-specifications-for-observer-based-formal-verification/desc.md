# 面向基于观察者形式化验证的定时 UML MARTE 规格转换方法 / Towards a Transformation Approach of Timed UML MARTE Specifications for Observer-Based Formal Verification

## 基本信息

- 标题：Towards a Transformation Approach of Timed UML MARTE Specifications for Observer-Based Formal Verification
- 中文标题：面向基于观察者形式化验证的定时 UML MARTE 规格转换方法
- 作者：Nadia Menad，Philippe Dhaussy，Zoé Drey，Rachida Mekki
- 发表：*Computing and Informatics*，35(2):338-368，2016
- DOI：原文未提供
- 链接：https://www.cai.sk/ojs/index.php/cai/article/view/2381
- 形式主义：`UML MARTE / CCSL / FIACRE / CDL / OBP`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed UML MARTE + CCSL to FIACRE / CDL / OBP verification bridge
- 工具/实现获取方式：论文明确给出 `OBP`、`FIACRE`、`CDL` 工具链，并说明案例完整代码可在 `http://www.obpcdl.org` 获取；整条路线依赖已有的 `UML MARTE -> FIACRE` 变换与 `OBP Explorer`。
- 标准/格式获取方式：核心承载对象是 `UML MARTE` profile、`CCSL` 时间约束、生成的 `FIACRE` 进程、`CDL` observers / contexts 与 `OBP` exploration；其中 `MARTE/CCSL` 属于 `OMG` 标准语言生态。

## 简报

这篇论文的价值，在于把 `UML MARTE + CCSL` 这条本来偏建模和时间约束描述的路线，真正接到了可执行的形式验证后端上。作者不是简单把 `CCSL` 约束翻成某个逻辑公式，而是把 `MARTE` 功能部件、`CCSL` 约束、调度器和 `CDL` 观察者一起编成 `FIACRE` 程序，再交给 `OBP` 做 observer-based verification。

- 形式主义定位：这是定时 `UML MARTE / CCSL` 规格到 formal backend 的验证桥接方法，不是新的 timed automata 母型。
- 构造方式简述：`UML MARTE` 的 `RtUnit / ClockConstraint / DataPool / ports` 等元素被翻成 `FIACRE` functional processes、constraint processes 与 `Scheduler`；性质再用 `CDL` observer automata 编写。
- 基础设施与场景简述：依托 `MARTE`、`CCSL`、`FIACRE`、`CDL` 与 `OBP`，服务实时嵌入式系统的时间约束实现验证与功能需求验证。

```text
UML MARTE model + CCSL constraints -> FIACRE processes + Scheduler -> CDL observers/contexts -> OBP exploration and reachability checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML MARTE` application model；
2. `CCSL` logical clocks 与 clock constraints；
3. 由转换生成的 `FIACRE` functional processes / constraint processes / `Scheduler`；
4. `CDL` observer automata 与 invariants；
5. `OBP` 的 exploration + reject-state reachability verification。

### 核心抽象

论文对 `CCSL` 的最核心定义是：logical clock 表示离散事件发生的 instants 集。可保守写成：

$$
clk = \{t_0,t_1,t_2,\ldots\}
$$

上式中的符号逐项解释如下：

1. `clk` 是一个 logical clock。
2. `t_i` 是该 clock 的第 `i` 个 discrete instant。
3. instants 严格有序。
4. 多个 clocks 之间的关系由 `CCSL` constraints 描述，例如同步、先行和采样。

案例中的时间约束被压成若干 `CCSL` 关系，例如：

$$
\mathrm{write1}\ \mathrm{alternatesWith}\ \mathrm{read1}
$$

$$
\mathrm{read1}\ \mathrm{strictPrec}\ \mathrm{comput}
$$

$$
\mathrm{filterOut} = \mathrm{comput}\ \mathrm{filteredBy}(001)
$$

上式中的符号逐项解释如下：

1. `write1/read1/comput/filterOut` 都是绑定到 `MARTE` 操作上的 logical clocks。
2. `alternatesWith` 约束读写交替。
3. `strictPrec` 约束严格先行。
4. `filteredBy(001)` 表示采样模式，只保留每三个值中的特定位置。

论文还把每个 `CCSL` 约束翻成一个 `FIACRE` constraint process，并由统一的时钟表解释。其核心结构可保守写成：

$$
\mathrm{tab\_Clocks}[i] = (\mathrm{clock\_state},\ \mathrm{enable\_tick},\ \mathrm{dead})
$$

上式中的符号逐项解释如下：

1. `i` 是 clock 编号。
2. `clock_state` 表示该 clock 在当前 instant 的约束求值状态。
3. `enable_tick` 表示当前是否允许触发与该 clock 绑定的功能进程。
4. `dead` 表示该 clock 在剩余执行中是否应失活。

### 一个最小例子与通俗解释

论文的例子很直观：采集电路里 `write1` 和 `read1` 不能乱序。

1. 在 `MARTE` 里，`Sensor1` 写内存 `M1`，`Acq1` 读 `M1`。
2. 在 `CCSL` 里写成 `write1 alternatesWith read1`。
3. 转换后，这条约束会被编成一个 `FIACRE` constraint process，并由 `Scheduler` 决定什么时候允许 `sync_pw1` 和 `sync_pr1` 发生。
4. 再用一个很小的 `CDL` observer 检查“不能先读再写，也不能连续两次写”。

通俗地说，作者把原本“画在 `UML MARTE` 图上的时间约束”，变成了一个真的会在后端里拦住非法时序的调度器加观察者组合。

### 运行 / 接受 / 转移语义

论文的转换链路可保守写成：

$$
\mathrm{MARTE} + \mathrm{CCSL} \xrightarrow{\tau_1} \mathrm{FIACRE} \xrightarrow{\tau_2} \mathrm{OBP\ exploration}
$$

上式中的符号逐项解释如下：

1. `\tau_1` 是 `MARTE/CCSL -> FIACRE` 代码生成。
2. `\tau_2` 是 `FIACRE + CDL` 送入 `OBP` 的探索和验证流程。
3. 第一层把语言对象变成可执行形式化模型。
4. 第二层把性质检查转成 observer/invariant 检查。

`Scheduler` 的工作可进一步压成：

$$
\mathrm{enable\_tick}(i)=\mathrm{true} \iff \mathrm{clock\_state}(i)=2
$$

上式中的符号逐项解释如下：

1. `i` 是某个逻辑时钟的编号。
2. `clock_state(i)=2` 表示相关 constraint processes 已判定该时钟在当前 instant 可触发。
3. 只有这时，对应的同步端口才会被调度。
4. 论文中的 `sync_pw1`、`sync_pr1`、`sync_comput`、`sync_filter` 都遵循这类规则。

性质检查仍被压成 observer 的 reject-state reachability。例如 `P1a` 对应的 observer 可以保守整理为：

$$
O=(Q,q_0,\Sigma,\delta,F_{rej})
$$

其中：

1. `Q` 是 observer 状态集合，如 `Start`、`Sw`、`Reject`。
2. `q_0` 是初始状态 `Start`。
3. `\Sigma` 是 `evt_write1`、`evt_read1` 这类同步事件。
4. `\delta` 是 observer 转移。
5. `F_{rej}` 是错误状态集合。

### 语义边界

这篇论文的边界主要有：

1. 它重点验证 `CCSL` 约束实现和功能需求，不是通用实时语义全集。
2. `MARTE -> FIACRE` 的功能转换本身引用前序工作，本文更聚焦 `CCSL` 和 property bridge。
3. 性质表达重心在 `CDL` observers / invariants，而不是全量 `LTL`。
4. 语义成立依赖 `Scheduler` 作为统一时钟解释器。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| logical clock | `$clk=\{t_0,t_1,t_2,\ldots\}$` | `CCSL` 用有序 instants 表达时间。 |
| 典型约束 | `$\mathrm{write1}\ \mathrm{alternatesWith}\ \mathrm{read1}$` | 用时钟关系表达设计要求。 |
| 调度表项 | `$\mathrm{tab\_Clocks}[i]=(\mathrm{clock\_state},\mathrm{enable\_tick},\mathrm{dead})$` | `Scheduler` 的统一约束解释载体。 |
| 触发规则 | `$\mathrm{enable\_tick}(i)=\mathrm{true} \iff \mathrm{clock\_state}(i)=2$` | 约束满足后才允许功能进程前进一步。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `MARTE` 功能部件、约束自动机与 observers 都有明确状态骨架。 |
| 事件 / 触发 | 很强 | clocks、ports 和 synchronization events 是全链路核心。 |
| 守卫 / 数据 | 中等支持 | 数据池、共享变量和 predicates 可表达功能要求，但主轴仍是时钟关系。 |
| 层次 | 中等支持 | 依托 `UML MARTE` profile 与系统结构。 |
| 并发 / 同步 | 很强 | `Scheduler` 统一驱动多个功能进程与约束进程。 |
| 时间约束 | 很强 | `CCSL` 与 logical clocks 就是论文核心。 |
| 连续动态 / 随机性 | 不支持 | 完全围绕离散 logical clocks 与实时同步。 |
| 可执行 / 可验证性 | 很强 | `MARTE/CCSL -> FIACRE -> CDL/OBP` 工具链完整。 |

### 形式化问题与性质

1. 论文真正解决的是“如何让 `MARTE/CCSL` 这种建模前端进入可验证闭环”。
2. 它把时间约束检查和功能属性检查统一到同一个 `OBP` 流程里。
3. 对本文库而言，这是一条非常典型的 `DSL/profile -> formal backend` 桥接方法。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `UML MARTE` 的 `RtUnit`、`DataPool`、ports、shared resources；
2. `CCSL` logical clocks 与 `ClockConstraint`；
3. 由转换生成的 `FIACRE` functional / constraint processes；
4. `CDL` observers、predicates、invariants 和 contexts。

### 承载格式

机器可处理承载方式包括：

1. `MARTE` profile model；
2. `CCSL` constraint declarations；
3. `FIACRE` 程序；
4. `CDL` property / context scripts；
5. `OBP` 生成的 exploration graph。

### 交换与互操作

这条路线的互操作重点在：

1. 用 `MARTE/CCSL` 保留建模层可读性；
2. 用 `FIACRE` 承接形式后端语义；
3. 用 `CDL/OBP` 承接 observer-based verification；
4. 论文明确把该路线与 `PROMELA`、`Esterel`、`SystemC`、`UPPAAL` 等其他 `CCSL` 验证路径做了对照。

## 配套基础设施

- 建模/编辑工具：`UML MARTE` profile、`CCSL` constraints、case-study model editor。
- 解析/交换/元模型支持：`MARTE -> FIACRE` 变换、clock-number declarations、shared structures。
- 仿真/执行支持：`FIACRE` execution semantics、`Scheduler` 驱动的功能过程同步。
- 验证/分析支持：`CDL` observers / invariants、`OBP`、counterexample reports。
- 代码生成/转换支持：自动生成 `FIACRE` functional processes、constraint processes 与 top-level component。
- 标准化或社区生态：前端依附 `OMG MARTE/CCSL` 标准，后端依附 `FIACRE/OBP` 学术工具链。

## 适用场景与需求前提

### 适用场景

适合以下场景：

1. 实时嵌入式系统已经用 `UML MARTE` 建模。
2. 时间要求天然适合写成 `CCSL` 的先行、交替、采样等关系。
3. 希望在保留模型驱动工程前端的同时，引入 observer-based formal verification。

### 需求前提

1. 系统要能落在 `MARTE` 可翻译子集里。
2. 关键时间关系要能抽成 logical clocks。
3. 性质更适合写成 observers / invariants / contexts，而不是复杂全局时序逻辑。
4. 团队接受 `FIACRE/OBP` 作为下游 formal backend。

### 不适用或高成本场景

如果系统主要依赖连续时间动力学、概率语义或难以翻译的复杂 `UML` 结构，这条路线的收益会下降。

## 与相邻形式主义的关系

相对 [model-checking-of-scade-designed-systems/desc.md](../model-checking-of-scade-designed-systems/desc.md)，那篇是 `SCADE/Lustre -> FIACRE -> CDL/OBP`，这篇则是 `UML MARTE/CCSL -> FIACRE -> CDL/OBP`。相对 [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)，后者走 executable-`UML + OBP2` 统一验证/监控闭环，这篇更偏 `MARTE/CCSL` 时间约束到 `FIACRE` 的形式翻译。相对 [timed-automata-approach-for-motion-planning-using-metric-interval-temporal-logic/desc.md](../timed-automata-approach-for-motion-planning-using-metric-interval-temporal-logic/desc.md)，那篇直接使用 timed automata 作为目标模型，而这篇保留了 `MARTE/CCSL` 语言层。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常贴近“需求到形式模型”的博士主线，因为它证明：像 `MARTE/CCSL` 这种更接近工程师表达习惯的语言，也可以稳定地落到 formal backend 上，不必一开始就要求工程师手写 timed automata。

### 作为目标形式主义还是中间表示

更像工程前端建模语言到 formal backend 的桥接条目，而不是最终验证后端本体。

### 对需求到模型生成的启发

1. LLM 若生成的是 `UML MARTE + CCSL`，后续仍可接形式验证闭环。
2. 时间要求可以先以 clock relations 表达，再在变换阶段落成可执行约束进程。
3. 性质层最好与模型层解耦，保持 observer/invariant 作为独立资产。

### 现实限制

本文并没有把所有 `MARTE` 语义都完整形式化；它更像一条面向特定可翻译子集的强桥接路线。

## 重要的相关工作

1. [model-checking-of-scade-designed-systems/desc.md](../model-checking-of-scade-designed-systems/desc.md)：同样使用 `FIACRE + CDL + OBP` 的同步 DSL 桥接条目。
2. [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)：`UML` 生态下 observer-based verification/monitoring 的另一条路线。
3. [towards-a-model-based-toolchain-for-remote-configuration-and-maintenance-of-space-aware-systems/desc.md](../towards-a-model-based-toolchain-for-remote-configuration-and-maintenance-of-space-aware-systems/desc.md)：展示 `Reactive Blocks + BeSpaceD` 等高层建模语言继续向验证/部署链落地的另一类工具链条目。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`UML MARTE / CCSL / FIACRE / CDL / OBP`
- 论文角色：timed UML MARTE + CCSL to FIACRE / CDL / OBP verification bridge
- 归类理由：论文主体仍围绕 `MARTE/CCSL` 语言对象及其时间约束承载方式展开，方法贡献是把这套 DSL/profile 稳定接到 `FIACRE + CDL + OBP` 验证后端，因此主类归 `🔣`、对象类型归 `🛠️`。
