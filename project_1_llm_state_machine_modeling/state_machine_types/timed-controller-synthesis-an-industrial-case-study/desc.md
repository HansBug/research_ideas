# 定时控制器综合：一个工业案例研究 / Timed Controller Synthesis: An Industrial Case Study

## 基本信息

- 标题：Timed Controller Synthesis: An Industrial Case Study
- 中文标题：定时控制器综合：一个工业案例研究
- 作者：Franck Cassez，Kim Larsen，Jean-Francois Raskin，Pierre-Alain Reynier
- 发表：书中章节，载于 *Quantitative Model-Based Analysis of Real-Time Embedded Systems*，Springer，2012
- DOI：本轮使用的作者页面与章节 PDF 未标出 DOI
- 链接：https://pageperso.lis-lab.fr/~pierre-alain.reynier/publis/Quasimodo-chap2.pdf
- 形式主义：`Timed Game Automata / UPPAAL-TIGA Oil-Pump Controller Synthesis`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：工业控制综合 / `Timed Game Automata` 分支代表应用条目
- 工具/实现获取方式：原文明确联用 `UPPAAL-TIGA` 做 synthesis，`PHAVER` 做 correctness/robustness verification，`SIMULINK` 做 performance simulation。
- 标准/格式获取方式：承载方式是 `UPPAAL-TIGA` game model、`PHAVER` hybrid verification model 与 `SIMULINK` simulation blocks；无统一交换标准。

## 简报

这篇论文是本轮最能稳定挂树的一篇，因为它直接把 `Timed Game Automata` 用在工业控制器综合上。作者研究的是 `HYDAC` 油泵控制问题：机器消耗油、泵补油、蓄能器油位必须始终在安全区间内，而泵本身又有最小开关间隔。论文先用 `UPPAAL-TIGA` 在抽象 game model 上综合开关策略，再把策略嵌入更细的 hybrid model 里用 `PHAVER` 证明安全与鲁棒，最后用 `SIMULINK` 比较性能。

- 形式主义定位：这是 `Timed Game Automata` 的工业控制综合代表条目，重点是“controller/environment game + robust winning strategy + physical verification loop”。
- 构造方式简述：先把 machine、pump、scheduler 压成一个 one-cycle timed game model，再为每个初始油量区间搜索能保证 `A<> Sched.END` 且 `V_acc` 最小的策略。
- 基础设施与场景简述：依托 `UPPAAL-TIGA`、`PHAVER` 和 `SIMULINK`，服务油泵-蓄能器这类受安全窗口、执行器延迟和环境扰动共同约束的物理控制系统。

```text
安全油位需求 + 周期性耗油 + 泵开关约束 -> timed game model -> strategy synthesis -> hybrid verification -> simulation comparison
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. machine、pump、accumulator 的物理/离散混合描述。
2. one-cycle timed game model 中的 machine automaton、pump automaton 和 scheduler automaton。
3. 初始油量区间 `I_1 = [V_1, V_2]` 与目标终止区间 `I_2`。
4. 累积油量代价变量 `V_acc`。
5. 鲁棒性三元组 `(\delta, \epsilon, f)`，分别对应执行时刻误差、油量测量误差和耗油扰动。

### 核心抽象

结合原文图 1.6-1.8 的模型结构，可把本文的控制综合模型保守整理为：

$$
\mathcal{G}(V_0, I_2) = A_{machine}^u \parallel A_{pump}^c \parallel A_{sched}
$$

上式中的符号逐项解释如下：

1. `A_{machine}^u` 是环境侧 automaton，机器耗油相关边是 uncontrollable。
2. `A_{pump}^c` 是控制器侧 automaton，泵开关边是 controllable。
3. `A_{sched}` 负责离散化时间推进和变量更新。
4. `V_0` 是周期开始时的油量。
5. `I_2` 是一个周期结束时要求达到的目标油量区间。

论文把稳定区间和目标区间定义成：

$$
I_2 = [V_1 + m, V_2 - m]
$$

其中 `m` 是 margin，表示为了鲁棒实施而预留的安全余量。

论文给出的评分函数是：

$$
\mathrm{Score}(V_0, J) = \min \{ K \in \mathbb{N} \mid A(V_0, J) \models \text{control: } A \Diamond \mathrm{Sched.END} \land V_{acc} \le K \}
$$

上式中的符号逐项解释如下：

1. `J` 是目标终止区间。
2. `A(V_0, J)` 是以初始油量 `V_0` 和目标区间 `J` 实例化的 game model。
3. `\mathrm{Sched.END}` 表示成功完成一个周期。
4. `V_{acc}` 是累积油量，用作优化目标。
5. 该式表示：在能保证安全完成周期的前提下，求最小累计油量上界。

### 一个最小例子与通俗解释

论文中的直觉性最强的例子是：

1. pump 最大输出速率是 `2.2 l/s`，而 machine 最大消耗速率是 `2.5 l/s`。
2. 因而控制器不能等油量已经掉到 `V_{min}` 才开泵，否则会来不及补回。
3. 它必须根据周期性耗油模式“提前开泵”，同时还要满足泵至少 `2` 秒才能再次切换的执行器约束。
4. timed game model 就是在回答：面对环境扰动和耗油波动，什么时候开/关泵才始终安全并尽量省油。

通俗地说，这像是在玩一个“有对手的秒表游戏”：环境负责让耗油曲线朝不利方向摆动，控制器负责在受限的开关时刻内守住安全区。

### 运行 / 接受 / 转移语义

论文明确指出：

1. machine automaton 的边是 uncontrollable；
2. pump automaton 的边是 controllable；
3. scheduler 每一步都会更新 `V`、`time` 和 `V_acc`。

作者把一轮控制问题写成稳定区间搜索：找一个 `I_1 = [V_1, V_2]`，使得对所有 `V_0 \in I_1`，都存在策略保证：

$$
A(V_0, I_2) \models \text{control: } A \Diamond \mathrm{Sched.END}
$$

并且在所有这类区间中，`Score(I_1)` 最小。这个“周期末仍回到稳定区间内部”的设计让同一策略可以被反复跨周期调用。

### 语义边界

这篇论文也给出了很明确的边界：

1. 为了让 timed game synthesis 可算，作者只在抽象的一周期模型上做合成。
2. 该模型是 perfect-information game，不处理部分可观测综合。
3. 连续物理行为没有直接在 `UPPAAL-TIGA` 里合成，而是交由 `PHAVER` 的 hybrid verification 补证。
4. 因此它非常适合做“合成-验证-仿真”闭环，但不是直接对完整物理模型做一次性综合。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 游戏模型 | `$\mathcal{G}(V_0, I_2) = A_{machine}^u \parallel A_{pump}^c \parallel A_{sched}$` | 把环境和控制器动作边界写进模型本身。 |
| 目标区间 | `$I_2 = [V_1 + m, V_2 - m]$` | 用 margin 保证周期拼接时的鲁棒余量。 |
| 成本评分 | `$\mathrm{Score}(V_0, J) = \min \{K \mid A(V_0, J) \models \text{control: } A \Diamond \mathrm{Sched.END} \land V_{acc} \le K \}$` | 在满足安全的前提下最小化累计油量。 |
| 鲁棒性检查 | `$(\delta, \epsilon, f)$` | 分别控制时刻误差、油量误差和耗油波动。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | machine、pump、scheduler 都有显式离散模式。 |
| 事件 / 触发 | 强支持 | pump on/off、周期推进、环境扰动都是核心。 |
| 守卫 / 数据 | 强支持 | 油量、时间、累计代价和 margin 都进入 guard/update。 |
| 层次 | 不支持 | 合成模型主体是平面 game automata 组合。 |
| 并发 / 同步 | 支持 | 多个 automata 通过同步更新共享变量。 |
| 时间约束 | 强支持 | 安全窗口、最小开关间隔、周期时刻是主体。 |
| 连续动态 / 随机性 | 部分支持 | 合成模型离散化，连续真实性交由 `PHAVER`/`SIMULINK` 补证。 |
| 可执行 / 可验证性 | 强综合 | `UPPAAL-TIGA` 做 synthesis，`PHAVER` 做 correctness，`SIMULINK` 做 performance。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先写出 machine 的周期性耗油模式和 pump 的开关约束。
2. 对时间和油量做离散化，构造 one-cycle game model。
3. 为不同初始油量搜索能保证安全终止且代价最低的策略。
4. 再把策略嵌入更细的 hybrid model 做鲁棒验证。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL-TIGA` 的 timed game model。
2. `PHAVER` 控制器 automaton 与 hybrid environment。
3. `SIMULINK` block diagram。
4. 由策略导出的 start/stop 时间向量。

### 交换与互操作

互操作重点在：

1. 从抽象 game model 到 concrete hybrid verification model 的嵌入；
2. 从 `UPPAAL-TIGA` 策略到 `SIMULINK` 可执行脚本的转换；
3. 把 synthesis、verification、simulation 串成一个闭环方法。

## 配套基础设施

- 建模/编辑工具：`UPPAAL-TIGA`、`PHAVER`、`SIMULINK`。
- 解析/交换/元模型支持：无统一标准，模型分别绑定到三个工具。
- 仿真/执行支持：`SIMULINK` 用于比较 Bang-Bang、Hydac Smart Controller 和合成策略。
- 验证/分析支持：`UPPAAL-TIGA` 负责 synthesis，`PHAVER` 负责 hybrid correctness/robustness。
- 代码生成/转换支持：论文用脚本把 `UPPAAL-TIGA` 输出策略转成 `SIMULINK` 所需格式。
- 标准化或社区生态：属于 `UPPAAL-Tiga`、hybrid verification 与 control-synthesis 交汇的研究工具线。

## 适用场景与需求前提

### 适用场景

适合具有安全区间、执行器切换约束、环境扰动和周期性负载的物理控制问题，例如油泵、蓄能器、阀门、储能和循环供给系统。

### 需求前提

1. 环境与控制器动作边界必须明确。
2. 系统必须允许抽成可算的一周期 game model。
3. 安全目标和优化目标要能分别写成 winning condition 与 cost bound。
4. 若需要真实物理保证，必须接受后续 hybrid verification / simulation 补证。

### 不适用或高成本场景

如果系统严重依赖部分可观测、长时非周期环境或高维连续控制律，仅靠本文这种抽象 `TGA` 模型就不够。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文从经典 `TA` 主干走向了明确的 controller/environment 二人博弈，因此是 `Timed Game Automata` 的稳定树节点；相对 [Adaptive Scheduling of Data Paths using Uppaal Tiga](../adaptive-scheduling-of-data-paths-using-uppaal-tiga/desc.md)，两者同属 `TGA` 分支，但本文面向物理控制器综合，后者面向不确定作业到达调度；相对 [Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems](../hybrid-automata-for-cps/survey.md)，本文把 hybrid model 放在验证环节，而不是直接把 hybrid automata 当综合目标。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常接近本博士工作想要的“生成-验证-修复”闭环：先合成一个离散/时间控制策略，再回到更细模型里验证其正确性与鲁棒性。

### 作为目标形式主义还是中间表示

对需要策略综合的控制需求，它可以直接作为目标形式主义；对一般需求到模型生成流程，它也非常适合作为后端 synthesis layer。

### 对需求到模型生成的启发

1. 需求抽取时要显式区分安全目标、优化目标和扰动来源。
2. “执行器最小开关间隔”“可接受油位区间”这类约束应优先进入 controllable/uncontrollable 游戏模型。
3. 自动化管线不必要求一步到位；可以先合成，再用更细模型补验证。

### 现实限制

若要把这条路线自动化，最大的难点不是写出一个 `TGA`，而是如何自动挑选足够抽象、但又能在后续验证中保真的 game model。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：`TGA` 仍以经典 `TA` 时钟语义为基底。
- [Adaptive Scheduling of Data Paths using Uppaal Tiga](../adaptive-scheduling-of-data-paths-using-uppaal-tiga/desc.md)：同属 `UPPAAL-Tiga` 工业应用主线。
- [Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems](../hybrid-automata-for-cps/survey.md)：本文的 `PHAVER` 补证阶段与 hybrid/CPS 验证路线直接相关。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：🌡️
- 形式主义：`Timed Game Automata / UPPAAL-TIGA Oil-Pump Controller Synthesis`
- 论文角色：工业控制综合 / `Timed Game Automata` 分支代表应用条目
- 核心功能：在环境扰动下综合安全且近优的油泵控制策略
- 关键特性：controllable/uncontrollable game、stable interval、cost-aware synthesis、hybrid robustness verification
- 构造方式：one-cycle game model + interval search + hybrid verification + simulation comparison
- 基础设施：`UPPAAL-TIGA`、`PHAVER`、`SIMULINK`
- 适用场景：具有安全窗口和执行器切换约束的周期性物理控制系统
- 需求前提：环境动作、控制动作、优化目标和安全区间需可明确分离
- 状态：🟢
