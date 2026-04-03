# 使用 Uppaal Tiga 的数据路径自适应调度 / Adaptive Scheduling of Data Paths using Uppaal Tiga

## 基本信息

- 标题：Adaptive Scheduling of Data Paths using Uppaal Tiga
- 中文标题：使用 Uppaal Tiga 的数据路径自适应调度
- 作者：Israa AlAttili，Fred Houben，Georgeta Igna，Steffen Michels，Feng Zhu，Frits Vaandrager
- 发表：*Electronic Proceedings in Theoretical Computer Science*，13:1-11，2009
- DOI：`10.4204/EPTCS.13.1`
- 链接：https://doi.org/10.4204/EPTCS.13.1
- 形式主义：`Timed Game Automata / Uppaal Tiga Printer Scheduling Model`
- 主类：⏱️
- 描述客体：🏭
- 所属领域：💻
- 论文角色：不确定到达调度 / `Timed Game Automata` 应用条目
- 工具/实现获取方式：原文明确使用 `Uppaal Tiga` 合成策略，并给出在线模型下载地址。
- 标准/格式获取方式：承载方式是 `Uppaal Tiga` 的 timed game automata templates、controllable/uncontrollable edges 与查询语句；无统一交换标准。

## 简报

这篇论文的关键点，不是“拿 `UPPAAL` 做一次工业调度”，而是明确把 `Timed Automata` 推到了 `Timed Game Automata` 这一支线上。作者处理的是打印机图像处理流水线中的不确定作业到达问题：普通 `UPPAAL` 可以把作业到达时间当成 nondeterminism，但它会在最优搜索时偷偷“预知未来”；`Uppaal Tiga` 则通过 controllable / uncontrollable edges 明确区分控制器和环境，把未知到达时间建成对抗方动作。

- 形式主义定位：这是 `Timed Game Automata` 在工业调度中的代表应用条目，重点是“uncertain job arrivals -> uncontrollable edges -> winning strategy synthesis”。
- 构造方式简述：在原 `Uppaal` 打印机模型上，把不可预测作业的首次到达边改成 uncontrollable，再用 `control:A[] ...` 赢条件搜索最优 trade-off。
- 基础设施与场景简述：依托 `Uppaal Tiga`、打印机 datapath 模型和 observer automata，服务带不确定作业到达的资源调度。

```text
打印机资源与作业路径 -> timed game automata -> uncontrollable arrival -> winning condition -> adaptive scheduling strategy
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 打印机数据路径中的资源组件与作业模板。
2. `DirectCopy` 与 `PrintWithProcessing` 两类循环作业。
3. `Uppaal Tiga` 中的 controllable / uncontrollable 边。
4. 用于度量完成时间的 observer automata 与局部时钟。
5. 以吞吐和服务时间 trade-off 为目标的 winning condition。

### 核心抽象

原文把系统建模为 timed game automata network。结合文中的描述，可保守整理为：

$$
\mathcal{G} = (A_1 \parallel \cdots \parallel A_n, E_c, E_u)
$$

上式中的符号逐项解释如下：

1. `A_1, \ldots, A_n` 是各个资源、作业和 observer 的自动机。
2. `E_c` 是 controllable edges，由 controller 选择。
3. `E_u` 是 uncontrollable edges，由 environment 选择。
4. 两者共同定义了一个 timed game，而不是普通的 reachability 模型。

本文最关键的建模动作是：把 `PrintWithProcessing` 作业的首次到达边放进 `E_u`。这样环境可以在“最坏时刻”激活这个作业，而控制器必须仍然保证时间约束。

论文直接给出了 winning condition：

```text
control:A[] (DC_OBSERVER.INIT imply DC_OBSERVER.x <= FIRST_DC_TIME) &&
(!DC_OBSERVER.INIT imply DC_OBSERVER.x <= DC_TIME) &&
(!DP0.INIT imply DP0.timeSinceArrival <= DP_TIME)
```

这段查询的含义是：

1. 第一份 `DirectCopy` 必须在 `FIRST_DC_TIME` 内完成。
2. 后续 `DirectCopy` 作业之间的间隔不能超过 `DC_TIME`。
3. 任何已到达的 `PrintWithProcessing` 作业都必须在 `DP_TIME` 内完成。

### 一个最小例子与通俗解释

最小例子就是论文反复强调的两类作业竞争 `USBclient`：

1. 一个 `DirectCopy` 作业按已知节奏进入系统。
2. 一个 `PrintWithProcessing` 作业的到达时刻未知。
3. 如果用普通 `UPPAAL` 做最优调度，求解器会假装提前知道未知作业何时到达，从而让关键资源预留出来。
4. 改用 `Uppaal Tiga` 后，这个未知到达必须由环境触发，控制器只能在“完全不知道它何时来”的前提下制定策略。

通俗地说，`Timed Game Automata` 像是在问：“如果世界专门挑你最难受的时候丢来一个新任务，你还能不能保证 SLA？”

### 运行 / 接受 / 转移语义

本文的 game semantics 核心是 controller 与 environment 的职责分裂：

1. environment 决定不可预测作业何时真正到达；
2. controller 决定什么时候占用资源、如何让不同作业排队；
3. 只要存在一种 controller 策略能对抗所有 environment 走法，winning condition 就成立。

原文报告的结论是：在该 case study 上找到了 `6` 个 Pareto-optimal strategies，对应不同的 `DC_TIME / DP_TIME` 折中点。

### 语义边界

论文也明确给出边界：

1. 生成的策略规则集很大，包含数千条规则，不能直接部署到真实打印机控制器中。
2. 模型假设同时在系统中的作业数是有界的。
3. 它适合做“最优折中边界”和“简单策略改进方向”分析，不是直接生成工业控制代码。
4. 但它足以证明 `Timed Game Automata` 对“不确定作业到达”这类问题比普通 `TA` 更贴切。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 游戏网络 | `$\mathcal{G} = (A_1 \parallel \cdots \parallel A_n, E_c, E_u)$` | 在 `TA` 网络上加入 controllable/uncontrollable 边划分。 |
| 不确定到达 | `$e_{arrival} \in E_u$` | 环境而不是控制器决定新作业何时到达。 |
| 赢条件 | `control:A[] ...` | 要求 controller 对所有环境走法都保持 deadline/trade-off 成立。 |
| 结果 | `6` 个 Pareto-optimal strategies | 论文实际求出了多组最优折中解。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 作业、资源和 observer 都是显式位置机。 |
| 事件 / 触发 | 强支持 | 作业到达、资源占用、完成事件都是核心。 |
| 守卫 / 数据 | 部分支持 | 以 clocks 和少量状态变量为主。 |
| 层次 | 不支持 | 核心是平面 timed game automata network。 |
| 并发 / 同步 | 强支持 | 多作业共享资源并发运行。 |
| 时间约束 | 强支持 | 服务时间和吞吐上界就是赢条件主体。 |
| 连续动态 / 随机性 | 不支持 | 不建模连续物理过程，环境是不确定而非概率。 |
| 可执行 / 可验证性 | 强综合 | `Uppaal Tiga` 直接做 strategy synthesis。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先给出打印机 datapath 与资源占用关系。
2. 再把已知作业与未知到达作业建成自动机模板。
3. 将未知作业首次到达边改成 uncontrollable。
4. 最后用 observer 和查询语句表达 trade-off 目标。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `Uppaal Tiga` 模板化 automata。
2. controllable / uncontrollable edge 标记。
3. observer automata 与 local clocks。
4. `control:A[] ...` 查询。

### 交换与互操作

互操作重点在：

1. 从普通 `Uppaal` 模型到 `Uppaal Tiga` 游戏模型的最小改造；
2. 通过 observer 把工业调度指标转成可判定赢条件；
3. 用合成结果反推真实控制器应优先实现哪些简单策略。

## 配套基础设施

- 建模/编辑工具：`Uppaal Tiga`。
- 解析/交换/元模型支持：无统一标准，承载高度工具化。
- 仿真/执行支持：原文主要用于策略合成和与固定策略对比，不直接生成部署代码。
- 验证/分析支持：`Uppaal Tiga` 赢条件求解与 Pareto 折中分析。
- 代码生成/转换支持：原文未给自动代码生成；策略以规则集导出。
- 标准化或社区生态：属于 `UPPAAL-Tiga` / timed controller synthesis 工具线。

## 适用场景与需求前提

### 适用场景

适合带不确定作业到达的工业调度、资源共享流水线、打印/制造/服务系统的在线调度策略综合。

### 需求前提

1. 不确定性需要能明确归到 environment。
2. 控制器可操纵的资源决策点必须可离散枚举。
3. 评价目标最好能写成 deadline、throughput 或 trade-off 上界。
4. 系统规模要足以让 timed game synthesis 仍然可算。

### 不适用或高成本场景

若系统真实部署需要大规模开放作业数、复杂数据依赖或直接可落地控制代码，本文这种游戏策略导出还不够。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文增加的不是参数或冻结时钟，而是 controllable / uncontrollable 两方博弈，因此可稳定挂到 `Timed Game Automata` 分支；相对 [Timed Controller Synthesis: An Industrial Case Study](../timed-controller-synthesis-an-industrial-case-study/desc.md)，两者同属 `TGA` 主线，但本文面向不确定作业到达调度，后者面向物理控制器综合；相对 [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)，两者都关心调度，但这里的关键不是“暂停时钟”，而是“环境对抗未知到达”。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里存在“控制器无法决定、但必须对其鲁棒”的时序触发时，普通 `TA` 可能不足，`Timed Game Automata` 更适合作为验证/综合后端。

### 作为目标形式主义还是中间表示

对在线调度与控制综合任务，它可以直接作为目标形式主义；对一般需求到模型流程，它更适合作为后端博弈求解中间表示。

### 对需求到模型生成的启发

1. 需要在需求抽取阶段显式区分 controllable 和 uncontrollable 事件。
2. “未知到达时间”不能粗暴当作普通 nondeterminism，否则会引入未来信息泄漏。
3. 需求中的 SLA 指标可直接转成 observer + 赢条件查询。

### 现实限制

策略规模膨胀很快，因此从需求自动生成 `TGA` 时必须同步考虑策略简化和部署抽象。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：`TGA` 仍建立在经典 `TA` 的时钟语义之上。
- `UPPAAL-Tiga: Time for Playing Games!`：本文直接依赖该工具线。
- [Timed Controller Synthesis: An Industrial Case Study](../timed-controller-synthesis-an-industrial-case-study/desc.md)：同属 `Uppaal Tiga` 工业应用主线。

## 文献分类总结

- 主类：⏱️
- 描述客体：🏭
- 所属领域：💻
- 形式主义：`Timed Game Automata / Uppaal Tiga Printer Scheduling Model`
- 论文角色：不确定到达调度 / `Timed Game Automata` 应用条目
- 核心功能：在未知作业到达条件下合成可保证 deadline/trade-off 的调度策略
- 关键特性：controllable/uncontrollable edges、observer automata、winning condition、Pareto frontier
- 构造方式：普通 `Uppaal` 模型改造成 `Uppaal Tiga` 游戏模型并求赢策略
- 基础设施：`Uppaal Tiga` 与在线模型
- 适用场景：带不确定作业到达的工业流水线调度
- 需求前提：必须能区分 controller 与 environment 的动作边界
- 状态：🟢
