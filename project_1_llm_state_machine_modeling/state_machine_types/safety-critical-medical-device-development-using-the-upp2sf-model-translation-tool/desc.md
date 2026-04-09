# UPP2SF：用于安全关键医疗设备开发的模型翻译工具 / Safety-critical Medical Device Development using the UPP2SF Model Translation Tool

## 基本信息

- 标题：Safety-critical Medical Device Development using the UPP2SF Model Translation Tool
- 中文标题：UPP2SF：用于安全关键医疗设备开发的模型翻译工具
- 作者：Miroslav Pajic，Zhihao Jiang，Insup Lee，Oleg Sokolsky，Rahul Mangharam
- 发表：*ACM Transactions on Embedded Computing Systems*，13(4s):1-26，2014
- DOI：`10.1145/2584651`
- 链接：https://people.duke.edu/~mp275/pubs/PacemakerUPP2SF_TECS13.pdf
- 形式主义：`UPPAAL Timed Automata / UPP2SF / Stateflow bridge`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：verified-model to Stateflow / code-generation bridge
- 工具/实现获取方式：原文详细描述了 `UPP2SF` 翻译工具与配套 tech report，但未给出稳定的独立公开下载入口。
- 标准/格式获取方式：输入承载是 `UPPAAL` 网络化 timed automata 模型，输出承载是双层 `Simulink/Stateflow` chart 以及后续生成的嵌入式代码。

## 简报

这篇论文最关键的地方，不是 pacemaker 案例本身，而是把“形式验证后的 `UPPAAL` 模型”接到了“可仿真、可测、可生成代码的 `Stateflow` 模型”上。`UPP2SF` 的核心目标，是在 `UPPAAL -> Stateflow -> generated code` 这条链上尽量保持语义一致，并且给出为何这种翻译在一大类模型上是 sound 的论证。对 `project_1` 来说，这正好对应“验证后端”和“工业实现载体”之间的桥。

- 形式主义定位：`UPPAAL` 已验证模型到 `Stateflow` / code generation 的桥接基础设施，而不是新的状态机语言。
- 构造方式简述：输入 `UPPAAL` timed automata network，经 `UPP2SF` 生成双层 `Stateflow` chart，再借助 `Simulink` code generation 输出模块化代码。
- 基础设施与场景简述：依托 `UPPAAL`、`Stateflow`、`Simulink Real-Time Workshop Embedded Coder` 与 `RTOS` 实装流程，服务实时嵌入式控制器从形式验证到实现的落地。

```text
verified UPPAAL model -> UPP2SF translation -> Stateflow chart -> simulation / testing -> generated embedded code
```

## 形式主义定义与核心对象

### 定义对象

论文把 `UPP2SF` 的输入和输出对象都限定得很明确：

1. 输入是 `UPPAAL` 的 timed automata network。
2. 输出是双层 `Stateflow` chart。
3. 额外引入 `Eng` 控制状态与若干 clock states。
4. 目标是得到某个 `maximal progress assumption` 下的执行轨迹对应物。
5. 最终还希望接到自动代码生成与平台测试。

### 核心抽象

论文先重述 `UPPAAL` automaton 的骨架，可保守整理为：

$$
A = (L, l_0, Act, C, V, E, I)
$$

上式中的符号逐项解释如下：

1. `L` 是 locations 集合。
2. `l_0` 是初始 location。
3. `Act` 是动作集合，包含同步动作与空动作。
4. `C` 是 clocks 集合。
5. `V` 是整数或布尔变量集合。
6. `E` 是带 guards 与 resets 的边集合。
7. `I` 为 location invariants。

论文接着给出运行抽取的关键限制：对 `Class LSC` 中的模型，在 maximal progress assumption (`MPA`) 下，所有离散转移都可在整数时间点评估。对任意 clock `x`，其在导出 `Stateflow` 中对应的值定义为：

$$
u^S(x) = n_x + tC_x
$$

上式中的符号逐项解释如下：

1. `u^S(x)` 是 `Stateflow` 侧对 `UPPAAL` clock `x` 的重建值。
2. `n_x` 是 accounting variable，保存上次状态切换前累计的整数时钟值。
3. `tC_x` 是由 `clk` 事件计数得到的当前并行状态局部计数。
4. 这个分解使得 `Stateflow` 即便只按整数 tick 触发，也能重建 `UPPAAL` 的时钟约束。

对无同步边 `l_i \xrightarrow{g,\tau,r} l_j`，论文把其映射为 `Stateflow` transition，可保守写成：

$$
[GC_V(l_i,l_j,g,r)]\ /\ \{RC_V(r); RS(r)\}
$$

上式中的符号逐项解释如下：

1. `GC_V` 把 guards 和 invariants 翻译为 `Stateflow` 条件。
2. `RC_V` 把 clock / variable resets 翻译为赋值语句。
3. `RS(r)` 负责必要的 chart reactivation 控制。

### 一个最小例子与通俗解释

论文在工具介绍部分用一个简单的 `UPPAAL` 网络解释了为什么只在整数 tick 上执行也能抽出一条合法 run：

1. `P0` 有本地 clock `t`，当 `t >= 10` 时发送 `e1!` 并重置 `t=0`。
2. `P1` 通过 `e1?` 与其同步。
3. `UPP2SF` 把每个 automaton 变成一个 parent state，再加一个 `Eng` 状态控制重激活。
4. 每次外部 `clk` 事件触发后，如果某个 transition 在当前 tick 可发生，`Eng` 会继续重入 chart，直到该整数时间点下所有 MPA 转移都处理完。

通俗地说，`UPP2SF` 像“会把 `UPPAAL` 的离散跳转节奏编排成 `Stateflow` 执行节奏的翻译器”。它不是把一个图静态拷贝过去，而是额外加了一层执行引擎来模仿 `UPPAAL` 的 maximal progress 语义。

### 运行 / 接受 / 转移语义

论文对 `UPPAAL` 网络语义写成 transition system：

$$
\langle S, s_0, \rightarrow \rangle
$$

其中运行 `R` 是一串状态转移，而 `MPA` 要求一旦存在更早可发生的离散转移，就不能继续拖延时间。论文据此证明：

$$
\forall k,\ \forall x \in C,\ u^R_k(x) \in \mathbb{N}_0
$$

上式中的符号逐项解释如下：

1. `R` 是某条满足 `MPA` 的运行。
2. `u^R_k(x)` 是第 `k` 步时 clock `x` 的值。
3. 对 `Class LSC` 模型，这些值在离散转移发生点都落在整数时间点。

这一定理是翻译成立的基础，因为它允许 `Stateflow` 只在外部 `clk` tick 时重建 run。为了保证同一 tick 内可能存在多个转移都被处理，论文引入 chart 级控制状态 `Eng` 和本地事件 `tt`，用自激活方式实现：

$$
act = 1 \Rightarrow send(tt)
$$

上式中的符号逐项解释如下：

1. `act` 是 chart reactivation flag。
2. 若在某次处理里有 transition 发生，就把 `act` 置为 `1`。
3. `Eng` 读到该标志后发送 `tt`，在同一外部 `clk` 执行中再次激活整个 chart。

### 语义边界

这篇论文的边界需要特别注意：

1. 只针对 `Class LSC`，即不包含 `x > E` 这类右开 clock 约束的大类 `UPPAAL` 模型。
2. 其 soundness 依赖最大进展假设，而不是覆盖所有非确定时间选择。
3. 输出目标是 `Stateflow` / `Simulink` 这一特定工业载体，不是通用交换格式。
4. 论文案例偏 centralized controller，对分布式实现只在结尾提作未来工作。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `UPPAAL` automaton 骨架 | `$A = (L, l_0, Act, C, V, E, I)$` | 固定翻译输入对象。 |
| `Stateflow` clock 重建 | `$u^S(x) = n_x + tC_x$` | 用计数器与 accounting variable 重建原始 clock 值。 |
| 整数时间点抽取 | `$\forall k,\forall x,\ u^R_k(x)\in\mathbb N_0$` | 说明 `Class LSC` 下可只在整数 tick 上处理转移。 |
| 自激活机制 | `$act = 1 \Rightarrow send(tt)$` | 确保同一外部 `clk` 下所有 MPA 转移都被吃掉。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 保留 `UPPAAL` automata 的 location 骨架。 |
| 事件 / 触发 | 很强 | `clk`、局部事件、broadcast channels 和 input events 都是主线。 |
| 守卫 / 数据 | 强支持 | guards、integer variables、clock resets 被系统翻译。 |
| 层次 | 中等支持 | 输出为双层 `Stateflow` chart，而不是完全扁平图。 |
| 并发 / 同步 | 很强 | `UPPAAL` network 的并发与同步通过 parallel parent states + `Eng` 机制落地。 |
| 时间约束 | 很强 | 整个工具目标就是保持实时语义。 |
| 连续动态 / 随机性 | 不支持 | 输入主体是 timed automata，不处理连续流。 |
| 可执行 / 可验证性 | 很强 | 既保留验证来源，又打通仿真、测试与代码生成。 |

### 形式化问题与性质

1. `UPP2SF` 的关键创新不是简单格式转换，而是附带一个“如何在 `Stateflow` 中模拟 `UPPAAL` MPA 执行”的执行框架。
2. 它还把 WCET 估计回接到 `UPPAAL` 模型级别，而不必等到代码完全生成后再做。
3. 在当前文库里，它补的是 `UPPAAL` verified model 到 `Stateflow` implementation carrier 的桥，而不是新的验证算法。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 在 `UPPAAL` 中建模并完成验证。
2. 用 `UPP2SF` 把 timed automata network 翻译成双层 `Stateflow` chart。
3. 在 `Simulink/Stateflow` 中做仿真和测试。
4. 再用 `Embedded Coder` 生成模块化嵌入式代码。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` XML / timed automata network。
2. `Stateflow` chart、parallel parent states、clock states、`Eng` state。
3. `Simulink` 输入事件 `clk/AinB/VinB` 等。
4. `Embedded Coder` 生成的 C 代码与 RTOS 任务。

### 交换与互操作

这篇论文的互操作重点非常明确：

1. 从 `UPPAAL` 这一形式验证环境桥接到 `Stateflow` 这一工业实现载体。
2. 再由 `Stateflow` 借助 `Simulink` 生态接代码生成与硬件测试。
3. 这条链路比单纯“从 `UPPAAL` 直接生成一坨 C”更利于中间仿真和系统级测试。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 和 `Stateflow`。
- 解析/交换/元模型支持：`UPP2SF` 负责 timed automata 到双层 chart 的结构翻译。
- 仿真/执行支持：`Stateflow` / `Simulink` 闭环仿真，必要时加入环境模型和测试激励。
- 验证/分析支持：前端依赖 `UPPAAL` 验证；模型级 WCET 估计也回到 `UPPAAL` 上完成。
- 代码生成/转换支持：`Simulink Real-Time Workshop Embedded Coder` 生成 C 代码，并可在 `nanoRK` 这类 RTOS 上部署。
- 标准化或社区生态：`UPPAAL`、`Stateflow/Simulink` 与嵌入式代码生成链共同构成工程生态。

## 适用场景与需求前提

### 适用场景

适合已经用 `UPPAAL` 做过早期形式验证、后续又必须进入 `Stateflow/Simulink` 工业流程的实时嵌入式控制器。

### 需求前提

1. 输入模型大体属于论文允许的 `Class LSC`。
2. 系统主要是 timed automata / reactive controller，而不是连续动力学主导。
3. 需要保持验证模型与仿真/实现模型的一致性。
4. 最终实现链条能够接受 `Simulink/Stateflow` 作为中间或最终承载。

### 不适用或高成本场景

如果模型广泛使用论文排除的 clock 条件，或者目标实现并不经过 `Stateflow/Simulink`，这条翻译链的收益就会变小。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，本文不是 `UPPAAL` 教程，而是它到实现载体的桥；相对 [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)，它不是给 `Stateflow` 定义语义，而是把外部已验证模型翻进 `Stateflow`；相对 [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)，`C2E2` 是 `Stateflow -> verifier` 路线，而 `UPP2SF` 是 `verifier -> Stateflow` 路线。

## 与本研究的关系

### 对 Project 1 的价值

它直接说明：如果未来 `project_1` 选择 `UPPAAL` 一类 timed automata 作为验证后端，并不意味着模型生命周期在验证处就结束，还可以继续桥接到 `Stateflow` 这种工业实现载体。

### 作为目标形式主义还是中间表示

`UPPAAL` 更像验证中间表示，`Stateflow` 更像实现侧载体；`UPP2SF` 的意义正是把这两层串起来。

### 对需求到模型生成的启发

1. 若生成目标最终要落到工业控制实现，最好及早考虑与 `Stateflow/Simulink` 一类载体的互操作。
2. 验证模型和实现模型最好不要各写一套，应尽量通过可证明的翻译链连接。
3. 最大进展、事件顺序与时间抽样这类“执行语义细节”必须在桥接层显式编码，而不能留给实现时拍脑袋补。

### 现实限制

它并没有解决所有 `UPPAAL` 模型到实现的桥接问题，而是对一大类可控子类给出了一条可操作、可论证的工程路线。

## 重要的相关工作

- [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：`UPPAAL` 工具和 timed automata 工作流母线。
- [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)：`Stateflow` 语义基础。
- [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)：与本文方向相反的 `Stateflow` 验证后端路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
